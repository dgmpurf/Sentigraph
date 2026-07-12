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
    "sentigraph_outer_execution_report_atomic_update_result_v0_1"
)
ATOMIC_UPDATE_RESULT_VERSION: Final = "0.1"

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
        "terminal_before_payload",
        "terminal_after_payload_before_writer",
        "terminal_after_writer",
    }
)
_LAST_TRANSITIONS: Final = _TRANSITIONS | {"initial_armed"}
_HASH_RE: Final = re.compile(r"^[a-f0-9]{64}$")


class OuterExecutionReportLatchError(ValueError):
    """Bounded state or document failure without document-value disclosure."""


class _DuplicateJsonKey(ValueError):
    pass


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
) -> dict[str, Any]:
    """Apply one allowed monotonic transition to a copied strict state."""

    current = _validate_state(state)
    if not isinstance(transition, str) or transition not in _TRANSITIONS:
        raise OuterExecutionReportLatchError("transition_unknown")
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
    derived = transition_outer_execution_latch_state(expected, transition)
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
) -> dict[str, Any]:
    """Atomically apply one strict state transition to one explicit report."""

    result = _base_atomic_result(next_state)
    temporary_path: Path | None = None
    replaced = False
    try:
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
        }
        if expected_pairs.get(last) != (payload_state, writer_state):
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
        "document_content_exposed": False,
        "physical_path_exposed": False,
    }
