from __future__ import annotations

from collections import Counter
from typing import Any, Sequence

from app.services.llm.base_provider import BaseLLMProvider
from app.services.llm.schemas import (
    ClusterSummaryResult,
    KeywordExpansionResult,
    LLMRecommendationResult,
    LLMReportResult,
    LLMSentimentResult,
    ProviderHealth,
    TopicExtractionResult,
    TopicItem,
)


NEGATIVE_TERMS = {
    "bad",
    "broken",
    "complaint",
    "defect",
    "delay",
    "issue",
    "problem",
    "recall",
    "terrible",
    "\u8d28\u91cf",
    "\u95ee\u9898",
    "\u6295\u8bc9",
    "\u5931\u671b",
    "\u5dee",
}
POSITIVE_TERMS = {
    "good",
    "great",
    "love",
    "resolved",
    "support",
    "trust",
    "\u6ee1\u610f",
    "\u652f\u6301",
    "\u4fe1\u4efb",
    "\u89e3\u51b3",
}
TOPIC_TERMS: dict[str, tuple[str, ...]] = {
    "Product quality issues": ("quality", "broken", "defect", "issue", "problem", "\u8d28\u91cf", "\u95ee\u9898"),
    "Official response": ("response", "official", "statement", "\u56de\u5e94", "\u5b98\u65b9", "\u58f0\u660e"),
    "Pricing and policy": ("price", "pricing", "discount", "policy", "\u4ef7\u683c", "\u964d\u4ef7", "\u653f\u7b56"),
    "Coordinated amplification": ("script", "repeat", "coordinated", "\u91cd\u590d", "\u5237\u5c4f", "\u6c34\u519b"),
}


