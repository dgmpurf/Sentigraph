# Internal Operator Env Gate Helper 8T-29 Allowed Change and Validation Contract v0.1

## A. Purpose

This document defines what a future 8T-29 implementation would be allowed to change only if explicitly approved.

It does not approve implementation.

## B. Allowed Implementation Strategy If 8T-29 Is Approved

Preferred implementation strategy:

Option A:

Extract the existing env decision logic into a local private helper inside:

`backend/app/api/v1/routes/internal_operator_review_only_staging.py`

Optional only if justified:

Option B:

`backend/app/services/internal_operator_route_guard.py`

Option A is preferred because it has the smallest surface area.

## C. Allowed Future Changed Files If Explicitly Approved

Allowed:

- `backend/app/api/v1/routes/internal_operator_review_only_staging.py`
- `backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py`
- `backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py`
- `backend/app/tests/test_internal_operator_route_ui_safety_contract.py`

Optional only if justified:

- `backend/app/services/internal_operator_route_guard.py`
- `backend/app/tests/test_internal_operator_route_env_gate_helper.py`

Forbidden:

- frontend files
- Source files
- `docs/project_sources`
- GitHub Actions
- storage/runtime persistence files
- Evidence Layer code
- production case code
- collector bridge/runtime code
- public/C-end/B-end route files

## D. Required Validation If 8T-29 Is Explicitly Approved

Required:

```text
python -m pytest backend/app/tests/test_internal_operator_route_ui_safety_contract.py
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
python -m py_compile backend/app/api/v1/routes/internal_operator_review_only_staging.py
git diff --check
git status --short
```

Optional:

- full backend pytest if helper extraction touches shared backend behavior or if route snapshots are unexpectedly different.

## E. Required Behavior Preservation

Future implementation must preserve:

- unset env disabled
- empty env disabled
- `false` disabled
- `0` disabled
- unknown disabled
- `1` enabled synthetic fixture only
- `true` enabled synthetic fixture only
- `yes` enabled synthetic fixture only
- current normalization behavior
- current response shape
- current route URL
- current route methods
- no public aliases
- no file reads
- no side effects

## F. Stop Rules

Stop if:

- route enabled by default.
- any disabled env becomes enabled.
- any enabled env becomes disabled.
- production mode appears.
- query-param/cookie/token/session enablement appears.
- response schema changes.
- route URL or method changes.
- `evidence_items` opening appears.
- private collector root read appears.
- storage/Evidence Layer/production case/analysis_run appears.
- UI appears.
- Source files appear.
- GitHub Actions workflow appears.
