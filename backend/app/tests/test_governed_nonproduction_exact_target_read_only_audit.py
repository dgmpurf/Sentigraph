from __future__ import annotations

import ast
import hashlib
import importlib
import inspect
import json
import os
import sqlite3
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

import app.services.governed_nonproduction_evidence_persistence as persistence


CREATED_AT = "2026-07-13T00:00:00Z"
LOGICAL_LABEL = persistence.LOGICAL_RUNTIME_TARGET_LABEL


def _module():
    return importlib.import_module(
        "app.services.governed_nonproduction_exact_target_read_only_audit"
    )


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _hex(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _identity(seed: str = "001") -> dict[str, Any]:
    return {
        "approved_package_name": f"synthetic-package-{seed}",
        "approved_package_role": "synthetic_governance_sample",
        "approved_case_id_hint": f"synthetic-case-{seed}",
        "approved_row_source": f"synthetic-row-source-{seed}",
        "selected_preview_row_opaque_id": f"synthetic-preview-row-{seed}",
        "selected_preview_row_safe_hash": _hex(f"synthetic-preview-{seed}"),
        "final_candidate_id": f"synthetic-candidate-{seed}",
        "final_candidate_safe_hash": _hex(f"synthetic-candidate-{seed}"),
        "final_candidate_schema": persistence.SOURCE_CANDIDATE_SET_SCHEMA,
        "identity_schema": persistence.IDENTITY_SCHEMA,
        "identity_version": "0.1",
        "hash_algorithm": "sha256",
        "hash_input_scope": "versioned_safe_canonical_projection_only",
        "candidate_lock_status": "locked_for_single_candidate_governance_review_only",
    }


def _candidate_projection(seed: str = "001") -> dict[str, Any]:
    return {
        "evidence_layer_write_candidate_schema": persistence.SOURCE_CANDIDATE_SCHEMA,
        "evidence_layer_write_candidate_id": f"synthetic-write-candidate-{seed}",
        "source_production_evidence_import_candidate_id": f"synthetic-production-import-{seed}",
        "source_evidence_layer_write_candidate_id": f"synthetic-direct-write-{seed}",
        "source_evidence_layer_import_candidate_id": f"synthetic-import-{seed}",
        "source_review_queue_candidate_id": f"synthetic-review-queue-{seed}",
        "source_evidence_candidate_id": f"synthetic-evidence-{seed}",
        "evidence_id_hash": _hex(f"synthetic-evidence-{seed}"),
        "text_snippet_redacted": "[redacted synthetic sample]",
        "preview_hash": _hex(f"synthetic-preview-content-{seed}"),
        "case_id_hint": f"synthetic-case-{seed}",
        "platform": "synthetic_platform",
        "evidence_type": "synthetic_metadata",
        "created_at_date": "2026-07-13",
        "source_url_present": False,
        "acquisition_mode": "synthetic_fixture",
        "provenance_type": "synthetic_fixture",
        "verification_status": "needs_review",
        "review_status": "review_needed",
        "trust_label": "unverified",
        "redaction_status": "redacted",
        "title_or_label_redacted": "synthetic redacted title",
        "redaction_warnings": ["synthetic_fixture_only"],
        "warning_labels": ["manual_review_required", "synthetic_fixture_only"],
        "blocker_codes": [],
    }


def _payload(identity: dict[str, Any], seed: str = "001") -> dict[str, Any]:
    candidate = _candidate_projection(seed)
    lineage = {
        field: candidate[field]
        for field in {
            "source_production_evidence_import_candidate_id",
            "source_evidence_layer_write_candidate_id",
            "source_evidence_layer_import_candidate_id",
            "source_review_queue_candidate_id",
            "source_evidence_candidate_id",
        }
    }
    lineage.update(
        {
            "source_candidate_set_schema": persistence.SOURCE_CANDIDATE_SET_SCHEMA,
            "source_candidate_schema": persistence.SOURCE_CANDIDATE_SCHEMA,
        }
    )
    value = {
        "payload_schema": persistence.PAYLOAD_SCHEMA,
        "payload_version": persistence.PAYLOAD_VERSION,
        "source_candidate_set_schema": persistence.SOURCE_CANDIDATE_SET_SCHEMA,
        "source_candidate_schema": persistence.SOURCE_CANDIDATE_SCHEMA,
        "source_schema_versions": {
            "candidate_set_schema": persistence.SOURCE_CANDIDATE_SET_SCHEMA,
            "candidate_schema": persistence.SOURCE_CANDIDATE_SCHEMA,
            "identity_schema": persistence.IDENTITY_SCHEMA,
            "payload_schema": persistence.PAYLOAD_SCHEMA,
        },
        "immutable_candidate_identity": deepcopy(identity),
        "candidate_projection": candidate,
        "lineage_projection": lineage,
        "boundary_projection": {
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
            "preview_only": True,
            "import_candidate_only": True,
            "production_import_candidate_only": True,
            "write_candidate_only": True,
            "evidence_layer_write_candidate_only": True,
            "not_production_evidence_item": True,
            "no_evidence_layer_write": True,
            "warning_count": 1,
            "warning_labels": ["manual_review_required"],
        },
    }
    value["input_safe_hash"] = _digest(value)
    return value


def _gate() -> dict[str, Any]:
    return {
        "gate_contract_schema": "sentigraph_synthetic_gate_contract_v0_1",
        "gate_contract_version": "0.1",
        "gate_contract_safe_hash": _hex("synthetic-gate-contract"),
    }


def _activation(identity: dict[str, Any], gate: dict[str, Any], seed: str = "001") -> dict[str, Any]:
    return {
        "activation_decision_id": f"synthetic-activation-decision-{seed}",
        "activation_decision_schema": "sentigraph_synthetic_activation_decision_v0_1",
        "activation_decision_version": "0.1",
        "activation_decision_safe_hash": _hex(f"synthetic-activation-{seed}"),
        "candidate_identity_digest": _digest(identity),
        "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
        "decision_scope": persistence.ACTIVATION_DECISION_SCOPE,
    }


def _command(seed: str = "001") -> dict[str, Any]:
    identity = _identity(seed)
    gate = _gate()
    activation = _activation(identity, gate, seed)
    return persistence.build_governed_nonproduction_evidence_persistence_command(
        _payload(identity, seed),
        expected_identity=identity,
        gate_contract_binding=gate,
        activation_decision_binding=activation,
        target_logical_label=LOGICAL_LABEL,
        mutation_attempt_number=1,
        created_at=CREATED_AT,
    )


def _context(tmp_path: Path, seed: str = "001") -> dict[str, Any]:
    root = tmp_path / "synthetic-authorized-root"
    database = root.joinpath(*LOGICAL_LABEL.split("/"))
    command = _command(seed)
    return {
        "root": root,
        "database": database,
        "command": command,
        "kwargs": {
            "authorized_root_path": root,
            "database_path": database,
            "target_logical_label": LOGICAL_LABEL,
            "expected_identity": deepcopy(command["immutable_candidate_identity"]),
            "expected_gate_contract_binding": deepcopy(command["gate_contract_binding"]),
            "expected_activation_decision_binding": deepcopy(
                command["activation_decision_binding"]
            ),
            "expected_input_safe_hash": command["input_safe_hash"],
            "expected_idempotency_key": command["idempotency_key"],
            "expected_persisted_record_id": command["persisted_record_id"],
            "expected_audit_receipt_reference": command["audit_receipt_reference"],
            "expected_attempt_scope_key": command["attempt_scope_key"],
            "expected_attempt_reservation_id": command["attempt_reservation_id"],
        },
    }


def _database(context: dict[str, Any]) -> None:
    database = context["database"]
    database.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.execute(persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL)
        connection.execute(persistence._CREATE_TABLE_SQL)


def _database_value(field: str, value: Any) -> Any:
    if field in persistence._JSON_RECORD_FIELDS:
        return persistence._canonical_json(value)
    if field in persistence._BOOLEAN_RECORD_FIELDS:
        return 1 if value else 0
    return value


def _seed_record_row_directly(
    connection: sqlite3.Connection,
    record: dict[str, Any],
) -> None:
    columns = ", ".join(persistence._COLUMN_ORDER)
    markers = ", ".join("?" for _ in persistence._COLUMN_ORDER)
    values = [_database_value(field, record[field]) for field in persistence._COLUMN_ORDER]
    connection.execute(
        f"INSERT INTO {persistence.TABLE_NAME} ({columns}) VALUES ({markers})",
        values,
    )


def _seed_reservation_row_directly(
    connection: sqlite3.Connection,
    reservation: dict[str, Any],
) -> None:
    columns = ", ".join(persistence._ATTEMPT_RESERVATION_COLUMN_ORDER)
    markers = ", ".join("?" for _ in persistence._ATTEMPT_RESERVATION_COLUMN_ORDER)
    values = [reservation[field] for field in persistence._ATTEMPT_RESERVATION_COLUMN_ORDER]
    connection.execute(
        f"INSERT INTO {persistence.ATTEMPT_RESERVATION_TABLE} ({columns}) VALUES ({markers})",
        values,
    )


def _seed(
    context: dict[str, Any],
    *,
    records: list[dict[str, Any]] | None = None,
    reservations: list[dict[str, Any]] | None = None,
) -> None:
    _database(context)
    with sqlite3.connect(context["database"]) as connection:
        for reservation in reservations or []:
            _seed_reservation_row_directly(connection, reservation)
        for record in records or []:
            _seed_record_row_directly(connection, record)


def _seed_classifiable_state(context: dict[str, Any], state: str) -> None:
    records = (
        [context["command"]["record"]]
        if state == "reservation_and_record"
        else []
    )
    reservations = (
        [context["command"]["reservation"]]
        if state in {"reservation_only", "reservation_and_record"}
        else []
    )
    _seed(context, records=records, reservations=reservations)


def _audit(context: dict[str, Any]) -> dict[str, Any]:
    return _module().audit_governed_nonproduction_exact_target_read_only(
        **context["kwargs"]
    )


def _assert_safe_result(result: dict[str, Any], module: Any) -> None:
    assert set(result) == set(module.RESULT_FIELDS)
    assert result["result_schema"] == module.RESULT_SCHEMA
    assert result["result_version"] == module.RESULT_VERSION
    assert result["audit_task_completed"] is True
    assert result["production_evidenceitem_created"] is False
    assert result["production_case_changed"] is False
    assert result["downstream_runtime_called"] is False
    assert result["writer_invoked"] is False
    assert result["mutation_attempted"] is False
    assert result["physical_path_disclosed"] is False
    assert result["raw_row_disclosed"] is False
    assert result["SQL_text_disclosed"] is False
    assert result["exception_text_disclosed"] is False
    assert result["stack_trace_disclosed"] is False
    json.dumps(result, ensure_ascii=True, sort_keys=True)


def _assert_classifiable_evidence_retained(
    result: dict[str, Any],
    state: str,
) -> None:
    assert result["record_snapshot_digest"] is not None
    assert result["reservation_snapshot_digest"] is not None
    if state == "empty":
        assert result["record_count_class"] == "exact_0"
        assert result["reservation_count_class"] == "exact_0"
        assert result["expected_record_present"] is False
        assert result["expected_reservation_present"] is False
    elif state == "reservation_only":
        assert result["record_count_class"] == "exact_0"
        assert result["reservation_count_class"] == "exact_1"
        assert result["expected_record_present"] is False
        assert result["expected_reservation_present"] is True
        assert result["reservation_actual_columns_verified"] is True
        assert result["reservation_canonical_hash_verified"] is True
        assert result["reservation_exact_binding_verified"] is True
    else:
        assert result["record_count_class"] == "exact_1"
        assert result["reservation_count_class"] == "exact_1"
        assert result["expected_record_present"] is True
        assert result["expected_reservation_present"] is True
        assert result["record_actual_columns_verified"] is True
        assert result["reservation_actual_columns_verified"] is True
        assert result["record_canonical_hash_verified"] is True
        assert result["reservation_canonical_hash_verified"] is True
        assert result["record_exact_binding_verified"] is True
        assert result["reservation_exact_binding_verified"] is True
        assert result["record_reservation_cross_binding_verified"] is True


def test_public_module_symbol_and_schema_exist() -> None:
    module = _module()
    assert callable(module.audit_governed_nonproduction_exact_target_read_only)
    assert module.RESULT_SCHEMA == (
        "sentigraph_governed_nonproduction_exact_target_read_only_audit_result_v0_1"
    )
    assert module.RESULT_VERSION == "0.1"


def test_derived_state_invalidation_is_pure_and_preserves_other_evidence() -> None:
    module = _module()
    result = module._base_result(
        outcome="exact_expected_reservation_and_record",
        safe_error_code="none",
        completed_stage="classification",
    )
    result["implementation_mutating_attempt_consumed_actual"] = "yes"
    result["governed_nonproduction_record_exists"] = "yes"
    result["record_count_class"] = "exact_1"
    result["reservation_count_class"] = "exact_1"
    result["record_snapshot_digest"] = _hex("retained-record-snapshot")
    result["reservation_snapshot_digest"] = _hex("retained-reservation-snapshot")
    before = deepcopy(result)

    invalidated = module._invalidate_derived_state_conclusions(result)

    assert invalidated is not result
    assert result == before
    assert invalidated["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert invalidated["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )
    for field in set(module.RESULT_FIELDS) - {
        "implementation_mutating_attempt_consumed_actual",
        "governed_nonproduction_record_exists",
    }:
        assert invalidated[field] == before[field]


def test_exact_empty_synthetic_database(tmp_path: Path) -> None:
    context = _context(tmp_path)
    _seed(context)
    result = _audit(context)
    assert result["target_state_outcome"] == "exact_empty"
    assert result["record_count_class"] == "exact_0"
    assert result["reservation_count_class"] == "exact_0"
    assert result["implementation_mutating_attempt_consumed_actual"] == "no"
    assert result["governed_nonproduction_record_exists"] == "no"
    _assert_safe_result(result, _module())


def test_exact_reservation_only_synthetic_database(tmp_path: Path) -> None:
    context = _context(tmp_path)
    _seed(context, reservations=[context["command"]["reservation"]])
    result = _audit(context)
    assert result["target_state_outcome"] == "exact_expected_reservation_only"
    assert result["record_count_class"] == "exact_0"
    assert result["reservation_count_class"] == "exact_1"
    assert result["reservation_exact_binding_verified"] is True
    assert result["implementation_mutating_attempt_consumed_actual"] == "yes"
    assert result["governed_nonproduction_record_exists"] == "no"


def test_exact_reservation_and_record_synthetic_database(tmp_path: Path) -> None:
    context = _context(tmp_path)
    _seed(
        context,
        records=[context["command"]["record"]],
        reservations=[context["command"]["reservation"]],
    )
    result = _audit(context)
    assert result["target_state_outcome"] == "exact_expected_reservation_and_record"
    assert result["record_count_class"] == "exact_1"
    assert result["reservation_count_class"] == "exact_1"
    assert result["record_exact_binding_verified"] is True
    assert result["reservation_exact_binding_verified"] is True
    assert result["record_reservation_cross_binding_verified"] is True
    assert result["implementation_mutating_attempt_consumed_actual"] == "yes"
    assert result["governed_nonproduction_record_exists"] == "yes"


def test_record_without_reservation_is_inconsistent(tmp_path: Path) -> None:
    context = _context(tmp_path)
    _seed(context, records=[context["command"]["record"]])
    assert _audit(context)["target_state_outcome"] == (
        "inconsistent_or_not_safely_classifiable"
    )


@pytest.mark.parametrize(
    ("records", "reservations"),
    [
        ("two", "exact"),
        ("exact", "two"),
        ("unrelated", "exact"),
        ("exact", "unrelated"),
    ],
)
def test_unexpected_additional_or_unrelated_rows_are_inconsistent(
    tmp_path: Path,
    records: str,
    reservations: str,
) -> None:
    context = _context(tmp_path)
    other = _command("002")
    record_values = {
        "two": [context["command"]["record"], other["record"]],
        "exact": [context["command"]["record"]],
        "unrelated": [other["record"]],
    }[records]
    reservation_values = {
        "two": [context["command"]["reservation"], other["reservation"]],
        "exact": [context["command"]["reservation"]],
        "unrelated": [other["reservation"]],
    }[reservations]
    _seed(context, records=record_values, reservations=reservation_values)
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"
    assert result["unexpected_record_present"] or result["unexpected_reservation_present"]


@pytest.mark.parametrize(
    ("target", "field", "value"),
    [
        ("record", "candidate_identity_digest", _hex("wrong-candidate")),
        ("record", "input_safe_hash", _hex("wrong-input")),
        ("record", "gate_contract_safe_hash", _hex("wrong-gate")),
        ("record", "activation_decision_safe_hash", _hex("wrong-activation")),
        ("record", "idempotency_key", _hex("wrong-idempotency")),
        ("record", "persisted_record_id", "synthetic-wrong-record-id"),
        ("reservation", "candidate_identity_digest", _hex("wrong-reservation-candidate")),
        ("reservation", "input_safe_hash", _hex("wrong-reservation-input")),
        ("reservation", "gate_contract_safe_hash", _hex("wrong-reservation-gate")),
        ("reservation", "activation_decision_safe_hash", _hex("wrong-reservation-activation")),
        ("reservation", "idempotency_key", _hex("wrong-reservation-idempotency")),
        ("reservation", "attempt_scope_key", _hex("wrong-scope")),
        ("reservation", "attempt_reservation_id", "synthetic-wrong-reservation-id"),
    ],
)
def test_stable_binding_mismatches_are_inconsistent(
    tmp_path: Path,
    target: str,
    field: str,
    value: Any,
) -> None:
    context = _context(tmp_path)
    record = deepcopy(context["command"]["record"])
    reservation = deepcopy(context["command"]["reservation"])
    selected = record if target == "record" else reservation
    selected[field] = value
    if target == "record":
        selected["record_canonical_hash"] = persistence._record_canonical_hash(selected)
    else:
        selected["reservation_canonical_hash"] = persistence._reservation_canonical_hash(
            selected
        )
    _seed(context, records=[record], reservations=[reservation])
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"


@pytest.mark.parametrize("target", ["record", "reservation"])
def test_stale_canonical_hash_is_detected(tmp_path: Path, target: str) -> None:
    context = _context(tmp_path)
    record = deepcopy(context["command"]["record"])
    reservation = deepcopy(context["command"]["reservation"])
    if target == "record":
        record["candidate_role"] = "synthetic_changed_role"
    else:
        reservation["activation_decision_id"] = "synthetic-changed-activation"
    _seed(context, records=[record], reservations=[reservation])
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"
    assert result[f"{target}_canonical_hash_verified"] is False


def test_malformed_stored_json_is_detected_without_row_disclosure(tmp_path: Path) -> None:
    context = _context(tmp_path)
    _seed(
        context,
        records=[context["command"]["record"]],
        reservations=[context["command"]["reservation"]],
    )
    with sqlite3.connect(context["database"]) as connection:
        connection.execute(
            f"UPDATE {persistence.TABLE_NAME} SET safe_payload_projection = ?",
            ("{synthetic-malformed",),
        )
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"
    assert result["raw_row_disclosed"] is False


@pytest.mark.parametrize(
    ("table", "column", "value"),
    [
        ("record", "human_review_required", 2),
        ("record", "persisted_record_schema", "synthetic_wrong_schema"),
        ("reservation", "attempt_reservation_schema", "synthetic_wrong_schema"),
        ("reservation", "attempt_reservation_version", "9.9"),
    ],
)
def test_invalid_boolean_or_schema_is_detected(
    tmp_path: Path,
    table: str,
    column: str,
    value: Any,
) -> None:
    context = _context(tmp_path)
    _seed(
        context,
        records=[context["command"]["record"]],
        reservations=[context["command"]["reservation"]],
    )
    table_name = (
        persistence.TABLE_NAME
        if table == "record"
        else persistence.ATTEMPT_RESERVATION_TABLE
    )
    with sqlite3.connect(context["database"]) as connection:
        connection.execute("PRAGMA ignore_check_constraints = ON")
        connection.execute(
            f"UPDATE {table_name} SET {column} = ?",
            (value,),
        )
    assert _audit(context)["target_state_outcome"] == (
        "inconsistent_or_not_safely_classifiable"
    )


def test_record_reservation_timestamp_mismatch_is_detected(tmp_path: Path) -> None:
    context = _context(tmp_path)
    record = deepcopy(context["command"]["record"])
    record["created_at"] = "2026-07-13T00:00:01Z"
    record["record_canonical_hash"] = persistence._record_canonical_hash(record)
    _seed(
        context,
        records=[record],
        reservations=[context["command"]["reservation"]],
    )
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"
    assert result["record_reservation_cross_binding_verified"] is False


@pytest.mark.parametrize("suffix", ["-journal", "-wal", "-shm"])
def test_exact_sidecar_preflight_blocks_sqlite_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    suffix: str,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed(context)
    Path(str(context["database"]) + suffix).write_bytes(b"synthetic-sidecar")

    def fail_connect(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("sqlite must not open")

    monkeypatch.setattr(module.sqlite3, "connect", fail_connect)
    result = _audit(context)
    assert result["target_state_outcome"] == "sidecar_present_read_prohibited"
    assert result["sqlite_opened"] is False
    assert result["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert result["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )


@pytest.mark.parametrize(
    "state",
    ["empty", "reservation_only", "reservation_and_record"],
)
def test_postflight_sidecar_appearance_invalidates_derived_state_conclusions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    state: str,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed_classifiable_state(context, state)
    calls = 0

    def changing_probe(_database: Path) -> dict[str, bool]:
        nonlocal calls
        calls += 1
        return {"journal": False, "wal": calls > 1, "shm": False}

    monkeypatch.setattr(module, "_probe_sidecars", changing_probe)
    result = _audit(context)
    assert result["target_state_outcome"] == "inconsistent_or_not_safely_classifiable"
    assert result["safe_error_code"] == "sidecar_state_changed"
    assert result["completed_stage"] == "sidecar_postflight"
    assert result["sidecar_postflight_passed"] is False
    assert result["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert result["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )
    _assert_classifiable_evidence_retained(result, state)


@pytest.mark.parametrize(
    "state",
    ["empty", "reservation_only", "reservation_and_record"],
)
def test_postflight_probe_failure_invalidates_derived_state_conclusions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    state: str,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed_classifiable_state(context, state)
    calls = 0

    def failing_postflight_probe(_database: Path) -> dict[str, bool]:
        nonlocal calls
        calls += 1
        if calls > 1:
            raise OSError("synthetic-postflight-probe-failure")
        return {"journal": False, "wal": False, "shm": False}

    monkeypatch.setattr(module, "_probe_sidecars", failing_postflight_probe)
    result = _audit(context)
    assert result["target_state_outcome"] == "bounded_read_only_failure"
    assert result["safe_error_code"] == "sidecar_postflight_failed"
    assert result["completed_stage"] == "sidecar_postflight"
    assert result["sidecar_postflight_passed"] is False
    assert result["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert result["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )
    _assert_classifiable_evidence_retained(result, state)
    assert "synthetic-postflight-probe-failure" not in json.dumps(result)


def test_missing_target_is_metadata_blocked(tmp_path: Path) -> None:
    context = _context(tmp_path)
    result = _audit(context)
    assert result["target_state_outcome"] == "target_identity_or_metadata_blocked"
    assert result["sqlite_opened"] is False
    assert result["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert result["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )


def test_directory_target_is_metadata_blocked(tmp_path: Path) -> None:
    context = _context(tmp_path)
    context["database"].mkdir(parents=True)
    result = _audit(context)
    assert result["target_state_outcome"] == "target_identity_or_metadata_blocked"


@pytest.mark.parametrize("mode", ["outside", "lexical_mismatch", "relative_root", "relative_db"])
def test_path_identity_violations_are_blocked(tmp_path: Path, mode: str) -> None:
    context = _context(tmp_path)
    _seed(context)
    kwargs = context["kwargs"]
    if mode == "outside":
        kwargs["database_path"] = tmp_path / "outside.sqlite3"
    elif mode == "lexical_mismatch":
        kwargs["database_path"] = context["database"].with_name("other.sqlite3")
    elif mode == "relative_root":
        kwargs["authorized_root_path"] = Path("relative-root")
    else:
        kwargs["database_path"] = Path("relative.sqlite3")
    result = _module().audit_governed_nonproduction_exact_target_read_only(**kwargs)
    assert result["target_state_outcome"] == "target_identity_or_metadata_blocked"
    assert result["sqlite_opened"] is False


@pytest.mark.parametrize(
    ("target_kind", "attribute"),
    [
        ("target", "symlink"),
        ("parent", "symlink"),
        ("target", "reparse"),
        ("parent", "reparse"),
    ],
)
def test_symlink_and_reparse_metadata_are_blocked(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    target_kind: str,
    attribute: str,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed(context)
    original = module._path_metadata
    selected = context["database"] if target_kind == "target" else context["database"].parent

    def simulated(path: Path):
        value = original(path)
        if path == selected:
            return replace(value, **{attribute: True})
        return value

    monkeypatch.setattr(module, "_path_metadata", simulated)
    result = _audit(context)
    assert result["target_state_outcome"] == "target_identity_or_metadata_blocked"


def test_mode_ro_without_immutable_and_query_only_verified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed(context)
    original = module.sqlite3.connect
    seen: list[str] = []

    def capturing_connect(database: str, *args: Any, **kwargs: Any):
        seen.append(database)
        return original(database, *args, **kwargs)

    monkeypatch.setattr(module.sqlite3, "connect", capturing_connect)
    result = _audit(context)
    assert len(seen) == 1
    assert "mode=ro" in seen[0]
    assert "immutable=1" not in seen[0]
    assert result["sqlite_uri_mode_ro_verified"] is True
    assert result["sqlite_query_only_verified"] is True


def test_authorizer_allows_only_intended_read_posture() -> None:
    module = _module()
    assert module._authorizer_decision(sqlite3.SQLITE_SELECT, None, None, None) == sqlite3.SQLITE_OK
    assert module._authorizer_decision(
        sqlite3.SQLITE_PRAGMA, "query_only", None, None
    ) == sqlite3.SQLITE_OK
    for table, columns in module._ALLOWED_COLUMNS.items():
        for column in columns:
            assert module._authorizer_decision(
                sqlite3.SQLITE_READ, table, column, "main"
            ) == sqlite3.SQLITE_OK
    assert module._authorizer_decision(
        sqlite3.SQLITE_READ, "synthetic_unlisted", "value", "main"
    ) == sqlite3.SQLITE_DENY
    assert module._authorizer_decision(
        sqlite3.SQLITE_READ, persistence.TABLE_NAME, "synthetic_extra", "main"
    ) == sqlite3.SQLITE_DENY


@pytest.mark.parametrize(
    "action",
    [
        sqlite3.SQLITE_INSERT,
        sqlite3.SQLITE_UPDATE,
        sqlite3.SQLITE_DELETE,
        sqlite3.SQLITE_CREATE_TABLE,
        sqlite3.SQLITE_DROP_TABLE,
        sqlite3.SQLITE_ALTER_TABLE,
        sqlite3.SQLITE_TRANSACTION,
        sqlite3.SQLITE_ATTACH,
        sqlite3.SQLITE_DETACH,
        sqlite3.SQLITE_REINDEX,
        sqlite3.SQLITE_ANALYZE,
        sqlite3.SQLITE_CREATE_INDEX,
        sqlite3.SQLITE_DROP_INDEX,
    ],
)
def test_authorizer_denies_mutation_and_schema_actions(action: int) -> None:
    module = _module()
    assert module._authorizer_decision(action, "synthetic", None, "main") == sqlite3.SQLITE_DENY


@pytest.mark.parametrize("pragma", ["writable_schema", "journal_mode", "foreign_keys"])
def test_authorizer_denies_unsafe_pragmas(pragma: str) -> None:
    assert _module()._authorizer_decision(
        sqlite3.SQLITE_PRAGMA, pragma, None, None
    ) == sqlite3.SQLITE_DENY


def test_bounded_sqlite_open_failure_has_no_exception_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed(context)

    def fail_open(*_args: Any, **_kwargs: Any) -> Any:
        raise sqlite3.OperationalError("synthetic-sensitive-open-value")

    monkeypatch.setattr(module.sqlite3, "connect", fail_open)
    result = _audit(context)
    assert result["target_state_outcome"] == "bounded_read_only_failure"
    assert "synthetic-sensitive-open-value" not in json.dumps(result)
    assert result["exception_text_disclosed"] is False


def test_bounded_schema_read_failure_has_no_exception_text(tmp_path: Path) -> None:
    context = _context(tmp_path)
    context["database"].parent.mkdir(parents=True)
    sqlite3.connect(context["database"]).close()
    result = _audit(context)
    assert result["target_state_outcome"] == "bounded_read_only_failure"
    assert result["schema_contract_verified"] is False
    assert result["exception_text_disclosed"] is False
    assert result["implementation_mutating_attempt_consumed_actual"] == (
        "unknown_not_safely_classified"
    )
    assert result["governed_nonproduction_record_exists"] == (
        "unknown_not_safely_classified"
    )


def test_result_exact_fields_json_determinism_and_value_safety(tmp_path: Path) -> None:
    module = _module()
    context = _context(tmp_path)
    _seed(context)
    first = _audit(context)
    second = _audit(context)
    assert first == second
    _assert_safe_result(first, module)
    rendered = json.dumps(first, ensure_ascii=True, sort_keys=True)
    assert str(tmp_path) not in rendered
    assert context["command"]["immutable_candidate_identity"]["final_candidate_id"] not in rendered
    assert "SELECT " not in rendered
    assert "INSERT INTO" not in rendered


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("expected_input_safe_hash", _hex("caller-wrong-input")),
        ("expected_idempotency_key", _hex("caller-wrong-idempotency")),
        ("expected_persisted_record_id", "synthetic-wrong-record"),
        ("expected_audit_receipt_reference", "synthetic-wrong-receipt"),
        ("expected_attempt_scope_key", _hex("caller-wrong-scope")),
        ("expected_attempt_reservation_id", "synthetic-wrong-reservation"),
    ],
)
def test_caller_derived_binding_mismatch_blocks_before_filesystem(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    replacement: Any,
) -> None:
    module = _module()
    context = _context(tmp_path)
    context["kwargs"][field] = replacement

    def fail_metadata(_path: Path):
        raise AssertionError("filesystem must not be touched")

    monkeypatch.setattr(module, "_path_metadata", fail_metadata)
    result = _audit(context)
    assert result["completed_stage"] == "input_validation"
    assert result["target_state_outcome"] == "target_identity_or_metadata_blocked"


def test_parity_derivation_matches_existing_pure_command_builder(tmp_path: Path) -> None:
    module = _module()
    context = _context(tmp_path)
    command = context["command"]
    derived = module._derive_expected_bindings(
        expected_identity=command["immutable_candidate_identity"],
        expected_gate_contract_binding=command["gate_contract_binding"],
        expected_activation_decision_binding=command["activation_decision_binding"],
        expected_input_safe_hash=command["input_safe_hash"],
        target_logical_label=LOGICAL_LABEL,
    )
    for field in {
        "candidate_identity_digest",
        "idempotency_key",
        "persisted_record_id",
        "audit_receipt_reference",
        "attempt_scope_key",
        "attempt_reservation_id",
    }:
        assert derived[field] == command[field]


def test_owner_static_capability_boundary() -> None:
    module = _module()
    source = inspect.getsource(module)
    tree = ast.parse(source)

    public_functions = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not node.name.startswith("_")
    ]
    assert public_functions == ["audit_governed_nonproduction_exact_target_read_only"]

    forbidden_calls = {
        "create_governed_nonproduction_evidence_record",
        "_persist_rederived_governed_nonproduction_command",
        "_reserve_mutating_attempt",
        "_create_base_record_after_reservation",
        "_insert_record",
        "_insert_attempt_reservation",
        "initialize",
        "_open_mutating",
        "glob",
        "rglob",
        "iterdir",
        "listdir",
        "scandir",
        "walk",
        "print",
    }
    called = set()
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
        elif isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
            imported.update(alias.name for alias in node.names)
    assert not called & forbidden_calls
    assert not imported & forbidden_calls
    assert not imported & {"requests", "httpx", "socket", "subprocess"}
    assert "immutable=1" not in source
    assert "os.environ" not in source
    assert "capture_receipt" not in source
    assert "runtime/governed_nonproduction_evidence_persistence" not in source
    mutation_sql = re_compile_mutation_sql()
    assert not mutation_sql.search(source)


