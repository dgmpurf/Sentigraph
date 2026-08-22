from __future__ import annotations

import ast
import inspect
import socket
import sys
import textwrap
import urllib.request
from typing import Any, Mapping

import httpx
import pytest

import app.services.crawling.youtube_adapter as youtube_adapter_module
from app.services.crawling.youtube_adapter import (
    YouTubeAdapter,
    YouTubeAuthError,
    YouTubeCredentials,
    YouTubeNetworkError,
    YouTubeParsingError,
    YouTubeQuotaError,
    search_youtube_official_api_live_metadata,
)
from app.services.search_discovery import (
    get_youtube_official_api_live_candidates,
    get_youtube_official_api_mock_candidates,
    map_youtube_official_api_live_candidates,
    search_discovery_candidates_to_evidence_items,
)


FAKE_API_KEY = "phase2b-synthetic-youtube-key-marker"


class FakeOfficialSearchClient:
    def __init__(self, failure: Exception | None = None) -> None:
        self.failure = failure
        self.search_call_count = 0
        self.videos_call_count = 0
        self.comment_call_count = 0
        self.search_limits: list[int] = []
        self.search_sorts: list[str] = []

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        del date_range
        self.search_call_count += 1
        self.search_limits.append(limit)
        self.search_sorts.append(sort)
        if self.failure is not None:
            raise self.failure

        self.videos_call_count += 1
        return [
            {
                "source_type": "youtube_data_api_v3",
                "id": f"phase2b_video_{index}",
                "snippet": {
                    "channelId": f"phase2b_channel_{index}",
                    "channelTitle": f"Phase 2B Channel {index}",
                    "title": f"{keyword} official metadata {index}",
                    "description": f"Public video metadata candidate {index}.",
                    "publishedAt": f"2026-08-{index + 10:02d}T12:00:00Z",
                },
                "statistics": {
                    "viewCount": str(1000 + index),
                    "likeCount": str(100 + index),
                    "commentCount": str(10 + index),
                },
            }
            for index in range(6)
        ]

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        del post_id, limit
        self.comment_call_count += 1
        raise AssertionError("The Search Discovery live boundary must not fetch comments.")


