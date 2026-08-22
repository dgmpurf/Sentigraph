from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

import httpx

from app.schemas.comment import RawComment, RawPost
from app.services.crawling.base_adapter import (
    AdapterHealth,
    AdapterMode,
    BasePlatformAdapter,
    PlatformAdapterError,
)
from app.services.crawling.youtube_cache import YouTubeAdapterConfig, YouTubeResponseCache


YOUTUBE_REQUIRED_CREDENTIALS = ("YOUTUBE_API_KEY",)
YOUTUBE_API_APPROVAL_STATUS = "api_key_configurable"
YOUTUBE_MOCK_POST_LIMIT = 100
YOUTUBE_MOCK_COMMENT_LIMIT = 500
YOUTUBE_REAL_POST_LIMIT = 5
YOUTUBE_REAL_COMMENT_LIMIT = 20
YOUTUBE_SEARCH_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_COMMENT_THREADS_ENDPOINT = "https://www.googleapis.com/youtube/v3/commentThreads"
YOUTUBE_SOURCE_TYPE = "youtube_data_api_v3"


class YouTubeRealModeError(PlatformAdapterError):
    category = "adapter_error"


class YouTubeAuthError(YouTubeRealModeError):
    category = "auth_error"


class YouTubeNetworkError(YouTubeRealModeError):
    category = "network_error"


class YouTubeQuotaError(YouTubeRealModeError):
    category = "quota_error"


class YouTubeCommentsDisabledError(YouTubeRealModeError):
    category = "comments_unavailable"


class YouTubeParsingError(YouTubeRealModeError):
    category = "parsing_error"


class YouTubeHttpClient(Protocol):
    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        ...

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        ...


class ClosableYouTubeHttpClient(YouTubeHttpClient, Protocol):
    def close(self) -> None:
        ...


@dataclass(frozen=True)
class YouTubeCredentials:
    api_key: str

    @classmethod
    def from_env(cls) -> "YouTubeCredentials | None":
        api_key = os.getenv("YOUTUBE_API_KEY", "").strip()
        if not api_key:
            return None
        return cls(api_key=api_key)


def search_youtube_official_api_live_metadata(
    keyword: str,
    *,
    credentials: YouTubeCredentials,
    http_client: YouTubeHttpClient,
    limit: int = YOUTUBE_REAL_POST_LIMIT,
) -> list[Mapping[str, Any]]:
    """Return bounded official video metadata through an injected client.

    This narrow Search Discovery boundary intentionally bypasses adapter mode,
    environment, cache, comment, and mock-fallback behavior.  Callers must
    resolve credentials and construct the official-search client explicitly.
    """

    if not isinstance(credentials, YouTubeCredentials) or not credentials.api_key.strip():
        raise YouTubeAuthError("youtube_explicit_credentials_required")

    safe_keyword = str(keyword).strip()
    if not safe_keyword:
        raise YouTubeParsingError("youtube_search_keyword_required")
    try:
        safe_limit = max(1, min(int(limit), YOUTUBE_REAL_POST_LIMIT))
    except (TypeError, ValueError) as exc:
        raise YouTubeParsingError("youtube_search_limit_invalid") from exc

    try:
        raw_posts = http_client.search_posts(
            safe_keyword,
            limit=safe_limit,
            sort="relevance",
            date_range=None,
        )
    except YouTubeRealModeError:
        raise
    except Exception as exc:
        raise _typed_youtube_exception(exc) from exc

    if not isinstance(raw_posts, list) or any(not isinstance(post, Mapping) for post in raw_posts):
        raise YouTubeParsingError("youtube_search_result_not_metadata_list")
    return list(raw_posts[:safe_limit])


