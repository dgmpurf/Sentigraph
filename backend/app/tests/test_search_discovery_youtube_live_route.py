from __future__ import annotations

import ast
import inspect
from pathlib import Path
import socket
import sys
from typing import Any, Mapping
import urllib.request

from fastapi import HTTPException
import httpx
import pytest

import app.api.v1.routes.search_discovery as route_module
import app.services.crawling.youtube_adapter as youtube_adapter_module
import app.services.search_discovery as service_module
from app.services.crawling.youtube_adapter import (
    YouTubeAuthError,
    YouTubeCommentsDisabledError,
    YouTubeCredentials,
    YouTubeNetworkError,
    YouTubeParsingError,
    YouTubeQuotaError,
    YouTubeRealModeError,
    close_official_youtube_search_client,
    create_official_youtube_search_client,
)
from app.services.search_discovery import (
    YouTubeLiveSearchDiscoveryCredentialMissingError,
    YouTubeLiveSearchDiscoveryRouteDisabledError,
    get_youtube_official_api_live_route_candidates,
)


ENABLE_FLAG = "SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_ROUTE_ENABLED"
LOCAL_ROUTE_PATH = "/youtube-official-api/live-candidates"
FULL_ROUTE_PATH = f"/api/v1/search-discovery{LOCAL_ROUTE_PATH}"
PHASE1_ROUTE_PATH = "/youtube-official-api/mock-candidates"
SYNTHETIC_CREDENTIAL = "synthetic-route-credential-marker"


class FakeOfficialSearchClient:
    def __init__(self, *, failure: Exception | None = None) -> None:
        self.failure = failure
        self.search_call_count = 0
        self.search_limits: list[int] = []
        self.search_sorts: list[str] = []
        self.comment_call_count = 0
        self.close_call_count = 0

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        assert keyword == "Synthetic public event"
        assert date_range is None
        self.search_call_count += 1
        self.search_limits.append(limit)
        self.search_sorts.append(sort)
        if self.failure is not None:
            raise self.failure
        return [
            {
                "id": f"phase2d1_video_{index}",
                "snippet": {
                    "title": f"Phase 2D1 metadata candidate {index}",
                    "description": "Synthetic metadata for an offline route test.",
                    "channelTitle": "Phase 2D1 Synthetic Channel",
                    "publishedAt": "2026-08-22T00:00:00Z",
                },
                "statistics": {
                    "viewCount": "100",
                    "likeCount": "10",
                    "commentCount": "2",
                },
            }
            for index in range(limit)
        ]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        del post_id, limit
        self.comment_call_count += 1
        raise AssertionError("The Phase-2D1 live route must not fetch comments.")

    def close(self) -> None:
        self.close_call_count += 1


