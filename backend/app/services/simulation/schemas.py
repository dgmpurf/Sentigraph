from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


SimulationStatus = Literal["completed", "rejected"]
SimulationTrend = Literal["improving", "worsening", "stable", "unknown"]
AgentStatus = Literal["active", "fatigued", "inactive"]
TargetScope = Literal["aggregate", "public", "community"]


class SimulationAgent(BaseModel):
    agent_id: str
    community_id: str
    latent_opinion: float = Field(ge=-1.0, le=1.0)
    expressed_opinion: float = Field(ge=-1.0, le=1.0)
    prior_anchor: float = Field(ge=-1.0, le=1.0)
    stubbornness: float = Field(ge=0.0, le=1.0)
    confidence_radius: float = Field(ge=0.0, le=2.0)
    action_threshold: float = Field(ge=0.0, le=1.0)
    confirmation_bias: float = Field(ge=0.0, le=1.0)
    negativity_weight: float = Field(ge=0.0, le=3.0)
    reactance: float = Field(ge=0.0, le=1.0)
    authority_trust: float = Field(ge=0.0, le=1.0)
    conformity: float = Field(ge=0.0, le=1.0)
    attention_budget: float = Field(ge=0.0, le=1.0)
    fatigue: float = Field(ge=0.0, le=1.0)
    identity_group: str = "general_public"
    status: AgentStatus = "active"


class SimulationNetworkEdge(BaseModel):
    source_agent_id: str
    target_agent_id: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    bridge_score: float = Field(default=0.0, ge=0.0, le=1.0)
    relationship_type: str = "peer"


class SimulationMessage(BaseModel):
    message_id: str
    topic: str
    source_type: str
    source_credibility: float = Field(ge=0.0, le=1.0)
    stance_direction: float = Field(ge=-1.0, le=1.0)
    emotional_intensity: float = Field(ge=0.0, le=1.0)
    evidence_strength: float = Field(ge=0.0, le=1.0)
    framing: str = "neutral"
    novelty: float = Field(default=0.5, ge=0.0, le=1.0)
    repetition: float = Field(default=0.0, ge=0.0, le=1.0)
    platform_reach: float = Field(default=0.5, ge=0.0, le=1.0)


class SimulationIntervention(BaseModel):
    intervention_id: str
    intervention_type: str
    topic: str = "brand_crisis"
    source_type: str = "official"
    message: str = ""
    target_scope: TargetScope = "aggregate"
    publication_step: int = Field(default=1, ge=0)
    source_credibility: float = Field(default=0.75, ge=0.0, le=1.0)
    stance_direction: float = Field(default=0.35, ge=-1.0, le=1.0)
    emotional_intensity: float = Field(default=0.25, ge=0.0, le=1.0)
    evidence_strength: float = Field(default=0.65, ge=0.0, le=1.0)
    framing: str = "clarifying"
    responsibility_acknowledgement: float = Field(default=0.4, ge=0.0, le=1.0)
    transparency_level: float = Field(default=0.7, ge=0.0, le=1.0)
    intensity: float = Field(default=0.6, ge=0.0, le=1.0)


class SimulationConfig(BaseModel):
    steps: int = Field(default=6, ge=1, le=50)
    seed: int | None = None
    peer_influence_weight: float = Field(default=0.28, ge=0.0, le=1.0)
    message_influence_weight: float = Field(default=0.32, ge=0.0, le=1.0)
    prior_persistence_weight: float = Field(default=0.35, ge=0.0, le=1.0)
    attention_decay: float = Field(default=0.08, ge=0.0, le=1.0)
    fatigue_increase: float = Field(default=0.035, ge=0.0, le=1.0)
    model_version: str = "simulation_lab_mvp_v1"


class SimulationScenario(BaseModel):
    scenario_id: str
    name: str
    description: str = ""
    topic: str = "brand_crisis"
    agents: list[SimulationAgent] = Field(default_factory=list)
    network_edges: list[SimulationNetworkEdge] = Field(default_factory=list)
    messages: list[SimulationMessage] = Field(default_factory=list)
    interventions: list[SimulationIntervention] = Field(default_factory=list)
    config: SimulationConfig = Field(default_factory=SimulationConfig)
    responsibility_level: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SimulationEthicsCheckResult(BaseModel):
    allowed: bool
    reason: str
    blocked_categories: list[str] = Field(default_factory=list)
    allowed_intervention_types: list[str] = Field(default_factory=list)
    forbidden_intervention_types: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SimulationMetricSummary(BaseModel):
    average_latent_opinion: float
    average_expressed_opinion: float
    negative_ratio: float
    neutral_ratio: float
    positive_ratio: float
    polarization_index: float
    attention_level: float
    trust_recovery_proxy: float
    intervention_effect_score: float
    false_belief_proxy: float = 0.0
    min_latent_opinion: float = Field(default=-1.0, ge=-1.0, le=1.0)
    max_latent_opinion: float = Field(default=1.0, ge=-1.0, le=1.0)
    min_expressed_opinion: float = Field(default=-1.0, ge=-1.0, le=1.0)
    max_expressed_opinion: float = Field(default=1.0, ge=-1.0, le=1.0)
    ethical_risk_flags: list[str] = Field(default_factory=list)


class SimulationStepResult(BaseModel):
    step: int
    active_intervention_type: str
    metrics: SimulationMetricSummary
    trend_direction: SimulationTrend
    forecast_reason: str
    community_metrics: dict[str, SimulationMetricSummary] = Field(default_factory=dict)


class SimulationRunResult(BaseModel):
    scenario_id: str
    scenario_name: str
    simulation_status: SimulationStatus
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_version: str = "simulation_lab_mvp_v1"
    steps_requested: int
    steps_completed: int
    ethics_check: SimulationEthicsCheckResult
    initial_metrics: SimulationMetricSummary
    final_metrics: SimulationMetricSummary
    step_results: list[SimulationStepResult]
    key_findings: list[str] = Field(default_factory=list)
    recommended_interpretation: str
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "aggregate_level_only": True,
            "real_api_calls": False,
            "real_llm_calls": False,
            "live_fetch_enabled": False,
            "individual_targeting": False,
        }
    )
    warnings: list[str] = Field(default_factory=list)


class SimulationEthicsPolicyResponse(BaseModel):
    allowed_intervention_types: list[str]
    forbidden_intervention_types: list[str]
    policy_summary: str
    aggregate_level_only: bool = True
