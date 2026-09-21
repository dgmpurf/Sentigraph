from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from pydantic import ValidationError

import app.services.case_store as case_store_module
import app.services.search_discovery as search_discovery_service_module
from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest
from app.schemas.search_discovery import (
    SearchDiscoveryDiscussionBatch,
    SearchDiscoveryDiscussionItem,
    YouTubeReviewedPublicDiscussionAttachRequest,
)
from app.services.crawling.youtube_adapter import (
    YouTubeAuthError,
    YouTubeNetworkError,
    YouTubeParsingError,
    YouTubeQuotaError,
)
from app.services.evidence_ingestion import analysis_eligible_evidence_items
from app.services.storage.local_json_store import LocalJsonCaseStore


VIDEO_ID = "AbC-d_EfG12"
ENABLE_FLAG = (
    "SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_REVIEWED_EVIDENCE_ATTACH_ENABLED"
)
EXPECTED_SAFE_MODE = {
    "official_api_public": True,
    "server_side_refetch": True,
    "top_level_comments_only": True,
    "reply_content_acquired": False,
    "author_identity_persisted": False,
    "url_fetching": False,
    "scraping": False,
    "cookies_used": False,
    "secrets_exposed": False,
    "case_evidence_write": True,
    "production_evidence_layer_write": False,
    "review_queue_runtime": False,
    "analysis_run": False,
    "report_triggered": False,
    "production_object_created": False,
    "automatic_truth_upgrade": False,
    "human_review_required": True,
}


class FakeDiscussionLoader:
    def __init__(
        self,
        batch: SearchDiscoveryDiscussionBatch,
        *,
        failure: Exception | None = None,
    ) -> None:
        self.batch = batch
        self.failure = failure
        self.call_count = 0
        self.video_ids: list[str] = []
        self.max_items: list[int] = []

    def __call__(
        self,
        video_id: str,
        *,
        max_items: int,
    ) -> SearchDiscoveryDiscussionBatch:
        self.call_count += 1
        self.video_ids.append(video_id)
        self.max_items.append(max_items)
        if self.failure is not None:
            raise self.failure
        return self.batch


@pytest.fixture(autouse=True)
def isolated_case_store(tmp_path) -> None:
    case_store_module.configure_case_repository(
        CaseRepository(LocalJsonCaseStore(tmp_path / "cases.json"))
    )
    case_store_module.reset_case_store()


def _create_case() -> str:
    case = case_store_module.create_case(
        AnalysisCaseCreateRequest(
            keyword="Current launch",
            title="Current launch",
            platforms=["youtube"],
        )
    )
    return case.case_id


def _item(index: int, *, body_text: str | None = None) -> SearchDiscoveryDiscussionItem:
    comment_id = f"comment_{index:03d}"
    return SearchDiscoveryDiscussionItem(
        discussion_id=f"youtube_official_api_{VIDEO_ID}_{comment_id}",
        video_id=VIDEO_ID,
        comment_id=comment_id,
        body_text=body_text or f"Public provider comment {index}",
        published_at=f"2026-09-{index + 1:02d}T00:00:00Z",
        like_count=index + 2,
        reply_count=index,
        source_url=f"https://www.youtube.com/watch?v={VIDEO_ID}&lc={comment_id}",
        safety_notes=[
            "Author identity omitted",
            "Reply content not acquired",
        ],
    )


def _batch(count: int = 3) -> SearchDiscoveryDiscussionBatch:
    items = [_item(index) for index in range(count)]
    safe_hash = (
        search_discovery_service_module.calculate_youtube_public_discussion_review_batch_safe_hash(
            VIDEO_ID,
            items,
        )
    )
    return SearchDiscoveryDiscussionBatch(
        video_id=VIDEO_ID,
        item_count=len(items),
        items=items,
        review_batch_safe_hash=safe_hash,
    )


def _payload(
    batch: SearchDiscoveryDiscussionBatch,
    selected_ids: list[str] | None = None,
) -> YouTubeReviewedPublicDiscussionAttachRequest:
    return YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash=batch.review_batch_safe_hash,
        selected_discussion_ids=selected_ids or [batch.items[0].discussion_id],
    )


