from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


EVIDENCE_LAYER_WRITE_CANDIDATE_SET_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1"
)
EVIDENCE_LAYER_WRITE_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1"
)
SUMMARY_SCHEMA = (
    "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_summary_v0_1"
)
SOURCE_PRODUCTION_EVIDENCE_IMPORT_CANDIDATE_SET_SCHEMA = (
    "sentigraph_controlled_production_evidence_import_candidate_set_v0_1"
)
SOURCE_PRODUCTION_EVIDENCE_IMPORT_CANDIDATE_SCHEMA = (
    "sentigraph_controlled_production_evidence_import_candidate_v0_1"
)
SOURCE_PHASE = "8W-22"
PHASE = "8W-25"
APPROVAL_PHRASE = "批准 8W-25 Controlled Evidence Layer Write Candidate Helper Implementation"
SOURCE_WARN_STATUS = "production_evidence_import_candidate_set_warn_manual_review_required"
READY_STATUS = "evidence_layer_write_candidate_set_ready_for_manual_review"
WARN_STATUS = "evidence_layer_write_candidate_set_warn_manual_review_required"
HARD_CANDIDATE_BOUND = 10

EVIDENCE_LAYER_WRITE_CANDIDATE_MODE = "backend_only_local_evidence_layer_write_candidate_boundary"

REQUIRED_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS = [
    "production_evidence_import_candidate_schema",
    "production_evidence_import_candidate_id",
    "source_evidence_layer_write_candidate_id",
    "source_evidence_layer_import_candidate_id",
    "source_review_queue_candidate_id",
    "source_evidence_candidate_id",
    "evidence_id_hash",
    "text_snippet_redacted",
]

OPTIONAL_SAFE_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS = [
    "preview_hash",
    "platform",
    "evidence_type",
    "coarse_created_at",
    "created_at_date",
    "source_url_present",
    "trust_boundary_label",
    "verification_status",
    "review_status",
    "trust_label",
    "redaction_status",
    "title_or_label_redacted",
]

FORBIDDEN_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS = {
    "evidence_item_id",
    "production_evidence_item_id",
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
    "evidence_item_creation",
    "production_evidence_item_creation",
    "evidence_layer_write",
    "review_queue_item_creation",
    "review_queue_runtime",
    "production_review_queue_item_creation",
    "production_case",
    "production_analysis_run",
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
    "publish",
    "send",
    "post",
    "execute",
    "auto_execute",
}

