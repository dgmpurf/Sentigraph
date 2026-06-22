# Analysis Requests Backend Golden Contract Test Plan v1

Status: test/docs-only plan. This document describes the test harness and does not move production modules.

## Purpose

The golden-contract tests protect the existing backend Analysis Requests governance behavior before modularization starts. The tests are intended to catch accidental route removal, schema deletion, dangerous public-delivery implementation, lost boundary flags, and runtime ignore regressions.

## Test Harness Strategy

The test harness should be stable and contract-focused:

- inspect FastAPI route paths for critical family fragments
- inspect source text for dangerous route implementations
- import schema classes to confirm latest and earlier families still exist
- instantiate latest public-access / external-delivery gate schemas where feasible
- check default dangerous `*_now` request flags are false
- check safe-mode and audit `now_flags` stay false for dangerous capabilities
- check Git ignore protection for runtime/build/benchmark paths
- inspect only targeted public-access / external-delivery store functions for source/content-read regressions

## Contracts Safe To Assert

Safe assertions:

- critical route families remain mounted
- latest schema classes remain importable
- dangerous route primitives are not used in the Analysis Requests router
- public-access / external-delivery request defaults keep dangerous flags false
- public-access / external-delivery gate and audit safe-mode flags remain false
- runtime folders remain ignored
- latest public-access / external-delivery gate code does not use file-byte responses, ZIP generation, artifact content reads, URL generation, email, object storage, or portal publication
- audit endpoints/classes exist for the latest gate family

## What Should Not Be Over-Snapshotted

Avoid brittle assertions such as:

- exact total route count
- exact line numbers
- exact function ordering
- exact full OpenAPI output
- exact full schema JSON for every class
- exact full source file text
- exact count of runtime helper functions
- exact number of warnings in unrelated tests

Future modularization should be able to add helpers or split modules without rewriting unrelated golden tests.

## Stable Tests For Refactor Protection

Stable protection areas:

- route family presence
- dangerous route implementation absence
- schema family existence
- public-access / external-delivery boundary defaults
- audit class and audit endpoint presence
- ignored runtime/build folders
- targeted no-content-read checks for the latest gate family

## Intentional Test Updates

If a future approved behavior change intentionally adds a new capability, update tests in the same commit as the approved design/runtime change. The update must explain:

- which contract changed
- which safety gate approved it
- why the old boundary no longer applies
- what replacement boundary protects users
- which tests now cover the new behavior

Examples requiring explicit test changes:

- approved download runtime
- approved file-byte route
- approved signed URL runtime
- approved external delivery runtime
- approved B-end report generation
- approved Sandbox/public event generation
- approved production Evidence Layer write

## Stop Conditions

Stop and do not proceed with modularization if tests reveal:

- a critical route family is missing
- a schema class for the current chain is missing
- dangerous response types or delivery helpers appear in the router
- public-access / external-delivery flags default to true
- latest gate code reads export artifact file content
- runtime/build artifacts are not ignored
- `.github/workflows/ci.yml` is recreated
- raw author identifiers or secrets appear in new test fixtures
- tests require reading original package rows or evidence CSV/JSONL

## Validation Commands

Run:

```cmd
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
python -m pytest backend/app/tests/test_analysis_request_store.py backend/app/tests/test_analysis_request_routes.py
python -m pytest
python scripts\run_offline_benchmarks.py
git diff --check
```

On machines where bare `python` is not available, use the existing project Python executable and report the substitution.

## Runtime Safety Checks

After tests:

- `runtime/analysis_requests/` remains ignored
- `frontend/dist/` remains ignored
- `.benchmarks/` remains ignored
- no runtime artifacts are staged
- no frontend build artifacts are staged
- no benchmark artifacts are staged
- no ZIP files were generated under `runtime`
- `.github/workflows/ci.yml` was not recreated

