from __future__ import annotations

from datetime import datetime
from typing import Any

from app.services import protected_value_boundary_scanner as _scanner


AUDIT_SCHEMA = "sentigraph_safe_payload_receipt_acceptance_audit_v0_1"
AUDIT_VERSION = "0.1"

RECEIPT_SCHEMA = "sentigraph_mvp_f03_real_safe_payload_capture_receipt_v1_0"
RECEIPT_VERSION = "1.0"
PAYLOAD_SCHEMA = "sentigraph_exact_locked_candidate_safe_write_payload_v0_1"
PAYLOAD_VERSION = "0.1"
RECEIPT_CLASSIFICATION = "safe_local_nonproduction_metadata_only"
REMEDIATION_CONTEXT = "MVP_C02_P2_separately_governed_remediation_capture"

FINDING_CATEGORIES = (
    "missing_required_field",
    "disallowed_extension_field",
    "invalid_field_type",
    "floating_value_present",
    "receipt_arithmetic_mismatch",
    "negative_proof_state_violation",
    "scanner_contract_mismatch",
    "payload_cross_binding_mismatch",
    "remediation_context_mismatch",
)

NEGATIVE_PROOF_FIELDS = frozenset(
    {
        "raw_row_retained",
        "raw_author_identity_retained",
        "absolute_path_recorded",
        "production_object_created",
        "database_accessed",
        "network_called",
        "gate_activated",
        "persistence_mutation_performed",
        "directory_enumeration_performed",
        "alternate_source_used",
    }
)

_STRING_FIELDS = frozenset(
    {
        "receipt_schema",
        "receipt_version",
        "milestone_id",
        "capture_session_id",
        "capture_started_at",
        "capture_completed_at",
        "source_file_open_mode",
        "payload_schema",
        "payload_version",
        "payload_safe_hash",
        "final_outcome",
    }
)
_INTEGER_FIELDS = frozenset(
    {
        "source_file_open_count",
        "source_file_reopen_count",
        "source_line_utf8_byte_limit",
        "source_line_probe_read_size",
        "source_read_call_count",
        "source_line_bytes_read",
        "rows_examined_or_parsed",
        "rows_selected",
        "payload_artifact_count",
        "receipt_artifact_count",
    }
)
_BOOLEAN_FIELDS = frozenset(
    {
        "source_access_session_consumed",
        "source_line_terminator_counted_in_limit",
        "oversized_source_line_detected",
        "UTF8_decode_attempted",
        "UTF8_decode_passed",
        "JSON_parse_attempted",
        "duplicate_JSON_key_detected",
        "nonstandard_numeric_constant_detected",
        "strict_JSON_parse_passed",
        "top_level_JSON_object_verified",
        "directory_enumeration_performed",
        "alternate_source_used",
        "approved_package_binding_verified",
        "approved_row_source_verified",
        "row_selector_verified",
        "row_hash_verified",
        "candidate_binding_verified",
        "forbidden_field_scan_passed",
        "protected_value_scan_passed",
        "raw_row_retained",
        "raw_author_identity_retained",
        "absolute_path_recorded",
        "production_object_created",
        "database_accessed",
        "network_called",
        "gate_activated",
        "persistence_mutation_performed",
    }
)
CORE_REQUIRED_FIELDS = frozenset(
    _STRING_FIELDS | _INTEGER_FIELDS | _BOOLEAN_FIELDS | {"pause_reason"}
)

