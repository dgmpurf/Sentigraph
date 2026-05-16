from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

WEIBO_REQUIRED_CREDENTIALS = (
    "WEIBO_CLIENT_ID",
    "WEIBO_CLIENT_SECRET",
    "WEIBO_ACCESS_TOKEN",
)
WEIBO_API_APPROVAL_STATUS = "planned"
WEIBO_MOCK_POST_LIMIT = 100
WEIBO_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class WeiboCredentials:
    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_env(cls) -> "WeiboCredentials | None":
        client_id = os.getenv("WEIBO_CLIENT_ID", "").strip()
        client_secret = os.getenv("WEIBO_CLIENT_SECRET", "").strip()
        access_token = os.getenv("WEIBO_ACCESS_TOKEN", "").strip()
        if not client_id or not client_secret or not access_token:
            return None
        return cls(client_id=client_id, client_secret=client_secret, access_token=access_token)


class WeiboAdapter(BasePlatformAdapter):
    platform_id = "weibo"
    display_name = "Weibo"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: WeiboCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or WeiboCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = WEIBO_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_weibo_credentials"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:weibo_official_api_not_implemented"

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
        return WEIBO_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = "Weibo official API mode is planned but disabled until approval and implementation are added."
            else:
                message = "Weibo official API mode was requested, but credentials are missing; using mock data."
        else:
            message = "Weibo adapter mock mode is active."

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
        safe_limit = self.clamp_limit(limit, default=20, maximum=WEIBO_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_weibo_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=WEIBO_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_weibo_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _status_payload(raw)
        user = payload.get("user") if isinstance(payload.get("user"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("status_id") or payload.get("idstr") or payload.get("id") or payload.get("mid"),
            default="weibo_unknown_status",
        )
        author_name = self.safe_text(
            payload.get("author_name") or user.get("screen_name") or payload.get("source"),
            default="mock_weibo_author",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("author_id") or user.get("idstr") or user.get("id"), default=author_name),
            author_name=author_name,
            title=self.safe_text(payload.get("title") or payload.get("topic_summary"), default="Weibo topic discussion"),
            content=self.safe_text(payload.get("text") or payload.get("content"), default="Mock Weibo status content."),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("attitudes_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("comments_count"))),
            share_count=max(0, self.coerce_int(payload.get("share_count") or payload.get("reposts_count"))),
            created_at=self.to_utc_iso(payload.get("created_at")),
            url=self.safe_text(payload.get("url"), default=f"https://weibo.com/{post_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        user = payload.get("user") if isinstance(payload.get("user"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("status_id") or payload.get("sid"),
            default="weibo_unknown_status",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("idstr") or payload.get("id") or payload.get("cid"),
            default="weibo_unknown_comment",
        )
        author_name = self.safe_text(
            payload.get("author_name") or user.get("screen_name") or payload.get("source"),
            default="mock_weibo_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("rootid")) or None,
            author_id=self.safe_text(payload.get("author_id") or user.get("idstr") or user.get("id"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("text") or payload.get("content")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("like_counts"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("comments_count"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at")),
            url=self.safe_text(payload.get("url"), default=f"https://weibo.com/{post_id}#comment-{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_weibo_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "weibo",
            "status_id": "weibo_mock_status_001",
            "title": f"#{topic}# service response discussion",
            "text": "Mock public microblog discussing service response timing, clarification needs, and user trust.",
            "author_id": "weibo_mock_media_001",
            "author_name": "Mock Weibo Observer",
            "created_at": "2026-05-15T08:20:00Z",
            "like_count": 2460,
            "reply_count": 136,
            "share_count": 78,
            "url": "https://weibo.com/weibo_mock_status_001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "weibo",
            "status_id": "weibo_mock_status_002",
            "title": f"{topic} customer feedback roundup",
            "text": "Mock Weibo-style post summarizing repeated customer feedback and common complaint phrases.",
            "author_id": "weibo_mock_media_002",
            "author_name": "Mock Consumer Watch",
            "created_at": "2026-05-15T09:05:00Z",
            "like_count": 1810,
            "reply_count": 94,
            "share_count": 52,
            "url": "https://weibo.com/weibo_mock_status_002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "weibo",
            "status_id": "weibo_mock_status_003",
            "title": f"{topic} official statement reaction",
            "text": "Mock microblog reaction comparing the official statement with the most visible public concerns.",
            "author_id": "weibo_mock_media_003",
            "author_name": "Mock Public Response Lab",
            "created_at": "2026-05-15T10:40:00Z",
            "like_count": 1120,
            "reply_count": 63,
            "share_count": 29,
            "url": "https://weibo.com/weibo_mock_status_003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_weibo_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "weibo_mock_status_001"
    return [
        {
            "mode": "mock",
            "platform": "weibo",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "weibo_mock_commenter_001",
            "author_name": "mock_weibo_user_a",
            "content": "Mock comment: users are asking for a clearer timeline and more direct follow-up.",
            "created_at": "2026-05-15T08:26:00Z",
            "like_count": 214,
            "reply_count": 12,
            "url": f"https://weibo.com/{target_post_id}#comment001",
        },
        {
            "mode": "mock",
            "platform": "weibo",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "weibo_mock_commenter_002",
            "author_name": "mock_weibo_user_b",
            "content": "Mock comment: the same wording is being reposted, so repeated-script signals should be watched.",
            "created_at": "2026-05-15T08:31:00Z",
            "like_count": 167,
            "reply_count": 7,
            "url": f"https://weibo.com/{target_post_id}#comment002",
        },
        {
            "mode": "mock",
            "platform": "weibo",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "weibo_mock_commenter_003",
            "author_name": "mock_weibo_user_c",
            "content": "Mock comment: a concise response pinned to the topic page could reduce speculation.",
            "created_at": "2026-05-15T08:39:00Z",
            "like_count": 93,
            "reply_count": 2,
            "url": f"https://weibo.com/{target_post_id}#comment003",
        },
    ]


def _status_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
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
    return _normalize_adapter_mode(os.getenv("WEIBO_ADAPTER_MODE", "mock"))


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
        for credential_name in WEIBO_REQUIRED_CREDENTIALS
    }
