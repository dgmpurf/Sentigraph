# Sentigraph Demo Readiness Checklist

Last updated: 2026-05-17

## Purpose

This is the short checklist for preparing a stable local Sentigraph demo. The full historical checklist remains in `docs/demo_checklist.md`; this file is the freeze-stage demo plan.

## Demo Boundary

The demo is offline/mock-first.

Do not enable:

- real platform APIs
- real crawlers
- live public fetching
- real LLM calls
- real notifications
- GitHub Actions CI
- API key input or `.env` modification from the UI

## Required Pre-Demo Commands

From the repository root:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m pytest
python scripts\run_offline_benchmarks.py
python scripts\reset_local_data.py --yes
python scripts\seed_demo_cases.py --reset-first
```

Start backend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
set CASE_STORE_BACKEND=local_json
set PUBLIC_PARSER_LIVE_FETCH_ENABLED=false
set LLM_PROVIDER=mock
set LLM_ENABLE_REAL_CALLS=false
python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000
```

Start frontend:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run dev
```

Build check:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm run build
```

Optional local API smoke check after backend starts:

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000
```

## Demo Story

1. Open `http://127.0.0.1:5173`.
2. Show Dashboard and selected project status.
3. Open Cases and select a seeded completed case.
4. Show Analysis Result with V1.5 topic risk.
5. Open Summary Report:
   - risk score
   - risk level
   - risk model version
   - key findings
   - representative comments
   - recommended actions
   - suggested public response
6. Copy or download the Markdown report.
7. Open Risk Monitor and run a mock monitoring check.
8. Show alerts and local notifications.
9. Open Platform Integration Overview:
   - official API scaffolds are mock-only
   - public parsers are fixture-first
   - Reddit is API-pending
10. Open LLM Safety:
   - MockProvider default
   - real calls disabled
   - API key state boolean-only
   - no prompt logging
11. Open Benchmarks:
   - latest benchmark summary
   - history
   - regression status

## Demo Pages To Verify

- Dashboard
- Keyword Search
- Cases
- Analysis Result
- Summary Report
- Risk Monitor
- Propagation Graph
- Notifications
- Public Parser Status
- Platform Integration Overview
- Selector Repair Tool
- LLM Safety
- Benchmarks

## Expected Demo Claims

Safe claims:

- "The mock-first MVP can demonstrate the end-to-end workflow offline."
- "The system has a V1.5 topic-risk layer and Chinese report generation."
- "Official API adapters are scaffolded but real modes remain disabled."
- "LLM integration is mock-only by default and real providers are disabled."
- "Offline benchmarks track regressions before real API or LLM work."

Do not claim:

- production readiness
- live monitoring of real platforms
- real Douyin/Xiaohongshu/Reddit integration
- real LLM intelligence
- real notification delivery
- compliance approval

## Known Non-Blocking Demo Issues

- Some older Chinese labels/docs may show mojibake and should be polished before a public-facing demo.
- Vite may report large vendor chunks for Ant Design/ECharts.
- Benchmark history is local file-based.
- Public parser examples are fixture-only and synthetic/sanitized.

## Demo Ready Criteria

- Backend tests pass.
- Offline benchmarks pass.
- Frontend build passes.
- Seeded cases load.
- Summary Report renders.
- Markdown export works.
- Risk Monitor mock check works.
- LLM Safety and Platform Integration Overview show safe disabled-real-mode state.
- No real API, real crawler, live public fetch, real LLM, or real notification is enabled.
