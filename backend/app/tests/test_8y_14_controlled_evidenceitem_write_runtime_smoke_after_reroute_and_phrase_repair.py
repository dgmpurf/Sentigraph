from __future__ import annotations

import builtins
import copy
import json
from pathlib import Path
from typing import Any

import pytest

import app.services.analysis_request_store as analysis_request_store
import app.services.controlled_evidenceitem_evidence_layer_write_runtime as evidenceitem_write_module
import app.services.controlled_production_analysis_run_candidate as production_analysis_run_module
import app.services.controlled_production_case_candidate as production_case_module
import app.services.evidence_import as evidence_import_module
import app.services.evidence_ingestion as evidence_ingestion_module
from app.tests.test_8y_13c_controlled_production_import_derived_reroute_smoke import (
    EIGHT_Y10_APPROVAL_PHRASE,
    EIGHT_Y12_APPROVAL_PHRASE,
    EIGHT_Y13C_APPROVAL_PHRASE,
    EIGHT_Y6_APPROVAL_PHRASE,
    EIGHT_Y8_APPROVAL_PHRASE,
    OLD_EIGHT_Y14_APPROVAL_PHRASE,
    _assert_no_forbidden_output,
)
from app.tests.test_controlled_evidenceitem_evidence_layer_write_runtime import (
    _valid_write_candidate_set,
)


EIGHT_Y14_APPROVAL_PHRASE = (
    "APPROVE_8Y_14_CONTROLLED_EVIDENCEITEM_WRITE_RUNTIME_SMOKE_AFTER_REROUTE_AND_PHRASE_REPAIR"
)
OLDER_AFTER_REROUTE_EIGHT_Y14_APPROVAL_PHRASE = (
    "APPROVE_8Y_14_CONTROLLED_EVIDENCEITEM_WRITE_RUNTIME_SMOKE_AFTER_REROUTE"
)
REPAIRED_HELPER_PHRASE = (
    "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION"
)
OLD_CHINESE_HELPER_PHRASE = "\u6279\u51c6 8W-28 Controlled EvidenceItem Evidence Layer Write Runtime Implementation"
MOJIBAKE_HELPER_PHRASE = (
    "\u93b5\u7470\u566f 8W-28 Controlled EvidenceItem Evidence Layer Write Runtime Implementation"
)
ALT_MOJIBAKE_HELPER_PHRASE = (
    "闁圭數鎳撻崳?8W-28 Controlled EvidenceItem Evidence Layer Write Runtime Implementation"
)

