from __future__ import annotations

import builtins
import copy
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.analysis_request_store as analysis_request_store
import app.services.controlled_production_analysis_run_candidate as production_analysis_run_module
import app.services.controlled_production_case_candidate as production_case_module
import app.services.evidence_import as evidence_import_module
import app.services.evidence_ingestion as evidence_ingestion_module
from app.services.controlled_row_preview import APPROVAL_PHRASE as ROW_PREVIEW_APPROVAL_PHRASE
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
    _build_8y16_smoke,
)


EIGHT_Y18_APPROVAL_PHRASE = (
    "APPROVE_8Y_18_CONTROLLED_PRODUCTION_CASE_CANDIDATE_TO_ANALYSIS_RUN_CANDIDATE_SMOKE"
)
EXISTING_ANALYSIS_RUN_HELPER_PHRASE = (
    "APPROVE_8W_34_CONTROLLED_PRODUCTION_ANALYSIS_RUN_CANDIDATE_HELPER_IMPLEMENTATION"
)
MOJIBAKE_ANALYSIS_RUN_HELPER_PHRASE = (
    "\u9395\u7470\u567f 8W-34 Controlled Production Analysis Run Candidate Helper Implementation"
)

EXPECTED_PRODUCTION_CASE_CANDIDATE_SCHEMA = "sentigraph_controlled_production_case_candidate_v0_1"
EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA = "sentigraph_controlled_production_analysis_run_candidate_v0_1"
EXPECTED_EVIDENCEITEM_RUNTIME_SCHEMA = "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1"

