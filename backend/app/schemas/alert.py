from datetime import datetime
from typing import Any, Literal

from app.schemas.common import RiskLevel
from app.schemas.risk import TopicRiskScore
from pydantic import BaseModel, Field


AlertLevel = Literal["info", "warning", "critical"]


class AlertItem(BaseModel):
    alert_id: str
    level: RiskLevel
    message: str
    created_at: str
    resolved: bool


class AlertsResponse(BaseModel):
    project_id: str
    alerts: list[AlertItem]


class AlertThresholdConfig(BaseModel):
    risk_score_delta_warning: float = 10
    risk_score_delta_critical: float = 20
    real_crisis_delta_warning: float = 10
    manipulation_delta_warning: float = 15
    topic_risk_high: float = 70
    topic_risk_critical: float = 85


class AnalysisSnapshot(BaseModel):
    snapshot_id: str
    case_id: str
    created_at: datetime
    run_index: int
    risk_score: float
    overall_risk: float
    risk_level: RiskLevel
    risk_model_version: str
    real_crisis_risk: float = 0.0
    manipulation_risk: float = 0.0
    top_risk_topics: list[TopicRiskScore] = Field(default_factory=list)
    summary: str | None = None


class AlertEvent(BaseModel):
    alert_id: str
    case_id: str
    snapshot_id: str
    level: AlertLevel
    alert_type: str
    message: str
    reason: str
    created_at: datetime
    resolved: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class MonitoringStatus(BaseModel):
    case_id: str
    status: Literal["baseline_created", "alerts_detected", "stable"]
    latest_snapshot: AnalysisSnapshot
    previous_snapshot: AnalysisSnapshot | None = None
    alerts: list[AlertEvent] = Field(default_factory=list)
    snapshot_count: int
    latest_risk_delta: float = 0.0
    latest_risk_level: RiskLevel
    message: str
