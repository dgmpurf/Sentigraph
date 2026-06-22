from __future__ import annotations

import inspect
import subprocess
from pathlib import Path

from app.api.v1.routes import analysis_requests as analysis_request_routes
from app.schemas import analysis_request as schemas
from app.schemas.analysis_request import (
    ReportExportPublicAccessExternalDeliveryGate,
    ReportExportPublicAccessExternalDeliveryGateAudit,
    ReportExportPublicAccessExternalDeliveryGateRequest,
)
from app.services import analysis_request_store


REPO_ROOT = Path(__file__).resolve().parents[3]
ROUTES_SOURCE = REPO_ROOT / "backend" / "app" / "api" / "v1" / "routes" / "analysis_requests.py"


def _app_route_paths() -> set[str]:
    return {f"/api/v1/analysis-requests{getattr(route, 'path', '')}" for route in analysis_request_routes.router.routes}


def test_analysis_request_route_inventory_keeps_key_endpoint_families() -> None:
    paths = _app_route_paths()
    joined = "\n".join(sorted(paths))

    assert "/api/v1/analysis-requests" in paths

    required_fragments = [
        "case-draft",
        "import-plan",
        "import-preview",
        "review-decisions",
        "import-jobs",
        "execution-preflights",
        "row-reader-dry-runs",
        "real-package-row-previews",
        "review-only-cases",
        "staging-imports",
        "review-queue-initializations",
        "review-queue-action-audits",
        "review-queue-completion-gates",
        "dedup-previews",
        "dedup-group-review-audits",
        "analysis-ready-promotion-gates",
        "manual-analysis-triggers",
        "analysis-result-boundary-gates",
        "manual-analysis-executions",
        "report-generation-gates",
        "summary-report-candidates",
        "final-summary-report-review-gates",
        "final-summary-reports",
        "final-summary-report-export-gates",
        "final-summary-report-export-artifacts",
        "report-export-download-package-gates",
        "report-export-download-package-artifacts",
        "report-export-public-access-external-delivery-gates",
        "report-export-public-access-external-delivery-gate-audits",
    ]

    for fragment in required_fragments:
        assert fragment in joined


def test_analysis_request_router_does_not_implement_public_delivery_primitives() -> None:
    source = ROUTES_SOURCE.read_text(encoding="utf-8")
    forbidden_tokens = [
        "FileResponse",
        "StreamingResponse",
        "send_file",
        "zipfile",
        "shutil.make_archive",
        "generate_public_url",
        "generate_signed_url",
        "create_signed_url",
        "upload_to_object_storage",
        "boto3",
        "send_mail",
        "smtp",
    ]

    for token in forbidden_tokens:
        assert token not in source


def test_latest_and_core_schema_classes_remain_importable() -> None:
    required_schema_names = [
        "ReportExportDownloadPackageArtifact",
        "ReportExportDownloadPackageArtifactAudit",
        "ReportExportPublicAccessExternalDeliveryGate",
        "ReportExportPublicAccessExternalDeliveryGateAudit",
        "FinalSummaryReport",
        "FinalSummaryReportExportArtifact",
        "ReportExportDownloadPackageGate",
        "ManualAnalysisExecution",
        "SummaryReportCandidate",
    ]

    for name in required_schema_names:
        assert hasattr(schemas, name), name


