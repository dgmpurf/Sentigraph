from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from app.services.governed_decision_existing_evidence_link import (
    DOWNSTREAM_AUTHORIZATION_FIELDS,
    LINK_CANDIDATE_FIELDS,
    LINK_CANDIDATE_MODE,
    LINK_CANDIDATE_SCHEMA,
    LINK_CANDIDATE_VERSION,
    LINK_RECORD_MODE,
    LINK_RECORD_SCHEMA,
    LINK_RECORD_VERSION,
    RELATION_TYPE,
    validate_governed_decision_existing_evidence_link_candidate,
)


LEDGER_SCOPE = "governed_decision_existing_evidence_link_append_only"
LOGICAL_TARGET_LABEL = (
    "runtime/governed_decision_existing_evidence_links/"
    "governed_decision_existing_evidence_links_v0_1.sqlite3"
)
PRIMARY_TABLE = "governed_decision_existing_evidence_links_v0_1"
REVOCATION_TABLE = "governed_decision_existing_evidence_link_revocations_v0_1"

LINK_RECORD_FIELDS = (
    "schema",
    "version",
    "mode",
    "ledger_scope",
    "link_id",
    "link_fingerprint_sha256",
    "relation_type",
    "status",
    "decision_reference",
    "evidence_reference",
    "human_authority_receipt_reference",
    "manual_review_responsibility_receipt_reference",
    "rollback_plan_reference",
    "warning_count_acknowledged",
    "lineage_review_status",
    "raw_private_secret_absence_acknowledged",
    "created_at",
    "candidate_only",
    "persisted",
    "human_review_required",
    "no_automatic_trust_upgrade",
    *DOWNSTREAM_AUTHORIZATION_FIELDS,
    "link_record_canonical_hash",
)

_PRIMARY_COLUMNS = (
    "link_id",
    "link_fingerprint_sha256",
    "decision_id",
    "audit_receipt_reference",
    "case_id",
    "evidence_id",
    "evidence_content_hash",
    "relation_type",
    "link_record_canonical_hash",
    "link_json",
)
_COMPOSITE_IDENTITY_COLUMNS = (
    "decision_id",
    "audit_receipt_reference",
    "case_id",
    "evidence_id",
    "evidence_content_hash",
    "relation_type",
)
_LOWER_HEX_64_PATTERN = re.compile(r"[0-9a-f]{64}")

CREATE_PRIMARY_TABLE_STATEMENT = f"""
CREATE TABLE IF NOT EXISTS {PRIMARY_TABLE} (
    link_id TEXT PRIMARY KEY,
    link_fingerprint_sha256 TEXT NOT NULL UNIQUE,
    decision_id TEXT NOT NULL,
    audit_receipt_reference TEXT NOT NULL,
    case_id TEXT NOT NULL,
    evidence_id TEXT NOT NULL,
    evidence_content_hash TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    link_record_canonical_hash TEXT NOT NULL,
    link_json TEXT NOT NULL,
    UNIQUE (
        decision_id,
        audit_receipt_reference,
        case_id,
        evidence_id,
        evidence_content_hash,
        relation_type
    )
)
""".strip()

CREATE_REVOCATION_TABLE_STATEMENT = f"""
CREATE TABLE IF NOT EXISTS {REVOCATION_TABLE} (
    revocation_event_id TEXT PRIMARY KEY,
    link_fingerprint_sha256 TEXT NOT NULL,
    revocation_status TEXT NOT NULL,
    revocation_reason_reference TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    revocation_json TEXT NOT NULL,
    FOREIGN KEY (link_fingerprint_sha256)
        REFERENCES {PRIMARY_TABLE} (link_fingerprint_sha256)
)
""".strip()


class GovernedDecisionExistingEvidenceLinkLedgerError(RuntimeError):
    """Raised when the isolated link ledger is unavailable or inconsistent."""

    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _is_lower_hex_64(value: object) -> bool:
    return (
        type(value) is str
        and _LOWER_HEX_64_PATTERN.fullmatch(value) is not None
    )


def _database_uri(database_path: Path, *, mode: str) -> str:
    return f"{database_path.resolve().as_uri()}?mode={mode}"


def _connect_existing(database_path: Path, *, mode: str) -> sqlite3.Connection:
    if not isinstance(database_path, Path) or not database_path.is_file():
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_ledger_target_absent"
        )
    try:
        return sqlite3.connect(
            _database_uri(database_path, mode=mode),
            uri=True,
            timeout=1.0,
        )
    except sqlite3.Error as exc:
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "bounded_link_ledger_unavailable"
        ) from exc


