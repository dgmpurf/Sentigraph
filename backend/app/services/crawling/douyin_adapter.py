from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

DOUYIN_REQUIRED_CREDENTIALS = (
    "DOUYIN_CLIENT_KEY",
    "DOUYIN_CLIENT_SECRET",
    "DOUYIN_REDIRECT_URI",
    "DOUYIN_ACCESS_TOKEN",
    "DOUYIN_REFRESH_TOKEN",
)
DOUYIN_API_APPROVAL_STATUS = "developer_access_obtained_permission_unverified"
DOUYIN_DEVELOPER_ACCESS_STATUS = "obtained"
DOUYIN_APP_TYPE = "web_app"
DOUYIN_COMMENT_API_STATUS = "item_comment_scope_not_verified"
DOUYIN_RECOMMENDED_COMMENT_SCOPE = "item.comment"
DOUYIN_VIDEO_COMMENT_SCOPE_STATUS = "not_recommended_for_mvp"
DOUYIN_REAL_MODE_BLOCKER = "oauth_and_scope_not_verified"
DOUYIN_PERMISSION_STATUS = "permission_not_verified"
DOUYIN_OAUTH_STATUS = "scaffold_documented_not_implemented"
DOUYIN_TOKEN_EXCHANGE_STATUS = "placeholder_not_implemented"
DOUYIN_ITEM_ID_SOURCE_STATUS = "not_confirmed"
DOUYIN_OPTIONAL_TOKEN_FIELDS = ("DOUYIN_CLIENT_TOKEN", "DOUYIN_STABLE_CLIENT_TOKEN")
DOUYIN_ENABLE_REAL_CALLS_ENV = "DOUYIN_ENABLE_REAL_CALLS"
DOUYIN_SCOPE_STATUS_ENV = "DOUYIN_SCOPE_STATUS"
DOUYIN_DEFAULT_SCOPE_STATUS = "unverified"
DOUYIN_MOCK_POST_LIMIT = 100
DOUYIN_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class DouyinCredentials:
    client_key: str
    client_secret: str
    redirect_uri: str
    access_token: str
    refresh_token: str

    @classmethod
    def from_env(cls) -> "DouyinCredentials | None":
        client_key = os.getenv("DOUYIN_CLIENT_KEY", "").strip()
        client_secret = os.getenv("DOUYIN_CLIENT_SECRET", "").strip()
        redirect_uri = os.getenv("DOUYIN_REDIRECT_URI", "").strip()
        access_token = os.getenv("DOUYIN_ACCESS_TOKEN", "").strip()
        refresh_token = os.getenv("DOUYIN_REFRESH_TOKEN", "").strip()
        if not client_key or not client_secret or not redirect_uri or not access_token or not refresh_token:
            return None
        return cls(
            client_key=client_key,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            access_token=access_token,
            refresh_token=refresh_token,
        )


