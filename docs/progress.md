# Sentigraph Progress

Last updated: 2026-05-16

## 1. Current Project Status

Sentigraph is currently in a mock-first desktop web MVP stage.

The repository has a FastAPI backend skeleton, a React + Vite desktop dashboard frontend, mock JSON data, API contracts, local development instructions, CI configuration, deterministic backend analysis services, a mock analysis pipeline, and a template-based public opinion report builder.

The current MVP flow is:

```text
keyword input -> mock pipeline analysis -> backend report/visualization APIs -> desktop dashboard
```

Real crawlers, real OpenAI/LLM calls, production database hardening, and complex ML models have not been implemented yet. The MVP remains runnable offline with mock data and deterministic rule/template logic.

Latest Bilibili official API adapter scaffold update: added `backend/app/services/crawling/bilibili_adapter.py` as a mock-first official API adapter scaffold for Bilibili video/comment-style public opinion data. `adapter_factory.get_adapter("bilibili")` now returns the Bilibili adapter, `/api/v1/crawl/start` routes explicit `platforms=["bilibili"]` through the adapter, and the response includes normalized mock `RawPost` / `RawComment` data plus safe metadata such as `source_type="official_api_adapter_scaffold"`, `mock_available=true`, `real_mode_available=false`, `api_pending=true`, and `real_mode_disabled=true`. `BILIBILI_ADAPTER_MODE=real` remains blocked as `api_pending` or `config_error`; no real Bilibili API calls or page scraping are implemented. Focused Bilibili/crawl/registry/adapter validation passed with `45 passed in 1.03s`; full backend validation passed with `189 passed in 3.25s`. Frontend build was not run because no frontend files changed.

Latest Bilibili official API adapter QA stabilization update: revalidated the Bilibili scaffold without credentials, real API calls, page scraping, login/captcha bypass, cookies, proxy rotation, private data access, or external LLM calls. Verified the adapter interface, default mock mode, missing-credential fallback, `BILIBILI_ADAPTER_MODE=real` safe `api_pending`/`config_error` behavior, `.env.example` Bilibili variables, adapter factory registration, platform registry status, `/api/v1/crawl/start` metadata, mock `RawPost` / `RawComment` schema fields, existing Reddit/public-parser adapters, case flow, V1.5 reports, monitoring, scheduler, alerts, notifications, public parser status/preview, and local JSON/MongoDB store regressions. Focused validation passed with `111 passed in 2.74s`; direct local adapter smoke returned 3 posts, 3 comments, and schema-valid crawl metadata; full backend validation passed with `189 passed in 3.09s`. Frontend build was not run because no frontend files changed.

Latest current milestone audit update: audited the mock-first Sentigraph state against the requested milestone list without product-code changes. Backend validation passed with `python -m pytest` (`167 passed in 3.02s`). Frontend validation passed with `npm.cmd run build` (`built in 7.69s`); the existing Vite warning for large Ant Design/ECharts vendor chunks remains non-blocking. No listed milestone is missing. Reddit remains partial by design because mock mode and the optional adapter scaffold are present, but real Reddit API use is still `api_pending` and disabled until approval.

| Milestone | Status | Evidence | Remaining work |
| --- | --- | --- | --- |
| Core mock MVP | complete | FastAPI mock APIs, React/Vite dashboard pages, mock pipeline, visualization/report flows, and local demo docs are present. | Production data sources remain out of scope. |
| V1.5 topic risk model | complete | `backend/app/services/scoring/topic_risk_score.py` and API/frontend handling expose `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_model_version`. | Future full V2 dynamic model remains planned. |
| Case management and Markdown export | complete | Case APIs, local JSON/MongoDB-capable store abstraction, Cases frontend flow, Summary Report case loading, and Markdown export are present. | Production multi-user persistence hardening remains future work. |
| Monitoring, alerts, scheduler, notifications | complete for local foundation | Monitoring snapshots, threshold alerts, manual scheduler/run-due endpoints, and local notification outbox APIs/UI are present. | No real background worker or external notification delivery yet. |
| Reddit mock/optional real adapter | partial | Reddit adapter, factory wiring, mock fallback, credential diagnostics, and approval-gated status exist. | Real Reddit API mode remains disabled until API approval; Reddit scraping remains not implemented. |
| Public parser foundation | complete | `backend/app/services/crawling/public_parser/` contains base parser, fetcher, registry, selector profiles, robots helper, parser status service, and tests. | More fixture variants and parser drift checks would improve confidence. |
| The Paper parser | complete | `the_paper` fixture parser and disabled-by-default live pilot scaffold are present. | Live fetch remains opt-in/local only and disabled by default. |
| Jiemian parser | complete | `jiemian` fixture-only article parser profile, fixture, crawl metadata, and tests are present. | Comments remain unavailable without public fixture visibility. |
| Hupu parser | complete | `hupu` fixture-only forum parser extracts thread and visible replies into `RawPost` / `RawComment`. | Live fetch remains disabled. |
| Maimai parser | complete | `maimai` fixture-only workplace/industry discussion parser extracts a visible post and replies into `RawPost` / `RawComment`. | Live fetch remains disabled. |
| Tieba parser | complete | `tieba` fixture-only forum parser extracts thread, visible replies, and floor numbers in `raw_data`. | Live fetch remains disabled. |
| NGA parser | complete | `nga` fixture-only forum parser extracts thread, visible replies, and floor numbers in `raw_data`. | Live fetch remains disabled. |
| Public parser status/preview APIs | complete | `GET /api/v1/public-parsers/status` and `POST /api/v1/public-parsers/preview` cover all six public parsers with fixture-first metadata. | Future UI/browser QA can add screenshots. |
| Public Parser Status frontend page | complete | `frontend/src/pages/PublicParserStatus.jsx`, sidebar route, and API helpers display status and fixture previews with `use_live_fetch=false`. | Manual browser click-through remains recommended before demos. |

Latest Maimai public parser update: added Maimai / 脉脉 (`maimai`) as a fixture-only public-page parser scaffold for company, workplace, and industry discussion-style content. The selector profile and sanitized fixture parse a public post title, main content, source/author, created time, permalink, interaction count, reply count, and two visible fixture replies normalized as `RawComment`. `POST /api/v1/crawl/start`, `GET /api/v1/public-parsers/status`, and `POST /api/v1/public-parsers/preview` now include `maimai` with safe fixture/mock metadata while keeping live fetch disabled. Focused parser/crawl/registry/adapter/status validation passed with `86 passed in 1.04s`; full backend validation passed with `176 passed in 3.09s`. Frontend build was not run because no frontend files changed for this parser task.

Latest Maimai public parser QA stabilization update: revalidated the Maimai fixture-only parser without enabling live fetch or calling real platform/API/LLM services. Verified Maimai profile loading, `RawPost` extraction for title/content/source/created time/permalink/interaction and reply counts, visible fixture reply `RawComment` extraction, schema validation, safe missing-selector failure, `/api/v1/crawl/start` metadata for `platforms=["maimai"]`, `GET /api/v1/public-parsers/status`, `POST /api/v1/public-parsers/preview`, Public Parser Status frontend dynamic listing behavior, forced fixture-only behavior when the global The Paper live-pilot flag is enabled, existing parser regressions for The Paper/Jiemian/Hupu/Tieba/NGA, Reddit API-pending/mock behavior, and old case/report/monitoring/scheduler/alert/notification flows. Focused parser/crawl/registry/adapter/status validation passed with `86 passed in 0.88s`; full backend validation passed with `176 passed in 3.29s`. Frontend build was not run because no frontend files changed in this QA pass.

Latest public parser status and preview QA update: stabilized the unified parser diagnostics layer for The Paper, Jiemian, Hupu, Tieba, and NGA. `GET /api/v1/public-parsers/status` returns all five parser profiles with effective live-fetch status, fixture/profile availability, comment support, safe limits, and notes. `POST /api/v1/public-parsers/preview` returns deterministic fixture-first preview data with sample `RawPost` / `RawComment` items, schema validation flags, and safe warnings such as `live_fetch_disabled` or `comments_unavailable_without_login_or_dynamic_loading`. Added regression coverage proving preview does not use live fetch unless the request explicitly opts in, fixture-only platforms stay fixture-only even when the global The Paper live-pilot flag is enabled, and unknown platforms fail safely. Live public fetching remains disabled by default, automated tests make no network calls, Reddit remains API-pending/mock, and Reddit scraping remains not implemented. Focused parser-status validation passed with `12 passed in 1.6s`; full backend validation passed with `167 passed in 3.23s`. Frontend build was not run because no frontend files changed.

Latest Public Parser Status frontend update: added a desktop-first `公开页面解析` page and sidebar navigation entry. The page calls `GET /api/v1/public-parsers/status`, displays all five parser sources (`the_paper`, `jiemian`, `hupu`, `tieba`, `nga`) with fixture/profile availability, comments support, safe limit, request interval, notes, and effective live-fetch status, and provides a per-platform `预览` action that calls `POST /api/v1/public-parsers/preview` with `limit=3` and `use_live_fetch=false`. Preview results render readable sample post/comment cards, fallback reason, warnings, and schema validation flags without directly rendering JavaScript objects. Frontend production build passed with `npm run build` in 7.94s; existing Ant Design/ECharts vendor chunk warning remains non-blocking. Local HTTP checks confirmed the frontend server returned 200, status returned all five parser profiles with `live_fetch_enabled=false`, and Hupu preview returned one post, two comments, schema-valid flags, and `fallback_reason_category=fixture_preview`. Backend code was not changed, so backend tests were not rerun for this frontend-only page task.

Latest Public Parser Status frontend QA stabilization update: rechecked the route wiring, sidebar entry, API helper normalization, status table, fixture preview panel, loading/empty/error states, and no-live-fetch frontend behavior. Added an inline `notes` column to the parser table so every parser row directly shows platform notes in addition to the safety-boundary notes card. API smoke checks confirmed `GET /api/v1/public-parsers/status` returns `the_paper`, `jiemian`, `hupu`, `tieba`, and `nga` with required fields and `live_fetch_enabled=false`; preview checks for all five parsers returned fixture-first samples with `use_live_fetch=false`, schema-valid flags, and no live attempts. `use_live_fetch=true` was also confirmed to fall back with `live_fetch_disabled` while global live fetch is disabled. Frontend production build passed with `npm run build` in 7.65s; the existing Ant Design/ECharts large vendor chunk warning remains non-blocking. Backend product code was not changed, so backend tests were not rerun in this QA pass.

