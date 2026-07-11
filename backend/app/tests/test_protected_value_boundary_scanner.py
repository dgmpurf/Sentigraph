from __future__ import annotations

import ast
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

import app.services.protected_value_boundary_scanner as scanner_module
from app.services.protected_value_boundary_scanner import (
    SAFE_CAPTURE_RECEIPT_PROFILE,
    SAFE_PAYLOAD_PROFILE,
    SCAN_SCHEMA,
    SCAN_VERSION,
    scan_protected_value_boundary,
)


NEGATIVE_PROOF_FIELDS = (
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
)


def _safe_receipt() -> dict[str, Any]:
    return {
        "receipt_schema": "sentigraph_mvp_f03_real_safe_payload_capture_receipt_v1_0",
        "receipt_version": "1.0",
        "milestone_id": "MVP-F03",
        "capture_session_id": "synthetic-capture-session-001",
        "forbidden_field_scan_passed": True,
        "protected_value_scan_passed": True,
        **{field: False for field in NEGATIVE_PROOF_FIELDS},
    }


def _safe_payload() -> dict[str, Any]:
    return {
        "payload_schema": "sentigraph_exact_locked_candidate_safe_write_payload_v0_1",
        "payload_version": "0.1",
        "input_safe_hash": "a" * 64,
        "candidate_projection": {
            "candidate_id": "synthetic-candidate-001",
            "text_snippet_redacted": "[redacted selected source content]",
            "source_url_present": False,
            "warning_labels": ["manual_review_required"],
        },
        "boundary_projection": {
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
        },
    }


def _assert_failed(result: dict[str, Any], category: str) -> None:
    assert result["passed"] is False
    assert category in result["finding_categories"]
    assert result["finding_count"] >= 1
    assert result["protected_value_exposed"] is False
    assert result["raw_key_echoed"] is False
    assert result["raw_value_echoed"] is False


def _synthetic_broad_key_substring_detector(value: dict[str, Any]) -> bool:
    fragments = ("raw_", "author", "path", "database", "network", "gate", "persistence")
    return any(fragment in key.casefold() for key in value for fragment in fragments)


def test_output_contract_and_safe_negative_proof_receipt_pass() -> None:
    result = scan_protected_value_boundary(
        _safe_receipt(),
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )

    assert result == {
        "scan_schema": SCAN_SCHEMA,
        "scan_version": SCAN_VERSION,
        "profile": SAFE_CAPTURE_RECEIPT_PROFILE,
        "passed": True,
        "finding_count": 0,
        "finding_categories": [],
        "first_finding_code": None,
        "finding_location_class": "receipt",
        "protected_value_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
    }


@pytest.mark.parametrize("field", NEGATIVE_PROOF_FIELDS)
def test_each_negative_proof_field_set_true_fails_closed(field: str) -> None:
    receipt = _safe_receipt()
    receipt[field] = True

    result = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )

    _assert_failed(result, "negative_proof_state_violation")


@pytest.mark.parametrize("unsafe_false", [0, 1, "false", None, {}, []])
def test_non_boolean_negative_proof_values_fail_closed(unsafe_false: Any) -> None:
    receipt = _safe_receipt()
    receipt["raw_row_retained"] = unsafe_false

    result = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )

    _assert_failed(result, "negative_proof_state_violation")


def test_receipt_negative_proof_exemption_is_root_only() -> None:
    receipt = _safe_receipt()
    receipt["nested"] = {"raw_row_retained": False}

    result = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )

    _assert_failed(result, "negative_proof_state_violation")


def test_receipt_negative_proof_exemption_never_applies_to_payload() -> None:
    payload = _safe_payload()
    payload["raw_row_retained"] = False

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    _assert_failed(result, "forbidden_key_present")


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("raw_comment", False),
        ("private_message", ""),
        ("profile_url", None),
        ("api_key", []),
    ],
)
def test_active_forbidden_fields_fail_regardless_of_value(key: str, value: Any) -> None:
    payload = _safe_payload()
    payload[key] = value

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    _assert_failed(result, "forbidden_key_present")


@pytest.mark.parametrize(
    ("unsafe_value", "category"),
    [
        ("https://synthetic.invalid/item", "unsafe_URL_pattern"),
        ("www.synthetic.invalid/item", "unsafe_URL_pattern"),
        (r"C:\synthetic\protected\fixture.txt", "unsafe_absolute_path_pattern"),
        (r"path=C:\synthetic\protected\fixture.txt", "unsafe_absolute_path_pattern"),
        (r"\\synthetic-host\fixture\item.json", "unsafe_absolute_path_pattern"),
        ("/tmp/synthetic/fixture.json", "unsafe_absolute_path_pattern"),
        ("path=/tmp/synthetic/fixture.json", "unsafe_absolute_path_pattern"),
        ("../synthetic/fixture.json", "unsafe_absolute_path_pattern"),
        ("synthetic.person@example.test", "unsafe_email_pattern"),
        ("13912345678", "unsafe_phone_pattern"),
        ("Bearer syntheticcredential123", "unsafe_secret_pattern"),
        ("api_key=syntheticcredential", "unsafe_secret_pattern"),
        ("-----BEGIN PRIVATE KEY-----", "unsafe_secret_pattern"),
        ("raw_author_id=synthetic-identity", "unsafe_raw_content_pattern"),
        ("private_message: synthetic-content", "unsafe_raw_content_pattern"),
    ],
)
def test_unsafe_string_patterns_fail_without_value_echo(
    unsafe_value: str,
    category: str,
) -> None:
    payload = _safe_payload()
    payload["safe_label"] = unsafe_value

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    _assert_failed(result, category)
    rendered = json.dumps(result, sort_keys=True)
    assert unsafe_value not in rendered


