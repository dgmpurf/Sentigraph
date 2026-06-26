# Opinion Ecosystem Frontend Generated-run Display Contract v0.1

## A. Purpose

This document defines how the future Opinion Ecosystem frontend should display a generated run output from the backend minimum real-run wrapper.

The display contract exists to prevent the UI from treating generated local sample output as production truth, full-web coverage, official verification, prediction, or a response-execution system.

## B. Current State

The current Opinion Ecosystem UI is still a static/local explanatory UI.

It does not call a backend generated-run API.

Phase 8S-2 added a backend-only pure-local generated run wrapper:

```text
backend/app/services/opinion_ecosystem_minimum_real_run.py
```

That wrapper is not exposed to the frontend. There is no route, no frontend integration, no runtime persistence, and no generated-run display state in the current UI.

Current frontend files reviewed for this checkpoint:

```text
frontend/src/pages/OpinionEcosystemSandbox.jsx
frontend/src/components/opinion/OpinionEcosystemModelExplanation.jsx
frontend/src/data/opinionEcosystemCalculatorOutputFixture.js
```

These files remain static/local explanation surfaces until a later route/API and frontend integration phase explicitly changes them.

## C. Required Visible Generated-run Metadata

Future frontend display must show:

- `run_id`
- `run_schema`
- `run_status`
- `case_id` or `sample_id`
- `input_package_id` if present
- `input_source_kind`
- `input_scope_note`
- `generated_at`
- `model_version`
- `coefficient_source`
- `calibration_status`
- `empirical_validation`
- `human_review_required`

Recommended display behavior:

- show `run_schema` close to the generated-run status, so reviewers know which contract is being displayed
- show `input_source_kind` and `input_scope_note` before module scores
- show `coefficient_source`, `calibration_status`, and `empirical_validation` as visible tags
- show `human_review_required` as a persistent visible boundary, not only in a tooltip

## D. Required Visible Boundary Labels

Future frontend display must clearly show:

- selected sample only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- no auto execution
- no generated public response

These labels must remain visible for ready, blocked, and manual-review runs.

## E. Required Module Rendering

Future generated-run UI must render these module envelopes:

- `ContentAggregate`
- `InfluenceCore`
- `EchoBox`
- `PeopleCluster`
- `ResponseStrategyComparisonV01`

Each module card must show:

- score/value fields only when present
- warnings
- blockers
- confidence/calibration labels
- plain-language explanation
- boundary reminder

Module-specific guidance:

| Module | Rendering expectation |
| --- | --- |
| `ContentAggregate` | Explain selected-sample heat, evidence confidence, review risk, duplicate folding, and rejected evidence exclusion without calling it real platform heat. |
| `InfluenceCore` | Explain content, narrative, official, media, or meme cores; do not render them as people or account nodes. |
| `EchoBox` | Explain selected-sample discussion container structure; do not call it a complete social graph. |
| `PeopleCluster` | Explain anonymous aggregate clusters; do not imply real individual users, targeting, profiling, or psychological diagnosis. |
| `ResponseStrategyComparisonV01` | Show human-review-only comparison, blockers before scores, no generated response copy, and no publish/send/post/execute controls. |

If a module output is missing, empty, blocked, or not calculated, the UI should show a gated/empty state with the reason. It must not backfill fake scores.

## F. Blocked / Manual-review Rendering

If `run_status` is `blocked`, `manual_review_required`, or `not_ready`:

- do not render the result as a normal score
- show blockers first
- keep all module outputs visibly gated
- do not hide warnings
- do not provide publish/send/post/execute CTA
- keep boundary labels visible
- keep `human_review_required` visible
- keep `runtime_side_effects` available for reviewer inspection

Blocked and manual-review states are product states, not UI errors.

## G. Static Fallback Behavior

If no generated run is available:

- keep the static/local explanatory UI
- label it as a static explanation snapshot
- do not imply backend generated run
- do not imply production score
- do not imply current backend connectivity
- do not imply the displayed sample is a generated runtime result

Recommended fallback label:

```text
Static/local explanation snapshot. No backend generated run is loaded.
```

## H. Forbidden Frontend Behavior

Future frontend must not:

- show `response_text`
- show `generated_public_message`
- show `target_user_list`
- show `persuasion_score`
- show `truth_score`
- show `official_verified`
- show `prediction_probability`
- show `psychological_profile`
- show `personality_diagnosis`
- show publish/send/post/execute CTA
- show `auto_execute` as active capability
- show full-web/full-platform claims

The frontend may show these strings only in forbidden-field warnings, boundary documentation, or stop-condition text. It must not render them as available product capabilities.