@pytest.fixture(autouse=True)
def hard_zero_guards(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    counters = {
        "real_network": 0,
        "real_credential_reads": 0,
        "repository_env_reads": 0,
    }

    def fail_network(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["real_network"] += 1
        raise AssertionError("Real network access is forbidden in Phase-2D1 tests.")

    original_getenv = youtube_adapter_module.os.getenv

    def guarded_getenv(key: str, default: object = None) -> object:
        if key == "YOUTUBE_API_KEY":
            counters["real_credential_reads"] += 1
            raise AssertionError("A real credential read is forbidden in Phase-2D1 tests.")
        return original_getenv(key, default)

    original_path_open = Path.open

    def guarded_path_open(self: Path, *args: object, **kwargs: object):
        if self.name == ".env":
            counters["repository_env_reads"] += 1
            raise AssertionError("Repository-root .env access is forbidden in Phase-2D1 tests.")
        return original_path_open(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "get", fail_network)
    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)
    monkeypatch.setattr(youtube_adapter_module.os, "getenv", guarded_getenv)
    monkeypatch.setattr(Path, "open", guarded_path_open)

    assert "app.main" not in sys.modules
    yield counters
    assert counters == {
        "real_network": 0,
        "real_credential_reads": 0,
        "repository_env_reads": 0,
    }
    assert "app.main" not in sys.modules


def _route(path: str):
    matches = [
        item
        for item in route_module.router.routes
        if getattr(item, "path", None) == path
    ]
    assert len(matches) == 1
    return matches[0]


def _has_constraint(field: object, attribute: str, value: object) -> bool:
    field_info = getattr(field, "field_info")
    return any(
        getattr(item, attribute, None) == value
        for item in field_info.metadata
    )


def test_hidden_live_route_metadata_and_query_bounds() -> None:
    route = _route(LOCAL_ROUTE_PATH)

    assert FULL_ROUTE_PATH == (
        "/api/v1/search-discovery/youtube-official-api/live-candidates"
    )
    assert route.methods == {"GET"}
    assert route.response_model is service_module.SearchDiscoveryBatch
    assert route.include_in_schema is False

    parameters = {item.name: item for item in route.dependant.query_params}
    assert set(parameters) == {"query", "max_candidates"}
    assert parameters["query"].default == "Tesla"
    assert _has_constraint(parameters["query"], "min_length", 1)
    assert _has_constraint(parameters["query"], "max_length", 120)
    assert parameters["max_candidates"].default == 5
    assert _has_constraint(parameters["max_candidates"], "ge", 1)
    assert _has_constraint(parameters["max_candidates"], "le", 5)


def test_public_official_client_factory_reuses_exact_credentials_and_closes_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    credentials = YouTubeCredentials(api_key=SYNTHETIC_CREDENTIAL)
    construction: dict[str, object] = {}

    class FakeInternalHttpxClient:
        def __init__(self) -> None:
            self.close_call_count = 0

        def close(self) -> None:
            self.close_call_count += 1

    internal_client = FakeInternalHttpxClient()

    def fake_httpx_client(*, timeout: float) -> FakeInternalHttpxClient:
        construction["timeout"] = timeout
        return internal_client

    monkeypatch.setattr(youtube_adapter_module.httpx, "Client", fake_httpx_client)

    official_client = create_official_youtube_search_client(credentials)

    assert official_client.credentials is credentials
    assert official_client.client is internal_client
    assert construction == {"timeout": 10.0}
    close_official_youtube_search_client(official_client)
    assert internal_client.close_call_count == 1


@pytest.mark.parametrize(
    "credentials",
    [None, YouTubeCredentials(api_key="")],
)
def test_public_official_client_factory_requires_valid_explicit_credentials(
    credentials: YouTubeCredentials | None,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    construction_count = 0

    def fail_construction(*args: object, **kwargs: object) -> None:
        nonlocal construction_count
        del args, kwargs
        construction_count += 1
        raise AssertionError("Invalid credentials must stop before client construction.")

    monkeypatch.setattr(youtube_adapter_module.httpx, "Client", fail_construction)

    with pytest.raises(YouTubeAuthError):
        create_official_youtube_search_client(credentials)  # type: ignore[arg-type]
    assert construction_count == 0


def test_disabled_gate_stops_before_credentials_or_client_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENABLE_FLAG, raising=False)
    calls = {"credentials": 0, "factory": 0}

    def fail_credentials(cls: type[YouTubeCredentials]) -> None:
        del cls
        calls["credentials"] += 1
        raise AssertionError("Disabled route must not resolve credentials.")

    def fail_factory(credentials: YouTubeCredentials) -> FakeOfficialSearchClient:
        del credentials
        calls["factory"] += 1
        raise AssertionError("Disabled route must not construct a client.")

    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(fail_credentials))

    with pytest.raises(YouTubeLiveSearchDiscoveryRouteDisabledError):
        get_youtube_official_api_live_route_candidates(
            "Synthetic public event",
            client_factory=fail_factory,
        )
    assert calls == {"credentials": 0, "factory": 0}


def test_enabled_missing_synthetic_credentials_resolves_once_and_stops(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    calls = {"credentials": 0, "factory": 0}

    def missing_credentials(cls: type[YouTubeCredentials]) -> None:
        del cls
        calls["credentials"] += 1
        return None

    def fail_factory(credentials: YouTubeCredentials) -> FakeOfficialSearchClient:
        del credentials
        calls["factory"] += 1
        raise AssertionError("Missing credentials must stop before client construction.")

    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(missing_credentials))

    with pytest.raises(YouTubeLiveSearchDiscoveryCredentialMissingError):
        get_youtube_official_api_live_route_candidates(
            "Synthetic public event",
            client_factory=fail_factory,
        )
    assert calls == {"credentials": 1, "factory": 0}


