from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.benchmark import BenchmarkSuiteSummary, LatestBenchmarkSummaryResponse


def _find_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists():
            return parent
    return Path.cwd()


DEFAULT_BENCHMARK_SUMMARY_PATH = (
    _find_project_root() / ".benchmarks" / "offline_benchmark_summary.json"
)


def load_latest_benchmark_summary(
    summary_path: str | Path | None = None,
) -> LatestBenchmarkSummaryResponse:
    path = Path(summary_path) if summary_path is not None else DEFAULT_BENCHMARK_SUMMARY_PATH
    if not path.exists():
        return LatestBenchmarkSummaryResponse(
            available=False,
            status="missing",
            message=(
                "No offline benchmark summary found. Run "
                "python scripts/run_offline_benchmarks.py to generate it."
            ),
        )

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return LatestBenchmarkSummaryResponse(
            available=False,
            status="malformed",
            message="Offline benchmark summary exists but could not be parsed safely.",
        )

    if not isinstance(payload, dict):
        return LatestBenchmarkSummaryResponse(
            available=False,
            status="malformed",
            message="Offline benchmark summary is not a JSON object.",
        )

    suites = _safe_suites(payload.get("suites"))
    total_warnings = _safe_int(
        payload.get("total_warnings"),
        fallback=sum(len(suite.warnings) for suite in suites),
    )

    return LatestBenchmarkSummaryResponse(
        available=True,
        status="available",
        generated_at=_safe_optional_text(payload.get("generated_at")),
        benchmark_version=_safe_optional_text(payload.get("benchmark_version")),
        total_passed=_safe_int(payload.get("total_passed")),
        total_failed=_safe_int(payload.get("total_failed")),
        total_warnings=total_warnings,
        suites=suites,
        message="Latest offline benchmark summary loaded.",
    )


def _safe_suites(value: Any) -> list[BenchmarkSuiteSummary]:
    if not isinstance(value, list):
        return []

    suites: list[BenchmarkSuiteSummary] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        suite_name = _safe_optional_text(item.get("suite"))
        if not suite_name:
            continue
        warnings = item.get("warnings")
        suites.append(
            BenchmarkSuiteSummary(
                suite=suite_name,
                status=_safe_optional_text(item.get("status")) or "unknown",
                passed=_safe_int(item.get("passed")),
                failed=_safe_int(item.get("failed")),
                warnings=[str(warning) for warning in warnings] if isinstance(warnings, list) else [],
            )
        )
    return suites


def _safe_int(value: Any, fallback: int = 0) -> int:
    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        return fallback
    return max(0, numeric_value)


def _safe_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
