from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from typing import Any

from app.schemas.evidence import EvidenceItem


_SAFE_IDENTITY_RECEIPT_SCHEMA = (
    "sentigraph_existing_evidenceitem_safe_identity_receipt_v0_1"
)
_SAFE_IDENTITY_RECEIPT_VERSION = "0.1"
_SAFE_IDENTITY_RECEIPT_MODE = (
    "internal_read_only_safe_existing_evidenceitem_identity_projection"
)
_EVIDENCE_MODEL_QUALIFIED_NAME = "app.schemas.evidence.EvidenceItem"
_EVIDENCE_MODEL_CONTRACT_SHA256 = (
    "7a3d5c188856087d6b1a42963c2be196d9a15eb574e554ce9351ca235eec6033"
)
_SAFE_IDENTITY_RECEIPT_FIELDS = (
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

_CONTENT_AUTHORITY_SCHEMA = (
    "sentigraph_existing_evidenceitem_one_modality_content_privacy_"
    "authority_binding_v0_1"
)
_CONTENT_AUTHORITY_VERSION = "0.1"
_CONTENT_AUTHORITY_SCOPE = (
    "one_selected_evidenceitem_one_modality_transient_review_card"
)
_CONTENT_AUTHORITY_FIELDS = (
    "schema",
    "version",
    "scope",
    "authority_receipt_reference",
    "case_id",
    "evidence_id",
    "identity_receipt_reference",
    "authorized_content_modality",
    "selected_field_read_max",
    "maximum_output_utf8_bytes",
    "raw_content_return_authorized",
    "source_url_access_authorized",
    "author_identity_access_authorized",
    "raw_data_safe_access_authorized",
    "ingestion_metadata_access_authorized",
    "review_history_access_authorized",
    "downstream_action_authorized",
)
_FALSE_AUTHORITY_FIELDS = (
    "raw_content_return_authorized",
    "source_url_access_authorized",
    "author_identity_access_authorized",
    "raw_data_safe_access_authorized",
    "ingestion_metadata_access_authorized",
    "review_history_access_authorized",
    "downstream_action_authorized",
)

_REDACTION_POLICY = (
    "SENTIGRAPH_EXISTING_EVIDENCEITEM_REVIEW_CARD_BOUNDED_REDACTION_V0_1"
)
_REVIEW_CARD_SCHEMA = (
    "sentigraph_existing_evidenceitem_final_linkage_target_review_card_v0_1"
)
_REVIEW_CARD_VERSION = "0.1"
_REVIEW_CARD_MODE = (
    "internal_pure_in_memory_nonpersistent_nonauthorizing_final_linkage_"
    "target_review_card"
)
_REVIEW_CARD_FIELDS = (
    "schema",
    "version",
    "mode",
    "identity_receipt_reference",
    "content_privacy_authority_receipt_reference",
    "case_id",
    "evidence_id",
    "content_hash",
    "content_modality",
    "review_text",
    "review_text_present",
    "review_text_utf8_bytes",
    "review_text_truncated",
    "redaction_policy",
    "redaction_counts",
    "privacy_stop",
    "privacy_stop_reasons",
    "privacy_review_required",
    "pii_free_claimed",
    "secret_free_claimed",
    "evidence_type",
    "language",
    "platform",
    "source_type",
    "provenance_type",
    "acquisition_mode",
    "verification_status",
    "review_status",
    "source_url_present",
    "duplicate_group_present",
    "duplicate_count_evaluated",
    "duplicate_context_class",
    "content_authority_binding_shape_validated",
    "human_authority_validated_by_builder",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "semantic_relevance_adjudicated",
    "final_linkage_target_selected",
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
)
_DOWNSTREAM_FALSE_FIELDS = (
    "semantic_relevance_adjudicated",
    "final_linkage_target_selected",
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
)
_CONTENT_MODALITIES = frozenset({"title", "body_text", "comment_text"})
_SAFE_ITEM_LABELS = ("evidence_type", "language", "platform", "source_type")
_SAFE_RECEIPT_LABELS = (
    "provenance_type",
    "acquisition_mode",
    "verification_status",
    "review_status",
)
_REDACTION_COUNT_FIELDS = ("url", "email", "handle", "ip", "phone", "path")
_LOWER_HEX_64 = re.compile(r"[0-9a-f]{64}")
_SECRET_MARKERS = (
    "authorization:",
    "bearer ",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "password",
    "passwd",
    "secret",
    "cookie",
    "sessionid",
    "sk-",
    "ghp_",
    "github_pat_",
    "akia",
)
_REDACTION_PATTERNS = (
    (
        "url",
        re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s]+", re.IGNORECASE),
        "[REDACTED_URL]",
    ),
    (
        "email",
        re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
        "[REDACTED_EMAIL]",
    ),
    (
        "handle",
        re.compile(r"(?<![\w@])@[A-Za-z0-9_][A-Za-z0-9_.-]*"),
        "[REDACTED_HANDLE]",
    ),
    (
        "ip",
        re.compile(
            r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}"
            r"(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)"
        ),
        "[REDACTED_IP]",
    ),
    (
        "phone",
        re.compile(r"(?<!\w)\+?\d[\d\s().-]{6,}\d(?!\w)"),
        "[REDACTED_PHONE]",
    ),
    (
        "path",
        re.compile(
            r"(?<!\w)(?:[A-Za-z]:[\\/]|\\\\)[^\s]+"
            r"|(?<![\w:])/(?:[^/\s]+/)*[^/\s]+"
        ),
        "[REDACTED_PATH]",
    ),
)


