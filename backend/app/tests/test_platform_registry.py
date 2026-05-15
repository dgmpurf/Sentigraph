from fastapi.testclient import TestClient

from app.main import app
from app.services.crawling.platform_registry import (
    CRAWLER_LATER,
    DISABLED_OR_OPTIONAL_FUTURE,
    FUTURE_REAL_ADAPTER_CANDIDATE,
    OFFICIAL_API_PLANNED,
    get_active_mvp_platform_ids,
    get_platform_registry,
)


client = TestClient(app)

MOCK_SELECTABLE_PLATFORM_IDS = [
    "reddit",
    "weibo",
    "bilibili",
    "douyin",
    "kuaishou",
    "xiaohongshu",
    "zhihu",
    "douban",
    "toutiao",
]


def test_platform_registry_categories_and_active_mvp() -> None:
    platforms = get_platform_registry()
    by_id = {platform.platform_id: platform for platform in platforms}

    assert get_active_mvp_platform_ids() == MOCK_SELECTABLE_PLATFORM_IDS
    assert by_id["reddit"].category == FUTURE_REAL_ADAPTER_CANDIDATE
    assert by_id["reddit"].status == "api_pending"
    assert by_id["reddit"].enabled_in_mvp is True
    assert by_id["reddit"].selectable_for_mock is True
    assert by_id["reddit"].mock_available is True
    assert by_id["reddit"].api_pending is True
    assert by_id["reddit"].real_mode_disabled is True
    assert by_id["weibo"].category == OFFICIAL_API_PLANNED
    assert by_id["weibo"].enabled_in_mvp is True
    assert by_id["weibo"].selectable_for_mock is True
    assert by_id["bilibili"].category == OFFICIAL_API_PLANNED
    assert by_id["bilibili"].selectable_for_mock is True
    assert by_id["youtube"].category == DISABLED_OR_OPTIONAL_FUTURE
    assert by_id["youtube"].enabled_in_mvp is False
    assert by_id["youtube"].selectable_for_mock is False
    assert by_id["youtube"].real_mode_disabled is True
    assert by_id["hupu"].category == CRAWLER_LATER
    assert by_id["hupu"].source_type == "public_page_parser"
    assert by_id["hupu"].status == "fixture_only"
    assert by_id["hupu"].mock_available is True
    assert by_id["hupu"].selectable_for_mock is False
    assert by_id["hupu"].selectable_for_real is False
    assert "Public-page parser scaffold" in by_id["hupu"].notes
    assert by_id["tieba"].category == CRAWLER_LATER
    assert by_id["tieba"].source_type == "public_page_parser"
    assert by_id["tieba"].status == "fixture_only"
    assert by_id["tieba"].mock_available is True
    assert by_id["tieba"].selectable_for_mock is False
    assert by_id["tieba"].selectable_for_real is False
    assert "Public-page parser scaffold" in by_id["tieba"].notes
    assert by_id["nga"].category == CRAWLER_LATER
    assert by_id["nga"].source_type == "public_page_parser"
    assert by_id["nga"].status == "fixture_only"
    assert by_id["nga"].mock_available is True
    assert by_id["nga"].selectable_for_mock is False
    assert by_id["nga"].selectable_for_real is False
    assert "Public-page parser scaffold" in by_id["nga"].notes
    assert by_id["the_paper"].category == CRAWLER_LATER
    assert by_id["the_paper"].source_type == "public_page_parser"
    assert by_id["the_paper"].status == "fixture_only"
    assert by_id["the_paper"].mock_available is True
    assert by_id["the_paper"].selectable_for_real is False
    assert by_id["jiemian"].category == CRAWLER_LATER
    assert by_id["jiemian"].source_type == "public_page_parser"
    assert by_id["jiemian"].status == "fixture_only"
    assert by_id["jiemian"].mock_available is True
    assert by_id["jiemian"].selectable_for_mock is False
    assert by_id["jiemian"].selectable_for_real is False
    assert all(platform.platform_id != "youtube" for platform in platforms if platform.selectable_for_mock)


def test_platform_registry_endpoint_contract() -> None:
    response = client.get("/api/v1/platforms")

    assert response.status_code == 200
    body = response.json()
    assert body["active_mvp_platforms"] == MOCK_SELECTABLE_PLATFORM_IDS
    assert isinstance(body["platforms"], list)
    assert {platform["platform_id"] for platform in body["platforms"]} >= {
        "reddit",
        "weibo",
        "bilibili",
        "douyin",
        "kuaishou",
        "xiaohongshu",
        "zhihu",
        "douban",
        "toutiao",
        "hupu",
        "tieba",
        "tianya",
        "nga",
        "maimai",
        "the_paper",
        "jiemian",
        "youtube",
    }
    assert all("selectable_for_mock" in platform for platform in body["platforms"])
    assert all("mock_available" in platform for platform in body["platforms"])
    assert all("api_pending" in platform for platform in body["platforms"])
    assert all("real_mode_disabled" in platform for platform in body["platforms"])


def test_platform_status_endpoint_reports_safe_readiness(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "client-value-should-not-appear")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "secret-value-should-not-appear")
    monkeypatch.setenv("REDDIT_USER_AGENT", "agent-value-should-not-appear")

    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    body = response.json()
    by_id = {platform["platform_id"]: platform for platform in body["platforms"]}
    reddit = by_id["reddit"]

    assert body["active_mvp_platforms"] == MOCK_SELECTABLE_PLATFORM_IDS
    assert body["mock_selectable_platforms"] == MOCK_SELECTABLE_PLATFORM_IDS
    assert body["real_selectable_platforms"] == []
    assert body["summary"]["mock_selectable_count"] == len(MOCK_SELECTABLE_PLATFORM_IDS)
    assert body["summary"]["real_selectable_count"] == 0
    assert reddit["status"] == "api_pending"
    assert reddit["mock_available"] is True
    assert reddit["real_mode_available"] is False
    assert reddit["api_approval_required"] is True
    assert reddit["api_approval_status"] == "api_pending"
    assert reddit["credentials_required"] == [
        "REDDIT_CLIENT_ID",
        "REDDIT_CLIENT_SECRET",
        "REDDIT_USER_AGENT",
    ]
    assert reddit["credentials_present"] == {
        "REDDIT_CLIENT_ID": True,
        "REDDIT_CLIENT_SECRET": True,
        "REDDIT_USER_AGENT": True,
    }
    assert reddit["selectable_for_mock"] is True
    assert reddit["selectable_for_real"] is False
    assert reddit["real_mode_disabled"] is True
    response_text = response.text
    assert "client-value-should-not-appear" not in response_text
    assert "secret-value-should-not-appear" not in response_text
    assert "agent-value-should-not-appear" not in response_text


def test_platform_status_endpoint_reports_missing_credentials_safely(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "")
    monkeypatch.setenv("REDDIT_USER_AGENT", "")

    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    reddit = next(platform for platform in response.json()["platforms"] if platform["platform_id"] == "reddit")
    assert reddit["credentials_present"] == {
        "REDDIT_CLIENT_ID": False,
        "REDDIT_CLIENT_SECRET": False,
        "REDDIT_USER_AGENT": False,
    }
    assert reddit["real_mode_available"] is False


def test_platform_status_keeps_crawler_later_not_real_selectable() -> None:
    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    crawler_later = [
        platform
        for platform in response.json()["platforms"]
        if platform["category"] == CRAWLER_LATER
    ]
    assert crawler_later
    assert all(platform["selectable_for_real"] is False for platform in crawler_later)
    assert all(platform["real_mode_available"] is False for platform in crawler_later)
