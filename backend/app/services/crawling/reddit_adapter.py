from __future__ import annotations

import importlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import (
    AdapterHealth,
    AdapterMode,
    BasePlatformAdapter,
    PlatformAdapterError,
)


load_project_env()

MOCK_DATA_DIR = Path(__file__).resolve().parents[4] / "mock_data"
MOCK_POST_LIMIT = 100
MOCK_COMMENT_LIMIT = 500
REAL_POST_LIMIT = 25
REAL_COMMENT_LIMIT = 100
REDDIT_REQUIRED_CREDENTIALS = (
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USER_AGENT",
)
REDDIT_API_APPROVAL_STATUS = "api_pending"


class RedditRealModeError(PlatformAdapterError):
    category = "adapter_error"


class RedditDependencyError(RedditRealModeError):
    category = "dependency_error"


class RedditAuthError(RedditRealModeError):
    category = "auth_error"


class RedditNetworkError(RedditRealModeError):
    category = "network_error"


class RedditParsingError(RedditRealModeError):
    category = "parsing_error"


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
        mode: AdapterMode | None = None,
        credentials: RedditCredentials | None = None,
        http_client: RedditHttpClient | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        requested_mode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.requested_mode: AdapterMode = requested_mode
        self.credentials = credentials or RedditCredentials.from_env()
        self.fallback_reason = ""
        self.real_mode_reached = False
        self.dependency_available = _is_praw_available()
        self.exception_class: str | None = None
        self.sanitized_error_category: str | None = None
        self.mock_available = True
        self.api_pending = _reddit_api_approval_status() == "api_pending"
        self.real_mode_disabled = self.api_pending
        self.api_approval_required = True
        self.api_approval_status = REDDIT_API_APPROVAL_STATUS
        self.selectable_for_real = False
        env_allows_real = self.env_mode == "real"
        effective_mode: AdapterMode = (
            "real"
            if requested_mode == "real"
            and env_allows_real
            and self.credentials
            and not self.real_mode_disabled
            else "mock"
        )
        if requested_mode == "real" and not env_allows_real:
            self.fallback_reason = "reddit_adapter_mode_not_real"
        elif requested_mode == "real" and not self.credentials:
            self.fallback_reason = "missing_reddit_credentials"
        elif requested_mode == "real" and self.real_mode_disabled:
            self.fallback_reason = "reddit_api_approval_pending"
        super().__init__(mode=effective_mode)
        self.http_client = http_client
        if self.http_client is None and self.mode == "real" and self.credentials:
            try:
                self.http_client = _OfficialRedditClient(self.credentials)
                self.dependency_available = True
            except Exception as exc:
                self._record_real_mode_exception(exc)
                self.mode = "mock"
                self.http_client = None

    @property
    def real_mode_available(self) -> bool:
        return self.is_real_mode_enabled()

    def has_required_credentials(self) -> bool:
        return self.credentials is not None

    def get_mode(self) -> AdapterMode:
        return self.mode

    def is_real_mode_enabled(self) -> bool:
        return (
            self.mode == "real"
            and self.has_required_credentials()
            and self.http_client is not None
            and not self.real_mode_disabled
        )

    def health_check(self) -> AdapterHealth:
        if self.is_real_mode_enabled():
            message = "Reddit adapter real mode is configured for public API access."
        elif self.fallback_reason == "reddit_adapter_mode_not_real":
            message = "Reddit adapter requested real mode but REDDIT_ADAPTER_MODE is not real; using mock data."
        elif self.fallback_reason == "missing_reddit_credentials":
            message = "Reddit adapter requested real mode but is using mock data because credentials are missing."
        elif self.fallback_reason == "reddit_api_approval_pending":
            message = "Reddit API approval is pending; real API mode is disabled and mock data is active."
        else:
            message = "Reddit adapter mock mode is active."

        return AdapterHealth(
            platform_id=self.platform_id,
            mode=self.mode,
            ok=True,
            real_mode_available=self.is_real_mode_enabled(),
            message=message,
            fallback_reason=self.fallback_reason,
        )

    def supports_real_mode(self) -> bool:
        return self.has_required_credentials() and self.dependency_available and not self.real_mode_disabled

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "platform_id": self.platform_id,
            "env_mode": self.env_mode,
            "requested_mode": self.requested_mode,
            "active_mode": self.mode,
            "has_required_credentials": self.has_required_credentials(),
            "real_mode_enabled": self.is_real_mode_enabled(),
            "fallback_reason": self.fallback_reason,
            "required_credentials": list(self.get_required_credentials()),
            "real_mode_reached": self.real_mode_reached,
            "dependency_available": self.dependency_available,
            "exception_class": self.exception_class,
            "sanitized_error_category": self.sanitized_error_category,
            "mock_available": self.mock_available,
            "real_mode_available": self.is_real_mode_enabled(),
            "api_approval_required": self.api_approval_required,
            "api_approval_status": self.api_approval_status,
            "api_pending": self.api_pending,
            "real_mode_disabled": self.real_mode_disabled,
            "selectable_for_real": self.selectable_for_real,
            "approval_status": REDDIT_API_APPROVAL_STATUS,
            "praw_installed": _is_praw_available(),
            "praw_required": True,
        }

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return REDDIT_REQUIRED_CREDENTIALS

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        is_real = self.is_real_mode_enabled()
        safe_limit = self.clamp_limit(
            limit,
            default=20,
            maximum=REAL_POST_LIMIT if is_real else MOCK_POST_LIMIT,
        )
        if not is_real:
            return self._search_mock_posts(keyword=keyword, limit=safe_limit)

        try:
            self.real_mode_reached = True
            raw_posts = self.http_client.search_posts(
                keyword,
                limit=safe_limit,
                sort=_normalize_sort(sort),
                date_range=date_range,
            )
            return [self.normalize_post(raw) for raw in raw_posts[:safe_limit]]
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self._record_real_mode_exception(exc)
            return self._search_mock_posts(keyword=keyword, limit=safe_limit)

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        is_real = self.is_real_mode_enabled()
        safe_limit = self.clamp_limit(
            limit,
            default=100,
            maximum=REAL_COMMENT_LIMIT if is_real else MOCK_COMMENT_LIMIT,
        )
        if not is_real:
            return self._fetch_mock_comments(post_id=post_id, limit=safe_limit)

        try:
            self.real_mode_reached = True
            raw_comments = self.http_client.fetch_comments(post_id, limit=safe_limit)
            return [self.normalize_comment(raw) for raw in raw_comments[:safe_limit]]
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self._record_real_mode_exception(exc)
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

    def _record_real_mode_exception(self, exc: Exception) -> None:
        category = _real_mode_error_category(exc)
        safe_exception = exc.__cause__ or exc
        self.sanitized_error_category = category
        self.exception_class = safe_exception.__class__.__name__
        self.fallback_reason = f"{category}:{self.exception_class}"
        if category == "dependency_error":
            self.dependency_available = False


