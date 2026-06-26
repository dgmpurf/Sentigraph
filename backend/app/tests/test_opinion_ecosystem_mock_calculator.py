from __future__ import annotations

import inspect

from app.services import opinion_ecosystem_mock_calculator as calculator


REQUIRED_BOUNDARY_FLAGS = [
    "not_full_web",
    "not_full_platform",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_personality_diagnosis",
    "not_individual_persuasion_scoring",
    "not_public_opinion_control",
    "not_auto_executed",
    "selected_sample_only",
    "evidence_not_truth",
    "human_review_required",
]

FORBIDDEN_SCORE_KEYS = [
    "sample_heat_score",
    "sample_controversy_score",
    "discussion_risk_score",
    "factual_credibility",
    "pull_score",
    "saturation_score",
    "strategy_score",
    "persuasion_score",
    "prediction_probability",
    "real_hotlist_score",
    "truth_score",
    "official_verified",
    "causal_chain_confirmed",
    "target_user_list",
    "raw_author_identifiers",
    "raw_author_id",
    "author_name",
    "profile_url",
]


def _minimal_fixture() -> dict:
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": "fixture_8p1_minimal",
            "case_id": "case_8p1",
            "sample_id": "sample_8p1",
            "fixture_role": "unit_test_synthetic",
            "source_mode": "synthetic_fixture",
            "stage_id": "T0",
            "coverage_note": "selected synthetic fixture only",
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": [],
        "content_aggregates": [],
        "influence_cores": [],
        "people_clusters": [],
        "echo_boxes": [],
        "response_strategy_candidates": [],
    }


def _content_aggregate_fixture() -> dict:
    fixture = _minimal_fixture()
    fixture["fixture_metadata"]["fixture_id"] = "fixture_8p2_content"
    fixture["content_aggregates"] = [
        {
            "aggregate_id": "agg_001",
            "volume_score": 0.40,
            "interaction_score": 0.30,
            "growth_score": 0.20,
            "emotion_intensity": 0.50,
            "spread_score": 0.25,
            "issue_sensitivity": 0.40,
            "response_gap": 0.30,
        }
    ]
    fixture["evidence_items_safe"] = [
        {
            "evidence_id": "evidence_001",
            "platform": "sample_forum",
            "provenance_type": "official_api_public",
            "verification_status": "verified_by_official_api",
            "trust_label": "high",
            "review_status": "approved",
            "duplicate_group_id": "dup_001",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "support",
            "emotion_intensity_hint": 0.40,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
        },
        {
            "evidence_id": "evidence_002",
            "platform": "sample_forum",
            "provenance_type": "manual_url_with_attestation",
            "trust_label": "medium",
            "review_status": "approved",
            "duplicate_group_id": "dup_002",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 0.50,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
        },
    ]
    return fixture


def _influencecore_fixture(core: dict | None = None, evidence_items: list[dict] | None = None) -> dict:
    fixture = _content_aggregate_fixture()
    fixture["fixture_metadata"]["fixture_id"] = "fixture_8p3_influencecore"
    fixture["influence_cores"] = [
        core
        or {
            "core_id": "core_official_001",
            "core_type": "official_statement",
            "associated_evidence_ids": ["evidence_001"],
            "clarity_hint": 0.86,
            "novelty_hint": 0.20,
            "bridge_hint": 0.62,
            "backlash_hint": 0.12,
            "emotional_charge_hint": 0.20,
            "repetition_hint": 0.10,
            "resolution_signal_hint": 0.78,
            "source_transparency_hint": 0.94,
            "cross_source_consistency_hint": 0.85,
            "privacy_safety_pass": True,
            "identity_or_group_relevance_hint": 0.45,
            "meme_or_symbolic_density_hint": 0.05,
            "neutral_or_explanatory_frame_hint": 0.80,
            "source_credibility_across_camps_hint": 0.72,
            "low_identity_threat_language_hint": 0.88,
            "shared_value_language_hint": 0.60,
            "media_or_third_party_relay_hint": 0.20,
            "empathy_or_context_hint": 0.72,
        }
    ]
    if evidence_items is not None:
        fixture["evidence_items_safe"] = evidence_items
    else:
        for evidence in fixture["evidence_items_safe"]:
            evidence["influence_core_refs"] = ["core_official_001"]
    return fixture


def _echobox_fixture(echo_box: dict | None = None, evidence_items: list[dict] | None = None) -> dict:
    fixture = _influencecore_fixture(evidence_items=evidence_items)
    fixture["fixture_metadata"]["fixture_id"] = "fixture_8p4_echobox"
    fixture["echo_boxes"] = [
        echo_box
        or {
            "echo_box_id": "echo_001",
            "echo_box_role": "mixed_discussion_box",
            "echo_type": "mixed_discussion_box",
            "platform_refs": ["sample_forum"],
            "aggregate_ids": ["agg_001"],
            "influence_core_ids": ["core_official_001"],
            "stance_distribution": {"support": 0.40, "oppose": 0.35, "neutral": 0.15, "mixed": 0.10},
            "interaction_proxy_summary": {"internal_density": 0.45},
            "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.40},
            "cross_box_exposure_hint": 0.35,
            "bridge_cluster_share_hint": 0.42,
            "low_identity_threat_language_hint": 0.72,
            "media_or_third_party_relay_hint": 0.20,
            "novelty_constructive_hint": 0.22,
            "repetition_hint": 0.20,
        }
    ]
    for evidence in fixture["evidence_items_safe"]:
            evidence["echo_box_refs"] = ["echo_001"]
    return fixture


def _peoplecluster_fixture(cluster: dict | None = None, evidence_items: list[dict] | None = None) -> dict:
    fixture = _echobox_fixture(evidence_items=evidence_items)
    fixture["fixture_metadata"]["fixture_id"] = "fixture_8p5_peoplecluster"
    fixture["people_clusters"] = [
        cluster
        or {
            "cluster_id": "cluster_mixed_001",
            "cluster_role": "mixed_bridge",
            "cluster_type": "mixed_bridge",
            "sample_share_hint": 0.42,
            "stance_distribution": {"support": 0.36, "oppose": 0.30, "neutral": 0.22, "mixed": 0.12},
            "stance_confidence_hint": 0.58,
            "attention_hint": 0.46,
            "fatigue_hint": 0.30,
            "expression_hint": 0.44,
            "openness_hint": 0.66,
            "confidence_radius_hint": 0.64,
            "aggregate_ids": ["agg_001"],
            "influence_core_ids": ["core_official_001"],
            "echo_box_ids": ["echo_001"],
            "previous_state": {"stance_score": 0.05, "attention_level": 0.40, "fatigue_level": 0.22},
            "novelty_signal_hint": 0.30,
            "personal_relevance_proxy_hint": 0.35,
            "reactivation_trigger_hint": 0.22,
            "resolution_signal_hint": 0.42,
            "unresolved_grievance_hint": 0.28,
            "constructive_new_info_hint": 0.50,
            "bridge_understanding_hint": 0.46,
            "social_norm_pressure_hint": 0.34,
            "action_threshold_hint": 0.52,
            "reputation_memory_hint": 0.38,
            "new_trigger_hint": 0.24,
            "identity_relevance_proxy_hint": 0.30,
        }
    ]
    for evidence in fixture["evidence_items_safe"]:
        evidence["people_cluster_refs"] = ["cluster_mixed_001"]
    return fixture


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def _walk_values(value: object) -> list[object]:
    values: list[object] = []
    if isinstance(value, dict):
        for child in value.values():
            values.extend(_walk_values(child))
    elif isinstance(value, list):
        for child in value:
            values.extend(_walk_values(child))
    else:
        values.append(value)
    return values


def test_minimal_safe_fixture_returns_metadata_only() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_minimal_fixture())

    assert run["schema"] == "sentigraph_opinion_ecosystem_mock_calculator_run_v0_1"
    assert run["fixture_id"] == "fixture_8p1_minimal"
    assert run["case_id"] == "case_8p1"
    assert run["sample_id"] == "sample_8p1"
    assert run["model_name"] == "sentigraph_opinion_ecosystem_weight_model"
    assert run["model_version"] == "0.1"
    assert run["model_status"] == "8P_1_metadata_skeleton"
    assert run["coefficient_source"] == "mock_default"
    assert run["calibration_status"] == "uncalibrated"
    assert run["empirical_validation"] == "not_started"
    assert run["generated_at"] == "not_runtime_generated_in_8P_1"
    assert run["scope_note"] == "selected_sample_or_local_fixture_only"
    assert run["human_review_required"] is True
    assert run["validation_summary"]["status"] == "metadata_ready"

    assert not (set(FORBIDDEN_SCORE_KEYS) & _walk_keys(run))
    assert set(run["module_outputs"].values()) == {"not_calculated_in_8P_1"}


def test_boundary_flags_are_always_present() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_minimal_fixture())

    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert run["boundary_flags"][flag] is True

    assert run["runtime_side_effects"]
    for flag_value in run["runtime_side_effects"].values():
        assert flag_value is False


