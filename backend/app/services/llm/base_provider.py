from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar, Sequence

from app.services.llm.schemas import (
    ClusterSummaryResult,
    KeywordExpansionResult,
    LLMRecommendationResult,
    LLMReportResult,
    LLMSentimentResult,
    ProviderHealth,
    TopicExtractionResult,
)
from app.schemas.selector_repair import SelectorRepairRequest, SelectorRepairSuggestion


class BaseLLMProvider(ABC):
    """Common interface for future LLM-backed assistance.

    Implementations must not print secrets. Real provider placeholders must not
    make network calls until explicit future integration work enables them.
    """

    provider_id: ClassVar[str]
    display_name: ClassVar[str]

    def __init__(self, *, real_calls_enabled: bool = False) -> None:
        self.real_calls_enabled = real_calls_enabled

    @abstractmethod
    def expand_keywords(self, keyword: str, language: str = "auto") -> KeywordExpansionResult:
        """Return related keywords and search query suggestions."""

    @abstractmethod
    def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
        """Analyze sentiment for a short text sample."""

    @abstractmethod
    def extract_topics(self, texts: Sequence[str], language: str = "auto") -> TopicExtractionResult:
        """Extract deterministic topic labels from text samples."""

    @abstractmethod
    def summarize_cluster(
        self,
        comments: Sequence[str | dict[str, Any]],
        language: str = "zh-CN",
    ) -> ClusterSummaryResult:
        """Summarize a cluster of public comments."""

    @abstractmethod
    def generate_report(self, context: dict[str, Any], language: str = "zh-CN") -> LLMReportResult:
        """Generate a report draft from already-normalized context."""

    @abstractmethod
    def generate_recommendations(
        self,
        context: dict[str, Any],
        user_type: str = "brand",
        language: str = "zh-CN",
    ) -> LLMRecommendationResult:
        """Generate response recommendations from already-normalized context."""

    @abstractmethod
    def suggest_selector_repair(
        self,
        request: SelectorRepairRequest,
    ) -> SelectorRepairSuggestion:
        """Suggest selector candidates from sanitized public fixture HTML."""

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider=self.provider_id,
            ok=True,
            real_calls_enabled=self.real_calls_enabled,
            configured=True,
            message=f"{self.display_name} provider is available.",
        )

    @classmethod
    def get_required_credentials(cls) -> tuple[str, ...]:
        return ()

    def supports_real_calls(self) -> bool:
        return False
