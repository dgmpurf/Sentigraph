from __future__ import annotations

import builtins
import importlib
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_evidence_candidate as evidence_candidate_module
import app.services.controlled_evidence_layer_import_candidate as import_candidate_module
import app.services.controlled_evidence_layer_write_candidate as write_candidate_module
import app.services.controlled_review_queue_candidate as review_queue_module


APPROVAL_PHRASE = "APPROVE_8Z_16_INTERNAL_ALPHA_NO_WRITE_END_TO_END_SMOKE"
ROW_PREVIEW_HELPER_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
EVIDENCE_CANDIDATE_HELPER_PHRASE = "APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION"
REVIEW_QUEUE_HELPER_PHRASE = "APPROVE_8W_13_CONTROLLED_REVIEW_QUEUE_CANDIDATE_IMPLEMENTATION"
IMPORT_CANDIDATE_HELPER_PHRASE = "APPROVE_8W_16_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_IMPLEMENTATION"
WRITE_CANDIDATE_HELPER_PHRASE = "APPROVE_8W_19_CONTROLLED_EVIDENCE_LAYER_WRITE_CANDIDATE_IMPLEMENTATION"

OLD_OUTER_PHRASES = (
    "APPROVE_8Z_14_15_BATCH_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_BOUNDARY_SMOKE",
    "APPROVE_8Z_12_13_BATCH_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_AND_IMPORT_CANDIDATE_SMOKE",
    "APPROVE_8Z_11_CONTROLLED_ROUTE_C_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SMOKE",
    "APPROVE_8Y_12_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_SMOKE",
    "APPROVE_8W_19_CONTROLLED_EVIDENCE_LAYER_WRITE_CANDIDATE_IMPLEMENTATION",
)
OLD_HELPER_PHRASES = (
    "批准 8W-7 Controlled Row Preview Implementation",
    "鎵瑰噯 8W-7 Controlled Row Preview Implementation",
    "閹电懓鍣?8W-7 Controlled Row Preview Implementation",
    "闁圭數鎳撻崳?8W-7 Controlled Row Preview Implementation",
    "鎵瑰噯 8W-10 Controlled Evidence Candidate Implementation",
)

PHASE = "8Z-16"
INTERNAL_ALPHA_SCHEMA = "sentigraph_8z_internal_alpha_no_write_chain_v0_1"
INTERNAL_ALPHA_MODE = "backend_only_local_no_write_internal_alpha"

FALSE_FLAGS = {
    "actual_evidence_layer_write_used": "actual_evidence_layer_write_used_true",
    "evidence_layer_write": "evidence_layer_write_true",
    "persisted_evidence_layer_record_created": "persisted_evidence_layer_record_created_true",
    "production_evidence_item_created": "production_evidence_item_created_true",
    "production_evidenceitem_write_runtime_used": "production_evidenceitem_write_runtime_used_true",
    "evidenceitem_write_runtime_called": "evidenceitem_write_runtime_called_true",
    "production_import_candidate_created": "production_import_candidate_created_true",
    "production_import_derived_write_candidate_created": "production_import_derived_write_candidate_created_true",
    "production_case_created": "production_case_created_true",
    "production_analysis_run_created": "production_analysis_run_created_true",
    "actual_analysis_execution_started": "actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": "production_analysis_result_creation_authorized_true",
    "production_analysis_result_created": "production_analysis_result_created_true",
    "actual_review_queue_runtime_used": "actual_review_queue_runtime_used_true",
    "production_review_queue_item_created": "production_review_queue_item_created_true",
    "downstream_route_c_auto_run": "downstream_route_c_auto_run_true",
    "source11_runtime_called": "source11_runtime_called_true",
    "actual_final_summary_report_created": "actual_final_summary_report_created_true",
    "b_end_report_runtime_generated": "b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "sandbox_public_event_runtime_generated_true",
    "export_download_public_delivery_created": "export_download_public_delivery_created_true",
    "route_changed": "route_changed_true",
    "frontend_changed": "frontend_changed_true",
    "runtime_changed": "runtime_changed_true",
    "route_ready": "route_ready_true",
    "frontend_ready": "frontend_ready_true",
    "production_ready": "production_ready_true",
    "customer_ready": "customer_ready_true",
    "public_ready": "public_ready_true",
    "real_exchange_dir_read": "real_exchange_dir_read_true",
    "real_package_dir_read": "real_package_dir_read_true",
    "production_package_rows_parsed": "production_package_rows_parsed_true",
    "original_package_rows_read": "original_package_rows_read_true",
    "arbitrary_package_dir_read": "arbitrary_package_dir_read_true",
    "evidence_items_csv_parsed": "evidence_items_csv_parsed_true",
    "source_manifest_rows_parsed": "source_manifest_rows_parsed_true",
    "collection_log_rows_parsed": "collection_log_rows_parsed_true",
    "source_manifest_file_opened": "source_manifest_file_opened_true",
    "collection_log_file_opened": "collection_log_file_opened_true",
    "package_resolver_called": "package_resolver_called_true",
    "provider_result_reader_called": "provider_result_reader_called_true",
    "local_exchange_reader_called": "local_exchange_reader_called_true",
    "collector_job_run": "collector_job_run_true",
    "provider_job_run": "provider_job_run_true",
    "scheduler_created": "scheduler_created_true",
    "http_bridge_created": "http_bridge_created_true",
    "webhook_created": "webhook_created_true",
    "private_collector_source_inspected": "private_collector_source_inspected_true",
    "raw_rows_exposed": "raw_rows_exposed_true",
    "raw_comments_exposed": "raw_comments_exposed_true",
    "raw_identities_exposed": "raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "author_names_or_profile_urls_exposed_true",
    "secrets_read": "secrets_read_true",
    "real_api_called": "real_api_called_true",
    "real_llm_called": "real_llm_called_true",
    "url_fetching_performed": "url_fetching_performed_true",
    "scraping_performed": "scraping_performed_true",
}

