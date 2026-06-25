from __future__ import annotations

from collections.abc import Iterable
from math import log, sqrt
from typing import Any


SCHEMA = "sentigraph_opinion_ecosystem_mock_calculator_run_v0_1"
MODEL_NAME = "sentigraph_opinion_ecosystem_weight_model"
MODEL_VERSION = "0.1"
MODEL_STATUS = "8P_1_metadata_skeleton"
COEFFICIENT_SOURCE = "mock_default"
CALIBRATION_STATUS = "uncalibrated"
EMPIRICAL_VALIDATION = "not_started"
GENERATED_AT = "not_runtime_generated_in_8P_1"
SCOPE_NOTE = "selected_sample_or_local_fixture_only"
NOT_CALCULATED = "not_calculated_in_8P_1"

REQUIRED_METADATA_FIELDS = (
    "fixture_id",
    "case_id",
    "sample_id",
    "fixture_role",
    "source_mode",
    "stage_id",
    "coverage_note",
)

REQUIRED_TRUE_METADATA_FLAGS = (
    "selected_sample_only",
    "not_full_web",
    "not_full_platform",
)

REQUIRED_BOUNDARY_FLAGS = (
    "not_full_web",
    "not_full_platform",
    "not_official_verification",
    "not_causal_proof",
    "not_prediction",
    "not_personality_diagnosis",
    "not_individual_persuasion_scoring",
    "not_public_opinion_control",
    "not_auto_executed",
    "selected_sample_only",
    "evidence_not_truth",
    "human_review_required",
)

FORBIDDEN_FIELD_KEYS = {
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
    "profile_url",
    "private_message",
    "private_messages",
    "dm_content",
    "cookie",
    "cookies",
    "token",
    "tokens",
    "access_token",
    "refresh_token",
    "session",
    "sessions",
    "browser_profile",
    "browser_profile_path",
    "profile_path",
    "localstorage",
    "secret",
    "secrets",
    "api_key",
    "password",
    "raw_author_identifiers",
}

OVERCLAIM_KEYS = {
    "full_web_claim",
    "full_platform_claim",
    "official_verification_claim",
    "causal_proof_claim",
    "prediction_claim",
    "personality_diagnosis_claim",
    "individual_persuasion_scoring_claim",
    "public_opinion_control_claim",
}

PLATFORM_FIELD_KEYS = {
    "platform",
    "platform_hint",
    "source_platform",
    "source_platform_claim",
    "platform_claim",
}

UNKNOWN_PLATFORM_VALUES = {
    "future_forum",
    "unknown_platform",
    "experimental_platform",
    "unsupported_platform",
    "placeholder_platform",
    "unconfigured_platform",
}

TRUST_WEIGHTS = {
    "official_api_public": 1.00,
    "official_api_oauth": 0.95,
    "reviewed_public_parser": 0.80,
    "manual_url_with_attestation": 0.65,
    "data_vendor_attested": 0.55,
    "user_upload_with_source": 0.50,
    "search_discovery_candidate": 0.40,
    "manual_text_without_source": 0.30,
    "screenshot_transcription": 0.30,
    "mock_fixture": 0.25,
    "unknown_or_unclear_source": 0.20,
    "official_api": 1.00,
    "verified_by_official_api": 1.00,
    "data_vendor": 0.55,
    "user_upload": 0.50,
    "manual_url": 0.65,
    "manual_text": 0.30,
    "high": 0.80,
    "medium": 0.55,
    "medium_low": 0.45,
    "low": 0.30,
    "unverified": 0.20,
    "rejected": 0.00,
}

REVIEW_WEIGHTS = {
    "approved": 1.00,
    "not_reviewed": 0.70,
    "review_needed": 0.70,
    "needs_more_source": 0.55,
    "marked_weak": 0.45,
    "rejected": 0.00,
    "human_rejected": 0.00,
}

RELEVANCE_WEIGHTS = {
    "strong_case_match": 1.00,
    "partial_case_match": 0.60,
    "weak_case_match": 0.30,
    "off_topic": 0.00,
}

RECENCY_WEIGHTS = {
    "inside_stage_window": 1.00,
    "near_stage_window": 0.70,
    "outside_but_relevant": 0.40,
    "unknown_time": 0.60,
}

REJECTED_REVIEW_STATUSES = {"rejected", "human_rejected"}
REVIEW_NEEDED_STATUSES = {"not_reviewed", "review_needed", "needs_more_source"}
LOW_TRUST_LABELS = {"low", "unverified", "rejected"}
UNKNOWN_STANCE_VALUES = {"", "unknown", "unclear", "not_sure", "missing"}
DEFAULT_DUPLICATE_CAP = 20

SOURCE_IDENTITY_WEIGHTS = {
    "official_statement": 0.95,
    "recognized_media_report": 0.78,
    "media_report": 0.78,
    "expert_explanation": 0.72,
    "known_org_or_institution": 0.70,
    "kol_creator_content": 0.58,
    "ordinary_viral_content": 0.45,
    "forum_thread": 0.42,
    "community_comment_cluster": 0.38,
    "meme_deconstruction": 0.30,
    "unknown_source_core": 0.25,
    "low_trust_claim": 0.15,
    "faq_or_longform_explanation": 0.72,
    "correction_or_apology": 0.88,
    "progress_update": 0.82,
    "third_party_context": 0.70,
}

KNOWN_INFLUENCE_CORE_TYPES = {
    "official_statement",
    "media_report",
    "recognized_media_report",
    "expert_explanation",
    "known_org_or_institution",
    "kol_creator_content",
    "ordinary_viral_content",
    "forum_thread",
    "community_comment_cluster",
    "meme_deconstruction",
    "faq_or_longform_explanation",
    "correction_or_apology",
    "progress_update",
    "third_party_context",
    "low_trust_claim",
    "unknown_source_core",
}


def _iter_fields(value: Any, path: str = "") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}" if path else key_text
            yield child_path, key_text, child
            yield from _iter_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]" if path else f"[{index}]"
            yield from _iter_fields(child, child_path)


def _blocker(field: str, path: str, reason: str, category: str) -> dict[str, str]:
    return {
        "field": field,
        "path": path,
        "reason": reason,
        "category": category,
    }


def _warning(field: str, path: str, reason: str, category: str) -> dict[str, str]:
    return {
        "field": field,
        "path": path,
        "reason": reason,
        "category": category,
    }


