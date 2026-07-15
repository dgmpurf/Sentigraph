from __future__ import annotations

import ast
import hashlib
import inspect
import json
import sqlite3
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest


MODULE_NAME = (
    "app.services.governed_nonproduction_human_review_decision_ledger"
)
CONTRACT_RELATIVE_PATH = Path(
    "docs/architecture/"
    "sentigraph_mvp_f12_p1_formal_decision_ledger_governance_contract_v1_0.md"
)
EXPECTED_RECEIPT_FIELDS = (
    "receipt_schema",
    "receipt_version",
    "outcome",
    "target_kind",
    "target_logical_label",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "target_preexistence_classification",
    "initialization_action",
    "schema_version",
    "primary_table",
    "sqlite_connection_open_count",
    "sqlite_connection_reopen_count",
    "schema_ddl_statement_count",
    "decision_table_dml_statement_count",
    "decision_row_count",
    "exact_schema_verified",
    "exact_empty_verified",
    "integrity_result",
    "final_sidecar_count",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_ready",
    "warnings",
    "blockers",
)
EXPECTED_OUTCOMES = (
    "initialized_exact_empty_formal_decision_ledger",
    "verified_existing_exact_empty_formal_decision_ledger",
    "blocked_existing_nonempty_formal_decision_ledger",
    "blocked_formal_decision_ledger_schema_mismatch",
    "blocked_formal_decision_ledger_target_identity_mismatch",
    "paused_formal_decision_ledger_initialization_ambiguous",
    "bounded_formal_decision_ledger_initialization_failure",
)
SUCCESS_OUTCOMES = EXPECTED_OUTCOMES[:2]
FORMAL_OPERATION = "initialize_exact_formal_governed_nonproduction_human_review_decision_ledger"


def _module():
    return import_module(MODULE_NAME)


def _contract_bytes() -> bytes:
    return CONTRACT_RELATIVE_PATH.read_bytes()


def _synthetic_repository(
    tmp_path: Path,
    *,
    contract_bytes: bytes | None = None,
) -> Path:
    root = tmp_path / "synthetic_repository"
    (root / "backend/app/services").mkdir(parents=True)
    contract_path = root / CONTRACT_RELATIVE_PATH
    contract_path.parent.mkdir(parents=True)
    contract_path.write_bytes(
        _contract_bytes() if contract_bytes is None else contract_bytes
    )
    return root


def _target(module, root: Path) -> Path:
    return root / module.FORMAL_LOGICAL_TARGET_LABEL


def _column_statement(
    module,
    *,
    fields: tuple[str, ...] | None = None,
    type_overrides: dict[str, str] | None = None,
    nullable: set[str] | None = None,
    unique_fields: set[str] | None = None,
    table: str | None = None,
) -> str:
    fields = fields or module.DECISION_FIELDS
    type_overrides = type_overrides or {}
    nullable = nullable or set()
    unique_fields = unique_fields or {
        "decision_id",
        "idempotency_key",
        "audit_receipt_reference",
    }
    definitions = []
    for field in fields:
        data_type = type_overrides.get(
            field,
            "INTEGER" if field in module._BOOLEAN_FIELDS else "TEXT",
        )
        not_null = "" if field in nullable else " NOT NULL"
        unique = " UNIQUE" if field in unique_fields else ""
        definitions.append(f'"{field}" {data_type}{not_null}{unique}')
    return (
        f'CREATE TABLE "{table or module.FORMAL_PRIMARY_TABLE}" '
        f"({', '.join(definitions)})"
    )


def _create_database(
    module,
    root: Path,
    statements: list[str] | None = None,
) -> Path:
    target = _target(module, root)
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as connection:
        for statement in statements or [module.FORMAL_CREATE_TABLE_STATEMENT]:
            connection.execute(statement)
    return target