class MockProvider(BaseLLMProvider):
    """Deterministic offline LLM stand-in used by the MVP."""

    provider_id = "mock"
    display_name = "Mock LLM Provider"

    def expand_keywords(self, keyword: str, language: str = "auto") -> KeywordExpansionResult:
        normalized = keyword.strip()
        if not normalized:
            normalized = "public opinion"

        language_hint = _language_hint(normalized, language)
        lowered = normalized.lower()

        if lowered == "tesla" or "\u7279\u65af\u62c9" in normalized:
            expanded = _tesla_expansion(normalized)
            queries = [
                "Tesla problem",
                "Tesla recall",
                "Tesla price cut",
                "\u7279\u65af\u62c9 \u53ec\u56de",
                "\u7279\u65af\u62c9 \u964d\u4ef7",
                "\u7279\u65af\u62c9 \u81ea\u52a8\u9a7e\u9a76",
            ]
        elif lowered == "bilibili" or "b\u7ad9" in lowered or "\u54d4\u54e9\u54d4\u54e9" in normalized:
            expanded = _bilibili_expansion(normalized)
            queries = [
                "Bilibili public opinion",
                "Bilibili comments",
                "B\u7ad9 UP\u4e3b",
                "\u54d4\u54e9\u54d4\u54e9 \u5f39\u5e55",
                "B\u7ad9 \u89c6\u9891\u8bc4\u8bba",
            ]
        elif language_hint == "zh-CN":
            expanded = [
                normalized,
                f"{normalized} \u8206\u60c5",
                f"{normalized} \u6295\u8bc9",
                f"{normalized} \u4e89\u8bae",
                f"{normalized} \u56de\u5e94",
                f"{normalized} \u98ce\u9669",
            ]
            queries = [
                f"{normalized} \u8206\u60c5",
                f"{normalized} \u6295\u8bc9",
                f"{normalized} \u4e89\u8bae",
                f"{normalized} \u5b98\u65b9\u56de\u5e94",
            ]
        else:
            expanded = [
                normalized,
                f"{normalized} public opinion",
                f"{normalized} complaints",
                f"{normalized} controversy",
                f"{normalized} response",
                f"{normalized} \u8206\u60c5",
            ]
            queries = [
                f"{normalized} problem",
                f"{normalized} complaints",
                f"{normalized} controversy",
                f"{normalized} response",
                f"{normalized} \u8206\u60c5",
            ]

        return KeywordExpansionResult(
            original_keyword=normalized,
            expanded_keywords=_dedupe(expanded),
            search_queries=_dedupe(queries),
            language=language,
            provider=self.provider_id,
        )

    def analyze_sentiment(self, text: str, language: str = "auto") -> LLMSentimentResult:
        normalized = text.lower()
        negative_hits = _count_hits(normalized, NEGATIVE_TERMS)
        positive_hits = _count_hits(normalized, POSITIVE_TERMS)
        score = _clamp((positive_hits - negative_hits) / 4)

        if score <= -0.15:
            sentiment = "negative"
            stance = "opposing"
            tags = ["anger", "disappointment"]
        elif score >= 0.15:
            sentiment = "positive"
            stance = "supportive"
            tags = ["trust", "supportive"]
        elif positive_hits and negative_hits:
            sentiment = "mixed"
            stance = "mixed"
            tags = ["uncertainty", "questioning"]
        else:
            sentiment = "neutral"
            stance = "neutral"
            tags = ["uncertainty"]

        return LLMSentimentResult(
            sentiment=sentiment,
            sentiment_score=round(score, 4),
            emotion_tags=tags,
            stance=stance,
            confidence=round(min(0.95, 0.6 + 0.08 * (positive_hits + negative_hits)), 4),
            reason="Deterministic mock provider used keyword sentiment signals only.",
            language=language,
            provider=self.provider_id,
        )

    def extract_topics(self, texts: Sequence[str], language: str = "auto") -> TopicExtractionResult:
        buckets: Counter[str] = Counter()
        keyword_hits: dict[str, set[str]] = {topic: set() for topic in TOPIC_TERMS}

        for text in texts:
            lowered = str(text).lower()
            assigned = "General discussion"
            for topic, terms in TOPIC_TERMS.items():
                hits = [term for term in terms if term in lowered]
                if hits:
                    assigned = topic
                    keyword_hits[topic].update(hits[:3])
                    break
            buckets[assigned] += 1

        if not buckets:
            buckets["General discussion"] = 0

        topics = [
            TopicItem(
                topic=topic,
                summary=f"{count} item(s) grouped by deterministic mock topic rules.",
                count=count,
                keywords=sorted(keyword_hits.get(topic, set()))[:5],
            )
            for topic, count in buckets.most_common()
        ]
        return TopicExtractionResult(topics=topics, language=language, provider=self.provider_id)

    def summarize_cluster(
        self,
        comments: Sequence[str | dict[str, Any]],
        language: str = "zh-CN",
    ) -> ClusterSummaryResult:
        texts = [_comment_text(comment) for comment in comments if _comment_text(comment)]
        topics = self.extract_topics(texts, language=language).topics
        leading_topic = topics[0].topic if topics else "General discussion"
        key_terms = topics[0].keywords if topics else []
        if language == "en-US":
            summary = f"{len(texts)} public comment(s) mainly discuss {leading_topic.lower()}."
        else:
            summary = f"{len(texts)}\u6761\u516c\u5f00\u8bc4\u8bba\u4e3b\u8981\u805a\u7126\u4e8e{leading_topic}\u3002"
        return ClusterSummaryResult(
            summary=summary,
            key_terms=key_terms,
            comment_count=len(texts),
            language=language,
            provider=self.provider_id,
        )

    def generate_report(self, context: dict[str, Any], language: str = "zh-CN") -> LLMReportResult:
        project_id = str(context.get("project_id", "offline_project"))
        risk_level = str(context.get("risk_level", context.get("risk", {}).get("risk_level", "medium")))
        risk_score = context.get("risk_score", context.get("risk", {}).get("risk_score", 50))
        keyword = str(context.get("keyword", "monitored topic"))

        if language == "en-US":
            summary = f"Mock LLM report for {project_id}: {keyword} is currently assessed as {risk_level} risk."
            response = "Acknowledge the public concern, share verified facts, and keep updates on official channels."
            findings = [f"Risk score: {risk_score}", f"Risk level: {risk_level}", "Generated offline by MockProvider."]
            actions = ["Assign an owner.", "Prepare a factual FAQ.", "Monitor the next update window."]
        else:
            summary = (
                f"\u6a21\u62dfLLM\u62a5\u544a\uff1a\u9879\u76ee{project_id}\u4e2d"
                f"\u300c{keyword}\u300d\u5f53\u524d\u8bc4\u4f30\u4e3a{risk_level}\u98ce\u9669\u3002"
            )
            response = "\u5df2\u5173\u6ce8\u76f8\u5173\u8ba8\u8bba\uff0c\u5c06\u57fa\u4e8e\u5df2\u6838\u5b9e\u4fe1\u606f\u6301\u7eed\u66f4\u65b0\u3002"
            findings = [f"\u98ce\u9669\u5206\uff1a{risk_score}", f"\u98ce\u9669\u7b49\u7ea7\uff1a{risk_level}", "\u7531MockProvider\u79bb\u7ebf\u751f\u6210\u3002"]
            actions = [
                "\u6307\u5b9a\u8ddf\u8fdb\u8d1f\u8d23\u4eba\u3002",
                "\u51c6\u5907\u4e8b\u5b9e\u6027\u95ee\u7b54\u3002",
                "\u6301\u7eed\u89c2\u5bdf\u4e0b\u4e00\u4e2a\u66f4\u65b0\u7a97\u53e3\u3002",
            ]

        return LLMReportResult(
            overall_summary=summary,
            key_findings=findings,
            recommended_actions=actions,
            suggested_public_response=response,
            language=language,
            provider=self.provider_id,
            raw_context_summary={
                "project_id": project_id,
                "keyword": keyword,
                "risk_level": risk_level,
                "risk_score": risk_score,
            },
        )

    def generate_recommendations(
        self,
        context: dict[str, Any],
        user_type: str = "brand",
        language: str = "zh-CN",
    ) -> LLMRecommendationResult:
        risk_level = str(context.get("risk_level", context.get("risk", {}).get("risk_level", "medium")))
        escalation = "watch"
        if risk_level in {"high", "critical"}:
            escalation = "escalate"
        elif risk_level == "low":
            escalation = "monitor"

        if language == "en-US":
            recommendations = [
                "Keep responses factual and concise.",
                "Separate organic complaints from repeated-script signals.",
                "Prepare a follow-up update if risk increases.",
            ]
            strategy = "Use a calm public response and avoid unverified claims."
        else:
            recommendations = [
                "\u4fdd\u6301\u56de\u5e94\u4e8b\u5b9e\u5316\u4e14\u7b80\u660e\u3002",
                "\u533a\u5206\u771f\u5b9e\u6295\u8bc9\u4e0e\u91cd\u590d\u8bdd\u672f\u4fe1\u53f7\u3002",
                "\u82e5\u98ce\u9669\u5347\u9ad8\uff0c\u51c6\u5907\u540e\u7eed\u66f4\u65b0\u3002",
            ]
            strategy = "\u91c7\u7528\u51b7\u9759\u3001\u53ef\u6838\u9a8c\u7684\u5bf9\u5916\u56de\u5e94\u3002"

        return LLMRecommendationResult(
            recommendations=recommendations,
            response_strategy=strategy,
            escalation_level=escalation,
            user_type=user_type,
            language=language,
            provider=self.provider_id,
        )

    def health_check(self) -> ProviderHealth:
        return ProviderHealth(
            provider=self.provider_id,
            ok=True,
            real_calls_enabled=False,
            configured=True,
            message="MockProvider is deterministic, offline, and requires no API keys.",
        )


