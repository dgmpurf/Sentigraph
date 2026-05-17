from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import RiskLevel
from app.schemas.risk import TopicRiskScore


ForecastHorizon = Literal["next_check", "1h", "6h", "24h"]
ForecastConfidence = Literal["insufficient_history", "low", "medium_low", "medium"]
TrendDirection = Literal["rising", "falling", "stable", "unknown"]
ForecastStatus = Literal["ready", "insufficient_history"]


class ForecastInputSnapshot(BaseModel):
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


class TrendFeatures(BaseModel):
    latest_risk: float = 0.0
    moving_average: float = 0.0
    slope: float = 0.0
    acceleration: float = 0.0
    volatility: float = 0.0
    snapshot_count: int = 0
    trend_direction: TrendDirection = "unknown"


class RiskForecast(BaseModel):
    horizon: ForecastHorizon
    predicted_risk_score: float
    predicted_risk_level: RiskLevel
    predicted_real_crisis_risk: float
    predicted_manipulation_risk: float
    trend_direction: TrendDirection
    real_crisis_trend_direction: TrendDirection
    manipulation_trend_direction: TrendDirection
    forecast_confidence: ForecastConfidence
    forecast_reason: str


class TopicRiskForecast(BaseModel):
    topic_id: str
    topic: str
    current_topic_risk_score: float
    predicted_topic_risk_score: float
    predicted_topic_risk_level: RiskLevel
    trend_direction: TrendDirection
    risk_explanation: str
    forecast_reason: str


class ForecastResult(BaseModel):
    case_id: str
    forecast_status: ForecastStatus
    generated_at: datetime | None = None
    risk_model_version: str | None = None
    snapshot_count: int = 0
    latest_snapshot_id: str | None = None
    horizon: ForecastHorizon = "next_check"
    latest_risk: float = 0.0
    moving_average: float = 0.0
    slope: float = 0.0
    acceleration: float = 0.0
    volatility: float = 0.0
    trend_direction: TrendDirection = "unknown"
    forecast_confidence: ForecastConfidence = "insufficient_history"
    predicted_risk_score: float = 0.0
    predicted_risk_level: RiskLevel = "low"
    predicted_real_crisis_risk: float = 0.0
    predicted_manipulation_risk: float = 0.0
    real_crisis_trend_direction: TrendDirection = "unknown"
    manipulation_trend_direction: TrendDirection = "unknown"
    risk_forecasts: list[RiskForecast] = Field(default_factory=list)
    topic_forecasts: list[TopicRiskForecast] = Field(default_factory=list)
    input_snapshots: list[ForecastInputSnapshot] = Field(default_factory=list)
    recommended_action: str
    message: str
