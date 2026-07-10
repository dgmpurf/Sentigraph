from __future__ import annotations

import inspect
import io
import json
import logging
import os
import re
from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest


OUTER_APPROVAL_PHRASE = (
    "APPROVE_9A_16B_ONE_APPROVED_ROW_IDENTITY_COMPLETE_LOCKED_CANDIDATE_REVIEW_"
    "AND_CONDITIONAL_9A_17_COMPLETION_NO_WRITE"
)
APPROVED_PACKAGE_NAME = "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
APPROVED_PACKAGE_ROLE = "candidate_demo_sample"
APPROVED_CASE_ID_HINT = "donglu_sunjihai_youth_football_202606"
APPROVED_ROW_SOURCE = "evidence_items.jsonl"

IDENTITY_SCHEMA = "sentigraph_one_real_source_locked_candidate_identity_v0_1"
AUDIT_SCHEMA = "sentigraph_one_real_source_locked_candidate_pre_write_review_audit_v0_1"
FINAL_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)
HASH_SCOPE = "versioned_safe_canonical_projection_only"
LOCK_STATUS = "locked_for_single_candidate_governance_review_only"
REAL_CAPTURE_ENV = "SENTIGRAPH_RUN_9A16C_REAL_IDENTITY_CAPTURE"

FALSE_FLAGS = [
    "actual_write_authorized",
    "actual_evidence_layer_write_approved",
    "actual_evidence_layer_write_performed",
    "persisted_evidence_layer_record_created",
    "production_evidenceitem_creation_authorized",
    "production_evidenceitem_created",
    "write_helper_execution_allowed",
    "evidenceitem_write_runtime_called",
    "human_authority_validated",
    "runtime_human_authority_validation_performed",
    "manual_review_responsibility_accepted_as_runtime_or_audit_state",
    "runtime_manual_review_responsibility_acceptance_performed",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "review_queue_runtime_used",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
]

EXPECTED_RISK_CATEGORIES = {
    "wrong_package_selection_risk",
    "excessive_row_read_risk",
    "raw_content_retention_risk",
    "raw_identity_privacy_risk",
    "secret_exposure_risk",
    "identity_binding_mismatch_risk",
    "lineage_mismatch_risk",
    "irreversible_write_risk",
    "authorization_confusion_risk",
    "trust_inflation_risk",
    "provider_output_mistaken_as_truth_risk",
    "duplicate_amplification_risk",
    "weak_rejected_evidence_inclusion_risk",
    "route_api_frontend_exposure_risk",
    "downstream_production_escalation_risk",
    "source11_finalsummaryreport_escalation_risk",
    "public_customer_readiness_overclaim_risk",
}


def _service():
    return import_module("app.services.evidence_layer_one_real_locked_candidate_pre_write_review")


def _legacy_service():
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
        "runtime_human_authority_validation_performed": False,
        "manual_review_responsibility_accepted": False,
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
        "revocation_target_kind": "one_real_source_locked_candidate",
        "revocation_target_ref": "bind_locked_final_candidate",
        "rollback_action": "discard_in_memory_preview_candidates_identity_and_audit",
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
    return _service().review_one_approved_row_as_locked_candidate(
        exact_outer_approval_phrase=phrase,
        declaration_context=declaration_context or _safe_declaration_context(),
        rollback_plan=rollback_plan or _safe_rollback_plan(),
    )