@pytest.fixture
def hard_zero_guards(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    counters = {
        "network": 0,
        "credential_env": 0,
        "api_key_env": 0,
        "credential_presence": 0,
        "adapter_construction": 0,
        "default_client_construction": 0,
    }

    def fail_network(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["network"] += 1
        raise AssertionError("Real network access is forbidden in the Phase-2B focused test.")

    def fail_credentials(cls: type[YouTubeCredentials]) -> None:
        del cls
        counters["credential_env"] += 1
        raise AssertionError("Credential environment resolution is forbidden.")

    def fail_getenv(key: str, default: object = None) -> object:
        del default
        if key == "YOUTUBE_API_KEY":
            counters["api_key_env"] += 1
        raise AssertionError("Environment reads are forbidden in the new live seam.")

    def fail_presence() -> dict[str, bool]:
        counters["credential_presence"] += 1
        raise AssertionError("Credential presence probing is forbidden.")

    def fail_adapter_init(self: YouTubeAdapter, *args: object, **kwargs: object) -> None:
        del self, args, kwargs
        counters["adapter_construction"] += 1
        raise AssertionError("YouTubeAdapter construction is forbidden in the new live seam.")

    def fail_default_client(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["default_client_construction"] += 1
        raise AssertionError("The focused test requires the injected fake client.")

    monkeypatch.setattr(httpx.Client, "get", fail_network)
    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)
    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(fail_credentials))
    monkeypatch.setattr(youtube_adapter_module.os, "getenv", fail_getenv)
    monkeypatch.setattr(youtube_adapter_module, "_credential_presence", fail_presence)
    monkeypatch.setattr(YouTubeAdapter, "__init__", fail_adapter_init)
    monkeypatch.setattr(youtube_adapter_module, "_OfficialYouTubeClient", fail_default_client)

    yield counters

    assert counters == {
        "network": 0,
        "credential_env": 0,
        "api_key_env": 0,
        "credential_presence": 0,
        "adapter_construction": 0,
        "default_client_construction": 0,
    }


def test_new_live_seam_is_service_only_and_structurally_env_free() -> None:
    assert "app.main" not in sys.modules

    source = textwrap.dedent(inspect.getsource(search_youtube_official_api_live_metadata))
    function = ast.parse(source).body[0]
    assert isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
    calls = {
        ast.unparse(node.func)
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
    }
    assert "load_project_env" not in calls
    assert "YouTubeCredentials.from_env" not in calls
    assert "_credential_presence" not in calls
    assert "os.getenv" not in calls
    assert "YouTubeAdapter" not in calls
    assert "_OfficialYouTubeClient" not in calls


def test_injected_live_boundary_clamps_to_five_and_maps_review_candidates(
    hard_zero_guards: dict[str, int],
) -> None:
    fake_client = FakeOfficialSearchClient()
    credentials = YouTubeCredentials(api_key=FAKE_API_KEY)

    batch = get_youtube_official_api_live_candidates(
        "Synthetic public event",
        credentials=credentials,
        http_client=fake_client,
        max_candidates=99,
    )

    assert batch.candidate_count == 5
    assert len(batch.candidates) == 5
    assert fake_client.search_call_count == 1
    assert fake_client.videos_call_count == 1
    assert fake_client.comment_call_count == 0
    assert fake_client.search_limits == [5]
    assert fake_client.search_sorts == ["relevance"]
    assert all(candidate.provider == "youtube_official_api" for candidate in batch.candidates)
    assert all(candidate.platform_hint == "youtube" for candidate in batch.candidates)
    assert all(candidate.content_type_hint == "video" for candidate in batch.candidates)
    assert all(candidate.status == "pending_review" for candidate in batch.candidates)
    assert all(candidate.acquisition_mode == "search_discovery" for candidate in batch.candidates)
    assert all(candidate.url.startswith("https://www.youtube.com/watch?v=") for candidate in batch.candidates)
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
    assert FAKE_API_KEY not in str(batch.model_dump(mode="json"))
    assert all(value == 0 for value in hard_zero_guards.values())


def test_live_mapping_uses_exact_neutral_fallbacks_and_provenance_notes() -> None:
    candidates = map_youtube_official_api_live_candidates(
        "Public event",
        [{"id": "live_video_without_metadata", "snippet": {}}],
        max_candidates=1,
    )

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.title == "Public event YouTube Official API metadata candidate"
    assert candidate.snippet == "YouTube Data API metadata lead only; URL content was not fetched."
    assert candidate.source_name == "YouTube Official API"
    assert candidate.safety_notes == [
        "Official YouTube Data API metadata lead",
        "URL was not fetched",
        "Snippet is not full content",
        "Human review required before attach",
        "Official API transport provenance is not truth verification",
    ]
    controlled_labels = " ".join(
        [candidate.title, candidate.snippet, candidate.source_name, *candidate.safety_notes]
    ).lower()
    assert "offline" not in controlled_labels
    assert "mock" not in controlled_labels
    assert "synthetic fixture" not in controlled_labels


def test_live_mapping_preserves_genuine_provider_text() -> None:
    candidates = map_youtube_official_api_live_candidates(
        "Public event",
        [
            {
                "id": "provider_text_video",
                "snippet": {
                    "title": "Synthetic is part of the provider title",
                    "description": "Mock is part of the provider description",
                    "channelTitle": "Offline Artists Channel",
                },
            }
        ],
        max_candidates=1,
    )

    candidate = candidates[0]
    assert candidate.title == "Synthetic is part of the provider title"
    assert candidate.snippet == "Mock is part of the provider description"
    assert candidate.source_name == "Offline Artists Channel"


def test_public_mapping_seam_is_metadata_only_and_limit_bounded() -> None:
    fake_client = FakeOfficialSearchClient()
    metadata = fake_client.search_posts(
        "Synthetic public event",
        limit=5,
        sort="relevance",
    )

    candidates = map_youtube_official_api_live_candidates(
        "Synthetic public event",
        metadata,
        max_candidates=3,
    )

    assert len(candidates) == 3
    assert [candidate.candidate_id for candidate in candidates] == [
        "youtube_official_api_phase2b_video_0",
        "youtube_official_api_phase2b_video_1",
        "youtube_official_api_phase2b_video_2",
    ]
    assert all(candidate.status == "pending_review" for candidate in candidates)
    assert all(candidate.source_name.startswith("Phase 2B Channel") for candidate in candidates)
    assert all(candidate.published_at for candidate in candidates)


def test_live_candidate_reuses_conservative_search_discovery_trust_lineage(
    hard_zero_guards: dict[str, int],
) -> None:
    batch = get_youtube_official_api_live_candidates(
        "Synthetic public event",
        credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
        http_client=FakeOfficialSearchClient(),
        max_candidates=1,
    )
    accepted = batch.candidates[0].model_copy(update={"status": "accepted"})

    evidence_items, skipped_count, rejected_count, warnings = (
        search_discovery_candidates_to_evidence_items(
            case_id="case_phase2b_offline_boundary",
            candidates=[accepted],
            reviewer_label="phase2b_offline_reviewer",
        )
    )

    assert skipped_count == 0
    assert rejected_count == 0
    assert warnings == []
    assert len(evidence_items) == 1
    evidence = evidence_items[0]
    assert evidence.acquisition_mode == "search_discovery"
    assert evidence.provenance_type == "search_discovery_candidate"
    assert evidence.verification_status == "source_url_provided_unverified"
    assert evidence.trust_score == 0.48
    assert evidence.trust_label == "low"
    assert evidence.review_status == "review_needed"
    assert evidence.raw_data_safe["url_fetched"] is False
    assert evidence.raw_data_safe["scraping"] is False
    assert FAKE_API_KEY not in str(evidence.model_dump(mode="json"))
    assert all(value == 0 for value in hard_zero_guards.values())


@pytest.mark.parametrize(
    "error_type",
    [YouTubeAuthError, YouTubeNetworkError, YouTubeQuotaError, YouTubeParsingError],
)
def test_live_boundary_propagates_typed_failures_without_mock_fallback_or_retry(
    error_type: type[Exception],
    hard_zero_guards: dict[str, int],
) -> None:
    failure = error_type("synthetic_typed_failure")
    fake_client = FakeOfficialSearchClient(failure=failure)

    with pytest.raises(error_type) as captured:
        get_youtube_official_api_live_candidates(
            "Synthetic public event",
            credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
            http_client=fake_client,
            max_candidates=5,
        )

    assert captured.value is failure
    assert fake_client.search_call_count == 1
    assert fake_client.videos_call_count == 0
    assert fake_client.comment_call_count == 0
    assert all(value == 0 for value in hard_zero_guards.values())


def test_live_boundary_requires_nonempty_explicit_credentials(
    hard_zero_guards: dict[str, int],
) -> None:
    fake_client = FakeOfficialSearchClient()

    with pytest.raises(YouTubeAuthError):
        search_youtube_official_api_live_metadata(
            "Synthetic public event",
            credentials=YouTubeCredentials(api_key=""),
            http_client=fake_client,
            limit=5,
        )

    assert fake_client.search_call_count == 0
    assert fake_client.videos_call_count == 0
    assert fake_client.comment_call_count == 0
    assert all(value == 0 for value in hard_zero_guards.values())


def test_phase1_offline_fixture_semantics_remain_unchanged(
    hard_zero_guards: dict[str, int],
) -> None:
    batch = get_youtube_official_api_mock_candidates(
        "Synthetic public event",
        max_candidates=10,
    )

    assert batch.candidate_count == 10
    assert batch.safe_mode["static_metadata_only"] is True
    assert batch.safe_mode["mock_candidates_only"] is True
    assert batch.safe_mode["offline_mocked_official_response"] is True
    assert batch.safe_mode["real_search_api_calls"] is False
    assert all(candidate.provider == "youtube_official_api" for candidate in batch.candidates)
    assert batch.candidates[0].safety_notes[0] == "Offline mocked official response only"
    assert all(value == 0 for value in hard_zero_guards.values())
