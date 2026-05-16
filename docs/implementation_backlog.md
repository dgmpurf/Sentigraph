# Sentigraph Implementation Backlog

Last updated: 2026-05-16

This backlog prioritizes practical next work while keeping the MVP mock-first and offline.

CI note: GitHub Actions CI is intentionally disabled. Do not restore or recreate `.github/workflows/ci.yml` unless explicitly requested. Use local/Codex validation commands such as `python -m pytest` and `npm run build`; future CI can be reconsidered only if cost and notification concerns are resolved.

## Completed Pre-v1.0 Hardening Items

### Local Demo Data Utilities

Status: implemented and validated on 2026-05-15.

Completed:

- `scripts/reset_local_data.py` safely resets project-local runtime JSON files and preserves `backend/data/.gitkeep`.
- `scripts/seed_demo_cases.py` creates deterministic demo cases, including one completed case with analysis, V1.5 topic risks, Chinese report, Markdown export data, snapshots, alerts, scheduler state, and notifications.
- `scripts/api_smoke_check.py` validates the local backend API flow without external services or Reddit credentials.
- Root `package.json` exposes helper commands: `data:reset`, `data:seed`, and `api:smoke`.
- Focused pytest coverage verifies reset/seed safety with temporary stores.

Acceptance:

- full backend tests passed with `92 passed in 2.82s`
- frontend production build passed in 7.75s
- local API smoke check passed with `26 passed, 0 failed`
- no MongoDB, Redis, real crawler, real platform API, external LLM, or real notification service was introduced

### Frontend Robustness Polish

Status: implemented and validated by production build on 2026-05-15.

Completed:

- global page-level `ErrorBoundary`
- not-found fallback page
- route-level lazy loading with `Suspense`
- Chinese risk labels in the top app shell
- stable QA selectors for notification/report copy and send actions

Known non-blocking issue:

- Vite still warns about large Ant Design and ECharts vendor chunks. The app/page chunks are split, and the warning is not blocking the local demo. Deeper vendor modularization can be revisited later if startup performance becomes a real user issue.

## P0: Demo Stabilization

### Browser QA Pass

Goal: confirm the desktop MVP works in a real browser runtime.

Scope:

- run `docs/demo_checklist.md`
- verify Dashboard, KeywordSearch, AnalysisResult, SummaryReport, RiskMonitor, and PropagationGraph
- confirm suggested response copy button works
- confirm empty/loading/error states
- capture any console/runtime errors

Acceptance:

- no major runtime errors
- copy button works
- charts render at 1440px desktop width
- known visual issues are documented

### Empty State Review

Goal: make mock-first failure modes feel intentional.

Scope:

- backend unavailable state
- empty visualization arrays
- empty report arrays
- small propagation graph

Acceptance:

- pages show user-facing empty states
- no raw JavaScript objects render in React
- no chart crashes

## P1: V1.5 Topic Risk Shadow Model

### Topic Risk Service

Goal: add deterministic topic-level risk without replacing active V1 scoring.

Status: implemented for the offline mock pipeline.

Scope:

- create a topic risk scoring service
- calculate per-topic risk fields from current topic clusters and analysis results
- output `risk_model_version = "v1_5_topic_risk_mvp"` for the shadow model result
- keep active project-level scoring as `v1_static_mvp`

Acceptance:

- deterministic pytest fixtures
- no external API/LLM dependency
- missing optional inputs do not crash
- MongoDB-safe dictionary keys

### Backward-Compatible Schema Fields

Goal: expose topic risk data safely.

Status: implemented for analysis, visualization, summary, and recommendation responses.

Scope:

- optional `topic_risks`
- optional `top_risk_topics`
- optional `real_crisis_risk`
- optional `manipulation_risk`
- optional `risk_explanation`

Acceptance:

- existing frontend does not break
- docs/api_contract.md and docs/data_schema.md stay aligned
- tests validate response shape

### Report and Visualization Integration

Goal: let reports and dashboards explain risk by topic.

Status: implemented for backend report/visualization responses and frontend report/dashboard pages. Browser QA remains recommended.

Scope:

- use V1.5 topic risk output when present
- add top risk topic explanations to report builder
- add optional chart-ready topic risk data

Acceptance:

- SummaryReport remains Chinese-first
- existing V1 score cards stay stable
- frontend handles missing V1.5 fields

## P2: Product Polish

