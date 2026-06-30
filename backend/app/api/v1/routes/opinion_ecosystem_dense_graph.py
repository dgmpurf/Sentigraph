from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Request

from app.services import opinion_ecosystem_dense_graph_builder as dense_builder
from app.services import opinion_ecosystem_dense_graph_generated_run_integration as integration


router = APIRouter()

ENV_FLAG = "SENTIGRAPH_OPINION_ECOSYSTEM_DENSE_GRAPH_ROUTE_ENABLED"
RESPONSE_SCHEMA = "sentigraph_opinion_ecosystem_dense_graph_route_response_v0_1"
ERROR_SCHEMA = "sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1"
VISUALIZATION_MODE = "dense_sandbox_proxy_graph"

ALLOWED_TRUE_VALUES = {"1", "true", "yes"}
ALLOWED_SAMPLE_PATHS = {
    "donglu-sunjihai-youth-football": (
        "docs/samples/donglu_sunjihai_youth_football/"
        "donglu-sunjihai-youth-football-202606-v2_20260617_121016/evidence_items.jsonl"
    ),
    "helldivers-psn": (
        "docs/samples/helldivers2_psn_demo/"
        "helldivers2-psn-demo_20260614_055754/evidence_items.jsonl"
    ),
}
ALLOWED_QUERY_PARAMS = {"node_limit", "edge_limit", "include_previews"}


@router.get("/generated-runs/{sample_id:path}")
def get_dense_graph_generated_run(
    sample_id: str,
    request: Request,
    node_limit: int = 240,
    edge_limit: int = 800,
    include_previews: bool = True,
) -> dict[str, Any]:
    if not _route_enabled():
        return _safe_error("disabled", "route_disabled", "Dense graph route is disabled.")

    unsupported_params = sorted(set(request.query_params.keys()) - ALLOWED_QUERY_PARAMS)
    if unsupported_params:
        return _safe_error(
            "unsupported_sample",
            "unsupported_query_parameter",
            "Dense graph route query parameter is not supported.",
            sample_id=sample_id,
        )

    if sample_id not in ALLOWED_SAMPLE_PATHS:
        return _unsupported_sample(sample_id)

    evidence_items = _load_allowed_sample_evidence_items(sample_id)
    if evidence_items is None:
        return _unsupported_sample(sample_id)

    bounded_node_limit = _bounded_int(node_limit, minimum=20, maximum=240)
    bounded_edge_limit = _bounded_int(edge_limit, minimum=50, maximum=800)
    fixture = _build_fixture_from_evidence_items(sample_id, evidence_items)
    generated_run_integration = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        fixture,
        sample_id=sample_id,
        source_run_id=f"dense_graph_route_{sample_id}",
        max_people_clusters=bounded_node_limit,
        max_edges=bounded_edge_limit,
    )
    generated_run_integration = _apply_preview_policy(
        generated_run_integration,
        node_limit=bounded_node_limit,
        edge_limit=bounded_edge_limit,
        include_previews=include_previews,
    )
    return _route_response(
        sample_id=sample_id,
        generated_run_integration=generated_run_integration,
        node_limit=bounded_node_limit,
        edge_limit=bounded_edge_limit,
        include_previews=include_previews,
    )


def _route_enabled() -> bool:
    return (os.environ.get(ENV_FLAG) or "").strip().lower() in ALLOWED_TRUE_VALUES


def _load_allowed_sample_evidence_items(sample_id: str) -> list[dict[str, Any]] | None:
    sample_path = ALLOWED_SAMPLE_PATHS.get(sample_id)
    if not sample_path:
        return None
    try:
        return dense_builder.load_controlled_repo_sample_evidence_items(sample_path)
    except (OSError, ValueError):
        return None


