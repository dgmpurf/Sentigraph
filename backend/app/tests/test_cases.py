import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseDetail
from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import CrawlStartResponse, PlatformCrawlMetadata
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
    assert body["analysis_result"]["analysis_input_source"] == "mock_data_fallback"
    assert body["analysis_input_source"] == "mock_data_fallback"
    assert body["raw_data_status"] == "missing"


def test_case_detail_defaults_keep_old_case_documents_loadable() -> None:
    old_case = AnalysisCaseDetail.model_validate(
        {
            "case_id": "case_old",
            "project_id": "project_old",
            "title": "Old persisted case",
            "keyword": "Tesla",
            "platforms": ["reddit"],
            "status": "draft",
            "created_at": "2026-05-14T09:00:00Z",
            "updated_at": "2026-05-14T09:00:00Z",
        }
    )

    assert old_case.raw_posts == []
    assert old_case.raw_comments == []
    assert old_case.crawl_metadata == []
    assert old_case.raw_data_status == "missing"
    assert old_case.raw_post_count == 0
    assert old_case.raw_comment_count == 0


def test_case_specific_crawl_start_stores_youtube_raw_data(monkeypatch) -> None:
    fake_key_marker = "youtube-test-marker-should-not-appear"
    case_id = _create_case(platforms=["youtube"])

    def fake_start_crawl(payload):
        assert payload.keyword == "Tesla"
        assert payload.platforms == ["youtube"]
        assert payload.limit == 3
        return _youtube_crawl_response()

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)

    response = client.post(
        f"/api/v1/cases/{case_id}/crawl/start",
        json={"limit": 3},
    )

    assert response.status_code == 200
    assert fake_key_marker not in response.text
    body = response.json()
    assert body["case_id"] == case_id
    assert body["raw_data_status"] == "attached"
    assert body["crawl_source_mode"] == "case_crawl_start"
    assert body["crawl_attached_at"]
    assert body["raw_post_count"] == 1
    assert body["raw_comment_count"] == 2
    assert body["raw_posts"][0]["platform"] == "youtube"
    assert body["raw_comments"][0]["platform"] == "youtube"
    assert body["crawl_metadata"][0]["credential_present"] is True
    assert fake_key_marker not in str(body["raw_posts"])
    assert fake_key_marker not in str(body["raw_comments"])


def test_case_specific_crawl_start_uses_case_defaults_without_body(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])

    def fake_start_crawl(payload):
        assert payload.keyword == "Tesla"
        assert payload.platforms == ["youtube"]
        return _youtube_crawl_response()

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)

    response = client.post(f"/api/v1/cases/{case_id}/crawl/start")

    assert response.status_code == 200
    body = response.json()
    assert body["raw_data_status"] == "attached"
    assert body["raw_comment_count"] == 2


def test_run_case_uses_attached_youtube_raw_comments(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])
    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", lambda payload: _youtube_crawl_response())
    attach_response = client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})
    assert attach_response.status_code == 200

    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    assert body["status"] == "completed"
    assert body["analysis_input_source"] == "case_raw_data"
    assert body["analysis_result"]["analysis_input_source"] == "case_raw_data"
    assert body["analysis_result"]["summary"].startswith(
        "Offline deterministic analysis from attached case raw data"
    )
    assert "Mock pipeline analysis" not in body["analysis_result"]["summary"]
    assert body["analysis_result"]["raw_post_count"] == 1
    assert body["analysis_result"]["raw_comment_count"] == 2
    assert body["report"]["generated_from_mock_pipeline"] is False
    assert any(
        "youtube fixture quality issue comment" in comment
        for comment in body["report"]["representative_comments"]
    )

    markdown_response = client.get(f"/api/v1/cases/{case_id}/report/markdown")
    assert markdown_response.status_code == 200
    markdown = markdown_response.json()["markdown"]
    assert "youtube fixture quality issue comment" in markdown
    assert "youtube fixture support comment" in markdown
    assert "I think this product has serious quality issues." not in markdown
    assert "raw_data" not in markdown
    assert '"source_type"' not in markdown


def test_youtube_raw_data_report_downranks_promotional_comments(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])
    monkeypatch.setattr(
        "app.services.case_store.start_crawl_with_adapters",
        lambda payload: _youtube_crawl_response_with_promotional_comment(),
    )
    attach_response = client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})
    assert attach_response.status_code == 200
    attached = attach_response.json()
    assert any("patreon" in comment["content"].lower() for comment in attached["raw_comments"])

    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    representative_comments = body["report"]["representative_comments"]
    assert body["analysis_input_source"] == "case_raw_data"
    assert any("official response timeline" in comment for comment in representative_comments)
    assert all("patreon" not in comment.lower() for comment in representative_comments)
    assert all("promo code" not in comment.lower() for comment in representative_comments)


def test_case_specific_crawl_start_missing_case_returns_404(monkeypatch) -> None:
    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", lambda payload: _youtube_crawl_response())

    response = client.post("/api/v1/cases/case_missing/crawl/start", json={"limit": 3})

    assert response.status_code == 404


