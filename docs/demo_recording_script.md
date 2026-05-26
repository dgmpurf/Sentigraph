# Sentigraph v6.26 Demo Recording Script

Last updated: 2026-05-26

Core safety note for both scripts: YouTube data can be real when locally configured, analysis is offline deterministic, Search Discovery/RSS/GDELT are mock/static, and the LLM provider is mock.

## Exact Page Order

1. Dashboard
2. Keyword Search
3. Cases
4. Evidence Import / Manual Evidence
5. Evidence Review Queue / Audit Timeline
6. Search Discovery
7. Evidence Scale / Coverage
8. Analysis Result
9. Summary Report
10. Risk Monitor / Forecast
11. Simulation Lab
12. Benchmarks
13. LLM Safety
14. Platform Integration Overview

## 3-Minute Short Demo

### 0:00 - Dashboard

Say: "Sentigraph is a public-opinion analysis workspace. This demo is mock-default, YouTube-real-capable, and evidence-ingestion-ready. It separates data source, offline analysis, and LLM mode."

Proves: Current case status, demo boundary, and navigation readiness.

### 0:20 - Keyword Search

Say: "When YouTube is selected alone, Sentigraph exposes the real-data case flow: create a case, crawl through the official YouTube API when locally configured, attach raw data, then run offline analysis. Automated tests never call YouTube."

Proves: YouTube real-data flow is explicit and optional.

### 0:40 - Cases / Evidence

Say: "For broader public-opinion evidence, users can import CSV/Excel datasets or manually attach URL/title/comment evidence. The system does not fetch URLs, scrape websites, store cookies, or save raw secrets."

Proves: CSV/manual evidence intake and safety boundary.

### 1:05 - Review Queue / Audit Timeline

Say: "Not all evidence has equal reliability. Low-trust, missing-source, duplicate, screenshot-style, or unverified evidence goes through human review. Rejected evidence is excluded from analysis by default."

Proves: Trust, provenance, deduplication, review decisions, and auditability.

### 1:30 - Search Discovery

Say: "Search Discovery is currently a mock-only candidate review scaffold. Mock Static, RSS Mock, and GDELT Mock return local URL/title/snippet metadata. Accepting a candidate attaches metadata as unverified evidence; no URL content is fetched."

Proves: Future discovery UX without live search or scraping.

### 1:55 - Analysis Result / Summary Report

Say: "The analysis result shows the input source, representative evidence, and caveats when evidence is user-uploaded or unverified. The report and Markdown export preserve these boundaries."

Proves: Evidence-driven offline analysis and report clarity.

### 2:25 - Risk Monitor / Simulation Lab

Say: "Forecasting and Simulation Lab are offline scenario tools. They help compare possible response strategies, but they do not guarantee outcomes or execute actions."

Proves: Offline risk and strategy workflow.

### 2:50 - Platform Integration / LLM Safety

Say: "YouTube is the current optional real-data demo. Douyin, Bilibili, and other platforms are pending official API or OAuth gates. The LLM provider remains mock."

Proves: Accurate real/offline/mock/pending boundary.

## 8-Minute Full Demo

### 0:00 - Dashboard

Say: "This is Sentigraph v6.26. The product is a desktop web MVP for public-opinion evidence ingestion, review, and offline analysis. The important distinction is: data can be real, analysis is deterministic and offline, and LLM output remains mock."

Proves: Product framing and safety promise.

### 0:45 - Keyword Search

Say: "The YouTube real-data path is intentionally explicit. If the local environment has the official API key and real adapter mode, this page creates a YouTube case, crawls public video/comment data, attaches raw data, and runs offline analysis. If the key is not configured, the mock fallback remains available."

Proves: Optional YouTube real-data flow and fallback.

### 1:30 - Cases: CSV / Excel Import

Say: "When official platform access is unavailable, users can import lawful datasets. The import flow previews normalized rows, maps columns into EvidenceItems, deduplicates repeated rows, redacts secret-like fields, and records an ingestion job."

Proves: User-uploaded evidence pipeline.

### 2:20 - Cases: Manual Evidence

Say: "Manual URL evidence is for cases where a user has a public source and wants to attach a single article, video, post, comment, or metric. Sentigraph does not fetch the URL. The user provides the text, attests they have rights to submit it, and the system stores normalized evidence only."

Proves: Manual evidence without scraping.

### 3:00 - Review Queue and Audit Timeline

Say: "Evidence carries provenance, trust labels, verification status, risk flags, duplicate groups, and review status. The review queue is human review only; it does not claim AI verified authenticity. Each decision is recorded in an audit timeline."

Proves: Governance for unverified or malicious evidence.

### 4:00 - Search Discovery

Say: "The Search Discovery page is a future-provider scaffold. Mock Static, RSS Mock, and GDELT Mock show how URL/title/snippet candidates would be reviewed. They are local fixtures, not live providers. Accepted candidates become unverified evidence for review; rejected candidates are ignored."

Proves: Safe discovery planning and candidate attachment.

### 4:50 - Evidence Scale / Coverage

Say: "Evidence Scale shows total, unique, duplicate, source, acquisition, trust, review, and latest-job summaries. The coverage note is deliberate: this is coverage of imported or available evidence, not full platform or full web coverage."

Proves: Scalable evidence summary without overclaiming capture.

### 5:35 - Analysis Result

Say: "The analysis result displays `analysis_input_source`. Raw YouTube data wins when present; otherwise evidence items are used; otherwise the mock fallback is used. Rejected evidence is excluded by default, and weak or unverified evidence is flagged."

Proves: Correct priority and caveats.

### 6:15 - Summary Report

Say: "The report turns the offline analysis into a readable Chinese report and Markdown export. It preserves representative evidence and warns when imported/manual evidence requires review."

Proves: Report output and export readiness.

### 6:50 - Risk Monitor and Simulation Lab

Say: "Risk Monitor, Forecast, and Simulation Lab are deterministic decision-support tools. They can compare strategies and export a strategy report, but they do not moderate content or execute real-world actions."

Proves: Forecast/simulation boundary.

### 7:35 - Benchmarks, LLM Safety, Platform Overview

Say: "The demo closes with offline benchmarks, mock LLM status, and platform readiness. YouTube is optional real-data ready; Douyin/Bilibili and other real integrations are pending approval or OAuth gates; RSS/GDELT are mock-only planning providers."

Proves: Validation, model safety, and platform roadmap.
