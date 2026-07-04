from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


GO_NO_GO_BOUNDARY_SET_SCHEMA = "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_set_v0_1"
GO_NO_GO_BOUNDARY_SCHEMA = "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_production_analysis_result_creation_go_no_go_boundary_summary_v0_1"
SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SET_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_set_v0_1"
)
SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_final_authorization_boundary_v0_1"
)
PHASE = "8W-65"
APPROVAL_PHRASE = (
    "APPROVE_8W_65_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_GO_NO_GO_BOUNDARY_HELPER_IMPLEMENTATION"
)
SOURCE_WARN_STATUS = "production_analysis_result_creation_final_authorization_boundary_set_warn_manual_review_required"
WARN_STATUS = "production_analysis_result_creation_go_no_go_boundary_set_warn_manual_review_required"

GO_NO_GO_BLOCKER_CATEGORIES = [
    "unresolved_warning_or_manual_review_required",
    "missing_human_review_authority",
    "attempted_automatic_trust_upgrade",
    "production_analysis_result_creation_final_authorization_not_performed",
    "production_analysis_result_creation_go_no_go_authorization_not_performed",
    "production_analysis_result_runtime_not_approved",
    "analysis_result_generation_not_approved",
    "actual_analysis_execution_not_approved",
    "production_analysis_run_not_approved",
    "production_case_not_approved",
    "production_evidence_item_creation_not_approved",
    "review_queue_runtime_not_approved",
    "route_api_frontend_not_approved",
    "b_end_report_runtime_not_approved",
    "sandbox_public_event_runtime_not_approved",
    "export_download_public_final_delivery_runtime_not_approved",
    "real_api_llm_provider_collector_not_approved",
    "private_collector_or_real_exchange_dir_access_forbidden",
    "additional_row_parsing_forbidden",
]

FORBIDDEN_SOURCE_FIELDS = {
    "production_analysis_result_id",
    "analysis_result_id",
    "actual_analysis_execution_id",
    "analysis_execution_id",
    "production_analysis_run_id",
    "analysis_run_id",
    "production_case_id",
    "production_evidence_item_id",
    "review_queue_item_id",
    "production_review_queue_item_id",
    "raw_author_id",
    "raw_author_ids",
    "author_id",
    "author_ids",
    "raw_author_name",
    "author_name",
    "author_names",
    "username",
    "user_name",
    "display_name",
    "profile_url",
    "profile_urls",
    "raw_profile_url",
    "raw_comment",
    "raw_comments",
    "raw_identities",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "address",
    "identity_fields",
    "cookie",
    "cookies",
    "token",
    "tokens",
    "session",
    "sessions",
    "password",
    "passwords",
    "api_key",
    "api_keys",
    "secret",
    "secrets",
    "salt",
    "salts",
    "browser_profile_path",
    "absolute_path",
    "package_path",
    "raw_collector_path",
    "generated_response_text",
    "generated_public_message",
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "sentiment_score",
    "risk_score",
    "forecast",
    "narrative",
    "recommendation",
    "strategy",
    "analysis_output",
    "public_conclusion",
    "customer_conclusion",
    "final_conclusion",
}

SOURCE_TRUE_FIELDS = {
    "human_review_required": "source_human_review_required_not_true",
    "no_automatic_trust_upgrade": "source_no_automatic_trust_upgrade_not_true",
    "production_analysis_result_creation_final_authorization_boundary_created": (
        "source_final_authorization_boundary_created_not_true"
    ),
}