def _route_response(
    *,
    sample_id: str,
    generated_run_integration: dict[str, Any],
    node_limit: int,
    edge_limit: int,
    include_previews: bool,
) -> dict[str, Any]:
    integration_status = str(generated_run_integration.get("integration_status") or "")
    if integration_status == "blocked":
        route_status = "blocked"
    elif integration_status.startswith("degraded"):
        route_status = "degraded"
    else:
        route_status = "ready"

    summary = _graph_summary(generated_run_integration)
    return {
        "response_schema": RESPONSE_SCHEMA,
        "route_status": route_status,
        "sample_id": sample_id,
        "generated_run_integration": generated_run_integration,
        "graph_summary": summary,
        "preview_limits": {
            "node_limit": node_limit,
            "edge_limit": edge_limit,
            "include_previews": include_previews,
        },
        "boundary_flags": generated_run_integration.get("boundary_flags", {}),
        "runtime_side_effects": generated_run_integration.get("runtime_side_effects", {}),
        "warnings": generated_run_integration.get("warnings", []),
        "blockers": generated_run_integration.get("blockers", []),
        "human_review_required": True,
    }


def _graph_summary(generated_run_integration: dict[str, Any]) -> dict[str, Any]:
    summary = generated_run_integration.get("integration_summary")
    summary = summary if isinstance(summary, dict) else {}
    return {
        "people_cluster_proxy_count": _safe_int(summary.get("people_cluster_proxy_count")),
        "influence_core_proxy_count": _safe_int(summary.get("influence_core_proxy_count")),
        "content_aggregate_proxy_count": _safe_int(summary.get("content_aggregate_proxy_count")),
        "echobox_proxy_count": _safe_int(summary.get("echobox_proxy_count")),
        "edge_count": _safe_int(summary.get("edge_count")),
        "timeline_bucket_count": _safe_int(summary.get("timeline_bucket_count")),
        "recommended_visualization_mode": str(summary.get("recommended_visualization_mode") or VISUALIZATION_MODE),
        "frontend_ready": False,
        "production_ready": False,
    }


def _apply_preview_policy(
    generated_run_integration: dict[str, Any],
    *,
    node_limit: int,
    edge_limit: int,
    include_previews: bool,
) -> dict[str, Any]:
    attachment = generated_run_integration.get("dense_graph_attachment")
    if not isinstance(attachment, dict):
        return generated_run_integration
    if include_previews:
        attachment["nodes_preview"] = _dict_list(attachment.get("nodes_preview"))[:node_limit]
        attachment["edges_preview"] = _dict_list(attachment.get("edges_preview"))[:edge_limit]
    else:
        attachment["nodes_preview"] = []
        attachment["edges_preview"] = []
    attachment["suggested_max_render_nodes"] = node_limit
    attachment["suggested_max_render_edges"] = edge_limit
    return generated_run_integration


def _build_fixture_from_evidence_items(sample_id: str, evidence_items: list[dict[str, Any]]) -> dict[str, Any]:
    safe_evidence = [_safe_evidence_item(index, item) for index, item in enumerate(evidence_items)]
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": f"dense_graph_route_fixture_{sample_id}",
            "case_id": f"case_{sample_id}",
            "sample_id": sample_id,
            "fixture_role": "controlled_repo_sample_route_fixture",
            "source_mode": "controlled_repo_docs_samples",
            "stage_id": "T4",
            "coverage_note": "selected controlled local sample only",
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": safe_evidence,
        "content_aggregates": [_content_aggregate()],
        "influence_cores": [_influence_core([item["evidence_id"] for item in safe_evidence[:10]])],
        "echo_boxes": [_echo_box()],
        "people_clusters": [_people_cluster()],
        "response_strategy_candidates": [_response_strategy_candidate()],
    }


