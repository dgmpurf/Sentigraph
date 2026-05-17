from __future__ import annotations

from app.schemas.alert import AnalysisSnapshot
from app.schemas.forecast import ForecastInputSnapshot, ForecastResult
from app.services.case_store import get_case_repository
from app.services.forecasting.risk_forecaster import build_risk_forecasts
from app.services.forecasting.topic_forecaster import build_topic_forecasts
from app.services.forecasting.trend_features import build_trend_features, confidence_from_snapshot_count


def get_case_forecast(case_id: str) -> ForecastResult | None:
    """Return a deterministic forecast for the case, computed from persisted snapshots."""
    return _compute_case_forecast(case_id)


def run_case_forecast(case_id: str) -> ForecastResult | None:
    """Compute the current deterministic MVP forecast.

    Forecast persistence is intentionally not added yet; the current storage
    layer stores snapshots/alerts/notifications and the forecast is a pure
    derived view over that history.
    """
    return _compute_case_forecast(case_id)


def compute_forecast_from_snapshots(case_id: str, snapshots: list[AnalysisSnapshot]) -> ForecastResult:
    sorted_snapshots = sorted(snapshots, key=lambda snapshot: snapshot.created_at)
    snapshot_count = len(sorted_snapshots)
    confidence = confidence_from_snapshot_count(snapshot_count)
    if not sorted_snapshots:
        return ForecastResult(
            case_id=case_id,
            forecast_status="insufficient_history",
            forecast_confidence=confidence,
            recommended_action="请先运行案例分析或监控检查，生成监控快照后再运行风险预测。",
            message="历史不足，需更多监控快照。当前没有可用于预测的监控快照。",
        )

    risk_features = build_trend_features([snapshot.risk_score for snapshot in sorted_snapshots])
    real_crisis_features = build_trend_features([snapshot.real_crisis_risk for snapshot in sorted_snapshots])
    manipulation_features = build_trend_features([snapshot.manipulation_risk for snapshot in sorted_snapshots])
    risk_forecasts = build_risk_forecasts(
        risk_features,
        real_crisis_features,
        manipulation_features,
        confidence=confidence,
    )
    primary = risk_forecasts[0]
    latest = sorted_snapshots[-1]

    return ForecastResult(
        case_id=case_id,
        forecast_status="ready",
        generated_at=latest.created_at,
        risk_model_version=latest.risk_model_version,
        snapshot_count=snapshot_count,
        latest_snapshot_id=latest.snapshot_id,
        horizon=primary.horizon,
        latest_risk=risk_features.latest_risk,
        moving_average=risk_features.moving_average,
        slope=risk_features.slope,
        acceleration=risk_features.acceleration,
        volatility=risk_features.volatility,
        trend_direction=risk_features.trend_direction,
        forecast_confidence=confidence,
        predicted_risk_score=primary.predicted_risk_score,
        predicted_risk_level=primary.predicted_risk_level,
        predicted_real_crisis_risk=primary.predicted_real_crisis_risk,
        predicted_manipulation_risk=primary.predicted_manipulation_risk,
        real_crisis_trend_direction=primary.real_crisis_trend_direction,
        manipulation_trend_direction=primary.manipulation_trend_direction,
        risk_forecasts=risk_forecasts,
        topic_forecasts=build_topic_forecasts(sorted_snapshots, confidence=confidence),
        input_snapshots=[_to_input_snapshot(snapshot) for snapshot in sorted_snapshots[-6:]],
        recommended_action=_recommended_action(snapshot_count, primary.trend_direction),
        message=_message(snapshot_count, primary.trend_direction, primary.predicted_risk_score),
    )


def _compute_case_forecast(case_id: str) -> ForecastResult | None:
    repository = get_case_repository()
    if not repository.get_case(case_id):
        return None
    return compute_forecast_from_snapshots(case_id, repository.list_analysis_snapshots(case_id))


def _to_input_snapshot(snapshot: AnalysisSnapshot) -> ForecastInputSnapshot:
    return ForecastInputSnapshot.model_validate(snapshot.model_dump(mode="json"))


def _recommended_action(snapshot_count: int, direction: str) -> str:
    if snapshot_count <= 1:
        return "继续运行监控检查，至少积累 2-3 个快照后再判断趋势。"
    if direction == "rising":
        return "风险预测呈上升趋势，建议提高监控频率并优先复核高风险话题。"
    if direction == "falling":
        return "风险预测呈下降趋势，可保持当前监控节奏并继续观察是否反弹。"
    if direction == "stable":
        return "风险预测较稳定，建议维持当前监控频率并关注新增高风险话题。"
    return "趋势方向仍不明确，建议继续积累监控快照。"


def _message(snapshot_count: int, direction: str, predicted_risk: float) -> str:
    if snapshot_count <= 1:
        return "Deterministic MVP 风险预测已生成，但历史样本较少，置信度较低。"
    direction_label = {
        "rising": "上升",
        "falling": "下降",
        "stable": "稳定",
        "unknown": "不明确",
    }.get(direction, direction)
    return f"Deterministic MVP 风险预测显示趋势{direction_label}，下一检查点预测风险为 {predicted_risk:.1f}/100。"
