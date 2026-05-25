from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import re
from typing import Any

from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import PlatformCrawlMetadata
from app.schemas.evidence import (
    EvidenceAcquisitionMode,
    EvidenceIngestionBatch,
    EvidenceIngestionResult,
    EvidenceItem,
    EvidenceNormalizationMetadata,
    EvidenceSourceType,
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
    return items


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
    return EvidenceItem(
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
        ingestion_metadata=_metadata(
            normalized_from="raw_post",
            source_record_id=record_id,
            source_type=source_type,
            acquisition_mode=acquisition_mode,
        ),
    )


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
    return EvidenceItem(
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
        ingestion_metadata=_metadata(
            normalized_from="raw_comment",
            source_record_id=record_id,
            source_type=source_type,
            acquisition_mode=acquisition_mode,
        ),
    )


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
                    "ingestion_metadata": normalized_metadata,
                },
                deep=True,
            )
        )
    return items


def evidence_items_to_raw_data(evidence_items: list[EvidenceItem]) -> tuple[list[RawPost], list[RawComment]]:
    posts: list[RawPost] = []
    comments: list[RawComment] = []
    post_ids: set[str] = set()
    now = datetime.now(timezone.utc).isoformat()

    for item in evidence_items:
        platform = item.platform or "uploaded_dataset"
        root_id = item.root_id or item.evidence_id or f"evidence_{len(posts) + 1}"
        raw_data = {
            "source_type": item.source_type,
            "acquisition_mode": item.acquisition_mode,
            "evidence_id": item.evidence_id,
            "normalized_evidence": True,
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
    source_distribution = evidence_source_distribution(evidence_items)
    evidence_type_counts = evidence_type_distribution(evidence_items)
    top_titles = _top_titles(evidence_items)
    representative_comments = _representative_comments(evidence_items)
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
        ingestion_metadata=_metadata(
            normalized_from="evidence_batch",
            source_record_id=case_id,
            source_type=_dominant_source_type(evidence_items),
            acquisition_mode=_dominant_acquisition_mode(evidence_items),
        ),
        warnings=result_warnings,
    )


def evidence_source_distribution(evidence_items: list[EvidenceItem]) -> dict[str, int]:
    return dict(Counter(item.source_type for item in evidence_items))


def evidence_type_distribution(evidence_items: list[EvidenceItem]) -> dict[str, int]:
    return dict(Counter(item.evidence_type for item in evidence_items))


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
