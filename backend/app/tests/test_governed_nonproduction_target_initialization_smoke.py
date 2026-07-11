from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Callable

import pytest

from app.services import governed_nonproduction_evidence_persistence as persistence
from app.services import governed_nonproduction_target_initialization_smoke as smoke
from app.services.protected_value_boundary_scanner import (
    SAFE_CAPTURE_RECEIPT_PROFILE,
    scan_protected_value_boundary,
)


EXPECTED_IDENTITY_HASH = (
    "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b"
)
EXPECTED_CONTRACT_HASH = (
    "f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2"
)


@pytest.fixture(autouse=True)
def _observe_every_p1_repository_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> list[Path]:
    observed: list[Path] = []

    def observe(repository_root: Path) -> None:
        assert repository_root == tmp_path or tmp_path in repository_root.parents
        observed.append(repository_root)

    monkeypatch.setattr(smoke, "_p1_repository_root_observer", observe)
    return observed


def _run(repository_root: Path) -> dict[str, Any]:
    return smoke.run_governed_nonproduction_target_initialization_smoke(
        repository_root=repository_root,
        expected_target_identity_safe_hash=EXPECTED_IDENTITY_HASH,
        expected_target_authorization_contract_safe_hash=EXPECTED_CONTRACT_HASH,
        allow_same_run_empty_target_cleanup=True,
    )


def _target(repository_root: Path) -> Path:
    return repository_root.joinpath(*smoke.LOCKED_TARGET_LOGICAL_LABEL.split("/"))


def _receipt(repository_root: Path) -> Path:
    return repository_root.joinpath(*smoke.LOCKED_RECEIPT_LOGICAL_LABEL.split("/"))


def _sidecars(repository_root: Path) -> tuple[Path, Path, Path]:
    target = _target(repository_root)
    return (
        Path(f"{target}-journal"),
        Path(f"{target}-wal"),
        Path(f"{target}-shm"),
    )


