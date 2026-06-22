# Analysis Requests Backend Next Tiny Helper Candidate v1

Status: docs-only candidate design. This document does not implement a helper, change production code, modify tests, move modules, or add runtime behavior.

## Purpose

Phase 8E chooses the next safest tiny no-behavior-change backend helper candidate after the Phase 8D timestamp / ID helper extraction. It keeps the Analysis Requests refactor intentionally narrow and avoids broad store, schema, route, frontend, runtime, public access, delivery, report, Sandbox, public event, or production Evidence Layer work.

## Current Phase 8D Helper Status

Phase 8D added:

- `backend/app/services/analysis_request_shared.py`
- `backend/app/tests/test_analysis_request_shared.py`

The current shared helpers are:

- `utc_compact_timestamp()`
- `generate_record_id(prefix: str)`

Current usage is intentionally narrow:

- `_new_report_export_public_access_external_delivery_gate_id()`
- `_new_report_export_public_access_external_delivery_gate_audit_id()`

The helper preserves the existing `<prefix>_<YYYYMMDDTHHMMSSZ>_<8 lowercase hex chars>` shape. It does not read files, call networks, touch runtime data, read environment values, or modify state.

## Candidate Comparison

| Candidate | Expected future scope | Safety | Main risk | Recommendation |
| --- | --- | --- | --- | --- |
| Extend existing timestamp / ID helper to one adjacent family | Change a few `_new_*_id()` functions in `analysis_request_store.py`; optionally add prefix-shape test cases | Low | accidentally changing ID prefix or request/file naming expectations | Selected |
| Append-only audit helper | Extract shared audit list/write behavior | Medium/high | audit ordering, append-only semantics, per-family audit IDs, or audit existence checks could drift | Wait |
| Runtime path helper | Extract runtime directory/path construction | Medium/high | persisted file locations, list/read glob patterns, runtime labels, and absolute path safeguards could drift | Wait |
| Boundary flag builder/helper | Extract no-side-effect flag dictionaries | High | missing a phase-specific false flag or making dangerous capabilities look generic | Wait |
| Safe metadata projection helper | Extract field allowlist/denylist projection | High | accidentally copying unsafe provider/package fields | Wait |
| Eligibility blocker/warning helper | Extract blocker/warning accumulation | High | conservative gate readiness and status mapping could be weakened | Wait |
| Stop helper extraction and product planning checkpoint | No code changes | Very low | does not reduce backend duplication | Fallback |

## Recommended Next Candidate

Recommended candidate: extend the existing timestamp / ID helper usage to the immediately adjacent report export download/package artifact ID generators.

Recommended future Phase 8F target functions:

- `_new_report_export_download_package_artifact_id()`
- `_new_report_export_download_package_artifact_audit_id()`
- `_new_report_export_download_package_manifest_id()`

Why this is selected:

- it reuses the already-tested `generate_record_id(prefix)` helper
- it does not introduce a new helper family
- it touches only the local ID-generation tail of `analysis_request_store.py`
- it is adjacent to the current public access / external delivery gate chain
- it avoids route, schema, runtime path, JSON field, audit write/read, eligibility, and boundary flag changes
- it is easy to validate through existing package artifact, public-access gate, route, golden-contract, and full backend tests

The future implementation should not extend to every remaining `_new_*_id()` function in one pass. It should stop after this single adjacent artifact ID group.

## Fallback Candidate

Fallback candidate: pause helper extraction and do a product planning checkpoint.

Choose the fallback if:

- the team wants to avoid any backend refactor churn before a demo or release checkpoint
- there is uncertainty about whether more backend helper extraction is worth the validation cost
- the next product decision is more important than reducing a few repeated ID lines

The fallback should not implement public access, delivery, B-end reports, Sandbox generation, public event generation, Evidence Layer writes, production cases, production review queues, production dedup, provider jobs, collector jobs, live platform integrations, or live model integrations.

## Why Other Candidates Should Wait

Append-only audit helper should wait because audit records are governance history. A generic helper could accidentally change sort order, overwrite behavior, audit file names, per-family audit IDs, or audit existence checks.

Runtime path helper should wait because it touches persisted file locations, list/read compatibility, runtime labels, and absolute path exposure safeguards. It is better attempted after more ID-only extractions prove the no-behavior-change pattern.

Boundary flag helper should wait because false no-side-effect flags are part of the safety contract. A broad helper could omit a phase-specific flag or make future dangerous capabilities appear routine.

Safe metadata projection helper should wait because projection mistakes can expose raw provider/package fields. It should be designed with explicit allowlists and denylist tests before implementation.

Eligibility blocker/warning helper should wait because gate eligibility is phase-specific and conservative. Shared blocker logic could weaken privacy holds, rejected evidence exclusion, weak evidence warnings, or readiness status mapping.

