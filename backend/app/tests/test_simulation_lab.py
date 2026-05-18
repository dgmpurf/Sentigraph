from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.simulation.errors import SimulationEthicsError
from app.services.simulation.schemas import (
    SimulationAgent,
    SimulationConfig,
    SimulationIntervention,
    SimulationMessage,
    SimulationNetworkEdge,
    SimulationScenario,
    VisibilityIntervention,
)
from app.services.simulation.visibility_model import (
    VISIBILITY_INTERVENTION_TYPES,
    calculate_visibility_intervention_result,
)
from app.services.simulation.opinion_update import update_agents_for_step
from app.services.simulation.simulation_engine import (
    create_brand_crisis_scenario,
    create_default_echo_chamber_scenario,
    create_high_reach_negative_video_scenario,
    create_misinformation_correction_scenario,
    run_simulation,
)
from scripts.run_offline_benchmarks import _run_simulation_lab_benchmark


client = TestClient(app)


def test_default_demo_scenario_builds() -> None:
    scenario = create_default_echo_chamber_scenario()

    assert scenario.scenario_id == "simulation_demo_echo_chamber"
    assert scenario.agents
    assert scenario.network_edges
    assert scenario.interventions[0].intervention_type == "clarification"


def test_brand_crisis_scenario_builds() -> None:
    scenario = create_brand_crisis_scenario(intervention_type="apology")

    assert scenario.topic == "brand_product_quality"
    assert scenario.interventions[0].intervention_type == "apology"
    assert scenario.responsibility_level > 0.5


def test_simulation_output_is_deterministic() -> None:
    scenario = create_misinformation_correction_scenario()

    first = run_simulation(scenario).model_dump(mode="json")
    second = run_simulation(scenario).model_dump(mode="json")

    assert first == second


def test_simulation_output_is_deterministic_with_same_seed() -> None:
    base = create_brand_crisis_scenario(intervention_type="apology")
    scenario = base.model_copy(update={"config": base.config.model_copy(update={"seed": 42})}, deep=True)

    first = run_simulation(scenario).model_dump(mode="json")
    second = run_simulation(scenario).model_dump(mode="json")

    assert first == second
    assert first["generated_at"] == "2026-05-18T00:00:42Z"


def test_opinions_stay_clamped_to_minus_one_one() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="apology", steps=8))

    for step in result.step_results:
        metrics = step.metrics
        assert -1 <= metrics.min_latent_opinion <= 1
        assert -1 <= metrics.max_latent_opinion <= 1
        assert -1 <= metrics.min_expressed_opinion <= 1
        assert -1 <= metrics.max_expressed_opinion <= 1


def test_metrics_are_present() -> None:
    result = run_simulation(create_default_echo_chamber_scenario())
    metrics = result.final_metrics

    assert result.simulation_status == "completed"
    assert metrics.negative_ratio >= 0
    assert metrics.neutral_ratio >= 0
    assert metrics.positive_ratio >= 0
    assert metrics.polarization_index >= 0
    assert metrics.attention_level >= 0
    assert result.safe_mode["aggregate_level_only"] is True


def test_forbidden_intervention_rejected() -> None:
    scenario = create_brand_crisis_scenario(intervention_type="fake_consensus")

    with pytest.raises(SimulationEthicsError) as exc:
        run_simulation(scenario)

    assert "fake_consensus" in exc.value.blocked_categories


def test_ethics_policy_lists_allowed_and_forbidden_interventions() -> None:
    response = client.get("/api/v1/simulation/ethics-policy")

    assert response.status_code == 200
    body = response.json()
    assert set(body["allowed_intervention_types"]) == {
        "clarification",
        "apology",
        "compensation",
        "faq",
        "progress_update",
        "third_party_evidence",
        "misinformation_correction",
        "no_response",
        "content_removal",
        "comment_closure",
        "account_restriction",
        "visibility_reduction",
        "platform_labeling",
        "policy_enforcement_notice",
        "content_removal_with_explanation",
    }
    assert set(body["forbidden_intervention_types"]) == {
        "fake_consensus",
        "bot_amplification",
        "fake_event",
        "deceptive_distraction",
        "covert_influencer_seeding",
        "targeted_persuasion",
        "suppression",
        "illegal_suppression",
        "covert_censorship",
        "covert_suppression",
        "targeted_silencing",
        "platform_governance_evasion",
    }
    assert body["aggregate_level_only"] is True


