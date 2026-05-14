from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.alert import AlertEvent
from app.schemas.case import AnalysisCaseCreateRequest
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.notifications.notification_service import (
    create_notification_from_alert,
    create_notifications_from_alerts,
    get_outbox_status,
    simulate_send_all_pending,
)
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cases(case_store_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))
    reset_case_store()


@pytest.fixture
def case_store_path(tmp_path):
    return tmp_path / "cases.json"


def test_create_notification_from_alert(case_store_path) -> None:
    repository = CaseRepository(LocalJsonCaseStore(case_store_path))
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    alert = _alert(case.case_id)

    notification = create_notification_from_alert(alert, repository=repository)

    assert notification.alert_id == alert.alert_id
    assert notification.case_id == case.case_id
    assert notification.channel_type == "in_app"
    assert notification.status == "pending"
    assert notification.message == "舆情风险出现上升，请关注该案例。"


def test_list_notifications_and_case_notifications(case_store_path) -> None:
    repository = CaseRepository(LocalJsonCaseStore(case_store_path))
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    create_notification_from_alert(_alert(case.case_id), repository=repository)

    all_notifications = repository.list_notifications()
    case_notifications = repository.list_case_notifications(case.case_id)

    assert len(all_notifications) == 1
    assert len(case_notifications) == 1
    assert case_notifications[0].case_id == case.case_id


def test_mark_notification_read_endpoint() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitor/run")
    notification = client.get(f"/api/v1/cases/{case_id}/notifications").json()[0]

    response = client.post(f"/api/v1/notifications/{notification['notification_id']}/read")

    assert response.status_code == 200
    body = response.json()
    assert body["read_at"] is not None
    assert body["status"] in {"pending", "simulated_sent"}


def test_simulate_send_endpoint() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitor/run")
    notification = client.get(f"/api/v1/cases/{case_id}/notifications").json()[0]

    response = client.post(f"/api/v1/notifications/{notification['notification_id']}/simulate-send")

    assert response.status_code == 200
    body = response.json()
    assert body["simulated"] is True
    assert body["status"] == "simulated_sent"
    assert body["simulated_sent_at"] is not None
    assert body["notification"]["simulated_sent_at"] is not None


def test_simulate_send_all_pending(case_store_path) -> None:
    repository = CaseRepository(LocalJsonCaseStore(case_store_path))
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    create_notifications_from_alerts(
        [
            _alert(case.case_id, alert_id="alert_case_001_snapshot_002_001"),
            _alert(case.case_id, alert_id="alert_case_001_snapshot_002_002", level="critical"),
        ],
        repository=repository,
    )

    results = simulate_send_all_pending(repository=repository)
    status = get_outbox_status(repository=repository)

    assert len(results) == 2
    assert all(result.status == "simulated_sent" for result in results)
    assert status.pending == 0
    assert status.simulated_sent == 2


def test_duplicate_alert_does_not_create_duplicate_notification(case_store_path) -> None:
    repository = CaseRepository(LocalJsonCaseStore(case_store_path))
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))
    alert = _alert(case.case_id)

    first = create_notification_from_alert(alert, repository=repository)
    second = create_notification_from_alert(alert, repository=repository)

    assert first.notification_id == second.notification_id
    assert len(repository.list_notifications()) == 1


def test_monitor_run_creates_notifications() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    monitor_response = client.post(f"/api/v1/cases/{case_id}/monitor/run")
    notifications_response = client.get(f"/api/v1/cases/{case_id}/notifications")
    outbox_response = client.get("/api/v1/notifications/outbox/status")

    assert monitor_response.status_code == 200
    assert notifications_response.status_code == 200
    notifications = notifications_response.json()
    assert len(notifications) == len(monitor_response.json()["alerts"])
    assert outbox_response.json()["total"] >= len(notifications)


def test_scheduler_run_due_creates_notifications() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    response = client.post("/api/v1/scheduler/run-due")
    notifications_response = client.get(f"/api/v1/cases/{case_id}/notifications")

    assert response.status_code == 200
    assert response.json()["executed_case_count"] == 1
    assert notifications_response.status_code == 200
    assert len(notifications_response.json()) >= 1


def test_old_alert_and_case_apis_still_work_with_notifications() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitor/run")

    assert client.get("/api/v1/alerts").status_code == 200
    assert client.get(f"/api/v1/cases/{case_id}/alerts").status_code == 200
    assert client.get(f"/api/v1/cases/{case_id}").status_code == 200
    assert client.get(f"/api/v1/cases/{case_id}/report/markdown").status_code == 200


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


def _alert(case_id: str, *, alert_id: str = "alert_case_001_snapshot_002_001", level: str = "warning") -> AlertEvent:
    return AlertEvent(
        alert_id=alert_id,
        case_id=case_id,
        snapshot_id="case_001_snapshot_002",
        level=level,
        alert_type="risk_score_increase",
        message="risk increased",
        reason="risk delta exceeded threshold",
        created_at=datetime(2026, 5, 14, 10, 0, tzinfo=timezone.utc),
    )
