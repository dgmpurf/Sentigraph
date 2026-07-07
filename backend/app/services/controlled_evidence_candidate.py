from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


CANDIDATE_SET_SCHEMA = "sentigraph_controlled_evidence_candidate_set_v0_1"
CANDIDATE_SCHEMA = "sentigraph_controlled_evidence_candidate_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_evidence_candidate_summary_v0_1"
SOURCE_SCHEMA = "sentigraph_controlled_row_preview_v0_1"
PHASE = "8W-10"
SOURCE_PHASE = "8W-7"
APPROVAL_PHRASE = "APPROVE_8W_10_CONTROLLED_EVIDENCE_CANDIDATE_IMPLEMENTATION"
SOURCE_WARN_STATUS = "row_preview_warn_manual_review_required"
READY_STATUS = "evidence_candidate_set_ready_for_manual_review"
WARN_STATUS = "evidence_candidate_set_warn_manual_review_required"
HARD_CANDIDATE_BOUND = 10

ALLOWED_ROW_SOURCE = "evidence_items.jsonl"
ALLOWED_ROW_POLICY = "single_approved_jsonl_source_only"
CANDIDATE_MODE = "backend_only_local_preview_derived_evidence_candidate"

REQUIRED_PREVIEW_ROW_FIELDS = [
    "evidence_id_hash",
    "preview_row_id",
    "row_index",
    "text_snippet_redacted",
]

OPTIONAL_SAFE_PREVIEW_ROW_FIELDS = [
    "evidence_type",
    "platform",
    "created_at_date",
    "trust_label",
    "verification_status",
    "review_status",
    "language",
    "content_visibility",
    "access_scope",
    "redaction_status",
]

