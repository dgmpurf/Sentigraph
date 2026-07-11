from __future__ import annotations

import ast
import inspect
import json
from copy import deepcopy
from typing import Any

import pytest

import app.services.safe_payload_receipt_acceptance_auditor as auditor_module
from app.services.safe_payload_receipt_acceptance_auditor import (
    AUDIT_SCHEMA,
    AUDIT_VERSION,
    CORE_REQUIRED_FIELDS,
    FINDING_CATEGORIES,
    NEGATIVE_PROOF_FIELDS,
    audit_safe_capture_receipt,
)


EXPECTED_HASH = "a" * 64
EXPECTED_MILESTONE = "MVP-C02-P2"
EXPECTED_BYTES_READ = 3313
EXPECTED_OUTCOME = "captured_one_safe_payload_for_independent_audit"
PAYLOAD_SCHEMA = "sentigraph_exact_locked_candidate_safe_write_payload_v0_1"
PAYLOAD_VERSION = "0.1"


def _receipt(*, payload_hash: str = EXPECTED_HASH) -> dict[str, Any]:
    return {
        "receipt_schema": "sentigraph_mvp_f03_real_safe_payload_capture_receipt_v1_0",
        "receipt_version": "1.0",
        "milestone_id": EXPECTED_MILESTONE,
        "capture_session_id": "synthetic-capture-session-001",
        "capture_started_at": "2026-07-11T00:00:00Z",
        "capture_completed_at": "2026-07-11T00:00:01Z",
        "source_access_session_consumed": True,
        "source_file_open_count": 1,
        "source_file_reopen_count": 0,
        "source_file_open_mode": "binary_read_only",
        "source_line_utf8_byte_limit": 1048576,
        "source_line_probe_read_size": 1048577,
        "source_read_call_count": 1,
        "source_line_bytes_read": EXPECTED_BYTES_READ,
        "source_line_terminator_counted_in_limit": True,
        "oversized_source_line_detected": False,
        "UTF8_decode_attempted": True,
        "UTF8_decode_passed": True,
        "JSON_parse_attempted": True,
        "duplicate_JSON_key_detected": False,
        "nonstandard_numeric_constant_detected": False,
        "strict_JSON_parse_passed": True,
        "top_level_JSON_object_verified": True,
        "directory_enumeration_performed": False,
        "alternate_source_used": False,
        "approved_package_binding_verified": True,
        "approved_row_source_verified": True,
        "row_selector_verified": True,
        "row_hash_verified": True,
        "candidate_binding_verified": True,
        "rows_examined_or_parsed": 1,
        "rows_selected": 1,
        "payload_artifact_count": 1,
        "receipt_artifact_count": 1,
        "payload_schema": PAYLOAD_SCHEMA,
        "payload_version": PAYLOAD_VERSION,
        "payload_safe_hash": payload_hash,
        "forbidden_field_scan_passed": True,
        "protected_value_scan_passed": True,
        "raw_row_retained": False,
        "raw_author_identity_retained": False,
        "absolute_path_recorded": False,
        "production_object_created": False,
        "database_accessed": False,
        "network_called": False,
        "gate_activated": False,
        "persistence_mutation_performed": False,
        "final_outcome": EXPECTED_OUTCOME,
        "pause_reason": None,
        "receipt_classification": "safe_local_nonproduction_metadata_only",
        "remediation_context": "MVP_C02_P2_separately_governed_remediation_capture",
        "new_remediation_source_session_authorized": True,
        "remediation_capture_execution_limit": 1,
        "remediation_capture_execution_count": 1,
        "remediation_source_session_consumed": True,
        "source_second_read_performed": False,
        "source_seek_performed": False,
        "fallback_used": False,
        "automatic_retry_performed": False,
        "historical_F03_retry": False,
        "historical_F03_reclassified": False,
        "physical_JSONL_record_selected": 1,
        "protected_value_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
        "production_evidenceitem_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "production_analysis_result_created": False,
        "source11_runtime_called": False,
        "public_or_delivery_runtime_called": False,
        "provider_or_collector_called": False,
    }