RUNTIME_FLAGS = {
    "called_real_api": False,
    "called_real_llm": False,
    "ran_collector": False,
    "ran_provider_job": False,
    "accessed_private_collector": False,
    "inspected_private_collector_source": False,
    "read_real_exchange_dir": False,
    "fetched_url": False,
    "scraped_page": False,
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
    "created_evidence_item": False,
    "created_evidence_items": False,
    "created_production_evidence_items": False,
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
}

STAGE_FIELDS = {
    "request_metadata_fixture": "request_metadata_fixture_created",
    "provider_result_metadata_fixture": "provider_result_metadata_fixture_created",
    "request_result_correlation": "request_result_correlation_created",
    "review_only_staging_candidate": "review_only_staging_candidate_created",
    "no_real_row_route_c_row_preview_entry_adapter": "no_real_row_route_c_row_preview_entry_adapter_created",
    "route_c_row_preview_entry_candidate": "route_c_row_preview_entry_candidate_created",
}

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/AICODING/网页端任务二",
    "G:/private-collector/should-never-appear",
)


def _runtime_side_effects(**overrides: bool) -> dict[str, bool]:
    flags = dict(RUNTIME_FLAGS)
    flags.update(overrides)
    return flags


def _false_flags(**overrides: bool) -> dict[str, bool]:
    flags = {field: False for field in FALSE_FLAGS}
    flags.update(overrides)
    return flags


def _stage(stage: str, **overrides: object) -> dict[str, object]:
    field = STAGE_FIELDS[stage]
    value: dict[str, object] = {
        "stage": stage,
        field: True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "preview_only": True,
        "local_only": True,
        "backend_only": True,
        "runtime_side_effects": _runtime_side_effects(),
        **_false_flags(),
    }
    value.update(overrides)
    return value


