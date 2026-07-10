from __future__ import annotations

import re
from typing import Any

from app.services import controlled_evidence_candidate as evidence_candidate_module
from app.services import controlled_evidence_layer_import_candidate as import_candidate_module
from app.services import controlled_evidence_layer_write_candidate as direct_write_candidate_module
from app.services import controlled_evidence_layer_write_candidate_from_production_import_candidate as derived_write_candidate_module
from app.services import controlled_production_evidence_import_candidate as production_import_candidate_module
from app.services import controlled_review_queue_candidate as review_queue_candidate_module
from app.services import controlled_row_preview as row_preview_module


OUTER_APPROVAL_PHRASE = "APPROVE_9A_16_ONE_REAL_EXPORTED_PACKAGE_BOUNDED_REDACTED_ROW_CANDIDATE_SPECIFIC_EVIDENCE_LAYER_PRE_WRITE_REVIEW_NO_WRITE"
INNER_ROW_PREVIEW_APPROVAL_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"

AUDIT_SCHEMA = "sentigraph_one_real_exported_package_candidate_pre_write_review_audit_v0_1"
AUDIT_MODE = "backend_only_local_one_real_exported_package_candidate_pre_write_review_no_write"

LOCKED_PACKAGE_NAME = "donglu-sunjihai-youth-football-202606-v2_20260617_121016"
LOCKED_PACKAGE_ROLE = "candidate_demo_sample"
LOCKED_CASE_ID_HINT = "donglu_sunjihai_youth_football_202606"
LOCKED_ROW_SOURCE = "evidence_items.jsonl"
LOCKED_ROW_FILE_PARTS = (
    "docs",
    "samples",
    "donglu_sunjihai_youth_football",
    LOCKED_PACKAGE_NAME,
    LOCKED_ROW_SOURCE,
)

STAGE_SCHEMAS = {
    "controlled_row_preview": "sentigraph_controlled_row_preview_v0_1",
    "controlled_evidence_candidate": "sentigraph_controlled_evidence_candidate_set_v0_1",
    "controlled_review_queue_candidate": "sentigraph_controlled_review_queue_candidate_set_v0_1",
    "controlled_evidence_layer_import_candidate": "sentigraph_controlled_evidence_layer_import_candidate_set_v0_1",
    "controlled_direct_write_candidate": "sentigraph_controlled_evidence_layer_write_candidate_set_v0_1",
    "controlled_production_evidence_import_candidate": "sentigraph_controlled_production_evidence_import_candidate_set_v0_1",
    "production_import_derived_write_candidate": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
}

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
    "one_real_candidate_pre_write_review",
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
    "manual_review_responsibility_accepted": False,
    "runtime_human_authority_validation_performed": False,
    "runtime_manual_review_responsibility_acceptance_performed": False,
    "final_write_authorization_performed": False,
    "final_write_authorization_still_required": True,
    "actual_write_authorized": False,
    "production_evidenceitem_creation_authorized": False,
    "ready_for_actual_write": False,
}

ROLLBACK_POLICY_VALUES = {
    "pause_on_any_blocker": True,
    "revocation_target_kind": "one_real_source_controlled_candidate",
    "revocation_target_ref": "bind_selected_safe_final_candidate",
    "rollback_action": "discard_in_memory_preview_candidates_and_audit",
    "persistence_rollback_required": False,
    "no_persistence": True,
    "final_write_authorization_still_required": True,
}

RISK_CLASSIFICATIONS = {
    "wrong_package_selection_risk": "mitigated_for_this_bounded_review",
    "excessive_row_read_risk": "mitigated_for_this_bounded_review",
    "raw_content_retention_risk": "mitigated_for_this_bounded_review",
    "raw_identity_privacy_risk": "mitigated_for_this_bounded_review",
    "secret_exposure_risk": "mitigated_for_this_bounded_review",
    "lineage_mismatch_risk": "mitigated_for_this_bounded_review",
    "irreversible_write_risk": "not_applicable_to_no_write_review",
    "authorization_confusion_risk": "mitigated_for_this_bounded_review",
    "trust_inflation_risk": "mitigated_for_this_bounded_review",
    "provider_vendor_output_mistaken_as_truth_risk": "open",
    "duplicate_amplification_risk": "unknown",
    "rejected_weak_evidence_inclusion_risk": "unknown",
    "route_api_frontend_accidental_write_exposure_risk": "not_applicable_to_no_write_review",
    "downstream_production_escalation_risk": "not_applicable_to_no_write_review",
    "source11_finalsummaryreport_escalation_risk": "not_applicable_to_no_write_review",
    "public_customer_readiness_overclaim_risk": "mitigated_for_this_bounded_review",
}