def _track_saves(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    repository = case_store_module.get_case_repository()
    original_save = repository.save_case_evidence
    calls: list[dict[str, Any]] = []

    def tracked_save(*args: Any, **kwargs: Any):
        calls.append({"args": args, "kwargs": kwargs})
        return original_save(*args, **kwargs)

    monkeypatch.setattr(repository, "save_case_evidence", tracked_save)
    return calls


def _attach(
    case_id: str,
    batch: SearchDiscoveryDiscussionBatch,
    loader: Callable[..., SearchDiscoveryDiscussionBatch],
    selected_ids: list[str] | None = None,
):
    return case_store_module.attach_youtube_reviewed_public_discussion(
        case_id,
        VIDEO_ID,
        _payload(batch, selected_ids),
        discussion_loader=loader,
    )


def test_attach_gate_disabled_stops_before_provider_and_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENABLE_FLAG, raising=False)
    case_id = _create_case()
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(
        search_discovery_service_module.YouTubeReviewedPublicDiscussionAttachDisabledError
    ):
        _attach(case_id, batch, loader)

    assert loader.call_count == 0
    assert save_calls == []


def test_missing_case_stops_before_gate_provider_and_write(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(ENABLE_FLAG, raising=False)
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)

    result = _attach("case_missing", batch, loader)

    assert result is None
    assert loader.call_count == 0
    assert save_calls == []


def test_invalid_hash_is_rejected_by_schema_before_provider_or_write() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="ABC",
            selected_discussion_ids=["discussion_001"],
        )


def test_duplicate_selected_discussion_ids_are_rejected() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=["discussion_001", "discussion_001"],
        )


def test_more_than_three_selected_discussion_ids_are_rejected() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=[
                "discussion_001",
                "discussion_002",
                "discussion_003",
                "discussion_004",
            ],
        )


def test_request_forbids_browser_comment_text_and_other_extra_fields() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest.model_validate(
            {
                "review_batch_safe_hash": "a" * 64,
                "selected_discussion_ids": ["discussion_001"],
                "body_text": "Browser text must not be authoritative",
            }
        )


def test_fresh_hash_mismatch_performs_one_refetch_and_zero_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)
    stale_payload = YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash="0" * 64,
        selected_discussion_ids=[batch.items[0].discussion_id],
    )

    with pytest.raises(
        case_store_module.YouTubeReviewedPublicDiscussionBatchMismatchError
    ):
        case_store_module.attach_youtube_reviewed_public_discussion(
            case_id,
            VIDEO_ID,
            stale_payload,
            discussion_loader=loader,
        )

    assert loader.call_count == 1
    assert loader.max_items == [3]
    assert save_calls == []


def test_selected_id_missing_from_refetch_performs_zero_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(
        case_store_module.YouTubeReviewedPublicDiscussionSelectionError
    ):
        _attach(case_id, batch, loader, ["youtube_official_api_missing_comment"])

    assert loader.call_count == 1
    assert save_calls == []


