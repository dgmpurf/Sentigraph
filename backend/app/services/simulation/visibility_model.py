from __future__ import annotations

from app.services.simulation.schemas import (
    AudienceImpactBreakdown,
    SimulationIntervention,
    VisibilityIntervention,
    VisibilityInterventionResult,
)


VISIBILITY_INTERVENTION_TYPES = (
    "content_removal",
    "comment_closure",
    "account_restriction",
    "visibility_reduction",
    "platform_labeling",
    "policy_enforcement_notice",
    "content_removal_with_explanation",
)


ACTION_STRENGTH = {
    "content_removal": 0.92,
    "content_removal_with_explanation": 0.92,
    "visibility_reduction": 0.62,
    "comment_closure": 0.38,
    "account_restriction": 0.56,
    "platform_labeling": 0.28,
    "policy_enforcement_notice": 0.2,
}


DEFAULT_VISIBILITY_INPUTS = {
    "content_removal": {
        "public_explanation_quality": 0.18,
        "perceived_suppression": 0.58,
        "policy_violation_clarity": 0.66,
        "legitimacy_of_removal": 0.52,
        "reactance_amplification": 0.54,
        "martyr_effect": 0.42,
        "neutral_audience_negative_shift": 0.24,
        "hard_opposition_negative_shift": 0.38,
    },
    "content_removal_with_explanation": {
        "public_explanation_quality": 0.82,
        "perceived_suppression": 0.28,
        "policy_violation_clarity": 0.8,
        "legitimacy_of_removal": 0.78,
        "reactance_amplification": 0.32,
        "martyr_effect": 0.2,
        "neutral_audience_negative_shift": 0.1,
        "hard_opposition_negative_shift": 0.22,
    },
    "visibility_reduction": {
        "public_explanation_quality": 0.62,
        "perceived_suppression": 0.34,
        "policy_violation_clarity": 0.68,
        "legitimacy_of_removal": 0.64,
        "reactance_amplification": 0.36,
        "martyr_effect": 0.24,
        "neutral_audience_negative_shift": 0.13,
        "hard_opposition_negative_shift": 0.27,
    },
    "platform_labeling": {
        "public_explanation_quality": 0.78,
        "perceived_suppression": 0.18,
        "policy_violation_clarity": 0.72,
        "legitimacy_of_removal": 0.76,
        "reactance_amplification": 0.22,
        "martyr_effect": 0.12,
        "neutral_audience_negative_shift": 0.06,
        "hard_opposition_negative_shift": 0.14,
    },
    "policy_enforcement_notice": {
        "public_explanation_quality": 0.84,
        "perceived_suppression": 0.16,
        "policy_violation_clarity": 0.76,
        "legitimacy_of_removal": 0.78,
        "reactance_amplification": 0.2,
        "martyr_effect": 0.1,
        "neutral_audience_negative_shift": 0.05,
        "hard_opposition_negative_shift": 0.12,
    },
    "comment_closure": {
        "public_explanation_quality": 0.56,
        "perceived_suppression": 0.42,
        "policy_violation_clarity": 0.62,
        "legitimacy_of_removal": 0.58,
        "reactance_amplification": 0.4,
        "martyr_effect": 0.22,
        "neutral_audience_negative_shift": 0.16,
        "hard_opposition_negative_shift": 0.3,
    },
    "account_restriction": {
        "public_explanation_quality": 0.58,
        "perceived_suppression": 0.46,
        "policy_violation_clarity": 0.74,
        "legitimacy_of_removal": 0.66,
        "reactance_amplification": 0.42,
        "martyr_effect": 0.34,
        "neutral_audience_negative_shift": 0.18,
        "hard_opposition_negative_shift": 0.34,
    },
}


def is_visibility_intervention_type(value: str | None) -> bool:
    return _normalize_type(value) in VISIBILITY_INTERVENTION_TYPES


def default_visibility_intervention(intervention_type: str) -> VisibilityIntervention:
    normalized_type = _normalize_type(intervention_type)
    defaults = DEFAULT_VISIBILITY_INPUTS.get(normalized_type, {})
    return VisibilityIntervention(intervention_type=normalized_type, **defaults)


