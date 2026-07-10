from __future__ import annotations

import inspect
import io
import json
import logging
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest


OUTER_APPROVAL_PHRASE = "APPROVE_9A_16_ONE_REAL_EXPORTED_PACKAGE_BOUNDED_REDACTED_ROW_CANDIDATE_SPECIFIC_EVIDENCE_LAYER_PRE_WRITE_REVIEW_NO_WRITE"
INNER_ROW_PREVIEW_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
OLD_CHINESE_ROW_PREVIEW_PHRASE = "批准 8W-7 Controlled Row Preview Implementation"
MOJIBAKE_ROW_PREVIEW_PHRASE = "鎵瑰噯 8W-7 Controlled Row Preview Implementation"

APPROVED_PACKAGE_NAME = "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
APPROVED_PACKAGE_ROLE = "candidate_demo_sample"
APPROVED_CASE_ID_HINT = "donglu_sunjihai_youth_football_202606"
APPROVED_ROW_SOURCE = "evidence_items.jsonl"

AUDIT_SCHEMA = "sentigraph_one_real_exported_package_candidate_pre_write_review_audit_v0_1"
AUDIT_MODE = "backend_only_local_one_real_exported_package_candidate_pre_write_review_no_write"

STAGE_SCHEMAS = {
    "controlled_row_preview": "sentigraph_controlled_row_preview_v0_1",
    "controlled_evidence_candidate": "sentigraph_controlled_evidence_candidate_set_v0_1",
    "controlled_review_queue_candidate": "sentigraph_controlled_review_queue_candidate_set_v0_1",
    "controlled_evidence_layer_import_candidate": "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
    "controlled_direct_write_candidate": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
    "controlled_production_evidence_import_candidate": "sentigraph_controlled_production_evidence_import_candidate_set_v0_1",
    "production_import_derived_write_candidate": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
}

EXPECTED_LINEAGE_STAGES = [
    "real_exported_package_metadata",
    "approved_evidence_items_jsonl",
    "bounded_redacted_preview_row",
    "controlled_evidence_candidate",
    "controlled_review_queue_candidate",
    "controlled_evidence_layer_import_candidate",
    "controlled_direct_write_candidate",
    "controlled_production_evidence_import_candidate",
    "production_import_derived_write_candidate",
    "one_real_candidate_pre_write_review",
]

RISK_CATEGORIES = {
    "wrong_package_selection_risk",
    "excessive_row_read_risk",
    "raw_content_retention_risk",
    "raw_identity_privacy_risk",
    "secret_exposure_risk",
    "lineage_mismatch_risk",
    "irreversible_write_risk",
    "authorization_confusion_risk",
    "trust_inflation_risk",
    "provider_vendor_output_mistaken_as_truth_risk",
    "duplicate_amplification_risk",
    "rejected_weak_evidence_inclusion_risk",
    "route_api_frontend_accidental_write_exposure_risk",
    "downstream_production_escalation_risk",
    "source11_finalsummaryreport_escalation_risk",
    "public_customer_readiness_overclaim_risk",
}

ALLOWED_RISK_LABELS = {
    "mitigated_for_this_bounded_review",
    "open",
    "unknown",
    "not_applicable_to_no_write_review",
    "blocked",
}

FALSE_FLAGS = [
    "actual_write_authorized",
    "actual_evidence_layer_write_approved",
    "actual_evidence_layer_write_performed",
    "persisted_evidence_layer_record_created",
    "production_evidenceitem_creation_authorized",
    "production_evidenceitem_created",
    "write_helper_execution_allowed",
    "write_authorization_object_created_that_permits_write",
    "evidenceitem_write_runtime_called",
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "runtime_human_authority_validation_performed",
    "runtime_manual_review_responsibility_acceptance_performed",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "review_queue_runtime_used",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_authorized",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
]

NEIGHBOR_OUTER_PHRASES = [
    INNER_ROW_PREVIEW_PHRASE,
    "APPROVE_9A_15_CONTROLLED_CANDIDATE_SPECIFIC_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_PRE_WRITE_REVIEW_AUDIT_NO_WRITE",
    "APPROVE_9A_14_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_RECOGNITION_SAFETY_CONTRACT_TESTS_ONLY",
    "APPROVE_8Y_13C_CONTROLLED_PRODUCTION_IMPORT_DERIVED_REROUTE_SMOKE",
    "APPROVE_GENERIC_ONE_REAL_PACKAGE_REVIEW",
]


