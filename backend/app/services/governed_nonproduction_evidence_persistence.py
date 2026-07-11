from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any


PAYLOAD_SCHEMA = "sentigraph_exact_locked_candidate_safe_write_payload_v0_1"
PAYLOAD_VERSION = "0.1"
SOURCE_CANDIDATE_SET_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)
SOURCE_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1"
)
IDENTITY_SCHEMA = "sentigraph_one_real_source_locked_candidate_identity_v0_1"
COMMAND_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_command_v0_1"
PERSISTED_RECORD_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_record_v0_1"
RECEIPT_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_1"
REVOCATION_EVENT_SCHEMA = (
    "sentigraph_governed_nonproduction_evidence_persistence_revocation_event_v0_1"
)
INITIAL_STATUS = "governed_nonproduction_pending_human_review"
MUTATION_MODE = "transactional_create_only"
LOGICAL_RUNTIME_TARGET_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3"
)
TABLE_NAME = "governed_nonproduction_evidence_records_v0_1"
ACTIVATION_DECISION_SCOPE = "exact_locked_candidate_and_selected_nonproduction_target_only"
MAXIMUM_MUTATING_ATTEMPTS = 1

_IDENTITY_FIELDS = {
    "approved_package_name",
    "approved_package_role",
    "approved_case_id_hint",
    "approved_row_source",
    "selected_preview_row_opaque_id",
    "selected_preview_row_safe_hash",
    "final_candidate_id",
    "final_candidate_safe_hash",
    "final_candidate_schema",
    "identity_schema",
    "identity_version",
    "hash_algorithm",
    "hash_input_scope",
    "candidate_lock_status",
}

_PAYLOAD_FIELDS = {
    "payload_schema",
    "payload_version",
    "source_candidate_set_schema",
    "source_candidate_schema",
    "source_schema_versions",
    "immutable_candidate_identity",
    "candidate_projection",
    "lineage_projection",
    "boundary_projection",
    "input_safe_hash",
}

_SOURCE_SCHEMA_VERSION_FIELDS = {
    "candidate_set_schema",
    "candidate_schema",
    "identity_schema",
    "payload_schema",
}

_REQUIRED_CANDIDATE_FIELDS = {
    "evidence_layer_write_candidate_schema",
    "evidence_layer_write_candidate_id",
    "source_production_evidence_import_candidate_id",
    "source_evidence_layer_write_candidate_id",
    "source_evidence_layer_import_candidate_id",
    "source_review_queue_candidate_id",
    "source_evidence_candidate_id",
    "evidence_id_hash",
    "text_snippet_redacted",
}

_OPTIONAL_CANDIDATE_FIELDS = {
    "preview_hash",
    "case_id_hint",
    "platform",
    "evidence_type",
    "created_at_date",
    "source_url_present",
    "acquisition_mode",
    "provenance_type",
    "verification_status",
    "review_status",
    "trust_label",
    "redaction_status",
    "title_or_label_redacted",
    "redaction_warnings",
    "warning_labels",
    "blocker_codes",
}

_LINEAGE_FIELDS = {
    "source_production_evidence_import_candidate_id",
    "source_evidence_layer_write_candidate_id",
    "source_evidence_layer_import_candidate_id",
    "source_review_queue_candidate_id",
    "source_evidence_candidate_id",
    "source_candidate_set_schema",
    "source_candidate_schema",
}

_BOUNDARY_FIELDS = {
    "human_review_required",
    "no_automatic_trust_upgrade",
    "preview_only",
    "import_candidate_only",
    "production_import_candidate_only",
    "write_candidate_only",
    "evidence_layer_write_candidate_only",
    "not_production_evidence_item",
    "no_evidence_layer_write",
    "warning_count",
    "warning_labels",
}

_GATE_BINDING_FIELDS = {
    "gate_contract_schema",
    "gate_contract_version",
    "gate_contract_safe_hash",
}

_ACTIVATION_BINDING_FIELDS = {
    "activation_decision_id",
    "activation_decision_schema",
    "activation_decision_version",
    "activation_decision_safe_hash",
    "candidate_identity_digest",
    "gate_contract_safe_hash",
    "decision_scope",
}

_COMMAND_FIELDS = {
    "command_schema",
    "command_version",
    "target_logical_label",
    "mutation_attempt_number",
    "candidate_identity_digest",
    "idempotency_key",
    "persisted_record_id",
    "record",
}

_RECORD_FIELDS = {
    "persisted_record_id",
    "persisted_record_schema",
    "candidate_id",
    "candidate_safe_hash",
    "candidate_identity_digest",
    "preview_row_id",
    "preview_row_safe_hash",
    "package_name",
    "candidate_role",
    "case_id_hint",
    "row_source",
    "identity_schema",
    "identity_version",
    "input_schema",
    "input_schema_version",
    "input_safe_hash",
    "safe_payload_projection",
    "source_schema_versions",
    "lineage_projection",
    "gate_contract_schema",
    "gate_contract_version",
    "gate_contract_safe_hash",
    "activation_decision_id",
    "activation_decision_safe_hash",
    "idempotency_key",
    "mutation_mode",
    "status",
    "human_review_required",
    "automatic_trust_upgrade_allowed",
    "created_at",
    "revoked_at",
    "revocation_reason",
    "audit_receipt_reference",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "package_or_row_read_during_persistence",
    "trust_or_role_reclassified",
    "record_canonical_hash",
}

_JSON_RECORD_FIELDS = {
    "safe_payload_projection",
    "source_schema_versions",
    "lineage_projection",
}

