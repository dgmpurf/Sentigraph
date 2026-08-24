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
)


ENABLE_FLAG = (
    "SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_PUBLIC_DISCUSSION_ROUTE_ENABLED"
)
LOCAL_ROUTE_PATH = (
    "/youtube-official-api/live-public-discussion/{video_id}"
)
FULL_ROUTE_PATH = f"/api/v1/search-discovery{LOCAL_ROUTE_PATH}"
VIDEO_ID = "phase2e3a_video"
SYNTHETIC_CREDENTIAL = "phase2e3a-synthetic-credential-marker"
PRIVATE_PROVIDER_DETAIL = "phase2e3a-private-provider-detail"


class FakePublicDiscussionClient:
    def __init__(self, *, failure: Exception | None = None) -> None:
        self.failure = failure
        self.top_level_call_count = 0
        self.top_level_limits: list[int] = []
        self.search_call_count = 0
        self.comments_call_count = 0
        self.close_call_count = 0

    def fetch_top_level_comments(
        self,
        video_id: str,
        *,
        limit: int,
    ) -> list[Mapping[str, Any]]:
        assert video_id == VIDEO_ID
        self.top_level_call_count += 1
        self.top_level_limits.append(limit)
        if self.failure is not None:
            raise self.failure
        return [
            {
                "comment_id": f"phase2e3a_comment_{index}",
                "post_id": VIDEO_ID,
                "body_text": f"Synthetic public discussion {index}",
                "published_at": "2026-08-24T00:00:00Z",
                "like_count": index,
                "reply_count": 0,
                "author_id": f"private_author_{index}",
                "author_name": "Private synthetic author",
                "raw": {"credential": SYNTHETIC_CREDENTIAL},
            }
            for index in range(limit + 3)
        ]

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del keyword, limit, sort, date_range
        self.search_call_count += 1
        raise AssertionError("The public-discussion route must not search videos.")

    def fetch_comments(
        self,
        post_id: str,
        *,
        limit: int,
    ) -> list[Mapping[str, Any]]:
        del post_id, limit
        self.comments_call_count += 1
        raise AssertionError("The route must not call the legacy comments seam.")

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
        raise AssertionError("Real network access is forbidden in Phase-2E3A tests.")

    original_getenv = youtube_adapter_module.os.getenv

    def guarded_getenv(key: str, default: object = None) -> object:
        if key == "YOUTUBE_API_KEY":
            counters["real_credential_reads"] += 1
            raise AssertionError(
                "A real credential read is forbidden in Phase-2E3A tests."
            )
        return original_getenv(key, default)

    original_path_open = Path.open

    def guarded_path_open(self: Path, *args: object, **kwargs: object):
        if self.name == ".env":
            counters["repository_env_reads"] += 1
            raise AssertionError(
                "Repository .env access is forbidden in Phase-2E3A tests."
            )
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


def _wrapper():
    wrapper = getattr(
        service_module,
        "get_youtube_official_api_live_public_discussion_route",
        None,
    )
    assert callable(wrapper)
    return wrapper


def _has_constraint(field: object, attribute: str, value: object) -> bool:
    field_info = getattr(field, "field_info")
    return any(
        getattr(item, attribute, None) == value
        for item in field_info.metadata
    )


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | {
            nested_key
            for nested in value.values()
            for nested_key in _all_keys(nested)
        }
    if isinstance(value, list):
        return {
            nested_key
            for nested in value
            for nested_key in _all_keys(nested)
        }
    return set()


def test_hidden_route_metadata_path_method_response_model_and_query_bounds() -> None:
    route = _route(LOCAL_ROUTE_PATH)

    assert FULL_ROUTE_PATH == (
        "/api/v1/search-discovery/youtube-official-api/"
        "live-public-discussion/{video_id}"
    )
    assert route.methods == {"GET"}
    assert route.response_model is service_module.SearchDiscoveryDiscussionBatch
    assert route.include_in_schema is False

    path_parameters = {item.name: item for item in route.dependant.path_params}
    query_parameters = {item.name: item for item in route.dependant.query_params}
    assert set(path_parameters) == {"video_id"}
    assert set(query_parameters) == {"max_items"}
    assert query_parameters["max_items"].default == 20
    assert _has_constraint(query_parameters["max_items"], "ge", 1)
    assert _has_constraint(query_parameters["max_items"], "le", 20)


