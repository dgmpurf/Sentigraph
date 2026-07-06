from __future__ import annotations

import builtins
import copy
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.analysis_request_store as analysis_request_store
import app.services.controlled_actual_analysis_execution_candidate as actual_execution_module
import app.services.controlled_analysis_result_candidate as analysis_result_module
import app.services.controlled_production_analysis_result_boundary as production_result_boundary_module
import app.services.controlled_production_analysis_result_candidate as production_result_candidate_module
import app.services.controlled_production_analysis_result_creation_boundary as result_creation_boundary_module
import app.services.controlled_production_analysis_result_creation_candidate as result_creation_candidate_module
import app.services.controlled_production_analysis_result_creation_execution_boundary as result_creation_execution_module
import app.services.controlled_production_analysis_result_creation_final_authorization_boundary as final_authorization_module
import app.services.controlled_production_analysis_result_creation_go_no_go_boundary as go_no_go_module
import app.services.controlled_production_analysis_result_creation_or_runtime_execution_candidate as creation_or_runtime_module
import app.services.controlled_production_analysis_result_creation_runtime_boundary as creation_runtime_module
import app.services.controlled_production_analysis_result_runtime_boundary as result_runtime_boundary_module
import app.services.evidence_import as evidence_import_module
import app.services.evidence_ingestion as evidence_ingestion_module
from app.tests.test_8y_13c_controlled_production_import_derived_reroute_smoke import (
    EIGHT_Y10_APPROVAL_PHRASE,
    EIGHT_Y12_APPROVAL_PHRASE,
    EIGHT_Y13C_APPROVAL_PHRASE,
    EIGHT_Y6_APPROVAL_PHRASE,
    EIGHT_Y8_APPROVAL_PHRASE,
    _assert_no_forbidden_output,
)
from app.tests.test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair import (
    EIGHT_Y14_APPROVAL_PHRASE,
    REPAIRED_HELPER_PHRASE,
)
from app.tests.test_8y_16_controlled_evidenceitem_write_result_to_production_case_candidate_smoke import (
    EIGHT_Y16_APPROVAL_PHRASE,
)
from app.tests.test_8y_18_controlled_production_case_candidate_to_analysis_run_candidate_smoke import (
    EIGHT_Y18_APPROVAL_PHRASE,
    ROW_PREVIEW_APPROVAL_PHRASE,
    _build_8y18_smoke,
)


EIGHT_Y20_APPROVAL_PHRASE = (
    "APPROVE_8Y_20_CONTROLLED_ANALYSIS_RUN_CANDIDATE_TO_ANALYSIS_RESULT_BOUNDARY_SMOKE"
)
EIGHT_W70_PLACEHOLDER_PHRASE = (
    "APPROVE_8W_70_PRODUCTION_ANALYSIS_RESULT_CREATION_CHAIN_REACTIVATION_DECISION_DOCS_ONLY"
)
EXISTING_ACTUAL_EXECUTION_HELPER_PHRASE = (
    "APPROVE_8W_37_CONTROLLED_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_HELPER_IMPLEMENTATION"
)
EXISTING_ANALYSIS_RESULT_HELPER_PHRASE = (
    "APPROVE_8W_40_CONTROLLED_ANALYSIS_RESULT_CANDIDATE_HELPER_IMPLEMENTATION"
)
MOJIBAKE_ACTUAL_EXECUTION_HELPER_PHRASE = (
    "\u9395\u7470\u567f 8W-37 Controlled Actual Analysis Execution Candidate Helper Implementation"
)
MOJIBAKE_ANALYSIS_RESULT_HELPER_PHRASE = (
    "\u9395\u7470\u567f 8W-40 Controlled Analysis Result Candidate Helper Implementation"
)

EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_production_analysis_run_candidate_v0_1"
)
EXPECTED_ACTUAL_EXECUTION_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_actual_analysis_execution_candidate_v0_1"
)
EXPECTED_ANALYSIS_RESULT_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_analysis_result_candidate_v0_1"
)