_CONTRACTED_STRING_EXTENSIONS = frozenset(
    {"receipt_classification", "remediation_context", "scanner_module_sha256"}
)
_CONTRACTED_INTEGER_EXTENSIONS = frozenset(
    {
        "remediation_capture_execution_limit",
        "remediation_capture_execution_count",
        "physical_JSONL_record_selected",
        "candidate_chain_stage_count",
        "payload_top_level_field_count",
        "payload_field_paths_contract_count",
    }
)
_CONTRACTED_TRUE_EXTENSIONS = frozenset(
    {
        "new_remediation_source_session_authorized",
        "remediation_source_session_consumed",
        "candidate_chain_all_singleton",
        "payload_validator_passed",
        "payload_validator_exact_equality",
        "payload_scanner_passed",
    }
)
_CONTRACTED_FALSE_EXTENSIONS = frozenset(
    {
        "source_second_read_performed",
        "source_seek_performed",
        "fallback_used",
        "automatic_retry_performed",
        "historical_F03_retry",
        "historical_F03_reclassified",
        "receipt_historical_F03_reclassified",
        "parser_exception_exposed",
        "candidate_substitution_performed",
        "package_or_row_substitution_performed",
        "protected_value_exposed",
        "raw_key_echoed",
        "raw_value_echoed",
        "production_evidenceitem_created",
        "production_case_created",
        "production_analysis_run_created",
        "production_analysis_result_created",
        "source11_runtime_called",
        "public_or_delivery_runtime_called",
        "provider_or_collector_called",
        "duplicate_copy_created",
        "runtime_artifact_staged",
        "third_runtime_artifact_created_by_process",
    }
)
_CONTRACTED_EXTENSIONS = frozenset(
    _CONTRACTED_STRING_EXTENSIONS
    | _CONTRACTED_INTEGER_EXTENSIONS
    | _CONTRACTED_TRUE_EXTENSIONS
    | _CONTRACTED_FALSE_EXTENSIONS
)

_DANGEROUS_EXTENSION_FRAGMENTS = (
    "authoriz",
    "approval_granted",
    "approved_for",
    "create_production",
    "delivery_enabled",
    "execute_now",
    "execution_allowed",
    "gate_activation_allowed",
    "mutation_allowed",
    "official_verified",
    "persist_now",
    "persistence_allowed",
    "production_ready",
    "publish",
    "trust_upgrade",
    "write_allowed",
    "write_enabled",
)
_MAX_DEPTH = 64
_MAX_EXTENSION_KEY_LENGTH = 80


def audit_safe_capture_receipt(
    receipt: Any,
    *,
    expected_payload_safe_hash: str,
    expected_milestone_id: str,
    expected_source_line_bytes_read: int,
    expected_final_outcome: str,
) -> dict[str, Any]:
    """Audit one parsed safe receipt without IO or unsafe diagnostic echo."""

    try:
        return _audit_safe_capture_receipt(
            receipt,
            expected_payload_safe_hash=expected_payload_safe_hash,
            expected_milestone_id=expected_milestone_id,
            expected_source_line_bytes_read=expected_source_line_bytes_read,
            expected_final_outcome=expected_final_outcome,
        )
    except Exception:
        return _build_result(invalid_field_type_count=1)


def _audit_safe_capture_receipt(
    receipt: Any,
    *,
    expected_payload_safe_hash: str,
    expected_milestone_id: str,
    expected_source_line_bytes_read: int,
    expected_final_outcome: str,
) -> dict[str, Any]:
    if type(receipt) is not dict:
        return _build_result(invalid_field_type_count=1)

    missing_count = sum(1 for field in CORE_REQUIRED_FIELDS if field not in receipt)
    disallowed_extension_count = _count_disallowed_extensions(receipt)
    structural_float_count, structural_invalid_count = _inspect_json_structure(
        receipt,
        depth=0,
        active_ids=frozenset(),
    )
    invalid_type_count = structural_invalid_count + _count_invalid_core_types(receipt)
    invalid_type_count += _count_invalid_contracted_extension_types(receipt)

    negative_count = _count_negative_proof_violations(receipt)
    arithmetic_count = _count_arithmetic_mismatches(
        receipt,
        expected_source_line_bytes_read=expected_source_line_bytes_read,
        expected_final_outcome=expected_final_outcome,
    )
    payload_binding_count = _count_payload_binding_mismatches(
        receipt,
        expected_payload_safe_hash=expected_payload_safe_hash,
    )
    remediation_count = _count_remediation_context_mismatches(
        receipt,
        expected_milestone_id=expected_milestone_id,
    )

    scanner_result = _scanner.scan_protected_value_boundary(
        receipt,
        profile=_scanner.SAFE_CAPTURE_RECEIPT_PROFILE,
    )
    scanner_count = _count_scanner_contract_mismatches(receipt, scanner_result)

    return _build_result(
        missing_required_field_count=missing_count,
        disallowed_extension_field_count=disallowed_extension_count,
        invalid_field_type_count=invalid_type_count,
        floating_value_count=structural_float_count,
        arithmetic_mismatch_count=arithmetic_count,
        negative_proof_violation_count=negative_count,
        scanner_contract_mismatch_count=scanner_count,
        payload_cross_binding_mismatch_count=payload_binding_count,
        remediation_context_mismatch_count=remediation_count,
    )