class YouTubeAdapter(BasePlatformAdapter):
    platform_id = "youtube"
    display_name = "YouTube"

    def __init__(
        self,
        *,
        mode: AdapterMode | None = None,
        credentials: YouTubeCredentials | None = None,
        http_client: YouTubeHttpClient | None = None,
        config: YouTubeAdapterConfig | None = None,
        cache: YouTubeResponseCache | None = None,
    ) -> None:
        from app.core.environment import load_project_env

        load_project_env()
        self.env_mode: AdapterMode = _adapter_mode_from_env()
        self.requested_mode: AdapterMode = self.env_mode if mode is None else _normalize_adapter_mode(mode)
        self.credentials = credentials or YouTubeCredentials.from_env()
        self.config = config or YouTubeAdapterConfig.from_env()
        self.cache = cache or YouTubeResponseCache.from_config(self.config)
        self.fallback_reason = ""
        self.real_mode_reached = False
        self.exception_class: str | None = None
        self.sanitized_error_category: str | None = None
        self.mock_available = True
        self.api_pending = False
        self.real_mode_disabled = False
        self.api_approval_required = False
        self.api_approval_status = YOUTUBE_API_APPROVAL_STATUS
        self.search_call_count = 0
        self.videos_call_count = 0
        self.comment_threads_call_count = 0
        self.comments_call_count = 0
        self.cache_lookup_count = 0
        self.cache_hit_count = 0
        self.cache_age_seconds_values: list[int] = []

        env_allows_real = self.env_mode == "real"
        effective_mode: AdapterMode = (
            "real"
            if self.requested_mode == "real"
            and env_allows_real
            and self.credentials is not None
            else "mock"
        )
        if self.requested_mode == "real" and not env_allows_real:
            self.fallback_reason = "config_error:youtube_adapter_mode_not_real"
        elif self.requested_mode == "real" and self.credentials is None:
            self.fallback_reason = "config_error:missing_youtube_api_key"

        super().__init__(mode=effective_mode)
        self.http_client = http_client
        if self.http_client is None and self.mode == "real" and self.credentials is not None:
            self.http_client = _OfficialYouTubeClient(self.credentials)

    def has_required_credentials(self) -> bool:
        return self.credentials is not None

    def get_mode(self) -> AdapterMode:
        return self.mode

    def is_real_mode_enabled(self) -> bool:
        return self.mode == "real" and self.credentials is not None and self.http_client is not None

    def supports_real_mode(self) -> bool:
        return self.has_required_credentials()

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return YOUTUBE_REQUIRED_CREDENTIALS

    def health_check(self) -> AdapterHealth:
        if self.is_real_mode_enabled():
            message = "YouTube adapter real mode is configured for official Data API v3 access."
        elif self.requested_mode == "real" and self.fallback_reason:
            message = "YouTube real mode was requested but is using mock data because configuration is incomplete."
        else:
            message = "YouTube adapter mock mode is active."

        return AdapterHealth(
            platform_id=self.platform_id,
            mode=self.mode,
            ok=True,
            real_mode_available=self.supports_real_mode(),
            message=message,
            fallback_reason=self.fallback_reason,
        )

    def get_status_metadata(self) -> dict[str, object]:
        fallback_category = _fallback_reason_category(self.fallback_reason)
        credential_present = self.has_required_credentials()
        return {
            "platform_id": self.platform_id,
            "source_type": YOUTUBE_SOURCE_TYPE,
            "env_mode": self.env_mode,
            "requested_mode": self.requested_mode,
            "active_mode": self.mode,
            "has_required_credentials": credential_present,
            "credential_present": credential_present,
            "real_mode_enabled": self.is_real_mode_enabled(),
            "fallback_reason": self.fallback_reason,
            "required_credentials": list(self.get_required_credentials()),
            "mock_available": self.mock_available,
            "real_mode_available": credential_present,
            "api_approval_required": self.api_approval_required,
            "api_approval_status": self.api_approval_status,
            "api_pending": self.api_pending,
            "real_mode_disabled": self.real_mode_disabled,
            "selectable_for_real": credential_present,
            "real_mode_reached": self.real_mode_reached,
            "dependency_available": True,
            "exception_class": self.exception_class,
            "sanitized_error_category": self.sanitized_error_category or fallback_category,
            "fetch_status": self.sanitized_error_category or fallback_category or ("real" if self.is_real_mode_enabled() else "mock"),
            "real_mode_blocked_reason": _real_mode_blocked_reason(fallback_category, self.mode),
            "credentials_present": _credential_presence(),
            "estimated_quota_units": self.estimated_quota_units(),
            "search_call_count": self.search_call_count,
            "videos_call_count": self.videos_call_count,
            "comment_threads_call_count": self.comment_threads_call_count,
            "comments_call_count": self.comments_call_count,
            "cache_enabled": self.config.cache_enabled,
            "cache_hit": self.cache_lookup_count > 0 and self.cache_hit_count == self.cache_lookup_count,
            "cache_age_seconds": max(self.cache_age_seconds_values) if self.cache_age_seconds_values else None,
            "quota_guardrail_status": self.quota_guardrail_status(),
            "max_search_results": self.config.max_search_results,
            "max_comments_per_video": self.config.max_comments_per_video,
            "max_replies_per_comment": self.config.max_replies_per_comment,
            "max_total_comments": self.config.max_total_comments,
            "deep_replies_enabled": self.config.enable_deep_replies,
        }

    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        is_real = self.is_real_mode_enabled()
        safe_limit = self.clamp_limit(
            limit,
            default=3,
            maximum=self.config.max_search_results if is_real else YOUTUBE_MOCK_POST_LIMIT,
        )
        if not is_real:
            return [
                self.normalize_post(raw)
                for raw in _mock_youtube_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
            ]

        normalized_sort = _normalize_sort(sort)
        cache_key_params = {
            "keyword": keyword,
            "limit": safe_limit,
            "order": normalized_sort,
            "date_range": date_range or None,
        }
        cache_key = self.cache.build_key("search_posts", cache_key_params)
        cached = self.cache.get(cache_key)
        self._record_cache_lookup(cached)
        if cached.hit and cached.payload:
            return [
                RawPost.model_validate(raw_post)
                for raw_post in cached.payload.get("raw_posts", [])
                if isinstance(raw_post, Mapping)
            ][:safe_limit]

        try:
            self.real_mode_reached = True
            self.search_call_count += 1
            raw_posts = self.http_client.search_posts(
                keyword,
                limit=safe_limit,
                sort=normalized_sort,
                date_range=date_range,
            )
            if raw_posts:
                self.videos_call_count += 1
            posts = [self.normalize_post(raw) for raw in raw_posts[:safe_limit]]
            self.cache.set(
                cache_key,
                safe_key=cache_key_params,
                payload={
                    "raw_posts": [post.model_dump(mode="json") for post in posts],
                    "raw_comments": [],
                    "crawl_metadata": self._cache_metadata_snapshot(),
                },
                source_type=YOUTUBE_SOURCE_TYPE,
            )
            return posts
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self._record_real_mode_exception(exc)
            return [
                self.normalize_post(raw)
                for raw in _mock_youtube_posts(keyword=keyword, sort=sort, date_range=date_range)[:safe_limit]
            ]

    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        is_real = self.is_real_mode_enabled()
        safe_limit = self.clamp_limit(
            limit,
            default=10,
            maximum=(
                min(self.config.max_comments_per_video, self.config.max_total_comments)
                if is_real
                else YOUTUBE_MOCK_COMMENT_LIMIT
            ),
        )
        if not is_real:
            return [self.normalize_comment(raw) for raw in _mock_youtube_comments(post_id)[:safe_limit]]

        cache_key_params = {
            "video_id": post_id,
            "limit": safe_limit,
            "deep_replies_enabled": self.config.enable_deep_replies,
            "max_replies_per_comment": self.config.max_replies_per_comment,
            "max_total_comments": self.config.max_total_comments,
        }
        cache_key = self.cache.build_key("fetch_comments", cache_key_params)
        cached = self.cache.get(cache_key)
        self._record_cache_lookup(cached)
        if cached.hit and cached.payload:
            return [
                RawComment.model_validate(raw_comment)
                for raw_comment in cached.payload.get("raw_comments", [])
                if isinstance(raw_comment, Mapping)
            ][:safe_limit]

        try:
            self.real_mode_reached = True
            self.comment_threads_call_count += 1
            raw_comments = self.http_client.fetch_comments(post_id, limit=safe_limit)
            comments = self._apply_comment_guardrails(
                [self.normalize_comment(raw) for raw in raw_comments],
                limit=safe_limit,
            )
            self.cache.set(
                cache_key,
                safe_key=cache_key_params,
                payload={
                    "raw_posts": [],
                    "raw_comments": [comment.model_dump(mode="json") for comment in comments],
                    "crawl_metadata": self._cache_metadata_snapshot(),
                },
                source_type=YOUTUBE_SOURCE_TYPE,
            )
            return comments
        except Exception as exc:  # pragma: no cover - defensive fallback for live mode only
            self._record_real_mode_exception(exc)
            if self.sanitized_error_category == "comments_unavailable":
                return []
            return [self.normalize_comment(raw) for raw in _mock_youtube_comments(post_id)[:safe_limit]]

    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        payload = _video_payload(raw)
        snippet = payload.get("snippet") if isinstance(payload.get("snippet"), Mapping) else {}
        statistics = payload.get("statistics") if isinstance(payload.get("statistics"), Mapping) else {}
        raw_id = payload.get("video_id") or payload.get("id")
        video_id = self.safe_text(
            raw_id.get("videoId") if isinstance(raw_id, Mapping) else raw_id,
            default="youtube_unknown_video",
        )
        channel_id = self.safe_text(
            payload.get("channel_id") or snippet.get("channelId"),
            default="youtube_unknown_channel",
        )
        channel_title = self.safe_text(
            payload.get("channel_title") or snippet.get("channelTitle"),
            default="YouTube public channel",
        )
        published_at = self.to_utc_iso(payload.get("published_at") or snippet.get("publishedAt"))
        title = self.safe_text(payload.get("title") or snippet.get("title"), default="Untitled YouTube video")
        description = self.safe_text(payload.get("description") or snippet.get("description"), default=title)
        like_count = max(0, self.coerce_int(payload.get("like_count") or statistics.get("likeCount")))
        comment_count = max(0, self.coerce_int(payload.get("comment_count") or statistics.get("commentCount")))

        return RawPost(
            platform=self.platform_id,
            post_id=video_id,
            author_id=channel_id,
            author_name=channel_title,
            title=title,
            content=description,
            like_count=like_count,
            reply_count=comment_count,
            share_count=0,
            created_at=published_at,
            url=self.safe_text(payload.get("url"), default=f"https://www.youtube.com/watch?v={video_id}"),
            raw_data=self.sanitize_raw_data(
                {
                    "mode": payload.get("mode", "real" if self.is_real_mode_enabled() else "mock"),
                    "source_type": payload.get("source_type", YOUTUBE_SOURCE_TYPE),
                    "video_id": video_id,
                    "channel_id": channel_id,
                    "channel_title": channel_title,
                    "published_at": published_at,
                    "like_count": like_count,
                    "comment_count": comment_count,
                    "view_count": max(0, self.coerce_int(payload.get("view_count") or statistics.get("viewCount"))),
                }
            ),
        )

    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        payload = _comment_payload(raw)
        author_channel_id = payload.get("authorChannelId")
        if isinstance(author_channel_id, Mapping):
            author_channel_id = author_channel_id.get("value")
        post_id = self.safe_text(
            payload.get("post_id") or payload.get("videoId"),
            default="youtube_unknown_video",
        )
        comment_id = self.safe_text(
            payload.get("comment_id") or payload.get("id"),
            default="youtube_unknown_comment",
        )
        parent_id = self.safe_text(payload.get("parent_id") or payload.get("parentId")) or None
        published_at = self.to_utc_iso(payload.get("published_at") or payload.get("publishedAt"))
        like_count = max(0, self.coerce_int(payload.get("like_count") or payload.get("likeCount")))
        reply_count = max(0, self.coerce_int(payload.get("reply_count") or payload.get("totalReplyCount")))

        return RawComment(
            platform=self.platform_id,
            post_id=post_id,
            comment_id=comment_id,
            parent_id=parent_id,
            author_id=self.safe_text(
                payload.get("author_id") or author_channel_id,
                default="youtube_unknown_commenter",
            ),
            author_name=self.safe_text(
                payload.get("author_name") or payload.get("authorDisplayName"),
                default="YouTube public commenter",
            ),
            content=self.safe_text(payload.get("content") or payload.get("textOriginal") or payload.get("textDisplay")),
            like_count=like_count,
            reply_count=reply_count,
            share_count=0,
            created_at=published_at,
            url=self.safe_text(payload.get("url"), default=f"https://www.youtube.com/watch?v={post_id}&lc={comment_id}"),
            raw_data=self.sanitize_raw_data(
                {
                    "mode": payload.get("mode", "real" if self.is_real_mode_enabled() else "mock"),
                    "source_type": payload.get("source_type", YOUTUBE_SOURCE_TYPE),
                    "post_id": post_id,
                    "comment_id": comment_id,
                    "parent_id": parent_id,
                    "published_at": published_at,
                    "updated_at": self.to_utc_iso(payload.get("updated_at") or payload.get("updatedAt")),
                    "like_count": like_count,
                    "reply_count": reply_count,
                }
            ),
        )

    def _record_real_mode_exception(self, exc: Exception) -> None:
        category = _real_mode_error_category(exc)
        safe_exception = exc.__cause__ or exc
        self.sanitized_error_category = category
        self.exception_class = safe_exception.__class__.__name__
        self.fallback_reason = f"{category}:{self.exception_class}"

    def estimated_quota_units(self) -> int:
        return (
            self.search_call_count * 100
            + self.videos_call_count
            + self.comment_threads_call_count
            + self.comments_call_count
        )

    def quota_guardrail_status(self) -> str:
        if self.sanitized_error_category == "quota_error":
            return "quota_error_fallback"
        if self.sanitized_error_category == "comments_unavailable":
            return "comments_unavailable_partial"
        if not self.is_real_mode_enabled():
            return "real_mode_blocked" if self.requested_mode == "real" else "mock_mode"
        if self.cache_lookup_count:
            if self.cache_hit_count == self.cache_lookup_count:
                return "cache_hit"
            if self.cache_hit_count:
                return "partial_cache_hit"
            return "cache_miss_real_call"
        return "real_mode_ready"

    def _record_cache_lookup(self, lookup) -> None:
        if not self.config.cache_enabled:
            return
        self.cache_lookup_count += 1
        if lookup.hit:
            self.cache_hit_count += 1
            if lookup.cache_age_seconds is not None:
                self.cache_age_seconds_values.append(lookup.cache_age_seconds)

    def _apply_comment_guardrails(self, comments: list[RawComment], *, limit: int) -> list[RawComment]:
        total_limit = min(limit, self.config.max_total_comments)
        if self.config.enable_deep_replies:
            kept: list[RawComment] = []
            replies_by_parent: dict[str, int] = {}
            for comment in comments:
                if comment.parent_id:
                    current_reply_count = replies_by_parent.get(comment.parent_id, 0)
                    if current_reply_count >= self.config.max_replies_per_comment:
                        continue
                    replies_by_parent[comment.parent_id] = current_reply_count + 1
                kept.append(comment)
                if len(kept) >= total_limit:
                    break
            return kept
        top_level_comments = [comment for comment in comments if comment.parent_id is None]
        return top_level_comments[:total_limit]

    def _cache_metadata_snapshot(self) -> dict[str, object]:
        return {
            "source_type": YOUTUBE_SOURCE_TYPE,
            "estimated_quota_units": self.estimated_quota_units(),
            "search_call_count": self.search_call_count,
            "videos_call_count": self.videos_call_count,
            "comment_threads_call_count": self.comment_threads_call_count,
            "comments_call_count": self.comments_call_count,
            "quota_guardrail_status": self.quota_guardrail_status(),
        }


