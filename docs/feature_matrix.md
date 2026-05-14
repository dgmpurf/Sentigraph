# Sentigraph Feature Matrix

Last updated: 2026-05-14

This matrix separates what is already usable in the mock-first MVP from polish work, next implementation work, future real-data integration, and future advanced algorithm work.

| Feature | Status Category | Current Scope | Next Action |
| --- | --- | --- | --- |
| Project skeleton | Completed | FastAPI backend, React + Vite frontend, docs, mock data, tests, and local scripts exist. | Keep structure stable. |
| Desktop dashboard layout | Completed | Sidebar, top status/header bar, chart cards, and desktop-first page layout exist. | Manual browser QA at 1440px. |
| Platform registry | Completed | Backend registry exposes Reddit, Chinese official-API-planned platforms, crawler-later platforms, and YouTube as optional future. | Keep registry as the source of truth for platform selection. |
| `GET /api/v1/platforms` | Completed | Frontend can fetch platform roadmap and mock-selectable choices. | Add adapter metadata only when real integrations start. |
| Mock keyword/crawl/analysis pipeline | Completed | Offline deterministic mock flow exists. | Add saved case state before real crawlers. |
| Sentiment analysis | Completed | Rule-based deterministic mock sentiment. | Improve language-aware phrase lists and tests. |
| Topic clustering | Completed | Simple keyword/topic grouping with embedding-compatible interface. | V1.5 should calculate topic-level risk from these clusters. |
| Duplicate detection | Completed | Exact fingerprint and simple similarity grouping. | Use duplicate clusters more directly in V1.5 bot/topic risk. |
| Bot/repeated-script detection | Completed | Rule-based score from duplicate ratio, posting frequency, repeated scripts, and sentiment uniformity. | Add topic-level bot signal in V1.5. |
| V1 risk scoring | Completed | `v1_static_mvp` project-level score and risk level. | Keep stable as active model while V1.5 is added as shadow output. |
| Visualization API | Completed | Returns mock-pipeline visualization data, propagation graph, and risk model metadata. | Add optional topic risk fields after V1.5 implementation. |
| Report builder | Completed | Offline template-based report builder. | Add richer V1.5 topic-risk explanations after V1.5 exists. |
| Chinese normalized report API | Completed | Summary/recommendation APIs return `zh-CN` report fields by default. | Keep backward compatibility when adding fields. |
| Chinese report display | Completed | SummaryReport and AnalysisResult render normalized Chinese report sections. | Browser QA for copy action and visual polish. |
| Propagation graph | Completed for MVP | Graph renders small mock graph plus metrics/details. | Later add stronger graph metrics and real propagation data. |
| Dashboard visualization | Completed for MVP | Shows risk, sentiment, topics, bot impact, platform distribution, and summary. | Browser visual QA and optional chart interaction polish. |
| Export-friendly report layout | Completed for Markdown MVP | Report layout is readable, print-friendly, and completed cases can export/copy Markdown reports. PDF export is not implemented. | Add PDF export only after the Markdown/demo flow is stable. |
| Copy suggested response | MVP polish needed | Copy helper exists in frontend code path. | Confirm in browser QA and add user feedback polish if needed. |
| Empty/loading/error states | MVP polish needed | Implemented across major pages, but needs browser QA. | Verify manually with backend stopped and empty mock data. |
| Saved analysis cases | Completed for mock MVP | Lightweight in-memory case APIs and a Cases frontend page preserve keyword, platforms, analysis result, V1.5 risk output, and Chinese report context during a local session. | Add real persistence later with MongoDB/Redis only after the mock case flow is stable. |
| Alerting | Next implementation | Alert schemas/placeholders exist, but no mature workflow. | Add deterministic mock alerts from risk thresholds. |
| V1.5 topic-level risk model | Completed | Deterministic offline topic-level risk scoring is implemented in the backend mock pipeline and exposed through analysis, visualization, summary, and recommendation responses. | Keep V1 fields backward-compatible and validate browser display during demo QA. |
| Real Reddit adapter | Future real-data integration | Reddit remains mock-selectable and now has a safe adapter scaffold with default mock fallback. No product flow calls real Reddit APIs yet. | Add fixture-backed real-mode tests and compliance checks before enabling live use. |
| Official API integrations | Future real-data integration | Weibo, Bilibili, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao are planned. | Add adapter contracts after credentials/permissions are available. |
| Crawler-later platforms | Future real-data integration | Hupu, Baidu Tieba, Tianya, NGA, Maimai, The Paper/Pengpai News, and Jiemian News are visible but disabled. | Future public-page parser profiles only; no bypasses. |
| V2 dynamic risk model | Future advanced algorithm | Documented only. Requires time windows, history, influence graph, and credibility modeling. | Implement only after V1.5 and better fixtures are stable. |
| LLM-assisted analysis | Future advanced feature | Not required and not used. | Future optional strict-schema mode only; no hidden/private data access. |
