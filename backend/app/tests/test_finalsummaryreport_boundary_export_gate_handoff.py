from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.final_report_boundary_source11_governance_handoff import (
    build_final_report_boundary_source11_governance_handoff,
)
from app.services.finalsummaryreport_boundary_export_gate_handoff import (
    build_finalsummaryreport_boundary_export_gate_handoff,
    build_safe_finalsummaryreport_boundary_export_gate_handoff_summary,
    create_finalsummaryreport_boundary_export_gate_handoff,
)
from app.services.generated_run_dense_graph_bridge_integration import (
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.report_candidate_final_report_boundary import build_report_candidate_final_report_boundary
from app.services.source11_governance_handoff_finalsummaryreport_adapter import (
    build_source11_governance_handoff_finalsummaryreport_adapter,
)
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


def _safe_adapter(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    candidate = build_dense_graph_report_candidate_from_integration(integration)
    boundary = build_report_candidate_final_report_boundary(candidate)
    handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(handoff)
    adapter.update(overrides)
    return adapter


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


def _assert_runtime_side_effects_false_except_local_handoff(value: dict) -> None:
    assert value["runtime_side_effects"]
    for key, flag_value in value["runtime_side_effects"].items():
        if key == "created_local_export_gate_handoff":
            assert flag_value is True
        else:
            assert flag_value is False


def _assert_runtime_side_effects_false(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def _assert_output_side_effect_flags_false(value: dict) -> None:
    for flag in (
        "export_gate_runtime_used",
        "called_export_gate_runtime",
        "export_gate_created",
        "export_artifact_created",
        "download_package_created",
        "public_access_created",
        "external_delivery_performed",
        "b_end_report_runtime_generated",
        "sandbox_public_event_generated",
        "generated_response_text",
        "public_route_created",
        "frontend_integration_approved",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "public_ready",
        "customer_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
    ):
        assert value[flag] is False


def test_ready_adapter_creates_export_gate_handoff_without_export_or_delivery_side_effects() -> None:
    handoff = build_finalsummaryreport_boundary_export_gate_handoff(
        _safe_adapter(),
        created_by="unit_test",
    )
    alias_handoff = create_finalsummaryreport_boundary_export_gate_handoff(
        _safe_adapter(),
        created_by="unit_test",
    )
    summary = build_safe_finalsummaryreport_boundary_export_gate_handoff_summary(handoff)

    assert handoff["export_gate_handoff_schema"] == "sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1"
    assert handoff["export_gate_handoff_status"] == "export_gate_handoff_ready_for_manual_review"
    assert handoff["export_gate_handoff_created"] is True
    assert handoff["created_local_export_gate_handoff"] is True
    assert handoff["input_source_kind"] == "finalsummaryreport_boundary_adapter"
    assert handoff["handoff_mode"] == "backend_only_local_export_gate_handoff_readiness_smoke"
    assert handoff["adapter_schema"] == "sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1"
    assert handoff["adapter_status"] == "adapter_ready_with_local_finalsummaryreport_boundary"
    assert handoff["final_summary_report_schema"] == "sentigraph_final_summary_report_v1"
    assert handoff["final_summary_report_created"] is True
    assert handoff["final_summary_report_created_local_only"] is True
    assert handoff["local_final_summary_report_only"] is True
    assert handoff["human_review_status"] == "required"
    assert handoff["human_review_required"] is True
    assert handoff["blockers"] == []
    assert handoff["export_gate_readiness_summary"]["eligible_for_later_manual_export_gate_review"] is True
    assert handoff["export_gate_readiness_summary"]["export_gate_runtime_used"] is False
    assert handoff["boundary_flags"]["export_gate_handoff_only"] is True
    assert handoff["boundary_flags"]["export_runtime_not_used"] is True
    assert handoff["boundary_flags"]["export_artifact_not_created"] is True
    assert handoff["boundary_flags"]["download_package_not_created"] is True
    assert handoff["boundary_flags"]["public_access_not_created"] is True
    assert handoff["boundary_flags"]["external_delivery_not_performed"] is True
    assert handoff["boundary_flags"]["downstream_gates_required"] is True
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false_except_local_handoff(handoff)

    assert alias_handoff["export_gate_handoff_status"] == "export_gate_handoff_ready_for_manual_review"
    assert summary["export_gate_handoff_created"] is True
    assert summary["created_local_export_gate_handoff"] is True
    assert summary["export_gate_runtime_used"] is False
    assert summary["export_artifact_created"] is False
    assert summary["download_package_created"] is False
    assert summary["public_access_created"] is False
    assert summary["external_delivery_performed"] is False


def test_wrong_or_missing_adapter_input_blocks_handoff() -> None:
    cases = (
        _safe_adapter(adapter_id=None),
        _safe_adapter(adapter_schema="unknown"),
        _safe_adapter(adapter_status="blocked_metadata_contract"),
        _safe_adapter(adapter_created=False),
        _safe_adapter(adapter_mode="unknown"),
        _safe_adapter(input_source_kind="unknown"),
        _safe_adapter(final_summary_report_schema="unknown"),
        _safe_adapter(final_summary_report_created=False),
        _safe_adapter(final_summary_report_created_local_only=False),
        _safe_adapter(local_final_summary_report_only=False),
        _safe_adapter(local_final_summary_report=None),
        _safe_adapter(boundary_flags=None),
        _safe_adapter(runtime_side_effects=None),
    )

    for adapter in cases:
        handoff = build_finalsummaryreport_boundary_export_gate_handoff(adapter)

        assert handoff["export_gate_handoff_status"] == "blocked_metadata_contract"
        assert handoff["export_gate_handoff_created"] is False
        assert handoff["created_local_export_gate_handoff"] is False
        _assert_output_side_effect_flags_false(handoff)
        _assert_runtime_side_effects_false(handoff)


def test_readiness_true_blocks_handoff_and_output_readiness_remains_false() -> None:
    for flag in (
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "public_ready",
        "customer_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
    ):
        handoff = build_finalsummaryreport_boundary_export_gate_handoff(_safe_adapter(**{flag: True}))

        assert handoff["export_gate_handoff_status"] == "blocked_requested_side_effect"
        assert handoff["export_gate_handoff_created"] is False
        assert handoff["created_local_export_gate_handoff"] is False
        _assert_output_side_effect_flags_false(handoff)
        _assert_runtime_side_effects_false(handoff)


def test_export_file_delivery_and_runtime_side_effect_requests_block_handoff() -> None:
    adapter = _safe_adapter(
        export_gate_runtime_used=True,
        called_export_gate_runtime=True,
        export_gate_created=True,
        export_artifact_created=True,
        generated_export_artifact=True,
        generated_markdown_file=True,
        generated_pdf_file=True,
        generated_briefing_deck=True,
        generated_evidence_appendix_package=True,
        download_package_created=True,
        generated_download_package=True,
        generated_zip_package=True,
        public_access_created=True,
        generated_public_access=True,
        external_delivery_performed=True,
        performed_external_delivery=True,
        b_end_report_runtime_generated=True,
        sandbox_public_event_generated=True,
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

    handoff = build_finalsummaryreport_boundary_export_gate_handoff(adapter)

    assert handoff["export_gate_handoff_status"] in {
        "blocked_requested_side_effect",
        "blocked_export_runtime_side_effect_risk",
    }
    assert handoff["export_gate_handoff_created"] is False
    assert handoff["created_local_export_gate_handoff"] is False
    _assert_output_side_effect_flags_false(handoff)
    _assert_runtime_side_effects_false(handoff)


def test_forbidden_values_block_or_do_not_leak() -> None:
    adapter = _safe_adapter(
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

    handoff = build_finalsummaryreport_boundary_export_gate_handoff(adapter)
    encoded = _encoded(handoff)

    assert handoff["export_gate_handoff_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert handoff["export_gate_handoff_created"] is False
    assert handoff["created_local_export_gate_handoff"] is False
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


def test_no_file_generation_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    adapter = _safe_adapter()

    def fail_file_access(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-18 export-gate handoff smoke")

    monkeypatch.setattr(builtins, "open", fail_file_access)
    monkeypatch.setattr(Path, "read_text", fail_file_access)
    monkeypatch.setattr(Path, "write_text", fail_file_access)
    monkeypatch.setattr(Path, "touch", fail_file_access)
    monkeypatch.setattr(Path, "mkdir", fail_file_access)

    handoff = build_finalsummaryreport_boundary_export_gate_handoff(adapter)
    encoded = _encoded(handoff)

    assert handoff["export_gate_handoff_status"] == "export_gate_handoff_ready_for_manual_review"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert handoff["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert handoff["runtime_side_effects"]["read_original_package_rows"] is False
    assert handoff["runtime_side_effects"]["generated_markdown_file"] is False
    assert handoff["runtime_side_effects"]["generated_pdf_file"] is False
    assert handoff["runtime_side_effects"]["generated_briefing_deck"] is False
    assert handoff["runtime_side_effects"]["generated_zip_package"] is False
    assert handoff["runtime_side_effects"]["generated_download_package"] is False


def test_no_export_route_frontend_public_delivery_or_file_fields_are_produced() -> None:
    handoff = build_finalsummaryreport_boundary_export_gate_handoff(_safe_adapter())
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
        }
        & keys
    )
    assert handoff["export_gate_runtime_used"] is False
    assert handoff["called_export_gate_runtime"] is False
    assert handoff["export_gate_created"] is False
    assert handoff["export_artifact_created"] is False
    assert handoff["download_package_created"] is False
    assert handoff["public_access_created"] is False
    assert handoff["external_delivery_performed"] is False
    assert handoff["public_route_created"] is False
    assert handoff["frontend_integration_approved"] is False
    assert handoff["route_ready"] is False
    assert handoff["frontend_ready"] is False
    assert handoff["production_ready"] is False
