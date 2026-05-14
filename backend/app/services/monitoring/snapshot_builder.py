from __future__ import annotations

from datetime import datetime

from app.schemas.alert import AnalysisSnapshot
from app.schemas.case import AnalysisCaseDetail
from app.schemas.common import RiskLevel
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScore
from app.services.scoring.topic_risk_score import risk_level_from_score


def build_analysis_snapshot(
    case: AnalysisCaseDetail,
    *,
    snapshot_id: str,
    created_at: datetime,
    run_index: int,
    apply_mock_shift: bool = False,
) -> AnalysisSnapshot:
    """Build a deterministic monitoring snapshot from the latest case output.

    The optional mock shift gives repeated offline monitoring checks a stable
    trend without random values or external data.
    """
    report = case.report
    analysis = case.analysis_result
    visualization = case.visualization_data

    base_score = _first_number(
        getattr(report, "overall_risk", None),
        getattr(report, "risk_score", None),
        getattr(visualization, "overall_risk", None),
        getattr(visualization, "risk_score", None),
        getattr(analysis, "overall_risk", None),
        getattr(getattr(analysis, "risk", None), "risk_score", None),
        case.risk_score,
        default=0.0,
    )
    base_real_crisis = _first_number(
        getattr(report, "real_crisis_risk", None),
        getattr(visualization, "real_crisis_risk", None),
        getattr(analysis, "real_crisis_risk", None),
        default=0.0,
    )
    base_manipulation = _first_number(
        getattr(report, "manipulation_risk", None),
        getattr(visualization, "manipulation_risk", None),
        getattr(analysis, "manipulation_risk", None),
        default=0.0,
    )
    risk_model_version = (
        getattr(report, "risk_model_version", None)
        or getattr(visualization, "risk_model_version", None)
        or getattr(analysis, "risk_model_version", None)
        or case.risk_model_version
        or TOPIC_RISK_MODEL_VERSION
    )
    top_topics = _first_topic_list(
        getattr(report, "top_risk_topics", None),
        getattr(visualization, "top_risk_topics", None),
        getattr(analysis, "top_risk_topics", None),
    )

    shift_index = max(run_index - 1, 0) if apply_mock_shift else 0
    risk_score = _clamp_score(base_score + min(36.0, shift_index * 12.0))
    real_crisis_risk = _clamp_score(base_real_crisis + min(30.0, shift_index * 8.0))
    manipulation_risk = _clamp_score(base_manipulation + min(45.0, shift_index * 16.0))
    shifted_topics = _shift_topic_scores(top_topics, shift_index)

    return AnalysisSnapshot(
        snapshot_id=snapshot_id,
        case_id=case.case_id,
        created_at=created_at,
        run_index=run_index,
        risk_score=risk_score,
        overall_risk=risk_score,
        risk_level=risk_level_from_score(risk_score),
        risk_model_version=risk_model_version,
        real_crisis_risk=real_crisis_risk,
        manipulation_risk=manipulation_risk,
        top_risk_topics=shifted_topics,
        summary=getattr(report, "overall_summary", None) or getattr(analysis, "summary", None),
    )


def _shift_topic_scores(topics: list[TopicRiskScore], shift_index: int) -> list[TopicRiskScore]:
    if not topics:
        return []

    topic_delta = min(24.0, shift_index * 10.0)
    shifted: list[TopicRiskScore] = []
    for topic in topics:
        score = _clamp_score(topic.topic_risk_score + topic_delta)
        level: RiskLevel = risk_level_from_score(score)
        explanation = topic.risk_explanation
        if shift_index:
            explanation = f"{explanation} Monitoring snapshot {shift_index} shows a deterministic mock increase."
        shifted.append(
            topic.model_copy(
                update={
                    "topic_risk_score": score,
                    "topic_risk_level": level,
                    "risk_score": score,
                    "risk_level": level,
                    "risk_explanation": explanation,
                }
            )
        )
    return sorted(shifted, key=lambda item: (-item.topic_risk_score, -item.comment_count, item.topic))


def _first_topic_list(*values: list[TopicRiskScore] | None) -> list[TopicRiskScore]:
    for value in values:
        if value:
            return list(value)
    return []


def _first_number(*values: float | int | None, default: float = 0.0) -> float:
    for value in values:
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return default


def _clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, float(value))), 2)
