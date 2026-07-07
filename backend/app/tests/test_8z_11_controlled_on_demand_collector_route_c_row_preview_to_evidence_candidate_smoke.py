from __future__ import annotations

import builtins
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_evidence_candidate as evidence_candidate_module


BATCH_APPROVAL_PHRASE = (
    "APPROVE_8Z_10A_11_BATCH_REPAIR_CONTROLLED_EVIDENCE_CANDIDATE_HELPER_PHRASE_REGATE_AND_SMOKE"
)
HELPER_APPROVAL_PHRASE = "APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION"
INACTIVE_STANDALONE_8Z11_PHRASE = (
    "APPROVE_8Z_11_CONTROLLED_ON_DEMAND_COLLECTOR_ROUTE_C_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SMOKE"
)
OLD_CHINESE_HELPER_PHRASE = "批准 8W-10 Controlled Evidence Candidate Helper Implementation"
OLD_MOJIBAKE_HELPER_PHRASE = "鎵瑰噯 8W-10 Controlled Evidence Candidate Helper Implementation"
OLD_GARBLED_HELPER_PHRASE = "閹电懓鍣?8W-10 Controlled Evidence Candidate Helper Implementation"

PHASE = "8Z-11"
SOURCE_ADAPTER_SCHEMA = "sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1"
SOURCE_ADAPTER_MODE = "backend_only_local_no_real_row_route_c_row_preview_entry_adapter"
ROW_PREVIEW_MODE = "backend_only_local_controlled_route_c_row_preview_smoke"
ROW_PREVIEW_SCOPE = "in_memory_non_production_fixture_only"

FALSE_SOURCE_FLAGS = {
    "real_exchange_dir_read": "source_real_exchange_dir_read_true",
    "real_package_dir_read": "source_real_package_dir_read_true",
    "production_package_rows_parsed": "source_production_package_rows_parsed_true",
    "original_package_rows_read": "source_original_package_rows_read_true",
    "evidence_items_csv_parsed": "source_evidence_items_csv_parsed_true",
    "source_manifest_rows_parsed": "source_source_manifest_rows_parsed_true",
    "collection_log_rows_parsed": "source_collection_log_rows_parsed_true",
    "package_resolver_called": "source_package_resolver_called_true",
    "provider_result_reader_called": "source_provider_result_reader_called_true",
    "local_exchange_reader_called": "source_local_exchange_reader_called_true",
    "review_only_staging_helper_called": "source_review_only_staging_helper_called_true",
    "controlled_evidence_candidate_called": "source_controlled_evidence_candidate_called_true",
    "downstream_route_c_evidence_candidate_created": "source_downstream_evidence_candidate_created_true",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "actual_review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": "source_analysis_result_authorized_true",
    "production_analysis_result_created": "source_analysis_result_created_true",
    "raw_rows_exposed": "source_raw_rows_exposed_true",
    "raw_comments_exposed": "source_raw_comments_exposed_true",
    "raw_identities_exposed": "source_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "source_author_identity_exposed_true",
    "secrets_read": "source_secrets_read_true",
    "collector_job_run": "source_collector_job_run_true",
    "provider_job_run": "source_provider_job_run_true",
    "scheduler_created": "source_scheduler_created_true",
    "http_bridge_created": "source_http_bridge_created_true",
    "webhook_created": "source_webhook_created_true",
    "private_collector_source_inspected": "source_private_collector_source_inspected_true",
    "source11_runtime_called": "source_source11_runtime_called_true",
    "actual_final_summary_report_created": "source_finalsummaryreport_created_true",
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "source_sandbox_public_event_generated_true",
    "export_download_public_delivery_created": "source_export_delivery_created_true",
    "route_changed": "source_route_changed_true",
    "frontend_changed": "source_frontend_changed_true",
    "runtime_changed": "source_runtime_changed_true",
    "route_ready": "source_route_ready_true",
    "frontend_ready": "source_frontend_ready_true",
    "production_ready": "source_production_ready_true",
    "customer_ready": "source_customer_ready_true",
    "public_ready": "source_public_ready_true",
}

