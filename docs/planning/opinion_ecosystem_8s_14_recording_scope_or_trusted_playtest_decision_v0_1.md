# Opinion Ecosystem 8S-14 Recording Scope or Trusted Playtest Decision v0.1

## A. Decision / Status

phase = 8S-14
task = recording_scope_or_trusted_playtest_decision_after_full_stack_gate
selected_path = internal_qa_capture_first
recording_capture = not_executed
trusted_manual_playtest = deferred
public_recording = blocked
external_distribution = blocked
source_update_after_commit = no_batch_later

next_state_if_ready = ready_for_8S_15_internal_qa_capture_execution_with_operator_approval

## B. Why This Path

8S-13 full-stack gate passed after backend targeted tests, frontend build, backend runtime smoke, browser route smoke, and Dong/Sun generated-run UI verification.

Internal QA capture is now safer than it was before the backend and full-stack gates because the local generated-run route, Dong/Sun route context, report sample route, and Analysis Requests governance route have all been checked together.

Internal QA capture is not a public demo video. It is a local operator self-check used to review route pacing, visible boundary language, screen hygiene, and whether the flow is safe enough to show to another person later.

Trusted manual playtest should wait until the internal capture is reviewed for clarity, safety, route stability, and boundary wording.

Public or external recording remains blocked until a separate approval explicitly authorizes capture, review, packaging, and distribution.

## C. Internal QA Capture Scope

Allowed future 8S-15 scope:

- local-only recording by the operator
- no external users
- no publishing
- no screenshots unless separately approved
- no secrets, `.env` values, API keys, tokens, cookies, sessions, browser profile paths, or private collector paths visible
- no raw author identifiers visible
- no real APIs, real LLMs, or collector jobs
- no public delivery
- no generated public response
- no publish/send/post/execute behavior

The future capture should remain an internal safety and clarity rehearsal. It must not be treated as a public demo release, customer proof, official verification, or production simulation.

## D. Proposed 8S-15 Route Script

Use the proven full-stack route:

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. Explicitly click `Load backend local generated run` once.
6. Confirm generated-run metadata, boundary labels, and module outputs.
7. `/#/reports/donglu-sunjihai-youth-football-sample`
8. Optional: `/#/analysis-requests` only if backend is running and the route is clean.

The operator should narrate that this is a selected local sample, not full-web coverage, not full-platform coverage, not official verification, not causal proof, and not a production score.

## E. Capture-safe Checklist

Before recording:

- browser has no devtools open
- no terminal with `.env` or commands showing secrets
- no filesystem path panels showing private collector path
- no API keys, tokens, cookies, or sessions visible
- no personal documents visible
- backend and frontend already running or started cleanly
- page zoom and window size set before recording

Stop immediately if any of these appear:

- visible 500
- ErrorBoundary
- `undefined`
- `NaN`
- `[object Object]`
- Dong/Sun falls back to Helldivers
- generated-run click fails
- public action CTA appears
- generated public response text appears
- secrets appear
- raw identifiers appear

## F. Trusted Manual Playtest Deferral

trusted_manual_playtest_status = deferred_until_internal_qa_capture_review

A trusted manual playtest should only happen after the internal capture is reviewed for clarity, safety, route stability, and boundary wording. The internal capture should answer whether a new viewer can understand:

- what the selected sample is
- why the generated run is local and fixture-backed
- why the output requires human review
- why the sandbox does not prove full-web truth, official verification, prediction, or causality
- why no public response, platform action, or delivery action is generated

## G. Source Update Policy

No immediate Project Source update after this 8S-14 docs-only decision.

Batch Source update later only if:

- internal QA capture is actually completed and reviewed
- trusted manual playtest is completed
- public/external demo package is produced
- code/runtime/API/route/schema/safety boundary changes
- Project Source and repo state diverge

## H. Validation

Validation for this docs-only phase:

- `git diff --check`
- `git status --short`

Backend tests, frontend build, browser smoke, screenshots, and recording are intentionally not required because this phase does not change code or UI behavior.

## I. Safety Confirmations

- docs-only
- no code changed
- no recording captured
- no screenshots captured
- no trusted manual playtest executed
- no Project Source changed
- no collector/private collector accessed
- no real APIs called
- no real LLM called
- no URL fetching/scraping
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no generated public response
- no publish/send/post/execute
- no secrets read or printed
- no GitHub Actions workflow recreated

