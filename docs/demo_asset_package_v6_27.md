# Sentigraph v6.27 Demo Screenshot / Recording Asset Package

Last updated: 2026-05-26

## Purpose

This package is a local capture plan for the v6.26 demo-ready Sentigraph MVP. It tells a presenter exactly what screenshots to capture, what to say in short and full recordings, what safety boundaries to mention, and what must stay out of the recording frame.

The package is for manual screenshot and recording production. It does not add product features and does not require live API calls.

## Audience

- Collaborators who need to understand the current product state.
- Clients who need a grounded walkthrough without overclaiming real integrations.
- Platform reviewers who need clear compliance boundaries.
- Investors and partners who need to see the product direction and current readiness.
- Internal archive so the v6.26/v6.27 demo state can be reproduced later.

## What The Demo Proves

- Sentigraph can run a local public-opinion intelligence workflow from case setup to report, forecast, and Simulation Lab rehearsal.
- Optional YouTube public video/comment data can be the real data source when a local ignored key is configured.
- CSV/Excel uploads and Manual URL evidence can enter the same normalized EvidenceItem layer.
- Search Discovery, RSS Mock, and GDELT Mock provide safe candidate-review UX using static metadata only.
- Evidence is not blindly trusted: trust/provenance, deduplication, review queue, audit timeline, and coverage summaries are visible.
- Offline deterministic analysis, Summary Report, Markdown export, Risk Monitor, Forecast, and Simulation Lab work from available case evidence.
- Benchmarks and LLM Safety make quality and mock-LLM boundaries visible.

## What The Demo Does Not Claim

- It does not claim all platforms are real.
- It does not claim full-web or full-platform capture.
- It does not claim RSS/GDELT or Search Discovery are live providers.
- It does not claim the LLM provider is real.
- It does not claim screenshots/transcriptions are automatically verified.
- It does not claim predictions are guaranteed.
- It does not claim Simulation Lab executes real-world actions or moderation.
- It does not integrate MediaCrawler, cookies, captcha bypass, proxy evasion, or anti-bot bypass.

## Screenshot Asset List

| # | File name | Screen | What it proves |
| --- | --- | --- | --- |
| 1 | `01_dashboard_overview.png` | Dashboard overview | App shell, status badges, risk/alert overview, and navigation. |
| 2 | `02_platform_source_catalog.png` | Source Catalog / Platform Integration Overview | YouTube real-capable, other platforms pending/scaffold, source strategy visible. |
| 3 | `03_youtube_real_flow_optional.png` | Keyword Search / YouTube real flow | Optional YouTube-only real-data flow and data/analysis/LLM separation. |
| 4 | `04_cases_page.png` | Cases page | Case list/detail surface and evidence entry points. |
| 5 | `05_csv_excel_evidence_import.png` | CSV/Excel Evidence Import | Upload, template, preview/commit flow, and user-upload data boundary. |
| 6 | `06_manual_url_evidence.png` | Manual URL Evidence | Manual public evidence entry with no automatic URL fetching. |
| 7 | `07_search_discovery_mock_review.png` | Search Discovery mock candidate review | Mock candidate generation, accept/reject, and metadata-only warning. |
| 8 | `08_rss_gdelt_mock_provider_selector.png` | RSS/GDELT mock provider selector | Provider selector and mock/static provider status. |
| 9 | `09_evidence_trust_dedup_fields.png` | Evidence Trust / Dedup fields | Trust label, provenance, verification status, duplicate/risk flags. |
| 10 | `10_evidence_review_queue.png` | Evidence Review Queue | Human review controls for weak/unverified/duplicate evidence. |
| 11 | `11_review_audit_timeline.png` | Review Audit Timeline | Append-only review decision history. |
| 12 | `12_evidence_scale_coverage.png` | Evidence Scale / Coverage | Counts, unique/duplicate values, jobs, distributions, coverage caveat. |
| 13 | `13_analysis_result.png` | Analysis Result | `analysis_input_source` and evidence-source caveats. |
| 14 | `14_summary_report.png` | Summary Report | Representative evidence, report wording, Markdown export. |
| 15 | `15_propagation_graph.png` | Propagation Graph | Graph output from current case data without duplicate-node regression. |
| 16 | `16_risk_monitor_forecast.png` | Risk Monitor / Forecast | Offline deterministic forecast and risk trend messaging. |
| 17 | `17_simulation_lab_initialized.png` | Simulation Lab initialized from case | Aggregate case-to-simulation initialization. |
| 18 | `18_ab_strategy_comparison.png` | A/B Strategy Comparison | Offline strategy comparison and human-review framing. |
| 19 | `19_strategy_report_export.png` | Strategy Report Export | Markdown strategy report export and no automatic action execution. |
| 20 | `20_benchmarks.png` | Benchmarks | Offline benchmark status. |
| 21 | `21_llm_safety.png` | LLM Safety | Mock LLM provider and real-call disabled boundary. |

