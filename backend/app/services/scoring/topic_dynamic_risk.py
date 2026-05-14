from dataclasses import dataclass
from typing import Any


DYNAMIC_RISK_MODEL_VERSION = "v2_topic_dynamic_planned"


@dataclass(frozen=True)
class TopicRiskPlaceholder:
    cluster_id: str
    risk_score: float
    real_crisis_risk: float = 0.0
    manipulation_risk: float = 0.0
    risk_explanation: str = "V2 topic-cluster dynamic risk is planned but not implemented."


def is_v2_topic_dynamic_available() -> bool:
    """Return whether the V2 topic-cluster dynamic model is active."""
    return False


def build_topic_dynamic_risk_placeholder(topic_clusters: list[Any] | None = None) -> list[TopicRiskPlaceholder]:
    """Keep a typed extension point for future topic-window risk scoring."""
    _ = topic_clusters
    return []
