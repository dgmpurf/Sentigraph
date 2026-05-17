from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
BENCHMARK_DIR = REPO_ROOT / "benchmarks"
DEFAULT_OUTPUT_DIR = REPO_ROOT / ".benchmarks"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.schemas.analysis import (  # noqa: E402
    AnalysisResultResponse,
    BotImpactSummary,
    BotScore,
    RiskBrief,
)
from app.schemas.case import AnalysisCaseDetail  # noqa: E402
from app.schemas.comment import CleanComment, RawComment, RawPost  # noqa: E402
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScoreResult  # noqa: E402
from app.services.case_store import _build_markdown  # noqa: E402
from app.services.crawling.adapter_factory import get_adapter  # noqa: E402
from app.services.crawling.public_parser.base_public_parser import BasePublicParser  # noqa: E402
from app.services.crawling.public_parser.parser_status_service import preview_public_parser  # noqa: E402
from app.services.crawling.public_parser.public_fetcher import PublicFetcher  # noqa: E402
from app.services.crawling.public_parser.selector_profile import PROFILE_DIR, load_selector_profile  # noqa: E402
from app.services.crawling.public_parser.selector_repair.html_sanitizer import sanitize_html  # noqa: E402
from app.services.crawling.public_parser.selector_repair.selector_repair_service import (  # noqa: E402
    build_repair_request,
    preview_suggestion,
    suggest_selectors,
)
from app.services.evaluation.report_quality_rubric import evaluate_report_quality  # noqa: E402
from app.services.llm.usage_guardrails import reset_usage_for_tests  # noqa: E402
from app.services.nlp.sentiment_analyzer import SentimentAnalyzer  # noqa: E402
from app.services.nlp.topic_clusterer import TopicClusterer  # noqa: E402
from app.services.recommendation.report_builder import build_public_opinion_report  # noqa: E402
from app.services.scoring.topic_risk_score import calculate_topic_risk_score  # noqa: E402


BENCHMARK_VERSION = "v4.0_offline_benchmark_v1"
LATEST_SUMMARY_FILENAME = "offline_benchmark_summary.json"
HISTORY_DIR_NAME = "history"
EXPECTED_FIXTURE_FILES = (
    "sentiment_cases.json",
    "topic_cluster_cases.json",
    "topic_risk_cases.json",
    "report_builder_cases.json",
    "report_quality_cases.json",
    "selector_repair_cases.json",
    "parser_fixture_cases.json",
    "adapter_mock_cases.json",
)
SAFE_ENV_DEFAULTS = {
    "LLM_PROVIDER": "mock",
    "LLM_ENABLE_REAL_CALLS": "false",
    "PUBLIC_PARSER_LIVE_FETCH_ENABLED": "false",
    "SELECTOR_REPAIR_MODE": "mock",
    "SELECTOR_REPAIR_ENABLE_REAL_LLM": "false",
    "SENTIMENT_ANALYZER_MODE": "rule_based",
    "TOPIC_SUMMARY_MODE": "template",
}


class BenchmarkFixtureError(RuntimeError):
    """Raised for fixture loading problems that should become benchmark failures."""


class SuiteRecorder:
    def __init__(self, suite: str) -> None:
        self.suite = suite
        self.cases: list[dict[str, Any]] = []
        self.warnings: list[str] = []

    def check(self, case_id: str, condition: bool, message: str, details: dict[str, Any] | None = None) -> None:
        self.cases.append(
            {
                "case_id": case_id,
                "passed": bool(condition),
                "message": message,
                "details": details or {},
            }
        )

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def summary(self) -> dict[str, Any]:
        passed = sum(1 for case in self.cases if case["passed"])
        failed = len(self.cases) - passed
        return {
            "suite": self.suite,
            "status": "pass" if failed == 0 else "fail",
            "case_count": len(self.cases),
            "passed": passed,
            "failed": failed,
            "warnings": self.warnings,
            "cases": self.cases,
        }


def run_all_benchmarks(
    *,
    fixture_dir: str | Path = BENCHMARK_DIR,
    output_dir: str | Path | None = DEFAULT_OUTPUT_DIR,
    write_json: bool = True,
) -> dict[str, Any]:
    """Run deterministic offline benchmark suites without a backend server."""

    _apply_safe_env_defaults()
    reset_usage_for_tests()
    start = time.perf_counter()
    fixture_root = Path(fixture_dir)
    suites = [
        _safe_run_suite("sentiment", lambda: _run_sentiment_benchmark(fixture_root)),
        _safe_run_suite("topic_cluster", lambda: _run_topic_cluster_benchmark(fixture_root)),
        _safe_run_suite("topic_risk", lambda: _run_topic_risk_benchmark(fixture_root)),
        _safe_run_suite("report_builder", lambda: _run_report_builder_benchmark(fixture_root)),
        _safe_run_suite("report_quality_rubric", lambda: _run_report_quality_rubric_benchmark(fixture_root)),
        _safe_run_suite("markdown_export", lambda: _run_markdown_export_benchmark(fixture_root)),
        _safe_run_suite("selector_repair", lambda: _run_selector_repair_benchmark(fixture_root)),
        _safe_run_suite("public_parser_fixtures", lambda: _run_public_parser_benchmark(fixture_root)),
        _safe_run_suite("platform_adapter_mocks", lambda: _run_adapter_mock_benchmark(fixture_root)),
    ]
    total_passed = sum(suite["passed"] for suite in suites)
    total_failed = sum(suite["failed"] for suite in suites)
    total_warnings = sum(len(suite["warnings"]) for suite in suites)
    result = {
        "benchmark_version": BENCHMARK_VERSION,
        "generated_at": _utc_now_iso(),
        "duration_seconds": round(time.perf_counter() - start, 4),
        "total_passed": total_passed,
        "total_failed": total_failed,
        "total_warnings": total_warnings,
        "safe_mode": {
            "real_llm_calls": False,
            "real_platform_calls": False,
            "live_fetch_enabled": False,
            "backend_server_required": False,
            "api_keys_required": False,
        },
        "suites": suites,
    }
    if write_json and output_dir is not None:
        write_result = _write_summary(result, Path(output_dir))
        result["json_summary_path"] = str(write_result["summary_path"])
        result["json_history_path"] = str(write_result["history_path"])
        result["regression_summary"] = write_result["regression_summary"]
    return result


