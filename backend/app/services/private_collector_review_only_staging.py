from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


ALLOWED_REVIEW_ONLY_ACTIONS = (
    "continue_review",
    "request_more_metadata",
    "mark_manual_review_required",
    "reject_package",
    "block_privacy_issue",
    "request_future_evidence_preview_gate",
    "request_future_dedup_gate",
    "request_future_promotion_gate",
)

BLOCKED_PRODUCTION_ACTIONS = (
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
)

REQUIRED_HANDOFF_FIELDS = (
    "package_name",
    "case_id",
    "validation_status",
    "metadata_only",
    "full_evidence_rows_read",
    "evidence_layer_write",
    "production_case_created",
    "analysis_run_created",
)

FORBIDDEN_ACTUAL_FIELDS = {
    "full_evidence_rows",
    "raw_comment_dump",
    "raw_author_id",
    "raw_author_name",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "browser_profile",
    "profile_path",
    "absolute_package_path",
    "generated_public_message",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}

ALLOWED_SAFETY_MARKERS = {
    "raw_author_id_exported": False,
    "raw_author_name_exported": False,
    "profile_url_exported": False,
    "raw_author_id_removed": True,
    "raw_author_name_removed": True,
    "no_private_messages": True,
}


@dataclass(slots=True)
class ReviewOnlyStagingInputValidationResult:
    status: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ReviewOnlyStagingCandidate:
    staging_candidate_id: str
    analysis_request_id: str | None
    provider_result_id: str | None
    package_name: str | None
    case_id_hint: str | None
    case_title_hint: str | None
    validation_status: str | None
    evidence_count: int | None
    source_count: int | None
    comment_count: int | None
    root_candidate_count: int | None
    warning_count: int | None
    error_count: int | None
    metadata_summary: dict[str, Any]
    validation_summary: dict[str, Any]
    coverage_summary: dict[str, Any]
    review_status: str
    promotion_status: str
    staging_status: str
    blockers: list[str]
    warnings: list[str]
    allowed_actions: tuple[str, ...]
    blocked_actions: tuple[str, ...]
    safety_flags: dict[str, bool]
    audit_refs: list[dict[str, str]]
    created_at: str


@dataclass(slots=True)
class ReviewOnlyStagingGateResult:
    gate_result_id: str
    staging_candidate_id: str
    package_resolution_status: str | None
    provider_result_status: str | None
    privacy_status: str
    path_status: str
    metadata_contract_status: str
    evidence_row_boundary_status: str
    staging_status: str
    blockers: list[str]
    warnings: list[str]
    created_at: str


def validate_review_only_staging_input(handoff_summary: dict[str, Any]) -> ReviewOnlyStagingInputValidationResult:
    if not isinstance(handoff_summary, dict):
        return ReviewOnlyStagingInputValidationResult(
            status="blocked_metadata_contract",
            blockers=["handoff_summary must be a dict"],
        )

    missing = [field_name for field_name in REQUIRED_HANDOFF_FIELDS if field_name not in handoff_summary]
    if missing:
        return ReviewOnlyStagingInputValidationResult(
            status="blocked_metadata_contract",
            blockers=[f"missing required handoff field: {field_name}" for field_name in missing],
        )

    forbidden_fields = sorted(_find_forbidden_fields(handoff_summary))
    if forbidden_fields:
        return ReviewOnlyStagingInputValidationResult(
            status="blocked_privacy_issue",
            blockers=[f"forbidden actual field present: {field_name}" for field_name in forbidden_fields],
            forbidden_fields=forbidden_fields,
        )

    if handoff_summary.get("metadata_only") is not True:
        return ReviewOnlyStagingInputValidationResult(
            status="blocked_metadata_contract",
            blockers=["metadata_only must be true"],
        )

    if handoff_summary.get("full_evidence_rows_read") is True:
        return ReviewOnlyStagingInputValidationResult(
            status="blocked_evidence_rows_in_metadata_stage",
            blockers=["full_evidence_rows_read must be false"],
        )

    production_blockers = [
        flag_name
        for flag_name in ("evidence_layer_write", "production_case_created", "analysis_run_created")
        if handoff_summary.get(flag_name) is True
    ]
    if production_blockers:
        return ReviewOnlyStagingInputValidationResult(
            status="production_import_blocked",
            blockers=[f"{flag_name} must be false" for flag_name in production_blockers],
        )

    smoke_status = str(handoff_summary.get("smoke_status", ""))
    if smoke_status in {
        "live_collection_not_authorized",
        "blocked_missing_package",
        "blocked_path_escape",
        "blocked_privacy_issue",
        "blocked_metadata_contract",
        "blocked_unsupported_platform",
    }:
        return ReviewOnlyStagingInputValidationResult(
            status=smoke_status,
            blockers=list(handoff_summary.get("blockers") or [smoke_status]),
            warnings=list(handoff_summary.get("warnings") or []),
        )

    if smoke_status == "manual_review_required" or handoff_summary.get("validation_status") == "warn":
        return ReviewOnlyStagingInputValidationResult(
            status="metadata_validation_warn",
            blockers=list(handoff_summary.get("blockers") or []),
            warnings=list(handoff_summary.get("warnings") or ["metadata validation warning requires manual review"]),
        )

    return ReviewOnlyStagingInputValidationResult(
        status="ready_for_human_review",
        blockers=list(handoff_summary.get("blockers") or []),
        warnings=list(handoff_summary.get("warnings") or []),
    )


