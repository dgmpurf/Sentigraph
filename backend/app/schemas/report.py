from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import RISK_MODEL_VERSION, RiskLevel
from app.schemas.risk import TopicRiskScore


ReportLanguage = Literal["zh-CN", "en-US"]


class PublicOpinionReport(BaseModel):
    project_id: str
    report_language: ReportLanguage = "zh-CN"
    risk_score: int
    risk_level: RiskLevel
    risk_level_label: str | None = None
    risk_model_version: str = RISK_MODEL_VERSION
    overall_summary: str
    key_findings: list[str] = Field(default_factory=list)
    main_risk_factors: list[str] = Field(default_factory=list)
    top_negative_topics: list[str] = Field(default_factory=list)
    representative_comments: list[str] = Field(default_factory=list)
    suspected_bot_signals: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    suggested_public_response: str
    generated_from_mock_pipeline: bool = True
    topic_risks: list[TopicRiskScore] = Field(default_factory=list)
    top_risk_topics: list[TopicRiskScore] = Field(default_factory=list)
    max_topic_risk: float | None = None
    average_topic_risk: float | None = None
    overall_risk: float | None = None
    real_crisis_risk: float | None = None
    manipulation_risk: float | None = None
    risk_explanation: str | None = None
    evidence_item_count: int = 0
    evidence_source_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_type_counts: dict[str, int] = Field(default_factory=dict)
