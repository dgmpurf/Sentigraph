# Phase 8S-10 Rehearsal / Playtest Execution Decision Checkpoint v0.1

## A. Decision

```text
phase = 8S-10
decision = rehearsal_or_trusted_playtest_execution_decision
current_state = ready_for_8S_10_internal_recording_rehearsal_dry_run_or_one_trusted_manual_playtest_execution_decision
selected_path = internal_recording_rehearsal_dry_run_first
trusted_manual_playtest_status = deferred_until_internal_rehearsal_review
recording_rehearsal_status = approved_for_internal_dry_run_preparation_only
actual_recording_status = not_executed
actual_playtest_status = not_executed
next_state_if_ready = ready_for_8S_11_internal_recording_rehearsal_dry_run_execution_with_operator_approval
```

This checkpoint chooses the safer next path: run an internal operator dry run before showing the demo to a trusted external tester. It does not execute the dry run, contact users, record video, generate media, run browser smoke, or modify product behavior.

## B. Evidence Reviewed

- 8S-7 completed generated-run browser QA, copy polish, and screenshot smoke.
- 8S-7 confirmed default `/#/opinion-ecosystem` and Dong/Sun `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` generated-run browser QA passed.
- 8S-7 confirmed before click: `0` generated-run API calls; after explicit click: `1` local fixture generated-run call per route.
- 8S-7 confirmed generated-run metadata, boundary labels, warnings/blockers, and module outputs were visible.
- 8S-8 approved limited manual playtest preparation and internal recording rehearsal preparation.
- 8S-9 created a rehearsal/playtest execution package with preflight, scripts, trusted tester prompts, observer sheet, and feedback triage.
- The local generated-run route and frontend panel already exist.
- Default and Dong/Sun generated-run browser QA previously passed.

## C. Decision Rationale

Internal recording rehearsal dry run comes before trusted manual playtest because it has lower risk and catches operator-side issues first:

- lower privacy risk
- no external misunderstanding risk
- validates screen hygiene
- validates route pacing
- validates generated-run click
- validates boundary explanation
- validates stop conditions
- lets the operator fix P0/P1 issues before showing another person

This sequence keeps the demo honest: first verify the operator can complete the route and explain boundaries clearly, then decide whether one trusted manual playtest is appropriate.

## D. Approved Scope For Next Phase

8S-11 may prepare and execute only:

- internal operator dry run
- local browser route walk-through
- optional local screen recording rehearsal if the operator explicitly chooses
- route timing notes
- operator self-observation notes
- stop-condition check
- post-run triage document

Any 8S-11 execution must still be local, controlled, and explicitly approved by the user/operator before it starts.

## E. Still Not Allowed

The following remain blocked:

- public launch
- public beta
- external mass testing
- trusted tester session without operator approval after internal rehearsal
- real API
- real LLM
- collector/private collector access
- real package row parsing
- `evidence_items.jsonl` / `evidence_items.csv` parsing
- real exchange dir read
- Evidence Layer write
- production case
- production `analysis_run`
- B-end report runtime
- Sandbox/public event runtime
- generated public response
- Strategy Lab runtime
- publish / send / post / execute behavior
- `auto_execute`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

These items may appear only as forbidden-language, boundary, stop-condition, decision, or triage text. They must not become active capabilities.

## F. Required Preconditions For 8S-11

8S-11 can start only if the user explicitly approves an internal dry run.

Before 8S-11:

- repo clean
- backend can start
- frontend can start
- operator confirms no secrets visible
- operator confirms no private browser profile visible
- operator confirms no private collector path visible
- operator confirms no `.env` / API keys / tokens / cookies / sessions visible
- selected primary route is Dong/Sun
- stop conditions are available

## G. Stop Conditions

Stop if:

- backend/frontend crashes
- visible 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`
- generated-run click fails on primary route
- publish / send / post / execute CTA appears
- generated public response text appears
- raw author identifiers appear
- secrets or `.env` or tokens or cookies are visible
- private collector path appears
- operator feels the demo implies live crawling / official truth / production score

## H. Source Recommendation

After the 8S-10 commit:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request / Provider / Import Governance behavior changes.
