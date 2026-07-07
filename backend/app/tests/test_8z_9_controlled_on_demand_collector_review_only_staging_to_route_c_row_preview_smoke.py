from __future__ import annotations

import builtins
import importlib
import json
import sys
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_row_preview as row_preview_module


OUTER_8Z9_PHRASE = (
    "APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE"
)
INNER_8W7_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
FUTURE_8Z10_PHRASE = (
    "APPROVE_8Z_10_ROUTE_C_ROW_PREVIEW_COMPLETION_EVIDENCE_CANDIDATE_GATE_DECISION_DOCS_ONLY"
)
PHASE = "8Z-9"
ADAPTER_SCHEMA = "sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1"
ADAPTER_MODE = "backend_only_local_no_real_row_route_c_row_preview_entry_adapter"
ROW_PREVIEW_MODE = "backend_only_local_controlled_route_c_row_preview_smoke"
SYNTHETIC_FIXTURE_MARKER = "8z9_controlled_synthetic_temp_fixture_non_production"
OLD_GARBLED_8W7_PHRASE = "鎵瑰噯 8W-7 Controlled Row Preview Implementation"
OLD_CHINESE_8W7_PHRASE = "批准 8W-7 Controlled Row Preview Implementation"

DISALLOWED_IMPORT_PREFIXES = (
    "app.services.private_collector_package_resolver",
    "app.services.private_collector_provider_result_reader",
    "app.services.local_exchange_reader",
    "app.services.private_collector_review_only_staging",
    "app.services.controlled_evidence_candidate",
    "app.services.controlled_review_queue_candidate",
    "app.services.controlled_evidence_layer_import_candidate",
    "app.services.controlled_evidence_layer_write_candidate",
    "app.services.controlled_evidenceitem_evidence_layer_write_runtime",
    "app.services.controlled_production_case_candidate",
    "app.services.controlled_production_analysis_run_candidate",
    "app.services.controlled_production_analysis_result",
    "app.services.evidence_import",
    "app.services.evidence_ingestion",
    "app.services.source11_governance_handoff_finalsummaryreport_adapter",
    "app.services.report_candidate_final_report_boundary",
    "app.services.final_summary_report",
    "app.services.export_artifact",
)

ADAPTER_FALSE_FIELDS = {
    "row_preview_executed": "source_adapter_row_preview_executed_true",
    "controlled_row_preview_helper_called": "source_adapter_controlled_row_preview_helper_called_true",
    "redacted_review_only_row_preview_created": "source_adapter_redacted_preview_created_true",
    "row_preview_rows_created": "source_adapter_row_preview_rows_created_true",
    "synthetic_evidence_rows_created": "source_adapter_synthetic_evidence_rows_created_true",
    "fake_evidence_rows_created": "source_adapter_fake_evidence_rows_created_true",
    "row_source_path_present": "source_adapter_row_source_path_present_true",
    "row_source_file_opened": "source_adapter_row_source_file_opened_true",
    "evidence_items_jsonl_parsed": "source_adapter_evidence_items_jsonl_parsed_true",
    "evidence_items_csv_parsed": "source_adapter_evidence_items_csv_parsed_true",
    "source_manifest_rows_parsed": "source_adapter_source_manifest_rows_parsed_true",
    "collection_log_rows_parsed": "source_adapter_collection_log_rows_parsed_true",
    "package_resolver_called": "source_adapter_package_resolver_called_true",
    "provider_result_reader_called": "source_adapter_provider_result_reader_called_true",
    "local_exchange_reader_called": "source_adapter_local_exchange_reader_called_true",
    "review_only_staging_helper_called": "source_adapter_review_only_staging_helper_called_true",
    "real_exchange_dir_read": "source_adapter_real_exchange_dir_read_true",
    "real_package_dir_read": "source_adapter_real_package_dir_read_true",
    "evidence_layer_write": "source_adapter_evidence_layer_write_true",
    "production_evidence_item_created": "source_adapter_production_evidence_item_created_true",
    "production_case_created": "source_adapter_production_case_created_true",
    "production_analysis_run_created": "source_adapter_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_adapter_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": (
        "source_adapter_production_analysis_result_creation_authorized_true"
    ),
    "production_analysis_result_created": "source_adapter_production_analysis_result_created_true",
    "actual_review_queue_runtime_used": "source_adapter_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_adapter_production_review_queue_item_created_true",
    "collector_job_run": "source_adapter_collector_job_run_true",
    "provider_job_run": "source_adapter_provider_job_run_true",
    "scheduler_created": "source_adapter_scheduler_created_true",
    "http_bridge_created": "source_adapter_http_bridge_created_true",
    "webhook_created": "source_adapter_webhook_created_true",
    "private_collector_source_inspected": "source_adapter_private_collector_source_inspected_true",
    "source11_runtime_called": "source_adapter_source11_runtime_called_true",
    "actual_final_summary_report_created": "source_adapter_finalsummaryreport_created_true",
    "b_end_report_runtime_generated": "source_adapter_b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "source_adapter_sandbox_public_event_runtime_generated_true",
    "export_download_public_delivery_created": "source_adapter_export_download_public_delivery_created_true",
    "route_changed": "source_adapter_route_changed_true",
    "frontend_changed": "source_adapter_frontend_changed_true",
    "runtime_changed": "source_adapter_runtime_changed_true",
    "raw_rows_exposed": "source_adapter_raw_rows_exposed_true",
    "raw_comments_exposed": "source_adapter_raw_comments_exposed_true",
    "raw_identities_exposed": "source_adapter_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "source_adapter_author_identity_exposed_true",
    "secrets_read": "source_adapter_secrets_read_true",
    "route_ready": "source_adapter_route_ready_true",
    "frontend_ready": "source_adapter_frontend_ready_true",
    "production_ready": "source_adapter_production_ready_true",
    "customer_ready": "source_adapter_customer_ready_true",
    "public_ready": "source_adapter_public_ready_true",
}