FALSE_SIDE_EFFECT_FIELDS = (
    "evidence_import_service_called",
    "evidence_ingestion_service_called",
    "general_production_import_service_called",
    "production_case_created",
    "production_analysis_run_created",
    "production_analysis_result_creation_authorized",
    "actual_review_queue_runtime_used",
    "production_review_queue_item_created",
    "source11_runtime_called",
    "actual_final_summary_report_created",
    "b_end_report_runtime_generated",
    "sandbox_public_event_runtime_generated",
    "export_download_public_delivery_created",
    "generated_response_text",
    "route_changed",
    "frontend_changed",
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


def _fail_if_called(*args: object, **kwargs: object) -> None:
    raise AssertionError("8Y-14 must not call production services, routes, frontend, or delivery helpers")


def _patch_optional(monkeypatch: pytest.MonkeyPatch, module: object, name: str) -> None:
    if hasattr(module, name):
        monkeypatch.setattr(module, name, _fail_if_called)


def _patch_forbidden_non_write_runtime_entrypoints(monkeypatch: pytest.MonkeyPatch) -> None:
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
    for name in ("build_controlled_production_analysis_run_candidate_set",):
        _patch_optional(monkeypatch, production_analysis_run_module, name)
    for name in (
        "create_review_queue_initialization",
        "create_review_queue_item_action",
        "create_review_queue_completion_gate",
        "create_final_summary_report",
        "create_report_export_download_package_artifact",
        "create_report_export_public_access_external_delivery_gate",
    ):
        _patch_optional(monkeypatch, analysis_request_store, name)


def _patch_file_open_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    def blocked_open(*args: object, **kwargs: object) -> None:
        raise AssertionError("8Y-14 controlled smoke must not open files")

    monkeypatch.setattr(builtins, "open", blocked_open)
    monkeypatch.setattr(Path, "open", blocked_open)


def _safe_8y13c_equivalent_production_import_derived_write_candidate_set() -> dict[str, Any]:
    candidate_set = copy.deepcopy(_valid_write_candidate_set())
    assert candidate_set["evidence_layer_write_candidate_set_schema"] == (
        "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
    )
    candidate_set["no_automatic_trust_upgrade"] = True
    candidate_set["controlled_evidenceitem_write_runtime_called"] = False
    candidate_set["production_evidenceitem_write_runtime_used"] = False
    candidate_set["source_path_step"] = "production_import_derived_write_candidate_to_controlled_evidenceitem_write_runtime"
    return candidate_set


def _blocked_8y14_output(reason: str) -> dict[str, Any]:
    return {
        "schema": "sentigraph_8y14_controlled_evidenceitem_write_runtime_smoke_v0_1",
        "phase": "8Y-14",
        "smoke_status": "blocked",
        "source_path_step": "production_import_derived_write_candidate_to_controlled_evidenceitem_write_runtime",
        "controlled_evidenceitem_write_runtime_called": False,
        "production_evidenceitem_write_runtime_used": False,
        "controlled_evidenceitem_write_result_created": False,
        "evidence_write_result_schema": None,
        "write_result_schema": None,
        "evidence_write_mode": None,
        "source_production_import_derived_write_candidate_schema": None,
        "actual_evidence_layer_write_used": False,
        "evidence_layer_write": False,
        "evidence_layer_write_scope": "not_performed",
        "production_evidence_item_created": False,
        "persisted_evidence_layer_record_created": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "warning_count": 0,
        "blockers": [reason],
        "warnings": [],
        "helper_runtime": None,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _build_8y14_smoke(
    *,
    outer_approval_phrase: str | None,
    helper_phrase: str | None = REPAIRED_HELPER_PHRASE,
    source_candidate_set: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if outer_approval_phrase is None or outer_approval_phrase == "":
        return _blocked_8y14_output("blocked_missing_exact_8y14_approval")
    if outer_approval_phrase != EIGHT_Y14_APPROVAL_PHRASE:
        return _blocked_8y14_output("blocked_wrong_exact_8y14_approval")

    source = source_candidate_set or _safe_8y13c_equivalent_production_import_derived_write_candidate_set()
    runtime = evidenceitem_write_module.build_controlled_evidenceitem_evidence_layer_write_runtime(
        source,
        exact_approval_phrase=helper_phrase,
    )
    result_created = runtime["controlled_evidence_layer_write_result_created"] is True
    return {
        "schema": "sentigraph_8y14_controlled_evidenceitem_write_runtime_smoke_v0_1",
        "phase": "8Y-14",
        "smoke_status": "ready" if result_created else "blocked",
        "source_path_step": "production_import_derived_write_candidate_to_controlled_evidenceitem_write_runtime",
        "controlled_evidenceitem_write_runtime_called": True,
        "production_evidenceitem_write_runtime_used": True,
        "controlled_evidenceitem_write_result_created": result_created,
        "evidence_write_result_schema": runtime["runtime_schema"] if result_created else None,
        "write_result_schema": runtime["write_result_schema"] if result_created else None,
        "evidence_write_mode": "controlled_backend_only_evidence_layer_write_runtime" if result_created else None,
        "source_production_import_derived_write_candidate_schema": runtime["source_candidate_set_schema"],
        "actual_evidence_layer_write_used": runtime["evidence_layer_write"] is True,
        "evidence_layer_write": runtime["evidence_layer_write"] is True,
        "evidence_layer_write_scope": runtime["evidence_layer_write_scope"],
        "production_evidence_item_created": runtime["production_evidence_item_created"],
        "persisted_evidence_layer_record_created": False,
        "human_review_required": runtime["human_review_required"],
        "no_automatic_trust_upgrade": runtime["no_automatic_trust_upgrade"],
        "warning_count": runtime["warning_count"],
        "blockers": list(runtime["blockers"]),
        "warnings": list(runtime["warnings"]),
        "helper_runtime": runtime,
        **{field: False for field in FALSE_SIDE_EFFECT_FIELDS},
    }


def _assert_smoke_safe(smoke: dict[str, Any]) -> None:
    for field in FALSE_SIDE_EFFECT_FIELDS:
        assert smoke[field] is False, field
    assert smoke["production_evidence_item_created"] is False
    assert smoke["persisted_evidence_layer_record_created"] is False
    assert smoke["production_case_created"] is False
    assert smoke["production_analysis_run_created"] is False
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    _assert_no_forbidden_output(smoke)


def _assert_runtime_side_effects_false(runtime: dict[str, Any]) -> None:
    runtime_side_effects = runtime["runtime_side_effects"]
    assert isinstance(runtime_side_effects, dict)
    for flag, value in runtime_side_effects.items():
        assert value is False, flag


def _assert_blocked_before_write_runtime(smoke: dict[str, Any], expected_reason: str) -> None:
    assert smoke["smoke_status"] == "blocked"
    assert smoke["controlled_evidenceitem_write_runtime_called"] is False
    assert smoke["production_evidenceitem_write_runtime_used"] is False
    assert smoke["controlled_evidenceitem_write_result_created"] is False
    assert smoke["actual_evidence_layer_write_used"] is False
    assert smoke["evidence_layer_write"] is False
    assert smoke["blockers"] == [expected_reason]
    _assert_smoke_safe(smoke)


def _assert_blocked_by_helper(smoke: dict[str, Any], expected_reason: str) -> None:
    assert smoke["smoke_status"] == "blocked"
    assert smoke["controlled_evidenceitem_write_runtime_called"] is True
    assert smoke["production_evidenceitem_write_runtime_used"] is True
    assert smoke["controlled_evidenceitem_write_result_created"] is False
    assert smoke["actual_evidence_layer_write_used"] is False
    assert smoke["evidence_layer_write"] is False
    assert expected_reason in smoke["blockers"]
    assert isinstance(smoke["helper_runtime"], dict)
    _assert_runtime_side_effects_false(smoke["helper_runtime"])
    _assert_smoke_safe(smoke)


def test_8y14_ready_path_calls_controlled_write_runtime_only_inside_backend_test_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert evidenceitem_write_module.APPROVAL_PHRASE == REPAIRED_HELPER_PHRASE
    assert evidenceitem_write_module.APPROVAL_PHRASE.isascii()
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)

    smoke = _build_8y14_smoke(outer_approval_phrase=EIGHT_Y14_APPROVAL_PHRASE)

    assert smoke["smoke_status"] == "ready"
    assert smoke["controlled_evidenceitem_write_runtime_called"] is True
    assert smoke["production_evidenceitem_write_runtime_used"] is True
    assert smoke["controlled_evidenceitem_write_result_created"] is True
    assert smoke["evidence_write_result_schema"] == (
        "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1"
    )
    assert smoke["write_result_schema"] == "sentigraph_controlled_evidence_layer_write_result_v0_1"
    assert smoke["evidence_write_mode"] == "controlled_backend_only_evidence_layer_write_runtime"
    assert smoke["source_production_import_derived_write_candidate_schema"] == (
        "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
    )
    assert smoke["actual_evidence_layer_write_used"] is True
    assert smoke["evidence_layer_write"] is True
    assert smoke["evidence_layer_write_scope"] == "controlled_local_helper_test_path_only"
    assert smoke["warning_count"] == 1
    assert "manual_review_required" in smoke["warnings"]
    assert smoke["blockers"] == []

    runtime = smoke["helper_runtime"]
    assert isinstance(runtime, dict)
    assert runtime["controlled_evidence_item_count"] > 0
    assert runtime["controlled_evidence_item_count"] <= 10
    assert runtime["production_evidence_item_created"] is False
    assert runtime["production_case_created"] is False
    assert runtime["production_analysis_run_created"] is False
    assert runtime["review_queue_runtime_used"] is False
    assert runtime["route_ready"] is False
    assert runtime["frontend_ready"] is False
    assert runtime["production_ready"] is False
    assert runtime["public_ready"] is False
    assert runtime["customer_ready"] is False
    assert runtime["audit_summary"]["production_side_effect"] == "none"
    _assert_runtime_side_effects_false(runtime)
    _assert_smoke_safe(smoke)


@pytest.mark.parametrize(
    "outer_phrase",
    [
        None,
        "",
        "wrong approval",
        OLD_EIGHT_Y14_APPROVAL_PHRASE,
        OLDER_AFTER_REROUTE_EIGHT_Y14_APPROVAL_PHRASE,
        EIGHT_Y13C_APPROVAL_PHRASE,
        EIGHT_Y12_APPROVAL_PHRASE,
        EIGHT_Y10_APPROVAL_PHRASE,
        EIGHT_Y8_APPROVAL_PHRASE,
        EIGHT_Y6_APPROVAL_PHRASE,
        REPAIRED_HELPER_PHRASE,
    ],
)
def test_outer_8y14_phrase_required_before_controlled_write_runtime_call(
    outer_phrase: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        evidenceitem_write_module,
        "build_controlled_evidenceitem_evidence_layer_write_runtime",
        _fail_if_called,
    )
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)

    smoke = _build_8y14_smoke(outer_approval_phrase=outer_phrase)

    expected = "blocked_missing_exact_8y14_approval" if outer_phrase in {None, ""} else (
        "blocked_wrong_exact_8y14_approval"
    )
    _assert_blocked_before_write_runtime(smoke, expected)


@pytest.mark.parametrize(
    ("helper_phrase", "expected_reason"),
    [
        (None, "blocked_missing_exact_approval"),
        ("", "blocked_missing_exact_approval"),
        ("wrong helper", "blocked_wrong_exact_approval"),
        (OLD_CHINESE_HELPER_PHRASE, "blocked_wrong_exact_approval"),
        (MOJIBAKE_HELPER_PHRASE, "blocked_wrong_exact_approval"),
        (ALT_MOJIBAKE_HELPER_PHRASE, "blocked_wrong_exact_approval"),
    ],
)
def test_repaired_helper_phrase_required_at_helper_layer(
    helper_phrase: str | None,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)

    smoke = _build_8y14_smoke(
        outer_approval_phrase=EIGHT_Y14_APPROVAL_PHRASE,
        helper_phrase=helper_phrase,
    )

    _assert_blocked_by_helper(smoke, expected_reason)


@pytest.mark.parametrize(
    ("field", "value", "expected_reason"),
    [
        (
            "evidence_layer_write_candidate_set_schema",
            "wrong",
            "source_evidence_layer_write_candidate_set_schema_wrong",
        ),
        ("raw_rows_exposed", True, "source_raw_rows_exposed_true"),
        ("raw_comments_exposed", True, "source_raw_comments_exposed_true"),
        ("raw_identities_exposed", True, "source_raw_identities_exposed_true"),
        (
            "author_names_or_profile_urls_exposed",
            True,
            "source_author_names_or_profile_urls_exposed_true",
        ),
        ("production_case_created", True, "source_production_case_created_true"),
        ("production_analysis_run_created", True, "source_production_analysis_run_created_true"),
        ("evidence_import_service_called", True, "source_evidence_import_service_called_true"),
        ("evidence_ingestion_service_called", True, "source_evidence_ingestion_service_called_true"),
        ("source11_runtime_called", True, "source_source11_runtime_called_true"),
        ("actual_final_summary_report_created", True, "source_actual_final_summary_report_created_true"),
    ],
)
def test_unsafe_source_candidate_set_blocks_at_helper_layer(
    field: str,
    value: object,
    expected_reason: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)
    source = _safe_8y13c_equivalent_production_import_derived_write_candidate_set()
    source[field] = value

    smoke = _build_8y14_smoke(
        outer_approval_phrase=EIGHT_Y14_APPROVAL_PHRASE,
        source_candidate_set=source,
    )

    _assert_blocked_by_helper(smoke, expected_reason)


def test_no_automatic_trust_upgrade_false_preserves_warning_and_manual_review_semantics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)
    source = _safe_8y13c_equivalent_production_import_derived_write_candidate_set()
    source["no_automatic_trust_upgrade"] = False

    smoke = _build_8y14_smoke(
        outer_approval_phrase=EIGHT_Y14_APPROVAL_PHRASE,
        source_candidate_set=source,
    )

    assert smoke["smoke_status"] == "ready"
    assert smoke["controlled_evidenceitem_write_runtime_called"] is True
    assert smoke["controlled_evidenceitem_write_result_created"] is True
    assert smoke["human_review_required"] is True
    assert smoke["no_automatic_trust_upgrade"] is True
    assert smoke["warning_count"] == 1
    assert "manual_review_required" in smoke["warnings"]
    _assert_smoke_safe(smoke)


