from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


DOWNLOAD_PUBLIC_ACCESS_BOUNDARY_SCHEMA = "sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1"
INPUT_EXPORT_ARTIFACT_BOUNDARY_SCHEMA = "sentigraph_export_gate_handoff_export_artifact_boundary_v0_1"
INPUT_EXPORT_ARTIFACT_BOUNDARY_STATUS = "export_artifact_boundary_ready_for_manual_review"
INPUT_EXPORT_ARTIFACT_BOUNDARY_SOURCE_KIND = "export_gate_handoff"
INPUT_EXPORT_ARTIFACT_BOUNDARY_MODE = "backend_only_local_export_artifact_boundary_readiness_smoke"
INPUT_EXPORT_GATE_HANDOFF_SCHEMA = "sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1"
INPUT_EXPORT_GATE_HANDOFF_STATUS = "export_gate_handoff_ready_for_manual_review"
INPUT_SOURCE_KIND = "export_artifact_boundary"
BOUNDARY_MODE = "backend_only_local_download_public_access_boundary_readiness_smoke"

READY_STATUS = "download_public_access_boundary_ready_for_manual_review"
BLOCKED_METADATA_STATUS = "blocked_metadata_contract"
BLOCKED_PRIVACY_STATUS = "blocked_privacy_issue"
BLOCKED_SIDE_EFFECT_STATUS = "blocked_requested_side_effect"
BLOCKED_FORBIDDEN_STATUS = "blocked_forbidden_input"
BLOCKED_DOWNLOAD_PUBLIC_ACCESS_RUNTIME_STATUS = "blocked_download_public_access_runtime_side_effect_risk"
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
    "export_gate_handoff_only",
    "export_artifact_boundary_only",
    "export_artifact_runtime_not_used",
    "export_artifact_record_not_created",
    "download_package_not_created",
    "public_access_not_created",
    "external_delivery_not_performed",
}

