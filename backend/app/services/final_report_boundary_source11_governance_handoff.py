from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


SOURCE11_GOVERNANCE_HANDOFF_SCHEMA = "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
INPUT_FINAL_REPORT_BOUNDARY_SCHEMA = "sentigraph_report_candidate_final_report_boundary_v0_1"
INPUT_FINAL_REPORT_BOUNDARY_STATUS = "boundary_ready"
INPUT_SOURCE_KIND = "final_report_boundary"
INPUT_BOUNDARY_SOURCE_KIND = "dense_graph_report_candidate"
INPUT_BOUNDARY_MODE = "backend_only_local_final_report_boundary"
INPUT_REPORT_CANDIDATE_SCHEMA = "sentigraph_dense_graph_report_candidate_v0_1"
INPUT_REPORT_CANDIDATE_STATUS = "candidate_ready"
INPUT_DENSE_GRAPH_INTEGRATION_SCHEMA = "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
GENERATED_RUN_SCHEMA = "sentigraph_opinion_ecosystem_run_v0_1"
HANDOFF_MODE = "backend_only_local_source11_governance_handoff"

HANDOFF_READY_STATUS = "handoff_ready_for_manual_source11_governance_review"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
BLOCKED_SOURCE11_RUNTIME_STATUS = "blocked_source11_runtime_request"
MANUAL_REVIEW_STATUS = "manual_review_required"

REQUIRED_BOUNDARY_TRUE_FLAGS = {
    "selected_sample_only",
    "human_review_required",
}

READINESS_FALSE_FIELDS = {
    "route_ready",
    "frontend_ready",
    "production_ready",
    "export_ready",
    "public_ready",
    "customer_ready",
}

REQUIRED_FALSE_FIELDS = {
    "source11_final_summary_report_runtime_used",
    "final_summary_report_created",
    "final_report_created",
    "b_end_report_runtime_generated",
    "sandbox_public_event_generated",
    "export_artifact_created",
    "download_package_created",
    "public_access_created",
    "external_delivery_performed",
    "generated_response_text",
    "public_route_created",
    "frontend_integration_approved",
}

SOURCE11_RUNTIME_REQUEST_FIELDS = {
    "source11_final_summary_report_runtime_used",
    "source11_runtime_called",
    "source11_runtime_invoked_now",
    "use_source11_runtime",
    "call_source11_runtime",
    "create_final_summary_report",
    "final_summary_report_created",
    "final_summary_report_created_now",
    "source11_final_summary_report_id",
}

