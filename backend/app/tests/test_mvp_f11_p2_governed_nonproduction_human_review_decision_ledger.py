from __future__ import annotations

import ast
import importlib
import inspect
import json
import re
import sqlite3
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError


SERVICE_MODULE = (
    "app.services.governed_nonproduction_human_review_decision_ledger"
)
ROUTE_MODULE = (
    "app.api.v1.routes.internal_alpha_governed_review_decisions"
)
GATE = "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_LEDGER_ENABLED"
ROUTE_PREFIX = "/api/v1/internal/alpha/governed-review-decisions"

REQUEST_SCHEMA = (
    "sentigraph_governed_nonproduction_human_review_decision_request_v0_1"
)
REQUEST_VERSION = "0.1"
REQUEST_FIELDS = (
    "request_schema",
    "request_version",
    "decision_type",
)
DECISION_TYPES = (
    "keep_pending_human_review",
    "request_more_governance_review",
)
DECISION_SCHEMA = (
    "sentigraph_governed_nonproduction_human_review_decision_record_v0_1"
)
DECISION_VERSION = "0.1"
DECISION_FIELDS = (
    "decision_schema",
    "decision_version",
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
    "ledger_scope",
    "decision_type",
    "decision_status",
    "recorded_at",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
    "reviewer_identity_verified",
    "source_projection_schema",
    "source_projection_version",
    "source_projection_id",
    "source_projection_status",
    "source_projection_canonical_sha256",
    "source_outer_response_canonical_sha256",
    "persisted_record_id",
    "attempt_reservation_id",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_safe_hash",
    "activation_decision_safe_hash",
    "record_snapshot_digest",
    "reservation_snapshot_digest",
    "decision_canonical_hash",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_changed",
    "production_case_changed",
    "downstream_runtime_called",
    "correction_or_revocation_performed",
    "deleted_or_updated",
    "allowed_follow_up_labels",
    "blocked_follow_up_labels",
    "warnings",
    "blockers",
)
RECEIPT_SCHEMA = (
    "sentigraph_governed_nonproduction_human_review_decision_receipt_v0_1"
)
RECEIPT_VERSION = "0.1"
RECEIPT_FIELDS = (
    "receipt_schema",
    "receipt_version",
    "outcome",
    "audit_receipt_reference",
    "decision_id",
    "idempotency_key",
    "decision_type",
    "decision_status",
    "decision_canonical_hash",
    "created_new_entry",
    "reused_existing_entry",
    "mutation_count",
    "decision_row_count_before",
    "decision_row_count_after",
    "exact_expected_entry_present",
    "conflicting_entry_present",
    "unrelated_entry_changed",
    "append_only_verified",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_changed",
    "production_case_changed",
    "downstream_runtime_called",
    "correction_or_revocation_performed",
    "deleted_or_updated",
    "warnings",
    "blockers",
)
RECEIPT_OUTCOMES = (
    "created_exactly_one_human_review_decision",
    "already_exists_same_human_review_decision",
    "blocked_unsupported_decision_type",
    "blocked_binding_or_snapshot_mismatch",
    "blocked_idempotency_conflict",
    "paused_pending_read_only_idempotency_verification",
    "bounded_decision_ledger_failure",
)
ALLOWED_FOLLOW_UP_LABELS = DECISION_TYPES
BLOCKED_FOLLOW_UP_LABELS = (
    "trust_approval_blocked",
    "automatic_trust_upgrade_blocked",
    "governed_record_mutation_blocked",
    "production_review_queue_blocked",
    "production_promotion_blocked",
    "analysis_trigger_blocked",
    "report_generation_blocked",
    "correction_or_revocation_execution_blocked",
    "delete_or_reset_blocked",
    "public_delivery_blocked",
)
SERVER_OWNED_CONTEXT = {
    "source_projection_schema": (
        "sentigraph_internal_alpha_governed_nonproduction_"
        "record_review_projection_v0_1"
    ),
    "source_projection_version": "0.1",
    "source_projection_id": "governed-nonproduction-record-review-v0-1",
    "source_projection_status": "governed_record_review_ready",
    "source_projection_canonical_sha256": (
        "0b9dc55caf3a375b1c5c4c2b66d851c1e192807fb0fd5259fcab77c32a74575f"
    ),
    "source_outer_response_canonical_sha256": (
        "9163797b7aa4ec5506ebbab00d1180451b5631a32c6f3a236c4127526366e110"
    ),
    "reviewer_role_label": "self_declared_project_owner_role",
    "reviewer_authority_basis_label": (
        "authority_basis_not_independently_validated"
    ),
    "reviewer_identity_verified": False,
    "persisted_record_id": "gnpepr-c886bd087e84dceff806e748d2f2ceaf",
    "attempt_reservation_id": (
        "gnpepr-attempt-34d95623c3678bdd63430d97fdc7d922"
    ),
    "candidate_identity_digest": (
        "078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54"
    ),
    "input_safe_hash": (
        "71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5"
    ),
    "gate_contract_safe_hash": (
        "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
    ),
    "activation_decision_safe_hash": (
        "e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d"
    ),
    "record_snapshot_digest": (
        "eda50fc437940ac519881638d76fa0443481fc9fda8f50cf62805be0d83baf20"
    ),
    "reservation_snapshot_digest": (
        "076584df7f9d712b78e9c3e5dee06cc55ff817487084074e34824bd9185f7a6c"
    ),
}
POST_RESPONSE_FIELDS = (
    "response_schema",
    "route_mode",
    "decision_id",
    "decision",
    "receipt",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "decision_ledger_write_performed",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "operator_runtime_ready",
    "public_ready",
    "production_ready",
)
GET_RESPONSE_FIELDS = (
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
OUTCOME_STATUS = {
    "created_exactly_one_human_review_decision": 201,
    "already_exists_same_human_review_decision": 200,
    "blocked_unsupported_decision_type": 422,
    "blocked_binding_or_snapshot_mismatch": 409,
    "blocked_idempotency_conflict": 409,
    "paused_pending_read_only_idempotency_verification": 503,
    "bounded_decision_ledger_failure": 500,
}
FORMAL_TARGET = Path(
    "runtime/governed_nonproduction_human_review_decisions/"
    "review_decisions_v0_1.sqlite3"
)


def _service():
    return importlib.import_module(SERVICE_MODULE)


def _route():
    return importlib.import_module(ROUTE_MODULE)


def _request(decision_type: str = DECISION_TYPES[0]) -> dict[str, str]:
    return {
        "request_schema": REQUEST_SCHEMA,
        "request_version": REQUEST_VERSION,
        "decision_type": decision_type,
    }


class CountingClock:
    def __init__(self, *values: str) -> None:
        self.values = values or ("2026-07-14T12:00:00Z",)
        self.calls = 0

    def __call__(self) -> str:
        value = self.values[min(self.calls, len(self.values) - 1)]
        self.calls += 1
        return value


def _initialized_ledger(
    module,
    tmp_path: Path,
    *,
    clock: CountingClock | None = None,
    before_commit_hook=None,
    after_commit_hook=None,
):
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        database_path=tmp_path / "synthetic-human-review-decisions.sqlite3",
        enabled=True,
        clock=clock or CountingClock(),
        before_commit_hook=before_commit_hook,
        after_commit_hook=after_commit_hook,
    )
    ledger.initialize()
    return ledger