REQUIRED_FALSE_FIELDS = {
    "export_artifact_runtime_used",
    "called_export_artifact_runtime",
    "final_summary_report_export_artifact_created",
    "export_artifact_created",
    "generated_markdown_file",
    "generated_pdf_file",
    "generated_briefing_deck",
    "generated_evidence_appendix_package",
    "generated_zip_package",
    "download_package_created",
    "public_access_created",
    "external_delivery_performed",
    "b_end_report_runtime_generated",
    "sandbox_public_event_generated",
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

DOWNLOAD_PUBLIC_ACCESS_RUNTIME_REQUEST_FIELDS = {
    "download_package_runtime_used",
    "called_download_package_runtime",
    "public_access_runtime_used",
    "called_public_access_runtime",
    "external_delivery_runtime_used",
    "called_external_delivery_runtime",
    "download_package_created",
    "generated_download_package",
    "generated_zip_package",
    "public_url_created",
    "signed_url_created",
    "generated_public_url",
    "generated_signed_url",
    "public_access_created",
    "generated_public_access",
    "external_delivery_performed",
    "performed_external_delivery",
    "file_byte_route_created",
    "created_file_byte_route",
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
    "download_ready",
    "public_ready",
    "public_access_ready",
    "external_delivery_ready",
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
    "evidence_appendix_package_path",
    "zip_path",
    "download_package_path",
    "package_path",
    "runtime_path",
    "local_runtime_path",
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
    "download",
    "delivery",
    "real_provider",
}


def build_export_artifact_boundary_download_public_access_boundary(
    export_artifact_boundary: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    safe_boundary = export_artifact_boundary if isinstance(export_artifact_boundary, dict) else {}
    blockers = _collect_blockers(safe_boundary)
    status = _boundary_status(blockers, safe_boundary)
    return _boundary_object(
        safe_boundary,
        created_by=created_by,
        download_public_access_boundary_status=status,
        download_public_access_boundary_created=not blockers,
        blockers=blockers,
    )


def create_export_artifact_boundary_download_public_access_boundary(
    export_artifact_boundary: dict[str, Any],
    *,
    created_by: str = "sentigraph_internal_operator",
) -> dict[str, Any]:
    return build_export_artifact_boundary_download_public_access_boundary(
        export_artifact_boundary,
        created_by=created_by,
    )


def build_safe_export_artifact_boundary_download_public_access_boundary_summary(
    boundary: dict[str, Any],
) -> dict[str, Any]:
    safe_boundary = boundary if isinstance(boundary, dict) else {}
    return {
        "schema": "sentigraph_export_artifact_boundary_download_public_access_boundary_summary_v0_1",
        "download_public_access_boundary_id": _safe_value(safe_boundary, "download_public_access_boundary_id"),
        "download_public_access_boundary_schema": _safe_value(safe_boundary, "download_public_access_boundary_schema"),
        "download_public_access_boundary_status": _safe_value(safe_boundary, "download_public_access_boundary_status"),
        "download_public_access_boundary_created": bool(safe_boundary.get("download_public_access_boundary_created")),
        "created_local_download_public_access_boundary": bool(
            safe_boundary.get("created_local_download_public_access_boundary")
        ),
        "export_artifact_boundary_id": _safe_value(safe_boundary, "export_artifact_boundary_id"),
        "export_gate_handoff_id": _safe_value(safe_boundary, "export_gate_handoff_id"),
        "final_summary_report_id": _safe_value(safe_boundary, "final_summary_report_id"),
        "request_id": _safe_value(safe_boundary, "request_id"),
        "package_name": _safe_package_name(safe_boundary.get("package_name")),
        "human_review_required": True,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "download_package_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "warnings": _safe_string_list(safe_boundary.get("warnings")),
        "blockers": _safe_blockers(safe_boundary.get("blockers")),
    }


def _boundary_object(
    export_artifact_boundary: dict[str, Any],
    *,
    created_by: str,
    download_public_access_boundary_status: str,
    download_public_access_boundary_created: bool,
    blockers: list[dict[str, str]],
) -> dict[str, Any]:
    export_artifact_boundary_id = _safe_value(export_artifact_boundary, "export_artifact_boundary_id")
    return {
        "download_public_access_boundary_id": _boundary_id(export_artifact_boundary_id),
        "download_public_access_boundary_schema": DOWNLOAD_PUBLIC_ACCESS_BOUNDARY_SCHEMA,
        "download_public_access_boundary_status": download_public_access_boundary_status,
        "download_public_access_boundary_created": bool(download_public_access_boundary_created),
        "created_local_download_public_access_boundary": bool(download_public_access_boundary_created),
        "created_at": _utc_now(),
        "created_by": _safe_label(created_by) or "sentigraph_internal_operator",
        "export_artifact_boundary_id": export_artifact_boundary_id,
        "export_gate_handoff_id": _safe_value(export_artifact_boundary, "export_gate_handoff_id"),
        "adapter_id": _safe_value(export_artifact_boundary, "adapter_id"),
        "final_summary_report_id": _safe_value(export_artifact_boundary, "final_summary_report_id"),
        "source11_governance_handoff_id": _safe_value(export_artifact_boundary, "source11_governance_handoff_id"),
        "final_report_boundary_id": _safe_value(export_artifact_boundary, "final_report_boundary_id"),
        "report_candidate_id": _safe_value(export_artifact_boundary, "report_candidate_id"),
        "integration_id": _safe_value(export_artifact_boundary, "integration_id"),
        "execution_id": _safe_value(export_artifact_boundary, "execution_id"),
        "bridge_id": _safe_value(export_artifact_boundary, "bridge_id"),
        "staging_candidate_id": _safe_value(export_artifact_boundary, "staging_candidate_id"),
        "provider_result_id": _safe_value(export_artifact_boundary, "provider_result_id"),
        "request_id": _safe_value(export_artifact_boundary, "request_id"),
        "case_id_hint": _safe_value(export_artifact_boundary, "case_id_hint"),
        "package_name": _safe_package_name(export_artifact_boundary.get("package_name")),
        "input_source_kind": INPUT_SOURCE_KIND,
        "boundary_mode": BOUNDARY_MODE,
        "export_artifact_boundary_schema": _safe_value(export_artifact_boundary, "export_artifact_boundary_schema")
        or INPUT_EXPORT_ARTIFACT_BOUNDARY_SCHEMA,
        "export_artifact_boundary_status": _safe_value(export_artifact_boundary, "export_artifact_boundary_status")
        or BLOCKED_METADATA_STATUS,
        "export_artifact_boundary_created": bool(export_artifact_boundary.get("export_artifact_boundary_created")),
        "created_local_export_artifact_boundary": bool(
            export_artifact_boundary.get("created_local_export_artifact_boundary")
        ),
        "export_gate_handoff_schema": _safe_value(export_artifact_boundary, "export_gate_handoff_schema"),
        "export_gate_handoff_status": _safe_value(export_artifact_boundary, "export_gate_handoff_status"),
        "export_gate_handoff_created": bool(export_artifact_boundary.get("export_gate_handoff_created")),
        "created_local_export_gate_handoff": bool(export_artifact_boundary.get("created_local_export_gate_handoff")),
        "final_summary_report_created": bool(download_public_access_boundary_created),
        "final_summary_report_created_local_only": bool(download_public_access_boundary_created),
        "local_final_summary_report_only": bool(download_public_access_boundary_created),
        "source_and_scope": _source_and_scope(),
        "export_artifact_boundary_summary": _export_artifact_boundary_summary(
            export_artifact_boundary,
            enabled=download_public_access_boundary_created,
        ),
        "download_public_access_boundary_readiness_summary": _download_public_access_boundary_readiness_summary(
            download_public_access_boundary_created
        ),
        "boundary_block": _boundary_block(),
        "coverage_limitations": _coverage_limitations(),
        "warnings": _warnings(export_artifact_boundary),
        "blockers": _safe_blockers(blockers),
        "human_review_status": "required",
        "human_review_required": True,
        **_output_false_flags(),
        "boundary_flags": _boundary_flags(download_public_access_boundary_created),
        "runtime_side_effects": _runtime_side_effects(download_public_access_boundary_created),
        "audit_refs": _safe_audit_refs(export_artifact_boundary.get("audit_refs")),
        "downstream_policy": _downstream_policy(download_public_access_boundary_created),
    }


def _collect_blockers(value: dict[str, Any]) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if _safe_value(value, "export_artifact_boundary_id") is None:
        blockers.append(_blocker("missing_export_artifact_boundary_id", "metadata_contract"))
    if _safe_value(value, "export_artifact_boundary_schema") != INPUT_EXPORT_ARTIFACT_BOUNDARY_SCHEMA:
        blockers.append(_blocker("wrong_export_artifact_boundary_schema", "metadata_contract"))
    if _safe_value(value, "export_artifact_boundary_status") != INPUT_EXPORT_ARTIFACT_BOUNDARY_STATUS:
        blockers.append(_blocker("export_artifact_boundary_status_not_ready", "metadata_contract"))
    if value.get("export_artifact_boundary_created") is not True:
        blockers.append(_blocker("export_artifact_boundary_not_created", "metadata_contract"))
    if value.get("created_local_export_artifact_boundary") is not True:
        blockers.append(_blocker("created_local_export_artifact_boundary_missing", "metadata_contract"))
    if _safe_value(value, "input_source_kind") != INPUT_EXPORT_ARTIFACT_BOUNDARY_SOURCE_KIND:
        blockers.append(_blocker("wrong_export_artifact_boundary_input_source_kind", "metadata_contract"))
    if _safe_value(value, "boundary_mode") != INPUT_EXPORT_ARTIFACT_BOUNDARY_MODE:
        blockers.append(_blocker("wrong_export_artifact_boundary_mode", "metadata_contract"))
    if _safe_value(value, "export_gate_handoff_schema") != INPUT_EXPORT_GATE_HANDOFF_SCHEMA:
        blockers.append(_blocker("wrong_export_gate_handoff_schema", "metadata_contract"))
    if _safe_value(value, "export_gate_handoff_status") != INPUT_EXPORT_GATE_HANDOFF_STATUS:
        blockers.append(_blocker("export_gate_handoff_status_not_ready", "metadata_contract"))
    if value.get("export_gate_handoff_created") is not True:
        blockers.append(_blocker("export_gate_handoff_not_created", "metadata_contract"))
    if value.get("created_local_export_gate_handoff") is not True:
        blockers.append(_blocker("created_local_export_gate_handoff_missing", "metadata_contract"))
    if value.get("final_summary_report_created") is not True:
        blockers.append(_blocker("final_summary_report_not_created", "metadata_contract"))
    if value.get("final_summary_report_created_local_only") is not True:
        blockers.append(_blocker("final_summary_report_not_local_only", "metadata_contract"))
    if value.get("local_final_summary_report_only") is not True:
        blockers.append(_blocker("local_final_summary_report_only_not_true", "metadata_contract"))
    if value.get("human_review_required") is not True:
        blockers.append(_blocker("human_review_not_required", "metadata_contract"))
    if not isinstance(value.get("export_gate_handoff_summary"), dict):
        blockers.append(_blocker("missing_export_gate_handoff_summary", "metadata_contract"))
    if not isinstance(value.get("export_artifact_boundary_readiness_summary"), dict):
        blockers.append(_blocker("missing_export_artifact_boundary_readiness_summary", "metadata_contract"))

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
            if key == "created_local_export_artifact_boundary" and flag_value is True:
                continue
            if flag_value is not False:
                blockers.append(_blocker(f"runtime_side_effect_not_false:{key}", "side_effect"))

    for field in sorted(REQUIRED_FALSE_FIELDS):
        if value.get(field, False) is not False:
            blockers.append(_blocker(f"export_artifact_boundary_flag_not_false:{field}", "side_effect"))

    for upstream_blocker in _safe_blockers(value.get("blockers")):
        reason = upstream_blocker["reason"].lower()
        category = upstream_blocker["category"].lower()
        if any(marker in reason or marker in category for marker in RISK_BLOCKER_MARKERS):
            blockers.append(_blocker(f"upstream_blocker:{upstream_blocker['reason']}", "metadata_contract"))

    for field_name in sorted(_find_forbidden_fields(value)):
        blockers.append(_blocker(f"forbidden_input_field:{field_name}", "privacy"))

    for field_name in sorted(_find_download_public_access_runtime_requests(value)):
        blockers.append(_blocker(f"requested_download_public_access_runtime_or_delivery:{field_name}", "download_public_access_runtime"))

    for field_name in sorted(_find_requested_side_effects(value)):
        blockers.append(_blocker(f"requested_side_effect:{field_name}", "side_effect"))

    if _has_sensitive_string(value):
        blockers.append(_blocker("blocked_sensitive_string_or_path", "privacy"))

    return _dedupe_blockers(blockers)


def _boundary_status(blockers: list[dict[str, str]], value: dict[str, Any]) -> str:
    if not blockers:
        return READY_STATUS
    categories = {blocker["category"] for blocker in blockers}
    reasons = {blocker["reason"] for blocker in blockers}
    if "download_public_access_runtime" in categories:
        return BLOCKED_DOWNLOAD_PUBLIC_ACCESS_RUNTIME_STATUS
    if "side_effect" in categories:
        return BLOCKED_SIDE_EFFECT_STATUS
    if "privacy" in categories:
        if any(reason.startswith("forbidden_input_field") for reason in reasons):
            return BLOCKED_PRIVACY_STATUS
        return BLOCKED_FORBIDDEN_STATUS
    if _safe_value(value, "export_artifact_boundary_status") == MANUAL_REVIEW_STATUS:
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
        "scope_note": "selected public sample only; download/public-access boundary marker only",
    }


def _export_artifact_boundary_summary(value: dict[str, Any], *, enabled: bool) -> dict[str, Any]:
    return {
        "export_artifact_boundary_id": _safe_value(value, "export_artifact_boundary_id"),
        "export_artifact_boundary_schema": _safe_value(value, "export_artifact_boundary_schema"),
        "export_artifact_boundary_status": _safe_value(value, "export_artifact_boundary_status"),
        "export_artifact_boundary_created": bool(value.get("export_artifact_boundary_created") and enabled),
        "created_local_export_artifact_boundary": bool(
            value.get("created_local_export_artifact_boundary") and enabled
        ),
        "export_gate_handoff_id": _safe_value(value, "export_gate_handoff_id"),
        "final_summary_report_id": _safe_value(value, "final_summary_report_id"),
        "final_summary_report_created": bool(value.get("final_summary_report_created") and enabled),
        "final_summary_report_created_local_only": bool(value.get("final_summary_report_created_local_only") and enabled),
        "human_review_required": True,
        "download_public_access_boundary_only": True,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
    }


def _download_public_access_boundary_readiness_summary(enabled: bool) -> dict[str, Any]:
    return {
        "eligible_for_later_manual_download_public_access_runtime_review": bool(enabled),
        "manual_review_required": True,
        "download_package_runtime_used": False,
        "called_download_package_runtime": False,
        "public_access_runtime_used": False,
        "called_public_access_runtime": False,
        "external_delivery_runtime_used": False,
        "called_external_delivery_runtime": False,
        "download_package_created": False,
        "generated_zip_package": False,
        "public_url_created": False,
        "signed_url_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "file_byte_route_created": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "export_ready": False,
        "download_ready": False,
        "public_ready": False,
        "public_access_ready": False,
        "external_delivery_ready": False,
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
        "download_public_access_boundary_only": True,
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
        "download_public_access_boundary_only",
    ]


def _warnings(value: dict[str, Any]) -> list[str]:
    warnings = _safe_string_list(value.get("warnings"))
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
        "download_public_access_boundary_only",
        "download_package_runtime_not_used",
        "public_access_runtime_not_used",
        "external_delivery_runtime_not_used",
        "download_package_not_created",
        "zip_package_not_generated",
        "public_url_not_created",
        "signed_url_not_created",
        "file_byte_route_not_created",
        "b_end_sandbox_public_event_not_approved",
        "downstream_gates_required",
    ]
    for item in required:
        if item not in warnings:
            warnings.append(item)
    return warnings


