# Sentigraph Data Schema

This document defines the core data structures for Sentigraph.

All schemas should be implemented as Pydantic models in:

```text
backend/app/schemas/
```

MongoDB document keys must always be strings.

## 0. Platform Source Registry

```json
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
}
```

Allowed platform categories:

```text
official_api_planned
future_real_adapter_candidate
crawler_later
disabled_or_optional_future
```

Only `selectable_for_mock=true` platforms should appear in active MVP frontend selectors. These selections are mock-only and must not trigger real crawlers or real platform APIs.

## 0.5 Analysis Case

Analysis cases are lightweight MVP objects used to preserve one mock analysis context across pages. Current storage is in-memory/local-process only. MongoDB/Redis persistence remains future work.

### AnalysisCaseCreateRequest

```json
{
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "report_language": "zh-CN"
}
```

### AnalysisCaseListItem

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
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
```

Allowed case statuses:

```text
draft
running
completed
failed
```

### AnalysisCaseDetail

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "title": "Tesla 舆情案例",
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo", "bilibili"],
  "status": "completed",
  "analysis_result": {},
  "visualization_data": {},
  "report": {},
  "markdown_available": true
}
```

Rules:

- `analysis_result` uses the existing `AnalysisResultResponse` schema.
- `visualization_data` uses the existing `VisualizationResponse` schema.
- `report` uses the normalized `PublicOpinionReport` schema.
- The MVP case store is deterministic and does not require a database.
- Case creation and case run must remain mock-first and must not call real platform APIs or crawlers.

### MarkdownExportResponse

```json
{
  "case_id": "case_001",
  "project_id": "project_001",
  "filename": "Tesla_舆情案例_case_001.md",
  "markdown": "# Tesla 舆情案例\n\n## 舆情总览\n...",
  "generated_at": "2026-05-14T09:03:00Z"
}
```

## 1. Keyword Expansion

### KeywordExpandRequest

```json
{
  "keyword": "Tesla",
  "platforms": ["reddit", "weibo"],
  "language": "auto"
}
```

### KeywordExpandResponse

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

## 2. Raw Post

```json
{
  "platform": "weibo",
  "post_id": "post_001",
  "author_id": "user_hash_001",
  "author_name": "anonymous_user",
  "title": "Is this product quality getting worse?",
  "content": "I have seen many complaints about this product recently.",
  "like_count": 120,
  "reply_count": 35,
  "share_count": 3,
  "created_at": "2026-05-13T10:00:00Z",
  "url": "https://example.com/post/post_001",
  "raw_data": {}
}
```

## 3. Raw Comment

```json
{
  "platform": "weibo",
  "post_id": "post_001",
  "comment_id": "comment_001",
  "parent_id": null,
  "author_id": "user_hash_002",
  "author_name": "anonymous_user",
  "content": "I think this product has serious quality issues.",
  "like_count": 45,
  "reply_count": 8,
  "share_count": 0,
  "created_at": "2026-05-13T10:05:00Z",
  "url": "https://example.com/post/post_001/comment/comment_001",
  "raw_data": {}
}
```

## 4. Clean Comment

```json
{
  "clean_comment_id": "clean_001",
  "original_comment_ids": ["comment_001", "comment_008", "comment_021"],
  "platforms": ["weibo"],
  "post_ids": ["post_001"],
  "author_id": "user_hash_002",
  "clean_text": "this product has serious quality issues",
  "language": "en",
  "duplicate_group_id": "dup_group_001",
  "duplicate_count": 12,
  "semantic_similarity_group": "sem_group_008",
  "is_repeated_script": true,
  "created_at_min": "2026-05-13T10:05:00Z",
  "created_at_max": "2026-05-13T12:08:00Z"
}
```

## 5. User Aggregation Result

```json
{
  "author_id": "user_hash_002",
  "platforms": ["weibo"],
  "comment_count": 18,
  "unique_comment_count": 5,
  "duplicate_comment_ratio": 0.72,
  "average_sentiment_score": -0.64,
  "first_seen_at": "2026-05-13T10:05:00Z",
  "last_seen_at": "2026-05-13T12:08:00Z"
}
```

## 6. Sentiment Result

```json
{
  "comment_id": "clean_001",
  "sentiment": "negative",
  "sentiment_score": -0.82,
  "emotion_tags": ["anger", "distrust"],
  "stance": "opposing",
  "confidence": 0.91,
  "reason": "The comment expresses strong dissatisfaction and distrust."
}
```

Allowed sentiment values:

```text
positive
negative
neutral
mixed
```

Recommended emotion tags:

```text
anger
fear
sadness
trust
mocking
questioning
supportive
opposing
disappointment
uncertainty
```

## 7. Topic Cluster

```json
{
  "cluster_id": "topic_001",
  "topic": "Product quality issues",
  "summary": "Many users complain about durability and defects.",
  "comment_count": 356,
  "average_sentiment_score": -0.74,
  "representative_comments": [
    "This product broke after two weeks.",
    "Quality control seems terrible."
  ]
}
```

