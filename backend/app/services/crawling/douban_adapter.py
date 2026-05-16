from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

DOUBAN_REQUIRED_CREDENTIALS = (
    "DOUBAN_CLIENT_ID",
    "DOUBAN_CLIENT_SECRET",
    "DOUBAN_ACCESS_TOKEN",
)
DOUBAN_API_APPROVAL_STATUS = "planned"
DOUBAN_MOCK_POST_LIMIT = 100
DOUBAN_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class DoubanCredentials:
    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_env(cls) -> "DoubanCredentials | None":
        client_id = os.getenv("DOUBAN_CLIENT_ID", "").strip()
        client_secret = os.getenv("DOUBAN_CLIENT_SECRET", "").strip()
        access_token = os.getenv("DOUBAN_ACCESS_TOKEN", "").strip()
        if not client_id or not client_secret or not access_token:
            return None
        return cls(client_id=client_id, client_secret=client_secret, access_token=access_token)


class DoubanAdapter(BasePlatformAdapter):
    platform_id = "douban"
    display_name = "Douban"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: DoubanCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or DoubanCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = DOUBAN_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_douban_credentials"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:douban_official_api_not_implemented"

        super().__init__(mode="mock")

    def has_required_credentials(self) -> bool:
        return self.credentials is not None

    def get_mode(self) -> AdapterMode:
        return self.mode

    def is_real_mode_enabled(self) -> bool:
        return False

    def supports_real_mode(self) -> bool:
        return False

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return DOUBAN_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = "Douban official API mode is planned but disabled until approval and implementation are added."
            else:
                message = "Douban official API mode was requested, but credentials are missing; using mock data."
        else:
            message = "Douban adapter mock mode is active."

        return AdapterHealth(
            platform_id=self.platform_id,
            mode=self.mode,
            ok=True,
            real_mode_available=False,
            message=message,
            fallback_reason=self.fallback_reason,
        )

    def get_status_metadata(self) -> dict[str, object]:
        fallback_category = _fallback_reason_category(self.fallback_reason)
        return {
            "platform_id": self.platform_id,
            "source_type": "official_api_adapter_scaffold",
            "env_mode": self.env_mode,
            "requested_mode": self.requested_mode,
            "active_mode": self.mode,
            "has_required_credentials": self.has_required_credentials(),
            "real_mode_enabled": False,
            "fallback_reason": self.fallback_reason,
            "required_credentials": list(self.get_required_credentials()),
            "mock_available": self.mock_available,
            "real_mode_available": False,
            "api_approval_required": self.api_approval_required,
            "api_approval_status": self.api_approval_status,
            "api_pending": self.api_pending,
            "real_mode_disabled": self.real_mode_disabled,
            "selectable_for_real": self.selectable_for_real,
            "real_mode_reached": False,
            "dependency_available": True,
            "exception_class": None,
            "sanitized_error_category": fallback_category,
            "fetch_status": fallback_category if fallback_category else "mock",
            "real_mode_blocked_reason": _real_mode_blocked_reason(fallback_category),
            "credentials_present": _credential_presence(),
        }

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        safe_limit = self.clamp_limit(limit, default=20, maximum=DOUBAN_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_douban_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=DOUBAN_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_douban_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _post_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        subject = payload.get("subject") if isinstance(payload.get("subject"), Mapping) else {}
        statistics = payload.get("statistics") if isinstance(payload.get("statistics"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("topic_id")
            or payload.get("review_id")
            or payload.get("post_id")
            or payload.get("id"),
            default="douban_unknown_post",
        )
        author_name = self.safe_text(
            payload.get("author_name") or author.get("name") or payload.get("source"),
            default="mock_douban_author",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("author_id") or author.get("id") or author.get("uid"), default=author_name),
            author_name=author_name,
            title=self.safe_text(
                payload.get("title")
                or payload.get("topic_title")
                or payload.get("review_title")
                or subject.get("title"),
                default="Douban public review or group discussion",
            ),
            content=self.safe_text(
                payload.get("content")
                or payload.get("review_text")
                or payload.get("text")
                or payload.get("description"),
                default="Mock Douban review or group discussion content.",
            ),
            like_count=max(
                0,
                self.coerce_int(
                    payload.get("like_count")
                    or payload.get("useful_count")
                    or payload.get("vote_count")
                    or statistics.get("like_count")
                ),
            ),
            reply_count=max(
                0,
                self.coerce_int(
                    payload.get("reply_count")
                    or payload.get("comment_count")
                    or statistics.get("comment_count")
                ),
            ),
            share_count=max(
                0,
                self.coerce_int(payload.get("share_count") or payload.get("reshare_count") or statistics.get("share_count")),
            ),
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("created_time") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.douban.com/group/topic/{post_id}/"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("topic_id") or payload.get("review_id"),
            default="douban_unknown_post",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("id") or payload.get("cid"),
            default="douban_unknown_comment",
        )
        author_name = self.safe_text(
            payload.get("author_name") or author.get("name") or payload.get("source"),
            default="mock_douban_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("reply_to_comment_id")) or None,
            author_id=self.safe_text(payload.get("author_id") or author.get("id") or author.get("uid"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("content") or payload.get("text")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("useful_count") or payload.get("vote_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("child_comment_count"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("created_time") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.douban.com/group/topic/{post_id}/#comment-{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_douban_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "douban",
            "topic_id": "douban_mock_topic_001",
            "title": f"{topic} group discussion sentiment thread",
            "content": "Mock Douban group post discussing consumer trust, response timing, and repeated community concerns.",
            "author_id": "douban_mock_author_001",
            "author_name": "Mock Douban Group User",
            "created_at": "2026-05-15T08:30:00Z",
            "like_count": 426,
            "reply_count": 68,
            "share_count": 12,
            "url": "https://www.douban.com/group/topic/douban_mock_topic_001/",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "douban",
            "review_id": "douban_mock_review_002",
            "title": f"{topic} review-style public reaction",
            "content": "Mock Douban review summarizing product experience, service gaps, and evidence users expect to see.",
            "author_id": "douban_mock_author_002",
            "author_name": "Mock Douban Reviewer",
            "created_at": "2026-05-15T09:15:00Z",
            "like_count": 318,
            "reply_count": 41,
            "share_count": 9,
            "url": "https://www.douban.com/review/douban_mock_review_002/",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "douban",
            "topic_id": "douban_mock_topic_003",
            "title": f"{topic} community comparison post",
            "content": "Mock Douban discussion comparing user stories and separating verified facts from speculation.",
            "author_id": "douban_mock_author_003",
            "author_name": "Mock Douban Observer",
            "created_at": "2026-05-15T10:05:00Z",
            "like_count": 214,
            "reply_count": 29,
            "share_count": 6,
            "url": "https://www.douban.com/group/topic/douban_mock_topic_003/",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_douban_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "douban_mock_topic_001"
    return [
        {
            "mode": "mock",
            "platform": "douban",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "douban_mock_commenter_001",
            "author_name": "mock_douban_user_a",
            "content": "Mock comment: the discussion needs an official timeline and clearer evidence.",
            "created_at": "2026-05-15T08:44:00Z",
            "like_count": 55,
            "reply_count": 6,
            "url": f"https://www.douban.com/group/topic/{target_post_id}/#comment001",
        },
        {
            "mode": "mock",
            "platform": "douban",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "douban_mock_commenter_002",
            "author_name": "mock_douban_user_b",
            "content": "Mock comment: similar reviews may reflect shared experience, but duplication should be checked.",
            "created_at": "2026-05-15T08:53:00Z",
            "like_count": 37,
            "reply_count": 2,
            "url": f"https://www.douban.com/group/topic/{target_post_id}/#comment002",
        },
        {
            "mode": "mock",
            "platform": "douban",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "douban_mock_commenter_003",
            "author_name": "mock_douban_user_c",
            "content": "Mock comment: a concise public response would help reduce repeated speculation.",
            "created_at": "2026-05-15T09:04:00Z",
            "like_count": 24,
            "reply_count": 1,
            "url": f"https://www.douban.com/group/topic/{target_post_id}/#comment003",
        },
    ]


def _post_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    data = raw.get("data")
    if isinstance(data, Mapping):
        return data
    return raw


def _comment_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    data = raw.get("data")
    if isinstance(data, Mapping):
        return data
    return raw


def _adapter_mode_from_env() -> AdapterMode:
    return _normalize_adapter_mode(os.getenv("DOUBAN_ADAPTER_MODE", "mock"))


def _normalize_adapter_mode(mode: str | None) -> AdapterMode:
    return "real" if str(mode or "mock").strip().lower() == "real" else "mock"


def _fallback_reason_category(fallback_reason: str | None) -> str | None:
    if not fallback_reason:
        return None
    prefix = fallback_reason.split(":", 1)[0].strip().lower()
    if prefix in {"api_pending", "config_error"}:
        return prefix
    if "missing" in fallback_reason.lower():
        return "config_error"
    if "pending" in fallback_reason.lower():
        return "api_pending"
    return "adapter_error"


def _real_mode_blocked_reason(fallback_category: str | None) -> str:
    if fallback_category == "config_error":
        return "credentials_missing"
    if fallback_category == "api_pending":
        return "api_pending"
    return "mock_only"


def _credential_presence() -> dict[str, bool]:
    load_project_env()
    return {
        credential_name: bool(os.getenv(credential_name, "").strip())
        for credential_name in DOUBAN_REQUIRED_CREDENTIALS
    }
