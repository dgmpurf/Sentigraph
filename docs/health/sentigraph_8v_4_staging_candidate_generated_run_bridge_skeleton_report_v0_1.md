# Sentigraph 8V-4 Staging Candidate Generated-run Bridge Skeleton Report v0.1

## A. Decision / Status

phase = 8V-4

task = controlled_staging_candidate_to_minimum_real_run_bridge_smoke_test_first_skeleton

decision = ready

privacy_issue_stop = no

backend_only = yes

test_first = yes

metadata_only = yes

backend_code_changed = yes

frontend_code_changed = no

tests_changed = yes

route_changed = no

api_route_added = no

runtime_changed = no

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

private_collector_inspected = no

real_exchange_dir_read = no

evidence_rows_parsed = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

minimum_real_run_executed = no

dense_graph_called = no

generated_response_text = no

public_route_created = no

source_files_created = no

docs_project_sources_created = no

Summary:

- Added a tiny backend-only bridge helper that maps a safe review-only staging summary into a generated-run bridge candidate object.
- The helper creates a minimum real-run input candidate, but does not execute the minimum real-run wrapper.
- The helper does not call dense graph integration.
- The helper does not read package row files, write Evidence Layer, create a production case, create a production `analysis_run`, add routes, or touch frontend.

## B. Changed Files

Backend service/helper:

- `backend/app/services/staging_candidate_generated_run_bridge.py`

Backend tests:

- `backend/app/tests/test_staging_candidate_generated_run_bridge.py`

Docs / health:

- `docs/health/sentigraph_8v_4_staging_candidate_generated_run_bridge_skeleton_report_v0_1.md`

Frontend code:

- none

API routes:

- none

Runtime files:

- none

Project Source files:

- none

## C. Implemented Bridge Skeleton

New helper functions:

- `build_staging_candidate_generated_run_bridge`
- `build_minimum_real_run_input_candidate_from_staging`
- `build_safe_staging_to_generated_run_bridge_summary`

The bridge accepts a safe review-only staging summary/candidate-like dict and returns a plain dict with:

- `bridge_schema = sentigraph_staging_candidate_generated_run_bridge_v0_1`
- deterministic bridge id derived from staging candidate id
- safe upstream refs
- `metadata_only=true`
- row parsing and production side-effect flags false
- human review required
- generated run requested false
- a safe minimum real-run input candidate
- boundary flags
- runtime side-effect flags
- warnings/blockers
- downstream allowed/blocked action labels

The helper is intentionally pure and local. It performs no file IO and no external calls.

## D. Bridge Output Contract Summary

Ready bridge status:

- `ready_for_minimum_real_run_input_candidate`

Blocked / review statuses:

- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_path_escape`
- `blocked_requested_side_effect`
- `manual_review_required`

The bridge emits required false flags:

- `evidence_rows_parsed=false`
- `evidence_layer_write=false`
- `production_case_created=false`
- `production_analysis_run_created=false`
- `generated_response_text=false`
- `public_route_created=false`

The bridge blocks downstream actions including:

- parse evidence rows
- read original package rows
- write Evidence Layer
- create production case
- create production analysis run
- execute minimum real-run now
- call dense graph directly
- add API route
- add frontend UI
- generate report
- generate Sandbox/public event
- publish/send/post/execute

## E. Minimum Real-run Input Candidate Summary

The input candidate is metadata-only. It includes:

- `case_id_hint`
- `sample_id`
- `provider_result_id`
- `staging_candidate_id`
- `package_name`
- `package_role`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `coverage_summary`
- `validation_summary`
- `scope_note`
- `model_input_kind = metadata_only_staging_summary`
- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- `human_review_required = true`
- `evidence_items_safe = []`

It does not execute or produce an actual `sentigraph_opinion_ecosystem_run_v0_1`.

## F. Safety Assertions

The focused tests assert:

- ready safe staging summary maps to bridge candidate
- minimum real-run input candidate exists but contains no evidence rows
- sentinel token / raw-author / raw-row / profile-url values are blocked or omitted
- requested side-effect flags block the bridge and output side-effect flags remain false
- monkeypatched minimum real-run and dense graph functions are not called
- private/absolute paths are not emitted in safe output
- missing required metadata blocks the bridge as metadata contract failure

## G. Validation Commands and Results

Initial repo checks:

```text
git status --short
git branch --show-current
git rev-parse HEAD
```

Result:

- branch: `main`
- HEAD: `24d30114abb613b70d20d15aee58efd66e1f3f64`
- initial working tree before implementation was clean.

TDD red check:

```text
python -m pytest backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
```

Initial result:

- failed during collection with `ModuleNotFoundError: No module named 'app.services.staging_candidate_generated_run_bridge'`
- this was the expected red state before creating the helper.

New focused test:

```text
python -m pytest backend/app/tests/test_staging_candidate_generated_run_bridge.py -q
```

Final result: passed, `7 passed`.

Nearby existing tests:

```text
python -m pytest backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py backend/app/tests/test_private_collector_review_only_staging.py backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py backend/app/tests/test_opinion_ecosystem_minimum_real_run.py -q
```

Result: passed, `54 passed`.

Py compile:

```text
python -m py_compile backend/app/services/staging_candidate_generated_run_bridge.py backend/app/services/private_collector_review_only_staging.py backend/app/services/opinion_ecosystem_minimum_real_run.py
```

Result: passed.

Final checks:

```text
git diff --check
git status --short
```

Result:

- `git diff --check`: passed.
- `git status --short`: three untracked files only:
  - `backend/app/services/staging_candidate_generated_run_bridge.py`
  - `backend/app/tests/test_staging_candidate_generated_run_bridge.py`
  - `docs/health/sentigraph_8v_4_staging_candidate_generated_run_bridge_skeleton_report_v0_1.md`

Static safety scan:

```text
rg -n "fetch\(|axios|http://|https://|API key|token|cookie|author_name|author_id|profile_url|evidence_items|production_case|analysis_run|auto_execute|publish_now|send_now|post_now|execute_now|private-collector|G:/|C:/" backend/app/services/staging_candidate_generated_run_bridge.py backend/app/tests/test_staging_candidate_generated_run_bridge.py docs/health/sentigraph_8v_4_staging_candidate_generated_run_bridge_skeleton_report_v0_1.md
```

Result:

- Expected matches only: forbidden-field sets, side-effect blocker labels, test sentinels, and written boundary language.
- No `fetch(`, `axios`, `http://`, or `https://` matches.
- No runtime network implementation found.
- No real secret value found.

## H. Not Run and Why

- Full backend pytest: not run by task boundary; this was a focused backend-only skeleton.
- Frontend build: not run because no frontend code changed.
- Browser smoke: not run because no UI/route behavior changed.
- Collector: not run by boundary.
- Real APIs / real LLMs / network: not run by boundary.
- Private collector source inspection: not run by boundary.
- Real exchange directory read: not run by boundary.
- Evidence row parsing: not run by boundary and explicitly avoided.

## I. Issues P0/P1/P2/P3

P0 privacy/security:

- none found.

P1 functional blockers:

- none found.

P2 next step:

- A separate decision is still required before executing the actual minimum real-run wrapper from a bridge candidate.
- Dense graph must remain downstream of a safe generated-run object and is not approved by this skeleton.

P3 cleanup:

- Helper names and status labels may be promoted to schema/dataclass types later if the bridge becomes persisted or routed.
- Current implementation intentionally stays as a small pure dict helper.

## J. Recommended Next Step

Recommended next task:

Phase 8V-5 Minimum Real-run Bridge Execution Decision Docs-only.

Alternative only if the team wants to proceed immediately after explicit approval:

Phase 8V-5 Controlled Minimum Real-run Bridge Smoke.

Do not choose:

- frontend polish
- dense graph frontend integration
- algorithm/weight recalibration
- row preview gate
- production Evidence import
- production case / production `analysis_run`
- public route
- real API / real LLM

## K. Source Maintenance

source_update_recommended = no immediate

Reason:

This is a small backend-only bridge skeleton. Source update can wait until the 8V chain reaches actual minimum real-run execution or several 8V checkpoints are batched.
