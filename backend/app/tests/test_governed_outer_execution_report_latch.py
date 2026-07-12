from __future__ import annotations

import ast
import hashlib
import importlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest


MODULE_NAME = "app.services.governed_outer_execution_report_latch"
PERSISTENCE_SOURCE = Path(
    "backend/app/services/governed_nonproduction_evidence_persistence.py"
)
EXPECTED_CANDIDATE_DIGEST = (
    "078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54"
)
EXPECTED_INPUT_SAFE_HASH = (
    "71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5"
)
EXPECTED_GATE_SAFE_HASH = (
    "a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"
)
EXPECTED_ACTIVATION_SAFE_HASH = (
    "5906eecd4eabb6d82a07af455f3558590938fc75f007faaa5bdd3299218c03be"
)
EXPECTED_TARGET_LABEL = (
    "runtime/governed_nonproduction_evidence_persistence/"
    "evidence_records_v0_1.sqlite3"
)
EXPECTED_IDEMPOTENCY_KEY = (
    "7410c2b090b44a41587a1fd806231fbc3f2f1e6d553d505db5e885d26d10ecdb"
)
EXPECTED_RECORD_ID = "gnpepr-7410c2b090b44a41587a1fd806231fbc"
EXPECTED_RECEIPT_ID = "gnpepr-receipt-7410c2b090b44a41587a1fd806231fbc"

