from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.evidence import (
    EvidenceDeduplicationSummary,
    EvidenceDuplicateGroup,
    EvidenceAcquisitionMode,
    EvidenceIngestionBatch,
    EvidenceIngestionResult,
    EvidenceItem,
    EvidenceNormalizationMetadata,
    EvidenceReviewAuditSummary,
    EvidenceReviewDecisionRequest,
    EvidenceReviewDecisionResult,
    EvidenceReviewHistoryEntry,
    EvidenceReviewQueueItem,
    EvidenceReviewSummary,
    EvidenceReviewStatus,
    EvidenceReviewTimeline,
    EvidenceSourceType,
    EvidenceTrustSummary,
)


SECRET_KEY_MARKERS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "access_token",
    "refresh_token",
    "client_secret",
    "cookie",
    "authorization",
    "password",
    "credential",
    ".env",
)

SECRET_TEXT_PATTERN = re.compile(
    r"\b(api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|cookie|authorization)\b\s*[:=]\s*([^\s,;]+)",
    re.IGNORECASE,
)

NON_ANALYSIS_REVIEW_STATUSES = {"rejected"}

MANUAL_TEXT_FIELDS = (
    "title",
    "body_text",
    "comment_text",
    "parent_id",
    "root_id",
    "author_id",
    "author_name",
    "url",
    "created_at",
    "language",
)

VIDEO_PLATFORMS = {"youtube", "douyin", "bilibili", "kuaishou"}
NEWS_PLATFORMS = {"the_paper", "jiemian", "toutiao"}
FORUM_PLATFORMS = {"hupu", "tieba", "nga", "maimai", "douban", "zhihu"}
DIRECT_SOURCE_TYPES = {"youtube", "douyin", "bilibili", "weibo", "xiaohongshu", "reddit"}
SUPPORTED_PLATFORM_CLAIMS = {
    "youtube",
    "douyin",
    "bilibili",
    "weibo",
    "xiaohongshu",
    "reddit",
    "news_site",
    "forum",
    "public_web",
    "uploaded_dataset",
    "mock",
    "manual_url",
    "user_upload",
}
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "spm",
}


class EvidenceValidationError(ValueError):
    """Raised when user-provided evidence cannot be normalized safely."""


def build_evidence_items_from_raw_data(
    *,
    case_id: str,
    raw_posts: list[RawPost],
    raw_comments: list[RawComment],
    crawl_metadata: list[PlatformCrawlMetadata] | None = None,
) -> list[EvidenceItem]:
    metadata_by_platform = {item.platform.lower(): item for item in crawl_metadata or []}
    items: list[EvidenceItem] = []
    for post in raw_posts:
        items.append(
            raw_post_to_evidence_item(
                post,
                case_id=case_id,
                metadata=metadata_by_platform.get(post.platform.lower()),
            )
        )
    for comment in raw_comments:
        items.append(
            raw_comment_to_evidence_item(
                comment,
                case_id=case_id,
                metadata=metadata_by_platform.get(comment.platform.lower()),
            )
        )
    return enrich_and_deduplicate_evidence_items(items)


def raw_post_to_evidence_item(
    post: RawPost,
    *,
    case_id: str | None = None,
    metadata: PlatformCrawlMetadata | None = None,
) -> EvidenceItem:
    normalized = RawPost.model_validate(post)
    source_type = _source_type_for_platform(normalized.platform)
    acquisition_mode = _acquisition_mode(normalized.platform, normalized.raw_data, metadata)
    evidence_type = "video" if normalized.platform.lower() in VIDEO_PLATFORMS else "article" if source_type == "news_site" else "post"
    record_id = str(normalized.post_id)
    return enrich_evidence_item(EvidenceItem(
        evidence_id=_evidence_id(normalized.platform, evidence_type, record_id),
        case_id=case_id,
        platform=normalized.platform,
        source_type=source_type,
        acquisition_mode=acquisition_mode,
        evidence_type=evidence_type,
        title=normalized.title,
        body_text=normalized.content,
        root_id=record_id,
        author_id=normalized.author_id,
        author_name=normalized.author_name,
        url=normalized.url,
        created_at=normalized.created_at,
        like_count=normalized.like_count,
        reply_count=normalized.reply_count,
        share_count=normalized.share_count,
        raw_data_safe=sanitize_raw_data(normalized.raw_data),
        language=_infer_language(normalized.title, normalized.content),
        content_visibility="public",
        access_scope="public",
        provenance_type=_provenance_for_acquisition(acquisition_mode),
        verification_status="needs_review",
        source_url=normalized.url,
        source_url_present=bool(normalized.url),
        source_platform_claim=normalized.platform,
        source_capture_method="official_api" if acquisition_mode == "official_api_public" else acquisition_mode,
        user_attestation_required=False,
        ingestion_metadata=_metadata(
            normalized_from="raw_post",
            source_record_id=record_id,
            source_type=source_type,
            acquisition_mode=acquisition_mode,
        ),
    ))


def raw_comment_to_evidence_item(
    comment: RawComment,
    *,
    case_id: str | None = None,
    metadata: PlatformCrawlMetadata | None = None,
) -> EvidenceItem:
    normalized = RawComment.model_validate(comment)
    source_type = _source_type_for_platform(normalized.platform)
    acquisition_mode = _acquisition_mode(normalized.platform, normalized.raw_data, metadata)
    evidence_type = "reply" if normalized.parent_id else "comment"
    record_id = str(normalized.comment_id)
    return enrich_evidence_item(EvidenceItem(
        evidence_id=_evidence_id(normalized.platform, evidence_type, record_id),
        case_id=case_id,
        platform=normalized.platform,
        source_type=source_type,
        acquisition_mode=acquisition_mode,
        evidence_type=evidence_type,
        comment_text=normalized.content,
        parent_id=normalized.parent_id,
        root_id=normalized.post_id,
        author_id=normalized.author_id,
        author_name=normalized.author_name,
        url=normalized.url,
        created_at=normalized.created_at,
        like_count=normalized.like_count,
        reply_count=normalized.reply_count,
        share_count=normalized.share_count,
        raw_data_safe=sanitize_raw_data(normalized.raw_data),
        language=_infer_language(normalized.content),
        content_visibility="public",
        access_scope="public",
        provenance_type=_provenance_for_acquisition(acquisition_mode),
        verification_status="needs_review",
        source_url=normalized.url,
        source_url_present=bool(normalized.url),
        source_platform_claim=normalized.platform,
        source_capture_method="official_api" if acquisition_mode == "official_api_public" else acquisition_mode,
        user_attestation_required=False,
        ingestion_metadata=_metadata(
            normalized_from="raw_comment",
            source_record_id=record_id,
            source_type=source_type,
            acquisition_mode=acquisition_mode,
        ),
    ))


