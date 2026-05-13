# Sentigraph

Sentigraph is a mock-first public opinion analysis and risk monitoring system.

This repository currently targets the desktop web MVP: a FastAPI backend returns stable mock API responses, and a React + Vite frontend renders a dark sci-fi dashboard with charts, risk monitoring, propagation graph, summary, and response recommendations.

## Desktop Web Target

MVP 0 prioritizes a PC/browser dashboard, not a mobile app and not a mobile-first interface.

- Default design width: 1440px desktop screen.
- Layout: left sidebar navigation, top status/header bar, and main dashboard workspace.
- Visualizations: ECharts panels sized for desktop monitoring and comparison.
- Smaller-screen responsive behavior is intentionally deferred to later phases.

This project does not use React Native and does not include a mobile app shell.

## MVP Flow

```text
User enters keyword
    ↓
Backend returns mock public opinion data
    ↓
Backend returns mock analysis result
    ↓
Frontend renders dashboard charts
    ↓
User can view sentiment, risk score, topics, bot impact, and propagation graph
```

## Tech Stack

Backend:

- Python 3.10+
- FastAPI
- Pydantic
- Pytest

Frontend:

- React
- Vite
- Ant Design
- ECharts
- Framer Motion
- Axios

## Local Development Requirements

- Windows 10/11 or another desktop OS.
- Python 3.10 or newer for the backend. The repository includes `.python-version` with `3.10`.
- Node.js 22 is recommended for the frontend and CI parity.
- npm 10+.

The MVP remains mock-first. No real crawlers, real OpenAI calls, database writes, login bypass, or captcha bypass are required for local development.

## Repository Structure

```text
sentigraph/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .python-version
├── AGENTS.md
├── README.md
├── package.json
├── pytest.ini
├── requirements.txt
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── api/
│       ├── core/
│       ├── db/
│       ├── models/
│       ├── repositories/
│       ├── schemas/
│       ├── services/
│       ├── tests/
│       ├── utils/
│       └── workers/
├── frontend/
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── api/
│       ├── components/
│       ├── pages/
│       ├── styles/
│       └── utils/
├── docs/
└── mock_data/
```

## Windows Setup

From PowerShell, confirm your tools:

```powershell
py -3.10 --version
node -v
npm.cmd -v
```

Create and activate a backend virtual environment:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

Install frontend dependencies:

```powershell
npm.cmd --prefix frontend install
```

If PowerShell blocks `npm` because script execution is disabled, use `npm.cmd` as shown above.

If npm reports a stale dependency error after earlier local installs, remove the generated dependency folder and install again:

```powershell
Remove-Item -Recurse -Force frontend\node_modules
npm.cmd --prefix frontend install
```

## Run Backend

With the virtual environment active, start the API server:

```bash
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Health checks:

```text
http://127.0.0.1:8000/api/v1/health
http://127.0.0.1:8000/health
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Run backend tests:

```bash
python -m pytest
```

## Run Frontend

Start the desktop web dashboard in another terminal:

```bash
npm --prefix frontend run dev
```

Open:

```text
http://127.0.0.1:5173
```

During development, Vite proxies `/api` requests to `http://127.0.0.1:8000`.

## Useful Scripts

From the repository root:

```bash
npm run backend:install
npm run backend:dev
npm run backend:test
npm run frontend:install
npm run frontend:dev
npm run frontend:build
```

On Windows PowerShell, use `npm.cmd run <script>` if `npm` is blocked by execution policy.

## Continuous Integration

GitHub Actions is configured in `.github/workflows/ci.yml`.

CI runs:

- Backend tests on Python 3.10 with `python -m pytest`.
- Frontend dependency install with `npm install`.
- Frontend production build with `npm run build`.

## Implemented Mock Endpoints

Base path:

```text
/api/v1
```

Endpoints:

- `GET /api/v1/health`
- `POST /api/v1/keywords/expand`
- `POST /api/v1/crawl/start`
- `POST /api/v1/analysis/run`
- `GET /api/v1/analysis/{project_id}`
- `POST /api/v1/visualization/data`
- `POST /api/v1/summary/generate`
- `POST /api/v1/recommendation/generate`
- `GET /api/v1/propagation/{project_id}`
- `GET /api/v1/alerts/{project_id}`

## Current Constraints

- Real crawlers are not implemented yet.
- Real OpenAI or other LLM API calls are not implemented yet.
- Mock data is stored under `mock_data/`.
- Duplicate statistics are represented in the schemas and mock data.
- API and frontend fields use the documented snake_case contract.

## Safety Rules

- Only collect publicly available data.
- Do not implement login bypass.
- Do not implement captcha bypass.
- Do not collect private user data.
- Do not hardcode secrets.
- Use mock mode before real platform adapters.