def _schema_is_exact(connection: sqlite3.Connection) -> bool:
    try:
        columns = tuple(
            row[1]
            for row in connection.execute(
                f"PRAGMA table_info({PRIMARY_TABLE})"
            ).fetchall()
        )
        if columns != _PRIMARY_COLUMNS:
            return False
        index_rows = connection.execute(
            f"PRAGMA index_list({PRIMARY_TABLE})"
        ).fetchall()
        unique_indexes: set[tuple[str, ...]] = set()
        for row in index_rows:
            if len(row) < 3 or row[2] != 1:
                continue
            index_name = row[1]
            if type(index_name) is not str:
                return False
            index_columns = tuple(
                index_row[2]
                for index_row in connection.execute(
                    f"PRAGMA index_info('{index_name}')"
                ).fetchall()
            )
            unique_indexes.add(index_columns)
        return (
            ("link_fingerprint_sha256",) in unique_indexes
            and _COMPOSITE_IDENTITY_COLUMNS in unique_indexes
        )
    except (IndexError, sqlite3.Error, TypeError):
        return False


def _record_from_candidate(candidate: Mapping[str, Any]) -> dict[str, Any]:
    validated = validate_governed_decision_existing_evidence_link_candidate(
        candidate
    )
    values: dict[str, Any] = {
        "schema": LINK_RECORD_SCHEMA,
        "version": LINK_RECORD_VERSION,
        "mode": LINK_RECORD_MODE,
        "ledger_scope": LEDGER_SCOPE,
        "link_id": validated["link_id"],
        "link_fingerprint_sha256": validated["link_fingerprint_sha256"],
        "relation_type": validated["relation_type"],
        "status": validated["initial_status"],
        "decision_reference": dict(validated["decision_reference"]),
        "evidence_reference": dict(validated["evidence_reference"]),
        "human_authority_receipt_reference": validated[
            "human_authority_receipt_reference"
        ],
        "manual_review_responsibility_receipt_reference": validated[
            "manual_review_responsibility_receipt_reference"
        ],
        "rollback_plan_reference": validated["rollback_plan_reference"],
        "warning_count_acknowledged": validated[
            "warning_count_acknowledged"
        ],
        "lineage_review_status": validated["lineage_review_status"],
        "raw_private_secret_absence_acknowledged": validated[
            "raw_private_secret_absence_acknowledged"
        ],
        "created_at": validated["created_at"],
        "candidate_only": False,
        "persisted": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in DOWNSTREAM_AUTHORIZATION_FIELDS},
    }
    values["link_record_canonical_hash"] = _canonical_sha256(values)
    return {field: values[field] for field in LINK_RECORD_FIELDS}