def test_enabled_success_reuses_one_credentials_object_clamps_and_closes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    credentials = YouTubeCredentials(api_key=SYNTHETIC_CREDENTIAL)
    fake_client = FakeOfficialSearchClient()
    calls = {"credentials": 0, "factory": 0, "closer": 0}

    def synthetic_credentials(cls: type[YouTubeCredentials]) -> YouTubeCredentials:
        del cls
        calls["credentials"] += 1
        return credentials

    def factory(received: YouTubeCredentials) -> FakeOfficialSearchClient:
        calls["factory"] += 1
        assert received is credentials
        return fake_client

    def closer(received: object) -> None:
        calls["closer"] += 1
        assert received is fake_client
        fake_client.close()

    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(synthetic_credentials))

    batch = get_youtube_official_api_live_route_candidates(
        "Synthetic public event",
        max_candidates=99,
        client_factory=factory,
        client_closer=closer,
    )

    assert calls == {"credentials": 1, "factory": 1, "closer": 1}
    assert fake_client.search_call_count == 1
    assert fake_client.search_limits == [5]
    assert fake_client.search_sorts == ["relevance"]
    assert fake_client.comment_call_count == 0
    assert fake_client.close_call_count == 1
    assert batch.candidate_count == 5
    assert len(batch.candidates) == 5
    assert batch.safe_mode == {
        "static_metadata_only": False,
        "mock_candidates_only": False,
        "offline_mocked_official_response": False,
        "real_search_api_calls": True,
        "real_website_api_calls": False,
        "url_fetching": False,
        "scraping": False,
        "cookies_used": False,
        "captcha_bypass": False,
        "anti_bot_bypass": False,
        "real_llm_calls": False,
        "secrets_exposed": False,
        "third_party_crawler_integrated": False,
    }
    assert all(item.status == "pending_review" for item in batch.candidates)
    assert all(item.acquisition_mode == "search_discovery" for item in batch.candidates)
    assert all("URL was not fetched" in item.safety_notes for item in batch.candidates)
    assert SYNTHETIC_CREDENTIAL not in str(batch.model_dump(mode="json"))


@pytest.mark.parametrize(
    "error_type",
    [YouTubeAuthError, YouTubeQuotaError, YouTubeNetworkError, YouTubeParsingError],
)
def test_typed_upstream_failure_closes_once_without_retry(
    error_type: type[YouTubeRealModeError],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    credentials = YouTubeCredentials(api_key=SYNTHETIC_CREDENTIAL)
    failure = error_type("private synthetic provider detail")
    fake_client = FakeOfficialSearchClient(failure=failure)
    calls = {"credentials": 0, "factory": 0, "closer": 0}

    def synthetic_credentials(cls: type[YouTubeCredentials]) -> YouTubeCredentials:
        del cls
        calls["credentials"] += 1
        return credentials

    def factory(received: YouTubeCredentials) -> FakeOfficialSearchClient:
        calls["factory"] += 1
        assert received is credentials
        return fake_client

    def closer(received: object) -> None:
        calls["closer"] += 1
        assert received is fake_client
        fake_client.close()

    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(synthetic_credentials))

    with pytest.raises(error_type) as captured:
        get_youtube_official_api_live_route_candidates(
            "Synthetic public event",
            client_factory=factory,
            client_closer=closer,
        )

    assert captured.value is failure
    assert calls == {"credentials": 1, "factory": 1, "closer": 1}
    assert fake_client.search_call_count == 1
    assert fake_client.comment_call_count == 0
    assert fake_client.close_call_count == 1


