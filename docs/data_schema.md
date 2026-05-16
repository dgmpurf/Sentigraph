# Sentigraph Data Schema

This document defines the core data structures for Sentigraph.

All schemas should be implemented as Pydantic models in:

```text
backend/app/schemas/
```

MongoDB document keys must always be strings.

## 0. Platform Source Registry

```json
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
}
```

Allowed platform categories:

```text
official_api_planned
future_real_adapter_candidate
crawler_later
disabled_or_optional_future
```

Only `selectable_for_mock=true` platforms should appear in active MVP frontend selectors. These selections are mock-only and must not trigger real crawlers or real platform APIs. `mock_available`, `real_mode_available`, `api_approval_required`, `api_approval_status`, `credentials_required`, `credentials_present`, `api_pending`, `real_mode_disabled`, and `selectable_for_real` are safe status fields for frontend/backend diagnostics. `credentials_present` must contain only booleans and must never expose credential values. Reddit currently has `mock_available=true`, `api_approval_status="api_pending"`, `api_pending=true`, `real_mode_available=false`, `selectable_for_real=false`, and `real_mode_disabled=true`. Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, and Zhihu currently have `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `api_approval_status="planned"`, `api_pending=true`, `real_mode_available=false`, `selectable_for_real=false`, and `real_mode_disabled=true`.

### PlatformStatusResponse

```json
{
  "platforms": [],
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

## 0.1 Public Parser Status and Preview

Public parser status and preview schemas are used for safe developer diagnostics around fixture-only public-page parser scaffolds. They are not production crawlers and must remain mock/fixture-first unless a separate live-fetch pilot is explicitly enabled.

### PublicParserStatusItem

```json
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
```

### PublicParserStatusResponse

```json
{
  "parsers": [],
  "total": 6,
  "live_fetch_enabled_default": false
}
```

### PublicParserPreviewRequest

```json
{
  "platform": "hupu",
  "limit": 3,
  "use_live_fetch": false
}
```

### PublicParserPreviewResponse

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

Rules:

- `sample_posts` uses the existing `RawPost` schema.
- `sample_comments` uses the existing `RawComment` schema.
- `limit` is clamped by the backend safe preview limit, currently `3`.
- `warnings` may include `live_fetch_disabled`, `comments_unavailable_without_login_or_dynamic_loading`, or `no_sample_posts`.
- Preview responses must not include credentials, browser cookies, private data, hidden authenticated content, or raw secrets.

## 0.5 Analysis Case

Analysis cases are lightweight MVP objects used to preserve one mock analysis context across pages. Current default storage is a project-local JSON file through the case repository/storage abstraction. MongoDB persistence is available as an optional v1.0 backend, while Redis remains future work.

Persistence defaults:

- `CASE_STORE_BACKEND=local_json`
- `CASE_STORE_PATH=backend/data/cases.json`
- Runtime JSON data is ignored by git with `backend/data/*.json` and `backend/data/*.json.tmp`.
- `backend/data/.gitkeep` keeps the runtime data directory in the repository.

Optional MongoDB persistence:

- `CASE_STORE_BACKEND=mongodb`
- `MONGODB_URI=mongodb://localhost:27017`
- `MONGODB_DATABASE=sentigraph`
- MongoDB mode is opt-in only and is not required for the default test suite.
- If MongoDB mode is selected but the connection cannot be opened, case-store creation raises a clear configuration error instead of silently losing data.
- Store selection loads the repository-root `.env` before reading `CASE_STORE_BACKEND`, while existing process environment variables still take precedence.
- Stored documents must be generated from Pydantic JSON-mode dumps so datetime fields remain consistent with local JSON behavior.
- Nested dictionary keys must be converted to MongoDB-safe strings; dotted keys are normalized and leading `$` keys are prefixed.

MongoDB collections used by the optional store:

```text
analysis_cases
markdown_reports
analysis_snapshots
alert_events
notification_outbox
```

Recommended indexes:

```text
analysis_cases.case_id unique
analysis_cases.created_at
analysis_cases.updated_at
markdown_reports.case_id unique
analysis_snapshots.snapshot_id unique
analysis_snapshots.case_id
analysis_snapshots.created_at
alert_events.alert_id unique
alert_events.case_id
alert_events.created_at
notification_outbox.notification_id unique
notification_outbox.case_id
notification_outbox.created_at
notification_outbox.status
```

### AnalysisCaseCreateRequest

```json
{
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "report_language": "zh-CN"
}
```

### AnalysisCaseListItem

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
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
```

Allowed case statuses:

```text
draft
running
completed
failed
```

### AnalysisCaseDetail

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "status": "completed",
  "monitoring_config": {
    "enabled": false,
    "interval_minutes": 60,
    "last_run_at": null,
    "next_run_at": null,
    "threshold_config": {},
    "status": "disabled"
  },
  "analysis_result": {},
  "visualization_data": {},
  "report": {},
  "markdown_available": true
}
```

Rules:

- `analysis_result` uses the existing `AnalysisResultResponse` schema.
- `visualization_data` uses the existing `VisualizationResponse` schema.
- `report` uses the normalized `PublicOpinionReport` schema.
- The MVP case store is deterministic and does not require a database.
- Case data survives backend restart when using the default local JSON store.
- Tests must use temporary case-store paths instead of `backend/data/cases.json`.
- Case creation and case run must remain mock-first and must not call real platform APIs or crawlers.

### MarkdownExportResponse

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "filename": "Tesla_舆情案例_case_001.md",
  "markdown": "# Tesla 舆情案例\n\n## 舆情总览\n...",
  "generated_at": "2026-05-14T09:03:00Z"
}
```

## 0.6 Monitoring and Alert Foundation

The v0.7 monitoring foundation stores local snapshots and alert events with the same case repository/storage layer. It is deterministic, mock-first, and does not require a scheduler, Redis, MongoDB, real crawlers, real platform APIs, or notification services.

### AnalysisSnapshot

```json
{
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
}
```

Rules:

- `snapshot_id` and `case_id` are strings.
- `risk_score`, `overall_risk`, `real_crisis_risk`, and `manipulation_risk` are clamped to `0-100`.
- `top_risk_topics` uses the existing V1.5 `TopicRiskScore` item shape.
- Repeated mock monitoring checks may apply deterministic snapshot-index shifts to support local demo trends.

### AlertLevel

```text
info
warning
critical
```

### AlertEvent

```json
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
```

### AlertThresholdConfig

```json
{
  "risk_score_delta_warning": 10,
  "risk_score_delta_critical": 20,
  "real_crisis_delta_warning": 10,
  "manipulation_delta_warning": 15,
  "topic_risk_high": 70,
  "topic_risk_critical": 85
}
```

### MonitoringStatus

```json
{
  "case_id": "case_001",
  "status": "alerts_detected",
  "latest_snapshot": {},
  "previous_snapshot": {},
  "alerts": [],
  "snapshot_count": 2,
  "latest_risk_delta": 12.0,
  "latest_risk_level": "medium",
  "message": "本轮监控触发 1 条预警事件。"
}
```

Allowed monitoring statuses:

```text
baseline_created
alerts_detected
stable
```

Alert evaluator rules:

- Create an `info` baseline event when no previous snapshot exists.
- Trigger risk-score alerts when `risk_score_delta >= 10`; use `critical` when the delta is at least `20`.
- Trigger risk-level escalation alerts when the latest raw `risk_level` moves upward.
- Trigger real-crisis alerts when `real_crisis_risk` increases by at least `10`.
- Trigger manipulation-risk alerts when `manipulation_risk` increases by at least `15`.
- Trigger topic alerts when a new topic appears with `topic_risk_score >= 70`; use `critical` when the score is at least `85`.

## 0.7 Monitoring Scheduler Foundation

The v0.8 scheduler foundation stores monitoring configuration and job state on each case. It remains manual and deterministic: no APScheduler, Celery, RQ, Redis, MongoDB, or long-running background worker starts by default.

### MonitoringScheduleConfig

```json
{
  "enabled": true,
  "interval_minutes": 60,
  "last_run_at": "2026-05-14T09:06:00Z",
  "next_run_at": "2026-05-14T10:06:00Z",
  "threshold_config": {
    "risk_score_delta_warning": 10,
    "risk_score_delta_critical": 20,
    "real_crisis_delta_warning": 10,
    "manipulation_delta_warning": 15,
    "topic_risk_high": 70,
    "topic_risk_critical": 85
  },
  "status": "scheduled"
}
```

Allowed scheduler config statuses:

```text
disabled
scheduled
due
```

Rules:

- `interval_minutes` defaults to `60`.
- The MVP accepts intervals from `5` to `1440` minutes.
- `threshold_config` uses the existing `AlertThresholdConfig` schema.
- Enabling monitoring sets the case to due immediately for deterministic local demos.
- Disabling monitoring clears `next_run_at`.

### MonitoringJobState

```json
{
  "case_id": "case_001",
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "enabled": true,
  "interval_minutes": 60,
  "last_run_at": "2026-05-14T09:06:00Z",
  "next_run_at": "2026-05-14T10:06:00Z",
  "status": "scheduled",
  "is_due": false,
  "snapshot_count": 2,
  "alert_count": 2
}
```

### SchedulerStatus

```json
{
  "background_scheduler_running": false,
  "total_cases": 1,
  "enabled_cases": 1,
  "due_cases": 0,
  "next_due_at": "2026-05-14T10:06:00Z",
  "job_states": [],
  "message": "Manual scheduler foundation is configured; no background worker is running."
}
```

### SchedulerRunDueResponse

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

Rules:

- `POST /api/v1/scheduler/run-due` runs only enabled cases whose `next_run_at` is due.
- It calls the existing mock monitoring logic and persists snapshots/alerts through the case store.
- It updates `last_run_at` to the latest snapshot time and `next_run_at` by adding `interval_minutes`.
- It must not start a background process, call real crawlers, or call real platform APIs.

## 1. Keyword Expansion

### KeywordExpandRequest

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo"],
  "language": "auto"
}
```

