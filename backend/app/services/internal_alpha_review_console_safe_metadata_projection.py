from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


APPROVAL_PHRASE = "APPROVE_8Z_20_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_METADATA_PROJECTION_HELPER_SMOKE"
PHASE = "8Z-20"
PROJECTION_SCHEMA = "sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1"
SUMMARY_SCHEMA = "sentigraph_internal_alpha_review_console_safe_metadata_projection_summary_v0_1"
SOURCE_SCHEMA = "sentigraph_internal_alpha_no_write_governance_chain_summary_v0_1"
PROJECTION_MODE = "backend_only_local_safe_metadata_projection"
SOURCE_CHAIN_BOUNDARY = "evidence_layer_write_candidate_boundary"
READY_STATUS = "safe_metadata_projection_ready_for_internal_alpha_review"

REQUIRED_SAFE_ID_FIELDS = [
    "request_id",
    "provider_result_id",
    "package_reference",
    "stage_id",
    "stage_schema",
    "stage_status",
    "stage_mode",
    "candidate_id",
    "boundary_id",
]

FALSE_SOURCE_FLAGS = {
    "actual_evidence_layer_write_used": "source_actual_evidence_layer_write_used_true",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "persisted_evidence_layer_record_created": "source_persisted_evidence_layer_record_created_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "production_analysis_result_authorized": "source_production_analysis_result_authorized_true",
    "production_analysis_result_created": "source_production_analysis_result_created_true",
    "source11_runtime_called": "source_source11_runtime_called_true",
    "finalsummaryreport_runtime_called": "source_finalsummaryreport_runtime_called_true",
    "public_delivery_created": "source_public_delivery_created_true",
    "export_download_public_delivery_created": "source_export_download_public_delivery_created_true",
    "collector_job_run": "source_collector_job_run_true",
    "provider_job_run": "source_provider_job_run_true",
    "real_exchange_dir_read": "source_real_exchange_dir_read_true",
    "real_package_dir_read": "source_real_package_dir_read_true",
    "production_package_rows_parsed": "source_production_package_rows_parsed_true",
    "raw_rows_exposed": "source_raw_rows_exposed_true",
    "raw_comments_exposed": "source_raw_comments_exposed_true",
    "raw_identities_exposed": "source_raw_identities_exposed_true",
    "secrets_read": "source_secrets_read_true",
    "route_changed": "source_route_changed_true",
    "api_route_added": "source_api_route_added_true",
    "frontend_changed": "source_frontend_changed_true",
    "runtime_changed": "source_runtime_changed_true",
}

READINESS_TRUE_FLAGS = {
    "route_ready": "source_route_ready_true",
    "frontend_ready": "source_frontend_ready_true",
    "runtime_ready": "source_runtime_ready_true",
    "public_ready": "source_public_ready_true",
    "production_ready": "source_production_ready_true",
    "actual_write_enabled": "source_actual_write_enabled_true",
    "production_object_enabled": "source_production_object_enabled_true",
    "review_queue_runtime_enabled": "source_review_queue_runtime_enabled_true",
    "source11_runtime_enabled": "source_source11_runtime_enabled_true",
    "finalsummaryreport_runtime_enabled": "source_finalsummaryreport_runtime_enabled_true",
}

