# Sentigraph UX Flow

Last updated: 2026-05-14

## 1. Layout Principles

Sentigraph MVP is a desktop-first browser dashboard. The default design target is a 1440px wide PC screen.

Core layout:

- left sidebar navigation
- top status/header bar
- main dashboard/report canvas
- chart and report sections designed for scanning
- dark sci-fi dashboard style with restrained operational density

Mobile-first optimization is not part of MVP 0-4. Future responsive support can be added later after the desktop demo is stable.

## 2. Navigation Model

Primary pages:

- Dashboard
- KeywordSearch
- AnalysisResult
- SummaryReport
- RiskMonitor
- PropagationGraph

The sidebar should let the user move between overview, input, result explanation, report, monitoring, and propagation views without losing the mental model of a single analysis case.

The top status/header bar should show high-level project state, backend connectivity if available, and current risk context.

## 3. Keyword and Platform Selection Flow

1. User opens KeywordSearch.
2. User enters a keyword.
3. User reviews platform groups:
   - MVP mock-selectable platforms
   - Official API planned platforms
   - Future real adapter candidates
   - Crawler-later platforms
   - Disabled or optional future platforms
4. User selects mock-capable platforms.
5. User starts mock analysis.
6. UI shows loading/progress state.
7. Successful run routes or guides the user to Dashboard and AnalysisResult.
8. Errors should explain whether the backend is unavailable or data is empty.

Crawler-later platforms should remain visible but disabled with future integration language. YouTube should never appear as an active MVP platform.

## 4. Dashboard Flow

Dashboard is the first operational reading surface after mock analysis.

The user should be able to answer within a few seconds:

- What is the current risk score?
- What is the risk level?
- Is sentiment worsening?
- Which topics are driving risk?
- Is there suspicious amplification?
- Which platforms carry the most signal?
- Where should I click for the full report or graph?

Charts should handle empty arrays safely and show designed empty states instead of broken panels.

## 5. Report Reading Flow

SummaryReport should behave like a public opinion report, not a debug page.

Recommended reading order:

1. 舆情总览
2. 风险分数 / 风险等级 / 风险模型版本
3. 核心发现
4. 主要风险因素
5. 高风险话题
6. 代表性评论
7. 疑似水军/重复话术信号
8. 建议行动
9. 建议公开回应文案

The suggested public response should be easy to copy. Representative comments should remain in their original language.

## 6. Risk Monitoring Flow

RiskMonitor should help the user interpret risk movement and urgency.

The page should show:

- risk trend
- risk factor cards
- warning status
- risk level explanation
- trend shift
- propagation speed
- controversy signal
- bot or repeated-script signal
- active risk model version

For MVP, signals are deterministic and mock-first. The page should avoid implying live monitoring or real platform ingestion until those features exist.

## 7. Propagation Graph Flow

PropagationGraph should help users understand spread shape even when mock data is small.

The page should show:

- graph nodes and edges
- central node or key node
- node type/platform/sentiment/influence if available
- graph metrics such as depth, breadth, central node, and propagation speed
- explanatory empty state for small or missing graphs

The graph should remain readable at desktop dashboard sizes and should not require mobile layout work in the current MVP.

## 8. Local Demo Flow

Recommended demo sequence:

1. Start backend.
2. Start frontend.
3. Open Dashboard.
4. Open KeywordSearch.
5. Enter a keyword.
6. Select mock-capable platforms.
7. Run mock analysis.
8. Review Dashboard.
9. Open AnalysisResult.
10. Open SummaryReport.
11. Copy the suggested public response.
12. Open RiskMonitor.
13. Open PropagationGraph.

Use `docs/demo_checklist.md` for the detailed local QA checklist.

