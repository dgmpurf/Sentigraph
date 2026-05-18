from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


SimulationStatus = Literal["completed", "rejected"]
SimulationTrend = Literal["improving", "worsening", "stable", "unknown"]
AgentStatus = Literal["active", "fatigued", "inactive"]
TargetScope = Literal["aggregate", "public", "community"]
SubIssueCategory = Literal[
    "product_quality",
    "official_response_delay",
    "pricing_dispute",
    "safety_legal_issue",
    "brand_trust",
    "suspected_manipulation",
    "public_figure_controversy",
    "workplace_company_issue",
    "unknown",
]
EvidenceQuality = Literal["weak", "mixed", "moderate", "strong"]
UncertaintyLabel = Literal["low", "medium", "high", "insufficient_data"]
FrameGapClassification = Literal[
    "aligned_public_and_frame",
    "frame_more_negative_than_public",
    "frame_more_positive_than_public",
    "polarized_frame",
    "manipulation_suspected_frame",
    "insufficient_data",
]
VisibilityRecommendation = Literal[
    "not_recommended",
    "conditional_human_review",
    "allowed_with_transparent_explanation",
    "prefer_labeling_or_clarification",
]


class SubIssue(BaseModel):
    sub_issue_id: str
    category: SubIssueCategory = "unknown"
    title: str
    summary: str = ""
    observed_volume: float = Field(default=0.0, ge=0.0, le=1.0)
    negative_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    neutral_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    positive_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    topic_risk_score: float = Field(default=0.0, ge=0.0, le=100.0)
    risk_score: float = Field(default=0.0, ge=0.0, le=100.0)
    risk_level: str = "low"
    real_crisis_signal: float = Field(default=0.0, ge=0.0, le=100.0)
    manipulation_signal: float = Field(default=0.0, ge=0.0, le=100.0)
    influence_proxy: float = Field(default=0.0, ge=0.0, le=100.0)
    evidence_quality: EvidenceQuality = "mixed"
    evidence_examples: list[str] = Field(default_factory=list)
    uncertainty_reasons: list[str] = Field(default_factory=list)


class AudienceSegment(BaseModel):
    segment_id: str
    label: str
    segment_type: str
    proportion: float = Field(default=0.0, ge=0.0, le=1.0)
    stance_distribution: dict[str, float] = Field(default_factory=dict)
    sentiment_distribution: dict[str, float] = Field(default_factory=dict)
    color_hint: str = "gray"
    average_attention_level: float = Field(default=0.5, ge=0.0, le=1.0)
    opinion_baseline: float = Field(default=0.0, ge=-1.0, le=1.0)
    action_threshold: float = Field(default=0.35, ge=0.0, le=1.0)
    influence_proxy: float = Field(default=20.0, ge=0.0, le=100.0)
    attention_level_source: str = "assumed"
    action_threshold_source: str = "assumed"
    bridge_score: float = Field(default=0.0, ge=0.0, le=1.0)
    data_origin: str = "synthetic_default"
    warnings: list[str] = Field(default_factory=list)


class PersonaCluster(BaseModel):
    cluster_id: str
    segment_id: str
    label: str
    confirmation_bias: float = Field(default=0.45, ge=0.0, le=1.0)
    authority_trust: float = Field(default=0.55, ge=0.0, le=1.0)
    conformity: float = Field(default=0.45, ge=0.0, le=1.0)
    reactance: float = Field(default=0.35, ge=0.0, le=1.0)
    negativity_weight: float = Field(default=0.5, ge=0.0, le=1.0)
    attention_fatigue: float = Field(default=0.12, ge=0.0, le=1.0)
    identity_attachment: float = Field(default=0.4, ge=0.0, le=1.0)
    loss_sensitivity: float = Field(default=0.45, ge=0.0, le=1.0)
    moral_outrage_sensitivity: float = Field(default=0.42, ge=0.0, le=1.0)
    harm_salience: float = Field(default=0.0, ge=0.0, le=1.0)
    crisis_legitimacy_pressure: float = Field(default=0.0, ge=0.0, le=1.0)
    platform_activity: float = Field(default=0.5, ge=0.0, le=1.0)
    source: str = "synthetic_default"
    no_individual_profile: bool = True


