from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail
from app.schemas.forecast import ForecastResult
from app.services.simulation.intervention_library import ALLOWED_INTERVENTION_TYPES
from app.services.simulation.network_builder import build_homophilous_network
from app.services.simulation.schemas import (
    AudienceSegment,
    BaselinePublicProfile,
    CaseSimulationInitializationResult,
    CaseSimulationInitializerConfig,
    EventFrame,
    FrameGapAnalysis,
    FrameGapClassification,
    ObservedFrameProfile,
    PersonaCluster,
    SimulationAgent,
    SimulationConfig,
    SimulationIntervention,
    SimulationMessage,
    SimulationScenario,
    StrategyImplication,
    SubIssue,
    SubIssueCategory,
)


class CaseAnalysisRequiredError(ValueError):
    """Raised when a case has no completed aggregate analysis to initialize from."""


def build_case_simulation_initialization(
    case: AnalysisCaseDetail,
    *,
    snapshots: list[AnalysisSnapshot] | None = None,
    alerts: list[AlertEvent] | None = None,
    forecast: ForecastResult | None = None,
    config: CaseSimulationInitializerConfig | None = None,
) -> CaseSimulationInitializationResult:
    config = config or CaseSimulationInitializerConfig()
    if case.analysis_result is None:
        raise CaseAnalysisRequiredError("case_analysis_required")

    warnings: list[str] = []
    generated_at = datetime.now(timezone.utc)
    snapshots = snapshots or []
    alerts = alerts or []
    analysis = case.analysis_result
    analysis_data = _model_data(analysis)

    sentiment = _sentiment_distribution(analysis_data.get("sentiment"), warnings)
    topic_risks = list(analysis_data.get("topic_risks") or [])
    topics = list(analysis_data.get("topics") or [])
    sub_issues = _sub_issues_from_topics(
        topic_risks,
        topics,
        config=config,
        real_crisis_risk=_score(analysis_data.get("real_crisis_risk")),
        manipulation_risk=_score(analysis_data.get("manipulation_risk")),
        warnings=warnings,
    )
    if not sub_issues:
        sub_issues = [_fallback_sub_issue(case, analysis_data, warnings)]

    observed_count = _observed_comment_count(topic_risks, topics)
    if observed_count < config.min_observed_comments:
        warnings.append("insufficient_observed_comment_count")

    real_crisis_risk = _score(analysis_data.get("real_crisis_risk") or analysis_data.get("overall_risk"))
    manipulation_risk = _score(analysis_data.get("manipulation_risk") or analysis_data.get("bot_score"))
    if manipulation_risk >= 60:
        warnings.append("aggregate_repeated_script_or_manipulation_signal_detected")

    audience_segments = _audience_segments_from_sentiment(sentiment, real_crisis_risk, manipulation_risk)
    persona_clusters = _persona_clusters_from_segments(audience_segments, real_crisis_risk, manipulation_risk)
    baseline = _baseline_public_profile(case, sub_issues, real_crisis_risk)
    observed = _observed_frame_profile(
        case=case,
        sentiment=sentiment,
        sub_issues=sub_issues,
        audience_segments=audience_segments,
        persona_clusters=persona_clusters,
        manipulation_risk=manipulation_risk,
        real_crisis_risk=real_crisis_risk,
        snapshots=snapshots,
        alerts=alerts,
        forecast=forecast,
        observed_count=observed_count,
        warnings=warnings,
    )
    gap_analysis = _frame_gap_analysis(
        case=case,
        observed=observed,
        baseline=baseline,
        sentiment=sentiment,
        manipulation_risk=manipulation_risk,
        observed_count=observed_count,
        config=config,
    )
    implications = _strategy_implications(gap_analysis)

    event_frame = EventFrame(
        event_frame_id=f"event_frame_{case.case_id}",
        case_id=case.case_id,
        event_title=case.title or case.keyword,
        event_summary=_safe_text(analysis_data.get("summary") or case.keyword, max_length=280),
        generated_at=generated_at,
        sub_issues=sub_issues,
        observed_frame_profile=observed,
        baseline_public_profile=baseline,
        frame_gap_analysis=gap_analysis,
        strategy_implications=implications,
        initialization_hints={
            "source_case_status": case.status,
            "source_platforms": case.platforms,
            "allowed_interventions": _safe_allowed_interventions(),
            "recommended_default_intervention": _recommended_default_intervention(gap_analysis),
        },
        uncertainty_label=observed.uncertainty_label,
        uncertainty_reasons=list(dict.fromkeys(warnings)),
        assumption_log={
            "aggregate_inputs": [
                "case keyword",
                "platform list",
                "sentiment distribution",
                "topic risk scores",
                "monitoring snapshot count",
                "alert count",
                "forecast status",
            ],
            "synthetic_defaults": [
                "ordinary-public baseline",
                "persona cluster weights",
                "synthetic agent count",
            ],
        },
    )

    scenario = _simulation_scenario_from_initialization(
        case=case,
        event_frame=event_frame,
        audience_segments=audience_segments,
        persona_clusters=persona_clusters,
        sub_issues=sub_issues,
        config=config,
        real_crisis_risk=real_crisis_risk,
        manipulation_risk=manipulation_risk,
    )
    status = "partial" if warnings else "initialized"
    return CaseSimulationInitializationResult(
        case_id=case.case_id,
        status=status,
        generated_at=generated_at,
        model_version=config.model_version,
        event_frame=event_frame,
        audience_segments=audience_segments,
        persona_clusters=persona_clusters,
        frame_gap_analysis=gap_analysis,
        strategy_implications=implications,
        simulation_scenario=scenario,
        warnings=list(dict.fromkeys(warnings)),
    )