def _record(module, ledger, request: dict[str, Any] | None = None):
    return module.record_governed_nonproduction_human_review_decision(
        ledger,
        request or _request(),
    )


def _row_count(ledger, table: str) -> int:
    with sqlite3.connect(ledger.database_path) as connection:
        return connection.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]


def _assert_false_boundaries(value: dict[str, Any]) -> None:
    assert value["human_review_required"] is True
    assert value["no_automatic_trust_upgrade"] is True
    assert value["production_evidenceitem_changed"] is False
    assert value["production_case_changed"] is False
    assert value["downstream_runtime_called"] is False
    assert value["correction_or_revocation_performed"] is False
    assert value["deleted_or_updated"] is False


def test_existing_f10_review_console_route_remains_separate_get_only() -> None:
    source = Path(
        "backend/app/api/v1/routes/internal_alpha_review_console.py"
    ).read_text(encoding="utf-8")
    assert '@router.get("/projections/{projection_id}")' in source
    assert "governed-review-decisions" not in source
    assert '@router.post("/decisions")' not in source


def test_formal_runtime_ledger_target_is_absent() -> None:
    assert not FORMAL_TARGET.exists()


def test_service_exposes_exact_contract_constants_and_public_surface() -> None:
    module = _service()
    assert module.REQUEST_SCHEMA == REQUEST_SCHEMA
    assert module.REQUEST_VERSION == REQUEST_VERSION
    assert module.REQUEST_FIELDS == REQUEST_FIELDS
    assert module.DECISION_TYPES == DECISION_TYPES
    assert module.DECISION_SCHEMA == DECISION_SCHEMA
    assert module.DECISION_VERSION == DECISION_VERSION
    assert module.DECISION_FIELDS == DECISION_FIELDS
    assert module.RECEIPT_SCHEMA == RECEIPT_SCHEMA
    assert module.RECEIPT_VERSION == RECEIPT_VERSION
    assert module.RECEIPT_FIELDS == RECEIPT_FIELDS
    assert module.RECEIPT_OUTCOMES == RECEIPT_OUTCOMES
    assert module.ALLOWED_FOLLOW_UP_LABELS == ALLOWED_FOLLOW_UP_LABELS
    assert module.BLOCKED_FOLLOW_UP_LABELS == BLOCKED_FOLLOW_UP_LABELS
    assert dict(module.SERVER_OWNED_CONTEXT) == SERVER_OWNED_CONTEXT
    assert len(module.REQUEST_FIELDS) == len(set(module.REQUEST_FIELDS)) == 3
    assert len(module.DECISION_FIELDS) == len(set(module.DECISION_FIELDS)) == 38
    assert len(module.RECEIPT_FIELDS) == len(set(module.RECEIPT_FIELDS)) == 27
    assert len(module.RECEIPT_OUTCOMES) == len(set(module.RECEIPT_OUTCOMES)) == 7
    assert module.LOGICAL_TARGET_LABEL == FORMAL_TARGET.as_posix()
    assert module.PRIMARY_TABLE == (
        "governed_nonproduction_human_review_decisions_v0_1"
    )
    assert callable(module.GovernedNonproductionHumanReviewDecisionLedger)
    assert callable(module.record_governed_nonproduction_human_review_decision)
    assert callable(module.get_governed_nonproduction_human_review_decision)
    assert callable(
        module.validate_governed_nonproduction_human_review_decision_request
    )


