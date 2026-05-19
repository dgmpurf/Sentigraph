import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.schemas.alert import AlertsResponse
from app.schemas.analysis import AnalysisResultResponse, AnalysisRunRequest, AnalysisRunResponse
from app.schemas.crawl import CrawlStartRequest, CrawlStartResponse
from app.schemas.propagation import PropagationResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.schemas.summary import SummaryGenerateRequest, SummaryGenerateResponse
from app.schemas.visualization import VisualizationDataRequest, VisualizationResponse
from app.services.keyword import build_keyword_expansion
from app.services.mock_pipeline import (
    build_mock_pipeline,
    build_pipeline_analysis,
    build_pipeline_propagation,
    build_pipeline_visualization,
)
from app.services.recommendation.report_builder import build_public_opinion_report, rank_representative_comments
from app.services.visualization.chart_data_builder import build_visualization_response

MOCK_DATA_DIR = Path(__file__).resolve().parents[3] / "mock_data"


@lru_cache(maxsize=16)
def load_mock_json(filename: str) -> dict[str, Any] | list[dict[str, Any]]:
    with (MOCK_DATA_DIR / filename).open("r", encoding="utf-8") as file:
        return json.load(file)


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
    return build_pipeline_analysis(project_id)


def get_mock_visualization(payload: VisualizationDataRequest) -> VisualizationResponse:
    return build_pipeline_visualization(payload.project_id, platforms=payload.platforms)


def get_mock_propagation(project_id: str) -> PropagationResponse:
    return build_pipeline_propagation(project_id)


def generate_mock_summary(payload: SummaryGenerateRequest) -> SummaryGenerateResponse:
    pipeline = build_mock_pipeline(payload.project_id)
    visualization = build_visualization_response(
        payload.project_id,
        pipeline.analysis,
        clean_comments=pipeline.clean_comments,
        raw_comments=pipeline.raw_comments,
        propagation=pipeline.propagation,
        risk_result=pipeline.risk_result,
        topic_risk_result=pipeline.topic_risk_result,
    )
    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        topic_risk_result=pipeline.topic_risk_result,
        representative_comments=_pipeline_representative_comments(pipeline),
        include_representative_comments=payload.include_representative_comments,
        report_language=payload.report_language,
    )
    return SummaryGenerateResponse(
        **report.model_dump(),
        summary=report.overall_summary,
    )


def generate_mock_recommendation(payload: RecommendationRequest) -> RecommendationResponse:
    pipeline = build_mock_pipeline(payload.project_id)
    visualization = build_visualization_response(
        payload.project_id,
        pipeline.analysis,
        clean_comments=pipeline.clean_comments,
        raw_comments=pipeline.raw_comments,
        propagation=pipeline.propagation,
        risk_result=pipeline.risk_result,
        topic_risk_result=pipeline.topic_risk_result,
    )
    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        topic_risk_result=pipeline.topic_risk_result,
        representative_comments=_pipeline_representative_comments(pipeline),
        user_type=payload.user_type,
        tone=payload.tone,
        report_language=payload.report_language,
    )
    return RecommendationResponse(
        **report.model_dump(),
        summary=report.overall_summary,
        main_risks=report.main_risk_factors + report.suspected_bot_signals,
        suggested_response=report.suggested_public_response,
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


def _pipeline_representative_comments(pipeline) -> list[str]:
    sentiment_by_comment = {
        result.comment_id: result.sentiment_score for result in pipeline.sentiment_results
    }
    ranked_comments = sorted(
        pipeline.clean_comments,
        key=lambda comment: (
            sentiment_by_comment.get(comment.clean_comment_id, 0.0),
            -comment.duplicate_count,
            comment.clean_comment_id,
        ),
    )
    return rank_representative_comments(
        [comment.clean_text for comment in ranked_comments if comment.clean_text],
        topics=pipeline.analysis.topics,
        limit=5,
    )
