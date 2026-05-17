# Sentigraph Next-Stage Roadmap Freeze

Last updated: 2026-05-17

## Purpose

This document freezes the next-stage direction so Sentigraph stops expanding scaffolds by default. The current system is broad enough for a mock-first product demo and for targeted real-data readiness work. New work should now fit one of the three tracks below.

## Freeze Rules

- Do not add new platform adapters for now.
- Do not add new public parser platforms for now.
- Do not add new LLM providers for now.
- Do not enable real LLM calls.
- Do not enable real platform APIs.
- Do not enable live public fetching by default.
- Do not restore GitHub Actions CI unless explicitly requested.
- Prefer demo stability, API permission verification, and benchmark-guided changes over more scaffolding.

## Track A: Product Demo Hardening

Goal: make a clean, repeatable local demo.

Scope:

- Run a full local reset/seed/smoke cycle.
- Confirm `python -m pytest`, `python scripts/run_offline_benchmarks.py`, and `npm run build`.
- Polish README run instructions where mojibake or stale commands are confusing.
- Polish critical UI labels only where demo-visible text is corrupted or unclear.
- Confirm sidebar routes load:
  - Dashboard
  - Keyword Search
  - Cases
  - Analysis Result
  - Summary Report
  - Risk Monitor
  - Propagation Graph
  - Notifications
  - Public Parser Status
  - Platform Integration Overview
  - Selector Repair Tool
  - LLM Safety
  - Benchmarks
- Prepare demo screenshots.
- Prepare a demo story:
  - seed demo data
  - open a completed case
  - show V1.5 risk topics
  - show Chinese report and Markdown export
  - run mock monitoring
  - show alerts/notifications
  - show platform/LLM/benchmark safety pages

Recommended immediate task:

1. Prepare a stable demo build.

Definition of done:

- Backend tests pass.
- Offline benchmarks pass.
- Frontend build passes.
- Demo reset/seed/smoke commands are documented and work locally.
- Known issues are documented as non-blocking.
- No real APIs or live fetch paths are enabled.

## Track B: Real Data Access

Goal: verify whether real comment data is legally and technically available through official APIs.

Scope:

- Douyin capability audit:
  - developer access obtained
  - comment permission unknown
  - verify interaction/comment management
  - verify `item.comment` or equivalent scope
  - verify keyword video comment management if applicable
  - verify user authorization and access limits
- Xiaohongshu capability audit:
  - developer access obtained
  - note/comment API availability unknown
  - verify whether public note/comment APIs exist
  - verify whether access is limited to own account, merchant, Ark/ad, or approved creator content
- Reddit:
  - API approval pending
  - no scraping bypass
- Bilibili / Weibo / Zhihu:
  - application work later
  - Weibo currently blocked by company-age requirement
- No public-page scraping bypasses.
- No login/captcha/anti-bot work.

Recommended order:

1. Audit Douyin and Xiaohongshu API permissions.
2. Add approved official payload fixtures.
3. Implement minimal Douyin real mode only after permission is confirmed.
4. Repeat for Xiaohongshu only if an official comment API is confirmed.

Definition of done for a real-data permission audit:

- Console screenshots or notes confirm exact product, scope, endpoint, and access limits.
- Required credentials and OAuth/token flow are documented without storing values.
- Rate limits, data retention, and compliance constraints are documented.
- Approved response fixtures are added before any real request code.

## Track C: Intelligence Layer

Goal: improve intelligence quality only after the data path is stable.

Current policy:

- Keep `LLM_PROVIDER=mock` by default.
- Keep `LLM_ENABLE_REAL_CALLS=false` by default.
- Keep rule-based sentiment as default.
- Keep template topic summary as default.
- Keep report builder deterministic/template-based.
- Use offline benchmarks for regression protection.

Later choices:

- Choose one real LLM provider first, not all providers at once.
- Add mocked HTTP client tests before live calls.
- Add prompt/output schemas and redaction tests.
- Add usage/cost limits and provider pricing fixtures.
- Evaluate changes with offline benchmarks before enabling real calls.
- Connect real LLM only after real data flow is stable and privacy handling is reviewed.

Recommended timing:

- Do not start real LLM integration before Track A is demo-stable and Track B has at least one verified official data path.

## Top Three Next Tasks

1. Prepare a stable demo build.
2. Audit Douyin and Xiaohongshu API permissions in their developer consoles.
3. Implement real Douyin mode only after comment permission is confirmed.

## Stop Doing For Now

- Stop adding more official API adapter scaffolds.
- Stop adding more public parser platforms.
- Stop adding more LLM provider abstractions.
- Stop expanding benchmark suites unless they directly support a demo or a real-data integration decision.
- Stop building real-mode code before console permissions and official payload fixtures are confirmed.
