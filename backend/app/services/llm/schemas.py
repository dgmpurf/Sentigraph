from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


ProviderId = Literal["mock", "openai", "deepseek", "qwen"]
SentimentLabel = Literal["positive", "negative", "neutral", "mixed"]


class ProviderHealth(BaseModel):
    provider: str
    ok: bool
    real_calls_enabled: bool
    configured: bool
    message: str
    error_category: str | None = None


class ProviderDiagnostics(BaseModel):
    provider_name: str
    real_calls_enabled: bool
    api_key_present: bool
    provider_status: str
    required_credentials: list[str] = Field(default_factory=list)
    credential_presence: dict[str, bool] = Field(default_factory=dict)


class KeywordExpansionResult(BaseModel):
    original_keyword: str
    expanded_keywords: list[str]
    search_queries: list[str]
    language: str = "auto"
    provider: str = "mock"


class LLMSentimentResult(BaseModel):
    sentiment: SentimentLabel
    sentiment_score: float
    emotion_tags: list[str] = Field(default_factory=list)
    stance: str = "neutral"
    confidence: float = 0.0
    reason: str
    language: str = "auto"
    provider: str = "mock"


class TopicItem(BaseModel):
    topic: str
    summary: str
    count: int
    keywords: list[str] = Field(default_factory=list)


class TopicExtractionResult(BaseModel):
    topics: list[TopicItem]
    language: str = "auto"
    provider: str = "mock"


class ClusterSummaryResult(BaseModel):
    summary: str
    key_terms: list[str] = Field(default_factory=list)
    comment_count: int = 0
    language: str = "zh-CN"
    provider: str = "mock"


class LLMReportResult(BaseModel):
    overall_summary: str
    key_findings: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    suggested_public_response: str
    language: str = "zh-CN"
    provider: str = "mock"
    generated_from_mock_provider: bool = True
    raw_context_summary: dict[str, Any] = Field(default_factory=dict)


class LLMRecommendationResult(BaseModel):
    recommendations: list[str]
    response_strategy: str
    escalation_level: str
    user_type: str = "brand"
    language: str = "zh-CN"
    provider: str = "mock"
