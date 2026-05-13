# Sentigraph Development Instructions

You are working on **Sentigraph**, an AI-powered public opinion analysis, sentiment graph, propagation graph, and risk monitoring system.

## 1. Project Goal

Build a full-stack web application that allows a user to input one or more keywords, collect public posts/comments from selected platforms, clean and deduplicate the data, analyze sentiment, detect repeated scripts, detect possible bot/AI-generated content, build propagation graphs, calculate risk scores, and display results through a dark sci-fi dashboard.

The system should support users such as:

- Companies
- Brands
- Public figures
- Influencers
- Artists
- Political or public-service teams
- Ordinary users who want to understand online opinion trends

## 2. Tech Stack

### Backend

- Python 3.10+
- FastAPI
- Pydantic
- MongoDB
- Redis
- Celery, RQ, or APScheduler
- SentenceTransformers / SimCSE / SBERT
- OpenAI API or compatible LLM API
- NetworkX
- Pandas / NumPy
- Pytest

### Frontend

- React
- Vite
- Ant Design
- ECharts
- Framer Motion
- Axios

## 3. Important Safety and Product Constraints

1. Only collect publicly available data.
2. Do not implement login bypass.
3. Do not implement captcha bypass.
4. Do not implement private data collection.
5. Do not implement anti-bot evasion.
6. Do not collect passwords, tokens, private messages, or hidden user data.
7. Do not hardcode secrets.
8. Use environment variables for API keys and credentials.
9. Keep duplicate content statistics. Do not simply delete duplicate comments.
10. For Chinese text deduplication, use a two-stage approach:
    - embedding-based rough clustering
    - GPT/rule-based confirmation for suspected duplicates
11. GPT/LLM responses must be parsed as strict JSON when JSON is expected.
12. Do not allow Markdown or free-form explanations when a JSON schema is expected.
13. MongoDB document keys must always be strings.
14. Do not directly render JavaScript objects in React.
15. Use mock data first before implementing real crawlers.
16. Implement real platform adapters one by one, starting with Reddit.

## 4. Development Order

Do not try to build the whole project at once.

### Phase 1

- Create backend FastAPI skeleton.
- Create frontend Vite React skeleton.
- Add mock data.
- Add basic API routes.
- Connect frontend to backend with mock data.

### Phase 2

- Build visualization dashboard with mock data.
- Ensure frontend and backend schemas match.

### Phase 3

- Implement preprocessing, deduplication, and user aggregation.

### Phase 4

- Implement sentiment analysis, topic clustering, conflict detection, bot detection, and AI-generated content detection.

### Phase 5

- Implement propagation graph and risk scoring.

### Phase 6

- Implement real platform adapters one by one, starting with Reddit.

### Phase 7

- Add alerts, hourly incremental analysis, and trend-shift detection.

## 5. Backend Requirements

Create a modular FastAPI backend with these layers:

- API routes
- Schemas
- Services
- Repositories
- Workers
- Utils
- Tests

The backend should support:

- keyword expansion
- crawl task creation
- mock crawler data
- text cleaning
- duplicate detection
- user aggregation
- sentiment analysis
- stance analysis
- topic clustering
- conflict detection
- AI-generated content detection
- bot score calculation
- propagation graph construction
- risk score calculation
- visualization data generation
- summary generation
- recommendation generation

## 6. Frontend Requirements

Create a React dashboard with:

- Dashboard page
- Keyword Search page
- Analysis Result page
- Propagation Graph page
- Risk Monitor page
- Summary Report page
- Settings page

Visual style:

- Dark sci-fi theme
- Dark background
- Glowing cards
- ECharts visualizations
- Smooth Framer Motion transitions
- Ant Design components

## 7. Required API Endpoints

Implement these endpoints first. They may return mock data during MVP 0 and MVP 1.

- `POST /api/v1/keywords/expand`
- `POST /api/v1/crawl/start`
- `POST /api/v1/analysis/run`
- `POST /api/v1/visualization/data`
- `POST /api/v1/summary/generate`
- `POST /api/v1/recommendation/generate`

## 8. Testing Requirements

Add backend tests for:

- API schema validation
- JSON parsing guard
- duplicate detection
- sentiment output format
- visualization response structure
- MongoDB-safe dictionary keys

Use pytest.

## 9. Coding Style

- Keep files modular.
- Avoid giant files.
- Add type hints.
- Use Pydantic models for request and response schemas.
- Add docstrings for non-trivial service methods.
- Use environment variables for API keys.
- Never hardcode secrets.
- Keep frontend API calls under `frontend/src/api`.
- Keep reusable charts under `frontend/src/components/charts`.
- Keep route handlers thin and put business logic in services.

## 10. First Task Recommendation for Codex

When starting from an empty repository, the first Codex task should be:

```text
Read AGENTS.md, README.md, and all files under docs/ first.

Create the initial Sentigraph repository skeleton.

Do not implement real crawlers yet.
Do not implement real OpenAI API calls yet.
Use mock data first.
Focus only on:
- backend/frontend structure
- API contract
- mock data
- dashboard connection

Follow the development order in docs/development_plan.md.
```

## 11. Project Handoff Rule

After each major Codex task, update `docs/progress.md`.

The progress file should record:

- Current project status
- Completed MVP steps
- Important files and modules changed
- Windows local run commands
- Known issues and validation status
- Next recommended task
