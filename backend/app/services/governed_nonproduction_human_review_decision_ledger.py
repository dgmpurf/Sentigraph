from __future__ import annotations

import hashlib
import hmac
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping


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
RECEIPT_OUTCOME_INVARIANTS = {
    "created_exactly_one_human_review_decision": (
        True,
        False,
        1,
        True,
        False,
        True,
    ),
    "already_exists_same_human_review_decision": (
        False,
        True,
        0,
        True,
        False,
        True,
    ),
    "blocked_unsupported_decision_type": (
        False,
        False,
        0,
        False,
        False,
        True,
    ),
    "blocked_binding_or_snapshot_mismatch": (
        False,
        False,
        0,
        False,
        False,
        True,
    ),
    "blocked_idempotency_conflict": (
        False,
        False,
        0,
        False,
        True,
        True,
    ),
    "paused_pending_read_only_idempotency_verification": (
        False,
        False,
        0,
        False,
        False,
        False,
    ),
    "bounded_decision_ledger_failure": (
        False,
        False,
        0,
        False,
        False,
        False,
    ),
}
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

LOGICAL_TARGET_LABEL = (
    "runtime/governed_nonproduction_human_review_decisions/"
    "review_decisions_v0_1.sqlite3"
)
PRIMARY_TABLE = "governed_nonproduction_human_review_decisions_v0_1"
LEDGER_SCOPE = "governed_nonproduction_record_human_review_only"
DECISION_STATUS = "recorded_append_only_nonproduction"

_FROZEN_SERVER_OWNED_CONTEXT = dict(SERVER_OWNED_CONTEXT)
_IDEMPOTENCY_FIELDS = (
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
_JSON_FIELDS = (
    "allowed_follow_up_labels",
    "blocked_follow_up_labels",
    "warnings",
    "blockers",
)
_BOOLEAN_FIELDS = (
    "reviewer_identity_verified",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_changed",
    "production_case_changed",
    "downstream_runtime_called",
    "correction_or_revocation_performed",
    "deleted_or_updated",
)


class GovernedNonproductionHumanReviewDecisionValidationError(ValueError):
    def __init__(self, outcome: str) -> None:
        super().__init__(outcome)
        self.outcome = outcome


class GovernedNonproductionHumanReviewDecisionLedgerUnavailable(RuntimeError):
    pass


class GovernedNonproductionHumanReviewDecisionIntegrityError(RuntimeError):
    pass


class GovernedNonproductionHumanReviewDecisionCommitAmbiguity(RuntimeError):
    pass


def _canonical_sha256(value: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_clock() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00",
        "Z",
    )


def validate_governed_nonproduction_human_review_decision_request(
    request: Mapping[str, Any],
) -> dict[str, str]:
    if not isinstance(request, dict) or tuple(request) != REQUEST_FIELDS:
        raise GovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_binding_or_snapshot_mismatch"
        )
    if any(type(request[field]) is not str for field in REQUEST_FIELDS):
        raise GovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_binding_or_snapshot_mismatch"
        )
    if (
        request["request_schema"] != REQUEST_SCHEMA
        or request["request_version"] != REQUEST_VERSION
    ):
        raise GovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_binding_or_snapshot_mismatch"
        )
    if request["decision_type"] not in DECISION_TYPES:
        raise GovernedNonproductionHumanReviewDecisionValidationError(
            "blocked_unsupported_decision_type"
        )
    return {field: request[field] for field in REQUEST_FIELDS}


def _formal_target_selected(path: Path) -> bool:
    normalized = path.as_posix().rstrip("/")
    return normalized == LOGICAL_TARGET_LABEL or normalized.endswith(
        f"/{LOGICAL_TARGET_LABEL}"
    )