def create_review_only_staging_candidate(
    handoff_summary: dict[str, Any],
    requested_by: str = "internal_operator",
) -> ReviewOnlyStagingCandidate:
    validation = validate_review_only_staging_input(handoff_summary)
    created_at = _utc_now()
    review_status = "ready_for_human_review" if validation.status == "ready_for_human_review" else "manual_review_required"
    promotion_status = "promotion_required"
    return ReviewOnlyStagingCandidate(
        staging_candidate_id=f"review_staging_candidate_{uuid4().hex}",
        analysis_request_id=_safe_str(handoff_summary.get("case_id")),
        provider_result_id=_safe_str(handoff_summary.get("provider_result_id")),
        package_name=_safe_str(handoff_summary.get("package_name")),
        case_id_hint=_safe_str(handoff_summary.get("case_id")),
        case_title_hint=_safe_str(handoff_summary.get("case_title_hint")),
        validation_status=_safe_str(handoff_summary.get("validation_status")),
        evidence_count=_safe_int(handoff_summary.get("evidence_count")),
        source_count=_safe_int(handoff_summary.get("source_count")),
        comment_count=_safe_int(handoff_summary.get("comment_count")),
        root_candidate_count=_safe_int(handoff_summary.get("root_candidate_count")),
        warning_count=_safe_int(handoff_summary.get("warning_count")),
        error_count=_safe_int(handoff_summary.get("error_count")),
        metadata_summary=_metadata_summary(handoff_summary),
        validation_summary=_validation_summary(handoff_summary),
        coverage_summary=_coverage_summary(handoff_summary),
        review_status=review_status,
        promotion_status=promotion_status,
        staging_status=validation.status,
        blockers=list(validation.blockers),
        warnings=list(validation.warnings),
        allowed_actions=ALLOWED_REVIEW_ONLY_ACTIONS,
        blocked_actions=BLOCKED_PRODUCTION_ACTIONS,
        safety_flags=_safety_flags(),
        audit_refs=[
            {
                "audit_ref_id": f"review_staging_audit_ref_{uuid4().hex}",
                "actor_type": requested_by,
                "action": "create_review_only_staging_candidate",
                "scope": "metadata_only",
            }
        ],
        created_at=created_at,
    )


def build_review_only_staging_gate_result(
    handoff_summary: dict[str, Any],
    candidate: ReviewOnlyStagingCandidate,
) -> ReviewOnlyStagingGateResult:
    privacy_status = "blocked_privacy_issue" if candidate.staging_status == "blocked_privacy_issue" else "clear"
    path_status = str(handoff_summary.get("package_resolution_status") or "unknown")
    metadata_contract_status = (
        "blocked_metadata_contract" if candidate.staging_status == "blocked_metadata_contract" else "metadata_contract_ok"
    )
    evidence_row_boundary_status = (
        "blocked_evidence_rows_in_metadata_stage"
        if candidate.staging_status == "blocked_evidence_rows_in_metadata_stage"
        else "evidence_rows_not_read"
    )
    return ReviewOnlyStagingGateResult(
        gate_result_id=f"review_staging_gate_{uuid4().hex}",
        staging_candidate_id=candidate.staging_candidate_id,
        package_resolution_status=_safe_str(handoff_summary.get("package_resolution_status")),
        provider_result_status=_safe_str(handoff_summary.get("provider_result_status")),
        privacy_status=privacy_status,
        path_status=path_status,
        metadata_contract_status=metadata_contract_status,
        evidence_row_boundary_status=evidence_row_boundary_status,
        staging_status=candidate.staging_status,
        blockers=list(candidate.blockers),
        warnings=list(candidate.warnings),
        created_at=_utc_now(),
    )