def validate_governed_decision_existing_evidence_link_record(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one immutable persisted link record and its canonical hash."""

    if not isinstance(record, Mapping) or set(record) != set(LINK_RECORD_FIELDS):
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_contract_mismatch"
        )
    if (
        record["schema"] != LINK_RECORD_SCHEMA
        or record["version"] != LINK_RECORD_VERSION
        or record["mode"] != LINK_RECORD_MODE
        or record["ledger_scope"] != LEDGER_SCOPE
        or record["relation_type"] != RELATION_TYPE
        or record["status"] != "active"
        or record["candidate_only"] is not False
        or record["persisted"] is not True
        or record["human_review_required"] is not True
        or record["no_automatic_trust_upgrade"] is not True
        or any(record[field] is not False for field in DOWNSTREAM_AUTHORIZATION_FIELDS)
    ):
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_contract_mismatch"
        )

    candidate_values: dict[str, Any] = {
        "schema": LINK_CANDIDATE_SCHEMA,
        "version": LINK_CANDIDATE_VERSION,
        "mode": LINK_CANDIDATE_MODE,
        "link_schema": LINK_RECORD_SCHEMA,
        "link_id": record["link_id"],
        "link_fingerprint_sha256": record["link_fingerprint_sha256"],
        "relation_type": record["relation_type"],
        "initial_status": record["status"],
        "decision_reference": record["decision_reference"],
        "evidence_reference": record["evidence_reference"],
        "human_authority_receipt_reference": record[
            "human_authority_receipt_reference"
        ],
        "manual_review_responsibility_receipt_reference": record[
            "manual_review_responsibility_receipt_reference"
        ],
        "rollback_plan_reference": record["rollback_plan_reference"],
        "warning_count_acknowledged": record["warning_count_acknowledged"],
        "lineage_review_status": record["lineage_review_status"],
        "raw_private_secret_absence_acknowledged": record[
            "raw_private_secret_absence_acknowledged"
        ],
        "created_at": record["created_at"],
        "candidate_only": True,
        "persisted": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in DOWNSTREAM_AUTHORIZATION_FIELDS},
    }
    candidate = {
        field: candidate_values[field] for field in LINK_CANDIDATE_FIELDS
    }
    try:
        validate_governed_decision_existing_evidence_link_candidate(candidate)
    except (TypeError, ValueError) as exc:
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_contract_mismatch"
        ) from exc

    material = {
        field: record[field]
        for field in LINK_RECORD_FIELDS
        if field != "link_record_canonical_hash"
    }
    canonical_hash = record["link_record_canonical_hash"]
    if (
        not _is_lower_hex_64(canonical_hash)
        or not hmac.compare_digest(canonical_hash, _canonical_sha256(material))
    ):
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_integrity_mismatch"
        )
    return {field: record[field] for field in LINK_RECORD_FIELDS}


def _receipt(
    outcome: str,
    *,
    source: Mapping[str, Any] | None = None,
    mutation_count: int = 0,
    row_count_before: int | None = None,
    row_count_after: int | None = None,
) -> dict[str, Any]:
    source = source or {}
    decision_reference = source.get("decision_reference", {})
    evidence_reference = source.get("evidence_reference", {})
    return {
        "receipt_schema": (
            "sentigraph_governed_decision_existing_evidence_link_"
            "ledger_receipt_v0_1"
        ),
        "receipt_version": "0.1",
        "outcome": outcome,
        "link_id": source.get("link_id"),
        "link_fingerprint_sha256": source.get("link_fingerprint_sha256"),
        "decision_id": decision_reference.get("decision_id"),
        "audit_receipt_reference": decision_reference.get(
            "audit_receipt_reference"
        ),
        "case_id": evidence_reference.get("case_id"),
        "evidence_id": evidence_reference.get("evidence_id"),
        "evidence_content_hash": evidence_reference.get(
            "evidence_content_hash"
        ),
        "relation_type": source.get("relation_type"),
        "link_status": source.get("status", source.get("initial_status")),
        "mutation_count": mutation_count,
        "link_row_count_before": row_count_before,
        "link_row_count_after": row_count_after,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        **{field: False for field in DOWNSTREAM_AUTHORIZATION_FIELDS},
    }


def initialize_governed_decision_existing_evidence_link_ledger(
    database_path: Path,
) -> dict[str, Any]:
    """Explicitly initialize a caller-selected ledger target."""

    if not isinstance(database_path, Path):
        return _receipt("blocked_link_ledger_path_invalid")
    try:
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(database_path, timeout=1.0) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(CREATE_PRIMARY_TABLE_STATEMENT)
            connection.execute(CREATE_REVOCATION_TABLE_STATEMENT)
            connection.commit()
            if not _schema_is_exact(connection):
                return _receipt("bounded_link_ledger_schema_unavailable")
    except (OSError, sqlite3.Error):
        return _receipt("bounded_link_ledger_initialization_failure")
    return _receipt("link_ledger_initialized")


def _row_count(connection: sqlite3.Connection) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {PRIMARY_TABLE}").fetchone()
    if row is None or len(row) != 1 or type(row[0]) is not int:
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_ledger_integrity_mismatch"
        )
    return row[0]


def _select_existing(
    connection: sqlite3.Connection,
    record: Mapping[str, Any],
) -> list[tuple[str]]:
    decision = record["decision_reference"]
    evidence = record["evidence_reference"]
    return connection.execute(
        f"""
        SELECT link_json FROM {PRIMARY_TABLE}
        WHERE link_fingerprint_sha256 = ?
           OR link_id = ?
           OR (
                decision_id = ?
            AND audit_receipt_reference = ?
            AND case_id = ?
            AND evidence_id = ?
            AND evidence_content_hash = ?
            AND relation_type = ?
           )
        """.strip(),
        (
            record["link_fingerprint_sha256"],
            record["link_id"],
            decision["decision_id"],
            decision["audit_receipt_reference"],
            evidence["case_id"],
            evidence["evidence_id"],
            evidence["evidence_content_hash"],
            record["relation_type"],
        ),
    ).fetchall()


def _row_to_record(row: tuple[str]) -> dict[str, Any]:
    if len(row) != 1 or type(row[0]) is not str:
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_integrity_mismatch"
        )
    try:
        value = json.loads(row[0])
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_integrity_mismatch"
        ) from exc
    if not isinstance(value, dict):
        raise GovernedDecisionExistingEvidenceLinkLedgerError(
            "link_record_integrity_mismatch"
        )
    return validate_governed_decision_existing_evidence_link_record(value)


def _insert_record(
    connection: sqlite3.Connection,
    record: Mapping[str, Any],
) -> None:
    decision = record["decision_reference"]
    evidence = record["evidence_reference"]
    connection.execute(
        f"""
        INSERT INTO {PRIMARY_TABLE} (
            link_id,
            link_fingerprint_sha256,
            decision_id,
            audit_receipt_reference,
            case_id,
            evidence_id,
            evidence_content_hash,
            relation_type,
            link_record_canonical_hash,
            link_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """.strip(),
        (
            record["link_id"],
            record["link_fingerprint_sha256"],
            decision["decision_id"],
            decision["audit_receipt_reference"],
            evidence["case_id"],
            evidence["evidence_id"],
            evidence["evidence_content_hash"],
            record["relation_type"],
            record["link_record_canonical_hash"],
            json.dumps(
                record,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ),
        ),
    )


def record_governed_decision_existing_evidence_link(
    database_path: Path,
    candidate: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Append one exact link to an already initialized caller-owned ledger."""

    try:
        record = _record_from_candidate(candidate)
    except (TypeError, ValueError):
        return None, _receipt("blocked_link_candidate_contract_mismatch")
    try:
        connection = _connect_existing(database_path, mode="rw")
    except GovernedDecisionExistingEvidenceLinkLedgerError as exc:
        return None, _receipt(exc.outcome, source=record)

    row_count_before: int | None = None
    try:
        if not _schema_is_exact(connection):
            return None, _receipt(
                "bounded_link_ledger_schema_unavailable",
                source=record,
            )
        row_count_before = _row_count(connection)
        existing_rows = _select_existing(connection, record)
        if len(existing_rows) > 1:
            return None, _receipt(
                "blocked_link_idempotency_conflict",
                source=record,
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )
        if len(existing_rows) == 1:
            try:
                existing = _row_to_record(existing_rows[0])
            except GovernedDecisionExistingEvidenceLinkLedgerError:
                return None, _receipt(
                    "blocked_link_idempotency_conflict",
                    source=record,
                    row_count_before=row_count_before,
                    row_count_after=row_count_before,
                )
            if existing != record:
                return None, _receipt(
                    "blocked_link_idempotency_conflict",
                    source=record,
                    row_count_before=row_count_before,
                    row_count_after=row_count_before,
                )
            return existing, _receipt(
                "already_linked_exact",
                source=existing,
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )

        connection.execute("BEGIN IMMEDIATE")
        _insert_record(connection, record)
        connection.commit()
    except (sqlite3.Error, TypeError, ValueError, RuntimeError):
        try:
            connection.rollback()
        except sqlite3.Error:
            pass
        return None, _receipt(
            "bounded_link_ledger_write_failure",
            source=record,
            row_count_before=row_count_before,
            row_count_after=row_count_before,
        )
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass

    row_count_after = (
        row_count_before + 1 if row_count_before is not None else None
    )
    return record, _receipt(
        "created_exactly_one_governed_decision_existing_evidence_link",
        source=record,
        mutation_count=1,
        row_count_before=row_count_before,
        row_count_after=row_count_after,
    )


def verify_governed_decision_existing_evidence_link(
    database_path: Path,
    link_fingerprint_sha256: str,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    """Read one exact link through an SQLite read-only connection."""

    if not _is_lower_hex_64(link_fingerprint_sha256):
        return None, _receipt("blocked_link_fingerprint_invalid")
    try:
        connection = _connect_existing(database_path, mode="ro")
    except GovernedDecisionExistingEvidenceLinkLedgerError as exc:
        return None, _receipt(exc.outcome)
    try:
        connection.execute("PRAGMA query_only = ON")
        if not _schema_is_exact(connection):
            return None, _receipt("bounded_link_ledger_schema_unavailable")
        rows = connection.execute(
            f"""
            SELECT link_json FROM {PRIMARY_TABLE}
            WHERE link_fingerprint_sha256 = ?
            LIMIT 2
            """.strip(),
            (link_fingerprint_sha256,),
        ).fetchall()
        if len(rows) == 0:
            return None, _receipt("link_not_found")
        if len(rows) != 1:
            return None, _receipt("link_record_integrity_mismatch")
        record = _row_to_record(rows[0])
        if not hmac.compare_digest(
            record["link_fingerprint_sha256"],
            link_fingerprint_sha256,
        ):
            return None, _receipt("link_record_integrity_mismatch")
    except (sqlite3.Error, TypeError, ValueError, RuntimeError):
        return None, _receipt("bounded_link_ledger_read_failure")
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass
    return record, _receipt("verified_exact_link", source=record)