def _model_data(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="python")
    if isinstance(value, dict):
        return value
    return {}


def _score(value: Any, default: float = 0.0) -> float:
    try:
        return _clamp(float(value if value is not None else default), 0.0, 100.0)
    except (TypeError, ValueError):
        return default


def _ratio(value: Any, default: float = 0.0) -> float:
    try:
        return _clamp(float(value if value is not None else default), 0.0, 1.0)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _round(value: float, digits: int = 4) -> float:
    return round(value, digits)


def _safe_text(value: Any, *, max_length: int = 180) -> str:
    text = str(value or "").strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*\S+", r"\1=[redacted]", text)
    if len(text) > max_length:
        return text[: max_length - 3].rstrip() + "..."
    return text


def _sentiment_distribution(sentiment_value: Any, warnings: list[str]) -> dict[str, float]:
    sentiment = _model_data(sentiment_value)
    if not sentiment:
        warnings.append("missing_sentiment_distribution_used_safe_default")
        return {"negative": 0.45, "neutral": 0.35, "positive": 0.20}

    negative = _ratio(sentiment.get("negative_ratio"), 0.45)
    neutral = _ratio(sentiment.get("neutral_ratio"), 0.35)
    positive = _ratio(sentiment.get("positive_ratio"), 0.20)
    total = negative + neutral + positive
    if total <= 0:
        warnings.append("empty_sentiment_distribution_used_safe_default")
        return {"negative": 0.45, "neutral": 0.35, "positive": 0.20}
    return {
        "negative": _round(negative / total),
        "neutral": _round(neutral / total),
        "positive": _round(positive / total),
    }


def _sub_issues_from_topics(
    topic_risks: list[Any],
    topics: list[Any],
    *,
    config: CaseSimulationInitializerConfig,
    real_crisis_risk: float,
    manipulation_risk: float,
    warnings: list[str],
) -> list[SubIssue]:
    topic_examples = _topic_examples(topics)
    total_comments = sum(max(0, int(_model_data(topic).get("comment_count") or 0)) for topic in topic_risks)
    sub_issues: list[SubIssue] = []
    for index, raw_topic in enumerate(topic_risks, start=1):
        topic = _model_data(raw_topic)
        title = _safe_text(topic.get("topic") or topic.get("cluster_id") or f"sub_issue_{index}", max_length=90)
        comment_count = max(0, int(topic.get("comment_count") or 0))
        observed_volume = comment_count / total_comments if total_comments else min(1.0, 0.25 + index * 0.05)
        risk_score = _score(topic.get("topic_risk_score") or topic.get("risk_score"))
        category = _infer_sub_issue_category(title, topic.get("risk_explanation"))
        examples = topic_examples.get(str(topic.get("cluster_id") or ""), []) + topic_examples.get(title, [])
        examples = [_safe_text(example, max_length=140) for example in examples[: config.max_evidence_examples_per_issue]]
        sub_issues.append(
            SubIssue(
                sub_issue_id=str(topic.get("topic_id") or topic.get("cluster_id") or f"sub_issue_{index}"),
                category=category,
                title=title,
                summary=_safe_text(topic.get("risk_explanation") or topic.get("summary") or title, max_length=220),
                observed_volume=_round(observed_volume),
                negative_ratio=_ratio(topic.get("negative_ratio"), 0.45),
                neutral_ratio=_round(max(0.0, 1.0 - _ratio(topic.get("negative_ratio"), 0.45))),
                positive_ratio=0.0,
                topic_risk_score=risk_score,
                risk_score=risk_score,
                risk_level=str(topic.get("topic_risk_level") or topic.get("risk_level") or _risk_level(risk_score)),
                real_crisis_signal=real_crisis_risk,
                manipulation_signal=_score(topic.get("bot_signal"), manipulation_risk),
                influence_proxy=_score(topic.get("influence_proxy")),
                evidence_quality=_evidence_quality(risk_score, comment_count, real_crisis_risk),
                evidence_examples=examples,
                uncertainty_reasons=[] if examples else ["representative_examples_not_available"],
            )
        )
    if topic_risks and not sub_issues:
        warnings.append("topic_risk_records_unreadable")
    return sub_issues


