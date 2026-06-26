from __future__ import annotations

import inspect

from app.services import opinion_ecosystem_minimum_real_run as minimum_run


REQUIRED_BOUNDARY_FLAGS = {
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
    "not_full_thread",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_production_score",
    "human_review_required",
    "no_auto_execute",
    "no_generated_public_response",
}

REQUIRED_SIDE_EFFECT_FLAGS = {
    "called_real_api",
    "called_real_llm",
    "ran_collector",
    "accessed_private_collector",
    "read_real_exchange_dir",
    "fetched_url",
    "scraped_page",
    "parsed_evidence_items_file",
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

REQUIRED_MODULE_KEYS = {
    "ContentAggregate",
    "InfluenceCore",
    "EchoBox",
    "PeopleCluster",
    "ResponseStrategyComparisonV01",
}

FORBIDDEN_OUTPUT_KEYS = {
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
}


def _full_safe_fixture() -> dict:
    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": "fixture_8s2_full",
            "case_id": "case_8s2",
            "sample_id": "sample_8s2",
            "fixture_role": "unit_test_synthetic",
            "source_mode": "synthetic_fixture",
            "stage_id": "T4",
            "coverage_note": "selected synthetic fixture only",
            "selected_sample_only": True,
            "not_full_web": True,
            "not_full_platform": True,
        },
        "evidence_items_safe": [
            {
                "evidence_id": "evidence_001",
                "platform": "sample_forum",
                "provenance_type": "official_api_public",
                "verification_status": "verified_by_official_api",
                "trust_label": "high",
                "review_status": "approved",
                "duplicate_group_id": "dup_001",
                "duplicate_count": 1,
                "relevance_label": "strong_case_match",
                "recency_label": "inside_stage_window",
                "stance_hint": "support",
                "emotion_intensity_hint": 0.40,
                "source_url_present": True,
                "aggregate_ref": "agg_001",
                "influence_core_refs": ["core_official_001"],
                "echo_box_refs": ["echo_001"],
                "people_cluster_refs": ["cluster_mixed_001"],
            },
            {
                "evidence_id": "evidence_002",
                "platform": "sample_forum",
                "provenance_type": "manual_url_with_attestation",
                "trust_label": "medium",
                "review_status": "approved",
                "duplicate_group_id": "dup_002",
                "duplicate_count": 1,
                "relevance_label": "strong_case_match",
                "recency_label": "inside_stage_window",
                "stance_hint": "oppose",
                "emotion_intensity_hint": 0.50,
                "source_url_present": True,
                "aggregate_ref": "agg_001",
                "influence_core_refs": ["core_official_001"],
                "echo_box_refs": ["echo_001"],
                "people_cluster_refs": ["cluster_mixed_001"],
            },
        ],
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
                "core_id": "core_official_001",
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
                "influence_core_ids": ["core_official_001"],
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
                "cluster_id": "cluster_mixed_001",
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
                "influence_core_ids": ["core_official_001"],
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


def test_generated_run_contains_contract_identity_and_model_metadata() -> None:
    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(_full_safe_fixture())

    assert run["run_id"].startswith("minimum_real_run_")
    assert run["run_schema"] == "sentigraph_opinion_ecosystem_run_v0_1"
    assert run["run_status"] == "ready"
    assert run["case_id"] == "case_8s2"
    assert run["sample_id"] == "sample_8s2"
    assert run["input_package_id"] is None
    assert run["input_source_kind"] == "in_memory_safe_fixture"
    assert run["input_scope_note"] == "selected_sample_or_local_fixture_only"
    assert run["model_version"] == "0.1"
    assert run["coefficient_source"] == "mock_default"
    assert run["calibration_status"] == "uncalibrated"
    assert run["empirical_validation"] == "not_started"
    assert run["human_review_required"] is True


def test_generated_run_contains_required_boundaries_and_false_side_effects() -> None:
    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(_full_safe_fixture())

    assert REQUIRED_BOUNDARY_FLAGS <= set(run["boundary_flags"])
    for flag in REQUIRED_BOUNDARY_FLAGS:
        assert run["boundary_flags"][flag] is True

    assert REQUIRED_SIDE_EFFECT_FLAGS <= set(run["runtime_side_effects"])
    for flag in REQUIRED_SIDE_EFFECT_FLAGS:
        assert run["runtime_side_effects"][flag] is False


def test_generated_run_maps_all_calculator_modules_to_contract_keys() -> None:
    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(_full_safe_fixture())

    assert REQUIRED_MODULE_KEYS == set(run["module_outputs"])
    assert isinstance(run["module_outputs"]["ContentAggregate"], list)
    assert isinstance(run["module_outputs"]["InfluenceCore"], list)
    assert isinstance(run["module_outputs"]["EchoBox"], list)
    assert isinstance(run["module_outputs"]["PeopleCluster"], list)
    assert isinstance(run["module_outputs"]["ResponseStrategyComparisonV01"], list)


def test_blocked_fixture_does_not_produce_ready_run() -> None:
    fixture = _full_safe_fixture()
    fixture["evidence_items_safe"][0]["raw_author_id"] = "hidden"

    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(fixture)

    assert run["run_status"] == "blocked"
    assert run["blockers"]
    assert run["human_review_required"] is True


def test_auto_execute_remains_blocked_and_not_active_capability() -> None:
    fixture = _full_safe_fixture()
    fixture["response_strategy_candidates"][0]["execute_now"] = True

    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(fixture)

    assert run["run_status"] == "blocked"
    assert run["runtime_side_effects"]["auto_executed"] is False
    assert "execute_now" not in _walk_keys(run)


def test_unknown_future_platform_remains_manual_review_or_blocked() -> None:
    fixture = _full_safe_fixture()
    fixture["evidence_items_safe"][0]["platform"] = "future_forum"

    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(fixture)

    assert run["run_status"] in {"manual_review_required", "blocked"}
    assert run["run_status"] != "ready"
    assert run["human_review_required"] is True
    assert run["runtime_side_effects"]["called_real_api"] is False


def test_forbidden_output_fields_are_not_produced() -> None:
    run = minimum_run.generate_opinion_ecosystem_minimum_real_run(_full_safe_fixture())
    keys = _walk_keys(run)

    assert not (FORBIDDEN_OUTPUT_KEYS & keys)


def test_wrapper_source_has_no_file_io_network_runtime_or_api_route_tokens() -> None:
    source = inspect.getsource(minimum_run)
    forbidden_tokens = [
        "op" + "en(",
        "Path(",
        "read" + "_text",
        "write" + "_text",
        "json.load",
        "json.dump",
        "requests.",
        "httpx.",
        "urllib.",
        "fetch(",
        "axios.",
        "/api/v1",
        "FileResponse",
        "StreamingResponse",
        "evidence" + "_items.jsonl",
        "evidence" + "_items.csv",
    ]

    for token in forbidden_tokens:
        assert token not in source
