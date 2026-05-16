from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

BILIBILI_REQUIRED_CREDENTIALS = (
    "BILIBILI_CLIENT_ID",
    "BILIBILI_CLIENT_SECRET",
    "BILIBILI_ACCESS_TOKEN",
)
BILIBILI_API_APPROVAL_STATUS = "planned"
BILIBILI_MOCK_POST_LIMIT = 100
BILIBILI_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class BilibiliCredentials:
    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_env(cls) -> "BilibiliCredentials | None":
        client_id = os.getenv("BILIBILI_CLIENT_ID", "").strip()
        client_secret = os.getenv("BILIBILI_CLIENT_SECRET", "").strip()
        access_token = os.getenv("BILIBILI_ACCESS_TOKEN", "").strip()
        if not client_id or not client_secret or not access_token:
            return None
        return cls(client_id=client_id, client_secret=client_secret, access_token=access_token)


class BilibiliAdapter(BasePlatformAdapter):
    platform_id = "bilibili"
    display_name = "Bilibili"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: BilibiliCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or BilibiliCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = BILIBILI_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_bilibili_credentials"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:bilibili_official_api_not_implemented"

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
        return BILIBILI_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = "Bilibili official API mode is planned but disabled until approval and implementation are added."
            else:
                message = "Bilibili official API mode was requested, but credentials are missing; using mock data."
        else:
            message = "Bilibili adapter mock mode is active."

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
        safe_limit = self.clamp_limit(limit, default=20, maximum=BILIBILI_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_bilibili_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=BILIBILI_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_bilibili_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _video_payload(raw)
        owner = payload.get("owner") if isinstance(payload.get("owner"), Mapping) else {}
        stat = payload.get("stat") if isinstance(payload.get("stat"), Mapping) else {}
        post_id = self.safe_text(payload.get("bvid") or payload.get("video_id") or payload.get("id"), default="bilibili_unknown_video")
        author_name = self.safe_text(
            payload.get("uploader_name") or owner.get("name") or payload.get("source"),
            default="mock_bilibili_uploader",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("uploader_id") or owner.get("mid"), default=author_name),
            author_name=author_name,
            title=self.safe_text(payload.get("title"), default="Untitled Bilibili video"),
            content=self.safe_text(payload.get("description") or payload.get("content"), default="Mock Bilibili video description."),
            like_count=max(0, self.coerce_int(payload.get("like_count") or stat.get("like"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or stat.get("reply"))),
            share_count=max(0, self.coerce_int(payload.get("share_count") or stat.get("share"))),
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("pubdate")),
            url=self.safe_text(payload.get("url"), default=f"https://www.bilibili.com/video/{post_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        member = payload.get("member") if isinstance(payload.get("member"), Mapping) else {}
        post_id = self.safe_text(payload.get("post_id") or payload.get("oid") or payload.get("bvid"), default="bilibili_unknown_video")
        comment_id = self.safe_text(payload.get("comment_id") or payload.get("rpid") or payload.get("id"), default="bilibili_unknown_comment")
        author_name = self.safe_text(
            payload.get("author_name") or member.get("uname") or payload.get("source"),
            default="mock_bilibili_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("parent")) or None,
            author_id=self.safe_text(payload.get("author_id") or member.get("mid"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("content") or payload.get("message")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("like"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("reply"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("ctime")),
            url=self.safe_text(payload.get("url"), default=f"https://www.bilibili.com/video/{post_id}#reply{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_bilibili_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "bilibili",
            "bvid": "BV1sentigraph001",
            "title": f"{topic} product review discussion",
            "description": "Mock public video discussion about product quality, customer support, and brand trust.",
            "uploader_id": "bilibili_mock_up_001",
            "uploader_name": "Mock Tech Observer",
            "created_at": "2026-05-15T08:00:00Z",
            "like_count": 1320,
            "reply_count": 86,
            "share_count": 45,
            "url": "https://www.bilibili.com/video/BV1sentigraph001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "bilibili",
            "bvid": "BV1sentigraph002",
            "title": f"{topic} service experience compilation",
            "description": "Mock Bilibili video collecting public service experience reactions and repeated concerns.",
            "uploader_id": "bilibili_mock_up_002",
            "uploader_name": "Mock Consumer Notes",
            "created_at": "2026-05-15T09:30:00Z",
            "like_count": 870,
            "reply_count": 64,
            "share_count": 31,
            "url": "https://www.bilibili.com/video/BV1sentigraph002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "bilibili",
            "bvid": "BV1sentigraph003",
            "title": f"{topic} official response analysis",
            "description": "Mock explainer video discussing public response timing and communication risk.",
            "uploader_id": "bilibili_mock_up_003",
            "uploader_name": "Mock Media Lab",
            "created_at": "2026-05-15T10:15:00Z",
            "like_count": 540,
            "reply_count": 38,
            "share_count": 22,
            "url": "https://www.bilibili.com/video/BV1sentigraph003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_bilibili_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "BV1sentigraph001"
    return [
        {
            "mode": "mock",
            "platform": "bilibili",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_reply_001",
            "author_id": "bilibili_mock_commenter_001",
            "author_name": "mock_bilibili_user_a",
            "content": "Mock comment: the explanation is useful, but many viewers still want clearer follow-up actions.",
            "created_at": "2026-05-15T08:10:00Z",
            "like_count": 128,
            "reply_count": 6,
            "url": f"https://www.bilibili.com/video/{target_post_id}#reply001",
        },
        {
            "mode": "mock",
            "platform": "bilibili",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_reply_002",
            "parent_id": f"{target_post_id}_reply_001",
            "author_id": "bilibili_mock_commenter_002",
            "author_name": "mock_bilibili_user_b",
            "content": "Mock comment: similar complaints are appearing across several videos, so the topic may keep spreading.",
            "created_at": "2026-05-15T08:15:00Z",
            "like_count": 92,
            "reply_count": 3,
            "url": f"https://www.bilibili.com/video/{target_post_id}#reply002",
        },
        {
            "mode": "mock",
            "platform": "bilibili",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_reply_003",
            "author_id": "bilibili_mock_commenter_003",
            "author_name": "mock_bilibili_user_c",
            "content": "Mock comment: a concise public response would help reduce repeated speculation.",
            "created_at": "2026-05-15T08:22:00Z",
            "like_count": 57,
            "reply_count": 1,
            "url": f"https://www.bilibili.com/video/{target_post_id}#reply003",
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
    return _normalize_adapter_mode(os.getenv("BILIBILI_ADAPTER_MODE", "mock"))


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
        for credential_name in BILIBILI_REQUIRED_CREDENTIALS
    }