def normalize_manual_evidence_batch(case_id: str, batch: EvidenceIngestionBatch) -> list[EvidenceItem]:
    source = batch.source
    items: list[EvidenceItem] = []
    for index, item in enumerate(batch.evidence_items):
        platform = source.platform if source else item.platform
        platform = platform or item.platform or "uploaded_dataset"
        source_type = source.source_type if source else item.source_type
        acquisition_mode = source.acquisition_mode if source else item.acquisition_mode
        is_manual_url = acquisition_mode == "manual_url"
        if is_manual_url:
            platform = platform if platform and platform != "uploaded_dataset" else "manual_url"
            source_type = source_type if source_type and source_type != "uploaded_dataset" else "public_web"
            acquisition_mode = "manual_url"
            if not _has_reviewable_text(item):
                raise EvidenceValidationError("manual_evidence_text_required")
        evidence_type = _manual_evidence_type(item) if item.evidence_type == "body_text" else item.evidence_type
        record_id = item.evidence_id or f"{case_id}_{index + 1}"
        redacted_item, redaction_warnings = _redact_manual_text_fields(item)
        normalized_metadata = item.ingestion_metadata.model_copy(
            update={
                "normalized_from": "manual_payload",
                "source_record_id": item.ingestion_metadata.source_record_id or record_id,
                "source_type": source_type,
                "acquisition_mode": acquisition_mode,
                "normalized_at": datetime.now(timezone.utc),
                "warnings": _dedupe_warnings([*item.ingestion_metadata.warnings, *redaction_warnings]),
            },
            deep=True,
        )
        items.append(
            redacted_item.model_copy(
                update={
                    "evidence_id": redacted_item.evidence_id or _evidence_id(platform, evidence_type, record_id),
                    "case_id": case_id,
                    "platform": platform,
                    "source_type": source_type,
                    "acquisition_mode": acquisition_mode,
                    "evidence_type": evidence_type,
                    "raw_data_safe": sanitize_raw_data(redacted_item.raw_data_safe),
                    "language": redacted_item.language if redacted_item.language != "unknown" else _infer_language(redacted_item.title, redacted_item.body_text, redacted_item.comment_text),
                    "provenance_type": redacted_item.provenance_type if redacted_item.provenance_type != "user_upload" or acquisition_mode != "manual_url" else "manual_url",
                    "source_url": redacted_item.source_url or redacted_item.url,
                    "source_url_present": bool(redacted_item.source_url or redacted_item.url),
                    "source_platform_claim": redacted_item.source_platform_claim or platform,
                    "user_attestation_required": acquisition_mode in {"manual_url", "user_upload"},
                    "ingestion_metadata": normalized_metadata,
                },
                deep=True,
            )
        )
    return enrich_and_deduplicate_evidence_items(items)


def evidence_items_to_raw_data(evidence_items: list[EvidenceItem]) -> tuple[list[RawPost], list[RawComment]]:
    posts: list[RawPost] = []
    comments: list[RawComment] = []
    post_ids: set[str] = set()
    now = datetime.now(timezone.utc).isoformat()

    for item in enrich_and_deduplicate_evidence_items(evidence_items):
        platform = item.platform or "uploaded_dataset"
        root_id = item.root_id or item.evidence_id or f"evidence_{len(posts) + 1}"
        raw_data = {
            "source_type": item.source_type,
            "acquisition_mode": item.acquisition_mode,
            "evidence_id": item.evidence_id,
            "normalized_evidence": True,
            "trust_label": item.trust_label,
            "verification_status": item.verification_status,
            "duplicate_count": item.duplicate_count,
        }
        if item.evidence_type in {"video", "article", "post", "title", "body_text", "metadata"} and root_id not in post_ids:
            posts.append(
                RawPost(
                    platform=platform,
                    post_id=root_id,
                    author_id=item.author_id or "evidence_source",
                    author_name=item.author_name or "Evidence source",
                    title=item.title or _trim_text(item.body_text or item.comment_text or "Evidence item", 120),
                    content=item.body_text or item.title or item.comment_text or "",
                    like_count=max(0, int(item.like_count or 0)),
                    reply_count=max(0, int(item.reply_count or 0)),
                    share_count=max(0, int(item.share_count or 0)),
                    created_at=item.created_at or now,
                    url=item.url or "",
                    raw_data=raw_data,
                )
            )
            post_ids.add(root_id)

        if item.evidence_type in {"comment", "reply", "body_text", "article", "post", "video"}:
            content = item.comment_text or item.body_text or item.title or ""
            if not content:
                continue
            comments.append(
                RawComment(
                    platform=platform,
                    post_id=root_id,
                    comment_id=item.evidence_id or _evidence_id(platform, item.evidence_type, str(len(comments) + 1)),
                    parent_id=item.parent_id,
                    author_id=item.author_id or "evidence_author",
                    author_name=item.author_name or "Evidence author",
                    content=content,
                    like_count=max(0, int(item.like_count or 0)),
                    reply_count=max(0, int(item.reply_count or 0)),
                    share_count=max(0, int(item.share_count or 0)),
                    created_at=item.created_at or now,
                    url=item.url or "",
                    raw_data=raw_data,
                )
            )

    return posts, comments


