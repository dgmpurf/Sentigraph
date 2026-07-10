from __future__ import annotations

import re
from typing import Any


APPROVAL_PHRASE = "APPROVE_9A_15_CONTROLLED_CANDIDATE_SPECIFIC_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_PRE_WRITE_REVIEW_AUDIT_NO_WRITE"
AUDIT_SCHEMA = "sentigraph_controlled_candidate_specific_evidence_layer_pre_write_review_audit_v0_1"
AUDIT_MODE = "backend_only_local_candidate_specific_pre_write_review_no_write"
DIRECT_WRITE_CANDIDATE_SCHEMA = "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1"
PRODUCTION_IMPORT_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_production_evidence_import_candidate_set_v0_1"
)
SELECTED_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)
CANDIDATE_ORIGIN = "controlled_8y13c_equivalent_in_memory_fixture"

LINEAGE_SPEC = [
    ("direct_write_candidate", DIRECT_WRITE_CANDIDATE_SCHEMA),
    ("controlled_production_evidence_import_candidate", PRODUCTION_IMPORT_CANDIDATE_SCHEMA),
    ("production_import_derived_write_candidate", SELECTED_CANDIDATE_SCHEMA),
]

FALSE_SAFETY_FLAGS = [
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
    "provider_called",
    "collector_called",
    "private_collector_inspected",
    "real_exchange_dir_read",
    "production_package_rows_parsed",
]

FORBIDDEN_RECURSIVE_KEYS = {
    "raw_row",
    "raw_rows",
    "raw_comment",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "profile_url",
    "profile_urls",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "password",
    "passwords",
    "secret",
    "secrets",
    "token",
    "tokens",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "salt",
    "salts",
    ".env",
    "env_value",
    "absolute_path",
    "filesystem_path",
    "package_path",
    "production_package_rows",
    "evidence_items_jsonl_contents",
    "evidence_items_csv_contents",
    "source_manifest_row_contents",
    "collection_log_row_contents",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "real_person_pii",
}

RISK_CLASSIFICATIONS = {
    "production_data_integrity_risk": "not_applicable_to_no_write_fixture",
    "privacy_raw_identity_risk": "mitigated_for_controlled_fixture",
    "irreversible_write_risk": "not_applicable_to_no_write_fixture",
    "authorization_confusion_risk": "mitigated_for_controlled_fixture",
    "trust_inflation_risk": "mitigated_for_controlled_fixture",
    "provider_vendor_output_mistaken_as_truth_risk": "open",
    "duplicate_amplification_risk": "unknown",
    "weak_rejected_evidence_inclusion_risk": "unknown",
    "route_api_frontend_accidental_write_exposure_risk": "not_applicable_to_no_write_fixture",
    "downstream_production_escalation_risk": "not_applicable_to_no_write_fixture",
    "source11_finalsummaryreport_escalation_risk": "not_applicable_to_no_write_fixture",
    "public_customer_readiness_overclaim_risk": "mitigated_for_controlled_fixture",
}

DECLARATION_REQUIRED_VALUES = {
    "declaration_source_kind": "explicit_human_message_later",
    "recognition_outcome": "declaration_present_for_docs_only_review",
    "declared_authority_role_label": "self_declared_project_owner_role",
    "authority_basis_label": "authority_basis_not_independently_validated",
    "manual_review_responsibility_statement_present": True,
    "warning_count_acknowledgment_present": True,
    "human_review_required_acknowledgment_present": True,
    "no_automatic_trust_upgrade_acknowledgment_present": True,
    "blocker_review_status_before_9a15": "not_reviewed_yet",
    "risk_review_status_before_9a15": "not_reviewed_yet",
    "lineage_review_status_before_9a15": "not_reviewed_yet",
    "raw_private_secret_absence_acknowledgment_before_9a15": "not_reviewed_yet",
    "rollback_pause_revocation_responsibility_label": "self_declared_project_owner_role",
    "human_authority_validated": False,
    "manual_review_responsibility_accepted": False,
    "final_write_authorization_performed": False,
    "actual_write_authorized": False,
    "production_evidenceitem_creation_authorized": False,
    "ready_for_actual_write": False,
}

