from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.final_report_boundary_source11_governance_handoff import (
    build_final_report_boundary_source11_governance_handoff,
    build_safe_final_report_boundary_source11_governance_handoff_summary,
    create_final_report_boundary_source11_governance_handoff,
)
from app.services.generated_run_dense_graph_bridge_integration import (
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.report_candidate_final_report_boundary import build_report_candidate_final_report_boundary
from app.services.staging_candidate_generated_run_bridge import build_staging_candidate_generated_run_bridge


SENTINEL_TOKEN = "actual-token-should-never-appear"
SENTINEL_AUTHOR = "actual-author-name-should-never-appear"
SENTINEL_PROFILE = "actual-profile-url-should-never-appear"
SENTINEL_RAW_ROW = "actual-raw-row-should-never-appear"
SENTINEL_PATH = "G:/private-collector/should-never-appear"
SENTINEL_RESPONSE = "actual-response-text-should-never-appear"
SENTINEL_PUBLIC_URL = "public-download-url-should-never-appear"
SENTINEL_SIGNED_URL = "signed-download-url-should-never-appear"
SENTINEL_EXTERNAL_TARGET = "external-delivery-target-should-never-appear"


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


def _safe_final_report_boundary(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    candidate = build_dense_graph_report_candidate_from_integration(integration)
    boundary = build_report_candidate_final_report_boundary(candidate)
    boundary.update(overrides)
    return boundary


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


def _assert_runtime_side_effects_false(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def _assert_output_side_effect_flags_false(value: dict) -> None:
    for flag in (
        "source11_final_summary_report_runtime_used",
        "source11_runtime_called",
        "final_summary_report_created",
        "final_report_created",
        "b_end_report_runtime_generated",
        "sandbox_public_event_generated",
        "export_artifact_created",
        "download_package_created",
        "public_access_created",
        "external_delivery_performed",
        "generated_response_text",
        "public_route_created",
        "frontend_integration_approved",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "public_ready",
        "customer_ready",
    ):
        assert value[flag] is False


def _assert_downstream_policy_false(value: dict) -> None:
    policy = value["downstream_policy"]
    assert policy["source11_manual_review_ready"] is value["source11_governance_handoff_created"]
    for flag in (
        "source11_runtime_ready",
        "final_summary_report_ready",
        "export_ready",
        "download_ready",
        "public_access_ready",
        "external_delivery_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
        "frontend_ready",
        "route_ready",
        "production_ready",
        "customer_ready",
    ):
        assert policy[flag] is False


def test_ready_boundary_creates_source11_governance_handoff_without_downstream_side_effects() -> None:
    handoff = build_final_report_boundary_source11_governance_handoff(
        _safe_final_report_boundary(),
        created_by="unit_test",
    )
    alias_handoff = create_final_report_boundary_source11_governance_handoff(
        _safe_final_report_boundary(),
        created_by="unit_test",
    )
    summary = build_safe_final_report_boundary_source11_governance_handoff_summary(handoff)

    assert (
        handoff["source11_governance_handoff_schema"]
        == "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
    )
    assert handoff["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert handoff["source11_governance_handoff_created"] is True
    assert handoff["input_source_kind"] == "final_report_boundary"
    assert handoff["handoff_mode"] == "backend_only_local_source11_governance_handoff"
    assert handoff["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert handoff["final_report_boundary_status"] == "boundary_ready"
    assert handoff["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert handoff["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert handoff["generated_run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert handoff["human_review_status"] == "required"
    assert handoff["human_review_required"] is True
    assert handoff["boundary_flags"]["source11_runtime_not_used"] is True
    assert handoff["boundary_flags"]["not_final_summary_report"] is True
    assert handoff["boundary_flags"]["not_export_ready"] is True
    assert handoff["boundary_flags"]["not_public_ready"] is True
    assert handoff["boundary_flags"]["not_customer_ready"] is True
    assert handoff["boundary_flags"]["not_production_ready"] is True
    assert handoff["final_report_boundary_summary"]
    assert handoff["source11_governance_review_summary"]["manual_review_required"] is True
    assert handoff["source11_compatibility_notes"]
    assert handoff["governance_handoff_limitations"]
    assert handoff["blockers"] == []
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false(handoff)
    _assert_downstream_policy_false(handoff)

    assert alias_handoff["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert summary["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert summary["source11_governance_handoff_created"] is True
    assert summary["source11_manual_review_ready"] is True
    assert summary["source11_runtime_ready"] is False
    assert summary["final_summary_report_created"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False
    assert summary["customer_ready"] is False


def test_wrong_or_missing_final_report_boundary_input_blocks_handoff() -> None:
    cases = (
        _safe_final_report_boundary(final_report_boundary_schema="unknown"),
        _safe_final_report_boundary(final_report_boundary_status="blocked_metadata_contract"),
        _safe_final_report_boundary(input_source_kind="unknown"),
        _safe_final_report_boundary(boundary_mode="unknown"),
        _safe_final_report_boundary(final_report_boundary_created=False),
        _safe_final_report_boundary(report_candidate_schema="unknown"),
        _safe_final_report_boundary(report_candidate_status="blocked_metadata_contract"),
        _safe_final_report_boundary(dense_graph_integration_schema="unknown"),
        _safe_final_report_boundary(generated_run_schema="unknown"),
        _safe_final_report_boundary(final_report_boundary_summary=None),
        _safe_final_report_boundary(boundary_flags=None),
        _safe_final_report_boundary(runtime_side_effects=None),
    )

    for boundary in cases:
        handoff = build_final_report_boundary_source11_governance_handoff(boundary)

        assert handoff["source11_governance_handoff_status"] == "blocked_metadata_contract"
        assert handoff["source11_governance_handoff_created"] is False
        _assert_output_side_effect_flags_false(handoff)
        _assert_runtime_side_effects_false(handoff)
        _assert_downstream_policy_false(handoff)


def test_readiness_true_blocks_handoff_and_output_readiness_remains_false() -> None:
    for flag in ("route_ready", "frontend_ready", "production_ready", "export_ready", "public_ready", "customer_ready"):
        handoff = build_final_report_boundary_source11_governance_handoff(
            _safe_final_report_boundary(**{flag: True})
        )

        assert handoff["source11_governance_handoff_status"] == "blocked_requested_side_effect"
        assert handoff["source11_governance_handoff_created"] is False
        _assert_output_side_effect_flags_false(handoff)
        _assert_runtime_side_effects_false(handoff)
        _assert_downstream_policy_false(handoff)


def test_source11_runtime_request_blocks_handoff_and_remains_false() -> None:
    handoff = build_final_report_boundary_source11_governance_handoff(
        _safe_final_report_boundary(
            source11_final_summary_report_runtime_used=True,
            source11_runtime_called=True,
            final_summary_report_created=True,
            create_final_summary_report=True,
        )
    )

    assert handoff["source11_governance_handoff_status"] == "blocked_source11_runtime_request"
    assert handoff["source11_governance_handoff_created"] is False
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false(handoff)


def test_downstream_side_effect_requests_block_handoff_and_remain_false() -> None:
    boundary = _safe_final_report_boundary(
        final_report_created=True,
        b_end_report_runtime_generated=True,
        sandbox_public_event_generated=True,
        export_artifact_created=True,
        download_package_created=True,
        public_access_created=True,
        external_delivery_performed=True,
        generated_response_text=True,
        public_route_created=True,
        route_changed=True,
        api_route_added=True,
        frontend_integration_approved=True,
        route_ready=True,
        frontend_ready=True,
        production_ready=True,
        export_ready=True,
        public_ready=True,
        customer_ready=True,
        evidence_layer_write=True,
        production_case_created=True,
        production_analysis_run_created=True,
        evidence_rows_parsed=True,
        called_real_api=True,
        called_real_llm=True,
        ran_collector=True,
        fetched_url=True,
        scraped_page=True,
        auto_execute=True,
        publish_now=True,
        send_now=True,
        post_now=True,
        execute_now=True,
    )

    handoff = build_final_report_boundary_source11_governance_handoff(boundary)

    assert handoff["source11_governance_handoff_status"] == "blocked_requested_side_effect"
    assert handoff["source11_governance_handoff_created"] is False
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false(handoff)


def test_forbidden_values_block_or_do_not_leak() -> None:
    boundary = _safe_final_report_boundary(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
        response_text=SENTINEL_RESPONSE,
        public_url=SENTINEL_PUBLIC_URL,
        signed_url=SENTINEL_SIGNED_URL,
        external_delivery_target=SENTINEL_EXTERNAL_TARGET,
    )

    handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    encoded = _encoded(handoff)

    assert handoff["source11_governance_handoff_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert handoff["source11_governance_handoff_created"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert SENTINEL_RESPONSE not in encoded
    assert SENTINEL_PUBLIC_URL not in encoded
    assert SENTINEL_SIGNED_URL not in encoded
    assert SENTINEL_EXTERNAL_TARGET not in encoded
    assert "private-collector" not in encoded
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false(handoff)


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    boundary = _safe_final_report_boundary()

    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-14 Source 11 governance handoff smoke")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-14 Source 11 governance handoff smoke")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    encoded = _encoded(handoff)

    assert handoff["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert handoff["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert handoff["runtime_side_effects"]["read_original_package_rows"] is False


def test_no_source11_export_route_or_public_delivery_fields_are_produced() -> None:
    handoff = build_final_report_boundary_source11_governance_handoff(_safe_final_report_boundary())
    keys = _walk_keys(handoff)

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
            "source11_final_summary_report_id",
            "final_summary_report_id",
        }
        & keys
    )
    assert handoff["source11_final_summary_report_runtime_used"] is False
    assert handoff["source11_runtime_called"] is False
    assert handoff["final_summary_report_created"] is False
    assert handoff["final_report_created"] is False
    assert handoff["export_artifact_created"] is False
    assert handoff["download_package_created"] is False
    assert handoff["public_access_created"] is False
    assert handoff["external_delivery_performed"] is False
    assert handoff["public_route_created"] is False
    assert handoff["frontend_integration_approved"] is False
    assert handoff["route_ready"] is False
    assert handoff["frontend_ready"] is False
    assert handoff["production_ready"] is False
