from __future__ import annotations

from collections.abc import Callable
import hashlib
import json
from typing import Any

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

import app.api.v1.routes.cases as cases_route_module
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


def _batch_from_items(
    items: list[SearchDiscoveryDiscussionItem],
) -> SearchDiscoveryDiscussionBatch:
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
        review_item_safe_hashes={
            item.discussion_id: (
                search_discovery_service_module.calculate_youtube_public_discussion_selected_item_safe_hash(
                    VIDEO_ID,
                    item,
                )
            )
            for item in items
        },
    )


def _batch(count: int = 3) -> SearchDiscoveryDiscussionBatch:
    return _batch_from_items([_item(index) for index in range(count)])


def _payload(
    batch: SearchDiscoveryDiscussionBatch,
    selected_ids: list[str] | None = None,
) -> YouTubeReviewedPublicDiscussionAttachRequest:
    return YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash=batch.review_batch_safe_hash,
        selected_discussion_ids=selected_ids or [batch.items[0].discussion_id],
    )


def _selected_payload(
    reviewed_batch: SearchDiscoveryDiscussionBatch,
    selected_ids: list[str] | None = None,
) -> YouTubeReviewedPublicDiscussionAttachRequest:
    selected_discussion_ids = (
        selected_ids
        if selected_ids is not None
        else [reviewed_batch.items[0].discussion_id]
    )
    reviewed_items = {
        item.discussion_id: item
        for item in reviewed_batch.items
    }
    return YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash=reviewed_batch.review_batch_safe_hash,
        selected_discussion_ids=selected_discussion_ids,
        review_binding_mode="selected_item_v1",
        selected_discussion_safe_hashes={
            discussion_id: (
                search_discovery_service_module.calculate_youtube_public_discussion_selected_item_safe_hash(
                    VIDEO_ID,
                    reviewed_items[discussion_id],
                )
            )
            for discussion_id in selected_discussion_ids
        },
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


def _attach_selected(
    case_id: str,
    reviewed_batch: SearchDiscoveryDiscussionBatch,
    fresh_batch: SearchDiscoveryDiscussionBatch,
    selected_ids: list[str] | None = None,
):
    return case_store_module.attach_youtube_reviewed_public_discussion(
        case_id,
        VIDEO_ID,
        _selected_payload(reviewed_batch, selected_ids),
        discussion_loader=FakeDiscussionLoader(fresh_batch),
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


def test_batch_v1_rejects_nonempty_selected_hash_map() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=["discussion_001"],
            selected_discussion_safe_hashes={"discussion_001": "b" * 64},
        )


def test_selected_item_v1_requires_selected_hash_map() -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=["discussion_001"],
            review_binding_mode="selected_item_v1",
        )


@pytest.mark.parametrize(
    "selected_hashes",
    [
        {
            "discussion_001": "b" * 64,
            "discussion_extra": "c" * 64,
        },
        {"discussion_extra": "b" * 64},
    ],
)
def test_selected_item_v1_hash_keys_must_exactly_match_selected_ids(
    selected_hashes: dict[str, str],
) -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=["discussion_001"],
            review_binding_mode="selected_item_v1",
            selected_discussion_safe_hashes=selected_hashes,
        )


