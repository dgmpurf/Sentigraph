from fastapi.testclient import TestClient

from app.main import app
from app.schemas.analysis import (
    AnalysisResultResponse,
    BotImpactSummary,
    RiskBrief,
    SentimentSummary,
    TopicCluster,
)
from app.schemas.common import RISK_MODEL_VERSION
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION
from app.schemas.recommendation import RecommendationResponse
from app.schemas.summary import SummaryGenerateResponse
from app.schemas.visualization import SentimentTrendPoint
from app.services.mock_pipeline import build_mock_pipeline
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.visualization.chart_data_builder import build_visualization_response


client = TestClient(app)


NORMALIZED_REPORT_FIELDS = {
    "project_id",
    "report_language",
    "risk_score",
    "risk_level",
    "risk_level_label",
    "risk_model_version",
    "overall_summary",
    "key_findings",
    "main_risk_factors",
    "top_negative_topics",
    "representative_comments",
    "suspected_bot_signals",
    "recommended_actions",
    "suggested_public_response",
    "generated_from_mock_pipeline",
    "topic_risks",
    "top_risk_topics",
    "max_topic_risk",
    "average_topic_risk",
    "overall_risk",
    "real_crisis_risk",
    "manipulation_risk",
    "risk_explanation",
    "evidence_item_count",
    "evidence_source_distribution",
    "evidence_type_counts",
    "evidence_trust_label_distribution",
    "evidence_verification_status_distribution",
    "evidence_provenance_type_distribution",
    "evidence_review_needed_count",
    "evidence_review_excluded_count",
    "evidence_unique_item_count",
    "evidence_duplicate_item_count",
}


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
    assert report.report_language == "zh-CN"
    assert report.overall_summary.startswith("本次离线模拟管线评估显示")
    assert report.project_id == "project_001"
    assert report.risk_score == pipeline.analysis.risk.risk_score
    assert report.risk_level == pipeline.analysis.risk.risk_level
    assert report.risk_level_label in {"低风险", "中等风险", "高风险", "严重风险"}
    assert report.risk_model_version == RISK_MODEL_VERSION
    assert report.main_risk_factors
    assert report.top_negative_topics
    assert report.key_findings
    assert report.representative_comments
    assert report.suspected_bot_signals
    assert report.recommended_actions
    assert report.suggested_public_response
    assert report.generated_from_mock_pipeline is True

    assert set(report.model_dump()) == NORMALIZED_REPORT_FIELDS


def test_report_builder_supports_en_us_output() -> None:
    pipeline, visualization = _pipeline_with_visualization()

    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        representative_comments=[comment.clean_text for comment in pipeline.clean_comments],
        report_language="en-US",
    )

    assert report.report_language == "en-US"
    assert report.risk_level_label == f"{report.risk_level} risk"
    assert report.risk_model_version == RISK_MODEL_VERSION
    assert report.overall_summary.startswith("Public opinion risk")
    assert any("Negative sentiment" in factor for factor in report.main_risk_factors)
    assert any("Publish a factual" in action for action in report.recommended_actions)
    assert report.suggested_public_response.startswith("We are aware")


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


def test_report_builder_downranks_promotional_representative_comments() -> None:
    analysis = AnalysisResultResponse(
        project_id="project_youtube_quality",
        summary="Offline deterministic analysis from attached case raw data.",
        sentiment=SentimentSummary(
            positive_ratio=0.1,
            neutral_ratio=0.2,
            negative_ratio=0.7,
            average_sentiment_score=-0.5,
        ),
        topics=[
            TopicCluster(
                cluster_id="topic_001",
                topic="Product quality issues",
                summary="Users discuss quality and response timing.",
                comment_count=6,
                average_sentiment_score=-0.6,
                representative_comments=[],
            )
        ],
        conflicts=[],
        bot_score=BotImpactSummary(suspected_bot_ratio=0.0, suspected_bot_comment_ratio=0.0),
        risk=RiskBrief(risk_score=72, risk_level="high"),
    )
    promotional = "Subscribe to my channel and join my Patreon for a promo code."
    merch_promotional = "Use my discount code for merch and subscribe for more updates."
    substantive_comments = [
        "Tesla quality issue looks serious because the official response timeline is still unclear.",
        "The safety concern needs evidence and a clearer product support path.",
        "A delayed response makes the problem feel worse for affected owners.",
        "The issue should be addressed with a transparent refund or repair timeline.",
        "Trust recovery depends on direct evidence, not channel promotion.",
    ]

    report = build_public_opinion_report(
        analysis,
        representative_comments=[promotional, merch_promotional, *substantive_comments],
        report_language="en-US",
    )

    assert promotional not in report.representative_comments
    assert merch_promotional not in report.representative_comments
    assert all("discount code" not in comment.lower() for comment in report.representative_comments)
    assert all("merch" not in comment.lower() for comment in report.representative_comments)
    assert report.representative_comments[0] == substantive_comments[0]
    assert len(report.representative_comments) == 5


def test_report_builder_uses_visualization_trend_and_graph_outputs() -> None:
    pipeline, visualization = _pipeline_with_visualization()
    trend_visualization = visualization.model_copy(
        update={
            "sentiment_trend": [
                SentimentTrendPoint(time="2026-05-13T10:00:00Z", positive=50, neutral=30, negative=20),
                SentimentTrendPoint(time="2026-05-13T11:00:00Z", positive=10, neutral=25, negative=65),
            ]
        }
    )

    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=trend_visualization,
        risk_factors=pipeline.risk_result.factors,
        report_language="en-US",
    )

    assert any("Negative sentiment trend rose from 20% to 65%" in item for item in report.main_risk_factors)
    assert any("Visualization propagation graph includes" in item for item in report.main_risk_factors)
    assert "2 sentiment time bucket(s)" in report.overall_summary


