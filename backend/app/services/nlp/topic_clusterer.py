import os
from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol

from app.core.environment import load_project_env
from app.schemas.analysis import SentimentResult, TopicCluster
from app.schemas.comment import CleanComment
from app.services.llm.errors import LLMProviderError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.provider_factory import get_llm_provider


TEMPLATE_TOPIC_SUMMARY_MODE = "template"
MOCK_LLM_TOPIC_SUMMARY_MODE = "mock_llm"
FUTURE_REAL_LLM_TOPIC_SUMMARY_MODE = "future_real_llm"
SUPPORTED_TOPIC_SUMMARY_MODES = {
    TEMPLATE_TOPIC_SUMMARY_MODE,
    MOCK_LLM_TOPIC_SUMMARY_MODE,
    FUTURE_REAL_LLM_TOPIC_SUMMARY_MODE,
}
TOPIC_SUMMARY_MODE_ALIASES = {
    "rule": TEMPLATE_TOPIC_SUMMARY_MODE,
    "rule_based": TEMPLATE_TOPIC_SUMMARY_MODE,
    "rules": TEMPLATE_TOPIC_SUMMARY_MODE,
}
TOPIC_DEFINITIONS: dict[str, tuple[str, ...]] = {
    "Product quality issues": ("quality", "broken", "defect", "issue", "problem", "\u8d28\u91cf", "\u95ee\u9898"),
    "Delayed official response": ("response", "respond", "official", "silence", "\u56de\u5e94", "\u5b98\u65b9"),
    "Coordinated amplification": (
        "coordinated",
        "repeating",
        "script",
        "attack",
        "\u91cd\u590d",
        "\u5237\u5c4f",
        "\u6c34\u519b",
    ),
    "Pricing and policy": ("price", "pricing", "discount", "\u964d\u4ef7", "\u4ef7\u683c"),
}


class EmbeddingProvider(Protocol):
    def embed(self, text: str) -> list[float]:
        ...


@dataclass(frozen=True)
class SimpleKeywordEmbeddingProvider:
    dimensions: tuple[str, ...] = tuple(TOPIC_DEFINITIONS.keys())

    def embed(self, text: str) -> list[float]:
        lowered = text.lower()
        vector: list[float] = []
        for topic in self.dimensions:
            terms = TOPIC_DEFINITIONS[topic]
            hits = sum(1 for term in terms if term in lowered)
            vector.append(float(hits))
        return vector


class TopicClusterer:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider | None = None,
        summary_mode: str | None = None,
    ) -> None:
        self.embedding_provider = embedding_provider or SimpleKeywordEmbeddingProvider()
        self.dimensions = tuple(
            getattr(self.embedding_provider, "dimensions", tuple(TOPIC_DEFINITIONS.keys()))
        )
        self.summary_mode = get_topic_summary_mode(summary_mode)

    def cluster(
        self,
        comments: list[CleanComment],
        sentiment_results: list[SentimentResult] | None = None,
    ) -> list[TopicCluster]:
        sentiment_by_comment = {
            result.comment_id: result.sentiment_score for result in sentiment_results or []
        }
        buckets: dict[str, list[CleanComment]] = defaultdict(list)

        for comment in comments:
            topic = self._assign_topic(comment.clean_text)
            buckets[topic].append(comment)

        clusters: list[TopicCluster] = []
        for index, (topic, topic_comments) in enumerate(sorted(buckets.items()), start=1):
            total_count = sum(comment.duplicate_count for comment in topic_comments)
            scores = [
                sentiment_by_comment[comment.clean_comment_id]
                for comment in topic_comments
                if comment.clean_comment_id in sentiment_by_comment
            ]
            average_score = sum(scores) / len(scores) if scores else 0.0
            representatives = [comment.clean_text for comment in topic_comments if comment.clean_text.strip()][:2]
            clusters.append(
                TopicCluster(
                    cluster_id=f"topic_{index:03d}",
                    topic=topic,
                    summary=self._summary(topic, total_count, topic_comments),
                    comment_count=total_count,
                    average_sentiment_score=round(average_score, 4),
                    representative_comments=representatives,
                )
            )
        return sorted(clusters, key=lambda cluster: cluster.comment_count, reverse=True)

    def _assign_topic(self, text: str) -> str:
        vector = self.embedding_provider.embed(text)
        if not vector or max(vector) <= 0 or not self.dimensions:
            return "General discussion"
        best_index = min(vector.index(max(vector)), len(self.dimensions) - 1)
        return self.dimensions[best_index]

    def _summary(self, topic: str, count: int, comments: list[CleanComment]) -> str:
        if self.summary_mode == MOCK_LLM_TOPIC_SUMMARY_MODE:
            return self._mock_llm_summary(topic, count, comments)
        return self._template_summary(topic, count)

    def _mock_llm_summary(self, topic: str, count: int, comments: list[CleanComment]) -> str:
        try:
            payload = [
                {"content": comment.clean_text}
                for comment in comments
                if comment.clean_text.strip()
            ]
            if not payload:
                return self._template_summary(topic, count)
            provider = get_llm_provider()
            if getattr(provider, "provider_id", None) != "mock":
                provider = MockProvider()
            summary = provider.summarize_cluster(
                payload,
                language="zh-CN",
            )
            return summary.summary or self._template_summary(topic, count)
        except LLMProviderError:
            return self._template_summary(topic, count)
        except Exception:
            return self._template_summary(topic, count)

    @staticmethod
    def _template_summary(topic: str, count: int) -> str:
        if topic == "General discussion":
            return f"{count} comment(s) discuss the monitored keyword without a strong topic signal."
        return f"{count} comment(s) are grouped under {topic.lower()} by deterministic keyword embeddings."


def get_topic_summary_mode(mode: str | None = None) -> str:
    load_project_env()
    raw_mode = mode if mode is not None else os.getenv("TOPIC_SUMMARY_MODE", TEMPLATE_TOPIC_SUMMARY_MODE)
    normalized = (raw_mode or TEMPLATE_TOPIC_SUMMARY_MODE).strip().lower()
    normalized = TOPIC_SUMMARY_MODE_ALIASES.get(normalized, normalized)
    if normalized not in SUPPORTED_TOPIC_SUMMARY_MODES:
        return TEMPLATE_TOPIC_SUMMARY_MODE
    return normalized
