from pathlib import Path
import urllib.request

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.case_repository import CaseRepository
from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.evidence import EvidenceItem
from app.services.case_store import configure_case_repository, reset_case_store
from app.services.evidence_ingestion import (
    build_evidence_items_from_raw_data,
    raw_comment_to_evidence_item,
    raw_post_to_evidence_item,
)
from app.services.storage.local_json_store import LocalJsonCaseStore


client = TestClient(app)


@pytest.fixture(autouse=True)
def configure_temp_case_store(tmp_path) -> None:
    configure_case_repository(CaseRepository(LocalJsonCaseStore(tmp_path / "cases.json")))
    reset_case_store()


def test_youtube_raw_data_converts_to_evidence_items() -> None:
    post = _youtube_post()
    comment = _youtube_comment()
    metadata = PlatformCrawlMetadata(
        platform="youtube",
        adapter_mode="real",
        source_type="youtube_data_api_v3",
        fallback_used=False,
        credential_present=True,
    )

    post_item = raw_post_to_evidence_item(post, case_id="case_001", metadata=metadata)
    comment_item = raw_comment_to_evidence_item(comment, case_id="case_001", metadata=metadata)

    assert post_item.source_type == "youtube"
    assert post_item.acquisition_mode == "official_api_public"
    assert post_item.evidence_type == "video"
    assert comment_item.source_type == "youtube"
    assert comment_item.acquisition_mode == "official_api_public"
    assert comment_item.evidence_type == "comment"
    assert comment_item.comment_text == comment.content
    assert "api_key" not in str(post_item.raw_data_safe).lower()
    assert post_item.trust_label == "high"
    assert post_item.verification_status == "verified_by_official_api"
    assert post_item.provenance_type == "official_api"


def test_public_parser_article_converts_to_evidence_item() -> None:
    post = RawPost(
        platform="the_paper",
        post_id="paper_001",
        author_id="paper_author",
        author_name="The Paper",
        title="Public article title",
        content="Public article body about a product quality issue.",
        like_count=0,
        reply_count=0,
        share_count=0,
        created_at="2026-05-21T12:00:00Z",
        url="https://example.test/article",
        raw_data={"source_type": "public_page_parser", "mode": "public_parser_fixture"},
    )

    item = raw_post_to_evidence_item(post, case_id="case_001")

    assert item.source_type == "news_site"
    assert item.acquisition_mode == "public_parser"
    assert item.evidence_type == "article"
    assert item.body_text == post.content


def test_case_crawl_exposes_normalized_evidence_items(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])

    def fake_start_crawl(payload):
        return _crawl_response()

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)
    response = client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})

    assert response.status_code == 200
    body = response.json()
    assert body["raw_data_status"] == "attached"
    assert body["evidence_item_count"] == 2
    assert body["evidence_items"][0]["source_type"] == "youtube"
    assert body["evidence_items"][0]["acquisition_mode"] == "official_api_public"

    evidence_response = client.get(f"/api/v1/cases/{case_id}/evidence")
    assert evidence_response.status_code == 200
    evidence = evidence_response.json()
    assert evidence["status"] == "attached"
    assert evidence["source_distribution"] == {"youtube": 2}
    assert evidence["evidence_type_counts"]["video"] == 1
    assert evidence["evidence_type_counts"]["comment"] == 1


