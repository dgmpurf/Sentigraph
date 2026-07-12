from __future__ import annotations

import hashlib
import os
import sqlite3
import stat
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from app.services.governed_nonproduction_evidence_persistence import (
    ATTEMPT_RESERVATION_ID_NAMESPACE,
    ATTEMPT_RESERVATION_SCHEMA,
    ATTEMPT_RESERVATION_TABLE,
    ATTEMPT_RESERVATION_VERSION,
    ATTEMPT_SCOPE_NAMESPACE,
    COMMAND_SCHEMA,
    COMMAND_VERSION,
    LOGICAL_RUNTIME_TARGET_LABEL,
    MAXIMUM_MUTATING_ATTEMPTS,
    MUTATION_MODE,
    PERSISTED_RECORD_SCHEMA,
    TABLE_NAME,
    _ATTEMPT_RESERVATION_COLUMN_ORDER,
    _COLUMN_ORDER,
    _JSON_RECORD_FIELDS,
    _is_hash,
    _is_opaque_token,
    _record_canonical_hash,
    _reservation_canonical_hash,
    _row_to_record,
    _sha256,
    _validate_activation_binding,
    _validate_gate_binding,
    _validate_identity,
    _validate_logical_target_label,
    _validate_timestamp,
    build_governed_nonproduction_evidence_persistence_command,
    validate_exact_locked_candidate_safe_write_payload,
)


RESULT_SCHEMA = (
    "sentigraph_governed_nonproduction_exact_target_read_only_audit_result_v0_1"
)
RESULT_VERSION = "0.1"

RESULT_FIELDS = (
    "result_schema",
    "result_version",
    "audit_task_completed",
    "target_state_outcome",
    "safe_error_code",
    "completed_stage",
    "target_identity_verified",
    "target_metadata_verified",
    "sidecar_preflight_passed",
    "sidecar_postflight_passed",
    "sqlite_opened",
    "sqlite_uri_mode_ro_verified",
    "sqlite_query_only_verified",
    "sqlite_authorizer_verified",
    "schema_contract_verified",
    "record_count_class",
    "reservation_count_class",
    "record_snapshot_digest",
    "reservation_snapshot_digest",
    "expected_record_present",
    "expected_reservation_present",
    "unexpected_record_present",
    "unexpected_reservation_present",
    "record_actual_columns_verified",
    "reservation_actual_columns_verified",
    "record_canonical_hash_verified",
    "reservation_canonical_hash_verified",
    "record_exact_binding_verified",
    "reservation_exact_binding_verified",
    "record_reservation_cross_binding_verified",
    "implementation_mutating_attempt_consumed_actual",
    "governed_nonproduction_record_exists",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "writer_invoked",
    "mutation_attempted",
    "runtime_target_classification_performed",
    "physical_path_disclosed",
    "raw_row_disclosed",
    "SQL_text_disclosed",
    "exception_text_disclosed",
    "stack_trace_disclosed",
)

TARGET_STATE_OUTCOMES = {
    "exact_empty",
    "exact_expected_reservation_only",
    "exact_expected_reservation_and_record",
    "inconsistent_or_not_safely_classifiable",
    "sidecar_present_read_prohibited",
    "target_identity_or_metadata_blocked",
    "bounded_read_only_failure",
}

