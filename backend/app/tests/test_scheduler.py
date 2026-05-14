from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_cases(case_store_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))
    reset_case_store()


@pytest.fixture
def case_store_path(tmp_path):
    return tmp_path / "cases.json"


def test_default_monitoring_config() -> None:
    case_id = _create_case()

    response = client.get(f"/api/v1/cases/{case_id}/monitoring/config")

    assert response.status_code == 200
    config = response.json()
    assert config["enabled"] is False
    assert config["interval_minutes"] == 60
    assert config["last_run_at"] is None
    assert config["next_run_at"] is None
    assert config["status"] == "disabled"
    assert config["threshold_config"]["risk_score_delta_warning"] == 10


def test_enable_monitoring() -> None:
    case_id = _create_case()

    response = client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    assert response.status_code == 200
    config = response.json()
    assert config["enabled"] is True
    assert config["status"] == "due"
    assert config["next_run_at"] is not None


def test_disable_monitoring() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    response = client.post(f"/api/v1/cases/{case_id}/monitoring/disable")

    assert response.status_code == 200
    config = response.json()
    assert config["enabled"] is False
    assert config["status"] == "disabled"
    assert config["next_run_at"] is None


def test_update_monitoring_interval() -> None:
    case_id = _create_case()
    config = client.post(f"/api/v1/cases/{case_id}/monitoring/enable").json()
    config["interval_minutes"] = 30

    response = client.put(f"/api/v1/cases/{case_id}/monitoring/config", json=config)

    assert response.status_code == 200
    updated = response.json()
    assert updated["enabled"] is True
    assert updated["interval_minutes"] == 30
    assert updated["status"] == "due"


def test_run_due_with_no_enabled_cases() -> None:
    _create_case()

    response = client.post("/api/v1/scheduler/run-due")

    assert response.status_code == 200
    body = response.json()
    assert body["due_case_count"] == 0
    assert body["executed_case_count"] == 0
    assert body["skipped_case_count"] == 0
    assert body["monitoring_results"] == []


def test_run_due_with_enabled_due_case() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    response = client.post("/api/v1/scheduler/run-due")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")
    config_response = client.get(f"/api/v1/cases/{case_id}/monitoring/config")

    assert response.status_code == 200
    body = response.json()
    assert body["due_case_count"] == 1
    assert body["executed_case_count"] == 1
    assert body["skipped_case_count"] == 0
    assert len(body["monitoring_results"]) == 1
    assert snapshots_response.status_code == 200
    assert len(snapshots_response.json()) == 2

    config = config_response.json()
    assert config["last_run_at"] is not None
    assert config["next_run_at"] is not None
    assert config["status"] == "scheduled"

    alerts_response = client.get(f"/api/v1/cases/{case_id}/alerts")
    assert alerts_response.status_code == 200
    assert isinstance(alerts_response.json(), list)


def test_run_due_does_not_run_not_due_case() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")
    client.post("/api/v1/scheduler/run-due")

    response = client.post("/api/v1/scheduler/run-due")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")

    assert response.status_code == 200
    body = response.json()
    assert body["due_case_count"] == 0
    assert body["executed_case_count"] == 0
    assert body["skipped_case_count"] == 1
    assert len(snapshots_response.json()) == 2


def test_run_due_does_not_run_disabled_case() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")
    client.post(f"/api/v1/cases/{case_id}/monitoring/disable")

    response = client.post("/api/v1/scheduler/run-due")
    snapshots_response = client.get(f"/api/v1/cases/{case_id}/snapshots")

    assert response.status_code == 200
    body = response.json()
    assert body["due_case_count"] == 0
    assert body["executed_case_count"] == 0
    assert body["skipped_case_count"] == 0
    assert len(snapshots_response.json()) == 1


def test_run_due_updates_last_and_next_run_at_by_interval() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    config = client.post(f"/api/v1/cases/{case_id}/monitoring/enable").json()
    config["interval_minutes"] = 30
    client.put(f"/api/v1/cases/{case_id}/monitoring/config", json=config)

    response = client.post("/api/v1/scheduler/run-due")
    config_response = client.get(f"/api/v1/cases/{case_id}/monitoring/config")

    assert response.status_code == 200
    config = config_response.json()
    last_run_at = _parse_datetime(config["last_run_at"])
    next_run_at = _parse_datetime(config["next_run_at"])
    assert config["interval_minutes"] == 30
    assert (next_run_at - last_run_at).total_seconds() == 30 * 60


def test_run_due_uses_case_threshold_config() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")
    config = client.post(f"/api/v1/cases/{case_id}/monitoring/enable").json()
    config["threshold_config"]["risk_score_delta_warning"] = 99
    config["threshold_config"]["risk_score_delta_critical"] = 100
    config["threshold_config"]["real_crisis_delta_warning"] = 99
    config["threshold_config"]["manipulation_delta_warning"] = 99
    config["threshold_config"]["topic_risk_high"] = 99
    config["threshold_config"]["topic_risk_critical"] = 100
    client.put(f"/api/v1/cases/{case_id}/monitoring/config", json=config)

    response = client.post("/api/v1/scheduler/run-due")

    assert response.status_code == 200
    body = response.json()
    assert body["executed_case_count"] == 1
    assert body["monitoring_results"][0]["status"] == "stable"
    assert body["monitoring_results"][0]["alerts"] == []


def test_scheduler_state_survives_store_reload(case_store_path) -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))

    response = client.get(f"/api/v1/cases/{case_id}/monitoring/config")

    assert response.status_code == 200
    config = response.json()
    assert config["enabled"] is True
    assert config["status"] == "due"
    assert config["next_run_at"] is not None


def test_old_monitor_run_endpoint_still_works() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    response = client.post(f"/api/v1/cases/{case_id}/monitor/run")

    assert response.status_code == 200
    body = response.json()
    assert body["case_id"] == case_id
    assert body["snapshot_count"] == 2


def test_scheduler_status_reports_enabled_and_due_jobs() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/monitoring/enable")

    response = client.get("/api/v1/scheduler/status")

    assert response.status_code == 200
    body = response.json()
    assert body["background_scheduler_running"] is False
    assert body["total_cases"] == 1
    assert body["enabled_cases"] == 1
    assert body["due_cases"] == 1
    assert body["job_states"][0]["case_id"] == case_id


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


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
