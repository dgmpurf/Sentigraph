# Sentigraph v6.28 Full Demo Package

Status: demo-readiness package for local presentation and recording.

Sentigraph is a mock-default, YouTube-real-capable, evidence-ingestion-ready desktop web MVP for public-opinion analysis. The current demo shows how evidence can enter a case from several safe sources, how the offline analysis stack summarizes it, how reviewers can mark weak, duplicate, or rejected evidence before downstream analysis, and how third-party vendor samples can be evaluated through an offline POC path before any live adapter work.

For final manual screenshot and recording production, use [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md). It contains the 21-screenshot asset list, recommended filenames, short and full recording scripts, capture commands, privacy checklist, and non-overclaim talking points.

For step-by-step local operation, use [operation_guide_v6_28.md](operation_guide_v6_28.md).

## What v6.28 Demonstrates

- Optional YouTube real-data demo when local `.env` has `YOUTUBE_ADAPTER_MODE=real` and `YOUTUBE_API_KEY`.
- CSV/Excel Evidence Import with preview, commit, template download, normalization, deduplication, and safety handling.
- Manual URL / manual text evidence entry without automatic URL fetching.
- Vendor Sample POC utilities: intake checklist, sample schema, offline CSV/JSON mapping utility, scoring rubric, scorecard template, and conservative `data_vendor` / `medium_low` trust mapping.
- Source Catalog and Feasibility Matrix for compliant acquisition planning.
- Mock-only Search Discovery candidate review.
- RSS Mock and GDELT Mock provider selector for future discovery planning.
- Evidence Trust, Provenance, Deduplication, Review Queue, and Audit Timeline.
- Evidence Scale / Coverage summaries and local batch-job scaffold.
- Offline deterministic Analysis Result, Summary Report / Markdown export, Risk Monitor / Forecast, and Simulation Lab.
- Benchmark Dashboard, LLM Safety, and Platform Integration Overview.

## Real vs Offline vs Mock

| Area | Current status | Boundary |
| --- | --- | --- |
| YouTube data | Optional local real-data demo | Public video/comment data through official API only when locally configured. Automated tests do not call YouTube. |
| Analysis pipeline | Offline deterministic | Uses case raw data or normalized evidence when present; no real LLM call. |
| Risk / forecast | Offline deterministic | Scenario support, not a guarantee of future outcomes. |
| Simulation Lab | Offline deterministic | Strategy rehearsal only; it does not execute real-world actions. |
| Reports / Markdown | Offline deterministic | Summarizes available/imported evidence and includes caveats for weak or unverified evidence. |
| Search Discovery | Mock/static | Generates local candidate metadata only; no live search API and no URL fetching. |
| RSS / GDELT providers | Mock/static | Local fixtures for future provider UX; no RSS or GDELT network calls. |
| Vendor Sample POC | Offline utility | Local CSV/JSON mapping and scorecard review only; no vendor API, no live adapter, and no official platform verification claim. |
| LLM provider | Mock | LLM Safety UI documents provider status; no real LLM calls are made. |
| Douyin / Bilibili / other platforms | Pending or scaffold | Official API/OAuth/permission gates remain unresolved. |
| MediaCrawler | Not integrated | No cookie crawling, captcha bypass, proxy evasion, or anti-bot bypass. |

## Local Run Commands

Run all commands from the repository root:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Validation commands:

```powershell
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

## Recommended Demo Flow

1. Dashboard: show current case status and safety framing.
2. Keyword Search: optional YouTube real-data flow, if local key is configured.
3. Cases: show CSV/Excel import, template download, manual URL evidence, and evidence summaries.
4. Vendor Sample POC: show intake checklist, offline mapper output, and scorecard template as a supporting path, not a live integration.
5. Evidence Review Queue: approve, reject, mark weak, and show audit timeline.
6. Search Discovery: generate Mock Static, RSS Mock, and GDELT Mock candidates; attach accepted metadata to a case.
7. Evidence Scale / Coverage: show counts, duplicates, trust distribution, latest jobs, and coverage limitation note.
8. Analysis Result: show `analysis_input_source` and evidence-source caveats.
9. Summary Report: show representative evidence and Markdown export.
10. Risk Monitor / Forecast: show offline scenario projection.
11. Simulation Lab: initialize from the case and compare strategies.
12. Benchmarks: show offline benchmark results.
13. LLM Safety: confirm mock provider boundary.
14. Platform Integration Overview: show YouTube real-capable, Douyin/Bilibili pending, RSS/GDELT mock-only.

## Screenshot List

Use [demo_screenshot_checklist.md](demo_screenshot_checklist.md) and [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md) for the exact screenshot sequence.

## Recording Script

Use [demo_recording_script.md](demo_recording_script.md) and [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md) for the 3-minute and 8-minute narration scripts.

## Caveats

- YouTube real data is optional and requires local configuration; it is not run in automated validation.
- Imported, manual, and search-discovery evidence may be unverified and can require human review.
- Search Discovery, RSS Mock, and GDELT Mock return metadata fixtures only.
- Vendor POC utilities map and score local sample files only; they are not a live vendor integration.
- Evidence Scale / Coverage describes imported or available evidence, not full-platform or full-web coverage.
- Predictions, risk scores, and simulations are decision-support outputs, not guarantees.
- No real LLM, Douyin, Bilibili, RSS, GDELT, vendor API, or general search provider is active in this demo.
