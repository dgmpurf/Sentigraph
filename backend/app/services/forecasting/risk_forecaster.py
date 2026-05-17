from __future__ import annotations

from app.schemas.forecast import ForecastConfidence, ForecastHorizon, RiskForecast, TrendFeatures
from app.services.forecasting.trend_features import trend_direction
from app.services.scoring.topic_risk_score import risk_level_from_score


HORIZON_MULTIPLIERS: dict[ForecastHorizon, float] = {
    "next_check": 1.0,
    "1h": 1.25,
    "6h": 1.75,
    "24h": 2.5,
}


def build_risk_forecasts(
    risk_features: TrendFeatures,
    real_crisis_features: TrendFeatures,
    manipulation_features: TrendFeatures,
    *,
    confidence: ForecastConfidence,
) -> list[RiskForecast]:
    return [
        _build_one_forecast(
            horizon,
            risk_features,
            real_crisis_features,
            manipulation_features,
            confidence=confidence,
        )
        for horizon in HORIZON_MULTIPLIERS
    ]


def predict_score(features: TrendFeatures, horizon: ForecastHorizon = "next_check") -> float:
    multiplier = HORIZON_MULTIPLIERS[horizon]
    predicted = features.latest_risk + features.slope * multiplier + features.acceleration * 0.5 * multiplier
    return _round_score(predicted)


def direction_for_values(values: list[float]) -> str:
    return trend_direction(values)


def _build_one_forecast(
    horizon: ForecastHorizon,
    risk_features: TrendFeatures,
    real_crisis_features: TrendFeatures,
    manipulation_features: TrendFeatures,
    *,
    confidence: ForecastConfidence,
) -> RiskForecast:
    predicted_risk = predict_score(risk_features, horizon)
    predicted_real_crisis = predict_score(real_crisis_features, horizon)
    predicted_manipulation = predict_score(manipulation_features, horizon)

    return RiskForecast(
        horizon=horizon,
        predicted_risk_score=predicted_risk,
        predicted_risk_level=risk_level_from_score(predicted_risk),
        predicted_real_crisis_risk=predicted_real_crisis,
        predicted_manipulation_risk=predicted_manipulation,
        trend_direction=risk_features.trend_direction,
        real_crisis_trend_direction=real_crisis_features.trend_direction,
        manipulation_trend_direction=manipulation_features.trend_direction,
        forecast_confidence=confidence,
        forecast_reason=_forecast_reason(risk_features, horizon, predicted_risk),
    )


def _forecast_reason(features: TrendFeatures, horizon: ForecastHorizon, predicted_risk: float) -> str:
    if features.snapshot_count < 2:
        return "Only one monitoring snapshot is available, so the deterministic forecast keeps the latest risk as a low-confidence baseline."
    return (
        f"Deterministic MVP forecast for {horizon} uses latest risk {features.latest_risk:.1f}, "
        f"slope {features.slope:.1f}, and acceleration {features.acceleration:.1f}; "
        f"predicted risk is {predicted_risk:.1f}/100."
    )


def _round_score(value: float) -> float:
    return round(max(0.0, min(100.0, float(value))), 2)
