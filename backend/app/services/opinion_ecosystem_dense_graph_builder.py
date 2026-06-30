from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


RUN_SCHEMA = "sentigraph_opinion_ecosystem_dense_graph_run_v0_1"
RUN_STATUS = "generated_local_dense_graph"
MODEL_VERSION = "0.1"
COEFFICIENT_SOURCE = "mock_default"
CALIBRATION_STATUS = "uncalibrated"
EMPIRICAL_VALIDATION = "not_started"
INPUT_SCOPE_NOTE = "selected_sample_only_controlled_local_evidence"
REPO_ROOT = Path(__file__).resolve().parents[3]

STANCE_LABELS = {"support", "neutral", "oppose", "mixed", "unknown"}
REJECTED_REVIEW_STATUSES = {"rejected", "human_rejected"}
FORBIDDEN_ACTIVE_FIELDS = {
    "raw_author_id",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "response_text",
    "generated_public_message",
    "auto_execute",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}


def build_dense_opinion_graph_from_evidence_items(
    evidence_items: list[dict],
    *,
    sample_id: str,
    max_people_clusters: int = 240,
    max_edges: int = 800,
) -> dict[str, Any]:
    privacy_scan = _scan_for_forbidden_fields(evidence_items)
    if privacy_scan["privacy_stop"]:
        return _blocked_run(sample_id, privacy_scan)

    eligible_items = _deduplicate_eligible_evidence(evidence_items)
    timeline_buckets = _build_timeline_buckets(eligible_items)
    people_nodes = _build_people_cluster_proxy_nodes(eligible_items, timeline_buckets, max_people_clusters)
    influence_nodes = _build_influence_core_proxy_nodes(eligible_items)
    content_nodes = _build_content_aggregate_proxy_nodes(eligible_items)
    echobox_nodes = _build_echobox_proxy_nodes(eligible_items)
    nodes = [*content_nodes, *influence_nodes, *echobox_nodes, *people_nodes]
    edges = _build_edges(
        people_nodes=people_nodes,
        influence_nodes=influence_nodes,
        content_nodes=content_nodes,
        echobox_nodes=echobox_nodes,
        max_edges=max_edges,
    )
    graph_summary = _graph_summary(
        evidence_items=evidence_items,
        eligible_items=eligible_items,
        nodes=nodes,
        edges=edges,
        timeline_buckets=timeline_buckets,
    )

    return {
        "run_schema": RUN_SCHEMA,
        "run_status": RUN_STATUS,
        "sample_id": str(sample_id),
        "input_scope_note": INPUT_SCOPE_NOTE,
        "generated_at": _generated_at(),
        "model_version": MODEL_VERSION,
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "human_review_required": True,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": _warnings(evidence_items, eligible_items),
        "blockers": [],
        "privacy_scan": privacy_scan,
        "graph": {
            "nodes": nodes,
            "edges": edges,
            "timeline_buckets": timeline_buckets,
            "graph_summary": graph_summary,
        },
    }


def load_controlled_repo_sample_evidence_items(path: str | Path) -> list[dict]:
    sample_path = Path(path)
    if sample_path.is_absolute():
        raise ValueError("repo_relative_path_required")
    if sample_path.suffix.lower() != ".jsonl":
        raise ValueError("jsonl_only")

    docs_samples_root = (REPO_ROOT / "docs" / "samples").resolve()
    resolved_path = (REPO_ROOT / sample_path).resolve()
    try:
        resolved_path.relative_to(docs_samples_root)
    except ValueError as exc:
        raise ValueError("docs_samples_only") from exc

    items: list[dict] = []
    with resolved_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            value = json.loads(stripped)
            if not isinstance(value, dict):
                raise ValueError(f"jsonl_object_required_at_line_{line_number}")
            items.append(value)
    return items


