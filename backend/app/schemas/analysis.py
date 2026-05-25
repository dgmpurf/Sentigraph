from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.common import RISK_MODEL_VERSION, RiskLevel, TaskStatus
from app.schemas.risk import TopicRiskScore


AnalysisType = Literal["sentiment", "topic", "bot", "ai_generated", "propagation", "risk"]
SentimentLabel = Literal["positive", "negative", "neutral", "mixed"]


class AnalysisRunRequest(BaseModel):
    project_id: str
    analysis_types: list[AnalysisType] = Field(default_factory=list)


class AnalysisRunResponse(BaseModel):
    project_id: str
    analysis_task_id: str
    status: TaskStatus
    message: str


class SentimentSummary(BaseModel):
    positive_ratio: float
    neutral_ratio: float
    negative_ratio: float
    average_sentiment_score: float


class SentimentResult(BaseModel):
    comment_id: str
    sentiment: SentimentLabel
    sentiment_score: float
    emotion_tags: list[str]
    stance: str
    confidence: float
    reason: str


class TopicCluster(BaseModel):
    cluster_id: str
    topic: str
    summary: str
    comment_count: int
    average_sentiment_score: float
    representative_comments: list[str]


class ConflictResult(BaseModel):
    conflict_id: str
    side_a: str
    side_b: str
    intensity: float
    evidence_comments: list[str]


class AIGeneratedDetection(BaseModel):
    comment_id: str
    ai_generated_probability: float
    template_similarity_score: float
    reason: str


class BotScore(BaseModel):
    author_id: str
    bot_probability: float
    bot_reasons: list[str]
    influence_weight: float


class BotImpactSummary(BaseModel):
    suspected_bot_ratio: float
    suspected_bot_comment_ratio: float


class RiskBrief(BaseModel):
    risk_score: int
    risk_level: RiskLevel


class AnalysisResultResponse(BaseModel):
    project_id: str
    summary: str
    sentiment: SentimentSummary
    topics: list[TopicCluster]
    conflicts: list[ConflictResult]
    bot_score: BotImpactSummary
    risk: RiskBrief
    sentiment_results: list[SentimentResult] = Field(default_factory=list)
    ai_generated: list[AIGeneratedDetection] = Field(default_factory=list)
    bot_accounts: list[BotScore] = Field(default_factory=list)
    risk_model_version: str = RISK_MODEL_VERSION
    topic_risks: list[TopicRiskScore] = Field(default_factory=list)
    top_risk_topics: list[TopicRiskScore] = Field(default_factory=list)
    max_topic_risk: float | None = None
    average_topic_risk: float | None = None
    overall_risk: float | None = None
    real_crisis_risk: float | None = None
    manipulation_risk: float | None = None
    risk_explanation: str | None = None
    analysis_input_source: Literal["case_evidence_items", "case_raw_data", "mock_data_fallback"] = "mock_data_fallback"
    raw_post_count: int = 0
    raw_comment_count: int = 0
    evidence_item_count: int = 0
    evidence_source_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_type_counts: dict[str, int] = Field(default_factory=dict)
    evidence_trust_label_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_verification_status_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_provenance_type_distribution: dict[str, int] = Field(default_factory=dict)
    evidence_review_needed_count: int = 0
    evidence_unique_item_count: int = 0
    evidence_duplicate_item_count: int = 0