def _topic_examples(topics: list[Any]) -> dict[str, list[str]]:
    examples: dict[str, list[str]] = {}
    for raw_topic in topics:
        topic = _model_data(raw_topic)
        comments = [_safe_text(item, max_length=140) for item in (topic.get("representative_comments") or [])]
        if not comments:
            continue
        if topic.get("cluster_id"):
            examples[str(topic["cluster_id"])] = comments
        if topic.get("topic"):
            examples[str(topic["topic"])] = comments
    return examples


def _fallback_sub_issue(
    case: AnalysisCaseDetail,
    analysis_data: dict[str, Any],
    warnings: list[str],
) -> SubIssue:
    warnings.append("missing_topic_risks_used_case_summary")
    risk_score = _score(analysis_data.get("overall_risk") or case.risk_score)
    return SubIssue(
        sub_issue_id="sub_issue_case_summary",
        category=_infer_sub_issue_category(case.keyword, analysis_data.get("summary")),
        title=_safe_text(case.keyword or case.title, max_length=90),
        summary=_safe_text(analysis_data.get("summary") or "Aggregate case summary only.", max_length=220),
        observed_volume=1.0,
        negative_ratio=0.45,
        neutral_ratio=0.35,
        positive_ratio=0.2,
        topic_risk_score=risk_score,
        risk_score=risk_score,
        risk_level=_risk_level(risk_score),
        uncertainty_reasons=["topic_risk_scores_not_available"],
    )


def _infer_sub_issue_category(*values: Any) -> SubIssueCategory:
    text = " ".join(str(value or "").lower() for value in values)
    if any(word in text for word in ("safety", "legal", "harm", "injury", "安全", "法律", "合规", "事故", "伤害")):
        return "safety_legal_issue"
    if any(word in text for word in ("price", "refund", "pricing", "价格", "退款", "收费")):
        return "pricing_dispute"
    if any(word in text for word in ("delay", "response", "silence", "回应", "延迟", "拖延", "通报")):
        return "official_response_delay"
    if any(word in text for word in ("quality", "defect", "service", "质量", "故障", "售后", "客服", "瑕疵")):
        return "product_quality"
    if any(word in text for word in ("trust", "brand", "信任", "品牌", "口碑")):
        return "brand_trust"
    if any(word in text for word in ("script", "coordinated", "repeat", "manipulation", "重复", "水军", "操纵")):
        return "suspected_manipulation"
    if any(word in text for word in ("celebrity", "public figure", "明星", "艺人", "公众人物")):
        return "public_figure_controversy"
    if any(word in text for word in ("workplace", "employee", "labor", "职场", "员工", "加班", "公司管理")):
        return "workplace_company_issue"
    return "unknown"


def _evidence_quality(risk_score: float, comment_count: int, real_crisis_risk: float) -> str:
    if comment_count >= 20 and (risk_score >= 70 or real_crisis_risk >= 70):
        return "strong"
    if comment_count >= 8 or risk_score >= 55:
        return "moderate"
    if comment_count <= 1:
        return "weak"
    return "mixed"


