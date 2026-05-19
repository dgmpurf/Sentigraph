# Sentigraph Current Project Status

Last updated: 2026-05-17

## Executive Summary

Sentigraph is a mock-first, offline-capable desktop web MVP for public opinion analysis, risk monitoring, and demo storytelling. The product can currently demonstrate the full local flow from keyword/case creation through deterministic mock analysis, V1.5 topic risk, Chinese report generation, Markdown export, monitoring snapshots, alerts, notifications, platform-readiness views, LLM safety diagnostics, selector repair mock tooling, and offline benchmark reporting.

The project is not production-ready. It does not call real platform APIs, does not run real crawlers, does not call real LLM APIs, does not send real notifications, and does not include authentication or production deployment hardening.

## Completed Core MVP Features

- FastAPI backend with modular routes, schemas, services, repositories, and tests.
- React + Vite desktop dashboard with dark dashboard style.
- Dashboard, Keyword Search, Cases, Analysis Result, Summary Report, Risk Monitor, Propagation Graph, Notifications, Public Parser Status, Platform Integration Overview, Selector Repair Tool, LLM Safety, and Benchmark Dashboard pages.
- Mock keyword expansion through the LLM provider interface with `MockProvider` as default.
- Deterministic mock analysis pipeline for local public-opinion scenarios.
- Text cleaning, duplicate detection, sentiment, topic clustering, propagation data, bot/repeated-script signals, and risk scoring foundations.
- Local JSON case persistence by default, with optional MongoDB store behind an explicit configuration path.
- Local reset, seed, and API smoke helper scripts.

## Completed V1.5 Risk Model

- Current static V1 scoring remains backward-compatible.
- V1.5 topic-risk layer is implemented for the mock pipeline.
- V1.5 outputs include topic-level risk, top risk topics, overall risk, real crisis risk, manipulation risk, and deterministic explanations.
- Chinese report and visualization outputs can consume V1.5 fields.
- V2 dynamic topic-window risk remains future work.

## Completed Case, Report, Monitoring, and Notification Features

- Case creation, listing, detail, and run flow.
- Chinese structured report generation.
- Markdown report export and copy/download support.
- Local monitoring snapshots for completed cases.
- Manual scheduler foundation through `POST /api/v1/scheduler/run-due`.
- Alert events for risk deltas, topic risk, real crisis risk, and manipulation risk.
- Local in-app notification outbox with read/simulated-send state.
- No real email, Slack, webhook, Enterprise WeChat, Feishu, SMS, push, or background delivery service is active.

## Completed Public Parser Platforms

Fixture-only public parser scaffolds exist for:

- `the_paper`
- `jiemian`
- `hupu`
- `tieba`
- `nga`
- `maimai`

These parsers use sanitized fixtures and selector profiles. Live public fetching remains disabled by default. The only documented live-fetch pilot is The Paper, and it remains explicitly opt-in/local-only. No parser uses login, cookies, captcha bypass, anti-bot evasion, proxy rotation, private pages, or hidden APIs.

## Completed Official API Scaffolds

Mock-only official API adapter scaffolds exist for:

- `bilibili`
- `weibo`
- `douyin`
- `kuaishou`
- `xiaohongshu`
- `zhihu`
- `douban`
- `toutiao`

Reddit has a mock/default adapter and an optional future official API path, but real Reddit mode remains blocked while API approval is pending.

All official API scaffolds normalize mock posts/comments into shared `RawPost` and `RawComment` schemas. Real modes stay disabled and return safe metadata rather than calling real APIs.

## Completed LLM Mock Infrastructure

- `LLM_PROVIDER=mock` is the default.
- `LLM_ENABLE_REAL_CALLS=false` is the default.
- `MockProvider` supports deterministic keyword expansion, sentiment assistance, topic extraction/summary, mock report/recommendation drafts, and selector repair suggestions.
- OpenAI, DeepSeek, and Qwen providers are placeholders only and do not make real calls.
- Usage guardrails record metadata-only mock usage summaries.
- LLM Safety page exposes provider status and key presence booleans only.
- No API key value, raw prompt, raw user content, raw HTML, or provider response body is stored in usage summaries.

## Completed Benchmark System

- Offline benchmark runner: `scripts/run_offline_benchmarks.py`.
- Benchmark fixtures live under `benchmarks/`.
- Current suites cover sentiment, topic clustering, V1.5 risk, report builder, report quality rubric, Markdown export, selector repair, public parser fixtures, and mock adapter normalization.
- Benchmark Dashboard displays latest summary, history, and regression status from generated `.benchmarks/` files.
- `.benchmarks/` output is gitignored and summary-only.
- Latest documented v4.5 benchmark status: 390 passed, 0 failed, 0 warnings.

## Known Non-Blocking Issues

- README and some older UI/documentation strings contain mojibake/encoding artifacts; this does not block backend behavior but should be cleaned before a public demo.
- Vite reports a large vendor chunk warning for Ant Design/ECharts; it is currently non-blocking.
- Some browser QA notes mention shared Ant Design `Spin` tip warnings; non-blocking.
- Benchmark history is local file-based, not durable storage.
- LLM usage guardrails are in-process/mock-only, not production-grade billing controls.
- Public parser fixtures are synthetic/sanitized and do not prove live-site robustness.
- No authentication or multi-user access model exists.

## Mock-Only Today

- Product analysis pipeline.
- Keyword expansion.
- Sentiment optional LLM mode.
- Topic summary optional LLM mode.
- Report/recommendation provider drafts.
- Official API platform adapters.
- Reddit unless approval and implementation are added later.
- Monitoring, scheduler, alerts, and notifications.
- Benchmark and evaluation data.

## Scaffold-Only Today

- OpenAI / DeepSeek / Qwen providers.
- Official API adapters for Bilibili, Weibo, Douyin, Kuaishou, Xiaohongshu, Zhihu, Douban, and Toutiao.
- Selector repair profile update workflow; suggestions are mock and review-only.
- Public parser live-fetch flow except the disabled The Paper local pilot.
- V2 dynamic risk model.
- Production persistence, queues, background scheduler, authentication, and real notification channels.

## Real-Data Ready Status

No platform is ready for production real-data ingestion today.

The repository is ready for controlled local demos and for the next external API application/permission verification phase. Douyin developer access is recorded and the planned app type is Web App, but OAuth, `item.comment`, and lawful `item_id` readiness remain unverified. Xiaohongshu developer access is recorded, but note-comment permission remains unverified. Reddit API approval is pending. Other official APIs remain unapproved or unapplied.

## Requires External API Approval or Console Verification

- Douyin: Web App redirect URI, test-account OAuth authorization, token flow, `item.comment` or equivalent scope, and lawful `item_id` source.
- Xiaohongshu: note/content/comment API availability and access limits.
- Reddit: API approval.
- Weibo: application blocked by company-age requirement.
- Bilibili: official API application and permission review.
- Kuaishou, Zhihu, Douban, Toutiao: official application and permission review later.

## Current Recommended Direction

Freeze scaffold expansion. The next stage should be:

1. Prepare a stable local demo build.
2. Audit Douyin and Xiaohongshu API permissions in their developer consoles.
3. Implement real Douyin mode only after Web App OAuth, `item.comment`, lawful `item_id` source, payloads, limits, and compliance constraints are confirmed.