def test_ethical_intervention_accepted() -> None:
    result = run_simulation(create_brand_crisis_scenario(intervention_type="clarification"))

    assert result.ethics_check.allowed is True
    assert result.final_metrics.trust_recovery_proxy > 0


def test_bounded_confidence_gate_affects_updates() -> None:
    low_confidence = _two_agent_confidence_scenario(confidence_radius=0.2)
    high_confidence = _two_agent_confidence_scenario(confidence_radius=2.0)

    low_result = run_simulation(low_confidence)
    high_result = run_simulation(high_confidence)

    assert low_result.final_metrics.polarization_index > high_result.final_metrics.polarization_index


def test_friedkin_johnsen_prior_persistence_limits_movement() -> None:
    low_stubbornness = _single_agent_message_scenario(stubbornness=0.0)
    high_stubbornness = _single_agent_message_scenario(stubbornness=1.0)

    low_result = run_simulation(low_stubbornness)
    high_result = run_simulation(high_stubbornness)

    assert low_result.final_metrics.average_latent_opinion > high_result.final_metrics.average_latent_opinion
    assert abs(high_result.final_metrics.average_latent_opinion - (-0.8)) < abs(
        low_result.final_metrics.average_latent_opinion - (-0.8)
    )


def test_source_credibility_affects_message_impact() -> None:
    low_credibility = _single_agent_message_scenario(source_credibility=0.1)
    high_credibility = _single_agent_message_scenario(source_credibility=0.95)

    assert run_simulation(high_credibility).final_metrics.average_latent_opinion > run_simulation(
        low_credibility
    ).final_metrics.average_latent_opinion


def test_framing_affects_message_impact() -> None:
    low_impact_frame = _single_agent_message_scenario(framing="faq")
    high_impact_frame = _single_agent_message_scenario(framing="third_party_evidence")

    assert run_simulation(high_impact_frame).final_metrics.average_latent_opinion > run_simulation(
        low_impact_frame
    ).final_metrics.average_latent_opinion


def test_threshold_based_expression_update_affects_public_expression() -> None:
    low_threshold = _single_agent_message_scenario(action_threshold=0.05, latent=-0.1, expressed=0.0, prior=-0.1)
    high_threshold = _single_agent_message_scenario(action_threshold=0.95, latent=-0.1, expressed=0.0, prior=-0.1)

    assert run_simulation(low_threshold).final_metrics.average_expressed_opinion > run_simulation(
        high_threshold
    ).final_metrics.average_expressed_opinion


def test_attention_decay_works() -> None:
    scenario = create_brand_crisis_scenario(intervention_type="no_response", steps=4)
    result = run_simulation(scenario)

    assert result.final_metrics.attention_level < result.initial_metrics.attention_level


def test_fatigue_increases_safely_during_update() -> None:
    agent = _test_agent("fatigue_agent", -0.2, 1.0).model_copy(
        update={"attention_budget": 1.0, "fatigue": 0.0}
    )
    updated = update_agents_for_step(
        [agent],
        [],
        [_positive_message(source_credibility=1.0, framing="third_party_evidence")],
        SimulationConfig(
            steps=1,
            peer_influence_weight=0.0,
            message_influence_weight=0.8,
            prior_persistence_weight=0.0,
            attention_decay=0.1,
            fatigue_increase=0.2,
        ),
    )[0]

    assert updated.fatigue > agent.fatigue
    assert 0 <= updated.fatigue <= 1
    assert 0 <= updated.attention_budget <= 1


def test_simulation_does_not_use_real_api_or_llm_calls() -> None:
    result = run_simulation(create_default_echo_chamber_scenario())

    assert result.safe_mode["real_api_calls"] is False
    assert result.safe_mode["real_llm_calls"] is False
    assert result.safe_mode["live_fetch_enabled"] is False
    assert result.safe_mode["individual_targeting"] is False


def test_simulation_run_output_remains_aggregate_level() -> None:
    result_text = run_simulation(create_default_echo_chamber_scenario()).model_dump_json()

    assert '"agent_id"' not in result_text
    assert '"agents"' not in result_text
    assert "influenceability_score" not in result_text
    assert "target_accounts" not in result_text
    assert "bot_script" not in result_text


