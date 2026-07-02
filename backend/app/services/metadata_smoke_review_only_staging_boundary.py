from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.real_exported_package_metadata_smoke import (
    APPROVED_CASE_ID_HINT,
    APPROVED_PACKAGE_NAME,
    APPROVED_PACKAGE_ROLE,
    SCHEMA as INPUT_SCHEMA,
    PHASE as INPUT_PHASE,
    READY_STATUS as INPUT_READY_STATUS,
    WARN_STATUS as INPUT_WARN_STATUS,
)


SCHEMA = "sentigraph_metadata_smoke_review_only_staging_boundary_v0_1"
PHASE = "8W-4"
INPUT_SOURCE_KIND = "real_exported_package_metadata_smoke"
READY_BOUNDARY_STATUS = "review_only_staging_boundary_ready_for_manual_review"

ALLOWED_ACTIONS = [
    "manual_review_warning_acknowledgement_required",
    "keep_as_metadata_checkpoint",
    "future_review_only_staging_boundary_review",
    "future_row_preview_gate_decision_required",
]

BLOCKED_ACTIONS = [
    "row_preview",
    "evidence_layer_write",
    "production_case_creation",
    "production_analysis_run_creation",
    "production_review_queue_creation",
    "b_end_report_runtime",
    "sandbox_public_event_runtime",
    "frontend_route",
    "report_export_download_public_final_delivery_runtime",
    "real_api_llm_provider_collector",
    "publish_send_post_execute",
]

