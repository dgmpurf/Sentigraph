from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services import opinion_ecosystem_dense_graph_generated_run_integration as dense_integration
from app.services.generated_run_dense_graph_bridge_integration import (
    build_safe_generated_run_dense_graph_bridge_summary,
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


SENTINEL_TOKEN = "actual-token-should-never-appear"
SENTINEL_AUTHOR = "actual-author-name-should-never-appear"
SENTINEL_PROFILE = "actual-profile-url-should-never-appear"
SENTINEL_RAW_ROW = "actual-raw-row-should-never-appear"
SENTINEL_PATH = "G:/private-collector/should-never-appear"
SENTINEL_RESPONSE = "actual-response-text-should-never-appear"


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


def _safe_execution(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    execution.update(overrides)
    return execution


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


def test_ready_execution_integrates_generated_run_with_dense_graph_without_public_side_effects() -> None:
    integration = integrate_generated_run_with_dense_graph_from_execution(_safe_execution(), created_by="unit_test")
    summary = build_safe_generated_run_dense_graph_bridge_summary(integration)

    assert integration["integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert integration["integration_status"] == "integrated_backend_dense_graph_preview"
    assert integration["input_source_kind"] == "minimum_real_run_bridge_execution"
    assert integration["integration_mode"] == "controlled_backend_only_generated_run_dense_graph"
    assert integration["generated_run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert integration["dense_graph_executed"] is True
    assert integration["dense_graph_integration"]
    assert integration["dense_graph_summary"]
    assert integration["frontend_integration_approved"] is False
    assert integration["route_changed"] is False
    assert integration["api_route_added"] is False
    assert integration["report_generated"] is False
    assert integration["sandbox_public_event_generated"] is False
    assert integration["generated_response_text"] is False
    assert integration["public_route_created"] is False

    assert integration["dense_graph_summary"]["frontend_ready"] is False
    assert integration["dense_graph_summary"]["route_ready"] is False
    assert integration["dense_graph_summary"]["production_ready"] is False
    assert integration["dense_graph_integration"]["human_review_required"] is True

    _assert_false_side_effects(integration)
    assert integration["runtime_side_effects"]["wrote_evidence_layer"] is False
    assert integration["runtime_side_effects"]["created_production_case"] is False
    assert integration["runtime_side_effects"]["created_analysis_run"] is False
    assert integration["boundary_flags"]["anonymous_aggregate_only"] is True
    assert integration["boundary_flags"]["not_full_web"] is True
    assert integration["boundary_flags"]["human_review_required"] is True
    assert summary["dense_graph_executed"] is True
    assert summary["frontend_ready"] is False
    assert summary["route_ready"] is False
    assert summary["production_ready"] is False


def test_blocked_execution_does_not_call_dense_graph(monkeypatch) -> None:
    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not execute for blocked 8V-6 execution")

    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)
    execution = _safe_execution(execution_status="blocked_metadata_contract", blockers=[{"reason": "upstream_blocked"}])

    integration = integrate_generated_run_with_dense_graph_from_execution(execution)

    assert integration["integration_status"] == "blocked_generated_run_not_ready"
    assert integration["dense_graph_executed"] is False
    assert integration["dense_graph_integration"] is None
    _assert_false_side_effects(integration)


def test_requested_side_effects_block_and_remain_false(monkeypatch) -> None:
    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not execute when side effects are requested")

    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)
    execution = _safe_execution(
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        route_changed=True,
        api_route_added=True,
        frontend_integration_approved=True,
        report_generated=True,
        sandbox_public_event_generated=True,
        public_route_created=True,
        generated_response_text=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    integration = integrate_generated_run_with_dense_graph_from_execution(execution)

    assert integration["integration_status"] == "blocked_requested_side_effect"
    assert integration["dense_graph_executed"] is False
    assert integration["frontend_integration_approved"] is False
    assert integration["route_changed"] is False
    assert integration["api_route_added"] is False
    assert integration["report_generated"] is False
    assert integration["sandbox_public_event_generated"] is False
    assert integration["generated_response_text"] is False
    assert integration["public_route_created"] is False
    _assert_false_side_effects(integration)


def test_forbidden_values_block_or_do_not_leak() -> None:
    execution = _safe_execution(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
        response_text=SENTINEL_RESPONSE,
    )

    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    encoded = _encoded(integration)

    assert integration["integration_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert integration["dense_graph_executed"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert SENTINEL_RESPONSE not in encoded
    assert "private-collector" not in encoded


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-8 dense graph bridge smoke")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-8 dense graph bridge smoke")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    integration = integrate_generated_run_with_dense_graph_from_execution(_safe_execution())
    encoded = _encoded(integration)

    assert integration["integration_status"] == "integrated_backend_dense_graph_preview"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert integration["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert integration["runtime_side_effects"]["read_original_package_rows"] is False


def test_frontend_route_report_readiness_remain_false() -> None:
    integration = integrate_generated_run_with_dense_graph_from_execution(_safe_execution())

    assert integration["frontend_integration_approved"] is False
    assert integration["route_changed"] is False
    assert integration["api_route_added"] is False
    assert integration["report_generated"] is False
    assert integration["sandbox_public_event_generated"] is False
    assert integration["public_route_created"] is False
    assert integration["dense_graph_summary"]["frontend_ready"] is False
    assert integration["dense_graph_summary"]["route_ready"] is False
    assert integration["dense_graph_summary"]["production_ready"] is False


def test_missing_generated_run_blocks_without_dense_graph(monkeypatch) -> None:
    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not execute without generated run")

    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)
    execution = _safe_execution(generated_run=None)

    integration = integrate_generated_run_with_dense_graph_from_execution(execution)

    assert integration["integration_status"] == "blocked_metadata_contract"
    assert integration["dense_graph_executed"] is False
    assert integration["dense_graph_integration"] is None
    assert any(blocker["reason"] == "missing_generated_run" for blocker in integration["blockers"])


def test_forbidden_output_fields_are_not_produced() -> None:
    integration = integrate_generated_run_with_dense_graph_from_execution(_safe_execution())
    keys = _walk_keys(integration)

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
