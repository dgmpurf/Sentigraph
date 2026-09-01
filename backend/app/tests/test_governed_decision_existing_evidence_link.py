from __future__ import annotations

from copy import deepcopy
from types import SimpleNamespace
from typing import Any

import pytest

from app.schemas.evidence import EvidenceItem
from app.services import governed_decision_existing_evidence_link as service
from app.services.existing_evidenceitem_safe_identity_projection import (
    project_existing_evidenceitem_safe_identity_receipt,
)
from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate,
)


DECISION_SUFFIX = "0123456789abcdef0123456789abcdef"
CASE_ID = "case-synthetic-001"
EVIDENCE_ID = "evidence-synthetic-001"
CONTENT_HASH = "a" * 64


class _FakeCaseRepository:
    def __init__(self, case_id: str) -> None:
        self.case = SimpleNamespace(
            evidence_items=[
                EvidenceItem(
                    case_id=case_id,
                    evidence_id=EVIDENCE_ID,
                    content_hash=CONTENT_HASH,
                    body_text="raw synthetic body",
                )
            ]
        )

    def get_case(self, _case_id: str) -> object:
        return self.case


def _handoff(*, suffix: str = DECISION_SUFFIX) -> dict[str, Any]:
    projection = {
        "decision_id": f"irghrd-{suffix}",
        "audit_receipt_reference": f"irghrd-receipt-{suffix}",
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
    return build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate(
        projection
    )


def _identity_receipt(*, case_id: str = CASE_ID) -> dict[str, Any]:
    return project_existing_evidenceitem_safe_identity_receipt(
        _FakeCaseRepository(case_id),
        case_id,
        EVIDENCE_ID,
    )


def _build(
    handoff: dict[str, Any] | None = None,
    receipt: dict[str, Any] | None = None,
    **overrides: Any,
) -> dict[str, Any]:
    arguments: dict[str, Any] = {
        "human_authority_receipt_reference": "human-authority-receipt-001",
        "manual_review_responsibility_receipt_reference": (
            "manual-review-responsibility-001"
        ),
        "rollback_plan_reference": "append-only-revocation-plan-v0-1",
        "created_at": "2026-09-02T00:00:00Z",
        "warning_count_acknowledged": True,
        "lineage_review_status": "verified",
        "raw_private_secret_absence_acknowledged": True,
    }
    arguments.update(overrides)
    return service.build_governed_decision_existing_evidence_link_candidate(
        handoff or _handoff(),
        receipt or _identity_receipt(),
        **arguments,
    )


def test_builds_one_pure_nonauthorizing_link_candidate() -> None:
    candidate = _build()

    assert tuple(candidate) == service.LINK_CANDIDATE_FIELDS
    assert candidate["schema"] == service.LINK_CANDIDATE_SCHEMA
    assert candidate["link_schema"] == service.LINK_RECORD_SCHEMA
    assert candidate["relation_type"] == service.RELATION_TYPE
    assert candidate["decision_reference"]["decision_id"] == (
        f"irghrd-{DECISION_SUFFIX}"
    )
    assert candidate["evidence_reference"]["case_id"] == CASE_ID
    assert candidate["evidence_reference"]["evidence_id"] == EVIDENCE_ID
    assert candidate["evidence_reference"]["evidence_content_hash"] == CONTENT_HASH
    assert candidate["candidate_only"] is True
    assert candidate["persisted"] is False
    assert candidate["human_review_required"] is True
    assert candidate["no_automatic_trust_upgrade"] is True
    assert all(
        candidate[field] is False
        for field in service.DOWNSTREAM_AUTHORIZATION_FIELDS
    )


def test_corrected_identity_uses_case_id_and_model_contract_not_fake_schema() -> None:
    candidate = _build()
    evidence = candidate["evidence_reference"]

    assert "evidence_schema" not in evidence
    assert evidence["evidence_model_qualified_name"] == (
        "app.schemas.evidence.EvidenceItem"
    )
    assert evidence["evidence_model_contract_sha256"] == (
        "7a3d5c188856087d6b1a42963c2be196d9a15eb574e554ce9351ca235eec6033"
    )
    assert evidence["evidence_identity_receipt_schema"] == (
        "sentigraph_existing_evidenceitem_safe_identity_receipt_v0_1"
    )


def test_fingerprint_binds_case_decision_evidence_hash_and_relation() -> None:
    first = _build()
    second_case = _build(receipt=_identity_receipt(case_id="case-synthetic-002"))
    second_decision = _build(
        handoff=_handoff(suffix="fedcba9876543210fedcba9876543210")
    )

    assert first["link_fingerprint_sha256"] != second_case[
        "link_fingerprint_sha256"
    ]
    assert first["link_fingerprint_sha256"] != second_decision[
        "link_fingerprint_sha256"
    ]
    assert first["link_id"] == (
        f"gdel-{first['link_fingerprint_sha256'][:32]}"
    )


def test_builder_is_deterministic_and_does_not_mutate_inputs() -> None:
    handoff = _handoff()
    receipt = _identity_receipt()
    original_handoff = deepcopy(handoff)
    original_receipt = deepcopy(receipt)

    first = _build(handoff, receipt)
    second = _build(handoff, receipt)

    assert first == second
    assert first is not second
    assert handoff == original_handoff
    assert receipt == original_receipt


def test_validator_accepts_reordered_keys_but_rejects_contract_drift() -> None:
    candidate = _build()
    reordered = dict(reversed(list(candidate.items())))

    validated = service.validate_governed_decision_existing_evidence_link_candidate(
        reordered
    )

    assert tuple(validated) == service.LINK_CANDIDATE_FIELDS
    with pytest.raises(service.GovernedDecisionExistingEvidenceLinkValidationError):
        service.validate_governed_decision_existing_evidence_link_candidate(
            {**candidate, "unexpected": True}
        )


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("warning_count_acknowledged", False),
        ("lineage_review_status", "pending"),
        ("raw_private_secret_absence_acknowledged", False),
        ("human_authority_receipt_reference", ""),
        ("created_at", "not-a-timestamp"),
    ],
)
def test_governance_mismatch_fails_closed(field: str, invalid_value: object) -> None:
    with pytest.raises(service.GovernedDecisionExistingEvidenceLinkValidationError):
        _build(**{field: invalid_value})


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("sample_handle", "another-sample"),
        ("decision_type", "approve_trust"),
        ("decision_status", "approved"),
        ("audit_receipt_reference", "irghrd-receipt-wrong"),
    ],
)
def test_forged_decision_handoff_identity_fails_closed(
    field: str,
    invalid_value: str,
) -> None:
    handoff = {**_handoff(), field: invalid_value}

    with pytest.raises(service.GovernedDecisionExistingEvidenceLinkValidationError):
        _build(handoff=handoff)


def test_forged_safe_receipt_reference_fails_closed() -> None:
    receipt = {**_identity_receipt(), "receipt_reference": "eir-wrong"}

    with pytest.raises(service.GovernedDecisionExistingEvidenceLinkValidationError):
        _build(receipt=receipt)


def test_non_string_evidence_hash_fails_with_bounded_validation_error() -> None:
    candidate = deepcopy(_build())
    candidate["evidence_reference"]["evidence_content_hash"] = 7

    with pytest.raises(service.GovernedDecisionExistingEvidenceLinkValidationError):
        service.validate_governed_decision_existing_evidence_link_candidate(
            candidate
        )


def test_candidate_contains_no_raw_evidence_review_queue_or_trust_payload() -> None:
    candidate = _build()
    serialized = repr(candidate).lower()

    assert "raw synthetic body" not in serialized
    assert "review_queue_item" not in serialized
    assert "provider_payload" not in serialized
    assert "production_object" not in candidate
    assert "trust_score" not in serialized
