from __future__ import annotations

import hashlib
from typing import Any, ClassVar

import pytest

from app.schemas.evidence import EvidenceItem
from app.services.existing_evidenceitem_final_linkage_target_review_card import (
    build_existing_evidenceitem_final_linkage_target_review_card,
)


CASE_ID = "synthetic_case_alpha"
EVIDENCE_ID = "synthetic_evidence_alpha"
CONTENT_HASH = "1" * 64
MODEL_HASH = "7a3d5c188856087d6b1a42963c2be196d9a15eb574e554ce9351ca235eec6033"
POLICY = "SENTIGRAPH_EXISTING_EVIDENCEITEM_REVIEW_CARD_BOUNDED_REDACTION_V0_1"
RECEIPT_FIELDS = (
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
AUTHORITY_FIELDS = (
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
OUTPUT_FIELDS = (
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
DOWNSTREAM_FALSE_FIELDS = (
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
FORBIDDEN_OUTPUT_FIELDS = {
    "url",
    "source_url",
    "author_id",
    "author_name",
    "submitted_by_label",
    "submitter_hash",
    "reviewer_label",
    "parent_id",
    "root_id",
    "raw_data_safe",
    "user_attestation_text",
    "verification_notes",
    "risk_flags",
    "review_reason_codes",
    "review_notes",
    "review_history",
    "ingestion_metadata",
    "duplicate_group_id",
}


def _receipt_reference(
    case_id: str = CASE_ID,
    evidence_id: str = EVIDENCE_ID,
    content_hash: str = CONTENT_HASH,
) -> str:
    material = "\0".join(
        (
            "sentigraph_existing_evidenceitem_safe_identity_receipt_v0_1",
            case_id,
            evidence_id,
            content_hash,
            MODEL_HASH,
        )
    )
    return f"eir-{hashlib.sha256(material.encode('utf-8')).hexdigest()[:32]}"


def _receipt(**updates: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "schema": "sentigraph_existing_evidenceitem_safe_identity_receipt_v0_1",
        "version": "0.1",
        "mode": "internal_read_only_safe_existing_evidenceitem_identity_projection",
        "receipt_reference": _receipt_reference(),
        "case_id": CASE_ID,
        "evidence_id": EVIDENCE_ID,
        "evidence_model_qualified_name": "app.schemas.evidence.EvidenceItem",
        "evidence_model_contract_sha256": MODEL_HASH,
        "content_hash": CONTENT_HASH,
        "provenance_type": "manual_submission",
        "acquisition_mode": "user_upload",
        "verification_status": "needs_review",
        "review_status": "not_reviewed",
        "source_url_present": True,
        "duplicate_group_id": None,
        "exact_one_evidenceitem": True,
        "read_only_verified": True,
        "raw_evidence_content_included": False,
        "raw_personal_identity_included": False,
    }
    values.update(updates)
    return {field: values[field] for field in RECEIPT_FIELDS}


def _authority(modality: str = "title", **updates: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "schema": (
            "sentigraph_existing_evidenceitem_one_modality_content_privacy_"
            "authority_binding_v0_1"
        ),
        "version": "0.1",
        "scope": "one_selected_evidenceitem_one_modality_transient_review_card",
        "authority_receipt_reference": "synthetic-authority-receipt-alpha",
        "case_id": CASE_ID,
        "evidence_id": EVIDENCE_ID,
        "identity_receipt_reference": _receipt_reference(),
        "authorized_content_modality": modality,
        "selected_field_read_max": 1,
        "maximum_output_utf8_bytes": 2048,
        "raw_content_return_authorized": False,
        "source_url_access_authorized": False,
        "author_identity_access_authorized": False,
        "raw_data_safe_access_authorized": False,
        "ingestion_metadata_access_authorized": False,
        "review_history_access_authorized": False,
        "downstream_action_authorized": False,
    }
    values.update(updates)
    return {field: values[field] for field in AUTHORITY_FIELDS}


def _item(model: type[EvidenceItem] = EvidenceItem, **updates: Any) -> EvidenceItem:
    values: dict[str, Any] = {
        "case_id": CASE_ID,
        "evidence_id": EVIDENCE_ID,
        "content_hash": CONTENT_HASH,
        "title": "Synthetic title for human review",
        "body_text": "Synthetic body for human review",
        "comment_text": "Synthetic comment for human review",
        "evidence_type": "comment",
        "language": "en",
        "platform": "synthetic_platform",
        "source_type": "manual_submission",
    }
    values.update(updates)
    return model.model_construct(**values)


def _build(
    *,
    item: EvidenceItem | None = None,
    receipt: dict[str, Any] | None = None,
    authority: dict[str, Any] | None = None,
    modality: str = "title",
    policy: str = POLICY,
) -> dict[str, Any]:
    return build_existing_evidenceitem_final_linkage_target_review_card(
        item if item is not None else _item(),
        receipt if receipt is not None else _receipt(),
        authority if authority is not None else _authority(modality),
        content_modality=modality,
        redaction_policy=policy,
    )


class _TrackingEvidenceItem(EvidenceItem):
    tracking_active: ClassVar[bool] = False
    reads: ClassVar[dict[str, int]] = {}
    blocked: ClassVar[set[str]] = set()

    def __getattribute__(self, name: str) -> Any:
        cls = type(self)
        if cls.tracking_active:
            if name in {"title", "body_text", "comment_text"}:
                cls.reads[name] = cls.reads.get(name, 0) + 1
            if name in cls.blocked:
                raise AssertionError(f"forbidden attribute accessed: {name}")
        return super().__getattribute__(name)


def _tracked_build(item: _TrackingEvidenceItem, *, modality: str) -> dict[str, Any]:
    _TrackingEvidenceItem.reads = {}
    _TrackingEvidenceItem.tracking_active = True
    try:
        return _build(item=item, modality=modality)
    finally:
        _TrackingEvidenceItem.tracking_active = False


@pytest.mark.parametrize(
    ("modality", "expected"),
    [
        ("title", "Synthetic title for human review"),
        ("body_text", "Synthetic body for human review"),
        ("comment_text", "Synthetic comment for human review"),
    ],
)
def test_valid_synthetic_card_for_each_explicit_modality(
    modality: str, expected: str
) -> None:
    card = _build(modality=modality)

    assert tuple(card) == OUTPUT_FIELDS
    assert card["content_modality"] == modality
    assert card["review_text"] == expected
    assert card["review_text_present"] is True
    assert card["privacy_stop"] is False


def test_reads_exactly_one_selected_modality_once() -> None:
    item = _item(model=_TrackingEvidenceItem)
    _tracked_build(item, modality="comment_text")

    assert _TrackingEvidenceItem.reads == {"comment_text": 1}


def test_empty_selected_modality_does_not_fallback() -> None:
    item = _item(model=_TrackingEvidenceItem, title="", body_text="fallback forbidden")
    _TrackingEvidenceItem.reads = {}
    _TrackingEvidenceItem.tracking_active = True
    try:
        with pytest.raises(ValueError, match="blocked_selected_content_empty"):
            _build(item=item, modality="title")
    finally:
        _TrackingEvidenceItem.tracking_active = False

    assert _TrackingEvidenceItem.reads == {"title": 1}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_model_qualified_name", "synthetic.WrongModel"),
        ("evidence_model_contract_sha256", "2" * 64),
    ],
)
def test_safe_receipt_model_identity_must_match(field: str, value: str) -> None:
    with pytest.raises(ValueError, match="blocked_safe_identity_receipt_contract_mismatch"):
        _build(receipt=_receipt(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("case_id", "synthetic_case_other"),
        ("evidence_id", "synthetic_evidence_other"),
        ("content_hash", "2" * 64),
    ],
)
def test_evidenceitem_identity_mismatch_fails(field: str, value: str) -> None:
    with pytest.raises(ValueError, match="blocked_evidenceitem_identity_mismatch"):
        _build(item=_item(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("case_id", "synthetic_case_other"),
        ("evidence_id", "synthetic_evidence_other"),
        ("identity_receipt_reference", "eir-synthetic-wrong"),
    ],
)
def test_authority_target_mismatch_fails(field: str, value: str) -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_target_mismatch"):
        _build(authority=_authority(**{field: value}))


def test_authority_modality_mismatch_fails() -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_modality_mismatch"):
        _build(modality="title", authority=_authority("body_text"))


@pytest.mark.parametrize("operation", ["missing", "extra"])
def test_receipt_exact_field_set_is_required(operation: str) -> None:
    receipt = _receipt()
    if operation == "missing":
        receipt.pop("review_status")
    else:
        receipt["extra"] = False
    with pytest.raises(ValueError, match="blocked_safe_identity_receipt_contract_mismatch"):
        _build(receipt=receipt)


@pytest.mark.parametrize("operation", ["missing", "extra"])
def test_authority_exact_field_set_is_required(operation: str) -> None:
    authority = _authority()
    if operation == "missing":
        authority.pop("scope")
    else:
        authority["extra"] = False
    with pytest.raises(ValueError, match="blocked_content_authority_binding_contract_mismatch"):
        _build(authority=authority)


def test_non_string_selected_content_fails_closed() -> None:
    with pytest.raises(ValueError, match="blocked_selected_content_non_string"):
        _build(item=_item(title=42))


@pytest.mark.parametrize("value", ["", " \t\r\n "])
def test_empty_selected_content_fails_closed(value: str) -> None:
    with pytest.raises(ValueError, match="blocked_selected_content_empty"):
        _build(item=_item(title=value))


def test_oversized_selected_content_fails_closed() -> None:
    with pytest.raises(ValueError, match="blocked_selected_content_oversized"):
        _build(item=_item(title="x" * 16385))


@pytest.mark.parametrize(
    ("value", "reason"),
    [("synthetic\x00text", "nul"), ("synthetic\x01text", "control"), ("synthetic\x85text", "control")],
)
def test_nul_and_disallowed_controls_fail(value: str, reason: str) -> None:
    with pytest.raises(ValueError, match=f"blocked_selected_content_{reason}"):
        _build(item=_item(title=value))


@pytest.mark.parametrize(
    ("source", "token", "count_field"),
    [
        ("Visit https://example.invalid/path now", "[REDACTED_URL]", "url"),
        ("Mail synthetic@example.invalid now", "[REDACTED_EMAIL]", "email"),
        ("Ask @synthetic_user now", "[REDACTED_HANDLE]", "handle"),
        ("Host 192.0.2.44 is synthetic", "[REDACTED_IP]", "ip"),
        ("Call +1 (555) 123-4567 now", "[REDACTED_PHONE]", "phone"),
        (r"Open C:\Users\synthetic\fixture.txt now", "[REDACTED_PATH]", "path"),
    ],
)
def test_each_sensitive_pattern_is_replaced_without_original(
    source: str, token: str, count_field: str
) -> None:
    card = _build(item=_item(title=source))

    assert token in card["review_text"]
    assert source not in card["review_text"]
    assert card["redaction_counts"][count_field] == 1
    assert tuple(card["redaction_counts"]) == ("url", "email", "handle", "ip", "phone", "path")


@pytest.mark.parametrize(
    ("case_index", "marker"),
    list(
        enumerate(
            [
                "Authorization:",
                "BEARER token",
                "api_key",
                "apikey",
                "access_token",
                "refresh_token",
                "password",
                "passwd",
                "secret",
                "cookie",
                "sessionid",
                "sk-value",
                "ghp_value",
                "github_pat_value",
                "AKIAvalue",
            ],
            start=1,
        )
    ),
)
def test_secret_like_markers_privacy_stop_without_matched_value(
    case_index: int, marker: str
) -> None:
    sentinel = (
        "SENTIGRAPH_RCI2_SYNTHETIC_SECRET_PAYLOAD_MUST_NOT_RETURN_"
        f"{case_index:02d}"
    )
    raw_source = f"synthetic {marker} {sentinel}"
    card = _build(item=_item(title=raw_source))

    assert card["privacy_stop"] is True
    assert card["review_text"] is None
    assert card["review_text_present"] is False
    assert card["review_text_utf8_bytes"] == 0
    assert card["privacy_stop_reasons"] == ["SECRET_LIKE_PATTERN_DETECTED"]
    assert card["secret_free_claimed"] is False
    assert card["pii_free_claimed"] is False
    assert raw_source not in repr(card)
    assert sentinel not in repr(card)
    assert all(value != raw_source for value in card.values())


def test_ascii_output_is_truncated_to_2048_utf8_bytes() -> None:
    card = _build(item=_item(title="x" * 3000))

    assert card["review_text_truncated"] is True
    assert card["review_text_utf8_bytes"] == 2048
    assert len(card["review_text"].encode("utf-8")) == 2048


def test_unicode_truncation_preserves_valid_utf8_boundary() -> None:
    card = _build(item=_item(title="界" * 1000))

    encoded = card["review_text"].encode("utf-8")
    assert card["review_text_truncated"] is True
    assert len(encoded) <= 2048
    assert encoded.decode("utf-8") == card["review_text"]


def test_safe_labels_and_receipt_statuses_are_preserved() -> None:
    card = _build()

    assert {field: card[field] for field in ("evidence_type", "language", "platform", "source_type")} == {
        "evidence_type": "comment",
        "language": "en",
        "platform": "synthetic_platform",
        "source_type": "manual_submission",
    }
    assert {field: card[field] for field in ("provenance_type", "acquisition_mode", "verification_status", "review_status")} == {
        "provenance_type": "manual_submission",
        "acquisition_mode": "user_upload",
        "verification_status": "needs_review",
        "review_status": "not_reviewed",
    }


def test_source_url_duplicate_value_and_all_forbidden_item_attributes_are_never_accessed() -> None:
    item = _item(model=_TrackingEvidenceItem)
    _TrackingEvidenceItem.blocked = set(FORBIDDEN_OUTPUT_FIELDS)
    try:
        card = _tracked_build(item, modality="title")
    finally:
        _TrackingEvidenceItem.blocked = set()

    assert card["source_url_present"] is True
    assert card["duplicate_group_present"] is False


def test_forbidden_evidenceitem_fields_are_absent_from_exact_output() -> None:
    card = _build()

    assert tuple(card) == OUTPUT_FIELDS
    assert FORBIDDEN_OUTPUT_FIELDS.isdisjoint(card)


def test_all_downstream_actions_and_semantic_verdicts_remain_false() -> None:
    card = _build()

    assert card["human_review_required"] is True
    assert card["no_automatic_trust_upgrade"] is True
    assert all(card[field] is False for field in DOWNSTREAM_FALSE_FIELDS)
    assert card["human_authority_validated_by_builder"] is False


def test_identical_safe_input_produces_identical_output() -> None:
    assert _build() == _build()


def test_privacy_stop_is_deterministic() -> None:
    item = _item(title="synthetic authorization: value")
    assert _build(item=item) == _build(item=item)


def test_raw_source_is_never_returned_as_a_separate_value() -> None:
    source = "Contact synthetic@example.invalid for review"
    card = _build(item=_item(title=source))

    assert source not in repr(card)
    assert set(card) == set(OUTPUT_FIELDS)


def test_alternate_redaction_policy_is_rejected() -> None:
    with pytest.raises(ValueError, match="blocked_redaction_policy_mismatch"):
        _build(policy="SYNTHETIC_ALTERNATE_POLICY")


@pytest.mark.parametrize("modality", ["", "body", "all", 1])
def test_unsupported_content_modality_is_rejected(modality: Any) -> None:
    with pytest.raises(ValueError, match="blocked_content_modality_unsupported"):
        _build(modality=modality)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("evidence_type", ""),
        ("language", "x" * 129),
        ("platform", "unsafe\x00label"),
        ("source_type", "unsafe\x85label"),
    ],
)
def test_unsafe_item_labels_fail_closed(field: str, value: str) -> None:
    with pytest.raises(ValueError, match=f"blocked_{field}_invalid"):
        _build(item=_item(**{field: value}))