FORBIDDEN_ACTIVE_KEYS = {
    "raw_row",
    "raw_rows",
    "full_row_json",
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

SAFE_OUTPUT_METADATA_FIELDS = [
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

_OPAQUE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,159}$")
_SAFE_HASH_RE = re.compile(r"^[a-f0-9]{16,64}$")
_URL_RE = re.compile(r"(?:https?://|www\.)", re.IGNORECASE)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"\+?\d[\d ()-]{7,}\d")
_SECRET_RE = re.compile(r"(?:sk-[A-Za-z0-9]|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----)", re.IGNORECASE)
_HANDLE_RE = re.compile(r"@[A-Za-z0-9_][A-Za-z0-9_.-]{2,}")


def review_one_real_exported_package_candidate_pre_write(
    *,
    exact_outer_approval_phrase: str | None,
    declaration_context: dict[str, Any] | None,
    rollback_plan: dict[str, Any] | None,
) -> dict[str, Any]:
    """Review one approved real-source candidate chain without write or persistence."""

    _require_outer_approval(exact_outer_approval_phrase)
    _require_static_contract_locks()

    safe_declaration = declaration_context if isinstance(declaration_context, dict) else {}
    safe_rollback = rollback_plan if isinstance(rollback_plan, dict) else {}
    declaration_review, declaration_blockers = _review_declaration_context(safe_declaration)
    rollback_policy_valid = all(safe_rollback.get(key) == value for key, value in ROLLBACK_POLICY_VALUES.items())
    preflight_unsafe_flags = _unsafe_true_flags([safe_declaration, safe_rollback])
    preflight_privacy_issue = _contains_privacy_or_secret([safe_declaration, safe_rollback])
    preflight_blockers = [*declaration_blockers]
    if not rollback_policy_valid:
        preflight_blockers.append("rollback_pause_revocation_plan_invalid")
    preflight_blockers.extend(f"unsafe_true_flag:{flag}" for flag in preflight_unsafe_flags)
    preflight_blockers = _dedupe(preflight_blockers)

    if preflight_privacy_issue or preflight_blockers:
        return _assemble_audit(
            chain={},
            declaration_review=declaration_review,
            rollback_policy=safe_rollback,
            preflight_blockers=preflight_blockers,
            preflight_privacy_issue=preflight_privacy_issue,
        )

    chain = _build_controlled_candidate_chain()
    return _assemble_audit(
        chain=chain,
        declaration_review=declaration_review,
        rollback_policy=safe_rollback,
        preflight_blockers=[],
        preflight_privacy_issue=False,
    )


def build_safe_one_real_candidate_pre_write_review_summary(audit: dict[str, Any]) -> dict[str, Any]:
    """Return a compact summary without row text, candidate payloads, or filesystem paths."""

    safe_keys = [
        "audit_schema",
        "phase",
        "audit_mode",
        "audit_status",
        "approved_package_name",
        "approved_package_role",
        "approved_case_id_hint",
        "approved_row_source",
        "selected_preview_row_id",
        "selected_row_safe_hash",
        "final_candidate_id",
        "final_candidate_schema",
        "preview_rows_count",
        "rows_inspected_count",
        "approved_evidence_items_jsonl_rows_parsed",
        "one_real_exported_package_selected",
        "one_bounded_real_row_reviewed",
        "one_real_source_candidate_created",
        "one_real_source_candidate_review_complete",
        "candidate_specific_blockers_clear",
        "candidate_specific_risks_classified",
        "candidate_specific_lineage_verified",
        "candidate_specific_privacy_review_complete",
        "candidate_specific_rollback_plan_verified",
        "authorization_blockers_remaining",
        "final_write_authorization_still_required",
        "overall_write_disposition",
        "ready_for_actual_write",
        "privacy_issue_stop",
        "blockers",
        "warnings",
    ]
    summary = {key: audit.get(key) for key in safe_keys}
    summary.update({field: audit.get(field) for field in SAFE_OUTPUT_METADATA_FIELDS})
    return summary


def _require_outer_approval(exact_outer_approval_phrase: str | None) -> None:
    if exact_outer_approval_phrase is None or exact_outer_approval_phrase == "":
        raise ValueError("blocked_missing_exact_9a16_outer_approval")
    if exact_outer_approval_phrase != OUTER_APPROVAL_PHRASE:
        raise ValueError("blocked_wrong_exact_9a16_outer_approval")