def _receipt(
    outcome: str,
    *,
    decision: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    row_count_before: int | None = None,
    row_count_after: int | None = None,
) -> dict[str, Any]:
    identity = identity or {}
    created, reused, mutation, exact, conflict, append_only = (
        RECEIPT_OUTCOME_INVARIANTS[outcome]
    )
    source = decision or identity
    blockers = [] if outcome in RECEIPT_OUTCOMES[:2] else [outcome]
    values = {
        "receipt_schema": RECEIPT_SCHEMA,
        "receipt_version": RECEIPT_VERSION,
        "outcome": outcome,
        "audit_receipt_reference": source.get("audit_receipt_reference"),
        "decision_id": source.get("decision_id"),
        "idempotency_key": source.get("idempotency_key"),
        "decision_type": source.get("decision_type"),
        "decision_status": source.get(
            "decision_status",
            "decision_not_recorded",
        ),
        "decision_canonical_hash": source.get("decision_canonical_hash"),
        "created_new_entry": created,
        "reused_existing_entry": reused,
        "mutation_count": mutation,
        "decision_row_count_before": row_count_before,
        "decision_row_count_after": row_count_after,
        "exact_expected_entry_present": exact,
        "conflicting_entry_present": conflict,
        "unrelated_entry_changed": False,
        "append_only_verified": append_only,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_evidenceitem_changed": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "correction_or_revocation_performed": False,
        "deleted_or_updated": False,
        "warnings": [],
        "blockers": blockers,
    }
    return {field: values[field] for field in RECEIPT_FIELDS}


def _identity_for(decision_type: str) -> dict[str, Any]:
    material = {
        "request_schema": REQUEST_SCHEMA,
        "request_version": REQUEST_VERSION,
        "decision_type": decision_type,
        **SERVER_OWNED_CONTEXT,
    }
    idempotency_key = _canonical_sha256(
        {field: material[field] for field in _IDEMPOTENCY_FIELDS}
    )
    identifier_suffix = idempotency_key[:32]
    return {
        "decision_id": f"ghrd-{identifier_suffix}",
        "idempotency_key": idempotency_key,
        "audit_receipt_reference": f"ghrd-receipt-{identifier_suffix}",
        "ledger_scope": LEDGER_SCOPE,
        "decision_type": decision_type,
        "decision_status": DECISION_STATUS,
        **SERVER_OWNED_CONTEXT,
    }


def _build_decision(identity: Mapping[str, Any], recorded_at: str) -> dict[str, Any]:
    values = {
        "decision_schema": DECISION_SCHEMA,
        "decision_version": DECISION_VERSION,
        **identity,
        "recorded_at": recorded_at,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_evidenceitem_changed": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "correction_or_revocation_performed": False,
        "deleted_or_updated": False,
        "allowed_follow_up_labels": list(ALLOWED_FOLLOW_UP_LABELS),
        "blocked_follow_up_labels": list(BLOCKED_FOLLOW_UP_LABELS),
        "warnings": [],
        "blockers": [],
    }
    values["decision_canonical_hash"] = _canonical_sha256(values)
    return {field: values[field] for field in DECISION_FIELDS}


