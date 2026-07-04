from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


EXECUTION_BOUNDARY_SET_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_execution_boundary_set_v0_1"
)
EXECUTION_BOUNDARY_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_execution_boundary_v0_1"
)
SUMMARY_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_execution_boundary_summary_v0_1"
)
SOURCE_RUNTIME_BOUNDARY_SET_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_runtime_boundary_set_v0_1"
)
SOURCE_RUNTIME_BOUNDARY_SCHEMA = (
    "sentigraph_controlled_production_analysis_result_creation_runtime_boundary_v0_1"
)
PHASE = "8W-61"
APPROVAL_PHRASE = (
    "APPROVE_8W_61_CONTROLLED_PRODUCTION_ANALYSIS_RESULT_CREATION_EXECUTION_BOUNDARY_HELPER_IMPLEMENTATION"
)
SOURCE_WARN_STATUS = "production_analysis_result_creation_runtime_boundary_set_warn_manual_review_required"
WARN_STATUS = "production_analysis_result_creation_execution_boundary_set_warn_manual_review_required"
EXPECTED_8W60_DECISION = "ready"
EXPECTED_8W60_NEXT_BOUNDARY_OPTION = (
    "ready_for_8W_61_controlled_production_analysis_result_creation_execution_boundary_helper_implementation_after_explicit_approval"
)

EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_RUNTIME_BOUNDARY_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_BOUNDARY_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_OR_RUNTIME_EXECUTION_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_RUNTIME_BOUNDARY_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_BOUNDARY_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_ANALYSIS_RESULT_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT = 5

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
    "response_text",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "review_action",
    "reviewer_assignment",
    "review_decision",
    "audit_timeline",
    "report_id",
    "sandbox_id",
    "public_event_id",
    "download_id",
    "public_access_id",
    "delivery_id",
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

REQUESTED_ACTIONS_BLOCKED = {
    "production_analysis_result",
    "production_analysis_result_creation",
    "production_analysis_result_creation_execution",
    "production_analysis_result_runtime",
    "analysis_result_generation",
    "actual_analysis_execution",
    "analysis_execution",
    "production_analysis_run",
    "production_case",
    "production_evidence_item",
    "review_queue_item_creation",
    "production_review_queue_item_creation",
    "review_queue_runtime",
    "frontend_route",
    "route_api",
    "b_end_report",
    "sandbox_public_event",
    "download_package",
    "public_access",
    "external_delivery",
    "final_delivery",
    "real_api",
    "real_llm",
    "provider_job",
    "collector_job",
    "row_parsing",
    "private_collector",
    "real_exchange",
    "publish",
    "send",
    "post",
    "execute",
    "auto_execute",
}

SOURCE_TRUE_FIELDS = {
    "human_review_required": "source_human_review_required_not_true",
    "no_automatic_trust_upgrade": "source_no_automatic_trust_upgrade_not_true",
    "production_analysis_result_creation_runtime_boundary_created": (
        "source_production_analysis_result_creation_runtime_boundary_created_not_true"
    ),
    "production_analysis_result_creation_boundary_created": (
        "source_production_analysis_result_creation_boundary_created_not_true"
    ),
}

SOURCE_FALSE_FIELDS = {
    "production_analysis_result_created": "source_production_analysis_result_created_true",
    "production_analysis_result_creation_executed": (
        "source_production_analysis_result_creation_executed_true"
    ),
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
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_generated": "source_sandbox_public_event_generated_true",
    "generated_response_text": "source_generated_response_text_true",
    "public_route_created": "source_public_route_created_true",
    "frontend_integration_approved": "source_frontend_integration_approved_true",
    "download_package_runtime_used": "source_download_package_runtime_used_true",
    "public_access_runtime_used": "source_public_access_runtime_used_true",
    "external_delivery_runtime_used": "source_external_delivery_runtime_used_true",
    "final_delivery_runtime_used": "source_final_delivery_runtime_used_true",
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


def build_controlled_production_analysis_result_creation_execution_boundary_set(
    controlled_production_analysis_result_creation_runtime_boundary_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    decision_8w60: str | None,
    selected_next_boundary_option_8w60: str | None,
    requested_actions: list[str] | dict[str, Any] | None = None,
    execution_boundary_count: int = 1,
) -> dict[str, Any]:
    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))
    if execution_boundary_count != 1:
        blockers.append("creation_execution_boundary_count_not_one")

    source_boundaries: list[dict[str, Any]] = []
    if not blockers:
        source_boundaries = _safe_source_runtime_boundaries(
            controlled_production_analysis_result_creation_runtime_boundary_set
        )
        blockers.extend(
            _source_runtime_boundary_set_blockers(
                controlled_production_analysis_result_creation_runtime_boundary_set,
                source_boundaries,
                decision_8w60=decision_8w60,
                selected_next_boundary_option_8w60=selected_next_boundary_option_8w60,
            )
        )

    boundaries: list[dict[str, Any]] = []
    if not blockers:
        blockers.extend(
            _source_runtime_boundary_blockers(
                controlled_production_analysis_result_creation_runtime_boundary_set,
                source_boundaries,
            )
        )
        if not blockers:
            boundaries.append(
                _creation_execution_boundary_from_source(
                    source_boundaries[0],
                    controlled_production_analysis_result_creation_runtime_boundary_set,
                )
            )

    status = WARN_STATUS if not blockers else _blocked_status(blockers)
    return _base_output(
        source_runtime_boundary_set=controlled_production_analysis_result_creation_runtime_boundary_set,
        status=status,
        boundaries=boundaries,
        blockers=blockers,
    )