REQUESTED_SIDE_EFFECT_FIELDS = {
    "final_report_created",
    "create_final_report",
    "final_report_artifact_created",
    "export_artifact_created",
    "create_export_artifact",
    "export_gate_invoked_now",
    "download_package_created",
    "create_download_package",
    "public_access_created",
    "create_public_access",
    "external_delivery_performed",
    "perform_external_delivery",
    "b_end_report_runtime_generated",
    "generate_b_end_report",
    "sandbox_public_event_generated",
    "generate_sandbox_public_event",
    "generated_response_text",
    "public_route_created",
    "route_changed",
    "api_route_added",
    "frontend_integration_approved",
    "route_ready",
    "frontend_ready",
    "production_ready",
    "export_ready",
    "public_ready",
    "customer_ready",
    "evidence_layer_write",
    "write_evidence_layer",
    "production_case_created",
    "create_production_case",
    "production_analysis_run_created",
    "create_production_analysis_run",
    "analysis_run_created",
    "evidence_rows_parsed",
    "evidence_row_parsing_requested",
    "parse_evidence_rows",
    "called_real_api",
    "called_real_llm",
    "ran_collector",
    "fetched_url",
    "scraped_page",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
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
    "external_delivery_target",
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


def build_final_report_boundary_source11_governance_handoff(
    final_report_boundary: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_boundary = final_report_boundary if isinstance(final_report_boundary, dict) else {}
    blockers = _collect_blockers(safe_boundary)
    status = _handoff_status(blockers, safe_boundary)
    return _handoff_object(
        safe_boundary,
        created_by=created_by,
        source11_governance_handoff_status=status,
        source11_governance_handoff_created=not blockers,
        blockers=blockers,
    )


def create_final_report_boundary_source11_governance_handoff(
    final_report_boundary: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return build_final_report_boundary_source11_governance_handoff(final_report_boundary, created_by=created_by)


def build_safe_final_report_boundary_source11_governance_handoff_summary(
    handoff: dict[str, Any],
) -> dict[str, Any]:
    safe_handoff = handoff if isinstance(handoff, dict) else {}
    downstream_policy = safe_handoff.get("downstream_policy") if isinstance(safe_handoff.get("downstream_policy"), dict) else {}
    return {
        "schema": "sentigraph_final_report_boundary_source11_governance_handoff_summary_v0_1",
        "source11_governance_handoff_id": _safe_value(safe_handoff, "source11_governance_handoff_id"),
        "source11_governance_handoff_schema": _safe_value(safe_handoff, "source11_governance_handoff_schema"),
        "source11_governance_handoff_status": _safe_value(safe_handoff, "source11_governance_handoff_status"),
        "source11_governance_handoff_created": bool(safe_handoff.get("source11_governance_handoff_created")),
        "final_report_boundary_id": _safe_value(safe_handoff, "final_report_boundary_id"),
        "report_candidate_id": _safe_value(safe_handoff, "report_candidate_id"),
        "request_id": _safe_value(safe_handoff, "request_id"),
        "package_name": _safe_package_name(safe_handoff.get("package_name")),
        "human_review_required": True,
        "source11_manual_review_ready": bool(downstream_policy.get("source11_manual_review_ready")),
        "source11_runtime_ready": bool(downstream_policy.get("source11_runtime_ready")),
        "final_summary_report_created": bool(safe_handoff.get("final_summary_report_created")),
        "export_ready": bool(safe_handoff.get("export_ready")),
        "public_ready": bool(safe_handoff.get("public_ready")),
        "customer_ready": bool(safe_handoff.get("customer_ready")),
        "warnings": _safe_string_list(safe_handoff.get("warnings")),
        "blockers": _safe_blockers(safe_handoff.get("blockers")),
    }


def _handoff_object(
    final_report_boundary: dict[str, Any],
    *,
    created_by: str,
    source11_governance_handoff_status: str,
    source11_governance_handoff_created: bool,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    final_report_boundary_id = _safe_value(final_report_boundary, "final_report_boundary_id")
    return {
        "source11_governance_handoff_id": _handoff_id(final_report_boundary_id),
        "source11_governance_handoff_schema": SOURCE11_GOVERNANCE_HANDOFF_SCHEMA,
        "source11_governance_handoff_status": source11_governance_handoff_status,
        "source11_governance_handoff_created": bool(source11_governance_handoff_created),
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "final_report_boundary_id": final_report_boundary_id,
        "report_candidate_id": _safe_value(final_report_boundary, "report_candidate_id"),
        "integration_id": _safe_value(final_report_boundary, "integration_id"),
        "execution_id": _safe_value(final_report_boundary, "execution_id"),
        "bridge_id": _safe_value(final_report_boundary, "bridge_id"),
        "staging_candidate_id": _safe_value(final_report_boundary, "staging_candidate_id"),
        "provider_result_id": _safe_value(final_report_boundary, "provider_result_id"),
        "request_id": _safe_value(final_report_boundary, "request_id"),
        "case_id_hint": _safe_value(final_report_boundary, "case_id_hint"),
        "package_name": _safe_package_name(final_report_boundary.get("package_name")),
        "input_source_kind": INPUT_SOURCE_KIND,
        "handoff_mode": HANDOFF_MODE,
        "final_report_boundary_schema": _safe_value(final_report_boundary, "final_report_boundary_schema")
        or INPUT_FINAL_REPORT_BOUNDARY_SCHEMA,
        "final_report_boundary_status": _safe_value(final_report_boundary, "final_report_boundary_status")
        or BLOCKED_METADATA_STATUS,
        "report_candidate_schema": _safe_value(final_report_boundary, "report_candidate_schema"),
        "report_candidate_status": _safe_value(final_report_boundary, "report_candidate_status"),
        "dense_graph_integration_schema": _safe_value(final_report_boundary, "dense_graph_integration_schema"),
        "generated_run_schema": _safe_value(final_report_boundary, "generated_run_schema"),
        "selected_sample_scope_note": "selected public sample only; not full-web, not full-platform, not full-thread",
        "final_report_boundary_summary": _safe_final_report_boundary_summary(final_report_boundary),
        "source11_governance_review_summary": _source11_governance_review_summary(
            source11_governance_handoff_created
        ),
        "source11_compatibility_notes": _source11_compatibility_notes(),
        "governance_handoff_limitations": _governance_handoff_limitations(),
        "warnings": _warnings(final_report_boundary),
        "blockers": _safe_blockers(blockers),
        "human_review_status": "required",
        "human_review_required": True,
        **_output_false_flags(),
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "audit_refs": _safe_audit_refs(final_report_boundary.get("audit_refs")),
        "downstream_policy": _downstream_policy(source11_governance_handoff_created),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "final_report_boundary_id") is None:
        blockers.append(_blocker("missing_final_report_boundary_id", "metadata_contract"))
    if _safe_value(value, "final_report_boundary_schema") != INPUT_FINAL_REPORT_BOUNDARY_SCHEMA:
        blockers.append(_blocker("wrong_final_report_boundary_schema", "metadata_contract"))
    if _safe_value(value, "final_report_boundary_status") != INPUT_FINAL_REPORT_BOUNDARY_STATUS:
        blockers.append(_blocker("final_report_boundary_status_not_ready", "metadata_contract"))
    if _safe_value(value, "input_source_kind") != INPUT_BOUNDARY_SOURCE_KIND:
        blockers.append(_blocker("wrong_final_report_boundary_input_source_kind", "metadata_contract"))
    if _safe_value(value, "boundary_mode") != INPUT_BOUNDARY_MODE:
        blockers.append(_blocker("wrong_final_report_boundary_mode", "metadata_contract"))
    if value.get("final_report_boundary_created") is not True:
        blockers.append(_blocker("final_report_boundary_not_created", "metadata_contract"))
    if _safe_value(value, "report_candidate_schema") != INPUT_REPORT_CANDIDATE_SCHEMA:
        blockers.append(_blocker("wrong_report_candidate_schema", "metadata_contract"))
    if _safe_value(value, "report_candidate_status") != INPUT_REPORT_CANDIDATE_STATUS:
        blockers.append(_blocker("report_candidate_status_not_ready", "metadata_contract"))
    if _safe_value(value, "dense_graph_integration_schema") != INPUT_DENSE_GRAPH_INTEGRATION_SCHEMA:
        blockers.append(_blocker("wrong_dense_graph_integration_schema", "metadata_contract"))
    if _safe_value(value, "generated_run_schema") != GENERATED_RUN_SCHEMA:
        blockers.append(_blocker("wrong_generated_run_schema", "metadata_contract"))
    if "final_report_boundary_summary" in value and not isinstance(value.get("final_report_boundary_summary"), dict):
        blockers.append(_blocker("missing_final_report_boundary_summary", "metadata_contract"))
    if not isinstance(value.get("dense_graph_proxy_summary"), dict):
        blockers.append(_blocker("missing_dense_graph_proxy_summary", "metadata_contract"))
    if not isinstance(value.get("report_candidate_summary"), dict):
        blockers.append(_blocker("missing_report_candidate_summary", "metadata_contract"))

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

    for field in sorted(REQUIRED_FALSE_FIELDS):
        if value.get(field, False) is not False:
            blockers.append(_blocker(f"final_report_boundary_flag_not_false:{field}", "side_effect"))

    for field in sorted(READINESS_FALSE_FIELDS):
        if value.get(field) is True:
            blockers.append(_blocker(f"readiness_flag_true:{field}", "side_effect"))

    for upstream_blocker in _safe_blockers(value.get("blockers")):
        reason = upstream_blocker["reason"].lower()
        category = upstream_blocker["category"].lower()
        if any(marker in reason or marker in category for marker in RISK_BLOCKER_MARKERS):
            blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "metadata_contract"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_source11_runtime_requests(value)):
        blockers.append(_blocker(f"requested_source11_runtime:{field_name}", "source11_runtime"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_sensitive_string(value):
        blockers.append(_blocker("blocked_sensitive_string_or_path", "privacy"))

    return _dedupe_blockers(blockers)


def _handoff_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return HANDOFF_READY_STATUS
    categories = {blocker["category"] for blocker in blockers}
    reasons = {blocker["reason"] for blocker in blockers}
    if "source11_runtime" in categories:
        return BLOCKED_SOURCE11_RUNTIME_STATUS
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if _safe_value(value, "final_report_boundary_status") == MANUAL_REVIEW_STATUS:
        return MANUAL_REVIEW_STATUS
    return BLOCKED_METADATA_STATUS


def _safe_final_report_boundary_summary(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "sentigraph_report_candidate_final_report_boundary_summary_v0_1",
        "final_report_boundary_id": _safe_value(value, "final_report_boundary_id"),
        "final_report_boundary_schema": _safe_value(value, "final_report_boundary_schema"),
        "final_report_boundary_status": _safe_value(value, "final_report_boundary_status"),
        "final_report_boundary_created": bool(value.get("final_report_boundary_created")),
        "report_candidate_id": _safe_value(value, "report_candidate_id"),
        "request_id": _safe_value(value, "request_id"),
        "package_name": _safe_package_name(value.get("package_name")),
        "selected_sample_scope_note": _safe_label(value.get("selected_sample_scope_note"))
        or "selected public sample only; not full-web, not full-platform, not full-thread",
        "coverage_limitations": _safe_string_list(value.get("coverage_limitations")),
        "human_review_required": True,
        "source11_final_summary_report_runtime_used": False,
        "final_summary_report_created": False,
        "final_report_created": False,
        "export_ready": False,
        "public_ready": False,
        "customer_ready": False,
    }


def _source11_governance_review_summary(source11_governance_handoff_created: bool) -> dict[str, Any]:
    return {
        "manual_review_required": True,
        "source11_manual_review_ready": bool(source11_governance_handoff_created),
        "source11_runtime_called": False,
        "final_summary_report_created": False,
        "final_report_created": False,
        "source11_runtime_requires_separate_decision": True,
        "source11_governance_handoff_is_not_final_report": True,
    }


def _source11_compatibility_notes() -> list[str]:
    return [
        "manual Source 11 governance review may inspect this handoff later",
        "Source 11 FinalSummaryReport runtime is not called by this handoff",
        "FinalSummaryReport creation requires a later explicit decision",
        "export/download/public-access gates remain separate and not ready",
    ]


def _governance_handoff_limitations() -> list[str]:
    return [
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "not_final_summary_report",
        "not_export_ready",
        "not_public_ready",
        "not_customer_ready",
        "not_production_ready",
    ]


def _warnings(final_report_boundary: dict[str, Any]) -> list[str]:
    warnings = _safe_string_list(final_report_boundary.get("warnings"))
    required = [
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "human_review_required",
        "source11_runtime_not_used",
        "final_summary_report_not_created",
        "export_download_public_access_not_approved",
        "downstream_gates_required",
    ]
    for item in required:
        if item not in warnings:
            warnings.append(item)
    return warnings


def _output_false_flags() -> dict[str, bool]:
    return {
        "source11_final_summary_report_runtime_used": False,
        "source11_runtime_called": False,
        "final_summary_report_created": False,
        "final_report_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "export_artifact_created": False,
        "download_package_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "generated_response_text": False,
        "public_route_created": False,
        "frontend_integration_approved": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "export_ready": False,
        "public_ready": False,
        "customer_ready": False,
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "selected_sample_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "human_review_required": True,
        "no_auto_execute": True,
        "no_generated_public_response": True,
        "not_final_summary_report": True,
        "source11_runtime_not_used": True,
        "not_export_ready": True,
        "not_public_ready": True,
        "not_customer_ready": True,
        "not_production_ready": True,
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
        "created_production_analysis_run": False,
        "used_source11_final_summary_report_runtime": False,
        "generated_final_summary_report": False,
        "generated_final_report_artifact": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "generated_export_artifact": False,
        "generated_download_package": False,
        "generated_public_access": False,
        "performed_external_delivery": False,
        "generated_response_text": False,
        "created_public_route": False,
        "created_file_byte_route": False,
        "generated_public_url": False,
        "generated_signed_url": False,
        "uploaded_object_storage": False,
        "sent_email": False,
        "published_to_portal": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _downstream_policy(source11_governance_handoff_created: bool) -> dict[str, Any]:
    return {
        "source11_manual_review_ready": bool(source11_governance_handoff_created),
        "source11_runtime_ready": False,
        "final_summary_report_ready": False,
        "export_ready": False,
        "download_ready": False,
        "public_access_ready": False,
        "external_delivery_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "source11_final_summary_report_runtime_requires_separate_decision": True,
        "export_download_package_runtime_requires_separate_decision": True,
        "public_access_external_delivery_requires_separate_decision": True,
        "b_end_report_runtime_requires_separate_decision": True,
        "sandbox_public_event_runtime_requires_separate_decision": True,
        "frontend_api_route_integration_requires_separate_decision": True,
        "evidence_layer_write_allowed": False,
        "production_case_creation_allowed": False,
        "production_analysis_run_creation_allowed": False,
        "generated_response_text_allowed": False,
        "platform_action_allowed": False,
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
            category = _safe_value(item, "category") or "source11_governance_handoff_blocker"
        else:
            reason = str(item)
            category = "source11_governance_handoff_blocker"
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
    if _looks_like_sensitive_string(stripped):
        return None
    return stripped or None


def _find_forbidden_fields(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if lowered in FORBIDDEN_FIELD_NAMES and not _is_allowed_false_flag(child_path, lowered, nested_value):
                found.add(str(key))
            found.update(_find_forbidden_fields(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item, path))
    return found


def _find_source11_runtime_requests(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if (
                lowered in SOURCE11_RUNTIME_REQUEST_FIELDS
                and _truthy(nested_value)
                and not _is_allowed_false_flag(child_path, lowered, nested_value)
            ):
                found.add(str(key))
            found.update(_find_source11_runtime_requests(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_source11_runtime_requests(item, path))
    return found


def _find_requested_side_effects(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if (
                lowered in REQUESTED_SIDE_EFFECT_FIELDS
                and _truthy(nested_value)
                and not _is_allowed_false_flag(child_path, lowered, nested_value)
            ):
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
                "external_delivery_target",
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
        or path.endswith(f"downstream_policy.{normalized_field}")
    )


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


def _handoff_id(final_report_boundary_id: str | None) -> str:
    return f"final_report_boundary_source11_governance_handoff_{_safe_identifier(final_report_boundary_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