class GovernedNonproductionHumanReviewDecisionLedger:
    def __init__(
        self,
        database_path: str | Path | None = None,
        *,
        enabled: bool = False,
        clock: Callable[[], str] | None = None,
        before_commit_hook: Callable[[], None] | None = None,
        after_commit_hook: Callable[[], None] | None = None,
    ) -> None:
        self.database_path = (
            Path(database_path) if database_path is not None else None
        )
        self.enabled = enabled
        self.clock = clock or _utc_clock
        self.before_commit_hook = before_commit_hook
        self.after_commit_hook = after_commit_hook

    def _require_available(self) -> Path:
        if not self.enabled or self.database_path is None:
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable()
        if _formal_target_selected(self.database_path):
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable()
        return self.database_path

    def initialize(self) -> None:
        database_path = self._require_available()
        database_path.parent.mkdir(parents=True, exist_ok=True)
        column_definitions = []
        for field in DECISION_FIELDS:
            data_type = "INTEGER" if field in _BOOLEAN_FIELDS else "TEXT"
            uniqueness = (
                " UNIQUE"
                if field
                in (
                    "decision_id",
                    "idempotency_key",
                    "audit_receipt_reference",
                )
                else ""
            )
            column_definitions.append(
                f'"{field}" {data_type} NOT NULL{uniqueness}'
            )
        statement = (
            f'CREATE TABLE IF NOT EXISTS "{PRIMARY_TABLE}" '
            f"({', '.join(column_definitions)})"
        )
        try:
            with sqlite3.connect(database_path) as connection:
                connection.execute(statement)
                columns = tuple(
                    row[1]
                    for row in connection.execute(
                        f'PRAGMA table_info("{PRIMARY_TABLE}")'
                    )
                )
        except sqlite3.Error as exc:
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable() from exc
        if columns != DECISION_FIELDS:
            raise GovernedNonproductionHumanReviewDecisionIntegrityError()

    def _connect(self) -> sqlite3.Connection:
        database_path = self._require_available()
        try:
            return sqlite3.connect(database_path)
        except sqlite3.Error as exc:
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable() from exc

    def _connect_read_only(self) -> sqlite3.Connection:
        database_path = self._require_available()
        if not database_path.is_file():
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable()
        uri = f"{database_path.resolve().as_uri()}?mode=ro"
        try:
            return sqlite3.connect(uri, uri=True)
        except sqlite3.Error as exc:
            raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable() from exc

    def _insert_record(
        self,
        connection: sqlite3.Connection,
        decision: Mapping[str, Any],
    ) -> None:
        placeholders = ", ".join("?" for _ in DECISION_FIELDS)
        columns = ", ".join(f'"{field}"' for field in DECISION_FIELDS)
        stored_values = []
        for field in DECISION_FIELDS:
            value = decision[field]
            if field in _JSON_FIELDS:
                value = json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            elif field in _BOOLEAN_FIELDS:
                value = int(value)
            stored_values.append(value)
        connection.execute(
            f'INSERT INTO "{PRIMARY_TABLE}" ({columns}) VALUES ({placeholders})',
            stored_values,
        )


def _row_count(connection: sqlite3.Connection) -> int:
    return int(
        connection.execute(
            f'SELECT COUNT(*) FROM "{PRIMARY_TABLE}"'
        ).fetchone()[0]
    )