@pytest.mark.parametrize("decision_type", DECISION_TYPES)
def test_request_validation_accepts_exact_two_decision_types(
    decision_type: str,
) -> None:
    module = _service()
    validated = (
        module.validate_governed_nonproduction_human_review_decision_request(
            _request(decision_type)
        )
    )
    assert tuple(validated) == REQUEST_FIELDS
    assert validated == _request(decision_type)


@pytest.mark.parametrize(
    ("request_payload", "outcome"),
    (
        ({"request_schema": REQUEST_SCHEMA, "request_version": REQUEST_VERSION}, "blocked_binding_or_snapshot_mismatch"),
        ({**_request(), "note": "free text"}, "blocked_binding_or_snapshot_mismatch"),
        ({**_request(), "persisted_record_id": "client-value"}, "blocked_binding_or_snapshot_mismatch"),
        ({"request_schema": REQUEST_SCHEMA, "request_version": REQUEST_VERSION, "decision_type": 1}, "blocked_binding_or_snapshot_mismatch"),
        ({"request_schema": REQUEST_SCHEMA, "request_version": REQUEST_VERSION, "decision_type": True}, "blocked_binding_or_snapshot_mismatch"),
        ({"request_schema": "wrong", "request_version": REQUEST_VERSION, "decision_type": DECISION_TYPES[0]}, "blocked_binding_or_snapshot_mismatch"),
        ({"request_schema": REQUEST_SCHEMA, "request_version": "9", "decision_type": DECISION_TYPES[0]}, "blocked_binding_or_snapshot_mismatch"),
        ({"decision_type": DECISION_TYPES[0], "request_version": REQUEST_VERSION, "request_schema": REQUEST_SCHEMA}, "blocked_binding_or_snapshot_mismatch"),
        ({"request_schema": REQUEST_SCHEMA, "request_version": REQUEST_VERSION, "decision_type": "approve_trust"}, "blocked_unsupported_decision_type"),
    ),
)
def test_request_validation_rejects_invalid_shapes_types_bindings_and_values(
    request_payload: dict[str, Any],
    outcome: str,
) -> None:
    module = _service()
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionValidationError
    ) as exc_info:
        module.validate_governed_nonproduction_human_review_decision_request(
            request_payload
        )
    assert exc_info.value.outcome == outcome


def test_invalid_request_opens_no_sqlite_and_acquires_no_clock(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    clock = CountingClock()
    database_path = tmp_path / "must-not-open.sqlite3"
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        database_path=database_path,
        enabled=True,
        clock=clock,
    )
    connect_calls = 0

    def fail_connect(*_args, **_kwargs):
        nonlocal connect_calls
        connect_calls += 1
        raise AssertionError("SQLite must remain unopened")

    monkeypatch.setattr(module.sqlite3, "connect", fail_connect)
    decision, receipt = _record(
        module,
        ledger,
        {**_request(), "note": "not accepted"},
    )
    assert decision is None
    assert tuple(receipt) == RECEIPT_FIELDS
    assert receipt["outcome"] == "blocked_binding_or_snapshot_mismatch"
    assert receipt["mutation_count"] == 0
    assert connect_calls == 0
    assert clock.calls == 0
    assert not database_path.exists()


