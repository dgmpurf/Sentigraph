from __future__ import annotations

import ast
import inspect
from typing import Any

import pytest

import app.services.case_subject_context_review_card as review_card_module
from app.services.case_subject_context_review_card import (
    build_case_subject_context_review_card,
)


CASE_ID = "synthetic_case_subject_001"
POLICY = "SENTIGRAPH_CASE_SUBJECT_CONTEXT_BOUNDED_REDACTION_V0_1"
AUTHORITY_FIELDS = (
    "schema",
    "version",
    "scope",
    "authority_receipt_reference",
    "case_id",
    "authorized_subject_fields",
    "title_read_max",
    "keyword_read_max",
    "maximum_source_utf8_bytes_per_field",
    "maximum_output_utf8_bytes_per_field",
    "raw_content_return_authorized",
    "full_case_detail_access_authorized",
    "project_metadata_access_authorized",
    "evidence_items_access_authorized",
    "raw_posts_comments_access_authorized",
    "analysis_report_access_authorized",
    "monitoring_metadata_access_authorized",
    "downstream_action_authorized",
)
OUTPUT_FIELDS = (
    "schema",
    "version",
    "mode",
    "content_privacy_authority_receipt_reference",
    "case_id",
    "subject_fields",
    "title_review_text",
    "title_review_text_present",
    "title_review_text_utf8_bytes",
    "title_review_text_truncated",
    "keyword_review_text",
    "keyword_review_text_present",
    "keyword_review_text_utf8_bytes",
    "keyword_review_text_truncated",
    "redaction_policy",
    "title_redaction_counts",
    "keyword_redaction_counts",
    "privacy_stop",
    "privacy_stop_reasons",
    "privacy_review_required",
    "pii_free_claimed",
    "secret_free_claimed",
    "case_id_validated",
    "title_type_validated",
    "keyword_type_validated",
    "title_read_max",
    "keyword_read_max",
    "content_authority_binding_shape_validated",
    "human_authority_validated_by_builder",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "semantic_relevance_adjudicated",
    "exact_decision_subject_binding_established",
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
    "exact_decision_subject_binding_established",
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


def _authority(**updates: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "schema": "sentigraph_case_subject_context_content_privacy_authority_binding_v0_1",
        "version": "0.1",
        "scope": "one_exact_case_title_and_keyword_transient_subject_context_review_card",
        "authority_receipt_reference": "synthetic-case-subject-authority-001",
        "case_id": CASE_ID,
        "authorized_subject_fields": ["title", "keyword"],
        "title_read_max": 1,
        "keyword_read_max": 1,
        "maximum_source_utf8_bytes_per_field": 16384,
        "maximum_output_utf8_bytes_per_field": 2048,
        "raw_content_return_authorized": False,
        "full_case_detail_access_authorized": False,
        "project_metadata_access_authorized": False,
        "evidence_items_access_authorized": False,
        "raw_posts_comments_access_authorized": False,
        "analysis_report_access_authorized": False,
        "monitoring_metadata_access_authorized": False,
        "downstream_action_authorized": False,
    }
    values.update(updates)
    return {field: values[field] for field in AUTHORITY_FIELDS}


def _build(
    *,
    case_id: Any = CASE_ID,
    title: Any = "Synthetic public update request",
    keyword: Any = "Synthetic game account policy",
    authority: Any = None,
    policy: str = POLICY,
) -> dict[str, Any]:
    return build_case_subject_context_review_card(
        case_id,
        title,
        keyword,
        _authority() if authority is None else authority,
        redaction_policy=policy,
    )


def test_valid_title_and_keyword_card_has_exact_44_field_contract() -> None:
    card = _build()

    assert tuple(card) == OUTPUT_FIELDS
    assert len(card) == 44
    assert card["schema"] == "sentigraph_case_subject_context_review_card_v0_1"
    assert card["subject_fields"] == ["title", "keyword"]
    assert card["title_review_text"] == "Synthetic public update request"
    assert card["keyword_review_text"] == "Synthetic game account policy"
    assert card["privacy_stop"] is False
    assert card["privacy_stop_reasons"] == []
    assert card["content_authority_binding_shape_validated"] is True
    assert card["human_authority_validated_by_builder"] is False


@pytest.mark.parametrize("operation", ["missing", "extra"])
def test_authority_requires_exact_field_set(operation: str) -> None:
    authority = _authority()
    if operation == "missing":
        authority.pop("scope")
    else:
        authority["extra"] = False

    with pytest.raises(ValueError, match="blocked_content_authority_binding_contract_mismatch"):
        _build(authority=authority)


def test_authority_case_id_must_match() -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_case_id_mismatch"):
        _build(authority=_authority(case_id="synthetic_case_other"))


@pytest.mark.parametrize(
    "subject_fields",
    [["keyword", "title"], ["title"], ["title", "keyword", "other"], ("title", "keyword")],
)
def test_authorized_subject_fields_require_exact_list_and_order(subject_fields: Any) -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_subject_fields_mismatch"):
        _build(authority=_authority(authorized_subject_fields=subject_fields))


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("title_read_max", 2),
        ("keyword_read_max", 0),
        ("maximum_source_utf8_bytes_per_field", 16383),
        ("maximum_output_utf8_bytes_per_field", 2049),
        ("raw_content_return_authorized", True),
        ("full_case_detail_access_authorized", True),
        ("project_metadata_access_authorized", True),
        ("evidence_items_access_authorized", True),
        ("raw_posts_comments_access_authorized", True),
        ("analysis_report_access_authorized", True),
        ("monitoring_metadata_access_authorized", True),
        ("downstream_action_authorized", True),
    ],
)
def test_authority_limits_and_false_permissions_are_exact(field: str, value: Any) -> None:
    with pytest.raises(ValueError, match="blocked_content_authority_binding_limits_mismatch"):
        _build(authority=_authority(**{field: value}))


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("case_id", object(), "blocked_case_id_invalid"),
        ("title", object(), "blocked_title_non_string"),
        ("keyword", object(), "blocked_keyword_non_string"),
    ],
)
def test_case_and_subject_inputs_require_exact_strings(
    field: str, value: Any, reason: str
) -> None:
    kwargs = {field: value}
    with pytest.raises(ValueError, match=reason):
        _build(**kwargs)


