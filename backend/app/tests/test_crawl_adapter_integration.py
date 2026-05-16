from __future__ import annotations

import json

from fastapi.testclient import TestClient

from app.main import app
from app.schemas.comment import RawComment, RawPost
from app.services.crawling import crawl_service
from app.services.crawling import reddit_adapter as reddit_adapter_module
from app.services.crawling.public_parser.public_fetcher import PublicFetcher, PublicFetchResult
from app.services.crawling.reddit_adapter import RedditAdapter, RedditCredentials, RedditDependencyError


client = TestClient(app)


class SpyRedditAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="reddit",
                post_id="reddit_spy_post_001",
                author_id="reddit_author_001",
                author_name="reddit_author",
                title=f"{keyword} adapter spy post",
                content="Mock Reddit adapter post.",
                like_count=12,
                reply_count=2,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.reddit.com/r/test/comments/reddit_spy_post_001/",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="reddit",
                post_id=post_id,
                comment_id="reddit_spy_comment_001",
                parent_id=None,
                author_id="reddit_commenter_001",
                author_name="reddit_commenter",
                content="Mock Reddit adapter comment.",
                like_count=3,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.reddit.com/r/test/comments/reddit_spy_post_001/comment/",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyBilibiliAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="bilibili",
                post_id="BV1spy001",
                author_id="bilibili_up_001",
                author_name="bilibili_uploader",
                title=f"{keyword} Bilibili adapter spy video",
                content="Mock Bilibili adapter video.",
                like_count=88,
                reply_count=2,
                share_count=4,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.bilibili.com/video/BV1spy001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="bilibili",
                post_id=post_id,
                comment_id="bilibili_spy_comment_001",
                parent_id=None,
                author_id="bilibili_commenter_001",
                author_name="bilibili_commenter",
                content="Mock Bilibili adapter comment.",
                like_count=7,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.bilibili.com/video/BV1spy001#reply001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyDoubanAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="douban",
                post_id="douban_spy_topic_001",
                author_id="douban_author_001",
                author_name="douban_author",
                title=f"{keyword} Douban adapter spy topic",
                content="Mock Douban adapter group discussion.",
                like_count=82,
                reply_count=8,
                share_count=3,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.douban.com/group/topic/douban_spy_topic_001/",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="douban",
                post_id=post_id,
                comment_id="douban_spy_comment_001",
                parent_id=None,
                author_id="douban_commenter_001",
                author_name="douban_commenter",
                content="Mock Douban adapter comment.",
                like_count=9,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.douban.com/group/topic/douban_spy_topic_001/#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyDouyinAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="douyin",
                post_id="douyin_spy_video_001",
                author_id="douyin_creator_001",
                author_name="douyin_creator",
                title=f"{keyword} Douyin adapter spy video",
                content="Mock Douyin adapter short video.",
                like_count=188,
                reply_count=12,
                share_count=9,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.douyin.com/video/douyin_spy_video_001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="douyin",
                post_id=post_id,
                comment_id="douyin_spy_comment_001",
                parent_id=None,
                author_id="douyin_commenter_001",
                author_name="douyin_commenter",
                content="Mock Douyin adapter comment.",
                like_count=17,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.douyin.com/video/douyin_spy_video_001#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyKuaishouAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="kuaishou",
                post_id="kuaishou_spy_video_001",
                author_id="kuaishou_creator_001",
                author_name="kuaishou_creator",
                title=f"{keyword} Kuaishou adapter spy video",
                content="Mock Kuaishou adapter short video.",
                like_count=168,
                reply_count=11,
                share_count=7,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.kuaishou.com/short-video/kuaishou_spy_video_001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="kuaishou",
                post_id=post_id,
                comment_id="kuaishou_spy_comment_001",
                parent_id=None,
                author_id="kuaishou_commenter_001",
                author_name="kuaishou_commenter",
                content="Mock Kuaishou adapter comment.",
                like_count=15,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.kuaishou.com/short-video/kuaishou_spy_video_001#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyXiaohongshuAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="xiaohongshu",
                post_id="xiaohongshu_spy_note_001",
                author_id="xiaohongshu_creator_001",
                author_name="xiaohongshu_creator",
                title=f"{keyword} Xiaohongshu adapter spy note",
                content="Mock Xiaohongshu adapter lifestyle/community note.",
                like_count=142,
                reply_count=9,
                share_count=5,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.xiaohongshu.com/explore/xiaohongshu_spy_note_001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="xiaohongshu",
                post_id=post_id,
                comment_id="xiaohongshu_spy_comment_001",
                parent_id=None,
                author_id="xiaohongshu_commenter_001",
                author_name="xiaohongshu_commenter",
                content="Mock Xiaohongshu adapter comment.",
                like_count=13,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.xiaohongshu.com/explore/xiaohongshu_spy_note_001#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyZhihuAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="zhihu",
                post_id="zhihu_spy_answer_001",
                author_id="zhihu_author_001",
                author_name="zhihu_author",
                title=f"{keyword} Zhihu adapter spy answer",
                content="Mock Zhihu adapter Q&A answer.",
                like_count=132,
                reply_count=8,
                share_count=4,
                created_at="2026-05-15T00:00:00Z",
                url="https://www.zhihu.com/question/zhihu_spy_question_001/answer/zhihu_spy_answer_001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="zhihu",
                post_id=post_id,
                comment_id="zhihu_spy_comment_001",
                parent_id=None,
                author_id="zhihu_commenter_001",
                author_name="zhihu_commenter",
                content="Mock Zhihu adapter comment.",
                like_count=12,
                created_at="2026-05-15T00:01:00Z",
                url="https://www.zhihu.com/question/zhihu_spy_question_001#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class SpyWeiboAdapter:
    def __init__(self) -> None:
        self.fallback_reason: str | None = None

    def get_mode(self) -> str:
        return "mock"

    def get_status_metadata(self) -> dict[str, object]:
        return {
            "source_type": "official_api_adapter_scaffold",
            "fetch_status": "mock",
            "mock_available": True,
            "real_mode_available": False,
            "api_approval_required": True,
            "api_approval_status": "planned",
            "api_pending": True,
            "real_mode_disabled": True,
            "selectable_for_real": False,
        }

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str = "new",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        return [
            RawPost(
                platform="weibo",
                post_id="weibo_spy_status_001",
                author_id="weibo_author_001",
                author_name="weibo_author",
                title=f"{keyword} Weibo adapter spy status",
                content="Mock Weibo adapter status.",
                like_count=188,
                reply_count=12,
                share_count=9,
                created_at="2026-05-15T00:00:00Z",
                url="https://weibo.com/weibo_spy_status_001",
                raw_data={"mode": "mock", "sort": sort, "date_range": date_range},
            )
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[RawComment]:
        return [
            RawComment(
                platform="weibo",
                post_id=post_id,
                comment_id="weibo_spy_comment_001",
                parent_id=None,
                author_id="weibo_commenter_001",
                author_name="weibo_commenter",
                content="Mock Weibo adapter comment.",
                like_count=17,
                created_at="2026-05-15T00:01:00Z",
                url="https://weibo.com/weibo_spy_status_001#comment001",
                raw_data={"mode": "mock"},
            )
        ][:limit]


class AuthFailingRedditClient:
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[dict[str, object]]:
        raise PermissionError("simulated auth failure")

    def fetch_comments(self, post_id: str, *, limit: int) -> list[dict[str, object]]:
        return []


class ParsingFailingRedditClient:
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[dict[str, object]]:
        raise json.JSONDecodeError("simulated parse failure", "", 0)

    def fetch_comments(self, post_id: str, *, limit: int) -> list[dict[str, object]]:
        return []


class RealLikeRedditClient:
    def __init__(self, credentials: RedditCredentials) -> None:
        self.credentials = credentials

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[dict[str, object]]:
        return [
            {
                "kind": "t3",
                "data": {
                    "id": "real001",
                    "name": "t3_real001",
                    "author": "public_redditor",
                    "author_fullname": "t2_public",
                    "title": f"{keyword} real-mode fixture post",
                    "selftext": "Public Reddit fixture content.",
                    "ups": 21,
                    "num_comments": 1,
                    "created_utc": 1778754000,
                    "permalink": "/r/test/comments/real001/fixture/",
                },
            }
        ][:limit]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[dict[str, object]]:
        return [
            {
                "kind": "t1",
                "data": {
                    "id": "real_comment_001",
                    "name": "t1_real_comment_001",
                    "link_id": post_id,
                    "parent_id": post_id,
                    "author": "public_commenter",
                    "author_fullname": "t2_commenter",
                    "body": "Public Reddit fixture comment.",
                    "ups": 5,
                    "created_utc": 1778754300,
                    "permalink": "/r/test/comments/real001/real_comment_001/",
                },
            }
        ][:limit]


def test_crawl_start_with_reddit_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyRedditAdapter:
        calls.append(platform_id)
        return SpyRedditAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["reddit"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "reddit"
    assert body["raw_comments"][0]["platform"] == "reddit"
    assert metadata["platform"] == "reddit"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is False
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_reddit_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "mock")
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["real_mode_reached"] is False
    assert metadata["dependency_available"] is True
    assert metadata["exception_class"] is None
    assert metadata["sanitized_error_category"] is None
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "reddit" for post in body["raw_posts"])
    assert all(comment["platform"] == "reddit" for comment in body["raw_comments"])


