from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from app.services.existing_evidenceitem_safe_identity_projection import (
    EVIDENCE_MODEL_CONTRACT_SHA256,
    EVIDENCE_MODEL_QUALIFIED_NAME,
    SAFE_IDENTITY_RECEIPT_SCHEMA,
    validate_existing_evidenceitem_safe_identity_receipt,
)
from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    HANDOFF_CANDIDATE_MODE,
    HANDOFF_CANDIDATE_SCHEMA,
    HANDOFF_CANDIDATE_VERSION,
    OUTPUT_FIELDS as HANDOFF_CANDIDATE_FIELDS,
)


LINK_RECORD_SCHEMA = "sentigraph_governed_decision_existing_evidence_link_v0_1"
LINK_RECORD_VERSION = "0.1"
LINK_CANDIDATE_SCHEMA = (
    "sentigraph_governed_decision_existing_evidence_link_candidate_v0_1"
)
LINK_CANDIDATE_VERSION = "0.1"
LINK_CANDIDATE_MODE = (
    "internal_pure_in_memory_nonpersistent_nonauthorizing_decision_to_"
    "existing_evidence_link_candidate"
)
LINK_RECORD_MODE = (
    "internal_append_only_nonproduction_nonauthorizing_decision_to_"
    "existing_evidence_link"
)
RELATION_TYPE = "governed_decision_audit_context_for_existing_evidence"

DECISION_REFERENCE_FIELDS = (
    "decision_id",
    "audit_receipt_reference",
    "sample_handle",
    "decision_type",
    "decision_status",
    "recorded_at",
)
EVIDENCE_REFERENCE_FIELDS = (
    "case_id",
    "evidence_id",
    "evidence_content_hash",
    "evidence_identity_receipt_reference",
    "evidence_identity_receipt_schema",
    "evidence_model_qualified_name",
    "evidence_model_contract_sha256",
)
DOWNSTREAM_AUTHORIZATION_FIELDS = (
    "authorizes_review_queue_runtime",
    "authorizes_evidence_layer_write",
    "authorizes_trust_upgrade",
    "authorizes_provider_or_b05",
    "authorizes_analysis",
    "authorizes_report",
    "authorizes_production_object",
    "authorizes_public_export_delivery",
)
LINK_CANDIDATE_FIELDS = (
    "schema",
    "version",
    "mode",
    "link_schema",
    "link_id",
    "link_fingerprint_sha256",
    "relation_type",
    "initial_status",
    "decision_reference",
    "evidence_reference",
    "human_authority_receipt_reference",
    "manual_review_responsibility_receipt_reference",
    "rollback_plan_reference",
    "warning_count_acknowledged",
    "lineage_review_status",
    "raw_private_secret_absence_acknowledged",
    "created_at",
    "candidate_only",
    "persisted",
    "human_review_required",
    "no_automatic_trust_upgrade",
    *DOWNSTREAM_AUTHORIZATION_FIELDS,
)

_LOWER_HEX_64_PATTERN = re.compile(r"[0-9a-f]{64}")
_DECISION_ID_PATTERN = re.compile(r"irghrd-[0-9a-f]{32}")
_MAX_OPAQUE_UTF8_BYTES = 512
_CURRENT_SAMPLE_HANDLE = "helldivers2-psn-demo"
_DECISION_STATUS = "recorded_append_only_nonproduction_identity_ready"
_DECISION_TYPES = frozenset(
    {
        "keep_pending_human_review",
        "request_more_governance_review",
    }
)


class GovernedDecisionExistingEvidenceLinkValidationError(ValueError):
    """Raised when a governed decision/evidence link contract is invalid."""

    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise GovernedDecisionExistingEvidenceLinkValidationError(outcome)


def _validate_opaque(value: Any, *, field_name: str) -> str:
    if type(value) is not str or value == "":
        _fail(f"blocked_{field_name}_invalid")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail(f"blocked_{field_name}_invalid")
    if len(encoded) > _MAX_OPAQUE_UTF8_BYTES:
        _fail(f"blocked_{field_name}_invalid")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        _fail(f"blocked_{field_name}_invalid")
    return value


