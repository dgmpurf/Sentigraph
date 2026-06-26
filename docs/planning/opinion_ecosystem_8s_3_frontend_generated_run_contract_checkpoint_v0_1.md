# Phase 8S-3 Frontend Generated-run Contract Checkpoint v0.1

## A. Decision

```text
phase = 8S-3
decision = docs_only_frontend_generated_run_contract_checkpoint
current_state = ready_for_8S_3_frontend_generated_run_contract_planning
next_state_if_ready = ready_for_8S_4_backend_generated_run_route_contract_implementation_or_frontend_static_fixture_sync_decision
```

8S-3 defines how future frontend display and route/API contracts should handle backend generated run output. It does not implement the route or frontend integration.

## B. Why Docs-only

Phase 8S-2 created a backend-only generated run wrapper for `sentigraph_opinion_ecosystem_run_v0_1`.

Exposing that wrapper to frontend or HTTP needs a separate contract checkpoint because generated-run output changes the user-visible meaning of the Opinion Ecosystem page.

The frontend must distinguish:

- static/local explanatory snapshot
- backend-generated local run output
- blocked/manual-review run
- unavailable generated run

Without this checkpoint, a UI change could accidentally imply production scoring, official verification, prediction, full-web coverage, or response execution.

## C. Why Not Manual Playtest / Recording Yet

```text
manual_playtest_status = deferred_until_frontend_displays_generated_run
recording_status = deferred_until_frontend_displays_generated_run
```

Manual playtest and recording remain deferred because the current UI does not yet display backend generated-run output.

The next credible external demo should wait until:

- generated-run output is available through an approved route or controlled fixture sync
- the frontend shows generated-run metadata and boundaries
- blocked/manual-review states are visible
- screenshot/browser smoke confirms no overclaiming labels

## D. Recommended Next Implementation Choices

### Option A: Backend Route Contract Implementation For Generated Run

Add a tiny backend route in a later phase that exposes a safe local generated run from an approved in-memory fixture source.

Benefits:

- turns 8S-2 service output into a route-contract artifact
- keeps frontend untouched until the backend response is stable
- enables route-level tests for metadata, boundaries, blockers, and false side-effect flags

Risks:

- route request shape must not accept paths, raw rows, exchange dirs, or private collector inputs
- persistence must remain disabled unless separately approved
- route names must fit existing FastAPI patterns

### Option B: Frontend Static Fixture Sync With Backend Generated-run Sample Output

Use a static frontend fixture shaped like `sentigraph_opinion_ecosystem_run_v0_1`, generated or copied only after a controlled backend output is reviewed.

Benefits:

- allows UI layout work without live route coupling
- lowers API risk
- keeps static demo fallback easy to compare with generated-run display

Risks:

- can drift from backend output
- may continue the static-demo pattern longer than desired
- external viewers may still ask whether the run is generated live

### Option C: Docs-only API Route Implementation Checkpoint Extension

Create a more detailed route implementation plan before code.

Benefits:

- safest if route naming, fixture source, or request shape is still unsettled
- allows review of blocked/manual-review response examples before code

Risks:

- slows the minimum real-run loop
- does not create new runtime evidence beyond the current 8S-2 service wrapper

### Recommended Safest Next Step

Recommended next step after 8S-3:

```text
8S-4 backend generated-run route contract implementation
```

This should be a tiny backend-only route slice with:

- no frontend integration
- no runtime persistence
- no file IO
- no real package row parsing
- no exchange dir access
- no private collector access
- no real API
- no real LLM
- no Evidence Layer write
- no production case
- no production `analysis_run`

If the route request shape is not approved, choose Option C first and keep 8S-4 docs-only.

## E. Acceptance Criteria For This Docs-only Phase

8S-3 is complete when:

- `docs/architecture/opinion_ecosystem_frontend_generated_run_display_contract_v0_1.md` exists
- `docs/architecture/opinion_ecosystem_generated_run_route_api_contract_checkpoint_v0_1.md` exists
- `docs/planning/opinion_ecosystem_8s_3_frontend_generated_run_contract_checkpoint_v0_1.md` exists
- no backend code changed
- no frontend code changed
- no tests changed
- no runtime files changed
- no package files changed
- no Project Source files changed
- no real API or real LLM was called
- no collector was run or accessed
- no private collector was accessed
- no real exchange dir was read
- no URL was fetched
- no website was scraped
- safety scans pass or only show accepted boundary/deferred/forbidden language

## F. Source Recommendation

After commit:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request, Provider, or Import Governance behavior changes.