def _safe_run_suite(suite_name: str, runner) -> dict[str, Any]:
    try:
        return runner()
    except BenchmarkFixtureError as exc:
        recorder = SuiteRecorder(suite_name)
        recorder.check(
            f"{suite_name}:fixture_error",
            False,
            str(exc),
            {"error_category": "fixture_error"},
        )
        return recorder.summary()
    except Exception as exc:
        recorder = SuiteRecorder(suite_name)
        recorder.check(
            f"{suite_name}:suite_error",
            False,
            (
                "Benchmark suite failed safely before completion. "
                "Check the fixture shape and deterministic runner logic for this suite."
            ),
            {
                "error_category": "suite_error",
                "error_type": type(exc).__name__,
            },
        )
        return recorder.summary()


def _run_sentiment_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("sentiment")
    cases = _load_json(fixture_root / "sentiment_cases.json")
    analyzer = SentimentAnalyzer(mode="rule_based")
    for index, case in enumerate(cases, start=1):
        comment = _clean_comment(
            case_id=case["case_id"],
            text=case["text"],
            language=case.get("language", "auto"),
            author_id=f"sentiment_author_{index}",
        )
        result = analyzer.analyze_comment(comment)
        recorder.check(
            case["case_id"],
            result.sentiment in set(case["expected_sentiments"]),
            "coarse sentiment label matches expected offline fixture",
            {"actual": result.sentiment, "expected": case["expected_sentiments"]},
        )
        recorder.check(
            f"{case['case_id']}:schema",
            -1.0 <= result.sentiment_score <= 1.0 and bool(result.reason) and bool(result.stance),
            "sentiment output keeps score range and required fields",
            {
                "sentiment_score": result.sentiment_score,
                "emotion_tags": result.emotion_tags,
                "confidence": result.confidence,
            },
        )
    return recorder.summary()


def _run_topic_cluster_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("topic_cluster")
    cases = _load_json(fixture_root / "topic_cluster_cases.json")
    analyzer = SentimentAnalyzer(mode="rule_based")
    clusterer = TopicClusterer(summary_mode="template")
    for case in cases:
        comments = [_comment_from_fixture(item) for item in case["comments"]]
        sentiments = [analyzer.analyze_comment(comment) for comment in comments]
        clusters = clusterer.cluster(comments, sentiments)
        topics = {cluster.topic for cluster in clusters}
        for expected_topic in case["expected_topics"]:
            recorder.check(
                f"{case['case_id']}:{expected_topic}",
                expected_topic in topics,
                "expected deterministic topic bucket is present",
                {"topics": sorted(topics)},
            )
        recorder.check(
            f"{case['case_id']}:shape",
            all(cluster.summary and cluster.comment_count >= 1 and cluster.representative_comments for cluster in clusters),
            "topic clusters include summary, count, and representatives",
            {"cluster_count": len(clusters)},
        )
    return recorder.summary()


def _run_topic_risk_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("topic_risk")
    cases = _load_json(fixture_root / "topic_risk_cases.json")
    for case in cases:
        comments = [_comment_from_fixture(item) for item in case["comments"]]
        sentiments = [SentimentAnalyzer(mode="rule_based").analyze_comment(comment) for comment in comments]
        clusters = TopicClusterer(summary_mode="template").cluster(comments, sentiments)
        result = _calculate_risk_from_comments(case["comments"], comments, sentiments, clusters)
        expected = case.get("expected", {})
        high_topic_name = expected.get("high_topic")
        low_topic_name = expected.get("low_topic")
        high_topic = _find_topic(result, high_topic_name) if high_topic_name else None
        low_topic = _find_topic(result, low_topic_name) if low_topic_name else None
        sorted_scores = [topic.topic_risk_score for topic in result.top_risk_topics]
        all_scores = [topic.topic_risk_score for topic in result.topic_risks]
        recorder.check(
            f"{case['case_id']}:version",
            result.risk_model_version == TOPIC_RISK_MODEL_VERSION,
            "V1.5 topic risk model version is preserved",
            {"risk_model_version": result.risk_model_version},
        )
        recorder.check(
            f"{case['case_id']}:score_range",
            all(0 <= score <= 100 for score in all_scores)
            and 0 <= result.overall_risk <= 100
            and 0 <= result.manipulation_risk <= 100,
            "all topic risk scores stay in 0-100",
            {"scores": all_scores, "overall_risk": result.overall_risk},
        )
        recorder.check(
            f"{case['case_id']}:ordering",
            sorted_scores == sorted(sorted_scores, reverse=True),
            "top risk topics are sorted deterministically by score",
            {"top_scores": sorted_scores},
        )
        if high_topic_name and low_topic_name:
            recorder.check(
                f"{case['case_id']}:negative_above_neutral",
                bool(high_topic and low_topic and high_topic.topic_risk_score > low_topic.topic_risk_score),
                "expected higher-risk topic scores above lower-risk comparison topic",
                {
                    "high_topic": high_topic_name,
                    "low_topic": low_topic_name,
                    "high_topic_score": high_topic.topic_risk_score if high_topic else None,
                    "low_topic_score": low_topic.topic_risk_score if low_topic else None,
                },
            )
        if expected.get("top_topic"):
            leading_topic = result.top_risk_topics[0].topic if result.top_risk_topics else None
            recorder.check(
                f"{case['case_id']}:top_topic",
                leading_topic == expected["top_topic"],
                "expected leading topic remains deterministic",
                {"leading_topic": leading_topic, "expected": expected["top_topic"]},
            )
        if "min_overall_risk" in expected:
            recorder.check(
                f"{case['case_id']}:min_overall_risk",
                result.overall_risk >= float(expected["min_overall_risk"]),
                "overall topic risk meets minimum expected range",
                {"overall_risk": result.overall_risk},
            )
        if "max_overall_risk" in expected:
            recorder.check(
                f"{case['case_id']}:max_overall_risk",
                result.overall_risk <= float(expected["max_overall_risk"]),
                "overall topic risk stays below maximum expected range",
                {"overall_risk": result.overall_risk},
            )
        if "min_real_crisis_risk" in expected:
            recorder.check(
                f"{case['case_id']}:real_crisis",
                result.real_crisis_risk >= float(expected["min_real_crisis_risk"]),
                "credible negative topic signals increase real-crisis risk",
                {"real_crisis_risk": result.real_crisis_risk},
            )
        if "min_manipulation_risk" in expected:
            recorder.check(
                f"{case['case_id']}:manipulation",
                result.manipulation_risk >= float(expected["min_manipulation_risk"]),
                "bot/manipulation signals increase manipulation risk",
                {"manipulation_risk": result.manipulation_risk},
            )
    return recorder.summary()