OUTPUT_FALSE_FIELDS = {
    "real_exchange_dir_read": "output_real_exchange_dir_read_true",
    "real_package_dir_read": "output_real_package_dir_read_true",
    "production_package_rows_parsed": "output_production_package_rows_parsed_true",
    "original_package_rows_read": "output_original_package_rows_read_true",
    "arbitrary_package_dir_read": "output_arbitrary_package_dir_read_true",
    "evidence_items_csv_parsed": "output_evidence_items_csv_parsed_true",
    "source_manifest_rows_parsed": "output_source_manifest_rows_parsed_true",
    "collection_log_rows_parsed": "output_collection_log_rows_parsed_true",
    "source_manifest_file_opened": "output_source_manifest_file_opened_true",
    "collection_log_file_opened": "output_collection_log_file_opened_true",
    "package_resolver_called": "output_package_resolver_called_true",
    "provider_result_reader_called": "output_provider_result_reader_called_true",
    "local_exchange_reader_called": "output_local_exchange_reader_called_true",
    "review_only_staging_helper_called": "output_review_only_staging_helper_called_true",
    "controlled_evidence_candidate_called": "output_controlled_evidence_candidate_called_true",
    "downstream_route_c_evidence_candidate_created": "output_downstream_evidence_candidate_created_true",
    "evidence_layer_write": "output_evidence_layer_write_true",
    "production_evidence_item_created": "output_production_evidence_item_created_true",
    "production_case_created": "output_production_case_created_true",
    "production_analysis_run_created": "output_production_analysis_run_created_true",
    "actual_analysis_execution_started": "output_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": (
        "output_production_analysis_result_creation_authorized_true"
    ),
    "production_analysis_result_created": "output_production_analysis_result_created_true",
    "actual_review_queue_runtime_used": "output_review_queue_runtime_used_true",
    "production_review_queue_item_created": "output_production_review_queue_item_created_true",
    "collector_job_run": "output_collector_job_run_true",
    "provider_job_run": "output_provider_job_run_true",
    "scheduler_created": "output_scheduler_created_true",
    "http_bridge_created": "output_http_bridge_created_true",
    "webhook_created": "output_webhook_created_true",
    "private_collector_source_inspected": "output_private_collector_source_inspected_true",
    "source11_runtime_called": "output_source11_runtime_called_true",
    "actual_final_summary_report_created": "output_finalsummaryreport_created_true",
    "b_end_report_runtime_generated": "output_b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "output_sandbox_public_event_runtime_generated_true",
    "export_download_public_delivery_created": "output_export_download_public_delivery_created_true",
    "route_changed": "output_route_changed_true",
    "frontend_changed": "output_frontend_changed_true",
    "runtime_changed": "output_runtime_changed_true",
    "raw_rows_exposed": "output_raw_rows_exposed_true",
    "raw_comments_exposed": "output_raw_comments_exposed_true",
    "raw_identities_exposed": "output_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "output_author_identity_exposed_true",
    "secrets_read": "output_secrets_read_true",
    "route_ready": "output_route_ready_true",
    "frontend_ready": "output_frontend_ready_true",
    "production_ready": "output_production_ready_true",
    "customer_ready": "output_customer_ready_true",
    "public_ready": "output_public_ready_true",
}