def _safe_evidence_item(index: int, item: dict[str, Any]) -> dict[str, Any]:
    evidence_id = str(item.get("evidence_id") or item.get("content_id") or f"evidence_{index:04d}")
    platform = _safe_label(item.get("platform") or item.get("platform_hint"), "unknown_platform")
    source_type = _safe_label(item.get("source_type") or item.get("evidence_type") or item.get("content_type_hint"), "comment")
    stance_hint = _safe_stance(item.get("stance_hint") or item.get("stance_label"))
    return {
        "evidence_id": evidence_id,
        "platform": platform,
        "provenance_type": "controlled_repo_sample",
        "verification_status": "user_attested_unverified",
        "trust_label": _safe_label(item.get("trust_label"), "medium"),
        "review_status": _safe_label(item.get("review_status"), "approved"),
        "duplicate_group_id": str(item.get("duplicate_group_id") or item.get("canonical_url_hash") or evidence_id),
        "duplicate_count": _safe_int(item.get("duplicate_count"), default=1),
        "relevance_label": "controlled_sample_case_match",
        "recency_label": "controlled_sample_window",
        "stance_hint": stance_hint,
        "emotion_intensity_hint": _safe_float(item.get("emotion_intensity_hint"), default=0.5),
        "source_url_present": bool(item.get("source_url") or item.get("url")),
        "source_url": str(item.get("source_url") or item.get("url") or ""),
        "title": str(item.get("title") or "")[:120],
        "body_text": str(item.get("body_text") or item.get("comment_text") or item.get("snippet") or "")[:240],
        "created_at": str(item.get("created_at") or item.get("published_at") or ""),
        "aggregate_ref": "agg_001",
        "influence_core_refs": ["core_controlled_sample_001"],
        "echo_box_refs": ["echo_controlled_sample_001"],
        "people_cluster_refs": ["cluster_controlled_sample_001"],
    }


def _content_aggregate() -> dict[str, float | str]:
    return {
        "aggregate_id": "agg_001",
        "volume_score": 0.45,
        "interaction_score": 0.30,
        "growth_score": 0.25,
        "emotion_intensity": 0.50,
        "spread_score": 0.35,
        "issue_sensitivity": 0.45,
        "response_gap": 0.30,
    }


def _influence_core(evidence_ids: list[str]) -> dict[str, Any]:
    return {
        "core_id": "core_controlled_sample_001",
        "core_type": "controlled_sample_narrative",
        "associated_evidence_ids": evidence_ids,
        "clarity_hint": 0.70,
        "novelty_hint": 0.35,
        "bridge_hint": 0.55,
        "backlash_hint": 0.24,
        "emotional_charge_hint": 0.35,
        "repetition_hint": 0.22,
        "resolution_signal_hint": 0.48,
        "source_transparency_hint": 0.68,
        "cross_source_consistency_hint": 0.58,
        "privacy_safety_pass": True,
        "identity_or_group_relevance_hint": 0.42,
        "meme_or_symbolic_density_hint": 0.18,
        "neutral_or_explanatory_frame_hint": 0.55,
        "source_credibility_across_camps_hint": 0.52,
        "low_identity_threat_language_hint": 0.68,
        "shared_value_language_hint": 0.48,
        "media_or_third_party_relay_hint": 0.28,
        "empathy_or_context_hint": 0.50,
    }


def _echo_box() -> dict[str, Any]:
    return {
        "echo_box_id": "echo_controlled_sample_001",
        "echo_box_role": "controlled_sample_discussion",
        "echo_type": "mixed_discussion_box",
        "platform_refs": ["controlled_sample"],
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_controlled_sample_001"],
        "stance_distribution": {"support": 0.25, "oppose": 0.35, "neutral": 0.25, "mixed": 0.15},
        "interaction_proxy_summary": {"internal_density": 0.45},
        "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.35},
        "cross_box_exposure_hint": 0.35,
        "bridge_cluster_share_hint": 0.36,
        "low_identity_threat_language_hint": 0.62,
        "media_or_third_party_relay_hint": 0.25,
        "novelty_constructive_hint": 0.30,
        "repetition_hint": 0.24,
    }


