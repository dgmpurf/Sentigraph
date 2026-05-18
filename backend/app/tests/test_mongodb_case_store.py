from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

import pytest

from app.repositories.case_repository import CaseRepository
from app.schemas.alert import AlertEvent, AnalysisSnapshot
from app.schemas.case import AnalysisCaseCreateRequest, MarkdownExportResponse
from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.notification import NotificationOutboxItem
from app.services.mock_pipeline import build_mock_pipeline
from app.services.mock_service import _pipeline_representative_comments
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.storage.local_json_store import LocalJsonCaseStore
from app.services.storage.mongodb_store import (
    MongoDbCaseStore,
    MongoDbStoreConfigError,
    _safe_document,
)
from app.services.storage.store_factory import create_case_store_from_env
from app.services.visualization.chart_data_builder import build_visualization_response


def test_store_factory_defaults_to_local_json(monkeypatch, tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    monkeypatch.delenv("CASE_STORE_BACKEND", raising=False)
    monkeypatch.setenv("CASE_STORE_PATH", str(store_path))

    store = create_case_store_from_env()

    assert isinstance(store, LocalJsonCaseStore)
    assert store.path == store_path


def test_store_factory_uses_explicit_local_json(monkeypatch, tmp_path) -> None:
    store_path = tmp_path / "cases.json"
    monkeypatch.setenv("CASE_STORE_BACKEND", "local_json")
    monkeypatch.setenv("CASE_STORE_PATH", str(store_path))

    store = create_case_store_from_env()

    assert isinstance(store, LocalJsonCaseStore)
    assert store.path == store_path


def test_store_factory_rejects_unknown_backend(monkeypatch) -> None:
    monkeypatch.setenv("CASE_STORE_BACKEND", "mystery_store")

    with pytest.raises(ValueError, match="Unsupported CASE_STORE_BACKEND='mystery_store'"):
        create_case_store_from_env()


def test_store_factory_uses_mongodb_when_configured(monkeypatch) -> None:
    fake_client = FakeMongoClient()
    monkeypatch.setenv("CASE_STORE_BACKEND", "mongodb")
    monkeypatch.setenv("MONGODB_URI", "mongodb://example.local:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "sentigraph_test")

    store = create_case_store_from_env(mongo_client_factory=lambda uri, **_: fake_client)

    assert isinstance(store, MongoDbCaseStore)
    assert store.uri == "mongodb://example.local:27017"
    assert fake_client.pinged is True
    assert fake_client.requested_database_names == ["sentigraph_test"]


def test_store_factory_rejects_blank_mongodb_uri(monkeypatch) -> None:
    monkeypatch.setenv("CASE_STORE_BACKEND", "mongodb")
    monkeypatch.setenv("MONGODB_URI", "")

    with pytest.raises(MongoDbStoreConfigError, match="MONGODB_URI is required"):
        create_case_store_from_env()


def test_store_factory_reports_mongodb_connection_failure(monkeypatch) -> None:
    monkeypatch.setenv("CASE_STORE_BACKEND", "mongodb")
    monkeypatch.setenv("MONGODB_URI", "mongodb://example.local:27017")

    with pytest.raises(MongoDbStoreConfigError, match="Unable to connect to MongoDB"):
        create_case_store_from_env(mongo_client_factory=lambda uri, **_: FailingMongoClient())


def test_mongodb_store_creates_expected_indexes() -> None:
    fake_database = FakeMongoDatabase()

    MongoDbCaseStore(database=fake_database)

    assert ("case_id",) in _index_args(fake_database["analysis_cases"])
    assert ("created_at",) in _index_args(fake_database["analysis_cases"])
    assert ("updated_at",) in _index_args(fake_database["analysis_cases"])
    assert ("case_id",) in _index_args(fake_database["markdown_reports"])
    assert ("snapshot_id",) in _index_args(fake_database["analysis_snapshots"])
    assert ("case_id",) in _index_args(fake_database["analysis_snapshots"])
    assert ("alert_id",) in _index_args(fake_database["alert_events"])
    assert ("case_id",) in _index_args(fake_database["alert_events"])
    assert ("notification_id",) in _index_args(fake_database["notification_outbox"])
    assert ("case_id",) in _index_args(fake_database["notification_outbox"])
    assert ("status",) in _index_args(fake_database["notification_outbox"])


def test_mongodb_store_case_report_markdown_snapshot_alert_and_notification() -> None:
    fake_database = FakeMongoDatabase()
    repository = CaseRepository(MongoDbCaseStore(database=fake_database))
    case = repository.create_case(
        AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit", "weibo"], title="Tesla Mongo Demo")
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
            filename="tesla_mongo_demo.md",
            markdown="# Tesla Mongo Demo\n\nMock Markdown report.",
            generated_at=datetime(2026, 5, 14, 10, 0, tzinfo=timezone.utc),
        ),
    )
    snapshot = AnalysisSnapshot(
        snapshot_id=f"{case.case_id}_snapshot_001",
        case_id=case.case_id,
        created_at=datetime(2026, 5, 14, 10, 5, tzinfo=timezone.utc),
        run_index=1,
        risk_score=42.0,
        overall_risk=42.0,
        risk_level="medium",
        risk_model_version="v1_5_topic_risk_mvp",
        real_crisis_risk=38.0,
        manipulation_risk=12.0,
        summary="Mock snapshot",
    )
    alert = AlertEvent(
        alert_id="alert_case_001_snapshot_001_001",
        case_id=case.case_id,
        snapshot_id=snapshot.snapshot_id,
        level="warning",
        alert_type="risk_score_increase",
        message="Risk increased.",
        reason="Mock alert reason.",
        created_at=datetime(2026, 5, 14, 10, 6, tzinfo=timezone.utc),
        metadata={"risk.score.delta": 12.0, "$driver": "mock"},
    )
    notification = NotificationOutboxItem(
        notification_id="notification_alert_case_001_snapshot_001_001_in_app",
        alert_id=alert.alert_id,
        case_id=case.case_id,
        level="warning",
        title="Mock warning",
        message="舆情风险出现上升，请关注该案例。",
        channel_type="in_app",
        status="pending",
        created_at=datetime(2026, 5, 14, 10, 7, tzinfo=timezone.utc),
    )

    repository.save_analysis_snapshot(case.case_id, snapshot)
    repository.save_alert_events(case.case_id, [alert])
    repository.save_notification(notification)
    reloaded_repository = CaseRepository(MongoDbCaseStore(database=fake_database))

    detail = reloaded_repository.get_case(case.case_id)
    markdown = reloaded_repository.get_markdown_report(case.case_id)
    snapshots = reloaded_repository.list_analysis_snapshots(case.case_id)
    alerts = reloaded_repository.list_case_alerts(case.case_id)
    notifications = reloaded_repository.list_case_notifications(case.case_id)

    assert detail is not None
    assert detail.analysis_result is not None
    assert detail.visualization_data is not None
    assert detail.report is not None
    assert detail.risk_model_version == "v1_5_topic_risk_mvp"
    assert markdown is not None
    assert "Mock Markdown report." in markdown.markdown
    assert snapshots == [snapshot]
    assert alerts[0].metadata == {"risk_score_delta": 12.0, "_driver": "mock"}
    assert notifications == [notification]


def test_mongodb_store_persists_attached_raw_crawl_data() -> None:
    fake_database = FakeMongoDatabase()
    repository = CaseRepository(MongoDbCaseStore(database=fake_database))
    case = repository.create_case(
        AnalysisCaseCreateRequest(keyword="Tesla", platforms=["youtube"], title="Tesla Mongo Raw Demo")
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
    reloaded_repository = CaseRepository(MongoDbCaseStore(database=fake_database))
    detail = reloaded_repository.get_case(case.case_id)

    assert attached is not None
    assert detail is not None
    assert detail.raw_data_status == "attached"
    assert detail.raw_post_count == 1
    assert detail.raw_comment_count == 1
    assert detail.raw_posts[0].post_id == "yt_mongo_video_001"
    assert detail.raw_comments[0].content == "YouTube fixture QA comment survives MongoDB reload."
    assert detail.crawl_metadata[0].credential_present is True
    assert "YOUTUBE_API_KEY" not in detail.model_dump_json()


def test_mongodb_store_reset_clears_all_collections() -> None:
    fake_database = FakeMongoDatabase()
    store = MongoDbCaseStore(database=fake_database)
    repository = CaseRepository(store)
    repository.create_case(AnalysisCaseCreateRequest(keyword="Tesla", platforms=["reddit"]))

    assert repository.list_cases()

    repository.reset()

    assert repository.list_cases() == []


def test_mongodb_safe_document_converts_nested_keys_to_strings() -> None:
    assert _safe_document({1: {"$bad.key": "value", "a.b": [{"$inner": 1}]}}) == {
        "1": {"_bad_key": "value", "a_b": [{"_inner": 1}]}
    }


class FakeAdmin:
    def __init__(self, client: "FakeMongoClient") -> None:
        self.client = client

    def command(self, command_name: str) -> dict[str, int]:
        assert command_name == "ping"
        self.client.pinged = True
        return {"ok": 1}


class FakeMongoClient:
    def __init__(self) -> None:
        self.admin = FakeAdmin(self)
        self.pinged = False
        self.databases: dict[str, FakeMongoDatabase] = {}
        self.requested_database_names: list[str] = []

    def __getitem__(self, database_name: str) -> "FakeMongoDatabase":
        self.requested_database_names.append(database_name)
        self.databases.setdefault(database_name, FakeMongoDatabase())
        return self.databases[database_name]


class FailingAdmin:
    def command(self, command_name: str) -> dict[str, int]:
        assert command_name == "ping"
        raise RuntimeError("connection unavailable")


class FailingMongoClient:
    def __init__(self) -> None:
        self.admin = FailingAdmin()


class FakeMongoDatabase:
    def __init__(self) -> None:
        self.collections: dict[str, FakeMongoCollection] = {}

    def __getitem__(self, collection_name: str) -> "FakeMongoCollection":
        self.collections.setdefault(collection_name, FakeMongoCollection())
        return self.collections[collection_name]


class FakeMongoCollection:
    def __init__(self) -> None:
        self.documents: list[dict[str, Any]] = []
        self.indexes: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def create_index(self, *args: Any, **kwargs: Any) -> None:
        self.indexes.append((args, kwargs))

    def replace_one(self, filter_query: dict[str, Any], document: dict[str, Any], *, upsert: bool = False) -> None:
        for index, existing in enumerate(self.documents):
            if _matches(existing, filter_query):
                replacement = deepcopy(document)
                replacement.setdefault("_id", existing.get("_id", f"fake_id_{index}"))
                self.documents[index] = replacement
                return
        if upsert:
            replacement = deepcopy(document)
            replacement.setdefault("_id", f"fake_id_{len(self.documents)}")
            self.documents.append(replacement)

    def find_one(self, filter_query: dict[str, Any]) -> dict[str, Any] | None:
        for document in self.documents:
            if _matches(document, filter_query):
                return deepcopy(document)
        return None

    def find(self, filter_query: dict[str, Any]) -> list[dict[str, Any]]:
        return [deepcopy(document) for document in self.documents if _matches(document, filter_query)]

    def delete_many(self, filter_query: dict[str, Any]) -> None:
        self.documents = [document for document in self.documents if not _matches(document, filter_query)]


def _matches(document: dict[str, Any], filter_query: dict[str, Any]) -> bool:
    return all(document.get(key) == value for key, value in filter_query.items())


def _index_args(collection: FakeMongoCollection) -> set[tuple[Any, ...]]:
    return {args for args, _kwargs in collection.indexes}


def _raw_post() -> RawPost:
    return RawPost(
        platform="youtube",
        post_id="yt_mongo_video_001",
        author_id="yt_mongo_channel",
        author_name="Fixture Channel",
        title="Mongo-safe YouTube fixture",
        content="Safe public fixture description.",
        like_count=12,
        reply_count=1,
        share_count=0,
        created_at="2026-05-17T12:00:00Z",
        url="https://www.youtube.com/watch?v=yt_mongo_video_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
    )


def _raw_comment() -> RawComment:
    return RawComment(
        platform="youtube",
        post_id="yt_mongo_video_001",
        comment_id="yt_mongo_comment_001",
        parent_id=None,
        author_id="yt_mongo_commenter",
        author_name="Fixture Viewer",
        content="YouTube fixture QA comment survives MongoDB reload.",
        like_count=3,
        reply_count=0,
        share_count=0,
        created_at="2026-05-17T12:05:00Z",
        url="https://www.youtube.com/watch?v=yt_mongo_video_001&lc=yt_mongo_comment_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
    )
