from __future__ import annotations

from pathlib import Path

from pydantic import ValidationError

from app.schemas.comment import RawComment, RawPost
from app.schemas.public_parser import (
    PublicParserPreviewResponse,
    PublicParserStatusItem,
    PublicParserStatusResponse,
)
from app.services.crawling.public_parser.base_public_parser import BasePublicParser, PublicParserResult
from app.services.crawling.public_parser.parser_registry import (
    get_public_parser_platform_ids,
    has_public_parser,
)
from app.services.crawling.public_parser.public_fetcher import PublicFetcher
from app.services.crawling.public_parser.selector_profile import SelectorProfile, load_selector_profile


PUBLIC_PARSER_SOURCE_TYPE = "public_page_parser"
SAFE_PUBLIC_PARSER_PREVIEW_LIMIT = 3

_FIXTURE_FILE_BY_PLATFORM = {
    "the_paper": "the_paper_article.html",
    "jiemian": "jiemian_article.html",
    "hupu": "hupu_thread.html",
    "maimai": "maimai_post.html",
    "tieba": "tieba_thread.html",
    "nga": "nga_thread.html",
}


def get_public_parser_status_response() -> PublicParserStatusResponse:
    fetcher = PublicFetcher.from_env()
    statuses = [
        _status_for_profile(load_selector_profile(platform_id), fetcher)
        for platform_id in get_public_parser_platform_ids()
    ]
    return PublicParserStatusResponse(
        parsers=statuses,
        total=len(statuses),
        live_fetch_enabled_default=fetcher.live_fetch_enabled,
    )


def preview_public_parser(
    platform: str,
    *,
    limit: int = SAFE_PUBLIC_PARSER_PREVIEW_LIMIT,
    use_live_fetch: bool = False,
) -> PublicParserPreviewResponse:
    platform_id = platform.strip().lower()
    if not has_public_parser(platform_id):
        raise ValueError(f"Public parser platform is not registered for '{platform}'.")

    profile = load_selector_profile(platform_id)
    safe_limit = _safe_limit(limit)
    env_fetcher = PublicFetcher.from_env(default_rate_limit_seconds=profile.rate_limit_seconds)
    live_supported = bool(profile.search_url_template)
    live_allowed = use_live_fetch and env_fetcher.live_fetch_enabled and live_supported
    warnings: list[str] = []

    if use_live_fetch and not live_allowed:
        warnings.append("live_fetch_disabled")
    if not _comments_supported(profile):
        warnings.append("comments_unavailable_without_login_or_dynamic_loading")

    if live_allowed:
        parser = BasePublicParser(profile, fetcher=env_fetcher)
        result = parser.search_public_pages("preview", limit=safe_limit)
    else:
        result = _fixture_preview(profile, safe_limit=safe_limit)

    if not result.posts:
        warnings.append("no_sample_posts")

    metadata = dict(result.metadata)
    fallback_reason = (
        metadata.get("fallback_reason_category")
        or ("live_fetch_disabled" if use_live_fetch and not live_allowed else "fixture_preview")
    )
    fallback_used = bool(metadata.get("fallback_used", not live_allowed))
    raw_post_schema_valid = _schema_valid(result.posts, RawPost)
    raw_comment_schema_valid = _schema_valid(result.comments, RawComment)

    return PublicParserPreviewResponse(
        platform=profile.platform_id,
        source_type=str(metadata.get("source_type") or PUBLIC_PARSER_SOURCE_TYPE),
        parser_status=str(metadata.get("parser_status") or profile.status),
        live_fetch_enabled=bool(metadata.get("live_fetch_enabled", live_allowed)),
        live_fetch_attempted=bool(metadata.get("live_fetch_attempted", False)),
        fallback_used=fallback_used,
        fallback_reason_category=str(fallback_reason) if fallback_reason else None,
        post_count=len(result.posts),
        comment_count=len(result.comments),
        raw_post_schema_valid=raw_post_schema_valid,
        raw_comment_schema_valid=raw_comment_schema_valid,
        sample_posts=result.posts[:safe_limit],
        sample_comments=result.comments[:safe_limit],
        warnings=_dedupe(warnings),
    )


