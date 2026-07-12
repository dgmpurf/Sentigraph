from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any, Final


LATCH_STATE_SCHEMA: Final = "sentigraph_outer_execution_report_latch_state_v0_1"
LATCH_STATE_VERSION: Final = "0.1"
LATCH_STATE_BEGIN_MARKER: Final = (
    "<!-- SENTIGRAPH_OUTER_EXECUTION_LATCH_STATE_V0_1_BEGIN -->"
)
LATCH_STATE_END_MARKER: Final = (
    "<!-- SENTIGRAPH_OUTER_EXECUTION_LATCH_STATE_V0_1_END -->"
)
ATOMIC_UPDATE_RESULT_SCHEMA: Final = (
    "sentigraph_outer_execution_report_atomic_update_result_v0_2"
)
ATOMIC_UPDATE_RESULT_VERSION: Final = "0.2"
RECEIPT_CROSS_BINDING_PROOF_SCHEMA: Final = (
    "sentigraph_outer_execution_writer_receipt_idempotency_cross_binding_proof_v0_1"
)
RECEIPT_CROSS_BINDING_PROOF_VERSION: Final = "0.1"
EXPECTED_WRITER_RECEIPT_SCHEMA: Final = (
    "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
)
IDEMPOTENCY_NAMESPACE: Final = (
    "sentigraph_governed_nonproduction_idempotency_v0_2"
)
EXPECTED_MUTATION_ATTEMPT_LIMIT: Final = 1

_STATE_FIELDS: Final = frozenset(
    {
        "state_schema",
        "state_version",
        "payload_read_latch_state",
        "payload_open_count",
        "payload_read_call_count",
        "payload_reopen_count",
        "payload_read_session_consumed",
        "writer_latch_state",
        "actual_public_writer_invocation_count",
        "writer_retry_count",
        "mutation_attempt_number",
        "F07_activation_execution_use_consumed",
        "MVP_F08_execution_approval_consumed",
        "implementation_mutating_attempt_consumed",
        "terminal_classification",
        "last_transition",
    }
)
_PAYLOAD_STATES: Final = frozenset(
    {
        "armed_not_started",
        "payload_read_started_no_reopen",
        "payload_read_completed_no_reopen",
    }
)
_WRITER_STATES: Final = frozenset(
    {
        "armed_not_started",
        "writer_invocation_started_no_retry",
        "writer_returned",
    }
)
_TERMINAL_CLASSIFICATIONS: Final = frozenset(
    {
        "terminal_before_payload",
        "terminal_after_payload_before_writer",
        "terminal_after_writer",
    }
)
_TRANSITIONS: Final = frozenset(
    {
        "payload_read_started_no_reopen",
        "payload_read_completed_no_reopen",
        "writer_invocation_started_no_retry",
        "writer_returned",
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        "terminal_before_payload",
        "terminal_after_payload_before_writer",
        "terminal_after_writer",
    }
)
_LAST_TRANSITIONS: Final = _TRANSITIONS | {"initial_armed"}
_HASH_RE: Final = re.compile(r"^[a-f0-9]{64}$")
_OPAQUE_ID_RE: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,159}$")
_TOKEN_RE: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
_LOGICAL_LABEL_RE: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,255}$")

_RECEIPT_FIELDS: Final = frozenset(
    {
        "receipt_id",
        "receipt_schema",
        "persisted_record_id",
        "idempotency_key",
        "candidate_identity_digest",
        "activation_decision_safe_hash",
        "target_logical_label",
        "mutation_mode",
        "mutation_attempt_limit",
        "mutation_attempt_number",
        "attempt_reservation_id",
        "attempt_scope_key",
        "attempt_reservation_committed",
        "mutating_attempt_consumed",
        "base_record_insert_issued",
        "base_record_transaction_started",
        "base_record_transaction_committed",
        "mutation_count",
        "transaction_rollback_performed",
        "transaction_rollback_available_before_commit",
        "transaction_rollback_available_after_commit",
        "post_commit_revocation_implemented",
        "post_commit_revocation_available",
        "already_exists",
        "duplicate_conflict",
        "persisted_record_verified",
        "exact_record_verified",
        "exactly_one_record_verified",
        "attempt_reservation_verified",
        "no_unrelated_attempt_change_verified",
        "no_unrelated_record_change_verified",
        "unrelated_record_change_detected",
        "post_write_readback_verified",
        "production_evidenceitem_created",
        "production_case_changed",
        "downstream_runtime_called",
        "final_outcome",
        "created_at",
    }
)
_RECEIPT_BOOLEAN_FIELDS: Final = frozenset(
    {
        "attempt_reservation_committed",
        "mutating_attempt_consumed",
        "base_record_insert_issued",
        "base_record_transaction_started",
        "base_record_transaction_committed",
        "transaction_rollback_performed",
        "transaction_rollback_available_before_commit",
        "transaction_rollback_available_after_commit",
        "post_commit_revocation_implemented",
        "post_commit_revocation_available",
        "already_exists",
        "duplicate_conflict",
        "persisted_record_verified",
        "exact_record_verified",
        "exactly_one_record_verified",
        "attempt_reservation_verified",
        "no_unrelated_attempt_change_verified",
        "no_unrelated_record_change_verified",
        "unrelated_record_change_detected",
        "post_write_readback_verified",
        "production_evidenceitem_created",
        "production_case_changed",
        "downstream_runtime_called",
    }
)
_PROOF_FIELDS: Final = frozenset(
    {
        "proof_schema",
        "proof_version",
        "writer_receipt_schema",
        "writer_receipt_safe_hash",
        "expected_idempotency_key",
        "receipt_idempotency_key",
        "idempotency_cross_binding_verified",
        "expected_persisted_record_id",
        "receipt_persisted_record_id",
        "persisted_record_id_verified",
        "expected_receipt_id",
        "receipt_receipt_id",
        "receipt_id_verified",
        "candidate_identity_digest",
        "input_safe_hash",
        "gate_contract_schema",
        "gate_contract_version",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
        "target_logical_label",
        "mutation_mode",
        "mutation_attempt_number",
        "attempt_reservation_committed",
        "mutating_attempt_consumed",
        "attempt_reservation_verified",
        "final_outcome",
        "proof_canonical_hash",
    }
)
_EXPECTED_BINDING_FIELDS: Final = frozenset(
    {
        "candidate_identity_digest",
        "input_safe_hash",
        "persisted_record_schema",
        "persisted_record_schema_version",
        "gate_contract_schema",
        "gate_contract_version",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
        "mutation_mode",
        "target_logical_label",
        "command_schema",
        "command_version",
        "mutation_attempt_number",
    }
)
_PROOF_PROVENANCE_TOKEN: Final = object()


