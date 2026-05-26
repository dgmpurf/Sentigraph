# Sentigraph API Contract

Base path:

```text
/api/v1
```

During MVP 0 and MVP 1, all endpoints may return mock data.

## 0. Health Check

### Endpoint

```http
GET /api/v1/health
```

### Response

```json
{
  "status": "ok",
  "mode": "development",
  "version": "0.1.0"
}
```

## 0.1 Platform Registry

### Endpoint

```http
GET /api/v1/platforms
```

### Response

```json
{
  "platforms": [
    {
      "platform_id": "reddit",
      "display_name": "Reddit",
      "category": "future_real_adapter_candidate",
      "source_type": "mock_data_future_adapter_placeholder",
      "status": "api_pending",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "api_pending",
      "credentials_required": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"],
      "credentials_present": {
        "REDDIT_CLIENT_ID": false,
        "REDDIT_CLIENT_SECRET": false,
        "REDDIT_USER_AGENT": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": null,
      "notes": "Selectable for offline mock analysis. Reddit API approval is pending, so real API mode is disabled and public-page scraping is not used as a bypass."
    },
    {
      "platform_id": "weibo",
      "display_name": "Weibo",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["WEIBO_CLIENT_ID", "WEIBO_CLIENT_SECRET", "WEIBO_ACCESS_TOKEN"],
      "credentials_present": {
        "WEIBO_CLIENT_ID": false,
        "WEIBO_CLIENT_SECRET": false,
        "WEIBO_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://open.weibo.com",
      "notes": "Selectable for offline Weibo-style mock microblog/comment analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "bilibili",
      "display_name": "Bilibili",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["BILIBILI_CLIENT_ID", "BILIBILI_CLIENT_SECRET", "BILIBILI_ACCESS_TOKEN"],
      "credentials_present": {
        "BILIBILI_CLIENT_ID": false,
        "BILIBILI_CLIENT_SECRET": false,
        "BILIBILI_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://openhome.bilibili.com",
      "notes": "Selectable for offline Bilibili-style mock video/comment analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "douyin",
      "display_name": "Douyin",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "developer_access_obtained_permission_unverified",
      "developer_access_status": "obtained",
      "app_type": "web_app",
      "comment_api_status": "item_comment_scope_not_verified",
      "recommended_comment_scope": "item.comment",
      "video_comment_scope_status": "not_recommended_for_mvp",
      "real_mode_blocker": "oauth_and_scope_not_verified",
      "credentials_required": ["DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET", "DOUYIN_REDIRECT_URI", "DOUYIN_ACCESS_TOKEN", "DOUYIN_REFRESH_TOKEN"],
      "credentials_present": {
        "DOUYIN_CLIENT_KEY": false,
        "DOUYIN_CLIENT_SECRET": false,
        "DOUYIN_REDIRECT_URI": false,
        "DOUYIN_ACCESS_TOKEN": false,
        "DOUYIN_REFRESH_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://developer.open-douyin.com",
      "notes": "Selectable for offline Douyin-style mock short-video/comment analysis. Developer access is obtained, but Web App OAuth, item.comment scope, test-account authorization, token exchange, and item_id source are not verified. Real mode remains disabled. No page scraping is implemented."
    },
    {
      "platform_id": "kuaishou",
      "display_name": "Kuaishou",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["KUAISHOU_CLIENT_ID", "KUAISHOU_CLIENT_SECRET", "KUAISHOU_ACCESS_TOKEN"],
      "credentials_present": {
        "KUAISHOU_CLIENT_ID": false,
        "KUAISHOU_CLIENT_SECRET": false,
        "KUAISHOU_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://open.kuaishou.com",
      "notes": "Selectable for offline Kuaishou-style mock short-video/comment analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "xiaohongshu",
      "display_name": "Xiaohongshu",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "developer_access_obtained_permission_unverified",
      "developer_access_status": "obtained",
      "comment_api_status": "unknown_or_not_confirmed",
      "real_mode_blocker": "permission_not_verified",
      "credentials_required": ["XIAOHONGSHU_CLIENT_ID", "XIAOHONGSHU_CLIENT_SECRET", "XIAOHONGSHU_ACCESS_TOKEN"],
      "credentials_present": {
        "XIAOHONGSHU_CLIENT_ID": false,
        "XIAOHONGSHU_CLIENT_SECRET": false,
        "XIAOHONGSHU_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://open.xiaohongshu.com",
      "notes": "Selectable for offline Xiaohongshu-style mock lifestyle/community note analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "zhihu",
      "display_name": "Zhihu",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["ZHIHU_CLIENT_ID", "ZHIHU_CLIENT_SECRET", "ZHIHU_ACCESS_TOKEN"],
      "credentials_present": {
        "ZHIHU_CLIENT_ID": false,
        "ZHIHU_CLIENT_SECRET": false,
        "ZHIHU_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://open.zhihu.com",
      "notes": "Selectable for offline Zhihu-style mock Q&A/article/comment analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "douban",
      "display_name": "Douban",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["DOUBAN_CLIENT_ID", "DOUBAN_CLIENT_SECRET", "DOUBAN_ACCESS_TOKEN"],
      "credentials_present": {
        "DOUBAN_CLIENT_ID": false,
        "DOUBAN_CLIENT_SECRET": false,
        "DOUBAN_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://developers.douban.com",
      "notes": "Selectable for offline Douban-style mock review/group/topic analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    },
    {
      "platform_id": "toutiao",
      "display_name": "Toutiao",
      "category": "official_api_planned",
      "source_type": "official_api_adapter_scaffold",
      "status": "official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "mock_available": true,
      "real_mode_available": false,
      "api_approval_required": true,
      "api_approval_status": "planned",
      "credentials_required": ["TOUTIAO_CLIENT_ID", "TOUTIAO_CLIENT_SECRET", "TOUTIAO_ACCESS_TOKEN"],
      "credentials_present": {
        "TOUTIAO_CLIENT_ID": false,
        "TOUTIAO_CLIENT_SECRET": false,
        "TOUTIAO_ACCESS_TOKEN": false
      },
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "official_platform_url": "https://open.toutiao.com",
      "notes": "Selectable for offline Toutiao-style mock article/micro-headline/comment analysis. Real official API mode is disabled until credentials, approval, and the compliant API implementation are added. No page scraping is implemented."
    }
  ],
  "active_mvp_platforms": [
    "reddit",
    "weibo",
    "bilibili",
    "douyin",
    "kuaishou",
    "xiaohongshu",
    "zhihu",
    "douban",
    "toutiao",
    "youtube"
  ]
}
```

Important:

- `selectable_for_mock=true` means the frontend may show the platform in mock-first selectors.
- `mock_available=true` means the platform has safe local mock data behavior.
- `GET /api/v1/platforms` and the readiness/status endpoints expose the same per-platform readiness fields; examples may omit some optional fields for brevity.
- `real_mode_available=true` means the backend may use a real source path for that platform when all explicit gates pass. YouTube is real-capable when locally configured; other current platform adapters remain mock-only or approval-gated.
- `credentials_present` is a safe boolean map only. It must never contain credential values.
- `developer_access_status`, `comment_api_status`, `recommended_comment_scope`, `video_comment_scope_status`, and `real_mode_blocker` are safe non-secret readiness fields. They describe console/access status only and must not expose credential values.
- `api_pending=true` means any future real API path is still waiting for approval, credentials, permissions, or compliance review.
- `real_mode_disabled=true` means the backend must not call the real platform API for that source.
- Official API planned platforms may be selectable for mock analysis, but they must not trigger real API calls until credentials, permissions, and compliance checks are available.
- Reddit is visible and mock-selectable as a future real adapter candidate, but its current real API status is `api_pending`.
- Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao are mock-selectable through official API adapter scaffolds. Their real API modes are disabled and not called until credentials, approval, permission verification, and implementation are added. Douyin additionally shows `developer_access_status="obtained"`, `app_type="web_app"`, `comment_api_status="item_comment_scope_not_verified"`, `recommended_comment_scope="item.comment"`, `video_comment_scope_status="not_recommended_for_mvp"`, and `real_mode_blocker="oauth_and_scope_not_verified"`. Xiaohongshu shows developer access obtained but note/comment permission not verified.
- YouTube is mock-selectable and uses `source_type="youtube_data_api_v3"`. It is real-capable by design, but real-selectable only when `YOUTUBE_ADAPTER_MODE=real` and a local `YOUTUBE_API_KEY` are configured; `credential_present`, `credentials_present`, and crawl metadata expose booleans only.
- Crawler-later platforms are not selectable for real crawling in the MVP.

### Platform Readiness Status

```http
GET /api/v1/platforms/status
GET /api/v1/platforms/readiness
```

`/platforms/readiness` is the preferred endpoint for the Real Data Source
Readiness Framework. `/platforms/status` remains a backward-compatible alias
with the same response shape.

Response:

```json
{
  "platforms": [
    {
      "platform_id": "reddit",
      "platform": "reddit",
      "display_name": "Reddit",
      "category": "future_real_adapter_candidate",
      "source_type": "mock_data_future_adapter_placeholder",
      "integration_type": "official_api_pending",
      "status": "api_pending",
      "mock_available": true,
      "real_mode_available": false,
      "real_mode_configured": false,
      "api_approval_required": true,
      "api_approval_status": "api_pending",
      "required_credentials": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"],
      "required_scopes": [],
      "scope_status": "approval_pending",
      "oauth_required": false,
      "oauth_status": "not_required",
      "real_mode_blocker": "approval_pending",
      "data_access_level": "mock_reddit_style_data",
      "next_user_action": "Wait for Reddit API approval; do not use public-page scraping as a bypass.",
      "credentials_required": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"],
      "credentials_present": {
        "REDDIT_CLIENT_ID": false,
        "REDDIT_CLIENT_SECRET": false,
        "REDDIT_USER_AGENT": false
      },
      "credential_present": false,
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "selectable_for_real": false,
      "api_pending": true,
      "real_mode_disabled": true,
      "official_platform_url": null,
      "notes": "Selectable for offline mock analysis. Reddit API approval is pending, so real API mode is disabled and public-page scraping is not used as a bypass."
    }
  ],
  "active_mvp_platforms": ["reddit", "weibo", "bilibili", "douyin", "kuaishou", "xiaohongshu", "zhihu", "douban", "toutiao", "youtube"],
  "mock_selectable_platforms": ["reddit", "weibo", "bilibili", "douyin", "kuaishou", "xiaohongshu", "zhihu", "douban", "toutiao", "youtube"],
  "real_selectable_platforms": [],
  "summary": {
    "total_platforms": 17,
    "mock_selectable_count": 10,
    "real_selectable_count": 0,
    "api_pending_count": 9,
    "disabled_count": 7,
    "crawler_later_count": 7
  }
}
```

Important:

- This endpoint is safe for UI diagnostics.
- It returns credential presence as booleans only.
- Unified readiness fields include `integration_type`, `required_credentials`, `required_scopes`, `scope_status`, `oauth_required`, `oauth_status`, `real_mode_configured`, `real_mode_blocker`, `data_access_level`, `next_user_action`, and `quota_cache_protected`.
- Reddit remains `api_pending`; real API mode is disabled until approval is granted.
- Crawler-later platforms are visible for roadmap planning but never real-selectable in the MVP.
- YouTube appears in mock-selectable platforms. `real_selectable_platforms` includes `youtube` only when `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` are configured locally.
- Douyin reports `integration_type=official_api_oauth`, `developer_access_status=obtained`, `app_type=web_app`, `required_scopes=["user_info", "item.comment"]`, `scope_status=item_comment_not_verified`, `oauth_required=true`, and `real_mode_blocker=oauth_and_scope_not_verified` until console verification is complete.
- Weibo reports `real_mode_blocker=company_age_requirement_pending`; Reddit and Bilibili report approval-pending blockers; Xiaohongshu reports `comment_api_unknown_or_not_confirmed`.

## 0.2 Public Parser Status and Preview

These endpoints expose safe developer diagnostics for the compliant public-page parser scaffolds. They do not require credentials and do not call real platform APIs or external LLM services.

### Parser Status

```http
GET /api/v1/public-parsers/status
```

Response:

```json
{
  "parsers": [
    {
      "platform_id": "hupu",
      "display_name": "Hupu / HuPu",
      "source_type": "public_page_parser",
      "parser_status": "fixture_only",
      "live_fetch_enabled": false,
      "fixture_available": true,
      "profile_available": true,
      "comments_supported": true,
      "last_test_status": "fixture_available",
      "notes": "Fixture-only public parser scaffold for forum-style Hupu threads.",
      "safe_limit": 3,
      "rate_limit_seconds": 3.0
    }
  ],
  "total": 6,
  "live_fetch_enabled_default": false
}
```

Current public parser platforms:

```text
the_paper
jiemian
hupu
maimai
tieba
nga
```

### Parser Preview

```http
POST /api/v1/public-parsers/preview
```

Request:

```json
{
  "platform": "hupu",
  "limit": 3,
  "use_live_fetch": false
}
```

Response:

```json
{
  "platform": "hupu",
  "source_type": "public_page_parser",
  "parser_status": "fixture_only",
  "live_fetch_enabled": false,
  "live_fetch_attempted": false,
  "fallback_used": true,
  "fallback_reason_category": "fixture_preview",
  "post_count": 1,
  "comment_count": 2,
  "raw_post_schema_valid": true,
  "raw_comment_schema_valid": true,
  "sample_posts": [],
  "sample_comments": [],
  "warnings": []
}
```

Important:

- Preview is fixture-first and deterministic.
- Default preview does not perform live public-page fetches.
- If `use_live_fetch=true` but live fetch is disabled by configuration or not supported by the platform, the endpoint returns fixture preview data with a `live_fetch_disabled` warning.
- Public parser previews must not use login, cookies, captcha handling, anti-bot evasion, proxy rotation, hidden APIs, private data, Reddit scraping, platform APIs, or external LLM calls.

### Selector Repair Suggestion

```http
POST /api/v1/public-parsers/selector-repair/suggest
```

Request:

```json
{
  "platform_id": "hupu",
  "html": "<article class=\"thread\"><h1 class=\"thread-title\">Fixture title</h1></article>",
  "profile": {
    "title_selector": ".old-title"
  },
  "extraction_targets": ["title", "content"],
  "error_summary": "title/content selectors did not match fixture HTML"
}
```

Response:

```json
{
  "platform_id": "hupu",
  "status": "suggested",
  "candidates": [
    {
      "target": "title",
      "selector": "h1",
      "selector_type": "css",
      "confidence": 0.82,
      "rationale": "Deterministic mock selector candidate for fixture-only repair review.",
      "source": "mock_provider"
    }
  ],
  "warnings": ["human_review_required", "active_profiles_not_modified"],
  "provider": "mock",
  "generated_by_mock": true,
  "applied": false,
  "review_required": true,
  "draft_id": null
}
```

### Selector Repair Preview

```http
POST /api/v1/public-parsers/selector-repair/preview
```

Request:

```json
{
  "platform_id": "hupu",
  "suggestion": {
    "platform_id": "hupu",
    "status": "suggested",
    "candidates": [
      {
        "target": "title",
        "selector": "h1.thread-title",
        "selector_type": "css",
        "confidence": 0.9,
        "rationale": "Fixture candidate",
        "source": "mock_provider"
      }
    ],
    "warnings": [],
    "provider": "mock",
    "generated_by_mock": true,
    "applied": false,
    "review_required": true,
    "draft_id": null
  },
  "fixture_html": "<article class=\"thread\"><h1 class=\"thread-title\">Fixture title</h1></article>"
}
```

Response:

```json
{
  "platform_id": "hupu",
  "status": "preview_ok",
  "matched_targets": {
    "title": true
  },
  "sample_values": {
    "title": "Fixture title"
  },
  "warnings": [],
  "suggestion": {
    "platform_id": "hupu",
    "status": "suggested",
    "candidates": [],
    "warnings": [],
    "provider": "mock",
    "generated_by_mock": true,
    "applied": false,
    "review_required": true,
    "draft_id": null
  },
  "profile_modified": false
}
```

Important:

- Selector repair is fixture-only and uses sanitized HTML only.
- `SELECTOR_REPAIR_MODE=mock` is the default, and suggestions are generated by the deterministic offline `MockProvider`.
- `future_real_llm` selector repair remains disabled and must not call external LLM APIs.
- The endpoints do not fetch live pages and do not call real platform APIs.
- Active parser profiles are never modified automatically; human review is required before any profile edit.

## 0.3 LLM Safety Status and Usage

These endpoints expose frontend-safe LLM readiness and usage guardrail diagnostics. They do not call external LLM APIs and never expose API key values, `.env` values, raw prompts, raw user content, or raw LLM request bodies.

### LLM Status

```http
GET /api/v1/llm/status
```

Response:

```json
{
  "provider_name": "mock",
  "provider_status": "mock_ready",
  "real_calls_enabled": false,
  "api_key_present": false,
  "available_providers": ["deepseek", "mock", "openai", "qwen"],
  "providers": [
    {
      "provider_name": "mock",
      "provider_status": "mock_ready",
      "real_calls_enabled": false,
      "api_key_present": false,
      "api_key_required": false,
      "available": true
    },
    {
      "provider_name": "openai",
      "provider_status": "provider_not_enabled",
      "real_calls_enabled": false,
      "api_key_present": false,
      "api_key_required": true,
      "available": false
    }
  ],
  "tracking_enabled": true,
  "daily_call_limit": 100,
  "daily_token_limit": 100000,
  "max_input_chars": 20000,
  "guardrail_mode": "mock",
  "safety_flags": {
    "mock_default": true,
    "real_calls_disabled_by_default": true,
    "api_key_values_exposed": false,
    "raw_prompt_logging": false,
    "raw_user_content_logging": false
  }
}
```

### LLM Usage

```http
GET /api/v1/llm/usage
```

Response:

```json
{
  "tracking_enabled": true,
  "guardrail_mode": "mock",
  "daily_call_limit": 100,
  "daily_token_limit": 100000,
  "max_input_chars": 20000,
  "total_calls": 1,
  "daily_calls": 1,
  "daily_input_tokens": 5,
  "daily_output_tokens": 30,
  "daily_total_tokens": 35,
  "recent_records": [
    {
      "provider": "mock",
      "operation": "expand_keywords",
      "input_chars": 20,
      "output_chars": 120,
      "estimated_input_tokens": 5,
      "estimated_output_tokens": 30,
      "timestamp": "2026-05-17T12:00:00Z",
      "success": true,
      "failure_category": null
    }
  ]
}
```

Important:

- `api_key_present` is a boolean only; API key names and values are not exposed by these endpoints.
- `recent_records` are metadata-only usage records. They must not include prompts, raw comments, sanitized HTML bodies, response bodies, cookies, headers, credentials, or `.env` values.
- `real_calls_enabled=false` is the default. The frontend LLM Safety page must not expose a real-call toggle or API key input field.

## 1. Keyword Expansion

### Endpoint

```http
POST /api/v1/keywords/expand
```

### Request

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo"],
  "language": "auto"
}
```

### Response

```json
{
  "original_keyword": "Tesla",
  "expanded_keywords": ["Tesla", "特斯拉", "Model Y", "自动驾驶", "降价"],
  "search_queries": [
    "Tesla problem",
    "Tesla recall",
    "特斯拉 刹车",
    "特斯拉 降价"
  ]
}
```

## 2. Start Crawl

### Endpoint

```http
POST /api/v1/crawl/start
```

### Request

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo"],
  "limit": 100,
  "date_range": {
    "start": "2026-05-01",
    "end": "2026-05-13"
  }
}
```

### Response

```json
{
  "project_id": "project_001",
  "crawl_task_id": "crawl_task_001",
  "status": "queued",
  "message": "Crawl task queued with platform adapter metadata. Mock-first fallback remains enabled.",
  "platform_metadata": [
    {
      "platform": "reddit",
      "adapter_mode": "mock",
      "source_type": null,
      "parser_status": null,
      "live_fetch_enabled": false,
      "live_fetch_attempted": false,
      "live_fetch_allowed": false,
      "fallback_used": false,
      "fallback_reason_category": null,
      "fetch_status": null,
      "mock_available": true,
      "real_mode_available": false,
      "credential_present": false,
      "api_approval_required": true,
      "api_approval_status": "api_pending",
      "api_pending": true,
      "real_mode_disabled": true,
      "selectable_for_real": false,
      "real_mode_blocked_reason": "mock_only",
      "real_mode_reached": false,
      "dependency_available": true,
      "exception_class": null,
      "sanitized_error_category": null,
      "estimated_quota_units": 0,
      "search_call_count": 0,
      "videos_call_count": 0,
      "comment_threads_call_count": 0,
      "comments_call_count": 0,
      "cache_hit": false,
      "cache_age_seconds": null,
      "quota_guardrail_status": "mock_mode",
      "post_count": 3,
      "comment_count": 3,
      "schema_valid": true,
      "raw_post_schema_valid": true,
      "raw_comment_schema_valid": true
    }
  ],
  "raw_posts": [
    {
      "platform": "reddit",
      "post_id": "reddit_mock_post_001",
      "author_id": "reddit_user_001",
      "author_name": "reddit_user",
      "title": "Tesla quality discussion",
      "content": "Mock Reddit public post content.",
      "like_count": 42,
      "reply_count": 3,
      "share_count": 0,
      "created_at": "2026-05-15T00:00:00Z",
      "url": "https://www.reddit.com/r/test/comments/reddit_mock_post_001/",
      "raw_data": {
        "mode": "mock"
      }
    }
  ],
  "raw_comments": [
    {
      "platform": "reddit",
      "post_id": "reddit_mock_post_001",
      "comment_id": "reddit_mock_comment_001",
      "parent_id": null,
      "author_id": "reddit_commenter_001",
      "author_name": "reddit_commenter",
      "content": "Mock Reddit public comment content.",
      "like_count": 8,
      "reply_count": 0,
      "share_count": 0,
      "created_at": "2026-05-15T00:01:00Z",
      "url": "https://www.reddit.com/r/test/comments/reddit_mock_post_001/comment/",
      "raw_data": {
        "mode": "mock"
      }
    }
  ]
}
```