create_controlled_production_analysis_result_creation_execution_boundary_set = (
    build_controlled_production_analysis_result_creation_execution_boundary_set
)


def build_safe_controlled_production_analysis_result_creation_execution_boundary_summary(
    controlled_production_analysis_result_creation_runtime_boundary_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    decision_8w60: str | None,
    selected_next_boundary_option_8w60: str | None,
) -> dict[str, Any]:
    boundary_set = build_controlled_production_analysis_result_creation_execution_boundary_set(
        controlled_production_analysis_result_creation_runtime_boundary_set,
        exact_approval_phrase=exact_approval_phrase,
        decision_8w60=decision_8w60,
        selected_next_boundary_option_8w60=selected_next_boundary_option_8w60,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "production_analysis_result_creation_execution_boundary_set_schema": boundary_set[
            "production_analysis_result_creation_execution_boundary_set_schema"
        ],
        "production_analysis_result_creation_execution_boundary_set_status": boundary_set[
            "production_analysis_result_creation_execution_boundary_set_status"
        ],
        "input_source_kind": boundary_set["input_source_kind"],
        "source_production_analysis_result_creation_runtime_boundary_set_schema": boundary_set[
            "source_production_analysis_result_creation_runtime_boundary_set_schema"
        ],
        "source_production_analysis_result_creation_runtime_boundary_schema": boundary_set[
            "source_production_analysis_result_creation_runtime_boundary_schema"
        ],
        "source_production_analysis_result_creation_runtime_boundary_count": boundary_set[
            "source_production_analysis_result_creation_runtime_boundary_count"
        ],
        "source_production_analysis_result_creation_candidate_count": boundary_set[
            "source_production_analysis_result_creation_candidate_count"
        ],
        "source_production_analysis_result_creation_boundary_count": boundary_set[
            "source_production_analysis_result_creation_boundary_count"
        ],
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": boundary_set[
            "source_production_analysis_result_creation_or_runtime_execution_candidate_count"
        ],
        "source_production_analysis_result_runtime_boundary_count": boundary_set[
            "source_production_analysis_result_runtime_boundary_count"
        ],
        "source_production_analysis_result_boundary_count": boundary_set[
            "source_production_analysis_result_boundary_count"
        ],
        "source_production_analysis_result_candidate_count": boundary_set[
            "source_production_analysis_result_candidate_count"
        ],
        "source_analysis_result_candidate_count": boundary_set["source_analysis_result_candidate_count"],
        "source_actual_analysis_execution_candidate_count": boundary_set[
            "source_actual_analysis_execution_candidate_count"
        ],
        "source_production_analysis_run_candidate_count": boundary_set[
            "source_production_analysis_run_candidate_count"
        ],
        "source_production_case_candidate_count": boundary_set["source_production_case_candidate_count"],
        "source_controlled_evidence_item_count": boundary_set["source_controlled_evidence_item_count"],
        "creation_execution_boundary_mode": boundary_set["creation_execution_boundary_mode"],
        "production_analysis_result_creation_execution_boundary_count": boundary_set[
            "production_analysis_result_creation_execution_boundary_count"
        ],
        "warning_count": boundary_set["warning_count"],
        "human_review_required": boundary_set["human_review_required"],
        "no_automatic_trust_upgrade": boundary_set["no_automatic_trust_upgrade"],
        "production_analysis_result_creation_runtime_boundary_created_upstream": boundary_set[
            "production_analysis_result_creation_runtime_boundary_created_upstream"
        ],
        "production_analysis_result_creation_execution_boundary_created": boundary_set[
            "production_analysis_result_creation_execution_boundary_created"
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
        "analysis_ready": boundary_set["analysis_ready"],
        "report_ready": boundary_set["report_ready"],
        "b_end_ready": boundary_set["b_end_ready"],
        "sandbox_ready": boundary_set["sandbox_ready"],
        "public_event_ready": boundary_set["public_event_ready"],
        "route_ready": boundary_set["route_ready"],
        "frontend_ready": boundary_set["frontend_ready"],
        "production_ready": boundary_set["production_ready"],
        "public_ready": boundary_set["public_ready"],
        "customer_ready": boundary_set["customer_ready"],
        "boundary_flags": boundary_set["boundary_flags"],
        "runtime_side_effects": boundary_set["runtime_side_effects"],
        "warnings": boundary_set["warnings"],
        "blockers": boundary_set["blockers"],
        "audit_summary": boundary_set["audit_summary"],
        "generated_at": boundary_set["generated_at"],
    }