FALSE_SIDE_EFFECT_FIELDS = (
    "actual_production_analysis_run_created",
    "production_analysis_run_created",
    "production_analysis_run_runtime_used",
    "production_analysis_run_store_record_created",
    "actual_analysis_execution_started",
    "analysis_execution_started",
    "production_analysis_result_creation_authorized",
    "production_analysis_result_created",
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
    "actual_production_case_created": "source_actual_production_case_created_true",
    "production_case_runtime_used": "source_production_case_runtime_used_true",
    "production_case_store_record_created": "source_production_case_store_record_created_true",
    "actual_production_analysis_run_created": "source_actual_production_analysis_run_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "analysis_execution_started": "source_analysis_execution_started_true",
    "production_analysis_result_creation_authorized": (
        "source_production_analysis_result_creation_authorized_true"
    ),
    "production_analysis_result_created": "source_production_analysis_result_created_true",
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

ANALYSIS_RUN_HELPER_REQUIRED_FALSE_DEFAULTS = (
    "analysis_execution_started",
    "analysis_result_created",
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
    raise AssertionError("8Y-18 must not call production runtime, route, frontend, or delivery helpers")


def _patch_optional(monkeypatch: pytest.MonkeyPatch, module: object, name: str) -> None:
    if hasattr(module, name):
        monkeypatch.setattr(module, name, _fail_if_called)


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
    for name in ("build_controlled_production_case_candidate_set",):
        _patch_optional(monkeypatch, production_case_module, name)
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


def _patch_file_open_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Y-18 controlled smoke must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)


def _safe_8y16_production_case_candidate_smoke() -> dict[str, Any]:
    smoke = _build_8y16_smoke(outer_approval_phrase=EIGHT_Y16_APPROVAL_PHRASE)
    assert smoke["smoke_status"] == "ready"
    assert smoke["production_case_candidate_created"] is True
    assert smoke["production_case_candidate_schema"] == EXPECTED_PRODUCTION_CASE_CANDIDATE_SCHEMA
    candidate_set = smoke["helper_candidate_set"]
    assert isinstance(candidate_set, dict)
    return copy.deepcopy(smoke)


def _blocked_8y18_output(
    reason: str,
    source_smoke: dict[str, Any] | None = None,
) -> dict[str, Any]:
    helper_candidate_set = source_smoke.get("helper_candidate_set") if isinstance(source_smoke, dict) else None
    return {
        "schema": "sentigraph_8y18_controlled_production_case_candidate_to_analysis_run_candidate_smoke_v0_1",
        "phase": "8Y-18",
        "smoke_status": "blocked",
        "source_path_step": "production_case_candidate_to_production_analysis_run_candidate",
        "outer_8y18_phrase": None,
        "production_analysis_run_candidate_created": False,
        "production_analysis_run_candidate_schema": None,
        "production_analysis_run_candidate_mode": None,
        "source_production_case_candidate_schema": (
            source_smoke.get("production_case_candidate_schema") if isinstance(source_smoke, dict) else None
        ),
        "source_evidence_write_result_schema": (
            helper_candidate_set.get("source_runtime_schema") if isinstance(helper_candidate_set, dict) else None
        ),
        "candidate_only": True,
        "backend_only": True,
        "local_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "warning_count": 0,
        "blockers": [reason],
        "warnings": [],
        "helper_candidate_set": None,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _source_blockers(source_smoke: dict[str, Any] | None) -> list[str]:
    if not isinstance(source_smoke, dict):
        return ["source_production_case_candidate_smoke_missing_or_not_object"]

    blockers: list[str] = []
    if source_smoke.get("smoke_status") != "ready":
        blockers.append("source_production_case_candidate_smoke_not_ready")
    if source_smoke.get("production_case_candidate_created") is not True:
        blockers.append("source_production_case_candidate_created_not_true")
    if source_smoke.get("production_case_candidate_schema") != EXPECTED_PRODUCTION_CASE_CANDIDATE_SCHEMA:
        blockers.append("source_production_case_candidate_schema_wrong")
    if source_smoke.get("human_review_required") is not True:
        blockers.append("source_human_review_required_not_true")
    if source_smoke.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")
    for field, reason in SOURCE_TRUE_BLOCKERS.items():
        if source_smoke.get(field) is True:
            blockers.append(reason)

    helper_candidate_set = source_smoke.get("helper_candidate_set")
    if not isinstance(helper_candidate_set, dict):
        blockers.append("source_helper_production_case_candidate_set_missing_or_not_object")
    return blockers


def _analysis_run_source_candidate_set(source_smoke: dict[str, Any]) -> dict[str, Any]:
    source_candidate_set = copy.deepcopy(source_smoke["helper_candidate_set"])
    for field in ANALYSIS_RUN_HELPER_REQUIRED_FALSE_DEFAULTS:
        source_candidate_set.setdefault(field, False)
    return source_candidate_set


def _build_8y18_smoke(
    *,
    outer_approval_phrase: str | None,
    source_case_candidate_smoke: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if outer_approval_phrase is None or outer_approval_phrase == "":
        return _blocked_8y18_output("blocked_missing_exact_8y18_approval")
    if outer_approval_phrase != EIGHT_Y18_APPROVAL_PHRASE:
        return _blocked_8y18_output("blocked_wrong_exact_8y18_approval")

    source_smoke = source_case_candidate_smoke or _safe_8y16_production_case_candidate_smoke()
    source_blockers = _source_blockers(source_smoke)
    if source_blockers:
        return _blocked_8y18_output(source_blockers[0], source_smoke)

    source_candidate_set = _analysis_run_source_candidate_set(source_smoke)
    candidate_set = production_analysis_run_module.build_controlled_production_analysis_run_candidate_set(
        source_candidate_set,
        exact_approval_phrase=production_analysis_run_module.APPROVAL_PHRASE,
    )
    candidates = candidate_set["production_analysis_run_candidates"]
    candidate = candidates[0] if candidates else {}
    created = candidate_set["production_analysis_run_candidate_created"] is True
    return {
        "schema": "sentigraph_8y18_controlled_production_case_candidate_to_analysis_run_candidate_smoke_v0_1",
        "phase": "8Y-18",
        "smoke_status": "ready" if created else "blocked",
        "source_path_step": "production_case_candidate_to_production_analysis_run_candidate",
        "outer_8y18_phrase": EIGHT_Y18_APPROVAL_PHRASE,
        "production_analysis_run_candidate_created": created,
        "production_analysis_run_candidate_schema": candidate.get("production_analysis_run_candidate_schema"),
        "production_analysis_run_candidate_mode": candidate_set["production_analysis_run_candidate_mode"],
        "source_production_case_candidate_schema": candidate_set["source_production_case_candidate_schema"],
        "source_evidence_write_result_schema": source_candidate_set.get("source_runtime_schema"),
        "candidate_only": candidate_set["production_analysis_run_candidate_only"],
        "backend_only": candidate_set["boundary_flags"]["backend_only"],
        "local_only": candidate_set["boundary_flags"]["local_only"],
        "human_review_required": candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": candidate_set["no_automatic_trust_upgrade"],
        "warning_count": candidate_set["warning_count"],
        "blockers": list(candidate_set["blockers"]),
        "warnings": list(candidate_set["warnings"]),
        "helper_candidate_set": candidate_set,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _assert_false_side_effects(smoke: dict[str, Any]) -> None:
    for field in FALSE_SIDE_EFFECT_FIELDS:
        assert smoke[field] is False, field
    candidate_set = smoke.get("helper_candidate_set")
    if isinstance(candidate_set, dict):
        assert candidate_set["production_analysis_run_created"] is False
        assert candidate_set["analysis_execution_started"] is False
        assert candidate_set["analysis_result_created"] is False
        assert candidate_set["production_case_created"] is False
        assert candidate_set["production_evidence_item_created"] is False
        assert candidate_set["review_queue_runtime_used"] is False
        assert candidate_set["route_ready"] is False
        assert candidate_set["frontend_ready"] is False
        assert candidate_set["production_ready"] is False
        assert candidate_set["public_ready"] is False
        assert candidate_set["customer_ready"] is False
        for flag, value in candidate_set["runtime_side_effects"].items():
            assert value is False, flag
    _assert_no_forbidden_output(smoke)


def _assert_blocked_before_analysis_run_candidate_helper(
    smoke: dict[str, Any],
    expected_reason: str,
) -> None:
    assert smoke["smoke_status"] == "blocked"
    assert smoke["production_analysis_run_candidate_created"] is False
    assert smoke["production_analysis_run_candidate_schema"] is None
    assert smoke["helper_candidate_set"] is None
    assert smoke["blockers"] == [expected_reason]
    _assert_false_side_effects(smoke)


def test_8y18_ready_path_builds_local_production_analysis_run_candidate_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert production_analysis_run_module.APPROVAL_PHRASE == EXISTING_ANALYSIS_RUN_HELPER_PHRASE
    assert production_analysis_run_module.APPROVAL_PHRASE.isascii()
    source_smoke = _safe_8y16_production_case_candidate_smoke()
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y18_smoke(
        outer_approval_phrase=EIGHT_Y18_APPROVAL_PHRASE,
        source_case_candidate_smoke=source_smoke,
    )

    assert smoke["smoke_status"] == "ready"
    assert smoke["production_analysis_run_candidate_created"] is True
    assert smoke["production_analysis_run_candidate_schema"] == EXPECTED_ANALYSIS_RUN_CANDIDATE_SCHEMA
    assert smoke["production_analysis_run_candidate_mode"] == (
        "backend_only_local_production_analysis_run_candidate_boundary"
    )
    assert smoke["source_production_case_candidate_schema"] == EXPECTED_PRODUCTION_CASE_CANDIDATE_SCHEMA
    assert smoke["source_evidence_write_result_schema"] == EXPECTED_EVIDENCEITEM_RUNTIME_SCHEMA
    assert smoke["candidate_only"] is True
    assert smoke["backend_only"] is True
    assert smoke["local_only"] is True
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    assert smoke["warning_count"] == 1
    assert "manual_review_required" in smoke["warnings"]

    candidate_set = smoke["helper_candidate_set"]
    assert isinstance(candidate_set, dict)
    assert candidate_set["production_analysis_run_candidate_set_schema"] == (
        "sentigraph_controlled_production_analysis_run_candidate_set_v0_1"
    )
    assert candidate_set["production_analysis_run_candidate_created"] is True
    assert candidate_set["production_analysis_run_candidate_count"] == 1
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["analysis_result_created"] is False
    assert candidate_set["production_case_created"] is False
    assert candidate_set["audit_summary"]["analysis_execution_effect"] == "none"
    assert candidate_set["audit_summary"]["production_side_effect"] == "none"
    _assert_false_side_effects(smoke)


@pytest.mark.parametrize(
    "outer_phrase",
    [
        None,
        "",
        "wrong approval",
        EIGHT_Y16_APPROVAL_PHRASE,
        EIGHT_Y14_APPROVAL_PHRASE,
        REPAIRED_HELPER_PHRASE,
        EIGHT_Y13C_APPROVAL_PHRASE,
        EIGHT_Y12_APPROVAL_PHRASE,
        EIGHT_Y10_APPROVAL_PHRASE,
        EIGHT_Y8_APPROVAL_PHRASE,
        EIGHT_Y6_APPROVAL_PHRASE,
        ROW_PREVIEW_APPROVAL_PHRASE,
    ],
)
def test_exact_8y18_phrase_required_before_analysis_run_candidate_helper(
    outer_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        production_analysis_run_module,
        "build_controlled_production_analysis_run_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y18_smoke(outer_approval_phrase=outer_phrase)

    expected = "blocked_missing_exact_8y18_approval" if outer_phrase in {None, ""} else (
        "blocked_wrong_exact_8y18_approval"
    )
    _assert_blocked_before_analysis_run_candidate_helper(smoke, expected)


def test_existing_analysis_run_helper_rejects_mojibake_phrase() -> None:
    assert production_analysis_run_module.APPROVAL_PHRASE == EXISTING_ANALYSIS_RUN_HELPER_PHRASE
    assert production_analysis_run_module.APPROVAL_PHRASE.isascii()
    assert MOJIBAKE_ANALYSIS_RUN_HELPER_PHRASE != production_analysis_run_module.APPROVAL_PHRASE

    source_smoke = _safe_8y16_production_case_candidate_smoke()
    candidate_set = production_analysis_run_module.build_controlled_production_analysis_run_candidate_set(
        _analysis_run_source_candidate_set(source_smoke),
        exact_approval_phrase=MOJIBAKE_ANALYSIS_RUN_HELPER_PHRASE,
    )

    assert candidate_set["production_analysis_run_candidate_created"] is False
    assert "blocked_non_ascii_approval" in candidate_set["blockers"]
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["analysis_result_created"] is False
    _assert_no_forbidden_output(candidate_set)


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        ("production_case_candidate_schema", "wrong", "source_production_case_candidate_schema_wrong"),
        ("actual_production_case_created", True, "source_actual_production_case_created_true"),
        ("production_case_runtime_used", True, "source_production_case_runtime_used_true"),
        ("production_case_store_record_created", True, "source_production_case_store_record_created_true"),
        ("actual_production_analysis_run_created", True, "source_actual_production_analysis_run_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("actual_analysis_execution_started", True, "source_actual_analysis_execution_started_true"),
        ("analysis_execution_started", True, "source_analysis_execution_started_true"),
        (
            "production_analysis_result_creation_authorized",
            True,
            "source_production_analysis_result_creation_authorized_true",
        ),
        ("production_analysis_result_created", True, "source_production_analysis_result_created_true"),
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
def test_unsafe_source_blocks_before_analysis_run_candidate_helper(
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source_smoke = _safe_8y16_production_case_candidate_smoke()
    source_smoke[field] = value
    monkeypatch.setattr(
        production_analysis_run_module,
        "build_controlled_production_analysis_run_candidate_set",
        _fail_if_called,
    )
    _patch_forbidden_runtime_entrypoints(monkeypatch)

    smoke = _build_8y18_smoke(
        outer_approval_phrase=EIGHT_Y18_APPROVAL_PHRASE,
        source_case_candidate_smoke=source_smoke,
    )

    _assert_blocked_before_analysis_run_candidate_helper(smoke, expected_reason)


def test_helper_blocks_requested_production_analysis_run_or_execution_actions() -> None:
    source_smoke = _safe_8y16_production_case_candidate_smoke()
    candidate_set = production_analysis_run_module.build_controlled_production_analysis_run_candidate_set(
        _analysis_run_source_candidate_set(source_smoke),
        exact_approval_phrase=production_analysis_run_module.APPROVAL_PHRASE,
        requested_actions=["production_analysis_run", "analysis_execution"],
    )

    assert candidate_set["production_analysis_run_candidate_created"] is False
    assert "requested_action_blocked:production_analysis_run" in candidate_set["blockers"]
    assert "requested_action_blocked:analysis_execution" in candidate_set["blockers"]
    assert candidate_set["production_analysis_run_created"] is False
    assert candidate_set["analysis_execution_started"] is False
    assert candidate_set["analysis_result_created"] is False
    _assert_no_forbidden_output(candidate_set)


def test_8y18_smoke_output_is_json_serializable_without_raw_or_absolute_values() -> None:
    smoke = _build_8y18_smoke(outer_approval_phrase=EIGHT_Y18_APPROVAL_PHRASE)

    json.dumps(smoke, ensure_ascii=False, sort_keys=True, default=str)
    _assert_false_side_effects(smoke)