## 8. Conflict Result

```json
{
  "conflict_id": "conflict_001",
  "side_a": "The product has real quality issues.",
  "side_b": "The negative trend is caused by malicious competitors.",
  "intensity": 0.83,
  "evidence_comments": [
    "This product has real quality problems.",
    "This looks like a coordinated attack."
  ]
}
```

## 9. AI-Generated Content Detection

```json
{
  "comment_id": "clean_001",
  "ai_generated_probability": 0.76,
  "template_similarity_score": 0.88,
  "reason": "Multiple comments share highly similar sentence structures."
}
```

## 10. Bot Score

```json
{
  "author_id": "user_hash_002",
  "bot_probability": 0.81,
  "bot_reasons": [
    "High repeated content ratio",
    "Abnormally frequent comments",
    "Highly synchronized posting time"
  ],
  "influence_weight": 0.43
}
```

## 11. Propagation Graph

### Node

```json
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
```

### Edge

```json
{
  "source": "post_001",
  "target": "comment_002",
  "relation": "reply",
  "weight": 0.64
}
```

### Full Graph

```json
{
  "nodes": [],
  "edges": [],
  "metrics": {
    "depth": 4,
    "breadth": 128,
    "central_node_id": "post_001",
    "propagation_speed": 0.84
  }
}
```

## 12. Risk Score

```json
{
  "risk_score": 87,
  "risk_level": "high",
  "risk_factors": {
    "negative_sentiment_ratio": 0.72,
    "negative_sentiment_strength": 0.81,
    "bot_impact_score": 0.61,
    "propagation_speed": 0.84,
    "controversy_score": 0.78,
    "trend_shift": 0.67
  },
  "explanation": "Negative sentiment is rapidly increasing with strong repeated-script signals."
}
```

Risk levels:

```text
low
medium
high
critical
```

Risk model metadata and V1.5 topic risk fields:

`risk_model_version` is active in current MVP visualization/report responses and should remain backward-compatible. V1.5 adds deterministic topic-level risk fields using current mock pipeline outputs. V2 topic-window fields remain future work.

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

Rules:

- `risk_model_version` identifies the scoring model used for the result. V1 remains `v1_static_mvp`; V1.5 topic-level output uses `v1_5_topic_risk_mvp`.
- `topic_risks` is the V1.5 per-topic risk output.
- `real_crisis_risk` and `manipulation_risk` are V1.5 aggregate scores from 0 to 100.
- `risk_explanation` should be deterministic and schema-compatible.
- MongoDB document keys must remain strings.

## 12.1 Analysis Result V1.5 Extension

`AnalysisResultResponse` keeps the original `risk` object for backward compatibility and may additionally include V1.5 topic-level risk fields when topic clusters exist:

```json
{
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

Rules:

- These fields are additive and must not remove or rename the legacy `risk.risk_score` and `risk.risk_level` fields.
- `topic_risks` and `top_risk_topics` use the `TopicRiskScore` shape defined above.
- Missing optional inputs should produce deterministic safe fallback values instead of crashing.

## 13. Visualization Response

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

## 14. Public Opinion Report

Normalized report output is returned by `POST /api/v1/summary/generate` and `POST /api/v1/recommendation/generate`.

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
    "负面议题：Product quality issues：356条评论，平均情绪-0.74"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks."
  ],
  "suspected_bot_signals": [
    "重复话术或疑似协同信号较高：疑似机器人评论影响为39%。"
  ],
  "recommended_actions": [
    "启动危机响应负责人机制，并在24小时内准备对外更新窗口。"
  ],
  "suggested_public_response": "我们已注意到近期关于Product quality issues的讨论。我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，我们会基于事实进行核查和处理。",
  "generated_from_mock_pipeline": true
}
```

Rules:

- `report_language` defaults to `zh-CN`; `en-US` is optional.
- `risk_level` stays as the raw English enum: `low`, `medium`, `high`, or `critical`.
- `risk_level_label` is a display-only label. For `zh-CN`, use `低风险`, `中等风险`, `高风险`, or `严重风险`.
- `risk_model_version` identifies the active scoring model, currently `v1_static_mvp`.
- V1.5 responses may set `risk_model_version` to `v1_5_topic_risk_mvp` and include `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.
- Chinese report templates should translate risk wording for display inside text, but not change the raw `risk_level` value.
- Representative comments preserve original text and are not translated by the report builder.
- Report generation is deterministic and template-based; it does not call external LLM APIs.

## 15. Recommendation Response

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
    "负面情绪占比较高，当前为72%。"
  ],
  "main_risk_factors": [
    "负面情绪占比较高，当前为72%。"
  ],
  "top_negative_topics": [
    "Product quality issues：356条评论，平均情绪-0.74"
  ],
  "representative_comments": [
    "This product broke after two weeks."
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
