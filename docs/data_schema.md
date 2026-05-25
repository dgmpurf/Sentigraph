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
  "platform": "reddit",
  "platform_id": "reddit",
  "display_name": "Reddit",
  "category": "future_real_adapter_candidate",
  "source_type": "mock_data_future_adapter_placeholder",
  "integration_type": "official_api_pending",
  "status": "api_pending",
  "enabled_in_mvp": true,
  "selectable_for_mock": true,
  "mock_available": true,
  "real_mode_available": false,
  "real_mode_configured": false,
  "api_approval_required": true,
  "api_approval_status": "api_pending",
  "developer_access_status": null,
  "comment_api_status": null,
  "recommended_comment_scope": null,
  "video_comment_scope_status": null,
  "required_credentials": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"],
  "required_scopes": [],
  "scope_status": "approval_pending",
  "oauth_required": false,
  "oauth_status": "not_required",
  "real_mode_blocker": "approval_pending",
  "data_access_level": "mock_reddit_style_data",
  "next_user_action": "Wait for Reddit API approval; do not use public-page scraping as a bypass.",
  "quota_cache_protected": false,
  "credentials_required": ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"],
  "credentials_present": {
    "REDDIT_CLIENT_ID": false,
    "REDDIT_CLIENT_SECRET": false,
    "REDDIT_USER_AGENT": false
  },
  "credential_present": false,
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

Only `selectable_for_mock=true` platforms should appear in active MVP frontend selectors. These selections are mock-first and must not trigger real crawlers. `mock_available`, `real_mode_available`, `real_mode_configured`, `api_approval_required`, `api_approval_status`, `developer_access_status`, `app_type`, `comment_api_status`, `recommended_comment_scope`, `video_comment_scope_status`, `required_credentials`, `required_scopes`, `scope_status`, `oauth_required`, `oauth_status`, `real_mode_blocker`, `data_access_level`, `next_user_action`, `quota_cache_protected`, `credentials_required`, `credentials_present`, `credential_present`, `api_pending`, `real_mode_disabled`, and `selectable_for_real` are safe status fields for frontend/backend diagnostics. `credentials_present` and `credential_present` must contain only booleans and must never expose credential values. Reddit currently has `integration_type="official_api_pending"`, `scope_status="approval_pending"`, `real_mode_blocker="approval_pending"`, `mock_available=true`, `api_approval_status="api_pending"`, `api_pending=true`, `real_mode_available=false`, `selectable_for_real=false`, and `real_mode_disabled=true`. Weibo reports `real_mode_blocker="company_age_requirement_pending"`. Bilibili reports `real_mode_blocker="approval_pending"`. Douyin records `integration_type="official_api_oauth"`, `developer_access_status="obtained"`, `app_type="web_app"`, `required_scopes=["user_info","item.comment"]`, `scope_status="item_comment_not_verified"`, `oauth_required=true`, `oauth_status="oauth_pending"`, `comment_api_status="item_comment_scope_not_verified"`, `recommended_comment_scope="item.comment"`, `video_comment_scope_status="not_recommended_for_mvp"`, and `real_mode_blocker="oauth_and_scope_not_verified"` until Web App OAuth, `item.comment`, and item-id source are verified. Xiaohongshu records `developer_access_status="obtained"`, `scope_status="comment_api_unknown_or_not_confirmed"`, `comment_api_status="unknown_or_not_confirmed"`, and `real_mode_blocker="permission_not_verified"` until console permissions are verified. YouTube uses `integration_type="official_api"`, `source_type="youtube_data_api_v3"`, `data_access_level="public_video_comment_data"`, and `quota_cache_protected=true`; it remains mock by default and becomes `selectable_for_real=true` only when `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` are both configured locally.

### PlatformStatusResponse

Returned by both `GET /api/v1/platforms/status` and
`GET /api/v1/platforms/readiness`. The latter is the preferred endpoint for
the Real Data Source Readiness Framework.

```json
{
  "platforms": [],
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

## 0.1 Planned Douyin Web App OAuth Schemas

These schemas are design placeholders for a future official Douyin Web App integration. They are not implemented as live token storage and must not trigger real Douyin API calls in the current MVP. The recommended MVP route is `item.comment`; `video.comment` remains `not_recommended_for_mvp` unless Douyin console verification proves otherwise.

### DouyinAccount

```json
{
  "open_id": "string",
  "nickname": "string",
  "avatar_url": "string|null",
  "authorized_scopes": ["item.comment"],
  "authorized_at": "datetime",
  "token_status": "missing|valid|expired|refresh_required",
  "safe_metadata_only": true
}
```

### DouyinVideo

```json
{
  "item_id": "string",
  "title": "string",
  "description": "string",
  "author_open_id": "string|null",
  "like_count": 0,
  "comment_count": 0,
  "share_count": 0,
  "published_at": "datetime|null",
  "url": "string|null",
  "raw_data": {"safe_metadata_only": true}
}
```

### DouyinComment

```json
{
  "comment_id": "string",
  "item_id": "string",
  "parent_id": "string|null",
  "author_open_id": "string|null",
  "author_name": "string|null",
  "content": "string",
  "like_count": 0,
  "reply_count": 0,
  "created_at": "datetime|null",
  "raw_data": {"safe_metadata_only": true}
}
```

### DouyinFetchJob

```json
{
  "job_id": "string",
  "case_id": "string|null",
  "item_ids": ["string"],
  "requested_limit": 20,
  "effective_limit": 20,
  "status": "planned|blocked|running|completed|failed",
  "blocked_reason": "oauth_and_scope_not_verified",
  "safe_counts": {"video_count": 0, "comment_count": 0}
}
```

### DouyinOAuthState

```json
{
  "state_id": "string",
  "state_hash": "string",
  "redirect_uri": "string",
  "requested_scopes": ["item.comment"],
  "created_at": "datetime",
  "expires_at": "datetime",
  "consumed_at": "datetime|null"
}
```

## 0.2 Public Parser Status and Preview

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
  "markdown_available": true,
  "raw_posts": [],
  "raw_comments": [],
  "evidence_items": [],
  "crawl_metadata": [],
  "crawl_source_mode": null,
  "crawl_attached_at": null,
  "raw_data_status": "missing",
  "analysis_input_source": "mock_data_fallback",
  "raw_post_count": 0,
  "raw_comment_count": 0,
  "evidence_item_count": 0
}
```

