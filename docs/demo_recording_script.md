# Sentigraph v6.3 Demo Recording Script

Last updated: 2026-05-19

Use this script for external screenshots or screen recording. The core framing should be repeated at the start and near the end:

> YouTube data is real, analysis is offline deterministic, LLM is mock.

Do not show `.env`, API keys, terminal history containing secrets, or raw credential settings. Do not imply that Sentigraph predicts the future with certainty, executes platform actions, performs content moderation automatically, or targets individuals.

## Exact Page Order

1. Dashboard
2. Keyword Search
3. Cases
4. Analysis Result
5. Summary Report
6. Propagation Graph
7. Risk Monitor / Forecast
8. Simulation Lab initialized from case
9. Simulation Lab A/B strategy comparison
10. Strategy report export
11. Benchmark Dashboard
12. LLM Safety
13. Platform Integration Overview

## 3-Minute Short Demo

### 0:00-0:20 Dashboard

Say: "Sentigraph is a public-opinion intelligence dashboard. In this demo, the YouTube public video/comment data is real when locally configured, while the analysis, risk model, forecast, and Simulation Lab are deterministic offline systems. The LLM provider is mock."

Proves: The command-center view is usable for a completed case and the demo does not present itself as a black-box live agent.

### 0:20-0:45 Keyword Search

Say: "The normal demo path stays mock/offline. For the YouTube-only path, the page makes the real-data steps explicit: create a YouTube case, crawl and attach raw data, then run offline analysis."

Proves: The app distinguishes data source from analysis mode and keeps multi-platform mock flow available.

### 0:45-1:15 Cases and Analysis Result

Say: "The completed YouTube case shows `analysis_input_source=case_raw_data`. That means the case analysis used attached public YouTube comments instead of the local mock comment fixture."

Proves: YouTube crawl output can enter the case pipeline while analysis remains offline and deterministic.

### 1:15-1:45 Summary Report

Say: "The Chinese report turns the case into structured findings, topic-risk explanation, representative comments, and Markdown export. Representative comments are YouTube-derived when raw case data is attached."

Proves: The report is analyst-ready and preserves provenance without using a real LLM.

### 1:45-2:10 Risk Monitor / Forecast

Say: "The monitoring and forecast panels use local snapshots and deterministic trend logic. They are scenario indicators, not guaranteed predictions."

Proves: Risk monitoring and forecast surfaces are demo-ready without live polling or external APIs.

### 2:10-2:40 Simulation Lab

Say: "Simulation Lab initializes from the aggregate case result, then compares transparent response strategies. Outputs are aggregate-level and human-review-oriented."

Proves: Case-to-simulation initialization, bubble visualization, and A/B strategy comparison work from the same case.

### 2:40-3:00 Strategy Report, Benchmarks, LLM Safety, Platform Overview

Say: "The strategy report exports a Markdown rehearsal summary with human review questions. Benchmarks show local regression checks, LLM Safety shows mock provider status, and Platform Overview shows YouTube as the only real-capable configured path while other platforms remain mock or scaffold."

Proves: The package is ready for review without overclaiming real integrations.

## 8-Minute Full Demo

### 0:00-0:40 Dashboard

Say: "This is the Sentigraph desktop dashboard. For the v6.3 demo, the key sentence is: YouTube data is real, analysis is offline deterministic, LLM is mock."

Point out:
- Current case status.
- Data/analysis/LLM badges.
- Risk score and topic cards.

Proves:
- The app can present a completed case as a single operations surface.
- Real data provenance is visible without implying real LLM usage.

### 0:40-1:25 Keyword Search

Say: "Keyword Search keeps the default `Create Case & Run Mock Analysis` path. When only YouTube is selected, it exposes the explicit real-data sequence: create case, crawl and attach raw data, run analysis."

Point out:
- YouTube-only flow controls.
- Warning for YouTube mixed with other platforms.
- Crawl metadata fields such as adapter mode, fallback status, cache hit, and quota guardrail status.

Proves:
- Real YouTube mode is deliberate, not hidden behind a generic mock button.
- The UI does not expose API keys.

### 1:25-2:05 Cases

Say: "Cases preserves the local case record and shows whether raw data was attached. This is still local demo storage, not production persistence."

Point out:
- Completed YouTube case.
- `raw_data_status=attached` where visible.
- Data source badges.