class DouyinAdapter(BasePlatformAdapter):
    platform_id = "douyin"
    display_name = "Douyin"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: DouyinCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or DouyinCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = DOUYIN_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_douyin_oauth_configuration"
        elif self.requested_mode == "real" and (
            not _real_calls_enabled() or _scope_status() != "verified"
        ):
            self.fallback_reason = "api_pending:permission_not_verified"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:implementation_not_enabled"

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
        return DOUYIN_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = (
                    "Douyin Web App real mode is scaffolded but disabled until OAuth callback, "
                    "token exchange, item.comment scope, authorized test account, and item_id "
                    "source are verified."
                )
            else:
                message = "Douyin Web App real mode was requested, but OAuth configuration is incomplete; using mock data."
        else:
            message = "Douyin adapter mock mode is active."

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
            "developer_access_status": DOUYIN_DEVELOPER_ACCESS_STATUS,
            "app_type": DOUYIN_APP_TYPE,
            "comment_api_status": DOUYIN_COMMENT_API_STATUS,
            "recommended_comment_scope": DOUYIN_RECOMMENDED_COMMENT_SCOPE,
            "video_comment_scope_status": DOUYIN_VIDEO_COMMENT_SCOPE_STATUS,
            "real_mode_blocker": DOUYIN_REAL_MODE_BLOCKER,
            "permission_status": DOUYIN_PERMISSION_STATUS,
            "oauth_status": DOUYIN_OAUTH_STATUS,
            "token_exchange_status": DOUYIN_TOKEN_EXCHANGE_STATUS,
            "item_id_source_status": DOUYIN_ITEM_ID_SOURCE_STATUS,
            "scope_status": _scope_status(),
            "real_calls_enabled": _real_calls_enabled(),
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
            "optional_credentials_present": _optional_token_presence(),
        }

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        safe_limit = self.clamp_limit(limit, default=20, maximum=DOUYIN_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_douyin_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=DOUYIN_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_douyin_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _video_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        statistics = payload.get("statistics") if isinstance(payload.get("statistics"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("aweme_id") or payload.get("video_id") or payload.get("item_id") or payload.get("id"),
            default="douyin_unknown_video",
        )
        author_name = self.safe_text(
            payload.get("creator_name") or author.get("nickname") or payload.get("source"),
            default="mock_douyin_creator",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("creator_id") or author.get("uid") or author.get("open_id"), default=author_name),
            author_name=author_name,
            title=self.safe_text(payload.get("title") or payload.get("topic_summary"), default="Douyin short-video discussion"),
            content=self.safe_text(payload.get("description") or payload.get("desc") or payload.get("content"), default="Mock Douyin video description."),
            like_count=max(0, self.coerce_int(payload.get("like_count") or statistics.get("digg_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or statistics.get("comment_count"))),
            share_count=max(0, self.coerce_int(payload.get("share_count") or statistics.get("share_count"))),
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("create_time")),
            url=self.safe_text(payload.get("url") or payload.get("share_url"), default=f"https://www.douyin.com/video/{post_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        user = payload.get("user") if isinstance(payload.get("user"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("aweme_id") or payload.get("video_id"),
            default="douyin_unknown_video",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("cid") or payload.get("id"),
            default="douyin_unknown_comment",
        )
        author_name = self.safe_text(
            payload.get("author_name") or user.get("nickname") or payload.get("source"),
            default="mock_douyin_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("reply_id")) or None,
            author_id=self.safe_text(payload.get("author_id") or user.get("uid") or user.get("open_id"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("content") or payload.get("text")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("digg_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("reply_comment_total"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.douyin.com/video/{post_id}#comment-{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_douyin_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "douyin",
            "aweme_id": "douyin_mock_video_001",
            "title": f"{topic} short-video reaction roundup",
            "description": "Mock short-video discussion collecting reactions about service timing, product quality, and response clarity.",
            "creator_id": "douyin_mock_creator_001",
            "creator_name": "Mock Douyin Observer",
            "created_at": "2026-05-15T08:45:00Z",
            "like_count": 3860,
            "reply_count": 228,
            "share_count": 146,
            "url": "https://www.douyin.com/video/douyin_mock_video_001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "douyin",
            "aweme_id": "douyin_mock_video_002",
            "title": f"{topic} creator commentary",
            "description": "Mock Douyin creator commentary about repeated complaints and whether the brand response is convincing.",
            "creator_id": "douyin_mock_creator_002",
            "creator_name": "Mock Short Video Lab",
            "created_at": "2026-05-15T09:25:00Z",
            "like_count": 2140,
            "reply_count": 151,
            "share_count": 92,
            "url": "https://www.douyin.com/video/douyin_mock_video_002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "douyin",
            "aweme_id": "douyin_mock_video_003",
            "title": f"{topic} public response explainer",
            "description": "Mock short-video explainer discussing public response wording, rumor control, and follow-up actions.",
            "creator_id": "douyin_mock_creator_003",
            "creator_name": "Mock Crisis Notes",
            "created_at": "2026-05-15T10:05:00Z",
            "like_count": 1420,
            "reply_count": 96,
            "share_count": 63,
            "url": "https://www.douyin.com/video/douyin_mock_video_003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_douyin_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "douyin_mock_video_001"
    return [
        {
            "mode": "mock",
            "platform": "douyin",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "douyin_mock_commenter_001",
            "author_name": "mock_douyin_user_a",
            "content": "Mock comment: the video makes the issue easier to understand, but users still want a concrete timeline.",
            "created_at": "2026-05-15T08:52:00Z",
            "like_count": 338,
            "reply_count": 21,
            "url": f"https://www.douyin.com/video/{target_post_id}#comment001",
        },
        {
            "mode": "mock",
            "platform": "douyin",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "douyin_mock_commenter_002",
            "author_name": "mock_douyin_user_b",
            "content": "Mock comment: similar scripts are appearing under several clips, so repeated-comment signals should be reviewed.",
            "created_at": "2026-05-15T08:58:00Z",
            "like_count": 214,
            "reply_count": 8,
            "url": f"https://www.douyin.com/video/{target_post_id}#comment002",
        },
        {
            "mode": "mock",
            "platform": "douyin",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "douyin_mock_commenter_003",
            "author_name": "mock_douyin_user_c",
            "content": "Mock comment: pinning a clear response would help slow down speculation in the comment area.",
            "created_at": "2026-05-15T09:06:00Z",
            "like_count": 126,
            "reply_count": 4,
            "url": f"https://www.douyin.com/video/{target_post_id}#comment003",
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
    return _normalize_adapter_mode(os.getenv("DOUYIN_ADAPTER_MODE", "mock"))


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
        return DOUYIN_PERMISSION_STATUS
    return "mock_only"


def _credential_presence() -> dict[str, bool]:
    load_project_env()
    return {
        credential_name: bool(os.getenv(credential_name, "").strip())
        for credential_name in DOUYIN_REQUIRED_CREDENTIALS
    }


def _optional_token_presence() -> dict[str, bool]:
    load_project_env()
    return {
        credential_name: bool(os.getenv(credential_name, "").strip())
        for credential_name in DOUYIN_OPTIONAL_TOKEN_FIELDS
    }


def _scope_status() -> str:
    load_project_env()
    status = os.getenv(DOUYIN_SCOPE_STATUS_ENV, DOUYIN_DEFAULT_SCOPE_STATUS).strip().lower()
    return status or DOUYIN_DEFAULT_SCOPE_STATUS


def _real_calls_enabled() -> bool:
    load_project_env()
    return os.getenv(DOUYIN_ENABLE_REAL_CALLS_ENV, "false").strip().lower() == "true"