Rules:

- `analysis_result` uses the existing `AnalysisResultResponse` schema.
- `visualization_data` uses the existing `VisualizationResponse` schema.
- `report` uses the normalized `PublicOpinionReport` schema.
- `raw_posts` and `raw_comments` use the shared `RawPost` / `RawComment` schemas returned by platform adapters and public-parser fixtures.
- `evidence_items` uses the shared `EvidenceItem` schema. Case-specific crawl output may be normalized into this field while preserving the original `raw_posts` and `raw_comments`.
- `crawl_metadata` uses `PlatformCrawlMetadata` and may include safe booleans such as `credential_present`; it must never include credential values.
- `raw_data_status` is `missing`, `attached`, or `empty`.
- `analysis_input_source` is `case_raw_data` when attached case raw comments are used, `case_evidence_items` when attached normalized evidence items are used without raw comments, and `mock_data_fallback` otherwise.
- The MVP case store is deterministic and does not require a database.
- Case data survives backend restart when using the default local JSON store.
- Tests must use temporary case-store paths instead of `backend/data/cases.json`.
- Case creation and case run must not call real platform APIs or crawlers automatically. Case-specific raw-data ingestion is explicit through `POST /api/v1/cases/{case_id}/crawl/start`.

### Universal Evidence Ingestion Schemas

`EvidenceItem`:

```json
{
  "evidence_id": "evidence_youtube_comment_yt_comment_001",
  "case_id": "case_001",
  "platform": "youtube",
  "source_type": "youtube",
  "acquisition_mode": "official_api_public",
  "evidence_type": "comment",
  "title": null,
  "body_text": null,
  "comment_text": "Public comment text.",
  "parent_id": null,
  "root_id": "yt_video_001",
  "author_id": "public_author_id",
  "author_name": "Public author label",
  "url": "https://www.youtube.com/watch?v=yt_video_001&lc=yt_comment_001",
  "created_at": "2026-05-21T12:05:00Z",
  "like_count": 4,
  "reply_count": 0,
  "share_count": 0,
  "view_count": 0,
  "raw_data_safe": {
    "source_type": "youtube_data_api_v3"
  },
  "language": "en-US",
  "confidence": 1.0,
  "content_visibility": "public",
  "access_scope": "public",
  "ingestion_metadata": {},
  "provenance_type": "official_api",
  "verification_status": "verified_by_official_api",
  "trust_score": 0.92,
  "trust_label": "high",
  "source_url_present": true,
  "source_url": "https://www.youtube.com/watch?v=yt_video_001&lc=yt_comment_001",
  "source_platform_claim": "youtube",
  "source_capture_method": "official_api",
  "submitted_by_label": null,
  "submitter_hash": null,
  "submitted_at": null,
  "user_attestation_required": false,
  "user_attestation_text": null,
  "verification_notes": ["Official API metadata is treated as high-trust source evidence, not a truth guarantee."],
  "duplicate_group_id": "dup_abc123",
  "content_hash": "sha256...",
  "normalized_content_hash": "sha256...",
  "canonical_url_hash": "sha256...",
  "duplicate_count": 1,
  "duplicate_group_size": 1,
  "risk_flags": [],
  "review_status": "not_reviewed",
  "review_reason_codes": [],
  "reviewed_at": null,
  "reviewer_label": null,
  "review_notes": null
}
```

Allowed `acquisition_mode` values:

```text
official_api_public
official_api_oauth
public_parser
search_discovery
user_upload
manual_url
data_vendor
mock_fixture
```

Allowed `source_type` values:

```text
youtube
douyin
bilibili
weibo
xiaohongshu
reddit
news_site
forum
public_web
uploaded_dataset
mock
```

Allowed `evidence_type` values:

```text
video
article
post
comment
reply
title
body_text
metadata
interaction_metric
interaction_metrics
search_result
uploaded_record
```

Allowed `provenance_type` values:

```text
official_api
public_parser
search_discovery_candidate
user_upload
manual_url
manual_text
screenshot_transcription
data_vendor
mock_fixture
```

Allowed `verification_status` values:

```text
verified_by_official_api
verified_by_public_parser
source_url_provided_unverified
user_attested_unverified
screenshot_unverified
vendor_attested
mock_fixture
rejected
needs_review
```

