from __future__ import annotations

import os
from typing import Any, NamedTuple

from fastapi import APIRouter


router = APIRouter()

ENV_FLAG = "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED"
SYNTHETIC_CANDIDATE_ID = "synthetic_review_staging_candidate"

ALLOWED_ACTIONS = [
    "continue_review",
    "request_more_metadata",
    "mark_manual_review_required",
    "reject_package",
    "block_privacy_issue",
    "request_future_evidence_preview_gate",
    "request_future_dedup_gate",
    "request_future_promotion_gate",
]

BLOCKED_ACTIONS = [
    "approve_production_evidence",
    "create_production_case",
    "start_analysis_run",
    "generate_report",
    "generate_public_event",
    "generate_public_response",
    "publish",
    "send",
    "post",
    "execute",
    "target_individuals",
]


class _InternalOperatorRouteEnabledMode(NamedTuple):
    enabled: bool
    mode: str
    disabled_reason: str | None


@router.get("/candidates")
def list_review_only_staging_candidates() -> dict[str, Any]:
    if not _route_enabled():
        return _safe_error("route_disabled", "Review-only staging route is disabled.")
    response = _base_response("internal_operator_review_only_staging_response_list_v0_1")
    response["candidates"] = [_safe_candidate_summary()]
    response["count"] = 1
    return response


@router.get("/candidates/{staging_candidate_id}")
def get_review_only_staging_candidate(staging_candidate_id: str) -> dict[str, Any]:
    if not _route_enabled():
        return _safe_error("route_disabled", "Review-only staging route is disabled.")
    if staging_candidate_id != SYNTHETIC_CANDIDATE_ID:
        return _safe_error("not_found", "Review-only staging candidate was not found.")
    return _safe_candidate_response()


def _route_enabled() -> bool:
    return _resolve_internal_operator_route_enabled_mode(os.environ.get(ENV_FLAG)).enabled


def _resolve_internal_operator_route_enabled_mode(
    raw_env_value: str | None,
) -> _InternalOperatorRouteEnabledMode:
    normalized_value = (raw_env_value or "").strip().lower()
    if normalized_value in {"1", "true", "yes"}:
        return _InternalOperatorRouteEnabledMode(
            enabled=True,
            mode="synthetic_fixture_only",
            disabled_reason=None,
        )
    return _InternalOperatorRouteEnabledMode(
        enabled=False,
        mode="disabled",
        disabled_reason="route_disabled",
    )


def _safe_error(error_code: str, message: str) -> dict[str, Any]:
    return {
        "schema": "internal_operator_review_only_staging_error_v0_1",
        "route_scope": "internal_operator",
        "access_scope": "local_or_disabled_by_default",
        "metadata_only": True,
        "review_only": True,
        "error_code": error_code,
        "message": message,
        "blockers": [error_code],
        "warnings": [],
        "path_exposed": False,
        "raw_metadata_exposed": False,
    }


def _base_response(schema: str) -> dict[str, Any]:
    return {
        "schema": schema,
        "route_scope": "internal_operator",
        "access_scope": "local_or_disabled_by_default",
        "metadata_only": True,
        "review_only": True,
        "production_import_allowed": False,
        "evidence_layer_write_allowed": False,
        "production_case_creation_allowed": False,
        "analysis_run_allowed": False,
        "public_output_allowed": False,
        "allowed_actions": list(ALLOWED_ACTIONS),
        "blocked_actions": list(BLOCKED_ACTIONS),
        "safety_flags": _safety_flags(),
        "warnings": [],
        "blockers": [],
        "audit_refs": [_safe_audit_ref()],
    }


def _safe_candidate_response() -> dict[str, Any]:
    response = _base_response("internal_operator_review_only_staging_response_v0_1")
    response["staging_candidate_id"] = SYNTHETIC_CANDIDATE_ID
    response["staging_candidate"] = _safe_candidate_summary()
    response["gate_summary"] = _safe_gate_summary()
    return response


def _safe_candidate_summary() -> dict[str, Any]:
    return {
        "staging_candidate_id": SYNTHETIC_CANDIDATE_ID,
        "analysis_request_id": "synthetic_analysis_request",
        "provider_result_id": "synthetic_provider_result",
        "package_name": "synthetic_package",
        "case_id_hint": "synthetic_case",
        "case_title_hint": "Synthetic review-only staging candidate",
        "validation_status": "passed",
        "evidence_count": 34,
        "source_count": 7,
        "warning_count": 0,
        "error_count": 0,
        "metadata_summary": {
            "evidence_count": 34,
            "source_count": 7,
            "package_name": "synthetic_package",
        },
        "validation_summary": {
            "status": "passed",
            "warnings": 0,
            "errors": 0,
        },
        "coverage_summary": {
            "coverage_note_present": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "review_status": "ready_for_human_review",
        "promotion_status": "promotion_required",
        "created_at": "2026-06-29T00:00:00Z",
    }


def _safe_gate_summary() -> dict[str, str]:
    return {
        "package_resolution_status": "accepted_metadata_only",
        "provider_result_status": "accepted_metadata_only",
        "privacy_status": "clear",
        "path_status": "accepted_metadata_only",
        "metadata_contract_status": "metadata_contract_ok",
        "evidence_row_boundary_status": "evidence_rows_not_read",
        "staging_status": "ready_for_human_review",
    }


def _safe_audit_ref() -> dict[str, str]:
    return {
        "audit_ref_id": "synthetic_review_staging_audit_ref",
        "actor_type": "internal_operator",
        "action": "create_review_only_staging_candidate",
        "scope": "metadata_only",
    }


def _safety_flags() -> dict[str, bool]:
    return {
        "collector_run": False,
        "live_crawl": False,
        "real_api_called": False,
        "real_llm_called": False,
        "url_fetching": False,
        "scraping": False,
        "full_evidence_rows_parsed": False,
        "evidence_items_jsonl_parsed": False,
        "evidence_items_csv_parsed": False,
        "raw_comments_printed": False,
        "raw_author_identifiers_printed": False,
        "secrets_read": False,
        "evidence_layer_written": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_runtime_generated": False,
        "persistent_staging_storage_created": False,
    }