def _count_invalid_core_types(receipt: dict[str, Any]) -> int:
    count = 0
    for field in _STRING_FIELDS:
        if field in receipt and type(receipt[field]) is not str:
            count += 1
    for field in _INTEGER_FIELDS:
        if field in receipt and type(receipt[field]) is not int:
            count += 1
    for field in _BOOLEAN_FIELDS:
        if field in receipt and type(receipt[field]) is not bool:
            count += 1
    if "pause_reason" in receipt and receipt["pause_reason"] is not None:
        if type(receipt["pause_reason"]) is not str:
            count += 1
    return count


def _count_invalid_contracted_extension_types(receipt: dict[str, Any]) -> int:
    count = 0
    for field in _CONTRACTED_STRING_EXTENSIONS:
        if field in receipt and type(receipt[field]) is not str:
            count += 1
    for field in _CONTRACTED_INTEGER_EXTENSIONS:
        if field in receipt and type(receipt[field]) is not int:
            count += 1
    for field in _CONTRACTED_TRUE_EXTENSIONS | _CONTRACTED_FALSE_EXTENSIONS:
        if field in receipt and type(receipt[field]) is not bool:
            count += 1
    return count


def _count_disallowed_extensions(receipt: dict[str, Any]) -> int:
    count = 0
    for key in receipt:
        if key in CORE_REQUIRED_FIELDS or key in _CONTRACTED_EXTENSIONS:
            continue
        if type(key) is not str or not _is_bounded_ascii_identifier(key):
            count += 1
            continue
        normalized = key.casefold()
        if key in _scanner._FORBIDDEN_KEYS or any(
            fragment in normalized for fragment in _DANGEROUS_EXTENSION_FRAGMENTS
        ):
            count += 1
    return count


def _is_bounded_ascii_identifier(value: str) -> bool:
    if not value or len(value) > _MAX_EXTENSION_KEY_LENGTH or not value.isascii():
        return False
    if not (value[0].isalpha() or value[0] == "_"):
        return False
    return all(character.isalnum() or character == "_" for character in value)


def _inspect_json_structure(
    value: Any,
    *,
    depth: int,
    active_ids: frozenset[int],
) -> tuple[int, int]:
    if depth > _MAX_DEPTH:
        return 0, 1
    if isinstance(value, float):
        return 1, 0
    if value is None or type(value) in {str, bool, int}:
        return 0, 0
    if type(value) is dict:
        container_id = id(value)
        if container_id in active_ids:
            return 0, 1
        next_ids = active_ids | {container_id}
        floats = 0
        invalid = 0
        for key, nested in value.items():
            if type(key) is not str:
                invalid += 1
            nested_floats, nested_invalid = _inspect_json_structure(
                nested,
                depth=depth + 1,
                active_ids=next_ids,
            )
            floats += nested_floats
            invalid += nested_invalid
        return floats, invalid
    if type(value) is list:
        container_id = id(value)
        if container_id in active_ids:
            return 0, 1
        next_ids = active_ids | {container_id}
        floats = 0
        invalid = 0
        for nested in value:
            nested_floats, nested_invalid = _inspect_json_structure(
                nested,
                depth=depth + 1,
                active_ids=next_ids,
            )
            floats += nested_floats
            invalid += nested_invalid
        return floats, invalid
    return 0, 1


def _count_negative_proof_violations(receipt: dict[str, Any]) -> int:
    count = sum(1 for field in NEGATIVE_PROOF_FIELDS if receipt.get(field) is not False)
    for field in _CONTRACTED_FALSE_EXTENSIONS:
        if field in receipt and receipt[field] is not False:
            count += 1
    return count


