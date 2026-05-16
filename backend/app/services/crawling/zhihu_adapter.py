from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from app.core.environment import load_project_env
from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, AdapterMode, BasePlatformAdapter


load_project_env()

ZHIHU_REQUIRED_CREDENTIALS = (
    "ZHIHU_CLIENT_ID",
    "ZHIHU_CLIENT_SECRET",
    "ZHIHU_ACCESS_TOKEN",
)
ZHIHU_API_APPROVAL_STATUS = "planned"
ZHIHU_MOCK_POST_LIMIT = 100
ZHIHU_MOCK_COMMENT_LIMIT = 500


@dataclass(frozen=True)
class ZhihuCredentials:
    client_id: str
    client_secret: str
    access_token: str

    @classmethod
    def from_env(cls) -> "ZhihuCredentials | None":
        client_id = os.getenv("ZHIHU_CLIENT_ID", "").strip()
        client_secret = os.getenv("ZHIHU_CLIENT_SECRET", "").strip()
        access_token = os.getenv("ZHIHU_ACCESS_TOKEN", "").strip()
        if not client_id or not client_secret or not access_token:
            return None
        return cls(client_id=client_id, client_secret=client_secret, access_token=access_token)


class ZhihuAdapter(BasePlatformAdapter):
    platform_id = "zhihu"
    display_name = "Zhihu"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: ZhihuCredentials | None = None,
    ) -> None:
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or ZhihuCredentials.from_env()
        self.fallback_reason = ""
        self.mock_available = True
        self.api_pending = True
        self.real_mode_disabled = True
        self.api_approval_required = True
        self.api_approval_status = ZHIHU_API_APPROVAL_STATUS
        self.selectable_for_real = False

        if self.requested_mode == "real" and not self.credentials:
            self.fallback_reason = "config_error:missing_zhihu_credentials"
        elif self.requested_mode == "real":
            self.fallback_reason = "api_pending:zhihu_official_api_not_implemented"

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
        return ZHIHU_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.requested_mode == "real":
            if self.has_required_credentials():
                message = "Zhihu official API mode is planned but disabled until approval and implementation are added."
            else:
                message = "Zhihu official API mode was requested, but credentials are missing; using mock data."
        else:
            message = "Zhihu adapter mock mode is active."

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
        safe_limit = self.clamp_limit(limit, default=20, maximum=ZHIHU_MOCK_POST_LIMIT)
        return [
            self.normalize_post(raw)
            for raw in _mock_zhihu_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
        ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        safe_limit = self.clamp_limit(limit, default=100, maximum=ZHIHU_MOCK_COMMENT_LIMIT)
        return [self.normalize_comment(raw) for raw in _mock_zhihu_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _post_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        question = payload.get("question") if isinstance(payload.get("question"), Mapping) else {}
        statistics = payload.get("statistics") if isinstance(payload.get("statistics"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("answer_id")
            or payload.get("article_id")
            or payload.get("question_id")
            or payload.get("post_id")
            or payload.get("id"),
            default="zhihu_unknown_post",
        )
        author_name = self.safe_text(
            payload.get("author_name") or author.get("name") or author.get("headline") or payload.get("source"),
            default="mock_zhihu_author",
        )

        return RawPost(
            platform=self.platform_id,
            post_id=post_id,
            author_id=self.safe_text(payload.get("author_id") or author.get("id") or author.get("url_token"), default=author_name),
            author_name=author_name,
            title=self.safe_text(
                payload.get("title")
                or payload.get("question_title")
                or question.get("title")
                or payload.get("article_title"),
                default="Zhihu public Q&A discussion",
            ),
            content=self.safe_text(
                payload.get("content")
                or payload.get("answer_text")
                or payload.get("excerpt")
                or payload.get("description"),
                default="Mock Zhihu answer or article content.",
            ),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("voteup_count") or statistics.get("like_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("comment_count") or statistics.get("comment_count"))),
            share_count=max(0, self.coerce_int(payload.get("share_count") or statistics.get("share_count"))),
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("created_time") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.zhihu.com/question/{post_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        author = payload.get("author") if isinstance(payload.get("author"), Mapping) else {}
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("answer_id") or payload.get("article_id") or payload.get("question_id"),
            default="zhihu_unknown_post",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("id") or payload.get("cid"),
            default="zhihu_unknown_comment",
        )
        author_name = self.safe_text(
            payload.get("author_name") or author.get("name") or author.get("headline") or payload.get("source"),
            default="mock_zhihu_commenter",
        )

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=self.safe_text(payload.get("parent_id") or payload.get("reply_to_comment_id")) or None,
            author_id=self.safe_text(payload.get("author_id") or author.get("id") or author.get("url_token"), default=author_name),
            author_name=author_name,
            content=self.safe_text(payload.get("content") or payload.get("text")),
            like_count=max(0, self.coerce_int(payload.get("like_count") or payload.get("vote_count"))),
            reply_count=max(0, self.coerce_int(payload.get("reply_count") or payload.get("child_comment_count"))),
            share_count=0,
            created_at=self.to_utc_iso(payload.get("created_at") or payload.get("created_time") or payload.get("create_time")),
            url=self.safe_text(payload.get("url"), default=f"https://www.zhihu.com/question/{post_id}#comment-{comment_id}"),
            raw_data=self.sanitize_raw_data(payload),
        )


def _mock_zhihu_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "platform": "zhihu",
            "question_id": "zhihu_mock_question_001",
            "answer_id": "zhihu_mock_answer_001",
            "title": f"{topic} public Q&A discussion",
            "content": "Mock Zhihu answer discussing public trust, service response timing, and evidence users expect to see.",
            "author_id": "zhihu_mock_author_001",
            "author_name": "Mock Zhihu Analyst",
            "created_at": "2026-05-15T08:35:00Z",
            "like_count": 1860,
            "reply_count": 124,
            "share_count": 39,
            "url": "https://www.zhihu.com/question/zhihu_mock_question_001/answer/zhihu_mock_answer_001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "zhihu",
            "article_id": "zhihu_mock_article_002",
            "title": f"{topic} article-style risk explainer",
            "content": "Mock Zhihu article explaining repeated complaint themes, likely stakeholder concerns, and response options.",
            "author_id": "zhihu_mock_author_002",
            "author_name": "Mock Public Opinion Notes",
            "created_at": "2026-05-15T09:20:00Z",
            "like_count": 1320,
            "reply_count": 76,
            "share_count": 28,
            "url": "https://zhuanlan.zhihu.com/p/zhihu_mock_article_002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "platform": "zhihu",
            "question_id": "zhihu_mock_question_003",
            "answer_id": "zhihu_mock_answer_003",
            "title": f"{topic} consumer experience comparison",
            "content": "Mock Zhihu answer comparing user experiences and identifying which claims need factual clarification.",
            "author_id": "zhihu_mock_author_003",
            "author_name": "Mock Consumer Researcher",
            "created_at": "2026-05-15T10:10:00Z",
            "like_count": 940,
            "reply_count": 51,
            "share_count": 17,
            "url": "https://www.zhihu.com/question/zhihu_mock_question_003/answer/zhihu_mock_answer_003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_zhihu_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "zhihu_mock_answer_001"
    return [
        {
            "mode": "mock",
            "platform": "zhihu",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "zhihu_mock_commenter_001",
            "author_name": "mock_zhihu_user_a",
            "content": "Mock comment: the answer is useful, but users still want official details and a timeline.",
            "created_at": "2026-05-15T08:48:00Z",
            "like_count": 176,
            "reply_count": 9,
            "url": f"https://www.zhihu.com/question/{target_post_id}#comment001",
        },
        {
            "mode": "mock",
            "platform": "zhihu",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "zhihu_mock_commenter_002",
            "author_name": "mock_zhihu_user_b",
            "content": "Mock comment: repeated wording across answers should be checked before judging the trend.",
            "created_at": "2026-05-15T08:56:00Z",
            "like_count": 118,
            "reply_count": 4,
            "url": f"https://www.zhihu.com/question/{target_post_id}#comment002",
        },
        {
            "mode": "mock",
            "platform": "zhihu",
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "zhihu_mock_commenter_003",
            "author_name": "mock_zhihu_user_c",
            "content": "Mock comment: a concise evidence-based clarification would reduce speculation in the discussion.",
            "created_at": "2026-05-15T09:07:00Z",
            "like_count": 74,
            "reply_count": 2,
            "url": f"https://www.zhihu.com/question/{target_post_id}#comment003",
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
    return _normalize_adapter_mode(os.getenv("ZHIHU_ADAPTER_MODE", "mock"))


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
        for credential_name in ZHIHU_REQUIRED_CREDENTIALS
    }
