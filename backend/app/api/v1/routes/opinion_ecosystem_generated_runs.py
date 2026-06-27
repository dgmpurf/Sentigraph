from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from app.services.opinion_ecosystem_minimum_real_run import generate_opinion_ecosystem_minimum_real_run


router = APIRouter()

ALLOWED_SAMPLE_KEYS = {"mock_default", "helldivers_psn", "donglu_sunjihai_youth_football"}
ALLOWED_REQUEST_FIELDS = {"sample_key", "case_id", "sample_id"}
FORBIDDEN_REQUEST_FIELDS = {
    "exchange_dir",
    "package_root",
    "evidence_items",
    "evidence_items_path",
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
    "cookie",
    "cookies",
    "token",
    "tokens",
    "session",
    "sessions",
    "browser_profile",
    "browser_profile_path",
    "private_message",
    "private_messages",
    "raw_evidence_rows",
    "collector_internals",
    "publish_now",
    "send_now",
    "post_now",
    "execute_now",
    "auto_execute",
}


@router.post("/generated-runs/local-fixture")
def create_local_fixture_generated_run(payload: dict[str, Any]) -> dict[str, Any]:
    _validate_payload(payload)
    sample_key = str(payload.get("sample_key") or "mock_default")
    fixture = _build_safe_fixture(
        sample_key=sample_key,
        case_id=payload.get("case_id"),
        sample_id=payload.get("sample_id"),
    )
    return generate_opinion_ecosystem_minimum_real_run(fixture)


def _validate_payload(payload: object) -> None:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="request_body_must_be_object")

    keys = {str(key) for key in payload}
    forbidden = sorted(keys & FORBIDDEN_REQUEST_FIELDS)
    if forbidden:
        raise HTTPException(status_code=400, detail={"reason": "forbidden_request_fields", "fields": forbidden})

    unknown = sorted(keys - ALLOWED_REQUEST_FIELDS)
    if unknown:
        raise HTTPException(status_code=400, detail={"reason": "unsupported_request_fields", "fields": unknown})

    sample_key = str(payload.get("sample_key") or "mock_default")
    if sample_key not in ALLOWED_SAMPLE_KEYS:
        raise HTTPException(status_code=400, detail={"reason": "unsupported_sample_key", "sample_key": sample_key})


def _build_safe_fixture(sample_key: str, case_id: object = None, sample_id: object = None) -> dict[str, Any]:
    fixture_case_id = str(case_id or f"case_{sample_key}")
    fixture_sample_id = str(sample_id or f"sample_{sample_key}")
    fixture_id = f"fixture_8s4_{sample_key}"
    source_mode = f"{sample_key}_local_fixture"

    return {
        "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
        "fixture_metadata": {
            "fixture_id": fixture_id,
            "case_id": fixture_case_id,
            "sample_id": fixture_sample_id,
            "fixture_role": "route_contract_synthetic",
            "source_mode": source_mode,
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