_BOOLEAN_RECORD_FIELDS = {
    "human_review_required",
    "automatic_trust_upgrade_allowed",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "package_or_row_read_during_persistence",
    "trust_or_role_reclassified",
}

_FORBIDDEN_KEYS = {
    "raw_row",
    "raw_rows",
    "raw_row_text",
    "raw_comment",
    "raw_comments",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_name",
    "account_id",
    "account_name",
    "profile_url",
    "profile_data",
    "private_message",
    "private_messages",
    "source_url",
    "url",
    "absolute_path",
    "package_path",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "token",
    "tokens",
    "password",
    "passwords",
    "api_key",
    "api_keys",
    "credential",
    "credentials",
    "environment_value",
    "env_value",
    "secret",
    "secrets",
    "unrelated_rows",
    "target_user_list",
    "persuasion_score",
    "psychological_profile",
    "personality_diagnosis",
    "official_verified",
    "truth_score",
    "prediction_probability",
    "real_person_pii",
}

_OPAQUE_TOKEN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,159}$")
_HASH_RE = re.compile(r"^[a-f0-9]{64}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_LOGICAL_LABEL_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{2,239}$")
_URL_RE = re.compile(r"(?:https?://|www\.)", re.IGNORECASE)
_WINDOWS_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")
_TRAVERSAL_RE = re.compile(r"(?:^|[\\/])\.\.(?:[\\/]|$)")
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
_SECRET_RE = re.compile(
    r"(?:sk-[A-Za-z0-9_-]{8,}|xox[baprs]-|-----BEGIN .*PRIVATE KEY-----|AKIA[0-9A-Z]{16})",
    re.IGNORECASE,
)

_COLUMN_ORDER = [
    "persisted_record_id",
    "persisted_record_schema",
    "candidate_id",
    "candidate_safe_hash",
    "candidate_identity_digest",
    "preview_row_id",
    "preview_row_safe_hash",
    "package_name",
    "candidate_role",
    "case_id_hint",
    "row_source",
    "identity_schema",
    "identity_version",
    "input_schema",
    "input_schema_version",
    "input_safe_hash",
    "safe_payload_projection",
    "source_schema_versions",
    "lineage_projection",
    "gate_contract_schema",
    "gate_contract_version",
    "gate_contract_safe_hash",
    "activation_decision_id",
    "activation_decision_safe_hash",
    "idempotency_key",
    "mutation_mode",
    "status",
    "human_review_required",
    "automatic_trust_upgrade_allowed",
    "created_at",
    "revoked_at",
    "revocation_reason",
    "audit_receipt_reference",
    "production_evidenceitem_created",
    "production_case_changed",
    "downstream_runtime_called",
    "package_or_row_read_during_persistence",
    "trust_or_role_reclassified",
    "record_canonical_hash",
]


class GovernedNonproductionPersistenceError(ValueError):
    """Bounded validation or store error without unsafe value echoing."""


class _AmbiguousCommitError(RuntimeError):
    pass


class GovernedNonproductionEvidencePersistenceStore:
    """Disabled-by-default isolated SQLite store for synthetic contract validation."""

    def __init__(
        self,
        database_path: str | Path | None,
        *,
        target_logical_label: str,
        allowed_candidate_identity_digest: str,
        enabled: bool = False,
    ) -> None:
        self.database_path = Path(database_path) if database_path is not None else None
        self.target_logical_label = target_logical_label
        self.allowed_candidate_identity_digest = allowed_candidate_identity_digest
        self.enabled = enabled

    def initialize(self) -> None:
        self._require_enabled_configuration()
        assert self.database_path is not None
        if not self.database_path.parent.is_dir():
            raise GovernedNonproductionPersistenceError("database_parent_missing")
        connection = sqlite3.connect(str(self.database_path))
        try:
            connection.execute(_CREATE_TABLE_SQL)
            connection.commit()
        finally:
            connection.close()

    def safe_snapshot(self) -> dict[str, Any]:
        self._require_enabled_configuration()
        connection = self._open_read_only()
        try:
            return _snapshot_connection(connection)
        finally:
            connection.close()

    def _require_enabled_configuration(self) -> None:
        if not self.enabled:
            raise GovernedNonproductionPersistenceError("store_disabled")
        if self.database_path is None:
            raise GovernedNonproductionPersistenceError("physical_database_path_required")
        _validate_logical_target_label(self.target_logical_label)
        if not _is_hash(self.allowed_candidate_identity_digest):
            raise GovernedNonproductionPersistenceError("allowed_candidate_identity_digest_invalid")

    def _require_initialized(self) -> None:
        self._require_enabled_configuration()
        assert self.database_path is not None
        if not self.database_path.is_file():
            raise GovernedNonproductionPersistenceError("store_not_initialized")

    def _open_mutating(self) -> sqlite3.Connection:
        self._require_initialized()
        assert self.database_path is not None
        connection = sqlite3.connect(str(self.database_path))
        connection.row_factory = sqlite3.Row
        return connection

    def _open_read_only(self) -> sqlite3.Connection:
        self._require_initialized()
        assert self.database_path is not None
        uri = f"{self.database_path.resolve().as_uri()}?mode=ro"
        connection = sqlite3.connect(uri, uri=True)
        connection.row_factory = sqlite3.Row
        return connection