def test_server_owned_context_mismatch_blocks_before_clock_or_sqlite(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    clock = CountingClock()
    database_path = tmp_path / "must-not-open.sqlite3"
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        database_path=database_path,
        enabled=True,
        clock=clock,
    )
    altered = dict(module.SERVER_OWNED_CONTEXT)
    altered["source_projection_status"] = "not-ready"
    monkeypatch.setattr(module, "SERVER_OWNED_CONTEXT", altered)

    def fail_connect(*_args, **_kwargs):
        raise AssertionError("SQLite must remain unopened")

    monkeypatch.setattr(module.sqlite3, "connect", fail_connect)
    decision, receipt = _record(module, ledger)
    assert decision is None
    assert receipt["outcome"] == "blocked_binding_or_snapshot_mismatch"
    assert receipt["mutation_count"] == 0
    assert clock.calls == 0
    assert not database_path.exists()


def test_store_defaults_disabled_and_enabled_requires_explicit_test_path(
    tmp_path: Path,
) -> None:
    module = _service()
    disabled_path = tmp_path / "disabled.sqlite3"
    disabled = module.GovernedNonproductionHumanReviewDecisionLedger(
        database_path=disabled_path
    )
    assert disabled.enabled is False
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        disabled.initialize()
    assert not disabled_path.exists()

    no_path = module.GovernedNonproductionHumanReviewDecisionLedger(enabled=True)
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        no_path.initialize()