## 3-Minute Recording Script

### Intro

"This is Sentigraph, a local public-opinion intelligence MVP. The key boundary is simple: data can come from optional real YouTube public comments or user-provided evidence, but analysis, reports, forecasts, and Simulation Lab are offline deterministic, and the LLM provider is mock."

### Data Source Boundaries

"The Platform Overview shows what is real-capable, what is pending, and what is mock/static. YouTube is the optional real-data path when a local key is configured. Douyin, Bilibili, Xiaohongshu, Reddit, and Weibo are still pending official API or OAuth gates."

### Evidence Import

"When platform APIs are unavailable, users can import CSV/Excel evidence or manually attach public URL/title/comment evidence. Sentigraph does not fetch URLs, scrape websites, use cookies, or save raw secret material."

### Trust And Review

"Evidence is normalized but not automatically trusted. The system tracks provenance, trust label, verification status, duplicates, risk flags, review status, and audit history. Screenshots and transcriptions need human review."

### Analysis And Report

"The Analysis Result shows `analysis_input_source`; Summary Report and Markdown export preserve evidence caveats. Rejected evidence is excluded from analysis by default, and weak or unverified evidence remains flagged."

### Simulation Lab

"Risk Monitor and Simulation Lab are deterministic decision-support tools. Simulation can compare strategies and export a report, but it does not execute real-world actions or guarantee outcomes."

### Quality And Safety Proof

"Benchmarks show offline quality checks. LLM Safety confirms the provider is mock. Search Discovery, RSS Mock, and GDELT Mock are local fixtures that save candidate metadata only."

### Closing

"The product is demo-ready as a local MVP. The next step is actual screenshot and recording production, while real platform integrations wait for official permissions."

## 8-Minute Recording Script

### 0:00 - Source Catalog / Platform Overview

Say: "Start with the source boundary. YouTube is optional real-capable through the official API when locally configured. Douyin/Bilibili/Xiaohongshu/Reddit/Weibo remain pending. RSS/GDELT and Search Discovery are mock/static planning surfaces."

Show: `02_platform_source_catalog.png`.

### 0:45 - Optional YouTube Real Path

Say: "If a local ignored `.env` has the YouTube mode and key, Keyword Search exposes a YouTube-only flow: create a case, crawl public data, attach raw data, then run offline analysis. Automated tests do not call YouTube."

Show: `03_youtube_real_flow_optional.png`.

### 1:25 - CSV/Excel Import

Say: "CSV/Excel import is the practical path for lawful datasets when APIs are unavailable. The system previews rows, maps columns, normalizes EvidenceItems, redacts secret-like fields, deduplicates repeated rows, and records an import job."

Show: `05_csv_excel_evidence_import.png`.

### 2:05 - Manual URL Evidence

Say: "Manual URL evidence lets a user attach a public source manually. Sentigraph does not open the URL; it stores only normalized evidence and safe metadata."

Show: `06_manual_url_evidence.png`.

### 2:40 - Search Discovery Mock Candidates

Say: "Search Discovery is mock-only. Mock Static, RSS Mock, and GDELT Mock generate static URL/title/snippet candidates. Accepting a candidate attaches metadata as unverified evidence; rejected candidates are ignored."

Show: `07_search_discovery_mock_review.png` and `08_rss_gdelt_mock_provider_selector.png`.