EXPECTED_RECEIPT_FIELDS = {
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

EXPECTED_PROOF_FIELDS = {
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


@pytest.fixture
def latch():
    return importlib.import_module(MODULE_NAME)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


def _proof_kwargs(**overrides: Any) -> dict[str, Any]:
    values = {
        "expected_candidate_identity_digest": EXPECTED_CANDIDATE_DIGEST,
        "expected_input_safe_hash": EXPECTED_INPUT_SAFE_HASH,
        "expected_persisted_record_schema": (
            "sentigraph_governed_nonproduction_evidence_persistence_record_v0_1"
        ),
        "expected_persisted_record_schema_version": "0.1",
        "expected_gate_contract_schema": (
            "sentigraph_exact_locked_candidate_actual_evidence_layer_write_"
            "execution_gate_contract_v0_1"
        ),
        "expected_gate_contract_version": "0.1",
        "expected_gate_contract_safe_hash": EXPECTED_GATE_SAFE_HASH,
        "expected_activation_decision_safe_hash": EXPECTED_ACTIVATION_SAFE_HASH,
        "expected_mutation_mode": "transactional_create_only",
        "expected_target_logical_label": EXPECTED_TARGET_LABEL,
        "expected_command_schema": (
            "sentigraph_governed_nonproduction_evidence_persistence_command_v0_2"
        ),
        "expected_command_version": "0.2",
        "expected_mutation_attempt_number": 1,
    }
    values.update(overrides)
    return values


def _idempotency_key(**overrides: Any) -> str:
    expected = _proof_kwargs(**overrides)
    projection = {
        "namespace": "sentigraph_governed_nonproduction_idempotency_v0_2",
        "candidate_identity_digest": expected["expected_candidate_identity_digest"],
        "input_safe_hash": expected["expected_input_safe_hash"],
        "persisted_record_schema": expected["expected_persisted_record_schema"],
        "persisted_record_schema_version": expected[
            "expected_persisted_record_schema_version"
        ],
        "gate_contract_schema": expected["expected_gate_contract_schema"],
        "gate_contract_version": expected["expected_gate_contract_version"],
        "gate_contract_safe_hash": expected["expected_gate_contract_safe_hash"],
        "activation_decision_safe_hash": expected[
            "expected_activation_decision_safe_hash"
        ],
        "mutation_mode": expected["expected_mutation_mode"],
        "target_logical_label": expected["expected_target_logical_label"],
        "command_schema": expected["expected_command_schema"],
        "command_version": expected["expected_command_version"],
    }
    return _sha256(_canonical_json(projection).encode("utf-8"))


def _synthetic_receipt(**overrides: Any) -> dict[str, Any]:
    receipt = {
        "receipt_id": EXPECTED_RECEIPT_ID,
        "receipt_schema": (
            "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
        ),
        "persisted_record_id": EXPECTED_RECORD_ID,
        "idempotency_key": EXPECTED_IDEMPOTENCY_KEY,
        "candidate_identity_digest": EXPECTED_CANDIDATE_DIGEST,
        "activation_decision_safe_hash": EXPECTED_ACTIVATION_SAFE_HASH,
        "target_logical_label": EXPECTED_TARGET_LABEL,
        "mutation_mode": "transactional_create_only",
        "mutation_attempt_limit": 1,
        "mutation_attempt_number": 1,
        "attempt_reservation_id": "gnpepr-attempt-7410c2b090b44a41587a1fd806231fbc",
        "attempt_scope_key": _sha256(b"synthetic-safe-attempt-scope"),
        "attempt_reservation_committed": True,
        "mutating_attempt_consumed": True,
        "base_record_insert_issued": False,
        "base_record_transaction_started": False,
        "base_record_transaction_committed": False,
        "mutation_count": 0,
        "transaction_rollback_performed": False,
        "transaction_rollback_available_before_commit": False,
        "transaction_rollback_available_after_commit": False,
        "post_commit_revocation_implemented": False,
        "post_commit_revocation_available": False,
        "already_exists": False,
        "duplicate_conflict": False,
        "persisted_record_verified": False,
        "exact_record_verified": False,
        "exactly_one_record_verified": False,
        "attempt_reservation_verified": True,
        "no_unrelated_attempt_change_verified": True,
        "no_unrelated_record_change_verified": True,
        "unrelated_record_change_detected": False,
        "post_write_readback_verified": False,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
        "final_outcome": (
            "paused_mutating_attempt_already_consumed_without_verified_record"
        ),
        "created_at": "2026-07-13T00:00:00Z",
    }
    receipt.update(overrides)
    assert set(receipt) == EXPECTED_RECEIPT_FIELDS
    return receipt


def _ambiguous_commit_receipt(**overrides: Any) -> dict[str, Any]:
    values = {
        "final_outcome": "paused_ambiguous_commit_not_proven",
        "mutation_count": None,
        "base_record_insert_issued": True,
        "base_record_transaction_started": True,
        "base_record_transaction_committed": False,
        "transaction_rollback_performed": False,
        "transaction_rollback_available_before_commit": True,
        "transaction_rollback_available_after_commit": False,
        "already_exists": False,
        "duplicate_conflict": False,
        "post_write_readback_verified": False,
        "post_commit_revocation_implemented": False,
        "post_commit_revocation_available": False,
        "production_evidenceitem_created": False,
        "production_case_changed": False,
        "downstream_runtime_called": False,
    }
    values.update(overrides)
    return _synthetic_receipt(**values)


def _proof(latch, receipt: dict[str, Any] | None = None, **expected_overrides: Any):
    return latch.build_writer_receipt_idempotency_cross_binding_proof(
        receipt or _synthetic_receipt(),
        **_proof_kwargs(**expected_overrides),
    )


def _raw_block(latch, value: dict[str, Any]) -> str:
    return (
        f"{latch.LATCH_STATE_BEGIN_MARKER}\n"
        "```json\n"
        f"{_canonical_json(value)}\n"
        "```\n"
        f"{latch.LATCH_STATE_END_MARKER}"
    )


def _document(latch, state: dict[str, Any] | None = None) -> str:
    current = state or latch.build_initial_outer_execution_latch_state()
    before = (
        "# Synthetic execution report\n\n"
        "activation_execution_use_consumed = no\n"
        "F07_activation_execution_use_consumed = no\n"
        "MVP_F08_execution_approval_consumed = no\n"
        "execution_approval_consumed = no\n"
        "writer_latch_state = historical_value\n"
        "historical_writer_latch_state = preserved\n\n"
    )
    after = (
        "\n\nactual_public_writer_invocation_count = 0\n"
        "public_writer_invocation_count = historical_zero\n"
        "Narrative bytes remain unchanged.\n"
    )
    return before + latch.render_outer_execution_latch_state_block(current) + after


def _outside(latch, markdown: str) -> tuple[str, str]:
    begin = markdown.index(latch.LATCH_STATE_BEGIN_MARKER)
    end = markdown.index(latch.LATCH_STATE_END_MARKER) + len(
        latch.LATCH_STATE_END_MARKER
    )
    return markdown[:begin], markdown[end:]


def _payload_completed(latch) -> dict[str, Any]:
    state = latch.build_initial_outer_execution_latch_state()
    state = latch.transition_outer_execution_latch_state(
        state, "payload_read_started_no_reopen"
    )
    return latch.transition_outer_execution_latch_state(
        state, "payload_read_completed_no_reopen"
    )


def _writer_started(latch) -> dict[str, Any]:
    return latch.transition_outer_execution_latch_state(
        _payload_completed(latch), "writer_invocation_started_no_retry"
    )


def test_red_naive_substring_reproduction_is_ambiguous() -> None:
    synthetic = (
        "activation_execution_use_consumed = no\n"
        "F07_activation_execution_use_consumed = no\n"
    )
    assert synthetic.count("activation_execution_use_consumed = no") == 2


def test_public_module_and_api_exist(latch) -> None:
    assert latch.LATCH_STATE_SCHEMA == "sentigraph_outer_execution_report_latch_state_v0_1"
    assert latch.LATCH_STATE_VERSION == "0.1"
    for name in (
        "build_initial_outer_execution_latch_state",
        "transition_outer_execution_latch_state",
        "render_outer_execution_latch_state_block",
        "parse_outer_execution_latch_state_block",
        "replace_outer_execution_latch_state_block",
        "atomic_write_outer_execution_report_state",
    ):
        assert callable(getattr(latch, name))


def test_canonical_initial_state_render_parse_round_trip(latch) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    block = latch.render_outer_execution_latch_state_block(state)
    assert latch.parse_outer_execution_latch_state_block(block) == state
    assert state == {
        "F07_activation_execution_use_consumed": False,
        "MVP_F08_execution_approval_consumed": False,
        "actual_public_writer_invocation_count": 0,
        "implementation_mutating_attempt_consumed": False,
        "last_transition": "initial_armed",
        "mutation_attempt_number": 1,
        "payload_open_count": 0,
        "payload_read_call_count": 0,
        "payload_read_latch_state": "armed_not_started",
        "payload_read_session_consumed": False,
        "payload_reopen_count": 0,
        "state_schema": "sentigraph_outer_execution_report_latch_state_v0_1",
        "state_version": "0.1",
        "terminal_classification": None,
        "writer_latch_state": "armed_not_started",
        "writer_retry_count": 0,
    }


def test_render_is_deterministic_compact_canonical_json(latch) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    first = latch.render_outer_execution_latch_state_block(state)
    second = latch.render_outer_execution_latch_state_block(deepcopy(state))
    assert first == second
    json_line = first.splitlines()[2]
    assert json_line == _canonical_json(state)
    assert ": " not in json_line
    assert ", " not in json_line


def test_exact_marker_pair_is_required(latch) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    block = latch.render_outer_execution_latch_state_block(state)
    assert block.count(latch.LATCH_STATE_BEGIN_MARKER) == 1
    assert block.count(latch.LATCH_STATE_END_MARKER) == 1
    assert block.splitlines()[1] == "```json"
    assert block.splitlines()[-2] == "```"


@pytest.mark.parametrize("marker_name", ["LATCH_STATE_BEGIN_MARKER", "LATCH_STATE_END_MARKER"])
def test_missing_marker_is_rejected(latch, marker_name: str) -> None:
    block = latch.render_outer_execution_latch_state_block(
        latch.build_initial_outer_execution_latch_state()
    )
    malformed = block.replace(getattr(latch, marker_name), "", 1)
    with pytest.raises(latch.OuterExecutionReportLatchError, match="marker_pair_invalid"):
        latch.parse_outer_execution_latch_state_block(malformed)


@pytest.mark.parametrize("marker_name", ["LATCH_STATE_BEGIN_MARKER", "LATCH_STATE_END_MARKER"])
def test_duplicate_marker_is_rejected(latch, marker_name: str) -> None:
    marker = getattr(latch, marker_name)
    block = latch.render_outer_execution_latch_state_block(
        latch.build_initial_outer_execution_latch_state()
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="marker_pair_invalid"):
        latch.parse_outer_execution_latch_state_block(marker + "\n" + block)


def test_malformed_json_is_rejected(latch) -> None:
    block = latch.render_outer_execution_latch_state_block(
        latch.build_initial_outer_execution_latch_state()
    )
    malformed = block.replace('{"F07_', '{not-json,"F07_', 1)
    with pytest.raises(latch.OuterExecutionReportLatchError, match="state_json_invalid"):
        latch.parse_outer_execution_latch_state_block(malformed)


def test_duplicate_json_key_is_rejected(latch) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    raw = _canonical_json(state)
    duplicated = raw[:-1] + ',"writer_retry_count":0}'
    block = (
        f"{latch.LATCH_STATE_BEGIN_MARKER}\n```json\n{duplicated}\n```\n"
        f"{latch.LATCH_STATE_END_MARKER}"
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="duplicate_json_key"):
        latch.parse_outer_execution_latch_state_block(block)


@pytest.mark.parametrize("mode", ["missing", "extra"])
def test_exact_state_field_set_is_required(latch, mode: str) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    if mode == "missing":
        state.pop("writer_retry_count")
    else:
        state["nearby_writer_retry_count"] = 0
    with pytest.raises(latch.OuterExecutionReportLatchError, match="state_fields_invalid"):
        latch.parse_outer_execution_latch_state_block(_raw_block(latch, state))


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("state_schema", "wrong_schema", "state_schema_invalid"),
        ("state_version", "9.9", "state_version_invalid"),
    ],
)
def test_schema_and_version_are_exact(latch, field: str, value: str, code: str) -> None:
    state = latch.build_initial_outer_execution_latch_state()
    state[field] = value
    with pytest.raises(latch.OuterExecutionReportLatchError, match=code):
        latch.parse_outer_execution_latch_state_block(_raw_block(latch, state))


