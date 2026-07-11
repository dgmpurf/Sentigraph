from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import stat
from pathlib import Path
from typing import Any

from app.services.governed_nonproduction_evidence_persistence import (
    ATTEMPT_RESERVATION_TABLE,
    LOGICAL_RUNTIME_TARGET_LABEL,
    TABLE_NAME,
    _CREATE_ATTEMPT_RESERVATION_TABLE_SQL,
    _CREATE_TABLE_SQL,
)
from app.services.protected_value_boundary_scanner import (
    SAFE_CAPTURE_RECEIPT_PROFILE,
    scan_protected_value_boundary,
)


RESULT_SCHEMA = "sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_1"
RESULT_VERSION = "0.1"
RECEIPT_SCHEMA = "sentigraph_mvp_f06_exact_logical_target_initialization_receipt_v1_0"
RECEIPT_VERSION = "1.0"
TARGET_KIND = "dedicated_local_sqlite_nonproduction_store"

LOCKED_TARGET_LOGICAL_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3"
)
LOCKED_RECEIPT_LOGICAL_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/"
    "target-initialization-receipt-"
    "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b.json"
)
TARGET_IDENTITY_SAFE_HASH = (
    "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b"
)
TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH = (
    "f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2"
)
ATTEMPT_TABLE_DDL_SAFE_HASH = (
    "2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266"
)
PRIMARY_TABLE_DDL_SAFE_HASH = (
    "d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26"
)

_EXPECTED_LOCKED_TARGET_LOGICAL_LABEL = LOCKED_TARGET_LOGICAL_LABEL
_EXPECTED_LOCKED_RECEIPT_LOGICAL_LABEL = LOCKED_RECEIPT_LOGICAL_LABEL
_EXPECTED_TARGET_PRIMARY_TABLE = "governed_nonproduction_evidence_records_v0_1"
_EXPECTED_TARGET_ATTEMPT_TABLE = (
    "governed_nonproduction_evidence_persistence_attempt_reservations_v0_1"
)

EXECUTION_PHASES = (
    "validate_inputs",
    "verify_locked_governance",
    "verify_committed_DDL",
    "derive_exact_paths",
    "verify_path_components",
    "verify_exact_collisions",
    "classify_target_preexistence",
    "create_exact_parents",
    "open_SQLite_session",
    "begin_schema_transaction",
    "initialize_schema",
    "verify_schema",
    "verify_zero_rows",
    "run_integrity_check",
    "commit_initialization",
    "verify_post_commit_same_session",
    "close_SQLite_session",
    "verify_post_connection_state",
    "build_initialization_receipt",
    "scan_initialization_receipt",
    "write_initialization_receipt",
    "readback_initialization_receipt",
    "evaluate_cleanup",
    "perform_cleanup",
    "completed",
    "terminal_failure",
)

SAFE_ERROR_CODES = (
    "none",
    "invalid_input",
    "governance_hash_mismatch",
    "committed_DDL_hash_mismatch",
    "unsafe_repository_root",
    "path_policy_failure",
    "path_escape_detected",
    "symlink_or_reparse_component_detected",
    "mount_boundary_failure",
    "receipt_preexists",
    "unsafe_target_collision",
    "ambiguous_sidecar_state",
    "target_preexistence_ambiguous",
    "parent_creation_failure",
    "SQLite_connect_failure",
    "transaction_begin_failure",
    "schema_initialization_failure",
    "schema_verification_failure",
    "unexpected_schema_object",
    "nonzero_candidate_rows",
    "nonzero_attempt_reservations",
    "integrity_check_failure",
    "commit_failure_known_rollback",
    "commit_outcome_ambiguous",
    "post_commit_verification_failure",
    "connection_close_failure",
    "post_connection_state_ambiguous",
    "receipt_build_failure",
    "receipt_privacy_scan_failure",
    "receipt_write_failure",
    "receipt_readback_failure",
    "receipt_hash_mismatch",
    "cleanup_failure",
    "unexpected_internal_failure",
)

REQUIRED_RESULT_FIELDS = (
    "result_schema",
    "result_version",
    "passed",
    "decision",
    "privacy_issue_stop",
    "execution_phase",
    "terminal_phase",
    "safe_error_code",
    "target_initialization_outcome",
    "target_preexistence_classification",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "committed_DDL_hashes_verified",
    "path_checks_started",
    "path_checks_completed",
    "path_escape_check_passed",
    "symlink_check_passed",
    "junction_check_passed",
    "reparse_point_check_passed",
    "mount_boundary_check_passed",
    "collision_checks_completed",
    "target_exists_before_run",
    "receipt_exists_before_run",
    "sidecar_exists_before_run",
    "target_created_this_run",
    "receipt_created_this_run",
    "parent_directory_created_count",
    "SQLite_connection_session_limit",
    "SQLite_connection_open_count",
    "SQLite_connection_reopen_count",
    "SQLite_create_count",
    "transaction_begin_count",
    "commit_call_count",
    "commit_returned_successfully",
    "commit_outcome_ambiguous",
    "rollback_count",
    "connection_close_count",
    "schema_DDL_statement_count",
    "candidate_table_DML_statement_count",
    "attempt_table_DML_statement_count",
    "other_user_DML_statement_count",
    "target_primary_table_verified",
    "target_attempt_reservation_table_verified",
    "target_indexes_verified",
    "target_constraints_verified",
    "unexpected_user_schema_object_count",
    "target_schema_inventory_safe_hash",
    "schema_verification_completed",
    "base_record_row_count",
    "attempt_reservation_row_count",
    "zero_row_verification_completed",
    "integrity_check",
    "post_connection_exact_state_checked",
    "unexpected_final_sidecar_state",
    "cleanup_eligible",
    "cleanup_attempted",
    "cleanup_performed",
    "cleanup_file_count",
    "cleanup_directory_count",
    "cleanup_incomplete_or_ambiguous",
    "initialization_receipt_built",
    "initialization_receipt_privacy_scan_passed",
    "initialization_receipt_exclusive_write_performed",
    "initialization_receipt_readback_verified",
    "initialization_receipt_safe_hash",
    "initialization_receipt_byte_sha256",
    "final_target_exists",
    "final_receipt_exists",
    "final_journal_exists",
    "final_WAL_exists",
    "final_SHM_exists",
    "protected_payload_read",
    "safe_capture_receipt_read",
    "source_or_package_read",
    "candidate_mutation_performed",
    "attempt_reservation_mutation_performed",
    "gate_activated",
    "persistence_executed",
    "production_object_created",
    "target_substitution_performed",
    "fallback_used",
    "runtime_directory_enumerated",
    "physical_absolute_path_recorded",
    "raw_exception_exposed",
    "raw_SQL_exposed",
    "raw_key_echoed",
    "raw_value_echoed",
)

