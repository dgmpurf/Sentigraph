from __future__ import annotations

from app.schemas.keyword import KeywordExpandRequest, KeywordExpandResponse
from app.services.llm.base_provider import BaseLLMProvider
from app.services.llm.errors import LLMProviderError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.provider_factory import get_llm_provider


def build_keyword_expansion(payload: KeywordExpandRequest) -> KeywordExpandResponse:
    """Expand keywords through the mock-first LLM provider interface."""

    keyword = payload.keyword.strip()
    language = payload.language or "auto"
    provider = _safe_keyword_provider()
    try:
        expansion = provider.expand_keywords(keyword, language=language)
    except LLMProviderError:
        expansion = MockProvider().expand_keywords(keyword, language=language)

    return KeywordExpandResponse(
        original_keyword=expansion.original_keyword,
        expanded_keywords=expansion.expanded_keywords,
        search_queries=expansion.search_queries,
    )


def _safe_keyword_provider() -> BaseLLMProvider:
    try:
        provider = get_llm_provider()
    except LLMProviderError:
        return MockProvider()
    if provider.provider_id != MockProvider.provider_id:
        return MockProvider()
    return provider
