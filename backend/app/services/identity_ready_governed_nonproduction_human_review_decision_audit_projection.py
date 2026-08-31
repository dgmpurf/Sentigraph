from __future__ import annotations

import json
import os
import re
import sqlite3
import stat
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from app.services.identity_ready_governed_nonproduction_human_review_decision_ledger import (
    CANDIDATE_MODE,
    CANDIDATE_SCHEMA,
    DECISION_FIELDS,
    DECISION_SCHEMA,
    DECISION_STATUS,
    DECISION_TYPES,
    DECISION_VERSION,
    IDENTITY_SCHEMA,
    IDENTITY_STATUS,
    IDENTITY_VERSION,
    LEDGER_SCOPE,
    LOGICAL_TARGET_LABEL,
    PRIMARY_TABLE,
    REQUEST_SCHEMA,
    REQUEST_VERSION,
    SERVER_SAMPLE_HANDLE,
    _row_to_decision,
)


RESPONSE_SCHEMA = (
    "sentigraph_internal_alpha_identity_ready_governed_review_"
    "decision_audit_projection_response_v0_1"
)
RESPONSE_VERSION = "0.1"
ROUTE_MODE = (
    "internal_disabled_by_default_read_only_identity_ready_"
    "human_review_decision_audit_projection"
)
HISTORY_RESPONSE_SCHEMA = (
    "sentigraph_internal_alpha_identity_ready_governed_review_"
    "decision_audit_history_response_v0_1"
)
HISTORY_ROUTE_MODE = (
    "internal_disabled_by_default_bounded_read_only_identity_ready_"
    "human_review_decision_audit_history"
)
HISTORY_ERROR_FIELDS = (
    "response_schema",
    "response_version",
    "route_mode",
    "history_status",
)
HISTORY_SUCCESS_FIELDS = HISTORY_ERROR_FIELDS + (
    "requested_limit",
    "returned_count",
    "ordering",
    "decisions",
)
HISTORY_ROW_FIELDS = (
    "decision_id",
    "audit_receipt_reference",
    "sample_handle",
    "decision_type",
    "decision_status",
    "recorded_at",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
)
HISTORY_ORDERING = "recorded_at_desc_decision_id_desc"
HISTORY_MAX_LIMIT = 20
ERROR_FIELDS = (
    "response_schema",
    "response_version",
    "route_mode",
    "readback_status",
)
SUCCESS_FIELDS = ERROR_FIELDS + (
    "decision_id",
    "audit_receipt_reference",
    "sample_handle",
    "decision_type",
    "decision_status",
    "recorded_at",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
)
READBACK_STATUSES = frozenset(
    {
        "decision_audit_ready",
        "audit_target_absent",
        "decision_not_found",
        "audit_schema_inconsistent",
        "decision_integrity_mismatch",
        "sidecar_present_read_prohibited",
        "target_identity_or_metadata_blocked",
        "bounded_read_only_unavailable",
    }
)
HISTORY_STATUSES = frozenset(
    {
        "decision_history_ready",
        "history_limit_invalid",
        "audit_target_absent",
        "audit_schema_inconsistent",
        "decision_integrity_mismatch",
        "sidecar_present_read_prohibited",
        "target_identity_or_metadata_blocked",
        "bounded_read_only_unavailable",
    }
)

_DECISION_ID_PATTERN = re.compile(r"irghrd-[0-9a-f]{32}")
_AUDIT_RECEIPT_PATTERN = re.compile(r"irghrd-receipt-[0-9a-f]{32}")
_LOWER_HEX_64_PATTERN = re.compile(r"[0-9a-f]{64}")
_FILE_ATTRIBUTE_REPARSE_POINT = 0x400
_TABLE_COLUMNS = (
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
    "sample_handle",
    "review_subject_binding_safe_hash",
    "decision_type",
    "decision_canonical_hash",
    "decision_json",
)
_ALLOWED_COLUMNS = frozenset(_TABLE_COLUMNS)
_FALSE_DECISION_FLAGS = (
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "evidence_layer_write_performed",
    "provider_or_b05_called",
    "analysis_triggered",
    "report_triggered",
)


@dataclass(frozen=True)
class _PathMetadata:
    exists: bool
    regular: bool
    directory: bool
    symlink: bool
    reparse: bool


