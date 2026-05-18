from __future__ import annotations

from app.services.simulation.schemas import (
    SimulationEthicsCheckResult,
    SimulationIntervention,
)


ALLOWED_INTERVENTION_TYPES = (
    "clarification",
    "apology",
    "compensation",
    "faq",
    "progress_update",
    "third_party_evidence",
    "misinformation_correction",
    "no_response",
)

FORBIDDEN_INTERVENTION_TYPES = (
    "fake_consensus",
    "bot_amplification",
    "fake_event",
    "deceptive_distraction",
    "covert_influencer_seeding",
    "targeted_persuasion",
    "suppression",
)


def check_intervention(intervention: SimulationIntervention) -> SimulationEthicsCheckResult:
    intervention_type = _normalize_type(intervention.intervention_type)
    if intervention_type in FORBIDDEN_INTERVENTION_TYPES:
        return SimulationEthicsCheckResult(
            allowed=False,
            reason=f"Forbidden intervention type rejected: {intervention_type}",
            blocked_categories=[intervention_type],
            allowed_intervention_types=list(ALLOWED_INTERVENTION_TYPES),
            forbidden_intervention_types=list(FORBIDDEN_INTERVENTION_TYPES),
            warnings=["Simulation Lab does not support manipulation, covert amplification, or suppression tactics."],
        )
    if intervention_type not in ALLOWED_INTERVENTION_TYPES:
        return SimulationEthicsCheckResult(
            allowed=False,
            reason=f"Unsupported intervention type: {intervention_type}",
            blocked_categories=["unsupported_intervention_type"],
            allowed_intervention_types=list(ALLOWED_INTERVENTION_TYPES),
            forbidden_intervention_types=list(FORBIDDEN_INTERVENTION_TYPES),
            warnings=["Use an allowed crisis-response intervention type from the ethics policy."],
        )
    if intervention.target_scope not in {"aggregate", "public", "community"}:
        return SimulationEthicsCheckResult(
            allowed=False,
            reason="Individual-level persuasion targeting is not supported.",
            blocked_categories=["individual_targeting"],
            allowed_intervention_types=list(ALLOWED_INTERVENTION_TYPES),
            forbidden_intervention_types=list(FORBIDDEN_INTERVENTION_TYPES),
            warnings=["Simulation outputs must remain aggregate-level."],
        )

    warnings: list[str] = []
    if intervention.intensity >= 0.95:
        warnings.append("Very high intervention intensity should be reviewed for realism.")
    return SimulationEthicsCheckResult(
        allowed=True,
        reason="Intervention is allowed for aggregate crisis-response comparison.",
        allowed_intervention_types=list(ALLOWED_INTERVENTION_TYPES),
        forbidden_intervention_types=list(FORBIDDEN_INTERVENTION_TYPES),
        warnings=warnings,
    )


def check_interventions(interventions: list[SimulationIntervention]) -> SimulationEthicsCheckResult:
    warnings: list[str] = []
    for intervention in interventions:
        result = check_intervention(intervention)
        warnings.extend(result.warnings)
        if not result.allowed:
            return result
    return SimulationEthicsCheckResult(
        allowed=True,
        reason="All interventions passed the Simulation Lab ethics policy.",
        allowed_intervention_types=list(ALLOWED_INTERVENTION_TYPES),
        forbidden_intervention_types=list(FORBIDDEN_INTERVENTION_TYPES),
        warnings=warnings,
    )


def build_no_response_intervention() -> SimulationIntervention:
    return SimulationIntervention(
        intervention_id="intervention_no_response",
        intervention_type="no_response",
        topic="brand_crisis",
        message="No public response is issued in this scenario.",
        stance_direction=0.0,
        emotional_intensity=0.0,
        evidence_strength=0.0,
        source_credibility=0.0,
        framing="no_response",
        intensity=0.0,
    )


def _normalize_type(value: str) -> str:
    return value.strip().lower()
