# AnalysisRequests Modularization Refactor Design v1

Status: design only. This document does not implement a refactor, add a gate, change behavior, or change API contracts.

## Purpose

The AnalysisRequests subsystem has become the local governance spine for provider handoff, import planning, review-only case handling, dedup governance, analysis promotion, manual analysis, report generation, report export, package preparation, and public-access / external-delivery gates.

The purpose of this design is to define a staged modularization plan before more governance runtimes are added. The refactor goal is maintainability without behavior change.

## Why Refactor Is Needed

Current inspection shows the subsystem has crossed the point where continuing to append new phases into the same files increases operational risk:

- `backend/app/schemas/analysis_request.py`: about 4,987 lines and 191 schema classes.
- `backend/app/services/analysis_request_store.py`: about 11,333 lines and 460 functions.
- `backend/app/api/v1/routes/analysis_requests.py`: about 1,782 lines and 158 route functions.
- `backend/app/tests/test_analysis_request_store.py`: about 6,745 lines and 162 test functions.
- `backend/app/tests/test_analysis_request_routes.py`: about 3,890 lines and 91 test functions.
- `frontend/src/api/sentigraphApi.js`: about 5,060 lines.
- `frontend/src/pages/AnalysisRequests.jsx`: about 8,905 lines.

The risks are not just file length. The same files now mix request creation, provider-result reading, local runtime path policy, privacy guards, review-only governance, dedup gates, promotion gates, analysis gates, report gates, export gates, UI form state, UI normalization, and audit rendering. This makes it easy for a safe gate-only change to accidentally touch runtime IO, public delivery, evidence promotion, or UI behavior outside its intended phase.

## Current File Responsibilities

### Backend schemas

`analysis_request.py` currently holds request/core records, provider result contracts, import plan and preview schemas, review decision records, review-only case records, staging imports, review queue records, dedup records, promotion records, manual analysis records, report generation records, summary/final report records, export records, package records, public-access gate records, boundary flags, audit schemas, and many literal status/decision types.

### Backend store

`analysis_request_store.py` currently owns runtime directory discovery, ignored local JSON storage, record creation, record listing, record reading, validation, status mapping, decision mapping, eligibility policy, boundary blocks, audit creation, ID generation, runtime path helpers, safe JSON writing, safe preview reading, final report export writing, package manifest writing, and many privacy checks.

### Backend routes

`analysis_requests.py` currently exposes the whole request lifecycle through one router file: global lists, request-scoped list/detail/create endpoints, gate creation endpoints, audit list endpoints, and item-level action endpoints.

### Frontend API

`sentigraphApi.js` currently combines unrelated API clients and normalizers across the broader product, including the Analysis Requests governance chain.

### Frontend page

`AnalysisRequests.jsx` currently holds page shell, request list, request detail, many phase-specific forms, derived state, API loading, normalization display helpers, JSON preview helpers, gate cards, audit timelines, warnings, boundary copy, and button handlers.

## No Behavior Change Principle

The first refactor phases must be behavior-preserving:

- Route URLs remain stable.
- Request and response contracts remain stable.
- Runtime JSON file names, directories, IDs, and record shapes remain backward compatible.
- Existing UI text and safety boundary copy remain visible.
- Existing tests remain the source of truth.
- Append-only audit behavior remains unchanged.
- No current gate becomes a side-effecting runtime because of the refactor.

## Compatibility Preservation

Compatibility must be preserved through adapter and facade layers before moving internals. The existing public import paths can remain in place while they delegate to smaller modules. This lets tests continue importing current names while internals move in small batches.

Recommended compatibility pattern:

1. Add a new internal module with moved helper logic.
2. Keep the original function name exported from `analysis_request_store.py`.
3. Delegate from the original function to the new module.
4. Run the existing targeted store/API tests.
5. Only later, update direct imports once the adapter has proven stable.

## Staged Refactor Plan

1. Inventory and golden contracts.
   - Capture route URLs, schema names, status values, decision values, required boundary flags, and audit shape expectations.
   - Add targeted contract tests if coverage is missing.

2. Extract shared helpers only.
   - Move ID generation, runtime path helpers, safe JSON IO, path containment checks, and boundary-note helpers behind facades.
   - Preserve original function names.

3. Extract one backend family at a time.
   - Start with low-risk read/list-only or late-chain modules.
   - Avoid combining import-governance, dedup-governance, report-export, and public-delivery refactors in one commit.

4. Extract route groups after store modules are stable.
   - Use FastAPI sub-routers or local route modules mounted by the existing route file.
   - Keep `/api/v1/analysis-requests/...` unchanged.

5. Extract frontend shared UI components.
   - Start with read-only display helpers, boundary blocks, status tags, and audit timelines.
   - Avoid changing form submit behavior in the same commit.

6. Extract phase-specific frontend sections.
   - Move one section at a time from `AnalysisRequests.jsx`.
   - Keep the page shell and data loading stable until sections are migrated.

7. Split API helpers.
   - Group Analysis Request API helpers and normalizers by phase family.
   - Keep existing re-exports from `sentigraphApi.js` while consumers migrate.

## Rollback Strategy

Each extraction should be revertable without data migration:

- Do not rename runtime directories during early phases.
- Do not change JSON schema names or persisted field names.
- Do not change route paths.
- Do not change UI form payload keys.
- Keep adapters in the original module until the next phase is validated.
- If a phase fails tests or smoke, revert that phase only.

## What Must Not Change During Modularization

The refactor must not introduce:

- public download route
- file-byte response route
- ZIP generation
- public URL generation
- signed URL generation
- external delivery
- email sending
- object storage upload
- portal publication
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup execution
- B-end report generation
- Sandbox or public event generation
- provider or collector job execution
- real API calls
- URL fetching or scraping
- real LLM calls
- MediaCrawler integration
- OpenClaw production ingestion
- secret, token, cookie, session, salt, or raw author identifier exposure

## Test Preservation

Every refactor step should run the smallest relevant targeted tests first, then the broader Analysis Request tests:

- targeted tests for the moved family
- `backend/app/tests/test_analysis_request_store.py`
- `backend/app/tests/test_analysis_request_routes.py`
- frontend build after frontend changes
- browser smoke only when UI is changed

Full backend pytest should be run before declaring a milestone ready.

