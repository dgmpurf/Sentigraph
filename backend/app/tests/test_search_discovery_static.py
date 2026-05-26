from pathlib import Path
import urllib.request

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def configure_temp_case_store(tmp_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(tmp_path / "cases.json")))
    reset_case_store()


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


def test_accepting_mock_candidate_attaches_search_discovery_evidence(monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError("Search Discovery candidate attach must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)
    case_id = _create_case()
    candidates = client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla"}).json()["candidates"]
    candidates[0]["status"] = "accepted"
    candidates[1]["status"] = "rejected"

    response = client.post(
        f"/api/v1/cases/{case_id}/search-discovery/candidates/attach",
        json={"candidates": candidates[:2], "reviewer_label": "qa_reviewer"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["attached_candidate_count"] == 1
    assert body["rejected_candidate_count"] == 1
    assert body["safe_mode"]["real_search_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False
    assert body["evidence_result"]["evidence_item_count"] == 1
    item = body["attached_evidence_items"][0]
    assert item["acquisition_mode"] == "search_discovery"
    assert item["provenance_type"] == "search_discovery_candidate"
    assert item["verification_status"] == "source_url_provided_unverified"
    assert item["source_url_present"] is True
    assert item["review_status"] == "review_needed"
    assert item["raw_data_safe"]["url_fetched"] is False
    assert "Mock discovery metadata only" in item["body_text"]

    evidence_response = client.get(f"/api/v1/cases/{case_id}/evidence")
    assert evidence_response.status_code == 200
    assert "public video reaction" not in evidence_response.text

    review_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-queue")
    assert review_response.status_code == 200
    queue = review_response.json()
    assert queue["queue_count"] == 1
    assert queue["queue_items"][0]["provenance_type"] == "search_discovery_candidate"

    jobs_response = client.get(f"/api/v1/cases/{case_id}/evidence/jobs")
    assert jobs_response.status_code == 200
    job = jobs_response.json()[0]
    assert job["input_type"] == "search_discovery"
    assert job["safe_metadata"]["real_search_api_calls"] is False
    assert job["safe_metadata"]["url_fetching"] is False


def test_search_discovery_candidate_attach_redacts_secret_like_metadata() -> None:
    case_id = _create_case()
    candidate = client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla"}).json()["candidates"][0]
    candidate.update(
        {
            "status": "accepted",
            "title": "api_key=should-not-appear",
            "snippet": "access_token=should-not-appear",
            "url": "https://example.test/news/item?client_secret=should-not-appear",
        }
    )

    response = client.post(
        f"/api/v1/cases/{case_id}/search-discovery/candidates/attach",
        json={"candidates": [candidate]},
    )

    assert response.status_code == 200
    assert "should-not-appear" not in response.text
    item = response.json()["attached_evidence_items"][0]
    assert "[REDACTED]" in item["title"]
    assert "[REDACTED]" in item["body_text"]
    assert "[REDACTED]" in item["url"]


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


def _create_case() -> str:
    response = client.post(
        "/api/v1/cases",
        json={"keyword": "Tesla", "platforms": ["public_web"], "title": "Search Discovery QA Case"},
    )
    assert response.status_code == 200
    return response.json()["case_id"]
