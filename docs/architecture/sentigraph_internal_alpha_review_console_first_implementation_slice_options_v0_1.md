# Sentigraph Internal Alpha Review Console First Implementation Slice Options v0.1

## Purpose

This document compares first implementation slice options after 8Z-17 planning and 8Z-18 safety contract tests. It selects only a future boundary, not implementation.

## Option A: pause_only

Risk classification: lowest.

Description:

- no implementation selected
- no backend code
- no tests
- no route/API
- no frontend
- no runtime

Why select if ambiguity remains:

- preserves current pause
- avoids exposure or readiness confusion
- avoids crossing actual write, production object, or route/UI boundaries

Status: valid fallback.

## Option B: backend-only safe metadata projection helper

Risk classification: low if separately approved.

Description:

- backend-only
- local-only
- test-first
- no route/API
- no frontend
- no runtime persistence
- no Evidence chain helper execution
- no actual Evidence Layer write
- no Review Queue runtime
- no production objects
- no Source 11 / FinalSummaryReport
- no public/export delivery
- no collector/provider jobs
- no real package reads
- no raw rows/comments/identities
- produces only a local safe review-console projection object from safe stage summaries or fixtures

Why selected:

- gives the future console a safe projection contract before any API or UI surface exists
- keeps all operator actions label-only
- preserves `human_review_required = true`
- preserves `no_automatic_trust_upgrade = true`
- avoids public/customer interpretation risk

Status: selected future boundary only.

Selected next boundary:

`ready_for_8Z_20_internal_alpha_review_console_safe_metadata_projection_helper_smoke`

## Option C: disabled-by-default internal read-only backend route skeleton

Risk classification: medium.

Description:

- internal/local route
- GET/read-only
- disabled by default
- safe metadata only

Why not selected:

- creates an API surface
- can be mistaken for an operational console
- should come only after a backend safe projection object exists
- needs separate approval phrase and route safety tests

Status: not next.

## Option D: frontend static read-only review console mock

Risk classification: medium/high.

Description:

- browser-visible static review console mock
- no backend route if implemented as static mock

Why not selected:

- UI can be misread as customer-facing or operational
- may imply route/frontend/product readiness
- should wait until backend projection contract exists
- would require browser self-validation and separate approval

Status: not next.

## Option E: actual review console route + UI implementation

Risk classification: high.

Why blocked:

- too broad
- crosses route/API/frontend boundaries
- increases exposure and readiness confusion
- may pressure downstream write/runtime assumptions

Status: blocked.

## Option F: write/runtime console

Risk classification: forbidden.

Includes:

- Review Queue runtime console
- Evidence write console
- production EvidenceItem console
- production case console
- production analysis_run console
- actual analysis execution console
- production Analysis Result console
- Source 11 / FinalSummaryReport / export/public delivery console

Why forbidden:

- crosses high-risk production/runtime boundaries
- conflicts with 8W-69 pause
- would require separate docs-only gates and exact approvals before any discussion

Status: forbidden / out of scope.

## Future 8Z-20 Phrase Status

Inactive future phrase only:

`APPROVE_8Z_20_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_METADATA_PROJECTION_HELPER_SMOKE`

This phrase does not authorize implementation in 8Z-19. It does not authorize route/API/frontend, actual Evidence Layer write, production EvidenceItem, Review Queue runtime, production case, production analysis_run, actual analysis execution, production Analysis Result, Source 11 runtime, FinalSummaryReport runtime, collector/provider jobs, real package reads, or public/export delivery.

## Non-selected Option Summary

- Option A remains fallback if the project chooses to pause.
- Option C is deferred until a safe projection object exists.
- Option D is deferred until backend projection and browser safety requirements are clearer.
- Option E is blocked as too broad.
- Option F remains forbidden.

## Final Selection

Selected: Option B, future backend-only safe metadata projection helper smoke, only if separately approved.

Default remains pause until the user provides the future exact approval phrase.
