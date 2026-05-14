from __future__ import annotations

import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol
from urllib import parse, request

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterMode, BasePlatformAdapter, PlatformAdapterError


MOCK_DATA_DIR = Path(__file__).resolve().parents[4] / "mock_data"


class RedditHttpClient(Protocol):
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        ...

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        ...


@dataclass(frozen=True)
class RedditCredentials:
    client_id: str
    client_secret: str
    user_agent: str

    @classmethod
    def from_env(cls) -> "RedditCredentials | None":
        client_id = os.getenv("REDDIT_CLIENT_ID", "").strip()
        client_secret = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
        user_agent = os.getenv("REDDIT_USER_AGENT", "").strip()
        if not client_id or not client_secret or not user_agent:
            return None
        return cls(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


class RedditAdapter(BasePlatformAdapter):
    platform_id = "reddit"
    display_name = "Reddit"

    def __init__(
        self,
        *,
        mode: AdapterMode = "mock",
        credentials: RedditCredentials | None = None,
        http_client: RedditHttpClient | None = None,
    ) -> None:
        self.credentials = credentials or RedditCredentials.from_env()
        self.fallback_reason = ""
        effective_mode: AdapterMode = "real" if mode == "real" and self.credentials else "mock"
        if mode == "real" and not self.credentials:
            self.fallback_reason = "missing_reddit_credentials"
        super().__init__(mode=effective_mode)
        self.http_client = http_client or (
            _OfficialRedditClient(self.credentials) if self.mode == "real" and self.credentials else None
        )

    @property
    def real_mode_available(self) -> bool:
        return self.mode == "real" and self.credentials is not None and self.http_client is not None

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        safe_limit = self.clamp_limit(limit, default=20, maximum=100)
        if not self.real_mode_available:
            return self._search_mock_posts(keyword=keyword, limit=safe_limit)

        try:
            raw_posts = self.http_client.search_posts(
                keyword,
                limit=safe_limit,
                sort=_normalize_sort(sort),
                date_range=date_range,
            )
            return [self.normalize_post(raw) for raw in raw_posts[:safe_limit]]
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self.fallback_reason = f"real_mode_error:{exc.__class__.__name__}"
            return self._search_mock_posts(keyword=keyword, limit=safe_limit)

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=500)
        if not self.real_mode_available:
            return self._fetch_mock_comments(post_id=post_id, limit=safe_limit)

        try:
            raw_comments = self.http_client.fetch_comments(post_id, limit=safe_limit)
            return [self.normalize_comment(raw) for raw in raw_comments[:safe_limit]]
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self.fallback_reason = f"real_mode_error:{exc.__class__.__name__}"
            return self._fetch_mock_comments(post_id=post_id, limit=safe_limit)

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _listing_payload(raw)
        post_id = _reddit_id("t3", payload.get("name") or payload.get("id") or "unknown")
        author_name = self.safe_text(payload.get("author"), default="unknown_reddit_author")
        title = self.safe_text(payload.get("title"), default="Untitled Reddit post")
        content = self.safe_text(payload.get("selftext"), default=title)
        permalink = self.safe_text(payload.get("permalink"))

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("author_fullname"), default=author_name),
            author_name=author_name,
            title=title,
            content=content,
            like_count=max(0, self.coerce_int(payload.get("ups") or payload.get("score"))),
            reply_count=max(0, self.coerce_int(payload.get("num_comments"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_utc") or payload.get("created_at")),
            url=_reddit_url(permalink) or self.safe_text(payload.get("url"), default="https://www.reddit.com"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _listing_payload(raw)
        comment_id = _reddit_id("t1", payload.get("name") or payload.get("id") or "unknown")
        link_id = _reddit_id("t3", payload.get("link_id") or payload.get("post_id") or "unknown")
        parent_id = self.safe_text(payload.get("parent_id"))
        if parent_id and parent_id == link_id:
            parent_id = None
        elif parent_id:
            parent_id = _reddit_id("t1", parent_id)

        author_name = self.safe_text(payload.get("author"), default="unknown_reddit_author")
        permalink = self.safe_text(payload.get("permalink"))

        return RawComment(
            platform=self.platform_id,
            post_id=link_id,
            comment_id=comment_id,
            parent_id=parent_id,
            author_id=self.safe_text(payload.get("author_fullname"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("body") or payload.get("content")),
            like_count=max(0, self.coerce_int(payload.get("ups") or payload.get("score"))),
            reply_count=_count_replies(payload.get("replies")),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_utc") or payload.get("created_at")),
            url=_reddit_url(permalink) or f"https://www.reddit.com/comments/{link_id.removeprefix('t3_')}",
            raw_data=self.sanitize_raw_data(payload),
        )

    def _search_mock_posts(self, *, keyword: str, limit: int) -> list[RawPost]:
        comments_by_post: dict[str, list[RawComment]] = {}
        for comment in _load_mock_reddit_comments():
            comments_by_post.setdefault(comment.post_id, []).append(comment)

        posts: list[RawPost] = []
        for post_id, comments in sorted(comments_by_post.items()):
            first_comment = min(comments, key=lambda item: item.created_at)
            interactions = sum(comment.like_count + comment.reply_count + comment.share_count for comment in comments)
            posts.append(
                RawPost(
                    platform=self.platform_id,
                    post_id=post_id,
                    author_id=f"mock_source_{post_id}",
                    author_name="mock_reddit_source",
                    title=f"Mock Reddit discussion for {keyword or 'public opinion'}",
                    content=first_comment.content,
                    like_count=interactions,
                    reply_count=len(comments),
                    share_count=0,
                    created_at=first_comment.created_at,
                    url=f"https://example.com/reddit/{post_id}",
                    raw_data={
                        "mode": "mock",
                        "keyword": keyword,
                        "source": "mock_data/raw_comments.json",
                    },
                )
            )
        return posts[:limit]

    def _fetch_mock_comments(self, *, post_id: str, limit: int) -> list[RawComment]:
        normalized_post_id = post_id.strip()
        comments = _load_mock_reddit_comments()
        matched = [comment for comment in comments if comment.post_id == normalized_post_id]
        return (matched or comments)[:limit]


class _OfficialRedditClient:
    """Small official API client used only when credentials are explicitly configured."""

    token_url = "https://www.reddit.com/api/v1/access_token"
    api_base = "https://oauth.reddit.com"

    def __init__(self, credentials: RedditCredentials) -> None:
        self.credentials = credentials
        self._access_token: str | None = None

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del date_range  # Reddit API time filters will be added after fixture validation.
        query = parse.urlencode({"q": keyword, "limit": limit, "sort": sort, "type": "link"})
        payload = self._get_json(f"{self.api_base}/search?{query}")
        return _children(payload)

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        clean_post_id = post_id.removeprefix("t3_")
        query = parse.urlencode({"limit": limit, "sort": "confidence"})
        payload = self._get_json(f"{self.api_base}/comments/{clean_post_id}?{query}")
        if isinstance(payload, list) and len(payload) > 1:
            return _children(payload[1])
        return []

    def _get_json(self, url: str) -> Any:
        headers = {
            "Authorization": f"Bearer {self._token()}",
            "User-Agent": self.credentials.user_agent,
        }
        return self._request_json(request.Request(url, headers=headers))

    def _token(self) -> str:
        if self._access_token:
            return self._access_token

        auth = f"{self.credentials.client_id}:{self.credentials.client_secret}".encode("utf-8")
        headers = {
            "Authorization": f"Basic {base64.b64encode(auth).decode('ascii')}",
            "User-Agent": self.credentials.user_agent,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        body = parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
        payload = self._request_json(request.Request(self.token_url, data=body, headers=headers, method="POST"))
        token = payload.get("access_token") if isinstance(payload, Mapping) else None
        if not token:
            raise PlatformAdapterError("Reddit token response did not include access_token.")
        self._access_token = str(token)
        return self._access_token

    def _request_json(self, req: request.Request) -> Any:
        last_error: Exception | None = None
        for attempt in range(2):
            try:
                with request.urlopen(req, timeout=10) as response:
                    return json.loads(response.read().decode("utf-8"))
            except Exception as exc:  # pragma: no cover - live network path is not used in MVP tests
                last_error = exc
                if attempt == 0:
                    time.sleep(0.25)
        raise PlatformAdapterError("Reddit API request failed.") from last_error


def _load_mock_reddit_comments() -> list[RawComment]:
    with (MOCK_DATA_DIR / "raw_comments.json").open("r", encoding="utf-8") as file:
        raw_data: list[dict[str, Any]] = json.load(file)
    return [
        RawComment(**item)
        for item in raw_data
        if str(item.get("platform", "")).lower() == "reddit"
    ]


def _listing_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    data = raw.get("data")
    if isinstance(data, Mapping):
        return data
    return raw


def _children(payload: Any) -> list[Mapping[str, Any]]:
    if not isinstance(payload, Mapping):
        return []
    data = payload.get("data")
    if not isinstance(data, Mapping):
        return []
    children = data.get("children")
    if not isinstance(children, list):
        return []
    return [child for child in children if isinstance(child, Mapping) and child.get("kind") != "more"]


def _reddit_id(prefix: str, value: Any) -> str:
    text = str(value or "unknown").strip()
    if not text:
        text = "unknown"
    if text.startswith("t1_") or text.startswith("t3_"):
        return text
    return f"{prefix}_{text}"


def _reddit_url(permalink: str) -> str:
    if not permalink:
        return ""
    if permalink.startswith("http://") or permalink.startswith("https://"):
        return permalink
    return f"https://www.reddit.com{permalink}"


def _count_replies(replies: Any) -> int:
    if not isinstance(replies, Mapping):
        return 0
    return len(_children(replies))


def _normalize_sort(sort: str) -> str:
    allowed = {"relevance", "hot", "new", "top", "comments"}
    normalized = str(sort or "relevance").lower()
    return normalized if normalized in allowed else "relevance"