### Saved Analysis Cases

Goal: make the demo feel like a case-based product.

Status: completed for the lightweight mock MVP with local JSON backend persistence and a frontend Cases page.

Scope:

- mock case model
- local JSON persistence
- case list or recent case panel
- current case context in header

Acceptance:

- user can return to the last mock case
- no real database required in the first version

Follow-up:

- MongoDB optional store is now implemented behind the existing case repository/storage interface.
- Add migration/backup behavior before production-style deployments.
- Keep Redis-backed caching/queue storage as future work.

### Report Export Preparation

Goal: make reports easier to share.

Status: completed for Markdown copy/download. PDF export remains future work.

Scope:

- print-friendly CSS
- report metadata block
- stable section spacing
- future PDF export placeholder

Acceptance:

- browser print preview is readable
- no PDF library required yet

### Alert Refinement

Goal: turn risk thresholds into practical warning cards.

Status: v0.9 foundation implemented with persisted case snapshots, deterministic threshold alerts, per-case monitoring config, a manual run-due scheduler endpoint, and a local notification outbox. Real background scheduler and external delivery channels remain future work.

Scope:

- persisted analysis snapshots per case
- deterministic mock monitoring checks
- threshold alerts for risk increase, risk-level escalation, real-crisis increase, manipulation-risk increase, new high-risk topics, and top-topic shifts
- warning severity labels
- recommended action mapping
- monitoring schedule config per case
- manual scheduler status and run-due endpoints
- local in-app notification outbox generated from alert events
- local simulate-send and mark-read notification state changes

Acceptance:

- RiskMonitor explains why an alert exists
- no real notification service or external delivery channel required
- no real background worker starts by default

Follow-up:

- Add APScheduler only after local manual scheduler behavior is stable.
- Add Celery/RQ only if a real queue and deployment target are defined.
- Add real notification channels later, behind explicit configuration and tests:
  - SMTP/email
  - Slack webhook
  - Enterprise WeChat
  - Feishu
  - generic webhook
- Add alert acknowledgement/resolution workflows when authentication exists.

## P3: Real Data Integration Preparation

### Data-source Readiness and Access Status Layer

Goal: make every platform's collection readiness explicit before enabling real data access.

Status: implemented for the mock-first MVP.

Scope:

- expose `GET /api/v1/platforms/status`
- keep `GET /api/v1/platforms` backward-compatible
- show mock availability, real-mode availability, API approval status, credential presence booleans, and real selectability
- keep Reddit `api_pending` and real mode disabled until approval
- keep crawler-later platforms visible but not real-selectable

Acceptance:

- no credential values are exposed
- no real platform APIs are called
- frontend platform display shows Chinese readiness labels
- `/crawl/start` keeps Reddit mock fallback while approval is pending

Current frontend support:

- `frontend/src/pages/PlatformIntegrationOverview.jsx` provides a desktop-first `平台接入总览` page for all data-source integrations.
- The page reads existing safe endpoints only: `GET /api/v1/platforms`, `GET /api/v1/platforms/status`, and `GET /api/v1/public-parsers/status`.
- It groups official API scaffolds, public-page parsers, Reddit, and disabled/future sources, displays credential presence as booleans only, and exposes public parser previews with `use_live_fetch=false`.
- It does not provide a live-fetch toggle and does not enable real adapter modes.

### Adapter Contracts

Goal: prepare real adapters without implementing crawlers yet.

Status: foundation implemented and QA-stabilized for the safe Reddit scaffold.

Scope:

- shared platform adapter interface
- request/response shape for public posts/comments
- safe rate-limit and credential placeholders
- fixture-first test strategy

Acceptance:

- no real platform calls
- no API keys required
- no bypass behavior
- outputs normalize into `RawPost` and `RawComment`
- missing credentials fall back to mock mode

### Crawl Adapter Bridge

Goal: connect `POST /api/v1/crawl/start` to the adapter factory for Reddit while preserving mock-first fallback behavior.

Status: implemented for Reddit with safe fallback metadata.

Scope:

- call `get_adapter("reddit")` when Reddit is selected
- keep existing crawl response fields backward-compatible
- return normalized mock `RawPost` / `RawComment` items in mock mode or fallback mode
- include safe platform metadata with adapter mode, fallback status, coarse fallback category, and schema validation booleans
- keep official API planned platforms as placeholders
- keep crawler-later platforms disabled