@pytest.mark.parametrize(
    ("failure", "status_code", "detail"),
    [
        (
            YouTubeLiveSearchDiscoveryRouteDisabledError("private disabled detail"),
            404,
            "youtube_live_search_discovery_route_disabled",
        ),
        (
            YouTubeLiveSearchDiscoveryCredentialMissingError("private credential detail"),
            503,
            "youtube_live_search_discovery_credential_missing",
        ),
        (
            YouTubeAuthError("private auth detail"),
            502,
            "youtube_live_search_discovery_auth_error",
        ),
        (
            YouTubeQuotaError("private quota detail"),
            429,
            "youtube_live_search_discovery_quota_error",
        ),
        (
            YouTubeNetworkError("private network detail"),
            502,
            "youtube_live_search_discovery_network_error",
        ),
        (
            YouTubeParsingError("private parsing detail"),
            502,
            "youtube_live_search_discovery_parsing_error",
        ),
        (
            YouTubeCommentsDisabledError("private provider detail"),
            502,
            "youtube_live_search_discovery_provider_error",
        ),
    ],
)
def test_route_maps_only_stable_safe_errors(
    failure: Exception,
    status_code: int,
    detail: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_service(query: str, *, max_candidates: int):
        del query, max_candidates
        raise failure

    monkeypatch.setattr(
        route_module,
        "get_youtube_official_api_live_route_candidates",
        fail_service,
    )

    with pytest.raises(HTTPException) as captured:
        route_module.search_discovery_youtube_official_api_live_candidates(
            query="Synthetic public event",
            max_candidates=5,
        )

    assert captured.value.status_code == status_code
    assert captured.value.detail == detail
    rendered = str(captured.value.detail)
    assert "private" not in rendered
    assert SYNTHETIC_CREDENTIAL not in rendered


def test_route_returns_service_batch_without_extra_processing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = service_module.get_youtube_official_api_mock_candidates(
        "Synthetic public event",
        max_candidates=1,
    )
    calls: list[tuple[str, int]] = []

    def fake_service(query: str, *, max_candidates: int):
        calls.append((query, max_candidates))
        return expected

    monkeypatch.setattr(
        route_module,
        "get_youtube_official_api_live_route_candidates",
        fake_service,
    )

    actual = route_module.search_discovery_youtube_official_api_live_candidates(
        query="Synthetic public event",
        max_candidates=3,
    )
    assert actual is expected
    assert calls == [("Synthetic public event", 3)]


def test_runtime_wrapper_is_structurally_narrow_and_env_fail_closed() -> None:
    source = inspect.getsource(get_youtube_official_api_live_route_candidates)
    function = ast.parse(source).body[0]
    assert isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
    calls = {
        ast.unparse(node.func)
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
    }

    assert "os.getenv" in calls
    assert "YouTubeCredentials.from_env" in calls
    assert "get_youtube_official_api_live_candidates" in calls
    assert "load_project_env" not in calls
    assert "YouTubeAdapter" not in calls
    assert "app.main" not in source
    assert "app.core.config" not in source
    assert "app.core.environment" not in source


def test_phase1_route_and_visible_provider_catalog_remain_mock_only() -> None:
    phase1_route = _route(PHASE1_ROUTE_PATH)
    assert phase1_route.methods == {"GET"}
    assert phase1_route.include_in_schema is True
    phase1_parameters = {
        item.name: item for item in phase1_route.dependant.query_params
    }
    assert phase1_parameters["max_candidates"].default == 5
    assert _has_constraint(phase1_parameters["max_candidates"], "le", 10)

    batch = service_module.get_youtube_official_api_mock_candidates(
        "Synthetic public event",
        max_candidates=10,
    )
    assert batch.candidate_count == 10
    assert batch.safe_mode["static_metadata_only"] is True
    assert batch.safe_mode["mock_candidates_only"] is True
    assert batch.safe_mode["offline_mocked_official_response"] is True
    assert batch.safe_mode["real_search_api_calls"] is False

    provider = next(
        item
        for item in service_module.get_search_discovery_provider_statuses()
        if item.provider_id == "youtube_official_api"
    )
    assert provider.status == "mock_only"
    assert provider.current_sentigraph_status == (
        "implemented_offline_mocked_official_response"
    )
    assert "offline mocked response" in provider.display_name.lower()
