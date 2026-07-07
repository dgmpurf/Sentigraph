from __future__ import annotations

import builtins
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_evidence_layer_write_candidate as write_candidate_module
import app.services.controlled_evidence_layer_write_candidate_from_production_import_candidate as write_from_production_import_module
import app.services.controlled_evidenceitem_evidence_layer_write_runtime as evidenceitem_write_module
import app.services.controlled_production_analysis_run_candidate as production_analysis_run_module
import app.services.controlled_production_case_candidate as production_case_module
import app.services.controlled_production_evidence_import_candidate as production_import_module
import app.services.evidence_import as evidence_import_module
import app.services.evidence_ingestion as evidence_ingestion_module


BATCH_APPROVAL_PHRASE = "APPROVE_8Z_14_15_BATCH_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_BOUNDARY_SMOKE"
WRITE_CANDIDATE_HELPER_PHRASE = "APPROVE_8W_19_CONTROLLED_EVIDENCE_LAYER_WRITE_CANDIDATE_IMPLEMENTATION"

OLD_HELPER_CHINESE_PHRASE = "批准 8W-19 Controlled Evidence Layer Write Candidate Helper Implementation"
OLD_HELPER_MOJIBAKE_PHRASE = "鎵瑰噯 8W-19 Controlled Evidence Layer Write Candidate Helper Implementation"
OLD_HELPER_GARBLED_PHRASE = "閹电懓鍣?8W-19 Controlled Evidence Layer Write Candidate Helper Implementation"

OLD_8Z12_13_PHRASE = (
    "APPROVE_8Z_12_13_BATCH_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_AND_IMPORT_CANDIDATE_SMOKE"
)
OLD_8Y12_PHRASE = "APPROVE_8Y_12_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_TO_WRITE_CANDIDATE_SMOKE"
OLD_8W19_HELPER_CHINESE_PHRASE = "批准 8W-19 Controlled Evidence Layer Write Candidate Helper Implementation"

PHASE = "8Z-14/15"

FALSE_SOURCE_FLAGS = {
    "actual_evidence_layer_write_used": "source_actual_evidence_layer_write_used_true",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "persisted_evidence_layer_record_created": "source_persisted_evidence_layer_record_created_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "production_evidenceitem_write_runtime_used": "source_production_evidenceitem_write_runtime_used_true",
    "evidenceitem_write_runtime_called": "source_evidenceitem_write_runtime_called_true",
    "production_import_candidate_created": "source_production_import_candidate_created_true",
    "production_import_derived_write_candidate_created": "source_production_import_derived_write_candidate_created_true",
    "actual_review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": "source_analysis_result_authorized_true",
    "production_analysis_result_created": "source_analysis_result_created_true",
    "downstream_route_c_auto_run": "source_downstream_route_c_auto_run_true",
    "real_exchange_dir_read": "source_real_exchange_dir_read_true",
    "real_package_dir_read": "source_real_package_dir_read_true",
    "production_package_rows_parsed": "source_production_package_rows_parsed_true",
    "original_package_rows_read": "source_original_package_rows_read_true",
    "raw_rows_exposed": "source_raw_rows_exposed_true",
    "raw_comments_exposed": "source_raw_comments_exposed_true",
    "raw_identities_exposed": "source_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "source_author_identity_exposed_true",
    "secrets_read": "source_secrets_read_true",
}

