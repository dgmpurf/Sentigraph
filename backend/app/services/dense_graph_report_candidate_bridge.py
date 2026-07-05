from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


REPORT_CANDIDATE_SCHEMA = "sentigraph_dense_graph_report_candidate_v0_1"
INPUT_INTEGRATION_SCHEMA = "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
READY_INTEGRATION_STATUS = "integrated_backend_dense_graph_preview"
INPUT_SOURCE_KIND = "generated_run_dense_graph_bridge_integration"
CANDIDATE_MODE = "backend_only_local_report_candidate"

CANDIDATE_READY_STATUS = "candidate_ready"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
MANUAL_REVIEW_STATUS = "manual_review_required"

REQUIRED_BOUNDARY_TRUE_FLAGS = {
    "selected_sample_only",
    "human_review_required",
}

READINESS_FALSE_FIELDS = {
    "frontend_ready",
    "route_ready",
    "production_ready",
}

OPTIONAL_FALSE_FIELDS = {
    "customer_ready",
}

REQUIRED_FALSE_FIELDS = {
    "frontend_integration_approved",
    "route_changed",
    "api_route_added",
    "report_generated",
    "sandbox_public_event_generated",
    "generated_response_text",
    "public_route_created",
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
    "public_url",
    "signed_url",
    "download_url",
    "file_byte_route",
    "pdf_path",
    "markdown_report_path",
    "briefing_deck_path",
    "zip_path",
    "package_path",
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
    "final_report_created",
    "create_final_report",
    "final_summary_report_requested",
    "report_generated",
    "generate_report",
    "b_end_report_runtime_generated",
    "generate_b_end_report",
    "sandbox_public_event_generated",
    "generate_sandbox_public_event",
    "export_artifact_created",
    "create_export_artifact",
    "generated_pdf",
    "generated_markdown_report",
    "generated_briefing_deck",
    "zip_package_created",
    "download_package_created",
    "file_byte_route_created",
    "external_delivery_performed",
    "generated_response_text",
    "public_route_created",
    "route_changed",
    "api_route_added",
    "frontend_integration_approved",
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
    "real_provider",
}

DOWNSTREAM_ALLOWED_ACTIONS = (
    "inspect_local_report_candidate_summary",
    "validate_boundary_flags",
    "validate_runtime_side_effect_flags",
    "request_future_report_candidate_to_final_report_decision",
)

DOWNSTREAM_BLOCKED_ACTIONS = (
    "create_final_summary_report",
    "generate_final_report",
    "generate_b_end_report",
    "generate_sandbox_or_public_event",
    "create_export_artifact",
    "generate_pdf",
    "generate_markdown_report",
    "generate_briefing_deck",
    "create_zip_or_download_package",
    "create_public_url",
    "create_signed_url",
    "create_file_byte_route",
    "perform_external_delivery",
    "write_evidence_layer",
    "create_production_case",
    "create_production_analysis_run",
    "add_api_route",
    "add_frontend_ui",
    "generate_public_response",
    "publish",
    "send",
    "post",
    "execute",
)


