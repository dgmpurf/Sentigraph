from __future__ import annotations

from typing import Any, ClassVar, Mapping

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import AdapterHealth, BasePlatformAdapter
from app.services.crawling.public_parser.base_public_parser import BasePublicParser, PublicParserResult
from app.services.crawling.public_parser.selector_profile import load_selector_profile


class PublicParserPlatformAdapter(BasePlatformAdapter):
    platform_id: ClassVar[str]
    display_name: ClassVar[str]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(mode="mock")
        self.profile = load_selector_profile(self.platform_id)
        self.parser = BasePublicParser(self.profile)
        self.last_result = PublicParserResult(metadata=self.parser._metadata(
            fallback_used=True,
            fallback_reason_category="not_started",
            post_count=0,
            comment_count=0,
            schema_valid=True,
        ))
        self.fallback_reason: str | None = None
        del kwargs

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        del sort, date_range
        self.last_result = self.parser.search_public_pages(keyword, limit=limit)
        self.fallback_reason = self.last_result.metadata.get("fallback_reason_category")
        return self.last_result.posts

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        del post_id, limit
        return self.last_result.comments

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        if isinstance(raw, RawPost):
            return raw
        return RawPost(
            platform=self.platform_id,
            post_id=self.safe_text(raw.get("post_id"), f"{self.platform_id}_public_post"),
            author_id=self.safe_text(raw.get("author_id"), f"{self.platform_id}_public_author"),
            author_name=self.safe_text(raw.get("author_name"), self.display_name),
            title=self.safe_text(raw.get("title"), "Public article"),
            content=self.safe_text(raw.get("content"), "Public article content."),
            like_count=self.coerce_int(raw.get("like_count")),
            reply_count=self.coerce_int(raw.get("reply_count")),
            share_count=self.coerce_int(raw.get("share_count")),
            created_at=self.to_utc_iso(raw.get("created_at")),
            url=self.safe_text(raw.get("url"), self.profile.base_url),
            raw_data=self.sanitize_raw_data(raw),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        if isinstance(raw, RawComment):
            return raw
        return RawComment(
            platform=self.platform_id,
            post_id=self.safe_text(raw.get("post_id"), f"{self.platform_id}_public_post"),
            comment_id=self.safe_text(raw.get("comment_id"), f"{self.platform_id}_public_comment"),
            parent_id=self.safe_text(raw.get("parent_id")) or None,
            author_id=self.safe_text(raw.get("author_id"), f"{self.platform_id}_public_commenter"),
            author_name=self.safe_text(raw.get("author_name"), "public_commenter"),
            content=self.safe_text(raw.get("content"), "Public comment content."),
            like_count=self.coerce_int(raw.get("like_count")),
            reply_count=self.coerce_int(raw.get("reply_count")),
            share_count=self.coerce_int(raw.get("share_count")),
            created_at=self.to_utc_iso(raw.get("created_at")),
            url=self.safe_text(raw.get("url"), self.profile.base_url),
            raw_data=self.sanitize_raw_data(raw),
        )

    def health_check(self) -> AdapterHealth:
        return AdapterHealth(
            platform_id=self.platform_id,
            mode="mock",
            ok=True,
            real_mode_available=False,
            message=(
                f"{self.display_name} public parser scaffold is fixture-only by default; "
                "live public fetching is disabled unless explicitly configured."
            ),
            fallback_reason="fixture_only",
        )

    def supports_real_mode(self) -> bool:
        return False

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return ()

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        metadata = dict(self.last_result.metadata)
        metadata.update(
            {
                "mock_available": True,
                "real_mode_available": False,
                "api_approval_required": False,
                "api_approval_status": "not_applicable",
                "api_pending": False,
                "real_mode_disabled": True,
                "selectable_for_real": False,
                "real_mode_reached": False,
                "dependency_available": True,
                "exception_class": None,
                "sanitized_error_category": metadata.get("fallback_reason_category"),
            }
        )
        return metadata


class ThePaperPublicParserAdapter(PublicParserPlatformAdapter):
    platform_id = "the_paper"
    display_name = "The Paper / Pengpai News"


class HupuPublicParserAdapter(PublicParserPlatformAdapter):
    platform_id = "hupu"
    display_name = "Hupu / HuPu"


class JiemianPublicParserAdapter(PublicParserPlatformAdapter):
    platform_id = "jiemian"
    display_name = "Jiemian News / 界面新闻"
