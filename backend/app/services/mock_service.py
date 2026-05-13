import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.schemas.alert import AlertsResponse
from app.schemas.analysis import AnalysisResultResponse, AnalysisRunRequest, AnalysisRunResponse
from app.schemas.crawl import CrawlStartRequest, CrawlStartResponse
from app.schemas.keyword import KeywordExpandRequest, KeywordExpandResponse
from app.schemas.propagation import PropagationResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.summary import SummaryGenerateRequest, SummaryGenerateResponse
from app.schemas.visualization import VisualizationDataRequest, VisualizationResponse

MOCK_DATA_DIR = Path(__file__).resolve().parents[3] / "mock_data"


@lru_cache(maxsize=16)
def load_mock_json(filename: str) -> dict[str, Any] | list[dict[str, Any]]:
    with (MOCK_DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


def build_keyword_expansion(payload: KeywordExpandRequest) -> KeywordExpandResponse:
    keyword = payload.keyword.strip()
    expanded = [keyword, "特斯拉", "Model Y", "自动驾驶", "降价"]
    queries = [
        f"{keyword} problem",
        f"{keyword} recall",
        "特斯拉 刹车",
        "特斯拉 降价",
    ]
    return KeywordExpandResponse(
        original_keyword=keyword,
        expanded_keywords=list(dict.fromkeys(expanded)),
        search_queries=queries,
    )


def start_mock_crawl(_: CrawlStartRequest) -> CrawlStartResponse:
    return CrawlStartResponse(
        project_id="project_001",
        crawl_task_id="crawl_task_001",
        status="queued",
        message="Crawl task created. Mock data will be used in MVP mode.",
    )


def run_mock_analysis(payload: AnalysisRunRequest) -> AnalysisRunResponse:
    return AnalysisRunResponse(
        project_id=payload.project_id,
        analysis_task_id="analysis_task_001",
        status="queued",
        message="Analysis task created. Mock analysis will be returned in MVP mode.",
    )


def get_mock_analysis_result(project_id: str) -> AnalysisResultResponse:
    raw_data = load_mock_json("analysis_result.json")
    assert isinstance(raw_data, dict)
    data = dict(raw_data)
    data["project_id"] = project_id
    return AnalysisResultResponse(**data)


def get_mock_visualization(payload: VisualizationDataRequest) -> VisualizationResponse:
    raw_data = load_mock_json("visualization_response.json")
    assert isinstance(raw_data, dict)
    data = dict(raw_data)
    data["project_id"] = payload.project_id
    return VisualizationResponse(**data)


def get_mock_propagation(project_id: str) -> PropagationResponse:
    raw_data = load_mock_json("propagation_graph.json")
    assert isinstance(raw_data, dict)
    data = dict(raw_data)
    data["project_id"] = project_id
    return PropagationResponse(**data)


def generate_mock_summary(payload: SummaryGenerateRequest) -> SummaryGenerateResponse:
    comments = [
        "This product broke after two weeks.",
        "Quality control seems terrible.",
        "The timing of these posts looks unusually synchronized.",
    ]
    return SummaryGenerateResponse(
        project_id=payload.project_id,
        summary="Current public opinion is mainly negative and focused on product quality and response speed.",
        key_findings=[
            "Negative sentiment is increasing quickly across monitored platforms.",
            "The main topic is product quality and delayed customer response.",
            "Repeated negative scripts are present and should be reviewed before escalation.",
        ],
        representative_comments=comments if payload.include_representative_comments else [],
    )


def generate_mock_recommendation(_: RecommendationRequest) -> RecommendationResponse:
    return RecommendationResponse(
        summary="Current public opinion is mainly negative and focused on product quality.",
        main_risks=[
            "Quality-related complaints are spreading quickly.",
            "Repeated negative scripts suggest coordinated amplification.",
            "Delayed official response may increase distrust.",
        ],
        recommended_actions=[
            "Publish a factual clarification within 24 hours.",
            "Address the most repeated complaint directly.",
            "Avoid emotional confrontation with users.",
            "Prepare FAQ responses for customer service.",
        ],
        suggested_response=(
            "We are aware of the concerns regarding product quality and are currently investigating. "
            "We will publish verified findings and support options as soon as possible."
        ),
    )


def get_mock_alerts(project_id: str) -> AlertsResponse:
    return AlertsResponse(
        project_id=project_id,
        alerts=[
            {
                "alert_id": "alert_001",
                "level": "high",
                "message": "Negative sentiment increased by more than 30% in the last hour.",
                "created_at": "2026-05-13T11:00:00Z",
                "resolved": False,
            },
            {
                "alert_id": "alert_002",
                "level": "medium",
                "message": "Repeated-script ratio crossed the early warning threshold.",
                "created_at": "2026-05-13T12:00:00Z",
                "resolved": False,
            },
        ],
    )
