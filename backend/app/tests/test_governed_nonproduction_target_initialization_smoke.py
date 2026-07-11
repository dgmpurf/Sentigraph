from __future__ import annotations

import ast
import hashlib
import inspect
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import pytest

import app.services.governed_nonproduction_evidence_persistence as persistence
import app.services.governed_nonproduction_target_initialization_smoke as runner_module
from app.services.governed_nonproduction_target_initialization_smoke import (
    ATTEMPT_DDL_SAFE_HASH,
    FAILURE_INJECTION_PHASES,
    FORMAL_EXECUTION_PROFILE,
    FORMAL_EXECUTION_PROFILE_CONTRACT_PROJECTION,
    FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH,
    FORMAL_REPOSITORY_IDENTITY_PROJECTION,
    FORMAL_REPOSITORY_IDENTITY_SAFE_HASH,
    FORMAL_REPOSITORY_IDENTITY_SCHEMA,
    LOCKED_RECEIPT_LOGICAL_LABEL,
    LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH,
    LOCKED_TARGET_IDENTITY_SAFE_HASH,
    LOCKED_TARGET_LOGICAL_LABEL,
    PRIMARY_DDL_SAFE_HASH,
    RESULT_FIELDS,
    RESULT_SCHEMA,
    SAFE_ERROR_CODES,
    SYNTHETIC_EXECUTION_PROFILE,
    run_governed_nonproduction_target_initialization_smoke,
)


EXPECTED_F06_HASH = "4f455eaeef1253f795da3b13b3cb960e5c55349e1858d866178047179b65c214"
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_FORMAL_ORIGIN = "https://github.com/dgmpurf/Sentigraph.git"


def _run(repository_root: Path, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "repository_root": repository_root,
        "expected_target_identity_safe_hash": LOCKED_TARGET_IDENTITY_SAFE_HASH,
        "expected_target_authorization_contract_safe_hash": (
            LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "allow_same_run_empty_target_cleanup": True,
        "enabled": True,
    }
    values.update(overrides)
    return run_governed_nonproduction_target_initialization_smoke(**values)


def _target(root: Path) -> Path:
    return root / Path(LOCKED_TARGET_LOGICAL_LABEL)


def _receipt(root: Path) -> Path:
    return root / Path(LOCKED_RECEIPT_LOGICAL_LABEL)


def _write_formal_git_config(root: Path, content: str | None = None) -> Path:
    git_dir = root / ".git"
    git_dir.mkdir()
    config = git_dir / "config"
    config.write_text(
        content
        if content is not None
        else '[remote "origin"]\n'
        f"\turl = {EXPECTED_FORMAL_ORIGIN}\n",
        encoding="utf-8",
    )
    return config


def _formal_run(repository_root: Path, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "execution_profile": FORMAL_EXECUTION_PROFILE,
        "expected_repository_identity_safe_hash": (
            FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
        ),
        "expected_formal_execution_profile_contract_safe_hash": (
            FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
        ),
        "formal_execution_enabled": True,
    }
    values.update(overrides)
    return _run(repository_root, **values)


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _create_exact_empty_target(root: Path) -> Path:
    target = _target(root)
    target.parent.mkdir(parents=True)
    with sqlite3.connect(target) as connection:
        connection.execute(persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL)
        connection.execute(persistence._CREATE_TABLE_SQL)
        connection.commit()
    return target


def _insert_reservation(target: Path) -> None:
    h = hashlib.sha256(b"synthetic-reservation").hexdigest()
    with sqlite3.connect(target) as connection:
        connection.execute(
            f"""
            INSERT INTO {persistence.ATTEMPT_RESERVATION_TABLE} VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                "synthetic-reservation-001",
                persistence.ATTEMPT_RESERVATION_SCHEMA,
                persistence.ATTEMPT_RESERVATION_VERSION,
                "synthetic-scope-001",
                h,
                h,
                "synthetic-gate-schema-v0-1",
                "0.1",
                h,
                "synthetic-activation-001",
                h,
                persistence.LOGICAL_RUNTIME_TARGET_LABEL,
                persistence.MUTATION_MODE,
                "synthetic-idempotency-001",
                "synthetic-record-001",
                1,
                1,
                "2026-07-12T00:00:00Z",
                h,
            ),
        )
        connection.commit()


def _insert_candidate(target: Path) -> None:
    h = hashlib.sha256(b"synthetic-candidate").hexdigest()
    with sqlite3.connect(target) as connection:
        connection.execute(
            f"""
            INSERT INTO {persistence.TABLE_NAME} VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                "synthetic-record-001",
                persistence.PERSISTED_RECORD_SCHEMA,
                "synthetic-candidate-001",
                h,
                h,
                "synthetic-preview-001",
                h,
                "synthetic-package-001",
                "synthetic-governance-sample",
                "synthetic-case-001",
                "synthetic-fixture",
                persistence.IDENTITY_SCHEMA,
                "0.1",
                persistence.PAYLOAD_SCHEMA,
                persistence.PAYLOAD_VERSION,
                h,
                "{}",
                "{}",
                "{}",
                "synthetic-gate-schema-v0-1",
                "0.1",
                h,
                "synthetic-activation-001",
                h,
                "synthetic-idempotency-001",
                persistence.MUTATION_MODE,
                persistence.INITIAL_STATUS,
                1,
                0,
                "2026-07-12T00:00:00Z",
                None,
                None,
                "synthetic-audit-reference-001",
                0,
                0,
                0,
                0,
                0,
                h,
            ),
        )
        connection.commit()