@pytest.mark.parametrize("duplicate_group_id", [None, "synthetic-duplicate-group"])
def test_duplicate_context_uses_presence_only_without_count_evaluation(
    duplicate_group_id: str | None,
) -> None:
    card = _build(receipt=_receipt(duplicate_group_id=duplicate_group_id))

    assert card["duplicate_group_present"] is (duplicate_group_id is not None)
    assert card["duplicate_count_evaluated"] is False
    assert card["duplicate_context_class"] == (
        "duplicate_group_present_count_not_evaluated"
        if duplicate_group_id is not None
        else "no_duplicate_group"
    )
    assert duplicate_group_id is None or duplicate_group_id not in repr(card)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("selected_field_read_max", 2),
        ("maximum_output_utf8_bytes", 2047),
        ("raw_content_return_authorized", True),
        ("source_url_access_authorized", True),
        ("author_identity_access_authorized", True),
        ("raw_data_safe_access_authorized", True),
        ("ingestion_metadata_access_authorized", True),
        ("review_history_access_authorized", True),
        ("downstream_action_authorized", True),
    ],
)
def test_authority_limits_and_all_false_permissions_are_exact(
    field: str, value: Any
) -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_limits_mismatch"):
        _build(authority=_authority(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("exact_one_evidenceitem", False),
        ("read_only_verified", False),
        ("raw_evidence_content_included", True),
        ("raw_personal_identity_included", True),
    ],
)
def test_safe_receipt_authority_booleans_are_exact(field: str, value: bool) -> None:
    with pytest.raises(ValueError, match="blocked_safe_identity_receipt_authority_mismatch"):
        _build(receipt=_receipt(**{field: value}))


