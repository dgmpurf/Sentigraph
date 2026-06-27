# Phase 8S-9 Limited Manual Playtest and Recording Rehearsal Package

## Package Purpose

This package prepares Sentigraph / Opinion Ecosystem for a limited trusted manual playtest and an internal recording rehearsal.

Current phase: `8S-9`

Current state: `ready_for_8S_9_limited_manual_playtest_and_recording_rehearsal_package`

This package does not execute playtest, does not contact users, does not record video, does not generate media, and does not authorize public launch.

## What This Package Is

- A local operator runbook.
- A 3-minute internal recording rehearsal script.
- An 8-minute internal recording rehearsal script.
- A trusted manual playtest script.
- An observer note template.
- A post-run feedback triage guide.
- A boundary reminder for selected-sample generated-run demos.

## What This Package Is Not

- Not a public launch package.
- Not a public beta package.
- Not a production deployment package.
- Not an external mass user testing package.
- Not a media output package.
- Not a real API, real LLM, crawler, collector, Evidence Layer, production case, production `analysis_run`, report runtime, or Sandbox/public event runtime implementation.

## File List

1. `README.md`
2. `operator_preflight_runbook.md`
3. `internal_recording_rehearsal_3min_script.md`
4. `internal_recording_rehearsal_8min_script.md`
5. `trusted_manual_playtest_script.md`
6. `observer_note_sheet.md`
7. `post_run_feedback_triage.md`

## Recommended Usage Order

1. Read this README.
2. Run `operator_preflight_runbook.md`.
3. Choose one path:
   - internal 3-minute recording rehearsal
   - internal 8-minute recording rehearsal
   - one trusted manual playtest
4. Use `observer_note_sheet.md` during the run.
5. Use `post_run_feedback_triage.md` after the run.

## Approved Route Scope

Primary route:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- explicit generated-run click inside Opinion Ecosystem Sandbox
- `/#/public-events/request`
- `/#/reports/donglu-sunjihai-youth-football-sample`

Secondary route:

- `/#/opinion-ecosystem`
- explicit generated-run click for Helldivers/default sample
- `/#/public-events/helldivers-psn`
- `/#/reports/helldivers-psn-sample`

Optional route:

- `/#/external-collector` only if explaining local package source boundaries.
- `/#/analysis-requests` only if the backend is running and there is no visible 500.

## Required Boundary Language

Use this wording consistently:

- This is a local demo.
- It is selected sample only.
- It is not full-web coverage.
- It is not full-platform coverage.
- It is not full-thread coverage.
- It is not official verification.
- It is not causal proof.
- It is not prediction.
- It is not a production score.
- The generated run is local fixture output.
- PeopleCluster is an anonymous aggregate group / behavioral proxy, not a real person.
- InfluenceCore is a content / narrative / official / media / meme core, not a people ball.
- ResponseStrategyComparison is human-review-only.
- There is no generated public response.
- There is no auto execution.
- There is no publish / send / post / execute action.

## Stop-condition Summary

Stop immediately if:

- a user cannot be corrected about live crawling, full-web coverage, or official truth
- a visible 500, ErrorBoundary, `undefined`, `NaN`, or `[object Object]` appears on the primary route
- a publish / send / post / execute CTA appears
- generated public response text appears
- raw author identifiers appear
- secrets, `.env`, API keys, tokens, cookies, sessions, or browser profile paths are visible
- the backend or frontend crashes
- private collector paths or real exchange dirs appear

## Final Note

This package prepares the operator. It does not execute playtest or recording.
