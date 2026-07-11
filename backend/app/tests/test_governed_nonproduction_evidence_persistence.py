from __future__ import annotations

import ast
import hashlib
import inspect
import json
import sqlite3
import threading
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

import app.services.governed_nonproduction_evidence_persistence as persistence_module
from app.services.governed_nonproduction_evidence_persistence import (
    ACTIVATION_DECISION_SCOPE,
    ATTEMPT_RESERVATION_SCHEMA,
    ATTEMPT_RESERVATION_TABLE,
    ATTEMPT_RESERVATION_VERSION,
    COMMAND_SCHEMA,
    COMMAND_VERSION,
    GovernedNonproductionEvidencePersistenceStore,
    GovernedNonproductionPersistenceError,
    IDENTITY_SCHEMA,
    INITIAL_STATUS,
    LOGICAL_RUNTIME_TARGET_LABEL,
    MUTATION_MODE,
    PAYLOAD_SCHEMA,
    PAYLOAD_VERSION,
    PERSISTED_RECORD_SCHEMA,
    RECEIPT_SCHEMA,
    REVOCATION_EVENT_SCHEMA,
    SOURCE_CANDIDATE_SCHEMA,
    SOURCE_CANDIDATE_SET_SCHEMA,
    TABLE_NAME,
    build_governed_nonproduction_evidence_persistence_command,
    create_governed_nonproduction_evidence_record,
    find_governed_nonproduction_record_by_idempotency_key,
    validate_exact_locked_candidate_safe_write_payload,
    verify_governed_nonproduction_evidence_record,
)


SYNTHETIC_TARGET_LABEL = "synthetic_governed_nonproduction_target_v0_1"
SYNTHETIC_CREATED_AT = "2026-07-11T00:00:00Z"


@pytest.fixture(autouse=True)
def _fixed_private_utc_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(persistence_module, "_utc_now", lambda: SYNTHETIC_CREATED_AT)


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _hex(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _identity(seed: str = "001") -> dict[str, Any]:
    return {
        "approved_package_name": f"synthetic-package-{seed}",
        "approved_package_role": "synthetic_governance_sample",
        "approved_case_id_hint": f"synthetic-case-{seed}",
        "approved_row_source": f"synthetic-row-source-{seed}",
        "selected_preview_row_opaque_id": f"synthetic-preview-row-{seed}",
        "selected_preview_row_safe_hash": _hex(f"synthetic-preview-{seed}"),
        "final_candidate_id": f"synthetic-candidate-{seed}",
        "final_candidate_safe_hash": _hex(f"synthetic-candidate-{seed}"),
        "final_candidate_schema": SOURCE_CANDIDATE_SET_SCHEMA,
        "identity_schema": IDENTITY_SCHEMA,
        "identity_version": "0.1",
        "hash_algorithm": "sha256",
        "hash_input_scope": "versioned_safe_canonical_projection_only",
        "candidate_lock_status": "locked_for_single_candidate_governance_review_only",
    }


def _candidate_projection(seed: str = "001", *, text: str = "[redacted synthetic sample]") -> dict[str, Any]:
    return {
        "evidence_layer_write_candidate_schema": SOURCE_CANDIDATE_SCHEMA,
        "evidence_layer_write_candidate_id": f"synthetic-write-candidate-{seed}",
        "source_production_evidence_import_candidate_id": f"synthetic-production-import-{seed}",
        "source_evidence_layer_write_candidate_id": f"synthetic-direct-write-{seed}",
        "source_evidence_layer_import_candidate_id": f"synthetic-import-{seed}",
        "source_review_queue_candidate_id": f"synthetic-review-queue-{seed}",
        "source_evidence_candidate_id": f"synthetic-evidence-{seed}",
        "evidence_id_hash": _hex(f"synthetic-evidence-{seed}"),
        "text_snippet_redacted": text,
        "preview_hash": _hex(f"synthetic-preview-content-{seed}"),
        "case_id_hint": f"synthetic-case-{seed}",
        "platform": "synthetic_platform",
        "evidence_type": "synthetic_metadata",
        "created_at_date": "2026-07-10",
        "source_url_present": False,
        "acquisition_mode": "synthetic_fixture",
        "provenance_type": "synthetic_fixture",
        "verification_status": "needs_review",
        "review_status": "review_needed",
        "trust_label": "unverified",
        "redaction_status": "redacted",
        "title_or_label_redacted": "synthetic redacted title",
        "redaction_warnings": ["synthetic_fixture_only"],
        "warning_labels": ["manual_review_required", "synthetic_fixture_only"],
        "blocker_codes": [],
    }


def _lineage_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_production_evidence_import_candidate_id": candidate[
            "source_production_evidence_import_candidate_id"
        ],
        "source_evidence_layer_write_candidate_id": candidate[
            "source_evidence_layer_write_candidate_id"
        ],
        "source_evidence_layer_import_candidate_id": candidate[
            "source_evidence_layer_import_candidate_id"
        ],
        "source_review_queue_candidate_id": candidate["source_review_queue_candidate_id"],
        "source_evidence_candidate_id": candidate["source_evidence_candidate_id"],
        "source_candidate_set_schema": SOURCE_CANDIDATE_SET_SCHEMA,
        "source_candidate_schema": SOURCE_CANDIDATE_SCHEMA,
    }


def _boundary_projection() -> dict[str, Any]:
    return {
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "preview_only": True,
        "import_candidate_only": True,
        "production_import_candidate_only": True,
        "write_candidate_only": True,
        "evidence_layer_write_candidate_only": True,
        "not_production_evidence_item": True,
        "no_evidence_layer_write": True,
        "warning_count": 1,
        "warning_labels": ["manual_review_required"],
    }


