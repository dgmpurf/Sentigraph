from pydantic import BaseModel, Field

from app.schemas.common import RiskLevel


TOPIC_RISK_MODEL_VERSION = "v1_5_topic_risk_mvp"


class TopicRiskScore(BaseModel):
    topic_id: str
    cluster_id: str
    topic: str
    comment_count: int
    negative_ratio: float
    average_sentiment_score: float
    neg_severity: float
    spread_signal: float
    controversy_signal: float
    bot_signal: float
    influence_proxy: float
    topic_risk_score: float
    topic_risk_level: RiskLevel
    risk_explanation: str
    # Backward-compatible aliases used by the existing frontend report mapper.
    risk_score: float
    risk_level: RiskLevel


class TopicRiskScoreResult(BaseModel):
    risk_model_version: str = TOPIC_RISK_MODEL_VERSION
    topic_risks: list[TopicRiskScore] = Field(default_factory=list)
    top_risk_topics: list[TopicRiskScore] = Field(default_factory=list)
    max_topic_risk: float = 0.0
    average_topic_risk: float = 0.0
    overall_risk: float = 0.0
    risk_level: RiskLevel = "low"
    real_crisis_risk: float = 0.0
    manipulation_risk: float = 0.0
    risk_explanation: str = "No topic-level risk signal crossed the V1.5 mock threshold."

