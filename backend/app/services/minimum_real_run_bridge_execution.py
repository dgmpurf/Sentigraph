from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services import opinion_ecosystem_minimum_real_run as minimum_real_run


EXECUTION_SCHEMA = "sentigraph_minimum_real_run_bridge_execution_v0_1"
BRIDGE_SCHEMA = "sentigraph_staging_candidate_generated_run_bridge_v0_1"
READY_BRIDGE_STATUS = "ready_for_minimum_real_run_input_candidate"
INPUT_SOURCE_KIND = "staging_candidate_generated_run_bridge"
EXECUTION_MODE = "controlled_backend_only_minimum_real_run"
MODEL_INPUT_KIND = "metadata_only_staging_summary"

EXECUTED_STATUS = "executed_local_minimum_real_run"
BLOCKED_BRIDGE_STATUS = "blocked_bridge_not_ready"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
MANUAL_REVIEW_STATUS = "manual_review_required"

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
    "absolute_package_path",
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
    "dense_graph_called",
    "call_dense_graph_directly",
    "report_generated",
    "generate_report",
    "sandbox_public_event_generated",
    "generated_response_text",
    "public_route_created",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}

DOWNSTREAM_ALLOWED_ACTIONS = (
    "inspect_generated_run",
    "validate_boundary_flags",
    "validate_runtime_side_effect_flags",
    "call_dense_graph_later_after_separate_decision",
)

DOWNSTREAM_BLOCKED_ACTIONS = (
    "parse_evidence_rows",
    "read_original_package_rows",
    "write_evidence_layer",
    "create_production_case",
    "create_production_analysis_run",
    "call_dense_graph_directly",
    "generate_report",
    "generate_b_end_report",
    "generate_sandbox_or_public_event",
    "generate_public_output",
    "add_api_route",
    "add_frontend_ui",
    "publish",
    "send",
    "post",
    "execute",
)