@pytest.mark.parametrize("invalid_hash", ["A" * 64, "g" * 64, "a" * 63])
def test_selected_item_v1_rejects_invalid_selected_hash(invalid_hash: str) -> None:
    with pytest.raises(ValidationError):
        YouTubeReviewedPublicDiscussionAttachRequest(
            review_batch_safe_hash="a" * 64,
            selected_discussion_ids=["discussion_001"],
            review_binding_mode="selected_item_v1",
            selected_discussion_safe_hashes={"discussion_001": invalid_hash},
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


def test_selected_item_hash_uses_exact_canonical_payload_and_is_deterministic() -> None:
    item = _item(0)
    calculate = (
        search_discovery_service_module.calculate_youtube_public_discussion_selected_item_safe_hash
    )
    canonical_payload = {
        "schema": (
            "sentigraph.youtube.reviewed_public_discussion."
            "selected_item_binding.v1"
        ),
        "video_id": VIDEO_ID,
        "discussion_id": item.discussion_id,
        "body_text": item.body_text,
        "published_at": item.published_at,
    }
    expected = hashlib.sha256(
        json.dumps(
            canonical_payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()

    assert calculate(VIDEO_ID, item) == expected
    assert calculate(VIDEO_ID, item.model_copy(deep=True)) == expected


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        ("like_count", 999),
        ("reply_count", 999),
        ("source_url", "https://example.invalid/engagement-drift"),
    ],
)
def test_selected_item_hash_ignores_engagement_and_source_url_drift(
    field_name: str,
    changed_value: object,
) -> None:
    item = _item(0)
    calculate = (
        search_discovery_service_module.calculate_youtube_public_discussion_selected_item_safe_hash
    )

    assert calculate(VIDEO_ID, item) == calculate(
        VIDEO_ID,
        item.model_copy(update={field_name: changed_value}),
    )


def test_selected_item_hash_is_independent_of_batch_order() -> None:
    items = [_item(0), _item(1), _item(2)]
    selected_item = items[1]
    reversed_items = list(reversed(items))
    calculate = (
        search_discovery_service_module.calculate_youtube_public_discussion_selected_item_safe_hash
    )

    assert calculate(VIDEO_ID, selected_item) == calculate(
        VIDEO_ID,
        next(
            item
            for item in reversed_items
            if item.discussion_id == selected_item.discussion_id
        ),
    )


@pytest.mark.parametrize("unselected_drift", ["changed", "removed", "reordered"])
def test_selected_item_v1_allows_unselected_item_drift(
    monkeypatch: pytest.MonkeyPatch,
    unselected_drift: str,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    reviewed_batch = _batch(3)
    if unselected_drift == "changed":
        fresh_items = [
            reviewed_batch.items[0],
            reviewed_batch.items[1],
            reviewed_batch.items[2].model_copy(
                update={"body_text": "Changed unselected public text"}
            ),
        ]
    elif unselected_drift == "removed":
        fresh_items = reviewed_batch.items[:2]
    else:
        fresh_items = list(reversed(reviewed_batch.items))
    fresh_batch = _batch_from_items(fresh_items)

    result = _attach_selected(
        _create_case(),
        reviewed_batch,
        fresh_batch,
    )

    assert result is not None
    assert result.attached_discussion_count == 1
    assert result.reviewed_batch_safe_hash == reviewed_batch.review_batch_safe_hash
    assert result.fresh_batch_safe_hash == fresh_batch.review_batch_safe_hash
    assert result.reviewed_batch_safe_hash != result.fresh_batch_safe_hash


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        ("body_text", "Changed selected public text"),
        ("published_at", "2026-10-01T00:00:00Z"),
    ],
)
def test_selected_item_v1_selected_content_drift_fails_closed_with_zero_writes(
    monkeypatch: pytest.MonkeyPatch,
    field_name: str,
    changed_value: str,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    case_id = _create_case()
    reviewed_batch = _batch(3)
    fresh_items = [
        reviewed_batch.items[0].model_copy(update={field_name: changed_value}),
        *reviewed_batch.items[1:],
    ]
    loader = FakeDiscussionLoader(_batch_from_items(fresh_items))
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(
        case_store_module.YouTubeReviewedPublicDiscussionSelectedBindingMismatchError
    ) as captured:
        case_store_module.attach_youtube_reviewed_public_discussion(
            case_id,
            VIDEO_ID,
            _selected_payload(reviewed_batch),
            discussion_loader=loader,
        )

    assert str(captured.value) == (
        "youtube_reviewed_public_discussion_selected_binding_mismatch"
    )
    assert loader.call_count == 1
    assert save_calls == []


def test_selected_item_v1_missing_selected_id_still_raises_selection_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    reviewed_batch = _batch(3)
    missing_id = "youtube_official_api_missing_comment"
    payload = YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash=reviewed_batch.review_batch_safe_hash,
        selected_discussion_ids=[missing_id],
        review_binding_mode="selected_item_v1",
        selected_discussion_safe_hashes={missing_id: "a" * 64},
    )
    loader = FakeDiscussionLoader(reviewed_batch)
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(case_store_module.YouTubeReviewedPublicDiscussionSelectionError):
        case_store_module.attach_youtube_reviewed_public_discussion(
            _create_case(),
            VIDEO_ID,
            payload,
            discussion_loader=loader,
        )

    assert loader.call_count == 1
    assert save_calls == []


