from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.schemas.benchmark import (
    BenchmarkHistoryEntry,
    BenchmarkHistoryResponse,
    BenchmarkRegressionResponse,
    BenchmarkRegressionSuiteChange,
    BenchmarkSuiteSummary,
    LatestBenchmarkSummaryResponse,
)


def _find_project_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists():
            return parent
    return Path.cwd()


DEFAULT_BENCHMARK_SUMMARY_PATH = (
    _find_project_root() / ".benchmarks" / "offline_benchmark_summary.json"
)
DEFAULT_BENCHMARK_HISTORY_DIR = _find_project_root() / ".benchmarks" / "history"


def load_latest_benchmark_summary(
    summary_path: str | Path | None = None,
) -> LatestBenchmarkSummaryResponse:
    payload, status = _read_json_object(
        Path(summary_path) if summary_path is not None else DEFAULT_BENCHMARK_SUMMARY_PATH
    )
    if status == "missing":
        return LatestBenchmarkSummaryResponse(
            available=False,
            status="missing",
            message=(
                "No offline benchmark summary found. Run "
                "python scripts/run_offline_benchmarks.py to generate it."
            ),
        )

    if status == "malformed" or payload is None:
        return LatestBenchmarkSummaryResponse(
            available=False,
            status="malformed",
            message="Offline benchmark summary exists but could not be parsed safely.",
        )

    suites = _safe_suites(payload.get("suites"))
    total_warnings = _safe_int(
        payload.get("total_warnings"),
        fallback=sum(len(suite.warnings) for suite in suites),
    )
    regression_summary = payload.get("regression_summary")
    regression_detected = (
        bool(regression_summary.get("regression_detected"))
        if isinstance(regression_summary, dict)
        else None
    )

    return LatestBenchmarkSummaryResponse(
        available=True,
        status="available",
        benchmark_id=_safe_optional_text(payload.get("benchmark_id")),
        generated_at=_safe_optional_text(payload.get("generated_at")),
        benchmark_version=_safe_optional_text(payload.get("benchmark_version")),
        duration_seconds=_safe_optional_float(payload.get("duration_seconds")),
        total_passed=_safe_int(payload.get("total_passed")),
        total_failed=_safe_int(payload.get("total_failed")),
        total_warnings=total_warnings,
        suites=suites,
        regression_detected=regression_detected,
        message="Latest offline benchmark summary loaded.",
    )


def load_benchmark_history(
    history_dir: str | Path | None = None,
    *,
    limit: int = 20,
) -> BenchmarkHistoryResponse:
    directory = Path(history_dir) if history_dir is not None else DEFAULT_BENCHMARK_HISTORY_DIR
    if not directory.exists() or not directory.is_dir():
        return BenchmarkHistoryResponse(
            available=False,
            status="missing",
            message="No benchmark history directory found. Run python scripts/run_offline_benchmarks.py to create history.",
        )

    entries: list[BenchmarkHistoryEntry] = []
    malformed_entries = 0
    for path in sorted(directory.glob("*.json"), reverse=True):
        payload, status = _read_json_object(path)
        if status != "available" or payload is None:
            malformed_entries += 1
            continue
        entry = _safe_history_entry(payload)
        if entry is None:
            malformed_entries += 1
            continue
        entries.append(entry)

    entries.sort(key=lambda entry: entry.generated_at or "", reverse=True)
    limited_entries = entries[: max(1, min(limit, 100))]
    if not entries and malformed_entries:
        return BenchmarkHistoryResponse(
            available=False,
            status="malformed",
            total_entries=0,
            malformed_entries=malformed_entries,
            message="Benchmark history exists but no entry could be parsed safely.",
        )

    return BenchmarkHistoryResponse(
        available=bool(limited_entries),
        status="available" if limited_entries else "missing",
        total_entries=len(entries),
        malformed_entries=malformed_entries,
        entries=limited_entries,
        message=(
            "Benchmark history loaded."
            if limited_entries
            else "No benchmark history entries found. Run python scripts/run_offline_benchmarks.py to create history."
        ),
    )


