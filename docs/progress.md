# Sentigraph Progress

Last updated: 2026-05-14

## 1. Current Project Status

Sentigraph is currently in a mock-first desktop web MVP stage.

The repository has a FastAPI backend skeleton, a React + Vite desktop dashboard frontend, mock JSON data, API contracts, local development instructions, CI configuration, deterministic backend analysis services, a mock analysis pipeline, and a template-based public opinion report builder.

The current MVP flow is:

```text
keyword input -> mock pipeline analysis -> backend report/visualization APIs -> desktop dashboard
```

Real crawlers, real OpenAI/LLM calls, real database persistence, and complex ML models have not been implemented yet. The MVP remains runnable offline with mock data and deterministic rule/template logic.

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

Latest case management and Markdown export update: Sentigraph now has lightweight in-memory analysis case management for the mock MVP. New backend endpoints support creating cases, listing cases, retrieving case details, running the existing offline V1.5 mock pipeline for a case, and exporting a Chinese public opinion report as Markdown. The frontend now includes a Cases page, Keyword Search creates and runs a case, the header shows the current case, Summary Report can copy/download Markdown for the selected completed case, and the existing Dashboard, AnalysisResult, RiskMonitor, PropagationGraph, and Chinese report pages continue to work. Backend tests passed with `40 passed in 0.41s`; frontend build passed in 7.55s with the existing non-blocking Ant Design/ECharts vendor chunk warning. Browser QA via local Playwright + Chrome passed for create case -> run mock analysis -> Cases list -> open report -> copy Markdown -> download `.md` -> V1.5 page navigation, with no console errors.

Latest v0.3 stabilization QA update: the case management and Markdown export flow was revalidated end to end without product code changes. Backend tests passed with `40 passed in 0.43s`, frontend production build passed in 7.71s, API smoke checks passed for all new case endpoints plus the existing platform, visualization, summary, recommendation, and analysis endpoints, and browser QA passed at a 1440x960 desktop viewport. The browser flow verified Keyword Search -> create/run case -> Dashboard -> Cases -> Summary Report -> copy suggested public response -> copy Markdown -> download `.md` -> AnalysisResult -> RiskMonitor -> PropagationGraph, with no relevant console errors. The in-app Browser runtime still timed out, so this QA pass used temporary Playwright + Chromium tooling outside the repository; no project dependency files were changed.