def _payload(
    identity: dict[str, Any] | None = None,
    *,
    seed: str = "001",
    text: str = "[redacted synthetic sample]",
) -> dict[str, Any]:
    selected_identity = deepcopy(identity or _identity(seed))
    candidate = _candidate_projection(seed, text=text)
    payload = {
        "payload_schema": PAYLOAD_SCHEMA,
        "payload_version": PAYLOAD_VERSION,
        "source_candidate_set_schema": SOURCE_CANDIDATE_SET_SCHEMA,
        "source_candidate_schema": SOURCE_CANDIDATE_SCHEMA,
        "source_schema_versions": {
            "candidate_set_schema": SOURCE_CANDIDATE_SET_SCHEMA,
            "candidate_schema": SOURCE_CANDIDATE_SCHEMA,
            "identity_schema": IDENTITY_SCHEMA,
            "payload_schema": PAYLOAD_SCHEMA,
        },
        "immutable_candidate_identity": selected_identity,
        "candidate_projection": candidate,
        "lineage_projection": _lineage_projection(candidate),
        "boundary_projection": _boundary_projection(),
    }
    payload["input_safe_hash"] = _digest(payload)
    return payload


def _gate_binding(*, safe_hash: str | None = None) -> dict[str, Any]:
    return {
        "gate_contract_schema": "sentigraph_synthetic_gate_contract_v0_1",
        "gate_contract_version": "0.1",
        "gate_contract_safe_hash": safe_hash or _hex("synthetic-gate-contract"),
    }


def _activation_binding(
    identity: dict[str, Any],
    gate_binding: dict[str, Any],
    *,
    seed: str = "001",
    safe_hash: str | None = None,
) -> dict[str, Any]:
    return {
        "activation_decision_id": f"synthetic-activation-decision-{seed}",
        "activation_decision_schema": "sentigraph_synthetic_activation_decision_v0_1",
        "activation_decision_version": "0.1",
        "activation_decision_safe_hash": safe_hash or _hex(f"synthetic-activation-{seed}"),
        "candidate_identity_digest": _digest(identity),
        "gate_contract_safe_hash": gate_binding["gate_contract_safe_hash"],
        "decision_scope": ACTIVATION_DECISION_SCOPE,
    }


def _command(
    payload: dict[str, Any] | None = None,
    *,
    expected_identity: dict[str, Any] | None = None,
    gate_binding: dict[str, Any] | None = None,
    activation_binding: dict[str, Any] | None = None,
    target_logical_label: str = SYNTHETIC_TARGET_LABEL,
    mutation_attempt_number: int = 1,
) -> dict[str, Any]:
    selected_identity = deepcopy(expected_identity or _identity())
    selected_payload = deepcopy(payload or _payload(selected_identity))
    selected_gate = deepcopy(gate_binding or _gate_binding())
    selected_activation = deepcopy(
        activation_binding or _activation_binding(selected_identity, selected_gate)
    )
    return build_governed_nonproduction_evidence_persistence_command(
        selected_payload,
        expected_identity=selected_identity,
        gate_contract_binding=selected_gate,
        activation_decision_binding=selected_activation,
        target_logical_label=target_logical_label,
        mutation_attempt_number=mutation_attempt_number,
        created_at=SYNTHETIC_CREATED_AT,
    )


def _initialized_store(
    tmp_path: Path,
    command: dict[str, Any],
) -> GovernedNonproductionEvidencePersistenceStore:
    store = GovernedNonproductionEvidencePersistenceStore(
        database_path=tmp_path / "synthetic-evidence.sqlite3",
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        allowed_candidate_identity_digest=command["candidate_identity_digest"],
        enabled=True,
    )
    store.initialize()
    return store


def _writer_inputs_from_command(command: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(command["record"]["safe_payload_projection"])
    candidate = payload["candidate_projection"]
    if "coarse_created_at" in candidate:
        candidate["created_at_date"] = candidate.pop("coarse_created_at")
    return {
        "payload": payload,
        "expected_identity": deepcopy(command["immutable_candidate_identity"]),
        "gate_contract_binding": deepcopy(command["gate_contract_binding"]),
        "activation_decision_binding": deepcopy(command["activation_decision_binding"]),
        "target_logical_label": command["target_logical_label"],
        "mutation_attempt_number": command["mutation_attempt_number"],
    }


def _write(
    store: GovernedNonproductionEvidencePersistenceStore,
    command: dict[str, Any],
) -> dict[str, Any]:
    return create_governed_nonproduction_evidence_record(
        store,
        **_writer_inputs_from_command(command),
    )


def _row_count(database_path: Path) -> int:
    with sqlite3.connect(database_path) as connection:
        return int(connection.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0])


def _reservation_count(database_path: Path) -> int:
    with sqlite3.connect(database_path) as connection:
        return int(
            connection.execute(
                f"SELECT COUNT(*) FROM {ATTEMPT_RESERVATION_TABLE}"
            ).fetchone()[0]
        )


def _assert_error(code: str, callback: Any) -> None:
    with pytest.raises(GovernedNonproductionPersistenceError, match=code):
        callback()


def test_public_symbol_and_schema_contract() -> None:
    expected_symbols = {
        "validate_exact_locked_candidate_safe_write_payload",
        "build_governed_nonproduction_evidence_persistence_command",
        "GovernedNonproductionEvidencePersistenceStore",
        "create_governed_nonproduction_evidence_record",
        "find_governed_nonproduction_record_by_idempotency_key",
        "verify_governed_nonproduction_evidence_record",
    }
    assert all(hasattr(persistence_module, name) for name in expected_symbols)
    assert PAYLOAD_SCHEMA == "sentigraph_exact_locked_candidate_safe_write_payload_v0_1"
    assert COMMAND_SCHEMA == "sentigraph_governed_nonproduction_evidence_persistence_command_v0_2"
    assert COMMAND_VERSION == "0.2"
    assert PERSISTED_RECORD_SCHEMA == "sentigraph_governed_nonproduction_evidence_persistence_record_v0_1"
    assert ATTEMPT_RESERVATION_SCHEMA == (
        "sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1"
    )
    assert ATTEMPT_RESERVATION_VERSION == "0.1"
    assert RECEIPT_SCHEMA == "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
    assert MUTATION_MODE == "transactional_create_only"
    assert INITIAL_STATUS == "governed_nonproduction_pending_human_review"
    assert LOGICAL_RUNTIME_TARGET_LABEL == (
        "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3"
    )
    assert REVOCATION_EVENT_SCHEMA == (
        "sentigraph_governed_nonproduction_evidence_persistence_revocation_event_v0_1"
    )