### KeywordExpandResponse

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

## 1.5 Crawl Start Response

`POST /api/v1/crawl/start` remains backward compatible with the original mock response and may include adapter output metadata when Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, or Zhihu is selected.

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

Rules:

- `platform_metadata` records safe adapter status only; it must not include credentials, tokens, or request secrets.
- `adapter_mode` is `mock` or `real`.
- `fallback_reason_category` and `sanitized_error_category` may be `api_pending`, `dependency_error`, `auth_error`, `network_error`, `parsing_error`, `config_error`, `adapter_error`, or `null`.
- `exception_class` is a safe exception class name only and must not include exception messages, request payloads, tokens, or credentials.
- `real_mode_reached` indicates whether the real adapter path was reached.
- `dependency_available` indicates whether required real-mode dependencies such as PRAW are importable.
- `mock_available`, `api_pending`, and `real_mode_disabled` communicate safe adapter/source status without exposing credentials. Reddit real API mode stays disabled while approval is pending. Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, and Zhihu real official API modes stay disabled while credentials, approval, permission scopes, and implementation are pending.
- `real_mode_available`, `api_approval_required`, `api_approval_status`, `selectable_for_real`, and `real_mode_blocked_reason` describe why a real source path is or is not usable. Current valid blocked reasons include `api_pending`, `disabled`, `mock_only`, `credentials_missing`, and `approval_required`.
- `raw_posts` uses the `RawPost` schema.
- `raw_comments` uses the `RawComment` schema.
- Official API planned platforms remain mock-only. Crawler-later platforms remain disabled for real crawling.
- Weibo uses `source_type="official_api_adapter_scaffold"` and may return Weibo-style mock microblog/comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Bilibili uses `source_type="official_api_adapter_scaffold"` and may return Bilibili-style mock video/comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Douyin uses `source_type="official_api_adapter_scaffold"` and may return Douyin-style mock short-video/comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Kuaishou uses `source_type="official_api_adapter_scaffold"` and may return Kuaishou-style mock short-video/livestream comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Xiaohongshu uses `source_type="official_api_adapter_scaffold"` and may return Xiaohongshu-style mock lifestyle/community note `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`.
- Zhihu uses `source_type="official_api_adapter_scaffold"` and may return Zhihu-style mock Q&A/article `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`.

