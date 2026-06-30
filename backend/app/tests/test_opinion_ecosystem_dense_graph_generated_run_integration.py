from __future__ import annotations

import json

from app.services import opinion_ecosystem_dense_graph_generated_run_integration as integration


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


def _fixture(evidence_count: int = 16) -> dict:
    evidence_items = [
        {
            "evidence_id": f"evidence_{index:03d}",
            "platform": "sample_forum" if index % 2 else "sample_news",
            "provenance_type": "manual_url_with_attestation",
            "verification_status": "user_attested_unverified",
            "trust_label": "medium",
            "review_status": "approved",
            "duplicate_group_id": f"dup_{index}",
            "duplicate_count": 1,
            "relevance_label": "strong_case_match",
            "recency_label": "inside_stage_window",
            "stance_hint": ["support", "neutral", "oppose", "mixed"][index % 4],
            "emotion_intensity_hint": (index % 10) / 10,
            "source_url_present": True,
            "source_url": f"https://example.test/thread/{index % 5}",
            "title": f"Safe sample title {index % 4}",
            "body_text": f"safe selected public sample text {index % 7}",
            "created_at": f"2026-06-{(index % 7) + 1:02d}T12:00:00Z",
            "aggregate_ref": "agg_001",
            "influence_core_refs": ["core_001"],
            "echo_box_refs": ["echo_001"],
            "people_cluster_refs": ["cluster_001"],
        }
        for index in range(evidence_count)
    ]
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": "fixture_8u3",
            "case_id": "case_8u3",
            "sample_id": "sample_8u3",
            "fixture_role": "unit_test_synthetic",
            "source_mode": "synthetic_fixture",
            "stage_id": "T4",
            "coverage_note": "selected synthetic fixture only",
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": evidence_items,
        "content_aggregates": [
            {
                "aggregate_id": "agg_001",
                "volume_score": 0.40,
                "interaction_score": 0.30,
                "growth_score": 0.20,
                "emotion_intensity": 0.50,
                "spread_score": 0.25,
                "issue_sensitivity": 0.40,
                "response_gap": 0.30,
            }
        ],
        "influence_cores": [
            {
                "core_id": "core_001",
                "core_type": "official_statement",
                "associated_evidence_ids": ["evidence_001"],
                "clarity_hint": 0.86,
                "novelty_hint": 0.20,
                "bridge_hint": 0.62,
                "backlash_hint": 0.12,
                "emotional_charge_hint": 0.20,
                "repetition_hint": 0.10,
                "resolution_signal_hint": 0.78,
                "source_transparency_hint": 0.94,
                "cross_source_consistency_hint": 0.85,
                "privacy_safety_pass": True,
                "identity_or_group_relevance_hint": 0.45,
                "meme_or_symbolic_density_hint": 0.05,
                "neutral_or_explanatory_frame_hint": 0.80,
                "source_credibility_across_camps_hint": 0.72,
                "low_identity_threat_language_hint": 0.88,
                "shared_value_language_hint": 0.60,
                "media_or_third_party_relay_hint": 0.20,
                "empathy_or_context_hint": 0.72,
            }
        ],
        "echo_boxes": [
            {
                "echo_box_id": "echo_001",
                "echo_box_role": "mixed_discussion_box",
                "echo_type": "mixed_discussion_box",
                "platform_refs": ["sample_forum"],
                "aggregate_ids": ["agg_001"],
                "influence_core_ids": ["core_001"],
                "stance_distribution": {"support": 0.40, "oppose": 0.35, "neutral": 0.15, "mixed": 0.10},
                "interaction_proxy_summary": {"internal_density": 0.45},
                "cross_cutting_proxy_summary": {"cross_cutting_exposure": 0.40},
                "cross_box_exposure_hint": 0.35,
                "bridge_cluster_share_hint": 0.42,
                "low_identity_threat_language_hint": 0.72,
                "media_or_third_party_relay_hint": 0.20,
                "novelty_constructive_hint": 0.22,
                "repetition_hint": 0.20,
            }
        ],
        "people_clusters": [
            {
                "cluster_id": "cluster_001",
                "cluster_role": "mixed_bridge",
                "cluster_type": "mixed_bridge",
                "sample_share_hint": 0.42,
                "stance_distribution": {"support": 0.36, "oppose": 0.30, "neutral": 0.22, "mixed": 0.12},
                "stance_confidence_hint": 0.58,
                "attention_hint": 0.46,
                "fatigue_hint": 0.30,
                "expression_hint": 0.44,
                "openness_hint": 0.66,
                "confidence_radius_hint": 0.64,
                "aggregate_ids": ["agg_001"],
                "influence_core_ids": ["core_001"],
                "echo_box_ids": ["echo_001"],
                "previous_state": {"stance_score": 0.05, "attention_level": 0.40, "fatigue_level": 0.22},
                "novelty_signal_hint": 0.30,
                "personal_relevance_proxy_hint": 0.35,
                "reactivation_trigger_hint": 0.22,
                "resolution_signal_hint": 0.42,
                "unresolved_grievance_hint": 0.28,
                "constructive_new_info_hint": 0.50,
                "bridge_understanding_hint": 0.46,
                "social_norm_pressure_hint": 0.34,
                "action_threshold_hint": 0.52,
                "reputation_memory_hint": 0.38,
                "new_trigger_hint": 0.24,
                "identity_relevance_proxy_hint": 0.30,
            }
        ],
        "response_strategy_candidates": [
            {
                "candidate_id": "strategy_candidate_s4",
                "strategy_id": "S4",
                "strategy_type": "FAQ_or_longform_explanation",
                "stage_id": "T4",
                "claim_intensity": 0.28,
                "stage_fit": 0.82,
                "response_gap_fit": 0.74,
                "heat_fit": 0.70,
                "fatigue_fit": 0.62,
                "strategy_clarity_base": 0.92,
                "strategy_deescalation_base": 0.70,
                "strategy_bridge_base": 0.58,
                "transparency_level": 0.88,
                "accountability_level": 0.78,
                "consistency_with_prior_record": 0.76,
                "resolution_signal": 0.70,
                "low_amplification_level": 0.66,
                "constructive_new_info": 0.82,
                "unresolved_grievance_reduction": 0.62,
                "low_identity_threat_language": 0.78,
                "exposure_level": 0.34,
                "novelty": 0.18,
                "media_relay_probability": 0.20,
                "mismatch_with_cluster_concerns": 0.20,
                "perceived_defensiveness": 0.14,
                "timing_lag": 0.18,
                "low_empathy_language": 0.10,
                "contradiction_with_prior_record": 0.08,
                "identity_threat_risk": 0.12,
                "ambiguity": 0.10,
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
        ],
    }


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