def _assert_complete_safe_failure(result: dict[str, Any], root: Path) -> None:
    assert set(result) == RESULT_FIELDS
    assert result["result_schema"] == RESULT_SCHEMA
    assert result["passed"] is False
    assert result["decision"] in {"blocked", "needs_fix"}
    assert result["privacy_issue_stop"] is False
    assert result["safe_error_code"] in SAFE_ERROR_CODES
    rendered = json.dumps(result, ensure_ascii=True, sort_keys=True)
    assert str(root) not in rendered
    assert "Traceback" not in rendered
    assert "CREATE TABLE" not in rendered
    assert "INSERT INTO" not in rendered
    assert "UPDATE " not in rendered
    assert "DELETE FROM" not in rendered
    assert re.search(r"[A-Za-z]:[\\/]", rendered) is None


def test_public_contract_and_locked_constants() -> None:
    signature = inspect.signature(
        run_governed_nonproduction_target_initialization_smoke
    )
    assert set(signature.parameters) == {
        "repository_root",
        "expected_target_identity_safe_hash",
        "expected_target_authorization_contract_safe_hash",
        "allow_same_run_empty_target_cleanup",
        "enabled",
        "execution_profile",
        "expected_repository_identity_safe_hash",
        "expected_formal_execution_profile_contract_safe_hash",
        "formal_execution_enabled",
        "_failure_injection_phase",
    }
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    assert signature.parameters["enabled"].default is False
    assert signature.parameters["execution_profile"].default == (
        SYNTHETIC_EXECUTION_PROFILE
    )
    assert signature.parameters["formal_execution_enabled"].default is False
    assert signature.parameters["expected_repository_identity_safe_hash"].default is None
    assert (
        signature.parameters[
            "expected_formal_execution_profile_contract_safe_hash"
        ].default
        is None
    )
    assert RESULT_SCHEMA == (
        "sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_2"
    )
    assert LOCKED_TARGET_LOGICAL_LABEL == (
        "runtime/governed_nonproduction_evidence_persistence/"
        "evidence_records_v0_1.sqlite3"
    )
    assert LOCKED_RECEIPT_LOGICAL_LABEL == (
        "runtime/governed_nonproduction_evidence_persistence/"
        "target-initialization-receipt-"
        "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b.json"
    )
    assert LOCKED_TARGET_IDENTITY_SAFE_HASH == (
        "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b"
    )
    assert LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH == (
        "f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2"
    )
    assert ATTEMPT_DDL_SAFE_HASH == (
        "2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266"
    )
    assert PRIMARY_DDL_SAFE_HASH == (
        "d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26"
    )
    assert FORMAL_REPOSITORY_IDENTITY_SCHEMA == (
        "sentigraph_formal_repository_identity_v0_1"
    )
    assert FORMAL_REPOSITORY_IDENTITY_SAFE_HASH == (
        "66ae70377a33d036ab68729e7b9a6f509c7218cbbc6d40739e1ca5a755a2d82b"
    )
    assert FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH == (
        "5225ff83fd2de19cb32e26b831da410f51a162c32afc40be97d522f87d2137bf"
    )
    assert _sha256_bytes(_canonical(dict(FORMAL_REPOSITORY_IDENTITY_PROJECTION))) == (
        FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
    )
    assert _sha256_bytes(
        _canonical(dict(FORMAL_EXECUTION_PROFILE_CONTRACT_PROJECTION))
    ) == FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
    assert "url" not in FORMAL_REPOSITORY_IDENTITY_PROJECTION
    with pytest.raises(TypeError):
        FORMAL_REPOSITORY_IDENTITY_PROJECTION["project_id"] = "other"  # type: ignore[index]
    with pytest.raises(TypeError):
        FORMAL_EXECUTION_PROFILE_CONTRACT_PROJECTION["execution_profile"] = (  # type: ignore[index]
            SYNTHETIC_EXECUTION_PROFILE
        )