def build_evidence_ingestion_result(
    case_id: str,
    evidence_items: list[EvidenceItem],
    *,
    status: str | None = None,
    warnings: list[str] | None = None,
) -> EvidenceIngestionResult:
    evidence_items = enrich_and_deduplicate_evidence_items(evidence_items)
    source_distribution = evidence_source_distribution(evidence_items)
    evidence_type_counts = evidence_type_distribution(evidence_items)
    top_titles = _top_titles(evidence_items)
    representative_comments = _representative_comments(evidence_items)
    dedup_summary = build_deduplication_summary(evidence_items)
    trust_summary = build_trust_summary(evidence_items, dedup_summary=dedup_summary)
    result_warnings = _dedupe_warnings(
        [
            *(warnings or []),
            *[
                warning
                for item in evidence_items
                for warning in item.ingestion_metadata.warnings
            ],
        ]
    )
    return EvidenceIngestionResult(
        case_id=case_id,
        status=status or ("attached" if evidence_items else "empty"),
        evidence_items=evidence_items,
        evidence_item_count=len(evidence_items),
        source_distribution=source_distribution,
        evidence_type_counts=evidence_type_counts,
        top_titles=top_titles,
        representative_comments=representative_comments,
        trust_summary=trust_summary,
        deduplication_summary=dedup_summary,
        ingestion_metadata=_metadata(
            normalized_from="evidence_batch",
            source_record_id=case_id,
            source_type=_dominant_source_type(evidence_items),
            acquisition_mode=_dominant_acquisition_mode(evidence_items),
        ),
        warnings=result_warnings,
    )


def enrich_evidence_item(item: EvidenceItem) -> EvidenceItem:
    normalized = EvidenceItem.model_validate(item)
    provenance_type = _resolve_provenance_type(normalized)
    url = normalized.source_url or normalized.url
    canonical_url = _canonicalize_url(url)
    source_url_present = bool(canonical_url)
    text = _evidence_text(normalized)
    content_hash = _content_hash(normalized, canonical_url=canonical_url)
    normalized_content_hash = _normalized_content_hash(normalized, canonical_url=canonical_url)
    canonical_url_hash = _hash_text(canonical_url) if canonical_url else None
    risk_flags = _risk_flags(normalized, provenance_type=provenance_type, source_url_present=source_url_present)
    verification_status, trust_score, trust_label, verification_notes = _trust_assessment(
        normalized,
        provenance_type=provenance_type,
        source_url_present=source_url_present,
        risk_flags=risk_flags,
    )
    if normalized.review_status == "rejected" or normalized.verification_status == "rejected":
        verification_status = "rejected"
        trust_score = 0.0
        trust_label = "rejected"
        risk_flags = _dedupe_warnings([*risk_flags, "human_review_rejected"])
        verification_notes = _dedupe_warnings([*verification_notes, "Human review rejected this evidence for analysis by default."])
    elif normalized.review_status == "marked_weak":
        trust_score = min(trust_score, 0.35)
        trust_label = _trust_label_for_score(trust_score, verification_status, [*risk_flags, "marked_weak_evidence"])
        risk_flags = _dedupe_warnings([*risk_flags, "marked_weak_evidence"])
        verification_notes = _dedupe_warnings([*verification_notes, "Human review marked this as weak evidence."])
    duplicate_group_id = normalized.duplicate_group_id or f"dup_{normalized_content_hash[:16]}"
    source_capture_method = normalized.source_capture_method or _capture_method_for_provenance(provenance_type)
    user_attestation_required = provenance_type in {"manual_url", "manual_text", "screenshot_transcription", "user_upload"}
    submitted_at = normalized.submitted_at
    if user_attestation_required and submitted_at is None:
        submitted_at = datetime.now(timezone.utc)
    return normalized.model_copy(
        update={
            "provenance_type": provenance_type,
            "verification_status": verification_status,
            "trust_score": trust_score,
            "trust_label": trust_label,
            "source_url_present": source_url_present,
            "source_url": canonical_url or url,
            "source_platform_claim": normalized.source_platform_claim or normalized.platform,
            "source_capture_method": source_capture_method,
            "submitted_at": submitted_at,
            "user_attestation_required": user_attestation_required,
            "verification_notes": _dedupe_warnings([*normalized.verification_notes, *verification_notes]),
            "duplicate_group_id": duplicate_group_id,
            "content_hash": content_hash,
            "normalized_content_hash": normalized_content_hash,
            "canonical_url_hash": canonical_url_hash,
            "duplicate_count": max(1, int(normalized.duplicate_count or 1)),
            "duplicate_group_size": max(1, int(normalized.duplicate_group_size or 1)),
            "risk_flags": _dedupe_warnings([*normalized.risk_flags, *risk_flags]),
        },
        deep=True,
    )


def enrich_and_deduplicate_evidence_items(evidence_items: list[EvidenceItem]) -> list[EvidenceItem]:
    grouped: dict[str, EvidenceItem] = {}
    counts: Counter[str] = Counter()
    for item in evidence_items:
        enriched = enrich_evidence_item(item)
        group_key = enriched.normalized_content_hash or enriched.content_hash or enriched.evidence_id
        counts[group_key] += max(1, int(enriched.duplicate_count or 1))
        if group_key not in grouped:
            grouped[group_key] = enriched
            continue
        existing = grouped[group_key]
        merged_flags = _dedupe_warnings([*existing.risk_flags, *enriched.risk_flags, "duplicate_submission"])
        merged_notes = _dedupe_warnings([*existing.verification_notes, *enriched.verification_notes, "Repeated evidence collapsed into one duplicate group."])
        merged_history = [*existing.review_history, *enriched.review_history]
        grouped[group_key] = existing.model_copy(
            update={
                "risk_flags": merged_flags,
                "verification_notes": merged_notes,
                "review_history": merged_history,
            },
            deep=True,
        )

    unique_items: list[EvidenceItem] = []
    used_ids: set[str] = set()
    for group_key, item in grouped.items():
        group_size = max(1, counts[group_key])
        flags = list(item.risk_flags)
        notes = list(item.verification_notes)
        trust_score = item.trust_score
        trust_label = item.trust_label
        verification_status = item.verification_status
        if group_size > 1:
            flags = _dedupe_warnings([*flags, "duplicate_submission"])
            notes = _dedupe_warnings([*notes, f"duplicate_group_size:{group_size}"])
        if group_size >= 4:
            flags = _dedupe_warnings([*flags, "high_duplicate_count"])
            trust_score = min(trust_score, 0.5)
            trust_label = _trust_label_for_score(trust_score, verification_status, flags)
        evidence_id = _unique_evidence_id(item.evidence_id, used_ids)
        used_ids.add(evidence_id)
        unique_items.append(
            item.model_copy(
                update={
                    "evidence_id": evidence_id,
                    "duplicate_count": group_size,
                    "duplicate_group_size": group_size,
                    "risk_flags": flags,
                    "verification_notes": notes,
                    "trust_score": trust_score,
                    "trust_label": trust_label,
                },
                deep=True,
            )
        )
    return unique_items


