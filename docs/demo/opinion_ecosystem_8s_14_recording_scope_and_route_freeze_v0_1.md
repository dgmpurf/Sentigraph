# Opinion Ecosystem 8S-14 Recording Scope and Route Freeze v0.1

## A. Purpose

This is a docs-only route freeze and recording scope plan.

No recording is executed in this phase.

## B. Frozen Recording Route

Primary C-end route:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- explicit generated-run click inside Opinion Ecosystem Sandbox
- `/#/public-events/request`
- `/#/reports/donglu-sunjihai-youth-football-sample`

Secondary route:

- `/#/opinion-ecosystem`
- explicit generated-run click for default / Helldivers sample
- `/#/public-events/helldivers-psn`
- `/#/reports/helldivers-psn-sample`

Optional route:

- `/#/external-collector` only if explaining local package source boundary
- `/#/analysis-requests` only if backend is running and no visible 500 appears

## C. 3-minute Recording Scope

Compact story:

1. Open `/#/demo`.
2. Enter public events.
3. Open the Dong Lu / Sun Jihai public event.
4. Enter the Dong/Sun Opinion Ecosystem Sandbox through `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`.
5. Trigger the generated run.
6. Explain boundary labels and the PeopleCluster anonymous aggregate proxy.
7. Open the Dong/Sun B-end report sample.
8. Close with boundaries:
   - selected sample only
   - not full-web coverage
   - not full-platform coverage
   - not official verification
   - not causal proof
   - no automatic platform action

## D. 8-minute Recording Scope

Expanded story:

1. Include the C-end path through `/#/demo`, Event Plaza, and Dong/Sun event detail.
2. Include generated-run explanation inside Opinion Ecosystem Sandbox.
3. Explain what module cards show and what they do not prove.
4. Explain the B-end reviewer report path through `/#/reports/donglu-sunjihai-youth-football-sample`.
5. Optionally compare with Helldivers via `/#/opinion-ecosystem` and `/#/public-events/helldivers-psn`.
6. Include `/#/public-events/request` only if stable and clearly described as request/mock flow.
7. Include `/#/analysis-requests` only if backend is running and no visible 500 appears.

## E. Pre-recording Safety Check

Confirm before recording:

- backend running if backend-dependent pages are shown
- frontend running
- generated run click succeeds
- no visible 500
- no console error/warn
- no undefined / NaN / `[object Object]`
- no secrets
- no private paths
- no raw author identifiers
- no publish/send/post/execute CTA
- no generated response text

## F. Boundary Talking Points

Say clearly:

- this is a local demo
- this uses selected sample only
- this is not full web
- this is not full platform
- this is not full thread
- this is not official verification
- this is not causal proof
- this is not prediction
- this is not a production score
- generated run is local fixture output
- PeopleCluster is anonymous aggregate proxy
- ResponseStrategyComparison is human-review-only
- no automatic public response is generated
- no platform action is executed

## G. Stop Conditions

Stop recording if:

- page crashes
- visible 500 appears
- ErrorBoundary appears
- undefined / NaN / `[object Object]` appears
- generated-run click fails
- any secret or private path appears
- raw author identifier appears
- publish/send/post/execute CTA appears
- user could reasonably think this is live crawling or official verification