Latest data-source readiness layer update: added a safe platform access status layer so all sources expose mock availability, real-mode availability, API approval status, credential presence booleans, and real selectability. `GET /api/v1/platforms/status` now returns readiness metadata for all platforms without exposing credential values. Reddit remains `api_pending`: mock mode is available, real Reddit API mode is disabled until approval, and public-page scraping is not implemented or used as a bypass. Keyword Search now displays Chinese readiness labels such as `Mock 可用`, `API 待审批`, `官方 API 规划中`, `未来公开页面解析`, and `暂不启用`. `/crawl/start` continues to return normalized mock Reddit data while approval is pending. Targeted readiness tests passed with `24 passed in 0.65s`; full backend validation passed with `114 passed in 2.56s`; frontend production build passed in 7.65s with the existing non-blocking Ant Design/ECharts vendor chunk warning.

Latest public-page parser framework update: added a compliant public-page parser scaffold under `backend/app/services/crawling/public_parser/`. The first site scaffold is The Paper / Pengpai News (`the_paper`) with a JSON selector profile and fixture-first parser tests. Live public fetching is disabled by default with `PUBLIC_PARSER_LIVE_FETCH_ENABLED=false`; the fetcher uses a polite user-agent, conservative rate limits, robots/profile checks, no cookies, no login, no captcha handling, no proxy rotation, and no private data access. `POST /api/v1/crawl/start` now routes explicit `the_paper` requests through `adapter_factory.get_adapter("the_paper")` and returns fixture/mock `RawPost` data plus safe metadata (`source_type`, `parser_status`, `live_fetch_enabled`, fallback category, and schema validation flags). Reddit scraping remains not implemented and must not be used to bypass Reddit API approval. Targeted parser/crawl/adapter/platform tests passed with `33 passed in 1.33s`; full backend validation passed with `123 passed in 2.45s`. Frontend build was not run because no frontend files changed.

Public parser revalidation update: rechecked the public-page parser foundation and adapter wiring without product-code changes. Full backend validation passed with `123 passed in 2.96s`; frontend build was not run because no frontend files changed.

Latest Jiemian public parser update: added Jiemian News / 界面新闻 (`jiemian`) as the second fixture-only public-page parser scaffold. The profile lives under `backend/app/services/crawling/public_parser/profiles/jiemian.json`, uses `source_type="public_page_parser"` and `status="fixture_only"`, and keeps live fetching disabled by default. The fixture parser extracts article title, content, source/author label, created time, and permalink into `RawPost`; comments are intentionally unavailable because the fixture does not expose public comments without login or dynamic loading (`comments_unavailable_without_login_or_dynamic_loading`). `POST /api/v1/crawl/start` now routes explicit `jiemian` requests through `adapter_factory.get_adapter("jiemian")` and returns safe fixture/mock metadata without enabling real crawling. Focused parser/adapter validation passed with `37 passed in 0.59s`; latest full backend validation passed with `127 passed in 2.56s`. Frontend build was not run because no frontend files changed.

Latest public parser fixture QA update: stabilized the fixture-only parser foundation for The Paper / Pengpai News and Jiemian News. Added focused QA assertions for The Paper author/date/url extraction, default `PublicFetcher.from_env()` live-fetch-disabled behavior, and Jiemian fixture/mock search fallback. `docs/demo_checklist.md` now includes public parser fixture smoke checks for `platforms=["the_paper"]` and `platforms=["jiemian"]`. Focused parser/crawl/registry/adapter validation passed with `39 passed in 0.56s`; full backend validation passed with `129 passed in 2.40s`. Live public fetching remains disabled by default, crawler-later platforms remain non-real-selectable, and Reddit remains API-pending/mock without scraping. Frontend build was not run because no frontend files changed.

Latest The Paper live public-page fetch pilot update: added an opt-in local live fetch pilot only for The Paper / Pengpai News. `PUBLIC_PARSER_LIVE_FETCH_ENABLED=false` remains the default, and fixture/mock fallback still handles disabled, blocked, unclear, network-failed, selector-failed, or parsing-failed cases. The live pilot records safe metadata fields (`live_fetch_attempted`, `live_fetch_allowed`, and `fetch_status`) on `/api/v1/crawl/start` without exposing secrets or using cookies, login, captcha handling, proxy rotation, anti-bot evasion, private data, Reddit scraping, platform APIs, or external LLM calls. Tests use mocked HTTP/fetch responses only and make no real network calls. Full backend validation passed with `134 passed in 2.37s`; frontend build was not run because no frontend files changed.

Latest The Paper live public-page fetch pilot QA update: stabilized the optional The Paper live pilot without enabling live fetch by default. Added mocked fetcher tests proving robots/policy is checked before any page request and that allowed live-fetch requests use only safe headers without cookies or authorization. Revalidated disabled-mode `/crawl/start` fixture/mock fallback metadata, mocked live success, robots-blocked fallback, network-error fallback, selector-error fallback, The Paper fixture parsing, Jiemian fixture parsing, Reddit API-pending/mock behavior, and old case/report/monitoring/scheduler/alert/notification flows through the full backend suite. Backend validation passed with `136 passed in 2.75s`; frontend build was not run because no frontend files changed. Live public fetching remains disabled by default.

Latest Hupu public parser update: added Hupu / HuPu (`hupu`) as a fixture-only public-page parser scaffold for forum-style discussion pages. The selector profile and sanitized fixture parse a public thread title, main content, author/source, created time, permalink, light/upvote count, reply count, and visible fixture replies normalized as `RawComment` with author, content, parent id when present, created time, and light/upvote count. `POST /api/v1/crawl/start` now routes explicit `hupu` requests through the public parser adapter and returns fixture parser data with safe metadata while keeping live fetch disabled. Focused parser/crawl/registry/adapter validation passed with `51 passed in 0.86s`; full backend validation passed with `141 passed in 3.46s`. Frontend build was not run because no frontend files changed.

Latest Hupu public parser QA stabilization update: revalidated the Hupu fixture-only parser without enabling live fetch or calling any real platform/API/LLM service. Verified Hupu profile loading, thread-level `RawPost` extraction, visible reply `RawComment` extraction, schema validation, safe missing-selector failure, `/api/v1/crawl/start` metadata for `platforms=["hupu"]`, The Paper and Jiemian parser regressions, Reddit API-pending/mock behavior, and old case/report/monitoring/scheduler/alert/notification flows. Focused public-parser plus old-flow validation passed with `99 passed in 2.52s`; full backend validation passed with `141 passed in 2.78s`. Frontend build was not run because no frontend files changed.

Latest Tieba public parser update: added Baidu Tieba / 百度贴吧 (`tieba`) as a fixture-only public-page parser scaffold for forum-style thread/reply pages. The selector profile and sanitized fixture parse a public thread title, main content, author/source, created time, permalink, like/upvote count, reply count, and three visible fixture replies normalized as `RawComment`; forum floor numbers are stored in `RawComment.raw_data.floor_number`. `POST /api/v1/crawl/start` now routes explicit `platforms=["tieba"]` requests through the public parser adapter and returns safe fixture metadata while keeping live fetch disabled. Focused parser/crawl/registry/adapter validation passed with `56 passed in 1.01s`; full backend validation passed with `146 passed in 2.97s`. Frontend build was not run because no frontend files changed.

Latest Tieba public parser QA stabilization update: revalidated the Baidu Tieba fixture-only parser without enabling live fetch or calling real platform/API/LLM services. Verified profile loading, thread-level `RawPost` extraction, visible reply `RawComment` extraction, reply floor numbers in `raw_data.floor_number`, schema validation, safe missing-selector failure, `/api/v1/crawl/start` metadata for `platforms=["tieba"]`, The Paper/Jiemian/Hupu parser regressions, Reddit API-pending/mock behavior, and old case/report/monitoring/scheduler/alert/notification flows. Tightened fixture-only safety so parser profiles without a live search URL, including Tieba, force `live_fetch_enabled=false` even if the global The Paper live-pilot flag is enabled. Focused parser/crawl/registry/adapter validation passed with `58 passed in 0.98s`; full backend validation passed with `148 passed in 2.84s`. Frontend build was not run because no frontend files changed.

Latest NGA public parser update: added NGA (`nga`) as a fixture-only public-page parser scaffold for forum-style thread/reply pages. The selector profile and sanitized fixture parse a public thread title, main content, author/source, created time, permalink, like/upvote count, reply count, and three visible fixture replies normalized as `RawComment`; forum floor numbers are stored in `RawComment.raw_data.floor_number`. `POST /api/v1/crawl/start` now routes explicit `platforms=["nga"]` requests through the public parser adapter and returns safe fixture metadata while keeping live fetch disabled. Focused parser/crawl/registry/adapter validation passed with `64 passed in 0.98s`; full backend validation passed with `154 passed in 3.03s`. Frontend build was not run because no frontend files changed.

Latest NGA public parser QA stabilization update: revalidated the NGA fixture-only parser without enabling live fetch or calling real platform/API/LLM services. Verified NGA profile loading, thread-level `RawPost` extraction, visible reply `RawComment` extraction, reply floor numbers in `raw_data.floor_number`, schema validation, safe missing-selector failure, `/api/v1/crawl/start` metadata for `platforms=["nga"]`, forced fixture-only behavior when the global The Paper live-pilot flag is enabled, The Paper/Jiemian/Hupu/Tieba parser regressions, Reddit API-pending/mock behavior, and old case/report/monitoring/scheduler/alert/notification flows. Focused parser/crawl/registry/adapter validation passed with `65 passed in 0.78s`; full backend validation passed with `155 passed in 3.01s`. Frontend build was not run because no frontend files changed.

Latest Reddit API approval status update: Reddit is now explicitly marked `api_pending` across the platform registry, API/data docs, adapter metadata, and implementation backlog. Reddit mock mode remains available and `/api/v1/crawl/start` continues to return normalized mock Reddit `RawPost` / `RawComment` data. Real Reddit API mode is disabled until Reddit approval is granted, even if local credentials and `REDDIT_ADAPTER_MODE=real` are present. Public-page scraping is not implemented and must not be used to bypass API approval. Targeted Reddit approval-gate tests passed with `21 passed in 0.58s`; full backend validation passed with `111 passed in 2.63s`; frontend build was not rerun because no frontend files changed.

Latest v1.0 MongoDB persistence update: added optional MongoDB persistence behind the existing `CaseStore` abstraction while keeping `local_json` as the default backend. `MongoDbCaseStore` stores analysis cases, analysis results, V1.5 topic-risk output, Chinese reports, Markdown reports, snapshots, alerts, scheduler config/state, and notification outbox items in separate MongoDB collections. `create_case_store_from_env()` selects MongoDB only when `CASE_STORE_BACKEND=mongodb`; normal tests and local development continue to use `CASE_STORE_BACKEND=local_json`. MongoDB connection settings are documented in `.env.example` as `MONGODB_URI=mongodb://localhost:27017` and `MONGODB_DATABASE=sentigraph`. If MongoDB mode is selected and the connection cannot be opened, case-store creation raises a clear configuration error rather than silently falling back. Added fake MongoDB unit tests so no real MongoDB server is required for the default suite. Backend validation passed with `99 passed in 2.39s`; local-json API smoke check passed with `26 passed, 0 failed`; frontend build was not run because no frontend files changed.

