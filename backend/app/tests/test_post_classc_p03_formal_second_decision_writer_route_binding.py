from __future__ import annotations

import hashlib
import inspect
import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from backend.app.api.v1.routes import (
    internal_alpha_governed_review_decisions as route_module,
)
from backend.app.services import (
    governed_nonproduction_human_review_decision_ledger as ledger_module,
)


EXPECTED_ACTIVATION_FIELDS = (
    "activation_schema",
    "activation_version",
    "milestone_id",
    "route_purpose",
    "repository_identity",
    "required_branch",
    "implementation_commit",
    "implementation_service_sha256",
    "implementation_route_sha256",
    "implementation_test_sha256",
    "implementation_report_sha256",
    "accepted_p03_design_result_sha256",
    "accepted_p03_design_acceptance_sha256",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "accepted_first_decision_type",
    "accepted_first_decision_id",
    "accepted_first_idempotency_key",
    "accepted_first_audit_receipt_reference",
    "accepted_first_decision_canonical_sha256",
    "required_prestate_row_count",
    "allowed_mutation_decision_type",
    "activation_decision_safe_hash",
    "fresh_runtime_goal_id",
    "fresh_runtime_approval_sha256",
    "formal_target_access_session_limit",
    "sqlite_connection_open_limit",
    "sqlite_connection_reopen_limit",
    "decision_insert_limit",
    "automatic_retry_allowed",
    "automatic_repair_allowed",
    "third_decision_allowed",
    "nonreusable",
)