SOURCE_FALSE_FIELDS = {
    "production_analysis_result_creation_go_no_go_authorization_performed": (
        "source_go_no_go_authorization_performed_true"
    ),
    "production_analysis_result_creation_final_authorization_performed": (
        "source_final_authorization_performed_true"
    ),
    "production_analysis_result_created": "source_production_analysis_result_created_true",
    "production_analysis_result_creation_executed": "source_production_analysis_result_creation_executed_true",
    "production_analysis_result_runtime_used": "source_production_analysis_result_runtime_used_true",
    "analysis_result_generation_executed": "source_analysis_result_generation_executed_true",
    "analysis_result_created": "source_analysis_result_created_true",
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "analysis_execution_started": "source_analysis_execution_started_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "review_queue_item_created": "source_review_queue_item_created_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "review_queue_runtime_used": "source_review_queue_runtime_used_true",
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_generated": "source_sandbox_public_event_generated_true",
    "generated_response_text": "source_generated_response_text_true",
    "public_route_created": "source_public_route_created_true",
    "download_package_runtime_used": "source_download_package_runtime_used_true",
    "public_access_runtime_used": "source_public_access_runtime_used_true",
    "external_delivery_runtime_used": "source_external_delivery_runtime_used_true",
    "final_delivery_runtime_used": "source_final_delivery_runtime_used_true",
    "analysis_ready": "source_analysis_ready_true",
    "report_ready": "source_report_ready_true",
    "b_end_ready": "source_b_end_ready_true",
    "sandbox_ready": "source_sandbox_ready_true",
    "public_event_ready": "source_public_event_ready_true",
    "route_ready": "source_route_ready_true",
    "frontend_ready": "source_frontend_ready_true",
    "production_ready": "source_production_ready_true",
    "public_ready": "source_public_ready_true",
    "customer_ready": "source_customer_ready_true",
    "additional_row_parsing_performed": "source_additional_row_parsing_performed_true",
    "evidence_items_jsonl_parsed_again": "source_evidence_items_jsonl_parsed_again_true",
    "evidence_items_csv_parsed": "source_evidence_items_csv_true",
    "source_manifest_rows_parsed": "source_source_manifest_rows_parsed_true",
    "collection_log_rows_parsed": "source_collection_log_rows_parsed_true",
    "original_package_rows_read": "source_original_package_rows_read_true",
    "raw_comments_read": "source_raw_comments_read_true",
    "raw_identities_read": "source_raw_identities_read_true",
    "private_collector_inspected": "source_private_collector_inspected_true",
    "private_collector_source_inspected": "source_private_collector_source_inspected_true",
    "real_exchange_dir_read": "source_real_exchange_dir_read_true",
}

RUNTIME_SIDE_EFFECT_FLAGS = [
    "called_real_api",
    "called_real_llm",
    "ran_provider_job",
    "ran_collector",
    "fetched_url",
    "scraped_page",
    "accessed_private_collector",
    "inspected_private_collector_source",
    "read_real_exchange_dir",
    "parsed_evidence_items_jsonl_again",
    "parsed_evidence_items_csv",
    "parsed_source_manifest_jsonl_rows",
    "parsed_collection_log_jsonl_rows",
    "read_original_package_rows",
    "read_private_collector_raw_output",
    "emitted_raw_comments",
    "emitted_raw_identities",
    "emitted_profile_urls",
    "created_production_evidence_items",
    "created_review_queue_items",
    "created_production_review_queue_items",
    "created_production_case",
    "created_production_analysis_run",
    "started_actual_analysis_execution",
    "started_analysis_execution",
    "created_analysis_result",
    "created_production_analysis_result",
    "executed_production_analysis_result_creation",
    "performed_production_analysis_result_creation_final_authorization",
    "performed_production_analysis_result_creation_go_no_go_authorization",
    "used_production_analysis_result_runtime",
    "created_report_candidate",
    "created_final_report",
    "generated_b_end_report_runtime",
    "generated_sandbox_runtime",
    "generated_public_event_runtime",
    "used_report_export_runtime",
    "used_download_package_runtime",
    "used_public_access_runtime",
    "used_external_delivery_runtime",
    "used_final_delivery_runtime",
    "generated_response_text",
    "created_public_route",
    "modified_frontend",
    "published_or_sent",
    "auto_executed",
]


def build_controlled_production_analysis_result_creation_go_no_go_boundary(
    controlled_production_analysis_result_creation_final_authorization_boundary_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))

    source_boundaries: list[dict[str, Any]] = []
    if not blockers:
        source_boundaries = _safe_source_final_authorization_boundaries(
            controlled_production_analysis_result_creation_final_authorization_boundary_set
        )
        blockers.extend(
            _source_final_authorization_boundary_set_blockers(
                controlled_production_analysis_result_creation_final_authorization_boundary_set,
                source_boundaries,
            )
        )

    boundaries: list[dict[str, Any]] = []
    if not blockers:
        boundaries.append(
            _go_no_go_boundary_from_source(
                source_boundaries[0],
                controlled_production_analysis_result_creation_final_authorization_boundary_set,
            )
        )

    status = WARN_STATUS if not blockers else _blocked_status(blockers)
    return _base_output(
        source_final_authorization_boundary_set=controlled_production_analysis_result_creation_final_authorization_boundary_set,
        status=status,
        boundaries=boundaries,
        blockers=blockers,
    )


