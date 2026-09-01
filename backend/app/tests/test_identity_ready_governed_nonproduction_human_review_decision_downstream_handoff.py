from __future__ import annotations

from typing import Any

import pytest

from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    HANDOFF_CANDIDATE_MODE,
    HANDOFF_CANDIDATE_SCHEMA,
    HANDOFF_CANDIDATE_VERSION,
    IDENTITY_FIELDS,
    INPUT_FIELDS,
    OUTPUT_FIELDS,
    IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError,
    build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate,
)


DECISION_SUFFIX = "0123456789abcdef0123456789abcdef"


def _projection() -> dict[str, Any]:
    return {
        "decision_id": f"irghrd-{DECISION_SUFFIX}",
        "audit_receipt_reference": f"irghrd-receipt-{DECISION_SUFFIX}",
        "sample_handle": "helldivers2-psn-demo",
        "decision_type": "keep_pending_human_review",
        "decision_status": "recorded_append_only_nonproduction_identity_ready",
        "recorded_at": "2026-08-31T12:34:56Z",
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
    }


def _build(projection: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate(
        projection or _projection()
    )


def test_valid_strict_projection_builds_one_exact_nonauthorizing_candidate() -> None:
    projection = _projection()

    candidate = _build(projection)

    assert tuple(candidate) == OUTPUT_FIELDS
    assert candidate["handoff_candidate_schema"] == HANDOFF_CANDIDATE_SCHEMA
    assert candidate["handoff_candidate_version"] == HANDOFF_CANDIDATE_VERSION
    assert candidate["handoff_candidate_mode"] == HANDOFF_CANDIDATE_MODE
    assert {field: candidate[field] for field in IDENTITY_FIELDS} == {
        field: projection[field] for field in IDENTITY_FIELDS
    }
    assert candidate["candidate_only"] is True
    assert candidate["persisted"] is False
    assert candidate["human_review_required"] is True
    assert candidate["no_automatic_trust_upgrade"] is True


def test_every_downstream_authorization_flag_is_frozen_false() -> None:
    candidate = _build()

    authorization_fields = (
        "authorizes_review_queue_runtime",
        "authorizes_evidence_layer_write",
        "authorizes_trust_upgrade",
        "authorizes_provider_or_b05",
        "authorizes_analysis",
        "authorizes_report",
        "authorizes_production_object",
        "authorizes_public_export_delivery",
    )
    assert all(candidate[field] is False for field in authorization_fields)


@pytest.mark.parametrize("missing_field", sorted(INPUT_FIELDS))
def test_each_missing_required_input_field_fails_closed(missing_field: str) -> None:
    projection = _projection()
    del projection[missing_field]

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection)


def test_unexpected_input_field_fails_closed() -> None:
    projection = {**_projection(), "unexpected": "value"}

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection)


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("human_review_required", False),
        ("no_automatic_trust_upgrade", False),
        ("production_object_enabled", True),
        ("review_queue_runtime_enabled", True),
        ("evidence_layer_write_performed", True),
        ("provider_or_b05_called", True),
        ("analysis_triggered", True),
        ("report_triggered", True),
    ],
)
def test_authority_semantic_mismatch_fails_closed(
    field: str,
    invalid_value: bool,
) -> None:
    projection = {**_projection(), field: invalid_value}

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection)


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("decision_id", 7),
        ("recorded_at", True),
        ("human_review_required", 1),
        ("review_queue_runtime_enabled", 0),
    ],
)
def test_string_and_boolean_coercion_is_rejected(
    field: str,
    invalid_value: object,
) -> None:
    projection = {**_projection(), field: invalid_value}

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection)


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("decision_id", "not-a-decision-id"),
        ("audit_receipt_reference", "irghrd-receipt-wrong"),
        ("sample_handle", "another-sample"),
        ("decision_type", "approve_production"),
        ("decision_status", "approved"),
        ("recorded_at", "not-a-timestamp"),
    ],
)
def test_invalid_safe_identity_semantics_fail_closed(
    field: str,
    invalid_value: str,
) -> None:
    projection = {**_projection(), field: invalid_value}

    with pytest.raises(
        IdentityReadyGovernedNonproductionHumanReviewDecisionDownstreamHandoffValidationError
    ):
        _build(projection)


def test_output_contains_no_protected_or_downstream_payload_fields() -> None:
    candidate = _build()
    prohibited_fields = {
        "raw_ledger_row",
        "binding_hash",
        "review_subject_binding_safe_hash",
        "decision_canonical_hash",
        "input_hash",
        "credentials",
        "private_identity",
        "raw_evidence",
        "evidence_item",
        "review_queue_item",
        "provider_payload",
    }

    assert prohibited_fields.isdisjoint(candidate)


def test_output_is_deterministic_and_does_not_mutate_input() -> None:
    projection = _projection()
    original = dict(projection)

    first = _build(projection)
    second = _build(projection)

    assert first == second
    assert first is not second
    assert projection == original
