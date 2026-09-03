from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from typing import Any

from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate,
)


POOL_REVIEW_SUMMARY_SCHEMA = (
    "sentigraph_governed_decision_existing_evidence_target_pool_review_summary_v0_1"
)
POOL_REVIEW_SUMMARY_VERSION = "0.1"
POOL_REVIEW_SUMMARY_MODE = (
    "mainline_adjudicated_safe_complete_existing_evidence_target_pool_review"
)
OUTCOME_RECEIPT_SCHEMA = (
    "sentigraph_governed_decision_existing_evidence_target_selection_"
    "outcome_receipt_v0_1"
)
OUTCOME_RECEIPT_VERSION = "0.1"
OUTCOME_RECEIPT_MODE = (
    "internal_pure_in_memory_nonpersistent_nonauthorizing_existing_evidence_"
    "target_selection_outcome_receipt"
)
OUTCOME = "NO_SELECTABLE_EXISTING_TARGET_AFTER_COMPLETE_REVIEW"
SELECTION_SCOPE = "CURRENT_CASESTORE_EXISTING_EVIDENCE"
SELECTION_EXHAUSTION_SCOPE = (
    "CURRENT_CASESTORE_EXISTING_EVIDENCE_UNDER_CURRENT_SUBJECT_PRIVACY_AND_"
    "ELIGIBILITY_CONTRACTS"
)
MAINLINE_ADJUDICATION_RECEIPT_REFERENCE = (
    "SENTIGRAPH_MAINLINE_NLO2_NO_SELECTABLE_EXISTING_TARGET_AFTER_COMPLETE_"
    "REVIEW_ADJUDICATION_V0_1"
)

POOL_REVIEW_SUMMARY_FIELDS = (
    "schema",
    "version",
    "mode",
    "mainline_adjudication_receipt_reference",
    "decision_subject",
    "review_scope",
    "complete_existing_evidence_bearing_case_count",
    "complete_existing_evidenceitem_count",
    "eligible_evidenceitem_count",
    "ineligible_evidenceitem_count",
    "reviewed_existing_evidence_bearing_case_count",
    "reviewed_existing_evidenceitem_count",
    "selectable_existing_target_count",
    "target_pool_complete",
    "selection_not_attempted",
    "selection_pending",
    "selection_exhausted",
    "privacy_blocked_unadjudicated_present",
    "privacy_blocked_unadjudicated_case_ids",
    "privacy_blocked_target_match_claimed",
    "privacy_blocked_target_mismatch_claimed",
    "operational_failure",
    "selected_case_id",
    "selected_evidence_id",
    "selected_evidence_content_hash",
    "final_linkage_target_selected",
    "accepted_result_bindings",
)
ACCEPTED_RESULT_BINDING_FIELDS = (
    "role",
    "filename",
    "bytes",
    "sha256",
    "terminal_classification",
    "mainline_accepted",
)
DECISION_REFERENCE_FIELDS = (
    "decision_id",
    "audit_receipt_reference",
    "sample_handle",
    "decision_type",
    "decision_status",
    "recorded_at",
)
OUTPUT_FIELDS = (
    "schema",
    "version",
    "mode",
    "outcome_receipt_reference",
    "outcome_fingerprint_sha256",
    "outcome",
    "selection_scope",
    "decision_reference",
    "mainline_adjudication_receipt_reference",
    "decision_subject",
    "accepted_result_bindings",
    "complete_existing_evidence_bearing_case_count",
    "complete_existing_evidenceitem_count",
    "eligible_evidenceitem_count",
    "ineligible_evidenceitem_count",
    "reviewed_existing_evidence_bearing_case_count",
    "reviewed_existing_evidenceitem_count",
    "selectable_existing_target_count",
    "target_pool_complete",
    "selection_not_attempted",
    "selection_pending",
    "selection_exhausted",
    "selection_exhaustion_scope",
    "privacy_blocked_unadjudicated_present",
    "privacy_blocked_unadjudicated_case_count",
    "privacy_blocked_unadjudicated_case_ids",
    "privacy_blocked_target_match_claimed",
    "privacy_blocked_target_mismatch_claimed",
    "operational_failure",
    "selected_case_id",
    "selected_evidence_id",
    "selected_evidence_content_hash",
    "final_linkage_target_selected",
    "decision_handoff_validated",
    "pool_review_summary_shape_validated",
    "accepted_result_bindings_shape_validated",
    "accepted_result_files_verified_by_builder",
    "mainline_adjudication_binding_shape_validated",
    "mainline_authority_validated_by_builder",
    "candidate_only",
    "persisted",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "truth_support_contradiction_verification_or_trust_claimed",
    "linkage_candidate_created",
    "linkage_write_authorized",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
    "production_object_enabled",
    "public_export_delivery_enabled",
    "new_evidence_acquisition_authorized",
)