def test_valid_payload_start_transition(latch) -> None:
    state = latch.transition_outer_execution_latch_state(
        latch.build_initial_outer_execution_latch_state(),
        "payload_read_started_no_reopen",
    )
    assert state["payload_read_latch_state"] == "payload_read_started_no_reopen"
    assert state["payload_open_count"] == 1
    assert state["payload_read_call_count"] == 1
    assert state["payload_reopen_count"] == 0
    assert state["payload_read_session_consumed"] is False


def test_valid_payload_completed_transition(latch) -> None:
    state = _payload_completed(latch)
    assert state["payload_read_latch_state"] == "payload_read_completed_no_reopen"
    assert state["payload_read_session_consumed"] is True
    assert state["actual_public_writer_invocation_count"] == 0


def test_valid_writer_start_transition(latch) -> None:
    state = _writer_started(latch)
    assert state["writer_latch_state"] == "writer_invocation_started_no_retry"
    assert state["actual_public_writer_invocation_count"] == 1
    assert state["writer_retry_count"] == 0
    assert state["F07_activation_execution_use_consumed"] is True
    assert state["MVP_F08_execution_approval_consumed"] is True
    assert state["implementation_mutating_attempt_consumed"] is False


def test_valid_writer_returned_transition_does_not_infer_attempt_consumption(latch) -> None:
    state = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    assert state["writer_latch_state"] == "writer_returned"
    assert state["implementation_mutating_attempt_consumed"] is False


def test_terminal_before_payload(latch) -> None:
    state = latch.transition_outer_execution_latch_state(
        latch.build_initial_outer_execution_latch_state(), "terminal_before_payload"
    )
    assert state["terminal_classification"] == "terminal_before_payload"
    assert state["payload_open_count"] == 0
    assert state["actual_public_writer_invocation_count"] == 0


def test_terminal_after_payload_before_writer(latch) -> None:
    state = latch.transition_outer_execution_latch_state(
        _payload_completed(latch), "terminal_after_payload_before_writer"
    )
    assert state["payload_read_session_consumed"] is True
    assert state["actual_public_writer_invocation_count"] == 0
    assert state["F07_activation_execution_use_consumed"] is False
    assert state["MVP_F08_execution_approval_consumed"] is False
    assert state["implementation_mutating_attempt_consumed"] is False


def test_terminal_after_writer(latch) -> None:
    state = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "terminal_after_writer"
    )
    assert state["terminal_classification"] == "terminal_after_writer"
    assert state["actual_public_writer_invocation_count"] == 1
    assert state["F07_activation_execution_use_consumed"] is True
    assert state["MVP_F08_execution_approval_consumed"] is True


def test_writer_before_payload_completion_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_invalid"):
        latch.transition_outer_execution_latch_state(
            latch.build_initial_outer_execution_latch_state(),
            "writer_invocation_started_no_retry",
        )


def test_second_writer_start_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_invalid"):
        latch.transition_outer_execution_latch_state(
            _writer_started(latch), "writer_invocation_started_no_retry"
        )


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("payload_open_count", 0, "state_invariant_invalid"),
        ("payload_read_session_consumed", False, "state_invariant_invalid"),
        ("writer_retry_count", 1, "writer_retry_count_invalid"),
        ("mutation_attempt_number", 2, "mutation_attempt_number_invalid"),
    ],
)
def test_invalid_count_boolean_retry_or_attempt_is_rejected(
    latch, field: str, value: Any, code: str
) -> None:
    state = _payload_completed(latch)
    state[field] = value
    with pytest.raises(latch.OuterExecutionReportLatchError, match=code):
        latch.render_outer_execution_latch_state_block(state)


def test_consumed_boolean_cannot_reset(latch) -> None:
    expected = _writer_started(latch)
    next_state = latch.transition_outer_execution_latch_state(expected, "writer_returned")
    next_state["F07_activation_execution_use_consumed"] = False
    markdown = _document(latch, expected)
    with pytest.raises(latch.OuterExecutionReportLatchError):
        latch.replace_outer_execution_latch_state_block(markdown, expected, next_state)


def test_unknown_transition_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_unknown"):
        latch.transition_outer_execution_latch_state(
            latch.build_initial_outer_execution_latch_state(), "future_transition"
        )