def _run_report_builder_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("report_builder")
    for case, _analysis, report in _iter_report_contexts(fixture_root):
        recorder.check(
            f"{case['case_id']}:fields",
            bool(report.overall_summary)
            and bool(report.key_findings)
            and bool(report.recommended_actions)
            and bool(report.suggested_public_response),
            "zh-CN report includes required strategic fields",
            {
                "report_language": report.report_language,
                "risk_score": report.risk_score,
                "risk_level": report.risk_level,
            },
        )
        representative_text = "\n".join(report.representative_comments)
        recorder.check(
            f"{case['case_id']}:representatives",
            all(comment in representative_text for comment in case["representative_comments"]),
            "representative comments are preserved in original language",
        )
        combined_report_text = "\n".join(
            [
                report.overall_summary,
                *report.key_findings,
                *report.main_risk_factors,
                *report.recommended_actions,
                report.suggested_public_response,
            ]
        )
        recorder.check(
            f"{case['case_id']}:no_json_dump",
            "{" not in combined_report_text and "}" not in combined_report_text,
            "report text does not degrade into a raw JSON dump",
        )
    return recorder.summary()


def _run_report_quality_rubric_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("report_quality_rubric")
    cases = _load_json(fixture_root / "report_quality_cases.json")
    report_contexts = {
        report_case["case_id"]: (report_case, analysis, report)
        for report_case, analysis, report in _iter_report_contexts(fixture_root)
    }
    for case in cases:
        source_case_id = str(case["source_report_case_id"])
        if source_case_id not in report_contexts:
            recorder.check(
                f"{case['case_id']}:source_case",
                False,
                "report quality fixture references an unknown report_builder case",
                {"source_case_id": source_case_id},
            )
            continue

        report_case, analysis, base_report = report_contexts[source_case_id]
        report = _mutate_report_for_quality_case(base_report, str(case.get("mutation") or "none"))
        markdown = None
        markdown_expected_values: list[str] = []
        if case.get("include_markdown"):
            markdown = _markdown_for_report_case(report_case, analysis, report)
            markdown_expected_values = [
                str(report_case.get("title") or ""),
                str(report_case.get("keyword") or ""),
                ", ".join(report_case.get("platforms") or []),
            ]

        result = evaluate_report_quality(
            report,
            markdown=markdown,
            expected_representative_comments=report_case.get("representative_comments"),
            required_markdown_sections=case.get("required_markdown_sections"),
            markdown_expected_values=markdown_expected_values,
        )
        finding_codes = set(result.finding_codes())
        missing_sections = set(result.missing_sections)
        details = {
            "score": result.total_score,
            "grade": result.grade,
            "finding_codes": sorted(finding_codes),
            "missing_sections": sorted(missing_sections),
            "dimension_scores": result.dimension_scores,
        }

        recorder.check(
            f"{case['case_id']}:score_range",
            0 <= result.total_score <= 100,
            "report quality rubric score stays in 0-100",
            details,
        )
        if case.get("expected_grade"):
            recorder.check(
                f"{case['case_id']}:grade",
                result.grade == case["expected_grade"],
                "report quality rubric grade matches coarse expectation",
                details,
            )
        if "min_score" in case:
            recorder.check(
                f"{case['case_id']}:min_score",
                result.total_score >= int(case["min_score"]),
                "report quality score meets minimum coarse threshold",
                details,
            )
        if "max_score" in case:
            recorder.check(
                f"{case['case_id']}:max_score",
                result.total_score <= int(case["max_score"]),
                "report quality score stays below maximum coarse threshold",
                details,
            )
        expected_finding_codes = set(case.get("expected_finding_codes") or [])
        if expected_finding_codes:
            recorder.check(
                f"{case['case_id']}:finding_codes",
                expected_finding_codes.issubset(finding_codes),
                "report quality rubric emits expected finding codes",
                details,
            )
        expected_missing_sections = set(case.get("expected_missing_sections") or [])
        if expected_missing_sections:
            recorder.check(
                f"{case['case_id']}:missing_sections",
                expected_missing_sections.issubset(missing_sections),
                "report quality rubric reports expected missing sections",
                details,
            )
        if case.get("expect_markdown_valid"):
            recorder.check(
                f"{case['case_id']}:markdown_quality",
                "markdown_missing_sections" not in finding_codes,
                "Markdown report quality check passes expected sections",
                details,
            )
    return recorder.summary()