create_controlled_production_analysis_result_creation_go_no_go_boundary = (
    build_controlled_production_analysis_result_creation_go_no_go_boundary
)


def build_safe_controlled_production_analysis_result_creation_go_no_go_boundary_summary(
    controlled_production_analysis_result_creation_final_authorization_boundary_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
) -> dict[str, Any]:
    boundary_set = build_controlled_production_analysis_result_creation_go_no_go_boundary(
        controlled_production_analysis_result_creation_final_authorization_boundary_set,
        exact_approval_phrase=exact_approval_phrase,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "production_analysis_result_creation_go_no_go_boundary_set_schema": boundary_set[
            "production_analysis_result_creation_go_no_go_boundary_set_schema"
        ],
        "production_analysis_result_creation_go_no_go_boundary_set_status": boundary_set[
            "production_analysis_result_creation_go_no_go_boundary_set_status"
        ],
        "input_source_kind": boundary_set["input_source_kind"],
        "source_production_analysis_result_creation_final_authorization_boundary_set_schema": boundary_set[
            "source_production_analysis_result_creation_final_authorization_boundary_set_schema"
        ],
        "source_production_analysis_result_creation_final_authorization_boundary_schema": boundary_set[
            "source_production_analysis_result_creation_final_authorization_boundary_schema"
        ],
        "source_production_analysis_result_creation_final_authorization_boundary_count": boundary_set[
            "source_production_analysis_result_creation_final_authorization_boundary_count"
        ],
        "production_analysis_result_creation_go_no_go_boundary_count": boundary_set[
            "production_analysis_result_creation_go_no_go_boundary_count"
        ],
        "warning_count": boundary_set["warning_count"],
        "human_review_required": boundary_set["human_review_required"],
        "no_automatic_trust_upgrade": boundary_set["no_automatic_trust_upgrade"],
        "go_no_go_boundary_created": boundary_set["go_no_go_boundary_created"],
        "production_analysis_result_creation_go_no_go_authorization_performed": boundary_set[
            "production_analysis_result_creation_go_no_go_authorization_performed"
        ],
        "production_analysis_result_creation_final_authorization_performed": boundary_set[
            "production_analysis_result_creation_final_authorization_performed"
        ],
        "production_analysis_result_created": boundary_set["production_analysis_result_created"],
        "production_analysis_result_creation_executed": boundary_set[
            "production_analysis_result_creation_executed"
        ],
        "production_analysis_result_runtime_used": boundary_set["production_analysis_result_runtime_used"],
        "analysis_result_generation_executed": boundary_set["analysis_result_generation_executed"],
        "analysis_result_created": boundary_set["analysis_result_created"],
        "actual_analysis_execution_started": boundary_set["actual_analysis_execution_started"],
        "analysis_execution_started": boundary_set["analysis_execution_started"],
        "production_analysis_run_created": boundary_set["production_analysis_run_created"],
        "production_case_created": boundary_set["production_case_created"],
        "production_evidence_item_created": boundary_set["production_evidence_item_created"],
        "review_queue_item_created": boundary_set["review_queue_item_created"],
        "production_review_queue_item_created": boundary_set["production_review_queue_item_created"],
        "review_queue_runtime_used": boundary_set["review_queue_runtime_used"],
        "b_end_report_runtime_generated": boundary_set["b_end_report_runtime_generated"],
        "sandbox_public_event_generated": boundary_set["sandbox_public_event_generated"],
        "generated_response_text": boundary_set["generated_response_text"],
        "public_route_created": boundary_set["public_route_created"],
        "download_package_runtime_used": boundary_set["download_package_runtime_used"],
        "public_access_runtime_used": boundary_set["public_access_runtime_used"],
        "external_delivery_runtime_used": boundary_set["external_delivery_runtime_used"],
        "final_delivery_runtime_used": boundary_set["final_delivery_runtime_used"],
        "go_no_go_blocker_categories": boundary_set["go_no_go_blocker_categories"],
        "boundary_flags": boundary_set["boundary_flags"],
        "runtime_side_effects": boundary_set["runtime_side_effects"],
        "warnings": boundary_set["warnings"],
        "blockers": boundary_set["blockers"],
        "audit_summary": boundary_set["audit_summary"],
        "generated_at": boundary_set["generated_at"],
    }


