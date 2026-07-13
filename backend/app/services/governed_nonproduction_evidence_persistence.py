from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from copy import deepcopy
from datetime import datetime, timezone
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
COMMAND_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_command_v0_2"
COMMAND_VERSION = "0.2"
PERSISTED_RECORD_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_record_v0_1"
ATTEMPT_RESERVATION_SCHEMA = (
    "sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1"
)
ATTEMPT_RESERVATION_VERSION = "0.1"
RECEIPT_SCHEMA = "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
REVOCATION_EVENT_SCHEMA = (
    "sentigraph_governed_nonproduction_evidence_persistence_revocation_event_v0_1"
)
INITIAL_STATUS = "governed_nonproduction_pending_human_review"
MUTATION_MODE = "transactional_create_only"
LOGICAL_RUNTIME_TARGET_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3"
)
TABLE_NAME = "governed_nonproduction_evidence_records_v0_1"
ATTEMPT_RESERVATION_TABLE = (
    "governed_nonproduction_evidence_persistence_attempt_reservations_v0_1"
)
ACTIVATION_DECISION_SCOPE = "exact_locked_candidate_and_selected_nonproduction_target_only"
MAXIMUM_MUTATING_ATTEMPTS = 1
ATTEMPT_SCOPE_NAMESPACE = "sentigraph_governed_nonproduction_attempt_scope_v0_1"
ATTEMPT_RESERVATION_ID_NAMESPACE = (
    "sentigraph_governed_nonproduction_attempt_reservation_id_v0_1"
)

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
    "mutation_mode",
    "mutation_attempt_number",
    "input_schema",
    "input_schema_version",
    "input_safe_hash",
    "immutable_candidate_identity",
    "gate_contract_binding",
    "activation_decision_binding",
    "candidate_identity_digest",
    "idempotency_key",
    "persisted_record_id",
    "audit_receipt_reference",
    "attempt_scope_key",
    "attempt_reservation_id",
    "record",
    "reservation",
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