def test_overlapping_names_outside_block_are_byte_stable(latch) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    markdown = _document(latch, expected)
    before_outside = _outside(latch, markdown)
    updated = latch.replace_outer_execution_latch_state_block(
        markdown, expected, next_state
    )
    assert _outside(latch, updated) == before_outside
    for line in (
        "activation_execution_use_consumed = no",
        "F07_activation_execution_use_consumed = no",
        "MVP_F08_execution_approval_consumed = no",
        "execution_approval_consumed = no",
        "writer_latch_state = historical_value",
        "historical_writer_latch_state = preserved",
        "actual_public_writer_invocation_count = 0",
        "public_writer_invocation_count = historical_zero",
    ):
        assert line in updated


def test_every_byte_outside_block_is_unchanged(latch) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "terminal_before_payload"
    )
    markdown = "\ufeffprefix\r\n" + _document(latch, expected) + "suffix\r\n"
    outside = _outside(latch, markdown)
    updated = latch.replace_outer_execution_latch_state_block(
        markdown, expected, next_state
    )
    assert _outside(latch, updated) == outside


def test_expected_state_mismatch_is_rejected(latch) -> None:
    actual = latch.build_initial_outer_execution_latch_state()
    wrong = latch.transition_outer_execution_latch_state(
        actual, "terminal_before_payload"
    )
    next_state = latch.transition_outer_execution_latch_state(
        actual, "payload_read_started_no_reopen"
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="expected_state_mismatch"):
        latch.replace_outer_execution_latch_state_block(
            _document(latch, actual), wrong, next_state
        )


def test_atomic_write_and_readback_succeeds_on_tmp_path(latch, tmp_path: Path) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    path = tmp_path / "synthetic-report.md"
    original = _document(latch, expected).encode("utf-8")
    path.write_bytes(original)
    expected_copy = deepcopy(expected)
    next_copy = deepcopy(next_state)

    result = latch.atomic_write_outer_execution_report_state(
        path, _sha256(original), expected, next_state
    )

    assert result["status"] == "updated_and_verified"
    assert result["safe_error_code"] == "none"
    assert result["flush_performed"] is True
    assert result["fsync_performed"] is True
    assert result["atomic_replace_performed"] is True
    assert result["readback_count"] == 1
    assert result["next_state_verified"] is True
    assert result["outside_block_bytes_unchanged"] is True
    assert result["document_content_exposed"] is False
    assert result["physical_path_exposed"] is False
    assert latch.parse_outer_execution_latch_state_block(
        path.read_text(encoding="utf-8")
    ) == next_state
    assert expected == expected_copy
    assert next_state == next_copy


def test_expected_file_hash_mismatch_blocks_without_change(latch, tmp_path: Path) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "terminal_before_payload"
    )
    path = tmp_path / "synthetic-report.md"
    original = _document(latch, expected).encode("utf-8")
    path.write_bytes(original)
    result = latch.atomic_write_outer_execution_report_state(
        path, "0" * 64, expected, next_state
    )
    assert result["status"] == "blocked"
    assert result["safe_error_code"] == "expected_file_sha256_mismatch"
    assert result["atomic_replace_performed"] is False
    assert path.read_bytes() == original