def test_simulation_initializer_works_after_youtube_based_case_analysis(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])
    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", lambda payload: _youtube_crawl_response())
    client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})
    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200

    response = client.get(f"/api/v1/cases/{case_id}/simulation/initialization-preview")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"initialized", "partial"}
    assert body["simulation_scenario"]["name"]
    assert "insufficient_observed_comment_count" in body["warnings"]
    assert "yt_fixture_commenter" not in response.text
    assert "influenceability_score" not in response.text


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


def _create_case(platforms: list[str] | None = None) -> str:
    response = client.post(
        "/api/v1/cases",
        json={
            "keyword": "Tesla",
            "platforms": platforms or ["reddit", "weibo", "bilibili"],
            "title": "Tesla 舆情案例",
        },
    )
    assert response.status_code == 200
    return response.json()["case_id"]


def _youtube_crawl_response() -> CrawlStartResponse:
    return CrawlStartResponse(
        project_id="project_001",
        crawl_task_id="crawl_task_youtube_fixture",
        status="queued",
        message="Fixture YouTube crawl response.",
        platform_metadata=[
            PlatformCrawlMetadata(
                platform="youtube",
                adapter_mode="real",
                source_type="youtube_data_api_v3",
                fallback_used=False,
                fetch_status="real",
                credential_present=True,
                real_mode_available=True,
                selectable_for_real=True,
                real_mode_reached=True,
                post_count=1,
                comment_count=2,
                raw_post_schema_valid=True,
                raw_comment_schema_valid=True,
            )
        ],
        raw_posts=[
            RawPost(
                platform="youtube",
                post_id="yt_fixture_video_001",
                author_id="yt_fixture_channel_001",
                author_name="Fixture YouTube Channel",
                title="Tesla public safety update fixture",
                content="Fixture public video description about quality issue response timing.",
                like_count=42,
                reply_count=2,
                share_count=0,
                created_at="2026-05-17T12:00:00Z",
                url="https://www.youtube.com/watch?v=yt_fixture_video_001",
                raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
            )
        ],
        raw_comments=[
            RawComment(
                platform="youtube",
                post_id="yt_fixture_video_001",
                comment_id="yt_fixture_comment_001",
                parent_id=None,
                author_id="yt_fixture_commenter_001",
                author_name="Fixture Viewer A",
                content="YouTube fixture quality issue comment: the problem looks serious and response is delayed.",
                like_count=9,
                reply_count=1,
                share_count=0,
                created_at="2026-05-17T12:05:00Z",
                url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_001",
                raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
            ),
            RawComment(
                platform="youtube",
                post_id="yt_fixture_video_001",
                comment_id="yt_fixture_comment_002",
                parent_id="yt_fixture_comment_001",
                author_id="yt_fixture_commenter_002",
                author_name="Fixture Viewer B",
                content="YouTube fixture support comment: a clear official explanation would help rebuild trust.",
                like_count=4,
                reply_count=0,
                share_count=0,
                created_at="2026-05-17T12:08:00Z",
                url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_002",
                raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
            ),
        ],
    )


def _youtube_crawl_response_with_promotional_comment() -> CrawlStartResponse:
    base = _youtube_crawl_response()
    comments = [
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_promo",
            parent_id=None,
            author_id="yt_fixture_commenter_promo",
            author_name="Fixture Promo Viewer",
            content="Subscribe to my channel and join my Patreon for a promo code.",
            like_count=50,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:04:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_promo",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_quality_001",
            parent_id=None,
            author_id="yt_fixture_commenter_quality_001",
            author_name="Fixture Viewer Quality 1",
            content="Tesla quality issue looks serious because the official response timeline is still unclear.",
            like_count=11,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:05:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_quality_001",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_quality_002",
            parent_id=None,
            author_id="yt_fixture_commenter_quality_002",
            author_name="Fixture Viewer Quality 2",
            content="The safety concern needs evidence and a clearer product support path.",
            like_count=8,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:06:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_quality_002",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_quality_003",
            parent_id=None,
            author_id="yt_fixture_commenter_quality_003",
            author_name="Fixture Viewer Quality 3",
            content="A delayed response makes the problem feel worse for affected owners.",
            like_count=7,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:07:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_quality_003",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_quality_004",
            parent_id=None,
            author_id="yt_fixture_commenter_quality_004",
            author_name="Fixture Viewer Quality 4",
            content="The issue should be addressed with a transparent refund or repair timeline.",
            like_count=6,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:08:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_quality_004",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
        RawComment(
            platform="youtube",
            post_id="yt_fixture_video_001",
            comment_id="yt_fixture_comment_quality_005",
            parent_id=None,
            author_id="yt_fixture_commenter_quality_005",
            author_name="Fixture Viewer Quality 5",
            content="Trust recovery depends on direct evidence and visible support operations.",
            like_count=5,
            reply_count=0,
            share_count=0,
            created_at="2026-05-17T12:09:00Z",
            url="https://www.youtube.com/watch?v=yt_fixture_video_001&lc=yt_fixture_comment_quality_005",
            raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
        ),
    ]
    metadata = base.platform_metadata[0].model_copy(update={"comment_count": len(comments)})
    return base.model_copy(update={"platform_metadata": [metadata], "raw_comments": comments})