class OuterExecutionReportLatchError(ValueError):
    """Bounded state or document failure without document-value disclosure."""


class _DuplicateJsonKey(ValueError):
    pass


class _ValidatedReceiptCrossBindingProof(dict[str, Any]):
    pass


def parse_synthetic_writer_receipt_fixture_json(receipt_json: str) -> dict[str, Any]:
    """Parse one strict synthetic receipt fixture without performing IO."""

    if not isinstance(receipt_json, str):
        raise OuterExecutionReportLatchError("receipt_JSON_invalid")
    try:
        value = json.loads(
            receipt_json,
            object_pairs_hook=_strict_object_pairs,
            parse_constant=_reject_json_constant,
        )
    except _DuplicateJsonKey as exc:
        raise OuterExecutionReportLatchError("duplicate_json_key") from exc
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise OuterExecutionReportLatchError("receipt_JSON_invalid") from exc
    return _validate_writer_receipt(value)


def build_writer_receipt_idempotency_cross_binding_proof(
    writer_receipt: dict[str, Any],
    *,
    expected_candidate_identity_digest: str,
    expected_input_safe_hash: str,
    expected_persisted_record_schema: str,
    expected_persisted_record_schema_version: str,
    expected_gate_contract_schema: str,
    expected_gate_contract_version: str,
    expected_gate_contract_safe_hash: str,
    expected_activation_decision_safe_hash: str,
    expected_mutation_mode: str,
    expected_target_logical_label: str,
    expected_command_schema: str,
    expected_command_version: str,
    expected_mutation_attempt_number: int,
) -> dict[str, Any]:
    """Build a strict proof from a synthetic receipt and explicit bindings."""

    expected_bindings = {
        "candidate_identity_digest": expected_candidate_identity_digest,
        "input_safe_hash": expected_input_safe_hash,
        "persisted_record_schema": expected_persisted_record_schema,
        "persisted_record_schema_version": expected_persisted_record_schema_version,
        "gate_contract_schema": expected_gate_contract_schema,
        "gate_contract_version": expected_gate_contract_version,
        "gate_contract_safe_hash": expected_gate_contract_safe_hash,
        "activation_decision_safe_hash": expected_activation_decision_safe_hash,
        "mutation_mode": expected_mutation_mode,
        "target_logical_label": expected_target_logical_label,
        "command_schema": expected_command_schema,
        "command_version": expected_command_version,
        "mutation_attempt_number": expected_mutation_attempt_number,
    }
    return _build_receipt_cross_binding_proof(writer_receipt, expected_bindings)


def validate_writer_receipt_idempotency_cross_binding_proof(
    proof: dict[str, Any],
) -> dict[str, Any]:
    """Revalidate one builder-origin proof against its sealed receipt inputs."""

    if not isinstance(proof, dict) or set(proof) != _PROOF_FIELDS:
        raise OuterExecutionReportLatchError("receipt_proof_fields_invalid")
    _validate_JSON_safe_value(proof)
    projection = dict(proof)
    supplied_hash = projection.pop("proof_canonical_hash")
    if not _is_safe_hash(supplied_hash) or supplied_hash != _sha256_bytes(
        _canonical_json(projection).encode("utf-8")
    ):
        raise OuterExecutionReportLatchError("receipt_proof_hash_mismatch")
    if (
        type(proof) is not _ValidatedReceiptCrossBindingProof
        or getattr(proof, "_provenance_token", None) is not _PROOF_PROVENANCE_TOKEN
    ):
        raise OuterExecutionReportLatchError("receipt_proof_provenance_invalid")
    receipt = getattr(proof, "_sealed_receipt", None)
    expected = getattr(proof, "_sealed_expected_bindings", None)
    if not isinstance(receipt, dict) or not isinstance(expected, dict):
        raise OuterExecutionReportLatchError("receipt_proof_provenance_invalid")
    rebuilt = _build_receipt_cross_binding_proof(receipt, expected)
    if dict(proof) != dict(rebuilt):
        raise OuterExecutionReportLatchError("receipt_proof_revalidation_failed")
    return dict(rebuilt)


