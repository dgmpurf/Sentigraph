from pydantic import BaseModel, Field


class PropagationNode(BaseModel):
    node_id: str
    type: str
    platform: str
    content: str
    author_id: str
    created_at: str
    sentiment_score: float
    influence_score: float


class PropagationEdge(BaseModel):
    source: str
    target: str
    relation: str
    weight: float


class PropagationMetrics(BaseModel):
    depth: int
    breadth: int
    central_node_id: str
    propagation_speed: float


class PropagationGraph(BaseModel):
    nodes: list[PropagationNode] = Field(default_factory=list)
    edges: list[PropagationEdge] = Field(default_factory=list)
    metrics: PropagationMetrics | None = None


class PropagationResponse(BaseModel):
    project_id: str
    nodes: list[PropagationNode]
    edges: list[PropagationEdge]
    metrics: PropagationMetrics