def _risk_level(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _observed_comment_count(topic_risks: list[Any], topics: list[Any]) -> int:
    total = 0
    for raw_topic in topic_risks or topics:
        topic = _model_data(raw_topic)
        total += max(0, int(topic.get("comment_count") or 0))
    return total


def _audience_segments_from_sentiment(
    sentiment: dict[str, float],
    real_crisis_risk: float,
    manipulation_risk: float,
) -> list[AudienceSegment]:
    negative = max(sentiment["negative"], 0.01)
    neutral = max(sentiment["neutral"], 0.04)
    positive = max(sentiment["positive"], 0.04)
    sentiment_total = negative + neutral + positive
    negative, neutral, positive = negative / sentiment_total, neutral / sentiment_total, positive / sentiment_total
    affected_share = min(0.16, real_crisis_risk / 1000)
    authority_share = min(0.12, 0.06 + real_crisis_risk / 1800)
    bridge_share = 0.08
    available = max(0.65, 1.0 - affected_share - authority_share - bridge_share)
    segments = [
        _audience_segment(
            "core_opposition",
            "核心反对者",
            "core_opposition",
            available * negative * 0.55,
            -0.78,
            "red",
            attention=0.82,
            threshold=0.2,
            influence=44 + manipulation_risk * 0.12,
        ),
        _audience_segment(
            "mild_opposition",
            "轻度反对者",
            "mild_opposition",
            available * negative * 0.45,
            -0.38,
            "orange",
            attention=0.7,
            threshold=0.32,
            influence=32,
        ),
        _audience_segment(
            "neutral_observers",
            "中立观察者",
            "neutral_observers",
            available * neutral,
            -0.02,
            "gray",
            attention=0.58,
            threshold=0.46,
            influence=28,
            bridge=0.25,
        ),
        _audience_segment(
            "supporters",
            "支持者",
            "supporters",
            available * positive,
            0.42,
            "green",
            attention=0.52,
            threshold=0.38,
            influence=26,
        ),
        _audience_segment(
            "affected_users",
            "受影响用户",
            "affected_users",
            affected_share,
            -0.62,
            "red",
            attention=0.88,
            threshold=0.18,
            influence=42,
        ),
        _audience_segment(
            "authority_trusting_group",
            "信任权威人群",
            "authority_trusting_group",
            authority_share,
            0.08,
            "blue",
            attention=0.6,
            threshold=0.42,
            influence=36,
            bridge=0.2,
        ),
        _audience_segment(
            "bridge_nodes",
            "跨圈层桥接节点",
            "bridge_nodes",
            bridge_share,
            -0.04,
            "blue",
            attention=0.72,
            threshold=0.44,
            influence=50,
            bridge=0.78,
        ),
    ]
    return _normalize_segments(segments)


def _audience_segment(
    segment_id: str,
    label: str,
    segment_type: str,
    proportion: float,
    opinion: float,
    color: str,
    *,
    attention: float,
    threshold: float,
    influence: float,
    bridge: float = 0.0,
) -> AudienceSegment:
    stance = "negative" if opinion < -0.15 else "positive" if opinion > 0.15 else "neutral"
    return AudienceSegment(
        segment_id=segment_id,
        label=label,
        segment_type=segment_type,
        proportion=_round(_clamp(proportion, 0.0, 1.0)),
        stance_distribution={stance: 1.0},
        sentiment_distribution={stance: 1.0},
        color_hint=color,
        average_attention_level=attention,
        opinion_baseline=opinion,
        action_threshold=threshold,
        influence_proxy=_clamp(influence, 0.0, 100.0),
        bridge_score=bridge,
        data_origin="aggregate_case_distribution",
    )


def _normalize_segments(segments: list[AudienceSegment]) -> list[AudienceSegment]:
    total = sum(segment.proportion for segment in segments) or 1.0
    return [
        segment.model_copy(update={"proportion": _round(segment.proportion / total)})
        for segment in segments
        if segment.proportion > 0.0001
    ]


def _persona_clusters_from_segments(
    segments: list[AudienceSegment],
    real_crisis_risk: float,
    manipulation_risk: float,
) -> list[PersonaCluster]:
    crisis = real_crisis_risk / 100
    manipulation = manipulation_risk / 100
    clusters: list[PersonaCluster] = []
    for segment in segments:
        is_opposition = "opposition" in segment.segment_type or segment.segment_type == "affected_users"
        is_bridge = segment.segment_type == "bridge_nodes"
        is_authority = segment.segment_type == "authority_trusting_group"
        clusters.append(
            PersonaCluster(
                cluster_id=f"persona_{segment.segment_id}",
                segment_id=segment.segment_id,
                label=segment.label,
                confirmation_bias=_round(0.32 + (0.28 if is_opposition else 0.0) + manipulation * 0.12),
                authority_trust=_round(0.82 if is_authority else 0.46 + (0.2 if is_bridge else 0.0)),
                conformity=_round(0.42 + manipulation * 0.15),
                reactance=_round(0.28 + (0.22 if is_opposition else 0.0) + crisis * 0.12),
                negativity_weight=_round(0.42 + (0.32 if is_opposition else 0.08) + crisis * 0.18),
                attention_fatigue=_round(0.12 + manipulation * 0.12),
                identity_attachment=_round(0.34 + (0.22 if is_opposition else 0.0)),
                loss_sensitivity=_round(0.38 + crisis * 0.36),
                moral_outrage_sensitivity=_round(0.36 + crisis * 0.32),
                harm_salience=_round(crisis),
                crisis_legitimacy_pressure=_round(0.3 + crisis * 0.55),
                platform_activity=_round(0.45 + segment.influence_proxy / 220),
                source="aggregate_persona_cluster_default",
            )
        )
    return clusters


def _baseline_public_profile(
    case: AnalysisCaseDetail,
    sub_issues: list[SubIssue],
    real_crisis_risk: float,
) -> BaselinePublicProfile:
    primary_category = max(sub_issues, key=lambda issue: issue.topic_risk_score).category if sub_issues else "unknown"
    defaults = {
        "safety_legal_issue": (-0.34, 0.76, 0.62, 0.5, 0.74, 0.84),
        "product_quality": (-0.22, 0.64, 0.58, 0.4, 0.55, 0.62),
        "official_response_delay": (-0.18, 0.52, 0.54, 0.46, 0.52, 0.5),
        "pricing_dispute": (-0.12, 0.58, 0.56, 0.38, 0.42, 0.42),
        "suspected_manipulation": (-0.08, 0.45, 0.6, 0.5, 0.45, 0.48),
        "brand_trust": (-0.16, 0.52, 0.56, 0.42, 0.48, 0.5),
        "workplace_company_issue": (-0.22, 0.58, 0.52, 0.48, 0.62, 0.52),
        "public_figure_controversy": (-0.18, 0.42, 0.48, 0.55, 0.6, 0.4),
        "unknown": (-0.08, 0.45, 0.58, 0.35, 0.42, 0.48),
    }
    reaction, loss, authority, reactance, outrage, safety = defaults.get(primary_category, defaults["unknown"])
    reaction = _clamp(reaction - (real_crisis_risk / 1000), -1.0, 1.0)
    return BaselinePublicProfile(
        baseline_id=f"baseline_{case.case_id}",
        event_category=primary_category,
        expected_average_reaction=_round(reaction),
        expected_loss_sensitivity=_round(loss),
        expected_authority_trust=_round(authority),
        expected_reactance=_round(reactance),
        expected_moral_outrage=_round(outrage),
        expected_safety_legal_sensitivity=_round(safety),
        assumed_parameters=[
            "Synthetic ordinary-public baseline; not empirical calibration.",
            "Aggregate-level use only.",
        ],
        limitations=[
            "Baseline should be recalibrated with lawful, public, representative data before production use.",
            "No individual-level persuasion profile is created.",
        ],
    )


def _observed_frame_profile(
    *,
    case: AnalysisCaseDetail,
    sentiment: dict[str, float],
    sub_issues: list[SubIssue],
    audience_segments: list[AudienceSegment],
    persona_clusters: list[PersonaCluster],
    manipulation_risk: float,
    real_crisis_risk: float,
    snapshots: list[AnalysisSnapshot],
    alerts: list[AlertEvent],
    forecast: ForecastResult | None,
    observed_count: int,
    warnings: list[str],
) -> ObservedFrameProfile:
    uncertainty = "medium"
    if observed_count <= 0:
        uncertainty = "insufficient_data"
    elif observed_count < 5:
        uncertainty = "high"
    elif snapshots:
        uncertainty = "low"
    topic_total = sum(issue.observed_volume for issue in sub_issues) or 1.0
    crisis = real_crisis_risk / 100
    return ObservedFrameProfile(
        observed_frame_id=f"observed_frame_{case.case_id}",
        observed_comment_count=observed_count,
        observed_post_count=len(sub_issues),
        observed_platforms=list(case.platforms),
        stance_distribution=dict(sentiment),
        sentiment_distribution=dict(sentiment),
        topic_distribution={
            issue.title: _round(issue.observed_volume / topic_total)
            for issue in sub_issues
        },
        top_risk_topics=[issue.title for issue in sorted(sub_issues, key=lambda item: item.topic_risk_score, reverse=True)[:5]],
        manipulation_signal_score=manipulation_risk,
        real_crisis_signal_score=real_crisis_risk,
        harm_salience=_round(crisis),
        loss_sensitivity=_round(0.35 + crisis * 0.45),
        moral_outrage_sensitivity=_round(0.34 + crisis * 0.42),
        crisis_legitimacy_pressure=_round(0.3 + crisis * 0.55),
        suspected_manipulation_pressure=_round(manipulation_risk / 100),
        repetition_exposure=_round(min(1.0, manipulation_risk / 120)),
        influence_distribution_summary={
            "max_topic_influence_proxy": _round(max((issue.influence_proxy for issue in sub_issues), default=0.0)),
            "high_attention_segments": _round(
                sum(segment.proportion for segment in audience_segments if segment.average_attention_level >= 0.7)
            ),
        },
        audience_segments=audience_segments,
        persona_clusters=persona_clusters,
        forecast_status=getattr(forecast, "forecast_status", "not_available") if forecast else "not_available",
        snapshot_count=len(snapshots),
        alert_count=len(alerts),
        uncertainty_label=uncertainty,
        confidence_warnings=list(dict.fromkeys(warnings)),
    )


def _frame_gap_analysis(
    *,
    case: AnalysisCaseDetail,
    observed: ObservedFrameProfile,
    baseline: BaselinePublicProfile,
    sentiment: dict[str, float],
    manipulation_risk: float,
    observed_count: int,
    config: CaseSimulationInitializerConfig,
) -> FrameGapAnalysis:
    observed_reaction = sentiment["positive"] - sentiment["negative"]
    gap = observed_reaction - baseline.expected_average_reaction
    secondary: list[FrameGapClassification] = []
    if observed_count < config.min_observed_comments:
        primary: FrameGapClassification = "insufficient_data"
    elif manipulation_risk >= 65:
        primary = "manipulation_suspected_frame"
    elif sentiment["negative"] >= 0.36 and sentiment["positive"] >= 0.24:
        primary = "polarized_frame"
    elif gap <= -0.18:
        primary = "frame_more_negative_than_public"
    elif gap >= 0.18:
        primary = "frame_more_positive_than_public"
    else:
        primary = "aligned_public_and_frame"

    if manipulation_risk >= 50 and primary != "manipulation_suspected_frame":
        secondary.append("manipulation_suspected_frame")
    if sentiment["negative"] >= 0.36 and sentiment["positive"] >= 0.24 and primary != "polarized_frame":
        secondary.append("polarized_frame")

    summary = _gap_summary(primary)
    return FrameGapAnalysis(
        analysis_id=f"frame_gap_{case.case_id}",
        event_frame_id=f"event_frame_{case.case_id}",
        primary_classification=primary,
        secondary_classifications=secondary,
        baseline_profile_id=baseline.baseline_id,
        observed_frame_id=observed.observed_frame_id,
        gap_scores={
            "observed_average_reaction": _round(observed_reaction),
            "baseline_expected_average_reaction": baseline.expected_average_reaction,
            "reaction_gap": _round(gap),
            "negative_ratio": sentiment["negative"],
            "positive_ratio": sentiment["positive"],
            "manipulation_signal_score": manipulation_risk,
        },
        summary=summary,
        strategy_cautions=_strategy_cautions(primary, secondary),
        monitoring_recommendations=_monitoring_recommendations(primary),
        uncertainty_label=observed.uncertainty_label,
        uncertainty_reasons=list(observed.confidence_warnings),
    )


def _gap_summary(classification: FrameGapClassification) -> str:
    summaries = {
        "aligned_public_and_frame": "Observed discussion is broadly aligned with the ordinary-public baseline.",
        "frame_more_negative_than_public": "Observed frame is more negative than the conservative ordinary-public baseline.",
        "frame_more_positive_than_public": "Observed frame is friendlier than the ordinary-public baseline; broader exposure may raise risk.",
        "polarized_frame": "Observed frame contains meaningful negative and supportive camps, so bridge and neutral audiences matter.",
        "manipulation_suspected_frame": "Aggregate repeated-script or manipulation pressure is elevated; organic complaints still require separate review.",
        "insufficient_data": "Case analysis has too little aggregate evidence for a confident frame comparison.",
    }
    return summaries[classification]


def _strategy_cautions(
    primary: FrameGapClassification,
    secondary: list[FrameGapClassification],
) -> list[str]:
    classifications = {primary, *secondary}
    cautions: list[str] = []
    if "frame_more_negative_than_public" in classifications:
        cautions.append("Broaden observation before concluding the wider public is equally negative.")
        cautions.append("Evaluate whether high-reach visibility intervention could create neutral-audience backlash.")
    if "frame_more_positive_than_public" in classifications:
        cautions.append("Avoid overconfidence from a friendly echo chamber.")
    if "manipulation_suspected_frame" in classifications:
        cautions.append("Separate organic user complaints from repeated-script signals; do not dismiss all negativity.")
    if "insufficient_data" in classifications:
        cautions.append("Run analysis or monitoring again before using the scenario for planning.")
    return cautions or ["Keep intervention comparison transparent and human-reviewed."]


def _monitoring_recommendations(primary: FrameGapClassification) -> list[str]:
    if primary == "insufficient_data":
        return ["Run monitoring to accumulate snapshots.", "Review whether topic risk data is available."]
    if primary == "manipulation_suspected_frame":
        return ["Track repeated-script indicators separately from organic complaint volume."]
    if primary == "frame_more_positive_than_public":
        return ["Sample broader public reactions before assuming risk is contained."]
    return ["Continue monitoring topic risk and audience sentiment changes."]


def _strategy_implications(gap_analysis: FrameGapAnalysis) -> list[StrategyImplication]:
    classifications = [gap_analysis.primary_classification, *gap_analysis.secondary_classifications]
    implications: list[StrategyImplication] = []
    for index, classification in enumerate(dict.fromkeys(classifications), start=1):
        if classification == "aligned_public_and_frame":
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_aligned",
                    frame_gap_classification=classification,
                    recommended_simulation_options=[
                        "clarification",
                        "apology",
                        "compensation",
                        "progress_update",
                        "third_party_evidence",
                        "content_removal_with_explanation",
                    ],
                    discouraged_options=["no_response"],
                    rationale=(
                        "When the observed frame aligns with the baseline, compare remediation, clarification, "
                        "transparent updates, evidence, and lawful content governance if needed."
                    ),
                )
            )
        elif classification == "frame_more_negative_than_public":
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_negative_gap",
                    frame_gap_classification=classification,
                    recommended_simulation_options=["clarification", "third_party_evidence", "progress_update"],
                    discouraged_options=["opaque_response", "unreviewed_visibility_action"],
                    rationale=(
                        "Broaden observation and test cross-community exposure. Visibility interventions should be "
                        "reviewed for neutral-audience backlash before any real-world decision."
                    ),
                    safety_warnings=["Keep all planning aggregate-level, transparent, and human-reviewed."],
                )
            )
        elif classification == "frame_more_positive_than_public":
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_positive_gap",
                    frame_gap_classification=classification,
                    recommended_simulation_options=["progress_update", "faq", "third_party_evidence"],
                    discouraged_options=["overconfident_no_response"],
                    rationale="Friendly observed reactions may understate broader risk; test more conservative scenarios.",
                )
            )
        elif classification == "manipulation_suspected_frame":
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_manipulation_signal",
                    frame_gap_classification=classification,
                    recommended_simulation_options=["misinformation_correction", "third_party_evidence", "clarification"],
                    discouraged_options=["dismiss_all_negative_feedback"],
                    rationale=(
                        "Repeated-script pressure is an aggregate signal only. Keep organic complaints separate and "
                        "watch whether real users begin following the narrative."
                    ),
                )
            )
        elif classification == "polarized_frame":
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_polarized",
                    frame_gap_classification=classification,
                    recommended_simulation_options=["faq", "third_party_evidence", "apology"],
                    discouraged_options=["high_intensity_argumentative_response"],
                    rationale="Polarized frames benefit from calm evidence and empathy toward neutral observers.",
                )
            )
        else:
            implications.append(
                StrategyImplication(
                    implication_id=f"strategy_{index}_insufficient",
                    frame_gap_classification=classification,
                    recommended_simulation_options=["no_response", "progress_update"],
                    discouraged_options=["automatic_action_execution"],
                    rationale="Data is insufficient; use the scenario only as a placeholder and collect more snapshots.",
                    confidence_label="insufficient_data",
                )
            )
    return implications


