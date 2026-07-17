from __future__ import annotations

import os
from typing import Any, NamedTuple

from fastapi import APIRouter

from app.services.internal_alpha_review_console_safe_metadata_projection import (
    APPROVAL_PHRASE as PROJECTION_APPROVAL_PHRASE,
    build_internal_alpha_review_console_safe_metadata_projection,
)
from app.services.internal_alpha_local_exchange_review_projection import (
    build_internal_alpha_local_exchange_review_projection,
)
from app.services.governed_nonproduction_review_console_projection import (
    PROJECTION_FIELDS as GOVERNED_RECORD_PROJECTION_FIELDS,
    build_governed_nonproduction_review_console_projection,
)


router = APIRouter()

ENV_FLAG = "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED"
GOVERNED_RECORD_ENV_FLAG = (
    "SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_ENABLED"
)
ROUTE_MODE = "disabled_by_default_internal_safe_projection_route_skeleton"
GOVERNED_RECORD_PROJECTION_ID = "governed-nonproduction-record-review-v0-1"
ALLOWED_PROJECTION_IDS = {
    "internal-alpha-safe-projection-fixture",
    "8z16-no-write-alpha-fixture",
}


@router.get("/local-exchange-projections/{sample_handle}")
def get_internal_alpha_local_exchange_review_projection(
    sample_handle: str,
) -> dict[str, Any]:
    return build_internal_alpha_local_exchange_review_projection(sample_handle)


class _RouteEnabledMode(NamedTuple):
    enabled: bool
    mode: str
    disabled_reason: str | None


@router.get("/projections/{projection_id}")
def get_internal_alpha_review_console_projection(projection_id: str) -> dict[str, Any]:
    if not _route_enabled():
        return _safe_error("route_disabled", projection_id=None)

    if projection_id == GOVERNED_RECORD_PROJECTION_ID:
        if not _governed_record_projection_enabled():
            return _safe_error(
                "governed_record_projection_disabled",
                projection_id=None,
            )
        projection = build_governed_nonproduction_review_console_projection()
        return _safe_governed_record_response(projection)

    if projection_id not in ALLOWED_PROJECTION_IDS:
        return _safe_error("unsupported_projection", projection_id="unsupported")

    projection = build_internal_alpha_review_console_safe_metadata_projection(
        _safe_projection_source_fixture(projection_id),
        exact_approval_phrase=PROJECTION_APPROVAL_PHRASE,
    )
    if projection.get("projection_created") is not True:
        return _safe_error("projection_unavailable", projection_id=projection_id)

    safe_projection = _safe_route_projection(projection)
    return {
        "response_schema": "sentigraph_internal_alpha_review_console_route_response_v0_1",
        "route_mode": ROUTE_MODE,
        "projection_id": projection_id,
        "projection": safe_projection,
        "projection_schema": safe_projection["projection_schema"],
        "projection_mode": safe_projection["projection_mode"],
        "source_chain_boundary": safe_projection["source_chain_boundary"],
        "safe_metadata_only": True,
        "label_only_operator_outcomes": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "route_ready": "skeleton_only",
        "frontend_ready": False,
        "runtime_ready": False,
        "public_ready": False,
        "production_ready": False,
        "actual_write_enabled": False,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "source11_runtime_enabled": False,
        "finalsummaryreport_runtime_enabled": False,
    }


def _route_enabled() -> bool:
    return _resolve_internal_alpha_review_console_route_enabled_mode(os.environ.get(ENV_FLAG)).enabled


def _governed_record_projection_enabled() -> bool:
    return _resolve_internal_alpha_review_console_route_enabled_mode(
        os.environ.get(GOVERNED_RECORD_ENV_FLAG)
    ).enabled


def _resolve_internal_alpha_review_console_route_enabled_mode(raw_env_value: str | None) -> _RouteEnabledMode:
    normalized_value = (raw_env_value or "").strip().lower()
    if normalized_value in {"1", "true", "yes"}:
        return _RouteEnabledMode(
            enabled=True,
            mode="synthetic_fixture_only",
            disabled_reason=None,
        )
    return _RouteEnabledMode(
        enabled=False,
        mode="disabled",
        disabled_reason="route_disabled",
    )


def _safe_error(error: str, *, projection_id: str | None) -> dict[str, Any]:
    response: dict[str, Any] = {
        "response_schema": "sentigraph_internal_alpha_review_console_route_error_v0_1",
        "route_mode": ROUTE_MODE,
        "error": error,
        "path_exposed": False,
        "raw_metadata_exposed": False,
        "raw_rows_exposed": False,
        "secrets_exposed": False,
        "route_ready": False,
        "frontend_ready": False,
        "runtime_ready": False,
        "production_ready": False,
        "public_ready": False,
        "actual_write_enabled": False,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "source11_runtime_enabled": False,
        "finalsummaryreport_runtime_enabled": False,
        "blockers": [error],
        "warnings": [],
    }
    if projection_id is not None:
        response["projection_id"] = projection_id
    return response