FALSE_SIDE_EFFECT_FIELDS = (
    "actual_analysis_execution_started",
    "analysis_execution_started",
    "production_analysis_result_creation_authorized",
    "production_analysis_result_created",
    "production_analysis_result_creation_go_no_go_authorization_performed",
    "production_analysis_result_creation_final_authorization_performed",
    "actual_production_analysis_run_created",
    "production_analysis_run_runtime_used",
    "production_analysis_run_store_record_created",
    "actual_production_case_created",
    "production_case_runtime_used",
    "production_case_store_record_created",
    "new_evidence_layer_write_performed",
    "evidence_import_service_called",
    "evidence_ingestion_service_called",
    "actual_review_queue_runtime_used",
    "production_review_queue_item_created",
    "source11_runtime_called",
    "actual_final_summary_report_created",
    "b_end_report_runtime_generated",
    "sandbox_public_event_runtime_generated",
    "export_download_public_delivery_created",
    "generated_response_text",
    "route_ready",
    "frontend_ready",
    "production_ready",
    "customer_ready",
    "public_ready",
    "raw_rows_exposed",
    "raw_comments_exposed",
    "raw_identities_exposed",
    "raw_author_ids_emitted",
    "raw_author_names_emitted",
    "profile_urls_emitted",
    "author_names_or_profile_urls_exposed",
    "secrets_read",
)

SOURCE_TRUE_BLOCKERS = {
    "actual_production_analysis_run_created": "source_actual_production_analysis_run_created_true",
    "production_analysis_run_runtime_used": "source_production_analysis_run_runtime_used_true",
    "production_analysis_run_store_record_created": (
        "source_production_analysis_run_store_record_created_true"
    ),
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "analysis_execution_started": "source_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": (
        "source_production_analysis_result_creation_authorized_true"
    ),
    "production_analysis_result_created": "source_production_analysis_result_created_true",
    "production_analysis_result_creation_go_no_go_authorization_performed": (
        "source_production_analysis_result_creation_go_no_go_authorization_performed_true"
    ),
    "production_analysis_result_creation_final_authorization_performed": (
        "source_production_analysis_result_creation_final_authorization_performed_true"
    ),
    "actual_production_case_created": "source_actual_production_case_created_true",
    "production_case_runtime_used": "source_production_case_runtime_used_true",
    "evidence_import_service_called": "source_evidence_import_service_called_true",
    "evidence_ingestion_service_called": "source_evidence_ingestion_service_called_true",
    "actual_review_queue_runtime_used": "source_actual_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "source11_runtime_called": "source_source11_runtime_called_true",
    "actual_final_summary_report_created": "source_actual_final_summary_report_created_true",
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_runtime_generated": "source_sandbox_public_event_runtime_generated_true",
    "export_download_public_delivery_created": "source_export_download_public_delivery_created_true",
    "raw_rows_exposed": "source_raw_rows_exposed_true",
    "raw_comments_exposed": "source_raw_comments_exposed_true",
    "raw_identities_exposed": "source_raw_identities_exposed_true",
    "author_names_or_profile_urls_exposed": "source_author_names_or_profile_urls_exposed_true",
}

ACTUAL_EXECUTION_HELPER_REQUIRED_FALSE_DEFAULTS = (
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "analysis_execution_started",
    "analysis_result_created",
    "production_case_created",
    "production_evidence_item_created",
    "review_queue_item_created",
    "production_review_queue_item_created",
    "review_queue_runtime_used",
    "analysis_ready",
    "report_ready",
    "b_end_ready",
    "sandbox_ready",
    "public_event_ready",
    "route_ready",
    "frontend_ready",
    "production_ready",
    "public_ready",
    "customer_ready",
    "additional_row_parsing_performed",
    "evidence_items_jsonl_parsed_again",
    "evidence_items_csv_parsed",
    "source_manifest_rows_parsed",
    "collection_log_rows_parsed",
    "original_package_rows_read",
    "raw_comments_read",
    "raw_identities_read",
    "private_collector_inspected",
    "private_collector_source_inspected",
    "real_exchange_dir_read",
    "b_end_report_runtime_generated",
    "sandbox_public_event_generated",
    "generated_response_text",
    "public_route_created",
    "frontend_integration_approved",
    "download_package_runtime_used",
    "public_access_runtime_used",
    "external_delivery_runtime_used",
    "final_delivery_runtime_used",
)