def test_crawl_start_with_bilibili_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyBilibiliAdapter:
        calls.append(platform_id)
        return SpyBilibiliAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["bilibili"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["bilibili"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "bilibili"
    assert body["raw_comments"][0]["platform"] == "bilibili"
    assert metadata["platform"] == "bilibili"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_bilibili_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "mock")
    monkeypatch.delenv("BILIBILI_CLIENT_ID", raising=False)
    monkeypatch.delenv("BILIBILI_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("BILIBILI_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["bilibili"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "bilibili"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "bilibili" for post in body["raw_posts"])
    assert all(comment["platform"] == "bilibili" for comment in body["raw_comments"])


def test_crawl_start_bilibili_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "real")
    monkeypatch.setenv("BILIBILI_CLIENT_ID", "client")
    monkeypatch.setenv("BILIBILI_CLIENT_SECRET", "secret")
    monkeypatch.setenv("BILIBILI_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["bilibili"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "bilibili"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_bilibili_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("BILIBILI_ADAPTER_MODE", "real")
    monkeypatch.delenv("BILIBILI_CLIENT_ID", raising=False)
    monkeypatch.delenv("BILIBILI_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("BILIBILI_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["bilibili"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "bilibili"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_douban_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyDoubanAdapter:
        calls.append(platform_id)
        return SpyDoubanAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douban"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["douban"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "douban"
    assert body["raw_comments"][0]["platform"] == "douban"
    assert metadata["platform"] == "douban"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_douban_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "mock")
    monkeypatch.delenv("DOUBAN_CLIENT_ID", raising=False)
    monkeypatch.delenv("DOUBAN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUBAN_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douban"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douban"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "douban" for post in body["raw_posts"])
    assert all(comment["platform"] == "douban" for comment in body["raw_comments"])


def test_crawl_start_douban_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "real")
    monkeypatch.setenv("DOUBAN_CLIENT_ID", "client")
    monkeypatch.setenv("DOUBAN_CLIENT_SECRET", "secret")
    monkeypatch.setenv("DOUBAN_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douban"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douban"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_douban_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("DOUBAN_ADAPTER_MODE", "real")
    monkeypatch.delenv("DOUBAN_CLIENT_ID", raising=False)
    monkeypatch.delenv("DOUBAN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUBAN_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douban"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douban"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_douyin_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyDouyinAdapter:
        calls.append(platform_id)
        return SpyDouyinAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douyin"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["douyin"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "douyin"
    assert body["raw_comments"][0]["platform"] == "douyin"
    assert metadata["platform"] == "douyin"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_douyin_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "mock")
    monkeypatch.delenv("DOUYIN_CLIENT_KEY", raising=False)
    monkeypatch.delenv("DOUYIN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUYIN_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douyin"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douyin"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "douyin" for post in body["raw_posts"])
    assert all(comment["platform"] == "douyin" for comment in body["raw_comments"])


def test_crawl_start_douyin_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "real")
    monkeypatch.setenv("DOUYIN_CLIENT_KEY", "client")
    monkeypatch.setenv("DOUYIN_CLIENT_SECRET", "secret")
    monkeypatch.setenv("DOUYIN_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douyin"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douyin"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_douyin_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("DOUYIN_ADAPTER_MODE", "real")
    monkeypatch.delenv("DOUYIN_CLIENT_KEY", raising=False)
    monkeypatch.delenv("DOUYIN_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("DOUYIN_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["douyin"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "douyin"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_kuaishou_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyKuaishouAdapter:
        calls.append(platform_id)
        return SpyKuaishouAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["kuaishou"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["kuaishou"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "kuaishou"
    assert body["raw_comments"][0]["platform"] == "kuaishou"
    assert metadata["platform"] == "kuaishou"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_kuaishou_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("KUAISHOU_ADAPTER_MODE", "mock")
    monkeypatch.delenv("KUAISHOU_CLIENT_ID", raising=False)
    monkeypatch.delenv("KUAISHOU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("KUAISHOU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["kuaishou"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "kuaishou"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "kuaishou" for post in body["raw_posts"])
    assert all(comment["platform"] == "kuaishou" for comment in body["raw_comments"])


def test_crawl_start_kuaishou_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("KUAISHOU_ADAPTER_MODE", "real")
    monkeypatch.setenv("KUAISHOU_CLIENT_ID", "client")
    monkeypatch.setenv("KUAISHOU_CLIENT_SECRET", "secret")
    monkeypatch.setenv("KUAISHOU_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["kuaishou"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "kuaishou"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_kuaishou_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("KUAISHOU_ADAPTER_MODE", "real")
    monkeypatch.delenv("KUAISHOU_CLIENT_ID", raising=False)
    monkeypatch.delenv("KUAISHOU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("KUAISHOU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["kuaishou"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "kuaishou"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_xiaohongshu_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyXiaohongshuAdapter:
        calls.append(platform_id)
        return SpyXiaohongshuAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["xiaohongshu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["xiaohongshu"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "xiaohongshu"
    assert body["raw_comments"][0]["platform"] == "xiaohongshu"
    assert metadata["platform"] == "xiaohongshu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_xiaohongshu_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("XIAOHONGSHU_ADAPTER_MODE", "mock")
    monkeypatch.delenv("XIAOHONGSHU_CLIENT_ID", raising=False)
    monkeypatch.delenv("XIAOHONGSHU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("XIAOHONGSHU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["xiaohongshu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "xiaohongshu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "xiaohongshu" for post in body["raw_posts"])
    assert all(comment["platform"] == "xiaohongshu" for comment in body["raw_comments"])


def test_crawl_start_xiaohongshu_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("XIAOHONGSHU_ADAPTER_MODE", "real")
    monkeypatch.setenv("XIAOHONGSHU_CLIENT_ID", "client")
    monkeypatch.setenv("XIAOHONGSHU_CLIENT_SECRET", "secret")
    monkeypatch.setenv("XIAOHONGSHU_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["xiaohongshu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "xiaohongshu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_xiaohongshu_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("XIAOHONGSHU_ADAPTER_MODE", "real")
    monkeypatch.delenv("XIAOHONGSHU_CLIENT_ID", raising=False)
    monkeypatch.delenv("XIAOHONGSHU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("XIAOHONGSHU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["xiaohongshu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "xiaohongshu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_zhihu_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyZhihuAdapter:
        calls.append(platform_id)
        return SpyZhihuAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["zhihu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["zhihu"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "zhihu"
    assert body["raw_comments"][0]["platform"] == "zhihu"
    assert metadata["platform"] == "zhihu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_zhihu_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("ZHIHU_ADAPTER_MODE", "mock")
    monkeypatch.delenv("ZHIHU_CLIENT_ID", raising=False)
    monkeypatch.delenv("ZHIHU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("ZHIHU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["zhihu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "zhihu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "zhihu" for post in body["raw_posts"])
    assert all(comment["platform"] == "zhihu" for comment in body["raw_comments"])


def test_crawl_start_zhihu_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("ZHIHU_ADAPTER_MODE", "real")
    monkeypatch.setenv("ZHIHU_CLIENT_ID", "client")
    monkeypatch.setenv("ZHIHU_CLIENT_SECRET", "secret")
    monkeypatch.setenv("ZHIHU_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["zhihu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "zhihu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_zhihu_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("ZHIHU_ADAPTER_MODE", "real")
    monkeypatch.delenv("ZHIHU_CLIENT_ID", raising=False)
    monkeypatch.delenv("ZHIHU_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("ZHIHU_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["zhihu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "zhihu"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_with_weibo_uses_adapter_factory(monkeypatch) -> None:
    calls: list[str] = []

    def fake_get_adapter(platform_id: str) -> SpyWeiboAdapter:
        calls.append(platform_id)
        return SpyWeiboAdapter()

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["weibo"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert calls == ["weibo"]
    assert body["status"] == "queued"
    assert body["raw_posts"][0]["platform"] == "weibo"
    assert body["raw_comments"][0]["platform"] == "weibo"
    assert metadata["platform"] == "weibo"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["mock_available"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 1


def test_crawl_start_weibo_mock_mode_returns_normalized_mock_data(monkeypatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "mock")
    monkeypatch.delenv("WEIBO_CLIENT_ID", raising=False)
    monkeypatch.delenv("WEIBO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("WEIBO_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["weibo"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "weibo"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["source_type"] == "official_api_adapter_scaffold"
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "mock_only"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert body["raw_comments"]
    assert all(post["platform"] == "weibo" for post in body["raw_posts"])
    assert all(comment["platform"] == "weibo" for comment in body["raw_comments"])


def test_crawl_start_weibo_real_mode_stays_api_pending_without_network(monkeypatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "real")
    monkeypatch.setenv("WEIBO_CLIENT_ID", "client")
    monkeypatch.setenv("WEIBO_CLIENT_SECRET", "secret")
    monkeypatch.setenv("WEIBO_ACCESS_TOKEN", "token")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["weibo"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "weibo"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["fetch_status"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_available"] is False
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_weibo_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("WEIBO_ADAPTER_MODE", "real")
    monkeypatch.delenv("WEIBO_CLIENT_ID", raising=False)
    monkeypatch.delenv("WEIBO_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("WEIBO_ACCESS_TOKEN", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["weibo"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "weibo"
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_reddit_real_request_stays_mock_until_api_approval(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")

    def fake_get_adapter(platform_id: str) -> RedditAdapter:
        assert platform_id == "reddit"
        return RedditAdapter(
            mode="real",
            credentials=RedditCredentials(
                client_id="client",
                client_secret="secret",
                user_agent="sentigraph-test",
            ),
            http_client=AuthFailingRedditClient(),
        )

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["dependency_available"] is True
    assert metadata["exception_class"] is None
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_reddit_real_without_credentials_falls_back_to_mock(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    monkeypatch.delenv("REDDIT_USER_AGENT", raising=False)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "config_error"
    assert metadata["real_mode_blocked_reason"] == "credentials_missing"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert body["raw_posts"]
    assert body["raw_comments"]


def test_crawl_start_reddit_api_pending_prevents_dependency_initialization(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")
    monkeypatch.setenv("REDDIT_CLIENT_ID", "client")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "secret")
    monkeypatch.setenv("REDDIT_USER_AGENT", "sentigraph-test")

    def missing_praw(credentials: RedditCredentials) -> object:
        del credentials
        raise AssertionError("Reddit API client should not initialize while API approval is pending")

    monkeypatch.setattr(reddit_adapter_module, "_build_praw_reddit", missing_praw)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]


def test_crawl_start_reddit_parsing_client_is_not_used_until_api_approval(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")

    def fake_get_adapter(platform_id: str) -> RedditAdapter:
        assert platform_id == "reddit"
        return RedditAdapter(
            mode="real",
            credentials=RedditCredentials(
                client_id="client",
                client_secret="secret",
                user_agent="sentigraph-test",
            ),
            http_client=ParsingFailingRedditClient(),
        )

    monkeypatch.setattr(crawl_service.adapter_factory, "get_adapter", fake_get_adapter)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["exception_class"] is None
    assert metadata["sanitized_error_category"] == "api_pending"
    assert body["raw_posts"]


def test_crawl_start_reddit_real_with_credentials_returns_mock_until_api_approval(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "real")
    monkeypatch.setenv("REDDIT_CLIENT_ID", "client")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "secret")
    monkeypatch.setenv("REDDIT_USER_AGENT", "sentigraph-test")
    monkeypatch.setattr(reddit_adapter_module, "_OfficialRedditClient", RealLikeRedditClient)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["adapter_mode"] == "mock"
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "api_pending"
    assert metadata["api_pending"] is True
    assert metadata["real_mode_disabled"] is True
    assert metadata["real_mode_blocked_reason"] == "api_pending"
    assert metadata["real_mode_reached"] is False
    assert metadata["dependency_available"] is True
    assert metadata["exception_class"] is None
    assert metadata["sanitized_error_category"] == "api_pending"
    assert metadata["post_count"] <= 3
    assert metadata["comment_count"] <= 3
    assert body["raw_posts"][0]["post_id"] != "t3_real001"
    assert body["raw_posts"][0]["raw_data"]["mode"] == "mock"


def test_crawl_start_non_adapter_official_platform_keeps_old_mock_first_behavior() -> None:
    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["toutiao"], "limit": 100},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["project_id"] == "project_001"
    assert body["crawl_task_id"] == "crawl_task_001"
    assert body["status"] == "queued"
    assert body["platform_metadata"] == []
    assert body["raw_posts"] == []
    assert body["raw_comments"] == []


def test_crawl_start_the_paper_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["the_paper"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "the_paper"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert all(post["platform"] == "the_paper" for post in body["raw_posts"])
    assert body["raw_comments"] == []


def test_crawl_start_the_paper_live_enabled_uses_mocked_public_fetch(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")
    html = """
    <article>
      <h1 class="article-title">The Paper live pilot fixture</h1>
      <div class="article-author">The Paper public source</div>
      <time class="article-date">2026-05-15T10:00:00Z</time>
      <section class="article-content">Public article body from a mocked live fetch.</section>
    </article>
    """

    def fake_fetch(self: PublicFetcher, url: str, profile) -> PublicFetchResult:
        del self, profile
        return PublicFetchResult(
            ok=True,
            url=url,
            html=html,
            status_code=200,
            live_fetch_enabled=True,
            live_fetch_attempted=True,
            live_fetch_allowed=True,
            fetch_status="ok",
        )

    monkeypatch.setattr(PublicFetcher, "fetch", fake_fetch)

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "fixture", "platforms": ["the_paper"], "limit": 3},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "the_paper"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is True
    assert metadata["live_fetch_attempted"] is True
    assert metadata["live_fetch_allowed"] is True
    assert metadata["fallback_used"] is False
    assert metadata["fallback_reason_category"] is None
    assert metadata["fetch_status"] == "ok"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 0
    assert metadata["schema_valid"] is True
    assert body["raw_posts"][0]["platform"] == "the_paper"
    assert body["raw_posts"][0]["title"] == "The Paper live pilot fixture"
    assert body["raw_posts"][0]["raw_data"]["mode"] == "public_parser_live"
    assert body["raw_comments"] == []


def test_crawl_start_jiemian_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["jiemian"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "jiemian"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert body["raw_posts"]
    assert all(post["platform"] == "jiemian" for post in body["raw_posts"])
    assert body["raw_comments"] == []


def test_crawl_start_hupu_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["hupu"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "hupu"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 2
    assert body["raw_posts"][0]["platform"] == "hupu"
    assert body["raw_posts"][0]["title"] == "Tesla service discussion on Hupu"
    assert len(body["raw_comments"]) == 2
    assert all(comment["platform"] == "hupu" for comment in body["raw_comments"])


def test_crawl_start_maimai_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["maimai"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "maimai"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 2
    assert body["raw_posts"][0]["platform"] == "maimai"
    assert body["raw_posts"][0]["title"] == "Tesla workplace discussion on Maimai"
    assert len(body["raw_comments"]) == 2
    assert all(comment["platform"] == "maimai" for comment in body["raw_comments"])


def test_crawl_start_maimai_stays_fixture_only_when_global_live_fetch_enabled(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["maimai"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "maimai"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 2
    assert body["raw_posts"][0]["platform"] == "maimai"


def test_crawl_start_tieba_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["tieba"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "tieba"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 3
    assert body["raw_posts"][0]["platform"] == "tieba"
    assert body["raw_posts"][0]["title"] == "Tesla service discussion on Baidu Tieba"
    assert len(body["raw_comments"]) == 3
    assert all(comment["platform"] == "tieba" for comment in body["raw_comments"])
    assert body["raw_comments"][0]["raw_data"]["floor_number"] == "1F"


def test_crawl_start_tieba_stays_fixture_only_when_global_live_fetch_enabled(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["tieba"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "tieba"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 3
    assert body["raw_posts"][0]["platform"] == "tieba"
    assert body["raw_comments"][0]["raw_data"]["floor_number"] == "1F"


def test_crawl_start_nga_uses_public_parser_fixture_fallback(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["nga"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "nga"
    assert metadata["source_type"] == "public_page_parser"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["real_mode_blocked_reason"] == "live_fetch_disabled"
    assert metadata["schema_valid"] is True
    assert metadata["raw_post_schema_valid"] is True
    assert metadata["raw_comment_schema_valid"] is True
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 3
    assert body["raw_posts"][0]["platform"] == "nga"
    assert body["raw_posts"][0]["title"] == "Tesla service discussion on NGA"
    assert len(body["raw_comments"]) == 3
    assert all(comment["platform"] == "nga" for comment in body["raw_comments"])
    assert body["raw_comments"][0]["raw_data"]["floor_number"] == "1F"


def test_crawl_start_nga_stays_fixture_only_when_global_live_fetch_enabled(monkeypatch) -> None:
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "true")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["nga"], "limit": 100},
    )

    body = response.json()
    metadata = body["platform_metadata"][0]

    assert response.status_code == 200
    assert metadata["platform"] == "nga"
    assert metadata["parser_status"] == "fixture_only"
    assert metadata["live_fetch_enabled"] is False
    assert metadata["live_fetch_attempted"] is False
    assert metadata["live_fetch_allowed"] is False
    assert metadata["fallback_used"] is True
    assert metadata["fallback_reason_category"] == "live_fetch_disabled"
    assert metadata["fetch_status"] == "disabled"
    assert metadata["post_count"] == 1
    assert metadata["comment_count"] == 3
    assert body["raw_posts"][0]["platform"] == "nga"
    assert body["raw_comments"][0]["raw_data"]["floor_number"] == "1F"


def test_crawl_start_mixed_reddit_and_public_parser_returns_both_metadata(monkeypatch) -> None:
    monkeypatch.setenv("REDDIT_ADAPTER_MODE", "mock")
    monkeypatch.setenv("PUBLIC_PARSER_LIVE_FETCH_ENABLED", "false")

    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["reddit", "the_paper"], "limit": 3},
    )

    body = response.json()
    metadata_by_platform = {item["platform"]: item for item in body["platform_metadata"]}

    assert response.status_code == 200
    assert set(metadata_by_platform) == {"reddit", "the_paper"}
    assert metadata_by_platform["reddit"]["adapter_mode"] == "mock"
    assert metadata_by_platform["the_paper"]["source_type"] == "public_page_parser"
    assert any(post["platform"] == "reddit" for post in body["raw_posts"])
    assert any(post["platform"] == "the_paper" for post in body["raw_posts"])
