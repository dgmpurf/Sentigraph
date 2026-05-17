from __future__ import annotations

from app.schemas.alert import AnalysisSnapshot
from app.schemas.forecast import ForecastConfidence, TopicRiskForecast
from app.schemas.risk import TopicRiskScore
from app.services.forecasting.risk_forecaster import predict_score
from app.services.forecasting.trend_features import build_trend_features
from app.services.scoring.topic_risk_score import risk_level_from_score


def build_topic_forecasts(
    snapshots: list[AnalysisSnapshot],
    *,
    confidence: ForecastConfidence,
) -> list[TopicRiskForecast]:
    if not snapshots:
        return []

    latest_topics = snapshots[-1].top_risk_topics[:3]
    forecasts = [_forecast_topic(topic, snapshots, confidence=confidence) for topic in latest_topics]
    return sorted(forecasts, key=lambda item: (-item.predicted_topic_risk_score, item.topic))


def _forecast_topic(
    latest_topic: TopicRiskScore,
    snapshots: list[AnalysisSnapshot],
    *,
    confidence: ForecastConfidence,
) -> TopicRiskForecast:
    series = _topic_score_series(latest_topic, snapshots)
    features = build_trend_features(series)
    predicted = predict_score(features, "next_check")
    topic_key = _topic_key(latest_topic)
    return TopicRiskForecast(
        topic_id=latest_topic.topic_id,
        topic=latest_topic.topic,
        current_topic_risk_score=round(float(latest_topic.topic_risk_score), 2),
        predicted_topic_risk_score=predicted,
        predicted_topic_risk_level=risk_level_from_score(predicted),
        trend_direction=features.trend_direction,
        risk_explanation=latest_topic.risk_explanation,
        forecast_reason=(
            "Topic forecast uses deterministic monitoring snapshot deltas for the same topic key. "
            f"Observed {len(series)} matching point(s) for {topic_key}; confidence is {confidence}."
        ),
    )


def _topic_score_series(topic: TopicRiskScore, snapshots: list[AnalysisSnapshot]) -> list[float]:
    key = _topic_key(topic)
    scores: list[float] = []
    for snapshot in snapshots:
        matched = next((item for item in snapshot.top_risk_topics if _topic_key(item) == key), None)
        if matched:
            scores.append(float(matched.topic_risk_score))
    return scores or [float(topic.topic_risk_score)]


def _topic_key(topic: TopicRiskScore) -> str:
    return topic.topic_id or topic.cluster_id or topic.topic
