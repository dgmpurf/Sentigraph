from __future__ import annotations

import inspect
import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from app.api.v1.routes import (
    internal_alpha_governed_review_decisions as route_module,
)
from app.services import (
    governed_nonproduction_human_review_decision_ledger as ledger_module,
)


EXPECTED_FIELDS = ledger_module.FORMAL_STATE_PROJECTION_FIELDS
PROHIBITED_RESPONSE_MARKERS = (
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
    "decision_canonical_hash",
    "recorded_at",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
    "activation_decision_safe_hash",
    ledger_module.FORMAL_LOGICAL_TARGET_LABEL,
    "SELECT *",
    "INSERT INTO",
)


def _write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def _first_decision() -> dict[str, Any]:
    return ledger_module._build_decision(
        ledger_module._identity_for("keep_pending_human_review"),
        "2026-07-15T11:52:08Z",
    )


def _later_decision(activation_hash: str) -> dict[str, Any]:
    context = ledger_module._formal_second_server_owned_context(
        activation_hash
    )
    return ledger_module._build_decision(
        ledger_module._identity_for_context(
            "request_more_governance_review",
            context,
        ),
        "2026-08-10T00:00:00Z",
    )


def _synthetic_repository(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "synthetic-repository"
    source_root = Path(__file__).resolve().parents[3]
    contract_relative = Path(ledger_module.FORMAL_CONTRACT_RELATIVE_PATH)
    _write(
        root / contract_relative,
        (source_root / contract_relative).read_bytes(),
    )
    (root / "backend/app/services").mkdir(parents=True, exist_ok=True)
    return root, root / Path(ledger_module.FORMAL_LOGICAL_TARGET_LABEL)


def _build_case(
    tmp_path: Path,
    *,
    row_count: int = 1,
    extra_table: bool = False,
) -> tuple[Path, Path]:
    root, target = _synthetic_repository(tmp_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as connection:
        connection.execute(ledger_module.FORMAL_CREATE_TABLE_STATEMENT)
        if extra_table:
            connection.execute("CREATE TABLE unexpected_table (value TEXT)")
        writer = ledger_module.GovernedNonproductionHumanReviewDecisionLedger(
            target,
            enabled=True,
        )
        if row_count >= 1:
            writer._insert_record(connection, _first_decision())
        if row_count >= 2:
            writer._insert_record(connection, _later_decision("6" * 64))
        if row_count >= 3:
            writer._insert_record(connection, _later_decision("8" * 64))
        connection.commit()
    return root, target


def _project(root: Path) -> dict[str, Any]:
    return ledger_module.project_exact_formal_governed_nonproduction_human_review_decision_state(
        repository_root=root,
        enabled=True,
    )


def _response_json(response: Any) -> dict[str, Any]:
    return json.loads(response.body.decode("utf-8"))


def _assert_fixed_safety(result: dict[str, Any]) -> None:
    assert result["human_review_required"] is True
    assert result["no_automatic_trust_upgrade"] is True
    for field in (
        "write_performed",
        "production_object_enabled",
        "review_queue_runtime_enabled",
        "operator_runtime_ready",
        "public_ready",
        "production_ready",
        "mutable_authority_granted",
        "third_decision_allowed",
    ):
        assert result[field] is False


def test_contract_surface_and_disabled_path_are_exact(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    def forbidden_profile(_root: str | Path) -> tuple[Path, Path]:
        raise AssertionError("disabled projection must not resolve the target")

    monkeypatch.setattr(
        ledger_module,
        "_validate_exact_formal_decision_ledger_profile",
        forbidden_profile,
    )
    result = ledger_module.project_exact_formal_governed_nonproduction_human_review_decision_state(
        repository_root=tmp_path,
        enabled=False,
    )
    assert tuple(result) == EXPECTED_FIELDS
    assert len(result) == 19
    assert result["projection_status"] == "formal_state_disabled"
    assert result["projection_error_code"] == (
        "formal_state_projection_disabled"
    )
    assert result["formal_first_decision_present"] is False
    assert result["formal_second_decision_present"] is False
    assert result["formal_second_decision_type"] is None
    assert result["formal_decision_count"] == 0
    _assert_fixed_safety(result)


@pytest.mark.parametrize("row_count", (1, 2))
def test_ready_one_or_two_row_projection_is_exact_and_bounded(
    tmp_path: Path,
    row_count: int,
) -> None:
    root, _target = _build_case(tmp_path, row_count=row_count)
    result = _project(root)
    assert tuple(result) == EXPECTED_FIELDS
    assert result["projection_status"] == "formal_state_ready"
    assert result["projection_error_code"] is None
    assert result["formal_first_decision_present"] is True
    assert result["formal_second_decision_present"] is (row_count == 2)
    assert result["formal_second_decision_type"] == (
        "request_more_governance_review" if row_count == 2 else None
    )
    assert result["formal_decision_count"] == row_count
    _assert_fixed_safety(result)
    serialized = json.dumps(result, ensure_ascii=False)
    for marker in PROHIBITED_RESPONSE_MARKERS:
        assert marker not in serialized


def test_read_path_uses_one_read_only_open_query_only_and_zero_dml(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root, target = _build_case(tmp_path, row_count=2)
    original_open = ledger_module._open_exact_formal_decision_ledger_connection
    open_modes: list[tuple[Path, bool]] = []
    statements: list[str] = []

    def tracked_open(path: Path, *, read_only: bool) -> sqlite3.Connection:
        open_modes.append((path, read_only))
        connection = original_open(path, read_only=read_only)
        connection.set_trace_callback(statements.append)
        return connection

    def forbidden_writer(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("read projection must not invoke a writer")

    monkeypatch.setattr(
        ledger_module,
        "_open_exact_formal_decision_ledger_connection",
        tracked_open,
    )
    monkeypatch.setattr(
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        forbidden_writer,
    )
    monkeypatch.setattr(
        ledger_module,
        "record_second_exact_formal_human_review_decision",
        forbidden_writer,
    )
    result = _project(root)
    assert result["projection_status"] == "formal_state_ready"
    assert open_modes == [(target, True)]
    normalized = [statement.strip().upper() for statement in statements]
    assert "PRAGMA QUERY_ONLY = ON" in normalized
    assert not any(
        statement.startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"))
        for statement in normalized
    )


def test_third_row_state_fails_closed(tmp_path: Path) -> None:
    root, _target = _build_case(tmp_path, row_count=3)
    result = _project(root)
    assert result["projection_status"] == "formal_state_inconsistent"
    assert result["projection_error_code"] == "formal_state_integrity_failure"
    assert result["formal_decision_count"] == 0
    assert result["formal_first_decision_present"] is False
    assert result["formal_second_decision_present"] is False
    _assert_fixed_safety(result)


@pytest.mark.parametrize("failure_kind", ("schema", "sidecar"))
def test_schema_or_sidecar_mismatch_fails_closed(
    tmp_path: Path,
    failure_kind: str,
) -> None:
    root, target = _build_case(
        tmp_path,
        row_count=1,
        extra_table=failure_kind == "schema",
    )
    if failure_kind == "sidecar":
        Path(f"{target}-wal").write_bytes(b"synthetic-sidecar")
    result = _project(root)
    assert result["projection_status"] == "formal_state_inconsistent"
    assert result["projection_error_code"] == "formal_state_integrity_failure"
    _assert_fixed_safety(result)


def test_integrity_mismatch_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root, _target = _build_case(tmp_path, row_count=1)
    original_open = ledger_module._open_exact_formal_decision_ledger_connection

    class FailedIntegrityCursor:
        @staticmethod
        def fetchall() -> list[tuple[str]]:
            return [("synthetic_integrity_failure",)]

    class IntegrityFailureConnection:
        def __init__(self, connection: sqlite3.Connection) -> None:
            self.connection = connection

        def execute(self, statement: str, *args: Any) -> Any:
            if statement == "PRAGMA integrity_check":
                return FailedIntegrityCursor()
            return self.connection.execute(statement, *args)

        def close(self) -> None:
            self.connection.close()

    def integrity_failure_open(
        path: Path,
        *,
        read_only: bool,
    ) -> IntegrityFailureConnection:
        return IntegrityFailureConnection(
            original_open(path, read_only=read_only)
        )

    monkeypatch.setattr(
        ledger_module,
        "_open_exact_formal_decision_ledger_connection",
        integrity_failure_open,
    )
    result = _project(root)
    assert result["projection_status"] == "formal_state_inconsistent"
    assert result["projection_error_code"] == "formal_state_integrity_failure"
    _assert_fixed_safety(result)


def test_missing_target_is_bounded_unavailable(tmp_path: Path) -> None:
    root, _target = _synthetic_repository(tmp_path)
    result = _project(root)
    assert result["projection_status"] == "formal_state_unavailable"
    assert result["projection_error_code"] == "formal_state_target_unavailable"
    _assert_fixed_safety(result)


def test_route_requires_both_gates_and_maps_ready_state(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    root, _target = _build_case(tmp_path, row_count=2)
    monkeypatch.setattr(route_module, "_repository_root", lambda: root)
    monkeypatch.delenv(route_module.GATE, raising=False)
    monkeypatch.delenv(route_module.FORMAL_STATE_PROJECTION_GATE, raising=False)

    primary_off = route_module.get_formal_state()
    monkeypatch.setenv(route_module.GATE, "1")
    dedicated_off = route_module.get_formal_state()
    monkeypatch.delenv(route_module.GATE, raising=False)
    monkeypatch.setenv(route_module.FORMAL_STATE_PROJECTION_GATE, "1")
    primary_still_off = route_module.get_formal_state()
    monkeypatch.setenv(route_module.GATE, "1")
    ready = route_module.get_formal_state()

    assert [primary_off.status_code, dedicated_off.status_code, primary_still_off.status_code] == [
        404,
        404,
        404,
    ]
    assert ready.status_code == 200
    ready_body = _response_json(ready)
    assert tuple(ready_body) == EXPECTED_FIELDS
    assert ready_body["projection_status"] == "formal_state_ready"
    assert ready_body["formal_decision_count"] == 2


def test_route_metadata_has_no_body_path_or_query_and_get_by_id_is_unchanged() -> None:
    matching_routes = [
        route
        for route in route_module.router.routes
        if getattr(route, "path", None) == "/formal-state"
    ]
    assert len(matching_routes) == 1
    formal_route = matching_routes[0]
    assert formal_route.methods == {"GET"}
    assert tuple(inspect.signature(route_module.get_formal_state).parameters) == ()
    assert formal_route.dependant.body_params == []
    assert formal_route.dependant.path_params == []
    assert formal_route.dependant.query_params == []

    existing_get_source = inspect.getsource(route_module.get_decision)
    assert "FORMAL_SECOND" not in existing_get_source
    assert "FORMAL_STATE" not in existing_get_source
    assert "project_exact_formal" not in existing_get_source


def test_unexpected_service_failure_returns_only_bounded_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(route_module.GATE, "1")
    monkeypatch.setenv(route_module.FORMAL_STATE_PROJECTION_GATE, "1")

    def failed_service(**_kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("synthetic_private_exception")

    monkeypatch.setattr(
        route_module,
        "project_exact_formal_governed_nonproduction_human_review_decision_state",
        failed_service,
    )
    response = route_module.get_formal_state()
    body = _response_json(response)
    assert response.status_code == 503
    assert tuple(body) == EXPECTED_FIELDS
    assert body["projection_status"] == "formal_state_unavailable"
    assert "synthetic_private_exception" not in json.dumps(body)
    _assert_fixed_safety(body)