def test_store_defaults_disabled_and_creates_nothing(tmp_path: Path) -> None:
    missing_parent = tmp_path / "not-created"
    database_path = missing_parent / "synthetic.sqlite3"
    store = GovernedNonproductionEvidencePersistenceStore(
        database_path=database_path,
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        allowed_candidate_identity_digest=_digest(_identity()),
    )
    assert store.enabled is False
    with pytest.raises(GovernedNonproductionPersistenceError, match="store_disabled"):
        store.initialize()
    assert not missing_parent.exists()
    assert not database_path.exists()


def test_enabled_store_requires_existing_parent_and_explicit_targets(tmp_path: Path) -> None:
    command = _command()
    with pytest.raises(GovernedNonproductionPersistenceError, match="physical_database_path_required"):
        GovernedNonproductionEvidencePersistenceStore(
            database_path=None,
            target_logical_label=SYNTHETIC_TARGET_LABEL,
            allowed_candidate_identity_digest=command["candidate_identity_digest"],
            enabled=True,
        ).initialize()
    with pytest.raises(GovernedNonproductionPersistenceError, match="target_logical_label_required"):
        GovernedNonproductionEvidencePersistenceStore(
            database_path=tmp_path / "synthetic.sqlite3",
            target_logical_label="",
            allowed_candidate_identity_digest=command["candidate_identity_digest"],
            enabled=True,
        ).initialize()
    missing_database = tmp_path / "missing" / "synthetic.sqlite3"
    with pytest.raises(GovernedNonproductionPersistenceError, match="database_parent_missing"):
        GovernedNonproductionEvidencePersistenceStore(
            database_path=missing_database,
            target_logical_label=SYNTHETIC_TARGET_LABEL,
            allowed_candidate_identity_digest=command["candidate_identity_digest"],
            enabled=True,
        ).initialize()
    assert not missing_database.exists()