def test_disabled_default_blocks_before_filesystem_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner_module,
        "_derive_exact_paths",
        lambda *_args, **_kwargs: pytest.fail("path access reached"),
    )
    result = run_governed_nonproduction_target_initialization_smoke(
        repository_root=tmp_path,
        expected_target_identity_safe_hash=LOCKED_TARGET_IDENTITY_SAFE_HASH,
        expected_target_authorization_contract_safe_hash=(
            LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        allow_same_run_empty_target_cleanup=True,
    )
    assert result["safe_error_code"] == "runner_disabled"
    assert result["path_derivation_completed"] is False
    assert not tmp_path.joinpath("runtime").exists()


@pytest.mark.parametrize(
    ("field", "wrong_value", "error_code"),
    [
        (
            "expected_target_identity_safe_hash",
            "0" * 64,
            "governance_identity_hash_mismatch",
        ),
        (
            "expected_target_authorization_contract_safe_hash",
            "1" * 64,
            "governance_contract_hash_mismatch",
        ),
    ],
)
def test_governance_mismatch_blocks_before_path_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    wrong_value: str,
    error_code: str,
) -> None:
    monkeypatch.setattr(
        runner_module,
        "_derive_exact_paths",
        lambda *_args, **_kwargs: pytest.fail("path access reached"),
    )
    result = _run(tmp_path, **{field: wrong_value})
    assert result["safe_error_code"] == error_code
    assert result["path_derivation_completed"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_DDL_hash_mismatch_blocks_before_SQLite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner_module,
        "_CREATE_TABLE_SQL",
        runner_module._CREATE_TABLE_SQL + " ",
    )
    monkeypatch.setattr(
        runner_module.sqlite3,
        "connect",
        lambda *_args, **_kwargs: pytest.fail("SQLite reached"),
    )
    result = _run(tmp_path)
    assert result["safe_error_code"] == "DDL_hash_mismatch"
    assert result["DDL_hashes_verified"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_absent_target_initializes_exact_empty_schema_and_safe_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_connect = sqlite3.connect
    calls: list[tuple[Any, ...]] = []

    def counted_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        calls.append(args)
        return original_connect(*args, **kwargs)

    monkeypatch.setattr(runner_module.sqlite3, "connect", counted_connect)
    result = _run(tmp_path)

    assert set(result) == RESULT_FIELDS
    assert result["passed"] is True
    assert result["decision"] == "ready"
    assert result["safe_error_code"] == "none"
    assert result["target_initialization_outcome"] == "initialized_exact_empty_target"
    assert result["target_preexistence_classification"] == "absent"
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["SQLite_create_count"] == 1
    assert result["transaction_begin_count"] == 1
    assert result["schema_DDL_statement_count"] == 2
    assert result["commit_call_count"] == 1
    assert result["successful_initialization_commit"] is True
    assert result["rollback_count"] == 0
    assert result["connection_close_count"] == 1
    assert len(calls) == 1
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert result["other_user_DML_statement_count"] == 0
    assert result["base_record_row_count"] == 0
    assert result["attempt_reservation_row_count"] == 0
    assert result["integrity_result"] == "ok"
    assert result["schema_exact_conformance_verified"] is True
    assert result["unexpected_user_schema_object_count"] == 0
    assert result["final_target_exists"] is True
    assert result["final_receipt_exists"] is True
    assert result["final_sidecar_count"] == 0
    assert result["receipt_privacy_scan_passed"] is True
    assert result["receipt_readback_verified"] is True
    assert HASH_RE.fullmatch(result["receipt_safe_hash"])
    assert HASH_RE.fullmatch(result["receipt_byte_sha256"])

    target = _target(tmp_path)
    receipt = _receipt(tmp_path)
    assert target.is_file()
    assert receipt.is_file()
    with original_connect(target) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
        assert tables == {persistence.ATTEMPT_RESERVATION_TABLE, persistence.TABLE_NAME}
        assert connection.execute(
            f"SELECT COUNT(*) FROM {persistence.TABLE_NAME}"
        ).fetchone()[0] == 0
        assert connection.execute(
            f"SELECT COUNT(*) FROM {persistence.ATTEMPT_RESERVATION_TABLE}"
        ).fetchone()[0] == 0

    receipt_object = json.loads(receipt.read_text(encoding="utf-8"))
    safe_hash = receipt_object.pop("receipt_safe_hash")
    assert safe_hash == _sha256_bytes(_canonical(receipt_object))
    assert result["receipt_byte_sha256"] == _sha256_bytes(receipt.read_bytes())


def test_existing_exact_empty_target_is_read_only_and_byte_stable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = _create_exact_empty_target(tmp_path)
    before = _sha256_bytes(target.read_bytes())
    original_connect = sqlite3.connect
    calls: list[tuple[Any, ...]] = []

    def counted_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        calls.append(args)
        return original_connect(*args, **kwargs)

    monkeypatch.setattr(runner_module.sqlite3, "connect", counted_connect)
    result = _run(tmp_path)
    after = _sha256_bytes(target.read_bytes())

    assert result["passed"] is True
    assert result["target_initialization_outcome"] == (
        "verified_existing_exact_empty_target_read_only"
    )
    assert result["target_preexistence_classification"] == "existing_regular_file"
    assert result["existing_target_read_only"] is True
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["SQLite_create_count"] == 0
    assert result["transaction_begin_count"] == 0
    assert result["schema_DDL_statement_count"] == 0
    assert result["commit_call_count"] == 0
    assert result["read_only_verification_completed"] is True
    assert before == after
    assert result["existing_target_bytes_unchanged"] is True
    assert len(calls) == 1


def test_receipt_preexistence_and_exact_collisions_fail_closed(tmp_path: Path) -> None:
    receipt = _receipt(tmp_path)
    receipt.parent.mkdir(parents=True)
    receipt.write_text("synthetic collision", encoding="utf-8")
    result = _run(tmp_path)
    assert result["safe_error_code"] == "receipt_preexistence"
    assert result["SQLite_connection_open_count"] == 0
    assert receipt.read_text(encoding="utf-8") == "synthetic collision"

    second_root = tmp_path / "target-directory"
    target = _target(second_root)
    target.mkdir(parents=True)
    result = _run(second_root)
    assert result["safe_error_code"] == "unsafe_target_collision"
    assert result["SQLite_connection_open_count"] == 0

    third_root = tmp_path / "sidecar"
    target = _target(third_root)
    target.parent.mkdir(parents=True)
    Path(str(target) + "-wal").write_bytes(b"synthetic")
    result = _run(third_root)
    assert result["safe_error_code"] == "ambiguous_sidecar"
    assert result["SQLite_connection_open_count"] == 0


def test_symlink_or_reparse_component_blocks_without_target_access(
    tmp_path: Path,
) -> None:
    external = tmp_path / "external"
    external.mkdir()
    runtime = tmp_path / "runtime"
    try:
        runtime.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable")
    result = _run(tmp_path)
    assert result["safe_error_code"] == "symlink_or_reparse_point"
    assert result["SQLite_connection_open_count"] == 0
    assert not _target(tmp_path).exists()


def test_repository_root_with_git_marker_is_rejected(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    result = _run(tmp_path)
    assert result["safe_error_code"] == "unsafe_repository_root"
    assert result["SQLite_connection_open_count"] == 0


def test_synthetic_profile_remains_default_and_environment_cannot_upgrade_it(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "SENTIGRAPH_INITIALIZATION_EXECUTION_PROFILE",
        FORMAL_EXECUTION_PROFILE,
    )

    result = _run(tmp_path)

    assert result["passed"] is True
    assert result["execution_profile_requested"] == SYNTHETIC_EXECUTION_PROFILE
    assert result["execution_profile_effective"] == SYNTHETIC_EXECUTION_PROFILE
    assert result["synthetic_profile_selected"] is True
    assert result["formal_profile_selected"] is False
    assert result["formal_execution_enabled"] is False
    assert result["environment_target_override_used"] is False


@pytest.mark.parametrize("invalid_profile", ["formal", "", None, 7])
def test_unknown_or_invalid_profile_blocks_before_path_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    invalid_profile: Any,
) -> None:
    monkeypatch.setattr(
        runner_module,
        "_derive_exact_paths",
        lambda *_args, **_kwargs: pytest.fail("path access reached"),
    )

    result = _run(tmp_path, execution_profile=invalid_profile)

    assert result["safe_error_code"] == "invalid_execution_profile"
    assert result["execution_profile_requested"] == "invalid"
    assert result["path_derivation_completed"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_formal_profile_disabled_blocks_before_git_config_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda *_args, **_kwargs: pytest.fail("git config read reached"),
    )

    result = _formal_run(tmp_path, formal_execution_enabled=False)

    assert result["safe_error_code"] == "formal_execution_disabled"
    assert result["git_config_check_started"] is False
    assert result["formal_target_path_derivation_started"] is False
    assert result["SQLite_connection_open_count"] == 0


@pytest.mark.parametrize(
    ("field", "value", "error_code"),
    [
        (
            "expected_repository_identity_safe_hash",
            None,
            "formal_repository_identity_hash_mismatch",
        ),
        (
            "expected_repository_identity_safe_hash",
            "0" * 64,
            "formal_repository_identity_hash_mismatch",
        ),
        (
            "expected_formal_execution_profile_contract_safe_hash",
            None,
            "formal_profile_contract_hash_mismatch",
        ),
        (
            "expected_formal_execution_profile_contract_safe_hash",
            "1" * 64,
            "formal_profile_contract_hash_mismatch",
        ),
    ],
)
def test_formal_profile_binding_mismatch_blocks_before_config_and_target(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    value: Any,
    error_code: str,
) -> None:
    _write_formal_git_config(tmp_path)
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda *_args, **_kwargs: pytest.fail("git config read reached"),
    )
    monkeypatch.setattr(
        runner_module,
        "_derive_exact_paths",
        lambda *_args, **_kwargs: pytest.fail("target derivation reached"),
    )

    result = _formal_run(tmp_path, **{field: value})

    assert result["safe_error_code"] == error_code
    assert result["formal_execution_guard_verified"] is False
    assert result["git_marker_check_started"] is False
    assert result["path_derivation_completed"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_profile_inputs_are_not_mutated(tmp_path: Path) -> None:
    _write_formal_git_config(tmp_path)
    inputs: dict[str, Any] = {
        "execution_profile": FORMAL_EXECUTION_PROFILE,
        "expected_repository_identity_safe_hash": (
            FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
        ),
        "expected_formal_execution_profile_contract_safe_hash": (
            FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
        ),
        "formal_execution_enabled": True,
    }
    before = dict(inputs)

    result = _run(tmp_path, **inputs)

    assert result["passed"] is True
    assert inputs == before


def test_formal_profile_missing_git_marker_blocks(tmp_path: Path) -> None:
    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_marker_invalid"
    assert result["formal_repository_identity_check_completed"] is True
    assert result["formal_repository_identity_check_passed"] is False
    assert result["path_derivation_completed"] is False


def test_formal_profile_git_marker_file_or_gitdir_pointer_blocks(
    tmp_path: Path,
) -> None:
    (tmp_path / ".git").write_text(
        "gitdir: synthetic-external-git-dir",
        encoding="utf-8",
    )

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_marker_invalid"
    assert result["git_marker_verified"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_formal_profile_git_marker_symlink_blocks(tmp_path: Path) -> None:
    external = tmp_path / "synthetic-git-directory"
    external.mkdir()
    try:
        (tmp_path / ".git").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation is unavailable")

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_marker_invalid"
    assert result["path_derivation_completed"] is False


def test_formal_profile_git_marker_reparse_classification_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    original_path_state = runner_module._path_state

    def classify_git_as_reparse(path: Path) -> str:
        if path == tmp_path / ".git":
            return "reparse"
        return original_path_state(path)

    monkeypatch.setattr(runner_module, "_path_state", classify_git_as_reparse)
    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_marker_invalid"
    assert result["git_config_check_started"] is False


def test_formal_profile_missing_git_config_blocks(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_config_invalid"
    assert result["git_marker_verified"] is True
    assert result["git_config_verified"] is False


def test_formal_profile_git_config_directory_blocks(tmp_path: Path) -> None:
    (tmp_path / ".git" / "config").mkdir(parents=True)

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_config_invalid"
    assert result["origin_remote_check_started"] is False


def test_formal_profile_git_config_symlink_blocks(tmp_path: Path) -> None:
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    external = tmp_path / "synthetic-config"
    external.write_text(
        f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n',
        encoding="utf-8",
    )
    try:
        (git_dir / "config").symlink_to(external)
    except OSError:
        pytest.skip("symlink creation is unavailable")

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_config_invalid"
    assert result["git_config_verified"] is False


def test_formal_profile_git_config_reparse_classification_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _write_formal_git_config(tmp_path)
    original_path_state = runner_module._path_state

    def classify_config_as_reparse(path: Path) -> str:
        if path == config:
            return "reparse"
        return original_path_state(path)

    monkeypatch.setattr(runner_module, "_path_state", classify_config_as_reparse)
    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_git_config_invalid"
    assert result["origin_remote_check_started"] is False


@pytest.mark.parametrize(
    ("config_text", "error_code"),
    [
        ("[core]\n\trepositoryformatversion = 0\n", "formal_origin_remote_invalid"),
        (
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n'
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n',
            "formal_git_config_invalid",
        ),
        (
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n'
            f"\turl = {EXPECTED_FORMAL_ORIGIN}\n",
            "formal_git_config_invalid",
        ),
        (
            '[remote "origin"]\n'
            "\turl = https://github.com/synthetic-owner/Sentigraph.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n'
            "\turl = https://github.com/dgmpurf/Synthetic.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n'
            "\turl = https://github.com/dgmpurf/sentigraph.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n'
            "\turl = git@github.com:dgmpurf/Sentigraph.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n\turl = C:/synthetic/Sentigraph.git\n',
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n\turl = file:///synthetic/Sentigraph.git\n',
            "formal_origin_remote_invalid",
        ),
        (
            '[remote "origin"]\n'
            "\turl = https://synthetic-user:synthetic-secret@github.com/"
            "dgmpurf/Sentigraph.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}?synthetic=1\n',
            "formal_origin_remote_invalid",
        ),
        (
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}#synthetic\n',
            "formal_origin_remote_invalid",
        ),
        (
            f'[remote "origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n'
            "\tpushurl = https://github.com/dgmpurf/Sentigraph.git\n",
            "formal_origin_remote_invalid",
        ),
        (
            f'[remote "Origin"]\n\turl = {EXPECTED_FORMAL_ORIGIN}\n',
            "formal_origin_remote_invalid",
        ),
    ],
)
def test_formal_profile_rejects_nonexact_or_ambiguous_origin_identity(
    tmp_path: Path,
    config_text: str,
    error_code: str,
) -> None:
    _write_formal_git_config(tmp_path, config_text)

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == error_code
    assert result["formal_repository_identity_check_completed"] is True
    assert result["formal_repository_identity_check_passed"] is False
    assert result["generic_git_repository_accepted"] is False
    assert result["raw_origin_remote_exposed"] is False
    assert result["formal_target_path_derivation_started"] is False
    assert result["SQLite_connection_open_count"] == 0
    rendered = json.dumps(result, ensure_ascii=True, sort_keys=True)
    assert config_text not in rendered
    assert "synthetic-secret" not in rendered


def test_exact_temporary_formal_fixture_initializes_absent_target_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    original_connect = sqlite3.connect
    calls: list[tuple[Any, ...]] = []

    def counted_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        calls.append(args)
        return original_connect(*args, **kwargs)

    monkeypatch.setattr(runner_module.sqlite3, "connect", counted_connect)
    result = _formal_run(tmp_path)

    assert result["passed"] is True
    assert result["execution_profile_requested"] == FORMAL_EXECUTION_PROFILE
    assert result["execution_profile_effective"] == FORMAL_EXECUTION_PROFILE
    assert result["formal_profile_selected"] is True
    assert result["synthetic_profile_selected"] is False
    assert result["formal_execution_enabled"] is True
    assert result["formal_execution_guard_verified"] is True
    assert result["repository_identity_safe_hash_verified"] is True
    assert result["formal_profile_contract_safe_hash_verified"] is True
    assert result["git_marker_verified"] is True
    assert result["git_config_verified"] is True
    assert result["origin_remote_verified"] is True
    assert result["formal_repository_identity_check_completed"] is True
    assert result["formal_repository_identity_check_passed"] is True
    assert result["formal_target_path_derivation_authorized"] is True
    assert result["formal_target_path_derivation_started"] is True
    assert result["target_initialization_outcome"] == "initialized_exact_empty_target"
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert len(calls) == 1
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert result["other_user_DML_statement_count"] == 0
    assert result["receipt_privacy_scan_passed"] is True
    assert result["generic_git_repository_accepted"] is False
    assert result["raw_origin_remote_exposed"] is False
    assert _target(tmp_path).is_file()
    assert _receipt(tmp_path).is_file()
    rendered = json.dumps(result, ensure_ascii=True, sort_keys=True)
    assert EXPECTED_FORMAL_ORIGIN not in rendered


def test_exact_temporary_formal_fixture_verifies_existing_target_read_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    target = _create_exact_empty_target(tmp_path)
    before = _sha256_bytes(target.read_bytes())
    original_connect = sqlite3.connect
    calls: list[tuple[Any, ...]] = []

    def counted_connect(*args: Any, **kwargs: Any) -> sqlite3.Connection:
        calls.append(args)
        return original_connect(*args, **kwargs)

    monkeypatch.setattr(runner_module.sqlite3, "connect", counted_connect)
    result = _formal_run(tmp_path)
    after = _sha256_bytes(target.read_bytes())

    assert result["passed"] is True
    assert result["target_initialization_outcome"] == (
        "verified_existing_exact_empty_target_read_only"
    )
    assert result["existing_target_read_only"] is True
    assert result["existing_target_bytes_unchanged"] is True
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert len(calls) == 1
    assert before == after
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert result["other_user_DML_statement_count"] == 0


def test_formal_failure_diagnostics_are_complete_and_value_free(tmp_path: Path) -> None:
    unsafe_origin = (
        '[remote "origin"]\n'
        "\turl = https://synthetic-user:synthetic-secret@github.com/"
        "dgmpurf/Sentigraph.git\n"
    )
    _write_formal_git_config(tmp_path, unsafe_origin)

    result = _formal_run(tmp_path)

    _assert_complete_safe_failure(result, tmp_path)
    assert result["safe_error_code"] == "formal_origin_remote_invalid"
    rendered = json.dumps(result, ensure_ascii=True, sort_keys=True)
    assert "synthetic-user" not in rendered
    assert "synthetic-secret" not in rendered
    assert EXPECTED_FORMAL_ORIGIN not in rendered


def test_formal_identity_completes_before_target_derivation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    events: list[str] = []
    original_identity = runner_module._verify_formal_repository_identity
    original_derive = runner_module._derive_exact_paths

    def verified_identity(root: Path, result: dict[str, Any]) -> None:
        original_identity(root, result)
        events.append("identity")

    def derived_paths(root: Path) -> dict[str, Path]:
        assert events == ["identity"]
        events.append("derive")
        return original_derive(root)

    monkeypatch.setattr(
        runner_module,
        "_verify_formal_repository_identity",
        verified_identity,
    )
    monkeypatch.setattr(runner_module, "_derive_exact_paths", derived_paths)
    result = _formal_run(tmp_path)

    assert result["passed"] is True
    assert events == ["identity", "derive"]


def test_wrong_origin_blocks_before_target_derivation_and_SQLite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(
        tmp_path,
        '[remote "origin"]\n'
        "\turl = https://github.com/synthetic-owner/Sentigraph.git\n",
    )
    monkeypatch.setattr(
        runner_module,
        "_derive_exact_paths",
        lambda *_args, **_kwargs: pytest.fail("target derivation reached"),
    )
    monkeypatch.setattr(
        runner_module.sqlite3,
        "connect",
        lambda *_args, **_kwargs: pytest.fail("SQLite reached"),
    )

    result = _formal_run(tmp_path)

    assert result["safe_error_code"] == "formal_origin_remote_invalid"
    assert result["formal_target_path_derivation_started"] is False
    assert result["path_derivation_completed"] is False
    assert result["SQLite_connection_open_count"] == 0


def test_formal_contract_mismatch_blocks_before_git_config_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda *_args, **_kwargs: pytest.fail("git config read reached"),
    )

    result = _formal_run(
        tmp_path,
        expected_formal_execution_profile_contract_safe_hash="2" * 64,
    )

    assert result["safe_error_code"] == "formal_profile_contract_hash_mismatch"
    assert result["git_marker_check_started"] is False
    assert result["formal_target_path_derivation_started"] is False


def test_collision_checks_begin_only_after_formal_identity_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_formal_git_config(tmp_path)
    original_collisions = runner_module._verify_exact_collisions
    observations: list[bool] = []

    def checked_collisions(
        paths: dict[str, Path],
        result: dict[str, Any],
    ) -> tuple[str, str, dict[str, str]]:
        observations.append(result["formal_repository_identity_check_passed"])
        return original_collisions(paths, result)

    monkeypatch.setattr(
        runner_module,
        "_verify_exact_collisions",
        checked_collisions,
    )
    result = _formal_run(tmp_path)

    assert result["passed"] is True
    assert observations == [True]


def test_formal_fixture_all_path_and_config_access_stays_under_tmp_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _write_formal_git_config(tmp_path)
    original_path_state = runner_module._path_state
    original_read_text = Path.read_text
    observed_paths: list[Path] = []
    observed_reads: list[Path] = []

    def bounded_path_state(path: Path) -> str:
        observed_paths.append(path)
        assert path == tmp_path or tmp_path in path.parents
        return original_path_state(path)

    def bounded_read_text(path: Path, *args: Any, **kwargs: Any) -> str:
        observed_reads.append(path)
        assert path == config
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(runner_module, "_path_state", bounded_path_state)
    monkeypatch.setattr(Path, "read_text", bounded_read_text)
    result = _formal_run(tmp_path)

    assert result["passed"] is True
    assert observed_paths
    assert observed_reads == [config]
    assert result["actual_Git_root_passed_to_runner"] is False
    assert result["actual_runtime_enumerated"] is False
    assert result["formal_logical_target_accessed"] is False
    assert result["formal_initialization_receipt_accessed"] is False


@pytest.mark.parametrize(
    "mutation",
    ["missing_table", "extra_table", "extra_index", "extra_trigger", "extra_view"],
)
def test_existing_schema_mismatch_fails_closed(tmp_path: Path, mutation: str) -> None:
    target = _target(tmp_path)
    target.parent.mkdir(parents=True)
    with sqlite3.connect(target) as connection:
        connection.execute(persistence._CREATE_ATTEMPT_RESERVATION_TABLE_SQL)
        if mutation != "missing_table":
            connection.execute(persistence._CREATE_TABLE_SQL)
        if mutation == "extra_table":
            connection.execute("CREATE TABLE synthetic_extra_table (id TEXT)")
        elif mutation == "extra_index":
            connection.execute(
                f"CREATE INDEX synthetic_extra_index ON {persistence.TABLE_NAME}(candidate_id)"
            )
        elif mutation == "extra_trigger":
            connection.execute(
                f"""
                CREATE TRIGGER synthetic_extra_trigger
                AFTER INSERT ON {persistence.TABLE_NAME}
                BEGIN SELECT 1; END
                """
            )
        elif mutation == "extra_view":
            connection.execute(
                f"CREATE VIEW synthetic_extra_view AS SELECT candidate_id FROM {persistence.TABLE_NAME}"
            )
        connection.commit()
    before = _sha256_bytes(target.read_bytes())
    result = _run(tmp_path)
    assert result["safe_error_code"] in {
        "schema_verification_failed",
        "unexpected_schema_object",
    }
    assert result["passed"] is False
    assert _sha256_bytes(target.read_bytes()) == before
    assert result["cleanup_performed"] is False


@pytest.mark.parametrize(
    ("row_kind", "expected_error"),
    [
        ("candidate", "nonzero_candidate_rows"),
        ("reservation", "nonzero_reservations"),
    ],
)
def test_existing_nonzero_rows_fail_closed(
    tmp_path: Path,
    row_kind: str,
    expected_error: str,
) -> None:
    target = _create_exact_empty_target(tmp_path)
    if row_kind == "candidate":
        _insert_candidate(target)
    else:
        _insert_reservation(target)
    before = _sha256_bytes(target.read_bytes())
    result = _run(tmp_path)
    assert result["safe_error_code"] == expected_error
    assert result["passed"] is False
    assert result["cleanup_performed"] is False
    assert _sha256_bytes(target.read_bytes()) == before


def test_known_commit_failure_rolls_back_and_cleans_same_run_target(tmp_path: Path) -> None:
    result = _run(tmp_path, _failure_injection_phase="commit_known_failure")
    _assert_complete_safe_failure(result, tmp_path)
    assert result["safe_error_code"] == "known_commit_failure"
    assert result["commit_outcome_ambiguous"] is False
    assert result["rollback_count"] == 1
    assert result["cleanup_eligible"] is True
    assert result["cleanup_performed"] is True
    assert result["final_target_exists"] is False
    assert result["final_receipt_exists"] is False


def test_ambiguous_commit_never_retries_and_preserves_target(tmp_path: Path) -> None:
    result = _run(tmp_path, _failure_injection_phase="commit_ambiguity")
    _assert_complete_safe_failure(result, tmp_path)
    assert result["safe_error_code"] == "commit_ambiguity"
    assert result["commit_call_count"] == 1
    assert result["commit_outcome_ambiguous"] is True
    assert result["automatic_retry"] is False
    assert result["second_attempt"] is False
    assert result["SQLite_connection_open_count"] == 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["cleanup_eligible"] is False
    assert result["cleanup_performed"] is False
    assert result["final_target_exists"] is True


def test_cleanup_can_be_disabled_without_deleting_same_run_target(tmp_path: Path) -> None:
    result = _run(
        tmp_path,
        allow_same_run_empty_target_cleanup=False,
        _failure_injection_phase="initialize_primary_schema",
    )
    _assert_complete_safe_failure(result, tmp_path)
    assert result["cleanup_allowed_by_caller"] is False
    assert result["cleanup_eligible"] is False
    assert result["cleanup_performed"] is False
    assert result["final_target_exists"] is True


def test_cleanup_diagnostic_failure_is_still_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        runner_module,
        "_refresh_exact_final_state",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(OSError("synthetic")),
    )
    result = _run(
        tmp_path,
        _failure_injection_phase="initialize_attempt_schema",
    )
    _assert_complete_safe_failure(result, tmp_path)
    assert result["safe_error_code"] == "cleanup_failure"


