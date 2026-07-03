from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


CANDIDATE_SET_SCHEMA = "sentigraph_controlled_production_case_candidate_set_v0_1"
CANDIDATE_SCHEMA = "sentigraph_controlled_production_case_candidate_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_production_case_candidate_summary_v0_1"
SOURCE_RUNTIME_SCHEMA = "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1"
SOURCE_WRITE_RESULT_SCHEMA = "sentigraph_controlled_evidence_layer_write_result_v0_1"
SOURCE_CONTROLLED_EVIDENCE_ITEM_SCHEMA = "sentigraph_controlled_evidence_item_v0_1"
PHASE = "8W-31"
APPROVAL_PHRASE = "APPROVE_8W_31_CONTROLLED_PRODUCTION_CASE_CANDIDATE_HELPER_IMPLEMENTATION"
SOURCE_WARN_STATUS = "evidence_layer_write_runtime_warn_manual_review_required"
WARN_STATUS = "production_case_candidate_set_warn_manual_review_required"
EXPECTED_CONTROLLED_EVIDENCE_ITEM_COUNT = 5

FORBIDDEN_SOURCE_FIELDS = {
    "production_case_id",
    "production_analysis_run_id",
    "production_evidence_item_id",
    "review_queue_item_id",
    "production_review_queue_item_id",
    "final_report_id",
    "b_end_report_id",
    "sandbox_id",
    "public_event_id",
    "download_id",
    "public_access_id",
    "external_delivery_id",
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
    "raw_comment",
    "raw_comments",
    "raw_identities",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "address",
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
    "browser_profile",
    "browser_profile_path",
    "absolute_path",
    "package_path",
    "raw_collector_path",
    "generated_response_text",
    "response_text",
    "generated_public_message",
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
    "publish_action",
    "send_action",
    "post_action",
    "execute_action",
}

REQUESTED_ACTIONS_BLOCKED = {
    "production_case",
    "production_analysis_run",
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
    "controlled_evidenceitem_created": "source_controlled_evidenceitem_created_not_true",
    "evidence_item_created": "source_evidence_item_created_not_true",
    "evidence_items_created": "source_evidence_items_created_not_true",
    "controlled_evidence_layer_write_result_created": (
        "source_controlled_evidence_layer_write_result_created_not_true"
    ),
    "evidence_layer_write": "source_evidence_layer_write_not_true",
}

