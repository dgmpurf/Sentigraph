from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.alert import AnalysisSnapshot
from app.schemas.case import AnalysisCaseCreateRequest
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScore
from app.services.case_store import configure_case_repository, get_case_repository, reset_case_store
from app.services.forecasting.forecast_service import compute_forecast_from_snapshots
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cases(case_store_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))
    reset_case_store()


@pytest.fixture
def case_store_path(tmp_path):
    return tmp_path / "cases.json"


def test_forecast_endpoint_no_snapshots_returns_insufficient_history() -> None:
    case_id = _create_case()

    response = client.get(f"/api/v1/cases/{case_id}/forecast")

    assert response.status_code == 200
    body = response.json()
    assert body["forecast_status"] == "insufficient_history"
    assert body["forecast_confidence"] == "insufficient_history"
    assert body["snapshot_count"] == 0
    assert "监控快照" in body["recommended_action"]


def test_one_snapshot_forecast_has_low_confidence() -> None:
    case_id = _create_case()
    _save_snapshots(case_id, [42])

    response = client.post(f"/api/v1/cases/{case_id}/forecast/run")

    assert response.status_code == 200
    body = response.json()
    assert body["forecast_status"] == "ready"
    assert body["forecast_confidence"] == "low"
    assert body["trend_direction"] == "unknown"
    assert body["predicted_risk_score"] == pytest.approx(42)


def test_rising_risk_forecast() -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([30, 45, 60]))

    assert forecast.trend_direction == "rising"
    assert forecast.predicted_risk_score > forecast.latest_risk
    assert forecast.forecast_confidence == "medium_low"


def test_falling_risk_forecast() -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([72, 61, 50]))

    assert forecast.trend_direction == "falling"
    assert forecast.predicted_risk_score < forecast.latest_risk


def test_stable_risk_forecast() -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([50, 51, 50]))

    assert forecast.trend_direction == "stable"
    assert abs(forecast.predicted_risk_score - forecast.latest_risk) <= 3


def test_four_or_more_snapshots_use_medium_confidence() -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([40, 43, 45, 47]))

    assert forecast.snapshot_count == 4
    assert forecast.forecast_confidence == "medium"
    assert [item.horizon for item in forecast.risk_forecasts] == ["next_check", "1h", "6h", "24h"]


def test_high_acceleration_raises_predicted_risk() -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([20, 25, 45]))

    assert forecast.acceleration > 0
    assert forecast.predicted_risk_score > forecast.latest_risk


def test_predicted_risk_is_clamped_to_0_100() -> None:
    high_forecast = compute_forecast_from_snapshots("case_001", _snapshots([90, 95, 100]))
    low_forecast = compute_forecast_from_snapshots("case_002", _snapshots([10, 5, 0]))

    assert high_forecast.predicted_risk_score == 100
    assert low_forecast.predicted_risk_score == 0


@pytest.mark.parametrize(
    ("score", "level"),
    [(20, "low"), (50, "medium"), (75, "high"), (90, "critical")],
)
def test_predicted_risk_level_mapping(score: float, level: str) -> None:
    forecast = compute_forecast_from_snapshots("case_001", _snapshots([score]))

    assert forecast.predicted_risk_level == level


def test_topic_forecast_generated_when_topics_exist() -> None:
    snapshots = _snapshots(
        [45, 55, 65],
        topic_scores=[40, 55, 70],
    )

    forecast = compute_forecast_from_snapshots("case_001", snapshots)

    assert forecast.topic_forecasts
    topic_forecast = forecast.topic_forecasts[0]
    assert topic_forecast.topic == "Product quality issues"
    assert topic_forecast.trend_direction == "rising"
    assert topic_forecast.predicted_topic_risk_score > topic_forecast.current_topic_risk_score


def test_real_crisis_and_manipulation_forecasts_work() -> None:
    forecast = compute_forecast_from_snapshots(
        "case_001",
        _snapshots(
            [40, 48, 58],
            real_crisis_scores=[20, 35, 50],
            manipulation_scores=[15, 25, 45],
        ),
    )

    assert forecast.real_crisis_trend_direction == "rising"
    assert forecast.manipulation_trend_direction == "rising"
    assert forecast.predicted_real_crisis_risk > 50
    assert forecast.predicted_manipulation_risk > 45


def test_forecast_endpoint_keeps_old_case_and_monitoring_apis_working() -> None:
    case_id = _create_case()

    assert client.post(f"/api/v1/cases/{case_id}/run").status_code == 200
    assert client.post(f"/api/v1/cases/{case_id}/monitor/run").status_code == 200
    assert client.get(f"/api/v1/cases/{case_id}/snapshots").status_code == 200
    assert client.get(f"/api/v1/cases/{case_id}/alerts").status_code == 200

    forecast_response = client.get(f"/api/v1/cases/{case_id}/forecast")
    assert forecast_response.status_code == 200
    assert forecast_response.json()["snapshot_count"] >= 2


def _create_case() -> str:
    case = get_case_repository().create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    return case.case_id


def _save_snapshots(case_id: str, scores: list[float]) -> None:
    repository = get_case_repository()
    for snapshot in _snapshots(scores, case_id=case_id):
        repository.save_analysis_snapshot(case_id, snapshot)


def _snapshots(
    scores: list[float],
    *,
    case_id: str = "case_001",
    real_crisis_scores: list[float] | None = None,
    manipulation_scores: list[float] | None = None,
    topic_scores: list[float] | None = None,
) -> list[AnalysisSnapshot]:
    start = datetime(2026, 5, 17, 10, 0, tzinfo=timezone.utc)
    real_values = real_crisis_scores or [20 + index * 2 for index, _score in enumerate(scores)]
    manipulation_values = manipulation_scores or [18 + index * 2 for index, _score in enumerate(scores)]
    topic_values = topic_scores or [42 + index * 3 for index, _score in enumerate(scores)]
    snapshots: list[AnalysisSnapshot] = []
    for index, score in enumerate(scores, start=1):
        snapshots.append(
            AnalysisSnapshot(
                snapshot_id=f"{case_id}_snapshot_{index:03d}",
                case_id=case_id,
                created_at=start + timedelta(minutes=index),
                run_index=index,
                risk_score=score,
                overall_risk=score,
                risk_level=_level(score),
                risk_model_version=TOPIC_RISK_MODEL_VERSION,
                real_crisis_risk=real_values[index - 1],
                manipulation_risk=manipulation_values[index - 1],
                top_risk_topics=[_topic(topic_values[index - 1])],
                summary="Synthetic forecast test snapshot.",
            )
        )
    return snapshots


def _topic(score: float) -> TopicRiskScore:
    return TopicRiskScore(
        topic_id="topic_quality",
        cluster_id="topic_quality",
        topic="Product quality issues",
        comment_count=18,
        negative_ratio=0.65,
        average_sentiment_score=-0.5,
        neg_severity=0.45,
        spread_signal=0.55,
        controversy_signal=0.25,
        bot_signal=0.2,
        influence_proxy=0.5,
        topic_risk_score=score,
        topic_risk_level=_level(score),
        risk_explanation="Synthetic quality topic risk explanation.",
        risk_score=score,
        risk_level=_level(score),
    )


def _level(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