FALSE_OUTPUT_FLAGS = {
    "evidence_layer_write": "output_evidence_layer_write_true",
    "production_evidence_item_created": "output_production_evidence_item_created_true",
    "actual_review_queue_runtime_used": "output_review_queue_runtime_used_true",
    "production_review_queue_item_created": "output_production_review_queue_item_created_true",
    "review_queue_candidate_created": "output_review_queue_candidate_created_true",
    "evidence_layer_import_candidate_created": "output_evidence_layer_import_candidate_created_true",
    "evidence_layer_write_candidate_created": "output_evidence_layer_write_candidate_created_true",
    "production_case_created": "output_production_case_created_true",
    "production_analysis_run_created": "output_production_analysis_run_created_true",
    "actual_analysis_execution_started": "output_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": "output_analysis_result_authorized_true",
    "production_analysis_result_created": "output_analysis_result_created_true",
    "downstream_route_c_auto_run": "output_downstream_route_c_auto_run_true",
    "package_resolver_called": "output_package_resolver_called_true",
    "provider_result_reader_called": "output_provider_result_reader_called_true",
    "local_exchange_reader_called": "output_local_exchange_reader_called_true",
    "review_only_staging_helper_called": "output_review_only_staging_helper_called_true",
    "collector_job_run": "output_collector_job_run_true",
    "provider_job_run": "output_provider_job_run_true",
    "scheduler_created": "output_scheduler_created_true",
    "http_bridge_created": "output_http_bridge_created_true",
    "webhook_created": "output_webhook_created_true",
    "private_collector_source_inspected": "output_private_collector_source_inspected_true",
    "real_exchange_dir_read": "output_real_exchange_dir_read_true",
    "real_package_dir_read": "output_real_package_dir_read_true",
    "production_package_rows_parsed": "output_production_package_rows_parsed_true",
    "original_package_rows_read": "output_original_package_rows_read_true",
    "raw_rows_exposed": "output_raw_rows_exposed_true",
    "raw_comments_exposed": "output_raw_comments_exposed_true",
    "raw_identities_exposed": "output_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "output_author_identity_exposed_true",
    "secrets_read": "output_secrets_read_true",
    "source11_runtime_called": "output_source11_runtime_called_true",
    "actual_final_summary_report_created": "output_finalsummaryreport_created_true",
    "b_end_report_runtime_generated": "output_b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "output_sandbox_public_event_generated_true",
    "export_download_public_delivery_created": "output_export_delivery_created_true",
    "route_changed": "output_route_changed_true",
    "frontend_changed": "output_frontend_changed_true",
    "runtime_changed": "output_runtime_changed_true",
    "route_ready": "output_route_ready_true",
    "frontend_ready": "output_frontend_ready_true",
    "production_ready": "output_production_ready_true",
    "customer_ready": "output_customer_ready_true",
    "public_ready": "output_public_ready_true",
}

DISALLOWED_IMPORT_PREFIXES = (
    "app.services.controlled_review_queue_candidate",
    "app.services.controlled_evidence_layer_import_candidate",
    "app.services.controlled_evidence_layer_write_candidate",
    "app.services.controlled_evidenceitem_evidence_layer_write_runtime",
    "app.services.controlled_production_case_candidate",
    "app.services.controlled_production_analysis_run_candidate",
    "app.services.controlled_production_analysis_result",
    "app.services.private_collector_package_resolver",
    "app.services.private_collector_provider_result_reader",
    "app.services.local_exchange_reader",
    "app.services.private_collector_review_only_staging",
    "app.services.evidence_import",
    "app.services.evidence_ingestion",
    "app.services.source11_governance_handoff_finalsummaryreport_adapter",
    "app.services.report_candidate_final_report_boundary",
    "app.services.final_summary_report",
    "app.services.export_artifact",
)


def _preview_row(index: int, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "preview_row_id": f"8z11-preview-row-{index:03d}",
        "row_index": index,
        "evidence_id_hash": f"8z11-hash-{index:03d}",
        "evidence_type": "synthetic_note",
        "platform": "synthetic_forum",
        "created_at_date": "2026-07-07",
        "trust_label": "synthetic_fixture",
        "verification_status": "not_official_verification",
        "review_status": "review_only",
        "language": "en",
        "content_visibility": "synthetic_public_sample",
        "access_scope": "synthetic_non_production",
        "text_snippet_redacted": f"8Z-11 redacted non-production snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only", "synthetic_non_production"],
    }
    row.update(overrides)
    return row