FORBIDDEN_SOURCE_FIELDS = {
    "raw_evidence_rows",
    "raw_rows",
    "raw_comments",
    "raw_comment",
    "raw_author_id",
    "raw_author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_id",
    "author_ids",
    "author_name",
    "author_names",
    "profile_url",
    "profile_urls",
    "private_message",
    "private_messages",
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
    "browser_profile",
    "browser_profiles",
    "absolute_private_path",
    "absolute_private_paths",
    ".env",
    "env_value",
    "evidence_items_jsonl_contents",
    "evidence_items_csv_contents",
    "source_manifest_row_contents",
    "collection_log_row_contents",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

ALLOWED_LABEL_ONLY_OUTCOMES = {
    "keep_paused",
    "needs_more_review",
    "blocked_privacy_or_raw_identity_risk",
    "blocked_missing_authority",
    "candidate_ready_for_future_docs_only_write_gate_discussion",
}

ACTIVE_ACTION_PREFIXES = (
    "approve ",
    "perform ",
    "create ",
    "use ",
    "start ",
    "authorize ",
    "call ",
    "generate ",
    "run ",
    "inspect ",
    "read ",
    "parse ",
    "fetch ",
    "scrape",
    "publish",
    "send ",
    "post ",
    "execute ",
)

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
    "read_real_package_dir",
    "parsed_production_package_rows",
    "parsed_evidence_items_jsonl",
    "parsed_evidence_items_csv",
    "read_original_package_rows",
    "emitted_raw_rows",
    "emitted_raw_comments",
    "emitted_raw_identities",
    "emitted_profile_urls",
    "read_secrets",
    "wrote_evidence_layer",
    "created_persisted_evidence_layer_record",
    "created_production_evidence_item",
    "used_review_queue_runtime",
    "created_production_review_queue_item",
    "created_production_case",
    "created_production_analysis_run",
    "started_actual_analysis_execution",
    "authorized_production_analysis_result",
    "created_production_analysis_result",
    "called_source11_runtime",
    "called_finalsummaryreport_runtime",
    "generated_b_end_report_runtime",
    "generated_sandbox_runtime",
    "generated_public_event_runtime",
    "created_export_download_public_delivery",
    "modified_route",
    "modified_frontend",
    "modified_runtime",
    "published_or_sent",
    "auto_executed",
]

OUTPUT_FALSE_FIELDS = [
    "route_ready",
    "frontend_ready",
    "runtime_ready",
    "public_ready",
    "production_ready",
    "actual_write_enabled",
    "production_object_enabled",
    "review_queue_runtime_enabled",
    "source11_runtime_enabled",
    "finalsummaryreport_runtime_enabled",
    "actual_evidence_layer_write",
    "persisted_evidence_layer_record_created",
    "production_evidence_item_created",
    "review_queue_runtime_used",
    "production_review_queue_item_created",
    "production_case_created",
    "production_analysis_run_created",
    "actual_analysis_execution_started",
    "production_analysis_result_authorized",
    "production_analysis_result_created",
    "source11_runtime_called",
    "finalsummaryreport_runtime_called",
    "public_delivery_created",
    "collector_provider_jobs",
    "real_exchange_package_dirs_read",
    "production_package_rows_parsed",
    "raw_rows_comments_identities_exposed",
    "secrets_read",
]