def test_manual_evidence_attach_is_sanitized_and_feeds_analysis() -> None:
    case_id = _create_case(platforms=["uploaded_dataset"])
    payload = {
        "source": {
            "platform": "uploaded_dataset",
            "source_type": "uploaded_dataset",
            "acquisition_mode": "user_upload",
            "source_name": "QA spreadsheet",
        },
        "evidence_items": [
            {
                "title": "Manual incident article",
                "body_text": "Users describe a delayed official response and product quality issue.",
                "raw_data_safe": {"api_key": "secret-marker-should-not-appear", "safe_field": "ok"},
            },
            {
                "evidence_type": "comment",
                "comment_text": "Manual evidence comment says the response timeline is still unclear.",
                "root_id": "manual_article",
                "raw_data_safe": {"access_token": "secret-marker-should-not-appear"},
            },
        ],
    }

    attach_response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert attach_response.status_code == 200
    assert "secret-marker-should-not-appear" not in attach_response.text
    attached = attach_response.json()
    assert attached["status"] == "attached"
    assert attached["evidence_item_count"] == 2
    assert attached["evidence_type_counts"]["article"] == 1
    assert attached["evidence_type_counts"]["comment"] == 1

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_input_source"] == "case_evidence_items"
    assert body["analysis_result"]["analysis_input_source"] == "case_evidence_items"
    assert body["analysis_result"]["evidence_item_count"] == 2
    assert body["report"]["generated_from_mock_pipeline"] is False
    assert body["report"]["evidence_source_distribution"] == {"uploaded_dataset": 2}
    assert any("Evidence layer normalized 2 item" in finding for finding in body["report"]["key_findings"])
    assert any("Manual evidence comment" in comment for comment in body["report"]["representative_comments"])
    assert "secret-marker-should-not-appear" not in run_response.text

    markdown_response = client.get(f"/api/v1/cases/{case_id}/report/markdown")
    assert markdown_response.status_code == 200
    assert "normalized case evidence offline deterministic analysis" in markdown_response.json()["markdown"]
    assert "attached case raw data offline deterministic analysis" not in markdown_response.json()["markdown"]


def test_manual_url_video_reply_and_metric_attach_are_supported() -> None:
    case_id = _create_case(platforms=["public_web"])
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
            "source_name": "Manual public URL evidence",
            "source_url": "https://example.test/video",
        },
        "evidence_items": [
            {
                "evidence_type": "video",
                "title": "Manual public video title",
                "body_text": "A public video description about delayed response.",
                "root_id": "manual_video_001",
                "url": "https://example.test/video",
            },
            {
                "evidence_type": "reply",
                "comment_text": "A reply says the official timeline is unclear.",
                "root_id": "manual_video_001",
                "parent_id": "manual_comment_001",
                "raw_data_safe": {"client_secret": "secret-marker-should-not-appear"},
            },
            {
                "evidence_type": "interaction_metric",
                "title": "Manual video interaction metrics",
                "root_id": "manual_video_001",
                "like_count": 23,
                "reply_count": 5,
                "view_count": 900,
            },
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 200
    assert "secret-marker-should-not-appear" not in response.text
    body = response.json()
    assert body["source_distribution"] == {"public_web": 3}
    assert body["evidence_type_counts"]["video"] == 1
    assert body["evidence_type_counts"]["reply"] == 1
    assert body["evidence_type_counts"]["interaction_metric"] == 1
    assert {item["acquisition_mode"] for item in body["evidence_items"]} == {"manual_url"}
    assert body["top_titles"][:2] == ["Manual public video title", "Manual video interaction metrics"]
    assert any("official timeline" in comment for comment in body["representative_comments"])


def test_manual_evidence_attach_appends_across_calls() -> None:
    case_id = _create_case(platforms=["public_web"])
    base_payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "First manual public comment for the case.",
            }
        ],
    }
    second_payload = {
        **base_payload,
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "Second manual public comment should append instead of replacing.",
            }
        ],
    }

    first_response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=base_payload)
    second_response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=second_payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    body = second_response.json()
    assert body["evidence_item_count"] == 2
    assert body["evidence_type_counts"] == {"comment": 2}
    assert body["evidence_items"][0]["evidence_id"] != body["evidence_items"][1]["evidence_id"]
    assert any("First manual public comment" in text for text in body["representative_comments"])
    assert any("Second manual public comment" in text for text in body["representative_comments"])


