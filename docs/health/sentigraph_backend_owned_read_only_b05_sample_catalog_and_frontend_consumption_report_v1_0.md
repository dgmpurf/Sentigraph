# Sentigraph Backend-owned Read-only B05 Sample Catalog and Frontend Consumption Report v1.0

## Goal lifecycle

- Goal: `SENTIGRAPH_BACKEND_OWNED_READ_ONLY_B05_SAMPLE_CATALOG_AND_FRONTEND_CONSUMPTION_V0_1`
- Fresh Goal requested / activated: yes / yes
- Former Goal or executor reused: no
- Approval UTF-8 bytes: `1370`
- Approval SHA-256: `05ada0750b24a675b55c7ebbab1c61cba232357eed0f2f281be7edda48599177`
- Approval consumed / reusable after activation: yes / no
- Bounded mechanical corrections: migrated directly related frozen tests to the registry-owned catalog contract; used `npm.cmd` after the PowerShell script launcher was blocked before Vite started.
- Product retries, real B05 retries, browser retries: `0 / 0 / 0`

## Starting repository checkpoint

- Repository: `dgmpurf/Sentigraph`
- Branch: `main`
- Starting HEAD and `origin/main`: `cdc1c668120ab668d95cfeec902abfb5e4026417`
- Starting commit message: `Add dual read-only B05 sample selection`
- Starting tracked / staged / untracked state: clean / `0` / `0`
- Bound catalog objective already present: no
- Backend/frontend project ports `8000 / 5173`: closed / closed

## Exact changed-file set

Product and route code:

1. `backend/app/services/internal_alpha_local_exchange_review_projection.py`
2. `backend/app/services/internal_alpha_local_exchange_sample_catalog.py`
3. `backend/app/api/v1/routes/internal_alpha_review_console.py`
4. `frontend/src/api/sentigraphApi.js`
5. `frontend/src/pages/InternalAlphaReviewConsole.jsx`

Directly related tests:

6. `backend/app/tests/test_mvp_b05_sample_catalog_frontend_consumption.py`
7. `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py`
8. `backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py`
9. `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py`

Health report:

10. `docs/health/sentigraph_backend_owned_read_only_b05_sample_catalog_and_frontend_consumption_report_v1_0.md`

No existing file is deleted. No dependency, lockfile, database, migration, configuration, Project Source, Provider Result, package, receipt or personal-crawler file is changed.

## Architecture and catalog ownership

The immutable backend B05 sample registry remains the private owner of each Provider Result mapping and now also owns the safe catalog metadata:

- `sample_handle`
- `display_label`
- `sample_role`
- `is_default`
- `enabled`
- `catalog_order`

A dedicated pure in-memory service projects only safe catalog metadata. It performs no filesystem, Provider Result, package, receipt, row, environment-value, database, network or persistence operation. The internal route reuses the existing shared Internal Alpha review-console gate and is GET-only.

The private `result_file_name`, route mode and capability label remain backend-only. They are not members of the catalog response.

## Safe catalog contract

Route:

`GET /api/v1/internal/alpha/review-console/local-exchange-samples`

Top-level ordered fields:

1. `schema`
2. `version`
3. `mode`
4. `status`
5. `sample_count`
6. `default_sample_handle`
7. `samples`
8. `read_only`
9. `human_review_required`
10. `production_ready`
11. `mutable_authority_granted`

Ready identity:

- Schema: `sentigraph_internal_alpha_local_exchange_sample_catalog_v0_1`
- Version: `0.1`
- Mode: `internal_alpha_read_only_local_exchange_sample_catalog`
- Status: `ready`

Sample-entry ordered fields:

1. `sample_handle`
2. `display_label`
3. `sample_role`
4. `is_default`
5. `enabled`
6. `catalog_order`

Exact ready order:

1. `Current curated sample`; `helldivers2-psn-demo`; role `current_curated`; default and enabled
2. `Accepted historical sample`; `helldivers2-psn-demo-20260614`; role `accepted_historical`; nondefault and enabled

Safety flags:

- `read_only = true`
- `human_review_required = true`
- `production_ready = false`
- `mutable_authority_granted = false`