Allowed `trust_label` values:

```text
high
medium
low
unverified
rejected
```

Allowed `review_status` values:

```text
not_reviewed
review_needed
approved
rejected
marked_weak
needs_more_source
duplicate_merged
```

Allowed human review decisions:

```text
approve
reject
mark_weak
request_more_source
merge_duplicate
reset_review
```

`EvidenceIngestionBatch` contains an optional `EvidenceSource` plus `evidence_items`. `EvidenceIngestionResult` returns normalized evidence items, `source_distribution`, `evidence_type_counts`, `top_titles`, `representative_comments`, `trust_summary`, `deduplication_summary`, warnings, and safe-mode flags.

Manual URL evidence uses `acquisition_mode="manual_url"` and usually `source_type="public_web"`. It is for user-entered public evidence only: URLs are stored as plain text review context and are never fetched, followed, scraped, or parsed automatically. Every manual URL evidence item must include at least one of `title`, `body_text`, or `comment_text`. Invalid numeric metric inputs are coerced to `0` with `invalid_numeric_metric:<field>` warnings. Secret-like pasted values in text fields are redacted and surfaced with `secret_like_text_redacted:<field>` warnings. The backend must never persist cookies, tokens, API keys, `.env` values, or raw credential data in manual evidence.

Trust and dedup summaries:

```json
{
  "trust_summary": {
    "trust_label_distribution": {"high": 1, "medium": 1, "unverified": 1},
    "verification_status_distribution": {"verified_by_official_api": 1, "needs_review": 1},
    "provenance_type_distribution": {"official_api": 1, "manual_url": 1},
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
  }
}
```

Analysis uses unique evidence items by default. Duplicate submissions are preserved as `duplicate_count` / `duplicate_group_size` repetition signals but must not directly inflate sentiment, topic, or risk counts.

Human review summaries:

```json
{
  "review_summary": {
    "case_id": "case_001",
    "total_items": 5,
    "queue_count": 3,
    "review_needed_count": 2,
    "low_trust_count": 1,
    "duplicate_group_count": 1,
    "missing_source_count": 1,
    "screenshot_count": 1,
    "approved_count": 1,
    "rejected_count": 1,
    "marked_weak_count": 1,
    "needs_more_source_count": 0,
    "review_status_distribution": {"review_needed": 2, "rejected": 1},
    "review_reason_distribution": {"missing_source_url": 1},
    "safe_mode": {
      "real_api_calls": false,
      "real_llm_calls": false,
      "url_fetching": false,
      "ai_review": false
    }
  }
}
```

Review queue items include evidence previews, provenance/trust fields, duplicate metadata, source URL status, attestation status, `review_status`, and `review_reason_codes`. They are meant for human review only. Sentigraph does not call an LLM to verify evidence and does not claim screenshots or pasted transcriptions are authentic. Rejected evidence remains stored but is excluded from default `case_evidence_items` analysis and representative comments.

### CSV / Excel Evidence Import Schemas

`GET /api/v1/evidence/import/template.csv` returns a static UTF-8 CSV template attachment named `sentigraph_evidence_import_template.csv`. The template uses the mapping fields below and includes safe article, video, and comment sample rows. It contains no credentials and can be parsed by the same preview endpoint as a normal user-uploaded CSV.

`EvidenceImportColumnMapping` maps uploaded file columns to normalized evidence fields:

```json
{
  "platform": "platform",
  "source_type": "source_type",
  "acquisition_mode": "acquisition_mode",
  "evidence_type": "evidence_type",
  "title": "title",
  "body_text": "body_text",
  "comment_text": "comment_text",
  "parent_id": "parent_id",
  "root_id": "root_id",
  "author_id": "author_id",
  "author_name": "author_name",
  "url": "url",
  "created_at": "created_at",
  "like_count": "like_count",
  "reply_count": "reply_count",
  "share_count": "share_count",
  "view_count": "view_count",
  "language": "language",
  "provenance_type": "provenance_type",
  "verification_status": "verification_status",
  "source_capture_method": "source_capture_method",
  "user_attestation": "user_attestation"
}
```

`EvidenceImportPreviewRequest` and `EvidenceImportCommitRequest`:

```json
{
  "filename": "sample_evidence.csv",
  "content_base64": "base64-encoded file bytes",
  "content_text": null,
  "column_mapping": {},
  "preview_limit": 10,
  "max_rows": 500
}
```

`EvidenceImportRowPreview`:

```json
{
  "row_number": 2,
  "evidence_id": "evidence_import_hash",
  "platform": "uploaded_dataset",
  "source_type": "uploaded_dataset",
  "acquisition_mode": "user_upload",
  "evidence_type": "comment",
  "title": "Public discussion title",
  "comment_text": "Public comment text",
  "author_name": "Public author label",
  "url": "https://example.test/post",
  "created_at": "2026-05-25T09:00:00Z",
  "like_count": 12,
  "reply_count": 3,
  "share_count": 0,
  "view_count": 0,
  "warnings": []
}
```

`EvidenceImportPreviewResult` returns `detected_format`, `detected_columns`, `column_mapping`, row counts, `preview_rows`, warnings, and safe-mode flags. `EvidenceImportCommitResult` returns imported `EvidenceItem` records, `imported_count`, `total_evidence_item_count`, duplicate/skipped counts, source/type distributions, warnings, and safe-mode flags.