def re_compile_mutation_sql():
    import re

    return re.compile(
        r"\b(?:INSERT\s+INTO|UPDATE\s+\S+\s+SET|DELETE\s+FROM|CREATE\s+TABLE|"
        r"DROP\s+TABLE|ALTER\s+TABLE|VACUUM|REINDEX)\b",
        re.IGNORECASE,
    )


def test_result_contract_sets_are_exact() -> None:
    module = _module()
    assert module.TARGET_STATE_OUTCOMES == {
        "exact_empty",
        "exact_expected_reservation_only",
        "exact_expected_reservation_and_record",
        "inconsistent_or_not_safely_classifiable",
        "sidecar_present_read_prohibited",
        "target_identity_or_metadata_blocked",
        "bounded_read_only_failure",
    }
    assert module.SAFE_STAGES == {
        "input_validation",
        "target_identity",
        "target_metadata",
        "sidecar_preflight",
        "sqlite_open",
        "read_only_posture",
        "schema_contract",
        "row_read",
        "row_reconstruction",
        "binding_validation",
        "classification",
        "sidecar_postflight",
        "completed",
    }
    assert len(module.RESULT_FIELDS) == len(set(module.RESULT_FIELDS))


def test_reparse_detector_is_pure_and_monkeypatchable() -> None:
    module = _module()

    class SyntheticStat:
        st_file_attributes = 0x400

    assert module._is_reparse_stat(SyntheticStat()) is True