def validate_exact_locked_candidate_safe_write_payload(
    payload: dict[str, Any],
    *,
    expected_identity: dict[str, Any],
) -> dict[str, Any]:
    """Validate and copy one strict safe payload without performing IO."""

    if not isinstance(payload, dict) or set(payload) != _PAYLOAD_FIELDS:
        raise GovernedNonproductionPersistenceError("payload_top_level_fields_invalid")
    if payload.get("payload_schema") != PAYLOAD_SCHEMA:
        raise GovernedNonproductionPersistenceError("payload_schema_invalid")
    if payload.get("payload_version") != PAYLOAD_VERSION:
        raise GovernedNonproductionPersistenceError("payload_version_invalid")
    if payload.get("source_candidate_set_schema") != SOURCE_CANDIDATE_SET_SCHEMA:
        raise GovernedNonproductionPersistenceError("source_candidate_set_schema_invalid")
    if payload.get("source_candidate_schema") != SOURCE_CANDIDATE_SCHEMA:
        raise GovernedNonproductionPersistenceError("source_candidate_schema_invalid")

    _validate_source_schema_versions(payload.get("source_schema_versions"))
    validated_expected = _validate_identity(expected_identity)
    validated_identity = _validate_identity(payload.get("immutable_candidate_identity"))
    if validated_identity != validated_expected:
        raise GovernedNonproductionPersistenceError("identity_mismatch")

    candidate = _validate_candidate_projection(payload.get("candidate_projection"))
    lineage = _validate_lineage_projection(payload.get("lineage_projection"), candidate)
    boundary = _validate_boundary_projection(payload.get("boundary_projection"))

    claimed_hash = payload.get("input_safe_hash")
    if not _is_hash(claimed_hash):
        raise GovernedNonproductionPersistenceError("input_safe_hash_invalid")
    hash_projection = {key: value for key, value in payload.items() if key != "input_safe_hash"}
    if _sha256(hash_projection) != claimed_hash:
        raise GovernedNonproductionPersistenceError("input_safe_hash_mismatch")

    validated = deepcopy(payload)
    validated["immutable_candidate_identity"] = validated_identity
    validated["candidate_projection"] = candidate
    validated["lineage_projection"] = lineage
    validated["boundary_projection"] = boundary
    return validated


def build_governed_nonproduction_evidence_persistence_command(
    payload: dict[str, Any],
    *,
    expected_identity: dict[str, Any],
    gate_contract_binding: dict[str, Any],
    activation_decision_binding: dict[str, Any],
    target_logical_label: str,
    mutation_attempt_number: int,
    created_at: str,
) -> dict[str, Any]:
    """Build one deterministic create-only command without performing IO."""

    validated = validate_exact_locked_candidate_safe_write_payload(
        payload,
        expected_identity=expected_identity,
    )
    identity = validated["immutable_candidate_identity"]
    candidate_identity_digest = _sha256(identity)
    gate = _validate_gate_binding(gate_contract_binding)
    activation = _validate_activation_binding(
        activation_decision_binding,
        candidate_identity_digest=candidate_identity_digest,
        gate_contract_safe_hash=gate["gate_contract_safe_hash"],
    )
    _validate_logical_target_label(target_logical_label)
    if mutation_attempt_number != MAXIMUM_MUTATING_ATTEMPTS:
        raise GovernedNonproductionPersistenceError("mutation_attempt_invalid")
    _validate_timestamp(created_at)

    idempotency_projection = {
        "candidate_identity_digest": candidate_identity_digest,
        "input_safe_hash": validated["input_safe_hash"],
        "persisted_record_schema": PERSISTED_RECORD_SCHEMA,
        "persisted_record_schema_version": "0.1",
        "gate_contract_schema": gate["gate_contract_schema"],
        "gate_contract_version": gate["gate_contract_version"],
        "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
        "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
        "mutation_mode": MUTATION_MODE,
        "target_logical_label": target_logical_label,
    }
    idempotency_key = _sha256(idempotency_projection)
    persisted_record_id = f"gnpepr-{idempotency_key[:32]}"
    receipt_reference = f"gnpepr-receipt-{idempotency_key[:32]}"

    safe_projection = deepcopy(validated)
    projected_candidate = safe_projection["candidate_projection"]
    if "created_at_date" in projected_candidate:
        projected_candidate["coarse_created_at"] = projected_candidate.pop("created_at_date")

    record: dict[str, Any] = {
        "persisted_record_id": persisted_record_id,
        "persisted_record_schema": PERSISTED_RECORD_SCHEMA,
        "candidate_id": identity["final_candidate_id"],
        "candidate_safe_hash": identity["final_candidate_safe_hash"],
        "candidate_identity_digest": candidate_identity_digest,
        "preview_row_id": identity["selected_preview_row_opaque_id"],
        "preview_row_safe_hash": identity["selected_preview_row_safe_hash"],
        "package_name": identity["approved_package_name"],
        "candidate_role": identity["approved_package_role"],
        "case_id_hint": identity["approved_case_id_hint"],
        "row_source": identity["approved_row_source"],
        "identity_schema": identity["identity_schema"],
        "identity_version": identity["identity_version"],
        "input_schema": PAYLOAD_SCHEMA,
        "input_schema_version": PAYLOAD_VERSION,
        "input_safe_hash": validated["input_safe_hash"],
        "safe_payload_projection": safe_projection,
        "source_schema_versions": deepcopy(validated["source_schema_versions"]),
        "lineage_projection": deepcopy(validated["lineage_projection"]),
        "gate_contract_schema": gate["gate_contract_schema"],
        "gate_contract_version": gate["gate_contract_version"],
        "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
        "activation_decision_id": activation["activation_decision_id"],
        "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
        "idempotency_key": idempotency_key,
        "mutation_mode": MUTATION_MODE,
        "status": INITIAL_STATUS,
        "human_review_required": True,
        "automatic_trust_upgrade_allowed": False,
        "created_at": created_at,
        "revoked_at": None,
        "revocation_reason": None,
        "audit_receipt_reference": receipt_reference,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "package_or_row_read_during_persistence": False,
        "trust_or_role_reclassified": False,
    }
    record["record_canonical_hash"] = _record_canonical_hash(record)

    return {
        "command_schema": COMMAND_SCHEMA,
        "command_version": "0.1",
        "target_logical_label": target_logical_label,
        "mutation_attempt_number": mutation_attempt_number,
        "candidate_identity_digest": candidate_identity_digest,
        "idempotency_key": idempotency_key,
        "persisted_record_id": persisted_record_id,
        "record": record,
    }