def test_forbidden_identity_fields_block_fixture() -> None:
    fixture = _minimal_fixture()
    fixture["evidence_items_safe"] = [
        {
            "evidence_id": "safe_001",
            "nested": {
                "raw_author_id": "hidden",
                "author_name": "hidden",
                "profile_url": "hidden",
            },
        }
    ]

    validation = calculator.validate_mock_fixture_contract(fixture)

    assert validation["status"] == "blocked"
    forbidden_keys = {blocker["field"] for blocker in validation["forbidden_fields"]}
    assert {"raw_author_id", "author_name", "profile_url"} <= forbidden_keys
    assert any("evidence_items_safe[0].nested.raw_author_id" == blocker["path"] for blocker in validation["blockers"])


def test_forbidden_secret_fields_block_fixture() -> None:
    fixture = _minimal_fixture()
    fixture["evidence_items_safe"] = [
        {
            "cookie": "hidden",
            "token": "hidden",
            "session": "hidden",
            "browser_profile": "hidden",
            "profile_path": "hidden",
            "localStorage": "hidden",
            "secret": "hidden",
        }
    ]

    validation = calculator.validate_mock_fixture_contract(fixture)

    assert validation["status"] == "blocked"
    forbidden_keys = {blocker["field"] for blocker in validation["forbidden_fields"]}
    assert {"cookie", "token", "session", "browser_profile", "profile_path", "localStorage", "secret"} <= forbidden_keys


def test_auto_execute_blocks_fixture() -> None:
    fixture = _minimal_fixture()
    fixture["response_strategy_candidates"] = [
        {
            "strategy_id": "strategy_001",
            "response_strategy": "auto_execute",
            "recommendation_level": "auto_execute",
        }
    ]

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert run["validation_summary"]["response_strategy_blocker_count"] >= 1
    assert run["runtime_side_effects"]["auto_execute"] is False
    assert "auto_execute" not in run


def test_overclaim_flags_block_fixture() -> None:
    fixture = _minimal_fixture()
    fixture["fixture_metadata"].update(
        {
            "full_web_claim": True,
            "official_verification_claim": True,
            "causal_proof_claim": True,
            "prediction_claim": True,
        }
    )

    validation = calculator.validate_mock_fixture_contract(fixture)

    assert validation["status"] == "blocked"
    fields = {blocker["field"] for blocker in validation["overclaim_blockers"]}
    assert {"full_web_claim", "official_verification_claim", "causal_proof_claim", "prediction_claim"} <= fields


def test_future_unknown_platform_manual_review() -> None:
    fixture = _minimal_fixture()
    fixture["evidence_items_safe"] = [{"evidence_id": "safe_002", "platform": "future_forum"}]

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert run["validation_summary"]["unknown_platform_warning_count"] == 1
    assert run["human_review_required"] is True
    assert run["runtime_side_effects"]["real_api_calls"] is False
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_no_module_scores_are_calculated_in_first_slice() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_minimal_fixture())

    keys = _walk_keys(run)
    assert not (set(FORBIDDEN_SCORE_KEYS) & keys)
    assert run["module_outputs"] == {
        "content_aggregate": "not_calculated_in_8P_1",
        "influence_core": "not_calculated_in_8P_1",
        "echo_box": "not_calculated_in_8P_1",
        "people_cluster": "not_calculated_in_8P_1",
        "response_strategy": "not_calculated_in_8P_1",
    }


def test_deterministic_same_fixture_same_output() -> None:
    fixture = _minimal_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second
    assert first["run_id"] == "mock_run_fixture_8p1_minimal"
    assert first["generated_at"] == "not_runtime_generated_in_8P_1"


def test_validate_output_boundary_flags_catches_missing_flags() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_minimal_fixture())
    del run["boundary_flags"]["not_full_web"]

    validation = calculator.validate_output_boundary_flags(run)

    assert validation["status"] == "blocked"
    assert any(blocker["field"] == "not_full_web" for blocker in validation["blockers"])


def test_no_real_io_or_runtime_side_effects_by_design() -> None:
    source = inspect.getsource(calculator)
    forbidden_tokens = [
        "op" + "en(",
        "read" + "_text",
        "write" + "_text",
        "requ" + "ests",
        "ht" + "tpx",
        "url" + "lib",
        "sub" + "process",
        "sock" + "et",
        "evidence" + "_items.jsonl",
        "evidence" + "_items.csv",
    ]

    for token in forbidden_tokens:
        assert token not in source


def _content_output(run: dict, index: int = 0) -> dict:
    outputs = run["module_outputs"]["content_aggregate"]
    assert isinstance(outputs, list)
    return outputs[index]


def test_content_aggregate_minimal_fixture_calculates_weight_v0_1() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture())
    content = _content_output(run)

    assert content["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert content["aggregate_id"] == "agg_001"
    assert content["model_status"] == "8P_2_content_aggregate_formula"
    assert content["coefficient_source"] == "mock_default"
    assert content["calibration_status"] == "uncalibrated"
    assert content["empirical_validation"] == "not_started"
    assert content["sample_scope"] == "selected_sample_or_local_fixture_only"
    assert content["evidence_mass"]["evidence_count"] == 2
    assert content["evidence_mass"]["analysis_ready_evidence_count"] == 2

    for score in content["scores"].values():
        assert 0 <= score <= 1

    for flag in [
        "not_real_hotlist",
        "not_full_web",
        "not_full_platform",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "evidence_not_truth",
        "human_review_required",
    ]:
        assert content["boundary_flags"][flag] is True

    assert run["module_outputs"]["influence_core"] == "not_calculated_in_8P_2"
    assert run["module_outputs"]["echo_box"] == "not_calculated_in_8P_2"
    assert run["module_outputs"]["people_cluster"] == "not_calculated_in_8P_2"
    assert run["module_outputs"]["response_strategy"] == "not_calculated_in_8P_2"


def test_rejected_evidence_excluded_from_content_aggregate_scores() -> None:
    base_run = calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture())
    fixture = _content_aggregate_fixture()
    fixture["evidence_items_safe"].append(
        {
            "evidence_id": "rejected_high_emotion",
            "platform": "sample_forum",
            "provenance_type": "official_api_public",
            "trust_label": "high",
            "review_status": "rejected",
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 1.0,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
        }
    )

    rejected_run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    base_content = _content_output(base_run)
    rejected_content = _content_output(rejected_run)

    assert rejected_content["scores"]["sample_heat_score"] == base_content["scores"]["sample_heat_score"]
    assert rejected_content["scores"]["overall_risk_score"] == base_content["scores"]["overall_risk_score"]
    assert rejected_content["evidence_mass"]["rejected_excluded_count"] == 1
    assert rejected_content["warnings"]["rejected_excluded_warnings"]


def test_duplicate_evidence_folded_not_linear_amplification() -> None:
    fixture = _content_aggregate_fixture()
    fixture["evidence_items_safe"][0]["duplicate_group_id"] = "dup_large"
    fixture["evidence_items_safe"][0]["duplicate_count"] = 16

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    content = _content_output(run)

    assert content["components"]["repetition_signal"] < 1
    assert content["scores"]["sample_heat_score"] < 1
    assert content["warnings"]["duplicate_folded_warnings"]
    assert content["evidence_mass"]["duplicate_group_count"] == 2


def test_low_trust_emotional_screenshot_lowers_confidence_and_raises_review_risk() -> None:
    high_trust_fixture = _content_aggregate_fixture()
    screenshot_fixture = _content_aggregate_fixture()
    screenshot_fixture["evidence_items_safe"] = [
        {
            "evidence_id": "screenshot_001",
            "platform": "sample_forum",
            "provenance_type": "screenshot_transcription",
            "trust_label": "low",
            "review_status": "review_needed",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 1.0,
            "source_url_present": False,
            "aggregate_ref": "agg_001",
        }
    ]

    high_content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(high_trust_fixture))
    screenshot_content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(screenshot_fixture))

    assert screenshot_content["scores"]["evidence_confidence_score"] < high_content["scores"]["evidence_confidence_score"]
    assert screenshot_content["scores"]["review_risk_score"] > high_content["scores"]["review_risk_score"]
    assert "official_verified" not in _walk_keys(screenshot_content)
    assert "truth_score" not in _walk_keys(screenshot_content)


def test_one_sided_high_heat_does_not_imply_high_controversy() -> None:
    fixture = _content_aggregate_fixture()
    fixture["content_aggregates"][0].update({"volume_score": 0.95, "emotion_intensity": 0.70})
    for evidence in fixture["evidence_items_safe"]:
        evidence["stance_hint"] = "support"

    content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert content["scores"]["sample_heat_score"] > content["scores"]["sample_controversy_score"]
    assert content["components"]["stance_distribution"]["oppose"] == 0


def test_missing_optional_components_renormalize_safely() -> None:
    fixture = _content_aggregate_fixture()
    fixture["content_aggregates"] = [{"aggregate_id": "agg_001"}]

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    content = _content_output(first)

    assert first == second
    assert 0 <= content["scores"]["sample_heat_score"] <= 1
    assert content["warnings"]["missing_component_warnings"]