_PHASE_ERROR_PAIRS = (
    ("validate_inputs", "invalid_input"),
    ("verify_locked_governance", "governance_hash_mismatch"),
    ("verify_committed_DDL", "committed_DDL_hash_mismatch"),
    ("derive_exact_paths", "path_policy_failure"),
    ("verify_path_components", "path_policy_failure"),
    ("verify_exact_collisions", "unsafe_target_collision"),
    ("classify_target_preexistence", "target_preexistence_ambiguous"),
    ("create_exact_parents", "parent_creation_failure"),
    ("open_SQLite_session", "SQLite_connect_failure"),
    ("begin_schema_transaction", "transaction_begin_failure"),
    ("initialize_schema", "schema_initialization_failure"),
    ("verify_schema", "schema_verification_failure"),
    ("verify_zero_rows", "schema_verification_failure"),
    ("run_integrity_check", "integrity_check_failure"),
    ("commit_initialization", "commit_outcome_ambiguous"),
    ("verify_post_commit_same_session", "post_commit_verification_failure"),
    ("close_SQLite_session", "connection_close_failure"),
    ("verify_post_connection_state", "post_connection_state_ambiguous"),
    ("build_initialization_receipt", "receipt_build_failure"),
    ("scan_initialization_receipt", "receipt_privacy_scan_failure"),
    ("write_initialization_receipt", "receipt_write_failure"),
    ("readback_initialization_receipt", "receipt_readback_failure"),
    ("evaluate_cleanup", "cleanup_failure"),
    ("perform_cleanup", "cleanup_failure"),
    ("terminal_failure", "unexpected_internal_failure"),
)


class _ControlledTerminalFailure(Exception):
    def __init__(self, safe_error_code: str) -> None:
        self.safe_error_code = safe_error_code
        super().__init__()


def _failure_injection_hook(_phase: str, _operation: str) -> None:
    return None


def _p1_repository_root_observer(_repository_root: Path) -> None:
    return None


def _committed_ddl_statements() -> tuple[str, str]:
    return _CREATE_ATTEMPT_RESERVATION_TABLE_SQL, _CREATE_TABLE_SQL


def _new_result_state() -> dict[str, Any]:
    unavailable = "not_available"
    pre_access_unknown = "unknown_due_to_pre_access_stop"
    return {
        "result_schema": RESULT_SCHEMA,
        "result_version": RESULT_VERSION,
        "passed": False,
        "decision": "needs_fix",
        "privacy_issue_stop": False,
        "execution_phase": "validate_inputs",
        "terminal_phase": "validate_inputs",
        "safe_error_code": "none",
        "target_initialization_outcome": "not_completed",
        "target_preexistence_classification": unavailable,
        "target_identity_safe_hash": TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "committed_DDL_hashes_verified": False,
        "path_checks_started": False,
        "path_checks_completed": False,
        "path_escape_check_passed": "not_started",
        "symlink_check_passed": "not_started",
        "junction_check_passed": "not_started",
        "reparse_point_check_passed": "not_started",
        "mount_boundary_check_passed": "not_started",
        "collision_checks_completed": False,
        "target_exists_before_run": pre_access_unknown,
        "receipt_exists_before_run": pre_access_unknown,
        "sidecar_exists_before_run": pre_access_unknown,
        "target_created_this_run": False,
        "receipt_created_this_run": False,
        "parent_directory_created_count": 0,
        "SQLite_connection_session_limit": 1,
        "SQLite_connection_open_count": 0,
        "SQLite_connection_reopen_count": 0,
        "SQLite_create_count": 0,
        "transaction_begin_count": 0,
        "commit_call_count": 0,
        "commit_returned_successfully": False,
        "commit_outcome_ambiguous": False,
        "rollback_count": 0,
        "connection_close_count": 0,
        "schema_DDL_statement_count": 0,
        "candidate_table_DML_statement_count": 0,
        "attempt_table_DML_statement_count": 0,
        "other_user_DML_statement_count": 0,
        "target_primary_table_verified": False,
        "target_attempt_reservation_table_verified": False,
        "target_indexes_verified": False,
        "target_constraints_verified": False,
        "unexpected_user_schema_object_count": unavailable,
        "target_schema_inventory_safe_hash": unavailable,
        "schema_verification_completed": False,
        "base_record_row_count": unavailable,
        "attempt_reservation_row_count": unavailable,
        "zero_row_verification_completed": False,
        "integrity_check": unavailable,
        "post_connection_exact_state_checked": False,
        "unexpected_final_sidecar_state": pre_access_unknown,
        "cleanup_eligible": False,
        "cleanup_attempted": False,
        "cleanup_performed": False,
        "cleanup_file_count": 0,
        "cleanup_directory_count": 0,
        "cleanup_incomplete_or_ambiguous": False,
        "initialization_receipt_built": False,
        "initialization_receipt_privacy_scan_passed": False,
        "initialization_receipt_exclusive_write_performed": False,
        "initialization_receipt_readback_verified": False,
        "initialization_receipt_safe_hash": unavailable,
        "initialization_receipt_byte_sha256": unavailable,
        "final_target_exists": pre_access_unknown,
        "final_receipt_exists": pre_access_unknown,
        "final_journal_exists": pre_access_unknown,
        "final_WAL_exists": pre_access_unknown,
        "final_SHM_exists": pre_access_unknown,
        "protected_payload_read": False,
        "safe_capture_receipt_read": False,
        "source_or_package_read": False,
        "candidate_mutation_performed": False,
        "attempt_reservation_mutation_performed": False,
        "gate_activated": False,
        "persistence_executed": False,
        "production_object_created": False,
        "target_substitution_performed": False,
        "fallback_used": False,
        "runtime_directory_enumerated": False,
        "physical_absolute_path_recorded": False,
        "raw_exception_exposed": False,
        "raw_SQL_exposed": False,
        "raw_key_echoed": False,
        "raw_value_echoed": False,
    }


