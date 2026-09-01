from __future__ import annotations

import inspect
from types import SimpleNamespace
from typing import Any

import pytest

from app.schemas.evidence import EvidenceItem
from app.services import existing_evidenceitem_safe_identity_projection as service


CASE_ID = "case-synthetic-001"
EVIDENCE_ID = "evidence-synthetic-001"
CONTENT_HASH = "a" * 64


class _FakeCaseRepository:
    def __init__(self, case: object | None) -> None:
        self.case = case
        self.get_calls: list[str] = []

    def get_case(self, case_id: str) -> object | None:
        self.get_calls.append(case_id)
        return self.case


def _item(**overrides: Any) -> EvidenceItem:
    values: dict[str, Any] = {
        "case_id": CASE_ID,
        "evidence_id": EVIDENCE_ID,
        "content_hash": CONTENT_HASH,
        "body_text": "synthetic raw body that must not enter the receipt",
        "author_name": "synthetic private label",
        "source_url_present": True,
        "duplicate_group_id": "duplicate-group-synthetic",
    }
    values.update(overrides)
    return EvidenceItem(**values)


def _repository(*items: EvidenceItem) -> _FakeCaseRepository:
    return _FakeCaseRepository(SimpleNamespace(evidence_items=list(items)))


def _project(
    repository: _FakeCaseRepository | None = None,
    *,
    case_id: str = CASE_ID,
    evidence_id: str = EVIDENCE_ID,
) -> dict[str, Any]:
    return service.project_existing_evidenceitem_safe_identity_receipt(
        repository or _repository(_item()),
        case_id,
        evidence_id,
    )


def test_exact_existing_item_projects_one_bounded_safe_identity_receipt() -> None:
    repository = _repository(_item())

    receipt = _project(repository)

    assert tuple(receipt) == service.SAFE_IDENTITY_RECEIPT_FIELDS
    assert receipt["case_id"] == CASE_ID
    assert receipt["evidence_id"] == EVIDENCE_ID
    assert receipt["content_hash"] == CONTENT_HASH
    assert receipt["evidence_model_qualified_name"] == (
        "app.schemas.evidence.EvidenceItem"
    )
    assert receipt["evidence_model_contract_sha256"] == (
        "7a3d5c188856087d6b1a42963c2be196d9a15eb574e554ce9351ca235eec6033"
    )
    assert receipt["source_url_present"] is True
    assert receipt["exact_one_evidenceitem"] is True
    assert receipt["read_only_verified"] is True
    assert receipt["raw_evidence_content_included"] is False
    assert receipt["raw_personal_identity_included"] is False
    assert repository.get_calls == [CASE_ID]


def test_receipt_excludes_raw_content_identity_and_url_values() -> None:
    receipt = _project()
    prohibited = {
        "body_text",
        "comment_text",
        "raw_data_safe",
        "author_id",
        "author_name",
        "source_url",
        "url",
        "submitter_hash",
        "review_notes",
    }

    assert prohibited.isdisjoint(receipt)
    serialized = repr(receipt)
    assert "synthetic raw body" not in serialized
    assert "synthetic private label" not in serialized


def test_receipt_validation_accepts_reordered_keys_but_rejects_field_drift() -> None:
    receipt = _project()
    reordered = dict(reversed(list(receipt.items())))

    validated = service.validate_existing_evidenceitem_safe_identity_receipt(
        reordered
    )

    assert tuple(validated) == service.SAFE_IDENTITY_RECEIPT_FIELDS
    with pytest.raises(service.ExistingEvidenceItemSafeIdentityProjectionError):
        service.validate_existing_evidenceitem_safe_identity_receipt(
            {**receipt, "unexpected": True}
        )


@pytest.mark.parametrize(
    "case",
    [
        None,
        SimpleNamespace(evidence_items=None),
        SimpleNamespace(evidence_items=[]),
        SimpleNamespace(evidence_items=[_item(), _item()]),
    ],
)
def test_absent_or_nonunique_evidence_fails_closed(case: object | None) -> None:
    repository = _FakeCaseRepository(case)

    with pytest.raises(service.ExistingEvidenceItemSafeIdentityProjectionError):
        _project(repository)

    assert repository.get_calls == [CASE_ID]


@pytest.mark.parametrize("content_hash", ["", "A" * 64, "a" * 63, "g" * 64])
def test_content_hash_must_be_exact_lowerhex64(content_hash: str) -> None:
    with pytest.raises(service.ExistingEvidenceItemSafeIdentityProjectionError):
        _project(_repository(_item(content_hash=content_hash)))


def test_optional_item_case_id_may_be_absent_but_cannot_contradict_case() -> None:
    assert _project(_repository(_item(case_id=None)))["case_id"] == CASE_ID

    with pytest.raises(service.ExistingEvidenceItemSafeIdentityProjectionError):
        _project(_repository(_item(case_id="different-case")))


def test_case_id_is_part_of_the_safe_receipt_identity_reference() -> None:
    first = _project()
    second_case_id = "case-synthetic-002"
    second = _project(
        _repository(_item(case_id=second_case_id)),
        case_id=second_case_id,
    )

    assert first["evidence_id"] == second["evidence_id"]
    assert first["content_hash"] == second["content_hash"]
    assert first["receipt_reference"] != second["receipt_reference"]


@pytest.mark.parametrize(
    ("case_id", "evidence_id"),
    [
        ("", EVIDENCE_ID),
        (CASE_ID, ""),
        ("case\ninvalid", EVIDENCE_ID),
        (CASE_ID, "evidence\x00invalid"),
    ],
)
def test_invalid_exact_identifiers_fail_before_repository_access(
    case_id: str,
    evidence_id: str,
) -> None:
    repository = _repository(_item())

    with pytest.raises(service.ExistingEvidenceItemSafeIdentityProjectionError):
        _project(repository, case_id=case_id, evidence_id=evidence_id)

    assert repository.get_calls == []


def test_projection_source_has_no_write_network_or_factory_surface() -> None:
    source = inspect.getsource(service)
    lowered = source.lower()

    for forbidden in (
        "case_repository.add",
        "case_repository.update",
        "case_repository.delete",
        "httpx",
        "requests",
        "socket",
        "subprocess",
        "store_factory",
    ):
        assert forbidden not in lowered