def build_dense_graph_report_candidate_from_integration(
    integration: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_integration = integration if isinstance(integration, dict) else {}
    blockers = _collect_blockers(safe_integration)
    status = _candidate_status(blockers, safe_integration)
    return _candidate_object(
        safe_integration,
        created_by=created_by,
        report_candidate_status=status,
        report_candidate_created=not blockers,
        blockers=blockers,
    )


def create_dense_graph_report_candidate_from_integration(
    integration: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return build_dense_graph_report_candidate_from_integration(integration, created_by=created_by)


def build_safe_dense_graph_report_candidate_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    safe_candidate = candidate if isinstance(candidate, dict) else {}
    report_summary = safe_candidate.get("report_candidate_summary")
    if not isinstance(report_summary, dict):
        report_summary = {}
    return {
        "schema": "sentigraph_dense_graph_report_candidate_summary_v0_1",
        "report_candidate_id": _safe_value(safe_candidate, "report_candidate_id"),
        "report_candidate_schema": _safe_value(safe_candidate, "report_candidate_schema"),
        "report_candidate_status": _safe_value(safe_candidate, "report_candidate_status"),
        "integration_id": _safe_value(safe_candidate, "integration_id"),
        "request_id": _safe_value(safe_candidate, "request_id"),
        "package_name": _safe_package_name(safe_candidate.get("package_name")),
        "report_candidate_created": bool(safe_candidate.get("report_candidate_created")),
        "candidate_scope": str(report_summary.get("candidate_scope") or "selected_sample_only_dense_graph_preview"),
        "human_review_required": bool(report_summary.get("human_review_required", True)),
        "final_report_ready": bool(report_summary.get("final_report_ready", False)),
        "export_ready": bool(report_summary.get("export_ready", False)),
        "public_ready": bool(report_summary.get("public_ready", False)),
        "b_end_runtime_ready": bool(report_summary.get("b_end_runtime_ready", False)),
        "sandbox_public_event_ready": bool(report_summary.get("sandbox_public_event_ready", False)),
        "warnings": _safe_string_list(safe_candidate.get("warnings")),
        "blockers": _safe_blockers(safe_candidate.get("blockers")),
    }


def _candidate_object(
    integration: dict[str, Any],
    *,
    created_by: str,
    report_candidate_status: str,
    report_candidate_created: bool,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    dense_graph_summary = _safe_dense_graph_summary(integration.get("dense_graph_summary"))
    return {
        "report_candidate_id": _candidate_id(_safe_value(integration, "integration_id")),
        "report_candidate_schema": REPORT_CANDIDATE_SCHEMA,
        "report_candidate_status": report_candidate_status,
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "input_source_kind": INPUT_SOURCE_KIND,
        "candidate_mode": CANDIDATE_MODE,
        "integration_id": _safe_value(integration, "integration_id"),
        "execution_id": _safe_value(integration, "execution_id"),
        "bridge_id": _safe_value(integration, "bridge_id"),
        "staging_candidate_id": _safe_value(integration, "staging_candidate_id"),
        "provider_result_id": _safe_value(integration, "provider_result_id"),
        "request_id": _safe_value(integration, "request_id"),
        "case_id_hint": _safe_value(integration, "case_id_hint"),
        "package_name": _safe_package_name(integration.get("package_name")),
        "generated_run_schema": _safe_value(integration, "generated_run_schema"),
        "dense_graph_integration_schema": _safe_value(integration, "integration_schema"),
        "dense_graph_summary": dense_graph_summary,
        "report_candidate_summary": _report_candidate_summary(dense_graph_summary, integration),
        "report_candidate_created": bool(report_candidate_created),
        "final_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "export_artifact_created": False,
        "generated_response_text": False,
        "public_route_created": False,
        "frontend_integration_approved": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _safe_string_list(integration.get("warnings")),
        "blockers": _safe_blockers(blockers),
        "audit_refs": _safe_audit_refs(integration.get("audit_refs")),
        "downstream_allowed_actions": list(DOWNSTREAM_ALLOWED_ACTIONS),
        "downstream_blocked_actions": list(DOWNSTREAM_BLOCKED_ACTIONS),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "integration_id") is None:
        blockers.append(_blocker("missing_integration_id", "metadata_contract"))
    if _safe_value(value, "integration_schema") != INPUT_INTEGRATION_SCHEMA:
        blockers.append(_blocker("wrong_integration_schema", "metadata_contract"))
    if _safe_value(value, "integration_status") != READY_INTEGRATION_STATUS:
        blockers.append(_blocker("integration_status_not_ready", "metadata_contract"))
    if value.get("dense_graph_executed") is not True:
        blockers.append(_blocker("dense_graph_not_executed", "metadata_contract"))
    if not isinstance(value.get("dense_graph_integration"), dict) or not value.get("dense_graph_integration"):
        blockers.append(_blocker("missing_dense_graph_integration", "metadata_contract"))
    dense_graph_summary = value.get("dense_graph_summary")
    if not isinstance(dense_graph_summary, dict) or not dense_graph_summary:
        blockers.append(_blocker("missing_dense_graph_summary", "metadata_contract"))
    else:
        for field in sorted(READINESS_FALSE_FIELDS):
            if dense_graph_summary.get(field) is not False:
                blockers.append(_blocker(f"dense_graph_summary_not_false:{field}", "side_effect"))
        for field in sorted(OPTIONAL_FALSE_FIELDS):
            if field in dense_graph_summary and dense_graph_summary.get(field) is not False:
                blockers.append(_blocker(f"dense_graph_summary_not_false:{field}", "side_effect"))

    for field in sorted(REQUIRED_FALSE_FIELDS):
        if value.get(field) is not False:
            blockers.append(_blocker(f"integration_flag_not_false:{field}", "side_effect"))
    for field in sorted(OPTIONAL_FALSE_FIELDS):
        if field in value and value.get(field) is not False:
            blockers.append(_blocker(f"integration_flag_not_false:{field}", "side_effect"))

    boundary_flags = value.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        blockers.append(_blocker("missing_boundary_flags", "metadata_contract"))
    else:
        for flag in sorted(REQUIRED_BOUNDARY_TRUE_FLAGS):
            if boundary_flags.get(flag) is not True:
                blockers.append(_blocker(f"boundary_flag_not_true:{flag}", "metadata_contract"))

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
            blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "metadata_contract"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_sensitive_string(value):
        blockers.append(_blocker("blocked_sensitive_string_or_path", "privacy"))

    return _dedupe_blockers(blockers)


def _candidate_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return CANDIDATE_READY_STATUS
    categories = {blocker["category"] for blocker in blockers}
    reasons = {blocker["reason"] for blocker in blockers}
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if _safe_value(value, "integration_status") == MANUAL_REVIEW_STATUS:
        return MANUAL_REVIEW_STATUS
    return BLOCKED_METADATA_STATUS


def _report_candidate_summary(dense_graph_summary: dict[str, Any], integration: dict[str, Any]) -> dict[str, Any]:
    warning_summary = _safe_string_list(integration.get("warnings"))
    blocker_summary = _safe_blockers(integration.get("blockers"))
    return {
        "candidate_title": "Dense graph preview report candidate",
        "candidate_scope": "selected_sample_only_dense_graph_preview",
        "candidate_sections": [
            "scope_and_boundaries",
            "dense_graph_proxy_summary",
            "coverage_limitations",
            "human_review_required",
            "not_final_report",
        ],
        "dense_graph_proxy_counts": {
            "people_cluster_proxy_count": _safe_int(dense_graph_summary.get("people_cluster_proxy_count")),
            "influence_core_proxy_count": _safe_int(dense_graph_summary.get("influence_core_proxy_count")),
            "content_aggregate_proxy_count": _safe_int(dense_graph_summary.get("content_aggregate_proxy_count")),
            "echobox_proxy_count": _safe_int(dense_graph_summary.get("echobox_proxy_count")),
            "edge_count": _safe_int(dense_graph_summary.get("edge_count")),
            "timeline_bucket_count": _safe_int(dense_graph_summary.get("timeline_bucket_count")),
        },
        "coverage_limitations": [
            "selected_sample_only",
            "not_full_web",
            "not_full_platform",
            "not_official_verification",
            "not_causal_proof",
            "not_prediction",
        ],
        "warning_summary": warning_summary,
        "blocker_summary": blocker_summary,
        "human_review_required": True,
        "final_report_ready": False,
        "export_ready": False,
        "public_ready": False,
        "b_end_runtime_ready": False,
        "sandbox_public_event_ready": False,
    }


def _safe_dense_graph_summary(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return _empty_dense_graph_summary()
    return {
        "dense_graph_attached": bool(value.get("dense_graph_attached")),
        "people_cluster_proxy_count": _safe_int(value.get("people_cluster_proxy_count")),
        "influence_core_proxy_count": _safe_int(value.get("influence_core_proxy_count")),
        "content_aggregate_proxy_count": _safe_int(value.get("content_aggregate_proxy_count")),
        "echobox_proxy_count": _safe_int(value.get("echobox_proxy_count")),
        "edge_count": _safe_int(value.get("edge_count")),
        "timeline_bucket_count": _safe_int(value.get("timeline_bucket_count")),
        "recommended_visualization_mode": str(value.get("recommended_visualization_mode") or "dense_sandbox_proxy_graph"),
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
        "dense_graph_preview_derived": True,
        "backend_only_local_candidate": True,
        "metadata_only_upstream": True,
        "anonymous_aggregate_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "not_final_report": True,
        "not_b_end_report_runtime": True,
        "not_sandbox_public_event_runtime": True,
        "not_export_artifact": True,
        "human_review_required": True,
        "no_auto_execute": True,
        "no_generated_public_response": True,
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
        "export_ready": False,
        "public_ready": False,
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
        "created_final_report": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "created_export_artifact": False,
        "generated_pdf": False,
        "generated_markdown_report": False,
        "generated_briefing_deck": False,
        "generated_response_text": False,
        "created_public_route": False,
        "generated_public_url": False,
        "generated_signed_url": False,
        "created_download_package": False,
        "performed_external_delivery": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


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
            if isinstance(nested_value, str) and not _looks_like_sensitive_string(nested_value)
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
            category = _safe_value(item, "category") or "report_candidate_blocker"
        else:
            reason = str(item)
            category = "report_candidate_blocker"
        blockers.append({"reason": reason, "category": category})
    return blockers


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in (str(item).strip() for item in value) if item and not _looks_like_sensitive_string(item)]


def _safe_package_name(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or "/" in stripped or "\\" in stripped or ":" in stripped:
        return None
    if _looks_like_sensitive_string(stripped):
        return None
    return stripped


def _safe_value(mapping: dict[str, Any], key: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_like_sensitive_string(stripped):
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


def _has_sensitive_string(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            if lowered in {
                "absolute_package_path",
                "collector_runtime_internal_path",
                "browser_profile_path",
                "profile_path",
                "public_url",
                "signed_url",
                "download_url",
                "pdf_path",
                "markdown_report_path",
                "briefing_deck_path",
                "zip_path",
                "package_path",
            }:
                return True
            if _has_sensitive_string(nested_value):
                return True
    elif isinstance(value, list):
        return any(_has_sensitive_string(item) for item in value)
    elif isinstance(value, str):
        return _looks_like_sensitive_string(value)
    return False


def _looks_like_sensitive_string(value: str) -> bool:
    lowered = value.lower()
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if "http://" in lowered or "https://" in lowered:
        return True
    if ":/" in lowered or ":\\" in lowered:
        return True
    if lowered.startswith("\\\\") or lowered.startswith("/"):
        return True
    return False


def _is_allowed_false_flag(path: str, normalized_field: str, value: Any) -> bool:
    if value is not False:
        return False
    return (
        not path
        or path == normalized_field
        or path.endswith(f"runtime_side_effects.{normalized_field}")
        or path.endswith(f"boundary_flags.{normalized_field}")
    )


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


def _candidate_id(integration_id: str | None) -> str:
    return f"dense_graph_report_candidate_{_safe_identifier(integration_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
