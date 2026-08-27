from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


REQUEST_SCHEMA = (
    "sentigraph_internal_alpha_identity_ready_governed_"
    "review_decision_binding_request_v0_1"
)
REQUEST_VERSION = "0.1"
REQUEST_FIELDS = frozenset({"request_schema", "request_version", "candidate"})
CANDIDATE_SCHEMA = (
    "sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1"
)
CANDIDATE_MODE = (
    "frontend_local_nonpersistent_governed_human_review_decision_candidate"
)
CANDIDATE_FIELDS = frozenset(
    {
        "schema",
        "mode",
        "identity_schema",
        "identity_version",
        "identity_status",
        "sample_handle",
        "review_subject_binding_safe_hash",
        "decision_type",
        "candidate_only",
        "persisted",
        "trust_upgraded",
        "production_object",
        "human_review_required",
        "no_automatic_trust_upgrade",
    }
)
IDENTITY_SCHEMA = "sentigraph_b05_review_subject_identity_v0_1"
IDENTITY_VERSION = "0.1"
IDENTITY_STATUS = "ready"
SERVER_SAMPLE_HANDLE = "helldivers2-psn-demo"
DECISION_TYPES = (
    "keep_pending_human_review",
    "request_more_governance_review",
)
LOWER_HEX_64 = re.compile(r"[0-9a-f]{64}")

DECISION_SCHEMA = (
    "sentigraph_identity_ready_governed_nonproduction_"
    "human_review_decision_record_v0_1"
)
DECISION_VERSION = "0.1"
DECISION_STATUS = "recorded_append_only_nonproduction_identity_ready"
LEDGER_SCOPE = "identity_ready_governed_nonproduction_human_review_only"
LOGICAL_TARGET_LABEL = (
    "runtime/identity_ready_governed_nonproduction_human_review_decisions/"
    "identity_ready_review_decisions_v0_1.sqlite3"
)
PRIMARY_TABLE = (
    "identity_ready_governed_nonproduction_human_review_decisions_v0_1"
)
DECISION_FIELDS = (
    "decision_schema",
    "decision_version",
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
    "ledger_scope",
    "decision_status",
    "recorded_at",
    "request_schema",
    "request_version",
    "candidate_schema",
    "candidate_mode",
    "identity_schema",
    "identity_version",
    "identity_status",
    "sample_handle",
    "review_subject_binding_safe_hash",
    "decision_type",
    "server_binding_context_mode",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
    "decision_canonical_hash",
)

CREATE_TABLE_STATEMENT = f"""
CREATE TABLE IF NOT EXISTS {PRIMARY_TABLE} (
    decision_id TEXT PRIMARY KEY,
    idempotency_key TEXT NOT NULL UNIQUE,
    audit_receipt_reference TEXT NOT NULL UNIQUE,
    sample_handle TEXT NOT NULL,
    review_subject_binding_safe_hash TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    decision_canonical_hash TEXT NOT NULL,
    decision_json TEXT NOT NULL
)
""".strip()


class IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
    ValueError
):
    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


class IdentityReadyGovernedNonproductionHumanReviewDecisionLedgerUnavailable(
    RuntimeError
):
    pass


class IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError(
    RuntimeError
):
    pass


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _utc_clock() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00",
        "Z",
    )


def _is_lower_hex_64(value: object) -> bool:
    return type(value) is str and LOWER_HEX_64.fullmatch(value) is not None


def validate_identity_ready_governed_review_decision_request(
    request: Mapping[str, Any],
    *,
    server_binding_safe_hash: str,
) -> dict[str, Any]:
    if not _is_lower_hex_64(server_binding_safe_hash):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_server_owned_binding_mismatch"
        )
    if not isinstance(request, dict) or set(request) != REQUEST_FIELDS:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_request_contract_mismatch"
        )
    if (
        type(request["request_schema"]) is not str
        or type(request["request_version"]) is not str
        or request["request_schema"] != REQUEST_SCHEMA
        or request["request_version"] != REQUEST_VERSION
        or not isinstance(request["candidate"], dict)
    ):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_request_contract_mismatch"
        )

    candidate = request["candidate"]
    if set(candidate) != CANDIDATE_FIELDS:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_candidate_contract_mismatch"
        )
    string_fields = (
        "schema",
        "mode",
        "identity_schema",
        "identity_version",
        "identity_status",
        "sample_handle",
        "review_subject_binding_safe_hash",
        "decision_type",
    )
    boolean_fields = tuple(CANDIDATE_FIELDS.difference(string_fields))
    if any(type(candidate[field]) is not str for field in string_fields) or any(
        type(candidate[field]) is not bool for field in boolean_fields
    ):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_candidate_contract_mismatch"
        )
    if (
        candidate["schema"] != CANDIDATE_SCHEMA
        or candidate["mode"] != CANDIDATE_MODE
        or candidate["identity_schema"] != IDENTITY_SCHEMA
        or candidate["identity_version"] != IDENTITY_VERSION
        or candidate["identity_status"] != IDENTITY_STATUS
        or candidate["sample_handle"] != SERVER_SAMPLE_HANDLE
        or candidate["candidate_only"] is not True
        or candidate["persisted"] is not False
        or candidate["trust_upgraded"] is not False
        or candidate["production_object"] is not False
        or candidate["human_review_required"] is not True
        or candidate["no_automatic_trust_upgrade"] is not True
    ):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_candidate_contract_mismatch"
        )
    if candidate["decision_type"] not in DECISION_TYPES:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_unsupported_decision_type"
        )
    candidate_hash = candidate["review_subject_binding_safe_hash"]
    if (
        not _is_lower_hex_64(candidate_hash)
        or not hmac.compare_digest(candidate_hash, server_binding_safe_hash)
    ):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_server_owned_binding_mismatch"
        )

    return {
        "request_schema": request["request_schema"],
        "request_version": request["request_version"],
        "candidate_schema": candidate["schema"],
        "candidate_mode": candidate["mode"],
        "identity_schema": candidate["identity_schema"],
        "identity_version": candidate["identity_version"],
        "identity_status": candidate["identity_status"],
        "sample_handle": candidate["sample_handle"],
        "review_subject_binding_safe_hash": candidate_hash,
        "decision_type": candidate["decision_type"],
        "server_binding_context_mode": "process_local_configuration_exact_match",
    }


