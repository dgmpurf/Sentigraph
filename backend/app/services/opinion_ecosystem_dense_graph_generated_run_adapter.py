from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services import opinion_ecosystem_dense_graph_builder as dense_builder


ATTACHMENT_SCHEMA = "sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1"
ATTACHMENT_STATUS_READY = "ready_for_backend_generated_run_surface"
ATTACHMENT_STATUS_DEGRADED = "degraded_missing_boundary_flags"
DENSE_GRAPH_SCHEMA = "sentigraph_opinion_ecosystem_dense_graph_run_v0_1"
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

NODE_PREVIEW_KEYS = {
    "node_id",
    "node_type",
    "stance_label",
    "platform_hint",
    "source_type_hint",
    "activity_level",
    "emotion_intensity",
    "attention_level",
    "fatigue_level",
    "confidence",
    "visual_weight",
    "time_bucket",
    "boundary_note",
    "core_label",
    "aggregate_label",
}

EDGE_PREVIEW_KEYS = {
    "edge_id",
    "source",
    "target",
    "edge_type",
    "weight",
    "confidence",
    "boundary_note",
}


def build_dense_graph_generated_run_attachment(
    *,
    dense_graph_run: dict[str, Any],
    source_run_id: str | None = None,
    sample_id: str | None = None,
    suggested_max_render_nodes: int = 240,
    suggested_max_render_edges: int = 800,
) -> dict[str, Any]:
    privacy_scan = _scan_for_forbidden_fields(dense_graph_run)
    resolved_sample_id = str(sample_id or dense_graph_run.get("sample_id") or "missing_sample_id")
    base_warnings = _safe_string_list(dense_graph_run.get("warnings"))

    if privacy_scan["privacy_stop"]:
        return _blocked_attachment(
            sample_id=resolved_sample_id,
            source_run_id=source_run_id,
            reason="forbidden_active_field_present",
            warnings=base_warnings,
            privacy_scan=privacy_scan,
        )

    if dense_graph_run.get("run_schema") != DENSE_GRAPH_SCHEMA:
        return _blocked_attachment(
            sample_id=resolved_sample_id,
            source_run_id=source_run_id,
            reason="invalid_dense_graph_run_schema",
            warnings=base_warnings,
            privacy_scan=privacy_scan,
        )

    graph = dense_graph_run.get("graph")
    if not isinstance(graph, dict):
        return _blocked_attachment(
            sample_id=resolved_sample_id,
            source_run_id=source_run_id,
            reason="missing_dense_graph_payload",
            warnings=base_warnings,
            privacy_scan=privacy_scan,
        )

    boundary_flags, missing_boundary_flags = _boundary_flags(dense_graph_run.get("boundary_flags"))
    runtime_side_effects, unsafe_side_effects = _runtime_side_effects(dense_graph_run.get("runtime_side_effects"))
    if unsafe_side_effects:
        return _blocked_attachment(
            sample_id=resolved_sample_id,
            source_run_id=source_run_id,
            reason="runtime_side_effect_flag_not_false",
            warnings=base_warnings,
            privacy_scan=privacy_scan,
        )

    warnings = [*base_warnings]
    attachment_status = ATTACHMENT_STATUS_READY
    if missing_boundary_flags:
        warnings.append("missing_boundary_flags")
        attachment_status = ATTACHMENT_STATUS_DEGRADED

    nodes = _dict_list(graph.get("nodes"))
    edges = _dict_list(graph.get("edges"))
    timeline_buckets = _dict_list(graph.get("timeline_buckets"))
    graph_summary = _graph_summary(graph.get("graph_summary"), nodes, edges, timeline_buckets)

    return {
        "attachment_schema": ATTACHMENT_SCHEMA,
        "attachment_status": attachment_status,
        "source_run_id": source_run_id,
        "sample_id": resolved_sample_id,
        "created_at": _utc_timestamp(),
        "graph_schema": DENSE_GRAPH_SCHEMA,
        "graph_summary": graph_summary,
        "people_cluster_proxy_count": graph_summary["people_cluster_proxy_count"],
        "influence_core_proxy_count": graph_summary["influence_core_proxy_count"],
        "content_aggregate_proxy_count": graph_summary["content_aggregate_proxy_count"],
        "echobox_proxy_count": graph_summary["echobox_proxy_count"],
        "edge_count": graph_summary["edge_count"],
        "timeline_bucket_count": graph_summary["timeline_bucket_count"],
        "nodes_preview": [_safe_node_preview(node) for node in nodes[:suggested_max_render_nodes]],
        "edges_preview": [_safe_edge_preview(edge) for edge in edges[:suggested_max_render_edges]],
        "timeline_buckets": [_safe_timeline_bucket(bucket) for bucket in timeline_buckets],
        "recommended_visualization_mode": VISUALIZATION_MODE,
        "suggested_max_render_nodes": int(max(0, suggested_max_render_nodes)),
        "suggested_max_render_edges": int(max(0, suggested_max_render_edges)),
        "density_note": str(
            graph_summary.get("density_note")
            or "anonymous_proxy_density_for_future_visualization_not_population_count"
        ),
        "boundary_flags": boundary_flags,
        "runtime_side_effects": runtime_side_effects,
        "warnings": _dedupe_strings(warnings),
        "blockers": [],
        "privacy_scan": privacy_scan,
        "human_review_required": True,
    }