@pytest.mark.parametrize(
    "failure_type",
    [YouTubeAuthError, YouTubeNetworkError, YouTubeQuotaError, YouTubeParsingError],
)
def test_provider_failure_propagates_with_one_call_zero_writes_and_no_fallback(
    monkeypatch: pytest.MonkeyPatch,
    failure_type: type[Exception],
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch()
    failure = failure_type("synthetic_provider_failure")
    loader = FakeDiscussionLoader(batch, failure=failure)
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(failure_type) as captured:
        _attach(case_id, batch, loader)

    assert captured.value is failure
    assert loader.call_count == 1
    assert loader.max_items == [3]
    assert save_calls == []


def test_one_selected_comment_attaches_with_one_provider_call_and_one_save(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)

    result = _attach(case_id, batch, loader)

    assert result is not None
    assert result.attached_discussion_count == 1
    assert result.evidence_result.evidence_item_count == 1
    assert len(result.attached_evidence_items) == 1
    assert loader.call_count == 1
    assert loader.video_ids == [VIDEO_ID]
    assert loader.max_items == [3]
    assert len(save_calls) == 1
    assert result.safe_mode == EXPECTED_SAFE_MODE
    saved_case = case_store_module.get_case(case_id)
    assert saved_case is not None
    assert saved_case.evidence_ingestion_jobs[0].safe_metadata["provider_request_count"] == 1
    assert saved_case.evidence_ingestion_jobs[0].safe_mode["real_api_calls"] is True


def test_three_selected_comments_map_and_persist_in_one_save(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch()
    loader = FakeDiscussionLoader(batch)
    save_calls = _track_saves(monkeypatch)
    selected_ids = [item.discussion_id for item in batch.items]

    result = _attach(case_id, batch, loader, selected_ids)

    assert result is not None
    assert result.attached_discussion_count == 3
    assert result.evidence_result.evidence_item_count == 3
    assert len(result.attached_evidence_items) == 3
    assert loader.call_count == 1
    assert len(save_calls) == 1


def test_attached_evidence_omits_author_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    result = _attach(_create_case(), _batch(), FakeDiscussionLoader(_batch()))

    assert result is not None
    item = result.attached_evidence_items[0]
    assert item.author_id is None
    assert item.author_name is None
    assert item.raw_data_safe["author_identity_omitted"] is True


def test_attached_evidence_omits_raw_provider_response_and_secrets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    batch = _batch()
    result = _attach(_create_case(), batch, FakeDiscussionLoader(batch))

    assert result is not None
    serialized = str(result.model_dump(mode="json")).lower()
    assert "raw_provider_response" not in serialized
    assert "api_key" not in serialized
    assert "credential" not in serialized
    assert "author_name" in serialized
    assert result.attached_evidence_items[0].author_name is None


def test_attached_evidence_has_exact_official_public_provenance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    batch = _batch()
    result = _attach(_create_case(), batch, FakeDiscussionLoader(batch))

    assert result is not None
    item = result.attached_evidence_items[0]
    assert item.platform == "youtube"
    assert item.source_type == "youtube"
    assert item.acquisition_mode == "official_api_public"
    assert item.provenance_type == "official_api"
    assert item.verification_status == "verified_by_official_api"
    assert item.source_capture_method == "official_api"
    assert item.content_visibility == "public"
    assert item.access_scope == "public"
    assert item.root_id == VIDEO_ID


def test_duplicate_attach_does_not_create_a_second_analysis_weight(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    batch = _batch(1)

    first = _attach(case_id, batch, FakeDiscussionLoader(batch))
    second = _attach(case_id, batch, FakeDiscussionLoader(batch))

    assert first is not None and second is not None
    assert first.evidence_result.evidence_item_count == 1
    assert second.evidence_result.evidence_item_count == 1
    case = case_store_module.get_case(case_id)
    assert case is not None
    eligible = analysis_eligible_evidence_items(case.evidence_items)
    assert len(eligible) == 1
    assert eligible[0].duplicate_count == 2


def test_attach_never_calls_analysis_or_report_builders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    counters = {"analysis": 0, "report": 0}

    def forbidden_analysis(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["analysis"] += 1
        raise AssertionError("analysis must remain a separate action")

    def forbidden_report(*args: object, **kwargs: object) -> None:
        del args, kwargs
        counters["report"] += 1
        raise AssertionError("report generation must remain a separate action")

    monkeypatch.setattr(case_store_module, "run_case", forbidden_analysis)
    monkeypatch.setattr(
        case_store_module,
        "build_public_opinion_report",
        forbidden_report,
    )
    batch = _batch()

    result = _attach(_create_case(), batch, FakeDiscussionLoader(batch))

    assert result is not None
    assert counters == {"analysis": 0, "report": 0}
    assert result.safe_mode["analysis_run"] is False
    assert result.safe_mode["report_triggered"] is False


def test_batch_safe_hash_is_deterministic_ordered_and_content_sensitive() -> None:
    first = [_item(0), _item(1)]
    second = [_item(0), _item(1)]
    calculate = (
        search_discovery_service_module.calculate_youtube_public_discussion_review_batch_safe_hash
    )

    assert calculate(VIDEO_ID, first) == calculate(VIDEO_ID, second)
    assert calculate(VIDEO_ID, first) != calculate(VIDEO_ID, list(reversed(second)))
    changed = [second[0].model_copy(update={"body_text": "Changed provider text"}), second[1]]
    assert calculate(VIDEO_ID, first) != calculate(VIDEO_ID, changed)


def test_hidden_route_is_registered_once_with_exact_identity() -> None:
    from app.api.v1.routes.cases import router

    target = (
        "/{case_id}/search-discovery/youtube-official-api/"
        "live-public-discussion/{video_id}/attach-reviewed"
    )
    routes = [
        route
        for route in router.routes
        if getattr(route, "path", None) == target
        and "POST" in getattr(route, "methods", set())
    ]

    assert len(routes) == 1
    assert routes[0].include_in_schema is False
