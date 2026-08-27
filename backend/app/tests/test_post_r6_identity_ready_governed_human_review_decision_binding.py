from __future__ import annotations

import inspect
import json
import sqlite3
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.api.v1.routes import internal_alpha_governed_review_decisions as route_module
from app.services import (
    identity_ready_governed_nonproduction_human_review_decision_ledger as service,
)


SAFE_BINDING_HASH = "a" * 64
CURRENT_SAMPLE_HANDLE = "helldivers2-psn-demo"


def _candidate(
    decision_type: str = "keep_pending_human_review",
    **overrides: object,
) -> dict[str, object]:
    values: dict[str, object] = {
        "schema": (
            "sentigraph_internal_alpha_identity_ready_"
            "review_decision_candidate_v0_1"
        ),
        "mode": (
            "frontend_local_nonpersistent_governed_"
            "human_review_decision_candidate"
        ),
        "identity_schema": "sentigraph_b05_review_subject_identity_v0_1",
        "identity_version": "0.1",
        "identity_status": "ready",
        "sample_handle": CURRENT_SAMPLE_HANDLE,
        "review_subject_binding_safe_hash": SAFE_BINDING_HASH,
        "decision_type": decision_type,
        "candidate_only": True,
        "persisted": False,
        "trust_upgraded": False,
        "production_object": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }
    values.update(overrides)
    return values


def _request(
    decision_type: str = "keep_pending_human_review",
    **candidate_overrides: object,
) -> dict[str, object]:
    return {
        "request_schema": (
            "sentigraph_internal_alpha_identity_ready_governed_"
            "review_decision_binding_request_v0_1"
        ),
        "request_version": "0.1",
        "candidate": _candidate(decision_type, **candidate_overrides),
    }


def _ledger(
    tmp_path: Path,
    *,
    before_commit_hook=None,
    after_commit_hook=None,
) -> service.IdentityReadyGovernedNonproductionHumanReviewDecisionLedger:
    return service.IdentityReadyGovernedNonproductionHumanReviewDecisionLedger(
        database_path=tmp_path / "identity-ready-test.sqlite3",
        enabled=True,
        clock=lambda: "2026-08-27T00:00:00Z",
        before_commit_hook=before_commit_hook,
        after_commit_hook=after_commit_hook,
    )


def _row_count(path: Path) -> int:
    with sqlite3.connect(path) as connection:
        row = connection.execute(
            f"SELECT COUNT(*) FROM {service.PRIMARY_TABLE}"
        ).fetchone()
    return int(row[0])


def _raise_runtime_error() -> None:
    raise RuntimeError("synthetic_hook_failure")


def test_semantic_field_sets_are_exact_but_json_key_order_is_not_authoritative() -> None:
    request = _request()
    request["candidate"] = dict(reversed(list(request["candidate"].items())))
    request = dict(reversed(list(request.items())))

    validated = service.validate_identity_ready_governed_review_decision_request(
        request,
        server_binding_safe_hash=SAFE_BINDING_HASH,
    )

    assert validated["sample_handle"] == CURRENT_SAMPLE_HANDLE
    assert validated["review_subject_binding_safe_hash"] == SAFE_BINDING_HASH
    assert validated["decision_type"] == "keep_pending_human_review"

    for malformed in (
        {**_request(), "extra": True},
        {**_request(), "candidate": {**_candidate(), "extra": True}},
        {**_request(), "candidate": {**_candidate(), "candidate_only": 1}},
        {**_request(), "candidate": {**_candidate(), "persisted": True}},
        {**_request(), "candidate": {**_candidate(), "decision_type": "approve_trust"}},
    ):
        with pytest.raises(
            service.IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError
        ):
            service.validate_identity_ready_governed_review_decision_request(
                malformed,
                server_binding_safe_hash=SAFE_BINDING_HASH,
            )


@pytest.mark.parametrize(
    "server_hash,candidate_hash",
    [
        ("", SAFE_BINDING_HASH),
        ("A" * 64, SAFE_BINDING_HASH),
        ("b" * 64, SAFE_BINDING_HASH),
        (SAFE_BINDING_HASH, "not-a-hash"),
    ],
)
def test_server_binding_mismatch_fails_before_sqlite_open(
    tmp_path: Path,
    server_hash: str,
    candidate_hash: str,
) -> None:
    ledger = _ledger(tmp_path)

    decision, receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            ledger,
            _request(review_subject_binding_safe_hash=candidate_hash),
            server_binding_safe_hash=server_hash,
        )
    )

    assert decision is None
    assert receipt["outcome"] == "blocked_server_owned_binding_mismatch"
    assert ledger.sqlite_connection_open_count == 0
    assert not ledger.database_path.exists()


@pytest.mark.parametrize(
    "decision_type",
    ["keep_pending_human_review", "request_more_governance_review"],
)
def test_each_allowed_decision_is_append_only_and_exactly_idempotent(
    tmp_path: Path,
    decision_type: str,
) -> None:
    ledger = _ledger(tmp_path)
    request = _request(decision_type)

    first, first_receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            ledger,
            request,
            server_binding_safe_hash=SAFE_BINDING_HASH,
        )
    )
    second, second_receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            ledger,
            request,
            server_binding_safe_hash=SAFE_BINDING_HASH,
        )
    )

    assert first is not None
    assert second == first
    assert first_receipt["outcome"] == "created_exactly_one_identity_ready_human_review_decision"
    assert first_receipt["mutation_count"] == 1
    assert second_receipt["outcome"] == "already_exists_same_identity_ready_human_review_decision"
    assert second_receipt["mutation_count"] == 0
    assert first["sample_handle"] == CURRENT_SAMPLE_HANDLE
    assert first["review_subject_binding_safe_hash"] == SAFE_BINDING_HASH
    assert first["decision_type"] == decision_type
    assert first["production_object_enabled"] is False
    assert first["analysis_triggered"] is False
    assert first["report_triggered"] is False
    assert _row_count(ledger.database_path) == 1