def _base_output(
    *,
    source_runtime_boundary_set: dict[str, Any] | None,
    status: str,
    boundaries: list[dict[str, Any]],
    blockers: list[str],
) -> dict[str, Any]:
    boundary_created = not blockers and len(boundaries) == 1
    return {
        "production_analysis_result_creation_execution_boundary_set_schema": EXECUTION_BOUNDARY_SET_SCHEMA,
        "phase": PHASE,
        "production_analysis_result_creation_execution_boundary_set_status": status,
        "input_source_kind": "controlled_production_analysis_result_creation_runtime_boundary",
        "source_production_analysis_result_creation_runtime_boundary_set_schema": _safe_source_value(
            source_runtime_boundary_set,
            "production_analysis_result_creation_runtime_boundary_set_schema",
        )
        or SOURCE_RUNTIME_BOUNDARY_SET_SCHEMA,
        "source_production_analysis_result_creation_runtime_boundary_schema": (
            _source_runtime_boundary_schema(source_runtime_boundary_set)
        ),
        "source_production_analysis_result_creation_runtime_boundary_count": (
            _source_creation_runtime_boundary_count(source_runtime_boundary_set)
        ),
        "source_production_analysis_result_creation_candidate_count": _source_creation_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_creation_boundary_count": _source_creation_boundary_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": (
            _source_creation_or_runtime_candidate_count(source_runtime_boundary_set)
        ),
        "source_production_analysis_result_runtime_boundary_count": _source_runtime_boundary_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_boundary_count": _source_boundary_count(source_runtime_boundary_set),
        "source_production_analysis_result_candidate_count": _source_production_candidate_count(
            source_runtime_boundary_set
        ),
        "source_analysis_result_candidate_count": _source_analysis_result_candidate_count(
            source_runtime_boundary_set
        ),
        "source_actual_analysis_execution_candidate_count": _source_actual_analysis_execution_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_run_candidate_count": _source_production_analysis_run_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_case_candidate_count": _source_production_case_candidate_count(
            source_runtime_boundary_set
        ),
        "source_controlled_evidence_item_count": _source_controlled_evidence_item_count(
            source_runtime_boundary_set
        ),
        "creation_execution_boundary_mode": (
            "backend_only_local_production_analysis_result_creation_execution_boundary"
        ),
        "production_analysis_result_creation_execution_boundary_count": len(boundaries),
        "warning_count": _source_warning_count(source_runtime_boundary_set),
        "human_review_required": _truthy(
            source_runtime_boundary_set.get("human_review_required")
            if isinstance(source_runtime_boundary_set, dict)
            else None
        ),
        "no_automatic_trust_upgrade": _truthy(
            source_runtime_boundary_set.get("no_automatic_trust_upgrade")
            if isinstance(source_runtime_boundary_set, dict)
            else None
        ),
        "production_analysis_result_creation_runtime_boundary_created_upstream": _truthy(
            source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_created")
            if isinstance(source_runtime_boundary_set, dict)
            else None
        ),
        "production_analysis_result_creation_execution_boundary_created": boundary_created,
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
        "analysis_ready": False,
        "report_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "production_analysis_result_creation_execution_boundaries": boundaries,
        "boundary_flags": _boundary_flags(creation_execution_boundary_only=boundary_created),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _boundary_warnings(source_runtime_boundary_set),
        "blockers": _dedupe(blockers),
        "audit_summary": {
            "analysis_effect": "none",
            "production_analysis_result_effect": "none",
            "production_analysis_result_creation_execution_effect": "none",
            "production_analysis_result_runtime_effect": "none",
            "production_analysis_run_effect": "none",
            "production_case_effect": "none",
            "production_evidence_item_effect": "none",
            "review_queue_effect": "none",
            "route_api_frontend_effect": "none",
            "report_public_delivery_effect": "none",
            "human_review_required": True,
        },
        "generated_at": _utc_now(),
    }


