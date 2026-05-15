from __future__ import annotations

import hashlib
import re
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.public_parser.html_cleaner import (
    extract_all_text,
    extract_first_text,
    extract_first_text_from_node,
    normalize_text,
    select_nodes,
)
from app.services.crawling.public_parser.public_fetcher import PublicFetcher, PublicFetchResult
from app.services.crawling.public_parser.selector_profile import SelectorProfile


@dataclass(frozen=True)
class PublicParserResult:
    posts: list[RawPost] = field(default_factory=list)
    comments: list[RawComment] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class BasePublicParser:
    """Fixture-first public page parser.

    The parser extracts public article-like pages with selector profiles. It
    never handles authentication, cookies, captcha flows, private messages, or
    hidden data.
    """

    source_type = "public_page_parser"

    def __init__(self, profile: SelectorProfile, *, fetcher: PublicFetcher | None = None) -> None:
        self.profile = profile
        self.fetcher = fetcher or PublicFetcher.from_env(
            default_rate_limit_seconds=profile.rate_limit_seconds
        )
        if self.fetcher.live_fetch_enabled and not self.profile.search_url_template:
            self.fetcher = PublicFetcher(
                live_fetch_enabled=False,
                rate_limit_seconds=self.fetcher.rate_limit_seconds,
                user_agent=self.fetcher.user_agent,
                timeout_seconds=self.fetcher.timeout_seconds,
                max_retries=self.fetcher.max_retries,
            )

    def search_public_pages(self, keyword: str, *, limit: int = 10) -> PublicParserResult:
        safe_limit = _clamp_limit(limit, default=3, maximum=5)
        if not self.fetcher.live_fetch_enabled or not self.profile.search_url_template:
            fixture_result = self._parse_fixture_html_if_available(keyword=keyword, limit=safe_limit)
            posts = self.mock_posts(keyword, limit=safe_limit)
            fallback_reason_category = (
                "live_fetch_disabled"
                if not self.fetcher.live_fetch_enabled
                else "fixture_only"
            )
            if fixture_result.posts:
                metadata = dict(fixture_result.metadata)
                metadata.update(
                    self._metadata(
                        fallback_used=True,
                        fallback_reason_category=fallback_reason_category,
                        post_count=len(fixture_result.posts),
                        comment_count=len(fixture_result.comments),
                        schema_valid=self._schema_valid(
                            fixture_result.posts, fixture_result.comments
                        ),
                        live_fetch_attempted=False,
                        live_fetch_allowed=False,
                        fetch_status=(
                            "disabled"
                            if not self.fetcher.live_fetch_enabled
                            else "fixture_only"
                        ),
                    )
                )
                return PublicParserResult(
                    posts=fixture_result.posts,
                    comments=fixture_result.comments,
                    metadata=metadata,
                )
            return PublicParserResult(
                posts=posts,
                comments=[],
                metadata=self._metadata(
                    fallback_used=True,
                    fallback_reason_category=fallback_reason_category,
                    post_count=len(posts),
                    comment_count=0,
                    schema_valid=self._schema_valid(posts, []),
                    live_fetch_attempted=False,
                    live_fetch_allowed=False,
                    fetch_status="disabled" if not self.fetcher.live_fetch_enabled else "fixture_only",
                ),
            )

        search_url = self.profile.search_url_template.format(
            keyword=urllib.parse.quote_plus(keyword),
            limit=safe_limit,
        )
        fetch_result = self.fetcher.fetch(search_url, self.profile)
        if not fetch_result.ok or not fetch_result.html:
            posts = self.mock_posts(keyword, limit=safe_limit)
            return PublicParserResult(
                posts=posts,
                comments=[],
                metadata=self._metadata(
                    fallback_used=True,
                    fallback_reason_category=fetch_result.fallback_reason_category or "fetch_failed",
                    post_count=len(posts),
                    comment_count=0,
                    schema_valid=self._schema_valid(posts, []),
                    **_fetch_metadata(fetch_result),
                ),
            )
        parsed = self.parse_html(
            fetch_result.html,
            source_url=search_url,
            keyword=keyword,
            limit=safe_limit,
            metadata_extra=_fetch_metadata(fetch_result),
        )
        if not parsed.posts:
            posts = self.mock_posts(keyword, limit=safe_limit)
            metadata = dict(parsed.metadata)
            metadata.update(
                {
                    "fallback_used": True,
                    "fallback_reason_category": parsed.metadata.get("fallback_reason_category") or "selector_missing",
                    "fetch_status": parsed.metadata.get("fallback_reason_category") or "selector_missing",
                    "post_count": len(posts),
                    "comment_count": 0,
                    "schema_valid": self._schema_valid(posts, []),
                    "raw_post_schema_valid": self._schema_valid(posts, []),
                    "raw_comment_schema_valid": True,
                }
            )
            return PublicParserResult(posts=posts, comments=[], metadata=metadata)
        return parsed

    def parse_html(
        self,
        document: str,
        *,
        source_url: str | None = None,
        keyword: str = "",
        limit: int = 10,
        metadata_extra: dict[str, Any] | None = None,
    ) -> PublicParserResult:
        title = extract_first_text(document, self.profile.title_selector)
        content = extract_first_text(document, self.profile.content_selector)
        if not title or not content:
            return PublicParserResult(
                posts=[],
                comments=[],
                metadata=self._metadata(
                    fallback_used=True,
                    fallback_reason_category="selector_missing",
                    post_count=0,
                    comment_count=0,
                    schema_valid=True,
                    **(metadata_extra or {}),
                ),
            )

        author_name = extract_first_text(document, self.profile.author_selector) or "public_source"
        created_at = (
            extract_first_text(document, self.profile.created_at_selector)
            or "2026-05-15T00:00:00Z"
        )
        like_count = self._extract_count(document, self.profile.like_count_selector)
        reply_count = self._extract_count(document, self.profile.reply_count_selector)
        source_url = source_url or self.profile.fixture_url or self.profile.base_url
        post = self._build_post(
            title=title,
            content=content,
            author_name=author_name,
            created_at=created_at,
            source_url=source_url,
            keyword=keyword,
            like_count=like_count,
            reply_count=reply_count,
        )
        comments = self._extract_comments(document, post.post_id, source_url=source_url, limit=limit)
        return PublicParserResult(
            posts=[post],
            comments=comments,
            metadata=self._metadata(
                fallback_used=False,
                fallback_reason_category=None,
                post_count=1,
                comment_count=len(comments),
                schema_valid=self._schema_valid([post], comments),
                **(metadata_extra or {}),
            ),
        )

    def mock_posts(self, keyword: str, *, limit: int = 3) -> list[RawPost]:
        safe_limit = _clamp_limit(limit, default=1, maximum=5)
        posts: list[RawPost] = []
        normalized_keyword = normalize_text(keyword) or "public opinion"
        for index in range(1, safe_limit + 1):
            title = f"{self.profile.display_name} fixture topic: {normalized_keyword}"
            content = (
                f"Fixture-only public-page parser scaffold for {self.profile.display_name}. "
                "Live fetching is disabled by default and no login, cookies, captcha bypass, "
                "anti-bot evasion, proxy rotation, or private data access is used."
            )
            source_url = self.profile.fixture_url or self.profile.base_url
            post_id = self._stable_id("mock", normalized_keyword, str(index))
            posts.append(
                RawPost(
                    platform=self.profile.platform_id,
                    post_id=post_id,
                    author_id=f"{self.profile.platform_id}_public_source",
                    author_name=self.profile.display_name,
                    title=title,
                    content=content,
                    like_count=0,
                    reply_count=0,
                    share_count=0,
                    created_at="2026-05-15T00:00:00Z",
                    url=source_url,
                    raw_data={
                        "mode": "fixture",
                        "source_type": self.source_type,
                        "parser_status": self.profile.status,
                    },
                )
            )
        return posts

    def _extract_comments(
        self,
        document: str,
        post_id: str,
        *,
        source_url: str,
        limit: int,
    ) -> list[RawComment]:
        if not self.profile.comment_selector:
            return []
        comments: list[RawComment] = []
        comment_nodes = select_nodes(document, self.profile.comment_selector)[:limit]
        if comment_nodes:
            for index, comment_node in enumerate(comment_nodes, start=1):
                content = (
                    extract_first_text_from_node(comment_node, self.profile.comment_content_selector)
                    if self.profile.comment_content_selector
                    else comment_node.text_content()
                )
                if not normalize_text(content):
                    continue
                author_name = (
                    extract_first_text_from_node(comment_node, self.profile.comment_author_selector)
                    if self.profile.comment_author_selector
                    else "public_commenter"
                )
                created_at = (
                    extract_first_text_from_node(comment_node, self.profile.comment_created_at_selector)
                    if self.profile.comment_created_at_selector
                    else "2026-05-15T00:00:00Z"
                )
                like_count = self._parse_count(
                    extract_first_text_from_node(comment_node, self.profile.comment_like_selector)
                    if self.profile.comment_like_selector
                    else ""
                )
                floor_number = (
                    extract_first_text_from_node(comment_node, self.profile.comment_floor_selector)
                    if self.profile.comment_floor_selector
                    else ""
                )
                comments.append(
                    self._build_comment(
                        post_id=post_id,
                        content=content,
                        source_url=source_url,
                        index=index,
                        comment_id=comment_node.attrs.get("data-comment-id") or None,
                        parent_id=comment_node.attrs.get("data-parent-id") or None,
                        author_name=author_name,
                        created_at=created_at,
                        like_count=like_count,
                        floor_number=floor_number,
                    )
                )
            return comments
        for index, content in enumerate(extract_all_text(document, self.profile.comment_selector, limit=limit), start=1):
            comments.append(
                self._build_comment(
                    post_id=post_id,
                    content=content,
                    source_url=source_url,
                    index=index,
                )
            )
        return comments

    def _build_post(
        self,
        *,
        title: str,
        content: str,
        author_name: str,
        created_at: str,
        source_url: str,
        keyword: str,
        like_count: int = 0,
        reply_count: int = 0,
    ) -> RawPost:
        post_id = self._stable_id(source_url, title, content[:80])
        return RawPost(
            platform=self.profile.platform_id,
            post_id=post_id,
            author_id=f"{self.profile.platform_id}_public_author",
            author_name=normalize_text(author_name) or "public_source",
            title=normalize_text(title),
            content=normalize_text(content),
            like_count=like_count,
            reply_count=reply_count,
            share_count=0,
            created_at=normalize_text(created_at) or "2026-05-15T00:00:00Z",
            url=source_url,
            raw_data={
                "mode": "public_parser_fixture" if not self.fetcher.live_fetch_enabled else "public_parser_live",
                "source_type": self.source_type,
                "parser_status": self.profile.status,
                "keyword": normalize_text(keyword),
            },
        )

    def _build_comment(
        self,
        *,
        post_id: str,
        content: str,
        source_url: str,
        index: int,
        comment_id: str | None = None,
        parent_id: str | None = None,
        author_name: str = "public_commenter",
        created_at: str = "2026-05-15T00:00:00Z",
        like_count: int = 0,
        floor_number: str | None = None,
    ) -> RawComment:
        comment_id = normalize_text(comment_id) or self._stable_id(post_id, content, str(index))
        raw_data = {
            "mode": "public_parser_fixture",
            "source_type": self.source_type,
            "parser_status": self.profile.status,
        }
        normalized_floor_number = normalize_text(floor_number)
        if normalized_floor_number:
            raw_data["floor_number"] = normalized_floor_number
        return RawComment(
            platform=self.profile.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=normalize_text(parent_id) or None,
            author_id=f"{self.profile.platform_id}_public_commenter",
            author_name=normalize_text(author_name) or "public_commenter",
            content=normalize_text(content),
            like_count=like_count,
            reply_count=0,
            share_count=0,
            created_at=normalize_text(created_at) or "2026-05-15T00:00:00Z",
            url=source_url,
            raw_data=raw_data,
        )

    def _parse_fixture_html_if_available(self, *, keyword: str, limit: int) -> PublicParserResult:
        if not self.profile.fixture_path:
            return PublicParserResult()
        fixture_path = _resolve_project_path(self.profile.fixture_path)
        if fixture_path is None or not fixture_path.exists():
            return PublicParserResult(
                metadata={
                    "fallback_used": True,
                    "fallback_reason_category": "fixture_missing",
                }
            )
        try:
            html = fixture_path.read_text(encoding="utf-8")
        except OSError:
            return PublicParserResult(
                metadata={
                    "fallback_used": True,
                    "fallback_reason_category": "fixture_unreadable",
                }
            )
        return self.parse_html(
            html,
            source_url=self.profile.fixture_url or self.profile.base_url,
            keyword=keyword,
            limit=limit,
            metadata_extra={"fetch_status": "fixture"},
        )

    def _extract_count(self, document: str, selector: str | None) -> int:
        if not selector:
            return 0
        return self._parse_count(extract_first_text(document, selector))

    def _parse_count(self, value: str | None) -> int:
        text = normalize_text(value)
        if not text:
            return 0
        match = re.search(r"\d[\d,]*", text)
        if not match:
            return 0
        return min(int(match.group(0).replace(",", "")), 10_000_000)

    def _metadata(
        self,
        *,
        fallback_used: bool,
        fallback_reason_category: str | None,
        post_count: int,
        comment_count: int,
        schema_valid: bool,
        live_fetch_attempted: bool | None = None,
        live_fetch_allowed: bool | None = None,
        fetch_status: str | None = None,
    ) -> dict[str, Any]:
        return {
            "platform": self.profile.platform_id,
            "source_type": self.source_type,
            "parser_status": self.profile.status,
            "live_fetch_enabled": self.fetcher.live_fetch_enabled,
            "live_fetch_attempted": bool(live_fetch_attempted) if live_fetch_attempted is not None else False,
            "live_fetch_allowed": bool(live_fetch_allowed) if live_fetch_allowed is not None else False,
            "fallback_used": fallback_used,
            "fallback_reason_category": fallback_reason_category,
            "fetch_status": fetch_status,
            "post_count": post_count,
            "comment_count": comment_count,
            "schema_valid": schema_valid,
            "raw_post_schema_valid": schema_valid,
            "raw_comment_schema_valid": schema_valid,
        }

    def _schema_valid(self, posts: list[RawPost], comments: list[RawComment]) -> bool:
        try:
            for post in posts:
                RawPost.model_validate(post.model_dump(mode="json"))
            for comment in comments:
                RawComment.model_validate(comment.model_dump(mode="json"))
        except ValidationError:
            return False
        return True

    def _stable_id(self, *parts: str) -> str:
        digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]
        return f"{self.profile.platform_id}_{digest}"


def _clamp_limit(limit: int, *, default: int, maximum: int) -> int:
    if not isinstance(limit, int) or limit <= 0:
        return default
    return min(limit, maximum)


def _resolve_project_path(path_value: str) -> Path | None:
    path = Path(path_value)
    root = _project_root()
    candidate = path if path.is_absolute() else root / path
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None
    return resolved


def _project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    return current.parents[5]


def _fetch_metadata(fetch_result: PublicFetchResult) -> dict[str, Any]:
    return {
        "live_fetch_attempted": fetch_result.live_fetch_attempted,
        "live_fetch_allowed": fetch_result.live_fetch_allowed,
        "fetch_status": fetch_result.fetch_status,
    }