def _canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def _activation() -> tuple[dict[str, Any], str]:
    values = {
        "activation_schema": (
            "sentigraph_post_classc_p03_formal_second_decision_activation_v0_1"
        ),
        "activation_version": "0.1",
        "milestone_id": (
            "sentigraph_post_classc_p03_formal_second_decision_route_binding_v0_1"
        ),
        "route_purpose": "formal_second_human_review_decision_only",
        "repository_identity": "dgmpurf/Sentigraph",
        "required_branch": "main",
        "implementation_commit": "1" * 40,
        "implementation_service_sha256": "2" * 64,
        "implementation_route_sha256": "3" * 64,
        "implementation_test_sha256": "4" * 64,
        "implementation_report_sha256": "5" * 64,
        "accepted_p03_design_result_sha256": (
            "86aeee2bf26949c8b28b6c68361a59137ff88f642b508c118457af2063a65fc1"
        ),
        "accepted_p03_design_acceptance_sha256": (
            "d37bee0fb798cb3febe8eab80ad779670969a2588d469dfc837220ca821424b0"
        ),
        "target_identity_safe_hash": (
            ledger_module.FORMAL_TARGET_IDENTITY_SAFE_HASH
        ),
        "target_authorization_contract_safe_hash": (
            ledger_module.FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "accepted_first_decision_type": "keep_pending_human_review",
        "accepted_first_decision_id": (
            "ghrd-b666c0f03a975c94e6b3b248bd05cdc9"
        ),
        "accepted_first_idempotency_key": (
            "b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db"
        ),
        "accepted_first_audit_receipt_reference": (
            "ghrd-receipt-b666c0f03a975c94e6b3b248bd05cdc9"
        ),
        "accepted_first_decision_canonical_sha256": (
            "604ded010ca6ea46a6c63d4011445fdcbd775fd498231260e5cd59f88d51452e"
        ),
        "required_prestate_row_count": 1,
        "allowed_mutation_decision_type": "request_more_governance_review",
        "activation_decision_safe_hash": "6" * 64,
        "fresh_runtime_goal_id": (
            "SENTIGRAPH_FRESH_FORMAL_SECOND_DECISION_RUNTIME_TEST_ONLY"
        ),
        "fresh_runtime_approval_sha256": "7" * 64,
        "formal_target_access_session_limit": 1,
        "sqlite_connection_open_limit": 1,
        "sqlite_connection_reopen_limit": 0,
        "decision_insert_limit": 1,
        "automatic_retry_allowed": False,
        "automatic_repair_allowed": False,
        "third_decision_allowed": False,
        "nonreusable": True,
    }
    activation = {field: values[field] for field in EXPECTED_ACTIVATION_FIELDS}
    return activation, _canonical_sha256(activation)


def _request(decision_type: str) -> dict[str, str]:
    return {
        "request_schema": ledger_module.REQUEST_SCHEMA,
        "request_version": ledger_module.REQUEST_VERSION,
        "decision_type": decision_type,
    }


def _first_decision(*, exact: bool = True) -> dict[str, Any]:
    recorded_at = (
        "2026-07-15T11:52:08Z" if exact else "2026-07-15T11:52:09Z"
    )
    return ledger_module._build_decision(
        ledger_module._identity_for("keep_pending_human_review"),
        recorded_at,
    )


def _build_case(
    tmp_path: Path,
    *,
    row_count: int = 1,
    exact_first: bool = True,
    extra_table: bool = False,
) -> dict[str, Any]:
    root = tmp_path / "synthetic-repository"
    source_root = Path(__file__).resolve().parents[3]
    contract_relative = Path(ledger_module.FORMAL_CONTRACT_RELATIVE_PATH)
    _write(
        root / contract_relative,
        (source_root / contract_relative).read_bytes(),
    )
    (root / "backend/app/services").mkdir(parents=True, exist_ok=True)
    target = root / Path(ledger_module.FORMAL_LOGICAL_TARGET_LABEL)
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
            writer._insert_record(
                connection,
                _first_decision(exact=exact_first),
            )
        if row_count >= 2:
            writer._insert_record(
                connection,
                ledger_module._build_decision(
                    ledger_module._identity_for(
                        "request_more_governance_review"
                    ),
                    "2026-07-15T11:53:00Z",
                ),
            )
        connection.commit()
    activation, activation_hash = _activation()
    return {
        "root": root,
        "target": target,
        "activation": activation,
        "activation_hash": activation_hash,
    }


def _call(
    case: dict[str, Any],
    decision_type: str,
    **overrides: Any,
) -> dict[str, Any]:
    values = {
        "repository_root": case["root"],
        "request": _request(decision_type),
        "second_activation_object": case["activation"],
        "second_activation_binding_safe_hash": case["activation_hash"],
        "enabled": True,
    }
    values.update(overrides)
    return ledger_module.record_second_exact_formal_human_review_decision(
        **values
    )


def _read_rows(target: Path) -> list[dict[str, Any]]:
    with sqlite3.connect(target) as connection:
        rows = connection.execute(
            f'SELECT * FROM "{ledger_module.FORMAL_PRIMARY_TABLE}" '
            "ORDER BY rowid"
        ).fetchall()
    return [ledger_module._row_to_decision(row) for row in rows]


def _response_json(response: Any) -> dict[str, Any]:
    return json.loads(response.body.decode("utf-8"))


def _route_request(decision_type: str) -> Any:
    return route_module.GovernedNonproductionHumanReviewDecisionRequest(
        **_request(decision_type)
    )


def _set_route_activation(
    monkeypatch: pytest.MonkeyPatch,
    activation: dict[str, Any],
    activation_hash: str,
) -> None:
    monkeypatch.setenv(route_module.GATE, "1")
    monkeypatch.setenv(route_module.FORMAL_SECOND_GATE, "1")
    monkeypatch.setenv(
        route_module.FORMAL_SECOND_ACTIVATION_JSON,
        json.dumps(activation, ensure_ascii=False, separators=(",", ":")),
    )
    monkeypatch.setenv(
        route_module.FORMAL_SECOND_ACTIVATION_SHA256,
        activation_hash,
    )
    monkeypatch.setattr(
        route_module,
        "_formal_second_activation_consumed",
        False,
    )


def test_contract_surface_and_activation_order_are_exact() -> None:
    assert callable(ledger_module._identity_for_context)
    assert callable(ledger_module.record_second_exact_formal_human_review_decision)
    assert (
        ledger_module.FORMAL_SECOND_ACTIVATION_FIELDS
        == EXPECTED_ACTIVATION_FIELDS
    )
    assert ledger_module.FORMAL_SECOND_ACTIVATION_SCHEMA == (
        "sentigraph_post_classc_p03_formal_second_decision_activation_v0_1"
    )
    assert len(ledger_module.DECISION_FIELDS) == 38
    assert len(ledger_module.RECEIPT_FIELDS) == 27
    assert len(ledger_module._IDEMPOTENCY_FIELDS) == 19
    assert len(ledger_module._BOOLEAN_FIELDS) == 8
    assert len(ledger_module._JSON_FIELDS) == 4
    assert not hasattr(ledger_module, "FORMAL_SECOND_ACTIVE_ACTIVATION")


def test_generic_identity_and_formal_target_guard_remain_frozen(
    tmp_path: Path,
) -> None:
    identity = ledger_module._identity_for("keep_pending_human_review")
    assert identity["idempotency_key"] == (
        "b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db"
    )
    case = _build_case(tmp_path)
    generic = ledger_module.GovernedNonproductionHumanReviewDecisionLedger(
        case["target"],
        enabled=True,
    )
    with pytest.raises(
        ledger_module.GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        generic._require_available()


def test_per_call_context_allows_only_new_activation_hash() -> None:
    activation, _ = _activation()
    context = ledger_module._formal_second_server_owned_context(
        activation["activation_decision_safe_hash"]
    )
    assert tuple(context) == tuple(ledger_module.SERVER_OWNED_CONTEXT)
    assert all(
        context[field] == value
        for field, value in ledger_module.SERVER_OWNED_CONTEXT.items()
        if field != "activation_decision_safe_hash"
    )
    assert context["activation_decision_safe_hash"] == "6" * 64
    second = ledger_module._identity_for_context(
        "request_more_governance_review",
        context,
    )
    first = ledger_module._identity_for("keep_pending_human_review")
    assert second["idempotency_key"] != first["idempotency_key"]
    bad = dict(context)
    bad["gate_contract_safe_hash"] = "8" * 64
    with pytest.raises(
        ledger_module.GovernedNonproductionHumanReviewDecisionIntegrityError
    ):
        ledger_module._formal_second_server_owned_context(
            bad["activation_decision_safe_hash"],
            candidate_context=bad,
        )


@pytest.mark.parametrize(
    "kind",
    ("same_first_hash", "historical_p3_activation", "wrong_order"),
)
def test_malformed_or_reused_activation_stops_before_target_access(
    tmp_path: Path,
    kind: str,
) -> None:
    case = _build_case(tmp_path)
    activation = dict(case["activation"])
    if kind == "same_first_hash":
        activation["activation_decision_safe_hash"] = (
            ledger_module.SERVER_OWNED_CONTEXT["activation_decision_safe_hash"]
        )
    elif kind == "historical_p3_activation":
        activation = {
            "activation_schema": ledger_module.P3_ACTIVATION_SCHEMA,
            "activation_version": ledger_module.P3_ACTIVATION_VERSION,
        }
    else:
        activation = dict(reversed(tuple(activation.items())))
    result = _call(
        case,
        "request_more_governance_review",
        second_activation_object=activation,
        second_activation_binding_safe_hash=_canonical_sha256(activation),
    )
    assert result["outcome"] == "blocked_formal_second_activation_mismatch"
    assert result["formal_target_access_session_count"] == 0
    assert result["sqlite_connection_open_count"] == 0
    assert result["decision_insert_issued_count"] == 0


def test_keep_pending_reuses_exact_first_row_without_mutation(
    tmp_path: Path,
) -> None:
    case = _build_case(tmp_path)
    result = _call(case, "keep_pending_human_review")
    assert result["outcome"] == "already_exists_same_human_review_decision"
    assert result["decision_row_count_before"] == 1
    assert result["decision_row_count_after"] == 1
    assert result["decision_insert_issued_count"] == 0
    assert result["mutation_count"] == 0
    assert result["receipt"]["created_new_entry"] is False
    assert result["receipt"]["reused_existing_entry"] is True
    assert result["decision"] == _first_decision()
    assert _read_rows(case["target"]) == [_first_decision()]


def test_request_more_inserts_one_distinct_second_row(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    monkeypatch.setattr(
        ledger_module,
        "_utc_clock",
        lambda: "2026-08-09T00:00:00Z",
    )
    insert_calls = 0
    original = (
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger._insert_record
    )

    def counted_insert(
        self: Any,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal insert_calls
        insert_calls += 1
        original(self, connection, decision)

    monkeypatch.setattr(
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_insert,
    )
    result = _call(case, "request_more_governance_review")
    rows = _read_rows(case["target"])
    assert result["outcome"] == "created_exactly_one_human_review_decision"
    assert result["decision_row_count_before"] == 1
    assert result["decision_row_count_after"] == 2
    assert result["decision_insert_issued_count"] == 1
    assert result["mutation_count"] == 1
    assert insert_calls == 1
    assert rows[0] == _first_decision()
    assert rows[1] == result["decision"]
    assert rows[1]["decision_type"] == "request_more_governance_review"
    assert rows[1]["idempotency_key"] != rows[0]["idempotency_key"]
    assert rows[1]["activation_decision_safe_hash"] == "6" * 64


@pytest.mark.parametrize(
    "case_options",
    (
        {"row_count": 0},
        {"row_count": 2},
        {"row_count": 1, "exact_first": False},
        {"row_count": 1, "extra_table": True},
    ),
)
def test_wrong_count_schema_or_first_row_blocks_before_insert(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case_options: dict[str, Any],
) -> None:
    case = _build_case(tmp_path, **case_options)
    inserts = 0
    original = (
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger._insert_record
    )

    def counted_insert(
        self: Any,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal inserts
        inserts += 1
        original(self, connection, decision)

    monkeypatch.setattr(
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_insert,
    )
    before = len(_read_rows(case["target"]))
    result = _call(case, "request_more_governance_review")
    after = len(_read_rows(case["target"]))
    assert result["outcome"] == "blocked_binding_or_snapshot_mismatch"
    assert result["decision_insert_issued_count"] == 0
    assert inserts == 0
    assert after == before


def test_commit_ambiguity_never_reopens_retries_or_reinserts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    open_calls = 0
    insert_calls = 0
    original_open = ledger_module._open_exact_formal_decision_ledger_connection
    original_insert = (
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger._insert_record
    )

    class AmbiguousConnection:
        def __init__(self, connection: sqlite3.Connection) -> None:
            self.connection = connection

        def __getattr__(self, name: str) -> Any:
            return getattr(self.connection, name)

        def commit(self) -> None:
            self.connection.commit()
            raise sqlite3.OperationalError("synthetic ambiguity")

    def ambiguous_open(path: Path, *, read_only: bool) -> Any:
        nonlocal open_calls
        open_calls += 1
        return AmbiguousConnection(
            original_open(path, read_only=read_only)
        )

    def counted_insert(
        self: Any,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal insert_calls
        insert_calls += 1
        original_insert(self, connection, decision)

    monkeypatch.setattr(
        ledger_module,
        "_open_exact_formal_decision_ledger_connection",
        ambiguous_open,
    )
    monkeypatch.setattr(
        ledger_module.GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_insert,
    )
    result = _call(case, "request_more_governance_review")
    assert result["outcome"] == (
        "paused_pending_read_only_idempotency_verification"
    )
    assert result["sqlite_connection_open_count"] == 1
    assert result["sqlite_connection_reopen_count"] == 0
    assert result["decision_insert_issued_count"] == 1
    assert open_calls == 1
    assert insert_calls == 1
    assert len(_read_rows(case["target"])) in (1, 2)


def test_primary_and_formal_gate_fail_closed_without_writer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def forbidden_writer(**_kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        raise AssertionError("writer must not run")

    monkeypatch.setattr(
        route_module,
        "record_second_exact_formal_human_review_decision",
        forbidden_writer,
    )
    monkeypatch.delenv(route_module.GATE, raising=False)
    monkeypatch.delenv(route_module.FORMAL_SECOND_GATE, raising=False)
    primary_off = route_module.post_decision(
        _route_request("request_more_governance_review")
    )
    monkeypatch.setenv(route_module.GATE, "1")
    formal_off = route_module.post_decision(
        _route_request("request_more_governance_review")
    )
    assert primary_off.status_code == 404
    assert formal_off.status_code == 503
    assert calls == 0


@pytest.mark.parametrize(
    "mode",
    ("missing", "bad_json", "duplicate_key", "wrong_hash"),
)
def test_invalid_activation_returns_503_before_formal_access(
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
) -> None:
    calls = 0

    def forbidden_writer(**_kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        raise AssertionError("writer must not run")

    monkeypatch.setattr(
        route_module,
        "record_second_exact_formal_human_review_decision",
        forbidden_writer,
    )
    monkeypatch.setenv(route_module.GATE, "1")
    monkeypatch.setenv(route_module.FORMAL_SECOND_GATE, "1")
    monkeypatch.setattr(
        route_module,
        "_formal_second_activation_consumed",
        False,
    )
    activation, activation_hash = _activation()
    if mode == "missing":
        monkeypatch.delenv(
            route_module.FORMAL_SECOND_ACTIVATION_JSON,
            raising=False,
        )
        monkeypatch.delenv(
            route_module.FORMAL_SECOND_ACTIVATION_SHA256,
            raising=False,
        )
    elif mode == "bad_json":
        monkeypatch.setenv(route_module.FORMAL_SECOND_ACTIVATION_JSON, "{")
        monkeypatch.setenv(
            route_module.FORMAL_SECOND_ACTIVATION_SHA256,
            activation_hash,
        )
    elif mode == "duplicate_key":
        monkeypatch.setenv(
            route_module.FORMAL_SECOND_ACTIVATION_JSON,
            '{"activation_schema":"a","activation_schema":"b"}',
        )
        monkeypatch.setenv(
            route_module.FORMAL_SECOND_ACTIVATION_SHA256,
            activation_hash,
        )
    else:
        monkeypatch.setenv(
            route_module.FORMAL_SECOND_ACTIVATION_JSON,
            json.dumps(activation, separators=(",", ":")),
        )
        monkeypatch.setenv(
            route_module.FORMAL_SECOND_ACTIVATION_SHA256,
            "0" * 64,
        )
    response = route_module.post_decision(
        _route_request("request_more_governance_review")
    )
    body = _response_json(response)
    assert response.status_code == 503
    assert calls == 0
    assert body["decision"] is None
    assert body["receipt"] is None
    assert "activation" not in json.dumps(body).lower()
    assert "sqlite" not in json.dumps(body).lower()


@pytest.mark.parametrize(
    "decision_type,status,outcome,mutation_count",
    (
        (
            "keep_pending_human_review",
            200,
            "already_exists_same_human_review_decision",
            0,
        ),
        (
            "request_more_governance_review",
            201,
            "created_exactly_one_human_review_decision",
            1,
        ),
    ),
)
def test_exact_route_activation_invokes_dedicated_writer_once_then_consumes(
    monkeypatch: pytest.MonkeyPatch,
    decision_type: str,
    status: int,
    outcome: str,
    mutation_count: int,
) -> None:
    activation, activation_hash = _activation()
    _set_route_activation(monkeypatch, activation, activation_hash)
    calls: list[dict[str, Any]] = []
    context = ledger_module._formal_second_server_owned_context(
        activation["activation_decision_safe_hash"]
    )
    identity = (
        ledger_module._identity_for("keep_pending_human_review")
        if decision_type == "keep_pending_human_review"
        else ledger_module._identity_for_context(decision_type, context)
    )
    decision = ledger_module._build_decision(
        identity,
        "2026-08-09T00:00:00Z",
    )
    receipt = ledger_module._receipt(
        outcome,
        decision=decision,
        row_count_before=1,
        row_count_after=1 + mutation_count,
    )

    def fake_writer(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {
            "outcome": outcome,
            "decision": decision,
            "receipt": receipt,
        }

    monkeypatch.setattr(
        route_module,
        "record_second_exact_formal_human_review_decision",
        fake_writer,
    )
    first = route_module.post_decision(_route_request(decision_type))
    second = route_module.post_decision(_route_request(decision_type))
    first_body = _response_json(first)
    second_body = _response_json(second)
    assert first.status_code == status
    assert first_body["decision_id"] == decision["decision_id"]
    assert first_body["receipt"]["outcome"] == outcome
    assert first_body["decision_ledger_write_performed"] is bool(
        mutation_count
    )
    assert second.status_code == 503
    assert second_body["decision"] is None
    assert len(calls) == 1
    assert calls[0]["request"] == _request(decision_type)
    assert calls[0]["second_activation_object"] == activation
    assert calls[0]["second_activation_binding_safe_hash"] == activation_hash
    assert calls[0]["repository_root"] == (
        Path(route_module.__file__).resolve().parents[5]
    )


def test_http_model_rejects_physical_and_activation_extra_fields() -> None:
    base = _request("request_more_governance_review")
    for field in (
        "database_path",
        "formal_target_path",
        "repository_root",
        "activation",
        "activation_sha256",
    ):
        with pytest.raises(ValidationError):
            route_module.GovernedNonproductionHumanReviewDecisionRequest(
                **base,
                **{field: "forbidden"},
            )


def test_get_route_has_no_formal_second_binding_and_outer_shape_is_frozen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = inspect.getsource(route_module.get_decision)
    assert "FORMAL_SECOND" not in source
    assert "record_second_exact_formal" not in source
    monkeypatch.delenv(route_module.GATE, raising=False)
    response = route_module.get_decision(
        "ghrd-b666c0f03a975c94e6b3b248bd05cdc9"
    )
    body = _response_json(response)
    assert response.status_code == 404
    assert tuple(body) == (
        "response_schema",
        "route_mode",
        "decision_id",
        "decision",
        "human_review_required",
        "no_automatic_trust_upgrade",
        "production_object_enabled",
        "review_queue_runtime_enabled",
        "operator_runtime_ready",
        "public_ready",
        "production_ready",
    )

