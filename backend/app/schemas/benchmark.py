from pydantic import BaseModel, Field


class BenchmarkSuiteSummary(BaseModel):
    suite: str
    status: str = "unknown"
    passed: int = 0
    failed: int = 0
    warnings: list[str] = Field(default_factory=list)


class LatestBenchmarkSummaryResponse(BaseModel):
    source: str = "offline_benchmark_summary"
    available: bool = False
    status: str = "missing"
    generated_at: str | None = None
    benchmark_version: str | None = None
    total_passed: int = 0
    total_failed: int = 0
    total_warnings: int = 0
    suites: list[BenchmarkSuiteSummary] = Field(default_factory=list)
    message: str = ""