Latest optional MongoDB persistence QA update: rechecked the storage abstraction, repository facade, case/scheduler/notification/public-parser routes, `.env.example`, and runtime data ignore rules. `local_json` remains the default and works with zero extra setup; MongoDB is selected only by `CASE_STORE_BACKEND=mongodb`; unknown store backends now have explicit regression coverage for the safe `Unsupported CASE_STORE_BACKEND` error. Fake-backed tests cover MongoDB selection, connection failure, index creation, case/report/Markdown/snapshot/alert/notification persistence, reset behavior, and MongoDB-safe document keys without requiring a real server. Focused persistence and case API validation passed with `20 passed in 1.11s`; full backend validation passed with `179 passed in 3.35s`. Frontend build was not run because no frontend files changed.

Latest Reddit environment loading fix: backend startup now loads the repository-root `.env` through `python-dotenv` using a fixed path, without overriding existing environment variables. `reddit_adapter` also performs the same one-time project `.env` load for direct adapter usage. Added safe diagnostics that report only `REDDIT_ADAPTER_MODE` and present/missing status for Reddit credentials, never credential values. `.env` remains ignored by git. Targeted tests passed with `21 passed in 0.46s`; full backend validation passed with `109 passed in 24.96s`.

Latest Reddit real-mode diagnostic update: the Reddit real-mode client now uses PRAW as the optional official API dependency and records safe diagnostics only: `real_mode_reached`, `dependency_available`, `exception_class`, and `sanitized_error_category`. Fallback categories are now separated into `dependency_error`, `auth_error`, `network_error`, `parsing_error`, `config_error`, and `adapter_error`. A tiny local smoke check with `keyword=Tesla` and `limit=3` reached real mode, confirmed PRAW dependency availability, and safely categorized the live failure as `auth_error` with exception class `ResponseException`; fallback mock data remained schema-valid. Targeted tests passed with `23 passed in 0.60s`; full backend validation passed with `111 passed in 4.44s`.

Latest pre-v1.0 hardening update: completed the overnight hardening pass for the v0.9 mock MVP before MongoDB work. Added safe local developer utilities for resetting ignored runtime JSON data, seeding deterministic demo cases, and running an API smoke check against a local backend. Added focused tests for the reset/seed utilities, a frontend error boundary, a not-found fallback, route-level lazy loading, Chinese risk label consistency in the app shell, and stable QA selectors on notification/report copy actions. Backend validation passed with `92 passed in 2.82s`; frontend production build passed in 7.75s; API smoke check passed with `26 passed, 0 failed` against a temporary local backend and temporary project-local JSON store. The Vite large chunk warning remains for Ant Design and ECharts vendor chunks, but route-level page chunks are now split and the warning is non-blocking.

Pre-v1.0 phase status:

| Phase | Status | Result |
| --- | --- | --- |
| Phase 1: v0.9 notification and alert regression QA | complete | API smoke verified health, platforms, keyword/crawl/analysis, cases, Markdown export, monitor/run, alerts, scheduler, notifications, and outbox endpoints. |
| Phase 2: Local demo data tools | complete | Added `scripts/reset_local_data.py` and `scripts/seed_demo_cases.py`; reset is dry-run by default and preserves `backend/data/.gitkeep`. |
| Phase 3: API smoke test script | complete | Added `scripts/api_smoke_check.py`; it requires a running local backend and does not call external APIs or require Reddit credentials. |
| Phase 4: Frontend polish and robustness | complete | Added `ErrorBoundary`, `NotFound`, route-level lazy loading, Chinese risk labels, and stable QA selectors. |
| Phase 5: Test coverage hardening | complete | Added script-level tests for safe local reset/seed behavior; full backend suite passed. |
| Phase 6: Documentation cleanup | complete | Added pre-v1.0 notes, demo commands, release notes, and kept MongoDB as the next major task. |

Recommended next v1.0 task: add local JSON to MongoDB migration/export/import tooling and an optional real MongoDB integration smoke test behind an explicit environment flag, while preserving `local_json` as the default.

Latest local environment validation on Windows on 2026-05-14 passed: required repository folders are present, ignore rules cover local environment/cache/build outputs, backend dependencies install in the repository-root `.venv`, backend tests pass, frontend dependencies install, and the frontend production build completes.

Latest platform selection update: Sentigraph now exposes Reddit plus the Chinese official-API-planned platforms as mock-selectable MVP choices, shows the full platform roadmap in the Keyword Search page, and keeps YouTube only as `disabled_or_optional_future`.

Latest report builder update: the backend template-based public opinion report builder remains fully offline and now uses sentiment trend changes plus visualization propagation graph data when available. Backend validation passed with `26 passed in 0.36s`.

Latest frontend report update: Summary Report and Analysis Result now consume the existing `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate` responses through the frontend API client and render an export-friendly structured public opinion report. Frontend validation passed with `npm.cmd --prefix frontend run build`; backend validation passed with `26 passed in 0.35s`.

Latest report API normalization update: `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate` now return a stable normalized public opinion report structure with `project_id`, `report_language`, `risk_score`, `risk_level`, `overall_summary`, `key_findings`, `main_risk_factors`, `top_negative_topics`, `representative_comments`, `suspected_bot_signals`, `recommended_actions`, `suggested_public_response`, and `generated_from_mock_pipeline`. The default report language is deterministic `zh-CN`, with optional `en-US`. Backward-compatible fields such as `summary`, `main_risks`, and `suggested_response` are still present. Backend validation passed with `27 passed in 0.32s`.

Latest frontend report language update: the frontend now explicitly calls summary/recommendation report APIs with `report_language: "zh-CN"`, prefers normalized report fields over legacy compatibility fields, derives a Chinese risk label such as `中等风险` while preserving the raw English `risk_level`, and displays report sections with Chinese labels by default. Frontend validation passed with `npm.cmd --prefix frontend run build`; backend validation passed with `27 passed in 0.33s`.

Latest algorithm design update: added the public opinion risk algorithm design document and risk model roadmap. The current active backend risk model is versioned as `v1_static_mvp`. V2 topic-cluster dynamic risk is documented and prepared as a future placeholder only; it is not implemented or active yet. Backend validation passed with `28 passed in 0.37s`.

Latest frontend Chinese report connection update: Summary Report and Analysis Result now render the backend normalized Chinese public opinion report fields directly from `summary/generate` and `recommendation/generate`. The frontend API client defaults both report requests to `report_language: "zh-CN"`, report rendering supports optional future `risk_model_version` and `risk_level_label`, and empty arrays render as report empty states instead of raw JSON. Frontend validation passed with `npm.cmd --prefix frontend run build`; backend validation passed with `28 passed in 0.37s`.

Latest README/full validation update: README endpoints match the FastAPI app, the documented Windows backend command imports successfully, backend tests pass with `28 passed in 0.37s`, `npm.cmd install` in `frontend` reports dependencies up to date, and `npm.cmd run build` completes successfully in 8.51s. API smoke checks confirm normalized `zh-CN` summary/recommendation report responses, 17 registered platforms, mock-selectable platforms `reddit`, `weibo`, `bilibili`, `douyin`, `kuaishou`, `xiaohongshu`, `zhihu`, `douban`, and `toutiao`, and YouTube remains inactive.

Latest frontend report API connection update: Summary Report and Analysis Result continue to request `report_language: "zh-CN"` from `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate`. Summary Report now always displays a clear report metadata strip with project ID, report language, risk score, risk level, and the current frontend fallback risk model version `v1_static_mvp` when the backend has not yet returned `risk_model_version`. Frontend build passed with `npm.cmd run build` in 8.52s, backend tests passed with `28 passed in 0.38s`, and API smoke checks confirmed normalized Chinese report responses.

Latest visualization refinement update: Dashboard, RiskMonitor, and PropagationGraph were improved into a more polished desktop public opinion monitoring experience. Dashboard now emphasizes the latest public opinion summary, risk score, risk factors, sentiment trend, topic clusters, bot impact, platform heatmap, and platform distribution. RiskMonitor now shows a risk model version fallback, risk level explanation, factor descriptions, warning cards, and trend/propagation/controversy insights. PropagationGraph now supports visualization-data fallback, small-graph guidance, central node detail, node breakdown, and edge detail panels. Frontend build passed with `npm.cmd run build` in 8.47s, backend tests passed with `28 passed in 0.39s`, and API smoke checks confirmed visualization plus propagation graph data.

Latest roadmap audit update: the current codebase was audited against the MVP roadmap without product code changes. Backend tests passed with `28 passed in 0.38s`, frontend production build passed with `npm.cmd run build` in 8.56s, and API smoke checks confirmed health, 17 registered platforms, 9 mock-selectable MVP platforms, visualization data, normalized `zh-CN` summary report output, and propagation graph data.

Latest MVP stabilization update: backend visualization/report responses now include `risk_model_version="v1_static_mvp"`, and normalized summary/recommendation reports include a display-only `risk_level_label` such as `中等风险` while preserving the raw English `risk_level`. `docs/api_contract.md` and `docs/data_schema.md` were updated for these stable fields, and `docs/demo_checklist.md` was added for local demo QA. Backend tests passed with `28 passed in 0.40s`; API smoke confirmed summary/recommendation/visualization metadata; frontend build passed in 7.73s. Vite large chunk warning remains for Ant Design and ECharts vendor chunks, but the application chunk was reduced through safe vendor chunking. in-app Browser runtime QA was attempted twice and timed out, so interactive screenshot/copy-button verification remains a manual/browser-runtime follow-up item.

Latest next-stage planning update: added product planning docs for requirements, feature matrix, UX flow, and implementation backlog. `docs/algorithm_design.md` and `docs/risk_model_roadmap.md` now define a practical V1.5 topic-level risk model between the current `v1_static_mvp` model and the future V2 dynamic model. V1.5 is planned as a deterministic shadow model only; no product code, crawler, platform API, OpenAI/LLM call, authentication, or active scoring behavior changed in this planning task.

Latest V1.5 risk model update: implemented deterministic offline topic-level risk scoring in `backend/app/services/scoring/topic_risk_score.py` with `risk_model_version="v1_5_topic_risk_mvp"`. The mock pipeline now produces `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation` for visualization and normalized Chinese report responses. The old V1 static scoring module remains in place for factor/radar compatibility. Backend tests passed with `33 passed in 0.46s`. No frontend code changed, so frontend build was not required for this task.