def _row_preview_fixture(**overrides: object) -> dict[str, object]:
    preview: dict[str, object] = {
        "schema": "sentigraph_controlled_row_preview_v0_1",
        "phase": "8W-7",
        "preview_status": "row_preview_warn_manual_review_required",
        "row_preview_mode": "backend_only_local_controlled_route_c_row_preview_smoke",
        "row_preview_scope": "in_memory_non_production_fixture_only",
        "row_source": "evidence_items.jsonl",
        "row_source_policy": "single_approved_jsonl_source_only",
        "created_local_row_preview": True,
        "redacted_review_only_row_preview_created": True,
        "preview_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "row_limit_enforced": True,
        "max_preview_rows_applied": 2,
        "max_preview_rows_hard_bound": 10,
        "rows_inspected_count": 2,
        "preview_rows_count": 2,
        "warning_count": 1,
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_non_production"],
        "blockers": [],
        "runtime_side_effects": _runtime_side_effects(),
        "preview_rows": [
            {
                "preview_row_id": "8z16-preview-row-001",
                "row_index": 1,
                "evidence_id_hash": "8z16-hash-001",
                "evidence_type": "comment",
                "platform": "synthetic_forum",
                "created_at_date": "2026-07-07",
                "trust_label": "synthetic_fixture",
                "verification_status": "not_official_verification",
                "review_status": "review_needed",
                "language": "zh",
                "content_visibility": "public_sample_redacted",
                "access_scope": "selected_public_sample",
                "text_snippet_redacted": "8Z-16 redacted non-production row preview one.",
                "redaction_status": "redacted",
                "redaction_warnings": ["synthetic_non_production"],
            },
            {
                "preview_row_id": "8z16-preview-row-002",
                "row_index": 2,
                "evidence_id_hash": "8z16-hash-002",
                "evidence_type": "post",
                "platform": "synthetic_forum",
                "created_at_date": "2026-07-07",
                "trust_label": "synthetic_fixture",
                "verification_status": "not_official_verification",
                "review_status": "review_needed",
                "language": "zh",
                "content_visibility": "public_sample_redacted",
                "access_scope": "selected_public_sample",
                "text_snippet_redacted": "8Z-16 redacted non-production row preview two.",
                "redaction_status": "redacted",
                "redaction_warnings": ["synthetic_non_production"],
            },
        ],
        **_false_flags(),
    }
    preview.update(overrides)
    return preview


def _blocked(reason: str, *, chain_executed: bool = False) -> dict[str, object]:
    return {
        "phase": PHASE,
        "decision": "blocked",
        "privacy_issue_stop": "raw" in reason or "secret" in reason or "identity" in reason,
        "blockers": [reason],
        "internal_alpha_no_write_end_to_end_smoke_executed": chain_executed,
        "internal_alpha_schema": INTERNAL_ALPHA_SCHEMA,
        "internal_alpha_mode": INTERNAL_ALPHA_MODE,
        "final_chain_boundary": "evidence_layer_write_candidate_boundary",
        "internal_alpha_no_write_checkpoint_reached": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "8w69_pause_preserved": True,
        "8w70_reactivation_selected": False,
        **{field: False for field in STAGE_FIELDS.values()},
        "route_c_row_preview_entry_candidate_created": False,
        "redacted_review_only_row_preview_created": False,
        "controlled_evidence_candidate_created": False,
        "controlled_review_queue_candidate_created": False,
        "controlled_evidence_layer_import_candidate_created": False,
        "controlled_evidence_layer_write_candidate_created": False,
        "write_candidate_created": False,
        **_false_flags(),
    }


def _source_blockers(stage: dict[str, object], stage_name: str) -> list[str]:
    blockers: list[str] = []
    if stage.get("human_review_required") is not True:
        blockers.append(f"{stage_name}_human_review_required_not_true")
    if stage.get("no_automatic_trust_upgrade") is not True:
        blockers.append(f"{stage_name}_no_automatic_trust_upgrade_not_true")
    for field, reason in FALSE_FLAGS.items():
        if stage.get(field) is True:
            blockers.append(f"{stage_name}_{reason}")
    runtime_side_effects = stage.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append(f"{stage_name}_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"{stage_name}_runtime_side_effect_true:{flag}")
    return blockers


def _output_blockers(output: dict[str, Any], label: str) -> list[str]:
    blockers: list[str] = []
    for field, reason in FALSE_FLAGS.items():
        if output.get(field) is True:
            blockers.append(f"{label}_{reason}")
    runtime_side_effects = output.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"{label}_runtime_side_effect_true:{flag}")
    return blockers


def _created_or_blocked(output: dict[str, Any], created_field: str, label: str) -> str | None:
    if output.get(created_field) is True:
        return None
    blockers = output.get("blockers")
    first_blocker = blockers[0] if isinstance(blockers, list) and blockers else f"{created_field}_not_true"
    return f"{label}_blocked:{first_blocker}"


