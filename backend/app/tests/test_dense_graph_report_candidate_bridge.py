from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import (
    build_dense_graph_report_candidate_from_integration,
    build_safe_dense_graph_report_candidate_summary,
)
from app.services.generated_run_dense_graph_bridge_integration import (
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
SENTINEL_PUBLIC_URL = "https://public-download.example/should-never-appear"


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


def _safe_integration(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    integration.update(overrides)
    return integration


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


def test_ready_dense_graph_integration_creates_local_report_candidate_without_report_side_effects() -> None:
    candidate = build_dense_graph_report_candidate_from_integration(_safe_integration(), created_by="unit_test")
    summary = build_safe_dense_graph_report_candidate_summary(candidate)
    report_summary = candidate["report_candidate_summary"]

    assert candidate["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert candidate["report_candidate_status"] == "candidate_ready"
    assert candidate["input_source_kind"] == "generated_run_dense_graph_bridge_integration"
    assert candidate["candidate_mode"] == "backend_only_local_report_candidate"
    assert candidate["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert candidate["dense_graph_summary"]
    assert report_summary
    assert report_summary["candidate_scope"] == "selected_sample_only_dense_graph_preview"
    assert report_summary["human_review_required"] is True
    assert report_summary["final_report_ready"] is False
    assert report_summary["export_ready"] is False
    assert report_summary["public_ready"] is False
    assert report_summary["b_end_runtime_ready"] is False
    assert report_summary["sandbox_public_event_ready"] is False

    assert candidate["report_candidate_created"] is True
    assert candidate["final_report_created"] is False
    assert candidate["b_end_report_runtime_generated"] is False
    assert candidate["sandbox_public_event_generated"] is False
    assert candidate["export_artifact_created"] is False
    assert candidate["generated_response_text"] is False
    assert candidate["public_route_created"] is False
    assert candidate["frontend_integration_approved"] is False
    assert candidate["route_ready"] is False
    assert candidate["frontend_ready"] is False
    assert candidate["production_ready"] is False
    assert candidate["boundary_flags"]["human_review_required"] is True
    assert candidate["boundary_flags"]["not_final_report"] is True
    _assert_false_side_effects(candidate)

    assert summary["report_candidate_status"] == "candidate_ready"
    assert summary["report_candidate_created"] is True
    assert summary["final_report_ready"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False


def test_wrong_or_missing_integration_blocks_report_candidate() -> None:
    wrong_schema = _safe_integration(integration_schema="unknown")
    wrong_status = _safe_integration(integration_status="blocked_metadata_contract")
    missing_dense_graph = _safe_integration(dense_graph_integration=None)
    missing_summary = _safe_integration(dense_graph_summary=None)

    for value in (wrong_schema, wrong_status, missing_dense_graph, missing_summary):
        candidate = build_dense_graph_report_candidate_from_integration(value)

        assert candidate["report_candidate_status"] == "blocked_metadata_contract"
        assert candidate["report_candidate_created"] is False
        assert candidate["final_report_created"] is False
        assert candidate["export_artifact_created"] is False
        assert candidate["public_route_created"] is False
        _assert_false_side_effects(candidate)


def test_frontend_route_or_production_ready_blocks_candidate() -> None:
    for flag in ("frontend_ready", "route_ready", "production_ready"):
        integration = _safe_integration()
        integration["dense_graph_summary"][flag] = True

        candidate = build_dense_graph_report_candidate_from_integration(integration)

        assert candidate["report_candidate_status"] == "blocked_requested_side_effect"
        assert candidate["report_candidate_created"] is False
        assert candidate["route_ready"] is False
        assert candidate["frontend_ready"] is False
        assert candidate["production_ready"] is False
        _assert_false_side_effects(candidate)


def test_requested_side_effects_block_report_candidate_and_remain_false() -> None:
    integration = _safe_integration(
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        final_report_created=True,
        final_summary_report_requested=True,
        export_artifact_created=True,
        generated_pdf=True,
        generated_markdown_report=True,
        generated_briefing_deck=True,
        zip_package_created=True,
        public_url=SENTINEL_PUBLIC_URL,
        signed_url=SENTINEL_PUBLIC_URL,
        download_package_created=True,
        file_byte_route_created=True,
        external_delivery_performed=True,
        route_changed=True,
        api_route_added=True,
        frontend_integration_approved=True,
        b_end_report_runtime_generated=True,
        sandbox_public_event_generated=True,
        generated_response_text=True,
        public_route_created=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    candidate = build_dense_graph_report_candidate_from_integration(integration)
    encoded = _encoded(candidate)

    assert candidate["report_candidate_status"] == "blocked_requested_side_effect"
    assert candidate["report_candidate_created"] is False
    assert candidate["final_report_created"] is False
    assert candidate["b_end_report_runtime_generated"] is False
    assert candidate["sandbox_public_event_generated"] is False
    assert candidate["export_artifact_created"] is False
    assert candidate["generated_response_text"] is False
    assert candidate["public_route_created"] is False
    assert SENTINEL_PUBLIC_URL not in encoded
    _assert_false_side_effects(candidate)


def test_forbidden_values_block_or_do_not_leak() -> None:
    integration = _safe_integration(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
        response_text=SENTINEL_RESPONSE,
        public_url=SENTINEL_PUBLIC_URL,
    )

    candidate = build_dense_graph_report_candidate_from_integration(integration)
    encoded = _encoded(candidate)

    assert candidate["report_candidate_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert candidate["report_candidate_created"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert SENTINEL_RESPONSE not in encoded
    assert SENTINEL_PUBLIC_URL not in encoded
    assert "private-collector" not in encoded


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    integration = _safe_integration()

    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-10 report candidate smoke")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-10 report candidate smoke")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    candidate = build_dense_graph_report_candidate_from_integration(integration)
    encoded = _encoded(candidate)

    assert candidate["report_candidate_status"] == "candidate_ready"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert candidate["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert candidate["runtime_side_effects"]["read_original_package_rows"] is False


def test_no_export_final_report_route_or_public_delivery_fields_are_produced() -> None:
    candidate = build_dense_graph_report_candidate_from_integration(_safe_integration())
    keys = _walk_keys(candidate)

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
            "pdf_path",
            "markdown_report_path",
            "briefing_deck_path",
            "zip_path",
            "package_path",
            "public_url",
            "signed_url",
            "download_url",
            "file_byte_route",
        }
        & keys
    )
    assert candidate["final_report_created"] is False
    assert candidate["export_artifact_created"] is False
    assert candidate["public_route_created"] is False
    assert candidate["frontend_integration_approved"] is False
    assert candidate["route_ready"] is False
    assert candidate["frontend_ready"] is False
    assert candidate["production_ready"] is False