def _service():
    return import_module("app.services.evidence_layer_one_real_candidate_pre_write_review")


def _safe_declaration_context(**overrides: object) -> dict[str, object]:
    context: dict[str, object] = {
        "declaration_source_kind": "explicit_human_message_later",
        "recognition_outcome": "declaration_present_for_docs_only_review",
        "declared_authority_role_label": "self_declared_project_owner_role",
        "authority_basis_label": "authority_basis_not_independently_validated",
        "manual_review_responsibility_statement_present": True,
        "warning_count_acknowledgment_present": True,
        "human_review_required_acknowledgment_present": True,
        "no_automatic_trust_upgrade_acknowledgment_present": True,
        "rollback_pause_revocation_responsibility_label": "self_declared_project_owner_role",
        "human_authority_validated": False,
        "manual_review_responsibility_accepted": False,
        "runtime_human_authority_validation_performed": False,
        "runtime_manual_review_responsibility_acceptance_performed": False,
        "final_write_authorization_performed": False,
        "final_write_authorization_still_required": True,
        "actual_write_authorized": False,
        "production_evidenceitem_creation_authorized": False,
        "ready_for_actual_write": False,
    }
    context.update(overrides)
    return context


def _safe_rollback_plan(**overrides: object) -> dict[str, object]:
    plan: dict[str, object] = {
        "pause_on_any_blocker": True,
        "revocation_target_kind": "one_real_source_controlled_candidate",
        "revocation_target_ref": "bind_selected_safe_final_candidate",
        "rollback_action": "discard_in_memory_preview_candidates_and_audit",
        "persistence_rollback_required": False,
        "no_persistence": True,
        "final_write_authorization_still_required": True,
    }
    plan.update(overrides)
    return plan


def _build(
    *,
    phrase: str | None = OUTER_APPROVAL_PHRASE,
    declaration_context: dict[str, object] | None = None,
    rollback_plan: dict[str, object] | None = None,
) -> dict[str, Any]:
    return _service().review_one_real_exported_package_candidate_pre_write(
        exact_outer_approval_phrase=phrase,
        declaration_context=declaration_context or _safe_declaration_context(),
        rollback_plan=rollback_plan or _safe_rollback_plan(),
    )