def _require_static_contract_locks() -> None:
    package_lock_values = {
        row_preview_module.APPROVED_PACKAGE_NAME: LOCKED_PACKAGE_NAME,
        row_preview_module.APPROVED_PACKAGE_ROLE: LOCKED_PACKAGE_ROLE,
        row_preview_module.APPROVED_CASE_ID_HINT: LOCKED_CASE_ID_HINT,
        row_preview_module.APPROVED_ROW_SOURCE: LOCKED_ROW_SOURCE,
    }
    if any(actual != expected for actual, expected in package_lock_values.items()):
        raise ValueError("blocked_exact_approved_package_lock_mismatch")
    if tuple(row_preview_module.APPROVED_ROW_FILE.parts) != LOCKED_ROW_FILE_PARTS:
        raise ValueError("blocked_exact_approved_package_lock_mismatch")
    if row_preview_module.APPROVAL_PHRASE != INNER_ROW_PREVIEW_APPROVAL_PHRASE:
        raise ValueError("blocked_inner_8w7_guard_mismatch")

    expected_ascii_guards = [
        (evidence_candidate_module.APPROVAL_PHRASE, "APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION"),
        (review_queue_candidate_module.APPROVAL_PHRASE, "APPROVE_8W_13_CONTROLLED_REVIEW_QUEUE_CANDIDATE_IMPLEMENTATION"),
        (import_candidate_module.APPROVAL_PHRASE, "APPROVE_8W_16_CONTROLLED_EVIDENCE_LAYER_IMPORT_CANDIDATE_IMPLEMENTATION"),
        (direct_write_candidate_module.APPROVAL_PHRASE, "APPROVE_8W_19_CONTROLLED_EVIDENCE_LAYER_WRITE_CANDIDATE_IMPLEMENTATION"),
    ]
    if any(actual != expected or not actual.isascii() for actual, expected in expected_ascii_guards):
        raise ValueError("blocked_downstream_helper_guard_contract_mismatch")

    approval_prefix = chr(0x6279) + chr(0x51C6)
    expected_unicode_guards = [
        (
            production_import_candidate_module.APPROVAL_PHRASE,
            f"{approval_prefix} 8W-22 Controlled Production Evidence Import Candidate Helper Implementation",
        ),
        (
            derived_write_candidate_module.APPROVAL_PHRASE,
            f"{approval_prefix} 8W-25 Controlled Evidence Layer Write Candidate Helper Implementation",
        ),
    ]
    if any(actual != expected for actual, expected in expected_unicode_guards):
        raise ValueError("blocked_downstream_helper_guard_contract_mismatch")


def _build_controlled_candidate_chain() -> dict[str, Any]:
    source_boundary = {
        "schema": row_preview_module.SOURCE_SCHEMA,
        "phase": row_preview_module.SOURCE_PHASE,
        "boundary_status": row_preview_module.SOURCE_READY_STATUS,
        "approved_target_package_name": LOCKED_PACKAGE_NAME,
        "approved_target_package_role": LOCKED_PACKAGE_ROLE,
        "approved_target_case_id_hint": LOCKED_CASE_ID_HINT,
        "metadata_only": True,
        "warning_count": 1,
        "human_review_required": True,
        "warning_manual_review_preserved": True,
        "row_preview_approved": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "runtime_side_effects": {},
    }
    preview = row_preview_module.build_controlled_row_preview(
        source_boundary,
        approval_phrase=INNER_ROW_PREVIEW_APPROVAL_PHRASE,
        max_preview_rows=1,
        row_source=LOCKED_ROW_SOURCE,
    )
    chain: dict[str, Any] = {"row_preview": preview}
    if not _preview_ready_for_candidate_chain(preview):
        return chain

    evidence_candidates = evidence_candidate_module.build_controlled_evidence_candidate_set(
        preview,
        exact_approval_phrase=evidence_candidate_module.APPROVAL_PHRASE,
        candidate_limit=1,
    )
    chain["evidence_candidate_set"] = evidence_candidates
    if not _stage_ready(
        evidence_candidates,
        schema_key="candidate_set_schema",
        schema=STAGE_SCHEMAS["controlled_evidence_candidate"],
        count_key="candidate_count",
        list_key="candidates",
        created_key="evidence_candidate_created",
    ):
        return chain

    review_candidates = review_queue_candidate_module.build_controlled_review_queue_candidate_set(
        evidence_candidates,
        exact_approval_phrase=review_queue_candidate_module.APPROVAL_PHRASE,
        candidate_limit=1,
    )
    chain["review_queue_candidate_set"] = review_candidates
    if not _stage_ready(
        review_candidates,
        schema_key="review_queue_candidate_set_schema",
        schema=STAGE_SCHEMAS["controlled_review_queue_candidate"],
        count_key="review_queue_candidate_count",
        list_key="review_queue_candidates",
        created_key="review_queue_candidate_created",
    ):
        return chain

    import_candidates = import_candidate_module.build_controlled_evidence_layer_import_candidate_set(
        review_candidates,
        exact_approval_phrase=import_candidate_module.APPROVAL_PHRASE,
        candidate_limit=1,
    )
    chain["import_candidate_set"] = import_candidates
    if not _stage_ready(
        import_candidates,
        schema_key="evidence_layer_import_candidate_set_schema",
        schema=STAGE_SCHEMAS["controlled_evidence_layer_import_candidate"],
        count_key="evidence_layer_import_candidate_count",
        list_key="evidence_layer_import_candidates",
        created_key="evidence_layer_import_candidate_created",
    ):
        return chain

    direct_write_candidates = direct_write_candidate_module.build_controlled_evidence_layer_write_candidate_set(
        import_candidates,
        exact_approval_phrase=direct_write_candidate_module.APPROVAL_PHRASE,
        candidate_limit=1,
    )
    chain["direct_write_candidate_set"] = direct_write_candidates
    if not _stage_ready(
        direct_write_candidates,
        schema_key="evidence_layer_write_candidate_set_schema",
        schema=STAGE_SCHEMAS["controlled_direct_write_candidate"],
        count_key="evidence_layer_write_candidate_count",
        list_key="evidence_layer_write_candidates",
        created_key="evidence_layer_write_candidate_created",
    ):
        return chain

    production_import_candidates = (
        production_import_candidate_module.build_controlled_production_evidence_import_candidate_set(
            direct_write_candidates,
            exact_approval_phrase=production_import_candidate_module.APPROVAL_PHRASE,
            candidate_limit=1,
        )
    )
    chain["production_import_candidate_set"] = production_import_candidates
    if not _stage_ready(
        production_import_candidates,
        schema_key="production_evidence_import_candidate_set_schema",
        schema=STAGE_SCHEMAS["controlled_production_evidence_import_candidate"],
        count_key="production_evidence_import_candidate_count",
        list_key="production_evidence_import_candidates",
        created_key="production_evidence_import_candidate_created",
    ):
        return chain

    derived_write_candidates = (
        derived_write_candidate_module.build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set(
            production_import_candidates,
            exact_approval_phrase=derived_write_candidate_module.APPROVAL_PHRASE,
            candidate_limit=1,
        )
    )
    chain["derived_write_candidate_set"] = derived_write_candidates
    return chain