@pytest.mark.parametrize(
    "safe_value",
    [
        "b" * 64,
        "synthetic-candidate-opaque-001",
        "sentigraph_exact_locked_candidate_safe_write_payload_v0_1",
        "0.1",
        "[redacted selected source content]",
        "manual_review_required",
    ],
)
def test_safe_hashes_ids_schema_versions_and_redaction_marker_pass(safe_value: str) -> None:
    payload = _safe_payload()
    payload["safe_label"] = safe_value

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    assert result["passed"] is True


def test_safe_sha256_with_phone_like_digit_run_passes_as_hash() -> None:
    synthetic_hash = "a" * 20 + "13912345678" + "b" * 33
    assert len(synthetic_hash) == 64
    payload = _safe_payload()
    payload["synthetic_safe_hash"] = synthetic_hash

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    assert result["passed"] is True


def test_nested_lists_and_objects_are_scanned_recursively() -> None:
    payload = _safe_payload()
    payload["nested"] = [{"safe_label": ["https://synthetic.invalid/nested"]}]

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    _assert_failed(result, "unsafe_URL_pattern")


def test_finding_output_and_controlled_failure_never_echo_raw_key_or_value() -> None:
    raw_key = "private_message"
    raw_value = "Bearer syntheticcredential123"
    payload = _safe_payload()
    payload[raw_key] = raw_value

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)
    rendered = json.dumps(result, sort_keys=True)

    assert raw_key not in rendered
    assert raw_value not in rendered
    assert set(result) == {
        "scan_schema",
        "scan_version",
        "profile",
        "passed",
        "finding_count",
        "finding_categories",
        "first_finding_code",
        "finding_location_class",
        "protected_value_exposed",
        "raw_key_echoed",
        "raw_value_echoed",
    }


def test_repeated_scans_are_deterministic_and_do_not_mutate_input() -> None:
    payload = _safe_payload()
    payload["nested"] = {"labels": ["synthetic-safe-label"]}
    before = deepcopy(payload)

    first = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)
    second = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    assert first == second
    assert payload == before


def test_invalid_profile_fails_closed_without_echoing_profile() -> None:
    invalid_profile = "synthetic-private-profile-value"

    result = scan_protected_value_boundary(_safe_payload(), profile=invalid_profile)

    _assert_failed(result, "invalid_scan_profile")
    assert result["profile"] == "invalid"
    assert invalid_profile not in json.dumps(result, sort_keys=True)


@pytest.mark.parametrize(
    "invalid_value",
    [object(), {1: "synthetic"}, {"safe": object()}, {"safe": math.nan}],
)
def test_invalid_non_json_like_input_fails_closed_without_exception(invalid_value: Any) -> None:
    result = scan_protected_value_boundary(invalid_value, profile=SAFE_PAYLOAD_PROFILE)

    _assert_failed(result, "invalid_scan_input")


def test_synthetic_broad_key_substring_false_positive_class_is_closed() -> None:
    receipt = _safe_receipt()

    assert _synthetic_broad_key_substring_detector(receipt) is True
    repaired = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )
    assert repaired["passed"] is True


def test_false_positive_repair_does_not_weaken_genuine_protection() -> None:
    receipt = _safe_receipt()
    receipt["raw_comment"] = False

    result = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )

    _assert_failed(result, "forbidden_key_present")


def test_finding_categories_are_bounded_enums() -> None:
    allowed = {
        "forbidden_key_present",
        "negative_proof_state_violation",
        "unsafe_URL_pattern",
        "unsafe_absolute_path_pattern",
        "unsafe_email_pattern",
        "unsafe_phone_pattern",
        "unsafe_secret_pattern",
        "unsafe_raw_content_pattern",
        "invalid_scan_profile",
        "invalid_scan_input",
    }
    payload = _safe_payload()
    payload["raw_comment"] = "https://synthetic.invalid/item"

    result = scan_protected_value_boundary(payload, profile=SAFE_PAYLOAD_PROFILE)

    assert set(result["finding_categories"]) <= allowed
    assert result["first_finding_code"] in allowed


def test_scanner_module_is_pure_and_has_no_io_or_integration_imports() -> None:
    source_path = Path(scanner_module.__file__)
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    forbidden_modules = {
        "io",
        "os",
        "pathlib",
        "sqlite3",
        "subprocess",
        "logging",
        "socket",
        "requests",
        "httpx",
        "urllib",
        "urllib.request",
        "dotenv",
    }
    forbidden_calls = {
        "open",
        "read_text",
        "read_bytes",
        "write_text",
        "write_bytes",
        "getenv",
        "system",
        "popen",
    }
    call_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    attribute_calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }

    assert not ((imported | imported_from) & forbidden_modules)
    assert not ((call_names | attribute_calls) & forbidden_calls)
    assert "print(" not in source
    assert "logger" not in source.casefold()
    assert "callback" not in source.casefold()