def _audit(
    receipt: Any,
    *,
    payload_hash: str = EXPECTED_HASH,
    milestone: str = EXPECTED_MILESTONE,
    bytes_read: int = EXPECTED_BYTES_READ,
    outcome: str = EXPECTED_OUTCOME,
) -> dict[str, Any]:
    return audit_safe_capture_receipt(
        receipt,
        expected_payload_safe_hash=payload_hash,
        expected_milestone_id=milestone,
        expected_source_line_bytes_read=bytes_read,
        expected_final_outcome=outcome,
    )


def _categories(result: dict[str, Any]) -> set[str]:
    return set(result["finding_categories"])


def test_complete_synthetic_c02_p2_receipt_passes_with_exact_result_contract() -> None:
    result = _audit(_receipt())

    assert result == {
        "audit_schema": AUDIT_SCHEMA,
        "audit_version": AUDIT_VERSION,
        "passed": True,
        "finding_count": 0,
        "finding_categories": [],
        "first_finding_code": None,
        "missing_required_field_count": 0,
        "disallowed_extension_field_count": 0,
        "invalid_field_type_count": 0,
        "floating_value_count": 0,
        "arithmetic_mismatch_count": 0,
        "negative_proof_violation_count": 0,
        "scanner_contract_mismatch_count": 0,
        "payload_cross_binding_mismatch_count": 0,
        "remediation_context_mismatch_count": 0,
        "protected_value_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
        "input_mutated": False,
    }


@pytest.mark.parametrize("field", sorted(CORE_REQUIRED_FIELDS))
def test_each_required_core_field_missing_is_reported_without_name_echo(field: str) -> None:
    receipt = _receipt()
    receipt.pop(field)

    result = _audit(receipt)

    assert "missing_required_field" in _categories(result)
    assert result["missing_required_field_count"] == 1
    assert field not in json.dumps(result, sort_keys=True)


def test_missing_field_and_float_are_separate_findings_from_one_object() -> None:
    receipt = _receipt()
    receipt.pop("capture_session_id")
    receipt["diagnostic_metric"] = 1.25

    result = _audit(receipt)

    assert {"missing_required_field", "floating_value_present"} <= _categories(result)
    assert result["missing_required_field_count"] == 1
    assert result["floating_value_count"] == 1


def test_multiple_missing_fields_have_complete_safe_count() -> None:
    receipt = _receipt()
    for field in ("capture_session_id", "capture_started_at", "capture_completed_at"):
        receipt.pop(field)

    result = _audit(receipt)

    assert result["missing_required_field_count"] == 3


def test_safe_extension_cannot_satisfy_missing_core_field() -> None:
    receipt = _receipt()
    receipt.pop("milestone_id")
    receipt["diagnostic_note"] = "synthetic-milestone-present-elsewhere"

    result = _audit(receipt)

    assert "missing_required_field" in _categories(result)


def test_bounded_nonauthoritative_safe_extension_passes() -> None:
    receipt = _receipt()
    receipt["diagnostic_note"] = {"label": "synthetic_metadata_only", "items": [1, True, None]}

    assert _audit(receipt)["passed"] is True


def test_disallowed_authority_bearing_extension_fails_closed() -> None:
    receipt = _receipt()
    receipt["write_authorization_granted"] = False

    result = _audit(receipt)

    assert "disallowed_extension_field" in _categories(result)
    assert result["disallowed_extension_field_count"] == 1


def test_forbidden_field_fails_even_when_value_is_false() -> None:
    receipt = _receipt()
    receipt["raw_row"] = False

    result = _audit(receipt)

    assert result["passed"] is False
    assert "disallowed_extension_field" in _categories(result)


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_integer_fields_reject_booleans(field: str) -> None:
    receipt = _receipt()
    receipt[field] = True

    assert "invalid_field_type" in _categories(_audit(receipt))


@pytest.mark.parametrize(
    "field",
    [
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
        "approved_package_binding_verified",
        "candidate_binding_verified",
    ],
)
@pytest.mark.parametrize("value", [0, 1])
def test_boolean_fields_reject_integer_values(field: str, value: int) -> None:
    receipt = _receipt()
    receipt[field] = value

    assert "invalid_field_type" in _categories(_audit(receipt))