def _enter_phase(state: dict[str, Any], phase: str, operation: str = "before") -> None:
    if phase not in EXECUTION_PHASES:
        raise _ControlledTerminalFailure("unexpected_internal_failure")
    state["execution_phase"] = phase
    _failure_injection_hook(phase, operation)


def _default_error_for_phase(phase: str) -> str:
    return dict(_PHASE_ERROR_PAIRS).get(phase, "unexpected_internal_failure")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_text(value: str) -> str:
    return _sha256_bytes(value.encode("utf-8"))


def _canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _validate_logical_label(label: str) -> tuple[str, ...]:
    if not isinstance(label, str) or not label or "\\" in label or "//" in label:
        raise _ControlledTerminalFailure("path_policy_failure")
    if label.startswith("/") or ":" in label:
        raise _ControlledTerminalFailure("path_policy_failure")
    components = tuple(label.split("/"))
    if not components or any(part in {"", ".", ".."} for part in components):
        raise _ControlledTerminalFailure("path_policy_failure")
    return components


def _lstat_optional(path: Path) -> os.stat_result | None:
    try:
        return os.lstat(path)
    except FileNotFoundError:
        return None


def _is_reparse_or_link(metadata: os.stat_result) -> bool:
    if stat.S_ISLNK(metadata.st_mode):
        return True
    attributes = int(getattr(metadata, "st_file_attributes", 0))
    reparse_flag = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))
    return bool(attributes & reparse_flag)


def _same_device_boundary(root: Path, candidate: Path) -> bool:
    root_metadata = os.lstat(root)
    candidate_metadata = os.lstat(candidate)
    return int(root_metadata.st_dev) == int(candidate_metadata.st_dev)


def _known_path_components(
    repository_root: Path,
    target: Path,
    receipt: Path,
) -> tuple[Path, ...]:
    ordered: list[Path] = [repository_root]
    for leaf in (target, receipt):
        current = repository_root
        for component in leaf.relative_to(repository_root).parts:
            current = current / component
            if current not in ordered:
                ordered.append(current)
    return tuple(ordered)


def _verify_path_components(
    repository_root: Path,
    target: Path,
    receipt: Path,
) -> None:
    root_metadata = _lstat_optional(repository_root)
    if root_metadata is None or not stat.S_ISDIR(root_metadata.st_mode):
        raise _ControlledTerminalFailure("unsafe_repository_root")
    for path in _known_path_components(repository_root, target, receipt):
        metadata = _lstat_optional(path)
        if metadata is None:
            continue
        if _is_reparse_or_link(metadata):
            raise _ControlledTerminalFailure(
                "symlink_or_reparse_component_detected"
            )
        if path not in {target, receipt} and not stat.S_ISDIR(metadata.st_mode):
            raise _ControlledTerminalFailure("path_policy_failure")
        if not _same_device_boundary(repository_root, path):
            raise _ControlledTerminalFailure("mount_boundary_failure")


def _is_regular_file(metadata: os.stat_result) -> bool:
    return stat.S_ISREG(metadata.st_mode)


def _create_exact_parents(
    repository_root: Path,
    target_parent: Path,
    state: dict[str, Any],
    created: list[Path],
) -> list[Path]:
    current = repository_root
    for component in target_parent.relative_to(repository_root).parts:
        current = current / component
        metadata = _lstat_optional(current)
        if metadata is None:
            os.mkdir(current)
            created.append(current)
            state["parent_directory_created_count"] = len(created)
            if len(created) == 1:
                _failure_injection_hook(
                    "create_exact_parents", "after_first_parent"
                )
            metadata = os.lstat(current)
        if _is_reparse_or_link(metadata) or not stat.S_ISDIR(metadata.st_mode):
            raise _ControlledTerminalFailure("path_policy_failure")
        if not _same_device_boundary(repository_root, current):
            raise _ControlledTerminalFailure("mount_boundary_failure")
    return created


def _open_sqlite_connection(target: Path, *, read_only: bool) -> sqlite3.Connection:
    if read_only:
        connection = sqlite3.connect(f"{target.as_uri()}?mode=ro", uri=True)
        connection.execute("PRAGMA query_only = ON")
        return connection
    return sqlite3.connect(target, isolation_level=None)