def test_fsync_failure_leaves_original_unchanged(
    latch, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    path = tmp_path / "synthetic-report.md"
    original = _document(latch, expected).encode("utf-8")
    path.write_bytes(original)

    def fail_fsync(_fd: int) -> None:
        raise OSError("synthetic")

    monkeypatch.setattr(latch.os, "fsync", fail_fsync)
    result = latch.atomic_write_outer_execution_report_state(
        path, _sha256(original), expected, next_state
    )
    assert result["status"] == "blocked"
    assert result["safe_error_code"] == "temporary_file_fsync_failure"
    assert result["atomic_replace_performed"] is False
    assert result["document_content_exposed"] is False
    assert result["physical_path_exposed"] is False
    assert path.read_bytes() == original


def test_post_replace_readback_failure_is_fail_closed_and_value_safe(
    latch, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    path = tmp_path / "synthetic-report.md"
    original = _document(latch, expected).encode("utf-8")
    path.write_bytes(original)
    real_read = latch._read_file_bytes
    calls = 0

    def fail_second_read(file_path: Path) -> bytes:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("synthetic")
        return real_read(file_path)

    monkeypatch.setattr(latch, "_read_file_bytes", fail_second_read)
    result = latch.atomic_write_outer_execution_report_state(
        path, _sha256(original), expected, next_state
    )
    assert result["status"] == "ambiguous_after_replace"
    assert result["safe_error_code"] == "post_replace_readback_failure"
    assert result["atomic_replace_performed"] is True
    assert result["readback_count"] == 0
    assert result["document_content_exposed"] is False
    assert result["physical_path_exposed"] is False
    assert str(tmp_path) not in json.dumps(result)
    assert "synthetic" not in json.dumps(result)


def test_no_forbidden_capabilities_or_discovery(latch) -> None:
    source = Path(latch.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    imported_from = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    forbidden_modules = {
        "sqlite3",
        "requests",
        "httpx",
        "urllib.request",
        "socket",
        "subprocess",
        "fastapi",
        "app.services.governed_nonproduction_evidence_persistence",
    }
    assert not ((imported | imported_from) & forbidden_modules)
    forbidden_calls = {"glob", "rglob", "listdir", "scandir", "walk", "print"}
    called = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    } | {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert not (called & forbidden_calls)
    for forbidden_text in (
        "provider",
        "collector",
        "CaseRepository",
        "evidence_import",
        "evidence_ingestion",
        "runtime/",
        "latest",
    ):
        assert forbidden_text not in source


def test_state_inputs_are_never_mutated(latch, tmp_path: Path) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    expected_copy = deepcopy(expected)
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    next_copy = deepcopy(next_state)
    markdown = _document(latch, expected)
    latch.render_outer_execution_latch_state_block(expected)
    latch.parse_outer_execution_latch_state_block(markdown)
    latch.replace_outer_execution_latch_state_block(markdown, expected, next_state)
    path = tmp_path / "synthetic-report.md"
    path.write_text(markdown, encoding="utf-8")
    latch.atomic_write_outer_execution_report_state(
        path, _sha256(markdown.encode("utf-8")), expected, next_state
    )
    assert expected == expected_copy
    assert next_state == next_copy


def test_attempt_consumption_transition_is_recognized_but_requires_proof(latch) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_required"):
        latch.transition_outer_execution_latch_state(
            returned,
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        )


def test_red_committed_CAS_cannot_accept_manual_attempt_consumption(latch) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    hand_edited = deepcopy(returned)
    hand_edited["implementation_mutating_attempt_consumed"] = True
    hand_edited["last_transition"] = (
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt"
    )
    markdown = _document(latch, returned)
    with pytest.raises(latch.OuterExecutionReportLatchError):
        latch.replace_outer_execution_latch_state_block(
            markdown, returned, hand_edited
        )


def test_receipt_idempotency_cross_binding_proof_builder_exists(latch) -> None:
    assert callable(latch.build_writer_receipt_idempotency_cross_binding_proof)


def test_persistence_source_constants_projection_and_receipt_align() -> None:
    source = PERSISTENCE_SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    def assigned_constant(name: str) -> Any:
        node = next(
            item
            for item in tree.body
            if isinstance(item, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == name for target in item.targets)
        )
        return ast.literal_eval(node.value)

    assert assigned_constant("RECEIPT_SCHEMA") == (
        "sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2"
    )
    assert assigned_constant("PERSISTED_RECORD_SCHEMA") == (
        "sentigraph_governed_nonproduction_evidence_persistence_record_v0_1"
    )
    assert assigned_constant("COMMAND_SCHEMA") == (
        "sentigraph_governed_nonproduction_evidence_persistence_command_v0_2"
    )
    assert assigned_constant("MUTATION_MODE") == "transactional_create_only"
    assert assigned_constant("MAXIMUM_MUTATING_ATTEMPTS") == 1

    builder = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef)
        and item.name == "build_governed_nonproduction_evidence_persistence_command"
    )
    projection = next(
        item.value
        for item in builder.body
        if isinstance(item, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "idempotency_projection"
            for target in item.targets
        )
    )
    assert isinstance(projection, ast.Dict)
    assert [key.value for key in projection.keys] == [
        "namespace",
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
    ]
    assert ast.literal_eval(projection.values[0]) == (
        "sentigraph_governed_nonproduction_idempotency_v0_2"
    )

    receipt_builder = next(
        item
        for item in tree.body
        if isinstance(item, ast.FunctionDef) and item.name == "_build_receipt"
    )
    receipt_return = next(
        item
        for item in ast.walk(receipt_builder)
        if isinstance(item, ast.Return) and isinstance(item.value, ast.Dict)
    )
    assert {key.value for key in receipt_return.value.keys} == EXPECTED_RECEIPT_FIELDS


def test_frozen_expected_idempotency_key_recomputes_independently() -> None:
    assert _idempotency_key() == EXPECTED_IDEMPOTENCY_KEY
    assert EXPECTED_RECORD_ID == f"gnpepr-{EXPECTED_IDEMPOTENCY_KEY[:32]}"
    assert EXPECTED_RECEIPT_ID == f"gnpepr-receipt-{EXPECTED_IDEMPOTENCY_KEY[:32]}"


def test_valid_synthetic_receipt_builds_deterministic_exact_proof(latch) -> None:
    first = _proof(latch)
    second = _proof(latch, deepcopy(_synthetic_receipt()))
    assert dict(first) == dict(second)
    assert set(first) == EXPECTED_PROOF_FIELDS
    assert first["proof_schema"] == (
        "sentigraph_outer_execution_writer_receipt_idempotency_cross_binding_proof_v0_1"
    )
    assert first["proof_version"] == "0.1"
    assert first["expected_idempotency_key"] == EXPECTED_IDEMPOTENCY_KEY
    assert first["receipt_idempotency_key"] == EXPECTED_IDEMPOTENCY_KEY
    assert first["idempotency_cross_binding_verified"] is True


def test_proof_and_complete_receipt_canonical_hashes_are_exact(latch) -> None:
    receipt = _synthetic_receipt()
    proof = _proof(latch, receipt)
    projection = dict(proof)
    proof_hash = projection.pop("proof_canonical_hash")
    assert proof_hash == _sha256(_canonical_json(projection).encode("utf-8"))
    assert proof["writer_receipt_safe_hash"] == _sha256(
        _canonical_json(receipt).encode("utf-8")
    )


def test_strict_synthetic_receipt_JSON_parser_rejects_duplicate_keys(latch) -> None:
    raw = _canonical_json(_synthetic_receipt())
    duplicated = raw[:-1] + ',"receipt_schema":"duplicate"}'
    with pytest.raises(latch.OuterExecutionReportLatchError, match="duplicate_json_key"):
        latch.parse_synthetic_writer_receipt_fixture_json(duplicated)


@pytest.mark.parametrize("mode", ["missing", "extra"])
def test_receipt_exact_key_set_is_required(latch, mode: str) -> None:
    receipt = _synthetic_receipt()
    if mode == "missing":
        receipt.pop("attempt_reservation_verified")
    else:
        receipt["nearby_attempt_reservation_verified"] = True
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_fields_invalid"):
        _proof(latch, receipt)


def test_receipt_schema_mismatch_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_schema_invalid"):
        _proof(latch, _synthetic_receipt(receipt_schema="wrong_schema"))


def test_non_JSON_safe_and_recursive_float_values_are_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_JSON_value_invalid"):
        _proof(latch, _synthetic_receipt(created_at=object()))
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_float_invalid"):
        _proof(latch, _synthetic_receipt(final_outcome={"nested": [1.5]}))


def test_integer_truthiness_is_not_accepted_for_receipt_boolean(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_boolean_type_invalid"):
        _proof(latch, _synthetic_receipt(attempt_reservation_committed=1))


@pytest.mark.parametrize(
    ("receipt_field", "value", "expected_override", "expected_value"),
    [
        ("candidate_identity_digest", "0" * 64, None, None),
        (None, None, "expected_input_safe_hash", "0" * 64),
        (None, None, "expected_gate_contract_schema", "wrong_gate_schema"),
        (None, None, "expected_gate_contract_version", "9.9"),
        (None, None, "expected_gate_contract_safe_hash", "0" * 64),
        ("activation_decision_safe_hash", "0" * 64, None, None),
        ("target_logical_label", "synthetic/other.sqlite3", None, None),
        ("mutation_mode", "synthetic_other_mode", None, None),
        (None, None, "expected_command_schema", "wrong_command_schema"),
        (None, None, "expected_command_version", "9.9"),
    ],
)
def test_direct_or_cross_bound_binding_mismatch_is_rejected(
    latch,
    receipt_field: str | None,
    value: Any,
    expected_override: str | None,
    expected_value: Any,
) -> None:
    receipt = _synthetic_receipt()
    expected: dict[str, Any] = {}
    if receipt_field is not None:
        receipt[receipt_field] = value
    if expected_override is not None:
        expected[expected_override] = expected_value
    with pytest.raises(latch.OuterExecutionReportLatchError):
        _proof(latch, receipt, **expected)


@pytest.mark.parametrize(
    ("field", "value", "code"),
    [
        ("mutation_attempt_limit", 2, "receipt_mutation_attempt_limit_invalid"),
        ("mutation_attempt_number", 2, "receipt_mutation_attempt_number_invalid"),
        ("idempotency_key", "0" * 64, "receipt_idempotency_key_mismatch"),
        ("persisted_record_id", "gnpepr-00000000000000000000000000000000", "receipt_record_id_mismatch"),
        ("receipt_id", "gnpepr-receipt-00000000000000000000000000000000", "receipt_id_mismatch"),
    ],
)
def test_attempt_and_derived_identifier_mismatch_is_rejected(
    latch, field: str, value: Any, code: str
) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match=code):
        _proof(latch, _synthetic_receipt(**{field: value}))


@pytest.mark.parametrize(
    ("field", "code"),
    [
        ("attempt_reservation_committed", "receipt_reservation_not_committed"),
        ("mutating_attempt_consumed", "receipt_attempt_not_consumed"),
        ("attempt_reservation_verified", "receipt_reservation_not_verified"),
    ],
)
def test_required_attempt_consumption_facts_must_be_exact_true(
    latch, field: str, code: str
) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match=code):
        _proof(latch, _synthetic_receipt(**{field: False}))