def _safe_legacy_audit(**overrides: object) -> dict[str, Any]:
    audit: dict[str, Any] = {
        "audit_schema": "sentigraph_one_real_exported_package_candidate_pre_write_review_audit_v0_1",
        "audit_status": "one_real_candidate_review_complete_no_write",
        "approved_package_name": APPROVED_PACKAGE_NAME,
        "approved_package_role": APPROVED_PACKAGE_ROLE,
        "approved_case_id_hint": APPROVED_CASE_ID_HINT,
        "approved_row_source": APPROVED_ROW_SOURCE,
        "approved_real_exported_package_selected": True,
        "approved_evidence_items_jsonl_opened": True,
        "approved_evidence_items_jsonl_rows_parsed": 1,
        "real_exported_package_rows_reviewed_count": 1,
        "preview_rows_count": 1,
        "rows_inspected_count": 1,
        "row_limit_enforced": True,
        "selected_preview_row_id": "preview-row-001",
        "selected_row_safe_hash": "a1b2c3d4e5f60718",
        "final_candidate_id": "evidence-layer-write-candidate-from-production-import-001-a1b2c3d4e5f60718",
        "final_candidate_schema": FINAL_CANDIDATE_SCHEMA,
        "row_preview_schema": "sentigraph_controlled_row_preview_v0_1",
        "stage_schemas": {
            "controlled_row_preview": "sentigraph_controlled_row_preview_v0_1",
            "controlled_evidence_candidate": "sentigraph_controlled_evidence_candidate_set_v0_1",
            "controlled_review_queue_candidate": "sentigraph_controlled_review_queue_candidate_set_v0_1",
            "controlled_evidence_layer_import_candidate": "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
            "controlled_direct_write_candidate": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
            "controlled_production_evidence_import_candidate": "sentigraph_controlled_production_evidence_import_candidate_set_v0_1",
            "production_import_derived_write_candidate": FINAL_CANDIDATE_SCHEMA,
        },
        "evidence_type": "comment",
        "platform": "selected_public_sample",
        "created_at_date": "2026-06-17",
        "trust_label": "selected_sample_unverified",
        "verification_status": "not_officially_verified",
        "review_status": "review_only",
        "language": "zh",
        "content_visibility": "public_sample",
        "access_scope": "selected_sample_only",
        "redaction_status": "redacted",
        "lineage_review": {
            "status": "reviewed",
            "stage_count": 10,
            "stages": [
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
            ],
            "lineage_gap_detected": False,
            "candidate_reference_continuity": True,
            "arbitrary_source_substitution": False,
        },
        "human_declaration_context_review": {
            "status": "reviewed_non_authorizing",
            "declaration_structurally_present": True,
            "authority_independently_validated": False,
            "responsibility_runtime_accepted": False,
            "final_write_authorization_present": False,
        },
        "one_real_exported_package_selected": True,
        "one_bounded_real_row_reviewed": True,
        "one_real_source_candidate_created": True,
        "one_real_source_candidate_review_complete": True,
        "candidate_specific_blockers_clear": True,
        "candidate_specific_risks_classified": True,
        "candidate_specific_lineage_verified": True,
        "candidate_specific_privacy_review_complete": True,
        "candidate_specific_rollback_plan_verified": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "authorization_blockers_remaining": True,
        "final_write_authorization_still_required": True,
        "overall_write_disposition": "pause",
        "privacy_issue_stop": False,
        "blockers": [],
        "warnings": ["manual_review_required", "selected_sample_only"],
        **{flag: False for flag in FALSE_FLAGS},
    }
    audit.update(overrides)
    return audit


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


def _execute_real_locked_identity_capture() -> dict[str, Any]:
    service = _service()
    row_preview_module = import_module("app.services.controlled_row_preview")
    approved_file = row_preview_module.APPROVED_ROW_FILE
    assert approved_file.name == APPROVED_ROW_SOURCE
    assert approved_file.is_file(), "the exact approved evidence_items.jsonl must exist"

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
        assert len(opened) == 1, "9A-16C may open the approved row source exactly once"
        return original_open(path, *args, **kwargs)

    def fail_file_read(*args: object, **kwargs: object) -> None:
        raise AssertionError("9A-16C must use only the single approved Path.open call")

    def fail_enumeration(*args: object, **kwargs: object) -> None:
        raise AssertionError("9A-16C must not enumerate directories")

    class CaptureHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logs.append(record)

    handler = CaptureHandler()
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    monkeypatch.setattr(Path, "open", guarded_open)
    monkeypatch.setattr(Path, "read_text", fail_file_read)
    monkeypatch.setattr(Path, "read_bytes", fail_file_read)
    monkeypatch.setattr(Path, "iterdir", fail_enumeration)
    monkeypatch.setattr(Path, "glob", fail_enumeration)
    monkeypatch.setattr(Path, "rglob", fail_enumeration)
    monkeypatch.setattr(os, "listdir", fail_enumeration)
    monkeypatch.setattr(os, "scandir", fail_enumeration)
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            audit = _build()
            marker = service.build_safe_locked_candidate_identity_capture_marker(audit)
    finally:
        monkeypatch.undo()
        root_logger.removeHandler(handler)

    return {
        "audit": audit,
        "opened": opened,
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "logs": [record.getMessage() for record in logs],
        "marker": marker,
    }


def test_exact_9a16b_outer_phrase_is_required_before_legacy_call(monkeypatch: pytest.MonkeyPatch) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: pytest.fail("legacy review must not run before exact 9A-16B approval"),
    )
    wrong_phrases = [
        None,
        "",
        "wrong",
        legacy.OUTER_APPROVAL_PHRASE,
        "APPROVE_9A_16A_SAFE_LOCKED_CANDIDATE_IDENTITY_BINDING_REPAIR_AND_9A_17_DECISION_COMPLETION_NO_PACKAGE_OR_ROW_REREAD_NO_WRITE",
    ]
    for phrase in wrong_phrases:
        with pytest.raises(ValueError, match="blocked_(missing|wrong)_exact_9a16b_outer_approval"):
            _build(phrase=phrase)


