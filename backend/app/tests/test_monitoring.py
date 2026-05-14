from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseCreateRequest
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScore
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.monitoring.alert_evaluator import evaluate_alerts
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cases(case_store_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))
    reset_case_store()


@pytest.fixture
def case_store_path(tmp_path):
    return tmp_path / "cases.json"


def test_case_run_creates_monitoring_snapshot() -> None:
    case_id = _create_case()

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")

    assert run_response.status_code == 200
    assert snapshots_response.status_code == 200
    snapshots = snapshots_response.json()
    assert len(snapshots) == 1
    assert snapshots[0]["case_id"] == case_id
    assert snapshots[0]["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert snapshots[0]["top_risk_topics"]


def test_monitor_run_endpoint_creates_snapshot_and_alerts() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    response = client.post(f"/api/v1/cases/{case_id}/monitor/run")
    alerts_response = client.get(f"/api/v1/cases/{case_id}/alerts")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")

    assert response.status_code == 200
    body = response.json()
    assert body["case_id"] == case_id
    assert body["snapshot_count"] == 2
    assert body["latest_snapshot"]["run_index"] == 2
    assert body["latest_risk_delta"] >= 0
    assert body["status"] in {"stable", "alerts_detected"}

    assert snapshots_response.status_code == 200
    assert len(snapshots_response.json()) == 2
    assert alerts_response.status_code == 200
    assert isinstance(alerts_response.json(), list)


def test_all_alerts_endpoint_returns_persisted_events() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitor/run")

    response = client.get("/api/v1/alerts")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alert_evaluator_with_no_previous_snapshot_returns_baseline_info() -> None:
    latest = _snapshot("case_001_snapshot_001", "case_001", 42, "medium")

    alerts = evaluate_alerts(None, latest)

    assert len(alerts) == 1
    assert alerts[0].level == "info"
    assert alerts[0].alert_type == "baseline_created"


def test_alert_evaluator_detects_risk_increase() -> None:
    previous = _snapshot("case_001_snapshot_001", "case_001", 40, "medium")
    latest = _snapshot("case_001_snapshot_002", "case_001", 62, "medium")

    alerts = evaluate_alerts(previous, latest)

    assert any(alert.alert_type == "risk_score_increase" for alert in alerts)
    assert any(alert.level == "critical" for alert in alerts)


def test_alert_evaluator_detects_risk_level_escalation() -> None:
    previous = _snapshot("case_001_snapshot_001", "case_001", 38, "low")
    latest = _snapshot("case_001_snapshot_002", "case_001", 45, "medium")

    alerts = evaluate_alerts(previous, latest)

    assert any(alert.alert_type == "risk_level_escalation" for alert in alerts)


def test_alert_evaluator_detects_manipulation_risk_increase() -> None:
    previous = _snapshot("case_001_snapshot_001", "case_001", 45, "medium", manipulation_risk=20)
    latest = _snapshot("case_001_snapshot_002", "case_001", 50, "medium", manipulation_risk=40)

    alerts = evaluate_alerts(previous, latest)

    assert any(alert.alert_type == "manipulation_risk_increase" for alert in alerts)


def test_alert_evaluator_detects_real_crisis_risk_increase() -> None:
    previous = _snapshot("case_001_snapshot_001", "case_001", 45, "medium", real_crisis_risk=18)
    latest = _snapshot("case_001_snapshot_002", "case_001", 50, "medium", real_crisis_risk=32)

    alerts = evaluate_alerts(previous, latest)

    assert any(alert.alert_type == "real_crisis_risk_increase" for alert in alerts)


def test_alert_evaluator_detects_new_high_risk_topic() -> None:
    previous = _snapshot(
        "case_001_snapshot_001",
        "case_001",
        45,
        "medium",
        top_topics=[_topic("topic_service", "service", 55, "medium")],
    )
    latest = _snapshot(
        "case_001_snapshot_002",
        "case_001",
        58,
        "medium",
        top_topics=[
            _topic("topic_safety", "safety", 78, "high"),
            _topic("topic_service", "service", 55, "medium"),
        ],
    )

    alerts = evaluate_alerts(previous, latest)

    assert any(alert.alert_type == "new_high_risk_topic" for alert in alerts)
    assert any(alert.metadata.get("topic") == "safety" for alert in alerts)


def test_local_json_store_persists_snapshots_and_alerts(case_store_path) -> None:
    repository = CaseRepository(LocalJsonCaseStore(case_store_path))
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    snapshot = _snapshot("case_001_snapshot_001", case.case_id, 42, "medium")
    alert = AlertEvent(
        alert_id="alert_case_001_snapshot_001_001",
        case_id=case.case_id,
        snapshot_id=snapshot.snapshot_id,
        level="info",
        alert_type="baseline_created",
        message="baseline",
        reason="first snapshot",
        created_at=snapshot.created_at,
    )

    repository.save_analysis_snapshot(case.case_id, snapshot)
    repository.save_alert_events(case.case_id, [alert])

    reloaded = CaseRepository(LocalJsonCaseStore(case_store_path))
    snapshots = reloaded.list_analysis_snapshots(case.case_id)
    alerts = reloaded.list_case_alerts(case.case_id)

    assert len(snapshots) == 1
    assert snapshots[0].snapshot_id == snapshot.snapshot_id
    assert len(alerts) == 1
    assert alerts[0].alert_type == "baseline_created"


def test_repeated_monitor_runs_persist_snapshot_history_and_delta() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    first_monitor_response = client.post(f"/api/v1/cases/{case_id}/monitor/run")
    second_monitor_response = client.post(f"/api/v1/cases/{case_id}/monitor/run")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")
    alerts_response = client.get(f"/api/v1/cases/{case_id}/alerts")

    assert first_monitor_response.status_code == 200
    assert second_monitor_response.status_code == 200
    assert snapshots_response.status_code == 200
    assert alerts_response.status_code == 200

    snapshots = snapshots_response.json()
    second_body = second_monitor_response.json()
    assert len(snapshots) == 3
    assert [snapshot["run_index"] for snapshot in snapshots] == [1, 2, 3]
    assert second_body["snapshot_count"] == 3
    assert second_body["latest_snapshot"]["run_index"] == 3
    assert second_body["latest_risk_delta"] == pytest.approx(12.0)
    assert isinstance(alerts_response.json(), list)


def test_old_case_flow_still_exports_markdown() -> None:
    case_id = _create_case()
    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    markdown_response = client.get(f"/api/v1/cases/{case_id}/report/markdown")

    assert run_response.status_code == 200
    assert markdown_response.status_code == 200
    assert TOPIC_RISK_MODEL_VERSION in markdown_response.json()["markdown"]


def test_old_mvp_apis_still_work_with_monitoring_changes() -> None:
    assert client.get("/api/v1/health").status_code == 200
    assert client.get("/api/v1/platforms").status_code == 200
    assert (
        client.post(
            "/api/v1/crawl/start",
            json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 20},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/analysis/run",
            json={"project_id": "project_001", "analysis_types": ["sentiment", "risk"]},
        ).status_code
        == 200
    )
    assert client.get("/api/v1/analysis/project_001").status_code == 200
    assert (
        client.post(
            "/api/v1/visualization/data",
            json={"project_id": "project_001", "platforms": ["reddit"]},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/summary/generate",
            json={"project_id": "project_001", "report_language": "zh-CN"},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/recommendation/generate",
            json={"project_id": "project_001", "report_language": "zh-CN"},
        ).status_code
        == 200
    )
    assert client.get("/api/v1/alerts/project_001").status_code == 200