def _output_false_flags() -> dict[str, bool]:
    return {
        "download_package_runtime_used": False,
        "called_download_package_runtime": False,
        "public_access_runtime_used": False,
        "called_public_access_runtime": False,
        "external_delivery_runtime_used": False,
        "called_external_delivery_runtime": False,
        "download_package_created": False,
        "generated_zip_package": False,
        "public_url_created": False,
        "signed_url_created": False,
        "public_access_created": False,
        "external_delivery_performed": False,
        "file_byte_route_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "frontend_integration_approved": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "export_ready": False,
        "download_ready": False,
        "public_ready": False,
        "public_access_ready": False,
        "external_delivery_ready": False,
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
        "export_artifact_boundary_only": True,
        "download_public_access_boundary_only": True,
        "download_package_runtime_not_used": True,
        "public_access_runtime_not_used": True,
        "external_delivery_runtime_not_used": True,
        "download_package_not_created": True,
        "zip_package_not_generated": True,
        "public_url_not_created": True,
        "signed_url_not_created": True,
        "file_byte_route_not_created": True,
        "public_access_not_created": True,
        "external_delivery_not_performed": True,
        "b_end_report_not_generated": True,
        "sandbox_public_event_not_generated": True,
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
        "called_export_artifact_runtime": False,
        "called_download_package_runtime": False,
        "called_public_access_runtime": False,
        "called_external_delivery_runtime": False,
        "generated_export_artifact": False,
        "created_final_summary_report_export_artifact": False,
        "generated_markdown_file": False,
        "generated_pdf_file": False,
        "generated_briefing_deck": False,
        "generated_evidence_appendix_package": False,
        "generated_download_package": False,
        "generated_zip_package": False,
        "generated_public_access": False,
        "performed_external_delivery": False,
        "created_file_byte_route": False,
        "generated_public_url": False,
        "generated_signed_url": False,
        "uploaded_object_storage": False,
        "sent_email": False,
        "published_to_portal": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "generated_response_text": False,
        "created_public_route": False,
        "published_or_sent": False,
        "auto_executed": False,
        "created_local_download_public_access_boundary": bool(created),
    }