def test_public_api_accepts_no_path_package_filename_url_glob_or_selector() -> None:
    parameters = inspect.signature(_service().review_one_approved_row_as_locked_candidate).parameters
    forbidden = {
        "path",
        "package_path",
        "export_root",
        "package_name",
        "row_index",
        "filename",
        "row_source",
        "url",
        "glob",
        "directory",
        "selector",
    }
    assert not (set(parameters) & forbidden)


@pytest.mark.parametrize(
    ("context_overrides", "rollback_overrides", "expected_blocker"),
    [
        ({"human_authority_validated": True}, {}, "human_declaration_context_invalid"),
        ({"warning_count_acknowledgment_present": False}, {}, "human_declaration_context_invalid"),
        ({}, {"no_persistence": False}, "rollback_pause_revocation_plan_invalid"),
    ],
)
def test_invalid_preflight_blocks_without_opening_row(
    context_overrides: dict[str, object],
    rollback_overrides: dict[str, object],
    expected_blocker: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: pytest.fail("legacy review must not run for invalid preflight"),
    )
    audit = _build(
        declaration_context=_safe_declaration_context(**context_overrides),
        rollback_plan=_safe_rollback_plan(**rollback_overrides),
    )
    assert audit["audit_status"] == "locked_candidate_review_blocked_no_write"
    assert expected_blocker in audit["blockers"]
    assert audit["approved_file_open_count"] == 0


def test_safe_in_memory_legacy_audit_creates_reproducible_identity(monkeypatch: pytest.MonkeyPatch) -> None:
    legacy = _legacy_service()
    legacy_audit = _safe_legacy_audit()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: deepcopy(legacy_audit),
    )
    first = _build()
    second = _build()
    identity = first["locked_candidate_identity"]

    assert first["audit_status"] == "locked_candidate_review_complete_no_write"
    assert identity == second["locked_candidate_identity"]
    assert identity["identity_schema"] == IDENTITY_SCHEMA
    assert identity["selected_preview_row_opaque_id"] == legacy_audit["selected_preview_row_id"]
    assert identity["final_candidate_id"] == legacy_audit["final_candidate_id"]
    assert identity["selected_preview_row_safe_hash"] != legacy_audit["selected_row_safe_hash"]
    assert identity["hash_algorithm"] == "sha256"
    assert identity["hash_input_scope"] == HASH_SCOPE
    assert identity["candidate_lock_status"] == LOCK_STATUS
    assert re.fullmatch(r"[a-f0-9]{64}", identity["selected_preview_row_safe_hash"])
    assert re.fullmatch(r"[a-f0-9]{64}", identity["final_candidate_safe_hash"])
    assert identity["selected_preview_row_safe_hash"] != identity["final_candidate_safe_hash"]


def test_9a16c_identity_capture_marker_is_exact_minimized_single_line_and_no_io(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: _safe_legacy_audit(),
    )
    review = _build()
    service = _service()

    def fail_io(*args: object, **kwargs: object) -> None:
        raise AssertionError("identity marker helper must perform no file IO or enumeration")

    monkeypatch.setattr(Path, "open", fail_io)
    monkeypatch.setattr(Path, "read_text", fail_io)
    monkeypatch.setattr(Path, "read_bytes", fail_io)
    monkeypatch.setattr(Path, "iterdir", fail_io)
    monkeypatch.setattr(Path, "glob", fail_io)
    monkeypatch.setattr(Path, "rglob", fail_io)
    monkeypatch.setattr(os, "listdir", fail_io)
    monkeypatch.setattr(os, "scandir", fail_io)

    marker = service.build_safe_locked_candidate_identity_capture_marker(review)
    prefix = "SENTIGRAPH_9A16C_LOCKED_IDENTITY="
    assert marker.startswith(prefix)
    assert "\n" not in marker
    assert "\r" not in marker
    payload = json.loads(marker[len(prefix) :])
    assert set(payload) == {
        "selected_preview_row_opaque_id",
        "selected_preview_row_safe_hash",
        "final_candidate_id",
        "final_candidate_safe_hash",
    }
    assert payload == {
        key: review["locked_candidate_identity"][key]
        for key in payload
    }
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    for forbidden in [
        "row_text",
        "raw_author",
        "profile_url",
        "source_url",
        "package_path",
        "absolute_path",
        "token",
        "secret",
    ]:
        assert forbidden not in serialized


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("selected_preview_row_opaque_id", None),
        ("selected_preview_row_opaque_id", "../unsafe"),
        ("selected_preview_row_safe_hash", "short"),
        ("final_candidate_id", "https://invalid.example"),
        ("final_candidate_safe_hash", "A" * 64),
    ],
)
def test_9a16c_identity_capture_marker_rejects_missing_or_invalid_fields(
    field: str, value: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: _safe_legacy_audit(),
    )
    review = _build()
    review["locked_candidate_identity"][field] = value
    with pytest.raises(ValueError, match="blocked_invalid_9a16c_locked_identity_capture"):
        _service().build_safe_locked_candidate_identity_capture_marker(review)