def _serialized(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def _json_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        keys = {str(key) for key in value}
        for nested in value.values():
            keys.update(_json_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_json_keys(item))
        return keys
    return set()


def _safe_synthetic_chain() -> dict[str, Any]:
    evidence_hash = "a1b2c3d4e5f60718"
    preview_id = "preview-row-001"
    evidence_candidate_id = f"candidate-001-{evidence_hash}"
    review_candidate_id = f"review-queue-candidate-001-{evidence_hash}"
    import_candidate_id = f"evidence-layer-import-candidate-001-{evidence_hash}"
    direct_write_id = f"evidence-layer-write-candidate-001-{evidence_hash}"
    production_import_id = f"production-evidence-import-candidate-001-{evidence_hash}"
    final_candidate_id = f"evidence-layer-write-candidate-from-production-import-001-{evidence_hash}"
    snippet = "synthetic-redacted-placeholder"
    safe_boundary = {
        "preview_only": True,
        "human_review_required": True,
        "not_production_evidence_item": True,
        "no_evidence_layer_write": True,
        "not_production_case": True,
        "not_production_analysis_run": True,
    }
    return {
        "row_preview": {
            "schema": STAGE_SCHEMAS["controlled_row_preview"],
            "preview_status": "row_preview_warn_manual_review_required",
            "approved_target_package_name": APPROVED_PACKAGE_NAME,
            "approved_target_package_role": APPROVED_PACKAGE_ROLE,
            "approved_target_case_id_hint": APPROVED_CASE_ID_HINT,
            "row_source": APPROVED_ROW_SOURCE,
            "max_preview_rows_requested": 1,
            "max_preview_rows_applied": 1,
            "rows_inspected_count": 1,
            "preview_rows_count": 1,
            "row_limit_enforced": True,
            "warning_count": 1,
            "human_review_required": True,
            "preview_rows": [{
                "preview_row_id": preview_id,
                "row_index": 1,
                "evidence_id_hash": evidence_hash,
                "evidence_type": "comment",
                "platform": "public_sample",
                "created_at_date": "2026-06-01",
                "trust_label": "medium_low",
                "verification_status": "unverified",
                "review_status": "review_needed",
                "language": "zh",
                "content_visibility": "public",
                "access_scope": "selected_sample",
                "text_snippet_redacted": snippet,
                "redaction_status": "redacted",
                "redaction_warnings": [],
            }],
            "runtime_side_effects": {
                "opened_approved_evidence_items_jsonl": True,
                "parsed_evidence_items_jsonl": True,
                "parsed_evidence_items_csv": False,
                "parsed_source_manifest_jsonl_rows": False,
                "parsed_collection_log_jsonl_rows": False,
                "wrote_evidence_layer": False,
            },
        },
        "evidence_candidate_set": {
            "candidate_set_schema": STAGE_SCHEMAS["controlled_evidence_candidate"],
            "candidate_count": 1,
            "evidence_candidate_created": True,
            "human_review_required": True,
            "candidates": [{
                "candidate_schema": "sentigraph_controlled_evidence_candidate_v0_1",
                "candidate_id": evidence_candidate_id,
                "source_preview_row_id": preview_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
        "review_queue_candidate_set": {
            "review_queue_candidate_set_schema": STAGE_SCHEMAS["controlled_review_queue_candidate"],
            "review_queue_candidate_count": 1,
            "review_queue_candidate_created": True,
            "human_review_required": True,
            "review_queue_candidates": [{
                "review_queue_candidate_schema": "sentigraph_controlled_review_queue_candidate_v0_1",
                "review_queue_candidate_id": review_candidate_id,
                "source_evidence_candidate_id": evidence_candidate_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
        "import_candidate_set": {
            "evidence_layer_import_candidate_set_schema": STAGE_SCHEMAS["controlled_evidence_layer_import_candidate"],
            "evidence_layer_import_candidate_count": 1,
            "evidence_layer_import_candidate_created": True,
            "human_review_required": True,
            "evidence_layer_import_candidates": [{
                "evidence_layer_import_candidate_schema": "sentigraph_controlled_evidence_layer_import_candidate_v0_1",
                "evidence_layer_import_candidate_id": import_candidate_id,
                "source_review_queue_candidate_id": review_candidate_id,
                "source_evidence_candidate_id": evidence_candidate_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
        "direct_write_candidate_set": {
            "evidence_layer_write_candidate_set_schema": STAGE_SCHEMAS["controlled_direct_write_candidate"],
            "evidence_layer_write_candidate_count": 1,
            "evidence_layer_write_candidate_created": True,
            "human_review_required": True,
            "evidence_layer_write_candidates": [{
                "evidence_layer_write_candidate_schema": "sentigraph_controlled_evidence_layer_write_candidate_v0_1",
                "evidence_layer_write_candidate_id": direct_write_id,
                "source_evidence_layer_import_candidate_id": import_candidate_id,
                "source_review_queue_candidate_id": review_candidate_id,
                "source_evidence_candidate_id": evidence_candidate_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
        "production_import_candidate_set": {
            "production_evidence_import_candidate_set_schema": STAGE_SCHEMAS["controlled_production_evidence_import_candidate"],
            "production_evidence_import_candidate_count": 1,
            "production_evidence_import_candidate_created": True,
            "human_review_required": True,
            "production_evidence_import_candidates": [{
                "production_evidence_import_candidate_schema": "sentigraph_controlled_production_evidence_import_candidate_v0_1",
                "production_evidence_import_candidate_id": production_import_id,
                "source_evidence_layer_write_candidate_id": direct_write_id,
                "source_evidence_layer_import_candidate_id": import_candidate_id,
                "source_review_queue_candidate_id": review_candidate_id,
                "source_evidence_candidate_id": evidence_candidate_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
        "derived_write_candidate_set": {
            "evidence_layer_write_candidate_set_schema": STAGE_SCHEMAS["production_import_derived_write_candidate"],
            "evidence_layer_write_candidate_count": 1,
            "evidence_layer_write_candidate_created": True,
            "human_review_required": True,
            "evidence_layer_write_candidates": [{
                "evidence_layer_write_candidate_schema": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1",
                "evidence_layer_write_candidate_id": final_candidate_id,
                "source_production_evidence_import_candidate_id": production_import_id,
                "source_evidence_layer_write_candidate_id": direct_write_id,
                "source_evidence_layer_import_candidate_id": import_candidate_id,
                "source_review_queue_candidate_id": review_candidate_id,
                "source_evidence_candidate_id": evidence_candidate_id,
                "evidence_id_hash": evidence_hash,
                "text_snippet_redacted": snippet,
                "human_review_required": True,
                "boundary_flags": dict(safe_boundary),
            }],
        },
    }


@pytest.fixture(scope="module")
def real_execution() -> dict[str, Any]:
    service = _service()
    row_preview_module = import_module("app.services.controlled_row_preview")
    approved_file = row_preview_module.APPROVED_ROW_FILE
    assert approved_file.name == APPROVED_ROW_SOURCE
    assert approved_file.is_file(), "exact approved evidence_items.jsonl must exist"

    opened: list[str] = []
    logs: list[logging.LogRecord] = []
    stdout = io.StringIO()
    stderr = io.StringIO()
    original_open = Path.open
    monkeypatch = pytest.MonkeyPatch()

    def guarded_open(path: Path, *args: object, **kwargs: object):
        assert path == approved_file
        assert path.name == APPROVED_ROW_SOURCE
        opened.append(path.name)
        return original_open(path, *args, **kwargs)

    def fail_enumeration(*args: object, **kwargs: object) -> None:
        raise AssertionError("9A-16 must not enumerate directories")

    class CaptureHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logs.append(record)

    handler = CaptureHandler()
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(Path, "iterdir", fail_enumeration)
    monkeypatch.setattr(Path, "glob", fail_enumeration)
    monkeypatch.setattr(Path, "rglob", fail_enumeration)
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            audit = service.review_one_real_exported_package_candidate_pre_write(
                exact_outer_approval_phrase=OUTER_APPROVAL_PHRASE,
                declaration_context=_safe_declaration_context(),
                rollback_plan=_safe_rollback_plan(),
            )
    finally:
        monkeypatch.undo()
        root_logger.removeHandler(handler)

    return {
        "audit": audit,
        "opened": opened,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "logs": [record.getMessage() for record in logs],
    }


def test_exact_outer_phrase_is_required_before_file_or_helper_access(monkeypatch: pytest.MonkeyPatch) -> None:
    service = _service()

    def fail_chain() -> None:
        raise AssertionError("chain called before exact outer approval")

    monkeypatch.setattr(service, "_build_controlled_candidate_chain", fail_chain)
    for phrase in [None, "", "wrong", *NEIGHBOR_OUTER_PHRASES]:
        with pytest.raises(ValueError, match="blocked_(missing|wrong)_exact_9a16_outer_approval"):
            _build(phrase=phrase)


@pytest.mark.parametrize(
    "inner_phrase",
    [None, "", OLD_CHINESE_ROW_PREVIEW_PHRASE, MOJIBAKE_ROW_PREVIEW_PHRASE, "APPROVE_WRONG_INNER"],
)
def test_inner_8w7_phrase_must_remain_canonical_ascii_before_file_access(
    inner_phrase: str | None, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    monkeypatch.setattr(service.row_preview_module, "APPROVAL_PHRASE", inner_phrase)
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    with pytest.raises(ValueError, match="blocked_inner_8w7_guard_mismatch"):
        _build()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("APPROVED_PACKAGE_NAME", "alternate-package"),
        ("APPROVED_PACKAGE_ROLE", "alternate-role"),
        ("APPROVED_CASE_ID_HINT", "alternate_case"),
        ("APPROVED_ROW_SOURCE", "evidence_items.csv"),
    ],
)
def test_exact_package_identity_and_row_source_lock_before_file_access(
    field: str, value: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    monkeypatch.setattr(service.row_preview_module, field, value)
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    with pytest.raises(ValueError, match="blocked_exact_approved_package_lock_mismatch"):
        _build()


def test_public_api_accepts_no_path_package_filename_url_glob_or_row_selector() -> None:
    parameters = inspect.signature(_service().review_one_real_exported_package_candidate_pre_write).parameters
    forbidden = {
        "path", "package_path", "export_root", "package_name", "package_role", "case_id_hint",
        "row_index", "filename", "row_source", "url", "glob", "directory", "selector",
    }
    assert not (set(parameters) & forbidden)


def test_real_integration_reads_only_one_approved_jsonl_row_and_is_not_skipped(real_execution: dict[str, Any]) -> None:
    audit = real_execution["audit"]
    assert real_execution["opened"] == [APPROVED_ROW_SOURCE]
    assert audit["audit_status"] == "one_real_candidate_review_complete_no_write"
    assert audit["approved_real_exported_package_selected"] is True
    assert audit["approved_evidence_items_jsonl_opened"] is True
    assert audit["approved_evidence_items_jsonl_rows_parsed"] == 1
    assert audit["real_exported_package_rows_reviewed_count"] == 1
    assert audit["preview_rows_count"] == 1
    assert audit["rows_inspected_count"] == 1
    assert audit["row_limit_enforced"] is True
    assert audit["real_integration_test_skipped"] is False
    assert audit["directory_enumeration_performed"] is False
    assert audit["arbitrary_path_accessed"] is False
    assert audit["evidence_items_csv_opened"] is False
    assert audit["source_manifest_rows_parsed"] is False
    assert audit["collection_log_rows_parsed"] is False
    assert audit["unapproved_package_rows_read"] is False
    assert audit["production_package_rows_parsed"] is False


def test_real_preview_and_summary_are_minimized_without_text_logs_or_paths(real_execution: dict[str, Any]) -> None:
    service = _service()
    audit = real_execution["audit"]
    summary = service.build_safe_one_real_candidate_pre_write_review_summary(audit)
    serialized = _serialized({"audit": audit, "summary": summary})

    assert audit["preview_text_inspected_in_memory"] is True
    assert audit["preview_text_persisted"] is False
    assert audit["preview_text_written_to_health_report"] is False
    assert audit["preview_text_logged"] is False
    assert audit["raw_author_identity_exposed"] is False
    assert audit["secret_value_exposed"] is False
    assert audit["redaction_status"] == "redacted"
    assert real_execution["stdout"] == ""
    assert real_execution["stderr"] == ""
    assert real_execution["logs"] == []
    forbidden_keys = {
        "text_snippet_redacted", "body_text", "comment_text", "title_text", "raw_author_id",
        "raw_author_name", "profile_url", "private_message", "source_url", "full_row_json",
        "package_path", "absolute_path",
    }
    assert not (_json_keys({"audit": audit, "summary": summary}) & forbidden_keys)
    assert ":/" not in serialized
    assert ":\\" not in serialized


def test_real_controlled_candidate_chain_has_exact_schemas_and_one_candidate(real_execution: dict[str, Any]) -> None:
    audit = real_execution["audit"]
    assert audit["audit_schema"] == AUDIT_SCHEMA
    assert audit["audit_mode"] == AUDIT_MODE
    assert audit["row_preview_schema"] == STAGE_SCHEMAS["controlled_row_preview"]
    assert audit["stage_schemas"] == STAGE_SCHEMAS
    assert audit["one_real_exported_package_selected"] is True
    assert audit["one_bounded_real_row_reviewed"] is True
    assert audit["one_real_source_candidate_created"] is True
    assert audit["one_real_source_candidate_review_complete"] is True
    assert audit["final_candidate_schema"] == STAGE_SCHEMAS["production_import_derived_write_candidate"]
    assert audit["candidate_specific_blockers_clear"] is True


def test_real_lineage_is_complete_ordered_and_continuous(real_execution: dict[str, Any]) -> None:
    lineage = real_execution["audit"]["lineage_review"]
    assert lineage["status"] == "reviewed"
    assert lineage["stage_count"] == len(EXPECTED_LINEAGE_STAGES)
    assert lineage["stages"] == EXPECTED_LINEAGE_STAGES
    assert lineage["lineage_gap_detected"] is False
    assert lineage["package_identity_match"] is True
    assert lineage["case_id_hint_match"] is True
    assert lineage["candidate_reference_continuity"] is True
    assert lineage["arbitrary_source_substitution"] is False
    assert lineage["alternate_package_used"] is False
    assert lineage["alternate_row_source_used"] is False


def test_all_required_real_candidate_risks_are_classified_conservatively(real_execution: dict[str, Any]) -> None:
    risk_review = real_execution["audit"]["risk_review"]
    assert risk_review["status"] == "reviewed"
    assert set(risk_review["classifications"]) == RISK_CATEGORIES
    assert set(risk_review["classifications"].values()) <= ALLOWED_RISK_LABELS
    assert real_execution["audit"]["candidate_specific_risks_classified"] is True


def test_human_declaration_context_remains_non_authorizing(real_execution: dict[str, Any]) -> None:
    audit = real_execution["audit"]
    review = audit["human_declaration_context_review"]
    assert review["preserved_context"] == _safe_declaration_context()
    assert review["status"] == "reviewed_non_authorizing"
    assert audit["human_authority_validated"] is False
    assert audit["manual_review_responsibility_accepted"] is False
    assert audit["runtime_human_authority_validation_performed"] is False
    assert audit["runtime_manual_review_responsibility_acceptance_performed"] is False
    assert audit["final_write_authorization_performed"] is False


def test_success_remains_paused_non_production_and_non_authorizing(real_execution: dict[str, Any]) -> None:
    audit = real_execution["audit"]
    assert audit["authorization_blockers_remaining"] is True
    assert audit["final_write_authorization_still_required"] is True
    assert audit["overall_write_disposition"] == "pause"
    assert audit["ready_for_actual_write"] is False
    assert audit["real_production_candidate_selected"] is False
    assert audit["real_production_candidate_reviewed"] is False
    assert audit["production_evidenceitem_created"] is False
    for flag in FALSE_FLAGS:
        assert audit[flag] is False, flag


@pytest.mark.parametrize(
    ("overrides", "expected_status"),
    [
        ({"pause_on_any_blocker": False}, "one_real_candidate_review_blocked_no_write"),
        ({"revocation_target_kind": "production_record"}, "one_real_candidate_review_blocked_no_write"),
        ({"revocation_target_ref": "arbitrary-target"}, "one_real_candidate_review_blocked_no_write"),
        ({"rollback_action": "persist_then_delete"}, "one_real_candidate_review_blocked_no_write"),
        ({"persistence_rollback_required": True}, "one_real_candidate_review_blocked_no_write"),
        ({"no_persistence": False}, "one_real_candidate_review_blocked_no_write"),
        ({"final_write_authorization_still_required": False}, "one_real_candidate_review_blocked_no_write"),
    ],
)
def test_invalid_rollback_plan_blocks_before_chain(
    overrides: dict[str, object], expected_status: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    audit = _build(rollback_plan=_safe_rollback_plan(**overrides))
    assert audit["audit_status"] == expected_status
    assert audit["rollback_pause_revocation_review"]["status"] == "blocked"


def test_missing_rollback_plan_blocks_before_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    service = _service()
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    audit = service.review_one_real_exported_package_candidate_pre_write(
        exact_outer_approval_phrase=OUTER_APPROVAL_PHRASE,
        declaration_context=_safe_declaration_context(),
        rollback_plan=None,
    )
    assert audit["audit_status"] == "one_real_candidate_review_blocked_no_write"
    assert "rollback_pause_revocation_plan_invalid" in audit["blockers"]


@pytest.mark.parametrize(
    "acknowledgment",
    [
        "warning_count_acknowledgment_present",
        "human_review_required_acknowledgment_present",
        "no_automatic_trust_upgrade_acknowledgment_present",
    ],
)
def test_required_acknowledgments_block_before_chain_when_missing(
    acknowledgment: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    audit = _build(declaration_context=_safe_declaration_context(**{acknowledgment: False}))
    assert audit["audit_status"] == "one_real_candidate_review_blocked_no_write"
    assert "human_declaration_context_invalid" in audit["blockers"]


@pytest.mark.parametrize("flag", FALSE_FLAGS)
def test_unsafe_true_declaration_or_review_flags_block_before_chain(
    flag: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: pytest.fail("chain must not run"))
    audit = _build(declaration_context=_safe_declaration_context(**{flag: True}))
    assert audit["audit_status"] == "one_real_candidate_review_blocked_no_write"
    assert f"unsafe_true_flag:{flag}" in audit["blockers"]
    assert audit["ready_for_actual_write"] is False


@pytest.mark.parametrize(
    ("mutation", "expected_status"),
    [
        (lambda chain: chain["derived_write_candidate_set"].update(evidence_layer_write_candidate_set_schema="wrong"), "one_real_candidate_review_blocked_no_write"),
        (lambda chain: chain["derived_write_candidate_set"].update(evidence_layer_write_candidate_count=2), "one_real_candidate_review_blocked_no_write"),
        (lambda chain: chain["derived_write_candidate_set"]["evidence_layer_write_candidates"].append(deepcopy(chain["derived_write_candidate_set"]["evidence_layer_write_candidates"][0])), "one_real_candidate_review_blocked_no_write"),
        (lambda chain: chain["derived_write_candidate_set"]["evidence_layer_write_candidates"][0].update(source_production_evidence_import_candidate_id="substituted-ref"), "one_real_candidate_review_blocked_no_write"),
        (lambda chain: chain["row_preview"].update(approved_target_package_name="alternate-package"), "one_real_candidate_review_blocked_no_write"),
        (lambda chain: chain["row_preview"].update(row_source="evidence_items.csv"), "one_real_candidate_review_blocked_no_write"),
    ],
)
def test_schema_count_lineage_or_package_substitution_blocks(
    mutation, expected_status: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    chain = _safe_synthetic_chain()
    mutation(chain)
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: chain)
    audit = _build()
    assert audit["audit_status"] == expected_status
    assert audit["candidate_specific_blockers_clear"] is False


@pytest.mark.parametrize(
    ("unsafe_key", "unsafe_value"),
    [
        ("raw_author_id", "forbidden-test-value"),
        ("raw_author_name", "forbidden-test-value"),
        ("profile_url", "https://example.invalid/profile"),
        ("private_message", "forbidden-test-value"),
        ("token", "forbidden-test-value"),
        ("cookie", "forbidden-test-value"),
        ("session", "forbidden-test-value"),
        ("secret", "forbidden-test-value"),
        ("full_row_json", {"body": "forbidden-test-value"}),
        ("response_text", "forbidden-test-value"),
        ("target_user_list", ["forbidden-test-value"]),
        ("truth_score", 1.0),
        ("official_verified", True),
        ("psychological_profile", "forbidden-test-value"),
    ],
)
def test_recursive_privacy_secret_scan_blocks_without_echo(
    unsafe_key: str, unsafe_value: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    service = _service()
    chain = _safe_synthetic_chain()
    chain["derived_write_candidate_set"]["unsafe_nested"] = {unsafe_key: unsafe_value}
    monkeypatch.setattr(service, "_build_controlled_candidate_chain", lambda: chain)
    audit = _build()
    serialized = _serialized(audit)
    assert audit["audit_status"] == "privacy_issue_stop"
    assert audit["privacy_issue_stop"] is True
    assert "privacy_or_forbidden_value_detected" in audit["blockers"]
    assert "forbidden-test-value" not in serialized
    assert "example.invalid" not in serialized


def test_service_uses_only_allowed_helpers_and_never_imports_write_runtime() -> None:
    source = inspect.getsource(_service()).lower()
    import_lines = "\n".join(
        line.strip() for line in source.splitlines()
        if line.strip().startswith("import ") or line.strip().startswith("from ")
    )
    for forbidden in [
        "controlled_evidenceitem_evidence_layer_write_runtime",
        "app.services.evidence_import ",
        "app.services.evidence_ingestion ",
        "analysis_request_store",
        "controlled_production_case",
        "controlled_production_analysis_run",
        "production_analysis_result",
        "source11",
        "finalsummaryreport",
    ]:
        assert forbidden not in import_lines
    assert "print(" not in source
    assert "logging." not in source


def test_safe_summary_contains_no_candidate_payload_or_preview_text(real_execution: dict[str, Any]) -> None:
    summary = _service().build_safe_one_real_candidate_pre_write_review_summary(real_execution["audit"])
    serialized = _serialized(summary)
    assert summary["audit_schema"] == AUDIT_SCHEMA
    assert summary["overall_write_disposition"] == "pause"
    assert summary["authorization_blockers_remaining"] is True
    assert summary["ready_for_actual_write"] is False
    forbidden_keys = {
        "text_snippet_redacted", "preview_rows", "candidates", "body_text", "comment_text", "source_url"
    }
    assert not (_json_keys(summary) & forbidden_keys)