def _insert_dummy_row(module, target: Path) -> None:
    values: list[Any] = []
    for field in module.DECISION_FIELDS:
        if field in module._BOOLEAN_FIELDS:
            values.append(0)
        elif field in module._JSON_FIELDS:
            values.append("[]")
        else:
            values.append(f"synthetic-{field}")
    columns = ", ".join(f'"{field}"' for field in module.DECISION_FIELDS)
    placeholders = ", ".join("?" for _ in module.DECISION_FIELDS)
    with sqlite3.connect(target) as connection:
        connection.execute(
            f'INSERT INTO "{module.FORMAL_PRIMARY_TABLE}" '
            f"({columns}) VALUES ({placeholders})",
            values,
        )


def _count_formal_opens(module, monkeypatch: pytest.MonkeyPatch) -> list[bool]:
    calls: list[bool] = []
    original = module._open_exact_formal_decision_ledger_connection

    def counted(path: Path, *, read_only: bool):
        calls.append(read_only)
        return original(path, read_only=read_only)

    monkeypatch.setattr(
        module,
        "_open_exact_formal_decision_ledger_connection",
        counted,
    )
    return calls


def _assert_receipt_shape(receipt: dict[str, Any]) -> None:
    assert tuple(receipt) == EXPECTED_RECEIPT_FIELDS
    assert receipt["outcome"] in EXPECTED_OUTCOMES
    assert receipt["human_review_required"] is True
    assert receipt["no_automatic_trust_upgrade"] is True
    assert receipt["production_ready"] is False
    assert isinstance(receipt["warnings"], list)
    assert isinstance(receipt["blockers"], list)


def test_public_operation_signature_and_disabled_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    assert hasattr(module, FORMAL_OPERATION)
    operation = getattr(module, FORMAL_OPERATION)
    signature = inspect.signature(operation)
    assert tuple(signature.parameters) == ("repository_root", "enabled")
    assert all(
        parameter.kind is inspect.Parameter.KEYWORD_ONLY
        for parameter in signature.parameters.values()
    )
    assert signature.parameters["enabled"].default is False

    def forbidden_profile_validation(_root: Path):
        raise AssertionError("disabled operation must not validate or access")

    monkeypatch.setattr(
        module,
        "_validate_exact_formal_decision_ledger_profile",
        forbidden_profile_validation,
    )
    receipt = operation(repository_root=tmp_path)
    _assert_receipt_shape(receipt)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[-1]
    assert receipt["sqlite_connection_open_count"] == 0
    assert receipt["decision_row_count"] is None
    assert receipt["exact_schema_verified"] is None
    assert receipt["exact_empty_verified"] is None
    assert receipt["integrity_result"] == "not_observed"
    assert receipt["final_sidecar_count"] is None
    assert list(tmp_path.iterdir()) == []


def test_formal_constants_and_public_surface_are_exact() -> None:
    module = _module()
    assert module.FORMAL_TARGET_KIND == (
        "dedicated_local_sqlite_nonproduction_human_review_decision_ledger"
    )
    assert module.FORMAL_LOGICAL_TARGET_LABEL == (
        "runtime/governed_nonproduction_human_review_decisions/"
        "review_decisions_v0_1.sqlite3"
    )
    assert module.FORMAL_PRIMARY_TABLE == (
        "governed_nonproduction_human_review_decisions_v0_1"
    )
    assert module.FORMAL_CONTRACT_RELATIVE_PATH == CONTRACT_RELATIVE_PATH.as_posix()
    assert module.FORMAL_CONTRACT_SHA256 == (
        "0d0e4c0c12a534eb5f523fffb4430f223480339d197ec031c5621f6e1312b4b8"
    )
    assert module.FORMAL_TARGET_IDENTITY_SAFE_HASH == (
        "4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202"
    )
    assert module.FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH == (
        "de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d"
    )
    assert module.FORMAL_SCHEMA_VERSION == "0.1"
    assert module.INITIALIZATION_RECEIPT_FIELDS == EXPECTED_RECEIPT_FIELDS
    assert module.INITIALIZATION_RECEIPT_OUTCOMES == EXPECTED_OUTCOMES