@pytest.mark.parametrize("field", ["title", "keyword"])
@pytest.mark.parametrize("value", ["", " \t\r\n ", "\u2003\u2009"])
def test_title_and_keyword_reject_empty_or_unicode_whitespace(
    field: str, value: str
) -> None:
    with pytest.raises(ValueError, match=f"blocked_{field}_empty"):
        _build(**{field: value})


@pytest.mark.parametrize("field", ["title", "keyword"])
def test_title_and_keyword_enforce_source_size_ceiling(field: str) -> None:
    with pytest.raises(ValueError, match=f"blocked_{field}_oversized"):
        _build(**{field: "x" * 16385})


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("title", "synthetic\x00value", "nul"),
        ("keyword", "synthetic\x00value", "nul"),
        ("title", "synthetic\x01value", "control"),
        ("keyword", "synthetic\x85value", "control"),
    ],
)
def test_nul_and_disallowed_controls_fail(
    field: str, value: str, reason: str
) -> None:
    with pytest.raises(ValueError, match=f"blocked_{field}_{reason}"):
        _build(**{field: value})


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
def test_title_redacts_all_six_pattern_classes(
    source: str, token: str, count_field: str
) -> None:
    card = _build(title=source)
    assert token in card["title_review_text"]
    assert source not in card["title_review_text"]
    assert card["title_redaction_counts"][count_field] == 1
    assert tuple(card["title_redaction_counts"]) == (
        "url",
        "email",
        "handle",
        "ip",
        "phone",
        "path",
    )


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
def test_keyword_redacts_all_six_pattern_classes(
    source: str, token: str, count_field: str
) -> None:
    card = _build(keyword=source)
    assert token in card["keyword_review_text"]
    assert source not in card["keyword_review_text"]
    assert card["keyword_redaction_counts"][count_field] == 1
    assert tuple(card["keyword_redaction_counts"]) == (
        "url",
        "email",
        "handle",
        "ip",
        "phone",
        "path",
    )


def test_title_secret_causes_overall_privacy_stop_and_nulls_both_texts() -> None:
    sentinel = "SENTIGRAPH_SYNTHETIC_TITLE_SECRET_MUST_NOT_RETURN"
    card = _build(title=f"synthetic authorization: {sentinel}")

    assert card["privacy_stop"] is True
    assert card["privacy_stop_reasons"] == ["TITLE_SECRET_LIKE_PATTERN_DETECTED"]
    _assert_both_texts_nulled(card)
    assert sentinel not in repr(card)


def test_keyword_secret_causes_overall_privacy_stop_and_nulls_both_texts() -> None:
    sentinel = "SENTIGRAPH_SYNTHETIC_KEYWORD_SECRET_MUST_NOT_RETURN"
    card = _build(keyword=f"synthetic bearer {sentinel}")

    assert card["privacy_stop"] is True
    assert card["privacy_stop_reasons"] == ["KEYWORD_SECRET_LIKE_PATTERN_DETECTED"]
    _assert_both_texts_nulled(card)
    assert sentinel not in repr(card)