SOURCE_FALSE_FIELDS = {
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
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
    "evidence_items_csv_parsed": "source_evidence_items_csv_parsed_true",
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
    "created_review_action_records",
    "created_review_audit_timeline_records",
    "created_reviewer_assignment_records",
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


def build_controlled_production_case_candidate_set(
    controlled_evidenceitem_runtime: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one local case-level candidate from an 8W-28 controlled runtime output."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))

    source_items = _safe_source_items(controlled_evidenceitem_runtime)
    source_count = _source_controlled_evidence_item_count(controlled_evidenceitem_runtime, source_items)

    blockers.extend(_source_runtime_blockers(controlled_evidenceitem_runtime, source_items, source_count))
    candidate: dict[str, Any] | None = None
    if not blockers:
        candidate_blockers = _source_item_blockers(source_items)
        blockers.extend(candidate_blockers)
        if not blockers:
            candidate = _candidate_from_source(controlled_evidenceitem_runtime, source_items)

    if blockers:
        return _base_output(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            warnings=[],
            candidate=None,
            source_runtime=controlled_evidenceitem_runtime,
            source_count=source_count,
        )

    return _base_output(
        status=WARN_STATUS,
        created=True,
        blockers=[],
        warnings=_candidate_warnings(controlled_evidenceitem_runtime),
        candidate=candidate,
        source_runtime=controlled_evidenceitem_runtime,
        source_count=source_count,
    )


create_controlled_production_case_candidate_set = build_controlled_production_case_candidate_set


def build_safe_controlled_production_case_candidate_summary(
    controlled_evidenceitem_runtime: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate_set = build_controlled_production_case_candidate_set(
        controlled_evidenceitem_runtime,
        exact_approval_phrase=exact_approval_phrase,
        requested_actions=requested_actions,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "production_case_candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "production_case_candidate_set_status": candidate_set["production_case_candidate_set_status"],
        "source_runtime_schema": candidate_set["source_runtime_schema"],
        "source_write_result_schema": candidate_set["source_write_result_schema"],
        "source_controlled_evidence_item_count": candidate_set["source_controlled_evidence_item_count"],
        "production_case_candidate_count": candidate_set["production_case_candidate_count"],
        "production_case_candidate_created": candidate_set["production_case_candidate_created"],
        "warning_count": candidate_set["warning_count"],
        "human_review_required": candidate_set["human_review_required"],
        "no_automatic_trust_upgrade": candidate_set["no_automatic_trust_upgrade"],
        "production_case_created": False,
        "production_analysis_run_created": False,
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
    source_runtime: dict[str, Any] | None,
    source_count: int,
) -> dict[str, Any]:
    candidates = [candidate] if candidate else []
    return {
        "production_case_candidate_set_schema": CANDIDATE_SET_SCHEMA,
        "phase": PHASE,
        "production_case_candidate_set_status": status,
        "created_at": _utc_now(),
        "input_source_kind": "controlled_evidenceitem_evidence_layer_write_runtime",
        "source_runtime_schema": _safe_source_value(source_runtime, "runtime_schema"),
        "source_write_result_schema": _safe_source_value(source_runtime, "write_result_schema"),
        "source_controlled_evidence_item_schema": _safe_source_value(
            source_runtime,
            "controlled_evidence_item_schema",
        ),
        "source_controlled_evidence_item_count": source_count,
        "production_case_candidate_mode": "backend_only_local_production_case_candidate_boundary",
        "warning_count": _source_warning_count(source_runtime),
        "human_review_required": True,
        "production_case_candidate_count": len(candidates),
        "production_case_candidate_created": created,
        "production_case_candidate_only": True,
        "controlled_evidenceitem_created_upstream": _truthy(
            source_runtime.get("controlled_evidenceitem_created") if isinstance(source_runtime, dict) else False
        ),
        "evidence_item_created_upstream": _truthy(
            source_runtime.get("evidence_item_created") if isinstance(source_runtime, dict) else False
        ),
        "evidence_layer_write_upstream": _truthy(
            source_runtime.get("evidence_layer_write") if isinstance(source_runtime, dict) else False
        ),
        "production_case_created": False,
        "production_analysis_run_created": False,
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
        "no_automatic_trust_upgrade": True,
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "production_case_candidate_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
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
        },
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _dedupe(warnings),
        "blockers": _dedupe(blockers),
        "audit_summary": {
            "audit_schema": "sentigraph_controlled_production_case_candidate_audit_summary_v0_1",
            "phase": PHASE,
            "analysis_effect": "none",
            "production_side_effect": "none",
            "human_review_required": True,
            "warning_count": _source_warning_count(source_runtime),
            "production_case_candidate_count": len(candidates),
            "review_queue_effect": "none",
            "route_api_frontend_effect": "none",
            "delivery_effect": "none",
        },
        "production_case_candidates": candidates,
    }


def _candidate_from_source(source_runtime: dict[str, Any] | None, source_items: list[dict[str, Any]]) -> dict[str, Any]:
    refs = [_safe_item_ref(item) for item in source_items]
    warning_labels = _merged_warning_labels(source_runtime, source_items)
    first_case_id_hint = _first_safe_value(source_items, "case_id_hint")
    return {
        "production_case_candidate_schema": CANDIDATE_SCHEMA,
        "production_case_candidate_id": _case_candidate_id(refs),
        "source_runtime_schema": SOURCE_RUNTIME_SCHEMA,
        "source_write_result_schema": SOURCE_WRITE_RESULT_SCHEMA,
        "source_controlled_evidence_item_count": len(source_items),
        "source_controlled_evidence_item_refs": refs,
        "case_id_hint": first_case_id_hint,
        "package_role": "controlled_local_evidence_package_candidate",
        "sample_role": "selected_public_sample_only",
        "candidate_scope": "controlled_local_helper_only",
        "review_status": "review_needed",
        "verification_status": "needs_review",
        "trust_label": _conservative_trust_label(source_items),
        "warning_count": _source_warning_count(source_runtime),
        "warning_labels": warning_labels,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "production_case_candidate_only": True,
        "redaction_status": _redaction_status(source_items),
        "blocker_codes": [],
        "boundary_flags": {
            "production_case_candidate_only": True,
            "controlled_local_helper_only": True,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
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
        "production_case_ready": False,
        "production_analysis_run_ready": False,
        "analysis_ready": False,
        "report_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "public_ready": False,
        "customer_ready": False,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


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


def _source_runtime_blockers(
    source_runtime: dict[str, Any] | None,
    source_items: list[dict[str, Any]],
    source_count: int,
) -> list[str]:
    if not isinstance(source_runtime, dict):
        return ["source_controlled_evidenceitem_runtime_missing_or_not_object"]

    blockers: list[str] = []
    expected = {
        "runtime_schema": (SOURCE_RUNTIME_SCHEMA, "source_runtime_schema_wrong"),
        "write_result_schema": (SOURCE_WRITE_RESULT_SCHEMA, "source_write_result_schema_wrong"),
        "controlled_evidence_item_schema": (
            SOURCE_CONTROLLED_EVIDENCE_ITEM_SCHEMA,
            "source_controlled_evidence_item_schema_wrong",
        ),
        "write_runtime_status": (SOURCE_WARN_STATUS, "source_write_runtime_status_not_warn_manual_review"),
    }
    for field, (expected_value, reason) in expected.items():
        if source_runtime.get(field) != expected_value:
            blockers.append(reason)

    if source_count != EXPECTED_CONTROLLED_EVIDENCE_ITEM_COUNT:
        blockers.append("source_controlled_evidence_item_count_not_five")
    if len(source_items) != source_count:
        blockers.append("source_controlled_evidence_items_count_inconsistent")

    write_candidate_count = source_runtime.get("source_evidence_layer_write_candidate_count")
    if write_candidate_count is None:
        write_candidate_count = source_runtime.get("source_candidate_count")
    if write_candidate_count != EXPECTED_CONTROLLED_EVIDENCE_ITEM_COUNT:
        blockers.append("source_evidence_layer_write_candidate_count_not_five")

    if source_runtime.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")
    for field, reason in SOURCE_TRUE_FIELDS.items():
        if source_runtime.get(field) is not True:
            blockers.append(reason)
    for field, reason in SOURCE_FALSE_FIELDS.items():
        if source_runtime.get(field) is not False:
            blockers.append(reason)

    write_result = source_runtime.get("controlled_evidence_layer_write_result")
    if isinstance(write_result, dict):
        if write_result.get("write_result_schema") != SOURCE_WRITE_RESULT_SCHEMA:
            blockers.append("source_write_result_nested_schema_wrong")
        if write_result.get("production_case_created") is True:
            blockers.append("source_write_result_production_case_created_true")
        if write_result.get("production_analysis_run_created") is True:
            blockers.append("source_write_result_production_analysis_run_created_true")
        if write_result.get("production_evidence_item_created") is True:
            blockers.append("source_write_result_production_evidence_item_created_true")

    runtime_side_effects = source_runtime.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("source_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")

    for field, value in source_runtime.items():
        if field == "controlled_evidence_items":
            continue
        if field in FORBIDDEN_SOURCE_FIELDS:
            if field in SOURCE_FALSE_FIELDS and value is False:
                continue
            blockers.append(f"forbidden_source_controlled_evidenceitem_runtime_field:{field}")
        elif _contains_forbidden_value(value):
            blockers.append(f"source_controlled_evidenceitem_runtime_forbidden_value:{field}")
    return _dedupe(blockers)


def _source_item_blockers(source_items: list[dict[str, Any]]) -> list[str]:
    blockers: list[str] = []
    for item in source_items:
        if not isinstance(item, dict):
            blockers.append("source_controlled_evidence_item_not_object")
            continue
        for field, value in item.items():
            if field in FORBIDDEN_SOURCE_FIELDS:
                blockers.append(f"forbidden_source_controlled_evidence_item_field:{field}")
            elif field in {"text_snippet_redacted", "title_or_label_redacted"}:
                continue
            elif _contains_forbidden_value(value):
                blockers.append(f"source_controlled_evidence_item_forbidden_value:{field}")
        if item.get("controlled_evidence_item_schema") != SOURCE_CONTROLLED_EVIDENCE_ITEM_SCHEMA:
            blockers.append("source_controlled_evidence_item_schema_wrong")
        if item.get("human_review_required") is not True:
            blockers.append("source_controlled_evidence_item_human_review_required_not_true")
        if item.get("preview_only") is not True:
            blockers.append("source_controlled_evidence_item_preview_only_not_true")
        if item.get("analysis_ready") is not False:
            blockers.append("source_controlled_evidence_item_analysis_ready_true")
        if item.get("report_ready") is not False:
            blockers.append("source_controlled_evidence_item_report_ready_true")
        if item.get("production_case_ready") is not False:
            blockers.append("source_controlled_evidence_item_production_case_ready_true")
        if item.get("production_analysis_run_ready") is not False:
            blockers.append("source_controlled_evidence_item_production_analysis_run_ready_true")
    return _dedupe(blockers)


def _safe_source_items(source_runtime: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_runtime, dict):
        return []
    items = source_runtime.get("controlled_evidence_items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _source_controlled_evidence_item_count(source_runtime: dict[str, Any] | None, source_items: list[dict[str, Any]]) -> int:
    if isinstance(source_runtime, dict):
        count = source_runtime.get("controlled_evidence_item_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return len(source_items)


def _source_warning_count(source_runtime: dict[str, Any] | None) -> int:
    if isinstance(source_runtime, dict):
        warning_count = source_runtime.get("warning_count")
        if isinstance(warning_count, int) and not isinstance(warning_count, bool):
            return max(warning_count, 0)
    return 0


def _safe_source_value(source_runtime: dict[str, Any] | None, field: str) -> str | None:
    if not isinstance(source_runtime, dict):
        return None
    return _safe_label(source_runtime.get(field))


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_invalid_source_controlled_evidenceitem_runtime"
    first = blockers[0]
    if first in {
        "blocked_missing_exact_approval",
        "blocked_wrong_exact_approval",
        "blocked_non_ascii_approval",
        "blocked_garbled_approval",
    }:
        return first
    if first.startswith("requested_action_blocked"):
        if "production_case" in first:
            return "blocked_unapproved_production_case_request"
        if "production_analysis_run" in first:
            return "blocked_unapproved_production_analysis_run_request"
        if "production_evidence_item" in first:
            return "blocked_unapproved_production_evidenceitem_request"
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
            for marker in ("b_end_report", "sandbox", "download", "public_access", "external_delivery", "final_delivery")
        ):
            return "blocked_unapproved_report_sandbox_delivery_request"
        return "blocked_source_boundary_violation"
    if first in {"source_warning_count_not_one"}:
        return "blocked_warning_state_missing"
    if first in {"source_human_review_required_not_true"}:
        return "blocked_manual_review_state_missing"
    if first.startswith("source_controlled_evidence_item_count") or first.startswith(
        "source_evidence_layer_write_candidate_count"
    ):
        return "blocked_source_count_violation"
    if first.startswith("forbidden_source") or first.startswith("source_controlled_evidence_item_forbidden_value"):
        return "blocked_forbidden_field_detected"
    if first.startswith("source_runtime_side_effect") or first.startswith("source_"):
        return "blocked_source_boundary_violation"
    return "blocked_invalid_source_controlled_evidenceitem_runtime"


def _safe_item_ref(item: dict[str, Any]) -> dict[str, str]:
    return {
        "controlled_evidence_item_id": _safe_token(item.get("controlled_evidence_item_id")),
        "evidence_id_hash": _safe_token(item.get("evidence_id_hash")),
        "preview_hash": _safe_token(item.get("preview_hash") or item.get("evidence_id_hash")),
        "source_evidence_layer_write_candidate_id": _safe_token(
            item.get("source_evidence_layer_write_candidate_id")
        ),
    }


def _case_candidate_id(refs: list[dict[str, str]]) -> str:
    first_hash = refs[0]["evidence_id_hash"] if refs else "unknown"
    return f"controlled-production-case-candidate-001-{first_hash}"


def _candidate_warnings(source_runtime: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_runtime, dict):
        source_warnings = source_runtime.get("warnings")
        if isinstance(source_warnings, list):
            warnings.extend(item for item in source_warnings if isinstance(item, str))
    return _dedupe(warnings)


def _merged_warning_labels(source_runtime: dict[str, Any] | None, source_items: list[dict[str, Any]]) -> list[str]:
    labels = _candidate_warnings(source_runtime)
    for item in source_items:
        value = item.get("warning_labels")
        if isinstance(value, list):
            labels.extend(label for label in value if isinstance(label, str))
    return _dedupe([_safe_label(label) or "manual_review_required" for label in labels])


def _conservative_trust_label(source_items: list[dict[str, Any]]) -> str:
    labels = {_safe_label(item.get("trust_label")) for item in source_items}
    if "low" in labels:
        return "low"
    if "medium_low" in labels:
        return "medium_low"
    return "medium_low"


def _redaction_status(source_items: list[dict[str, Any]]) -> str:
    statuses = {_safe_label(item.get("redaction_status")) for item in source_items}
    if "redacted" in statuses:
        return "redacted"
    return "redacted"


def _first_safe_value(items: list[dict[str, Any]], field: str) -> str | None:
    for item in items:
        text = _safe_label(item.get(field))
        if text:
            return text
    return None


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
    if "actual-" in lowered and "should-never-appear" in lowered:
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
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:80]


def _safe_label(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:120]


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
