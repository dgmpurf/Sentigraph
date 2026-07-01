from __future__ import annotations

import json
from pathlib import Path

from app.services import opinion_ecosystem_dense_graph_generated_run_integration as dense_integration
from app.services import opinion_ecosystem_minimum_real_run as minimum_real_run
from app.services.staging_candidate_generated_run_bridge import (
    build_minimum_real_run_input_candidate_from_staging,
    build_safe_staging_to_generated_run_bridge_summary,
    build_staging_candidate_generated_run_bridge,
)


SENTINEL_TOKEN = "actual-token-should-never-appear"
SENTINEL_AUTHOR = "actual-author-name-should-never-appear"
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
        "allowed_actions": ["continue_review", "request_future_promotion_gate"],
        "blocked_actions": ["create_production_case", "start_analysis_run", "publish", "send", "post", "execute"],
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


def _encoded(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def test_ready_staging_summary_maps_to_metadata_only_bridge_candidate() -> None:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary(), created_by="unit_test")
    minimum_input = bridge["minimum_real_run_input_candidate"]
    safe_summary = build_safe_staging_to_generated_run_bridge_summary(bridge)

    assert bridge["bridge_schema"] == "sentigraph_staging_candidate_generated_run_bridge_v0_1"
    assert bridge["bridge_status"] == "ready_for_minimum_real_run_input_candidate"
    assert bridge["staging_candidate_id"] == "review_staging_candidate_controlled"
    assert bridge["provider_result_id"] == "provider_result_controlled"
    assert bridge["provider_job_id"] == "provider_job_controlled"
    assert bridge["request_id"] == "analysis_request_controlled"
    assert bridge["case_id_hint"] == "case_controlled"
    assert bridge["package_name"] == "controlled_exported_package_fixture"
    assert bridge["package_role"] == "review_ready_candidate"
    assert bridge["input_source_kind"] == "review_only_staging_candidate"
    assert bridge["metadata_only"] is True
    assert bridge["evidence_rows_parsed"] is False
    assert bridge["evidence_layer_write"] is False
    assert bridge["production_case_created"] is False
    assert bridge["production_analysis_run_created"] is False
    assert bridge["generated_response_text"] is False
    assert bridge["public_route_created"] is False
    assert bridge["human_review_required"] is True
    assert bridge["generated_run_requested"] is False

    assert minimum_input["model_input_kind"] == "metadata_only_staging_summary"
    assert minimum_input["human_review_required"] is True
    assert minimum_input["coefficient_source"] == "mock_default"
    assert minimum_input["calibration_status"] == "uncalibrated"
    assert minimum_input["empirical_validation"] == "not_started"
    assert minimum_input["evidence_items_safe"] == []
    assert minimum_input["fixture_metadata"]["selected_sample_only"] is True

    assert "request_future_minimum_real_run_execution_decision" in bridge["downstream_allowed_actions"]
    for blocked_action in (
        "parse_evidence_rows",
        "write_evidence_layer",
        "create_production_case",
        "create_production_analysis_run",
        "call_dense_graph_directly",
        "generate_public_output",
    ):
        assert blocked_action in bridge["downstream_blocked_actions"]
    assert safe_summary["path_exposed"] is False


def test_minimum_input_builder_returns_safe_candidate_without_executing_run() -> None:
    candidate = build_minimum_real_run_input_candidate_from_staging(_safe_staging_summary())

    assert candidate["case_id_hint"] == "case_controlled"
    assert candidate["sample_id"] == "controlled_exported_package_fixture"
    assert candidate["provider_result_id"] == "provider_result_controlled"
    assert candidate["staging_candidate_id"] == "review_staging_candidate_controlled"
    assert candidate["package_name"] == "controlled_exported_package_fixture"
    assert candidate["coverage_summary"]["not_full_web"] is True
    assert candidate["validation_summary"]["status"] == "passed"
    assert candidate["evidence_items_safe"] == []


def test_sentinel_values_in_forbidden_places_are_blocked_and_not_emitted() -> None:
    unsafe = _safe_staging_summary(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        profile_url="actual-profile-url-should-never-appear",
    )

    bridge = build_staging_candidate_generated_run_bridge(unsafe)
    encoded = _encoded(bridge)

    assert bridge["bridge_status"] == "blocked_privacy_issue"
    assert bridge["blockers"]
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert "actual-profile-url-should-never-appear" not in encoded
    assert bridge["runtime_side_effects"]["called_real_api"] is False
    assert bridge["runtime_side_effects"]["parsed_evidence_items_file"] is False


def test_requested_side_effect_flags_block_bridge_and_remain_false() -> None:
    unsafe = _safe_staging_summary(
        evidence_row_parsing_requested=True,
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        generated_response_text=True,
        public_route_created=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    bridge = build_staging_candidate_generated_run_bridge(unsafe)

    assert bridge["bridge_status"] == "blocked_requested_side_effect"
    assert bridge["blockers"]
    assert bridge["evidence_rows_parsed"] is False
    assert bridge["evidence_layer_write"] is False
    assert bridge["production_case_created"] is False
    assert bridge["production_analysis_run_created"] is False
    assert bridge["generated_response_text"] is False
    assert bridge["public_route_created"] is False
    assert all(value is False for value in bridge["runtime_side_effects"].values())


def test_bridge_does_not_call_minimum_real_run_or_dense_graph(monkeypatch) -> None:
    def fail_minimum_run(*args, **kwargs):
        raise AssertionError("minimum real-run must not execute in 8V-4 bridge skeleton")

    def fail_dense_graph(*args, **kwargs):
        raise AssertionError("dense graph must not execute in 8V-4 bridge skeleton")

    monkeypatch.setattr(minimum_real_run, "generate_opinion_ecosystem_minimum_real_run", fail_minimum_run)
    monkeypatch.setattr(dense_integration, "generate_opinion_ecosystem_run_with_dense_graph_attachment", fail_dense_graph)

    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())

    assert bridge["bridge_status"] == "ready_for_minimum_real_run_input_candidate"
    assert bridge["runtime_side_effects"]["created_analysis_run"] is False
    assert bridge["runtime_side_effects"]["generated_sandbox_runtime"] is False


def test_absolute_or_private_paths_do_not_leak_to_safe_output() -> None:
    unsafe = _safe_staging_summary(
        package_name=SENTINEL_PATH,
        absolute_package_path=SENTINEL_PATH,
        path_reference=SENTINEL_PATH,
    )

    bridge = build_staging_candidate_generated_run_bridge(unsafe)
    encoded = _encoded(bridge)

    assert bridge["bridge_status"] in {"blocked_path_escape", "blocked_privacy_issue", "blocked_metadata_contract"}
    assert SENTINEL_PATH not in encoded
    assert "private-collector" not in encoded
    assert bridge["package_name"] is None
    assert bridge["minimum_real_run_input_candidate"]["package_name"] is None


def test_missing_required_metadata_blocks_bridge() -> None:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary(package_name="", provider_result_id=""))

    assert bridge["bridge_status"] == "blocked_metadata_contract"
    assert {item["reason"] for item in bridge["blockers"]} >= {"missing_package_name", "missing_provider_result_id"}

