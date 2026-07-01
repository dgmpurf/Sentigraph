from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


BRIDGE_SCHEMA = "sentigraph_staging_candidate_generated_run_bridge_v0_1"
INPUT_SOURCE_KIND = "review_only_staging_candidate"
MODEL_INPUT_KIND = "metadata_only_staging_summary"

READY_STATUS = "ready_for_minimum_real_run_input_candidate"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_PATH_STATUS = "blocked_path_escape"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
MANUAL_REVIEW_STATUS = "manual_review_required"

REQUIRED_FIELDS = {
    "staging_candidate_id": "missing_staging_candidate_id",
    "provider_result_id": "missing_provider_result_id",
    "request_id": "missing_request_id",
    "package_name": "missing_package_name",
}

FORBIDDEN_FIELD_NAMES = {
    "full_evidence_rows",
    "raw_comment_dump",
    "raw_comments",
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
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
    "browser_profile",
    "browser_profile_path",
    "profile_path",
    "collector_runtime_internal_path",
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

REQUESTED_SIDE_EFFECT_FIELDS = {
    "evidence_row_parsing_requested",
    "evidence_rows_parsed",
    "parse_evidence_rows",
    "evidence_layer_write",
    "write_evidence_layer",
    "production_case_created",
    "create_production_case",
    "production_analysis_run_created",
    "create_production_analysis_run",
    "analysis_run_created",
    "generated_response_text",
    "public_route_created",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

PATH_FIELD_NAMES = {
    "absolute_package_path",
    "collector_runtime_internal_path",
    "browser_profile_path",
    "profile_path",
    "path_reference",
}

DOWNSTREAM_ALLOWED_ACTIONS = (
    "review_bridge_candidate",
    "request_future_minimum_real_run_execution_decision",
)

DOWNSTREAM_BLOCKED_ACTIONS = (
    "parse_evidence_rows",
    "read_original_package_rows",
    "write_evidence_layer",
    "create_production_case",
    "create_production_analysis_run",
    "execute_minimum_real_run_now",
    "call_dense_graph_directly",
    "add_api_route",
    "add_frontend_ui",
    "generate_report",
    "generate_sandbox_or_public_event",
    "generate_public_output",
    "publish",
    "send",
    "post",
    "execute",
)


def build_staging_candidate_generated_run_bridge(
    staging_summary: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_input = staging_summary if isinstance(staging_summary, dict) else {}
    blockers = _collect_blockers(safe_input)
    warnings = _safe_string_list(safe_input.get("warnings"))
    bridge_status = _bridge_status(blockers, safe_input)
    minimum_candidate = build_minimum_real_run_input_candidate_from_staging(safe_input)

    return {
        "bridge_id": _bridge_id(_safe_value(safe_input, "staging_candidate_id")),
        "bridge_schema": BRIDGE_SCHEMA,
        "bridge_status": bridge_status,
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "staging_candidate_id": _safe_value(safe_input, "staging_candidate_id"),
        "provider_result_id": _safe_value(safe_input, "provider_result_id"),
        "provider_job_id": _safe_value(safe_input, "provider_job_id"),
        "request_id": _request_id(safe_input),
        "case_id_hint": _safe_value(safe_input, "case_id_hint"),
        "package_name": _safe_package_name(safe_input.get("package_name")),
        "package_role": _package_role(safe_input),
        "input_source_kind": INPUT_SOURCE_KIND,
        "input_scope_note": _input_scope_note(safe_input),
        "metadata_only": True,
        "evidence_rows_parsed": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "generated_response_text": False,
        "public_route_created": False,
        "human_review_required": True,
        "generated_run_requested": False,
        "minimum_real_run_input_candidate": minimum_candidate,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": warnings,
        "blockers": blockers,
        "audit_refs": _safe_audit_refs(safe_input.get("audit_refs")),
        "downstream_allowed_actions": list(DOWNSTREAM_ALLOWED_ACTIONS),
        "downstream_blocked_actions": list(DOWNSTREAM_BLOCKED_ACTIONS),
    }


def build_minimum_real_run_input_candidate_from_staging(staging_summary: dict[str, Any]) -> dict[str, Any]:
    safe_input = staging_summary if isinstance(staging_summary, dict) else {}
    package_name = _safe_package_name(safe_input.get("package_name"))
    sample_id = package_name or _safe_value(safe_input, "staging_candidate_id") or "missing_sample_id"
    case_id_hint = _safe_value(safe_input, "case_id_hint") or "missing_case_id"
    return {
        "candidate_id": f"minimum_real_run_input_{_safe_identifier(sample_id)}",
        "case_id_hint": case_id_hint,
        "case_id": case_id_hint,
        "sample_id": sample_id,
        "provider_result_id": _safe_value(safe_input, "provider_result_id"),
        "staging_candidate_id": _safe_value(safe_input, "staging_candidate_id"),
        "package_name": package_name,
        "package_role": _package_role(safe_input),
        "validation_status": _safe_value(safe_input, "validation_status"),
        "evidence_count": _safe_int(safe_input.get("evidence_count")),
        "source_count": _safe_int(safe_input.get("source_count")),
        "warning_count": _safe_int(safe_input.get("warning_count")),
        "error_count": _safe_int(safe_input.get("error_count")),
        "coverage_summary": _safe_mapping(safe_input.get("coverage_summary")),
        "validation_summary": _safe_mapping(safe_input.get("validation_summary")),
        "scope_note": _input_scope_note(safe_input),
        "model_input_kind": MODEL_INPUT_KIND,
        "human_review_required": True,
        "coefficient_source": "mock_default",
        "calibration_status": "uncalibrated",
        "empirical_validation": "not_started",
        "fixture_metadata": {
            "case_id": case_id_hint,
            "sample_id": sample_id,
            "fixture_role": "bridge_input_candidate",
            "source_mode": MODEL_INPUT_KIND,
            "coverage_note": _coverage_note(safe_input),
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": [],
        "module_seed_policy": "metadata_only_seed_candidate",
    }


def build_safe_staging_to_generated_run_bridge_summary(bridge: dict[str, Any]) -> dict[str, Any]:
    safe_bridge = bridge if isinstance(bridge, dict) else {}
    return {
        "schema": "sentigraph_staging_candidate_generated_run_bridge_summary_v0_1",
        "bridge_id": _safe_value(safe_bridge, "bridge_id"),
        "bridge_schema": _safe_value(safe_bridge, "bridge_schema"),
        "bridge_status": _safe_value(safe_bridge, "bridge_status"),
        "staging_candidate_id": _safe_value(safe_bridge, "staging_candidate_id"),
        "provider_result_id": _safe_value(safe_bridge, "provider_result_id"),
        "request_id": _safe_value(safe_bridge, "request_id"),
        "package_name": _safe_package_name(safe_bridge.get("package_name")),
        "metadata_only": True,
        "evidence_rows_parsed": False,
        "evidence_layer_write": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "generated_response_text": False,
        "public_route_created": False,
        "human_review_required": True,
        "path_exposed": False,
        "path_reference": "review_only_metadata_summary",
        "downstream_allowed_actions": list(safe_bridge.get("downstream_allowed_actions") or []),
        "downstream_blocked_actions": list(safe_bridge.get("downstream_blocked_actions") or []),
        "blockers": list(safe_bridge.get("blockers") or []),
        "warnings": list(safe_bridge.get("warnings") or []),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    normalized = dict(value)
    if "request_id" not in normalized and "analysis_request_id" in normalized:
        normalized["request_id"] = normalized.get("analysis_request_id")

    for field_name, reason in REQUIRED_FIELDS.items():
        field_value = normalized.get(field_name)
        if field_name == "package_name":
            field_value = _safe_package_name(field_value)
        if not _safe_label(field_value):
            blockers.append(_blocker(reason, "metadata_contract"))

    package_status = _nested_value(value, ("gate_result", "package_resolution_status"))
    if package_status not in {None, "", "accepted_metadata_only", "validation_passed"}:
        blockers.append(_blocker("package_resolution_not_accepted", "metadata_contract"))

    validation_status = str(value.get("validation_status") or "").lower()
    gate_privacy_status = str(_nested_value(value, ("gate_result", "privacy_status")) or "").lower()
    if "privacy" in validation_status or gate_privacy_status not in {"", "clear"}:
        blockers.append(_blocker("blocked_privacy_issue", "privacy"))

    if _has_path_leak(value):
        blockers.append(_blocker("blocked_path_escape", "path"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_metadata_field_present:{field_name}", "privacy"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    for existing_blocker in _safe_string_list(value.get("blockers")):
        lowered = existing_blocker.lower()
        if any(marker in lowered for marker in ("privacy", "path_escape", "forbidden", "security")):
            blockers.append(_blocker("upstream_blocker_requires_manual_review", "upstream"))

    return _dedupe_blockers(blockers)


def _bridge_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        if str(value.get("validation_status") or "").lower() in {"warn", "warning", "manual_review_required"}:
            return MANUAL_REVIEW_STATUS
        return READY_STATUS
    categories = {blocker["category"] for blocker in blockers}
    reasons = {blocker["reason"] for blocker in blockers}
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "path" in categories or "blocked_path_escape" in reasons:
        return BLOCKED_PATH_STATUS
    if "privacy" in categories:
        return BLOCKED_PRIVACY_STATUS
    return BLOCKED_METADATA_STATUS


def _boundary_flags() -> dict[str, bool]:
    return {
        "selected_sample_only": True,
        "controlled_package_only": True,
        "metadata_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "provider_output_is_evidence_not_truth": True,
        "human_review_required": True,
        "no_auto_execute": True,
        "no_generated_public_response": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_collector": False,
        "accessed_private_collector": False,
        "read_real_exchange_dir": False,
        "fetched_url": False,
        "scraped_page": False,
        "parsed_evidence_items_file": False,
        "read_original_package_rows": False,
        "wrote_evidence_layer": False,
        "created_production_case": False,
        "created_analysis_run": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "generated_response_text": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _find_forbidden_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_FIELD_NAMES:
                found.add(str(key))
            found.update(_find_forbidden_fields(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item))
    return found


def _find_requested_side_effects(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            if lowered in REQUESTED_SIDE_EFFECT_FIELDS and _truthy(nested_value):
                found.add(str(key))
            found.update(_find_requested_side_effects(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_requested_side_effects(item))
    return found


def _has_path_leak(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            if lowered in PATH_FIELD_NAMES and lowered != "path_reference" and _safe_label(nested_value):
                return True
            if lowered == "path_reference" and isinstance(nested_value, str) and _looks_like_private_or_absolute_path(nested_value):
                return True
            if lowered == "package_name" and _safe_label(nested_value) and not _is_safe_package_name(nested_value):
                return True
            if _has_path_leak(nested_value):
                return True
    elif isinstance(value, list):
        return any(_has_path_leak(item) for item in value)
    elif isinstance(value, str):
        return _looks_like_private_or_absolute_path(value)
    return False


def _safe_package_name(value: Any) -> str | None:
    if not _is_safe_package_name(value):
        return None
    return str(value).strip()


def _is_safe_package_name(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    if not stripped or stripped in {".", ".."}:
        return False
    if "/" in stripped or "\\" in stripped or ":" in stripped:
        return False
    if _looks_like_private_or_absolute_path(stripped):
        return False
    return True


def _looks_like_private_or_absolute_path(value: str) -> bool:
    lowered = value.lower()
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if ":/" in lowered or ":\\" in lowered:
        return True
    if lowered.startswith("\\\\") or lowered.startswith("/"):
        return True
    return False


def _package_role(value: dict[str, Any]) -> str | None:
    direct = _safe_value(value, "package_role")
    if direct:
        return direct
    package_reference = value.get("package_reference")
    if isinstance(package_reference, dict):
        return _safe_value(package_reference, "package_role")
    return None


def _request_id(value: dict[str, Any]) -> str | None:
    return _safe_value(value, "request_id") or _safe_value(value, "analysis_request_id")


def _input_scope_note(value: dict[str, Any]) -> str:
    coverage = value.get("coverage_summary")
    if isinstance(coverage, dict):
        note = _safe_value(coverage, "coverage_note")
        if note:
            return note
    return "selected sample / controlled package metadata only"


def _coverage_note(value: dict[str, Any]) -> str:
    coverage = value.get("coverage_summary")
    if isinstance(coverage, dict):
        return _safe_value(coverage, "coverage_note") or "selected sample / controlled package metadata only"
    return "selected sample / controlled package metadata only"


def _safe_value(mapping: dict[str, Any], key: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str):
        return None
    if _looks_like_private_or_absolute_path(value):
        return None
    stripped = value.strip()
    return stripped or None


def _safe_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    safe: dict[str, Any] = {}
    for key, nested_value in value.items():
        key_text = str(key)
        lowered = key_text.lower()
        if lowered in FORBIDDEN_FIELD_NAMES | PATH_FIELD_NAMES:
            continue
        if isinstance(nested_value, str):
            if _looks_like_private_or_absolute_path(nested_value):
                continue
            safe[key_text] = nested_value
        elif isinstance(nested_value, (int, float, bool)) or nested_value is None:
            safe[key_text] = nested_value
        elif isinstance(nested_value, dict):
            safe[key_text] = _safe_mapping(nested_value)
        elif isinstance(nested_value, list):
            safe[key_text] = [_safe_mapping(item) if isinstance(item, dict) else item for item in nested_value if not isinstance(item, str) or not _looks_like_private_or_absolute_path(item)]
    return safe


def _safe_audit_refs(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    refs: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        safe_item = {
            key: str(nested_value)
            for key, nested_value in item.items()
            if isinstance(nested_value, str) and not _looks_like_private_or_absolute_path(nested_value)
        }
        if safe_item:
            refs.append(safe_item)
    return refs


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in (str(item).strip() for item in value) if item and not _looks_like_private_or_absolute_path(item)]


def _safe_label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _safe_int(value: Any) -> int | None:
    return value if isinstance(value, int) else None


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _nested_value(value: dict[str, Any], keys: tuple[str, ...]) -> Any:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "requested", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _blocker(reason: str, category: str) -> dict[str, str]:
    return {"reason": reason, "category": category}


def _dedupe_blockers(blockers: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for blocker in blockers:
        key = (blocker["reason"], blocker["category"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(blocker)
    return deduped


def _bridge_id(staging_candidate_id: str | None) -> str:
    return f"staging_generated_run_bridge_{_safe_identifier(staging_candidate_id)}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
