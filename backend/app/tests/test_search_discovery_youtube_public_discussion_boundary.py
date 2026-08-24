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
from pydantic import ValidationError

import app.schemas.search_discovery as search_discovery_schema_module
import app.services.crawling.youtube_adapter as youtube_adapter_module
import app.services.search_discovery as search_discovery_service_module
from app.services.crawling.youtube_adapter import (
    YouTubeAdapter,
    YouTubeAuthError,
    YouTubeCommentsDisabledError,
    YouTubeCredentials,
    YouTubeNetworkError,
    YouTubeParsingError,
    YouTubeQuotaError,
    YouTubeRealModeError,
)


FAKE_API_KEY = "phase2e1-synthetic-youtube-key-marker"
VIDEO_ID = "phase2e1_video"
EXPECTED_SAFETY_NOTES = [
    "Official YouTube Data API public comment",
    "Top-level public comment text only",
    "Author identity omitted from this Search Discovery surface",
    "Reply content was not acquired",
    "Human review required before Evidence persistence",
    "Official API transport provenance is not truth verification",
]
EXPECTED_SAFE_MODE = {
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


def _raw_comment(index: int, *, video_id: str = VIDEO_ID) -> Mapping[str, Any]:
    return {
        "source_type": "youtube_data_api_v3",
        "comment_id": f"comment_{index}",
        "post_id": video_id,
        "body_text": f" Genuine provider comment {index} ",
        "published_at": f"2026-08-{index + 1:02d}T12:00:00Z",
        "like_count": str(index + 3),
        "reply_count": str(index),
        "author_id": f"must_not_escape_{index}",
        "author_name": f"Must Not Escape {index}",
    }


class FakePublicDiscussionClient:
    def __init__(
        self,
        comments: list[Mapping[str, Any]] | None = None,
        *,
        failure: Exception | None = None,
    ) -> None:
        self.comments = comments if comments is not None else [_raw_comment(0)]
        self.failure = failure
        self.call_count = 0
        self.video_ids: list[str] = []
        self.limits: list[int] = []

    def fetch_top_level_comments(
        self,
        post_id: str,
        *,
        limit: int,
    ) -> list[Mapping[str, Any]]:
        self.call_count += 1
        self.video_ids.append(post_id)
        self.limits.append(limit)
        if self.failure is not None:
            raise self.failure
        return list(self.comments)


@pytest.fixture
def hard_zero_guards(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    counters = {
        "network": 0,
        "credential_env": 0,
        "api_key_env": 0,
        "credential_presence": 0,
        "legacy_adapter": 0,
        "evidence": 0,
        "analysis": 0,
    }

    def fail_network(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["network"] += 1
        raise AssertionError("Real network access is forbidden in Phase-2E1.")

    def fail_credentials(cls: type[YouTubeCredentials]) -> None:
        del cls
        counters["credential_env"] += 1
        raise AssertionError("Credential environment resolution is forbidden.")

    def fail_getenv(key: str, default: object = None) -> object:
        del default
        if key == "YOUTUBE_API_KEY":
            counters["api_key_env"] += 1
        raise AssertionError("Environment reads are forbidden in Phase-2E1.")

    def fail_presence() -> dict[str, bool]:
        counters["credential_presence"] += 1
        raise AssertionError("Credential presence probing is forbidden.")

    def fail_adapter_init(self: YouTubeAdapter, *args: object, **kwargs: object) -> None:
        del self, args, kwargs
        counters["legacy_adapter"] += 1
        raise AssertionError("Legacy YouTubeAdapter construction is forbidden.")

    def fail_evidence(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["evidence"] += 1
        raise AssertionError("Evidence conversion or persistence is forbidden.")

    def fail_analysis(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["analysis"] += 1
        raise AssertionError("Analysis is forbidden in Phase-2E1.")

    monkeypatch.setattr(httpx.Client, "get", fail_network)
    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(urllib.request, "urlopen", fail_network)
    monkeypatch.setattr(YouTubeCredentials, "from_env", classmethod(fail_credentials))
    monkeypatch.setattr(youtube_adapter_module.os, "getenv", fail_getenv)
    monkeypatch.setattr(youtube_adapter_module, "_credential_presence", fail_presence)
    monkeypatch.setattr(YouTubeAdapter, "__init__", fail_adapter_init)
    monkeypatch.setattr(
        search_discovery_service_module,
        "search_discovery_candidates_to_evidence_items",
        fail_evidence,
    )
    monkeypatch.setattr(
        search_discovery_service_module,
        "enrich_and_deduplicate_evidence_items",
        fail_analysis,
    )

    yield counters

    assert counters == {
        "network": 0,
        "credential_env": 0,
        "api_key_env": 0,
        "credential_presence": 0,
        "legacy_adapter": 0,
        "evidence": 0,
        "analysis": 0,
    }


def _call_names(function: object) -> set[str]:
    source = textwrap.dedent(inspect.getsource(function))
    parsed = ast.parse(source).body[0]
    assert isinstance(parsed, (ast.FunctionDef, ast.AsyncFunctionDef))
    return {
        ast.unparse(node.func)
        for node in ast.walk(parsed)
        if isinstance(node, ast.Call)
    }


def test_public_discussion_symbols_exist_and_seams_are_structurally_fail_closed() -> None:
    assert "app.main" not in sys.modules

    adapter_seam = getattr(
        youtube_adapter_module,
        "fetch_youtube_official_api_live_public_comments",
        None,
    )
    service_seam = getattr(
        search_discovery_service_module,
        "get_youtube_official_api_live_public_discussion",
        None,
    )
    assert callable(adapter_seam), "Phase-2E1 adapter seam is not implemented yet."
    assert callable(service_seam), "Phase-2E1 service seam is not implemented yet."
    assert hasattr(youtube_adapter_module, "YouTubePublicDiscussionHttpClient")
    assert hasattr(search_discovery_schema_module, "SearchDiscoveryDiscussionItem")
    assert hasattr(search_discovery_schema_module, "SearchDiscoveryDiscussionBatch")

    forbidden_adapter_calls = {
        "load_project_env",
        "YouTubeCredentials.from_env",
        "_credential_presence",
        "os.getenv",
        "YouTubeAdapter",
        "_OfficialYouTubeClient",
        "http_client.fetch_comments",
        "http_client.search_posts",
    }
    adapter_calls = _call_names(adapter_seam)
    assert forbidden_adapter_calls.isdisjoint(adapter_calls)
    assert "http_client.fetch_top_level_comments" in adapter_calls

    service_calls = _call_names(service_seam)
    assert "search_discovery_candidates_to_evidence_items" not in service_calls
    assert "enrich_and_deduplicate_evidence_items" not in service_calls


def test_explicit_seam_requires_credentials_and_clamps_one_injected_call(
    hard_zero_guards: dict[str, int],
) -> None:
    seam = youtube_adapter_module.fetch_youtube_official_api_live_public_comments
    fake = FakePublicDiscussionClient([_raw_comment(index) for index in range(25)])

    with pytest.raises(YouTubeAuthError):
        seam(
            VIDEO_ID,
            credentials=YouTubeCredentials(api_key=""),
            http_client=fake,
            limit=99,
        )
    assert fake.call_count == 0

    result = seam(
        VIDEO_ID,
        credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
        http_client=fake,
        limit=99,
    )
    assert len(result) == 20
    assert fake.call_count == 1
    assert fake.video_ids == [VIDEO_ID]
    assert fake.limits == [20]
    assert all(value == 0 for value in hard_zero_guards.values())


@pytest.mark.parametrize(
    "error_type",
    [
        YouTubeAuthError,
        YouTubeQuotaError,
        YouTubeNetworkError,
        YouTubeParsingError,
        YouTubeCommentsDisabledError,
    ],
)
def test_typed_public_comment_failures_propagate_without_retry_or_fallback(
    error_type: type[YouTubeRealModeError],
    hard_zero_guards: dict[str, int],
) -> None:
    failure = error_type("phase2e1_synthetic_failure")
    fake = FakePublicDiscussionClient(failure=failure)

    with pytest.raises(error_type) as captured:
        youtube_adapter_module.fetch_youtube_official_api_live_public_comments(
            VIDEO_ID,
            credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
            http_client=fake,
            limit=5,
        )

    assert captured.value is failure
    assert fake.call_count == 1
    assert fake.video_ids == [VIDEO_ID]
    assert fake.limits == [5]
    assert all(value == 0 for value in hard_zero_guards.values())


@pytest.mark.parametrize(
    "bad_result",
    [None, {"items": []}, [None], ["not-a-mapping"]],
)
def test_public_comment_seam_rejects_non_list_or_non_mapping_results(
    bad_result: object,
    hard_zero_guards: dict[str, int],
) -> None:
    class BadResultClient:
        def fetch_top_level_comments(self, post_id: str, *, limit: int) -> object:
            del post_id, limit
            return bad_result

    with pytest.raises(YouTubeParsingError):
        youtube_adapter_module.fetch_youtube_official_api_live_public_comments(
            VIDEO_ID,
            credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
            http_client=BadResultClient(),  # type: ignore[arg-type]
            limit=5,
        )
    assert all(value == 0 for value in hard_zero_guards.values())


def test_official_primitive_requests_snippet_only_and_ignores_embedded_replies() -> None:
    official_client_type = youtube_adapter_module._OfficialYouTubeClient
    official_client = object.__new__(official_client_type)
    official_client.credentials = YouTubeCredentials(api_key=FAKE_API_KEY)
    calls: list[tuple[str, Mapping[str, Any]]] = []

    def fake_get_json(url: str, *, params: Mapping[str, Any]) -> Mapping[str, Any]:
        calls.append((url, dict(params)))
        return {
            "items": [
                {
                    "snippet": {
                        "videoId": VIDEO_ID,
                        "totalReplyCount": 2,
                        "topLevelComment": {
                            "id": "comment_top",
                            "snippet": {
                                "videoId": VIDEO_ID,
                                "textOriginal": "Top-level provider text",
                                "publishedAt": "2026-08-24T12:00:00Z",
                                "likeCount": 7,
                                "authorChannelId": {"value": "private_to_surface"},
                                "authorDisplayName": "Private To Surface",
                            },
                        },
                    },
                    "replies": {
                        "comments": [
                            {
                                "id": "reply_must_not_appear",
                                "snippet": {
                                    "parentId": "comment_top",
                                    "textOriginal": "Reply content must not appear",
                                },
                            }
                        ]
                    },
                }
            ],
            "nextPageToken": "must_not_be_followed",
        }

    official_client._get_json = fake_get_json
    result = official_client.fetch_top_level_comments(VIDEO_ID, limit=99)

    assert len(calls) == 1
    endpoint, params = calls[0]
    assert endpoint == youtube_adapter_module.YOUTUBE_COMMENT_THREADS_ENDPOINT
    assert params == {
        "part": "snippet",
        "videoId": VIDEO_ID,
        "maxResults": 20,
        "order": "relevance",
        "textFormat": "plainText",
        "key": FAKE_API_KEY,
    }
    assert result == [
        {
            "source_type": "youtube_data_api_v3",
            "comment_id": "comment_top",
            "post_id": VIDEO_ID,
            "body_text": "Top-level provider text",
            "published_at": "2026-08-24T12:00:00Z",
            "like_count": 7,
            "reply_count": 2,
        }
    ]
    assert "reply_must_not_appear" not in str(result)
    assert "Reply content must not appear" not in str(result)
    assert "author" not in str(result).lower()


def test_mapper_preserves_text_omits_identity_and_skips_malformed_or_reply_items() -> None:
    mapper = search_discovery_service_module.map_youtube_official_api_live_public_discussion
    mapped = mapper(
        VIDEO_ID,
        [
            _raw_comment(0),
            {**_raw_comment(1), "parent_id": "comment_0"},
            {"comment_id": "", "body_text": "missing id"},
            {"comment_id": "missing_body", "body_text": ""},
            {**_raw_comment(2), "post_id": "different_video"},
        ],
        max_items=20,
    )

    assert len(mapped) == 1
    item = mapped[0]
    assert item.discussion_id == "youtube_official_api_phase2e1_video_comment_0"
    assert item.provider == "youtube_official_api"
    assert item.platform_hint == "youtube"
    assert item.video_id == VIDEO_ID
    assert item.comment_id == "comment_0"
    assert item.body_text == "Genuine provider comment 0"
    assert item.published_at == "2026-08-01T12:00:00Z"
    assert item.like_count == 3
    assert item.reply_count == 0
    assert item.source_url == (
        "https://www.youtube.com/watch?v=phase2e1_video&lc=comment_0"
    )
    assert item.content_type_hint == "comment"
    assert item.acquisition_mode == "search_discovery_public_discussion"
    assert item.status == "pending_review"
    assert item.safety_notes == EXPECTED_SAFETY_NOTES

    item_fields = set(item.model_dump(mode="json"))
    assert item_fields.isdisjoint(
        {
            "author_id",
            "author_channel_id",
            "author_name",
            "author_display_name",
            "raw",
            "raw_data",
            "credential",
            "key",
        }
    )


def test_discussion_schema_forbids_author_identity_and_raw_upstream_fields() -> None:
    item_type = search_discovery_schema_module.SearchDiscoveryDiscussionItem
    with pytest.raises(ValidationError):
        item_type(
            discussion_id="discussion_forbidden_extra",
            video_id=VIDEO_ID,
            comment_id="comment_forbidden_extra",
            body_text="Public comment",
            source_url=f"https://www.youtube.com/watch?v={VIDEO_ID}&lc=comment_forbidden_extra",
            safety_notes=EXPECTED_SAFETY_NOTES,
            author_name="Must be rejected",
        )


def test_service_batch_calls_one_seam_and_keeps_review_only_hard_zeroes(
    hard_zero_guards: dict[str, int],
) -> None:
    fake = FakePublicDiscussionClient([_raw_comment(index) for index in range(25)])
    batch = search_discovery_service_module.get_youtube_official_api_live_public_discussion(
        VIDEO_ID,
        credentials=YouTubeCredentials(api_key=FAKE_API_KEY),
        http_client=fake,
        max_items=99,
    )

    assert batch.video_id == VIDEO_ID
    assert batch.item_count == 20
    assert len(batch.items) == 20
    assert fake.call_count == 1
    assert fake.video_ids == [VIDEO_ID]
    assert fake.limits == [20]
    assert batch.safe_mode == EXPECTED_SAFE_MODE
    assert all(item.status == "pending_review" for item in batch.items)
    assert all(item.safety_notes == EXPECTED_SAFETY_NOTES for item in batch.items)
    assert FAKE_API_KEY not in str(batch.model_dump(mode="json"))
    assert all(value == 0 for value in hard_zero_guards.values())