Rules:

- Imported evidence defaults to `source_type="uploaded_dataset"` and `acquisition_mode="user_upload"`.
- CSV import supports UTF-8, UTF-8-BOM, and GB18030/GBK fallback. XLSX import supports macro-free `.xlsx` only.
- Uploaded raw files are not persisted by default. Only normalized `EvidenceItem` records and safe import metadata are stored.
- Formula-like cells are treated as plain text and formulas are not executed.
- Secret-like fields and values are redacted or omitted before preview/commit output.
- Duplicate rows are skipped by deterministic content hash.

Rules:

- Evidence normalization does not fetch data and does not call real APIs or real LLM APIs.
- `interaction_metric` is the preferred standalone metric evidence type. `interaction_metrics` remains accepted as a backward-compatible alias for older local payloads.
- `search_result` and `uploaded_record` are planning-compatible evidence types for future discovery/vendor/upload flows.
- `raw_data_safe` must remove API keys, tokens, cookies, authorization headers, client secrets, passwords, credential values, and `.env` values.
- Evidence is case-level public/user-provided material. It must not create individual persuasion profiles, named-user targeting outputs, or account-level influenceability scores.

## 0.4 Source Catalog Schemas

The source catalog is static readiness/planning metadata exposed by
`GET /api/v1/sources/catalog`. It does not call real APIs, fetch URLs, use
cookies, inspect `.env`, or start crawlers.

`SourceCatalogEntry`:

```json
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
```

`SourceCatalogCategory`:

```json
{
  "category_id": "video_platforms",
  "display_name": "Video Platforms",
  "description": "Public video/post metadata and comments through official APIs, OAuth, user upload, or mock fixtures.",
  "sources": []
}
```

`SourceCatalogResponse`:

```json
{
  "categories": [],
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

## 0.5 Search Discovery Schemas

Search Discovery is a planned candidate-discovery layer. Current API support is static/mock only:

```http
GET /api/v1/search-discovery/status
GET /api/v1/search-discovery/mock-candidates?query=Tesla
```

It does not call real search APIs, call website APIs, fetch URLs, scrape pages, use cookies, inspect `.env`, expose secrets, integrate MediaCrawler, or call real LLM APIs.

`SearchDiscoveryQuery`:

```json
{
  "query": "Tesla",
  "providers": ["mock_fixture"],
  "max_candidates": 5,
  "language": "auto"
}
```

`SearchDiscoveryCandidate`:

```json
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
```

`SearchDiscoveryProviderStatus`:

```json
{
  "provider_id": "rss_feeds",
  "display_name": "RSS / Atom Feeds",
  "provider_class": "rss",
  "status": "pilot_candidate",
  "allowed_use": "Use public feed metadata when feed terms permit it.",
  "forbidden_use": "Do not fetch private feeds, paywalled content, or subscriber-only metadata.",
  "data_returned": ["url", "title", "summary_or_snippet", "source_name", "published_at"],
  "full_content_available": false,
  "requires_api_key": false,
  "credential_present": false,
  "user_review_required": true,
  "current_sentigraph_status": "planned_only",
  "next_action": "Add an RSS fixture pilot only after source-specific review."
}
```

`SearchDiscoveryBatch` returns a query, generated time, candidates, provider statuses, counts, and safe-mode flags. `SearchDiscoveryReviewDecision` is a planned review object with `candidate_id`, `decision`, `reviewer_note`, and `route_to`.

Candidate status values:

- `pending_review`
- `accepted`
- `rejected`
- `attached`

Review rule:

- Search Discovery candidates are not evidence by themselves.
- Accepted candidates must become `manual_url` evidence, user-upload/import evidence, or go through a separately reviewed public parser route.
- Search Discovery never performs automatic page fetching by itself.

### Case Raw Data Ingestion

`POST /api/v1/cases/{case_id}/crawl/start` stores adapter output on a case:

```json
{
  "raw_posts": [
    {
      "platform": "youtube",
      "post_id": "yt_video_id",
      "author_id": "channel_id",
      "author_name": "Channel title",
      "title": "Public video title",
      "content": "Public video description",
      "like_count": 42,
      "reply_count": 7,
      "share_count": 0,
      "created_at": "2026-05-17T12:00:00Z",
      "url": "https://www.youtube.com/watch?v=yt_video_id",
      "raw_data": {
        "source_type": "youtube_data_api_v3"
      }
    }
  ],
  "raw_comments": [
    {
      "platform": "youtube",
      "post_id": "yt_video_id",
      "comment_id": "yt_comment_id",
      "parent_id": null,
      "author_id": "channel_or_commenter_id",
      "author_name": "Public commenter name",
      "content": "Public comment text.",
      "like_count": 5,
      "reply_count": 1,
      "share_count": 0,
      "created_at": "2026-05-17T12:05:00Z",
      "url": "https://www.youtube.com/watch?v=yt_video_id&lc=yt_comment_id",
      "raw_data": {
        "source_type": "youtube_data_api_v3"
      }
    }
  ],
  "crawl_metadata": [],
  "crawl_source_mode": "case_crawl_start",
  "crawl_attached_at": "2026-05-18T10:00:00Z",
  "raw_data_status": "attached"
}
```

Rules:

- Do not store API keys, `.env` values, cookies, OAuth-only private fields, or platform credentials.
- `case_raw_data` analysis is still deterministic and uses existing local analysis services; it does not call real LLM APIs.
- If no attached raw comments exist, case analysis falls back to existing mock data.

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

## 0.6.5 Deterministic Forecasting Foundation

The v4.5 forecasting foundation derives near-future risk estimates from existing `AnalysisSnapshot` records. It is deterministic, offline-only, and does not call real platform APIs, real LLM APIs, crawlers, or live public fetch.

### ForecastInputSnapshot

Same core fields as `AnalysisSnapshot`, minus alert-only summary fields:

```json
{
  "snapshot_id": "case_001_snapshot_003",
  "case_id": "case_001",
  "created_at": "2026-05-17T12:03:00Z",
  "run_index": 3,
  "risk_score": 61.0,
  "overall_risk": 61.0,
  "risk_level": "medium",
  "risk_model_version": "v1_5_topic_risk_mvp",
  "real_crisis_risk": 38.0,
  "manipulation_risk": 24.0,
  "top_risk_topics": []
}
```

### TrendFeatures

```json
{
  "latest_risk": 61.0,
  "moving_average": 46.0,
  "slope": 14.5,
  "acceleration": 3.0,
  "volatility": 9.67,
  "snapshot_count": 3,
  "trend_direction": "rising"
}
```

Allowed `trend_direction` values:

```text
rising
falling
stable
unknown
```

### RiskForecast

```json
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
```

Allowed `horizon` values:

```text
next_check
1h
6h
24h
```

Allowed `forecast_confidence` values:

```text
insufficient_history
low
medium_low
medium
```

### TopicRiskForecast

```json
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
```

### ForecastResult

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
  "risk_forecasts": [],
  "topic_forecasts": [],
  "input_snapshots": [],
  "recommended_action": "风险预测呈上升趋势，建议提高监控频率并优先复核高风险话题。",
  "message": "Deterministic MVP 风险预测显示趋势上升，下一检查点预测风险为 77.0/100。"
}
```

