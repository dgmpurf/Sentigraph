# Sentigraph v6.28 Demo Recording Script

Last updated: 2026-05-28

Use this script with [demo_asset_package_v6_27.md](demo_asset_package_v6_27.md) and [operation_guide_v6_28.md](operation_guide_v6_28.md). The recording package is for manual local capture of the v6.28 demo-ready MVP.

Core safety note: YouTube data can be real only when locally configured; analysis, risk, report, forecast, and Simulation Lab are offline deterministic; Search Discovery/RSS/GDELT are mock/static metadata providers; Vendor POC utilities are offline sample mapping and scoring only; the LLM provider is mock.

## Exact Page Order

1. Source Catalog / Platform Integration Overview
2. Keyword Search / optional YouTube real-data flow
3. Cases
4. CSV/Excel Evidence Import
5. Vendor Sample POC utility
6. Manual URL Evidence
7. Search Discovery
8. Evidence Trust / Dedup
9. Evidence Review Queue
10. Evidence Review Audit Timeline
11. Evidence Scale / Coverage
12. Analysis Result
13. Summary Report
14. Propagation Graph
15. Risk Monitor / Forecast
16. Simulation Lab initialized from case
17. A/B Strategy Comparison
18. Strategy Report Export
19. Benchmarks
20. LLM Safety

## 3-Minute Script

### Intro

"Sentigraph is a local public-opinion intelligence MVP. The important boundary is that data can come from optional real YouTube public comments or user-provided evidence, while analysis, reports, forecasts, and Simulation Lab remain offline deterministic. The LLM provider is mock."

### Data Source Boundaries

"The Platform Overview shows what is real-capable, mock/static, or pending. YouTube is optional real-data when a local key is configured. Douyin, Bilibili, Xiaohongshu, Reddit, and Weibo still need official API or OAuth gates."

### Evidence Import

"Cases can ingest CSV/Excel datasets and manual URL evidence. The app does not fetch URLs, scrape pages, use cookies, bypass anti-bot systems, or store raw secret material."

### Vendor POC

"The v6.28 addition is a vendor POC utility path. Vendor samples are not official API data. They can be mapped offline from local CSV or JSON into EvidenceItem-compatible rows, scored with a 100-point rubric, and reviewed before any adapter work. The default trust label is `medium_low`; `vendor_attested` is used only when source rights and attestation are documented. A live vendor adapter remains blocked until POC, contract, security, quota, deletion-sync, retention, mocked-fixture, and credential-handling gates pass."

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

### 2:05 - Vendor Sample POC

"Vendor POC is a supporting path, not a live integration. The intake checklist asks who the vendor is, what platforms and fields they support, what rights and deletion-sync policy they document, and whether personal data is handled safely. The offline mapper converts only local sample CSV or JSON files into EvidenceItem-compatible JSONL or CSV. It does not call vendor APIs or fetch URLs. The scorecard classifies the vendor as `approved_poc`, `limited_poc`, `internal_research_only`, or `reject`."

### 2:50 - Manual URL Evidence

"Manual URL evidence is for single public items: article, video, post, comment, reply, or metric. The system does not open the URL; the user supplies the text and attestation."

### 3:20 - Search Discovery Mock Candidates

"Search Discovery is mock-only. Mock Static, RSS Mock, and GDELT Mock generate local URL/title/snippet candidates. Accepting a candidate stores unverified metadata as evidence; rejected candidates are ignored."

### 4:00 - Review Queue

"Evidence with low trust, missing sources, duplicates, screenshot-style capture, or missing attestation goes to human review. AI is not used for authenticity verification."

### 4:35 - Audit Timeline

"Every review decision is append-only. The audit timeline records previous status, new status, reviewer label, notes, and the effect on analysis."

### 5:00 - Evidence Scale / Coverage

"Evidence Scale shows total, unique, duplicate, source, acquisition, trust, review, and latest job summaries. This is imported or available evidence coverage, not full-platform or full-web capture."

### 5:35 - Analysis Result

"The analysis priority is explicit: case raw data wins, then EvidenceItems, then mock fallback. Rejected evidence is excluded, and weak or unverified evidence is called out."

### 6:05 - Summary Report

"The report turns offline analysis into a readable Chinese report and Markdown export while preserving representative evidence and review caveats."

### 6:35 - Risk Monitor / Forecast

"Forecasting is deterministic decision support. It gives a structured risk projection, not a guaranteed prediction."

### 7:00 - Simulation Lab

"Simulation Lab initializes from aggregate case data, compares strategies, and exports a Markdown strategy report. It remains human-review-oriented and does not execute platform actions."

### 7:40 - Benchmarks / LLM Safety

"The final proof is validation and safety: offline benchmarks pass, the LLM provider is mock, and future real provider work remains behind explicit permission and policy review."

## Required Closing Line

"Sentigraph is demo-ready as a local MVP. It clearly separates optional real YouTube data, offline deterministic analysis, mock/static discovery, offline vendor POC utilities, mock LLM behavior, and pending platform integrations."