def load_benchmark_regression(
    summary_path: str | Path | None = None,
    history_dir: str | Path | None = None,
) -> BenchmarkRegressionResponse:
    latest_payload, latest_status = _read_json_object(
        Path(summary_path) if summary_path is not None else DEFAULT_BENCHMARK_SUMMARY_PATH
    )
    if latest_status == "missing":
        return BenchmarkRegressionResponse(
            available=False,
            status="missing",
            message="No offline benchmark summary found for regression comparison.",
        )
    if latest_status == "malformed" or latest_payload is None:
        return BenchmarkRegressionResponse(
            available=False,
            status="malformed",
            message="Offline benchmark summary exists but could not be parsed safely.",
        )

    embedded_regression = latest_payload.get("regression_summary")
    if isinstance(embedded_regression, dict):
        return _safe_regression_response(embedded_regression)

    history_response = load_benchmark_history(history_dir)
    latest_id = _safe_optional_text(latest_payload.get("benchmark_id"))
    previous_entry = next(
        (
            entry
            for entry in history_response.entries
            if entry.benchmark_id and entry.benchmark_id != latest_id
        ),
        None,
    )
    if previous_entry is None:
        return BenchmarkRegressionResponse(
            available=False,
            status="no_history",
            latest_benchmark_id=latest_id,
            latest_generated_at=_safe_optional_text(latest_payload.get("generated_at")),
            latest_total_failed=_safe_int(latest_payload.get("total_failed")),
            latest_total_warnings=_safe_int(latest_payload.get("total_warnings")),
            latest_total_passed=_safe_int(latest_payload.get("total_passed")),
            message="No previous benchmark history entry is available for comparison.",
        )

    latest_summary = _safe_summary_dict(latest_payload)
    previous_summary = _history_entry_to_dict(previous_entry)
    return _safe_regression_response(_compare_summaries(latest_summary, previous_summary))


def _safe_history_entry(payload: dict[str, Any]) -> BenchmarkHistoryEntry | None:
    benchmark_id = _safe_optional_text(payload.get("benchmark_id"))
    if not benchmark_id:
        return None
    return BenchmarkHistoryEntry(
        source="offline_benchmark",
        benchmark_id=benchmark_id,
        generated_at=_safe_optional_text(payload.get("generated_at")),
        benchmark_version=_safe_optional_text(payload.get("benchmark_version")),
        duration_seconds=_safe_optional_float(payload.get("duration_seconds")),
        total_passed=_safe_int(payload.get("total_passed")),
        total_failed=_safe_int(payload.get("total_failed")),
        total_warnings=_safe_int(payload.get("total_warnings")),
        suites=_safe_suites(payload.get("suites")),
        regression_detected=(
            bool(payload.get("regression_detected"))
            if "regression_detected" in payload
            else None
        ),
    )


def _safe_regression_response(payload: dict[str, Any]) -> BenchmarkRegressionResponse:
    changed_suites = []
    raw_changes = payload.get("changed_suites")
    if isinstance(raw_changes, list):
        for item in raw_changes:
            if not isinstance(item, dict):
                continue
            suite_name = _safe_optional_text(item.get("suite"))
            if not suite_name:
                continue
            change_types = item.get("change_types")
            changed_suites.append(
                BenchmarkRegressionSuiteChange(
                    suite=suite_name,
                    change_types=[str(value) for value in change_types] if isinstance(change_types, list) else [],
                    previous_status=_safe_optional_text(item.get("previous_status")) or "unknown",
                    latest_status=_safe_optional_text(item.get("latest_status")) or "unknown",
                    previous_failed=_safe_int(item.get("previous_failed")),
                    latest_failed=_safe_int(item.get("latest_failed")),
                    previous_warnings=_safe_int(item.get("previous_warnings")),
                    latest_warnings=_safe_int(item.get("latest_warnings")),
                )
            )
    reason_categories = payload.get("reason_categories")
    return BenchmarkRegressionResponse(
        available=bool(payload.get("available")),
        status=_safe_optional_text(payload.get("status")) or "unknown",
        regression_detected=bool(payload.get("regression_detected")),
        changed_suites=changed_suites,
        previous_benchmark_id=_safe_optional_text(payload.get("previous_benchmark_id")),
        latest_benchmark_id=_safe_optional_text(payload.get("latest_benchmark_id")),
        previous_generated_at=_safe_optional_text(payload.get("previous_generated_at")),
        latest_generated_at=_safe_optional_text(payload.get("latest_generated_at")),
        previous_total_failed=_safe_optional_int(payload.get("previous_total_failed")),
        latest_total_failed=_safe_int(payload.get("latest_total_failed")),
        previous_total_warnings=_safe_optional_int(payload.get("previous_total_warnings")),
        latest_total_warnings=_safe_int(payload.get("latest_total_warnings")),
        previous_total_passed=_safe_optional_int(payload.get("previous_total_passed")),
        latest_total_passed=_safe_int(payload.get("latest_total_passed")),
        reason_categories=[str(value) for value in reason_categories] if isinstance(reason_categories, list) else [],
        message=_safe_optional_text(payload.get("message")) or "",
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
                case_count=_safe_int(
                    item.get("case_count"),
                    fallback=_safe_int(item.get("passed")) + _safe_int(item.get("failed")),
                ),
                passed=_safe_int(item.get("passed")),
                failed=_safe_int(item.get("failed")),
                warnings=[str(warning) for warning in warnings] if isinstance(warnings, list) else [],
            )
        )
    return suites