def test_public_access_external_delivery_gate_defaults_keep_side_effects_false() -> None:
    request = ReportExportPublicAccessExternalDeliveryGateRequest(
        package_artifact_id="package_artifact_contract",
        download_package_gate_id="download_package_gate_contract",
        final_summary_report_id="final_report_contract",
        review_case_id="review_case_contract",
        reviewer_label="contract_reviewer",
        note="Golden contract default boundary check.",
        access_delivery_decision="approve_for_future_public_access_external_delivery_runtime",
    )

    dangerous_request_flags = [
        "creates_public_download_route_now",
        "creates_file_byte_response_now",
        "generates_public_url_now",
        "generates_signed_url_now",
        "performs_external_delivery_now",
        "sends_email_now",
        "uploads_to_object_storage_now",
        "publishes_to_portal_now",
        "exposes_runtime_file_now",
        "exposes_absolute_path_now",
        "exposes_manifest_file_content_now",
        "exposes_export_artifact_content_now",
        "reads_export_artifact_file_content_now",
        "copies_export_artifact_content_now",
        "generates_zip_now",
        "generates_binary_archive_now",
        "generates_b_end_report_now",
        "generates_sandbox_now",
        "generates_public_event_now",
        "writes_evidence_layer_now",
        "creates_production_case_now",
        "calls_real_api_now",
        "calls_real_llm_now",
        "fetches_url_now",
        "scrapes_now",
        "reads_original_package_rows_now",
    ]

    for field_name in dangerous_request_flags:
        assert getattr(request, field_name) is False

    gate = ReportExportPublicAccessExternalDeliveryGate(
        public_access_delivery_gate_id="public_access_delivery_gate_contract",
        request_id="request_contract",
        review_case_id="review_case_contract",
        package_artifact_id="package_artifact_contract",
        download_package_gate_id="download_package_gate_contract",
        final_summary_report_id="final_report_contract",
        gate_status="ready_for_future_public_access_external_delivery_runtime",
        access_delivery_decision="approve_for_future_public_access_external_delivery_runtime",
    )

    dangerous_safe_mode_flags = [
        "public_download_route_created",
        "file_byte_response_created",
        "zip_generated",
        "public_url_generated",
        "signed_url_generated",
        "external_delivery_performed",
        "email_sent",
        "object_storage_uploaded",
        "portal_published",
        "runtime_file_exposed",
        "absolute_path_exposed",
        "manifest_file_content_exposed",
        "export_artifact_content_read",
        "export_artifact_content_copied",
        "b_end_report_generated",
        "sandbox_fixture_generated",
        "public_event_page_generated",
        "evidence_layer_written",
        "production_case_created",
        "production_review_queue_created",
        "production_dedup_run",
        "provider_execution",
        "collector_jobs_run",
        "real_api_calls",
        "real_llm_calls",
        "url_fetching",
        "scraping",
        "secrets_exposed",
        "raw_author_identifiers_exposed",
    ]

    assert gate.safe_mode["public_access_external_delivery_gate_only"] is True
    for flag in dangerous_safe_mode_flags:
        assert gate.safe_mode[flag] is False

    audit = ReportExportPublicAccessExternalDeliveryGateAudit(
        public_access_delivery_gate_audit_id="public_access_delivery_gate_audit_contract",
        public_access_delivery_gate_id="public_access_delivery_gate_contract",
        package_artifact_id="package_artifact_contract",
        package_artifact_audit_id="package_artifact_audit_contract",
        download_package_gate_id="download_package_gate_contract",
        final_summary_report_id="final_report_contract",
        request_id="request_contract",
        review_case_id="review_case_contract",
        new_status="ready_for_future_public_access_external_delivery_runtime",
        access_delivery_decision="approve_for_future_public_access_external_delivery_runtime",
        reviewer_label="contract_reviewer",
    )

    for flag_value in audit.now_flags.values():
        assert flag_value is False
    assert audit.safe_mode["public_access_external_delivery_gate_audit_only"] is True
    for flag in dangerous_safe_mode_flags:
        if flag in audit.safe_mode:
            assert audit.safe_mode[flag] is False


def test_runtime_and_build_outputs_remain_git_ignored() -> None:
    paths = ["runtime/analysis_requests/", "frontend/dist/", ".benchmarks/"]
    result = subprocess.run(
        ["git", "check-ignore", *paths],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    ignored = set(result.stdout.strip().splitlines())
    assert ignored == set(paths)


def test_public_access_external_delivery_store_code_does_not_read_artifact_content_or_generate_delivery() -> None:
    targeted_functions = [
        analysis_request_store.create_report_export_public_access_external_delivery_gate,
        analysis_request_store._validate_report_export_public_access_external_delivery_gate_payload,
        analysis_request_store._validate_report_export_public_access_external_delivery_gate_prerequisites,
        analysis_request_store._validate_report_export_public_access_external_delivery_package_metadata,
        analysis_request_store._report_export_public_access_external_delivery_payload_has_forbidden_extra,
    ]
    source = "\n".join(inspect.getsource(function) for function in targeted_functions)

    forbidden_tokens = [
        "FileResponse",
        "StreamingResponse",
        "read_text(",
        "read_bytes(",
        "open(",
        "evidence_items.jsonl",
        "evidence_items.csv",
        "zipfile",
        "ZipFile",
        "shutil.make_archive",
        "generate_public_url",
        "generate_signed_url",
        "send_mail",
        "smtp",
        "boto3",
        "upload_to_object_storage",
    ]

    for token in forbidden_tokens:
        assert token not in source


def test_latest_public_access_external_delivery_audit_contract_is_exposed() -> None:
    paths = _app_route_paths()
    joined = "\n".join(sorted(paths))

    assert "report-export-public-access-external-delivery-gate-audits" in joined
    assert hasattr(schemas, "ReportExportPublicAccessExternalDeliveryGateAudit")
    assert hasattr(analysis_request_store, "list_report_export_public_access_external_delivery_gate_audits")
    assert hasattr(analysis_request_store, "list_report_export_public_access_external_delivery_gate_audits_for_gate")
    assert hasattr(analysis_request_routes, "analysis_request_report_export_public_access_external_delivery_gate_audit_list")