### 3:30 - Review Queue

Say: "Evidence with low trust, missing sources, duplicates, screenshots, or missing attestation goes to human review. Approve, reject, mark weak, request source, merge duplicate, and reset are human decisions. AI does not verify authenticity."

Show: `10_evidence_review_queue.png`.

### 4:10 - Audit Timeline

Say: "Each review decision is append-only. The audit timeline records previous status, new status, reviewer label, notes, and analysis effect."

Show: `11_review_audit_timeline.png`.

### 4:40 - Evidence Scale / Coverage

Say: "Scale and coverage summaries show total, unique, duplicate, trust, review, acquisition, source, and latest job data. This is imported or available evidence coverage, not full-platform or full-web capture."

Show: `12_evidence_scale_coverage.png`.

### 5:20 - Analysis Result

Say: "The analysis priority is explicit: case raw data wins, then evidence items, then mock fallback. The UI shows `analysis_input_source` and caveats for weak or unverified evidence."

Show: `13_analysis_result.png`.

### 5:55 - Summary Report

Say: "The Summary Report turns offline analysis into a readable report and Markdown export while preserving representative evidence and trust warnings."

Show: `14_summary_report.png`.

### 6:25 - Risk Monitor / Forecast

Say: "Forecasting is deterministic decision support. It gives a structured risk projection, not a guaranteed prediction."

Show: `16_risk_monitor_forecast.png`.

### 6:55 - Simulation Lab

Say: "Simulation Lab initializes from aggregate case data, compares strategies, and exports a strategy report. It remains human-review-oriented and does not execute platform actions."

Show: `17_simulation_lab_initialized.png`, `18_ab_strategy_comparison.png`, and `19_strategy_report_export.png`.

### 7:35 - Benchmarks And LLM Safety

Say: "The demo closes with offline benchmark evidence and LLM Safety. No real LLM calls are active; real provider integration remains future work."

Show: `20_benchmarks.png` and `21_llm_safety.png`.

## Talking Points

- Real: optional YouTube public video/comment data when locally configured.
- Offline deterministic: analysis, V1.5 risk model, report generation, forecast, Simulation Lab, and strategy report export.
- Mock/static: Search Discovery, RSS Mock, and GDELT Mock providers.
- Mock: LLM provider.
- Pending: Douyin, Bilibili, Xiaohongshu, Reddit, Weibo, and other real platform integrations.
- Not integrated: MediaCrawler.
- No scraping, cookies, captcha bypass, proxy evasion, or anti-bot bypass.
- Uploaded evidence is not automatically trusted.
- Screenshots and transcriptions require human review.
- Evidence Scale is imported/available coverage only, not full-web capture.

## Capture Commands

Run from repository root.

Validation before recording:

```powershell
python -m pytest
python scripts/run_offline_benchmarks.py
npm --prefix frontend run build
```

Start backend:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Start frontend:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1 --port 5173
```

Optional YouTube real-mode capture, only if local ignored `.env` is configured:

```powershell
# Do not print or show the key.
# Use the frontend YouTube-only flow or the documented manual path in docs/youtube_real_data_demo.md.
```

Never show API keys, `.env` values, terminal commands that echo secrets, or private user data in the recording.

## Privacy And Safety Checklist Before Recording

- Hide `.env`, shell history, terminal panes with credentials, and browser tabs with secrets.
- Do not show API keys, access tokens, refresh tokens, cookies, passwords, client secrets, or private messages.
- Do not show private user data or non-public source data.
- Use mock/static fixtures, uploaded safe samples, or intentionally selected public YouTube comments.
- If using YouTube real data, show only public comments and avoid sensitive personal information.
- Keep Search Discovery/RSS/GDELT labeled mock/static.
- Keep LLM labeled mock.
- Keep Douyin/Bilibili/other real APIs labeled pending.
- Do not imply full-platform/full-web capture.
- Do not imply Simulation Lab actions are executed in the real world.
- Do not imply AI or the app verifies screenshot authenticity.

## Final Handoff

After capture, store screenshots with the recommended filenames, keep the recording script with the footage, and preserve this file as the v6.27 asset-package manifest.
