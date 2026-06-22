# Analysis Requests Backend Shared Helper Extraction Design v1

Status: docs-only design. This document does not extract code, change runtime behavior, move modules, or modify production backend/frontend files.

## Purpose

Phase 8C defines the safest first backend shared helper extraction for the large Analysis Requests backend. The goal is to reduce repeated code in a way that keeps `analysis_request_store.py` as the public facade and preserves all route URLs, response schemas, runtime JSON shapes, status names, decision names, append-only audit behavior, and boundary flags.

This phase is design only. The future extraction must be tiny, reversible, and protected by the Phase 8B golden-contract tests.

## Current Context

Phase 8B added backend golden-contract inventory docs and `test_analysis_request_golden_contracts.py`. Those tests protect:

- key `/api/v1/analysis-requests` route families
- latest and core schema class availability
- public access / external delivery default side-effect flags
- audit endpoint visibility
- ignored runtime/build/benchmark paths
- absence of dangerous delivery primitives in the Analysis Requests router
- absence of export artifact content reads or delivery primitives in the latest public-access / external-delivery store functions

The next extraction should rely on those guards while adding only focused helper tests if needed.

## Candidate Helper Families

### Timestamp / ID Helper

Observed pattern:

- many `_new_*_id()` functions repeat the same UTC timestamp format
- most return `<prefix>_<YYYYMMDDTHHMMSSZ>_<8 hex chars>`
- `_new_request_id(title)` adds a slug between timestamp and suffix

Safety assessment:

- safest first candidate
- no route behavior changes
- no schema class changes
- no runtime directory changes
- no persisted field name changes
- no audit semantics changes
- no boundary flag changes
- easy to validate with existing store/API tests

Risks:

- ID string format must remain byte-for-byte compatible enough for existing parsing expectations
- request IDs must preserve the title slug segment
- audit IDs and gate IDs must preserve their prefixes
- tests should not assert exact UUIDs, only prefix/shape and downstream behavior

Recommended phase:

- Phase 8D first tiny extraction candidate.

### Runtime Path Helper

Observed pattern:

- `_ensure_root()` creates many runtime directories
- path helpers repeat request ID validation, child directory selection, and file naming
- ID extraction helpers repeat prefix splitting checks

Safety assessment:

- useful but riskier than ID helper
- touches runtime path construction and persisted file locations
- mistakes could break existing records, list/read behavior, or runtime ignore assumptions

Risks:

- path labels or directory names could drift
- absolute path exposure protections could regress
- existing runtime JSON records could become unreadable
- audit list glob patterns could change

Recommendation:

- do not choose as first extraction
- consider after timestamp/ID helper proves the no-behavior-change pattern
- protect with targeted tests for runtime directory names, path labels, and list/read compatibility

### Append-Only Audit Helper

Observed pattern:

- create functions often build a record, build an audit record, write both, and expose list/read helpers
- audit list functions repeat sorted glob and model validation logic

Safety assessment:

- high value but medium risk
- audit behavior is governance-critical
- changes could affect ordering, audit existence checks, or append-only guarantees

Risks:

- accidentally overwriting audits
- changing sort order used by UI and tests
- losing per-family audit ID conventions
- hiding phase-specific audit fields behind a too-generic abstraction

Recommendation:

- defer until after at least one tiny helper extraction
- extract read/list-only audit helpers before write helpers
- keep per-family audit models explicit

### Boundary Flag Builder / Helper

Observed pattern:

- gate and audit records repeat no-side-effect dictionaries
- latest public-access / external-delivery gate has many false flags in request, record, audit, and tests

Safety assessment:

- high value but riskier than ID helper
- boundary flags are part of the safety contract and must remain explicit

Risks:

- generic helper could omit a phase-specific flag
- defaulting a dangerous flag incorrectly would be severe
- shared helper could make future unsafe capabilities look routine

Recommendation:

- defer
- if extracted later, prefer named family helpers such as `build_public_access_external_delivery_boundary_block()` rather than one permissive universal helper
- golden tests should continue checking dangerous flags directly

### Safe Metadata Projection Helper

Observed pattern:

- runtime records keep safe IDs, statuses, counts, source names, timestamps, and validation summaries
- unsafe fields such as raw identifiers, secret-like values, file bytes, profile links, and artifact contents must not enter API/UI records

Safety assessment:

- valuable but medium/high risk
- mistakes can expose sensitive metadata

Risks:

- helper may accidentally copy unknown payload keys
- helper may blur differences between safe metadata and raw provider/package rows
- hard to prove with only broad tests

Recommendation:

- not first
- introduce only with denylist and allowlist tests
- keep safe projections family-specific until patterns are proven

### Eligibility Blocker / Warning Helper

Observed pattern:

- gate builders collect blockers and warnings from upstream readiness, privacy hold, weak evidence, rejected evidence, audit presence, and unsafe side-effect flags

Safety assessment:

- useful but risky because eligibility logic is phase-specific

Risks:

- helper could over-generalize review-only governance
- blocker wording changes can affect UI and tests
- status mapping might drift from conservative behavior

Recommendation:

- not first
- extract only repeated tiny predicates, not full gate eligibility
- keep phase-specific status mapping near the gate family until module extraction is mature

## Recommended First Tiny Extraction

Choose the timestamp / ID helper family.

Future Phase 8D should add a small helper module such as:

- `backend/app/services/analysis_request_shared.py`

The first helper should be limited to:

```python
def utc_compact_timestamp() -> str:
    ...

def new_prefixed_runtime_id(prefix: str) -> str:
    ...
```

The request ID slug behavior should remain inside `analysis_request_store.py` or use the helper only for the timestamp and suffix. That avoids changing request ID semantics while still reducing duplicated timestamp/UUID code.

## Expected Future Changed Files

For the first extraction only:

- create `backend/app/services/analysis_request_shared.py`
- modify `backend/app/services/analysis_request_store.py` to import and use the helper inside `_new_*_id()` functions
- optionally add `backend/app/tests/test_analysis_request_shared.py` for helper shape tests
- optionally extend `backend/app/tests/test_analysis_request_golden_contracts.py` only if a stable import contract is desired

No route file, schema file, frontend file, runtime file, package file, Project Source file, or GitHub Actions workflow should change for the first extraction.

## Required Validation For Future Extraction

Before the future extraction:

```cmd
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_store.py backend/app/tests/test_analysis_request_routes.py
```

After the future extraction:

```cmd
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_shared.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_store.py backend/app/tests/test_analysis_request_routes.py
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe scripts\run_offline_benchmarks.py
git diff --check
```

If `test_analysis_request_shared.py` is not added, skip only that first command and explain why the existing tests are sufficient.

## How Golden-Contract Tests Protect The Refactor

The Phase 8B golden-contract tests protect this extraction by catching:

- missing key route families
- missing latest/core schema classes
- unsafe delivery primitives appearing in routes
- public-access / external-delivery side-effect defaults changing
- missing latest audit route/helper exposure
- runtime/build ignore regressions
- latest public-access / external-delivery functions reading artifact content or generating delivery

The ID helper extraction should not affect any of these. If it does, the extraction is too broad.

## Preservation Rules

The future extraction must preserve:

- route URLs exactly
- response model classes and field names
- status literal names
- decision literal names
- runtime directory names
- persisted JSON field names and values
- append-only audit behavior
- per-family audit ID prefixes
- request ID slug behavior
- boundary flag keys and default values
- no-side-effect safe mode flags
- no absolute filesystem path exposure
- no raw author identifier exposure

## Rollback Strategy

Rollback should be simple:

1. Restore the old inline timestamp/UUID expressions inside `_new_*_id()` functions.
2. Remove the new helper import.
3. Remove the new helper module only if no other code uses it.
4. Re-run the targeted golden, store, and route tests.

No runtime migration should be needed because the helper must preserve ID shape and file locations.

## Stop Conditions

Stop the future extraction immediately if any of these occur:

- route URL changes
- persisted JSON shape changes
- runtime directory names change
- generated IDs lose their existing prefixes
- request IDs lose the title slug segment
- audit records are overwritten instead of appended
- any dangerous side-effect flag defaults to true
- public download, file-byte response, public/signed URL, external delivery, object storage, email, portal publication, ZIP, B-end report, Sandbox/public event, Evidence Layer write, production case/review queue/dedup, live integration call, fetch, scrape, or real model call appears
- tests require reading original package rows or artifact file content
- raw author identifiers or secret-like fields appear in fixtures or outputs

## What Is Intentionally Not Implemented

This document does not implement:

- backend helper extraction
- schema split
- route split
- store family module split
- frontend extraction
- runtime migration
- production Evidence Layer write
- production case/review queue/dedup
- report/public event/Sandbox generation
- public access or external delivery
- live provider execution
- collector jobs
- live model integration

