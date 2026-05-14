# Sentigraph API Contract

Base path:

```text
/api/v1
```

During MVP 0 and MVP 1, all endpoints may return mock data.

## 0. Health Check

### Endpoint

```http
GET /api/v1/health
```

### Response

```json
{
  "status": "ok",
  "mode": "development",
  "version": "0.1.0"
}
```

## 0.1 Platform Registry

### Endpoint

```http
GET /api/v1/platforms
```

### Response

```json
{
  "platforms": [
    {
      "platform_id": "reddit",
      "display_name": "Reddit",
      "category": "future_real_adapter_candidate",
      "source_type": "mock_data_future_adapter_placeholder",
      "status": "mock_selectable_future_adapter_candidate",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "official_platform_url": null,
      "notes": "Selectable for offline mock analysis. Reddit stays in the project as a future real adapter candidate, but no real API call is implemented yet."
    },
    {
      "platform_id": "weibo",
      "display_name": "Weibo",
      "category": "official_api_planned",
      "source_type": "mock_data_official_api_placeholder",
      "status": "mock_selectable_official_api_planned",
      "enabled_in_mvp": true,
      "selectable_for_mock": true,
      "official_platform_url": "https://open.weibo.com",
      "notes": "Selectable for offline mock analysis only. Real access is planned through the official API after credentials, permissions, and compliance review."
    }
  ],
  "active_mvp_platforms": [
    "reddit",
    "weibo",
    "bilibili",
    "douyin",
    "kuaishou",
    "xiaohongshu",
    "zhihu",
    "douban",
    "toutiao"
  ]
}
```

Important:

- `selectable_for_mock=true` means the frontend may show the platform in mock-first selectors.
- Official API planned platforms may be selectable for mock analysis, but they must not trigger real API calls until credentials, permissions, and compliance checks are available.
- Reddit is visible and mock-selectable as a future real adapter candidate.
- Crawler-later platforms are not selectable for real crawling in the MVP.
- YouTube is `disabled_or_optional_future` and is not an active MVP platform.

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
  "platforms": ["reddit", "weibo"],
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
  },
  "risk_model_version": "v1_5_topic_risk_mvp",
  "topic_risks": [],
  "top_risk_topics": [],
  "max_topic_risk": 52.2,
  "average_topic_risk": 41.8,
  "overall_risk": 48.56,
  "real_crisis_risk": 50.4,
  "manipulation_risk": 31.0,
  "risk_explanation": "V1.5 topic risk identifies the leading risk topic and separates crisis/manipulation signals."
}
```

Important:

- `risk`, `risk_score`, and `risk_level` remain backward-compatible project-level fields.
- When topic clusters exist, mock-first analysis responses may also include the V1.5 topic-risk extension fields.
- `topic_risks` and `top_risk_topics` use the same item shape documented in the V1.5 Topic Risk Extension section below.
- `risk_model_version="v1_5_topic_risk_mvp"` means the response includes the deterministic V1.5 topic-level mock risk layer.

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
  "risk_model_version": "v1_static_mvp",
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
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5-compatible visualization responses may set `risk_model_version` to `v1_5_topic_risk_mvp` and include backward-compatible optional fields: `topic_risks`, `top_risk_topics`, `max_topic_risk`, `average_topic_risk`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.
- If schema changes are required, update this file and frontend API transformation together.

### V1.5 Topic Risk Extension

When the V1.5 topic-level mock model is available, visualization/report responses may include:

```json
{
  "risk_model_version": "v1_5_topic_risk_mvp",
  "topic_risks": [
    {
      "topic_id": "topic_001",
      "cluster_id": "topic_001",
      "topic": "Product quality issues",
      "comment_count": 56,
      "negative_ratio": 0.72,
      "average_sentiment_score": -0.74,
      "neg_severity": 0.53,
      "spread_signal": 0.84,
      "controversy_signal": 0.18,
      "bot_signal": 0.31,
      "influence_proxy": 0.62,
      "topic_risk_score": 52.2,
      "topic_risk_level": "medium",
      "risk_explanation": "Product quality issues has topic risk 52.2/100, mainly driven by spread.",
      "risk_score": 52.2,
      "risk_level": "medium"
    }
  ],
  "top_risk_topics": [],
  "max_topic_risk": 52.2,
  "average_topic_risk": 41.8,
  "overall_risk": 48.56,
  "real_crisis_risk": 50.4,
  "manipulation_risk": 31.0,
  "risk_explanation": "V1.5 topic risk identifies the leading risk topic and separates crisis/manipulation signals."
}
```

Risk level mapping for V1.5 topic risk:

```text
0-39   low
40-69  medium
70-84  high
85-100 critical
```

## 6. Summary Generation

### Endpoint

```http
POST /api/v1/summary/generate
```

### Request

```json
{
  "project_id": "project_001",
  "include_representative_comments": true,
  "report_language": "zh-CN"
}
```

### Response

```json
{
  "project_id": "project_001",
  "report_language": "zh-CN",
  "risk_score": 87,
  "risk_level": "high",
  "risk_level_label": "高风险",
  "risk_model_version": "v1_static_mvp",
  "overall_summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "key_findings": [
    "负面情绪占比较高，当前为72%。",
    "负面议题：Product quality issues：356条评论，平均情绪-0.74",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。",
    "传播速度信号较高，当前为84%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。",
    "发布事实性监测说明，承认主要关切，避免放大未经证实的信息。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true,
  "summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。"
}
```

Important:

- `report_language` defaults to `zh-CN`; `en-US` is optional.
- `risk_level` remains the raw English enum: `low`, `medium`, `high`, or `critical`.
- `risk_level_label` is a display label. For `zh-CN`, use `低风险`, `中等风险`, `高风险`, or `严重风险`.
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5 report responses may use `risk_model_version="v1_5_topic_risk_mvp"` and include the optional topic-risk extension fields documented above.
- `summary` is retained as a backward-compatible alias for `overall_summary`.
- Representative comments preserve their original text and are not translated by the report builder.

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
  "tone": "professional",
  "report_language": "zh-CN"
}
```