def test_requested_side_effects_still_block_through_helper_layer(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_file_open_blocked(monkeypatch)
    _patch_forbidden_non_write_runtime_entrypoints(monkeypatch)
    source = _safe_8y13c_equivalent_production_import_derived_write_candidate_set()
    runtime = evidenceitem_write_module.build_controlled_evidenceitem_evidence_layer_write_runtime(
        source,
        exact_approval_phrase=REPAIRED_HELPER_PHRASE,
        requested_actions=["production_case"],
    )

    assert runtime["write_runtime_status"] == "blocked_unapproved_production_case_or_analysis_run_request"
    assert "requested_action_blocked:production_case" in runtime["blockers"]
    assert runtime["controlled_evidence_layer_write_result_created"] is False
    assert runtime["production_case_created"] is False
    assert runtime["production_analysis_run_created"] is False
    _assert_runtime_side_effects_false(runtime)
    _assert_no_forbidden_output(runtime)


def test_smoke_output_is_json_serializable_without_raw_or_absolute_values() -> None:
    smoke = _build_8y14_smoke(outer_approval_phrase=EIGHT_Y14_APPROVAL_PHRASE)

    json.dumps(smoke, ensure_ascii=False, sort_keys=True, default=str)
    _assert_no_forbidden_output(smoke)