def test_formal_target_is_rejected_without_sqlite_open(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    connect_calls = 0

    def fail_connect(*_args, **_kwargs):
        nonlocal connect_calls
        connect_calls += 1
        raise AssertionError("Formal target must remain unopened")

    monkeypatch.setattr(module.sqlite3, "connect", fail_connect)
    ledger = module.GovernedNonproductionHumanReviewDecisionLedger(
        database_path=Path(module.LOGICAL_TARGET_LABEL),
        enabled=True,
    )
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        ledger.initialize()
    assert connect_calls == 0
    assert not FORMAL_TARGET.exists()


def test_initialization_creates_exact_table_columns_and_unique_constraints(
    tmp_path: Path,
) -> None:
    module = _service()
    ledger = _initialized_ledger(module, tmp_path)
    with sqlite3.connect(ledger.database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert tables == {module.PRIMARY_TABLE}
        columns = tuple(
            row[1]
            for row in connection.execute(
                f'PRAGMA table_info("{module.PRIMARY_TABLE}")'
            )
        )
        assert columns == DECISION_FIELDS
        index_rows = list(
            connection.execute(f'PRAGMA index_list("{module.PRIMARY_TABLE}")')
        )
        assert sum(bool(row[2]) for row in index_rows) >= 2


def test_new_decision_builds_exact_record_and_receipt(tmp_path: Path) -> None:
    module = _service()
    clock = CountingClock("2026-07-14T12:34:56Z")
    ledger = _initialized_ledger(module, tmp_path, clock=clock)
    decision, receipt = _record(module, ledger)

    assert tuple(decision) == DECISION_FIELDS
    assert tuple(receipt) == RECEIPT_FIELDS
    assert decision["decision_schema"] == DECISION_SCHEMA
    assert decision["decision_version"] == DECISION_VERSION
    assert decision["decision_type"] == DECISION_TYPES[0]
    assert decision["recorded_at"] == "2026-07-14T12:34:56Z"
    assert re.fullmatch(r"ghrd-[0-9a-f]{32}", decision["decision_id"])
    assert re.fullmatch(r"[0-9a-f]{64}", decision["idempotency_key"])
    assert re.fullmatch(
        r"ghrd-receipt-[0-9a-f]{32}",
        decision["audit_receipt_reference"],
    )
    assert re.fullmatch(r"[0-9a-f]{64}", decision["decision_canonical_hash"])
    assert decision["allowed_follow_up_labels"] == list(ALLOWED_FOLLOW_UP_LABELS)
    assert decision["blocked_follow_up_labels"] == list(BLOCKED_FOLLOW_UP_LABELS)
    assert decision["warnings"] == []
    assert decision["blockers"] == []
    _assert_false_boundaries(decision)
    assert receipt["outcome"] == "created_exactly_one_human_review_decision"
    assert receipt["created_new_entry"] is True
    assert receipt["reused_existing_entry"] is False
    assert receipt["mutation_count"] == 1
    assert receipt["decision_row_count_before"] == 0
    assert receipt["decision_row_count_after"] == 1
    assert receipt["exact_expected_entry_present"] is True
    assert receipt["conflicting_entry_present"] is False
    assert receipt["unrelated_entry_changed"] is False
    assert receipt["append_only_verified"] is True
    _assert_false_boundaries(receipt)
    assert clock.calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 1


def test_idempotent_reuse_returns_exact_record_without_new_clock_or_mutation(
    tmp_path: Path,
) -> None:
    module = _service()
    clock = CountingClock(
        "2026-07-14T12:00:00Z",
        "2026-07-14T13:00:00Z",
    )
    ledger = _initialized_ledger(module, tmp_path, clock=clock)
    first_decision, first_receipt = _record(module, ledger)
    second_decision, second_receipt = _record(module, ledger)

    assert first_receipt["mutation_count"] == 1
    assert second_decision == first_decision
    assert second_receipt["outcome"] == (
        "already_exists_same_human_review_decision"
    )
    assert second_receipt["created_new_entry"] is False
    assert second_receipt["reused_existing_entry"] is True
    assert second_receipt["mutation_count"] == 0
    assert second_receipt["decision_row_count_before"] == 1
    assert second_receipt["decision_row_count_after"] == 1
    assert clock.calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 1


def test_recorded_at_is_excluded_from_idempotency_and_included_in_decision_hash(
    tmp_path: Path,
) -> None:
    module = _service()
    first = _initialized_ledger(
        module,
        tmp_path / "one",
        clock=CountingClock("2026-07-14T12:00:00Z"),
    )
    second = _initialized_ledger(
        module,
        tmp_path / "two",
        clock=CountingClock("2026-07-14T13:00:00Z"),
    )
    first_decision, _ = _record(module, first)
    second_decision, _ = _record(module, second)
    assert first_decision["idempotency_key"] == second_decision["idempotency_key"]
    assert first_decision["decision_id"] == second_decision["decision_id"]
    assert first_decision["audit_receipt_reference"] == (
        second_decision["audit_receipt_reference"]
    )
    assert first_decision["recorded_at"] != second_decision["recorded_at"]
    assert first_decision["decision_canonical_hash"] != (
        second_decision["decision_canonical_hash"]
    )


def test_other_allowed_decision_appends_distinct_record_without_changing_first(
    tmp_path: Path,
) -> None:
    module = _service()
    ledger = _initialized_ledger(module, tmp_path)
    first, _ = _record(module, ledger, _request(DECISION_TYPES[0]))
    second, receipt = _record(module, ledger, _request(DECISION_TYPES[1]))
    reloaded = module.get_governed_nonproduction_human_review_decision(
        ledger,
        first["decision_id"],
    )
    assert second["decision_id"] != first["decision_id"]
    assert second["idempotency_key"] != first["idempotency_key"]
    assert receipt["outcome"] == "created_exactly_one_human_review_decision"
    assert receipt["decision_row_count_before"] == 1
    assert receipt["decision_row_count_after"] == 2
    assert receipt["unrelated_entry_changed"] is False
    assert reloaded == first
    assert _row_count(ledger, module.PRIMARY_TABLE) == 2


def test_actual_column_readback_recomputes_hash_and_parses_ordered_arrays(
    tmp_path: Path,
) -> None:
    module = _service()
    ledger = _initialized_ledger(module, tmp_path)
    decision, _ = _record(module, ledger)
    loaded = module.get_governed_nonproduction_human_review_decision(
        ledger,
        decision["decision_id"],
    )
    assert loaded == decision
    assert tuple(loaded) == DECISION_FIELDS
    assert loaded["allowed_follow_up_labels"] == list(ALLOWED_FOLLOW_UP_LABELS)
    assert loaded["blocked_follow_up_labels"] == list(BLOCKED_FOLLOW_UP_LABELS)


def test_stale_stored_hash_is_detected_and_same_request_conflicts(
    tmp_path: Path,
) -> None:
    module = _service()
    ledger = _initialized_ledger(module, tmp_path)
    decision, _ = _record(module, ledger)
    with sqlite3.connect(ledger.database_path) as connection:
        connection.execute(
            f'UPDATE "{module.PRIMARY_TABLE}" SET decision_canonical_hash = ? '
            "WHERE decision_id = ?",
            ("0" * 64, decision["decision_id"]),
        )
        connection.commit()
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionIntegrityError
    ):
        module.get_governed_nonproduction_human_review_decision(
            ledger,
            decision["decision_id"],
        )
    conflicting_decision, receipt = _record(module, ledger)
    assert conflicting_decision is None
    assert receipt["outcome"] == "blocked_idempotency_conflict"
    assert receipt["mutation_count"] == 0
    assert receipt["conflicting_entry_present"] is True


def test_malformed_canonical_json_is_detected(tmp_path: Path) -> None:
    module = _service()
    ledger = _initialized_ledger(module, tmp_path)
    decision, _ = _record(module, ledger)
    with sqlite3.connect(ledger.database_path) as connection:
        connection.execute(
            f'UPDATE "{module.PRIMARY_TABLE}" '
            "SET allowed_follow_up_labels = ? WHERE decision_id = ?",
            ("not-json", decision["decision_id"]),
        )
        connection.commit()
    with pytest.raises(
        module.GovernedNonproductionHumanReviewDecisionIntegrityError
    ):
        module.get_governed_nonproduction_human_review_decision(
            ledger,
            decision["decision_id"],
        )


def test_known_precommit_failure_rolls_back_without_retry_or_raw_error(
    tmp_path: Path,
) -> None:
    module = _service()
    hook_calls = 0

    def fail_before_commit() -> None:
        nonlocal hook_calls
        hook_calls += 1
        raise RuntimeError("private synthetic detail")

    ledger = _initialized_ledger(
        module,
        tmp_path,
        before_commit_hook=fail_before_commit,
    )
    decision, receipt = _record(module, ledger)
    assert decision is None
    assert receipt["outcome"] == "bounded_decision_ledger_failure"
    assert receipt["mutation_count"] == 0
    assert receipt["created_new_entry"] is False
    assert receipt["reused_existing_entry"] is False
    assert hook_calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 0
    rendered = json.dumps(receipt, sort_keys=True)
    assert "private synthetic detail" not in rendered
    assert str(tmp_path) not in rendered


def test_commit_ambiguity_exact_row_resolution_uses_one_insert(
    tmp_path: Path,
) -> None:
    module = _service()
    hook_calls = 0

    def ambiguous_after_commit() -> None:
        nonlocal hook_calls
        hook_calls += 1
        raise module.GovernedNonproductionHumanReviewDecisionCommitAmbiguity()

    ledger = _initialized_ledger(
        module,
        tmp_path,
        after_commit_hook=ambiguous_after_commit,
    )
    insert_calls = 0
    original_insert = ledger._insert_record

    def counted_insert(*args, **kwargs):
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    ledger._insert_record = counted_insert
    decision, receipt = _record(module, ledger)
    assert decision is not None
    assert receipt["outcome"] == "created_exactly_one_human_review_decision"
    assert receipt["mutation_count"] == 1
    assert hook_calls == 1
    assert insert_calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 1


def test_commit_ambiguity_mismatch_returns_conflict_without_second_insert(
    tmp_path: Path,
) -> None:
    module = _service()
    database_path = tmp_path / "synthetic-human-review-decisions.sqlite3"

    def corrupt_then_ambiguous() -> None:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                f'UPDATE "{module.PRIMARY_TABLE}" '
                "SET decision_canonical_hash = ?",
                ("f" * 64,),
            )
            connection.commit()
        raise module.GovernedNonproductionHumanReviewDecisionCommitAmbiguity()

    ledger = _initialized_ledger(
        module,
        tmp_path,
        after_commit_hook=corrupt_then_ambiguous,
    )
    insert_calls = 0
    original_insert = ledger._insert_record

    def counted_insert(*args, **kwargs):
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    ledger._insert_record = counted_insert
    decision, receipt = _record(module, ledger)
    assert decision is None
    assert receipt["outcome"] == "blocked_idempotency_conflict"
    assert receipt["mutation_count"] == 0
    assert receipt["conflicting_entry_present"] is True
    assert insert_calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 1