def _status_for_profile(
    profile: SelectorProfile,
    env_fetcher: PublicFetcher,
) -> PublicParserStatusItem:
    fixture_available = _fixture_path_for_profile(profile) is not None
    live_fetch_enabled = env_fetcher.live_fetch_enabled and bool(profile.search_url_template)
    return PublicParserStatusItem(
        platform_id=profile.platform_id,
        display_name=profile.display_name,
        source_type=PUBLIC_PARSER_SOURCE_TYPE,
        parser_status=profile.status,
        live_fetch_enabled=live_fetch_enabled,
        fixture_available=fixture_available,
        profile_available=True,
        comments_supported=_comments_supported(profile),
        last_test_status="fixture_available" if fixture_available else "fixture_missing",
        notes=profile.notes,
        safe_limit=SAFE_PUBLIC_PARSER_PREVIEW_LIMIT,
        rate_limit_seconds=profile.rate_limit_seconds,
    )


def _fixture_preview(profile: SelectorProfile, *, safe_limit: int) -> PublicParserResult:
    parser = BasePublicParser(
        profile,
        fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
    )
    fixture_path = _fixture_path_for_profile(profile)
    if fixture_path is not None:
        try:
            html = fixture_path.read_text(encoding="utf-8")
        except OSError:
            html = ""
        if html:
            result = parser.parse_html(
                html,
                source_url=profile.fixture_url or profile.base_url,
                keyword="preview",
                limit=safe_limit,
                metadata_extra={"fetch_status": "fixture"},
            )
            if result.posts:
                metadata = dict(result.metadata)
                metadata.update(
                    {
                        "fallback_used": True,
                        "fallback_reason_category": "fixture_preview",
                        "live_fetch_enabled": False,
                        "live_fetch_attempted": False,
                    }
                )
                return PublicParserResult(
                    posts=result.posts,
                    comments=result.comments,
                    metadata=metadata,
                )

    result = parser.search_public_pages("preview", limit=safe_limit)
    metadata = dict(result.metadata)
    metadata.setdefault("fallback_reason_category", "fixture_missing")
    metadata["fallback_used"] = True
    return PublicParserResult(posts=result.posts, comments=result.comments, metadata=metadata)


def _fixture_path_for_profile(profile: SelectorProfile) -> Path | None:
    candidates: list[Path] = []
    root = _project_root()
    if profile.fixture_path:
        profile_path = Path(profile.fixture_path)
        candidates.append(profile_path if profile_path.is_absolute() else root / profile_path)
    fixture_file = _FIXTURE_FILE_BY_PLATFORM.get(profile.platform_id)
    if fixture_file:
        candidates.append(root / "backend" / "app" / "tests" / "fixtures" / "public_parser" / fixture_file)
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved.exists() and resolved.is_file():
            return resolved
    return None


def _project_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "AGENTS.md").exists():
            return parent
    return current.parents[6]


def _comments_supported(profile: SelectorProfile) -> bool:
    return bool(profile.comment_selector and profile.comment_content_selector)


def _safe_limit(limit: int) -> int:
    if not isinstance(limit, int) or limit <= 0:
        return SAFE_PUBLIC_PARSER_PREVIEW_LIMIT
    return min(limit, SAFE_PUBLIC_PARSER_PREVIEW_LIMIT)


def _schema_valid(items: list[object], model: type[RawPost] | type[RawComment]) -> bool:
    try:
        for item in items:
            if hasattr(item, "model_dump"):
                model.model_validate(item.model_dump(mode="json"))
            else:
                model.model_validate(item)
    except ValidationError:
        return False
    return True


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique
