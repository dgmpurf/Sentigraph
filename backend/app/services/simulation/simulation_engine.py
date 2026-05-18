from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.services.simulation.agent_factory import (
    create_brand_crisis_agents,
    create_echo_chamber_agents,
    create_high_reach_video_agents,
    create_misinformation_agents,
)
from app.services.simulation.errors import SimulationEthicsError
from app.services.simulation.intervention_library import (
    ALLOWED_INTERVENTION_TYPES,
    FORBIDDEN_INTERVENTION_TYPES,
    build_no_response_intervention,
    check_interventions,
)
from app.services.simulation.message_model import intervention_to_message
from app.services.simulation.network_builder import build_homophilous_network
from app.services.simulation.opinion_update import update_agents_for_step
from app.services.simulation.schemas import (
    SimulationConfig,
    SimulationIntervention,
    SimulationMessage,
    SimulationMetricSummary,
    SimulationRunResult,
    SimulationScenario,
    SimulationStepResult,
    VisibilityInterventionResult,
)
from app.services.simulation.simulation_metrics import calculate_community_metrics, calculate_metrics
from app.services.simulation.visibility_model import (
    calculate_visibility_intervention_result,
    default_visibility_intervention,
)


def run_simulation(scenario: SimulationScenario, steps: int | None = None) -> SimulationRunResult:
    ethics_check = check_interventions(scenario.interventions)
    if not ethics_check.allowed:
        raise SimulationEthicsError(
            ethics_check.reason,
            blocked_categories=ethics_check.blocked_categories,
            intervention_type=(scenario.interventions[0].intervention_type if scenario.interventions else None),
        )

    config = scenario.config.model_copy(update={"steps": steps or scenario.config.steps})
    agents = [agent.model_copy(deep=True) for agent in scenario.agents] or create_echo_chamber_agents()
    edges = scenario.network_edges or build_homophilous_network(agents)
    initial_metrics = calculate_metrics(agents, ethical_flags=ethics_check.warnings)
    baseline_metrics = initial_metrics
    step_results: list[SimulationStepResult] = []
    visibility_results: list[VisibilityInterventionResult] = []

    for step in range(1, config.steps + 1):
        active_intervention = _active_intervention_for_step(scenario.interventions, step)
        step_messages = [message.model_copy(deep=True) for message in scenario.messages]
        step_messages.append(intervention_to_message(active_intervention, step))
        agents = update_agents_for_step(agents, edges, step_messages, config)
        metrics = calculate_metrics(agents, baseline=baseline_metrics, ethical_flags=ethics_check.warnings)
        visibility_result = calculate_visibility_intervention_result(active_intervention)
        if visibility_result:
            visibility_results.append(visibility_result)
        step_results.append(
            SimulationStepResult(
                step=step,
                active_intervention_type=active_intervention.intervention_type,
                metrics=metrics,
                trend_direction=_trend_direction(baseline_metrics, metrics),
                forecast_reason=_step_reason(active_intervention.intervention_type, baseline_metrics, metrics),
                community_metrics=calculate_community_metrics(
                    agents,
                    baseline=baseline_metrics,
                    ethical_flags=ethics_check.warnings,
                ),
                visibility_intervention_result=visibility_result,
            )
        )

    final_metrics = step_results[-1].metrics if step_results else initial_metrics
    final_visibility_result = visibility_results[-1] if visibility_results else None
    warnings = [
        "Simulation Lab MVP uses synthetic agents and deterministic assumptions.",
        "Do not use outputs for individual-level targeting or covert influence.",
    ]
    if final_visibility_result:
        warnings.extend(final_visibility_result.warnings)
    return SimulationRunResult(
        scenario_id=scenario.scenario_id,
        scenario_name=scenario.name,
        simulation_status="completed",
        generated_at=_deterministic_generated_at(config.seed),
        model_version=config.model_version,
        steps_requested=config.steps,
        steps_completed=len(step_results),
        ethics_check=ethics_check,
        initial_metrics=initial_metrics,
        final_metrics=final_metrics,
        step_results=step_results,
        visibility_intervention_result=final_visibility_result,
        key_findings=_key_findings(initial_metrics, final_metrics, final_visibility_result),
        recommended_interpretation=(
            "This deterministic MVP simulation compares aggregate crisis-response scenarios. "
            "It is a transparent trend rehearsal, not a prediction of real individual behavior."
        ),
        warnings=warnings,
    )


def create_default_echo_chamber_scenario() -> SimulationScenario:
    agents = create_echo_chamber_agents()
    return SimulationScenario(
        scenario_id="simulation_demo_echo_chamber",
        name="Default Echo Chamber Demo",
        description="Synthetic aggregate echo-chamber scenario for ethical intervention comparison.",
        topic="product_quality_discussion",
        agents=agents,
        network_edges=build_homophilous_network(agents),
        messages=[
            SimulationMessage(
                message_id="message_quality_complaint",
                topic="product_quality_discussion",
                source_type="public_posts",
                source_credibility=0.62,
                stance_direction=-0.58,
                emotional_intensity=0.58,
                evidence_strength=0.45,
                framing="safety",
                novelty=0.72,
                repetition=0.18,
                platform_reach=0.7,
            )
        ],
        interventions=[
            SimulationIntervention(
                intervention_id="intervention_clarification",
                intervention_type="clarification",
                topic="product_quality_discussion",
                message="Clarify known facts, investigation scope, and next update time.",
                publication_step=1,
                intensity=0.62,
            )
        ],
        config=SimulationConfig(steps=6),
        metadata={"safe_demo": True, "aggregate_only": True},
    )


def create_brand_crisis_scenario(
    *,
    intervention_type: str = "clarification",
    steps: int = 6,
    responsibility_level: float = 0.72,
) -> SimulationScenario:
    agents = create_brand_crisis_agents()
    return SimulationScenario(
        scenario_id=f"simulation_brand_crisis_{intervention_type}",
        name="Brand Crisis Response Scenario",
        description="Synthetic crisis-response rehearsal using aggregate public-opinion assumptions.",
        topic="brand_product_quality",
        agents=agents,
        network_edges=build_homophilous_network(agents),
        messages=[
            SimulationMessage(
                message_id="message_brand_quality_crisis",
                topic="brand_product_quality",
                source_type="public_posts",
                source_credibility=0.68,
                stance_direction=-0.72,
                emotional_intensity=0.74,
                evidence_strength=0.58,
                framing="accountability",
                novelty=0.82,
                repetition=0.28,
                platform_reach=0.76,
            )
        ],
        interventions=[
            SimulationIntervention(
                intervention_id=f"intervention_{intervention_type}",
                intervention_type=intervention_type,
                topic="brand_product_quality",
                message=_intervention_message(intervention_type),
                publication_step=1,
                responsibility_acknowledgement=responsibility_level,
                intensity=0.68 if intervention_type != "no_response" else 0.0,
            )
        ],
        config=SimulationConfig(steps=steps),
        responsibility_level=responsibility_level,
        metadata={"scenario_family": "brand_crisis", "aggregate_only": True},
    )


def create_misinformation_correction_scenario(
    *,
    intervention_type: str = "misinformation_correction",
    steps: int = 6,
) -> SimulationScenario:
    agents = create_misinformation_agents()
    return SimulationScenario(
        scenario_id=f"simulation_misinformation_{intervention_type}",
        name="Misinformation Correction Scenario",
        description="Synthetic aggregate scenario for comparing transparent correction responses.",
        topic="misinformation_correction",
        agents=agents,
        network_edges=build_homophilous_network(agents),
        messages=[
            SimulationMessage(
                message_id="message_unverified_claim",
                topic="misinformation_correction",
                source_type="public_posts",
                source_credibility=0.42,
                stance_direction=-0.68,
                emotional_intensity=0.7,
                evidence_strength=0.28,
                framing="safety",
                novelty=0.86,
                repetition=0.38,
                platform_reach=0.72,
            )
        ],
        interventions=[
            SimulationIntervention(
                intervention_id=f"intervention_{intervention_type}",
                intervention_type=intervention_type,
                topic="misinformation_correction",
                message=_intervention_message(intervention_type),
                publication_step=1,
                source_credibility=0.82,
                evidence_strength=0.82,
                intensity=0.72 if intervention_type != "no_response" else 0.0,
            )
        ],
        config=SimulationConfig(steps=steps),
        metadata={"scenario_family": "misinformation_correction", "aggregate_only": True},
    )


def create_high_reach_negative_video_scenario(
    *,
    intervention_type: str = "content_removal_with_explanation",
    steps: int = 6,
) -> SimulationScenario:
    agents = create_high_reach_video_agents()
    default_visibility = default_visibility_intervention(intervention_type)
    visibility = default_visibility.model_copy(
        update={
            "target_message_reach": 0.94,
            "current_visibility": 1.0,
            "residual_copies": 0.22,
            "screenshot_probability": 0.28,
            "repost_migration_probability": 0.22,
            "cross_platform_spillover": 0.26,
            "policy_basis": "platform_policy_public_harm_rule",
            "authorization_source": "platform_policy",
            "public_explanation_required": True,
        }
    )
    return SimulationScenario(
        scenario_id=f"simulation_high_reach_video_{intervention_type}",
        name="High-Reach Negative Video Visibility Scenario",
        description=(
            "Synthetic aggregate scenario comparing lawful platform-authorized visibility actions, "
            "transparent explanation, and backlash/spillover tradeoffs."
        ),
        topic="high_reach_negative_video",
        agents=agents,
        network_edges=build_homophilous_network(agents),
        messages=[
            SimulationMessage(
                message_id="message_high_reach_negative_video",
                topic="high_reach_negative_video",
                source_type="public_video",
                source_credibility=0.54,
                stance_direction=-0.78,
                emotional_intensity=0.82,
                evidence_strength=0.46,
                framing="safety",
                novelty=0.88,
                repetition=0.32,
                platform_reach=0.94,
            )
        ],
        interventions=[
            SimulationIntervention(
                intervention_id=f"intervention_{intervention_type}",
                intervention_type=intervention_type,
                topic="high_reach_negative_video",
                message=_intervention_message(intervention_type),
                publication_step=1,
                source_credibility=0.8,
                stance_direction=0.2,
                emotional_intensity=0.18,
                evidence_strength=0.76,
                framing=intervention_type,
                transparency_level=0.82 if intervention_type == "content_removal_with_explanation" else 0.38,
                intensity=0.72 if intervention_type != "no_response" else 0.0,
                visibility_intervention=visibility if intervention_type != "no_response" else None,
            )
        ],
        config=SimulationConfig(steps=steps),
        metadata={
            "scenario_family": "content_visibility_intervention",
            "aggregate_only": True,
            "human_review_required": True,
            "does_not_execute_platform_action": True,
        },
    )


def _active_intervention_for_step(
    interventions: list[SimulationIntervention],
    step: int,
) -> SimulationIntervention:
    active = [
        intervention
        for intervention in interventions
        if intervention.publication_step <= step
    ]
    if not active:
        return build_no_response_intervention()
    return sorted(active, key=lambda item: item.publication_step)[-1]


def _trend_direction(
    initial_metrics: SimulationMetricSummary,
    current_metrics: SimulationMetricSummary,
) -> str:
    delta = current_metrics.average_expressed_opinion - initial_metrics.average_expressed_opinion
    if delta >= 0.04:
        return "improving"
    if delta <= -0.04:
        return "worsening"
    return "stable"


def _step_reason(
    intervention_type: str,
    initial_metrics: SimulationMetricSummary,
    current_metrics: SimulationMetricSummary,
) -> str:
    negative_delta = current_metrics.negative_ratio - initial_metrics.negative_ratio
    if intervention_type == "no_response":
        return "No-response baseline keeps message pressure driven by the original public discussion."
    if negative_delta < -0.03:
        return "Negative aggregate expression declined after the transparent response entered the scenario."
    if current_metrics.trust_recovery_proxy > 0.5:
        return "Trust recovery proxy improved because aggregate latent opinion moved toward neutral or supportive territory."
    return "Aggregate response impact remains limited under the current synthetic assumptions."


def _key_findings(
    initial_metrics: SimulationMetricSummary,
    final_metrics: SimulationMetricSummary,
    visibility_result: VisibilityInterventionResult | None = None,
) -> list[str]:
    findings = [
        f"Average expressed opinion changed from {initial_metrics.average_expressed_opinion:.2f} to {final_metrics.average_expressed_opinion:.2f}.",
        f"Negative ratio changed from {initial_metrics.negative_ratio:.2f} to {final_metrics.negative_ratio:.2f}.",
        f"Attention level ended at {final_metrics.attention_level:.2f}; fatigue is represented indirectly through declining attention.",
    ]
    if final_metrics.intervention_effect_score > 8:
        findings.append("The ethical response package shows a positive aggregate intervention effect proxy.")
    else:
        findings.append("The aggregate intervention effect proxy remains limited in this deterministic run.")
    if visibility_result:
        findings.append(
            "Visibility tradeoff model estimates "
            f"{visibility_result.exposure_reduction:.1f}/100 exposure reduction and "
            f"{visibility_result.backlash_cost:.1f}/100 backlash cost."
        )
    return findings


def _deterministic_generated_at(seed: int | None) -> datetime:
    return datetime(2026, 5, 18, 0, 0, tzinfo=timezone.utc) + timedelta(seconds=seed or 0)


def _intervention_message(intervention_type: str) -> str:
    messages = {
        "clarification": "Publish verified facts, scope, and a clear next-update time.",
        "apology": "Acknowledge responsibility, apologize for impact, and state corrective steps.",
        "compensation": "Explain a transparent compensation or remediation path for affected users.",
        "faq": "Publish an FAQ that answers recurring factual questions.",
        "progress_update": "Share a progress update with investigation status and next milestones.",
        "third_party_evidence": "Share independently verifiable evidence from a credible third party.",
        "misinformation_correction": "Correct unsupported claims with evidence and calm factual language.",
        "content_removal": "Simulate lawful platform-authorized removal without assuming automatic execution.",
        "comment_closure": "Simulate platform-authorized comment closure and its aggregate backlash tradeoff.",
        "account_restriction": "Simulate policy-based account restriction as an aggregate scenario variable.",
        "visibility_reduction": "Simulate lawful visibility reduction and its exposure/backlash tradeoff.",
        "platform_labeling": "Simulate a platform label that adds context without removing the content.",
        "policy_enforcement_notice": "Simulate a transparent policy enforcement notice.",
        "content_removal_with_explanation": "Simulate policy-based removal paired with a transparent public explanation.",
        "no_response": "No public response is issued.",
    }
    return messages.get(intervention_type, "Unsupported response type.")


def ethics_policy_dict() -> dict[str, object]:
    return {
        "allowed_intervention_types": list(ALLOWED_INTERVENTION_TYPES),
        "forbidden_intervention_types": list(FORBIDDEN_INTERVENTION_TYPES),
        "policy_summary": (
            "Simulation Lab supports aggregate-level ethical crisis-response comparison only. "
            "It can model lawful platform-authorized visibility interventions as tradeoffs for human review. "
            "It rejects manipulation, bot amplification, fake events, deceptive diversion, covert seeding, "
            "targeted persuasion, illegal suppression, and covert censorship."
        ),
        "aggregate_level_only": True,
    }