def _build_internal_alpha_no_write_chain(
    *,
    approval_phrase: str | None,
    helper_phrases: dict[str, str | None] | None = None,
    stage_overrides: dict[str, dict[str, object]] | None = None,
) -> dict[str, object]:
    if approval_phrase is None or approval_phrase == "":
        return _blocked("blocked_missing_exact_8z16_internal_alpha_approval")
    if approval_phrase != APPROVAL_PHRASE:
        return _blocked("blocked_wrong_exact_8z16_internal_alpha_approval")

    helper_phrases = helper_phrases or {}
    stage_overrides = stage_overrides or {}

    stages = {
        stage_name: _stage(stage_name, **stage_overrides.get(stage_name, {}))
        for stage_name in STAGE_FIELDS
    }
    for stage_name, stage in stages.items():
        blockers = _source_blockers(stage, stage_name)
        if blockers:
            return _blocked(blockers[0], chain_executed=True)

    row_preview = _row_preview_fixture(**stage_overrides.get("row_preview", {}))
    blockers = _source_blockers(row_preview, "row_preview")
    if blockers:
        return _blocked(blockers[0], chain_executed=True)

    evidence_candidate_set = evidence_candidate_module.build_controlled_evidence_candidate_set(
        row_preview,
        exact_approval_phrase=helper_phrases.get("evidence", EVIDENCE_CANDIDATE_HELPER_PHRASE),
    )
    blockers = _output_blockers(evidence_candidate_set, "evidence_candidate_helper")
    if blockers:
        return _blocked(blockers[0], chain_executed=True)
    not_created = _created_or_blocked(evidence_candidate_set, "evidence_candidate_created", "evidence_candidate_helper")
    if not_created:
        return _blocked(not_created, chain_executed=True)

    review_queue_set = review_queue_module.build_controlled_review_queue_candidate_set(
        evidence_candidate_set,
        exact_approval_phrase=helper_phrases.get("review_queue", REVIEW_QUEUE_HELPER_PHRASE),
    )
    blockers = _output_blockers(review_queue_set, "review_queue_helper")
    if blockers:
        return _blocked(blockers[0], chain_executed=True)
    not_created = _created_or_blocked(review_queue_set, "review_queue_candidate_created", "review_queue_helper")
    if not_created:
        return _blocked(not_created, chain_executed=True)

    import_candidate_set = import_candidate_module.build_controlled_evidence_layer_import_candidate_set(
        review_queue_set,
        exact_approval_phrase=helper_phrases.get("import_candidate", IMPORT_CANDIDATE_HELPER_PHRASE),
    )
    blockers = _output_blockers(import_candidate_set, "import_candidate_helper")
    if blockers:
        return _blocked(blockers[0], chain_executed=True)
    not_created = _created_or_blocked(
        import_candidate_set,
        "evidence_layer_import_candidate_created",
        "import_candidate_helper",
    )
    if not_created:
        return _blocked(not_created, chain_executed=True)

    write_candidate_set = write_candidate_module.build_controlled_evidence_layer_write_candidate_set(
        import_candidate_set,
        exact_approval_phrase=helper_phrases.get("write_candidate", WRITE_CANDIDATE_HELPER_PHRASE),
    )
    blockers = _output_blockers(write_candidate_set, "write_candidate_helper")
    if blockers:
        return _blocked(blockers[0], chain_executed=True)
    not_created = _created_or_blocked(
        write_candidate_set,
        "evidence_layer_write_candidate_created",
        "write_candidate_helper",
    )
    if not_created:
        return _blocked(not_created, chain_executed=True)

    return {
        "phase": PHASE,
        "decision": "ready",
        "privacy_issue_stop": False,
        "blockers": [],
        "internal_alpha_no_write_end_to_end_smoke_executed": True,
        "internal_alpha_schema": INTERNAL_ALPHA_SCHEMA,
        "internal_alpha_mode": INTERNAL_ALPHA_MODE,
        "final_chain_boundary": "evidence_layer_write_candidate_boundary",
        "internal_alpha_no_write_checkpoint_reached": True,
        "helper_inner_phrase_alone_authorizes_internal_alpha": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "8w69_pause_preserved": True,
        "8w70_reactivation_selected": False,
        **{field: True for field in STAGE_FIELDS.values()},
        "route_c_row_preview_entry_candidate_created": True,
        "redacted_review_only_row_preview_created": True,
        "controlled_evidence_candidate_created": True,
        "controlled_review_queue_candidate_created": True,
        "controlled_evidence_layer_import_candidate_created": True,
        "controlled_evidence_layer_write_candidate_created": True,
        "write_candidate_created": True,
        "evidence_candidate_count": evidence_candidate_set["candidate_count"],
        "review_queue_candidate_count": review_queue_set["review_queue_candidate_count"],
        "evidence_layer_import_candidate_count": import_candidate_set["evidence_layer_import_candidate_count"],
        "evidence_layer_write_candidate_count": write_candidate_set["evidence_layer_write_candidate_count"],
        "stage_safety": {
            stage_name: {
                "human_review_required": True,
                "no_automatic_trust_upgrade": True,
            }
            for stage_name in [
                *STAGE_FIELDS,
                "row_preview",
                "evidence_candidate",
                "review_queue_candidate",
                "evidence_layer_import_candidate",
                "evidence_layer_write_candidate",
            ]
        },
        **_false_flags(),
    }


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_no_forbidden_flags(output: dict[str, object]) -> None:
    for field in FALSE_FLAGS:
        assert output[field] is False, field