class _OfficialYouTubeClient:
    """Tiny official YouTube Data API v3 client used only behind explicit env gates."""

    def __init__(self, credentials: YouTubeCredentials) -> None:
        self.credentials = credentials
        self.client = httpx.Client(timeout=10.0)

    def close(self) -> None:
        """Close only the internal HTTP client without issuing a request."""

        self.client.close()

    def search_posts(
        self,
        keyword: str,
        *,
        limit: int,
        sort: str,
        date_range: dict[str, str] | None = None,
    ) -> list[Mapping[str, Any]]:
        try:
            params: dict[str, Any] = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "maxResults": min(limit, YOUTUBE_REAL_POST_LIMIT),
                "order": _youtube_search_order(sort),
                "key": self.credentials.api_key,
            }
            if date_range:
                if published_after := date_range.get("start"):
                    params["publishedAfter"] = published_after
                if published_before := date_range.get("end"):
                    params["publishedBefore"] = published_before
            search_payload = self._get_json(YOUTUBE_SEARCH_ENDPOINT, params=params)
            search_items = _items(search_payload)
            video_ids = [
                _video_id_from_search_item(item)
                for item in search_items
                if _video_id_from_search_item(item)
            ][:limit]
            if not video_ids:
                return []
            videos_response = self._video_details_response(video_ids)
            return parse_official_search_and_videos_responses(
                search_payload,
                videos_response,
            )[:limit]
        except Exception as exc:
            raise _typed_youtube_exception(exc) from exc

    def fetch_comments(self, post_id: str, *, limit: int) -> list[Mapping[str, Any]]:
        try:
            params = {
                "part": "snippet,replies",
                "videoId": post_id,
                "maxResults": min(limit, YOUTUBE_REAL_COMMENT_LIMIT),
                "order": "relevance",
                "textFormat": "plainText",
                "key": self.credentials.api_key,
            }
            payload = self._get_json(YOUTUBE_COMMENT_THREADS_ENDPOINT, params=params)
            comments: list[Mapping[str, Any]] = []
            for item in _items(payload):
                comments.extend(_comment_thread_to_mappings(item, video_id=post_id))
                if len(comments) >= limit:
                    break
            return comments[:limit]
        except Exception as exc:
            raise _typed_youtube_exception(exc) from exc

    def _video_details(self, video_ids: list[str]) -> list[Mapping[str, Any]]:
        return _items(self._video_details_response(video_ids))

    def _video_details_response(self, video_ids: list[str]) -> Mapping[str, Any]:
        params = {
            "part": "snippet,statistics",
            "id": ",".join(video_ids),
            "maxResults": min(len(video_ids), YOUTUBE_REAL_POST_LIMIT),
            "key": self.credentials.api_key,
        }
        return self._get_json(YOUTUBE_VIDEOS_ENDPOINT, params=params)

    def _video_id_from_detail(self, item: Mapping[str, Any]) -> str:
        return str(item.get("id") or "").strip()

    def _get_json(self, url: str, *, params: Mapping[str, Any]) -> Mapping[str, Any]:
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()
            if not isinstance(payload, Mapping):
                raise YouTubeParsingError("youtube_response_not_object")
            return payload
        except Exception as exc:
            raise _typed_youtube_exception(exc) from exc