def _row_to_decision(row: tuple[Any, ...]) -> dict[str, Any]:
    if len(row) != len(DECISION_FIELDS):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    decision = dict(zip(DECISION_FIELDS, row, strict=True))
    try:
        for field in _JSON_FIELDS:
            parsed = json.loads(decision[field])
            if not isinstance(parsed, list) or any(
                type(item) is not str for item in parsed
            ):
                raise ValueError
            decision[field] = parsed
        for field in _BOOLEAN_FIELDS:
            if decision[field] not in (0, 1):
                raise ValueError
            decision[field] = bool(decision[field])
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise GovernedNonproductionHumanReviewDecisionIntegrityError() from exc
    stored_hash = decision["decision_canonical_hash"]
    material = {
        field: decision[field]
        for field in DECISION_FIELDS
        if field != "decision_canonical_hash"
    }
    computed_hash = _canonical_sha256(material)
    if not isinstance(stored_hash, str) or not hmac.compare_digest(
        stored_hash,
        computed_hash,
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    return {field: decision[field] for field in DECISION_FIELDS}


def _select_by_identity(
    connection: sqlite3.Connection,
    identity: Mapping[str, Any],
) -> tuple[Any, ...] | None:
    return connection.execute(
        f'SELECT * FROM "{PRIMARY_TABLE}" '
        "WHERE idempotency_key = ? OR decision_id = ? "
        "OR audit_receipt_reference = ?",
        (
            identity["idempotency_key"],
            identity["decision_id"],
            identity["audit_receipt_reference"],
        ),
    ).fetchone()


def _identity_matches(
    decision: Mapping[str, Any],
    identity: Mapping[str, Any],
) -> bool:
    fields = (
        "decision_id",
        "idempotency_key",
        "audit_receipt_reference",
        "ledger_scope",
        "decision_type",
        *tuple(SERVER_OWNED_CONTEXT),
        "decision_status",
    )
    return all(decision[field] == identity[field] for field in fields)


def _resolve_commit_ambiguity(
    ledger: GovernedNonproductionHumanReviewDecisionLedger,
    decision: Mapping[str, Any],
    identity: Mapping[str, Any],
    row_count_before: int,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        with ledger._connect_read_only() as connection:
            row_count_after = _row_count(connection)
            row = _select_by_identity(connection, identity)
            if row is None:
                return None, _receipt(
                    "paused_pending_read_only_idempotency_verification",
                    identity=identity,
                    row_count_before=row_count_before,
                    row_count_after=row_count_after,
                )
            try:
                loaded = _row_to_decision(row)
            except GovernedNonproductionHumanReviewDecisionIntegrityError:
                return None, _receipt(
                    "blocked_idempotency_conflict",
                    identity=identity,
                    row_count_before=row_count_before,
                    row_count_after=row_count_after,
                )
    except (
        GovernedNonproductionHumanReviewDecisionLedgerUnavailable,
        sqlite3.Error,
    ):
        return None, _receipt(
            "paused_pending_read_only_idempotency_verification",
            identity=identity,
        )
    if loaded != decision:
        return None, _receipt(
            "blocked_idempotency_conflict",
            identity=identity,
            row_count_before=row_count_before,
            row_count_after=row_count_after,
        )
    return loaded, _receipt(
        "created_exactly_one_human_review_decision",
        decision=loaded,
        row_count_before=row_count_before,
        row_count_after=row_count_after,
    )


def record_governed_nonproduction_human_review_decision(
    ledger: GovernedNonproductionHumanReviewDecisionLedger,
    request: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    try:
        validated = validate_governed_nonproduction_human_review_decision_request(
            request
        )
    except GovernedNonproductionHumanReviewDecisionValidationError as exc:
        decision_type = request.get("decision_type") if isinstance(request, dict) else None
        return None, _receipt(
            exc.outcome,
            identity={"decision_type": decision_type},
        )
    if dict(SERVER_OWNED_CONTEXT) != _FROZEN_SERVER_OWNED_CONTEXT:
        return None, _receipt(
            "blocked_binding_or_snapshot_mismatch",
            identity={"decision_type": validated["decision_type"]},
        )
    identity = _identity_for(validated["decision_type"])
    try:
        connection = ledger._connect()
    except GovernedNonproductionHumanReviewDecisionLedgerUnavailable:
        return None, _receipt(
            "bounded_decision_ledger_failure",
            identity=identity,
        )
    try:
        row_count_before = _row_count(connection)
        row = _select_by_identity(connection, identity)
        if row is not None:
            try:
                existing = _row_to_decision(row)
            except GovernedNonproductionHumanReviewDecisionIntegrityError:
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
                "already_exists_same_human_review_decision",
                decision=existing,
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )
        decision = _build_decision(identity, ledger.clock())
        try:
            ledger._insert_record(connection, decision)
        except (sqlite3.Error, TypeError, ValueError):
            connection.rollback()
            return None, _receipt(
                "bounded_decision_ledger_failure",
                identity=identity,
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )
        if ledger.before_commit_hook is not None:
            try:
                ledger.before_commit_hook()
            except Exception:
                connection.rollback()
                return None, _receipt(
                    "bounded_decision_ledger_failure",
                    identity=identity,
                    row_count_before=row_count_before,
                    row_count_after=row_count_before,
                )
        try:
            connection.commit()
        except sqlite3.Error:
            connection.close()
            return _resolve_commit_ambiguity(
                ledger,
                decision,
                identity,
                row_count_before,
            )
    except sqlite3.Error:
        return None, _receipt(
            "bounded_decision_ledger_failure",
            identity=identity,
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
            return _resolve_commit_ambiguity(
                ledger,
                decision,
                identity,
                row_count_before,
            )
    return decision, _receipt(
        "created_exactly_one_human_review_decision",
        decision=decision,
        row_count_before=row_count_before,
        row_count_after=row_count_before + 1,
    )


def get_governed_nonproduction_human_review_decision(
    ledger: GovernedNonproductionHumanReviewDecisionLedger,
    decision_id: str,
) -> dict[str, Any] | None:
    try:
        with ledger._connect_read_only() as connection:
            row = connection.execute(
                f'SELECT * FROM "{PRIMARY_TABLE}" WHERE decision_id = ?',
                (decision_id,),
            ).fetchone()
    except sqlite3.Error as exc:
        raise GovernedNonproductionHumanReviewDecisionLedgerUnavailable() from exc
    if row is None:
        return None
    return _row_to_decision(row)