def test_builds_integrated_generated_run_object_from_safe_fixture() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        _fixture(),
        sample_id="sample_8u3",
        source_run_id="source_run_8u3",
    )

    assert result["integration_schema"] == "sentigraph_opinion_ecosystem_generated_run_dense_graph_integration_v0_1"
    assert result["integration_status"] == "ready_for_backend_service_surface"
    assert result["sample_id"] == "sample_8u3"
    assert result["source_run_id"] == "source_run_8u3"
    assert result["base_generated_run"]["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert result["base_generated_run"]["run_status"] == "ready"
    assert result["human_review_required"] is True


def test_includes_dense_graph_attachment_with_expected_schema() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(_fixture(), sample_id="sample_8u3")

    attachment = result["dense_graph_attachment"]
    assert attachment["attachment_schema"] == "sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1"
    assert attachment["attachment_status"] == "ready_for_backend_generated_run_surface"
    assert result["integration_summary"]["dense_graph_attached"] is True


def test_preserves_base_and_dense_graph_boundary_flags() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(_fixture(), sample_id="sample_8u3")

    assert REQUIRED_BOUNDARY_FLAGS <= set(result["boundary_flags"])
    assert all(result["boundary_flags"][flag] is True for flag in REQUIRED_BOUNDARY_FLAGS)
    assert result["base_generated_run"]["boundary_flags"]["selected_sample_only"] is True
    assert result["dense_graph_attachment"]["boundary_flags"]["anonymous_aggregate_only"] is True


def test_runtime_side_effect_flags_are_all_false() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(_fixture(), sample_id="sample_8u3")

    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(result["runtime_side_effects"])
    assert all(result["runtime_side_effects"][flag] is False for flag in REQUIRED_SIDE_EFFECT_FLAGS)
    assert result["base_generated_run"]["runtime_side_effects"]["called_real_api"] is False
    assert result["dense_graph_attachment"]["runtime_side_effects"]["called_real_api"] is False


def test_integration_summary_exposes_graph_counts_and_readiness_false() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        _fixture(24),
        sample_id="sample_8u3",
        max_people_clusters=120,
        max_edges=260,
    )
    summary = result["integration_summary"]

    assert summary["people_cluster_proxy_count"] > 24
    assert summary["influence_core_proxy_count"] > 0
    assert summary["content_aggregate_proxy_count"] > 0
    assert summary["echobox_proxy_count"] > 0
    assert summary["edge_count"] <= 260
    assert summary["timeline_bucket_count"] > 0
    assert summary["recommended_visualization_mode"] == "dense_sandbox_proxy_graph"
    assert summary["frontend_ready"] is False
    assert summary["route_ready"] is False
    assert summary["production_ready"] is False