def _safe_source_preview(**overrides: object) -> dict[str, object]:
    rows = [_preview_row(1), _preview_row(2)]
    preview: dict[str, object] = {
        "schema": "sentigraph_controlled_row_preview_v0_1",
        "phase": "8W-7",
        "preview_status": "row_preview_warn_manual_review_required",
        "created_local_row_preview": True,
        "row_preview_mode": ROW_PREVIEW_MODE,
        "row_preview_scope": ROW_PREVIEW_SCOPE,
        "source_adapter_schema": SOURCE_ADAPTER_SCHEMA,
        "source_adapter_mode": SOURCE_ADAPTER_MODE,
        "source_boundary_schema": "sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1",
        "source_boundary_phase": "8Z-9",
        "row_source": "evidence_items.jsonl",
        "row_source_policy": "single_approved_jsonl_source_only",
        "row_source_path_exposed": False,
        "absolute_path_exposed": False,
        "package_path_exposed": False,
        "max_preview_rows_applied": 2,
        "max_preview_rows_hard_bound": 10,
        "rows_inspected_count": 2,
        "preview_rows_count": 2,
        "row_limit_enforced": True,
        "warning_count": 1,
        "human_review_required": True,
        "warning_manual_review_preserved": True,
        "no_automatic_trust_upgrade": True,
        "preview_only": True,
        "review_only": True,
        "preview_rows": rows,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_non_production"],
        "runtime_side_effects": {
            "called_real_api": False,
            "called_real_llm": False,
            "ran_provider_job": False,
            "ran_collector": False,
            "accessed_private_collector": False,
            "inspected_private_collector_source": False,
            "read_real_exchange_dir": False,
            "parsed_evidence_items_jsonl_again": False,
            "parsed_evidence_items_csv": False,
            "parsed_source_manifest_jsonl_rows": False,
            "parsed_collection_log_jsonl_rows": False,
            "read_original_package_rows": False,
            "read_private_collector_raw_output": False,
            "emitted_raw_comments": False,
            "emitted_raw_identities": False,
            "emitted_profile_urls": False,
            "wrote_evidence_layer": False,
            "created_evidence_items": False,
            "created_review_queue_items": False,
            "created_production_review_queue_items": False,
            "created_production_case": False,
            "created_production_analysis_run": False,
            "generated_b_end_report_runtime": False,
            "generated_sandbox_runtime": False,
            "generated_public_event_runtime": False,
            "used_report_export_runtime": False,
            "used_download_package_runtime": False,
            "used_public_access_runtime": False,
            "used_external_delivery_runtime": False,
            "used_final_delivery_runtime": False,
            "generated_response_text": False,
            "created_public_route": False,
            "modified_frontend": False,
            "published_or_sent": False,
            "auto_executed": False,
        },
        **{field: False for field in FALSE_SOURCE_FLAGS},
    }
    preview.update(overrides)
    return preview


def _blocked_output(reason: str, *, helper_called: bool = False) -> dict[str, object]:
    return {
        "phase": PHASE,
        "decision": "blocked",
        "privacy_issue_stop": "raw" in reason or "secret" in reason,
        "blockers": [reason],
        "batch_outer_phrase_required": True,
        "helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_evidence_candidate_called": helper_called,
        "controlled_evidence_candidate_created": False,
        "candidate_count": 0,
        "candidate_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in FALSE_OUTPUT_FLAGS},
    }


