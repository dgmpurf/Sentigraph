# Sentigraph v5.6 Release Readiness

Status: local demo-ready mock/offline MVP.

This document describes what can be shown today, what remains mock or scaffold-only, and what must happen before any real API, real LLM, or production deployment work.

## Current Completed Capabilities

- FastAPI backend with deterministic mock analysis pipeline.
- React + Vite desktop dashboard frontend.
- Local JSON case management and deterministic demo seeding.
- V1.5 topic-risk scoring with real-crisis and manipulation-risk dimensions.
- Chinese public-opinion report builder and Markdown export.
- Monitoring snapshots, alerts, local notification outbox, scheduler metadata, and deterministic MVP forecasting.
- Platform registry, official API scaffolds, mock adapters, fixture-first public parser status, and selector repair mock tooling.
- LLM mock provider readiness and metadata-only usage guardrail pages.
- Offline benchmark harness with history, regression tracking, expanded datasets, report quality rubric, forecasting, parser fixtures, platform adapter mocks, Simulation Lab, case-to-simulation initializer, and strategy report suites.
- Simulation Lab backend and frontend MVP: deterministic aggregate simulation, bubble visualization, A/B intervention comparison, lawful content visibility backlash modeling, case-to-simulation initialization, and Markdown strategy report export.
- Demo Flow page for a guided local walkthrough.
- Browser smoke story and screenshot target list in `docs/demo_story.md`.

## Demo-Ready Features

- End-to-end local demo from `Demo Flow / 演示流程`.
- Tesla demo case creation/loading and mock analysis.
- V1.5 risk results across Dashboard, Analysis Result, Risk Monitor, and Summary Report.
- Chinese report and Markdown export.
- Risk Monitor deterministic forecast panel.
- Simulation Lab single scenario and A/B comparison.
- Content visibility tradeoff panel for lawful/platform-authorized visibility interventions.
- Simulation strategy Markdown report export.
- Benchmark Dashboard, LLM Safety, Platform Integration Overview, Public Parser Status, and Selector Repair Tool.

## Mock / Scaffold-Only Features

- All platform analysis uses local mock data or deterministic fixtures.
- Official API adapters for Chinese platforms are scaffolds only.
- Public parser previews are fixture-first and do not enable live fetch.
- Selector repair uses sanitized fixture HTML and mock selector suggestions.
- LLM providers other than `mock` are readiness placeholders.
- Local notifications are an in-app outbox simulation, not external delivery.
- Simulation Lab does not execute real-world strategy actions.
- Forecasting and Simulation Lab outputs are deterministic MVP estimates, not guaranteed predictions.

## Real API Pending Features

- Douyin: developer access is recorded and the planned app type is Web App, but redirect URI, test-account authorization, OAuth/token flow, `item.comment` permission, and lawful `item_id` source must be verified in the console before implementation.
- Xiaohongshu: developer access is recorded, but note/comment/interaction data API availability and access limits must be verified.
- Reddit: API approval remains pending before real mode should be enabled.
- Weibo: current application path is blocked by company-age requirement.
- Bilibili, Kuaishou, Zhihu, Douban, Toutiao, and other platforms remain future official API application work.
- No platform should be integrated through login bypass, captcha bypass, proxy rotation, scraping private data, or anti-bot evasion.

## Real LLM Pending Features

- OpenAI, DeepSeek, and Qwen real calls remain disabled.
- Real provider integration should happen only after a real data path is stable, guardrails are reviewed, prompt/raw-content logging is avoided, and offline benchmarks are used as regression checks.
- Any future real LLM work must not print API keys, `.env` values, raw prompts, raw user content, or raw responses.

## Non-Blocking Known Issues

- Vite production build reports a non-blocking large vendor chunk warning for Ant Design and ECharts.
- API smoke check requires a running local backend.
- Runtime data, benchmark summaries, and demo screenshots are local artifacts and should remain gitignored.
- Simulation Lab is not empirically calibrated against historical real events yet.
- There is no PDF export, legal/policy workflow, production authentication, or production deployment hardening.
- Browser screenshot/recording production is a documentation/demo asset task, not a product capability.

## Validation Expectations

Use local validation only:

```cmd
python -m pytest
python scripts\run_offline_benchmarks.py
npm --prefix frontend run build
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

Run the API smoke check only when the backend is already running at the chosen base URL.

GitHub Actions CI is intentionally disabled. Do not recreate `.github/workflows/ci.yml` unless explicitly requested.

## Next-Stage Options

1. Produce the final screenshot deck or short demo recording using `docs/demo_package.md` and `docs/demo_story.md`.
2. Audit Douyin and Xiaohongshu console permissions for comment/note-comment access.
3. Implement minimal real Douyin mode only after permission and payload shape are confirmed.
4. Add a policy/legal review checklist for Simulation Lab strategy reports.
5. Add optional PDF export for reports.
6. Plan real LLM integration later, behind provider gates and benchmark regression checks.
7. Calibrate Simulation Lab with historical replay data only after real data governance is settled.
