from __future__ import annotations

import inspect
import json
import sqlite3
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from app.schemas.evidence import EvidenceItem
from app.services import governed_decision_existing_evidence_link as link_service
from app.services import governed_decision_existing_evidence_link_ledger as service
from app.services.existing_evidenceitem_safe_identity_projection import (
    project_existing_evidenceitem_safe_identity_receipt,
)
from app.services.identity_ready_governed_nonproduction_human_review_decision_downstream_handoff import (
    build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate,
)


DECISION_SUFFIX = "0123456789abcdef0123456789abcdef"
EVIDENCE_ID = "evidence-synthetic-001"
CONTENT_HASH = "a" * 64


class _FakeCaseRepository:
    def __init__(self, case_id: str) -> None:
        self.case = SimpleNamespace(
            evidence_items=[
                EvidenceItem(
                    case_id=case_id,
                    evidence_id=EVIDENCE_ID,
                    content_hash=CONTENT_HASH,
                    body_text="raw synthetic body",
                )
            ]
        )

    def get_case(self, _case_id: str) -> object:
        return self.case


def _candidate(*, case_id: str = "case-synthetic-001") -> dict[str, Any]:
    handoff = build_identity_ready_governed_nonproduction_human_review_decision_downstream_handoff_candidate(
        {
            "decision_id": f"irghrd-{DECISION_SUFFIX}",
            "audit_receipt_reference": f"irghrd-receipt-{DECISION_SUFFIX}",
            "sample_handle": "helldivers2-psn-demo",
            "decision_type": "keep_pending_human_review",
            "decision_status": (
                "recorded_append_only_nonproduction_identity_ready"
            ),
            "recorded_at": "2026-08-31T12:34:56Z",
            "human_review_required": True,
            "no_automatic_trust_upgrade": True,
            "production_object_enabled": False,
            "review_queue_runtime_enabled": False,
            "evidence_layer_write_performed": False,
            "provider_or_b05_called": False,
            "analysis_triggered": False,
            "report_triggered": False,
        }
    )
    receipt = project_existing_evidenceitem_safe_identity_receipt(
        _FakeCaseRepository(case_id),
        case_id,
        EVIDENCE_ID,
    )
    return link_service.build_governed_decision_existing_evidence_link_candidate(
        handoff,
        receipt,
        human_authority_receipt_reference="human-authority-receipt-001",
        manual_review_responsibility_receipt_reference=(
            "manual-review-responsibility-001"
        ),
        rollback_plan_reference="append-only-revocation-plan-v0-1",
        created_at="2026-09-02T00:00:00Z",
        warning_count_acknowledged=True,
        lineage_review_status="verified",
        raw_private_secret_absence_acknowledged=True,
    )


def _database(tmp_path: Path) -> Path:
    return tmp_path / "isolated-link-ledger.sqlite3"


def _row_count(database: Path) -> int:
    with sqlite3.connect(database) as connection:
        row = connection.execute(
            f"SELECT COUNT(*) FROM {service.PRIMARY_TABLE}"
        ).fetchone()
    assert row is not None
    return int(row[0])


def test_initializer_is_explicit_and_creates_only_the_two_ledger_tables(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)

    receipt = service.initialize_governed_decision_existing_evidence_link_ledger(
        database
    )

    assert receipt["outcome"] == "link_ledger_initialized"
    with sqlite3.connect(database) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert tables == {service.PRIMARY_TABLE, service.REVOCATION_TABLE}
    assert _row_count(database) == 0


def test_writer_refuses_absent_or_uninitialized_schema_without_creating_it(
    tmp_path: Path,
) -> None:
    absent = _database(tmp_path)

    record, receipt = service.record_governed_decision_existing_evidence_link(
        absent,
        _candidate(),
    )

    assert record is None
    assert receipt["outcome"] == "link_ledger_target_absent"
    assert receipt["mutation_count"] == 0
    assert not absent.exists()

    wrong_schema = tmp_path / "wrong-schema.sqlite3"
    with sqlite3.connect(wrong_schema) as connection:
        connection.execute("CREATE TABLE unrelated (value TEXT)")
        connection.commit()
    before = wrong_schema.read_bytes()
    record, receipt = service.record_governed_decision_existing_evidence_link(
        wrong_schema,
        _candidate(),
    )
    assert record is None
    assert receipt["outcome"] == "bounded_link_ledger_schema_unavailable"
    assert receipt["mutation_count"] == 0
    assert wrong_schema.read_bytes() == before


