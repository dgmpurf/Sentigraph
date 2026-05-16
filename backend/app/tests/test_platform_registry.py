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
    assert by_id["weibo"].source_type == "official_api_adapter_scaffold"
    assert by_id["weibo"].status == "official_api_planned"
    assert by_id["weibo"].enabled_in_mvp is True
    assert by_id["weibo"].selectable_for_mock is True
    assert by_id["weibo"].mock_available is True
    assert by_id["weibo"].real_mode_available is False
    assert by_id["weibo"].api_pending is True
    assert by_id["weibo"].real_mode_disabled is True
    assert by_id["weibo"].selectable_for_real is False
    assert by_id["bilibili"].category == OFFICIAL_API_PLANNED
    assert by_id["bilibili"].source_type == "official_api_adapter_scaffold"
    assert by_id["bilibili"].status == "official_api_planned"
    assert by_id["bilibili"].selectable_for_mock is True
    assert by_id["bilibili"].mock_available is True
    assert by_id["bilibili"].real_mode_available is False
    assert by_id["bilibili"].api_pending is True
    assert by_id["bilibili"].real_mode_disabled is True
    assert by_id["bilibili"].selectable_for_real is False
    assert by_id["douyin"].category == OFFICIAL_API_PLANNED
    assert by_id["douyin"].source_type == "official_api_adapter_scaffold"
    assert by_id["douyin"].status == "official_api_planned"
    assert by_id["douyin"].selectable_for_mock is True
    assert by_id["douyin"].mock_available is True
    assert by_id["douyin"].real_mode_available is False
    assert by_id["douyin"].api_pending is True
    assert by_id["douyin"].real_mode_disabled is True
    assert by_id["douyin"].selectable_for_real is False
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
    assert by_id["maimai"].category == CRAWLER_LATER
    assert by_id["maimai"].source_type == "public_page_parser"
    assert by_id["maimai"].status == "fixture_only"
    assert by_id["maimai"].mock_available is True
    assert by_id["maimai"].selectable_for_mock is False
    assert by_id["maimai"].selectable_for_real is False
    assert "Public-page parser scaffold" in by_id["maimai"].notes
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
    monkeypatch.setenv("BILIBILI_CLIENT_ID", "bilibili-client-should-not-appear")
    monkeypatch.setenv("BILIBILI_CLIENT_SECRET", "bilibili-secret-should-not-appear")
    monkeypatch.setenv("BILIBILI_ACCESS_TOKEN", "bilibili-token-should-not-appear")
    monkeypatch.setenv("WEIBO_CLIENT_ID", "weibo-client-should-not-appear")
    monkeypatch.setenv("WEIBO_CLIENT_SECRET", "weibo-secret-should-not-appear")
    monkeypatch.setenv("WEIBO_ACCESS_TOKEN", "weibo-token-should-not-appear")
    monkeypatch.setenv("DOUYIN_CLIENT_KEY", "douyin-client-key-should-not-appear")
    monkeypatch.setenv("DOUYIN_CLIENT_SECRET", "douyin-secret-should-not-appear")
    monkeypatch.setenv("DOUYIN_ACCESS_TOKEN", "douyin-token-should-not-appear")

    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    body = response.json()
    by_id = {platform["platform_id"]: platform for platform in body["platforms"]}
    reddit = by_id["reddit"]
    bilibili = by_id["bilibili"]
    weibo = by_id["weibo"]
    douyin = by_id["douyin"]

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
    assert weibo["status"] == "official_api_planned"
    assert weibo["source_type"] == "official_api_adapter_scaffold"
    assert weibo["mock_available"] is True
    assert weibo["real_mode_available"] is False
    assert weibo["api_approval_required"] is True
    assert weibo["api_approval_status"] == "planned"
    assert weibo["credentials_required"] == [
        "WEIBO_CLIENT_ID",
        "WEIBO_CLIENT_SECRET",
        "WEIBO_ACCESS_TOKEN",
    ]
    assert weibo["credentials_present"] == {
        "WEIBO_CLIENT_ID": True,
        "WEIBO_CLIENT_SECRET": True,
        "WEIBO_ACCESS_TOKEN": True,
    }
    assert weibo["selectable_for_mock"] is True
    assert weibo["selectable_for_real"] is False
    assert weibo["real_mode_disabled"] is True
    assert bilibili["status"] == "official_api_planned"
    assert bilibili["source_type"] == "official_api_adapter_scaffold"
    assert bilibili["mock_available"] is True
    assert bilibili["real_mode_available"] is False
    assert bilibili["api_approval_required"] is True
    assert bilibili["api_approval_status"] == "planned"
    assert bilibili["credentials_required"] == [
        "BILIBILI_CLIENT_ID",
        "BILIBILI_CLIENT_SECRET",
        "BILIBILI_ACCESS_TOKEN",
    ]
    assert bilibili["credentials_present"] == {
        "BILIBILI_CLIENT_ID": True,
        "BILIBILI_CLIENT_SECRET": True,
        "BILIBILI_ACCESS_TOKEN": True,
    }
    assert bilibili["selectable_for_mock"] is True
    assert bilibili["selectable_for_real"] is False
    assert bilibili["real_mode_disabled"] is True
    assert douyin["status"] == "official_api_planned"
    assert douyin["source_type"] == "official_api_adapter_scaffold"
    assert douyin["mock_available"] is True
    assert douyin["real_mode_available"] is False
    assert douyin["api_approval_required"] is True
    assert douyin["api_approval_status"] == "planned"
    assert douyin["credentials_required"] == [
        "DOUYIN_CLIENT_KEY",
        "DOUYIN_CLIENT_SECRET",
        "DOUYIN_ACCESS_TOKEN",
    ]
    assert douyin["credentials_present"] == {
        "DOUYIN_CLIENT_KEY": True,
        "DOUYIN_CLIENT_SECRET": True,
        "DOUYIN_ACCESS_TOKEN": True,
    }
    assert douyin["selectable_for_mock"] is True
    assert douyin["selectable_for_real"] is False
    assert douyin["real_mode_disabled"] is True
    response_text = response.text
    assert "client-value-should-not-appear" not in response_text
    assert "secret-value-should-not-appear" not in response_text
    assert "agent-value-should-not-appear" not in response_text
    assert "bilibili-client-should-not-appear" not in response_text
    assert "bilibili-secret-should-not-appear" not in response_text
    assert "bilibili-token-should-not-appear" not in response_text
    assert "weibo-client-should-not-appear" not in response_text
    assert "weibo-secret-should-not-appear" not in response_text
    assert "weibo-token-should-not-appear" not in response_text
    assert "douyin-client-key-should-not-appear" not in response_text
    assert "douyin-secret-should-not-appear" not in response_text
    assert "douyin-token-should-not-appear" not in response_text