class BaselinePublicProfile(BaseModel):
    baseline_id: str
    baseline_version: str = "ordinary_public_baseline_v1"
    event_category: SubIssueCategory = "unknown"
    expected_average_reaction: float = Field(default=0.0, ge=-1.0, le=1.0)
    expected_loss_sensitivity: float = Field(default=0.45, ge=0.0, le=1.0)
    expected_authority_trust: float = Field(default=0.58, ge=0.0, le=1.0)
    expected_reactance: float = Field(default=0.35, ge=0.0, le=1.0)
    expected_moral_outrage: float = Field(default=0.42, ge=0.0, le=1.0)
    expected_safety_legal_sensitivity: float = Field(default=0.48, ge=0.0, le=1.0)
    expected_policy_enforcement_tolerance: float = Field(default=0.55, ge=0.0, le=1.0)
    assumed_parameters: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class ObservedFrameProfile(BaseModel):
    observed_frame_id: str
    observed_comment_count: int = Field(default=0, ge=0)
    observed_post_count: int = Field(default=0, ge=0)
    observed_platforms: list[str] = Field(default_factory=list)
    stance_distribution: dict[str, float] = Field(default_factory=dict)
    sentiment_distribution: dict[str, float] = Field(default_factory=dict)
    topic_distribution: dict[str, float] = Field(default_factory=dict)
    top_risk_topics: list[str] = Field(default_factory=list)
    manipulation_signal_score: float = Field(default=0.0, ge=0.0, le=100.0)
    real_crisis_signal_score: float = Field(default=0.0, ge=0.0, le=100.0)
    harm_salience: float = Field(default=0.0, ge=0.0, le=1.0)
    loss_sensitivity: float = Field(default=0.45, ge=0.0, le=1.0)
    moral_outrage_sensitivity: float = Field(default=0.42, ge=0.0, le=1.0)
    crisis_legitimacy_pressure: float = Field(default=0.0, ge=0.0, le=1.0)
    suspected_manipulation_pressure: float = Field(default=0.0, ge=0.0, le=1.0)
    repetition_exposure: float = Field(default=0.0, ge=0.0, le=1.0)
    influence_distribution_summary: dict[str, float] = Field(default_factory=dict)
    audience_segments: list[AudienceSegment] = Field(default_factory=list)
    persona_clusters: list[PersonaCluster] = Field(default_factory=list)
    forecast_status: str = "not_available"
    snapshot_count: int = Field(default=0, ge=0)
    alert_count: int = Field(default=0, ge=0)
    uncertainty_label: UncertaintyLabel = "medium"
    confidence_warnings: list[str] = Field(default_factory=list)


class FrameGapAnalysis(BaseModel):
    analysis_id: str
    event_frame_id: str
    primary_classification: FrameGapClassification
    secondary_classifications: list[FrameGapClassification] = Field(default_factory=list)
    baseline_profile_id: str
    observed_frame_id: str
    gap_scores: dict[str, float] = Field(default_factory=dict)
    summary: str
    strategy_cautions: list[str] = Field(default_factory=list)
    monitoring_recommendations: list[str] = Field(default_factory=list)
    uncertainty_label: UncertaintyLabel = "medium"
    uncertainty_reasons: list[str] = Field(default_factory=list)
    aggregate_only: bool = True
    no_individual_targeting: bool = True
    no_manipulation_tactics: bool = True


class StrategyImplication(BaseModel):
    implication_id: str
    frame_gap_classification: FrameGapClassification
    recommended_simulation_options: list[str] = Field(default_factory=list)
    discouraged_options: list[str] = Field(default_factory=list)
    rationale: str
    human_review_required: bool = True
    confidence_label: UncertaintyLabel = "medium"
    safety_warnings: list[str] = Field(default_factory=list)


class EventFrame(BaseModel):
    event_frame_id: str
    case_id: str | None = None
    event_title: str
    event_summary: str = ""
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source_mode: str = "aggregate_case_output"
    data_safety: dict[str, bool] = Field(
        default_factory=lambda: {
            "aggregate_only": True,
            "no_real_account_targets": True,
            "no_private_data": True,
            "raw_payload_retained": False,
        }
    )
    sub_issues: list[SubIssue] = Field(default_factory=list)
    observed_frame_profile: ObservedFrameProfile
    baseline_public_profile: BaselinePublicProfile
    frame_gap_analysis: FrameGapAnalysis
    strategy_implications: list[StrategyImplication] = Field(default_factory=list)
    initialization_hints: dict[str, Any] = Field(default_factory=dict)
    uncertainty_label: UncertaintyLabel = "medium"
    uncertainty_reasons: list[str] = Field(default_factory=list)
    assumption_log: dict[str, list[str]] = Field(default_factory=dict)


class CaseSimulationInitializerConfig(BaseModel):
    min_observed_comments: int = Field(default=3, ge=0)
    synthetic_agent_count: int = Field(default=14, ge=6, le=40)
    include_representative_examples: bool = True
    max_evidence_examples_per_issue: int = Field(default=2, ge=0, le=5)
    model_version: str = "case_to_simulation_initializer_v1"