FORBIDDEN_FIXTURE_FIELDS = {
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_name",
    "username",
    "display_name",
    "profile_url",
    "raw_profile_url",
    "raw_comment",
    "raw_comments",
    "private_message",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "api_key",
    "api_keys",
    "secret",
    "secrets",
    "password",
    "phone",
    "email",
}

FORBIDDEN_READY_CLAIMS = (
    "production" + "-ready",
    "customer" + "-ready",
    "public" + "-ready",
    "export" + "-ready",
    "final" + "-ready",
    "Source-11" + "-runtime-ready",
)


def build_safe_8z8b_no_real_row_adapter_candidate(**overrides: Any) -> dict[str, Any]:
    adapter = {
        "adapter_schema": ADAPTER_SCHEMA,
        "adapter_mode": ADAPTER_MODE,
        "route_c_row_preview_entry_candidate_created": True,
        "entry_candidate_only": True,
        "metadata_only": True,
        "row_preview_executed": False,
        "controlled_row_preview_helper_called": False,
        "redacted_review_only_row_preview_created": False,
        "row_preview_rows_created": False,
        "synthetic_evidence_rows_created": False,
        "fake_evidence_rows_created": False,
        "row_source_path_present": False,
        "row_source_file_opened": False,
        "evidence_items_jsonl_parsed": False,
        "evidence_items_csv_parsed": False,
        "source_manifest_rows_parsed": False,
        "collection_log_rows_parsed": False,
        "package_resolver_called": False,
        "provider_result_reader_called": False,
        "local_exchange_reader_called": False,
        "review_only_staging_helper_called": False,
        "real_exchange_dir_read": False,
        "real_package_dir_read": False,
        "evidence_layer_write": False,
        "production_evidence_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "actual_analysis_execution_started": False,
        "production_analysis_result_creation_authorized": False,
        "production_analysis_result_created": False,
        "actual_review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "collector_job_run": False,
        "provider_job_run": False,
        "scheduler_created": False,
        "http_bridge_created": False,
        "webhook_created": False,
        "private_collector_source_inspected": False,
        "source11_runtime_called": False,
        "actual_final_summary_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "export_download_public_delivery_created": False,
        "route_changed": False,
        "frontend_changed": False,
        "runtime_changed": False,
        "raw_rows_exposed": False,
        "raw_comments_exposed": False,
        "raw_identities_exposed": False,
        "author_names_or_profile_urls_exposed": False,
        "secrets_read": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "public_ready": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    adapter.update(overrides)
    return adapter


def build_8z9_controlled_route_c_row_preview_smoke(
    *,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch | None = None,
    source_adapter: dict[str, Any] | None = None,
    outer_approval_phrase: str | None = OUTER_8Z9_PHRASE,
    inner_helper_phrase: str | None = INNER_8W7_PHRASE,
    synthetic_rows: list[dict[str, Any]] | None = None,
    output_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blockers: list[str] = []
    adapter = source_adapter or build_safe_8z8b_no_real_row_adapter_candidate()
    rows = synthetic_rows if synthetic_rows is not None else _safe_synthetic_rows()

    if outer_approval_phrase != OUTER_8Z9_PHRASE:
        blockers.append("blocked_missing_exact_8z9_approval")
        return _blocked_output(blockers, source_adapter=adapter)

    blockers.extend(_source_adapter_blockers(adapter))
    if blockers:
        return _blocked_output(blockers, source_adapter=adapter)

    if inner_helper_phrase != INNER_8W7_PHRASE:
        preview = row_preview_module.build_controlled_row_preview(
            _safe_8w4_source_boundary(),
            approval_phrase=inner_helper_phrase,
        )
        return _blocked_output(
            ["blocked_inner_8w7_helper_phrase", *preview["blockers"]],
            source_adapter=adapter,
            helper_called=True,
        )

    blockers.extend(_synthetic_row_fixture_blockers(rows))
    if blockers:
        return _blocked_output(blockers, source_adapter=adapter)

    row_file = tmp_path / row_preview_module.APPROVED_ROW_SOURCE
    _write_synthetic_rows(row_file, rows)
    if monkeypatch is not None:
        monkeypatch.setattr(row_preview_module, "APPROVED_ROW_FILE", row_file)
    else:
        row_preview_module.APPROVED_ROW_FILE = row_file

    preview = row_preview_module.build_controlled_row_preview(
        _safe_8w4_source_boundary(),
        approval_phrase=inner_helper_phrase,
        row_source=row_preview_module.APPROVED_ROW_SOURCE,
    )
    if preview["created_local_row_preview"] is not True:
        return _blocked_output(
            ["controlled_row_preview_blocked", *preview["blockers"]],
            source_adapter=adapter,
            helper_called=True,
        )

    output = _ready_output(adapter, preview)
    if output_overrides:
        output.update(output_overrides)
    output_blockers = _output_blockers(output)
    if output_blockers:
        output["decision"] = "blocked"
        output["blockers"] = _dedupe([*output["blockers"], *output_blockers])
        output["privacy_issue_stop"] = any("raw" in blocker or "secret" in blocker for blocker in output_blockers)
    return output


def _ready_output(source_adapter: dict[str, Any], preview: dict[str, Any]) -> dict[str, Any]:
    preview_rows = preview["preview_rows"]
    assert isinstance(preview_rows, list)
    return {
        "phase": PHASE,
        "decision": "ready",
        "privacy_issue_stop": False,
        "backend_only": True,
        "test_first": True,
        "controlled_smoke": True,
        "service_code_changed": False,
        "source_path_step": "on_demand_collector_review_only_staging_to_route_c_row_preview",
        "outer_8z9_phrase_required": True,
        "outer_8z9_phrase": OUTER_8Z9_PHRASE,
        "repaired_8w7_inner_helper_phrase_required": True,
        "repaired_8w7_inner_helper_phrase": INNER_8W7_PHRASE,
        "8w7_inner_phrase_alone_authorizes_8z9": False,
        "old_8w7_garbled_or_chinese_phrase_accepted": False,
        "source_adapter_schema": source_adapter["adapter_schema"],
        "source_adapter_mode": source_adapter["adapter_mode"],
        "route_c_row_preview_entry_created": True,
        "redacted_review_only_row_preview_created": True,
        "row_preview_schema": preview["schema"],
        "row_preview_mode": ROW_PREVIEW_MODE,
        "row_preview_scope": "controlled_synthetic_temp_fixture_only",
        "controlled_row_preview_helper_called": True,
        "synthetic_temp_row_fixture_used": True,
        "synthetic_temp_row_source_opened": True,
        "row_preview_executed": True,
        "review_only": True,
        "redacted": True,
        "no_downstream_route_c_auto_run": True,
        "preview_rows_count": preview["preview_rows_count"],
        "preview_rows": preview_rows,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_temp_fixture_only"],
        **{field: False for field in OUTPUT_FALSE_FIELDS},
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "8w69_pause_preserved": True,
        "8w70_reactivation_selected": False,
        "future_8z10_phrase": FUTURE_8Z10_PHRASE,
        "future_8z10_phrase_active": False,
    }


def _blocked_output(
    blockers: list[str],
    *,
    source_adapter: dict[str, Any] | None,
    helper_called: bool = False,
) -> dict[str, Any]:
    return {
        "phase": PHASE,
        "decision": "blocked",
        "privacy_issue_stop": any("raw" in blocker or "secret" in blocker for blocker in blockers),
        "source_adapter_schema": (source_adapter or {}).get("adapter_schema"),
        "source_adapter_mode": (source_adapter or {}).get("adapter_mode"),
        "route_c_row_preview_entry_created": False,
        "redacted_review_only_row_preview_created": False,
        "row_preview_scope": "blocked",
        "controlled_row_preview_helper_called": helper_called,
        "synthetic_temp_row_fixture_used": False,
        "synthetic_temp_row_source_opened": False,
        "row_preview_executed": False,
        "8w7_inner_phrase_alone_authorizes_8z9": False,
        "old_8w7_garbled_or_chinese_phrase_accepted": False,
        "blockers": _dedupe(blockers),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in OUTPUT_FALSE_FIELDS},
    }


def _safe_8w4_source_boundary() -> dict[str, Any]:
    return {
        "schema": row_preview_module.SOURCE_SCHEMA,
        "phase": row_preview_module.SOURCE_PHASE,
        "boundary_status": row_preview_module.SOURCE_READY_STATUS,
        "approved_target_package_name": row_preview_module.APPROVED_PACKAGE_NAME,
        "approved_target_package_role": row_preview_module.APPROVED_PACKAGE_ROLE,
        "approved_target_case_id_hint": row_preview_module.APPROVED_CASE_ID_HINT,
        "metadata_only": True,
        "warning_count": 1,
        "human_review_required": True,
        "warning_manual_review_preserved": True,
        "row_preview_approved": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "runtime_side_effects": {
            "called_real_api": False,
            "called_real_llm": False,
            "ran_provider_job": False,
            "ran_collector": False,
            "read_real_exchange_dir": False,
            "parsed_evidence_items_jsonl": False,
            "parsed_evidence_items_csv": False,
            "parsed_source_manifest_jsonl_rows": False,
            "parsed_collection_log_jsonl_rows": False,
            "wrote_evidence_layer": False,
        },
    }


def _safe_synthetic_rows() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "synthetic-8z9-row-001",
            "evidence_type": "synthetic_note",
            "platform": "synthetic_forum",
            "created_at": "2026-07-07T00:00:00Z",
            "trust_label": "synthetic_fixture",
            "verification_status": "not_official_verification",
            "review_status": "review_only",
            "language": "en",
            "content_visibility": "synthetic_public_sample",
            "access_scope": "synthetic_non_production",
            "synthetic_non_production_marker": SYNTHETIC_FIXTURE_MARKER,
            "body_text": "Synthetic non-production Route C preview fixture for boundary testing only.",
        }
    ]