SAFE_ROLLBACK_VALUES = {
    "pause_on_any_blocker": True,
    "revocation_target_kind": "controlled_candidate_fixture",
    "rollback_action": "discard_in_memory_candidate_and_audit",
    "persistence_rollback_required": False,
    "no_persistence": True,
    "final_write_authorization_still_required": True,
}

_OPAQUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
_URL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_WINDOWS_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_PHONE_RE = re.compile(r"^\+?\d[\d ()-]{7,}\d$")
_SECRET_VALUE_RE = re.compile(r"^(?:sk-[A-Za-z0-9]|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----)")


def audit_candidate_specific_pre_write_review(
    controlled_candidate_fixture: dict[str, Any] | None,
    *,
    declaration_context: dict[str, Any] | None,
    rollback_plan: dict[str, Any] | None,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    """Audit one controlled candidate fixture without reading, writing, or persisting data."""

    _require_exact_approval(exact_approval_phrase)

    candidate_fixture = controlled_candidate_fixture if isinstance(controlled_candidate_fixture, dict) else {}
    safe_declaration = declaration_context if isinstance(declaration_context, dict) else {}
    safe_rollback_plan = rollback_plan if isinstance(rollback_plan, dict) else {}

    privacy_issue = _contains_forbidden_or_sensitive_data(
        [candidate_fixture, safe_declaration, safe_rollback_plan]
    )
    candidates = candidate_fixture.get("candidates")
    candidate_rows = candidates if isinstance(candidates, list) else []
    selected_candidate = candidate_rows[0] if len(candidate_rows) == 1 and isinstance(candidate_rows[0], dict) else {}
    candidate_id = selected_candidate.get("candidate_id")
    safe_candidate_id = candidate_id if _is_safe_opaque_id(candidate_id) else None

    structural_blockers, blocker_checks = _candidate_blockers(candidate_fixture, candidate_rows, selected_candidate)
    unsafe_true_flags = _unsafe_true_flags([candidate_fixture, safe_declaration, safe_rollback_plan])
    structural_blockers.extend(f"unsafe_true_flag:{flag}" for flag in unsafe_true_flags)

    lineage_review, lineage_blockers = _review_lineage(selected_candidate)
    structural_blockers.extend(lineage_blockers)

    declaration_review, declaration_blockers = _review_declaration_context(safe_declaration)
    structural_blockers.extend(declaration_blockers)

    rollback_review, rollback_blockers = _review_rollback_plan(safe_rollback_plan, safe_candidate_id)
    structural_blockers.extend(rollback_blockers)

    blockers = _deduplicate(structural_blockers)
    if privacy_issue:
        blockers = _deduplicate(["privacy_or_forbidden_field_detected", *blockers])

    candidate_specific_review_complete = not privacy_issue and not blockers
    audit_status = (
        "privacy_issue_stop"
        if privacy_issue
        else "candidate_review_complete_no_write"
        if candidate_specific_review_complete
        else "candidate_review_blocked_no_write"
    )

    blocker_checks["no_unsafe_true_flags"] = not unsafe_true_flags
    blocker_checks["no_write_runtime_or_production_surface"] = not unsafe_true_flags
    blocker_checks["no_unresolved_candidate_specific_structural_blocker"] = not any(
        blocker
        for blocker in blockers
        if blocker not in {"declaration_context_invalid", "rollback_pause_revocation_plan_invalid"}
    )
    candidate_blocker_review_status = "reviewed" if candidate_specific_review_complete else "blocked"

    raw_private_secret_review = {
        "status": "blocked" if privacy_issue else "reviewed",
        "privacy_or_forbidden_field_found": privacy_issue,
        "secret_like_found": privacy_issue,
        "path_or_url_found": privacy_issue,
        "real_person_pii_found": privacy_issue,
        "unsafe_values_echoed": False,
    }

    audit = {
        "audit_schema": AUDIT_SCHEMA,
        "phase": "9A-15",
        "audit_mode": AUDIT_MODE,
        "audit_status": audit_status,
        "selected_candidate_count": len(candidate_rows),
        "selected_candidate_id": safe_candidate_id,
        "selected_candidate_schema": (
            selected_candidate.get("selected_candidate_schema")
            if isinstance(selected_candidate.get("selected_candidate_schema"), str)
            else None
        ),
        "selected_candidate_origin": (
            CANDIDATE_ORIGIN
            if selected_candidate.get("candidate_origin") == CANDIDATE_ORIGIN
            else None
        ),
        "candidate_blocker_review": {
            "status": candidate_blocker_review_status,
            "checks": blocker_checks,
            "candidate_specific_structural_blocker_count": len(structural_blockers),
        },
        "risk_review": {
            "status": "reviewed" if not privacy_issue else "blocked",
            "classifications": dict(RISK_CLASSIFICATIONS),
            "labels_are_fixture_scoped_only": True,
            "production_safety_claimed": False,
            "write_approval_claimed": False,
        },
        "lineage_review": lineage_review,
        "raw_private_secret_review": raw_private_secret_review,
        "rollback_pause_revocation_review": rollback_review,
        "human_declaration_context_review": declaration_review,
        "candidate_specific_review_complete": candidate_specific_review_complete,
        "candidate_specific_blockers_clear": candidate_specific_review_complete,
        "real_production_candidate_reviewed": False,
        "real_package_or_rows_reviewed": False,
        "authorization_blockers_remaining": True,
        "overall_write_disposition": "pause",
        "final_write_authorization_still_required": True,
        "warnings": ["manual_review_required"] if selected_candidate.get("warning_count") == 1 else [],
        "blockers": blockers,
        **{flag: False for flag in FALSE_SAFETY_FLAGS},
    }
    return audit


def build_candidate_specific_pre_write_review_summary(audit: dict[str, Any]) -> dict[str, Any]:
    """Return a compact boundary-only summary without candidate or lineage payloads."""

    return {
        "audit_schema": AUDIT_SCHEMA,
        "phase": "9A-15",
        "audit_mode": AUDIT_MODE,
        "audit_status": audit.get("audit_status", "paused"),
        "selected_candidate_count": audit.get("selected_candidate_count", 0),
        "candidate_specific_review_complete": audit.get("candidate_specific_review_complete") is True,
        "candidate_specific_blockers_clear": audit.get("candidate_specific_blockers_clear") is True,
        "real_production_candidate_reviewed": False,
        "real_package_or_rows_reviewed": False,
        "authorization_blockers_remaining": True,
        "overall_write_disposition": "pause",
        "final_write_authorization_still_required": True,
        "ready_for_actual_write": False,
        "actual_write_authorized": False,
        "production_evidenceitem_creation_authorized": False,
    }


def _require_exact_approval(exact_approval_phrase: str | None) -> None:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        raise ValueError("blocked_missing_exact_9a15_approval")
    if exact_approval_phrase != APPROVAL_PHRASE:
        raise ValueError("blocked_wrong_exact_9a15_approval")


def _candidate_blockers(
    fixture: dict[str, Any],
    candidate_rows: list[Any],
    candidate: dict[str, Any],
) -> tuple[list[str], dict[str, bool]]:
    blockers: list[str] = []
    checks = {
        "source_direct_write_candidate_schema_exact": (
            fixture.get("source_direct_write_candidate_schema") == DIRECT_WRITE_CANDIDATE_SCHEMA
        ),
        "production_import_candidate_schema_exact": (
            fixture.get("production_import_candidate_schema") == PRODUCTION_IMPORT_CANDIDATE_SCHEMA
        ),
        "selected_candidate_schema_exact": (
            fixture.get("selected_candidate_schema") == SELECTED_CANDIDATE_SCHEMA
            and candidate.get("selected_candidate_schema") == SELECTED_CANDIDATE_SCHEMA
        ),
        "exactly_one_candidate": len(candidate_rows) == 1 and bool(candidate),
        "candidate_id_is_safe_opaque_id": _is_safe_opaque_id(candidate.get("candidate_id")),
        "controlled_in_memory_origin": (
            fixture.get("candidate_origin") == CANDIDATE_ORIGIN
            and candidate.get("candidate_origin") == CANDIDATE_ORIGIN
        ),
        "not_real_production_candidate": candidate.get("real_production_candidate") is False,
        "no_real_package_rows_used": candidate.get("real_package_rows_used") is False,
        "human_review_required": candidate.get("human_review_required") is True,
        "no_automatic_trust_upgrade": candidate.get("no_automatic_trust_upgrade") is True,
        "warning_count_is_one": candidate.get("warning_count") == 1,
        "manual_review_required_warning_present": _has_manual_review_warning(candidate),
        "warning_acknowledgment_present": candidate.get("warning_acknowledgment_present") is True,
        "boundary_flags_complete_and_false": _boundary_flags_complete_and_false(candidate),
    }

    blocker_by_check = {
        "source_direct_write_candidate_schema_exact": "source_direct_write_candidate_schema_wrong",
        "production_import_candidate_schema_exact": "production_import_candidate_schema_wrong",
        "selected_candidate_schema_exact": "selected_candidate_schema_wrong",
        "exactly_one_candidate": "candidate_count_not_exactly_one",
        "candidate_id_is_safe_opaque_id": "candidate_id_not_safe_opaque_id",
        "controlled_in_memory_origin": "candidate_origin_not_controlled_in_memory_fixture",
        "not_real_production_candidate": "real_production_candidate_not_allowed",
        "no_real_package_rows_used": "real_package_rows_not_allowed",
        "human_review_required": "human_review_required_not_true",
        "no_automatic_trust_upgrade": "no_automatic_trust_upgrade_not_true",
        "warning_count_is_one": "warning_count_not_one",
        "manual_review_required_warning_present": "manual_review_required_warning_missing",
        "warning_acknowledgment_present": "warning_acknowledgment_missing",
        "boundary_flags_complete_and_false": "boundary_flags_missing_or_not_false",
    }
    blockers.extend(blocker_by_check[check] for check, passed in checks.items() if not passed)
    return blockers, checks


def _review_lineage(candidate: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    lineage = candidate.get("lineage")
    rows = lineage if isinstance(lineage, list) else []
    stage_order = [row.get("stage") for row in rows if isinstance(row, dict)]
    expected_order = [stage for stage, _ in LINEAGE_SPEC]
    ordered = stage_order == expected_order
    schemas_match = len(rows) == len(LINEAGE_SPEC) and all(
        isinstance(row, dict) and row.get("schema") == expected_schema
        for row, (_, expected_schema) in zip(rows, LINEAGE_SPEC)
    )
    refs_safe = len(rows) == len(LINEAGE_SPEC) and all(
        isinstance(row, dict)
        and _is_safe_opaque_id(row.get("candidate_ref"))
        and (index == 0 or _is_safe_opaque_id(row.get("source_candidate_ref")))
        for index, row in enumerate(rows)
    )
    continuity = len(rows) == len(LINEAGE_SPEC) and refs_safe and all(
        rows[index].get("source_candidate_ref") == rows[index - 1].get("candidate_ref")
        for index in range(1, len(rows))
    )
    selected_ref_matches = (
        len(rows) == len(LINEAGE_SPEC)
        and isinstance(rows[-1], dict)
        and rows[-1].get("candidate_ref") == candidate.get("candidate_id")
    )
    no_gap = ordered and schemas_match and continuity and selected_ref_matches
    blockers = [] if no_gap else ["lineage_missing_inconsistent_or_substituted"]
    return (
        {
            "status": "reviewed" if no_gap else "blocked",
            "stage_order": expected_order if no_gap else stage_order,
            "schema_transitions_match": schemas_match,
            "candidate_reference_continuity": continuity and selected_ref_matches,
            "no_lineage_gap": no_gap,
            "no_arbitrary_source_substitution": continuity and selected_ref_matches,
            "source_candidate_refs_are_opaque_ids_only": refs_safe,
            "no_original_row_or_real_package_dependency": (
                candidate.get("real_package_rows_used") is False
            ),
        },
        blockers,
    )


def _review_declaration_context(context: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    valid = all(context.get(key) == value for key, value in DECLARATION_REQUIRED_VALUES.items())
    preserved = {key: context.get(key) for key in DECLARATION_REQUIRED_VALUES}
    return (
        {
            "status": "reviewed_non_authorizing" if valid else "blocked_non_authorizing",
            "declaration_structurally_present_for_docs_only_review": valid,
            "authority_basis_independently_validated": False,
            "manual_review_responsibility_runtime_accepted": False,
            "final_write_authorization_present": False,
            "preserved_context": preserved,
        },
        [] if valid else ["declaration_context_invalid"],
    )


def _review_rollback_plan(
    plan: dict[str, Any], candidate_id: str | None
) -> tuple[dict[str, Any], list[str]]:
    valid = candidate_id is not None and all(
        plan.get(key) == value for key, value in SAFE_ROLLBACK_VALUES.items()
    )
    valid = valid and plan.get("revocation_target_ref") == candidate_id
    return (
        {
            "status": "reviewed" if valid else "blocked",
            "pause_on_any_blocker": plan.get("pause_on_any_blocker") is True,
            "revocation_target_kind": (
                "controlled_candidate_fixture"
                if plan.get("revocation_target_kind") == "controlled_candidate_fixture"
                else None
            ),
            "revocation_target_ref": candidate_id if valid else None,
            "rollback_action": (
                "discard_in_memory_candidate_and_audit"
                if plan.get("rollback_action") == "discard_in_memory_candidate_and_audit"
                else None
            ),
            "persistence_rollback_required": False,
            "no_persistence": True,
            "final_write_authorization_still_required": True,
        },
        [] if valid else ["rollback_pause_revocation_plan_invalid"],
    )


def _contains_forbidden_or_sensitive_data(values: list[Any]) -> bool:
    return any(_scan_value(value, parent_key=None) for value in values)


def _scan_value(value: Any, *, parent_key: str | None) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower()
            if normalized_key in FORBIDDEN_RECURSIVE_KEYS:
                return True
            if _scan_value(nested, parent_key=normalized_key):
                return True
        return False
    if isinstance(value, (list, tuple, set)):
        return any(_scan_value(item, parent_key=parent_key) for item in value)
    if not isinstance(value, str):
        return False
    if parent_key in {"candidate_id", "candidate_ref", "source_candidate_ref"}:
        return False
    stripped = value.strip()
    return bool(
        _URL_RE.match(stripped)
        or _WINDOWS_PATH_RE.match(stripped)
        or stripped.startswith("\\\\")
        or stripped.startswith("/")
        or _EMAIL_RE.match(stripped)
        or _PHONE_RE.match(stripped)
        or _SECRET_VALUE_RE.match(stripped)
    )


def _unsafe_true_flags(values: list[Any]) -> list[str]:
    found: list[str] = []
    for value in values:
        _collect_unsafe_true_flags(value, found)
    return _deduplicate(found)


def _collect_unsafe_true_flags(value: Any, found: list[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower()
            if normalized_key in FALSE_SAFETY_FLAGS and _is_affirmative(nested):
                found.append(normalized_key)
            _collect_unsafe_true_flags(nested, found)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _collect_unsafe_true_flags(item, found)


def _boundary_flags_complete_and_false(candidate: dict[str, Any]) -> bool:
    flags = candidate.get("boundary_flags")
    return isinstance(flags, dict) and all(flags.get(flag) is False for flag in FALSE_SAFETY_FLAGS)


def _has_manual_review_warning(candidate: dict[str, Any]) -> bool:
    warnings = candidate.get("warnings")
    return isinstance(warnings, list) and "manual_review_required" in warnings


def _is_safe_opaque_id(value: Any) -> bool:
    return isinstance(value, str) and bool(_OPAQUE_ID_RE.fullmatch(value))


def _is_affirmative(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes"})


def _deduplicate(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