def create_governed_nonproduction_evidence_record(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
) -> dict[str, Any]:
    """Create at most one isolated record and return an in-memory safe receipt."""

    validated_command = _validate_command(command)
    if validated_command["target_logical_label"] != store.target_logical_label:
        raise GovernedNonproductionPersistenceError("target_logical_label_mismatch")
    if validated_command["candidate_identity_digest"] != store.allowed_candidate_identity_digest:
        return _build_receipt(
            validated_command,
            transaction_started=False,
            transaction_committed=False,
            mutation_count=0,
            final_outcome="scope_violation",
        )

    store._require_enabled_configuration()
    connection = store._open_mutating()
    transaction_started = False
    before_state: dict[str, Any] | None = None
    try:
        connection.execute("BEGIN IMMEDIATE")
        transaction_started = True
        before_state = _snapshot_connection(connection)

        existing_by_idempotency = _find_row_by_idempotency(connection, validated_command["idempotency_key"])
        if existing_by_idempotency is not None:
            connection.rollback()
            existing_record = _row_to_record(existing_by_idempotency)
            same_record = existing_record == validated_command["record"]
            if not same_record:
                return _build_receipt(
                    validated_command,
                    transaction_started=True,
                    transaction_committed=False,
                    mutation_count=0,
                    duplicate_conflict=True,
                    final_outcome="blocked_identity_or_payload_conflict",
                )
            verification = verify_governed_nonproduction_evidence_record(
                store,
                validated_command,
                before_state=before_state,
                expected_mutation_count=0,
            )
            return _build_receipt(
                validated_command,
                transaction_started=True,
                transaction_committed=False,
                mutation_count=0,
                already_exists=True,
                final_outcome="already_exists_same_record",
                verification=verification,
            )

        existing_candidate = _find_row_by_candidate_digest(
            connection,
            validated_command["candidate_identity_digest"],
        )
        if existing_candidate is not None:
            connection.rollback()
            return _build_receipt(
                validated_command,
                transaction_started=True,
                transaction_committed=False,
                mutation_count=0,
                duplicate_conflict=True,
                final_outcome="blocked_identity_or_payload_conflict",
            )

        try:
            _insert_record(connection, validated_command["record"])
        except Exception:
            connection.rollback()
            return _build_receipt(
                validated_command,
                transaction_started=True,
                transaction_committed=False,
                mutation_count=0,
                final_outcome="rolled_back_before_commit",
            )

        try:
            _commit_connection(connection)
        except Exception:
            connection.close()
            verification = _verify_after_ambiguous_commit(
                store,
                validated_command,
                before_state=before_state,
            )
            if verification["post_write_readback_verified"]:
                return _build_receipt(
                    validated_command,
                    transaction_started=True,
                    transaction_committed=True,
                    mutation_count=1,
                    final_outcome="created_exactly_one_governed_nonproduction_record",
                    verification=verification,
                )
            return _build_receipt(
                validated_command,
                transaction_started=True,
                transaction_committed=False,
                mutation_count=None,
                final_outcome="paused_ambiguous_commit_not_proven",
                verification=verification,
            )
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass

    assert before_state is not None
    verification = verify_governed_nonproduction_evidence_record(
        store,
        validated_command,
        before_state=before_state,
        expected_mutation_count=1,
    )
    outcome = (
        "created_exactly_one_governed_nonproduction_record"
        if verification["post_write_readback_verified"]
        else "paused_post_write_verification_failed"
    )
    return _build_receipt(
        validated_command,
        transaction_started=transaction_started,
        transaction_committed=True,
        mutation_count=1,
        final_outcome=outcome,
        verification=verification,
    )


def find_governed_nonproduction_record_by_idempotency_key(
    store: GovernedNonproductionEvidencePersistenceStore,
    idempotency_key: str,
) -> dict[str, Any] | None:
    """Read one record by idempotency key without creating or mutating storage."""

    if not _is_hash(idempotency_key):
        raise GovernedNonproductionPersistenceError("idempotency_key_invalid")
    connection = store._open_read_only()
    try:
        row = _find_row_by_idempotency(connection, idempotency_key)
        return _row_to_record(row) if row is not None else None
    finally:
        connection.close()