def visibility_intervention_for(intervention: SimulationIntervention) -> VisibilityIntervention | None:
    intervention_type = _normalize_type(intervention.intervention_type)
    if not is_visibility_intervention_type(intervention_type):
        return None
    if intervention.visibility_intervention:
        supplied = intervention.visibility_intervention
        supplied_type = _normalize_type(supplied.intervention_type) or intervention_type
        merged = default_visibility_intervention(supplied_type).model_dump()
        explicit_values = {
            field: getattr(supplied, field)
            for field in supplied.model_fields_set
            if hasattr(supplied, field)
        }
        merged.update(explicit_values)
        merged["intervention_type"] = supplied_type
        return VisibilityIntervention.model_validate(merged)
    return default_visibility_intervention(intervention_type)


def calculate_visibility_intervention_result(
    intervention: SimulationIntervention,
) -> VisibilityInterventionResult | None:
    visibility = visibility_intervention_for(intervention)
    if visibility is None:
        return None

    intervention_type = _normalize_type(visibility.intervention_type or intervention.intervention_type)
    action_strength = ACTION_STRENGTH.get(intervention_type, 0.35)
    time_factor = 1.0 - visibility.removal_time * 0.22
    copy_factor = 1.0 - visibility.residual_copies * 0.45
    migration_factor = 1.0 - visibility.repost_migration_probability * 0.22

    exposure_reduction = _clamp100(
        visibility.target_message_reach
        * visibility.current_visibility
        * action_strength
        * time_factor
        * copy_factor
        * migration_factor
        * 100.0
    )

    removal_legitimacy_score = _clamp100(
        (
            visibility.policy_violation_clarity * 0.34
            + visibility.legitimacy_of_removal * 0.32
            + visibility.public_explanation_quality * 0.22
            + (1.0 - visibility.perceived_suppression) * 0.12
        )
        * 100.0
    )

    perceived_suppression = _clamp01(
        visibility.perceived_suppression
        + (1.0 - visibility.policy_violation_clarity) * 0.28
        + (1.0 - visibility.public_explanation_quality) * 0.22
        - visibility.legitimacy_of_removal * 0.16
    )
    spillover_risk = _clamp100(
        (
            visibility.screenshot_probability * 0.34
            + visibility.repost_migration_probability * 0.28
            + visibility.residual_copies * 0.14
            + visibility.martyr_effect * 0.12
            + visibility.cross_platform_spillover * 0.12
        )
        * 100.0
    )
    backlash_cost = _clamp100(
        perceived_suppression * 25.0
        + visibility.reactance_amplification * 22.0
        + visibility.martyr_effect * 17.0
        + spillover_risk * 0.2
        + (1.0 - visibility.policy_violation_clarity) * 16.0
        - visibility.public_explanation_quality * 10.0
        - visibility.legitimacy_of_removal * 8.0
    )
    trust_loss = _clamp100(
        (1.0 - visibility.legitimacy_of_removal) * 28.0
        + (1.0 - visibility.public_explanation_quality) * 24.0
        + perceived_suppression * 20.0
        + visibility.neutral_audience_negative_shift * 42.0
        + (1.0 - visibility.policy_violation_clarity) * 16.0
    )
    neutral_audience_impact = _clamp100(
        visibility.neutral_audience_negative_shift * 72.0
        + perceived_suppression * 18.0
        + (1.0 - visibility.public_explanation_quality) * 10.0
    )
    opposition_group_impact = _clamp100(
        visibility.hard_opposition_negative_shift * 46.0
        + visibility.reactance_amplification * 22.0
        + visibility.martyr_effect * 16.0
        + perceived_suppression * 10.0
    )
    net_risk_change = _clamp100(
        backlash_cost * 0.26
        + trust_loss * 0.34
        + spillover_risk * 0.18
        + neutral_audience_impact * 0.32
        - exposure_reduction * 0.46
        + 24.0
    )

    audience_impact = AudienceImpactBreakdown(
        neutral_audience_impact=neutral_audience_impact,
        opposition_group_impact=opposition_group_impact,
        neutral_audience_negative_shift=visibility.neutral_audience_negative_shift,
        hard_opposition_negative_shift=visibility.hard_opposition_negative_shift,
        high_concern=neutral_audience_impact >= 38.0,
        explanation=(
            "Neutral audience movement is weighted as higher concern than hard-opposition-only backlash."
        ),
    )
    warnings = _visibility_warnings(
        visibility=visibility,
        neutral_audience_impact=neutral_audience_impact,
        spillover_risk=spillover_risk,
        removal_legitimacy_score=removal_legitimacy_score,
    )
    recommendation = _recommendation(
        visibility=visibility,
        exposure_reduction=exposure_reduction,
        backlash_cost=backlash_cost,
        trust_loss=trust_loss,
        spillover_risk=spillover_risk,
        neutral_audience_impact=neutral_audience_impact,
    )
    return VisibilityInterventionResult(
        intervention_type=intervention_type,
        exposure_reduction=exposure_reduction,
        backlash_cost=backlash_cost,
        trust_loss=trust_loss,
        spillover_risk=spillover_risk,
        net_risk_change=net_risk_change,
        removal_legitimacy_score=removal_legitimacy_score,
        public_explanation_quality_score=_clamp100(visibility.public_explanation_quality * 100.0),
        neutral_audience_impact=neutral_audience_impact,
        opposition_group_impact=opposition_group_impact,
        recommendation=recommendation,
        explanation=_explanation(intervention_type, recommendation, neutral_audience_impact, spillover_risk),
        audience_impact=audience_impact,
        warnings=warnings,
    )


