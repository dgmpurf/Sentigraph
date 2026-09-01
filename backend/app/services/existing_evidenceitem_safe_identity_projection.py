from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from typing import Any, Protocol

from app.schemas.evidence import EvidenceItem


SAFE_IDENTITY_RECEIPT_SCHEMA = (
    "sentigraph_existing_evidenceitem_safe_identity_receipt_v0_1"
)
SAFE_IDENTITY_RECEIPT_VERSION = "0.1"
SAFE_IDENTITY_RECEIPT_MODE = (
    "internal_read_only_safe_existing_evidenceitem_identity_projection"
)
EVIDENCE_MODEL_QUALIFIED_NAME = "app.schemas.evidence.EvidenceItem"
EVIDENCE_MODEL_CONTRACT_SHA256 = (
    "7a3d5c188856087d6b1a42963c2be196d9a15eb574e554ce9351ca235eec6033"
)

SAFE_IDENTITY_RECEIPT_FIELDS = (
    "schema",
    "version",
    "mode",
    "receipt_reference",
    "case_id",
    "evidence_id",
    "evidence_model_qualified_name",
    "evidence_model_contract_sha256",
    "content_hash",
    "provenance_type",
    "acquisition_mode",
    "verification_status",
    "review_status",
    "source_url_present",
    "duplicate_group_id",
    "exact_one_evidenceitem",
    "read_only_verified",
    "raw_evidence_content_included",
    "raw_personal_identity_included",
)

_LOWER_HEX_64_PATTERN = re.compile(r"[0-9a-f]{64}")
_MAX_IDENTIFIER_UTF8_BYTES = 512


class _CaseRepositoryLike(Protocol):
    def get_case(self, case_id: str) -> Any: ...


class ExistingEvidenceItemSafeIdentityProjectionError(ValueError):
    """Raised when an existing EvidenceItem cannot produce a safe receipt."""

    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise ExistingEvidenceItemSafeIdentityProjectionError(outcome)


def validate_exact_identifier(value: Any, *, field_name: str) -> str:
    """Validate an exact identifier without rewriting or normalizing it."""

    if type(value) is not str or value == "":
        _fail(f"blocked_{field_name}_invalid")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail(f"blocked_{field_name}_invalid")
    if len(encoded) > _MAX_IDENTIFIER_UTF8_BYTES:
        _fail(f"blocked_{field_name}_invalid")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        _fail(f"blocked_{field_name}_invalid")
    return value


def _validate_safe_string(value: Any, *, field_name: str) -> str:
    return validate_exact_identifier(value, field_name=field_name)


