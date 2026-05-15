from pydantic import BaseModel, Field

from app.schemas.comment import RawComment, RawPost
from app.schemas.common import DateRange, TaskStatus


class CrawlStartRequest(BaseModel):
    keyword: str = Field(..., min_length=1, examples=["Tesla"])
    platforms: list[str] = Field(default_factory=list, examples=[["reddit", "weibo"]])
    limit: int = Field(default=100, ge=1, le=1000)
    date_range: DateRange | None = None


class PlatformCrawlMetadata(BaseModel):
    platform: str
    adapter_mode: str
    source_type: str | None = None
    parser_status: str | None = None
    live_fetch_enabled: bool = False
    live_fetch_attempted: bool = False
    live_fetch_allowed: bool = False
    fallback_used: bool = False
    fallback_reason_category: str | None = None
    fetch_status: str | None = None
    mock_available: bool = True
    real_mode_available: bool = False
    api_approval_required: bool = False
    api_approval_status: str | None = None
    api_pending: bool = False
    real_mode_disabled: bool = False
    selectable_for_real: bool = False
    real_mode_blocked_reason: str | None = None
    real_mode_reached: bool = False
    dependency_available: bool = True
    exception_class: str | None = None
    sanitized_error_category: str | None = None
    post_count: int = 0
    comment_count: int = 0
    schema_valid: bool = True
    raw_post_schema_valid: bool = True
    raw_comment_schema_valid: bool = True


class CrawlStartResponse(BaseModel):
    project_id: str
    crawl_task_id: str
    status: TaskStatus
    message: str
    platform_metadata: list[PlatformCrawlMetadata] = Field(default_factory=list)
    raw_posts: list[RawPost] = Field(default_factory=list)
    raw_comments: list[RawComment] = Field(default_factory=list)
