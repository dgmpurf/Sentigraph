from __future__ import annotations

import builtins
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.controlled_evidence_layer_import_candidate as import_candidate_module
import app.services.controlled_review_queue_candidate as review_queue_module


BATCH_APPROVAL_PHRASE = (
    "APPROVE_8Z_12_13_BATCH_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_AND_IMPORT_CANDIDATE_SMOKE"
)
REVIEW_QUEUE_HELPER_PHRASE = "APPROVE_8W_13_CONTROLLED_REVIEW_QUEUE_CANDIDATE_IMPLEMENTATION"
IMPORT_CANDIDATE_HELPER_PHRASE = "APPROVE_8W_16_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_IMPLEMENTATION"

OLD_REVIEW_QUEUE_CHINESE_PHRASE = "批准 8W-13 Controlled Review Queue Candidate Helper Implementation"
OLD_REVIEW_QUEUE_MOJIBAKE_PHRASE = "鎵瑰噯 8W-13 Controlled Review Queue Candidate Helper Implementation"
OLD_REVIEW_QUEUE_GARBLED_PHRASE = "閹电懓鍣?8W-13 Controlled Review Queue Candidate Helper Implementation"
OLD_IMPORT_CHINESE_PHRASE = "批准 8W-16 Controlled Evidence Layer Import Candidate Helper Implementation"
OLD_IMPORT_MOJIBAKE_PHRASE = "鎵瑰噯 8W-16 Controlled Evidence Layer Import Candidate Helper Implementation"
OLD_IMPORT_GARBLED_PHRASE = "閹电懓鍣?8W-16 Controlled Evidence Layer Import Candidate Helper Implementation"

OLD_8Z11_PHRASE = (
    "APPROVE_8Z_11_CONTROLLED_ON_DEMAND_COLLECTOR_ROUTE_C_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SMOKE"
)
OLD_8Y8_PHRASE = "APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE"
OLD_8Y10_PHRASE = (
    "APPROVE_8Y_10_CONTROLLED_REVIEW_QUEUE_CANDIDATE_TO_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE"
)

PHASE = "8Z-12/13"

