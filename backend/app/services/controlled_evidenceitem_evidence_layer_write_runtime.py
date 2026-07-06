from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


RUNTIME_SCHEMA = "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1"
WRITE_RESULT_SCHEMA = "sentigraph_controlled_evidence_layer_write_result_v0_1"
CONTROLLED_EVIDENCE_ITEM_SCHEMA = "sentigraph_controlled_evidence_item_v0_1"
SUMMARY_SCHEMA = "sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_summary_v0_1"
SOURCE_CANDIDATE_SET_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)
SOURCE_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1"
)
PHASE = "8W-28"
SOURCE_PHASE = "8W-25"
APPROVAL_PHRASE = "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION"
SOURCE_WARN_STATUS = "evidence_layer_write_candidate_set_warn_manual_review_required"
WARN_STATUS = "evidence_layer_write_runtime_warn_manual_review_required"
HARD_CANDIDATE_BOUND = 10

REQUIRED_SOURCE_CANDIDATE_FIELDS = [
    "evidence_layer_write_candidate_schema",
    "evidence_layer_write_candidate_id",
    "source_production_evidence_import_candidate_id",
    "source_evidence_layer_write_candidate_id",
    "source_evidence_layer_import_candidate_id",
    "source_review_queue_candidate_id",
    "source_evidence_candidate_id",
    "evidence_id_hash",
    "text_snippet_redacted",
]

OPTIONAL_SAFE_SOURCE_CANDIDATE_FIELDS = [
    "preview_hash",
    "case_id_hint",
    "platform",
    "evidence_type",
    "coarse_created_at",
    "created_at_date",
    "source_url_present",
    "acquisition_mode",
    "provenance_type",
    "verification_status",
    "review_status",
    "trust_label",
    "redaction_status",
    "title_or_label_redacted",
]

FORBIDDEN_SOURCE_CANDIDATE_FIELDS = {
    "raw_author_id",
    "raw_author_ids",
    "raw_author_identifier",
    "raw_author_identifiers",
    "author_id",
    "author_ids",
    "raw_author_name",
    "raw_author_names",
    "author_name",
    "author_names",
    "username",
    "user_name",
    "display_name",
    "profile_url",
    "profile_urls",
    "raw_profile_url",
    "source_url",
    "url",
    "raw_comment",
    "raw_comments",
    "private_message",
    "private_messages",
    "email",
    "phone",
    "address",
    "identity",
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
    "browser_profile",
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
    "review_queue_item_id",
    "production_review_queue_item_id",
    "production_case_id",
    "production_analysis_run_id",
    "report_id",
    "sandbox_id",
    "public_event_id",
    "download_id",
    "public_access_id",
    "delivery_id",
}