@pytest.mark.parametrize(
    "field",
    ["production_evidenceitem_created", "production_case_changed", "downstream_runtime_called"],
)
def test_production_or_downstream_true_is_rejected(latch, field: str) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_side_effect_invalid"):
        _proof(latch, _synthetic_receipt(**{field: True}))


def test_contradictory_transaction_claim_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_claims_contradictory"):
        _proof(
            latch,
            _synthetic_receipt(
                base_record_insert_issued=False,
                base_record_transaction_started=False,
                base_record_transaction_committed=True,
                mutation_count=1,
            ),
        )


def test_receipt_and_expected_inputs_are_not_mutated(latch) -> None:
    receipt = _synthetic_receipt()
    expected = _proof_kwargs()
    receipt_copy = deepcopy(receipt)
    expected_copy = deepcopy(expected)
    latch.build_writer_receipt_idempotency_cross_binding_proof(receipt, **expected)
    assert receipt == receipt_copy
    assert expected == expected_copy


def test_caller_created_self_consistent_proof_mapping_is_rejected(latch) -> None:
    forged = dict(_proof(latch))
    projection = dict(forged)
    projection.pop("proof_canonical_hash")
    forged["proof_canonical_hash"] = _sha256(
        _canonical_json(projection).encode("utf-8")
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_provenance_invalid"):
        latch.validate_writer_receipt_idempotency_cross_binding_proof(forged)


def test_builder_proof_hash_tampering_is_rejected(latch) -> None:
    proof = _proof(latch)
    proof["proof_canonical_hash"] = "0" * 64
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_hash_mismatch"):
        latch.validate_writer_receipt_idempotency_cross_binding_proof(proof)


def test_builder_proof_receipt_hash_tampering_is_rejected_on_revalidation(latch) -> None:
    proof = _proof(latch)
    proof["writer_receipt_safe_hash"] = "0" * 64
    projection = dict(proof)
    projection.pop("proof_canonical_hash")
    proof["proof_canonical_hash"] = _sha256(
        _canonical_json(projection).encode("utf-8")
    )
    with pytest.raises(
        latch.OuterExecutionReportLatchError,
        match="receipt_proof_revalidation_failed",
    ):
        latch.validate_writer_receipt_idempotency_cross_binding_proof(proof)


def test_valid_receipt_bound_attempt_consumption_transition(latch) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=_proof(latch),
    )
    changed = {
        key for key in returned if returned[key] != consumed[key]
    }
    assert changed == {"implementation_mutating_attempt_consumed", "last_transition"}
    assert consumed["implementation_mutating_attempt_consumed"] is True


