# Sentigraph v5.6 Demo Package

Status: demo-ready mock/offline MVP package.

This package explains how to present Sentigraph locally to collaborators, reviewers, or future users without real platform APIs, real LLM APIs, live public fetching, real crawlers, real notifications, authentication, or production deployment.

## Demo Story

Sentigraph demonstrates a mock-first public-opinion intelligence workflow: create or load a deterministic Tesla demo case, run offline analysis, inspect V1.5 topic risk, read the Chinese public-opinion report, export Markdown, initialize Simulation Lab from aggregate case data, compare two transparent response strategies, export a Simulation Lab strategy report, then verify offline benchmarks and LLM Safety status.

The story to tell:

1. Sentigraph can turn a keyword into a local case workspace.
2. The mock pipeline produces deterministic sentiment, topic, risk, report, monitoring, forecast, and alert outputs.
3. Simulation Lab can rehearse aggregate crisis-response scenarios from case data without targeting individuals.
4. Benchmarks and safety pages show that the demo is offline, deterministic, and real-call disabled.

## Recommended Screenshot Sequence

Generated screenshots can live under `.benchmarks/demo_smoke_screenshots/`; that directory is runtime output and should remain gitignored.

1. Demo Flow page.
2. Dashboard overview.
3. Cases page with the Tesla demo case.
4. Analysis Result with V1.5 topic-risk cards.
5. Chinese Summary Report and Markdown export controls.
6. Risk Monitor with deterministic forecast panel.
7. Simulation Lab bubble view before running.
8. Simulation Lab initialized from the case.
9. Simulation Lab single-scenario run.
10. Simulation Lab A/B comparison.
11. Content visibility tradeoff panel.
12. Simulation strategy report export card.
13. Benchmark Dashboard.
14. LLM Safety page.
15. Platform Integration Overview.
16. Public Parser Status.
17. Selector Repair Tool.

## Exact Local Run Commands

Run from the repository root unless a command says otherwise.

Reset and seed deterministic demo data:

```cmd
python scripts\reset_local_data.py --yes
python scripts\seed_demo_cases.py --reset-first
```

Run offline benchmarks:

```cmd
python scripts\run_offline_benchmarks.py
```

Start the backend:

```cmd
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Start the frontend in a second terminal:

```cmd
npm --prefix frontend run dev
```

Open:

```text
http://127.0.0.1:5173
```

Optional local API smoke check while the backend is running:

```cmd
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

Full local validation:

```cmd
python -m pytest
python scripts\run_offline_benchmarks.py
npm --prefix frontend run build
```

## Demo Talking Points

- Mock/offline by design: every screen in the demo is safe to run without credentials.
- V1.5 topic risk explains risk by topic rather than only by a single global score.
- Chinese reports and Markdown exports show how Sentigraph can support analyst handoff.
- Risk Monitor forecasting is deterministic MVP trend extrapolation from local snapshots, not a guaranteed prediction.
- Simulation Lab compares transparent, aggregate crisis-response options and requires human review.
- Content visibility modeling estimates lawful/platform-authorized governance tradeoffs; it does not execute platform actions.
- LLM Safety shows mock provider status and metadata-only usage guardrails; it does not call OpenAI, DeepSeek, Qwen, or any external model.
- Benchmark Dashboard shows offline regression protection before future real API or real LLM work.

## What Each Screen Proves

| Screen | What it proves |
| --- | --- |
| Demo Flow | The local demo path is guided and does not require manual page-hunting. |
| Dashboard | Mock analysis results can be summarized in an operations dashboard. |
| Cases | Case data persists locally and can be reopened for demo continuity. |
| Analysis Result | V1.5 topic-risk outputs are visible and deterministic. |
| Summary Report | Chinese report output and Markdown export are available. |
| Risk Monitor | Monitoring snapshots, alerts, local notifications, and deterministic forecasting are wired. |
| Simulation Lab | Aggregate scenario simulation, A/B comparison, visibility tradeoffs, and strategy export are demo-ready. |
| Benchmarks | Offline benchmark suites run without backend server, API keys, live fetch, or external LLMs. |
| LLM Safety | Real LLM calls remain disabled and only safe metadata is displayed. |
| Platform Integration Overview | Real platform APIs are documented as pending/scaffold-only, not integrated. |
| Public Parser Status | Parser fixtures can be inspected without live fetching. |
| Selector Repair Tool | Selector repair is mock/fixture-only and does not change active profiles automatically. |

## Known Limitations

- This is not a production release.
- No authentication, multi-user roles, production database hardening, or deployment hardening is included.
- Real platform APIs are not integrated.
- Real LLM calls are not integrated.
- Live public fetching and real crawlers remain disabled.
- Simulation Lab is deterministic and aggregate-level; it is not empirically calibrated to guarantee real-world outcomes.
- Browser screenshots are local demo artifacts and should remain under ignored runtime output such as `.benchmarks/`.
- Vite may report a non-blocking large vendor chunk warning for Ant Design and ECharts.

## Safety and Ethics Boundaries

- No real APIs or real LLM APIs are required or called.
- No API keys, `.env` values, raw prompts, or raw user content should be printed in logs.
- No bot amplification, fake consensus, fake events, covert influencer seeding, deceptive attention diversion, individual-level persuasion targeting, account-level influenceability scoring, harassment, or suppression tactic is implemented.
- Content visibility simulation is limited to lawful/platform-authorized aggregate tradeoff analysis and human review.
- Real-world actions require policy, legal, and human review outside Sentigraph.