def _preview_ready_for_candidate_chain(preview: dict[str, Any]) -> bool:
    rows = preview.get("preview_rows")
    runtime = preview.get("runtime_side_effects")
    return bool(
        preview.get("schema") == STAGE_SCHEMAS["controlled_row_preview"]
        and preview.get("approved_target_package_name") == LOCKED_PACKAGE_NAME
        and preview.get("approved_target_package_role") == LOCKED_PACKAGE_ROLE
        and preview.get("approved_target_case_id_hint") == LOCKED_CASE_ID_HINT
        and preview.get("row_source") == LOCKED_ROW_SOURCE
        and preview.get("max_preview_rows_requested") == 1
        and preview.get("max_preview_rows_applied") == 1
        and preview.get("rows_inspected_count") == 1
        and preview.get("preview_rows_count") == 1
        and isinstance(rows, list)
        and len(rows) == 1
        and isinstance(rows[0], dict)
        and isinstance(runtime, dict)
        and runtime.get("opened_approved_evidence_items_jsonl") is True
        and runtime.get("parsed_evidence_items_jsonl") is True
        and not _contains_privacy_or_secret([preview])
    )


def _stage_ready(
    stage: dict[str, Any],
    *,
    schema_key: str,
    schema: str,
    count_key: str,
    list_key: str,
    created_key: str,
) -> bool:
    rows = stage.get(list_key)
    return bool(
        stage.get(schema_key) == schema
        and stage.get(count_key) == 1
        and isinstance(rows, list)
        and len(rows) == 1
        and isinstance(rows[0], dict)
        and stage.get(created_key) is True
        and stage.get("human_review_required") is True
        and not _unsafe_true_flags([stage])
        and not _contains_privacy_or_secret([stage])
    )


