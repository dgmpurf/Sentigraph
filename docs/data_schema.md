# Sentigraph Data Schema

This document defines the core data structures for Sentigraph.

All schemas should be implemented as Pydantic models in:

```text
backend/app/schemas/
```

MongoDB document keys must always be strings.

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
  "platform": "reddit",
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
  "platform": "reddit",
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
  "platforms": ["reddit"],
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
  "platforms": ["reddit", "weibo"],
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
  "platform": "reddit",
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

## 13. Visualization Response

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

## 14. Recommendation Response

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
