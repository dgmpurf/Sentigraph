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
