from __future__ import annotations

from typing import Iterable

from pydantic import ValidationError

from app.schemas.comment import RawComment, RawPost
from app.schemas.crawl import CrawlStartRequest, CrawlStartResponse, PlatformCrawlMetadata
from app.services.crawling import adapter_factory
from app.services.crawling.base_adapter import BasePlatformAdapter, PlatformAdapterError
from app.services.crawling.bilibili_adapter import BilibiliAdapter
from app.services.crawling.douyin_adapter import DouyinAdapter
from app.services.crawling.kuaishou_adapter import KuaishouAdapter
from app.services.crawling.public_parser.parser_registry import get_public_parser_platform_ids
from app.services.crawling.reddit_adapter import RedditAdapter
from app.services.crawling.weibo_adapter import WeiboAdapter
from app.services.crawling.xiaohongshu_adapter import XiaohongshuAdapter


SAFE_BILIBILI_POST_LIMIT = 3
SAFE_BILIBILI_COMMENT_LIMIT = 3
SAFE_DOUYIN_POST_LIMIT = 3
SAFE_DOUYIN_COMMENT_LIMIT = 3
SAFE_KUAISHOU_POST_LIMIT = 3
SAFE_KUAISHOU_COMMENT_LIMIT = 3
SAFE_REDDIT_POST_LIMIT = 3
SAFE_REDDIT_COMMENT_LIMIT = 3
SAFE_WEIBO_POST_LIMIT = 3
SAFE_WEIBO_COMMENT_LIMIT = 3
SAFE_XIAOHONGSHU_POST_LIMIT = 3
SAFE_XIAOHONGSHU_COMMENT_LIMIT = 3
SAFE_PUBLIC_PARSER_POST_LIMIT = 3
SAFE_PUBLIC_PARSER_COMMENT_LIMIT = 3


def start_crawl_with_adapters(payload: CrawlStartRequest) -> CrawlStartResponse:
    platforms = _normalize_platforms(payload.platforms)
    raw_posts: list[RawPost] = []
    raw_comments: list[RawComment] = []
    metadata: list[PlatformCrawlMetadata] = []

    if "reddit" in platforms:
        reddit_posts, reddit_comments, reddit_metadata = _crawl_reddit(payload)
        raw_posts.extend(reddit_posts)
        raw_comments.extend(reddit_comments)
        metadata.append(reddit_metadata)

    if "bilibili" in platforms:
        bilibili_posts, bilibili_comments, bilibili_metadata = _crawl_bilibili(payload)
        raw_posts.extend(bilibili_posts)
        raw_comments.extend(bilibili_comments)
        metadata.append(bilibili_metadata)

    if "douyin" in platforms:
        douyin_posts, douyin_comments, douyin_metadata = _crawl_douyin(payload)
        raw_posts.extend(douyin_posts)
        raw_comments.extend(douyin_comments)
        metadata.append(douyin_metadata)

    if "kuaishou" in platforms:
        kuaishou_posts, kuaishou_comments, kuaishou_metadata = _crawl_kuaishou(payload)
        raw_posts.extend(kuaishou_posts)
        raw_comments.extend(kuaishou_comments)
        metadata.append(kuaishou_metadata)

    if "xiaohongshu" in platforms:
        xiaohongshu_posts, xiaohongshu_comments, xiaohongshu_metadata = _crawl_xiaohongshu(payload)
        raw_posts.extend(xiaohongshu_posts)
        raw_comments.extend(xiaohongshu_comments)
        metadata.append(xiaohongshu_metadata)

    if "weibo" in platforms:
        weibo_posts, weibo_comments, weibo_metadata = _crawl_weibo(payload)
        raw_posts.extend(weibo_posts)
        raw_comments.extend(weibo_comments)
        metadata.append(weibo_metadata)

    for platform_id in get_public_parser_platform_ids():
        if platform_id in platforms:
            parser_posts, parser_comments, parser_metadata = _crawl_public_parser(platform_id, payload)
            raw_posts.extend(parser_posts)
            raw_comments.extend(parser_comments)
            metadata.append(parser_metadata)

    message = "Mock crawl task queued. Real crawlers are not enabled in MVP."
    if metadata:
        message = "Crawl task queued with platform adapter metadata. Mock-first fallback remains enabled."

    return CrawlStartResponse(
        project_id="project_001",
        crawl_task_id="crawl_task_001",
        status="queued",
        message=message,
        platform_metadata=metadata,
        raw_posts=raw_posts,
        raw_comments=raw_comments,
    )


