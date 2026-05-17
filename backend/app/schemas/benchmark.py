from pydantic import BaseModel, Field


class BenchmarkSuiteSummary(BaseModel):
    suite: str
    status: str = "unknown"
    case_count: int = 0
    passed: int = 0
    failed: int = 0
    warnings: list[str] = Field(default_factory=list)


class BenchmarkRegressionSuiteChange(BaseModel):
    suite: str
    change_types: list[str] = Field(default_factory=list)
    previous_status: str = "unknown"
    latest_status: str = "unknown"
    previous_failed: int = 0
    latest_failed: int = 0
    previous_warnings: int = 0
    latest_warnings: int = 0


class BenchmarkRegressionResponse(BaseModel):
    source: str = "offline_benchmark_regression"
    available: bool = False
    status: str = "missing"
    regression_detected: bool = False
    changed_suites: list[BenchmarkRegressionSuiteChange] = Field(default_factory=list)
    previous_benchmark_id: str | None = None
    latest_benchmark_id: str | None = None
    previous_generated_at: str | None = None
    latest_generated_at: str | None = None
    previous_total_failed: int | None = None
    latest_total_failed: int = 0
    previous_total_warnings: int | None = None
    latest_total_warnings: int = 0
    previous_total_passed: int | None = None
    latest_total_passed: int = 0
    reason_categories: list[str] = Field(default_factory=list)
    message: str = ""


class BenchmarkHistoryEntry(BaseModel):
    source: str = "offline_benchmark"
    benchmark_id: str
    generated_at: str | None = None
    benchmark_version: str | None = None
    duration_seconds: float | None = None
    total_passed: int = 0
    total_failed: int = 0
    total_warnings: int = 0
    suites: list[BenchmarkSuiteSummary] = Field(default_factory=list)
    regression_detected: bool | None = None


class BenchmarkHistoryResponse(BaseModel):
    source: str = "offline_benchmark_history"
    available: bool = False
    status: str = "missing"
    total_entries: int = 0
    malformed_entries: int = 0
    entries: list[BenchmarkHistoryEntry] = Field(default_factory=list)
    message: str = ""


class LatestBenchmarkSummaryResponse(BaseModel):
    source: str = "offline_benchmark_summary"
    available: bool = False
    status: str = "missing"
    benchmark_id: str | None = None
    generated_at: str | None = None
    benchmark_version: str | None = None
    duration_seconds: float | None = None
    total_passed: int = 0
    total_failed: int = 0
    total_warnings: int = 0
    suites: list[BenchmarkSuiteSummary] = Field(default_factory=list)
    regression_detected: bool | None = None
    message: str = ""