### Public Parser Metadata Extension

`POST /api/v1/crawl/start` may include public-parser metadata when a scaffolded public-page parser such as `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, or `nga` is explicitly requested.

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
  "post_count": 3,
  "comment_count": 0,
  "schema_valid": true,
  "raw_post_schema_valid": true,
  "raw_comment_schema_valid": true
}
```

Rules:

- `source_type="public_page_parser"` identifies the compliant public-page parser framework.
- `parser_status` may be `fixture_only`, `disabled`, `scaffolded`, or a future reviewed status such as `live_public_enabled`.
- `live_fetch_enabled` defaults to false and must remain false unless explicitly enabled for local testing.
- `live_fetch_attempted` means the parser reached the live fetch path. It stays false for the default fixture/mock fallback.
- `live_fetch_allowed` means the robots/profile policy check allowed the fetch attempt. It stays false when policy is unclear, blocked, disallowed, or live fetch is disabled.
- `fetch_status` is safe status metadata such as `disabled`, `ok`, `robots_disallowed`, `robots_unavailable_or_unclear`, `path_not_allowed_by_profile`, `network_error`, `http_error`, or `selector_missing`.
- Public parser fallback categories may include `fixture_only`, `live_fetch_disabled`, `selector_missing`, `robots_disallowed`, `robots_unavailable_or_unclear`, `path_not_allowed_by_profile`, `http_error`, or `network_error`.
- Public parser outputs must validate against `RawPost` / `RawComment`.
- The Paper has an optional local live public-page fetch pilot when `PUBLIC_PARSER_LIVE_FETCH_ENABLED=true`; fixture/mock fallback remains the default.
- Jiemian fixture output currently normalizes title, content, source/author label, created time, and permalink into `RawPost`. Comments remain unavailable because the fixture does not expose public comments without login or dynamic loading: `comments_unavailable_without_login_or_dynamic_loading`.
- Maimai fixture output currently normalizes post title, main post content, source/author label, created time, permalink, interaction count, reply count, and visible fixture replies into the common `RawPost` / `RawComment` schemas.
- Hupu fixture output normalizes a public fixture thread into `RawPost` and visible fixture replies into `RawComment`, including author, content, created time, parent id when present, and light/upvote count when present.
- Tieba fixture output normalizes a public fixture thread into `RawPost` and visible fixture replies into `RawComment`, including author, content, created time, parent id when present, like count when present, and forum floor number in `RawComment.raw_data.floor_number`.
- NGA fixture output normalizes a public fixture thread into `RawPost` and visible fixture replies into `RawComment`, including author, content, created time, parent id when present, like count when present, and forum floor number in `RawComment.raw_data.floor_number`.
- Parser code must not use login, cookies, captcha bypass, anti-bot evasion, proxy rotation, private messages, hidden data, or authentication-gated pages.

