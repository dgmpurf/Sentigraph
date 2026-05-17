from __future__ import annotations

from statistics import mean

from app.schemas.forecast import ForecastConfidence, TrendDirection, TrendFeatures


def build_trend_features(values: list[float]) -> TrendFeatures:
    scores = [_clamp_score(value) for value in values]
    snapshot_count = len(scores)
    if not scores:
        return TrendFeatures()

    latest = scores[-1]
    moving_window = scores[-3:]
    moving_average = mean(moving_window)
    slope = _average_delta(scores)
    acceleration = _acceleration(scores)
    volatility = mean(abs(value - moving_average) for value in moving_window)

    return TrendFeatures(
        latest_risk=_round(latest),
        moving_average=_round(moving_average),
        slope=_round(slope),
        acceleration=_round(acceleration),
        volatility=_round(volatility),
        snapshot_count=snapshot_count,
        trend_direction=trend_direction(scores),
    )


def trend_direction(values: list[float], *, threshold: float = 2.0) -> TrendDirection:
    scores = [_clamp_score(value) for value in values]
    if len(scores) < 2:
        return "unknown"
    slope = _average_delta(scores)
    total_change = scores[-1] - scores[0]
    if slope >= threshold or total_change >= threshold * 2:
        return "rising"
    if slope <= -threshold or total_change <= -threshold * 2:
        return "falling"
    return "stable"


def confidence_from_snapshot_count(snapshot_count: int) -> ForecastConfidence:
    if snapshot_count <= 0:
        return "insufficient_history"
    if snapshot_count == 1:
        return "low"
    if snapshot_count <= 3:
        return "medium_low"
    return "medium"


def _average_delta(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    deltas = [values[index] - values[index - 1] for index in range(1, len(values))]
    return mean(deltas)


def _acceleration(values: list[float]) -> float:
    if len(values) < 3:
        return 0.0
    latest_delta = values[-1] - values[-2]
    previous_delta = values[-2] - values[-3]
    return latest_delta - previous_delta


def _clamp_score(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def _round(value: float) -> float:
    return round(float(value), 2)
