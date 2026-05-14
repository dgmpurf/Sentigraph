from pydantic import BaseModel, Field

from app.schemas.common import DateRange, TaskStatus


class CrawlStartRequest(BaseModel):
    keyword: str = Field(..., min_length=1, examples=["Tesla"])
    platforms: list[str] = Field(default_factory=list, examples=[["reddit", "weibo"]])
    limit: int = Field(default=100, ge=1, le=1000)
    date_range: DateRange | None = None


class CrawlStartResponse(BaseModel):
    project_id: str
    crawl_task_id: str
    status: TaskStatus
    message: str