def _blocked_run(sample_id: str, privacy_scan: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_schema": RUN_SCHEMA,
        "run_status": "blocked",
        "sample_id": str(sample_id),
        "input_scope_note": INPUT_SCOPE_NOTE,
        "generated_at": _generated_at(),
        "model_version": MODEL_VERSION,
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "human_review_required": True,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "warnings": ["privacy_or_forbidden_active_field_detected"],
        "blockers": privacy_scan["blockers"],
        "privacy_scan": privacy_scan,
        "graph": {
            "nodes": [],
            "edges": [],
            "timeline_buckets": [],
            "graph_summary": {
                "people_cluster_proxy_count": 0,
                "influence_core_proxy_count": 0,
                "content_aggregate_proxy_count": 0,
                "echobox_proxy_count": 0,
                "edge_count": 0,
                "timeline_bucket_count": 0,
                "raw_evidence_count": len(privacy_scan.get("item_scan_refs", [])),
                "eligible_evidence_count": 0,
                "rejected_excluded_count": 0,
                "duplicate_folded_count": 0,
            },
        },
    }


def _boundary_flags() -> dict[str, bool]:
    return {
        "selected_sample_only": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_full_thread": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_production_score": True,
        "no_auto_execute": True,
        "no_generated_public_response": True,
        "anonymous_aggregate_only": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "called_real_api": False,
        "called_real_llm": False,
        "ran_collector": False,
        "accessed_private_collector": False,
        "read_real_exchange_dir": False,
        "fetched_url": False,
        "scraped_page": False,
        "wrote_evidence_layer": False,
        "created_production_case": False,
        "created_analysis_run": False,
        "generated_b_end_report_runtime": False,
        "generated_sandbox_runtime": False,
        "generated_public_event_runtime": False,
        "generated_response_text": False,
        "published_or_sent": False,
        "auto_executed": False,
    }