def merge_evidence_items(existing_items: list[EvidenceItem], incoming_items: list[EvidenceItem]) -> list[EvidenceItem]:
    return enrich_and_deduplicate_evidence_items([*existing_items, *incoming_items])


def build_deduplication_summary(evidence_items: list[EvidenceItem]) -> EvidenceDeduplicationSummary:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    total_items = sum(max(1, int(item.duplicate_count or 1)) for item in unique_items)
    duplicate_items = max(0, total_items - len(unique_items))
    duplicate_groups = [
        EvidenceDuplicateGroup(
            duplicate_group_id=item.duplicate_group_id or f"dup_{item.normalized_content_hash[:16]}",
            duplicate_group_size=max(1, int(item.duplicate_count or 1)),
            representative_evidence_id=item.evidence_id,
            normalized_content_hash=item.normalized_content_hash,
            canonical_url_hash=item.canonical_url_hash,
            sample_text=_trim_text(_evidence_text(item), 160) or None,
        )
        for item in unique_items
        if max(1, int(item.duplicate_count or 1)) > 1
    ]
    duplicate_groups.sort(key=lambda group: group.duplicate_group_size, reverse=True)
    return EvidenceDeduplicationSummary(
        total_items=total_items,
        unique_items=len(unique_items),
        duplicate_items=duplicate_items,
        duplicate_group_count=len(duplicate_groups),
        top_duplicate_groups=duplicate_groups[:5],
    )


def build_trust_summary(
    evidence_items: list[EvidenceItem],
    *,
    dedup_summary: EvidenceDeduplicationSummary | None = None,
) -> EvidenceTrustSummary:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    trust_distribution = Counter(item.trust_label for item in unique_items)
    verification_distribution = Counter(item.verification_status for item in unique_items)
    provenance_distribution = Counter(item.provenance_type for item in unique_items)
    warning_counts = Counter(flag for item in unique_items for flag in item.risk_flags)
    review_needed_count = sum(
        1
        for item in unique_items
        if item.verification_status in {"needs_review", "rejected"}
        or item.trust_label in {"low", "unverified", "rejected"}
        or "user_attestation_missing" in item.risk_flags
    )
    return EvidenceTrustSummary(
        trust_label_distribution=dict(trust_distribution),
        verification_status_distribution=dict(verification_distribution),
        provenance_type_distribution=dict(provenance_distribution),
        warning_counts=dict(warning_counts),
        review_needed_count=review_needed_count,
        low_trust_count=int(trust_distribution.get("low", 0)),
        unverified_count=int(trust_distribution.get("unverified", 0)),
        duplicate_summary=dedup_summary or build_deduplication_summary(unique_items),
    )


def analysis_eligible_evidence_items(evidence_items: list[EvidenceItem]) -> list[EvidenceItem]:
    """Return deduplicated evidence that is usable for deterministic analysis."""

    return [
        item
        for item in enrich_and_deduplicate_evidence_items(evidence_items)
        if item.review_status not in NON_ANALYSIS_REVIEW_STATUSES
        and item.verification_status != "rejected"
        and item.trust_label != "rejected"
    ]


def build_review_summary(case_id: str, evidence_items: list[EvidenceItem]) -> EvidenceReviewSummary:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    queue_items = [
        _review_queue_item(item)
        for item in unique_items
        if _include_in_review_queue(item)
    ]
    return EvidenceReviewSummary(
        case_id=case_id,
        total_evidence_count=len(unique_items),
        queue_count=len(queue_items),
        review_needed_count=sum(1 for item in queue_items if item.review_status == "review_needed"),
        low_trust_count=sum(1 for item in unique_items if item.trust_label in {"low", "unverified", "rejected"}),
        duplicate_group_count=sum(1 for item in unique_items if max(1, int(item.duplicate_count or 1)) > 1),
        rejected_count=sum(1 for item in unique_items if item.review_status == "rejected"),
        approved_count=sum(1 for item in unique_items if item.review_status == "approved"),
        marked_weak_count=sum(1 for item in unique_items if item.review_status == "marked_weak"),
        needs_more_source_count=sum(1 for item in unique_items if item.review_status == "needs_more_source"),
        duplicate_merged_count=sum(1 for item in unique_items if item.review_status == "duplicate_merged"),
        queue_items=queue_items,
    )


def build_review_timeline(
    case_id: str,
    evidence_items: list[EvidenceItem],
    *,
    evidence_id: str | None = None,
) -> EvidenceReviewTimeline:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    entries: list[EvidenceReviewHistoryEntry] = []
    for item in unique_items:
        if evidence_id is not None and item.evidence_id != evidence_id:
            continue
        entries.extend(item.review_history)
    entries.sort(key=lambda entry: entry.reviewed_at, reverse=True)
    return EvidenceReviewTimeline(
        case_id=case_id,
        evidence_id=evidence_id,
        entries=entries,
        total_review_events=len(entries),
    )


