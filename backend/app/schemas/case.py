from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.common import RiskLevel
from app.schemas.report import PublicOpinionReport, ReportLanguage
from app.schemas.scheduler import MonitoringScheduleConfig
from app.schemas.visualization import VisualizationResponse


AnalysisCaseStatus = Literal["draft", "running", "completed", "failed"]


class AnalysisCaseCreateRequest(BaseModel):
    keyword: str = Field(..., min_length=1)
    platforms: list[str] = Field(default_factory=list)
    title: str | None = None
    report_language: ReportLanguage = "zh-CN"


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


class MarkdownExportResponse(BaseModel):
    case_id: str
    project_id: str
    filename: str
    markdown: str
    generated_at: datetime