def test_attempt_consumption_transition_requires_returned_writer_and_no_terminal(latch) -> None:
    proof = _proof(latch)
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_invalid"):
        latch.transition_outer_execution_latch_state(
            _writer_started(latch),
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
            receipt_idempotency_cross_binding_proof=proof,
        )
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    terminal = latch.transition_outer_execution_latch_state(
        returned, "terminal_after_writer"
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_invalid"):
        latch.transition_outer_execution_latch_state(
            terminal,
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
            receipt_idempotency_cross_binding_proof=proof,
        )


def test_attempt_consumption_transition_requires_valid_proof(latch) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_required"):
        latch.transition_outer_execution_latch_state(
            returned,
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        )
    malformed = dict(_proof(latch))
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_provenance_invalid"):
        latch.transition_outer_execution_latch_state(
            returned,
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
            receipt_idempotency_cross_binding_proof=malformed,
        )


def test_irrelevant_proof_on_ordinary_transition_is_rejected(latch) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_irrelevant"):
        latch.transition_outer_execution_latch_state(
            latch.build_initial_outer_execution_latch_state(),
            "payload_read_started_no_reopen",
            receipt_idempotency_cross_binding_proof=_proof(latch),
        )


def test_attempt_consumption_transition_is_one_time_and_monotonic(latch) -> None:
    proof = _proof(latch)
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    with pytest.raises(latch.OuterExecutionReportLatchError, match="transition_invalid"):
        latch.transition_outer_execution_latch_state(
            consumed,
            "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
            receipt_idempotency_cross_binding_proof=proof,
        )
    reset = deepcopy(consumed)
    reset["implementation_mutating_attempt_consumed"] = False
    with pytest.raises(latch.OuterExecutionReportLatchError):
        latch.render_outer_execution_latch_state_block(reset)


def test_whole_block_CAS_with_valid_proof_succeeds_and_preserves_outside(latch) -> None:
    proof = _proof(latch)
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    outside = _outside(latch, markdown)
    updated = latch.replace_outer_execution_latch_state_block(
        markdown,
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=proof,
    )
    assert latch.parse_outer_execution_latch_state_block(updated) == consumed
    assert _outside(latch, updated) == outside


def test_whole_block_CAS_without_proof_fails_without_output(latch) -> None:
    proof = _proof(latch)
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    with pytest.raises(latch.OuterExecutionReportLatchError, match="receipt_proof_required"):
        latch.replace_outer_execution_latch_state_block(markdown, returned, consumed)
    assert latch.parse_outer_execution_latch_state_block(markdown) == returned


def test_atomic_receipt_bound_transition_and_v02_metadata(latch, tmp_path: Path) -> None:
    proof = _proof(latch)
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    path = tmp_path / "synthetic-report.md"
    path.write_bytes(markdown.encode("utf-8"))
    result = latch.atomic_write_outer_execution_report_state(
        path,
        _sha256(markdown.encode("utf-8")),
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=proof,
    )
    assert result["result_schema"] == (
        "sentigraph_outer_execution_report_atomic_update_result_v0_2"
    )
    assert result["result_version"] == "0.2"
    assert result["status"] == "updated_and_verified"
    assert result["receipt_idempotency_cross_binding_proof_used"] is True
    assert result["writer_receipt_safe_hash"] == proof["writer_receipt_safe_hash"]
    assert result["receipt_cross_binding_proof_safe_hash"] == proof[
        "proof_canonical_hash"
    ]
    assert result["idempotency_cross_binding_verified"] is True


def test_atomic_invalid_proof_leaves_original_unchanged(latch, tmp_path: Path) -> None:
    valid = _proof(latch)
    invalid = dict(valid)
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=valid,
    )
    markdown = _document(latch, returned)
    path = tmp_path / "synthetic-report.md"
    path.write_text(markdown, encoding="utf-8")
    result = latch.atomic_write_outer_execution_report_state(
        path,
        _sha256(markdown.encode("utf-8")),
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=invalid,
    )
    assert result["status"] == "blocked"
    assert result["atomic_replace_performed"] is False
    assert path.read_text(encoding="utf-8") == markdown


def test_terminal_after_writer_preserves_consumed_true_or_false(latch) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    false_terminal = latch.transition_outer_execution_latch_state(
        returned, "terminal_after_writer"
    )
    assert false_terminal["implementation_mutating_attempt_consumed"] is False

    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=_proof(latch),
    )
    true_terminal = latch.transition_outer_execution_latch_state(
        consumed, "terminal_after_writer"
    )
    assert true_terminal["implementation_mutating_attempt_consumed"] is True


def test_ordinary_atomic_transition_reports_no_proof_metadata(
    latch, tmp_path: Path
) -> None:
    expected = latch.build_initial_outer_execution_latch_state()
    next_state = latch.transition_outer_execution_latch_state(
        expected, "payload_read_started_no_reopen"
    )
    markdown = _document(latch, expected)
    path = tmp_path / "synthetic-report.md"
    path.write_bytes(markdown.encode("utf-8"))
    result = latch.atomic_write_outer_execution_report_state(
        path, _sha256(markdown.encode("utf-8")), expected, next_state
    )
    assert result["status"] == "updated_and_verified"
    assert result["receipt_idempotency_cross_binding_proof_used"] is False
    assert result["writer_receipt_safe_hash"] is None
    assert result["receipt_cross_binding_proof_safe_hash"] is None
    assert result["idempotency_cross_binding_verified"] is False


def test_red_valid_ambiguous_commit_receipt_with_null_mutation_count_parses(
    latch,
) -> None:
    receipt = _ambiguous_commit_receipt()
    parsed = latch.parse_synthetic_writer_receipt_fixture_json(
        _canonical_json(receipt)
    )
    assert parsed == receipt


def test_red_valid_verified_ambiguous_commit_receipt_builds_proof(latch) -> None:
    proof = _proof(latch, _ambiguous_commit_receipt())
    assert proof["attempt_reservation_verified"] is True
    assert proof["final_outcome"] == "paused_ambiguous_commit_not_proven"


def test_red_ambiguous_receipt_proof_completes_atomic_transition(
    latch, tmp_path: Path
) -> None:
    proof = _proof(latch, _ambiguous_commit_receipt())
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    path = tmp_path / "synthetic-report.md"
    path.write_bytes(markdown.encode("utf-8"))
    result = latch.atomic_write_outer_execution_report_state(
        path,
        _sha256(markdown.encode("utf-8")),
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=proof,
    )
    assert result["status"] == "updated_and_verified"


def test_ambiguous_receipt_proof_preserves_complete_receipt_hash(latch) -> None:
    receipt = _ambiguous_commit_receipt()
    proof = _proof(latch, receipt)
    validated = latch.validate_writer_receipt_idempotency_cross_binding_proof(
        proof
    )
    expected_hash = _sha256(_canonical_json(receipt).encode("utf-8"))
    assert proof["writer_receipt_safe_hash"] == expected_hash
    assert validated["writer_receipt_safe_hash"] == expected_hash


def test_ambiguous_receipt_without_verified_reservation_is_structurally_valid_only(
    latch,
) -> None:
    receipt = _ambiguous_commit_receipt(attempt_reservation_verified=False)
    parsed = latch.parse_synthetic_writer_receipt_fixture_json(
        _canonical_json(receipt)
    )
    assert parsed["attempt_reservation_verified"] is False
    with pytest.raises(
        latch.OuterExecutionReportLatchError,
        match="receipt_reservation_not_verified",
    ):
        _proof(latch, receipt)