Latest frontend V1.5 topic-risk display update: Dashboard, AnalysisResult, RiskMonitor, and SummaryReport now render the V1.5 topic-level risk fields from visualization/report APIs. The frontend API client normalizes `risk_model_version`, `topic_risks`, `top_risk_topics`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`; Dashboard shows the current risk model and top 3 high-risk topics; AnalysisResult shows topic risk cards with scores, levels, and explanations; RiskMonitor shows real-crisis risk, manipulation risk, and top risk drivers; SummaryReport/PublicOpinionReport includes top risk topics with explanations. Frontend build passed with `npm.cmd run build`; backend tests passed with `33 passed in 0.35s`. The existing Vite large chunk warning remains non-blocking.

Latest backend V1.5 completion update: `AnalysisResultResponse` now also exposes the V1.5 topic-level fields when topic clusters exist: `risk_model_version`, `topic_risks`, `top_risk_topics`, `max_topic_risk`, `average_topic_risk`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`. The mock pipeline attaches these fields to `GET /api/v1/analysis/{project_id}` while keeping the old `risk.risk_score` and `risk.risk_level` fields. Added explicit tests for analysis response V1.5 fields and `top_risk_topics` ordering. Backend tests passed with `34 passed in 0.40s`; frontend build was not needed because no frontend API handling changed.

Latest frontend V1.5 API alignment update: the frontend API client now normalizes V1.5 fields from `GET /api/v1/analysis/{project_id}` as well as visualization, summary, and recommendation responses. The shared report model now treats analysis output as a source for `risk_model_version`, `topic_risks`, `top_risk_topics`, `overall_risk`, `max_topic_risk`, `average_topic_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`. Dashboard also displays separate `真实危机风险` and `操纵传播风险` cards. Frontend build passed with `npm.cmd run build` in 7.59s; backend tests were not rerun because this task only changed frontend normalization/display and docs. The existing non-blocking Vite vendor chunk warning remains.

Latest browser QA and demo polish update: a 1440x900 desktop browser smoke test passed for Dashboard, Keyword Search, Analysis Result, Summary Report, Risk Monitor, and Propagation Graph. The mock analysis flow was exercised from Keyword Search back to Dashboard, V1.5 fields displayed correctly across pages, the Chinese structured report rendered, the suggested public response copy button wrote report text to the browser clipboard, crawler-later platforms were visible as disabled/future items, and YouTube remained inactive. Small polish fixes were added: Summary Report risk badge text no longer wraps the raw risk enum, copy buttons now have stable QA selectors, and `frontend/index.html` includes a local favicon to avoid the browser favicon 404. Backend tests passed with `34 passed in 0.38s`; frontend build passed in 7.64s with the existing non-blocking Vite vendor chunk warning. The in-app Browser runtime still timed out, so QA used a local Playwright + Chrome fallback.

Latest case management and Markdown export update: Sentigraph now has lightweight analysis case management for the mock MVP, currently backed by local JSON persistence. New backend endpoints support creating cases, listing cases, retrieving case details, running the existing offline V1.5 mock pipeline for a case, and exporting a Chinese public opinion report as Markdown. The frontend now includes a Cases page, Keyword Search creates and runs a case, the header shows the current case, Summary Report can copy/download Markdown for the selected completed case, and the existing Dashboard, AnalysisResult, RiskMonitor, PropagationGraph, and Chinese report pages continue to work. Backend tests passed with `40 passed in 0.41s`; frontend build passed in 7.55s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser QA via local Playwright + Chrome passed for create case -> run mock analysis -> Cases list -> open report -> copy Markdown -> download `.md` -> V1.5 page navigation, with no console errors.

Latest v0.3 stabilization QA update: the case management and Markdown export flow was revalidated end to end without product code changes. Backend tests passed with `40 passed in 0.43s`, frontend production build passed in 7.71s, API smoke checks passed for all new case endpoints plus the existing platform, visualization, summary, recommendation, and analysis endpoints, and browser QA passed at a 1440x960 desktop viewport. The browser flow verified Keyword Search -> create/run case -> Dashboard -> Cases -> Summary Report -> copy suggested public response -> copy Markdown -> download `.md` -> AnalysisResult -> RiskMonitor -> PropagationGraph, with no relevant console errors. The in-app Browser runtime still timed out, so this QA pass used temporary Playwright + Chromium tooling outside the repository; no project dependency files were changed.