## 2. Raw Post

```json
{
  "platform": "weibo",
  "post_id": "post_001",
  "author_id": "user_hash_001",
  "author_name": "anonymous_user",
  "title": "Is this product quality getting worse?",
  "content": "I have seen many complaints about this product recently.",
  "like_count": 120,
  "reply_count": 35,
  "share_count": 3,
  "created_at": "2026-05-13T10:00:00Z",
  "url": "https://example.com/post/post_001",
  "raw_data": {}
}
```

## 3. Raw Comment

```json
{
  "platform": "weibo",
  "post_id": "post_001",
  "comment_id": "comment_001",
  "parent_id": null,
  "author_id": "user_hash_002",
  "author_name": "anonymous_user",
  "content": "I think this product has serious quality issues.",
  "like_count": 45,
  "reply_count": 8,
  "share_count": 0,
  "created_at": "2026-05-13T10:05:00Z",
  "url": "https://example.com/post/post_001/comment/comment_001",
  "raw_data": {}
}
```

## 4. Clean Comment

```json
{
  "clean_comment_id": "clean_001",
  "original_comment_ids": ["comment_001", "comment_008", "comment_021"],
  "platforms": ["weibo"],
  "post_ids": ["post_001"],
  "author_id": "user_hash_002",
  "clean_text": "this product has serious quality issues",
  "language": "en",
  "duplicate_group_id": "dup_group_001",
  "duplicate_count": 12,
  "semantic_similarity_group": "sem_group_008",
  "is_repeated_script": true,
  "created_at_min": "2026-05-13T10:05:00Z",
  "created_at_max": "2026-05-13T12:08:00Z"
}
```