def build_review_audit_summary(case_id: str, evidence_items: list[EvidenceItem]) -> EvidenceReviewAuditSummary:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    timeline = build_review_timeline(case_id, unique_items)
    entries = timeline.entries
    return EvidenceReviewAuditSummary(
        case_id=case_id,
        total_review_events=len(entries),
        approved_count=sum(1 for entry in entries if entry.decision == "approve"),
        rejected_count=sum(1 for entry in entries if entry.decision == "reject"),
        marked_weak_count=sum(1 for entry in entries if entry.decision == "mark_weak"),
        needs_more_source_count=sum(1 for entry in entries if entry.decision == "request_more_source"),
        duplicate_merged_count=sum(1 for entry in entries if entry.decision == "merge_duplicate"),
        reset_count=sum(1 for entry in entries if entry.decision == "reset_review"),
        latest_reviewed_at=entries[0].reviewed_at if entries else None,
        evidence_with_history_count=sum(1 for item in unique_items if item.review_history),
    )


def apply_review_decision(
    *,
    case_id: str,
    evidence_items: list[EvidenceItem],
    evidence_id: str,
    request: EvidenceReviewDecisionRequest,
    reviewed_at: datetime | None = None,
) -> tuple[list[EvidenceItem], EvidenceReviewDecisionResult] | None:
    unique_items = enrich_and_deduplicate_evidence_items(evidence_items)
    updated_items: list[EvidenceItem] = []
    updated_item: EvidenceItem | None = None
    timestamp = reviewed_at or datetime.now(timezone.utc)
    for item in unique_items:
        if item.evidence_id != evidence_id:
            updated_items.append(item)
            continue
        updated_item = _apply_decision_to_item(item, request, reviewed_at=timestamp)
        updated_items.append(updated_item)
    if updated_item is None:
        return None
    deduped_items = enrich_and_deduplicate_evidence_items(updated_items)
    persisted_item = next((item for item in deduped_items if item.evidence_id == updated_item.evidence_id), updated_item)
    result = EvidenceReviewDecisionResult(
        case_id=case_id,
        evidence_id=persisted_item.evidence_id,
        decision=request.decision,
        review_status=persisted_item.review_status,
        evidence_item=persisted_item,
        summary=build_review_summary(case_id, deduped_items),
        history_entry=persisted_item.review_history[-1] if persisted_item.review_history else None,
    )
    return deduped_items, result


def _include_in_review_queue(item: EvidenceItem) -> bool:
    if item.review_status in {"approved", "rejected", "marked_weak", "needs_more_source", "duplicate_merged"}:
        return True
    return bool(_review_reason_codes(item))


def _review_queue_item(item: EvidenceItem) -> EvidenceReviewQueueItem:
    reason_codes = _review_reason_codes(item)
    review_status = _effective_review_status(item, reason_codes)
    return EvidenceReviewQueueItem(
        evidence_id=item.evidence_id,
        case_id=item.case_id,
        platform=item.platform,
        evidence_type=item.evidence_type,
        title=item.title,
        body_text_preview=_trim_text(item.body_text or "", 180) or None,
        comment_text_preview=_trim_text(item.comment_text or "", 180) or None,
        url=item.source_url or item.url,
        provenance_type=item.provenance_type,
        verification_status=item.verification_status,
        trust_label=item.trust_label,
        trust_score=item.trust_score,
        risk_flags=item.risk_flags,
        duplicate_group_id=item.duplicate_group_id,
        duplicate_count=item.duplicate_count,
        source_url_present=item.source_url_present,
        user_attestation_required=item.user_attestation_required,
        user_attestation_text=item.user_attestation_text,
        review_status=review_status,
        review_reason_codes=reason_codes,
        created_at=item.created_at,
        submitted_at=item.submitted_at,
    )


def _review_reason_codes(item: EvidenceItem) -> list[str]:
    reasons: list[str] = []
    if item.verification_status in {"needs_review", "source_url_provided_unverified", "user_attested_unverified", "screenshot_unverified"}:
        reasons.append(f"verification:{item.verification_status}")
    if item.trust_label in {"low", "unverified", "rejected"}:
        reasons.append(f"trust:{item.trust_label}")
    if item.provenance_type == "screenshot_transcription":
        reasons.append("provenance:screenshot_transcription")
    if not item.source_url_present:
        reasons.append("source_url_missing")
    if max(1, int(item.duplicate_count or 1)) > 1:
        reasons.append("duplicate_group")
    if item.user_attestation_required and not (item.user_attestation_text or "").strip():
        reasons.append("user_attestation_missing")
    reasons.extend(f"risk_flag:{flag}" for flag in item.risk_flags if flag)
    if item.review_status in {"rejected", "marked_weak", "needs_more_source", "duplicate_merged"}:
        reasons.append(f"review_status:{item.review_status}")
    return _dedupe_warnings(reasons)


def _effective_review_status(item: EvidenceItem, reason_codes: list[str] | None = None) -> EvidenceReviewStatus:
    if item.review_status != "not_reviewed":
        return item.review_status
    active_reasons = reason_codes if reason_codes is not None else _review_reason_codes(item)
    if active_reasons:
        return "review_needed"
    return "not_reviewed"


def _apply_decision_to_item(
    item: EvidenceItem,
    request: EvidenceReviewDecisionRequest,
    *,
    reviewed_at: datetime,
) -> EvidenceItem:
    notes = list(item.review_notes)
    sanitized_note = _sanitize_review_note(request.notes)
    if sanitized_note:
        notes.append(sanitized_note)
    reviewer_label = request.reviewer_label or item.reviewer_label
    base_update = {
        "reviewed_at": reviewed_at,
        "reviewer_label": reviewer_label,
        "review_notes": _dedupe_warnings(notes),
    }
    if request.decision == "approve":
        updated = item.model_copy(update={**base_update, "review_status": "approved"}, deep=True)
    elif request.decision == "reject":
        flags = _dedupe_warnings([*item.risk_flags, "human_review_rejected"])
        updated = item.model_copy(
            update={
                **base_update,
                "review_status": "rejected",
                "verification_status": "rejected",
                "trust_score": 0.0,
                "trust_label": "rejected",
                "risk_flags": flags,
            },
            deep=True,
        )
    elif request.decision == "mark_weak":
        flags = _dedupe_warnings([*item.risk_flags, "marked_weak_evidence"])
        updated = item.model_copy(
            update={
                **base_update,
                "review_status": "marked_weak",
                "trust_score": min(item.trust_score, 0.35),
                "trust_label": "low",
                "risk_flags": flags,
            },
            deep=True,
        )
    elif request.decision == "request_more_source":
        flags = _dedupe_warnings([*item.risk_flags, "source_review_requested"])
        updated = item.model_copy(
            update={**base_update, "review_status": "needs_more_source", "risk_flags": flags},
            deep=True,
        )
    elif request.decision == "merge_duplicate":
        flags = _dedupe_warnings([*item.risk_flags, "duplicate_merged"])
        updated = item.model_copy(
            update={**base_update, "review_status": "duplicate_merged", "risk_flags": flags},
            deep=True,
        )
    else:
        updated = item.model_copy(
            update={
                "review_status": "not_reviewed",
                "reviewed_at": reviewed_at,
                "reviewer_label": reviewer_label,
                "review_notes": _dedupe_warnings(notes),
                "verification_status": "needs_review",
                "trust_label": "unverified",
                "risk_flags": [
                    flag
                    for flag in item.risk_flags
                    if flag not in {"human_review_rejected", "marked_weak_evidence", "source_review_requested", "duplicate_merged"}
                ],
            },
            deep=True,
        )
    return _append_review_history(item, updated, request, reviewed_at=reviewed_at, note=sanitized_note)