def test_synthetic_initialization_creates_only_expected_tables(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    with sqlite3.connect(store.database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        }
    assert tables == {ATTEMPT_RESERVATION_TABLE, TABLE_NAME}
    assert _row_count(store.database_path) == 0
    assert _reservation_count(store.database_path) == 0


def test_valid_payload_and_hash_validate() -> None:
    identity = _identity()
    payload = _payload(identity)
    validated = validate_exact_locked_candidate_safe_write_payload(
        payload,
        expected_identity=identity,
    )
    assert validated == payload
    assert validated is not payload


@pytest.mark.parametrize("mode", ["missing", "extra"])
def test_top_level_payload_field_set_is_strict(mode: str) -> None:
    identity = _identity()
    payload = _payload(identity)
    if mode == "missing":
        payload.pop("lineage_projection")
    else:
        payload["unexpected"] = "blocked"
    _assert_error(
        "payload_top_level_fields_invalid",
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


@pytest.mark.parametrize("mode", ["missing", "extra", "mismatch"])
def test_immutable_identity_is_strict_and_exact(mode: str) -> None:
    identity = _identity()
    payload = _payload(identity)
    if mode == "missing":
        payload["immutable_candidate_identity"].pop("final_candidate_id")
    elif mode == "extra":
        payload["immutable_candidate_identity"]["fallback_candidate_id"] = "synthetic-fallback"
    else:
        payload["immutable_candidate_identity"]["final_candidate_id"] = "synthetic-candidate-999"
    payload["input_safe_hash"] = _digest({k: v for k, v in payload.items() if k != "input_safe_hash"})
    expected_code = "identity_fields_invalid" if mode != "mismatch" else "identity_mismatch"
    _assert_error(
        expected_code,
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


def test_payload_hash_mismatch_blocks() -> None:
    identity = _identity()
    payload = _payload(identity)
    payload["input_safe_hash"] = "f" * 64
    _assert_error(
        "input_safe_hash_mismatch",
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("payload_schema", "wrong_schema", "payload_schema_invalid"),
        ("payload_version", "9.9", "payload_version_invalid"),
        ("source_candidate_set_schema", "wrong_set", "source_candidate_set_schema_invalid"),
        ("source_candidate_schema", "wrong_item", "source_candidate_schema_invalid"),
    ],
)
def test_payload_schema_and_version_mismatch_blocks(field: str, value: str, code: str) -> None:
    identity = _identity()
    payload = _payload(identity)
    payload[field] = value
    payload["input_safe_hash"] = _digest({k: v for k, v in payload.items() if k != "input_safe_hash"})
    _assert_error(
        code,
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("human_review_required", False),
        ("no_automatic_trust_upgrade", False),
        ("no_evidence_layer_write", False),
        ("warning_count", 0),
        ("warning_labels", ["synthetic_fixture_only"]),
    ],
)
def test_boundary_weakening_blocks(field: str, value: Any) -> None:
    identity = _identity()
    payload = _payload(identity)
    payload["boundary_projection"][field] = value
    payload["input_safe_hash"] = _digest({k: v for k, v in payload.items() if k != "input_safe_hash"})
    _assert_error(
        "boundary_projection_invalid",
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


@pytest.mark.parametrize(
    ("unsafe_field", "unsafe_value"),
    [
        ("raw_author_id", "synthetic-raw-identity"),
        ("private_message", "synthetic private content"),
        ("source_url", "https://invalid.example/synthetic"),
        ("absolute_path", "C:/synthetic/private"),
        ("api_key", "synthetic-secret-value"),
    ],
)
def test_forbidden_candidate_fields_and_values_block(unsafe_field: str, unsafe_value: str) -> None:
    identity = _identity()
    payload = _payload(identity)
    payload["candidate_projection"][unsafe_field] = unsafe_value
    payload["input_safe_hash"] = _digest({k: v for k, v in payload.items() if k != "input_safe_hash"})
    _assert_error(
        "candidate_projection_fields_invalid",
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


@pytest.mark.parametrize(
    "text",
    [
        "x" * 161,
        "https://invalid.example/synthetic",
        "../synthetic-private",
        "synthetic.person@example.invalid",
    ],
)
def test_redacted_text_must_be_bounded_and_safe(text: str) -> None:
    identity = _identity()
    payload = _payload(identity, text=text)
    _assert_error(
        "candidate_projection_value_unsafe",
        lambda: validate_exact_locked_candidate_safe_write_payload(
            payload,
            expected_identity=identity,
        ),
    )


def test_lineage_is_strict_opaque_and_consistent() -> None:
    identity = _identity()
    for mutation, code in [
        (("extra", "synthetic"), "lineage_projection_fields_invalid"),
        (("source_evidence_candidate_id", "../synthetic"), "lineage_projection_value_unsafe"),
        (("source_review_queue_candidate_id", "synthetic-review-queue-999"), "lineage_projection_mismatch"),
    ]:
        payload = _payload(identity)
        payload["lineage_projection"][mutation[0]] = mutation[1]
        payload["input_safe_hash"] = _digest({k: v for k, v in payload.items() if k != "input_safe_hash"})
        _assert_error(
            code,
            lambda payload=payload: validate_exact_locked_candidate_safe_write_payload(
                payload,
                expected_identity=identity,
            ),
        )


def test_pure_validation_and_adapter_perform_no_io(monkeypatch: pytest.MonkeyPatch) -> None:
    identity = _identity()
    payload = _payload(identity)

    def fail_io(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("pure adapter attempted IO")

    monkeypatch.setattr(sqlite3, "connect", fail_io)
    monkeypatch.setattr(Path, "open", fail_io)
    validated = validate_exact_locked_candidate_safe_write_payload(
        payload,
        expected_identity=identity,
    )
    gate = _gate_binding()
    activation = _activation_binding(identity, gate)
    command = build_governed_nonproduction_evidence_persistence_command(
        validated,
        expected_identity=identity,
        gate_contract_binding=gate,
        activation_decision_binding=activation,
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        mutation_attempt_number=1,
        created_at=SYNTHETIC_CREATED_AT,
    )
    assert command["command_schema"] == COMMAND_SCHEMA


def test_command_hashes_and_ids_are_deterministic() -> None:
    first = _command()
    second = _command()
    assert first == second
    assert first["candidate_identity_digest"] == _digest(_identity())
    assert len(first["idempotency_key"]) == 64
    assert first["persisted_record_id"].startswith("gnpepr-")
    assert first["record"]["audit_receipt_reference"].startswith("gnpepr-receipt-")
    assert first["record"]["safe_payload_projection"]["candidate_projection"]["coarse_created_at"] == (
        "2026-07-10"
    )
    assert "created_at_date" not in first["record"]["safe_payload_projection"]["candidate_projection"]


def test_stable_ids_and_replay_bindings_do_not_depend_on_timestamps() -> None:
    identity = _identity()
    payload = _payload(identity)
    gate = _gate_binding()
    activation = _activation_binding(identity, gate)
    common = {
        "expected_identity": identity,
        "gate_contract_binding": gate,
        "activation_decision_binding": activation,
        "target_logical_label": SYNTHETIC_TARGET_LABEL,
        "mutation_attempt_number": 1,
    }
    first = build_governed_nonproduction_evidence_persistence_command(
        payload,
        created_at="2026-07-11T00:00:00Z",
        **common,
    )
    second = build_governed_nonproduction_evidence_persistence_command(
        payload,
        created_at="2026-07-12T00:00:00Z",
        **common,
    )

    stable_fields = {
        "candidate_identity_digest",
        "idempotency_key",
        "persisted_record_id",
        "audit_receipt_reference",
        "attempt_scope_key",
        "attempt_reservation_id",
    }
    assert all(first[field] == second[field] for field in stable_fields)
    assert first["record"]["created_at"] != second["record"]["created_at"]
    assert first["reservation"]["reserved_at"] != second["reservation"]["reserved_at"]


def test_gate_and_activation_bindings_are_strict() -> None:
    identity = _identity()
    payload = _payload(identity)
    gate = _gate_binding()
    activation = _activation_binding(identity, gate)

    wrong_gate = deepcopy(gate)
    wrong_gate["gate_contract_safe_hash"] = "f" * 64
    _assert_error(
        "activation_gate_binding_mismatch",
        lambda: _command(
            payload,
            expected_identity=identity,
            gate_binding=wrong_gate,
            activation_binding=activation,
        ),
    )

    wrong_activation = deepcopy(activation)
    wrong_activation["candidate_identity_digest"] = "e" * 64
    _assert_error(
        "activation_candidate_binding_mismatch",
        lambda: _command(
            payload,
            expected_identity=identity,
            gate_binding=gate,
            activation_binding=wrong_activation,
        ),
    )


@pytest.mark.parametrize("attempt", [0, 2, -1])
def test_mutation_attempt_must_be_exactly_one(attempt: int) -> None:
    _assert_error("mutation_attempt_invalid", lambda: _command(mutation_attempt_number=attempt))


def test_valid_single_create_and_receipt_verification(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    receipt = _write(store, command)
    assert receipt["receipt_schema"] == RECEIPT_SCHEMA
    assert receipt["mutation_count"] == 1
    assert receipt["attempt_reservation_committed"] is True
    assert receipt["mutating_attempt_consumed"] is True
    assert receipt["base_record_transaction_started"] is True
    assert receipt["base_record_transaction_committed"] is True
    assert receipt["already_exists"] is False
    assert receipt["duplicate_conflict"] is False
    assert receipt["persisted_record_verified"] is True
    assert receipt["exactly_one_record_verified"] is True
    assert receipt["unrelated_record_change_detected"] is False
    assert receipt["post_write_readback_verified"] is True
    assert receipt["production_evidenceitem_created"] is False
    assert receipt["production_case_changed"] is False
    assert receipt["downstream_runtime_called"] is False
    assert receipt["final_outcome"] == "created_exactly_one_governed_nonproduction_record"
    assert _row_count(store.database_path) == 1

    record = find_governed_nonproduction_record_by_idempotency_key(
        store,
        command["idempotency_key"],
    )
    assert record is not None
    assert record["persisted_record_id"] == command["persisted_record_id"]
    assert record["status"] == INITIAL_STATUS
    assert record["human_review_required"] is True
    assert record["automatic_trust_upgrade_allowed"] is False
    assert record["revoked_at"] is None
    assert record["revocation_reason"] is None


def test_same_request_is_idempotent_with_zero_second_mutation(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    first = _write(store, command)
    second = _write(store, command)
    assert first["mutation_count"] == 1
    assert second["mutation_count"] == 0
    assert second["already_exists"] is True
    assert second["final_outcome"] == "already_exists_same_record"
    assert second["persisted_record_verified"] is True
    assert _row_count(store.database_path) == 1


def test_exact_replay_with_later_clock_returns_original_creation_time(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    first = _write(store, command)
    monkeypatch.setattr(
        persistence_module,
        "_utc_now",
        lambda: "2026-07-12T00:00:00Z",
    )
    second = _write(store, command)

    assert second["final_outcome"] == "already_exists_same_record"
    assert second["mutation_count"] == 0
    assert second["created_at"] == first["created_at"] == SYNTHETIC_CREATED_AT
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 1


def test_conflicting_payload_for_same_candidate_blocks_without_mutation(tmp_path: Path) -> None:
    identity = _identity()
    first_command = _command(_payload(identity), expected_identity=identity)
    second_payload = _payload(identity, text="[redacted synthetic alternate]")
    second_command = _command(second_payload, expected_identity=identity)
    store = _initialized_store(tmp_path, first_command)
    _write(store, first_command)
    receipt = _write(store, second_command)
    assert receipt["mutation_count"] == 0
    assert receipt["duplicate_conflict"] is True
    assert receipt["final_outcome"] == "blocked_identity_or_payload_conflict"
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 1


def test_conflicting_activation_for_same_candidate_blocks_without_mutation(tmp_path: Path) -> None:
    identity = _identity()
    payload = _payload(identity)
    gate = _gate_binding()
    first = _command(payload, expected_identity=identity, gate_binding=gate)
    alternate_activation = _activation_binding(
        identity,
        gate,
        safe_hash=_hex("synthetic-alternate-activation"),
    )
    second = _command(
        payload,
        expected_identity=identity,
        gate_binding=gate,
        activation_binding=alternate_activation,
    )
    store = _initialized_store(tmp_path, first)
    _write(store, first)
    receipt = _write(store, second)
    assert receipt["mutation_count"] == 0
    assert receipt["duplicate_conflict"] is True
    assert receipt["final_outcome"] == "blocked_identity_or_payload_conflict"
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 1


def test_different_candidate_is_scope_violation_before_connection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    allowed = _command()
    other_identity = _identity("002")
    other = _command(_payload(other_identity, seed="002"), expected_identity=other_identity)
    store = GovernedNonproductionEvidencePersistenceStore(
        database_path=tmp_path / "not-opened.sqlite3",
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        allowed_candidate_identity_digest=allowed["candidate_identity_digest"],
        enabled=True,
    )

    def fail_connect(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("scope violation opened SQLite")

    monkeypatch.setattr(sqlite3, "connect", fail_connect)
    receipt = _write(store, other)
    assert receipt["mutation_count"] == 0
    assert receipt["base_record_transaction_started"] is False
    assert receipt["final_outcome"] == "scope_violation"
    assert not store.database_path.exists()


def test_target_binding_mismatch_blocks_before_connection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command(target_logical_label="synthetic_other_target_v0_1")
    store = GovernedNonproductionEvidencePersistenceStore(
        database_path=tmp_path / "not-opened.sqlite3",
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        allowed_candidate_identity_digest=command["candidate_identity_digest"],
        enabled=True,
    )

    def fail_connect(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("target mismatch opened SQLite")

    monkeypatch.setattr(sqlite3, "connect", fail_connect)
    _assert_error(
        "target_logical_label_mismatch",
        lambda: _write(store, command),
    )


def test_sqlite_uniqueness_constraints_are_enforced(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)
    with sqlite3.connect(store.database_path) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(f"INSERT INTO {TABLE_NAME} SELECT * FROM {TABLE_NAME}")
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                f"INSERT INTO {ATTEMPT_RESERVATION_TABLE} "
                f"SELECT * FROM {ATTEMPT_RESERVATION_TABLE}"
            )
    assert _row_count(store.database_path) == 1
    assert _reservation_count(store.database_path) == 1


def test_known_insert_failure_rolls_back_without_record(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)

    def fail_insert(*_args: Any, **_kwargs: Any) -> Any:
        raise RuntimeError("synthetic insert failure")

    monkeypatch.setattr(persistence_module, "_insert_record", fail_insert)
    receipt = _write(store, command)
    assert receipt["attempt_reservation_committed"] is True
    assert receipt["mutating_attempt_consumed"] is True
    assert receipt["base_record_transaction_started"] is True
    assert receipt["base_record_transaction_committed"] is False
    assert receipt["mutation_count"] == 0
    assert receipt["final_outcome"] == "rolled_back_before_commit"
    assert _row_count(store.database_path) == 0


def test_commit_after_success_ambiguity_uses_read_only_lookup_without_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    original_insert = persistence_module._insert_record
    insert_calls = 0

    def counting_insert(*args: Any, **kwargs: Any) -> Any:
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    def commit_then_ambiguous(connection: sqlite3.Connection) -> None:
        connection.commit()
        raise persistence_module._AmbiguousCommitError("synthetic ambiguous commit")

    monkeypatch.setattr(persistence_module, "_insert_record", counting_insert)
    monkeypatch.setattr(persistence_module, "_commit_record_connection", commit_then_ambiguous)
    receipt = _write(store, command)
    assert insert_calls == 1
    assert receipt["mutation_count"] == 1
    assert receipt["base_record_transaction_committed"] is True
    assert receipt["post_write_readback_verified"] is True
    assert receipt["final_outcome"] == "created_exactly_one_governed_nonproduction_record"
    assert _row_count(store.database_path) == 1


def test_unproven_ambiguous_commit_pauses_without_retry(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    original_insert = persistence_module._insert_record
    insert_calls = 0

    def counting_insert(*args: Any, **kwargs: Any) -> Any:
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    def rollback_then_ambiguous(connection: sqlite3.Connection) -> None:
        connection.rollback()
        raise persistence_module._AmbiguousCommitError("synthetic ambiguous rollback")

    monkeypatch.setattr(persistence_module, "_insert_record", counting_insert)
    monkeypatch.setattr(persistence_module, "_commit_record_connection", rollback_then_ambiguous)
    receipt = _write(store, command)
    assert insert_calls == 1
    assert receipt["mutation_count"] is None
    assert receipt["base_record_transaction_committed"] is False
    assert receipt["post_write_readback_verified"] is False
    assert receipt["final_outcome"] == "paused_ambiguous_commit_not_proven"
    assert _row_count(store.database_path) == 0


def test_verification_detects_unrelated_record_change(tmp_path: Path) -> None:
    first = _command()
    store = _initialized_store(tmp_path, first)
    before = store.safe_snapshot()
    _write(store, first)
    verification = verify_governed_nonproduction_evidence_record(
        store,
        first,
        before_state=before,
        expected_mutation_count=1,
    )
    assert verification["persisted_record_verified"] is True
    assert verification["exactly_one_record_verified"] is True
    assert verification["unrelated_record_change_detected"] is False

    unrelated = deepcopy(first["record"])
    unrelated["persisted_record_id"] = "gnpepr-synthetic-unrelated"
    unrelated["idempotency_key"] = _hex("synthetic-unrelated-idempotency")
    unrelated["candidate_identity_digest"] = _hex("synthetic-unrelated-candidate")
    unrelated["record_canonical_hash"] = persistence_module._record_canonical_hash(unrelated)
    with sqlite3.connect(store.database_path) as connection:
        persistence_module._insert_record(connection, unrelated)
        connection.commit()
    verification = verify_governed_nonproduction_evidence_record(
        store,
        first,
        before_state=before,
        expected_mutation_count=1,
    )
    assert verification["unrelated_record_change_detected"] is True
    assert verification["post_write_readback_verified"] is False


def test_record_and_receipt_do_not_expose_physical_path_or_production_objects(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    receipt = _write(store, command)
    record = find_governed_nonproduction_record_by_idempotency_key(store, command["idempotency_key"])
    rendered = _canonical_json({"receipt": receipt, "record": record})
    assert str(store.database_path) not in rendered
    assert str(tmp_path) not in rendered
    assert receipt["target_logical_label"] == SYNTHETIC_TARGET_LABEL
    assert receipt["production_evidenceitem_created"] is False
    assert receipt["production_case_changed"] is False
    assert receipt["downstream_runtime_called"] is False
    assert record is not None
    assert record["persisted_record_schema"] == PERSISTED_RECORD_SCHEMA
    assert "evidence_items" not in record
    assert "production_case" not in record


def test_receipt_is_not_persisted_and_revocation_is_not_implemented(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)
    with sqlite3.connect(store.database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
            ).fetchall()
        }
        columns = {
            row[1]
            for row in connection.execute(f"PRAGMA table_info({TABLE_NAME})").fetchall()
        }
    assert tables == {ATTEMPT_RESERVATION_TABLE, TABLE_NAME}
    assert "receipt_schema" not in columns
    assert "revoked_at" in columns
    assert "revocation_reason" in columns
    assert not hasattr(store, "revoke")


def test_public_writer_rederives_from_source_inputs_and_rejects_command_authority(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    identity = _identity()
    payload = _payload(identity)
    gate = _gate_binding()
    activation = _activation_binding(identity, gate)
    command = _command(
        payload,
        expected_identity=identity,
        gate_binding=gate,
        activation_binding=activation,
    )
    store = _initialized_store(tmp_path, command)
    monkeypatch.setattr(
        persistence_module,
        "_utc_now",
        lambda: SYNTHETIC_CREATED_AT,
        raising=False,
    )

    receipt = create_governed_nonproduction_evidence_record(
        store,
        payload=payload,
        expected_identity=identity,
        gate_contract_binding=gate,
        activation_decision_binding=activation,
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        mutation_attempt_number=1,
    )

    assert receipt["final_outcome"] == "created_exactly_one_governed_nonproduction_record"
    with pytest.raises(TypeError):
        create_governed_nonproduction_evidence_record(store, command)


def test_public_writer_has_keyword_only_source_contract_and_all_forged_commands_block_before_io(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    signature = inspect.signature(create_governed_nonproduction_evidence_record)
    assert "command" not in signature.parameters
    assert signature.parameters["payload"].kind is inspect.Parameter.KEYWORD_ONLY

    base = _command()
    forged_commands: list[dict[str, Any]] = []

    redacted = deepcopy(base)
    redacted["record"]["safe_payload_projection"]["candidate_projection"][
        "text_snippet_redacted"
    ] = "[redacted caller-forged alternate]"
    redacted["record"]["record_canonical_hash"] = persistence_module._record_canonical_hash(
        redacted["record"]
    )
    forged_commands.append(redacted)

    for field in (
        "candidate_identity_digest",
        "idempotency_key",
        "persisted_record_id",
        "audit_receipt_reference",
        "attempt_scope_key",
        "attempt_reservation_id",
    ):
        forged = deepcopy(base)
        forged[field] = _hex(f"synthetic-forged-{field}")
        forged_commands.append(forged)

    forged_gate = deepcopy(base)
    forged_gate["gate_contract_binding"]["gate_contract_safe_hash"] = _hex(
        "synthetic-forged-gate"
    )
    forged_commands.append(forged_gate)

    forged_activation = deepcopy(base)
    forged_activation["activation_decision_binding"]["activation_decision_safe_hash"] = _hex(
        "synthetic-forged-activation"
    )
    forged_commands.append(forged_activation)

    database_path = tmp_path / "must-not-open.sqlite3"
    store = GovernedNonproductionEvidencePersistenceStore(
        database_path=database_path,
        target_logical_label=SYNTHETIC_TARGET_LABEL,
        allowed_candidate_identity_digest=base["candidate_identity_digest"],
        enabled=True,
    )

    def fail_connect(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("forged command reached SQLite")

    monkeypatch.setattr(sqlite3, "connect", fail_connect)
    for forged in forged_commands:
        with pytest.raises(TypeError):
            create_governed_nonproduction_evidence_record(store, forged)
        with pytest.raises(TypeError):
            create_governed_nonproduction_evidence_record(store, command=forged)
    assert not database_path.exists()


def test_consumed_attempt_blocks_second_call_after_record_rollback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    insert_calls = 0

    def fail_insert(*_args: Any, **_kwargs: Any) -> Any:
        nonlocal insert_calls
        insert_calls += 1
        raise RuntimeError("synthetic base-record insert failure")

    monkeypatch.setattr(persistence_module, "_insert_record", fail_insert)
    first = _write(store, command)
    second = _write(store, command)

    assert first["mutating_attempt_consumed"] is True
    assert second["final_outcome"] == (
        "paused_mutating_attempt_already_consumed_without_verified_record"
    )
    assert second["base_record_insert_issued"] is False
    assert insert_calls == 1
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 0


def test_exact_replay_performs_zero_reservation_and_record_mutations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    first = _write(store, command)

    def fail_mutation(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("exact replay attempted mutation")

    monkeypatch.setattr(persistence_module, "_insert_attempt_reservation", fail_mutation)
    monkeypatch.setattr(persistence_module, "_insert_record", fail_mutation)
    second = _write(store, command)

    assert first["mutation_count"] == 1
    assert second["final_outcome"] == "already_exists_same_record"
    assert second["mutation_count"] == 0
    assert second["base_record_insert_issued"] is False
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 1


def test_ambiguous_base_record_rollback_consumes_attempt_and_later_call_never_inserts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    original_insert = persistence_module._insert_record
    insert_calls = 0

    def counting_insert(*args: Any, **kwargs: Any) -> Any:
        nonlocal insert_calls
        insert_calls += 1
        return original_insert(*args, **kwargs)

    def rollback_then_ambiguous(connection: sqlite3.Connection) -> None:
        connection.rollback()
        raise persistence_module._AmbiguousCommitError("synthetic ambiguous rollback")

    monkeypatch.setattr(persistence_module, "_insert_record", counting_insert)
    monkeypatch.setattr(
        persistence_module,
        "_commit_record_connection",
        rollback_then_ambiguous,
    )
    first = _write(store, command)
    monkeypatch.setattr(
        persistence_module,
        "_commit_record_connection",
        lambda connection: connection.commit(),
    )
    second = _write(store, command)

    assert first["final_outcome"] == "paused_ambiguous_commit_not_proven"
    assert second["final_outcome"] == (
        "paused_mutating_attempt_already_consumed_without_verified_record"
    )
    assert second["base_record_insert_issued"] is False
    assert insert_calls == 1
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 0


def test_controlled_stop_after_reservation_commit_leaves_attempt_consumed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)

    def controlled_stop(_command_value: dict[str, Any]) -> None:
        raise RuntimeError("synthetic controlled stop")

    monkeypatch.setattr(
        persistence_module,
        "_after_attempt_reservation_commit",
        controlled_stop,
    )
    with pytest.raises(RuntimeError, match="synthetic controlled stop"):
        _write(store, command)
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 0

    monkeypatch.setattr(
        persistence_module,
        "_after_attempt_reservation_commit",
        lambda _command_value: None,
    )
    second = _write(store, command)
    assert second["final_outcome"] == (
        "paused_mutating_attempt_already_consumed_without_verified_record"
    )
    assert second["base_record_insert_issued"] is False


def test_reservation_commit_ambiguity_never_reaches_base_record_insert(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    base_insert_calls = 0

    def commit_then_ambiguous(connection: sqlite3.Connection) -> None:
        connection.commit()
        raise persistence_module._AmbiguousCommitError("synthetic reservation ambiguity")

    def count_base_insert(*_args: Any, **_kwargs: Any) -> None:
        nonlocal base_insert_calls
        base_insert_calls += 1

    monkeypatch.setattr(
        persistence_module,
        "_commit_attempt_reservation_connection",
        commit_then_ambiguous,
    )
    monkeypatch.setattr(persistence_module, "_insert_record", count_base_insert)
    first = _write(store, command)
    second = _write(store, command)

    assert first["final_outcome"] == (
        "paused_attempt_reservation_commit_ambiguous_attempt_consumed"
    )
    assert second["final_outcome"] == (
        "paused_mutating_attempt_already_consumed_without_verified_record"
    )
    assert first["base_record_insert_issued"] is False
    assert second["base_record_insert_issued"] is False
    assert base_insert_calls == 0
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 0


def test_unproven_reservation_commit_ambiguity_pauses_without_base_mutation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)

    def rollback_then_ambiguous(connection: sqlite3.Connection) -> None:
        connection.rollback()
        raise persistence_module._AmbiguousCommitError("synthetic unproven reservation")

    def fail_base_insert(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("unproven reservation reached base INSERT")

    monkeypatch.setattr(
        persistence_module,
        "_commit_attempt_reservation_connection",
        rollback_then_ambiguous,
    )
    monkeypatch.setattr(persistence_module, "_insert_record", fail_base_insert)
    receipt = _write(store, command)

    assert receipt["final_outcome"] == "paused_attempt_reservation_commit_ambiguous_not_proven"
    assert receipt["base_record_insert_issued"] is False
    assert _reservation_count(store.database_path) == 0
    assert _row_count(store.database_path) == 0


def test_known_reservation_failure_rolls_back_without_consuming_attempt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)

    def fail_reservation(*_args: Any, **_kwargs: Any) -> None:
        raise RuntimeError("synthetic reservation insert failure")

    monkeypatch.setattr(persistence_module, "_insert_attempt_reservation", fail_reservation)
    receipt = _write(store, command)

    assert receipt["final_outcome"] == "reservation_rolled_back_before_commit"
    assert receipt["attempt_reservation_committed"] is False
    assert receipt["mutating_attempt_consumed"] is False
    assert receipt["base_record_insert_issued"] is False
    assert _reservation_count(store.database_path) == 0
    assert _row_count(store.database_path) == 0


def test_concurrent_identical_calls_allow_at_most_one_base_record_insert(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    reservation_committed = threading.Event()
    release_winner = threading.Event()
    original_insert = persistence_module._insert_record
    insert_calls = 0
    insert_lock = threading.Lock()
    winner_results: list[dict[str, Any]] = []
    winner_errors: list[BaseException] = []

    def hold_after_reservation(_command_value: dict[str, Any]) -> None:
        reservation_committed.set()
        if not release_winner.wait(timeout=5):
            raise AssertionError("synthetic concurrency release timeout")

    def counting_insert(*args: Any, **kwargs: Any) -> Any:
        nonlocal insert_calls
        with insert_lock:
            insert_calls += 1
        return original_insert(*args, **kwargs)

    def run_winner() -> None:
        try:
            winner_results.append(_write(store, command))
        except BaseException as exc:  # pragma: no cover - surfaced by assertions below
            winner_errors.append(exc)

    monkeypatch.setattr(
        persistence_module,
        "_after_attempt_reservation_commit",
        hold_after_reservation,
    )
    monkeypatch.setattr(persistence_module, "_insert_record", counting_insert)
    thread = threading.Thread(target=run_winner, name="synthetic-persistence-winner")
    thread.start()
    assert reservation_committed.wait(timeout=5)
    competing = _write(store, command)
    release_winner.set()
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert winner_errors == []
    assert len(winner_results) == 1
    assert winner_results[0]["final_outcome"] == (
        "created_exactly_one_governed_nonproduction_record"
    )
    assert competing["final_outcome"] == (
        "paused_mutating_attempt_already_consumed_without_verified_record"
    )
    assert competing["base_record_insert_issued"] is False
    assert insert_calls == 1
    assert _reservation_count(store.database_path) == 1
    assert _row_count(store.database_path) == 1


def test_snapshot_recomputes_hash_from_actual_record_columns(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)

    with sqlite3.connect(store.database_path) as connection:
        connection.execute(
            f"UPDATE {TABLE_NAME} SET candidate_role = ? WHERE persisted_record_id = ?",
            ("synthetic_tampered_role", command["persisted_record_id"]),
        )
        connection.commit()

    with pytest.raises(
        GovernedNonproductionPersistenceError,
        match="stored_record_integrity_failure",
    ):
        store.safe_snapshot()


def test_snapshot_detects_stale_hash_after_canonical_json_column_change(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)

    with sqlite3.connect(store.database_path) as connection:
        raw = connection.execute(
            f"SELECT safe_payload_projection FROM {TABLE_NAME} WHERE persisted_record_id = ?",
            (command["persisted_record_id"],),
        ).fetchone()[0]
        projection = json.loads(raw)
        projection["candidate_projection"]["trust_label"] = "synthetic_tampered_trust"
        connection.execute(
            f"UPDATE {TABLE_NAME} SET safe_payload_projection = ? WHERE persisted_record_id = ?",
            (_canonical_json(projection), command["persisted_record_id"]),
        )
        connection.commit()

    with pytest.raises(
        GovernedNonproductionPersistenceError,
        match="stored_record_integrity_failure",
    ):
        store.safe_snapshot()


def test_snapshot_rejects_malformed_stored_record_json(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)

    with sqlite3.connect(store.database_path) as connection:
        connection.execute(
            f"UPDATE {TABLE_NAME} SET lineage_projection = ? WHERE persisted_record_id = ?",
            ("{synthetic-malformed-json", command["persisted_record_id"]),
        )
        connection.commit()

    with pytest.raises(
        GovernedNonproductionPersistenceError,
        match="stored_record_integrity_failure",
    ):
        store.safe_snapshot()


def test_attempt_snapshot_detects_stale_reservation_hash(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    _write(store, command)

    with sqlite3.connect(store.database_path) as connection:
        connection.execute(
            f"UPDATE {ATTEMPT_RESERVATION_TABLE} SET activation_decision_id = ? "
            "WHERE attempt_reservation_id = ?",
            ("synthetic-tampered-activation", command["attempt_reservation_id"]),
        )
        connection.commit()

    with pytest.raises(
        GovernedNonproductionPersistenceError,
        match="stored_attempt_reservation_integrity_failure",
    ):
        store.safe_attempt_snapshot()


def test_unrelated_concurrent_record_insert_forces_conservative_pause(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = _command()
    other_identity = _identity("002")
    unrelated = _command(
        _payload(other_identity, seed="002"),
        expected_identity=other_identity,
    )
    store = _initialized_store(tmp_path, command)

    def commit_then_add_unrelated(connection: sqlite3.Connection) -> None:
        connection.commit()
        with sqlite3.connect(store.database_path) as unrelated_connection:
            persistence_module._insert_record(unrelated_connection, unrelated["record"])
            unrelated_connection.commit()

    monkeypatch.setattr(
        persistence_module,
        "_commit_record_connection",
        commit_then_add_unrelated,
    )
    receipt = _write(store, command)

    assert receipt["final_outcome"] == "paused_post_write_verification_failed"
    assert receipt["exact_record_verified"] is True
    assert receipt["no_unrelated_record_change_verified"] is False
    assert receipt["post_write_readback_verified"] is False
    assert _row_count(store.database_path) == 2


def test_receipt_v02_removes_combined_rollback_revocation_claim(tmp_path: Path) -> None:
    command = _command()
    store = _initialized_store(tmp_path, command)
    receipt = _write(store, command)

    assert receipt["receipt_schema"] == (
        "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
    )
    assert "rollback_or_revocation_available" not in receipt
    assert receipt["attempt_reservation_committed"] is True
    assert receipt["mutating_attempt_consumed"] is True
    assert receipt["base_record_insert_issued"] is True
    assert receipt["base_record_transaction_committed"] is True
    assert receipt["transaction_rollback_performed"] is False
    assert receipt["transaction_rollback_available_after_commit"] is False
    assert receipt["post_commit_revocation_implemented"] is False
    assert receipt["post_commit_revocation_available"] is False
    assert receipt["exact_record_verified"] is True
    assert receipt["attempt_reservation_verified"] is True


def test_new_module_has_no_forbidden_integration_references() -> None:
    source = Path(persistence_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    forbidden_modules = {
        "app.repositories.case_repository",
        "app.services.case_store",
        "app.services.evidence_import",
        "app.services.evidence_ingestion",
        "fastapi",
        "requests",
        "httpx",
        "urllib.request",
        "socket",
        "subprocess",
        "dotenv",
    }
    assert not ((imported_modules | imported_from) & forbidden_modules)
    forbidden = [
        "CaseRepository",
        "save_case_evidence",
        "LocalJsonCaseStore",
        "MongoDbCaseStore",
        "case_store",
        "app.services.evidence_import",
        "app.services.evidence_ingestion",
        "evidence_import.",
        "evidence_ingestion.",
        "FastAPI",
        "APIRouter",
        "import requests",
        "import httpx",
        "urllib.request",
        "import socket",
        "import subprocess",
        "os.getenv",
        "load_dotenv",
        "provider",
        "collector",
    ]
    assert all(value not in source for value in forbidden)
    assert "pickle" not in source
    assert "eval(" not in source
    assert "exec(" not in source
    assert "rollback_or_revocation_available" not in source