def _identity_for(validated: Mapping[str, Any]) -> dict[str, Any]:
    canonical_material = {
        key: validated[key]
        for key in (
            "request_schema",
            "request_version",
            "candidate_schema",
            "candidate_mode",
            "identity_schema",
            "identity_version",
            "identity_status",
            "sample_handle",
            "review_subject_binding_safe_hash",
            "decision_type",
            "server_binding_context_mode",
        )
    }
    idempotency_key = _canonical_sha256(canonical_material)
    suffix = idempotency_key[:32]
    return {
        "decision_id": f"irghrd-{suffix}",
        "idempotency_key": idempotency_key,
        "audit_receipt_reference": f"irghrd-receipt-{suffix}",
        "ledger_scope": LEDGER_SCOPE,
        **canonical_material,
    }


def _build_decision(
    identity: Mapping[str, Any],
    recorded_at: str,
) -> dict[str, Any]:
    values = {
        "decision_schema": DECISION_SCHEMA,
        "decision_version": DECISION_VERSION,
        **identity,
        "decision_status": DECISION_STATUS,
        "recorded_at": recorded_at,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
    }
    values["decision_canonical_hash"] = _canonical_sha256(values)
    return {field: values[field] for field in DECISION_FIELDS}


def _receipt(
    outcome: str,
    *,
    decision: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    mutation_count: int = 0,
    row_count_before: int | None = None,
    row_count_after: int | None = None,
) -> dict[str, Any]:
    source = decision or identity or {}
    return {
        "receipt_schema": (
            "sentigraph_identity_ready_governed_nonproduction_"
            "human_review_decision_receipt_v0_1"
        ),
        "receipt_version": "0.1",
        "outcome": outcome,
        "decision_id": source.get("decision_id"),
        "idempotency_key": source.get("idempotency_key"),
        "audit_receipt_reference": source.get("audit_receipt_reference"),
        "decision_type": source.get("decision_type"),
        "sample_handle": source.get("sample_handle"),
        "review_subject_binding_safe_hash": source.get(
            "review_subject_binding_safe_hash"
        ),
        "decision_status": source.get(
            "decision_status",
            "decision_not_recorded",
        ),
        "decision_canonical_hash": source.get("decision_canonical_hash"),
        "mutation_count": mutation_count,
        "decision_row_count_before": row_count_before,
        "decision_row_count_after": row_count_after,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "evidence_layer_write_performed": False,
        "provider_or_b05_called": False,
        "analysis_triggered": False,
        "report_triggered": False,
    }


class IdentityReadyGovernedNonproductionHumanReviewDecisionLedger:
    def __init__(
        self,
        database_path: Path | None = None,
        *,
        enabled: bool = False,
        clock: Callable[[], str] | None = None,
        before_commit_hook: Callable[[], None] | None = None,
        after_commit_hook: Callable[[], None] | None = None,
    ) -> None:
        self.database_path = database_path
        self.enabled = enabled
        self.clock = clock or _utc_clock
        self.before_commit_hook = before_commit_hook
        self.after_commit_hook = after_commit_hook
        self.sqlite_connection_open_count = 0

    def _connect(self) -> sqlite3.Connection:
        if not self.enabled or self.database_path is None:
            raise IdentityReadyGovernedNonproductionHumanReviewDecisionLedgerUnavailable()
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            connection = sqlite3.connect(self.database_path)
        except sqlite3.Error as exc:
            raise IdentityReadyGovernedNonproductionHumanReviewDecisionLedgerUnavailable() from exc
        self.sqlite_connection_open_count += 1
        return connection

    @staticmethod
    def _ensure_schema(connection: sqlite3.Connection) -> None:
        connection.execute(CREATE_TABLE_STATEMENT)

    @staticmethod
    def _insert_record(
        connection: sqlite3.Connection,
        decision: Mapping[str, Any],
    ) -> None:
        connection.execute(
            f"""
            INSERT INTO {PRIMARY_TABLE} (
                decision_id,
                idempotency_key,
                audit_receipt_reference,
                sample_handle,
                review_subject_binding_safe_hash,
                decision_type,
                decision_canonical_hash,
                decision_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """.strip(),
            (
                decision["decision_id"],
                decision["idempotency_key"],
                decision["audit_receipt_reference"],
                decision["sample_handle"],
                decision["review_subject_binding_safe_hash"],
                decision["decision_type"],
                decision["decision_canonical_hash"],
                json.dumps(
                    decision,
                    ensure_ascii=False,
                    allow_nan=False,
                    separators=(",", ":"),
                ),
            ),
        )