@pytest.mark.parametrize("phase", sorted(FAILURE_INJECTION_PHASES))
def test_every_controlled_failure_returns_complete_value_free_state(
    tmp_path: Path,
    phase: str,
) -> None:
    root = tmp_path / hashlib.sha256(phase.encode("utf-8")).hexdigest()[:12]
    root.mkdir()
    result = _run(root, _failure_injection_phase=phase)
    _assert_complete_safe_failure(result, root)
    assert result["terminal_phase"] == "terminal_failure"
    assert result["automatic_retry"] is False
    assert result["second_attempt"] is False
    assert result["SQLite_connection_open_count"] <= 1
    assert result["SQLite_connection_reopen_count"] == 0
    assert result["candidate_table_DML_statement_count"] == 0
    assert result["attempt_table_DML_statement_count"] == 0
    assert result["other_user_DML_statement_count"] == 0
    assert result["candidate_writer_called"] is False
    assert result["reservation_writer_called"] is False
    assert result["actual_runtime_enumerated"] is False
    assert result["formal_logical_target_accessed"] is False


def test_invalid_failure_injection_label_blocks_before_path_access(tmp_path: Path) -> None:
    result = _run(tmp_path, _failure_injection_phase="not-a-phase")
    assert result["safe_error_code"] == "invalid_input"
    assert result["path_derivation_completed"] is False