def _count_hits(text: str, terms: set[str]) -> int:
    return sum(1 for term in terms if term in text)


def _clamp(value: float, minimum: float = -1.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


def _language_hint(keyword: str, language: str) -> str:
    requested = (language or "auto").strip()
    if requested == "zh-CN":
        return "zh-CN"
    if _contains_cjk(keyword):
        return "zh-CN"
    if requested == "en-US":
        return "en-US"
    return "en-US"


def _contains_cjk(value: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in value)


def _tesla_expansion(keyword: str) -> list[str]:
    if "\u7279\u65af\u62c9" in keyword:
        return [
            keyword,
            "Tesla",
            "Model Y",
            "Model 3",
            "\u7535\u52a8\u8f66",
            "\u81ea\u52a8\u9a7e\u9a76",
            "\u53ec\u56de",
            "\u964d\u4ef7",
        ]
    return [
        keyword,
        "\u7279\u65af\u62c9",
        "Model Y",
        "Model 3",
        "\u7535\u52a8\u8f66",
        "\u81ea\u52a8\u9a7e\u9a76",
        "\u53ec\u56de",
        "\u964d\u4ef7",
    ]


def _bilibili_expansion(keyword: str) -> list[str]:
    if keyword.lower() == "bilibili":
        return [
            keyword,
            "B\u7ad9",
            "\u54d4\u54e9\u54d4\u54e9",
            "UP\u4e3b",
            "\u5f39\u5e55",
            "\u89c6\u9891\u8bc4\u8bba",
        ]
    return [
        keyword,
        "Bilibili",
        "B\u7ad9",
        "\u54d4\u54e9\u54d4\u54e9",
        "UP\u4e3b",
        "\u5f39\u5e55",
        "\u89c6\u9891\u8bc4\u8bba",
    ]


def _dedupe(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _comment_text(comment: str | dict[str, Any]) -> str:
    if isinstance(comment, dict):
        return str(comment.get("content") or comment.get("text") or "").strip()
    return str(comment).strip()
