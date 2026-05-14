# Sentigraph Product Requirements

Last updated: 2026-05-14

## 1. Product Goal

Sentigraph is a desktop-first public opinion analysis and risk monitoring system. The current MVP should feel like a usable local demo product, even though it is still mock-first and offline.

The next-stage product goal is to make the flow clear for a user who wants to quickly understand:

- what public opinion topic is being monitored
- which platforms are included in the mock analysis
- what the current risk level is
- which topics and comments are driving risk
- whether repeated scripts or bot-like behavior may be amplifying the issue
- what response actions and public-facing language are recommended

## 2. Target MVP Experience

The MVP experience should remain a PC/browser dashboard optimized around a 1440px desktop layout. Mobile optimization is future work.

Core user flow:

1. User creates or starts a public opinion analysis case.
2. User enters a keyword.
3. User selects platforms.
4. User runs mock analysis.
5. System shows the dashboard.
6. System shows topic and risk explanations.
7. System generates a Chinese public opinion report.
8. System gives recommended actions and a suggested public response.
9. User copies the suggested response for later editing or approval.

## 3. Product Pages

### Dashboard

Purpose: give the user an immediate operational overview.

Should show:

- overall risk score and risk level
- latest public opinion summary
- sentiment trend
- topic cluster ranking
- risk radar
- bot or repeated-script impact
- platform distribution or heatmap
- navigation entry points to report, risk monitor, and propagation graph

### KeywordSearch

Purpose: start a mock analysis case.

Should support:

- keyword input
- grouped platform selection
- mock-selectable platform choices
- visible but disabled future platform groups
- analysis progress/loading state
- clear error state if backend is unavailable

### AnalysisResult

Purpose: explain what the mock pipeline found.

Should show:

- sentiment explanation
- topic clusters
- bot/repeated-script signals
- representative comments
- report-related insights
- suggested response preview

### SummaryReport

Purpose: present an export-friendly Chinese public opinion report.

Should show:

- 舆情总览
- 风险分数
- 风险等级
- 风险模型版本
- 核心发现
- 主要风险因素
- 高风险话题
- 代表性评论
- 疑似水军/重复话术信号
- 建议行动
- 建议公开回应文案

PDF export is not part of the current MVP, but the layout should be print/export friendly.

### RiskMonitor

Purpose: help the user understand how risk is changing.

Should show:

- risk level explanation
- risk trend
- risk factors
- warning cards
- trend shift, propagation speed, controversy, and bot impact indicators when available
- current risk model version

### PropagationGraph

Purpose: show how discussion spreads through comments, topics, platforms, or account nodes.

Should show:

- graph nodes and edges from backend mock data
- small-graph guidance
- central node details
- platform/type breakdown
- graph metrics such as depth, breadth, central node, and propagation speed when available

### PlatformRoadmap or Settings

This page is optional until the product needs a dedicated configuration surface. For now, platform roadmap information can remain in KeywordSearch and documentation.

## 4. MVP Acceptance Criteria

- The backend and frontend run locally without external API keys.
- The user can run a mock keyword/platform analysis.
- Dashboard, AnalysisResult, RiskMonitor, PropagationGraph, and SummaryReport load without runtime errors.
- SummaryReport displays Chinese report text by default.
- Representative comments remain in their original language.
- Suggested public response can be copied.
- Empty arrays do not crash charts or report sections.
- The UI remains desktop-first and does not require mobile-first layout work.

## 5. Current Non-Goals

- No real crawlers.
- No real platform API calls.
- No real OpenAI or external LLM calls.
- No login bypass, captcha bypass, paywall bypass, anti-bot evasion, or private data collection.
- No authentication.
- No production deployment hardening.
- No full V2 dynamic risk model implementation yet.