class _OfficialRedditClient:
    """Small PRAW-backed API client used only when credentials are explicitly configured."""

    def __init__(self, credentials: RedditCredentials) -> None:
        self.credentials = credentials
        self.reddit = _build_praw_reddit(credentials)

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del date_range  # Reddit API time filters will be added after fixture validation.
        try:
            submissions = self.reddit.subreddit("all").search(
                keyword,
                sort=sort,
                limit=limit,
                params={"type": "link"},
            )
            return [_submission_to_mapping(submission) for submission in submissions]
        except Exception as exc:
            raise _typed_reddit_exception(exc) from exc

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        clean_post_id = post_id.removeprefix("t3_")
        try:
            submission = self.reddit.submission(id=clean_post_id)
            submission.comment_sort = "confidence"
            submission.comments.replace_more(limit=0)
            return [_comment_to_mapping(comment, post_id=f"t3_{clean_post_id}") for comment in submission.comments.list()[:limit]]
        except Exception as exc:
            raise _typed_reddit_exception(exc) from exc


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


def _build_praw_reddit(credentials: RedditCredentials) -> Any:
    try:
        praw = importlib.import_module("praw")
    except ModuleNotFoundError as exc:
        raise RedditDependencyError("praw_missing") from exc

    try:
        reddit = praw.Reddit(
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            user_agent=credentials.user_agent,
            check_for_async=False,
        )
        reddit.read_only = True
        return reddit
    except Exception as exc:
        raise _typed_reddit_exception(exc) from exc


def _is_praw_available() -> bool:
    try:
        importlib.import_module("praw")
    except ModuleNotFoundError:
        return False
    return True


