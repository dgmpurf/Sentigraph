from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.services.metadata_smoke_review_only_staging_boundary import (
    PHASE as SOURCE_PHASE,
    READY_BOUNDARY_STATUS as SOURCE_READY_STATUS,
    SCHEMA as SOURCE_SCHEMA,
)
from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
    APPROVED_TARGET_DIR,
)


SCHEMA = "sentigraph_controlled_row_preview_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_row_preview_summary_v0_1"
PHASE = "8W-7"
APPROVAL_PHRASE = "APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION"
APPROVED_ROW_SOURCE = "evidence_items.jsonl"
APPROVED_ROW_FILE = APPROVED_TARGET_DIR / APPROVED_ROW_SOURCE
READY_STATUS = "row_preview_ready_for_manual_review"
WARN_STATUS = "row_preview_warn_manual_review_required"
HARD_ROW_BOUND = 10
DEFAULT_MAX_PREVIEW_ROWS = 5
TEXT_SNIPPET_MAX_CHARS = 160
REDACTION_POLICY_VERSION = "sentigraph_row_preview_redaction_policy_v0_1"

FORBIDDEN_ROW_FIELDS = {
    "raw_author_id",
    "raw_author_ids",
    "raw_author_identifier",
    "raw_author_identifiers",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "username",
    "user_name",
    "display_name",
    "profile_url",
    "profile_urls",
    "raw_profile_url",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "address",
    "identity",
    "identity_fields",
    "token",
    "tokens",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "password",
    "passwords",
    "api_key",
    "api_keys",
    "secret",
    "secrets",
    "salt",
    "salts",
    "browser_profile",
    "browser_profile_path",
    "absolute_path",
    "package_path",
    "raw_collector_path",
    "raw_comment",
    "raw_comments",
    "generated_response_text",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

BLOCKED_REQUESTED_ACTIONS = {
    "evidence_layer_write",
    "production_case",
    "production_analysis_run",
    "review_queue_runtime",
    "frontend_route",
    "b_end_report",
    "sandbox_public_event",
    "public_url",
    "signed_url",
    "download_package",
    "final_delivery",
    "publish",
    "send",
    "post",
    "execute",
    "auto_execute",
}

SOURCE_FALSE_FIELDS = {
    "row_preview_approved": "row_preview_already_approved_in_source",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "frontend_ready": "source_frontend_ready_true",
    "route_ready": "source_route_ready_true",
    "production_ready": "source_production_ready_true",
    "public_ready": "source_public_ready_true",
    "customer_ready": "source_customer_ready_true",
}


def build_controlled_row_preview(
    source_boundary: dict[str, Any] | None,
    *,
    approval_phrase: str | None,
    max_preview_rows: int = DEFAULT_MAX_PREVIEW_ROWS,
    row_source: str = APPROVED_ROW_SOURCE,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a bounded, redacted, review-only preview from one approved row source."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(approval_phrase))
    blockers.extend(_source_boundary_blockers(source_boundary))
    blockers.extend(_row_source_blockers(row_source))
    blockers.extend(_row_limit_blockers(max_preview_rows))
    blockers.extend(_requested_action_blockers(requested_actions))

    if blockers:
        return _base_output(
            preview_status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            max_preview_rows_requested=max_preview_rows,
            max_preview_rows_applied=0,
            rows_inspected_count=0,
            preview_rows=[],
            parsed_evidence_items_jsonl=False,
            opened_approved_evidence_items_jsonl=False,
        )

    row_file = APPROVED_ROW_FILE
    file_blockers = _approved_row_file_blockers(row_file)
    if file_blockers:
        return _base_output(
            preview_status=_blocked_status(file_blockers),
            created=False,
            blockers=file_blockers,
            max_preview_rows_requested=max_preview_rows,
            max_preview_rows_applied=max_preview_rows,
            rows_inspected_count=0,
            preview_rows=[],
            parsed_evidence_items_jsonl=False,
            opened_approved_evidence_items_jsonl=False,
        )

    preview_rows, rows_inspected_count, row_warnings = _read_preview_rows(
        row_file,
        max_preview_rows=max_preview_rows,
    )
    warnings = ["manual_review_required", "selected_sample_only", *row_warnings]
    status = WARN_STATUS if warnings else READY_STATUS
    return _base_output(
        preview_status=status,
        created=True,
        blockers=[],
        warnings=_dedupe(warnings),
        max_preview_rows_requested=max_preview_rows,
        max_preview_rows_applied=max_preview_rows,
        rows_inspected_count=rows_inspected_count,
        preview_rows=preview_rows,
        parsed_evidence_items_jsonl=True,
        opened_approved_evidence_items_jsonl=True,
    )


create_controlled_row_preview = build_controlled_row_preview


def build_safe_controlled_row_preview_summary(
    source_boundary: dict[str, Any] | None,
    *,
    approval_phrase: str | None,
    max_preview_rows: int = DEFAULT_MAX_PREVIEW_ROWS,
    row_source: str = APPROVED_ROW_SOURCE,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    preview = build_controlled_row_preview(
        source_boundary,
        approval_phrase=approval_phrase,
        max_preview_rows=max_preview_rows,
        row_source=row_source,
        requested_actions=requested_actions,
    )
    return {
        "schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "preview_status": preview["preview_status"],
        "created_local_row_preview": preview["created_local_row_preview"],
        "approved_target_package_name": APPROVED_PACKAGE_NAME,
        "approved_target_package_role": APPROVED_PACKAGE_ROLE,
        "approved_target_case_id_hint": APPROVED_CASE_ID_HINT,
        "row_source": APPROVED_ROW_SOURCE,
        "max_preview_rows_applied": preview["max_preview_rows_applied"],
        "max_preview_rows_hard_bound": HARD_ROW_BOUND,
        "rows_inspected_count": preview["rows_inspected_count"],
        "preview_rows_count": preview["preview_rows_count"],
        "row_limit_enforced": preview["row_limit_enforced"],
        "human_review_required": True,
        "preview_only": True,
        "blockers": list(preview["blockers"]),
        "warnings": list(preview["warnings"]),
        "runtime_side_effects": dict(preview["runtime_side_effects"]),
        "absolute_path_exposed": False,
        "package_path_exposed": False,
    }


def _base_output(
    *,
    preview_status: str,
    created: bool,
    blockers: list[str],
    max_preview_rows_requested: Any,
    max_preview_rows_applied: int,
    rows_inspected_count: int,
    preview_rows: list[dict[str, Any]],
    parsed_evidence_items_jsonl: bool,
    opened_approved_evidence_items_jsonl: bool,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    output = {
        "schema": SCHEMA,
        "phase": PHASE,
        "preview_status": preview_status,
        "created_at": _utc_now(),
        "created_local_row_preview": created,
        "source_boundary_schema": SOURCE_SCHEMA,
        "source_boundary_phase": SOURCE_PHASE,
        "approved_target_package_name": APPROVED_PACKAGE_NAME,
        "approved_target_package_role": APPROVED_PACKAGE_ROLE,
        "approved_target_case_id_hint": APPROVED_CASE_ID_HINT,
        "row_source": APPROVED_ROW_SOURCE,
        "row_source_policy": "single_approved_jsonl_source_only",
        "row_source_path_exposed": False,
        "absolute_path_exposed": False,
        "package_path_exposed": False,
        "max_preview_rows_requested": max_preview_rows_requested,
        "max_preview_rows_applied": max_preview_rows_applied,
        "max_preview_rows_hard_bound": HARD_ROW_BOUND,
        "rows_inspected_count": rows_inspected_count,
        "preview_rows_count": len(preview_rows),
        "row_limit_enforced": True,
        "redaction_policy_version": REDACTION_POLICY_VERSION,
        "warning_count": 1,
        "human_review_required": True,
        "warning_manual_review_preserved": True,
        "preview_only": True,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "evidence_layer_ready": False,
        "route_changed": False,
        "frontend_code_changed": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "evidence_items_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
        "preview_rows": preview_rows,
        "blockers": _dedupe(blockers),
        "warnings": _dedupe(warnings or []),
        "runtime_side_effects": _runtime_side_effects(
            parsed_evidence_items_jsonl=parsed_evidence_items_jsonl,
            opened_approved_evidence_items_jsonl=opened_approved_evidence_items_jsonl,
        ),
    }
    return output


def _runtime_side_effects(
    *,
    parsed_evidence_items_jsonl: bool,
    opened_approved_evidence_items_jsonl: bool,
) -> dict[str, bool]:
    return {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_provider_job": False,
        "ran_collector": False,
        "accessed_private_collector": False,
        "inspected_private_collector_source": False,
        "read_real_exchange_dir": False,
        "fetched_url": False,
        "scraped_page": False,
        "opened_approved_evidence_items_jsonl": opened_approved_evidence_items_jsonl,
        "parsed_evidence_items_jsonl": parsed_evidence_items_jsonl,
        "parsed_evidence_items_csv": False,
        "parsed_source_manifest_jsonl_rows": False,
        "parsed_collection_log_jsonl_rows": False,
        "read_original_package_rows": False,
        "read_private_collector_raw_output": False,
        "emitted_raw_comments": False,
        "emitted_raw_identities": False,
        "emitted_profile_urls": False,
        "wrote_evidence_layer": False,
        "created_evidence_items": False,
        "created_review_queue_items": False,
        "created_production_review_queue_items": False,
        "created_production_case": False,
        "created_production_analysis_run": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "used_report_export_runtime": False,
        "used_download_package_runtime": False,
        "used_public_access_runtime": False,
        "used_external_delivery_runtime": False,
        "used_final_delivery_runtime": False,
        "generated_response_text": False,
        "created_public_route": False,
        "modified_frontend": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _approval_blockers(approval_phrase: str | None) -> list[str]:
    if approval_phrase != APPROVAL_PHRASE:
        return ["blocked_missing_exact_approval"]
    return []


def _source_boundary_blockers(source_boundary: dict[str, Any] | None) -> list[str]:
    if not isinstance(source_boundary, dict):
        return ["source_boundary_missing_or_not_object"]
    blockers: list[str] = []
    expected = {
        "schema": (SOURCE_SCHEMA, "source_boundary_schema_wrong"),
        "phase": (SOURCE_PHASE, "source_boundary_phase_wrong"),
        "boundary_status": (SOURCE_READY_STATUS, "source_boundary_status_wrong"),
        "approved_target_package_name": (APPROVED_PACKAGE_NAME, "source_package_name_mismatch"),
        "approved_target_package_role": (APPROVED_PACKAGE_ROLE, "source_package_role_mismatch"),
        "approved_target_case_id_hint": (APPROVED_CASE_ID_HINT, "source_case_id_hint_mismatch"),
    }
    for field, (expected_value, reason) in expected.items():
        if source_boundary.get(field) != expected_value:
            blockers.append(reason)
    if source_boundary.get("metadata_only") is not True:
        blockers.append("metadata_only_not_true")
    if source_boundary.get("warning_count") != 1:
        blockers.append("warning_count_not_one")
    if source_boundary.get("human_review_required") is not True:
        blockers.append("human_review_required_not_true")
    if source_boundary.get("warning_manual_review_preserved") is not True:
        blockers.append("warning_manual_review_not_preserved")
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if source_boundary.get(field) is True:
            blockers.append(reason)
    runtime_side_effects = source_boundary.get("runtime_side_effects")
    if isinstance(runtime_side_effects, dict):
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")
    return _dedupe(blockers)


def _row_source_blockers(row_source: str) -> list[str]:
    if row_source != APPROVED_ROW_SOURCE:
        return ["blocked_unapproved_row_source"]
    return []


def _row_limit_blockers(max_preview_rows: Any) -> list[str]:
    if isinstance(max_preview_rows, bool) or not isinstance(max_preview_rows, int):
        return ["blocked_requested_row_limit_invalid"]
    if max_preview_rows <= 0:
        return ["blocked_requested_row_limit_not_positive"]
    if max_preview_rows > HARD_ROW_BOUND:
        return ["blocked_requested_row_limit_too_high"]
    return []


def _requested_action_blockers(requested_actions: list[str] | dict[str, Any] | None) -> list[str]:
    blockers: list[str] = []
    if isinstance(requested_actions, list):
        for action in requested_actions:
            if isinstance(action, str) and action in BLOCKED_REQUESTED_ACTIONS:
                blockers.append(f"requested_action_blocked:{action}")
    elif isinstance(requested_actions, dict):
        for action, requested in requested_actions.items():
            if isinstance(action, str) and action in BLOCKED_REQUESTED_ACTIONS and _truthy(requested):
                blockers.append(f"requested_action_blocked:{action}")
    return _dedupe(blockers)


def _approved_row_file_blockers(row_file: Path) -> list[str]:
    blockers: list[str] = []
    if row_file.name != APPROVED_ROW_SOURCE:
        blockers.append("blocked_unapproved_row_source")
    if ".." in row_file.parts:
        blockers.append("blocked_row_source_path_traversal")
    if not row_file.exists() or not row_file.is_file():
        blockers.append("blocked_approved_row_file_missing")
    return _dedupe(blockers)


def _read_preview_rows(
    row_file: Path,
    *,
    max_preview_rows: int,
) -> tuple[list[dict[str, Any]], int, list[str]]:
    preview_rows: list[dict[str, Any]] = []
    warnings: list[str] = []
    inspected = 0
    with row_file.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            if inspected >= HARD_ROW_BOUND:
                break
            inspected += 1
            stripped = raw_line.strip()
            if not stripped:
                continue
            try:
                payload = json.loads(stripped)
            except json.JSONDecodeError:
                warnings.append("row_invalid_json_skipped")
                continue
            if not isinstance(payload, dict):
                warnings.append("row_not_object_skipped")
                continue
            row = _safe_preview_row(payload, row_index=inspected)
            if row is None:
                warnings.append("row_blocked_by_redaction_policy")
                continue
            preview_rows.append(row)
            if len(preview_rows) >= max_preview_rows:
                break
    return preview_rows, inspected, _dedupe(warnings)


def _safe_preview_row(payload: dict[str, Any], *, row_index: int) -> dict[str, Any] | None:
    snippet, redaction_warnings = _first_redacted_snippet(
        payload.get("body_text"),
        payload.get("comment_text"),
        payload.get("text"),
        payload.get("snippet"),
        payload.get("claim_summary"),
        payload.get("title"),
    )
    if snippet is None:
        return None
    evidence_id_hash = _safe_hash(
        payload.get("evidence_id")
        or payload.get("content_id")
        or payload.get("id")
        or f"row:{row_index}"
    )
    return {
        "preview_row_id": f"preview-row-{row_index:03d}",
        "row_index": row_index,
        "evidence_id_hash": evidence_id_hash,
        "evidence_type": _safe_enum(payload.get("evidence_type") or payload.get("source_type")),
        "platform": _safe_enum(payload.get("platform")),
        "created_at_date": _safe_date(payload.get("created_at")),
        "trust_label": _safe_enum(payload.get("trust_label")),
        "verification_status": _safe_enum(payload.get("verification_status")),
        "review_status": _safe_enum(payload.get("review_status")),
        "language": _safe_enum(payload.get("language")),
        "content_visibility": _safe_enum(payload.get("content_visibility")),
        "access_scope": _safe_enum(payload.get("access_scope")),
        "text_snippet_redacted": snippet,
        "redaction_status": "redacted",
        "redaction_warnings": redaction_warnings,
        "row_boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }


def _first_safe_text(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value
    return ""


def _first_redacted_snippet(*values: Any) -> tuple[str | None, list[str]]:
    combined_warnings: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            continue
        snippet, warnings = _redacted_snippet(value)
        combined_warnings.extend(warnings)
        if snippet is not None and snippet.strip():
            return snippet, _dedupe(combined_warnings)
    return _redacted_snippet(_first_safe_text(*values))


def _redacted_snippet(value: str) -> tuple[str | None, list[str]]:
    normalized = " ".join(str(value).split())
    warnings: list[str] = []
    if _looks_like_private_or_dangerous_text(normalized):
        return None, ["blocked_private_or_sensitive_text"]
    patterns = [
        (r"https?://\S+|www\.\S+", "[REDACTED_URL]"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED_EMAIL]"),
        (r"\b(?:\+?\d[\d\s().-]{7,}\d)\b", "[REDACTED_PHONE]"),
        (r"@[A-Za-z0-9_][A-Za-z0-9_.-]{2,}", "[REDACTED_HANDLE]"),
        (r"\b(?:token|cookie|api[_-]?key|password|session)\s*[:=]\s*\S+", "[REDACTED_SECRET]"),
        (r"\b[A-Za-z0-9_-]{32,}\b", "[REDACTED_ID]"),
    ]
    redacted = normalized
    for pattern, replacement in patterns:
        redacted, count = re.subn(pattern, replacement, redacted, flags=re.IGNORECASE)
        if count:
            warnings.append("redacted_sensitive_text")
    return redacted[:TEXT_SNIPPET_MAX_CHARS], _dedupe(warnings)


def _looks_like_private_or_dangerous_text(value: str) -> bool:
    lowered = value.lower()
    blocked_markers = {
        "private_message",
        "private message",
        "doxx",
        "doxxing",
        "minor child",
        "family address",
        "browser profile",
    }
    return any(marker in lowered for marker in blocked_markers)


def _safe_hash(value: Any) -> str:
    text = str(value if value is not None else "unknown")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _safe_enum(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _unsafe_string(stripped):
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", stripped)[:80]


def _safe_date(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", value.strip())
    if not match:
        return None
    return match.group(1)


def _unsafe_string(value: str) -> bool:
    lowered = value.lower()
    if "actual-" in lowered and "should-never-appear" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    if ":\\" in value or ":/" in value:
        return True
    return False


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_unknown"
    first = blockers[0]
    if first.startswith("blocked_"):
        return first
    if first.startswith("requested_action_blocked"):
        return "blocked_requested_side_effect"
    if "package" in first or "case_id" in first:
        return "blocked_target_identity"
    if "source_" in first or "metadata" in first or "warning" in first:
        return "blocked_source_boundary"
    return f"blocked_{first}"


def _truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "requested", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