def _build_receipt_cross_binding_proof(
    writer_receipt: dict[str, Any],
    expected_bindings: dict[str, Any],
) -> _ValidatedReceiptCrossBindingProof:
    receipt = _validate_writer_receipt(writer_receipt)
    expected = _validate_expected_bindings(expected_bindings)

    if receipt["candidate_identity_digest"] != expected["candidate_identity_digest"]:
        raise OuterExecutionReportLatchError("receipt_candidate_binding_mismatch")
    if (
        receipt["activation_decision_safe_hash"]
        != expected["activation_decision_safe_hash"]
    ):
        raise OuterExecutionReportLatchError("receipt_activation_binding_mismatch")
    if receipt["target_logical_label"] != expected["target_logical_label"]:
        raise OuterExecutionReportLatchError("receipt_target_binding_mismatch")
    if receipt["mutation_mode"] != expected["mutation_mode"]:
        raise OuterExecutionReportLatchError("receipt_mutation_mode_binding_mismatch")
    if receipt["mutation_attempt_limit"] != EXPECTED_MUTATION_ATTEMPT_LIMIT:
        raise OuterExecutionReportLatchError("receipt_mutation_attempt_limit_invalid")
    if (
        receipt["mutation_attempt_number"]
        != expected["mutation_attempt_number"]
    ):
        raise OuterExecutionReportLatchError("receipt_mutation_attempt_number_invalid")

    idempotency_projection = {
        "namespace": IDEMPOTENCY_NAMESPACE,
        "candidate_identity_digest": expected["candidate_identity_digest"],
        "input_safe_hash": expected["input_safe_hash"],
        "persisted_record_schema": expected["persisted_record_schema"],
        "persisted_record_schema_version": expected[
            "persisted_record_schema_version"
        ],
        "gate_contract_schema": expected["gate_contract_schema"],
        "gate_contract_version": expected["gate_contract_version"],
        "gate_contract_safe_hash": expected["gate_contract_safe_hash"],
        "activation_decision_safe_hash": expected["activation_decision_safe_hash"],
        "mutation_mode": expected["mutation_mode"],
        "target_logical_label": expected["target_logical_label"],
        "command_schema": expected["command_schema"],
        "command_version": expected["command_version"],
    }
    expected_idempotency_key = _sha256_bytes(
        _canonical_json(idempotency_projection).encode("utf-8")
    )
    if receipt["idempotency_key"] != expected_idempotency_key:
        raise OuterExecutionReportLatchError("receipt_idempotency_key_mismatch")

    expected_record_id = f"gnpepr-{expected_idempotency_key[:32]}"
    if receipt["persisted_record_id"] != expected_record_id:
        raise OuterExecutionReportLatchError("receipt_record_id_mismatch")
    expected_receipt_id = f"gnpepr-receipt-{expected_idempotency_key[:32]}"
    if receipt["receipt_id"] != expected_receipt_id:
        raise OuterExecutionReportLatchError("receipt_id_mismatch")
    if receipt["attempt_reservation_committed"] is not True:
        raise OuterExecutionReportLatchError("receipt_reservation_not_committed")
    if receipt["mutating_attempt_consumed"] is not True:
        raise OuterExecutionReportLatchError("receipt_attempt_not_consumed")
    if receipt["attempt_reservation_verified"] is not True:
        raise OuterExecutionReportLatchError("receipt_reservation_not_verified")
    if any(
        receipt[field] is not False
        for field in (
            "production_evidenceitem_created",
            "production_case_changed",
            "downstream_runtime_called",
        )
    ):
        raise OuterExecutionReportLatchError("receipt_side_effect_invalid")
    _validate_receipt_claim_consistency(receipt)

    receipt_safe_hash = _sha256_bytes(
        _canonical_json(receipt).encode("utf-8")
    )
    proof_projection = {
        "proof_schema": RECEIPT_CROSS_BINDING_PROOF_SCHEMA,
        "proof_version": RECEIPT_CROSS_BINDING_PROOF_VERSION,
        "writer_receipt_schema": receipt["receipt_schema"],
        "writer_receipt_safe_hash": receipt_safe_hash,
        "expected_idempotency_key": expected_idempotency_key,
        "receipt_idempotency_key": receipt["idempotency_key"],
        "idempotency_cross_binding_verified": True,
        "expected_persisted_record_id": expected_record_id,
        "receipt_persisted_record_id": receipt["persisted_record_id"],
        "persisted_record_id_verified": True,
        "expected_receipt_id": expected_receipt_id,
        "receipt_receipt_id": receipt["receipt_id"],
        "receipt_id_verified": True,
        "candidate_identity_digest": expected["candidate_identity_digest"],
        "input_safe_hash": expected["input_safe_hash"],
        "gate_contract_schema": expected["gate_contract_schema"],
        "gate_contract_version": expected["gate_contract_version"],
        "gate_contract_safe_hash": expected["gate_contract_safe_hash"],
        "activation_decision_safe_hash": expected["activation_decision_safe_hash"],
        "target_logical_label": expected["target_logical_label"],
        "mutation_mode": expected["mutation_mode"],
        "mutation_attempt_number": expected["mutation_attempt_number"],
        "attempt_reservation_committed": True,
        "mutating_attempt_consumed": True,
        "attempt_reservation_verified": True,
        "final_outcome": receipt["final_outcome"],
    }
    proof = _ValidatedReceiptCrossBindingProof(proof_projection)
    proof["proof_canonical_hash"] = _sha256_bytes(
        _canonical_json(proof_projection).encode("utf-8")
    )
    proof._provenance_token = _PROOF_PROVENANCE_TOKEN
    proof._sealed_receipt = deepcopy(receipt)
    proof._sealed_expected_bindings = deepcopy(expected)
    return proof