The catalog excludes Provider Result/package basenames, paths, configuration values, adapter identity, Artifact contents, raw metadata, evidence/source/comment rows, receipts, collector internals and any trust, production or mutable authority.

Validation fails closed for an empty or oversized catalog, mapping/handle mismatch, duplicate handles or labels, unsafe labels or roles, missing or multiple defaults, a disabled default, malformed booleans, noncontiguous order, or registry route/capability mismatch. A disabled gate or invalid registry returns a bounded `unavailable` envelope with zero samples and no internal error detail.

## Frontend single-runtime-source behavior

The Local-exchange projection review page now:

- requests the backend catalog once at most per component mount;
- strictly validates exact top-level and sample-entry field order and values;
- obtains selector handles, labels, roles, default, enabled state and order only from the loaded catalog;
- contains no hardcoded runtime handle/label fallback catalog;
- selects the one catalog default after successful normalization;
- disables catalog entries marked disabled;
- issues no B05 projection request until the catalog is loaded and the selected entry is enabled;
- shows a bounded loading/unavailable state without internal error, path or configuration detail;
- retains independent per-handle request state and in-memory cache;
- performs at most one projection GET per handle per page mount;
- reuses a previously requested handle without another request;
- performs no retry, polling or historical prefetch;
- adds no localStorage, sessionStorage, mutation, promotion, public, export or delivery control.

The existing current sample remains the default and the accepted historical sample remains selectable. The existing private B05 registry mapping is unchanged.

## Test-first and validation evidence

RED command:

`python -m pytest backend/app/tests/test_mvp_b05_sample_catalog_frontend_consumption.py -q`

RED result:

- collection stopped because the bound registry entry did not yet have `display_label`;
- the failure was directly attributable to the missing backend catalog ownership contract;
- product files had not yet been modified.

Focused and nearby GREEN set:

- 294 tests collected across the new catalog contract, B01, B03, B05 and Internal Alpha 8Z-18/20/22/24/26/28/30 suites;
- result: all 294 passed;
- the new contract file contributes 15 passing tests, including an in-process gated catalog GET with Artifact builders replaced by failure sentinels.

Python validation:

- Changed Python service and route sources compiled in memory with `compile()`.
- Changed service and route modules imported with `python -B`.
- Result: pass; no bytecode cache requested.

Frontend production build:

- Launcher note: PowerShell blocked `npm.ps1` before the build process started.
- Actual build command: `npm.cmd run build`
- Vite: `5.4.21`
- Modules transformed: `4028`
- Result: pass in `10.40s`
- Existing large-chunk advisory remained nonblocking; no dependency or build configuration changed.

Repository validation:

- `git diff --check`: pass before report creation and required again before commit.
- Frontend runtime catalog duplicate scan: no duplicated handles, labels, safe-handle array or static sample-options catalog.
- No real runtime or browser validation was performed.

## No-action ledger

- Real Provider Result reads: `0`
- Package / receipt / row reads: `0 / 0 / 0`
- Real B05 projection GET: `0`
- Live backend / frontend server starts: `0 / 0`
- Browser / navigation / screenshot: `0 / 0 / 0`
- External network before authorized Git push: `0`
- Database / persistence / Evidence Layer writes: `0 / 0 / 0`
- Production / public / export / delivery: `0 / 0 / 0 / 0`
- Project Source changes: `0`
- Personal-crawler access: `0`
- Dependency or lockfile changes: `0`

## Commit, push and downstream boundary

Authorized commit identity:

- Parent: `cdc1c668120ab668d95cfeec902abfb5e4026417`
- Message: `Add backend-owned B05 sample catalog`
- Branch and push target: local `main` to `origin/main`
- Resulting commit SHA and final local/remote alignment are recorded in the terminal receipt because a commit cannot contain its own SHA without changing that SHA.

This report does not claim real catalog browser validation, a real B05 GET, Artifact validation, production readiness, Source activation or independent ChatGPT acceptance.

Downstream runtime, persistence, production, public, export and delivery authority remains none. Independent ChatGPT review of the final commit and terminal receipt is required.