ANALYSIS_RESULT_HELPER_REQUIRED_FALSE_DEFAULTS = (
    "production_analysis_result_created",
    "additional_row_parsing_performed",
    "evidence_items_jsonl_parsed_again",
    "evidence_items_csv_parsed",
    "source_manifest_rows_parsed",
    "collection_log_rows_parsed",
    "original_package_rows_read",
    "raw_comments_read",
    "raw_identities_read",
    "private_collector_inspected",
    "private_collector_source_inspected",
    "real_exchange_dir_read",
    "b_end_report_runtime_generated",
    "sandbox_public_event_generated",
    "generated_response_text",
    "public_route_created",
    "frontend_integration_approved",
    "download_package_runtime_used",
    "public_access_runtime_used",
    "external_delivery_runtime_used",
    "final_delivery_runtime_used",
)


def _fail_if_called(*args: object, **kwargs: object) -> None:
    raise AssertionError("8Y-20 must not call production runtime, route, frontend, or delivery helpers")


def _patch_optional(monkeypatch: pytest.MonkeyPatch, module: object, name: str) -> None:
    if hasattr(module, name):
        monkeypatch.setattr(module, name, _fail_if_called)


def _patch_file_open_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Y-20 controlled smoke must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)


def _patch_forbidden_runtime_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "build_imported_evidence_items",
        "build_import_commit_result",
        "build_evidence_import_commit_result",
        "preview_evidence_import",
    ):
        _patch_optional(monkeypatch, evidence_import_module, name)
    for name in (
        "build_evidence_items_from_raw_data",
        "raw_post_to_evidence_item",
        "raw_comment_to_evidence_item",
        "normalize_manual_evidence_batch",
        "build_evidence_ingestion_result",
        "enrich_and_deduplicate_evidence_items",
        "merge_evidence_items",
        "build_review_summary",
        "apply_review_decision",
    ):
        _patch_optional(monkeypatch, evidence_ingestion_module, name)
    for name in (
        "create_review_queue_initialization",
        "create_review_queue_item_action",
        "create_review_queue_completion_gate",
        "create_manual_analysis_execution",
        "create_manual_analysis_result_candidate",
        "create_analysis_result_boundary_gate",
        "create_summary_report_candidate",
        "create_final_summary_report",
        "create_final_summary_report_export_artifact",
        "create_report_export_download_package_artifact",
        "create_report_export_public_access_external_delivery_gate",
    ):
        _patch_optional(monkeypatch, analysis_request_store, name)
    for module in (
        production_result_candidate_module,
        production_result_boundary_module,
        result_runtime_boundary_module,
        creation_or_runtime_module,
        result_creation_boundary_module,
        result_creation_candidate_module,
        creation_runtime_module,
        result_creation_execution_module,
        final_authorization_module,
        go_no_go_module,
    ):
        for name in dir(module):
            if name.startswith(("build_", "create_")):
                _patch_optional(monkeypatch, module, name)


def _safe_8y18_analysis_run_candidate_smoke() -> dict[str, Any]:
    smoke = _build_8y18_smoke(outer_approval_phrase=EIGHT_Y18_APPROVAL_PHRASE)
    assert smoke["smoke_status"] == "ready"
    assert smoke["production_analysis_run_candidate_created"] is True
    assert smoke["production_analysis_run_candidate_schema"] == EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA
    assert isinstance(smoke["helper_candidate_set"], dict)
    return copy.deepcopy(smoke)


