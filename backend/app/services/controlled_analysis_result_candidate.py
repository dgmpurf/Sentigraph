from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


CANDIDATE_SET_SCHEMA = "sentigraph_controlled_analysis_result_candidate_set_v0_1"
CANDIDATE_SCHEMA = "sentigraph_controlled_analysis_result_candidate_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_analysis_result_candidate_summary_v0_1"
SOURCE_CANDIDATE_SET_SCHEMA = "sentigraph_controlled_actual_analysis_execution_candidate_set_v0_1"
SOURCE_CANDIDATE_SCHEMA = "sentigraph_controlled_actual_analysis_execution_candidate_v0_1"
PHASE = "8W-40"
APPROVAL_PHRASE = "APPROVE_8W_40_CONTROLLED_ANALYSIS_RESULT_CANDIDATE_HELPER_IMPLEMENTATION"
SOURCE_WARN_STATUS = "actual_analysis_execution_candidate_set_warn_manual_review_required"
WARN_STATUS = "analysis_result_candidate_set_warn_manual_review_required"
EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT = 1
EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT = 5

FORBIDDEN_SOURCE_FIELDS = {
    "analysis_result_id",
    "production_analysis_result_id",
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
    "analysis_result_generation",
    "production_analysis_result",
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
    "actual_analysis_execution_candidate_created": "source_actual_analysis_execution_candidate_created_not_true",
}

