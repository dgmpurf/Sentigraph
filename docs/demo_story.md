# Sentigraph Demo Story

Last updated: 2026-05-18

## Product Summary

Sentigraph is a mock-first, desktop public-opinion intelligence dashboard that turns a keyword-driven case into deterministic offline analysis, V1.5 topic risk scoring, Chinese reports, monitoring/forecasting, ethical Simulation Lab rehearsal, benchmark status, and LLM/platform safety diagnostics. The current demo uses local mock/offline data only and does not call real platform APIs, real crawlers, live public pages, or real LLM APIs.

## Demo Script

1. Reset and seed deterministic local data:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\reset_local_data.py --yes
python scripts\seed_demo_cases.py --reset-first
python scripts\run_offline_benchmarks.py
```

2. Start the backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=local_json
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

3. Start the frontend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

4. Open the frontend, usually `http://127.0.0.1:5173`. If that port is occupied, use the alternate port printed by Vite or run `npm run dev -- --host 127.0.0.1 --port 5174`.
5. Open `Demo Flow / 演示流程` and click `一键准备演示数据` if the page has not already loaded the Tesla demo case.
6. Walk the cards in order: create/load case, run mock analysis, inspect V1.5 risk, open the Chinese report, export Markdown, initialize Simulation Lab, run A/B comparison, export the Simulation Lab strategy report, then open Benchmarks and LLM Safety.
7. Finish by opening `平台接入总览`, `公开页面解析`, and `Selector 修复工具` to show real integrations remain disabled or fixture/mock-only.

## Screenshot Checklist

During the 2026-05-18 browser smoke, screenshots were captured under `.benchmarks/demo_smoke_screenshots/` for local review. Recommended demo screenshots:

| Target | What It Proves |
| --- | --- |
| `01_dashboard_overview.png` | The command center loads risk, topic, chart, alert, and platform summaries. |
| `02_demo_flow.png` / `03_demo_flow_ready.png` | The one-page demo guide is visible and clearly labeled mock/offline. |
| `05_analysis_v15_topic_risk.png` | V1.5 topic-risk fields and top risk topics are visible. |
| `06_chinese_summary_report.png` | The Chinese public-opinion report and public-response draft are available. |
| `07_risk_monitor_forecast.png` | Monitoring and deterministic forecasting are visible. |
| `09_simulation_case_initialized.png` | Simulation Lab can initialize from aggregate case data. |
| `10_simulation_single_run.png` | Bubble simulation runs with aggregate metrics and explanations. |
| `13_simulation_ab_comparison_visibility.png` | A/B strategy comparison and visibility tradeoff panel work. |
| `14_simulation_ab_strategy_report.png` | Strategy report Markdown export is available and human-review-oriented. |
| `15_benchmark_dashboard.png` | Offline benchmark summary is visible. |
| `16_llm_safety_final.png` | LLM Safety page shows mock provider and real-call disabled status. |
| `17_platform_integration_overview.png` | Platform real modes remain disabled/pending, with fixture/mock status. |

## Browser Smoke Result

- Frontend pages loaded: Demo Flow, Dashboard, Cases, Analysis Result, Summary Report, Risk Monitor, Simulation Lab, Benchmarks, LLM Safety, Platform Integration Overview, Public Parser Status, and Selector Repair Tool.
- Simulation Lab actions verified: case initialization from `case_001`, single-scenario run, A/B comparison, content visibility tradeoff panel, strategy report export, and allowed-intervention dropdown.
- Scoped intervention dropdown options contained only allowed transparent responses and lawful visibility actions; forbidden tactics were not selectable.
- No raw `[object Object]` rendering was observed on smoked pages.
- A small Ant Design table warning on the LLM Safety usage table was fixed by switching to a stable string `rowKey`.

## Current Limitations

- The demo remains mock/offline and deterministic; it is not a production monitoring system.
- Real platform APIs, real public crawling, real LLM calls, authentication, production persistence, and external notifications remain disabled or future work.
- Simulation Lab outputs are aggregate scenario-rehearsal signals only. They are not guarantees of real-world outcomes and must not be treated as automatic strategy execution.
- PDF export, richer Simulation Lab animation, empirical calibration, and policy/legal review workflow are future tasks.

## Safety Note

The demo does not call real APIs or real LLM APIs, does not enable live public fetching, does not implement crawlers, and does not expose fake consensus, bot amplification, fake events, covert seeding, deceptive distraction, individual-level persuasion targeting, account-level influenceability scoring, harassment, or suppression tactics. Simulation Lab output is aggregate-level and human-review-oriented.
