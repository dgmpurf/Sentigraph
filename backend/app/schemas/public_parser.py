from pydantic import BaseModel, Field

from app.schemas.comment import RawComment, RawPost


class PublicParserStatusItem(BaseModel):
    platform_id: str
    display_name: str
    source_type: str = "public_page_parser"
    parser_status: str
    live_fetch_enabled: bool = False
    fixture_available: bool = False
    profile_available: bool = True
    comments_supported: bool = False
    last_test_status: str | None = None
    notes: str = ""
    safe_limit: int = 3
    rate_limit_seconds: float = 3.0


class PublicParserStatusResponse(BaseModel):
    parsers: list[PublicParserStatusItem]
    total: int
    live_fetch_enabled_default: bool = False


class PublicParserPreviewRequest(BaseModel):
    platform: str = Field(..., min_length=1, examples=["hupu"])
    limit: int = Field(default=3, ge=1, le=20)
    use_live_fetch: bool = False


class PublicParserPreviewResponse(BaseModel):
    platform: str
    source_type: str = "public_page_parser"
    parser_status: str
    live_fetch_enabled: bool = False
    live_fetch_attempted: bool = False
    fallback_used: bool = True
    fallback_reason_category: str | None = None
    post_count: int = 0
    comment_count: int = 0
    raw_post_schema_valid: bool = True
    raw_comment_schema_valid: bool = True
    sample_posts: list[RawPost] = Field(default_factory=list)
    sample_comments: list[RawComment] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
