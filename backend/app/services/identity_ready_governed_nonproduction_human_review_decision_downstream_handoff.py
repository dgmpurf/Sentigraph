from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import datetime
from typing import Any


HANDOFF_CANDIDATE_SCHEMA = (
    "sentigraph_identity_ready_governed_nonproduction_human_review_"
    "decision_downstream_handoff_candidate_v0_1"
)
HANDOFF_CANDIDATE_VERSION = "0.1"
HANDOFF_CANDIDATE_MODE = (
    "internal_pure_in_memory_nonpersistent_nonauthorizing_downstream_"
    "handoff_candidate"
)

INPUT_FIELDS = frozenset(
    {
        "decision_id",
        "audit_receipt_reference",
        "sample_handle",
        "decision_type",
        "decision_status",
        "recorded_at",
        "human_review_required",
        "no_automatic_trust_upgrade",
        "production_object_enabled",
        "review_queue_runtime_enabled",
        "evidence_layer_write_performed",
        "provider_or_b05_called",
        "analysis_triggered",
        "report_triggered",
    }
)
IDENTITY_FIELDS = (
    "decision_id",
    "audit_receipt_reference",
    "sample_handle",
    "decision_type",
    "decision_status",
    "recorded_at",
)
OUTPUT_FIELDS = (
    "handoff_candidate_schema",
    "handoff_candidate_version",
    "handoff_candidate_mode",
    *IDENTITY_FIELDS,
    "candidate_only",
    "persisted",
    "authorizes_review_queue_runtime",
    "authorizes_evidence_layer_write",
    "authorizes_trust_upgrade",
    "authorizes_provider_or_b05",
    "authorizes_analysis",
    "authorizes_report",
    "authorizes_production_object",
    "authorizes_public_export_delivery",
    "human_review_required",
    "no_automatic_trust_upgrade",
)

_DECISION_ID_PATTERN = re.compile(r"irghrd-[0-9a-f]{32}")
_DECISION_TYPES = frozenset(
    {
        "keep_pending_human_review",
        "request_more_governance_review",
    }
)
_DECISION_STATUS = "recorded_append_only_nonproduction_identity_ready"
_SAMPLE_HANDLE = "helldivers2-psn-demo"
_TRUE_INPUT_FIELDS = (
    "human_review_required",
    "no_automatic_trust_upgrade",
)
_FALSE_INPUT_FIELDS = (
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
)


class IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError(
    ValueError
):
    """Raised when a safe projection cannot form a non-authorizing candidate."""

    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError(
        outcome
    )


def _validate_projection(projection: Mapping[str, Any]) -> None:
    if not isinstance(projection, Mapping) or set(projection) != INPUT_FIELDS:
        _fail("blocked_safe_projection_contract_mismatch")

    if any(type(projection[field]) is not str for field in IDENTITY_FIELDS):
        _fail("blocked_safe_projection_contract_mismatch")
    if any(
        type(projection[field]) is not bool
        for field in (*_TRUE_INPUT_FIELDS, *_FALSE_INPUT_FIELDS)
    ):
        _fail("blocked_safe_projection_contract_mismatch")

    decision_id = projection["decision_id"]
    if _DECISION_ID_PATTERN.fullmatch(decision_id) is None:
        _fail("blocked_safe_projection_identity_mismatch")
    expected_suffix = decision_id.removeprefix("irghrd-")
    if (
        projection["audit_receipt_reference"]
        != f"irghrd-receipt-{expected_suffix}"
        or projection["sample_handle"] != _SAMPLE_HANDLE
        or projection["decision_type"] not in _DECISION_TYPES
        or projection["decision_status"] != _DECISION_STATUS
    ):
        _fail("blocked_safe_projection_identity_mismatch")

    try:
        datetime.strptime(projection["recorded_at"], "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        _fail("blocked_safe_projection_identity_mismatch")

    if any(projection[field] is not True for field in _TRUE_INPUT_FIELDS) or any(
        projection[field] is not False for field in _FALSE_INPUT_FIELDS
    ):
        _fail("blocked_safe_projection_authority_mismatch")


def build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate(
    projection: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one pure, nonpersistent candidate from a strict safe projection."""

    _validate_projection(projection)
    values: dict[str, Any] = {
        "handoff_candidate_schema": HANDOFF_CANDIDATE_SCHEMA,
        "handoff_candidate_version": HANDOFF_CANDIDATE_VERSION,
        "handoff_candidate_mode": HANDOFF_CANDIDATE_MODE,
        **{field: projection[field] for field in IDENTITY_FIELDS},
        "candidate_only": True,
        "persisted": False,
        "authorizes_review_queue_runtime": False,
        "authorizes_evidence_layer_write": False,
        "authorizes_trust_upgrade": False,
        "authorizes_provider_or_b05": False,
        "authorizes_analysis": False,
        "authorizes_report": False,
        "authorizes_production_object": False,
        "authorizes_public_export_delivery": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    return {field: values[field] for field in OUTPUT_FIELDS}