_COUNT_FIELDS = (
    "complete_existing_evidence_bearing_case_count",
    "complete_existing_evidenceitem_count",
    "eligible_evidenceitem_count",
    "ineligible_evidenceitem_count",
    "reviewed_existing_evidence_bearing_case_count",
    "reviewed_existing_evidenceitem_count",
    "selectable_existing_target_count",
)
_BOOLEAN_FIELDS = (
    "target_pool_complete",
    "selection_not_attempted",
    "selection_pending",
    "selection_exhausted",
    "privacy_blocked_unadjudicated_present",
    "privacy_blocked_target_match_claimed",
    "privacy_blocked_target_mismatch_claimed",
    "operational_failure",
    "final_linkage_target_selected",
)
_RESULT_ROLE_PATTERN = re.compile(r"[A-Z][A-Z0-9_]{0,63}")
_RESULT_FILENAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,254}\.json")
_LOWERHEX64_PATTERN = re.compile(r"[0-9a-f]{64}")
_TERMINAL_PATTERN = re.compile(r"[A-Z][A-Z0-9_]{0,199}")
_SAFE_CASE_ID_PATTERN = re.compile(r"[a-z][a-z0-9_]{0,63}")


class GovernedDecisionExistingEvidenceTargetSelectionOutcomeValidationError(
    ValueError
):
    """Raised when a safe target-pool summary cannot form an outcome receipt."""

    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise GovernedDecisionExistingEvidenceTargetSelectionOutcomeValidationError(
        outcome
    )


def _validate_result_bindings(value: Any) -> list[dict[str, Any]]:
    if type(value) is not list or not 1 <= len(value) <= 16:
        _fail("blocked_accepted_result_bindings_contract_mismatch")

    validated: list[dict[str, Any]] = []
    roles: list[str] = []
    filenames: list[str] = []
    for record in value:
        if not isinstance(record, Mapping) or set(record) != set(
            ACCEPTED_RESULT_BINDING_FIELDS
        ):
            _fail("blocked_accepted_result_bindings_contract_mismatch")

        role = record["role"]
        filename = record["filename"]
        byte_count = record["bytes"]
        sha256 = record["sha256"]
        terminal = record["terminal_classification"]
        mainline_accepted = record["mainline_accepted"]
        if (
            type(role) is not str
            or _RESULT_ROLE_PATTERN.fullmatch(role) is None
            or type(filename) is not str
            or _RESULT_FILENAME_PATTERN.fullmatch(filename) is None
            or ".." in filename
            or "/" in filename
            or "\\" in filename
            or type(byte_count) is not int
            or byte_count <= 0
            or type(sha256) is not str
            or _LOWERHEX64_PATTERN.fullmatch(sha256) is None
            or type(terminal) is not str
            or _TERMINAL_PATTERN.fullmatch(terminal) is None
            or mainline_accepted is not True
        ):
            _fail("blocked_accepted_result_bindings_contract_mismatch")

        roles.append(role)
        filenames.append(filename)
        validated.append(
            {
                field: record[field]
                for field in ACCEPTED_RESULT_BINDING_FIELDS
            }
        )

    if (
        roles != sorted(roles)
        or len(set(roles)) != len(roles)
        or len(set(filenames)) != len(filenames)
    ):
        _fail("blocked_accepted_result_bindings_contract_mismatch")
    return validated


def _validate_pool_review_summary(
    summary: Mapping[str, Any],
    decision_subject: str,
) -> tuple[list[str], list[dict[str, Any]]]:
    if not isinstance(summary, Mapping) or set(summary) != set(
        POOL_REVIEW_SUMMARY_FIELDS
    ):
        _fail("blocked_pool_review_summary_contract_mismatch")

    if (
        summary["schema"] != POOL_REVIEW_SUMMARY_SCHEMA
        or summary["version"] != POOL_REVIEW_SUMMARY_VERSION
        or summary["mode"] != POOL_REVIEW_SUMMARY_MODE
        or summary["mainline_adjudication_receipt_reference"]
        != MAINLINE_ADJUDICATION_RECEIPT_REFERENCE
        or summary["review_scope"] != SELECTION_EXHAUSTION_SCOPE
    ):
        _fail("blocked_pool_review_summary_contract_mismatch")
    if type(summary["decision_subject"]) is not str:
        _fail("blocked_pool_review_summary_contract_mismatch")
    if summary["decision_subject"] != decision_subject:
        _fail("blocked_decision_subject_mismatch")

    if any(
        type(summary[field]) is not int or summary[field] < 0
        for field in _COUNT_FIELDS
    ):
        _fail("blocked_pool_review_summary_count_mismatch")
    if any(type(summary[field]) is not bool for field in _BOOLEAN_FIELDS):
        _fail("blocked_pool_review_summary_contract_mismatch")

    if (
        summary["eligible_evidenceitem_count"]
        + summary["ineligible_evidenceitem_count"]
        != summary["complete_existing_evidenceitem_count"]
        or summary["reviewed_existing_evidenceitem_count"]
        != summary["complete_existing_evidenceitem_count"]
        or summary["reviewed_existing_evidence_bearing_case_count"]
        != summary["complete_existing_evidence_bearing_case_count"]
    ):
        _fail("blocked_pool_review_summary_count_mismatch")

    if (
        summary["target_pool_complete"] is not True
        or summary["selection_not_attempted"] is not False
        or summary["selection_pending"] is not False
        or summary["selection_exhausted"] is not True
        or summary["operational_failure"] is not False
        or summary["selectable_existing_target_count"] != 0
        or summary["selected_case_id"] is not None
        or summary["selected_evidence_id"] is not None
        or summary["selected_evidence_content_hash"] is not None
        or summary["final_linkage_target_selected"] is not False
    ):
        _fail("blocked_pool_review_summary_state_mismatch")

    case_ids = summary["privacy_blocked_unadjudicated_case_ids"]
    if (
        type(case_ids) is not list
        or len(case_ids) > 20
        or any(
            type(case_id) is not str
            or _SAFE_CASE_ID_PATTERN.fullmatch(case_id) is None
            for case_id in case_ids
        )
        or case_ids != sorted(case_ids)
        or len(set(case_ids)) != len(case_ids)
        or summary["privacy_blocked_unadjudicated_present"] is not bool(case_ids)
        or summary["privacy_blocked_target_match_claimed"] is not False
        or summary["privacy_blocked_target_mismatch_claimed"] is not False
    ):
        _fail("blocked_privacy_contract_mismatch")

    bindings = _validate_result_bindings(summary["accepted_result_bindings"])
    return [case_id for case_id in case_ids], bindings


