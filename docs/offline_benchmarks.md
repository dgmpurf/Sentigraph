# Sentigraph Offline Benchmarks

Status: v4.2 benchmark history and regression tracking implemented and QA-stabilized.

## Purpose

The offline benchmark harness gives Sentigraph a deterministic regression check before future real platform APIs or real LLM providers are enabled. It exercises the core mock-first product surfaces without requiring a backend server, API keys, live public fetching, or external network calls.

## Coverage

The current benchmark suites cover:

- sentiment analysis: English, Chinese, neutral/questioning, and mixed-language samples
- topic clustering and template summaries
- V1.5 topic risk scoring, including ordering and manipulation-risk signals
- report builder output shape
- Markdown export sections
- selector repair mock flow using sanitized fixture HTML
- public parser fixture parsing for `the_paper`, `jiemian`, `hupu`, `tieba`, `nga`, and `maimai`
- platform mock adapter normalization for `reddit`, `bilibili`, `weibo`, `douyin`, `kuaishou`, `xiaohongshu`, `zhihu`, `douban`, and `toutiao`

Fixtures live in:

```text
benchmarks/
```

The runner lives at:

```text
scripts/run_offline_benchmarks.py
```

## How To Run

From the repository root on Windows:

```cmd
python scripts\run_offline_benchmarks.py
```

The script prints a readable pass/fail summary and writes a generated latest JSON summary to:

```text
.benchmarks/offline_benchmark_summary.json
```

Each JSON-writing run also creates a timestamped summary-only history entry under:

```text
.benchmarks/history/
```

Generated `.benchmarks/` output is intentionally gitignored. To run without writing JSON or history output:

```cmd
python scripts\run_offline_benchmarks.py --no-json
```

If a required fixture file is missing or malformed, the runner prints a normal benchmark summary with the affected suite marked `FAIL` and exits nonzero. It should not drop a Python traceback for fixture-loading problems.

## Safety Guarantees

The harness is designed to remain offline and deterministic:

- no real OpenAI, DeepSeek, Qwen, or external LLM API calls
- no real platform API calls
- no live public fetching
- no crawlers
- no real notification delivery
- no API keys required
- no `.env` values printed
- no raw prompts or raw user content stored in generated benchmark summaries
- generated summaries contain pass/fail metadata only, not raw fixture HTML, prompts, API keys, or `.env` values

The script applies safe process-local defaults for mock/offline behavior. It does not modify `.env`.

## What It Does Not Cover

The current v4.x harness is intentionally small and coarse. It does not replace:

- a human-labeled sentiment evaluation dataset
- topic clustering quality metrics such as purity, recall, or NMI
- report quality review by humans
- large parser regression corpora
- real LLM output evaluation
- real provider latency, cost, timeout, retry, or rate-limit testing
- real platform integration benchmarks

## Future Use

Before enabling any real LLM provider or real platform API, run:

```cmd
python -m pytest
python scripts\run_offline_benchmarks.py
```

Future real-provider work should add mocked HTTP tests, provider-specific cost accounting, prompt/output schema tests, and human review datasets before any live call path is activated.

## Viewing Results In The UI

The Benchmark Dashboard / Evaluation Report page reads the latest generated summary through:

```http
GET /api/v1/benchmarks/latest
```

It also reads history and regression status through:

```http
GET /api/v1/benchmarks/history
GET /api/v1/benchmarks/regression
```

The endpoints read only:

```text
.benchmarks/offline_benchmark_summary.json
.benchmarks/history/
```

They do not run benchmarks automatically. Generate the summary first:

```cmd
python scripts\run_offline_benchmarks.py
```

Then start the local backend and frontend and open the sidebar item:

```text
Benchmarks / 离线评测
```

The dashboard displays totals, suite-level pass/fail counts, warning counts, generated time, benchmark version, history rows, and regression detection. Missing or malformed summary/history files return clear empty/error states without exposing project-local file paths. It intentionally does not expose benchmark case payloads, raw fixture content, prompts, API keys, `.env` values, or raw user content.

## Regression Detection

Each run compares the latest summary with the previous history entry, when one exists. The regression summary reports:

- `regression_detected`
- changed suites
- previous/latest total failures
- previous/latest total warnings
- previous/latest total passed counts
- reason categories such as `total_failed_increased`, `total_warnings_increased`, `suite_pass_to_fail`, and `total_passed_decreased`

If only one run exists, the regression endpoint returns `status="no_history"` so the UI can show `无历史记录可比较`. The comparison is summary-only and does not inspect or expose benchmark case payloads.
