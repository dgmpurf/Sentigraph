from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.comment import RawComment, RawPost
from app.schemas.common import DateRange, RiskLevel
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.evidence import EvidenceItem
from app.schemas.report import PublicOpinionReport, ReportLanguage
from app.schemas.scheduler import MonitoringScheduleConfig
from app.schemas.visualization import VisualizationResponse


AnalysisCaseStatus = Literal["draft", "running", "completed", "failed"]
RawDataStatus = Literal["missing", "attached", "empty"]


class AnalysisCaseCreateRequest(BaseModel):
    keyword: str = Field(..., min_length=1)
    platforms: list[str] = Field(default_factory=list)
    title: str | None = None
    report_language: ReportLanguage = "zh-CN"


class CaseCrawlStartRequest(BaseModel):
    keyword: str | None = Field(default=None, min_length=1)
    platforms: list[str] | None = None
    limit: int = Field(default=100, ge=1, le=1000)
    date_range: DateRange | None = None


class AnalysisCase(BaseModel):
    case_id: str
    project_id: str
    title: str
    keyword: str
    platforms: list[str] = Field(default_factory=list)
    status: AnalysisCaseStatus
    created_at: datetime
    updated_at: datetime
    risk_score: float | None = None
    risk_level: RiskLevel | None = None
    risk_model_version: str | None = None
    report_language: ReportLanguage = "zh-CN"
    monitoring_config: MonitoringScheduleConfig = Field(default_factory=MonitoringScheduleConfig)


class AnalysisCaseListItem(AnalysisCase):
    pass


class AnalysisCaseDetail(AnalysisCase):
    analysis_result: AnalysisResultResponse | None = None
    visualization_data: VisualizationResponse | None = None
    report: PublicOpinionReport | None = None
    markdown_available: bool = False
    raw_posts: list[RawPost] = Field(default_factory=list)
    raw_comments: list[RawComment] = Field(default_factory=list)
    evidence_items: list[EvidenceItem] = Field(default_factory=list)
    crawl_metadata: list[PlatformCrawlMetadata] = Field(default_factory=list)
    crawl_source_mode: str | None = None
    crawl_attached_at: datetime | None = None
    raw_data_status: RawDataStatus = "missing"
    analysis_input_source: Literal["case_evidence_items", "case_raw_data", "mock_data_fallback"] | None = None
    raw_post_count: int = 0
    raw_comment_count: int = 0
    evidence_item_count: int = 0


class MarkdownExportResponse(BaseModel):
    case_id: str
    project_id: str
    filename: str
    markdown: str
    generated_at: datetime
