from __future__ import annotations

from fastapi import APIRouter

from app.schemas.benchmark import (
    BenchmarkHistoryResponse,
    BenchmarkRegressionResponse,
    LatestBenchmarkSummaryResponse,
)
from app.services.benchmark_summary import (
    load_benchmark_history,
    load_benchmark_regression,
    load_latest_benchmark_summary,
)


router = APIRouter()


@router.get("/latest", response_model=LatestBenchmarkSummaryResponse)
def get_latest_benchmark_summary() -> LatestBenchmarkSummaryResponse:
    """Return the latest generated offline benchmark summary.

    The API reads the project-local summary file only. It does not run
    benchmark suites, call external APIs, or expose per-case benchmark payloads.
    """

    return load_latest_benchmark_summary()


@router.get("/history", response_model=BenchmarkHistoryResponse)
def get_benchmark_history() -> BenchmarkHistoryResponse:
    """Return project-local offline benchmark history entries.

    The API reads generated summary-only history files. It does not run
    benchmarks, expose local file paths, or return per-case benchmark payloads.
    """

    return load_benchmark_history()


@router.get("/regression", response_model=BenchmarkRegressionResponse)
def get_benchmark_regression() -> BenchmarkRegressionResponse:
    """Return the latest offline benchmark regression comparison.

    The API compares summary metadata only and never triggers benchmark runs or
    external services.
    """

    return load_benchmark_regression()