FALSE_SOURCE_FLAGS = {
    "evidence_layer_write": "source_evidence_layer_write_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "actual_review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "review_queue_candidate_created": "source_review_queue_candidate_created_before_8z12",
    "evidence_layer_import_candidate_created": "source_import_candidate_created_before_8z13",
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
    "actual_review_queue_runtime_used": "output_review_queue_runtime_used_true",
    "production_review_queue_item_created": "output_production_review_queue_item_created_true",
    "evidence_layer_write": "output_evidence_layer_write_true",
    "evidence_layer_write_candidate_created": "output_evidence_layer_write_candidate_created_true",
    "production_evidence_item_created": "output_production_evidence_item_created_true",
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


def _evidence_candidate(index: int, **overrides: object) -> dict[str, object]:
    candidate: dict[str, object] = {
        "candidate_schema": "sentigraph_controlled_evidence_candidate_v0_1",
        "candidate_id": f"8z12-evidence-candidate-{index:03d}",
        "source_preview_row_id": f"8z12-preview-row-{index:03d}",
        "source_row_index": index,
        "source_preview_schema": "sentigraph_controlled_row_preview_v0_1",
        "evidence_id_hash": f"8z12-hash-{index:03d}",
        "evidence_type": "comment",
        "platform": "synthetic_forum",
        "coarse_created_at": "2026-07-07",
        "trust_label": "synthetic_fixture",
        "verification_status": "not_official_verification",
        "review_status": "review_needed",
        "language": "en",
        "content_visibility": "synthetic_public_sample",
        "access_scope": "synthetic_non_production",
        "text_snippet_redacted": f"8Z-12/13 redacted non-production snippet {index}",
        "redaction_status": "redacted",
        "redaction_warnings": ["selected_sample_only", "synthetic_non_production"],
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "human_review_required": True,
        "boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "not_evidence_item": True,
            "no_evidence_layer_write": True,
            "no_review_queue_runtime": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }
    candidate.update(overrides)
    return candidate


def _safe_evidence_candidate_set(**overrides: object) -> dict[str, object]:
    candidates = [_evidence_candidate(1), _evidence_candidate(2)]
    candidate_set: dict[str, object] = {
        "candidate_set_schema": "sentigraph_controlled_evidence_candidate_set_v0_1",
        "phase": "8W-10",
        "candidate_set_status": "evidence_candidate_set_warn_manual_review_required",
        "input_source_kind": "controlled_route_c_row_preview_smoke",
        "source_preview_schema": "sentigraph_controlled_row_preview_v0_1",
        "source_preview_phase": "8W-7",
        "candidate_mode": "backend_only_local_controlled_evidence_candidate",
        "candidate_count": 2,
        "source_preview_rows_count": 2,
        "warning_count": 1,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "candidate_only": True,
        "review_only": True,
        "preview_only": True,
        "evidence_candidate_implementation_approved": True,
        "evidence_candidate_created": True,
        "evidence_items_created": False,
        "evidence_layer_write": False,
        "production_evidence_item_created": False,
        "actual_review_queue_runtime_used": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_candidate_created": False,
        "evidence_layer_import_candidate_created": False,
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
        "candidates": candidates,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only", "synthetic_non_production"],
        "runtime_side_effects": _runtime_side_effects(),
    }
    candidate_set.update(overrides)
    return candidate_set


def _blocked_output(reason: str, *, review_called: bool = False, import_called: bool = False) -> dict[str, object]:
    return {
        "phase": PHASE,
        "decision": "blocked",
        "privacy_issue_stop": "raw" in reason or "secret" in reason,
        "blockers": [reason],
        "batch_prompt": True,
        "batch_outer_phrase_required": True,
        "review_queue_helper_inner_phrase_required": True,
        "import_candidate_helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_review_queue_candidate_called": review_called,
        "controlled_review_queue_candidate_created": False,
        "controlled_evidence_layer_import_candidate_called": import_called,
        "controlled_evidence_layer_import_candidate_created": False,
        "candidate_only": True,
        "review_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in FALSE_OUTPUT_FLAGS},
    }


def _source_blockers(source: dict[str, object]) -> list[str]:
    blockers: list[str] = []
    expected_values = {
        "candidate_set_schema": (
            "sentigraph_controlled_evidence_candidate_set_v0_1",
            "source_candidate_set_schema_wrong",
        ),
        "phase": ("8W-10", "source_candidate_phase_wrong"),
        "candidate_set_status": (
            "evidence_candidate_set_warn_manual_review_required",
            "source_candidate_set_status_not_warn_manual_review",
        ),
        "candidate_mode": (
            "backend_only_local_controlled_evidence_candidate",
            "source_candidate_mode_wrong",
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
        "evidence_candidate_created": "source_evidence_candidate_created_not_true",
    }
    for field, reason in required_true_fields.items():
        if source.get(field) is not True:
            blockers.append(reason)

    if source.get("candidate_count") != len(source.get("candidates", [])):
        blockers.append("source_candidate_count_inconsistent")

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


def _output_side_effect_blockers(output: dict[str, Any], prefix: str) -> list[str]:
    blockers: list[str] = []
    for field, reason in FALSE_OUTPUT_FLAGS.items():
        if output.get(field) is True:
            blockers.append(f"{prefix}_{reason}")

    runtime_side_effects = output.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"{prefix}_runtime_side_effect_true:{flag}")
    return blockers


def _build_8z12_13_batch_smoke(
    *,
    batch_phrase: str | None,
    source_candidate_set: dict[str, object] | None = None,
    review_queue_helper_phrase: str | None = REVIEW_QUEUE_HELPER_PHRASE,
    import_candidate_helper_phrase: str | None = IMPORT_CANDIDATE_HELPER_PHRASE,
) -> dict[str, object]:
    if batch_phrase is None or batch_phrase == "":
        return _blocked_output("blocked_missing_exact_8z12_13_batch_approval")
    if batch_phrase != BATCH_APPROVAL_PHRASE:
        return _blocked_output("blocked_wrong_exact_8z12_13_batch_approval")

    source = _safe_evidence_candidate_set() if source_candidate_set is None else source_candidate_set
    source_blockers = _source_blockers(source)
    if source_blockers:
        return _blocked_output(source_blockers[0])

    review_queue_candidate_set = review_queue_module.build_controlled_review_queue_candidate_set(
        source,
        exact_approval_phrase=review_queue_helper_phrase,
    )
    review_blockers = _output_side_effect_blockers(review_queue_candidate_set, "review_queue_helper")
    if review_blockers:
        return _blocked_output(review_blockers[0], review_called=True)
    if review_queue_candidate_set.get("review_queue_candidate_created") is not True:
        blockers = review_queue_candidate_set.get("blockers")
        first_blocker = blockers[0] if isinstance(blockers, list) and blockers else "review_queue_candidate_not_created"
        return _blocked_output(f"review_queue_helper_blocked:{first_blocker}", review_called=True)

    import_candidate_set = import_candidate_module.build_controlled_evidence_layer_import_candidate_set(
        review_queue_candidate_set,
        exact_approval_phrase=import_candidate_helper_phrase,
    )
    import_blockers = _output_side_effect_blockers(import_candidate_set, "import_candidate_helper")
    if import_blockers:
        return _blocked_output(import_blockers[0], review_called=True, import_called=True)
    if import_candidate_set.get("evidence_layer_import_candidate_created") is not True:
        blockers = import_candidate_set.get("blockers")
        first_blocker = blockers[0] if isinstance(blockers, list) and blockers else "import_candidate_not_created"
        return _blocked_output(
            f"import_candidate_helper_blocked:{first_blocker}",
            review_called=True,
            import_called=True,
        )

    return {
        "phase": PHASE,
        "decision": "ready",
        "privacy_issue_stop": False,
        "blockers": [],
        "batch_prompt": True,
        "batch_outer_phrase_required": True,
        "review_queue_helper_inner_phrase_required": True,
        "import_candidate_helper_inner_phrase_required": True,
        "helper_inner_phrase_alone_authorizes_batch": False,
        "old_chinese_or_mojibake_helper_phrase_accepted": False,
        "controlled_review_queue_candidate_called": True,
        "controlled_review_queue_candidate_created": True,
        "review_queue_candidate_schema": "sentigraph_controlled_review_queue_candidate_v0_1",
        "review_queue_candidate_mode": review_queue_candidate_set["review_queue_candidate_mode"],
        "review_queue_candidate_count": review_queue_candidate_set["review_queue_candidate_count"],
        "controlled_evidence_layer_import_candidate_called": True,
        "controlled_evidence_layer_import_candidate_created": True,
        "evidence_layer_import_candidate_schema": "sentigraph_controlled_evidence_layer_import_candidate_v0_1",
        "evidence_layer_import_candidate_mode": import_candidate_set["evidence_layer_import_candidate_mode"],
        "evidence_layer_import_candidate_count": import_candidate_set["evidence_layer_import_candidate_count"],
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
    assert output["controlled_review_queue_candidate_created"] is False
    assert output["controlled_evidence_layer_import_candidate_created"] is False
    _assert_no_forbidden_side_effects(output)
    _assert_safe_output(output)


def test_8z12_13_batch_creates_candidate_chain_without_production_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked_file_access(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Z-12/13 smoke must not read files")

    monkeypatch.setattr(builtins, "open", blocked_file_access)
    monkeypatch.setattr(Path, "open", blocked_file_access)
    monkeypatch.setattr(Path, "read_text", blocked_file_access)
    monkeypatch.setattr(Path, "read_bytes", blocked_file_access)

    output = _build_8z12_13_batch_smoke(batch_phrase=BATCH_APPROVAL_PHRASE)

    assert review_queue_module.APPROVAL_PHRASE == REVIEW_QUEUE_HELPER_PHRASE
    assert import_candidate_module.APPROVAL_PHRASE == IMPORT_CANDIDATE_HELPER_PHRASE
    assert output["decision"] == "ready"
    assert output["controlled_review_queue_candidate_created"] is True
    assert output["review_queue_candidate_schema"] == "sentigraph_controlled_review_queue_candidate_v0_1"
    assert output["review_queue_candidate_mode"] == "backend_only_local_review_queue_candidate_boundary"
    assert output["controlled_evidence_layer_import_candidate_created"] is True
    assert output["evidence_layer_import_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_import_candidate_v0_1"
    )
    assert output["evidence_layer_import_candidate_mode"] == (
        "backend_only_local_evidence_layer_import_candidate_boundary"
    )
    assert output["candidate_only"] is True
    assert output["review_only"] is True
    assert output["human_review_required"] is True
    assert output["no_automatic_trust_upgrade"] is True
    assert output["batch_outer_phrase_required"] is True
    assert output["review_queue_helper_inner_phrase_required"] is True
    assert output["import_candidate_helper_inner_phrase_required"] is True
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
        OLD_8Z11_PHRASE,
        OLD_8Y8_PHRASE,
        OLD_8Y10_PHRASE,
        REVIEW_QUEUE_HELPER_PHRASE,
        IMPORT_CANDIDATE_HELPER_PHRASE,
    ],
)
def test_batch_phrase_required_before_any_helper_call(
    batch_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_review_queue(*args: object, **kwargs: object) -> None:
        raise AssertionError("review queue helper must not run without exact 8Z-12/13 batch approval")

    def fail_import_candidate(*args: object, **kwargs: object) -> None:
        raise AssertionError("import candidate helper must not run without exact 8Z-12/13 batch approval")

    monkeypatch.setattr(review_queue_module, "build_controlled_review_queue_candidate_set", fail_review_queue)
    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_candidate)

    output = _build_8z12_13_batch_smoke(batch_phrase=batch_phrase)

    expected_reason = (
        "blocked_missing_exact_8z12_13_batch_approval"
        if batch_phrase in {None, ""}
        else "blocked_wrong_exact_8z12_13_batch_approval"
    )
    _assert_blocked(output, expected_reason)
    assert output["controlled_review_queue_candidate_called"] is False
    assert output["controlled_evidence_layer_import_candidate_called"] is False


@pytest.mark.parametrize(
    "review_queue_phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_REVIEW_QUEUE_CHINESE_PHRASE,
        OLD_REVIEW_QUEUE_MOJIBAKE_PHRASE,
        OLD_REVIEW_QUEUE_GARBLED_PHRASE,
        BATCH_APPROVAL_PHRASE,
    ],
)
def test_review_queue_helper_phrase_required_before_import_candidate_call(
    review_queue_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_import_candidate(*args: object, **kwargs: object) -> None:
        raise AssertionError("import candidate helper must not run when review queue candidate is blocked")

    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_candidate)

    output = _build_8z12_13_batch_smoke(
        batch_phrase=BATCH_APPROVAL_PHRASE,
        review_queue_helper_phrase=review_queue_phrase,
    )

    expected_inner_reason = (
        "blocked_missing_exact_approval" if review_queue_phrase in {None, ""} else "blocked_wrong_exact_approval"
    )
    _assert_blocked(output, f"review_queue_helper_blocked:{expected_inner_reason}")
    assert output["controlled_review_queue_candidate_called"] is True
    assert output["controlled_evidence_layer_import_candidate_called"] is False