def test_required_formal_result_fields_exist_on_early_failure(tmp_path: Path) -> None:
    result = _formal_run(tmp_path, formal_execution_enabled=False)
    required_fields = {
        "execution_profile_requested",
        "execution_profile_effective",
        "synthetic_profile_selected",
        "formal_profile_selected",
        "formal_execution_enabled",
        "formal_execution_guard_verified",
        "repository_identity_schema",
        "repository_identity_safe_hash_expected",
        "repository_identity_safe_hash_verified",
        "formal_profile_contract_safe_hash_expected",
        "formal_profile_contract_safe_hash_verified",
        "git_marker_check_started",
        "git_marker_verified",
        "git_config_check_started",
        "git_config_verified",
        "origin_remote_check_started",
        "origin_remote_verified",
        "formal_repository_identity_check_completed",
        "formal_repository_identity_check_passed",
        "generic_git_repository_accepted",
        "raw_origin_remote_exposed",
        "formal_target_path_derivation_authorized",
        "formal_target_path_derivation_started",
    }

    assert set(result) == RESULT_FIELDS
    assert required_fields <= set(result)
    assert result["execution_profile_requested"] == FORMAL_EXECUTION_PROFILE
    assert result["execution_profile_effective"] == FORMAL_EXECUTION_PROFILE
    assert result["formal_profile_selected"] is True
    assert result["formal_execution_guard_verified"] is False


