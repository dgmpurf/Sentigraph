# Post-8R Minimum Real-run Closed Loop Decision Checkpoint v0.1

## A. Purpose

This checkpoint defines what "minimum real-run" means for Sentigraph after the Phase 8R model-card QA and screenshot smoke work.

Manual playtest and recording are deferred until a minimum real-run closed loop exists. The current static/local explanatory UI is useful for internal QA, but external users need to see a generated run record rather than only a hardcoded explanatory snapshot.

This document is docs-only. It does not authorize backend code, frontend code, API routes, schemas, tests, runtime persistence, collector access, real APIs, real LLMs, URL fetching, scraping, or Project Source changes.

## B. Why Static Demo Is Not Enough

The current Phase 8Q / 8R UI is a static/local explanatory UI. It is useful for:

- verifying model-card language
- validating boundary labels
- showing module meaning
- checking screenshot readiness
- proving that the UI does not overclaim production capability

It is not enough for external manual playtest because users may confuse:

- a selected static sample with a generated run
- model explanation with real runtime output
- screenshot smoke with product operation
- fixture labels with backend-validated input scope
- a hardcoded report sample with report runtime
- a public event page with a generated analysis lifecycle

For external demo confidence, Sentigraph needs at least one controlled, local, backend-generated run output that the frontend can display with clear boundaries.

## C. Definition Of Minimum Real-run

Minimum real-run means all of the following are true:

- a user or operator selects or creates an event or sample package
- the backend reads a controlled local sample, package, or metadata source
- the backend validates safe input boundaries
- the backend creates a run record or run candidate
- the backend invokes the Opinion Ecosystem deterministic calculator
- the backend produces a versioned calculator output with:
  - `run_id`
  - input scope
  - model metadata
  - boundary flags
  - warnings
  - blockers
- the frontend can display the generated run output instead of a hardcoded static-only explanatory snapshot
- the UI still labels:
  - selected sample
  - not full-web
  - not full-platform
  - not full-thread
  - not official verification
  - not causal proof
  - not prediction
  - human review required

Minimum real-run is still local, bounded, selected-sample, deterministic, and non-production. It is a closed loop from controlled input to generated calculator output to frontend display, not a claim of full public-opinion coverage or truth.

## D. What Does Not Count As Minimum Real-run

The following do not count:

- static frontend fixture only
- screenshot package only
- docs-only model spec
- mock explanation card only
- hardcoded report sample only
- manual screenshots
- prewritten B-end report page
- public event page with no generated run
- Strategy Lab planned-only block
- request/support mock page

These are useful demo and QA surfaces, but they are not a run lifecycle.

## E. What Is Not Required Yet

Minimum real-run does not require:

- live crawler
- full-web or full-platform collection
- real Douyin API
- real Bilibili API
- real Weibo API
- real Reddit API
- vendor API adapter
- real LLM
- production multi-user system
- public deployment
- payment or sponsorship
- production B-end report runtime
- generated response text
- `auto_execute`
- publish / send / post actions
- historical calibration
- causal proof or prediction validation

## F. Recommended Path

Recommended sequence:

1. Docs-only minimum real-run contract.
2. Backend-only contract, schema, and test design for calculator run output.
3. Backend pure-local run generator from safe sample or package fixture.
4. Gated frontend integration behind clear "local generated run" labels.
5. Screenshot smoke.
6. Manual playtest and recording only after the generated-run loop passes.

This path keeps the demo honest: first prove a bounded local run lifecycle, then invite external users to react to it.

## G. Stop Conditions

Stop if any task attempts:

- real API or real LLM use
- collector run
- real exchange directory read without explicit approval
- `evidence_items` parsing without a design checkpoint
- production Evidence write
- production case creation
- production `analysis_run`
- B-end report runtime
- Sandbox/public event runtime generation
- generated response text
- `auto_execute`
- publish / send / post actions
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

The stop condition applies even if the implementation appears technically simple.

## H. Current Decision

`manual_playtest_status = deferred_until_minimum_real_run`

`recording_status = deferred_until_minimum_real_run`

`next_state = ready_for_minimum_real_run_contract_design`

Recommended next task:

Create the minimum real-run contract design before any manual playtest, recording, frontend API integration, Strategy Lab runtime, or production report runtime work.