def _recommended_default_intervention(gap_analysis: FrameGapAnalysis) -> str:
    if gap_analysis.primary_classification == "manipulation_suspected_frame":
        return "misinformation_correction"
    if gap_analysis.primary_classification == "frame_more_positive_than_public":
        return "progress_update"
    if gap_analysis.primary_classification == "insufficient_data":
        return "no_response"
    return "clarification"


def _simulation_scenario_from_initialization(
    *,
    case: AnalysisCaseDetail,
    event_frame: EventFrame,
    audience_segments: list[AudienceSegment],
    persona_clusters: list[PersonaCluster],
    sub_issues: list[SubIssue],
    config: CaseSimulationInitializerConfig,
    real_crisis_risk: float,
    manipulation_risk: float,
) -> SimulationScenario:
    agents = _synthetic_agents(audience_segments, persona_clusters, config.synthetic_agent_count)
    primary_issue = max(sub_issues, key=lambda issue: issue.topic_risk_score)
    messages = [
        SimulationMessage(
            message_id=f"case_message_{index}",
            topic=issue.title,
            source_type="aggregate_case_analysis",
            source_credibility=_round(0.48 + issue.real_crisis_signal / 300),
            stance_direction=_round(-0.25 - issue.topic_risk_score / 140),
            emotional_intensity=_round(0.32 + issue.topic_risk_score / 180),
            evidence_strength=_round(0.3 + issue.real_crisis_signal / 180),
            framing=issue.category,
            novelty=_round(0.55 + min(0.3, issue.observed_volume * 0.3)),
            repetition=_round(min(0.85, issue.manipulation_signal / 100)),
            platform_reach=_round(0.42 + issue.influence_proxy / 180),
        )
        for index, issue in enumerate(sub_issues[:3], start=1)
    ]
    intervention_type = event_frame.initialization_hints.get("recommended_default_intervention", "clarification")
    intervention = SimulationIntervention(
        intervention_id=f"case_intervention_{intervention_type}",
        intervention_type=intervention_type,
        topic=primary_issue.title,
        message="Aggregate, transparent crisis-response option initialized from case analysis.",
        publication_step=1,
        source_credibility=0.78,
        stance_direction=0.28 if intervention_type != "no_response" else 0.0,
        emotional_intensity=0.24 if intervention_type != "no_response" else 0.0,
        evidence_strength=0.68 if intervention_type != "no_response" else 0.0,
        framing=intervention_type,
        responsibility_acknowledgement=_round(real_crisis_risk / 120),
        transparency_level=0.72,
        intensity=0.62 if intervention_type != "no_response" else 0.0,
    )
    return SimulationScenario(
        scenario_id=f"case_simulation_{case.case_id}",
        name=f"Case initialized scenario: {case.title or case.keyword}",
        description=(
            "Deterministic aggregate Simulation Lab scenario initialized from Sentigraph case analysis. "
            "Synthetic agents represent audience segments, not real accounts."
        ),
        topic=primary_issue.title,
        agents=agents,
        network_edges=build_homophilous_network(agents),
        messages=messages,
        interventions=[intervention],
        config=SimulationConfig(steps=6, seed=0),
        responsibility_level=_round(real_crisis_risk / 100),
        metadata={
            "source": "case_to_simulation_initializer",
            "case_id": case.case_id,
            "event_frame_id": event_frame.event_frame_id,
            "aggregate_only": True,
            "no_individual_targeting": True,
            "no_real_account_targets": True,
            "synthetic_agents_only": True,
            "frame_gap_classification": event_frame.frame_gap_analysis.primary_classification,
            "manipulation_signal_score": manipulation_risk,
            "allowed_interventions": _safe_allowed_interventions(),
        },
    )


