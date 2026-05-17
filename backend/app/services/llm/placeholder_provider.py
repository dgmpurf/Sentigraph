from __future__ import annotations

import os
from typing import Any, ClassVar, Sequence

from app.services.llm.base_provider import BaseLLMProvider
from app.services.llm.errors import LLMProviderConfigError, LLMProviderNotEnabledError
from app.services.llm.schemas import (
    ClusterSummaryResult,
    KeywordExpansionResult,
    LLMRecommendationResult,
    LLMReportResult,
    LLMSentimentResult,
    ProviderHealth,
    TopicExtractionResult,
)
from app.services.llm.usage_guardrails import check_call_allowed
from app.schemas.selector_repair import SelectorRepairRequest, SelectorRepairSuggestion


class PlaceholderLLMProvider(BaseLLMProvider):
    """Future real provider placeholder that never performs network calls."""

    required_credentials: ClassVar[tuple[str, ...]] = ()

    def expand_keywords(self, keyword: str, language: str = "auto") -> KeywordExpansionResult:
        self._raise_unavailable("expand_keywords", len(keyword))

    def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
        self._raise_unavailable("analyze_sentiment", len(text))

    def extract_topics(self, texts: Sequence[str], language: str = "auto") -> TopicExtractionResult:
        self._raise_unavailable("extract_topics", sum(len(str(text)) for text in texts))

    def summarize_cluster(
        self,
        comments: Sequence[str | dict[str, Any]],
        language: str = "zh-CN",
    ) -> ClusterSummaryResult:
        self._raise_unavailable("summarize_cluster", sum(len(str(comment)) for comment in comments))

    def generate_report(self, context: dict[str, Any], language: str = "zh-CN") -> LLMReportResult:
        self._raise_unavailable("generate_report", len(str(context)))

    def generate_recommendations(
        self,
        context: dict[str, Any],
        user_type: str = "brand",
        language: str = "zh-CN",
    ) -> LLMRecommendationResult:
        self._raise_unavailable("generate_recommendations", len(str(context)))

    def suggest_selector_repair(
        self,
        request: SelectorRepairRequest,
    ) -> SelectorRepairSuggestion:
        self._raise_unavailable(
            "suggest_selector_repair",
            len(request.sanitized_html) + len(request.parser_error_summary or ""),
        )

    def health_check(self) -> ProviderHealth:
        if not self.real_calls_enabled:
            return ProviderHealth(
                provider=self.provider_id,
                ok=False,
                real_calls_enabled=False,
                configured=self._has_required_credentials(),
                message=f"{self.display_name} is a future placeholder; real calls are disabled.",
                error_category="provider_not_enabled",
            )
        if not self._has_required_credentials():
            return ProviderHealth(
                provider=self.provider_id,
                ok=False,
                real_calls_enabled=True,
                configured=False,
                message=f"{self.display_name} credentials are missing.",
                error_category="not_configured",
            )
        return ProviderHealth(
            provider=self.provider_id,
            ok=False,
            real_calls_enabled=True,
            configured=True,
            message=f"{self.display_name} credentials are present, but real integration is not implemented.",
            error_category="provider_not_enabled",
        )

    def supports_real_calls(self) -> bool:
        return False

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return cls.required_credentials

    def credential_presence(self) -> dict[str, bool]:
        return {name: bool(os.getenv(name, "").strip()) for name in self.required_credentials}

    def _has_required_credentials(self) -> bool:
        return all(self.credential_presence().values())

    def _raise_unavailable(self, operation: str, input_chars: int) -> None:
        if not self.real_calls_enabled:
            raise LLMProviderNotEnabledError(
                f"{self.display_name} real calls are disabled. Use MockProvider for the offline MVP.",
                provider=self.provider_id,
            )
        if not self._has_required_credentials():
            raise LLMProviderConfigError(
                f"{self.display_name} credentials are not configured.",
                category="not_configured",
                provider=self.provider_id,
            )
        decision = check_call_allowed(self.provider_id, operation, input_chars)
        if not decision.allowed:
            raise LLMProviderNotEnabledError(
                f"{self.display_name} request blocked by LLM guardrail: {decision.reason_category}.",
                category=decision.reason_category or "guardrail_blocked",
                provider=self.provider_id,
            )
        raise LLMProviderNotEnabledError(
            f"{self.display_name} real integration is a placeholder and is not implemented yet.",
            category="provider_not_enabled",
            provider=self.provider_id,
        )