FALSE_OUTPUT_FLAGS = {
    "actual_evidence_layer_write_used": "output_actual_evidence_layer_write_used_true",
    "evidence_layer_write": "output_evidence_layer_write_true",
    "persisted_evidence_layer_record_created": "output_persisted_evidence_layer_record_created_true",
    "production_evidence_item_created": "output_production_evidence_item_created_true",
    "production_evidenceitem_write_runtime_used": "output_production_evidenceitem_write_runtime_used_true",
    "evidenceitem_write_runtime_called": "output_evidenceitem_write_runtime_called_true",
    "production_import_candidate_created": "output_production_import_candidate_created_true",
    "production_import_derived_write_candidate_created": "output_production_import_derived_write_candidate_created_true",
    "production_case_created": "output_production_case_created_true",
    "production_analysis_run_created": "output_production_analysis_run_created_true",
    "actual_analysis_execution_started": "output_actual_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": "output_analysis_result_authorized_true",
    "production_analysis_result_created": "output_analysis_result_created_true",
    "downstream_route_c_auto_run": "output_downstream_route_c_auto_run_true",
    "actual_review_queue_runtime_used": "output_review_queue_runtime_used_true",
    "production_review_queue_item_created": "output_production_review_queue_item_created_true",
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

FORBIDDEN_SENTINELS = (
    "actual-token-should-never-appear",
    "actual-cookie-should-never-appear",
    "actual-api-key-should-never-appear",
    "actual-raw-author-should-never-appear",
    "actual-author-name-should-never-appear",
    "actual-profile-url-should-never-appear",
    "actual-raw-comment-should-never-appear",
    "G:/private-collector/should-never-appear",
    "C:/Users/msjpurf/private-collector/should-never-appear",
)


def _runtime_side_effects(**overrides: bool) -> dict[str, bool]:
    flags = {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_provider_job": False,
        "ran_collector": False,
        "fetched_url": False,
        "scraped_page": False,
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
        "created_evidence_item": False,
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
    flags.update(overrides)
    return flags


def _import_candidate(index: int, **overrides: object) -> dict[str, object]:
    candidate: dict[str, object] = {
        "evidence_layer_import_candidate_schema": "sentigraph_controlled_evidence_layer_import_candidate_v0_1",
        "evidence_layer_import_candidate_id": f"8z14-import-candidate-{index:03d}",
        "source_review_queue_candidate_id": f"8z14-review-queue-candidate-{index:03d}",
        "source_review_queue_candidate_set_schema": "sentigraph_controlled_review_queue_candidate_set_v0_1",
        "source_review_queue_candidate_schema": "sentigraph_controlled_review_queue_candidate_v0_1",
        "source_evidence_candidate_id": f"8z14-evidence-candidate-{index:03d}",
        "evidence_id_hash": f"8z14-hash-{index:03d}",
        "preview_hash": f"8z14-hash-{index:03d}",
        "platform": "synthetic_forum",
        "evidence_type": "comment",
        "coarse_created_at": "2026-07-07",
        "source_url_present": False,
        "trust_boundary_label": "synthetic_fixture",
        "verification_status": "not_official_verification",
        "review_status": "review_needed",
        "title_or_label_redacted": f"8Z-14/15 redacted label {index}",
        "text_snippet_redacted": f"8Z-14/15 redacted non-production snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only", "synthetic_non_production"],
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "import_readiness_blockers": [
            "human_review_required",
            "not_evidence_item",
            "no_evidence_layer_write",
        ],
        "blocker_codes": [],
        "human_review_required": True,
        "preview_only": True,
        "import_candidate_only": True,
        "boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "import_candidate_only": True,
            "not_evidence_item": True,
            "not_production_evidence_item": True,
            "no_evidence_layer_write": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_analysis_ready": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }
    candidate.update(overrides)
    return candidate


def _safe_import_candidate_set(**overrides: object) -> dict[str, object]:
    candidates = [_import_candidate(1), _import_candidate(2)]
    candidate_set: dict[str, object] = {
        "evidence_layer_import_candidate_set_schema": "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
        "phase": "8W-16",
        "evidence_layer_import_candidate_set_status": "evidence_layer_import_candidate_set_warn_manual_review_required",
        "input_source_kind": "controlled_review_queue_candidate_set",
        "source_review_queue_candidate_set_schema": "sentigraph_controlled_review_queue_candidate_set_v0_1",
        "source_review_queue_candidate_set_status": "review_queue_candidate_set_warn_manual_review_required",
        "source_review_queue_candidate_count": 2,
        "evidence_layer_import_candidate_mode": "backend_only_local_evidence_layer_import_candidate_boundary",
        "evidence_layer_import_candidate_count": 2,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "candidate_only": True,
        "review_only": True,
        "preview_only": True,
        "import_candidate_only": True,
        "evidence_layer_import_candidate_helper_implementation_approved": True,
        "evidence_layer_import_candidate_created": True,
        "evidence_item_created": False,
        "evidence_items_created": False,
        "actual_evidence_layer_write_used": False,
        "evidence_layer_write": False,
        "persisted_evidence_layer_record_created": False,
        "evidence_layer_write_candidate_created": False,
        "production_evidence_item_created": False,
        "production_evidenceitem_write_runtime_used": False,
        "evidenceitem_write_runtime_called": False,
        "production_import_candidate_created": False,
        "production_import_derived_write_candidate_created": False,
        "actual_review_queue_runtime_used": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "actual_analysis_execution_started": False,
        "production_analysis_result_creation_authorized": False,
        "production_analysis_result_created": False,
        "downstream_route_c_auto_run": False,
        "real_exchange_dir_read": False,
        "real_package_dir_read": False,
        "production_package_rows_parsed": False,
        "original_package_rows_read": False,
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
        "evidence_layer_import_candidates": candidates,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_non_production"],
        "runtime_side_effects": _runtime_side_effects(),
    }
    candidate_set.update(overrides)
    return candidate_set


def _blocked_output(reason: str, *, write_candidate_called: bool = False) -> dict[str, object]:
    return {
        "phase": PHASE,
        "decision": "blocked",
        "privacy_issue_stop": "raw" in reason or "secret" in reason,
        "blockers": [reason],
        "batch_prompt": True,
        "batch_outer_phrase_required": True,
        "write_candidate_helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_evidence_layer_write_candidate_called": write_candidate_called,
        "controlled_evidence_layer_write_candidate_created": False,
        "write_candidate_created": False,
        "boundary_only": True,
        "candidate_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in FALSE_OUTPUT_FLAGS},
    }


def _source_blockers(source: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    expected_values = {
        "evidence_layer_import_candidate_set_schema": (
            "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
            "source_import_candidate_set_schema_wrong",
        ),
        "phase": ("8W-16", "source_import_candidate_phase_wrong"),
        "evidence_layer_import_candidate_set_status": (
            "evidence_layer_import_candidate_set_warn_manual_review_required",
            "source_import_candidate_set_status_not_warn_manual_review",
        ),
        "evidence_layer_import_candidate_mode": (
            "backend_only_local_evidence_layer_import_candidate_boundary",
            "source_import_candidate_mode_wrong",
        ),
    }
    for field, (expected, reason) in expected_values.items():
        if source.get(field) != expected:
            blockers.append(reason)

    required_true_fields = {
        "candidate_only": "source_candidate_only_not_true",
        "review_only": "source_review_only_not_true",
        "human_review_required": "source_human_review_required_not_true",
        "no_automatic_trust_upgrade": "source_no_automatic_trust_upgrade_not_true",
        "evidence_layer_import_candidate_created": "source_import_candidate_created_not_true",
    }
    for field, reason in required_true_fields.items():
        if source.get(field) is not True:
            blockers.append(reason)

    if source.get("evidence_layer_import_candidate_count") != len(source.get("evidence_layer_import_candidates", [])):
        blockers.append("source_import_candidate_count_inconsistent")

    for field, reason in FALSE_SOURCE_FLAGS.items():
        if source.get(field) is True:
            blockers.append(reason)

    runtime_side_effects = source.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("source_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")

    return blockers


def _output_side_effect_blockers(output: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for field, reason in FALSE_OUTPUT_FLAGS.items():
        if output.get(field) is True:
            blockers.append(f"write_candidate_helper_{reason}")

    runtime_side_effects = output.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"write_candidate_helper_runtime_side_effect_true:{flag}")
    return blockers


def _build_8z14_15_batch_smoke(
    *,
    batch_phrase: str | None,
    source_import_candidate_set: dict[str, object] | None = None,
    write_candidate_helper_phrase: str | None = WRITE_CANDIDATE_HELPER_PHRASE,
) -> dict[str, object]:
    if batch_phrase is None or batch_phrase == "":
        return _blocked_output("blocked_missing_exact_8z14_15_batch_approval")
    if batch_phrase != BATCH_APPROVAL_PHRASE:
        return _blocked_output("blocked_wrong_exact_8z14_15_batch_approval")

    source = _safe_import_candidate_set() if source_import_candidate_set is None else source_import_candidate_set
    source_blockers = _source_blockers(source)
    if source_blockers:
        return _blocked_output(source_blockers[0])

    write_candidate_set = write_candidate_module.build_controlled_evidence_layer_write_candidate_set(
        source,
        exact_approval_phrase=write_candidate_helper_phrase,
    )
    output_blockers = _output_side_effect_blockers(write_candidate_set)
    if output_blockers:
        return _blocked_output(output_blockers[0], write_candidate_called=True)
    if write_candidate_set.get("evidence_layer_write_candidate_created") is not True:
        blockers = write_candidate_set.get("blockers")
        first_blocker = blockers[0] if isinstance(blockers, list) and blockers else "write_candidate_not_created"
        return _blocked_output(f"write_candidate_helper_blocked:{first_blocker}", write_candidate_called=True)

    return {
        "phase": PHASE,
        "decision": "ready",
        "privacy_issue_stop": False,
        "blockers": [],
        "batch_prompt": True,
        "batch_outer_phrase_required": True,
        "write_candidate_helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_evidence_layer_write_candidate_called": True,
        "controlled_evidence_layer_write_candidate_created": True,
        "write_candidate_created": True,
        "evidence_layer_write_candidate_schema": write_candidate_set["evidence_layer_write_candidate_set_schema"],
        "write_candidate_mode": write_candidate_set["evidence_layer_write_candidate_mode"],
        "source_import_candidate_schema": "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
        "boundary_only": True,
        "candidate_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in FALSE_OUTPUT_FLAGS},
    }


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _assert_safe_output(value: object) -> None:
    serialized = _serialized(value)
    for sentinel in FORBIDDEN_SENTINELS:
        assert sentinel not in serialized
    assert ":/" not in serialized
    assert ":\\" not in serialized


def _assert_no_forbidden_side_effects(output: dict[str, object]) -> None:
    for field in FALSE_OUTPUT_FLAGS:
        assert output[field] is False, field


def _assert_blocked(output: dict[str, object], expected_reason: str) -> None:
    assert output["decision"] == "blocked"
    assert output["blockers"] == [expected_reason]
    assert output["controlled_evidence_layer_write_candidate_created"] is False
    assert output["write_candidate_created"] is False
    _assert_no_forbidden_side_effects(output)
    _assert_safe_output(output)


def _patch_forbidden_downstream_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_if_called(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-14/15 must not call downstream runtime, write, or production helpers")

    for module, names in (
        (evidence_import_module, ("import_evidence", "write_evidence_items", "create_evidence_items")),
        (evidence_ingestion_module, ("ingest_evidence", "write_evidence_items", "create_evidence_items")),
        (evidenceitem_write_module, ("build_controlled_evidenceitem_evidence_layer_write_runtime",)),
        (production_import_module, ("build_controlled_production_evidence_import_candidate_set",)),
        (
            write_from_production_import_module,
            ("build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set",),
        ),
        (production_case_module, ("build_controlled_production_case_candidate_set",)),
        (production_analysis_run_module, ("build_controlled_production_analysis_run_candidate_set",)),
    ):
        for name in names:
            if hasattr(module, name):
                monkeypatch.setattr(module, name, fail_if_called)


def test_8z14_15_batch_creates_write_candidate_boundary_without_actual_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-14/15 smoke must not read files")

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)
    _patch_forbidden_downstream_entrypoints(monkeypatch)

    output = _build_8z14_15_batch_smoke(batch_phrase=BATCH_APPROVAL_PHRASE)

    assert write_candidate_module.APPROVAL_PHRASE == WRITE_CANDIDATE_HELPER_PHRASE
    assert output["decision"] == "ready"
    assert output["controlled_evidence_layer_write_candidate_created"] is True
    assert output["write_candidate_created"] is True
    assert output["evidence_layer_write_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1"
    )
    assert output["write_candidate_mode"] == "backend_only_local_evidence_layer_write_candidate_boundary"
    assert output["source_import_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1"
    )
    assert output["boundary_only"] is True
    assert output["candidate_only"] is True
    assert output["review_only"] is True
    assert output["human_review_required"] is True
    assert output["no_automatic_trust_upgrade"] is True
    assert output["batch_outer_phrase_required"] is True
    assert output["write_candidate_helper_inner_phrase_required"] is True
    assert output["helper_inner_phrase_alone_authorizes_batch"] is False
    assert output["old_chinese_or_mojibake_helper_phrase_accepted"] is False
    assert output["downstream_route_c_auto_run"] is False
    _assert_no_forbidden_side_effects(output)
    _assert_safe_output(output)


@pytest.mark.parametrize(
    "batch_phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_8Z12_13_PHRASE,
        OLD_8Y12_PHRASE,
        OLD_8W19_HELPER_CHINESE_PHRASE,
        WRITE_CANDIDATE_HELPER_PHRASE,
    ],
)
def test_batch_phrase_required_before_write_candidate_helper_call(
    batch_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_write_candidate(*args: object, **kwargs: object) -> None:
        raise AssertionError("write-candidate helper must not run without exact 8Z-14/15 batch approval")

    monkeypatch.setattr(write_candidate_module, "build_controlled_evidence_layer_write_candidate_set", fail_write_candidate)

    output = _build_8z14_15_batch_smoke(batch_phrase=batch_phrase)

    expected_reason = (
        "blocked_missing_exact_8z14_15_batch_approval"
        if batch_phrase in {None, ""}
        else "blocked_wrong_exact_8z14_15_batch_approval"
    )
    _assert_blocked(output, expected_reason)
    assert output["controlled_evidence_layer_write_candidate_called"] is False


@pytest.mark.parametrize(
    "helper_phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_HELPER_CHINESE_PHRASE,
        OLD_HELPER_MOJIBAKE_PHRASE,
        OLD_HELPER_GARBLED_PHRASE,
        BATCH_APPROVAL_PHRASE,
    ],
)
def test_write_candidate_helper_phrase_required_before_write_candidate_creation(
    helper_phrase: str | None,
) -> None:
    output = _build_8z14_15_batch_smoke(
        batch_phrase=BATCH_APPROVAL_PHRASE,
        write_candidate_helper_phrase=helper_phrase,
    )

    expected_inner_reason = (
        "blocked_missing_exact_approval" if helper_phrase in {None, ""} else "blocked_wrong_exact_approval"
    )
    _assert_blocked(output, f"write_candidate_helper_blocked:{expected_inner_reason}")
    assert output["controlled_evidence_layer_write_candidate_called"] is True


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("evidence_layer_import_candidate_set_schema", "wrong", "source_import_candidate_set_schema_wrong"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("persisted_evidence_layer_record_created", True, "source_persisted_evidence_layer_record_created_true"),
        ("production_evidence_item_created", True, "source_production_evidence_item_created_true"),
        ("production_evidenceitem_write_runtime_used", True, "source_production_evidenceitem_write_runtime_used_true"),
        ("evidenceitem_write_runtime_called", True, "source_evidenceitem_write_runtime_called_true"),
        ("production_import_candidate_created", True, "source_production_import_candidate_created_true"),
        (
            "production_import_derived_write_candidate_created",
            True,
            "source_production_import_derived_write_candidate_created_true",
        ),
        ("actual_review_queue_runtime_used", True, "source_review_queue_runtime_used_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("actual_analysis_execution_started", True, "source_actual_analysis_execution_started_true"),
        ("production_analysis_result_creation_authorized", True, "source_analysis_result_authorized_true"),
        ("production_analysis_result_created", True, "source_analysis_result_created_true"),
        ("human_review_required", False, "source_human_review_required_not_true"),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
    ],
)
def test_unsafe_source_import_candidate_blocks_before_write_candidate_helper_call(
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_write_candidate(*args: object, **kwargs: object) -> None:
        raise AssertionError("write-candidate helper must not run for unsafe import candidate source")

    monkeypatch.setattr(write_candidate_module, "build_controlled_evidence_layer_write_candidate_set", fail_write_candidate)

    output = _build_8z14_15_batch_smoke(
        batch_phrase=BATCH_APPROVAL_PHRASE,
        source_import_candidate_set=_safe_import_candidate_set(**{field: value}),
    )

    _assert_blocked(output, expected_reason)
    assert output["controlled_evidence_layer_write_candidate_called"] is False


@pytest.mark.parametrize(
    ("field", "expected_reason"),
    [
        ("evidence_layer_write", "write_candidate_helper_output_evidence_layer_write_true"),
        ("actual_evidence_layer_write_used", "write_candidate_helper_output_actual_evidence_layer_write_used_true"),
        (
            "persisted_evidence_layer_record_created",
            "write_candidate_helper_output_persisted_evidence_layer_record_created_true",
        ),
        ("production_evidence_item_created", "write_candidate_helper_output_production_evidence_item_created_true"),
        (
            "production_evidenceitem_write_runtime_used",
            "write_candidate_helper_output_production_evidenceitem_write_runtime_used_true",
        ),
        ("evidenceitem_write_runtime_called", "write_candidate_helper_output_evidenceitem_write_runtime_called_true"),
        ("production_import_candidate_created", "write_candidate_helper_output_production_import_candidate_created_true"),
        (
            "production_import_derived_write_candidate_created",
            "write_candidate_helper_output_production_import_derived_write_candidate_created_true",
        ),
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
            "evidence_layer_write_candidate_set_schema": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
            "evidence_layer_write_candidate_mode": "backend_only_local_evidence_layer_write_candidate_boundary",
            field: True,
            "runtime_side_effects": _runtime_side_effects(),
            "blockers": [],
        }

    monkeypatch.setattr(
        write_candidate_module,
        "build_controlled_evidence_layer_write_candidate_set",
        unsafe_write_candidate_output,
    )

    output = _build_8z14_15_batch_smoke(batch_phrase=BATCH_APPROVAL_PHRASE)

    _assert_blocked(output, expected_reason)
    assert output["controlled_evidence_layer_write_candidate_called"] is True
