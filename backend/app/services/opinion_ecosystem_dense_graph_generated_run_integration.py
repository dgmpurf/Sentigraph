from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services import opinion_ecosystem_dense_graph_generated_run_adapter as adapter
from app.services import opinion_ecosystem_minimum_real_run as minimum_real_run


INTEGRATION_SCHEMA = "sentigraph_opinion_ecosystem_generated_run_dense_graph_integration_v0_1"
INTEGRATION_STATUS_READY = "ready_for_backend_service_surface"
INTEGRATION_STATUS_DEGRADED = "degraded_dense_graph_attachment"
VISUALIZATION_MODE = "dense_sandbox_proxy_graph"

REQUIRED_BOUNDARY_FLAGS = {
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "no_auto_execute",
    "no_generated_public_response",
    "anonymous_aggregate_only",
    "human_review_required",
}

REQUIRED_SIDE_EFFECT_FLAGS = {
    "called_real_api",
    "called_real_llm",
    "ran_collector",
    "accessed_private_collector",
    "read_real_exchange_dir",
    "fetched_url",
    "scraped_page",
    "wrote_evidence_layer",
    "created_production_case",
    "created_analysis_run",
    "generated_b_end_report_runtime",
    "generated_sandbox_runtime",
    "generated_public_event_runtime",
    "generated_response_text",
    "published_or_sent",
    "auto_executed",
}

FORBIDDEN_ACTIVE_FIELDS = {
    "raw_author_id",
    "author_id",
    "author_name",
    "profile_url",
    "username",
    "account_id",
    "cookie",
    "session",
    "token",
    "browser_profile_path",
    "private_message",
    "response_text",
    "generated_response_text",
    "generated_public_message",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
}


def generate_opinion_ecosystem_run_with_dense_graph_attachment(
    fixture_or_sample: dict[str, Any],
    *,
    sample_id: str,
    source_run_id: str | None = None,
    include_dense_graph: bool = True,
    max_people_clusters: int = 240,
    max_edges: int = 800,
) -> dict[str, Any]:
    preflight_scan = _scan_for_forbidden_fields(fixture_or_sample)
    if preflight_scan["privacy_stop"]:
        return _blocked_integration(
            sample_id=sample_id,
            source_run_id=source_run_id,
            reason="forbidden_active_field_present",
            privacy_scan=preflight_scan,
        )

    base_generated_run = minimum_real_run.generate_opinion_ecosystem_minimum_real_run(fixture_or_sample)
    resolved_source_run_id = str(source_run_id or base_generated_run.get("run_id") or "missing_source_run_id")
    base_warnings = _safe_string_list(base_generated_run.get("warnings"))
    base_blockers = _safe_blockers(base_generated_run.get("blockers"))

    dense_graph_attachment: dict[str, Any] | None = None
    if include_dense_graph:
        dense_graph_attachment = adapter.build_dense_graph_generated_run_attachment_from_evidence_items(
            _safe_evidence_items(fixture_or_sample),
            sample_id=sample_id,
            source_run_id=resolved_source_run_id,
            max_people_clusters=max_people_clusters,
            max_edges=max_edges,
        )
        if dense_graph_attachment.get("attachment_status") == "blocked":
            return _blocked_integration(
                sample_id=sample_id,
                source_run_id=resolved_source_run_id,
                reason="dense_graph_attachment_blocked",
                privacy_scan=_safe_privacy_scan(dense_graph_attachment.get("privacy_scan")),
            )

    boundary_flags, missing_base_boundary_flags = _boundary_flags(
        base_generated_run.get("boundary_flags"),
        dense_graph_attachment.get("boundary_flags") if dense_graph_attachment else None,
    )
    runtime_side_effects, unsafe_side_effects = _runtime_side_effects(
        base_generated_run.get("runtime_side_effects"),
        dense_graph_attachment.get("runtime_side_effects") if dense_graph_attachment else None,
    )
    if unsafe_side_effects:
        return _blocked_integration(
            sample_id=sample_id,
            source_run_id=resolved_source_run_id,
            reason="runtime_side_effect_flag_not_false",
            privacy_scan=_empty_privacy_scan(),
        )

    warnings = [*base_warnings]
    if missing_base_boundary_flags:
        warnings.append("missing_base_boundary_flags")
    attachment_status = dense_graph_attachment.get("attachment_status") if dense_graph_attachment else None
    if attachment_status == "degraded_missing_boundary_flags":
        warnings.extend(_safe_string_list(dense_graph_attachment.get("warnings")))
        integration_status = INTEGRATION_STATUS_DEGRADED
    elif base_blockers:
        integration_status = "blocked"
    else:
        integration_status = INTEGRATION_STATUS_READY

    integration = {
        "integration_schema": INTEGRATION_SCHEMA,
        "integration_status": integration_status,
        "sample_id": str(sample_id),
        "source_run_id": resolved_source_run_id,
        "created_at": _utc_timestamp(),
        "base_generated_run": base_generated_run,
        "dense_graph_attachment": dense_graph_attachment,
        "integration_summary": _integration_summary(dense_graph_attachment),
        "boundary_flags": boundary_flags,
        "runtime_side_effects": runtime_side_effects,
        "warnings": _dedupe_strings(warnings),
        "blockers": base_blockers if integration_status == "blocked" else [],
        "privacy_scan": _empty_privacy_scan(),
        "human_review_required": True,
    }

    output_scan = _scan_for_forbidden_fields(integration)
    if output_scan["privacy_stop"]:
        return _blocked_integration(
            sample_id=sample_id,
            source_run_id=resolved_source_run_id,
            reason="forbidden_field_in_integrated_output",
            privacy_scan=output_scan,
        )
    return integration