def test_blocks_forbidden_field_in_dense_graph_attachment_path() -> None:
    fixture = _fixture()
    fixture["evidence_items_safe"][0]["author_name"] = "Do Not Expose"

    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(fixture, sample_id="sample_8u3")
    encoded = json.dumps(result, ensure_ascii=False)

    assert result["integration_status"] == "blocked"
    assert result["blockers"]
    assert "Do Not Expose" not in encoded
    assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(result))


def test_blocks_response_text_generated_public_message_and_auto_execute() -> None:
    for forbidden_key in ("response_text", "generated_public_message", "auto_execute"):
        fixture = _fixture()
        fixture["evidence_items_safe"][0][forbidden_key] = "blocked value"

        result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(fixture, sample_id="sample_8u3")
        encoded = json.dumps(result, ensure_ascii=False)

        assert result["integration_status"] == "blocked"
        assert "blocked value" not in encoded
        assert not (FORBIDDEN_OUTPUT_KEYS & _walk_keys(result))


def test_degraded_dense_attachment_becomes_degraded_integration(monkeypatch) -> None:
    def degraded_attachment(*args, **kwargs):
        return {
            "attachment_schema": "sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1",
            "attachment_status": "degraded_missing_boundary_flags",
            "source_run_id": kwargs.get("source_run_id"),
            "sample_id": kwargs.get("sample_id", "sample_8u3"),
            "graph_summary": {
                "people_cluster_proxy_count": 1,
                "influence_core_proxy_count": 1,
                "content_aggregate_proxy_count": 1,
                "echobox_proxy_count": 1,
                "edge_count": 1,
                "timeline_bucket_count": 1,
            },
            "people_cluster_proxy_count": 1,
            "influence_core_proxy_count": 1,
            "content_aggregate_proxy_count": 1,
            "echobox_proxy_count": 1,
            "edge_count": 1,
            "timeline_bucket_count": 1,
            "recommended_visualization_mode": "dense_sandbox_proxy_graph",
            "boundary_flags": {flag: True for flag in REQUIRED_BOUNDARY_FLAGS if flag != "human_review_required"},
            "runtime_side_effects": {flag: False for flag in REQUIRED_SIDE_EFFECT_FLAGS},
            "warnings": ["missing_boundary_flags"],
            "blockers": [],
            "human_review_required": True,
        }

    monkeypatch.setattr(
        integration.adapter,
        "build_dense_graph_generated_run_attachment_from_evidence_items",
        degraded_attachment,
    )

    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        _fixture(),
        sample_id="sample_8u3",
    )

    assert result["integration_status"] == "degraded_dense_graph_attachment"
    assert result["integration_summary"]["frontend_ready"] is False
    assert result["integration_summary"]["route_ready"] is False
    assert "missing_boundary_flags" in result["warnings"]


def test_output_is_json_serializable_and_does_not_require_route_or_frontend() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(_fixture(), sample_id="sample_8u3")

    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert "sentigraph_opinion_ecosystem_generated_run_dense_graph_integration_v0_1" in encoded
    assert "route" not in result
    assert "frontend" not in result


def test_dense_graph_can_be_excluded_without_claiming_frontend_or_production_ready() -> None:
    result = integration.generate_opinion_ecosystem_run_with_dense_graph_attachment(
        _fixture(),
        sample_id="sample_8u3",
        include_dense_graph=False,
    )

    assert result["integration_status"] == "ready_for_backend_service_surface"
    assert result["dense_graph_attachment"] is None
    assert result["integration_summary"]["dense_graph_attached"] is False
    assert result["integration_summary"]["frontend_ready"] is False
    assert result["integration_summary"]["production_ready"] is False
