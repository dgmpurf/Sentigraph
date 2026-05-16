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


class PlaceholderLLMProvider(BaseLLMProvider):
    """Future real provider placeholder that never performs network calls."""

    required_credentials: ClassVar[tuple[str, ...]] = ()

    def expand_keywords(self, keyword: str, language: str = "auto") -> KeywordExpansionResult:
        self._raise_unavailable()

    def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
        self._raise_unavailable()

    def extract_topics(self, texts: Sequence[str], language: str = "auto") -> TopicExtractionResult:
        self._raise_unavailable()

    def summarize_cluster(
        self,
        comments: Sequence[str | dict[str, Any]],
        language: str = "zh-CN",
    ) -> ClusterSummaryResult:
        self._raise_unavailable()

    def generate_report(self, context: dict[str, Any], language: str = "zh-CN") -> LLMReportResult:
        self._raise_unavailable()

    def generate_recommendations(
        self,
        context: dict[str, Any],
        user_type: str = "brand",
        language: str = "zh-CN",
    ) -> LLMRecommendationResult:
        self._raise_unavailable()

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

    def _raise_unavailable(self) -> None:
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
        raise LLMProviderNotEnabledError(
            f"{self.display_name} real integration is a placeholder and is not implemented yet.",
            category="provider_not_enabled",
            provider=self.provider_id,
        )