Latest platform adapter foundation update: added a safe shared platform adapter interface, adapter factory, and Reddit adapter scaffold. Reddit defaults to mock mode and falls back to local mock data when `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, or `REDDIT_USER_AGENT` are missing. Optional real mode is explicit only and is not connected to the current case flow or mock dashboard. Adapter outputs normalize into existing `RawPost` and `RawComment` schemas, with mocked Reddit response tests covering normalization and factory registration. Backend tests passed with `44 passed in 0.42s`; frontend build was not rerun because no frontend files changed.

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
- `backend/app/services/case_store.py` - Deterministic in-memory analysis case store and Markdown report exporter for the mock MVP.
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
- Frontend dependency installation passes with `npm.cmd run frontend:install`, which runs `cd frontend && npm install`; the latest install completed with dependencies already up to date.
- Avoid using `npm.cmd --prefix frontend install` for installation on npm 10.9.2; it can incorrectly link the parent package into `frontend` as `sentigraph: file:..`.
- Frontend production build passes with `npm.cmd run build` from `frontend`; the latest MVP stabilization Vite build completed in 7.73s.
- Latest frontend validation after V1.5 display work passed with `npm.cmd run build`. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after case management and Markdown export passed with `npm.cmd run build` in 7.55s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
- Latest frontend validation after v0.3 stabilization QA passed with `npm.cmd run build` in 7.71s. The Vite large chunk warning for Ant Design/ECharts vendor chunks remains non-blocking.
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
- Rendered browser QA passed through a local Playwright + Chrome fallback at 1440x900. The in-app Browser runtime still timed out during connection, so future Codex browser sessions may need the same fallback until that runtime is stable.
- Case-flow browser QA passed through local Playwright + Chrome: create case, run mock analysis, open the Cases page, open Summary Report, copy Markdown, download `.md`, and navigate to AnalysisResult, RiskMonitor, and PropagationGraph with no console errors.
- v0.3 browser QA passed through temporary Playwright + Chromium tooling at 1440x960: create case, run mock analysis, verify platform roadmap, open report, copy suggested public response, copy Markdown, download `.md`, and navigate through Dashboard, Cases, AnalysisResult, RiskMonitor, and PropagationGraph with no relevant console errors.
- v0.3 API smoke validation passed for `GET /api/v1/cases`, `POST /api/v1/cases`, `GET /api/v1/cases/{case_id}`, `POST /api/v1/cases/{case_id}/run`, `GET /api/v1/cases/{case_id}/report/markdown`, `GET /api/v1/platforms`, `POST /api/v1/visualization/data`, `POST /api/v1/summary/generate`, `POST /api/v1/recommendation/generate`, and `GET /api/v1/analysis/{project_id}`.
- Case storage is currently in-memory per backend process. Restarting the FastAPI server clears created cases; this is intentional for the mock MVP and should be replaced by local JSON or database persistence in a later phase.
- If npm reports a stale dependency or `extraneous` error after earlier local installs, remove generated dependencies and install again:

```powershell
Remove-Item -Recurse -Force frontend\node_modules
Set-Location frontend
npm.cmd install
Set-Location ..
```

- The canonical Git repository root is the `Sentigraph` folder inside the workspace. Any sibling `backend`, `frontend`, or `mock_data` directories outside that folder should be ignored unless intentionally moved into the repository.
- Real crawlers, real OpenAI calls, real MongoDB persistence, Redis, Celery/APScheduler jobs, and real NLP/ML analysis are not implemented yet.
- The report builder is template-based and deterministic; it does not require `OPENAI_API_KEY`.
- Report builder handles missing optional visualization, propagation, risk-factor, and explicit representative-comment inputs without crashing.
- Summary and recommendation endpoints now return the normalized `PublicOpinionReport` fields directly while preserving backward-compatible fields for the current frontend.
- Report builder defaults to Chinese `zh-CN` template output and supports optional `en-US`; it remains deterministic and does not require `OPENAI_API_KEY`.
- Frontend report pages derive structured report sections from the normalized summary/recommendation API responses, explicitly request `zh-CN`, and preserve original-language representative comments.
- The previous frontend only showed Weibo because the backend registry had only `weibo` marked `enabled_in_mvp=true`, and `frontend/src/App.jsx` filtered platform options only by that field. This has been fixed by adding `selectable_for_mock` and marking Reddit, Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao as safe mock-selectable platforms.
- Crawler-later platforms remain visible but disabled with the note `Future crawler integration`. YouTube is not active in the MVP and is marked as optional future.
- YouTube is not active in the MVP and is marked as optional future.
- Reddit adapter scaffold is available but defaults to mock mode; missing credentials intentionally fall back to local mock data.
- Reddit real mode requires `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT`, and remains opt-in and disconnected from current product flows.
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
| RiskMonitor page | complete for MVP | `frontend/src/pages/RiskMonitor.jsx` renders risk trend, radar factors, warnings, and risk model fallback. | Backend should eventually return explicit risk model metadata. |
| PropagationGraph page | complete for MVP | `frontend/src/pages/PropagationGraph.jsx` and `PropagationGraphChart.jsx`; smoke check returned 6 nodes and 3 edges. | Real graph metrics and NetworkX-backed propagation builder are future work. |
| README accuracy | complete with minor caveat | README endpoints match routes in `backend/app/api/v1/api.py`; Windows commands are consistent with root `requirements.txt` and scripts. | Keep README updated after schema changes; production-readiness is correctly not claimed. |
| Algorithm docs | complete for V1.5 | `docs/algorithm_design.md` and `docs/risk_model_roadmap.md` document V1 active, V1.5 implemented as a practical topic-risk bridge, and V2 planned for later. | Frontend should surface V1.5 topic-risk explanations more directly; do not start full V2 yet. |
| Backend tests | complete | `.\.venv\Scripts\python.exe -m pytest` passed with `40 passed in 0.41s`. | Add tests as new features land. |
| Frontend build | complete | `npm.cmd run build` in `frontend` passed in 7.55s. | Vite large chunk warning remains for Ant Design and ECharts vendor chunks; the app chunk is now smaller after safe manual chunking. |

Overall audit conclusion: MVP 0 through MVP 4 are complete enough for the mock-first desktop prototype. The project should not move to real crawlers or real platform APIs yet. The compatibility/metadata and interactive browser QA tasks are complete for the local demo baseline.

## 7. Next Recommended Task

Recommended next implementation task: add fixture-backed Reddit adapter integration tests and a mock-only crawl service bridge that can call the adapter factory without enabling live Reddit requests. If demo continuity is more important, add simple local JSON persistence for cases first.

Suggested scope:

- Do not enable V2 scoring yet.
- Do not replace V1/V1.5 with full V2 during the next task.
- Keep the current mock pipeline and V1.5 report APIs stable.
- If persistence is selected next, keep it local JSON first and do not add MongoDB/Redis yet.
- If alert refinement is selected next, generate alerts from existing V1.5 risk fields without real notifications.
- If Reddit integration is selected next, keep real mode disabled by default and use sanitized fixtures or mocked clients only.
- Re-run the browser checklist in `docs/demo_checklist.md` after the next product-polish task.
- Keep existing API schemas stable.
