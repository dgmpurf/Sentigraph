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


@pytest.fixture
def latch():
    return importlib.import_module(MODULE_NAME)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))


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