def _crawl_douyin(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_DOUYIN_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_DOUYIN_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("douyin")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _douyin_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _douyin_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="douyin",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")) or "official_api_adapter_scaffold",
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", True)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", True)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_bilibili(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_BILIBILI_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_BILIBILI_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("bilibili")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _bilibili_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _bilibili_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="bilibili",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")) or "official_api_adapter_scaffold",
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", True)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", True)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_kuaishou(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_KUAISHOU_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_KUAISHOU_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("kuaishou")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _kuaishou_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _kuaishou_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="kuaishou",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")) or "official_api_adapter_scaffold",
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", True)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", True)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_xiaohongshu(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_XIAOHONGSHU_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_XIAOHONGSHU_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("xiaohongshu")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _xiaohongshu_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _xiaohongshu_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="xiaohongshu",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")) or "official_api_adapter_scaffold",
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", True)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", True)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_weibo(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_WEIBO_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_WEIBO_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("weibo")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _weibo_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _weibo_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="weibo",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")) or "official_api_adapter_scaffold",
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", True)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", True)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_reddit(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_REDDIT_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_REDDIT_COMMENT_LIMIT)

    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter("reddit")
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)

        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _reddit_mock_fallback(payload)
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
        posts, comments = _reddit_mock_fallback(payload)

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_mode = _adapter_mode(adapter, fallback_reason)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("sanitized_error_category")
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform="reddit",
            adapter_mode=adapter_mode,
            source_type=_safe_str(adapter_status.get("source_type")),
            parser_status=_safe_str(adapter_status.get("parser_status")),
            live_fetch_enabled=bool(adapter_status.get("live_fetch_enabled", False)),
            live_fetch_attempted=bool(adapter_status.get("live_fetch_attempted", False)),
            live_fetch_allowed=bool(adapter_status.get("live_fetch_allowed", False)),
            fallback_used=fallback_used,
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", False)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", False)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", False)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=_real_mode_blocked_reason(fallback_reason, adapter_status, adapter_mode),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=post_schema_valid and comment_schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _crawl_public_parser(
    platform_id: str,
    payload: CrawlStartRequest,
) -> tuple[list[RawPost], list[RawComment], PlatformCrawlMetadata]:
    post_limit = min(payload.limit, SAFE_PUBLIC_PARSER_POST_LIMIT)
    comment_limit = min(payload.limit, SAFE_PUBLIC_PARSER_COMMENT_LIMIT)
    posts: list[RawPost] = []
    comments: list[RawComment] = []
    adapter: BasePlatformAdapter | None = None
    fallback_reason: str | None = None
    fallback_used = False

    try:
        adapter = adapter_factory.get_adapter(platform_id)
        posts = adapter.search_posts(
            keyword=payload.keyword,
            limit=post_limit,
            sort="new",
            date_range=_serialize_date_range(payload),
        )
        fallback_reason = getattr(adapter, "fallback_reason", None)
        fallback_used = bool(fallback_reason)
        if posts:
            comments = adapter.fetch_comments(posts[0].post_id, limit=comment_limit)
            fallback_reason = getattr(adapter, "fallback_reason", None) or fallback_reason
            fallback_used = bool(fallback_reason)
    except PlatformAdapterError as exc:
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None
    except Exception as exc:  # pragma: no cover - last-resort safety guard
        fallback_reason = f"adapter_error:{exc.__class__.__name__}"
        fallback_used = True
        adapter = None

    post_schema_valid = _validate_items(posts, RawPost)
    comment_schema_valid = _validate_items(comments, RawComment)
    adapter_status = _adapter_status_metadata(adapter)
    fallback_category = _fallback_reason_category(fallback_reason) or _safe_str(
        adapter_status.get("fallback_reason_category")
    )
    parser_status = _safe_str(adapter_status.get("parser_status")) or "fixture_only"
    live_fetch_enabled = bool(adapter_status.get("live_fetch_enabled", False))
    live_fetch_attempted = bool(adapter_status.get("live_fetch_attempted", False))
    live_fetch_allowed = bool(adapter_status.get("live_fetch_allowed", False))
    schema_valid = bool(
        adapter_status.get("schema_valid", post_schema_valid and comment_schema_valid)
    )

    return (
        posts,
        comments,
        PlatformCrawlMetadata(
            platform=platform_id,
            adapter_mode=_adapter_mode(adapter, fallback_reason),
            source_type=_safe_str(adapter_status.get("source_type")) or "public_page_parser",
            parser_status=parser_status,
            live_fetch_enabled=live_fetch_enabled,
            live_fetch_attempted=live_fetch_attempted,
            live_fetch_allowed=live_fetch_allowed,
            fallback_used=fallback_used or bool(adapter_status.get("fallback_used", False)),
            fallback_reason_category=fallback_category,
            fetch_status=_safe_str(adapter_status.get("fetch_status")),
            mock_available=bool(adapter_status.get("mock_available", True)),
            real_mode_available=bool(adapter_status.get("real_mode_available", False)),
            api_approval_required=bool(adapter_status.get("api_approval_required", False)),
            api_approval_status=_safe_str(adapter_status.get("api_approval_status")),
            api_pending=bool(adapter_status.get("api_pending", False)),
            real_mode_disabled=bool(adapter_status.get("real_mode_disabled", True)),
            selectable_for_real=bool(adapter_status.get("selectable_for_real", False)),
            real_mode_blocked_reason=(
                "live_fetch_disabled" if not live_fetch_enabled else "mock_only"
            ),
            real_mode_reached=bool(adapter_status.get("real_mode_reached", False)),
            dependency_available=bool(adapter_status.get("dependency_available", True)),
            exception_class=_safe_str(adapter_status.get("exception_class")),
            sanitized_error_category=fallback_category,
            post_count=len(posts),
            comment_count=len(comments),
            schema_valid=schema_valid,
            raw_post_schema_valid=post_schema_valid,
            raw_comment_schema_valid=comment_schema_valid,
        ),
    )