def build_safe_review_only_staging_summary(
    candidate: ReviewOnlyStagingCandidate,
    gate_result: ReviewOnlyStagingGateResult,
) -> dict[str, Any]:
    return {
        "schema": "sentigraph_review_only_staging_summary_v0_1",
        "staging_candidate_id": candidate.staging_candidate_id,
        "gate_result_id": gate_result.gate_result_id,
        "analysis_request_id": candidate.analysis_request_id,
        "provider_result_id": candidate.provider_result_id,
        "package_name": candidate.package_name,
        "case_id_hint": candidate.case_id_hint,
        "case_title_hint": candidate.case_title_hint,
        "validation_status": candidate.validation_status,
        "evidence_count": candidate.evidence_count,
        "source_count": candidate.source_count,
        "comment_count": candidate.comment_count,
        "root_candidate_count": candidate.root_candidate_count,
        "warning_count": candidate.warning_count,
        "error_count": candidate.error_count,
        "review_status": candidate.review_status,
        "promotion_status": candidate.promotion_status,
        "staging_status": candidate.staging_status,
        "blockers": list(candidate.blockers),
        "warnings": list(candidate.warnings),
        "allowed_actions": list(candidate.allowed_actions),
        "blocked_actions": list(candidate.blocked_actions),
        "safety_flags": dict(candidate.safety_flags),
        "audit_refs": list(candidate.audit_refs),
        "gate_result": {
            "package_resolution_status": gate_result.package_resolution_status,
            "provider_result_status": gate_result.provider_result_status,
            "privacy_status": gate_result.privacy_status,
            "path_status": gate_result.path_status,
            "metadata_contract_status": gate_result.metadata_contract_status,
            "evidence_row_boundary_status": gate_result.evidence_row_boundary_status,
            "staging_status": gate_result.staging_status,
        },
        "metadata_only": True,
        "path_exposed": False,
        "path_reference": "review_only_metadata_summary",
    }


def _find_forbidden_fields(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, nested_value in value.items():
            key_text = str(key)
            lowered_key = key_text.lower()
            if lowered_key in ALLOWED_SAFETY_MARKERS and nested_value is ALLOWED_SAFETY_MARKERS[lowered_key]:
                continue
            if lowered_key in FORBIDDEN_ACTUAL_FIELDS:
                found.add(key_text)
            found.update(_find_forbidden_fields(nested_value))
    elif isinstance(value, list):
        for item in value:
            found.update(_find_forbidden_fields(item))
    return found


def _metadata_summary(handoff_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_count": _safe_int(handoff_summary.get("evidence_count")),
        "source_count": _safe_int(handoff_summary.get("source_count")),
        "comment_count": _safe_int(handoff_summary.get("comment_count")),
        "root_candidate_count": _safe_int(handoff_summary.get("root_candidate_count")),
        "package_name": _safe_str(handoff_summary.get("package_name")),
    }


def _validation_summary(handoff_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": _safe_str(handoff_summary.get("validation_status")),
        "warnings": _safe_int(handoff_summary.get("warning_count")),
        "errors": _safe_int(handoff_summary.get("error_count")),
    }


def _coverage_summary(handoff_summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_count": _safe_int(handoff_summary.get("evidence_count")),
        "source_count": _safe_int(handoff_summary.get("source_count")),
        "comment_count": _safe_int(handoff_summary.get("comment_count")),
        "root_candidate_count": _safe_int(handoff_summary.get("root_candidate_count")),
        "coverage_note": _safe_str(handoff_summary.get("coverage_note")),
        "coverage_note_present": bool(handoff_summary.get("coverage_note")),
        "not_full_web": True,
        "not_full_platform": True,
    }


def _safety_flags() -> dict[str, bool]:
    return {
        "metadata_only": True,
        "review_only_staging_helper_only": True,
        "runtime_file_written": False,
        "persistent_staging_storage_created": False,
        "collector_run": False,
        "live_crawl": False,
        "browser_automation": False,
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
        "frontend_api_route_added": False,
        "project_source_changed": False,
        "github_actions_recreated": False,
    }


def _safe_int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def _safe_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
