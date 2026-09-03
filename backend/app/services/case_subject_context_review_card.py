from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any


_AUTHORITY_SCHEMA = (
    "sentigraph_case_subject_context_content_privacy_authority_binding_v0_1"
)
_AUTHORITY_VERSION = "0.1"
_AUTHORITY_SCOPE = (
    "one_exact_case_title_and_keyword_transient_subject_context_review_card"
)
_AUTHORITY_FIELDS = (
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
_FALSE_AUTHORITY_FIELDS = (
    "raw_content_return_authorized",
    "full_case_detail_access_authorized",
    "project_metadata_access_authorized",
    "evidence_items_access_authorized",
    "raw_posts_comments_access_authorized",
    "analysis_report_access_authorized",
    "monitoring_metadata_access_authorized",
    "downstream_action_authorized",
)

_REDACTION_POLICY = "SENTIGRAPH_CASE_SUBJECT_CONTEXT_BOUNDED_REDACTION_V0_1"
_REVIEW_CARD_SCHEMA = "sentigraph_case_subject_context_review_card_v0_1"
_REVIEW_CARD_VERSION = "0.1"
_REVIEW_CARD_MODE = (
    "internal_pure_in_memory_nonpersistent_nonauthorizing_case_subject_context_"
    "review_card"
)
_OUTPUT_FIELDS = (
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
_DOWNSTREAM_FALSE_FIELDS = (
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
_REDACTION_COUNT_FIELDS = ("url", "email", "handle", "ip", "phone", "path")
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


class _CaseSubjectReviewCardContractError(ValueError):
    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _fail(outcome: str) -> None:
    raise _CaseSubjectReviewCardContractError(outcome)


def _validate_case_id(value: Any) -> str:
    if type(value) is not str or value == "":
        _fail("blocked_case_id_invalid")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail("blocked_case_id_invalid_utf8")
    if len(encoded) > 512:
        _fail("blocked_case_id_oversized")
    if any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in value):
        _fail("blocked_case_id_control")
    return value


def _validate_authority_reference(value: Any) -> str:
    if type(value) is not str or value == "":
        _fail("blocked_authority_receipt_reference_invalid")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail("blocked_authority_receipt_reference_invalid_utf8")
    if len(encoded) > 512:
        _fail("blocked_authority_receipt_reference_oversized")
    if any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in value):
        _fail("blocked_authority_receipt_reference_control")
    return value


def _validate_subject_text(value: Any, *, field_name: str) -> str:
    if type(value) is not str:
        _fail(f"blocked_{field_name}_non_string")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError:
        _fail(f"blocked_{field_name}_invalid_utf8")
    if len(encoded) > 16384:
        _fail(f"blocked_{field_name}_oversized")
    for character in value:
        codepoint = ord(character)
        if codepoint == 0:
            _fail(f"blocked_{field_name}_nul")
        if (codepoint < 32 and character not in "\t\r\n") or 127 <= codepoint <= 159:
            _fail(f"blocked_{field_name}_control")
    if not any(not character.isspace() for character in value):
        _fail(f"blocked_{field_name}_empty")
    return value


def _validate_authority_binding(
    binding: Mapping[str, Any], *, case_id: str
) -> str:
    if not isinstance(binding, Mapping) or set(binding) != set(_AUTHORITY_FIELDS):
        _fail("blocked_content_authority_binding_contract_mismatch")
    if (
        binding["schema"] != _AUTHORITY_SCHEMA
        or binding["version"] != _AUTHORITY_VERSION
        or binding["scope"] != _AUTHORITY_SCOPE
    ):
        _fail("blocked_content_authority_binding_contract_mismatch")
    if binding["case_id"] != case_id:
        _fail("blocked_content_authority_binding_case_id_mismatch")
    if binding["authorized_subject_fields"] != ["title", "keyword"]:
        _fail("blocked_content_authority_binding_subject_fields_mismatch")
    if (
        type(binding["title_read_max"]) is not int
        or binding["title_read_max"] != 1
        or type(binding["keyword_read_max"]) is not int
        or binding["keyword_read_max"] != 1
        or type(binding["maximum_source_utf8_bytes_per_field"]) is not int
        or binding["maximum_source_utf8_bytes_per_field"] != 16384
        or type(binding["maximum_output_utf8_bytes_per_field"]) is not int
        or binding["maximum_output_utf8_bytes_per_field"] != 2048
        or any(binding[field] is not False for field in _FALSE_AUTHORITY_FIELDS)
    ):
        _fail("blocked_content_authority_binding_limits_mismatch")
    return _validate_authority_reference(binding["authority_receipt_reference"])


def _truncate_utf8(value: str, maximum_bytes: int) -> tuple[str, bool]:
    encoded = value.encode("utf-8")
    if len(encoded) <= maximum_bytes:
        return value, False
    return encoded[:maximum_bytes].decode("utf-8", errors="ignore"), True


def _redact_subject_field(value: str, *, field_name: str) -> dict[str, Any]:
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    counts = {field: 0 for field in _REDACTION_COUNT_FIELDS}
    if any(marker in normalized.casefold() for marker in _SECRET_MARKERS):
        return {
            "review_text": None,
            "review_text_present": False,
            "review_text_utf8_bytes": 0,
            "review_text_truncated": False,
            "redaction_counts": counts,
            "privacy_stop_reason": f"{field_name.upper()}_SECRET_LIKE_PATTERN_DETECTED",
        }

    redacted = normalized
    for count_field, pattern, token in _REDACTION_PATTERNS:
        redacted, count = pattern.subn(token, redacted)
        counts[count_field] = count
    redacted = re.sub(r"\s+", " ", redacted).strip()
    if redacted == "":
        return {
            "review_text": None,
            "review_text_present": False,
            "review_text_utf8_bytes": 0,
            "review_text_truncated": False,
            "redaction_counts": counts,
            "privacy_stop_reason": f"{field_name.upper()}_EMPTY_AFTER_REDACTION",
        }
    review_text, truncated = _truncate_utf8(redacted, 2048)
    return {
        "review_text": review_text,
        "review_text_present": True,
        "review_text_utf8_bytes": len(review_text.encode("utf-8")),
        "review_text_truncated": truncated,
        "redaction_counts": counts,
        "privacy_stop_reason": None,
    }


def build_case_subject_context_review_card(
    case_id: str,
    title: str,
    keyword: str,
    content_privacy_authority_binding: Mapping[str, Any],
    *,
    redaction_policy: str,
) -> dict[str, Any]:
    """Build one bounded case-subject card without storage or side effects."""

    validated_case_id = _validate_case_id(case_id)
    validated_title = _validate_subject_text(title, field_name="title")
    validated_keyword = _validate_subject_text(keyword, field_name="keyword")
    authority_reference = _validate_authority_binding(
        content_privacy_authority_binding, case_id=validated_case_id
    )
    if redaction_policy != _REDACTION_POLICY:
        _fail("blocked_redaction_policy_mismatch")

    title_redaction = _redact_subject_field(validated_title, field_name="title")
    keyword_redaction = _redact_subject_field(validated_keyword, field_name="keyword")
    privacy_stop_reasons = [
        reason
        for reason in (
            title_redaction["privacy_stop_reason"],
            keyword_redaction["privacy_stop_reason"],
        )
        if reason is not None
    ]
    privacy_stop = bool(privacy_stop_reasons)
    if privacy_stop:
        title_output = {
            "review_text": None,
            "review_text_present": False,
            "review_text_utf8_bytes": 0,
            "review_text_truncated": False,
        }
        keyword_output = {**title_output}
    else:
        title_output = title_redaction
        keyword_output = keyword_redaction

    values: dict[str, Any] = {
        "schema": _REVIEW_CARD_SCHEMA,
        "version": _REVIEW_CARD_VERSION,
        "mode": _REVIEW_CARD_MODE,
        "content_privacy_authority_receipt_reference": authority_reference,
        "case_id": validated_case_id,
        "subject_fields": ["title", "keyword"],
        "title_review_text": title_output["review_text"],
        "title_review_text_present": title_output["review_text_present"],
        "title_review_text_utf8_bytes": title_output["review_text_utf8_bytes"],
        "title_review_text_truncated": title_output["review_text_truncated"],
        "keyword_review_text": keyword_output["review_text"],
        "keyword_review_text_present": keyword_output["review_text_present"],
        "keyword_review_text_utf8_bytes": keyword_output["review_text_utf8_bytes"],
        "keyword_review_text_truncated": keyword_output["review_text_truncated"],
        "redaction_policy": _REDACTION_POLICY,
        "title_redaction_counts": title_redaction["redaction_counts"],
        "keyword_redaction_counts": keyword_redaction["redaction_counts"],
        "privacy_stop": privacy_stop,
        "privacy_stop_reasons": privacy_stop_reasons,
        "privacy_review_required": True,
        "pii_free_claimed": False,
        "secret_free_claimed": False,
        "case_id_validated": True,
        "title_type_validated": True,
        "keyword_type_validated": True,
        "title_read_max": 1,
        "keyword_read_max": 1,
        "content_authority_binding_shape_validated": True,
        "human_authority_validated_by_builder": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in _DOWNSTREAM_FALSE_FIELDS},
    }
    if tuple(values) != _OUTPUT_FIELDS or len(values) != 44:
        _fail("blocked_review_card_output_contract_mismatch")
    return {field: values[field] for field in _OUTPUT_FIELDS}