def test_manual_url_evidence_redacts_text_secrets_and_warns_on_invalid_metrics(monkeypatch) -> None:
    case_id = _create_case(platforms=["public_web"])

    def fail_urlopen(*args, **kwargs):
        raise AssertionError("Manual URL evidence attach must not fetch URLs.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)
    payload = {
        "source": {
            "platform": "",
            "source_type": "uploaded_dataset",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "Manual public comment includes access_token=secret-marker and should be sanitized.",
                "url": "https://example.invalid/should-not-be-fetched?api_key=secret-marker",
                "like_count": "not-a-number",
                "reply_count": "7",
            }
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 200
    assert "secret-marker" not in response.text
    body = response.json()
    assert body["source_distribution"] == {"public_web": 1}
    assert body["evidence_items"][0]["platform"] == "manual_url"
    assert body["evidence_items"][0]["source_type"] == "public_web"
    assert body["evidence_items"][0]["acquisition_mode"] == "manual_url"
    assert body["evidence_items"][0]["comment_text"].endswith("access_token=[REDACTED] and should be sanitized.")
    assert body["evidence_items"][0]["url"] == "https://example.invalid/should-not-be-fetched?api_key=[REDACTED]"
    assert body["evidence_items"][0]["like_count"] == 0
    assert body["evidence_items"][0]["reply_count"] == 7
    assert "invalid_numeric_metric:like_count" in body["warnings"]
    assert "secret_like_text_redacted:comment_text" in body["warnings"]
    assert "secret_like_text_redacted:url" in body["warnings"]


def test_manual_url_evidence_requires_reviewable_text() -> None:
    case_id = _create_case(platforms=["public_web"])
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "interaction_metric",
                "url": "https://example.test/metric-only",
                "like_count": 12,
            }
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"]["error"] == "evidence_attach_rejected"
    assert response.json()["detail"]["message"] == "manual_evidence_text_required"


def test_manual_url_with_attestation_gets_medium_unverified_trust() -> None:
    case_id = _create_case(platforms=["public_web"])
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "Manual public comment with a source URL and attestation.",
                "url": "https://example.test/source?utm_source=newsletter",
                "created_at": "2026-05-25T09:00:00Z",
                "user_attestation_text": "I confirm I have the right to submit this public-opinion evidence.",
            }
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 200
    item = response.json()["evidence_items"][0]
    assert item["trust_label"] == "medium"
    assert item["verification_status"] == "source_url_provided_unverified"
    assert item["source_url"] == "https://example.test/source"
    assert item["source_url_present"] is True


def test_screenshot_transcription_is_unverified_and_needs_review() -> None:
    case_id = _create_case(platforms=["public_web"])
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "Screenshot transcription says users are still waiting for evidence.",
                "source_capture_method": "screenshot_transcription",
                "provenance_type": "screenshot_transcription",
                "user_attestation_text": "I confirm lawful source.",
            }
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 200
    body = response.json()
    item = body["evidence_items"][0]
    assert item["trust_label"] == "unverified"
    assert item["verification_status"] == "screenshot_unverified"
    assert "screenshot_unverified" in item["risk_flags"]
    assert body["trust_summary"]["review_needed_count"] == 1


def test_duplicate_manual_evidence_is_collapsed_and_does_not_inflate_analysis() -> None:
    case_id = _create_case(platforms=["public_web"])
    duplicate_item = {
        "evidence_type": "comment",
        "comment_text": "Repeated public comment should be counted once for analysis.",
        "url": "https://example.test/thread?utm_campaign=tracking",
        "created_at": "2026-05-25T09:00:00Z",
        "user_attestation_text": "I confirm lawful source.",
    }
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [duplicate_item, duplicate_item],
    }

    attach_response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert attach_response.status_code == 200
    attached = attach_response.json()
    assert attached["evidence_item_count"] == 1
    assert attached["evidence_items"][0]["duplicate_count"] == 2
    assert attached["deduplication_summary"]["duplicate_items"] == 1

    dedup_response = client.get(f"/api/v1/cases/{case_id}/evidence/dedup-summary")
    assert dedup_response.status_code == 200
    assert dedup_response.json()["unique_items"] == 1
    assert dedup_response.json()["duplicate_items"] == 1

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_result"]["evidence_item_count"] == 1
    assert body["analysis_result"]["evidence_duplicate_item_count"] == 1
    assert body["report"]["evidence_item_count"] == 1
    assert body["report"]["evidence_duplicate_item_count"] == 1


