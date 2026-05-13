# Sentigraph Progress

Last updated: 2026-05-13

## 1. Current Project Status

Sentigraph is currently in a mock-first desktop web MVP stage.

The repository has a FastAPI backend skeleton, a React + Vite desktop dashboard frontend, mock JSON data, API contracts, local development instructions, CI configuration, deterministic backend analysis services, a mock analysis pipeline, and a template-based public opinion report builder.

The current MVP flow is:

```text
keyword input -> mock pipeline analysis -> backend report/visualization APIs -> desktop dashboard
```

Real crawlers, real OpenAI/LLM calls, real database persistence, and complex ML models have not been implemented yet. The MVP remains runnable offline with mock data and deterministic rule/template logic.

Latest local environment validation on Windows passed: backend dependencies install in the repository-root `.venv`, backend tests pass, frontend dependencies install, and the frontend production build completes.

## 2. Completed MVP Steps

- Created backend FastAPI structure under `backend/app`.
- Created frontend React + Vite structure under `frontend/src`.
- Added Pydantic schemas for keyword, crawl, comment, analysis, visualization, propagation, recommendation, summary, and alerts.
- Added mock JSON data under `mock_data`.
- Added mock FastAPI routes for the MVP API contract.
- Added desktop browser dashboard pages:
  - Dashboard
  - KeywordSearch
  - AnalysisResult
  - PropagationGraph
  - RiskMonitor
  - SummaryReport
- Connected frontend API client to backend mock endpoints.
- Added dark sci-fi desktop dashboard styling with Ant Design, ECharts, Framer Motion, Axios, and lucide icons.
- Prioritized a 1440px desktop browser layout with left sidebar, top status bar, and chart-heavy dashboard panels.
- Added Windows local development instructions to `README.md`.
- Updated frontend install instructions/scripts to run `npm install` from inside `frontend`, avoiding accidental parent-package linking from `npm --prefix frontend install`.
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
- Added `backend/app/services/mock_pipeline.py` to run the offline mock pipeline end to end from `mock_data/raw_comments.json`.
- Updated analysis, visualization, and propagation mock service methods to use pipeline-generated outputs where available.
- Added `backend/app/services/recommendation/report_builder.py` for deterministic template-based public opinion reports.
- Updated `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate` to use the report builder while preserving their existing response schemas.
- Strengthened report builder tests to assert the structured internal report fields and validate summary/recommendation endpoint outputs against Pydantic response schemas.
- Improved the desktop frontend analysis/report experience:
  - Analysis Result now has clearer risk, sentiment, topic, bot, and conflict sections.
  - Risk Monitor now emphasizes risk level, negative sentiment trend, bot impact, radar factors, heatmap, and alert tiles.
  - Propagation Graph now includes small-data-friendly key node summaries beside the graph.
  - Summary Report now includes an export-friendly Public Opinion Report section built from existing summary and recommendation APIs.
- Added module-level pytest coverage for preprocessing, NLP, bot scoring, risk scoring, visualization response structure, mock API contracts, and report generation.

## 3. Important Files and Modules

Backend:

- `backend/app/main.py` - FastAPI app factory and root health route.
- `backend/app/api/v1/api.py` - API router registration.
- `backend/app/api/v1/routes/` - Route handlers for health, keyword expansion, crawl, analysis, visualization, summary, recommendation, propagation, and alerts.
- `backend/app/schemas/` - Pydantic request and response schemas.
- `backend/app/services/mock_service.py` - Mock API response service now backed by the deterministic mock pipeline/report builder where possible.
- `backend/app/services/mock_pipeline.py` - Offline mock pipeline that loads raw comments, runs analysis services, builds propagation, risk, and visualization inputs.
- `backend/app/services/preprocessing/text_cleaner.py` - Rule-based text normalization, language detection, and duplicate fingerprinting.
- `backend/app/services/preprocessing/duplicate_detector.py` - Exact hash and similarity duplicate grouping while preserving author-level clean comments.
- `backend/app/services/preprocessing/user_aggregator.py` - User-level aggregation with duplicate ratio, weighted sentiment, and time range.
- `backend/app/services/nlp/sentiment_analyzer.py` - Mock-mode rule-based sentiment analyzer.
- `backend/app/services/nlp/topic_clusterer.py` - Simple embedding-compatible keyword topic clusterer.
- `backend/app/services/bot_detection/bot_score_service.py` - Rule-based bot probability and impact scoring.
- `backend/app/services/scoring/risk_score.py` - Weighted risk score and factor calculation.
- `backend/app/services/visualization/chart_data_builder.py` - Analysis-to-visualization response transformer and MongoDB-safe key helper.
- `backend/app/services/recommendation/report_builder.py` - Template-based public opinion report builder with no external LLM dependency.
- `backend/app/tests/test_api_contract.py` - API contract tests.
- `backend/app/tests/test_preprocessing_services.py` - Tests for text cleaner, duplicate detector, and user aggregator.
- `backend/app/tests/test_nlp_and_bot_services.py` - Tests for sentiment, topic clustering, and bot scoring.
- `backend/app/tests/test_scoring_and_visualization_services.py` - Tests for risk scoring, visualization builder, and MongoDB-safe key conversion.
- `backend/app/tests/test_report_builder.py` - Tests for deterministic offline report generation and summary/recommendation endpoints.
- `backend/requirements.txt` - Backend dependencies.

Frontend:

- `frontend/src/App.jsx` - Main app state, data loading, page switching, and API orchestration.
- `frontend/src/api/` - Axios client and Sentigraph API functions.
- `frontend/src/components/layout/AppShell.jsx` - Desktop app shell with sidebar and top bar.
- `frontend/src/components/charts/` - ECharts chart components.
- `frontend/src/components/report/PublicOpinionReport.jsx` - Export-friendly public opinion report renderer using existing summary/recommendation data.
- `frontend/src/pages/` - Dashboard and feature pages.
- `frontend/src/styles/global.css` - Desktop dashboard styling.
- `frontend/src/utils/reportModel.js` - Frontend report model mapper for summary, recommendation, analysis, and visualization responses.
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
- Backend tests pass locally in the root `.venv`: `21 passed in 0.41s`.
- Frontend dependency installation passes with `npm.cmd run frontend:install`, which runs `cd frontend && npm install`.
- Avoid using `npm.cmd --prefix frontend install` for installation on npm 10.9.2; it can incorrectly link the parent package into `frontend` as `sentigraph: file:..`.
- Frontend production build passes with `npm.cmd run frontend:build`.
- A stale `backend\.venv` directory exists and points to an older missing Python path. Use the repository-root `.venv` instead.
- `git diff --check` only reports CRLF normalization warnings for touched files; no whitespace errors were reported.
- Vite reports a large chunk warning because Ant Design and ECharts are bundled into a large MVP JavaScript asset. Code splitting can be added later.
- `npm install` reports 2 moderate audit vulnerabilities. They were not force-fixed because `npm audit fix --force` may introduce breaking dependency changes.
- Rendered browser QA could not be completed in this environment because the Browser plugin did not expose callable browser tools, Node REPL did not have Playwright installed, `npx playwright --version` timed out, and Chrome/Edge were not available on PATH. HTTP/API smoke checks and production build passed.
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

## 6. Next Recommended Task

Recommended next task: complete browser-based QA for the improved desktop frontend, then add first-pass PDF/export support for the Public Opinion Report.

Suggested scope:

- Open the local app in a browser at `http://127.0.0.1:5173`.
- Verify Dashboard, AnalysisResult, RiskMonitor, PropagationGraph, and SummaryReport visually.
- Check browser console for React object rendering errors.
- Add a non-PDF export action first, such as print-friendly view or copy report markdown.
- Keep existing API schemas stable.
