# Sentigraph v6.3 Demo Screenshot Checklist

Last updated: 2026-05-20

Use this checklist when capturing the v6.3 YouTube real-data demo. Recommended storage for local captures is `.benchmarks/demo_smoke_screenshots/` or another ignored folder outside source control.

Safety reminder: do not capture `.env`, API keys, browser cookies, terminal history with credentials, or raw credential settings. The screenshot story should clearly distinguish:

- Real: YouTube public video/comment data.
- Offline deterministic: analysis, V1.5 risk, reports, monitoring, forecasting, and Simulation Lab.
- Mock: LLM provider.
- Scaffold/mock: other platform APIs unless future permissioned integrations are added.
- Pending: Douyin Web App OAuth and `item.comment` verification; no real Douyin API call is part of this demo.

## Required Screenshot Sequence

| # | Screenshot | Capture Target | What It Proves | Pre-Capture Check |
| --- | --- | --- | --- | --- |
| 1 | Dashboard showing YouTube real case | Dashboard overview with active YouTube case and provenance badges | The command center can present a real-data case while showing offline analysis and mock LLM status. | Badge row shows `Data: YouTube Real / Analysis: Offline / LLM: Mock`. |
| 2 | Keyword Search with YouTube real-data flow | Keyword Search with only YouTube selected | The UI exposes the explicit real-data sequence: create case, crawl/attach raw data, run analysis. | Buttons show `Create YouTube Real Case`, `Crawl YouTube & Attach Raw Data`, and `Run Case Analysis`. |
| 3 | Cases page showing completed YouTube case | Cases list/detail card | The YouTube case is persisted locally and completed. | Case status is completed and raw-data context is visible where implemented. |
| 4 | Analysis Result showing raw-data source | Analysis Result page | The analysis used attached case raw data instead of mock comments. | `analysis_input_source=case_raw_data` is visible. |
| 5 | Summary Report with YouTube-derived comments | Summary Report representative comments and Markdown controls | The report can surface YouTube-derived comments and export Markdown. | Comments are substantive public YouTube-derived examples; no raw JSON is visible. |
| 6 | Propagation Graph showing YouTube nodes | Propagation Graph canvas and details | The graph visualization remains connected for the YouTube-based case. | Node/platform labels are readable and no `[object Object]` appears. |
| 7 | Risk Monitor / Forecast | Risk Monitor forecast panel | Monitoring snapshots and deterministic forecast are visible. | Forecast copy states deterministic/limited confidence, not guaranteed prediction. |
| 8 | Simulation Lab initialized from case | Simulation Lab case-initialization summary and bubble view | The aggregate case result can initialize the sandbox. | Event frame, audience distribution, and aggregate-only safety copy are visible. |
| 9 | Simulation Lab A/B strategy comparison | A/B comparison mode with side-by-side panels | Transparent interventions can be compared from the same initial scenario. | Delta badges and human-review recommendation are visible. |
| 10 | Strategy report export | Simulation Lab strategy report Markdown card | The strategy rehearsal exports a review artifact. | Report shows human-review questions and limitations. |
| 11 | Benchmark Dashboard | Benchmarks page | Offline regression checks are available and passing. | Latest summary shows no failures or clearly documented status. |
| 12 | LLM Safety | LLM Safety page | The demo uses a mock LLM provider and real LLM calls are disabled. | Provider/status fields do not expose secrets. |
| 13 | Platform Integration Overview | Platform overview table/cards | YouTube is real-capable when configured; other platforms remain mock/scaffold. | The page does not imply all platforms are real. |
| 14 | Douyin readiness / platform status | Platform Integration Overview Douyin card or OAuth Pending section | Douyin Web App research/readiness is visible, but OAuth, `item.comment`, redirect URI, whitelist/test account, token flow, and lawful item-id source are still pending. | No UI implies Douyin real API calls are already integrated or enabled. |

## Optional Supporting Screenshots

- YouTube crawl metadata from Keyword Search after attach, showing `adapter_mode=real`, `fallback_used=false`, `cache_hit`, and `quota_guardrail_status`.
- Markdown case report export preview.
- Simulation Lab content visibility tradeoff panel for lawful/platform-authorized visibility intervention.
- Demo Flow page showing the overall local demo route.
- Public Parser Status and Selector Repair Tool to show fixture/mock-only parser safety.

## Filename Suggestions

```text
01_dashboard_youtube_real_case.png
02_keyword_search_youtube_real_flow.png
03_cases_completed_youtube_case.png
04_analysis_case_raw_data.png
05_summary_report_youtube_comments.png
06_propagation_graph_youtube_case.png
07_risk_monitor_forecast.png
08_simulation_lab_case_initialized.png
09_simulation_lab_ab_comparison.png
10_strategy_report_export.png
11_benchmark_dashboard.png
12_llm_safety_mock_provider.png
13_platform_integration_overview.png
14_douyin_readiness_platform_status.png
```

## QA Before Capture

- Run `python -m pytest`.
- Run `python scripts\run_offline_benchmarks.py`.
- Run `npm --prefix frontend run build`.
- Start backend and frontend locally.
- Confirm the YouTube case has `analysis_input_source=case_raw_data`.
- Confirm no forbidden Simulation Lab tactics appear as selectable UI options.
- Confirm no real LLM status is shown.
- Confirm no screenshots reveal API keys, `.env` values, or private data.