def _run_markdown_export_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("markdown_export")
    for case, analysis, report in _iter_report_contexts(fixture_root):
        markdown = _markdown_for_report_case(case, analysis, report)
        recorder.check(
            f"{case['case_id']}:markdown_sections",
            _markdown_has_required_sections(markdown, case, report),
            "Markdown export includes required benchmark sections",
            {"markdown_length": len(markdown)},
        )
    return recorder.summary()


def _run_selector_repair_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("selector_repair")
    cases = _load_json(fixture_root / "selector_repair_cases.json")
    for case in cases:
        profile_path = PROFILE_DIR / f"{case['platform_id']}.json"
        before_profile = profile_path.read_text(encoding="utf-8") if profile_path.exists() else ""
        sanitized = sanitize_html(case["html"], max_chars=20000)
        recorder.check(
            f"{case['case_id']}:sanitize",
            "<script" not in sanitized.lower()
            and "<style" not in sanitized.lower()
            and "onclick=" not in sanitized.lower()
            and len(sanitized) <= 20000,
            "sanitizer removes scripts, styles, inline events, and obeys length limit",
        )
        request = build_repair_request(
            platform_id=case["platform_id"],
            html=case["html"],
            error_summary=case.get("error_summary", ""),
            extraction_targets=case.get("extraction_targets"),
        )
        suggestion = suggest_selectors(request)
        second_suggestion = suggest_selectors(request)
        suggestion_dump = suggestion.model_dump(mode="json")
        second_dump = second_suggestion.model_dump(mode="json")
        targets = {candidate.target for candidate in suggestion.candidates}
        recorder.check(
            f"{case['case_id']}:deterministic",
            suggestion_dump == second_dump and set(case["expected_targets"]).issubset(targets),
            "MockProvider selector suggestions are deterministic and cover expected targets",
            {"targets": sorted(targets)},
        )
        preview = preview_suggestion(case["platform_id"], suggestion, sanitized)
        matched_targets = {target for target, matched in preview.matched_targets.items() if matched}
        expected_matched_targets = set(case.get("expected_matched_targets") or case["expected_targets"])
        min_matched_targets = int(case.get("min_matched_targets", 1))
        recorder.check(
            f"{case['case_id']}:preview",
            preview.profile_modified is False
            and len(matched_targets.intersection(expected_matched_targets)) >= min_matched_targets,
            "selector preview matches fixture HTML and does not modify profiles",
            {"matched_targets": sorted(matched_targets), "warnings": preview.warnings},
        )
        if case.get("expected_preview_status"):
            recorder.check(
                f"{case['case_id']}:preview_status",
                preview.status == case["expected_preview_status"],
                "selector preview status matches expected fixture outcome",
                {"status": preview.status, "expected": case["expected_preview_status"]},
            )
        after_profile = profile_path.read_text(encoding="utf-8") if profile_path.exists() else ""
        recorder.check(
            f"{case['case_id']}:profile_unchanged",
            before_profile == after_profile,
            "active parser profile file is not modified automatically",
        )
    return recorder.summary()


def _run_public_parser_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("public_parser_fixtures")
    cases = _load_json(fixture_root / "parser_fixture_cases.json")
    for case in cases:
        platform = case["platform_id"]
        safe_limit = int(case.get("limit", 3))
        if case.get("fixture_html"):
            profile = load_selector_profile(platform)
            parser = BasePublicParser(
                profile,
                fetcher=PublicFetcher(live_fetch_enabled=False, rate_limit_seconds=0),
            )
            parsed = parser.parse_html(
                case["fixture_html"],
                source_url=profile.fixture_url or profile.base_url,
                keyword=case.get("keyword", "benchmark"),
                limit=safe_limit,
                metadata_extra={"fetch_status": "inline_fixture"},
            )
            posts = parsed.posts[:safe_limit]
            comments = parsed.comments[:safe_limit]
            post_count = len(parsed.posts)
            comment_count = len(parsed.comments)
            raw_post_schema_valid = all(_schema_valid(RawPost, item) for item in posts)
            raw_comment_schema_valid = all(_schema_valid(RawComment, item) for item in comments)
            live_fetch_enabled = bool(parsed.metadata.get("live_fetch_enabled", False))
            fallback_reason_category = parsed.metadata.get("fallback_reason_category")
        else:
            result = preview_public_parser(platform, limit=safe_limit, use_live_fetch=False)
            posts = result.sample_posts
            comments = result.sample_comments
            post_count = result.post_count
            comment_count = result.comment_count
            raw_post_schema_valid = (
                result.raw_post_schema_valid and all(_schema_valid(RawPost, item) for item in posts)
            )
            raw_comment_schema_valid = (
                result.raw_comment_schema_valid and all(_schema_valid(RawComment, item) for item in comments)
            )
            live_fetch_enabled = result.live_fetch_enabled
            fallback_reason_category = result.fallback_reason_category
        recorder.check(
            f"{case.get('case_id', platform)}:counts",
            post_count >= case["min_posts"] and comment_count >= case["min_comments"],
            "public parser fixture returns expected post/comment counts",
            {"post_count": post_count, "comment_count": comment_count},
        )
        recorder.check(
            f"{case.get('case_id', platform)}:schema",
            raw_post_schema_valid is True and raw_comment_schema_valid is True,
            "public parser fixture output validates RawPost/RawComment schema",
        )
        recorder.check(
            f"{case.get('case_id', platform)}:live_disabled",
            live_fetch_enabled is False,
            "public parser benchmark keeps live fetch disabled",
        )
        if case.get("expect_default_author"):
            recorder.check(
                f"{case['case_id']}:default_author",
                bool(posts) and all(post.author_name == "public_source" for post in posts),
                "missing author falls back to safe public_source value",
                {"authors": [post.author_name for post in posts]},
            )
        if case.get("expect_default_created_at"):
            recorder.check(
                f"{case['case_id']}:default_created_at",
                bool(posts) and all(post.created_at == "2026-05-15T00:00:00Z" for post in posts),
                "missing created_at falls back to deterministic timestamp",
                {"created_at": [post.created_at for post in posts]},
            )
        if case.get("expected_fallback_reason_category"):
            recorder.check(
                f"{case['case_id']}:fallback_reason",
                fallback_reason_category == case["expected_fallback_reason_category"],
                "parser reports expected safe fallback reason for edge fixture",
                {
                    "fallback_reason_category": fallback_reason_category,
                    "expected": case["expected_fallback_reason_category"],
                },
            )
    return recorder.summary()


