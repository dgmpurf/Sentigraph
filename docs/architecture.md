# Sentigraph Architecture

## 1. System Overview

Sentigraph is a full-stack public opinion analysis system.

A user inputs one or more keywords. The system expands the keywords, collects public posts and comments from selected platforms, stores raw data, cleans and deduplicates the data, performs sentiment and topic analysis, detects repeated scripts and possible bot behavior, builds propagation graphs, calculates risk scores, and visualizes the result.

## 2. High-Level Data Flow

```text
User keyword input
    ↓
Keyword expansion / synonym generation
    ↓
Crawl task scheduler
    ↓
Platform adapters
    ↓
Raw data storage
    ↓
Text cleaning / normalization
    ↓
User aggregation / duplicate detection
    ↓
Embedding / semantic clustering
    ↓
Sentiment / stance / topic analysis
    ↓
AI-generated content detection
    ↓
Bot / repeated-script detection
    ↓
Propagation graph construction
    ↓
Risk scoring / trend shift detection
    ↓
Visualization / summary / recommendation
```

## 3. Backend Architecture

```text
backend/
└── app/
    ├── main.py
    ├── core/
    ├── db/
    ├── schemas/
    ├── models/
    ├── api/
    ├── services/
    ├── repositories/
    ├── workers/
    ├── utils/
    └── tests/
```

## 4. Backend Layer Responsibilities

### API Layer

Responsible for HTTP request/response handling.

Location:

```text
backend/app/api/v1/routes/
```

### Schema Layer

Defines Pydantic request and response models.

Location:

```text
backend/app/schemas/
```

### Service Layer

Contains business logic.

Location:

```text
backend/app/services/
```

Major service groups:

```text
services/keyword/
services/crawling/
services/preprocessing/
services/nlp/
services/bot_detection/
services/propagation/
services/scoring/
services/recommendation/
services/visualization/
```

### Repository Layer

Responsible for database read/write operations.

Location:

```text
backend/app/repositories/
```

### Worker Layer

Responsible for async/background tasks.

Location:

```text
backend/app/workers/
```

### Utils Layer

Shared helpers.

Location:

```text
backend/app/utils/
```

## 5. Frontend Architecture

```text
frontend/
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── api/
    ├── pages/
    ├── components/
    ├── styles/
    └── utils/
```

## 6. Frontend Page Responsibilities

### Dashboard

Shows overall risk score, sentiment summary, platform distribution, bot impact, and alerts.

### KeywordSearch

Allows the user to input keywords, select platforms, select date range, and start analysis.

### AnalysisResult

Shows sentiment analysis, topic clusters, conflicts, representative comments, bot/AI content detection.

### PropagationGraph

Shows public opinion propagation graph, core nodes, propagation depth, propagation breadth, and influence ranking.

### RiskMonitor

Shows risk trend, threshold alerts, hourly changes, and trend shift.

### SummaryReport

Shows final summary, risks, conflicts, response suggestions, and response templates.

## 7. Core Modules

## 7.1 Keyword Module

Location:

```text
services/keyword/
```

Responsibilities:

- Expand keywords
- Generate synonym queries
- Generate platform-specific search queries

## 7.2 Crawling Module

Location:

```text
services/crawling/
```

Responsibilities:

- Schedule crawl jobs
- Use platform adapters
- Normalize raw data into unified schema

Important constraint:

- Only collect public data.
- Do not implement login bypass or captcha bypass.

## 7.3 Preprocessing Module

Location:

```text
services/preprocessing/
```

Responsibilities:

- Clean text
- Normalize text
- Detect language
- Detect duplicates
- Aggregate comments by user
- Preserve duplicate statistics

## 7.4 NLP Module

Location:

```text
services/nlp/
```

Responsibilities:

- Embedding generation
- Sentiment analysis
- Stance analysis
- Topic clustering
- Opinion extraction
- Conflict detection
- AI-generated content detection
- Summary generation

## 7.5 Bot Detection Module

Location:

```text
services/bot_detection/
```

Responsibilities:

- Extract behavior features
- Detect repeated scripts
- Detect account patterns
- Calculate bot probability

## 7.6 Propagation Module

Location:

```text
services/propagation/
```

Responsibilities:

- Build post-comment-reply graph
- Calculate graph metrics
- Analyze propagation depth
- Calculate influence score

## 7.7 Scoring Module

Location:

```text
services/scoring/
```

Responsibilities:

- Calculate sentiment score
- Calculate risk score
- Calculate bot impact score
- Calculate controversy score
- Detect trend shift

## 7.8 Recommendation Module

Location:

```text
services/recommendation/
```

Responsibilities:

- Generate response suggestions
- Generate crisis strategy
- Generate public response templates

## 7.9 Visualization Module

Location:

```text
services/visualization/
```

Responsibilities:

- Build chart-ready data
- Build radar chart data
- Build trend chart data
- Build heatmap data
- Build graph data

## 8. Recommended Initial Directory Structure

```text
sentigraph/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── models/
│   │   ├── api/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── workers/
│   │   ├── utils/
│   │   └── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api/
│       ├── pages/
│       ├── components/
│       ├── styles/
│       └── utils/
│
├── docs/
└── mock_data/
```

## 9. MVP Principle

The first working version should use mock data.

Do not build all real crawlers in the first version.

The first version should prove:

```text
keyword input → backend mock analysis → frontend visual dashboard
```