def build_initial_outer_execution_latch_state() -> dict[str, Any]:
    """Return the canonical unconsumed state for one governed execution."""

    return {
        "state_schema": LATCH_STATE_SCHEMA,
        "state_version": LATCH_STATE_VERSION,
        "payload_read_latch_state": "armed_not_started",
        "payload_open_count": 0,
        "payload_read_call_count": 0,
        "payload_reopen_count": 0,
        "payload_read_session_consumed": False,
        "writer_latch_state": "armed_not_started",
        "actual_public_writer_invocation_count": 0,
        "writer_retry_count": 0,
        "mutation_attempt_number": 1,
        "F07_activation_execution_use_consumed": False,
        "MVP_F08_execution_approval_consumed": False,
        "implementation_mutating_attempt_consumed": False,
        "terminal_classification": None,
        "last_transition": "initial_armed",
    }


def transition_outer_execution_latch_state(
    state: dict[str, Any],
    transition: str,
    *,
    receipt_idempotency_cross_binding_proof: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Apply one allowed monotonic transition to a copied strict state."""

    current = _validate_state(state)
    if not isinstance(transition, str) or transition not in _TRANSITIONS:
        raise OuterExecutionReportLatchError("transition_unknown")
    attempt_consumption_transition = (
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt"
    )
    if (
        transition != attempt_consumption_transition
        and receipt_idempotency_cross_binding_proof is not None
    ):
        raise OuterExecutionReportLatchError("receipt_proof_irrelevant")
    if current["terminal_classification"] is not None:
        raise OuterExecutionReportLatchError("transition_invalid")

    next_state = deepcopy(current)
    if transition == "payload_read_started_no_reopen":
        if not _is_initial_armed(current):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "payload_read_latch_state": transition,
                "payload_open_count": 1,
                "payload_read_call_count": 1,
                "payload_reopen_count": 0,
                "last_transition": transition,
            }
        )
    elif transition == "payload_read_completed_no_reopen":
        if not (
            current["payload_read_latch_state"] == "payload_read_started_no_reopen"
            and current["writer_latch_state"] == "armed_not_started"
            and current["payload_open_count"] == 1
            and current["payload_read_call_count"] == 1
            and current["payload_reopen_count"] == 0
            and current["payload_read_session_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "payload_read_latch_state": transition,
                "payload_read_session_consumed": True,
                "last_transition": transition,
            }
        )
    elif transition == "writer_invocation_started_no_retry":
        if not (
            current["payload_read_latch_state"] == "payload_read_completed_no_reopen"
            and current["payload_read_session_consumed"] is True
            and current["writer_latch_state"] == "armed_not_started"
            and current["actual_public_writer_invocation_count"] == 0
            and current["F07_activation_execution_use_consumed"] is False
            and current["MVP_F08_execution_approval_consumed"] is False
            and current["implementation_mutating_attempt_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "writer_latch_state": transition,
                "actual_public_writer_invocation_count": 1,
                "writer_retry_count": 0,
                "F07_activation_execution_use_consumed": True,
                "MVP_F08_execution_approval_consumed": True,
                "last_transition": transition,
            }
        )
    elif transition == "writer_returned":
        if not (
            current["writer_latch_state"] == "writer_invocation_started_no_retry"
            and current["actual_public_writer_invocation_count"] == 1
            and current["F07_activation_execution_use_consumed"] is True
            and current["MVP_F08_execution_approval_consumed"] is True
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "writer_latch_state": transition,
                "last_transition": transition,
            }
        )
    elif transition == attempt_consumption_transition:
        if not (
            current["payload_read_latch_state"]
            == "payload_read_completed_no_reopen"
            and current["payload_read_session_consumed"] is True
            and current["writer_latch_state"] == "writer_returned"
            and current["actual_public_writer_invocation_count"] == 1
            and current["writer_retry_count"] == 0
            and current["mutation_attempt_number"] == 1
            and current["F07_activation_execution_use_consumed"] is True
            and current["MVP_F08_execution_approval_consumed"] is True
            and current["implementation_mutating_attempt_consumed"] is False
            and current["last_transition"] == "writer_returned"
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        if receipt_idempotency_cross_binding_proof is None:
            raise OuterExecutionReportLatchError("receipt_proof_required")
        validate_writer_receipt_idempotency_cross_binding_proof(
            receipt_idempotency_cross_binding_proof
        )
        next_state.update(
            {
                "implementation_mutating_attempt_consumed": True,
                "last_transition": transition,
            }
        )
    elif transition == "terminal_before_payload":
        if not _is_initial_armed(current):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "terminal_classification": transition,
                "last_transition": transition,
            }
        )
    elif transition == "terminal_after_payload_before_writer":
        if not (
            current["payload_read_latch_state"] == "payload_read_completed_no_reopen"
            and current["payload_read_session_consumed"] is True
            and current["writer_latch_state"] == "armed_not_started"
            and current["actual_public_writer_invocation_count"] == 0
            and current["F07_activation_execution_use_consumed"] is False
            and current["MVP_F08_execution_approval_consumed"] is False
            and current["implementation_mutating_attempt_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "terminal_classification": transition,
                "last_transition": transition,
            }
        )
    else:
        if not (
            current["payload_read_latch_state"] == "payload_read_completed_no_reopen"
            and current["payload_read_session_consumed"] is True
            and current["writer_latch_state"]
            in {"writer_invocation_started_no_retry", "writer_returned"}
            and current["actual_public_writer_invocation_count"] == 1
            and current["F07_activation_execution_use_consumed"] is True
            and current["MVP_F08_execution_approval_consumed"] is True
        ):
            raise OuterExecutionReportLatchError("transition_invalid")
        next_state.update(
            {
                "terminal_classification": transition,
                "last_transition": transition,
            }
        )

    return _validate_state(next_state)


def render_outer_execution_latch_state_block(state: dict[str, Any]) -> str:
    """Render one exact marker-bounded canonical JSON state block."""

    validated = _validate_state(state)
    return (
        f"{LATCH_STATE_BEGIN_MARKER}\n"
        "```json\n"
        f"{_canonical_json(validated)}\n"
        "```\n"
        f"{LATCH_STATE_END_MARKER}"
    )


def parse_outer_execution_latch_state_block(markdown: str) -> dict[str, Any]:
    """Parse exactly one canonical state block from a report document."""

    if not isinstance(markdown, str):
        raise OuterExecutionReportLatchError("report_text_invalid")
    begin_count = markdown.count(LATCH_STATE_BEGIN_MARKER)
    end_count = markdown.count(LATCH_STATE_END_MARKER)
    if begin_count != 1 or end_count != 1:
        raise OuterExecutionReportLatchError("marker_pair_invalid")
    begin = markdown.index(LATCH_STATE_BEGIN_MARKER)
    end_start = markdown.index(LATCH_STATE_END_MARKER)
    if end_start <= begin:
        raise OuterExecutionReportLatchError("marker_pair_invalid")
    end = end_start + len(LATCH_STATE_END_MARKER)
    block = markdown[begin:end]
    lines = block.splitlines()
    if (
        len(lines) != 5
        or lines[0] != LATCH_STATE_BEGIN_MARKER
        or lines[1] != "```json"
        or lines[3] != "```"
        or lines[4] != LATCH_STATE_END_MARKER
    ):
        raise OuterExecutionReportLatchError("state_block_shape_invalid")
    try:
        value = json.loads(
            lines[2],
            object_pairs_hook=_strict_object_pairs,
            parse_constant=_reject_json_constant,
        )
    except _DuplicateJsonKey as exc:
        raise OuterExecutionReportLatchError("duplicate_json_key") from exc
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise OuterExecutionReportLatchError("state_json_invalid") from exc
    validated = _validate_state(value)
    if render_outer_execution_latch_state_block(validated) != block:
        raise OuterExecutionReportLatchError("state_block_not_canonical")
    return validated


def replace_outer_execution_latch_state_block(
    markdown: str,
    expected_state: dict[str, Any],
    next_state: dict[str, Any],
    *,
    receipt_idempotency_cross_binding_proof: dict[str, Any] | None = None,
) -> str:
    """Replace only the complete exact state block after strict CAS checks."""

    expected = _validate_state(expected_state)
    requested = _validate_state(next_state)
    observed = parse_outer_execution_latch_state_block(markdown)
    if observed != expected:
        raise OuterExecutionReportLatchError("expected_state_mismatch")
    transition = requested["last_transition"]
    if transition == "initial_armed":
        raise OuterExecutionReportLatchError("transition_invalid")
    derived = transition_outer_execution_latch_state(
        expected,
        transition,
        receipt_idempotency_cross_binding_proof=(
            receipt_idempotency_cross_binding_proof
        ),
    )
    if derived != requested:
        raise OuterExecutionReportLatchError("next_state_transition_mismatch")

    begin = markdown.index(LATCH_STATE_BEGIN_MARKER)
    end = markdown.index(LATCH_STATE_END_MARKER) + len(LATCH_STATE_END_MARKER)
    replacement = render_outer_execution_latch_state_block(requested)
    updated = markdown[:begin] + replacement + markdown[end:]
    if _outside_segments(markdown) != _outside_segments(updated):
        raise OuterExecutionReportLatchError("outside_block_stability_failure")
    return updated


def atomic_write_outer_execution_report_state(
    path: str | Path,
    expected_file_sha256: str,
    expected_state: dict[str, Any],
    next_state: dict[str, Any],
    *,
    receipt_idempotency_cross_binding_proof: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Atomically apply one strict state transition to one explicit report."""

    result = _base_atomic_result(next_state)
    temporary_path: Path | None = None
    replaced = False
    try:
        attempt_consumption_transition = (
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt"
        )
        if result["transition"] == attempt_consumption_transition:
            if receipt_idempotency_cross_binding_proof is None:
                raise OuterExecutionReportLatchError("receipt_proof_required")
            validated_proof = (
                validate_writer_receipt_idempotency_cross_binding_proof(
                    receipt_idempotency_cross_binding_proof
                )
            )
            result.update(
                {
                    "receipt_idempotency_cross_binding_proof_used": True,
                    "writer_receipt_safe_hash": validated_proof[
                        "writer_receipt_safe_hash"
                    ],
                    "receipt_cross_binding_proof_safe_hash": validated_proof[
                        "proof_canonical_hash"
                    ],
                    "idempotency_cross_binding_verified": True,
                }
            )
        elif receipt_idempotency_cross_binding_proof is not None:
            raise OuterExecutionReportLatchError("receipt_proof_irrelevant")
        if not isinstance(expected_file_sha256, str) or not _HASH_RE.fullmatch(
            expected_file_sha256
        ):
            result["safe_error_code"] = "expected_file_sha256_invalid"
            return result
        report_path = Path(path)
        before_bytes = _read_file_bytes(report_path)
        result["before_file_sha256"] = _sha256_bytes(before_bytes)
        result["before_byte_count"] = len(before_bytes)
        if result["before_file_sha256"] != expected_file_sha256:
            result["safe_error_code"] = "expected_file_sha256_mismatch"
            return result
        try:
            before_text = before_bytes.decode("utf-8", errors="strict")
        except UnicodeError:
            result["safe_error_code"] = "report_UTF8_invalid"
            return result
        if "\ufffd" in before_text:
            result["safe_error_code"] = "report_UTF8_invalid"
            return result

        updated_text = replace_outer_execution_latch_state_block(
            before_text,
            expected_state,
            next_state,
            receipt_idempotency_cross_binding_proof=(
                receipt_idempotency_cross_binding_proof
            ),
        )
        updated_bytes = updated_text.encode("utf-8")
        result["after_file_sha256"] = _sha256_bytes(updated_bytes)
        result["after_byte_count"] = len(updated_bytes)
        result["marker_pair_count"] = 1
        result["outside_block_bytes_unchanged"] = (
            _outside_segments(before_text) == _outside_segments(updated_text)
        )
        if result["outside_block_bytes_unchanged"] is not True:
            result["safe_error_code"] = "outside_block_stability_failure"
            return result

        try:
            with tempfile.NamedTemporaryFile(
                mode="xb",
                dir=report_path.parent,
                prefix=f".{report_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary_path = Path(handle.name)
                handle.write(updated_bytes)
                handle.flush()
                result["flush_performed"] = True
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    result["safe_error_code"] = "temporary_file_fsync_failure"
                    return result
                result["fsync_performed"] = True
        except OSError:
            result["safe_error_code"] = "temporary_file_write_failure"
            return result

        try:
            os.replace(temporary_path, report_path)
        except OSError:
            result["safe_error_code"] = "atomic_replace_failure"
            return result
        replaced = True
        temporary_path = None
        result["atomic_replace_performed"] = True

        try:
            readback_bytes = _read_file_bytes(report_path)
            result["readback_count"] = 1
            readback_text = readback_bytes.decode("utf-8", errors="strict")
            readback_state = parse_outer_execution_latch_state_block(readback_text)
        except (OSError, UnicodeError, OuterExecutionReportLatchError):
            result["status"] = "ambiguous_after_replace"
            result["safe_error_code"] = "post_replace_readback_failure"
            return result
        if (
            _sha256_bytes(readback_bytes) != result["after_file_sha256"]
            or readback_state != _validate_state(next_state)
            or _outside_segments(before_text) != _outside_segments(readback_text)
        ):
            result["status"] = "ambiguous_after_replace"
            result["safe_error_code"] = "post_replace_verification_failure"
            return result

        result.update(
            {
                "status": "updated_and_verified",
                "safe_error_code": "none",
                "next_state_verified": True,
            }
        )
        return result
    except OuterExecutionReportLatchError as exc:
        result["safe_error_code"] = str(exc)
        return result
    except OSError:
        result["safe_error_code"] = (
            "post_replace_readback_failure" if replaced else "report_read_failure"
        )
        if replaced:
            result["status"] = "ambiguous_after_replace"
        return result
    except (TypeError, ValueError):
        result["safe_error_code"] = "invalid_atomic_update_input"
        return result
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def _validate_writer_receipt(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _RECEIPT_FIELDS:
        raise OuterExecutionReportLatchError("receipt_fields_invalid")
    _validate_JSON_safe_value(value)
    if value.get("receipt_schema") != EXPECTED_WRITER_RECEIPT_SCHEMA:
        raise OuterExecutionReportLatchError("receipt_schema_invalid")
    for field in _RECEIPT_BOOLEAN_FIELDS:
        if type(value.get(field)) is not bool:
            raise OuterExecutionReportLatchError("receipt_boolean_type_invalid")
    for field in (
        "mutation_attempt_limit",
        "mutation_attempt_number",
        "mutation_count",
    ):
        if type(value.get(field)) is not int:
            raise OuterExecutionReportLatchError("receipt_integer_type_invalid")
    if value["mutation_count"] not in {0, 1}:
        raise OuterExecutionReportLatchError("receipt_mutation_count_invalid")
    for field in (
        "idempotency_key",
        "candidate_identity_digest",
        "activation_decision_safe_hash",
        "attempt_scope_key",
    ):
        if not _is_safe_hash(value.get(field)):
            raise OuterExecutionReportLatchError("receipt_safe_hash_invalid")
    for field in (
        "receipt_id",
        "persisted_record_id",
        "attempt_reservation_id",
    ):
        if not isinstance(value.get(field), str) or not _OPAQUE_ID_RE.fullmatch(
            value[field]
        ):
            raise OuterExecutionReportLatchError("receipt_opaque_id_invalid")
    for field in ("mutation_mode", "final_outcome"):
        if not isinstance(value.get(field), str) or not _TOKEN_RE.fullmatch(
            value[field]
        ):
            raise OuterExecutionReportLatchError("receipt_token_invalid")
    if not _is_safe_logical_label(value.get("target_logical_label")):
        raise OuterExecutionReportLatchError("receipt_target_logical_label_invalid")
    created_at = value.get("created_at")
    if (
        not isinstance(created_at, str)
        or not 1 <= len(created_at) <= 80
        or any(ord(character) < 32 or ord(character) > 126 for character in created_at)
        or "/" in created_at
        or "\\" in created_at
    ):
        raise OuterExecutionReportLatchError("receipt_created_at_invalid")
    return deepcopy(value)


def _validate_expected_bindings(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _EXPECTED_BINDING_FIELDS:
        raise OuterExecutionReportLatchError("expected_binding_fields_invalid")
    _validate_JSON_safe_value(value)
    for field in (
        "candidate_identity_digest",
        "input_safe_hash",
        "gate_contract_safe_hash",
        "activation_decision_safe_hash",
    ):
        if not _is_safe_hash(value.get(field)):
            raise OuterExecutionReportLatchError("expected_binding_safe_hash_invalid")
    for field in (
        "persisted_record_schema",
        "persisted_record_schema_version",
        "gate_contract_schema",
        "gate_contract_version",
        "mutation_mode",
        "command_schema",
        "command_version",
    ):
        if not isinstance(value.get(field), str) or not _TOKEN_RE.fullmatch(
            value[field]
        ):
            raise OuterExecutionReportLatchError("expected_binding_token_invalid")
    if not _is_safe_logical_label(value.get("target_logical_label")):
        raise OuterExecutionReportLatchError("expected_target_logical_label_invalid")
    if type(value.get("mutation_attempt_number")) is not int:
        raise OuterExecutionReportLatchError("expected_mutation_attempt_type_invalid")
    if value["mutation_attempt_number"] != 1:
        raise OuterExecutionReportLatchError("expected_mutation_attempt_invalid")
    return deepcopy(value)


def _validate_JSON_safe_value(value: Any) -> None:
    if isinstance(value, float):
        raise OuterExecutionReportLatchError("receipt_float_invalid")
    if value is None or type(value) in {bool, int, str}:
        return
    if isinstance(value, list):
        for item in value:
            _validate_JSON_safe_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise OuterExecutionReportLatchError("receipt_JSON_value_invalid")
            _validate_JSON_safe_value(item)
        return
    raise OuterExecutionReportLatchError("receipt_JSON_value_invalid")


def _validate_receipt_claim_consistency(receipt: dict[str, Any]) -> None:
    insert_issued = receipt["base_record_insert_issued"]
    transaction_started = receipt["base_record_transaction_started"]
    transaction_committed = receipt["base_record_transaction_committed"]
    mutation_count = receipt["mutation_count"]
    if transaction_started and not insert_issued:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if transaction_committed and not (insert_issued and transaction_started):
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if mutation_count == 1 and not transaction_committed:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if transaction_committed and mutation_count != 1:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if receipt["transaction_rollback_performed"] and transaction_committed:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if receipt["exact_record_verified"] and not receipt["persisted_record_verified"]:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if receipt["exactly_one_record_verified"] and not receipt["exact_record_verified"]:
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")
    if (
        receipt["unrelated_record_change_detected"]
        and receipt["no_unrelated_record_change_verified"]
    ):
        raise OuterExecutionReportLatchError("receipt_claims_contradictory")


def _is_safe_hash(value: Any) -> bool:
    return isinstance(value, str) and _HASH_RE.fullmatch(value) is not None


def _is_safe_logical_label(value: Any) -> bool:
    if not isinstance(value, str) or not _LOGICAL_LABEL_RE.fullmatch(value):
        return False
    if value.startswith("/") or "\\" in value or "://" in value:
        return False
    return all(segment not in {"", ".", ".."} for segment in value.split("/"))


def _validate_state(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != _STATE_FIELDS:
        raise OuterExecutionReportLatchError("state_fields_invalid")
    if value.get("state_schema") != LATCH_STATE_SCHEMA:
        raise OuterExecutionReportLatchError("state_schema_invalid")
    if value.get("state_version") != LATCH_STATE_VERSION:
        raise OuterExecutionReportLatchError("state_version_invalid")
    for field in (
        "payload_open_count",
        "payload_read_call_count",
        "payload_reopen_count",
        "actual_public_writer_invocation_count",
        "writer_retry_count",
        "mutation_attempt_number",
    ):
        if type(value.get(field)) is not int:
            raise OuterExecutionReportLatchError("state_integer_type_invalid")
    for field in (
        "payload_read_session_consumed",
        "F07_activation_execution_use_consumed",
        "MVP_F08_execution_approval_consumed",
        "implementation_mutating_attempt_consumed",
    ):
        if type(value.get(field)) is not bool:
            raise OuterExecutionReportLatchError("state_boolean_type_invalid")
    if value.get("payload_read_latch_state") not in _PAYLOAD_STATES:
        raise OuterExecutionReportLatchError("payload_latch_state_invalid")
    if value.get("writer_latch_state") not in _WRITER_STATES:
        raise OuterExecutionReportLatchError("writer_latch_state_invalid")
    terminal = value.get("terminal_classification")
    if terminal is not None and terminal not in _TERMINAL_CLASSIFICATIONS:
        raise OuterExecutionReportLatchError("terminal_classification_invalid")
    if value.get("last_transition") not in _LAST_TRANSITIONS:
        raise OuterExecutionReportLatchError("last_transition_invalid")
    if value["writer_retry_count"] != 0:
        raise OuterExecutionReportLatchError("writer_retry_count_invalid")
    if value["mutation_attempt_number"] != 1:
        raise OuterExecutionReportLatchError("mutation_attempt_number_invalid")
    if value["payload_reopen_count"] != 0:
        raise OuterExecutionReportLatchError("state_invariant_invalid")
    if value["payload_open_count"] not in {0, 1}:
        raise OuterExecutionReportLatchError("state_invariant_invalid")
    if value["payload_read_call_count"] not in {0, 1}:
        raise OuterExecutionReportLatchError("state_invariant_invalid")
    if value["actual_public_writer_invocation_count"] not in {0, 1}:
        raise OuterExecutionReportLatchError("state_invariant_invalid")

    payload_state = value["payload_read_latch_state"]
    if payload_state == "armed_not_started":
        if not (
            value["payload_open_count"] == 0
            and value["payload_read_call_count"] == 0
            and value["payload_read_session_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
    elif payload_state == "payload_read_started_no_reopen":
        if not (
            value["payload_open_count"] == 1
            and value["payload_read_call_count"] == 1
            and value["payload_read_session_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
    elif not (
        value["payload_open_count"] == 1
        and value["payload_read_call_count"] == 1
        and value["payload_read_session_consumed"] is True
    ):
        raise OuterExecutionReportLatchError("state_invariant_invalid")

    writer_state = value["writer_latch_state"]
    if writer_state == "armed_not_started":
        if not (
            value["actual_public_writer_invocation_count"] == 0
            and value["F07_activation_execution_use_consumed"] is False
            and value["MVP_F08_execution_approval_consumed"] is False
            and value["implementation_mutating_attempt_consumed"] is False
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
    elif not (
        value["actual_public_writer_invocation_count"] == 1
        and value["F07_activation_execution_use_consumed"] is True
        and value["MVP_F08_execution_approval_consumed"] is True
    ):
        raise OuterExecutionReportLatchError("state_invariant_invalid")
    if (
        value["implementation_mutating_attempt_consumed"] is True
        and writer_state != "writer_returned"
    ):
        raise OuterExecutionReportLatchError("state_invariant_invalid")

    last = value["last_transition"]
    if terminal is not None:
        if terminal != last:
            raise OuterExecutionReportLatchError("state_invariant_invalid")
        if terminal == "terminal_before_payload" and not (
            payload_state == "armed_not_started" and writer_state == "armed_not_started"
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
        if terminal == "terminal_after_payload_before_writer" and not (
            payload_state == "payload_read_completed_no_reopen"
            and writer_state == "armed_not_started"
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
        if terminal == "terminal_after_writer" and not (
            payload_state == "payload_read_completed_no_reopen"
            and writer_state in {"writer_invocation_started_no_retry", "writer_returned"}
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
    else:
        expected_pairs = {
            "initial_armed": ("armed_not_started", "armed_not_started"),
            "payload_read_started_no_reopen": (
                "payload_read_started_no_reopen",
                "armed_not_started",
            ),
            "payload_read_completed_no_reopen": (
                "payload_read_completed_no_reopen",
                "armed_not_started",
            ),
            "writer_invocation_started_no_retry": (
                "payload_read_completed_no_reopen",
                "writer_invocation_started_no_retry",
            ),
            "writer_returned": ("payload_read_completed_no_reopen", "writer_returned"),
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt": (
                "payload_read_completed_no_reopen",
                "writer_returned",
            ),
        }
        if expected_pairs.get(last) != (payload_state, writer_state):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
        if (
            last == "writer_returned"
            and value["implementation_mutating_attempt_consumed"] is not False
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
        if (
            last
            == "implementation_mutating_attempt_consumed_after_verified_writer_receipt"
            and value["implementation_mutating_attempt_consumed"] is not True
        ):
            raise OuterExecutionReportLatchError("state_invariant_invalid")
    return deepcopy(value)


def _is_initial_armed(state: dict[str, Any]) -> bool:
    return state == build_initial_outer_execution_latch_state()


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _strict_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJsonKey
        result[key] = value
    return result


def _reject_json_constant(_value: str) -> None:
    raise ValueError("nonstandard_json_constant")


def _outside_segments(markdown: str) -> tuple[str, str]:
    begin = markdown.index(LATCH_STATE_BEGIN_MARKER)
    end = markdown.index(LATCH_STATE_END_MARKER) + len(LATCH_STATE_END_MARKER)
    return markdown[:begin], markdown[end:]


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _read_file_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _base_atomic_result(next_state: Any) -> dict[str, Any]:
    transition = (
        next_state.get("last_transition")
        if isinstance(next_state, dict) and isinstance(next_state.get("last_transition"), str)
        else "invalid"
    )
    return {
        "result_schema": ATOMIC_UPDATE_RESULT_SCHEMA,
        "result_version": ATOMIC_UPDATE_RESULT_VERSION,
        "status": "blocked",
        "safe_error_code": "unclassified_failure",
        "transition": transition,
        "before_file_sha256": None,
        "after_file_sha256": None,
        "before_byte_count": None,
        "after_byte_count": None,
        "marker_pair_count": 0,
        "flush_performed": False,
        "fsync_performed": False,
        "atomic_replace_performed": False,
        "readback_count": 0,
        "next_state_verified": False,
        "outside_block_bytes_unchanged": False,
        "receipt_idempotency_cross_binding_proof_used": False,
        "writer_receipt_safe_hash": None,
        "receipt_cross_binding_proof_safe_hash": None,
        "idempotency_cross_binding_verified": False,
        "document_content_exposed": False,
        "physical_path_exposed": False,
    }
