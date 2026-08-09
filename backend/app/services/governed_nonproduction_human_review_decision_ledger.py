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


def _identity_for_context(
    decision_type: str,
    context: Mapping[str, Any],
) -> dict[str, Any]:
    if (
        not isinstance(context, dict)
        or tuple(context) != tuple(SERVER_OWNED_CONTEXT)
        or any(
            type(context[field]) is not type(expected)
            for field, expected in SERVER_OWNED_CONTEXT.items()
        )
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    material = {
        "request_schema": REQUEST_SCHEMA,
        "request_version": REQUEST_VERSION,
        "decision_type": decision_type,
        **context,
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
        **context,
    }


def _identity_for(decision_type: str) -> dict[str, Any]:
    return _identity_for_context(decision_type, SERVER_OWNED_CONTEXT)


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


FORMAL_TARGET_KIND = (
    "dedicated_local_sqlite_nonproduction_human_review_decision_ledger"
)
FORMAL_LOGICAL_TARGET_LABEL = LOGICAL_TARGET_LABEL
FORMAL_PRIMARY_TABLE = PRIMARY_TABLE
FORMAL_CONTRACT_RELATIVE_PATH = (
    "docs/architecture/"
    "sentigraph_mvp_f12_p1_formal_decision_ledger_governance_contract_v1_0.md"
)
FORMAL_CONTRACT_SHA256 = (
    "0d0e4c0c12a534eb5f523fffb4430f223480339d197ec031c5621f6e1312b4b8"
)
FORMAL_TARGET_IDENTITY_SAFE_HASH = (
    "4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202"
)
FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH = (
    "de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d"
)
FORMAL_SCHEMA_VERSION = "0.1"
INITIALIZATION_RECEIPT_SCHEMA = (
    "sentigraph_governed_nonproduction_human_review_decision_ledger_"
    "initialization_receipt_v0_1"
)
INITIALIZATION_RECEIPT_VERSION = "0.1"
INITIALIZATION_RECEIPT_FIELDS = (
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
INITIALIZATION_RECEIPT_OUTCOMES = (
    "initialized_exact_empty_formal_decision_ledger",
    "verified_existing_exact_empty_formal_decision_ledger",
    "blocked_existing_nonempty_formal_decision_ledger",
    "blocked_formal_decision_ledger_schema_mismatch",
    "blocked_formal_decision_ledger_target_identity_mismatch",
    "paused_formal_decision_ledger_initialization_ambiguous",
    "bounded_formal_decision_ledger_initialization_failure",
)
_FORMAL_UNIQUE_FIELDS = (
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
)
_FORMAL_COLUMN_DEFINITIONS = tuple(
    f'"{field}" '
    f'{"INTEGER" if field in _BOOLEAN_FIELDS else "TEXT"} NOT NULL'
    f'{" UNIQUE" if field in _FORMAL_UNIQUE_FIELDS else ""}'
    for field in DECISION_FIELDS
)
FORMAL_CREATE_TABLE_STATEMENT = (
    f'CREATE TABLE "{FORMAL_PRIMARY_TABLE}" '
    f"({', '.join(_FORMAL_COLUMN_DEFINITIONS)})"
)


def canonical_initialization_receipt_sha256(
    receipt: Mapping[str, Any],
) -> str:
    if not isinstance(receipt, dict) or tuple(receipt) != (
        INITIALIZATION_RECEIPT_FIELDS
    ):
        raise ValueError("invalid_initialization_receipt_shape")
    return _canonical_sha256(receipt)


def _initialization_receipt(
    outcome: str,
    *,
    target_preexistence_classification: str,
    initialization_action: str,
    sqlite_connection_open_count: int,
    schema_ddl_statement_count: int,
    decision_row_count: int | None = None,
    exact_schema_verified: bool | None = None,
    exact_empty_verified: bool | None = None,
    integrity_result: str = "not_observed",
    final_sidecar_count: int | None = None,
    warnings: list[str] | None = None,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    if outcome not in INITIALIZATION_RECEIPT_OUTCOMES:
        raise ValueError("invalid_initialization_outcome")
    values = {
        "receipt_schema": INITIALIZATION_RECEIPT_SCHEMA,
        "receipt_version": INITIALIZATION_RECEIPT_VERSION,
        "outcome": outcome,
        "target_kind": FORMAL_TARGET_KIND,
        "target_logical_label": FORMAL_LOGICAL_TARGET_LABEL,
        "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "target_preexistence_classification": (
            target_preexistence_classification
        ),
        "initialization_action": initialization_action,
        "schema_version": FORMAL_SCHEMA_VERSION,
        "primary_table": FORMAL_PRIMARY_TABLE,
        "sqlite_connection_open_count": sqlite_connection_open_count,
        "sqlite_connection_reopen_count": 0,
        "schema_ddl_statement_count": schema_ddl_statement_count,
        "decision_table_dml_statement_count": 0,
        "decision_row_count": decision_row_count,
        "exact_schema_verified": exact_schema_verified,
        "exact_empty_verified": exact_empty_verified,
        "integrity_result": integrity_result,
        "final_sidecar_count": final_sidecar_count,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_ready": False,
        "warnings": list(warnings or []),
        "blockers": list(blockers or []),
    }
    return {field: values[field] for field in INITIALIZATION_RECEIPT_FIELDS}


def _strict_json_object(value: str) -> dict[str, Any]:
    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        keys = [key for key, _ in pairs]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate_json_key")
        return dict(pairs)

    def reject_constant(_value: str) -> None:
        raise ValueError("nonstandard_json_constant")

    parsed = json.loads(
        value,
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    if not isinstance(parsed, dict):
        raise ValueError("marked_json_not_object")
    return parsed


def _extract_exact_marked_json_object(
    contract: str,
    *,
    begin_marker: str,
    end_marker: str,
) -> dict[str, Any]:
    if contract.count(begin_marker) != 1 or contract.count(end_marker) != 1:
        raise ValueError("marked_object_count_mismatch")
    begin = contract.index(begin_marker) + len(begin_marker)
    end = contract.index(end_marker, begin)
    marked = contract[begin:end]
    fence = "```json"
    if marked.count(fence) != 1:
        raise ValueError("marked_json_fence_mismatch")
    json_begin = marked.index(fence) + len(fence)
    if marked.count("```", json_begin) != 1:
        raise ValueError("marked_json_closing_fence_mismatch")
    json_end = marked.index("```", json_begin)
    return _strict_json_object(marked[json_begin:json_end].strip())


def _expected_formal_target_identity() -> dict[str, Any]:
    return {
        "target_identity_schema": (
            "sentigraph_governed_nonproduction_human_review_decision_ledger_"
            "formal_target_identity_v0_1"
        ),
        "target_identity_version": "0.1",
        "target_kind": FORMAL_TARGET_KIND,
        "target_logical_label": FORMAL_LOGICAL_TARGET_LABEL,
        "table_count": 1,
        "additional_tables_allowed": False,
        "primary_table": FORMAL_PRIMARY_TABLE,
        "schema_version": FORMAL_SCHEMA_VERSION,
        "owner_module": (
            "backend/app/services/"
            "governed_nonproduction_human_review_decision_ledger.py"
        ),
        "owner_class": "GovernedNonproductionHumanReviewDecisionLedger",
        "decision_schema": DECISION_SCHEMA,
        "decision_version": DECISION_VERSION,
        "decision_fields": list(DECISION_FIELDS),
        "integer_boolean_columns": list(_BOOLEAN_FIELDS),
        "canonical_json_columns": list(_JSON_FIELDS),
        "unique_columns": list(_FORMAL_UNIQUE_FIELDS),
        "ledger_scope": LEDGER_SCOPE,
        "decision_status": DECISION_STATUS,
        "append_only_policy": "plain_insert_only_no_existing_row_mutation",
    }


def _known_path_has_symlink(root: Path, relative_parts: tuple[str, ...]) -> bool:
    current = root
    for part in relative_parts:
        current = current / part
        if current.is_symlink():
            return True
    return False


def _validate_exact_formal_decision_ledger_profile(
    repository_root: str | Path,
) -> tuple[Path, Path]:
    supplied_root = Path(repository_root)
    if supplied_root.is_symlink() or not supplied_root.is_dir():
        raise ValueError("repository_root_mismatch")
    root = supplied_root.resolve(strict=True)
    if not (root / "backend/app/services").is_dir():
        raise ValueError("repository_structure_mismatch")
    contract_parts = tuple(FORMAL_CONTRACT_RELATIVE_PATH.split("/"))
    if _known_path_has_symlink(root, contract_parts):
        raise ValueError("contract_path_symlink_mismatch")
    contract_path = root.joinpath(*contract_parts)
    if not contract_path.is_file():
        raise ValueError("contract_file_missing")
    contract_bytes = contract_path.read_bytes()
    if hashlib.sha256(contract_bytes).hexdigest() != FORMAL_CONTRACT_SHA256:
        raise ValueError("contract_file_hash_mismatch")
    contract = contract_bytes.decode("utf-8")
    identity = _extract_exact_marked_json_object(
        contract,
        begin_marker="<!-- TARGET_IDENTITY_OBJECT_BEGIN -->",
        end_marker="<!-- TARGET_IDENTITY_OBJECT_END -->",
    )
    authorization = _extract_exact_marked_json_object(
        contract,
        begin_marker="<!-- TARGET_AUTHORIZATION_OBJECT_BEGIN -->",
        end_marker="<!-- TARGET_AUTHORIZATION_OBJECT_END -->",
    )
    if (
        _canonical_sha256(identity) != FORMAL_TARGET_IDENTITY_SAFE_HASH
        or identity != _expected_formal_target_identity()
    ):
        raise ValueError("target_identity_mismatch")
    if _canonical_sha256(authorization) != (
        FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
    ):
        raise ValueError("target_authorization_mismatch")
    required_authorization = {
        "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "authorized_operation": "exact_empty_formal_target_initialization_only",
        "target_resolution_mode": "internal_exact_logical_label_only",
        "required_initial_state": "contract_defined_uninitialized",
        "allowed_success_state": "initialized_exact_empty",
        "formal_target_access_session_maximum": 1,
        "sqlite_connection_open_maximum": 1,
        "sqlite_connection_reopen_maximum": 0,
        "schema_ddl_statement_count_maximum": 1,
        "decision_table_dml_statement_count_maximum": 0,
        "decision_insert_maximum": 0,
        "decision_writer_invocation_maximum": 0,
        "route_invocation_maximum": 0,
        "automatic_retry_allowed": False,
        "caller_supplied_physical_target_allowed": False,
        "environment_target_override_allowed": False,
        "first_real_decision_allowed": False,
        "initialization_receipt_fields": list(INITIALIZATION_RECEIPT_FIELDS),
        "initialization_receipt_outcomes": list(
            INITIALIZATION_RECEIPT_OUTCOMES
        ),
    }
    if any(
        authorization.get(field) != expected
        for field, expected in required_authorization.items()
    ):
        raise ValueError("target_authorization_contract_mismatch")
    target_parts = tuple(FORMAL_LOGICAL_TARGET_LABEL.split("/"))
    if (
        not target_parts
        or any(part in {"", ".", ".."} for part in target_parts)
        or Path(FORMAL_LOGICAL_TARGET_LABEL).is_absolute()
    ):
        raise ValueError("target_logical_label_mismatch")
    target = root.joinpath(*target_parts)
    try:
        target.resolve(strict=False).relative_to(root)
    except ValueError as exc:
        raise ValueError("target_path_escape") from exc
    if _known_path_has_symlink(root, target_parts):
        raise ValueError("target_path_symlink_escape")
    return root, target


def _open_exact_formal_decision_ledger_connection(
    path: Path,
    *,
    read_only: bool,
) -> sqlite3.Connection:
    if read_only:
        return sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    return sqlite3.connect(path)


def _exact_formal_schema_verified(connection: sqlite3.Connection) -> bool:
    objects = connection.execute(
        "SELECT type, name, sql FROM sqlite_master "
        "WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name"
    ).fetchall()
    if objects != [
        ("table", FORMAL_PRIMARY_TABLE, FORMAL_CREATE_TABLE_STATEMENT)
    ]:
        return False
    columns = connection.execute(
        f'PRAGMA table_info("{FORMAL_PRIMARY_TABLE}")'
    ).fetchall()
    if len(columns) != len(DECISION_FIELDS):
        return False
    for position, (column, field) in enumerate(zip(columns, DECISION_FIELDS)):
        cid, name, data_type, not_null, default, primary_key = column
        expected_type = "INTEGER" if field in _BOOLEAN_FIELDS else "TEXT"
        if (
            cid != position
            or name != field
            or data_type.upper() != expected_type
            or not_null != 1
            or default is not None
            or primary_key != 0
        ):
            return False
    indexes = connection.execute(
        f'PRAGMA index_list("{FORMAL_PRIMARY_TABLE}")'
    ).fetchall()
    if len(indexes) != len(_FORMAL_UNIQUE_FIELDS):
        return False
    unique_columns = set()
    for index in indexes:
        _sequence, name, unique, origin, partial = index[:5]
        if (
            unique != 1
            or origin != "u"
            or partial != 0
            or not name.startswith(
                f"sqlite_autoindex_{FORMAL_PRIMARY_TABLE}_"
            )
        ):
            return False
        index_columns = connection.execute(
            f'PRAGMA index_info("{name}")'
        ).fetchall()
        if len(index_columns) != 1:
            return False
        unique_columns.add(index_columns[0][2])
    return unique_columns == set(_FORMAL_UNIQUE_FIELDS)


def _exact_formal_sidecar_count(target: Path) -> int:
    return sum(
        int(Path(f"{target}{suffix}").exists())
        for suffix in ("-wal", "-shm", "-journal")
    )


def _initialize_exact_formal_decision_ledger_once(
    target: Path,
) -> dict[str, Any]:
    if target.is_symlink():
        return _initialization_receipt(
            "blocked_formal_decision_ledger_target_identity_mismatch",
            target_preexistence_classification="target_identity_mismatch",
            initialization_action="blocked_before_target_access",
            sqlite_connection_open_count=0,
            schema_ddl_statement_count=0,
            blockers=["blocked_formal_decision_ledger_target_identity_mismatch"],
        )
    target_existed = target.exists()
    if target_existed and not target.is_file():
        return _initialization_receipt(
            "blocked_formal_decision_ledger_target_identity_mismatch",
            target_preexistence_classification="target_identity_mismatch",
            initialization_action="blocked_before_sqlite_open",
            sqlite_connection_open_count=0,
            schema_ddl_statement_count=0,
            blockers=["blocked_formal_decision_ledger_target_identity_mismatch"],
        )
    if not target_existed:
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.parent.is_symlink() or target.is_symlink():
            return _initialization_receipt(
                "blocked_formal_decision_ledger_target_identity_mismatch",
                target_preexistence_classification="target_identity_mismatch",
                initialization_action="blocked_before_sqlite_open",
                sqlite_connection_open_count=0,
                schema_ddl_statement_count=0,
                blockers=[
                    "blocked_formal_decision_ledger_target_identity_mismatch"
                ],
            )
    preexistence = "existing_unclassified" if target_existed else "absent"
    try:
        connection = _open_exact_formal_decision_ledger_connection(
            target,
            read_only=target_existed,
        )
    except sqlite3.Error:
        return _initialization_receipt(
            "bounded_formal_decision_ledger_initialization_failure",
            target_preexistence_classification=preexistence,
            initialization_action="connection_open_failed",
            sqlite_connection_open_count=0,
            schema_ddl_statement_count=0,
            blockers=["bounded_formal_decision_ledger_initialization_failure"],
        )
    schema_ddl_statement_count = 0
    outcome = "bounded_formal_decision_ledger_initialization_failure"
    action = "bounded_verification_failure"
    classification = preexistence
    row_count: int | None = None
    exact_schema: bool | None = None
    exact_empty: bool | None = None
    integrity_result = "not_observed"
    blockers = ["bounded_formal_decision_ledger_initialization_failure"]
    commit_ambiguous = False
    try:
        if not target_existed:
            schema_ddl_statement_count = 1
            try:
                connection.execute(FORMAL_CREATE_TABLE_STATEMENT)
            except sqlite3.Error:
                action = "schema_creation_failed"
            else:
                try:
                    connection.commit()
                except sqlite3.Error:
                    outcome = (
                        "paused_formal_decision_ledger_initialization_ambiguous"
                    )
                    action = "commit_outcome_ambiguous"
                    blockers = [outcome]
                    commit_ambiguous = True
        if not commit_ambiguous and action != "schema_creation_failed":
            try:
                exact_schema = _exact_formal_schema_verified(connection)
                if not exact_schema:
                    outcome = (
                        "blocked_formal_decision_ledger_schema_mismatch"
                    )
                    classification = "schema_mismatch_or_unrelated_table"
                    action = "verification_blocked_schema_mismatch"
                    exact_empty = None
                    blockers = [outcome]
                else:
                    row_count = connection.execute(
                        f'SELECT COUNT(*) FROM "{FORMAL_PRIMARY_TABLE}"'
                    ).fetchone()[0]
                    exact_empty = row_count == 0
                    integrity_rows = connection.execute(
                        "PRAGMA integrity_check"
                    ).fetchall()
                    integrity_result = (
                        "ok" if integrity_rows == [("ok",)] else "failed"
                    )
                    if integrity_result != "ok":
                        action = "integrity_verification_failed"
                    elif row_count > 0:
                        outcome = (
                            "blocked_existing_nonempty_formal_decision_ledger"
                        )
                        classification = "existing_nonempty"
                        action = "verification_blocked_existing_nonempty"
                        blockers = [outcome]
                    elif target_existed:
                        outcome = (
                            "verified_existing_exact_empty_formal_decision_ledger"
                        )
                        classification = "existing_exact_empty"
                        action = (
                            "verified_existing_exact_schema_without_mutation"
                        )
                        blockers = []
                    else:
                        outcome = (
                            "initialized_exact_empty_formal_decision_ledger"
                        )
                        classification = "absent"
                        action = "created_exact_schema"
                        blockers = []
            except (sqlite3.Error, TypeError, IndexError):
                classification = "malformed_or_unclassifiable"
                action = "bounded_verification_failure"
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            outcome = "bounded_formal_decision_ledger_initialization_failure"
            action = "connection_close_failure"
            blockers = [outcome]
    final_sidecar_count = _exact_formal_sidecar_count(target)
    if outcome in INITIALIZATION_RECEIPT_OUTCOMES[:2] and (
        final_sidecar_count != 0
    ):
        outcome = "bounded_formal_decision_ledger_initialization_failure"
        action = "unexpected_final_sidecar"
        blockers = [outcome]
    return _initialization_receipt(
        outcome,
        target_preexistence_classification=classification,
        initialization_action=action,
        sqlite_connection_open_count=1,
        schema_ddl_statement_count=schema_ddl_statement_count,
        decision_row_count=row_count,
        exact_schema_verified=exact_schema,
        exact_empty_verified=exact_empty,
        integrity_result=integrity_result,
        final_sidecar_count=final_sidecar_count,
        blockers=blockers,
    )


def initialize_exact_formal_governed_nonproduction_human_review_decision_ledger(
    *,
    repository_root: str | Path,
    enabled: bool = False,
) -> dict[str, Any]:
    if not enabled:
        return _initialization_receipt(
            "bounded_formal_decision_ledger_initialization_failure",
            target_preexistence_classification="not_observed",
            initialization_action="disabled_no_target_access",
            sqlite_connection_open_count=0,
            schema_ddl_statement_count=0,
            blockers=["formal_initialization_disabled"],
        )
    try:
        _root, target = _validate_exact_formal_decision_ledger_profile(
            repository_root
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return _initialization_receipt(
            "blocked_formal_decision_ledger_target_identity_mismatch",
            target_preexistence_classification="target_identity_mismatch",
            initialization_action="blocked_before_target_access",
            sqlite_connection_open_count=0,
            schema_ddl_statement_count=0,
            blockers=["blocked_formal_decision_ledger_target_identity_mismatch"],
        )
    return _initialize_exact_formal_decision_ledger_once(target)


P3_ACTIVATION_SCHEMA = (
    "sentigraph_mvp_f12_p3_first_exact_formal_human_review_decision_"
    "activation_v0_1"
)
P3_ACTIVATION_VERSION = "0.1"
P3_ACTIVATION_FIELDS = (
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
P3_PRE_WRITER_BINDING_FIELDS = (
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
P3_RESULT_SCHEMA = (
    "sentigraph_mvp_f12_p3_first_exact_formal_human_review_decision_"
    "result_v0_1"
)
P3_RESULT_VERSION = "0.1"
P3_RESULT_FIELDS = (
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
P3_ACCEPTED_P2_INITIALIZATION_RECEIPT_CANONICAL_SHA256 = (
    "5d65da59110352def9c0160f78f38a94251ff51adb918c8c1ea142a44b0b4874"
)
P3_EXACT_APPROVAL_SHA256 = (
    "4ee5fcb567bbd3a43681cd3b90e95b8147a110df84862f365d749d8a82f78fd7"
)
P3_EXPECTED_IDEMPOTENCY_KEY = (
    "b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db"
)
P3_SERVICE_RELATIVE_PATH = (
    "backend/app/services/"
    "governed_nonproduction_human_review_decision_ledger.py"
)
P3_TEST_RELATIVE_PATH = (
    "backend/app/tests/"
    "test_mvp_f12_p3_first_formal_human_review_decision.py"
)
P3_REPORT_RELATIVE_PATH = (
    "docs/health/"
    "sentigraph_mvp_f12_p3_first_formal_human_review_decision_report_v1_0.md"
)

_P3_FIXED_ACTIVATION_VALUES = {
    "activation_schema": P3_ACTIVATION_SCHEMA,
    "activation_version": P3_ACTIVATION_VERSION,
    "milestone_id": "MVP-F12-P3",
    "repository_identity": "dgmpurf/Sentigraph",
    "required_branch": "main",
    "starting_commit": "6848a5d6c5bb52174b9a336c7ac7c12ac69ae4b6",
    "baseline_v1_4_blob": "8e280300ff3db283ba7fe2aaf64063b4bf63597e",
    "accepted_f11_p1_contract_blob": (
        "29d3806a535680247713ae317c1d1c9097f69d06"
    ),
    "accepted_f11_p1_contract_sha256": (
        "dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152"
    ),
    "accepted_effective_f11_commit": (
        "1300e10fba526c0d37f310a004e17a17a9c65420"
    ),
    "accepted_f11_decision_ledger_service_blob": (
        "b9d74ca5d3d593fbe27043dcb7db0a76e25d4056"
    ),
    "accepted_f12_p1_contract_blob": (
        "c2b9645ba1ee2724ba4a023fa267d4dfb5059302"
    ),
    "accepted_f12_p1_contract_sha256": FORMAL_CONTRACT_SHA256,
    "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
    "target_authorization_contract_safe_hash": (
        FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
    ),
    "accepted_p2_service_blob": (
        "13ade443cd3186d17e8f10af229f5f7ea82984ed"
    ),
    "accepted_p2_test_blob": "5e9dd6c8b60643926c6eea73c1b49345b114eea4",
    "accepted_p2_report_blob": (
        "1626b16db8362c3f32a00f89acecb625f50412fd"
    ),
    "accepted_p2_initialization_receipt_canonical_sha256": (
        P3_ACCEPTED_P2_INITIALIZATION_RECEIPT_CANONICAL_SHA256
    ),
    "required_formal_target_state": "initialized_exact_empty",
    "accepted_decision_row_count": 0,
    "first_real_decision_type": "keep_pending_human_review",
    "reviewer_role_label": "self_declared_project_owner_role",
    "reviewer_authority_basis_label": (
        "authority_basis_not_independently_validated"
    ),
    "reviewer_identity_verified": False,
    "exact_p3_approval_sha256": P3_EXACT_APPROVAL_SHA256,
    "p3_activation_binding_nonreusable": True,
    "formal_target_access_session_limit": 1,
    "sqlite_connection_open_success_limit": 1,
    "sqlite_connection_reopen_success_limit": 0,
    "formal_operation_invocation_limit": 1,
    "decision_writer_invocation_limit": 1,
    "decision_insert_limit": 1,
    "route_invocation_limit": 0,
    "f10_invocation_limit": 0,
    "automatic_retry_allowed": False,
    "automatic_repair_allowed": False,
    "second_decision_allowed": False,
    "result_artifact_count_limit": 1,
    "result_artifact_binary_read_limit": 1,
    "result_artifact_read_max_bytes": 65537,
    "production_or_downstream_action_limit": 0,
}


def _p3_result(
    outcome: str,
    *,
    activation_hash: str | None = None,
    pre_writer_hash: str | None = None,
    formal_state_before: str = "not_observed",
    formal_state_after: str = "not_changed",
    formal_target_access_session_count: int = 0,
    sqlite_connection_open_count: int = 0,
    formal_writer_invocation_count: int = 0,
    decision_insert_issued_count: int = 0,
    mutation_count: int = 0,
    decision_row_count_before: int | None = None,
    decision_row_count_after: int | None = None,
    exact_schema_verified: bool | None = None,
    integrity_result: str = "not_observed",
    final_sidecar_count: int | None = None,
    decision: Mapping[str, Any] | None = None,
    receipt: Mapping[str, Any] | None = None,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    values = {
        "result_schema": P3_RESULT_SCHEMA,
        "result_version": P3_RESULT_VERSION,
        "outcome": outcome,
        "p3_activation_binding_safe_hash": activation_hash,
        "p3_pre_writer_binding_canonical_sha256": pre_writer_hash,
        "formal_state_before": formal_state_before,
        "formal_state_after": formal_state_after,
        "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "accepted_p2_initialization_receipt_canonical_sha256": (
            P3_ACCEPTED_P2_INITIALIZATION_RECEIPT_CANONICAL_SHA256
        ),
        "formal_target_access_session_count": (
            formal_target_access_session_count
        ),
        "sqlite_connection_open_count": sqlite_connection_open_count,
        "sqlite_connection_reopen_count": 0,
        "formal_writer_invocation_count": formal_writer_invocation_count,
        "decision_insert_issued_count": decision_insert_issued_count,
        "mutation_count": mutation_count,
        "decision_row_count_before": decision_row_count_before,
        "decision_row_count_after": decision_row_count_after,
        "exact_schema_verified": exact_schema_verified,
        "integrity_result": integrity_result,
        "final_sidecar_count": final_sidecar_count,
        "route_invocation_count": 0,
        "f10_invocation_count": 0,
        "decision": dict(decision) if decision is not None else None,
        "receipt": dict(receipt) if receipt is not None else None,
        "warnings": [],
        "blockers": list(blockers or []),
    }
    return {field: values[field] for field in P3_RESULT_FIELDS}


def _p3_expected_pre_writer_binding(
    activation_hash: str,
) -> dict[str, Any]:
    values = {
        "accepted_f11_p1_contract_blob": (
            _P3_FIXED_ACTIVATION_VALUES["accepted_f11_p1_contract_blob"]
        ),
        "accepted_f11_p1_contract_sha256": (
            _P3_FIXED_ACTIVATION_VALUES["accepted_f11_p1_contract_sha256"]
        ),
        "accepted_effective_f11_commit": (
            _P3_FIXED_ACTIVATION_VALUES["accepted_effective_f11_commit"]
        ),
        "accepted_decision_ledger_service_blob": (
            _P3_FIXED_ACTIVATION_VALUES[
                "accepted_f11_decision_ledger_service_blob"
            ]
        ),
        "accepted_request_schema": REQUEST_SCHEMA,
        "accepted_request_version": REQUEST_VERSION,
        "accepted_decision_schema": DECISION_SCHEMA,
        "accepted_decision_version": DECISION_VERSION,
        "accepted_ledger_scope": LEDGER_SCOPE,
        "accepted_decision_status": DECISION_STATUS,
        "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "independently_accepted_p2_initialization_receipt_canonical_sha256": (
            P3_ACCEPTED_P2_INITIALIZATION_RECEIPT_CANONICAL_SHA256
        ),
        "required_formal_target_state": "initialized_exact_empty",
        "first_real_decision_type": "keep_pending_human_review",
        "reviewer_role_label": "self_declared_project_owner_role",
        "reviewer_authority_basis_label": (
            "authority_basis_not_independently_validated"
        ),
        "reviewer_identity_verified": False,
        "p3_activation_binding_safe_hash": activation_hash,
        "p3_activation_binding_nonreusable": True,
        "formal_writer_invocation_limit": 1,
        "automatic_retry_allowed": False,
        "route_invocation_limit": 0,
    }
    return {
        field: values[field] for field in P3_PRE_WRITER_BINDING_FIELDS
    }


def _p3_activation_is_exact(
    activation: Mapping[str, Any],
    activation_hash: str,
    runner_sha256: str,
) -> bool:
    if not isinstance(activation, dict) or tuple(activation) != (
        P3_ACTIVATION_FIELDS
    ):
        return False
    if not isinstance(activation_hash, str) or not hmac.compare_digest(
        _canonical_sha256(activation), activation_hash
    ):
        return False
    if any(
        field not in activation
        or type(activation[field]) is not type(expected)
        or activation[field] != expected
        for field, expected in _P3_FIXED_ACTIVATION_VALUES.items()
    ):
        return False
    dynamic_hash_fields = (
        "post_implementation_service_sha256",
        "post_implementation_test_sha256",
        "pre_execution_report_sha256",
        "repository_external_runner_sha256",
    )
    if any(
        not isinstance(activation[field], str)
        or len(activation[field]) != 64
        or any(character not in "0123456789abcdef" for character in activation[field])
        for field in dynamic_hash_fields
    ):
        return False
    return isinstance(runner_sha256, str) and hmac.compare_digest(
        activation["repository_external_runner_sha256"], runner_sha256
    )


def _p3_repository_file_hashes_are_exact(
    root: Path,
    activation: Mapping[str, Any],
) -> bool:
    expected = (
        (P3_SERVICE_RELATIVE_PATH, "post_implementation_service_sha256"),
        (P3_TEST_RELATIVE_PATH, "post_implementation_test_sha256"),
        (P3_REPORT_RELATIVE_PATH, "pre_execution_report_sha256"),
    )
    try:
        for relative_path, activation_field in expected:
            parts = tuple(relative_path.split("/"))
            if _known_path_has_symlink(root, parts):
                return False
            path = root.joinpath(*parts)
            if not path.is_file() or not hmac.compare_digest(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                activation[activation_field],
            ):
                return False
    except (OSError, TypeError):
        return False
    return True


def record_first_exact_formal_human_review_decision(
    *,
    repository_root: str | Path,
    request: Mapping[str, Any],
    p3_activation_object: Mapping[str, Any],
    p3_activation_binding_safe_hash: str,
    p3_pre_writer_binding: Mapping[str, Any],
    p3_pre_writer_binding_canonical_sha256: str,
    runner_sha256: str,
    enabled: bool = False,
) -> dict[str, Any]:
    if not enabled:
        return _p3_result(
            "blocked_p3_formal_operation_disabled",
            blockers=["blocked_p3_formal_operation_disabled"],
        )
    if not _p3_activation_is_exact(
        p3_activation_object,
        p3_activation_binding_safe_hash,
        runner_sha256,
    ):
        return _p3_result(
            "blocked_p3_activation_binding_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            blockers=["blocked_p3_activation_binding_mismatch"],
        )
    expected_pre_writer = _p3_expected_pre_writer_binding(
        p3_activation_binding_safe_hash
    )
    if (
        not isinstance(p3_pre_writer_binding, dict)
        or tuple(p3_pre_writer_binding) != P3_PRE_WRITER_BINDING_FIELDS
        or p3_pre_writer_binding != expected_pre_writer
        or any(
            type(p3_pre_writer_binding[field]) is not type(expected)
            for field, expected in expected_pre_writer.items()
        )
        or not isinstance(p3_pre_writer_binding_canonical_sha256, str)
        or not hmac.compare_digest(
            _canonical_sha256(p3_pre_writer_binding),
            p3_pre_writer_binding_canonical_sha256,
        )
    ):
        return _p3_result(
            "blocked_p3_pre_writer_binding_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_pre_writer_binding_mismatch"],
        )
    try:
        validated_request = (
            validate_governed_nonproduction_human_review_decision_request(
                request
            )
        )
    except GovernedNonproductionHumanReviewDecisionValidationError:
        return _p3_result(
            "blocked_p3_exact_request_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_exact_request_mismatch"],
        )
    if validated_request["decision_type"] != "keep_pending_human_review":
        return _p3_result(
            "blocked_p3_exact_request_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_exact_request_mismatch"],
        )
    if dict(SERVER_OWNED_CONTEXT) != _FROZEN_SERVER_OWNED_CONTEXT:
        return _p3_result(
            "blocked_p3_binding_or_snapshot_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_binding_or_snapshot_mismatch"],
        )
    try:
        root, target = _validate_exact_formal_decision_ledger_profile(
            repository_root
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return _p3_result(
            "blocked_p3_formal_target_profile_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_formal_target_profile_mismatch"],
        )
    if not _p3_repository_file_hashes_are_exact(root, p3_activation_object):
        return _p3_result(
            "blocked_p3_frozen_file_hash_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_frozen_file_hash_mismatch"],
        )
    if target.is_symlink() or not target.is_file():
        return _p3_result(
            "blocked_p3_required_formal_state_mismatch",
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            blockers=["blocked_p3_required_formal_state_mismatch"],
        )

    formal_target_access_session_count = 1
    sqlite_connection_open_count = 0
    writer_count = 0
    insert_count = 0
    mutation_count = 0
    row_count_before: int | None = None
    row_count_after: int | None = None
    exact_schema: bool | None = None
    integrity_result = "not_observed"
    decision: dict[str, Any] | None = None
    receipt: dict[str, Any] | None = None
    outcome = "bounded_p3_formal_decision_failure"
    state_before = "not_observed"
    state_after = "not_changed"
    blockers = [outcome]
    try:
        connection = _open_exact_formal_decision_ledger_connection(
            target,
            read_only=False,
        )
        sqlite_connection_open_count = 1
    except sqlite3.Error:
        return _p3_result(
            outcome,
            activation_hash=p3_activation_binding_safe_hash,
            pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
            formal_target_access_session_count=(
                formal_target_access_session_count
            ),
            blockers=blockers,
        )
    try:
        exact_schema = _exact_formal_schema_verified(connection)
        if not exact_schema:
            outcome = "blocked_p3_formal_schema_mismatch"
            blockers = [outcome]
        else:
            row_count_before = _row_count(connection)
            integrity_rows = connection.execute(
                "PRAGMA integrity_check"
            ).fetchall()
            integrity_result = (
                "ok" if integrity_rows == [("ok",)] else "failed"
            )
            if row_count_before != 0:
                outcome = "blocked_p3_required_formal_state_mismatch"
                blockers = [outcome]
            elif integrity_result != "ok":
                outcome = "blocked_p3_formal_integrity_failure"
                blockers = [outcome]
            elif _exact_formal_sidecar_count(target) != 0:
                outcome = "blocked_p3_unexpected_prewrite_sidecar"
                blockers = [outcome]
            else:
                state_before = "initialized_exact_empty"
                identity = _identity_for(validated_request["decision_type"])
                expected_decision_id = f"ghrd-{P3_EXPECTED_IDEMPOTENCY_KEY[:32]}"
                expected_receipt_reference = (
                    f"ghrd-receipt-{P3_EXPECTED_IDEMPOTENCY_KEY[:32]}"
                )
                if (
                    identity["idempotency_key"]
                    != P3_EXPECTED_IDEMPOTENCY_KEY
                    or identity["decision_id"] != expected_decision_id
                    or identity["audit_receipt_reference"]
                    != expected_receipt_reference
                ):
                    outcome = "blocked_p3_binding_or_snapshot_mismatch"
                    blockers = [outcome]
                else:
                    decision = _build_decision(identity, _utc_clock())
                    ledger = GovernedNonproductionHumanReviewDecisionLedger(
                        target,
                        enabled=True,
                    )
                    writer_count = 1
                    insert_count = 1
                    try:
                        ledger._insert_record(connection, decision)
                    except (sqlite3.Error, TypeError, ValueError):
                        connection.rollback()
                        row_count_after = row_count_before
                        outcome = "bounded_p3_formal_writer_failure"
                        blockers = [outcome]
                    else:
                        try:
                            connection.commit()
                        except sqlite3.Error:
                            if connection.in_transaction:
                                row_count_after = row_count_before
                            else:
                                try:
                                    connection.execute(
                                        "PRAGMA query_only = ON"
                                    )
                                    row_count_after = _row_count(connection)
                                    row = _select_by_identity(
                                        connection,
                                        identity,
                                    )
                                    loaded = (
                                        _row_to_decision(row)
                                        if row is not None
                                        else None
                                    )
                                except (
                                    GovernedNonproductionHumanReviewDecisionIntegrityError,
                                    sqlite3.Error,
                                    TypeError,
                                    ValueError,
                                ):
                                    loaded = None
                                if row_count_after == 1 and loaded == decision:
                                    mutation_count = 1
                                else:
                                    row_count_after = row_count_before
                            outcome = "paused_p3_commit_outcome_ambiguous"
                            blockers = [outcome]
                        else:
                            row_count_after = _row_count(connection)
                            row = _select_by_identity(connection, identity)
                            loaded = (
                                _row_to_decision(row)
                                if row is not None
                                else None
                            )
                            exact_schema = _exact_formal_schema_verified(
                                connection
                            )
                            integrity_rows = connection.execute(
                                "PRAGMA integrity_check"
                            ).fetchall()
                            integrity_result = (
                                "ok"
                                if integrity_rows == [("ok",)]
                                else "failed"
                            )
                            if (
                                row_count_after == 1
                                and loaded == decision
                                and exact_schema
                                and integrity_result == "ok"
                            ):
                                mutation_count = 1
                                state_after = "first_exact_decision_recorded"
                                receipt = _receipt(
                                    "created_exactly_one_human_review_decision",
                                    decision=decision,
                                    row_count_before=0,
                                    row_count_after=1,
                                )
                                outcome = (
                                    "created_exactly_one_human_review_decision"
                                )
                                blockers = []
                            else:
                                outcome = (
                                    "blocked_p3_postwrite_verification_failure"
                                )
                                blockers = [outcome]
    except (
        GovernedNonproductionHumanReviewDecisionIntegrityError,
        sqlite3.Error,
        TypeError,
        ValueError,
    ):
        outcome = "bounded_p3_formal_decision_failure"
        blockers = [outcome]
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            outcome = "bounded_p3_formal_decision_failure"
            blockers = [outcome]
    final_sidecar_count = _exact_formal_sidecar_count(target)
    if outcome == "created_exactly_one_human_review_decision" and (
        final_sidecar_count != 0
    ):
        outcome = "blocked_p3_unexpected_final_sidecar"
        blockers = [outcome]
    return _p3_result(
        outcome,
        activation_hash=p3_activation_binding_safe_hash,
        pre_writer_hash=p3_pre_writer_binding_canonical_sha256,
        formal_state_before=state_before,
        formal_state_after=state_after,
        formal_target_access_session_count=formal_target_access_session_count,
        sqlite_connection_open_count=sqlite_connection_open_count,
        formal_writer_invocation_count=writer_count,
        decision_insert_issued_count=insert_count,
        mutation_count=mutation_count,
        decision_row_count_before=row_count_before,
        decision_row_count_after=row_count_after,
        exact_schema_verified=exact_schema,
        integrity_result=integrity_result,
        final_sidecar_count=final_sidecar_count,
        decision=decision if mutation_count == 1 else None,
        receipt=receipt,
        blockers=blockers,
    )


FORMAL_SECOND_ACTIVATION_SCHEMA = (
    "sentigraph_post_classc_p03_formal_second_decision_activation_v0_1"
)
FORMAL_SECOND_ACTIVATION_VERSION = "0.1"
FORMAL_SECOND_ACTIVATION_FIELDS = (
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
FORMAL_SECOND_RESULT_SCHEMA = (
    "sentigraph_post_classc_p03_formal_second_decision_result_v0_1"
)
FORMAL_SECOND_RESULT_VERSION = "0.1"
FORMAL_SECOND_RESULT_FIELDS = (
    "result_schema",
    "result_version",
    "outcome",
    "second_activation_binding_safe_hash",
    "formal_state_before",
    "formal_state_after",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
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
    "decision",
    "receipt",
    "warnings",
    "blockers",
)
FORMAL_SECOND_ACCEPTED_DESIGN_RESULT_SHA256 = (
    "86aeee2bf26949c8b28b6c68361a59137ff88f642b508c118457af2063a65fc1"
)
FORMAL_SECOND_ACCEPTED_DESIGN_ACCEPTANCE_SHA256 = (
    "d37bee0fb798cb3febe8eab80ad779670969a2588d469dfc837220ca821424b0"
)
FORMAL_SECOND_ACCEPTED_FIRST_DECISION_ID = (
    "ghrd-b666c0f03a975c94e6b3b248bd05cdc9"
)
FORMAL_SECOND_ACCEPTED_FIRST_IDEMPOTENCY_KEY = (
    "b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db"
)
FORMAL_SECOND_ACCEPTED_FIRST_AUDIT_RECEIPT_REFERENCE = (
    "ghrd-receipt-b666c0f03a975c94e6b3b248bd05cdc9"
)
FORMAL_SECOND_ACCEPTED_FIRST_DECISION_CANONICAL_SHA256 = (
    "604ded010ca6ea46a6c63d4011445fdcbd775fd498231260e5cd59f88d51452e"
)
FORMAL_SECOND_HISTORICAL_P3_ACTIVATION_BINDING_SAFE_HASH = (
    "d69ebc59eb77637274a1d9743b57d04571c7828eafba2e115c27ff8c82599a0d"
)
_FORMAL_SECOND_FIXED_ACTIVATION_VALUES = {
    "activation_schema": FORMAL_SECOND_ACTIVATION_SCHEMA,
    "activation_version": FORMAL_SECOND_ACTIVATION_VERSION,
    "milestone_id": (
        "sentigraph_post_classc_p03_formal_second_decision_route_binding_v0_1"
    ),
    "route_purpose": "formal_second_human_review_decision_only",
    "repository_identity": "dgmpurf/Sentigraph",
    "required_branch": "main",
    "accepted_p03_design_result_sha256": (
        FORMAL_SECOND_ACCEPTED_DESIGN_RESULT_SHA256
    ),
    "accepted_p03_design_acceptance_sha256": (
        FORMAL_SECOND_ACCEPTED_DESIGN_ACCEPTANCE_SHA256
    ),
    "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
    "target_authorization_contract_safe_hash": (
        FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
    ),
    "accepted_first_decision_type": "keep_pending_human_review",
    "accepted_first_decision_id": FORMAL_SECOND_ACCEPTED_FIRST_DECISION_ID,
    "accepted_first_idempotency_key": (
        FORMAL_SECOND_ACCEPTED_FIRST_IDEMPOTENCY_KEY
    ),
    "accepted_first_audit_receipt_reference": (
        FORMAL_SECOND_ACCEPTED_FIRST_AUDIT_RECEIPT_REFERENCE
    ),
    "accepted_first_decision_canonical_sha256": (
        FORMAL_SECOND_ACCEPTED_FIRST_DECISION_CANONICAL_SHA256
    ),
    "required_prestate_row_count": 1,
    "allowed_mutation_decision_type": "request_more_governance_review",
    "formal_target_access_session_limit": 1,
    "sqlite_connection_open_limit": 1,
    "sqlite_connection_reopen_limit": 0,
    "decision_insert_limit": 1,
    "automatic_retry_allowed": False,
    "automatic_repair_allowed": False,
    "third_decision_allowed": False,
    "nonreusable": True,
}
_FORMAL_SECOND_DYNAMIC_SHA256_FIELDS = (
    "implementation_service_sha256",
    "implementation_route_sha256",
    "implementation_test_sha256",
    "implementation_report_sha256",
    "activation_decision_safe_hash",
    "fresh_runtime_approval_sha256",
)


def _lower_hex_exact(value: Any, length: int) -> bool:
    return (
        isinstance(value, str)
        and len(value) == length
        and all(character in "0123456789abcdef" for character in value)
    )


def validate_second_exact_formal_human_review_decision_activation(
    activation: Mapping[str, Any],
    activation_binding_safe_hash: str,
) -> dict[str, Any]:
    if (
        not isinstance(activation, dict)
        or tuple(activation) != FORMAL_SECOND_ACTIVATION_FIELDS
        or not _lower_hex_exact(activation_binding_safe_hash, 64)
        or not hmac.compare_digest(
            _canonical_sha256(activation),
            activation_binding_safe_hash,
        )
        or hmac.compare_digest(
            activation_binding_safe_hash,
            FORMAL_SECOND_HISTORICAL_P3_ACTIVATION_BINDING_SAFE_HASH,
        )
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    if any(
        field not in activation
        or type(activation[field]) is not type(expected)
        or activation[field] != expected
        for field, expected in _FORMAL_SECOND_FIXED_ACTIVATION_VALUES.items()
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    if not _lower_hex_exact(activation["implementation_commit"], 40):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    if any(
        not _lower_hex_exact(activation[field], 64)
        for field in _FORMAL_SECOND_DYNAMIC_SHA256_FIELDS
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    if (
        not isinstance(activation["fresh_runtime_goal_id"], str)
        or not activation["fresh_runtime_goal_id"].startswith("SENTIGRAPH_")
        or hmac.compare_digest(
            activation["activation_decision_safe_hash"],
            SERVER_OWNED_CONTEXT["activation_decision_safe_hash"],
        )
        or hmac.compare_digest(
            activation["activation_decision_safe_hash"],
            FORMAL_SECOND_HISTORICAL_P3_ACTIVATION_BINDING_SAFE_HASH,
        )
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    return {field: activation[field] for field in FORMAL_SECOND_ACTIVATION_FIELDS}


def _formal_second_server_owned_context(
    activation_decision_safe_hash: str,
    *,
    candidate_context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    context = (
        dict(candidate_context)
        if candidate_context is not None
        else {
            **SERVER_OWNED_CONTEXT,
            "activation_decision_safe_hash": activation_decision_safe_hash,
        }
    )
    if (
        not _lower_hex_exact(activation_decision_safe_hash, 64)
        or hmac.compare_digest(
            activation_decision_safe_hash,
            SERVER_OWNED_CONTEXT["activation_decision_safe_hash"],
        )
        or hmac.compare_digest(
            activation_decision_safe_hash,
            FORMAL_SECOND_HISTORICAL_P3_ACTIVATION_BINDING_SAFE_HASH,
        )
        or tuple(context) != tuple(SERVER_OWNED_CONTEXT)
        or context.get("activation_decision_safe_hash")
        != activation_decision_safe_hash
        or any(
            type(context[field]) is not type(expected)
            or (
                field != "activation_decision_safe_hash"
                and context[field] != expected
            )
            for field, expected in SERVER_OWNED_CONTEXT.items()
        )
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    return {field: context[field] for field in SERVER_OWNED_CONTEXT}


def _accepted_first_formal_decision(
    row: tuple[Any, ...],
) -> dict[str, Any]:
    decision = _row_to_decision(row)
    identity = _identity_for("keep_pending_human_review")
    if (
        not _identity_matches(decision, identity)
        or decision["decision_id"]
        != FORMAL_SECOND_ACCEPTED_FIRST_DECISION_ID
        or decision["idempotency_key"]
        != FORMAL_SECOND_ACCEPTED_FIRST_IDEMPOTENCY_KEY
        or decision["audit_receipt_reference"]
        != FORMAL_SECOND_ACCEPTED_FIRST_AUDIT_RECEIPT_REFERENCE
        or decision["decision_canonical_hash"]
        != FORMAL_SECOND_ACCEPTED_FIRST_DECISION_CANONICAL_SHA256
    ):
        raise GovernedNonproductionHumanReviewDecisionIntegrityError()
    return decision


def _formal_second_result(
    outcome: str,
    *,
    activation_hash: str | None = None,
    formal_state_before: str = "not_observed",
    formal_state_after: str = "not_changed",
    formal_target_access_session_count: int = 0,
    sqlite_connection_open_count: int = 0,
    formal_writer_invocation_count: int = 0,
    decision_insert_issued_count: int = 0,
    mutation_count: int = 0,
    decision_row_count_before: int | None = None,
    decision_row_count_after: int | None = None,
    exact_schema_verified: bool | None = None,
    integrity_result: str = "not_observed",
    final_sidecar_count: int | None = None,
    decision: Mapping[str, Any] | None = None,
    receipt: Mapping[str, Any] | None = None,
    blockers: list[str] | None = None,
) -> dict[str, Any]:
    values = {
        "result_schema": FORMAL_SECOND_RESULT_SCHEMA,
        "result_version": FORMAL_SECOND_RESULT_VERSION,
        "outcome": outcome,
        "second_activation_binding_safe_hash": activation_hash,
        "formal_state_before": formal_state_before,
        "formal_state_after": formal_state_after,
        "target_identity_safe_hash": FORMAL_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            FORMAL_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "formal_target_access_session_count": formal_target_access_session_count,
        "sqlite_connection_open_count": sqlite_connection_open_count,
        "sqlite_connection_reopen_count": 0,
        "formal_writer_invocation_count": formal_writer_invocation_count,
        "decision_insert_issued_count": decision_insert_issued_count,
        "mutation_count": mutation_count,
        "decision_row_count_before": decision_row_count_before,
        "decision_row_count_after": decision_row_count_after,
        "exact_schema_verified": exact_schema_verified,
        "integrity_result": integrity_result,
        "final_sidecar_count": final_sidecar_count,
        "decision": dict(decision) if decision is not None else None,
        "receipt": dict(receipt) if receipt is not None else None,
        "warnings": [],
        "blockers": list(blockers or []),
    }
    return {field: values[field] for field in FORMAL_SECOND_RESULT_FIELDS}


def record_second_exact_formal_human_review_decision(
    *,
    repository_root: str | Path,
    request: Mapping[str, Any],
    second_activation_object: Mapping[str, Any],
    second_activation_binding_safe_hash: str,
    enabled: bool = False,
) -> dict[str, Any]:
    if not enabled:
        return _formal_second_result(
            "blocked_formal_second_operation_disabled",
            blockers=["blocked_formal_second_operation_disabled"],
        )
    try:
        activation = (
            validate_second_exact_formal_human_review_decision_activation(
                second_activation_object,
                second_activation_binding_safe_hash,
            )
        )
        second_context = _formal_second_server_owned_context(
            activation["activation_decision_safe_hash"]
        )
    except GovernedNonproductionHumanReviewDecisionIntegrityError:
        return _formal_second_result(
            "blocked_formal_second_activation_mismatch",
            activation_hash=second_activation_binding_safe_hash,
            blockers=["blocked_formal_second_activation_mismatch"],
        )
    try:
        validated_request = (
            validate_governed_nonproduction_human_review_decision_request(
                request
            )
        )
    except GovernedNonproductionHumanReviewDecisionValidationError as exc:
        decision_type = (
            request.get("decision_type") if isinstance(request, dict) else None
        )
        receipt = _receipt(
            exc.outcome,
            identity={"decision_type": decision_type},
        )
        return _formal_second_result(
            exc.outcome,
            activation_hash=second_activation_binding_safe_hash,
            receipt=receipt,
            blockers=[exc.outcome],
        )
    if dict(SERVER_OWNED_CONTEXT) != _FROZEN_SERVER_OWNED_CONTEXT:
        receipt = _receipt(
            "blocked_binding_or_snapshot_mismatch",
            identity={"decision_type": validated_request["decision_type"]},
        )
        return _formal_second_result(
            "blocked_binding_or_snapshot_mismatch",
            activation_hash=second_activation_binding_safe_hash,
            receipt=receipt,
            blockers=["blocked_binding_or_snapshot_mismatch"],
        )
    try:
        _root, target = _validate_exact_formal_decision_ledger_profile(
            repository_root
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        return _formal_second_result(
            "blocked_formal_second_target_profile_mismatch",
            activation_hash=second_activation_binding_safe_hash,
            blockers=["blocked_formal_second_target_profile_mismatch"],
        )
    if (
        target.is_symlink()
        or not target.is_file()
        or _exact_formal_sidecar_count(target) != 0
    ):
        return _formal_second_result(
            "blocked_formal_second_target_profile_mismatch",
            activation_hash=second_activation_binding_safe_hash,
            blockers=["blocked_formal_second_target_profile_mismatch"],
        )

    access_count = 1
    open_count = 0
    writer_count = 0
    insert_count = 0
    mutation_count = 0
    row_count_before: int | None = None
    row_count_after: int | None = None
    exact_schema: bool | None = None
    integrity_result = "not_observed"
    final_sidecar_count: int | None = None
    formal_state_before = "not_observed"
    formal_state_after = "not_changed"
    decision: dict[str, Any] | None = None
    receipt: dict[str, Any] | None = None
    outcome = "bounded_formal_second_decision_failure"
    blockers = [outcome]
    try:
        connection = _open_exact_formal_decision_ledger_connection(
            target,
            read_only=False,
        )
        open_count = 1
    except sqlite3.Error:
        return _formal_second_result(
            outcome,
            activation_hash=second_activation_binding_safe_hash,
            formal_target_access_session_count=access_count,
            blockers=blockers,
        )
    try:
        connection.execute("BEGIN IMMEDIATE")
        exact_schema = _exact_formal_schema_verified(connection)
        integrity_rows = connection.execute("PRAGMA integrity_check").fetchall()
        integrity_result = "ok" if integrity_rows == [("ok",)] else "failed"
        row_count_before = _row_count(connection)
        if (
            not exact_schema
            or integrity_result != "ok"
            or row_count_before != 1
        ):
            outcome = "blocked_binding_or_snapshot_mismatch"
            blockers = [outcome]
            receipt = _receipt(
                outcome,
                identity={"decision_type": validated_request["decision_type"]},
                row_count_before=row_count_before,
                row_count_after=row_count_before,
            )
            connection.rollback()
            row_count_after = row_count_before
        else:
            first_row = connection.execute(
                f'SELECT * FROM "{FORMAL_PRIMARY_TABLE}" ORDER BY rowid'
            ).fetchone()
            if first_row is None:
                raise GovernedNonproductionHumanReviewDecisionIntegrityError()
            first_decision = _accepted_first_formal_decision(first_row)
            formal_state_before = "first_exact_decision_recorded"
            if validated_request["decision_type"] == (
                "keep_pending_human_review"
            ):
                decision = first_decision
                row_count_after = 1
                receipt = _receipt(
                    "already_exists_same_human_review_decision",
                    decision=decision,
                    row_count_before=1,
                    row_count_after=1,
                )
                outcome = "already_exists_same_human_review_decision"
                blockers = []
                formal_state_after = "first_exact_decision_reused_without_mutation"
                connection.rollback()
            else:
                identity = _identity_for_context(
                    "request_more_governance_review",
                    second_context,
                )
                if (
                    identity["idempotency_key"]
                    == first_decision["idempotency_key"]
                    or _select_by_identity(connection, identity) is not None
                ):
                    raise GovernedNonproductionHumanReviewDecisionIntegrityError()
                decision = _build_decision(identity, _utc_clock())
                ledger = GovernedNonproductionHumanReviewDecisionLedger(
                    target,
                    enabled=True,
                )
                writer_count = 1
                insert_count = 1
                ledger._insert_record(connection, decision)
                try:
                    connection.commit()
                except sqlite3.Error:
                    if connection.in_transaction:
                        try:
                            connection.rollback()
                        except sqlite3.Error:
                            pass
                    try:
                        if not connection.in_transaction:
                            connection.execute("PRAGMA query_only = ON")
                            row_count_after = _row_count(connection)
                    except sqlite3.Error:
                        row_count_after = None
                    outcome = (
                        "paused_pending_read_only_idempotency_verification"
                    )
                    blockers = [outcome]
                    receipt = _receipt(
                        outcome,
                        identity=identity,
                        row_count_before=1,
                        row_count_after=row_count_after,
                    )
                    formal_state_after = "ambiguous_requires_independent_audit"
                else:
                    row_count_after = _row_count(connection)
                    rows = connection.execute(
                        f'SELECT * FROM "{FORMAL_PRIMARY_TABLE}" ORDER BY rowid'
                    ).fetchall()
                    first_after = (
                        _accepted_first_formal_decision(rows[0])
                        if len(rows) >= 1
                        else None
                    )
                    second_after = (
                        _row_to_decision(rows[1]) if len(rows) >= 2 else None
                    )
                    exact_schema = _exact_formal_schema_verified(connection)
                    integrity_rows = connection.execute(
                        "PRAGMA integrity_check"
                    ).fetchall()
                    integrity_result = (
                        "ok" if integrity_rows == [("ok",)] else "failed"
                    )
                    if (
                        row_count_after == 2
                        and first_after == first_decision
                        and second_after == decision
                        and exact_schema
                        and integrity_result == "ok"
                    ):
                        mutation_count = 1
                        receipt = _receipt(
                            "created_exactly_one_human_review_decision",
                            decision=decision,
                            row_count_before=1,
                            row_count_after=2,
                        )
                        outcome = "created_exactly_one_human_review_decision"
                        blockers = []
                        formal_state_after = "second_exact_decision_recorded"
                    else:
                        outcome = "blocked_binding_or_snapshot_mismatch"
                        blockers = [outcome]
                        receipt = _receipt(
                            outcome,
                            identity=identity,
                            row_count_before=1,
                            row_count_after=row_count_after,
                        )
    except (
        GovernedNonproductionHumanReviewDecisionIntegrityError,
        sqlite3.Error,
        TypeError,
        ValueError,
    ):
        try:
            if connection.in_transaction:
                connection.rollback()
        except sqlite3.Error:
            pass
        outcome = "blocked_binding_or_snapshot_mismatch"
        blockers = [outcome]
        receipt = _receipt(
            outcome,
            identity={"decision_type": validated_request["decision_type"]},
            row_count_before=row_count_before,
            row_count_after=row_count_before,
        )
        row_count_after = row_count_before
        decision = None
        writer_count = 0 if insert_count == 0 else writer_count
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            outcome = "bounded_formal_second_decision_failure"
            blockers = [outcome]
    final_sidecar_count = _exact_formal_sidecar_count(target)
    if outcome in (
        "already_exists_same_human_review_decision",
        "created_exactly_one_human_review_decision",
    ) and final_sidecar_count != 0:
        outcome = "bounded_formal_second_decision_failure"
        blockers = [outcome]
        receipt = _receipt(
            "bounded_decision_ledger_failure",
            identity={"decision_type": validated_request["decision_type"]},
            row_count_before=row_count_before,
            row_count_after=row_count_after,
        )
    return _formal_second_result(
        outcome,
        activation_hash=second_activation_binding_safe_hash,
        formal_state_before=formal_state_before,
        formal_state_after=formal_state_after,
        formal_target_access_session_count=access_count,
        sqlite_connection_open_count=open_count,
        formal_writer_invocation_count=writer_count,
        decision_insert_issued_count=insert_count,
        mutation_count=mutation_count,
        decision_row_count_before=row_count_before,
        decision_row_count_after=row_count_after,
        exact_schema_verified=exact_schema,
        integrity_result=integrity_result,
        final_sidecar_count=final_sidecar_count,
        decision=decision if not blockers else None,
        receipt=receipt,
        blockers=blockers,
    )