FORBIDDEN_PREVIEW_ROW_FIELDS = {
    "raw_author_id",
    "raw_author_ids",
    "raw_author_identifier",
    "raw_author_identifiers",
    "author_id",
    "author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_name",
    "author_names",
    "username",
    "user_name",
    "display_name",
    "profile_url",
    "profile_urls",
    "raw_profile_url",
    "raw_comment",
    "raw_comments",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "address",
    "identity",
    "identity_fields",
    "cookie",
    "cookies",
    "token",
    "tokens",
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

REQUESTED_ACTIONS_BLOCKED = {
    "evidence_layer_write",
    "review_queue_runtime",
    "production_case",
    "production_analysis_run",
    "frontend_route",
    "route_api",
    "b_end_report",
    "sandbox_public_event",
    "real_api",
    "real_llm",
    "provider_job",
    "collector_job",
    "publish",
    "send",
    "post",
    "execute",
    "auto_execute",
}

TOP_LEVEL_FALSE_FIELDS = {
    "absolute_path_exposed": "source_absolute_path_exposed",
    "package_path_exposed": "source_package_path_exposed",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "evidence_items_created": "source_evidence_items_created_true",
    "review_queue_item_created": "source_review_queue_item_created_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "frontend_ready": "source_frontend_ready_true",
    "route_ready": "source_route_ready_true",
    "production_ready": "source_production_ready_true",
    "public_ready": "source_public_ready_true",
    "customer_ready": "source_customer_ready_true",
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_generated": "source_sandbox_public_event_generated_true",
    "generated_response_text": "source_generated_response_text_true",
    "public_route_created": "source_public_route_created_true",
    "download_package_runtime_used": "source_download_package_runtime_used_true",
    "public_access_runtime_used": "source_public_access_runtime_used_true",
    "external_delivery_runtime_used": "source_external_delivery_runtime_used_true",
    "final_delivery_runtime_used": "source_final_delivery_runtime_used_true",
}

ALLOWED_TRUE_SOURCE_RUNTIME_FLAGS = {
    "opened_approved_evidence_items_jsonl",
    "parsed_evidence_items_jsonl",
}

RUNTIME_SIDE_EFFECT_FLAGS = [
    "called_real_api",
    "called_real_llm",
    "ran_provider_job",
    "ran_collector",
    "fetched_url",
    "scraped_page",
    "accessed_private_collector",
    "inspected_private_collector_source",
    "read_real_exchange_dir",
    "parsed_evidence_items_jsonl_again",
    "parsed_evidence_items_csv",
    "parsed_source_manifest_jsonl_rows",
    "parsed_collection_log_jsonl_rows",
    "read_original_package_rows",
    "read_private_collector_raw_output",
    "emitted_raw_comments",
    "emitted_raw_identities",
    "emitted_profile_urls",
    "wrote_evidence_layer",
    "created_evidence_items",
    "created_review_queue_items",
    "created_production_review_queue_items",
    "created_production_case",
    "created_production_analysis_run",
    "generated_b_end_report_runtime",
    "generated_sandbox_runtime",
    "generated_public_event_runtime",
    "used_report_export_runtime",
    "used_download_package_runtime",
    "used_public_access_runtime",
    "used_external_delivery_runtime",
    "used_final_delivery_runtime",
    "generated_response_text",
    "created_public_route",
    "modified_frontend",
    "published_or_sent",
    "auto_executed",
]


def build_controlled_evidence_candidate_set(
    controlled_row_preview: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create local, redacted, human-review-only candidate-shaped objects from preview rows."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))

    source_rows = _safe_source_rows(controlled_row_preview)
    source_preview_rows_count = _source_preview_rows_count(controlled_row_preview, source_rows)
    effective_limit = source_preview_rows_count if candidate_limit is None else candidate_limit

    blockers.extend(_candidate_limit_blockers(effective_limit, source_preview_rows_count))
    blockers.extend(_source_preview_blockers(controlled_row_preview, source_rows))

    candidates: list[dict[str, Any]] = []
    if not blockers:
        candidate_rows, row_blockers = _build_candidates(source_rows[:effective_limit])
        blockers.extend(row_blockers)
        candidates = candidate_rows if not blockers else []

    if blockers:
        return _base_output(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            candidates=[],
            source_preview=controlled_row_preview,
            source_preview_rows_count=source_preview_rows_count,
        )

    status = WARN_STATUS if _source_warning_count(controlled_row_preview) else READY_STATUS
    return _base_output(
        status=status,
        created=True,
        blockers=[],
        warnings=_candidate_warnings(controlled_row_preview),
        candidates=candidates,
        source_preview=controlled_row_preview,
        source_preview_rows_count=source_preview_rows_count,
    )


create_controlled_evidence_candidate_set = build_controlled_evidence_candidate_set


def build_safe_controlled_evidence_candidate_summary(
    controlled_row_preview: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate_set = build_controlled_evidence_candidate_set(
        controlled_row_preview,
        exact_approval_phrase=exact_approval_phrase,
        candidate_limit=candidate_limit,
        requested_actions=requested_actions,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "candidate_set_status": candidate_set["candidate_set_status"],
        "candidate_count": candidate_set["candidate_count"],
        "source_preview_rows_count": candidate_set["source_preview_rows_count"],
        "warning_count": candidate_set["warning_count"],
        "human_review_required": candidate_set["human_review_required"],
        "preview_only": candidate_set["preview_only"],
        "evidence_items_created": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "blockers": list(candidate_set["blockers"]),
        "warnings": list(candidate_set["warnings"]),
        "runtime_side_effects": dict(candidate_set["runtime_side_effects"]),
    }


def _base_output(
    *,
    status: str,
    created: bool,
    blockers: list[str],
    candidates: list[dict[str, Any]],
    source_preview: dict[str, Any] | None,
    source_preview_rows_count: int,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "phase": PHASE,
        "candidate_set_status": status,
        "created_at": _utc_now(),
        "input_source_kind": "controlled_row_preview",
        "source_preview_schema": _safe_source_value(source_preview, "schema"),
        "source_preview_phase": _safe_source_value(source_preview, "phase"),
        "source_preview_status": _safe_source_value(source_preview, "preview_status"),
        "candidate_mode": CANDIDATE_MODE,
        "candidate_count": len(candidates),
        "source_preview_rows_count": source_preview_rows_count,
        "warning_count": _source_warning_count(source_preview),
        "human_review_required": True,
        "preview_only": True,
        "evidence_candidate_implementation_approved": created,
        "evidence_candidate_created": created,
        "evidence_items_created": False,
        "evidence_layer_write": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "candidates": candidates,
        "blockers": _dedupe(blockers),
        "warnings": _dedupe(warnings or []),
        "runtime_side_effects": _runtime_side_effects(),
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_missing_exact_approval"]
    return []


def _source_preview_blockers(source_preview: dict[str, Any] | None, source_rows: list[dict[str, Any]]) -> list[str]:
    if not isinstance(source_preview, dict):
        return ["source_preview_missing_or_not_object"]

    blockers: list[str] = []
    expected = {
        "schema": (SOURCE_SCHEMA, "source_preview_schema_wrong"),
        "phase": (SOURCE_PHASE, "source_preview_phase_wrong"),
        "preview_status": (SOURCE_WARN_STATUS, "source_preview_status_not_warn_manual_review"),
        "row_source": (ALLOWED_ROW_SOURCE, "source_row_source_not_approved_jsonl"),
        "row_source_policy": (ALLOWED_ROW_POLICY, "source_row_policy_wrong"),
    }
    for field, (expected_value, reason) in expected.items():
        if source_preview.get(field) != expected_value:
            blockers.append(reason)

    true_fields = {
        "created_local_row_preview": "source_preview_not_created",
        "preview_only": "source_preview_only_not_true",
        "human_review_required": "source_human_review_required_not_true",
        "row_limit_enforced": "source_row_limit_not_enforced",
    }
    for field, reason in true_fields.items():
        if source_preview.get(field) is not True:
            blockers.append(reason)

    if source_preview.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")

    preview_rows_count = source_preview.get("preview_rows_count")
    rows_inspected_count = source_preview.get("rows_inspected_count")
    if not isinstance(preview_rows_count, int) or isinstance(preview_rows_count, bool):
        blockers.append("source_preview_rows_count_missing_or_invalid")
    elif preview_rows_count != len(source_rows):
        blockers.append("source_preview_rows_count_inconsistent")
    elif preview_rows_count < 1:
        blockers.append("source_preview_rows_missing")
    elif preview_rows_count > HARD_CANDIDATE_BOUND:
        blockers.append("source_preview_rows_count_too_high")

    if not isinstance(rows_inspected_count, int) or isinstance(rows_inspected_count, bool):
        blockers.append("source_rows_inspected_count_missing_or_invalid")
    elif isinstance(preview_rows_count, int) and not isinstance(preview_rows_count, bool):
        if rows_inspected_count < preview_rows_count:
            blockers.append("source_rows_inspected_less_than_preview_rows")
        if rows_inspected_count > HARD_CANDIDATE_BOUND:
            blockers.append("source_rows_inspected_count_too_high")

    for field, reason in TOP_LEVEL_FALSE_FIELDS.items():
        if source_preview.get(field) is True:
            blockers.append(reason)

    runtime_side_effects = source_preview.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("source_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if flag in ALLOWED_TRUE_SOURCE_RUNTIME_FLAGS:
                continue
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")

    return _dedupe(blockers)


def _candidate_limit_blockers(candidate_limit: Any, source_preview_rows_count: int) -> list[str]:
    if isinstance(candidate_limit, bool) or not isinstance(candidate_limit, int):
        return ["blocked_candidate_limit_invalid"]
    if candidate_limit <= 0:
        return ["blocked_candidate_limit_not_positive"]
    blockers: list[str] = []
    if candidate_limit > HARD_CANDIDATE_BOUND:
        blockers.append("blocked_candidate_limit_too_high")
    if source_preview_rows_count >= 0 and candidate_limit > source_preview_rows_count:
        blockers.append("blocked_candidate_limit_exceeds_source_preview_rows")
    return blockers


def _requested_action_blockers(requested_actions: list[str] | dict[str, Any] | None) -> list[str]:
    blockers: list[str] = []
    if isinstance(requested_actions, list):
        for action in requested_actions:
            if isinstance(action, str) and action in REQUESTED_ACTIONS_BLOCKED:
                blockers.append(f"requested_action_blocked:{action}")
    elif isinstance(requested_actions, dict):
        for action, requested in requested_actions.items():
            if isinstance(action, str) and action in REQUESTED_ACTIONS_BLOCKED and _truthy(requested):
                blockers.append(f"requested_action_blocked:{action}")
    return _dedupe(blockers)


def _build_candidates(source_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    candidates: list[dict[str, Any]] = []
    blockers: list[str] = []
    for index, source_row in enumerate(source_rows, start=1):
        row_blockers = _preview_row_blockers(source_row)
        if row_blockers:
            blockers.extend(row_blockers)
            continue
        candidates.append(_candidate_from_preview_row(source_row, index=index))
    return candidates, _dedupe(blockers)


def _preview_row_blockers(source_row: dict[str, Any]) -> list[str]:
    if not isinstance(source_row, dict):
        return ["candidate_row_not_object"]
    blockers: list[str] = []
    for field in source_row:
        if field in FORBIDDEN_PREVIEW_ROW_FIELDS:
            blockers.append(f"forbidden_preview_row_field:{field}")
    for field in REQUIRED_PREVIEW_ROW_FIELDS:
        value = source_row.get(field)
        if value is None or value == "":
            blockers.append(f"candidate_row_missing_required_field:{field}")
    for field in [*REQUIRED_PREVIEW_ROW_FIELDS, *OPTIONAL_SAFE_PREVIEW_ROW_FIELDS, "redaction_warnings"]:
        value = source_row.get(field)
        if _contains_forbidden_value(value):
            blockers.append(f"candidate_row_forbidden_value:{field}")
    return _dedupe(blockers)


def _candidate_from_preview_row(source_row: dict[str, Any], *, index: int) -> dict[str, Any]:
    preview_row_id = _safe_text(source_row.get("preview_row_id")) or f"preview-row-{index:03d}"
    redaction_warnings = source_row.get("redaction_warnings")
    return {
        "candidate_schema": CANDIDATE_SCHEMA,
        "candidate_id": f"candidate-{index:03d}-{_safe_token(source_row.get('evidence_id_hash'))}",
        "source_preview_row_id": preview_row_id,
        "source_row_index": _safe_int(source_row.get("row_index")),
        "source_preview_schema": SOURCE_SCHEMA,
        "evidence_id_hash": _safe_token(source_row.get("evidence_id_hash")),
        "evidence_type": _safe_label(source_row.get("evidence_type")),
        "platform": _safe_label(source_row.get("platform")),
        "coarse_created_at": _safe_date(source_row.get("created_at_date")),
        "trust_label": _safe_label(source_row.get("trust_label")),
        "verification_status": _safe_label(source_row.get("verification_status")),
        "review_status": _safe_label(source_row.get("review_status")),
        "language": _safe_label(source_row.get("language")),
        "content_visibility": _safe_label(source_row.get("content_visibility")),
        "access_scope": _safe_label(source_row.get("access_scope")),
        "text_snippet_redacted": _safe_snippet(source_row.get("text_snippet_redacted")),
        "redaction_status": _safe_label(source_row.get("redaction_status")) or "redacted",
        "redaction_warnings": _safe_string_list(redaction_warnings),
        "warning_labels": ["manual_review_required", "selected_sample_only"],
        "human_review_required": True,
        "boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "not_evidence_item": True,
            "no_evidence_layer_write": True,
            "no_review_queue_runtime": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }


def _candidate_warnings(source_preview: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_preview, dict):
        source_warnings = source_preview.get("warnings")
        if isinstance(source_warnings, list):
            warnings.extend(item for item in source_warnings if isinstance(item, str))
    return _dedupe(warnings)


def _safe_source_rows(source_preview: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_preview, dict):
        return []
    rows = source_preview.get("preview_rows")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, dict)]


def _source_preview_rows_count(source_preview: dict[str, Any] | None, source_rows: list[dict[str, Any]]) -> int:
    if isinstance(source_preview, dict):
        count = source_preview.get("preview_rows_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return len(source_rows)


def _source_warning_count(source_preview: dict[str, Any] | None) -> int:
    if isinstance(source_preview, dict):
        warning_count = source_preview.get("warning_count")
        if isinstance(warning_count, int) and not isinstance(warning_count, bool):
            return max(warning_count, 0)
    return 0


def _safe_source_value(source_preview: dict[str, Any] | None, field: str) -> str | None:
    if not isinstance(source_preview, dict):
        return None
    return _safe_label(source_preview.get(field))


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_invalid_source_preview"
    first = blockers[0]
    if first == "blocked_missing_exact_approval":
        return first
    if first.startswith("requested_action_blocked"):
        return "blocked_source_boundary_violation"
    if first.startswith("blocked_candidate_limit"):
        return "blocked_candidate_limit_violation"
    if first.startswith("forbidden_preview_row_field") or first.startswith("candidate_row_forbidden_value"):
        return "blocked_forbidden_field_detected"
    if first.startswith("candidate_row") or first.startswith("source_preview") or first.startswith("source_rows"):
        return "blocked_invalid_source_preview"
    return "blocked_source_boundary_violation"


def _contains_forbidden_value(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_value(nested) for nested in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_value(item) for item in value)
    if not isinstance(value, str):
        return False
    return _looks_forbidden(value)


def _looks_forbidden(value: str) -> bool:
    lowered = value.lower()
    if "actual-" in lowered and "should-never-appear" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if ":\\" in value or ":/" in value:
        return True
    if "donglu_sunjihai_youth_football/" in value or "donglu_sunjihai_youth_football\\" in value:
        return True
    return False


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_forbidden(stripped):
        return None
    return stripped


def _safe_token(value: Any) -> str:
    text = _safe_text(value)
    if text is None:
        return "unknown"
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:80]


def _safe_label(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:80]


def _safe_snippet(value: Any) -> str:
    text = _safe_text(value)
    if text is None:
        return ""
    return text[:160]


def _safe_date(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", text)
    if not match:
        return None
    return match.group(1)


def _safe_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe: list[str] = []
    for item in value[:20]:
        text = _safe_label(item)
        if text is not None:
            safe.append(text)
    return safe


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