def test_html_like_manual_input_is_plain_text_and_flagged() -> None:
    case_id = _create_case(platforms=["public_web"])
    payload = {
        "source": {
            "platform": "public_web",
            "source_type": "public_web",
            "acquisition_mode": "manual_url",
        },
        "evidence_items": [
            {
                "evidence_type": "comment",
                "comment_text": "<script>alert('x')</script> public concern remains unresolved.",
                "user_attestation_text": "I confirm lawful source.",
            }
        ],
    }

    response = client.post(f"/api/v1/cases/{case_id}/evidence/attach", json=payload)

    assert response.status_code == 200
    item = response.json()["evidence_items"][0]
    assert "<script>" in item["comment_text"]
    assert "raw_html_script_like_input" in item["risk_flags"]


def test_trust_summary_endpoint_reports_distributions() -> None:
    case_id = _create_case(platforms=["public_web"])
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "public_web",
                "source_type": "public_web",
                "acquisition_mode": "manual_url",
            },
            "evidence_items": [
                {
                    "evidence_type": "comment",
                    "comment_text": "Manual evidence without attestation needs review.",
                }
            ],
        },
    )
    assert response.status_code == 200

    summary_response = client.get(f"/api/v1/cases/{case_id}/evidence/trust-summary")

    assert summary_response.status_code == 200
    body = summary_response.json()
    assert body["trust_label_distribution"]["unverified"] == 1
    assert body["verification_status_distribution"]["needs_review"] == 1
    assert body["provenance_type_distribution"]["manual_url"] == 1
    assert body["warning_counts"]["user_attestation_missing"] == 1


def test_review_queue_lists_needs_review_screenshot_missing_source_and_duplicate_evidence() -> None:
    case_id = _create_case(platforms=["public_web"])
    duplicate_item = {
        "evidence_type": "comment",
        "comment_text": "Repeated complaint should collapse but still be review-visible.",
        "url": "https://example.test/thread?utm_source=tracking",
        "user_attestation_text": "I confirm lawful source.",
    }
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "public_web",
                "source_type": "public_web",
                "acquisition_mode": "manual_url",
            },
            "evidence_items": [
                {
                    "evidence_type": "comment",
                    "comment_text": "Screenshot transcription still needs source verification.",
                    "source_capture_method": "screenshot_transcription",
                    "provenance_type": "screenshot_transcription",
                },
                {
                    "evidence_type": "comment",
                    "comment_text": "Manual evidence without a URL should request source review.",
                    "user_attestation_text": "I confirm lawful source.",
                },
                duplicate_item,
                duplicate_item,
            ],
        },
    )
    assert response.status_code == 200

    queue_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-queue")

    assert queue_response.status_code == 200
    body = queue_response.json()
    assert body["queue_count"] == 3
    reason_codes = {code for item in body["queue_items"] for code in item["review_reason_codes"]}
    assert "provenance:screenshot_transcription" in reason_codes
    assert "source_url_missing" in reason_codes
    assert "duplicate_group" in reason_codes
    assert body["duplicate_group_count"] == 1
    assert body["safe_mode"]["real_ai_review"] is False


def test_official_api_high_trust_evidence_is_not_in_review_queue_unless_flagged(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])

    def fake_start_crawl(payload):
        return _crawl_response()

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)
    crawl_response = client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})
    assert crawl_response.status_code == 200

    queue_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-queue")

    assert queue_response.status_code == 200
    assert queue_response.json()["queue_count"] == 0