def test_receipt_reference_mismatch_fails() -> None:
    with pytest.raises(ValueError, match="blocked_safe_identity_receipt_reference_mismatch"):
        _build(receipt=_receipt(receipt_reference="eir-synthetic-wrong"))


@pytest.mark.parametrize("content_hash", ["A" * 64, "1" * 63, "z" * 64])
def test_receipt_content_hash_must_be_lowerhex64(content_hash: str) -> None:
    with pytest.raises(ValueError, match="blocked_content_hash_invalid"):
        _build(receipt=_receipt(content_hash=content_hash))


def test_non_evidenceitem_input_fails() -> None:
    with pytest.raises(ValueError, match="blocked_evidenceitem_model_mismatch"):
        build_existing_evidenceitem_final_linkage_target_review_card(
            object(),
            _receipt(),
            _authority(),
            content_modality="title",
            redaction_policy=POLICY,
        )


def test_lone_surrogate_selected_content_fails_utf8_validation() -> None:
    with pytest.raises(ValueError, match="blocked_selected_content_invalid_utf8"):
        _build(item=_item(title="synthetic \ud800"))


def test_linebreak_tabs_and_contiguous_unicode_whitespace_collapse() -> None:
    card = _build(item=_item(title="Synthetic\r\n\t review\u2003  text"))

    assert card["review_text"] == "Synthetic review text"


def test_card_declares_bounded_privacy_nonclaims() -> None:
    card = _build()

    assert card["privacy_review_required"] is True
    assert card["pii_free_claimed"] is False
    assert card["secret_free_claimed"] is False
    assert card["content_authority_binding_shape_validated"] is True
    assert card["human_authority_validated_by_builder"] is False