@pytest.mark.parametrize(
    ("field", "value", "expected_blocker"),
    [
        ("selected_preview_row_id", "../unsafe", "locked_candidate_identity_invalid"),
        ("selected_preview_row_id", "https://invalid.example", "locked_candidate_identity_invalid"),
        ("final_candidate_id", "C:/unsafe", "locked_candidate_identity_invalid"),
        ("final_candidate_schema", "wrong-schema", "controlled_candidate_schema_mismatch"),
        ("preview_rows_count", 2, "one_package_one_file_one_row_accounting_invalid"),
        ("approved_evidence_items_jsonl_rows_parsed", 2, "one_package_one_file_one_row_accounting_invalid"),
        ("approved_package_role", "production", "approved_package_identity_mismatch"),
    ],
)
def test_identity_schema_scope_and_one_row_invariants_block_before_lock(
    field: str, value: object, expected_blocker: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: _safe_legacy_audit(**{field: value}),
    )
    audit = _build()
    assert audit["audit_status"] == "locked_candidate_review_blocked_no_write"
    assert expected_blocker in audit["blockers"]
    assert audit["locked_candidate_identity_complete"] is False


@pytest.mark.parametrize(
    ("unsafe_key", "unsafe_value"),
    [
        ("raw_author_id", "person-123"),
        ("profile_url", "https://invalid.example/profile"),
        ("private_message", "private"),
        ("token", "not-a-real-token"),
        ("package_path", "C:/unsafe/package"),
        ("body_text", "raw text"),
    ],
)
def test_recursive_privacy_scan_stops_without_echo(
    unsafe_key: str, unsafe_value: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    legacy = _legacy_service()
    monkeypatch.setattr(
        legacy,
        "review_one_real_exported_package_candidate_pre_write",
        lambda **kwargs: _safe_legacy_audit(unsafe_container={unsafe_key: unsafe_value}),
    )
    audit = _build()
    serialized = json.dumps(audit, ensure_ascii=False, sort_keys=True)
    assert audit["audit_status"] == "privacy_issue_stop"
    assert audit["privacy_issue_stop"] is True
    assert unsafe_key not in _json_keys(audit)
    assert f': "{unsafe_value}"' not in serialized
    assert audit["locked_candidate_identity_complete"] is False


def test_9a_16c_real_locked_candidate_identity_capture_once() -> None:
    if os.environ.get(REAL_CAPTURE_ENV) != "1":
        pytest.skip(f"set {REAL_CAPTURE_ENV}=1 only for the separately approved one-time capture")

    execution = _execute_real_locked_identity_capture()
    audit = execution["audit"]
    identity = audit["locked_candidate_identity"]
    service = _service()

    assert execution["opened"] == [APPROVED_ROW_SOURCE]
    assert audit["approved_package_selected"] is True
    assert audit["approved_evidence_items_jsonl_opened"] is True
    assert audit["approved_file_open_count"] == 1
    assert audit["logical_rows_inspected"] == 1
    assert audit["logical_rows_parsed"] == 1
    assert audit["preview_rows_created"] == 1
    assert audit["row_limit_enforced"] is True
    assert audit["evidence_items_csv_opened"] is False
    assert audit["source_manifest_rows_parsed"] == 0
    assert audit["collection_log_rows_parsed"] == 0
    assert audit["directory_enumeration_performed"] is False
    assert audit["private_collector_inspected"] is False
    assert execution["stdout"] == ""
    assert execution["stderr"] == ""
    assert execution["logs"] == []
    assert audit["audit_schema"] == AUDIT_SCHEMA
    assert audit["audit_status"] == "locked_candidate_review_complete_no_write"
    assert audit["new_9a16b_locked_candidate_created"] is True
    assert audit["old_9a16_ephemeral_candidate_recovered"] is False
    assert audit["locked_candidate_identity_complete"] is True
    assert identity["identity_schema"] == IDENTITY_SCHEMA
    assert identity["final_candidate_schema"] == FINAL_CANDIDATE_SCHEMA
    assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,159}", identity["selected_preview_row_opaque_id"])
    assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,159}", identity["final_candidate_id"])
    assert re.fullmatch(r"[a-f0-9]{64}", identity["selected_preview_row_safe_hash"])
    assert re.fullmatch(r"[a-f0-9]{64}", identity["final_candidate_safe_hash"])
    assert "/" not in identity["selected_preview_row_opaque_id"]
    assert "\\" not in identity["selected_preview_row_opaque_id"]
    assert "/" not in identity["final_candidate_id"]
    assert "\\" not in identity["final_candidate_id"]
    assert audit["whole_package_approved"] is False
    assert audit["other_rows_approved"] is False
    assert audit["candidate_substitution_allowed"] is False
    assert audit["package_substitution_allowed"] is False
    assert audit["row_substitution_allowed"] is False
    assert audit["candidate_specific_blockers_clear"] is True
    assert audit["candidate_specific_risks_classified"] is True
    assert set(audit["risk_review"]["classifications"]) == EXPECTED_RISK_CATEGORIES
    assert audit["candidate_specific_lineage_verified"] is True
    assert audit["lineage_review"]["lineage_gap_detected"] is False
    assert audit["lineage_review"]["candidate_reference_continuity"] is True
    assert "locked_candidate_identity_projection" in audit["lineage_review"]["stages"]
    assert audit["candidate_specific_privacy_review_complete"] is True
    assert audit["raw_private_secret_review"]["privacy_or_forbidden_value_found"] is False
    assert audit["candidate_specific_rollback_plan_verified"] is True
    rollback = audit["rollback_pause_revocation_review"]
    assert rollback["revocation_target_ref"] == audit["final_candidate_id"]
    assert rollback["persistence_rollback_required"] is False
    assert rollback["no_persistence"] is True
    assert rollback["final_write_authorization_still_required"] is True
    context = audit["human_declaration_context_review"]
    assert context["declared_authority_role_label"] == "self_declared_project_owner_role"
    assert context["authority_basis_label"] == "authority_basis_not_independently_validated"
    assert context["manual_review_responsibility_statement_present"] is True
    assert context["warning_count_acknowledgment_present"] is True
    assert context["human_review_required_acknowledgment_present"] is True
    assert context["no_automatic_trust_upgrade_acknowledgment_present"] is True
    for flag in FALSE_FLAGS:
        assert audit[flag] is False, flag
    assert audit["authorization_blockers_remaining"] is True
    assert audit["final_write_authorization_still_required"] is True
    assert audit["overall_write_disposition"] == "pause"
    summary = service.build_safe_locked_candidate_pre_write_review_summary(audit)
    safe_identity = service.build_safe_locked_candidate_identity(audit)
    assert safe_identity == identity
    assert summary["locked_candidate_identity"] == identity
    assert summary["selected_preview_row_opaque_id"] == identity["selected_preview_row_opaque_id"]
    assert summary["final_candidate_safe_hash"] == identity["final_candidate_safe_hash"]
    forbidden_keys = {
        "text_snippet_redacted",
        "preview_rows",
        "candidates",
        "body_text",
        "comment_text",
        "raw_author_id",
        "raw_author_name",
        "profile_url",
        "source_url",
        "package_path",
        "absolute_path",
        "full_row_json",
    }
    assert not (_json_keys(summary) & forbidden_keys)
    serialized = json.dumps(summary, ensure_ascii=False, sort_keys=True)
    assert ":/" not in serialized
    assert ":\\" not in serialized
    assert execution["marker"] == service.build_safe_locked_candidate_identity_capture_marker(audit)
    print(execution["marker"])


def test_service_has_no_write_production_or_delivery_imports() -> None:
    source = inspect.getsource(_service())
    import_lines = "\n".join(line for line in source.splitlines() if line.startswith(("import ", "from ")))
    for forbidden in [
        "controlled_evidenceitem_evidence_layer_write_runtime",
        "evidence_import",
        "evidence_ingestion",
        "review_queue_runtime",
        "production_case",
        "production_analysis_run",
        "production_analysis_result",
        "source11",
        "finalsummaryreport",
    ]:
        assert forbidden not in import_lines
    assert "print(" not in source
    assert "logging." not in source