def test_review_decisions_update_status_and_analysis_excludes_rejected_evidence() -> None:
    case_id = _create_case(platforms=["public_web"])
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "public_web",
                "source_type": "public_web",
                "acquisition_mode": "manual_url",
            },
            "evidence_items": [
                {
                    "evidence_type": "comment",
                    "comment_text": "Approved evidence should remain in representative comments.",
                    "url": "https://example.test/approved",
                    "user_attestation_text": "I confirm lawful source.",
                },
                {
                    "evidence_type": "comment",
                    "comment_text": "Rejected evidence should not appear in representative comments.",
                    "url": "https://example.test/rejected",
                    "user_attestation_text": "I confirm lawful source.",
                },
                {
                    "evidence_type": "comment",
                    "comment_text": "Weak evidence remains usable but should stay warning-tagged.",
                    "user_attestation_text": "I confirm lawful source.",
                },
                {
                    "evidence_type": "comment",
                    "comment_text": "Evidence needs a better source URL before full confidence.",
                },
            ],
        },
    )
    assert response.status_code == 200
    items = response.json()["evidence_items"]
    ids_by_text = {item["comment_text"]: item["evidence_id"] for item in items}

    approve_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/{ids_by_text['Approved evidence should remain in representative comments.']}/review",
        json={"decision": "approve", "reviewer_label": "qa"},
    )
    reject_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/{ids_by_text['Rejected evidence should not appear in representative comments.']}/review",
        json={"decision": "reject", "notes": "Not relevant to this event."},
    )
    weak_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/{ids_by_text['Weak evidence remains usable but should stay warning-tagged.']}/review",
        json={"decision": "mark_weak"},
    )
    source_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/{ids_by_text['Evidence needs a better source URL before full confidence.']}/review",
        json={"decision": "request_more_source"},
    )

    assert approve_response.status_code == 200
    assert approve_response.json()["review_status"] == "approved"
    assert reject_response.status_code == 200
    assert reject_response.json()["review_status"] == "rejected"
    assert weak_response.status_code == 200
    assert weak_response.json()["review_status"] == "marked_weak"
    assert source_response.status_code == 200
    assert source_response.json()["review_status"] == "needs_more_source"

    summary_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["approved_count"] == 1
    assert summary["rejected_count"] == 1
    assert summary["marked_weak_count"] == 1
    assert summary["needs_more_source_count"] == 1

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    body = run_response.json()
    representative_comments = body["report"]["representative_comments"]
    assert body["analysis_input_source"] == "case_evidence_items"
    assert body["analysis_result"]["evidence_item_count"] == 3
    assert body["analysis_result"]["evidence_review_excluded_count"] == 1
    assert any("Approved evidence" in comment for comment in representative_comments)
    assert not any("Rejected evidence" in comment for comment in representative_comments)