def _blocked_integration(
    *,
    sample_id: str,
    source_run_id: str | None,
    reason: str,
    privacy_scan: dict[str, Any],
) -> dict[str, Any]:
    return {
        "integration_schema": INTEGRATION_SCHEMA,
        "integration_status": "blocked",
        "sample_id": str(sample_id),
        "source_run_id": source_run_id,
        "created_at": _utc_timestamp(),
        "base_generated_run": None,
        "dense_graph_attachment": None,
        "integration_summary": _integration_summary(None),
        "boundary_flags": _required_boundary_defaults(),
        "runtime_side_effects": _required_side_effect_defaults(),
        "warnings": ["dense_graph_generated_run_integration_blocked"],
        "blockers": [{"reason": reason, "category": "dense_graph_generated_run_integration_blocker"}],
        "privacy_scan": privacy_scan,
        "human_review_required": True,
    }


def _integration_summary(dense_graph_attachment: dict[str, Any] | None) -> dict[str, Any]:
    if not dense_graph_attachment:
        return {
            "dense_graph_attached": False,
            "people_cluster_proxy_count": 0,
            "influence_core_proxy_count": 0,
            "content_aggregate_proxy_count": 0,
            "echobox_proxy_count": 0,
            "edge_count": 0,
            "timeline_bucket_count": 0,
            "recommended_visualization_mode": VISUALIZATION_MODE,
            "frontend_ready": False,
            "route_ready": False,
            "production_ready": False,
        }
    return {
        "dense_graph_attached": True,
        "people_cluster_proxy_count": _safe_int(dense_graph_attachment.get("people_cluster_proxy_count")),
        "influence_core_proxy_count": _safe_int(dense_graph_attachment.get("influence_core_proxy_count")),
        "content_aggregate_proxy_count": _safe_int(dense_graph_attachment.get("content_aggregate_proxy_count")),
        "echobox_proxy_count": _safe_int(dense_graph_attachment.get("echobox_proxy_count")),
        "edge_count": _safe_int(dense_graph_attachment.get("edge_count")),
        "timeline_bucket_count": _safe_int(dense_graph_attachment.get("timeline_bucket_count")),
        "recommended_visualization_mode": str(
            dense_graph_attachment.get("recommended_visualization_mode") or VISUALIZATION_MODE
        ),
        "frontend_ready": False,
        "route_ready": False,
        "production_ready": False,
    }


