from pydantic import BaseModel, Field

from app.schemas.common import RISK_MODEL_VERSION, DateRange, RiskLevel
from app.schemas.propagation import PropagationEdge, PropagationNode
from app.schemas.risk import TopicRiskScore


class VisualizationDataRequest(BaseModel):
    project_id: str
    date_range: DateRange | None = None
    platforms: list[str] = Field(default_factory=list)


class SentimentTrendPoint(BaseModel):
    time: str
    positive: int
    neutral: int
    negative: int


class RiskRadar(BaseModel):
    negative_sentiment: float
    bot_impact: float
    propagation_speed: float
    controversy: float
    trend_shift: float


class HeatmapPoint(BaseModel):
    platform: str
    time_bucket: str
    intensity: int


class VisualizationGraph(BaseModel):
    nodes: list[PropagationNode] = Field(default_factory=list)
    edges: list[PropagationEdge] = Field(default_factory=list)


class VisualizationTopicCluster(BaseModel):
    name: str
    value: int
    sentiment_score: float


class BotImpactVisualization(BaseModel):
    suspected_bot_ratio: float
    suspected_bot_comment_ratio: float


class VisualizationResponse(BaseModel):
    project_id: str
    risk_score: int
    risk_level: RiskLevel
    risk_model_version: str = RISK_MODEL_VERSION
    sentiment_trend: list[SentimentTrendPoint]
    risk_radar: RiskRadar
    heatmap: list[HeatmapPoint]
    propagation_graph: VisualizationGraph
    topic_clusters: list[VisualizationTopicCluster]
    bot_impact: BotImpactVisualization
    topic_risks: list[TopicRiskScore] = Field(default_factory=list)
    top_risk_topics: list[TopicRiskScore] = Field(default_factory=list)
    max_topic_risk: float | None = None
    average_topic_risk: float | None = None
    overall_risk: float | None = None
    real_crisis_risk: float | None = None
    manipulation_risk: float | None = None
    risk_explanation: str | None = None