def test_static_import_and_API_boundary_has_no_overreach() -> None:
    source = inspect.getsource(runner_module)
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    forbidden_import_fragments = {
        "requests",
        "httpx",
        "urllib",
        "subprocess",
        "evidence_import",
        "evidence_ingestion",
        "case_repository",
    }
    assert not any(
        fragment in name
        for fragment in forbidden_import_fragments
        for name in imported
    )
    forbidden_source_fragments = {
        "os.environ",
        "os.getenv",
        ".iterdir(",
        ".glob(",
        ".rglob(",
        "listdir(",
        "scandir(",
        "os.walk(",
        "create_governed_nonproduction_evidence_record",
        "_reserve_mutating_attempt",
        "CaseRepository",
        "LocalJsonCaseStore",
        "MongoDbCaseStore",
        "target_path=",
        "receipt_path=",
        "remote_url=",
        "origin_url=",
    }
    assert not any(fragment in source for fragment in forbidden_source_fragments)
    assert "Quantitative Trading" not in source
    assert "e33443cf5fd2410eaf1444f9455262a3814f4516" not in source
    assert "subprocess.run" not in source
    assert "subprocess.Popen" not in source


def test_historical_F06_report_remains_byte_exact() -> None:
    report = (
        Path(__file__).resolve().parents[3]
        / "docs"
        / "health"
        / "sentigraph_mvp_f06_exact_logical_target_initialization_smoke_report_v1_0.md"
    )
    assert report.is_file()
    assert _sha256_bytes(report.read_bytes()) == EXPECTED_F06_HASH
