# Sentigraph

Sentigraph is an AI-powered public opinion analysis and risk monitoring system.

It allows a user to input one or more keywords, collect public posts/comments from selected platforms, clean and deduplicate the data, analyze sentiment and stance, detect repeated scripts and possible bot behavior, build propagation graphs, calculate risk scores, and display results through a dashboard.

## Main Use Cases

- Brand public opinion monitoring
- Product crisis monitoring
- Public figure reputation analysis
- Social media controversy analysis
- Repeated-script and bot participation detection
- Propagation path visualization
- Risk alerts and public-relations response suggestions

## MVP Goal

The first MVP should not implement real crawlers.

The first MVP should complete this flow:

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

## Recommended Tech Stack

### Backend

- Python 3.10+
- FastAPI
- Pydantic
- MongoDB
- Redis
- Celery or APScheduler
- SentenceTransformers / SimCSE / SBERT
- OpenAI API or compatible LLM API
- NetworkX
- Pytest

### Frontend

- React
- Vite
- Ant Design
- ECharts
- Framer Motion
- Axios

## Initial Repository Structure

```text
sentigraph/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── backend/
├── frontend/
├── docs/
└── mock_data/
```

## Development Order

1. Project skeleton
2. Mock backend APIs
3. Mock frontend dashboard
4. Data schemas
5. Text cleaning and deduplication
6. Sentiment and topic analysis
7. Bot and repeated-script detection
8. Propagation graph
9. Risk scoring
10. Real crawler adapters
11. Incremental monitoring and alerts

## Important Constraints

- Only collect publicly available data.
- Do not implement login bypass.
- Do not implement captcha bypass.
- Do not collect private user data.
- Use mock data before real crawlers.
- Keep frontend/backend schemas consistent.
- Keep duplicate statistics instead of simply deleting duplicate content.

## Suggested First Codex Prompt

```text
Read AGENTS.md, README.md, and all files under docs/ first.

Then create the initial Sentigraph repository skeleton.

Do not implement real crawlers yet.
Do not implement real OpenAI API calls yet.
Use mock data first.
Focus on backend/frontend structure, API contract, mock data, and dashboard connection.
```