def _run_adapter_mock_benchmark(fixture_root: Path) -> dict[str, Any]:
    recorder = SuiteRecorder("platform_adapter_mocks")
    cases = _load_json(fixture_root / "adapter_mock_cases.json")
    for case in cases:
        platform = case["platform_id"]
        case_label = case.get("case_id", platform)
        adapter = get_adapter(platform, mode="mock")
        posts = adapter.search_posts(case["keyword"], limit=case.get("limit", 2))
        comments = adapter.fetch_comments(posts[0].post_id, limit=case.get("limit", 2)) if posts else []
        recorder.check(
            f"{case_label}:counts",
            len(posts) >= case["min_posts"] and len(comments) >= case["min_comments"],
            "mock adapter returns deterministic posts and comments",
            {"post_count": len(posts), "comment_count": len(comments)},
        )
        recorder.check(
            f"{case_label}:post_schema",
            all(_schema_valid(RawPost, post) for post in posts),
            "mock adapter posts validate RawPost schema",
        )
        recorder.check(
            f"{case_label}:comment_schema",
            all(_schema_valid(RawComment, comment) for comment in comments),
            "mock adapter comments validate RawComment schema",
        )
    return recorder.summary()


def _calculate_risk_from_comments(
    raw_comment_fixtures: list[dict[str, Any]],
    comments: list[CleanComment],
    sentiments: list[Any],
    clusters: list[Any],
) -> TopicRiskScoreResult:
    bot_accounts = [
        BotScore(
            author_id=item["author_id"],
            bot_probability=float(item.get("bot_probability", 0.0)),
            bot_reasons=["benchmark repeated-script signal"],
            influence_weight=1.0,
        )
        for item in raw_comment_fixtures
        if float(item.get("bot_probability", 0.0)) >= 0.5 or bool(item.get("is_repeated_script"))
    ]
    suspected_comment_count = sum(
        int(item.get("duplicate_count", 1))
        for item in raw_comment_fixtures
        if float(item.get("bot_probability", 0.0)) >= 0.5 or bool(item.get("is_repeated_script"))
    )
    total_comment_count = max(1, sum(int(item.get("duplicate_count", 1)) for item in raw_comment_fixtures))
    bot_impact = BotImpactSummary(
        suspected_bot_ratio=round(len(bot_accounts) / max(1, len(raw_comment_fixtures)), 4),
        suspected_bot_comment_ratio=round(suspected_comment_count / total_comment_count, 4),
    )
    raw_comments = [_raw_comment_from_fixture(item) for item in raw_comment_fixtures]
    return calculate_topic_risk_score(
        clusters,
        clean_comments=comments,
        sentiment_results=sentiments,
        bot_accounts=bot_accounts,
        bot_impact=bot_impact,
        raw_comments=raw_comments,
    )


def _analysis_from_outputs(
    project_id: str,
    comments: list[CleanComment],
    sentiments: list[Any],
    clusters: list[Any],
    risk_result: TopicRiskScoreResult,
) -> AnalysisResultResponse:
    sentiment_summary = SentimentAnalyzer.summarize(sentiments)
    bot_impact = BotImpactSummary(suspected_bot_ratio=0.25, suspected_bot_comment_ratio=0.5)
    return AnalysisResultResponse(
        project_id=project_id,
        summary="Offline benchmark analysis for deterministic Sentigraph report evaluation.",
        sentiment=sentiment_summary,
        topics=clusters,
        conflicts=[],
        bot_score=bot_impact,
        risk=RiskBrief(risk_score=int(round(risk_result.overall_risk)), risk_level=risk_result.risk_level),
        sentiment_results=sentiments,
        ai_generated=[],
        bot_accounts=[],
        risk_model_version=TOPIC_RISK_MODEL_VERSION,
        topic_risks=risk_result.topic_risks,
        top_risk_topics=risk_result.top_risk_topics,
        max_topic_risk=risk_result.max_topic_risk,
        average_topic_risk=risk_result.average_topic_risk,
        overall_risk=risk_result.overall_risk,
        real_crisis_risk=risk_result.real_crisis_risk,
        manipulation_risk=risk_result.manipulation_risk,
        risk_explanation=risk_result.risk_explanation,
    )