def _validate_utc_seconds(value: Any, *, field_name: str) -> str:
    validated = _validate_opaque(value, field_name=field_name)
    try:
        datetime.strptime(validated, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        _fail(f"blocked_{field_name}_invalid")
    return validated


def _validate_handoff_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, Mapping) or set(candidate) != set(
        HANDOFF_CANDIDATE_FIELDS
    ):
        _fail("blocked_decision_handoff_contract_mismatch")
    if (
        candidate["handoff_candidate_schema"] != HANDOFF_CANDIDATE_SCHEMA
        or candidate["handoff_candidate_version"] != HANDOFF_CANDIDATE_VERSION
        or candidate["handoff_candidate_mode"] != HANDOFF_CANDIDATE_MODE
    ):
        _fail("blocked_decision_handoff_contract_mismatch")
    for field_name in DECISION_REFERENCE_FIELDS:
        _validate_opaque(candidate[field_name], field_name=field_name)
    decision_id = candidate["decision_id"]
    if _DECISION_ID_PATTERN.fullmatch(decision_id) is None:
        _fail("blocked_decision_handoff_identity_mismatch")
    if candidate["audit_receipt_reference"] != (
        f"irghrd-receipt-{decision_id.removeprefix('irghrd-')}"
    ):
        _fail("blocked_decision_handoff_identity_mismatch")
    if (
        candidate["sample_handle"] != _CURRENT_SAMPLE_HANDLE
        or candidate["decision_type"] not in _DECISION_TYPES
        or candidate["decision_status"] != _DECISION_STATUS
    ):
        _fail("blocked_decision_handoff_identity_mismatch")
    _validate_utc_seconds(candidate["recorded_at"], field_name="recorded_at")
    if candidate["candidate_only"] is not True or candidate["persisted"] is not False:
        _fail("blocked_decision_handoff_authority_mismatch")
    if (
        candidate["human_review_required"] is not True
        or candidate["no_automatic_trust_upgrade"] is not True
        or any(candidate[field] is not False for field in DOWNSTREAM_AUTHORIZATION_FIELDS)
    ):
        _fail("blocked_decision_handoff_authority_mismatch")
    return {field: candidate[field] for field in HANDOFF_CANDIDATE_FIELDS}