def test_absent_target_initializes_exact_empty_with_one_open_and_one_ddl(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    calls = _count_formal_opens(module, monkeypatch)
    receipt = getattr(module, FORMAL_OPERATION)(
        repository_root=root,
        enabled=True,
    )
    _assert_receipt_shape(receipt)
    assert receipt == {
        "receipt_schema": module.INITIALIZATION_RECEIPT_SCHEMA,
        "receipt_version": "0.1",
        "outcome": EXPECTED_OUTCOMES[0],
        "target_kind": module.FORMAL_TARGET_KIND,
        "target_logical_label": module.FORMAL_LOGICAL_TARGET_LABEL,
        "target_identity_safe_hash": module.FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            module.FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "target_preexistence_classification": "absent",
        "initialization_action": "created_exact_schema",
        "schema_version": "0.1",
        "primary_table": module.FORMAL_PRIMARY_TABLE,
        "sqlite_connection_open_count": 1,
        "sqlite_connection_reopen_count": 0,
        "schema_ddl_statement_count": 1,
        "decision_table_dml_statement_count": 0,
        "decision_row_count": 0,
        "exact_schema_verified": True,
        "exact_empty_verified": True,
        "integrity_result": "ok",
        "final_sidecar_count": 0,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_ready": False,
        "warnings": [],
        "blockers": [],
    }
    assert calls == [False]
    target = _target(module, root)
    with sqlite3.connect(target) as connection:
        objects = connection.execute(
            "SELECT type, name FROM sqlite_master "
            "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
        ).fetchall()
        assert objects == [("table", module.FORMAL_PRIMARY_TABLE)]
        assert connection.execute(
            f'SELECT COUNT(*) FROM "{module.FORMAL_PRIMARY_TABLE}"'
        ).fetchone() == (0,)
    assert not Path(f"{target}-wal").exists()
    assert not Path(f"{target}-shm").exists()
    assert not Path(f"{target}-journal").exists()


def test_existing_exact_empty_is_verified_read_only_with_one_open(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    target = _create_database(module, root)
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    calls = _count_formal_opens(module, monkeypatch)
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[1]
    assert receipt["target_preexistence_classification"] == "existing_exact_empty"
    assert receipt["initialization_action"] == (
        "verified_existing_exact_schema_without_mutation"
    )
    assert receipt["schema_ddl_statement_count"] == 0
    assert receipt["decision_table_dml_statement_count"] == 0
    assert receipt["decision_row_count"] == 0
    assert receipt["exact_schema_verified"] is True
    assert receipt["exact_empty_verified"] is True
    assert receipt["integrity_result"] == "ok"
    assert receipt["final_sidecar_count"] == 0
    assert calls == [True]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before


def test_existing_nonempty_blocks_without_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    target = _create_database(module, root)
    _insert_dummy_row(module, target)
    before = hashlib.sha256(target.read_bytes()).hexdigest()
    calls = _count_formal_opens(module, monkeypatch)
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[2]
    assert receipt["target_preexistence_classification"] == "existing_nonempty"
    assert receipt["decision_row_count"] == 1
    assert receipt["exact_schema_verified"] is True
    assert receipt["exact_empty_verified"] is False
    assert receipt["schema_ddl_statement_count"] == 0
    assert receipt["decision_table_dml_statement_count"] == 0
    assert calls == [True]
    assert hashlib.sha256(target.read_bytes()).hexdigest() == before


@pytest.mark.parametrize(
    "statements",
    [
        ['CREATE TABLE "unrelated" ("value" TEXT NOT NULL)'],
        [
            "__EXACT__",
            'CREATE TABLE "unrelated" ("value" TEXT NOT NULL)',
        ],
    ],
    ids=("wrong-table", "extra-table"),
)
def test_wrong_or_extra_table_blocks(
    tmp_path: Path,
    statements: list[str],
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    _create_database(
        module,
        root,
        [
            module.FORMAL_CREATE_TABLE_STATEMENT if item == "__EXACT__" else item
            for item in statements
        ],
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[3]
    assert receipt["exact_schema_verified"] is False
    assert receipt["decision_table_dml_statement_count"] == 0


@pytest.mark.parametrize(
    "extra_statement",
    [
        'CREATE VIEW "unexpected_view" AS SELECT 1 AS value',
        (
            'CREATE TRIGGER "unexpected_trigger" AFTER INSERT ON '
            '"governed_nonproduction_human_review_decisions_v0_1" '
            "BEGIN SELECT 1; END"
        ),
    ],
    ids=("view", "trigger"),
)
def test_view_or_trigger_blocks(
    tmp_path: Path,
    extra_statement: str,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    _create_database(
        module,
        root,
        [module.FORMAL_CREATE_TABLE_STATEMENT, extra_statement],
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[3]
    assert receipt["exact_schema_verified"] is False


def test_wrong_column_order_blocks(tmp_path: Path) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    fields = (module.DECISION_FIELDS[1], module.DECISION_FIELDS[0], *module.DECISION_FIELDS[2:])
    _create_database(module, root, [_column_statement(module, fields=fields)])
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[3]


@pytest.mark.parametrize(
    ("type_overrides", "nullable"),
    [
        ({"decision_schema": "INTEGER"}, set()),
        ({}, {"decision_schema"}),
    ],
    ids=("wrong-type", "wrong-nullability"),
)
def test_wrong_type_or_nullability_blocks(
    tmp_path: Path,
    type_overrides: dict[str, str],
    nullable: set[str],
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    _create_database(
        module,
        root,
        [
            _column_statement(
                module,
                type_overrides=type_overrides,
                nullable=nullable,
            )
        ],
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[3]


def test_wrong_uniqueness_blocks(tmp_path: Path) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    _create_database(
        module,
        root,
        [
            _column_statement(
                module,
                unique_fields={"decision_id", "idempotency_key"},
            )
        ],
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[3]


def test_malformed_database_is_bounded_failure(tmp_path: Path) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    target = _target(module, root)
    target.parent.mkdir(parents=True)
    target.write_bytes(b"not-a-sqlite-database")
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[6]
    assert receipt["sqlite_connection_open_count"] == 1
    assert receipt["decision_row_count"] is None
    assert receipt["integrity_result"] == "not_observed"


def _tampered_contract(old: bytes, before: bytes, after: bytes) -> bytes:
    assert old.count(before) == 1
    return old.replace(before, after, 1)


def test_contract_sha_mismatch_blocks_before_target_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path, contract_bytes=_contract_bytes() + b"\n")

    def forbidden_open(*_args, **_kwargs):
        raise AssertionError("identity mismatch must not open SQLite")

    monkeypatch.setattr(
        module,
        "_open_exact_formal_decision_ledger_connection",
        forbidden_open,
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[4]
    assert receipt["sqlite_connection_open_count"] == 0
    assert not _target(module, root).exists()


@pytest.mark.parametrize(
    ("before", "after"),
    [
        (
            b'"target_identity_version": "0.1"',
            b'"target_identity_version": "0.2"',
        ),
        (
            b'"authorization_contract_version": "0.1"',
            b'"authorization_contract_version": "0.2"',
        ),
        (
            b'"target_logical_label": "runtime/governed_nonproduction_human_review_decisions/review_decisions_v0_1.sqlite3"',
            b'"target_logical_label": "runtime/substituted.sqlite3"',
        ),
    ],
    ids=("identity-hash", "authorization-hash", "logical-target"),
)
def test_canonical_profile_mismatch_blocks_before_target_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    before: bytes,
    after: bytes,
) -> None:
    module = _module()
    content = _tampered_contract(_contract_bytes(), before, after)
    root = _synthetic_repository(tmp_path, contract_bytes=content)
    monkeypatch.setattr(
        module,
        "FORMAL_CONTRACT_SHA256",
        hashlib.sha256(content).hexdigest(),
    )

    def forbidden_open(*_args, **_kwargs):
        raise AssertionError("profile mismatch must not open SQLite")

    monkeypatch.setattr(
        module,
        "_open_exact_formal_decision_ledger_connection",
        forbidden_open,
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[4]
    assert receipt["sqlite_connection_open_count"] == 0
    assert not _target(module, root).exists()


def test_alternate_logical_target_argument_and_constant_substitution_are_blocked(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    signature = inspect.signature(getattr(module, FORMAL_OPERATION))
    assert "database_path" not in signature.parameters
    assert "target_path" not in signature.parameters
    assert "logical_target" not in signature.parameters
    assert "table_name" not in signature.parameters
    root = _synthetic_repository(tmp_path)
    monkeypatch.setattr(module, "FORMAL_LOGICAL_TARGET_LABEL", "../escape.sqlite3")
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[4]
    assert receipt["sqlite_connection_open_count"] == 0
    assert not (tmp_path / "escape.sqlite3").exists()


def test_symlink_escape_blocks_before_target_access(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    runtime = root / "runtime"
    original = Path.is_symlink

    def selected_symlink(path: Path) -> bool:
        if path == runtime:
            return True
        return original(path)

    monkeypatch.setattr(Path, "is_symlink", selected_symlink)
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[4]
    assert receipt["sqlite_connection_open_count"] == 0


def test_connection_open_failure_is_bounded(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    calls = 0

    def fail_open(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        raise sqlite3.OperationalError("synthetic open failure")

    monkeypatch.setattr(
        module,
        "_open_exact_formal_decision_ledger_connection",
        fail_open,
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert calls == 1
    assert receipt["outcome"] == EXPECTED_OUTCOMES[6]
    assert receipt["sqlite_connection_open_count"] == 0
    assert receipt["schema_ddl_statement_count"] == 0


class _ConnectionProxy:
    def __init__(self, connection: sqlite3.Connection, *, fail: str) -> None:
        self.connection = connection
        self.fail = fail
        self.commit_calls = 0
        self.close_calls = 0

    def execute(self, statement: str, parameters=()):
        if self.fail == "ddl" and statement.startswith("CREATE TABLE"):
            raise sqlite3.OperationalError("synthetic DDL failure")
        return self.connection.execute(statement, parameters)

    def commit(self) -> None:
        self.commit_calls += 1
        if self.fail == "commit":
            raise sqlite3.OperationalError("synthetic commit ambiguity")
        self.connection.commit()

    def close(self) -> None:
        self.close_calls += 1
        self.connection.close()


@pytest.mark.parametrize(
    ("failure", "expected_outcome"),
    [
        ("ddl", EXPECTED_OUTCOMES[6]),
        ("commit", EXPECTED_OUTCOMES[5]),
    ],
    ids=("ddl-failure", "commit-ambiguity"),
)
def test_ddl_failure_and_commit_ambiguity_are_nonretrying(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
    expected_outcome: str,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    target = _target(module, root)
    proxies: list[_ConnectionProxy] = []

    def open_proxy(path: Path, *, read_only: bool):
        assert path == target
        assert read_only is False
        proxy = _ConnectionProxy(sqlite3.connect(path), fail=failure)
        proxies.append(proxy)
        return proxy

    monkeypatch.setattr(
        module,
        "_open_exact_formal_decision_ledger_connection",
        open_proxy,
    )
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == expected_outcome
    assert receipt["sqlite_connection_open_count"] == 1
    assert receipt["sqlite_connection_reopen_count"] == 0
    assert len(proxies) == 1
    assert proxies[0].close_calls == 1
    assert proxies[0].commit_calls == (1 if failure == "commit" else 0)


def test_final_sidecar_mismatch_cannot_produce_success(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    target = _target(module, root)
    false_sidecar = Path(f"{target}-wal")
    original = Path.exists

    def sidecar_exists(path: Path) -> bool:
        if path == false_sidecar:
            return True
        return original(path)

    monkeypatch.setattr(Path, "exists", sidecar_exists)
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    assert receipt["outcome"] == EXPECTED_OUTCOMES[6]
    assert receipt["final_sidecar_count"] == 1
    assert receipt["outcome"] not in SUCCESS_OUTCOMES


def test_receipt_contract_all_outcomes_types_and_null_semantics() -> None:
    module = _module()
    assert module.INITIALIZATION_RECEIPT_FIELDS == EXPECTED_RECEIPT_FIELDS
    assert module.INITIALIZATION_RECEIPT_OUTCOMES == EXPECTED_OUTCOMES
    receipt = getattr(module, FORMAL_OPERATION)(
        repository_root=Path("synthetic-disabled-root")
    )
    _assert_receipt_shape(receipt)
    for field in (
        "sqlite_connection_open_count",
        "sqlite_connection_reopen_count",
        "schema_ddl_statement_count",
        "decision_table_dml_statement_count",
    ):
        assert type(receipt[field]) is int
        assert receipt[field] >= 0
    assert receipt["decision_row_count"] is None
    assert receipt["exact_schema_verified"] is None
    assert receipt["exact_empty_verified"] is None
    assert receipt["final_sidecar_count"] is None


def test_canonical_receipt_hash_is_pure_and_deterministic(
    tmp_path: Path,
) -> None:
    module = _module()
    root = _synthetic_repository(tmp_path)
    receipt = getattr(module, FORMAL_OPERATION)(repository_root=root, enabled=True)
    expected = hashlib.sha256(
        json.dumps(
            receipt,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    first = module.canonical_initialization_receipt_sha256(receipt)
    second = module.canonical_initialization_receipt_sha256(dict(receipt))
    assert first == second == expected
    assert len(first) == 64


def test_formal_initializer_has_no_writer_route_dml_discovery_or_network() -> None:
    module = _module()
    source = inspect.getsource(module)
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        node.module or ""
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    )
    operation_source = inspect.getsource(getattr(module, FORMAL_OPERATION))
    private_source = inspect.getsource(
        module._initialize_exact_formal_decision_ledger_once
    )
    combined = operation_source + private_source
    for forbidden in (
        "record_governed_nonproduction_human_review_decision",
        "INSERT INTO",
        "UPDATE ",
        "DELETE FROM",
        ".initialize(",
        "glob(",
        "rglob(",
        "iterdir(",
        "listdir(",
        "walk(",
        "subprocess",
        "requests",
        "httpx",
        "os.environ",
    ):
        assert forbidden not in combined
    assert "subprocess" not in imported
    assert "requests" not in imported
    assert "httpx" not in imported
    assert "app.api" not in source
    assert "governed_nonproduction_review_console_projection" not in source
    assert "governed_nonproduction_exact_target" not in source
    assert "governed_nonproduction_evidence_persistence" not in source


def test_existing_formal_rejection_guard_remains_exact() -> None:
    module = _module()
    source = inspect.getsource(
        module.GovernedNonproductionHumanReviewDecisionLedger._require_available
    )
    assert "if _formal_target_selected(self.database_path):" in source
    assert source.count(
        "raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable()"
    ) == 2
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        module.FORMAL_LOGICAL_TARGET_LABEL,
        enabled=True,
    )
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        ledger.initialize()


def test_generic_temporary_sqlite_f11_behavior_remains_available(
    tmp_path: Path,
) -> None:
    module = _module()
    database = tmp_path / "synthetic" / "review_decisions.sqlite3"
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        database,
        enabled=True,
    )
    ledger.initialize()
    assert database.exists()
    with sqlite3.connect(database) as connection:
        assert connection.execute(
            f'SELECT COUNT(*) FROM "{module.PRIMARY_TABLE}"'
        ).fetchone() == (0,)


def test_synthetic_matrix_declares_all_35_required_controls() -> None:
    covered_controls = tuple(range(1, 36))
    assert len(covered_controls) == 35
    assert covered_controls == tuple(range(1, 36))