def test_no_evidence_for_aggregate_yields_insufficient_data_warning() -> None:
    fixture = _content_aggregate_fixture()
    fixture["evidence_items_safe"] = []

    content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert content["warnings"]["insufficient_data_warnings"]
    assert all(score == 0 for score in content["scores"].values())
    assert content["schema"] == "sentigraph_content_aggregate_weight_v0_1"


def test_forbidden_fields_still_block_before_scoring() -> None:
    fixture = _content_aggregate_fixture()
    fixture["evidence_items_safe"][0]["raw_author_id"] = "hidden"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["content_aggregate"], list)


def test_overclaim_fields_still_block_before_scoring() -> None:
    fixture = _content_aggregate_fixture()
    fixture["fixture_metadata"]["full_web_claim"] = True

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["content_aggregate"], list)


def test_auto_execute_still_blocks_before_scoring() -> None:
    fixture = _content_aggregate_fixture()
    fixture["response_strategy_candidates"].append({"recommendation_level": "auto_execute"})

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["content_aggregate"], list)


def test_future_unknown_platform_does_not_imply_provider_runnable() -> None:
    fixture = _content_aggregate_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert run["validation_summary"]["unknown_platform_warning_count"] == 1
    assert not isinstance(run["module_outputs"]["content_aggregate"], list)
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_no_non_contentaggregate_module_scores_in_8P_2() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture())
    keys = _walk_keys(run)

    forbidden_non_content_keys = {
        "factual_credibility",
        "pull_score",
        "saturation_score",
        "stance_delta",
        "strategy_score",
    }

    assert not (forbidden_non_content_keys & keys)


def test_no_forbidden_output_fields_after_content_aggregate_scoring() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture())
    keys = _walk_keys(run)

    forbidden_output_fields = {
        "truth_score",
        "official_verified",
        "causal_chain_confirmed",
        "prediction_probability",
        "persuasion_score",
        "target_user_list",
        "raw_author_identifiers",
    }

    assert not (forbidden_output_fields & keys)


def test_deterministic_same_fixture_same_output_after_scoring() -> None:
    fixture = _content_aggregate_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second


def _influence_output(run: dict, index: int = 0) -> dict:
    outputs = run["module_outputs"]["influence_core"]
    assert isinstance(outputs, list)
    return outputs[index]


def _echo_output(run: dict, index: int = 0) -> dict:
    outputs = run["module_outputs"]["echo_box"]
    assert isinstance(outputs, list)
    return outputs[index]


def _peoplecluster_output(run: dict, index: int = 0) -> dict:
    outputs = run["module_outputs"]["people_cluster"]
    assert isinstance(outputs, list)
    return outputs[index]


def _response_strategy_fixture(candidate: dict | None = None) -> dict:
    fixture = _peoplecluster_fixture()
    fixture["fixture_metadata"]["fixture_id"] = "fixture_8p6_response_strategy"
    fixture["fixture_metadata"]["stage_id"] = "T4"
    fixture["response_strategy_candidates"] = [
        candidate
        or {
            "candidate_id": "strategy_candidate_s4",
            "strategy_id": "S4",
            "strategy_type": "FAQ_or_longform_explanation",
            "stage_id": "T4",
            "claim_intensity": 0.28,
            "stage_fit": 0.82,
            "response_gap_fit": 0.74,
            "heat_fit": 0.70,
            "fatigue_fit": 0.62,
            "strategy_clarity_base": 0.92,
            "strategy_deescalation_base": 0.70,
            "strategy_bridge_base": 0.58,
            "transparency_level": 0.88,
            "accountability_level": 0.78,
            "consistency_with_prior_record": 0.76,
            "resolution_signal": 0.70,
            "low_amplification_level": 0.66,
            "constructive_new_info": 0.82,
            "unresolved_grievance_reduction": 0.62,
            "low_identity_threat_language": 0.78,
            "exposure_level": 0.34,
            "novelty": 0.18,
            "media_relay_probability": 0.20,
            "mismatch_with_cluster_concerns": 0.20,
            "perceived_defensiveness": 0.14,
            "timing_lag": 0.18,
            "low_empathy_language": 0.10,
            "contradiction_with_prior_record": 0.08,
            "identity_threat_risk": 0.12,
            "ambiguity": 0.10,
            "causal_language": 0.0,
            "full_web_claim": 0.0,
            "official_verification_claim": 0.0,
            "prediction_language": 0.0,
            "uncalibrated_score_without_boundary": 0.0,
            "requires_new_runtime": 0.0,
            "requires_real_API_or_LLM": 0.0,
            "requires_unreviewed_data": 0.0,
            "requires_external_actor_coordination": 0.0,
            "requires_legal_review": 0.0,
            "requires_sensitive_material": 0.0,
        }
    ]
    return fixture


def _response_strategy_output(run: dict, index: int = 0) -> dict:
    outputs = run["module_outputs"]["response_strategy"]
    assert isinstance(outputs, list)
    return outputs[index]


def test_influencecore_minimal_fixture_calculates_weight_v0_1() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture())
    influence = _influence_output(run)

    assert influence["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert influence["core_id"] == "core_official_001"
    assert influence["core_type"] == "official_statement"
    assert influence["model_status"] == "8P_3_influencecore_formula"
    assert influence["coefficient_source"] == "mock_default"
    assert influence["calibration_status"] == "uncalibrated"
    assert influence["empirical_validation"] == "not_started"
    assert influence["sample_scope"] == "selected_sample_or_local_fixture_only"
    assert influence["evidence_mass"]["associated_evidence_count"] >= 1

    for score in influence["scores"].values():
        assert 0 <= score <= 1

    for flag in [
        "not_official_verification",
        "not_truth_score",
        "not_causal_proof",
        "not_prediction",
        "not_persuasion_probability",
        "not_people_cluster",
        "not_real_person",
        "evidence_not_truth",
        "human_review_required",
    ]:
        assert influence["boundary_flags"][flag] is True

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert run["module_outputs"]["echo_box"] == "not_calculated_in_8P_3"
    assert run["module_outputs"]["people_cluster"] == "not_calculated_in_8P_3"
    assert run["module_outputs"]["response_strategy"] == "not_calculated_in_8P_3"


def test_official_statement_credible_but_low_exposure() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture())
    influence = _influence_output(run)

    assert influence["scores"]["factual_credibility"] > 0.70
    assert influence["scores"]["sample_exposure"] < 0.40
    assert influence["scores"]["amplification_score"] < influence["scores"]["factual_credibility"]
    assert not any("changed discourse" in line.lower() for line in influence["explanation"])


def test_viral_meme_low_credibility_high_amplification_warning() -> None:
    core = {
        "core_id": "core_meme_001",
        "core_type": "meme_deconstruction",
        "associated_evidence_ids": ["meme_001"],
        "clarity_hint": 0.70,
        "novelty_hint": 0.90,
        "emotional_charge_hint": 0.95,
        "repetition_hint": 0.95,
        "meme_or_symbolic_density_hint": 1.0,
        "bridge_hint": 0.45,
        "backlash_hint": 0.55,
        "privacy_safety_pass": True,
    }
    evidence = [
        {
            "evidence_id": "meme_001",
            "platform": "sample_forum",
            "provenance_type": "screenshot_transcription",
            "trust_label": "low",
            "review_status": "review_needed",
            "duplicate_group_id": "dup_meme",
            "duplicate_count": 18,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "emotion_intensity_hint": 0.95,
            "source_url_present": False,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_meme_001"],
        }
    ]

    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture(core, evidence)))

    assert influence["scores"]["amplification_score"] > 0.55
    assert influence["scores"]["factual_credibility"] < 0.50
    assert "high_attention_low_credibility" in influence["warnings"]["low_confidence_warnings"]
    assert "truth_score" not in _walk_keys(influence)
    assert "official_verified" not in _walk_keys(influence)


def test_low_trust_claim_raises_core_risk_but_not_truth() -> None:
    core = {
        "core_id": "core_claim_001",
        "core_type": "low_trust_claim",
        "associated_evidence_ids": ["claim_001"],
        "clarity_hint": 0.55,
        "novelty_hint": 0.75,
        "emotional_charge_hint": 0.88,
        "repetition_hint": 0.80,
        "low_trust_conflict_hint": 0.95,
        "privacy_or_sensitivity_risk_hint": 0.50,
        "contradiction_risk_hint": 0.70,
        "unresolved_grievance_hint": 0.80,
    }
    evidence = [
        {
            "evidence_id": "claim_001",
            "platform": "sample_forum",
            "provenance_type": "manual_text_without_source",
            "trust_label": "low",
            "review_status": "review_needed",
            "duplicate_count": 8,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "source_url_present": False,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_claim_001"],
        }
    ]

    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture(core, evidence)))

    assert influence["scores"]["core_risk"] > 0.50
    assert influence["scores"]["factual_credibility"] < 0.45
    assert "truth_score" not in _walk_keys(influence)
    assert "official_verified" not in _walk_keys(influence)


