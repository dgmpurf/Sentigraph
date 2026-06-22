# AnalysisRequests Refactor Migration Plan v1

Status: design only. This document defines a staged migration plan and does not refactor code.

## Purpose

The migration plan breaks the AnalysisRequests modularization into small, reversible phases. Each phase should keep route URLs, response contracts, runtime formats, append-only audit behavior, and safety boundaries stable.

## Global Principles

- No behavior change first.
- Keep route URLs stable.
- Keep response contracts stable.
- Keep tests green after each small extraction.
- Do not combine large backend and frontend refactors in the same commit.
- Prefer adapter and facade wrappers before moving internals.
- Keep runtime data backward compatible.
- Preserve append-only audit.
- Preserve all no-side-effect and boundary flags.
- Preserve all current safety copy.
- Do not introduce real APIs, real LLMs, provider jobs, or collector jobs.
- Do not introduce production Evidence Layer writes, production cases, production review queues, or production dedup.
- Do not introduce public access or external delivery.

## Phase 8A: Docs-Only Design

Expected changed files:

- architecture design docs only

Validation:

- `git diff --check`
- static scan of new docs
- `git status --short`

Stop conditions:

- any backend, frontend, test, runtime, package, or Project Source file changes
- any wording that implies real public delivery or production side effects

## Phase 8B: Backend Golden-Contract Inventory / Test Harness

Goal:

Create a contract inventory before moving code.

Expected changed files:

- backend tests
- optional docs update

Recommended inventory:

- route URL list
- response schema names
- decision literal values
- status literal values
- no-side-effect flag keys
- audit record required keys
- runtime directory names
- forbidden payload field matrix

Validation:

- targeted contract tests
- `backend/app/tests/test_analysis_request_store.py`
- `backend/app/tests/test_analysis_request_routes.py`
- full backend pytest before completion

Must not touch:

- frontend code
- runtime files
- production data
- route behavior

Commit strategy:

- one commit for test harness only

## Phase 8C: Backend Shared Helper Extraction Only

Goal:

Extract low-risk shared helpers while keeping `analysis_request_store.py` as the facade.

Candidate helpers:

- ID generation helpers
- path helpers
- safe JSON IO
- path containment checks
- safe root labels
- runtime-relative labels
- repeated boundary-note builders

Expected changed files:

- new backend service helper modules
- `analysis_request_store.py` facade imports/delegation
- tests only if import paths need coverage

Validation:

- targeted helper tests if added
- full Analysis Request store/API tests
- full backend pytest

Stop conditions:

- runtime path changes
- persisted JSON field changes
- absolute path exposure
- new side-effect flags missing or changed

Commit strategy:

- one small helper family per commit

## Phase 8D: Backend Module Extraction by One Family at a Time

Goal:

Move one governance family behind a module while keeping existing exported store functions.

Suggested order:

1. report_export_public_access_external_delivery
2. report_export_download_package
3. final_summary_report_export
4. final_summary_report
5. summary_report_candidate
6. report_generation
7. manual_analysis
8. analysis_promotion
9. dedup_governance
10. review_queue
11. review_only_case
12. import_governance
13. provider_result
14. request_core

Rationale:

Late-chain families are newer, narrower, and easier to isolate. Core request and import governance should move later because they are depended on by many phases.

Validation after each family:

- tests for that family
- full `test_analysis_request_store.py`
- full `test_analysis_request_routes.py`
- full backend pytest before declaring the family ready

Stop conditions:

- route URL change
- status or decision value change
- audit shape change
- missing append-only audit
- public delivery or production side-effect capability appears

Commit strategy:

- one family per commit
- do not combine unrelated family moves

## Phase 8E: Frontend Shared Component Extraction

Goal:

Extract pure display components without changing form behavior.

Candidate components:

- `StatusTag`
- `BoundaryBlock`
- `AuditTimeline`
- `EligibilitySummary`
- `JsonPreview`
- `SafeModeFlags`

Expected changed files:

- new frontend component files
- `AnalysisRequests.jsx` imports and render calls

Validation:

- `npm --prefix frontend run build`
- browser smoke `/#/analysis-requests`
- no `[object Object]`, `undefined`, or `NaN`
- no public URL, signed URL, runtime download, file-byte, or external delivery UI

Stop conditions:

- form submit behavior changes
- safety copy disappears
- console errors
- route fails to render

Commit strategy:

- extract read-only components first

## Phase 8F: Frontend Section Extraction

Goal:

Move one phase-specific section at a time into separate files.

Suggested order:

1. latest public-access / external-delivery section
2. download/package section
3. final report export section
4. final report section
5. report generation section
6. manual analysis section
7. promotion/dedup/review sections
8. import/core sections last

Validation:

- frontend build
- page smoke
- create-button presence where expected
- boundary copy visible
- no clickable runtime file download link
- no public/signed URL UI

Stop conditions:

- any form creates a different payload
- any dangerous now flag defaults to true
- section hidden or duplicated

Commit strategy:

- one section or small adjacent pair per commit

## Phase 8G: API Helper Split

Goal:

Move Analysis Request API helpers into grouped modules while preserving named exports from `sentigraphApi.js`.

Expected changed files:

- new API helper files
- `sentigraphApi.js` re-exports or facade wrappers
- imported section files only after wrappers are stable

Validation:

- frontend build
- browser smoke
- static scan for new `fetch(` or `axios` usage outside the existing API client pattern

Stop conditions:

- duplicated base URL handling
- new external network target
- changed normalized field shape
- raw object rendering regression

Commit strategy:

- one API family per commit, or one facade-only commit followed by consumer migration

## Phase 8H: Cleanup and Smoke

Goal:

Remove dead duplicate code only after all wrappers are stable and tests have passed.

Validation:

- full backend pytest
- offline benchmarks if shared behavior could affect existing flows
- frontend build
- browser smoke `/#/analysis-requests`
- static safety scan
- `git diff --check`

Stop conditions:

- any deleted wrapper still imported
- any route mismatch
- any UI section missing
- any runtime records unreadable

## Rollback Conditions

Rollback the current subphase if any of these appear:

- backend tests fail due to contract drift
- frontend build fails due to section extraction
- route URL changes unintentionally
- runtime file names or directories change unintentionally
- safety boundary copy disappears
- dangerous capability appears in code or UI
- absolute filesystem path appears in API/UI
- raw author identifiers appear in API/UI
- public access or external delivery appears as an action rather than a gate

## What Must Not Be Touched Without Separate Approval

- private collector project
- Project Source files
- GitHub Actions workflows
- package dependency files
- runtime records
- production Evidence Layer
- production cases
- production review queues
- production dedup
- live platform integrations
- real LLM integrations
- MediaCrawler or OpenClaw production ingestion

## Next Recommended Phase

If this design is accepted, Phase 8B should build the backend golden-contract inventory and test harness. It should not move code yet unless the contract inventory reveals that the current tests already fully cover the intended extraction boundary.

