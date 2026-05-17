import os
from collections import Counter

from app.core.environment import load_project_env
from app.schemas.analysis import SentimentResult, SentimentSummary
from app.schemas.comment import CleanComment
from app.services.llm.errors import LLMProviderError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.provider_factory import get_llm_provider
from app.services.llm.schemas import LLMSentimentResult


RULE_BASED_MODE = "rule_based"
MOCK_LLM_MODE = "mock_llm"
FUTURE_REAL_LLM_MODE = "future_real_llm"
SUPPORTED_SENTIMENT_ANALYZER_MODES = {
    RULE_BASED_MODE,
    MOCK_LLM_MODE,
    FUTURE_REAL_LLM_MODE,
}
MODE_ALIASES = {
    "mock": RULE_BASED_MODE,
    "rule": RULE_BASED_MODE,
    "rules": RULE_BASED_MODE,
}

NEGATIVE_TERMS = {
    "bad",
    "broken",
    "complaint",
    "complaints",
    "defect",
    "defects",
    "delay",
    "delayed",
    "issue",
    "issues",
    "problem",
    "problems",
    "recall",
    "serious",
    "terrible",
    "worse",
    "\u8d28\u91cf",
    "\u95ee\u9898",
    "\u6295\u8bc9",
    "\u5931\u671b",
    "\u56de\u5e94",
    "\u5dee",
}
POSITIVE_TERMS = {
    "good",
    "great",
    "love",
    "resolved",
    "support",
    "trust",
    "works",
    "\u6ee1\u610f",
    "\u652f\u6301",
    "\u4fe1\u4efb",
    "\u89e3\u51b3",
}
MOCKING_TERMS = {
    "coordinated",
    "repeating",
    "script",
    "attack",
    "\u6c34\u519b",
    "\u5237\u5c4f",
    "\u91cd\u590d",
}


def get_sentiment_analyzer_mode(mode: str | None = None) -> str:
    load_project_env()
    raw_mode = mode if mode is not None else os.getenv("SENTIMENT_ANALYZER_MODE", RULE_BASED_MODE)
    normalized = (raw_mode or RULE_BASED_MODE).strip().lower()
    normalized = MODE_ALIASES.get(normalized, normalized)
    if normalized not in SUPPORTED_SENTIMENT_ANALYZER_MODES:
        return RULE_BASED_MODE
    return normalized


def _token_hits(text: str, terms: set[str]) -> int:
    return sum(1 for term in terms if term in text)


def _clamp(value: float, minimum: float = -1.0, maximum: float = 1.0) -> float:
    return max(minimum, min(maximum, value))


class SentimentAnalyzer:
    def __init__(self, mode: str | None = None) -> None:
        self.mode = get_sentiment_analyzer_mode(mode)

    def analyze_comment(self, comment: CleanComment) -> SentimentResult:
        if self.mode == MOCK_LLM_MODE:
            return self._analyze_comment_with_mock_llm(comment)
        return self._analyze_comment_rule_based(comment)

    def _analyze_comment_rule_based(self, comment: CleanComment) -> SentimentResult:
        text = comment.clean_text.lower()
        negative_hits = _token_hits(text, NEGATIVE_TERMS)
        positive_hits = _token_hits(text, POSITIVE_TERMS)
        mocking_hits = _token_hits(text, MOCKING_TERMS)
        score = _clamp((positive_hits - negative_hits - mocking_hits * 0.5) / 4)

        if score <= -0.15:
            sentiment = "negative"
            stance = "opposing"
        elif score >= 0.15:
            sentiment = "positive"
            stance = "supportive"
        elif positive_hits and negative_hits:
            sentiment = "mixed"
            stance = "mixed"
        else:
            sentiment = "neutral"
            stance = "neutral"

        emotion_tags = self._emotion_tags(sentiment, text, mocking_hits)
        confidence = min(0.95, 0.58 + 0.08 * (positive_hits + negative_hits + mocking_hits))

        return SentimentResult(
            comment_id=comment.clean_comment_id,
            sentiment=sentiment,
            sentiment_score=round(score, 4),
            emotion_tags=emotion_tags,
            stance=stance,
            confidence=round(confidence, 4),
            reason=self._reason(sentiment, negative_hits, positive_hits, mocking_hits),
        )

    def _analyze_comment_with_mock_llm(self, comment: CleanComment) -> SentimentResult:
        try:
            provider = get_llm_provider()
            if getattr(provider, "provider_id", None) != "mock":
                provider = MockProvider()
            llm_result = provider.analyze_sentiment(comment.clean_text, language="auto")
            return self._llm_result_to_sentiment_result(comment, llm_result)
        except LLMProviderError:
            return self._analyze_comment_rule_based(comment)
        except Exception:
            return self._analyze_comment_rule_based(comment)

    def analyze(self, comments: list[CleanComment]) -> list[SentimentResult]:
        return [self.analyze_comment(comment) for comment in comments]

    @staticmethod
    def summarize(results: list[SentimentResult]) -> SentimentSummary:
        if not results:
            return SentimentSummary(
                positive_ratio=0.0,
                neutral_ratio=0.0,
                negative_ratio=0.0,
                average_sentiment_score=0.0,
            )
        counts = Counter(result.sentiment for result in results)
        total = len(results)
        neutral_count = counts["neutral"] + counts["mixed"]
        average_score = sum(result.sentiment_score for result in results) / total
        return SentimentSummary(
            positive_ratio=round(counts["positive"] / total, 4),
            neutral_ratio=round(neutral_count / total, 4),
            negative_ratio=round(counts["negative"] / total, 4),
            average_sentiment_score=round(average_score, 4),
        )

    @staticmethod
    def _emotion_tags(sentiment: str, text: str, mocking_hits: int) -> list[str]:
        if mocking_hits:
            return ["mocking", "questioning"]
        if sentiment == "negative":
            if "trust" in text or "\u4fe1\u4efb" in text:
                return ["distrust", "disappointment"]
            return ["anger", "disappointment"]
        if sentiment == "positive":
            return ["trust", "supportive"]
        if sentiment == "mixed":
            return ["uncertainty", "questioning"]
        return ["uncertainty"]

    @staticmethod
    def _reason(sentiment: str, negative_hits: int, positive_hits: int, mocking_hits: int) -> str:
        if mocking_hits:
            return "Rule-based mock analysis detected repeated-script or coordination language."
        if sentiment == "negative":
            return f"Rule-based mock analysis found {negative_hits} negative signal(s)."
        if sentiment == "positive":
            return f"Rule-based mock analysis found {positive_hits} positive signal(s)."
        if sentiment == "mixed":
            return "Rule-based mock analysis found both positive and negative signals."
        return "Rule-based mock analysis found no strong polarity signal."

    @staticmethod
    def _llm_result_to_sentiment_result(
        comment: CleanComment,
        llm_result: LLMSentimentResult,
    ) -> SentimentResult:
        return SentimentResult(
            comment_id=comment.clean_comment_id,
            sentiment=llm_result.sentiment,
            sentiment_score=round(llm_result.sentiment_score, 4),
            emotion_tags=list(llm_result.emotion_tags),
            stance=llm_result.stance,
            confidence=round(llm_result.confidence, 4),
            reason=llm_result.reason,
        )


def analyze_sentiment(comments: list[CleanComment], mode: str | None = None) -> list[SentimentResult]:
    return SentimentAnalyzer(mode=mode).analyze(comments)