def _creation_execution_boundary_from_source(
    source_runtime_boundary: dict[str, Any],
    source_runtime_boundary_set: dict[str, Any] | None,
) -> dict[str, Any]:
    source_ids = _source_runtime_boundary_ids(source_runtime_boundary)
    return {
        "production_analysis_result_creation_execution_boundary_schema": EXECUTION_BOUNDARY_SCHEMA,
        "production_analysis_result_creation_execution_boundary_id": _execution_boundary_id(source_ids),
        "source_production_analysis_result_creation_runtime_boundary_ids": source_ids,
        "source_production_analysis_result_creation_runtime_boundary_count": (
            _source_creation_runtime_boundary_count(source_runtime_boundary_set)
        ),
        "source_production_analysis_result_creation_candidate_count": _source_creation_candidate_count(
            source_runtime_boundary
        ),
        "source_production_analysis_result_creation_boundary_count": _source_creation_boundary_count(
            source_runtime_boundary
        ),
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": (
            _source_creation_or_runtime_candidate_count(source_runtime_boundary)
        ),
        "source_production_analysis_result_runtime_boundary_count": _source_runtime_boundary_count(
            source_runtime_boundary
        ),
        "source_production_analysis_result_boundary_count": _source_boundary_count(source_runtime_boundary),
        "source_production_analysis_result_candidate_count": _source_production_candidate_count(
            source_runtime_boundary
        ),
        "source_analysis_result_candidate_count": _source_analysis_result_candidate_count(
            source_runtime_boundary
        ),
        "source_actual_analysis_execution_candidate_count": _source_actual_analysis_execution_candidate_count(
            source_runtime_boundary
        ),
        "source_production_analysis_run_candidate_count": _source_production_analysis_run_candidate_count(
            source_runtime_boundary
        ),
        "source_production_case_candidate_count": _source_production_case_candidate_count(
            source_runtime_boundary
        ),
        "source_controlled_evidence_item_count": _source_controlled_evidence_item_count(
            source_runtime_boundary
        ),
        "case_id_hint": _safe_label(source_runtime_boundary.get("case_id_hint")),
        "case_title_or_label_redacted": _safe_label(
            source_runtime_boundary.get("case_title_or_label_redacted")
        ),
        "input_scope_summary_redacted": _safe_label(
            source_runtime_boundary.get("input_scope_summary_redacted")
        ),
        "intended_creation_execution_boundary_labels": [
            "creation_execution_boundary_only",
            "selected_sample_only",
            "human_review_required",
            "no_automatic_trust_upgrade",
        ],
        "intended_module_scope_labels": [
            "production_analysis_result_creation_execution_boundary",
            "no_production_analysis_result",
            "no_production_analysis_result_creation_execution",
            "no_production_analysis_result_runtime_use",
            "no_analysis_result_generation",
            "no_actual_analysis_execution",
        ],
        "creation_execution_gate_labels": [
            "creation_execution_boundary_gate_only",
            "manual_review_required",
            "not_production_analysis_result_creation_execution",
            "not_runtime_execution",
        ],
        "warning_count": source_runtime_boundary.get("warning_count", 0),
        "human_review_required": True,
        "review_status": "human_review_required",
        "trust_boundary_label": "no_automatic_trust_upgrade",
        "verification_status_summary": "needs_review",
        "redaction_status": "redacted",
        "redaction_warnings": _safe_list(source_runtime_boundary.get("redaction_warnings")),
        "warning_labels": _safe_list(source_runtime_boundary.get("warning_labels")),
        "blocker_codes": [],
        "production_analysis_result_creation_readiness_blockers": [
            "production_analysis_result_creation_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_creation_execution_readiness_blockers": [
            "production_analysis_result_creation_execution_not_approved",
            "human_review_required",
        ],
        "production_analysis_result_runtime_readiness_blockers": [
            "production_analysis_result_runtime_not_approved",
            "human_review_required",
        ],
        "analysis_result_generation_readiness_blockers": [
            "analysis_result_generation_not_approved",
            "human_review_required",
        ],
        "actual_analysis_execution_readiness_blockers": [
            "actual_analysis_execution_not_approved",
            "human_review_required",
        ],
        "production_runtime_blockers": [
            "production_analysis_result_runtime_not_approved",
            "human_review_required",
        ],
        "report_readiness_blockers": [
            "analysis_result_not_created",
            "report_generation_not_approved",
            "human_review_required",
        ],
        "production_record_creation_blockers": [
            "production_analysis_run_creation_not_approved",
            "production_case_creation_not_approved",
            "production_evidence_item_creation_not_approved",
        ],
        "creation_execution_boundary_only": True,
        "no_automatic_trust_upgrade": True,
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
        "report_ready": False,
        "boundary_flags": _boundary_flags(creation_execution_boundary_only=True),
    }


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if not exact_approval_phrase:
        return ["blocked_missing_exact_approval"]
    if not isinstance(exact_approval_phrase, str):
        return ["blocked_wrong_exact_approval"]
    if not exact_approval_phrase.isascii():
        return ["blocked_non_ascii_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_approval"]
    return []


def _requested_action_blockers(requested_actions: list[str] | dict[str, Any] | None) -> list[str]:
    if requested_actions is None:
        return []
    if isinstance(requested_actions, dict):
        actions = [str(key) for key, value in requested_actions.items() if value]
    elif isinstance(requested_actions, list):
        actions = [str(action) for action in requested_actions]
    else:
        return ["blocked_source_boundary_violation"]
    blockers: list[str] = []
    for action in actions:
        if action in REQUESTED_ACTIONS_BLOCKED:
            blockers.append(_requested_action_status(action))
    return _dedupe(blockers)