def verify_governed_nonproduction_evidence_record(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
    *,
    before_state: dict[str, Any] | None,
    expected_mutation_count: int,
) -> dict[str, Any]:
    """Read back the intended record and prove exact isolation using safe digests."""

    validated_command = _validate_command(command)
    if expected_mutation_count not in {0, 1}:
        raise GovernedNonproductionPersistenceError("expected_mutation_count_invalid")
    connection = store._open_read_only()
    try:
        row = _find_row_by_idempotency(connection, validated_command["idempotency_key"])
        record = _row_to_record(row) if row is not None else None
        matching_count = int(
            connection.execute(
                f"SELECT COUNT(*) FROM {TABLE_NAME} "
                "WHERE persisted_record_id = ? AND candidate_identity_digest = ?",
                (
                    validated_command["persisted_record_id"],
                    validated_command["candidate_identity_digest"],
                ),
            ).fetchone()[0]
        )
        after_state = _snapshot_connection(connection)
    finally:
        connection.close()

    persisted_record_verified = record == validated_command["record"]
    exactly_one_record_verified = matching_count == 1
    unrelated_change = _unrelated_change_detected(
        before_state,
        after_state,
        validated_command["record"],
        expected_mutation_count=expected_mutation_count,
    )
    post_write_verified = (
        persisted_record_verified and exactly_one_record_verified and not unrelated_change
    )
    return {
        "persisted_record_verified": persisted_record_verified,
        "exactly_one_record_verified": exactly_one_record_verified,
        "unrelated_record_change_detected": unrelated_change,
        "post_write_readback_verified": post_write_verified,
        "before_count": before_state.get("count") if isinstance(before_state, dict) else None,
        "after_count": after_state["count"],
        "before_digest": before_state.get("digest") if isinstance(before_state, dict) else None,
        "after_digest": after_state["digest"],
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
    }


def _validate_source_schema_versions(value: Any) -> None:
    expected = {
        "candidate_set_schema": SOURCE_CANDIDATE_SET_SCHEMA,
        "candidate_schema": SOURCE_CANDIDATE_SCHEMA,
        "identity_schema": IDENTITY_SCHEMA,
        "payload_schema": PAYLOAD_SCHEMA,
    }
    if not isinstance(value, dict) or set(value) != _SOURCE_SCHEMA_VERSION_FIELDS or value != expected:
        raise GovernedNonproductionPersistenceError("source_schema_versions_invalid")