def _assemble_audit(
    *,
    chain: dict[str, Any],
    declaration_review: dict[str, Any],
    rollback_policy: dict[str, Any],
    preflight_blockers: list[str],
    preflight_privacy_issue: bool,
) -> dict[str, Any]:
    chain_review = _review_chain(chain)
    final_candidate_id = chain_review["final_candidate_id"]
    rollback_valid = bool(
        final_candidate_id
        and all(rollback_policy.get(key) == value for key, value in ROLLBACK_POLICY_VALUES.items())
    )
    rollback_review = {
        "status": "reviewed" if rollback_valid else "blocked",
        "pause_on_any_blocker": rollback_policy.get("pause_on_any_blocker") is True,
        "revocation_target_kind": (
            "one_real_source_controlled_candidate"
            if rollback_policy.get("revocation_target_kind") == "one_real_source_controlled_candidate"
            else None
        ),
        "revocation_target_ref": final_candidate_id if rollback_valid else None,
        "rollback_action": (
            "discard_in_memory_preview_candidates_and_audit"
            if rollback_policy.get("rollback_action") == "discard_in_memory_preview_candidates_and_audit"
            else None
        ),
        "persistence_rollback_required": False,
        "no_persistence": True,
        "final_write_authorization_still_required": True,
    }

    blockers = [*preflight_blockers, *chain_review["blockers"]]
    if chain and not rollback_valid:
        blockers.append("rollback_pause_revocation_plan_invalid")
    privacy_issue = preflight_privacy_issue or chain_review["privacy_issue"]
    if privacy_issue:
        blockers.insert(0, "privacy_or_forbidden_value_detected")
    blockers = _dedupe(blockers)
    ready = bool(chain and not privacy_issue and not blockers)
    status = (
        "privacy_issue_stop"
        if privacy_issue
        else "one_real_candidate_review_complete_no_write"
        if ready
        else "one_real_candidate_review_blocked_no_write"
    )

    package_review = chain_review["package_selection_review"]
    lineage_review = chain_review["lineage_review"]
    risk_status = "reviewed" if ready else "blocked"
    candidate_blocker_checks = dict(chain_review["candidate_blocker_checks"])
    candidate_blocker_checks["warning_acknowledgment_present"] = (
        declaration_review["preserved_context"].get("warning_count_acknowledgment_present") is True
    )
    candidate_blocker_checks["no_automatic_trust_upgrade"] = (
        declaration_review["preserved_context"].get("no_automatic_trust_upgrade_acknowledgment_present") is True
    )
    candidate_blocker_checks["rollback_plan_verified"] = rollback_valid

    audit = {
        "audit_schema": AUDIT_SCHEMA,
        "phase": "9A-16",
        "audit_mode": AUDIT_MODE,
        "audit_status": status,
        "privacy_issue_stop": privacy_issue,
        "approved_package_name": LOCKED_PACKAGE_NAME,
        "approved_package_role": LOCKED_PACKAGE_ROLE,
        "approved_case_id_hint": LOCKED_CASE_ID_HINT,
        "approved_row_source": LOCKED_ROW_SOURCE,
        "approved_real_exported_package_selected": package_review["package_identity_match"],
        "approved_evidence_items_jsonl_opened": chain_review["approved_evidence_items_jsonl_opened"],
        "approved_evidence_items_jsonl_rows_parsed": chain_review["approved_evidence_items_jsonl_rows_parsed"],
        "real_exported_package_rows_reviewed_count": chain_review["approved_evidence_items_jsonl_rows_parsed"],
        "preview_rows_count": chain_review["preview_rows_count"],
        "rows_inspected_count": chain_review["rows_inspected_count"],
        "row_limit_enforced": chain_review["row_limit_enforced"],
        "real_integration_test_skipped": False,
        "alternate_package_used": False,
        "directory_enumeration_performed": False,
        "arbitrary_path_accessed": False,
        "evidence_items_csv_opened": False,
        "source_manifest_rows_parsed": False,
        "collection_log_rows_parsed": False,
        "unapproved_package_rows_read": False,
        "production_package_rows_parsed": False,
        "private_collector_inspected": False,
        "preview_text_inspected_in_memory": chain_review["preview_text_inspected_in_memory"],
        "preview_text_persisted": False,
        "preview_text_written_to_health_report": False,
        "preview_text_logged": False,
        "raw_author_identity_exposed": False,
        "secret_value_exposed": False,
        "real_human_pii_exposed": False,
        "row_preview_schema": chain_review["row_preview_schema"],
        "stage_schemas": dict(chain_review["stage_schemas"]),
        "selected_preview_row_id": chain_review["selected_preview_row_id"],
        "selected_row_safe_hash": chain_review["selected_row_safe_hash"],
        "final_candidate_id": final_candidate_id,
        "final_candidate_schema": chain_review["final_candidate_schema"],
        **chain_review["safe_metadata"],
        "package_selection_review": package_review,
        "candidate_blocker_review": {
            "status": "reviewed" if ready else "blocked",
            "checks": candidate_blocker_checks,
        },
        "risk_review": {
            "status": risk_status,
            "classifications": dict(RISK_CLASSIFICATIONS),
            "write_approval_claimed": False,
            "production_readiness_claimed": False,
        },
        "lineage_review": lineage_review,
        "raw_private_secret_review": {
            "status": "blocked" if privacy_issue else "reviewed",
            "privacy_or_forbidden_value_found": privacy_issue,
            "unsafe_value_echoed": False,
        },
        "rollback_pause_revocation_review": rollback_review,
        "human_declaration_context_review": declaration_review,
        "one_real_exported_package_selected": package_review["package_identity_match"],
        "one_bounded_real_row_reviewed": chain_review["one_bounded_real_row_reviewed"],
        "one_real_source_candidate_created": chain_review["one_real_source_candidate_created"],
        "one_real_source_candidate_review_complete": ready,
        "real_production_candidate_selected": False,
        "real_production_candidate_reviewed": False,
        "candidate_specific_blockers_clear": ready,
        "candidate_specific_risks_classified": ready,
        "candidate_specific_lineage_verified": ready and lineage_review["status"] == "reviewed",
        "candidate_specific_privacy_review_complete": not privacy_issue and bool(chain),
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


def _review_chain(chain: dict[str, Any]) -> dict[str, Any]:
    if not chain:
        return _empty_chain_review()

    preview = _dict(chain.get("row_preview"))
    evidence_set = _dict(chain.get("evidence_candidate_set"))
    review_set = _dict(chain.get("review_queue_candidate_set"))
    import_set = _dict(chain.get("import_candidate_set"))
    direct_set = _dict(chain.get("direct_write_candidate_set"))
    production_set = _dict(chain.get("production_import_candidate_set"))
    derived_set = _dict(chain.get("derived_write_candidate_set"))

    preview_row = _single_row(preview, "preview_rows")
    evidence_candidate = _single_row(evidence_set, "candidates")
    review_candidate = _single_row(review_set, "review_queue_candidates")
    import_candidate = _single_row(import_set, "evidence_layer_import_candidates")
    direct_candidate = _single_row(direct_set, "evidence_layer_write_candidates")
    production_candidate = _single_row(production_set, "production_evidence_import_candidates")
    final_candidate = _single_row(derived_set, "evidence_layer_write_candidates")

    actual_stage_schemas = {
        "controlled_row_preview": preview.get("schema"),
        "controlled_evidence_candidate": evidence_set.get("candidate_set_schema"),
        "controlled_review_queue_candidate": review_set.get("review_queue_candidate_set_schema"),
        "controlled_evidence_layer_import_candidate": import_set.get("evidence_layer_import_candidate_set_schema"),
        "controlled_direct_write_candidate": direct_set.get("evidence_layer_write_candidate_set_schema"),
        "controlled_production_evidence_import_candidate": production_set.get(
            "production_evidence_import_candidate_set_schema"
        ),
        "production_import_derived_write_candidate": derived_set.get("evidence_layer_write_candidate_set_schema"),
    }
    schemas_exact = actual_stage_schemas == STAGE_SCHEMAS
    counts_exact = all(
        [
            preview.get("preview_rows_count") == 1 and len(_list(preview.get("preview_rows"))) == 1,
            evidence_set.get("candidate_count") == 1 and len(_list(evidence_set.get("candidates"))) == 1,
            review_set.get("review_queue_candidate_count") == 1
            and len(_list(review_set.get("review_queue_candidates"))) == 1,
            import_set.get("evidence_layer_import_candidate_count") == 1
            and len(_list(import_set.get("evidence_layer_import_candidates"))) == 1,
            direct_set.get("evidence_layer_write_candidate_count") == 1
            and len(_list(direct_set.get("evidence_layer_write_candidates"))) == 1,
            production_set.get("production_evidence_import_candidate_count") == 1
            and len(_list(production_set.get("production_evidence_import_candidates"))) == 1,
            derived_set.get("evidence_layer_write_candidate_count") == 1
            and len(_list(derived_set.get("evidence_layer_write_candidates"))) == 1,
        ]
    )
    package_identity_match = all(
        [
            preview.get("approved_target_package_name") == LOCKED_PACKAGE_NAME,
            preview.get("approved_target_package_role") == LOCKED_PACKAGE_ROLE,
            preview.get("approved_target_case_id_hint") == LOCKED_CASE_ID_HINT,
        ]
    )
    row_source_match = preview.get("row_source") == LOCKED_ROW_SOURCE
    row_accounting_exact = all(
        [
            preview.get("max_preview_rows_requested") == 1,
            preview.get("max_preview_rows_applied") == 1,
            preview.get("rows_inspected_count") == 1,
            preview.get("preview_rows_count") == 1,
            preview.get("row_limit_enforced") is True,
        ]
    )
    runtime = _dict(preview.get("runtime_side_effects"))
    file_read_exact = all(
        [
            runtime.get("opened_approved_evidence_items_jsonl") is True,
            runtime.get("parsed_evidence_items_jsonl") is True,
            runtime.get("parsed_evidence_items_csv") is False,
            runtime.get("parsed_source_manifest_jsonl_rows") is False,
            runtime.get("parsed_collection_log_jsonl_rows") is False,
        ]
    )
    ids = {
        "preview": preview_row.get("preview_row_id"),
        "evidence": evidence_candidate.get("candidate_id"),
        "review": review_candidate.get("review_queue_candidate_id"),
        "import": import_candidate.get("evidence_layer_import_candidate_id"),
        "direct": direct_candidate.get("evidence_layer_write_candidate_id"),
        "production_import": production_candidate.get("production_evidence_import_candidate_id"),
        "final": final_candidate.get("evidence_layer_write_candidate_id"),
    }
    ids_safe = all(_is_safe_opaque_id(value) for value in ids.values())
    evidence_hash = preview_row.get("evidence_id_hash")
    hash_safe = isinstance(evidence_hash, str) and bool(_SAFE_HASH_RE.fullmatch(evidence_hash))
    continuity = all(
        [
            evidence_candidate.get("source_preview_row_id") == ids["preview"],
            review_candidate.get("source_evidence_candidate_id") == ids["evidence"],
            import_candidate.get("source_review_queue_candidate_id") == ids["review"],
            import_candidate.get("source_evidence_candidate_id") == ids["evidence"],
            direct_candidate.get("source_evidence_layer_import_candidate_id") == ids["import"],
            direct_candidate.get("source_review_queue_candidate_id") == ids["review"],
            direct_candidate.get("source_evidence_candidate_id") == ids["evidence"],
            production_candidate.get("source_evidence_layer_write_candidate_id") == ids["direct"],
            production_candidate.get("source_evidence_layer_import_candidate_id") == ids["import"],
            production_candidate.get("source_review_queue_candidate_id") == ids["review"],
            production_candidate.get("source_evidence_candidate_id") == ids["evidence"],
            final_candidate.get("source_production_evidence_import_candidate_id") == ids["production_import"],
            final_candidate.get("source_evidence_layer_write_candidate_id") == ids["direct"],
            final_candidate.get("source_evidence_layer_import_candidate_id") == ids["import"],
            final_candidate.get("source_review_queue_candidate_id") == ids["review"],
            final_candidate.get("source_evidence_candidate_id") == ids["evidence"],
        ]
    )
    human_review_preserved = all(
        candidate.get("human_review_required") is True
        for candidate in [evidence_candidate, review_candidate, import_candidate, direct_candidate, production_candidate, final_candidate]
    )
    privacy_issue = _contains_privacy_or_secret([chain])
    unsafe_flags = _unsafe_true_flags([chain])
    blockers: list[str] = []
    if not package_identity_match:
        blockers.append("approved_package_identity_mismatch")
    if not row_source_match:
        blockers.append("approved_row_source_mismatch")
    if not row_accounting_exact or not file_read_exact:
        blockers.append("one_bounded_row_accounting_invalid")
    if not schemas_exact:
        blockers.append("controlled_candidate_chain_schema_mismatch")
    if not counts_exact:
        blockers.append("controlled_candidate_chain_count_not_exactly_one")
    if not ids_safe or not hash_safe:
        blockers.append("candidate_or_preview_id_not_safe_opaque")
    if not continuity:
        blockers.append("candidate_lineage_gap_or_substitution")
    if not human_review_preserved:
        blockers.append("human_review_required_not_preserved")
    blockers.extend(f"unsafe_true_flag:{flag}" for flag in unsafe_flags)
    blockers = _dedupe(blockers)

    preview_text = preview_row.get("text_snippet_redacted")
    preview_text_inspected = isinstance(preview_text, str) and bool(preview_text.strip())
    safe_metadata = {
        field: preview_row.get(field)
        for field in SAFE_OUTPUT_METADATA_FIELDS
        if _safe_output_value(preview_row.get(field)) is not None
    }
    safe_metadata = {key: _safe_output_value(value) for key, value in safe_metadata.items()}
    final_schema = derived_set.get("evidence_layer_write_candidate_set_schema")
    lineage_ready = bool(
        package_identity_match
        and row_source_match
        and schemas_exact
        and counts_exact
        and ids_safe
        and continuity
    )
    return {
        "blockers": blockers,
        "privacy_issue": privacy_issue,
        "package_selection_review": {
            "status": "reviewed" if package_identity_match and row_source_match else "blocked",
            "package_identity_match": package_identity_match,
            "package_role_match": preview.get("approved_target_package_role") == LOCKED_PACKAGE_ROLE,
            "case_id_hint_match": preview.get("approved_target_case_id_hint") == LOCKED_CASE_ID_HINT,
            "row_source_match": row_source_match,
            "alternate_package_used": False,
            "alternate_row_source_used": False,
            "directory_enumeration_performed": False,
            "arbitrary_path_accessed": False,
        },
        "candidate_blocker_checks": {
            "all_schemas_exact": schemas_exact,
            "one_preview_row_only": row_accounting_exact,
            "one_final_candidate_only": counts_exact,
            "safe_opaque_ids_only": ids_safe and hash_safe,
            "human_review_required": human_review_preserved,
            "no_unsafe_true_flags": not unsafe_flags,
            "no_write_runtime_or_production_surface": not unsafe_flags,
            "no_unresolved_candidate_specific_structural_blocker": not blockers,
        },
        "lineage_review": {
            "status": "reviewed" if lineage_ready else "blocked",
            "stage_count": len(LINEAGE_STAGES) if lineage_ready else 0,
            "stages": list(LINEAGE_STAGES) if lineage_ready else [],
            "lineage_gap_detected": not continuity,
            "package_identity_match": package_identity_match,
            "case_id_hint_match": preview.get("approved_target_case_id_hint") == LOCKED_CASE_ID_HINT,
            "candidate_reference_continuity": continuity,
            "arbitrary_source_substitution": not continuity,
            "alternate_package_used": False,
            "alternate_row_source_used": False,
        },
        "row_preview_schema": preview.get("schema"),
        "stage_schemas": actual_stage_schemas,
        "selected_preview_row_id": ids["preview"] if _is_safe_opaque_id(ids["preview"]) else None,
        "selected_row_safe_hash": evidence_hash if hash_safe else None,
        "final_candidate_id": ids["final"] if _is_safe_opaque_id(ids["final"]) else None,
        "final_candidate_schema": final_schema if final_schema == STAGE_SCHEMAS["production_import_derived_write_candidate"] else None,
        "safe_metadata": safe_metadata,
        "approved_evidence_items_jsonl_opened": runtime.get("opened_approved_evidence_items_jsonl") is True,
        "approved_evidence_items_jsonl_rows_parsed": 1 if file_read_exact and row_accounting_exact else 0,
        "preview_rows_count": preview.get("preview_rows_count") if isinstance(preview.get("preview_rows_count"), int) else 0,
        "rows_inspected_count": preview.get("rows_inspected_count") if isinstance(preview.get("rows_inspected_count"), int) else 0,
        "row_limit_enforced": preview.get("row_limit_enforced") is True,
        "preview_text_inspected_in_memory": preview_text_inspected,
        "one_bounded_real_row_reviewed": row_accounting_exact and file_read_exact and preview_text_inspected,
        "one_real_source_candidate_created": bool(final_candidate and counts_exact and schemas_exact),
    }


def _empty_chain_review() -> dict[str, Any]:
    return {
        "blockers": ["controlled_candidate_chain_not_created"],
        "privacy_issue": False,
        "package_selection_review": {
            "status": "blocked",
            "package_identity_match": False,
            "package_role_match": False,
            "case_id_hint_match": False,
            "row_source_match": False,
            "alternate_package_used": False,
            "alternate_row_source_used": False,
            "directory_enumeration_performed": False,
            "arbitrary_path_accessed": False,
        },
        "candidate_blocker_checks": {},
        "lineage_review": {
            "status": "blocked",
            "stage_count": 0,
            "stages": [],
            "lineage_gap_detected": True,
            "package_identity_match": False,
            "case_id_hint_match": False,
            "candidate_reference_continuity": False,
            "arbitrary_source_substitution": False,
            "alternate_package_used": False,
            "alternate_row_source_used": False,
        },
        "row_preview_schema": None,
        "stage_schemas": {key: None for key in STAGE_SCHEMAS},
        "selected_preview_row_id": None,
        "selected_row_safe_hash": None,
        "final_candidate_id": None,
        "final_candidate_schema": None,
        "safe_metadata": {},
        "approved_evidence_items_jsonl_opened": False,
        "approved_evidence_items_jsonl_rows_parsed": 0,
        "preview_rows_count": 0,
        "rows_inspected_count": 0,
        "row_limit_enforced": True,
        "preview_text_inspected_in_memory": False,
        "one_bounded_real_row_reviewed": False,
        "one_real_source_candidate_created": False,
    }


def _review_declaration_context(context: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    valid = all(context.get(key) == value for key, value in DECLARATION_REQUIRED_VALUES.items())
    preserved = {key: context.get(key) for key in DECLARATION_REQUIRED_VALUES}
    return (
        {
            "status": "reviewed_non_authorizing" if valid else "blocked_non_authorizing",
            "declaration_structurally_present": valid,
            "preserved_context": preserved,
            "authority_independently_validated": False,
            "responsibility_runtime_accepted": False,
            "final_write_authorization_present": False,
        },
        [] if valid else ["human_declaration_context_invalid"],
    )


def _contains_privacy_or_secret(values: list[Any]) -> bool:
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
        "candidate_id",
        "candidate_ref",
        "source_candidate_ref",
        "preview_row_id",
        "source_preview_row_id",
        "evidence_id_hash",
        "preview_hash",
        "revocation_target_ref",
    }:
        return False
    text = value.strip()
    if parent_key == "text_snippet_redacted":
        return bool(
            not text
            or len(text) > row_preview_module.TEXT_SNIPPET_MAX_CHARS
            or _URL_RE.search(text)
            or _EMAIL_RE.search(text)
            or _PHONE_RE.search(text)
            or _SECRET_RE.search(text)
            or _HANDLE_RE.search(text)
            or ":\\" in text
            or "file://" in text.lower()
        )
    return bool(
        _URL_RE.search(text)
        or _EMAIL_RE.search(text)
        or _SECRET_RE.search(text)
        or re.match(r"^[A-Za-z]:[\\/]", text)
        or text.startswith("\\\\")
        or text.lower().startswith("file://")
    )


def _unsafe_true_flags(values: list[Any]) -> list[str]:
    found: list[str] = []
    for value in values:
        _collect_unsafe_true_flags(value, found)
    return _dedupe(found)


def _collect_unsafe_true_flags(value: Any, found: list[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized = str(key).strip().lower()
            if normalized in FALSE_SAFETY_FLAGS and _affirmative(nested):
                found.append(normalized)
            _collect_unsafe_true_flags(nested, found)
    elif isinstance(value, (list, tuple, set)):
        for item in value:
            _collect_unsafe_true_flags(item, found)


def _single_row(container: dict[str, Any], key: str) -> dict[str, Any]:
    rows = container.get(key)
    if not isinstance(rows, list) or len(rows) != 1 or not isinstance(rows[0], dict):
        return {}
    return rows[0]


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _is_safe_opaque_id(value: Any) -> bool:
    return isinstance(value, str) and bool(_OPAQUE_ID_RE.fullmatch(value))


def _safe_output_value(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _scan_sensitive(stripped, parent_key="safe_output"):
        return None
    return stripped[:80]


def _active(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, (str, list, tuple, set, dict)):
        return bool(value)
    return True


def _affirmative(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes"})


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