def test_third_party_explanation_can_have_bridge_and_deescalation_potential() -> None:
    core = {
        "core_id": "core_context_001",
        "core_type": "third_party_context",
        "associated_evidence_ids": ["context_001"],
        "clarity_hint": 0.90,
        "novelty_hint": 0.35,
        "bridge_hint": 0.88,
        "backlash_hint": 0.08,
        "emotional_charge_hint": 0.20,
        "resolution_signal_hint": 0.90,
        "source_transparency_hint": 0.88,
        "cross_source_consistency_hint": 0.82,
        "privacy_safety_pass": True,
        "neutral_or_explanatory_frame_hint": 0.96,
        "source_credibility_across_camps_hint": 0.84,
        "low_identity_threat_language_hint": 0.95,
        "shared_value_language_hint": 0.78,
        "media_or_third_party_relay_hint": 0.92,
        "empathy_or_context_hint": 0.85,
    }
    evidence = [
        {
            "evidence_id": "context_001",
            "platform": "sample_forum",
            "provenance_type": "manual_url_with_attestation",
            "trust_label": "medium",
            "trust_score": 0.70,
            "review_status": "approved",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "source_url_present": True,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_context_001"],
        }
    ]

    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture(core, evidence)))

    assert influence["scores"]["bridge_potential"] > 0.70
    assert influence["scores"]["deescalation_potential"] > 0.65
    assert not any("guarantee" in line.lower() for line in influence["explanation"])


def test_unknown_core_type_uses_unknown_source_core_warning() -> None:
    core = {
        "core_id": "core_unknown_001",
        "core_type": "future_unknown_core",
        "associated_evidence_ids": ["evidence_001"],
        "clarity_hint": 0.50,
        "novelty_hint": 0.50,
        "privacy_safety_pass": True,
    }

    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture(core)))

    assert influence["core_type"] == "unknown_source_core"
    assert influence["components"]["source_identity_weight"] == 0.25
    assert influence["warnings"]["unknown_core_type_warnings"]


def test_rejected_evidence_excluded_from_influencecore_scores() -> None:
    base = _influencecore_fixture()
    rejected_fixture = _influencecore_fixture()
    rejected_fixture["evidence_items_safe"].append(
        {
            "evidence_id": "rejected_core_001",
            "platform": "sample_forum",
            "provenance_type": "official_api_public",
            "trust_label": "high",
            "review_status": "rejected",
            "duplicate_count": 20,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "emotion_intensity_hint": 1.0,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_official_001"],
        }
    )

    base_influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(base))
    rejected_influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(rejected_fixture))

    assert rejected_influence["scores"]["amplification_score"] == base_influence["scores"]["amplification_score"]
    assert rejected_influence["scores"]["core_risk"] == base_influence["scores"]["core_risk"]
    assert rejected_influence["evidence_mass"]["rejected_excluded_count"] == 1
    assert rejected_influence["warnings"]["rejected_excluded_warnings"]


def test_missing_associated_evidence_yields_insufficient_data_warning() -> None:
    core = {
        "core_id": "core_orphan_001",
        "core_type": "official_statement",
        "associated_evidence_ids": ["missing_evidence"],
        "clarity_hint": 0.95,
    }

    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture(core)))

    assert influence["warnings"]["insufficient_data_warnings"]
    assert influence["evidence_mass"]["analysis_ready_evidence_count"] == 0
    assert all(score <= 0.30 for score in influence["scores"].values())
    assert influence["schema"] == "sentigraph_influence_core_weight_v0_1"


def test_forbidden_fields_still_block_before_influencecore_scoring() -> None:
    fixture = _influencecore_fixture()
    fixture["evidence_items_safe"][0]["profile_url"] = "hidden"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["influence_core"], list)


def test_overclaim_fields_still_block_before_influencecore_scoring() -> None:
    fixture = _influencecore_fixture()
    fixture["fixture_metadata"]["official_verification_claim"] = True

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["influence_core"], list)


def test_auto_execute_still_blocks_before_influencecore_scoring() -> None:
    fixture = _influencecore_fixture()
    fixture["response_strategy_candidates"].append({"recommendation_level": "auto_execute"})

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["influence_core"], list)


def test_future_unknown_platform_does_not_imply_provider_runnable_for_influencecore() -> None:
    fixture = _influencecore_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert run["validation_summary"]["unknown_platform_warning_count"] == 1
    assert not isinstance(run["module_outputs"]["influence_core"], list)
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_no_echobox_peoplecluster_response_strategy_scores_in_8P_3() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture())
    keys = _walk_keys(run)

    forbidden_non_influence_keys = {
        "saturation_score",
        "stance_delta",
        "strategy_score",
        "persuasion_score",
    }

    assert not (forbidden_non_influence_keys & keys)
    assert run["module_outputs"]["echo_box"] == "not_calculated_in_8P_3"
    assert run["module_outputs"]["people_cluster"] == "not_calculated_in_8P_3"
    assert run["module_outputs"]["response_strategy"] == "not_calculated_in_8P_3"


def test_no_peoplecluster_pull_or_stance_effect_in_8P_3() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {
        "pull_ik",
        "stance_effect_ik",
        "stance_effect_ik_adjusted",
        "InfluenceCoreToClusterEffectV01",
    }

    assert not (forbidden_keys & keys)


def test_no_forbidden_output_fields_after_influencecore_scoring() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture())
    keys = _walk_keys(run)

    forbidden_output_fields = {
        "truth_score",
        "official_verified",
        "causal_chain_confirmed",
        "prediction_probability",
        "persuasion_score",
        "target_user_list",
        "raw_author_identifiers",
    }

    assert not (forbidden_output_fields & keys)


def test_deterministic_same_fixture_same_output_after_influencecore_scoring() -> None:
    fixture = _influencecore_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second


def test_echobox_minimal_fixture_calculates_weight_v0_1() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())
    echo = _echo_output(run)

    assert echo["schema"] == "sentigraph_echobox_weight_v0_1"
    assert echo["echo_box_id"] == "echo_001"
    assert echo["echo_box_role"] == "mixed_discussion_box"
    assert echo["model_status"] == "8P_4_echobox_formula"
    assert echo["coefficient_source"] == "mock_default"
    assert echo["calibration_status"] == "uncalibrated"
    assert echo["empirical_validation"] == "not_started"
    assert echo["sample_scope"] == "selected_sample_or_local_fixture_only"
    assert echo["evidence_mass"]["analysis_ready_evidence_count"] == 2
    assert echo["evidence_mass"]["associated_aggregate_count"] == 1
    assert echo["evidence_mass"]["associated_influence_core_count"] == 1

    for score in echo["scores"].values():
        assert 0 <= score <= 1

    for flag in [
        "not_real_community_map",
        "not_full_graph",
        "not_full_platform",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_individual_tracking",
        "not_target_user_list",
        "evidence_not_truth",
        "human_review_required",
    ]:
        assert echo["boundary_flags"][flag] is True

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert isinstance(run["module_outputs"]["influence_core"], list)
    assert run["module_outputs"]["people_cluster"] == "not_calculated_in_8P_4"
    assert run["module_outputs"]["response_strategy"] == "not_calculated_in_8P_4"


def test_strong_echo_no_breakout_high_closure_low_breakout() -> None:
    echo_box = {
        "echo_box_id": "echo_sealed_001",
        "echo_box_role": "sealed_echo_box",
        "platform_refs": ["sample_forum"],
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_official_001"],
        "stance_distribution": {"support": 0.92, "neutral": 0.04, "oppose": 0.02, "mixed": 0.02},
        "interaction_proxy_summary": {"internal_density": 0.92},
        "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.04},
        "cross_box_exposure_hint": 0.03,
        "bridge_cluster_share_hint": 0.05,
        "bridge_capacity_hint": 0.05,
        "low_identity_threat_language_hint": 0.20,
        "media_or_third_party_relay_hint": 0.05,
        "novelty_constructive_hint": 0.05,
        "repetition_hint": 0.88,
        "core_dominance_hint": 0.84,
    }

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture(echo_box)))

    assert echo["scores"]["saturation_score"] > 0.70
    assert echo["scores"]["closure_score"] > 0.75
    assert echo["scores"]["constructive_breakout_score"] < echo["scores"]["closure_score"]
    assert "causal_chain_confirmed" not in _walk_keys(echo)
    assert "prediction_probability" not in _walk_keys(echo)


def test_bridgeable_controversy_has_bridge_capacity() -> None:
    echo_box = {
        "echo_box_id": "echo_bridge_001",
        "echo_box_role": "bridge_ready_box",
        "platform_refs": ["sample_forum"],
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_official_001"],
        "stance_distribution": {"support": 0.45, "oppose": 0.42, "neutral": 0.08, "mixed": 0.05},
        "interaction_proxy_summary": {"internal_density": 0.55},
        "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.78},
        "cross_box_exposure_hint": 0.70,
        "bridge_cluster_share_hint": 0.80,
        "bridge_core_share_hint": 0.86,
        "neutral_or_mixed_cluster_share_hint": 0.52,
        "explanatory_core_share_hint": 0.78,
        "low_identity_threat_language_hint": 0.88,
        "media_or_third_party_relay_hint": 0.75,
        "novelty_constructive_hint": 0.35,
    }

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture(echo_box)))

    assert echo["scores"]["bridge_capacity_score"] > 0.65
    assert echo["scores"]["constructive_breakout_score"] > 0.50
    assert not any("guarantee" in line.lower() for line in echo["explanation"])


