# Internal Operator Route/UI Contract-to-Test Mapping v0.1

## A. Purpose

This document maps 8T-17 / 8T-18 / 8T-19 / 8T-20 contracts to future tests.

This is docs-only. It does not implement tests, modify code, approve route implementation, approve UI implementation, or approve auth/runtime/storage/evidence-preview work.

## B. 8T-17 Route Skeleton Contract Mapping

| Contract requirement | Future test type | Expected assertion | Current implementation status | Implementation approved now? |
| --- | --- | --- | --- | --- |
| Disabled by default | Backend route smoke | Unset env returns safe `route_disabled` response | Existing route skeleton and smoke coverage | No |
| Enabled synthetic fixture only | Backend route smoke | Only explicit `1` / `true` / `yes` enables synthetic fixture mode | Existing synthetic/test-only mode | No expansion approved |
| GET-only | Route registry test | Route family contains GET and no POST/PUT/PATCH/DELETE | Existing route family verified | No method expansion approved |
| Safe list/detail metadata | Backend response test | List/detail responses are metadata-only and review-only | Existing synthetic fixture response | No expansion approved |
| Unknown candidate safe `not_found` | Backend response test | Unknown ID returns safe error with no path/raw metadata leak | Existing synthetic fixture behavior | No expansion approved |
| No evidence row parsing | File-open guard / static scan | No `evidence_items.jsonl` / `evidence_items.csv` open or parse | Existing smoke coverage | No |
| No real package read | Path guard / static scan | No real package directory or private export root access | Existing smoke coverage | No |
| No storage | Filesystem side-effect test | No runtime/staging/db/review queue artifacts created | Existing smoke coverage | No |
| No production import | Response and side-effect test | No Evidence Layer write, production case, or `analysis_run` | Existing contract only | No |
| No collector runtime | Static/path guard | No collector job, callback, API bridge, or private root access | Existing contract only | No |

## C. 8T-18 Auth / Local-only Contract Mapping

| Contract requirement | Future test type | Expected assertion | Current implementation status | Implementation approved now? |
| --- | --- | --- | --- | --- |
| No anonymous access | Future auth safety test | Future non-synthetic route denies anonymous access safely | Contract-only | No |
| Local-only / internal-only | Future locality test | Future access is blocked outside local/internal context | Contract-only | No |
| No public/customer/provider/private collector direct access | Route exposure test | No public/C-end/B-end/provider/collector alias routes exist | Contract-only plus current route registry checks | No |
| No query-string token | Static scan / request test | No query-string token accepted or documented as access path | Contract-only | No |
| No hardcoded token | Static scan | No hardcoded token in code/docs beyond forbidden-boundary text | Contract-only | No |
| No sessions/cookies/tokens unless separately approved | Static scan / auth test | No session/cookie/token auth added without explicit approval | Contract-only | No |
| Safe denial response | Backend response test | Auth/locality denials use safe error schema with no leaks | Contract-only | No |

## D. 8T-19 UI Contract Mapping

| Contract requirement | Future test type | Expected assertion | Current implementation status | Implementation approved now? |
| --- | --- | --- | --- | --- |
| Safe metadata display only | Future UI render test | UI displays only approved safe metadata fields | Contract-only | No |
| Raw rows/comments/identifiers/secrets/paths forbidden | Future UI text scan / browser smoke | No forbidden content appears in DOM/text | Contract-only | No |
| Active production/public actions forbidden | Future UI interaction test | No active production/public CTA exists | Contract-only | No |
| Internal/local boundary copy | Future UI render test | Boundary copy visible | Contract-only | No |
| Empty/denied states safe | Future UI state test | Disabled/auth/not-found/privacy states leak no paths/raw values | Contract-only | No |
| No customer/public/C-end/B-end exposure | Route smoke / UI route registry test | UI route, if approved later, remains internal-only | Contract-only | No |

## E. 8T-20 Readiness Decision Mapping

| Decision | Consequence | Future test/design need | Current implementation status |
| --- | --- | --- | --- |
| Route implementation not approved | Do not expand route behavior now | Safety test plan first | Not approved |
| UI implementation not approved | Do not add frontend UI now | UI safety test plan and first-slice design first | Not approved |
| Auth implementation not approved | Do not add auth runtime now | Auth/local-only test plan and explicit approval | Not approved |
| Storage not approved | Do not write persistent staging storage | Separate storage/privacy design gate | Blocked |
| Evidence row preview not approved | Do not open or display evidence rows | Separate evidence preview/redaction gate | Blocked |
| Production import not approved | Do not write Evidence Layer or production case | Separate production import governance gate | Blocked |
| Safety test plan is next gate | Create docs-only safety plan before implementation | 8T-21 docs-only test plan | Current phase |

## F. Readiness Verdict

```text
ready_for_safety_test_plan_docs = yes
ready_for_test_implementation = no
ready_for_route_implementation = no
ready_for_ui_implementation = no
ready_for_auth_runtime = no
ready_for_storage = no
ready_for_evidence_row_preview = no
ready_for_production_import = no
```

The mapping supports writing a future test implementation plan, but it does not approve tests or runtime implementation in this phase.