def _submission_to_mapping(submission: Any) -> Mapping[str, Any]:
    try:
        return {
            "kind": "t3",
            "data": {
                "id": getattr(submission, "id", "unknown"),
                "name": getattr(submission, "name", "") or f"t3_{getattr(submission, 'id', 'unknown')}",
                "author": _reddit_author_name(getattr(submission, "author", None)),
                "author_fullname": _reddit_author_fullname(getattr(submission, "author", None)),
                "title": getattr(submission, "title", ""),
                "selftext": getattr(submission, "selftext", ""),
                "ups": getattr(submission, "ups", getattr(submission, "score", 0)),
                "score": getattr(submission, "score", 0),
                "num_comments": getattr(submission, "num_comments", 0),
                "created_utc": getattr(submission, "created_utc", None),
                "permalink": getattr(submission, "permalink", ""),
                "url": getattr(submission, "url", ""),
            },
        }
    except Exception as exc:
        raise RedditParsingError("submission_mapping_failed") from exc


def _comment_to_mapping(comment: Any, *, post_id: str) -> Mapping[str, Any]:
    try:
        comment_id = getattr(comment, "id", "unknown")
        parent_id = getattr(comment, "parent_id", post_id) or post_id
        return {
            "kind": "t1",
            "data": {
                "id": comment_id,
                "name": getattr(comment, "name", "") or f"t1_{comment_id}",
                "link_id": post_id,
                "parent_id": parent_id,
                "author": _reddit_author_name(getattr(comment, "author", None)),
                "author_fullname": _reddit_author_fullname(getattr(comment, "author", None)),
                "body": getattr(comment, "body", ""),
                "ups": getattr(comment, "ups", getattr(comment, "score", 0)),
                "score": getattr(comment, "score", 0),
                "created_utc": getattr(comment, "created_utc", None),
                "permalink": getattr(comment, "permalink", ""),
            },
        }
    except Exception as exc:
        raise RedditParsingError("comment_mapping_failed") from exc


def _reddit_author_name(author: Any) -> str:
    return "unknown_reddit_author" if author is None else str(author)


def _reddit_author_fullname(author: Any) -> str:
    fullname = getattr(author, "fullname", None)
    return str(fullname) if fullname else _reddit_author_name(author)


def _typed_reddit_exception(exc: Exception) -> RedditRealModeError:
    category = _real_mode_error_category(exc)
    if category == "dependency_error":
        return RedditDependencyError("reddit_dependency_error")
    if category == "auth_error":
        return RedditAuthError("reddit_auth_error")
    if category == "network_error":
        return RedditNetworkError("reddit_network_error")
    if category == "parsing_error":
        return RedditParsingError("reddit_parsing_error")
    return RedditRealModeError("reddit_adapter_error")


def _real_mode_error_category(exc: Exception) -> str:
    if isinstance(exc, RedditRealModeError):
        return exc.category

    class_name = exc.__class__.__name__.lower()
    module_name = exc.__class__.__module__.lower()
    status_code = _status_code_from_exception(exc)

    if "modulenotfound" in class_name or "importerror" in class_name:
        return "dependency_error"
    if status_code in {401, 403}:
        return "auth_error"
    if "oauth" in class_name or "forbidden" in class_name or "unauthorized" in class_name:
        return "auth_error"
    if "permission" in class_name or "auth" in class_name:
        return "auth_error"
    if status_code in {408, 409, 425, 429, 500, 502, 503, 504}:
        return "network_error"
    if "timeout" in class_name or "connection" in class_name or "request" in class_name:
        return "network_error"
    if "server" in class_name or "toomanyrequests" in class_name:
        return "network_error"
    if "jsondecode" in class_name or "decode" in class_name or "parsing" in class_name:
        return "parsing_error"
    if "validation" in class_name or "keyerror" in class_name or "typeerror" in class_name:
        return "parsing_error"
    if "prawcore" in module_name and "response" in class_name:
        return "auth_error" if status_code in {401, 403, None} else "network_error"
    return "adapter_error"


def _status_code_from_exception(exc: Exception) -> int | None:
    for candidate in (exc, getattr(exc, "response", None), getattr(exc, "__cause__", None)):
        status_code = getattr(candidate, "status_code", None) or getattr(candidate, "status", None)
        if isinstance(status_code, int):
            return status_code
    return None


def _normalize_sort(sort: str) -> str:
    allowed = {"relevance", "hot", "new", "top", "comments"}
    normalized = str(sort or "relevance").lower()
    return normalized if normalized in allowed else "relevance"


def _adapter_mode_from_env() -> AdapterMode:
    return _normalize_adapter_mode(os.getenv("REDDIT_ADAPTER_MODE", "mock"))


def _reddit_api_approval_status() -> str:
    return REDDIT_API_APPROVAL_STATUS


def _normalize_adapter_mode(mode: str) -> AdapterMode:
    return "real" if str(mode or "mock").strip().lower() == "real" else "mock"