def test_writer_rejects_invalid_candidate_before_opening_or_creating_database(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    invalid = {**_candidate(), "candidate_only": 1}

    record, receipt = service.record_governed_decision_existing_evidence_link(
        database,
        invalid,
    )

    assert record is None
    assert receipt["outcome"] == "blocked_link_candidate_contract_mismatch"
    assert receipt["mutation_count"] == 0
    assert not database.exists()


def test_one_append_and_exact_idempotent_replay_produce_one_row(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    candidate = _candidate()

    first, first_receipt = (
        service.record_governed_decision_existing_evidence_link(
            database,
            candidate,
        )
    )
    second, second_receipt = (
        service.record_governed_decision_existing_evidence_link(
            database,
            candidate,
        )
    )

    assert first is not None
    assert second == first
    assert tuple(first) == service.LINK_RECORD_FIELDS
    assert first["candidate_only"] is False
    assert first["persisted"] is True
    assert first_receipt["outcome"] == (
        "created_exactly_one_governed_decision_existing_evidence_link"
    )
    assert first_receipt["mutation_count"] == 1
    assert second_receipt["outcome"] == "already_linked_exact"
    assert second_receipt["mutation_count"] == 0
    assert _row_count(database) == 1


def test_same_fingerprint_with_immutable_field_drift_is_a_zero_write_conflict(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    candidate = _candidate()
    created, _receipt = service.record_governed_decision_existing_evidence_link(
        database,
        candidate,
    )
    assert created is not None
    conflicting = deepcopy(candidate)
    conflicting["rollback_plan_reference"] = "different-revocation-plan"
    assert conflicting["link_fingerprint_sha256"] == candidate[
        "link_fingerprint_sha256"
    ]

    record, receipt = service.record_governed_decision_existing_evidence_link(
        database,
        conflicting,
    )

    assert record is None
    assert receipt["outcome"] == "blocked_link_idempotency_conflict"
    assert receipt["mutation_count"] == 0
    assert _row_count(database) == 1


def test_case_id_is_part_of_unique_identity_and_allows_distinct_case_links(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    first_candidate = _candidate(case_id="case-synthetic-001")
    second_candidate = _candidate(case_id="case-synthetic-002")

    first, first_receipt = (
        service.record_governed_decision_existing_evidence_link(
            database,
            first_candidate,
        )
    )
    second, second_receipt = (
        service.record_governed_decision_existing_evidence_link(
            database,
            second_candidate,
        )
    )

    assert first is not None and second is not None
    assert first["link_fingerprint_sha256"] != second[
        "link_fingerprint_sha256"
    ]
    assert first_receipt["mutation_count"] == 1
    assert second_receipt["mutation_count"] == 1
    assert _row_count(database) == 2


def test_read_only_verifier_returns_exact_record_without_changing_database_bytes(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    created, _receipt = service.record_governed_decision_existing_evidence_link(
        database,
        _candidate(),
    )
    assert created is not None
    before = database.read_bytes()

    verified, receipt = service.verify_governed_decision_existing_evidence_link(
        database,
        created["link_fingerprint_sha256"],
    )

    assert verified == created
    assert receipt["outcome"] == "verified_exact_link"
    assert receipt["mutation_count"] == 0
    assert database.read_bytes() == before


def test_read_only_verifier_distinguishes_absence_and_integrity_failure(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    record, receipt = service.verify_governed_decision_existing_evidence_link(
        database,
        "f" * 64,
    )
    assert record is None
    assert receipt["outcome"] == "link_not_found"

    created, _receipt = service.record_governed_decision_existing_evidence_link(
        database,
        _candidate(),
    )
    assert created is not None
    with sqlite3.connect(database) as connection:
        corrupted = {**created, "link_record_canonical_hash": "0" * 64}
        connection.execute(
            f"UPDATE {service.PRIMARY_TABLE} SET link_json = ? "
            "WHERE link_fingerprint_sha256 = ?",
            (
                json.dumps(corrupted, separators=(",", ":")),
                created["link_fingerprint_sha256"],
            ),
        )
        connection.commit()

    record, receipt = service.verify_governed_decision_existing_evidence_link(
        database,
        created["link_fingerprint_sha256"],
    )
    assert record is None
    assert receipt["outcome"] == "bounded_link_ledger_read_failure"


def test_persisted_record_and_receipts_keep_all_downstream_authority_false(
    tmp_path: Path,
) -> None:
    database = _database(tmp_path)
    service.initialize_governed_decision_existing_evidence_link_ledger(database)
    record, receipt = service.record_governed_decision_existing_evidence_link(
        database,
        _candidate(),
    )

    assert record is not None
    assert all(
        record[field] is False
        for field in link_service.DOWNSTREAM_AUTHORIZATION_FIELDS
    )
    assert all(
        receipt[field] is False
        for field in link_service.DOWNSTREAM_AUTHORIZATION_FIELDS
    )
    assert "raw synthetic body" not in repr(record)


def test_writer_and_verifier_have_separate_schema_and_access_responsibilities() -> None:
    writer_source = inspect.getsource(
        service.record_governed_decision_existing_evidence_link
    )
    verifier_source = inspect.getsource(
        service.verify_governed_decision_existing_evidence_link
    )

    assert "initialize_governed_decision_existing_evidence_link_ledger" not in (
        writer_source
    )
    assert "CREATE TABLE" not in writer_source.upper()
    for forbidden in ("UPDATE ", "DELETE ", "REPLACE ", "UPSERT"):
        assert forbidden not in writer_source.upper()
    assert 'mode="rw"' in writer_source
    assert 'mode="ro"' in verifier_source
    assert "PRAGMA query_only = ON" in verifier_source
    for forbidden in ("INSERT ", "UPDATE ", "DELETE ", "CREATE TABLE"):
        assert forbidden not in verifier_source.upper()


def test_module_has_no_case_store_network_or_canonical_factory_dependency() -> None:
    source = inspect.getsource(service).lower()

    for forbidden in (
        "case_repository",
        "case_store",
        "store_factory",
        "httpx",
        "requests",
        "socket",
        "subprocess",
        "backend/data/cases.json",
    ):
        assert forbidden not in source
