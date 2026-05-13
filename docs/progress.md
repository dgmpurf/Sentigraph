# Sentigraph Progress

Last updated: 2026-05-13

## 1. Current Project Status

Sentigraph is currently in a mock-first desktop web MVP stage.

The repository has a FastAPI backend skeleton, a React + Vite desktop dashboard frontend, mock JSON data, API contracts, local development instructions, CI configuration, and deterministic backend analysis service foundations.

The current MVP flow is:

```text
keyword input -> backend mock APIs -> frontend desktop dashboard visualization
```

Real crawlers, real OpenAI/LLM calls, real database persistence, and complex ML models have not been implemented yet.

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
- Added `.python-version` with Python 3.10.
- Added `pytest.ini`.
- Added `GET /api/v1/health`.
- Added GitHub Actions CI for backend tests and frontend build.
- Created `docs/progress.md` as the project handoff and progress log.
- Added an `AGENTS.md` rule requiring `docs/progress.md` updates after each major Codex task.
- Confirmed frontend production build works locally with `npm.cmd --prefix frontend run build`.
- Implemented deterministic backend analysis service modules:
  - text cleaning with whitespace normalization, HTML tag removal, punctuation normalization, language detection, and safe empty-text handling
  - exact SHA-256 fingerprint duplicate detection plus similarity-based grouping
  - author-level aggregation with comment counts, duplicate ratio, weighted sentiment, and time range
  - mock rule-based sentiment analysis
  - embedding-compatible keyword topic clustering
  - rule-based bot scoring using duplicate ratio, repeated scripts, posting frequency, synchronization, and sentiment uniformity
  - weighted risk scoring from sentiment, bot impact, propagation speed, controversy, and trend shift
  - visualization response building for the existing `/api/v1/visualization/data` contract
- Added module-level pytest coverage for preprocessing, NLP, bot scoring, risk scoring, and visualization response structure.

## 3. Important Files and Modules

Backend:

- `backend/app/main.py` - FastAPI app factory and root health route.
- `backend/app/api/v1/api.py` - API router registration.
- `backend/app/api/v1/routes/` - Route handlers for health, keyword expansion, crawl, analysis, visualization, summary, recommendation, propagation, and alerts.
- `backend/app/schemas/` - Pydantic request and response schemas.
- `backend/app/services/mock_service.py` - Mock response service used by current MVP routes.
- `backend/app/services/preprocessing/text_cleaner.py` - Rule-based text normalization, language detection, and duplicate fingerprinting.
- `backend/app/services/preprocessing/duplicate_detector.py` - Exact hash and similarity duplicate grouping while preserving author-level clean comments.
- `backend/app/services/preprocessing/user_aggregator.py` - User-level aggregation with duplicate ratio, weighted sentiment, and time range.
- `backend/app/services/nlp/sentiment_analyzer.py` - Mock-mode rule-based sentiment analyzer.
- `backend/app/services/nlp/topic_clusterer.py` - Simple embedding-compatible keyword topic clusterer.
- `backend/app/services/bot_detection/bot_score_service.py` - Rule-based bot probability and impact scoring.
- `backend/app/services/scoring/risk_score.py` - Weighted risk score and factor calculation.
- `backend/app/services/visualization/chart_data_builder.py` - Analysis-to-visualization response transformer and MongoDB-safe key helper.
- `backend/app/tests/test_api_contract.py` - Minimal API contract tests.
- `backend/app/tests/test_preprocessing_services.py` - Tests for text cleaner, duplicate detector, and user aggregator.
- `backend/app/tests/test_nlp_and_bot_services.py` - Tests for sentiment, topic clustering, and bot scoring.
- `backend/app/tests/test_scoring_and_visualization_services.py` - Tests for risk scoring, visualization builder, and MongoDB-safe key conversion.
- `backend/requirements.txt` - Backend dependencies.

Frontend:

- `frontend/src/App.jsx` - Main app state, data loading, page switching, and API orchestration.
- `frontend/src/api/` - Axios client and Sentigraph API functions.
- `frontend/src/components/layout/AppShell.jsx` - Desktop app shell with sidebar and top bar.
- `frontend/src/components/charts/` - ECharts chart components.
- `frontend/src/pages/` - Dashboard and feature pages.
- `frontend/src/styles/global.css` - Desktop dashboard styling.
- `frontend/package.json` - Frontend scripts and dependencies.
- `frontend/package-lock.json` - Frontend dependency lock file.

Project and docs:

- `README.md` - Setup, run instructions, constraints, and endpoint list.
- `AGENTS.md` - Development instructions, safety constraints, and the rule to update `docs/progress.md` after each major Codex task.
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
npm.cmd --prefix frontend install
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

- Local backend pytest could not be run in this environment because Python 3.10 is not installed. The Windows Python launcher currently lists only Python 3.7 and Python 2.7.
- The existing `backend\.venv` is broken in this environment because it points to a missing Python 3.10 executable path.
- A syntax-only fallback check passed with Python 3.7 using `py -3.7 -m py_compile` against the updated backend service and test files.
- The current frontend build succeeds, but Vite reports a large chunk warning because Ant Design and ECharts are bundled into a large MVP JavaScript asset. Code splitting can be added later.
- If npm reports a stale dependency or `extraneous` error after earlier local installs, remove generated dependencies and install again:

```powershell
Remove-Item -Recurse -Force frontend\node_modules
npm.cmd --prefix frontend install
```

- The canonical Git repository root is the `Sentigraph` folder inside the workspace. Any sibling `backend`, `frontend`, or `mock_data` directories outside that folder should be ignored unless intentionally moved into the repository.
- Real crawlers, real OpenAI calls, real MongoDB persistence, Redis, Celery/APScheduler jobs, and real NLP/ML analysis are not implemented yet.
- New rule-based service modules are not yet wired into the existing mock API endpoints; current endpoints still return predefined mock responses.

## 6. Next Recommended Task

Recommended next task: wire the new rule-based analysis services into the mock analysis pipeline while keeping the API response schema stable.

Suggested scope:

- Load `mock_data/raw_comments.json`.
- Run text cleaning and duplicate detection.
- Run user aggregation, sentiment analysis, topic clustering, bot scoring, and risk scoring.
- Use `chart_data_builder.py` for visualization responses.
- Keep all `/api/v1` response fields unchanged.
- Run backend tests in a working Python 3.10 environment.

Keep the frontend/backend API contract stable while adding these backend services.
