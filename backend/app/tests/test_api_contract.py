from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_contract() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"]


def test_keyword_expand_contract() -> None:
    response = client.post(
        "/api/v1/keywords/expand",
        json={"keyword": "Tesla", "platforms": ["reddit", "weibo"], "language": "auto"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["original_keyword"] == "Tesla"
    assert "expanded_keywords" in body
    assert "search_queries" in body


def test_visualization_response_structure() -> None:
    response = client.post(
        "/api/v1/visualization/data",
        json={
            "project_id": "project_001",
            "date_range": {"start": "2026-05-01", "end": "2026-05-13"},
            "platforms": ["reddit", "weibo"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "project_001"
    assert isinstance(body["sentiment_trend"], list)
    assert isinstance(body["propagation_graph"]["nodes"], list)
    assert isinstance(body["risk_radar"]["negative_sentiment"], float)


def test_crawl_and_analysis_task_contracts() -> None:
    crawl_response = client.post(
        "/api/v1/crawl/start",
        json={
            "keyword": "Tesla",
            "platforms": ["reddit"],
            "limit": 100,
            "date_range": {"start": "2026-05-01", "end": "2026-05-13"},
        },
    )
    assert crawl_response.status_code == 200
    assert crawl_response.json()["status"] == "queued"

    analysis_response = client.post(
        "/api/v1/analysis/run",
        json={
            "project_id": crawl_response.json()["project_id"],
            "analysis_types": ["sentiment", "topic", "bot", "ai_generated", "propagation", "risk"],
        },
    )
    assert analysis_response.status_code == 200
    assert analysis_response.json()["status"] == "queued"


def test_analysis_result_contract() -> None:
    response = client.get("/api/v1/analysis/project_001")
    assert response.status_code == 200
    body = response.json()
    assert body["risk"]["risk_level"] in {"low", "medium", "high", "critical"}
    assert body["bot_score"]["suspected_bot_ratio"] >= 0
    assert body["sentiment_results"]
    assert body["topics"]


def test_summary_recommendation_propagation_and_alert_contracts() -> None:
    summary_response = client.post(
        "/api/v1/summary/generate",
        json={"project_id": "project_001", "include_representative_comments": True},
    )
    assert summary_response.status_code == 200
    assert summary_response.json()["representative_comments"]

    recommendation_response = client.post(
        "/api/v1/recommendation/generate",
        json={"project_id": "project_001", "user_type": "brand", "tone": "professional"},
    )
    assert recommendation_response.status_code == 200
    assert recommendation_response.json()["recommended_actions"]

    propagation_response = client.get("/api/v1/propagation/project_001")
    assert propagation_response.status_code == 200
    assert propagation_response.json()["metrics"]["central_node_id"] == "post_001"

    alerts_response = client.get("/api/v1/alerts/project_001")
    assert alerts_response.status_code == 200
    assert alerts_response.json()["alerts"][0]["level"] == "high"