def test_commit_ambiguity_unresolved_pauses_without_second_insert(
    tmp_path: Path,
) -> None:
    module = _service()
    database_path = tmp_path / "synthetic-human-review-decisions.sqlite3"

    def remove_then_ambiguous() -> None:
        database_path.unlink()
        raise module.GovernedNonproductionHumanReviewDecisionCommitAmbiguity()

    ledger = _initialized_ledger(
        module,
        tmp_path,
        after_commit_hook=remove_then_ambiguous,
    )
    insert_calls = 0
    original_insert = ledger._insert_record

    def counted_insert(*args, **kwargs):
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    ledger._insert_record = counted_insert
    decision, receipt = _record(module, ledger)
    assert decision is None
    assert receipt["outcome"] == (
        "paused_pending_read_only_idempotency_verification"
    )
    assert receipt["mutation_count"] == 0
    assert receipt["append_only_verified"] is False
    assert insert_calls == 1


def test_receipt_outcome_invariant_matrix_is_exact() -> None:
    module = _service()
    expected = {
        "created_exactly_one_human_review_decision": (True, False, 1, True, False, True),
        "already_exists_same_human_review_decision": (False, True, 0, True, False, True),
        "blocked_unsupported_decision_type": (False, False, 0, False, False, True),
        "blocked_binding_or_snapshot_mismatch": (False, False, 0, False, False, True),
        "blocked_idempotency_conflict": (False, False, 0, False, True, True),
        "paused_pending_read_only_idempotency_verification": (False, False, 0, False, False, False),
        "bounded_decision_ledger_failure": (False, False, 0, False, False, False),
    }
    assert module.RECEIPT_OUTCOME_INVARIANTS == expected