def _source_blockers(source_preview: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    expected = {
        "schema": ("sentigraph_controlled_row_preview_v0_1", "source_row_preview_schema_wrong"),
        "row_preview_mode": (ROW_PREVIEW_MODE, "source_row_preview_mode_wrong"),
        "row_preview_scope": (ROW_PREVIEW_SCOPE, "source_row_preview_scope_wrong"),
        "source_adapter_schema": (SOURCE_ADAPTER_SCHEMA, "source_adapter_schema_wrong"),
    }
    for field, (expected_value, reason) in expected.items():
        if source_preview.get(field) != expected_value:
            blockers.append(reason)
    if source_preview.get("human_review_required") is not True:
        blockers.append("source_human_review_required_not_true")
    if source_preview.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")
    for field, reason in FALSE_SOURCE_FLAGS.items():
        if source_preview.get(field) is True:
            blockers.append(reason)
    return _dedupe(blockers)


def _output_blockers(output: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    for field, reason in FALSE_OUTPUT_FLAGS.items():
        if output.get(field) is True:
            blockers.append(reason)
    return _dedupe(blockers)


def _ready_output(source_preview: dict[str, object], candidate_set: dict[str, Any]) -> dict[str, object]:
    candidate_schema = None
    candidates = candidate_set.get("candidates")
    if isinstance(candidates, list) and candidates:
        first = candidates[0]
        if isinstance(first, dict):
            candidate_schema = first.get("candidate_schema")
    output: dict[str, object] = {
        "phase": PHASE,
        "decision": "ready",
        "privacy_issue_stop": False,
        "batch_outer_phrase_required": True,
        "helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_evidence_candidate_called": True,
        "controlled_evidence_candidate_created": True,
        "evidence_candidate_schema": candidate_schema,
        "evidence_candidate_set_schema": candidate_set["candidate_set_schema"],
        "evidence_candidate_mode": "backend_only_local_controlled_evidence_candidate",
        "source_row_preview_schema": source_preview["schema"],
        "source_row_preview_mode": source_preview["row_preview_mode"],
        "source_row_preview_scope": source_preview["row_preview_scope"],
        "source_adapter_schema": source_preview["source_adapter_schema"],
        "candidate_count": candidate_set["candidate_count"],
        "candidate_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_non_production"],
        **{field: False for field in FALSE_OUTPUT_FLAGS},
    }
    output_blockers = _output_blockers(output)
    if output_blockers:
        output["decision"] = "blocked"
        output["blockers"] = output_blockers
        output["controlled_evidence_candidate_created"] = False
    return output


def build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
    *,
    batch_approval_phrase: str | None,
    helper_approval_phrase: str | None,
    source_preview: dict[str, object] | None = None,
    output_overrides: dict[str, object] | None = None,
) -> dict[str, object]:
    if batch_approval_phrase != BATCH_APPROVAL_PHRASE:
        return _blocked_output("blocked_missing_exact_8z10a_11_batch_approval", helper_called=False)

    preview = source_preview if source_preview is not None else _safe_source_preview()
    blockers = _source_blockers(preview)
    if blockers:
        return _blocked_output(blockers[0], helper_called=False)

    candidate_set = evidence_candidate_module.build_controlled_evidence_candidate_set(
        preview,
        exact_approval_phrase=helper_approval_phrase,
    )
    if candidate_set["evidence_candidate_created"] is not True:
        return _blocked_output(str(candidate_set["blockers"][0]), helper_called=True)

    output = _ready_output(preview, candidate_set)
    if output_overrides:
        output.update(output_overrides)
    output_blockers = _output_blockers(output)
    if output_blockers:
        output["decision"] = "blocked"
        output["blockers"] = output_blockers
        output["controlled_evidence_candidate_created"] = False
    return output


def install_no_file_or_downstream_guard(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-11 must not read files")

    original_import = builtins.__import__

    def guarded_import(name: str, *args: object, **kwargs: object):
        if name.startswith(DISALLOWED_IMPORT_PREFIXES):
            raise AssertionError(f"disallowed downstream import attempted: {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)
    monkeypatch.setattr(builtins, "__import__", guarded_import)


def _assert_false_side_effects(output: dict[str, object]) -> None:
    for field in FALSE_OUTPUT_FLAGS:
        assert output[field] is False, field


def _assert_no_forbidden_output(output: dict[str, object]) -> None:
    serialized = json.dumps(output, sort_keys=True, ensure_ascii=False)
    assert "http://" not in serialized
    assert "https://" not in serialized
    assert "raw_author" not in serialized
    assert '"profile_url":' not in serialized
    assert "actual-profile-url" not in serialized
    assert "cookie=" not in serialized
    assert "token=" not in serialized
    assert ".env" not in serialized


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def test_8z11_creates_local_evidence_candidate_only_in_controlled_backend_test_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_no_file_or_downstream_guard(monkeypatch)

    result = build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
        batch_approval_phrase=BATCH_APPROVAL_PHRASE,
        helper_approval_phrase=HELPER_APPROVAL_PHRASE,
    )

    assert result["decision"] == "ready"
    assert result["controlled_evidence_candidate_called"] is True
    assert result["controlled_evidence_candidate_created"] is True
    assert result["evidence_candidate_schema"] == "sentigraph_controlled_evidence_candidate_v0_1"
    assert result["evidence_candidate_set_schema"] == "sentigraph_controlled_evidence_candidate_set_v0_1"
    assert result["evidence_candidate_mode"] == "backend_only_local_controlled_evidence_candidate"
    assert result["source_row_preview_schema"] == "sentigraph_controlled_row_preview_v0_1"
    assert result["candidate_only"] is True
    assert result["review_only"] is True
    assert result["human_review_required"] is True
    assert result["no_automatic_trust_upgrade"] is True
    assert result["batch_outer_phrase_required"] is True
    assert result["helper_inner_phrase_required"] is True
    assert result["helper_inner_phrase_alone_authorizes_batch"] is False
    assert result["old_chinese_or_mojibake_helper_phrase_accepted"] is False
    _assert_false_side_effects(result)
    _assert_no_forbidden_output(result)


@pytest.mark.parametrize(
    "batch_phrase",
    [
        None,
        "",
        "wrong",
        INACTIVE_STANDALONE_8Z11_PHRASE,
        "APPROVE_8Z_10_ROUTE_C_ROW_PREVIEW_COMPLETION_EVIDENCE_CANDIDATE_GATE_DECISION_DOCS_ONLY",
        "APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE",
        "APPROVE_8Z_8C_NO_REAL_ROW_ADAPTER_COMPLETION_ROUTE_C_ROW_PREVIEW_REGATE_DECISION_DOCS_ONLY",
        "APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE",
        HELPER_APPROVAL_PHRASE,
    ],
)
def test_batch_phrase_required_before_helper_call(batch_phrase: str | None) -> None:
    result = build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
        batch_approval_phrase=batch_phrase,
        helper_approval_phrase=HELPER_APPROVAL_PHRASE,
    )

    assert result["decision"] == "blocked"
    assert result["controlled_evidence_candidate_called"] is False
    assert result["controlled_evidence_candidate_created"] is False
    assert result["blockers"] == ["blocked_missing_exact_8z10a_11_batch_approval"]
    _assert_false_side_effects(result)


