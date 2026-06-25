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