def _count_arithmetic_mismatches(
    receipt: dict[str, Any],
    *,
    expected_source_line_bytes_read: int,
    expected_final_outcome: str,
) -> int:
    count = 0
    exact_values = (
        ("source_access_session_consumed", True),
        ("source_file_open_count", 1),
        ("source_read_call_count", 1),
        ("source_file_reopen_count", 0),
        ("source_file_open_mode", "binary_read_only"),
        ("source_line_utf8_byte_limit", 1048576),
        ("source_line_probe_read_size", 1048577),
        ("source_line_bytes_read", expected_source_line_bytes_read),
        ("source_line_terminator_counted_in_limit", True),
        ("oversized_source_line_detected", False),
        ("UTF8_decode_attempted", True),
        ("UTF8_decode_passed", True),
        ("JSON_parse_attempted", True),
        ("duplicate_JSON_key_detected", False),
        ("nonstandard_numeric_constant_detected", False),
        ("strict_JSON_parse_passed", True),
        ("top_level_JSON_object_verified", True),
        ("rows_examined_or_parsed", 1),
        ("rows_selected", 1),
        ("payload_artifact_count", 1),
        ("receipt_artifact_count", 1),
        ("approved_package_binding_verified", True),
        ("approved_row_source_verified", True),
        ("row_selector_verified", True),
        ("row_hash_verified", True),
        ("candidate_binding_verified", True),
        ("final_outcome", expected_final_outcome),
        ("pause_reason", None),
    )
    for field, expected in exact_values:
        if field in receipt and _has_expected_type(field, receipt[field]):
            if receipt[field] != expected:
                count += 1

    started = _parse_utc(receipt.get("capture_started_at"))
    completed = _parse_utc(receipt.get("capture_completed_at"))
    if type(receipt.get("capture_started_at")) is str and started is None:
        count += 1
    if type(receipt.get("capture_completed_at")) is str and completed is None:
        count += 1
    if started is not None and completed is not None and completed < started:
        count += 1

    session_id = receipt.get("capture_session_id")
    if type(session_id) is str and not _is_safe_opaque_id(session_id):
        count += 1
    return count


def _has_expected_type(field: str, value: Any) -> bool:
    if field in _STRING_FIELDS:
        return type(value) is str
    if field in _INTEGER_FIELDS:
        return type(value) is int
    if field in _BOOLEAN_FIELDS:
        return type(value) is bool
    if field == "pause_reason":
        return value is None or type(value) is str
    return True


def _parse_utc(value: Any) -> datetime | None:
    if type(value) is not str or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    if parsed.utcoffset().total_seconds() != 0:
        return None
    return parsed


def _is_safe_opaque_id(value: str) -> bool:
    if not 3 <= len(value) <= 160 or not value.isascii():
        return False
    if not value[0].isalnum():
        return False
    return all(character.isalnum() or character in "._:-" for character in value)


def _count_payload_binding_mismatches(
    receipt: dict[str, Any],
    *,
    expected_payload_safe_hash: str,
) -> int:
    count = 0
    exact_values = (
        ("payload_schema", PAYLOAD_SCHEMA),
        ("payload_version", PAYLOAD_VERSION),
        ("payload_safe_hash", expected_payload_safe_hash),
        ("payload_artifact_count", 1),
        ("receipt_artifact_count", 1),
    )
    for field, expected in exact_values:
        if field in receipt and _has_expected_type(field, receipt[field]):
            if receipt[field] != expected:
                count += 1
    if type(expected_payload_safe_hash) is not str or not _is_sha256(expected_payload_safe_hash):
        count += 1
    return count


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(character in "0123456789abcdef" for character in value)