def test_service_source_is_append_only_isolated_and_has_one_insert() -> None:
    module = _service()
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
    assert source.upper().count("INSERT INTO") == 1
    for pattern in (
        r"\bUPDATE\s+",
        r"\bDELETE\s+FROM\b",
        r"\bREPLACE\s+INTO\b",
        r"INSERT\s+OR\s+REPLACE",
        r"ON\s+CONFLICT\s+DO\s+UPDATE",
    ):
        assert re.search(pattern, source, flags=re.IGNORECASE) is None
    assert "subprocess" not in imported
    assert "requests" not in imported
    assert "httpx" not in imported
    assert "governed_nonproduction_review_console_projection" not in source
    assert "governed_nonproduction_exact_target" not in source
    assert "governed_nonproduction_evidence_persistence" not in source
    assert "os.environ" not in source
    assert "glob(" not in source
    assert "rglob(" not in source


def test_route_request_model_is_strict_ordered_and_extra_forbidden() -> None:
    route = _route()
    model = route.GovernedNonproductionHumanReviewDecisionRequest
    assert tuple(model.model_fields) == REQUEST_FIELDS
    validated = model(**_request())
    assert tuple(validated.model_dump()) == REQUEST_FIELDS
    with pytest.raises(ValidationError):
        model(**{**_request(), "note": "not allowed"})
    with pytest.raises(ValidationError):
        model(
            request_schema=REQUEST_SCHEMA,
            request_version=REQUEST_VERSION,
            decision_type=1,
        )


def test_gate_disabled_constructs_no_ledger_and_returns_safe_posture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    route = _route()
    monkeypatch.delenv(GATE, raising=False)
    factory_calls = 0

    def forbidden_factory():
        nonlocal factory_calls
        factory_calls += 1
        raise AssertionError("disabled route must not construct a ledger")

    monkeypatch.setattr(route, "_ledger_factory", forbidden_factory)
    from app.main import app

    response = TestClient(app).post(f"{ROUTE_PREFIX}/decisions", json=_request())
    assert response.status_code == 404
    body = response.json()
    assert tuple(body) == POST_RESPONSE_FIELDS
    assert body["decision"] is None
    assert body["receipt"] is None
    assert body["decision_ledger_write_performed"] is False
    assert factory_calls == 0