Broad store/schema/routes/frontend splitting should wait because Phase 8 is still proving small, reversible extractions. The facade should remain `analysis_request_store.py` until helper-level refactors are well covered by tests.

## Expected Future Changed Files

If Phase 8F implements the selected candidate, expected changed files are:

- `backend/app/services/analysis_request_store.py`
- optionally `backend/app/tests/test_analysis_request_shared.py`

No other file should change for this candidate.

Files that should not change:

- `backend/app/services/analysis_request_shared.py`, unless adding no new behavior is impossible
- `backend/app/schemas/analysis_request.py`
- `backend/app/api/v1/routes/analysis_requests.py`
- frontend files
- runtime files
- Project Source files
- package/dependency files
- GitHub Actions workflow files

## Expected Future Tests

If Phase 8F implements the selected candidate, run:

```cmd
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_shared.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
.venv\Scripts\python.exe -m pytest backend/app/tests/test_analysis_request_store.py backend/app/tests/test_analysis_request_routes.py
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe scripts\run_offline_benchmarks.py
git diff --check
```

Optional helper-test update:

- add a parametrized prefix-shape assertion for `report_export_download_package_artifact`
- add a parametrized prefix-shape assertion for `report_export_download_package_artifact_audit`
- add a parametrized prefix-shape assertion for `report_export_download_package_manifest`

Runtime/artifact safety checks after future implementation:

- `runtime/analysis_requests/` remains ignored
- `frontend/dist/` remains ignored
- `.benchmarks/` remains ignored
- no runtime artifacts are staged
- no frontend build artifacts are staged
- no benchmark artifacts are staged
- no ZIP files are generated under `runtime`
- `.github/workflows/ci.yml` is not recreated

## No-Behavior-Change Checklist

The future implementation must preserve:

- route URLs
- response contracts
- schema class names
- status names
- decision names
- runtime directory names
- runtime path labels
- JSON field names
- append-only audit behavior
- audit list/read behavior
- boundary flag keys and values
- safe-mode keys and values
- public access / external delivery gate behavior
- report export download/package artifact behavior
- manifest runtime reference behavior
- no absolute filesystem path exposure
- no raw author identifier exposure

## Stop Conditions

Stop and revert the future implementation if any of these occur:

- route URLs change
- response contracts change
- status or decision names change
- runtime paths or directory names change
- JSON field names change
- report export download/package artifact IDs lose their prefixes
- manifest IDs lose the `report_export_download_package_manifest` prefix
- append-only audit behavior changes
- boundary flags change
- public access / external delivery behavior changes
- a public download route is created
- a file-byte response route is created
- a public URL or signed URL is generated
- external delivery is performed
- email is sent
- object storage upload is introduced
- portal publication is introduced
- ZIP or binary archive generation is introduced
- B-end report generation is introduced
- Sandbox or public event generation is introduced
- Evidence Layer write is introduced
- production case, production review queue, or production dedup is introduced
- provider or collector job execution is introduced
- live integration calls, URL fetching, scraping, or live model calls appear
- original package rows, evidence item CSV/JSONL files, or export artifact file contents are parsed for this refactor
- secret-like values or raw author identifiers appear in new fixtures or outputs

## Rollback Strategy

Rollback should be direct:

1. Restore inline timestamp/UUID expressions for the three selected report export download/package artifact ID functions.
2. Keep `analysis_request_shared.py` in place because Phase 8D already uses it.
3. Revert any optional helper-test prefix additions if they were only for the reverted candidate.
4. Re-run helper, golden-contract, store, route, full backend, and offline benchmark checks.

No runtime migration should be required because the selected candidate must preserve ID shape and file locations.

## Why Broad Splitting Must Still Wait

Broad store, schema, route, or frontend splitting should still wait because:

- `analysis_request_store.py` remains the compatibility facade
- route URLs and response contracts are more important than reducing file size in one pass
- late-chain governance families still share many phase-specific safety boundaries
- frontend behavior should not move until backend helper-level extraction has proven stable
- current golden-contract tests protect contracts, not every internal dependency that a broad split could disturb

The next backend step should stay smaller than a module split.

## Why Public Access / Delivery / Report / Sandbox Work Must Still Wait

The selected candidate is a refactor-only ID helper usage extension. It must not implement:

- public download route
- file-byte response route
- public URL
- signed URL
- external delivery
- email sending
- object storage upload
- portal publication
- ZIP or binary archive generation
- B-end report generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- provider execution
- collector jobs
- live platform calls
- live model calls

Provider output remains evidence, not truth. Passing a helper refactor does not make any downstream public access, delivery, report, Sandbox, public event, production write, or live integration capability available.

## Recommended Next Task

If accepted, Phase 8F should implement only the selected report export download/package artifact ID helper usage extension and then stop for validation. If the team wants to reduce refactor risk before a demo, choose the fallback product planning checkpoint instead.

