from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from app.services import evidence_layer_one_real_candidate_pre_write_review as legacy_review_module


OUTER_APPROVAL_PHRASE = (
    "APPROVE_9A_16B_ONE_APPROVED_ROW_IDENTITY_COMPLETE_LOCKED_CANDIDATE_REVIEW_"
    "AND_CONDITIONAL_9A_17_COMPLETION_NO_WRITE"
)

AUDIT_SCHEMA = "sentigraph_one_real_source_locked_candidate_pre_write_review_audit_v0_1"
AUDIT_MODE = "backend_only_local_one_approved_row_identity_complete_locked_candidate_review_no_write"
IDENTITY_SCHEMA = "sentigraph_one_real_source_locked_candidate_identity_v0_1"
IDENTITY_VERSION = "0.1"
HASH_ALGORITHM = "sha256"
HASH_INPUT_SCOPE = "versioned_safe_canonical_projection_only"
CANDIDATE_LOCK_STATUS = "locked_for_single_candidate_governance_review_only"
IDENTITY_CAPTURE_MARKER_PREFIX = "SENTIGRAPH_9A16C_LOCKED_IDENTITY="

LOCKED_PACKAGE_NAME = legacy_review_module.LOCKED_PACKAGE_NAME
LOCKED_PACKAGE_ROLE = legacy_review_module.LOCKED_PACKAGE_ROLE
LOCKED_CASE_ID_HINT = legacy_review_module.LOCKED_CASE_ID_HINT
LOCKED_ROW_SOURCE = legacy_review_module.LOCKED_ROW_SOURCE
FINAL_CANDIDATE_SCHEMA = legacy_review_module.STAGE_SCHEMAS["production_import_derived_write_candidate"]