def _write_synthetic_rows(row_file: Path, rows: list[dict[str, Any]]) -> None:
    payload = "\n".join(json.dumps(row, sort_keys=True, ensure_ascii=False) for row in rows)
    row_file.write_text(payload + "\n", encoding="utf-8")


def _source_adapter_blockers(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if adapter.get("adapter_schema") != ADAPTER_SCHEMA:
        blockers.append("source_adapter_schema_wrong")
    if adapter.get("adapter_mode") != ADAPTER_MODE:
        blockers.append("source_adapter_mode_wrong")
    if adapter.get("route_c_row_preview_entry_candidate_created") is not True:
        blockers.append("source_adapter_entry_candidate_not_true")
    if adapter.get("metadata_only") is not True:
        blockers.append("source_adapter_metadata_only_not_true")
    if adapter.get("human_review_required") is not True:
        blockers.append("source_adapter_human_review_required_not_true")
    if adapter.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_adapter_no_automatic_trust_upgrade_not_true")
    for field, reason in ADAPTER_FALSE_FIELDS.items():
        if adapter.get(field) is True:
            blockers.append(reason)
    blockers.extend(_forbidden_payload_blockers(adapter, prefix="source_adapter"))
    return _dedupe(blockers)


def _synthetic_row_fixture_blockers(rows: Any) -> list[str]:
    blockers: list[str] = []
    if not isinstance(rows, list) or not rows:
        return ["synthetic_temp_row_fixture_missing"]
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            blockers.append(f"synthetic_row_{index}_not_object")
            continue
        if row.get("synthetic_non_production_marker") != SYNTHETIC_FIXTURE_MARKER:
            blockers.append("synthetic_temp_row_fixture_missing_non_production_marker")
        blockers.extend(_forbidden_payload_blockers(row, prefix=f"synthetic_row_{index}"))
    return _dedupe(blockers)


def _output_blockers(output: dict[str, Any]) -> list[str]:
    blockers = []
    for field, reason in OUTPUT_FALSE_FIELDS.items():
        if output.get(field) is True:
            blockers.append(reason)
    blockers.extend(_forbidden_payload_blockers(output, prefix="output"))
    return _dedupe(blockers)


def _forbidden_payload_blockers(payload: Any, *, prefix: str) -> list[str]:
    blockers: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            normalized_key = str(key).lower()
            if normalized_key in FORBIDDEN_FIXTURE_FIELDS:
                blockers.append(f"{prefix}_forbidden_field:{key}")
            blockers.extend(_forbidden_payload_blockers(value, prefix=prefix))
    elif isinstance(payload, list):
        for item in payload:
            blockers.extend(_forbidden_payload_blockers(item, prefix=prefix))
    elif isinstance(payload, str):
        lowered = payload.lower()
        if "http://" in lowered or "https://" in lowered:
            blockers.append(f"{prefix}_forbidden_real_looking_url")
        if any(claim.lower() in lowered for claim in FORBIDDEN_READY_CLAIMS):
            blockers.append(f"{prefix}_forbidden_ready_claim")
        if any(marker in lowered for marker in ("cookie=", "token=", "api_key=", "password=", ".env")):
            blockers.append(f"{prefix}_forbidden_secret_like_text")
    return blockers


def install_exact_synthetic_file_guard(
    monkeypatch: pytest.MonkeyPatch,
    allowed_path: Path,
    opened_reads: list[Path],
) -> None:
    original_open = Path.open

    def guarded_open(self: Path, *args: Any, **kwargs: Any):
        mode = args[0] if args else kwargs.get("mode", "r")
        if self != allowed_path:
            raise AssertionError(f"unexpected file open: {self}")
        if "r" in str(mode):
            opened_reads.append(self)
        return original_open(self, *args, **kwargs)

    def blocked_read(*args: Any, **kwargs: Any) -> str:
        raise AssertionError("Path.read_text/read_bytes must not be used in 8Z-9")

    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(Path, "read_text", blocked_read)
    monkeypatch.setattr(Path, "read_bytes", blocked_read)


def install_no_downstream_import_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    original_import = builtins.__import__
    original_import_module = importlib.import_module

    def guarded_import(name: str, *args: Any, **kwargs: Any):
        fromlist = kwargs.get("fromlist")
        if len(args) >= 4:
            fromlist = args[3]
        requested_names = [name]
        if fromlist:
            requested_names.extend(f"{name}.{item}" for item in fromlist if isinstance(item, str))
        if any(_is_disallowed_import(requested_name) for requested_name in requested_names):
            raise AssertionError(f"disallowed downstream import attempted: {name}")
        return original_import(name, *args, **kwargs)

    def guarded_import_module(name: str, package: str | None = None):
        if _is_disallowed_import(name):
            raise AssertionError(f"disallowed downstream import_module attempted: {name}")
        return original_import_module(name, package=package)

    monkeypatch.setattr(builtins, "__import__", guarded_import)
    monkeypatch.setattr(importlib, "import_module", guarded_import_module)


def _is_disallowed_import(module_name: str) -> bool:
    return any(
        module_name == prefix or module_name.startswith(f"{prefix}.")
        for prefix in DISALLOWED_IMPORT_PREFIXES
    )


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def assert_ready_side_effects_false(result: dict[str, Any]) -> None:
    for field in OUTPUT_FALSE_FIELDS:
        assert result[field] is False, field


def assert_blocked_before_helper_and_file(result: dict[str, Any], opened_reads: list[Path]) -> None:
    assert result["decision"] == "blocked"
    assert result["controlled_row_preview_helper_called"] is False
    assert result["synthetic_temp_row_source_opened"] is False
    assert result["row_preview_executed"] is False
    assert opened_reads == []


def test_8z9_builds_controlled_route_c_row_preview_from_no_real_row_adapter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)
    install_no_downstream_import_guard(monkeypatch)

    result = build_8z9_controlled_route_c_row_preview_smoke(tmp_path=tmp_path, monkeypatch=monkeypatch)

    assert result["decision"] == "ready"
    assert result["route_c_row_preview_entry_created"] is True
    assert result["redacted_review_only_row_preview_created"] is True
    assert result["source_adapter_schema"] == ADAPTER_SCHEMA
    assert result["source_adapter_mode"] == ADAPTER_MODE
    assert result["row_preview_schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert result["row_preview_mode"] == ROW_PREVIEW_MODE
    assert result["row_preview_scope"] == "controlled_synthetic_temp_fixture_only"
    assert result["outer_8z9_phrase_required"] is True
    assert result["repaired_8w7_inner_helper_phrase_required"] is True
    assert result["8w7_inner_phrase_alone_authorizes_8z9"] is False
    assert result["old_8w7_garbled_or_chinese_phrase_accepted"] is False
    assert result["controlled_row_preview_helper_called"] is True
    assert result["synthetic_temp_row_fixture_used"] is True
    assert result["synthetic_temp_row_source_opened"] is True
    assert result["row_preview_executed"] is True
    assert result["human_review_required"] is True
    assert result["no_automatic_trust_upgrade"] is True
    assert result["review_only"] is True
    assert result["redacted"] is True
    assert result["no_downstream_route_c_auto_run"] is True
    assert result["future_8z10_phrase_active"] is False
    assert opened_reads == [tmp_path / row_preview_module.APPROVED_ROW_SOURCE]
    assert result["preview_rows_count"] == 1
    preview_row = result["preview_rows"][0]
    assert preview_row["redaction_status"] == "redacted"
    assert preview_row["row_boundary_flags"]["preview_only"] is True
    assert preview_row["row_boundary_flags"]["human_review_required"] is True
    assert_ready_side_effects_false(result)


@pytest.mark.parametrize(
    "outer_phrase",
    [
        None,
        "",
        "wrong",
        "APPROVE_8Z_8C_NO_REAL_ROW_ADAPTER_COMPLETION_ROUTE_C_ROW_PREVIEW_REGATE_DECISION_DOCS_ONLY",
        "APPROVE_8Z_8B_CONTROLLED_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_ADAPTER_SMOKE",
        "APPROVE_8Z_8_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ENTRY_GATE_DECISION_DOCS_ONLY",
        "APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE",
        "APPROVE_8Y_4_CONTROLLED_REDACTED_REVIEW_ONLY_ROW_PREVIEW_SMOKE",
        INNER_8W7_PHRASE,
        FUTURE_8Z10_PHRASE,
    ],
)
def test_missing_wrong_historical_or_inner_phrase_blocks_before_helper_and_file(
    outer_phrase: str | None,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        outer_approval_phrase=outer_phrase,
    )

    assert "blocked_missing_exact_8z9_approval" in result["blockers"]
    assert_blocked_before_helper_and_file(result, opened_reads)


@pytest.mark.parametrize(
    "inner_phrase",
    [None, "", "wrong", OLD_GARBLED_8W7_PHRASE, OLD_CHINESE_8W7_PHRASE],
)
def test_missing_wrong_or_old_inner_8w7_phrase_blocks_before_row_source_access(
    inner_phrase: str | None,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        inner_helper_phrase=inner_phrase,
    )

    assert result["decision"] == "blocked"
    assert result["controlled_row_preview_helper_called"] is True
    assert "blocked_inner_8w7_helper_phrase" in result["blockers"]
    assert "blocked_missing_exact_approval" in result["blockers"]
    assert result["synthetic_temp_row_source_opened"] is False
    assert result["row_preview_executed"] is False
    assert opened_reads == []


@pytest.mark.parametrize(
    ("override", "reason"),
    [
        ({"adapter_schema": "wrong"}, "source_adapter_schema_wrong"),
        ({"metadata_only": False}, "source_adapter_metadata_only_not_true"),
        ({"row_source_path_present": True}, "source_adapter_row_source_path_present_true"),
        ({"row_source_file_opened": True}, "source_adapter_row_source_file_opened_true"),
        ({"row_preview_executed": True}, "source_adapter_row_preview_executed_true"),
        ({"controlled_row_preview_helper_called": True}, "source_adapter_controlled_row_preview_helper_called_true"),
        ({"row_preview_rows_created": True}, "source_adapter_row_preview_rows_created_true"),
        ({"synthetic_evidence_rows_created": True}, "source_adapter_synthetic_evidence_rows_created_true"),
        ({"fake_evidence_rows_created": True}, "source_adapter_fake_evidence_rows_created_true"),
        ({"package_resolver_called": True}, "source_adapter_package_resolver_called_true"),
        ({"provider_result_reader_called": True}, "source_adapter_provider_result_reader_called_true"),
        ({"local_exchange_reader_called": True}, "source_adapter_local_exchange_reader_called_true"),
        ({"review_only_staging_helper_called": True}, "source_adapter_review_only_staging_helper_called_true"),
        ({"real_exchange_dir_read": True}, "source_adapter_real_exchange_dir_read_true"),
        ({"real_package_dir_read": True}, "source_adapter_real_package_dir_read_true"),
        ({"evidence_layer_write": True}, "source_adapter_evidence_layer_write_true"),
        ({"production_case_created": True}, "source_adapter_production_case_created_true"),
    ],
)
def test_unsafe_source_adapter_blocks_before_helper_and_file(
    override: dict[str, Any],
    reason: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)
    adapter = build_safe_8z8b_no_real_row_adapter_candidate(**override)

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        source_adapter=adapter,
    )

    assert reason in result["blockers"]
    assert_blocked_before_helper_and_file(result, opened_reads)