Important:

- `POST /api/v1/crawl/start` is still mock-first and backward compatible.
- When `platforms` contains `reddit`, the endpoint calls the Reddit platform adapter through `adapter_factory.get_adapter("reddit")`.
- Reddit mock mode returns normalized `RawPost` and `RawComment` items in `raw_posts` and `raw_comments`.
- Reddit real API mode is disabled while Reddit approval is pending. If Reddit is selected, the endpoint returns normalized mock data and safe approval/fallback metadata.
- Public-page scraping is not implemented and must not be used to bypass Reddit API approval.
- When `platforms` contains `weibo`, the endpoint calls the Weibo official API adapter scaffold through `adapter_factory.get_adapter("weibo")`.
- Weibo mock mode returns deterministic microblog-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Weibo real API mode is disabled. If `WEIBO_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Weibo API call.
- When `platforms` contains `bilibili`, the endpoint calls the Bilibili official API adapter scaffold through `adapter_factory.get_adapter("bilibili")`.
- Bilibili mock mode returns deterministic video-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Bilibili real API mode is disabled. If `BILIBILI_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Bilibili API call.
- When `platforms` contains `douyin`, the endpoint calls the Douyin official API adapter scaffold through `adapter_factory.get_adapter("douyin")`.
- Douyin mock mode returns deterministic short-video-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Douyin real API mode is disabled. Developer access is recorded as obtained by the user, but Web App OAuth, redirect URI, authorized test account, token exchange, `item.comment` scope, and lawful `item_id` source are not verified. If `DOUYIN_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending:permission_not_verified` when complete placeholder OAuth configuration is present or `config_error` metadata when configuration is incomplete, and makes no real Douyin API call.
- When `platforms` contains `kuaishou`, the endpoint calls the Kuaishou official API adapter scaffold through `adapter_factory.get_adapter("kuaishou")`.
- Kuaishou mock mode returns deterministic short-video/livestream-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Kuaishou real API mode is disabled. If `KUAISHOU_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Kuaishou API call.
- When `platforms` contains `xiaohongshu`, the endpoint calls the Xiaohongshu official API adapter scaffold through `adapter_factory.get_adapter("xiaohongshu")`.
- Xiaohongshu mock mode returns deterministic lifestyle/community-note-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Xiaohongshu real API mode is disabled. Developer access is recorded as obtained by the user, but note/comment API availability is not verified. If `XIAOHONGSHU_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending:permission_not_verified` when credentials are present or `config_error` metadata when credentials are missing, and makes no real Xiaohongshu API call.
- When `platforms` contains `zhihu`, the endpoint calls the Zhihu official API adapter scaffold through `adapter_factory.get_adapter("zhihu")`.
- Zhihu mock mode returns deterministic Q&A/article-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Zhihu real API mode is disabled. If `ZHIHU_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Zhihu API call.
- When `platforms` contains `douban`, the endpoint calls the Douban official API adapter scaffold through `adapter_factory.get_adapter("douban")`.
- Douban mock mode returns deterministic review/group/topic-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Douban real API mode is disabled. If `DOUBAN_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Douban API call.
- When `platforms` contains `toutiao`, the endpoint calls the Toutiao official API adapter scaffold through `adapter_factory.get_adapter("toutiao")`.
- Toutiao mock mode returns deterministic article/micro-headline-style `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `official_api_adapter_scaffold`.
- Toutiao real API mode is disabled. If `TOUTIAO_ADAPTER_MODE=real`, the endpoint still returns mock data plus safe `api_pending` or `config_error` metadata and makes no real Toutiao API call.
- When `platforms` contains `youtube`, the endpoint calls the YouTube official Data API v3 adapter through `adapter_factory.get_adapter("youtube")`.
- YouTube mock mode returns deterministic YouTube-style video `RawPost` data and visible public-comment-style `RawComment` data. `source_type` is `youtube_data_api_v3`.
- YouTube real mode is enabled only when `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` is present locally. If the key is missing, the endpoint safely returns mock data plus `credential_present=false` and `fallback_reason_category=config_error`.
- YouTube real mode uses tiny quota-guarded `search.list`, `videos.list`, and `commentThreads.list` requests. `search.list` is treated as expensive, so real-mode calls check the project-local cache before calling the official API.
- YouTube cache and guardrail configuration is controlled by `YOUTUBE_CACHE_ENABLED`, `YOUTUBE_CACHE_TTL_SECONDS`, `YOUTUBE_MAX_SEARCH_RESULTS`, `YOUTUBE_MAX_COMMENTS_PER_VIDEO`, `YOUTUBE_MAX_REPLIES_PER_COMMENT`, `YOUTUBE_MAX_TOTAL_COMMENTS`, and `YOUTUBE_ENABLE_DEEP_REPLIES`. The defaults are cache enabled for 3600 seconds, at most 5 search results, 20 comments per video, 5 replies per top-level comment, 50 total comments, and deep replies disabled.
- YouTube cache entries are stored under the ignored runtime path `backend/data/youtube_cache.json`; cache keys include only safe query fields such as keyword, video id, limit, order, and date range. API keys are never stored.

### Planned Douyin Web App OAuth API Design

These endpoints are design-only placeholders and are not implemented in the current backend:

- `GET /api/v1/douyin/oauth/authorize-url`: planned helper to generate an authorization URL with `client_key`, configured HTTPS `redirect_uri`, requested scopes such as `user_info,item.comment` plus `trial.whitelist` only when required in test mode, and a one-time `state`. The future Douyin-side authorization concept is `/platform/oauth/connect/`.
- `GET /api/v1/douyin/oauth/callback`: planned callback to receive `code`, `state`, and granted scopes, validate state, and record safe OAuth metadata.
- `POST /api/v1/douyin/oauth/token/exchange`: planned token-exchange placeholder for the official `/oauth/access_token/` concept; disabled until token storage and scope verification are reviewed.
- `POST /api/v1/douyin/oauth/token/refresh`: planned refresh placeholder for the official `/oauth/refresh_token/` concept; disabled until protected token storage is designed.

