from __future__ import annotations

import json

from app.services import opinion_ecosystem_dense_graph_builder as dense_builder
from app.services import opinion_ecosystem_dense_graph_generated_run_adapter as adapter


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

FORBIDDEN_OUTPUT_KEYS = {
    "raw_author_id",
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


def _evidence(index: int, **overrides: object) -> dict:
    item = {
        "evidence_id": f"evidence_{index:03d}",
        "platform": "sample_forum" if index % 2 else "sample_news",
        "source_type": "comment" if index % 3 else "post",
        "source_url": f"https://example.test/thread/{index % 5}",
        "title": f"Safe sample title {index % 4}",
        "body_text": f"safe selected public sample text {index % 7}",
        "created_at": f"2026-06-{(index % 7) + 1:02d}T12:00:00Z",
        "stance_hint": ["support", "neutral", "oppose", "mixed"][index % 4],
        "review_status": "approved",
        "trust_label": "medium",
        "duplicate_group_id": f"dup_{index}",
    }
    item.update(overrides)
    return item


def _dense_graph_run(count: int = 12) -> dict:
    return dense_builder.build_dense_opinion_graph_from_evidence_items(
        [_evidence(index) for index in range(count)],
        sample_id="unit_adapter_sample",
        max_people_clusters=80,
        max_edges=180,
    )


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_walk_keys(child))
    return keys


def test_builds_attachment_from_synthetic_dense_graph_run() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment(
        dense_graph_run=_dense_graph_run(),
        source_run_id="minimum_real_run_unit",
    )

    assert attachment["attachment_schema"] == "sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1"
    assert attachment["attachment_status"] == "ready_for_backend_generated_run_surface"
    assert attachment["source_run_id"] == "minimum_real_run_unit"
    assert attachment["sample_id"] == "unit_adapter_sample"
    assert attachment["graph_schema"] == "sentigraph_opinion_ecosystem_dense_graph_run_v0_1"
    assert attachment["human_review_required"] is True
    assert attachment["recommended_visualization_mode"] == "dense_sandbox_proxy_graph"
    assert attachment["graph_summary"]["people_cluster_proxy_count"] > 0
    assert attachment["nodes_preview"]
    assert attachment["edges_preview"]
    assert attachment["timeline_buckets"]


def test_builds_attachment_from_evidence_items_via_dense_builder() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment_from_evidence_items(
        [_evidence(index) for index in range(20)],
        sample_id="adapter_from_evidence",
        source_run_id="minimum_real_run_from_evidence",
        max_people_clusters=90,
        max_edges=220,
    )

    assert attachment["attachment_status"] == "ready_for_backend_generated_run_surface"
    assert attachment["sample_id"] == "adapter_from_evidence"
    assert attachment["source_run_id"] == "minimum_real_run_from_evidence"
    assert attachment["graph_summary"]["people_cluster_proxy_count"] > 20
    assert attachment["graph_summary"]["edge_count"] <= 220


def test_preserves_required_boundary_flags_and_false_side_effects() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment(dense_graph_run=_dense_graph_run())

    assert REQUIRED_BOUNDARY_FLAGS <= set(attachment["boundary_flags"])
    assert all(attachment["boundary_flags"][flag] is True for flag in REQUIRED_BOUNDARY_FLAGS)
    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(attachment["runtime_side_effects"])
    assert all(attachment["runtime_side_effects"][flag] is False for flag in REQUIRED_SIDE_EFFECT_FLAGS)


def test_exposes_graph_counts_and_preview_metadata_for_future_frontend() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment(
        dense_graph_run=_dense_graph_run(24),
        suggested_max_render_nodes=64,
        suggested_max_render_edges=128,
    )
    summary = attachment["graph_summary"]

    assert summary["people_cluster_proxy_count"] == attachment["people_cluster_proxy_count"]
    assert summary["influence_core_proxy_count"] == attachment["influence_core_proxy_count"]
    assert summary["content_aggregate_proxy_count"] == attachment["content_aggregate_proxy_count"]
    assert summary["echobox_proxy_count"] == attachment["echobox_proxy_count"]
    assert summary["edge_count"] == attachment["edge_count"]
    assert summary["timeline_bucket_count"] == attachment["timeline_bucket_count"]
    assert attachment["suggested_max_render_nodes"] == 64
    assert attachment["suggested_max_render_edges"] == 128
    assert "not_population_count" in attachment["density_note"]


def test_blocks_forbidden_field_in_node_metadata_without_exposing_value() -> None:
    dense_graph_run = _dense_graph_run()
    dense_graph_run["graph"]["nodes"][0]["metadata"] = {"author_name": "Do Not Expose"}

    attachment = adapter.build_dense_graph_generated_run_attachment(dense_graph_run=dense_graph_run)
    encoded = json.dumps(attachment, ensure_ascii=False)

    assert attachment["attachment_status"] == "blocked"
    assert attachment["blockers"]
    assert "Do Not Expose" not in encoded
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(attachment))


def test_blocks_generated_response_text_without_exposing_value() -> None:
    dense_graph_run = _dense_graph_run()
    dense_graph_run["generated_response_text"] = "draft response should not leave adapter"

    attachment = adapter.build_dense_graph_generated_run_attachment(dense_graph_run=dense_graph_run)
    encoded = json.dumps(attachment, ensure_ascii=False)

    assert attachment["attachment_status"] == "blocked"
    assert "draft response should not leave adapter" not in encoded
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(attachment))


def test_missing_boundary_flags_returns_degraded_attachment_with_warning() -> None:
    dense_graph_run = _dense_graph_run()
    dense_graph_run["boundary_flags"] = {"selected_sample_only": True}

    attachment = adapter.build_dense_graph_generated_run_attachment(dense_graph_run=dense_graph_run)

    assert attachment["attachment_status"] == "degraded_missing_boundary_flags"
    assert "missing_boundary_flags" in attachment["warnings"]
    assert REQUIRED_BOUNDARY_FLAGS <= set(attachment["boundary_flags"])
    assert all(attachment["boundary_flags"][flag] is True for flag in REQUIRED_BOUNDARY_FLAGS)


def test_invalid_dense_graph_schema_returns_safe_blocked_attachment() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment(
        dense_graph_run={"run_schema": "unknown", "graph": {}},
        sample_id="invalid_schema_sample",
    )

    assert attachment["attachment_status"] == "blocked"
    assert attachment["sample_id"] == "invalid_schema_sample"
    assert attachment["blockers"][0]["reason"] == "invalid_dense_graph_run_schema"


def test_output_is_json_serializable_and_does_not_require_route_or_frontend() -> None:
    attachment = adapter.build_dense_graph_generated_run_attachment(dense_graph_run=_dense_graph_run())

    encoded = json.dumps(attachment, ensure_ascii=False, sort_keys=True)
    assert "sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1" in encoded
    assert "route" not in attachment
    assert "frontend" not in attachment