Allowed `forecast_status` values:

```text
ready
insufficient_history
```

Score fields are clamped to `0-100`. With zero snapshots, `forecast_status` is `insufficient_history` and `recommended_action` asks the user to run monitoring checks first.

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

`POST /api/v1/crawl/start` remains backward compatible with the original mock response and may include adapter output metadata when Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, Toutiao, or YouTube is selected.

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

Rules:

- `platform_metadata` records safe adapter status only; it must not include credentials, tokens, or request secrets.
- `adapter_mode` is `mock` or `real`.
- `fallback_reason_category` and `sanitized_error_category` may be `api_pending`, `dependency_error`, `auth_error`, `quota_error`, `comments_unavailable`, `network_error`, `parsing_error`, `config_error`, `adapter_error`, or `null`.
- `exception_class` is a safe exception class name only and must not include exception messages, request payloads, tokens, or credentials.
- `real_mode_reached` indicates whether the real adapter path was reached.
- `dependency_available` indicates whether required real-mode dependencies such as PRAW are importable.
- `mock_available`, `api_pending`, `real_mode_disabled`, and `credential_present` communicate safe adapter/source status without exposing credentials. Reddit real API mode stays disabled while approval is pending. Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao real official API modes stay disabled while credentials, approval, permission scopes, and implementation are pending. Douyin may additionally report `developer_access_status`, `app_type`, `comment_api_status`, `real_mode_blocker`, `permission_status`, `oauth_status`, `token_exchange_status`, and `item_id_source_status`. YouTube real mode is available only when `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` is present locally.
- YouTube-specific crawl metadata may include safe quota/cache fields: `estimated_quota_units`, `search_call_count`, `videos_call_count`, `comment_threads_call_count`, `comments_call_count`, `cache_hit`, `cache_age_seconds`, and `quota_guardrail_status`. These fields are operational counters only and must not include API keys, `.env` values, request headers, or raw official API error bodies.
- `real_mode_available`, `api_approval_required`, `api_approval_status`, `selectable_for_real`, and `real_mode_blocked_reason` describe why a real source path is or is not usable. Current valid blocked reasons include `api_pending`, `permission_not_verified`, `oauth_and_scope_not_verified`, `disabled`, `mock_only`, `credentials_missing`, and `approval_required`.
- `raw_posts` uses the `RawPost` schema.
- `raw_comments` uses the `RawComment` schema.
- Official API planned platforms remain mock-only by default. YouTube is the only current credential-gated real-capable official API adapter. Crawler-later platforms remain disabled for real crawling.
- Weibo uses `source_type="official_api_adapter_scaffold"` and may return Weibo-style mock microblog/comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Bilibili uses `source_type="official_api_adapter_scaffold"` and may return Bilibili-style mock video/comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Douyin uses `source_type="official_api_adapter_scaffold"` and may return Douyin-style mock short-video/comment `RawPost` and `RawComment` items when selected in `/crawl/start`; Web App OAuth, `item.comment`, token exchange, and item-id source remain scaffolded but unverified, so no real Douyin call is made.
- Kuaishou uses `source_type="official_api_adapter_scaffold"` and may return Kuaishou-style mock short-video/livestream comment `RawPost` and `RawComment` items when selected in `/crawl/start`.
- Xiaohongshu uses `source_type="official_api_adapter_scaffold"` and may return Xiaohongshu-style mock lifestyle/community note `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`.
- Zhihu uses `source_type="official_api_adapter_scaffold"` and may return Zhihu-style mock Q&A/article `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`.
- Douban uses `source_type="official_api_adapter_scaffold"` and may return Douban-style mock review/group/topic `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`.
- YouTube uses `source_type="youtube_data_api_v3"` and may return YouTube-style video `RawPost` and visible-comment `RawComment` items when selected in `/crawl/start`; real mode uses the official YouTube Data API v3 only when explicitly configured. The adapter checks the ignored project-local cache `backend/data/youtube_cache.json` before real API calls, clamps requested limits to safe configured maxima, uses tiny `search.list`, `videos.list`, and `commentThreads.list` requests, disables deep reply expansion by default, and stops at the configured total-comment limit. Exhaustive reply expansion through `comments.list` with `parentId` remains future work behind strict limits.

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