SAFE_STAGES = {
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

_COUNT_CLASSES = {"exact_0", "exact_1", "at_least_2", "not_obtained"}
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_RECORD_COLUMNS = tuple(_COLUMN_ORDER)
_RESERVATION_COLUMNS = tuple(_ATTEMPT_RESERVATION_COLUMN_ORDER)
_ALLOWED_COLUMNS = {
    TABLE_NAME: frozenset(_RECORD_COLUMNS),
    ATTEMPT_RESERVATION_TABLE: frozenset(_RESERVATION_COLUMNS),
}


@dataclass(frozen=True)
class _PathMetadata:
    exists: bool
    regular: bool
    directory: bool
    symlink: bool
    reparse: bool


def _base_result(
    *,
    outcome: str,
    safe_error_code: str,
    completed_stage: str,
) -> dict[str, Any]:
    if outcome not in TARGET_STATE_OUTCOMES or completed_stage not in SAFE_STAGES:
        raise ValueError("bounded_result_token_invalid")
    result = {
        "result_schema": RESULT_SCHEMA,
        "result_version": RESULT_VERSION,
        "audit_task_completed": True,
        "target_state_outcome": outcome,
        "safe_error_code": safe_error_code,
        "completed_stage": completed_stage,
        "target_identity_verified": False,
        "target_metadata_verified": False,
        "sidecar_preflight_passed": False,
        "sidecar_postflight_passed": False,
        "sqlite_opened": False,
        "sqlite_uri_mode_ro_verified": False,
        "sqlite_query_only_verified": False,
        "sqlite_authorizer_verified": False,
        "schema_contract_verified": False,
        "record_count_class": "not_obtained",
        "reservation_count_class": "not_obtained",
        "record_snapshot_digest": None,
        "reservation_snapshot_digest": None,
        "expected_record_present": False,
        "expected_reservation_present": False,
        "unexpected_record_present": False,
        "unexpected_reservation_present": False,
        "record_actual_columns_verified": False,
        "reservation_actual_columns_verified": False,
        "record_canonical_hash_verified": False,
        "reservation_canonical_hash_verified": False,
        "record_exact_binding_verified": False,
        "reservation_exact_binding_verified": False,
        "record_reservation_cross_binding_verified": False,
        "implementation_mutating_attempt_consumed_actual": (
            "unknown_not_safely_classified"
        ),
        "governed_nonproduction_record_exists": "unknown_not_safely_classified",
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "writer_invoked": False,
        "mutation_attempted": False,
        "runtime_target_classification_performed": False,
        "physical_path_disclosed": False,
        "raw_row_disclosed": False,
        "SQL_text_disclosed": False,
        "exception_text_disclosed": False,
        "stack_trace_disclosed": False,
    }
    if tuple(result) != RESULT_FIELDS:
        raise ValueError("bounded_result_fields_invalid")
    return result


def _bounded_result(
    result: dict[str, Any],
    *,
    outcome: str,
    safe_error_code: str,
    completed_stage: str,
) -> dict[str, Any]:
    result["target_state_outcome"] = outcome
    result["safe_error_code"] = safe_error_code
    result["completed_stage"] = completed_stage
    if set(result) != set(RESULT_FIELDS):
        return _base_result(
            outcome="bounded_read_only_failure",
            safe_error_code="bounded_result_contract_failed",
            completed_stage="classification",
        )
    if outcome not in TARGET_STATE_OUTCOMES or completed_stage not in SAFE_STAGES:
        return _base_result(
            outcome="bounded_read_only_failure",
            safe_error_code="bounded_result_contract_failed",
            completed_stage="classification",
        )
    if result["record_count_class"] not in _COUNT_CLASSES:
        return _base_result(
            outcome="bounded_read_only_failure",
            safe_error_code="bounded_result_contract_failed",
            completed_stage="classification",
        )
    if result["reservation_count_class"] not in _COUNT_CLASSES:
        return _base_result(
            outcome="bounded_read_only_failure",
            safe_error_code="bounded_result_contract_failed",
            completed_stage="classification",
        )
    return result


def _derive_expected_bindings(
    *,
    expected_identity: Mapping[str, Any],
    expected_gate_contract_binding: Mapping[str, Any],
    expected_activation_decision_binding: Mapping[str, Any],
    expected_input_safe_hash: str,
    target_logical_label: str,
) -> dict[str, Any]:
    if not isinstance(expected_identity, Mapping):
        raise ValueError("expected_identity_invalid")
    if not isinstance(expected_gate_contract_binding, Mapping):
        raise ValueError("expected_gate_invalid")
    if not isinstance(expected_activation_decision_binding, Mapping):
        raise ValueError("expected_activation_invalid")
    identity = _validate_identity(dict(expected_identity))
    candidate_identity_digest = _sha256(identity)
    gate = _validate_gate_binding(dict(expected_gate_contract_binding))
    activation = _validate_activation_binding(
        dict(expected_activation_decision_binding),
        candidate_identity_digest=candidate_identity_digest,
        gate_contract_safe_hash=gate["gate_contract_safe_hash"],
    )
    if target_logical_label != LOGICAL_RUNTIME_TARGET_LABEL:
        raise ValueError("target_logical_label_invalid")
    if not _is_hash(expected_input_safe_hash):
        raise ValueError("expected_input_safe_hash_invalid")

    idempotency_key = _sha256(
        {
            "namespace": "sentigraph_governed_nonproduction_idempotency_v0_2",
            "candidate_identity_digest": candidate_identity_digest,
            "input_safe_hash": expected_input_safe_hash,
            "persisted_record_schema": PERSISTED_RECORD_SCHEMA,
            "persisted_record_schema_version": "0.1",
            "gate_contract_schema": gate["gate_contract_schema"],
            "gate_contract_version": gate["gate_contract_version"],
            "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
            "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
            "mutation_mode": MUTATION_MODE,
            "target_logical_label": target_logical_label,
            "command_schema": COMMAND_SCHEMA,
            "command_version": COMMAND_VERSION,
        }
    )
    persisted_record_id = f"gnpepr-{idempotency_key[:32]}"
    audit_receipt_reference = f"gnpepr-receipt-{idempotency_key[:32]}"
    attempt_scope_key = _sha256(
        {
            "namespace": ATTEMPT_SCOPE_NAMESPACE,
            "candidate_identity_digest": candidate_identity_digest,
            "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
            "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
            "target_logical_label": target_logical_label,
            "mutation_mode": MUTATION_MODE,
            "command_schema": COMMAND_SCHEMA,
            "command_version": COMMAND_VERSION,
        }
    )
    attempt_reservation_id = "gnpepr-attempt-" + _sha256(
        {
            "namespace": ATTEMPT_RESERVATION_ID_NAMESPACE,
            "attempt_scope_key": attempt_scope_key,
        }
    )[:32]
    return {
        "identity": identity,
        "gate": gate,
        "activation": activation,
        "candidate_identity_digest": candidate_identity_digest,
        "input_safe_hash": expected_input_safe_hash,
        "idempotency_key": idempotency_key,
        "persisted_record_id": persisted_record_id,
        "audit_receipt_reference": audit_receipt_reference,
        "attempt_scope_key": attempt_scope_key,
        "attempt_reservation_id": attempt_reservation_id,
    }


def _validate_caller_derived_values(
    derived: dict[str, Any],
    *,
    expected_idempotency_key: str,
    expected_persisted_record_id: str,
    expected_audit_receipt_reference: str,
    expected_attempt_scope_key: str,
    expected_attempt_reservation_id: str,
) -> None:
    hash_values = {
        "idempotency_key": expected_idempotency_key,
        "attempt_scope_key": expected_attempt_scope_key,
    }
    token_values = {
        "persisted_record_id": expected_persisted_record_id,
        "audit_receipt_reference": expected_audit_receipt_reference,
        "attempt_reservation_id": expected_attempt_reservation_id,
    }
    if any(not _is_hash(value) for value in hash_values.values()):
        raise ValueError("expected_derived_hash_invalid")
    if any(not _is_opaque_token(value) for value in token_values.values()):
        raise ValueError("expected_derived_token_invalid")
    supplied = {**hash_values, **token_values}
    if any(derived[key] != value for key, value in supplied.items()):
        raise ValueError("expected_derived_binding_mismatch")


def _lexical_absolute(path: str | Path) -> Path:
    if not isinstance(path, (str, Path)):
        raise ValueError("path_type_invalid")
    candidate = Path(path)
    if not candidate.is_absolute():
        raise ValueError("absolute_path_required")
    return Path(os.path.abspath(os.path.normpath(os.fspath(candidate))))


def _is_reparse_stat(value: Any) -> bool:
    return bool(
        getattr(value, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT
    )


def _path_metadata(path: Path) -> _PathMetadata:
    if not os.path.lexists(path):
        return _PathMetadata(False, False, False, False, False)
    value = os.lstat(path)
    return _PathMetadata(
        exists=True,
        regular=stat.S_ISREG(value.st_mode),
        directory=stat.S_ISDIR(value.st_mode),
        symlink=stat.S_ISLNK(value.st_mode),
        reparse=_is_reparse_stat(value),
    )


def _probe_sidecars(database_path: Path) -> dict[str, bool]:
    return {
        "journal": os.path.lexists(Path(str(database_path) + "-journal")),
        "wal": os.path.lexists(Path(str(database_path) + "-wal")),
        "shm": os.path.lexists(Path(str(database_path) + "-shm")),
    }


def _authorizer_decision(
    action: int,
    arg1: str | None,
    arg2: str | None,
    database_name: str | None,
) -> int:
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_PRAGMA:
        if str(arg1 or "").lower() == "query_only" and arg2 in {None, ""}:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_READ:
        columns = _ALLOWED_COLUMNS.get(str(arg1 or ""))
        if columns is not None and arg2 in columns and database_name == "main":
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    return sqlite3.SQLITE_DENY


def _authorizer_callback(
    action: int,
    arg1: str | None,
    arg2: str | None,
    database_name: str | None,
    _trigger_name: str | None,
) -> int:
    return _authorizer_decision(action, arg1, arg2, database_name)


def _count_class(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "exact_0"
    if len(rows) == 1:
        return "exact_1"
    return "at_least_2"


def _safe_cell_digest(value: Any) -> list[str]:
    if value is None:
        return ["null"]
    if isinstance(value, bytes):
        return ["bytes", hashlib.sha256(value).hexdigest()]
    if isinstance(value, str):
        return ["text", hashlib.sha256(value.encode("utf-8")).hexdigest()]
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return ["number", hashlib.sha256(repr(value).encode("ascii")).hexdigest()]
    return ["unsupported"]


def _snapshot_digest(rows: list[sqlite3.Row], count_class: str) -> str:
    projection = [
        [_safe_cell_digest(value) for value in tuple(row)]
        for row in rows
    ]
    return _sha256({"count_class": count_class, "rows": projection})


def _schema_and_rows(
    connection: sqlite3.Connection,
    *,
    table: str,
    columns: tuple[str, ...],
    primary_id: str,
) -> list[sqlite3.Row]:
    schema_cursor = connection.execute(f"SELECT * FROM {table} LIMIT 0")
    description = tuple(item[0] for item in schema_cursor.description or ())
    if description != columns:
        raise ValueError("schema_contract_mismatch")
    selected_columns = ", ".join(columns)
    return connection.execute(
        f"SELECT {selected_columns} FROM {table} ORDER BY {primary_id} LIMIT 2"
    ).fetchall()


def _restore_payload_projection(record: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(record["safe_payload_projection"])
    candidate = payload.get("candidate_projection")
    if not isinstance(candidate, dict):
        raise ValueError("stored_payload_projection_invalid")
    if "coarse_created_at" in candidate:
        if "created_at_date" in candidate:
            raise ValueError("stored_payload_projection_invalid")
        candidate["created_at_date"] = candidate.pop("coarse_created_at")
    return payload


def _reconstruct_reservation(row: sqlite3.Row) -> dict[str, Any]:
    reservation = dict(row)
    if set(reservation) != set(_RESERVATION_COLUMNS):
        raise ValueError("reservation_columns_invalid")
    required_values = {
        "attempt_reservation_schema": ATTEMPT_RESERVATION_SCHEMA,
        "attempt_reservation_version": ATTEMPT_RESERVATION_VERSION,
        "mutation_mode": MUTATION_MODE,
        "maximum_mutating_attempts": MAXIMUM_MUTATING_ATTEMPTS,
        "reserved_attempt_number": MAXIMUM_MUTATING_ATTEMPTS,
    }
    if any(reservation.get(key) != value for key, value in required_values.items()):
        raise ValueError("reservation_contract_invalid")
    for field in {
        "attempt_scope_key",
        "candidate_identity_digest",
        "input_safe_hash",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
        "idempotency_key",
        "reservation_canonical_hash",
    }:
        if not _is_hash(reservation.get(field)):
            raise ValueError("reservation_hash_invalid")
    for field in {
        "attempt_reservation_id",
        "gate_contract_schema",
        "gate_contract_version",
        "activation_decision_id",
        "expected_persisted_record_id",
    }:
        if not _is_opaque_token(reservation.get(field)):
            raise ValueError("reservation_value_invalid")
    _validate_logical_target_label(reservation.get("target_logical_label"))
    _validate_timestamp(reservation.get("reserved_at"))
    if (
        _reservation_canonical_hash(reservation)
        != reservation.get("reservation_canonical_hash")
    ):
        raise ValueError("reservation_canonical_hash_invalid")
    return reservation


def _record_binding_matches(
    record: dict[str, Any],
    derived: dict[str, Any],
    target_logical_label: str,
) -> bool:
    try:
        payload = _restore_payload_projection(record)
        validated_payload = validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=derived["identity"],
        )
        if validated_payload["input_safe_hash"] != derived["input_safe_hash"]:
            return False
        if record["source_schema_versions"] != validated_payload["source_schema_versions"]:
            return False
        if record["lineage_projection"] != validated_payload["lineage_projection"]:
            return False
        command = build_governed_nonproduction_evidence_persistence_command(
            validated_payload,
            expected_identity=derived["identity"],
            gate_contract_binding=derived["gate"],
            activation_decision_binding=derived["activation"],
            target_logical_label=target_logical_label,
            mutation_attempt_number=MAXIMUM_MUTATING_ATTEMPTS,
            created_at=record["created_at"],
        )
        return record == command["record"]
    except Exception:
        return False


def _reservation_binding_matches(
    reservation: dict[str, Any],
    derived: dict[str, Any],
    target_logical_label: str,
) -> bool:
    expected = {
        "attempt_reservation_id": derived["attempt_reservation_id"],
        "attempt_reservation_schema": ATTEMPT_RESERVATION_SCHEMA,
        "attempt_reservation_version": "0.1",
        "attempt_scope_key": derived["attempt_scope_key"],
        "candidate_identity_digest": derived["candidate_identity_digest"],
        "input_safe_hash": derived["input_safe_hash"],
        "gate_contract_schema": derived["gate"]["gate_contract_schema"],
        "gate_contract_version": derived["gate"]["gate_contract_version"],
        "gate_contract_safe_hash": derived["gate"]["gate_contract_safe_hash"],
        "activation_decision_id": derived["activation"]["activation_decision_id"],
        "activation_decision_safe_hash": derived["activation"][
            "activation_decision_safe_hash"
        ],
        "target_logical_label": target_logical_label,
        "mutation_mode": MUTATION_MODE,
        "idempotency_key": derived["idempotency_key"],
        "expected_persisted_record_id": derived["persisted_record_id"],
        "maximum_mutating_attempts": MAXIMUM_MUTATING_ATTEMPTS,
        "reserved_attempt_number": MAXIMUM_MUTATING_ATTEMPTS,
    }
    return all(reservation.get(key) == value for key, value in expected.items())


def _cross_binding_matches(
    record: dict[str, Any],
    reservation: dict[str, Any],
) -> bool:
    fields = {
        "candidate_identity_digest",
        "input_safe_hash",
        "gate_contract_schema",
        "gate_contract_version",
        "gate_contract_safe_hash",
        "activation_decision_id",
        "activation_decision_safe_hash",
        "idempotency_key",
    }
    return all(record.get(field) == reservation.get(field) for field in fields) and (
        record.get("created_at") == reservation.get("reserved_at")
    )


def _postflight(
    result: dict[str, Any],
    database_path: Path,
) -> dict[str, Any]:
    try:
        sidecars = _probe_sidecars(database_path)
    except Exception:
        return _bounded_result(
            result,
            outcome="bounded_read_only_failure",
            safe_error_code="sidecar_postflight_failed",
            completed_stage="sidecar_postflight",
        )
    if any(sidecars.values()):
        result["sidecar_postflight_passed"] = False
        result["runtime_target_classification_performed"] = True
        return _bounded_result(
            result,
            outcome="inconsistent_or_not_safely_classifiable",
            safe_error_code="sidecar_state_changed",
            completed_stage="sidecar_postflight",
        )
    result["sidecar_postflight_passed"] = True
    result["completed_stage"] = "completed"
    return result


def audit_governed_nonproduction_exact_target_read_only(
    *,
    authorized_root_path: str | Path,
    database_path: str | Path,
    target_logical_label: str,
    expected_identity: Mapping[str, Any],
    expected_gate_contract_binding: Mapping[str, Any],
    expected_activation_decision_binding: Mapping[str, Any],
    expected_input_safe_hash: str,
    expected_idempotency_key: str,
    expected_persisted_record_id: str,
    expected_audit_receipt_reference: str,
    expected_attempt_scope_key: str,
    expected_attempt_reservation_id: str,
) -> dict[str, Any]:
    """Return one bounded read-only classification for one explicit target."""

    result = _base_result(
        outcome="target_identity_or_metadata_blocked",
        safe_error_code="input_validation_failed",
        completed_stage="input_validation",
    )
    try:
        derived = _derive_expected_bindings(
            expected_identity=expected_identity,
            expected_gate_contract_binding=expected_gate_contract_binding,
            expected_activation_decision_binding=expected_activation_decision_binding,
            expected_input_safe_hash=expected_input_safe_hash,
            target_logical_label=target_logical_label,
        )
        _validate_caller_derived_values(
            derived,
            expected_idempotency_key=expected_idempotency_key,
            expected_persisted_record_id=expected_persisted_record_id,
            expected_audit_receipt_reference=expected_audit_receipt_reference,
            expected_attempt_scope_key=expected_attempt_scope_key,
            expected_attempt_reservation_id=expected_attempt_reservation_id,
        )
    except Exception:
        return result

    try:
        root = _lexical_absolute(authorized_root_path)
        database = _lexical_absolute(database_path)
        expected_database = root.joinpath(*target_logical_label.split("/"))
        exact_match = os.path.normcase(os.fspath(database)) == os.path.normcase(
            os.fspath(expected_database)
        )
        inside_root = os.path.commonpath([root, database]) == os.fspath(root)
    except Exception:
        return _bounded_result(
            result,
            outcome="target_identity_or_metadata_blocked",
            safe_error_code="target_identity_failed",
            completed_stage="target_identity",
        )
    if not exact_match or not inside_root:
        return _bounded_result(
            result,
            outcome="target_identity_or_metadata_blocked",
            safe_error_code="target_identity_failed",
            completed_stage="target_identity",
        )
    result["target_identity_verified"] = True

    try:
        root_metadata = _path_metadata(root)
        if not (
            root_metadata.exists
            and root_metadata.directory
            and not root_metadata.symlink
            and not root_metadata.reparse
        ):
            raise ValueError("root_metadata_invalid")
        current = root
        for component in target_logical_label.split("/")[:-1]:
            current = current / component
            metadata = _path_metadata(current)
            if not (
                metadata.exists
                and metadata.directory
                and not metadata.symlink
                and not metadata.reparse
            ):
                raise ValueError("parent_metadata_invalid")
        target_metadata = _path_metadata(database)
        if not (
            target_metadata.exists
            and target_metadata.regular
            and not target_metadata.directory
            and not target_metadata.symlink
            and not target_metadata.reparse
        ):
            raise ValueError("target_metadata_invalid")
    except Exception:
        return _bounded_result(
            result,
            outcome="target_identity_or_metadata_blocked",
            safe_error_code="target_metadata_failed",
            completed_stage="target_metadata",
        )
    result["target_metadata_verified"] = True

    try:
        sidecars_before = _probe_sidecars(database)
    except Exception:
        return _bounded_result(
            result,
            outcome="target_identity_or_metadata_blocked",
            safe_error_code="sidecar_preflight_failed",
            completed_stage="sidecar_preflight",
        )
    if any(sidecars_before.values()):
        return _bounded_result(
            result,
            outcome="sidecar_present_read_prohibited",
            safe_error_code="sidecar_present",
            completed_stage="sidecar_preflight",
        )
    result["sidecar_preflight_passed"] = True

    connection: sqlite3.Connection | None = None
    try:
        uri = f"{database.as_uri()}?mode=ro"
        connection = sqlite3.connect(uri, uri=True, timeout=5.0)
        connection.row_factory = sqlite3.Row
        result["sqlite_opened"] = True
        result["sqlite_uri_mode_ro_verified"] = True
    except Exception:
        return _postflight(
            _bounded_result(
                result,
                outcome="bounded_read_only_failure",
                safe_error_code="sqlite_open_failed",
                completed_stage="sqlite_open",
            ),
            database,
        )

    try:
        connection.execute("PRAGMA query_only = ON")
        query_only = int(connection.execute("PRAGMA query_only").fetchone()[0])
        if query_only != 1:
            raise ValueError("query_only_not_enabled")
        result["sqlite_query_only_verified"] = True
        connection.set_authorizer(_authorizer_callback)
        result["sqlite_authorizer_verified"] = True
    except Exception:
        try:
            connection.close()
        except Exception:
            pass
        return _postflight(
            _bounded_result(
                result,
                outcome="bounded_read_only_failure",
                safe_error_code="read_only_posture_failed",
                completed_stage="read_only_posture",
            ),
            database,
        )

    try:
        record_rows = _schema_and_rows(
            connection,
            table=TABLE_NAME,
            columns=_RECORD_COLUMNS,
            primary_id="persisted_record_id",
        )
        reservation_rows = _schema_and_rows(
            connection,
            table=ATTEMPT_RESERVATION_TABLE,
            columns=_RESERVATION_COLUMNS,
            primary_id="attempt_reservation_id",
        )
        result["schema_contract_verified"] = True
    except Exception:
        try:
            connection.close()
        except Exception:
            pass
        return _postflight(
            _bounded_result(
                result,
                outcome="bounded_read_only_failure",
                safe_error_code="schema_or_row_read_failed",
                completed_stage="schema_contract",
            ),
            database,
        )
    finally:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass

    result["record_count_class"] = _count_class(record_rows)
    result["reservation_count_class"] = _count_class(reservation_rows)
    result["record_snapshot_digest"] = _snapshot_digest(
        record_rows,
        result["record_count_class"],
    )
    result["reservation_snapshot_digest"] = _snapshot_digest(
        reservation_rows,
        result["reservation_count_class"],
    )
    result["expected_record_present"] = any(
        row["persisted_record_id"] == derived["persisted_record_id"]
        for row in record_rows
    )
    result["expected_reservation_present"] = any(
        row["attempt_reservation_id"] == derived["attempt_reservation_id"]
        for row in reservation_rows
    )
    result["unexpected_record_present"] = any(
        row["persisted_record_id"] != derived["persisted_record_id"]
        for row in record_rows
    )
    result["unexpected_reservation_present"] = any(
        row["attempt_reservation_id"] != derived["attempt_reservation_id"]
        for row in reservation_rows
    )

    record: dict[str, Any] | None = None
    reservation: dict[str, Any] | None = None
    reconstruction_failed = False
    if len(record_rows) == 1 and result["expected_record_present"]:
        try:
            record = _row_to_record(record_rows[0])
            result["record_actual_columns_verified"] = True
            result["record_canonical_hash_verified"] = (
                _record_canonical_hash(record) == record["record_canonical_hash"]
            )
        except Exception:
            reconstruction_failed = True
    if len(reservation_rows) == 1 and result["expected_reservation_present"]:
        try:
            reservation = _reconstruct_reservation(reservation_rows[0])
            result["reservation_actual_columns_verified"] = True
            result["reservation_canonical_hash_verified"] = (
                _reservation_canonical_hash(reservation)
                == reservation["reservation_canonical_hash"]
            )
        except Exception:
            reconstruction_failed = True

    if record is not None:
        result["record_exact_binding_verified"] = _record_binding_matches(
            record,
            derived,
            target_logical_label,
        )
    if reservation is not None:
        result["reservation_exact_binding_verified"] = _reservation_binding_matches(
            reservation,
            derived,
            target_logical_label,
        )
    if record is not None and reservation is not None:
        result["record_reservation_cross_binding_verified"] = _cross_binding_matches(
            record,
            reservation,
        )

    result["runtime_target_classification_performed"] = True
    exact_empty = (
        result["record_count_class"] == "exact_0"
        and result["reservation_count_class"] == "exact_0"
        and not result["expected_record_present"]
        and not result["expected_reservation_present"]
        and not result["unexpected_record_present"]
        and not result["unexpected_reservation_present"]
    )
    exact_reservation_only = (
        result["record_count_class"] == "exact_0"
        and result["reservation_count_class"] == "exact_1"
        and result["expected_reservation_present"]
        and not result["unexpected_record_present"]
        and not result["unexpected_reservation_present"]
        and result["reservation_actual_columns_verified"]
        and result["reservation_canonical_hash_verified"]
        and result["reservation_exact_binding_verified"]
    )
    exact_both = (
        result["record_count_class"] == "exact_1"
        and result["reservation_count_class"] == "exact_1"
        and result["expected_record_present"]
        and result["expected_reservation_present"]
        and not result["unexpected_record_present"]
        and not result["unexpected_reservation_present"]
        and result["record_actual_columns_verified"]
        and result["reservation_actual_columns_verified"]
        and result["record_canonical_hash_verified"]
        and result["reservation_canonical_hash_verified"]
        and result["record_exact_binding_verified"]
        and result["reservation_exact_binding_verified"]
        and result["record_reservation_cross_binding_verified"]
    )

    if exact_empty:
        result["implementation_mutating_attempt_consumed_actual"] = "no"
        result["governed_nonproduction_record_exists"] = "no"
        classified = _bounded_result(
            result,
            outcome="exact_empty",
            safe_error_code="none",
            completed_stage="classification",
        )
    elif exact_reservation_only:
        result["implementation_mutating_attempt_consumed_actual"] = "yes"
        result["governed_nonproduction_record_exists"] = "no"
        classified = _bounded_result(
            result,
            outcome="exact_expected_reservation_only",
            safe_error_code="none",
            completed_stage="classification",
        )
    elif exact_both:
        result["implementation_mutating_attempt_consumed_actual"] = "yes"
        result["governed_nonproduction_record_exists"] = "yes"
        classified = _bounded_result(
            result,
            outcome="exact_expected_reservation_and_record",
            safe_error_code="none",
            completed_stage="classification",
        )
    else:
        classified = _bounded_result(
            result,
            outcome="inconsistent_or_not_safely_classifiable",
            safe_error_code=(
                "row_reconstruction_failed"
                if reconstruction_failed
                else "state_or_binding_inconsistent"
            ),
            completed_stage=(
                "row_reconstruction" if reconstruction_failed else "classification"
            ),
        )
    return _postflight(classified, database)
