from __future__ import annotations

from fastapi import APIRouter

from app.schemas.benchmark import LatestBenchmarkSummaryResponse
from app.services.benchmark_summary import load_latest_benchmark_summary


router = APIRouter()


@router.get("/latest", response_model=LatestBenchmarkSummaryResponse)
def get_latest_benchmark_summary() -> LatestBenchmarkSummaryResponse:
    """Return the latest generated offline benchmark summary.

    The API reads the project-local summary file only. It does not run
    benchmark suites, call external APIs, or expose per-case benchmark payloads.
    """

    return load_latest_benchmark_summary()