@pytest.mark.parametrize(
    "helper_phrase",
    [
        None,
        "",
        "wrong",
        BATCH_APPROVAL_PHRASE,
        OLD_CHINESE_HELPER_PHRASE,
        OLD_MOJIBAKE_HELPER_PHRASE,
        OLD_GARBLED_HELPER_PHRASE,
    ],
)
def test_helper_phrase_required_at_helper_layer(helper_phrase: str | None, monkeypatch: pytest.MonkeyPatch) -> None:
    install_no_file_or_downstream_guard(monkeypatch)

    result = build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
        batch_approval_phrase=BATCH_APPROVAL_PHRASE,
        helper_approval_phrase=helper_phrase,
    )

    assert result["decision"] == "blocked"
    assert result["controlled_evidence_candidate_called"] is True
    assert result["controlled_evidence_candidate_created"] is False
    assert result["blockers"] == ["blocked_missing_exact_approval"]
    _assert_false_side_effects(result)


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("schema", "wrong", "source_row_preview_schema_wrong"),
        ("real_exchange_dir_read", True, "source_real_exchange_dir_read_true"),
        ("real_package_dir_read", True, "source_real_package_dir_read_true"),
        ("production_package_rows_parsed", True, "source_production_package_rows_parsed_true"),
        ("raw_rows_exposed", True, "source_raw_rows_exposed_true"),
        ("raw_comments_exposed", True, "source_raw_comments_exposed_true"),
        ("raw_identities_exposed", True, "source_raw_identities_exposed_true"),
        ("author_names_or_profile_urls_exposed", True, "source_author_identity_exposed_true"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("production_evidence_item_created", True, "source_production_evidence_item_created_true"),
        ("actual_review_queue_runtime_used", True, "source_review_queue_runtime_used_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("production_analysis_result_created", True, "source_analysis_result_created_true"),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
        ("human_review_required", False, "source_human_review_required_not_true"),
    ],
)
def test_unsafe_source_preview_blocks_before_evidence_candidate_call(
    field: str,
    value: object,
    reason: str,
) -> None:
    result = build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
        batch_approval_phrase=BATCH_APPROVAL_PHRASE,
        helper_approval_phrase=HELPER_APPROVAL_PHRASE,
        source_preview=_safe_source_preview(**{field: value}),
    )

    assert result["decision"] == "blocked"
    assert result["controlled_evidence_candidate_called"] is False
    assert result["controlled_evidence_candidate_created"] is False
    assert reason in result["blockers"]
    _assert_false_side_effects(result)


@pytest.mark.parametrize("field", list(FALSE_OUTPUT_FLAGS))
def test_unsafe_output_attempts_block(field: str, monkeypatch: pytest.MonkeyPatch) -> None:
    install_no_file_or_downstream_guard(monkeypatch)

    result = build_8z11_controlled_row_preview_to_evidence_candidate_smoke(
        batch_approval_phrase=BATCH_APPROVAL_PHRASE,
        helper_approval_phrase=HELPER_APPROVAL_PHRASE,
        output_overrides={field: True},
    )

    assert result["decision"] == "blocked"
    assert result["controlled_evidence_candidate_created"] is False
    assert FALSE_OUTPUT_FLAGS[field] in result["blockers"]