No current endpoint exchanges tokens, refreshes tokens, calls `item.comment`, or calls any real Douyin API.
- YouTube crawl metadata may include safe quota/cache fields: `estimated_quota_units`, `search_call_count`, `videos_call_count`, `comment_threads_call_count`, `comments_call_count`, `cache_hit`, `cache_age_seconds`, and `quota_guardrail_status`.
- `quota_guardrail_status` may be `mock_mode`, `real_mode_blocked`, `real_mode_ready`, `cache_hit`, `partial_cache_hit`, `cache_miss_real_call`, `quota_error_fallback`, or `comments_unavailable_partial`.
- If YouTube comments are disabled or unavailable, the adapter returns a safe partial result rather than crashing. If quota/auth/network/parsing errors happen in real mode, the adapter falls back safely with coarse error metadata.
- `commentThreads.list` may include only a limited subset of replies; deeper reply expansion through `comments.list` with `parentId` remains future work behind strict limits and is disabled by default.
- YouTube crawl metadata includes `credential_present` as a boolean only. It must never include the key value.
- When `platforms` explicitly contains a registered public-parser scaffold such as `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, or `nga`, the endpoint calls the public parser adapter through `adapter_factory.get_adapter(platform_id)`.
- The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA public parsers currently run in `fixture_only` mode and return safe fixture/mock `RawPost` data by default.
- The Paper has an optional local live public-page fetch pilot only when `PUBLIC_PARSER_LIVE_FETCH_ENABLED=true`. Jiemian remains fixture-only in this phase.
- The Paper live pilot checks robots/profile policy first, uses low request limits and timeout, sends no cookies or authorization headers, performs no login or captcha handling, uses no proxy rotation, and falls back to fixture/mock data on unclear policy, blocked access, network errors, selector errors, or parsing failures.
- Jiemian fixture output currently includes title, content, source/author label, created time, and permalink. Comments are not parsed because public comments are unavailable without login or dynamic loading in the fixture: `comments_unavailable_without_login_or_dynamic_loading`.
- Maimai fixture output currently includes post title, main post content, source/author label, created time, permalink, interaction count, reply count, and visible fixture replies normalized as `RawComment`. Maimai live fetch remains disabled.
- Hupu fixture output currently includes thread title, main post content, source/author, created time, permalink, light/upvote count, reply count, and visible fixture replies normalized to `RawComment`.
- Tieba fixture output currently includes thread title, main post content, source/author, created time, permalink, like/upvote count, reply count, and visible fixture replies normalized to `RawComment`; floor numbers are stored in `RawComment.raw_data.floor_number`.
- NGA fixture output currently includes thread title, main post content, source/author, created time, permalink, like/upvote count, reply count, and visible fixture replies normalized to `RawComment`; floor numbers are stored in `RawComment.raw_data.floor_number`.
- Public parser metadata may include `source_type`, `parser_status`, `live_fetch_enabled`, `live_fetch_attempted`, `live_fetch_allowed`, `fetch_status`, `schema_valid`, `fallback_used`, and `fallback_reason_category`.
- `fallback_reason_category` and `sanitized_error_category` are intentionally coarse and safe: `api_pending`, `dependency_error`, `auth_error`, `quota_error`, `comments_unavailable`, `network_error`, `parsing_error`, `config_error`, or `adapter_error`. They must never include credentials, tokens, or secret values.
- Public parser fallback categories may also include `fixture_only`, `live_fetch_disabled`, `selector_missing`, `robots_disallowed`, `robots_unavailable_or_unclear`, `path_not_allowed_by_profile`, or `http_error`.
- `exception_class` is a safe class name only, for example `ResponseException` or `JSONDecodeError`; it must not include exception messages or secret-bearing request data.
- `real_mode_reached` indicates whether the adapter reached the real API code path.
- `dependency_available` indicates whether required adapter dependencies such as PRAW are available.
- `real_mode_blocked_reason` may be `api_pending`, `disabled`, `mock_only`, `credentials_missing`, `approval_required`, or `null`.
- Official API planned platforms still use mock behavior by default. YouTube is the only current credential-gated real-capable official API adapter. Crawler-later platforms are not activated for real crawling.

Example public-parser fixture metadata:

```json
{
  "platform": "the_paper",
  "adapter_mode": "mock",
  "source_type": "public_page_parser",
  "parser_status": "fixture_only",
  "live_fetch_enabled": false,
  "live_fetch_attempted": false,
  "live_fetch_allowed": false,
  "fallback_used": true,
  "fallback_reason_category": "live_fetch_disabled",
  "fetch_status": "disabled",
  "mock_available": true,
  "real_mode_available": false,
  "api_approval_required": false,
  "api_approval_status": "not_applicable",
  "api_pending": false,
  "real_mode_disabled": true,
  "selectable_for_real": false,
  "real_mode_blocked_reason": "live_fetch_disabled",
  "post_count": 3,
  "comment_count": 0,
  "schema_valid": true,
  "raw_post_schema_valid": true,
  "raw_comment_schema_valid": true
}
```

Example The Paper live-pilot metadata with mocked/successful public HTML:

```json
{
  "platform": "the_paper",
  "adapter_mode": "mock",
  "source_type": "public_page_parser",
  "parser_status": "fixture_only",
  "live_fetch_enabled": true,
  "live_fetch_attempted": true,
  "live_fetch_allowed": true,
  "fallback_used": false,
  "fallback_reason_category": null,
  "fetch_status": "ok",
  "post_count": 1,
  "comment_count": 0,
  "schema_valid": true,
  "raw_post_schema_valid": true,
  "raw_comment_schema_valid": true
}
```

## 3. Run Analysis

### Endpoint

```http
POST /api/v1/analysis/run
```

### Request

```json
{
  "project_id": "project_001",
  "analysis_types": [
    "sentiment",
    "topic",
    "bot",
    "ai_generated",
    "propagation",
    "risk"
  ]
}
```

### Response

```json
{
  "project_id": "project_001",
  "analysis_task_id": "analysis_task_001",
  "status": "queued",
  "message": "Analysis task created. Mock analysis will be returned in MVP mode."
}
```

## 4. Get Analysis Result

### Endpoint

```http
GET /api/v1/analysis/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "summary": "Current public opinion is mainly negative and focused on product quality.",
  "sentiment": {
    "positive_ratio": 0.12,
    "neutral_ratio": 0.16,
    "negative_ratio": 0.72,
    "average_sentiment_score": -0.68
  },
  "topics": [],
  "conflicts": [],
  "bot_score": {
    "suspected_bot_ratio": 0.24,
    "suspected_bot_comment_ratio": 0.39
  },
  "risk": {
    "risk_score": 87,
    "risk_level": "high"
  },
  "risk_model_version": "v1_5_topic_risk_mvp",
  "topic_risks": [],
  "top_risk_topics": [],
  "max_topic_risk": 52.2,
  "average_topic_risk": 41.8,
  "overall_risk": 48.56,
  "real_crisis_risk": 50.4,
  "manipulation_risk": 31.0,
  "risk_explanation": "V1.5 topic risk identifies the leading risk topic and separates crisis/manipulation signals."
}
```

Important:

- `risk`, `risk_score`, and `risk_level` remain backward-compatible project-level fields.
- When topic clusters exist, mock-first analysis responses may also include the V1.5 topic-risk extension fields.
- `topic_risks` and `top_risk_topics` use the same item shape documented in the V1.5 Topic Risk Extension section below.
- `risk_model_version="v1_5_topic_risk_mvp"` means the response includes the deterministic V1.5 topic-level mock risk layer.

## 5. Visualization Data

### Endpoint

```http
POST /api/v1/visualization/data
```

### Request

```json
{
  "project_id": "project_001",
  "date_range": {
    "start": "2026-05-01",
    "end": "2026-05-13"
  },
  "platforms": ["reddit", "weibo"]
}
```

### Response

```json
{
  "project_id": "project_001",
  "risk_score": 87,
  "risk_level": "high",
  "risk_model_version": "v1_static_mvp",
  "sentiment_trend": [
    {
      "time": "2026-05-13T10:00:00Z",
      "positive": 12,
      "neutral": 20,
      "negative": 68
    }
  ],
  "risk_radar": {
    "negative_sentiment": 0.72,
    "bot_impact": 0.61,
    "propagation_speed": 0.84,
    "controversy": 0.78,
    "trend_shift": 0.67
  },
  "heatmap": [],
  "propagation_graph": {
    "nodes": [],
    "edges": []
  },
  "topic_clusters": [],
  "bot_impact": {
    "suspected_bot_ratio": 0.24,
    "suspected_bot_comment_ratio": 0.39
  }
}
```

Important:

- The frontend must not assume fields that are not defined here.
- The backend must keep this schema stable.
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5-compatible visualization responses may set `risk_model_version` to `v1_5_topic_risk_mvp` and include backward-compatible optional fields: `topic_risks`, `top_risk_topics`, `max_topic_risk`, `average_topic_risk`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.
- If schema changes are required, update this file and frontend API transformation together.

### V1.5 Topic Risk Extension

When the V1.5 topic-level mock model is available, visualization/report responses may include:

```json
{
  "risk_model_version": "v1_5_topic_risk_mvp",
  "topic_risks": [
    {
      "topic_id": "topic_001",
      "cluster_id": "topic_001",
      "topic": "Product quality issues",
      "comment_count": 56,
      "negative_ratio": 0.72,
      "average_sentiment_score": -0.74,
      "neg_severity": 0.53,
      "spread_signal": 0.84,
      "controversy_signal": 0.18,
      "bot_signal": 0.31,
      "influence_proxy": 0.62,
      "topic_risk_score": 52.2,
      "topic_risk_level": "medium",
      "risk_explanation": "Product quality issues has topic risk 52.2/100, mainly driven by spread.",
      "risk_score": 52.2,
      "risk_level": "medium"
    }
  ],
  "top_risk_topics": [],
  "max_topic_risk": 52.2,
  "average_topic_risk": 41.8,
  "overall_risk": 48.56,
  "real_crisis_risk": 50.4,
  "manipulation_risk": 31.0,
  "risk_explanation": "V1.5 topic risk identifies the leading risk topic and separates crisis/manipulation signals."
}
```

Risk level mapping for V1.5 topic risk:

```text
0-39   low
40-69  medium
70-84  high
85-100 critical
```

## 6. Summary Generation

### Endpoint

```http
POST /api/v1/summary/generate
```

### Request

```json
{
  "project_id": "project_001",
  "include_representative_comments": true,
  "report_language": "zh-CN"
}
```

### Response

```json
{
  "project_id": "project_001",
  "report_language": "zh-CN",
  "risk_score": 87,
  "risk_level": "high",
  "risk_level_label": "高风险",
  "risk_model_version": "v1_static_mvp",
  "overall_summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "key_findings": [
    "负面情绪占比较高，当前为72%。",
    "负面议题：Product quality issues：356条评论，平均情绪-0.74",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。",
    "传播速度信号较高，当前为84%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。",
    "发布事实性监测说明，承认主要关切，避免放大未经证实的信息。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true,
  "summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。"
}
```

Important:

- `report_language` defaults to `zh-CN`; `en-US` is optional.
- `risk_level` remains the raw English enum: `low`, `medium`, `high`, or `critical`.
- `risk_level_label` is a display label. For `zh-CN`, use `低风险`, `中等风险`, `高风险`, or `严重风险`.
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5 report responses may use `risk_model_version="v1_5_topic_risk_mvp"` and include the optional topic-risk extension fields documented above.
- `summary` is retained as a backward-compatible alias for `overall_summary`.
- Representative comments preserve their original text and are not translated by the report builder.

## 7. Recommendation Generation

### Endpoint

```http
POST /api/v1/recommendation/generate
```

### Request

```json
{
  "project_id": "project_001",
  "user_type": "brand",
  "tone": "professional",
  "report_language": "zh-CN"
}
```

### Response

```json
{
  "project_id": "project_001",
  "report_language": "zh-CN",
  "risk_score": 87,
  "risk_level": "high",
  "risk_level_label": "高风险",
  "risk_model_version": "v1_static_mvp",
  "overall_summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "key_findings": [
    "负面情绪占比较高，当前为72%。",
    "负面议题：Product quality issues：356条评论，平均情绪-0.74",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。",
    "传播速度信号较高，当前为84%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。",
    "发布事实性监测说明，承认主要关切，避免放大未经证实的信息。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true,
  "summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "main_risks": [
    "负面情绪占比较高，当前为72%。",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "suggested_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。"
}
```

Important:

- `main_risks` and `suggested_response` are retained for backward compatibility.
- New frontend code should prefer `main_risk_factors`, `suspected_bot_signals`, and `suggested_public_response`.

## 8. Propagation Graph

### Endpoint

```http
GET /api/v1/propagation/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "nodes": [
    {
      "node_id": "post_001",
      "type": "post",
      "platform": "weibo",
      "content": "Original post content",
      "author_id": "user_hash_001",
      "created_at": "2026-05-13T10:00:00Z",
      "sentiment_score": -0.72,
      "influence_score": 0.88
    }
  ],
  "edges": [
    {
      "source": "post_001",
      "target": "comment_002",
      "relation": "reply",
      "weight": 0.64
    }
  ],
  "metrics": {
    "depth": 4,
    "breadth": 128,
    "central_node_id": "post_001",
    "propagation_speed": 0.84
  }
}
```

## 9. Alerts

### List Persisted Case Alert Events

```http
GET /api/v1/alerts
```

Response:

```json
[
  {
    "alert_id": "alert_case_001_snapshot_002_001",
    "case_id": "case_001",
    "snapshot_id": "case_001_snapshot_002",
    "level": "warning",
    "alert_type": "risk_score_increase",
    "message": "总体风险分上升 12.0 分。",
    "reason": "最新快照相对上一轮出现明显风险增量，建议优先复核高风险话题和传播信号。",
    "created_at": "2026-05-14T09:08:00Z",
    "resolved": false,
    "metadata": {
      "risk_score_delta": 12.0
    }
  }
]
```

This endpoint returns alert events generated by case monitoring checks. It is local/mock-first and does not send real notifications.

### Legacy Mock Project Alerts

### Endpoint

```http
GET /api/v1/alerts/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "alerts": [
    {
      "alert_id": "alert_001",
      "level": "high",
      "message": "Negative sentiment increased by more than 30% in the last hour.",
      "created_at": "2026-05-13T11:00:00Z",
      "resolved": false
    }
  ]
}
```

## 10. Analysis Cases

Case APIs are lightweight MVP endpoints for saving mock analysis contexts during local development. The default store is project-local JSON at `backend/data/cases.json` through the case repository/storage abstraction. Optional MongoDB persistence is available only when `CASE_STORE_BACKEND=mongodb`; the default local MVP does not require MongoDB, Redis, authentication, real crawlers, real platform APIs, or external LLM APIs.

Persistence notes:

- Default backend: `CASE_STORE_BACKEND=local_json`.
- Default path: `CASE_STORE_PATH=backend/data/cases.json`.
- Runtime case JSON files are ignored by git via `backend/data/*.json` and `backend/data/*.json.tmp`.
- Tests must use temporary paths and must not write to the real local demo store.
- Optional MongoDB store: set `CASE_STORE_BACKEND=mongodb`, `MONGODB_URI`, and `MONGODB_DATABASE`.
- Redis remains a future TODO behind the same repository/interface boundary.

### List Cases

```http
GET /api/v1/cases
```

Response:

```json
[
  {
    "case_id": "case_001",
    "project_id": "project_001",
    "title": "Tesla 舆情分析",
    "keyword": "Tesla",
    "platforms": ["reddit", "weibo", "bilibili"],
    "status": "completed",
    "created_at": "2026-05-14T09:00:00Z",
    "updated_at": "2026-05-14T09:02:00Z",
    "risk_score": 52.2,
    "risk_level": "medium",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "report_language": "zh-CN"
  }
]
```

### Create Case

```http
POST /api/v1/cases
```

Request:

```json
{
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "report_language": "zh-CN"
}
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "status": "draft",
  "monitoring_config": {
    "enabled": false,
    "interval_minutes": 60,
    "last_run_at": null,
    "next_run_at": null,
    "threshold_config": {
      "risk_score_delta_warning": 10,
      "risk_score_delta_critical": 20,
      "real_crisis_delta_warning": 10,
      "manipulation_delta_warning": 15,
      "topic_risk_high": 70,
      "topic_risk_critical": 85
    },
    "status": "disabled"
  },
  "analysis_result": null,
  "visualization_data": null,
  "report": null,
  "markdown_available": false,
  "raw_posts": [],
  "raw_comments": [],
  "crawl_metadata": [],
  "crawl_source_mode": null,
  "crawl_attached_at": null,
  "raw_data_status": "missing",
  "analysis_input_source": null,
  "raw_post_count": 0,
  "raw_comment_count": 0
}
```

### Get Case Detail

```http
GET /api/v1/cases/{case_id}
```

Response contains the same metadata as Create Case. After a run, `analysis_result`, `visualization_data`, `report`, and `markdown_available` are populated.

### Start Case Crawl and Attach Raw Data

```http
POST /api/v1/cases/{case_id}/crawl/start
```

This endpoint explicitly attaches normalized crawl output to one case. It uses the case keyword and selected platforms by default, or safe request overrides when provided. It calls the same adapter layer as `POST /api/v1/crawl/start`, stores `raw_posts`, `raw_comments`, and safe `crawl_metadata` on the case, and returns the updated case detail.

Request:

```json
{
  "keyword": "Tesla",
  "platforms": ["youtube"],
  "limit": 3,
  "date_range": null
}
```

All fields are optional. If omitted, `keyword` and `platforms` come from the case.

Response additions on `AnalysisCaseDetail`:

```json
{
  "raw_posts": [],
  "raw_comments": [],
  "crawl_metadata": [
    {
      "platform": "youtube",
      "adapter_mode": "real",
      "source_type": "youtube_data_api_v3",
      "credential_present": true,
      "post_count": 3,
      "comment_count": 3,
      "raw_post_schema_valid": true,
      "raw_comment_schema_valid": true
    }
  ],
  "crawl_source_mode": "case_crawl_start",
  "crawl_attached_at": "2026-05-18T10:00:00Z",
  "raw_data_status": "attached",
  "raw_post_count": 3,
  "raw_comment_count": 3
}
```

Rules:

- The endpoint must not expose credential values; `credential_present` is a boolean only.
- Real YouTube calls can occur only during manual local smoke when `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` are configured in ignored local environment files.
- Automated tests must mock adapter/client output and must not call the real YouTube API.
- Case creation and case run do not automatically crawl.

### Universal Evidence Ingestion

```http
GET /api/v1/cases/{case_id}/evidence
POST /api/v1/cases/{case_id}/evidence/attach
GET /api/v1/cases/{case_id}/evidence/trust-summary
GET /api/v1/cases/{case_id}/evidence/dedup-summary
GET /api/v1/cases/{case_id}/evidence/summary
GET /api/v1/cases/{case_id}/evidence/jobs
GET /api/v1/cases/{case_id}/evidence/coverage
GET /api/v1/cases/{case_id}/evidence/review-queue
GET /api/v1/cases/{case_id}/evidence/review-summary
GET /api/v1/cases/{case_id}/evidence/review-timeline
GET /api/v1/cases/{case_id}/evidence/review-audit-summary
GET /api/v1/cases/{case_id}/evidence/{evidence_id}/review-history
POST /api/v1/cases/{case_id}/evidence/{evidence_id}/review
```

`GET /cases/{case_id}/evidence` returns a normalized case-level evidence view. If a case has `evidence_items`, the endpoint returns them directly. If the case only has `raw_posts` / `raw_comments`, it derives evidence items from those raw records. If neither exists, it returns `status="empty"`.

`POST /cases/{case_id}/evidence/attach` accepts safe manual/user-provided evidence such as article title/body, video title/description, comments, replies, public URLs, public author labels, and interaction metrics. It does not fetch external URLs and does not call platform APIs.

Manual URL evidence is a first-class safe attach mode. It uses the same attach endpoint with `acquisition_mode="manual_url"` and stores the URL as plain text review context only. The backend does not fetch the URL, follow links, run a parser, use cookies, scrape, call real APIs, or call real LLM APIs. At least one of `title`, `body_text`, or `comment_text` is required for every manual URL evidence item. Secret-like pasted values in manual text fields are redacted before storage/output; invalid numeric metrics are coerced to `0` and returned with warnings.

Trust and dedup endpoints are read-only summaries over normalized case evidence. They expose only aggregate distributions and hash/group identifiers; they do not expose credentials, fetch sources, or verify screenshots.

Batch and coverage endpoints are read-only local summaries:

- `GET /cases/{case_id}/evidence/summary` returns total, unique, duplicate, source, acquisition-mode, trust, verification, and review-status distributions, latest ingestion jobs, latest review events, rejected evidence count, weak/unverified evidence count, and the coverage note `This is coverage of imported/available evidence, not full platform coverage.`
- `GET /cases/{case_id}/evidence/jobs` returns lightweight local job records created by CSV/XLSX import commits and manual evidence attach calls.
- `GET /cases/{case_id}/evidence/coverage` returns platforms/source types/acquisition modes/time range/counts for currently available case evidence only.

These endpoints do not start background workers, call real APIs, call search providers, fetch URLs, scrape pages, persist raw uploaded files, expose secrets, or claim full all-web/platform coverage.

Review endpoints implement a human review workflow only. They do not run AI review, verify screenshot authenticity, fetch source URLs, call real search/platform APIs, or call real LLM APIs. The review queue includes low-trust, unverified, screenshot/transcription, source-url-missing, duplicate, attestation-missing, and risk-flagged evidence.

Review decision request:

```json
{
  "decision": "reject",
  "reviewer_label": "local_reviewer",
  "notes": "Screenshot transcription without a source URL."
}
```

Supported `decision` values:

- `approve`
- `reject`
- `mark_weak`
- `request_more_source`
- `merge_duplicate`
- `reset_review`

Review decision effects:

- `approve` sets `review_status=approved` and keeps evidence usable.
- `reject` sets `review_status=rejected`, keeps the normalized evidence stored, and excludes it from default analysis and representative comments.
- `mark_weak` keeps evidence usable while surfacing a weak-evidence warning.
- `request_more_source` keeps evidence visible but flags it for better source context.
- `merge_duplicate` preserves duplicate grouping and duplicate-collapse behavior.
- `reset_review` returns review state to the computed default based on risk flags.

Review summary response includes `total_items`, `queue_count`, `review_needed_count`, `low_trust_count`, `duplicate_group_count`, `missing_source_count`, `screenshot_count`, `approved_count`, `rejected_count`, `marked_weak_count`, `needs_more_source_count`, distributions for `review_status`, `review_reason_codes`, `trust_label`, `verification_status`, and `provenance_type`, plus `safe_mode` flags.

Review history and audit responses:

- `GET /cases/{case_id}/evidence/{evidence_id}/review-history` returns an append-only timeline for one evidence item.
- `GET /cases/{case_id}/evidence/review-timeline` returns the latest review events across the case.
- `GET /cases/{case_id}/evidence/review-audit-summary` returns counts for approve/reject/mark weak/request source/merge duplicate/reset decisions, latest reviewed time, and evidence-with-history count.

History entries include `previous_review_status`, `new_review_status`, `decision`, `reason_code`, `reviewer_label`, `reviewed_at`, redacted `note`, trust/verification before-after fields, `analysis_effect`, and safe-mode flags. The audit trail is human-review-only; it does not fetch URLs, call real APIs, call real LLMs, or claim AI/platform authenticity verification.

If analysis is based on `case_evidence_items`, rejected evidence is excluded by default. `case_raw_data` still takes priority when attached raw comments exist, and mock fallback remains unchanged when neither raw data nor evidence exists.

Manual URL request:

```json
{
  "source": {
    "platform": "manual_url",
    "source_type": "public_web",
    "acquisition_mode": "manual_url",
    "source_name": "Manual URL evidence",
    "source_url": "https://example.test/public-thread",
    "credential_present": false
  },
  "evidence_items": [
    {
      "evidence_type": "comment",
      "title": "Public discussion thread",
      "comment_text": "用户认为官方回应太慢，希望看到明确进展。",
      "author_name": "Public author label",
      "url": "https://example.test/public-thread",
      "like_count": 12,
      "reply_count": 3,
      "provenance_type": "manual_url",
      "verification_status": "needs_review",
      "source_capture_method": "manual_copy_from_public_page",
      "user_attestation_text": "I confirm I have the right to submit this public-opinion evidence.",
      "raw_data_safe": {
        "manual_entry": true,
        "no_url_fetch": true
      }
    }
  ]
}
```

Manual URL validation failure:

```json
{
  "detail": {
    "error": "evidence_attach_rejected",
    "message": "manual_evidence_text_required",
    "real_api_calls": false,
    "real_llm_calls": false,
    "url_fetching": false
  }
}
```

CSV / Excel import endpoints:

```http
GET /api/v1/evidence/import/template.csv
POST /api/v1/cases/{case_id}/evidence/import/preview
POST /api/v1/cases/{case_id}/evidence/import/commit
```

`GET /evidence/import/template.csv` returns a static UTF-8 CSV attachment named `sentigraph_evidence_import_template.csv`. It includes the recommended evidence import headers plus safe sample rows for article, video, and comment evidence. It does not read case data, does not expose credentials, does not fetch external sources, and does not call real APIs.

These endpoints implement a stateless upload-confirm flow: the frontend reads the selected file locally, sends `filename`, `content_base64`, and optional `column_mapping`, then the backend parses the bytes in memory. Preview returns normalized row samples and warnings. Commit saves only sanitized `EvidenceItem` records on the case; the original uploaded file is not persisted by default.

Request:

```json
{
  "filename": "sample_evidence.csv",
  "content_base64": "base64-encoded CSV or XLSX bytes",
  "column_mapping": {
    "platform": "platform",
    "title": "title",
    "comment_text": "comment_text",
    "author_name": "author_name",
    "url": "url",
    "created_at": "created_at",
    "like_count": "like_count",
    "reply_count": "reply_count"
  },
  "preview_limit": 10,
  "max_rows": 500
}
```

Preview response includes `detected_format`, `detected_columns`, confirmed `column_mapping`, `valid_row_count`, `duplicate_row_count`, `skipped_row_count`, `preview_rows`, warnings, and safe-mode flags. Commit response includes `imported_count`, `total_evidence_item_count`, imported `evidence_items`, source/type distributions, warnings, and the same safe-mode flags.

Import commit also records an `EvidenceIngestionJob` on the case. The job includes `job_id`, `case_id`, `status`, `source_type`, `acquisition_mode`, `input_type`, row counts, warning/review-needed counts, timestamps, progress, and safe metadata such as `raw_file_persisted=false`, `formulas_executed=false`, `url_fetching=false`, and `scraping=false`.

Optional CSV/Excel mapping fields now include `provenance_type`, `verification_status`, `source_capture_method`, and `user_attestation`. Missing attestation is allowed but records `user_attestation_missing` and lowers trust/review status for user-uploaded evidence.

Import rules:

- Supported formats: CSV, UTF-8 / UTF-8-BOM CSV, GB18030 / GBK CSV fallback, and macro-free `.xlsx`.
- Rejected formats: `.xls`, `.xlsm`, `.xlsb`, unknown binaries, macros, executable content, and oversized files.
- Cells beginning with `=`, `+`, `-`, or `@` are treated as plain text; formulas are not executed.
- Secret-like columns or values such as `api_key`, `access_token`, `refresh_token`, `client_secret`, `password`, and `cookie` are redacted or omitted.
- Duplicate rows are deduped by deterministic content hash.
- Imported evidence uses `acquisition_mode="user_upload"` and `source_type="uploaded_dataset"` by default.
- Case analysis uses imported `evidence_items` only when no attached raw comments are available; `case_raw_data` still wins over uploaded evidence.

Request:

```json
{
  "source": {
    "platform": "uploaded_dataset",
    "source_type": "uploaded_dataset",
    "acquisition_mode": "user_upload",
    "source_name": "Manual evidence sheet",
    "credential_present": false
  },
  "evidence_items": [
    {
      "evidence_type": "article",
      "title": "Public article title",
      "body_text": "Public article body.",
      "url": "https://example.test/article"
    },
    {
      "evidence_type": "comment",
      "comment_text": "Public or user-provided comment text.",
      "root_id": "article_or_video_id"
    }
  ]
}
```

Response:

```json
{
  "case_id": "case_001",
  "status": "attached",
  "evidence_item_count": 2,
  "source_distribution": {
    "uploaded_dataset": 2
  },
  "evidence_type_counts": {
    "article": 1,
    "comment": 1
  },
  "top_titles": ["Public article title"],
  "representative_comments": ["Public or user-provided comment text."],
  "trust_summary": {
    "trust_label_distribution": {"unverified": 1, "medium": 1},
    "verification_status_distribution": {"needs_review": 1, "source_url_provided_unverified": 1},
    "provenance_type_distribution": {"manual_url": 2},
    "warning_counts": {"user_attestation_missing": 1},
    "review_needed_count": 1,
    "low_trust_count": 0,
    "unverified_count": 1
  },
  "deduplication_summary": {
    "total_items": 3,
    "unique_items": 2,
    "duplicate_items": 1,
    "duplicate_group_count": 1,
    "top_duplicate_groups": []
  },
  "safe_mode": {
    "secrets_exposed": false,
    "real_api_calls": false,
    "real_llm_calls": false,
    "scraping_bypass": false
  }
}
```

Rules:

- Evidence attachment is normalization only; it does not call real APIs, crawlers, external LLMs, or live public fetch.
- Trust labels are deterministic provenance labels, not truth guarantees. Screenshots/transcriptions are never automatically verified.
- Exact duplicate text/URL submissions are collapsed within a case. `duplicate_count` / `duplicate_group_size` remain available as repetition signals, but unique evidence is used for default analysis counts.
- `raw_data_safe` is sanitized; API keys, tokens, cookies, authorization headers, client secrets, passwords, credentials, and `.env` values are removed.
- `evidence_type="interaction_metric"` is accepted for standalone metric evidence; `interaction_metrics` is kept as a backward-compatible alias.
- `analysis_input_source="case_evidence_items"` is used when case analysis consumes attached evidence items and no raw comments are present.
- Existing YouTube case raw-data analysis remains `analysis_input_source="case_raw_data"` when attached `raw_comments` are available.
- Output remains aggregate/case-level and must not expose individual targeting recommendations or account-level influenceability scores.

### Source Catalog

```http
GET /api/v1/sources/catalog
```

Returns static source readiness/planning metadata for all-web public-opinion evidence ingestion. This endpoint does not call real APIs, read credentials, fetch URLs, run crawlers, use cookies, call LLMs, or enable live public fetching.

Response:

```json
{
  "categories": [
    {
      "category_id": "video_platforms",
      "display_name": "Video Platforms",
      "description": "Public video/post metadata and comments through official APIs, OAuth, user upload, or mock fixtures.",
      "sources": [
        {
          "source_id": "youtube",
          "display_name": "YouTube",
          "category": "video_platforms",
          "feasibility_status": "green",
          "acquisition_modes": ["official_api_public", "user_upload", "mock_fixture"],
          "allowed_data_types": ["video", "comment", "reply", "title", "body_text", "interaction_metric"],
          "forbidden_data_types": ["private_messages", "oauth_private_data", "cookie_session_data"],
          "current_status": "real_capable_when_configured",
          "compliance_notes": "Official YouTube Data API v3 only; default mock mode; cache and tiny-limit guardrails.",
          "next_action": "Keep local key in ignored environment files and use cached tiny demos.",
          "priority": "high"
        }
      ]
    }
  ],
  "total_categories": 12,
  "total_sources": 22,
  "safe_mode": {
    "static_metadata_only": true,
    "real_api_calls": false,
    "real_llm_calls": false,
    "live_fetch_enabled": false,
    "cookies_used": false,
    "scraping_bypass": false,
    "secrets_exposed": false,
    "third_party_crawler_integrated": false
  }
}
```

Important:

- The catalog is a planning/status endpoint, not a crawler.
- It returns source categories such as video platforms, news/media sites, forums, Q&A, complaints/reviews, finance/investor forums, social platforms, search discovery, RSS, user-uploaded datasets, manual URL evidence, and data-vendor future integration.
- It must not expose API keys, client secrets, OAuth tokens, cookies, `.env` values, or local secret paths.
- MediaCrawler is not integrated as a core source. Third-party crawler exports may only enter as user-provided datasets with lawful-source attestation.

### Search Discovery Static Status

```http
GET /api/v1/search-discovery/status
```

Returns static Search Discovery planning metadata. It does not call real search APIs, call website APIs, fetch URLs, scrape pages, use cookies, inspect `.env`, call real LLM APIs, or expose secrets.

Response includes:

- `status="planning_mock_only"`
- `provider_statuses`
- `review_flow`
- `next_actions`
- `safe_mode`

Provider classes covered by the status endpoint:

- search engine APIs
- news discovery APIs
- RSS / Atom feeds
- site-specific public search pages
- user-provided URL lists
- data vendor discovery indexes
- mock fixtures

`safe_mode` must keep `real_search_api_calls=false`, `real_website_api_calls=false`, `url_fetching=false`, `scraping=false`, `cookies_used=false`, `captcha_bypass=false`, `anti_bot_bypass=false`, `real_llm_calls=false`, `secrets_exposed=false`, and `third_party_crawler_integrated=false`.

### Search Discovery Mock Candidates

```http
GET /api/v1/search-discovery/mock-candidates?query=Tesla
```

Returns deterministic mock candidate URL/title/snippet metadata for UI planning and regression tests. The endpoint uses `example.test` URLs and never fetches them.

Response:

```json
{
  "query": "Tesla",
  "candidate_count": 4,
  "candidates": [
    {
      "candidate_id": "mock_search_tesla_article_001",
      "query": "Tesla",
      "provider": "mock_fixture",
      "platform_hint": "news_site",
      "title": "Tesla public article discussion",
      "snippet": "Mock discovery metadata only.",
      "url": "https://example.test/news/tesla-public-article",
      "published_at": "2026-05-25T08:00:00Z",
      "source_name": "Mock News Index",
      "content_type_hint": "article",
      "confidence": 0.82,
      "acquisition_mode": "search_discovery",
      "status": "pending_review",
      "safety_notes": ["mock fixture only", "URL was not fetched", "human review required before attach"]
    }
  ],
  "safe_mode": {
    "static_metadata_only": true,
    "mock_candidates_only": true,
    "real_search_api_calls": false,
    "real_website_api_calls": false,
    "url_fetching": false,
    "scraping": false,
    "cookies_used": false,
    "captcha_bypass": false,
    "anti_bot_bypass": false,
    "real_llm_calls": false,
    "secrets_exposed": false,
    "third_party_crawler_integrated": false
  }
}
```

Important:

- Search Discovery candidates are not automatically attached to a case.
- A human must review candidates before using candidate URLs/text as evidence.
- Accepted candidates should route to Manual URL Evidence, CSV/Excel import, or a separately reviewed public parser path.
- Full content extraction is not part of Search Discovery.

### Search Discovery Candidate Attach

```http
POST /api/v1/cases/{case_id}/search-discovery/candidates/attach
```

Accepts user-reviewed mock/static candidates and converts only accepted candidates into normalized `EvidenceItem` records. Rejected or still-pending candidates are not attached.

Request:

```json
{
  "candidates": [
    {
      "candidate_id": "mock_search_tesla_article_001",
      "query": "Tesla",
      "provider": "mock_fixture",
      "platform_hint": "news_site",
      "title": "Tesla public article discussion",
      "snippet": "Mock discovery metadata only.",
      "url": "https://example.test/news/tesla-public-article",
      "source_name": "Mock News Index",
      "content_type_hint": "article",
      "confidence": 0.82,
      "acquisition_mode": "search_discovery",
      "status": "accepted",
      "safety_notes": ["mock fixture only", "URL was not fetched"]
    }
  ],
  "reviewer_label": "local_demo_reviewer"
}
```

Attached evidence uses `acquisition_mode=search_discovery`, `provenance_type=search_discovery_candidate`, `verification_status=source_url_provided_unverified`, conservative trust, safe metadata only, and review-needed behavior. The endpoint does not call real search APIs, fetch URLs, scrape pages, use cookies, call real LLMs, expose secrets, or integrate MediaCrawler.

### Run Case

```http
POST /api/v1/cases/{case_id}/run
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "status": "completed",
  "risk_score": 52.2,
  "risk_level": "medium",
  "risk_model_version": "v1_5_topic_risk_mvp",
  "analysis_result": {
    "project_id": "project_001",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "topic_risks": [],
    "analysis_input_source": "case_raw_data",
    "raw_post_count": 3,
    "raw_comment_count": 3
  },
  "visualization_data": {
    "project_id": "project_001",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "top_risk_topics": []
  },
  "report": {
    "project_id": "project_001",
    "report_language": "zh-CN",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "overall_summary": "..."
  },
  "markdown_available": true
}
```

Important:

- `POST /api/v1/cases/{case_id}/run` uses attached case `raw_comments` when present; otherwise it uses the same deterministic offline mock pipeline as the existing analysis, visualization, summary, and recommendation APIs.
- `analysis_result.analysis_input_source` is `case_raw_data` when stored raw comments are used and `mock_data_fallback` when the run falls back to local mock data.
- Running a case must not trigger real crawlers or real platform APIs.
- Representative comments preserve original attached public comment text when `case_raw_data` is used.
- The response keeps V1.5 topic-risk fields inside `analysis_result`, `visualization_data`, and `report` where available.
- A case run also saves a local monitoring snapshot for the completed mock analysis.

### List Case Snapshots

```http
GET /api/v1/cases/{case_id}/snapshots
```

Response:

```json
[
  {
    "snapshot_id": "case_001_snapshot_001",
    "case_id": "case_001",
    "created_at": "2026-05-14T09:04:00Z",
    "run_index": 1,
    "risk_score": 52.2,
    "overall_risk": 52.2,
    "risk_level": "medium",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "real_crisis_risk": 50.4,
    "manipulation_risk": 31.0,
    "top_risk_topics": [],
    "summary": "Template-based mock public opinion summary."
  }
]
```

### Case Risk Forecast

```http
GET /api/v1/cases/{case_id}/forecast
POST /api/v1/cases/{case_id}/forecast/run
```

`GET` returns the latest deterministic forecast computed from persisted monitoring snapshots. `POST /forecast/run` computes the same forecast explicitly. Forecasts are derived views over local snapshots and do not call real platform APIs, real LLM APIs, crawlers, or live public fetch.

Response:

```json
{
  "case_id": "case_001",
  "forecast_status": "ready",
  "generated_at": "2026-05-17T12:03:00Z",
  "risk_model_version": "v1_5_topic_risk_mvp",
  "snapshot_count": 3,
  "latest_snapshot_id": "case_001_snapshot_003",
  "horizon": "next_check",
  "latest_risk": 61.0,
  "moving_average": 46.0,
  "slope": 14.5,
  "acceleration": 3.0,
  "volatility": 9.67,
  "trend_direction": "rising",
  "forecast_confidence": "medium_low",
  "predicted_risk_score": 77.0,
  "predicted_risk_level": "high",
  "predicted_real_crisis_risk": 46.0,
  "predicted_manipulation_risk": 30.5,
  "real_crisis_trend_direction": "rising",
  "manipulation_trend_direction": "rising",
  "risk_forecasts": [
    {
      "horizon": "next_check",
      "predicted_risk_score": 77.0,
      "predicted_risk_level": "high",
      "predicted_real_crisis_risk": 46.0,
      "predicted_manipulation_risk": 30.5,
      "trend_direction": "rising",
      "real_crisis_trend_direction": "rising",
      "manipulation_trend_direction": "rising",
      "forecast_confidence": "medium_low",
      "forecast_reason": "Deterministic MVP forecast for next_check uses latest risk 61.0, slope 14.5, and acceleration 3.0; predicted risk is 77.0/100."
    }
  ],
  "topic_forecasts": [
    {
      "topic_id": "topic_safety",
      "topic": "Safety concern",
      "current_topic_risk_score": 73.0,
      "predicted_topic_risk_score": 88.5,
      "predicted_topic_risk_level": "critical",
      "trend_direction": "rising",
      "risk_explanation": "Synthetic benchmark topic forecast signal.",
      "forecast_reason": "Topic forecast uses deterministic monitoring snapshot deltas for the same topic key."
    }
  ],
  "input_snapshots": [],
  "recommended_action": "风险预测呈上升趋势，建议提高监控频率并优先复核高风险话题。",
  "message": "Deterministic MVP 风险预测显示趋势上升，下一检查点预测风险为 77.0/100。"
}
```

When no snapshots exist, the endpoint returns `forecast_status="insufficient_history"`, `forecast_confidence="insufficient_history"`, and a recommendation to run monitoring checks first.

### Run Mock Monitoring Check

```http
POST /api/v1/cases/{case_id}/monitor/run
```

Response:

```json
{
  "case_id": "case_001",
  "status": "alerts_detected",
  "latest_snapshot": {
    "snapshot_id": "case_001_snapshot_002",
    "case_id": "case_001",
    "created_at": "2026-05-14T09:08:00Z",
    "run_index": 2,
    "risk_score": 64.2,
    "overall_risk": 64.2,
    "risk_level": "medium",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "real_crisis_risk": 58.4,
    "manipulation_risk": 47.0,
    "top_risk_topics": [],
    "summary": "Template-based mock public opinion summary."
  },
  "previous_snapshot": {
    "snapshot_id": "case_001_snapshot_001",
    "case_id": "case_001",
    "created_at": "2026-05-14T09:04:00Z",
    "run_index": 1,
    "risk_score": 52.2,
    "overall_risk": 52.2,
    "risk_level": "medium",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "real_crisis_risk": 50.4,
    "manipulation_risk": 31.0,
    "top_risk_topics": [],
    "summary": "Template-based mock public opinion summary."
  },
  "alerts": [],
  "snapshot_count": 2,
  "latest_risk_delta": 12.0,
  "latest_risk_level": "medium",
  "message": "本轮监控触发 1 条预警事件。"
}
```

Monitoring checks remain deterministic and offline. Repeated checks create slightly shifted mock snapshots based on the snapshot index so local demos can show trend and alert behavior without random data.

### List Case Alerts

```http
GET /api/v1/cases/{case_id}/alerts
```

Response:

```json
[
  {
    "alert_id": "alert_case_001_snapshot_002_001",
    "case_id": "case_001",
    "snapshot_id": "case_001_snapshot_002",
    "level": "warning",
    "alert_type": "risk_score_increase",
    "message": "总体风险分上升 12.0 分。",
    "reason": "最新快照相对上一轮出现明显风险增量，建议优先复核高风险话题和传播信号。",
    "created_at": "2026-05-14T09:08:00Z",
    "resolved": false,
    "metadata": {}
  }
]
```

## 10.1 Monitoring Scheduler Foundation

The v0.8 scheduler foundation stores monitoring configuration and scheduler job state, but it does not start a real background worker. Local demos should use the manual `run-due` endpoint to simulate scheduler behavior.

### Get Scheduler Status

```http
GET /api/v1/scheduler/status
```

Response:

```json
{
  "background_scheduler_running": false,
  "total_cases": 1,
  "enabled_cases": 1,
  "due_cases": 1,
  "next_due_at": null,
  "job_states": [
    {
      "case_id": "case_001",
      "title": "Tesla 舆情案例",
      "keyword": "Tesla",
      "enabled": true,
      "interval_minutes": 60,
      "last_run_at": null,
      "next_run_at": "2026-05-14T09:05:00Z",
      "status": "due",
      "is_due": true,
      "snapshot_count": 1,
      "alert_count": 0
    }
  ],
  "message": "Manual scheduler foundation is configured; no background worker is running."
}
```

### Run Due Monitoring Jobs

```http
POST /api/v1/scheduler/run-due
```

Behavior:

- Finds cases with monitoring enabled.
- Runs only jobs whose `next_run_at` is due.
- Calls the existing deterministic mock monitoring check.
- Saves snapshots and alert events.
- Updates `last_run_at` and `next_run_at`.
- Does not run a background scheduler or real platform collection.

Response:

```json
{
  "checked_at": "2026-05-14T09:06:00Z",
  "due_case_count": 1,
  "executed_case_count": 1,
  "skipped_case_count": 0,
  "monitoring_results": [],
  "job_states": [],
  "message": "Executed 1 due monitoring job(s)."
}
```

### Get Case Monitoring Config

```http
GET /api/v1/cases/{case_id}/monitoring/config
```

Response:

```json
{
  "enabled": false,
  "interval_minutes": 60,
  "last_run_at": null,
  "next_run_at": null,
  "threshold_config": {
    "risk_score_delta_warning": 10,
    "risk_score_delta_critical": 20,
    "real_crisis_delta_warning": 10,
    "manipulation_delta_warning": 15,
    "topic_risk_high": 70,
    "topic_risk_critical": 85
  },
  "status": "disabled"
}
```

### Update Case Monitoring Config

```http
PUT /api/v1/cases/{case_id}/monitoring/config
```

Request and response use `MonitoringScheduleConfig`. When `enabled=true` and `next_run_at` is missing, the backend schedules the case as due immediately for manual local testing.

### Enable Case Monitoring

```http
POST /api/v1/cases/{case_id}/monitoring/enable
```

Enables the case and sets `next_run_at` to the deterministic repository clock so `POST /api/v1/scheduler/run-due` can run it in the local MVP.

### Disable Case Monitoring

```http
POST /api/v1/cases/{case_id}/monitoring/disable
```

Disables scheduled monitoring for the case and clears `next_run_at`.

### Export Markdown Report

```http
GET /api/v1/cases/{case_id}/report/markdown
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "filename": "Tesla_舆情案例_case_001.md",
  "markdown": "# Tesla 舆情案例\n\n## 舆情总览\n...",
  "generated_at": "2026-05-14T09:03:00Z"
}
```

The Markdown report includes title, keyword, selected platforms, risk score, risk level, risk model version, overall summary, key findings, top risk topics, representative comments, suspected bot/repeated-script signals, recommended actions, and suggested public response.

## 10.2 Notification Outbox Foundation

The v0.9 notification foundation converts persisted alert events into local notification outbox items. It is mock-first and offline: no real email, Slack, webhook, SMS, Enterprise WeChat, Feishu, or push API is called.

Notifications are created when alerts are generated by:

- `POST /api/v1/cases/{case_id}/monitor/run`
- `POST /api/v1/scheduler/run-due`

Duplicate notifications are avoided by using a deterministic notification id derived from the alert id and channel type.

### List Notifications

```http
GET /api/v1/notifications
```

Response:

```json
[
  {
    "notification_id": "notification_alert_case_001_snapshot_002_001_in_app",
    "alert_id": "alert_case_001_snapshot_002_001",
    "case_id": "case_001",
    "level": "warning",
    "title": "舆情风险预警",
    "message": "舆情风险出现上升，请关注该案例。",
    "channel_type": "in_app",
    "status": "pending",
    "created_at": "2026-05-14T09:08:00Z",
    "read_at": null,
    "simulated_sent_at": null,
    "metadata": {
      "alert_type": "risk_score_increase",
      "reason": "risk delta exceeded threshold",
      "snapshot_id": "case_001_snapshot_002"
    }
  }
]
```

### List Case Notifications

```http
GET /api/v1/cases/{case_id}/notifications
```

Returns the same `NotificationOutboxItem` shape, filtered by case.

### Mark Notification Read

```http
POST /api/v1/notifications/{notification_id}/read
```

Sets `read_at` using the deterministic local repository clock. This does not send any external message.

### Simulate Send Notification

```http
POST /api/v1/notifications/{notification_id}/simulate-send
```

Response:

```json
{
  "notification_id": "notification_alert_case_001_snapshot_002_001_in_app",
  "channel_type": "in_app",
  "status": "simulated_sent",
  "simulated": true,
  "simulated_sent_at": "2026-05-14T09:09:00Z",
  "message": "通知已完成本地模拟发送，未调用任何外部通道。",
  "notification": {
    "notification_id": "notification_alert_case_001_snapshot_002_001_in_app",
    "status": "simulated_sent",
    "simulated_sent_at": "2026-05-14T09:09:00Z"
  }
}
```

`notification` contains the updated `NotificationOutboxItem`. `simulated_sent_at` is also exposed at the top level for frontend state handling.

### Simulate Send All Pending

```http
POST /api/v1/notifications/simulate-send-pending
```

Returns a list of `NotificationSendResult` objects for pending notifications. This is a local state transition only.

### Get Outbox Status

```http
GET /api/v1/notifications/outbox/status
```

Response:

```json
{
  "total": 2,
  "unread": 2,
  "pending": 1,
  "simulated_sent": 1,
  "failed": 0,
  "mock_only": true,
  "channels": [
    {
      "channel_id": "in_app",
      "channel_type": "in_app",
      "display_name": "站内通知",
      "enabled": true,
      "mock_only": true,
      "notes": "MVP 本地通知，不发送外部消息。"
    }
  ],
  "message": "通知出箱仅用于本地模拟，不会发送真实外部消息。"
}
```

Supported channel types are `in_app`, `email_placeholder`, `webhook_placeholder`, `slack_placeholder`, `enterprise_wechat_placeholder`, and `feishu_placeholder`. Only `in_app` local notifications are active in the MVP.

## 10.3 Offline Benchmark Summary, History, and Regression

The benchmark endpoints are read-only local diagnostics endpoints. They read JSON summaries generated by `scripts/run_offline_benchmarks.py` and never start a benchmark run from the API.

```http
GET /api/v1/benchmarks/latest
```

Response when a summary exists:

```json
{
  "source": "offline_benchmark_summary",
  "available": true,
  "status": "available",
  "benchmark_id": "benchmark_20260517T000000z",
  "generated_at": "2026-05-17T00:00:00Z",
  "benchmark_version": "v4.0_offline_benchmark_v1",
  "duration_seconds": 0.74,
  "total_passed": 246,
  "total_failed": 0,
  "total_warnings": 0,
  "suites": [
    {
      "suite": "sentiment",
      "status": "pass",
      "case_count": 28,
      "passed": 28,
      "failed": 0,
      "warnings": []
    }
  ],
  "regression_detected": false,
  "message": "Latest offline benchmark summary loaded."
}
```

Response when no summary exists:

```json
{
  "source": "offline_benchmark_summary",
  "available": false,
  "status": "missing",
  "benchmark_id": null,
  "generated_at": null,
  "benchmark_version": null,
  "duration_seconds": null,
  "total_passed": 0,
  "total_failed": 0,
  "total_warnings": 0,
  "suites": [],
  "regression_detected": null,
  "message": "No offline benchmark summary found. Run python scripts/run_offline_benchmarks.py to generate it."
}
```

Benchmark history:

```http
GET /api/v1/benchmarks/history
```

Response:

```json
{
  "source": "offline_benchmark_history",
  "available": true,
  "status": "available",
  "total_entries": 2,
  "malformed_entries": 0,
  "entries": [
    {
      "source": "offline_benchmark",
      "benchmark_id": "benchmark_20260517T000000z",
      "generated_at": "2026-05-17T00:00:00Z",
      "benchmark_version": "v4.0_offline_benchmark_v1",
      "duration_seconds": 0.74,
      "total_passed": 246,
      "total_failed": 0,
      "total_warnings": 0,
      "suites": [],
      "regression_detected": false
    }
  ],
  "message": "Benchmark history loaded."
}
```

Regression comparison:

```http
GET /api/v1/benchmarks/regression
```

Response:

```json
{
  "source": "offline_benchmark_regression",
  "available": true,
  "status": "no_regression",
  "regression_detected": false,
  "changed_suites": [],
  "previous_benchmark_id": "benchmark_20260516T000000z",
  "latest_benchmark_id": "benchmark_20260517T000000z",
  "previous_generated_at": "2026-05-16T00:00:00Z",
  "latest_generated_at": "2026-05-17T00:00:00Z",
  "previous_total_failed": 0,
  "latest_total_failed": 0,
  "previous_total_warnings": 0,
  "latest_total_warnings": 0,
  "previous_total_passed": 246,
  "latest_total_passed": 246,
  "reason_categories": [],
  "message": "No benchmark regression detected compared with the previous run."
}
```

Rules:

- The endpoint reads only `.benchmarks/offline_benchmark_summary.json` under the project root.
- History is read only from `.benchmarks/history/` under the project root.
- The endpoints do not run benchmarks automatically.
- They return suite-level summary fields only: suite name, status, `case_count`, passed, failed, and warnings. They intentionally omit per-case benchmark payloads.
- They must not expose raw fixture text, raw HTML, prompts, raw user content, API keys, `.env` values, local file paths, or external request bodies.
- Missing or malformed summary/history files return safe `status="missing"` or `status="malformed"` responses with no traceback.
- Regression detection compares summary metadata only: increased total failures, increased warnings, suite `pass` to `fail`, and decreased total passed count.

## 10.6 Simulation Lab MVP Backend

The Simulation Lab MVP is an offline, deterministic, aggregate-level crisis-response simulation scaffold. It is a toy model for ethical scenario rehearsal, not a manipulation engine and not a guarantee about future public opinion.

It must not call real platform APIs, real LLM APIs, crawlers, live public fetch, notification providers, or external services.

### Run Simulation

```http
POST /api/v1/simulation/run
```

Request body: `SimulationScenario`.

Response body: `SimulationRunResult`.

The scenario may include synthetic agents, network edges, messages, and transparent intervention packages. The run result exposes aggregate metrics only.

Visibility and content-governance interventions are modeled only as lawful/platform-authorized, policy-based scenario variables. They are not execution endpoints and do not modify platform content.

Allowed intervention types:

- `clarification`
- `apology`
- `compensation`
- `faq`
- `progress_update`
- `third_party_evidence`
- `misinformation_correction`
- `no_response`
- `content_removal`
- `comment_closure`
- `account_restriction`
- `visibility_reduction`
- `platform_labeling`
- `policy_enforcement_notice`
- `content_removal_with_explanation`

Forbidden intervention types are rejected with HTTP `400`:

- `fake_consensus`
- `bot_amplification`
- `fake_event`
- `deceptive_distraction`
- `covert_influencer_seeding`
- `targeted_persuasion`
- `suppression`
- `illegal_suppression`
- `covert_censorship`
- `covert_suppression`
- `targeted_silencing`
- `platform_governance_evasion`

When a run uses `content_removal`, `visibility_reduction`, `platform_labeling`, or another allowed visibility intervention, `SimulationRunResult.visibility_intervention_result` may be present:

```json
{
  "intervention_type": "content_removal_with_explanation",
  "exposure_reduction": 68.44,
  "backlash_cost": 10.57,
  "trust_loss": 23.52,
  "spillover_risk": 24.28,
  "net_risk_change": 11.98,
  "removal_legitimacy_score": 78.2,
  "public_explanation_quality_score": 82.0,
  "neutral_audience_impact": 13.57,
  "opposition_group_impact": 23.82,
  "recommendation": "allowed_with_transparent_explanation",
  "human_review_required": true,
  "aggregate_level_only": true
}
```

`recommendation` is one of `not_recommended`, `conditional_human_review`, `allowed_with_transparent_explanation`, or `prefer_labeling_or_clarification`. It is a review cue only, not an automatic moderation command.

Example safe response shape:

```json
{
  "scenario_id": "simulation_brand_crisis_clarification",
  "scenario_name": "Brand Crisis Response Scenario",
  "simulation_status": "completed",
  "model_version": "simulation_lab_mvp_v1",
  "steps_requested": 6,
  "steps_completed": 6,
  "ethics_check": {
    "allowed": true,
    "reason": "All interventions passed the Simulation Lab ethics policy.",
    "blocked_categories": []
  },
  "final_metrics": {
    "average_latent_opinion": -0.3772,
    "average_expressed_opinion": -0.3323,
    "negative_ratio": 0.7,
    "neutral_ratio": 0.2,
    "positive_ratio": 0.1,
    "polarization_index": 0.2856,
    "attention_level": 0.5281,
    "trust_recovery_proxy": 0.4214,
    "intervention_effect_score": 0.0,
    "false_belief_proxy": 0.2956,
    "ethical_risk_flags": []
  },
  "safe_mode": {
    "aggregate_level_only": true,
    "real_api_calls": false,
    "real_llm_calls": false,
    "live_fetch_enabled": false,
    "individual_targeting": false
  }
}
```

### Demo Scenario

```http
GET /api/v1/simulation/demo-scenario
```

Returns a deterministic synthetic echo-chamber demo scenario. The endpoint does not fetch external data.

### Ethics Policy

```http
GET /api/v1/simulation/ethics-policy
```

Returns allowed intervention types, forbidden intervention types, a short policy summary, and `aggregate_level_only=true`. The policy endpoint is safe metadata only and does not expose credentials or environment values.

### Case-to-Simulation Initialization

```http
GET /api/v1/cases/{case_id}/simulation/initialization-preview
POST /api/v1/cases/{case_id}/simulation/initialize
```

Both endpoints build a deterministic `SimulationScenario` from an existing completed case analysis. They read only project-local aggregate case artifacts such as sentiment distribution, topic risks, top risk topics, monitoring snapshot count, alert count, and derived forecast status.

Behavior:

- If the case does not exist, return `404`.
- If the case has not been analyzed, return `400` with `error=case_analysis_required`.
- If optional data is missing, return a partial initialization with warnings rather than crashing.
- Do not call real platform APIs, real LLM APIs, crawlers, or live public fetchers.
- Do not expose named user targeting, account lists, private data, API keys, `.env` values, raw prompts, or automatic action execution.

Response includes:

- `event_frame`
- `audience_segments`
- `persona_clusters`
- `frame_gap_analysis`
- `strategy_implications`
- `simulation_scenario`
- `warnings`
- `safe_mode`

The generated `simulation_scenario.agents` are synthetic aggregate audience bubbles only. They are not real user accounts and must not be used for individual-level targeting.

The `event_frame.sub_issues` records expose both `topic_risk_score` and `risk_score` for compatibility with benchmark/UI consumers. `observed_frame_profile` exposes only aggregate real-crisis mappings such as `harm_salience`, `loss_sensitivity`, `moral_outrage_sensitivity`, and `crisis_legitimacy_pressure`; these are not individual profiles.

### Simulation Strategy Report Export

```http
POST /api/v1/simulation/report/markdown
```

Builds a safe Markdown strategy rehearsal report from an already-computed `SimulationRunResult` or A/B comparison result. The endpoint does not run a simulation, call real APIs, call real LLMs, enable live fetching, or execute any real-world action.

Request body: `SimulationStrategyReportRequest`.

Supported modes:

- `single`: requires `run_result` and `intervention_a`.
- `comparison`: requires `result_a`, `result_b`, `intervention_a`, and `intervention_b`; may include `comparison_summary`.

Response body: `SimulationStrategyReportResponse`:

- `report`: normalized report metadata.
- `markdown`: safe Markdown text.
- `safe_mode`: `aggregate_level_only=true`, `real_api_calls=false`, `real_llm_calls=false`, `live_fetch_enabled=false`, `individual_targeting=false`, `automatic_action_execution=false`.

The Markdown report includes:

- `# Simulation Lab Strategy Report`
- `## Scenario Overview`
- `## Intervention Comparison`
- `## Key Metrics`
- `## Audience Impact`
- `## Visibility Intervention Tradeoff` when visibility-intervention data is present
- `## Ethical Risk Review`
- `## Recommended Human Review Questions`
- `## Limitations`

The report must remain aggregate-level and human-review-oriented. It must not expose raw JSON dumps, raw prompts, raw user content, API keys, `.env` values, account-level influenceability scores, named-user target lists, or recommendations to automatically execute a real-world strategy.

## 11. API Rules

1. Every endpoint should return JSON.
2. Use Pydantic schemas for all request and response bodies.
3. Avoid inconsistent field names.
4. Use snake_case in backend JSON fields.
5. Keep frontend transformations isolated in `frontend/src/api`.
6. Use mock data when real data is unavailable.
7. Do not break existing frontend components without updating this contract.
