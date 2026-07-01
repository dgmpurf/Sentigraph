from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


EXPORT_GATE_HANDOFF_SCHEMA = "sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1"
INPUT_ADAPTER_SCHEMA = "sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1"
INPUT_ADAPTER_STATUS = "adapter_ready_with_local_finalsummaryreport_boundary"
INPUT_ADAPTER_MODE = "backend_only_local_finalsummaryreport_runtime_adapter_smoke"
INPUT_ADAPTER_SOURCE_KIND = "source11_governance_handoff"
INPUT_HANDOFF_SCHEMA = "sentigraph_final_report_boundary_source11_governance_handoff_v0_1"
INPUT_HANDOFF_STATUS = "handoff_ready_for_manual_source11_governance_review"
FINAL_SUMMARY_REPORT_SCHEMA = "sentigraph_final_summary_report_v1"
INPUT_SOURCE_KIND = "finalsummaryreport_boundary_adapter"
HANDOFF_MODE = "backend_only_local_export_gate_handoff_readiness_smoke"

READY_STATUS = "export_gate_handoff_ready_for_manual_review"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
BLOCKED_EXPORT_RUNTIME_STATUS = "blocked_export_runtime_side_effect_risk"
MANUAL_REVIEW_STATUS = "manual_review_required"

REQUIRED_BOUNDARY_TRUE_FLAGS = {
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

REQUIRED_FALSE_FIELDS = {
    "source11_runtime_called",
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
    "route_ready",
    "frontend_ready",
    "production_ready",
    "export_ready",
    "public_ready",
    "customer_ready",
    "b_end_ready",
    "sandbox_ready",
    "public_event_ready",
}

EXPORT_RUNTIME_REQUEST_FIELDS = {
    "export_gate_runtime_used",
    "called_export_gate_runtime",
    "export_gate_created",
    "export_artifact_created",
    "generated_export_artifact",
    "create_export_artifact",
    "generated_markdown_file",
    "generated_pdf_file",
    "generated_briefing_deck",
    "generated_evidence_appendix_package",
    "download_package_created",
    "generated_download_package",
    "generated_zip_package",
    "public_access_created",
    "generated_public_access",
    "external_delivery_performed",
    "performed_external_delivery",
}

REQUESTED_SIDE_EFFECT_FIELDS = {
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
    "b_end_ready",
    "sandbox_ready",
    "public_event_ready",
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
    "object_storage_target",
    "email_delivery_target",
    "portal_publication_target",
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
    "export",
    "download",
    "delivery",
}


def build_finalsummaryreport_boundary_export_gate_handoff(
    finalsummaryreport_adapter: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_adapter = finalsummaryreport_adapter if isinstance(finalsummaryreport_adapter, dict) else {}
    blockers = _collect_blockers(safe_adapter)
    status = _handoff_status(blockers, safe_adapter)
    return _handoff_object(
        safe_adapter,
        created_by=created_by,
        export_gate_handoff_status=status,
        export_gate_handoff_created=not blockers,
        blockers=blockers,
    )


def create_finalsummaryreport_boundary_export_gate_handoff(
    finalsummaryreport_adapter: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return build_finalsummaryreport_boundary_export_gate_handoff(
        finalsummaryreport_adapter,
        created_by=created_by,
    )


def build_safe_finalsummaryreport_boundary_export_gate_handoff_summary(
    handoff: dict[str, Any],
) -> dict[str, Any]:
    safe_handoff = handoff if isinstance(handoff, dict) else {}
    return {
        "schema": "sentigraph_finalsummaryreport_boundary_export_gate_handoff_summary_v0_1",
        "export_gate_handoff_id": _safe_value(safe_handoff, "export_gate_handoff_id"),
        "export_gate_handoff_schema": _safe_value(safe_handoff, "export_gate_handoff_schema"),
        "export_gate_handoff_status": _safe_value(safe_handoff, "export_gate_handoff_status"),
        "export_gate_handoff_created": bool(safe_handoff.get("export_gate_handoff_created")),
        "created_local_export_gate_handoff": bool(safe_handoff.get("created_local_export_gate_handoff")),
        "adapter_id": _safe_value(safe_handoff, "adapter_id"),
        "final_summary_report_id": _safe_value(safe_handoff, "final_summary_report_id"),
        "request_id": _safe_value(safe_handoff, "request_id"),
        "package_name": _safe_package_name(safe_handoff.get("package_name")),
        "human_review_required": True,
        "export_gate_runtime_used": False,
        "export_artifact_created": False,
        "download_package_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "warnings": _safe_string_list(safe_handoff.get("warnings")),
        "blockers": _safe_blockers(safe_handoff.get("blockers")),
    }


def _handoff_object(
    adapter: dict[str, Any],
    *,
    created_by: str,
    export_gate_handoff_status: str,
    export_gate_handoff_created: bool,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    adapter_id = _safe_value(adapter, "adapter_id")
    local_report = adapter.get("local_final_summary_report") if isinstance(adapter.get("local_final_summary_report"), dict) else {}
    final_summary_report_id = _safe_value(local_report, "final_summary_report_id") or _safe_value(
        adapter, "final_summary_report_id"
    )
    return {
        "export_gate_handoff_id": _handoff_id(adapter_id),
        "export_gate_handoff_schema": EXPORT_GATE_HANDOFF_SCHEMA,
        "export_gate_handoff_status": export_gate_handoff_status,
        "export_gate_handoff_created": bool(export_gate_handoff_created),
        "created_local_export_gate_handoff": bool(export_gate_handoff_created),
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "adapter_id": adapter_id,
        "final_summary_report_id": final_summary_report_id,
        "source11_governance_handoff_id": _safe_value(adapter, "source11_governance_handoff_id"),
        "final_report_boundary_id": _safe_value(adapter, "final_report_boundary_id"),
        "report_candidate_id": _safe_value(adapter, "report_candidate_id"),
        "integration_id": _safe_value(adapter, "integration_id"),
        "execution_id": _safe_value(adapter, "execution_id"),
        "bridge_id": _safe_value(adapter, "bridge_id"),
        "staging_candidate_id": _safe_value(adapter, "staging_candidate_id"),
        "provider_result_id": _safe_value(adapter, "provider_result_id"),
        "request_id": _safe_value(adapter, "request_id"),
        "case_id_hint": _safe_value(adapter, "case_id_hint"),
        "package_name": _safe_package_name(adapter.get("package_name")),
        "input_source_kind": INPUT_SOURCE_KIND,
        "handoff_mode": HANDOFF_MODE,
        "adapter_schema": _safe_value(adapter, "adapter_schema") or INPUT_ADAPTER_SCHEMA,
        "adapter_status": _safe_value(adapter, "adapter_status") or BLOCKED_METADATA_STATUS,
        "source11_governance_handoff_schema": _safe_value(adapter, "source11_governance_handoff_schema"),
        "source11_governance_handoff_status": _safe_value(adapter, "source11_governance_handoff_status"),
        "final_summary_report_schema": FINAL_SUMMARY_REPORT_SCHEMA if export_gate_handoff_created else None,
        "final_summary_report_created": bool(export_gate_handoff_created),
        "final_summary_report_created_local_only": bool(export_gate_handoff_created),
        "local_final_summary_report_only": bool(export_gate_handoff_created),
        "source_and_scope": _source_and_scope(),
        "final_summary_report_boundary_summary": _final_summary_report_boundary_summary(
            adapter,
            local_report,
            enabled=export_gate_handoff_created,
        ),
        "export_gate_readiness_summary": _export_gate_readiness_summary(export_gate_handoff_created),
        "boundary_block": _boundary_block(),
        "coverage_limitations": _coverage_limitations(),
        "warnings": _warnings(adapter),
        "blockers": _safe_blockers(blockers),
        "human_review_status": "required",
        "human_review_required": True,
        **_output_false_flags(),
        "boundary_flags": _boundary_flags(export_gate_handoff_created),
        "runtime_side_effects": _runtime_side_effects(export_gate_handoff_created),
        "audit_refs": _safe_audit_refs(adapter.get("audit_refs")),
        "downstream_policy": _downstream_policy(export_gate_handoff_created),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "adapter_id") is None:
        blockers.append(_blocker("missing_adapter_id", "metadata_contract"))
    if _safe_value(value, "adapter_schema") != INPUT_ADAPTER_SCHEMA:
        blockers.append(_blocker("wrong_adapter_schema", "metadata_contract"))
    if _safe_value(value, "adapter_status") != INPUT_ADAPTER_STATUS:
        blockers.append(_blocker("adapter_status_not_ready", "metadata_contract"))
    if value.get("adapter_created") is not True:
        blockers.append(_blocker("adapter_not_created", "metadata_contract"))
    if _safe_value(value, "adapter_mode") != INPUT_ADAPTER_MODE:
        blockers.append(_blocker("wrong_adapter_mode", "metadata_contract"))
    if _safe_value(value, "input_source_kind") != INPUT_ADAPTER_SOURCE_KIND:
        blockers.append(_blocker("wrong_adapter_input_source_kind", "metadata_contract"))
    if _safe_value(value, "source11_governance_handoff_schema") != INPUT_HANDOFF_SCHEMA:
        blockers.append(_blocker("wrong_source11_governance_handoff_schema", "metadata_contract"))
    if _safe_value(value, "source11_governance_handoff_status") != INPUT_HANDOFF_STATUS:
        blockers.append(_blocker("source11_governance_handoff_status_not_ready", "metadata_contract"))
    if _safe_value(value, "final_summary_report_schema") != FINAL_SUMMARY_REPORT_SCHEMA:
        blockers.append(_blocker("wrong_final_summary_report_schema", "metadata_contract"))
    if value.get("final_summary_report_created") is not True:
        blockers.append(_blocker("final_summary_report_not_created", "metadata_contract"))
    if value.get("final_summary_report_created_local_only") is not True:
        blockers.append(_blocker("final_summary_report_not_local_only", "metadata_contract"))
    if value.get("local_final_summary_report_only") is not True:
        blockers.append(_blocker("local_final_summary_report_only_not_true", "metadata_contract"))
    if value.get("human_review_required") is not True:
        blockers.append(_blocker("human_review_not_required", "metadata_contract"))

    local_report = value.get("local_final_summary_report")
    if not isinstance(local_report, dict):
        blockers.append(_blocker("missing_local_final_summary_report", "metadata_contract"))
    else:
        if _safe_value(local_report, "schema") != FINAL_SUMMARY_REPORT_SCHEMA:
            blockers.append(_blocker("wrong_local_final_summary_report_schema", "metadata_contract"))
        if _safe_value(local_report, "status") != "final_summary_report_created":
            blockers.append(_blocker("local_final_summary_report_status_not_created", "metadata_contract"))
        if local_report.get("local_only") is not True:
            blockers.append(_blocker("local_final_summary_report_not_local_only", "metadata_contract"))

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
            if key == "created_local_final_summary_report_boundary" and flag_value is True:
                continue
            if flag_value is not False:
                blockers.append(_blocker(f"runtime_side_effect_not_false:{key}", "side_effect"))

    for field in sorted(REQUIRED_FALSE_FIELDS):
        if value.get(field, False) is not False:
            blockers.append(_blocker(f"adapter_flag_not_false:{field}", "side_effect"))

    if value.get("source11_final_summary_report_runtime_used") is not True:
        blockers.append(_blocker("source11_final_summary_report_runtime_marker_missing", "metadata_contract"))
    if value.get("source11_runtime_called") is not False:
        blockers.append(_blocker("source11_runtime_called_not_false", "side_effect"))

    for upstream_blocker in _safe_blockers(value.get("blockers")):
        reason = upstream_blocker["reason"].lower()
        category = upstream_blocker["category"].lower()
        if any(marker in reason or marker in category for marker in RISK_BLOCKER_MARKERS):
            blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "metadata_contract"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_export_runtime_requests(value)):
        blockers.append(_blocker(f"requested_export_runtime_or_artifact:{field_name}", "export_runtime"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_sensitive_string(value):
        blockers.append(_blocker("blocked_sensitive_string_or_path", "privacy"))

    return _dedupe_blockers(blockers)


def _handoff_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return READY_STATUS
    categories = {blocker["category"] for blocker in blockers}
    reasons = {blocker["reason"] for blocker in blockers}
    if "export_runtime" in categories:
        return BLOCKED_EXPORT_RUNTIME_STATUS
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if _safe_value(value, "adapter_status") == MANUAL_REVIEW_STATUS:
        return MANUAL_REVIEW_STATUS
    return BLOCKED_METADATA_STATUS


def _source_and_scope() -> dict[str, bool | str]:
    return {
        "input_source_kind": INPUT_SOURCE_KIND,
        "selected_sample_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "provider_output_is_evidence_not_truth": True,
        "scope_note": "selected public sample only; export gate handoff only",
    }


def _final_summary_report_boundary_summary(
    adapter: dict[str, Any],
    local_report: dict[str, Any],
    *,
    enabled: bool,
) -> dict[str, Any]:
    return {
        "adapter_id": _safe_value(adapter, "adapter_id"),
        "final_summary_report_id": _safe_value(local_report, "final_summary_report_id"),
        "final_summary_report_schema": FINAL_SUMMARY_REPORT_SCHEMA if enabled else None,
        "final_summary_report_created": bool(enabled),
        "final_summary_report_created_local_only": bool(enabled),
        "local_final_summary_report_only": bool(enabled),
        "report_sections": _safe_string_list(local_report.get("report_sections")),
        "human_review_required": True,
        "export_gate_handoff_only": True,
        "export_gate_runtime_used": False,
        "export_artifact_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
    }


def _export_gate_readiness_summary(enabled: bool) -> dict[str, Any]:
    return {
        "eligible_for_later_manual_export_gate_review": bool(enabled),
        "manual_review_required": True,
        "export_gate_runtime_used": False,
        "called_export_gate_runtime": False,
        "export_gate_created": False,
        "export_artifact_created": False,
        "download_package_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "export_ready": False,
        "public_ready": False,
        "customer_ready": False,
    }


def _boundary_block() -> dict[str, bool]:
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
        "export_gate_handoff_only": True,
    }


def _coverage_limitations() -> list[str]:
    return [
        "selected_sample_only",
        "not_full_web",
        "not_full_platform",
        "not_full_thread",
        "not_official_verification",
        "not_causal_proof",
        "not_prediction",
        "not_production_score",
        "export_gate_handoff_only",
    ]


def _warnings(adapter: dict[str, Any]) -> list[str]:
    warnings = _safe_string_list(adapter.get("warnings"))
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
        "export_gate_handoff_only",
        "export_gate_runtime_not_used",
        "export_artifact_not_created",
        "download_public_access_external_delivery_not_approved",
        "b_end_sandbox_public_event_not_approved",
        "downstream_gates_required",
    ]
    for item in required:
        if item not in warnings:
            warnings.append(item)
    return warnings


def _output_false_flags() -> dict[str, bool]:
    return {
        "export_gate_runtime_used": False,
        "called_export_gate_runtime": False,
        "export_gate_created": False,
        "export_artifact_created": False,
        "download_package_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "frontend_integration_approved": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "export_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
    }


def _boundary_flags(created: bool) -> dict[str, bool]:
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
        "local_final_summary_report_only": bool(created),
        "export_gate_handoff_only": True,
        "export_runtime_not_used": True,
        "export_artifact_not_created": True,
        "download_package_not_created": True,
        "public_access_not_created": True,
        "external_delivery_not_performed": True,
        "downstream_gates_required": True,
        "not_export_ready": True,
        "not_public_ready": True,
        "not_customer_ready": True,
        "not_production_ready": True,
        "not_b_end_ready": True,
        "not_sandbox_ready": True,
        "not_public_event_ready": True,
    }


def _runtime_side_effects(created: bool) -> dict[str, bool]:
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
        "called_export_gate_runtime": False,
        "generated_export_artifact": False,
        "generated_markdown_file": False,
        "generated_pdf_file": False,
        "generated_briefing_deck": False,
        "generated_evidence_appendix_package": False,
        "generated_download_package": False,
        "generated_zip_package": False,
        "generated_public_access": False,
        "performed_external_delivery": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
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
        "created_local_export_gate_handoff": bool(created),
    }


def _downstream_policy(created: bool) -> dict[str, Any]:
    return {
        "export_gate_handoff_ready_for_manual_review": bool(created),
        "export_gate_runtime_ready": False,
        "export_artifact_ready": False,
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
        "export_gate_runtime_requires_separate_decision": True,
        "export_artifact_runtime_requires_separate_decision": True,
        "download_package_runtime_requires_separate_decision": True,
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
            category = _safe_value(item, "category") or "finalsummaryreport_export_gate_handoff_blocker"
        else:
            reason = str(item)
            category = "finalsummaryreport_export_gate_handoff_blocker"
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


def _find_export_runtime_requests(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if (
                lowered in EXPORT_RUNTIME_REQUEST_FIELDS
                and _truthy(nested_value)
                and not _is_allowed_false_flag(child_path, lowered, nested_value)
            ):
                found.add(str(key))
            found.update(_find_export_runtime_requests(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_export_runtime_requests(item, path))
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
                "object_storage_target",
                "email_delivery_target",
                "portal_publication_target",
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
        or path.endswith(f"export_gate_readiness_summary.{normalized_field}")
        or path.endswith(f"final_summary_report_boundary_summary.{normalized_field}")
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


def _handoff_id(adapter_id: str | None) -> str:
    return f"finalsummaryreport_boundary_export_gate_handoff_{_safe_identifier(adapter_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