def test_simulation_api_routes_work() -> None:
    scenario = client.get("/api/v1/simulation/demo-scenario")
    assert scenario.status_code == 200

    run_response = client.post("/api/v1/simulation/run", json=scenario.json())
    assert run_response.status_code == 200
    body = run_response.json()
    assert body["simulation_status"] == "completed"
    assert body["final_metrics"]["negative_ratio"] >= 0

    policy_response = client.get("/api/v1/simulation/ethics-policy")
    assert policy_response.status_code == 200
    assert "fake_consensus" in policy_response.json()["forbidden_intervention_types"]


def test_simulation_api_rejects_forbidden_intervention() -> None:
    scenario = create_brand_crisis_scenario(intervention_type="fake_consensus").model_dump(mode="json")

    response = client.post("/api/v1/simulation/run", json=scenario)

    assert response.status_code == 400
    body = response.json()["detail"]
    assert body["error"] == "simulation_intervention_rejected"
    assert "fake_consensus" in body["blocked_categories"]


def test_high_reach_negative_video_scenario_builds() -> None:
    scenario = create_high_reach_negative_video_scenario()

    assert scenario.topic == "high_reach_negative_video"
    assert scenario.interventions[0].intervention_type == "content_removal_with_explanation"
    assert scenario.interventions[0].visibility_intervention is not None
    assert scenario.metadata["human_review_required"] is True


def test_high_reach_negative_video_scenario_contains_required_aggregate_groups() -> None:
    scenario = create_high_reach_negative_video_scenario()

    groups = {agent.community_id for agent in scenario.agents}

    assert {
        "neutral_audience",
        "hard_opposition",
        "authority_trusting",
        "bridge_nodes",
    }.issubset(groups)


def test_visibility_intervention_types_are_registered() -> None:
    assert set(VISIBILITY_INTERVENTION_TYPES) == {
        "content_removal",
        "comment_closure",
        "account_restriction",
        "visibility_reduction",
        "platform_labeling",
        "policy_enforcement_notice",
        "content_removal_with_explanation",
    }


def test_content_removal_reduces_exposure() -> None:
    result = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation")
    )

    assert result is not None
    assert result.exposure_reduction >= 55
    assert result.aggregate_level_only is True
    assert result.human_review_required is True


def test_high_target_reach_increases_exposure_reduction() -> None:
    low_reach = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", target_message_reach=0.2)
    )
    high_reach = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", target_message_reach=0.95)
    )

    assert low_reach is not None
    assert high_reach is not None
    assert high_reach.exposure_reduction > low_reach.exposure_reduction


def test_low_legitimacy_increases_backlash() -> None:
    safer = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation")
    )
    low_legitimacy = calculate_visibility_intervention_result(
        _visibility_intervention(
            "content_removal_with_explanation",
            policy_violation_clarity=0.18,
            legitimacy_of_removal=0.2,
            public_explanation_quality=0.18,
        )
    )

    assert safer is not None
    assert low_legitimacy is not None
    assert low_legitimacy.backlash_cost > safer.backlash_cost
    assert low_legitimacy.trust_loss > safer.trust_loss
    assert low_legitimacy.recommendation == "prefer_labeling_or_clarification"


def test_transparent_explanation_reduces_backlash() -> None:
    unexplained = calculate_visibility_intervention_result(_visibility_intervention("content_removal"))
    explained = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation")
    )

    assert unexplained is not None
    assert explained is not None
    assert explained.backlash_cost < unexplained.backlash_cost
    assert explained.trust_loss < unexplained.trust_loss


def test_high_screenshot_probability_increases_spillover() -> None:
    low = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", screenshot_probability=0.05)
    )
    high = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", screenshot_probability=0.92)
    )

    assert low is not None
    assert high is not None
    assert high.spillover_risk > low.spillover_risk


def test_high_reactance_amplification_increases_opposition_impact() -> None:
    low = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", reactance_amplification=0.05)
    )
    high = calculate_visibility_intervention_result(
        _visibility_intervention("content_removal_with_explanation", reactance_amplification=0.92)
    )

    assert low is not None
    assert high is not None
    assert high.opposition_group_impact > low.opposition_group_impact


