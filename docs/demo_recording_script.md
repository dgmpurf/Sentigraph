# Sentigraph v6.27 Demo Recording Script

Last updated: 2026-05-26

Use this script with [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md). The recording package is for manual local capture of the v6.26 demo-ready MVP.

Core safety note: YouTube data can be real only when locally configured; analysis, risk, report, forecast, and Simulation Lab are offline deterministic; Search Discovery/RSS/GDELT are mock/static metadata providers; the LLM provider is mock.

## Exact Page Order

1. Source Catalog / Platform Integration Overview
2. Keyword Search / optional YouTube real-data flow
3. Cases
4. CSV/Excel Evidence Import
5. Manual URL Evidence
6. Search Discovery
7. Evidence Trust / Dedup
8. Evidence Review Queue
9. Evidence Review Audit Timeline
10. Evidence Scale / Coverage
11. Analysis Result
12. Summary Report
13. Propagation Graph
14. Risk Monitor / Forecast
15. Simulation Lab initialized from case
16. A/B Strategy Comparison
17. Strategy Report Export
18. Benchmarks
19. LLM Safety

## 3-Minute Script

### Intro

"Sentigraph is a local public-opinion intelligence MVP. The important boundary is that data can come from optional real YouTube public comments or user-provided evidence, while analysis, reports, forecasts, and Simulation Lab remain offline deterministic. The LLM provider is mock."

### Data Source Boundaries

"The Platform Overview shows what is real-capable, mock/static, or pending. YouTube is optional real-data when a local key is configured. Douyin, Bilibili, Xiaohongshu, Reddit, and Weibo still need official API or OAuth gates."

### Evidence Import

"Cases can ingest CSV/Excel datasets and manual URL evidence. The app does not fetch URLs, scrape pages, use cookies, bypass anti-bot systems, or store raw secret material."

### Trust And Review

"Evidence is normalized, not automatically trusted. Sentigraph tracks provenance, verification status, trust labels, duplicate groups, review status, and audit history. Screenshots and transcriptions need human review."

### Analysis And Report

"Analysis Result shows `analysis_input_source`; Summary Report and Markdown export preserve evidence caveats. Rejected evidence is excluded from analysis by default, and weak or unverified evidence remains flagged."

### Simulation Lab

"Risk Monitor and Simulation Lab are deterministic decision-support tools. Simulation compares possible strategies and exports a report, but it does not execute real-world actions or guarantee outcomes."

### Quality And Safety

"Benchmarks show offline quality checks. LLM Safety confirms mock-provider status. Search Discovery, RSS Mock, and GDELT Mock save metadata only and do not call live providers."

## 8-Minute Script

### 0:00 - Source Catalog / Platform Overview

"Start with source readiness. YouTube is optional real-capable through the official API when locally configured. Other real platforms are pending official access or OAuth verification. Search Discovery, RSS Mock, and GDELT Mock are static planning providers."

### 0:45 - Optional YouTube Real Path

"Keyword Search exposes the YouTube-only flow: create a case, crawl public YouTube data when locally configured, attach raw data, and run offline deterministic analysis. Automated tests never call YouTube and the recording must not expose the key."

### 1:25 - CSV/Excel Import

"CSV/Excel import is the practical route for lawful user-provided datasets. It previews rows, maps columns, normalizes EvidenceItems, redacts secret-like fields, deduplicates repeated rows, and records an import job."

### 2:05 - Manual URL Evidence

"Manual URL evidence is for single public items: article, video, post, comment, reply, or metric. The system does not open the URL; the user supplies the text and attestation."

### 2:40 - Search Discovery Mock Candidates

"Search Discovery is mock-only. Mock Static, RSS Mock, and GDELT Mock generate local URL/title/snippet candidates. Accepting a candidate stores unverified metadata as evidence; rejected candidates are ignored."

### 3:30 - Review Queue

"Evidence with low trust, missing sources, duplicates, screenshot-style capture, or missing attestation goes to human review. AI is not used for authenticity verification."

### 4:10 - Audit Timeline

"Every review decision is append-only. The audit timeline records previous status, new status, reviewer label, notes, and the effect on analysis."

### 4:40 - Evidence Scale / Coverage

"Evidence Scale shows total, unique, duplicate, source, acquisition, trust, review, and latest job summaries. This is imported or available evidence coverage, not full-platform or full-web capture."

### 5:20 - Analysis Result

"The analysis priority is explicit: case raw data wins, then EvidenceItems, then mock fallback. Rejected evidence is excluded, and weak or unverified evidence is called out."

### 5:55 - Summary Report

"The report turns offline analysis into a readable Chinese report and Markdown export while preserving representative evidence and review caveats."

### 6:25 - Risk Monitor / Forecast

"Forecasting is deterministic decision support. It gives a structured risk projection, not a guaranteed prediction."

### 6:55 - Simulation Lab

"Simulation Lab initializes from aggregate case data, compares strategies, and exports a Markdown strategy report. It remains human-review-oriented and does not execute platform actions."

### 7:35 - Benchmarks / LLM Safety

"The final proof is validation and safety: offline benchmarks pass, the LLM provider is mock, and future real provider work remains behind explicit permission and policy review."

## Required Closing Line

"Sentigraph is demo-ready as a local MVP. It clearly separates optional real YouTube data, offline deterministic analysis, mock/static discovery, mock LLM behavior, and pending platform integrations."