def test_sealed_echo_box_has_high_closure_low_bridge_capacity() -> None:
    echo_box = {
        "echo_box_id": "echo_closed_001",
        "echo_box_role": "sealed_echo_box",
        "platform_refs": ["sample_forum"],
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_official_001"],
        "stance_distribution": {"support": 0.90, "neutral": 0.05, "oppose": 0.03, "mixed": 0.02},
        "interaction_proxy_summary": {"internal_density": 0.88},
        "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.02},
        "cross_box_exposure_hint": 0.02,
        "bridge_cluster_share_hint": 0.02,
        "bridge_core_share_hint": 0.05,
        "neutral_or_mixed_cluster_share_hint": 0.04,
        "explanatory_core_share_hint": 0.04,
        "low_identity_threat_language_hint": 0.10,
    }

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture(echo_box)))

    assert echo["scores"]["closure_score"] > 0.75
    assert echo["scores"]["bridge_capacity_score"] < 0.20


def test_low_trust_evidence_lowers_echobox_confidence_and_raises_warning() -> None:
    low_trust_evidence = [
        {
            "evidence_id": "low_echo_001",
            "platform": "sample_forum",
            "provenance_type": "screenshot_transcription",
            "trust_label": "low",
            "review_status": "review_needed",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 0.90,
            "source_url_present": False,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_official_001"],
            "echo_box_refs": ["echo_001"],
        }
    ]

    high_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture()))
    low_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture(evidence_items=low_trust_evidence)))

    assert low_echo["scores"]["saturation_confidence_adjusted"] < high_echo["scores"]["saturation_confidence_adjusted"]
    assert low_echo["warnings"]["low_trust_warnings"]
    assert low_echo["warnings"]["low_confidence_warnings"]
    assert "truth_score" not in _walk_keys(low_echo)
    assert "official_verified" not in _walk_keys(low_echo)


def test_duplicate_evidence_folded_not_linear_saturation() -> None:
    base = _echobox_fixture()
    duplicate_fixture = _echobox_fixture()
    duplicate_fixture["evidence_items_safe"][0]["duplicate_group_id"] = "dup_echo_large"
    duplicate_fixture["evidence_items_safe"][0]["duplicate_count"] = 200

    base_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(base))
    duplicate_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(duplicate_fixture))

    assert duplicate_echo["components"]["repetition_signal"] <= 1
    assert duplicate_echo["scores"]["saturation_score"] - base_echo["scores"]["saturation_score"] < 0.25
    assert duplicate_echo["warnings"]["duplicate_folded_warnings"]


def test_one_sided_high_heat_does_not_automatically_mean_echo_chamber() -> None:
    fixture = _echobox_fixture()
    fixture["content_aggregates"][0].update({"volume_score": 0.95, "interaction_score": 0.90})
    for evidence in fixture["evidence_items_safe"]:
        evidence["stance_hint"] = "support"
    fixture["echo_boxes"][0] = {
        "echo_box_id": "echo_heat_001",
        "echo_box_role": "mixed_discussion_box",
        "platform_refs": ["sample_forum"],
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_official_001"],
        "interaction_proxy_summary": {"internal_density": 0.25},
        "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.60},
        "cross_box_exposure_hint": 0.55,
        "bridge_cluster_share_hint": 0.40,
        "low_identity_threat_language_hint": 0.60,
    }

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert echo["scores"]["saturation_score"] < 0.75
    assert echo["boundary_flags"]["not_real_community_map"] is True
    assert any("selected-sample" in line.lower() for line in echo["explanation"])


def test_unknown_echobox_role_uses_unknown_warning() -> None:
    fixture = _echobox_fixture({"echo_box_id": "echo_unknown_001", "echo_box_role": "future_role", "aggregate_ids": ["agg_001"]})

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert echo["echo_box_role"] == "unknown_echo_box"
    assert echo["warnings"]["unknown_echo_box_role_warnings"]
    assert all(0 <= score <= 1 for score in echo["scores"].values())


def test_missing_aggregate_or_evidence_yields_insufficient_data_warning() -> None:
    fixture = _echobox_fixture({"echo_box_id": "echo_orphan_001", "echo_box_role": "mixed_discussion_box", "aggregate_ids": ["missing_agg"]})
    fixture["evidence_items_safe"] = []

    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert echo["warnings"]["insufficient_data_warnings"]
    assert echo["evidence_mass"]["analysis_ready_evidence_count"] == 0
    assert all(score <= 0.30 for score in echo["scores"].values())
    assert echo["schema"] == "sentigraph_echobox_weight_v0_1"


def test_rejected_evidence_excluded_from_echobox_scores() -> None:
    base = _echobox_fixture()
    rejected_fixture = _echobox_fixture()
    rejected_fixture["evidence_items_safe"].append(
        {
            "evidence_id": "rejected_echo_001",
            "platform": "sample_forum",
            "provenance_type": "official_api_public",
            "trust_label": "high",
            "review_status": "rejected",
            "duplicate_count": 20,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 1.0,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_official_001"],
            "echo_box_refs": ["echo_001"],
        }
    )

    base_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(base))
    rejected_echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(rejected_fixture))

    assert rejected_echo["scores"]["saturation_score"] <= base_echo["scores"]["saturation_score"]
    assert rejected_echo["scores"]["echo_risk_score"] <= base_echo["scores"]["echo_risk_score"]
    assert rejected_echo["evidence_mass"]["rejected_excluded_count"] == 1
    assert rejected_echo["warnings"]["rejected_excluded_warnings"]


def test_forbidden_fields_still_block_before_echobox_scoring() -> None:
    fixture = _echobox_fixture()
    fixture["evidence_items_safe"][0]["raw_author_id"] = "hidden"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["echo_box"], list)


def test_overclaim_fields_still_block_before_echobox_scoring() -> None:
    fixture = _echobox_fixture()
    fixture["fixture_metadata"]["causal_proof_claim"] = True

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["echo_box"], list)


def test_auto_execute_still_blocks_before_echobox_scoring() -> None:
    fixture = _echobox_fixture()
    fixture["response_strategy_candidates"].append({"recommendation_level": "auto_execute"})

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["echo_box"], list)


def test_future_unknown_platform_does_not_imply_provider_runnable_for_echobox() -> None:
    fixture = _echobox_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert run["validation_summary"]["unknown_platform_warning_count"] == 1
    assert not isinstance(run["module_outputs"]["echo_box"], list)
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_contentaggregate_and_influencecore_outputs_preserved_in_8P_4() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert run["module_outputs"]["content_aggregate"][0]["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert isinstance(run["module_outputs"]["influence_core"], list)
    assert run["module_outputs"]["influence_core"][0]["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert isinstance(run["module_outputs"]["echo_box"], list)


def test_no_peoplecluster_response_strategy_scores_in_8P_4() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {
        "stance_delta",
        "fatigue_delta",
        "transition_probability",
        "strategy_score",
        "persuasion_score",
    }

    assert not (forbidden_keys & keys)
    assert run["module_outputs"]["people_cluster"] == "not_calculated_in_8P_4"
    assert run["module_outputs"]["response_strategy"] == "not_calculated_in_8P_4"


def test_no_pull_or_stance_effect_in_8P_4() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {
        "pull_ik",
        "stance_effect_ik",
        "stance_effect_ik_adjusted",
        "InfluenceCoreToClusterEffectV01",
    }

    assert not (forbidden_keys & keys)


def test_no_real_community_map_or_full_graph_output() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())
    echo = _echo_output(run)
    keys = _walk_keys(run)

    assert "real_community_map" not in keys
    assert "full_social_graph" not in keys
    assert "target_user_list" not in keys
    assert echo["boundary_flags"]["not_real_community_map"] is True
    assert echo["boundary_flags"]["not_full_graph"] is True


def test_no_forbidden_output_fields_after_echobox_scoring() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture())
    keys = _walk_keys(run)

    forbidden_output_fields = {
        "truth_score",
        "official_verified",
        "causal_chain_confirmed",
        "prediction_probability",
        "persuasion_score",
        "target_user_list",
        "raw_author_identifiers",
        "real_hotlist_score",
    }

    assert not (forbidden_output_fields & keys)


def test_deterministic_same_fixture_same_output_after_echobox_scoring() -> None:
    fixture = _echobox_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second