def build_dense_graph_generated_run_attachment_from_evidence_items(
    evidence_items: list[dict[str, Any]],
    *,
    sample_id: str,
    source_run_id: str | None = None,
    max_people_clusters: int = 240,
    max_edges: int = 800,
    suggested_max_render_nodes: int = 240,
    suggested_max_render_edges: int = 800,
) -> dict[str, Any]:
    dense_graph_run = dense_builder.build_dense_opinion_graph_from_evidence_items(
        evidence_items,
        sample_id=sample_id,
        max_people_clusters=max_people_clusters,
        max_edges=max_edges,
    )
    return build_dense_graph_generated_run_attachment(
        dense_graph_run=dense_graph_run,
        source_run_id=source_run_id,
        sample_id=sample_id,
        suggested_max_render_nodes=suggested_max_render_nodes,
        suggested_max_render_edges=suggested_max_render_edges,
    )


def _blocked_attachment(
    *,
    sample_id: str,
    source_run_id: str | None,
    reason: str,
    warnings: list[str],
    privacy_scan: dict[str, Any],
) -> dict[str, Any]:
    return {
        "attachment_schema": ATTACHMENT_SCHEMA,
        "attachment_status": "blocked",
        "source_run_id": source_run_id,
        "sample_id": sample_id,
        "created_at": _utc_timestamp(),
        "graph_schema": DENSE_GRAPH_SCHEMA,
        "graph_summary": _empty_graph_summary(),
        "people_cluster_proxy_count": 0,
        "influence_core_proxy_count": 0,
        "content_aggregate_proxy_count": 0,
        "echobox_proxy_count": 0,
        "edge_count": 0,
        "timeline_bucket_count": 0,
        "nodes_preview": [],
        "edges_preview": [],
        "timeline_buckets": [],
        "recommended_visualization_mode": VISUALIZATION_MODE,
        "suggested_max_render_nodes": 0,
        "suggested_max_render_edges": 0,
        "density_note": "blocked_attachment_no_visualization_density",
        "boundary_flags": _required_boundary_defaults(),
        "runtime_side_effects": _required_side_effect_defaults(),
        "warnings": _dedupe_strings([*warnings, "dense_graph_attachment_blocked"]),
        "blockers": [{"reason": reason, "category": "dense_graph_attachment_blocker"}],
        "privacy_scan": privacy_scan,
        "human_review_required": True,
    }


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
            blockers.append(
                {
                    "path_ref": _path_ref(path),
                    "reason": "forbidden_active_field_present",
                }
            )
    return {
        "raw_identifier_found": raw_identifier_found,
        "secret_like_found": secret_like_found,
        "privacy_stop": bool(blockers),
        "blocked_field_count": len(blockers),
        "blockers": blockers,
    }


def _is_allowed_runtime_side_effect_flag(path: str, normalized_field: str) -> bool:
    return path == f"runtime_side_effects.{normalized_field}" and normalized_field in REQUIRED_SIDE_EFFECT_FLAGS


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


def _path_ref(path: str) -> str:
    return f"path_hash_{abs(hash(path)) % 1_000_000:06d}"


