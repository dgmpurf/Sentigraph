# Sentigraph Implementation Backlog

Last updated: 2026-05-15

This backlog prioritizes practical next work while keeping the MVP mock-first and offline.

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

Status: scaffolded for the first fixture-only parser.

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
- `/api/v1/crawl/start` public parser fallback metadata for explicit `the_paper` requests

Safety constraints:

- do not use Reddit public-page scraping to bypass Reddit API approval
- do not use browser cookies, login bypass, captcha bypass, anti-bot evasion, proxy rotation, paywall bypass, hidden APIs, or private data access
- do not activate crawler-later platforms until compliance review, fixtures, selector tests, and explicit product requirements are ready

### Official API Application Packages

Goal: prepare future official API applications without implementing API calls yet.

Status: planned.

Near-term candidates:

- Weibo
- Bilibili

Scope:

- document platform purpose, data minimization plan, callback/redirect needs if any, rate-limit expectations, and compliance notes
- list required app credentials and permissions without storing values in the repository
- prepare mock/fixture parity tests before any live API call

Safety constraints:

- no bypass behavior
- no private data collection
- no real API calls until approval, credentials, permission scopes, and rate limits are reviewed

## P4: Future Advanced Algorithm

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
- `create_case_store_from_env()` selects `local_json` by default and `mongodb` only when `CASE_STORE_BACKEND=mongodb`.
- `.env.example` documents `MONGODB_URI` and `MONGODB_DATABASE`.
- MongoDB store unit tests use fake client/database objects and do not require a real MongoDB server.
- Default backend tests still run with local JSON.

Future production hardening:

- optional real MongoDB integration tests behind an explicit environment flag
- migration/export/import tooling from local JSON into MongoDB
- deployment-specific connection pooling, timeout, and backup guidance
- operational indexes review after real dataset shape is known