def _downstream_policy(created: bool) -> dict[str, Any]:
    return {
        "download_public_access_boundary_ready_for_manual_review": bool(created),
        "download_package_runtime_ready": False,
        "public_access_runtime_ready": False,
        "external_delivery_runtime_ready": False,
        "zip_package_ready": False,
        "file_byte_route_ready": False,
        "public_url_ready": False,
        "signed_url_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
        "customer_ready": False,
        "download_package_runtime_requires_separate_decision": True,
        "public_access_runtime_requires_separate_decision": True,
        "external_delivery_runtime_requires_separate_decision": True,
        "zip_package_generation_requires_separate_decision": True,
        "public_url_generation_requires_separate_decision": True,
        "signed_url_generation_requires_separate_decision": True,
        "file_byte_route_requires_separate_decision": True,
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
            category = _safe_value(item, "category") or "download_public_access_boundary_blocker"
        else:
            reason = str(item)
            category = "download_public_access_boundary_blocker"
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


def _find_download_public_access_runtime_requests(value: Any, path: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            lowered = str(key).lower()
            child_path = f"{path}.{lowered}" if path else lowered
            if (
                lowered in DOWNLOAD_PUBLIC_ACCESS_RUNTIME_REQUEST_FIELDS
                and _truthy(nested_value)
                and not _is_allowed_false_flag(child_path, lowered, nested_value)
            ):
                found.add(str(key))
            found.update(_find_download_public_access_runtime_requests(nested_value, child_path))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_download_public_access_runtime_requests(item, path))
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
                "file_byte_route",
                "pdf_path",
                "markdown_report_path",
                "briefing_deck_path",
                "evidence_appendix_package_path",
                "zip_path",
                "download_package_path",
                "package_path",
                "runtime_path",
                "local_runtime_path",
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
        or path.endswith(f"export_artifact_boundary_summary.{normalized_field}")
        or path.endswith(f"download_public_access_boundary_readiness_summary.{normalized_field}")
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


def _boundary_id(export_artifact_boundary_id: str | None) -> str:
    return f"export_artifact_boundary_download_public_access_boundary_{_safe_identifier(export_artifact_boundary_id)}"


def _safe_identifier(value: Any) -> str:
    text = str(value or "missing").strip()
    safe = "".join(character if character.isalnum() or character in {"_", "-"} else "_" for character in text)
    return safe[:120] or "missing"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