def _append_review_history(
    original: EvidenceItem,
    updated: EvidenceItem,
    request: EvidenceReviewDecisionRequest,
    *,
    reviewed_at: datetime,
    note: str | None,
) -> EvidenceItem:
    reason_codes = _review_reason_codes(original) or _review_reason_codes(updated)
    entry = EvidenceReviewHistoryEntry(
        review_event_id=_review_event_id(
            updated.case_id or original.case_id,
            updated.evidence_id,
            request.decision,
            reviewed_at,
            len(original.review_history),
        ),
        evidence_id=updated.evidence_id,
        case_id=updated.case_id or original.case_id,
        previous_review_status=_effective_review_status(original, reason_codes),
        new_review_status=updated.review_status,
        decision=request.decision,
        reason_code=reason_codes[0] if reason_codes else f"decision:{request.decision}",
        reviewer_label=request.reviewer_label or updated.reviewer_label,
        reviewed_at=reviewed_at,
        note=note,
        trust_label_before=original.trust_label,
        trust_label_after=updated.trust_label,
        verification_status_before=original.verification_status,
        verification_status_after=updated.verification_status,
        analysis_effect=_review_analysis_effect(request.decision),
    )
    return updated.model_copy(update={"review_history": [*original.review_history, entry]}, deep=True)


def _review_event_id(
    case_id: str | None,
    evidence_id: str,
    decision: str,
    reviewed_at: datetime,
    existing_history_count: int,
) -> str:
    raw = f"{case_id or ''}|{evidence_id}|{decision}|{reviewed_at.isoformat()}|{existing_history_count}"
    return f"review_{hashlib.sha256(raw.encode('utf-8')).hexdigest()[:20]}"


def _review_analysis_effect(decision: str) -> str:
    if decision == "reject":
        return "excluded_from_analysis"
    if decision == "mark_weak":
        return "weak_evidence"
    if decision == "merge_duplicate":
        return "duplicate_collapsed"
    return "included_in_analysis"


def _sanitize_review_note(note: str | None) -> str | None:
    if not note:
        return None
    redacted = SECRET_TEXT_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", note.strip())
    redacted = _trim_text(redacted, 500)
    return redacted or None


def evidence_source_distribution(evidence_items: list[EvidenceItem]) -> dict[str, int]:
    return dict(Counter(item.source_type for item in enrich_and_deduplicate_evidence_items(evidence_items)))


def evidence_type_distribution(evidence_items: list[EvidenceItem]) -> dict[str, int]:
    return dict(Counter(item.evidence_type for item in enrich_and_deduplicate_evidence_items(evidence_items)))


def sanitize_raw_data(value: Any) -> Any:
    if isinstance(value, dict):
        safe: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if _is_secret_key(key_text):
                continue
            else:
                safe[key_text] = sanitize_raw_data(item)
        return safe
    if isinstance(value, list):
        return [sanitize_raw_data(item) for item in value]
    return value


def _has_reviewable_text(item: EvidenceItem) -> bool:
    return any((value or "").strip() for value in (item.title, item.body_text, item.comment_text))


def _redact_manual_text_fields(item: EvidenceItem) -> tuple[EvidenceItem, list[str]]:
    updates: dict[str, str] = {}
    warnings: list[str] = []
    for field_name in MANUAL_TEXT_FIELDS:
        value = getattr(item, field_name, None)
        if not isinstance(value, str) or not value:
            continue
        redacted = SECRET_TEXT_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", value)
        if redacted != value:
            updates[field_name] = redacted
            warnings.append(f"secret_like_text_redacted:{field_name}")

    if not updates:
        return item, warnings
    return item.model_copy(update=updates, deep=True), _dedupe_warnings(warnings)


def _dedupe_warnings(warnings: list[str]) -> list[str]:
    values: list[str] = []
    for warning in warnings:
        if warning and warning not in values:
            values.append(warning)
    return values


def _source_type_for_platform(platform: str) -> EvidenceSourceType:
    normalized = (platform or "").lower()
    if normalized in DIRECT_SOURCE_TYPES:
        return normalized  # type: ignore[return-value]
    if normalized in NEWS_PLATFORMS:
        return "news_site"
    if normalized in FORUM_PLATFORMS:
        return "forum"
    if normalized in {"mock", "mock_data"}:
        return "mock"
    if normalized in {"csv", "excel", "uploaded_dataset"}:
        return "uploaded_dataset"
    return "public_web"


def _acquisition_mode(
    platform: str,
    raw_data: dict[str, Any],
    metadata: PlatformCrawlMetadata | None,
) -> EvidenceAcquisitionMode:
    raw_source_type = str(raw_data.get("source_type", "")).lower()
    raw_mode = str(raw_data.get("mode", "")).lower()
    if metadata and metadata.source_type == "youtube_data_api_v3" and not metadata.fallback_used:
        return "official_api_public"
    if platform.lower() == "youtube" and raw_source_type == "youtube_data_api_v3" and raw_mode == "real":
        return "official_api_public"
    if raw_source_type == "public_page_parser" or raw_mode.startswith("public_parser"):
        return "public_parser"
    if raw_mode == "mock" or (metadata and metadata.fallback_used):
        return "mock_fixture"
    if platform.lower() == "youtube":
        return "official_api_public" if raw_source_type == "youtube_data_api_v3" else "mock_fixture"
    return "mock_fixture"