def test_neutral_audience_impact_is_high_concern() -> None:
    result = calculate_visibility_intervention_result(
        _visibility_intervention(
            "content_removal_with_explanation",
            neutral_audience_negative_shift=0.68,
            hard_opposition_negative_shift=0.05,
        )
    )

    assert result is not None
    assert result.audience_impact.high_concern is True
    assert result.neutral_audience_impact > result.opposition_group_impact


def test_hard_opposition_only_backlash_is_lower_concern() -> None:
    neutral_shift = calculate_visibility_intervention_result(
        _visibility_intervention(
            "content_removal_with_explanation",
            neutral_audience_negative_shift=0.56,
            hard_opposition_negative_shift=0.05,
        )
    )
    opposition_shift = calculate_visibility_intervention_result(
        _visibility_intervention(
            "content_removal_with_explanation",
            neutral_audience_negative_shift=0.04,
            hard_opposition_negative_shift=0.56,
        )
    )

    assert neutral_shift is not None
    assert opposition_shift is not None
    assert neutral_shift.trust_loss > opposition_shift.trust_loss
    assert neutral_shift.net_risk_change > opposition_shift.net_risk_change


def test_visibility_scores_are_clamped_to_zero_one_hundred() -> None:
    result = calculate_visibility_intervention_result(
        _visibility_intervention(
            "content_removal",
            target_message_reach=1.0,
            current_visibility=1.0,
            removal_time=0.0,
            residual_copies=0.0,
            screenshot_probability=1.0,
            repost_migration_probability=1.0,
            perceived_suppression=1.0,
            policy_violation_clarity=0.0,
            legitimacy_of_removal=0.0,
            public_explanation_quality=0.0,
            reactance_amplification=1.0,
            martyr_effect=1.0,
            cross_platform_spillover=1.0,
            neutral_audience_negative_shift=1.0,
            hard_opposition_negative_shift=1.0,
        )
    )

    assert result is not None
    for field_name in (
        "exposure_reduction",
        "backlash_cost",
        "trust_loss",
        "spillover_risk",
        "net_risk_change",
        "removal_legitimacy_score",
        "public_explanation_quality_score",
        "neutral_audience_impact",
        "opposition_group_impact",
    ):
        value = getattr(result, field_name)
        assert 0 <= value <= 100
    assert 0 <= result.audience_impact.neutral_audience_impact <= 100
    assert 0 <= result.audience_impact.opposition_group_impact <= 100


def test_forbidden_covert_suppression_rejected() -> None:
    scenario = create_high_reach_negative_video_scenario(intervention_type="covert_censorship")

    with pytest.raises(SimulationEthicsError) as exc:
        run_simulation(scenario)

    assert "covert_censorship" in exc.value.blocked_categories


def test_visibility_simulation_output_is_deterministic_and_aggregate_only() -> None:
    scenario = create_high_reach_negative_video_scenario()

    first = run_simulation(scenario).model_dump(mode="json")
    second = run_simulation(scenario).model_dump(mode="json")

    assert first == second
    assert first["visibility_intervention_result"]["exposure_reduction"] >= 55
    assert '"agent_id"' not in run_simulation(scenario).model_dump_json()
    assert "target_accounts" not in run_simulation(scenario).model_dump_json()


def test_ab_style_visibility_comparison_runs_with_two_aggregate_results() -> None:
    baseline = run_simulation(create_high_reach_negative_video_scenario(intervention_type="no_response"))
    visibility = run_simulation(create_high_reach_negative_video_scenario())

    assert baseline.visibility_intervention_result is None
    assert visibility.visibility_intervention_result is not None
    assert visibility.visibility_intervention_result.exposure_reduction > 0
    assert visibility.safe_mode["aggregate_level_only"] is True


def test_simulation_api_accepts_visibility_intervention_payload() -> None:
    scenario = create_high_reach_negative_video_scenario().model_dump(mode="json")

    response = client.post("/api/v1/simulation/run", json=scenario)

    assert response.status_code == 200
    body = response.json()
    visibility = body["visibility_intervention_result"]
    assert visibility["intervention_type"] == "content_removal_with_explanation"
    assert visibility["human_review_required"] is True
    assert visibility["aggregate_level_only"] is True
    assert body["safe_mode"]["aggregate_level_only"] is True
    assert "target_accounts" not in response.text
    assert "influenceability_score" not in response.text