def _source_runtime_boundary_set_blockers(
    source_runtime_boundary_set: dict[str, Any] | None,
    source_boundaries: list[dict[str, Any]],
    *,
    decision_8w60: str | None,
    selected_next_boundary_option_8w60: str | None,
) -> list[str]:
    if not isinstance(source_runtime_boundary_set, dict):
        return ["source_creation_runtime_boundary_set_missing"]
    blockers: list[str] = []
    for field, value in source_runtime_boundary_set.items():
        if field == "runtime_side_effects":
            continue
        if field in FORBIDDEN_SOURCE_FIELDS and _forbidden_field_has_payload(value):
            blockers.append(f"forbidden_source_runtime_boundary_set_field:{field}")
        elif _contains_forbidden_value(value):
            blockers.append(f"source_runtime_boundary_set_forbidden_value:{field}")
    if (
        source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_set_schema")
        != SOURCE_RUNTIME_BOUNDARY_SET_SCHEMA
    ):
        blockers.append("source_creation_runtime_boundary_set_schema_wrong")
    if (
        source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_set_status")
        != SOURCE_WARN_STATUS
    ):
        blockers.append("source_creation_runtime_boundary_set_status_wrong")
    if _source_runtime_boundary_schema(source_runtime_boundary_set) != SOURCE_RUNTIME_BOUNDARY_SCHEMA:
        blockers.append("source_creation_runtime_boundary_schema_wrong")
    if (
        _source_creation_runtime_boundary_count(source_runtime_boundary_set)
        != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_RUNTIME_BOUNDARY_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_count_not_one")
    if (
        _safe_int(source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_count"))
        not in (0, EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_RUNTIME_BOUNDARY_COUNT)
    ):
        blockers.append("source_creation_runtime_boundary_count_not_one")
    if (
        _source_creation_candidate_count(source_runtime_boundary_set)
        != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_source_candidate_count_not_one")
    if (
        _source_creation_boundary_count(source_runtime_boundary_set)
        != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_BOUNDARY_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_source_boundary_count_not_one")
    if _source_creation_or_runtime_candidate_count(source_runtime_boundary_set) != (
        EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_OR_RUNTIME_EXECUTION_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_creation_or_runtime_candidate_count_not_one")
    if (
        _source_runtime_boundary_count(source_runtime_boundary_set)
        != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_RUNTIME_BOUNDARY_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_runtime_boundary_count_not_one")
    if _source_boundary_count(source_runtime_boundary_set) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_BOUNDARY_COUNT:
        blockers.append("source_creation_runtime_boundary_production_analysis_result_boundary_count_not_one")
    if (
        _source_production_candidate_count(source_runtime_boundary_set)
        != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_production_analysis_result_candidate_count_not_one")
    if _source_analysis_result_candidate_count(source_runtime_boundary_set) != EXPECTED_SOURCE_ANALYSIS_RESULT_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_analysis_result_candidate_count_not_one")
    if _source_actual_analysis_execution_candidate_count(source_runtime_boundary_set) != (
        EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_actual_analysis_execution_candidate_count_not_one")
    if _source_production_analysis_run_candidate_count(source_runtime_boundary_set) != (
        EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_production_analysis_run_candidate_count_not_one")
    if _source_production_case_candidate_count(source_runtime_boundary_set) != (
        EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_production_case_candidate_count_not_one")
    if _source_controlled_evidence_item_count(source_runtime_boundary_set) != EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT:
        blockers.append("source_creation_runtime_boundary_controlled_evidence_item_count_not_five")
    if source_runtime_boundary_set.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")
    if decision_8w60 != EXPECTED_8W60_DECISION:
        blockers.append("source_8w60_decision_not_ready")
    if selected_next_boundary_option_8w60 != EXPECTED_8W60_NEXT_BOUNDARY_OPTION:
        blockers.append("source_8w60_next_boundary_option_wrong")
    for field, reason in SOURCE_TRUE_FIELDS.items():
        if source_runtime_boundary_set.get(field) is not True:
            blockers.append(reason)
    if not _source_creation_candidate_created(source_runtime_boundary_set):
        blockers.append("source_production_analysis_result_creation_candidate_created_not_true")
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if field in source_runtime_boundary_set and source_runtime_boundary_set.get(field) is not False:
            blockers.append(reason)
    runtime_side_effects = source_runtime_boundary_set.get("runtime_side_effects", {})
    if isinstance(runtime_side_effects, dict):
        for flag in RUNTIME_SIDE_EFFECT_FLAGS:
            if runtime_side_effects.get(flag) is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")
    else:
        blockers.append("source_runtime_side_effects_not_object")
    if "production_analysis_result_creation_runtime_boundaries" in source_runtime_boundary_set and len(source_boundaries) != 1:
        blockers.append("source_production_analysis_result_creation_runtime_boundary_missing")
    return _dedupe(blockers)


def _source_runtime_boundary_blockers(
    source_runtime_boundary_set: dict[str, Any] | None,
    source_boundaries: list[dict[str, Any]],
) -> list[str]:
    if len(source_boundaries) != 1:
        return ["source_production_analysis_result_creation_runtime_boundary_missing"]
    blockers: list[str] = []
    boundary = source_boundaries[0]
    if not isinstance(boundary, dict):
        return ["source_production_analysis_result_creation_runtime_boundary_not_object"]
    for field, value in boundary.items():
        if field in FORBIDDEN_SOURCE_FIELDS and _forbidden_field_has_payload(value):
            blockers.append(f"forbidden_source_creation_runtime_boundary_field:{field}")
        elif _contains_forbidden_value(value):
            blockers.append(f"source_creation_runtime_boundary_forbidden_value:{field}")
    if boundary.get("production_analysis_result_creation_runtime_boundary_schema") != SOURCE_RUNTIME_BOUNDARY_SCHEMA:
        blockers.append("source_creation_runtime_boundary_schema_wrong")
    if _source_creation_candidate_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_source_candidate_count_not_one")
    if _source_creation_boundary_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_BOUNDARY_COUNT:
        blockers.append("source_creation_runtime_boundary_source_boundary_count_not_one")
    if _source_creation_or_runtime_candidate_count(boundary) != (
        EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CREATION_OR_RUNTIME_EXECUTION_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_creation_or_runtime_candidate_count_not_one")
    if _source_runtime_boundary_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_RUNTIME_BOUNDARY_COUNT:
        blockers.append("source_creation_runtime_boundary_runtime_boundary_count_not_one")
    if _source_boundary_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_BOUNDARY_COUNT:
        blockers.append("source_creation_runtime_boundary_production_analysis_result_boundary_count_not_one")
    if _source_production_candidate_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RESULT_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_production_analysis_result_candidate_count_not_one")
    if _source_analysis_result_candidate_count(boundary) != EXPECTED_SOURCE_ANALYSIS_RESULT_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_analysis_result_candidate_count_not_one")
    if _source_actual_analysis_execution_candidate_count(boundary) != (
        EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT
    ):
        blockers.append("source_creation_runtime_boundary_actual_analysis_execution_candidate_count_not_one")
    if _source_production_analysis_run_candidate_count(boundary) != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_production_analysis_run_candidate_count_not_one")
    if _source_production_case_candidate_count(boundary) != EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT:
        blockers.append("source_creation_runtime_boundary_production_case_candidate_count_not_one")
    if _source_controlled_evidence_item_count(boundary) != EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT:
        blockers.append("source_creation_runtime_boundary_controlled_evidence_item_count_not_five")
    if boundary.get("warning_count") != 1:
        blockers.append("source_creation_runtime_boundary_warning_count_not_one")
    if boundary.get("human_review_required") is not True:
        blockers.append("source_creation_runtime_boundary_human_review_required_not_true")
    if boundary.get("no_automatic_trust_upgrade") is not True:
        blockers.append("source_creation_runtime_boundary_no_automatic_trust_upgrade_not_true")
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if field in boundary and boundary.get(field) is not False:
            blockers.append(f"source_creation_runtime_boundary_{reason.removeprefix('source_')}")
    return _dedupe(blockers)


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return WARN_STATUS
    first = blockers[0]
    if first.startswith("blocked_"):
        return first
    if first == "creation_execution_boundary_count_not_one":
        return "blocked_creation_execution_boundary_limit_violation"
    if first.startswith("forbidden_") or "_forbidden_value:" in first:
        return "blocked_forbidden_field_detected"
    if first == "source_warning_count_not_one" or "warning_count" in first:
        return "blocked_warning_state_missing"
    if "human_review_required" in first:
        return "blocked_manual_review_state_missing"
    if "schema" in first or "status" in first or "count" in first or "missing" in first or "8w60" in first:
        return "blocked_invalid_source_production_analysis_result_creation_runtime_boundary"
    return "blocked_source_boundary_violation"


def _requested_action_status(action: str) -> str:
    if "production_analysis_result_creation_execution" in action:
        return "blocked_unapproved_production_analysis_result_creation_execution_request"
    if "production_analysis_result_runtime" in action:
        return "blocked_unapproved_production_analysis_result_runtime_request"
    if "production_analysis_result_creation" in action:
        return "blocked_unapproved_production_analysis_result_creation_request"
    if "production_analysis_result" in action:
        return "blocked_unapproved_production_analysis_result_creation_request"
    if "analysis_result_generation" in action:
        return "blocked_unapproved_analysis_result_generation_request"
    if "actual_analysis_execution" in action or action == "analysis_execution":
        return "blocked_unapproved_actual_analysis_execution_request"
    if "production_analysis_run" in action:
        return "blocked_unapproved_production_analysis_run_creation_request"
    if "production_case" in action:
        return "blocked_unapproved_production_case_creation_request"
    if "production_evidence_item" in action:
        return "blocked_unapproved_production_evidence_item_request"
    if "review_queue" in action:
        return "blocked_unapproved_review_queue_request"
    if "route" in action or "frontend" in action:
        return "blocked_unapproved_route_api_frontend_request"
    if "report" in action or "sandbox" in action or "public_event" in action or "download" in action or "delivery" in action:
        return "blocked_unapproved_report_or_public_output_request"
    if "row_parsing" in action:
        return "blocked_unapproved_row_parsing_request"
    if "collector" in action or "real_exchange" in action:
        return "blocked_unapproved_collector_or_real_exchange_request"
    return "blocked_source_boundary_violation"


def _safe_source_runtime_boundaries(source_runtime_boundary_set: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_runtime_boundary_set, dict):
        return []
    if "production_analysis_result_creation_runtime_boundaries" not in source_runtime_boundary_set:
        return [_summary_runtime_boundary_from_source_set(source_runtime_boundary_set)]
    boundaries = source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundaries")
    if not isinstance(boundaries, list):
        return []
    return [boundary for boundary in boundaries if isinstance(boundary, dict)]


def _summary_runtime_boundary_from_source_set(source_runtime_boundary_set: dict[str, Any]) -> dict[str, Any]:
    return {
        "production_analysis_result_creation_runtime_boundary_schema": SOURCE_RUNTIME_BOUNDARY_SCHEMA,
        "production_analysis_result_creation_runtime_boundary_id": _safe_label(
            source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_id")
        ),
        "source_production_analysis_result_creation_candidate_count": _source_creation_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_creation_boundary_count": _source_creation_boundary_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_creation_or_runtime_execution_candidate_count": (
            _source_creation_or_runtime_candidate_count(source_runtime_boundary_set)
        ),
        "source_production_analysis_result_runtime_boundary_count": _source_runtime_boundary_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_result_boundary_count": _source_boundary_count(source_runtime_boundary_set),
        "source_production_analysis_result_candidate_count": _source_production_candidate_count(
            source_runtime_boundary_set
        ),
        "source_analysis_result_candidate_count": _source_analysis_result_candidate_count(
            source_runtime_boundary_set
        ),
        "source_actual_analysis_execution_candidate_count": _source_actual_analysis_execution_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_analysis_run_candidate_count": _source_production_analysis_run_candidate_count(
            source_runtime_boundary_set
        ),
        "source_production_case_candidate_count": _source_production_case_candidate_count(
            source_runtime_boundary_set
        ),
        "source_controlled_evidence_item_count": _source_controlled_evidence_item_count(
            source_runtime_boundary_set
        ),
        "case_id_hint": _safe_label(source_runtime_boundary_set.get("case_id_hint")),
        "case_title_or_label_redacted": _safe_label(
            source_runtime_boundary_set.get("case_title_or_label_redacted")
        ),
        "input_scope_summary_redacted": _safe_label(
            source_runtime_boundary_set.get("input_scope_summary_redacted")
        ),
        "warning_count": _source_warning_count(source_runtime_boundary_set),
        "human_review_required": source_runtime_boundary_set.get("human_review_required"),
        "review_status": "human_review_required",
        "trust_boundary_label": "no_automatic_trust_upgrade",
        "verification_status_summary": "needs_review",
        "redaction_status": "redacted",
        "redaction_warnings": _safe_list(source_runtime_boundary_set.get("warnings")),
        "warning_labels": _safe_list(source_runtime_boundary_set.get("warnings")),
        "no_automatic_trust_upgrade": source_runtime_boundary_set.get("no_automatic_trust_upgrade"),
        "production_analysis_result_created": source_runtime_boundary_set.get("production_analysis_result_created"),
        "production_analysis_result_creation_executed": source_runtime_boundary_set.get(
            "production_analysis_result_creation_executed"
        ),
        "production_analysis_result_runtime_used": source_runtime_boundary_set.get(
            "production_analysis_result_runtime_used"
        ),
        "analysis_result_generation_executed": source_runtime_boundary_set.get(
            "analysis_result_generation_executed"
        ),
        "analysis_result_created": source_runtime_boundary_set.get("analysis_result_created"),
        "actual_analysis_execution_started": source_runtime_boundary_set.get(
            "actual_analysis_execution_started"
        ),
        "analysis_execution_started": source_runtime_boundary_set.get("analysis_execution_started"),
        "production_analysis_run_created": source_runtime_boundary_set.get("production_analysis_run_created"),
        "production_case_created": source_runtime_boundary_set.get("production_case_created"),
        "production_evidence_item_created": source_runtime_boundary_set.get("production_evidence_item_created"),
        "review_queue_item_created": source_runtime_boundary_set.get("review_queue_item_created"),
        "production_review_queue_item_created": source_runtime_boundary_set.get(
            "production_review_queue_item_created"
        ),
        "review_queue_runtime_used": source_runtime_boundary_set.get("review_queue_runtime_used"),
        "report_ready": source_runtime_boundary_set.get("report_ready"),
        "boundary_flags": source_runtime_boundary_set.get("boundary_flags", {}),
    }


def _source_runtime_boundary_schema(source_runtime_boundary_set: dict[str, Any] | None) -> str | None:
    if not isinstance(source_runtime_boundary_set, dict):
        return None
    value = source_runtime_boundary_set.get("source_production_analysis_result_creation_runtime_boundary_schema")
    if isinstance(value, str):
        return value
    boundaries = _safe_source_runtime_boundaries(source_runtime_boundary_set)
    if boundaries:
        boundary_schema = boundaries[0].get("production_analysis_result_creation_runtime_boundary_schema")
        if isinstance(boundary_schema, str):
            return boundary_schema
    return SOURCE_RUNTIME_BOUNDARY_SCHEMA


def _source_creation_runtime_boundary_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    explicit_count = _safe_int(
        source_runtime_boundary_set.get("source_production_analysis_result_creation_runtime_boundary_count"),
        source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundary_count"),
    )
    if explicit_count:
        return explicit_count
    boundaries = source_runtime_boundary_set.get("production_analysis_result_creation_runtime_boundaries")
    if isinstance(boundaries, list):
        return len([boundary for boundary in boundaries if isinstance(boundary, dict)])
    return 0


def _source_creation_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_result_creation_candidate_count"))


def _source_creation_boundary_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_result_creation_boundary_count"))


def _source_creation_or_runtime_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(
        source_runtime_boundary_set.get(
            "source_production_analysis_result_creation_or_runtime_execution_candidate_count"
        )
    )


def _source_runtime_boundary_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_result_runtime_boundary_count"))


def _source_boundary_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_result_boundary_count"))


def _source_production_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_result_candidate_count"))


def _source_analysis_result_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_analysis_result_candidate_count"))


def _source_actual_analysis_execution_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_actual_analysis_execution_candidate_count"))


def _source_production_analysis_run_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_analysis_run_candidate_count"))


def _source_production_case_candidate_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_production_case_candidate_count"))


def _source_controlled_evidence_item_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("source_controlled_evidence_item_count"))


def _source_warning_count(source_runtime_boundary_set: dict[str, Any] | None) -> int:
    if not isinstance(source_runtime_boundary_set, dict):
        return 0
    return _safe_int(source_runtime_boundary_set.get("warning_count"))


def _source_creation_candidate_created(source_runtime_boundary_set: dict[str, Any]) -> bool:
    if (
        "production_analysis_result_creation_candidate_created" in source_runtime_boundary_set
        and source_runtime_boundary_set.get("production_analysis_result_creation_candidate_created") is not True
    ):
        return False
    return (
        source_runtime_boundary_set.get("production_analysis_result_creation_candidate_created") is True
        or source_runtime_boundary_set.get("production_analysis_result_creation_candidate_created_upstream") is True
    )


def _source_runtime_boundary_ids(source_runtime_boundary: dict[str, Any]) -> list[str]:
    ids = source_runtime_boundary.get("source_production_analysis_result_creation_runtime_boundary_ids")
    if isinstance(ids, list):
        safe = [_safe_label(item) for item in ids]
        return [item for item in safe if item]
    single = _safe_label(source_runtime_boundary.get("production_analysis_result_creation_runtime_boundary_id"))
    return [single] if single else []


def _execution_boundary_id(source_ids: list[str]) -> str:
    suffix = "-".join(source_ids) if source_ids else "safe-summary"
    return f"controlled-production-analysis-result-creation-execution-boundary-{_slug(suffix)}"


def _runtime_side_effects() -> dict[str, bool]:
    return {flag: False for flag in RUNTIME_SIDE_EFFECT_FLAGS}


def _boundary_flags(*, creation_execution_boundary_only: bool = False) -> dict[str, bool]:
    return {
        "backend_only": True,
        "local_only": True,
        "creation_execution_boundary_only": creation_execution_boundary_only,
        "controlled_production_analysis_result_creation_runtime_boundary_derived_only": True,
        "human_review_required": True,
        "warning_preserving": True,
        "no_automatic_trust_upgrade": True,
        "not_production_analysis_result": True,
        "not_production_analysis_result_creation": True,
        "not_production_analysis_result_creation_execution": True,
        "not_production_analysis_result_runtime_use": True,
        "not_analysis_result_generation": True,
        "not_analysis_result": True,
        "not_actual_analysis_execution": True,
        "not_production_analysis_run": True,
        "not_production_case": True,
        "not_production_evidence_item": True,
        "not_review_queue_item": True,
        "not_production_review_queue_item": True,
        "not_analysis_ready": True,
        "not_report_ready": True,
        "not_frontend_ready": True,
        "not_route_ready": True,
        "not_public_ready": True,
        "not_customer_ready": True,
        "not_official_verification": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_causal_proof": True,
        "no_generated_response_text": True,
    }


def _boundary_warnings(source_runtime_boundary_set: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_runtime_boundary_set, dict):
        warnings.extend(_safe_list(source_runtime_boundary_set.get("warnings")))
    return _dedupe(warnings)


def _contains_forbidden_value(value: Any) -> bool:
    if isinstance(value, dict):
        return any(
            (key in FORBIDDEN_SOURCE_FIELDS and _forbidden_field_has_payload(item))
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
        "private-collector",
        "raw-author",
        "raw-comment",
        "actual-token",
        "actual-cookie",
        "actual-api-key",
        "actual-secret",
        "actual-salt",
        "profile-url",
        "sentiment-should-never",
        "risk-should-never",
        "forecast-should-never",
        "narrative-should-never",
        "recommendation-should-never",
        "strategy-should-never",
        "public-conclusion",
        "customer-conclusion",
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


def _truthy(value: Any) -> bool:
    return value is True


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