def _trace_statement(state: dict[str, Any], statement: str) -> None:
    token = statement.lstrip().split(None, 1)[0].upper() if statement.strip() else ""
    if token not in {"INSERT", "UPDATE", "DELETE", "REPLACE", "UPSERT"}:
        return
    normalized = statement.lower()
    if TABLE_NAME.lower() in normalized:
        state["candidate_table_DML_statement_count"] += 1
    elif ATTEMPT_RESERVATION_TABLE.lower() in normalized:
        state["attempt_table_DML_statement_count"] += 1
    else:
        state["other_user_DML_statement_count"] += 1


def _normalize_create_statement(statement: str) -> str:
    normalized = " ".join(statement.strip().rstrip(";").split())
    return normalized.replace("CREATE TABLE IF NOT EXISTS", "CREATE TABLE", 1)


def _schema_inventory_for_table(
    connection: sqlite3.Connection,
    table: str,
    role: str,
) -> tuple[dict[str, Any], int, bool]:
    columns = connection.execute(f"PRAGMA table_info({table})").fetchall()
    indexes = connection.execute(f"PRAGMA index_list({table})").fetchall()
    foreign_keys = connection.execute(f"PRAGMA foreign_key_list({table})").fetchall()

    unique_column_ids: set[int] = set()
    safe_indexes: list[dict[str, Any]] = []
    named_index_count = 0
    for index in indexes:
        index_name = str(index[1])
        index_columns = connection.execute(
            f"PRAGMA index_info({json.dumps(index_name)})"
        ).fetchall()
        column_ids = [int(row[1]) for row in index_columns]
        is_unique = bool(index[2])
        if is_unique and len(column_ids) == 1:
            unique_column_ids.add(column_ids[0])
        if not index_name.startswith("sqlite_autoindex_"):
            named_index_count += 1
        safe_indexes.append(
            {
                "unique": is_unique,
                "origin": str(index[3]),
                "partial": bool(index[4]),
                "column_ordinals": column_ids,
            }
        )

    safe_columns = [
        {
            "ordinal": int(row[0]),
            "declared_type": str(row[2]).upper(),
            "not_null": bool(row[3]),
            "default_present": row[4] is not None,
            "primary_key_ordinal": int(row[5]),
            "unique": int(row[0]) in unique_column_ids,
        }
        for row in columns
    ]
    safe_foreign_keys = [
        {
            "ordinal": int(row[0]),
            "sequence": int(row[1]),
            "on_update": str(row[5]),
            "on_delete": str(row[6]),
            "match": str(row[7]),
        }
        for row in foreign_keys
    ]
    inventory = {
        "role": role,
        "columns": safe_columns,
        "indexes": sorted(
            safe_indexes,
            key=lambda item: (
                item["origin"],
                item["column_ordinals"],
                item["unique"],
            ),
        ),
        "foreign_keys": safe_foreign_keys,
    }
    expected_internal_indexes = len(indexes) == 3 and all(
        bool(index[2]) and str(index[1]).startswith("sqlite_autoindex_")
        for index in indexes
    )
    return inventory, named_index_count, expected_internal_indexes


def _verify_schema(
    connection: sqlite3.Connection,
    attempt_ddl: str,
    primary_ddl: str,
) -> dict[str, Any]:
    objects = connection.execute(
        "SELECT type, name, tbl_name, sql FROM sqlite_master "
        "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
    ).fetchall()
    expected_tables = {
        ATTEMPT_RESERVATION_TABLE: attempt_ddl,
        TABLE_NAME: primary_ddl,
    }
    table_rows = {
        str(row[1]): row for row in objects if str(row[0]) == "table"
    }
    unexpected_objects = [
        row
        for row in objects
        if str(row[0]) != "table" or str(row[1]) not in expected_tables
    ]
    table_set_exact = set(table_rows) == set(expected_tables)
    statements_exact = table_set_exact and all(
        _normalize_create_statement(str(table_rows[name][3]))
        == _normalize_create_statement(statement)
        for name, statement in expected_tables.items()
    )

    inventories: list[dict[str, Any]] = []
    named_index_count = 0
    internal_indexes_exact = True
    for table, role in (
        (ATTEMPT_RESERVATION_TABLE, "attempt_reservation"),
        (TABLE_NAME, "primary_record"),
    ):
        if table not in table_rows:
            internal_indexes_exact = False
            continue
        inventory, named_count, indexes_exact = _schema_inventory_for_table(
            connection,
            table,
            role,
        )
        inventories.append(inventory)
        named_index_count += named_count
        internal_indexes_exact = internal_indexes_exact and indexes_exact

    unexpected_count = len(unexpected_objects) + named_index_count
    inventory_projection = {
        "tables": sorted(inventories, key=lambda item: item["role"]),
        "expected_user_table_count": 2,
        "unexpected_user_schema_object_count": unexpected_count,
        "expected_trigger_count": 0,
        "expected_view_count": 0,
    }
    return {
        "primary_verified": TABLE_NAME in table_rows,
        "attempt_verified": ATTEMPT_RESERVATION_TABLE in table_rows,
        "indexes_verified": internal_indexes_exact and named_index_count == 0,
        "constraints_verified": statements_exact and internal_indexes_exact,
        "unexpected_count": unexpected_count,
        "inventory_hash": _sha256_bytes(_canonical_json_bytes(inventory_projection)),
        "exact": (
            table_set_exact
            and statements_exact
            and internal_indexes_exact
            and unexpected_count == 0
        ),
    }


