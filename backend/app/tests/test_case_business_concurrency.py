"""Synthetic, event-controlled case-document CAS interleavings.

These tests do not assert currentness for Markdown or monitoring auxiliaries;
their lineage is a separate F1R5 concern.
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Event, current_thread

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.case import AnalysisCaseCreateRequest, AnalysisCaseDetail
from app.schemas.crawl import CrawlStartResponse
from app.schemas.evidence import (
    EvidenceImportCommitRequest, EvidenceIngestionBatch, EvidenceReviewDecisionRequest,
)
from app.schemas.search_discovery import (
    SearchDiscoveryCandidate, SearchDiscoveryCandidateAttachRequest,
    SearchDiscoveryDiscussionBatch, SearchDiscoveryDiscussionItem,
    YouTubeReviewedPublicDiscussionAttachRequest,
)
from app.schemas.scheduler import MonitoringScheduleConfig
from app.services import case_store
from app.services.monitoring import scheduler_service
from app.services.storage.base_store import CaseRevisionConflict
from app.services.storage.local_json_store import LocalJsonCaseStore


def _repository(tmp_path) -> CaseRepository:
    repository = CaseRepository(LocalJsonCaseStore(tmp_path / "synthetic-cases.json"))
    case_store.configure_case_repository(repository)
    return repository


def _case_with_evidence(repository: CaseRepository) -> AnalysisCaseDetail:
    case = repository.create_case(
        AnalysisCaseCreateRequest(keyword="synthetic event", platforms=["public_web"])
    )
    attached = case_store.attach_case_evidence(
        case.case_id,
        EvidenceIngestionBatch.model_validate({
            "evidence_items": [{
                "evidence_type": "comment",
                "comment_text": "Synthetic public comment for a case CAS test.",
            }],
        }),
    )
    assert attached is not None and attached.evidence_items
    current = repository.get_case(case.case_id)
    assert current is not None
    return current


def _review(case: AnalysisCaseDetail) -> object:
    return case_store.review_case_evidence_item(
        case.case_id,
        case.evidence_items[0].evidence_id,
        EvidenceReviewDecisionRequest(decision="reject"),
    )


def _attach(case_id: str) -> object:
    return case_store.attach_case_evidence(
        case_id,
        EvidenceIngestionBatch.model_validate({
            "evidence_items": [{
                "evidence_type": "comment",
                "comment_text": "A second synthetic public comment wins CAS.",
            }],
        }),
    )


def _blocked_analysis_compute(monkeypatch, entered: Event, release: Event) -> None:
    original = case_store.build_pipeline_from_evidence_items

    def blocked(*args, **kwargs):
        entered.set()
        assert release.wait(10), "analysis event release timed out"
        return original(*args, **kwargs)

    monkeypatch.setattr(case_store, "build_pipeline_from_evidence_items", blocked)


def _blocked_review_cas(monkeypatch, repository: CaseRepository, entered: Event, release: Event) -> None:
    original = repository.replace_case_if_revision_matches

    def blocked(candidate, expected_revision):
        if current_thread().name.startswith("review-worker"):
            entered.set()
            assert release.wait(10), "review event release timed out"
        return original(candidate, expected_revision)

    monkeypatch.setattr(repository, "replace_case_if_revision_matches", blocked)


def _future_conflict(future: Future) -> CaseRevisionConflict:
    with pytest.raises(CaseRevisionConflict) as error:
        future.result(timeout=20)
    return error.value


def _assert_invalidated(case: AnalysisCaseDetail) -> None:
    assert case.status == "draft"
    assert case.analysis_revision is None
    assert case.analysis_run_id is None
    assert case.analysis_result is None
    assert case.visualization_data is None
    assert case.report is None
    assert case.markdown_available is False
    assert case.analysis_input_source is None
    assert case.risk_score is None
    assert case.risk_level is None
    assert case.risk_model_version is None


def test_review_wins_during_analysis_compute_and_losing_run_publishes_nothing(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    entered, release = Event(), Event()
    _blocked_analysis_compute(monkeypatch, entered, release)

    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(case_store.run_case, case.case_id)
        assert entered.wait(10)
        running = repository.get_case(case.case_id)
        assert running is not None and running.status == "running"
        assert running.analysis_run_id
        review = _review(case)
        assert review is not None
        release.set()
        conflict = _future_conflict(future)

    winner = repository.get_case(case.case_id)
    assert winner is not None
    assert conflict.expected_revision == running.case_revision
    assert len(winner.evidence_items[0].review_history) == 1
    _assert_invalidated(winner)
    assert repository.get_markdown_report(case.case_id) is None
    assert repository.list_analysis_snapshots(case.case_id) == []


def test_evidence_attach_wins_during_analysis_compute_and_is_not_lost(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    entered, release = Event(), Event()
    _blocked_analysis_compute(monkeypatch, entered, release)

    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(case_store.run_case, case.case_id)
        assert entered.wait(10)
        running = repository.get_case(case.case_id)
        assert running is not None
        attached = _attach(case.case_id)
        assert attached is not None
        release.set()
        _future_conflict(future)

    winner = repository.get_case(case.case_id)
    assert winner is not None
    _assert_invalidated(winner)
    assert len(winner.evidence_items) == 2
    assert repository.get_markdown_report(case.case_id) is None
    assert repository.list_analysis_snapshots(case.case_id) == []


def test_review_and_attach_share_start_revision_one_wins_no_retry(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    entered, release = Event(), Event()
    _blocked_review_cas(monkeypatch, repository, entered, release)

    with ThreadPoolExecutor(max_workers=1, thread_name_prefix="review-worker") as pool:
        future = pool.submit(_review, case)
        assert entered.wait(10)
        attached = _attach(case.case_id)
        assert attached is not None
        release.set()
        conflict = _future_conflict(future)

    winner = repository.get_case(case.case_id)
    assert winner is not None
    assert conflict.expected_revision == case.case_revision
    assert winner.case_revision == case.case_revision + 1
    assert len(winner.evidence_items) == 2
    assert winner.evidence_items[0].review_history == []


def test_review_and_config_share_start_revision_one_wins_no_overwrite(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    entered, release = Event(), Event()
    _blocked_review_cas(monkeypatch, repository, entered, release)

    with ThreadPoolExecutor(max_workers=1, thread_name_prefix="review-worker") as pool:
        future = pool.submit(_review, case)
        assert entered.wait(10)
        config = scheduler_service.update_case_monitoring_config(
            case.case_id, MonitoringScheduleConfig(enabled=True, interval_minutes=15)
        )
        assert config is not None and config.enabled
        release.set()
        _future_conflict(future)

    winner = repository.get_case(case.case_id)
    assert winner is not None
    assert winner.case_revision == case.case_revision + 1
    assert winner.monitoring_config.enabled is True
    assert winner.monitoring_config.interval_minutes == 15
    assert winner.evidence_items[0].review_history == []


def test_config_wins_during_analysis_and_same_run_abort_preserves_config(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    entered, release = Event(), Event()
    _blocked_analysis_compute(monkeypatch, entered, release)

    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(case_store.run_case, case.case_id)
        assert entered.wait(10)
        running = repository.get_case(case.case_id)
        assert running is not None and running.status == "running"
        updated = scheduler_service.update_case_monitoring_config(
            case.case_id, MonitoringScheduleConfig(enabled=True, interval_minutes=20)
        )
        assert updated is not None and updated.enabled
        during = repository.get_case(case.case_id)
        assert during is not None and during.status == "running"
        assert during.analysis_run_id == running.analysis_run_id
        release.set()
        _future_conflict(future)

    final = repository.get_case(case.case_id)
    assert final is not None
    assert final.case_revision == case.case_revision + 3
    assert final.monitoring_config.enabled is True
    assert final.monitoring_config.interval_minutes == 20
    _assert_invalidated(final)
    assert repository.get_markdown_report(case.case_id) is None
    assert repository.list_analysis_snapshots(case.case_id) == []


def test_scheduler_last_run_loses_to_disable_and_counts_conflict(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    completed = case_store.run_case(case.case_id)
    assert completed is not None
    enabled = scheduler_service.enable_case_monitoring(case.case_id)
    assert enabled is not None and enabled.enabled
    entered, release = Event(), Event()
    original = scheduler_service._mark_case_schedule_ran

    def blocked(repo, selected_case, last_run_at):
        entered.set()
        assert release.wait(10), "scheduler event release timed out"
        return original(repo, selected_case, last_run_at)

    monkeypatch.setattr(scheduler_service, "_mark_case_schedule_ran", blocked)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(scheduler_service.run_due_monitoring_jobs)
        assert entered.wait(10)
        disabled = scheduler_service.disable_case_monitoring(case.case_id)
        assert disabled is not None and disabled.enabled is False
        release.set()
        result = future.result(timeout=20)

    final = repository.get_case(case.case_id)
    assert final is not None
    assert final.monitoring_config.enabled is False
    assert final.monitoring_config.next_run_at is None
    assert result.conflict_case_count == 1
    assert result.executed_case_count == 1


def test_first_run_revision_and_later_config_revision_are_distinct(tmp_path) -> None:
    repository = _repository(tmp_path)
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="synthetic event"))
    assert case.case_revision == 0
    assert case.analysis_revision is None and case.analysis_run_id is None
    completed = case_store.run_case(case.case_id)
    assert completed is not None
    assert completed.status == "completed"
    assert completed.case_revision == 2
    assert completed.analysis_revision == 2
    assert completed.analysis_run_id
    assert completed.analysis_result is not None and completed.report is not None
    updated = scheduler_service.enable_case_monitoring(case.case_id)
    assert updated is not None
    later = repository.get_case(case.case_id)
    assert later is not None
    assert later.case_revision == 3
    assert later.analysis_revision == 2
    assert later.analysis_run_id == completed.analysis_run_id
    assert later.analysis_result is not None and later.report is not None


def test_legacy_case_load_does_not_fabricate_analysis_lineage() -> None:
    legacy = AnalysisCaseDetail.model_validate({
        "case_id": "case_old", "project_id": "project_old", "title": "Old",
        "keyword": "old", "status": "completed",
        "created_at": datetime(2026, 5, 14, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 5, 14, tzinfo=timezone.utc),
    })
    assert legacy.case_revision == 0
    assert legacy.analysis_revision is None
    assert legacy.analysis_run_id is None


def test_case_revision_conflict_is_safe_http_409(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = repository.create_case(AnalysisCaseCreateRequest(keyword="synthetic event"))

    def conflict(candidate, expected_revision):
        raise CaseRevisionConflict(case.case_id, expected_revision, expected_revision + 1)

    monkeypatch.setattr(repository, "replace_case_if_revision_matches", conflict)
    response = TestClient(app).post(f"/api/v1/cases/{case.case_id}/run")
    assert response.status_code == 409
    assert response.json() == {"detail": {
        "error": "case_revision_conflict",
        "case_id": case.case_id,
        "expected_revision": 0,
        "current_revision": 1,
    }}


@pytest.mark.parametrize("writer", [
    "review", "raw_crawl", "manual_attach", "search_attach", "youtube_attach", "import_commit",
])
def test_each_input_writer_invalidates_in_its_single_winning_cas(tmp_path, monkeypatch, writer) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    analyzed = case_store.run_case(case.case_id)
    assert analyzed is not None and analyzed.analysis_revision == analyzed.case_revision
    prior_snapshots = repository.list_analysis_snapshots(case.case_id)
    prior_markdown = repository.get_markdown_report(case.case_id)
    assert prior_snapshots and prior_markdown is not None

    if writer == "review":
        result = _review(analyzed)
    elif writer == "raw_crawl":
        monkeypatch.setattr(case_store, "start_crawl_with_adapters", lambda request: CrawlStartResponse(
            project_id=analyzed.project_id, crawl_task_id="synthetic_crawl",
            status="completed", message="synthetic empty crawl",
        ))
        result = case_store.run_case_crawl(case.case_id)
    elif writer == "manual_attach":
        result = _attach(case.case_id)
    elif writer == "search_attach":
        result = case_store.attach_search_discovery_candidates(
            case.case_id,
            SearchDiscoveryCandidateAttachRequest(candidates=[SearchDiscoveryCandidate(
                candidate_id="synthetic_search_1", query="synthetic event", provider="mock_static",
                title="Synthetic public result", snippet="Synthetic snippet", url="https://example.test/synthetic",
                status="accepted",
            )]),
        )
    elif writer == "youtube_attach":
        monkeypatch.setenv(
            "SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_REVIEWED_EVIDENCE_ATTACH_ENABLED", "1"
        )
        video_id = "AbC-d_EfG12"
        item = SearchDiscoveryDiscussionItem(
            discussion_id="youtube_official_api_AbC-d_EfG12_comment_001",
            video_id=video_id, comment_id="comment_001",
            body_text="Synthetic provider-free public comment",
            source_url="https://www.youtube.com/watch?v=AbC-d_EfG12&lc=comment_001",
        )
        safe_hash = case_store.calculate_youtube_public_discussion_review_batch_safe_hash(video_id, [item])
        batch = SearchDiscoveryDiscussionBatch(
            video_id=video_id, item_count=1, items=[item], review_batch_safe_hash=safe_hash
        )
        result = case_store.attach_youtube_reviewed_public_discussion(
            case.case_id, video_id,
            YouTubeReviewedPublicDiscussionAttachRequest(
                review_batch_safe_hash=safe_hash, selected_discussion_ids=[item.discussion_id]
            ),
            discussion_loader=lambda requested_video_id, *, max_items: batch,
        )
    else:
        result = case_store.commit_case_evidence_import(
            case.case_id,
            EvidenceImportCommitRequest(
                filename="synthetic.csv",
                content_text=(
                    "platform,source_type,acquisition_mode,evidence_type,comment_text,url,user_attestation\n"
                    "uploaded_dataset,uploaded_dataset,user_upload,comment,Synthetic import comment,https://example.test/import,true\n"
                ),
            ),
        )

    assert result is not None
    winner = repository.get_case(case.case_id)
    assert winner is not None
    assert winner.case_revision == analyzed.case_revision + 1
    _assert_invalidated(winner)
    assert repository.list_analysis_snapshots(case.case_id) == prior_snapshots
    assert repository.get_markdown_report(case.case_id) == prior_markdown
    if writer == "review":
        assert len(winner.evidence_items[0].review_history) == 1


def test_start_cas_conflict_does_not_compute_or_publish(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)

    def conflict(candidate, expected_revision):
        raise CaseRevisionConflict(case.case_id, expected_revision, expected_revision + 1)

    def no_compute(*args, **kwargs):
        raise AssertionError("start CAS loser must not compute")

    monkeypatch.setattr(repository, "replace_case_if_revision_matches", conflict)
    monkeypatch.setattr(case_store, "build_pipeline_from_evidence_items", no_compute)
    with pytest.raises(CaseRevisionConflict):
        case_store.run_case(case.case_id)
    assert repository.get_markdown_report(case.case_id) is None
    assert repository.list_analysis_snapshots(case.case_id) == []


def test_raw_adapter_called_once_and_original_revision_conflicts(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    calls = 0

    def synthetic_adapter(request):
        nonlocal calls
        calls += 1
        scheduler_service.enable_case_monitoring(case.case_id)
        return CrawlStartResponse(
            project_id=case.project_id, crawl_task_id="synthetic_crawl",
            status="completed", message="synthetic empty crawl",
        )

    monkeypatch.setattr(case_store, "start_crawl_with_adapters", synthetic_adapter)
    with pytest.raises(CaseRevisionConflict) as error:
        case_store.run_case_crawl(case.case_id)
    assert error.value.expected_revision == case.case_revision
    assert calls == 1
    winner = repository.get_case(case.case_id)
    assert winner is not None and winner.monitoring_config.enabled
    assert winner.raw_data_status == case.raw_data_status
    assert winner.evidence_items == case.evidence_items


def test_youtube_mock_loader_called_once_and_original_revision_conflicts(tmp_path, monkeypatch) -> None:
    repository = _repository(tmp_path)
    case = _case_with_evidence(repository)
    monkeypatch.setenv(
        "SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_REVIEWED_EVIDENCE_ATTACH_ENABLED", "1"
    )
    video_id = "AbC-d_EfG12"
    item = SearchDiscoveryDiscussionItem(
        discussion_id="youtube_official_api_AbC-d_EfG12_comment_001",
        video_id=video_id, comment_id="comment_001",
        body_text="Synthetic provider-free public comment",
        source_url="https://www.youtube.com/watch?v=AbC-d_EfG12&lc=comment_001",
    )
    safe_hash = case_store.calculate_youtube_public_discussion_review_batch_safe_hash(video_id, [item])
    batch = SearchDiscoveryDiscussionBatch(
        video_id=video_id, item_count=1, items=[item], review_batch_safe_hash=safe_hash
    )
    calls = 0

    def synthetic_loader(requested_video_id, *, max_items):
        nonlocal calls
        calls += 1
        scheduler_service.enable_case_monitoring(case.case_id)
        return batch

    with pytest.raises(CaseRevisionConflict) as error:
        case_store.attach_youtube_reviewed_public_discussion(
            case.case_id, video_id,
            YouTubeReviewedPublicDiscussionAttachRequest(
                review_batch_safe_hash=safe_hash, selected_discussion_ids=[item.discussion_id]
            ),
            discussion_loader=synthetic_loader,
        )
    assert error.value.expected_revision == case.case_revision
    assert calls == 1
    winner = repository.get_case(case.case_id)
    assert winner is not None and winner.monitoring_config.enabled
    assert winner.evidence_items == case.evidence_items