### Selector Repair Schemas

Selector repair is a mock-first maintenance scaffold for public parser profiles. It uses sanitized public fixture HTML and deterministic `MockProvider` suggestions only. Active selector profiles are not modified automatically.

`SelectorRepairRequest`:

```json
{
  "platform_id": "hupu",
  "sanitized_html": "<article class=\"thread\"><h1 class=\"thread-title\">Fixture title</h1></article>",
  "current_profile": {
    "title_selector": ".old-title"
  },
  "extraction_targets": ["title", "content"],
  "parser_error_summary": "title selector did not match",
  "mode": "mock",
  "max_html_chars": 20000
}
```

`SelectorCandidate`:

```json
{
  "target": "title",
  "selector": "h1.thread-title",
  "selector_type": "css",
  "confidence": 0.9,
  "rationale": "Deterministic mock selector candidate for fixture-only repair review.",
  "source": "mock_provider"
}
```

`SelectorRepairSuggestion`:

```json
{
  "platform_id": "hupu",
  "status": "suggested",
  "candidates": [],
  "warnings": ["human_review_required", "active_profiles_not_modified"],
  "provider": "mock",
  "generated_by_mock": true,
  "applied": false,
  "review_required": true,
  "draft_id": null
}
```

`SelectorRepairPreviewResult`:

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
  "suggestion": null,
  "profile_modified": false
}
```

Allowed `SelectorRepairStatus` values are `suggested`, `draft`, `preview_ok`, `preview_failed`, `invalid_platform`, `provider_not_enabled`, `not_configured`, and `error`.

Rules:

- Sanitized HTML removes scripts, styles, inline event handlers, obvious token/cookie/authorization fields, and caps length through `SELECTOR_REPAIR_MAX_HTML_CHARS`.
- `SELECTOR_REPAIR_MODE=mock` and `SELECTOR_REPAIR_ENABLE_REAL_LLM=false` are the default safe settings.
- `future_real_llm` mode is disabled until a future explicit integration task.
- `profile_modified` must remain false for suggestion and preview flows.
- Credential values, cookies, and private data must never be included.

## 0.2 LLM Provider Readiness Diagnostics

The LLM provider diagnostics schema is internal/backend-safe status metadata. It is not an external LLM response and must never include API key values.

```json
{
  "provider_name": "mock",
  "real_calls_enabled": false,
  "api_key_present": false,
  "provider_status": "mock_ready",
  "required_credentials": [],
  "credential_presence": {}
}
```

Allowed `provider_status` values in the current scaffold:

```text
mock_ready
provider_not_enabled
not_configured
unknown_provider
```

Rules:

- `LLM_PROVIDER=mock` and `LLM_ENABLE_REAL_CALLS=false` remain the defaults.
- `api_key_present` and `credential_presence` are booleans only.
- Secret redaction helpers return `present` or `missing` only; no full or partial API key should appear in logs, tests, docs, or diagnostics.
- OpenAI, DeepSeek, and Qwen providers remain placeholders until a future real-provider integration task adds reviewed HTTP clients, timeout/rate-limit/cost controls, mocked HTTP tests, and strict output validation.

`LLMSafetyStatusResponse` is the public API shape used by `GET /api/v1/llm/status` and the frontend LLM Safety page:

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

Public LLM status responses intentionally omit credential variable names and values. They expose only provider ids, provider status, real-call enablement, and API key presence booleans.

## 0.3 LLM Usage Guardrail Schemas

LLM usage guardrails are offline metadata counters for future provider readiness. They do not store prompts, raw comments, raw HTML, model outputs, API keys, cookies, headers, or credentials.

Default config:

```json
{
  "tracking_enabled": true,
  "daily_call_limit": 100,
  "daily_token_limit": 100000,
  "max_input_chars": 20000,
  "fail_closed_on_limit": true,
  "mode": "mock"
}
```

`LLMGuardrailDecision`:

```json
{
  "allowed": true,
  "provider": "mock",
  "operation": "expand_keywords",
  "estimated_input_tokens": 5,
  "reason_category": null,
  "daily_calls_remaining": 99,
  "daily_tokens_remaining": 99995,
  "message": "LLM guardrail allowed call."
}
```

`LLMUsageRecord`:

```json
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
```

`LLMUsageSummary`:

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
  "recent_records": []
}
```