DECLARATION_REQUIRED_VALUES = {
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

ROLLBACK_REQUIRED_VALUES = {
    "pause_on_any_blocker": True,
    "revocation_target_kind": "one_real_source_locked_candidate",
    "revocation_target_ref": "bind_locked_final_candidate",
    "rollback_action": "discard_in_memory_preview_candidates_identity_and_audit",
    "persistence_rollback_required": False,
    "no_persistence": True,
    "final_write_authorization_still_required": True,
}

FALSE_SAFETY_FLAGS = [
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

RISK_CLASSIFICATIONS = {
    "wrong_package_selection_risk": "mitigated_for_this_bounded_review",
    "excessive_row_read_risk": "mitigated_for_this_bounded_review",
    "raw_content_retention_risk": "mitigated_for_this_bounded_review",
    "raw_identity_privacy_risk": "mitigated_for_this_bounded_review",
    "secret_exposure_risk": "mitigated_for_this_bounded_review",
    "identity_binding_mismatch_risk": "mitigated_for_this_bounded_review",
    "lineage_mismatch_risk": "mitigated_for_this_bounded_review",
    "irreversible_write_risk": "not_applicable_to_no_write_review",
    "authorization_confusion_risk": "mitigated_for_this_bounded_review",
    "trust_inflation_risk": "mitigated_for_this_bounded_review",
    "provider_output_mistaken_as_truth_risk": "open",
    "duplicate_amplification_risk": "unknown",
    "weak_rejected_evidence_inclusion_risk": "unknown",
    "route_api_frontend_exposure_risk": "not_applicable_to_no_write_review",
    "downstream_production_escalation_risk": "not_applicable_to_no_write_review",
    "source11_finalsummaryreport_escalation_risk": "not_applicable_to_no_write_review",
    "public_customer_readiness_overclaim_risk": "mitigated_for_this_bounded_review",
}

SAFE_METADATA_FIELDS = [
    "evidence_type",
    "platform",
    "created_at_date",
    "trust_label",
    "verification_status",
    "review_status",
    "language",
    "content_visibility",
    "access_scope",
    "redaction_status",
]

LINEAGE_STAGES = [
    "real_exported_package_metadata",
    "approved_evidence_items_jsonl",
    "bounded_redacted_preview_row",
    "controlled_evidence_candidate",
    "controlled_review_queue_candidate",
    "controlled_evidence_layer_import_candidate",
    "controlled_direct_write_candidate",
    "controlled_production_evidence_import_candidate",
    "production_import_derived_write_candidate",
    "locked_candidate_identity_projection",
    "one_real_locked_candidate_pre_write_review",
]

FORBIDDEN_ACTIVE_KEYS = {
    "raw_row",
    "raw_rows",
    "full_row_json",
    "title_text",
    "body_text",
    "comment_text",
    "raw_comment",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_name",
    "username",
    "profile_url",
    "private_message",
    "private_messages",
    "source_url",
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
    "password",
    "passwords",
    ".env",
    "env_value",
    "credential",
    "credentials",
    "absolute_path",
    "package_path",
    "export_root",
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

_OPAQUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,159}$")
_HASH_RE = re.compile(r"^[a-f0-9]{64}$")
_URL_RE = re.compile(r"(?:https?://|www\.)", re.IGNORECASE)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_SECRET_RE = re.compile(r"(?:sk-[A-Za-z0-9]|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----)", re.IGNORECASE)


def review_one_approved_row_as_locked_candidate(
    *,
    exact_outer_approval_phrase: str | None,
    declaration_context: dict[str, Any] | None,
    rollback_plan: dict[str, Any] | None,
) -> dict[str, Any]:
    """Create one identity-complete locked candidate review without any write."""

    _require_outer_approval(exact_outer_approval_phrase)

    safe_declaration = declaration_context if isinstance(declaration_context, dict) else {}
    safe_rollback = rollback_plan if isinstance(rollback_plan, dict) else {}
    preflight_blockers: list[str] = []
    if not _matches_required_values(safe_declaration, DECLARATION_REQUIRED_VALUES):
        preflight_blockers.append("human_declaration_context_invalid")
    if not _matches_required_values(safe_rollback, ROLLBACK_REQUIRED_VALUES):
        preflight_blockers.append("rollback_pause_revocation_plan_invalid")
    preflight_privacy_issue = _contains_sensitive([safe_declaration, safe_rollback])

    if preflight_blockers or preflight_privacy_issue:
        return _assemble_audit(
            legacy_audit={},
            declaration_context=safe_declaration,
            rollback_plan=safe_rollback,
            preflight_blockers=preflight_blockers,
            preflight_privacy_issue=preflight_privacy_issue,
        )

    legacy_audit = legacy_review_module.review_one_real_exported_package_candidate_pre_write(
        exact_outer_approval_phrase=legacy_review_module.OUTER_APPROVAL_PHRASE,
        declaration_context=safe_declaration,
        rollback_plan={
            "pause_on_any_blocker": True,
            "revocation_target_kind": "one_real_source_controlled_candidate",
            "revocation_target_ref": "bind_selected_safe_final_candidate",
            "rollback_action": "discard_in_memory_preview_candidates_and_audit",
            "persistence_rollback_required": False,
            "no_persistence": True,
            "final_write_authorization_still_required": True,
        },
    )
    return _assemble_audit(
        legacy_audit=legacy_audit if isinstance(legacy_audit, dict) else {},
        declaration_context=safe_declaration,
        rollback_plan=safe_rollback,
        preflight_blockers=[],
        preflight_privacy_issue=False,
    )


def build_safe_locked_candidate_identity(source: dict[str, Any]) -> dict[str, Any]:
    """Return only the versioned safe locked-candidate identity fields."""

    nested = source.get("locked_candidate_identity") if isinstance(source, dict) else None
    if isinstance(nested, dict) and _identity_complete(nested):
        return {key: nested.get(key) for key in _identity_output_keys()}
    identity = _build_identity_from_legacy(source if isinstance(source, dict) else {})
    return identity if _identity_complete(identity) else {}


def build_safe_locked_candidate_pre_write_review_summary(audit: dict[str, Any]) -> dict[str, Any]:
    """Return minimized governance output without text, paths, or candidate payloads."""

    identity = build_safe_locked_candidate_identity(audit)
    safe_keys = [
        "audit_schema",
        "phase",
        "audit_mode",
        "audit_status",
        "privacy_issue_stop",
        "approved_package_name",
        "approved_package_role",
        "approved_case_id_hint",
        "approved_row_source",
        "approved_file_open_count",
        "logical_rows_inspected",
        "logical_rows_parsed",
        "preview_rows_created",
        "new_9a16b_locked_candidate_created",
        "old_9a16_ephemeral_candidate_recovered",
        "locked_candidate_identity_complete",
        "locked_candidate_review_complete",
        "whole_package_approved",
        "other_rows_approved",
        "candidate_substitution_allowed",
        "candidate_specific_blockers_clear",
        "candidate_specific_risks_classified",
        "candidate_specific_lineage_verified",
        "candidate_specific_privacy_review_complete",
        "candidate_specific_rollback_plan_verified",
        "authorization_blockers_remaining",
        "final_write_authorization_still_required",
        "overall_write_disposition",
        "ready_for_actual_write",
        "blockers",
        "warnings",
    ]
    summary = {key: audit.get(key) for key in safe_keys}
    summary["locked_candidate_identity"] = identity
    summary.update({key: identity.get(key) for key in _identity_output_keys()})
    return summary


def build_safe_locked_candidate_identity_capture_marker(review_result: dict[str, Any]) -> str:
    """Serialize only the four locked identity values without any file access."""

    if not isinstance(review_result, dict) or review_result.get("locked_candidate_review_complete") is not True:
        raise ValueError("blocked_invalid_9a16c_locked_identity_capture")
    identity = build_safe_locked_candidate_identity(review_result)
    if not _identity_complete(identity):
        raise ValueError("blocked_invalid_9a16c_locked_identity_capture")
    payload = {
        "selected_preview_row_opaque_id": identity["selected_preview_row_opaque_id"],
        "selected_preview_row_safe_hash": identity["selected_preview_row_safe_hash"],
        "final_candidate_id": identity["final_candidate_id"],
        "final_candidate_safe_hash": identity["final_candidate_safe_hash"],
    }
    body = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return f"{IDENTITY_CAPTURE_MARKER_PREFIX}{body}"


def _require_outer_approval(exact_outer_approval_phrase: str | None) -> None:
    if exact_outer_approval_phrase is None or exact_outer_approval_phrase == "":
        raise ValueError("blocked_missing_exact_9a16b_outer_approval")
    if exact_outer_approval_phrase != OUTER_APPROVAL_PHRASE:
        raise ValueError("blocked_wrong_exact_9a16b_outer_approval")


def _assemble_audit(
    *,
    legacy_audit: dict[str, Any],
    declaration_context: dict[str, Any],
    rollback_plan: dict[str, Any],
    preflight_blockers: list[str],
    preflight_privacy_issue: bool,
) -> dict[str, Any]:
    blockers = list(preflight_blockers)
    privacy_issue = preflight_privacy_issue or _contains_sensitive([legacy_audit])

    package_exact = _legacy_package_exact(legacy_audit)
    accounting_exact = _legacy_accounting_exact(legacy_audit)
    schema_exact = legacy_audit.get("final_candidate_schema") == FINAL_CANDIDATE_SCHEMA
    legacy_review_complete = all(
        legacy_audit.get(key) is True
        for key in [
            "one_real_source_candidate_review_complete",
            "candidate_specific_blockers_clear",
            "candidate_specific_risks_classified",
            "candidate_specific_lineage_verified",
            "candidate_specific_privacy_review_complete",
            "candidate_specific_rollback_plan_verified",
        ]
    )

    if legacy_audit:
        if not package_exact:
            blockers.append("approved_package_identity_mismatch")
        if not accounting_exact:
            blockers.append("one_package_one_file_one_row_accounting_invalid")
        if not schema_exact:
            blockers.append("controlled_candidate_schema_mismatch")
        if not legacy_review_complete:
            blockers.append("legacy_candidate_specific_review_incomplete")

    identity = (
        _build_identity_from_legacy(legacy_audit)
        if not privacy_issue and package_exact and accounting_exact and schema_exact and legacy_review_complete
        else {}
    )
    if legacy_audit and not _identity_complete(identity):
        blockers.append("locked_candidate_identity_invalid")

    lineage_valid = bool(
        legacy_review_complete
        and isinstance(legacy_audit.get("lineage_review"), dict)
        and legacy_audit["lineage_review"].get("status") == "reviewed"
        and legacy_audit["lineage_review"].get("candidate_reference_continuity") is True
        and identity
    )
    if legacy_audit and not lineage_valid:
        blockers.append("locked_candidate_lineage_invalid")

    rollback_valid = _matches_required_values(rollback_plan, ROLLBACK_REQUIRED_VALUES) and bool(identity)
    if legacy_audit and not rollback_valid:
        blockers.append("rollback_pause_revocation_plan_invalid")

    blockers = _dedupe(blockers)
    ready = bool(legacy_audit and not privacy_issue and not blockers)
    status = (
        "privacy_issue_stop"
        if privacy_issue
        else "locked_candidate_review_complete_no_write"
        if ready
        else "locked_candidate_review_blocked_no_write"
    )

    human_review = _human_declaration_review(declaration_context)
    final_candidate_id = identity.get("final_candidate_id") if identity else None
    audit: dict[str, Any] = {
        "audit_schema": AUDIT_SCHEMA,
        "phase": "9A-16B",
        "audit_mode": AUDIT_MODE,
        "audit_status": status,
        "privacy_issue_stop": privacy_issue,
        "approved_package_name": LOCKED_PACKAGE_NAME,
        "approved_package_role": LOCKED_PACKAGE_ROLE,
        "approved_case_id_hint": LOCKED_CASE_ID_HINT,
        "approved_row_source": LOCKED_ROW_SOURCE,
        "approved_package_selected": package_exact,
        "approved_evidence_items_jsonl_opened": accounting_exact,
        "approved_file_open_count": 1 if accounting_exact else 0,
        "logical_rows_inspected": 1 if accounting_exact else 0,
        "logical_rows_parsed": 1 if accounting_exact else 0,
        "preview_rows_created": 1 if accounting_exact else 0,
        "row_limit_enforced": legacy_audit.get("row_limit_enforced") is True if legacy_audit else True,
        "evidence_items_csv_opened": False,
        "source_manifest_rows_parsed": 0,
        "collection_log_rows_parsed": 0,
        "alternate_package_used": False,
        "unapproved_package_rows_read": False,
        "directory_enumeration_performed": False,
        "arbitrary_path_accessed": False,
        "private_collector_inspected": False,
        "preview_text_inspected_in_memory": legacy_audit.get("preview_text_inspected_in_memory") is True,
        "preview_text_persisted": False,
        "preview_text_logged": False,
        "preview_text_written_to_report": False,
        "raw_author_identity_exposed": False,
        "profile_url_exposed": False,
        "real_human_pii_exposed": False,
        "secret_value_exposed": False,
        "absolute_path_exposed": False,
        "locked_candidate_identity": identity,
        **{key: identity.get(key) if identity else None for key in _identity_output_keys()},
        "new_9a16b_locked_candidate_created": ready,
        "old_9a16_ephemeral_candidate_recovered": False,
        "one_real_exported_package_selected": package_exact,
        "one_bounded_real_row_reviewed": accounting_exact,
        "locked_candidate_identity_complete": _identity_complete(identity),
        "locked_candidate_review_complete": ready,
        "whole_package_approved": False,
        "other_rows_approved": False,
        "candidate_substitution_allowed": False,
        "package_substitution_allowed": False,
        "row_substitution_allowed": False,
        "real_production_candidate_selected": False,
        "production_evidenceitem_created": False,
        "candidate_blocker_review": {
            "status": "reviewed" if ready else "blocked",
            "exact_package_and_row": package_exact and accounting_exact,
            "schema_exact": schema_exact,
            "identity_complete": _identity_complete(identity),
            "no_unresolved_candidate_specific_structural_blocker": ready,
        },
        "risk_review": {
            "status": "reviewed" if ready else "blocked",
            "classifications": dict(RISK_CLASSIFICATIONS),
            "write_approval_claimed": False,
            "production_readiness_claimed": False,
        },
        "lineage_review": {
            "status": "reviewed" if lineage_valid else "blocked",
            "stage_count": len(LINEAGE_STAGES) if lineage_valid else 0,
            "stages": list(LINEAGE_STAGES) if lineage_valid else [],
            "lineage_gap_detected": not lineage_valid,
            "candidate_reference_continuity": lineage_valid,
            "arbitrary_source_substitution": False,
        },
        "raw_private_secret_review": {
            "status": "blocked" if privacy_issue else "reviewed",
            "privacy_or_forbidden_value_found": privacy_issue,
            "unsafe_value_echoed": False,
        },
        "rollback_pause_revocation_review": {
            "status": "reviewed" if rollback_valid else "blocked",
            "pause_on_any_blocker": rollback_plan.get("pause_on_any_blocker") is True,
            "revocation_target_kind": "one_real_source_locked_candidate" if rollback_valid else None,
            "revocation_target_ref": final_candidate_id if rollback_valid else None,
            "rollback_action": (
                "discard_in_memory_preview_candidates_identity_and_audit" if rollback_valid else None
            ),
            "persistence_rollback_required": False,
            "no_persistence": True,
            "final_write_authorization_still_required": True,
        },
        "human_declaration_context_review": human_review,
        "candidate_specific_blockers_clear": ready,
        "candidate_specific_risks_classified": ready,
        "candidate_specific_lineage_verified": lineage_valid and ready,
        "candidate_specific_privacy_review_complete": not privacy_issue and bool(legacy_audit),
        "candidate_specific_rollback_plan_verified": rollback_valid,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "authorization_blockers_remaining": True,
        "final_write_authorization_still_required": True,
        "overall_write_disposition": "pause",
        "blockers": blockers,
        "warnings": ["manual_review_required", "selected_sample_only"],
        "real_api_called": False,
        "real_llm_called": False,
        "url_fetch_or_scrape": False,
        "provider_called": False,
        "collector_called": False,
        **{flag: False for flag in FALSE_SAFETY_FLAGS},
    }
    return audit


def _build_identity_from_legacy(legacy_audit: dict[str, Any]) -> dict[str, Any]:
    preview_id = legacy_audit.get("selected_preview_row_id")
    final_candidate_id = legacy_audit.get("final_candidate_id")
    final_schema = legacy_audit.get("final_candidate_schema")
    if not _safe_opaque_id(preview_id) or not _safe_opaque_id(final_candidate_id):
        return {}
    if final_schema != FINAL_CANDIDATE_SCHEMA:
        return {}

    safe_metadata = {
        key: value
        for key in SAFE_METADATA_FIELDS
        if (value := _safe_scalar(legacy_audit.get(key))) is not None
    }
    preview_projection = {
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "projection_kind": "selected_preview_row",
        "approved_package_name": LOCKED_PACKAGE_NAME,
        "approved_package_role": LOCKED_PACKAGE_ROLE,
        "approved_case_id_hint": LOCKED_CASE_ID_HINT,
        "approved_row_source": LOCKED_ROW_SOURCE,
        "selected_preview_row_opaque_id": preview_id,
        "row_preview_schema": legacy_audit.get("row_preview_schema"),
        "safe_metadata": safe_metadata,
    }
    selected_hash = _hash_safe_projection(preview_projection)
    final_projection = {
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "projection_kind": "final_locked_candidate",
        "approved_package_name": LOCKED_PACKAGE_NAME,
        "approved_package_role": LOCKED_PACKAGE_ROLE,
        "approved_case_id_hint": LOCKED_CASE_ID_HINT,
        "approved_row_source": LOCKED_ROW_SOURCE,
        "selected_preview_row_opaque_id": preview_id,
        "selected_preview_row_safe_hash": selected_hash,
        "final_candidate_id": final_candidate_id,
        "final_candidate_schema": final_schema,
        "safe_metadata": safe_metadata,
        "lineage_stages": list(LINEAGE_STAGES[:-1]),
    }
    final_hash = _hash_safe_projection(final_projection)
    identity = {
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": IDENTITY_VERSION,
        "selected_preview_row_opaque_id": preview_id,
        "selected_preview_row_safe_hash": selected_hash,
        "final_candidate_id": final_candidate_id,
        "final_candidate_safe_hash": final_hash,
        "final_candidate_schema": final_schema,
        "hash_algorithm": HASH_ALGORITHM,
        "hash_input_scope": HASH_INPUT_SCOPE,
        "candidate_lock_status": CANDIDATE_LOCK_STATUS,
        "safe_hash_length": 64,
        "safe_hash_is_not_raw_content_hash": True,
        "safe_hash_is_not_path_hash": True,
        "safe_hash_is_not_identity_hash": True,
        "safe_hash_reproducible_from_safe_projection": True,
        "candidate_substitution_allowed": False,
    }
    return identity if _identity_complete(identity) else {}


def _hash_safe_projection(projection: dict[str, Any]) -> str:
    canonical = json.dumps(projection, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _legacy_package_exact(audit: dict[str, Any]) -> bool:
    return bool(
        audit
        and audit.get("approved_package_name") == LOCKED_PACKAGE_NAME
        and audit.get("approved_package_role") == LOCKED_PACKAGE_ROLE
        and audit.get("approved_case_id_hint") == LOCKED_CASE_ID_HINT
        and audit.get("approved_row_source") == LOCKED_ROW_SOURCE
        and audit.get("one_real_exported_package_selected") is True
    )


def _legacy_accounting_exact(audit: dict[str, Any]) -> bool:
    return bool(
        audit
        and audit.get("approved_evidence_items_jsonl_opened") is True
        and audit.get("approved_evidence_items_jsonl_rows_parsed") == 1
        and audit.get("real_exported_package_rows_reviewed_count") == 1
        and audit.get("rows_inspected_count") == 1
        and audit.get("preview_rows_count") == 1
        and audit.get("row_limit_enforced") is True
        and audit.get("one_bounded_real_row_reviewed") is True
    )


def _human_declaration_review(context: dict[str, Any]) -> dict[str, Any]:
    valid = _matches_required_values(context, DECLARATION_REQUIRED_VALUES)
    return {
        "status": "reviewed_non_authorizing" if valid else "blocked_non_authorizing",
        "human_declaration_structurally_present": valid,
        "declared_authority_role_label": context.get("declared_authority_role_label"),
        "authority_basis_label": context.get("authority_basis_label"),
        "manual_review_responsibility_statement_present": (
            context.get("manual_review_responsibility_statement_present") is True
        ),
        "warning_count_acknowledgment_present": context.get("warning_count_acknowledgment_present") is True,
        "human_review_required_acknowledgment_present": (
            context.get("human_review_required_acknowledgment_present") is True
        ),
        "no_automatic_trust_upgrade_acknowledgment_present": (
            context.get("no_automatic_trust_upgrade_acknowledgment_present") is True
        ),
        "rollback_pause_revocation_responsibility_label": context.get(
            "rollback_pause_revocation_responsibility_label"
        ),
        "authority_independently_validated": False,
        "responsibility_runtime_accepted": False,
        "final_write_authorization_present": False,
    }


def _identity_complete(identity: dict[str, Any]) -> bool:
    return bool(
        isinstance(identity, dict)
        and identity.get("identity_schema") == IDENTITY_SCHEMA
        and identity.get("identity_version") == IDENTITY_VERSION
        and _safe_opaque_id(identity.get("selected_preview_row_opaque_id"))
        and isinstance(identity.get("selected_preview_row_safe_hash"), str)
        and _HASH_RE.fullmatch(identity["selected_preview_row_safe_hash"])
        and _safe_opaque_id(identity.get("final_candidate_id"))
        and isinstance(identity.get("final_candidate_safe_hash"), str)
        and _HASH_RE.fullmatch(identity["final_candidate_safe_hash"])
        and identity.get("final_candidate_schema") == FINAL_CANDIDATE_SCHEMA
        and identity.get("hash_algorithm") == HASH_ALGORITHM
        and identity.get("hash_input_scope") == HASH_INPUT_SCOPE
        and identity.get("candidate_lock_status") == CANDIDATE_LOCK_STATUS
        and identity.get("candidate_substitution_allowed") is False
    )


def _identity_output_keys() -> list[str]:
    return [
        "identity_schema",
        "identity_version",
        "selected_preview_row_opaque_id",
        "selected_preview_row_safe_hash",
        "final_candidate_id",
        "final_candidate_safe_hash",
        "final_candidate_schema",
        "hash_algorithm",
        "hash_input_scope",
        "candidate_lock_status",
        "safe_hash_length",
        "safe_hash_is_not_raw_content_hash",
        "safe_hash_is_not_path_hash",
        "safe_hash_is_not_identity_hash",
        "safe_hash_reproducible_from_safe_projection",
        "candidate_substitution_allowed",
    ]


def _matches_required_values(value: dict[str, Any], required: dict[str, Any]) -> bool:
    return all(value.get(key) == expected for key, expected in required.items())


def _safe_opaque_id(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and _OPAQUE_ID_RE.fullmatch(value)
        and not _URL_RE.search(value)
        and "/" not in value
        and "\\" not in value
        and ":" not in value
    )


def _safe_scalar(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or len(stripped) > 80 or _string_is_sensitive(stripped):
        return None
    return stripped


def _contains_sensitive(values: list[Any]) -> bool:
    return any(_scan_sensitive(value, parent_key=None) for value in values)


def _scan_sensitive(value: Any, *, parent_key: str | None) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_ACTIVE_KEYS and _active(nested):
                return True
            if _scan_sensitive(nested, parent_key=normalized):
                return True
        return False
    if isinstance(value, (list, tuple, set)):
        return any(_scan_sensitive(item, parent_key=parent_key) for item in value)
    if not isinstance(value, str):
        return False
    if parent_key in {
        "selected_preview_row_id",
        "selected_preview_row_opaque_id",
        "final_candidate_id",
        "revocation_target_ref",
    }:
        return False
    return _string_is_sensitive(value)


def _string_is_sensitive(value: str) -> bool:
    text = value.strip()
    return bool(
        _URL_RE.search(text)
        or _EMAIL_RE.search(text)
        or _SECRET_RE.search(text)
        or re.match(r"^[A-Za-z]:[\\/]", text)
        or text.startswith("\\\\")
        or text.lower().startswith("file://")
    )


def _active(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, (str, list, tuple, set, dict)):
        return bool(value)
    return True


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