Acceptance:

- default mode performs no real Reddit API calls
- no credentials required for mock mode or tests
- Reddit real API mode is disabled while API approval is pending
- approval/config/dependency/auth/network/adapter states fall back to mock data without exposing secrets
- old mock crawl behavior remains backward-compatible
- backend tests cover Reddit-selected crawl start, mock mode, API-pending fallback, missing credentials fallback, and non-Reddit mock behavior

### Reddit Real Adapter Planning

Goal: define the first practical real-data candidate.

Status: `api_pending`. Mock mode is available; real API mode is disabled until Reddit approval is granted.

Scope:

- public API feasibility notes
- compliance constraints
- fixture schema
- adapter tests with recorded/sanitized fixtures only
- future optional real mode using `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT` after approval
- helper/status methods: `has_required_credentials()`, `get_mode()`, `is_real_mode_enabled()`, and `get_status_metadata()`

Acceptance:

- Reddit API approval remains pending before any live call
- credentials remain outside the repository
- current case/mock analysis flow remains offline; `/crawl/start` returns mock Reddit data while approval is pending
- tests use mocked Reddit responses and do not make network calls

### Future Compliant Public-Source Parser Framework

Goal: prepare a safe framework for public-source parsers without implementing scraping now.

Status: scaffolded for six fixture-only parsers plus an optional The Paper live pilot.

Scope:

- sanitized public HTML fixture format
- selector profile structure and versioning
- compliance checklist per source
- normalization to `RawPost` / `RawComment`
- deterministic parser tests with no external network calls

Implemented:

- `backend/app/services/crawling/public_parser/` framework package
- JSON selector profile loading
- simple deterministic HTML selector extraction for fixture tests
- conservative fetcher/robots helpers with live fetch disabled by default
- The Paper / Pengpai News (`the_paper`) `fixture_only` parser scaffold
- Jiemian News / 界面新闻 (`jiemian`) `fixture_only` parser scaffold
- Hupu / HuPu (`hupu`) `fixture_only` parser scaffold for forum-style thread/reply fixtures
- Maimai / 脉脉 (`maimai`) `fixture_only` parser scaffold for workplace and industry discussion fixtures
- Baidu Tieba / 百度贴吧 (`tieba`) `fixture_only` parser scaffold for forum-style thread/reply fixtures
- NGA (`nga`) `fixture_only` parser scaffold for forum-style thread/reply fixtures
- `/api/v1/crawl/start` public parser fallback metadata for explicit `the_paper`, `jiemian`, `hupu`, `maimai`, `tieba`, and `nga` requests
- unified public parser diagnostics endpoints:
  - `GET /api/v1/public-parsers/status`
  - `POST /api/v1/public-parsers/preview`
- frontend `公开页面解析` page with sidebar navigation, status table, fixture-safe preview buttons, sample post/comment cards, schema validation flags, and no live-fetch enable control
- deterministic fixture preview for The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA with sample `RawPost` / `RawComment` items and schema validation flags
- status/preview QA stabilized for all six parser sources, unknown-platform failure, disabled-live fallback, and fixture-only behavior when the global live-pilot flag is enabled
- Jiemian comments are documented as `comments_unavailable_without_login_or_dynamic_loading` and are not parsed in the fixture.
- Hupu visible fixture replies are normalized to `RawComment` with author, created time, parent id when present, and light/upvote count.
- Hupu fixture parser QA is stabilized for profile loading, thread/reply extraction, schema validation, safe missing-selector failure, `/crawl/start` metadata, and regressions for The Paper, Jiemian, Reddit mock/API-pending behavior, and old case/report/monitoring/scheduler/notification flows.
- Maimai fixture parser QA is stabilized for profile loading, post/reply extraction, schema validation, safe missing-selector failure, `/crawl/start` metadata, public parser status, public parser preview, Public Parser Status frontend dynamic listing behavior, fixture-only behavior when the global The Paper live-pilot flag is enabled, and regressions for The Paper, Jiemian, Hupu, Tieba, NGA, Reddit mock/API-pending behavior, and old case/report/monitoring/scheduler/notification flows.
- Tieba visible fixture replies are normalized to `RawComment` with author, created time, parent id when present, like count, and floor number in `RawComment.raw_data.floor_number`.
- Tieba fixture parser QA is stabilized for profile loading, thread/reply extraction, schema validation, safe missing-selector failure, `/crawl/start` metadata, forced fixture-only behavior when the global The Paper live-pilot flag is enabled, and regressions for The Paper, Jiemian, Hupu, Reddit mock/API-pending behavior, and old case/report/monitoring/scheduler/notification flows.
- NGA visible fixture replies are normalized to `RawComment` with author, created time, parent id when present, like count, and floor number in `RawComment.raw_data.floor_number`.
- NGA fixture parser QA is stabilized for profile loading, thread/reply extraction, schema validation, safe missing-selector failure, `/crawl/start` metadata, forced fixture-only behavior when the global The Paper live-pilot flag is enabled, and regressions for The Paper, Jiemian, Hupu, Tieba, Reddit mock/API-pending behavior, and old case/report/monitoring/scheduler/notification flows.
- Optional The Paper local live public-page fetch pilot behind `PUBLIC_PARSER_LIVE_FETCH_ENABLED=true`, with fixture/mock fallback as the default.