def _bounded_result(readback_status: str) -> dict[str, Any]:
    if readback_status not in READBACK_STATUSES:
        readback_status = "bounded_read_only_unavailable"
    values = {
        "response_schema": RESPONSE_SCHEMA,
        "response_version": RESPONSE_VERSION,
        "route_mode": ROUTE_MODE,
        "readback_status": readback_status,
    }
    return {field: values[field] for field in ERROR_FIELDS}


def _success_result(decision: dict[str, Any]) -> dict[str, Any]:
    values = {
        **_bounded_result("decision_audit_ready"),
        "decision_id": decision["decision_id"],
        "audit_receipt_reference": decision["audit_receipt_reference"],
        "sample_handle": decision["sample_handle"],
        "decision_type": decision["decision_type"],
        "decision_status": decision["decision_status"],
        "recorded_at": decision["recorded_at"],
        "human_review_required": decision["human_review_required"],
        "no_automatic_trust_upgrade": decision["no_automatic_trust_upgrade"],
        "production_object_enabled": decision["production_object_enabled"],
        "review_queue_runtime_enabled": decision["review_queue_runtime_enabled"],
        "evidence_layer_write_performed": decision["evidence_layer_write_performed"],
        "provider_or_b05_called": decision["provider_or_b05_called"],
        "analysis_triggered": decision["analysis_triggered"],
        "report_triggered": decision["report_triggered"],
    }
    return {field: values[field] for field in SUCCESS_FIELDS}


def _history_bounded_result(history_status: str) -> dict[str, Any]:
    if history_status not in HISTORY_STATUSES:
        history_status = "bounded_read_only_unavailable"
    values = {
        "response_schema": HISTORY_RESPONSE_SCHEMA,
        "response_version": RESPONSE_VERSION,
        "route_mode": HISTORY_ROUTE_MODE,
        "history_status": history_status,
    }
    return {field: values[field] for field in HISTORY_ERROR_FIELDS}


def _history_row(decision: dict[str, Any]) -> dict[str, Any]:
    return {field: decision[field] for field in HISTORY_ROW_FIELDS}


def _history_success_result(
    decisions: list[dict[str, Any]],
    *,
    requested_limit: int,
) -> dict[str, Any]:
    values = {
        **_history_bounded_result("decision_history_ready"),
        "requested_limit": requested_limit,
        "returned_count": len(decisions),
        "ordering": HISTORY_ORDERING,
        "decisions": [_history_row(decision) for decision in decisions],
    }
    return {field: values[field] for field in HISTORY_SUCCESS_FIELDS}


def _lexical_absolute(path: str | Path) -> Path:
    if not isinstance(path, (str, Path)):
        raise ValueError("path_type_invalid")
    candidate = Path(path)
    if not candidate.is_absolute():
        raise ValueError("absolute_path_required")
    return Path(os.path.abspath(os.path.normpath(os.fspath(candidate))))


def _is_reparse_stat(value: Any) -> bool:
    return bool(
        getattr(value, "st_file_attributes", 0) & _FILE_ATTRIBUTE_REPARSE_POINT
    )


def _path_metadata(path: Path) -> _PathMetadata:
    if not os.path.lexists(path):
        return _PathMetadata(False, False, False, False, False)
    value = os.lstat(path)
    return _PathMetadata(
        exists=True,
        regular=stat.S_ISREG(value.st_mode),
        directory=stat.S_ISDIR(value.st_mode),
        symlink=stat.S_ISLNK(value.st_mode),
        reparse=_is_reparse_stat(value),
    )


def _stable_file_signature(path: Path) -> tuple[int, int, int, int]:
    value = os.lstat(path)
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)


def _probe_sidecars(database_path: Path) -> tuple[bool, bool, bool]:
    return tuple(
        os.path.lexists(Path(f"{database_path}{suffix}"))
        for suffix in ("-journal", "-wal", "-shm")
    )


def _authorizer_callback(
    action: int,
    arg1: str | None,
    arg2: str | None,
    database_name: str | None,
    _trigger_name: str | None,
) -> int:
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_READ:
        if (
            arg1 == PRIMARY_TABLE
            and arg2 in _ALLOWED_COLUMNS
            and database_name == "main"
        ):
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY
    if action == sqlite3.SQLITE_FUNCTION and (arg2 or arg1) == "json_extract":
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY


def _decision_semantics_are_valid(
    decision: dict[str, Any],
    *,
    requested_decision_id: str,
    stored_json: str,
) -> bool:
    try:
        datetime.strptime(decision["recorded_at"], "%Y-%m-%dT%H:%M:%SZ")
        canonical_json = json.dumps(
            decision,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
        expected_suffix = requested_decision_id.removeprefix("irghrd-")
        return bool(
            tuple(decision) == DECISION_FIELDS
            and decision["decision_schema"] == DECISION_SCHEMA
            and decision["decision_version"] == DECISION_VERSION
            and decision["decision_id"] == requested_decision_id
            and decision["idempotency_key"][:32] == expected_suffix
            and _LOWER_HEX_64_PATTERN.fullmatch(decision["idempotency_key"])
            and decision["audit_receipt_reference"]
            == f"irghrd-receipt-{expected_suffix}"
            and _AUDIT_RECEIPT_PATTERN.fullmatch(
                decision["audit_receipt_reference"]
            )
            and decision["ledger_scope"] == LEDGER_SCOPE
            and decision["decision_status"] == DECISION_STATUS
            and decision["request_schema"] == REQUEST_SCHEMA
            and decision["request_version"] == REQUEST_VERSION
            and decision["candidate_schema"] == CANDIDATE_SCHEMA
            and decision["candidate_mode"] == CANDIDATE_MODE
            and decision["identity_schema"] == IDENTITY_SCHEMA
            and decision["identity_version"] == IDENTITY_VERSION
            and decision["identity_status"] == IDENTITY_STATUS
            and decision["sample_handle"] == SERVER_SAMPLE_HANDLE
            and _LOWER_HEX_64_PATTERN.fullmatch(
                decision["review_subject_binding_safe_hash"]
            )
            and decision["decision_type"] in DECISION_TYPES
            and decision["server_binding_context_mode"]
            == "process_local_configuration_exact_match"
            and decision["human_review_required"] is True
            and decision["no_automatic_trust_upgrade"] is True
            and all(decision[field] is False for field in _FALSE_DECISION_FLAGS)
            and canonical_json == stored_json
        )
    except (KeyError, TypeError, ValueError):
        return False


def _indexed_columns_match_decision(
    row: sqlite3.Row,
    decision: dict[str, Any],
) -> bool:
    return all(
        row[field] == decision[field]
        for field in _TABLE_COLUMNS
        if field != "decision_json"
    )


def project_identity_ready_governed_nonproduction_human_review_decision_audit(
    *,
    authorized_root_path: str | Path,
    database_path: str | Path,
    target_logical_label: str,
    decision_id: str,
) -> dict[str, Any]:
    """Project one exact identity-ready decision through a bounded read-only path."""

    if (
        type(decision_id) is not str
        or _DECISION_ID_PATTERN.fullmatch(decision_id) is None
    ):
        return _bounded_result("decision_not_found")

    try:
        root = _lexical_absolute(authorized_root_path)
        database = _lexical_absolute(database_path)
        if target_logical_label != LOGICAL_TARGET_LABEL:
            raise ValueError("logical_target_mismatch")
        expected_database = root.joinpath(*target_logical_label.split("/"))
        exact_match = os.path.normcase(os.fspath(database)) == os.path.normcase(
            os.fspath(expected_database)
        )
        inside_root = os.path.commonpath([root, database]) == os.fspath(root)
        if not exact_match or not inside_root:
            raise ValueError("target_identity_mismatch")
    except Exception:
        return _bounded_result("target_identity_or_metadata_blocked")

    try:
        root_metadata = _path_metadata(root)
        if not root_metadata.exists:
            return _bounded_result("audit_target_absent")
        if not (
            root_metadata.directory
            and not root_metadata.symlink
            and not root_metadata.reparse
        ):
            return _bounded_result("target_identity_or_metadata_blocked")

        current = root
        for component in target_logical_label.split("/")[:-1]:
            current = current / component
            metadata = _path_metadata(current)
            if not metadata.exists:
                return _bounded_result("audit_target_absent")
            if not (
                metadata.directory
                and not metadata.symlink
                and not metadata.reparse
            ):
                return _bounded_result("target_identity_or_metadata_blocked")

        target_metadata = _path_metadata(database)
        if not target_metadata.exists:
            return _bounded_result("audit_target_absent")
        if not (
            target_metadata.regular
            and not target_metadata.directory
            and not target_metadata.symlink
            and not target_metadata.reparse
        ):
            return _bounded_result("target_identity_or_metadata_blocked")
        signature_before = _stable_file_signature(database)
    except Exception:
        return _bounded_result("target_identity_or_metadata_blocked")

    try:
        if any(_probe_sidecars(database)):
            return _bounded_result("sidecar_present_read_prohibited")
    except Exception:
        return _bounded_result("bounded_read_only_unavailable")

    connection: sqlite3.Connection | None = None
    result: dict[str, Any]
    try:
        connection = sqlite3.connect(
            f"{database.as_uri()}?mode=ro",
            uri=True,
            timeout=5.0,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only = ON")
        query_only_row = connection.execute("PRAGMA query_only").fetchone()
        if query_only_row is None or int(query_only_row[0]) != 1:
            raise sqlite3.OperationalError("query_only_not_enabled")
        connection.set_authorizer(_authorizer_callback)
    except Exception:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
        result = _bounded_result("bounded_read_only_unavailable")
    else:
        try:
            schema_cursor = connection.execute(f"SELECT * FROM {PRIMARY_TABLE} LIMIT 0")
            actual_columns = tuple(
                item[0] for item in (schema_cursor.description or ())
            )
            if actual_columns != _TABLE_COLUMNS:
                result = _bounded_result("audit_schema_inconsistent")
            else:
                selected_columns = ", ".join(_TABLE_COLUMNS)
                rows = connection.execute(
                    f"SELECT {selected_columns} FROM {PRIMARY_TABLE} "
                    "WHERE decision_id = ? LIMIT 2",
                    (decision_id,),
                ).fetchall()
                if not rows:
                    result = _bounded_result("decision_not_found")
                elif len(rows) != 1:
                    result = _bounded_result("audit_schema_inconsistent")
                else:
                    row = rows[0]
                    try:
                        decision = _row_to_decision((row["decision_json"],))
                    except Exception:
                        result = _bounded_result("decision_integrity_mismatch")
                    else:
                        if not _indexed_columns_match_decision(row, decision) or not (
                            _decision_semantics_are_valid(
                                decision,
                                requested_decision_id=decision_id,
                                stored_json=row["decision_json"],
                            )
                        ):
                            result = _bounded_result("decision_integrity_mismatch")
                        else:
                            result = _success_result(decision)
        except sqlite3.DatabaseError:
            result = _bounded_result("audit_schema_inconsistent")
        except Exception:
            result = _bounded_result("bounded_read_only_unavailable")
        finally:
            try:
                connection.close()
            except Exception:
                result = _bounded_result("bounded_read_only_unavailable")

    try:
        if any(_probe_sidecars(database)):
            return _bounded_result("sidecar_present_read_prohibited")
        target_metadata_after = _path_metadata(database)
        if not (
            target_metadata_after.exists
            and target_metadata_after.regular
            and not target_metadata_after.symlink
            and not target_metadata_after.reparse
            and _stable_file_signature(database) == signature_before
        ):
            return _bounded_result("target_identity_or_metadata_blocked")
    except Exception:
        return _bounded_result("bounded_read_only_unavailable")
    return result


def list_identity_ready_governed_nonproduction_human_review_decision_audit_projections(
    *,
    authorized_root_path: str | Path,
    database_path: str | Path,
    target_logical_label: str,
    limit: int = HISTORY_MAX_LIMIT,
) -> dict[str, Any]:
    """List a bounded, deterministic safe history from the identity-ready ledger."""

    if type(limit) is not int or not 1 <= limit <= HISTORY_MAX_LIMIT:
        return _history_bounded_result("history_limit_invalid")

    try:
        root = _lexical_absolute(authorized_root_path)
        database = _lexical_absolute(database_path)
        if target_logical_label != LOGICAL_TARGET_LABEL:
            raise ValueError("logical_target_mismatch")
        expected_database = root.joinpath(*target_logical_label.split("/"))
        exact_match = os.path.normcase(os.fspath(database)) == os.path.normcase(
            os.fspath(expected_database)
        )
        inside_root = os.path.commonpath([root, database]) == os.fspath(root)
        if not exact_match or not inside_root:
            raise ValueError("target_identity_mismatch")
    except Exception:
        return _history_bounded_result("target_identity_or_metadata_blocked")

    try:
        root_metadata = _path_metadata(root)
        if not root_metadata.exists:
            return _history_bounded_result("audit_target_absent")
        if not (
            root_metadata.directory
            and not root_metadata.symlink
            and not root_metadata.reparse
        ):
            return _history_bounded_result("target_identity_or_metadata_blocked")

        current = root
        for component in target_logical_label.split("/")[:-1]:
            current = current / component
            metadata = _path_metadata(current)
            if not metadata.exists:
                return _history_bounded_result("audit_target_absent")
            if not (
                metadata.directory
                and not metadata.symlink
                and not metadata.reparse
            ):
                return _history_bounded_result("target_identity_or_metadata_blocked")

        target_metadata = _path_metadata(database)
        if not target_metadata.exists:
            return _history_bounded_result("audit_target_absent")
        if not (
            target_metadata.regular
            and not target_metadata.directory
            and not target_metadata.symlink
            and not target_metadata.reparse
        ):
            return _history_bounded_result("target_identity_or_metadata_blocked")
        signature_before = _stable_file_signature(database)
    except Exception:
        return _history_bounded_result("target_identity_or_metadata_blocked")

    try:
        if any(_probe_sidecars(database)):
            return _history_bounded_result("sidecar_present_read_prohibited")
    except Exception:
        return _history_bounded_result("bounded_read_only_unavailable")

    connection: sqlite3.Connection | None = None
    result: dict[str, Any]
    try:
        connection = sqlite3.connect(
            f"{database.as_uri()}?mode=ro",
            uri=True,
            timeout=5.0,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA query_only = ON")
        query_only_row = connection.execute("PRAGMA query_only").fetchone()
        if query_only_row is None or int(query_only_row[0]) != 1:
            raise sqlite3.OperationalError("query_only_not_enabled")
        connection.set_authorizer(_authorizer_callback)
    except Exception:
        if connection is not None:
            try:
                connection.close()
            except Exception:
                pass
        result = _history_bounded_result("bounded_read_only_unavailable")
    else:
        try:
            schema_cursor = connection.execute(f"SELECT * FROM {PRIMARY_TABLE} LIMIT 0")
            actual_columns = tuple(
                item[0] for item in (schema_cursor.description or ())
            )
            if actual_columns != _TABLE_COLUMNS:
                result = _history_bounded_result("audit_schema_inconsistent")
            else:
                selected_columns = ", ".join(_TABLE_COLUMNS)
                rows = connection.execute(
                    f"SELECT {selected_columns} FROM {PRIMARY_TABLE} "
                    "ORDER BY json_extract(decision_json, '$.recorded_at') DESC, "
                    "decision_id DESC LIMIT ?",
                    (limit,),
                ).fetchall()
                decisions: list[dict[str, Any]] = []
                for row in rows:
                    try:
                        decision = _row_to_decision((row["decision_json"],))
                    except Exception:
                        result = _history_bounded_result(
                            "decision_integrity_mismatch"
                        )
                        break
                    if not _indexed_columns_match_decision(row, decision) or not (
                        _decision_semantics_are_valid(
                            decision,
                            requested_decision_id=row["decision_id"],
                            stored_json=row["decision_json"],
                        )
                    ):
                        result = _history_bounded_result(
                            "decision_integrity_mismatch"
                        )
                        break
                    decisions.append(decision)
                else:
                    result = _history_success_result(
                        decisions,
                        requested_limit=limit,
                    )
        except sqlite3.DatabaseError:
            result = _history_bounded_result("audit_schema_inconsistent")
        except Exception:
            result = _history_bounded_result("bounded_read_only_unavailable")
        finally:
            try:
                connection.close()
            except Exception:
                result = _history_bounded_result("bounded_read_only_unavailable")

    try:
        if any(_probe_sidecars(database)):
            return _history_bounded_result("sidecar_present_read_prohibited")
        target_metadata_after = _path_metadata(database)
        if not (
            target_metadata_after.exists
            and target_metadata_after.regular
            and not target_metadata_after.symlink
            and not target_metadata_after.reparse
            and _stable_file_signature(database) == signature_before
        ):
            return _history_bounded_result("target_identity_or_metadata_blocked")
    except Exception:
        return _history_bounded_result("bounded_read_only_unavailable")
    return result