def test_conflicting_existing_identity_fails_closed_without_overwrite(tmp_path: Path) -> None:
    ledger = _ledger(tmp_path)
    validated = service.validate_identity_ready_governed_review_decision_request(
        _request(),
        server_binding_safe_hash=SAFE_BINDING_HASH,
    )
    identity = service._identity_for(validated)
    conflict = service._build_decision(identity, "2026-08-26T00:00:00Z")
    conflict["decision_canonical_hash"] = "f" * 64

    with ledger._connect() as connection:
        ledger._ensure_schema(connection)
        ledger._insert_record(connection, conflict)
        connection.commit()

    decision, receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            ledger,
            _request(),
            server_binding_safe_hash=SAFE_BINDING_HASH,
        )
    )

    assert decision is None
    assert receipt["outcome"] == "blocked_idempotency_conflict"
    assert receipt["mutation_count"] == 0
    assert _row_count(ledger.database_path) == 1


def test_commit_boundary_failures_are_fail_closed(tmp_path: Path) -> None:
    before_ledger = _ledger(tmp_path / "before", before_commit_hook=_raise_runtime_error)
    decision, receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            before_ledger,
            _request(),
            server_binding_safe_hash=SAFE_BINDING_HASH,
        )
    )
    assert decision is None
    assert receipt["outcome"] == "bounded_identity_ready_decision_ledger_failure"
    assert receipt["mutation_count"] == 0
    assert _row_count(before_ledger.database_path) == 0

    after_ledger = _ledger(tmp_path / "after", after_commit_hook=_raise_runtime_error)
    decision, receipt = (
        service.record_identity_ready_governed_nonproduction_human_review_decision(
            after_ledger,
            _request(),
            server_binding_safe_hash=SAFE_BINDING_HASH,
        )
    )
    assert decision is None
    assert receipt["outcome"] == "paused_identity_ready_decision_commit_ambiguity"
    assert receipt["mutation_count"] == 0
    assert _row_count(after_ledger.database_path) == 1


def test_writer_source_contains_no_update_or_delete_statement() -> None:
    source = inspect.getsource(service)
    assert "UPDATE " not in source.upper()
    assert "DELETE " not in source.upper()


def test_route_model_forbids_extra_fields_and_disabled_route_opens_no_ledger(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(ValidationError):
        route_module.IdentityReadyGovernedReviewDecisionBindingRequest(
            **{**_request(), "extra": True}
        )

    monkeypatch.delenv(route_module.IDENTITY_READY_GATE, raising=False)
    monkeypatch.delenv(route_module.IDENTITY_READY_BINDING_SAFE_HASH, raising=False)
    factory_calls = 0

    def fail_factory():
        nonlocal factory_calls
        factory_calls += 1
        raise AssertionError("ledger factory must not run")

    monkeypatch.setattr(route_module, "_identity_ready_ledger_factory", fail_factory)
    response = route_module.post_identity_ready_decision(
        route_module.IdentityReadyGovernedReviewDecisionBindingRequest(**_request())
    )
    payload = json.loads(response.body)

    assert response.status_code == 404
    assert payload["request_status"] == "blocked_route_disabled"
    assert payload["decision_ledger_write_performed"] is False
    assert factory_calls == 0


def test_route_uses_temp_ledger_and_returns_only_bounded_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ledger = _ledger(tmp_path)
    monkeypatch.setenv(route_module.IDENTITY_READY_GATE, "1")
    monkeypatch.setenv(route_module.IDENTITY_READY_BINDING_SAFE_HASH, SAFE_BINDING_HASH)
    monkeypatch.setattr(route_module, "_identity_ready_ledger_factory", lambda: ledger)

    response = route_module.post_identity_ready_decision(
        route_module.IdentityReadyGovernedReviewDecisionBindingRequest(**_request())
    )
    payload = json.loads(response.body)

    assert response.status_code == 201
    assert tuple(payload) == route_module.IDENTITY_READY_POST_RESPONSE_FIELDS
    assert payload["request_status"] == "created"
    assert payload["sample_handle"] == CURRENT_SAMPLE_HANDLE
    assert payload["review_subject_binding_safe_hash"] == SAFE_BINDING_HASH
    assert payload["decision_ledger_write_performed"] is True
    assert payload["production_object_enabled"] is False
    assert payload["analysis_triggered"] is False
    assert payload["report_triggered"] is False
    assert "configuration" not in json.dumps(payload).lower()
    assert _row_count(ledger.database_path) == 1


def test_historical_route_contract_remains_separate_and_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert tuple(route_module.GovernedNonproductionHumanReviewDecisionRequest.model_fields) == (
        "request_schema",
        "request_version",
        "decision_type",
    )
    monkeypatch.delenv(route_module.GATE, raising=False)
    response = route_module.post_decision(
        route_module.GovernedNonproductionHumanReviewDecisionRequest(
            request_schema=(
                "sentigraph_governed_nonproduction_"
                "human_review_decision_request_v0_1"
            ),
            request_version="0.1",
            decision_type="keep_pending_human_review",
        )
    )
    payload = json.loads(response.body)
    assert response.status_code == 404
    assert payload["route_mode"] == (
        "internal_disabled_by_default_append_only_nonproduction_"
        "human_review_decision_ledger"
    )