def test_review_history_timeline_and_audit_summary_are_append_only() -> None:
    case_id = _create_case(platforms=["public_web"])
    comments_by_decision = {
        "approve": "History approve evidence.",
        "reject": "History reject evidence.",
        "mark_weak": "History weak evidence.",
        "request_more_source": "History source request evidence.",
        "merge_duplicate": "History duplicate merge evidence.",
        "reset_review": "History reset evidence.",
    }
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "public_web",
                "source_type": "public_web",
                "acquisition_mode": "manual_url",
            },
            "evidence_items": [
                {
                    "evidence_type": "comment",
                    "comment_text": text,
                    "url": f"https://example.test/{decision}",
                    "user_attestation_text": "I confirm lawful source.",
                }
                for decision, text in comments_by_decision.items()
            ],
        },
    )
    assert response.status_code == 200
    ids_by_text = {item["comment_text"]: item["evidence_id"] for item in response.json()["evidence_items"]}

    for decision, text in comments_by_decision.items():
        payload = {"decision": decision, "reviewer_label": "qa"}
        if decision == "approve":
            payload["notes"] = "approved with access_token=secret-marker-should-not-appear"
        review_response = client.post(
            f"/api/v1/cases/{case_id}/evidence/{ids_by_text[text]}/review",
            json=payload,
        )
        assert review_response.status_code == 200
        body = review_response.json()
        assert body["history_entry"]["decision"] == decision
        assert body["history_entry"]["safe_mode"]["no_ai_verification"] is True
        assert body["history_entry"]["safe_mode"]["no_url_fetch"] is True
        assert body["history_entry"]["safe_mode"]["no_secret_exposed"] is True

    timeline_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-timeline")
    assert timeline_response.status_code == 200
    timeline = timeline_response.json()
    assert timeline["total_review_events"] == 6
    assert len(timeline["entries"]) == 6
    assert "secret-marker-should-not-appear" not in str(timeline)
    assert "[REDACTED]" in str(timeline)

    audit_response = client.get(f"/api/v1/cases/{case_id}/evidence/review-audit-summary")
    assert audit_response.status_code == 200
    audit = audit_response.json()
    assert audit["total_review_events"] == 6
    assert audit["approved_count"] == 1
    assert audit["rejected_count"] == 1
    assert audit["marked_weak_count"] == 1
    assert audit["needs_more_source_count"] == 1
    assert audit["duplicate_merged_count"] == 1
    assert audit["reset_count"] == 1
    assert audit["evidence_with_history_count"] == 6
    assert audit["latest_reviewed_at"]

    approve_history_response = client.get(
        f"/api/v1/cases/{case_id}/evidence/{ids_by_text[comments_by_decision['approve']]}/review-history"
    )
    assert approve_history_response.status_code == 200
    approve_history = approve_history_response.json()
    assert approve_history["total_review_events"] == 1
    assert approve_history["entries"][0]["decision"] == "approve"


def test_merge_duplicate_review_status_preserves_collapse_without_inflating_counts() -> None:
    case_id = _create_case(platforms=["public_web"])
    duplicate_item = {
        "evidence_type": "comment",
        "comment_text": "Duplicate group should be merged by human review.",
        "url": "https://example.test/duplicate",
        "user_attestation_text": "I confirm lawful source.",
    }
    response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "public_web",
                "source_type": "public_web",
                "acquisition_mode": "manual_url",
            },
            "evidence_items": [duplicate_item, duplicate_item],
        },
    )
    assert response.status_code == 200
    item = response.json()["evidence_items"][0]

    review_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/{item['evidence_id']}/review",
        json={"decision": "merge_duplicate"},
    )
    assert review_response.status_code == 200
    assert review_response.json()["review_status"] == "duplicate_merged"

    run_response = client.post(f"/api/v1/cases/{case_id}/run")
    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_result"]["evidence_item_count"] == 1
    assert body["analysis_result"]["evidence_duplicate_item_count"] == 1
    assert body["analysis_result"]["evidence_review_excluded_count"] == 0


def test_raw_comments_take_priority_over_evidence_items_when_both_exist(monkeypatch) -> None:
    case_id = _create_case(platforms=["youtube"])
    attach_response = client.post(
        f"/api/v1/cases/{case_id}/evidence/attach",
        json={
            "source": {
                "platform": "uploaded_dataset",
                "source_type": "uploaded_dataset",
                "acquisition_mode": "user_upload",
            },
            "evidence_items": [
                {
                    "evidence_type": "comment",
                    "comment_text": "Manual evidence exists but raw YouTube comments should win.",
                }
            ],
        },
    )
    assert attach_response.status_code == 200

    def fake_start_crawl(payload):
        return _crawl_response()

    monkeypatch.setattr("app.services.case_store.start_crawl_with_adapters", fake_start_crawl)
    crawl_response = client.post(f"/api/v1/cases/{case_id}/crawl/start", json={"limit": 3})
    assert crawl_response.status_code == 200

    run_response = client.post(f"/api/v1/cases/{case_id}/run")

    assert run_response.status_code == 200
    body = run_response.json()
    assert body["analysis_input_source"] == "case_raw_data"
    assert body["analysis_result"]["analysis_input_source"] == "case_raw_data"
    assert body["raw_comment_count"] == 1
    assert body["evidence_item_count"] == 2
    assert any("YouTube fixture quality issue comment" in comment for comment in body["report"]["representative_comments"])


