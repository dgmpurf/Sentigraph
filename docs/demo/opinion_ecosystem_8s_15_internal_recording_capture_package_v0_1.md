# Opinion Ecosystem 8S-15 Internal Recording Capture Package v0.1

## A. Decision / Status

```text
phase = 8S-15
task = internal_recording_capture_scope_package_docs_only
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
recording_capture_package_created = yes
three_minute_script_created = yes
eight_minute_script_created = yes
pre_recording_checklist_created = yes
recording_review_form_created = yes
actual_recording_approved_now = no
trusted_playtest_approved_now = no
public_release_approved_now = no
future_actual_recording_requires_explicit_approval = yes
future_actual_recording_phase = 8S-16_internal_recording_capture_execution
exact_future_approval_phrase = 批准 8S-16 internal recording capture execution
recommended_next_state = ready_to_request_explicit_8S_16_internal_recording_capture_execution_or_pause
```

Decision: ready

## B. Inputs From 8S-14

- 8S-14 chose internal recording capture scope first.
- Trusted playtest is deferred until internal recording review.
- Public release remains blocked.
- 8S-14 route freeze defined primary Dong/Sun route, secondary Helldivers route, and optional routes.
- 8S-14 did not execute recording, screenshot capture, media generation, playtest, or external contact.

## C. Recording Package Purpose

8S-15 prepares the internal recording package only.

It is not actual recording. It is not screenshot capture. It is not public demo publication. It is not trusted playtest.

This package exists so a future 8S-16 capture can be executed with a stable route, a precise script, clear stop conditions, and a review form.

## D. Primary 3-minute Recording Script

### 0:00-0:20 Opening and Boundary

Say:

- This is a local demo.
- It uses selected sample only.
- It is not full-web coverage.
- It is not full-platform coverage.
- It is not official verification.
- It is not causal proof.
- It is not prediction.

### 0:20-0:45 Demo Homepage and Public Events

Click:

- `/#/demo`
- enter public events through the guided demo flow
- `/#/public-events`

Say:

- This path shows how a user reaches a public event page.
- The event list is a demo surface, not a live platform-wide crawler.

### 0:45-1:15 Dong/Sun Public Event Detail

Click:

- `/#/public-events/donglu-sunjihai-youth-football`

Say:

- This page is a selected public sample event view.
- It is not full-thread coverage and not official verification.
- It is meant to help explain an event, not prove final truth.

### 1:15-2:10 Dong/Sun Opinion Ecosystem Sandbox and Generated-run Click

Click:

- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- explicit generated-run button inside Opinion Ecosystem Sandbox

Say:

- Generated run is local fixture output.
- It does not call a real API or real LLM.
- It does not execute a platform action.

### 2:10-2:40 PeopleCluster / Generated Run / Selected Sample Explanation

Point to:

- PeopleCluster
- module cards
- boundary labels

Say:

- PeopleCluster is an anonymous aggregate proxy.
- It does not represent real individual users.
- The generated run should be treated as a local analytical fixture, not a production score.

### 2:40-3:00 Dong/Sun B-end Report Sample and Closing Boundary

Click:

- `/#/reports/donglu-sunjihai-youth-football-sample`

Say:

- This is a sample report page, not a production report.
- No automatic public response is generated.
- No automatic platform action is executed.

## E. Expanded 8-minute Recording Script

### 0:00-0:45 Opening Boundary

State that this is a local demo using selected samples. It is not full-web, not full-platform, not official verification, not causal proof, not prediction, and not a production score.

### 0:45-1:45 C-end Demo Route

Open `/#/demo` and walk through the guided route into `/#/public-events`. Explain that this is a demo path for event discovery and orientation, not live crawling.

### 1:45-2:45 Dong/Sun Public Event Detail

Open `/#/public-events/donglu-sunjihai-youth-football`. Explain the event summary, boundary copy, and why selected sample context is shown before analysis.

### 2:45-4:30 Dong/Sun Sandbox Generated-run Explanation