def _provenance_for_acquisition(acquisition_mode: EvidenceAcquisitionMode) -> str:
    if acquisition_mode in {"official_api_public", "official_api_oauth"}:
        return "official_api"
    if acquisition_mode == "public_parser":
        return "public_parser"
    if acquisition_mode == "search_discovery":
        return "search_discovery_candidate"
    if acquisition_mode == "manual_url":
        return "manual_url"
    if acquisition_mode == "data_vendor":
        return "data_vendor"
    if acquisition_mode == "mock_fixture":
        return "mock_fixture"
    return "user_upload"


def _resolve_provenance_type(item: EvidenceItem) -> str:
    inferred = _provenance_for_acquisition(item.acquisition_mode)
    if item.provenance_type == "user_upload" and inferred != "user_upload":
        return inferred
    capture_method = (item.source_capture_method or "").strip().lower()
    if capture_method in {"screenshot", "screenshot_transcription", "screen_capture"}:
        return "screenshot_transcription"
    return item.provenance_type or inferred


def _capture_method_for_provenance(provenance_type: str) -> str:
    if provenance_type == "official_api":
        return "official_api"
    if provenance_type == "public_parser":
        return "public_parser_fixture_or_reviewed_parser"
    if provenance_type == "manual_url":
        return "manual_entry_with_source_url"
    if provenance_type == "manual_text":
        return "manual_text_entry"
    if provenance_type == "screenshot_transcription":
        return "screenshot_transcription"
    if provenance_type == "search_discovery_candidate":
        return "search_result_metadata"
    if provenance_type == "data_vendor":
        return "vendor_dataset"
    if provenance_type == "mock_fixture":
        return "mock_fixture"
    return "user_upload"


def _trust_assessment(
    item: EvidenceItem,
    *,
    provenance_type: str,
    source_url_present: bool,
    risk_flags: list[str],
) -> tuple[str, float, str, list[str]]:
    notes: list[str] = []
    verification_status = item.verification_status
    trust_score = float(item.trust_score or 0)

    has_attestation = bool((item.user_attestation_text or "").strip())
    if provenance_type == "official_api":
        verification_status = "verified_by_official_api"
        trust_score = 0.92
        notes.append("Official API metadata is treated as high-trust source evidence, not a truth guarantee.")
    elif provenance_type == "public_parser":
        verification_status = "verified_by_public_parser"
        trust_score = 0.78
        notes.append("Reviewed public parser output is medium/high trust and still human-reviewable.")
    elif provenance_type == "data_vendor":
        verification_status = "vendor_attested"
        trust_score = 0.72
        notes.append("Vendor-provided evidence is vendor-attested and requires vendor contract review.")
    elif provenance_type == "mock_fixture":
        verification_status = "mock_fixture"
        trust_score = 0.5
        notes.append("Mock fixture evidence is deterministic demo data.")
    elif provenance_type == "screenshot_transcription":
        verification_status = "screenshot_unverified"
        trust_score = 0.2
        notes.append("Screenshot/transcribed evidence is never automatically verified.")
    elif provenance_type == "search_discovery_candidate":
        verification_status = "needs_review"
        trust_score = 0.18
        notes.append("Search discovery candidates are URL/title/snippet leads only until reviewed.")
    elif provenance_type == "manual_url":
        if source_url_present and has_attestation:
            verification_status = "source_url_provided_unverified"
            trust_score = 0.62
        elif source_url_present:
            verification_status = "source_url_provided_unverified"
            trust_score = 0.48
        elif has_attestation:
            verification_status = "user_attested_unverified"
            trust_score = 0.42
        else:
            verification_status = "needs_review"
            trust_score = 0.25
        notes.append("Manual URL evidence is user-provided and must remain reviewable.")
    else:
        if source_url_present and has_attestation:
            verification_status = "user_attested_unverified"
            trust_score = 0.55
        elif has_attestation:
            verification_status = "user_attested_unverified"
            trust_score = 0.42
        else:
            verification_status = "needs_review"
            trust_score = 0.25
        notes.append("User-uploaded evidence is not independently verified by Sentigraph.")

    if "possible_secret_redacted" in risk_flags:
        notes.append("Secret-like content was redacted before storage/output.")
    if "raw_html_script_like_input" in risk_flags:
        notes.append("HTML/script-like input is stored as plain text only and is not executed.")
    if "user_attestation_missing" in risk_flags:
        trust_score = min(trust_score, 0.35)
    if "suspiciously_short_content" in risk_flags:
        trust_score = min(trust_score, 0.4)
    if "unsupported_platform_claim" in risk_flags:
        trust_score = min(trust_score, 0.35)

    trust_label = _trust_label_for_score(trust_score, verification_status, risk_flags)
    return verification_status, round(trust_score, 3), trust_label, notes


def _trust_label_for_score(trust_score: float, verification_status: str, risk_flags: list[str]) -> str:
    if verification_status == "rejected":
        return "rejected"
    if verification_status in {"needs_review", "screenshot_unverified"}:
        return "unverified"
    if "user_attestation_missing" in risk_flags and trust_score < 0.5:
        return "unverified"
    if trust_score >= 0.8:
        return "high"
    if trust_score >= 0.55:
        return "medium"
    if trust_score >= 0.35:
        return "low"
    return "unverified"