def _create_case() -> str:
    response = client.post(
        "/api/v1/cases",
        json={
            "keyword": "Tesla",
            "platforms": ["reddit", "weibo", "bilibili"],
            "title": "Tesla public opinion case",
        },
    )
    assert response.status_code == 200
    return response.json()["case_id"]


def _snapshot(
    snapshot_id: str,
    case_id: str,
    risk_score: float,
    risk_level: str,
    *,
    real_crisis_risk: float = 20,
    manipulation_risk: float = 20,
    top_topics: list[TopicRiskScore] | None = None,
) -> AnalysisSnapshot:
    return AnalysisSnapshot(
        snapshot_id=snapshot_id,
        case_id=case_id,
        created_at=datetime(2026, 5, 14, 10, 0, tzinfo=timezone.utc),
        run_index=1,
        risk_score=risk_score,
        overall_risk=risk_score,
        risk_level=risk_level,
        risk_model_version=TOPIC_RISK_MODEL_VERSION,
        real_crisis_risk=real_crisis_risk,
        manipulation_risk=manipulation_risk,
        top_risk_topics=top_topics or [_topic("topic_default", "default", 42, "medium")],
        summary="mock snapshot",
    )


def _topic(topic_id: str, topic: str, score: float, level: str) -> TopicRiskScore:
    return TopicRiskScore(
        topic_id=topic_id,
        cluster_id=topic_id,
        topic=topic,
        comment_count=12,
        negative_ratio=0.6,
        average_sentiment_score=-0.4,
        neg_severity=0.4,
        spread_signal=0.5,
        controversy_signal=0.2,
        bot_signal=0.3,
        influence_proxy=0.4,
        topic_risk_score=score,
        topic_risk_level=level,
        risk_explanation=f"{topic} risk explanation",
        risk_score=score,
        risk_level=level,
    )
