from __future__ import annotations

from app.services.simulation.schemas import SimulationAgent


def create_echo_chamber_agents() -> list[SimulationAgent]:
    return [
        _agent("a01", "concerned", -0.72, -0.62, "quality_concern"),
        _agent("a02", "concerned", -0.58, -0.45, "quality_concern", attention=0.78),
        _agent("a03", "concerned", -0.48, -0.35, "quality_concern", confirmation=0.68),
        _agent("a04", "concerned", -0.28, -0.18, "price_sensitive", confidence=0.42),
        _agent("a05", "neutral", -0.08, -0.04, "mainstream", authority=0.62, confirmation=0.35),
        _agent("a06", "neutral", 0.04, 0.02, "mainstream", authority=0.68, confirmation=0.3),
        _agent("a07", "supportive", 0.25, 0.18, "brand_supporter", negativity=1.05, authority=0.7),
        _agent("a08", "supportive", 0.38, 0.25, "brand_supporter", negativity=1.0, authority=0.72),
    ]


def create_brand_crisis_agents() -> list[SimulationAgent]:
    return [
        _agent("bc01", "affected_users", -0.78, -0.7, "quality_concern", attention=0.9, negativity=1.45),
        _agent("bc02", "affected_users", -0.68, -0.55, "quality_concern", attention=0.84, negativity=1.35),
        _agent("bc03", "affected_users", -0.56, -0.4, "service_concern", attention=0.78),
        _agent("bc04", "watchers", -0.32, -0.2, "mainstream", authority=0.58, confirmation=0.42),
        _agent("bc05", "watchers", -0.18, -0.08, "mainstream", authority=0.62, confirmation=0.36),
        _agent("bc06", "watchers", -0.05, -0.02, "mainstream", authority=0.66, confirmation=0.32),
        _agent("bc07", "supporters", 0.16, 0.12, "brand_supporter", negativity=1.0, authority=0.72),
        _agent("bc08", "supporters", 0.28, 0.18, "brand_supporter", negativity=0.95, authority=0.76),
        _agent("bc09", "bridge", -0.12, -0.05, "industry_observer", authority=0.7, confirmation=0.28),
        _agent("bc10", "bridge", 0.05, 0.02, "industry_observer", authority=0.74, confirmation=0.24),
    ]


def create_misinformation_agents() -> list[SimulationAgent]:
    return [
        _agent("mi01", "rumor_exposed", -0.62, -0.5, "safety_concern", attention=0.9, negativity=1.5),
        _agent("mi02", "rumor_exposed", -0.52, -0.38, "safety_concern", attention=0.86, negativity=1.45),
        _agent("mi03", "rumor_exposed", -0.42, -0.3, "safety_concern", attention=0.8),
        _agent("mi04", "uncertain", -0.12, -0.05, "mainstream", authority=0.62, confirmation=0.35),
        _agent("mi05", "uncertain", 0.02, 0.0, "mainstream", authority=0.68, confirmation=0.28),
        _agent("mi06", "evidence_oriented", 0.18, 0.1, "evidence_oriented", authority=0.82, confirmation=0.18),
        _agent("mi07", "evidence_oriented", 0.24, 0.16, "evidence_oriented", authority=0.86, confirmation=0.16),
        _agent("mi08", "bridge", -0.04, -0.02, "industry_observer", authority=0.72, confirmation=0.22),
    ]


def create_high_reach_video_agents() -> list[SimulationAgent]:
    return [
        _agent("hv01", "hard_opposition", -0.84, -0.78, "hard_opposition", attention=0.94, negativity=1.55, confirmation=0.74),
        _agent("hv02", "hard_opposition", -0.72, -0.62, "hard_opposition", attention=0.9, negativity=1.48, confirmation=0.68),
        _agent("hv03", "neutral_audience", -0.22, -0.1, "neutral_observer", attention=0.82, authority=0.58, confirmation=0.34),
        _agent("hv04", "neutral_audience", -0.08, -0.02, "neutral_observer", attention=0.78, authority=0.64, confirmation=0.28),
        _agent("hv05", "neutral_audience", 0.02, 0.0, "neutral_observer", attention=0.74, authority=0.68, confirmation=0.24),
        _agent("hv06", "authority_trusting", 0.14, 0.08, "authority_trusting", attention=0.68, authority=0.82, confirmation=0.18),
        _agent("hv07", "authority_trusting", 0.24, 0.14, "authority_trusting", attention=0.64, authority=0.86, confirmation=0.16),
        _agent("hv08", "bridge_nodes", -0.06, -0.02, "bridge_observer", attention=0.82, authority=0.72, confirmation=0.2, confidence=0.68),
        _agent("hv09", "bridge_nodes", 0.08, 0.04, "bridge_observer", attention=0.78, authority=0.74, confirmation=0.18, confidence=0.72),
        _agent("hv10", "supporters", 0.32, 0.22, "brand_supporter", attention=0.62, authority=0.72, confirmation=0.24),
    ]


def _agent(
    agent_id: str,
    community_id: str,
    latent: float,
    expressed: float,
    identity: str,
    *,
    attention: float = 0.72,
    negativity: float = 1.2,
    authority: float = 0.55,
    confirmation: float = 0.5,
    confidence: float = 0.5,
) -> SimulationAgent:
    return SimulationAgent(
        agent_id=agent_id,
        community_id=community_id,
        latent_opinion=latent,
        expressed_opinion=expressed,
        prior_anchor=latent,
        stubbornness=0.45 + confirmation * 0.25,
        confidence_radius=confidence,
        action_threshold=0.18,
        confirmation_bias=confirmation,
        negativity_weight=negativity,
        reactance=0.22 + confirmation * 0.22,
        authority_trust=authority,
        conformity=0.45,
        attention_budget=attention,
        fatigue=0.08,
        identity_group=identity,
        status="active",
    )