REQUESTED_ACTIONS_BLOCKED = {
    "production_case",
    "production_analysis_run",
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

TOP_LEVEL_FALSE_FIELDS = {
    "production_evidence_import_candidate_created": "source_production_evidence_import_candidate_created_true",
    "evidence_item_created": "source_evidence_item_created_true",
    "evidence_items_created": "source_evidence_items_created_true",
    "production_evidence_item_created": "source_production_evidence_item_created_true",
    "evidence_layer_write": "source_evidence_layer_write_true",
    "review_queue_item_created": "source_review_queue_item_created_true",
    "production_review_queue_item_created": "source_production_review_queue_item_created_true",
    "production_case_created": "source_production_case_created_true",
    "production_analysis_run_created": "source_production_analysis_run_created_true",
    "route_ready": "source_route_ready_true",
    "frontend_ready": "source_frontend_ready_true",
    "production_ready": "source_production_ready_true",
    "public_ready": "source_public_ready_true",
    "customer_ready": "source_customer_ready_true",
    "b_end_ready": "source_b_end_ready_true",
    "sandbox_ready": "source_sandbox_ready_true",
    "public_event_ready": "source_public_event_ready_true",
    "b_end_report_runtime_generated": "source_b_end_report_runtime_generated_true",
    "sandbox_public_event_generated": "source_sandbox_public_event_generated_true",
    "generated_response_text": "source_generated_response_text_true",
    "public_route_created": "source_public_route_created_true",
    "download_package_runtime_used": "source_download_package_runtime_used_true",
    "public_access_runtime_used": "source_public_access_runtime_used_true",
    "external_delivery_runtime_used": "source_external_delivery_runtime_used_true",
    "final_delivery_runtime_used": "source_final_delivery_runtime_used_true",
    "absolute_path_exposed": "source_absolute_path_exposed",
    "package_path_exposed": "source_package_path_exposed",
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
    "wrote_evidence_layer",
    "created_evidence_items",
    "created_evidence_item",
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


def build_controlled_evidenceitem_evidence_layer_write_runtime(
    controlled_evidence_layer_write_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a local, controlled EvidenceItem-shaped write result from 8W-25 candidates."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))

    source_candidates = _safe_source_candidates(controlled_evidence_layer_write_candidate_set)
    source_candidate_count = _source_candidate_count(controlled_evidence_layer_write_candidate_set, source_candidates)
    effective_limit = source_candidate_count if candidate_limit is None else candidate_limit

    blockers.extend(_candidate_limit_blockers(effective_limit, source_candidate_count))
    blockers.extend(
        _source_candidate_set_blockers(
            controlled_evidence_layer_write_candidate_set,
            source_candidates,
        )
    )

    controlled_items: list[dict[str, Any]] = []
    if not blockers:
        controlled_items, candidate_blockers = _build_controlled_items(source_candidates[:effective_limit])
        blockers.extend(candidate_blockers)
        if blockers:
            controlled_items = []

    if blockers:
        return _base_output(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            warnings=[],
            controlled_items=[],
            source_candidate_set=controlled_evidence_layer_write_candidate_set,
            source_candidate_count=source_candidate_count,
        )

    return _base_output(
        status=WARN_STATUS,
        created=True,
        blockers=[],
        warnings=_runtime_warnings(controlled_evidence_layer_write_candidate_set),
        controlled_items=controlled_items,
        source_candidate_set=controlled_evidence_layer_write_candidate_set,
        source_candidate_count=source_candidate_count,
    )


create_controlled_evidenceitem_evidence_layer_write_runtime = (
    build_controlled_evidenceitem_evidence_layer_write_runtime
)


def build_safe_controlled_evidenceitem_evidence_layer_write_runtime_summary(
    controlled_evidence_layer_write_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    runtime = build_controlled_evidenceitem_evidence_layer_write_runtime(
        controlled_evidence_layer_write_candidate_set,
        exact_approval_phrase=exact_approval_phrase,
        candidate_limit=candidate_limit,
        requested_actions=requested_actions,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "runtime_schema": RUNTIME_SCHEMA,
        "write_runtime_status": runtime["write_runtime_status"],
        "source_candidate_set_schema": runtime["source_candidate_set_schema"],
        "source_candidate_set_status": runtime["source_candidate_set_status"],
        "source_candidate_count": runtime["source_candidate_count"],
        "controlled_evidence_item_schema": CONTROLLED_EVIDENCE_ITEM_SCHEMA,
        "controlled_evidence_item_count": runtime["controlled_evidence_item_count"],
        "write_result_schema": WRITE_RESULT_SCHEMA,
        "controlled_evidence_layer_write_result_created": runtime[
            "controlled_evidence_layer_write_result_created"
        ],
        "controlled_evidenceitem_created": runtime["controlled_evidenceitem_created"],
        "evidence_item_created": runtime["evidence_item_created"],
        "evidence_items_created": runtime["evidence_items_created"],
        "evidence_layer_write": runtime["evidence_layer_write"],
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "warning_count": runtime["warning_count"],
        "human_review_required": runtime["human_review_required"],
        "no_automatic_trust_upgrade": runtime["no_automatic_trust_upgrade"],
        "analysis_ready": False,
        "report_ready": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "blockers": list(runtime["blockers"]),
        "warnings": list(runtime["warnings"]),
        "audit_summary": dict(runtime["audit_summary"]),
    }


def _base_output(
    *,
    status: str,
    created: bool,
    blockers: list[str],
    warnings: list[str],
    controlled_items: list[dict[str, Any]],
    source_candidate_set: dict[str, Any] | None,
    source_candidate_count: int,
) -> dict[str, Any]:
    return {
        "runtime_schema": RUNTIME_SCHEMA,
        "phase": PHASE,
        "created_at": _utc_now(),
        "write_runtime_status": status,
        "input_source_kind": "controlled_evidence_layer_write_candidate_set",
        "source_candidate_set_schema": _safe_source_value(
            source_candidate_set,
            "evidence_layer_write_candidate_set_schema",
        ),
        "source_candidate_set_status": _safe_source_value(
            source_candidate_set,
            "evidence_layer_write_candidate_set_status",
        ),
        "source_candidate_count": source_candidate_count,
        "controlled_evidence_item_schema": CONTROLLED_EVIDENCE_ITEM_SCHEMA,
        "controlled_evidence_item_count": len(controlled_items),
        "write_result_schema": WRITE_RESULT_SCHEMA,
        "controlled_evidence_layer_write_result_created": created,
        "controlled_evidenceitem_created": created,
        "evidence_item_created": created,
        "evidence_items_created": created,
        "evidence_layer_write": created,
        "evidence_layer_write_scope": (
            "controlled_local_helper_test_path_only" if created else "not_performed"
        ),
        "production_evidence_item_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "review_queue_runtime_used": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
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
        "warning_count": _source_warning_count(source_candidate_set),
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
        "controlled_evidence_items": controlled_items,
        "controlled_evidence_layer_write_result": _write_result(controlled_items, created=created),
        "boundary_flags": {
            "backend_only": True,
            "local_only": True,
            "controlled_local_write_only": created,
            "human_review_required": True,
            "warning_preserving": True,
            "no_automatic_trust_upgrade": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
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
            "audit_schema": "sentigraph_controlled_evidence_layer_write_runtime_audit_summary_v0_1",
            "phase": PHASE,
            "analysis_effect": "controlled_local_evidence_layer_write_only" if created else "none",
            "production_side_effect": "none",
            "human_review_required": True,
            "warning_count": _source_warning_count(source_candidate_set),
            "controlled_evidence_item_count": len(controlled_items),
            "review_queue_effect": "none",
            "route_api_frontend_effect": "none",
            "delivery_effect": "none",
        },
    }


def _write_result(controlled_items: list[dict[str, Any]], *, created: bool) -> dict[str, Any]:
    return {
        "write_result_schema": WRITE_RESULT_SCHEMA,
        "phase": PHASE,
        "controlled_evidence_layer_write_result_created": created,
        "controlled_evidence_item_count": len(controlled_items),
        "evidence_layer_write_scope": (
            "controlled_local_helper_test_path_only" if created else "not_performed"
        ),
        "production_evidence_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "analysis_ready": False,
        "report_ready": False,
        "human_review_required": True,
        "no_automatic_trust_upgrade": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        return ["blocked_missing_exact_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_approval"]
    return []


def _source_candidate_set_blockers(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> list[str]:
    if not isinstance(source_candidate_set, dict):
        return ["source_evidence_layer_write_candidate_set_missing_or_not_object"]

    blockers: list[str] = []
    expected = {
        "evidence_layer_write_candidate_set_schema": (
            SOURCE_CANDIDATE_SET_SCHEMA,
            "source_evidence_layer_write_candidate_set_schema_wrong",
        ),
        "phase": (SOURCE_PHASE, "source_evidence_layer_write_candidate_set_phase_wrong"),
        "evidence_layer_write_candidate_set_status": (
            SOURCE_WARN_STATUS,
            "source_evidence_layer_write_candidate_set_status_not_warn_manual_review",
        ),
    }
    for field, (expected_value, reason) in expected.items():
        if source_candidate_set.get(field) != expected_value:
            blockers.append(reason)

    true_fields = {
        "human_review_required": "source_human_review_required_not_true",
        "preview_only": "source_preview_only_not_true",
        "import_candidate_only": "source_import_candidate_only_not_true",
        "production_import_candidate_only": "source_production_import_candidate_only_not_true",
        "write_candidate_only": "source_write_candidate_only_not_true",
        "evidence_layer_write_candidate_only": "source_evidence_layer_write_candidate_only_not_true",
        "evidence_layer_write_candidate_helper_implementation_approved": (
            "source_evidence_layer_write_candidate_helper_not_approved"
        ),
        "evidence_layer_write_candidate_created": (
            "source_evidence_layer_write_candidate_created_not_true"
        ),
    }
    for field, reason in true_fields.items():
        if source_candidate_set.get(field) is not True:
            blockers.append(reason)

    if source_candidate_set.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")

    candidate_count = source_candidate_set.get("evidence_layer_write_candidate_count")
    source_production_import_count = source_candidate_set.get("source_production_evidence_import_candidate_count")
    if not isinstance(candidate_count, int) or isinstance(candidate_count, bool):
        blockers.append("source_evidence_layer_write_candidate_count_missing_or_invalid")
    elif candidate_count != len(source_candidates):
        blockers.append("source_evidence_layer_write_candidate_count_inconsistent")
    elif candidate_count < 1:
        blockers.append("source_evidence_layer_write_candidates_missing")
    elif candidate_count > HARD_CANDIDATE_BOUND:
        blockers.append("source_evidence_layer_write_candidate_count_too_high")

    if not isinstance(source_production_import_count, int) or isinstance(source_production_import_count, bool):
        blockers.append("source_production_evidence_import_candidate_count_missing_or_invalid")
    elif isinstance(candidate_count, int) and not isinstance(candidate_count, bool):
        if source_production_import_count < candidate_count:
            blockers.append("source_production_evidence_import_candidate_count_less_than_write_candidate_count")
        if source_production_import_count > HARD_CANDIDATE_BOUND:
            blockers.append("source_production_evidence_import_candidate_count_too_high")

    for field, reason in TOP_LEVEL_FALSE_FIELDS.items():
        if source_candidate_set.get(field) is True:
            blockers.append(reason)

    runtime_side_effects = source_candidate_set.get("runtime_side_effects")
    if not isinstance(runtime_side_effects, dict):
        blockers.append("source_runtime_side_effects_missing_or_invalid")
    else:
        for flag, value in runtime_side_effects.items():
            if value is True:
                blockers.append(f"source_runtime_side_effect_true:{flag}")

    return _dedupe(blockers)


def _candidate_limit_blockers(candidate_limit: Any, source_candidate_count: int) -> list[str]:
    if isinstance(candidate_limit, bool) or not isinstance(candidate_limit, int):
        return ["blocked_candidate_limit_invalid"]
    if candidate_limit <= 0:
        return ["blocked_candidate_limit_not_positive"]
    blockers: list[str] = []
    if candidate_limit > HARD_CANDIDATE_BOUND:
        blockers.append("blocked_candidate_limit_too_high")
    if source_candidate_count >= 0 and candidate_limit > source_candidate_count:
        blockers.append("blocked_candidate_limit_exceeds_source_candidate_count")
    return blockers


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


def _build_controlled_items(source_candidates: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    controlled_items: list[dict[str, Any]] = []
    blockers: list[str] = []
    for index, source_candidate in enumerate(source_candidates, start=1):
        candidate_blockers = _source_candidate_blockers(source_candidate)
        if candidate_blockers:
            blockers.extend(candidate_blockers)
            continue
        controlled_items.append(_controlled_item_from_source(source_candidate, index=index))
    return controlled_items, _dedupe(blockers)


def _source_candidate_blockers(source_candidate: dict[str, Any]) -> list[str]:
    if not isinstance(source_candidate, dict):
        return ["source_evidence_layer_write_candidate_not_object"]
    blockers: list[str] = []
    for field in source_candidate:
        if field in FORBIDDEN_SOURCE_CANDIDATE_FIELDS:
            blockers.append(f"forbidden_source_evidence_layer_write_candidate_field:{field}")
    for field in REQUIRED_SOURCE_CANDIDATE_FIELDS:
        value = source_candidate.get(field)
        if value is None or value == "":
            blockers.append(f"source_evidence_layer_write_candidate_missing_required_field:{field}")
    if source_candidate.get("evidence_layer_write_candidate_schema") != SOURCE_CANDIDATE_SCHEMA:
        blockers.append("source_evidence_layer_write_candidate_schema_wrong")
    if source_candidate.get("human_review_required") is not True:
        blockers.append("source_evidence_layer_write_candidate_human_review_required_not_true")
    if source_candidate.get("preview_only") is not True:
        blockers.append("source_evidence_layer_write_candidate_preview_only_not_true")
    if source_candidate.get("import_candidate_only") is not True:
        blockers.append("source_evidence_layer_write_candidate_import_candidate_only_not_true")
    if source_candidate.get("production_import_candidate_only") is not True:
        blockers.append("source_evidence_layer_write_candidate_production_import_candidate_only_not_true")
    if source_candidate.get("write_candidate_only") is not True:
        blockers.append("source_evidence_layer_write_candidate_write_candidate_only_not_true")
    if source_candidate.get("evidence_layer_write_candidate_only") is not True:
        blockers.append("source_evidence_layer_write_candidate_evidence_layer_write_candidate_only_not_true")

    boundary_flags = source_candidate.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        blockers.append("source_evidence_layer_write_candidate_boundary_flags_missing_or_invalid")
    else:
        required_true_flags = {
            "preview_only": "source_evidence_layer_write_candidate_boundary_preview_only_not_true",
            "human_review_required": (
                "source_evidence_layer_write_candidate_boundary_human_review_required_not_true"
            ),
            "import_candidate_only": "source_evidence_layer_write_candidate_boundary_import_candidate_only_not_true",
            "production_import_candidate_only": (
                "source_evidence_layer_write_candidate_boundary_production_import_candidate_only_not_true"
            ),
            "write_candidate_only": "source_evidence_layer_write_candidate_boundary_write_candidate_only_not_true",
            "evidence_layer_write_candidate_only": (
                "source_evidence_layer_write_candidate_boundary_evidence_layer_write_candidate_only_not_true"
            ),
            "not_evidence_item": "source_evidence_layer_write_candidate_boundary_not_evidence_item_not_true",
            "not_production_evidence_item": (
                "source_evidence_layer_write_candidate_boundary_not_production_evidence_item_not_true"
            ),
            "no_evidence_layer_write": (
                "source_evidence_layer_write_candidate_boundary_no_evidence_layer_write_not_true"
            ),
            "not_review_queue_item": (
                "source_evidence_layer_write_candidate_boundary_not_review_queue_item_not_true"
            ),
            "not_production_review_queue_item": (
                "source_evidence_layer_write_candidate_boundary_not_production_review_queue_item_not_true"
            ),
            "not_production_case": (
                "source_evidence_layer_write_candidate_boundary_not_production_case_not_true"
            ),
            "not_production_analysis_run": (
                "source_evidence_layer_write_candidate_boundary_not_production_analysis_run_not_true"
            ),
        }
        for flag, reason in required_true_flags.items():
            if boundary_flags.get(flag) is not True:
                blockers.append(reason)

    safe_fields = [
        *REQUIRED_SOURCE_CANDIDATE_FIELDS,
        *OPTIONAL_SAFE_SOURCE_CANDIDATE_FIELDS,
        "redaction_warnings",
        "warning_labels",
        "evidence_layer_write_readiness_blockers",
        "blocker_codes",
    ]
    for field in safe_fields:
        value = source_candidate.get(field)
        if _contains_forbidden_value(value):
            blockers.append(f"source_evidence_layer_write_candidate_forbidden_value:{field}")
    return _dedupe(blockers)


def _controlled_item_from_source(source_candidate: dict[str, Any], *, index: int) -> dict[str, Any]:
    evidence_hash = _safe_token(source_candidate.get("evidence_id_hash"))
    source_write_candidate_id = _safe_token(source_candidate.get("evidence_layer_write_candidate_id"))
    return {
        "controlled_evidence_item_schema": CONTROLLED_EVIDENCE_ITEM_SCHEMA,
        "controlled_evidence_item_id": f"controlled-evidence-item-{index:03d}-{evidence_hash}",
        "source_evidence_layer_write_candidate_id": source_write_candidate_id,
        "source_production_evidence_import_candidate_id": _safe_token(
            source_candidate.get("source_production_evidence_import_candidate_id")
        ),
        "source_evidence_layer_import_candidate_id": _safe_token(
            source_candidate.get("source_evidence_layer_import_candidate_id")
        ),
        "source_review_queue_candidate_id": _safe_token(source_candidate.get("source_review_queue_candidate_id")),
        "source_evidence_candidate_id": _safe_token(source_candidate.get("source_evidence_candidate_id")),
        "evidence_id_hash": evidence_hash,
        "controlled_content_hash": evidence_hash,
        "preview_hash": _safe_token(source_candidate.get("preview_hash") or source_candidate.get("evidence_id_hash")),
        "case_id_hint": _safe_token(source_candidate.get("case_id_hint")) if source_candidate.get("case_id_hint") else None,
        "platform": _safe_label(source_candidate.get("platform")),
        "evidence_type": _safe_label(source_candidate.get("evidence_type")),
        "coarse_created_at": _safe_date(
            source_candidate.get("coarse_created_at") or source_candidate.get("created_at_date")
        ),
        "source_url_present": source_candidate.get("source_url_present") is True,
        "acquisition_mode": _safe_label(source_candidate.get("acquisition_mode")) or "controlled_local_import",
        "provenance_type": _safe_label(source_candidate.get("provenance_type")) or "evidence_layer_write_candidate",
        "verification_status": _safe_label(source_candidate.get("verification_status")) or "vendor_attested",
        "trust_label": _safe_label(source_candidate.get("trust_label")) or "medium_low",
        "review_status": _safe_label(source_candidate.get("review_status")) or "review_needed",
        "title_or_label_redacted": _safe_snippet(source_candidate.get("title_or_label_redacted"))
        or _safe_label(source_candidate.get("evidence_type")),
        "text_snippet_redacted": _safe_snippet(source_candidate.get("text_snippet_redacted")),
        "redaction_status": _safe_label(source_candidate.get("redaction_status")) or "redacted",
        "redaction_warnings": _safe_string_list(source_candidate.get("redaction_warnings")),
        "warning_labels": _safe_string_list(source_candidate.get("warning_labels")) or [
            "manual_review_required",
            "selected_sample_only",
        ],
        "blocker_codes": _safe_string_list(source_candidate.get("blocker_codes")),
        "human_review_required": True,
        "preview_only": True,
        "import_candidate_only": True,
        "evidence_layer_write_runtime_controlled_only": True,
        "analysis_ready": False,
        "report_ready": False,
        "production_case_ready": False,
        "production_analysis_run_ready": False,
        "boundary_flags": {
            "controlled_local_evidence_item_only": True,
            "controlled_local_evidence_layer_write_only": True,
            "human_review_required": True,
            "preview_only": True,
            "import_candidate_only": True,
            "no_automatic_trust_upgrade": True,
            "not_production_evidence_item": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
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
    }


def _runtime_warnings(source_candidate_set: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_candidate_set, dict):
        source_warnings = source_candidate_set.get("warnings")
        if isinstance(source_warnings, list):
            warnings.extend(item for item in source_warnings if isinstance(item, str))
    return _dedupe(warnings)


def _safe_source_candidates(source_candidate_set: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_candidate_set, dict):
        return []
    candidates = source_candidate_set.get("evidence_layer_write_candidates")
    if not isinstance(candidates, list):
        return []
    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def _source_candidate_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("evidence_layer_write_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return len(source_candidates)


def _source_warning_count(source_candidate_set: dict[str, Any] | None) -> int:
    if isinstance(source_candidate_set, dict):
        warning_count = source_candidate_set.get("warning_count")
        if isinstance(warning_count, int) and not isinstance(warning_count, bool):
            return max(warning_count, 0)
    return 0


def _safe_source_value(source_candidate_set: dict[str, Any] | None, field: str) -> str | None:
    if not isinstance(source_candidate_set, dict):
        return None
    return _safe_label(source_candidate_set.get(field))


def _blocked_status(blockers: list[str]) -> str:
    if not blockers:
        return "blocked_invalid_source_evidence_layer_write_candidate_set"
    first = blockers[0]
    if first in {"blocked_missing_exact_approval", "blocked_wrong_exact_approval"}:
        return first
    if first.startswith("blocked_candidate_limit"):
        return "blocked_candidate_limit_violation"
    if first.startswith("forbidden_source_evidence_layer_write_candidate_field") or first.startswith(
        "source_evidence_layer_write_candidate_forbidden_value"
    ):
        return "blocked_forbidden_field_detected"
    if first.startswith("requested_action_blocked"):
        if any(marker in first for marker in ("production_case", "production_analysis_run")):
            return "blocked_unapproved_production_case_or_analysis_run_request"
        if "review_queue" in first:
            return "blocked_unapproved_review_queue_request"
        if any(marker in first for marker in ("route", "frontend")):
            return "blocked_unapproved_route_api_frontend_request"
        if "row_parsing" in first:
            return "blocked_unapproved_row_parsing_request"
        if any(marker in first for marker in ("collector", "real_exchange", "real_api", "provider_job")):
            return "blocked_unapproved_collector_or_real_exchange_request"
        return "blocked_source_boundary_violation"
    if first.startswith("source_evidence_layer_write_candidate_set") or first.startswith(
        "source_evidence_layer_write_candidate_count"
    ):
        return "blocked_invalid_source_evidence_layer_write_candidate_set"
    if first in {"source_warning_count_not_one"}:
        return "blocked_warning_state_missing"
    if first in {"source_human_review_required_not_true"}:
        return "blocked_manual_review_state_missing"
    if first.startswith("source_evidence_layer_write_candidate") or first == (
        "source_evidence_layer_write_candidate_not_object"
    ):
        return "blocked_invalid_source_evidence_layer_write_candidate_set"
    if first.startswith("source_runtime_side_effect") or first.startswith("source_"):
        return "blocked_source_boundary_violation"
    return "blocked_source_boundary_violation"


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
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:160]


def _safe_snippet(value: Any) -> str:
    text = _safe_text(value)
    if text is None:
        return ""
    return text[:160]


def _safe_date(value: Any) -> str | None:
    text = _safe_text(value)
    if text is None:
        return None
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", text)
    if not match:
        return None
    return match.group(1)


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe: list[str] = []
    for item in value[:20]:
        text = _safe_label(item)
        if text is not None:
            safe.append(text)
    return safe


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