def _validate_identity(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _IDENTITY_FIELDS:
        raise GovernedNonproductionPersistenceError("identity_fields_invalid")
    for field, field_value in value.items():
        if not isinstance(field_value, str) or not field_value:
            raise GovernedNonproductionPersistenceError("identity_value_invalid")
        if field.endswith("_hash"):
            if not _is_hash(field_value):
                raise GovernedNonproductionPersistenceError("identity_hash_invalid")
        elif not _is_opaque_token(field_value):
            raise GovernedNonproductionPersistenceError("identity_value_invalid")
    required_values = {
        "final_candidate_schema": SOURCE_CANDIDATE_SET_SCHEMA,
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": "0.1",
        "hash_algorithm": "sha256",
        "hash_input_scope": "versioned_safe_canonical_projection_only",
        "candidate_lock_status": "locked_for_single_candidate_governance_review_only",
    }
    if any(value.get(key) != expected for key, expected in required_values.items()):
        raise GovernedNonproductionPersistenceError("identity_contract_invalid")
    return deepcopy(value)


def _validate_candidate_projection(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GovernedNonproductionPersistenceError("candidate_projection_invalid")
    fields = set(value)
    if not _REQUIRED_CANDIDATE_FIELDS.issubset(fields) or not fields.issubset(
        _REQUIRED_CANDIDATE_FIELDS | _OPTIONAL_CANDIDATE_FIELDS
    ):
        raise GovernedNonproductionPersistenceError("candidate_projection_fields_invalid")
    if value.get("evidence_layer_write_candidate_schema") != SOURCE_CANDIDATE_SCHEMA:
        raise GovernedNonproductionPersistenceError("candidate_projection_schema_invalid")

    token_fields = {
        "evidence_layer_write_candidate_schema",
        "evidence_layer_write_candidate_id",
        "source_production_evidence_import_candidate_id",
        "source_evidence_layer_write_candidate_id",
        "source_evidence_layer_import_candidate_id",
        "source_review_queue_candidate_id",
        "source_evidence_candidate_id",
        "case_id_hint",
        "platform",
        "evidence_type",
        "acquisition_mode",
        "provenance_type",
        "verification_status",
        "review_status",
        "trust_label",
        "redaction_status",
    }
    for field in token_fields & fields:
        if not _is_opaque_token(value.get(field)):
            raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    for field in {"evidence_id_hash", "preview_hash"} & fields:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("candidate_projection_hash_invalid")
    for field in {"text_snippet_redacted", "title_or_label_redacted"} & fields:
        _validate_redacted_snippet(value.get(field))
    if "created_at_date" in fields:
        _validate_date(value.get("created_at_date"))
    if "source_url_present" in fields and not isinstance(value.get("source_url_present"), bool):
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    for field in {"redaction_warnings", "warning_labels", "blocker_codes"} & fields:
        _validate_safe_label_list(value.get(field))
    _reject_sensitive(value, "candidate_projection_value_unsafe")
    return deepcopy(value)


def _validate_lineage_projection(value: Any, candidate: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _LINEAGE_FIELDS:
        raise GovernedNonproductionPersistenceError("lineage_projection_fields_invalid")
    for field, field_value in value.items():
        if not _is_opaque_token(field_value):
            raise GovernedNonproductionPersistenceError("lineage_projection_value_unsafe")
    if value.get("source_candidate_set_schema") != SOURCE_CANDIDATE_SET_SCHEMA:
        raise GovernedNonproductionPersistenceError("lineage_projection_mismatch")
    if value.get("source_candidate_schema") != SOURCE_CANDIDATE_SCHEMA:
        raise GovernedNonproductionPersistenceError("lineage_projection_mismatch")
    for field in _LINEAGE_FIELDS - {"source_candidate_set_schema", "source_candidate_schema"}:
        if value.get(field) != candidate.get(field):
            raise GovernedNonproductionPersistenceError("lineage_projection_mismatch")
    _reject_sensitive(value, "lineage_projection_value_unsafe")
    return deepcopy(value)


def _validate_boundary_projection(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _BOUNDARY_FIELDS:
        raise GovernedNonproductionPersistenceError("boundary_projection_invalid")
    required_true = _BOUNDARY_FIELDS - {"warning_count", "warning_labels"}
    if any(value.get(field) is not True for field in required_true):
        raise GovernedNonproductionPersistenceError("boundary_projection_invalid")
    if value.get("warning_count") != 1:
        raise GovernedNonproductionPersistenceError("boundary_projection_invalid")
    labels = value.get("warning_labels")
    _validate_safe_label_list(labels)
    if "manual_review_required" not in labels:
        raise GovernedNonproductionPersistenceError("boundary_projection_invalid")
    return deepcopy(value)


def _validate_gate_binding(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _GATE_BINDING_FIELDS:
        raise GovernedNonproductionPersistenceError("gate_contract_binding_invalid")
    if not _is_opaque_token(value.get("gate_contract_schema")):
        raise GovernedNonproductionPersistenceError("gate_contract_binding_invalid")
    if value.get("gate_contract_version") != "0.1":
        raise GovernedNonproductionPersistenceError("gate_contract_binding_invalid")
    if not _is_hash(value.get("gate_contract_safe_hash")):
        raise GovernedNonproductionPersistenceError("gate_contract_binding_invalid")
    return deepcopy(value)


def _validate_activation_binding(
    value: Any,
    *,
    candidate_identity_digest: str,
    gate_contract_safe_hash: str,
) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _ACTIVATION_BINDING_FIELDS:
        raise GovernedNonproductionPersistenceError("activation_decision_binding_invalid")
    for field in {
        "activation_decision_id",
        "activation_decision_schema",
        "activation_decision_version",
        "decision_scope",
    }:
        if not _is_opaque_token(value.get(field)):
            raise GovernedNonproductionPersistenceError("activation_decision_binding_invalid")
    for field in {"activation_decision_safe_hash", "candidate_identity_digest", "gate_contract_safe_hash"}:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("activation_decision_binding_invalid")
    if value.get("candidate_identity_digest") != candidate_identity_digest:
        raise GovernedNonproductionPersistenceError("activation_candidate_binding_mismatch")
    if value.get("gate_contract_safe_hash") != gate_contract_safe_hash:
        raise GovernedNonproductionPersistenceError("activation_gate_binding_mismatch")
    if value.get("decision_scope") != ACTIVATION_DECISION_SCOPE:
        raise GovernedNonproductionPersistenceError("activation_decision_scope_invalid")
    return deepcopy(value)


def _validate_command(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _COMMAND_FIELDS:
        raise GovernedNonproductionPersistenceError("persistence_command_invalid")
    if value.get("command_schema") != COMMAND_SCHEMA or value.get("command_version") != "0.1":
        raise GovernedNonproductionPersistenceError("persistence_command_schema_invalid")
    _validate_logical_target_label(value.get("target_logical_label"))
    if value.get("mutation_attempt_number") != MAXIMUM_MUTATING_ATTEMPTS:
        raise GovernedNonproductionPersistenceError("mutation_attempt_invalid")
    for field in {"candidate_identity_digest", "idempotency_key"}:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("persistence_command_hash_invalid")
    if not _is_opaque_token(value.get("persisted_record_id")):
        raise GovernedNonproductionPersistenceError("persisted_record_id_invalid")
    record = _validate_record(value.get("record"))
    if record["candidate_identity_digest"] != value["candidate_identity_digest"]:
        raise GovernedNonproductionPersistenceError("command_record_identity_mismatch")
    if record["idempotency_key"] != value["idempotency_key"]:
        raise GovernedNonproductionPersistenceError("command_record_idempotency_mismatch")
    if record["persisted_record_id"] != value["persisted_record_id"]:
        raise GovernedNonproductionPersistenceError("command_record_id_mismatch")
    validated = deepcopy(value)
    validated["record"] = record
    return validated


def _validate_record(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _RECORD_FIELDS:
        raise GovernedNonproductionPersistenceError("persisted_record_fields_invalid")
    required_values = {
        "persisted_record_schema": PERSISTED_RECORD_SCHEMA,
        "input_schema": PAYLOAD_SCHEMA,
        "input_schema_version": PAYLOAD_VERSION,
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": "0.1",
        "mutation_mode": MUTATION_MODE,
        "status": INITIAL_STATUS,
        "human_review_required": True,
        "automatic_trust_upgrade_allowed": False,
        "revoked_at": None,
        "revocation_reason": None,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "package_or_row_read_during_persistence": False,
        "trust_or_role_reclassified": False,
    }
    if any(value.get(key) != expected for key, expected in required_values.items()):
        raise GovernedNonproductionPersistenceError("persisted_record_contract_invalid")
    for field in {
        "candidate_safe_hash",
        "candidate_identity_digest",
        "preview_row_safe_hash",
        "input_safe_hash",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
        "idempotency_key",
        "record_canonical_hash",
    }:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("persisted_record_hash_invalid")
    for field in {
        "persisted_record_id",
        "candidate_id",
        "preview_row_id",
        "package_name",
        "candidate_role",
        "case_id_hint",
        "row_source",
        "gate_contract_schema",
        "gate_contract_version",
        "activation_decision_id",
        "audit_receipt_reference",
    }:
        if not _is_opaque_token(value.get(field)):
            raise GovernedNonproductionPersistenceError("persisted_record_value_invalid")
    _validate_timestamp(value.get("created_at"))
    for field in _JSON_RECORD_FIELDS:
        if not isinstance(value.get(field), dict):
            raise GovernedNonproductionPersistenceError("persisted_record_json_invalid")
    if _record_canonical_hash(value) != value.get("record_canonical_hash"):
        raise GovernedNonproductionPersistenceError("persisted_record_canonical_hash_mismatch")
    return deepcopy(value)


def _validate_logical_target_label(value: Any) -> None:
    if not isinstance(value, str) or not value:
        raise GovernedNonproductionPersistenceError("target_logical_label_required")
    if (
        not _LOGICAL_LABEL_RE.fullmatch(value)
        or value.startswith("/")
        or "\\" in value
        or ":" in value
        or _TRAVERSAL_RE.search(value)
    ):
        raise GovernedNonproductionPersistenceError("target_logical_label_invalid")


def _validate_redacted_snippet(value: Any) -> None:
    if not isinstance(value, str) or not value or len(value) > 160:
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    if "redacted" not in value.lower():
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    if _string_is_sensitive(value):
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")


def _validate_safe_label_list(value: Any) -> None:
    if not isinstance(value, list) or len(value) > 20:
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    for item in value:
        if not isinstance(item, str) or len(item) > 80 or not _is_opaque_token(item):
            raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")


def _validate_date(value: Any) -> None:
    if not isinstance(value, str) or not _DATE_RE.fullmatch(value):
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise GovernedNonproductionPersistenceError("candidate_projection_value_unsafe") from exc


def _validate_timestamp(value: Any) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise GovernedNonproductionPersistenceError("created_at_invalid")
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise GovernedNonproductionPersistenceError("created_at_invalid") from exc


def _reject_sensitive(value: Any, code: str) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if str(key).lower() in _FORBIDDEN_KEYS:
                raise GovernedNonproductionPersistenceError(code)
            _reject_sensitive(nested, code)
    elif isinstance(value, list):
        for item in value:
            _reject_sensitive(item, code)
    elif isinstance(value, str) and _string_is_sensitive(value):
        raise GovernedNonproductionPersistenceError(code)


def _string_is_sensitive(value: str) -> bool:
    return bool(
        _URL_RE.search(value)
        or _WINDOWS_PATH_RE.search(value)
        or _TRAVERSAL_RE.search(value)
        or value.startswith("/")
        or _EMAIL_RE.search(value)
        or _PHONE_RE.search(value)
        or _SECRET_RE.search(value)
        or ".env" in value.lower()
    )


def _is_opaque_token(value: Any) -> bool:
    return isinstance(value, str) and bool(_OPAQUE_TOKEN_RE.fullmatch(value)) and not _string_is_sensitive(value)


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_HASH_RE.fullmatch(value))


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _record_canonical_hash(record: dict[str, Any]) -> str:
    return _sha256({key: value for key, value in record.items() if key != "record_canonical_hash"})


def _insert_record(connection: sqlite3.Connection, record: dict[str, Any]) -> None:
    values = []
    for field in _COLUMN_ORDER:
        value = record[field]
        if field in _JSON_RECORD_FIELDS:
            value = _canonical_json(value)
        elif field in _BOOLEAN_RECORD_FIELDS:
            value = 1 if value else 0
        values.append(value)
    columns = ", ".join(_COLUMN_ORDER)
    parameter_markers = ", ".join("?" for _ in _COLUMN_ORDER)
    connection.execute(
        f"INSERT INTO {TABLE_NAME} ({columns}) VALUES ({parameter_markers})",
        values,
    )


def _commit_connection(connection: sqlite3.Connection) -> None:
    connection.commit()


def _find_row_by_idempotency(
    connection: sqlite3.Connection,
    idempotency_key: str,
) -> sqlite3.Row | None:
    return connection.execute(
        f"SELECT * FROM {TABLE_NAME} WHERE idempotency_key = ?",
        (idempotency_key,),
    ).fetchone()


def _find_row_by_candidate_digest(
    connection: sqlite3.Connection,
    candidate_identity_digest: str,
) -> sqlite3.Row | None:
    return connection.execute(
        f"SELECT * FROM {TABLE_NAME} WHERE candidate_identity_digest = ?",
        (candidate_identity_digest,),
    ).fetchone()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    record = dict(row)
    for field in _JSON_RECORD_FIELDS:
        record[field] = json.loads(record[field])
    for field in _BOOLEAN_RECORD_FIELDS:
        record[field] = bool(record[field])
    return record


def _snapshot_connection(connection: sqlite3.Connection) -> dict[str, Any]:
    rows = connection.execute(
        f"SELECT persisted_record_id, record_canonical_hash FROM {TABLE_NAME} "
        "ORDER BY persisted_record_id"
    ).fetchall()
    records = {str(row[0]): str(row[1]) for row in rows}
    return {
        "count": len(records),
        "digest": _sha256(records),
        "records": records,
    }


def _unrelated_change_detected(
    before_state: dict[str, Any] | None,
    after_state: dict[str, Any],
    intended_record: dict[str, Any],
    *,
    expected_mutation_count: int,
) -> bool:
    if not isinstance(before_state, dict) or not isinstance(before_state.get("records"), dict):
        return True
    expected_records = dict(before_state["records"])
    if expected_mutation_count == 1:
        if intended_record["persisted_record_id"] in expected_records:
            return True
        expected_records[intended_record["persisted_record_id"]] = intended_record["record_canonical_hash"]
    return expected_records != after_state.get("records")


def _verify_after_ambiguous_commit(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
    *,
    before_state: dict[str, Any] | None,
) -> dict[str, Any]:
    try:
        return verify_governed_nonproduction_evidence_record(
            store,
            command,
            before_state=before_state,
            expected_mutation_count=1,
        )
    except (GovernedNonproductionPersistenceError, sqlite3.Error):
        return {
            "persisted_record_verified": False,
            "exactly_one_record_verified": False,
            "unrelated_record_change_detected": False,
            "post_write_readback_verified": False,
            "production_evidenceitem_created": False,
            "production_case_changed": False,
            "downstream_runtime_called": False,
        }


def _build_receipt(
    command: dict[str, Any],
    *,
    transaction_started: bool,
    transaction_committed: bool,
    mutation_count: int | None,
    final_outcome: str,
    already_exists: bool = False,
    duplicate_conflict: bool = False,
    verification: dict[str, Any] | None = None,
) -> dict[str, Any]:
    proof = verification or {}
    record = command["record"]
    return {
        "receipt_id": record["audit_receipt_reference"],
        "receipt_schema": RECEIPT_SCHEMA,
        "persisted_record_id": command["persisted_record_id"],
        "idempotency_key": command["idempotency_key"],
        "candidate_identity_digest": command["candidate_identity_digest"],
        "activation_decision_safe_hash": record["activation_decision_safe_hash"],
        "target_logical_label": command["target_logical_label"],
        "mutation_mode": MUTATION_MODE,
        "mutation_attempt_limit": MAXIMUM_MUTATING_ATTEMPTS,
        "mutation_attempt_number": command["mutation_attempt_number"],
        "transaction_started": transaction_started,
        "transaction_committed": transaction_committed,
        "mutation_count": mutation_count,
        "already_exists": already_exists,
        "duplicate_conflict": duplicate_conflict,
        "persisted_record_verified": proof.get("persisted_record_verified", False),
        "exactly_one_record_verified": proof.get("exactly_one_record_verified", False),
        "unrelated_record_change_detected": proof.get("unrelated_record_change_detected", False),
        "post_write_readback_verified": proof.get("post_write_readback_verified", False),
        "rollback_or_revocation_available": True,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "final_outcome": final_outcome,
        "created_at": record["created_at"],
    }


_CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    persisted_record_id TEXT PRIMARY KEY,
    persisted_record_schema TEXT NOT NULL CHECK (
        persisted_record_schema = '{PERSISTED_RECORD_SCHEMA}'
    ),
    candidate_id TEXT NOT NULL,
    candidate_safe_hash TEXT NOT NULL,
    candidate_identity_digest TEXT NOT NULL UNIQUE,
    preview_row_id TEXT NOT NULL,
    preview_row_safe_hash TEXT NOT NULL,
    package_name TEXT NOT NULL,
    candidate_role TEXT NOT NULL,
    case_id_hint TEXT NOT NULL,
    row_source TEXT NOT NULL,
    identity_schema TEXT NOT NULL CHECK (identity_schema = '{IDENTITY_SCHEMA}'),
    identity_version TEXT NOT NULL CHECK (identity_version = '0.1'),
    input_schema TEXT NOT NULL CHECK (input_schema = '{PAYLOAD_SCHEMA}'),
    input_schema_version TEXT NOT NULL CHECK (input_schema_version = '{PAYLOAD_VERSION}'),
    input_safe_hash TEXT NOT NULL,
    safe_payload_projection TEXT NOT NULL,
    source_schema_versions TEXT NOT NULL,
    lineage_projection TEXT NOT NULL,
    gate_contract_schema TEXT NOT NULL,
    gate_contract_version TEXT NOT NULL,
    gate_contract_safe_hash TEXT NOT NULL,
    activation_decision_id TEXT NOT NULL,
    activation_decision_safe_hash TEXT NOT NULL,
    idempotency_key TEXT NOT NULL UNIQUE,
    mutation_mode TEXT NOT NULL CHECK (mutation_mode = '{MUTATION_MODE}'),
    status TEXT NOT NULL CHECK (status = '{INITIAL_STATUS}'),
    human_review_required INTEGER NOT NULL CHECK (human_review_required = 1),
    automatic_trust_upgrade_allowed INTEGER NOT NULL CHECK (automatic_trust_upgrade_allowed = 0),
    created_at TEXT NOT NULL,
    revoked_at TEXT NULL CHECK (revoked_at IS NULL),
    revocation_reason TEXT NULL CHECK (revocation_reason IS NULL),
    audit_receipt_reference TEXT NOT NULL,
    production_evidenceitem_created INTEGER NOT NULL CHECK (production_evidenceitem_created = 0),
    production_case_changed INTEGER NOT NULL CHECK (production_case_changed = 0),
    downstream_runtime_called INTEGER NOT NULL CHECK (downstream_runtime_called = 0),
    package_or_row_read_during_persistence INTEGER NOT NULL CHECK (
        package_or_row_read_during_persistence = 0
    ),
    trust_or_role_reclassified INTEGER NOT NULL CHECK (trust_or_role_reclassified = 0),
    record_canonical_hash TEXT NOT NULL
)
"""
