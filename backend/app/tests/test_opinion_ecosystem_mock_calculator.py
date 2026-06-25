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