def _blocked_8y20_output(
    reason: str,
    source_smoke: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "schema": "sentigraph_8y20_controlled_analysis_run_candidate_to_analysis_result_boundary_smoke_v0_1",
        "phase": "8Y-20",
        "smoke_status": "blocked",
        "source_path_step": "production_analysis_run_candidate_to_analysis_result_boundary",
        "outer_8y20_phrase": None,
        "analysis_result_boundary_candidate_created": False,
        "analysis_execution_boundary_candidate_created": False,
        "analysis_result_boundary_schema": None,
        "analysis_result_boundary_mode": None,
        "source_production_analysis_run_candidate_schema": (
            source_smoke.get("production_analysis_run_candidate_schema")
            if isinstance(source_smoke, dict)
            else None
        ),
        "candidate_only": True,
        "backend_only": True,
        "local_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "warning_count": 0,
        "8w69_pause_preserved": True,
        "8w70_reactivation_selected": False,
        "blockers": [reason],
        "warnings": [],
        "actual_execution_helper_candidate_set": None,
        "analysis_result_helper_candidate_set": None,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _source_blockers(source_smoke: dict[str, Any] | None) -> list[str]:
    if not isinstance(source_smoke, dict):
        return ["source_production_analysis_run_candidate_smoke_missing_or_not_object"]

    blockers: list[str] = []
    if source_smoke.get("smoke_status") != "ready":
        blockers.append("source_production_analysis_run_candidate_smoke_not_ready")
    if source_smoke.get("production_analysis_run_candidate_created") is not True:
        blockers.append("source_production_analysis_run_candidate_created_not_true")
    if source_smoke.get("production_analysis_run_candidate_schema") != EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA:
        blockers.append("source_production_analysis_run_candidate_schema_wrong")
    if source_smoke.get("human_review_required") is not True:
        blockers.append("source_human_review_required_not_true")
    if source_smoke.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")
    for field, reason in SOURCE_TRUE_BLOCKERS.items():
        if source_smoke.get(field) is True:
            blockers.append(reason)

    helper_candidate_set = source_smoke.get("helper_candidate_set")
    if not isinstance(helper_candidate_set, dict):
        blockers.append("source_helper_production_analysis_run_candidate_set_missing_or_not_object")
    return blockers


def _actual_execution_source_candidate_set(source_smoke: dict[str, Any]) -> dict[str, Any]:
    source_candidate_set = copy.deepcopy(source_smoke["helper_candidate_set"])
    for field in ACTUAL_EXECUTION_HELPER_REQUIRED_FALSE_DEFAULTS:
        source_candidate_set.setdefault(field, False)
    return source_candidate_set


def _analysis_result_source_candidate_set(
    actual_execution_candidate_set: dict[str, Any],
) -> dict[str, Any]:
    source_candidate_set = copy.deepcopy(actual_execution_candidate_set)
    for field in ANALYSIS_RESULT_HELPER_REQUIRED_FALSE_DEFAULTS:
        source_candidate_set.setdefault(field, False)
    candidates = source_candidate_set.get("actual_analysis_execution_candidates")
    if isinstance(candidates, list):
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            for field in ANALYSIS_RESULT_HELPER_REQUIRED_FALSE_DEFAULTS:
                candidate.setdefault(field, False)
    return source_candidate_set


def _build_8y20_smoke(
    *,
    outer_approval_phrase: str | None,
    source_analysis_run_candidate_smoke: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if outer_approval_phrase is None or outer_approval_phrase == "":
        return _blocked_8y20_output("blocked_missing_exact_8y20_approval")
    if outer_approval_phrase != EIGHT_Y20_APPROVAL_PHRASE:
        return _blocked_8y20_output("blocked_wrong_exact_8y20_approval")

    source_smoke = source_analysis_run_candidate_smoke or _safe_8y18_analysis_run_candidate_smoke()
    source_blockers = _source_blockers(source_smoke)
    if source_blockers:
        return _blocked_8y20_output(source_blockers[0], source_smoke)

    actual_execution_candidate_set = actual_execution_module.build_controlled_actual_analysis_execution_candidate_set(
        _actual_execution_source_candidate_set(source_smoke),
        exact_approval_phrase=actual_execution_module.APPROVAL_PHRASE,
    )
    analysis_result_candidate_set = analysis_result_module.build_controlled_analysis_result_candidate_set(
        _analysis_result_source_candidate_set(actual_execution_candidate_set),
        exact_approval_phrase=analysis_result_module.APPROVAL_PHRASE,
    )
    actual_candidates = actual_execution_candidate_set["actual_analysis_execution_candidates"]
    result_candidates = analysis_result_candidate_set["analysis_result_candidates"]
    actual_candidate = actual_candidates[0] if actual_candidates else {}
    result_candidate = result_candidates[0] if result_candidates else {}
    actual_created = actual_execution_candidate_set["actual_analysis_execution_candidate_created"] is True
    result_created = analysis_result_candidate_set["analysis_result_candidate_created"] is True
    status = "ready" if actual_created and result_created else "blocked"

    blockers = [
        *actual_execution_candidate_set["blockers"],
        *analysis_result_candidate_set["blockers"],
    ]
    return {
        "schema": "sentigraph_8y20_controlled_analysis_run_candidate_to_analysis_result_boundary_smoke_v0_1",
        "phase": "8Y-20",
        "smoke_status": status,
        "source_path_step": "production_analysis_run_candidate_to_analysis_result_boundary",
        "outer_8y20_phrase": EIGHT_Y20_APPROVAL_PHRASE,
        "analysis_result_boundary_candidate_created": result_created,
        "analysis_execution_boundary_candidate_created": actual_created,
        "analysis_result_boundary_schema": result_candidate.get("analysis_result_candidate_schema"),
        "analysis_result_boundary_mode": analysis_result_candidate_set["analysis_result_candidate_mode"],
        "source_production_analysis_run_candidate_schema": source_smoke[
            "production_analysis_run_candidate_schema"
        ],
        "source_actual_analysis_execution_candidate_schema": actual_candidate.get(
            "actual_analysis_execution_candidate_schema"
        ),
        "candidate_only": analysis_result_candidate_set["analysis_result_candidate_only"],
        "backend_only": analysis_result_candidate_set["boundary_flags"]["backend_only"],
        "local_only": analysis_result_candidate_set["boundary_flags"]["local_only"],
        "human_review_required": analysis_result_candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": analysis_result_candidate_set["no_automatic_trust_upgrade"],
        "warning_count": analysis_result_candidate_set["warning_count"],
        "8w69_pause_preserved": True,
        "8w70_reactivation_selected": False,
        "blockers": blockers,
        "warnings": list(analysis_result_candidate_set["warnings"]),
        "actual_execution_helper_candidate_set": actual_execution_candidate_set,
        "analysis_result_helper_candidate_set": analysis_result_candidate_set,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _assert_false_side_effects(smoke: dict[str, Any]) -> None:
    for field in FALSE_SIDE_EFFECT_FIELDS:
        assert smoke[field] is False, field
    assert smoke["8w69_pause_preserved"] is True
    assert smoke["8w70_reactivation_selected"] is False

    for helper_key in ("actual_execution_helper_candidate_set", "analysis_result_helper_candidate_set"):
        candidate_set = smoke.get(helper_key)
        if not isinstance(candidate_set, dict):
            continue
        for flag, value in candidate_set["runtime_side_effects"].items():
            assert value is False, flag
        assert candidate_set["actual_analysis_execution_started"] is False
        assert candidate_set["analysis_execution_started"] is False
        assert candidate_set["analysis_result_created"] is False
        assert candidate_set["production_analysis_run_created"] is False
        assert candidate_set["production_case_created"] is False
        assert candidate_set["production_evidence_item_created"] is False
        assert candidate_set["review_queue_runtime_used"] is False
        assert candidate_set["route_ready"] is False
        assert candidate_set["frontend_ready"] is False
        assert candidate_set["production_ready"] is False
        assert candidate_set["public_ready"] is False
        assert candidate_set["customer_ready"] is False
    _assert_no_forbidden_output(smoke)


def _assert_blocked_before_boundary_candidate_helper(
    smoke: dict[str, Any],
    expected_reason: str,
) -> None:
    assert smoke["smoke_status"] == "blocked"
    assert smoke["analysis_result_boundary_candidate_created"] is False
    assert smoke["analysis_execution_boundary_candidate_created"] is False
    assert smoke["analysis_result_boundary_schema"] is None
    assert smoke["analysis_result_boundary_mode"] is None
    assert smoke["actual_execution_helper_candidate_set"] is None
    assert smoke["analysis_result_helper_candidate_set"] is None
    assert smoke["blockers"] == [expected_reason]
    _assert_false_side_effects(smoke)


def test_8y20_ready_path_builds_local_analysis_result_boundary_candidate_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert actual_execution_module.APPROVAL_PHRASE == EXISTING_ACTUAL_EXECUTION_HELPER_PHRASE
    assert actual_execution_module.APPROVAL_PHRASE.isascii()
    assert analysis_result_module.APPROVAL_PHRASE == EXISTING_ANALYSIS_RESULT_HELPER_PHRASE
    assert analysis_result_module.APPROVAL_PHRASE.isascii()
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y20_smoke(outer_approval_phrase=EIGHT_Y20_APPROVAL_PHRASE)

    assert smoke["smoke_status"] == "ready"
    assert smoke["analysis_result_boundary_candidate_created"] is True
    assert smoke["analysis_execution_boundary_candidate_created"] is True
    assert smoke["analysis_result_boundary_schema"] == EXPECTED_ANALYSIS_RESULT_CANDIDATE_SCHEMA
    assert smoke["analysis_result_boundary_mode"] == "backend_only_local_analysis_result_candidate_boundary"
    assert smoke["source_production_analysis_run_candidate_schema"] == EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA
    assert smoke["source_actual_analysis_execution_candidate_schema"] == EXPECTED_ACTUAL_EXECUTION_CANDIDATE_SCHEMA
    assert smoke["candidate_only"] is True
    assert smoke["backend_only"] is True
    assert smoke["local_only"] is True
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    assert smoke["warning_count"] == 1

    actual_candidate_set = smoke["actual_execution_helper_candidate_set"]
    assert actual_candidate_set["actual_analysis_execution_candidate_set_schema"] == (
        "sentigraph_controlled_actual_analysis_execution_candidate_set_v0_1"
    )
    assert actual_candidate_set["actual_analysis_execution_candidate_created"] is True
    assert actual_candidate_set["actual_analysis_execution_started"] is False
    assert actual_candidate_set["analysis_result_created"] is False
    assert actual_candidate_set["audit_summary"]["actual_analysis_execution_effect"] == "none"

    result_candidate_set = smoke["analysis_result_helper_candidate_set"]
    assert result_candidate_set["analysis_result_candidate_set_schema"] == (
        "sentigraph_controlled_analysis_result_candidate_set_v0_1"
    )
    assert result_candidate_set["analysis_result_candidate_created"] is True
    assert result_candidate_set["analysis_result_generation_executed"] is False
    assert result_candidate_set["analysis_result_created"] is False
    assert result_candidate_set["production_analysis_result_created"] is False
    assert result_candidate_set["audit_summary"]["analysis_result_effect"] == "none"
    assert result_candidate_set["audit_summary"]["production_side_effect"] == "none"
    _assert_false_side_effects(smoke)


@pytest.mark.parametrize(
    "outer_phrase",
    [
        None,
        "",
        "wrong approval",
        EIGHT_Y18_APPROVAL_PHRASE,
        EIGHT_Y16_APPROVAL_PHRASE,
        EIGHT_Y14_APPROVAL_PHRASE,
        REPAIRED_HELPER_PHRASE,
        EIGHT_Y13C_APPROVAL_PHRASE,
        EIGHT_Y12_APPROVAL_PHRASE,
        EIGHT_Y10_APPROVAL_PHRASE,
        EIGHT_Y8_APPROVAL_PHRASE,
        EIGHT_Y6_APPROVAL_PHRASE,
        ROW_PREVIEW_APPROVAL_PHRASE,
        EIGHT_W70_PLACEHOLDER_PHRASE,
    ],
)
def test_exact_8y20_phrase_required_before_boundary_candidate_helpers(
    outer_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        actual_execution_module,
        "build_controlled_actual_analysis_execution_candidate_set",
        _fail_if_called,
    )
    monkeypatch.setattr(
        analysis_result_module,
        "build_controlled_analysis_result_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y20_smoke(outer_approval_phrase=outer_phrase)

    expected = (
        "blocked_missing_exact_8y20_approval"
        if outer_phrase in {None, ""}
        else "blocked_wrong_exact_8y20_approval"
    )
    _assert_blocked_before_boundary_candidate_helper(smoke, expected)


def test_existing_boundary_helpers_reject_mojibake_phrases() -> None:
    source_smoke = _safe_8y18_analysis_run_candidate_smoke()
    actual_candidate_set = actual_execution_module.build_controlled_actual_analysis_execution_candidate_set(
        _actual_execution_source_candidate_set(source_smoke),
        exact_approval_phrase=MOJIBAKE_ACTUAL_EXECUTION_HELPER_PHRASE,
    )
    assert actual_candidate_set["actual_analysis_execution_candidate_created"] is False
    assert "blocked_non_ascii_approval" in actual_candidate_set["blockers"]
    assert actual_candidate_set["actual_analysis_execution_started"] is False
    assert actual_candidate_set["analysis_result_created"] is False
    _assert_no_forbidden_output(actual_candidate_set)

    safe_actual_candidate_set = actual_execution_module.build_controlled_actual_analysis_execution_candidate_set(
        _actual_execution_source_candidate_set(source_smoke),
        exact_approval_phrase=actual_execution_module.APPROVAL_PHRASE,
    )
    analysis_candidate_set = analysis_result_module.build_controlled_analysis_result_candidate_set(
        _analysis_result_source_candidate_set(safe_actual_candidate_set),
        exact_approval_phrase=MOJIBAKE_ANALYSIS_RESULT_HELPER_PHRASE,
    )
    assert analysis_candidate_set["analysis_result_candidate_created"] is False
    assert "blocked_non_ascii_approval" in analysis_candidate_set["blockers"]
    assert analysis_candidate_set["analysis_result_generation_executed"] is False
    assert analysis_candidate_set["analysis_result_created"] is False
    assert analysis_candidate_set["production_analysis_result_created"] is False
    _assert_no_forbidden_output(analysis_candidate_set)


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("production_analysis_run_candidate_schema", "wrong", "source_production_analysis_run_candidate_schema_wrong"),
        ("actual_production_analysis_run_created", True, "source_actual_production_analysis_run_created_true"),
        ("production_analysis_run_runtime_used", True, "source_production_analysis_run_runtime_used_true"),
        (
            "production_analysis_run_store_record_created",
            True,
            "source_production_analysis_run_store_record_created_true",
        ),
        ("actual_analysis_execution_started", True, "source_actual_analysis_execution_started_true"),
        ("analysis_execution_started", True, "source_analysis_execution_started_true"),
        (
            "production_analysis_result_creation_authorized",
            True,
            "source_production_analysis_result_creation_authorized_true",
        ),
        ("production_analysis_result_created", True, "source_production_analysis_result_created_true"),
        (
            "production_analysis_result_creation_go_no_go_authorization_performed",
            True,
            "source_production_analysis_result_creation_go_no_go_authorization_performed_true",
        ),
        (
            "production_analysis_result_creation_final_authorization_performed",
            True,
            "source_production_analysis_result_creation_final_authorization_performed_true",
        ),
        ("actual_production_case_created", True, "source_actual_production_case_created_true"),
        ("production_case_runtime_used", True, "source_production_case_runtime_used_true"),
        ("evidence_import_service_called", True, "source_evidence_import_service_called_true"),
        ("evidence_ingestion_service_called", True, "source_evidence_ingestion_service_called_true"),
        ("actual_review_queue_runtime_used", True, "source_actual_review_queue_runtime_used_true"),
        ("production_review_queue_item_created", True, "source_production_review_queue_item_created_true"),
        ("source11_runtime_called", True, "source_source11_runtime_called_true"),
        ("actual_final_summary_report_created", True, "source_actual_final_summary_report_created_true"),
        ("b_end_report_runtime_generated", True, "source_b_end_report_runtime_generated_true"),
        ("sandbox_public_event_runtime_generated", True, "source_sandbox_public_event_runtime_generated_true"),
        ("export_download_public_delivery_created", True, "source_export_download_public_delivery_created_true"),
        ("raw_rows_exposed", True, "source_raw_rows_exposed_true"),
        ("raw_comments_exposed", True, "source_raw_comments_exposed_true"),
        ("raw_identities_exposed", True, "source_raw_identities_exposed_true"),
        (
            "author_names_or_profile_urls_exposed",
            True,
            "source_author_names_or_profile_urls_exposed_true",
        ),
        ("no_automatic_trust_upgrade", False, "source_no_automatic_trust_upgrade_not_true"),
    ],
)
def test_unsafe_source_blocks_before_boundary_candidate_helpers(
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_smoke = _safe_8y18_analysis_run_candidate_smoke()
    source_smoke[field] = value
    monkeypatch.setattr(
        actual_execution_module,
        "build_controlled_actual_analysis_execution_candidate_set",
        _fail_if_called,
    )
    monkeypatch.setattr(
        analysis_result_module,
        "build_controlled_analysis_result_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y20_smoke(
        outer_approval_phrase=EIGHT_Y20_APPROVAL_PHRASE,
        source_analysis_run_candidate_smoke=source_smoke,
    )

    _assert_blocked_before_boundary_candidate_helper(smoke, expected_reason)


def test_8y20_smoke_output_is_json_serializable_without_raw_or_absolute_values() -> None:
    smoke = _build_8y20_smoke(outer_approval_phrase=EIGHT_Y20_APPROVAL_PHRASE)

    json.dumps(smoke, ensure_ascii=False, sort_keys=True, default=str)
    _assert_false_side_effects(smoke)