def _risk_flags(item: EvidenceItem, *, provenance_type: str, source_url_present: bool) -> list[str]:
    flags = list(item.risk_flags)
    text = _evidence_text(item)
    lowered_text = text.lower()
    metadata_warnings = item.ingestion_metadata.warnings
    if not source_url_present and provenance_type in {"manual_url", "manual_text", "screenshot_transcription", "user_upload"}:
        flags.append("source_url_missing")
    if provenance_type == "screenshot_transcription":
        flags.append("screenshot_unverified")
    if item.created_at in {None, ""}:
        flags.append("missing_timestamp")
    if any("secret_like_text_redacted" in warning for warning in metadata_warnings):
        flags.append("possible_secret_redacted")
    if "<script" in lowered_text or "</script" in lowered_text or re.search(r"<[a-z][^>]*>", lowered_text):
        flags.append("raw_html_script_like_input")
    if _is_short_content(item, text):
        flags.append("suspiciously_short_content")
    platform_claim = (item.source_platform_claim or item.platform or "").strip().lower()
    if platform_claim and platform_claim not in SUPPORTED_PLATFORM_CLAIMS:
        flags.append("unsupported_platform_claim")
    if provenance_type in {"manual_url", "manual_text", "screenshot_transcription", "user_upload"} and not (item.user_attestation_text or "").strip():
        flags.append("user_attestation_missing")
    return _dedupe_warnings(flags)


def _is_short_content(item: EvidenceItem, text: str) -> bool:
    if item.evidence_type == "interaction_metric":
        return False
    normalized = _normalize_content_text(text)
    return bool(normalized) and len(normalized) < 8


def _content_hash(item: EvidenceItem, *, canonical_url: str) -> str:
    payload = {
        "platform": item.platform,
        "source_type": item.source_type,
        "evidence_type": item.evidence_type,
        "title": item.title or "",
        "body_text": item.body_text or "",
        "comment_text": item.comment_text or "",
        "parent_id": item.parent_id or "",
        "root_id": item.root_id or "",
        "url": canonical_url,
        "created_at": item.created_at or "",
    }
    return _hash_text(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _normalized_content_hash(item: EvidenceItem, *, canonical_url: str) -> str:
    payload = {
        "platform": (item.platform or "").strip().lower(),
        "source_type": item.source_type,
        "evidence_type": item.evidence_type,
        "text": _normalize_content_text(_evidence_text(item)),
        "url": canonical_url,
    }
    return _hash_text(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _canonicalize_url(value: str | None) -> str:
    if not value:
        return ""
    text = SECRET_TEXT_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", str(value).strip())
    if not text:
        return ""
    parsed = urlsplit(text)
    if not parsed.scheme or not parsed.netloc:
        return text
    query_pairs = []
    for key, item_value in parse_qsl(parsed.query, keep_blank_values=True):
        lowered_key = key.lower()
        if lowered_key.startswith("utm_") or lowered_key in TRACKING_QUERY_KEYS:
            continue
        query_pairs.append((key, item_value))
    query = urlencode(query_pairs, doseq=True)
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/") or parsed.path,
            query,
            "",
        )
    )


def _hash_text(value: str) -> str:
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def _evidence_text(item: EvidenceItem) -> str:
    return " ".join(
        value
        for value in (item.title, item.body_text, item.comment_text, item.url)
        if isinstance(value, str) and value.strip()
    )


def _normalize_content_text(value: str) -> str:
    return " ".join(str(value or "").casefold().split())


def _metadata(
    *,
    normalized_from: str,
    source_record_id: str | None,
    source_type: EvidenceSourceType,
    acquisition_mode: EvidenceAcquisitionMode,
    warnings: list[str] | None = None,
) -> EvidenceNormalizationMetadata:
    return EvidenceNormalizationMetadata(
        normalized_from=normalized_from,
        source_record_id=source_record_id,
        source_type=source_type,
        acquisition_mode=acquisition_mode,
        warnings=warnings or [],
    )


def _manual_evidence_type(item: EvidenceItem) -> str:
    if item.comment_text:
        return "comment"
    if item.title and item.body_text:
        return "article"
    if item.title:
        return "title"
    return "body_text"


def _dominant_source_type(evidence_items: list[EvidenceItem]) -> EvidenceSourceType:
    if not evidence_items:
        return "uploaded_dataset"
    return Counter(item.source_type for item in evidence_items).most_common(1)[0][0]  # type: ignore[return-value]


def _dominant_acquisition_mode(evidence_items: list[EvidenceItem]) -> EvidenceAcquisitionMode:
    if not evidence_items:
        return "user_upload"
    return Counter(item.acquisition_mode for item in evidence_items).most_common(1)[0][0]  # type: ignore[return-value]


def _top_titles(evidence_items: list[EvidenceItem]) -> list[str]:
    titles: list[str] = []
    for item in evidence_items:
        title = (item.title or "").strip()
        if title and title not in titles:
            titles.append(title)
        if len(titles) >= 5:
            break
    return titles


def _representative_comments(evidence_items: list[EvidenceItem]) -> list[str]:
    comments: list[str] = []
    for item in evidence_items:
        text = (item.comment_text or item.body_text or "").strip()
        if text and text not in comments:
            comments.append(text)
        if len(comments) >= 5:
            break
    return comments


def _evidence_id(platform: str, evidence_type: str, record_id: str) -> str:
    safe_platform = _safe_token(platform or "source")
    safe_type = _safe_token(evidence_type or "evidence")
    safe_record = _safe_token(record_id or "item")
    return f"evidence_{safe_platform}_{safe_type}_{safe_record}"


def _unique_evidence_id(evidence_id: str, used_ids: set[str]) -> str:
    base_id = evidence_id or "evidence_item"
    if base_id not in used_ids:
        return base_id
    suffix = 2
    while f"{base_id}_{suffix}" in used_ids:
        suffix += 1
    return f"{base_id}_{suffix}"


def _safe_token(value: str) -> str:
    return "".join(char.lower() if char.isalnum() else "_" for char in str(value)).strip("_") or "item"


def _is_secret_key(key: str) -> bool:
    lowered = key.lower()
    return any(marker in lowered for marker in SECRET_KEY_MARKERS)


def _infer_language(*values: str | None) -> str:
    joined = " ".join(value for value in values if value)
    if any("\u4e00" <= char <= "\u9fff" for char in joined):
        return "zh-CN"
    if joined:
        return "en-US"
    return "unknown"


def _trim_text(value: str, length: int) -> str:
    text = " ".join(str(value).split())
    return text[:length]
