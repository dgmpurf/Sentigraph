# Sentigraph Implementation Backlog

Last updated: 2026-05-19

This backlog prioritizes practical next work while keeping the MVP mock-first and offline.

CI note: GitHub Actions CI is intentionally disabled. Do not restore or recreate `.github/workflows/ci.yml` unless explicitly requested. Use local/Codex validation commands such as `python -m pytest` and `npm run build`; future CI can be reconsidered only if cost and notification concerns are resolved.

## Completed Pre-v1.0 Hardening Items

### Real Data Source Readiness Framework

Status: implemented, QA complete, and locally validated on 2026-05-19.

Completed:

- Added normalized readiness fields to platform source metadata: `integration_type`, `required_credentials`, `required_scopes`, `scope_status`, `oauth_required`, `oauth_status`, `real_mode_configured`, `credential_present`, `data_access_level`, `next_user_action`, and `quota_cache_protected`.
- Added `GET /api/v1/platforms/readiness` while preserving `GET /api/v1/platforms/status` as a compatible alias.
- Applied readiness semantics to YouTube, Douyin, Xiaohongshu, Reddit, Bilibili, Weibo, Kuaishou, Zhihu, Douban, Toutiao, and public-parser/future sources.
- YouTube is real-capable but real-selectable only when both `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY` are locally configured; cache/quota guardrails remain visible.
- Douyin is grouped as OAuth pending with Web App developer access obtained, `user_info` and `item.comment` as required scopes, and OAuth/scope/item-id verification still blocking real mode.
- Weibo records `company_age_requirement_pending`; Reddit/Bilibili record `approval_pending`; Xiaohongshu records `comment_api_unknown_or_not_confirmed`.
- Platform Integration Overview now groups sources into Real Ready, Configured but Guarded, Permission Pending, OAuth Pending, and Mock / Scaffold Only.

Acceptance:

- Backend tests passed with `python -m pytest` (`559 passed in 5.41s`).
- Offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`).
- Frontend build passed with `npm run build` from `frontend/` (`built in 7.82s`; existing non-blocking vendor chunk warning remains).
- No real YouTube or Douyin API calls in automated tests.
- No API keys, tokens, or `.env` values exposed; credential presence remains boolean only.
- GitHub Actions CI remains intentionally disabled.

QA stabilization:

- Added regression coverage for the complete readiness field set returned by `/api/v1/platforms/readiness`.
- Reconfirmed YouTube readiness as official API, public video/comment data, real-capable, credential-gated, and quota/cache protected.
- Reconfirmed Douyin readiness as Web App OAuth pending with `item.comment`, HTTPS `redirect_uri`, whitelist/test account, token flow, and lawful `item_id` source still requiring console verification.
- Reconfirmed Weibo `company_age_requirement_pending`, Reddit/Bilibili `approval_pending`, and Xiaohongshu `comment_api_unknown_or_not_confirmed` blockers.
- Reconfirmed no secret values are returned; required credential names and presence booleans remain safe display metadata.

Next options:

- Browser-smoke the Platform Integration Overview page against a running local backend/frontend.
- Continue Douyin console verification for Web App redirect URI, whitelist/test account, `item.comment`, token flow, and lawful `item_id` source.
- Add a future quota/status dashboard only if repeated real-data demos need operator-facing cache diagnostics.
- Keep other real platforms as future work behind official approvals, mocked fixtures, and redacted readiness metadata.

### Douyin Web App OAuth and item.comment Readiness Scaffold

Status: QA complete as a readiness/documentation scaffold on 2026-05-19.

Completed:

- Added `docs/douyin_web_app_integration_plan.md` with future Douyin Web App OAuth design, callback/token placeholder flow, `item.comment` readiness gates, planned schemas, and no-real-call safety requirements.
- Updated `.env.example` with `DOUYIN_REDIRECT_URI`, `DOUYIN_REFRESH_TOKEN`, `DOUYIN_CLIENT_TOKEN`, `DOUYIN_STABLE_CLIENT_TOKEN`, `DOUYIN_ENABLE_REAL_CALLS=false`, and `DOUYIN_SCOPE_STATUS=unverified` placeholders. Real values must stay in ignored local `.env` files or a future secret store.
- Added `docs/douyin_console_checklist.md` for Web App type, Client Key/Secret, HTTPS full-path redirect URI, preview whitelist/test account, `user_info`, `item.comment`, `video.list.bind`, `video.data.bind`, keyword-comment availability, authorized-account limits, app status, and daily quota checks.
- Added a non-network OAuth helper scaffold for authorization URL construction, redirect URI validation, callback parsing, and placeholder token exchange/refresh functions that raise no-network placeholder errors.
- Updated the Douyin adapter and platform registry to report safe readiness metadata: `developer_access_status="obtained"`, `app_type="web_app"`, `comment_api_status="item_comment_scope_not_verified"`, `recommended_comment_scope="item.comment"`, `video_comment_scope_status="not_recommended_for_mvp"`, `real_mode_blocker="oauth_and_scope_not_verified"`, `permission_status="permission_not_verified"`, `oauth_status="scaffold_documented_not_implemented"`, `token_exchange_status="placeholder_not_implemented"`, `item_id_source_status="not_confirmed"`, `scope_status="unverified"`, and `real_calls_enabled=false`.
- Kept Douyin real mode disabled. `DOUYIN_ADAPTER_MODE=real` still returns normalized mock data with safe `api_pending:permission_not_verified` when complete placeholder OAuth config is present or `config_error` when OAuth config is incomplete.
- Updated README, platform source docs, API contract, data schema, API application plan, real API capability audit, current status, and release-readiness notes for the new Douyin Web App gates.
- Added/updated tests for mock mode, missing OAuth config fallback, verified-scope blocker metadata, OAuth authorization URL safety, HTTPS redirect validation, token placeholder no-network behavior, no real network calls, registry metadata, `/crawl/start` metadata, `.env.example` placeholders, and credential redaction.

Acceptance:

- Focused Douyin OAuth/adapter/registry/crawl validation passed with `69 passed in 0.97s`.
- Full backend validation passed with `python -m pytest` (`556 passed in 5.13s`).
- Offline benchmarks passed with `python scripts/run_offline_benchmarks.py` (`522 passed, 0 failed, 0 warnings`, `no_regression`).
- Frontend build was not run because no frontend files changed.
- No real Douyin API call, scraping, browser-cookie use, login/captcha/anti-bot bypass, credential printing, `.env` modification, real LLM call, or GitHub Actions workflow was introduced.

Next options:

- Verify in the Douyin developer console that the app is a Web App and the redirect URI is configured.
- Verify `item.comment` or the current official equivalent scope approval.
- Keep `video.comment` out of the MVP path unless the console proves it is the correct Web App route.
- Verify `video.list.bind` and `video.data.bind` availability or pending status for lawful item-id discovery.
- Confirm preview whitelist / test account setup, app status, and current daily testing quota.
- Complete test-account OAuth authorization and confirm token exchange/refresh behavior.
- Confirm the lawful source of `item_id` values before any item-comment request.
- Keep Douyin token storage, quota/rate-limit guardrails, and item.comment minimal real mode as future tasks after console verification.
- Capture sanitized official payload fixtures before implementing real-mode code.

### v6.3 Screenshot / Recording Demo Package

Status: complete as a documentation/package checkpoint on 2026-05-19.

Completed:

- Added `docs/demo_recording_script.md` with a 3-minute short demo script, an 8-minute full demo script, exact page order, page-by-page talking points, what each screen proves, and presenter guardrails.
- Added `docs/demo_screenshot_checklist.md` with the canonical 13-screen capture sequence: Dashboard, Keyword Search, Cases, Analysis Result, Summary Report, Propagation Graph, Risk Monitor / Forecast, Simulation Lab initialized from case, Simulation Lab A/B comparison, strategy report export, Benchmark Dashboard, LLM Safety, and Platform Integration Overview.
- Updated `docs/demo_package.md` from the older mock/offline package into the v6.3 YouTube real-data screenshot/recording package, including local commands, YouTube caveats, current limitations, and real-vs-mock boundaries.
- Updated `README.md`, `docs/demo_story.md`, `docs/demo_checklist.md`, and `docs/progress.md` to point to the package docs and preserve the core demo framing.

Acceptance:

- `python -m pytest` passed with `544 passed in 6.00s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm --prefix frontend run build` passed in 8.05s with the existing non-blocking large vendor chunk warning.
- Documentation distinguishes real YouTube public video/comment data, offline deterministic analysis/risk/report/forecast/Simulation Lab, mock LLM provider, and mock/scaffold status for other platforms.
- Documentation does not claim all platforms are real, does not claim real LLM integration, does not imply guaranteed predictions, does not imply Simulation Lab or content moderation executes real-world actions, and does not imply individual targeting.
- Automated validation did not call the real YouTube API, print API keys, modify `.env`, scrape, call real LLM APIs, or recreate GitHub Actions CI.

Next options:

- Produce the actual screenshot set and short recording from the v6.3 package.
- Run a Douyin Web App permission audit.
- Improve YouTube comment quality/filter heuristics if recording review finds low-signal examples.
- Keep real LLM integration as later work behind explicit provider gates, guardrails, and offline benchmark regression checks.
- Add additional real platform APIs only after official permission and mocked regression coverage.
- Keep GitHub Actions CI intentionally disabled.

### YouTube Real Data Demo Story

Status: documented and locally validated as a manual demo path.

Completed:

- Added `docs/youtube_real_data_demo.md` with prerequisites, `.env` requirements, key-redaction warnings, backend/frontend startup commands, tiny YouTube crawl command, case-specific raw-data attachment command, case run command, Markdown export command, Risk Monitor/Forecast steps, Simulation Lab initialization steps, A/B strategy comparison steps, strategy report export steps, cache notes, screenshot checklist, and troubleshooting.
- Updated `docs/demo_story.md` to separate the default mock/offline demo from the optional YouTube real-data demo.
- Updated `docs/demo_checklist.md` with the current expected signs of success: `adapter_mode=real`, `fallback_used=false`, `credential_present=true`, schema-valid tiny counts, `raw_data_status=attached`, `analysis_input_source=case_raw_data`, YouTube-derived representative comments, and working strategy report export.
- Linked the manual walkthrough from `README.md`.

Acceptance:

- `python -m pytest` passed with `542 passed in 6.32s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm --prefix frontend run build` passed in 8.26s with the existing non-blocking large vendor chunk warning.
- Automated validation did not call the real YouTube API and did not require API credentials.
- No API key values or `.env` values were printed, committed, or documented.
- No scraping, browser-cookie use, login bypass, captcha bypass, anti-bot evasion, real LLM call, `.env` modification, new product feature, or GitHub Actions workflow was introduced.

Future work:

- Run the manual YouTube real-data demo with the locally configured key and capture screenshots/recording.
- Add a small guarded frontend affordance for case-specific crawl attachment only if repeated real-data demos need it.
- Keep other real-platform demos behind official permissions, mocked regression tests, and key-redacted metadata.
- Keep GitHub Actions CI intentionally disabled.

### YouTube Quota-Safe Cache and Real-Data Guardrails

Status: implemented and QA-stabilized for the credential-gated YouTube official API adapter; revalidated on 2026-05-19.

Completed:

- Added project-local YouTube cache support at `backend/data/youtube_cache.json`; runtime JSON cache files remain ignored by git and `backend/data/.gitkeep` is preserved.
- Added `.env.example` guardrail defaults: `YOUTUBE_CACHE_ENABLED`, `YOUTUBE_CACHE_TTL_SECONDS`, `YOUTUBE_MAX_SEARCH_RESULTS`, `YOUTUBE_MAX_COMMENTS_PER_VIDEO`, `YOUTUBE_MAX_REPLIES_PER_COMMENT`, `YOUTUBE_MAX_TOTAL_COMMENTS`, and `YOUTUBE_ENABLE_DEEP_REPLIES`.
- Added cache keys based only on safe query fields: keyword, video id, limit, order, and date range. API keys are not used in cache keys and are not stored in cache payloads.
- Added crawl metadata for cache/quota diagnostics: `estimated_quota_units`, `search_call_count`, `videos_call_count`, `comment_threads_call_count`, `comments_call_count`, `cache_hit`, `cache_age_seconds`, and `quota_guardrail_status`.
- Added guardrails for clamped limits, disabled deep replies by default, total-comment caps, comments-unavailable partial results, and quota-error fallback.
- Added mocked-only regression coverage for cache miss/hit/expiry, limit clamping, reply limiting, quota fallback, comments-disabled partial output, cache metadata, and API-key redaction.
- QA stabilization revalidated case raw-data ingestion compatibility so attached YouTube `RawPost` / `RawComment` data still drives `analysis_input_source=case_raw_data` while missing raw data safely falls back to mock data.

Acceptance:

- `python -m pytest` passed with `542 passed in 5.42s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- Frontend build was not run because no frontend files changed.
- `backend/data/youtube_cache.json` was absent after automated validation; `backend/data/.gitkeep` remains preserved.
- Automated tests use mocked YouTube clients only and do not call the real YouTube API.
- No API key values are printed, returned, or stored in cache payloads.
- `backend/data/youtube_cache.json` is ignored runtime data.
- No scraping, browser-cookie use, login bypass, captcha bypass, anti-bot evasion, real LLM call, `.env` modification, or GitHub Actions workflow was introduced.

Future work:

- Add a small operator-facing quota/cache status panel only if repeated real-data demos need it.
- Add deeper reply crawling through `comments.list` only behind explicit strict limits and mocked regression tests.
- Add durable quota usage reporting after real-data demo patterns are better understood.
- Keep GitHub Actions CI intentionally disabled.

### YouTube Official API Adapter Minimal Real Mode

Status: implemented and QA-stabilized as the first real-capable official API adapter, mock-first by default.

Completed:

- Added `backend/app/services/crawling/youtube_adapter.py` with deterministic mock mode and optional official YouTube Data API v3 real mode.
- Added official API concepts for tiny `search.list`, `videos.list`, and `commentThreads.list` usage behind `YOUTUBE_ADAPTER_MODE=real` plus local `YOUTUBE_API_KEY`.
- Wired `youtube` into `adapter_factory`, `platform_registry`, and `/api/v1/crawl/start`.
- Added safe crawl metadata including `credential_present` as a boolean only; no key values are returned or logged.
- Added `.env.example` placeholders for `YOUTUBE_ADAPTER_MODE=mock` and `YOUTUBE_API_KEY=`.
- Added tests for mock search/comments, normalization, missing-key fallback, mocked real API response normalization, adapter factory registration, `/crawl/start` mock and missing-key metadata behavior, UTF-8/emoji text handling, top-level/reply comment parent/default URL behavior, and mocked auth/network fallback behavior.
- Verified a local real-mode smoke check with `adapter_mode=real`, `fallback_used=false`, `credential_present=true`, `post_count=3`, `comment_count=3`, and valid normalized post/comment schema metadata.
- Verified the mocked-real `/crawl/start` output shape remains downstream-compatible with `RawPost` / `RawComment` consumers, with credential values redacted from response text and `raw_data`.
- Added explicit case raw-data ingestion so normalized YouTube/future crawl output can be attached to a case and used by the next case analysis run.

Acceptance:

- `python -m pytest` passed with `533 passed in 5.30s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm run build` passed from `frontend/` in 7.66s with the existing non-blocking large vendor chunk warning.
- Automated tests do not call the real YouTube API; real-mode test coverage uses mocked clients only.
- No scraping, API-key printing, `.env` modification, real LLM call, login bypass, captcha bypass, anti-bot evasion, or GitHub Actions workflow was introduced.

Future work:

- Keep any future YouTube real-mode validation manual, tiny-limit, quota-aware, and key-redacted.
- Add a small guarded frontend affordance or demo-flow card for `POST /api/v1/cases/{case_id}/crawl/start` if real-data demos become frequent.
- Douyin comment API permission verification remains future work.
- Xiaohongshu note/comment API permission verification remains future work.
- Reddit and Bilibili approval/permission work remains future work.
- Weibo company-age/application requirement remains future work.
- GitHub Actions CI remains intentionally disabled.

### Case Raw Data Ingestion for Real Crawl Outputs

Status: implemented and QA-stabilized for YouTube and future normalized `RawPost` / `RawComment` adapter outputs.

Completed:

- Extended case detail/storage schemas with `raw_posts`, `raw_comments`, `crawl_metadata`, `crawl_source_mode`, `crawl_attached_at`, `raw_data_status`, raw counts, and `analysis_input_source`.
- Added `POST /api/v1/cases/{case_id}/crawl/start` to explicitly crawl with the case keyword/platforms or safe overrides, attach normalized output to the case, and return safe counts/metadata.
- Refactored case analysis so attached raw comments use the deterministic local analysis pipeline; missing raw comments still fall back to the existing mock dataset.
- Representative report comments can now come from attached YouTube public comments.
- Simulation Lab case initialization can consume the resulting YouTube-based analysis through existing aggregate case outputs.
- Added regression coverage for old-case compatibility, raw-data persistence, case-specific crawl attachment, raw-data analysis source metadata, report representative comments, fallback behavior, and Simulation Lab initialization.
- QA stabilization added local JSON reload coverage, MongoDB-shaped persistence coverage through the fake store, Markdown provenance checks that keep YouTube-derived comments and exclude old mock comments when raw case comments exist, and a guard against raw-data JSON dumps in user-facing Markdown.
- Full-demo QA added mocked-real fallback coverage for YouTube comments-disabled/quota/auth-style failures and network failures, and documented the end-to-end manual path from YouTube crawl attachment through case analysis, report export, monitoring/forecasting, Simulation Lab initialization, A/B simulation, and strategy report export.

Acceptance:

- `python -m pytest` passed with `533 passed in 5.30s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm run build` passed from `frontend/` in 7.66s with the existing non-blocking large vendor chunk warning.
- Automated tests use mocked crawl output only and do not call the real YouTube API.
- No scraping, API-key printing, `.env` modification, real LLM call, login bypass, captcha bypass, anti-bot evasion, or GitHub Actions workflow was introduced.

Future work:

- Capture manual YouTube real-data demo screenshots from the documented case-ingestion path.
- Extend quota-aware search strategy only if real-data demos need broader query controls.
- Add deeper reply crawling through `comments.list` with strict per-video limits only if the demo needs more reply coverage.
- Add an optional frontend button for case-specific crawl attachment.
- Keep other platform real-mode ingestion behind official permissions, mocked regression tests, and key-redacted metadata.
- GitHub Actions CI remains intentionally disabled.

### v5.6 Demo Package and Release Readiness

Status: complete as a documentation/package checkpoint on 2026-05-18.

Completed:

- Updated `README.md` with a top-level v5.6 demo-ready snapshot covering product purpose, demo scope, mock/offline boundaries, future API approvals, local run commands, validation commands, and intentionally disabled GitHub Actions CI.
- Added `docs/demo_package.md` for the demo story, recommended screenshot sequence, exact Windows run commands, talking points, screen proof notes, known limitations, and safety/ethics boundaries.
- Added `docs/release_readiness.md` for completed capabilities, demo-ready features, mock/scaffold-only features, real API pending features, real LLM pending features, non-blocking issues, validation expectations, and next-stage options.
- Updated `docs/progress.md` with the v5.6 packaging status and next recommended task.
- Rechecked wording so docs do not claim real platform API integration, real LLM integration, active live fetching, guaranteed predictions, or Simulation Lab real-world action execution.

Acceptance:

- `python -m pytest` passed with `511 passed in 5.25s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm run build` passed from `frontend/` in 7.93s with the existing non-blocking Ant Design/ECharts large vendor chunk warning.
- `python scripts/api_smoke_check.py --base-url http://127.0.0.1:8000` passed against the already-running local backend with `38 passed, 0 failed`.
- `.github/workflows/ci.yml` remains absent; GitHub Actions CI remains intentionally disabled.
- No real APIs, real LLM APIs, live public fetch, real crawler, authentication, new adapter/parser, or `.env` modification was introduced.

Next options:

- Produce the final screenshot deck or short demo recording from the current demo story.
- Audit Douyin and Xiaohongshu API permissions in their developer consoles.
- Implement real Douyin minimal mode only after Web App OAuth, `item.comment`, token flow, lawful `item_id` source, and official payload shape are confirmed.
- Add a policy/legal review checklist for Simulation Lab strategy reports.
- Keep real LLM integration as later work behind provider gates, guardrails, and offline benchmark regression checks.
- Keep Simulation Lab empirical calibration as later work after real data governance is settled.
- Keep GitHub Actions CI intentionally disabled unless explicitly requested.

### v5.4 Demo Polish and One-Click Demo Flow

Status: implemented and locally validated on 2026-05-18.

Completed:

- Added `Demo Flow / 演示流程` sidebar navigation and a desktop-first guided page for the local end-to-end demo.
- Added a one-click frontend demo-prep action that creates or loads the deterministic Tesla mock case, runs offline mock analysis, prepares monitoring snapshots, enables local schedule metadata, and computes deterministic forecasting through existing local APIs.
- Added cards for the demo story: create/load case, run mock analysis, inspect V1.5 risk, view Chinese report, export Markdown, initialize Simulation Lab, run A/B strategy comparison, export Simulation Lab strategy report, and verify Benchmarks plus LLM Safety.
- Updated `scripts/seed_demo_cases.py` so seed output verifies forecast readiness and case-to-simulation initialization readiness.
- Extended `scripts/api_smoke_check.py` to cover forecast endpoints, Simulation Lab demo scenario, Simulation Lab run, Simulation Lab strategy report export, latest benchmark summary, and LLM status/usage.
- Updated demo documentation with exact Windows reset, seed, benchmark, backend, frontend, smoke, and page walkthrough steps.

Acceptance:

- `python -m pytest` passed with `511 passed in 4.88s`.
- `python scripts/run_offline_benchmarks.py` passed with `522 passed, 0 failed, 0 warnings` and `no_regression`.
- `npm run build` passed from `frontend/` in 8.06s with the existing non-blocking Ant Design/ECharts large vendor chunk warning.
- `python scripts/api_smoke_check.py --base-url http://127.0.0.1:8010` passed against a temporary local backend with `38 passed, 0 failed`.
- No real API, real LLM API, live public fetch, real crawler, real notification, fake consensus, bot amplification, fake event, deceptive diversion, covert seeding, individual targeting, or account-level influenceability path was introduced.

Future work:

- Production onboarding remains future work.
- Final screenshot deck or recording production remains future work; the browser smoke story and local screenshot targets are documented.
- Real API integrations remain future work and require official permission verification.
- Real LLM integrations remain future work behind explicit provider gates and guardrails.
- GitHub Actions CI remains intentionally disabled.

### Simulation Lab MVP Backend and Frontend Scaffold

Status: backend implemented and QA-stabilized; frontend bubble visualization implemented and QA-stabilized; A/B intervention comparison implemented and QA-stabilized on 2026-05-18. Content visibility intervention backlash modeling is implemented and QA-stabilized on 2026-05-18. Event Frame and Audience Initialization design is documentation-complete and QA-stabilized on 2026-05-18.

Completed:

- Added a deterministic offline Simulation Lab backend scaffold under `backend/app/services/simulation/`.
- Added synthetic aggregate scenarios for echo-chamber discussion, brand crisis response, and misinformation correction.
- Added ethics-bounded intervention validation with allowed transparent responses only.
- Added hard rejection for fake consensus, bot amplification, fake events, deceptive distraction, covert influencer seeding, targeted persuasion, and suppression.
- Added `POST /api/v1/simulation/run`, `GET /api/v1/simulation/demo-scenario`, and `GET /api/v1/simulation/ethics-policy`.
- Added backend tests and an offline `simulation_lab` benchmark suite.
- Added `frontend/src/pages/SimulationLab.jsx` with scenario controls, synthetic bubble visualization, message/intervention event cards, aggregate metrics, explanation cards, and a step timeline.
- Added frontend A/B comparison mode for two allowed interventions from the same initial scenario, with aggregate deltas and human-review-only recommendation.
- Added deterministic content visibility backlash modeling for lawful/platform-authorized actions, including exposure reduction, backlash cost, trust loss, spillover risk, removal legitimacy, neutral-audience impact, hard-opposition impact, and human-review recommendations.
- Added frontend A/B visibility tradeoff panel for `content_removal_with_explanation`, `visibility_reduction`, and `platform_labeling` when exposed by the backend ethics policy.
- Added Simulation Lab sidebar navigation and frontend API helpers for the existing simulation endpoints.
- Added Event Frame and Audience Initialization design docs for event decomposition, aggregate audience segments, observed frame initialization, baseline gap analysis, strategy policy, visibility tradeoffs, and disclosed creator/expert communication modeling.
- QA-stabilized Event Frame and Audience Initialization terminology, schema coverage, V1.5/monitoring/forecasting relationships, attention/action-threshold mapping, creator/expert communication boundaries, and aggregate-only safety wording.

QA coverage:

- Revalidated route registration, demo scenario, ethics policy, safe rejection errors, deterministic output, bounded opinions, model mechanics, aggregate metrics, and aggregate-only output shape.
- Revalidated the offline `simulation_lab` benchmark suite.
- Browser smoke with local backend/frontend servers revalidated the Simulation Lab route, sidebar navigation, API helper flow, left/center/right/bottom layout, event cards, bubble rendering, aggregate metrics, explanation cards, run/step controls, and timeline updates.
- Browser smoke also revalidated A/B strategy comparison for `no_response` vs `clarification`, `no_response` vs `apology`, `no_response` vs `third_party_evidence`, `clarification` vs `misinformation_correction`, and `no_response` vs `content_removal_with_explanation`; forbidden intervention values remain absent from selectable controls.
- Content visibility QA coverage now includes supported visibility type registration, high-reach exposure reduction sensitivity, low-legitimacy backlash/trust-loss increase, transparent-explanation backlash reduction, screenshot-driven spillover, reactance-driven hard-opposition impact, neutral-audience high concern, 0-100 score clamping, required aggregate scenario groups, API visibility-result shape, aggregate-only output, and target-list absence.
- Latest validation: `python -m pytest` passed (`488 passed in 4.17s`), `python scripts/run_offline_benchmarks.py` passed (`483 passed, 0 failed, 0 warnings`), and `npm run build` passed from `frontend` in 7.90s with the existing non-blocking Ant Design/ECharts vendor chunk warning.
- Event Frame design QA validation: `python -m pytest` passed (`488 passed in 4.03s`) and `python scripts/run_offline_benchmarks.py` passed (`483 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed.
- Frontend build passed for the Simulation Lab page with the existing non-blocking Ant Design/ECharts chunk warning.
- QA fixes normalized simulation numeric ranges, made `intervention_type` visible on event cards, strengthened deterministic/aggregate safety copy, made both rising/falling explanation cards visible, made A/B comparison scalar summary fields explicit, and removed noisy shared Ant Design `Spin` `tip` usage.

Future work:

- Add richer A/B replay controls or a safe aggregate assumption editor after A/B comparison remains stable.
- Implement the case-to-simulation EventFrame and AudienceInitialization initializer from synthetic fixtures and existing aggregate case outputs.
- Add offline benchmark cases for aligned, more-negative, more-positive, polarized, manipulation-suspected, and insufficient-data frames.
- Keep initializing simulation from real monitoring cases and advanced animation as future work.
- Keep real-data event-frame initialization, empirical calibration, creator communication execution, and platform action execution as future/manual-review-only work.
- Keep richer empirical calibration, platform-policy-specific moderation rules, real-data initialization, automatic action execution, and platform enforcement integration as future work.
- Expand ABM validation with sensitivity, docking, ablation, and richer synthetic benchmarks.
- Keep empirical calibration, dynamic network rewiring, cross-platform diffusion, and optional real LLM narrative generation as future work behind safeguards.
- Keep GitHub Actions CI intentionally disabled unless explicitly requested.

### v3.9 LLM Safety QA Stabilization

Status: QA-stabilized on 2026-05-17.

Completed:

- Revalidated `GET /api/v1/llm/status` and `GET /api/v1/llm/usage` as safe metadata-only endpoints.
- Revalidated the `LLM Safety` / `大模型安全状态` page source wiring, sidebar navigation, API helpers, provider cards, guardrail metric display, and safety flags.
- Confirmed the page has no real-call enable button, no API key input, and no `.env` modification path.
- Revalidated `scripts/reset_local_data.py`, `scripts/seed_demo_cases.py`, and `scripts/api_smoke_check.py` for local/mock-only behavior.
- Confirmed GitHub Actions CI remains intentionally disabled and `.github/workflows/ci.yml` was not recreated.

Acceptance:

- backend tests passed with `409 passed in 3.73s`
- frontend production build passed in 7.84s with the existing non-blocking Ant Design/ECharts vendor chunk warning
- no real LLM API, real platform API, real crawler, live public fetch, real notification delivery, API key printing, `.env` printing, raw prompt logging, or raw user-content logging was introduced

Next recommended task:

- Run a browser click-through QA pass for LLM Safety, Platform Integration Overview, Selector Repair Tool, Public Parser Status, and Keyword Search data-source selectors before starting any new real-provider or real-platform work.

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
- `DOUYIN_ADAPTER_MODE=real` is safely blocked as `api_pending:permission_not_verified` when credentials are present or `config_error` when credentials are missing; no real Douyin API calls are made.
- Douyin developer access is recorded as obtained by the user, but Web App OAuth, `item.comment`, token flow, and lawful `item_id` source are not yet verified.
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
- `XIAOHONGSHU_ADAPTER_MODE=real` is safely blocked as `api_pending:permission_not_verified` when credentials are present or `config_error` when credentials are missing; no real Xiaohongshu API calls are made.
- Xiaohongshu developer access is recorded as obtained by the user, but official note/comment API availability is not yet verified.
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
- Douyin comment API permission verification in the Douyin developer console, including interaction/comment management, `item.comment` or equivalent scope, keyword video comment management if applicable, and user authorization limits
- Douyin real-mode minimal integration only after Web App OAuth, `item.comment`, token flow, lawful `item_id` source, and official payload shapes are confirmed
- Kuaishou real API application and approved implementation, only after permission scopes and compliance review are complete
- Xiaohongshu note/comment API permission verification in the Xiaohongshu developer console, including whether comments are available through an official API and whether access is limited to own account, merchant, Ark, ad, or approved creator content
- Xiaohongshu real-mode minimal integration only after note/comment API availability, scope, and official payload shapes are confirmed
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

Status: scaffolded and QA-stabilized with deterministic mock provider on 2026-05-17.

Implemented:

- `backend/app/services/llm/` provider module with a common interface, deterministic `MockProvider`, placeholder `OpenAIProvider`, `DeepSeekProvider`, and `QwenProvider`.
- `provider_factory.get_llm_provider()` defaults to `LLM_PROVIDER=mock`.
- `LLM_ENABLE_REAL_CALLS=false` remains the default; placeholder real providers return safe `provider_not_enabled` / `not_configured` errors and do not make network calls.
- `.env.example` documents `LLM_PROVIDER`, `LLM_ENABLE_REAL_CALLS`, `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, and `QWEN_API_KEY` without requiring values.
- `json_guard` helpers provide deterministic JSON object/array parsing fallbacks for future schema-checked LLM output.
- LLM real-provider readiness helpers are in place: `redaction.redact_api_key()`, `redaction.redact_config_dict()`, and `provider_factory.get_llm_provider_diagnostics()` expose only provider status and present/missing credential state without printing API key values.
- `docs/llm_provider_readiness.md` documents the current mock-only default, safety gates, secret handling rules, and checklist required before any real OpenAI / DeepSeek / Qwen call.
- LLM usage/cost guardrail scaffold is implemented in `backend/app/services/llm/usage_guardrails.py`, with metadata-only mock usage records, deterministic token estimates, call/token/input-size limit checks, in-process usage summaries, and `reset_usage_for_tests()`.
- `.env.example` documents `LLM_USAGE_TRACKING_ENABLED=true`, `LLM_DAILY_CALL_LIMIT=100`, `LLM_DAILY_TOKEN_LIMIT=100000`, `LLM_MAX_INPUT_CHARS=20000`, `LLM_FAIL_CLOSED_ON_LIMIT=true`, and `LLM_COST_GUARDRAIL_MODE=mock`.
- `MockProvider` records safe usage metadata for keyword expansion, sentiment mock LLM analysis, topic extraction/summary, mock report/recommendation drafts, and selector repair suggestions; prompts, raw text, raw HTML, response bodies, and keys are not stored.
- `docs/llm_usage_guardrails.md` documents the current mock-only usage tracking behavior, what is recorded, what is never recorded, and the future checklist before real LLM calls.
- LLM safety status APIs are available at `GET /api/v1/llm/status` and `GET /api/v1/llm/usage`; they expose provider readiness, real-call disabled state, API key presence booleans only, and metadata-only usage summaries.
- `frontend/src/pages/LlmAdminStatus.jsx` adds the `LLM Safety` / `大模型安全状态` dashboard page. It has no real-call toggle, no API key input, no `.env` modification path, and no raw prompt display.
- Local smoke tooling now checks LLM safety endpoints and public parser preview, while `seed_demo_cases.py` creates a deterministic Hupu public-parser demo case without live fetching.
- Keyword expansion now routes through `backend/app/services/keyword/keyword_expander.py`, calls the safe provider factory, and uses `MockProvider` only for current deterministic expansion.
- MockProvider keyword expansion is active for the keyword API and includes deterministic Tesla, Bilibili, Chinese-language, and generic public-opinion variants while preserving the existing keyword response schema.
- Sentiment analysis now supports `SENTIMENT_ANALYZER_MODE=rule_based|mock_llm|future_real_llm`; `rule_based` remains the default, `mock_llm` uses the deterministic offline MockProvider path with rule-based fallback, and `future_real_llm` is a no-call placeholder.
- Topic cluster summaries now support `TOPIC_SUMMARY_MODE=template|mock_llm|future_real_llm`; `template` remains the default, `mock_llm` uses deterministic offline MockProvider cluster summaries with template fallback, and `future_real_llm` is a no-call placeholder.
- Public parser selector repair now has a mock-first backend scaffold: sanitized fixture HTML requests, deterministic `MockProvider.suggest_selector_repair()` candidates, preview against fixture HTML, and explicit `profile_modified=false` behavior.
- `frontend/src/pages/SelectorRepairTool.jsx` provides a developer-facing `Selector 修复工具` page that calls only the mock selector repair suggest/preview endpoints with caller-provided fixture HTML.
- The Selector Repair Tool displays safety notices, candidate selector cards, preview extraction cards, warnings/errors, empty/loading states, and a copy-only JSON draft action; it has no live-fetch toggle and no apply-to-profile action.
- Selector Repair Tool frontend QA is complete for the current mock workflow: route/sidebar wiring, platform options, safety notice, suggestion/preview interactions, empty-HTML error handling, copy-only draft behavior, optional preview field normalization, and no raw JavaScript object rendering were rechecked.
- `.env.example` documents `SELECTOR_REPAIR_MODE=mock`, `SELECTOR_REPAIR_ENABLE_REAL_LLM=false`, and `SELECTOR_REPAIR_MAX_HTML_CHARS=20000`.
- `docs/selector_repair_design.md` documents the sanitized HTML requirement, no-bypass policy, no automatic profile application, and future human-review workflow.
- Selector repair mock scaffold QA is complete: tests cover schema usability, script/style/event-handler removal, bearer/token/cookie-style redaction, HTML length limits, empty/malformed HTML, missing profiles, invalid platforms, deterministic MockProvider suggestions, fixture preview, malformed suggestion rejection, active-profile immutability, endpoint safety, and old parser/API regressions.
- QA coverage verifies module presence, deterministic mock outputs, provider factory defaults and unknown-provider errors, provider-factory invocation from keyword expansion, disabled real-provider behavior, missing-key endpoint safety, secret redaction, safe keyword fallback, old keyword response-schema compatibility, and JSON guard fallback behavior.
- LLM real-provider readiness QA covers default/mock diagnostics, disabled real-provider diagnostics, missing-key diagnostics, unknown-provider diagnostics, present/missing-only redaction helpers, and no credential value exposure.
- LLM usage guardrail QA is complete for the current scaffold. Coverage includes deterministic token estimates, under-limit decisions, call/token/input-size limit blocking, fail-open mode, MockProvider metadata recording across keyword, sentiment, topic, report, recommendation, and selector-repair operations, safe usage-record field shape, no raw prompt/user-content/HTML storage, safe label normalization, usage summary/reset behavior, tracking-disabled behavior, disabled real-provider safety, and placeholder real-provider guardrail checks before future call paths.
- QA coverage also verifies sentiment default mode, rule-based provider isolation, unknown-mode fallback, deterministic English/Chinese/neutral mock LLM mode, disabled/missing-key real-provider safety, failure fallback, no future-real provider calls, V1.5 topic-risk pipeline compatibility, and report-builder compatibility.
- QA coverage also verifies topic summary default template mode, template provider isolation, unknown-mode fallback, deterministic mock LLM cluster summaries, Chinese/English/mixed-input handling, empty-comment and empty-cluster safety, disabled/missing-key real-provider safety, failure fallback, no future-real provider calls, V1.5 topic-risk pipeline compatibility, and report-builder compatibility.
- Latest LLM usage guardrail QA validation passed with focused `python -m pytest backend/app/tests/test_llm_usage_guardrails.py backend/app/tests/test_llm_provider_scaffold.py` (`50 passed in 0.58s`) and full `python -m pytest` (`405 passed in 3.35s`). Frontend build was not rerun for the guardrail QA checkpoint because no frontend files changed. The existing large vendor chunk warning remains non-blocking.

Future real LLM integration tasks:

- Keep real OpenAI integration as a future task.
- Keep real DeepSeek integration as a future task.
- Keep real Qwen integration as a future task.
- Keep real LLM keyword expansion as a future task; current keyword expansion must remain MockProvider-only until an explicit real-provider integration task is approved.
- Keep real LLM sentiment analysis as a future task; current sentiment analysis must remain `rule_based` by default and `mock_llm` must stay offline/deterministic.
- Keep real LLM topic summary generation as a future task; current topic summaries must remain `template` by default and `mock_llm` must stay offline/deterministic.
- Keep real LLM selector repair as a future task; current selector repair must remain `mock` mode, fixture-only, sanitized, and review-required.
- Keep report-builder real LLM drafting as a future task. Current product report generation remains deterministic and template-based; `MockProvider.generate_report()` is available as a provider-layer scaffold only.
- Keep automatic selector profile application as a future/manual-review task. The current frontend must not write active profile files.
- Add prompt calibration and a labeled sentiment evaluation dataset before any real-provider sentiment mode is considered.
- Add topic-summary prompt calibration and fixture evaluation before any real-provider topic summary mode is considered.
- Keep richer frontend selector repair workflow features as future tasks: durable draft storage, side-by-side profile diffing, and explicit human approval gates.
- Add durable draft storage and review/approval workflow before allowing any profile update from selector repair output.
- Add provider-specific HTTP clients only behind explicit `LLM_ENABLE_REAL_CALLS=true` and selected provider configuration.
- Add strict prompt/output schemas for keyword expansion, topic labeling, risk explanations, report drafts, and recommendations.
- Add mocked HTTP tests, timeout handling, retry limits, rate limits, cost/rate-limit tracking, and redacted diagnostics before any live provider call.
- Add provider usage/cost safeguards and clear failure fallbacks to the deterministic pipeline.
- Add real token accounting per provider/model before enabling any real provider call.
- Add provider-specific pricing tables and budget calculation.
- Add user-level or project-level budgets after authentication and tenancy exist.
- Add request throttling and durable usage storage only after the in-process scaffold is stable.
- Add prompt evaluation datasets for each LLM-assisted operation.
- Keep GitHub Actions CI intentionally disabled unless explicitly requested later.
- Keep the LLM Safety page read-only; real-call enabling, key management, provider selection, and durable usage budgets remain future work behind explicit approval.

### v4.0 Offline Benchmark Harness

Status: implemented and QA-stabilized on 2026-05-17.

Completed:

- Added deterministic benchmark fixtures under `benchmarks/`.
- Added `scripts/run_offline_benchmarks.py` for serverless offline evaluation.
- Covered sentiment, topic clustering, V1.5 topic risk, report builder, Markdown export, selector repair mock, public parser fixtures, and mock platform adapter normalization.
- Added generated benchmark output ignore policy via `.benchmarks/`.
- Added pytest coverage for the benchmark runner.
- Added QA coverage for missing fixture files so fixture-loading problems become clear suite failures instead of tracebacks.
- Added `docs/offline_benchmarks.md` and README command notes.
- Added `GET /api/v1/benchmarks/latest`, a safe read-only endpoint for the latest generated offline benchmark summary.
- Added the frontend `Benchmarks / 离线评测` dashboard page for viewing totals, suite status, warning counts, generated time, and regression-risk status.
- Completed Benchmark Dashboard QA for valid, missing, and malformed summary states, expected suite display, safe field exposure, and frontend build regression.
- Added v4.2 benchmark history and regression tracking with `.benchmarks/history/` summary-only entries, `GET /api/v1/benchmarks/history`, `GET /api/v1/benchmarks/regression`, previous/latest comparison, changed-suite reporting, and Dashboard history/regression panels.
- Confirmed the benchmark history/regression design remains summary-only and must not expose per-case payloads, raw prompts, raw user content, API keys, `.env` values, or local file paths.
- Benchmark history/regression QA is complete: latest/history/regression endpoint behavior, runner history output, regression comparison, generated-output redaction, Dashboard labels, sidebar navigation, and frontend build regression are locally validated.
- Expanded the v4.3 synthetic offline evaluation dataset across Chinese crisis/risk sentiment cases, richer topic-cluster scenarios, V1.5 topic-risk edge cases, report/Markdown contexts, selector repair failures, public parser edge fixtures, and adapter mock normalization cases.
- Added `case_count` to suite-level benchmark summaries and safe benchmark API schema normalization. Generated summaries still omit per-case payloads and raw fixture content.
- Expanded dataset QA is complete for the current v4.3 corpus, including malformed fixture-case fail-safe behavior and no raw fixture-text echoing in suite-level failure metadata.
- Added the v4.4 deterministic report quality rubric with a `report_quality_rubric` offline benchmark suite. The rubric checks completeness, risk explanation quality, actionability, safety/professionalism, language/formatting, representative comment preservation, and Markdown report quality without using real LLMs.
- Expanded the v4.5 public parser regression corpus with synthetic per-platform variants for missing author, missing `created_at`, no comments, extra whitespace, nested content, changed container classes, and partial/malformed HTML across `the_paper`, `jiemian`, `hupu`, `tieba`, `nga`, and `maimai`.
- Added per-platform parser corpus status to the offline benchmark summary so fixture-case/check pass-fail counts can be tracked without exposing raw HTML payloads.
- Added the v4.5 deterministic public-opinion forecasting foundation over persisted monitoring snapshots, including forecast schemas, case forecast endpoints, Risk Monitor UI panel, and an offline `forecasting` benchmark suite.

Validation:

- Backend tests passed with `415 passed in 3.47s`.
- Offline benchmark passed with `78 passed, 0 failed, 0 warnings`.
- Frontend build passed in 7.62s with the existing non-blocking Ant Design/ECharts vendor chunk warning.
- v4.2 benchmark history validation passed with `423 passed in 3.66s`, two offline benchmark runs at `78 passed, 0 failed, 0 warnings`, and frontend build in 8.15s with the same non-blocking vendor chunk warning.
- Latest v4.2 QA stabilization passed with focused benchmark tests (`14 passed in 0.77s`), full backend tests (`423 passed in 3.40s`), offline benchmarks (`78 passed, 0 failed, 0 warnings`, `no_regression`), and frontend build in 7.43s with the same non-blocking vendor chunk warning.
- v4.3 dataset expansion validation passed with full backend tests (`423 passed in 3.70s`) and offline benchmarks (`246 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed.
- v4.3 dataset QA stabilization passed with focused benchmark tests (`15 passed in 0.93s`), full backend tests (`424 passed in 3.37s`), and offline benchmarks (`246 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed.
- v4.4 report quality rubric validation passed with focused rubric/benchmark tests (`23 passed in 0.91s`), full backend tests (`432 passed in 3.54s`), and offline benchmarks (`273 passed, 0 failed, 0 warnings`, `no_regression`). Frontend build was not run because no frontend files changed.
- v4.4 report quality rubric QA stabilization passed with focused rubric/benchmark route tests (`24 passed in 0.92s`), full backend tests (`433 passed in 3.52s`), and offline benchmarks (`273 passed, 0 failed, 0 warnings`, `report_quality_rubric: 27 passed`, `no_regression`). QA coverage now explicitly checks dimension-key completeness, secret/private-data finding codes, and benchmark regression tracking for the `report_quality_rubric` suite. Frontend build was not run because no frontend files changed.
- v4.5 parser regression corpus validation passed with parser/benchmark tests (`46 passed in 0.82s`), full backend tests (`436 passed in 3.98s`), and offline benchmarks with generated summary/history output (`390 passed, 0 failed, 0 warnings`, `public_parser_fixtures: 156 passed`, `no_regression`). Frontend build was not run because no frontend files changed.
- v4.5 forecasting foundation validation passed with forecast/benchmark tests (`20 passed`), full backend tests (`450 passed in 4.54s`), offline benchmarks with generated summary/history output (`447 passed, 0 failed, 0 warnings`, `forecasting: 57 passed`, `no_regression`), and frontend build in 8.02s with the existing non-blocking vendor chunk warning.
- v4.5 deterministic forecasting QA stabilization is complete. The pass revalidated no/one/multiple snapshot behavior, conservative confidence rules, risk-level mapping, score clamping, topic forecasts, real-crisis/manipulation forecasts, Risk Monitor forecast-panel source wiring and browser smoke, forecast endpoints, and the offline forecasting benchmark suite. Full backend tests passed with `451 passed in 4.30s`, offline benchmarks passed with `447 passed, 0 failed, 0 warnings`, and frontend build passed in 7.79s with the existing non-blocking vendor chunk warning.
- Forecasting dashboard explanation polish is complete. The Risk Monitor forecast panel now explains forecast status, trend rationale, primary deterministic drivers, history sufficiency, confidence meaning, and recommended action, with an explicit deterministic-MVP disclaimer. Frontend build passed in 7.62s, and browser smoke confirmed the explanation cards on seeded local data; backend tests and offline benchmarks were not rerun because no backend or benchmark code changed.
- GitHub Actions CI remains intentionally disabled unless explicitly requested later.

Future evaluation tasks:

- Expand to a larger human-labeled sentiment dataset.
- Add topic clustering quality metrics and fixture-level expected groupings.
- Expand the report quality rubric with a human-labeled report quality dataset.
- Add optional LLM-as-judge report evaluation only after real-provider safety gates, redaction, budget controls, and human review are ready.
- Continue expanding the parser regression corpus with larger synthetic/sanitized fixture coverage before any real live fetch QA.
- Keep real live fetch QA as future work behind explicit approval, safety review, and mocked regression coverage.
- Add dedicated markdown export rubric checks if report format begins to diverge by report type.
- Expand benchmark history UX with charts after the local file-based history format is stable.
- Add benchmark drill-down views only after a safe redaction/review model for per-case payloads exists.
- Add larger synthetic/historical forecast evaluation cases before any advanced forecasting work.
- Draft a Simulation Lab / forecast scenario design before implementation, including safe mock-only controls, no real-data calls, and benchmark expectations.
- Add V2 dynamic risk forecasting only after topic history, baselines, and benchmark expectations are stable.
- Add LLM output evaluation fixtures before any real LLM provider is enabled.
- Add platform-specific integration benchmarks with mocked clients before any real platform API is enabled.
- Keep GitHub Actions CI intentionally disabled unless explicitly requested later.

### Simulation Lab Design Foundation

Status: documentation complete and QA-stabilized; MVP backend scaffold and frontend bubble visualization are now implemented.

Completed design artifacts:

- `docs/simulation_lab_design.md` defines the ethical aggregate scenario-rehearsal architecture, hybrid agent-based layers, echo chamber model, intervention layer, output metrics, and relationship to monitoring, forecasting, V1.5 risk, and reports.
- `docs/simulation_research_basis.md` maps the DeepSearch research basis into Sentigraph priorities across DeGroot, Friedkin-Johnsen, Hegselmann-Krause, Deffuant-Weisbuch, Granovetter, Watts, complex contagion, homophily/echo chambers, source credibility, framing, agenda-setting, SCCT, Image Repair, misinformation correction, and ODD validation.
- `docs/simulation_model_variables.md` defines conceptual Agent, Message, Network, Intervention, FeedPolicy, and SimulationOutput schemas.
- `docs/simulation_ethics.md` defines allowed and forbidden uses.
- `docs/simulation_mvp_roadmap.md` stages MVP, V2, and later work.
- `docs/simulation_validation_plan.md` defines ODD documentation, docking, sensitivity, ablation, assumption logging, uncertainty labels, and benchmark integration.
- `docs/simulation_event_frame_design.md` defines the Event Frame layer that decomposes observed events into simulation-ready aggregate sub-issues.
- `docs/simulation_audience_initialization.md` defines aggregate audience segments, observed community initialization, persona clusters, and synthetic ordinary-public baselines.
- `docs/simulation_baseline_gap_analysis.md` defines comparison between an observed frame and an external public baseline.
- `docs/simulation_strategy_policy.md` defines ethical strategy implications, content visibility tradeoffs, and disclosed creator/expert communication modeling.

Simulation Lab MVP implementation tasks:

- Backend deterministic toy simulator service using synthetic fixtures: complete.
- Allowed/forbidden intervention validation before simulation run: complete.
- Friedkin-Johnsen style persistence, bounded-confidence gate, threshold expression, homophilous static network, source credibility/framing, and attention decay: complete for MVP.
- Aggregate-only output schemas and safe-mode flags: complete for MVP.
- Offline `simulation_lab` benchmark suite: complete for MVP.
- Frontend 2D bubble visualization: complete for MVP.
- Frontend QA stabilization: complete for MVP.
- Frontend A/B comparison: complete for MVP using the existing safe simulation run endpoint twice from the same initial scenario.
- Strategy report export: complete for MVP with Markdown output from existing aggregate single-scenario or A/B results.
- Richer animation, richer replay controls, and empirical calibration remain future work.

Forbidden implementation paths:

- Do not implement fake consensus, bot amplification, covert influencer seeding, fake events, deceptive attention diversion, vulnerable-group manipulation, individual-level persuasion targeting, account-level influenceability scoring, suppression, or harassment tactics.
- Do not use real accounts, real platform APIs, real LLM APIs, live public fetching, browser cookies, proxy rotation, login bypass, captcha bypass, or private data.
- Do not present simulation output as guaranteed prediction; it must remain assumption-based scenario rehearsal.

Recommended next task:

- Add optional PDF export or a policy/legal review checklist workflow for human-reviewed Simulation Lab strategy reports.

Implemented in current checkpoint:

- Case-to-simulation initializer backend scaffold converts completed case outputs into EventFrame, SubIssue, AudienceSegment, PersonaCluster, FrameGapAnalysis, StrategyImplication, and SimulationScenario objects.
- Case endpoints expose initialization preview and initialization run without calling real APIs, real LLM APIs, crawlers, or live public fetchers.
- Simulation Lab frontend can load a completed case into the bubble sandbox through `从案例初始化沙盘`.
- Offline benchmark suite `case_to_simulation_initializer` covers complete, incomplete, high manipulation-risk, more-negative-frame, and aligned-frame synthetic cases.
- User-level targeting remains forbidden; outputs stay aggregate-level and human-review-oriented.
- GitHub Actions CI remains intentionally disabled.

QA complete:

- Case-to-Simulation Initializer QA is complete.
- `SubIssue.risk_score` is available as a UI/benchmark compatibility alias for `topic_risk_score`.
- Aggregate real-crisis factors are exposed as scenario-level/persona-cluster weights only: `harm_salience`, `loss_sensitivity`, `moral_outrage_sensitivity`, and `crisis_legitimacy_pressure`.
- Positive-skewed, polarized, insufficient-data, and real-crisis mapping tests now guard frame-gap behavior.
- Initializer output avoids named-user targeting, account-level influenceability scoring, forbidden manipulation guidance, and automatic action execution.

Future work:

- Empirically calibrate ordinary-public baselines from lawful, representative public datasets.
- Expand case-to-simulation benchmarks for positive-skewed, polarized, and insufficient-history monitoring cases.
- Add a human-reviewed simulation assumption editor.
- Add PDF export for Simulation Lab strategy reports.
- Add a legal/policy review workflow for real-world action approval.
- Keep individual persuasion profiles, account-level influenceability scoring, covert influence, and automatic action execution out of scope.

Strategy report export implemented:

- `POST /api/v1/simulation/report/markdown` returns a safe Markdown strategy report.
- Frontend Simulation Lab supports `策略预演报告`, `导出策略预演报告`, `复制 Markdown`, and `.md` download.
- Offline benchmark suite `simulation_strategy_report` covers single report export, A/B comparison export, visibility-tradeoff section presence, human-review questions, and safe-content checks.
- Strategy report export QA is complete; tests cover supplied A/B backlash-risk and attention-level fields plus expanded unsafe-content checks.
- PDF export remains future work.
- Legal/policy review workflow remains future work.
- GitHub Actions CI remains intentionally disabled.

QA stabilization result, 2026-05-18:

- Simulation Lab documentation checklist is complete across design, research basis, model variables, ethics, MVP roadmap, and validation plan.
- Event Frame and Audience Initialization documentation is complete across event decomposition, aggregate audience setup, baseline gap analysis, and safe strategy policy.
- Event Frame design QA is complete; real empirical calibration remains future work and GitHub Actions CI remains intentionally disabled.
- Documentation now explicitly preserves the project boundary: aggregate scenario rehearsal only, synthetic/offline MVP first, no real APIs, no real LLM APIs, no live fetching, and no manipulation tactic implementation.
- Simulation Lab MVP backend and frontend scaffolds are implemented; frontend QA stabilization is complete.
- Case-to-Simulation Initializer QA is complete; Strategy Report Export QA is complete; real empirical calibration remains future work, user-level targeting remains forbidden, and PDF export or a legal/policy review workflow remains the next product-polish task.
- Empirical calibration remains future work after synthetic fixtures, benchmark docking, sensitivity analysis, and historical replay planning are stable.
- Real LLM narrative generation remains future work behind explicit safeguards, provider gates, redaction, usage guardrails, schema validation, and human review.
- Latest validation passed with full backend tests (`511 passed in 4.72s`), offline benchmarks (`522 passed, 0 failed, 0 warnings`, `no_regression`), and frontend build (`built in 8.02s`; existing non-blocking Ant Design/ECharts large vendor chunk warning remains).
- GitHub Actions CI remains intentionally disabled unless explicitly requested.

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