_ATTEMPT_RESERVATION_FIELDS = {
    "attempt_reservation_id",
    "attempt_reservation_schema",
    "attempt_reservation_version",
    "attempt_scope_key",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_schema",
    "gate_contract_version",
    "gate_contract_safe_hash",
    "activation_decision_id",
    "activation_decision_safe_hash",
    "target_logical_label",
    "mutation_mode",
    "idempotency_key",
    "expected_persisted_record_id",
    "maximum_mutating_attempts",
    "reserved_attempt_number",
    "reserved_at",
    "reservation_canonical_hash",
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

_ATTEMPT_RESERVATION_COLUMN_ORDER = [
    "attempt_reservation_id",
    "attempt_reservation_schema",
    "attempt_reservation_version",
    "attempt_scope_key",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_schema",
    "gate_contract_version",
    "gate_contract_safe_hash",
    "activation_decision_id",
    "activation_decision_safe_hash",
    "target_logical_label",
    "mutation_mode",
    "idempotency_key",
    "expected_persisted_record_id",
    "maximum_mutating_attempts",
    "reserved_attempt_number",
    "reserved_at",
    "reservation_canonical_hash",
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
            connection.execute(_CREATE_ATTEMPT_RESERVATION_TABLE_SQL)
            connection.execute(_CREATE_TABLE_SQL)
            connection.commit()
        finally:
            connection.close()

    def safe_snapshot(self) -> dict[str, Any]:
        self._require_enabled_configuration()
        connection = self._open_read_only()
        try:
            return _snapshot_record_connection(connection)
        finally:
            connection.close()

    def safe_attempt_snapshot(self) -> dict[str, Any]:
        """Return a safe digest snapshot reconstructed from reservation columns."""

        self._require_enabled_configuration()
        connection = self._open_read_only()
        try:
            return _snapshot_attempt_connection(connection)
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
    """Build one deterministic v0.2 inspection command without performing IO."""

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
        "namespace": "sentigraph_governed_nonproduction_idempotency_v0_2",
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
        "command_schema": COMMAND_SCHEMA,
        "command_version": COMMAND_VERSION,
    }
    idempotency_key = _sha256(idempotency_projection)
    persisted_record_id = f"gnpepr-{idempotency_key[:32]}"
    receipt_reference = f"gnpepr-receipt-{idempotency_key[:32]}"
    attempt_scope_key = _sha256(
        {
            "namespace": ATTEMPT_SCOPE_NAMESPACE,
            "candidate_identity_digest": candidate_identity_digest,
            "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
            "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
            "target_logical_label": target_logical_label,
            "mutation_mode": MUTATION_MODE,
            "command_schema": COMMAND_SCHEMA,
            "command_version": COMMAND_VERSION,
        }
    )
    attempt_reservation_id = "gnpepr-attempt-" + _sha256(
        {
            "namespace": ATTEMPT_RESERVATION_ID_NAMESPACE,
            "attempt_scope_key": attempt_scope_key,
        }
    )[:32]

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

    reservation: dict[str, Any] = {
        "attempt_reservation_id": attempt_reservation_id,
        "attempt_reservation_schema": ATTEMPT_RESERVATION_SCHEMA,
        "attempt_reservation_version": ATTEMPT_RESERVATION_VERSION,
        "attempt_scope_key": attempt_scope_key,
        "candidate_identity_digest": candidate_identity_digest,
        "input_safe_hash": validated["input_safe_hash"],
        "gate_contract_schema": gate["gate_contract_schema"],
        "gate_contract_version": gate["gate_contract_version"],
        "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
        "activation_decision_id": activation["activation_decision_id"],
        "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
        "target_logical_label": target_logical_label,
        "mutation_mode": MUTATION_MODE,
        "idempotency_key": idempotency_key,
        "expected_persisted_record_id": persisted_record_id,
        "maximum_mutating_attempts": MAXIMUM_MUTATING_ATTEMPTS,
        "reserved_attempt_number": mutation_attempt_number,
        "reserved_at": created_at,
    }
    reservation["reservation_canonical_hash"] = _reservation_canonical_hash(reservation)

    return {
        "command_schema": COMMAND_SCHEMA,
        "command_version": COMMAND_VERSION,
        "target_logical_label": target_logical_label,
        "mutation_mode": MUTATION_MODE,
        "mutation_attempt_number": mutation_attempt_number,
        "input_schema": PAYLOAD_SCHEMA,
        "input_schema_version": PAYLOAD_VERSION,
        "input_safe_hash": validated["input_safe_hash"],
        "immutable_candidate_identity": deepcopy(identity),
        "gate_contract_binding": gate,
        "activation_decision_binding": activation,
        "candidate_identity_digest": candidate_identity_digest,
        "idempotency_key": idempotency_key,
        "persisted_record_id": persisted_record_id,
        "audit_receipt_reference": receipt_reference,
        "attempt_scope_key": attempt_scope_key,
        "attempt_reservation_id": attempt_reservation_id,
        "record": record,
        "reservation": reservation,
    }


def create_governed_nonproduction_evidence_record(
    store: GovernedNonproductionEvidencePersistenceStore,
    *,
    payload: dict[str, Any],
    expected_identity: dict[str, Any],
    gate_contract_binding: dict[str, Any],
    activation_decision_binding: dict[str, Any],
    target_logical_label: str,
    mutation_attempt_number: int,
) -> dict[str, Any]:
    """Revalidate source inputs and run one isolated synthetic persistence attempt."""

    command = build_governed_nonproduction_evidence_persistence_command(
        payload,
        expected_identity=expected_identity,
        gate_contract_binding=gate_contract_binding,
        activation_decision_binding=activation_decision_binding,
        target_logical_label=target_logical_label,
        mutation_attempt_number=mutation_attempt_number,
        created_at=_utc_now(),
    )
    return _persist_rederived_governed_nonproduction_command(store, command)


def _persist_rederived_governed_nonproduction_command(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
) -> dict[str, Any]:
    validated_command = _validate_command(command)
    if validated_command["target_logical_label"] != store.target_logical_label:
        raise GovernedNonproductionPersistenceError("target_logical_label_mismatch")
    if validated_command["candidate_identity_digest"] != store.allowed_candidate_identity_digest:
        return _build_receipt(
            validated_command,
            final_outcome="scope_violation",
        )

    store._require_enabled_configuration()
    existing = _resolve_existing_state_receipt(store, validated_command)
    if existing is not None:
        return existing

    reservation_phase = _reserve_mutating_attempt(store, validated_command)
    if reservation_phase.get("receipt") is not None:
        return reservation_phase["receipt"]

    _after_attempt_reservation_commit(validated_command)
    return _create_base_record_after_reservation(
        store,
        validated_command,
        attempt_state_after_reservation=reservation_phase["attempt_state_after"],
    )


def _resolve_existing_state_receipt(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
) -> dict[str, Any] | None:
    connection = store._open_read_only()
    try:
        _snapshot_record_connection(connection)
        _snapshot_attempt_connection(connection)
        existing_by_idempotency = _find_row_by_idempotency(connection, command["idempotency_key"])
        if existing_by_idempotency is not None:
            existing_record = _row_to_record(existing_by_idempotency)
            if not _records_have_same_stable_binding(existing_record, command["record"]):
                return _build_receipt(
                    command,
                    final_outcome="blocked_identity_or_payload_conflict",
                    duplicate_conflict=True,
                )
            reservation_row = _find_attempt_row_by_scope(connection, command["attempt_scope_key"])
            if reservation_row is None:
                return _build_receipt(
                    command,
                    final_outcome="paused_post_write_verification_failed",
                    exact_record_verified=True,
                    created_at=existing_record["created_at"],
                )
            reservation = _row_to_reservation(reservation_row)
            reservation_verified = _reservations_have_same_stable_binding(
                reservation,
                command["reservation"],
            )
            if not reservation_verified:
                raise GovernedNonproductionPersistenceError(
                    "stored_attempt_reservation_binding_conflict"
                )
            return _build_receipt(
                command,
                already_exists=True,
                final_outcome="already_exists_same_record",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                exact_record_verified=True,
                attempt_reservation_verified=True,
                no_unrelated_attempt_change_verified=True,
                no_unrelated_record_change_verified=True,
                created_at=existing_record["created_at"],
            )

        existing_candidate = _find_row_by_candidate_digest(
            connection,
            command["candidate_identity_digest"],
        )
        if existing_candidate is not None:
            return _build_receipt(
                command,
                duplicate_conflict=True,
                final_outcome="blocked_identity_or_payload_conflict",
            )

        reservation_row = _find_attempt_row_by_scope(connection, command["attempt_scope_key"])
        if reservation_row is None:
            reservation_row = _find_attempt_row_by_id(
                connection,
                command["attempt_reservation_id"],
            )
        if reservation_row is not None:
            reservation = _row_to_reservation(reservation_row)
            if not _reservations_have_same_stable_binding(
                reservation,
                command["reservation"],
            ):
                raise GovernedNonproductionPersistenceError(
                    "stored_attempt_reservation_binding_conflict"
                )
            return _build_receipt(
                command,
                final_outcome=(
                    "paused_mutating_attempt_already_consumed_without_verified_record"
                ),
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                attempt_reservation_verified=True,
                no_unrelated_attempt_change_verified=True,
            )
        return None
    finally:
        connection.close()


def _reserve_mutating_attempt(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
) -> dict[str, Any]:
    connection = store._open_mutating()
    attempt_before: dict[str, Any] | None = None
    try:
        connection.execute("BEGIN IMMEDIATE")
        attempt_before = _snapshot_attempt_connection(connection)
        _snapshot_record_connection(connection)
        if (
            _find_attempt_row_by_scope(connection, command["attempt_scope_key"]) is not None
            or _find_attempt_row_by_id(connection, command["attempt_reservation_id"]) is not None
            or _find_row_by_idempotency(connection, command["idempotency_key"]) is not None
            or _find_row_by_candidate_digest(
                connection,
                command["candidate_identity_digest"],
            )
            is not None
        ):
            connection.rollback()
            return {"receipt": _resolve_existing_state_receipt(store, command)}
        try:
            _insert_attempt_reservation(connection, command["reservation"])
        except sqlite3.IntegrityError:
            connection.rollback()
            return {"receipt": _resolve_existing_state_receipt(store, command)}
        except Exception:
            connection.rollback()
            return {
                "receipt": _build_receipt(
                    command,
                    final_outcome="reservation_rolled_back_before_commit",
                )
            }
        try:
            _commit_attempt_reservation_connection(connection)
        except Exception:
            connection.close()
            verification = _verify_attempt_reservation_after_commit(
                store,
                command,
                before_state=attempt_before,
                expected_mutation_count=1,
            )
            if verification["attempt_reservation_verified"]:
                return {
                    "receipt": _build_receipt(
                        command,
                        final_outcome=(
                            "paused_attempt_reservation_commit_ambiguous_attempt_consumed"
                        ),
                        attempt_reservation_committed=True,
                        mutating_attempt_consumed=True,
                        attempt_reservation_verified=True,
                        no_unrelated_attempt_change_verified=verification[
                            "no_unrelated_attempt_change_verified"
                        ],
                    )
                }
            return {
                "receipt": _build_receipt(
                    command,
                    final_outcome="paused_attempt_reservation_commit_ambiguous_not_proven",
                )
            }
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass

    assert attempt_before is not None
    verification = _verify_attempt_reservation_after_commit(
        store,
        command,
        before_state=attempt_before,
        expected_mutation_count=1,
    )
    if not (
        verification["attempt_reservation_verified"]
        and verification["no_unrelated_attempt_change_verified"]
    ):
        return {
            "receipt": _build_receipt(
                command,
                final_outcome="paused_post_write_verification_failed",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                attempt_reservation_verified=verification["attempt_reservation_verified"],
                no_unrelated_attempt_change_verified=verification[
                    "no_unrelated_attempt_change_verified"
                ],
            )
        }
    return {
        "receipt": None,
        "attempt_state_after": verification["after_state"],
    }


def _create_base_record_after_reservation(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
    *,
    attempt_state_after_reservation: dict[str, Any],
) -> dict[str, Any]:
    connection = store._open_mutating()
    record_before: dict[str, Any] | None = None
    attempt_before: dict[str, Any] | None = None
    insert_issued = False
    try:
        connection.execute("BEGIN IMMEDIATE")
        record_before = _snapshot_record_connection(connection)
        attempt_before = _snapshot_attempt_connection(connection)
        if attempt_before.get("records") != attempt_state_after_reservation.get("records"):
            connection.rollback()
            return _build_receipt(
                command,
                final_outcome="paused_post_write_verification_failed",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                attempt_reservation_verified=True,
            )
        reservation_row = _find_attempt_row_by_scope(connection, command["attempt_scope_key"])
        if reservation_row is None or not _reservations_have_same_stable_binding(
            _row_to_reservation(reservation_row),
            command["reservation"],
        ):
            connection.rollback()
            return _build_receipt(
                command,
                final_outcome="paused_post_write_verification_failed",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
            )
        if (
            _find_row_by_idempotency(connection, command["idempotency_key"]) is not None
            or _find_row_by_candidate_digest(
                connection,
                command["candidate_identity_digest"],
            )
            is not None
        ):
            connection.rollback()
            resolved = _resolve_existing_state_receipt(store, command)
            assert resolved is not None
            return resolved
        try:
            insert_issued = True
            _insert_record(connection, command["record"])
        except Exception:
            connection.rollback()
            return _build_receipt(
                command,
                final_outcome="rolled_back_before_commit",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                base_record_insert_issued=insert_issued,
                base_record_transaction_started=True,
                transaction_rollback_performed=True,
                attempt_reservation_verified=True,
                no_unrelated_attempt_change_verified=True,
            )
        try:
            _commit_record_connection(connection)
        except Exception:
            connection.close()
            verification = _verify_full_persistence_state(
                store,
                command,
                attempt_before=attempt_before,
                record_before=record_before,
                expected_record_mutation_count=1,
            )
            if verification["post_write_readback_verified"]:
                return _build_receipt(
                    command,
                    final_outcome="created_exactly_one_governed_nonproduction_record",
                    attempt_reservation_committed=True,
                    mutating_attempt_consumed=True,
                    base_record_insert_issued=True,
                    base_record_transaction_started=True,
                    base_record_transaction_committed=True,
                    mutation_count=1,
                    verification=verification,
                )
            return _build_receipt(
                command,
                final_outcome="paused_ambiguous_commit_not_proven",
                attempt_reservation_committed=True,
                mutating_attempt_consumed=True,
                base_record_insert_issued=True,
                base_record_transaction_started=True,
                mutation_count=None,
                verification=verification,
            )
    finally:
        try:
            connection.close()
        except sqlite3.Error:
            pass

    assert record_before is not None and attempt_before is not None
    verification = _verify_full_persistence_state(
        store,
        command,
        attempt_before=attempt_before,
        record_before=record_before,
        expected_record_mutation_count=1,
    )
    verified = verification["post_write_readback_verified"]
    return _build_receipt(
        command,
        final_outcome=(
            "created_exactly_one_governed_nonproduction_record"
            if verified
            else "paused_post_write_verification_failed"
        ),
        attempt_reservation_committed=True,
        mutating_attempt_consumed=True,
        base_record_insert_issued=True,
        base_record_transaction_started=True,
        base_record_transaction_committed=True,
        mutation_count=1,
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
    """Read back one intended record and recompute integrity from actual columns."""

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
        after_state = _snapshot_record_connection(connection)
    finally:
        connection.close()

    persisted_record_verified = bool(
        record is not None
        and _records_have_same_stable_binding(record, validated_command["record"])
    )
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
    if value.get("command_schema") != COMMAND_SCHEMA or value.get("command_version") != COMMAND_VERSION:
        raise GovernedNonproductionPersistenceError("persistence_command_schema_invalid")
    if value.get("mutation_mode") != MUTATION_MODE:
        raise GovernedNonproductionPersistenceError("persistence_command_mutation_mode_invalid")
    if value.get("input_schema") != PAYLOAD_SCHEMA or value.get("input_schema_version") != PAYLOAD_VERSION:
        raise GovernedNonproductionPersistenceError("persistence_command_input_schema_invalid")
    _validate_logical_target_label(value.get("target_logical_label"))
    if value.get("mutation_attempt_number") != MAXIMUM_MUTATING_ATTEMPTS:
        raise GovernedNonproductionPersistenceError("mutation_attempt_invalid")
    identity = _validate_identity(value.get("immutable_candidate_identity"))
    candidate_identity_digest = _sha256(identity)
    if value.get("candidate_identity_digest") != candidate_identity_digest:
        raise GovernedNonproductionPersistenceError("persistence_command_identity_digest_mismatch")
    gate = _validate_gate_binding(value.get("gate_contract_binding"))
    activation = _validate_activation_binding(
        value.get("activation_decision_binding"),
        candidate_identity_digest=candidate_identity_digest,
        gate_contract_safe_hash=gate["gate_contract_safe_hash"],
    )
    for field in {
        "input_safe_hash",
        "candidate_identity_digest",
        "idempotency_key",
        "attempt_scope_key",
    }:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("persistence_command_hash_invalid")
    for field in {
        "persisted_record_id",
        "audit_receipt_reference",
        "attempt_reservation_id",
    }:
        if not _is_opaque_token(value.get(field)):
            raise GovernedNonproductionPersistenceError("persistence_command_id_invalid")

    expected_idempotency_key = _sha256(
        {
            "namespace": "sentigraph_governed_nonproduction_idempotency_v0_2",
            "candidate_identity_digest": candidate_identity_digest,
            "input_safe_hash": value["input_safe_hash"],
            "persisted_record_schema": PERSISTED_RECORD_SCHEMA,
            "persisted_record_schema_version": "0.1",
            "gate_contract_schema": gate["gate_contract_schema"],
            "gate_contract_version": gate["gate_contract_version"],
            "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
            "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
            "mutation_mode": MUTATION_MODE,
            "target_logical_label": value["target_logical_label"],
            "command_schema": COMMAND_SCHEMA,
            "command_version": COMMAND_VERSION,
        }
    )
    if value["idempotency_key"] != expected_idempotency_key:
        raise GovernedNonproductionPersistenceError("persistence_command_idempotency_mismatch")
    expected_record_id = f"gnpepr-{expected_idempotency_key[:32]}"
    expected_receipt_reference = f"gnpepr-receipt-{expected_idempotency_key[:32]}"
    if value["persisted_record_id"] != expected_record_id:
        raise GovernedNonproductionPersistenceError("persisted_record_id_invalid")
    if value["audit_receipt_reference"] != expected_receipt_reference:
        raise GovernedNonproductionPersistenceError("audit_receipt_reference_invalid")

    expected_attempt_scope_key = _sha256(
        {
            "namespace": ATTEMPT_SCOPE_NAMESPACE,
            "candidate_identity_digest": candidate_identity_digest,
            "activation_decision_safe_hash": activation["activation_decision_safe_hash"],
            "gate_contract_safe_hash": gate["gate_contract_safe_hash"],
            "target_logical_label": value["target_logical_label"],
            "mutation_mode": MUTATION_MODE,
            "command_schema": COMMAND_SCHEMA,
            "command_version": COMMAND_VERSION,
        }
    )
    if value["attempt_scope_key"] != expected_attempt_scope_key:
        raise GovernedNonproductionPersistenceError("attempt_scope_key_mismatch")
    expected_reservation_id = "gnpepr-attempt-" + _sha256(
        {
            "namespace": ATTEMPT_RESERVATION_ID_NAMESPACE,
            "attempt_scope_key": expected_attempt_scope_key,
        }
    )[:32]
    if value["attempt_reservation_id"] != expected_reservation_id:
        raise GovernedNonproductionPersistenceError("attempt_reservation_id_mismatch")

    record = _validate_record(value.get("record"))
    reservation = _validate_reservation(value.get("reservation"))
    if record["candidate_identity_digest"] != value["candidate_identity_digest"]:
        raise GovernedNonproductionPersistenceError("command_record_identity_mismatch")
    if record["idempotency_key"] != value["idempotency_key"]:
        raise GovernedNonproductionPersistenceError("command_record_idempotency_mismatch")
    if record["persisted_record_id"] != value["persisted_record_id"]:
        raise GovernedNonproductionPersistenceError("command_record_id_mismatch")
    if record["audit_receipt_reference"] != value["audit_receipt_reference"]:
        raise GovernedNonproductionPersistenceError("command_record_receipt_mismatch")
    if record["input_safe_hash"] != value["input_safe_hash"]:
        raise GovernedNonproductionPersistenceError("command_record_input_hash_mismatch")
    if record["gate_contract_safe_hash"] != gate["gate_contract_safe_hash"]:
        raise GovernedNonproductionPersistenceError("command_record_gate_mismatch")
    if record["activation_decision_safe_hash"] != activation["activation_decision_safe_hash"]:
        raise GovernedNonproductionPersistenceError("command_record_activation_mismatch")
    expected_record_identity = {
        "candidate_id": identity["final_candidate_id"],
        "candidate_safe_hash": identity["final_candidate_safe_hash"],
        "preview_row_id": identity["selected_preview_row_opaque_id"],
        "preview_row_safe_hash": identity["selected_preview_row_safe_hash"],
        "package_name": identity["approved_package_name"],
        "candidate_role": identity["approved_package_role"],
        "case_id_hint": identity["approved_case_id_hint"],
        "row_source": identity["approved_row_source"],
    }
    if any(record.get(field) != expected for field, expected in expected_record_identity.items()):
        raise GovernedNonproductionPersistenceError("command_record_identity_projection_mismatch")
    if reservation["attempt_reservation_id"] != value["attempt_reservation_id"]:
        raise GovernedNonproductionPersistenceError("command_reservation_id_mismatch")
    if reservation["attempt_scope_key"] != value["attempt_scope_key"]:
        raise GovernedNonproductionPersistenceError("command_reservation_scope_mismatch")
    if reservation["candidate_identity_digest"] != value["candidate_identity_digest"]:
        raise GovernedNonproductionPersistenceError("command_reservation_identity_mismatch")
    if reservation["idempotency_key"] != value["idempotency_key"]:
        raise GovernedNonproductionPersistenceError("command_reservation_idempotency_mismatch")
    if reservation["expected_persisted_record_id"] != value["persisted_record_id"]:
        raise GovernedNonproductionPersistenceError("command_reservation_record_mismatch")
    if reservation["input_safe_hash"] != value["input_safe_hash"]:
        raise GovernedNonproductionPersistenceError("command_reservation_input_hash_mismatch")
    if record["created_at"] != reservation["reserved_at"]:
        raise GovernedNonproductionPersistenceError("command_timestamp_binding_mismatch")
    validated = deepcopy(value)
    validated["immutable_candidate_identity"] = identity
    validated["gate_contract_binding"] = gate
    validated["activation_decision_binding"] = activation
    validated["record"] = record
    validated["reservation"] = reservation
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


def _validate_reservation(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _ATTEMPT_RESERVATION_FIELDS:
        raise GovernedNonproductionPersistenceError("attempt_reservation_fields_invalid")
    required_values = {
        "attempt_reservation_schema": ATTEMPT_RESERVATION_SCHEMA,
        "attempt_reservation_version": ATTEMPT_RESERVATION_VERSION,
        "mutation_mode": MUTATION_MODE,
        "maximum_mutating_attempts": MAXIMUM_MUTATING_ATTEMPTS,
        "reserved_attempt_number": MAXIMUM_MUTATING_ATTEMPTS,
    }
    if any(value.get(key) != expected for key, expected in required_values.items()):
        raise GovernedNonproductionPersistenceError("attempt_reservation_contract_invalid")
    for field in {
        "attempt_scope_key",
        "candidate_identity_digest",
        "input_safe_hash",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
        "idempotency_key",
        "reservation_canonical_hash",
    }:
        if not _is_hash(value.get(field)):
            raise GovernedNonproductionPersistenceError("attempt_reservation_hash_invalid")
    for field in {
        "attempt_reservation_id",
        "gate_contract_schema",
        "gate_contract_version",
        "activation_decision_id",
        "expected_persisted_record_id",
    }:
        if not _is_opaque_token(value.get(field)):
            raise GovernedNonproductionPersistenceError("attempt_reservation_value_invalid")
    _validate_logical_target_label(value.get("target_logical_label"))
    _validate_timestamp(value.get("reserved_at"))
    if _reservation_canonical_hash(value) != value.get("reservation_canonical_hash"):
        raise GovernedNonproductionPersistenceError("attempt_reservation_canonical_hash_mismatch")
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


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _record_canonical_hash(record: dict[str, Any]) -> str:
    return _sha256({key: value for key, value in record.items() if key != "record_canonical_hash"})


def _reservation_canonical_hash(reservation: dict[str, Any]) -> str:
    return _sha256(
        {
            key: value
            for key, value in reservation.items()
            if key != "reservation_canonical_hash"
        }
    )


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


def _insert_attempt_reservation(
    connection: sqlite3.Connection,
    reservation: dict[str, Any],
) -> None:
    values = [reservation[field] for field in _ATTEMPT_RESERVATION_COLUMN_ORDER]
    columns = ", ".join(_ATTEMPT_RESERVATION_COLUMN_ORDER)
    parameter_markers = ", ".join("?" for _ in _ATTEMPT_RESERVATION_COLUMN_ORDER)
    connection.execute(
        f"INSERT INTO {ATTEMPT_RESERVATION_TABLE} ({columns}) VALUES ({parameter_markers})",
        values,
    )


def _commit_attempt_reservation_connection(connection: sqlite3.Connection) -> None:
    connection.commit()


def _commit_record_connection(connection: sqlite3.Connection) -> None:
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


def _find_attempt_row_by_scope(
    connection: sqlite3.Connection,
    attempt_scope_key: str,
) -> sqlite3.Row | None:
    return connection.execute(
        f"SELECT * FROM {ATTEMPT_RESERVATION_TABLE} WHERE attempt_scope_key = ?",
        (attempt_scope_key,),
    ).fetchone()


def _find_attempt_row_by_id(
    connection: sqlite3.Connection,
    attempt_reservation_id: str,
) -> sqlite3.Row | None:
    return connection.execute(
        f"SELECT * FROM {ATTEMPT_RESERVATION_TABLE} WHERE attempt_reservation_id = ?",
        (attempt_reservation_id,),
    ).fetchone()


def _row_to_record(row: sqlite3.Row) -> dict[str, Any]:
    try:
        record = dict(row)
        if set(record) != set(_COLUMN_ORDER):
            raise ValueError("record columns")
        for field in _JSON_RECORD_FIELDS:
            if not isinstance(record[field], str):
                raise ValueError("record json type")
            record[field] = json.loads(record[field])
        for field in _BOOLEAN_RECORD_FIELDS:
            if record[field] not in {0, 1}:
                raise ValueError("record boolean")
            record[field] = bool(record[field])
        return _validate_record(record)
    except (GovernedNonproductionPersistenceError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise GovernedNonproductionPersistenceError("stored_record_integrity_failure") from exc


def _row_to_reservation(row: sqlite3.Row) -> dict[str, Any]:
    try:
        reservation = dict(row)
        if set(reservation) != set(_ATTEMPT_RESERVATION_COLUMN_ORDER):
            raise ValueError("reservation columns")
        return _validate_reservation(reservation)
    except (GovernedNonproductionPersistenceError, TypeError, ValueError) as exc:
        raise GovernedNonproductionPersistenceError(
            "stored_attempt_reservation_integrity_failure"
        ) from exc


def _snapshot_record_connection(connection: sqlite3.Connection) -> dict[str, Any]:
    rows = connection.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY persisted_record_id").fetchall()
    records: dict[str, str] = {}
    for row in rows:
        record = _row_to_record(row)
        records[record["persisted_record_id"]] = _record_canonical_hash(record)
    return {
        "count": len(records),
        "digest": _sha256(records),
        "records": records,
    }


def _snapshot_attempt_connection(connection: sqlite3.Connection) -> dict[str, Any]:
    rows = connection.execute(
        f"SELECT * FROM {ATTEMPT_RESERVATION_TABLE} ORDER BY attempt_reservation_id"
    ).fetchall()
    records: dict[str, str] = {}
    for row in rows:
        reservation = _row_to_reservation(row)
        records[reservation["attempt_reservation_id"]] = _reservation_canonical_hash(reservation)
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
    return not _snapshot_change_matches(
        before_state,
        after_state,
        intended_id=intended_record["persisted_record_id"],
        intended_hash=_record_canonical_hash(intended_record),
        expected_mutation_count=expected_mutation_count,
    )


def _snapshot_change_matches(
    before_state: dict[str, Any] | None,
    after_state: dict[str, Any],
    *,
    intended_id: str,
    intended_hash: str,
    expected_mutation_count: int,
) -> bool:
    if expected_mutation_count not in {0, 1}:
        return False
    if not isinstance(before_state, dict) or not isinstance(before_state.get("records"), dict):
        return False
    if not isinstance(after_state, dict) or not isinstance(after_state.get("records"), dict):
        return False
    expected_records = dict(before_state["records"])
    if expected_mutation_count == 1:
        if intended_id in expected_records:
            return False
        expected_records[intended_id] = intended_hash
    return expected_records == after_state["records"]


def _records_have_same_stable_binding(
    stored: dict[str, Any],
    expected: dict[str, Any],
) -> bool:
    candidate = deepcopy(expected)
    candidate["created_at"] = stored.get("created_at")
    candidate["record_canonical_hash"] = _record_canonical_hash(candidate)
    return stored == candidate


def _reservations_have_same_stable_binding(
    stored: dict[str, Any],
    expected: dict[str, Any],
) -> bool:
    candidate = deepcopy(expected)
    candidate["reserved_at"] = stored.get("reserved_at")
    candidate["reservation_canonical_hash"] = _reservation_canonical_hash(candidate)
    return stored == candidate


def _verify_attempt_reservation_after_commit(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
    *,
    before_state: dict[str, Any] | None,
    expected_mutation_count: int,
) -> dict[str, Any]:
    try:
        connection = store._open_read_only()
        try:
            row = _find_attempt_row_by_scope(connection, command["attempt_scope_key"])
            reservation = _row_to_reservation(row) if row is not None else None
            after_state = _snapshot_attempt_connection(connection)
        finally:
            connection.close()
        verified = bool(
            reservation is not None
            and _reservations_have_same_stable_binding(
                reservation,
                command["reservation"],
            )
        )
        no_unrelated = _snapshot_change_matches(
            before_state,
            after_state,
            intended_id=command["attempt_reservation_id"],
            intended_hash=_reservation_canonical_hash(command["reservation"]),
            expected_mutation_count=expected_mutation_count,
        )
        return {
            "attempt_reservation_verified": verified,
            "no_unrelated_attempt_change_verified": no_unrelated,
            "after_state": after_state,
        }
    except (GovernedNonproductionPersistenceError, sqlite3.Error):
        return {
            "attempt_reservation_verified": False,
            "no_unrelated_attempt_change_verified": False,
            "after_state": {},
        }


def _verify_full_persistence_state(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
    *,
    attempt_before: dict[str, Any] | None,
    record_before: dict[str, Any] | None,
    expected_record_mutation_count: int,
) -> dict[str, Any]:
    try:
        connection = store._open_read_only()
        try:
            record_row = _find_row_by_idempotency(connection, command["idempotency_key"])
            reservation_row = _find_attempt_row_by_scope(connection, command["attempt_scope_key"])
            record = _row_to_record(record_row) if record_row is not None else None
            reservation = (
                _row_to_reservation(reservation_row) if reservation_row is not None else None
            )
            matching_count = int(
                connection.execute(
                    f"SELECT COUNT(*) FROM {TABLE_NAME} "
                    "WHERE persisted_record_id = ? AND candidate_identity_digest = ?",
                    (
                        command["persisted_record_id"],
                        command["candidate_identity_digest"],
                    ),
                ).fetchone()[0]
            )
            attempt_after = _snapshot_attempt_connection(connection)
            record_after = _snapshot_record_connection(connection)
        finally:
            connection.close()

        exact_record = bool(
            record is not None and _records_have_same_stable_binding(record, command["record"])
        )
        exact_reservation = bool(
            reservation is not None
            and _reservations_have_same_stable_binding(
                reservation,
                command["reservation"],
            )
        )
        no_unrelated_attempt = _snapshot_change_matches(
            attempt_before,
            attempt_after,
            intended_id=command["attempt_reservation_id"],
            intended_hash=_reservation_canonical_hash(command["reservation"]),
            expected_mutation_count=0,
        )
        no_unrelated_record = _snapshot_change_matches(
            record_before,
            record_after,
            intended_id=command["persisted_record_id"],
            intended_hash=_record_canonical_hash(command["record"]),
            expected_mutation_count=expected_record_mutation_count,
        )
        verified = (
            exact_record
            and matching_count == 1
            and exact_reservation
            and no_unrelated_attempt
            and no_unrelated_record
        )
        return {
            "persisted_record_verified": exact_record,
            "exact_record_verified": exact_record,
            "exactly_one_record_verified": matching_count == 1,
            "attempt_reservation_verified": exact_reservation,
            "no_unrelated_attempt_change_verified": no_unrelated_attempt,
            "no_unrelated_record_change_verified": no_unrelated_record,
            "unrelated_record_change_detected": not no_unrelated_record,
            "post_write_readback_verified": verified,
            "production_evidenceitem_created": False,
            "production_case_changed": False,
            "downstream_runtime_called": False,
        }
    except (GovernedNonproductionPersistenceError, sqlite3.Error):
        return {
            "persisted_record_verified": False,
            "exact_record_verified": False,
            "exactly_one_record_verified": False,
            "attempt_reservation_verified": False,
            "no_unrelated_attempt_change_verified": False,
            "no_unrelated_record_change_verified": False,
            "unrelated_record_change_detected": True,
            "post_write_readback_verified": False,
            "production_evidenceitem_created": False,
            "production_case_changed": False,
            "downstream_runtime_called": False,
        }


def _after_attempt_reservation_commit(_command: dict[str, Any]) -> None:
    """Private deterministic test seam after durable attempt consumption."""


def _build_receipt(
    command: dict[str, Any],
    *,
    final_outcome: str,
    attempt_reservation_committed: bool = False,
    mutating_attempt_consumed: bool = False,
    base_record_insert_issued: bool = False,
    base_record_transaction_started: bool = False,
    base_record_transaction_committed: bool = False,
    mutation_count: int | None = 0,
    transaction_rollback_performed: bool = False,
    exact_record_verified: bool = False,
    attempt_reservation_verified: bool = False,
    no_unrelated_attempt_change_verified: bool = False,
    no_unrelated_record_change_verified: bool = False,
    already_exists: bool = False,
    duplicate_conflict: bool = False,
    verification: dict[str, Any] | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    proof = verification or {}
    record = command["record"]
    exact_record = proof.get("exact_record_verified", exact_record_verified)
    exact_reservation = proof.get(
        "attempt_reservation_verified",
        attempt_reservation_verified,
    )
    no_attempt_change = proof.get(
        "no_unrelated_attempt_change_verified",
        no_unrelated_attempt_change_verified,
    )
    no_record_change = proof.get(
        "no_unrelated_record_change_verified",
        no_unrelated_record_change_verified,
    )
    post_write_verified = proof.get(
        "post_write_readback_verified",
        exact_record and exact_reservation and no_attempt_change and no_record_change,
    )
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
        "attempt_reservation_id": command["attempt_reservation_id"],
        "attempt_scope_key": command["attempt_scope_key"],
        "attempt_reservation_committed": attempt_reservation_committed,
        "mutating_attempt_consumed": mutating_attempt_consumed,
        "base_record_insert_issued": base_record_insert_issued,
        "base_record_transaction_started": base_record_transaction_started,
        "base_record_transaction_committed": base_record_transaction_committed,
        "mutation_count": mutation_count,
        "transaction_rollback_performed": transaction_rollback_performed,
        "transaction_rollback_available_before_commit": base_record_transaction_started,
        "transaction_rollback_available_after_commit": False,
        "post_commit_revocation_implemented": False,
        "post_commit_revocation_available": False,
        "already_exists": already_exists,
        "duplicate_conflict": duplicate_conflict,
        "persisted_record_verified": proof.get("persisted_record_verified", exact_record),
        "exact_record_verified": exact_record,
        "exactly_one_record_verified": proof.get("exactly_one_record_verified", exact_record),
        "attempt_reservation_verified": exact_reservation,
        "no_unrelated_attempt_change_verified": no_attempt_change,
        "no_unrelated_record_change_verified": no_record_change,
        "unrelated_record_change_detected": proof.get(
            "unrelated_record_change_detected",
            False,
        ),
        "post_write_readback_verified": post_write_verified,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "final_outcome": final_outcome,
        "created_at": created_at or record["created_at"],
    }


_CREATE_ATTEMPT_RESERVATION_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {ATTEMPT_RESERVATION_TABLE} (
    attempt_reservation_id TEXT PRIMARY KEY,
    attempt_reservation_schema TEXT NOT NULL CHECK (
        attempt_reservation_schema = '{ATTEMPT_RESERVATION_SCHEMA}'
    ),
    attempt_reservation_version TEXT NOT NULL CHECK (
        attempt_reservation_version = '{ATTEMPT_RESERVATION_VERSION}'
    ),
    attempt_scope_key TEXT NOT NULL UNIQUE,
    candidate_identity_digest TEXT NOT NULL,
    input_safe_hash TEXT NOT NULL,
    gate_contract_schema TEXT NOT NULL,
    gate_contract_version TEXT NOT NULL,
    gate_contract_safe_hash TEXT NOT NULL,
    activation_decision_id TEXT NOT NULL,
    activation_decision_safe_hash TEXT NOT NULL,
    target_logical_label TEXT NOT NULL,
    mutation_mode TEXT NOT NULL CHECK (mutation_mode = '{MUTATION_MODE}'),
    idempotency_key TEXT NOT NULL UNIQUE,
    expected_persisted_record_id TEXT NOT NULL,
    maximum_mutating_attempts INTEGER NOT NULL CHECK (
        maximum_mutating_attempts = {MAXIMUM_MUTATING_ATTEMPTS}
    ),
    reserved_attempt_number INTEGER NOT NULL CHECK (
        reserved_attempt_number = {MAXIMUM_MUTATING_ATTEMPTS}
    ),
    reserved_at TEXT NOT NULL,
    reservation_canonical_hash TEXT NOT NULL
)
"""


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
