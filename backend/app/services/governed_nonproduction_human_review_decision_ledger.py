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