def _iter_report_contexts(fixture_root: Path):
    cases = _load_json(fixture_root / "report_builder_cases.json")
    topic_fixture = _load_json(fixture_root / "topic_risk_cases.json")[0]
    comments = [_comment_from_fixture(item) for item in topic_fixture["comments"]]
    analyzer = SentimentAnalyzer(mode="rule_based")
    sentiments = [analyzer.analyze_comment(comment) for comment in comments]
    clusters = TopicClusterer(summary_mode="template").cluster(comments, sentiments)
    risk_result = _calculate_risk_from_comments(topic_fixture["comments"], comments, sentiments, clusters)
    for case in cases:
        analysis = _analysis_from_outputs(case["project_id"], comments, sentiments, clusters, risk_result)
        report = build_public_opinion_report(
            analysis,
            topic_risk_result=risk_result,
            representative_comments=case["representative_comments"],
            report_language=case.get("report_language", "zh-CN"),
        )
        yield case, analysis, report


def _markdown_for_report_case(case: dict[str, Any], analysis: AnalysisResultResponse, report: Any) -> str:
    now = datetime(2026, 5, 17, tzinfo=timezone.utc)
    detail = AnalysisCaseDetail(
        case_id=f"{case['case_id']}_case",
        project_id=case["project_id"],
        title=case["title"],
        keyword=case["keyword"],
        platforms=case["platforms"],
        status="completed",
        created_at=now,
        updated_at=now,
        risk_score=report.overall_risk if report.overall_risk is not None else report.risk_score,
        risk_level=report.risk_level,
        risk_model_version=report.risk_model_version,
        report_language=case.get("report_language", "zh-CN"),
        analysis_result=analysis,
        visualization_data=None,
        report=report,
        markdown_available=True,
    )
    return _build_markdown(detail)


def _markdown_has_required_sections(markdown: str, case: dict[str, Any], report: Any) -> bool:
    if not markdown.startswith(f"# {case['title']}"):
        return False
    required_values = [
        case["keyword"],
        ", ".join(case["platforms"]),
        "/100",
        report.risk_level,
        report.risk_model_version,
        report.overall_summary,
        report.suggested_public_response,
    ]
    if report.key_findings:
        required_values.append(report.key_findings[0])
    if report.top_risk_topics:
        required_values.append(report.top_risk_topics[0].topic)
    if report.representative_comments:
        required_values.append(report.representative_comments[0])
    if report.recommended_actions:
        required_values.append(report.recommended_actions[0])
    return all(value in markdown for value in required_values if value)


def _mutate_report_for_quality_case(report: Any, mutation: str) -> Any:
    normalized = (mutation or "none").strip().lower()
    if normalized == "none":
        return report
    if normalized == "remove_recommended_actions":
        return report.model_copy(update={"recommended_actions": []})
    if normalized == "inject_raw_json":
        return report.model_copy(update={"overall_summary": '{"risk": "high", "status": "mock"}'})
    if normalized == "vague_response":
        return report.model_copy(
            update={
                "recommended_actions": ["Monitor.", "Follow up."],
                "suggested_public_response": "We care.",
            }
        )
    if normalized == "unsafe_overclaim":
        return report.model_copy(
            update={
                "suggested_public_response": (
                    "We confirmed fraud and criminal conduct before the mock review has verified facts."
                )
            }
        )
    return report


def _comment_from_fixture(item: dict[str, Any]) -> CleanComment:
    return _clean_comment(
        case_id=item["comment_id"],
        text=item["text"],
        language=item.get("language", "auto"),
        author_id=item.get("author_id", "benchmark_author"),
        duplicate_count=int(item.get("duplicate_count", 1)),
        is_repeated_script=bool(item.get("is_repeated_script", False)),
    )


def _clean_comment(
    *,
    case_id: str,
    text: str,
    language: str,
    author_id: str,
    duplicate_count: int = 1,
    is_repeated_script: bool = False,
) -> CleanComment:
    return CleanComment(
        clean_comment_id=case_id,
        original_comment_ids=[case_id],
        platforms=["benchmark"],
        post_ids=["benchmark_post"],
        author_id=author_id,
        clean_text=text,
        language=language,
        duplicate_group_id=f"{case_id}_dup" if duplicate_count > 1 else None,
        duplicate_count=duplicate_count,
        semantic_similarity_group=None,
        is_repeated_script=is_repeated_script,
        created_at_min="2026-05-17T00:00:00Z",
        created_at_max="2026-05-17T00:00:00Z",
    )


def _raw_comment_from_fixture(item: dict[str, Any]) -> RawComment:
    comment_id = item["comment_id"]
    return RawComment(
        platform="benchmark",
        post_id="benchmark_post",
        comment_id=comment_id,
        parent_id=None,
        author_id=item.get("author_id", "benchmark_author"),
        author_name=item.get("author_id", "benchmark_author"),
        content=item["text"],
        like_count=int(item.get("like_count", 0)),
        reply_count=int(item.get("reply_count", 0)),
        share_count=int(item.get("share_count", 0)),
        created_at="2026-05-17T00:00:00Z",
        url=f"https://example.invalid/benchmark/{comment_id}",
        raw_data={"mode": "offline_benchmark"},
    )


def _find_topic(result: TopicRiskScoreResult, topic_name: str):
    return next((topic for topic in result.topic_risks if topic.topic == topic_name), None)


