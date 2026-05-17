from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Sequence


RUBRIC_DIMENSIONS = (
    "completeness",
    "risk_explanation_quality",
    "actionability",
    "safety_professionalism",
    "language_formatting",
)
DIMENSION_MAX_SCORE = 20
PASS_THRESHOLD = 80
WARNING_THRESHOLD = 60


@dataclass(frozen=True)
class ReportQualityFinding:
    code: str
    dimension: str
    severity: str
    message: str
    points_deducted: int = 0


@dataclass(frozen=True)
class ReportQualityScore:
    dimension: str
    score: int
    max_score: int = DIMENSION_MAX_SCORE


@dataclass(frozen=True)
class ReportQualityRubricResult:
    total_score: int
    grade: str
    dimension_scores: dict[str, int]
    findings: list[ReportQualityFinding] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def finding_codes(self) -> list[str]:
        return [finding.code for finding in self.findings]


class _RubricAccumulator:
    def __init__(self) -> None:
        self.dimension_scores = {dimension: DIMENSION_MAX_SCORE for dimension in RUBRIC_DIMENSIONS}
        self.findings: list[ReportQualityFinding] = []
        self.missing_sections: list[str] = []

    def deduct(
        self,
        dimension: str,
        code: str,
        message: str,
        points: int,
        *,
        severity: str = "warning",
        missing_section: str | None = None,
    ) -> None:
        self.dimension_scores[dimension] = max(0, self.dimension_scores[dimension] - points)
        self.findings.append(
            ReportQualityFinding(
                code=code,
                dimension=dimension,
                severity=severity,
                message=message,
                points_deducted=points,
            )
        )
        if missing_section and missing_section not in self.missing_sections:
            self.missing_sections.append(missing_section)

    def result(self) -> ReportQualityRubricResult:
        total_score = max(0, min(100, sum(self.dimension_scores.values())))
        has_fail = any(finding.severity == "fail" for finding in self.findings)
        has_warning = bool(self.findings)
        if has_fail or total_score < WARNING_THRESHOLD:
            grade = "fail"
        elif has_warning or total_score < PASS_THRESHOLD:
            grade = "warning"
        else:
            grade = "pass"
        return ReportQualityRubricResult(
            total_score=total_score,
            grade=grade,
            dimension_scores=dict(self.dimension_scores),
            findings=list(self.findings),
            missing_sections=list(self.missing_sections),
            warnings=[finding.code for finding in self.findings if finding.severity == "warning"],
        )


def evaluate_report_quality(
    report: Any,
    *,
    markdown: str | None = None,
    expected_representative_comments: Sequence[str] | None = None,
    required_markdown_sections: Sequence[str] | None = None,
    markdown_expected_values: Sequence[str] | None = None,
) -> ReportQualityRubricResult:
    """Evaluate a generated public-opinion report with deterministic rule checks.

    The rubric is intentionally offline and rule-based. It does not call LLMs,
    inspect external sources, or store raw report text.
    """

    acc = _RubricAccumulator()
    generated_text = _generated_report_text(report)
    full_text = _full_report_text(report)

    _score_completeness(acc, report)
    _score_risk_explanation(acc, report, generated_text)
    _score_actionability(acc, report)
    _score_safety(acc, generated_text, full_text)
    _score_language_and_formatting(
        acc,
        report,
        generated_text,
        markdown=markdown,
        expected_representative_comments=expected_representative_comments,
        required_markdown_sections=required_markdown_sections,
        markdown_expected_values=markdown_expected_values,
    )
    return acc.result()


def _score_completeness(acc: _RubricAccumulator, report: Any) -> None:
    required = {
        "overall_summary": _text_value(report, "overall_summary"),
        "key_findings": _list_value(report, "key_findings"),
        "main_risk_factors": _list_value(report, "main_risk_factors"),
        "recommended_actions": _list_value(report, "recommended_actions"),
        "suggested_public_response": _text_value(report, "suggested_public_response"),
    }
    for section, value in required.items():
        present = bool(value) if isinstance(value, str) else bool(value)
        if not present:
            acc.deduct(
                "completeness",
                f"missing_{section}",
                f"Required report section is missing: {section}.",
                4 if section in {"recommended_actions", "suggested_public_response"} else 3,
                missing_section=section,
            )

    topic_risks_available = bool(_list_value(report, "topic_risks") or _text_value(report, "risk_explanation"))
    top_topics_present = bool(_list_value(report, "top_risk_topics") or _list_value(report, "top_negative_topics"))
    if topic_risks_available and not top_topics_present:
        acc.deduct(
            "completeness",
            "missing_top_risk_topics",
            "Topic risk data is present but top risk topics are not surfaced.",
            3,
            missing_section="top_risk_topics",
        )