def _link_fingerprint(
    *,
    decision_id: str,
    audit_receipt_reference: str,
    case_id: str,
    evidence_id: str,
    evidence_content_hash: str,
) -> str:
    material = "\0".join(
        (
            LINK_RECORD_SCHEMA,
            decision_id,
            audit_receipt_reference,
            case_id,
            evidence_id,
            evidence_content_hash,
            RELATION_TYPE,
        )
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def validate_governed_decision_existing_evidence_link_candidate(
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and copy one exact nonauthorizing linkage candidate."""

    if not isinstance(candidate, Mapping) or set(candidate) != set(
        LINK_CANDIDATE_FIELDS
    ):
        _fail("blocked_link_candidate_contract_mismatch")
    if (
        candidate["schema"] != LINK_CANDIDATE_SCHEMA
        or candidate["version"] != LINK_CANDIDATE_VERSION
        or candidate["mode"] != LINK_CANDIDATE_MODE
        or candidate["link_schema"] != LINK_RECORD_SCHEMA
        or candidate["relation_type"] != RELATION_TYPE
        or candidate["initial_status"] != "active"
        or candidate["candidate_only"] is not True
        or candidate["persisted"] is not False
        or candidate["human_review_required"] is not True
        or candidate["no_automatic_trust_upgrade"] is not True
        or any(candidate[field] is not False for field in DOWNSTREAM_AUTHORIZATION_FIELDS)
    ):
        _fail("blocked_link_candidate_contract_mismatch")

    decision_reference = candidate["decision_reference"]
    if not isinstance(decision_reference, Mapping) or set(decision_reference) != set(
        DECISION_REFERENCE_FIELDS
    ):
        _fail("blocked_link_candidate_decision_reference_mismatch")
    for field_name in DECISION_REFERENCE_FIELDS:
        _validate_opaque(decision_reference[field_name], field_name=field_name)
    decision_id = decision_reference["decision_id"]
    if (
        _DECISION_ID_PATTERN.fullmatch(decision_id) is None
        or decision_reference["audit_receipt_reference"]
        != f"irghrd-receipt-{decision_id.removeprefix('irghrd-')}"
        or decision_reference["sample_handle"] != _CURRENT_SAMPLE_HANDLE
        or decision_reference["decision_type"] not in _DECISION_TYPES
        or decision_reference["decision_status"] != _DECISION_STATUS
    ):
        _fail("blocked_link_candidate_decision_reference_mismatch")
    _validate_utc_seconds(
        decision_reference["recorded_at"],
        field_name="recorded_at",
    )

    evidence_reference = candidate["evidence_reference"]
    if not isinstance(evidence_reference, Mapping) or set(evidence_reference) != set(
        EVIDENCE_REFERENCE_FIELDS
    ):
        _fail("blocked_link_candidate_evidence_reference_mismatch")
    for field_name in (
        "case_id",
        "evidence_id",
        "evidence_identity_receipt_reference",
        "evidence_identity_receipt_schema",
        "evidence_model_qualified_name",
        "evidence_model_contract_sha256",
    ):
        _validate_opaque(evidence_reference[field_name], field_name=field_name)
    if (
        evidence_reference["evidence_identity_receipt_schema"]
        != SAFE_IDENTITY_RECEIPT_SCHEMA
        or evidence_reference["evidence_model_qualified_name"]
        != EVIDENCE_MODEL_QUALIFIED_NAME
        or evidence_reference["evidence_model_contract_sha256"]
        != EVIDENCE_MODEL_CONTRACT_SHA256
        or type(evidence_reference["evidence_content_hash"]) is not str
        or _LOWER_HEX_64_PATTERN.fullmatch(
            evidence_reference["evidence_content_hash"]
        )
        is None
    ):
        _fail("blocked_link_candidate_evidence_reference_mismatch")

    for field_name in (
        "human_authority_receipt_reference",
        "manual_review_responsibility_receipt_reference",
        "rollback_plan_reference",
    ):
        _validate_opaque(candidate[field_name], field_name=field_name)
    if (
        candidate["warning_count_acknowledged"] is not True
        or candidate["lineage_review_status"] != "verified"
        or candidate["raw_private_secret_absence_acknowledged"] is not True
    ):
        _fail("blocked_link_candidate_governance_mismatch")
    _validate_utc_seconds(candidate["created_at"], field_name="created_at")

    expected_fingerprint = _link_fingerprint(
        decision_id=decision_id,
        audit_receipt_reference=decision_reference["audit_receipt_reference"],
        case_id=evidence_reference["case_id"],
        evidence_id=evidence_reference["evidence_id"],
        evidence_content_hash=evidence_reference["evidence_content_hash"],
    )
    if (
        candidate["link_fingerprint_sha256"] != expected_fingerprint
        or candidate["link_id"] != f"gdel-{expected_fingerprint[:32]}"
    ):
        _fail("blocked_link_candidate_fingerprint_mismatch")
    return {field: candidate[field] for field in LINK_CANDIDATE_FIELDS}


def build_governed_decision_existing_evidence_link_candidate(
    decision_handoff_candidate: Mapping[str, Any],
    evidence_identity_receipt: Mapping[str, Any],
    *,
    human_authority_receipt_reference: str,
    manual_review_responsibility_receipt_reference: str,
    rollback_plan_reference: str,
    created_at: str,
    warning_count_acknowledged: bool,
    lineage_review_status: str,
    raw_private_secret_absence_acknowledged: bool,
) -> dict[str, Any]:
    """Build one pure candidate without reading or mutating repository state."""

    handoff = _validate_handoff_candidate(decision_handoff_candidate)
    try:
        identity_receipt = validate_existing_evidenceitem_safe_identity_receipt(
            evidence_identity_receipt
        )
    except (TypeError, ValueError) as exc:
        _fail(f"blocked_safe_identity_receipt:{exc}")
    for field_name, value in (
        ("human_authority_receipt_reference", human_authority_receipt_reference),
        (
            "manual_review_responsibility_receipt_reference",
            manual_review_responsibility_receipt_reference,
        ),
        ("rollback_plan_reference", rollback_plan_reference),
    ):
        _validate_opaque(value, field_name=field_name)
    _validate_utc_seconds(created_at, field_name="created_at")
    if (
        warning_count_acknowledged is not True
        or lineage_review_status != "verified"
        or raw_private_secret_absence_acknowledged is not True
    ):
        _fail("blocked_link_candidate_governance_mismatch")

    decision_reference = {
        field: handoff[field] for field in DECISION_REFERENCE_FIELDS
    }
    evidence_reference = {
        "case_id": identity_receipt["case_id"],
        "evidence_id": identity_receipt["evidence_id"],
        "evidence_content_hash": identity_receipt["content_hash"],
        "evidence_identity_receipt_reference": identity_receipt[
            "receipt_reference"
        ],
        "evidence_identity_receipt_schema": identity_receipt["schema"],
        "evidence_model_qualified_name": identity_receipt[
            "evidence_model_qualified_name"
        ],
        "evidence_model_contract_sha256": identity_receipt[
            "evidence_model_contract_sha256"
        ],
    }
    fingerprint = _link_fingerprint(
        decision_id=decision_reference["decision_id"],
        audit_receipt_reference=decision_reference["audit_receipt_reference"],
        case_id=evidence_reference["case_id"],
        evidence_id=evidence_reference["evidence_id"],
        evidence_content_hash=evidence_reference["evidence_content_hash"],
    )
    values: dict[str, Any] = {
        "schema": LINK_CANDIDATE_SCHEMA,
        "version": LINK_CANDIDATE_VERSION,
        "mode": LINK_CANDIDATE_MODE,
        "link_schema": LINK_RECORD_SCHEMA,
        "link_id": f"gdel-{fingerprint[:32]}",
        "link_fingerprint_sha256": fingerprint,
        "relation_type": RELATION_TYPE,
        "initial_status": "active",
        "decision_reference": decision_reference,
        "evidence_reference": evidence_reference,
        "human_authority_receipt_reference": human_authority_receipt_reference,
        "manual_review_responsibility_receipt_reference": (
            manual_review_responsibility_receipt_reference
        ),
        "rollback_plan_reference": rollback_plan_reference,
        "warning_count_acknowledged": True,
        "lineage_review_status": "verified",
        "raw_private_secret_absence_acknowledged": True,
        "created_at": created_at,
        "candidate_only": True,
        "persisted": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in DOWNSTREAM_AUTHORIZATION_FIELDS},
    }
    candidate = {field: values[field] for field in LINK_CANDIDATE_FIELDS}
    return validate_governed_decision_existing_evidence_link_candidate(candidate)