SOURCE_FALSE_FIELDS = {
    "actual_analysis_execution_started": "source_actual_analysis_execution_started_true",
    "analysis_execution_started": "source_analysis_execution_started_true",
    "analysis_result_created": "source_analysis_result_created_true",
    "production_analysis_result_created": "source_production_analysis_result_created_true",
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


def build_controlled_analysis_result_candidate_set(
    controlled_actual_analysis_execution_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one local analysis-result-candidate-shaped boundary object from an 8W-37 candidate set."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))

    source_candidates = _safe_source_candidates(controlled_actual_analysis_execution_candidate_set)
    source_actual_candidate_count = _source_actual_analysis_execution_candidate_count(
        controlled_actual_analysis_execution_candidate_set,
        source_candidates,
    )
    source_analysis_run_candidate_count = _source_production_analysis_run_candidate_count(
        controlled_actual_analysis_execution_candidate_set,
        source_candidates,
    )
    source_case_candidate_count = _source_production_case_candidate_count(
        controlled_actual_analysis_execution_candidate_set,
        source_candidates,
    )
    source_controlled_evidence_item_count = _source_controlled_evidence_item_count(
        controlled_actual_analysis_execution_candidate_set,
        source_candidates,
    )

    blockers.extend(
        _source_candidate_set_blockers(
            controlled_actual_analysis_execution_candidate_set,
            source_candidates,
            source_actual_candidate_count,
            source_analysis_run_candidate_count,
            source_case_candidate_count,
            source_controlled_evidence_item_count,
        )
    )

    candidate: dict[str, Any] | None = None
    if not blockers:
        blockers.extend(_source_candidate_blockers(source_candidates))
        if not blockers:
            candidate = _candidate_from_source(
                controlled_actual_analysis_execution_candidate_set,
                source_candidates,
                source_actual_candidate_count,
                source_analysis_run_candidate_count,
                source_case_candidate_count,
                source_controlled_evidence_item_count,
            )

    if blockers:
        return _base_output(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            warnings=[],
            candidate=None,
            source_candidate_set=controlled_actual_analysis_execution_candidate_set,
            source_actual_candidate_count=source_actual_candidate_count,
            source_analysis_run_candidate_count=source_analysis_run_candidate_count,
            source_case_candidate_count=source_case_candidate_count,
            source_controlled_evidence_item_count=source_controlled_evidence_item_count,
        )

    return _base_output(
        status=WARN_STATUS,
        created=True,
        blockers=[],
        warnings=_candidate_warnings(controlled_actual_analysis_execution_candidate_set),
        candidate=candidate,
        source_candidate_set=controlled_actual_analysis_execution_candidate_set,
        source_actual_candidate_count=source_actual_candidate_count,
        source_analysis_run_candidate_count=source_analysis_run_candidate_count,
        source_case_candidate_count=source_case_candidate_count,
        source_controlled_evidence_item_count=source_controlled_evidence_item_count,
    )


create_controlled_analysis_result_candidate_set = build_controlled_analysis_result_candidate_set


def build_safe_controlled_analysis_result_candidate_summary(
    controlled_actual_analysis_execution_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate_set = build_controlled_analysis_result_candidate_set(
        controlled_actual_analysis_execution_candidate_set,
        exact_approval_phrase=exact_approval_phrase,
        requested_actions=requested_actions,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "analysis_result_candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "analysis_result_candidate_set_status": candidate_set["analysis_result_candidate_set_status"],
        "source_actual_analysis_execution_candidate_set_schema": candidate_set[
            "source_actual_analysis_execution_candidate_set_schema"
        ],
        "source_actual_analysis_execution_candidate_schema": candidate_set[
            "source_actual_analysis_execution_candidate_schema"
        ],
        "source_actual_analysis_execution_candidate_count": candidate_set[
            "source_actual_analysis_execution_candidate_count"
        ],
        "source_production_analysis_run_candidate_count": candidate_set[
            "source_production_analysis_run_candidate_count"
        ],
        "source_production_case_candidate_count": candidate_set["source_production_case_candidate_count"],
        "source_controlled_evidence_item_count": candidate_set["source_controlled_evidence_item_count"],
        "analysis_result_candidate_count": candidate_set["analysis_result_candidate_count"],
        "analysis_result_candidate_created": candidate_set["analysis_result_candidate_created"],
        "warning_count": candidate_set["warning_count"],
        "human_review_required": candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": candidate_set["no_automatic_trust_upgrade"],
        "actual_analysis_execution_candidate_created_upstream": candidate_set[
            "actual_analysis_execution_candidate_created_upstream"
        ],
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "production_analysis_result_created": False,
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
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "blockers": list(candidate_set["blockers"]),
        "warnings": list(candidate_set["warnings"]),
        "audit_summary": dict(candidate_set["audit_summary"]),
    }


def _base_output(
    *,
    status: str,
    created: bool,
    blockers: list[str],
    warnings: list[str],
    candidate: dict[str, Any] | None,
    source_candidate_set: dict[str, Any] | None,
    source_actual_candidate_count: int,
    source_analysis_run_candidate_count: int,
    source_case_candidate_count: int,
    source_controlled_evidence_item_count: int,
) -> dict[str, Any]:
    candidates = [candidate] if candidate else []
    return {
        "analysis_result_candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "phase": PHASE,
        "analysis_result_candidate_set_status": status,
        "created_at": _utc_now(),
        "input_source_kind": "controlled_actual_analysis_execution_candidate",
        "source_actual_analysis_execution_candidate_set_schema": _safe_source_value(
            source_candidate_set,
            "actual_analysis_execution_candidate_set_schema",
        ),
        "source_actual_analysis_execution_candidate_schema": _source_actual_analysis_execution_candidate_schema(
            source_candidate_set
        ),
        "source_actual_analysis_execution_candidate_count": source_actual_candidate_count,
        "source_production_analysis_run_candidate_count": source_analysis_run_candidate_count,
        "source_production_case_candidate_count": source_case_candidate_count,
        "source_controlled_evidence_item_count": source_controlled_evidence_item_count,
        "analysis_result_candidate_mode": "backend_only_local_analysis_result_candidate_boundary",
        "analysis_result_candidate_count": len(candidates),
        "warning_count": _source_warning_count(source_candidate_set),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "actual_analysis_execution_candidate_created_upstream": _truthy(
            source_candidate_set.get("actual_analysis_execution_candidate_created")
            if isinstance(source_candidate_set, dict)
            else False
        ),
        "analysis_result_candidate_created": created,
        "analysis_result_candidate_only": True,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "production_analysis_result_created": False,
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
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "analysis_result_candidate_only": True,
            "controlled_actual_analysis_execution_candidate_derived_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_analysis_result_generation": True,
            "not_analysis_result": True,
            "not_production_analysis_result": True,
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
        },
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _dedupe(warnings),
        "blockers": _dedupe(blockers),
        "audit_summary": {
            "audit_schema": "sentigraph_controlled_analysis_result_candidate_audit_summary_v0_1",
            "phase": PHASE,
            "analysis_effect": "none",
            "analysis_result_effect": "none",
            "production_analysis_result_effect": "none",
            "actual_analysis_execution_effect": "none",
            "production_side_effect": "none",
            "human_review_required": True,
            "warning_count": _source_warning_count(source_candidate_set),
            "analysis_result_candidate_count": len(candidates),
            "review_queue_effect": "none",
            "route_api_frontend_effect": "none",
            "report_effect": "none",
            "delivery_effect": "none",
        },
        "analysis_result_candidates": candidates,
    }


def _candidate_from_source(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
    source_actual_candidate_count: int,
    source_analysis_run_candidate_count: int,
    source_case_candidate_count: int,
    source_controlled_evidence_item_count: int,
) -> dict[str, Any]:
    source_ids = [_safe_token(candidate.get("actual_analysis_execution_candidate_id")) for candidate in source_candidates]
    first_source = source_candidates[0] if source_candidates else {}
    warning_labels = _merged_warning_labels(source_candidate_set, source_candidates)
    return {
        "analysis_result_candidate_schema": CANDIDATE_SCHEMA,
        "analysis_result_candidate_id": _analysis_result_candidate_id(source_ids),
        "source_actual_analysis_execution_candidate_id": source_ids[0] if source_ids else "unknown",
        "source_actual_analysis_execution_candidate_ids": source_ids,
        "source_actual_analysis_execution_candidate_count": source_actual_candidate_count,
        "source_production_analysis_run_candidate_count": source_analysis_run_candidate_count,
        "source_production_case_candidate_count": source_case_candidate_count,
        "source_controlled_evidence_item_count": source_controlled_evidence_item_count,
        "case_id_hint": _safe_label(first_source.get("case_id_hint")),
        "case_title_or_label_redacted": _safe_label(first_source.get("case_title_or_label_redacted"))
        or "redacted_case_label",
        "input_scope_summary_redacted": "controlled_local_actual_analysis_execution_candidate_summary_only",
        "intended_result_scope_labels": [
            "analysis_result_candidate_only",
            "selected_sample_only",
            "human_review_required",
            "no_automatic_trust_upgrade",
        ],
        "intended_module_scope_labels": [
            "analysis_result_candidate_boundary",
            "no_analysis_result_generation",
            "no_actual_analysis_execution",
            "no_report_generation",
        ],
        "warning_count": _source_warning_count(source_candidate_set),
        "human_review_required": True,
        "review_status": "human_review_required",
        "trust_boundary_label": "no_automatic_trust_upgrade",
        "verification_status_summary": _safe_label(first_source.get("verification_status_summary"))
        or "needs_review",
        "redaction_status": _safe_label(first_source.get("redaction_status")) or "redacted",
        "redaction_warnings": warning_labels,
        "warning_labels": warning_labels,
        "blocker_codes": [],
        "analysis_result_generation_readiness_blockers": [
            "analysis_result_generation_not_approved",
            "actual_analysis_execution_not_started",
            "human_review_required",
        ],
        "production_analysis_result_readiness_blockers": [
            "production_analysis_result_not_approved",
            "analysis_result_not_created",
            "human_review_required",
        ],
        "report_readiness_blockers": [
            "analysis_result_not_created",
            "report_generation_not_approved",
            "human_review_required",
        ],
        "analysis_result_candidate_only": True,
        "no_automatic_trust_upgrade": True,
        "analysis_result_generation_executed": False,
        "analysis_result_created": False,
        "production_analysis_result_created": False,
        "actual_analysis_execution_started": False,
        "analysis_execution_started": False,
        "production_analysis_run_created": False,
        "production_case_created": False,
        "production_evidence_item_created": False,
        "report_ready": False,
        "boundary_flags": {
            "analysis_result_candidate_only": True,
            "controlled_actual_analysis_execution_candidate_derived_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_analysis_result_generation": True,
            "not_analysis_result": True,
            "not_production_analysis_result": True,
            "not_actual_analysis_execution": True,
            "not_production_analysis_run": True,
            "not_production_case": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_report_ready": True,
            "not_frontend_ready": True,
            "not_route_ready": True,
            "not_public_ready": True,
            "not_customer_ready": True,
            "no_generated_response_text": True,
        },
    }


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        return ["blocked_missing_exact_approval"]
    if not exact_approval_phrase.isascii():
        return ["blocked_non_ascii_approval"]
    if "???" in exact_approval_phrase or "\ufffd" in exact_approval_phrase:
        return ["blocked_garbled_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_approval"]
    return []


def _requested_action_blockers(requested_actions: list[str] | dict[str, Any] | None) -> list[str]:
    blockers: list[str] = []
    if isinstance(requested_actions, list):
        for action in requested_actions:
            if isinstance(action, str) and action in REQUESTED_ACTIONS_BLOCKED:
                blockers.append(f"requested_action_blocked:{action}")
    elif isinstance(requested_actions, dict):
        for action, requested in requested_actions.items():
            if isinstance(action, str) and action in REQUESTED_ACTIONS_BLOCKED and _truthy(requested):
                blockers.append(f"requested_action_blocked:{action}")
    return _dedupe(blockers)


def _source_candidate_set_blockers(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
    source_actual_candidate_count: int,
    source_analysis_run_candidate_count: int,
    source_case_candidate_count: int,
    source_controlled_evidence_item_count: int,
) -> list[str]:
    if not isinstance(source_candidate_set, dict):
        return ["source_actual_analysis_execution_candidate_set_missing_or_not_object"]

    blockers: list[str] = []
    expected = {
        "actual_analysis_execution_candidate_set_schema": (
            SOURCE_CANDIDATE_SET_SCHEMA,
            "source_actual_analysis_execution_candidate_set_schema_wrong",
        ),
        "actual_analysis_execution_candidate_set_status": (
            SOURCE_WARN_STATUS,
            "source_actual_analysis_execution_candidate_set_status_not_warn_manual_review",
        ),
    }
    for field, (expected_value, reason) in expected.items():
        if source_candidate_set.get(field) != expected_value:
            blockers.append(reason)

    if source_actual_candidate_count != EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT:
        blockers.append("source_actual_analysis_execution_candidate_count_not_one")
    if len(source_candidates) != EXPECTED_SOURCE_ACTUAL_ANALYSIS_EXECUTION_CANDIDATE_COUNT:
        blockers.append("source_actual_analysis_execution_candidates_count_not_one")
    if source_analysis_run_candidate_count != EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT:
        blockers.append("source_production_analysis_run_candidate_count_not_one")
    if source_case_candidate_count != EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT:
        blockers.append("source_production_case_candidate_count_not_one")
    if source_controlled_evidence_item_count != EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT:
        blockers.append("source_controlled_evidence_item_count_not_five")

    if source_candidate_set.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")
    for field, reason in SOURCE_TRUE_FIELDS.items():
        if source_candidate_set.get(field) is not True:
            blockers.append(reason)
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if source_candidate_set.get(field) is not False:
            blockers.append(reason)

    runtime_side_effects = source_candidate_set.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("source_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")

    for field, value in source_candidate_set.items():
        if field == "actual_analysis_execution_candidates":
            continue
        if field in FORBIDDEN_SOURCE_FIELDS:
            if field in SOURCE_FALSE_FIELDS and value is False:
                continue
            blockers.append(f"forbidden_source_actual_analysis_execution_candidate_set_field:{field}")
        elif _contains_forbidden_value(value):
            blockers.append(f"source_actual_analysis_execution_candidate_set_forbidden_value:{field}")
    return _dedupe(blockers)


def _source_candidate_blockers(source_candidates: list[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    for candidate in source_candidates:
        if not isinstance(candidate, dict):
            blockers.append("source_actual_analysis_execution_candidate_not_object")
            continue
        for field, value in candidate.items():
            if field in FORBIDDEN_SOURCE_FIELDS:
                if field in SOURCE_FALSE_FIELDS and value is False:
                    continue
                blockers.append(f"forbidden_source_actual_analysis_execution_candidate_field:{field}")
            elif _contains_forbidden_value(value):
                blockers.append(f"source_actual_analysis_execution_candidate_forbidden_value:{field}")
        if candidate.get("actual_analysis_execution_candidate_schema") != SOURCE_CANDIDATE_SCHEMA:
            blockers.append("source_actual_analysis_execution_candidate_schema_wrong")
        if candidate.get("source_actual_analysis_execution_candidate_count") not in (None, 1):
            blockers.append("source_candidate_actual_analysis_execution_candidate_count_not_one")
        if candidate.get("source_production_analysis_run_candidate_count") != (
            EXPECTED_SOURCE_PRODUCTION_ANALYSIS_RUN_CANDIDATE_COUNT
        ):
            blockers.append("source_candidate_production_analysis_run_candidate_count_not_one")
        if candidate.get("source_production_case_candidate_count") != EXPECTED_SOURCE_PRODUCTION_CASE_CANDIDATE_COUNT:
            blockers.append("source_candidate_production_case_candidate_count_not_one")
        if candidate.get("source_controlled_evidence_item_count") != EXPECTED_SOURCE_CONTROLLED_EVIDENCE_ITEM_COUNT:
            blockers.append("source_candidate_controlled_evidence_item_count_not_five")
        if candidate.get("human_review_required") is not True:
            blockers.append("source_actual_analysis_execution_candidate_human_review_required_not_true")
        if candidate.get("no_automatic_trust_upgrade") is not True:
            blockers.append("source_actual_analysis_execution_candidate_no_automatic_trust_upgrade_not_true")
        if candidate.get("actual_analysis_execution_candidate_only") is not True:
            blockers.append("source_actual_analysis_execution_candidate_only_not_true")
        if candidate.get("actual_analysis_execution_started") is not False:
            blockers.append("source_candidate_actual_analysis_execution_started_true")
        if candidate.get("analysis_execution_started") is not False:
            blockers.append("source_candidate_analysis_execution_started_true")
        if candidate.get("analysis_result_created") is not False:
            blockers.append("source_candidate_analysis_result_created_true")
        if candidate.get("production_analysis_result_created") is not False:
            blockers.append("source_candidate_production_analysis_result_created_true")
        if candidate.get("production_analysis_run_created") is not False:
            blockers.append("source_candidate_production_analysis_run_created_true")
        if candidate.get("report_ready") is not False:
            blockers.append("source_candidate_report_ready_true")
    return _dedupe(blockers)


def _safe_source_candidates(source_candidate_set: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_candidate_set, dict):
        return []
    candidates = source_candidate_set.get("actual_analysis_execution_candidates")
    if not isinstance(candidates, list):
        return []
    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def _source_actual_analysis_execution_candidate_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("actual_analysis_execution_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return len(source_candidates)


def _source_production_analysis_run_candidate_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("source_production_analysis_run_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    if source_candidates:
        count = source_candidates[0].get("source_production_analysis_run_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return 0


def _source_production_case_candidate_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("source_production_case_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    if source_candidates:
        count = source_candidates[0].get("source_production_case_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return 0


def _source_controlled_evidence_item_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("source_controlled_evidence_item_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    if source_candidates:
        count = source_candidates[0].get("source_controlled_evidence_item_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return 0


def _source_warning_count(source_candidate_set: dict[str, Any] | None) -> int:
    if isinstance(source_candidate_set, dict):
        warning_count = source_candidate_set.get("warning_count")
        if isinstance(warning_count, int) and not isinstance(warning_count, bool):
            return max(warning_count, 0)
    return 0


def _source_actual_analysis_execution_candidate_schema(source_candidate_set: dict[str, Any] | None) -> str | None:
    candidates = _safe_source_candidates(source_candidate_set)
    if candidates:
        return _safe_label(candidates[0].get("actual_analysis_execution_candidate_schema"))
    return None


def _safe_source_value(source_candidate_set: dict[str, Any] | None, field: str) -> str | None:
    if not isinstance(source_candidate_set, dict):
        return None
    return _safe_label(source_candidate_set.get(field))


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_invalid_source_actual_analysis_execution_candidate"
    first = blockers[0]
    if first in {
        "blocked_missing_exact_approval",
        "blocked_wrong_exact_approval",
        "blocked_non_ascii_approval",
        "blocked_garbled_approval",
    }:
        return first
    if first.startswith("requested_action_blocked"):
        if "production_analysis_result" in first:
            return "blocked_unapproved_production_analysis_result_creation_request"
        if "analysis_result_generation" in first:
            return "blocked_unapproved_analysis_result_generation_request"
        if any(marker in first for marker in ("actual_analysis_execution", "analysis_execution", "execute")):
            return "blocked_unapproved_actual_analysis_execution_request"
        if "production_analysis_run" in first:
            return "blocked_unapproved_production_analysis_run_creation_request"
        if "production_case" in first:
            return "blocked_unapproved_production_case_creation_request"
        if "production_evidence_item" in first:
            return "blocked_unapproved_production_evidence_item_request"
        if "review_queue" in first:
            return "blocked_unapproved_review_queue_request"
        if any(marker in first for marker in ("route", "frontend")):
            return "blocked_unapproved_route_api_frontend_request"
        if "row_parsing" in first:
            return "blocked_unapproved_row_parsing_request"
        if any(marker in first for marker in ("collector", "real_exchange", "real_api", "provider_job")):
            return "blocked_unapproved_collector_or_real_exchange_request"
        if any(
            marker in first
            for marker in (
                "b_end_report",
                "sandbox",
                "download",
                "public_access",
                "external_delivery",
                "final_delivery",
            )
        ):
            return "blocked_unapproved_report_or_public_output_request"
        return "blocked_source_boundary_violation"
    if first == "source_warning_count_not_one":
        return "blocked_warning_state_missing"
    if first == "source_human_review_required_not_true":
        return "blocked_manual_review_state_missing"
    if first.startswith("source_actual_analysis_execution_candidate_count") or first.startswith(
        "source_actual_analysis_execution_candidates_count"
    ):
        return "blocked_candidate_limit_violation"
    if first.startswith("source_production_analysis_run_candidate_count"):
        return "blocked_candidate_limit_violation"
    if first.startswith("source_production_case_candidate_count"):
        return "blocked_candidate_limit_violation"
    if first.startswith("source_controlled_evidence_item_count"):
        return "blocked_candidate_limit_violation"
    if first.startswith("forbidden_source") or first.startswith("source_actual_analysis_execution_candidate_forbidden"):
        return "blocked_forbidden_field_detected"
    if first.startswith("source_runtime_side_effect") or first.startswith("source_"):
        return "blocked_source_boundary_violation"
    return "blocked_invalid_source_actual_analysis_execution_candidate"


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


def _candidate_warnings(source_candidate_set: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only", "analysis_result_candidate_only"]
    if isinstance(source_candidate_set, dict):
        source_warnings = source_candidate_set.get("warnings")
        if isinstance(source_warnings, list):
            warnings.extend(item for item in source_warnings if isinstance(item, str))
    return _dedupe(warnings)


def _merged_warning_labels(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> list[str]:
    labels = _candidate_warnings(source_candidate_set)
    for candidate in source_candidates:
        value = candidate.get("warning_labels")
        if isinstance(value, list):
            labels.extend(label for label in value if isinstance(label, str))
        redaction_warnings = candidate.get("redaction_warnings")
        if isinstance(redaction_warnings, list):
            labels.extend(label for label in redaction_warnings if isinstance(label, str))
    return _dedupe([_safe_label(label) or "manual_review_required" for label in labels])


def _analysis_result_candidate_id(source_ids: list[str]) -> str:
    first_id = source_ids[0] if source_ids else "unknown"
    return f"controlled-analysis-result-candidate-001-{first_id}"


def _contains_forbidden_value(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_forbidden_value(nested) for nested in value.values())
    if isinstance(value, list):
        return any(_contains_forbidden_value(item) for item in value)
    if not isinstance(value, str):
        return False
    return _looks_forbidden(value)


def _looks_forbidden(value: str) -> bool:
    lowered = value.lower()
    if "should-never-appear" in lowered:
        return True
    if "token=" in lowered or "cookie=" in lowered or "api_key=" in lowered:
        return True
    if "private-collector" in lowered or "private_collector" in lowered:
        return True
    if ":\\" in value or ":/" in value:
        return True
    if "donglu_sunjihai_youth_football/" in value or "donglu_sunjihai_youth_football\\" in value:
        return True
    return False


def _safe_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    if not stripped or _looks_forbidden(stripped):
        return None
    return stripped


def _safe_token(value: Any) -> str:
    text = _safe_text(value)
    if text is None:
        return "unknown"
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:120]


def _safe_label(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:160]


def _truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "requested", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