def create_official_youtube_search_client(
    credentials: YouTubeCredentials,
) -> ClosableYouTubeHttpClient:
    """Construct the official client from explicit credentials only."""

    if not isinstance(credentials, YouTubeCredentials) or not credentials.api_key.strip():
        raise YouTubeAuthError("youtube_explicit_credentials_required")
    return _OfficialYouTubeClient(credentials)


def close_official_youtube_search_client(
    http_client: ClosableYouTubeHttpClient,
) -> None:
    """Close a client produced by ``create_official_youtube_search_client``."""

    http_client.close()


def _mock_youtube_posts(
    *,
    keyword: str,
    sort: str,
    date_range: dict[str, str] | None,
) -> list[dict[str, Any]]:
    topic = keyword or "public opinion"
    return [
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "video_id": "yt_mock_video_001",
            "title": f"{topic} public video discussion",
            "description": "Mock YouTube video discussion about product quality, response timing, and public trust.",
            "channel_id": "yt_mock_channel_001",
            "channel_title": "Mock YouTube Observer",
            "published_at": "2026-05-15T08:00:00Z",
            "like_count": 1820,
            "comment_count": 126,
            "view_count": 48500,
            "url": "https://www.youtube.com/watch?v=yt_mock_video_001",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "video_id": "yt_mock_video_002",
            "title": f"{topic} response analysis",
            "description": "Mock YouTube explainer on how the public is interpreting the official response.",
            "channel_id": "yt_mock_channel_002",
            "channel_title": "Mock Policy Notes",
            "published_at": "2026-05-15T09:25:00Z",
            "like_count": 940,
            "comment_count": 74,
            "view_count": 21200,
            "url": "https://www.youtube.com/watch?v=yt_mock_video_002",
            "sort": sort,
            "date_range": date_range,
        },
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "video_id": "yt_mock_video_003",
            "title": f"{topic} community reaction recap",
            "description": "Mock YouTube recap of comments, repeated concerns, and cross-platform attention.",
            "channel_id": "yt_mock_channel_003",
            "channel_title": "Mock Media Desk",
            "published_at": "2026-05-15T10:10:00Z",
            "like_count": 640,
            "comment_count": 41,
            "view_count": 10800,
            "url": "https://www.youtube.com/watch?v=yt_mock_video_003",
            "sort": sort,
            "date_range": date_range,
        },
    ]