@pytest.mark.parametrize(
    ("row_override", "reason"),
    [
        ({}, "synthetic_temp_row_fixture_missing_non_production_marker"),
        ({"raw_comment": "private raw text"}, "synthetic_row_0_forbidden_field:raw_comment"),
        ({"author_name": "real name"}, "synthetic_row_0_forbidden_field:author_name"),
        ({"profile_url": "https://example.com/profile"}, "synthetic_row_0_forbidden_field:profile_url"),
        ({"cookie": "cookie=secret"}, "synthetic_row_0_forbidden_field:cookie"),
        ({"body_text": "contains https://example.com/profile"}, "synthetic_row_0_forbidden_real_looking_url"),
        ({"body_text": "token=secret"}, "synthetic_row_0_forbidden_secret_like_text"),
    ],
)
def test_unsafe_synthetic_fixture_blocks_before_row_source_access(
    row_override: dict[str, Any],
    reason: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)
    row = _safe_synthetic_rows()[0]
    row.update(row_override)
    if row_override == {}:
        row.pop("synthetic_non_production_marker")

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        synthetic_rows=[row],
    )

    assert reason in result["blockers"]
    assert_blocked_before_helper_and_file(result, opened_reads)


@pytest.mark.parametrize(
    ("override", "reason"),
    [
        ({"raw_rows_exposed": True}, "output_raw_rows_exposed_true"),
        ({"raw_comments_exposed": True}, "output_raw_comments_exposed_true"),
        ({"raw_identities_exposed": True}, "output_raw_identities_exposed_true"),
        ({"author_names_or_profile_urls_exposed": True}, "output_author_identity_exposed_true"),
        ({"controlled_evidence_candidate_called": True}, "output_controlled_evidence_candidate_called_true"),
        (
            {"downstream_route_c_evidence_candidate_created": True},
            "output_downstream_evidence_candidate_created_true",
        ),
        ({"evidence_layer_write": True}, "output_evidence_layer_write_true"),
        ({"production_evidence_item_created": True}, "output_production_evidence_item_created_true"),
        ({"production_case_created": True}, "output_production_case_created_true"),
        ({"production_analysis_run_created": True}, "output_production_analysis_run_created_true"),
        ({"production_analysis_result_created": True}, "output_production_analysis_result_created_true"),
        (
            {"operator_claim": "production" + "-ready " + "Source-11" + "-runtime-ready"},
            "output_forbidden_ready_claim",
        ),
    ],
)
def test_unsafe_output_blocks_without_downstream_authorization(
    override: dict[str, Any],
    reason: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        output_overrides=override,
    )

    assert result["decision"] == "blocked"
    assert reason in result["blockers"]
    assert result["controlled_row_preview_helper_called"] is True
    assert opened_reads == [tmp_path / row_preview_module.APPROVED_ROW_SOURCE]


def test_8z9_does_not_import_downstream_route_c_or_collector_helpers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)
    install_no_downstream_import_guard(monkeypatch)
    before_modules = set(sys.modules)

    result = build_8z9_controlled_route_c_row_preview_smoke(tmp_path=tmp_path, monkeypatch=monkeypatch)

    assert result["decision"] == "ready"
    new_disallowed_modules = sorted(
        module_name
        for module_name in set(sys.modules) - before_modules
        if _is_disallowed_import(module_name)
    )
    assert new_disallowed_modules == []
    assert_ready_side_effects_false(result)


def test_future_8z10_phrase_is_inactive_and_does_not_authorize_8z9(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opened_reads: list[Path] = []
    install_exact_synthetic_file_guard(monkeypatch, tmp_path / row_preview_module.APPROVED_ROW_SOURCE, opened_reads)

    result = build_8z9_controlled_route_c_row_preview_smoke(
        tmp_path=tmp_path,
        monkeypatch=monkeypatch,
        outer_approval_phrase=FUTURE_8Z10_PHRASE,
    )

    assert "blocked_missing_exact_8z9_approval" in result["blockers"]
    assert_blocked_before_helper_and_file(result, opened_reads)