class CaseSimulationInitializationResult(BaseModel):
    case_id: str
    status: Literal["initialized", "partial"]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_version: str = "case_to_simulation_initializer_v1"
    event_frame: EventFrame
    audience_segments: list[AudienceSegment] = Field(default_factory=list)
    persona_clusters: list[PersonaCluster] = Field(default_factory=list)
    frame_gap_analysis: FrameGapAnalysis
    strategy_implications: list[StrategyImplication] = Field(default_factory=list)
    simulation_scenario: "SimulationScenario"
    warnings: list[str] = Field(default_factory=list)
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "aggregate_level_only": True,
            "real_api_calls": False,
            "real_llm_calls": False,
            "live_fetch_enabled": False,
            "individual_targeting": False,
            "automatic_action_execution": False,
        }
    )


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


class AudienceImpactBreakdown(BaseModel):
    neutral_audience_impact: float = Field(ge=0.0, le=100.0)
    opposition_group_impact: float = Field(ge=0.0, le=100.0)
    neutral_audience_negative_shift: float = Field(ge=0.0, le=1.0)
    hard_opposition_negative_shift: float = Field(ge=0.0, le=1.0)
    high_concern: bool = False
    explanation: str = ""


class BacklashModel(BaseModel):
    perceived_suppression: float = Field(default=0.35, ge=0.0, le=1.0)
    reactance_amplification: float = Field(default=0.35, ge=0.0, le=1.0)
    martyr_effect: float = Field(default=0.25, ge=0.0, le=1.0)
    cross_platform_spillover: float = Field(default=0.25, ge=0.0, le=1.0)
    neutral_audience_negative_shift: float = Field(default=0.12, ge=0.0, le=1.0)
    hard_opposition_negative_shift: float = Field(default=0.24, ge=0.0, le=1.0)


class VisibilityIntervention(BaseModel):
    intervention_type: str = "content_removal_with_explanation"
    target_message_reach: float = Field(default=0.82, ge=0.0, le=1.0)
    current_visibility: float = Field(default=1.0, ge=0.0, le=1.0)
    removal_time: float = Field(default=0.35, ge=0.0, le=1.0)
    residual_copies: float = Field(default=0.18, ge=0.0, le=1.0)
    screenshot_probability: float = Field(default=0.22, ge=0.0, le=1.0)
    repost_migration_probability: float = Field(default=0.18, ge=0.0, le=1.0)
    perceived_suppression: float = Field(default=0.3, ge=0.0, le=1.0)
    policy_violation_clarity: float = Field(default=0.78, ge=0.0, le=1.0)
    legitimacy_of_removal: float = Field(default=0.72, ge=0.0, le=1.0)
    public_explanation_quality: float = Field(default=0.76, ge=0.0, le=1.0)
    reactance_amplification: float = Field(default=0.32, ge=0.0, le=1.0)
    martyr_effect: float = Field(default=0.2, ge=0.0, le=1.0)
    cross_platform_spillover: float = Field(default=0.22, ge=0.0, le=1.0)
    neutral_audience_negative_shift: float = Field(default=0.1, ge=0.0, le=1.0)
    hard_opposition_negative_shift: float = Field(default=0.22, ge=0.0, le=1.0)
    policy_basis: str = "platform_policy"
    authorization_source: str = "platform_policy"
    public_explanation_required: bool = True


class VisibilityInterventionResult(BaseModel):
    intervention_type: str
    exposure_reduction: float = Field(ge=0.0, le=100.0)
    backlash_cost: float = Field(ge=0.0, le=100.0)
    trust_loss: float = Field(ge=0.0, le=100.0)
    spillover_risk: float = Field(ge=0.0, le=100.0)
    net_risk_change: float = Field(ge=0.0, le=100.0)
    removal_legitimacy_score: float = Field(ge=0.0, le=100.0)
    public_explanation_quality_score: float = Field(ge=0.0, le=100.0)
    neutral_audience_impact: float = Field(ge=0.0, le=100.0)
    opposition_group_impact: float = Field(ge=0.0, le=100.0)
    recommendation: VisibilityRecommendation
    explanation: str
    audience_impact: AudienceImpactBreakdown
    human_review_required: bool = True
    aggregate_level_only: bool = True
    warnings: list[str] = Field(default_factory=list)


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
    visibility_intervention: VisibilityIntervention | None = None


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
    visibility_intervention_result: VisibilityInterventionResult | None = None


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
    visibility_intervention_result: VisibilityInterventionResult | None = None
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