def _row_count(connection: sqlite3.Connection) -> int:
    row = connection.execute(f"SELECT COUNT(*) FROM {PRIMARY_TABLE}").fetchone()
    if row is None or len(row) != 1 or type(row[0]) is not int:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError()
    return row[0]


def _select_by_identity(
    connection: sqlite3.Connection,
    identity: Mapping[str, Any],
) -> tuple[str] | None:
    return connection.execute(
        f"""
        SELECT decision_json FROM {PRIMARY_TABLE}
        WHERE decision_id = ?
           OR idempotency_key = ?
           OR audit_receipt_reference = ?
        """.strip(),
        (
            identity["decision_id"],
            identity["idempotency_key"],
            identity["audit_receipt_reference"],
        ),
    ).fetchone()


def _row_to_decision(row: tuple[str]) -> dict[str, Any]:
    if len(row) != 1 or type(row[0]) is not str:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError()
    try:
        decision = json.loads(row[0])
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError() from exc
    if not isinstance(decision, dict) or tuple(decision) != DECISION_FIELDS:
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError()
    material = {
        field: decision[field]
        for field in DECISION_FIELDS
        if field != "decision_canonical_hash"
    }
    if (
        not _is_lower_hex_64(decision["decision_canonical_hash"])
        or not hmac.compare_digest(
            decision["decision_canonical_hash"],
            _canonical_sha256(material),
        )
    ):
        raise IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError()
    return decision


def _identity_matches(
    decision: Mapping[str, Any],
    identity: Mapping[str, Any],
) -> bool:
    return all(decision.get(field) == value for field, value in identity.items())


def record_identity_ready_governed_nonproduction_human_review_decision(
    ledger: IdentityReadyGovernedNonproductionHumanReviewDecisionLedger,
    request: Mapping[str, Any],
    *,
    server_binding_safe_hash: str,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        validated = validate_identity_ready_governed_review_decision_request(
            request,
            server_binding_safe_hash=server_binding_safe_hash,
        )
    except IdentityReadyGovernedNonproductionHumanReviewDecisionValidationError as exc:
        return None, _receipt(exc.outcome)

    identity = _identity_for(validated)
    try:
        connection = ledger._connect()
    except IdentityReadyGovernedNonproductionHumanReviewDecisionLedgerUnavailable:
        return None, _receipt(
            "bounded_identity_ready_decision_ledger_failure",
            identity=identity,
        )

    row_count_before: int | None = None
    decision: dict[str, Any] | None = None
    try:
        ledger._ensure_schema(connection)
        row_count_before = _row_count(connection)
        row = _select_by_identity(connection, identity)
        if row is not None:
            try:
                existing = _row_to_decision(row)
            except IdentityReadyGovernedNonproductionHumanReviewDecisionIntegrityError:
                return None, _receipt(
                    "blocked_idempotency_conflict",
                    identity=identity,
                    row_count_before=row_count_before,
                    row_count_after=row_count_before,
                )
            if not _identity_matches(existing, identity):
                return None, _receipt(
                    "blocked_idempotency_conflict",
                    identity=identity,
                    row_count_before=row_count_before,
                    row_count_after=row_count_before,
                )
            return existing, _receipt(
                "already_exists_same_identity_ready_human_review_decision",
                decision=existing,
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )

        decision = _build_decision(identity, ledger.clock())
        ledger._insert_record(connection, decision)
        if ledger.before_commit_hook is not None:
            ledger.before_commit_hook()
        connection.commit()
    except (sqlite3.Error, TypeError, ValueError, RuntimeError):
        try:
            connection.rollback()
        except sqlite3.Error:
            pass
        return None, _receipt(
            "bounded_identity_ready_decision_ledger_failure",
            identity=identity,
            row_count_before=row_count_before,
            row_count_after=row_count_before,
        )
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass

    if ledger.after_commit_hook is not None:
        try:
            ledger.after_commit_hook()
        except Exception:
            return None, _receipt(
                "paused_identity_ready_decision_commit_ambiguity",
                identity=identity,
                row_count_before=row_count_before,
                row_count_after=(
                    row_count_before + 1
                    if row_count_before is not None
                    else None
                ),
            )

    return decision, _receipt(
        "created_exactly_one_identity_ready_human_review_decision",
        decision=decision,
        mutation_count=1,
        row_count_before=row_count_before,
        row_count_after=(
            row_count_before + 1 if row_count_before is not None else None
        ),
    )
