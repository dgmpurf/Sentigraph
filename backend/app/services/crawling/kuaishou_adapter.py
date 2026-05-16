from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

KUAISHOU_REQUIRED_CREDENTIALS = (
    "KUAISHOU_CLIENT_ID",
    "KUAISHOU_CLIENT_SECRET",
    "KUAISHOU_ACCESS_TOKEN",
)
KUAISHOU_API_APPROVAL_STATUS = "planned"
KUAISHOU_MOCK_POST_LIMIT = 100
KUAISHOU_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class KuaishouCredentials:
    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_env(cls) -> "KuaishouCredentials | None":
        client_id = os.getenv("KUAISHOU_CLIENT_ID", "").strip()
        client_secret = os.getenv("KUAISHOU_CLIENT_SECRET", "").strip()
        access_token = os.getenv("KUAISHOU_ACCESS_TOKEN", "").strip()
        if not client_id or not client_secret or not access_token:
            return None
        return cls(client_id=client_id, client_secret=client_secret, access_token=access_token)


class KuaishouAdapter(BasePlatformAdapter):
    platform_id = "kuaishou"
    display_name = "Kuaishou"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: KuaishouCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or KuaishouCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = KUAISHOU_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_kuaishou_credentials"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:kuaishou_official_api_not_implemented"

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
        return KUAISHOU_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = "Kuaishou official API mode is planned but disabled until approval and implementation are added."
            else:
                message = "Kuaishou official API mode was requested, but credentials are missing; using mock data."
        else:
            message = "Kuaishou adapter mock mode is active."

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
        safe_limit = self.clamp_limit(limit, default=20, maximum=KUAISHOU_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_kuaishou_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=KUAISHOU_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_kuaishou_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _video_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        statistics = payload.get("statistics") if isinstance(payload.get("statistics"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("photo_id") or payload.get("video_id") or payload.get("work_id") or payload.get("id"),
            default="kuaishou_unknown_video",
        )
        author_name = self.safe_text(
            payload.get("creator_name") or author.get("name") or author.get("nickname") or payload.get("source"),
            default="mock_kuaishou_creator",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("creator_id") or author.get("id") or author.get("user_id"), default=author_name),
            author_name=author_name,
            title=self.safe_text(payload.get("title") or payload.get("topic_summary"), default="Kuaishou short-video discussion"),
            content=self.safe_text(payload.get("description") or payload.get("caption") or payload.get("content"), default="Mock Kuaishou video description."),
            like_count=max(0, self.coerce_int(payload.get("like_count") or statistics.get("like_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or statistics.get("comment_count"))),
            share_count=max(0, self.coerce_int(payload.get("share_count") or statistics.get("share_count"))),
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("create_time")),
            url=self.safe_text(payload.get("url") or payload.get("share_url"), default=f"https://www.kuaishou.com/short-video/{post_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        user = payload.get("user") if isinstance(payload.get("user"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("photo_id") or payload.get("video_id") or payload.get("work_id"),
            default="kuaishou_unknown_video",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("cid") or payload.get("id"),
            default="kuaishou_unknown_comment",
        )
        author_name = self.safe_text(
            payload.get("author_name") or user.get("name") or user.get("nickname") or payload.get("source"),
            default="mock_kuaishou_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("reply_id")) or None,
            author_id=self.safe_text(payload.get("author_id") or user.get("id") or user.get("user_id"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("content") or payload.get("text")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("liked_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("sub_comment_count"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.kuaishou.com/short-video/{post_id}#comment-{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_kuaishou_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "kuaishou",
            "photo_id": "kuaishou_mock_video_001",
            "title": f"{topic} short-video discussion",
            "description": "Mock Kuaishou video collecting public reactions about service follow-up, product trust, and response clarity.",
            "creator_id": "kuaishou_mock_creator_001",
            "creator_name": "Mock Kuaishou Observer",
            "created_at": "2026-05-15T08:55:00Z",
            "like_count": 3260,
            "reply_count": 184,
            "share_count": 102,
            "url": "https://www.kuaishou.com/short-video/kuaishou_mock_video_001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "kuaishou",
            "photo_id": "kuaishou_mock_video_002",
            "title": f"{topic} livestream replay reaction",
            "description": "Mock livestream-style recap where viewers discuss complaint handling and whether the response feels timely.",
            "creator_id": "kuaishou_mock_creator_002",
            "creator_name": "Mock Live Notes",
            "created_at": "2026-05-15T09:35:00Z",
            "like_count": 1980,
            "reply_count": 121,
            "share_count": 76,
            "url": "https://www.kuaishou.com/short-video/kuaishou_mock_video_002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "kuaishou",
            "photo_id": "kuaishou_mock_video_003",
            "title": f"{topic} creator response analysis",
            "description": "Mock Kuaishou creator analysis of rumor control, public response tone, and high-risk comment themes.",
            "creator_id": "kuaishou_mock_creator_003",
            "creator_name": "Mock Short Video Watch",
            "created_at": "2026-05-15T10:20:00Z",
            "like_count": 1260,
            "reply_count": 82,
            "share_count": 48,
            "url": "https://www.kuaishou.com/short-video/kuaishou_mock_video_003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_kuaishou_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "kuaishou_mock_video_001"
    return [
        {
            "mode": "mock",
            "platform": "kuaishou",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "kuaishou_mock_commenter_001",
            "author_name": "mock_kuaishou_user_a",
            "content": "Mock comment: viewers want a clear explanation and a timeline for the next response.",
            "created_at": "2026-05-15T09:02:00Z",
            "like_count": 286,
            "reply_count": 16,
            "url": f"https://www.kuaishou.com/short-video/{target_post_id}#comment001",
        },
        {
            "mode": "mock",
            "platform": "kuaishou",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "kuaishou_mock_commenter_002",
            "author_name": "mock_kuaishou_user_b",
            "content": "Mock comment: similar phrases under multiple videos should be checked for repeated-script signals.",
            "created_at": "2026-05-15T09:09:00Z",
            "like_count": 174,
            "reply_count": 5,
            "url": f"https://www.kuaishou.com/short-video/{target_post_id}#comment002",
        },
        {
            "mode": "mock",
            "platform": "kuaishou",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "kuaishou_mock_commenter_003",
            "author_name": "mock_kuaishou_user_c",
            "content": "Mock comment: a short official clarification would help reduce speculation in the comment area.",
            "created_at": "2026-05-15T09:17:00Z",
            "like_count": 103,
            "reply_count": 2,
            "url": f"https://www.kuaishou.com/short-video/{target_post_id}#comment003",
        },
    ]


def _video_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
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
    return _normalize_adapter_mode(os.getenv("KUAISHOU_ADAPTER_MODE", "mock"))


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
        for credential_name in KUAISHOU_REQUIRED_CREDENTIALS
    }