def _score_risk_explanation(acc: _RubricAccumulator, report: Any, generated_text: str) -> None:
    risk_score = _field_value(report, "risk_score")
    risk_level = _text_value(report, "risk_level")
    risk_label = _text_value(report, "risk_level_label")
    risk_markers = [str(risk_score), risk_level, risk_label, "/100"]
    if not any(marker and marker in generated_text for marker in risk_markers):
        acc.deduct(
            "risk_explanation_quality",
            "risk_score_or_level_not_explained",
            "Report does not mention the risk score or risk level.",
            4,
        )

    if not _has_reason_signal(report, generated_text):
        acc.deduct(
            "risk_explanation_quality",
            "risk_driver_missing",
            "Report does not explain the primary reason the risk is elevated.",
            5,
        )

    top_topics = _list_value(report, "top_risk_topics")
    if top_topics and not any(_topic_name(topic) and _topic_name(topic) in generated_text for topic in top_topics):
        acc.deduct(
            "risk_explanation_quality",
            "top_risk_topic_not_referenced",
            "Report has top risk topics but does not reference them in the explanation.",
            4,
        )

    real_crisis = _field_value(report, "real_crisis_risk")
    manipulation = _field_value(report, "manipulation_risk")
    if real_crisis is not None and manipulation is not None:
        expected_numbers = {_score_marker(real_crisis), _score_marker(manipulation)}
        has_split_terms = _contains_any(
            generated_text.lower(),
            (
                "real-crisis",
                "real crisis",
                "manipulation",
                "repeated-script",
                "script",
                "\u5371\u673a",
                "\u64cd\u7eb5",
                "\u91cd\u590d",
            ),
        )
        if not (expected_numbers.issubset(set(_numbers_in_text(generated_text))) or has_split_terms):
            acc.deduct(
                "risk_explanation_quality",
                "crisis_manipulation_split_missing",
                "Report does not distinguish real-crisis and manipulation risk signals.",
                4,
            )


def _score_actionability(acc: _RubricAccumulator, report: Any) -> None:
    actions = _list_value(report, "recommended_actions")
    response = _text_value(report, "suggested_public_response")
    if len(actions) < 2:
        acc.deduct(
            "actionability",
            "vague_recommendations",
            "Recommended actions are missing or too sparse.",
            6,
        )
    elif not any(_is_specific_action(action) for action in actions):
        acc.deduct(
            "actionability",
            "vague_recommendations",
            "Recommended actions are too generic for operator use.",
            5,
        )

    if len(response.strip()) < 24:
        acc.deduct(
            "actionability",
            "vague_public_response",
            "Suggested public response is too short or vague.",
            5,
        )
    if _contains_any(response.lower(), ("guarantee", "solve everything", "fix everything", "never happen again")):
        acc.deduct(
            "actionability",
            "public_response_overpromises",
            "Suggested public response appears to overpromise beyond verified facts.",
            5,
        )


def _score_safety(acc: _RubricAccumulator, generated_text: str, full_text: str) -> None:
    if _looks_like_json_dump(generated_text):
        acc.deduct(
            "safety_professionalism",
            "raw_json_dump",
            "Generated report text appears to contain a raw JSON dump.",
            10,
            severity="fail",
        )
    if _contains_secret(full_text):
        acc.deduct(
            "safety_professionalism",
            "secret_or_api_key_exposed",
            "Report text appears to expose an API key, token, or secret marker.",
            10,
            severity="fail",
        )
    if _contains_private_data(full_text):
        acc.deduct(
            "safety_professionalism",
            "private_data_pattern",
            "Report text appears to contain private contact data.",
            7,
            severity="fail",
        )
    if _contains_unsupported_overclaim(generated_text):
        acc.deduct(
            "safety_professionalism",
            "unsupported_overclaim",
            "Report makes an unsupported legal or fraud conclusion.",
            8,
            severity="fail",
        )
    if _contains_aggressive_language(generated_text):
        acc.deduct(
            "safety_professionalism",
            "aggressive_or_accusatory_language",
            "Report uses aggressive or accusatory language.",
            5,
            severity="fail",
        )