@pytest.mark.parametrize(
    "field",
    [
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
    ],
)
def test_string_fields_reject_other_json_types(field: str) -> None:
    receipt = _receipt()
    receipt[field] = ["synthetic"]

    assert "invalid_field_type" in _categories(_audit(receipt))


@pytest.mark.parametrize("value", [None, "synthetic_pause_reason"])
def test_nullable_pause_reason_accepts_only_null_or_string(value: Any) -> None:
    receipt = _receipt()
    receipt["pause_reason"] = value
    result = _audit(receipt)
    if value is None:
        assert result["passed"] is True
    else:
        assert "receipt_arithmetic_mismatch" in _categories(result)
        assert "invalid_field_type" not in _categories(result)


@pytest.mark.parametrize("value", [1.25, float("nan"), float("inf"), float("-inf")])
def test_each_float_class_is_reported_separately(value: float) -> None:
    receipt = _receipt()
    receipt["diagnostic_metric"] = value

    result = _audit(receipt)

    assert "floating_value_present" in _categories(result)
    assert result["floating_value_count"] == 1


def test_nested_floats_are_counted_completely() -> None:
    receipt = _receipt()
    receipt["diagnostic_metrics"] = {"values": [1.0, {"deeper": 2.0}]}

    result = _audit(receipt)

    assert result["floating_value_count"] == 2


@pytest.mark.parametrize("field", NEGATIVE_PROOF_FIELDS)
def test_each_negative_proof_true_fails(field: str) -> None:
    receipt = _receipt()
    receipt[field] = True

    result = _audit(receipt)

    assert "negative_proof_state_violation" in _categories(result)


@pytest.mark.parametrize("value", ["false", 0, 1, None, [], {}])
def test_negative_proofs_reject_false_like_values(value: Any) -> None:
    receipt = _receipt()
    receipt["raw_row_retained"] = value

    result = _audit(receipt)

    assert "negative_proof_state_violation" in _categories(result)


def test_nested_only_negative_proof_does_not_satisfy_root_contract() -> None:
    receipt = _receipt()
    receipt.pop("raw_row_retained")
    receipt["diagnostic_container"] = {"raw_row_retained": False}

    result = _audit(receipt)

    assert "missing_required_field" in _categories(result)
    assert "negative_proof_state_violation" in _categories(result)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_file_open_count", 0),
        ("source_read_call_count", 0),
        ("source_file_reopen_count", 1),
        ("source_line_utf8_byte_limit", 1),
        ("source_line_probe_read_size", 2),
        ("source_line_bytes_read", 3),
        ("UTF8_decode_passed", False),
        ("strict_JSON_parse_passed", False),
        ("rows_selected", 0),
        ("payload_artifact_count", 0),
        ("candidate_binding_verified", False),
        ("final_outcome", "synthetic_other_outcome"),
    ],
)
def test_arithmetic_and_state_mismatches_are_bounded(field: str, value: Any) -> None:
    receipt = _receipt()
    receipt[field] = value

    assert "receipt_arithmetic_mismatch" in _categories(_audit(receipt))


def test_milestone_context_mismatch_is_separate() -> None:
    receipt = _receipt()
    receipt["milestone_id"] = "MVP-SYNTHETIC"

    assert "remediation_context_mismatch" in _categories(_audit(receipt))


def test_payload_safe_hash_mismatch_is_separate() -> None:
    receipt = _receipt()
    receipt["payload_safe_hash"] = "b" * 64

    assert "payload_cross_binding_mismatch" in _categories(_audit(receipt))


@pytest.mark.parametrize(("field", "value"), [("payload_schema", "synthetic_schema"), ("payload_version", "9.9")])
def test_payload_schema_and_version_mismatch_are_separate(field: str, value: str) -> None:
    receipt = _receipt()
    receipt[field] = value

    assert "payload_cross_binding_mismatch" in _categories(_audit(receipt))


