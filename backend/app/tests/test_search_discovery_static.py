from pathlib import Path
import urllib.request

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_search_discovery_status_is_static_and_safe(monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError("Search Discovery status must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)

    response = client.get("/api/v1/search-discovery/status")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "planning_mock_only"
    provider_ids = {provider["provider_id"] for provider in body["provider_statuses"]}
    assert {
        "search_engine_api",
        "news_discovery_api",
        "rss_feeds",
        "site_public_search",
        "user_url_list",
        "data_vendor",
        "mock_fixture",
    }.issubset(provider_ids)
    assert body["safe_mode"]["static_metadata_only"] is True
    assert body["safe_mode"]["real_search_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False
    assert body["safe_mode"]["scraping"] is False
    assert body["safe_mode"]["third_party_crawler_integrated"] is False
    assert any("User reviews candidates" in step for step in body["review_flow"])


def test_search_discovery_mock_candidates_return_review_only_metadata(monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError("Mock Search Discovery candidates must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)

    response = client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla"})

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "Tesla"
    assert body["candidate_count"] == 4
    assert body["safe_mode"]["mock_candidates_only"] is True
    assert body["safe_mode"]["real_search_api_calls"] is False
    assert body["safe_mode"]["real_website_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False
    assert all(candidate["acquisition_mode"] == "search_discovery" for candidate in body["candidates"])
    assert all(candidate["status"] == "pending_review" for candidate in body["candidates"])
    assert all(candidate["url"].startswith("https://example.test/") for candidate in body["candidates"])
    assert all("URL was not fetched" in candidate["safety_notes"] for candidate in body["candidates"])


def test_search_discovery_does_not_expose_secrets_or_credentials() -> None:
    response_text = (
        client.get("/api/v1/search-discovery/status").text
        + client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla"}).text
    ).lower()

    forbidden_fragments = [
        "youtube_api_key",
        "douyin_client_secret",
        "access_token=",
        "refresh_token=",
        "client_secret=",
        "authorization:",
        "cookie:",
    ]
    for fragment in forbidden_fragments:
        assert fragment not in response_text


def test_search_discovery_does_not_integrate_mediacrawler_in_product_code() -> None:
    body = client.get("/api/v1/search-discovery/status").json()
    assert body["safe_mode"]["third_party_crawler_integrated"] is False

    repo_root = Path(__file__).resolve().parents[3]
    product_paths = [
        repo_root / "backend" / "app" / "api",
        repo_root / "backend" / "app" / "schemas",
        repo_root / "backend" / "app" / "services",
        repo_root / "frontend" / "src",
    ]
    matches: list[str] = []
    for product_path in product_paths:
        for file_path in product_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in {".py", ".js", ".jsx", ".ts", ".tsx"}:
                text = file_path.read_text(encoding="utf-8", errors="ignore").lower()
                if "mediacrawler" in text or "media crawler" in text:
                    matches.append(str(file_path.relative_to(repo_root)))

    assert matches == []