def test_case_without_evidence_still_falls_back_to_mock_data() -> None:
    case_id = _create_case()
    response = client.post(f"/api/v1/cases/{case_id}/run")

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_input_source"] == "mock_data_fallback"
    assert body["analysis_result"]["evidence_item_count"] == 0
    assert body["report"]["evidence_item_count"] == 0


def test_converter_redacts_nested_secret_fields() -> None:
    items = build_evidence_items_from_raw_data(
        case_id="case_001",
        raw_posts=[
            _youtube_post().model_copy(
                update={
                    "raw_data": {
                        "source_type": "youtube_data_api_v3",
                        "nested": {"refresh_token": "secret-marker-should-not-appear"},
                    }
                }
            )
        ],
        raw_comments=[],
        crawl_metadata=[],
    )

    assert "refresh_token" not in items[0].raw_data_safe["nested"]
    assert "secret-marker-should-not-appear" not in str(items[0].raw_data_safe)


def test_interaction_metric_evidence_type_is_supported() -> None:
    item = EvidenceItem(
        evidence_id="evidence_metric_001",
        platform="uploaded_dataset",
        source_type="uploaded_dataset",
        acquisition_mode="user_upload",
        evidence_type="interaction_metric",
        like_count=42,
        reply_count=7,
        share_count=3,
        view_count=1200,
    )

    assert item.evidence_type == "interaction_metric"
    assert item.view_count == 1200


def test_mediacrawler_is_not_integrated_in_product_code() -> None:
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


def _create_case(platforms: list[str] | None = None) -> str:
    response = client.post(
        "/api/v1/cases",
        json={"keyword": "Tesla", "platforms": platforms or ["reddit"], "title": "Evidence QA Case"},
    )
    assert response.status_code == 200
    return response.json()["case_id"]


def _crawl_response():
    from app.schemas.crawl import CrawlStartResponse

    return CrawlStartResponse(
        project_id="project_crawl_youtube",
        crawl_task_id="task_youtube_fixture",
        status="completed",
        message="Fixture YouTube crawl response.",
        platform_metadata=[
            PlatformCrawlMetadata(
                platform="youtube",
                adapter_mode="real",
                source_type="youtube_data_api_v3",
                fallback_used=False,
                credential_present=True,
                post_count=1,
                comment_count=1,
            )
        ],
        raw_posts=[_youtube_post()],
        raw_comments=[_youtube_comment()],
    )


def _youtube_post() -> RawPost:
    return RawPost(
        platform="youtube",
        post_id="yt_video_001",
        author_id="yt_channel_001",
        author_name="Fixture YouTube Channel",
        title="YouTube public video title",
        content="Fixture metadata from a mocked official YouTube Data API response.",
        like_count=12,
        reply_count=1,
        share_count=0,
        created_at="2026-05-21T12:00:00Z",
        url="https://www.youtube.com/watch?v=yt_video_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real", "api_key": "redact-me"},
    )


def _youtube_comment() -> RawComment:
    return RawComment(
        platform="youtube",
        post_id="yt_video_001",
        comment_id="yt_comment_001",
        parent_id=None,
        author_id="yt_commenter_001",
        author_name="Fixture commenter",
        content="YouTube fixture quality issue comment: the response is delayed.",
        like_count=4,
        reply_count=0,
        share_count=0,
        created_at="2026-05-21T12:05:00Z",
        url="https://www.youtube.com/watch?v=yt_video_001&lc=yt_comment_001",
        raw_data={"source_type": "youtube_data_api_v3", "mode": "real"},
    )