def _boundary_flags(value: Any) -> tuple[dict[str, bool], set[str]]:
    flags = value if isinstance(value, dict) else {}
    resolved = _required_boundary_defaults()
    for flag in REQUIRED_BOUNDARY_FLAGS:
        resolved[flag] = bool(flags.get(flag, True))
    missing = {flag for flag in REQUIRED_BOUNDARY_FLAGS if flag not in flags}
    return resolved, missing


def _runtime_side_effects(value: Any) -> tuple[dict[str, bool], set[str]]:
    flags = value if isinstance(value, dict) else {}
    resolved = _required_side_effect_defaults()
    unsafe = set()
    for flag in REQUIRED_SIDE_EFFECT_FLAGS:
        resolved[flag] = bool(flags.get(flag, False))
        if resolved[flag] is not False:
            unsafe.add(flag)
    return resolved, unsafe


def _required_boundary_defaults() -> dict[str, bool]:
    return {flag: True for flag in sorted(REQUIRED_BOUNDARY_FLAGS)}


def _required_side_effect_defaults() -> dict[str, bool]:
    return {flag: False for flag in sorted(REQUIRED_SIDE_EFFECT_FLAGS)}


def _graph_summary(value: Any, nodes: list[dict[str, Any]], edges: list[dict[str, Any]], timeline_buckets: list[dict[str, Any]]) -> dict[str, Any]:
    summary = value.copy() if isinstance(value, dict) else {}
    node_type_counts = {
        "people_cluster_proxy": 0,
        "influence_core_proxy": 0,
        "content_aggregate_proxy": 0,
        "echobox_proxy": 0,
    }
    for node in nodes:
        node_type = str(node.get("node_type") or "")
        if node_type in node_type_counts:
            node_type_counts[node_type] += 1
    summary.setdefault("people_cluster_proxy_count", node_type_counts["people_cluster_proxy"])
    summary.setdefault("influence_core_proxy_count", node_type_counts["influence_core_proxy"])
    summary.setdefault("content_aggregate_proxy_count", node_type_counts["content_aggregate_proxy"])
    summary.setdefault("echobox_proxy_count", node_type_counts["echobox_proxy"])
    summary.setdefault("edge_count", len(edges))
    summary.setdefault("timeline_bucket_count", len(timeline_buckets))
    summary.setdefault("density_note", "anonymous_proxy_density_for_future_visualization_not_population_count")
    return {
        "raw_evidence_count": _safe_int(summary.get("raw_evidence_count")),
        "eligible_evidence_count": _safe_int(summary.get("eligible_evidence_count")),
        "rejected_excluded_count": _safe_int(summary.get("rejected_excluded_count")),
        "duplicate_folded_count": _safe_int(summary.get("duplicate_folded_count")),
        "people_cluster_proxy_count": _safe_int(summary.get("people_cluster_proxy_count")),
        "influence_core_proxy_count": _safe_int(summary.get("influence_core_proxy_count")),
        "content_aggregate_proxy_count": _safe_int(summary.get("content_aggregate_proxy_count")),
        "echobox_proxy_count": _safe_int(summary.get("echobox_proxy_count")),
        "edge_count": _safe_int(summary.get("edge_count")),
        "timeline_bucket_count": _safe_int(summary.get("timeline_bucket_count")),
        "density_note": str(summary.get("density_note")),
    }


def _empty_graph_summary() -> dict[str, Any]:
    return {
        "raw_evidence_count": 0,
        "eligible_evidence_count": 0,
        "rejected_excluded_count": 0,
        "duplicate_folded_count": 0,
        "people_cluster_proxy_count": 0,
        "influence_core_proxy_count": 0,
        "content_aggregate_proxy_count": 0,
        "echobox_proxy_count": 0,
        "edge_count": 0,
        "timeline_bucket_count": 0,
        "density_note": "blocked_attachment_no_visualization_density",
    }


def _safe_node_preview(node: dict[str, Any]) -> dict[str, Any]:
    return {key: node[key] for key in NODE_PREVIEW_KEYS if key in node}


def _safe_edge_preview(edge: dict[str, Any]) -> dict[str, Any]:
    return {key: edge[key] for key in EDGE_PREVIEW_KEYS if key in edge}


def _safe_timeline_bucket(bucket: dict[str, Any]) -> dict[str, Any]:
    allowed = {"bucket_id", "bucket_label", "evidence_count", "boundary_note"}
    return {key: bucket[key] for key in allowed if key in bucket}


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


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
