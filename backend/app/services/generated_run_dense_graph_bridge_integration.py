from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services import opinion_ecosystem_dense_graph_generated_run_integration as dense_integration


INTEGRATION_SCHEMA = "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
EXECUTION_SCHEMA = "sentigraph_minimum_real_run_bridge_execution_v0_1"
GENERATED_RUN_SCHEMA = "sentigraph_opinion_ecosystem_run_v0_1"
READY_EXECUTION_STATUS = "executed_local_minimum_real_run"
INPUT_SOURCE_KIND = "minimum_real_run_bridge_execution"
INTEGRATION_MODE = "controlled_backend_only_generated_run_dense_graph"

READY_STATUS = "integrated_backend_dense_graph_preview"
BLOCKED_GENERATED_RUN_STATUS = "blocked_generated_run_not_ready"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
MANUAL_REVIEW_STATUS = "manual_review_required"

REQUIRED_GENERATED_RUN_BOUNDARY_FLAGS = {
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "human_review_required",
    "no_auto_execute",
    "no_generated_public_response",
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
    "route_changed",
    "api_route_added",
    "frontend_integration_approved",
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

RISK_BLOCKER_MARKERS = {
    "privacy",
    "security",
    "path",
    "side_effect",
    "forbidden",
    "secret",
    "token",
    "cookie",
    "production",
    "public",
}

DOWNSTREAM_ALLOWED_ACTIONS = (
    "inspect_backend_dense_graph_preview",
    "validate_boundary_flags",
    "validate_runtime_side_effect_flags",
    "request_future_dense_graph_route_or_frontend_decision",
)

DOWNSTREAM_BLOCKED_ACTIONS = (
    "parse_evidence_rows",
    "read_original_package_rows",
    "write_evidence_layer",
    "create_production_case",
    "create_production_analysis_run",
    "add_api_route",
    "add_frontend_ui",
    "generate_report",
    "generate_b_end_report",
    "generate_sandbox_or_public_event",
    "generate_public_output",
    "publish",
    "send",
    "post",
    "execute",
)


def integrate_generated_run_with_dense_graph_from_execution(
    execution: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_execution = execution if isinstance(execution, dict) else {}
    blockers = _collect_blockers(safe_execution)
    status = _blocked_status(blockers, safe_execution)
    if blockers:
        return _integration_object(
            safe_execution,
            created_by=created_by,
            integration_status=status,
            dense_graph_executed=False,
            dense_graph_value=None,
            blockers=blockers,
        )

    generated_run = safe_execution.get("generated_run")
    fixture = _fixture_from_generated_run(generated_run if isinstance(generated_run, dict) else {}, safe_execution)
    dense_graph_value = dense_integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        fixture,
        sample_id=str(generated_run.get("sample_id") or safe_execution.get("package_name") or "missing_sample_id"),
        source_run_id=str(generated_run.get("run_id") or safe_execution.get("execution_id") or "missing_source_run_id"),
    )
    return _integration_object(
        safe_execution,
        created_by=created_by,
        integration_status=READY_STATUS,
        dense_graph_executed=True,
        dense_graph_value=dense_graph_value,
        blockers=[],
    )


def build_generated_run_dense_graph_bridge_integration(
    execution: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return integrate_generated_run_with_dense_graph_from_execution(execution, created_by=created_by)


def build_safe_generated_run_dense_graph_bridge_summary(integration: dict[str, Any]) -> dict[str, Any]:
    safe_integration = integration if isinstance(integration, dict) else {}
    dense_summary = safe_integration.get("dense_graph_summary")
    if not isinstance(dense_summary, dict):
        dense_summary = {}
    return {
        "schema": "sentigraph_generated_run_dense_graph_bridge_summary_v0_1",
        "integration_id": _safe_value(safe_integration, "integration_id"),
        "integration_schema": _safe_value(safe_integration, "integration_schema"),
        "integration_status": _safe_value(safe_integration, "integration_status"),
        "execution_id": _safe_value(safe_integration, "execution_id"),
        "bridge_id": _safe_value(safe_integration, "bridge_id"),
        "staging_candidate_id": _safe_value(safe_integration, "staging_candidate_id"),
        "provider_result_id": _safe_value(safe_integration, "provider_result_id"),
        "request_id": _safe_value(safe_integration, "request_id"),
        "package_name": _safe_package_name(safe_integration.get("package_name")),
        "dense_graph_executed": bool(safe_integration.get("dense_graph_executed")),
        "frontend_ready": bool(dense_summary.get("frontend_ready", False)),
        "route_ready": bool(dense_summary.get("route_ready", False)),
        "production_ready": bool(dense_summary.get("production_ready", False)),
        "frontend_integration_approved": False,
        "route_changed": False,
        "api_route_added": False,
        "report_generated": False,
        "sandbox_public_event_generated": False,
        "public_route_created": False,
        "path_exposed": False,
        "path_reference": "generated_run_dense_graph_bridge_summary",
        "warnings": _safe_string_list(safe_integration.get("warnings")),
        "blockers": _safe_blockers(safe_integration.get("blockers")),
    }


def _integration_object(
    execution: dict[str, Any],
    *,
    created_by: str,
    integration_status: str,
    dense_graph_executed: bool,
    dense_graph_value: dict[str, Any] | None,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "integration_id": _integration_id(_safe_value(execution, "execution_id")),
        "integration_schema": INTEGRATION_SCHEMA,
        "integration_status": integration_status,
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "execution_id": _safe_value(execution, "execution_id"),
        "bridge_id": _safe_value(execution, "bridge_id"),
        "staging_candidate_id": _safe_value(execution, "staging_candidate_id"),
        "provider_result_id": _safe_value(execution, "provider_result_id"),
        "request_id": _safe_value(execution, "request_id"),
        "case_id_hint": _safe_value(execution, "case_id_hint"),
        "package_name": _safe_package_name(execution.get("package_name")),
        "input_source_kind": INPUT_SOURCE_KIND,
        "integration_mode": INTEGRATION_MODE,
        "generated_run_schema": _generated_run_schema(execution),
        "dense_graph_executed": bool(dense_graph_executed),
        "frontend_integration_approved": False,
        "route_changed": False,
        "api_route_added": False,
        "report_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "dense_graph_integration": _safe_mapping(dense_graph_value) if dense_graph_value is not None else None,
        "dense_graph_summary": _dense_graph_summary(dense_graph_value),
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _safe_string_list(execution.get("warnings")),
        "blockers": _safe_blockers(blockers),
        "audit_refs": _safe_audit_refs(execution.get("audit_refs")),
        "downstream_allowed_actions": list(DOWNSTREAM_ALLOWED_ACTIONS),
        "downstream_blocked_actions": list(DOWNSTREAM_BLOCKED_ACTIONS),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "execution_id") is None:
        blockers.append(_blocker("missing_execution_id", "metadata_contract"))
    if _safe_value(value, "execution_schema") != EXECUTION_SCHEMA:
        blockers.append(_blocker("wrong_execution_schema", "metadata_contract"))
    if _safe_value(value, "execution_status") != READY_EXECUTION_STATUS:
        blockers.append(_blocker("execution_status_not_ready", "generated_run_status"))
    if value.get("minimum_real_run_executed") is not True:
        blockers.append(_blocker("minimum_real_run_not_executed", "metadata_contract"))
    if value.get("dense_graph_called") is not False:
        blockers.append(_blocker("dense_graph_already_called", "side_effect"))
    if value.get("metadata_only") is not True:
        blockers.append(_blocker("metadata_only_not_true", "metadata_contract"))
    if value.get("evidence_rows_parsed") is not False:
        blockers.append(_blocker("evidence_rows_parsed_not_false", "side_effect"))

    generated_run = value.get("generated_run")
    if not isinstance(generated_run, dict):
        blockers.append(_blocker("missing_generated_run", "metadata_contract"))
    else:
        blockers.extend(_generated_run_blockers(generated_run))

    runtime_side_effects = value.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append(_blocker("missing_runtime_side_effects", "metadata_contract"))
    else:
        for key, flag_value in runtime_side_effects.items():
            if flag_value is not False:
                blockers.append(_blocker(f"runtime_side_effect_not_false:{key}", "side_effect"))

    for upstream_blocker in _safe_blockers(value.get("blockers")):
        reason = upstream_blocker["reason"].lower()
        category = upstream_blocker["category"].lower()
        if any(marker in reason or marker in category for marker in RISK_BLOCKER_MARKERS):
            blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "generated_run_status"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_path_leak(value):
        blockers.append(_blocker("blocked_path_escape", "privacy"))

    return _dedupe_blockers(blockers)


def _generated_run_blockers(generated_run: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if generated_run.get("run_schema") != GENERATED_RUN_SCHEMA:
        blockers.append(_blocker("wrong_generated_run_schema", "metadata_contract"))
    if generated_run.get("human_review_required") is not True:
        blockers.append(_blocker("generated_run_human_review_required_not_true", "metadata_contract"))
    if generated_run.get("coefficient_source") not in {None, "mock_default"}:
        blockers.append(_blocker("generated_run_coefficient_source_not_mock_default", "metadata_contract"))
    if generated_run.get("calibration_status") != "uncalibrated":
        blockers.append(_blocker("generated_run_calibration_status_not_uncalibrated", "metadata_contract"))
    if generated_run.get("empirical_validation") != "not_started":
        blockers.append(_blocker("generated_run_empirical_validation_not_started", "metadata_contract"))

    boundary_flags = generated_run.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        blockers.append(_blocker("missing_generated_run_boundary_flags", "metadata_contract"))
    else:
        for flag in sorted(REQUIRED_GENERATED_RUN_BOUNDARY_FLAGS):
            if boundary_flags.get(flag) is not True:
                blockers.append(_blocker(f"generated_run_boundary_flag_not_true:{flag}", "metadata_contract"))

    runtime_side_effects = generated_run.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append(_blocker("missing_generated_run_runtime_side_effects", "metadata_contract"))
    else:
        for key, flag_value in runtime_side_effects.items():
            if flag_value is not False:
                blockers.append(_blocker(f"generated_run_runtime_side_effect_not_false:{key}", "side_effect"))

    for upstream_blocker in _safe_blockers(generated_run.get("blockers")):
        reason = upstream_blocker["reason"].lower()
        category = upstream_blocker["category"].lower()
        if any(marker in reason or marker in category for marker in RISK_BLOCKER_MARKERS):
            blockers.append(_blocker(f"generated_run_blocker:{upstream_blocker['reason']}", "generated_run_status"))
    return blockers


def _blocked_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return READY_STATUS
    reasons = {blocker["reason"] for blocker in blockers}
    categories = {blocker["category"] for blocker in blockers}
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if any(
        reason.startswith("execution_status_not_ready")
        or reason.startswith("upstream_blocker")
        or reason.startswith("generated_run_blocker")
        for reason in reasons
    ):
        return BLOCKED_GENERATED_RUN_STATUS
    if _safe_value(value, "execution_status") == MANUAL_REVIEW_STATUS:
        return MANUAL_REVIEW_STATUS
    return BLOCKED_METADATA_STATUS


def _fixture_from_generated_run(generated_run: dict[str, Any], execution: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": f"generated_run_dense_graph_bridge_fixture_{_safe_identifier(generated_run.get('run_id'))}",
            "case_id": _safe_value(generated_run, "case_id") or _safe_value(execution, "case_id_hint") or "missing_case_id",
            "sample_id": _safe_value(generated_run, "sample_id") or _safe_package_name(execution.get("package_name")) or "missing_sample_id",
            "fixture_role": "generated_run_dense_graph_bridge",
            "source_mode": "minimum_real_run_bridge_execution",
            "coverage_note": _safe_value(generated_run, "input_scope_note") or "selected generated run only",
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": [],
        "content_aggregates": _module_output(generated_run, "ContentAggregate"),
        "influence_cores": _module_output(generated_run, "InfluenceCore"),
        "echo_boxes": _module_output(generated_run, "EchoBox"),
        "people_clusters": _module_output(generated_run, "PeopleCluster"),
        "response_strategy_candidates": _module_output(generated_run, "ResponseStrategyComparisonV01"),
    }


def _module_output(generated_run: dict[str, Any], key: str) -> list[dict[str, Any]]:
    module_outputs = generated_run.get("module_outputs")
    if not isinstance(module_outputs, dict):
        return []
    value = module_outputs.get(key)
    if not isinstance(value, list):
        return []
    return [_safe_mapping(item) for item in value if isinstance(item, dict)]


def _dense_graph_summary(value: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(value, dict):
        return _empty_dense_graph_summary()
    summary = value.get("integration_summary")
    if not isinstance(summary, dict):
        return _empty_dense_graph_summary()
    return {
        "dense_graph_attached": bool(summary.get("dense_graph_attached")),
        "people_cluster_proxy_count": _safe_int(summary.get("people_cluster_proxy_count")),
        "influence_core_proxy_count": _safe_int(summary.get("influence_core_proxy_count")),
        "content_aggregate_proxy_count": _safe_int(summary.get("content_aggregate_proxy_count")),
        "echobox_proxy_count": _safe_int(summary.get("echobox_proxy_count")),
        "edge_count": _safe_int(summary.get("edge_count")),
        "timeline_bucket_count": _safe_int(summary.get("timeline_bucket_count")),
        "recommended_visualization_mode": str(summary.get("recommended_visualization_mode") or "dense_sandbox_proxy_graph"),
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
    }


def _empty_dense_graph_summary() -> dict[str, Any]:
    return {
        "dense_graph_attached": False,
        "people_cluster_proxy_count": 0,
        "influence_core_proxy_count": 0,
        "content_aggregate_proxy_count": 0,
        "echobox_proxy_count": 0,
        "edge_count": 0,
        "timeline_bucket_count": 0,
        "recommended_visualization_mode": "dense_sandbox_proxy_graph",
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "selected_sample_only": True,
        "controlled_generated_run_only": True,
        "metadata_only_upstream": True,
        "anonymous_aggregate_only": True,
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
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
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


def _safe_mapping(value: Any, path: str = "") -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    safe: dict[str, Any] = {}
    for key, nested_value in value.items():
        key_text = str(key)
        lowered = key_text.lower()
        child_path = f"{path}.{lowered}" if path else lowered
        if lowered in FORBIDDEN_FIELD_NAMES and not _is_allowed_false_flag(child_path, lowered, nested_value):
            continue
        if isinstance(nested_value, str):
            if _looks_like_private_or_absolute_path(nested_value):
                continue
            safe[key_text] = nested_value
        elif isinstance(nested_value, (int, float, bool)) or nested_value is None:
            safe[key_text] = nested_value
        elif isinstance(nested_value, dict):
            safe[key_text] = _safe_mapping(nested_value, child_path)
        elif isinstance(nested_value, list):
            safe[key_text] = [
                _safe_mapping(item, child_path) if isinstance(item, dict) else item
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
            category = _safe_value(item, "category") or "integration_blocker"
        else:
            reason = str(item)
            category = "integration_blocker"
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


def _find_forbidden_fields(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered = key_text.lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if lowered in FORBIDDEN_FIELD_NAMES and not _is_allowed_false_flag(child_path, lowered, nested_value):
                found.add(str(key))
            found.update(_find_forbidden_fields(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item, path))
    return found


def _find_requested_side_effects(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered = key_text.lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if lowered in REQUESTED_SIDE_EFFECT_FIELDS and _truthy(nested_value) and not _is_allowed_false_flag(child_path, lowered, nested_value):
                found.add(str(key))
            found.update(_find_requested_side_effects(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_requested_side_effects(item, path))
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


def _is_allowed_false_flag(path: str, normalized_field: str, value: Any) -> bool:
    if value is not False:
        return False
    return path.endswith(f"runtime_side_effects.{normalized_field}") or path.endswith(f"boundary_flags.{normalized_field}")


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


def _safe_int(value: Any) -> int:
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return 0


def _generated_run_schema(execution: dict[str, Any]) -> str | None:
    generated_run = execution.get("generated_run")
    if not isinstance(generated_run, dict):
        return None
    value = generated_run.get("run_schema")
    return str(value) if isinstance(value, str) and value else None


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


def _integration_id(execution_id: str | None) -> str:
    return f"generated_run_dense_graph_bridge_integration_{_safe_identifier(execution_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