def test_content_aggregate_existing_8p_2_tests_still_pass() -> None:
    content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture()))

    assert content["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert content["model_status"] == "8P_2_content_aggregate_formula"


def test_influencecore_existing_8p_3_tests_still_pass() -> None:
    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture()))

    assert influence["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert influence["model_status"] == "8P_3_influencecore_formula"


def test_peoplecluster_minimal_fixture_calculates_state_v0_1() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    cluster = _peoplecluster_output(run)

    assert cluster["schema"] == "sentigraph_people_cluster_state_v0_1"
    assert cluster["cluster_id"] == "cluster_mixed_001"
    assert cluster["cluster_role"] == "mixed_bridge"
    assert cluster["cluster_type"] == "mixed_bridge"
    assert cluster["model_status"] == "8P_5_peoplecluster_transition"
    assert cluster["coefficient_source"] == "mock_default"
    assert cluster["calibration_status"] == "uncalibrated"
    assert cluster["empirical_validation"] == "not_started"
    assert cluster["sample_scope"] == "selected_sample_or_local_fixture_only"
    assert cluster["evidence_mass"]["analysis_ready_evidence_count"] == 2
    assert cluster["evidence_mass"]["associated_aggregate_count"] == 1
    assert cluster["evidence_mass"]["associated_influence_core_count"] == 1
    assert cluster["evidence_mass"]["associated_echo_box_count"] == 1

    for score in cluster["state"].values():
        if isinstance(score, (int, float)):
            assert -1 <= score <= 1

    for flag in [
        "anonymous_aggregate_only",
        "not_real_person",
        "not_real_account",
        "not_psychological_profile",
        "not_personality_diagnosis",
        "not_individual_tracking",
        "not_target_user_list",
        "not_persuasion_probability",
        "not_causal_proof",
        "not_prediction",
        "evidence_not_truth",
        "human_review_required",
    ]:
        assert cluster["boundary_flags"][flag] is True

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert isinstance(run["module_outputs"]["influence_core"], list)
    assert isinstance(run["module_outputs"]["echo_box"], list)
    assert run["module_outputs"]["response_strategy"] == []


def test_peoplecluster_output_is_anonymous_aggregate_only() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    cluster = _peoplecluster_output(run)
    keys = _walk_keys(cluster)

    for flag in [
        "anonymous_aggregate_only",
        "not_real_person",
        "not_real_account",
        "not_individual_tracking",
        "not_target_user_list",
    ]:
        assert cluster["boundary_flags"][flag] is True

    assert not ({"raw_author_id", "author_name", "profile_url", "target_user_list"} & keys)


def test_high_heat_does_not_imply_all_people_changed_stance() -> None:
    fixture = _peoplecluster_fixture()
    fixture["content_aggregates"][0].update({"volume_score": 0.98, "interaction_score": 0.95, "growth_score": 0.92})
    fixture["people_clusters"][0]["previous_state"] = {"stance_score": 0.02}

    cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert abs(cluster["state"]["state_delta"]) < 0.20
    assert any("sample-scoped" in line.lower() for line in cluster["explanation"])
    keys = _walk_keys(cluster)
    assert "prediction_probability" not in keys
    assert "causal_chain_confirmed" not in keys


def test_high_echobox_closure_can_raise_fatigue_without_personal_claim() -> None:
    base_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture()))
    fixture = _peoplecluster_fixture()
    fixture["echo_boxes"][0].update(
        {
            "echo_box_role": "sealed_echo_box",
            "stance_distribution": {"support": 0.02, "neutral": 0.02, "oppose": 0.92, "mixed": 0.04},
            "interaction_proxy_summary": {"internal_density": 0.95},
            "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.02},
            "cross_box_exposure_hint": 0.02,
            "bridge_cluster_share_hint": 0.02,
            "bridge_capacity_hint": 0.02,
            "repetition_hint": 0.90,
        }
    )

    sealed_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert sealed_cluster["state"]["fatigue_level"] >= base_cluster["state"]["fatigue_level"]
    assert sealed_cluster["state"]["exit_risk"] >= base_cluster["state"]["exit_risk"]
    assert sealed_cluster["boundary_flags"]["anonymous_aggregate_only"] is True
    assert "psychological_profile" not in _walk_keys(sealed_cluster)


def test_bridgeable_mixed_cluster_has_reactivation_or_openness_potential_without_persuasion_claim() -> None:
    fixture = _peoplecluster_fixture()
    fixture["echo_boxes"][0].update({"bridge_cluster_share_hint": 0.90, "cross_box_exposure_hint": 0.86})
    fixture["influence_cores"][0].update({"core_type": "third_party_context", "bridge_hint": 0.88, "resolution_signal_hint": 0.70})

    cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))
    keys = _walk_keys(cluster)

    assert cluster["state"]["openness_score"] > 0.55
    assert cluster["state"]["reactivation_potential"] > 0
    assert "persuasion_score" not in keys
    assert "pull_ik" not in keys
    assert "stance_effect_ik" not in keys


def test_missing_previous_state_yields_current_state_only_warning() -> None:
    fixture = _peoplecluster_fixture()
    fixture["people_clusters"][0].pop("previous_state", None)

    cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert cluster["state"]["current_state_only"] is True
    assert "missing_previous_state_current_state_only" in cluster["warnings"]["transition_low_confidence_warnings"]
    assert abs(cluster["state"]["state_delta"]) <= 0.05


def test_low_trust_evidence_lowers_peoplecluster_confidence() -> None:
    high_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture()))
    low_trust_evidence = [
        {
            "evidence_id": "low_cluster_001",
            "platform": "sample_forum",
            "provenance_type": "screenshot_transcription",
            "trust_label": "low",
            "review_status": "review_needed",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 0.90,
            "source_url_present": False,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_official_001"],
            "echo_box_refs": ["echo_001"],
            "people_cluster_refs": ["cluster_mixed_001"],
        }
    ]

    low_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture(evidence_items=low_trust_evidence)))

    assert low_cluster["state"]["stance_confidence"] < high_cluster["state"]["stance_confidence"]
    assert low_cluster["warnings"]["low_trust_warnings"]
    assert "truth_score" not in _walk_keys(low_cluster)


def test_rejected_evidence_excluded_from_peoplecluster_scores() -> None:
    base = _peoplecluster_fixture()
    rejected_fixture = _peoplecluster_fixture()
    rejected_fixture["evidence_items_safe"].append(
        {
            "evidence_id": "rejected_cluster_001",
            "platform": "sample_forum",
            "provenance_type": "official_api_public",
            "trust_label": "high",
            "review_status": "rejected",
            "duplicate_count": 20,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": "oppose",
            "emotion_intensity_hint": 1.0,
            "source_url_present": True,
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_official_001"],
            "echo_box_refs": ["echo_001"],
            "people_cluster_refs": ["cluster_mixed_001"],
        }
    )

    base_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(base))
    rejected_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(rejected_fixture))

    assert rejected_cluster["state"]["attention_level"] - base_cluster["state"]["attention_level"] < 0.01
    assert rejected_cluster["state"]["expression_intensity"] - base_cluster["state"]["expression_intensity"] < 0.01
    assert rejected_cluster["evidence_mass"]["rejected_excluded_count"] == 1
    assert rejected_cluster["warnings"]["rejected_excluded_warnings"]


def test_duplicate_evidence_folded_not_linear_attention() -> None:
    base = _peoplecluster_fixture()
    duplicate_fixture = _peoplecluster_fixture()
    duplicate_fixture["evidence_items_safe"][0]["duplicate_group_id"] = "dup_cluster_large"
    duplicate_fixture["evidence_items_safe"][0]["duplicate_count"] = 200

    base_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(base))
    duplicate_cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(duplicate_fixture))

    assert duplicate_cluster["components"]["repetition_signal"] <= 1
    assert duplicate_cluster["state"]["attention_level"] - base_cluster["state"]["attention_level"] < 0.25
    assert duplicate_cluster["warnings"]["duplicate_folded_warnings"]


def test_unknown_peoplecluster_role_uses_unknown_warning() -> None:
    fixture = _peoplecluster_fixture({"cluster_id": "cluster_unknown_001", "cluster_role": "future_cluster", "aggregate_ids": ["agg_001"]})

    cluster = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert cluster["cluster_role"] == "unknown_people_cluster"
    assert cluster["cluster_type"] == "unknown_people_cluster"
    assert cluster["warnings"]["unknown_people_cluster_warnings"]
    for value in cluster["state"].values():
        if isinstance(value, (int, float)):
            assert -1 <= value <= 1


def test_forbidden_fields_still_block_before_peoplecluster_scoring() -> None:
    fixture = _peoplecluster_fixture()
    fixture["evidence_items_safe"][0]["raw_author_id"] = "hidden"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["people_cluster"], list)


def test_overclaim_fields_still_block_before_peoplecluster_scoring() -> None:
    fixture = _peoplecluster_fixture()
    fixture["fixture_metadata"]["causal_proof_claim"] = True

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["people_cluster"], list)


def test_auto_execute_still_blocks_before_peoplecluster_scoring() -> None:
    fixture = _peoplecluster_fixture()
    fixture["response_strategy_candidates"].append({"recommendation_level": "auto_execute"})

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "blocked"
    assert not isinstance(run["module_outputs"]["people_cluster"], list)