def test_scanner_claim_mismatch_is_separate() -> None:
    receipt = _receipt()
    receipt["protected_value_scan_passed"] = False

    assert "scanner_contract_mismatch" in _categories(_audit(receipt))


def test_findings_never_echo_raw_field_name_or_value() -> None:
    receipt = _receipt()
    forbidden_name = "raw_row"
    forbidden_value = "synthetic-sensitive-marker"
    receipt[forbidden_name] = forbidden_value

    rendered = json.dumps(_audit(receipt), sort_keys=True)

    assert forbidden_name not in rendered
    assert forbidden_value not in rendered


def test_invalid_values_return_bounded_result_without_unsafe_exception() -> None:
    receipt = _receipt()
    receipt["diagnostic_note"] = object()

    result = _audit(receipt)

    assert result["passed"] is False
    assert set(result["finding_categories"]) <= set(FINDING_CATEGORIES)


def test_results_are_deterministic_and_input_is_not_mutated() -> None:
    receipt = _receipt()
    original = deepcopy(receipt)

    first = _audit(receipt)
    second = _audit(receipt)

    assert first == second
    assert receipt == original
    assert first["input_mutated"] is False


def test_cyclic_input_fails_closed() -> None:
    receipt = _receipt()
    cycle: dict[str, Any] = {}
    cycle["self"] = cycle
    receipt["diagnostic_container"] = cycle

    result = _audit(receipt)

    assert result["passed"] is False
    assert "invalid_field_type" in _categories(result)


def test_excessive_depth_fails_closed() -> None:
    receipt = _receipt()
    nested: dict[str, Any] = {}
    cursor = nested
    for _ in range(80):
        child: dict[str, Any] = {}
        cursor["child"] = child
        cursor = child
    receipt["diagnostic_container"] = nested

    assert _audit(receipt)["passed"] is False


@pytest.mark.parametrize("value", [None, [], "synthetic"])
def test_invalid_top_level_input_fails_closed(value: Any) -> None:
    result = _audit(value)

    assert result["passed"] is False
    assert "invalid_field_type" in _categories(result)


def test_finding_categories_are_bounded_enums() -> None:
    receipt = _receipt()
    receipt.pop("capture_session_id")
    receipt["write_authorization_granted"] = True
    receipt["diagnostic_metric"] = 1.0

    result = _audit(receipt)

    assert set(result["finding_categories"]) <= set(FINDING_CATEGORIES)
    assert result["first_finding_code"] in FINDING_CATEGORIES


def test_complete_diagnostics_continue_after_unrelated_missing_field() -> None:
    receipt = _receipt()
    receipt.pop("capture_session_id")
    receipt["source_file_open_count"] = 0
    receipt["raw_row_retained"] = True
    receipt["diagnostic_metric"] = 1.0

    result = _audit(receipt)

    assert {
        "missing_required_field",
        "floating_value_present",
        "receipt_arithmetic_mismatch",
        "negative_proof_state_violation",
    } <= _categories(result)


def test_safe_sha256_with_phone_like_digits_passes_scanner_integration() -> None:
    safe_hash = "13800138000" + "a" * 53
    receipt = _receipt(payload_hash=safe_hash)

    assert _audit(receipt, payload_hash=safe_hash)["passed"] is True


def test_genuine_phone_like_extension_value_fails_scanner_integration() -> None:
    receipt = _receipt()
    receipt["diagnostic_note"] = "synthetic contact 13800138000"

    result = _audit(receipt)

    assert "scanner_contract_mismatch" in _categories(result)
    assert result["protected_value_exposed"] is False
    assert result["raw_key_echoed"] is False
    assert result["raw_value_echoed"] is False


def test_module_is_pure_and_has_no_io_or_side_effect_imports() -> None:
    source = inspect.getsource(auditor_module)
    tree = ast.parse(source)
    banned_imports = {
        "asyncio",
        "http",
        "logging",
        "os",
        "pathlib",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
    }
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert imported.isdisjoint(banned_imports)
    assert called_names.isdisjoint({"open", "print", "input", "exec", "eval", "compile"})
    assert "getenv" not in source
    assert "environ" not in source
    assert "callback" not in source.casefold()