def test_simulation_lab_offline_benchmark_suite_passes() -> None:
    result = _run_simulation_lab_benchmark(Path("benchmarks"))

    assert result["suite"] == "simulation_lab"
    assert result["status"] == "pass"
    assert result["case_count"] >= 8


def _two_agent_confidence_scenario(confidence_radius: float) -> SimulationScenario:
    agents = [
        _test_agent("agent_negative", -0.8, confidence_radius),
        _test_agent("agent_positive", 0.8, confidence_radius),
    ]
    return SimulationScenario(
        scenario_id=f"bounded_confidence_{confidence_radius}",
        name="Bounded confidence test",
        agents=agents,
        network_edges=[
            SimulationNetworkEdge(source_agent_id="agent_negative", target_agent_id="agent_positive", weight=1.0),
            SimulationNetworkEdge(source_agent_id="agent_positive", target_agent_id="agent_negative", weight=1.0),
        ],
        messages=[],
        interventions=[],
        config=SimulationConfig(
            steps=3,
            peer_influence_weight=0.8,
            message_influence_weight=0.0,
            prior_persistence_weight=0.0,
            attention_decay=0.0,
            fatigue_increase=0.0,
        ),
    )


def _single_agent_message_scenario(
    *,
    stubbornness: float = 0.1,
    source_credibility: float = 0.9,
    framing: str = "neutral",
    action_threshold: float = 0.1,
    latent: float = -0.8,
    expressed: float = -0.8,
    prior: float = -0.8,
) -> SimulationScenario:
    return SimulationScenario(
        scenario_id=f"single_agent_{stubbornness}_{source_credibility}_{framing}_{action_threshold}",
        name="Single agent message test",
        agents=[
            _test_agent("single_agent", latent, 1.0).model_copy(
                update={
                    "latent_opinion": latent,
                    "expressed_opinion": expressed,
                    "prior_anchor": prior,
                    "stubbornness": stubbornness,
                    "action_threshold": action_threshold,
                    "authority_trust": 1.0,
                    "confirmation_bias": 0.0,
                    "reactance": 0.0,
                    "attention_budget": 1.0,
                }
            )
        ],
        network_edges=[],
        messages=[_positive_message(source_credibility=source_credibility, framing=framing)],
        interventions=[],
        config=SimulationConfig(
            steps=1,
            peer_influence_weight=0.0,
            message_influence_weight=0.8,
            prior_persistence_weight=0.8,
            attention_decay=0.0,
            fatigue_increase=0.0,
        ),
    )


def _positive_message(source_credibility: float, framing: str) -> SimulationMessage:
    return SimulationMessage(
        message_id=f"positive_{source_credibility}_{framing}",
        topic="synthetic_test",
        source_type="third_party",
        source_credibility=source_credibility,
        stance_direction=0.9,
        emotional_intensity=0.5,
        evidence_strength=0.85,
        framing=framing,
        novelty=0.8,
        repetition=0.0,
        platform_reach=0.8,
    )


def _test_agent(agent_id: str, opinion: float, confidence_radius: float) -> SimulationAgent:
    return SimulationAgent(
        agent_id=agent_id,
        community_id="test_community",
        latent_opinion=opinion,
        expressed_opinion=opinion,
        prior_anchor=opinion,
        stubbornness=0.1,
        confidence_radius=confidence_radius,
        action_threshold=0.1,
        confirmation_bias=0.1,
        negativity_weight=1.0,
        reactance=0.1,
        authority_trust=0.5,
        conformity=1.0,
        attention_budget=0.5,
        fatigue=0.0,
        identity_group="synthetic_test",
        status="active",
    )


def _visibility_intervention(intervention_type: str, **overrides: float) -> SimulationIntervention:
    return SimulationIntervention(
        intervention_id=f"visibility_{intervention_type}",
        intervention_type=intervention_type,
        topic="visibility_test",
        message="Synthetic visibility intervention for aggregate human-review simulation.",
        intensity=0.72,
        visibility_intervention=VisibilityIntervention(intervention_type=intervention_type, **overrides),
    )