def _schema_valid(schema: Any, value: Any) -> bool:
    try:
        if hasattr(value, "model_dump"):
            schema.model_validate(value.model_dump(mode="json"))
        else:
            schema.model_validate(value)
    except Exception:
        return False
    return True


def _load_json(path: Path) -> Any:
    if not path.exists():
        expected = ", ".join(EXPECTED_FIXTURE_FILES)
        raise BenchmarkFixtureError(
            f"Required benchmark fixture is missing: {path.name}. Expected fixtures: {expected}."
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BenchmarkFixtureError(
            f"Benchmark fixture is not valid JSON: {path.name}."
        ) from exc


def _apply_safe_env_defaults() -> None:
    for key, value in SAFE_ENV_DEFAULTS.items():
        os.environ.setdefault(key, value)


def _write_summary(result: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    history_dir = output_dir / HISTORY_DIR_NAME
    previous_entry = _load_previous_history_entry(history_dir)
    safe_summary = _safe_benchmark_summary(result)
    regression_summary = build_regression_summary(safe_summary, previous_entry)
    safe_summary["regression_summary"] = regression_summary

    summary_path = output_dir / LATEST_SUMMARY_FILENAME
    summary_path.write_text(
        json.dumps(safe_summary, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    history_dir.mkdir(parents=True, exist_ok=True)
    history_entry = {
        **safe_summary,
        "source": "offline_benchmark",
        "regression_detected": bool(regression_summary.get("regression_detected")),
    }
    history_path = _build_history_path(history_dir, str(history_entry["benchmark_id"]))
    history_path.write_text(
        json.dumps(history_entry, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return {
        "summary_path": summary_path,
        "history_path": history_path,
        "regression_summary": regression_summary,
    }


def _safe_benchmark_summary(result: dict[str, Any]) -> dict[str, Any]:
    generated_at = str(result.get("generated_at") or _utc_now_iso())
    return {
        "source": "offline_benchmark_summary",
        "benchmark_id": _build_benchmark_id(generated_at),
        "benchmark_version": str(result.get("benchmark_version") or BENCHMARK_VERSION),
        "generated_at": generated_at,
        "duration_seconds": _safe_float(result.get("duration_seconds")),
        "total_passed": _safe_int(result.get("total_passed")),
        "total_failed": _safe_int(result.get("total_failed")),
        "total_warnings": _safe_int(result.get("total_warnings")),
        "suites": [_safe_suite_summary(suite) for suite in result.get("suites", []) if isinstance(suite, dict)],
    }


def _safe_suite_summary(suite: dict[str, Any]) -> dict[str, Any]:
    warnings = suite.get("warnings")
    return {
        "suite": str(suite.get("suite") or "unknown"),
        "status": str(suite.get("status") or "unknown"),
        "case_count": _safe_int(suite.get("case_count"), fallback=_safe_int(suite.get("passed")) + _safe_int(suite.get("failed"))),
        "passed": _safe_int(suite.get("passed")),
        "failed": _safe_int(suite.get("failed")),
        "warnings": [str(warning)[:300] for warning in warnings] if isinstance(warnings, list) else [],
    }


def build_regression_summary(
    latest_summary: dict[str, Any],
    previous_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    latest_total_failed = _safe_int(latest_summary.get("total_failed"))
    latest_total_warnings = _safe_int(latest_summary.get("total_warnings"))
    latest_total_passed = _safe_int(latest_summary.get("total_passed"))
    if previous_summary is None:
        return {
            "source": "offline_benchmark_regression",
            "available": False,
            "status": "no_history",
            "regression_detected": False,
            "changed_suites": [],
            "previous_total_failed": None,
            "latest_total_failed": latest_total_failed,
            "previous_total_warnings": None,
            "latest_total_warnings": latest_total_warnings,
            "previous_total_passed": None,
            "latest_total_passed": latest_total_passed,
            "message": "No previous benchmark history entry is available for comparison.",
        }

    previous_total_failed = _safe_int(previous_summary.get("total_failed"))
    previous_total_warnings = _safe_int(previous_summary.get("total_warnings"))
    previous_total_passed = _safe_int(previous_summary.get("total_passed"))
    changed_suites = _build_changed_suites(latest_summary, previous_summary)
    regression_reasons: list[str] = []
    if latest_total_failed > previous_total_failed:
        regression_reasons.append("total_failed_increased")
    if latest_total_warnings > previous_total_warnings:
        regression_reasons.append("total_warnings_increased")
    if latest_total_passed < previous_total_passed:
        regression_reasons.append("total_passed_decreased")
    if any("suite_pass_to_fail" in change["change_types"] for change in changed_suites):
        regression_reasons.append("suite_pass_to_fail")

    regression_detected = bool(regression_reasons or changed_suites)
    return {
        "source": "offline_benchmark_regression",
        "available": True,
        "status": "regression_detected" if regression_detected else "no_regression",
        "regression_detected": regression_detected,
        "changed_suites": changed_suites,
        "previous_benchmark_id": previous_summary.get("benchmark_id"),
        "latest_benchmark_id": latest_summary.get("benchmark_id"),
        "previous_generated_at": previous_summary.get("generated_at"),
        "latest_generated_at": latest_summary.get("generated_at"),
        "previous_total_failed": previous_total_failed,
        "latest_total_failed": latest_total_failed,
        "previous_total_warnings": previous_total_warnings,
        "latest_total_warnings": latest_total_warnings,
        "previous_total_passed": previous_total_passed,
        "latest_total_passed": latest_total_passed,
        "reason_categories": regression_reasons,
        "message": (
            "Regression risk detected in the latest offline benchmark run."
            if regression_detected
            else "No benchmark regression detected compared with the previous run."
        ),
    }


def _build_changed_suites(
    latest_summary: dict[str, Any],
    previous_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    previous_suites = _suite_map(previous_summary.get("suites"))
    latest_suites = _suite_map(latest_summary.get("suites"))
    changed: list[dict[str, Any]] = []
    for suite_name in sorted(set(previous_suites) | set(latest_suites)):
        previous_suite = previous_suites.get(suite_name, {})
        latest_suite = latest_suites.get(suite_name, {})
        change_types: list[str] = []
        previous_status = str(previous_suite.get("status") or "missing")
        latest_status = str(latest_suite.get("status") or "missing")
        previous_failed = _safe_int(previous_suite.get("failed"))
        latest_failed = _safe_int(latest_suite.get("failed"))
        previous_warning_count = len(previous_suite.get("warnings") or [])
        latest_warning_count = len(latest_suite.get("warnings") or [])

        if previous_status == "pass" and latest_status == "fail":
            change_types.append("suite_pass_to_fail")
        if latest_failed > previous_failed:
            change_types.append("new_failures")
        if latest_warning_count > previous_warning_count:
            change_types.append("warnings_increased")
        if not change_types:
            continue
        changed.append(
            {
                "suite": suite_name,
                "change_types": change_types,
                "previous_status": previous_status,
                "latest_status": latest_status,
                "previous_failed": previous_failed,
                "latest_failed": latest_failed,
                "previous_warnings": previous_warning_count,
                "latest_warnings": latest_warning_count,
            }
        )
    return changed


def _suite_map(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        return {}
    suites: dict[str, dict[str, Any]] = {}
    for item in value:
        if not isinstance(item, dict):
            continue
        suite_name = str(item.get("suite") or "").strip()
        if suite_name:
            suites[suite_name] = item
    return suites


def _load_previous_history_entry(history_dir: Path) -> dict[str, Any] | None:
    if not history_dir.exists() or not history_dir.is_dir():
        return None
    for path in sorted(history_dir.glob("*.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            return _safe_history_entry(payload)
    return None


def _safe_history_entry(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": "offline_benchmark",
        "benchmark_id": str(payload.get("benchmark_id") or ""),
        "benchmark_version": str(payload.get("benchmark_version") or BENCHMARK_VERSION),
        "generated_at": str(payload.get("generated_at") or ""),
        "duration_seconds": _safe_float(payload.get("duration_seconds")),
        "total_passed": _safe_int(payload.get("total_passed")),
        "total_failed": _safe_int(payload.get("total_failed")),
        "total_warnings": _safe_int(payload.get("total_warnings")),
        "suites": [_safe_suite_summary(suite) for suite in payload.get("suites", []) if isinstance(suite, dict)],
        "regression_detected": bool(payload.get("regression_detected")),
    }


def _build_history_path(history_dir: Path, benchmark_id: str) -> Path:
    safe_id = "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in benchmark_id)
    safe_id = safe_id or "benchmark"
    path = history_dir / f"{safe_id}.json"
    counter = 2
    while path.exists():
        path = history_dir / f"{safe_id}_{counter}.json"
        counter += 1
    return path


def _build_benchmark_id(generated_at: str) -> str:
    safe_timestamp = (
        generated_at.replace(":", "")
        .replace("-", "")
        .replace("+", "")
        .replace(".", "")
        .replace("Z", "z")
    )
    safe_timestamp = "".join(char for char in safe_timestamp if char.isalnum() or char in {"T", "z"})
    return f"benchmark_{safe_timestamp or int(time.time())}"


def _safe_int(value: Any, fallback: int = 0) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return fallback


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 4)
    except (TypeError, ValueError):
        return None


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Sentigraph v4.0 offline benchmark suites without external APIs."
    )
    parser.add_argument(
        "--fixture-dir",
        default=str(BENCHMARK_DIR),
        help="Benchmark fixture directory. Defaults to the repository benchmarks directory.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Generated JSON summary directory. Defaults to .benchmarks.",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="Do not write a generated JSON summary file.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    result = run_all_benchmarks(
        fixture_dir=args.fixture_dir,
        output_dir=None if args.no_json else args.output_dir,
        write_json=not args.no_json,
    )
    _print_summary(result)
    return 0 if result["total_failed"] == 0 else 1


def _print_summary(result: dict[str, Any]) -> None:
    print("Sentigraph offline benchmark summary")
    print(f"Benchmark version: {result['benchmark_version']}")
    for suite in result["suites"]:
        status = "PASS" if suite["failed"] == 0 else "FAIL"
        print(
            f"- {suite['suite']}: {status} "
            f"({suite.get('case_count', suite['passed'] + suite['failed'])} cases, "
            f"{suite['passed']} passed, {suite['failed']} failed, {len(suite['warnings'])} warnings)"
        )
    print(
        "Total: "
        f"{result['total_passed']} passed, {result['total_failed']} failed, "
        f"{result['total_warnings']} warnings in {result['duration_seconds']}s"
    )
    if result.get("json_summary_path"):
        print(f"JSON summary: {result['json_summary_path']}")
    if result.get("json_history_path"):
        print(f"History entry: {result['json_history_path']}")
    regression = result.get("regression_summary")
    if isinstance(regression, dict):
        if regression.get("available") is False:
            print("Regression: no previous history entry available for comparison")
        elif regression.get("regression_detected"):
            print(f"Regression: detected ({', '.join(regression.get('reason_categories') or ['suite_changed'])})")
        else:
            print("Regression: no regression detected")
    print("Safety: no real LLM calls, no real platform API calls, live fetch disabled.")


if __name__ == "__main__":
    raise SystemExit(main())
