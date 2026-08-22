import ast
from pathlib import Path
import socket
import urllib.request

import httpx
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
        "mock_static",
        "rss_mock",
        "gdelt_mock",
        "search_api_future",
        "user_url_list",
        "data_vendor_future",
    }.issubset(provider_ids)
    for provider in body["provider_statuses"]:
        assert provider["live_fetch_enabled"] is False
        assert provider["returns_full_content"] is False
        assert provider["returns_title_snippet_url"] is True
    assert body["safe_mode"]["static_metadata_only"] is True
    assert body["safe_mode"]["real_search_api_calls"] is False
    assert body["safe_mode"]["url_fetching"] is False
    assert body["safe_mode"]["scraping"] is False
    assert body["safe_mode"]["third_party_crawler_integrated"] is False
    assert any("User reviews candidates" in step for step in body["review_flow"])


def test_search_discovery_providers_endpoint_returns_mock_provider_taxonomy(monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError("Search Discovery providers must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)

    response = client.get("/api/v1/search-discovery/providers")

    assert response.status_code == 200
    providers = response.json()
    providers_by_id = {provider["provider_id"]: provider for provider in providers}
    for provider_id in ("mock_static", "rss_mock", "gdelt_mock"):
        provider = providers_by_id[provider_id]
        assert provider["provider_type"] == provider_id
        assert provider["status"] == "mock_only"
        assert provider["live_fetch_enabled"] is False
        assert provider["requires_network"] is False
        assert provider["returns_full_content"] is False
        assert provider["safety_boundary"]["url_fetching"] is False
        assert provider["safety_boundary"]["scraping"] is False
    assert providers_by_id["search_api_future"]["requires_api_key"] is True
    assert providers_by_id["search_api_future"]["credential_present"] is False


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


@pytest.mark.parametrize("provider", ["rss_mock", "gdelt_mock"])
def test_search_discovery_rss_and_gdelt_mock_candidates_are_static(provider, monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError(f"{provider} candidates must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)

    response = client.get(
        "/api/v1/search-discovery/mock-candidates",
        params={"query": "Tesla", "provider": provider},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "Tesla"
    assert body["candidate_count"] == 3
    assert body["provider_statuses"][0]["provider_id"] == provider
    assert body["provider_statuses"][0]["live_fetch_enabled"] is False
    assert all(candidate["provider"] == provider for candidate in body["candidates"])
    assert all(candidate["status"] == "pending_review" for candidate in body["candidates"])
    assert all(candidate["url"].startswith(f"https://example.test/{provider.split('_')[0]}/") for candidate in body["candidates"])
    assert all("URL was not fetched" in candidate["safety_notes"] for candidate in body["candidates"])


def test_search_discovery_does_not_expose_secrets_or_credentials() -> None:
    response_text = (
        client.get("/api/v1/search-discovery/status").text
        + client.get("/api/v1/search-discovery/providers").text
        + client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla"}).text
        + client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla", "provider": "rss_mock"}).text
        + client.get("/api/v1/search-discovery/mock-candidates", params={"query": "Tesla", "provider": "gdelt_mock"}).text
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

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    run_body = run_response.json()
    assert run_body["analysis_input_source"] == "case_evidence_items"
    graph_nodes = run_body["visualization_data"]["propagation_graph"]["nodes"]
    node_ids = [node["node_id"] for node in graph_nodes]
    assert len(node_ids) == len(set(node_ids))


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


@pytest.mark.parametrize("provider", ["rss_mock", "gdelt_mock"])
def test_accepting_rss_and_gdelt_mock_candidate_attaches_review_evidence(provider, monkeypatch) -> None:
    def fail_urlopen(*args, **kwargs):
        raise AssertionError(f"{provider} candidate attach must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)
    case_id = _create_case()
    candidate = client.get(
        "/api/v1/search-discovery/mock-candidates",
        params={"query": "Tesla", "provider": provider},
    ).json()["candidates"][0]
    candidate["status"] = "accepted"

    response = client.post(
        f"/api/v1/cases/{case_id}/search-discovery/candidates/attach",
        json={"candidates": [candidate], "reviewer_label": "qa_reviewer"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["attached_candidate_count"] == 1
    item = body["attached_evidence_items"][0]
    assert item["acquisition_mode"] == "search_discovery"
    assert item["provenance_type"] == "search_discovery_candidate"
    assert item["verification_status"] == "source_url_provided_unverified"
    assert item["review_status"] == "review_needed"
    assert item["raw_data_safe"]["provider"] == provider
    assert item["raw_data_safe"]["url_fetched"] is False
    assert item["raw_data_safe"]["scraping"] is False

    queue = client.get(f"/api/v1/cases/{case_id}/evidence/review-queue").json()
    assert queue["queue_count"] == 1
    assert queue["queue_items"][0]["provenance_type"] == "search_discovery_candidate"


def _create_case() -> str:
    response = client.post(
        "/api/v1/cases",
        json={"keyword": "Tesla", "platforms": ["public_web"], "title": "Search Discovery QA Case"},
    )
    assert response.status_code == 200
    return response.json()["case_id"]


def test_youtube_official_response_parser_preserves_search_order_and_skips_invalid_items() -> None:
    from app.services.crawling.youtube_adapter import (
        parse_official_search_and_videos_responses,
    )

    search_response = {
        "items": [
            {"id": {"videoId": "synthetic_b"}, "snippet": {"title": "Search B"}},
            {"id": {"videoId": ""}, "snippet": {"title": "Missing ID"}},
            {"id": {"videoId": "synthetic_a"}, "snippet": {"title": "Search A"}},
            "not-a-mapping",
        ]
    }
    videos_response = {
        "items": [
            {
                "id": "synthetic_a",
                "snippet": {"title": "Detail A"},
                "statistics": {"viewCount": "10"},
            },
            {
                "id": "synthetic_b",
                "snippet": {"title": "Detail B"},
                "statistics": {"viewCount": "20"},
            },
            {
                "id": "unselected_video",
                "snippet": {"title": "Unselected"},
                "statistics": {"viewCount": "999"},
            },
        ]
    }

    parsed = parse_official_search_and_videos_responses(search_response, videos_response)

    assert [item["id"] for item in parsed] == ["synthetic_b", "synthetic_a"]
    assert [item["snippet"]["title"] for item in parsed] == ["Detail B", "Detail A"]
    assert [item["statistics"]["viewCount"] for item in parsed] == ["20", "10"]
    assert all(item["source_type"] == "youtube_data_api_v3" for item in parsed)


def test_youtube_official_api_mock_route_is_bounded_offline_and_credential_free(monkeypatch) -> None:
    from app.services.crawling.youtube_adapter import YouTubeCredentials

    credential_reads = 0
    network_attempts = 0

    def fail_credentials(cls):
        nonlocal credential_reads
        credential_reads += 1
        raise AssertionError("Offline mocked official responses must not read credentials.")

    def fail_network(*args, **kwargs):
        nonlocal network_attempts
        network_attempts += 1
        raise AssertionError("Offline mocked official responses must not use real network primitives.")

    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(fail_credentials))
    monkeypatch.setattr(httpx.HTTPTransport, "handle_request", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)
    monkeypatch.setattr(socket, "create_connection", fail_network)

    response = client.get(
        "/api/v1/search-discovery/youtube-official-api/mock-candidates",
        params={"query": "Synthetic launch", "max_candidates": 3},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["query"] == "Synthetic launch"
    assert body["candidate_count"] == 3
    assert body["safe_mode"]["mock_candidates_only"] is True
    assert body["safe_mode"]["offline_mocked_official_response"] is True
    assert body["safe_mode"]["real_search_api_calls"] is False
    assert body["provider_statuses"][0]["provider_id"] == "youtube_official_api"
    assert body["provider_statuses"][0]["live_fetch_enabled"] is False
    assert body["provider_statuses"][0]["requires_api_key"] is False
    assert body["provider_statuses"][0]["requires_network"] is False
    assert body["provider_statuses"][0]["limits"]["max_candidates_per_query"] == 10
    assert all(item["provider"] == "youtube_official_api" for item in body["candidates"])
    assert all(item["platform_hint"] == "youtube" for item in body["candidates"])
    assert all(item["content_type_hint"] == "video" for item in body["candidates"])
    assert all(item["status"] == "pending_review" for item in body["candidates"])
    assert all(item["url"].startswith("https://www.youtube.com/watch?v=synthetic_") for item in body["candidates"])

    max_response = client.get(
        "/api/v1/search-discovery/youtube-official-api/mock-candidates",
        params={"query": "Synthetic launch", "max_candidates": 10},
    )
    assert max_response.status_code == 200
    assert max_response.json()["candidate_count"] == 10

    over_limit_response = client.get(
        "/api/v1/search-discovery/youtube-official-api/mock-candidates",
        params={"query": "Synthetic launch", "max_candidates": 11},
    )
    assert over_limit_response.status_code == 422
    assert credential_reads == 0
    assert network_attempts == 0


def test_youtube_official_api_candidate_reuses_attach_and_analysis_flow(monkeypatch) -> None:
    requested_paths: list[str] = []
    original_request = client.request

    def record_request(method, url, *args, **kwargs):
        requested_paths.append(str(url))
        return original_request(method, url, *args, **kwargs)

    monkeypatch.setattr(client, "request", record_request)
    case_id = _create_case()
    candidates = client.get(
        "/api/v1/search-discovery/youtube-official-api/mock-candidates",
        params={"query": "Synthetic launch", "max_candidates": 2},
    ).json()["candidates"]
    candidates[0]["status"] = "accepted"
    candidates[1]["status"] = "rejected"

    attach_response = client.post(
        f"/api/v1/cases/{case_id}/search-discovery/candidates/attach",
        json={"candidates": candidates, "reviewer_label": "phase1_offline_reviewer"},
    )

    assert attach_response.status_code == 200
    attach_body = attach_response.json()
    assert attach_body["attached_candidate_count"] == 1
    assert attach_body["rejected_candidate_count"] == 1
    item = attach_body["attached_evidence_items"][0]
    assert item["acquisition_mode"] == "search_discovery"
    assert item["provenance_type"] == "search_discovery_candidate"
    assert item["verification_status"] == "source_url_provided_unverified"
    assert item["trust_score"] == 0.48
    assert item["trust_label"] == "low"
    assert item["review_status"] == "review_needed"
    assert item["raw_data_safe"]["provider"] == "youtube_official_api"
    assert item["raw_data_safe"]["url_fetched"] is False
    assert item["raw_data_safe"]["scraping"] is False

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    assert run_response.json()["analysis_input_source"] == "case_evidence_items"
    assert not any("local-exchange-projections" in path for path in requested_paths)


def test_youtube_official_api_candidate_secret_like_metadata_is_redacted() -> None:
    case_id = _create_case()
    candidate = client.get(
        "/api/v1/search-discovery/youtube-official-api/mock-candidates",
        params={"query": "Synthetic launch", "max_candidates": 1},
    ).json()["candidates"][0]
    candidate.update(
        {
            "status": "accepted",
            "title": "api_key=synthetic-secret",
            "snippet": "access_token=synthetic-secret",
            "url": "https://www.youtube.com/watch?v=synthetic_001&client_secret=synthetic-secret",
        }
    )

    response = client.post(
        f"/api/v1/cases/{case_id}/search-discovery/candidates/attach",
        json={"candidates": [candidate]},
    )

    assert response.status_code == 200
    assert "synthetic-secret" not in response.text
    attached = response.json()["attached_evidence_items"][0]
    assert "[REDACTED]" in attached["title"]
    assert "[REDACTED]" in attached["body_text"]
    assert "[REDACTED]" in attached["url"]


def test_youtube_adapter_project_env_loading_is_function_local_and_ordered() -> None:
    adapter_path = Path(__file__).resolve().parents[1] / "services" / "crawling" / "youtube_adapter.py"
    tree = ast.parse(adapter_path.read_text(encoding="utf-8"))

    top_level_environment_imports = [
        node
        for node in tree.body
        if isinstance(node, ast.ImportFrom) and node.module == "app.core.environment"
    ]
    top_level_load_calls = [
        node
        for statement in tree.body
        if not isinstance(statement, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "load_project_env"
    ]

    assert top_level_environment_imports == []
    assert top_level_load_calls == []

    adapter_class = next(
        node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "YouTubeAdapter"
    )
    init_method = next(
        node for node in adapter_class.body if isinstance(node, ast.FunctionDef) and node.name == "__init__"
    )

    local_import_positions = [
        index
        for index, statement in enumerate(init_method.body)
        if any(
            isinstance(node, ast.ImportFrom)
            and node.module == "app.core.environment"
            and [alias.name for alias in node.names] == ["load_project_env"]
            for node in ast.walk(statement)
        )
    ]

    def call_positions(qualified_name: str) -> list[int]:
        return [
            index
            for index, statement in enumerate(init_method.body)
            if any(
                isinstance(node, ast.Call) and ast.unparse(node.func) == qualified_name
                for node in ast.walk(statement)
            )
        ]

    load_positions = call_positions("load_project_env")
    mode_positions = call_positions("_adapter_mode_from_env")
    credential_positions = call_positions("YouTubeCredentials.from_env")
    config_positions = call_positions("YouTubeAdapterConfig.from_env")

    assert len(local_import_positions) == 1
    assert len(load_positions) == 1
    assert len(mode_positions) == 1
    assert len(credential_positions) == 1
    assert len(config_positions) == 1
    assert load_positions[0] == local_import_positions[0] + 1
    assert load_positions[0] < min(mode_positions + credential_positions + config_positions)