def _read_zero_row_counts(connection: sqlite3.Connection) -> tuple[int, int]:
    primary_count = int(
        connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    )
    attempt_count = int(
        connection.execute(
            f"SELECT COUNT(*) FROM {ATTEMPT_RESERVATION_TABLE}"
        ).fetchone()[0]
    )
    return primary_count, attempt_count


def _run_integrity_check(connection: sqlite3.Connection) -> bool:
    result = connection.execute("PRAGMA quick_check").fetchone()
    return bool(result and str(result[0]).lower() == "ok")


def _apply_schema_result(state: dict[str, Any], result: dict[str, Any]) -> None:
    state["target_primary_table_verified"] = result["primary_verified"]
    state["target_attempt_reservation_table_verified"] = result["attempt_verified"]
    state["target_indexes_verified"] = result["indexes_verified"]
    state["target_constraints_verified"] = result["constraints_verified"]
    state["unexpected_user_schema_object_count"] = result["unexpected_count"]
    state["target_schema_inventory_safe_hash"] = result["inventory_hash"]
    state["schema_verification_completed"] = True


def _verify_schema_or_fail(
    state: dict[str, Any],
    connection: sqlite3.Connection,
    attempt_ddl: str,
    primary_ddl: str,
) -> None:
    result = _verify_schema(connection, attempt_ddl, primary_ddl)
    _apply_schema_result(state, result)
    if result["unexpected_count"]:
        raise _ControlledTerminalFailure("unexpected_schema_object")
    if not result["exact"]:
        raise _ControlledTerminalFailure("schema_verification_failure")


def _verify_rows_or_fail(
    state: dict[str, Any],
    connection: sqlite3.Connection,
) -> None:
    primary_count, attempt_count = _read_zero_row_counts(connection)
    state["base_record_row_count"] = primary_count
    state["attempt_reservation_row_count"] = attempt_count
    state["zero_row_verification_completed"] = True
    if primary_count:
        raise _ControlledTerminalFailure("nonzero_candidate_rows")
    if attempt_count:
        raise _ControlledTerminalFailure("nonzero_attempt_reservations")


def _verify_integrity_or_fail(
    state: dict[str, Any],
    connection: sqlite3.Connection,
) -> None:
    passed = _run_integrity_check(connection)
    state["integrity_check"] = "ok" if passed else "failed"
    if not passed:
        raise _ControlledTerminalFailure("integrity_check_failure")


def _close_connection(connection: sqlite3.Connection) -> None:
    connection.close()


def _unlink_exact(path: Path) -> None:
    os.unlink(path)


def _rmdir_exact(path: Path) -> None:
    os.rmdir(path)


def _exact_state(path: Path) -> bool:
    return _lstat_optional(path) is not None


def _update_final_exact_state(
    state: dict[str, Any],
    target: Path | None,
    receipt: Path | None,
    sidecars: tuple[Path, Path, Path] | None,
) -> bool:
    if target is None or receipt is None or sidecars is None:
        return False
    try:
        state["final_target_exists"] = _exact_state(target)
        state["final_receipt_exists"] = _exact_state(receipt)
        state["final_journal_exists"] = _exact_state(sidecars[0])
        state["final_WAL_exists"] = _exact_state(sidecars[1])
        state["final_SHM_exists"] = _exact_state(sidecars[2])
        state["unexpected_final_sidecar_state"] = any(
            (
                state["final_journal_exists"],
                state["final_WAL_exists"],
                state["final_SHM_exists"],
            )
        )
        state["post_connection_exact_state_checked"] = True
        return True
    except BaseException:
        state["final_target_exists"] = "unknown_due_to_terminal_failure"
        state["final_receipt_exists"] = "unknown_due_to_terminal_failure"
        state["final_journal_exists"] = "unknown_due_to_terminal_failure"
        state["final_WAL_exists"] = "unknown_due_to_terminal_failure"
        state["final_SHM_exists"] = "unknown_due_to_terminal_failure"
        state["unexpected_final_sidecar_state"] = (
            "unknown_due_to_terminal_failure"
        )
        return False


def _receipt_projection(state: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "receipt_schema": RECEIPT_SCHEMA,
        "receipt_version": RECEIPT_VERSION,
        "target_kind": TARGET_KIND,
        "locked_target_logical_label": LOCKED_TARGET_LOGICAL_LABEL,
        "locked_receipt_logical_label": LOCKED_RECEIPT_LOGICAL_LABEL,
        "target_identity_safe_hash": TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "attempt_table_DDL_safe_hash": ATTEMPT_TABLE_DDL_SAFE_HASH,
        "primary_table_DDL_safe_hash": PRIMARY_TABLE_DDL_SAFE_HASH,
        "target_preexistence_classification": state[
            "target_preexistence_classification"
        ],
        "runner_result_schema": RESULT_SCHEMA,
        "runner_result_version": RESULT_VERSION,
        "runner_module_hash_classification": (
            "not_recorded_self_modification_avoided"
        ),
        "execution_phase": "completed",
        "safe_error_code": "none",
        "SQLite_connection_session_limit": state[
            "SQLite_connection_session_limit"
        ],
        "SQLite_connection_open_count": state["SQLite_connection_open_count"],
        "SQLite_connection_reopen_count": state[
            "SQLite_connection_reopen_count"
        ],
        "SQLite_create_count": state["SQLite_create_count"],
        "transaction_begin_count": state["transaction_begin_count"],
        "commit_call_count": state["commit_call_count"],
        "commit_returned_successfully": state[
            "commit_returned_successfully"
        ],
        "schema_DDL_statement_count": state["schema_DDL_statement_count"],
        "candidate_table_DML_statement_count": state[
            "candidate_table_DML_statement_count"
        ],
        "attempt_table_DML_statement_count": state[
            "attempt_table_DML_statement_count"
        ],
        "other_user_DML_statement_count": state[
            "other_user_DML_statement_count"
        ],
        "target_schema_inventory_safe_hash": state[
            "target_schema_inventory_safe_hash"
        ],
        "base_record_row_count": state["base_record_row_count"],
        "attempt_reservation_row_count": state[
            "attempt_reservation_row_count"
        ],
        "integrity_check": state["integrity_check"],
        "target_created_this_run": state["target_created_this_run"],
        "cleanup_performed": False,
        "raw_row_retained": False,
        "raw_author_identity_retained": False,
        "absolute_path_recorded": False,
        "production_object_created": False,
        "network_called": False,
        "gate_activated": False,
        "persistence_mutation_performed": False,
        "directory_enumeration_performed": False,
        "alternate_source_used": False,
        "protected_payload_read": False,
        "safe_capture_receipt_read": False,
        "source_or_package_read": False,
        "candidate_mutation_performed": False,
        "attempt_reservation_mutation_performed": False,
    }
    receipt["initialization_receipt_safe_hash"] = _sha256_bytes(
        _canonical_json_bytes(receipt)
    )
    return receipt