def _people_cluster() -> dict[str, Any]:
    return {
        "cluster_id": "cluster_controlled_sample_001",
        "cluster_role": "controlled_sample_anonymous_group",
        "cluster_type": "mixed_bridge",
        "sample_share_hint": 0.42,
        "stance_distribution": {"support": 0.25, "oppose": 0.35, "neutral": 0.25, "mixed": 0.15},
        "stance_confidence_hint": 0.55,
        "attention_hint": 0.50,
        "fatigue_hint": 0.30,
        "expression_hint": 0.46,
        "openness_hint": 0.58,
        "confidence_radius_hint": 0.60,
        "aggregate_ids": ["agg_001"],
        "influence_core_ids": ["core_controlled_sample_001"],
        "echo_box_ids": ["echo_controlled_sample_001"],
        "previous_state": {"stance_score": 0.0, "attention_level": 0.40, "fatigue_level": 0.25},
        "novelty_signal_hint": 0.30,
        "personal_relevance_proxy_hint": 0.35,
        "reactivation_trigger_hint": 0.22,
        "resolution_signal_hint": 0.38,
        "unresolved_grievance_hint": 0.28,
        "constructive_new_info_hint": 0.45,
        "bridge_understanding_hint": 0.42,
        "social_norm_pressure_hint": 0.34,
        "action_threshold_hint": 0.50,
        "reputation_memory_hint": 0.35,
        "new_trigger_hint": 0.24,
        "identity_relevance_proxy_hint": 0.30,
    }


def _response_strategy_candidate() -> dict[str, Any]:
    return {
        "candidate_id": "strategy_candidate_controlled_sample",
        "strategy_id": "S4",
        "strategy_type": "FAQ_or_longform_explanation",
        "stage_id": "T4",
        "claim_intensity": 0.20,
        "stage_fit": 0.74,
        "response_gap_fit": 0.70,
        "heat_fit": 0.68,
        "fatigue_fit": 0.58,
        "strategy_clarity_base": 0.82,
        "strategy_deescalation_base": 0.68,
        "strategy_bridge_base": 0.55,
        "transparency_level": 0.78,
        "accountability_level": 0.66,
        "consistency_with_prior_record": 0.62,
        "resolution_signal": 0.58,
        "low_amplification_level": 0.70,
        "constructive_new_info": 0.72,
        "unresolved_grievance_reduction": 0.52,
        "low_identity_threat_language": 0.72,
        "exposure_level": 0.30,
        "novelty": 0.22,
        "media_relay_probability": 0.20,
        "mismatch_with_cluster_concerns": 0.20,
        "perceived_defensiveness": 0.16,
        "timing_lag": 0.18,
        "low_empathy_language": 0.12,
        "contradiction_with_prior_record": 0.08,
        "identity_threat_risk": 0.12,
        "ambiguity": 0.12,
        "causal_language": 0.0,
        "full_web_claim": 0.0,
        "official_verification_claim": 0.0,
        "prediction_language": 0.0,
        "uncalibrated_score_without_boundary": 0.0,
        "requires_new_runtime": 0.0,
        "requires_real_API_or_LLM": 0.0,
        "requires_unreviewed_data": 0.0,
        "requires_external_actor_coordination": 0.0,
        "requires_legal_review": 0.0,
        "requires_sensitive_material": 0.0,
    }


def _unsupported_sample(sample_id: str) -> dict[str, Any]:
    return _safe_error(
        "unsupported_sample",
        "unsupported_sample",
        "Sample is not supported for dense graph route.",
        sample_id=sample_id,
    )


def _safe_error(route_status: str, error_code: str, message: str, *, sample_id: str | None = None) -> dict[str, Any]:
    response: dict[str, Any] = {
        "error_schema": ERROR_SCHEMA,
        "route_status": route_status,
        "error_code": error_code,
        "message": message,
        "path_exposed": False,
        "raw_metadata_exposed": False,
        "private_collector_path_exposed": False,
        "evidence_rows_exposed": False,
    }
    if sample_id is not None:
        response["sample_id"] = str(sample_id)
    return response


def _dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _bounded_int(value: Any, *, minimum: int, maximum: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = maximum
    return max(minimum, min(maximum, number))


def _safe_int(value: Any, *, default: int = 0) -> int:
    try:
        return max(0, int(float(value)))
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, *, default: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        number = default
    return max(0.0, min(1.0, number))


def _safe_stance(value: Any) -> str:
    label = _safe_label(value, "unknown")
    return label if label in {"support", "neutral", "oppose", "mixed", "unknown"} else "unknown"


def _safe_label(value: Any, default: str) -> str:
    text = str(value or "").strip().lower()
    if not text:
        return default
    safe = "".join(char if char.isalnum() else "_" for char in text)[:40].strip("_")
    return safe or default