Safety constraints:

- do not use Reddit public-page scraping to bypass Reddit API approval
- do not use browser cookies, login bypass, captcha bypass, anti-bot evasion, proxy rotation, paywall bypass, hidden APIs, or private data access
- do not activate crawler-later platforms until compliance review, fixtures, selector tests, and explicit product requirements are ready

Next parser tasks:

- Add additional sanitized fixture variants for The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA.
- Add selector drift preview fixtures for alternate article/thread layouts per platform.
- Add additional browser QA screenshots for the Public Parser Status page at 1440px after the in-app browser tooling is available.
- Add a selector-drift QA matrix for missing title, content, author/source, created time, and permalink fields.
- Add a mocked test matrix for The Paper live pilot status categories if new failure categories are introduced.
- Add fixture-only parser scaffolds for the next candidate only after the current fixture QA matrix is stable.
- Keep live public fetching disabled until a separate compliance review and explicit local-only pilot task.

### Official API Application Packages

Goal: prepare future official API applications without implementing API calls yet.

Status: first scaffold round implemented and cross-platform QA-stabilized. Real official API integrations remain future work.

Completed:

- Weibo official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("weibo")` returns the Weibo adapter.
- `/api/v1/crawl/start` can return Weibo-style normalized mock `RawPost` and `RawComment` data with safe adapter metadata.
- `WEIBO_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Weibo API calls are made.
- Weibo scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and old adapter regressions.
- Weibo scaffold QA is stabilized: the explicit adapter interface, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Bilibili official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("bilibili")` returns the Bilibili adapter.
- `/api/v1/crawl/start` can return Bilibili-style normalized mock `RawPost` and `RawComment` data with safe adapter metadata.
- `BILIBILI_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Bilibili API calls are made.
- Bilibili scaffold QA is stabilized: mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and old case/monitoring/scheduler/notification/public-parser regressions are covered by tests.
- Douyin official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("douyin")` returns the Douyin adapter.
- `/api/v1/crawl/start` can return Douyin-style normalized mock short-video `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `DOUYIN_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Douyin API calls are made.
- Douyin scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Douyin scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with focused Douyin/adapter/crawl/registry checks (`20 passed in 0.67s`) and full `python -m pytest` (`213 passed in 3.10s`). Frontend build was not run for this adapter scaffold because no frontend files changed.
- Kuaishou official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("kuaishou")` returns the Kuaishou adapter.
- `/api/v1/crawl/start` can return Kuaishou-style normalized mock short-video/livestream `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `KUAISHOU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Kuaishou API calls are made.
- Kuaishou scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Kuaishou scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with focused Kuaishou/adapter/crawl/registry checks (`59 passed in 0.75s`) and full `python -m pytest` (`225 passed in 3.17s`). Frontend build was not run for this adapter scaffold because no frontend files changed.
- Xiaohongshu official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("xiaohongshu")` returns the Xiaohongshu adapter.
- `/api/v1/crawl/start` can return Xiaohongshu-style normalized mock lifestyle/community note `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `XIAOHONGSHU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Xiaohongshu API calls are made.
- Xiaohongshu scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Xiaohongshu scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with focused Xiaohongshu/adapter/crawl/registry checks (`63 passed in 0.77s`) and full `python -m pytest` (`237 passed in 2.90s`). Frontend build was not run for this adapter scaffold because no frontend files changed.
- Zhihu official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("zhihu")` returns the Zhihu adapter.
- `/api/v1/crawl/start` can return Zhihu-style normalized mock Q&A/article `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `ZHIHU_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Zhihu API calls are made.
- Zhihu scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Zhihu scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with focused Zhihu/adapter/crawl/registry checks (`67 passed in 0.80s`) and full `python -m pytest` (`249 passed in 3.04s`). Frontend build was not run for this adapter scaffold because no frontend files changed.
- Douban official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("douban")` returns the Douban adapter.
- `/api/v1/crawl/start` can return Douban-style normalized mock review/group/topic `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `DOUBAN_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Douban API calls are made.
- Douban scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Douban scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with focused Douban/adapter/crawl/registry checks (`71 passed in 0.76s`) and full `python -m pytest` (`261 passed in 3.29s`). Frontend build was not run for this QA pass because no frontend files changed.
- Toutiao official API adapter scaffold is implemented in mock mode.
- `adapter_factory.get_adapter("toutiao")` returns the Toutiao adapter.
- `/api/v1/crawl/start` can return Toutiao-style normalized mock article/micro-headline `RawPost` and visible-comment `RawComment` data with safe adapter metadata.
- `TOUTIAO_ADAPTER_MODE=real` is safely blocked as `api_pending` or `config_error`; no real Toutiao API calls are made.
- Toutiao scaffold coverage includes mock search/comments, normalization, missing credentials, real-mode blocked behavior, crawl metadata, platform registry status, and adapter factory registration.
- Toutiao scaffold QA is stabilized: the explicit adapter interface, default mock behavior, mock `RawPost` / `RawComment` schema fields, real-mode blocked behavior, crawl metadata, platform registry status, existing platform regressions, and old case/monitoring/scheduler/notification/public-parser regressions are covered by local tests.
- Latest local/Codex validation passed with full `python -m pytest` (`272 passed in 2.75s`). Frontend build was not run for this QA pass because no frontend files changed.
- Cross-platform adapter QA matrix is implemented in `backend/app/tests/test_cross_platform_adapter_consistency.py`.
- The matrix covers Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, Toutiao, and the fixture-only public parser adapters.
- It verifies adapter factory registration, official scaffold interface parity, default mock mode, safe blocked real-mode metadata, schema-valid `RawPost` / `RawComment` output, `/crawl/start` metadata, credential redaction, and fixture-first public parser preview behavior.
- Latest cross-platform validation passed with focused checks (`43 passed in 0.78s`) and full `python -m pytest` (`315 passed in 3.19s`). Frontend build was not run because no frontend files changed.

Near-term candidates:

- Browser QA for the Platform Integration Overview page and the existing Public Parser Status page at the desktop 1440px target
- Frontend/API mock data source selector QA for Keyword Search and case creation across Reddit plus all eight official API scaffolds
- Weibo official API application and approved implementation, only after permission scopes and compliance review are complete
- Bilibili real API application and approved implementation
- Kuaishou real API application and approved implementation, only after permission scopes and compliance review are complete
- Xiaohongshu real API application and approved implementation, only after permission scopes and compliance review are complete
- Zhihu real API application and approved implementation, only after permission scopes and compliance review are complete
- Douban real API application and approved implementation, only after permission scopes and compliance review are complete
- Toutiao real API application and approved implementation, only after permission scopes and compliance review are complete

Scope:

- document platform purpose, data minimization plan, callback/redirect needs if any, rate-limit expectations, and compliance notes
- list required app credentials and permissions without storing values in the repository
- prepare mock/fixture parity tests before any live API call

Safety constraints:

- no bypass behavior
- no private data collection
- no real API calls until approval, credentials, permission scopes, and rate limits are reviewed

## P4: Future Advanced Algorithm

### LLM Provider Interface

Goal: prepare future GPT / DeepSeek / Qwen assistance without changing the current offline MVP behavior.

Status: scaffolded and QA-stabilized with deterministic mock provider on 2026-05-16.

Implemented:

- `backend/app/services/llm/` provider module with a common interface, deterministic `MockProvider`, placeholder `OpenAIProvider`, `DeepSeekProvider`, and `QwenProvider`.
- `provider_factory.get_llm_provider()` defaults to `LLM_PROVIDER=mock`.
- `LLM_ENABLE_REAL_CALLS=false` remains the default; placeholder real providers return safe `provider_not_enabled` / `not_configured` errors and do not make network calls.
- `.env.example` documents `LLM_PROVIDER`, `LLM_ENABLE_REAL_CALLS`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, and `QWEN_API_KEY` without requiring values.
- `json_guard` helpers provide deterministic JSON object/array parsing fallbacks for future schema-checked LLM output.
- Keyword expansion now routes through `backend/app/services/keyword/keyword_expander.py`, calls the safe provider factory, and uses `MockProvider` only for current deterministic expansion.
- MockProvider keyword expansion is active for the keyword API and includes deterministic Tesla, Bilibili, Chinese-language, and generic public-opinion variants while preserving the existing keyword response schema.
- QA coverage verifies module presence, deterministic mock outputs, provider factory defaults and unknown-provider errors, provider-factory invocation from keyword expansion, disabled real-provider behavior, missing-key endpoint safety, secret redaction, safe keyword fallback, old keyword response-schema compatibility, and JSON guard fallback behavior.
- Latest backend validation passed with `python -m pytest` (`341 passed in 3.46s`).

Future real LLM integration tasks:

- Keep real OpenAI integration as a future task.
- Keep real DeepSeek integration as a future task.
- Keep real Qwen integration as a future task.
- Keep real LLM keyword expansion as a future task; current keyword expansion must remain MockProvider-only until an explicit real-provider integration task is approved.
- Keep any frontend or API LLM selector repair/status UI as a future task unless explicitly requested.
- Add provider-specific HTTP clients only behind explicit `LLM_ENABLE_REAL_CALLS=true` and selected provider configuration.
- Add strict prompt/output schemas for keyword expansion, topic labeling, risk explanations, report drafts, and recommendations.
- Add mocked HTTP tests, timeout handling, retry limits, rate limits, and redacted diagnostics before any live provider call.
- Add provider usage/cost safeguards and clear failure fallbacks to the deterministic pipeline.
- Keep GitHub Actions CI intentionally disabled unless explicitly requested later.

### V2 Dynamic Risk Readiness

Goal: prepare for full topic-cluster dynamic risk later.

Scope:

- time-windowed data fixtures
- topic history and baseline utilities
- influence graph metrics
- credibility modeling
- comparison between V1, V1.5, and V2 shadow outputs

Acceptance:

- V2 remains inactive until evaluated
- API migration is planned before exposure

## P5: v1.0 Persistence Upgrade

### MongoDB Store Behind Existing Repository Interface

Goal: add optional MongoDB-backed persistence without breaking the current local JSON demo flow.

Status: implemented as an optional v1.0 persistence backend.

Scope:

- keep `CASE_STORE_BACKEND=local_json` as the default for local/offline demo usage
- add an optional `mongo` backend behind the existing case repository/storage interface
- persist cases, reports, snapshots, alerts, scheduler config/state, and notifications
- document MongoDB connection settings in `.env.example` without committing secrets
- add indexes/schema notes for case id, updated time, alert level, notification status, and scheduler due time
- add migration/export/backfill strategy from local JSON to MongoDB
- add tests using mocked or isolated MongoDB-compatible fixtures; do not require MongoDB for the default test suite unless explicitly configured

Acceptance:

- current API contracts remain backward-compatible
- local JSON tests keep passing without MongoDB installed
- MongoDB path is optional and explicitly configured
- reset/seed/smoke tooling remains safe for local development

Implemented:

- `MongoDbCaseStore` implements the existing `CaseStore` interface.
- `create_case_store_from_env()` loads the repository-root `.env`, selects `local_json` by default, and selects `mongodb` only when `CASE_STORE_BACKEND=mongodb`.
- `.env.example` documents `MONGODB_URI` and `MONGODB_DATABASE`.
- MongoDB store unit tests use fake client/database objects and do not require a real MongoDB server.
- Fake-backed tests cover clear MongoDB connection failure errors and expected indexes for cases, markdown reports, snapshots, alerts, and notification outbox collections.
- Store factory tests cover the default local JSON backend, explicit local JSON, explicit MongoDB, missing MongoDB URI, MongoDB connection failure, and unknown backend errors.
- Default backend tests still run with local JSON.

Future production hardening:

- optional real MongoDB integration tests behind an explicit environment flag
- migration/export/import tooling from local JSON into MongoDB
- deployment-specific connection pooling, timeout, and backup guidance
- operational indexes review after real dataset shape is known