def test_ambiguous_receipt_is_not_persisted_record_success(latch) -> None:
    parsed = latch.parse_synthetic_writer_receipt_fixture_json(
        _canonical_json(_ambiguous_commit_receipt())
    )
    assert parsed["final_outcome"] == "paused_ambiguous_commit_not_proven"
    assert parsed["base_record_transaction_committed"] is False
    assert parsed["mutation_count"] is None
    assert parsed["persisted_record_verified"] is False
    assert parsed["exact_record_verified"] is False
    assert parsed["exactly_one_record_verified"] is False
    assert parsed["post_write_readback_verified"] is False


@pytest.mark.parametrize(
    "final_outcome",
    [
        "created_exactly_one_governed_nonproduction_record",
        "already_exists_same_record",
        "rolled_back_before_commit",
        "reservation_rolled_back_before_commit",
        "paused_mutating_attempt_already_consumed_without_verified_record",
        "paused_attempt_reservation_commit_ambiguous_attempt_consumed",
        "paused_attempt_reservation_commit_ambiguous_not_proven",
        "paused_post_write_verification_failed",
        "scope_violation",
        "blocked_identity_or_payload_conflict",
        "synthetic_unknown_outcome",
    ],
)
def test_null_mutation_count_is_rejected_for_unrelated_outcome(
    latch, final_outcome: str
) -> None:
    with pytest.raises(
        latch.OuterExecutionReportLatchError,
        match="receipt_null_mutation_shape_invalid",
    ):
        latch.parse_synthetic_writer_receipt_fixture_json(
            _canonical_json(
                _ambiguous_commit_receipt(final_outcome=final_outcome)
            )
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("attempt_reservation_committed", False),
        ("mutating_attempt_consumed", False),
        ("base_record_insert_issued", False),
        ("base_record_transaction_started", False),
        ("base_record_transaction_committed", True),
        ("transaction_rollback_performed", True),
        ("transaction_rollback_available_before_commit", False),
        ("transaction_rollback_available_after_commit", True),
        ("already_exists", True),
        ("duplicate_conflict", True),
        ("post_write_readback_verified", True),
        ("post_commit_revocation_implemented", True),
        ("post_commit_revocation_available", True),
        ("production_evidenceitem_created", True),
        ("production_case_changed", True),
        ("downstream_runtime_called", True),
    ],
)
def test_null_mutation_count_requires_exact_ambiguous_shape(
    latch, field: str, value: bool
) -> None:
    with pytest.raises(
        latch.OuterExecutionReportLatchError,
        match="receipt_null_mutation_shape_invalid",
    ):
        latch.parse_synthetic_writer_receipt_fixture_json(
            _canonical_json(_ambiguous_commit_receipt(**{field: value}))
        )


def test_valid_success_receipt_with_one_mutation_remains_accepted(latch) -> None:
    receipt = _synthetic_receipt(
        final_outcome="created_exactly_one_governed_nonproduction_record",
        base_record_insert_issued=True,
        base_record_transaction_started=True,
        base_record_transaction_committed=True,
        mutation_count=1,
        transaction_rollback_available_before_commit=True,
        persisted_record_verified=True,
        exact_record_verified=True,
        exactly_one_record_verified=True,
        post_write_readback_verified=True,
    )
    parsed = latch.parse_synthetic_writer_receipt_fixture_json(
        _canonical_json(receipt)
    )
    assert parsed["mutation_count"] == 1
    assert _proof(latch, receipt)["mutating_attempt_consumed"] is True


def test_valid_noncommitting_receipt_with_zero_mutations_remains_accepted(
    latch,
) -> None:
    receipt = _synthetic_receipt()
    parsed = latch.parse_synthetic_writer_receipt_fixture_json(
        _canonical_json(receipt)
    )
    assert parsed["mutation_count"] == 0


@pytest.mark.parametrize(
    ("mutation_count", "code"),
    [
        (False, "receipt_integer_type_invalid"),
        (True, "receipt_integer_type_invalid"),
        (0.5, "receipt_float_invalid"),
    ],
)
def test_boolean_or_float_mutation_count_is_rejected(
    latch, mutation_count: Any, code: str
) -> None:
    with pytest.raises(latch.OuterExecutionReportLatchError, match=code):
        _proof(
            latch,
            _ambiguous_commit_receipt(mutation_count=mutation_count),
        )


def test_whole_block_CAS_accepts_verified_ambiguous_receipt_proof(latch) -> None:
    proof = _proof(latch, _ambiguous_commit_receipt())
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    outside = _outside(latch, markdown)
    updated = latch.replace_outer_execution_latch_state_block(
        markdown,
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=proof,
    )
    assert latch.parse_outer_execution_latch_state_block(updated) == consumed
    assert _outside(latch, updated) == outside


def test_atomic_ambiguous_receipt_proof_metadata_remains_exact(
    latch, tmp_path: Path
) -> None:
    proof = _proof(latch, _ambiguous_commit_receipt())
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=proof,
    )
    markdown = _document(latch, returned)
    path = tmp_path / "synthetic-report.md"
    path.write_bytes(markdown.encode("utf-8"))
    result = latch.atomic_write_outer_execution_report_state(
        path,
        _sha256(markdown.encode("utf-8")),
        returned,
        consumed,
        receipt_idempotency_cross_binding_proof=proof,
    )
    assert result["status"] == "updated_and_verified"
    assert result["receipt_idempotency_cross_binding_proof_used"] is True
    assert result["writer_receipt_safe_hash"] == proof["writer_receipt_safe_hash"]
    assert result["receipt_cross_binding_proof_safe_hash"] == proof[
        "proof_canonical_hash"
    ]
    assert result["idempotency_cross_binding_verified"] is True


def test_terminal_after_writer_preserves_consumed_after_ambiguous_proof(
    latch,
) -> None:
    returned = latch.transition_outer_execution_latch_state(
        _writer_started(latch), "writer_returned"
    )
    consumed = latch.transition_outer_execution_latch_state(
        returned,
        "implementation_mutating_attempt_consumed_after_verified_writer_receipt",
        receipt_idempotency_cross_binding_proof=_proof(
            latch, _ambiguous_commit_receipt()
        ),
    )
    terminal = latch.transition_outer_execution_latch_state(
        consumed, "terminal_after_writer"
    )
    assert terminal["implementation_mutating_attempt_consumed"] is True