def _score_language_and_formatting(
    acc: _RubricAccumulator,
    report: Any,
    generated_text: str,
    *,
    markdown: str | None,
    expected_representative_comments: Sequence[str] | None,
    required_markdown_sections: Sequence[str] | None,
    markdown_expected_values: Sequence[str] | None,
) -> None:
    language = _text_value(report, "report_language")
    if language == "zh-CN" and not _has_cjk(generated_text):
        acc.deduct(
            "language_formatting",
            "zh_cn_text_missing",
            "zh-CN report does not contain enough Chinese text.",
            5,
        )

    expected_comments = [comment for comment in expected_representative_comments or [] if comment]
    representative_comments = "\n".join(_list_value(report, "representative_comments"))
    missing_representatives = [comment for comment in expected_comments if comment not in representative_comments]
    if missing_representatives:
        acc.deduct(
            "language_formatting",
            "representative_comments_not_preserved",
            "Representative comments are not preserved in their original language.",
            5,
        )

    if markdown is not None:
        missing_sections = _missing_markdown_sections(
            markdown,
            report,
            required_markdown_sections=required_markdown_sections,
            expected_values=markdown_expected_values,
        )
        if missing_sections:
            acc.deduct(
                "language_formatting",
                "markdown_missing_sections",
                "Markdown export is missing expected report sections.",
                min(8, 2 * len(missing_sections)),
            )
            for section in missing_sections:
                if section not in acc.missing_sections:
                    acc.missing_sections.append(f"markdown:{section}")

    if _is_fragmented_report(generated_text):
        acc.deduct(
            "language_formatting",
            "report_too_fragmented",
            "Report text is too short or reads like disconnected fragments.",
            4,
        )


def _field_value(report: Any, field_name: str) -> Any:
    if isinstance(report, dict):
        return report.get(field_name)
    return getattr(report, field_name, None)


def _text_value(report: Any, field_name: str) -> str:
    value = _field_value(report, field_name)
    if value is None:
        return ""
    return str(value).strip()


def _list_value(report: Any, field_name: str) -> list[Any]:
    value = _field_value(report, field_name)
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _generated_report_text(report: Any) -> str:
    sections: list[str] = [
        _text_value(report, "overall_summary"),
        *_stringify_items(_list_value(report, "key_findings")),
        *_stringify_items(_list_value(report, "main_risk_factors")),
        *_stringify_items(_list_value(report, "top_negative_topics")),
        *_stringify_items(_list_value(report, "suspected_bot_signals")),
        *_stringify_items(_list_value(report, "recommended_actions")),
        _text_value(report, "suggested_public_response"),
        _text_value(report, "risk_explanation"),
    ]
    return "\n".join(section for section in sections if section)


def _full_report_text(report: Any) -> str:
    sections = [_generated_report_text(report), *_stringify_items(_list_value(report, "representative_comments"))]
    return "\n".join(section for section in sections if section)


def _stringify_items(items: Iterable[Any]) -> list[str]:
    values: list[str] = []
    for item in items:
        if hasattr(item, "model_dump"):
            values.append(" ".join(str(value) for value in item.model_dump().values() if value is not None))
        else:
            values.append(str(item))
    return [value.strip() for value in values if value and value.strip()]


def _topic_name(topic: Any) -> str:
    if hasattr(topic, "topic"):
        return str(topic.topic)
    if isinstance(topic, dict):
        return str(topic.get("topic") or "")
    return ""


def _has_reason_signal(report: Any, generated_text: str) -> bool:
    if _list_value(report, "main_risk_factors"):
        return True
    return _contains_any(
        generated_text.lower(),
        (
            "negative",
            "risk",
            "topic",
            "bot",
            "signal",
            "driver",
            "driven",
            "concern",
            "\u98ce\u9669",
            "\u8bdd\u9898",
            "\u8d1f\u9762",
            "\u4fe1\u53f7",
        ),
    )


def _score_marker(value: Any) -> str:
    try:
        return f"{float(value):.1f}"
    except (TypeError, ValueError):
        return str(value)


def _numbers_in_text(value: str) -> list[str]:
    return re.findall(r"\b\d+(?:\.\d+)?\b", value)