def _safe_summary_dict(payload: dict[str, Any]) -> dict[str, Any]:
    suites = _safe_suites(payload.get("suites"))
    return {
        "benchmark_id": _safe_optional_text(payload.get("benchmark_id")),
        "generated_at": _safe_optional_text(payload.get("generated_at")),
        "total_passed": _safe_int(payload.get("total_passed")),
        "total_failed": _safe_int(payload.get("total_failed")),
        "total_warnings": _safe_int(
            payload.get("total_warnings"),
            fallback=sum(len(suite.warnings) for suite in suites),
        ),
        "suites": [suite.model_dump() for suite in suites],
    }


def _history_entry_to_dict(entry: BenchmarkHistoryEntry) -> dict[str, Any]:
    return {
        "benchmark_id": entry.benchmark_id,
        "generated_at": entry.generated_at,
        "total_passed": entry.total_passed,
        "total_failed": entry.total_failed,
        "total_warnings": entry.total_warnings,
        "suites": [suite.model_dump() for suite in entry.suites],
    }


def _compare_summaries(latest_summary: dict[str, Any], previous_summary: dict[str, Any]) -> dict[str, Any]:
    latest_total_failed = _safe_int(latest_summary.get("total_failed"))
    latest_total_warnings = _safe_int(latest_summary.get("total_warnings"))
    latest_total_passed = _safe_int(latest_summary.get("total_passed"))
    previous_total_failed = _safe_int(previous_summary.get("total_failed"))
    previous_total_warnings = _safe_int(previous_summary.get("total_warnings"))
    previous_total_passed = _safe_int(previous_summary.get("total_passed"))
    changed_suites = _build_changed_suites(latest_summary, previous_summary)
    reason_categories: list[str] = []
    if latest_total_failed > previous_total_failed:
        reason_categories.append("total_failed_increased")
    if latest_total_warnings > previous_total_warnings:
        reason_categories.append("total_warnings_increased")
    if latest_total_passed < previous_total_passed:
        reason_categories.append("total_passed_decreased")
    if any("suite_pass_to_fail" in change["change_types"] for change in changed_suites):
        reason_categories.append("suite_pass_to_fail")
    regression_detected = bool(reason_categories or changed_suites)
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
        "reason_categories": reason_categories,
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
    latest_suites = _suite_map(latest_summary.get("suites"))
    previous_suites = _suite_map(previous_summary.get("suites"))
    changed: list[dict[str, Any]] = []
    for suite_name in sorted(set(latest_suites) | set(previous_suites)):
        latest_suite = latest_suites.get(suite_name, {})
        previous_suite = previous_suites.get(suite_name, {})
        previous_status = _safe_optional_text(previous_suite.get("status")) or "missing"
        latest_status = _safe_optional_text(latest_suite.get("status")) or "missing"
        previous_failed = _safe_int(previous_suite.get("failed"))
        latest_failed = _safe_int(latest_suite.get("failed"))
        previous_warnings = len(previous_suite.get("warnings") or [])
        latest_warnings = len(latest_suite.get("warnings") or [])
        change_types: list[str] = []
        if previous_status == "pass" and latest_status == "fail":
            change_types.append("suite_pass_to_fail")
        if latest_failed > previous_failed:
            change_types.append("new_failures")
        if latest_warnings > previous_warnings:
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
                "previous_warnings": previous_warnings,
                "latest_warnings": latest_warnings,
            }
        )
    return changed


def _suite_map(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, list):
        return {}
    suites: dict[str, dict[str, Any]] = {}
    for item in value:
        if hasattr(item, "model_dump"):
            item = item.model_dump()
        if not isinstance(item, dict):
            continue
        suite_name = _safe_optional_text(item.get("suite"))
        if suite_name:
            suites[suite_name] = item
    return suites


def _read_json_object(path: Path) -> tuple[dict[str, Any] | None, str]:
    if not path.exists():
        return None, "missing"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "malformed"
    if not isinstance(payload, dict):
        return None, "malformed"
    return payload, "available"


def _safe_int(value: Any, fallback: int = 0) -> int:
    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        return fallback
    return max(0, numeric_value)


def _safe_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        return None
    return max(0, numeric_value)


def _safe_optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, numeric_value)


def _safe_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
