from datetime import datetime, timezone

from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest, MarkdownExportResponse
from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import PlatformCrawlMetadata
from app.services.mock_pipeline import build_mock_pipeline
from app.services.mock_service import _pipeline_representative_comments
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.storage.local_json_store import LocalJsonCaseStore
from app.services.visualization.chart_data_builder import build_visualization_response


def test_local_json_store_create_list_get_update_and_reload(tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    repository = CaseRepository(LocalJsonCaseStore(store_path))

    created = repository.create_case(
        AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit", "weibo"], title="Tesla Demo")
    )
    running = created.model_copy(update={"status": "running", "updated_at": repository.next_timestamp()})
    repository.update_case(running)

    reloaded_repository = CaseRepository(LocalJsonCaseStore(store_path))
    cases = reloaded_repository.list_cases()
    detail = reloaded_repository.get_case(created.case_id)

    assert store_path.exists()
    assert len(cases) == 1
    assert cases[0].case_id == "case_001"
    assert detail is not None
    assert detail.status == "running"
    assert detail.platforms == ["reddit", "weibo"]


def test_local_json_store_generates_next_case_after_reload(tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    repository = CaseRepository(LocalJsonCaseStore(store_path))
    repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))

    reloaded_repository = CaseRepository(LocalJsonCaseStore(store_path))
    second = reloaded_repository.create_case(AnalysisCaseCreateRequest(keyword="BYD", platforms=["weibo"]))

    assert second.case_id == "case_002"
    assert second.project_id == "project_002"
    assert second.title == "BYD 舆情分析"


def test_local_json_store_saves_analysis_result_report_and_markdown(tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    repository = CaseRepository(LocalJsonCaseStore(store_path))
    case = repository.create_case(
        AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit", "weibo"], title="Tesla Demo")
    )
    pipeline = build_mock_pipeline(case.project_id, platforms=case.platforms)
    visualization = build_visualization_response(
        case.project_id,
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
        include_representative_comments=True,
        report_language="zh-CN",
    )

    repository.save_analysis_result(
        case.case_id,
        analysis_result=pipeline.analysis,
        visualization_data=visualization,
        risk_score=pipeline.topic_risk_result.overall_risk,
        risk_level=pipeline.topic_risk_result.risk_level,
        risk_model_version=pipeline.topic_risk_result.risk_model_version,
    )
    repository.save_report(case.case_id, report=report)
    repository.save_markdown_report(
        case.case_id,
        MarkdownExportResponse(
            case_id=case.case_id,
            project_id=case.project_id,
            filename="tesla_demo.md",
            markdown="# Tesla Demo\n\nMock Markdown report.",
            generated_at=datetime(2026, 5, 14, 10, 0, tzinfo=timezone.utc),
        ),
    )

    reloaded_repository = CaseRepository(LocalJsonCaseStore(store_path))
    detail = reloaded_repository.get_case(case.case_id)
    markdown = reloaded_repository.get_markdown_report(case.case_id)

    assert detail is not None
    assert detail.analysis_result is not None
    assert detail.analysis_result.project_id == case.project_id
    assert detail.visualization_data is not None
    assert detail.report is not None
    assert detail.report.report_language == "zh-CN"
    assert detail.markdown_available is True
    assert markdown is not None
    assert markdown.filename == "tesla_demo.md"
    assert "Mock Markdown report." in markdown.markdown


def test_local_json_store_persists_attached_raw_crawl_data_after_reload(tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    repository = CaseRepository(LocalJsonCaseStore(store_path))
    case = repository.create_case(
        AnalysisCaseCreateRequest(keyword="Tesla", platforms=["youtube"], title="Tesla YouTube Demo")
    )

    attached = repository.save_case_raw_data(
        case.case_id,
        raw_posts=[_raw_post()],
        raw_comments=[_raw_comment()],
        crawl_metadata=[
            PlatformCrawlMetadata(
                platform="youtube",
                adapter_mode="real",
                source_type="youtube_data_api_v3",
                fetch_status="real",
                credential_present=True,
                post_count=1,
                comment_count=1,
                raw_post_schema_valid=True,
                raw_comment_schema_valid=True,
            )
        ],
        crawl_source_mode="case_crawl_start",
        raw_data_status="attached",
        attached_at=datetime(2026, 5, 14, 10, 30, tzinfo=timezone.utc),
    )

    reloaded_repository = CaseRepository(LocalJsonCaseStore(store_path))
    detail = reloaded_repository.get_case(case.case_id)

    assert attached is not None
    assert detail is not None
    assert detail.raw_data_status == "attached"
    assert detail.crawl_source_mode == "case_crawl_start"
    assert detail.crawl_attached_at == datetime(2026, 5, 14, 10, 30, tzinfo=timezone.utc)
    assert detail.raw_post_count == 1
    assert detail.raw_comment_count == 1
    assert detail.raw_posts[0].platform == "youtube"
    assert detail.raw_comments[0].content == "YouTube fixture QA comment survives local JSON reload."
    assert detail.crawl_metadata[0].credential_present is True
    assert "YOUTUBE_API_KEY" not in detail.model_dump_json()


def _raw_post() -> RawPost:
    return RawPost(
        platform="youtube",
        post_id="yt_reload_video_001",
        author_id="yt_reload_channel",
        author_name="Fixture Channel",
        title="Reload-safe YouTube fixture",
        content="Safe public fixture description.",
        like_count=12,
        reply_count=1,
        share_count=0,
        created_at="2026-05-17T12:00:00Z",
        url="https://www.youtube.com/watch?v=yt_reload_video_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
    )


def _raw_comment() -> RawComment:
    return RawComment(
        platform="youtube",
        post_id="yt_reload_video_001",
        comment_id="yt_reload_comment_001",
        parent_id=None,
        author_id="yt_reload_commenter",
        author_name="Fixture Viewer",
        content="YouTube fixture QA comment survives local JSON reload.",
        like_count=3,
        reply_count=0,
        share_count=0,
        created_at="2026-05-17T12:05:00Z",
        url="https://www.youtube.com/watch?v=yt_reload_video_001&lc=yt_reload_comment_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
    )