def _contains_any(value: str, terms: Sequence[str]) -> bool:
    return any(term and term in value for term in terms)


def _is_specific_action(action: Any) -> bool:
    text = str(action).strip()
    lowered = text.lower()
    if len(text) < 12:
        return False
    if lowered in {"monitor", "follow up", "respond", "handle it", "keep watching"}:
        return False
    return True


def _looks_like_json_dump(value: str) -> bool:
    return bool(re.search(r"\{[^{}\n]{0,200}:[^{}\n]{0,200}\}", value))


def _contains_secret(value: str) -> bool:
    return bool(
        re.search(
            r"(sk-[A-Za-z0-9_-]{8,}|OPENAI_API_KEY|DEEPSEEK_API_KEY|QWEN_API_KEY|api[_-]?key|password|bearer\s+[A-Za-z0-9._-]+|token\s*[:=])",
            value,
            flags=re.IGNORECASE,
        )
    )


def _contains_private_data(value: str) -> bool:
    return bool(
        re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", value)
        or re.search(r"\b1[3-9]\d{9}\b", value)
    )


def _contains_unsupported_overclaim(value: str) -> bool:
    lowered = value.lower()
    return _contains_any(
        lowered,
        (
            "confirmed fraud",
            "proven fraud",
            "fraud confirmed",
            "confirmed scam",
            "guilty of fraud",
            "criminal conduct is confirmed",
            "\u5df2\u8bc1\u5b9e\u6b3a\u8bc8",
            "\u786e\u8ba4\u9020\u5047",
            "\u5b9e\u9524\u8bc8\u9a97",
            "\u4e00\u5b9a\u8fdd\u6cd5",
        ),
    )


def _contains_aggressive_language(value: str) -> bool:
    lowered = value.lower()
    return _contains_any(
        lowered,
        (
            "idiot",
            "stupid",
            "liar",
            "destroy them",
            "attack them",
            "\u8c23\u8a00\u5236\u9020\u8005\u90fd\u662f\u50bb",
            "\u5fc5\u987b\u5f7b\u5e95\u6253\u5012",
        ),
    )


def _has_cjk(value: str) -> bool:
    return sum(1 for char in value if "\u4e00" <= char <= "\u9fff") >= 8


def _missing_markdown_sections(
    markdown: str,
    report: Any,
    *,
    required_markdown_sections: Sequence[str] | None,
    expected_values: Sequence[str] | None,
) -> list[str]:
    required = [section for section in required_markdown_sections or [] if section]
    missing: list[str] = []
    for section in required:
        if not _markdown_has_section(markdown, report, section):
            missing.append(section)

    for value in expected_values or []:
        if value and str(value) not in markdown:
            missing.append(f"value:{str(value)[:30]}")
    return missing


def _markdown_has_section(markdown: str, report: Any, section: str) -> bool:
    normalized = section.strip().lower()
    if normalized == "risk score":
        return "/100" in markdown or str(_field_value(report, "risk_score")) in markdown
    if normalized == "risk level":
        return _text_value(report, "risk_level") in markdown or _text_value(report, "risk_level_label") in markdown
    if normalized == "risk model version":
        return _text_value(report, "risk_model_version") in markdown
    if normalized == "summary":
        return _text_value(report, "overall_summary") in markdown
    if normalized == "key findings":
        return _contains_any(markdown, _stringify_items(_list_value(report, "key_findings"))[:1])
    if normalized == "top risk topics":
        topics = [_topic_name(topic) for topic in _list_value(report, "top_risk_topics")]
        return not topics or _contains_any(markdown, topics)
    if normalized == "representative comments":
        comments = _stringify_items(_list_value(report, "representative_comments"))[:1]
        return not comments or _contains_any(markdown, comments)
    if normalized == "recommended actions":
        actions = _stringify_items(_list_value(report, "recommended_actions"))[:1]
        return not actions or _contains_any(markdown, actions)
    if normalized == "suggested public response":
        return _text_value(report, "suggested_public_response") in markdown
    return True


def _is_fragmented_report(generated_text: str) -> bool:
    non_empty_lines = [line.strip() for line in generated_text.splitlines() if line.strip()]
    if len(generated_text.strip()) < 80:
        return True
    return len(non_empty_lines) >= 4 and all(len(line) < 12 for line in non_empty_lines)