def _assert_blocked(output: dict[str, object], expected_reason: str) -> None:
    assert output["decision"] == "blocked"
    assert output["blockers"] == [expected_reason]
    assert output["internal_alpha_no_write_checkpoint_reached"] is False
    assert output["controlled_evidence_layer_write_candidate_created"] is False
    assert output["write_candidate_created"] is False
    _assert_no_forbidden_flags(output)
    _assert_safe_output(output)


def _patch_forbidden_file_and_runtime_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-16 no-write smoke must not read files")

    def fail_runtime_call(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-16 no-write smoke must not call runtime, collector, provider, or production helpers")

    module_names = [
        "app.services.local_exchange_reader",
        "app.services.evidence_import",
        "app.services.evidence_ingestion",
        "app.services.controlled_evidenceitem_evidence_layer_write_runtime",
        "app.services.controlled_evidence_layer_write_candidate_from_production_import_candidate",
        "app.services.controlled_production_evidence_import_candidate",
        "app.services.controlled_production_case_candidate",
        "app.services.controlled_production_analysis_run_candidate",
        "app.services.controlled_actual_analysis_execution_candidate",
        "app.services.controlled_production_analysis_result_candidate",
        "app.services.controlled_final_summary_report",
        "app.services.report_export_download_package",
        "app.services.report_export_public_access_external_delivery_gate",
    ]
    function_fragments = (
        "resolve",
        "read",
        "import",
        "ingest",
        "write",
        "create",
        "run",
        "execute",
        "collect",
        "provider",
        "analysis_result",
        "final_summary",
        "export",
        "delivery",
    )
    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        for name in dir(module):
            if name.startswith("_"):
                continue
            attr = getattr(module, name)
            if callable(attr) and any(fragment in name.lower() for fragment in function_fragments):
                monkeypatch.setattr(module, name, fail_runtime_call)

    monkeypatch.setattr(builtins, "open", fail_file_access)
    monkeypatch.setattr(Path, "open", fail_file_access)
    monkeypatch.setattr(Path, "read_text", fail_file_access)
    monkeypatch.setattr(Path, "read_bytes", fail_file_access)


def test_internal_alpha_chain_reaches_write_candidate_boundary_without_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_forbidden_file_and_runtime_entrypoints(monkeypatch)

    output = _build_internal_alpha_no_write_chain(approval_phrase=APPROVAL_PHRASE)

    assert output["decision"] == "ready"
    assert output["internal_alpha_no_write_end_to_end_smoke_executed"] is True
    assert output["internal_alpha_schema"] == INTERNAL_ALPHA_SCHEMA
    assert output["internal_alpha_mode"] == INTERNAL_ALPHA_MODE
    assert output["final_chain_boundary"] == "evidence_layer_write_candidate_boundary"
    assert output["internal_alpha_no_write_checkpoint_reached"] is True
    assert output["request_metadata_fixture_created"] is True
    assert output["provider_result_metadata_fixture_created"] is True
    assert output["request_result_correlation_created"] is True
    assert output["review_only_staging_candidate_created"] is True
    assert output["no_real_row_route_c_row_preview_entry_adapter_created"] is True
    assert output["route_c_row_preview_entry_candidate_created"] is True
    assert output["redacted_review_only_row_preview_created"] is True
    assert output["controlled_evidence_candidate_created"] is True
    assert output["controlled_review_queue_candidate_created"] is True
    assert output["controlled_evidence_layer_import_candidate_created"] is True
    assert output["controlled_evidence_layer_write_candidate_created"] is True
    assert output["write_candidate_created"] is True
    assert output["evidence_candidate_count"] == 2
    assert output["review_queue_candidate_count"] == 2
    assert output["evidence_layer_import_candidate_count"] == 2
    assert output["evidence_layer_write_candidate_count"] == 2
    assert output["human_review_required"] is True
    assert output["no_automatic_trust_upgrade"] is True
    assert output["8w69_pause_preserved"] is True
    assert output["8w70_reactivation_selected"] is False
    for stage_safety in output["stage_safety"].values():
        assert stage_safety["human_review_required"] is True
        assert stage_safety["no_automatic_trust_upgrade"] is True
    _assert_no_forbidden_flags(output)
    _assert_safe_output(output)


@pytest.mark.parametrize("approval_phrase", [None, "", "wrong approval", *OLD_OUTER_PHRASES])
def test_outer_8z16_phrase_required_before_chain_execution(
    approval_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_helper_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-16 helper chain must not run without exact outer approval")

    monkeypatch.setattr(
        evidence_candidate_module,
        "build_controlled_evidence_candidate_set",
        fail_if_helper_called,
    )
    output = _build_internal_alpha_no_write_chain(approval_phrase=approval_phrase)
    expected = (
        "blocked_missing_exact_8z16_internal_alpha_approval"
        if approval_phrase in {None, ""}
        else "blocked_wrong_exact_8z16_internal_alpha_approval"
    )
    _assert_blocked(output, expected)
    assert output["internal_alpha_no_write_end_to_end_smoke_executed"] is False


@pytest.mark.parametrize(
    "approval_phrase",
    [
        ROW_PREVIEW_HELPER_PHRASE,
        EVIDENCE_CANDIDATE_HELPER_PHRASE,
        REVIEW_QUEUE_HELPER_PHRASE,
        IMPORT_CANDIDATE_HELPER_PHRASE,
        WRITE_CANDIDATE_HELPER_PHRASE,
    ],
)
def test_helper_inner_phrases_alone_do_not_authorize_internal_alpha(
    approval_phrase: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_helper_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("helper phrase alone must block before helper chain")

    monkeypatch.setattr(
        evidence_candidate_module,
        "build_controlled_evidence_candidate_set",
        fail_if_helper_called,
    )
    output = _build_internal_alpha_no_write_chain(approval_phrase=approval_phrase)
    _assert_blocked(output, "blocked_wrong_exact_8z16_internal_alpha_approval")
    assert output["internal_alpha_no_write_end_to_end_smoke_executed"] is False


@pytest.mark.parametrize(
    ("helper_name", "expected_prefix"),
    [
        ("evidence", "evidence_candidate_helper"),
        ("review_queue", "review_queue_helper"),
        ("import_candidate", "import_candidate_helper"),
        ("write_candidate", "write_candidate_helper"),
    ],
)
@pytest.mark.parametrize("helper_phrase", [None, "", "wrong approval", *OLD_HELPER_PHRASES])
def test_helper_phrases_remain_required_at_helper_layer(
    helper_name: str,
    expected_prefix: str,
    helper_phrase: str | None,
) -> None:
    output = _build_internal_alpha_no_write_chain(
        approval_phrase=APPROVAL_PHRASE,
        helper_phrases={helper_name: helper_phrase},
    )
    if helper_name == "evidence":
        expected_inner = "blocked_missing_exact_approval"
    else:
        expected_inner = "blocked_missing_exact_approval" if helper_phrase in {None, ""} else "blocked_wrong_exact_approval"
    _assert_blocked(output, f"{expected_prefix}_blocked:{expected_inner}")
    assert output["internal_alpha_no_write_end_to_end_smoke_executed"] is True


@pytest.mark.parametrize(
    ("stage_name", "field", "value", "expected_reason"),
    [
        ("request_metadata_fixture", "evidence_layer_write", True, "request_metadata_fixture_evidence_layer_write_true"),
        (
            "provider_result_metadata_fixture",
            "production_evidence_item_created",
            True,
            "provider_result_metadata_fixture_production_evidence_item_created_true",
        ),
        (
            "request_result_correlation",
            "actual_review_queue_runtime_used",
            True,
            "request_result_correlation_actual_review_queue_runtime_used_true",
        ),
        (
            "review_only_staging_candidate",
            "production_review_queue_item_created",
            True,
            "review_only_staging_candidate_production_review_queue_item_created_true",
        ),
        (
            "no_real_row_route_c_row_preview_entry_adapter",
            "production_case_created",
            True,
            "no_real_row_route_c_row_preview_entry_adapter_production_case_created_true",
        ),
        (
            "route_c_row_preview_entry_candidate",
            "production_analysis_run_created",
            True,
            "route_c_row_preview_entry_candidate_production_analysis_run_created_true",
        ),
        (
            "row_preview",
            "production_analysis_result_created",
            True,
            "row_preview_production_analysis_result_created_true",
        ),
        ("row_preview", "source11_runtime_called", True, "row_preview_source11_runtime_called_true"),
        (
            "provider_result_metadata_fixture",
            "actual_final_summary_report_created",
            True,
            "provider_result_metadata_fixture_actual_final_summary_report_created_true",
        ),
        ("request_metadata_fixture", "real_exchange_dir_read", True, "request_metadata_fixture_real_exchange_dir_read_true"),
        ("request_metadata_fixture", "real_package_dir_read", True, "request_metadata_fixture_real_package_dir_read_true"),
        (
            "request_metadata_fixture",
            "production_package_rows_parsed",
            True,
            "request_metadata_fixture_production_package_rows_parsed_true",
        ),
        ("request_metadata_fixture", "raw_rows_exposed", True, "request_metadata_fixture_raw_rows_exposed_true"),
        ("request_metadata_fixture", "raw_comments_exposed", True, "request_metadata_fixture_raw_comments_exposed_true"),
        ("request_metadata_fixture", "raw_identities_exposed", True, "request_metadata_fixture_raw_identities_exposed_true"),
        (
            "request_metadata_fixture",
            "author_names_or_profile_urls_exposed",
            True,
            "request_metadata_fixture_author_names_or_profile_urls_exposed_true",
        ),
        (
            "request_metadata_fixture",
            "human_review_required",
            False,
            "request_metadata_fixture_human_review_required_not_true",
        ),
        (
            "request_metadata_fixture",
            "no_automatic_trust_upgrade",
            False,
            "request_metadata_fixture_no_automatic_trust_upgrade_not_true",
        ),
    ],
)
def test_unsafe_stage_source_blocks_before_downstream(
    stage_name: str,
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_if_evidence_helper_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("unsafe upstream stage must block before Evidence candidate helper")

    if stage_name != "row_preview":
        monkeypatch.setattr(
            evidence_candidate_module,
            "build_controlled_evidence_candidate_set",
            fail_if_evidence_helper_called,
        )
    output = _build_internal_alpha_no_write_chain(
        approval_phrase=APPROVAL_PHRASE,
        stage_overrides={stage_name: {field: value}},
    )
    _assert_blocked(output, expected_reason)


@pytest.mark.parametrize(
    ("field", "expected_reason"),
    [
        ("evidence_layer_write", "write_candidate_helper_evidence_layer_write_true"),
        ("actual_evidence_layer_write_used", "write_candidate_helper_actual_evidence_layer_write_used_true"),
        ("persisted_evidence_layer_record_created", "write_candidate_helper_persisted_evidence_layer_record_created_true"),
        ("production_evidence_item_created", "write_candidate_helper_production_evidence_item_created_true"),
        ("production_evidenceitem_write_runtime_used", "write_candidate_helper_production_evidenceitem_write_runtime_used_true"),
        ("evidenceitem_write_runtime_called", "write_candidate_helper_evidenceitem_write_runtime_called_true"),
        ("route_ready", "write_candidate_helper_route_ready_true"),
        ("frontend_ready", "write_candidate_helper_frontend_ready_true"),
        ("production_ready", "write_candidate_helper_production_ready_true"),
        ("public_ready", "write_candidate_helper_public_ready_true"),
        ("export_download_public_delivery_created", "write_candidate_helper_export_download_public_delivery_created_true"),
    ],
)
def test_write_candidate_helper_output_with_forbidden_side_effect_blocks(
    field: str,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unsafe_write_candidate_output(*args: object, **kwargs: object) -> dict[str, object]:
        return {
            "evidence_layer_write_candidate_created": True,
            "evidence_layer_write_candidate_count": 2,
            "runtime_side_effects": _runtime_side_effects(),
            "blockers": [],
            field: True,
        }

    monkeypatch.setattr(
        write_candidate_module,
        "build_controlled_evidence_layer_write_candidate_set",
        unsafe_write_candidate_output,
    )

    output = _build_internal_alpha_no_write_chain(approval_phrase=APPROVAL_PHRASE)
    _assert_blocked(output, expected_reason)
