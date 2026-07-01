from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services import opinion_ecosystem_dense_graph_generated_run_integration as dense_integration
from app.services import opinion_ecosystem_minimum_real_run as minimum_real_run
from app.services.minimum_real_run_bridge_execution import (
    build_safe_minimum_real_run_bridge_execution_summary,
    execute_minimum_real_run_from_bridge_candidate,
)
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


SENTINEL_TOKEN = "actual-token-should-never-appear"
SENTINEL_AUTHOR = "actual-author-name-should-never-appear"
SENTINEL_PROFILE = "actual-profile-url-should-never-appear"
SENTINEL_RAW_ROW = "actual-raw-row-should-never-appear"
SENTINEL_PATH = "G:/private-collector/should-never-appear"


def _safe_staging_summary(**overrides) -> dict:
    summary = {
        "schema": "sentigraph_review_only_staging_summary_v0_1",
        "staging_candidate_id": "review_staging_candidate_controlled",
        "analysis_request_id": "analysis_request_controlled",
        "provider_result_id": "provider_result_controlled",
        "provider_job_id": "provider_job_controlled",
        "package_name": "controlled_exported_package_fixture",
        "package_role": "review_ready_candidate",
        "case_id_hint": "case_controlled",
        "case_title_hint": "Controlled case",
        "validation_status": "passed",
        "evidence_count": 12,
        "source_count": 3,
        "warning_count": 1,
        "error_count": 0,
        "metadata_summary": {
            "evidence_count": 12,
            "source_count": 3,
            "package_name": "controlled_exported_package_fixture",
        },
        "validation_summary": {"status": "passed", "warnings": 1, "errors": 0},
        "coverage_summary": {
            "coverage_note": "Controlled metadata fixture only; not full-web and not full-platform.",
            "coverage_note_present": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "gate_result": {
            "package_resolution_status": "accepted_metadata_only",
            "provider_result_status": "accepted_metadata_only",
            "privacy_status": "clear",
            "path_status": "accepted_metadata_only",
            "metadata_contract_status": "metadata_contract_ok",
            "evidence_row_boundary_status": "evidence_rows_not_read",
        },
        "audit_refs": [{"audit_ref_id": "audit_ref_controlled", "scope": "metadata_only"}],
        "metadata_only": True,
        "path_exposed": False,
        "path_reference": "review_only_metadata_summary",
        "blockers": [],
        "warnings": [],
        "safety_flags": {
            "metadata_only": True,
            "full_evidence_rows_parsed": False,
            "evidence_layer_written": False,
            "production_case_created": False,
            "analysis_run_created": False,
        },
    }
    summary.update(overrides)
    return summary


def _safe_bridge(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    bridge.update(overrides)
    return bridge


def _encoded(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


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


def _assert_false_side_effects(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def test_ready_bridge_executes_local_minimum_real_run_without_production_side_effects() -> None:
    execution = execute_minimum_real_run_from_bridge_candidate(_safe_bridge(), created_by="unit_test")
    summary = build_safe_minimum_real_run_bridge_execution_summary(execution)
    generated_run = execution["generated_run"]

    assert execution["execution_schema"] == "sentigraph_minimum_real_run_bridge_execution_v0_1"
    assert execution["execution_status"] == "executed_local_minimum_real_run"
    assert execution["bridge_status_at_execution"] == "ready_for_minimum_real_run_input_candidate"
    assert execution["input_source_kind"] == "staging_candidate_generated_run_bridge"
    assert execution["execution_mode"] == "controlled_backend_only_minimum_real_run"
    assert execution["metadata_only"] is True
    assert execution["evidence_rows_parsed"] is False
    assert execution["minimum_real_run_executed"] is True
    assert execution["dense_graph_called"] is False

    assert generated_run["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert generated_run["human_review_required"] is True
    assert generated_run["coefficient_source"] == "mock_default"
    assert generated_run["calibration_status"] == "uncalibrated"
    assert generated_run["empirical_validation"] == "not_started"
    assert generated_run["runtime_side_effects"]["called_real_api"] is False
    assert generated_run["runtime_side_effects"]["created_analysis_run"] is False
    assert generated_run["runtime_side_effects"]["generated_response_text"] is False

    for flag in (
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "human_review_required",
        "no_auto_execute",
        "no_generated_public_response",
    ):
        assert generated_run["boundary_flags"][flag] is True

    _assert_false_side_effects(execution)
    assert execution["runtime_side_effects"]["wrote_evidence_layer"] is False
    assert execution["runtime_side_effects"]["created_production_case"] is False
    assert execution["runtime_side_effects"]["created_analysis_run"] is False
    assert "call_dense_graph_later_after_separate_decision" in execution["downstream_allowed_actions"]
    assert "call_dense_graph_directly" in execution["downstream_blocked_actions"]
    assert summary["minimum_real_run_executed"] is True
    assert summary["path_exposed"] is False


def test_blocked_bridge_does_not_execute_minimum_wrapper(monkeypatch) -> None:
    def fail_wrapper(*args, **kwargs):
        raise AssertionError("minimum real-run wrapper must not execute for blocked bridge")

    monkeypatch.setattr(minimum_real_run, "generate_opinion_ecosystem_minimum_real_run", fail_wrapper)
    bridge = _safe_bridge(bridge_status="blocked_metadata_contract", blockers=[{"reason": "upstream_blocked"}])

    execution = execute_minimum_real_run_from_bridge_candidate(bridge)

    assert execution["execution_status"] == "blocked_bridge_not_ready"
    assert execution["minimum_real_run_executed"] is False
    assert execution["generated_run"] is None
    _assert_false_side_effects(execution)


def test_requested_side_effects_block_execution_and_remain_false(monkeypatch) -> None:
    def fail_wrapper(*args, **kwargs):
        raise AssertionError("minimum real-run wrapper must not execute when side effects are requested")

    monkeypatch.setattr(minimum_real_run, "generate_opinion_ecosystem_minimum_real_run", fail_wrapper)
    bridge = _safe_bridge(
        evidence_rows_parsed=True,
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        dense_graph_called=True,
        report_generated=True,
        public_route_created=True,
        generated_response_text=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    execution = execute_minimum_real_run_from_bridge_candidate(bridge)

    assert execution["execution_status"] == "blocked_requested_side_effect"
    assert execution["minimum_real_run_executed"] is False
    assert execution["dense_graph_called"] is False
    assert execution["generated_run"] is None
    assert execution["blockers"]
    _assert_false_side_effects(execution)


def test_dense_graph_is_not_called(monkeypatch) -> None:
    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not execute in 8V-6 bridge execution")

    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)

    execution = execute_minimum_real_run_from_bridge_candidate(_safe_bridge())

    assert execution["execution_status"] == "executed_local_minimum_real_run"
    assert execution["dense_graph_called"] is False


def test_forbidden_values_block_or_do_not_leak() -> None:
    bridge = _safe_bridge(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
    )

    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    encoded = _encoded(execution)

    assert execution["execution_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert execution["minimum_real_run_executed"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert "private-collector" not in encoded


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-6 bridge execution")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-6 bridge execution")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    execution = execute_minimum_real_run_from_bridge_candidate(_safe_bridge())
    encoded = _encoded(execution)

    assert execution["execution_status"] == "executed_local_minimum_real_run"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert execution["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert execution["runtime_side_effects"]["read_original_package_rows"] is False


def test_missing_minimum_candidate_blocks_without_executing(monkeypatch) -> None:
    def fail_wrapper(*args, **kwargs):
        raise AssertionError("minimum real-run wrapper must not execute without candidate")

    monkeypatch.setattr(minimum_real_run, "generate_opinion_ecosystem_minimum_real_run", fail_wrapper)
    bridge = _safe_bridge(minimum_real_run_input_candidate=None)

    execution = execute_minimum_real_run_from_bridge_candidate(bridge)

    assert execution["execution_status"] == "blocked_metadata_contract"
    assert execution["minimum_real_run_executed"] is False
    assert execution["generated_run"] is None
    assert any(blocker["reason"] == "missing_minimum_real_run_input_candidate" for blocker in execution["blockers"])


def test_forbidden_output_fields_are_not_produced() -> None:
    execution = execute_minimum_real_run_from_bridge_candidate(_safe_bridge())
    keys = _walk_keys(execution)

    assert not (
        {
            "response_text",
            "generated_public_message",
            "target_user_list",
            "persuasion_score",
            "truth_score",
            "official_verified",
            "prediction_probability",
            "psychological_profile",
            "personality_diagnosis",
            "publish_now",
            "send_now",
            "post_now",
            "execute_now",
        }
        & keys
    )