def test_selected_item_v1_wrong_selected_hash_uses_distinct_error_and_zero_writes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(ENABLE_FLAG, "1")
    reviewed_batch = _batch(3)
    selected_id = reviewed_batch.items[0].discussion_id
    payload = YouTubeReviewedPublicDiscussionAttachRequest(
        review_batch_safe_hash=reviewed_batch.review_batch_safe_hash,
        selected_discussion_ids=[selected_id],
        review_binding_mode="selected_item_v1",
        selected_discussion_safe_hashes={selected_id: "0" * 64},
    )
    loader = FakeDiscussionLoader(reviewed_batch)
    save_calls = _track_saves(monkeypatch)

    with pytest.raises(
        case_store_module.YouTubeReviewedPublicDiscussionSelectedBindingMismatchError
    ):
        case_store_module.attach_youtube_reviewed_public_discussion(
            _create_case(),
            VIDEO_ID,
            payload,
            discussion_loader=loader,
        )

    assert loader.call_count == 1
    assert save_calls == []


def test_selected_item_v1_success_persists_exact_safe_binding_lineage(
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
    case_id = _create_case()
    reviewed_batch = _batch(3)
    selected_ids = [
        reviewed_batch.items[0].discussion_id,
        reviewed_batch.items[1].discussion_id,
    ]
    fresh_batch = _batch_from_items(
        [
            reviewed_batch.items[1],
            reviewed_batch.items[0],
            reviewed_batch.items[2].model_copy(
                update={
                    "body_text": "Changed unselected public text",
                    "like_count": 999,
                }
            ),
        ]
    )
    loader = FakeDiscussionLoader(fresh_batch)
    save_calls = _track_saves(monkeypatch)
    payload = _selected_payload(reviewed_batch, selected_ids)

    result = case_store_module.attach_youtube_reviewed_public_discussion(
        case_id,
        VIDEO_ID,
        payload,
        discussion_loader=loader,
    )

    assert result is not None
    assert loader.call_count == 1
    assert len(save_calls) == 1
    assert result.attached_discussion_count == 2
    assert result.evidence_result.evidence_item_count == 2
    assert len(result.attached_evidence_items) == 2
    assert result.review_binding_mode == "selected_item_v1"
    assert result.reviewed_batch_safe_hash == reviewed_batch.review_batch_safe_hash
    assert result.fresh_batch_safe_hash == fresh_batch.review_batch_safe_hash
    assert result.review_batch_safe_hash == result.fresh_batch_safe_hash
    assert result.reviewed_batch_safe_hash != result.fresh_batch_safe_hash
    assert result.selected_discussion_safe_hashes == (
        payload.selected_discussion_safe_hashes
    )
    assert counters == {"analysis": 0, "report": 0}

    attached_by_discussion_id = {
        item.raw_data_safe["discussion_id"]: item
        for item in result.attached_evidence_items
    }
    assert set(attached_by_discussion_id) == set(selected_ids)
    for discussion_id, item in attached_by_discussion_id.items():
        assert item.author_id is None
        assert item.author_name is None
        assert item.raw_data_safe["reply_content_acquired"] is False
        assert item.raw_data_safe["review_binding_mode"] == "selected_item_v1"
        assert item.raw_data_safe["reviewed_batch_safe_hash"] == (
            reviewed_batch.review_batch_safe_hash
        )
        assert item.raw_data_safe["fresh_batch_safe_hash"] == (
            fresh_batch.review_batch_safe_hash
        )
        assert item.raw_data_safe["selected_discussion_safe_hash"] == (
            payload.selected_discussion_safe_hashes[discussion_id]
        )

    saved_case = case_store_module.get_case(case_id)
    assert saved_case is not None
    metadata = saved_case.evidence_ingestion_jobs[0].safe_metadata
    assert metadata["review_binding_mode"] == "selected_item_v1"
    assert metadata["reviewed_batch_safe_hash"] == reviewed_batch.review_batch_safe_hash
    assert metadata["fresh_batch_safe_hash"] == fresh_batch.review_batch_safe_hash
    assert metadata["selected_discussion_safe_hashes"] == (
        payload.selected_discussion_safe_hashes
    )


def test_selected_binding_mismatch_maps_to_exact_http_409(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    reviewed_batch = _batch(1)

    def fail_with_selected_binding_mismatch(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise case_store_module.YouTubeReviewedPublicDiscussionSelectedBindingMismatchError(
            "youtube_reviewed_public_discussion_selected_binding_mismatch"
        )

    monkeypatch.setattr(
        cases_route_module,
        "attach_youtube_reviewed_public_discussion",
        fail_with_selected_binding_mismatch,
    )

    with pytest.raises(HTTPException) as captured:
        cases_route_module.attach_youtube_reviewed_public_discussion_to_case(
            "case_synthetic",
            VIDEO_ID,
            _selected_payload(reviewed_batch),
        )

    assert captured.value.status_code == 409
    assert captured.value.detail == (
        "youtube_reviewed_public_discussion_selected_binding_mismatch"
    )


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