TOP_LEVEL_FALSE_FIELDS = {
    "evidence_layer_write_candidate_created": "source_evidence_layer_write_candidate_created_true",
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


def build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set(
    controlled_production_evidence_import_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create local, human-review-only write-candidate boundary objects from production import candidates."""

    blockers: list[str] = []
    blockers.extend(_approval_blockers(exact_approval_phrase))
    blockers.extend(_requested_action_blockers(requested_actions))

    source_candidates = _safe_source_candidates(controlled_production_evidence_import_candidate_set)
    source_candidate_count = _source_production_evidence_import_candidate_count(
        controlled_production_evidence_import_candidate_set,
        source_candidates,
    )
    effective_limit = source_candidate_count if candidate_limit is None else candidate_limit

    blockers.extend(_candidate_limit_blockers(effective_limit, source_candidate_count))
    blockers.extend(
        _source_production_evidence_import_candidate_set_blockers(
            controlled_production_evidence_import_candidate_set,
            source_candidates,
        )
    )

    write_candidates: list[dict[str, Any]] = []
    if not blockers:
        candidate_rows, candidate_blockers = _build_write_candidates(source_candidates[:effective_limit])
        blockers.extend(candidate_blockers)
        write_candidates = candidate_rows if not blockers else []

    if blockers:
        return _base_output(
            status=_blocked_status(blockers),
            created=False,
            blockers=blockers,
            write_candidates=[],
            source_candidate_set=controlled_production_evidence_import_candidate_set,
            source_candidate_count=source_candidate_count,
        )

    status = WARN_STATUS if _source_warning_count(controlled_production_evidence_import_candidate_set) else READY_STATUS
    return _base_output(
        status=status,
        created=True,
        blockers=[],
        warnings=_write_candidate_warnings(controlled_production_evidence_import_candidate_set),
        write_candidates=write_candidates,
        source_candidate_set=controlled_production_evidence_import_candidate_set,
        source_candidate_count=source_candidate_count,
    )


create_controlled_evidence_layer_write_candidate_from_production_import_candidate_set = (
    build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set
)


def build_safe_controlled_evidence_layer_write_candidate_from_production_import_candidate_summary(
    controlled_production_evidence_import_candidate_set: dict[str, Any] | None,
    *,
    exact_approval_phrase: str | None,
    candidate_limit: int | None = None,
    requested_actions: list[str] | dict[str, Any] | None = None,
) -> dict[str, Any]:
    candidate_set = build_controlled_evidence_layer_write_candidate_from_production_import_candidate_set(
        controlled_production_evidence_import_candidate_set,
        exact_approval_phrase=exact_approval_phrase,
        candidate_limit=candidate_limit,
        requested_actions=requested_actions,
    )
    return {
        "summary_schema": SUMMARY_SCHEMA,
        "phase": PHASE,
        "evidence_layer_write_candidate_set_schema": EVIDENCE_LAYER_WRITE_CANDIDATE_SET_SCHEMA,
        "evidence_layer_write_candidate_set_status": candidate_set["evidence_layer_write_candidate_set_status"],
        "evidence_layer_write_candidate_count": candidate_set["evidence_layer_write_candidate_count"],
        "source_production_evidence_import_candidate_count": candidate_set[
            "source_production_evidence_import_candidate_count"
        ],
        "warning_count": candidate_set["warning_count"],
        "human_review_required": candidate_set["human_review_required"],
        "preview_only": candidate_set["preview_only"],
        "import_candidate_only": candidate_set["import_candidate_only"],
        "production_import_candidate_only": candidate_set["production_import_candidate_only"],
        "write_candidate_only": candidate_set["write_candidate_only"],
        "evidence_layer_write_candidate_only": candidate_set["evidence_layer_write_candidate_only"],
        "evidence_item_created": False,
        "evidence_items_created": False,
        "production_evidence_item_created": False,
        "evidence_layer_write": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "blockers": list(candidate_set["blockers"]),
        "warnings": list(candidate_set["warnings"]),
        "runtime_side_effects": dict(candidate_set["runtime_side_effects"]),
    }


def _base_output(
    *,
    status: str,
    created: bool,
    blockers: list[str],
    write_candidates: list[dict[str, Any]],
    source_candidate_set: dict[str, Any] | None,
    source_candidate_count: int,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "evidence_layer_write_candidate_set_schema": EVIDENCE_LAYER_WRITE_CANDIDATE_SET_SCHEMA,
        "phase": PHASE,
        "evidence_layer_write_candidate_set_status": status,
        "created_at": _utc_now(),
        "input_source_kind": "controlled_production_evidence_import_candidate_set",
        "source_production_evidence_import_candidate_set_schema": _safe_source_value(
            source_candidate_set,
            "production_evidence_import_candidate_set_schema",
        ),
        "source_production_evidence_import_candidate_set_status": _safe_source_value(
            source_candidate_set,
            "production_evidence_import_candidate_set_status",
        ),
        "source_production_evidence_import_candidate_count": source_candidate_count,
        "source_evidence_layer_write_candidate_count": _source_evidence_layer_write_candidate_count(
            source_candidate_set
        ),
        "evidence_layer_write_candidate_mode": EVIDENCE_LAYER_WRITE_CANDIDATE_MODE,
        "evidence_layer_write_candidate_count": len(write_candidates),
        "warning_count": _source_warning_count(source_candidate_set),
        "human_review_required": True,
        "preview_only": True,
        "import_candidate_only": True,
        "production_import_candidate_only": True,
        "write_candidate_only": True,
        "evidence_layer_write_candidate_only": True,
        "evidence_layer_write_candidate_helper_implementation_approved": created,
        "evidence_layer_write_candidate_created": created,
        "production_evidence_import_candidate_created": False,
        "evidence_item_created": False,
        "evidence_items_created": False,
        "production_evidence_item_created": False,
        "evidence_layer_write": False,
        "review_queue_item_created": False,
        "production_review_queue_item_created": False,
        "production_case_created": False,
        "production_analysis_run_created": False,
        "route_ready": False,
        "frontend_ready": False,
        "production_ready": False,
        "public_ready": False,
        "customer_ready": False,
        "b_end_ready": False,
        "sandbox_ready": False,
        "public_event_ready": False,
        "evidence_layer_write_candidates": write_candidates,
        "blockers": _dedupe(blockers),
        "warnings": _dedupe(warnings or []),
        "runtime_side_effects": _runtime_side_effects(),
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {flag_name: False for flag_name in RUNTIME_SIDE_EFFECT_FLAGS}


def _approval_blockers(exact_approval_phrase: str | None) -> list[str]:
    if exact_approval_phrase is None or exact_approval_phrase == "":
        return ["blocked_missing_exact_approval"]
    if exact_approval_phrase != APPROVAL_PHRASE:
        return ["blocked_wrong_exact_approval"]
    return []


def _source_production_evidence_import_candidate_set_blockers(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> list[str]:
    if not isinstance(source_candidate_set, dict):
        return ["source_production_evidence_import_candidate_set_missing_or_not_object"]

    blockers: list[str] = []
    expected = {
        "production_evidence_import_candidate_set_schema": (
            SOURCE_PRODUCTION_EVIDENCE_IMPORT_CANDIDATE_SET_SCHEMA,
            "source_production_evidence_import_candidate_set_schema_wrong",
        ),
        "phase": (SOURCE_PHASE, "source_production_evidence_import_candidate_set_phase_wrong"),
        "production_evidence_import_candidate_set_status": (
            SOURCE_WARN_STATUS,
            "source_production_evidence_import_candidate_set_status_not_warn_manual_review",
        ),
    }
    for field, (expected_value, reason) in expected.items():
        if source_candidate_set.get(field) != expected_value:
            blockers.append(reason)

    true_fields = {
        "human_review_required": "source_human_review_required_not_true",
        "preview_only": "source_preview_only_not_true",
        "import_candidate_only": "source_import_candidate_only_not_true",
        "write_candidate_only": "source_write_candidate_only_not_true",
        "production_import_candidate_only": "source_production_import_candidate_only_not_true",
        "production_evidence_import_candidate_helper_implementation_approved": (
            "source_production_evidence_import_candidate_helper_not_approved"
        ),
        "production_evidence_import_candidate_created": (
            "source_production_evidence_import_candidate_created_not_true"
        ),
    }
    for field, reason in true_fields.items():
        if source_candidate_set.get(field) is not True:
            blockers.append(reason)

    if source_candidate_set.get("warning_count") != 1:
        blockers.append("source_warning_count_not_one")

    candidate_count = source_candidate_set.get("production_evidence_import_candidate_count")
    source_write_candidate_count = source_candidate_set.get("source_evidence_layer_write_candidate_count")
    if not isinstance(candidate_count, int) or isinstance(candidate_count, bool):
        blockers.append("source_production_evidence_import_candidate_count_missing_or_invalid")
    elif candidate_count != len(source_candidates):
        blockers.append("source_production_evidence_import_candidate_count_inconsistent")
    elif candidate_count < 1:
        blockers.append("source_production_evidence_import_candidates_missing")
    elif candidate_count > HARD_CANDIDATE_BOUND:
        blockers.append("source_production_evidence_import_candidate_count_too_high")

    if not isinstance(source_write_candidate_count, int) or isinstance(source_write_candidate_count, bool):
        blockers.append("source_evidence_layer_write_candidate_count_missing_or_invalid")
    elif isinstance(candidate_count, int) and not isinstance(candidate_count, bool):
        if source_write_candidate_count < candidate_count:
            blockers.append(
                "source_evidence_layer_write_candidate_count_less_than_production_evidence_import_candidate_count"
            )
        if source_write_candidate_count > HARD_CANDIDATE_BOUND:
            blockers.append("source_evidence_layer_write_candidate_count_too_high")

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
        blockers.append("blocked_candidate_limit_exceeds_source_production_evidence_import_candidate_count")
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


def _build_write_candidates(
    source_candidates: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    write_candidates: list[dict[str, Any]] = []
    blockers: list[str] = []
    for index, source_candidate in enumerate(source_candidates, start=1):
        candidate_blockers = _source_production_evidence_import_candidate_blockers(source_candidate)
        if candidate_blockers:
            blockers.extend(candidate_blockers)
            continue
        write_candidates.append(_write_candidate_from_source(source_candidate, index=index))
    return write_candidates, _dedupe(blockers)


def _source_production_evidence_import_candidate_blockers(source_candidate: dict[str, Any]) -> list[str]:
    if not isinstance(source_candidate, dict):
        return ["source_production_evidence_import_candidate_not_object"]
    blockers: list[str] = []
    for field in source_candidate:
        if field in FORBIDDEN_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS:
            blockers.append(f"forbidden_source_production_evidence_import_candidate_field:{field}")
    for field in REQUIRED_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS:
        value = source_candidate.get(field)
        if value is None or value == "":
            blockers.append(f"source_production_evidence_import_candidate_missing_required_field:{field}")
    if (
        source_candidate.get("production_evidence_import_candidate_schema")
        != SOURCE_PRODUCTION_EVIDENCE_IMPORT_CANDIDATE_SCHEMA
    ):
        blockers.append("source_production_evidence_import_candidate_schema_wrong")
    if source_candidate.get("human_review_required") is not True:
        blockers.append("source_production_evidence_import_candidate_human_review_required_not_true")
    if source_candidate.get("preview_only") is not True:
        blockers.append("source_production_evidence_import_candidate_preview_only_not_true")
    if source_candidate.get("import_candidate_only") is not True:
        blockers.append("source_production_evidence_import_candidate_import_candidate_only_not_true")
    if source_candidate.get("write_candidate_only") is not True:
        blockers.append("source_production_evidence_import_candidate_write_candidate_only_not_true")
    if source_candidate.get("production_import_candidate_only") is not True:
        blockers.append("source_production_evidence_import_candidate_production_import_candidate_only_not_true")

    boundary_flags = source_candidate.get("boundary_flags")
    if not isinstance(boundary_flags, dict):
        blockers.append("source_production_evidence_import_candidate_boundary_flags_missing_or_invalid")
    else:
        required_true_flags = {
            "preview_only": "source_production_evidence_import_candidate_boundary_preview_only_not_true",
            "human_review_required": (
                "source_production_evidence_import_candidate_boundary_human_review_required_not_true"
            ),
            "import_candidate_only": (
                "source_production_evidence_import_candidate_boundary_import_candidate_only_not_true"
            ),
            "write_candidate_only": (
                "source_production_evidence_import_candidate_boundary_write_candidate_only_not_true"
            ),
            "production_import_candidate_only": (
                "source_production_evidence_import_candidate_boundary_production_import_candidate_only_not_true"
            ),
            "not_evidence_item": "source_production_evidence_import_candidate_boundary_not_evidence_item_not_true",
            "not_production_evidence_item": (
                "source_production_evidence_import_candidate_boundary_not_production_evidence_item_not_true"
            ),
            "no_evidence_layer_write": (
                "source_production_evidence_import_candidate_boundary_no_evidence_layer_write_not_true"
            ),
            "not_review_queue_item": (
                "source_production_evidence_import_candidate_boundary_not_review_queue_item_not_true"
            ),
            "not_production_review_queue_item": (
                "source_production_evidence_import_candidate_boundary_not_production_review_queue_item_not_true"
            ),
            "not_production_case": (
                "source_production_evidence_import_candidate_boundary_not_production_case_not_true"
            ),
            "not_production_analysis_run": (
                "source_production_evidence_import_candidate_boundary_not_production_analysis_run_not_true"
            ),
        }
        for flag, reason in required_true_flags.items():
            if boundary_flags.get(flag) is not True:
                blockers.append(reason)

    safe_fields = [
        *REQUIRED_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS,
        *OPTIONAL_SAFE_SOURCE_PRODUCTION_IMPORT_CANDIDATE_FIELDS,
        "redaction_warnings",
        "warning_labels",
        "production_import_readiness_blockers",
        "blocker_codes",
    ]
    for field in safe_fields:
        value = source_candidate.get(field)
        if _contains_forbidden_value(value):
            blockers.append(f"source_production_evidence_import_candidate_forbidden_value:{field}")
    return _dedupe(blockers)


def _write_candidate_from_source(source_candidate: dict[str, Any], *, index: int) -> dict[str, Any]:
    evidence_hash = _safe_token(source_candidate.get("evidence_id_hash"))
    source_production_import_candidate_id = _safe_token(
        source_candidate.get("production_evidence_import_candidate_id")
    )
    source_write_candidate_id = _safe_token(source_candidate.get("source_evidence_layer_write_candidate_id"))
    source_import_candidate_id = _safe_token(source_candidate.get("source_evidence_layer_import_candidate_id"))
    source_review_queue_candidate_id = _safe_token(source_candidate.get("source_review_queue_candidate_id"))
    source_evidence_candidate_id = _safe_token(source_candidate.get("source_evidence_candidate_id"))
    return {
        "evidence_layer_write_candidate_schema": EVIDENCE_LAYER_WRITE_CANDIDATE_SCHEMA,
        "evidence_layer_write_candidate_id": (
            f"evidence-layer-write-candidate-from-production-import-{index:03d}-{evidence_hash}"
        ),
        "source_production_evidence_import_candidate_id": source_production_import_candidate_id,
        "source_evidence_layer_write_candidate_id": source_write_candidate_id,
        "source_evidence_layer_import_candidate_id": source_import_candidate_id,
        "source_review_queue_candidate_id": source_review_queue_candidate_id,
        "source_evidence_candidate_id": source_evidence_candidate_id,
        "evidence_id_hash": evidence_hash,
        "preview_hash": _safe_token(source_candidate.get("preview_hash") or source_candidate.get("evidence_id_hash")),
        "platform": _safe_label(source_candidate.get("platform")),
        "evidence_type": _safe_label(source_candidate.get("evidence_type")),
        "coarse_created_at": _safe_date(source_candidate.get("coarse_created_at") or source_candidate.get("created_at_date")),
        "source_url_present": source_candidate.get("source_url_present") is True,
        "trust_boundary_label": _safe_label(source_candidate.get("trust_boundary_label")) or "manual_review_required",
        "verification_status": _safe_label(source_candidate.get("verification_status")),
        "review_status": _safe_label(source_candidate.get("review_status")),
        "trust_label": _safe_label(source_candidate.get("trust_label")) or "medium_low",
        "title_or_label_redacted": _safe_snippet(source_candidate.get("title_or_label_redacted"))
        or _safe_label(source_candidate.get("evidence_type")),
        "text_snippet_redacted": _safe_snippet(source_candidate.get("text_snippet_redacted")),
        "redaction_status": _safe_label(source_candidate.get("redaction_status")) or "redacted",
        "redaction_warnings": _safe_string_list(source_candidate.get("redaction_warnings")),
        "warning_labels": _safe_string_list(source_candidate.get("warning_labels")) or [
            "manual_review_required",
            "selected_sample_only",
        ],
        "evidence_layer_write_readiness_blockers": [
            "human_review_required",
            "not_evidence_item",
            "no_evidence_layer_write",
        ],
        "blocker_codes": _safe_string_list(source_candidate.get("blocker_codes")),
        "human_review_required": True,
        "preview_only": True,
        "import_candidate_only": True,
        "production_import_candidate_only": True,
        "write_candidate_only": True,
        "evidence_layer_write_candidate_only": True,
        "boundary_flags": {
            "preview_only": True,
            "human_review_required": True,
            "import_candidate_only": True,
            "production_import_candidate_only": True,
            "write_candidate_only": True,
            "evidence_layer_write_candidate_only": True,
            "not_evidence_item": True,
            "not_production_evidence_item": True,
            "no_evidence_layer_write": True,
            "not_review_queue_item": True,
            "not_production_review_queue_item": True,
            "not_production_case": True,
            "not_production_analysis_run": True,
            "not_analysis_ready": True,
            "not_report_ready": True,
            "no_review_action": True,
            "no_review_audit_timeline": True,
            "no_reviewer_assignment": True,
            "not_official_verification": True,
            "not_full_web": True,
            "not_full_platform": True,
            "not_causal_proof": True,
        },
    }


def _write_candidate_warnings(source_candidate_set: dict[str, Any] | None) -> list[str]:
    warnings = ["manual_review_required", "selected_sample_only"]
    if isinstance(source_candidate_set, dict):
        source_warnings = source_candidate_set.get("warnings")
        if isinstance(source_warnings, list):
            warnings.extend(item for item in source_warnings if isinstance(item, str))
    return _dedupe(warnings)


def _safe_source_candidates(source_candidate_set: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(source_candidate_set, dict):
        return []
    candidates = source_candidate_set.get("production_evidence_import_candidates")
    if not isinstance(candidates, list):
        return []
    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def _source_production_evidence_import_candidate_count(
    source_candidate_set: dict[str, Any] | None,
    source_candidates: list[dict[str, Any]],
) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("production_evidence_import_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return len(source_candidates)


def _source_evidence_layer_write_candidate_count(source_candidate_set: dict[str, Any] | None) -> int:
    if isinstance(source_candidate_set, dict):
        count = source_candidate_set.get("source_evidence_layer_write_candidate_count")
        if isinstance(count, int) and not isinstance(count, bool):
            return count
    return 0


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
        return "blocked_invalid_source_production_evidence_import_candidate_set"
    first = blockers[0]
    if first in {"blocked_missing_exact_approval", "blocked_wrong_exact_approval"}:
        return first
    if first.startswith("requested_action_blocked"):
        return "blocked_source_boundary_violation"
    if first.startswith("blocked_candidate_limit"):
        return "blocked_candidate_limit_violation"
    if first.startswith("forbidden_source_production_evidence_import_candidate_field") or first.startswith(
        "source_production_evidence_import_candidate_forbidden_value"
    ):
        return "blocked_forbidden_field_detected"
    if first.startswith("source_production_evidence_import_candidate_set") or first.startswith(
        "source_production_evidence_import_candidate_count"
    ):
        return "blocked_invalid_source_production_evidence_import_candidate_set"
    if first.startswith("source_production_evidence_import_candidate") or first == (
        "source_production_evidence_import_candidate_not_object"
    ):
        return "blocked_invalid_source_production_evidence_import_candidate_set"
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
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", text)[:80]


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