def build_internal_alpha_review_console_safe_metadata_projection(
    source_summary: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    if not blockers:
        blockers.extend(_source_blockers(source_summary))

    if blockers:
        return _base_projection(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            source_summary=None,
        )

    assert isinstance(source_summary, dict)
    return _base_projection(
        status=READY_STATUS,
        created=True,
        blockers=[],
        source_summary=source_summary,
    )


create_internal_alpha_review_console_safe_metadata_projection = (
    build_internal_alpha_review_console_safe_metadata_projection
)


def build_safe_internal_alpha_review_console_projection_summary(
    source_summary: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    projection = build_internal_alpha_review_console_safe_metadata_projection(
        source_summary,
        exact_approval_phrase=exact_approval_phrase,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "projection_schema": projection["projection_schema"],
        "projection_status": projection["projection_status"],
        "projection_created": projection["projection_created"],
        "projection_mode": projection["projection_mode"],
        "source_chain_boundary": projection["source_chain_boundary"],
        "safe_metadata_only": projection["safe_metadata_only"],
        "label_only_operator_outcomes": projection["label_only_operator_outcomes"],
        "warning_count": projection["warning_count"],
        "blocker_count": projection["blocker_count"],
        "human_review_required": projection["human_review_required"],
        "no_automatic_trust_upgrade": projection["no_automatic_trust_upgrade"],
        "blockers": list(projection["blockers"]),
        "runtime_side_effects": dict(projection["runtime_side_effects"]),
        **_false_output_flags(),
    }


def _base_projection(
    *,
    status: str,
    created: bool,
    blockers: list[str],
    source_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "projection_schema": PROJECTION_SCHEMA,
        "phase": PHASE,
        "projection_status": status,
        "projection_created": created,
        "created_at": _utc_now(),
        "projection_mode": PROJECTION_MODE,
        "source_chain_boundary": SOURCE_CHAIN_BOUNDARY,
        "safe_metadata_only": True,
        "label_only_operator_outcomes": True,
        "request_id": _safe_source_label(source_summary, "request_id"),
        "provider_result_id": _safe_source_label(source_summary, "provider_result_id"),
        "package_reference": _safe_source_label(source_summary, "package_reference"),
        "stage_summary": _stage_summary(source_summary),
        "candidate_id": _safe_source_label(source_summary, "candidate_id"),
        "boundary_id": _safe_source_label(source_summary, "boundary_id"),
        "evidence_count": _safe_non_negative_int(_source_value(source_summary, "evidence_count")),
        "source_count": _safe_non_negative_int(_source_value(source_summary, "source_count")),
        "warning_count": _safe_non_negative_int(_source_value(source_summary, "warning_count")),
        "blocker_count": _safe_non_negative_int(_source_value(source_summary, "blocker_count")),
        "coverage_note_summary": _safe_source_text(source_summary, "coverage_note_summary"),
        "validation_summary": _safe_source_text(source_summary, "validation_summary"),
        "safety_flags": _safe_dict(_source_value(source_summary, "safety_flags")),
        "boundary_flags": _safe_dict(_source_value(source_summary, "boundary_flags")),
        "audit_refs": _safe_string_list(_source_value(source_summary, "audit_refs")),
        "health_report_refs": _safe_string_list(_source_value(source_summary, "health_report_refs")),
        "allowed_actions": _safe_string_list(_source_value(source_summary, "allowed_actions")),
        "blocked_actions": _safe_string_list(_source_value(source_summary, "blocked_actions")),
        "next_gate_inactive_phrase_labels": _safe_string_list(
            _source_value(source_summary, "next_gate_inactive_phrase_labels")
        ),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "blockers": _dedupe(blockers),
        "runtime_side_effects": _runtime_side_effects(),
        **_false_output_flags(),
    }


def _source_blockers(source_summary: dict[str, Any] | None) -> list[str]:
    if not isinstance(source_summary, dict):
        return ["source_summary_missing_or_not_object"]

    blockers: list[str] = []
    if source_summary.get("source_summary_schema") != SOURCE_SCHEMA:
        blockers.append("source_schema_wrong")
    if source_summary.get("source_chain_boundary") != SOURCE_CHAIN_BOUNDARY:
        blockers.append("source_chain_boundary_wrong")
    if source_summary.get("human_review_required") is not True:
        blockers.append("source_human_review_required_not_true")
    if source_summary.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_no_automatic_trust_upgrade_not_true")

    for field in REQUIRED_SAFE_ID_FIELDS:
        value = source_summary.get(field)
        if not _is_safe_text(value):
            blockers.append(f"source_required_safe_id_missing:{field}")

    package_reference = source_summary.get("package_reference")
    if isinstance(package_reference, str) and _looks_path_like(package_reference):
        blockers.append("source_package_reference_path_like")

    for field, reason in FALSE_SOURCE_FLAGS.items():
        if source_summary.get(field) is True:
            blockers.append(reason)
    for field, reason in READINESS_TRUE_FLAGS.items():
        if source_summary.get(field) is True:
            blockers.append(reason)

    for field in ["evidence_count", "source_count", "warning_count", "blocker_count"]:
        value = source_summary.get(field)
        if not _is_non_negative_int(value):
            blockers.append(f"source_count_invalid:{field}")

    forbidden_field = _first_forbidden_field(source_summary)
    if forbidden_field is not None:
        blockers.append(f"source_forbidden_field:{forbidden_field}")

    forbidden_value_path = _first_forbidden_value_path(source_summary)
    if forbidden_value_path is not None:
        blockers.append(f"source_forbidden_value:{forbidden_value_path}")

    action_blocker = _action_label_blocker(source_summary.get("allowed_actions"))
    if action_blocker is None:
        action_blocker = _action_label_blocker(source_summary.get("blocked_actions"))
    if action_blocker is not None:
        blockers.append(action_blocker)

    return _dedupe(blockers)


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        return ["blocked_missing_exact_8z20_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_8z20_approval"]
    return []


def _action_label_blocker(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, list):
        return "source_action_labels_not_list"
    for action in value:
        if not _is_safe_text(action):
            return "source_action_label_invalid"
        assert isinstance(action, str)
        normalized = " ".join(action.strip().casefold().split())
        if action in ALLOWED_LABEL_ONLY_OUTCOMES:
            continue
        if _looks_like_active_action(normalized):
            return f"source_forbidden_active_action:{action}"
    return None


def _looks_like_active_action(normalized_action: str) -> bool:
    if any(normalized_action.startswith(prefix) for prefix in ACTIVE_ACTION_PREFIXES):
        return True
    if "publish/send/post/execute" in normalized_action:
        return True
    return False


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_source_boundary_violation"
    first = blockers[0]
    if first.startswith("blocked_"):
        return first
    if first.startswith("source_required") or first.startswith("source_schema") or first.startswith("source_chain"):
        return "blocked_invalid_safe_projection_source"
    if first.startswith("source_forbidden_field") or first.startswith("source_forbidden_value"):
        return "blocked_forbidden_safe_projection_source"
    return "blocked_source_boundary_violation"


def _stage_summary(source_summary: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "stage_id": _safe_source_label(source_summary, "stage_id"),
        "stage_schema": _safe_source_label(source_summary, "stage_schema"),
        "stage_status": _safe_source_label(source_summary, "stage_status"),
        "stage_mode": _safe_source_label(source_summary, "stage_mode"),
    }


def _source_value(source_summary: dict[str, Any] | None, field: str) -> Any:
    if not isinstance(source_summary, dict):
        return None
    return source_summary.get(field)


def _safe_source_label(source_summary: dict[str, Any] | None, field: str) -> str | None:
    return _safe_label(_source_value(source_summary, field))


def _safe_source_text(source_summary: dict[str, Any] | None, field: str) -> str | None:
    text = _safe_text(_source_value(source_summary, field))
    if text is None:
        return None
    return text[:240]


def _safe_dict(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    safe: dict[str, Any] = {}
    for key, item in value.items():
        safe_key = _safe_label(key)
        if safe_key is None:
            continue
        if isinstance(item, bool):
            safe[safe_key] = item
        elif isinstance(item, int) and not isinstance(item, bool):
            safe[safe_key] = item
        else:
            safe_value = _safe_label(item)
            if safe_value is not None:
                safe[safe_key] = safe_value
    return safe


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe: list[str] = []
    for item in value[:20]:
        label = _safe_label(item)
        if label is not None:
            safe.append(label)
    return safe


def _safe_non_negative_int(value: Any) -> int:
    if _is_non_negative_int(value):
        return value
    return 0


def _is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _is_safe_text(value: Any) -> bool:
    return _safe_text(value) is not None


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if _looks_forbidden_value(stripped):
        return None
    return stripped


def _safe_label(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:120]


def _first_forbidden_field(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in FORBIDDEN_SOURCE_FIELDS:
                return key
            nested = _first_forbidden_field(item)
            if nested is not None:
                return nested
    elif isinstance(value, list):
        for item in value:
            nested = _first_forbidden_field(item)
            if nested is not None:
                return nested
    return None


def _first_forbidden_value_path(value: Any, path: str | None = None) -> str | None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = key if isinstance(key, str) else "unknown"
            nested_path = key_text if path is None else f"{path}.{key_text}"
            nested = _first_forbidden_value_path(item, nested_path)
            if nested is not None:
                return nested
    elif isinstance(value, list):
        for item in value:
            nested = _first_forbidden_value_path(item, path)
            if nested is not None:
                return nested
    elif isinstance(value, str) and _looks_forbidden_value(value):
        return path or "value"
    return None


def _looks_path_like(value: str) -> bool:
    return "/" in value or "\\" in value or ":\\" in value or ":/" in value


def _looks_forbidden_value(value: str) -> bool:
    lowered = value.casefold()
    if "actual-" in lowered and "should-never-appear" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if "://" in value or ":\\" in value or ":/" in value:
        return True
    if ".env" in lowered:
        return True
    return False


def _runtime_side_effects() -> dict[str, bool]:
    return {flag: False for flag in RUNTIME_SIDE_EFFECT_FLAGS}


def _false_output_flags() -> dict[str, bool]:
    return {field: False for field in OUTPUT_FALSE_FIELDS}


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