Open `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` and trigger the generated run. Explain that generated run is local fixture output and no real API, LLM, collector, or platform action is executed.

### 4:30-5:45 Module Card Explanation

Explain module cards as local explanatory analysis surfaces. Keep claims conservative:

- PeopleCluster = anonymous aggregate proxy
- ResponseStrategyComparison = human-review-only
- no automatic public response
- no target-user list
- no persuasion score
- no official verification

### 5:45-6:45 Boundary Labels Explanation

Call out labels for selected sample, not full-web, not full-platform, not full-thread, not official verification, not prediction, and not causal proof.

### 6:45-7:30 B-end Report Sample

Open `/#/reports/donglu-sunjihai-youth-football-sample`. Explain it as a sample reviewer/report surface, not a production customer report.

### 7:30-8:00 Optional Comparison and Closing

If stable, briefly show Helldivers comparison through `/#/opinion-ecosystem` or `/#/public-events/helldivers-psn`. If not, close with what is implemented vs not implemented:

- implemented: local demo route, generated-run display, selected sample explanation, B-end report sample
- not implemented: public beta, live crawler, real platform APIs, real LLM, automatic response generation, production report runtime

Optional route `/#/public-events/request` may be shown only if stable and clearly described as request/private analysis flow. Optional route `/#/analysis-requests` may be shown only if backend is running and no visible 500 appears.

## F. Frozen Routes

Primary:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- explicit generated-run click inside Opinion Ecosystem Sandbox
- `/#/public-events/request`
- `/#/reports/donglu-sunjihai-youth-football-sample`

Secondary:

- `/#/opinion-ecosystem`
- explicit generated-run click for default / Helldivers sample
- `/#/public-events/helldivers-psn`
- `/#/reports/helldivers-psn-sample`

Optional:

- `/#/external-collector` only if explaining local package source boundary
- `/#/analysis-requests` only if backend is running and no visible 500 appears

## G. Recording Stop Conditions

Stop if:

- visible 500
- ErrorBoundary
- page crash
- undefined / NaN / `[object Object]`
- generated-run click fails
- console error/warn appears during checked route
- secret appears
- private path appears
- raw author identifier appears
- publish/send/post/execute CTA appears
- generated response text appears
- page makes user think this is live crawling
- page makes user think this is official verification
- page makes user think this is full-web/full-platform coverage

## H. Future Approval Protocol

Actual recording is not approved in 8S-15.

Future actual recording requires exact approval phrase:

`批准 8S-16 internal recording capture execution`

Do not treat the following as approval:

- 下一步
- 继续
- 好
- git clean
- Codex says ready
- commit 完成

## I. Files Changed

- `docs/demo/opinion_ecosystem_8s_15_internal_recording_capture_package_v0_1.md`
- `docs/demo/opinion_ecosystem_8s_15_pre_recording_safety_checklist_v0_1.md`
- `docs/demo/opinion_ecosystem_8s_15_recording_review_form_v0_1.md`

## J. Validation

Run:

```text
git diff --check
git status --short
```

Also run textual scan on three docs for placeholder markers and trailing whitespace.

Do not run backend tests, frontend build, browser smoke, collector, screenshot capture, or recording because this is docs-only.

Validation result for this phase:

```text
git diff --check = passed
git status --short = three untracked docs-only files
placeholder/trailing whitespace scan = passed
decision field scan = passed
```

## K. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Package Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- No actual recording is executed.
- No screenshots are captured.
- No media is generated.
- No trusted playtest is executed.

These limitations are intentional.

### P3 Nice-to-have

- Ask for exact 8S-16 approval if actual recording should proceed.
- Pause if the user wants more route or copy review before capture.

## L. Source Update Policy

No immediate Project Source update unless user requests a small patch later.

Do not create Source files in repo. Do not create `docs/project_sources`.

## M. Safety Confirmations

- no backend code changed
- no frontend code changed
- no tests changed
- no runtime code changed
- no backend route added
- no frontend UI added
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