def _receipt_safe_hash(receipt: dict[str, Any]) -> str:
    projection = dict(receipt)
    projection.pop("initialization_receipt_safe_hash", None)
    return _sha256_bytes(_canonical_json_bytes(projection))


def _cleanup_is_eligible(
    state: dict[str, Any],
    *,
    target_absent_before: bool,
    created_directories: list[Path],
    receipt_successful: bool,
    allow_cleanup: bool,
) -> bool:
    created_artifact_exists = bool(
        state["target_created_this_run"] or created_directories
    )
    return bool(
        allow_cleanup
        and target_absent_before
        and created_artifact_exists
        and not state["commit_returned_successfully"]
        and not state["commit_outcome_ambiguous"]
        and state["candidate_table_DML_statement_count"] == 0
        and state["attempt_table_DML_statement_count"] == 0
        and state["other_user_DML_statement_count"] == 0
        and not receipt_successful
        and not state["receipt_created_this_run"]
    )


def _perform_bounded_cleanup(
    state: dict[str, Any],
    *,
    target: Path,
    sidecars: tuple[Path, Path, Path],
    created_directories: list[Path],
) -> None:
    state["cleanup_attempted"] = True
    state["execution_phase"] = "perform_cleanup"
    try:
        _failure_injection_hook("perform_cleanup", "during_cleanup")
        for path in sidecars:
            if _lstat_optional(path) is not None:
                _unlink_exact(path)
                state["cleanup_file_count"] += 1
        if state["target_created_this_run"] and _lstat_optional(target) is not None:
            _unlink_exact(target)
            state["cleanup_file_count"] += 1
        for directory in reversed(created_directories):
            if _lstat_optional(directory) is not None:
                _rmdir_exact(directory)
                state["cleanup_directory_count"] += 1
        state["cleanup_performed"] = True
    except BaseException:
        state["cleanup_incomplete_or_ambiguous"] = True
        state["cleanup_performed"] = False
        state["safe_error_code"] = "cleanup_failure"


def _bounded_result(state: dict[str, Any]) -> dict[str, Any]:
    try:
        return {field: state[field] for field in REQUIRED_RESULT_FIELDS}
    except BaseException:
        fallback = _new_result_state()
        fallback["execution_phase"] = "terminal_failure"
        fallback["terminal_phase"] = "terminal_failure"
        fallback["safe_error_code"] = "unexpected_internal_failure"
        fallback["target_initialization_outcome"] = "failed_safe"
        return {field: fallback[field] for field in REQUIRED_RESULT_FIELDS}