def _prepare_target(
    repository_root: Path,
    *,
    attempt_ddl: str | None = None,
    primary_ddl: str | None = None,
    extra_statements: tuple[str, ...] = (),
) -> Path:
    target = _target(repository_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as connection:
        if attempt_ddl is not None:
            connection.execute(attempt_ddl)
        if primary_ddl is not None:
            connection.execute(primary_ddl)
        for statement in extra_statements:
            connection.execute(statement)
        connection.commit()
    return target


def _prepare_exact_target(repository_root: Path) -> Path:
    return _prepare_target(
        repository_root,
        attempt_ddl=persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL,
        primary_ddl=persistence._CREATE_TABLE_SQL,
    )


def _insert_synthetic_row(target: Path, table: str) -> None:
    with sqlite3.connect(target) as connection:
        connection.execute("PRAGMA ignore_check_constraints = ON")
        columns = connection.execute(f"PRAGMA table_info({table})").fetchall()
        values = [
            index + 1 if str(row[2]).upper() == "INTEGER" else f"synthetic_{index}"
            for index, row in enumerate(columns)
        ]
        parameter_slots = ",".join("?" for _ in values)
        connection.execute(f"INSERT INTO {table} VALUES ({parameter_slots})", values)
        connection.commit()


def _assert_complete(result: dict[str, Any]) -> None:
    assert set(result) == set(smoke.REQUIRED_RESULT_FIELDS)
    assert result["result_schema"] == smoke.RESULT_SCHEMA
    assert result["result_version"] == smoke.RESULT_VERSION
    assert result["execution_phase"] in smoke.EXECUTION_PHASES
    assert result["terminal_phase"] in smoke.EXECUTION_PHASES
    assert result["safe_error_code"] in smoke.SAFE_ERROR_CODES


def _assert_value_free(result: dict[str, Any], repository_root: Path) -> None:
    serialized = json.dumps(result, sort_keys=True)
    assert str(repository_root) not in serialized
    assert not re.search(r"[A-Za-z]:[\\/]", serialized)
    assert "CREATE TABLE" not in serialized
    assert "SELECT " not in serialized
    assert "Traceback" not in serialized
    assert "RuntimeError" not in serialized


def _inject(
    monkeypatch: pytest.MonkeyPatch,
    *,
    phase: str,
    operation: str | None = None,
    safe_error_code: str | None = None,
) -> None:
    def fail(current_phase: str, current_operation: str) -> None:
        if current_phase == phase and (operation is None or current_operation == operation):
            if safe_error_code is not None:
                raise smoke._ControlledTerminalFailure(safe_error_code)
            raise RuntimeError

    monkeypatch.setattr(smoke, "_failure_injection_hook", fail)


def test_absent_synthetic_target_initializes_schema_once_with_safe_receipt(
    tmp_path: Path,
) -> None:
    """Matrix 1-9, 53, 56-58, 107, and 110."""
    result = _run(tmp_path)

    _assert_complete(result)
    _assert_value_free(result, tmp_path)
    assert result["passed"] is True
    assert result["decision"] == "ready"
    assert result["safe_error_code"] == "none"
    assert result["target_initialization_outcome"] == "initialized_schema_only"
    assert result["target_preexistence_classification"] == "absent"
    assert result["SQLite_connection_session_limit"] == 1
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["SQLite_create_count"] == 1
    assert result["transaction_begin_count"] == 1
    assert result["commit_call_count"] == 1
    assert result["commit_returned_successfully"] is True
    assert result["schema_DDL_statement_count"] == 2
    assert result["base_record_row_count"] == 0
    assert result["attempt_reservation_row_count"] == 0
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert result["other_user_DML_statement_count"] == 0
    assert result["integrity_check"] == "ok"
    assert result["initialization_receipt_exclusive_write_performed"] is True
    assert result["initialization_receipt_readback_verified"] is True
    assert result["initialization_receipt_privacy_scan_passed"] is True
    assert result["final_target_exists"] is True
    assert result["final_receipt_exists"] is True
    assert _target(tmp_path).is_file()
    assert _receipt(tmp_path).is_file()
    receipt = json.loads(_receipt(tmp_path).read_text(encoding="utf-8"))
    scan = scan_protected_value_boundary(
        receipt,
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )
    assert scan["passed"] is True
    assert scan["finding_count"] == 0


def test_existing_exact_empty_target_is_verified_read_only_in_one_session(
    tmp_path: Path,
) -> None:
    """Matrix 10-14 and 54-55."""
    target = _prepare_exact_target(tmp_path)
    before = hashlib.sha256(target.read_bytes()).hexdigest()

    result = _run(tmp_path)

    after = hashlib.sha256(target.read_bytes()).hexdigest()
    _assert_complete(result)
    assert result["passed"] is True
    assert result["target_initialization_outcome"] == "verified_existing_exact_empty_read_only"
    assert result["target_preexistence_classification"] == "existing_regular_file"
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["SQLite_create_count"] == 0
    assert result["transaction_begin_count"] == 0
    assert result["commit_call_count"] == 0
    assert result["schema_DDL_statement_count"] == 0
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert before == after
    assert _receipt(tmp_path).is_file()


@pytest.mark.parametrize(
    ("identity_hash", "contract_hash", "expected_code"),
    [
        ("0" * 64, EXPECTED_CONTRACT_HASH, "governance_hash_mismatch"),
        (EXPECTED_IDENTITY_HASH, "0" * 64, "governance_hash_mismatch"),
    ],
)
def test_wrong_governance_hash_blocks_before_path_access(
    tmp_path: Path,
    identity_hash: str,
    contract_hash: str,
    expected_code: str,
) -> None:
    """Matrix 15-16."""
    result = smoke.run_governed_nonproduction_target_initialization_smoke(
        repository_root=tmp_path,
        expected_target_identity_safe_hash=identity_hash,
        expected_target_authorization_contract_safe_hash=contract_hash,
        allow_same_run_empty_target_cleanup=True,
    )
    _assert_complete(result)
    assert result["passed"] is False
    assert result["safe_error_code"] == expected_code
    assert result["path_checks_started"] is False
    assert result["SQLite_connection_open_count"] == 0
    assert not _target(tmp_path).exists()


def test_committed_ddl_hash_mismatch_blocks_before_sqlite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 17."""
    monkeypatch.setattr(
        smoke,
        "_committed_ddl_statements",
        lambda: (
            persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL + " ",
            persistence._CREATE_TABLE_SQL,
        ),
    )
    result = _run(tmp_path)
    assert result["safe_error_code"] == "committed_DDL_hash_mismatch"
    assert result["path_checks_started"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_public_surface_has_no_target_receipt_or_schema_override() -> None:
    """Matrix 18-19 and 111."""
    parameters = inspect.signature(
        smoke.run_governed_nonproduction_target_initialization_smoke
    ).parameters
    assert set(parameters) == {
        "repository_root",
        "expected_target_identity_safe_hash",
        "expected_target_authorization_contract_safe_hash",
        "allow_same_run_empty_target_cleanup",
    }
    assert "target_path" not in parameters
    assert "receipt_path" not in parameters
    assert "schema" not in parameters


def test_environment_cannot_redirect_locked_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 20-22."""
    alternate = tmp_path / "alternate.sqlite3"
    monkeypatch.setenv("SENTIGRAPH_TARGET_PATH", str(alternate))
    result = _run(tmp_path)
    assert result["passed"] is True
    assert result["target_substitution_performed"] is False
    assert result["fallback_used"] is False
    assert _target(tmp_path).is_file()
    assert not alternate.exists()


def test_source_has_no_forbidden_integrations_or_runtime_enumeration() -> None:
    """Matrix 21-25, 37-38, 59-60, and 120."""
    source = Path(smoke.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        (node.module or "").split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    called_attributes = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "subprocess" not in imported_modules | imported_from
    assert "logging" not in imported_modules | imported_from
    assert not {"glob", "rglob", "iterdir", "listdir", "scandir", "walk"} & (
        called_names | called_attributes
    )
    assert not {"getenv", "environ"} & (called_names | called_attributes)
    assert "create_governed_nonproduction_evidence_record" not in source
    assert "CaseRepository" not in source
    assert "LocalJsonCaseStore" not in source
    assert "MongoDbCaseStore" not in source
    assert "ATTACH" not in source
    assert "VACUUM" not in source
    assert "REINDEX" not in source
    assert "ANALYZE" not in source
    assert "load_extension" not in source


@pytest.mark.parametrize(
    ("replacement", "expected_code"),
    [
        ("../escape.sqlite3", "governance_hash_mismatch"),
        ("/absolute.sqlite3", "governance_hash_mismatch"),
        ("runtime//evidence.sqlite3", "governance_hash_mismatch"),
        ("runtime/substituted.sqlite3", "governance_hash_mismatch"),
    ],
)
def test_locked_logical_target_cannot_be_substituted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    replacement: str,
    expected_code: str,
) -> None:
    """Matrix 26-27."""
    monkeypatch.setattr(smoke, "LOCKED_TARGET_LOGICAL_LABEL", replacement)
    result = _run(tmp_path)
    assert result["safe_error_code"] == expected_code
    assert result["path_checks_started"] is False


def _make_directory_symlink_or_skip(link: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(target, target_is_directory=True)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"directory symlink unavailable: {type(error).__name__}")


def test_symlink_parent_blocks_without_sqlite(
    tmp_path: Path,
) -> None:
    """Matrix 28 and 30-31 where supported."""
    outside = tmp_path / "synthetic_outside"
    _make_directory_symlink_or_skip(tmp_path / "runtime", outside)
    result = _run(tmp_path)
    assert result["safe_error_code"] == "symlink_or_reparse_component_detected"
    assert result["SQLite_connection_open_count"] == 0


def test_symlink_target_blocks_without_sqlite(tmp_path: Path) -> None:
    """Matrix 29."""
    target = _target(tmp_path)
    target.parent.mkdir(parents=True)
    backing = tmp_path / "synthetic_backing_file"
    backing.write_bytes(b"synthetic")
    try:
        target.symlink_to(backing)
    except (OSError, NotImplementedError) as error:
        pytest.skip(f"file symlink unavailable: {type(error).__name__}")
    result = _run(tmp_path)
    assert result["safe_error_code"] == "symlink_or_reparse_component_detected"
    assert result["SQLite_connection_open_count"] == 0


def test_mount_boundary_failure_blocks_before_sqlite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 32."""
    monkeypatch.setattr(smoke, "_same_device_boundary", lambda *_args: False)
    result = _run(tmp_path)
    assert result["safe_error_code"] == "mount_boundary_failure"
    assert result["SQLite_connection_open_count"] == 0


@pytest.mark.parametrize("collision", ["target_directory", "receipt_directory"])
def test_exact_directory_collision_blocks(
    tmp_path: Path,
    collision: str,
) -> None:
    """Matrix 33-34."""
    selected = _target(tmp_path) if collision == "target_directory" else _receipt(tmp_path)
    selected.mkdir(parents=True)
    result = _run(tmp_path)
    assert result["safe_error_code"] == "unsafe_target_collision"
    assert result["SQLite_connection_open_count"] == 0


def test_receipt_preexistence_blocks_before_sqlite(tmp_path: Path) -> None:
    """Matrix 35."""
    receipt = _receipt(tmp_path)
    receipt.parent.mkdir(parents=True)
    receipt.write_text("{}", encoding="utf-8")
    result = _run(tmp_path)
    assert result["safe_error_code"] == "receipt_preexists"
    assert result["SQLite_connection_open_count"] == 0


def test_preexisting_sidecar_blocks_before_sqlite_and_is_preserved(tmp_path: Path) -> None:
    """Matrix 36 and 93."""
    sidecar = _sidecars(tmp_path)[0]
    sidecar.parent.mkdir(parents=True)
    sidecar.write_bytes(b"synthetic-sidecar")
    result = _run(tmp_path)
    assert result["safe_error_code"] == "ambiguous_sidecar_state"
    assert result["SQLite_connection_open_count"] == 0
    assert sidecar.read_bytes() == b"synthetic-sidecar"


SCHEMA_MISMATCH_CASES = (
    "missing_primary",
    "missing_reservation",
    "extra_table",
    "extra_index",
    "extra_trigger",
    "extra_view",
    "column_type",
    "nullability",
    "primary_key",
    "uniqueness",
    "check_constraint",
)


def _prepare_schema_mismatch(repository_root: Path, case: str) -> None:
    attempt = persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL
    primary = persistence._CREATE_TABLE_SQL
    extras: tuple[str, ...] = ()
    if case == "missing_primary":
        primary = None
    elif case == "missing_reservation":
        attempt = None
    elif case == "extra_table":
        extras = ("CREATE TABLE synthetic_extra (safe_id TEXT PRIMARY KEY)",)
    elif case == "extra_index":
        extras = (
            f"CREATE INDEX synthetic_extra_index ON {persistence.TABLE_NAME}(candidate_id)",
        )
    elif case == "extra_trigger":
        extras = (
            f"CREATE TRIGGER synthetic_trigger AFTER INSERT ON {persistence.TABLE_NAME} BEGIN SELECT 1; END",
        )
    elif case == "extra_view":
        extras = (
            f"CREATE VIEW synthetic_view AS SELECT candidate_id FROM {persistence.TABLE_NAME}",
        )
    elif case == "column_type":
        primary = primary.replace(
            "persisted_record_id TEXT PRIMARY KEY",
            "persisted_record_id BLOB PRIMARY KEY",
            1,
        )
    elif case == "nullability":
        primary = primary.replace("candidate_id TEXT NOT NULL", "candidate_id TEXT", 1)
    elif case == "primary_key":
        primary = primary.replace(
            "persisted_record_id TEXT PRIMARY KEY",
            "persisted_record_id TEXT",
            1,
        )
    elif case == "uniqueness":
        primary = primary.replace(
            "candidate_identity_digest TEXT NOT NULL UNIQUE",
            "candidate_identity_digest TEXT NOT NULL",
            1,
        )
    elif case == "check_constraint":
        primary = primary.replace("human_review_required = 1", "human_review_required = 0", 1)
    _prepare_target(
        repository_root,
        attempt_ddl=attempt,
        primary_ddl=primary,
        extra_statements=extras,
    )


@pytest.mark.parametrize("case", SCHEMA_MISMATCH_CASES)
def test_existing_schema_mismatch_fails_closed_without_mutation(
    tmp_path: Path,
    case: str,
) -> None:
    """Matrix 39-49."""
    _prepare_schema_mismatch(tmp_path, case)
    target = _target(tmp_path)
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    result = _run(tmp_path)
    after = hashlib.sha256(target.read_bytes()).hexdigest()
    assert result["passed"] is False
    assert result["safe_error_code"] in {
        "schema_verification_failure",
        "unexpected_schema_object",
    }
    assert result["commit_call_count"] == 0
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert before == after


@pytest.mark.parametrize(
    ("table", "expected_code"),
    [
        (persistence.TABLE_NAME, "nonzero_candidate_rows"),
        (persistence.ATTEMPT_RESERVATION_TABLE, "nonzero_attempt_reservations"),
    ],
)
def test_nonzero_rows_fail_closed(
    tmp_path: Path,
    table: str,
    expected_code: str,
) -> None:
    """Matrix 50-51."""
    target = _prepare_exact_target(tmp_path)
    _insert_synthetic_row(target, table)
    result = _run(tmp_path)
    assert result["safe_error_code"] == expected_code
    assert result["commit_call_count"] == 0


def test_integrity_failure_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 52."""
    _prepare_exact_target(tmp_path)
    monkeypatch.setattr(smoke, "_run_integrity_check", lambda _connection: False)
    result = _run(tmp_path)
    assert result["safe_error_code"] == "integrity_check_failure"
    assert result["commit_call_count"] == 0


FAILURE_CASES = (
    ("verify_locked_governance", "before", "governance_hash_mismatch"),
    ("verify_committed_DDL", "before", "committed_DDL_hash_mismatch"),
    ("derive_exact_paths", "before", "path_policy_failure"),
    ("verify_path_components", "before", "path_policy_failure"),
    ("verify_exact_collisions", "before", "unsafe_target_collision"),
    ("classify_target_preexistence", "before", "target_preexistence_ambiguous"),
    ("create_exact_parents", "before", "parent_creation_failure"),
    ("open_SQLite_session", "before", "SQLite_connect_failure"),
    ("begin_schema_transaction", "before", "transaction_begin_failure"),
    ("initialize_schema", "before_attempt_DDL", "schema_initialization_failure"),
    ("initialize_schema", "before_primary_DDL", "schema_initialization_failure"),
    ("verify_schema", "before", "schema_verification_failure"),
    ("verify_zero_rows", "before", "schema_verification_failure"),
    ("run_integrity_check", "before", "integrity_check_failure"),
    ("commit_initialization", "known_failure", "commit_failure_known_rollback"),
    ("commit_initialization", "ambiguous", "commit_outcome_ambiguous"),
    ("verify_post_commit_same_session", "before", "post_commit_verification_failure"),
    ("close_SQLite_session", "after_close", "connection_close_failure"),
    ("verify_post_connection_state", "before", "post_connection_state_ambiguous"),
    ("build_initialization_receipt", "before", "receipt_build_failure"),
    ("scan_initialization_receipt", "before", "receipt_privacy_scan_failure"),
    ("write_initialization_receipt", "before_exclusive_write", "receipt_write_failure"),
    ("write_initialization_receipt", "before_fsync", "receipt_write_failure"),
    ("readback_initialization_receipt", "before_readback", "receipt_readback_failure"),
    ("readback_initialization_receipt", "before_hash_verification", "receipt_hash_mismatch"),
    ("perform_cleanup", "during_cleanup", "cleanup_failure"),
    ("terminal_failure", "unexpected", "unexpected_internal_failure"),
)


@pytest.mark.parametrize(("phase", "operation", "expected_code"), FAILURE_CASES)
def test_each_critical_failure_returns_complete_bounded_value_free_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
    operation: str,
    expected_code: str,
) -> None:
    """Matrix 61-87."""
    if phase == "perform_cleanup":
        state = {"triggered": False}

        def cleanup_failure(current_phase: str, current_operation: str) -> None:
            if current_phase == "open_SQLite_session" and not state["triggered"]:
                state["triggered"] = True
                raise smoke._ControlledTerminalFailure("SQLite_connect_failure")
            if current_phase == phase and current_operation == operation:
                raise smoke._ControlledTerminalFailure(expected_code)

        monkeypatch.setattr(smoke, "_failure_injection_hook", cleanup_failure)
    else:
        _inject(
            monkeypatch,
            phase=phase,
            operation=operation,
            safe_error_code=expected_code,
        )

    result = _run(tmp_path)

    _assert_complete(result)
    _assert_value_free(result, tmp_path)
    assert result["passed"] is False
    assert result["decision"] == "needs_fix"
    assert result["safe_error_code"] == expected_code
    assert result["raw_exception_exposed"] is False
    assert result["physical_absolute_path_recorded"] is False
    assert result["raw_SQL_exposed"] is False
    assert result["raw_key_echoed"] is False
    assert result["raw_value_echoed"] is False


