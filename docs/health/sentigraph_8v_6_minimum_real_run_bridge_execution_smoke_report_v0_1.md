# Sentigraph 8V-6 Minimum Real-run Bridge Execution Smoke Report v0.1

## A. Decision / Status

phase = 8V-6

task = controlled_minimum_real_run_bridge_execution_smoke

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

minimum_real_run_executed = yes, only inside the controlled backend-only helper/test path

dense_graph_called = no

generated_response_text = no

public_route_created = no

report_generated = no

sandbox_public_event_generated = no

source_files_created = no

docs_project_sources_created = no

Summary:

- Added a tiny backend-only helper that accepts a safe 8V-4 bridge candidate and executes the existing pure-local minimum real-run wrapper.
- The helper is deterministic and in-memory only.
- The helper does not call dense graph.
- The helper does not parse evidence rows or package files.
- The helper does not write Evidence Layer, create production case, create production `analysis_run`, add routes, touch frontend, or write runtime files.

## B. Changed Files

Backend service/helper:

- `backend/app/services/minimum_real_run_bridge_execution.py`

Backend tests:

- `backend/app/tests/test_minimum_real_run_bridge_execution.py`

Docs / health:

- `docs/health/sentigraph_8v_6_minimum_real_run_bridge_execution_smoke_report_v0_1.md`

Frontend code:

- none

API routes:

- none

Runtime files:

- none

Project Source files:

- none

## C. Execution Helper Summary

New helper functions:

- `execute_minimum_real_run_from_bridge_candidate`
- `build_minimum_real_run_bridge_execution`
- `build_safe_minimum_real_run_bridge_execution_summary`

Ready execution object:

- `execution_schema = sentigraph_minimum_real_run_bridge_execution_v0_1`
- `execution_status = executed_local_minimum_real_run`
- `input_source_kind = staging_candidate_generated_run_bridge`
- `execution_mode = controlled_backend_only_minimum_real_run`
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `minimum_real_run_executed = true`
- `dense_graph_called = false`
- generated run embedded under `generated_run`
- boundary flags preserved
- runtime side-effect flags false

Blocked execution object:

- `minimum_real_run_executed = false`
- `dense_graph_called = false`
- `generated_run = null`
- runtime side-effect flags false
- blockers explain why execution was not allowed

## D. Ready Execution Path

The ready test path builds:

1. safe review-only staging summary
2. 8V-4 `sentigraph_staging_candidate_generated_run_bridge_v0_1`
3. 8V-6 `sentigraph_minimum_real_run_bridge_execution_v0_1`
4. existing `sentigraph_opinion_ecosystem_run_v0_1` generated run

The generated run remains:

- backend-only
- selected sample / controlled metadata scoped
- human-review-required
- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- not prediction
- not causal proof
- not official verification
- not production score
- no response text
- no public output

## E. Blocked Path Behavior

The helper blocks without calling the wrapper when:

- bridge status is not ready
- bridge schema is wrong
- bridge id is missing
- package name is missing
- metadata-only boundary is not true
- evidence rows parsed flag is not false
- human review required flag is not true
- generated run was already requested
- minimum real-run input candidate is missing
- runtime side-effect flags are true
- upstream blockers are present
- privacy/forbidden fields appear
- path escape is detected
- row parsing / Evidence Layer / production case / production `analysis_run` / dense graph / report / public output / generated response actions are requested

## F. Generated-run Output Boundary

The execution object and generated run keep conservative boundaries:

- selected sample only
- controlled metadata only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- provider output is evidence, not truth
- human review required
- no auto-execute
- no generated public response

The execution marker `minimum_real_run_executed = true` means only that the existing backend-only local wrapper ran against a safe in-memory bridge candidate. It does not mean production `analysis_run` creation or downstream product output.

## G. Safety Assertions

Focused tests assert:

- ready bridge executes the existing minimum real-run wrapper
- blocked bridge does not execute the wrapper
- requested side effects block execution
- dense graph integration is not called
- forbidden sentinel token / author / profile URL / raw row / private path values do not leak
- no package files are opened
- no `evidence_items.jsonl` or `evidence_items.csv` path appears in output
- missing minimum real-run input candidate blocks execution
- forbidden output fields are not produced
- side-effect flags remain false

## H. Validation Commands and Results

Initial repo checks:

```text
git status --short
git branch --show-current
git rev-parse HEAD
```

Result:

- initial working tree before 8V-6 changes was clean.
- branch: `main`
- HEAD: `8c2af765dbae25ade2e0e5855442f9cc0fc12813`

TDD red check:

```text
python -m pytest backend/app/tests/test_minimum_real_run_bridge_execution.py -q
```

Initial result:

- failed during collection with `ModuleNotFoundError: No module named 'app.services.minimum_real_run_bridge_execution'`
- this was the expected red state before creating the helper.

New focused test:

```text
python -m pytest backend/app/tests/test_minimum_real_run_bridge_execution.py -q
```

Final result: passed, `8 passed`.

Nearby existing tests:

```text
python -m pytest backend/app/tests/test_minimum_real_run_bridge_execution.py backend/app/tests/test_staging_candidate_generated_run_bridge.py backend/app/tests/test_opinion_ecosystem_minimum_real_run.py backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py -q
```

Result: passed, `27 passed`.

Py compile:

```text
python -m py_compile backend/app/services/minimum_real_run_bridge_execution.py backend/app/services/staging_candidate_generated_run_bridge.py backend/app/services/opinion_ecosystem_minimum_real_run.py
```

Result: passed.

Final checks:

```text
git diff --check
git status --short
```

Result:

- `git diff --check`: passed.
- `git status --short`: three untracked files:
  - `backend/app/services/minimum_real_run_bridge_execution.py`
  - `backend/app/tests/test_minimum_real_run_bridge_execution.py`
  - `docs/health/sentigraph_8v_6_minimum_real_run_bridge_execution_smoke_report_v0_1.md`

## I. Not Run and Why

- Full backend pytest: not run by task instruction; focused and nearby tests were required instead.
- Frontend build: not run because no frontend code changed.
- Browser smoke: not run because no UI/route behavior changed.
- Collector: not run by boundary.
- Real APIs / real LLMs / network: not run by boundary.
- Private collector source inspection: not run by boundary.
- Real exchange directory read: not run by boundary.
- Evidence row parsing: not run by boundary and explicitly avoided.
- Dense graph route/integration smoke: not run; dense graph was only imported in tests for a no-call monkeypatch assertion.

## J. Issues P0/P1/P2/P3

P0 privacy/security:

- none found.

P1 functional blockers:

- none found.

P2 next-step boundary:

- A separate decision is required before dense graph integration.
- A separate decision is required before any route/UI exposure.
- A separate decision is required before row parsing, Evidence Layer import, production case, production `analysis_run`, report generation, Sandbox/public event runtime, or public access.

P3 cleanup:

- Execution/helper schemas may later become typed schema objects if the chain is routed or persisted.
- Status labels may later be centralized if more bridge stages are added.

## K. Recommended Next Step

Recommended next task:

Phase 8V-7 Generated-run to Dense Graph Integration Decision Docs-only.

Do not recommend:

- frontend polish
- dense graph frontend integration
- algorithm/weight recalibration
- row preview gate
- production Evidence import
- production case / production `analysis_run`
- public route
- real API / real LLM

## L. Source Maintenance

source_update_recommended = consider_after_8V_6_commit

Reason:

8V-6 is the first controlled minimum real-run execution from the provider/staging bridge. Do not create Source files in this repo. Recommend ChatGPT-side Source patch only after the user commits 8V-6 and the working tree is clean.
