from pydantic import BaseModel

from app.schemas.report import PublicOpinionReport, ReportLanguage


class RecommendationRequest(BaseModel):
    project_id: str
    user_type: str = "brand"
    tone: str = "professional"
    report_language: ReportLanguage = "zh-CN"


class RecommendationResponse(PublicOpinionReport):
    # Backward-compatible fields for older frontend code.
    summary: str
    main_risks: list[str]
    suggested_response: str
