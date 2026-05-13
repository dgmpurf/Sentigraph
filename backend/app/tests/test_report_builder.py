from fastapi.testclient import TestClient

from app.main import app
from app.schemas.recommendation import RecommendationResponse
from app.schemas.summary import SummaryGenerateResponse
from app.services.mock_pipeline import build_mock_pipeline
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.visualization.chart_data_builder import build_visualization_response


client = TestClient(app)


def _pipeline_with_visualization(project_id: str = "project_001"):
    pipeline = build_mock_pipeline(project_id)
    visualization = build_visualization_response(
        project_id,
        pipeline.analysis,
        clean_comments=pipeline.clean_comments,
        raw_comments=pipeline.raw_comments,
        propagation=pipeline.propagation,
        risk_result=pipeline.risk_result,
    )
    return pipeline, visualization


def test_report_builder_is_deterministic_and_offline(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    pipeline, visualization = _pipeline_with_visualization()

    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        representative_comments=[comment.clean_text for comment in pipeline.clean_comments],
    )
    second_report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        representative_comments=[comment.clean_text for comment in pipeline.clean_comments],
    )

    assert report.model_dump() == second_report.model_dump()
    assert report.overall_summary.startswith("Public opinion risk")
    assert report.main_risk_factors
    assert report.top_negative_topics
    assert report.representative_comments
    assert report.suspected_bot_signals
    assert report.recommended_actions
    assert report.suggested_public_response

    assert set(report.model_dump()) == {
        "overall_summary",
        "main_risk_factors",
        "top_negative_topics",
        "representative_comments",
        "suspected_bot_signals",
        "recommended_actions",
        "suggested_public_response",
    }


def test_report_builder_can_omit_representative_comments() -> None:
    pipeline, visualization = _pipeline_with_visualization()

    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        representative_comments=[comment.clean_text for comment in pipeline.clean_comments],
        include_representative_comments=False,
    )

    assert report.representative_comments == []


def test_summary_endpoint_returns_report_based_schema_output() -> None:
    response = client.post(
        "/api/v1/summary/generate",
        json={"project_id": "project_001", "include_representative_comments": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "project_001"
    assert body["summary"].startswith("Public opinion risk")
    assert isinstance(body["key_findings"], list)
    assert isinstance(body["representative_comments"], list)
    assert body["key_findings"]
    SummaryGenerateResponse(**body)


def test_recommendation_endpoint_returns_report_based_schema_output() -> None:
    response = client.post(
        "/api/v1/recommendation/generate",
        json={"project_id": "project_001", "user_type": "brand", "tone": "professional"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"].startswith("Public opinion risk")
    assert isinstance(body["main_risks"], list)
    assert isinstance(body["recommended_actions"], list)
    assert isinstance(body["suggested_response"], str)
    assert body["main_risks"]
    assert body["recommended_actions"]
    assert body["suggested_response"]
    RecommendationResponse(**body)