RUNTIME_SIDE_EFFECT_FLAGS = [
    "called_real_api",
    "called_real_llm",
    "ran_provider_job",
    "ran_collector",
    "accessed_private_collector",
    "inspected_private_collector_source",
    "read_real_exchange_dir",
    "fetched_url",
    "scraped_page",
    "parsed_evidence_items_jsonl",
    "parsed_evidence_items_csv",
    "parsed_source_manifest_jsonl_rows",
    "parsed_collection_log_jsonl_rows",
    "read_original_package_rows",
    "read_raw_comments",
    "read_raw_identities",
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

TOP_LEVEL_FALSE_FLAGS = {
    "review_only_staging_runtime_used": False,
    "review_queue_item_created": False,
    "production_review_queue_item_created": False,
    "evidence_items_created": False,
    "row_preview_approved": False,
    "row_files_parsed": False,
    "original_package_rows_read": False,
    "private_collector_source_inspected": False,
    "real_exchange_dir_read": False,
    "evidence_layer_write": False,
    "production_case_created": False,
    "production_analysis_run_created": False,
    "frontend_ready": False,
    "route_ready": False,
    "production_ready": False,
    "public_ready": False,
    "customer_ready": False,
    "b_end_ready": False,
    "sandbox_ready": False,
    "public_event_ready": False,
}

FORBIDDEN_FIELD_NAMES = {
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
    "profile_url",
    "profile_urls",
    "raw_comment",
    "raw_comments",
    "private_message",
    "private_messages",
    "token",
    "tokens",
    "cookie",
    "cookies",
    "session",
    "sessions",
    "api_key",
    "api_keys",
    "password",
    "passwords",
    "salt",
    "salts",
    "absolute_path",
    "absolute_package_path",
    "package_path",
    "runtime_path",
    "browser_profile",
    "browser_profile_path",
    "collector_runtime_internal_path",
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

TOP_LEVEL_TRUE_BLOCK_FLAGS = {
    "row_files_parsed": "row_files_parsed_true",
    "evidence_items_jsonl_parsed": "evidence_items_jsonl_parsed_true",
    "evidence_items_csv_parsed": "evidence_items_csv_parsed_true",
    "original_package_rows_read": "original_package_rows_read_true",
    "private_collector_source_inspected": "private_collector_source_inspected_true",
    "real_exchange_dir_read": "real_exchange_dir_read_true",
    "evidence_layer_write": "evidence_layer_write_requested",
    "production_case_created": "production_case_requested",
    "production_analysis_run_created": "production_analysis_run_requested",
}

REQUESTED_ACTIONS = {
    "row_preview",
    "evidence_layer_write",
    "production_case",
    "production_analysis_run",
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


def build_metadata_smoke_review_only_staging_boundary(
    metadata_smoke: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build an 8W-4 metadata-only boundary marker from an existing 8W-2 object."""

    blockers = _validate_input(metadata_smoke)
    ready = not blockers
    safe_summary = _safe_source_summary(metadata_smoke if isinstance(metadata_smoke, dict) else {})

    boundary = {
        "schema": SCHEMA,
        "phase": PHASE,
        "boundary_status": READY_BOUNDARY_STATUS if ready else _blocked_status(blockers),
        "created_at": _utc_now(),
        "created_local_review_only_staging_boundary": ready,
        "input_source_kind": INPUT_SOURCE_KIND,
        "input_schema": _safe_string((metadata_smoke or {}).get("schema")) if isinstance(metadata_smoke, dict) else None,
        "input_phase": _safe_string((metadata_smoke or {}).get("phase")) if isinstance(metadata_smoke, dict) else None,
        "input_smoke_status": _safe_string((metadata_smoke or {}).get("smoke_status")) if isinstance(metadata_smoke, dict) else None,
        "approved_target_package_name": APPROVED_PACKAGE_NAME,
        "approved_target_package_role": APPROVED_PACKAGE_ROLE,
        "approved_target_case_id_hint": APPROVED_CASE_ID_HINT,
        "metadata_only": True,
        "human_review_required": True,
        "warning_count": safe_summary["warning_count"],
        "warning_manual_review_preserved": ready,
        "safe_source_summary": safe_summary,
        "boundary_flags": _boundary_flags(ready=ready),
        "runtime_side_effects": _runtime_side_effects(),
        "allowed_actions": list(ALLOWED_ACTIONS),
        "blocked_actions": list(BLOCKED_ACTIONS),
        "blocker_codes": blockers,
        **TOP_LEVEL_FALSE_FLAGS,
    }
    boundary["review_only_staging_boundary_created"] = ready
    return boundary


create_metadata_smoke_review_only_staging_boundary = build_metadata_smoke_review_only_staging_boundary


def build_safe_metadata_smoke_review_only_staging_boundary_summary(
    metadata_smoke: dict[str, Any] | None,
) -> dict[str, Any]:
    return build_metadata_smoke_review_only_staging_boundary(metadata_smoke)


def _validate_input(metadata_smoke: dict[str, Any] | None) -> list[str]:
    if not isinstance(metadata_smoke, dict):
        return ["input_missing_or_not_object"]

    blockers: list[str] = []
    if metadata_smoke.get("schema") != INPUT_SCHEMA:
        blockers.append("input_schema_not_8w2_metadata_smoke")
    if metadata_smoke.get("phase") != INPUT_PHASE:
        blockers.append("input_phase_not_8w2")
    smoke_status = metadata_smoke.get("smoke_status")
    if smoke_status not in {INPUT_READY_STATUS, INPUT_WARN_STATUS}:
        blockers.append("input_smoke_status_blocked_or_unknown")
    if metadata_smoke.get("target_package_name") != APPROVED_PACKAGE_NAME:
        blockers.append("package_name_not_approved")
    if metadata_smoke.get("target_package_role") != APPROVED_PACKAGE_ROLE:
        blockers.append("package_role_not_approved")
    if metadata_smoke.get("target_case_id_hint") != APPROVED_CASE_ID_HINT:
        blockers.append("case_id_hint_not_approved")
    if metadata_smoke.get("metadata_only") is not True:
        blockers.append("metadata_only_not_true")
    if metadata_smoke.get("human_review_required") is not True:
        blockers.append("human_review_required_not_true")

    warning_count = metadata_smoke.get("warning_count")
    if not isinstance(warning_count, int) or isinstance(warning_count, bool):
        blockers.append("warning_count_missing_or_invalid")
    elif smoke_status == INPUT_WARN_STATUS and warning_count < 1:
        blockers.append("warning_manual_review_state_dropped")

    for flag_name, reason in TOP_LEVEL_TRUE_BLOCK_FLAGS.items():
        if metadata_smoke.get(flag_name) is True:
            blockers.append(reason)

    runtime_side_effects = metadata_smoke.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("runtime_side_effects_missing_or_invalid")
    else:
        for flag_name in RUNTIME_SIDE_EFFECT_FLAGS:
            if runtime_side_effects.get(flag_name) is True:
                blockers.append(f"runtime_side_effect_true:{flag_name}")

    requested_actions = metadata_smoke.get("requested_actions")
    if isinstance(requested_actions, list):
        for action in requested_actions:
            if isinstance(action, str) and action in REQUESTED_ACTIONS:
                blockers.append(f"requested_action_blocked:{action}")
    elif isinstance(requested_actions, dict):
        for action, requested in requested_actions.items():
            if isinstance(action, str) and action in REQUESTED_ACTIONS and _truthy(requested):
                blockers.append(f"requested_action_blocked:{action}")

    blockers.extend(_forbidden_input_blockers(metadata_smoke))
    return _dedupe(blockers)


def _safe_source_summary(metadata_smoke: dict[str, Any]) -> dict[str, Any]:
    safe_summary = metadata_smoke.get("safe_summary")
    if not isinstance(safe_summary, dict):
        safe_summary = {}
    return {
        "target_package_name": APPROVED_PACKAGE_NAME,
        "target_package_role": APPROVED_PACKAGE_ROLE,
        "target_case_id_hint": APPROVED_CASE_ID_HINT,
        "input_smoke_status": _safe_string(metadata_smoke.get("smoke_status")),
        "warning_count": _safe_count(metadata_smoke.get("warning_count")),
        "error_count": _safe_count(metadata_smoke.get("error_count"), safe_summary.get("error_count")),
        "validation_status": _safe_string(safe_summary.get("validation_status")),
        "evidence_count_summary": _safe_string_or_int(safe_summary.get("evidence_count_summary")),
        "source_count_summary": _safe_string_or_int(safe_summary.get("source_count_summary")),
        "coverage_note_summary": _safe_summary_text(safe_summary.get("coverage_note_summary")),
        "privacy_status": _safe_string(safe_summary.get("privacy_status")),
        "path_status": _safe_string(safe_summary.get("path_status")),
        "warning_summary": _safe_string_list(safe_summary.get("warning_summary") or metadata_smoke.get("warnings")),
        "blocker_summary": _safe_string_list(safe_summary.get("blocker_summary") or metadata_smoke.get("blockers")),
    }


def _boundary_flags(*, ready: bool) -> dict[str, bool]:
    return {
        "metadata_only": True,
        "selected_sample_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "provider_output_is_evidence_candidate_not_truth": True,
        "no_row_read": True,
        "no_private_collector_source_inspection": True,
        "no_evidence_layer_write": True,
        "no_production_case": True,
        "no_production_analysis_run": True,
        "no_frontend_route": True,
        "no_real_api_llm_provider_collector": True,
        "human_review_required": True,
        "warning_manual_review_preserved": ready,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


def _blocked_status(blockers: list[str]) -> str:
    if any(reason.startswith("forbidden_input_field") or reason == "forbidden_input_sensitive_value" for reason in blockers):
        return "blocked_forbidden_input"
    if any(reason.startswith("requested_action_blocked") for reason in blockers):
        return "blocked_requested_action"
    if any(reason.startswith("runtime_side_effect_true") for reason in blockers):
        return "blocked_runtime_side_effect"
    if any(reason in blockers for reason in ("package_name_not_approved", "package_role_not_approved", "case_id_hint_not_approved")):
        return "blocked_target_identity"
    if any(
        reason in blockers
        for reason in (
            "row_files_parsed_true",
            "evidence_items_jsonl_parsed_true",
            "evidence_items_csv_parsed_true",
            "original_package_rows_read_true",
            "private_collector_source_inspected_true",
            "real_exchange_dir_read_true",
        )
    ):
        return "blocked_unsafe_source"
    return "blocked_metadata_smoke_contract"


def _forbidden_input_blockers(value: Any) -> list[str]:
    blockers: list[str] = []
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            if lowered in {"runtime_side_effects", "boundary_flags"} and isinstance(nested_value, dict):
                blockers.extend(_forbidden_runtime_or_boundary_values(nested_value))
                continue
            if lowered in FORBIDDEN_FIELD_NAMES:
                blockers.append(f"forbidden_input_field:{lowered}")
                continue
            blockers.extend(_forbidden_input_blockers(nested_value))
    elif isinstance(value, list):
        for item in value:
            blockers.extend(_forbidden_input_blockers(item))
    elif isinstance(value, str) and _looks_like_forbidden_string(value):
        blockers.append("forbidden_input_sensitive_value")
    return blockers


def _forbidden_runtime_or_boundary_values(value: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for nested_value in value.values():
        if isinstance(nested_value, str) and _looks_like_forbidden_string(nested_value):
            blockers.append("forbidden_input_sensitive_value")
    return blockers


def _safe_count(*values: Any) -> int:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return max(value, 0)
    return 0


def _safe_string_or_int(value: Any) -> str | int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return max(value, 0)
    return _safe_string(value)


def _safe_summary_text(value: Any) -> str | None:
    text = _safe_string(value)
    if text is None:
        return None
    return text[:240]


def _safe_string(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_like_forbidden_string(stripped):
        return None
    return stripped


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe: list[str] = []
    for item in value[:20]:
        text = _safe_string(item)
        if text is not None:
            safe.append(text[:120])
    return safe


def _looks_like_forbidden_string(value: str) -> bool:
    lowered = value.lower()
    if "actual-" in lowered and "should-never-appear" in lowered:
        return True
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    if ":\\" in value or ":/" in value:
        return True
    if "donglu_sunjihai_youth_football/" in value or "donglu_sunjihai_youth_football\\" in value:
        return True
    return False


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