def test_gate_enabled_default_factory_opens_no_sqlite(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    route = _route()
    monkeypatch.setenv(GATE, "1")
    connect_calls = 0

    def fail_connect(*_args, **_kwargs):
        nonlocal connect_calls
        connect_calls += 1
        raise AssertionError("default route factory must not open SQLite")

    monkeypatch.setattr(module.sqlite3, "connect", fail_connect)
    from app.main import app

    response = TestClient(app).post(f"{ROUTE_PREFIX}/decisions", json=_request())
    assert response.status_code == 503
    assert response.json()["decision"] is None
    assert response.json()["receipt"] is None
    assert connect_calls == 0


def test_injected_route_post_create_reuse_and_exact_get(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    route = _route()
    ledger = _initialized_ledger(module, tmp_path)
    monkeypatch.setenv(GATE, "true")
    monkeypatch.setattr(route, "_ledger_factory", lambda: ledger)
    from app.main import app

    client = TestClient(app)
    created = client.post(f"{ROUTE_PREFIX}/decisions", json=_request())
    assert created.status_code == 201
    created_body = created.json()
    assert tuple(created_body) == POST_RESPONSE_FIELDS
    assert created_body["response_schema"] == (
        "sentigraph_internal_alpha_governed_review_decision_"
        "post_response_v0_1"
    )
    assert created_body["receipt"]["outcome"] == (
        "created_exactly_one_human_review_decision"
    )
    assert created_body["decision_ledger_write_performed"] is True

    reused = client.post(f"{ROUTE_PREFIX}/decisions", json=_request())
    assert reused.status_code == 200
    assert reused.json()["decision"] == created_body["decision"]
    assert reused.json()["receipt"]["outcome"] == (
        "already_exists_same_human_review_decision"
    )
    assert reused.json()["decision_ledger_write_performed"] is False

    decision_id = created_body["decision_id"]
    fetched = client.get(f"{ROUTE_PREFIX}/decisions/{decision_id}")
    assert fetched.status_code == 200
    assert tuple(fetched.json()) == GET_RESPONSE_FIELDS
    assert fetched.json()["decision"] == created_body["decision"]
    assert "receipt" not in fetched.json()


def test_route_unsupported_decision_status_and_false_runtime_flags(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    route = _route()
    ledger = _initialized_ledger(module, tmp_path)
    monkeypatch.setenv(GATE, "yes")
    monkeypatch.setattr(route, "_ledger_factory", lambda: ledger)
    from app.main import app

    response = TestClient(app).post(
        f"{ROUTE_PREFIX}/decisions",
        json=_request("approve_trust"),
    )
    assert response.status_code == 422
    body = response.json()
    assert tuple(body) == POST_RESPONSE_FIELDS
    assert body["receipt"]["outcome"] == "blocked_unsupported_decision_type"
    assert body["decision"] is None
    assert body["decision_ledger_write_performed"] is False
    for field in (
        "production_object_enabled",
        "review_queue_runtime_enabled",
        "operator_runtime_ready",
        "public_ready",
        "production_ready",
    ):
        assert body[field] is False


def test_malformed_and_unknown_get_fail_closed_without_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    route = _route()
    ledger = _initialized_ledger(module, tmp_path)
    monkeypatch.setenv(GATE, "on")
    factory_calls = 0

    def factory():
        nonlocal factory_calls
        factory_calls += 1
        return ledger

    monkeypatch.setattr(route, "_ledger_factory", factory)
    from app.main import app

    client = TestClient(app)
    malformed = client.get(f"{ROUTE_PREFIX}/decisions/not-an-id")
    assert malformed.status_code == 422
    assert malformed.json()["decision"] is None
    assert factory_calls == 0

    unknown = client.get(f"{ROUTE_PREFIX}/decisions/ghrd-{'0' * 32}")
    assert unknown.status_code == 404
    assert tuple(unknown.json()) == GET_RESPONSE_FIELDS
    assert unknown.json()["decision"] is None
    assert factory_calls == 1
    assert _row_count(ledger, module.PRIMARY_TABLE) == 0


def test_route_surface_and_api_registration_are_exact() -> None:
    route = _route()
    assert route.OUTCOME_STATUS == OUTCOME_STATUS
    source = inspect.getsource(route)
    assert '@router.post("/decisions")' in source
    assert '@router.get("/decisions/{decision_id}")' in source
    for forbidden in (
        '@router.get("/decisions")',
        "@router.put",
        "@router.patch",
        "@router.delete",
        "retry",
        "download",
        "FileResponse",
    ):
        assert forbidden not in source
    api_source = Path("backend/app/api/v1/api.py").read_text(encoding="utf-8")
    assert "internal_alpha_governed_review_decisions," in api_source
    assert "internal_alpha_governed_review_decisions.router" in api_source
    assert 'prefix="/internal/alpha/governed-review-decisions"' in api_source
    assert api_source.count("internal_alpha_governed_review_decisions.router") == 1


def test_registered_app_exposes_only_post_and_exact_id_get_for_new_family() -> None:
    from app.main import app

    family_routes = [
        route
        for route in app.routes
        if getattr(route, "path", "").startswith(ROUTE_PREFIX)
    ]
    assert {(route.path, tuple(sorted(route.methods))) for route in family_routes} == {
        (f"{ROUTE_PREFIX}/decisions", ("POST",)),
        (f"{ROUTE_PREFIX}/decisions/{{decision_id}}", ("GET",)),
    }


def test_receipts_and_route_responses_expose_no_path_sql_error_or_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = _service()
    route = _route()
    ledger = _initialized_ledger(module, tmp_path)
    monkeypatch.setenv(GATE, "1")
    monkeypatch.setattr(route, "_ledger_factory", lambda: ledger)
    from app.main import app

    body = TestClient(app).post(
        f"{ROUTE_PREFIX}/decisions",
        json=_request(),
    ).json()
    rendered = json.dumps(body, ensure_ascii=False, sort_keys=True)
    assert str(tmp_path) not in rendered
    for forbidden in (
        "SELECT ",
        "INSERT ",
        "UPDATE ",
        "DELETE ",
        "Traceback",
        "Exception",
        "reviewer_name",
        "reviewer_email",
        "password",
        "secret",
    ):
        assert forbidden not in rendered
    assert body["production_object_enabled"] is False
    assert body["review_queue_runtime_enabled"] is False
    assert body["operator_runtime_ready"] is False
    assert body["public_ready"] is False
    assert body["production_ready"] is False