def _mock_youtube_comments(post_id: str) -> list[dict[str, Any]]:
    target_post_id = post_id or "yt_mock_video_001"
    return [
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_001",
            "author_id": "yt_mock_commenter_001",
            "author_name": "mock_youtube_user_a",
            "content": "Mock comment: this summary is helpful, but the company still needs a clear timeline.",
            "published_at": "2026-05-15T08:15:00Z",
            "like_count": 83,
            "reply_count": 4,
            "url": f"https://www.youtube.com/watch?v={target_post_id}&lc={target_post_id}_comment_001",
        },
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_002",
            "parent_id": f"{target_post_id}_comment_001",
            "author_id": "yt_mock_commenter_002",
            "author_name": "mock_youtube_user_b",
            "content": "Mock reply: repeated talking points are showing up, but some real complaints also look valid.",
            "published_at": "2026-05-15T08:22:00Z",
            "like_count": 36,
            "reply_count": 0,
            "url": f"https://www.youtube.com/watch?v={target_post_id}&lc={target_post_id}_comment_002",
        },
        {
            "mode": "mock",
            "source_type": YOUTUBE_SOURCE_TYPE,
            "post_id": target_post_id,
            "comment_id": f"{target_post_id}_comment_003",
            "author_id": "yt_mock_commenter_003",
            "author_name": "mock_youtube_user_c",
            "content": "Mock comment: a factual update with evidence would reduce speculation.",
            "published_at": "2026-05-15T08:30:00Z",
            "like_count": 24,
            "reply_count": 1,
            "url": f"https://www.youtube.com/watch?v={target_post_id}&lc={target_post_id}_comment_003",
        },
    ]


