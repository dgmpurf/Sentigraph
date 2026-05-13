from pydantic import BaseModel, Field

from app.schemas.common import DateRange, RiskLevel
from app.schemas.propagation import PropagationEdge, PropagationNode


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
    sentiment_trend: list[SentimentTrendPoint]
    risk_radar: RiskRadar
    heatmap: list[HeatmapPoint]
    propagation_graph: VisualizationGraph
    topic_clusters: list[VisualizationTopicCluster]
    bot_impact: BotImpactVisualization