def test_future_unknown_platform_does_not_imply_provider_runnable_for_peoplecluster() -> None:
    fixture = _peoplecluster_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert run["validation_summary"]["unknown_platform_warning_count"] == 1
    assert not isinstance(run["module_outputs"]["people_cluster"], list)
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_contentaggregate_influencecore_echobox_outputs_preserved_in_8P_5() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert run["module_outputs"]["content_aggregate"][0]["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert isinstance(run["module_outputs"]["influence_core"], list)
    assert run["module_outputs"]["influence_core"][0]["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert isinstance(run["module_outputs"]["echo_box"], list)
    assert run["module_outputs"]["echo_box"][0]["schema"] == "sentigraph_echobox_weight_v0_1"
    assert isinstance(run["module_outputs"]["people_cluster"], list)


def test_no_response_strategy_scores_in_8P_5() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {"strategy_score", "recommendation_level", "benefit_score", "cost_score"}

    assert run["module_outputs"]["response_strategy"] == []
    assert not (forbidden_keys & keys)
    assert run["runtime_side_effects"]["auto_execute"] is False


def test_no_pull_or_stance_effect_in_8P_5() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {"pull_ik", "stance_effect_ik", "stance_effect_ik_adjusted", "InfluenceCoreToClusterEffectV01"}

    assert not (forbidden_keys & keys)


def test_no_target_user_list_or_real_identity_output() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    keys = _walk_keys(run)

    forbidden_keys = {
        "target_user_list",
        "raw_author_identifiers",
        "raw_author_id",
        "author_id",
        "author_name",
        "profile_url",
        "real_account_id",
        "cross_platform_identity",
    }

    assert not (forbidden_keys & keys)


def test_no_psychological_profile_or_personality_diagnosis_output() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    keys = _walk_keys(run)

    assert "psychological_profile" not in keys
    assert "personality_diagnosis" not in keys


def test_no_forbidden_output_fields_after_peoplecluster_scoring() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())
    keys = _walk_keys(run)

    forbidden_output_fields = {
        "truth_score",
        "official_verified",
        "causal_chain_confirmed",
        "prediction_probability",
        "persuasion_score",
        "target_user_list",
        "raw_author_identifiers",
    }

    assert not (forbidden_output_fields & keys)


def test_deterministic_same_fixture_same_output_after_peoplecluster_scoring() -> None:
    fixture = _peoplecluster_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second


def test_echobox_existing_8p_4_tests_still_pass() -> None:
    echo = _echo_output(calculator.calculate_opinion_ecosystem_mock_fixture(_echobox_fixture()))

    assert echo["schema"] == "sentigraph_echobox_weight_v0_1"
    assert echo["model_status"] == "8P_4_echobox_formula"


def test_response_strategy_minimal_fixture_calculates_comparison_v0_1() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture())
    comparison = _response_strategy_output(run)

    assert comparison["schema"] == "sentigraph_response_strategy_comparison_v0_1"
    assert comparison["model_status"] == "8P_6_response_strategy_comparison"
    assert comparison["coefficient_source"] == "mock_default"
    assert comparison["calibration_status"] == "uncalibrated"
    assert comparison["empirical_validation"] == "not_started"
    assert comparison["sample_scope"] == "selected_sample_or_local_fixture_only"
    assert comparison["candidate_id"] == "strategy_candidate_s4"
    assert comparison["strategy_id"] == "S4"
    assert comparison["strategy_type"] == "FAQ_or_longform_explanation"

    expected_scores = {
        "evidence_fit",
        "timing_fit",
        "clarity_gain",
        "confusion_reduction",
        "emotion_deescalation",
        "bridge_opening",
        "trust_repair_potential",
        "fatigue_relief",
        "reactivation_risk_reduction",
        "amplification_risk",
        "backlash_risk",
        "privacy_risk",
        "overclaim_risk",
        "implementation_risk",
        "benefit_score",
        "cost_score",
        "strategy_score",
    }
    assert expected_scores <= set(comparison["scores"])
    for score in comparison["scores"].values():
        assert 0 <= score <= 1

    recommendation = comparison["recommendation"]
    assert recommendation["human_review_required"] is True
    assert recommendation["not_auto_executed"] is True
    assert recommendation["execution_authorized"] is False
    assert recommendation["public_response_generated"] is False
    assert recommendation["guaranteed_outcome"] is False


def test_response_strategy_preserves_all_upstream_outputs() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture())

    assert isinstance(run["module_outputs"]["content_aggregate"], list)
    assert run["module_outputs"]["content_aggregate"][0]["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert isinstance(run["module_outputs"]["influence_core"], list)
    assert run["module_outputs"]["influence_core"][0]["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert isinstance(run["module_outputs"]["echo_box"], list)
    assert run["module_outputs"]["echo_box"][0]["schema"] == "sentigraph_echobox_weight_v0_1"
    assert isinstance(run["module_outputs"]["people_cluster"], list)
    assert run["module_outputs"]["people_cluster"][0]["schema"] == "sentigraph_people_cluster_state_v0_1"
    assert isinstance(run["module_outputs"]["response_strategy"], list)


def test_response_strategy_highest_level_is_human_review_candidate() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture())
    comparison = _response_strategy_output(run)
    keys = _walk_keys(comparison)
    values = {str(value) for value in _walk_values(comparison)}

    assert comparison["recommendation"]["recommendation_level"] == "strong_candidate_for_human_review"
    assert "approved_for_execution" not in values
    assert "auto_execute" not in values
    assert {"publish_now", "send_now", "post_now"} <= keys or not ({"publish_now", "send_now", "post_now"} & keys)
    assert not ({"publish_now", "send_now", "post_now"} & keys)


def test_response_strategy_auto_execute_is_forbidden() -> None:
    fixture = _response_strategy_fixture({"candidate_id": "bad_auto", "strategy_id": "S3", "execute_now": True})

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    comparison = _response_strategy_output(run)

    assert comparison["strategy_status"] == "forbidden"
    assert comparison["recommendation"]["recommendation_level"] == "forbidden"
    assert comparison["recommendation"]["execution_authorized"] is False
    assert "execute_now" in {blocker["field"] for blocker in comparison["blockers"]["forbidden_behavior_blockers"]}


def test_response_strategy_forbidden_behavior_is_blocked() -> None:
    fixture = _response_strategy_fixture(
        {
            "candidate_id": "bad_seed",
            "strategy_id": "S9",
            "risk_flags": ["fake_consensus", "astroturfing", "covert_seeding", "bot", "sockpuppet", "harassment", "suppression"],
        }
    )

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["strategy_status"] == "forbidden"
    assert comparison["recommendation"]["recommendation_level"] == "forbidden"
    assert comparison["blockers"]["forbidden_behavior_blockers"]


def test_response_strategy_unknown_id_requires_manual_review() -> None:
    fixture = _response_strategy_fixture({"candidate_id": "unknown_strategy", "strategy_id": "S99"})

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["strategy_status"] == "blocked"
    assert comparison["recommendation"]["recommendation_level"] == "blocked_pending_review"
    assert any("unknown_strategy_id" in blocker["reason"] for blocker in comparison["blockers"]["evidence_blockers"])


def test_response_strategy_insufficient_evidence_is_not_strong_candidate() -> None:
    fixture = _minimal_fixture()
    fixture["response_strategy_candidates"] = [
        {"candidate_id": "weak_clarification", "strategy_id": "S3", "strategy_type": "factual_clarification"}
    ]

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["recommendation"]["recommendation_level"] in {"prepare_materials_first", "private_review_only"}
    assert comparison["recommendation"]["recommendation_level"] != "strong_candidate_for_human_review"
    assert comparison["warnings"]["missing_component_warnings"]


def test_t4_long_faq_can_have_clarity_benefit_and_backlash_risk() -> None:
    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture()))

    assert comparison["strategy_id"] == "S4"
    assert comparison["scores"]["clarity_gain"] > 0
    assert comparison["scores"]["backlash_risk"] > 0 or comparison["scores"]["amplification_risk"] > 0
    explanation = " ".join(comparison["explanation"]).lower()
    assert "benefit" in explanation
    assert "risk" in explanation
    assert "guarantee" not in explanation


def test_no_guaranteed_calming_claim() -> None:
    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture()))
    keys = _walk_keys(comparison)
    values = {str(value).lower() for value in _walk_values(comparison)}

    assert "guaranteed_calming" not in keys
    assert "guaranteed_success" not in keys
    assert comparison["recommendation"]["guaranteed_outcome"] is False
    assert all("guaranteed calming" not in value for value in values)