def _safe_evidence_items(fixture_or_sample: dict[str, Any]) -> list[dict[str, Any]]:
    value = fixture_or_sample.get("evidence_items_safe")
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _boundary_flags(base_value: Any, dense_value: Any) -> tuple[dict[str, bool], set[str]]:
    base_flags = base_value if isinstance(base_value, dict) else {}
    dense_flags = dense_value if isinstance(dense_value, dict) else {}
    resolved = _required_boundary_defaults()
    for flag in REQUIRED_BOUNDARY_FLAGS:
        resolved[flag] = bool(base_flags.get(flag, dense_flags.get(flag, True)))
    missing_base = {
        flag
        for flag in {
            "selected_sample_only",
            "not_full_web",
            "not_full_platform",
            "not_full_thread",
            "not_official_verification",
            "not_causal_proof",
            "not_prediction",
            "not_production_score",
            "no_auto_execute",
            "no_generated_public_response",
            "human_review_required",
        }
        if flag not in base_flags
    }
    return resolved, missing_base


def _runtime_side_effects(base_value: Any, dense_value: Any) -> tuple[dict[str, bool], set[str]]:
    base_flags = base_value if isinstance(base_value, dict) else {}
    dense_flags = dense_value if isinstance(dense_value, dict) else {}
    resolved = _required_side_effect_defaults()
    unsafe = set()
    for flag in REQUIRED_SIDE_EFFECT_FLAGS:
        resolved[flag] = bool(base_flags.get(flag, dense_flags.get(flag, False)))
        if resolved[flag] is not False:
            unsafe.add(flag)
    return resolved, unsafe


def _scan_for_forbidden_fields(value: Any) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    raw_identifier_found = False
    secret_like_found = False
    for path, field in _iter_fields(value):
        normalized_field = field.strip().lower()
        if _is_allowed_runtime_side_effect_flag(path, normalized_field):
            continue
        if normalized_field in FORBIDDEN_ACTIVE_FIELDS:
            raw_identifier_found = raw_identifier_found or normalized_field in {
                "raw_author_id",
                "author_id",
                "author_name",
                "profile_url",
                "username",
                "account_id",
            }
            secret_like_found = secret_like_found or normalized_field in {
                "cookie",
                "session",
                "token",
                "browser_profile_path",
            }
            blockers.append({"path_ref": _path_ref(path), "reason": "forbidden_active_field_present"})
    return {
        "raw_identifier_found": raw_identifier_found,
        "secret_like_found": secret_like_found,
        "privacy_stop": bool(blockers),
        "blocked_field_count": len(blockers),
        "blockers": blockers,
    }


def _iter_fields(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}" if path else key_text
            yield child_path, key_text
            yield from _iter_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            yield from _iter_fields(child, child_path)


def _is_allowed_runtime_side_effect_flag(path: str, normalized_field: str) -> bool:
    return path.endswith(f"runtime_side_effects.{normalized_field}") and normalized_field in REQUIRED_SIDE_EFFECT_FLAGS


def _path_ref(path: str) -> str:
    return f"path_hash_{abs(hash(path)) % 1_000_000:06d}"


def _required_boundary_defaults() -> dict[str, bool]:
    return {flag: True for flag in sorted(REQUIRED_BOUNDARY_FLAGS)}


def _required_side_effect_defaults() -> dict[str, bool]:
    return {flag: False for flag in sorted(REQUIRED_SIDE_EFFECT_FLAGS)}


def _safe_privacy_scan(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return _empty_privacy_scan()
    return {
        "raw_identifier_found": bool(value.get("raw_identifier_found")),
        "secret_like_found": bool(value.get("secret_like_found")),
        "privacy_stop": bool(value.get("privacy_stop")),
        "blocked_field_count": _safe_int(value.get("blocked_field_count")),
        "blockers": _safe_blockers(value.get("blockers")),
    }


def _empty_privacy_scan() -> dict[str, Any]:
    return {
        "raw_identifier_found": False,
        "secret_like_found": False,
        "privacy_stop": False,
        "blocked_field_count": 0,
        "blockers": [],
    }


def _safe_blockers(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    blockers: list[dict[str, str]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            continue
        blockers.append(
            {
                "item_ref": f"blocker_{index}",
                "reason": str(item.get("reason") or "blocked"),
                "category": str(item.get("category") or "integration_blocker"),
            }
        )
    return blockers


def _safe_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _dedupe_strings(values: list[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        if value and value not in deduped:
            deduped.append(value)
    return deduped


def _safe_int(value: Any) -> int:
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return 0


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