def _base_output(
    *,
    source_final_authorization_boundary_set: dict[str, Any] | None,
    status: str,
    boundaries: list[dict[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    boundary_created = not blockers and len(boundaries) == 1
    return {
        "production_analysis_result_creation_go_no_go_boundary_set_schema": GO_NO_GO_BOUNDARY_SET_SCHEMA,
        "phase": PHASE,
        "production_analysis_result_creation_go_no_go_boundary_set_status": status,
        "input_source_kind": "controlled_production_analysis_result_creation_final_authorization_boundary",
        "source_production_analysis_result_creation_final_authorization_boundary_set_schema": _safe_source_value(
            source_final_authorization_boundary_set,
            "production_analysis_result_creation_final_authorization_boundary_set_schema",
        )
        or SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SET_SCHEMA,
        "source_production_analysis_result_creation_final_authorization_boundary_schema": (
            _source_final_authorization_boundary_schema(source_final_authorization_boundary_set)
        ),
        "source_production_analysis_result_creation_final_authorization_boundary_count": (
            _source_final_authorization_boundary_count(source_final_authorization_boundary_set)
        ),
        "production_analysis_result_creation_go_no_go_boundary_count": len(boundaries),
        "warning_count": _source_warning_count(source_final_authorization_boundary_set),
        "human_review_required": bool(
            isinstance(source_final_authorization_boundary_set, dict)
            and source_final_authorization_boundary_set.get("human_review_required") is True
        ),
        "no_automatic_trust_upgrade": bool(
            isinstance(source_final_authorization_boundary_set, dict)
            and source_final_authorization_boundary_set.get("no_automatic_trust_upgrade") is True
        ),
        "go_no_go_boundary_created": boundary_created,
        "production_analysis_result_creation_go_no_go_authorization_performed": False,
        "production_analysis_result_creation_final_authorization_performed": False,
        "production_analysis_result_created": False,
        "production_analysis_result_creation_executed": False,
        "production_analysis_result_runtime_used": False,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "actual_analysis_execution_started": False,
        "analysis_execution_started": False,
        "production_analysis_run_created": False,
        "production_case_created": False,
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
        "production_analysis_result_creation_go_no_go_boundaries": boundaries,
        "go_no_go_blocker_categories": list(GO_NO_GO_BLOCKER_CATEGORIES),
        "boundary_flags": _boundary_flags(go_no_go_boundary_only=boundary_created),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _boundary_warnings(source_final_authorization_boundary_set),
        "blockers": _dedupe(blockers),
        "audit_summary": {
            "analysis_effect": "none",
            "production_analysis_result_effect": "none",
            "production_analysis_result_creation_go_no_go_effect": "none",
            "production_analysis_result_creation_final_authorization_effect": "none",
            "production_analysis_result_creation_effect": "none",
            "production_analysis_result_runtime_effect": "none",
            "route_api_frontend_effect": "none",
            "report_public_output_effect": "none",
        },
        "generated_at": _utc_now(),
    }


def _go_no_go_boundary_from_source(
    source_boundary: dict[str, Any],
    source_boundary_set: dict[str, Any] | None,
) -> dict[str, Any]:
    source_ids = _source_final_authorization_boundary_ids(source_boundary)
    return {
        "production_analysis_result_creation_go_no_go_boundary_schema": GO_NO_GO_BOUNDARY_SCHEMA,
        "production_analysis_result_creation_go_no_go_boundary_id": _go_no_go_boundary_id(source_ids),
        "source_production_analysis_result_creation_final_authorization_boundary_ids": source_ids,
        "source_production_analysis_result_creation_final_authorization_boundary_count": (
            _source_final_authorization_boundary_count(source_boundary_set)
        ),
        "case_id_hint": _safe_label(source_boundary.get("case_id_hint")),
        "case_title_or_label_redacted": _safe_label(source_boundary.get("case_title_or_label_redacted")),
        "input_scope_summary_redacted": _safe_label(source_boundary.get("input_scope_summary_redacted")),
        "go_no_go_boundary_only": True,
        "warning_count": _source_warning_count(source_boundary_set),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "go_no_go_blocker_categories": list(GO_NO_GO_BLOCKER_CATEGORIES),
        "production_analysis_result_creation_go_no_go_authorization_performed": False,
        "production_analysis_result_creation_final_authorization_performed": False,
        "production_analysis_result_created": False,
        "production_analysis_result_creation_executed": False,
        "production_analysis_result_runtime_used": False,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "actual_analysis_execution_started": False,
        "analysis_execution_started": False,
        "production_analysis_run_created": False,
        "production_case_created": False,
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
        "b_end_report_runtime_generated": False,
        "sandbox_public_event_generated": False,
        "generated_response_text": False,
        "public_route_created": False,
        "download_package_runtime_used": False,
        "public_access_runtime_used": False,
        "external_delivery_runtime_used": False,
        "final_delivery_runtime_used": False,
        "boundary_flags": _boundary_flags(go_no_go_boundary_only=True),
    }


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        return ["blocked_missing_exact_approval"]
    if not isinstance(exact_approval_phrase, str) or not exact_approval_phrase.isascii():
        return ["blocked_non_ascii_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_approval"]
    return []


def _source_final_authorization_boundary_set_blockers(
    source_boundary_set: dict[str, Any] | None,
    source_boundaries: list[dict[str, Any]],
) -> list[str]:
    blockers: list[str] = []
    if not isinstance(source_boundary_set, dict):
        return ["source_final_authorization_boundary_set_missing"]
    if _contains_forbidden_value(source_boundary_set):
        return ["forbidden_source_payload_detected"]
    if _source_final_authorization_boundary_set_schema(source_boundary_set) != SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SET_SCHEMA:
        blockers.append("source_final_authorization_boundary_set_schema_mismatch")
    if source_boundary_set.get("production_analysis_result_creation_final_authorization_boundary_set_status") != (
        SOURCE_WARN_STATUS
    ):
        blockers.append("source_final_authorization_boundary_set_status_mismatch")
    if _source_final_authorization_boundary_schema(source_boundary_set) != SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SCHEMA:
        blockers.append("source_final_authorization_boundary_schema_mismatch")
    if _source_final_authorization_boundary_count(source_boundary_set) != 1:
        blockers.append("source_final_authorization_boundary_count_not_one")
    if _source_warning_count(source_boundary_set) != 1:
        blockers.append("source_warning_count_not_one")
    for field, reason in SOURCE_TRUE_FIELDS.items():
        if source_boundary_set.get(field) is not True:
            blockers.append(reason)
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if field in source_boundary_set and source_boundary_set.get(field) is not False:
            blockers.append(reason)
    blockers.extend(_runtime_side_effect_blockers(source_boundary_set.get("runtime_side_effects")))
    if source_boundaries == []:
        blockers.append("source_final_authorization_boundary_missing_or_malformed")
    else:
        blockers.extend(_source_final_authorization_boundary_item_blockers(source_boundaries[0]))
    return _dedupe(blockers)


def _source_final_authorization_boundary_item_blockers(source_boundary: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if _contains_forbidden_value(source_boundary):
        return ["forbidden_source_boundary_payload_detected"]
    if source_boundary.get("production_analysis_result_creation_final_authorization_boundary_schema") != (
        SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SCHEMA
    ):
        blockers.append("source_final_authorization_boundary_item_schema_mismatch")
    if source_boundary.get("warning_count") != 1:
        blockers.append("source_final_authorization_boundary_warning_count_not_one")
    if source_boundary.get("human_review_required") is not True:
        blockers.append("source_final_authorization_boundary_human_review_required_not_true")
    if source_boundary.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_final_authorization_boundary_no_automatic_trust_upgrade_not_true")
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if field in source_boundary and source_boundary.get(field) is not False:
            blockers.append(f"source_final_authorization_boundary_{reason.removeprefix('source_')}")
    return _dedupe(blockers)


def _runtime_side_effect_blockers(runtime_side_effects: Any) -> list[str]:
    if runtime_side_effects is None:
        return []
    if not isinstance(runtime_side_effects, dict):
        return ["runtime_side_effects_not_object"]
    return [
        f"runtime_side_effect_true:{flag}"
        for flag in RUNTIME_SIDE_EFFECT_FLAGS
        if runtime_side_effects.get(flag) is not False
    ]


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return WARN_STATUS
    first = blockers[0]
    if first.startswith("blocked_"):
        return first
    if first.startswith("forbidden_"):
        return "blocked_forbidden_field_detected"
    if "warning_count" in first:
        return "blocked_warning_state_missing"
    if "human_review_required" in first:
        return "blocked_manual_review_state_missing"
    if "schema" in first or "status" in first or "count" in first or "missing" in first:
        return "blocked_invalid_source_production_analysis_result_creation_final_authorization_boundary"
    return "blocked_source_boundary_violation"


def _safe_source_final_authorization_boundaries(source_boundary_set: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_boundary_set, dict):
        return []
    boundaries = source_boundary_set.get("production_analysis_result_creation_final_authorization_boundaries")
    if isinstance(boundaries, list):
        return [boundary for boundary in boundaries if isinstance(boundary, dict)]
    return [_summary_final_authorization_boundary_from_source_set(source_boundary_set)]


def _summary_final_authorization_boundary_from_source_set(source_boundary_set: dict[str, Any]) -> dict[str, Any]:
    return {
        "production_analysis_result_creation_final_authorization_boundary_schema": (
            SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SCHEMA
        ),
        "production_analysis_result_creation_final_authorization_boundary_id": _safe_label(
            source_boundary_set.get("production_analysis_result_creation_final_authorization_boundary_id")
        ),
        "case_id_hint": _safe_label(source_boundary_set.get("case_id_hint")),
        "case_title_or_label_redacted": _safe_label(source_boundary_set.get("case_title_or_label_redacted")),
        "input_scope_summary_redacted": _safe_label(source_boundary_set.get("input_scope_summary_redacted")),
        "warning_count": _source_warning_count(source_boundary_set),
        "human_review_required": source_boundary_set.get("human_review_required"),
        "no_automatic_trust_upgrade": source_boundary_set.get("no_automatic_trust_upgrade"),
        "production_analysis_result_creation_go_no_go_authorization_performed": source_boundary_set.get(
            "production_analysis_result_creation_go_no_go_authorization_performed"
        ),
        "production_analysis_result_creation_final_authorization_performed": source_boundary_set.get(
            "production_analysis_result_creation_final_authorization_performed"
        ),
        "production_analysis_result_created": source_boundary_set.get("production_analysis_result_created"),
        "production_analysis_result_creation_executed": source_boundary_set.get(
            "production_analysis_result_creation_executed"
        ),
        "production_analysis_result_runtime_used": source_boundary_set.get(
            "production_analysis_result_runtime_used"
        ),
        "analysis_result_generation_executed": source_boundary_set.get("analysis_result_generation_executed"),
        "analysis_result_created": source_boundary_set.get("analysis_result_created"),
        "actual_analysis_execution_started": source_boundary_set.get("actual_analysis_execution_started"),
        "analysis_execution_started": source_boundary_set.get("analysis_execution_started"),
        "production_analysis_run_created": source_boundary_set.get("production_analysis_run_created"),
        "production_case_created": source_boundary_set.get("production_case_created"),
        "production_evidence_item_created": source_boundary_set.get("production_evidence_item_created"),
        "review_queue_item_created": source_boundary_set.get("review_queue_item_created"),
        "production_review_queue_item_created": source_boundary_set.get("production_review_queue_item_created"),
        "review_queue_runtime_used": source_boundary_set.get("review_queue_runtime_used"),
    }


def _source_final_authorization_boundary_set_schema(source_boundary_set: dict[str, Any] | None) -> str | None:
    if not isinstance(source_boundary_set, dict):
        return None
    value = source_boundary_set.get("production_analysis_result_creation_final_authorization_boundary_set_schema")
    if isinstance(value, str):
        return value
    return None


def _source_final_authorization_boundary_schema(source_boundary_set: dict[str, Any] | None) -> str | None:
    if not isinstance(source_boundary_set, dict):
        return None
    value = source_boundary_set.get("source_production_analysis_result_creation_final_authorization_boundary_schema")
    if isinstance(value, str):
        return value
    boundaries = _safe_source_final_authorization_boundaries(source_boundary_set)
    if boundaries:
        boundary_schema = boundaries[0].get("production_analysis_result_creation_final_authorization_boundary_schema")
        if isinstance(boundary_schema, str):
            return boundary_schema
    return SOURCE_FINAL_AUTHORIZATION_BOUNDARY_SCHEMA


def _source_final_authorization_boundary_count(source_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_boundary_set, dict):
        return 0
    explicit_count = _safe_int(
        source_boundary_set.get("source_production_analysis_result_creation_final_authorization_boundary_count"),
        source_boundary_set.get("production_analysis_result_creation_final_authorization_boundary_count"),
    )
    if explicit_count:
        return explicit_count
    boundaries = source_boundary_set.get("production_analysis_result_creation_final_authorization_boundaries")
    if isinstance(boundaries, list):
        return len([boundary for boundary in boundaries if isinstance(boundary, dict)])
    return 0


def _source_warning_count(source_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_boundary_set, dict):
        return 0
    return _safe_int(source_boundary_set.get("warning_count"))


def _source_final_authorization_boundary_ids(source_boundary: dict[str, Any]) -> list[str]:
    ids = source_boundary.get("source_production_analysis_result_creation_final_authorization_boundary_ids")
    if isinstance(ids, list):
        safe = [_safe_label(item) for item in ids]
        return [item for item in safe if item]
    single = _safe_label(source_boundary.get("production_analysis_result_creation_final_authorization_boundary_id"))
    return [single] if single else []


def _go_no_go_boundary_id(source_ids: list[str]) -> str:
    suffix = "-".join(source_ids) if source_ids else "safe-summary"
    return f"controlled-production-analysis-result-creation-go-no-go-boundary-{_slug(suffix)}"


def _runtime_side_effects() -> dict[str, bool]:
    return {flag: False for flag in RUNTIME_SIDE_EFFECT_FLAGS}


def _boundary_flags(*, go_no_go_boundary_only: bool = False) -> dict[str, bool]:
    return {
        "backend_only": True,
        "local_only": True,
        "go_no_go_boundary_only": go_no_go_boundary_only,
        "controlled_production_analysis_result_creation_final_authorization_boundary_derived_only": True,
        "human_review_required": True,
        "warning_preserving": True,
        "no_automatic_trust_upgrade": True,
        "not_production_analysis_result": True,
        "not_production_analysis_result_creation_go_no_go_authorization": True,
        "not_production_analysis_result_creation_final_authorization": True,
        "not_production_analysis_result_creation_execution": True,
        "not_production_analysis_result_runtime_use": True,
        "not_analysis_result_generation": True,
        "not_actual_analysis_execution": True,
        "not_production_analysis_run": True,
        "not_production_case": True,
        "not_production_evidence_item": True,
        "not_review_queue_runtime": True,
        "not_route_api_frontend": True,
        "not_b_end_report": True,
        "not_sandbox_public_event": True,
        "not_delivery_runtime": True,
        "no_generated_response_text": True,
    }


def _boundary_warnings(source_boundary_set: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_boundary_set, dict):
        warnings.extend(_safe_list(source_boundary_set.get("warnings")))
    return _dedupe(warnings)


def _contains_forbidden_value(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            False
            if key == "runtime_side_effects" and isinstance(item, dict)
            else (key in FORBIDDEN_SOURCE_FIELDS and _forbidden_field_has_payload(item))
            or _contains_forbidden_value(item)
            for key, item in value.items()
        )
    if isinstance(value, list | tuple | set):
        return any(_contains_forbidden_value(item) for item in value)
    if not isinstance(value, str):
        return False
    lowered = value.lower()
    forbidden_fragments = (
        "should-never-appear",
        "private-path",
        "private-collector",
        "raw-comment",
        "raw-identity",
        "actual-token",
        "actual-secret",
        "response-text",
        "public-message",
        "target-user",
        "psych-profile",
    )
    if any(fragment in lowered for fragment in forbidden_fragments):
        return True
    if re.search(r"[a-z]:[/\\]", value, flags=re.IGNORECASE):
        return True
    if value.startswith("/") or value.startswith("\\\\"):
        return True
    return False


def _forbidden_field_has_payload(value: Any) -> bool:
    return value not in (None, False, [], {})


def _safe_source_value(source: dict[str, Any] | None, key: str) -> Any:
    if not isinstance(source, dict):
        return None
    value = source.get(key)
    if isinstance(value, str):
        return _safe_label(value)
    return value


def _safe_label(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if _contains_forbidden_value(value):
        return None
    sanitized = re.sub(r"[^A-Za-z0-9_.:-]+", "-", value.strip()).strip("-")
    return sanitized or None


def _safe_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        safe = _safe_label(item)
        if safe:
            result.append(safe)
    return _dedupe(result)


def _safe_int(*values: Any) -> int:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
    return 0


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def _slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:96] or "safe-summary"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
