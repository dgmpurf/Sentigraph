from pydantic import BaseModel

from app.schemas.report import PublicOpinionReport, ReportLanguage


class SummaryGenerateRequest(BaseModel):
    project_id: str
    include_representative_comments: bool = True
    report_language: ReportLanguage = "zh-CN"


class SummaryGenerateResponse(PublicOpinionReport):
    # Backward-compatible alias for older frontend code.
    summary: str