Rules:

- `estimate_tokens_from_chars()` uses deterministic character-based approximation for the scaffold.
- `record_mock_call()` records metadata only when `LLM_USAGE_TRACKING_ENABLED=true`.
- Future real providers should call `check_call_allowed()` before any external request.
- When `LLM_FAIL_CLOSED_ON_LIMIT=true`, over-limit real calls must be blocked before network access.
- Current OpenAI, DeepSeek, and Qwen providers remain disabled placeholders and make no external calls.

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
## 17. Offline Benchmark Summary, History, and Regression

`LatestBenchmarkSummaryResponse`, `BenchmarkHistoryResponse`, and `BenchmarkRegressionResponse` are used by the Benchmark Dashboard. They are safe summaries of generated offline benchmark results and must not include per-case payloads.

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

`BenchmarkHistoryEntry`:

```json
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
```

`BenchmarkRegressionResponse`:

```json
{
  "source": "offline_benchmark_regression",
  "available": true,
  "status": "regression_detected",
  "regression_detected": true,
  "changed_suites": [
    {
      "suite": "sentiment",
      "change_types": ["suite_pass_to_fail", "new_failures"],
      "previous_status": "pass",
      "latest_status": "fail",
      "previous_failed": 0,
      "latest_failed": 1,
      "previous_warnings": 0,
      "latest_warnings": 0
    }
  ],
  "previous_total_failed": 0,
  "latest_total_failed": 1,
  "previous_total_warnings": 0,
  "latest_total_warnings": 0,
  "previous_total_passed": 246,
  "latest_total_passed": 245,
  "reason_categories": ["total_failed_increased", "suite_pass_to_fail"],
  "message": "Regression risk detected in the latest offline benchmark run."
}
```

Allowed `status` values for the response:

```text
available
missing
malformed
no_history
no_regression
regression_detected
```

Rules:

- `source` is `offline_benchmark_summary`, `offline_benchmark_history`, `offline_benchmark`, or `offline_benchmark_regression` depending on the object.
- `suites` contains only suite name, suite status, `case_count`, pass/fail counts, and suite-level warnings.
- Benchmark `cases` arrays and raw fixture content are intentionally omitted from the API response.
- Regression detection records new failures, warning increases, suite `pass` to `fail`, and total-passed decreases.
- Missing or malformed summary/history files produce safe empty responses rather than uncaught errors.
- API responses and generated history summaries must not include local file paths, raw prompts, raw user content, API keys, `.env` values, or external request bodies.

## 18. Simulation Lab MVP Schemas

The Simulation Lab backend scaffold uses service-local Pydantic models under:

```text
backend/app/services/simulation/schemas.py
```

The schemas are synthetic, deterministic, and aggregate-only. They are not platform API payloads and must not include real personal data, API keys, cookies, tokens, `.env` values, raw prompts, or private content.

`SimulationAgent` includes:

- `agent_id`
- `community_id`
- `latent_opinion`
- `expressed_opinion`
- `prior_anchor`
- `stubbornness`
- `confidence_radius`
- `action_threshold`
- `confirmation_bias`
- `negativity_weight`
- `reactance`
- `authority_trust`
- `conformity`
- `attention_budget`
- `fatigue`
- `identity_group`
- `status`

`SimulationMessage` includes:

- `message_id`
- `topic`
- `source_type`
- `source_credibility`
- `stance_direction`
- `emotional_intensity`
- `evidence_strength`
- `framing`
- `novelty`
- `repetition`
- `platform_reach`

`SimulationIntervention` supports only transparent aggregate crisis-response types:

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

Allowed visibility interventions model lawful/platform-authorized content governance as aggregate scenario variables only. They are not execution commands and must not contain account lists, targeting instructions, or platform-governance evasion guidance.

`VisibilityIntervention` includes:

- `intervention_type`
- `target_message_reach`
- `current_visibility`
- `removal_time`
- `residual_copies`
- `screenshot_probability`
- `repost_migration_probability`
- `perceived_suppression`
- `policy_violation_clarity`
- `legitimacy_of_removal`
- `public_explanation_quality`
- `reactance_amplification`
- `martyr_effect`
- `cross_platform_spillover`
- `neutral_audience_negative_shift`
- `hard_opposition_negative_shift`
- `policy_basis`
- `authorization_source`
- `public_explanation_required`

`VisibilityInterventionResult` includes:

- `intervention_type`
- `exposure_reduction`
- `backlash_cost`
- `trust_loss`
- `spillover_risk`
- `net_risk_change`
- `removal_legitimacy_score`
- `public_explanation_quality_score`
- `neutral_audience_impact`
- `opposition_group_impact`
- `recommendation`
- `explanation`
- `audience_impact`
- `human_review_required`
- `aggregate_level_only`
- `warnings`

Forbidden intervention strings such as `fake_consensus`, `bot_amplification`, `fake_event`, `deceptive_distraction`, `covert_influencer_seeding`, `targeted_persuasion`, `suppression`, `illegal_suppression`, `covert_censorship`, `covert_suppression`, `targeted_silencing`, and `platform_governance_evasion` are rejected by the ethics policy.

`SimulationMetricSummary` includes:

- `average_latent_opinion`
- `average_expressed_opinion`
- `negative_ratio`
- `neutral_ratio`
- `positive_ratio`
- `polarization_index`
- `attention_level`
- `trust_recovery_proxy`
- `intervention_effect_score`
- `false_belief_proxy`
- `min_latent_opinion`
- `max_latent_opinion`
- `min_expressed_opinion`
- `max_expressed_opinion`
- `ethical_risk_flags`

`SimulationRunResult` includes:

- `simulation_status`
- `ethics_check`
- `initial_metrics`
- `final_metrics`
- `step_results`
- `visibility_intervention_result` when a visibility intervention is active
- `key_findings`
- `recommended_interpretation`
- `safe_mode`
- `warnings`

Run results intentionally omit individual targeting recommendations. `step_results.community_metrics` may include synthetic community aggregate metrics only.

## 19. Case-to-Simulation Initializer Schemas

The case-to-simulation initializer converts completed Sentigraph case outputs into a deterministic Simulation Lab scenario. It uses aggregate case data only and creates synthetic audience clusters; it never creates individual persuasion profiles or account-level influenceability scores.

`EventFrame` includes:

- `event_frame_id`
- `case_id`
- `event_title`
- `event_summary`
- `source_mode`
- `data_safety`
- `sub_issues`
- `observed_frame_profile`
- `baseline_public_profile`
- `frame_gap_analysis`
- `strategy_implications`
- `initialization_hints`
- `uncertainty_label`
- `uncertainty_reasons`
- `assumption_log`

`SubIssue` includes:

- `sub_issue_id`
- `category`
- `title`
- `summary`
- `observed_volume`
- `negative_ratio`
- `topic_risk_score`
- `risk_score` (alias for the topic risk score used by UI and benchmark summaries)
- `risk_level`
- `real_crisis_signal`
- `manipulation_signal`
- `influence_proxy`
- `evidence_quality`
- `evidence_examples`

`AudienceSegment` includes:

- `segment_id`
- `label`
- `segment_type`
- `proportion`
- `stance_distribution`
- `sentiment_distribution`
- `color_hint`
- `average_attention_level`
- `opinion_baseline`
- `action_threshold`
- `influence_proxy`
- `bridge_score`
- `data_origin`
- `warnings`

`PersonaCluster` includes aggregate cluster weights only:

- `confirmation_bias`
- `authority_trust`
- `conformity`
- `reactance`
- `negativity_weight`
- `attention_fatigue`
- `identity_attachment`
- `loss_sensitivity`
- `moral_outrage_sensitivity`
- `harm_salience`
- `crisis_legitimacy_pressure`
- `platform_activity`
- `no_individual_profile=true`

`ObservedFrameProfile` includes aggregate real-crisis mappings:

- `real_crisis_signal_score`
- `harm_salience`
- `loss_sensitivity`
- `moral_outrage_sensitivity`
- `crisis_legitimacy_pressure`
- `suspected_manipulation_pressure`
- `repetition_exposure`

`FrameGapAnalysis.primary_classification` is one of:

- `aligned_public_and_frame`
- `frame_more_negative_than_public`
- `frame_more_positive_than_public`
- `polarized_frame`
- `manipulation_suspected_frame`
- `insufficient_data`

`CaseSimulationInitializationResult` includes:

- `case_id`
- `status`
- `event_frame`
- `audience_segments`
- `persona_clusters`
- `frame_gap_analysis`
- `strategy_implications`
- `simulation_scenario`
- `warnings`
- `safe_mode`

`safe_mode` must keep `real_api_calls=false`, `real_llm_calls=false`, `live_fetch_enabled=false`, `individual_targeting=false`, and `automatic_action_execution=false`.

## 20. Simulation Strategy Report Export Schemas

The Simulation Lab strategy report export uses service-local Pydantic models under `backend/app/services/simulation/schemas.py` and a deterministic builder under `backend/app/services/simulation/simulation_report_builder.py`.

`SimulationStrategyReportRequest` includes:

- `simulation_mode`: `single` or `comparison`.
- `scenario_name`.
- `run_result` for single-scenario export.
- `result_a` and `result_b` for A/B comparison export.
- `intervention_a`.
- `intervention_b` when comparison mode is used.
- `comparison_summary` when the frontend has already computed A/B deltas.
- `generated_from`.

`SimulationStrategyComparisonSummary` includes aggregate comparison fields only:

- `better_option`
- `risk_a`
- `risk_b`
- `risk_delta`
- `negative_ratio_delta`
- `polarization_delta`
- `trust_recovery_delta`
- `attention_level_delta`
- `backlash_risk_a`
- `backlash_risk_b`
- `backlash_risk_delta`
- `exposure_reduction_delta`
- `visibility_backlash_delta`
- `trust_loss_delta`
- `spillover_risk_delta`
- `net_risk_change_delta`
- `ethical_risk_notes`
- `recommendation`
- `human_review_required`

`SimulationStrategyReportResponse` includes:

- `report`: report metadata such as title, generated time, scenario name, simulation mode, interventions, summary, ethical risk flags, human review requirement, and limitations.
- `markdown`: the generated Markdown strategy report.
- `safe_mode`: aggregate-only safety metadata.

The Markdown export must not include raw JSON dumps, raw prompts, raw user content, API key values, `.env` values, named user targets, account-level influenceability scoring, or automatic action-execution instructions.