## 5. User Aggregation Result

```json
{
  "author_id": "user_hash_002",
  "platforms": ["weibo"],
  "comment_count": 18,
  "unique_comment_count": 5,
  "duplicate_comment_ratio": 0.72,
  "average_sentiment_score": -0.64,
  "first_seen_at": "2026-05-13T10:05:00Z",
  "last_seen_at": "2026-05-13T12:08:00Z"
}
```

## 6. Sentiment Result

```json
{
  "comment_id": "clean_001",
  "sentiment": "negative",
  "sentiment_score": -0.82,
  "emotion_tags": ["anger", "distrust"],
  "stance": "opposing",
  "confidence": 0.91,
  "reason": "The comment expresses strong dissatisfaction and distrust."
}
```

Allowed sentiment values:

```text
positive
negative
neutral
mixed
```

Recommended emotion tags:

```text
anger
fear
sadness
trust
mocking
questioning
supportive
opposing
disappointment
uncertainty
```

## 7. Topic Cluster

```json
{
  "cluster_id": "topic_001",
  "topic": "Product quality issues",
  "summary": "Many users complain about durability and defects.",
  "comment_count": 356,
  "average_sentiment_score": -0.74,
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ]
}
```

## 8. Conflict Result

```json
{
  "conflict_id": "conflict_001",
  "side_a": "The product has real quality issues.",
  "side_b": "The negative trend is caused by malicious competitors.",
  "intensity": 0.83,
  "evidence_comments": [
    "This product has real quality problems.",
    "This looks like a coordinated attack."
  ]
}
```

## 9. AI-Generated Content Detection

```json
{
  "comment_id": "clean_001",
  "ai_generated_probability": 0.76,
  "template_similarity_score": 0.88,
  "reason": "Multiple comments share highly similar sentence structures."
}
```

## 10. Bot Score

```json
{
  "author_id": "user_hash_002",
  "bot_probability": 0.81,
  "bot_reasons": [
    "High repeated content ratio",
    "Abnormally frequent comments",
    "Highly synchronized posting time"
  ],
  "influence_weight": 0.43
}
```

## 11. Propagation Graph

### Node

```json
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
```

### Edge

```json
{
  "source": "post_001",
  "target": "comment_002",
  "relation": "reply",
  "weight": 0.64
}
```

### Full Graph

```json
{
  "nodes": [],
  "edges": [],
  "metrics": {
    "depth": 4,
    "breadth": 128,
    "central_node_id": "post_001",
    "propagation_speed": 0.84
  }
}
```

## 12. Risk Score

```json
{
  "risk_score": 87,
  "risk_level": "high",
  "risk_factors": {
    "negative_sentiment_ratio": 0.72,
    "negative_sentiment_strength": 0.81,
    "bot_impact_score": 0.61,
    "propagation_speed": 0.84,
    "controversy_score": 0.78,
    "trend_shift": 0.67
  },
  "explanation": "Negative sentiment is rapidly increasing with strong repeated-script signals."
}
```