def test_disabled_gate_stops_before_credentials_or_client_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENABLE_FLAG, raising=False)
    calls = {"credentials": 0, "factory": 0}

    def fail_credentials() -> None:
        calls["credentials"] += 1
        raise AssertionError("Disabled route must not resolve credentials.")

    def fail_factory(credentials: YouTubeCredentials) -> FakePublicDiscussionClient:
        del credentials
        calls["factory"] += 1
        raise AssertionError("Disabled route must not construct a client.")

    error_type = getattr(
        service_module,
        "YouTubePublicDiscussionRouteDisabledError",
    )
    with pytest.raises(error_type):
        _wrapper()(
            VIDEO_ID,
            credentials_loader=fail_credentials,
            client_factory=fail_factory,
        )

    assert calls == {"credentials": 0, "factory": 0}


def test_enabled_missing_synthetic_credential_resolves_once_and_stops(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    calls = {"credentials": 0, "factory": 0}

    def missing_credentials() -> None:
        calls["credentials"] += 1
        return None

    def fail_factory(credentials: YouTubeCredentials) -> FakePublicDiscussionClient:
        del credentials
        calls["factory"] += 1
        raise AssertionError("Missing credentials must stop before construction.")

    error_type = getattr(
        service_module,
        "YouTubePublicDiscussionCredentialMissingError",
    )
    with pytest.raises(error_type):
        _wrapper()(
            VIDEO_ID,
            credentials_loader=missing_credentials,
            client_factory=fail_factory,
        )

    assert calls == {"credentials": 1, "factory": 0}


def test_enabled_success_calls_one_fake_top_level_seam_clamps_and_closes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    credentials = YouTubeCredentials(api_key=SYNTHETIC_CREDENTIAL)
    fake_client = FakePublicDiscussionClient()
    calls = {"credentials": 0, "factory": 0, "closer": 0}

    def synthetic_credentials() -> YouTubeCredentials:
        calls["credentials"] += 1
        return credentials

    def factory(received: YouTubeCredentials) -> FakePublicDiscussionClient:
        calls["factory"] += 1
        assert received is credentials
        return fake_client

    def closer(received: object) -> None:
        calls["closer"] += 1
        assert received is fake_client
        fake_client.close()

    batch = _wrapper()(
        VIDEO_ID,
        max_items=99,
        credentials_loader=synthetic_credentials,
        client_factory=factory,
        client_closer=closer,
    )

    assert calls == {"credentials": 1, "factory": 1, "closer": 1}
    assert fake_client.top_level_call_count == 1
    assert fake_client.top_level_limits == [20]
    assert fake_client.search_call_count == 0
    assert fake_client.comments_call_count == 0
    assert fake_client.close_call_count == 1
    assert batch.item_count == 20
    assert len(batch.items) == 20
    assert batch.safe_mode == {
        "public_discussion_text": True,
        "top_level_comments_only": True,
        "reply_content_acquired": False,
        "pagination": False,
        "url_fetching": False,
        "scraping": False,
        "cookies_used": False,
        "secrets_exposed": False,
        "evidence_write": False,
        "analysis_run": False,
        "human_review_required": True,
    }
    assert all(item.status == "pending_review" for item in batch.items)
    assert all(
        item.acquisition_mode == "search_discovery_public_discussion"
        for item in batch.items
    )
    assert all(item.provider == "youtube_official_api" for item in batch.items)
    assert all(item.platform_hint == "youtube" for item in batch.items)

    rendered = batch.model_dump(mode="json")
    assert SYNTHETIC_CREDENTIAL not in str(rendered)
    assert not (
        _all_keys(rendered)
        & {"author", "author_id", "author_name", "credential", "raw"}
    )


@pytest.mark.parametrize(
    "error_type",
    [
        YouTubeCommentsDisabledError,
        YouTubeAuthError,
        YouTubeQuotaError,
        YouTubeNetworkError,
        YouTubeParsingError,
        YouTubeRealModeError,
    ],
)
def test_typed_provider_failure_propagates_with_close_once_and_no_retry(
    error_type: type[YouTubeRealModeError],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    credentials = YouTubeCredentials(api_key=SYNTHETIC_CREDENTIAL)
    failure = error_type(PRIVATE_PROVIDER_DETAIL)
    fake_client = FakePublicDiscussionClient(failure=failure)
    calls = {"credentials": 0, "factory": 0, "closer": 0}

    def synthetic_credentials() -> YouTubeCredentials:
        calls["credentials"] += 1
        return credentials

    def factory(received: YouTubeCredentials) -> FakePublicDiscussionClient:
        calls["factory"] += 1
        assert received is credentials
        return fake_client

    def closer(received: object) -> None:
        calls["closer"] += 1
        assert received is fake_client
        fake_client.close()

    with pytest.raises(error_type) as captured:
        _wrapper()(
            VIDEO_ID,
            credentials_loader=synthetic_credentials,
            client_factory=factory,
            client_closer=closer,
        )

    assert captured.value is failure
    assert calls == {"credentials": 1, "factory": 1, "closer": 1}
    assert fake_client.top_level_call_count == 1
    assert fake_client.search_call_count == 0
    assert fake_client.comments_call_count == 0
    assert fake_client.close_call_count == 1


@pytest.mark.parametrize(
    ("failure_kind", "status_code", "detail"),
    [
        ("disabled", 404, "youtube_public_discussion_route_disabled"),
        ("credential", 503, "youtube_public_discussion_credential_missing"),
        ("comments", 404, "youtube_public_discussion_comments_unavailable"),
        ("auth", 502, "youtube_public_discussion_auth_error"),
        ("quota", 429, "youtube_public_discussion_quota_error"),
        ("network", 502, "youtube_public_discussion_network_error"),
        ("parsing", 502, "youtube_public_discussion_parsing_error"),
        ("provider", 502, "youtube_public_discussion_provider_error"),
    ],
)
def test_route_maps_only_stable_safe_http_errors(
    failure_kind: str,
    status_code: int,
    detail: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    error_types: dict[str, type[Exception]] = {
        "disabled": getattr(
            service_module,
            "YouTubePublicDiscussionRouteDisabledError",
        ),
        "credential": getattr(
            service_module,
            "YouTubePublicDiscussionCredentialMissingError",
        ),
        "comments": YouTubeCommentsDisabledError,
        "auth": YouTubeAuthError,
        "quota": YouTubeQuotaError,
        "network": YouTubeNetworkError,
        "parsing": YouTubeParsingError,
        "provider": YouTubeRealModeError,
    }
    failure = error_types[failure_kind](PRIVATE_PROVIDER_DETAIL)

    def fail_service(video_id: str, *, max_items: int):
        del video_id, max_items
        raise failure

    monkeypatch.setattr(
        route_module,
        "get_youtube_official_api_live_public_discussion_route",
        fail_service,
    )

    route_function = getattr(
        route_module,
        "search_discovery_youtube_official_api_live_public_discussion",
    )
    with pytest.raises(HTTPException) as captured:
        route_function(video_id=VIDEO_ID, max_items=20)

    assert captured.value.status_code == status_code
    assert captured.value.detail == detail
    assert "private" not in str(captured.value.detail)
    assert SYNTHETIC_CREDENTIAL not in str(captured.value.detail)


def test_route_returns_existing_batch_without_evidence_or_analysis_processing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = service_module.SearchDiscoveryDiscussionBatch(
        video_id=VIDEO_ID,
        item_count=0,
        items=[],
        safe_mode=dict(service_module.YOUTUBE_PUBLIC_DISCUSSION_SAFE_MODE),
    )
    calls: list[tuple[str, int]] = []

    def fake_service(video_id: str, *, max_items: int):
        calls.append((video_id, max_items))
        return expected

    monkeypatch.setattr(
        route_module,
        "get_youtube_official_api_live_public_discussion_route",
        fake_service,
    )
    route_function = getattr(
        route_module,
        "search_discovery_youtube_official_api_live_public_discussion",
    )

    actual = route_function(video_id=VIDEO_ID, max_items=7)

    assert actual is expected
    assert calls == [(VIDEO_ID, 7)]


def test_public_discussion_gate_is_independent_and_wrapper_is_narrow() -> None:
    wrapper = _wrapper()
    assert service_module.YOUTUBE_PUBLIC_DISCUSSION_ROUTE_ENABLE_FLAG == ENABLE_FLAG
    assert (
        service_module.YOUTUBE_PUBLIC_DISCUSSION_ROUTE_ENABLE_FLAG
        != service_module.YOUTUBE_LIVE_SEARCH_DISCOVERY_ROUTE_ENABLE_FLAG
    )

    source = inspect.getsource(wrapper)
    function = ast.parse(source).body[0]
    assert isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
    calls = {
        ast.unparse(node.func)
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
    }

    assert "os.getenv" in calls
    assert "YouTubeCredentials.from_env" in calls
    assert "get_youtube_official_api_live_public_discussion" in calls
    assert "load_project_env" not in calls
    assert "get_youtube_official_api_live_candidates" not in calls
    assert "search_discovery_candidates_to_evidence_items" not in calls
    assert "enrich_and_deduplicate_evidence_items" not in calls
    assert "YouTubeAdapter" not in calls
    assert "app.main" not in source
    assert "retry" not in source.lower()
    assert "pagination" not in source.lower()

    route_source = inspect.getsource(
        getattr(
            route_module,
            "search_discovery_youtube_official_api_live_public_discussion",
        )
    )
    assert "evidence" not in route_source.lower()
    assert "analysis" not in route_source.lower()
    assert "provider_selector" not in route_source
    assert "credential" not in inspect.signature(
        getattr(
            route_module,
            "search_discovery_youtube_official_api_live_public_discussion",
        )
    ).parameters
