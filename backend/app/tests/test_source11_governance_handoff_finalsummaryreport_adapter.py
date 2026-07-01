from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.final_report_boundary_source11_governance_handoff import (
    build_final_report_boundary_source11_governance_handoff,
)
from app.services.generated_run_dense_graph_bridge_integration import (
    integrate_generated_run_with_dense_graph_from_execution,
)
from app.services.minimum_real_run_bridge_execution import execute_minimum_real_run_from_bridge_candidate
from app.services.report_candidate_final_report_boundary import build_report_candidate_final_report_boundary
from app.services.source11_governance_handoff_finalsummaryreport_adapter import (
    build_safe_source11_governance_handoff_finalsummaryreport_adapter_summary,
    build_source11_governance_handoff_finalsummaryreport_adapter,
    create_source11_governance_handoff_finalsummaryreport_adapter,
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


def _safe_handoff(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    candidate = build_dense_graph_report_candidate_from_integration(integration)
    boundary = build_report_candidate_final_report_boundary(candidate)
    handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    handoff.update(overrides)
    return handoff


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


def _assert_runtime_side_effects_false_except_local_boundary(value: dict) -> None:
    assert value["runtime_side_effects"]
    for key, flag_value in value["runtime_side_effects"].items():
        if key == "created_local_final_summary_report_boundary":
            assert flag_value is True
        else:
            assert flag_value is False


def _assert_runtime_side_effects_false(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def _assert_downstream_flags_false(value: dict) -> None:
    for flag in (
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
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
    ):
        assert value[flag] is False


def test_ready_handoff_creates_local_finalsummaryreport_adapter_without_downstream_side_effects() -> None:
    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(
        _safe_handoff(),
        created_by="unit_test",
    )
    alias_adapter = create_source11_governance_handoff_finalsummaryreport_adapter(
        _safe_handoff(),
        created_by="unit_test",
    )
    summary = build_safe_source11_governance_handoff_finalsummaryreport_adapter_summary(adapter)

    assert adapter["adapter_schema"] == "sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1"
    assert adapter["adapter_status"] == "adapter_ready_with_local_finalsummaryreport_boundary"
    assert adapter["adapter_created"] is True
    assert adapter["input_source_kind"] == "source11_governance_handoff"
    assert adapter["adapter_mode"] == "backend_only_local_finalsummaryreport_runtime_adapter_smoke"
    assert adapter["source11_governance_handoff_schema"] == "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
    assert adapter["source11_governance_handoff_status"] == "handoff_ready_for_manual_source11_governance_review"
    assert adapter["final_report_boundary_schema"] == "sentigraph_report_candidate_final_report_boundary_v0_1"
    assert adapter["report_candidate_schema"] == "sentigraph_dense_graph_report_candidate_v0_1"
    assert adapter["dense_graph_integration_schema"] == "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
    assert adapter["generated_run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert adapter["human_review_status"] == "required"
    assert adapter["human_review_required"] is True
    assert adapter["final_summary_report_schema"] == "sentigraph_final_summary_report_v1"
    assert adapter["final_summary_report_status"] == "final_summary_report_created"
    assert adapter["final_summary_report_created"] is True
    assert adapter["final_summary_report_created_local_only"] is True
    assert adapter["local_final_summary_report_only"] is True
    assert adapter["source11_final_summary_report_runtime_used"] is True
    assert adapter["source11_runtime_called"] is False
    assert adapter["downstream_gates_required"] is True
    assert adapter["blockers"] == []
    _assert_downstream_flags_false(adapter)
    _assert_runtime_side_effects_false_except_local_boundary(adapter)

    local_report = adapter["local_final_summary_report"]
    assert local_report["schema"] == "sentigraph_final_summary_report_v1"
    assert local_report["status"] == "final_summary_report_created"
    assert local_report["local_only"] is True
    assert local_report["human_review_required"] is True
    assert local_report["source_and_scope"]["selected_sample_only"] is True
    assert local_report["report_sections"]
    assert local_report["boundary_block"]["not_full_web"] is True
    assert local_report["downstream_flags"]["export_ready"] is False
    assert local_report["downstream_flags"]["public_ready"] is False
    assert local_report["downstream_flags"]["b_end_ready"] is False
    assert local_report["downstream_flags"]["sandbox_ready"] is False
    assert local_report["required_next_gates"]["export_gate_required"] is True
    assert local_report["required_next_gates"]["public_access_gate_required"] is True

    assert alias_adapter["adapter_status"] == "adapter_ready_with_local_finalsummaryreport_boundary"
    assert summary["adapter_created"] is True
    assert summary["final_summary_report_created"] is True
    assert summary["final_summary_report_created_local_only"] is True
    assert summary["source11_runtime_called"] is False
    assert summary["export_ready"] is False
    assert summary["public_ready"] is False
    assert summary["customer_ready"] is False


def test_wrong_or_missing_source11_handoff_input_blocks_adapter() -> None:
    cases = (
        _safe_handoff(source11_governance_handoff_schema="unknown"),
        _safe_handoff(source11_governance_handoff_status="blocked_metadata_contract"),
        _safe_handoff(source11_governance_handoff_created=False),
        _safe_handoff(input_source_kind="unknown"),
        _safe_handoff(handoff_mode="unknown"),
        _safe_handoff(final_report_boundary_schema="unknown"),
        _safe_handoff(final_report_boundary_status="blocked_metadata_contract"),
        _safe_handoff(report_candidate_schema="unknown"),
        _safe_handoff(dense_graph_integration_schema="unknown"),
        _safe_handoff(generated_run_schema="unknown"),
        _safe_handoff(boundary_flags=None),
        _safe_handoff(runtime_side_effects=None),
        _safe_handoff(source11_governance_handoff_id=None),
    )

    for handoff in cases:
        adapter = build_source11_governance_handoff_finalsummaryreport_adapter(handoff)

        assert adapter["adapter_status"] == "blocked_metadata_contract"
        assert adapter["adapter_created"] is False
        assert adapter["final_summary_report_created"] is False
        assert adapter["source11_final_summary_report_runtime_used"] is False
        assert adapter["source11_runtime_called"] is False
        _assert_downstream_flags_false(adapter)
        _assert_runtime_side_effects_false(adapter)


def test_readiness_true_blocks_adapter_and_output_readiness_remains_false() -> None:
    for flag in (
        "source11_runtime_ready",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "public_ready",
        "customer_ready",
    ):
        adapter = build_source11_governance_handoff_finalsummaryreport_adapter(_safe_handoff(**{flag: True}))

        assert adapter["adapter_status"] in {
            "blocked_requested_side_effect",
            "blocked_source11_runtime_side_effect_risk",
        }
        assert adapter["adapter_created"] is False
        assert adapter["final_summary_report_created"] is False
        _assert_downstream_flags_false(adapter)
        _assert_runtime_side_effects_false(adapter)


def test_side_effect_requests_block_adapter_and_remain_false() -> None:
    handoff = _safe_handoff(
        source11_final_summary_report_runtime_used=True,
        source11_runtime_called=True,
        final_summary_report_created=True,
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

    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(handoff)

    assert adapter["adapter_status"] in {
        "blocked_requested_side_effect",
        "blocked_source11_runtime_side_effect_risk",
    }
    assert adapter["adapter_created"] is False
    assert adapter["final_summary_report_created"] is False
    assert adapter["source11_final_summary_report_runtime_used"] is False
    assert adapter["source11_runtime_called"] is False
    _assert_downstream_flags_false(adapter)
    _assert_runtime_side_effects_false(adapter)


def test_forbidden_values_block_or_do_not_leak() -> None:
    handoff = _safe_handoff(
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

    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(handoff)
    encoded = _encoded(adapter)

    assert adapter["adapter_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert adapter["adapter_created"] is False
    assert adapter["final_summary_report_created"] is False
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
    _assert_downstream_flags_false(adapter)
    _assert_runtime_side_effects_false(adapter)


def test_no_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    handoff = _safe_handoff()

    def fail_open(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-16 adapter smoke")

    def fail_read_text(*args, **kwargs):
        raise AssertionError("Path.read_text is not allowed in 8V-16 adapter smoke")

    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(Path, "read_text", fail_read_text)

    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(handoff)
    encoded = _encoded(adapter)

    assert adapter["adapter_status"] == "adapter_ready_with_local_finalsummaryreport_boundary"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert adapter["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert adapter["runtime_side_effects"]["read_original_package_rows"] is False


def test_no_export_route_frontend_public_delivery_or_response_fields_are_produced() -> None:
    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(_safe_handoff())
    keys = _walk_keys(adapter)

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
    assert adapter["source11_runtime_called"] is False
    assert adapter["final_report_created"] is False
    assert adapter["export_artifact_created"] is False
    assert adapter["download_package_created"] is False
    assert adapter["public_access_created"] is False
    assert adapter["external_delivery_performed"] is False
    assert adapter["public_route_created"] is False
    assert adapter["frontend_integration_approved"] is False
    assert adapter["route_ready"] is False
    assert adapter["frontend_ready"] is False
    assert adapter["production_ready"] is False