def test_both_secret_reasons_use_title_then_keyword_canonical_order() -> None:
    card = _build(title="synthetic api_key value", keyword="synthetic cookie value")

    assert card["privacy_stop_reasons"] == [
        "TITLE_SECRET_LIKE_PATTERN_DETECTED",
        "KEYWORD_SECRET_LIKE_PATTERN_DETECTED",
    ]
    _assert_both_texts_nulled(card)


@pytest.mark.parametrize("field", ["title", "keyword"])
def test_empty_after_redaction_branch_is_fail_closed(field: str) -> None:
    redaction = review_card_module._redact_subject_field(" \t\r\n ", field_name=field)

    assert redaction["review_text"] is None
    assert redaction["review_text_present"] is False
    assert redaction["review_text_utf8_bytes"] == 0
    assert redaction["review_text_truncated"] is False
    assert redaction["privacy_stop_reason"] == f"{field.upper()}_EMPTY_AFTER_REDACTION"


def test_title_and_keyword_truncate_independently_on_valid_utf8_boundaries() -> None:
    title_card = _build(title="界" * 1000, keyword="short keyword")
    keyword_card = _build(title="short title", keyword="界" * 1000)

    assert title_card["title_review_text_truncated"] is True
    assert title_card["keyword_review_text_truncated"] is False
    assert len(title_card["title_review_text"].encode("utf-8")) <= 2048
    assert title_card["title_review_text"].encode("utf-8").decode("utf-8") == title_card["title_review_text"]
    assert keyword_card["keyword_review_text_truncated"] is True
    assert keyword_card["title_review_text_truncated"] is False
    assert len(keyword_card["keyword_review_text"].encode("utf-8")) <= 2048
    assert keyword_card["keyword_review_text"].encode("utf-8").decode("utf-8") == keyword_card["keyword_review_text"]


def test_raw_sensitive_source_is_never_returned_separately() -> None:
    raw_title = "Contact synthetic@example.invalid for title review"
    raw_keyword = "Visit https://example.invalid/private for keyword review"
    card = _build(title=raw_title, keyword=raw_keyword)

    assert raw_title not in repr(card)
    assert raw_keyword not in repr(card)
    assert set(card) == set(OUTPUT_FIELDS)


def test_full_case_object_is_not_accepted() -> None:
    full_case_like = object()
    with pytest.raises(ValueError, match="blocked_case_id_invalid"):
        _build(case_id=full_case_like)


def test_all_governance_and_downstream_flags_remain_false() -> None:
    card = _build()

    assert card["privacy_review_required"] is True
    assert card["pii_free_claimed"] is False
    assert card["secret_free_claimed"] is False
    assert card["human_review_required"] is True
    assert card["no_automatic_trust_upgrade"] is True
    assert all(card[field] is False for field in DOWNSTREAM_FALSE_FIELDS)


def test_identical_synthetic_input_produces_identical_output() -> None:
    assert _build() == _build()


def test_alternate_redaction_policy_is_rejected() -> None:
    with pytest.raises(ValueError, match="blocked_redaction_policy_mismatch"):
        _build(policy="SENTIGRAPH_ALTERNATE_POLICY")


def test_private_evidenceitem_helpers_and_forbidden_imports_are_absent() -> None:
    source = inspect.getsource(review_card_module)
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }

    assert "existing_evidenceitem_final_linkage_target_review_card" not in source
    assert "_redact_selected_source" not in source
    assert not any(
        token in imported
        for token in {
            "CaseRepository",
            "CaseStore",
            "EvidenceItem",
            "fastapi",
            "pathlib",
            "subprocess",
            "socket",
            "requests",
            "httpx",
        }
    )


def test_no_io_or_broad_object_serialization_calls_exist() -> None:
    tree = ast.parse(inspect.getsource(review_card_module))
    forbidden_names = {
        "open",
        "model_dump",
        "dict",
        "vars",
        "__dict__",
        "get_case",
        "list_cases",
        "urlopen",
        "run",
        "Popen",
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    accessed_attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }

    assert forbidden_names.isdisjoint(called_names)
    assert {"model_dump", "__dict__"}.isdisjoint(accessed_attributes)


def _assert_both_texts_nulled(card: dict[str, Any]) -> None:
    for prefix in ("title", "keyword"):
        assert card[f"{prefix}_review_text"] is None
        assert card[f"{prefix}_review_text_present"] is False
        assert card[f"{prefix}_review_text_utf8_bytes"] == 0
        assert card[f"{prefix}_review_text_truncated"] is False