class _ReviewCardContractError(ValueError):
    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise _ReviewCardContractError(outcome)


def _validate_text_scalar(
    value: Any,
    *,
    field_name: str,
    maximum_utf8_bytes: int,
) -> str:
    if type(value) is not str or value == "":
        _fail(f"blocked_{field_name}_invalid")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail(f"blocked_{field_name}_invalid")
    if len(encoded) > maximum_utf8_bytes:
        _fail(f"blocked_{field_name}_invalid")
    if any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in value):
        _fail(f"blocked_{field_name}_invalid")
    return value


def _receipt_reference(*, case_id: str, evidence_id: str, content_hash: str) -> str:
    material = "\0".join(
        (
            _SAFE_IDENTITY_RECEIPT_SCHEMA,
            case_id,
            evidence_id,
            content_hash,
            _EVIDENCE_MODEL_CONTRACT_SHA256,
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"eir-{digest[:32]}"


def _validate_identity_receipt(receipt: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(receipt, Mapping) or set(receipt) != set(
        _SAFE_IDENTITY_RECEIPT_FIELDS
    ):
        _fail("blocked_safe_identity_receipt_contract_mismatch")
    if (
        receipt["schema"] != _SAFE_IDENTITY_RECEIPT_SCHEMA
        or receipt["version"] != _SAFE_IDENTITY_RECEIPT_VERSION
        or receipt["mode"] != _SAFE_IDENTITY_RECEIPT_MODE
        or receipt["evidence_model_qualified_name"]
        != _EVIDENCE_MODEL_QUALIFIED_NAME
        or receipt["evidence_model_contract_sha256"]
        != _EVIDENCE_MODEL_CONTRACT_SHA256
    ):
        _fail("blocked_safe_identity_receipt_contract_mismatch")

    case_id = _validate_text_scalar(
        receipt["case_id"], field_name="case_id", maximum_utf8_bytes=512
    )
    evidence_id = _validate_text_scalar(
        receipt["evidence_id"], field_name="evidence_id", maximum_utf8_bytes=512
    )
    content_hash = receipt["content_hash"]
    if type(content_hash) is not str or _LOWER_HEX_64.fullmatch(content_hash) is None:
        _fail("blocked_content_hash_invalid")
    for field_name in _SAFE_RECEIPT_LABELS:
        _validate_text_scalar(
            receipt[field_name], field_name=field_name, maximum_utf8_bytes=128
        )
    if type(receipt["source_url_present"]) is not bool:
        _fail("blocked_source_url_presence_invalid")
    duplicate_group_present = receipt["duplicate_group_id"] is not None
    expected_booleans = {
        "exact_one_evidenceitem": True,
        "read_only_verified": True,
        "raw_evidence_content_included": False,
        "raw_personal_identity_included": False,
    }
    if any(receipt[field] is not expected for field, expected in expected_booleans.items()):
        _fail("blocked_safe_identity_receipt_authority_mismatch")
    if receipt["receipt_reference"] != _receipt_reference(
        case_id=case_id,
        evidence_id=evidence_id,
        content_hash=content_hash,
    ):
        _fail("blocked_safe_identity_receipt_reference_mismatch")
    return {
        **{field: receipt[field] for field in _SAFE_IDENTITY_RECEIPT_FIELDS},
        "duplicate_group_present": duplicate_group_present,
    }


def _validate_authority_binding(
    binding: Mapping[str, Any],
    *,
    identity_receipt: Mapping[str, Any],
    content_modality: str,
) -> dict[str, Any]:
    if not isinstance(binding, Mapping) or set(binding) != set(
        _CONTENT_AUTHORITY_FIELDS
    ):
        _fail("blocked_content_authority_binding_contract_mismatch")
    if (
        binding["schema"] != _CONTENT_AUTHORITY_SCHEMA
        or binding["version"] != _CONTENT_AUTHORITY_VERSION
        or binding["scope"] != _CONTENT_AUTHORITY_SCOPE
        or binding["case_id"] != identity_receipt["case_id"]
        or binding["evidence_id"] != identity_receipt["evidence_id"]
        or binding["identity_receipt_reference"]
        != identity_receipt["receipt_reference"]
    ):
        _fail("blocked_content_authority_binding_target_mismatch")
    _validate_text_scalar(
        binding["authority_receipt_reference"],
        field_name="authority_receipt_reference",
        maximum_utf8_bytes=512,
    )
    if binding["authorized_content_modality"] != content_modality:
        _fail("blocked_content_authority_binding_modality_mismatch")
    if (
        type(binding["selected_field_read_max"]) is not int
        or binding["selected_field_read_max"] != 1
        or type(binding["maximum_output_utf8_bytes"]) is not int
        or binding["maximum_output_utf8_bytes"] != 2048
        or any(binding[field] is not False for field in _FALSE_AUTHORITY_FIELDS)
    ):
        _fail("blocked_content_authority_binding_limits_mismatch")
    return {field: binding[field] for field in _CONTENT_AUTHORITY_FIELDS}


def _validate_selected_source(value: Any) -> str:
    if type(value) is not str:
        _fail("blocked_selected_content_non_string")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail("blocked_selected_content_invalid_utf8")
    if len(encoded) > 16384:
        _fail("blocked_selected_content_oversized")
    for character in value:
        codepoint = ord(character)
        if codepoint == 0:
            _fail("blocked_selected_content_nul")
        if (codepoint < 32 and character not in "\t\r\n") or 127 <= codepoint <= 159:
            _fail("blocked_selected_content_control")
    if value.strip() == "":
        _fail("blocked_selected_content_empty")
    return value


def _truncate_utf8(value: str, maximum_bytes: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8")
    if len(encoded) <= maximum_bytes:
        return value, False
    return encoded[:maximum_bytes].decode("utf-8", errors="ignore"), True


def _redact_selected_source(value: str) -> dict[str, Any]:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    counts = {field: 0 for field in _REDACTION_COUNT_FIELDS}
    folded = normalized.casefold()
    if any(marker in folded for marker in _SECRET_MARKERS):
        return {
            "review_text": None,
            "review_text_present": False,
            "review_text_utf8_bytes": 0,
            "review_text_truncated": False,
            "redaction_counts": counts,
            "privacy_stop": True,
            "privacy_stop_reasons": ["SECRET_LIKE_PATTERN_DETECTED"],
        }

    redacted = normalized
    for field_name, pattern, token in _REDACTION_PATTERNS:
        redacted, count = pattern.subn(token, redacted)
        counts[field_name] = count
    redacted = re.sub(r"\s+", " ", redacted).strip()
    if redacted == "":
        return {
            "review_text": None,
            "review_text_present": False,
            "review_text_utf8_bytes": 0,
            "review_text_truncated": False,
            "redaction_counts": counts,
            "privacy_stop": True,
            "privacy_stop_reasons": ["EMPTY_AFTER_REDACTION"],
        }
    review_text, truncated = _truncate_utf8(redacted, 2048)
    return {
        "review_text": review_text,
        "review_text_present": True,
        "review_text_utf8_bytes": len(review_text.encode("utf-8")),
        "review_text_truncated": truncated,
        "redaction_counts": counts,
        "privacy_stop": False,
        "privacy_stop_reasons": [],
    }


def build_existing_evidenceitem_final_linkage_target_review_card(
    evidence_item: EvidenceItem,
    safe_identity_receipt: Mapping[str, Any],
    content_privacy_authority_binding: Mapping[str, Any],
    *,
    content_modality: str,
    redaction_policy: str,
) -> dict[str, Any]:
    """Build one bounded synthetic-capable review card without side effects."""

    if not isinstance(evidence_item, EvidenceItem):
        _fail("blocked_evidenceitem_model_mismatch")
    if type(content_modality) is not str or content_modality not in _CONTENT_MODALITIES:
        _fail("blocked_content_modality_unsupported")
    if redaction_policy != _REDACTION_POLICY:
        _fail("blocked_redaction_policy_mismatch")

    receipt = _validate_identity_receipt(safe_identity_receipt)
    if (
        evidence_item.case_id != receipt["case_id"]
        or evidence_item.evidence_id != receipt["evidence_id"]
        or evidence_item.content_hash != receipt["content_hash"]
    ):
        _fail("blocked_evidenceitem_identity_mismatch")
    authority = _validate_authority_binding(
        content_privacy_authority_binding,
        identity_receipt=receipt,
        content_modality=content_modality,
    )

    safe_item_labels = {
        field_name: _validate_text_scalar(
            getattr(evidence_item, field_name),
            field_name=field_name,
            maximum_utf8_bytes=128,
        )
        for field_name in _SAFE_ITEM_LABELS
    }
    selected_source = _validate_selected_source(getattr(evidence_item, content_modality))
    redaction = _redact_selected_source(selected_source)
    duplicate_group_present = receipt["duplicate_group_present"]

    values: dict[str, Any] = {
        "schema": _REVIEW_CARD_SCHEMA,
        "version": _REVIEW_CARD_VERSION,
        "mode": _REVIEW_CARD_MODE,
        "identity_receipt_reference": receipt["receipt_reference"],
        "content_privacy_authority_receipt_reference": authority[
            "authority_receipt_reference"
        ],
        "case_id": receipt["case_id"],
        "evidence_id": receipt["evidence_id"],
        "content_hash": receipt["content_hash"],
        "content_modality": content_modality,
        **redaction,
        "redaction_policy": _REDACTION_POLICY,
        "privacy_review_required": True,
        "pii_free_claimed": False,
        "secret_free_claimed": False,
        **safe_item_labels,
        **{field: receipt[field] for field in _SAFE_RECEIPT_LABELS},
        "source_url_present": receipt["source_url_present"],
        "duplicate_group_present": duplicate_group_present,
        "duplicate_count_evaluated": False,
        "duplicate_context_class": (
            "duplicate_group_present_count_not_evaluated"
            if duplicate_group_present
            else "no_duplicate_group"
        ),
        "content_authority_binding_shape_validated": True,
        "human_authority_validated_by_builder": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in _DOWNSTREAM_FALSE_FIELDS},
    }
    if set(values) != set(_REVIEW_CARD_FIELDS):
        _fail("blocked_review_card_output_contract_mismatch")
    return {field: values[field] for field in _REVIEW_CARD_FIELDS}