@pytest.mark.parametrize(
    "import_candidate_phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_IMPORT_CHINESE_PHRASE,
        OLD_IMPORT_MOJIBAKE_PHRASE,
        OLD_IMPORT_GARBLED_PHRASE,
        BATCH_APPROVAL_PHRASE,
    ],
)
def test_import_candidate_helper_phrase_required_before_import_candidate_creation(
    import_candidate_phrase: str | None,
) -> None:
    output = _build_8z12_13_batch_smoke(
        batch_phrase=BATCH_APPROVAL_PHRASE,
        import_candidate_helper_phrase=import_candidate_phrase,
    )

    expected_inner_reason = (
        "blocked_missing_exact_approval" if import_candidate_phrase in {None, ""} else "blocked_wrong_exact_approval"
    )
    _assert_blocked(output, f"import_candidate_helper_blocked:{expected_inner_reason}")
    assert output["controlled_review_queue_candidate_called"] is True
    assert output["controlled_evidence_layer_import_candidate_called"] is True


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("candidate_set_schema", "wrong", "source_candidate_set_schema_wrong"),
        ("evidence_layer_write", True, "source_evidence_layer_write_true"),
        ("production_evidence_item_created", True, "source_production_evidence_item_created_true"),
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
def test_unsafe_source_candidate_blocks_before_helper_call(
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_review_queue(*args: object, **kwargs: object) -> None:
        raise AssertionError("review queue helper must not run for unsafe source")

    monkeypatch.setattr(review_queue_module, "build_controlled_review_queue_candidate_set", fail_review_queue)

    output = _build_8z12_13_batch_smoke(
        batch_phrase=BATCH_APPROVAL_PHRASE,
        source_candidate_set=_safe_evidence_candidate_set(**{field: value}),
    )

    _assert_blocked(output, expected_reason)
    assert output["controlled_review_queue_candidate_called"] is False
    assert output["controlled_evidence_layer_import_candidate_called"] is False


def test_review_queue_helper_output_with_production_side_effect_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unsafe_review_queue_output(*args: object, **kwargs: object) -> dict[str, object]:
        return {
            "review_queue_candidate_created": True,
            "review_queue_candidate_mode": "backend_only_local_review_queue_candidate_boundary",
            "review_queue_candidate_count": 1,
            "evidence_layer_write": True,
            "runtime_side_effects": _runtime_side_effects(),
            "blockers": [],
        }

    def fail_import_candidate(*args: object, **kwargs: object) -> None:
        raise AssertionError("import helper must not run after unsafe review queue helper output")

    monkeypatch.setattr(review_queue_module, "build_controlled_review_queue_candidate_set", unsafe_review_queue_output)
    monkeypatch.setattr(import_candidate_module, "build_controlled_evidence_layer_import_candidate_set", fail_import_candidate)

    output = _build_8z12_13_batch_smoke(batch_phrase=BATCH_APPROVAL_PHRASE)

    _assert_blocked(output, "review_queue_helper_output_evidence_layer_write_true")
    assert output["controlled_review_queue_candidate_called"] is True
    assert output["controlled_evidence_layer_import_candidate_called"] is False


def test_import_candidate_helper_output_with_production_side_effect_blocks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def unsafe_import_candidate_output(*args: object, **kwargs: object) -> dict[str, object]:
        return {
            "evidence_layer_import_candidate_created": True,
            "evidence_layer_import_candidate_mode": "backend_only_local_evidence_layer_import_candidate_boundary",
            "evidence_layer_import_candidate_count": 1,
            "production_evidence_item_created": True,
            "runtime_side_effects": _runtime_side_effects(),
            "blockers": [],
        }

    monkeypatch.setattr(
        import_candidate_module,
        "build_controlled_evidence_layer_import_candidate_set",
        unsafe_import_candidate_output,
    )

    output = _build_8z12_13_batch_smoke(batch_phrase=BATCH_APPROVAL_PHRASE)

    _assert_blocked(output, "import_candidate_helper_output_production_evidence_item_created_true")
    assert output["controlled_review_queue_candidate_called"] is True
    assert output["controlled_evidence_layer_import_candidate_called"] is True