def _video_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    data = raw.get("data")
    if isinstance(data, Mapping):
        return data
    return raw


def _comment_payload(raw: Mapping[str, Any]) -> Mapping[str, Any]:
    if "data" in raw and isinstance(raw.get("data"), Mapping):
        return raw["data"]
    snippet = raw.get("snippet")
    if isinstance(snippet, Mapping) and isinstance(snippet.get("topLevelComment"), Mapping):
        top_level = snippet["topLevelComment"]
        top_snippet = top_level.get("snippet") if isinstance(top_level.get("snippet"), Mapping) else {}
        payload = dict(top_snippet)
        payload["comment_id"] = top_level.get("id")
        payload["post_id"] = snippet.get("videoId") or top_snippet.get("videoId")
        payload["reply_count"] = snippet.get("totalReplyCount")
        return payload
    if isinstance(snippet, Mapping):
        payload = dict(snippet)
        payload["comment_id"] = raw.get("id")
        payload["post_id"] = snippet.get("videoId")
        payload["parent_id"] = snippet.get("parentId")
        return payload
    return raw


def _items(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    items = payload.get("items")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, Mapping)]


def parse_official_search_and_videos_responses(
    search_response: Mapping[str, Any],
    videos_response: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    """Merge official-shaped search and video payloads without I/O.

    Search ordering is authoritative. Malformed identifiers are skipped and
    video detail rows that were not selected by the search payload are ignored.
    """

    details_by_id: dict[str, Mapping[str, Any]] = {}
    for detail in _items(videos_response):
        video_id = str(detail.get("id") or "").strip()
        if video_id and video_id not in details_by_id:
            details_by_id[video_id] = detail

    merged: list[Mapping[str, Any]] = []
    seen_video_ids: set[str] = set()
    for search_item in _items(search_response):
        video_id = _video_id_from_search_item(search_item)
        if not video_id or video_id in seen_video_ids:
            continue
        seen_video_ids.add(video_id)
        detail = details_by_id.get(video_id, {})
        search_snippet = (
            search_item.get("snippet")
            if isinstance(search_item.get("snippet"), Mapping)
            else {}
        )
        detail_snippet = (
            detail.get("snippet")
            if isinstance(detail.get("snippet"), Mapping)
            else {}
        )
        statistics = (
            detail.get("statistics")
            if isinstance(detail.get("statistics"), Mapping)
            else {}
        )
        merged.append(
            {
                "source_type": YOUTUBE_SOURCE_TYPE,
                "id": video_id,
                "snippet": detail_snippet or search_snippet,
                "statistics": statistics,
            }
        )
    return merged


def _video_id_from_search_item(item: Mapping[str, Any]) -> str:
    raw_id = item.get("id")
    if isinstance(raw_id, Mapping):
        return str(raw_id.get("videoId") or "").strip()
    return str(raw_id or "").strip()


def _comment_thread_to_mappings(item: Mapping[str, Any], *, video_id: str) -> list[Mapping[str, Any]]:
    snippet = item.get("snippet") if isinstance(item.get("snippet"), Mapping) else {}
    top_level = snippet.get("topLevelComment") if isinstance(snippet.get("topLevelComment"), Mapping) else None
    comments: list[Mapping[str, Any]] = []
    if top_level is not None:
        top_snippet = top_level.get("snippet") if isinstance(top_level.get("snippet"), Mapping) else {}
        top_payload = dict(top_snippet)
        top_payload.update(
            {
                "source_type": YOUTUBE_SOURCE_TYPE,
                "comment_id": top_level.get("id"),
                "post_id": snippet.get("videoId") or top_snippet.get("videoId") or video_id,
                "reply_count": snippet.get("totalReplyCount"),
            }
        )
        comments.append(top_payload)
        parent_id = str(top_level.get("id") or "").strip()
        replies = item.get("replies") if isinstance(item.get("replies"), Mapping) else {}
        reply_items = replies.get("comments", [])
        if not isinstance(reply_items, list):
            reply_items = []
        for reply in reply_items:
            if not isinstance(reply, Mapping):
                continue
            reply_snippet = reply.get("snippet") if isinstance(reply.get("snippet"), Mapping) else {}
            reply_payload = dict(reply_snippet)
            reply_payload.update(
                {
                    "source_type": YOUTUBE_SOURCE_TYPE,
                    "comment_id": reply.get("id"),
                    "post_id": reply_snippet.get("videoId") or video_id,
                    "parent_id": reply_snippet.get("parentId") or parent_id,
                }
            )
            comments.append(reply_payload)
    return comments


def _adapter_mode_from_env() -> AdapterMode:
    return _normalize_adapter_mode(os.getenv("YOUTUBE_ADAPTER_MODE", "mock"))


def _normalize_adapter_mode(mode: str | None) -> AdapterMode:
    return "real" if str(mode or "mock").strip().lower() == "real" else "mock"


def _normalize_sort(sort: str) -> str:
    normalized = str(sort or "relevance").strip().lower()
    return normalized if normalized in {"relevance", "date", "view_count", "rating"} else "relevance"


def _youtube_search_order(sort: str) -> str:
    mapping = {
        "new": "date",
        "date": "date",
        "hot": "relevance",
        "top": "viewCount",
        "view_count": "viewCount",
        "rating": "rating",
        "relevance": "relevance",
    }
    return mapping.get(str(sort or "relevance").strip().lower(), "relevance")


def _fallback_reason_category(fallback_reason: str | None) -> str | None:
    if not fallback_reason:
        return None
    prefix = fallback_reason.split(":", 1)[0].strip().lower()
    if prefix in {
        "auth_error",
        "network_error",
        "parsing_error",
        "adapter_error",
        "config_error",
        "quota_error",
        "comments_unavailable",
    }:
        return prefix
    if "missing" in fallback_reason.lower() or "config" in fallback_reason.lower():
        return "config_error"
    if "auth" in fallback_reason.lower() or "key" in fallback_reason.lower():
        return "auth_error"
    if "quota" in fallback_reason.lower():
        return "quota_error"
    if "comment" in fallback_reason.lower() and "unavailable" in fallback_reason.lower():
        return "comments_unavailable"
    if "network" in fallback_reason.lower() or "timeout" in fallback_reason.lower():
        return "network_error"
    return "adapter_error"


def _real_mode_blocked_reason(fallback_category: str | None, mode: AdapterMode) -> str | None:
    if fallback_category == "config_error":
        return "credentials_missing"
    if fallback_category:
        return fallback_category
    if mode == "mock":
        return "mock_only"
    return None


def _credential_presence() -> dict[str, bool]:
    from app.core.environment import load_project_env

    load_project_env()
    return {
        credential_name: bool(os.getenv(credential_name, "").strip())
        for credential_name in YOUTUBE_REQUIRED_CREDENTIALS
    }


def _typed_youtube_exception(exc: Exception) -> YouTubeRealModeError:
    category = _real_mode_error_category(exc)
    if category == "auth_error":
        return YouTubeAuthError("youtube_auth_error")
    if category == "network_error":
        return YouTubeNetworkError("youtube_network_error")
    if category == "quota_error":
        return YouTubeQuotaError("youtube_quota_error")
    if category == "comments_unavailable":
        return YouTubeCommentsDisabledError("youtube_comments_unavailable")
    if category == "parsing_error":
        return YouTubeParsingError("youtube_parsing_error")
    if isinstance(exc, YouTubeRealModeError):
        return exc
    return YouTubeRealModeError("youtube_adapter_error")


def _real_mode_error_category(exc: Exception) -> str:
    if isinstance(exc, YouTubeRealModeError):
        return exc.category

    status_code = _status_code_from_exception(exc)
    class_name = exc.__class__.__name__.lower()
    safe_text = str(exc).lower()

    if "quota" in safe_text or "quota" in class_name:
        return "quota_error"
    if (
        "commentsdisabled" in safe_text
        or "comments disabled" in safe_text
        or "comments_unavailable" in safe_text
        or "disabled_comment" in safe_text
    ):
        return "comments_unavailable"

    if status_code in {400, 401, 403}:
        return "auth_error"
    if status_code in {408, 409, 425, 429, 500, 502, 503, 504}:
        return "network_error"
    if "timeout" in class_name or "connect" in class_name or "network" in class_name:
        return "network_error"
    if "httpstatus" in class_name:
        return "auth_error" if status_code in {400, 401, 403, None} else "network_error"
    if "json" in class_name or "decode" in class_name or "validation" in class_name or "keyerror" in class_name:
        return "parsing_error"
    return "adapter_error"


def _status_code_from_exception(exc: Exception) -> int | None:
    for candidate in (exc, getattr(exc, "response", None), getattr(exc, "__cause__", None)):
        status_code = getattr(candidate, "status_code", None) or getattr(candidate, "status", None)
        if isinstance(status_code, int):
            return status_code
    return None
