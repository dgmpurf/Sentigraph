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
    assert by_id["reddit"].enabled_in_mvp is True
    assert by_id["reddit"].selectable_for_mock is True
    assert by_id["weibo"].category == OFFICIAL_API_PLANNED
    assert by_id["weibo"].enabled_in_mvp is True
    assert by_id["weibo"].selectable_for_mock is True
    assert by_id["bilibili"].category == OFFICIAL_API_PLANNED
    assert by_id["bilibili"].selectable_for_mock is True
    assert by_id["youtube"].category == DISABLED_OR_OPTIONAL_FUTURE
    assert by_id["youtube"].enabled_in_mvp is False
    assert by_id["youtube"].selectable_for_mock is False
    assert by_id["hupu"].category == CRAWLER_LATER
    assert by_id["hupu"].selectable_for_mock is False
    assert "Future crawler integration" in by_id["hupu"].notes
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
        "baidu_tieba",
        "tianya",
        "nga",
        "maimai",
        "the_paper",
        "jiemian",
        "youtube",
    }
    assert all("selectable_for_mock" in platform for platform in body["platforms"])