Risk levels:

```text
low
medium
high
critical
```

Risk model metadata and V1.5 topic risk fields:

`risk_model_version` is active in current MVP visualization/report responses and should remain backward-compatible. V1.5 adds deterministic topic-level risk fields using current mock pipeline outputs. V2 topic-window fields remain future work.

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

Rules:

- `risk_model_version` identifies the scoring model used for the result. V1 remains `v1_static_mvp`; V1.5 topic-level output uses `v1_5_topic_risk_mvp`.
- `topic_risks` is the V1.5 per-topic risk output.
- `real_crisis_risk` and `manipulation_risk` are V1.5 aggregate scores from 0 to 100.
- `risk_explanation` should be deterministic and schema-compatible.
- MongoDB document keys must remain strings.

## 12.1 Analysis Result V1.5 Extension

`AnalysisResultResponse` keeps the original `risk` object for backward compatibility and may additionally include V1.5 topic-level risk fields when topic clusters exist:

```json
{
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

Rules:

- These fields are additive and must not remove or rename the legacy `risk.risk_score` and `risk.risk_level` fields.
- `topic_risks` and `top_risk_topics` use the `TopicRiskScore` shape defined above.
- Missing optional inputs should produce deterministic safe fallback values instead of crashing.

## 13. Visualization Response

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

## 14. Public Opinion Report

Normalized report output is returned by `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate`.

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
    "负面议题：Product quality issues：356条评论，平均情绪-0.74"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true
}
```

Rules:

- `report_language` defaults to `zh-CN`; `en-US` is optional.
- `risk_level` stays as the raw English enum: `low`, `medium`, `high`, or `critical`.
- `risk_level_label` is a display-only label. For `zh-CN`, use `低风险`, `中等风险`, `高风险`, or `严重风险`.
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5 responses may set `risk_model_version` to `v1_5_topic_risk_mvp` and include `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.
- Chinese report templates should translate risk wording for display inside text, but not change the raw `risk_level` value.
- Representative comments preserve original text and are not translated by the report builder.
- Report generation is deterministic and template-based; it does not call external LLM APIs.

## 15. Notification Outbox Schemas

The v0.9 notification foundation stores local notification outbox items in the same mock-first persistence layer as cases, snapshots, and alerts. Notifications are generated from alert events and are never sent to real external services in the MVP.

### NotificationChannelType

Allowed values:

- `in_app`
- `email_placeholder`
- `webhook_placeholder`
- `slack_placeholder`
- `enterprise_wechat_placeholder`
- `feishu_placeholder`

Only `in_app` is active. Placeholder channel types are schema-compatible future slots and must not call real APIs yet.

### NotificationStatus

Allowed values:

- `pending`
- `simulated_sent`
- `failed`

Read/unread state is represented separately with `read_at`.

### NotificationOutboxItem

```json
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
    "alert_message": "risk increased",
    "reason": "risk delta exceeded threshold",
    "snapshot_id": "case_001_snapshot_002"
  }
}
```

Rules:

- `notification_id` is deterministic for the alert/channel pair to prevent duplicate notifications.
- `message` uses deterministic Chinese templates.
- `simulate_send` only updates local fields and never calls email, Slack, webhook, Enterprise WeChat, Feishu, SMS, or push services.
- Notification runtime data is persisted in the local JSON case store by default and is ignored by git.

### NotificationSendResult

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

### NotificationOutboxStatus

```json
{
  "total": 2,
  "unread": 2,
  "pending": 1,
  "simulated_sent": 1,
  "failed": 0,
  "mock_only": true,
  "channels": [],
  "message": "通知出箱仅用于本地模拟，不会发送真实外部消息。"
}
```

## 16. Recommendation Response

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
    "负面情绪占比较高，当前为72%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks."
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