def run_governed_nonproduction_target_initialization_smoke(
    *,
    repository_root: Path,
    expected_target_identity_safe_hash: str,
    expected_target_authorization_contract_safe_hash: str,
    allow_same_run_empty_target_cleanup: bool,
) -> dict[str, Any]:
    """Initialize or verify one locked synthetic target with bounded diagnostics."""

    state = _new_result_state()
    target: Path | None = None
    receipt_path: Path | None = None
    sidecars: tuple[Path, Path, Path] | None = None
    created_directories: list[Path] = []
    connection: sqlite3.Connection | None = None
    transaction_started = False
    target_absent_before = False
    receipt_successful = False
    failure: BaseException | None = None
    attempt_ddl = ""
    primary_ddl = ""

    try:
        _failure_injection_hook("terminal_failure", "unexpected")
        _enter_phase(state, "validate_inputs")
        if (
            not isinstance(repository_root, Path)
            or not repository_root.is_absolute()
            or not isinstance(expected_target_identity_safe_hash, str)
            or not isinstance(expected_target_authorization_contract_safe_hash, str)
            or not isinstance(allow_same_run_empty_target_cleanup, bool)
        ):
            raise _ControlledTerminalFailure("invalid_input")
        _p1_repository_root_observer(repository_root)

        _enter_phase(state, "verify_locked_governance")
        if (
            expected_target_identity_safe_hash != TARGET_IDENTITY_SAFE_HASH
            or expected_target_authorization_contract_safe_hash
            != TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
            or LOCKED_TARGET_LOGICAL_LABEL
            != _EXPECTED_LOCKED_TARGET_LOGICAL_LABEL
            or LOCKED_RECEIPT_LOGICAL_LABEL
            != _EXPECTED_LOCKED_RECEIPT_LOGICAL_LABEL
            or LOGICAL_RUNTIME_TARGET_LABEL
            != _EXPECTED_LOCKED_TARGET_LOGICAL_LABEL
            or TABLE_NAME != _EXPECTED_TARGET_PRIMARY_TABLE
            or ATTEMPT_RESERVATION_TABLE != _EXPECTED_TARGET_ATTEMPT_TABLE
        ):
            raise _ControlledTerminalFailure("governance_hash_mismatch")

        _enter_phase(state, "verify_committed_DDL")
        attempt_ddl, primary_ddl = _committed_ddl_statements()
        if (
            _sha256_text(attempt_ddl) != ATTEMPT_TABLE_DDL_SAFE_HASH
            or _sha256_text(primary_ddl) != PRIMARY_TABLE_DDL_SAFE_HASH
        ):
            raise _ControlledTerminalFailure("committed_DDL_hash_mismatch")
        state["committed_DDL_hashes_verified"] = True

        _enter_phase(state, "derive_exact_paths")
        target_parts = _validate_logical_label(LOCKED_TARGET_LOGICAL_LABEL)
        receipt_parts = _validate_logical_label(LOCKED_RECEIPT_LOGICAL_LABEL)
        repository_root = Path(os.path.abspath(os.fspath(repository_root)))
        target = repository_root.joinpath(*target_parts)
        receipt_path = repository_root.joinpath(*receipt_parts)
        if (
            os.path.commonpath((repository_root, target))
            != os.fspath(repository_root)
            or os.path.commonpath((repository_root, receipt_path))
            != os.fspath(repository_root)
        ):
            raise _ControlledTerminalFailure("path_escape_detected")
        sidecars = (
            Path(f"{target}-journal"),
            Path(f"{target}-wal"),
            Path(f"{target}-shm"),
        )

        _enter_phase(state, "verify_path_components")
        state["path_checks_started"] = True
        _verify_path_components(repository_root, target, receipt_path)
        state["path_escape_check_passed"] = True
        state["symlink_check_passed"] = True
        state["junction_check_passed"] = True
        state["reparse_point_check_passed"] = True
        state["mount_boundary_check_passed"] = True
        state["path_checks_completed"] = True

        _enter_phase(state, "verify_exact_collisions")
        target_metadata = _lstat_optional(target)
        receipt_metadata = _lstat_optional(receipt_path)
        sidecar_metadata = tuple(_lstat_optional(path) for path in sidecars)
        state["target_exists_before_run"] = target_metadata is not None
        state["receipt_exists_before_run"] = receipt_metadata is not None
        state["sidecar_exists_before_run"] = any(
            metadata is not None for metadata in sidecar_metadata
        )
        if receipt_metadata is not None:
            if not _is_regular_file(receipt_metadata):
                raise _ControlledTerminalFailure("unsafe_target_collision")
            raise _ControlledTerminalFailure("receipt_preexists")
        if target_metadata is not None and not _is_regular_file(target_metadata):
            raise _ControlledTerminalFailure("unsafe_target_collision")
        if any(metadata is not None for metadata in sidecar_metadata):
            raise _ControlledTerminalFailure("ambiguous_sidecar_state")
        state["collision_checks_completed"] = True

        _enter_phase(state, "classify_target_preexistence")
        target_absent_before = target_metadata is None
        state["target_preexistence_classification"] = (
            "absent" if target_absent_before else "existing_regular_file"
        )

        _enter_phase(state, "create_exact_parents")
        created_directories = _create_exact_parents(
            repository_root,
            target.parent,
            state,
            created_directories,
        )

        _enter_phase(state, "open_SQLite_session")
        connection = _open_sqlite_connection(
            target,
            read_only=not target_absent_before,
        )
        state["SQLite_connection_open_count"] = 1
        connection.set_trace_callback(lambda statement: _trace_statement(state, statement))
        if target_absent_before:
            target_after_open = _lstat_optional(target)
            if target_after_open is None or not _is_regular_file(target_after_open):
                raise _ControlledTerminalFailure("SQLite_connect_failure")
            state["target_created_this_run"] = True
            state["SQLite_create_count"] = 1

            _enter_phase(state, "begin_schema_transaction")
            connection.execute("BEGIN IMMEDIATE")
            transaction_started = True
            state["transaction_begin_count"] = 1
            _failure_injection_hook("begin_schema_transaction", "after_begin")

            state["execution_phase"] = "initialize_schema"
            _failure_injection_hook("initialize_schema", "before_attempt_DDL")
            connection.execute(attempt_ddl)
            state["schema_DDL_statement_count"] = 1
            _failure_injection_hook("initialize_schema", "before_primary_DDL")
            connection.execute(primary_ddl)
            state["schema_DDL_statement_count"] = 2

        _enter_phase(state, "verify_schema")
        _verify_schema_or_fail(state, connection, attempt_ddl, primary_ddl)

        _enter_phase(state, "verify_zero_rows")
        _verify_rows_or_fail(state, connection)

        _enter_phase(state, "run_integrity_check")
        _verify_integrity_or_fail(state, connection)

        if target_absent_before:
            state["execution_phase"] = "commit_initialization"
            _failure_injection_hook("commit_initialization", "known_failure")
            state["commit_call_count"] = 1
            connection.commit()
            transaction_started = False
            _failure_injection_hook("commit_initialization", "ambiguous")
            state["commit_returned_successfully"] = True

            _enter_phase(state, "verify_post_commit_same_session")
            _verify_schema_or_fail(state, connection, attempt_ddl, primary_ddl)
            _verify_rows_or_fail(state, connection)
            _verify_integrity_or_fail(state, connection)

        state["execution_phase"] = "close_SQLite_session"
        _close_connection(connection)
        connection = None
        state["connection_close_count"] = 1
        _failure_injection_hook("close_SQLite_session", "after_close")

        _enter_phase(state, "verify_post_connection_state")
        if not _update_final_exact_state(state, target, receipt_path, sidecars):
            raise _ControlledTerminalFailure("post_connection_state_ambiguous")
        if state["unexpected_final_sidecar_state"]:
            raise _ControlledTerminalFailure("ambiguous_sidecar_state")

        _enter_phase(state, "build_initialization_receipt")
        receipt = _receipt_projection(state)
        state["initialization_receipt_built"] = True
        state["initialization_receipt_safe_hash"] = receipt[
            "initialization_receipt_safe_hash"
        ]
        receipt_bytes = _canonical_json_bytes(receipt)

        _enter_phase(state, "scan_initialization_receipt")
        scan = scan_protected_value_boundary(
            receipt,
            profile=SAFE_CAPTURE_RECEIPT_PROFILE,
        )
        if (
            scan.get("passed") is not True
            or scan.get("finding_count") != 0
            or scan.get("protected_value_exposed") is not False
            or scan.get("raw_key_echoed") is not False
            or scan.get("raw_value_echoed") is not False
        ):
            state["privacy_issue_stop"] = True
            raise _ControlledTerminalFailure("receipt_privacy_scan_failure")
        state["initialization_receipt_privacy_scan_passed"] = True

        state["execution_phase"] = "write_initialization_receipt"
        _failure_injection_hook(
            "write_initialization_receipt", "before_exclusive_write"
        )
        with receipt_path.open("xb") as receipt_handle:
            state["receipt_created_this_run"] = True
            receipt_handle.write(receipt_bytes)
            receipt_handle.flush()
            _failure_injection_hook("write_initialization_receipt", "before_fsync")
            os.fsync(receipt_handle.fileno())
        state["initialization_receipt_exclusive_write_performed"] = True

        state["execution_phase"] = "readback_initialization_receipt"
        _failure_injection_hook(
            "readback_initialization_receipt", "before_readback"
        )
        readback_bytes = receipt_path.read_bytes()
        readback = json.loads(readback_bytes.decode("utf-8"))
        if readback != receipt:
            raise _ControlledTerminalFailure("receipt_readback_failure")
        _failure_injection_hook(
            "readback_initialization_receipt", "before_hash_verification"
        )
        if (
            _receipt_safe_hash(readback)
            != readback.get("initialization_receipt_safe_hash")
        ):
            raise _ControlledTerminalFailure("receipt_hash_mismatch")
        if readback_bytes != _canonical_json_bytes(readback):
            raise _ControlledTerminalFailure("receipt_hash_mismatch")
        state["initialization_receipt_readback_verified"] = True
        state["initialization_receipt_byte_sha256"] = _sha256_bytes(readback_bytes)
        receipt_successful = True

        _enter_phase(state, "completed")
        state["terminal_phase"] = "completed"
        state["passed"] = True
        state["decision"] = "ready"
        state["safe_error_code"] = "none"
        state["target_initialization_outcome"] = (
            "initialized_schema_only"
            if target_absent_before
            else "verified_existing_exact_empty_read_only"
        )
        _update_final_exact_state(state, target, receipt_path, sidecars)
    except BaseException as caught:
        failure = caught
    finally:
        if connection is not None:
            if (
                transaction_started
                and not state["commit_returned_successfully"]
                and not state["commit_outcome_ambiguous"]
            ):
                try:
                    connection.rollback()
                    state["rollback_count"] += 1
                    transaction_started = False
                except BaseException:
                    state["cleanup_incomplete_or_ambiguous"] = True
            try:
                _close_connection(connection)
                state["connection_close_count"] += 1
            except BaseException as close_failure:
                if failure is None:
                    failure = close_failure
                    state["execution_phase"] = "close_SQLite_session"
            connection = None

    if failure is not None:
        state["passed"] = False
        state["decision"] = "needs_fix"
        state["terminal_phase"] = state["execution_phase"]
        state["target_initialization_outcome"] = "failed_safe"
        if isinstance(failure, _ControlledTerminalFailure):
            code = failure.safe_error_code
        else:
            code = _default_error_for_phase(state["execution_phase"])
        if code not in SAFE_ERROR_CODES:
            code = "unexpected_internal_failure"
        if code == "commit_outcome_ambiguous":
            state["commit_outcome_ambiguous"] = True
        if code == "receipt_privacy_scan_failure":
            state["privacy_issue_stop"] = True
        state["safe_error_code"] = code

        if target is not None and sidecars is not None:
            state["execution_phase"] = "evaluate_cleanup"
            try:
                _failure_injection_hook("evaluate_cleanup", "before")
                state["cleanup_eligible"] = _cleanup_is_eligible(
                    state,
                    target_absent_before=target_absent_before,
                    created_directories=created_directories,
                    receipt_successful=receipt_successful,
                    allow_cleanup=allow_same_run_empty_target_cleanup,
                )
            except BaseException:
                state["cleanup_eligible"] = False
                state["cleanup_incomplete_or_ambiguous"] = True
                state["safe_error_code"] = "cleanup_failure"
            if state["cleanup_eligible"]:
                _perform_bounded_cleanup(
                    state,
                    target=target,
                    sidecars=sidecars,
                    created_directories=created_directories,
                )
            _update_final_exact_state(state, target, receipt_path, sidecars)

    return _bounded_result(state)
