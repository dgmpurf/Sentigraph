# Sentigraph Implementation Backlog

Last updated: 2026-05-14

This backlog prioritizes practical next work while keeping the MVP mock-first and offline.

## P0: Demo Stabilization

### Browser QA Pass

Goal: confirm the desktop MVP works in a real browser runtime.

Scope:

- run `docs/demo_checklist.md`
- verify Dashboard, KeywordSearch, AnalysisResult, SummaryReport, RiskMonitor, and PropagationGraph
- confirm suggested response copy button works
- confirm empty/loading/error states
- capture any console/runtime errors

Acceptance:

- no major runtime errors
- copy button works
- charts render at 1440px desktop width
- known visual issues are documented

### Empty State Review

Goal: make mock-first failure modes feel intentional.

Scope:

- backend unavailable state
- empty visualization arrays
- empty report arrays
- small propagation graph

Acceptance:

- pages show user-facing empty states
- no raw JavaScript objects render in React
- no chart crashes

## P1: V1.5 Topic Risk Shadow Model

### Topic Risk Service

Goal: add deterministic topic-level risk without replacing active V1 scoring.

Status: implemented for the offline mock pipeline.

Scope:

- create a topic risk scoring service
- calculate per-topic risk fields from current topic clusters and analysis results
- output `risk_model_version = "v1_5_topic_risk_mvp"` for the shadow model result
- keep active project-level scoring as `v1_static_mvp`

Acceptance:

- deterministic pytest fixtures
- no external API/LLM dependency
- missing optional inputs do not crash
- MongoDB-safe dictionary keys

### Backward-Compatible Schema Fields

Goal: expose topic risk data safely.

Status: implemented for analysis, visualization, summary, and recommendation responses.

Scope:

- optional `topic_risks`
- optional `top_risk_topics`
- optional `real_crisis_risk`
- optional `manipulation_risk`
- optional `risk_explanation`

Acceptance:

- existing frontend does not break
- docs/api_contract.md and docs/data_schema.md stay aligned
- tests validate response shape

### Report and Visualization Integration

Goal: let reports and dashboards explain risk by topic.

Status: implemented for backend report/visualization responses and frontend report/dashboard pages. Browser QA remains recommended.

Scope:

- use V1.5 topic risk output when present
- add top risk topic explanations to report builder
- add optional chart-ready topic risk data

Acceptance:

- SummaryReport remains Chinese-first
- existing V1 score cards stay stable
- frontend handles missing V1.5 fields

## P2: Product Polish

### Saved Analysis Cases

Goal: make the demo feel like a case-based product.

Status: completed for the lightweight mock MVP with local JSON backend persistence and a frontend Cases page.

Scope:

- mock case model
- local JSON persistence
- case list or recent case panel
- current case context in header

Acceptance:

- user can return to the last mock case
- no real database required in the first version

Follow-up:

- Add MongoDB/Redis-backed stores later behind the existing case repository/storage interface.
- Add migration/backup behavior before production-style deployments.

### Report Export Preparation

Goal: make reports easier to share.

Status: completed for Markdown copy/download. PDF export remains future work.

Scope:

- print-friendly CSS
- report metadata block
- stable section spacing
- future PDF export placeholder

Acceptance:

- browser print preview is readable
- no PDF library required yet

### Alert Refinement

Goal: turn risk thresholds into practical warning cards.

Status: v0.8 foundation implemented with persisted case snapshots, deterministic threshold alerts, per-case monitoring config, and a manual run-due scheduler endpoint. Real background scheduler, notifications, and delivery channels remain future work.

Scope:

- persisted analysis snapshots per case
- deterministic mock monitoring checks
- threshold alerts for risk increase, risk-level escalation, real-crisis increase, manipulation-risk increase, new high-risk topics, and top-topic shifts
- warning severity labels
- recommended action mapping
- monitoring schedule config per case
- manual scheduler status and run-due endpoints

Acceptance:

- RiskMonitor explains why an alert exists
- no real notification service required
- no real background worker starts by default

Follow-up:

- Add APScheduler only after local manual scheduler behavior is stable.
- Add Celery/RQ only if a real queue and deployment target are defined.
- Add notification channels later, for example email, Slack, or webhook, behind explicit user configuration.
- Add alert acknowledgement/resolution workflows when authentication exists.

## P3: Real Data Integration Preparation

### Adapter Contracts

Goal: prepare real adapters without implementing crawlers yet.

Status: foundation implemented and QA-stabilized for the safe Reddit scaffold.

Scope:

- shared platform adapter interface
- request/response shape for public posts/comments
- safe rate-limit and credential placeholders
- fixture-first test strategy

Acceptance:

- no real platform calls
- no API keys required
- no bypass behavior
- outputs normalize into `RawPost` and `RawComment`
- missing credentials fall back to mock mode

### Mock-only Crawl Adapter Bridge

Goal: connect `POST /api/v1/crawl/start` to the adapter factory in mock mode only, without enabling real Reddit mode.

Status: next recommended implementation task.

Scope:

- call `get_adapter("reddit")` only in mock mode when Reddit is selected
- keep existing crawl response shape stable
- attach or log normalized mock `RawPost` / `RawComment` counts for future pipeline integration
- keep official API planned platforms as placeholders
- keep crawler-later platforms disabled

Acceptance:

- no real Reddit API calls
- no credentials required
- old mock crawl behavior remains backward-compatible
- backend tests cover Reddit-selected crawl start and unknown/inactive platform handling

### Reddit Real Adapter Planning

Goal: define the first practical real-data candidate.

Status: minimal optional real-mode path implemented behind explicit credentials; live product flow is still disabled.

Scope:

- public API feasibility notes
- compliance constraints
- fixture schema
- adapter tests with recorded/sanitized fixtures only
- optional real mode using `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_USER_AGENT`
- helper/status methods: `has_required_credentials()`, `get_mode()`, `is_real_mode_enabled()`, and `get_status_metadata()`

Acceptance:

- implementation plan exists before any live call
- credentials remain outside the repository
- current case/mock analysis flow remains offline unless a future task explicitly enables real mode
- tests use mocked Reddit responses and do not make network calls

## P4: Future Advanced Algorithm

### V2 Dynamic Risk Readiness

Goal: prepare for full topic-cluster dynamic risk later.

Scope:

- time-windowed data fixtures
- topic history and baseline utilities
- influence graph metrics
- credibility modeling
- comparison between V1, V1.5, and V2 shadow outputs

Acceptance:

- V2 remains inactive until evaluated
- API migration is planned before exposure