def _fingerprint(values: Mapping[str, Any]) -> str:
    material = {
        key: values[key]
        for key in values
        if key not in {"outcome_receipt_reference", "outcome_fingerprint_sha256"}
    }
    canonical = json.dumps(
        material,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def build_governed_decision_existing_evidence_target_selection_outcome(
    decision_audit_projection: Mapping[str, Any],
    pool_review_summary: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one deterministic, nonpersistent, nonauthorizing outcome receipt."""

    handoff = (
        build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate(
            decision_audit_projection
        )
    )
    case_ids, bindings = _validate_pool_review_summary(
        pool_review_summary,
        handoff["sample_handle"],
    )
    decision_reference = {
        field: handoff[field] for field in DECISION_REFERENCE_FIELDS
    }
    values: dict[str, Any] = {
        "schema": OUTCOME_RECEIPT_SCHEMA,
        "version": OUTCOME_RECEIPT_VERSION,
        "mode": OUTCOME_RECEIPT_MODE,
        "outcome_receipt_reference": "",
        "outcome_fingerprint_sha256": "",
        "outcome": OUTCOME,
        "selection_scope": SELECTION_SCOPE,
        "decision_reference": decision_reference,
        "mainline_adjudication_receipt_reference": (
            MAINLINE_ADJUDICATION_RECEIPT_REFERENCE
        ),
        "decision_subject": handoff["sample_handle"],
        "accepted_result_bindings": bindings,
        "complete_existing_evidence_bearing_case_count": pool_review_summary[
            "complete_existing_evidence_bearing_case_count"
        ],
        "complete_existing_evidenceitem_count": pool_review_summary[
            "complete_existing_evidenceitem_count"
        ],
        "eligible_evidenceitem_count": pool_review_summary[
            "eligible_evidenceitem_count"
        ],
        "ineligible_evidenceitem_count": pool_review_summary[
            "ineligible_evidenceitem_count"
        ],
        "reviewed_existing_evidence_bearing_case_count": pool_review_summary[
            "reviewed_existing_evidence_bearing_case_count"
        ],
        "reviewed_existing_evidenceitem_count": pool_review_summary[
            "reviewed_existing_evidenceitem_count"
        ],
        "selectable_existing_target_count": 0,
        "target_pool_complete": True,
        "selection_not_attempted": False,
        "selection_pending": False,
        "selection_exhausted": True,
        "selection_exhaustion_scope": SELECTION_EXHAUSTION_SCOPE,
        "privacy_blocked_unadjudicated_present": bool(case_ids),
        "privacy_blocked_unadjudicated_case_count": len(case_ids),
        "privacy_blocked_unadjudicated_case_ids": case_ids,
        "privacy_blocked_target_match_claimed": False,
        "privacy_blocked_target_mismatch_claimed": False,
        "operational_failure": False,
        "selected_case_id": None,
        "selected_evidence_id": None,
        "selected_evidence_content_hash": None,
        "final_linkage_target_selected": False,
        "decision_handoff_validated": True,
        "pool_review_summary_shape_validated": True,
        "accepted_result_bindings_shape_validated": True,
        "accepted_result_files_verified_by_builder": False,
        "mainline_adjudication_binding_shape_validated": True,
        "mainline_authority_validated_by_builder": False,
        "candidate_only": True,
        "persisted": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "truth_support_contradiction_verification_or_trust_claimed": False,
        "linkage_candidate_created": False,
        "linkage_write_authorized": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
        "production_object_enabled": False,
        "public_export_delivery_enabled": False,
        "new_evidence_acquisition_authorized": False,
    }
    fingerprint = _fingerprint(values)
    values["outcome_fingerprint_sha256"] = fingerprint
    values["outcome_receipt_reference"] = f"gdetso-{fingerprint[:32]}"
    return {field: values[field] for field in OUTPUT_FIELDS}