def _safe_governed_record_response(projection: dict[str, Any]) -> dict[str, Any]:
    if tuple(projection) != GOVERNED_RECORD_PROJECTION_FIELDS:
        return _safe_error(
            "governed_record_projection_unavailable",
            projection_id=None,
        )
    return {
        "response_schema": (
            "sentigraph_internal_alpha_review_console_"
            "governed_record_route_response_v0_1"
        ),
        "route_mode": ROUTE_MODE,
        "projection_id": GOVERNED_RECORD_PROJECTION_ID,
        "projection": projection,
        "projection_schema": projection["projection_schema"],
        "projection_status": projection["projection_status"],
        "source_chain_boundary": projection["source_chain_boundary"],
        "safe_metadata_only": True,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "actual_write_enabled": False,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "operator_runtime_ready": False,
        "public_ready": False,
        "production_ready": False,
    }


def _safe_projection_source_fixture(projection_id: str) -> dict[str, Any]:
    return {
        "source_summary_schema": "sentigraph_internal_alpha_no_write_governance_chain_summary_v0_1",
        "request_id": f"{projection_id}_request",
        "provider_result_id": f"{projection_id}_provider_result",
        "package_reference": f"{projection_id}_opaque_package_ref",
        "stage_id": f"{projection_id}_stage",
        "stage_schema": "sentigraph_internal_alpha_stage_summary_v0_1",
        "stage_status": "warn_manual_review_required",
        "stage_mode": "backend_only_local_no_write_governance_chain",
        "candidate_id": f"{projection_id}_write_candidate_boundary",
        "boundary_id": f"{projection_id}_boundary",
        "source_chain_boundary": "evidence_layer_write_candidate_boundary",
        "evidence_count": 3,
        "source_count": 2,
        "warning_count": 1,
        "blocker_count": 0,
        "coverage_note_summary": "selected sample only; not full-web coverage",
        "validation_summary": "synthetic local route skeleton projection fixture",
        "safety_flags": {
            "safe_metadata_only": True,
            "raw_identity_exposed": False,
            "secrets_read": False,
        },
        "boundary_flags": {
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_official_verification": True,
            "not_causal_proof": True,
            "no_actual_write": True,
        },
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "audit_refs": [f"{projection_id}_audit_ref"],
        "health_report_refs": ["sentigraph_8z_20_safe_metadata_projection_helper_smoke"],
        "allowed_actions": [
            "keep_paused",
            "needs_more_review",
            "blocked_privacy_or_raw_identity_risk",
            "blocked_missing_authority",
            "candidate_ready_for_future_docs_only_write_gate_discussion",
        ],
        "blocked_actions": [
            "actual_write_blocked",
            "route_api_blocked",
            "frontend_blocked",
            "runtime_blocked",
        ],
        "next_gate_inactive_phrase_labels": [
            "inactive_future_route_skeleton_completion_gate_phrase_required",
        ],
        "actual_evidence_layer_write_used": False,
        "evidence_layer_write": False,
        "persisted_evidence_layer_record_created": False,
        "production_evidence_item_created": False,
        "review_queue_runtime_used": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "actual_analysis_execution_started": False,
        "production_analysis_result_authorized": False,
        "production_analysis_result_created": False,
        "source11_runtime_called": False,
        "finalsummaryreport_runtime_called": False,
        "public_delivery_created": False,
        "export_download_public_delivery_created": False,
        "collector_job_run": False,
        "provider_job_run": False,
        "real_exchange_dir_read": False,
        "real_package_dir_read": False,
        "production_package_rows_parsed": False,
        "raw_rows_exposed": False,
        "raw_comments_exposed": False,
        "raw_identities_exposed": False,
        "secrets_read": False,
        "route_changed": False,
        "api_route_added": False,
        "frontend_changed": False,
        "runtime_changed": False,
        "route_ready": False,
        "frontend_ready": False,
        "runtime_ready": False,
        "public_ready": False,
        "production_ready": False,
        "actual_write_enabled": False,
        "production_object_enabled": False,
        "review_queue_runtime_enabled": False,
        "source11_runtime_enabled": False,
        "finalsummaryreport_runtime_enabled": False,
    }


def _safe_route_projection(projection: dict[str, Any]) -> dict[str, Any]:
    allowed_fields = [
        "projection_schema",
        "phase",
        "projection_status",
        "projection_created",
        "created_at",
        "projection_mode",
        "source_chain_boundary",
        "safe_metadata_only",
        "label_only_operator_outcomes",
        "request_id",
        "provider_result_id",
        "package_reference",
        "stage_summary",
        "candidate_id",
        "boundary_id",
        "evidence_count",
        "source_count",
        "warning_count",
        "blocker_count",
        "coverage_note_summary",
        "validation_summary",
        "safety_flags",
        "boundary_flags",
        "audit_refs",
        "health_report_refs",
        "allowed_actions",
        "blocked_actions",
        "next_gate_inactive_phrase_labels",
        "human_review_required",
        "no_automatic_trust_upgrade",
        "blockers",
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
    ]
    return {field: projection[field] for field in allowed_fields if field in projection}