def test_platform_status_endpoint_reports_missing_credentials_safely(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_CLIENT_ID", "")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "")
    monkeypatch.setenv("REDDIT_USER_AGENT", "")
    monkeypatch.setenv("BILIBILI_CLIENT_ID", "")
    monkeypatch.setenv("BILIBILI_CLIENT_SECRET", "")
    monkeypatch.setenv("BILIBILI_ACCESS_TOKEN", "")
    monkeypatch.setenv("WEIBO_CLIENT_ID", "")
    monkeypatch.setenv("WEIBO_CLIENT_SECRET", "")
    monkeypatch.setenv("WEIBO_ACCESS_TOKEN", "")
    monkeypatch.setenv("DOUYIN_CLIENT_KEY", "")
    monkeypatch.setenv("DOUYIN_CLIENT_SECRET", "")
    monkeypatch.setenv("DOUYIN_ACCESS_TOKEN", "")

    response = client.get("/api/v1/platforms/status")

    assert response.status_code == 200
    by_id = {platform["platform_id"]: platform for platform in response.json()["platforms"]}
    reddit = by_id["reddit"]
    bilibili = by_id["bilibili"]
    weibo = by_id["weibo"]
    douyin = by_id["douyin"]
    assert reddit["credentials_present"] == {
        "REDDIT_CLIENT_ID": False,
        "REDDIT_CLIENT_SECRET": False,
        "REDDIT_USER_AGENT": False,
    }
    assert reddit["real_mode_available"] is False
    assert bilibili["credentials_present"] == {
        "BILIBILI_CLIENT_ID": False,
        "BILIBILI_CLIENT_SECRET": False,
        "BILIBILI_ACCESS_TOKEN": False,
    }
    assert bilibili["real_mode_available"] is False
    assert weibo["credentials_present"] == {
        "WEIBO_CLIENT_ID": False,
        "WEIBO_CLIENT_SECRET": False,
        "WEIBO_ACCESS_TOKEN": False,
    }
    assert weibo["real_mode_available"] is False
    assert douyin["credentials_present"] == {
        "DOUYIN_CLIENT_KEY": False,
        "DOUYIN_CLIENT_SECRET": False,
        "DOUYIN_ACCESS_TOKEN": False,
    }
    assert douyin["real_mode_available"] is False


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