def _is_truthy_claim(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "claimed", "enabled"}
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def _as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _label(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def clamp01(value: Any) -> float:
    number = _as_float(value)
    if number is None:
        return 0.0
    return max(0.0, min(1.0, number))


def log_norm(value: Any, cap: Any) -> float:
    number = max(0.0, _as_float(value) or 0.0)
    cap_number = max(0.0, _as_float(cap) or 0.0)
    if cap_number <= 0:
        return 0.0
    return clamp01(log(1 + number) / log(1 + cap_number))


def _component_value(source: dict[str, Any], *keys: str) -> float | None:
    nested = source.get("raw_metric_summary")
    for key in keys:
        value = source.get(key)
        if value is None and isinstance(nested, dict):
            value = nested.get(key)
        number = _as_float(value)
        if number is not None:
            return clamp01(number)
    return None


def _weighted_available(components: list[tuple[str, float | None, float]]) -> tuple[float, list[str]]:
    available_total = 0.0
    weighted_total = 0.0
    missing: list[str] = []
    for name, value, weight in components:
        if value is None:
            missing.append(name)
            continue
        available_total += weight
        weighted_total += clamp01(value) * weight
    if available_total <= 0:
        return 0.0, missing
    return clamp01(weighted_total / available_total), missing


def _is_rejected(evidence: dict[str, Any]) -> bool:
    return _label(evidence.get("review_status")) in REJECTED_REVIEW_STATUSES


def _eligible_evidence(evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [evidence for evidence in evidence_items if not _is_rejected(evidence)]


def _matching_evidence(aggregate: dict[str, Any], evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    aggregate_id = aggregate.get("aggregate_id")
    evidence_ids = aggregate.get("evidence_ids")
    if isinstance(evidence_ids, list) and evidence_ids:
        wanted = {str(evidence_id) for evidence_id in evidence_ids}
        return [evidence for evidence in evidence_items if str(evidence.get("evidence_id")) in wanted]
    if aggregate_id is None:
        return evidence_items
    matching = [evidence for evidence in evidence_items if evidence.get("aggregate_ref") == aggregate_id]
    if matching:
        return matching
    has_any_ref = any(evidence.get("aggregate_ref") for evidence in evidence_items)
    return [] if has_any_ref else evidence_items


def _duplicate_group_sizes(evidence_items: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for index, evidence in enumerate(evidence_items):
        group_id = str(evidence.get("duplicate_group_id") or evidence.get("evidence_id") or f"evidence_{index}")
        declared_count = int(max(1.0, _as_float(evidence.get("duplicate_count")) or 1.0))
        counts[group_id] = max(counts.get(group_id, 0) + 1, declared_count)
    return counts


def _duplicate_group_size(evidence: dict[str, Any], group_sizes: dict[str, int]) -> int:
    group_id = str(evidence.get("duplicate_group_id") or evidence.get("evidence_id") or "")
    declared_count = int(max(1.0, _as_float(evidence.get("duplicate_count")) or 1.0))
    return max(1, group_sizes.get(group_id, declared_count), declared_count)


def get_trust_weight(evidence: dict[str, Any]) -> float:
    trust_score = _as_float(evidence.get("trust_score"))
    if trust_score is not None:
        return clamp01(trust_score)
    for field in ("provenance_type", "acquisition_mode", "verification_status", "trust_label"):
        label = _label(evidence.get(field))
        if label in TRUST_WEIGHTS:
            return TRUST_WEIGHTS[label]
    return TRUST_WEIGHTS["unknown_or_unclear_source"]


def get_review_weight(evidence: dict[str, Any]) -> float:
    return REVIEW_WEIGHTS.get(_label(evidence.get("review_status")), REVIEW_WEIGHTS["not_reviewed"])


def get_dedup_weight(evidence: dict[str, Any], duplicate_group_size: int | None = None) -> float:
    group_size = duplicate_group_size
    if group_size is None:
        group_size = int(max(1.0, _as_float(evidence.get("duplicate_count")) or 1.0))
    if group_size <= 1:
        return 1.0
    return clamp01(1 / sqrt(group_size))


def get_relevance_weight(evidence: dict[str, Any]) -> float:
    label = _label(evidence.get("relevance_label"))
    if not label:
        return RELEVANCE_WEIGHTS["partial_case_match"]
    return RELEVANCE_WEIGHTS.get(label, RELEVANCE_WEIGHTS["partial_case_match"])


def get_recency_weight(evidence: dict[str, Any]) -> float:
    label = _label(evidence.get("recency_label"))
    if not label:
        return RECENCY_WEIGHTS["unknown_time"]
    return RECENCY_WEIGHTS.get(label, RECENCY_WEIGHTS["unknown_time"])


def calculate_evidence_base_weight(evidence: dict[str, Any], duplicate_group_size: int | None = None) -> float:
    if _is_rejected(evidence):
        return 0.0
    return clamp01(
        get_trust_weight(evidence)
        * get_review_weight(evidence)
        * get_dedup_weight(evidence, duplicate_group_size)
        * get_relevance_weight(evidence)
        * get_recency_weight(evidence)
    )


def calculate_coverage_quality(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    total = len(eligible)
    source_url_present_share = sum(1 for item in eligible if item.get("source_url_present") is True) / total
    reviewed_or_approved_share = sum(1 for item in eligible if _label(item.get("review_status")) == "approved") / total
    non_low_trust_share = sum(
        1
        for item in eligible
        if _label(item.get("trust_label")) not in LOW_TRUST_LABELS and get_trust_weight(item) > 0.30
    ) / total
    non_unknown_stance_share = sum(1 for item in eligible if _label(item.get("stance_hint")) not in UNKNOWN_STANCE_VALUES) / total
    return clamp01(
        0.35 * source_url_present_share
        + 0.25 * reviewed_or_approved_share
        + 0.20 * non_low_trust_share
        + 0.20 * non_unknown_stance_share
    )


def calculate_evidence_confidence(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    group_sizes = _duplicate_group_sizes(eligible)
    weighted_total = 0.0
    weight_total = 0.0
    for evidence in eligible:
        group_size = _duplicate_group_size(evidence, group_sizes)
        dedup_weight = get_dedup_weight(evidence, group_size)
        weighted_total += get_trust_weight(evidence) * get_review_weight(evidence) * dedup_weight
        weight_total += dedup_weight
    evidence_quality = weighted_total / weight_total if weight_total else 0.0
    coverage_quality = calculate_coverage_quality(eligible)
    return clamp01(0.65 * evidence_quality + 0.35 * coverage_quality)


def find_forbidden_fixture_fields(fixture: object) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path, key, _value in _iter_fields(fixture):
        if key.lower() in FORBIDDEN_FIELD_KEYS:
            findings.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="forbidden_identity_or_sensitive_field",
                    category="forbidden_field",
                )
            )
    return findings


def _find_response_strategy_blockers(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        key_lower = key.lower()
        value_is_auto = isinstance(value, str) and value.strip().lower() == "auto_execute"
        if key_lower == "auto_execute" or value_is_auto:
            blockers.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="auto_execute_is_forbidden",
                    category="response_strategy_blocker",
                )
            )
    return blockers


def _find_overclaim_blockers(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        if key.lower() in OVERCLAIM_KEYS and _is_truthy_claim(value):
            blockers.append(
                _blocker(
                    field=key,
                    path=path,
                    reason="overclaim_flag_is_forbidden",
                    category="overclaim_blocker",
                )
            )
    return blockers


def _find_unknown_platform_warnings(fixture: object) -> list[dict[str, str]]:
    warnings: list[dict[str, str]] = []
    for path, key, value in _iter_fields(fixture):
        if key.lower() not in PLATFORM_FIELD_KEYS or not isinstance(value, str):
            continue
        if value.strip().lower() in UNKNOWN_PLATFORM_VALUES:
            warnings.append(
                _warning(
                    field=key,
                    path=path,
                    reason="unknown_or_future_platform_requires_manual_review",
                    category="unknown_or_future_platform",
                )
            )
    return warnings


def _validate_required_fixture_shape(fixture: object) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    if not isinstance(fixture, dict):
        return [
            _blocker(
                field="fixture",
                path="fixture",
                reason="fixture_must_be_dict",
                category="fixture_contract_blocker",
            )
        ]

    metadata = fixture.get("fixture_metadata")
    if not isinstance(metadata, dict):
        return [
            _blocker(
                field="fixture_metadata",
                path="fixture_metadata",
                reason="fixture_metadata_must_be_dict",
                category="fixture_contract_blocker",
            )
        ]

    for field in REQUIRED_METADATA_FIELDS:
        if metadata.get(field) in (None, ""):
            blockers.append(
                _blocker(
                    field=field,
                    path=f"fixture_metadata.{field}",
                    reason="required_fixture_metadata_missing",
                    category="fixture_contract_blocker",
                )
            )

    for flag in REQUIRED_TRUE_METADATA_FLAGS:
        if metadata.get(flag) is not True:
            blockers.append(
                _blocker(
                    field=flag,
                    path=f"fixture_metadata.{flag}",
                    reason="required_fixture_boundary_flag_missing_or_false",
                    category="fixture_contract_blocker",
                )
            )

    return blockers


def validate_mock_fixture_contract(fixture: dict) -> dict[str, Any]:
    shape_blockers = _validate_required_fixture_shape(fixture)
    forbidden_fields = find_forbidden_fixture_fields(fixture)
    overclaim_blockers = _find_overclaim_blockers(fixture)
    response_strategy_blockers = _find_response_strategy_blockers(fixture)
    unknown_platform_warnings = _find_unknown_platform_warnings(fixture)

    blockers = [
        *shape_blockers,
        *forbidden_fields,
        *overclaim_blockers,
        *response_strategy_blockers,
    ]
    warnings = [*unknown_platform_warnings]

    if blockers:
        status = "blocked"
    elif warnings:
        status = "manual_review_required"
    else:
        status = "metadata_ready"

    return {
        "status": status,
        "compatibility_status": status,
        "human_review_required": True,
        "blockers": blockers,
        "warnings": warnings,
        "forbidden_fields": forbidden_fields,
        "overclaim_blockers": overclaim_blockers,
        "response_strategy_blockers": response_strategy_blockers,
        "unknown_platform_warnings": unknown_platform_warnings,
        "forbidden_field_count": len(forbidden_fields),
        "overclaim_blocker_count": len(overclaim_blockers),
        "response_strategy_blocker_count": len(response_strategy_blockers),
        "unknown_platform_warning_count": len(unknown_platform_warnings),
    }


def _fixture_metadata(fixture: dict) -> dict[str, Any]:
    if isinstance(fixture, dict) and isinstance(fixture.get("fixture_metadata"), dict):
        return fixture["fixture_metadata"]
    return {}


def _fixture_value(fixture: dict, field: str, fallback: str) -> str:
    value = _fixture_metadata(fixture).get(field, fallback)
    if value in (None, ""):
        return fallback
    return str(value)


def _boundary_flags() -> dict[str, bool]:
    return {
        "not_full_web": True,
        "not_full_platform": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_personality_diagnosis": True,
        "not_individual_persuasion_scoring": True,
        "not_public_opinion_control": True,
        "not_auto_executed": True,
        "selected_sample_only": True,
        "evidence_not_truth": True,
        "human_review_required": True,
    }


def _runtime_side_effects() -> dict[str, bool]:
    return {
        "real_api_calls": False,
        "real_llm_calls": False,
        "url_fetching": False,
        "scraping": False,
        "collector_jobs_run": False,
        "evidence_items_read": False,
        "evidence_items_parsed": False,
        "evidence_items_imported": False,
        "evidence_layer_written": False,
        "production_case_created": False,
        "analysis_run_created": False,
        "b_end_report_generated": False,
        "sandbox_fixture_generated": False,
        "public_event_page_generated": False,
        "auto_execute": False,
    }


def _module_outputs() -> dict[str, str]:
    return {
        "content_aggregate": NOT_CALCULATED,
        "influence_core": NOT_CALCULATED,
        "echo_box": NOT_CALCULATED,
        "people_cluster": NOT_CALCULATED,
        "response_strategy": NOT_CALCULATED,
    }


def _module_outputs_with_content_aggregate(outputs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "content_aggregate": outputs,
        "influence_core": "not_calculated_in_8P_2",
        "echo_box": "not_calculated_in_8P_2",
        "people_cluster": "not_calculated_in_8P_2",
        "response_strategy": "not_calculated_in_8P_2",
    }


def _module_outputs_with_content_and_influence(
    content_outputs: list[dict[str, Any]],
    influence_outputs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "content_aggregate": content_outputs if content_outputs else "not_calculated_in_8P_3",
        "influence_core": influence_outputs,
        "echo_box": "not_calculated_in_8P_3",
        "people_cluster": "not_calculated_in_8P_3",
        "response_strategy": "not_calculated_in_8P_3",
    }


def _zero_content_scores() -> dict[str, float]:
    return {
        "sample_heat_score": 0.0,
        "heat_confidence_adjusted": 0.0,
        "sample_controversy_score": 0.0,
        "discussion_risk_score": 0.0,
        "review_risk_score": 0.0,
        "overall_risk_score": 0.0,
        "evidence_confidence_score": 0.0,
    }


def _content_boundary_flags() -> dict[str, bool]:
    return {
        "not_real_hotlist": True,
        "not_full_web": True,
        "not_full_platform": True,
        "not_official_verification": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "evidence_not_truth": True,
        "human_review_required": True,
    }


def _content_warnings() -> dict[str, list[str]]:
    return {
        "low_confidence_warnings": [],
        "low_trust_warnings": [],
        "review_needed_warnings": [],
        "duplicate_folded_warnings": [],
        "rejected_excluded_warnings": [],
        "missing_component_warnings": [],
        "insufficient_data_warnings": [],
        "model_card_warnings": [
            "selected_sample_only",
            "not_real_hotlist",
            "evidence_not_truth",
            "human_review_required",
        ],
    }


def _low_trust_share(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    return sum(
        1
        for evidence in eligible
        if _label(evidence.get("trust_label")) in LOW_TRUST_LABELS or get_trust_weight(evidence) <= 0.30
    ) / len(eligible)


def _review_needed_share(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    return sum(1 for evidence in eligible if _label(evidence.get("review_status")) in REVIEW_NEEDED_STATUSES) / len(eligible)


def _missing_source_url_share(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    return sum(1 for evidence in eligible if evidence.get("source_url_present") is not True) / len(eligible)


def _sensitive_privacy_flag_share(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    sensitive_terms = {"sensitive", "privacy", "minor", "family", "private"}
    count = 0
    for evidence in eligible:
        risk_flags = evidence.get("risk_flags")
        if not isinstance(risk_flags, list):
            continue
        labels = {_label(flag) for flag in risk_flags}
        if labels & sensitive_terms:
            count += 1
    return count / len(eligible)


def _stance_distribution(evidence_items: list[dict[str, Any]], aggregate: dict[str, Any]) -> dict[str, float]:
    aggregate_distribution = aggregate.get("stance_distribution")
    if isinstance(aggregate_distribution, dict):
        support = max(0.0, _as_float(aggregate_distribution.get("support")) or 0.0)
        oppose = max(0.0, _as_float(aggregate_distribution.get("oppose")) or 0.0)
        neutral = max(0.0, _as_float(aggregate_distribution.get("neutral")) or 0.0)
        mixed = max(0.0, _as_float(aggregate_distribution.get("mixed")) or 0.0)
        unknown = max(0.0, _as_float(aggregate_distribution.get("unknown")) or 0.0)
        support += mixed * 0.5
        oppose += mixed * 0.5
    else:
        support = oppose = neutral = unknown = 0.0
        for evidence in _eligible_evidence(evidence_items):
            stance = _label(evidence.get("stance_hint"))
            if stance == "support":
                support += 1
            elif stance == "oppose":
                oppose += 1
            elif stance == "mixed":
                support += 0.5
                oppose += 0.5
            elif stance == "neutral":
                neutral += 1
            else:
                unknown += 1

    total = support + oppose + neutral + unknown
    if total <= 0:
        return {"support": 0.0, "oppose": 0.0, "neutral": 0.0, "unknown": 1.0}
    return {
        "support": clamp01(support / total),
        "oppose": clamp01(oppose / total),
        "neutral": clamp01(neutral / total),
        "unknown": clamp01(unknown / total),
    }


def _average_emotion(evidence_items: list[dict[str, Any]]) -> float | None:
    values = [clamp01(value) for value in (item.get("emotion_intensity_hint") for item in _eligible_evidence(evidence_items)) if _as_float(value) is not None]
    if not values:
        return None
    return clamp01(sum(values) / len(values))


def _derive_spread(evidence_items: list[dict[str, Any]]) -> float | None:
    platforms = {_label(evidence.get("platform")) for evidence in _eligible_evidence(evidence_items) if _label(evidence.get("platform"))}
    if not platforms:
        return None
    return log_norm(len(platforms), 8)


def _repetition_signal(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    group_sizes = _duplicate_group_sizes(eligible)
    max_group_size = max((_duplicate_group_size(evidence, group_sizes) for evidence in eligible), default=1)
    return log_norm(max_group_size, DEFAULT_DUPLICATE_CAP)


def _heat_components(
    aggregate: dict[str, Any],
    evidence_items: list[dict[str, Any]],
) -> tuple[dict[str, float | None], float, list[str]]:
    ready_count = len(_eligible_evidence(evidence_items))
    components = {
        "volume_score": _component_value(aggregate, "volume_score"),
        "interaction_score": _component_value(aggregate, "interaction_score"),
        "growth_score": _component_value(aggregate, "growth_score"),
        "emotion_intensity": _component_value(aggregate, "emotion_intensity"),
        "spread_score": _component_value(aggregate, "spread_score"),
        "repetition_signal": _component_value(aggregate, "repetition_signal"),
    }
    if components["volume_score"] is None and ready_count:
        components["volume_score"] = log_norm(ready_count, DEFAULT_DUPLICATE_CAP)
    if components["emotion_intensity"] is None:
        components["emotion_intensity"] = _average_emotion(evidence_items)
    if components["spread_score"] is None:
        components["spread_score"] = _derive_spread(evidence_items)
    if components["repetition_signal"] is None:
        components["repetition_signal"] = _repetition_signal(evidence_items)

    score, missing = _weighted_available(
        [
            ("volume_score", components["volume_score"], 0.30),
            ("interaction_score", components["interaction_score"], 0.20),
            ("growth_score", components["growth_score"], 0.15),
            ("emotion_intensity", components["emotion_intensity"], 0.15),
            ("spread_score", components["spread_score"], 0.10),
            ("repetition_signal", components["repetition_signal"], 0.10),
        ]
    )
    return components, score, missing


def _controversy_score(
    aggregate: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    heat_components: dict[str, float | None],
    low_trust_share: float,
) -> tuple[float, dict[str, Any], list[str]]:
    stance = _stance_distribution(evidence_items, aggregate)
    support = stance["support"]
    oppose = stance["oppose"]
    unknown = stance["unknown"]
    conflict_mass = support + oppose
    balance = 1 - abs(support - oppose) / (conflict_mass + 0.000001)
    known_ratio = 1 - unknown
    polarization = clamp01(conflict_mass * balance * sqrt(max(0.0, known_ratio)))

    emotion = heat_components.get("emotion_intensity")
    cross_stance = _component_value(aggregate, "cross_stance_interaction_score", "cross_stance_proxy")
    divergence = _component_value(aggregate, "narrative_divergence_score", "narrative_divergence")
    repetition = heat_components.get("repetition_signal")
    low_trust_component = clamp01(low_trust_share * polarization)

    score, missing = _weighted_available(
        [
            ("polarization", polarization, 0.30),
            ("emotion_intensity", emotion, 0.20),
            ("cross_stance_interaction", cross_stance, 0.15),
            ("narrative_divergence", divergence, 0.15),
            ("repetition_signal", repetition, 0.10),
            ("low_trust_polarization", low_trust_component, 0.10),
        ]
    )
    components = {
        "stance_distribution": stance,
        "polarization": polarization,
        "conflict_mass": clamp01(conflict_mass),
        "balance": clamp01(balance),
        "known_ratio": clamp01(known_ratio),
        "cross_stance_interaction": cross_stance,
        "narrative_divergence": divergence,
        "low_trust_polarization": low_trust_component,
    }
    return score, components, missing


def _discussion_risk_score(
    aggregate: dict[str, Any],
    observed_heat: float,
    controversy: float,
    heat_components: dict[str, float | None],
) -> tuple[float, dict[str, float | None], list[str]]:
    components = {
        "observed_heat": observed_heat,
        "controversy": controversy,
        "emotion_intensity": heat_components.get("emotion_intensity"),
        "spread_score": heat_components.get("spread_score"),
        "issue_sensitivity": _component_value(aggregate, "issue_sensitivity", "issue_sensitivity_score"),
        "response_gap": _component_value(aggregate, "response_gap", "response_gap_score"),
    }
    score, missing = _weighted_available(
        [
            ("observed_heat", components["observed_heat"], 0.25),
            ("controversy", components["controversy"], 0.25),
            ("emotion_intensity", components["emotion_intensity"], 0.15),
            ("spread_score", components["spread_score"], 0.15),
            ("issue_sensitivity", components["issue_sensitivity"], 0.10),
            ("response_gap", components["response_gap"], 0.10),
        ]
    )
    return score, components, missing


def _review_risk_score(
    evidence_confidence: float,
    low_trust_share: float,
    review_needed_share: float,
    missing_source_url_share: float,
    sensitive_privacy_share: float,
) -> tuple[float, dict[str, float]]:
    components = {
        "confidence_gap": clamp01(1 - evidence_confidence),
        "low_trust_share": clamp01(low_trust_share),
        "review_needed_share": clamp01(review_needed_share),
        "missing_source_url_share": clamp01(missing_source_url_share),
        "sensitive_privacy_flag_share": clamp01(sensitive_privacy_share),
    }
    score = clamp01(
        0.30 * components["confidence_gap"]
        + 0.25 * components["low_trust_share"]
        + 0.20 * components["review_needed_share"]
        + 0.15 * components["missing_source_url_share"]
        + 0.10 * components["sensitive_privacy_flag_share"]
    )
    return score, components


def _content_evidence_mass(evidence_items: list[dict[str, Any]]) -> dict[str, int]:
    eligible = _eligible_evidence(evidence_items)
    groups = {
        str(evidence.get("duplicate_group_id") or evidence.get("evidence_id") or index)
        for index, evidence in enumerate(eligible)
    }
    return {
        "evidence_count": len(evidence_items),
        "analysis_ready_evidence_count": len(eligible),
        "rejected_excluded_count": len(evidence_items) - len(eligible),
        "duplicate_group_count": len(groups),
        "low_trust_count": sum(
            1
            for evidence in eligible
            if _label(evidence.get("trust_label")) in LOW_TRUST_LABELS or get_trust_weight(evidence) <= 0.30
        ),
        "review_needed_count": sum(1 for evidence in eligible if _label(evidence.get("review_status")) in REVIEW_NEEDED_STATUSES),
    }


def calculate_content_aggregate_weight(
    aggregate: dict[str, Any],
    evidence_items: list[dict[str, Any]],
) -> dict[str, Any]:
    aggregate_id = str(aggregate.get("aggregate_id") or "aggregate_unknown")
    matched_evidence = _matching_evidence(aggregate, evidence_items)
    eligible = _eligible_evidence(matched_evidence)
    warnings = _content_warnings()
    evidence_mass = _content_evidence_mass(matched_evidence)

    if evidence_mass["rejected_excluded_count"]:
        warnings["rejected_excluded_warnings"].append("rejected_evidence_excluded_from_content_aggregate_scores")
    if not eligible:
        warnings["insufficient_data_warnings"].append("no_analysis_ready_evidence_for_aggregate")
        return {
            "schema": "sentigraph_content_aggregate_weight_v0_1",
            "aggregate_id": aggregate_id,
            "model_status": "8P_2_content_aggregate_formula",
            "coefficient_source": COEFFICIENT_SOURCE,
            "calibration_status": CALIBRATION_STATUS,
            "empirical_validation": EMPIRICAL_VALIDATION,
            "sample_scope": SCOPE_NOTE,
            "evidence_mass": evidence_mass,
            "scores": _zero_content_scores(),
            "components": {
                "heat_components": {},
                "controversy_components": {},
                "discussion_risk_components": {},
                "review_risk_components": {},
                "coverage_quality": 0.0,
                "stance_distribution": {"support": 0.0, "oppose": 0.0, "neutral": 0.0, "unknown": 1.0},
                "repetition_signal": 0.0,
                "low_trust_share": 0.0,
                "review_needed_share": 0.0,
                "missing_source_url_share": 0.0,
            },
            "quality_flags": ["selected_sample_only", "uncalibrated", "mock_default_coefficients", "evidence_not_truth", "not_real_hotlist"],
            "warnings": warnings,
            "explanation": ["No analysis-ready evidence matched this ContentAggregate."],
            "boundary_flags": _content_boundary_flags(),
        }

    duplicate_present = any((_as_float(evidence.get("duplicate_count")) or 1.0) > 1 for evidence in eligible)
    if duplicate_present:
        warnings["duplicate_folded_warnings"].append("duplicate_count_used_only_as_bounded_repetition_signal")

    evidence_confidence = calculate_evidence_confidence(eligible)
    coverage_quality = calculate_coverage_quality(eligible)
    low_trust_share = _low_trust_share(eligible)
    review_needed_share = _review_needed_share(eligible)
    missing_source_url_share = _missing_source_url_share(eligible)
    sensitive_share = _sensitive_privacy_flag_share(eligible)

    if evidence_confidence < 0.45:
        warnings["low_confidence_warnings"].append("low_evidence_confidence_downgrades_conclusions")
    if evidence_mass["low_trust_count"]:
        warnings["low_trust_warnings"].append("low_trust_evidence_lowers_confidence")
    if evidence_mass["review_needed_count"]:
        warnings["review_needed_warnings"].append("review_needed_evidence_raises_review_risk")

    heat_components, observed_heat, heat_missing = _heat_components(aggregate, eligible)
    controversy, controversy_components, controversy_missing = _controversy_score(
        aggregate=aggregate,
        evidence_items=eligible,
        heat_components=heat_components,
        low_trust_share=low_trust_share,
    )
    discussion_risk, discussion_components, discussion_missing = _discussion_risk_score(
        aggregate=aggregate,
        observed_heat=observed_heat,
        controversy=controversy,
        heat_components=heat_components,
    )
    review_risk, review_components = _review_risk_score(
        evidence_confidence=evidence_confidence,
        low_trust_share=low_trust_share,
        review_needed_share=review_needed_share,
        missing_source_url_share=missing_source_url_share,
        sensitive_privacy_share=sensitive_share,
    )
    overall_risk = clamp01(0.70 * discussion_risk + 0.30 * review_risk)
    heat_confidence_adjusted = clamp01(observed_heat * (0.60 + 0.40 * evidence_confidence))

    for component in [*heat_missing, *controversy_missing, *discussion_missing]:
        if component not in warnings["missing_component_warnings"]:
            warnings["missing_component_warnings"].append(component)

    scores = {
        "sample_heat_score": observed_heat,
        "heat_confidence_adjusted": heat_confidence_adjusted,
        "sample_controversy_score": controversy,
        "discussion_risk_score": discussion_risk,
        "review_risk_score": review_risk,
        "overall_risk_score": overall_risk,
        "evidence_confidence_score": evidence_confidence,
    }
    components = {
        "heat_components": heat_components,
        "controversy_components": controversy_components,
        "discussion_risk_components": discussion_components,
        "review_risk_components": review_components,
        "coverage_quality": coverage_quality,
        "stance_distribution": controversy_components["stance_distribution"],
        "repetition_signal": heat_components.get("repetition_signal") or 0.0,
        "low_trust_share": low_trust_share,
        "review_needed_share": review_needed_share,
        "missing_source_url_share": missing_source_url_share,
    }
    explanation = [
        "ContentAggregate scores use selected-sample metadata only.",
        "Scores are uncalibrated mock-default heuristics.",
        "Evidence is evidence, not truth.",
    ]

    return {
        "schema": "sentigraph_content_aggregate_weight_v0_1",
        "aggregate_id": aggregate_id,
        "model_status": "8P_2_content_aggregate_formula",
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "sample_scope": SCOPE_NOTE,
        "evidence_mass": evidence_mass,
        "scores": scores,
        "components": components,
        "quality_flags": ["selected_sample_only", "uncalibrated", "mock_default_coefficients", "evidence_not_truth", "not_real_hotlist"],
        "warnings": warnings,
        "explanation": explanation,
        "boundary_flags": _content_boundary_flags(),
    }


def calculate_all_content_aggregate_weights(fixture: dict) -> list[dict[str, Any]]:
    aggregates = fixture.get("content_aggregates") if isinstance(fixture, dict) else None
    evidence_items = fixture.get("evidence_items_safe") if isinstance(fixture, dict) else None
    if not isinstance(aggregates, list) or not aggregates:
        return []
    safe_evidence = [item for item in evidence_items if isinstance(item, dict)] if isinstance(evidence_items, list) else []
    return [
        calculate_content_aggregate_weight(aggregate, safe_evidence)
        for aggregate in aggregates
        if isinstance(aggregate, dict)
    ]


def _influence_core_type(core: dict[str, Any]) -> str:
    core_type = _label(core.get("core_type"))
    if core_type in KNOWN_INFLUENCE_CORE_TYPES:
        return core_type
    return "unknown_source_core"


def get_source_identity_weight(core: dict[str, Any]) -> float:
    for field in ("source_identity_hint", "core_type"):
        label = _label(core.get(field))
        if label in SOURCE_IDENTITY_WEIGHTS:
            return SOURCE_IDENTITY_WEIGHTS[label]
    return SOURCE_IDENTITY_WEIGHTS["unknown_source_core"]


def get_influencecore_associated_evidence(
    core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    core_id = str(core.get("core_id") or "")
    raw_ids = core.get("associated_evidence_ids")
    wanted_ids = {str(item) for item in raw_ids if item not in (None, "")} if isinstance(raw_ids, list) else set()
    associated: list[dict[str, Any]] = []

    for evidence in evidence_items:
        evidence_id = str(evidence.get("evidence_id") or "")
        refs = evidence.get("influence_core_refs")
        if isinstance(refs, list):
            ref_ids = {str(ref) for ref in refs}
        elif refs in (None, ""):
            ref_ids = set()
        else:
            ref_ids = {str(refs)}

        if evidence_id in wanted_ids or (core_id and core_id in ref_ids):
            associated.append(evidence)

    return associated


def _mean(values: list[float]) -> float:
    if not values:
        return 0.0
    return clamp01(sum(clamp01(value) for value in values) / len(values))


def _hint(core: dict[str, Any], *keys: str) -> float | None:
    for key in keys:
        value = _as_float(core.get(key))
        if value is not None:
            return clamp01(value)
    return None


def _safe_metric_sum(evidence_items: list[dict[str, Any]], *keys: str) -> float | None:
    total = 0.0
    found = False
    for evidence in evidence_items:
        nested = evidence.get("raw_metric_summary")
        for key in keys:
            value = evidence.get(key)
            if value is None and isinstance(nested, dict):
                value = nested.get(key)
            number = _as_float(value)
            if number is not None:
                total += max(0.0, number)
                found = True
                break
    return total if found else None


def _has_risk_flag(core: dict[str, Any], *terms: str) -> bool:
    flags = core.get("risk_flags")
    if not isinstance(flags, list):
        return False
    labels = {_label(flag) for flag in flags}
    return any(term in label for label in labels for term in terms)


def _influence_warnings() -> dict[str, list[str]]:
    return {
        "low_confidence_warnings": [],
        "low_trust_warnings": [],
        "review_needed_warnings": [],
        "duplicate_folded_warnings": [],
        "rejected_excluded_warnings": [],
        "missing_component_warnings": [],
        "insufficient_data_warnings": [],
        "unknown_core_type_warnings": [],
        "model_card_warnings": [
            "selected_sample_only",
            "uncalibrated",
            "mock_default_coefficients",
            "evidence_not_truth",
            "human_review_required",
            "not_official_verification",
            "not_people_cluster",
        ],
    }


def _influence_boundary_flags() -> dict[str, bool]:
    return {
        "not_official_verification": True,
        "not_truth_score": True,
        "not_causal_proof": True,
        "not_prediction": True,
        "not_persuasion_probability": True,
        "not_people_cluster": True,
        "not_real_person": True,
        "evidence_not_truth": True,
        "human_review_required": True,
    }


def _influence_zero_scores() -> dict[str, float]:
    return {
        "factual_credibility": 0.0,
        "narrative_resonance": 0.0,
        "sample_exposure": 0.0,
        "bridge_potential": 0.0,
        "backlash_risk": 0.0,
        "core_strength": 0.0,
        "attention_amplification": 0.0,
        "amplification_score": 0.0,
        "credibility_adjusted_influence_score": 0.0,
        "deescalation_potential": 0.0,
        "core_risk": 0.0,
    }


def _influence_evidence_mass(evidence_items: list[dict[str, Any]]) -> dict[str, int]:
    eligible = _eligible_evidence(evidence_items)
    return {
        "evidence_count": len(evidence_items),
        "analysis_ready_evidence_count": len(eligible),
        "rejected_excluded_count": len(evidence_items) - len(eligible),
        "low_trust_count": sum(
            1
            for evidence in eligible
            if _label(evidence.get("trust_label")) in LOW_TRUST_LABELS or get_trust_weight(evidence) <= 0.30
        ),
        "review_needed_count": sum(1 for evidence in eligible if _label(evidence.get("review_status")) in REVIEW_NEEDED_STATUSES),
        "associated_evidence_count": len(evidence_items),
    }


def _source_url_present_share(evidence_items: list[dict[str, Any]]) -> float:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        return 0.0
    return sum(1 for evidence in eligible if evidence.get("source_url_present") is True) / len(eligible)


def _privacy_safety_value(core: dict[str, Any]) -> float:
    explicit = _as_float(core.get("privacy_safety_pass"))
    if explicit is not None:
        return clamp01(explicit)
    if _has_risk_flag(core, "privacy", "sensitive", "minor", "private"):
        return 0.30
    return 1.0


def _penalty_value(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    evidence_count = len(evidence_items)
    rejected_share = 0.0 if evidence_count == 0 else (evidence_count - len(_eligible_evidence(evidence_items))) / evidence_count
    penalty = 0.15 * rejected_share
    if _influence_core_type(core) == "low_trust_claim":
        penalty += 0.20
    if _has_risk_flag(core, "privacy", "sensitive", "minor", "private"):
        penalty += 0.15
    penalty += 0.10 * (_hint(core, "contradiction_risk_hint") or 0.0)
    return clamp01(penalty)


def _factual_credibility_detail(
    core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    warnings: dict[str, list[str]],
) -> tuple[float, dict[str, float]]:
    eligible = _eligible_evidence(evidence_items)
    if not eligible:
        warnings["insufficient_data_warnings"].append("no_analysis_ready_evidence_for_influencecore")
        return 0.0, {
            "source_identity_weight": get_source_identity_weight(core),
            "evidence_trust_mean": 0.0,
            "review_quality": 0.0,
            "source_transparency": 0.0,
            "cross_source_consistency": 0.0,
            "privacy_safety_pass": _privacy_safety_value(core),
            "penalty": 0.0,
        }

    source_transparency = _hint(core, "source_transparency_hint")
    if source_transparency is None:
        source_transparency = _source_url_present_share(eligible)
        warnings["missing_component_warnings"].append("source_transparency_hint")

    cross_source_consistency = _hint(core, "cross_source_consistency_hint")
    if cross_source_consistency is None:
        cross_source_consistency = 0.50
        warnings["missing_component_warnings"].append("cross_source_consistency_hint")

    components = {
        "source_identity_weight": get_source_identity_weight(core),
        "evidence_trust_mean": _mean([get_trust_weight(evidence) for evidence in eligible]),
        "review_quality": _mean([get_review_weight(evidence) for evidence in eligible]),
        "source_transparency": clamp01(source_transparency),
        "cross_source_consistency": clamp01(cross_source_consistency),
        "privacy_safety_pass": _privacy_safety_value(core),
        "penalty": _penalty_value(core, evidence_items),
    }
    score = clamp01(
        0.28 * components["source_identity_weight"]
        + 0.24 * components["evidence_trust_mean"]
        + 0.18 * components["review_quality"]
        + 0.14 * components["source_transparency"]
        + 0.10 * components["cross_source_consistency"]
        + 0.06 * components["privacy_safety_pass"]
        - components["penalty"]
    )
    return score, components


def calculate_factual_credibility(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    score, _components = _factual_credibility_detail(core, get_influencecore_associated_evidence(core, evidence_items), warnings)
    return score


def _narrative_resonance_detail(
    core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    warnings: dict[str, list[str]],
) -> tuple[float, dict[str, float]]:
    eligible = _eligible_evidence(evidence_items)
    clarity = _hint(core, "clarity_hint")
    novelty = _hint(core, "novelty_hint")
    emotional_charge = _hint(core, "emotional_charge_hint")
    repetition = _hint(core, "repetition_hint")
    identity_relevance = _hint(core, "identity_or_group_relevance_hint")
    meme_density = _hint(core, "meme_or_symbolic_density_hint")

    if clarity is None:
        clarity = 0.50
        warnings["missing_component_warnings"].append("clarity_hint")
    if novelty is None:
        novelty = 0.50
        warnings["missing_component_warnings"].append("novelty_hint")
    if emotional_charge is None:
        emotional_charge = _average_emotion(eligible)
        if emotional_charge is None:
            emotional_charge = 0.35
            warnings["missing_component_warnings"].append("emotional_charge_hint")
    if repetition is None:
        repetition = _repetition_signal(eligible)
        warnings["missing_component_warnings"].append("repetition_hint")
    if identity_relevance is None:
        identity_relevance = 0.50
        warnings["missing_component_warnings"].append("identity_or_group_relevance_hint")
    if meme_density is None:
        meme_density = 1.0 if _influence_core_type(core) == "meme_deconstruction" else 0.35
        warnings["missing_component_warnings"].append("meme_or_symbolic_density_hint")

    components = {
        "clarity_score": clamp01(clarity),
        "emotional_charge": clamp01(emotional_charge),
        "repetition_signal": clamp01(repetition),
        "novelty_score": clamp01(novelty),
        "identity_or_group_relevance_proxy": clamp01(identity_relevance),
        "meme_or_symbolic_density": clamp01(meme_density),
    }
    score = clamp01(
        0.22 * components["clarity_score"]
        + 0.20 * components["emotional_charge"]
        + 0.18 * components["repetition_signal"]
        + 0.15 * components["novelty_score"]
        + 0.15 * components["identity_or_group_relevance_proxy"]
        + 0.10 * components["meme_or_symbolic_density"]
    )
    return score, components


def calculate_narrative_resonance(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    score, _components = _narrative_resonance_detail(core, get_influencecore_associated_evidence(core, evidence_items), warnings)
    return score


def _sample_exposure_detail(
    _core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    warnings: dict[str, list[str]],
) -> tuple[float, dict[str, float | None]]:
    eligible = _eligible_evidence(evidence_items)
    weighted_mentions = sum(calculate_evidence_base_weight(evidence) for evidence in eligible)
    weighted_replies = _safe_metric_sum(eligible, "reply_count", "reply_proxy", "weighted_replies")
    weighted_shares = _safe_metric_sum(eligible, "share_count", "repost_count", "weighted_shares_or_reposts")
    platform_spread = _derive_spread(eligible)
    source_spread = log_norm(sum(1 for evidence in eligible if evidence.get("source_url_present") is True), 8)

    if weighted_replies is None:
        warnings["missing_component_warnings"].append("weighted_replies")
    if weighted_shares is None:
        warnings["missing_component_warnings"].append("weighted_shares_or_reposts")
    if platform_spread is None:
        warnings["missing_component_warnings"].append("platform_spread")

    components = {
        "weighted_mentions": log_norm(weighted_mentions, DEFAULT_DUPLICATE_CAP),
        "weighted_replies": log_norm(weighted_replies, 100) if weighted_replies is not None else None,
        "weighted_shares_or_reposts": log_norm(weighted_shares, 100) if weighted_shares is not None else None,
        "platform_spread": platform_spread,
        "source_spread": source_spread,
    }
    score, _missing = _weighted_available(
        [
            ("weighted_mentions", components["weighted_mentions"], 0.35),
            ("weighted_replies", components["weighted_replies"], 0.20),
            ("weighted_shares_or_reposts", components["weighted_shares_or_reposts"], 0.15),
            ("platform_spread", components["platform_spread"], 0.15),
            ("source_spread", components["source_spread"], 0.15),
        ]
    )
    return score, components


def calculate_sample_exposure(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    score, _components = _sample_exposure_detail(core, get_influencecore_associated_evidence(core, evidence_items), warnings)
    return score


def _bridge_potential_detail(
    core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
    factual_credibility: float,
    warnings: dict[str, list[str]],
) -> tuple[float, dict[str, float]]:
    platform_spread = _derive_spread(evidence_items) or 0.0
    core_type = _influence_core_type(core)
    explanatory_core = core_type in {"faq_or_longform_explanation", "expert_explanation", "third_party_context"}
    relay_core = core_type in {"media_report", "recognized_media_report", "third_party_context", "expert_explanation"}

    components = {
        "cross_platform_presence": _hint(core, "cross_platform_presence_hint") if _hint(core, "cross_platform_presence_hint") is not None else platform_spread,
        "neutral_or_explanatory_frame": _hint(core, "neutral_or_explanatory_frame_hint") if _hint(core, "neutral_or_explanatory_frame_hint") is not None else (0.80 if explanatory_core else 0.40),
        "source_credibility_across_camps": _hint(core, "source_credibility_across_camps_hint") if _hint(core, "source_credibility_across_camps_hint") is not None else factual_credibility,
        "low_identity_threat_language": _hint(core, "low_identity_threat_language_hint") if _hint(core, "low_identity_threat_language_hint") is not None else 0.50,
        "shared_value_language": _hint(core, "shared_value_language_hint") if _hint(core, "shared_value_language_hint") is not None else 0.40,
        "media_or_third_party_relay": _hint(core, "media_or_third_party_relay_hint") if _hint(core, "media_or_third_party_relay_hint") is not None else (0.80 if relay_core else 0.20),
    }
    for name, value in components.items():
        components[name] = clamp01(value)
    for missing_name in ("cross_platform_presence_hint", "neutral_or_explanatory_frame_hint", "source_credibility_across_camps_hint"):
        if _hint(core, missing_name) is None:
            warnings["missing_component_warnings"].append(missing_name)
    score = clamp01(
        0.25 * components["cross_platform_presence"]
        + 0.20 * components["neutral_or_explanatory_frame"]
        + 0.20 * components["source_credibility_across_camps"]
        + 0.15 * components["low_identity_threat_language"]
        + 0.10 * components["shared_value_language"]
        + 0.10 * components["media_or_third_party_relay"]
    )
    return score, components


def calculate_bridge_potential(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    associated = get_influencecore_associated_evidence(core, evidence_items)
    factual_credibility, _components = _factual_credibility_detail(core, associated, warnings)
    score, _bridge_components = _bridge_potential_detail(core, associated, factual_credibility, warnings)
    return score


def _backlash_risk_detail(
    core: dict[str, Any],
    warnings: dict[str, list[str]],
) -> tuple[float, dict[str, float | None]]:
    components = {
        "mismatch_with_cluster_concerns": _hint(core, "mismatch_with_cluster_concerns_hint"),
        "perceived_defensiveness": _hint(core, "perceived_defensiveness_hint"),
        "timing_lag": _hint(core, "timing_lag_hint"),
        "low_empathy_language": _hint(core, "low_empathy_language_hint"),
        "contradiction_with_prior_record": _hint(core, "contradiction_with_prior_record_hint"),
        "high_identity_threat": _hint(core, "high_identity_threat_hint"),
        "ambiguity_or_missing_detail": _hint(core, "ambiguity_or_missing_detail_hint"),
    }
    backlash_hint = _hint(core, "backlash_hint")
    if backlash_hint is not None and all(value is None for value in components.values()):
        components["mismatch_with_cluster_concerns"] = backlash_hint
        components["ambiguity_or_missing_detail"] = backlash_hint
    for name, value in components.items():
        if value is None:
            warnings["missing_component_warnings"].append(name)
    score, _missing = _weighted_available(
        [
            ("mismatch_with_cluster_concerns", components["mismatch_with_cluster_concerns"], 0.22),
            ("perceived_defensiveness", components["perceived_defensiveness"], 0.18),
            ("timing_lag", components["timing_lag"], 0.16),
            ("low_empathy_language", components["low_empathy_language"], 0.14),
            ("contradiction_with_prior_record", components["contradiction_with_prior_record"], 0.12),
            ("high_identity_threat", components["high_identity_threat"], 0.10),
            ("ambiguity_or_missing_detail", components["ambiguity_or_missing_detail"], 0.08),
        ]
    )
    return score, components


def calculate_backlash_risk(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    _ = evidence_items
    warnings = _influence_warnings()
    score, _components = _backlash_risk_detail(core, warnings)
    return score


def calculate_core_strength(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    associated = get_influencecore_associated_evidence(core, evidence_items)
    fc, _fc_components = _factual_credibility_detail(core, associated, warnings)
    nr, nr_components = _narrative_resonance_detail(core, associated, warnings)
    ex, _ex_components = _sample_exposure_detail(core, associated, warnings)
    br, _br_components = _bridge_potential_detail(core, associated, fc, warnings)
    return clamp01(
        0.24 * fc
        + 0.22 * nr
        + 0.18 * ex
        + 0.14 * nr_components["clarity_score"]
        + 0.12 * nr_components["novelty_score"]
        + 0.10 * br
    )


def calculate_attention_amplification(core: dict[str, Any], evidence_items: list[dict[str, Any]]) -> float:
    warnings = _influence_warnings()
    associated = get_influencecore_associated_evidence(core, evidence_items)
    fc, _fc_components = _factual_credibility_detail(core, associated, warnings)
    nr, nr_components = _narrative_resonance_detail(core, associated, warnings)
    ex, _ex_components = _sample_exposure_detail(core, associated, warnings)
    br, _br_components = _bridge_potential_detail(core, associated, fc, warnings)
    return clamp01(
        0.24 * ex
        + 0.20 * nr
        + 0.18 * nr_components["emotional_charge"]
        + 0.16 * nr_components["novelty_score"]
        + 0.12 * nr_components["repetition_signal"]
        + 0.10 * br
    )


def _influence_quality_flags() -> list[str]:
    return [
        "selected_sample_only",
        "uncalibrated",
        "mock_default_coefficients",
        "evidence_not_truth",
        "not_official_verification",
        "not_truth_score",
        "not_people_cluster",
        "not_real_person",
    ]


def calculate_influencecore_weight(
    core: dict[str, Any],
    evidence_items: list[dict[str, Any]],
) -> dict[str, Any]:
    core_id = str(core.get("core_id") or "core_unknown")
    core_type = _influence_core_type(core)
    associated = get_influencecore_associated_evidence(core, evidence_items)
    eligible = _eligible_evidence(associated)
    warnings = _influence_warnings()
    evidence_mass = _influence_evidence_mass(associated)

    if _label(core.get("core_type")) not in KNOWN_INFLUENCE_CORE_TYPES:
        warnings["unknown_core_type_warnings"].append("unknown_core_type_defaulted_to_unknown_source_core")
    if evidence_mass["rejected_excluded_count"]:
        warnings["rejected_excluded_warnings"].append("rejected_evidence_excluded_from_influencecore_scores")
    if evidence_mass["low_trust_count"]:
        warnings["low_trust_warnings"].append("low_trust_evidence_lowers_factual_credibility")
    if evidence_mass["review_needed_count"]:
        warnings["review_needed_warnings"].append("review_needed_evidence_keeps_human_review_required")
    if any((_as_float(evidence.get("duplicate_count")) or 1.0) > 1 for evidence in eligible):
        warnings["duplicate_folded_warnings"].append("duplicate_count_used_only_as_bounded_repetition_signal")

    if not eligible:
        warnings["insufficient_data_warnings"].append("no_associated_analysis_ready_evidence")
        return {
            "schema": "sentigraph_influence_core_weight_v0_1",
            "core_id": core_id,
            "core_type": core_type,
            "model_status": "8P_3_influencecore_formula",
            "coefficient_source": COEFFICIENT_SOURCE,
            "calibration_status": CALIBRATION_STATUS,
            "empirical_validation": EMPIRICAL_VALIDATION,
            "sample_scope": SCOPE_NOTE,
            "evidence_mass": evidence_mass,
            "scores": _influence_zero_scores(),
            "components": {
                "factual_credibility_components": {},
                "narrative_resonance_components": {},
                "sample_exposure_components": {},
                "bridge_potential_components": {},
                "backlash_risk_components": {},
                "core_strength_components": {},
                "attention_amplification_components": {},
                "core_risk_components": {},
                "source_identity_weight": get_source_identity_weight(core),
                "associated_evidence_ids_used": [],
            },
            "quality_flags": _influence_quality_flags(),
            "warnings": warnings,
            "explanation": [
                "No analysis-ready evidence matched this InfluenceCore.",
                "InfluenceCore scores are selected-sample metadata only.",
            ],
            "boundary_flags": _influence_boundary_flags(),
        }

    fc, fc_components = _factual_credibility_detail(core, associated, warnings)
    nr, nr_components = _narrative_resonance_detail(core, associated, warnings)
    ex, ex_components = _sample_exposure_detail(core, associated, warnings)
    br, br_components = _bridge_potential_detail(core, associated, fc, warnings)
    bk, bk_components = _backlash_risk_detail(core, warnings)

    core_strength = clamp01(
        0.24 * fc
        + 0.22 * nr
        + 0.18 * ex
        + 0.14 * nr_components["clarity_score"]
        + 0.12 * nr_components["novelty_score"]
        + 0.10 * br
    )
    attention_amplification = clamp01(
        0.24 * ex
        + 0.20 * nr
        + 0.18 * nr_components["emotional_charge"]
        + 0.16 * nr_components["novelty_score"]
        + 0.12 * nr_components["repetition_signal"]
        + 0.10 * br
    )
    amplification = clamp01(
        0.25 * attention_amplification
        + 0.20 * ex
        + 0.18 * nr_components["repetition_signal"]
        + 0.15 * br
        + 0.12 * nr_components["novelty_score"]
        + 0.10 * nr_components["emotional_charge"]
    )
    credibility_adjusted = clamp01(amplification * (0.55 + 0.45 * fc))

    empathy_or_context = _hint(core, "empathy_or_context_hint")
    if empathy_or_context is None:
        empathy_or_context = 0.40
        warnings["missing_component_warnings"].append("empathy_or_context_hint")
    resolution_signal = _hint(core, "resolution_signal_hint")
    if resolution_signal is None:
        resolution_signal = 0.35
        warnings["missing_component_warnings"].append("resolution_signal_hint")
    deescalation = clamp01(
        0.24 * fc
        + 0.22 * nr_components["clarity_score"]
        + 0.20 * resolution_signal
        + 0.16 * br
        + 0.10 * empathy_or_context
        + 0.08 * br_components["low_identity_threat_language"]
        - 0.20 * bk
    )

    low_trust_conflict = _hint(core, "low_trust_conflict_hint") if _hint(core, "low_trust_conflict_hint") is not None else _low_trust_share(eligible)
    privacy_risk = _hint(core, "privacy_or_sensitivity_risk_hint") if _hint(core, "privacy_or_sensitivity_risk_hint") is not None else _sensitive_privacy_flag_share(eligible)
    contradiction_risk = _hint(core, "contradiction_risk_hint") or 0.0
    unresolved_grievance = _hint(core, "unresolved_grievance_hint") or 0.0
    core_risk = clamp01(
        0.20 * amplification
        + 0.18 * bk
        + 0.16 * nr_components["emotional_charge"]
        + 0.14 * low_trust_conflict
        + 0.12 * privacy_risk
        + 0.10 * contradiction_risk
        + 0.10 * unresolved_grievance
    )

    if amplification > 0.55 and fc < 0.50:
        warnings["low_confidence_warnings"].append("high_attention_low_credibility")

    scores = {
        "factual_credibility": fc,
        "narrative_resonance": nr,
        "sample_exposure": ex,
        "bridge_potential": br,
        "backlash_risk": bk,
        "core_strength": core_strength,
        "attention_amplification": attention_amplification,
        "amplification_score": amplification,
        "credibility_adjusted_influence_score": credibility_adjusted,
        "deescalation_potential": deescalation,
        "core_risk": core_risk,
    }
    components = {
        "factual_credibility_components": fc_components,
        "narrative_resonance_components": nr_components,
        "sample_exposure_components": ex_components,
        "bridge_potential_components": br_components,
        "backlash_risk_components": bk_components,
        "core_strength_components": {
            "factual_credibility": fc,
            "narrative_resonance": nr,
            "sample_exposure": ex,
            "clarity_score": nr_components["clarity_score"],
            "novelty_score": nr_components["novelty_score"],
            "bridge_potential": br,
        },
        "attention_amplification_components": {
            "sample_exposure": ex,
            "narrative_resonance": nr,
            "emotional_charge": nr_components["emotional_charge"],
            "novelty_score": nr_components["novelty_score"],
            "repetition_signal": nr_components["repetition_signal"],
            "bridge_potential": br,
        },
        "core_risk_components": {
            "amplification_score": amplification,
            "backlash_risk": bk,
            "emotional_charge": nr_components["emotional_charge"],
            "low_trust_conflict": clamp01(low_trust_conflict),
            "privacy_or_sensitivity_risk": clamp01(privacy_risk),
            "contradiction_risk": clamp01(contradiction_risk),
            "unresolved_grievance": clamp01(unresolved_grievance),
        },
        "source_identity_weight": fc_components["source_identity_weight"],
        "associated_evidence_ids_used": [str(evidence.get("evidence_id")) for evidence in eligible if evidence.get("evidence_id")],
    }
    explanation = [
        "InfluenceCore scores use selected-sample metadata only.",
        "Scores are uncalibrated mock-default heuristics.",
        "InfluenceCore is a content or narrative core, not a person or PeopleCluster.",
        "Evidence is evidence, not truth.",
    ]

    return {
        "schema": "sentigraph_influence_core_weight_v0_1",
        "core_id": core_id,
        "core_type": core_type,
        "model_status": "8P_3_influencecore_formula",
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "sample_scope": SCOPE_NOTE,
        "evidence_mass": evidence_mass,
        "scores": scores,
        "components": components,
        "quality_flags": _influence_quality_flags(),
        "warnings": warnings,
        "explanation": explanation,
        "boundary_flags": _influence_boundary_flags(),
    }


def calculate_all_influencecore_weights(fixture: dict) -> list[dict[str, Any]]:
    cores = fixture.get("influence_cores") if isinstance(fixture, dict) else None
    evidence_items = fixture.get("evidence_items_safe") if isinstance(fixture, dict) else None
    if not isinstance(cores, list) or not cores:
        return []
    safe_evidence = [item for item in evidence_items if isinstance(item, dict)] if isinstance(evidence_items, list) else []
    return [
        calculate_influencecore_weight(core, safe_evidence)
        for core in cores
        if isinstance(core, dict)
    ]


def build_mock_calculator_run_metadata(fixture: dict) -> dict[str, Any]:
    validation = validate_mock_fixture_contract(fixture)
    fixture_id = _fixture_value(fixture, "fixture_id", "missing_fixture_id")
    case_id = _fixture_value(fixture, "case_id", "missing_case_id")
    sample_id = _fixture_value(fixture, "sample_id", "missing_sample_id")

    return {
        "schema": SCHEMA,
        "run_id": f"mock_run_{fixture_id}",
        "fixture_id": fixture_id,
        "case_id": case_id,
        "sample_id": sample_id,
        "model_name": MODEL_NAME,
        "model_version": MODEL_VERSION,
        "model_status": MODEL_STATUS,
        "coefficient_source": COEFFICIENT_SOURCE,
        "calibration_status": CALIBRATION_STATUS,
        "empirical_validation": EMPIRICAL_VALIDATION,
        "generated_at": GENERATED_AT,
        "scope_note": SCOPE_NOTE,
        "human_review_required": True,
        "boundary_flags": _boundary_flags(),
        "runtime_side_effects": _runtime_side_effects(),
        "validation_summary": {
            "status": validation["status"],
            "blockers": validation["blockers"],
            "warnings": validation["warnings"],
            "forbidden_field_count": validation["forbidden_field_count"],
            "overclaim_blocker_count": validation["overclaim_blocker_count"],
            "response_strategy_blocker_count": validation["response_strategy_blocker_count"],
            "unknown_platform_warning_count": validation["unknown_platform_warning_count"],
        },
        "module_outputs": _module_outputs(),
    }


def validate_output_boundary_flags(run: dict) -> dict[str, Any]:
    blockers: list[dict[str, str]] = []
    flags = run.get("boundary_flags") if isinstance(run, dict) else None
    side_effects = run.get("runtime_side_effects") if isinstance(run, dict) else None

    if not isinstance(flags, dict):
        blockers.append(
            _blocker(
                field="boundary_flags",
                path="boundary_flags",
                reason="boundary_flags_must_be_dict",
                category="output_boundary_blocker",
            )
        )
    else:
        for flag in REQUIRED_BOUNDARY_FLAGS:
            if flags.get(flag) is not True:
                blockers.append(
                    _blocker(
                        field=flag,
                        path=f"boundary_flags.{flag}",
                        reason="required_boundary_flag_missing_or_false",
                        category="output_boundary_blocker",
                    )
                )

    if not isinstance(side_effects, dict):
        blockers.append(
            _blocker(
                field="runtime_side_effects",
                path="runtime_side_effects",
                reason="runtime_side_effects_must_be_dict",
                category="output_boundary_blocker",
            )
        )
    else:
        for key, value in side_effects.items():
            if value is not False:
                blockers.append(
                    _blocker(
                        field=str(key),
                        path=f"runtime_side_effects.{key}",
                        reason="runtime_side_effect_flag_must_be_false",
                        category="output_boundary_blocker",
                    )
                )

    return {
        "status": "blocked" if blockers else "pass",
        "blockers": blockers,
        "human_review_required": True,
    }


def calculate_opinion_ecosystem_mock_fixture(fixture: dict) -> dict[str, Any]:
    run = build_mock_calculator_run_metadata(fixture)
    boundary_validation = validate_output_boundary_flags(run)
    if boundary_validation["status"] == "blocked":
        run["validation_summary"]["status"] = "blocked"
        run["validation_summary"]["blockers"] = [
            *run["validation_summary"]["blockers"],
            *boundary_validation["blockers"],
        ]
    if run["validation_summary"]["status"] == "metadata_ready":
        content_outputs = calculate_all_content_aggregate_weights(fixture)
        influence_outputs = calculate_all_influencecore_weights(fixture)
        if influence_outputs:
            run["module_outputs"] = _module_outputs_with_content_and_influence(content_outputs, influence_outputs)
        elif content_outputs:
            run["module_outputs"] = _module_outputs_with_content_aggregate(content_outputs)
    return run
