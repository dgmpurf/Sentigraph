from __future__ import annotations

import builtins
import json
from pathlib import Path

from app.services.dense_graph_report_candidate_bridge import build_dense_graph_report_candidate_from_integration
from app.services.download_public_access_boundary_final_delivery_boundary import (
    build_download_public_access_boundary_final_delivery_boundary,
    build_safe_download_public_access_boundary_final_delivery_boundary_summary,
    create_download_public_access_boundary_final_delivery_boundary,
)
from app.services.export_artifact_boundary_download_public_access_boundary import (
    build_export_artifact_boundary_download_public_access_boundary,
)
from app.services.export_gate_handoff_export_artifact_boundary import (
    build_export_gate_handoff_export_artifact_boundary,
)
from app.services.final_report_boundary_source11_governance_handoff import (
    build_final_report_boundary_source11_governance_handoff,
)
from app.services.finalsummaryreport_boundary_export_gate_handoff import (
    build_finalsummaryreport_boundary_export_gate_handoff,
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
SENTINEL_MARKDOWN_PATH = "G:/runtime/report.md"
SENTINEL_PDF_PATH = "G:/runtime/report.pdf"
SENTINEL_ZIP_PATH = "G:/runtime/report.zip"
SENTINEL_DOWNLOAD_PATH = "G:/runtime/download-package.zip"
SENTINEL_PUBLIC_URL = "public-download-url-should-never-appear"
SENTINEL_SIGNED_URL = "signed-download-url-should-never-appear"
SENTINEL_FILE_ROUTE = "/api/v1/download/should-never-appear"
SENTINEL_EXTERNAL_TARGET = "external-delivery-target-should-never-appear"
SENTINEL_OBJECT_STORAGE_TARGET = "object-storage-target-should-never-appear"
SENTINEL_EMAIL_TARGET = "email-target-should-never-appear"
SENTINEL_PORTAL_TARGET = "portal-target-should-never-appear"
SENTINEL_CUSTOMER_TARGET = "customer-delivery-target-should-never-appear"


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


def _safe_download_public_access_boundary(**overrides) -> dict:
    bridge = build_staging_candidate_generated_run_bridge(_safe_staging_summary())
    execution = execute_minimum_real_run_from_bridge_candidate(bridge)
    integration = integrate_generated_run_with_dense_graph_from_execution(execution)
    candidate = build_dense_graph_report_candidate_from_integration(integration)
    boundary = build_report_candidate_final_report_boundary(candidate)
    source11_handoff = build_final_report_boundary_source11_governance_handoff(boundary)
    adapter = build_source11_governance_handoff_finalsummaryreport_adapter(source11_handoff)
    handoff = build_finalsummaryreport_boundary_export_gate_handoff(adapter)
    artifact_boundary = build_export_gate_handoff_export_artifact_boundary(handoff)
    download_boundary = build_export_artifact_boundary_download_public_access_boundary(artifact_boundary)
    download_boundary.update(overrides)
    return download_boundary


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
        if key == "created_local_final_delivery_boundary":
            assert flag_value is True
        else:
            assert flag_value is False


def _assert_runtime_side_effects_false(value: dict) -> None:
    assert value["runtime_side_effects"]
    assert all(flag_value is False for flag_value in value["runtime_side_effects"].values())


def _assert_output_side_effect_flags_false(value: dict) -> None:
    for flag in (
        "final_delivery_runtime_used",
        "called_final_delivery_runtime",
        "final_delivery_performed",
        "customer_delivery_created",
        "public_access_runtime_used",
        "called_public_access_runtime",
        "external_delivery_runtime_used",
        "called_external_delivery_runtime",
        "download_package_runtime_used",
        "called_download_package_runtime",
        "download_package_created",
        "generated_zip_package",
        "public_url_created",
        "signed_url_created",
        "public_access_created",
        "external_delivery_performed",
        "file_byte_route_created",
        "object_storage_uploaded",
        "email_sent",
        "portal_published",
        "b_end_report_runtime_generated",
        "sandbox_public_event_generated",
        "generated_response_text",
        "public_route_created",
        "frontend_integration_approved",
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "download_ready",
        "public_ready",
        "public_access_ready",
        "external_delivery_ready",
        "customer_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
    ):
        assert value[flag] is False


def test_ready_download_public_access_boundary_creates_final_delivery_boundary_without_runtime_or_delivery_side_effects() -> None:
    boundary = build_download_public_access_boundary_final_delivery_boundary(
        _safe_download_public_access_boundary(),
        created_by="unit_test",
    )
    alias_boundary = create_download_public_access_boundary_final_delivery_boundary(
        _safe_download_public_access_boundary(),
        created_by="unit_test",
    )
    summary = build_safe_download_public_access_boundary_final_delivery_boundary_summary(boundary)

    assert boundary["final_delivery_boundary_schema"] == (
        "sentigraph_download_public_access_boundary_final_delivery_boundary_v0_1"
    )
    assert boundary["final_delivery_boundary_status"] == "final_delivery_boundary_ready_for_manual_review"
    assert boundary["final_delivery_boundary_created"] is True
    assert boundary["created_local_final_delivery_boundary"] is True
    assert boundary["input_source_kind"] == "download_public_access_boundary"
    assert boundary["boundary_mode"] == "backend_only_local_final_delivery_boundary_readiness_smoke"
    assert boundary["download_public_access_boundary_schema"] == (
        "sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1"
    )
    assert boundary["download_public_access_boundary_status"] == (
        "download_public_access_boundary_ready_for_manual_review"
    )
    assert boundary["download_public_access_boundary_created"] is True
    assert boundary["created_local_download_public_access_boundary"] is True
    assert boundary["export_artifact_boundary_schema"] == "sentigraph_export_gate_handoff_export_artifact_boundary_v0_1"
    assert boundary["export_artifact_boundary_status"] == "export_artifact_boundary_ready_for_manual_review"
    assert boundary["export_artifact_boundary_created"] is True
    assert boundary["created_local_export_artifact_boundary"] is True
    assert boundary["export_gate_handoff_schema"] == "sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1"
    assert boundary["export_gate_handoff_status"] == "export_gate_handoff_ready_for_manual_review"
    assert boundary["export_gate_handoff_created"] is True
    assert boundary["created_local_export_gate_handoff"] is True
    assert boundary["final_summary_report_created"] is True
    assert boundary["final_summary_report_created_local_only"] is True
    assert boundary["local_final_summary_report_only"] is True
    assert boundary["human_review_status"] == "required"
    assert boundary["human_review_required"] is True
    assert boundary["blockers"] == []
    assert boundary["final_delivery_boundary_readiness_summary"][
        "eligible_for_later_manual_final_delivery_runtime_review"
    ] is True
    assert boundary["final_delivery_boundary_readiness_summary"]["final_delivery_runtime_used"] is False
    assert boundary["final_delivery_boundary_readiness_summary"]["customer_delivery_created"] is False
    assert boundary["final_delivery_boundary_readiness_summary"]["public_access_runtime_used"] is False
    assert boundary["final_delivery_boundary_readiness_summary"]["external_delivery_runtime_used"] is False
    assert boundary["boundary_flags"]["final_delivery_boundary_only"] is True
    assert boundary["boundary_flags"]["final_delivery_runtime_not_used"] is True
    assert boundary["boundary_flags"]["final_delivery_not_performed"] is True
    assert boundary["boundary_flags"]["customer_delivery_not_created"] is True
    assert boundary["boundary_flags"]["object_storage_not_uploaded"] is True
    assert boundary["boundary_flags"]["email_not_sent"] is True
    assert boundary["boundary_flags"]["portal_not_published"] is True
    _assert_output_side_effect_flags_false(boundary)
    _assert_runtime_side_effects_false_except_local_boundary(boundary)

    assert alias_boundary["final_delivery_boundary_status"] == "final_delivery_boundary_ready_for_manual_review"
    assert summary["final_delivery_boundary_created"] is True
    assert summary["created_local_final_delivery_boundary"] is True
    assert summary["final_delivery_runtime_used"] is False
    assert summary["public_access_runtime_used"] is False
    assert summary["external_delivery_runtime_used"] is False
    assert summary["download_package_runtime_used"] is False
    assert summary["customer_delivery_created"] is False


def test_wrong_or_missing_download_public_access_boundary_input_blocks_boundary() -> None:
    cases = (
        _safe_download_public_access_boundary(download_public_access_boundary_id=None),
        _safe_download_public_access_boundary(download_public_access_boundary_schema="unknown"),
        _safe_download_public_access_boundary(download_public_access_boundary_status="blocked_metadata_contract"),
        _safe_download_public_access_boundary(download_public_access_boundary_created=False),
        _safe_download_public_access_boundary(created_local_download_public_access_boundary=False),
        _safe_download_public_access_boundary(input_source_kind="unknown"),
        _safe_download_public_access_boundary(boundary_mode="unknown"),
        _safe_download_public_access_boundary(export_artifact_boundary_summary=None),
        _safe_download_public_access_boundary(download_public_access_boundary_readiness_summary=None),
        _safe_download_public_access_boundary(boundary_flags=None),
        _safe_download_public_access_boundary(runtime_side_effects=None),
    )

    for download_boundary in cases:
        boundary = build_download_public_access_boundary_final_delivery_boundary(download_boundary)

        assert boundary["final_delivery_boundary_status"] == "blocked_metadata_contract"
        assert boundary["final_delivery_boundary_created"] is False
        assert boundary["created_local_final_delivery_boundary"] is False
        _assert_output_side_effect_flags_false(boundary)
        _assert_runtime_side_effects_false(boundary)


def test_readiness_true_blocks_boundary_and_output_readiness_remains_false() -> None:
    for flag in (
        "route_ready",
        "frontend_ready",
        "production_ready",
        "export_ready",
        "download_ready",
        "public_ready",
        "public_access_ready",
        "external_delivery_ready",
        "customer_ready",
        "b_end_ready",
        "sandbox_ready",
        "public_event_ready",
    ):
        boundary = build_download_public_access_boundary_final_delivery_boundary(
            _safe_download_public_access_boundary(**{flag: True})
        )

        assert boundary["final_delivery_boundary_status"] == "blocked_requested_side_effect"
        assert boundary["final_delivery_boundary_created"] is False
        assert boundary["created_local_final_delivery_boundary"] is False
        _assert_output_side_effect_flags_false(boundary)
        _assert_runtime_side_effects_false(boundary)


def test_final_delivery_public_access_file_delivery_and_runtime_side_effect_requests_block_boundary() -> None:
    download_boundary = _safe_download_public_access_boundary(
        final_delivery_runtime_used=True,
        called_final_delivery_runtime=True,
        final_delivery_performed=True,
        customer_delivery_created=True,
        download_package_runtime_used=True,
        called_download_package_runtime=True,
        public_access_runtime_used=True,
        called_public_access_runtime=True,
        external_delivery_runtime_used=True,
        called_external_delivery_runtime=True,
        download_package_created=True,
        generated_download_package=True,
        generated_zip_package=True,
        public_url_created=True,
        signed_url_created=True,
        generated_public_url=True,
        generated_signed_url=True,
        public_access_created=True,
        generated_public_access=True,
        external_delivery_performed=True,
        performed_external_delivery=True,
        file_byte_route_created=True,
        created_file_byte_route=True,
        object_storage_uploaded=True,
        uploaded_object_storage=True,
        email_sent=True,
        sent_email=True,
        portal_published=True,
        published_to_portal=True,
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

    boundary = build_download_public_access_boundary_final_delivery_boundary(download_boundary)

    assert boundary["final_delivery_boundary_status"] in {
        "blocked_requested_side_effect",
        "blocked_final_delivery_runtime_side_effect_risk",
    }
    assert boundary["final_delivery_boundary_created"] is False
    assert boundary["created_local_final_delivery_boundary"] is False
    _assert_output_side_effect_flags_false(boundary)
    _assert_runtime_side_effects_false(boundary)


def test_forbidden_values_block_or_do_not_leak() -> None:
    download_boundary = _safe_download_public_access_boundary(
        token=SENTINEL_TOKEN,
        raw_author_name=SENTINEL_AUTHOR,
        profile_url=SENTINEL_PROFILE,
        full_evidence_rows=[SENTINEL_RAW_ROW],
        absolute_package_path=SENTINEL_PATH,
        response_text=SENTINEL_RESPONSE,
        markdown_report_path=SENTINEL_MARKDOWN_PATH,
        pdf_path=SENTINEL_PDF_PATH,
        zip_path=SENTINEL_ZIP_PATH,
        download_package_path=SENTINEL_DOWNLOAD_PATH,
        public_url=SENTINEL_PUBLIC_URL,
        signed_url=SENTINEL_SIGNED_URL,
        file_byte_route=SENTINEL_FILE_ROUTE,
        external_delivery_target=SENTINEL_EXTERNAL_TARGET,
        object_storage_target=SENTINEL_OBJECT_STORAGE_TARGET,
        email_delivery_target=SENTINEL_EMAIL_TARGET,
        portal_publication_target=SENTINEL_PORTAL_TARGET,
        customer_delivery_target=SENTINEL_CUSTOMER_TARGET,
    )

    boundary = build_download_public_access_boundary_final_delivery_boundary(download_boundary)
    encoded = _encoded(boundary)

    assert boundary["final_delivery_boundary_status"] in {"blocked_privacy_issue", "blocked_forbidden_input"}
    assert boundary["final_delivery_boundary_created"] is False
    assert boundary["created_local_final_delivery_boundary"] is False
    assert SENTINEL_TOKEN not in encoded
    assert SENTINEL_AUTHOR not in encoded
    assert SENTINEL_PROFILE not in encoded
    assert SENTINEL_RAW_ROW not in encoded
    assert SENTINEL_PATH not in encoded
    assert SENTINEL_RESPONSE not in encoded
    assert SENTINEL_MARKDOWN_PATH not in encoded
    assert SENTINEL_PDF_PATH not in encoded
    assert SENTINEL_ZIP_PATH not in encoded
    assert SENTINEL_DOWNLOAD_PATH not in encoded
    assert SENTINEL_PUBLIC_URL not in encoded
    assert SENTINEL_SIGNED_URL not in encoded
    assert SENTINEL_FILE_ROUTE not in encoded
    assert SENTINEL_EXTERNAL_TARGET not in encoded
    assert SENTINEL_OBJECT_STORAGE_TARGET not in encoded
    assert SENTINEL_EMAIL_TARGET not in encoded
    assert SENTINEL_PORTAL_TARGET not in encoded
    assert SENTINEL_CUSTOMER_TARGET not in encoded
    assert "private-collector" not in encoded
    _assert_output_side_effect_flags_false(boundary)
    _assert_runtime_side_effects_false(boundary)


def test_no_file_generation_package_files_or_evidence_rows_are_accessed(monkeypatch) -> None:
    download_boundary = _safe_download_public_access_boundary()

    def fail_file_access(*args, **kwargs):
        raise AssertionError("file access is not allowed in 8V-24 final-delivery boundary smoke")

    monkeypatch.setattr(builtins, "open", fail_file_access)
    monkeypatch.setattr(Path, "read_text", fail_file_access)
    monkeypatch.setattr(Path, "write_text", fail_file_access)
    monkeypatch.setattr(Path, "touch", fail_file_access)
    monkeypatch.setattr(Path, "mkdir", fail_file_access)

    boundary = build_download_public_access_boundary_final_delivery_boundary(download_boundary)
    encoded = _encoded(boundary)

    assert boundary["final_delivery_boundary_status"] == "final_delivery_boundary_ready_for_manual_review"
    assert "evidence_items.jsonl" not in encoded
    assert "evidence_items.csv" not in encoded
    assert boundary["runtime_side_effects"]["parsed_evidence_items_file"] is False
    assert boundary["runtime_side_effects"]["read_original_package_rows"] is False
    assert boundary["runtime_side_effects"]["generated_download_package"] is False
    assert boundary["runtime_side_effects"]["generated_zip_package"] is False
    assert boundary["runtime_side_effects"]["generated_public_access"] is False
    assert boundary["runtime_side_effects"]["performed_external_delivery"] is False
    assert boundary["runtime_side_effects"]["performed_final_delivery"] is False
    assert boundary["runtime_side_effects"]["created_customer_delivery"] is False
    assert boundary["runtime_side_effects"]["created_file_byte_route"] is False
    assert boundary["runtime_side_effects"]["generated_public_url"] is False
    assert boundary["runtime_side_effects"]["generated_signed_url"] is False
    assert boundary["runtime_side_effects"]["uploaded_object_storage"] is False
    assert boundary["runtime_side_effects"]["sent_email"] is False
    assert boundary["runtime_side_effects"]["published_to_portal"] is False


def test_no_final_delivery_public_access_route_frontend_or_file_fields_are_produced() -> None:
    boundary = build_download_public_access_boundary_final_delivery_boundary(_safe_download_public_access_boundary())
    keys = _walk_keys(boundary)

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
            "evidence_appendix_package_path",
            "zip_path",
            "download_package_path",
            "package_path",
            "runtime_path",
            "local_runtime_path",
            "public_url",
            "signed_url",
            "download_url",
            "file_byte_route",
            "external_delivery_target",
            "object_storage_target",
            "email_delivery_target",
            "portal_publication_target",
            "customer_delivery_target",
        }
        & keys
    )
    _assert_output_side_effect_flags_false(boundary)
    assert boundary["runtime_side_effects"]["called_final_delivery_runtime"] is False
    assert boundary["runtime_side_effects"]["performed_final_delivery"] is False
    assert boundary["runtime_side_effects"]["created_customer_delivery"] is False
    assert boundary["runtime_side_effects"]["called_download_package_runtime"] is False
    assert boundary["runtime_side_effects"]["called_public_access_runtime"] is False
    assert boundary["runtime_side_effects"]["called_external_delivery_runtime"] is False