def execute_minimum_real_run_from_bridge_candidate(
    bridge_candidate: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_bridge = bridge_candidate if isinstance(bridge_candidate, dict) else {}
    blockers = _collect_blockers(safe_bridge)
    status = _blocked_status(blockers, safe_bridge)

    if blockers:
        return _execution_object(
            safe_bridge,
            created_by=created_by,
            execution_status=status,
            minimum_real_run_executed=False,
            generated_run=None,
            blockers=blockers,
        )

    minimum_candidate = safe_bridge.get("minimum_real_run_input_candidate")
    generated_run = minimum_real_run.generate_opinion_ecosystem_minimum_real_run(
        _fixture_from_minimum_candidate(minimum_candidate if isinstance(minimum_candidate, dict) else {}, safe_bridge)
    )
    return _execution_object(
        safe_bridge,
        created_by=created_by,
        execution_status=EXECUTED_STATUS,
        minimum_real_run_executed=True,
        generated_run=generated_run,
        blockers=[],
    )


def build_minimum_real_run_bridge_execution(
    bridge_candidate: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return execute_minimum_real_run_from_bridge_candidate(bridge_candidate, created_by=created_by)


def build_safe_minimum_real_run_bridge_execution_summary(execution: dict[str, Any]) -> dict[str, Any]:
    safe_execution = execution if isinstance(execution, dict) else {}
    return {
        "schema": "sentigraph_minimum_real_run_bridge_execution_summary_v0_1",
        "execution_id": _safe_value(safe_execution, "execution_id"),
        "execution_schema": _safe_value(safe_execution, "execution_schema"),
        "execution_status": _safe_value(safe_execution, "execution_status"),
        "bridge_id": _safe_value(safe_execution, "bridge_id"),
        "bridge_schema": _safe_value(safe_execution, "bridge_schema"),
        "bridge_status_at_execution": _safe_value(safe_execution, "bridge_status_at_execution"),
        "staging_candidate_id": _safe_value(safe_execution, "staging_candidate_id"),
        "provider_result_id": _safe_value(safe_execution, "provider_result_id"),
        "request_id": _safe_value(safe_execution, "request_id"),
        "package_name": _safe_package_name(safe_execution.get("package_name")),
        "metadata_only": True,
        "evidence_rows_parsed": False,
        "minimum_real_run_executed": bool(safe_execution.get("minimum_real_run_executed")),
        "dense_graph_called": False,
        "path_exposed": False,
        "path_reference": "minimum_real_run_bridge_execution_summary",
        "blockers": _safe_blockers(safe_execution.get("blockers")),
        "warnings": _safe_string_list(safe_execution.get("warnings")),
    }


def _execution_object(
    bridge: dict[str, Any],
    *,
    created_by: str,
    execution_status: str,
    minimum_real_run_executed: bool,
    generated_run: dict[str, Any] | None,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "execution_id": _execution_id(_safe_value(bridge, "bridge_id")),
        "execution_schema": EXECUTION_SCHEMA,
        "execution_status": execution_status,
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "bridge_id": _safe_value(bridge, "bridge_id"),
        "bridge_schema": _safe_value(bridge, "bridge_schema"),
        "bridge_status_at_execution": _safe_value(bridge, "bridge_status"),
        "staging_candidate_id": _safe_value(bridge, "staging_candidate_id"),
        "provider_result_id": _safe_value(bridge, "provider_result_id"),
        "provider_job_id": _safe_value(bridge, "provider_job_id"),
        "request_id": _safe_value(bridge, "request_id"),
        "case_id_hint": _safe_value(bridge, "case_id_hint"),
        "package_name": _safe_package_name(bridge.get("package_name")),
        "input_source_kind": INPUT_SOURCE_KIND,
        "execution_mode": EXECUTION_MODE,
        "metadata_only": True,
        "evidence_rows_parsed": False,
        "minimum_real_run_executed": bool(minimum_real_run_executed),
        "dense_graph_called": False,
        "generated_run": _safe_generated_run(generated_run),
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _safe_string_list(bridge.get("warnings")),
        "blockers": _safe_blockers(blockers),
        "audit_refs": _safe_audit_refs(bridge.get("audit_refs")),
        "downstream_allowed_actions": list(DOWNSTREAM_ALLOWED_ACTIONS),
        "downstream_blocked_actions": list(DOWNSTREAM_BLOCKED_ACTIONS),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "bridge_id") is None:
        blockers.append(_blocker("missing_bridge_id", "metadata_contract"))
    if _safe_value(value, "bridge_schema") != BRIDGE_SCHEMA:
        blockers.append(_blocker("wrong_bridge_schema", "metadata_contract"))
    if _safe_value(value, "bridge_status") != READY_BRIDGE_STATUS:
        blockers.append(_blocker("bridge_status_not_ready", "bridge_status"))
    if _safe_package_name(value.get("package_name")) is None:
        blockers.append(_blocker("missing_package_name", "metadata_contract"))
    if value.get("metadata_only") is not True:
        blockers.append(_blocker("metadata_only_not_true", "metadata_contract"))
    if value.get("evidence_rows_parsed") is not False:
        blockers.append(_blocker("evidence_rows_parsed_not_false", "side_effect"))
    if value.get("human_review_required") is not True:
        blockers.append(_blocker("human_review_required_not_true", "metadata_contract"))
    if value.get("generated_run_requested") is not False:
        blockers.append(_blocker("generated_run_requested_not_false", "side_effect"))

    minimum_candidate = value.get("minimum_real_run_input_candidate")
    if not isinstance(minimum_candidate, dict):
        blockers.append(_blocker("missing_minimum_real_run_input_candidate", "metadata_contract"))
    else:
        blockers.extend(_candidate_blockers(minimum_candidate))

    runtime_side_effects = value.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append(_blocker("missing_runtime_side_effects", "metadata_contract"))
    else:
        for key, flag_value in runtime_side_effects.items():
            if flag_value is not False:
                blockers.append(_blocker(f"runtime_side_effect_not_false:{key}", "side_effect"))

    for upstream_blocker in _safe_blockers(value.get("blockers")):
        blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "bridge_status"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_path_leak(value):
        blockers.append(_blocker("blocked_path_escape", "privacy"))

    return _dedupe_blockers(blockers)


def _candidate_blockers(candidate: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if candidate.get("model_input_kind") != MODEL_INPUT_KIND:
        blockers.append(_blocker("wrong_model_input_kind", "metadata_contract"))
    if candidate.get("human_review_required") is not True:
        blockers.append(_blocker("candidate_human_review_required_not_true", "metadata_contract"))
    if candidate.get("evidence_items_safe") != []:
        blockers.append(_blocker("candidate_evidence_items_safe_not_empty", "metadata_contract"))
    if candidate.get("coefficient_source") not in {None, "mock_default"}:
        blockers.append(_blocker("candidate_coefficient_source_not_mock_default", "metadata_contract"))
    if candidate.get("calibration_status") != "uncalibrated":
        blockers.append(_blocker("candidate_calibration_status_not_uncalibrated", "metadata_contract"))
    if candidate.get("empirical_validation") != "not_started":
        blockers.append(_blocker("candidate_empirical_validation_not_started", "metadata_contract"))
    return blockers


def _blocked_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return EXECUTED_STATUS
    reasons = {blocker["reason"] for blocker in blockers}
    categories = {blocker["category"] for blocker in blockers}
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if any(reason.startswith("bridge_status_not_ready") or reason.startswith("upstream_blocker") for reason in reasons):
        return BLOCKED_BRIDGE_STATUS
    if _safe_value(value, "bridge_status") == MANUAL_REVIEW_STATUS:
        return MANUAL_REVIEW_STATUS
    return BLOCKED_METADATA_STATUS


def _fixture_from_minimum_candidate(candidate: dict[str, Any], bridge: dict[str, Any]) -> dict[str, Any]:
    fixture_metadata = candidate.get("fixture_metadata") if isinstance(candidate.get("fixture_metadata"), dict) else {}
    sample_id = _safe_value(candidate, "sample_id") or _safe_package_name(bridge.get("package_name")) or "missing_sample_id"
    case_id = _safe_value(candidate, "case_id") or _safe_value(candidate, "case_id_hint") or _safe_value(bridge, "case_id_hint") or "missing_case_id"
    coverage_note = _safe_value(fixture_metadata, "coverage_note") or _safe_value(candidate, "scope_note") or "selected controlled package metadata only"
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": _safe_value(candidate, "candidate_id") or f"minimum_real_run_bridge_fixture_{_safe_identifier(sample_id)}",
            "case_id": case_id,
            "sample_id": sample_id,
            "fixture_role": "minimum_real_run_bridge_execution",
            "source_mode": MODEL_INPUT_KIND,
            "stage_id": _safe_value(fixture_metadata, "stage_id"),
            "coverage_note": coverage_note,
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": [],
        "content_aggregates": [],
        "influence_cores": [],
        "echo_boxes": [],
        "people_clusters": [],
        "response_strategy_candidates": [],
    }


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


def _safe_generated_run(value: dict[str, Any] | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return _safe_mapping(value)


def _safe_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    safe: dict[str, Any] = {}
    for key, nested_value in value.items():
        key_text = str(key)
        lowered = key_text.lower()
        if lowered in FORBIDDEN_FIELD_NAMES:
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
            safe[key_text] = [
                _safe_mapping(item) if isinstance(item, dict) else item
                for item in nested_value
                if not isinstance(item, str) or not _looks_like_private_or_absolute_path(item)
            ]
    return safe


def _safe_audit_refs(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    refs: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        safe_item = {
            str(key): str(nested_value)
            for key, nested_value in item.items()
            if isinstance(nested_value, str) and not _looks_like_private_or_absolute_path(nested_value)
        }
        if safe_item:
            refs.append(safe_item)
    return refs


def _safe_blockers(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    blockers: list[dict[str, str]] = []
    for item in value:
        if isinstance(item, dict):
            reason = _safe_value(item, "reason") or "blocked"
            category = _safe_value(item, "category") or "execution_blocker"
        else:
            reason = str(item)
            category = "execution_blocker"
        blockers.append({"reason": reason, "category": category})
    return blockers


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in (str(item).strip() for item in value) if item and not _looks_like_private_or_absolute_path(item)]


def _safe_package_name(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or "/" in stripped or "\\" in stripped or ":" in stripped:
        return None
    if _looks_like_private_or_absolute_path(stripped):
        return None
    return stripped


def _safe_value(mapping: dict[str, Any], key: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_like_private_or_absolute_path(stripped):
        return None
    return stripped


def _safe_label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


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
            if lowered in {"absolute_package_path", "collector_runtime_internal_path", "browser_profile_path", "profile_path"}:
                return True
            if isinstance(nested_value, str) and _looks_like_private_or_absolute_path(nested_value):
                return True
            if _has_path_leak(nested_value):
                return True
    elif isinstance(value, list):
        return any(_has_path_leak(item) for item in value)
    return False


def _looks_like_private_or_absolute_path(value: str) -> bool:
    lowered = value.lower()
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if ":/" in lowered or ":\\" in lowered:
        return True
    if lowered.startswith("\\\\") or lowered.startswith("/"):
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


def _execution_id(bridge_id: str | None) -> str:
    return f"minimum_real_run_bridge_execution_{_safe_identifier(bridge_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