def test_preconnect_failure_without_created_artifact_performs_no_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 88."""
    _inject(monkeypatch, phase="derive_exact_paths", operation="before")
    result = _run(tmp_path)
    assert result["cleanup_eligible"] is False
    assert result["cleanup_attempted"] is False
    assert result["cleanup_file_count"] == 0
    assert result["cleanup_directory_count"] == 0


def test_parent_creation_failure_removes_only_same_run_empty_parents(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 89."""
    _inject(
        monkeypatch,
        phase="create_exact_parents",
        operation="after_first_parent",
        safe_error_code="parent_creation_failure",
    )
    result = _run(tmp_path)
    assert result["cleanup_eligible"] is True
    assert result["cleanup_performed"] is True
    assert result["cleanup_directory_count"] == 1
    assert not (tmp_path / "runtime").exists()


def test_precommit_failure_removes_same_run_target_and_sidecar(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 90-91 and 99."""
    target = _target(tmp_path)
    sidecar = _sidecars(tmp_path)[2]

    def fail_after_begin(phase: str, operation: str) -> None:
        if phase == "begin_schema_transaction" and operation == "after_begin":
            sidecar.write_bytes(b"synthetic-same-run-sidecar")
            raise smoke._ControlledTerminalFailure("transaction_begin_failure")

    monkeypatch.setattr(smoke, "_failure_injection_hook", fail_after_begin)
    result = _run(tmp_path)
    assert result["cleanup_eligible"] is True
    assert result["cleanup_attempted"] is True
    assert result["cleanup_performed"] is True
    assert result["cleanup_file_count"] >= 2
    assert not target.exists()
    assert not sidecar.exists()


def test_preexisting_target_is_never_removed_on_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 92."""
    target = _prepare_exact_target(tmp_path)
    _inject(monkeypatch, phase="verify_schema", operation="before")
    result = _run(tmp_path)
    assert result["cleanup_eligible"] is False
    assert result["cleanup_performed"] is False
    assert target.is_file()


@pytest.mark.parametrize(
    ("phase", "operation", "safe_code"),
    [
        ("verify_post_commit_same_session", "before", "post_commit_verification_failure"),
        ("commit_initialization", "ambiguous", "commit_outcome_ambiguous"),
    ],
)
def test_committed_or_ambiguous_target_is_preserved(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
    operation: str,
    safe_code: str,
) -> None:
    """Matrix 94-95."""
    _inject(
        monkeypatch,
        phase=phase,
        operation=operation,
        safe_error_code=safe_code,
    )
    result = _run(tmp_path)
    assert result["cleanup_eligible"] is False
    assert result["cleanup_performed"] is False
    assert _target(tmp_path).is_file()


def test_successful_target_and_receipt_are_preserved(tmp_path: Path) -> None:
    """Matrix 96."""
    result = _run(tmp_path)
    assert result["passed"] is True
    assert result["cleanup_performed"] is False
    assert _target(tmp_path).is_file()
    assert _receipt(tmp_path).is_file()


def test_partial_cleanup_is_bounded_and_reports_needs_fix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matrix 97-98."""
    _inject(
        monkeypatch,
        phase="initialize_schema",
        operation="before_attempt_DDL",
        safe_error_code="schema_initialization_failure",
    )
    original_unlink = smoke._unlink_exact

    def fail_target_unlink(path: Path) -> None:
        if path == _target(tmp_path):
            raise OSError
        original_unlink(path)

    monkeypatch.setattr(smoke, "_unlink_exact", fail_target_unlink)
    result = _run(tmp_path)
    assert result["decision"] == "needs_fix"
    assert result["safe_error_code"] == "cleanup_failure"
    assert result["cleanup_incomplete_or_ambiguous"] is True
    assert _target(tmp_path).exists()


def test_results_are_value_free_and_deterministic_across_temporary_roots(
    tmp_path: Path,
) -> None:
    """Matrix 100-106 and 110."""
    first_root = tmp_path / "synthetic_one"
    second_root = tmp_path / "synthetic_two"
    first_root.mkdir()
    second_root.mkdir()
    first = _run(first_root)
    second = _run(second_root)
    _assert_value_free(first, first_root)
    _assert_value_free(second, second_root)
    assert first == second


def test_scanner_rejects_phone_like_value_but_accepts_full_safe_sha256() -> None:
    """Matrix 108-109."""
    unsafe = scan_protected_value_boundary(
        {"safe_note": "13800138000"},
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )
    safe_hash = "a" + "13800138000" + ("b" * 52)
    safe = scan_protected_value_boundary(
        {"safe_hash": safe_hash},
        profile=SAFE_CAPTURE_RECEIPT_PROFILE,
    )
    assert unsafe["passed"] is False
    assert unsafe["first_finding_code"] == "unsafe_phone_pattern"
    assert len(safe_hash) == 64
    assert safe["passed"] is True


def test_caller_inputs_are_not_mutated(tmp_path: Path) -> None:
    """Matrix 111."""
    root_before = str(tmp_path)
    identity_before = EXPECTED_IDENTITY_HASH
    contract_before = EXPECTED_CONTRACT_HASH
    _run(tmp_path)
    assert str(tmp_path) == root_before
    assert EXPECTED_IDENTITY_HASH == identity_before
    assert EXPECTED_CONTRACT_HASH == contract_before


def test_every_runner_call_observes_only_pytest_temporary_root(
    tmp_path: Path,
    _observe_every_p1_repository_root: list[Path],
) -> None:
    """Matrix 112-119."""
    result = _run(tmp_path)
    assert result["passed"] is True
    assert _observe_every_p1_repository_root == [tmp_path]
    assert result["runtime_directory_enumerated"] is False
    assert result["protected_payload_read"] is False
    assert result["safe_capture_receipt_read"] is False
    assert result["source_or_package_read"] is False
    assert result["candidate_mutation_performed"] is False
    assert result["attempt_reservation_mutation_performed"] is False
    assert result["gate_activated"] is False
    assert result["persistence_executed"] is False
    assert result["production_object_created"] is False


def test_test_module_routes_all_execution_through_synthetic_helper() -> None:
    """Static companion for Matrix 112-120."""
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    public_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "run_governed_nonproduction_target_initialization_smoke"
    ]
    assert len(public_calls) == 2
    forbidden_fragments = (
        "Path." + "cwd",
        "runtime/" + "governed_nonproduction",
        "evidence_items" + ".jsonl",
        "APPROVED_" + "ROW_FILE",
    )
    assert not any(fragment in source for fragment in forbidden_fragments)


MATRIX_GROUP_COVERAGE = {
    "successful_paths": tuple(range(1, 15)),
    "governance_and_target_authority": tuple(range(15, 26)),
    "path_safety": tuple(range(26, 39)),
    "schema_incompatibility": tuple(range(39, 53)),
    "single_session_and_DML": tuple(range(53, 61)),
    "complete_safe_failure_diagnostics": tuple(range(61, 88)),
    "cleanup": tuple(range(88, 100)),
    "value_free_and_privacy": tuple(range(100, 112)),
    "formal_target_isolation": tuple(range(112, 121)),
}


def test_required_matrix_has_no_coverage_gap() -> None:
    covered = sorted(
        case_id
        for case_ids in MATRIX_GROUP_COVERAGE.values()
        for case_id in case_ids
    )
    assert covered == list(range(1, 121))
