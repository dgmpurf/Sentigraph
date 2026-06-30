# Opinion Ecosystem 8S-14 Recording Scope / Trusted Playtest Decision After Full-stack Gate v0.1

## A. Decision / Status

```text
phase = 8S-14
task = recording_scope_trusted_playtest_decision_after_full_stack_gate
privacy_issue_stop = no
docs_only = yes
code_changed = no
tests_changed = no
runtime_code_changed = no
frontend_changed = no
backend_changed = no
collector_run = no
real_api_called = no
real_llm_called = no
real_exchange_dir_read = no
evidence_items_parsed = no
evidence_layer_write = no
production_case_created = no
production_analysis_run_created = no
recording_executed = no
screenshots_captured = no
media_generated = no
trusted_playtest_executed = no
external_users_contacted = no
public_beta_started = no
project_source_changed = no
project_source_files_created_in_repo = no
```

Decision fields:

```text
full_stack_readiness_gate_passed = yes
recording_scope_decision_created = yes
trusted_playtest_decision_created = yes
recommended_first_action = internal_recording_capture_scope_first
trusted_playtest_status = deferred_until_internal_recording_review
public_release_status = blocked
recommended_next_state = ready_for_8S_15_internal_recording_capture_scope_package_docs_only_or_pause
```

Decision: ready

## B. Inputs

- 8S-7 generated-run browser QA / screenshot smoke passed earlier.
- 8S-8 approved limited trusted manual playtest preparation and internal recording rehearsal preparation.
- 8S-9 created limited playtest / recording rehearsal package.
- 8S-10 selected internal recording rehearsal dry run first.
- 8S-11 internal recording rehearsal dry run passed.
- 8S-12 backend runtime readiness gate passed.
- 8S-13 full-stack runtime readiness gate passed.
- Actual recording capture has not been executed.
- Trusted playtest has not been executed.
- 8T route/env gate helper line is paused after Source patch.

## C. Decision Comparison

| Option | Allowed now? | Risk level | Prerequisites | Expected benefit | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Internal recording capture scope first | yes, as planning only | low | route freeze, safety checklist, local-only capture scope | produces a reviewable artifact before external feedback | recommended |
| Trusted manual playtest first | not recommended now | medium | internal recording reviewed, obvious demo confusion fixed, observer script ready | gets early outside comprehension feedback | defer unless user explicitly insists |
| Both in parallel | no | medium/high | mature script, reviewed recording, trusted tester logistics | saves calendar time but increases confusion and coordination risk | not recommended |
| Pause | yes | low | none | avoids premature external exposure | acceptable |

Expected conclusion:

```text
internal_recording_capture_scope_first = recommended
trusted_playtest_first = deferred_until_internal_recording_review_or_explicit_user_insistence
both_in_parallel = not_recommended
pause = allowed
```

## D. Recommended Route Freeze

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

## E. Recording Scope Recommendation

Recommended:

- one short 3-minute internal capture
- one longer 8-minute internal capture only after the 3-minute capture is reviewed
- no public upload
- no external sharing before human review
- no secrets on screen
- no `.env`, API keys, tokens, cookies, or browser profile paths
- no private collector paths
- no raw author identifiers

## F. Trusted Playtest Entry Criteria

Trusted playtest should require:

- internal recording reviewed
- no visible 500 / ErrorBoundary / undefined / NaN / `[object Object]`
- generated-run click works
- boundary labels visible
- no publish/send/post/execute CTA
- no generated response text
- no raw author identifiers
- no secrets
- clear explanation that generated run is local fixture output
- clear explanation that PeopleCluster is anonymous aggregate proxy
- clear explanation that this is not full-web/full-platform coverage

## G. Explicit Non-goals

- no actual recording in this phase
- no actual playtest in this phase
- no external user contact
- no public release
- no public beta
- no real platform API
- no real LLM
- no collector run
- no evidence_items parsing
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime generation
- no generated response text
- no publish/send/post/execute
- no UI/auth/storage/import/evidence preview work

## H. Files Changed

- `docs/planning/opinion_ecosystem_8s_14_recording_scope_trusted_playtest_decision_after_full_stack_gate_v0_1.md`
- `docs/demo/opinion_ecosystem_8s_14_recording_scope_and_route_freeze_v0_1.md`
- `docs/playtest/opinion_ecosystem_8s_14_trusted_playtest_entry_criteria_v0_1.md`

## I. Validation

Run:

```text
git diff --check
git status --short
```

Also run a simple textual scan on the three docs for placeholder markers and trailing whitespace.

Do not run backend tests, frontend build, browser smoke, collector, or recording because this is docs-only.

Validation result for this phase:

```text
git diff --check = passed
git status --short = three untracked docs-only files
placeholder/trailing whitespace scan = passed
decision field scan = passed
```

## J. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Decision Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- No actual recording is executed in this phase.
- No trusted playtest is executed in this phase.
- No Source patch is produced in this phase.

These limitations are intentional.

### P3 Nice-to-have

- Prepare 8S-15 internal recording capture scope package docs-only if the user approves.
- Pause before involving trusted external playtesters.

## K. Source Update Policy

No immediate Project Source update unless the user requests another small patch.

Do not create Source files in repo. Do not create `docs/project_sources`.

## L. Safety Confirmations

- no backend code changed
- no frontend code changed
- no tests changed
- no runtime code changed
- no backend route added
- no frontend UI added
- no route behavior changed
- no recording executed
- no screenshots captured
- no media generated
- no trusted playtest executed
- no external users contacted
- no public beta started
- no accounts created
- no analytics added
- no payment or sponsor flow added
- no collector run
- no private collector access
- no real exchange dirs read
- no real API called
- no real LLM called
- no URL fetching
- no scraping
- no `evidence_items.jsonl` parsed or opened
- no `evidence_items.csv` parsed or opened
- no Evidence Layer write
- no production case created
- no production analysis_run created
- no B-end report runtime generated
- no Sandbox/public event runtime generated
- no response_text or generated_public_message generated
- no publish / send / post / execute behavior implemented
- no target_user_list, persuasion_score, truth_score, official_verified, prediction_probability, psychological_profile, or personality_diagnosis exposed
- no Project Source files created in repo
- no `docs/project_sources` created
- no GitHub Actions workflow recreated