### Response

```json
{
  "project_id": "project_001",
  "report_language": "zh-CN",
  "risk_score": 87,
  "risk_level": "high",
  "risk_level_label": "高风险",
  "risk_model_version": "v1_static_mvp",
  "overall_summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "key_findings": [
    "负面情绪占比较高，当前为72%。",
    "负面议题：Product quality issues：356条评论，平均情绪-0.74",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。",
    "传播速度信号较高，当前为84%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。",
    "发布事实性监测说明，承认主要关切，避免放大未经证实的信息。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true,
  "summary": "本次离线模拟管线评估显示，项目 project_001 当前舆情风险为高（87/100）。负面情绪占比为72%，讨论焦点集中在「Product quality issues」。系统观察到3个情绪时间桶和18个传播节点。主要风险压力来自负面情绪（72%）。",
  "main_risks": [
    "负面情绪占比较高，当前为72%。",
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "suggested_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。"
}
```

Important:

- `main_risks` and `suggested_response` are retained for backward compatibility.
- New frontend code should prefer `main_risk_factors`, `suspected_bot_signals`, and `suggested_public_response`.

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
      "platform": "weibo",
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

## 10. Analysis Cases

Case APIs are lightweight MVP endpoints for saving mock analysis contexts during local development. The default store is project-local JSON at `backend/data/cases.json` through the case repository/storage abstraction. They do not require MongoDB, Redis, authentication, real crawlers, real platform APIs, or external LLM APIs.

Persistence notes:

- Default backend: `CASE_STORE_BACKEND=local_json`.
- Default path: `CASE_STORE_PATH=backend/data/cases.json`.
- Runtime case JSON files are ignored by git via `backend/data/*.json` and `backend/data/*.json.tmp`.
- Tests must use temporary paths and must not write to the real local demo store.
- MongoDB/Redis stores remain future TODOs behind the same repository interface.

### List Cases

```http
GET /api/v1/cases
```

Response:

```json
[
  {
    "case_id": "case_001",
    "project_id": "project_001",
    "title": "Tesla 舆情分析",
    "keyword": "Tesla",
    "platforms": ["reddit", "weibo", "bilibili"],
    "status": "completed",
    "created_at": "2026-05-14T09:00:00Z",
    "updated_at": "2026-05-14T09:02:00Z",
    "risk_score": 52.2,
    "risk_level": "medium",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "report_language": "zh-CN"
  }
]
```

### Create Case

```http
POST /api/v1/cases
```

Request:

```json
{
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "report_language": "zh-CN"
}
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "status": "draft",
  "analysis_result": null,
  "visualization_data": null,
  "report": null,
  "markdown_available": false
}
```

### Get Case Detail

```http
GET /api/v1/cases/{case_id}
```

Response contains the same metadata as Create Case. After a run, `analysis_result`, `visualization_data`, `report`, and `markdown_available` are populated.

### Run Case

```http
POST /api/v1/cases/{case_id}/run
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "status": "completed",
  "risk_score": 52.2,
  "risk_level": "medium",
  "risk_model_version": "v1_5_topic_risk_mvp",
  "analysis_result": {
    "project_id": "project_001",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "topic_risks": []
  },
  "visualization_data": {
    "project_id": "project_001",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "top_risk_topics": []
  },
  "report": {
    "project_id": "project_001",
    "report_language": "zh-CN",
    "risk_model_version": "v1_5_topic_risk_mvp",
    "overall_summary": "..."
  },
  "markdown_available": true
}
```

Important:

- `POST /api/v1/cases/{case_id}/run` uses the same deterministic offline mock pipeline as the existing analysis, visualization, summary, and recommendation APIs.
- Running a case must not trigger real crawlers or real platform APIs.
- The response keeps V1.5 topic-risk fields inside `analysis_result`, `visualization_data`, and `report` where available.

### Export Markdown Report

```http
GET /api/v1/cases/{case_id}/report/markdown
```

Response:

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "filename": "Tesla_舆情案例_case_001.md",
  "markdown": "# Tesla 舆情案例\n\n## 舆情总览\n...",
  "generated_at": "2026-05-14T09:03:00Z"
}
```

The Markdown report includes title, keyword, selected platforms, risk score, risk level, risk model version, overall summary, key findings, top risk topics, representative comments, suspected bot/repeated-script signals, recommended actions, and suggested public response.

## 11. API Rules

1. Every endpoint should return JSON.
2. Use Pydantic schemas for all request and response bodies.
3. Avoid inconsistent field names.
4. Use snake_case in backend JSON fields.
5. Keep frontend transformations isolated in `frontend/src/api`.
6. Use mock data when real data is unavailable.
7. Do not break existing frontend components without updating this contract.