def _recommendation(
    *,
    visibility: VisibilityIntervention,
    exposure_reduction: float,
    backlash_cost: float,
    trust_loss: float,
    spillover_risk: float,
    neutral_audience_impact: float,
) -> str:
    if visibility.policy_violation_clarity < 0.35 or visibility.legitimacy_of_removal < 0.35:
        return "prefer_labeling_or_clarification"
    if exposure_reduction < 20.0 and (backlash_cost > 40.0 or trust_loss > 36.0):
        return "not_recommended"
    if neutral_audience_impact >= 45.0 or spillover_risk >= 62.0 or trust_loss >= 52.0:
        return "conditional_human_review"
    if visibility.public_explanation_quality >= 0.65 and exposure_reduction >= 42.0:
        return "allowed_with_transparent_explanation"
    return "conditional_human_review"


def _visibility_warnings(
    *,
    visibility: VisibilityIntervention,
    neutral_audience_impact: float,
    spillover_risk: float,
    removal_legitimacy_score: float,
) -> list[str]:
    warnings: list[str] = []
    if neutral_audience_impact >= 38.0:
        warnings.append("Neutral audience negative shift is a high-concern tradeoff.")
    if spillover_risk >= 55.0:
        warnings.append("Screenshot or repost migration may increase cross-platform spillover.")
    if removal_legitimacy_score < 55.0:
        warnings.append("Policy clarity or legitimacy is weak; prefer labeling, clarification, or review.")
    if visibility.public_explanation_required and visibility.public_explanation_quality < 0.55:
        warnings.append("Transparent public explanation quality is below the safe-review threshold.")
    return warnings


def _explanation(
    intervention_type: str,
    recommendation: str,
    neutral_audience_impact: float,
    spillover_risk: float,
) -> str:
    if recommendation == "prefer_labeling_or_clarification":
        return (
            "Policy clarity or legitimacy is not strong enough for removal-first handling; compare labeling, "
            "clarification, or a transparent enforcement notice before any action."
        )
    if neutral_audience_impact >= 45.0:
        return (
            "Neutral-audience negative movement is material, so any visibility action requires human review "
            "and a transparent explanation."
        )
    if spillover_risk >= 62.0:
        return "Spillover risk is elevated; screenshots and repost migration may offset exposure reduction."
    if intervention_type == "platform_labeling":
        return "Platform labeling offers a lower-backlash visibility intervention with modest exposure reduction."
    return "Exposure reduction appears meaningful only as a lawful, platform-authorized, transparent action."


def _normalize_type(value: str | None) -> str:
    return (value or "").strip().lower()


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _clamp100(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)
