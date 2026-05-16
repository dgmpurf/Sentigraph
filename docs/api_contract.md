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
    "toutiao"
  ]
}
```

Important:

- `selectable_for_mock=true` means the frontend may show the platform in mock-first selectors.
- `mock_available=true` means the platform has safe local mock data behavior.
- `real_mode_available=true` means the backend may use a real source path for that platform. In the current MVP this is false for all platforms.
- `credentials_present` is a safe boolean map only. It must never contain credential values.
- `api_pending=true` means any future real API path is still waiting for approval, credentials, permissions, or compliance review.
- `real_mode_disabled=true` means the backend must not call the real platform API for that source.
- Official API planned platforms may be selectable for mock analysis, but they must not trigger real API calls until credentials, permissions, and compliance checks are available.
- Reddit is visible and mock-selectable as a future real adapter candidate, but its current real API status is `api_pending`.
- Weibo and Bilibili are mock-selectable through official API adapter scaffolds. Their real API modes are disabled and not called until credentials, approval, and implementation are added.
- Crawler-later platforms are not selectable for real crawling in the MVP.
- YouTube is `disabled_or_optional_future` and is not an active MVP platform.

### Platform Readiness Status

```http
GET /api/v1/platforms/status
```

Response:

```json
{
  "platforms": [
    {
      "platform_id": "reddit",
      "display_name": "Reddit",
      "category": "future_real_adapter_candidate",
      "source_type": "mock_data_future_adapter_placeholder",
      "status": "api_pending",
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
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "selectable_for_real": false,
      "api_pending": true,
      "real_mode_disabled": true,
      "official_platform_url": null,
      "notes": "Selectable for offline mock analysis. Reddit API approval is pending, so real API mode is disabled and public-page scraping is not used as a bypass."
    }
  ],
  "active_mvp_platforms": ["reddit", "weibo", "bilibili", "douyin", "kuaishou", "xiaohongshu", "zhihu", "douban", "toutiao"],
  "mock_selectable_platforms": ["reddit", "weibo", "bilibili", "douyin", "kuaishou", "xiaohongshu", "zhihu", "douban", "toutiao"],
  "real_selectable_platforms": [],
  "summary": {
    "total_platforms": 17,
    "mock_selectable_count": 9,
    "real_selectable_count": 0,
    "api_pending_count": 9,
    "disabled_count": 8,
    "crawler_later_count": 7
  }
}
```

Important:

- This endpoint is safe for UI diagnostics.
- It returns credential presence as booleans only.
- Reddit remains `api_pending`; real API mode is disabled until approval is granted.
- Crawler-later platforms are visible for roadmap planning but never real-selectable in the MVP.
- YouTube remains disabled or optional future.

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
- `fallback_reason_category` and `sanitized_error_category` are intentionally coarse and safe: `api_pending`, `dependency_error`, `auth_error`, `network_error`, `parsing_error`, `config_error`, or `adapter_error`. They must never include credentials, tokens, or secret values.
- Public parser fallback categories may also include `fixture_only`, `live_fetch_disabled`, `selector_missing`, `robots_disallowed`, `robots_unavailable_or_unclear`, `path_not_allowed_by_profile`, or `http_error`.
- `exception_class` is a safe class name only, for example `ResponseException` or `JSONDecodeError`; it must not include exception messages or secret-bearing request data.
- `real_mode_reached` indicates whether the adapter reached the real API code path.
- `dependency_available` indicates whether required adapter dependencies such as PRAW are available.
- `real_mode_blocked_reason` may be `api_pending`, `disabled`, `mock_only`, `credentials_missing`, `approval_required`, or `null`.
- Official API planned platforms still use the existing mock behavior. Crawler-later platforms are not activated for real crawling.

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
  "markdown_available": false
}
```

### Get Case Detail

```http
GET /api/v1/cases/{case_id}
```

Response contains the same metadata as Create Case. After a run, `analysis_result`, `visualization_data`, `report`, and `markdown_available` are populated.

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
    "topic_risks": []
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

- `POST /api/v1/cases/{case_id}/run` uses the same deterministic offline mock pipeline as the existing analysis, visualization, summary, and recommendation APIs.
- Running a case must not trigger real crawlers or real platform APIs.
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

## 11. API Rules

1. Every endpoint should return JSON.
2. Use Pydantic schemas for all request and response bodies.
3. Avoid inconsistent field names.
4. Use snake_case in backend JSON fields.
5. Keep frontend transformations isolated in `frontend/src/api`.
6. Use mock data when real data is unavailable.
7. Do not break existing frontend components without updating this contract.
