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


def test_crawl_start_non_reddit_keeps_old_mock_first_behavior() -> None:
    response = client.post(
        "/api/v1/crawl/start",
        json={"keyword": "Tesla", "platforms": ["weibo"], "limit": 100},
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
