# Opinion Ecosystem Frontend Generated-run API Integration First Slice Plan v0.1

## A. Purpose

This document plans the smallest safe frontend integration with the 8S-4 backend generated-run route:

```text
POST /api/v1/opinion-ecosystem/generated-runs/local-fixture
```

The integration should let a local operator explicitly request a backend local fixture generated run from the Opinion Ecosystem Sandbox, while preserving static fallback UI and all safety boundaries.

## B. Allowed Future Changed Files For 8S-6

Likely future changed files:

- `frontend/src/api/sentigraphApi.js`
- `frontend/src/pages/OpinionEcosystemSandbox.jsx`
- optional `frontend/src/components/opinion/OpinionEcosystemGeneratedRunPanel.jsx`
- optional `frontend/src/styles/global.css`

8S-6 should avoid backend code changes unless an existing route-contract bug is found and the user approves a blocker fix. It should avoid tests/package/runtime/Project Source changes unless the explicit 8S-6 prompt allows them.

## C. Preferred Frontend Behavior

Future UI should:

- keep the existing static/local explanatory UI
- add a clearly labeled generated-run section
- make it clear that the generated run is a backend local fixture run
- require an explicit click/action to request a generated run
- map current sample to `sample_key`
- show `run_id`, `run_schema`, `run_status`, and `generated_at`
- show `model_version`, `coefficient_source`, `calibration_status`, and `empirical_validation`
- show selected-sample / not-full-web / not-official-verification / not-causal-proof / not-prediction labels
- show warnings and blockers
- show `ContentAggregate`, `InfluenceCore`, `EchoBox`, `PeopleCluster`, and `ResponseStrategyComparisonV01` module cards

Recommended sample mapping:

| Current frontend mode | Route `sample_key` |
| --- | --- |
| default / Helldivers | `helldivers_psn` |
| `donglu-sunjihai-youth-football` query sample | `donglu_sunjihai_youth_football` |

The generated-run action should not run automatically on page load in the first slice. The static explanation should remain visible before and after a generated-run request.

## D. Error And Blocked State Rules

If the route returns 4xx, `blocked`, or `manual_review_required`:

- do not present it as a normal score
- show blockers first
- keep static fallback visible
- do not hide boundary warnings
- do not show publish/send/post/execute CTA
- do not show generated public response text
- do not backfill missing module scores with fake values

Blocked and manual-review states are valid product governance states, not generic UI failures.

Recommended UI states:

| State | Expected behavior |
| --- | --- |
| idle | show static explanation and a local generated-run action |
| loading | show a small loading state without hiding static fallback |
| success | show metadata, boundary flags, warnings/blockers, module cards |
| blocked/manual review | show blockers before any module values |
| route error | show safe error message and keep static fallback visible |

## E. Safety And Copy Requirements

UI copy must clearly say:

- generated run is backend local fixture run
- selected sample only
- not full-web / not full-platform / not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- no generated public response
- no auto execution

The UI must continue to distinguish:

- static/local explanation snapshot
- backend generated-run local fixture output
- blocked/manual-review run
- unavailable generated run

The UI must not expose raw author identifiers, private collector paths, exchange dirs, `evidence_items` file paths, cookies, tokens, sessions, secrets, or absolute private filesystem paths.

## F. Deferred

Explicitly deferred:

- automatic run on page load if risky
- runtime persistence
- generated run history
- GET generated run route
- real package parsing
- private collector / exchange dirs
- Evidence Layer write
- production case / `analysis_run`
- B-end report runtime
- Sandbox/public event runtime
- Strategy Lab runtime
- manual playtest / recording
- response_text
- generated_public_message
- auto_execute
- publish/send/post/execute
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

Deferred means not implemented, not implied, and not exposed through hidden UI behavior.

## G. Future 8S-6 Validation Plan

Future implementation should run:

```text
npm.cmd --prefix frontend run build
python -m pytest backend/app/tests/test_opinion_ecosystem_generated_run_routes.py
python -m pytest backend/app/tests/test_opinion_ecosystem_minimum_real_run.py
python -m pytest backend/app/tests/test_opinion_ecosystem_mock_calculator.py
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
git diff --check
```

Future browser smoke should cover:

- `/#/opinion-ecosystem`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

Smoke expectations:

- static fallback is visible before generated-run action
- local generated-run action is explicit
- generated-run panel renders metadata, boundaries, warnings/blockers, and module cards
- Dong/Sun query route maps to `donglu_sunjihai_youth_football`
- no visible `undefined`
- no visible `NaN`
- no visible `[object Object]`
- no visible 500 prompt
- no visible ErrorBoundary
- no publish/send/post/execute CTA
- no raw author identifiers
- no generated public response text

Do not require full backend pytest for the first tiny frontend slice unless code touch is broader than expected.