def _generated_at() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _scan_for_forbidden_fields(evidence_items: list[dict]) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    raw_identifier_found = False
    secret_like_found = False
    item_refs: list[str] = []
    for index, evidence in enumerate(evidence_items):
        item_refs.append(f"evidence_index_{index}")
        for path, field in _iter_fields(evidence):
            normalized_field = field.strip().lower()
            if normalized_field in FORBIDDEN_ACTIVE_FIELDS:
                raw_identifier_found = raw_identifier_found or normalized_field in {
                    "raw_author_id",
                    "author_id",
                    "author_name",
                    "profile_url",
                }
                secret_like_found = secret_like_found or normalized_field in {
                    "cookie",
                    "session",
                    "token",
                    "password",
                    "api_key",
                }
                blockers.append(
                    {
                        "item_ref": f"evidence_index_{index}",
                        "field": normalized_field,
                        "path": path,
                        "reason": "forbidden_active_field_present",
                    }
                )
    return {
        "raw_identifier_found": raw_identifier_found,
        "secret_like_found": secret_like_found,
        "privacy_stop": bool(blockers),
        "blocked_field_count": len(blockers),
        "blockers": blockers,
        "item_scan_refs": item_refs,
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


def _deduplicate_eligible_evidence(evidence_items: list[dict]) -> list[dict]:
    selected_by_group: dict[str, dict] = {}
    for index, evidence in enumerate(evidence_items):
        if _is_rejected(evidence):
            continue
        group_id = _duplicate_group_id(evidence, index)
        selected_by_group.setdefault(group_id, evidence)
    return list(selected_by_group.values())


def _is_rejected(evidence: dict) -> bool:
    return _label(evidence.get("review_status")) in REJECTED_REVIEW_STATUSES


def _duplicate_group_id(evidence: dict, index: int) -> str:
    for field in ("duplicate_group_id", "canonical_url_hash", "source_url", "url", "evidence_id", "content_id"):
        value = evidence.get(field)
        if value:
            return f"{field}:{value}"
    return f"evidence_index:{index}"


def _build_timeline_buckets(eligible_items: list[dict]) -> list[dict[str, Any]]:
    bucket_keys: list[str] = []
    for index, evidence in enumerate(eligible_items):
        bucket_keys.append(_time_bucket_key(evidence, index))
    ordered_keys = sorted(set(bucket_keys))
    if not ordered_keys and eligible_items:
        ordered_keys = ["T0"]
    bucket_ids = {key: f"T{min(index, 6)}" for index, key in enumerate(ordered_keys[:7])}
    counts = Counter(bucket_ids.get(key, "T6") for key in bucket_keys)
    return [
        {
            "bucket_id": f"T{index}",
            "bucket_label": _bucket_label(f"T{index}"),
            "evidence_count": counts.get(f"T{index}", 0),
            "boundary_note": "deterministic_bucket_not_complete_historical_reconstruction",
        }
        for index in range(7)
        if counts.get(f"T{index}", 0) or index == 0
    ]


def _time_bucket_key(evidence: dict, index: int) -> str:
    timestamp = str(evidence.get("created_at") or evidence.get("published_at") or "").strip()
    if len(timestamp) >= 10:
        return timestamp[:10]
    return f"order_{index // 8}"


def _bucket_label(bucket_id: str) -> str:
    labels = {
        "T0": "initial_attention",
        "T1": "discussion_growth",
        "T2": "response_or_context",
        "T3": "cross_platform_relay",
        "T4": "community_deconstruction",
        "T5": "fatigue_or_cooling",
        "T6": "reputation_memory",
    }
    return labels.get(bucket_id, "timeline_bucket")


def _build_people_cluster_proxy_nodes(
    eligible_items: list[dict],
    timeline_buckets: list[dict[str, Any]],
    max_people_clusters: int,
) -> list[dict[str, Any]]:
    if not eligible_items or max_people_clusters <= 0:
        return []
    group_counts = Counter(
        (
            _safe_label(evidence.get("platform") or evidence.get("platform_hint"), "unknown_platform"),
            _safe_stance(evidence.get("stance_hint") or evidence.get("stance_label")),
            _time_bucket_for_index(index, timeline_buckets),
            _safe_label(evidence.get("source_type") or evidence.get("evidence_type"), "unknown_type"),
        )
        for index, evidence in enumerate(eligible_items)
    )
    target_count = min(max_people_clusters, max(len(eligible_items) * 2, len(group_counts) * 3, 12))
    nodes: list[dict[str, Any]] = []
    group_items = sorted(group_counts.items(), key=lambda item: (item[0], item[1]))
    index = 0
    while len(nodes) < target_count:
        group, count = group_items[index % len(group_items)]
        platform_hint, stance_label, time_bucket, source_type = group
        local_round = index // len(group_items)
        activity_level = _bounded(0.25 + 0.08 * count + 0.03 * (local_round % 5))
        emotion_intensity = _bounded(0.35 + 0.07 * _stance_intensity(stance_label) + 0.02 * (local_round % 4))
        attention_level = _bounded(0.30 + 0.06 * count + 0.01 * (index % 7))
        fatigue_level = _bounded(0.12 + 0.04 * local_round)
        confidence = _bounded(0.42 + min(0.24, count * 0.04))
        visual_weight = _bounded(0.20 + 0.05 * count + 0.01 * (index % 9))
        nodes.append(
            {
                "node_id": f"pc_{len(nodes) + 1:04d}",
                "node_type": "people_cluster_proxy",
                "stance_label": stance_label,
                "platform_hint": platform_hint,
                "source_type_hint": source_type,
                "activity_level": activity_level,
                "emotion_intensity": emotion_intensity,
                "attention_level": attention_level,
                "fatigue_level": fatigue_level,
                "confidence": confidence,
                "visual_weight": visual_weight,
                "time_bucket": time_bucket,
                "boundary_note": "anonymous_aggregate_proxy_not_real_person",
            }
        )
        index += 1
    return nodes


def _build_influence_core_proxy_nodes(eligible_items: list[dict]) -> list[dict[str, Any]]:
    platforms = sorted({_safe_label(item.get("platform") or item.get("platform_hint"), "unknown_platform") for item in eligible_items})
    stances = sorted({_safe_stance(item.get("stance_hint") or item.get("stance_label")) for item in eligible_items})
    nodes = []
    for index, label in enumerate([*platforms[:4], *stances[:4]], start=1):
        nodes.append(
            {
                "node_id": f"ic_{index:03d}",
                "node_type": "influence_core_proxy",
                "core_label": label,
                "confidence": 0.55,
                "visual_weight": 0.55,
                "boundary_note": "content_or_narrative_core_not_person",
            }
        )
    return nodes or [
        {
            "node_id": "ic_001",
            "node_type": "influence_core_proxy",
            "core_label": "unknown_core",
            "confidence": 0.30,
            "visual_weight": 0.35,
            "boundary_note": "content_or_narrative_core_not_person",
        }
    ]


def _build_content_aggregate_proxy_nodes(eligible_items: list[dict]) -> list[dict[str, Any]]:
    source_types = sorted({_safe_label(item.get("source_type") or item.get("evidence_type"), "unknown_type") for item in eligible_items})
    return [
        {
            "node_id": f"ca_{index:03d}",
            "node_type": "content_aggregate_proxy",
            "aggregate_label": source_type,
            "confidence": 0.50,
            "visual_weight": 0.45,
            "boundary_note": "content_aggregate_proxy_not_truth_strength",
        }
        for index, source_type in enumerate(source_types[:6], start=1)
    ]


def _build_echobox_proxy_nodes(eligible_items: list[dict]) -> list[dict[str, Any]]:
    platforms = sorted({_safe_label(item.get("platform") or item.get("platform_hint"), "unknown_platform") for item in eligible_items})
    return [
        {
            "node_id": f"eb_{index:03d}",
            "node_type": "echobox_proxy",
            "platform_hint": platform,
            "confidence": 0.48,
            "visual_weight": 0.50,
            "boundary_note": "echo_box_proxy_not_real_social_graph",
        }
        for index, platform in enumerate(platforms[:6], start=1)
    ]


def _build_edges(
    *,
    people_nodes: list[dict],
    influence_nodes: list[dict],
    content_nodes: list[dict],
    echobox_nodes: list[dict],
    max_edges: int,
) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for index, node in enumerate(people_nodes):
        if influence_nodes:
            target = influence_nodes[index % len(influence_nodes)]
            edges.append(_edge(node["node_id"], target["node_id"], "influence_core_exposure", 0.48, len(edges)))
        if echobox_nodes:
            target = echobox_nodes[index % len(echobox_nodes)]
            edges.append(_edge(node["node_id"], target["node_id"], "echobox_membership", 0.52, len(edges)))
        if content_nodes:
            target = content_nodes[index % len(content_nodes)]
            edges.append(_edge(node["node_id"], target["node_id"], "same_platform_discussion", 0.42, len(edges)))
        if index > 0 and people_nodes[index - 1]["time_bucket"] == node["time_bucket"]:
            edges.append(_edge(people_nodes[index - 1]["node_id"], node["node_id"], "same_time_bucket", 0.35, len(edges)))
        if index > 1 and people_nodes[index - 2]["stance_label"] == node["stance_label"]:
            edges.append(_edge(people_nodes[index - 2]["node_id"], node["node_id"], "stance_affinity", 0.33, len(edges)))
        if index > 3 and people_nodes[index - 3]["platform_hint"] != node["platform_hint"]:
            edges.append(_edge(people_nodes[index - 3]["node_id"], node["node_id"], "cross_platform_bridge_candidate", 0.24, len(edges)))
        if len(edges) >= max_edges:
            break
    return edges[:max_edges]


def _edge(source: str, target: str, edge_type: str, weight: float, index: int) -> dict[str, Any]:
    return {
        "edge_id": f"edge_{index + 1:04d}",
        "source": source,
        "target": target,
        "edge_type": edge_type,
        "weight": _bounded(weight),
        "confidence": 0.50 if edge_type != "cross_platform_bridge_candidate" else 0.35,
        "boundary_note": "synthetic_safe_edge_not_real_social_or_causal_graph",
    }


def _graph_summary(
    *,
    evidence_items: list[dict],
    eligible_items: list[dict],
    nodes: list[dict],
    edges: list[dict],
    timeline_buckets: list[dict[str, Any]],
) -> dict[str, Any]:
    type_counts = Counter(node["node_type"] for node in nodes)
    rejected_count = sum(1 for item in evidence_items if _is_rejected(item))
    duplicate_folded_count = _duplicate_folded_count(evidence_items)
    return {
        "raw_evidence_count": len(evidence_items),
        "eligible_evidence_count": len(eligible_items),
        "rejected_excluded_count": rejected_count,
        "duplicate_folded_count": duplicate_folded_count,
        "people_cluster_proxy_count": type_counts.get("people_cluster_proxy", 0),
        "influence_core_proxy_count": type_counts.get("influence_core_proxy", 0),
        "content_aggregate_proxy_count": type_counts.get("content_aggregate_proxy", 0),
        "echobox_proxy_count": type_counts.get("echobox_proxy", 0),
        "edge_count": len(edges),
        "timeline_bucket_count": len(timeline_buckets),
        "density_note": "anonymous_proxy_density_for_future_visualization_not_population_count",
    }


def _duplicate_folded_count(evidence_items: list[dict]) -> int:
    eligible_groups: defaultdict[str, list[dict]] = defaultdict(list)
    for index, evidence in enumerate(evidence_items):
        if not _is_rejected(evidence):
            eligible_groups[_duplicate_group_id(evidence, index)].append(evidence)
    folded = 0
    for group in eligible_groups.values():
        if len(group) > 1:
            folded += len(group) - 1
        for evidence in group:
            duplicate_count = _as_int(evidence.get("duplicate_count"), default=1)
            if duplicate_count > 1:
                folded += duplicate_count - 1
    return folded


def _warnings(evidence_items: list[dict], eligible_items: list[dict]) -> list[str]:
    warnings: list[str] = []
    if len(eligible_items) < len(evidence_items):
        warnings.append("rejected_evidence_excluded_from_density")
    if _duplicate_folded_count(evidence_items) > 0:
        warnings.append("duplicates_folded_to_reduce_amplification")
    warnings.append("selected_sample_only_not_full_web_or_platform")
    return warnings


def _time_bucket_for_index(index: int, timeline_buckets: list[dict[str, Any]]) -> str:
    if not timeline_buckets:
        return "T0"
    return timeline_buckets[min(index % len(timeline_buckets), len(timeline_buckets) - 1)]["bucket_id"]


def _safe_stance(value: Any) -> str:
    label = _safe_label(value, "unknown")
    return label if label in STANCE_LABELS else "unknown"


def _safe_label(value: Any, default: str) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return default
    digest = sha256(text.encode("utf-8")).hexdigest()[:8]
    safe = "".join(char if char.isalnum() else "_" for char in text)[:32].strip("_")
    return safe or f"label_{digest}"


def _label(value: Any) -> str:
    return str(value or "").strip().lower()


def _stance_intensity(stance_label: str) -> float:
    return {
        "oppose": 1.0,
        "support": 0.8,
        "mixed": 0.6,
        "neutral": 0.35,
        "unknown": 0.25,
    }.get(stance_label, 0.25)


def _bounded(value: float) -> float:
    return round(max(0.0, min(1.0, float(value))), 4)


def _as_int(value: Any, *, default: int) -> int:
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return default