def _receipt_reference(
    *,
    case_id: str,
    evidence_id: str,
    content_hash: str,
) -> str:
    material = "\0".join(
        (
            SAFE_IDENTITY_RECEIPT_SCHEMA,
            case_id,
            evidence_id,
            content_hash,
            EVIDENCE_MODEL_CONTRACT_SHA256,
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"eir-{digest[:32]}"


def validate_existing_evidenceitem_safe_identity_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and copy one strict safe EvidenceItem identity receipt."""

    if not isinstance(receipt, Mapping) or set(receipt) != set(
        SAFE_IDENTITY_RECEIPT_FIELDS
    ):
        _fail("blocked_safe_identity_receipt_contract_mismatch")
    if (
        receipt["schema"] != SAFE_IDENTITY_RECEIPT_SCHEMA
        or receipt["version"] != SAFE_IDENTITY_RECEIPT_VERSION
        or receipt["mode"] != SAFE_IDENTITY_RECEIPT_MODE
        or receipt["evidence_model_qualified_name"]
        != EVIDENCE_MODEL_QUALIFIED_NAME
        or receipt["evidence_model_contract_sha256"]
        != EVIDENCE_MODEL_CONTRACT_SHA256
    ):
        _fail("blocked_safe_identity_receipt_contract_mismatch")

    case_id = validate_exact_identifier(receipt["case_id"], field_name="case_id")
    evidence_id = validate_exact_identifier(
        receipt["evidence_id"], field_name="evidence_id"
    )
    content_hash = receipt["content_hash"]
    if type(content_hash) is not str or _LOWER_HEX_64_PATTERN.fullmatch(content_hash) is None:
        _fail("blocked_content_hash_invalid")

    for field_name in (
        "provenance_type",
        "acquisition_mode",
        "verification_status",
        "review_status",
    ):
        _validate_safe_string(receipt[field_name], field_name=field_name)

    if type(receipt["source_url_present"]) is not bool:
        _fail("blocked_source_url_presence_invalid")
    duplicate_group_id = receipt["duplicate_group_id"]
    if duplicate_group_id is not None:
        _validate_safe_string(
            duplicate_group_id,
            field_name="duplicate_group_id",
        )

    expected_booleans = {
        "exact_one_evidenceitem": True,
        "read_only_verified": True,
        "raw_evidence_content_included": False,
        "raw_personal_identity_included": False,
    }
    if any(receipt[field] is not expected for field, expected in expected_booleans.items()):
        _fail("blocked_safe_identity_receipt_authority_mismatch")

    expected_reference = _receipt_reference(
        case_id=case_id,
        evidence_id=evidence_id,
        content_hash=content_hash,
    )
    if receipt["receipt_reference"] != expected_reference:
        _fail("blocked_safe_identity_receipt_reference_mismatch")
    return {field: receipt[field] for field in SAFE_IDENTITY_RECEIPT_FIELDS}


def project_existing_evidenceitem_safe_identity_receipt(
    case_repository: _CaseRepositoryLike,
    case_id: str,
    evidence_id: str,
) -> dict[str, Any]:
    """Resolve exactly one existing EvidenceItem into a bounded safe receipt."""

    validated_case_id = validate_exact_identifier(case_id, field_name="case_id")
    validated_evidence_id = validate_exact_identifier(
        evidence_id,
        field_name="evidence_id",
    )
    case = case_repository.get_case(validated_case_id)
    if case is None:
        _fail("case_not_found")
    evidence_items = getattr(case, "evidence_items", None)
    if not isinstance(evidence_items, list):
        _fail("blocked_case_evidence_contract_mismatch")
    matches = [
        item
        for item in evidence_items
        if isinstance(item, EvidenceItem) and item.evidence_id == validated_evidence_id
    ]
    if len(matches) != 1:
        _fail("evidenceitem_exact_match_count_invalid")
    item = matches[0]
    if item.case_id is not None and item.case_id != validated_case_id:
        _fail("blocked_evidenceitem_case_identity_mismatch")

    content_hash = item.content_hash
    if type(content_hash) is not str or _LOWER_HEX_64_PATTERN.fullmatch(content_hash) is None:
        _fail("blocked_content_hash_invalid")

    safe_values: dict[str, Any] = {}
    for field_name in (
        "provenance_type",
        "acquisition_mode",
        "verification_status",
        "review_status",
    ):
        safe_values[field_name] = _validate_safe_string(
            getattr(item, field_name, None),
            field_name=field_name,
        )
    if type(item.source_url_present) is not bool:
        _fail("blocked_source_url_presence_invalid")
    duplicate_group_id = item.duplicate_group_id
    if duplicate_group_id is not None:
        duplicate_group_id = _validate_safe_string(
            duplicate_group_id,
            field_name="duplicate_group_id",
        )

    values: dict[str, Any] = {
        "schema": SAFE_IDENTITY_RECEIPT_SCHEMA,
        "version": SAFE_IDENTITY_RECEIPT_VERSION,
        "mode": SAFE_IDENTITY_RECEIPT_MODE,
        "receipt_reference": _receipt_reference(
            case_id=validated_case_id,
            evidence_id=validated_evidence_id,
            content_hash=content_hash,
        ),
        "case_id": validated_case_id,
        "evidence_id": validated_evidence_id,
        "evidence_model_qualified_name": EVIDENCE_MODEL_QUALIFIED_NAME,
        "evidence_model_contract_sha256": EVIDENCE_MODEL_CONTRACT_SHA256,
        "content_hash": content_hash,
        **safe_values,
        "source_url_present": item.source_url_present,
        "duplicate_group_id": duplicate_group_id,
        "exact_one_evidenceitem": True,
        "read_only_verified": True,
        "raw_evidence_content_included": False,
        "raw_personal_identity_included": False,
    }
    receipt = {field: values[field] for field in SAFE_IDENTITY_RECEIPT_FIELDS}
    return validate_existing_evidenceitem_safe_identity_receipt(receipt)