def _count_remediation_context_mismatches(
    receipt: dict[str, Any],
    *,
    expected_milestone_id: str,
) -> int:
    count = 0
    exact_values = (
        ("receipt_schema", RECEIPT_SCHEMA),
        ("receipt_version", RECEIPT_VERSION),
        ("milestone_id", expected_milestone_id),
    )
    for field, expected in exact_values:
        if field in receipt and _has_expected_type(field, receipt[field]):
            if receipt[field] != expected:
                count += 1
    if type(expected_milestone_id) is not str:
        count += 1

    extension_values = (
        ("receipt_classification", RECEIPT_CLASSIFICATION),
        ("remediation_context", REMEDIATION_CONTEXT),
        ("new_remediation_source_session_authorized", True),
        ("remediation_capture_execution_limit", 1),
        ("remediation_capture_execution_count", 1),
        ("remediation_source_session_consumed", True),
        ("physical_JSONL_record_selected", 1),
        ("candidate_chain_stage_count", 7),
        ("payload_top_level_field_count", 10),
        ("payload_field_paths_contract_count", 71),
    )
    for field, expected in extension_values:
        if field in receipt and _contracted_extension_type_valid(field, receipt[field]):
            if receipt[field] != expected:
                count += 1
    return count


def _contracted_extension_type_valid(field: str, value: Any) -> bool:
    if field in _CONTRACTED_STRING_EXTENSIONS:
        return type(value) is str
    if field in _CONTRACTED_INTEGER_EXTENSIONS:
        return type(value) is int
    if field in _CONTRACTED_TRUE_EXTENSIONS | _CONTRACTED_FALSE_EXTENSIONS:
        return type(value) is bool
    return True


def _count_scanner_contract_mismatches(
    receipt: dict[str, Any],
    scanner_result: dict[str, Any],
) -> int:
    count = 0
    scanner_clean = (
        scanner_result.get("profile") == _scanner.SAFE_CAPTURE_RECEIPT_PROFILE
        and scanner_result.get("passed") is True
        and scanner_result.get("finding_count") == 0
        and scanner_result.get("protected_value_exposed") is False
        and scanner_result.get("raw_key_echoed") is False
        and scanner_result.get("raw_value_echoed") is False
    )
    if not scanner_clean:
        count += 1
    for field in ("forbidden_field_scan_passed", "protected_value_scan_passed"):
        if field in receipt and type(receipt[field]) is bool and receipt[field] is not True:
            count += 1
    for field in ("protected_value_exposed", "raw_key_echoed", "raw_value_echoed"):
        if field in receipt and type(receipt[field]) is bool and receipt[field] is not False:
            count += 1
    return count


def _build_result(
    *,
    missing_required_field_count: int = 0,
    disallowed_extension_field_count: int = 0,
    invalid_field_type_count: int = 0,
    floating_value_count: int = 0,
    arithmetic_mismatch_count: int = 0,
    negative_proof_violation_count: int = 0,
    scanner_contract_mismatch_count: int = 0,
    payload_cross_binding_mismatch_count: int = 0,
    remediation_context_mismatch_count: int = 0,
) -> dict[str, Any]:
    counts = (
        missing_required_field_count,
        disallowed_extension_field_count,
        invalid_field_type_count,
        floating_value_count,
        arithmetic_mismatch_count,
        negative_proof_violation_count,
        scanner_contract_mismatch_count,
        payload_cross_binding_mismatch_count,
        remediation_context_mismatch_count,
    )
    categories = [
        category
        for category, count in zip(FINDING_CATEGORIES, counts)
        if count > 0
    ]
    return {
        "audit_schema": AUDIT_SCHEMA,
        "audit_version": AUDIT_VERSION,
        "passed": not categories,
        "finding_count": sum(counts),
        "finding_categories": categories,
        "first_finding_code": categories[0] if categories else None,
        "missing_required_field_count": missing_required_field_count,
        "disallowed_extension_field_count": disallowed_extension_field_count,
        "invalid_field_type_count": invalid_field_type_count,
        "floating_value_count": floating_value_count,
        "arithmetic_mismatch_count": arithmetic_mismatch_count,
        "negative_proof_violation_count": negative_proof_violation_count,
        "scanner_contract_mismatch_count": scanner_contract_mismatch_count,
        "payload_cross_binding_mismatch_count": payload_cross_binding_mismatch_count,
        "remediation_context_mismatch_count": remediation_context_mismatch_count,
        "protected_value_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
        "input_mutated": False,
    }