def test_report_builder_adds_urgent_actions_for_high_risk_and_high_bot_impact() -> None:
    analysis = AnalysisResultResponse(
        project_id="project_high_risk",
        summary="High risk mock analysis.",
        sentiment=SentimentSummary(
            positive_ratio=0.05,
            neutral_ratio=0.15,
            negative_ratio=0.8,
            average_sentiment_score=-0.72,
        ),
        topics=[
            TopicCluster(
                cluster_id="topic_001",
                topic="Service failure",
                summary="Users report unresolved service failure.",
                comment_count=24,
                average_sentiment_score=-0.82,
                representative_comments=["The issue has not been addressed."],
            )
        ],
        conflicts=[],
        bot_score=BotImpactSummary(suspected_bot_ratio=0.25, suspected_bot_comment_ratio=0.48),
        risk=RiskBrief(risk_score=88, risk_level="high"),
    )

    report = build_public_opinion_report(
        analysis,
        risk_factors={
            "negative_sentiment_ratio": 0.8,
            "negative_sentiment_strength": 0.72,
            "bot_impact_score": 0.48,
            "propagation_speed": 0.62,
            "controversy_score": 0.4,
            "trend_shift": 0.3,
        },
    )

    assert report.report_language == "zh-CN"
    assert any("24小时" in action for action in report.recommended_actions)
    assert any("重复话术" in signal for signal in report.suspected_bot_signals)
    assert "官方渠道" in report.suggested_public_response


def test_report_builder_handles_missing_optional_pipeline_outputs() -> None:
    analysis = AnalysisResultResponse(
        project_id="project_minimal",
        summary="Minimal mock analysis.",
        sentiment=SentimentSummary(
            positive_ratio=0.2,
            neutral_ratio=0.3,
            negative_ratio=0.5,
            average_sentiment_score=-0.2,
        ),
        topics=[
            TopicCluster(
                cluster_id="topic_001",
                topic="Product quality issues",
                summary="Users discuss quality concerns.",
                comment_count=7,
                average_sentiment_score=-0.6,
                representative_comments=["Quality needs a clear response."],
            )
        ],
        conflicts=[],
        bot_score=BotImpactSummary(suspected_bot_ratio=0.0, suspected_bot_comment_ratio=0.0),
        risk=RiskBrief(risk_score=62, risk_level="medium"),
    )

    report = build_public_opinion_report(analysis)

    assert report.overall_summary.startswith("本次离线模拟管线评估显示")
    assert report.top_negative_topics == [
        "Product quality issues：7条评论，平均情绪-0.60"
    ]
    assert report.representative_comments == ["Quality needs a clear response."]
    assert report.suspected_bot_signals == ["当前模拟阈值下未发现强疑似机器人账号信号。"]
    assert report.suggested_public_response


def test_summary_endpoint_returns_report_based_schema_output() -> None:
    response = client.post(
        "/api/v1/summary/generate",
        json={"project_id": "project_001", "include_representative_comments": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] == "project_001"
    assert body["report_language"] == "zh-CN"
    assert body["overall_summary"].startswith("本次离线模拟管线评估显示")
    assert body["summary"] == body["overall_summary"]
    assert body["risk_level"] in {"low", "medium", "high", "critical"}
    assert body["risk_level_label"] in {"低风险", "中等风险", "高风险", "严重风险"}
    assert body["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert isinstance(body["risk_score"], int)
    assert isinstance(body["key_findings"], list)
    assert isinstance(body["main_risk_factors"], list)
    assert isinstance(body["top_negative_topics"], list)
    assert isinstance(body["suspected_bot_signals"], list)
    assert isinstance(body["recommended_actions"], list)
    assert isinstance(body["suggested_public_response"], str)
    assert isinstance(body["representative_comments"], list)
    assert body["generated_from_mock_pipeline"] is True
    assert body["topic_risks"]
    assert body["top_risk_topics"]
    assert body["overall_risk"] is not None
    assert body["key_findings"]
    SummaryGenerateResponse(**body)


def test_recommendation_endpoint_returns_report_based_schema_output() -> None:
    response = client.post(
        "/api/v1/recommendation/generate",
        json={"project_id": "project_001", "user_type": "brand", "tone": "professional"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["report_language"] == "zh-CN"
    assert body["risk_level_label"] in {"低风险", "中等风险", "高风险", "严重风险"}
    assert body["risk_model_version"] == TOPIC_RISK_MODEL_VERSION
    assert body["overall_summary"].startswith("本次离线模拟管线评估显示")
    assert body["summary"] == body["overall_summary"]
    assert body["suggested_response"] == body["suggested_public_response"]
    assert isinstance(body["main_risks"], list)
    assert isinstance(body["main_risk_factors"], list)
    assert isinstance(body["top_negative_topics"], list)
    assert isinstance(body["suspected_bot_signals"], list)
    assert isinstance(body["recommended_actions"], list)
    assert isinstance(body["suggested_response"], str)
    assert body["generated_from_mock_pipeline"] is True
    assert body["topic_risks"]
    assert body["top_risk_topics"]
    assert body["overall_risk"] is not None
    assert body["main_risks"]
    assert body["recommended_actions"]
    assert body["suggested_response"]
    RecommendationResponse(**body)