def _synthetic_agents(
    segments: list[AudienceSegment],
    personas: list[PersonaCluster],
    target_count: int,
) -> list[SimulationAgent]:
    persona_by_segment = {persona.segment_id: persona for persona in personas}
    counts = _segment_agent_counts(segments, target_count)
    agents: list[SimulationAgent] = []
    for segment in segments:
        persona = persona_by_segment.get(segment.segment_id)
        count = counts.get(segment.segment_id, 0)
        for index in range(count):
            offset = (index - (count - 1) / 2) * 0.035
            latent = _clamp(segment.opinion_baseline + offset, -1.0, 1.0)
            agents.append(
                SimulationAgent(
                    agent_id=f"synthetic_{segment.segment_id}_{index + 1:02d}",
                    community_id=segment.segment_id,
                    latent_opinion=_round(latent),
                    expressed_opinion=_round(latent * 0.82),
                    prior_anchor=_round(latent),
                    stubbornness=_round(0.32 + (persona.confirmation_bias if persona else 0.45) * 0.35),
                    confidence_radius=_round(0.36 + segment.bridge_score * 0.34),
                    action_threshold=segment.action_threshold,
                    confirmation_bias=persona.confirmation_bias if persona else 0.45,
                    negativity_weight=_round(0.9 + (persona.negativity_weight if persona else 0.5)),
                    reactance=persona.reactance if persona else 0.35,
                    authority_trust=persona.authority_trust if persona else 0.55,
                    conformity=persona.conformity if persona else 0.45,
                    attention_budget=segment.average_attention_level,
                    fatigue=persona.attention_fatigue if persona else 0.12,
                    identity_group=segment.segment_type,
                    status="active",
                )
            )
    return agents


def _segment_agent_counts(segments: list[AudienceSegment], target_count: int) -> dict[str, int]:
    counts = {segment.segment_id: max(1, int(round(segment.proportion * target_count))) for segment in segments}
    while sum(counts.values()) > target_count:
        largest = max(counts, key=counts.get)
        if counts[largest] <= 1:
            break
        counts[largest] -= 1
    while sum(counts.values()) < target_count:
        largest = max(segments, key=lambda segment: segment.proportion).segment_id
        counts[largest] += 1
    return counts


def _safe_allowed_interventions() -> list[str]:
    safe = [
        intervention_type
        for intervention_type in ALLOWED_INTERVENTION_TYPES
        if intervention_type
        not in {
            "content_removal",
            "comment_closure",
            "account_restriction",
        }
    ]
    if "content_removal_with_explanation" not in safe:
        safe.append("content_removal_with_explanation")
    return safe