Latest platform adapter foundation update: added a safe shared platform adapter interface, adapter factory, and Reddit adapter scaffold. Reddit defaults to mock mode and falls back to local mock data when `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, or `REDDIT_USER_AGENT` are missing. Optional real mode is explicit only and is not connected to the current case flow or mock dashboard. Adapter outputs normalize into existing `RawPost` and `RawComment` schemas, with mocked Reddit response tests covering normalization and factory registration. Backend tests passed with `44 passed in 0.42s`; frontend build was not rerun because no frontend files changed.

Latest platform adapter revalidation update: re-read the required project docs and rechecked the adapter scaffold. The active interface remains `search_posts`, `fetch_comments`, `normalize_post`, and `normalize_comment`; Reddit remains mock-first with credential-gated optional real mode and local mock fallback. Backend tests passed with `44 passed in 0.41s`; frontend build was not rerun because this task did not change frontend files.

Latest case management and Markdown export revalidation update: re-read the required project docs and rechecked the existing lightweight case-based mock MVP implementation. The backend case schemas, case store facade, local JSON persistence layer, case routes, V1.5 mock pipeline attachment, Chinese report attachment, and Markdown report export are present; the frontend Cases page, Keyword Search create/run flow, Summary Report case loading, and Markdown copy/download controls are present. Backend tests passed with `44 passed in 0.50s`; frontend production build passed in 7.92s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks passed for create case, run case, Markdown export, and the existing platform, visualization, summary, recommendation, and analysis endpoints.

Latest v0.3 case-flow stabilization QA update: completed a full stabilization pass for lightweight case management and Markdown export. API smoke checks passed for all case endpoints, old MVP endpoints, Markdown report content, V1.5 topic-risk fields, 9 mock-selectable platforms, crawler-later disabled state, and YouTube inactive state. Backend tests passed with `44 passed in 0.48s`; frontend production build passed in 7.83s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser QA at 1440x960 passed through a Chrome headless CDP fallback after the in-app Browser connection timed out: Dashboard, Keyword Search, Cases, Analysis Result, Summary Report, Risk Monitor, and Propagation Graph rendered; create/run case worked; suggested public response copy worked; Markdown copy worked; no relevant console errors or `[object Object]` rendering were observed.

Latest Reddit adapter contract update: the shared platform adapter interface now includes `health_check`, `supports_real_mode`, and `get_required_credentials` in addition to search/fetch/normalize methods. `get_adapter("reddit")` is available as a factory alias, `.env.example` documents `REDDIT_ADAPTER_MODE=mock`, and the Reddit adapter can read that mode while still falling back to local mock data if credentials are missing. Backend tests passed with `46 passed in 0.50s`; frontend build was not rerun because no frontend files changed.

Latest platform adapter QA update: completed a stabilization pass for the shared adapter foundation and Reddit mock scaffold. Verified the adapter files exist, `.env.example` contains the Reddit placeholders plus `REDDIT_ADAPTER_MODE=mock`, Reddit defaults to mock mode, missing credentials do not crash, `get_adapter("reddit")` returns `RedditAdapter`, unknown/planned/crawler-later platforms raise safe adapter errors, and normalized mock output validates as `RawPost`/`RawComment`. API smoke checks passed for health, platforms, crawl start, cases list/create/run, Markdown export, visualization, summary, and recommendation endpoints. Backend tests passed with `47 passed in 0.43s`; frontend build was not needed because no frontend files changed.

Latest long maintenance pass: completed the requested six-phase safe maintenance run. Phase 1 audit found the project skeleton, V1.5 topic-risk backend, frontend V1.5 display, case management, Markdown export, platform registry, Reddit adapter foundation, demo checklist, and README to be complete for the mock-first MVP. Phase 2 confirmed case creation/list/detail/run plus Markdown export still work. Phase 3 confirmed Reddit mock adapter defaults to offline mock mode and no planned/crawler-later platform is activated as an adapter. Phase 4 confirmed frontend production build passes; the existing Ant Design/ECharts vendor chunk warning remains non-blocking. Phase 5 confirmed backend tests pass with `47 passed in 0.42s` and API smoke checks pass for old MVP and case/report endpoints. Phase 6 updated docs for the v0.4 checkpoint and kept real Reddit mode out of scope.

Latest Reddit minimal real-mode update: the Reddit adapter now exposes explicit mode/status helpers (`has_required_credentials()`, `get_mode()`, `is_real_mode_enabled()`, and `get_status_metadata()`) and keeps `REDDIT_ADAPTER_MODE=mock` as the safe default. Optional real mode is enabled only when `REDDIT_ADAPTER_MODE=real` and all three Reddit credentials are present. Missing credentials fall back to mock mode without crashing. Real-mode search and comments continue to use the lightweight official Reddit HTTP path with conservative request limits, while tests use mocked clients and make no network calls. Targeted Reddit adapter tests passed with `9 passed in 0.14s`.

Latest Reddit real-mode hardening update: tightened the Reddit adapter so a code-level `mode="real"` request cannot enable live Reddit access unless the environment gate is also `REDDIT_ADAPTER_MODE=real` and all required credentials are present. Adapter status metadata now includes `env_mode` alongside requested and active modes. Targeted Reddit adapter tests passed with `11 passed in 0.12s`, and full backend validation passed with `51 passed in 0.43s`. Frontend build was not rerun because no frontend files changed.

Latest v0.5 Reddit real-mode QA update: revalidated the minimal Reddit real-mode integration without enabling live product flows. `REDDIT_ADAPTER_MODE=mock` remains the default, missing credentials fall back to mock mode, and real mode requires `REDDIT_ADAPTER_MODE=real`, all three Reddit credentials, and an explicit code-level real-mode request. Targeted Reddit adapter tests passed with `11 passed in 0.09s`; full backend tests passed with `51 passed in 0.41s`; API smoke checks passed for health, platform registry, crawl start, case create/run, V1.5 topic-risk output, Chinese report, Markdown export, visualization, summary, and recommendation. Frontend build was not rerun because no frontend files changed. Recommended checkpoint tag: `v0.5-reddit-real-mode-qa`.

Latest local JSON persistence update: case management now uses a repository/storage abstraction with `LocalJsonCaseStore` as the default backend. Created cases, completed V1.5 mock analysis output, Chinese structured reports, and Markdown report metadata persist to `backend/data/cases.json` by default, while tests use temporary JSON paths and do not write to the demo store. Runtime case JSON files are ignored by git via `backend/data/*.json`; `backend/data/.gitkeep` preserves the directory. Targeted persistence/case API tests passed with `9 passed in 0.53s`; full backend validation passed with `54 passed in 0.53s`. Frontend build was not rerun because no frontend files changed. MongoDB/Redis remain future TODOs behind the same interface.

Latest v0.6 persistence QA update: revalidated the local JSON persistence layer and tightened git hygiene for runtime store files. Case APIs still use the repository/storage layer, created and completed cases persist through a repository reload, and Markdown export remains available after reload. `.gitignore` now excludes both `backend/data/*.json` and transient `backend/data/*.json.tmp` while keeping `backend/data/.gitkeep`. Targeted case/persistence tests passed with `10 passed in 0.49s`; full backend validation passed with `55 passed in 0.51s`. Frontend build was not rerun because no frontend files changed. Known limitation: local JSON persistence is suitable for the offline demo but is not a production database or concurrent multi-user store.

Latest v0.7 monitoring foundation update: implemented persisted analysis snapshots and deterministic threshold-based alert events for local analysis cases. `POST /api/v1/cases/{case_id}/run` now saves a baseline snapshot, `POST /api/v1/cases/{case_id}/monitor/run` creates a new deterministic mock monitoring snapshot, evaluates risk increase / risk-level escalation / real-crisis delta / manipulation delta / new high-risk topic / top-topic shift alerts, and persists alert events in the same local JSON store. New endpoints are available for case snapshots, case alerts, and all persisted alerts. Risk Monitor now displays monitoring status, risk delta, latest snapshots, alert badges, top triggered reason, real-crisis risk, manipulation risk, and high-risk topic cards. Backend validation passed with `65 passed in 1.04s`; frontend production build passed in 7.54s with the existing non-blocking Ant Design/ECharts vendor chunk warning.

Latest v0.7 monitoring QA update: revalidated the monitoring and alert foundation without enabling real crawlers, real platform APIs, external LLM calls, authentication, MongoDB/Redis, or a scheduler. Added narrow regression coverage for real-crisis-risk alert detection, repeated monitor runs, persisted snapshot history, deterministic risk deltas, and the frontend-loaded legacy `GET /api/v1/alerts/{project_id}` path. Backend tests passed with `68 passed in 1.05s`. Frontend production build passed in 7.45s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks passed for health, platform registry, crawl start, analysis, visualization, summary, recommendation, case create/list/detail/run, Markdown export, snapshots, monitor/run, case alerts, and all alerts. The in-app browser automation connection timed out during this QA pass; the frontend dev server responded with HTTP 200, and RiskMonitor source/build/API wiring were verified, but an interactive click-through should still be repeated manually or with a stable browser runtime before a public demo.

Latest v0.8 scheduler foundation update: added a safe manual scheduler foundation for case monitoring. Cases now persist `monitoring_config` with enabled/disabled state, interval, last/next run times, threshold config, and schedule status. New endpoints support scheduler status, manual run-due checks, and per-case monitoring config/enable/disable. `POST /api/v1/scheduler/run-due` scans enabled due cases, calls the existing deterministic mock monitoring check, saves snapshots and alerts, and advances `last_run_at` / `next_run_at`; no real background worker starts by default. Risk Monitor now displays monitoring config and provides `启用监控`, `暂停监控`, and `运行到期监控任务` controls. Final backend tests passed with `78 passed in 1.53s`; final frontend production build passed in 7.59s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks passed for scheduler status/run-due, monitoring config, enable/disable, old monitor/run, case flow, and old MVP endpoints. In-app browser automation still timed out, so manual RiskMonitor click-through remains recommended before a live demo.

Latest v0.8 scheduler QA stabilization update: revalidated the scheduler foundation without starting a background scheduler and without calling real crawlers, platform APIs, external LLM APIs, MongoDB, or Redis. Added focused regression tests for disabled cases not being executed by `run-due`, interval-based `last_run_at` / `next_run_at` updates, and case-specific threshold configs being honored by scheduler-triggered monitoring. Full backend validation passed with `81 passed in 1.76s`. Frontend production build passed in 7.46s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks passed 24 scheduler/case/old-MVP checks using a project-local temporary JSON store that was removed after the run. The in-app Browser runtime timed out when opening `http://127.0.0.1:5173`; source-level RiskMonitor wiring, API smoke checks, and production build passed, but a manual browser click-through of the scheduler controls remains recommended before a public demo.

Latest v0.9 notification foundation update: added a local notification outbox for monitoring alerts. Alert events generated by `POST /api/v1/cases/{case_id}/monitor/run` and `POST /api/v1/scheduler/run-due` now create deterministic in-app notification records in the local JSON store, with duplicate prevention by alert/channel id. New endpoints list all notifications, list case notifications, mark notifications read, simulate-send one notification, simulate-send all pending notifications, and report outbox status. Risk Monitor now includes a `通知中心` panel with unread/pending counts, local send state, associated case id, mark-read, and simulate-send controls. No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, crawler, platform API, OpenAI/LLM, authentication, MongoDB, Redis, or background worker was added. Backend tests passed with `90 passed in 2.29s`; frontend production build passed in 7.76s with the existing non-blocking Ant Design/ECharts vendor chunk warning. API smoke checks on a fresh local backend confirmed case create/run, monitor/run, notification creation, outbox status, simulate-send-pending, and mark-read. The in-app Browser runtime timed out when opening the local frontend, so manual RiskMonitor notification click-through remains recommended before a public demo.

Latest v0.9 notification QA stabilization update: revalidated the notification foundation without calling any real notification, platform, crawler, or LLM service. Full backend tests passed with `90 passed in 2.34s`. Frontend production build passed in 7.61s; the existing Ant Design/ECharts vendor chunk warning remains non-blocking. Isolated API smoke checks with a temporary project-local JSON store verified case create/run, `monitor/run`, alert creation, notification creation, required notification fields, mark-read, simulate-send, scheduler status, monitoring config, scheduler run-due, Markdown export, platform registry, visualization data, and Chinese summary/recommendation report responses. Fixed a schema consistency issue so `POST /api/v1/notifications/{notification_id}/simulate-send` now exposes `simulated_sent_at` at the top level as well as inside the nested notification. Also corrected a garbled Windows path in `docs/demo_checklist.md`. The in-app Browser runtime timed out twice against an isolated local frontend, so source-level RiskMonitor wiring, production build, and API smoke checks passed, while manual browser click-through of notification buttons remains recommended before a public live demo.

Maintenance status audit:

| Area | Status | Notes |
| --- | --- | --- |
| Project skeleton | complete | Backend, frontend, docs, mock data, tests, and local scripts are present. |
| V1.5 topic-risk backend | complete | `v1_5_topic_risk_mvp` fields appear in analysis, visualization, summary, recommendation, and case run outputs. |
| Frontend V1.5 display | complete | Dashboard, AnalysisResult, RiskMonitor, and SummaryReport consume V1.5 fields; production build passes. |
| Case management | complete | Local JSON-backed case APIs, repository/storage abstraction, frontend case flow, snapshots, and alerts are present. |
| Markdown export | complete | Completed cases export/copy Markdown with report sections and risk metadata. |
| Monitoring, alerts, scheduler, and notification foundation | complete for v0.9 foundation | Case runs create snapshots; mock monitoring checks create deterministic shifted snapshots and persisted threshold alerts; manual scheduler config/run-due endpoints are available; alert events create local in-app notification outbox items. No real background scheduler or external notification delivery exists. |
| Platform registry | complete | 9 mock-selectable platforms are active; crawler-later and YouTube remain inactive. |
| Reddit adapter foundation | complete for mock scaffold | Adapter contract, factory, mock fallback, credential placeholders, and tests are present. Real mode remains future. |
| Demo checklist | complete | Includes v0.9 notification outbox demo steps, v0.8 scheduler QA steps, and optional Reddit mock adapter smoke check. |
| README accuracy | complete with caveat | Run/API instructions remain usable; README now notes V1.5 mock topic-risk outputs. Some existing Chinese text displays garbled in the current terminal encoding. |

Recommended release checkpoint:

- Checkpoint name: Sentigraph v0.9 notification foundation.
- Suggested git tag: `v0.9-notification-foundation`.
- Completed capabilities: mock-first V1.5 topic-risk pipeline, Chinese structured reports, lightweight local JSON-backed cases, Markdown export, persisted monitoring snapshots, threshold alert events, manual scheduler config/run-due foundation, local notification outbox, platform registry, Reddit mock/optional real-mode adapter scaffold, and full backend/frontend local validation.
- Known non-blocking issues: Vite still reports large vendor chunks for Ant Design and ECharts; browser QA may require Playwright/Chrome fallback if the in-app Browser runtime times out. Local JSON persistence is demo-friendly but not a production database or concurrent multi-user store. Monitoring remains manual/mock-only; notifications remain local mock-only and do not send real external messages.
- Next recommended task: run one manual/stable-runtime browser click-through for the v0.9 RiskMonitor notification controls before any public demo, then implement a mock-only crawl service bridge that can call the adapter factory for Reddit mock data without enabling live Reddit requests.

## 2. Completed MVP Steps

- Created backend FastAPI structure under `backend/app`.
- Created frontend React + Vite structure under `frontend/src`.
- Added Pydantic schemas for keyword, crawl, comment, analysis, visualization, propagation, recommendation, summary, and alerts.
- Added mock JSON data under `mock_data`.
- Added mock FastAPI routes for the MVP API contract.
- Added `GET /api/v1/platforms` to expose platform source planning and active MVP platform choices.
- Added desktop browser dashboard pages:
  - Dashboard
  - KeywordSearch
  - AnalysisResult
  - PropagationGraph
  - RiskMonitor
  - SummaryReport
- Connected frontend API client to backend mock endpoints.
- Updated frontend platform selection to use backend registry data, show grouped platform roadmap sections, and enable only mock-selectable platforms.
- Added `selectable_for_mock` to platform registry responses so mock selection is separate from future real adapter or official API planning status.
- Added dark sci-fi desktop dashboard styling with Ant Design, ECharts, Framer Motion, Axios, and lucide icons.
- Prioritized a 1440px desktop browser layout with left sidebar, top status bar, and chart-heavy dashboard panels.
- Added Windows local development instructions to `README.md`.
- Updated frontend install instructions/scripts to run `npm install` from inside `frontend`, avoiding accidental parent-package linking from `npm --prefix frontend install`.
- Confirmed `.gitignore` excludes `.env`, `.venv/`, `node_modules/`, `dist/`, `build/`, `__pycache__/`, and `.pytest_cache/`; `.venv` and `.pytest_cache` are not tracked by Git.
- Added `docs/platform_sources.md` with official API planned platforms, crawler-later platforms, disabled/optional future platforms, and the future crawler maintenance rule.
- Added `.python-version` with Python 3.10.
- Added `pytest.ini`.
- Added `GET /api/v1/health`.
- Added GitHub Actions CI for backend tests and frontend build.
- Created `docs/progress.md` as the project handoff and progress log.
- Added an `AGENTS.md` rule requiring `docs/progress.md` updates after each major Codex task.
- Confirmed frontend production build works locally with `npm.cmd --prefix frontend run build`.
- Validated the current local development environment with Python 3.10.6, Node 22.15.1, and npm 10.9.2.
- Implemented deterministic backend analysis service modules:
  - text cleaning with whitespace normalization, HTML tag removal, punctuation normalization, language detection, and safe empty-text handling
  - exact SHA-256 fingerprint duplicate detection plus similarity-based grouping
  - author-level aggregation with comment counts, duplicate ratio, weighted sentiment, and time range
  - mock rule-based sentiment analysis
  - embedding-compatible keyword topic clustering
  - rule-based bot scoring using duplicate ratio, repeated scripts, posting frequency, synchronization, and sentiment uniformity
  - weighted risk scoring from sentiment, bot impact, propagation speed, controversy, and trend shift
  - visualization response building for the existing `/api/v1/visualization/data` contract
- Added `docs/algorithm_design.md` with the system pipeline, V1 MVP static scoring design, V2 topic-cluster dynamic model, metric definitions, aggregation, visualization outputs, recommendation generation, and future LLM safety notes.
- Added `docs/risk_model_roadmap.md` documenting that V1 is current MVP and V2 requires time-window data, topic history, influence graphs, and credibility modeling before implementation.
- Added next-stage product planning documents:
  - `docs/product_requirements.md`
  - `docs/feature_matrix.md`
  - `docs/ux_flow.md`
  - `docs/implementation_backlog.md`
- Documented `v1_5_topic_risk_mvp` as the next practical algorithm upgrade path.
- Implemented `v1_5_topic_risk_mvp` as a deterministic offline topic-level risk scoring layer for the mock pipeline.
- Added topic-level risk schema fields for `topic_risks`, `top_risk_topics`, `max_topic_risk`, `average_topic_risk`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.
- Updated backend visualization and report responses to include V1.5 topic risk fields while keeping existing `risk_score` and `risk_level` fields.
- Updated backend analysis responses to include the same additive V1.5 topic risk fields while keeping the legacy nested `risk` object.
- Connected V1.5 topic-level risk fields to the frontend dashboard/report pages:
  - Dashboard displays risk model version and top 3 high-risk topics.
  - AnalysisResult displays topic risk cards with topic risk score, topic risk level, and risk explanation.
  - RiskMonitor displays real-crisis risk, manipulation risk, and top risk drivers.
  - SummaryReport/PublicOpinionReport displays top risk topics and their explanations.
- Added the backend risk model version constant `RISK_MODEL_VERSION = "v1_static_mvp"` without changing the active scoring calculation.
- Added `risk_model_version` to backend visualization/report responses and `risk_level_label` to normalized report responses without changing active scoring behavior.
- Added a safe documented V2 placeholder module for topic-cluster dynamic risk; it returns inactive/empty deterministic output.
- Added `docs/demo_checklist.md` as the step-by-step local MVP demo checklist.
- Added lightweight case-based mock MVP flow:
  - `GET /api/v1/cases`
  - `POST /api/v1/cases`
  - `GET /api/v1/cases/{case_id}`
  - `POST /api/v1/cases/{case_id}/run`
  - `GET /api/v1/cases/{case_id}/report/markdown`
- Added a frontend Cases page and connected Keyword Search to create and run mock analysis cases.
- Added Markdown report copy/download from Summary Report for completed cases.
- Added `backend/app/services/mock_pipeline.py` to run the offline mock pipeline end to end from `mock_data/raw_comments.json`.
- Updated analysis, visualization, and propagation mock service methods to use pipeline-generated outputs where available.
- Added safe platform adapter foundation modules for future real-data work:
  - `backend/app/services/crawling/base_adapter.py`
  - `backend/app/services/crawling/adapter_factory.py`
  - `backend/app/services/crawling/reddit_adapter.py`
- Added a Reddit adapter scaffold with default mock fallback, optional credential-gated real mode, rate-limit/retry placeholders, and schema normalization into `RawPost` and `RawComment`.
- Added `backend/app/services/recommendation/report_builder.py` for deterministic template-based public opinion reports.
- Updated `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate` to use the report builder while preserving their existing response schemas.
- Added `backend/app/schemas/report.py` as the normalized public opinion report schema.
- Normalized summary/recommendation report API output and added deterministic `zh-CN` report templates with optional `en-US`.
- Strengthened report builder tests to assert the structured internal report fields and validate summary/recommendation endpoint outputs against Pydantic response schemas.
- Strengthened report builder logic for high bot impact so suspected bot signals explicitly describe repeated-script or suspicious coordination signals.
- Added report builder tests for high-risk urgent recommendations, sentiment trend/propagation graph usage, endpoint schema compatibility, deterministic output, and missing optional pipeline outputs.
- Added backend platform registry tests covering category membership, active MVP platforms, and the `/api/v1/platforms` endpoint.
- Improved the desktop frontend analysis/report experience:
  - Analysis Result now has clearer risk, sentiment, topic, bot, and conflict sections.
  - Analysis Result now also shows report-builder insights, backend report API source tags, top negative topics, and a copyable suggested response template.
  - Analysis Result and Summary Report now request `zh-CN` report output and display Chinese report labels by default.
  - Summary Report now renders the normalized Chinese report sections: 舆情总览, 核心发现, 主要风险因素, 高风险话题, 代表性评论, 疑似水军/重复话术信号, 建议行动, and 建议公开回应文案.
  - Analysis Result now renders report-related topic risks, sentiment explanation, bot/repeated-script explanation, representative comments, and a copyable suggested public response.
  - Risk Monitor now emphasizes risk level, negative sentiment trend, bot impact, radar factors, heatmap, and alert tiles.
  - Propagation Graph now includes small-data-friendly key node summaries beside the graph.
  - Summary Report now includes an export-friendly Public Opinion Report section built from existing summary and recommendation APIs, with loading, empty, and error states.
- Improved Dashboard, RiskMonitor, and PropagationGraph for MVP visualization refinement:
  - Dashboard displays pipeline-backed risk score, risk level, sentiment trend, risk radar, topic clusters, bot impact, platform heatmap, platform distribution, and latest public opinion summary.
  - RiskMonitor displays risk trend, risk factor explanations, warning status, trend shift, propagation speed, controversy indicators, and current risk model version fallback.
  - PropagationGraph displays backend graph nodes/edges, graph metrics, central node detail, platform/type breakdowns, and readable edge details.
  - ECharts components were hardened for empty arrays and small mock datasets.
- Added module-level pytest coverage for preprocessing, NLP, bot scoring, risk scoring, visualization response structure, mock API contracts, and report generation.

## 3. Important Files and Modules

Backend:

- `backend/app/main.py` - FastAPI app factory and root health route.
- `backend/app/api/v1/api.py` - API router registration.
- `backend/app/api/v1/routes/` - Route handlers for health, keyword expansion, crawl, analysis, visualization, summary, recommendation, propagation, and alerts.
- `backend/app/api/v1/routes/platforms.py` - Route handler for the platform registry endpoint.
- `backend/app/api/v1/routes/cases.py` - Case management and Markdown export route handlers.
- `backend/app/schemas/` - Pydantic request and response schemas.
- `backend/app/schemas/case.py` - Lightweight analysis case and Markdown export schemas.
- `backend/app/schemas/report.py` - Normalized public opinion report schema and report language enum.
- `backend/app/schemas/platform.py` - Platform registry response schemas.
- `backend/app/services/mock_service.py` - Mock API response service now backed by the deterministic mock pipeline/report builder where possible.
- `backend/app/services/case_store.py` - Case management facade that runs the offline mock pipeline and exports Markdown reports.
- `backend/app/repositories/case_repository.py` - Repository layer for case IDs, timestamps, list/detail mapping, and persisted report attachments.
- `backend/app/services/storage/base_store.py` - Storage interface for current local JSON and future MongoDB/Redis implementations.
- `backend/app/services/storage/local_json_store.py` - Default project-local JSON case store at `backend/data/cases.json`.
- `backend/data/.gitkeep` - Keeps the runtime data directory present while generated `*.json` files remain ignored.
- `backend/app/services/crawling/base_adapter.py` - Shared adapter interface and safe utility helpers for future public platform adapters.
- `backend/app/services/crawling/adapter_factory.py` - Adapter registry/factory; currently registers the Reddit scaffold.
- `backend/app/services/crawling/platform_registry.py` - Platform source registry defining mock-selectable MVP, official API planned, future real adapter candidate, crawler-later, and optional future platforms.
- `backend/app/services/crawling/reddit_adapter.py` - Reddit adapter scaffold with mock fallback and optional credential-gated official API client path.
- `backend/app/services/mock_pipeline.py` - Offline mock pipeline that loads raw comments, runs analysis services, builds propagation, risk, and visualization inputs.
- `backend/app/services/preprocessing/text_cleaner.py` - Rule-based text normalization, language detection, and duplicate fingerprinting.
- `backend/app/services/preprocessing/duplicate_detector.py` - Exact hash and similarity duplicate grouping while preserving author-level clean comments.
- `backend/app/services/preprocessing/user_aggregator.py` - User-level aggregation with duplicate ratio, weighted sentiment, and time range.
- `backend/app/services/nlp/sentiment_analyzer.py` - Mock-mode rule-based sentiment analyzer.
- `backend/app/services/nlp/topic_clusterer.py` - Simple embedding-compatible keyword topic clusterer.
- `backend/app/services/bot_detection/bot_score_service.py` - Rule-based bot probability and impact scoring.
- `backend/app/services/scoring/risk_score.py` - Weighted risk score and factor calculation with `RISK_MODEL_VERSION = "v1_static_mvp"`.
- `backend/app/services/scoring/topic_risk_score.py` - Deterministic V1.5 topic-level risk scoring with `TOPIC_RISK_MODEL_VERSION = "v1_5_topic_risk_mvp"`.
- `backend/app/services/scoring/topic_dynamic_risk.py` - Future V2 topic-cluster dynamic risk placeholder; not active in scoring.
- `backend/app/services/visualization/chart_data_builder.py` - Analysis-to-visualization response transformer and MongoDB-safe key helper.
- `backend/app/services/recommendation/report_builder.py` - Template-based public opinion report builder with no external LLM dependency.
- `backend/app/tests/test_api_contract.py` - API contract tests.
- `backend/app/tests/test_preprocessing_services.py` - Tests for text cleaner, duplicate detector, and user aggregator.
- `backend/app/tests/test_nlp_and_bot_services.py` - Tests for sentiment, topic clustering, and bot scoring.
- `backend/app/tests/test_scoring_and_visualization_services.py` - Tests for risk scoring, visualization builder, and MongoDB-safe key conversion.
- `backend/app/tests/test_topic_risk_score.py` - Tests for V1.5 topic risk range, level mapping, missing-input fallbacks, aggregation, and report integration.
- `backend/app/tests/test_report_builder.py` - Tests for deterministic offline report generation and summary/recommendation endpoints.
- `backend/app/tests/test_cases.py` - Tests for case creation, listing, running, detail retrieval, Markdown export, and old endpoint compatibility.
- `backend/app/tests/test_platform_registry.py` - Tests for platform registry categories and endpoint contract.
- `backend/app/tests/test_reddit_adapter.py` - Tests for Reddit adapter mock fallback, mocked response normalization, optional real-mode client injection, and adapter factory registration.
- `backend/requirements.txt` - Backend dependencies.

Frontend:

- `frontend/src/App.jsx` - Main app state, data loading, page switching, and API orchestration.
- `frontend/src/api/` - Axios client and Sentigraph API functions, including platform registry loading and default `zh-CN` report requests.
- `frontend/src/components/layout/AppShell.jsx` - Desktop app shell with sidebar and top bar.
- `frontend/src/components/charts/` - ECharts chart components.
- `frontend/src/components/report/PublicOpinionReport.jsx` - Export-friendly Chinese public opinion report renderer using normalized summary/recommendation fields.
- `frontend/src/pages/` - Dashboard and feature pages.
- `frontend/src/pages/Cases.jsx` - Lightweight case list and case action page.
- `frontend/src/styles/global.css` - Desktop dashboard styling.
- `frontend/src/utils/reportModel.js` - Frontend report model mapper for summary, recommendation, analysis, visualization, optional risk model metadata, and topic risk fallbacks.
- `frontend/src/utils/clipboard.js` - Shared browser clipboard helper for copying suggested response text.
- `frontend/package.json` - Frontend scripts and dependencies.
- `frontend/package-lock.json` - Frontend dependency lock file.

Project and docs:

- `README.md` - Setup, run instructions, constraints, and endpoint list.
- `AGENTS.md` - Development instructions, safety constraints, and the rule to update `docs/progress.md` after each major Codex task.
- `package.json` - Root helper scripts for backend and frontend local tasks.
- `docs/architecture.md` - System architecture.
- `docs/data_schema.md` - Core data schema.
- `docs/api_contract.md` - API contract.
- `docs/development_plan.md` - MVP roadmap.
- `docs/algorithm_design.md` - Risk algorithm design covering V1 and planned V2.
- `docs/risk_model_roadmap.md` - Risk model versioning, V1.5 bridge plan, and V2 readiness roadmap.
- `docs/product_requirements.md` - Next-stage product requirements and target MVP experience.
- `docs/feature_matrix.md` - Completed, polish, next implementation, real-data, and advanced algorithm feature matrix.
- `docs/ux_flow.md` - Desktop-first UX flow for analysis, report reading, risk monitoring, propagation, and local demo.
- `docs/implementation_backlog.md` - Prioritized backlog for demo stabilization, V1.5 topic risk, product polish, real-data preparation, and V2 readiness.
- `docs/platform_sources.md` - Platform source roadmap and safety constraints.
- `docs/demo_checklist.md` - Local demo checklist for backend/frontend startup, mock analysis flow, report copy action, risk monitor, and propagation graph checks.
- `docs/progress.md` - Current progress log.
- `.github/workflows/ci.yml` - CI workflow.
- `.python-version` - Python version marker.
- `pytest.ini` - Pytest configuration.

## 4. Windows Local Run Instructions

Run these commands from the repository root.

Backend setup:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

Run backend tests:

```powershell
python -m pytest
```

Run only report builder/API tests:

```powershell
python -m pytest backend\app\tests\test_report_builder.py backend\app\tests\test_api_contract.py
```

Start backend:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Health check:

```text
http://127.0.0.1:8000/api/v1/health
```

Frontend setup in another PowerShell terminal:

```powershell
Set-Location frontend
npm.cmd install
Set-Location ..
```

Start frontend:

```powershell
npm.cmd --prefix frontend run dev
```

Open the desktop dashboard:

```text
http://127.0.0.1:5173
```

Build frontend:

```powershell
npm.cmd --prefix frontend run build
```

## 5. Known Issues

- Backend dependency installation passes in the root `.venv` with Python 3.10.6.
- Backend tests pass locally in the root `.venv`: latest MVP stabilization validation `28 passed in 0.40s`.
- Latest backend validation after frontend V1.5 display work passed with `33 passed in 0.35s`.
- Latest backend validation after completing analysis-response V1.5 fields passed with `34 passed in 0.40s`.
- Latest backend validation after case management and Markdown export passed with `40 passed in 0.41s`.
- Latest backend validation after v0.3 stabilization QA passed with `40 passed in 0.43s`.
- Latest backend validation after platform adapter foundation and Reddit scaffold passed with `44 passed in 0.42s`.
- Latest backend validation after Reddit adapter contract refinement passed with `46 passed in 0.50s`.
- Latest backend validation after platform adapter QA passed with `47 passed in 0.43s`.
- Latest backend validation after the long maintenance pass passed with `47 passed in 0.42s`.
- Latest targeted Reddit adapter validation after minimal real-mode helper updates passed with `9 passed in 0.14s`.
- Latest backend validation after Reddit real-mode hardening passed with `51 passed in 0.43s`; targeted Reddit adapter validation passed with `11 passed in 0.12s`.
- Latest v0.5 Reddit real-mode QA passed with full backend validation `51 passed in 0.41s`, targeted Reddit adapter validation `11 passed in 0.09s`, and API smoke checks for old MVP and case/report endpoints.
- Latest Reddit API approval status update passed with full backend validation `111 passed in 2.63s`; real Reddit API mode is disabled while `api_pending`, and `/crawl/start` continues to return mock Reddit data.
- Latest data-source readiness layer validation passed with full backend validation `114 passed in 2.56s`; frontend build passed in 7.65s with the existing non-blocking vendor chunk warning.
- Latest backend validation after local JSON case persistence passed with `54 passed in 0.53s`.
- Latest backend validation after v0.6 persistence QA passed with `55 passed in 0.51s`.
- Latest backend validation after v0.7 monitoring foundation passed with `65 passed in 1.04s`.
- Latest backend validation after v0.7 monitoring QA passed with `68 passed in 1.05s`.
- Latest backend validation after v0.8 scheduler QA passed with `81 passed in 1.76s`.
- Latest backend validation after v0.9 notification foundation passed with `90 passed in 2.29s`.
- Latest backend validation after v0.9 notification QA stabilization passed with `90 passed in 2.34s`.
- Frontend dependency installation passes with `npm.cmd run frontend:install`, which runs `cd frontend && npm install`; the latest install completed with dependencies already up to date.
- Avoid using `npm.cmd --prefix frontend install` for installation on npm 10.9.2; it can incorrectly link the parent package into `frontend` as `sentigraph: file:..`.
- Frontend production build passes with `npm.cmd run build` from `frontend`; the latest MVP stabilization Vite build completed in 7.73s.
- Latest frontend validation after V1.5 display work passed with `npm.cmd run build`. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after case management and Markdown export passed with `npm.cmd run build` in 7.55s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.3 stabilization QA passed with `npm.cmd run build` in 7.71s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after the long maintenance pass passed with `npm.cmd run build` in 7.68s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.7 monitoring foundation passed with `npm run build` in 7.54s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.7 monitoring QA passed with `npm run build` in 7.45s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.8 scheduler QA passed with `npm run build` in 7.46s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.9 notification foundation passed with `npm run build` in 7.76s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.9 notification QA stabilization passed with `npm run build` in 7.61s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Frontend build was not rerun for the platform adapter scaffold because no frontend files changed.
- No blocking environment, dependency, import, path, or test issue was found in the latest MVP stabilization pass.
- README validation passed after the README update: all README-listed API endpoints exist in FastAPI, the Windows run commands are still valid, and no README command correction was needed.
- API smoke validation passed: summary/recommendation return normalized Chinese `zh-CN` report fields, and `GET /api/v1/platforms` returns the full 17-platform registry.
- Visualization API smoke validation passed: `POST /api/v1/visualization/data` returns risk, sentiment, radar, heatmap, topic, bot, propagation graph fields, and `risk_model_version="v1_static_mvp"`; propagation data contains 6 nodes, 3 edges, and metrics for breadth, central node, depth, and propagation speed.
- Summary Report displays normalized Chinese report sections and report metadata. The backend now returns `risk_model_version` and `risk_level_label`, so the frontend no longer needs those fields only as fallbacks.
- A stale `backend\.venv` directory exists and points to an older missing Python path. Use the repository-root `.venv` instead.
- `git diff --check` only reports CRLF normalization warnings for touched files; no whitespace errors were reported.
- Vite still reports a large chunk warning for Ant Design and ECharts vendor chunks. Safe manual chunking reduced the app chunk from roughly 2.4 MB to roughly 226 KB, but deeper lazy loading would require a broader frontend refactor and should be handled separately.
- The latest `npm install` emitted an npm audit endpoint retirement notice. Previous audit output reported 2 moderate vulnerabilities; they were not force-fixed because `npm audit fix --force` may introduce breaking dependency changes.
- Rendered browser QA passed through a local Playwright + Chrome fallback at 1440x900 in an earlier pass. The in-app Browser runtime timed out again during the v0.7 monitoring QA pass, so future Codex browser sessions may need manual verification or a stable local browser fallback until that runtime is stable.
- Case-flow browser QA passed through local Playwright + Chrome: create case, run mock analysis, open the Cases page, open Summary Report, copy Markdown, download `.md`, and navigate to AnalysisResult, RiskMonitor, and PropagationGraph with no console errors.
- v0.3 browser QA passed through temporary Playwright + Chromium tooling at 1440x960: create case, run mock analysis, verify platform roadmap, open report, copy suggested public response, copy Markdown, download `.md`, and navigate through Dashboard, Cases, AnalysisResult, RiskMonitor, and PropagationGraph with no relevant console errors.
- v0.3 API smoke validation passed for `GET /api/v1/cases`, `POST /api/v1/cases`, `GET /api/v1/cases/{case_id}`, `POST /api/v1/cases/{case_id}/run`, `GET /api/v1/cases/{case_id}/report/markdown`, `GET /api/v1/platforms`, `POST /api/v1/visualization/data`, `POST /api/v1/summary/generate`, `POST /api/v1/recommendation/generate`, and `GET /api/v1/analysis/{project_id}`.
- Case storage now uses the default local JSON store at `backend/data/cases.json`. Restarting the FastAPI server preserves local demo cases unless that runtime JSON file is deleted.
- Monitoring scheduler config, snapshots, and alert events are stored in the same default local JSON store at `backend/data/cases.json`. There is no real background scheduler; `POST /api/v1/scheduler/run-due` is the manual local MVP trigger.
- Notification outbox items are stored in the same default local JSON store at `backend/data/cases.json`. `simulate-send` and `mark-read` only update local notification state; no external notification channel is called.
- v0.9 notification QA smoke validation confirmed `simulate-send` sets both top-level `simulated_sent_at` and nested `notification.simulated_sent_at`, while `mark-read` sets `read_at`.
- If npm reports a stale dependency or `extraneous` error after earlier local installs, remove generated dependencies and install again:

```powershell
Remove-Item -Recurse -Force frontend\node_modules
Set-Location frontend
npm.cmd install
Set-Location ..
```

- The canonical Git repository root is the `Sentigraph` folder inside the workspace. Any sibling `backend`, `frontend`, or `mock_data` directories outside that folder should be ignored unless intentionally moved into the repository.
- Real crawlers, real OpenAI calls, Redis, Celery/APScheduler jobs, production MongoDB hardening, and real NLP/ML analysis are not implemented yet.
- The report builder is template-based and deterministic; it does not require `OPENAI_API_KEY`.
- Report builder handles missing optional visualization, propagation, risk-factor, and explicit representative-comment inputs without crashing.
- Summary and recommendation endpoints now return the normalized `PublicOpinionReport` fields directly while preserving backward-compatible fields for the current frontend.
- Report builder defaults to Chinese `zh-CN` template output and supports optional `en-US`; it remains deterministic and does not require `OPENAI_API_KEY`.
- Frontend report pages derive structured report sections from the normalized summary/recommendation API responses, explicitly request `zh-CN`, and preserve original-language representative comments.
- The previous frontend only showed Weibo because the backend registry had only `weibo` marked `enabled_in_mvp=true`, and `frontend/src/App.jsx` filtered platform options only by that field. This has been fixed by adding `selectable_for_mock` and marking Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao as safe mock-selectable platforms.
- Crawler-later platforms remain visible but disabled with the note `Future crawler integration`. YouTube is not active in the MVP and is marked as optional future.
- YouTube is not active in the MVP and is marked as optional future.
- Reddit adapter scaffold is available and defaults to mock mode; mock mode intentionally falls back to local mock data.
- Reddit real API mode is currently `api_pending` and disabled until Reddit approval is granted, even if `REDDIT_ADAPTER_MODE=real` and credentials are present.
- `POST /api/v1/crawl/start` now routes Reddit selections through `adapter_factory.get_adapter("reddit")`; default local demos still use `REDDIT_ADAPTER_MODE=mock`.
- While approval is pending, `crawl/start` returns normalized mock Reddit data with safe metadata: `mock_available=true`, `api_pending=true`, and `real_mode_disabled=true`.
- Public-page scraping for Reddit is not implemented and must not be used to bypass API approval.
- Before expanding Reddit real mode further, obtain/confirm Reddit API approval, keep tests fixture-first, and preserve safe mock fallback.
- The legacy V1 static scoring module remains for factor/radar compatibility; the current active mock pipeline/report risk model is `v1_5_topic_risk_mvp`.
- V1.5 topic-level risk (`v1_5_topic_risk_mvp`) is now implemented for mock pipeline visualization/report outputs.
- V1.5 topic-level risk (`v1_5_topic_risk_mvp`) is now implemented for mock pipeline analysis, visualization, summary, and recommendation outputs.
- V2 topic-cluster dynamic risk is planned but not implemented yet.
- `risk_model_version` is now active in stable visualization/report responses. V1.5 fields (`topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`) are implemented for mock responses. Future full V2 time-window fields remain documented but are not yet implemented.
- The actual normalized report APIs currently return `project_id`, `report_language`, `risk_score`, `risk_level`, `risk_level_label`, `risk_model_version`, `overall_summary`, `key_findings`, `main_risk_factors`, `top_negative_topics`, `representative_comments`, `suspected_bot_signals`, `recommended_actions`, `suggested_public_response`, `generated_from_mock_pipeline`, V1.5 topic-risk fields, and backward-compatible aliases.

## 6. MVP Roadmap Audit

Audit date: 2026-05-14.

| Item | Status | Evidence | Missing work / recommended action |
| --- | --- | --- | --- |
| Project skeleton | complete | `backend/app`, `frontend/src`, `docs`, `mock_data`, root `package.json`, and root `requirements.txt` are present. | Keep structure stable; add only needed modules per feature. |
| Desktop frontend layout | complete | `frontend/src/components/layout/AppShell.jsx`, `frontend/src/styles/global.css`, and pages under `frontend/src/pages`. | Browser visual QA at 1440px is still recommended. |
| Platform registry and `GET /api/v1/platforms` | complete | `backend/app/services/crawling/platform_registry.py`, `backend/app/api/v1/routes/platforms.py`, `backend/app/tests/test_platform_registry.py`; smoke check returned 17 platforms and 9 active MVP mock-selectable platforms. | Real adapter interfaces are future work; keep crawler-later platforms disabled. |
| Mock analysis pipeline | complete for MVP | `backend/app/services/mock_pipeline.py`, `backend/app/services/mock_service.py`, preprocessing/NLP/bot/risk services, and service tests. | No real crawlers, persistence, or advanced ML yet. |
| Visualization API | complete for MVP | `POST /api/v1/visualization/data` route and `backend/app/services/visualization/chart_data_builder.py`; smoke check returned risk, sentiment, radar, heatmap, topic, bot, graph fields, and `risk_model_version`. | Future V2 fields remain out of scope. |
| Report builder | complete for MVP | `backend/app/services/recommendation/report_builder.py` and `backend/app/tests/test_report_builder.py`. | Future LLM mode remains unimplemented by design. |
| Chinese normalized report API | complete for MVP | `backend/app/schemas/report.py`, `backend/app/schemas/summary.py`, `backend/app/schemas/recommendation.py`; smoke check confirmed `report_language="zh-CN"`, `risk_level_label`, `risk_model_version`, and normalized report fields. | Future V2 report fields remain out of scope. |
| SummaryReport frontend page | complete for MVP | `frontend/src/pages/SummaryReport.jsx`, `frontend/src/components/report/PublicOpinionReport.jsx`, and `frontend/src/utils/reportModel.js`; browser QA confirmed the suggested response copy button works. | Later add print/PDF export polish. |
| AnalysisResult frontend page | complete for MVP | `frontend/src/pages/AnalysisResult.jsx` renders analysis plus report insights, V1.5 topic-risk labels, and a copyable suggested response. | Later add deeper topic drill-down interactions. |
| Dashboard visualization | complete for MVP | `frontend/src/pages/Dashboard.jsx` and chart components consume backend visualization data. | Browser visual QA and later code splitting for large chart bundle. |
| RiskMonitor page | complete for v0.9 foundation | `frontend/src/pages/RiskMonitor.jsx` renders monitoring status, risk delta, snapshot timeline, alert events, notification center, risk drivers, radar factors, V1.5 signals, and scheduler config controls; API smoke confirmed alert-generated notifications, outbox status, simulate-send-pending, and mark-read. | Interactive browser automation timed out in the latest QA pass, so manually click the scheduler and notification controls before a live demo; real background scheduler and external notification delivery remain future work. |
| PropagationGraph page | complete for MVP | `frontend/src/pages/PropagationGraph.jsx` and `PropagationGraphChart.jsx`; smoke check returned 6 nodes and 3 edges. | Real graph metrics and NetworkX-backed propagation builder are future work. |
| README accuracy | complete with minor caveat | README endpoints match routes in `backend/app/api/v1/api.py`; Windows commands are consistent with root `requirements.txt` and scripts. | Keep README updated after schema changes; production-readiness is correctly not claimed. |
| Algorithm docs | complete for V1.5 | `docs/algorithm_design.md` and `docs/risk_model_roadmap.md` document V1 active, V1.5 implemented as a practical topic-risk bridge, and V2 planned for later. | Frontend should surface V1.5 topic-risk explanations more directly; do not start full V2 yet. |
| Backend tests | complete | `python -m pytest` passed with `81 passed in 1.76s`. | Add tests as new features land. |
| Frontend build | complete | `npm run build` in `frontend` passed in 7.46s. | Vite large chunk warning remains for Ant Design and ECharts vendor chunks; the app chunk is now smaller after safe manual chunking. |

Overall audit conclusion: MVP 0 through the v0.9 notification foundation are complete enough for the mock-first desktop prototype. The project should not move to real crawlers or broad real platform APIs yet. Browser QA should cover the scheduler and notification controls before a public demo.

## 6.1 Crawl Adapter Bridge Update

Update date: 2026-05-15.

Status: complete for the safe Reddit bridge.

What changed:

- `POST /api/v1/crawl/start` now uses the platform adapter layer when `platforms` contains `reddit`.
- Reddit mock mode returns normalized `RawPost` and `RawComment` items and adapter metadata.
- Reddit real API mode is disabled while API approval is pending and falls back to mock data with `api_pending` metadata.
- Safe response metadata includes `platform`, `adapter_mode`, `fallback_used`, `fallback_reason_category`, `mock_available`, `api_pending`, `real_mode_disabled`, post/comment counts, and schema validation booleans.
- Official API planned platforms still use mock behavior. Crawler-later platforms are not activated.

Validation:

- Backend tests passed: `111 passed in 4.44s`.
- No frontend code changed, so frontend build was not required for this task.

Known limitations:

- `crawl/start` does not expose a detailed real Reddit error message by design; only safe category-level fallback metadata is returned.
- Non-Reddit platforms still use the previous mock-first behavior and do not have adapter output yet.
- Case runs still use the deterministic mock pipeline rather than live crawl results.

## 7. Next Recommended Task

Recommended next platform parser task: expand fixture coverage for The Paper, Jiemian, Hupu, Maimai, Tieba, and NGA with additional sanitized article/thread/post variants, then add a small parser QA matrix for selector drift and missing metadata. Keep live fetch disabled by default, keep crawler-later platforms non-selectable for real collection, and require fixture tests plus compliance notes before any parser is promoted beyond scaffold status.

Suggested scope:

- Do not enable V2 scoring yet.
- Do not replace V1/V1.5 with full V2 during the next task.
- Keep the current mock pipeline and V1.5 report APIs stable.
- If alert refinement continues next, keep it manual/mock-only. Notification delivery must remain local simulation only until explicit external-channel configuration and tests are added.
- If Reddit integration is selected next, keep real API mode disabled until approval is granted and use sanitized fixtures or mocked clients only.
- If public parser work continues, do not implement login bypass, captcha bypass, proxy rotation, cookies, private data scraping, or Reddit scraping.
- Re-run the browser checklist in `docs/demo_checklist.md` after the next product-polish task.
- Keep existing API schemas stable.
