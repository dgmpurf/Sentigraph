import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION
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


def test_create_and_list_cases() -> None:
    create_response = client.post(
        "/api/v1/cases",
        json={"keyword": "Tesla", "platforms": ["reddit", "weibo"], "title": "Tesla Demo Case"},
    )

    assert create_response.status_code == 200
    created = create_response.json()
    assert created["case_id"] == "case_001"
    assert created["project_id"] == "project_001"
    assert created["title"] == "Tesla Demo Case"
    assert created["keyword"] == "Tesla"
    assert created["platforms"] == ["reddit", "weibo"]
    assert created["status"] == "draft"
    assert created["markdown_available"] is False

    list_response = client.get("/api/v1/cases")
    assert list_response.status_code == 200
    cases = list_response.json()
    assert len(cases) == 1
    assert cases[0]["case_id"] == "case_001"
    assert cases[0]["status"] == "draft"


def test_run_case_attaches_mock_pipeline_outputs() -> None:
    case_id = _create_case()

    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    assert body["status"] == "completed"
    assert body["risk_score"] is not None
    assert body["risk_level"] in {"low", "medium", "high", "critical"}
    assert body["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert body["analysis_result"]["project_id"] == body["project_id"]
    assert body["analysis_result"]["topic_risks"]
    assert body["visualization_data"]["project_id"] == body["project_id"]
    assert body["visualization_data"]["top_risk_topics"]
    assert body["report"]["report_language"] == "zh-CN"
    assert body["report"]["top_risk_topics"]
    assert body["markdown_available"] is True


def test_get_case_detail_after_run() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    detail_response = client.get(f"/api/v1/cases/{case_id}")

    assert detail_response.status_code == 200
    body = detail_response.json()
    assert body["case_id"] == case_id
    assert body["status"] == "completed"
    assert body["analysis_result"]["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert body["report"]["risk_model_version"] == TOPIC_RISK_MODEL_VERSION


def test_export_markdown_report() -> None:
    case_id = _create_case()
    client.post(f"/api/v1/cases/{case_id}/run")

    report_response = client.get(f"/api/v1/cases/{case_id}/report/markdown")

    assert report_response.status_code == 200
    body = report_response.json()
    assert body["case_id"] == case_id
    assert body["filename"].endswith(".md")
    assert body["markdown"].startswith("# Tesla")
    assert "## 舆情总览" in body["markdown"]
    assert "## 高风险话题" in body["markdown"]
    assert "建议公开回应文案" in body["markdown"]
    assert TOPIC_RISK_MODEL_VERSION in body["markdown"]


def test_case_api_persists_after_repository_reload(case_store_path) -> None:
    case_id = _create_case()
    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200

    configure_case_repository(CaseRepository(LocalJsonCaseStore(case_store_path)))

    detail_response = client.get(f"/api/v1/cases/{case_id}")
    markdown_response = client.get(f"/api/v1/cases/{case_id}/report/markdown")

    assert detail_response.status_code == 200
    detail = detail_response.json()
    assert detail["case_id"] == case_id
    assert detail["status"] == "completed"
    assert detail["analysis_result"]["topic_risks"]
    assert detail["report"]["report_language"] == "zh-CN"
    assert detail["markdown_available"] is True

    assert markdown_response.status_code == 200
    markdown = markdown_response.json()
    assert markdown["case_id"] == case_id
    assert TOPIC_RISK_MODEL_VERSION in markdown["markdown"]


def test_case_markdown_requires_completed_report() -> None:
    case_id = _create_case()

    response = client.get(f"/api/v1/cases/{case_id}/report/markdown")

    assert response.status_code == 404


def test_old_mock_endpoints_still_work() -> None:
    health_response = client.get("/api/v1/health")
    visualization_response = client.post(
        "/api/v1/visualization/data",
        json={"project_id": "project_001", "platforms": ["reddit", "weibo"]},
    )
    summary_response = client.post(
        "/api/v1/summary/generate",
        json={"project_id": "project_001", "report_language": "zh-CN"},
    )
    analysis_response = client.get("/api/v1/analysis/project_001")

    assert health_response.status_code == 200
    assert visualization_response.status_code == 200
    assert visualization_response.json()["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert summary_response.status_code == 200
    assert summary_response.json()["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert analysis_response.status_code == 200
    assert analysis_response.json()["risk_model_version"] == TOPIC_RISK_MODEL_VERSION


def _create_case() -> str:
    response = client.post(
        "/api/v1/cases",
        json={
            "keyword": "Tesla",
            "platforms": ["reddit", "weibo", "bilibili"],
            "title": "Tesla 舆情案例",
        },
    )
    assert response.status_code == 200
    return response.json()["case_id"]