def _normalize_platforms(platforms: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    normalized: list[str] = []
    for platform in platforms:
        platform_id = platform.strip().lower()
        if platform_id and platform_id not in seen:
            seen.add(platform_id)
            normalized.append(platform_id)
    return normalized


def _reddit_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = RedditAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_REDDIT_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_REDDIT_COMMENT_LIMIT))
    return posts, comments


def _bilibili_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = BilibiliAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_BILIBILI_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_BILIBILI_COMMENT_LIMIT))
    return posts, comments


def _douyin_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = DouyinAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_DOUYIN_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_DOUYIN_COMMENT_LIMIT))
    return posts, comments


def _kuaishou_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = KuaishouAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_KUAISHOU_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_KUAISHOU_COMMENT_LIMIT))
    return posts, comments


def _xiaohongshu_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = XiaohongshuAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_XIAOHONGSHU_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_XIAOHONGSHU_COMMENT_LIMIT))
    return posts, comments


def _weibo_mock_fallback(payload: CrawlStartRequest) -> tuple[list[RawPost], list[RawComment]]:
    mock_adapter = WeiboAdapter(mode="mock")
    posts = mock_adapter.search_posts(
        keyword=payload.keyword,
        limit=min(payload.limit, SAFE_WEIBO_POST_LIMIT),
        sort="new",
        date_range=_serialize_date_range(payload),
    )
    comments: list[RawComment] = []
    if posts:
        comments = mock_adapter.fetch_comments(posts[0].post_id, limit=min(payload.limit, SAFE_WEIBO_COMMENT_LIMIT))
    return posts, comments


def _serialize_date_range(payload: CrawlStartRequest) -> dict[str, str] | None:
    if payload.date_range is None:
        return None
    return payload.date_range.model_dump(mode="json")


def _validate_items(items: list[object], model: type[RawPost] | type[RawComment]) -> bool:
    try:
        for item in items:
            if hasattr(item, "model_dump"):
                model.model_validate(item.model_dump(mode="json"))
            else:
                model.model_validate(item)
    except ValidationError:
        return False
    return True


def _adapter_mode(adapter: BasePlatformAdapter | None, fallback_reason: str | None) -> str:
    if adapter is not None and hasattr(adapter, "get_mode"):
        return str(adapter.get_mode())
    if fallback_reason and "missing" in fallback_reason.lower():
        return "mock"
    return "mock"


def _adapter_status_metadata(adapter: BasePlatformAdapter | None) -> dict[str, object]:
    if adapter is None or not hasattr(adapter, "get_status_metadata"):
        return {}
    metadata = adapter.get_status_metadata()
    return metadata if isinstance(metadata, dict) else {}


def _safe_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _fallback_reason_category(fallback_reason: str | None) -> str | None:
    if not fallback_reason:
        return None

    reason = fallback_reason.lower()
    prefix = reason.split(":", 1)[0]
    if prefix in {
        "dependency_error",
        "auth_error",
        "network_error",
        "parsing_error",
        "adapter_error",
        "config_error",
        "api_pending",
        "fixture_only",
        "live_fetch_disabled",
        "selector_missing",
        "robots_disallowed",
        "robots_unavailable_or_unclear",
        "path_not_allowed_by_profile",
        "http_error",
    }:
        return prefix
    if "approval_pending" in reason or "api_pending" in reason:
        return "api_pending"
    if "missing" in reason or "config" in reason or "mode_not_real" in reason:
        return "config_error"
    if "dependency" in reason or "modulenotfound" in reason or "importerror" in reason:
        return "dependency_error"
    if "auth" in reason or "permission" in reason or "unauthorized" in reason or "forbidden" in reason:
        return "auth_error"
    if "timeout" in reason or "connection" in reason or "network" in reason or "urlerror" in reason:
        return "network_error"
    if "parsing" in reason or "jsondecode" in reason or "validation" in reason:
        return "parsing_error"
    return "adapter_error"


def _real_mode_blocked_reason(
    fallback_reason: str | None,
    adapter_status: dict[str, object],
    adapter_mode: str,
) -> str | None:
    reason = (fallback_reason or "").lower()
    if "missing" in reason:
        return "credentials_missing"
    if "approval_pending" in reason or adapter_status.get("api_pending") is True:
        if reason:
            return "api_pending"
        return "mock_only" if adapter_mode == "mock" else "api_pending"
    if adapter_status.get("real_mode_disabled") is True:
        return "disabled"
    if adapter_mode == "mock":
        return "mock_only"
    return None
