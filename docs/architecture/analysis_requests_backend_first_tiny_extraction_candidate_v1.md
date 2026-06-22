# Analysis Requests Backend First Tiny Extraction Candidate v1

Status: docs-only candidate selection. This document recommends the first Phase 8D extraction and does not modify production code.

## Candidate

First extraction candidate: timestamp / ID generation helper.

Recommended helper module:

- `backend/app/services/analysis_request_shared.py`

Recommended helper functions:

```python
def utc_compact_timestamp() -> str:
    """Return the existing Analysis Requests compact UTC timestamp format."""

def new_prefixed_runtime_id(prefix: str) -> str:
    """Return '<prefix>_<timestamp>_<8 hex chars>' without changing existing ID shape."""
```

The existing `_new_*_id()` functions in `analysis_request_store.py` should remain as the public/internal call sites for Phase 8D. They should delegate only the repeated timestamp and suffix construction to the helper.

## Why This Candidate Is First

This is the least risky extraction because it does not require:

- changing FastAPI route definitions
- changing Pydantic schemas
- changing runtime directory names
- changing JSON file field names
- changing audit write/read order
- changing gate eligibility
- changing boundary flags
- changing safe metadata projection
- changing frontend code

It reduces duplicated code while keeping all existing family-specific ID functions visible in `analysis_request_store.py`.

## Current Repetition To Remove Later

The store contains many functions with this pattern:

```python
timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
return f"<family_prefix>_{timestamp}_{uuid.uuid4().hex[:8]}"
```

The future helper should centralize only the timestamp and UUID suffix pattern.

## Future Phase 8D Edit Scope

Expected future changed files:

- create `backend/app/services/analysis_request_shared.py`
- modify `backend/app/services/analysis_request_store.py`
- create `backend/app/tests/test_analysis_request_shared.py` if helper-specific tests are added

Files that should not change in Phase 8D:

- `backend/app/schemas/analysis_request.py`
- `backend/app/api/v1/routes/analysis_requests.py`
- frontend files
- runtime files
- docs other than an optional progress note
- package/dependency files
- Project Source files
- GitHub Actions workflow files

## Future Helper Contract

`utc_compact_timestamp()` must:

- use UTC
- keep the exact compact format: `YYYYMMDDTHHMMSSZ`
- return a string
- not read runtime data
- not read environment secrets
- not call external systems

`new_prefixed_runtime_id(prefix)` must:

- preserve the `<prefix>_<timestamp>_<8 hex chars>` shape
- accept only a non-empty prefix string supplied by existing store functions
- avoid path operations
- avoid runtime file reads/writes
- avoid route/schema imports
- avoid side effects other than local UUID generation

`_new_request_id(title)` should continue to preserve the existing slug segment:

```text
req_<timestamp>_<slug>_<8 hex chars>
```

It may call `utc_compact_timestamp()` and a future local suffix helper, but it should not be rewritten into `new_prefixed_runtime_id("req")` because that would drop the slug.

## Test Plan For Phase 8D

Add helper tests only if the helper module is created:

```python
def test_new_prefixed_runtime_id_preserves_shape() -> None:
    value = new_prefixed_runtime_id("manual_analysis_trigger")
    assert value.startswith("manual_analysis_trigger_")
    assert re.match(r"^manual_analysis_trigger_\\d{8}T\\d{6}Z_[0-9a-f]{8}$", value)


def test_utc_compact_timestamp_preserves_shape() -> None:
    value = utc_compact_timestamp()
    assert re.match(r"^\\d{8}T\\d{6}Z$", value)
```

Run after extraction:

```cmd
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_shared.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_store.py backend/app/tests/test_analysis_request_routes.py
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe scripts\run_offline_benchmarks.py
git diff --check
```

If no helper-specific test is added, run the remaining commands and explain why the extraction is fully covered by existing store/API/golden tests.

## Acceptance Criteria For Phase 8D

The extraction is acceptable only if:

- generated IDs keep existing prefixes
- generated IDs keep the compact UTC timestamp segment
- generated IDs keep an 8-character lowercase hex suffix
- request IDs keep their slug segment
- all existing Analysis Request store tests pass
- all existing Analysis Request route tests pass
- golden-contract tests pass
- full backend pytest passes
- offline benchmarks pass
- `git diff --check` passes
- no runtime/build/benchmark artifacts are staged

## Rollback Plan

Rollback steps:

1. Replace calls to `new_prefixed_runtime_id(prefix)` with the previous inline timestamp/UUID expression.
2. Replace calls to `utc_compact_timestamp()` in `_new_request_id(title)` with the previous inline timestamp expression.
3. Remove the helper import.
4. Remove `analysis_request_shared.py` only if it has no users.
5. Re-run golden, store, route, and full backend tests.

No runtime migration should be required.

## Stop Conditions

Stop and revert the future extraction if:

- any route URL changes
- any schema import changes
- any JSON field shape changes
- any runtime directory or filename convention changes
- request ID slug behavior changes
- audit ID prefixes change
- append-only audit behavior changes
- public access, external delivery, file-byte response, public/signed URL, ZIP generation, object storage, email, portal publication, B-end report, Sandbox/public event, Evidence Layer write, production case/review queue/dedup, live integration call, fetch, scrape, or live model call appears
- secret-like values, raw author identifiers, profile links, or artifact file content appear in new fixtures or responses

## Why Other Candidates Are Deferred

Runtime path helpers are deferred because they can affect persisted file locations and list/read compatibility.

Append-only audit helpers are deferred because they protect governance history and could affect audit ordering or overwrite behavior.

Boundary flag helpers are deferred because phase-specific no-side-effect flags should remain explicit until the pattern is proven.

Safe metadata helpers are deferred because over-general projection can accidentally copy unsafe fields.

Eligibility blocker/warning helpers are deferred because gate readiness logic is phase-specific and conservative by design.

## Recommended Next Task

Phase 8D should implement only this timestamp / ID helper extraction, then stop for validation. It should not combine path helpers, audit helpers, boundary flag helpers, safe metadata helpers, schema splitting, route splitting, or frontend work.