Proves:
- The crawl result is stored on the case and can be reopened.

### 2:05-2:50 Analysis Result

Say: "Here we verify `analysis_input_source=case_raw_data`. The risk model is V1.5 topic risk and remains deterministic."

Point out:
- `analysis_input_source`.
- Topic risk cards.
- Overall risk, real-crisis risk, and manipulation-risk signals if visible.

Proves:
- The analysis stage can consume attached YouTube public comments.
- The app does not claim real LLM reasoning.

### 2:50-3:35 Summary Report

Say: "The report is generated from offline deterministic analysis. It can include YouTube-derived representative comments and can be exported as Markdown."

Point out:
- Chinese report sections.
- Representative comments.
- Markdown copy/download controls.

Proves:
- The analyst handoff path is credible for screenshots.
- UTF-8 Chinese report output remains normal in the browser.

### 3:35-4:10 Propagation Graph

Say: "Propagation Graph shows the case network view. For the demo, it is a normalized visualization layer from case analysis, not a claim of complete platform graph coverage."

Point out:
- YouTube/platform node labels if present.
- Graph metrics.
- Node details.

Proves:
- The visualization stack remains connected after real-data case ingestion.

### 4:10-4:45 Risk Monitor / Forecast

Say: "Monitoring and forecast use local snapshots and deterministic MVP trend logic. They provide review signals, not guaranteed future outcomes."

Point out:
- Snapshot history.
- Forecast confidence.
- Deterministic-MVP notice.

Proves:
- Forecasting can be demonstrated safely without live polling.

### 4:45-5:35 Simulation Lab Initialized From Case

Say: "Simulation Lab converts the completed aggregate case analysis into an echo-chamber frame. It creates synthetic audience segments and does not output named-user targets."

Point out:
- Case initialization controls.
- Event frame.
- Audience distribution.
- Bubble visualization.

Proves:
- The case-to-simulation bridge works from aggregate analysis.
- Simulation remains human-review-oriented.

### 5:35-6:25 Simulation Lab A/B Strategy Comparison

Say: "A/B mode compares transparent response strategies from the same initial scenario. It can show lawful content-visibility tradeoffs when the ethics policy allows them, but it does not execute moderation actions."

Point out:
- A and B panels.
- Delta badges.
- Visibility tradeoff panel if used.
- Human review recommendation.

Proves:
- Simulation Lab supports aggregate strategy rehearsal without forbidden manipulation tactics.

### 6:25-6:55 Strategy Report Export

Say: "The strategy report is a Markdown export for review. It includes limitations, ethics review, and human-review questions."

Point out:
- `# Simulation Lab Strategy Report`.
- Human review questions.
- Copy Markdown action.

Proves:
- The demo can produce a clean artifact without a real LLM.

### 6:55-7:25 Benchmark Dashboard

Say: "Offline benchmarks run locally and guard regression across sentiment, topics, reports, forecasting, adapters, and Simulation Lab."

Point out:
- Pass/fail totals.
- Regression status.
- Suite list.

Proves:
- The package has repeatable local validation.

### 7:25-7:45 LLM Safety

Say: "LLM Safety shows the provider is mock and real LLM calls are disabled. This is intentional for the demo."

Point out:
- Mock provider.
- Real-call disabled state.
- Metadata-only usage boundaries.

Proves:
- The demo is not silently calling OpenAI or any other model provider.

### 7:45-8:00 Platform Integration Overview

Say: "YouTube is the first real-capable official API path when locally configured. Other platforms remain mock or scaffold until their permissions and official integrations are approved."

Point out:
- YouTube status.
- Other platform scaffold/mock statuses.
- No scraping note.

Proves:
- The product roadmap is honest about what is real today.

## Presenter Guardrails

- Say "real YouTube public video/comment data" only for a locally configured YouTube case with attached raw data.
- Say "offline deterministic analysis" for analysis, reports, risk scoring, monitoring, forecasting, and Simulation Lab.
- Say "mock LLM" unless real LLM integration is explicitly implemented in a future task.
- Do not claim all platforms are real.
- Do not claim forecasts or Simulation Lab outputs are guaranteed.
- Do not imply Simulation Lab executes real-world actions or content moderation.
- Do not imply individual targeting, account-level influenceability scoring, or automatic persuasion is supported.
- Do not show API keys, `.env`, private data, browser cookies, or terminal commands that reveal secrets.
