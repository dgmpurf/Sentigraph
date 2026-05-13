# Sentigraph API Contract

Base path:

```text
/api/v1
```

During MVP 0 and MVP 1, all endpoints may return mock data.

## 1. Keyword Expansion

### Endpoint

```http
POST /api/v1/keywords/expand
```

### Request

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo"],
  "language": "auto"
}
```

### Response

```json
{
  "original_keyword": "Tesla",
  "expanded_keywords": ["Tesla", "特斯拉", "Model Y", "自动驾驶", "降价"],
  "search_queries": [
    "Tesla problem",
    "Tesla recall",
    "特斯拉 刹车",
    "特斯拉 降价"
  ]
}
```

## 2. Start Crawl

### Endpoint

```http
POST /api/v1/crawl/start
```

### Request

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit"],
  "limit": 100,
  "date_range": {
    "start": "2026-05-01",
    "end": "2026-05-13"
  }
}
```

### Response

```json
{
  "project_id": "project_001",
  "crawl_task_id": "crawl_task_001",
  "status": "queued",
  "message": "Crawl task created. Mock data will be used in MVP mode."
}
```

## 3. Run Analysis

### Endpoint

```http
POST /api/v1/analysis/run
```

### Request

```json
{
  "project_id": "project_001",
  "analysis_types": [
    "sentiment",
    "topic",
    "bot",
    "ai_generated",
    "propagation",
    "risk"
  ]
}
```

### Response

```json
{
  "project_id": "project_001",
  "analysis_task_id": "analysis_task_001",
  "status": "queued",
  "message": "Analysis task created. Mock analysis will be returned in MVP mode."
}
```

## 4. Get Analysis Result

### Endpoint

```http
GET /api/v1/analysis/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "summary": "Current public opinion is mainly negative and focused on product quality.",
  "sentiment": {
    "positive_ratio": 0.12,
    "neutral_ratio": 0.16,
    "negative_ratio": 0.72,
    "average_sentiment_score": -0.68
  },
  "topics": [],
  "conflicts": [],
  "bot_score": {
    "suspected_bot_ratio": 0.24,
    "suspected_bot_comment_ratio": 0.39
  },
  "risk": {
    "risk_score": 87,
    "risk_level": "high"
  }
}
```

## 5. Visualization Data

### Endpoint

```http
POST /api/v1/visualization/data
```

### Request

```json
{
  "project_id": "project_001",
  "date_range": {
    "start": "2026-05-01",
    "end": "2026-05-13"
  },
  "platforms": ["reddit", "weibo"]
}
```

### Response

```json
{
  "project_id": "project_001",
  "risk_score": 87,
  "risk_level": "high",
  "sentiment_trend": [
    {
      "time": "2026-05-13T10:00:00Z",
      "positive": 12,
      "neutral": 20,
      "negative": 68
    }
  ],
  "risk_radar": {
    "negative_sentiment": 0.72,
    "bot_impact": 0.61,
    "propagation_speed": 0.84,
    "controversy": 0.78,
    "trend_shift": 0.67
  },
  "heatmap": [],
  "propagation_graph": {
    "nodes": [],
    "edges": []
  },
  "topic_clusters": [],
  "bot_impact": {
    "suspected_bot_ratio": 0.24,
    "suspected_bot_comment_ratio": 0.39
  }
}
```

Important:

- The frontend must not assume fields that are not defined here.
- The backend must keep this schema stable.
- If schema changes are required, update this file and frontend API transformation together.

## 6. Summary Generation

### Endpoint

```http
POST /api/v1/summary/generate
```

### Request

```json
{
  "project_id": "project_001",
  "include_representative_comments": true
}
```

### Response

```json
{
  "project_id": "project_001",
  "summary": "Current public opinion is mainly negative and focused on product quality.",
  "key_findings": [
    "Negative sentiment is increasing quickly.",
    "The main topic is product quality.",
    "Repeated negative scripts are detected."
  ],
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ]
}
```

## 7. Recommendation Generation

### Endpoint

```http
POST /api/v1/recommendation/generate
```

### Request

```json
{
  "project_id": "project_001",
  "user_type": "brand",
  "tone": "professional"
}
```

### Response

```json
{
  "summary": "Current public opinion is mainly negative and focused on product quality.",
  "main_risks": [
    "Quality-related complaints are spreading quickly.",
    "Repeated negative scripts suggest coordinated amplification."
  ],
  "recommended_actions": [
    "Publish a factual clarification within 24 hours.",
    "Address the most repeated complaint directly.",
    "Avoid emotional confrontation with users.",
    "Prepare FAQ responses for customer service."
  ],
  "suggested_response": "We are aware of the concerns regarding product quality and are currently investigating..."
}
```

## 8. Propagation Graph

### Endpoint

```http
GET /api/v1/propagation/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "nodes": [
    {
      "node_id": "post_001",
      "type": "post",
      "platform": "reddit",
      "content": "Original post content",
      "author_id": "user_hash_001",
      "created_at": "2026-05-13T10:00:00Z",
      "sentiment_score": -0.72,
      "influence_score": 0.88
    }
  ],
  "edges": [
    {
      "source": "post_001",
      "target": "comment_002",
      "relation": "reply",
      "weight": 0.64
    }
  ],
  "metrics": {
    "depth": 4,
    "breadth": 128,
    "central_node_id": "post_001",
    "propagation_speed": 0.84
  }
}
```

## 9. Alerts

### Endpoint

```http
GET /api/v1/alerts/{project_id}
```

### Response

```json
{
  "project_id": "project_001",
  "alerts": [
    {
      "alert_id": "alert_001",
      "level": "high",
      "message": "Negative sentiment increased by more than 30% in the last hour.",
      "created_at": "2026-05-13T11:00:00Z",
      "resolved": false
    }
  ]
}
```

## 10. API Rules

1. Every endpoint should return JSON.
2. Use Pydantic schemas for all request and response bodies.
3. Avoid inconsistent field names.
4. Use snake_case in backend JSON fields.
5. Keep frontend transformations isolated in `frontend/src/api`.
6. Use mock data when real data is unavailable.
7. Do not break existing frontend components without updating this contract.
