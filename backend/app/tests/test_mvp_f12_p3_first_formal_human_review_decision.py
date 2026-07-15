from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from backend.app.services import (
    governed_nonproduction_human_review_decision_ledger as ledger_module,
)
from backend.app.services.governed_nonproduction_human_review_decision_ledger import (
    GovernedNonproductionHumanReviewDecisionLedger,
    GovernedNonproductionHumanReviewDecisionLedgerUnavailable,
    record_first_exact_formal_human_review_decision,
)


EXPECTED_ACTIVATION_FIELDS = (
    "activation_schema",
    "activation_version",
    "milestone_id",
    "repository_identity",
    "required_branch",
    "starting_commit",
    "baseline_v1_4_blob",
    "accepted_f11_p1_contract_blob",
    "accepted_f11_p1_contract_sha256",
    "accepted_effective_f11_commit",
    "accepted_f11_decision_ledger_service_blob",
    "accepted_f12_p1_contract_blob",
    "accepted_f12_p1_contract_sha256",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "accepted_p2_service_blob",
    "accepted_p2_test_blob",
    "accepted_p2_report_blob",
    "accepted_p2_initialization_receipt_canonical_sha256",
    "required_formal_target_state",
    "accepted_decision_row_count",
    "first_real_decision_type",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
    "reviewer_identity_verified",
    "exact_p3_approval_sha256",
    "post_implementation_service_sha256",
    "post_implementation_test_sha256",
    "pre_execution_report_sha256",
    "repository_external_runner_sha256",
    "p3_activation_binding_nonreusable",
    "formal_target_access_session_limit",
    "sqlite_connection_open_success_limit",
    "sqlite_connection_reopen_success_limit",
    "formal_operation_invocation_limit",
    "decision_writer_invocation_limit",
    "decision_insert_limit",
    "route_invocation_limit",
    "f10_invocation_limit",
    "automatic_retry_allowed",
    "automatic_repair_allowed",
    "second_decision_allowed",
    "result_artifact_count_limit",
    "result_artifact_binary_read_limit",
    "result_artifact_read_max_bytes",
    "production_or_downstream_action_limit",
)
EXPECTED_PRE_WRITER_FIELDS = (
    "accepted_f11_p1_contract_blob",
    "accepted_f11_p1_contract_sha256",
    "accepted_effective_f11_commit",
    "accepted_decision_ledger_service_blob",
    "accepted_request_schema",
    "accepted_request_version",
    "accepted_decision_schema",
    "accepted_decision_version",
    "accepted_ledger_scope",
    "accepted_decision_status",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "independently_accepted_p2_initialization_receipt_canonical_sha256",
    "required_formal_target_state",
    "first_real_decision_type",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
    "reviewer_identity_verified",
    "p3_activation_binding_safe_hash",
    "p3_activation_binding_nonreusable",
    "formal_writer_invocation_limit",
    "automatic_retry_allowed",
    "route_invocation_limit",
)
EXPECTED_RESULT_FIELDS = (
    "result_schema",
    "result_version",
    "outcome",
    "p3_activation_binding_safe_hash",
    "p3_pre_writer_binding_canonical_sha256",
    "formal_state_before",
    "formal_state_after",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "accepted_p2_initialization_receipt_canonical_sha256",
    "formal_target_access_session_count",
    "sqlite_connection_open_count",
    "sqlite_connection_reopen_count",
    "formal_writer_invocation_count",
    "decision_insert_issued_count",
    "mutation_count",
    "decision_row_count_before",
    "decision_row_count_after",
    "exact_schema_verified",
    "integrity_result",
    "final_sidecar_count",
    "route_invocation_count",
    "f10_invocation_count",
    "decision",
    "receipt",
    "warnings",
    "blockers",
)
EXPECTED_IDEMPOTENCY_FIELDS = (
    "request_schema",
    "request_version",
    "decision_type",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def _build_case(tmp_path: Path) -> dict[str, Any]:
    root = tmp_path / "synthetic-repository"
    source_root = Path(__file__).resolve().parents[3]
    contract_relative = Path(ledger_module.FORMAL_CONTRACT_RELATIVE_PATH)
    _write(
        root / contract_relative,
        (source_root / contract_relative).read_bytes(),
    )
    service_path = root / Path(ledger_module.P3_SERVICE_RELATIVE_PATH)
    test_path = root / Path(ledger_module.P3_TEST_RELATIVE_PATH)
    report_path = root / Path(ledger_module.P3_REPORT_RELATIVE_PATH)
    _write(service_path, b"synthetic frozen service\n")
    _write(test_path, b"synthetic frozen test\n")
    _write(report_path, b"synthetic pre-execution report\n")
    target = root / Path(ledger_module.FORMAL_LOGICAL_TARGET_LABEL)
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(target) as connection:
        connection.execute(ledger_module.FORMAL_CREATE_TABLE_STATEMENT)
        connection.commit()
    runner_sha256 = hashlib.sha256(b"synthetic runner\n").hexdigest()
    activation_values = {
        **ledger_module._P3_FIXED_ACTIVATION_VALUES,
        "post_implementation_service_sha256": _sha256(service_path),
        "post_implementation_test_sha256": _sha256(test_path),
        "pre_execution_report_sha256": _sha256(report_path),
        "repository_external_runner_sha256": runner_sha256,
    }
    activation = {
        field: activation_values[field] for field in EXPECTED_ACTIVATION_FIELDS
    }
    activation_hash = _canonical_sha256(activation)
    pre_writer = ledger_module._p3_expected_pre_writer_binding(
        activation_hash
    )
    request = {
        "request_schema": ledger_module.REQUEST_SCHEMA,
        "request_version": ledger_module.REQUEST_VERSION,
        "decision_type": "keep_pending_human_review",
    }
    return {
        "root": root,
        "target": target,
        "service_path": service_path,
        "activation": activation,
        "activation_hash": activation_hash,
        "pre_writer": pre_writer,
        "pre_writer_hash": _canonical_sha256(pre_writer),
        "runner_sha256": runner_sha256,
        "request": request,
    }


def _call(case: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    values = {
        "repository_root": case["root"],
        "request": case["request"],
        "p3_activation_object": case["activation"],
        "p3_activation_binding_safe_hash": case["activation_hash"],
        "p3_pre_writer_binding": case["pre_writer"],
        "p3_pre_writer_binding_canonical_sha256": case[
            "pre_writer_hash"
        ],
        "runner_sha256": case["runner_sha256"],
        "enabled": True,
    }
    values.update(overrides)
    return record_first_exact_formal_human_review_decision(**values)


def _assert_zero_target_activity(result: dict[str, Any]) -> None:
    assert result["formal_target_access_session_count"] == 0
    assert result["sqlite_connection_open_count"] == 0
    assert result["sqlite_connection_reopen_count"] == 0
    assert result["formal_writer_invocation_count"] == 0
    assert result["decision_insert_issued_count"] == 0
    assert result["mutation_count"] == 0


def test_exact_p3_contract_fields_and_frozen_identity() -> None:
    assert callable(record_first_exact_formal_human_review_decision)
    assert ledger_module.P3_ACTIVATION_FIELDS == EXPECTED_ACTIVATION_FIELDS
    assert (
        ledger_module.P3_PRE_WRITER_BINDING_FIELDS
        == EXPECTED_PRE_WRITER_FIELDS
    )
    assert ledger_module.P3_RESULT_FIELDS == EXPECTED_RESULT_FIELDS
    assert ledger_module._IDEMPOTENCY_FIELDS == EXPECTED_IDEMPOTENCY_FIELDS
    assert (
        ledger_module.P3_ACTIVATION_SCHEMA
        == "sentigraph_mvp_f12_p3_first_exact_formal_human_review_decision_"
        "activation_v0_1"
    )
    assert (
        ledger_module.P3_RESULT_SCHEMA
        == "sentigraph_mvp_f12_p3_first_exact_formal_human_review_decision_"
        "result_v0_1"
    )
    assert ledger_module.P3_EXACT_APPROVAL_SHA256 == (
        "4ee5fcb567bbd3a43681cd3b90e95b8147a110df84862f365d749d8a82f78fd7"
    )
    identity_material = {
        "request_schema": ledger_module.REQUEST_SCHEMA,
        "request_version": ledger_module.REQUEST_VERSION,
        "decision_type": "keep_pending_human_review",
        **ledger_module.SERVER_OWNED_CONTEXT,
    }
    independently_computed_key = _canonical_sha256(
        {
            field: identity_material[field]
            for field in EXPECTED_IDEMPOTENCY_FIELDS
        }
    )
    identity = ledger_module._identity_for("keep_pending_human_review")
    assert identity["idempotency_key"] == independently_computed_key
    assert identity["idempotency_key"] == (
        "b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db"
    )
    assert identity["decision_id"] == (
        "ghrd-b666c0f03a975c94e6b3b248bd05cdc9"
    )
    assert identity["audit_receipt_reference"] == (
        "ghrd-receipt-b666c0f03a975c94e6b3b248bd05cdc9"
    )


def test_exact_success_records_one_append_only_decision(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    monkeypatch.setattr(
        ledger_module,
        "_utc_clock",
        lambda: "2026-07-15T00:00:00Z",
    )
    result = _call(case)
    assert tuple(result) == EXPECTED_RESULT_FIELDS
    assert result["outcome"] == "created_exactly_one_human_review_decision"
    assert result["formal_state_before"] == "initialized_exact_empty"
    assert result["formal_state_after"] == "first_exact_decision_recorded"
    assert result["formal_target_access_session_count"] == 1
    assert result["sqlite_connection_open_count"] == 1
    assert result["sqlite_connection_reopen_count"] == 0
    assert result["formal_writer_invocation_count"] == 1
    assert result["decision_insert_issued_count"] == 1
    assert result["mutation_count"] == 1
    assert result["decision_row_count_before"] == 0
    assert result["decision_row_count_after"] == 1
    assert result["exact_schema_verified"] is True
    assert result["integrity_result"] == "ok"
    assert result["final_sidecar_count"] == 0
    assert result["route_invocation_count"] == 0
    assert result["f10_invocation_count"] == 0
    assert tuple(result["decision"]) == ledger_module.DECISION_FIELDS
    assert tuple(result["receipt"]) == ledger_module.RECEIPT_FIELDS
    assert result["decision"]["recorded_at"] == "2026-07-15T00:00:00Z"
    assert result["decision"]["decision_type"] == "keep_pending_human_review"
    decision_hash_material = {
        field: result["decision"][field]
        for field in ledger_module.DECISION_FIELDS
        if field != "decision_canonical_hash"
    }
    assert result["decision"]["decision_canonical_hash"] == (
        _canonical_sha256(decision_hash_material)
    )
    assert result["receipt"]["mutation_count"] == 1
    assert result["receipt"]["decision_row_count_before"] == 0
    assert result["receipt"]["decision_row_count_after"] == 1
    assert result["warnings"] == []
    assert result["blockers"] == []
    with sqlite3.connect(case["target"]) as connection:
        assert ledger_module._row_count(connection) == 1
        stored = connection.execute(
            f'SELECT * FROM "{ledger_module.FORMAL_PRIMARY_TABLE}"'
        ).fetchone()
    assert ledger_module._row_to_decision(stored) == result["decision"]


def test_success_invokes_accepted_writer_exactly_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    calls = 0
    original = GovernedNonproductionHumanReviewDecisionLedger._insert_record

    def counted_writer(
        self: GovernedNonproductionHumanReviewDecisionLedger,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal calls
        calls += 1
        original(self, connection, decision)

    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_writer,
    )
    result = _call(case)
    assert result["outcome"] == "created_exactly_one_human_review_decision"
    assert calls == 1


def test_disabled_operation_stops_before_target_access(tmp_path: Path) -> None:
    case = _build_case(tmp_path)
    result = _call(case, enabled=False)
    assert result["outcome"] == "blocked_p3_formal_operation_disabled"
    _assert_zero_target_activity(result)


@pytest.mark.parametrize(
    "field,bad_value",
    (
        ("starting_commit", "0" * 40),
        ("accepted_decision_row_count", 1),
        ("accepted_decision_row_count", False),
        ("reviewer_identity_verified", True),
        ("reviewer_identity_verified", 0),
        ("p3_activation_binding_nonreusable", False),
        ("decision_insert_limit", 2),
        ("automatic_retry_allowed", True),
        ("second_decision_allowed", True),
        ("route_invocation_limit", 1),
    ),
)
def test_fixed_activation_mismatch_stops_before_target_access(
    tmp_path: Path,
    field: str,
    bad_value: Any,
) -> None:
    case = _build_case(tmp_path)
    activation = dict(case["activation"])
    activation[field] = bad_value
    result = _call(
        case,
        p3_activation_object=activation,
        p3_activation_binding_safe_hash=_canonical_sha256(activation),
    )
    assert result["outcome"] == "blocked_p3_activation_binding_mismatch"
    _assert_zero_target_activity(result)


def test_activation_order_hash_and_runner_gates_stop_before_access(
    tmp_path: Path,
) -> None:
    case = _build_case(tmp_path)
    reversed_activation = dict(reversed(tuple(case["activation"].items())))
    order_result = _call(
        case,
        p3_activation_object=reversed_activation,
        p3_activation_binding_safe_hash=_canonical_sha256(reversed_activation),
    )
    hash_result = _call(
        case,
        p3_activation_binding_safe_hash="0" * 64,
    )
    runner_result = _call(case, runner_sha256="1" * 64)
    for result in (order_result, hash_result, runner_result):
        assert result["outcome"] == "blocked_p3_activation_binding_mismatch"
        _assert_zero_target_activity(result)


def test_pre_writer_order_value_and_hash_gates_stop_before_access(
    tmp_path: Path,
) -> None:
    case = _build_case(tmp_path)
    reversed_binding = dict(reversed(tuple(case["pre_writer"].items())))
    wrong_value = dict(case["pre_writer"])
    wrong_value["formal_writer_invocation_limit"] = 2
    results = (
        _call(
            case,
            p3_pre_writer_binding=reversed_binding,
            p3_pre_writer_binding_canonical_sha256=_canonical_sha256(
                reversed_binding
            ),
        ),
        _call(
            case,
            p3_pre_writer_binding=wrong_value,
            p3_pre_writer_binding_canonical_sha256=_canonical_sha256(
                wrong_value
            ),
        ),
        _call(
            case,
            p3_pre_writer_binding_canonical_sha256="0" * 64,
        ),
    )
    for result in results:
        assert result["outcome"] == "blocked_p3_pre_writer_binding_mismatch"
        _assert_zero_target_activity(result)


def test_request_more_governance_review_is_not_a_first_decision(
    tmp_path: Path,
) -> None:
    case = _build_case(tmp_path)
    request = dict(case["request"])
    request["decision_type"] = "request_more_governance_review"
    result = _call(case, request=request)
    assert result["outcome"] == "blocked_p3_exact_request_mismatch"
    _assert_zero_target_activity(result)


def test_frozen_repository_file_mismatch_stops_before_sqlite_open(
    tmp_path: Path,
) -> None:
    case = _build_case(tmp_path)
    case["service_path"].write_bytes(b"changed after activation\n")
    result = _call(case)
    assert result["outcome"] == "blocked_p3_frozen_file_hash_mismatch"
    _assert_zero_target_activity(result)


def test_absent_or_nonempty_target_never_invokes_writer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    absent_case = _build_case(tmp_path / "absent")
    absent_case["target"].unlink()
    absent = _call(absent_case)
    assert absent["outcome"] == "blocked_p3_required_formal_state_mismatch"
    _assert_zero_target_activity(absent)

    nonempty_case = _build_case(tmp_path / "nonempty")
    identity = ledger_module._identity_for("keep_pending_human_review")
    decision = ledger_module._build_decision(
        identity,
        "2026-07-15T00:00:00Z",
    )
    with sqlite3.connect(nonempty_case["target"]) as connection:
        ledger = GovernedNonproductionHumanReviewDecisionLedger(
            nonempty_case["target"],
            enabled=True,
        )
        ledger._insert_record(connection, decision)
        connection.commit()

    def unexpected_writer(*_args: Any, **_kwargs: Any) -> None:
        pytest.fail("writer must not be invoked for a nonempty formal target")

    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        unexpected_writer,
    )
    nonempty = _call(nonempty_case)
    assert nonempty["outcome"] == "blocked_p3_required_formal_state_mismatch"
    assert nonempty["formal_target_access_session_count"] == 1
    assert nonempty["sqlite_connection_open_count"] == 1
    assert nonempty["formal_writer_invocation_count"] == 0
    assert nonempty["decision_insert_issued_count"] == 0
    assert nonempty["mutation_count"] == 0
    assert nonempty["decision_row_count_before"] == 1


def test_schema_mismatch_blocks_before_writer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    with sqlite3.connect(case["target"]) as connection:
        connection.execute('CREATE TABLE "unrelated" ("value" TEXT)')
        connection.commit()

    def unexpected_writer(*_args: Any, **_kwargs: Any) -> None:
        pytest.fail("writer must not be invoked for a schema mismatch")

    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        unexpected_writer,
    )
    result = _call(case)
    assert result["outcome"] == "blocked_p3_formal_schema_mismatch"
    assert result["formal_target_access_session_count"] == 1
    assert result["sqlite_connection_open_count"] == 1
    assert result["formal_writer_invocation_count"] == 0
    assert result["decision_insert_issued_count"] == 0


def test_commit_ambiguity_uses_same_connection_and_never_reinserts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    opens = 0
    writes = 0
    real_open = ledger_module._open_exact_formal_decision_ledger_connection
    real_write = GovernedNonproductionHumanReviewDecisionLedger._insert_record

    class CommitThenRaise:
        def __init__(self, connection: sqlite3.Connection) -> None:
            self.connection = connection

        def __getattr__(self, name: str) -> Any:
            return getattr(self.connection, name)

        def commit(self) -> None:
            self.connection.commit()
            raise sqlite3.OperationalError("synthetic ambiguity")

    def counted_open(path: Path, *, read_only: bool) -> CommitThenRaise:
        nonlocal opens
        opens += 1
        return CommitThenRaise(real_open(path, read_only=read_only))

    def counted_write(
        self: GovernedNonproductionHumanReviewDecisionLedger,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal writes
        writes += 1
        real_write(self, connection, decision)

    monkeypatch.setattr(
        ledger_module,
        "_open_exact_formal_decision_ledger_connection",
        counted_open,
    )
    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_write,
    )
    result = _call(case)
    assert result["outcome"] == "paused_p3_commit_outcome_ambiguous"
    assert opens == 1
    assert writes == 1
    assert result["sqlite_connection_open_count"] == 1
    assert result["sqlite_connection_reopen_count"] == 0
    assert result["decision_insert_issued_count"] == 1
    assert result["mutation_count"] == 1
    with sqlite3.connect(case["target"]) as connection:
        assert ledger_module._row_count(connection) == 1


def test_precommit_writer_failure_rolls_back_without_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    writes = 0
    real_write = GovernedNonproductionHumanReviewDecisionLedger._insert_record

    def write_then_fail(
        self: GovernedNonproductionHumanReviewDecisionLedger,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal writes
        writes += 1
        real_write(self, connection, decision)
        raise ValueError("synthetic precommit failure")

    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        write_then_fail,
    )
    result = _call(case)
    assert result["outcome"] == "bounded_p3_formal_writer_failure"
    assert writes == 1
    assert result["formal_writer_invocation_count"] == 1
    assert result["decision_insert_issued_count"] == 1
    assert result["mutation_count"] == 0
    assert result["decision_row_count_before"] == 0
    assert result["decision_row_count_after"] == 0
    assert result["decision"] is None
    assert result["receipt"] is None
    with sqlite3.connect(case["target"]) as connection:
        assert ledger_module._row_count(connection) == 0


def test_unresolved_commit_ambiguity_pauses_without_retry_or_second_insert(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _build_case(tmp_path)
    opens = 0
    writes = 0
    real_open = ledger_module._open_exact_formal_decision_ledger_connection
    real_write = GovernedNonproductionHumanReviewDecisionLedger._insert_record

    class RaiseBeforeCommit:
        def __init__(self, connection: sqlite3.Connection) -> None:
            self.connection = connection

        def __getattr__(self, name: str) -> Any:
            return getattr(self.connection, name)

        def commit(self) -> None:
            raise sqlite3.OperationalError("synthetic unresolved ambiguity")

    def counted_open(path: Path, *, read_only: bool) -> RaiseBeforeCommit:
        nonlocal opens
        opens += 1
        return RaiseBeforeCommit(real_open(path, read_only=read_only))

    def counted_write(
        self: GovernedNonproductionHumanReviewDecisionLedger,
        connection: sqlite3.Connection,
        decision: dict[str, Any],
    ) -> None:
        nonlocal writes
        writes += 1
        real_write(self, connection, decision)

    monkeypatch.setattr(
        ledger_module,
        "_open_exact_formal_decision_ledger_connection",
        counted_open,
    )
    monkeypatch.setattr(
        GovernedNonproductionHumanReviewDecisionLedger,
        "_insert_record",
        counted_write,
    )
    result = _call(case)
    assert result["outcome"] == "paused_p3_commit_outcome_ambiguous"
    assert opens == 1
    assert writes == 1
    assert result["sqlite_connection_open_count"] == 1
    assert result["sqlite_connection_reopen_count"] == 0
    assert result["formal_writer_invocation_count"] == 1
    assert result["decision_insert_issued_count"] == 1
    assert result["mutation_count"] == 0
    assert result["decision_row_count_after"] == 0
    with sqlite3.connect(case["target"]) as connection:
        assert ledger_module._row_count(connection) == 0


def test_generic_ledger_formal_target_guard_remains_frozen(
    tmp_path: Path,
) -> None:
    formal_target = tmp_path / Path(ledger_module.FORMAL_LOGICAL_TARGET_LABEL)
    ledger = GovernedNonproductionHumanReviewDecisionLedger(
        formal_target,
        enabled=True,
    )
    with pytest.raises(
        GovernedNonproductionHumanReviewDecisionLedgerUnavailable
    ):
        ledger._require_available()


def test_success_preserves_no_side_effect_boundaries(tmp_path: Path) -> None:
    case = _build_case(tmp_path)
    result = _call(case)
    decision = result["decision"]
    receipt = result["receipt"]
    for field in (
        "production_evidenceitem_changed",
        "production_case_changed",
        "downstream_runtime_called",
        "correction_or_revocation_performed",
        "deleted_or_updated",
    ):
        assert decision[field] is False
        assert receipt[field] is False
    assert decision["human_review_required"] is True
    assert decision["no_automatic_trust_upgrade"] is True
    assert receipt["human_review_required"] is True
    assert receipt["no_automatic_trust_upgrade"] is True
    assert "request_more_governance_review" in decision[
        "allowed_follow_up_labels"
    ]
    assert "production_promotion_blocked" in decision[
        "blocked_follow_up_labels"
    ]
    serialized = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert str(case["target"]) not in serialized
    assert ledger_module.FORMAL_LOGICAL_TARGET_LABEL not in serialized
    assert ".sqlite3" not in serialized
    assert "password" not in serialized.lower()
    assert "credential" not in serialized.lower()


def test_blocked_result_preserves_exact_null_and_counter_types(
    tmp_path: Path,
) -> None:
    result = _call(_build_case(tmp_path), enabled=False)
    assert tuple(result) == EXPECTED_RESULT_FIELDS
    assert result["decision"] is None
    assert result["receipt"] is None
    assert result["exact_schema_verified"] is None
    assert result["decision_row_count_before"] is None
    assert result["decision_row_count_after"] is None
    for field in (
        "formal_target_access_session_count",
        "sqlite_connection_open_count",
        "sqlite_connection_reopen_count",
        "formal_writer_invocation_count",
        "decision_insert_issued_count",
        "mutation_count",
        "route_invocation_count",
        "f10_invocation_count",
    ):
        assert type(result[field]) is int
        assert result[field] == 0