def test_low_credibility_claim_not_treated_as_fact() -> None:
    fixture = _response_strategy_fixture(
        {
            "candidate_id": "weak_fact_claim",
            "strategy_id": "S3",
            "strategy_type": "factual_clarification",
            "claim_intensity": 0.95,
            "strategy_clarity_base": 0.80,
        }
    )
    fixture["influence_cores"][0]["core_type"] = "low_trust_claim"
    fixture["influence_cores"][0]["source_transparency_hint"] = 0.05
    fixture["influence_cores"][0]["cross_source_consistency_hint"] = 0.05
    for evidence in fixture["evidence_items_safe"]:
        evidence["trust_label"] = "low"
        evidence["provenance_type"] = "manual_text_without_source"

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))
    keys = _walk_keys(comparison)

    assert comparison["recommendation"]["recommendation_level"] != "strong_candidate_for_human_review"
    assert comparison["blockers"]["evidence_blockers"]
    assert "truth_score" not in keys
    assert "official_verified" not in keys


def test_no_response_is_baseline_not_automatic_recommendation() -> None:
    fixture = _response_strategy_fixture({"candidate_id": "baseline", "strategy_id": "S0"})

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))
    explanation = " ".join(comparison["explanation"]).lower()

    assert comparison["recommendation"]["recommendation_level"] == "monitor_only"
    assert "baseline" in explanation
    assert "ignore" not in explanation
    assert comparison["recommendation"]["execution_authorized"] is False


def test_third_party_explanation_requires_disclosure_and_review() -> None:
    fixture = _response_strategy_fixture(
        {
            "candidate_id": "third_party_ok",
            "strategy_id": "S6",
            "strategy_type": "third_party_explanation",
            "third_party_explanation": True,
            "voluntary": True,
            "informed_consent": True,
            "redacted": True,
            "minor_protected": True,
            "context_verifiable": True,
            "no_private_detail_exposure": True,
            "human_review_approved": True,
            "disclosed_third_party": True,
            "fabricated_endorsement": False,
        }
    )

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["strategy_status"] in {"allowed", "allowed_with_review"}
    assert comparison["recommendation"]["human_review_required"] is True
    assert not comparison["blockers"]["forbidden_behavior_blockers"]


def test_fabricated_third_party_endorsement_is_forbidden() -> None:
    fixture = _response_strategy_fixture(
        {
            "candidate_id": "fake_third_party",
            "strategy_id": "S6",
            "strategy_type": "third_party_explanation",
            "third_party_explanation": True,
            "fabricated_endorsement": True,
        }
    )

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["strategy_status"] == "forbidden"
    assert comparison["recommendation"]["recommendation_level"] == "forbidden"


def test_minors_or_family_material_without_consent_is_blocked() -> None:
    fixture = _response_strategy_fixture(
        {
            "candidate_id": "minor_sensitive",
            "strategy_id": "S7",
            "use_of_personal_story": 1.0,
            "minor_or_family_sensitivity": 1.0,
        }
    )

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))

    assert comparison["recommendation"]["recommendation_level"] in {"blocked_pending_review", "private_review_only"}
    assert comparison["blockers"]["privacy_blockers"]
    assert comparison["recommendation"]["eligible_for_human_review"] is False


def test_privacy_blocker_overrides_high_benefit() -> None:
    candidate = _response_strategy_fixture()["response_strategy_candidates"][0]
    candidate.update({"candidate_id": "high_benefit_private", "use_of_personal_story": 1.0, "minor_or_family_sensitivity": 1.0})

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture(candidate)))

    assert comparison["scores"]["benefit_score"] > 0.4
    assert comparison["recommendation"]["recommendation_level"] in {"blocked_pending_review", "private_review_only"}
    assert comparison["blockers"]["privacy_blockers"] or comparison["blockers"]["consent_blockers"]


def test_community_deconstruction_support_not_covert_seeding() -> None:
    transparent = _response_strategy_fixture(
        {
            "candidate_id": "community_transparent",
            "strategy_id": "S9",
            "strategy_type": "community_deconstruction_support",
            "transparency_level": 0.9,
            "strategy_bridge_base": 0.7,
        }
    )
    covert = _response_strategy_fixture(
        {
            "candidate_id": "community_covert",
            "strategy_id": "S9",
            "strategy_type": "community_deconstruction_support",
            "risk_flags": ["covert_seeding", "fake_consensus"],
        }
    )

    transparent_output = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(transparent))
    covert_output = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(covert))

    assert transparent_output["strategy_status"] in {"allowed", "allowed_with_review"}
    assert covert_output["strategy_status"] == "forbidden"


def test_correction_or_apology_requires_applicability_evidence() -> None:
    fixture = _response_strategy_fixture(
        {"candidate_id": "apology_without_basis", "strategy_id": "S7", "strategy_type": "correction_or_apology_if_applicable"}
    )
    for evidence in fixture["evidence_items_safe"]:
        evidence["trust_label"] = "low"
        evidence["source_url_present"] = False

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(fixture))
    keys = _walk_keys(comparison)

    assert comparison["recommendation"]["recommendation_level"] in {"prepare_materials_first", "private_review_only"}
    assert "official_verified" not in keys


def test_no_generated_response_text_in_8P_6() -> None:
    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture()))
    keys = _walk_keys(comparison)

    assert "response_text" not in keys
    assert "generated_public_message" not in keys
    assert "message_draft" not in keys


def test_no_peoplecluster_or_echobox_effect_objects_in_8P_6() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture())
    keys = _walk_keys(run)
    values = {str(value) for value in _walk_values(run)}

    assert "ResponseToPeopleClusterEffectV01" not in keys
    assert "ResponseToEchoBoxEffectV01" not in keys
    assert "GeneratedInfluenceCoreCandidateV01" not in keys
    assert "ResponseToPeopleClusterEffectV01" not in values
    assert "ResponseToEchoBoxEffectV01" not in values
    assert "GeneratedInfluenceCoreCandidateV01" not in values


def test_no_pull_or_stance_effect_in_8P_6() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture())
    keys = _walk_keys(run)

    assert "pull_ik" not in keys
    assert "stance_effect_ik" not in keys
    assert "stance_effect_ik_adjusted" not in keys
    assert "InfluenceCoreToClusterEffectV01" not in keys


def test_no_target_user_list_or_persuasion_score() -> None:
    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture()))
    keys = _walk_keys(comparison)

    assert "target_user_list" not in keys
    assert "persuasion_score" not in keys
    assert "individual_persuasion_score" not in keys
    assert "real_identity_matching" not in keys


def test_no_forbidden_output_fields_after_response_strategy_scoring() -> None:
    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture()))
    keys = _walk_keys(comparison)

    forbidden_output_fields = {
        "truth_score",
        "official_verified",
        "causal_chain_confirmed",
        "prediction_probability",
        "generated_public_message",
        "target_user_list",
        "raw_author_identifiers",
    }

    assert not (forbidden_output_fields & keys)


def test_response_strategy_blocker_precedence_over_score() -> None:
    candidate = _response_strategy_fixture()["response_strategy_candidates"][0]
    candidate.update({"candidate_id": "score_cannot_override", "risk_flags": ["fake_consensus"], "privacy_risk": 1.0})

    comparison = _response_strategy_output(calculator.calculate_opinion_ecosystem_mock_fixture(_response_strategy_fixture(candidate)))

    assert comparison["scores"]["benefit_score"] > 0.4
    assert comparison["strategy_status"] == "forbidden"
    assert comparison["recommendation"]["recommendation_level"] == "forbidden"


def test_response_strategy_missing_candidates_yields_safe_empty_or_warning() -> None:
    run = calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture())

    assert run["module_outputs"]["response_strategy"] == []
    assert "strong_candidate_for_human_review" not in {str(value) for value in _walk_values(run["module_outputs"]["response_strategy"])}


def test_future_unknown_platform_does_not_calculate_response_strategy() -> None:
    fixture = _response_strategy_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert run["validation_summary"]["status"] == "manual_review_required"
    assert not isinstance(run["module_outputs"]["response_strategy"], list)
    assert all("provider" not in str(value).lower() or "not" in str(value).lower() for value in _walk_values(run))


def test_deterministic_same_fixture_same_response_strategy_output() -> None:
    fixture = _response_strategy_fixture()

    first = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)
    second = calculator.calculate_opinion_ecosystem_mock_fixture(fixture)

    assert first == second


def test_content_aggregate_existing_8p_2_tests_still_pass() -> None:
    content = _content_output(calculator.calculate_opinion_ecosystem_mock_fixture(_content_aggregate_fixture()))

    assert content["schema"] == "sentigraph_content_aggregate_weight_v0_1"
    assert 0 <= content["scores"]["sample_heat_score"] <= 1


def test_influencecore_existing_8p_3_tests_still_pass() -> None:
    influence = _influence_output(calculator.calculate_opinion_ecosystem_mock_fixture(_influencecore_fixture()))

    assert influence["schema"] == "sentigraph_influence_core_weight_v0_1"
    assert 0 <= influence["scores"]["factual_credibility"] <= 1


def test_peoplecluster_existing_8p_5_tests_still_pass() -> None:
    people = _peoplecluster_output(calculator.calculate_opinion_ecosystem_mock_fixture(_peoplecluster_fixture()))

    assert people["schema"] == "sentigraph_people_cluster_state_v0_1"
    assert 0 <= people["state"]["attention_level"] <= 1
