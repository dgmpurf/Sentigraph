# Sentigraph Internal Alpha Review Console Future Disabled Backend Route Consumption Implementation Gate Contract v0.1

## Scope

This document defines the future 8Z-30 disabled backend route consumption smoke gate. It is inactive in 8Z-29 and does not implement frontend code, backend code, routes, APIs, runtime persistence, UI behavior, browser behavior, route calls, helper calls, or backend route consumption.

The future gate may be discussed only under:

`APPROVE_8Z_30_INTERNAL_ALPHA_REVIEW_CONSOLE_DISABLED_BACKEND_ROUTE_CONSUMPTION_SMOKE`

This phrase is inactive here and does not authorize anything in 8Z-29.

## Gate Purpose

The future gate would be the first tightly scoped implementation phase that lets the internal alpha review console frontend consume the existing disabled internal backend route skeleton. It would test the disabled/not-connected and safe local/synthetic states without changing backend route behavior, adding write operations, creating production objects, or expanding route/API scope.

## Allowed Future Scope

If separately approved, future 8Z-30 may:

- update frontend code only where needed for internal alpha review console route consumption
- add a tightly scoped read-only `sentigraphApi` helper for review-console projection retrieval
- call only `GET /api/v1/internal/alpha/review-console/projections/{projection_id}`
- keep projection IDs allowlisted and safe
- display disabled route responses as disabled or not connected
- display unsupported projection responses safely
- preserve the static fallback path
- preserve visible no-write and no-production boundaries
- preserve `human_review_required`
- preserve `no_automatic_trust_upgrade`
- run frontend build
- run browser smoke if browser capability is available
- report `browser_unavailable = yes` if browser cannot run
- run focused regressions for 8Z-22, 8Z-24, 8Z-26, and 8Z-28
- keep 8W-69 pause and 8W-70 non-selection intact

## Forbidden Future Scope

Future 8Z-30 must not:

- change backend route behavior
- add backend route/API behavior
- add POST / PUT / PATCH / DELETE routes
- create runtime persistence
- use Review Queue runtime
- perform actual Evidence Layer write
- create persisted Evidence Layer records
- create production EvidenceItem
- create production Review Queue item
- create production case
- create production analysis_run
- start actual analysis execution
- authorize production Analysis Result
- create production Analysis Result
- call Source 11 runtime
- create FinalSummaryReport runtime output
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- run collector/provider job
- inspect private collector source
- read real exchange/package dir
- parse production package rows
- fetch URL
- scrape
- call real API
- call real LLM
- publish/send/post/execute platform action
- expose raw rows/comments/identities
- expose secrets
- add public / C-end / B-end / customer route aliases
- add write / approve / publish / send / post / execute CTA
- claim operational or customer-facing completion

## API Helper Boundary

A future helper may be added only if it:

- is read-only
- uses GET only
- targets only the internal alpha review console projection endpoint
- accepts only a safe projection ID, not an arbitrary URL or file path
- does not accept credentials, cookies, tokens, or package paths
- does not download files
- does not return file bytes
- does not retry in a way that hides disabled route state
- does not auto-enable the backend route
- does not silently switch to another projection ID
- surfaces disabled/not-connected state explicitly

## UI Boundary

Future UI behavior must:

- keep the review console internal-only
- keep static fallback visible or available
- show disabled route state as disabled, not as operationally available
- show local/synthetic enabled mode only when the existing backend route allows it
- keep no-write copy visible
- keep no-production copy visible
- keep human review copy visible
- keep no automatic trust upgrade copy visible
- present allowed and blocked actions as labels only
- avoid public / customer / B-end / C-end copy
- avoid write/approve/publish/send/post/execute CTA
- avoid raw/private/secret fields

## Required Future Validation

Future 8Z-30 must run, unless a blocker is reported:

- frontend build
- focused frontend tests or static safety tests for the route helper and shell
- 8Z-22 disabled backend route skeleton regression
- 8Z-24 frontend safety regression
- 8Z-26 static shell regression
- 8Z-28 backend-route-consumption safety regression
- py_compile for any touched backend test/support files if touched for regression only
- browser smoke if browser capability is available
- console error check if browser smoke runs
- static scan for public aliases, forbidden raw fields, write CTA, and overclaim copy
- `git diff --check`

If browser automation is unavailable, future 8Z-30 must report `browser_unavailable = yes` and use fallback validation without claiming browser validation success.

## Stop Rules

Stop before implementation if:

- approval phrase is missing or ambiguous
- backend route behavior change is needed
- non-GET method is needed
- runtime persistence is needed
- write/approve/publish/send/post/execute CTA is requested
- route path becomes public/generic/customer-facing
- helper needs tokens, cookies, credentials, arbitrary URLs, or package paths
- UI needs raw/private/secret fields
- browser smoke is unavailable and fallback validation is insufficient
- 8Z-22 / 8Z-24 / 8Z-26 / 8Z-28 regressions fail
- the task drifts toward Review Queue runtime or actual Evidence Layer write
- the task drifts toward production objects, Source 11, FinalSummaryReport, or public delivery

## Relationship to Actual Write

This future gate does not approve actual write. Actual Evidence Layer write and production EvidenceItem creation remain separate high-risk docs-only gates.

## Relationship to Backend Route

This future gate must consume only the existing disabled internal backend route skeleton. Backend route expansion requires a later separate gate.

## Relationship to Frontend

This future gate is the first possible frontend route-consumption implementation boundary, but only if separately approved. 8Z-29 does not create the helper or consume the route.

## Relationship to 8W and Recording

This future gate does not reactivate 8W production Analysis Result authorization and does not prepare recording/video assets. 8W-69 pause remains preserved and 8W-70 reactivation remains not selected.

## Source Update Recommendation

No immediate Project Source update is required for this inactive future gate unless it becomes part of a larger checkpoint.

Source 11 update = no.
