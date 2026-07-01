# Sentigraph 8V-8 Generated-run Dense Graph Integration Smoke Report v0.1

## A. Decision / Status

phase = 8V-8

task = controlled_generated_run_to_dense_graph_integration_smoke

decision = ready

privacy_issue_stop = no

backend_only = yes

test_first = yes

metadata_only_upstream = yes

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

dense_graph_executed = yes, only inside the controlled backend-only helper/test path

frontend_integration_approved = no

route_ready = no

frontend_ready = no

production_ready = no

report_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

source_files_created = no

docs_project_sources_created = no

Summary:

- Added a tiny backend-only helper that accepts a safe 8V-6 execution object and calls the existing dense graph integration/helper surface.
- The helper is deterministic and in-memory only.
- The helper does not add or modify routes.
- The helper does not touch frontend.
- The helper does not parse evidence rows or package files.
- The helper does not write Evidence Layer, create production case, create production `analysis_run`, generate report, generate Sandbox/public event runtime, or create public output.

## B. Changed Files

Backend service/helper:

- `backend/app/services/generated_run_dense_graph_bridge_integration.py`

Backend tests:

- `backend/app/tests/test_generated_run_dense_graph_bridge_integration.py`

Docs / health:

- `docs/health/sentigraph_8v_8_generated_run_dense_graph_integration_smoke_report_v0_1.md`

Frontend code:

- none

API routes:

- none

Runtime files:

- none

Project Source files:

- none

## C. Integration Helper Summary

New helper functions:

- `integrate_generated_run_with_dense_graph_from_execution`
- `build_generated_run_dense_graph_bridge_integration`
- `build_safe_generated_run_dense_graph_bridge_summary`

Ready integration object:

- `integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- `integration_status = integrated_backend_dense_graph_preview`
- `input_source_kind = minimum_real_run_bridge_execution`
- `integration_mode = controlled_backend_only_generated_run_dense_graph`
- `generated_run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- `dense_graph_executed = true`
- `frontend_integration_approved = false`
- `route_changed = false`
- `api_route_added = false`
- `report_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- dense graph summary keeps route/frontend/production readiness false
- runtime side-effect flags false

Blocked integration object:

- `dense_graph_executed = false`
- `dense_graph_integration = null`
- route/frontend/report/public flags false
- runtime side-effect flags false
- blockers explain why dense graph was not allowed

## D. Ready Integration Path

The ready test path builds:

1. safe review-only staging summary
2. 8V-4 `sentigraph_staging_candidate_generated_run_bridge_v0_1`
3. 8V-6 `sentigraph_minimum_real_run_bridge_execution_v0_1`
4. existing `sentigraph_opinion_ecosystem_run_v0_1` generated run
5. 8V-8 `sentigraph_generated_run_dense_graph_bridge_integration_v0_1`

The dense graph integration remains:

- backend-only
- selected-sample-only
- controlled generated-run only
- internal preview
- anonymous aggregate/proxy only
- `frontend_ready = false`
- `route_ready = false`
- `production_ready = false`
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human-review-required

## E. Blocked Path Behavior

The helper blocks without calling dense graph when:

- execution schema is wrong
- execution status is not ready
- minimum real-run was not executed
- dense graph was already called upstream
- metadata-only boundary is not true
- evidence rows parsed flag is not false
- generated run is missing
- generated-run schema is wrong
- generated-run boundary flags are missing or false
- generated-run runtime side-effect flags are true
- upstream blockers indicate privacy/security/path/side-effect/production/public-output risk
- forbidden active fields appear
- private or absolute path is detected
- row parsing, Evidence Layer, production case, production `analysis_run`, route, frontend, report, Sandbox/public event, generated response, public route, publish/send/post/execute, real API, real LLM, collector, private project access, URL fetch, or scrape is requested

## F. Dense Graph Output Boundary

The integration object and dense graph summary keep conservative boundaries:

- selected sample only
- controlled generated-run only
- metadata-only upstream
- anonymous aggregate/proxy only
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
- frontend not approved
- route not changed
- API route not added
- report not generated
- Sandbox/public event not generated

The execution marker `dense_graph_executed = true` means only that the backend-only dense graph preview helper ran against a safe 8V-6 generated run. It does not mean route readiness, frontend readiness, production readiness, public access, report generation, or Sandbox/public event generation.

## G. Safety Assertions

Focused tests assert:

- ready 8V chain reaches dense graph integration
- frontend/route/report/public flags remain false
- runtime side-effect flags remain false
- blocked 8V-6 execution does not call dense graph
- requested side effects block dense graph
- forbidden sentinel token / author / profile URL / raw row / private path / response text values do not leak
- no package files are opened
- no `evidence_items.jsonl` or `evidence_items.csv` path appears in output
- missing generated run blocks dense graph
- forbidden output fields are not produced

## H. Validation Commands and Results

Initial repo checks:

```text
git status --short
git branch --show-current
git rev-parse HEAD
```

Result:

- initial working tree before 8V-8 changes was clean.
- branch: `main`
- HEAD: `2a100d79e6d8a5e2c3469089d7a9474f735b0396`

TDD red check:

```text
python -m pytest backend/app/tests/test_generated_run_dense_graph_bridge_integration.py -q
```

Initial result:

- failed during collection with `ModuleNotFoundError: No module named 'app.services.generated_run_dense_graph_bridge_integration'`
- this was the expected red state before creating the helper.

New focused test:

```text
python -m pytest backend/app/tests/test_generated_run_dense_graph_bridge_integration.py -q
```

Final result: passed, `8 passed`.

Nearby existing tests:

```text
python -m pytest backend/app/tests/test_generated_run_dense_graph_bridge_integration.py backend/app/tests/test_minimum_real_run_bridge_execution.py backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py -q
```

Result: passed, `46 passed`.

Py compile:

```text
python -m py_compile backend/app/services/generated_run_dense_graph_bridge_integration.py backend/app/services/minimum_real_run_bridge_execution.py backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py
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
  - `backend/app/services/generated_run_dense_graph_bridge_integration.py`
  - `backend/app/tests/test_generated_run_dense_graph_bridge_integration.py`
  - `docs/health/sentigraph_8v_8_generated_run_dense_graph_integration_smoke_report_v0_1.md`

## I. Not Run and Why

- Full backend pytest: not run by task instruction; focused and nearby tests were required instead.
- Frontend build: not run because no frontend code changed.
- Browser smoke: not run because no UI/route behavior changed.
- Collector: not run by boundary.
- Real APIs / real LLMs / network: not run by boundary.
- Private collector source inspection: not run by boundary.
- Real exchange directory read: not run by boundary.
- Evidence row parsing: not run by boundary and explicitly avoided.
- Route smoke: not run because route behavior was not changed and this phase is backend helper only.

## J. Issues P0/P1/P2/P3

P0 privacy/security:

- none found.

P1 functional blockers:

- none found.

P2 next-step boundary:

- A separate decision is required before dense graph route, frontend, report, Sandbox/public event, public route, row parsing, Evidence Layer import, production case, or production `analysis_run`.
- Existing dense graph route behavior was not changed and remains governed by its own disabled/internal boundary.

P3 cleanup:

- Helper schemas may later become typed schema objects if the chain is routed or persisted.
- Status labels may later be centralized if more bridge stages are added.

## K. Recommended Next Step

Recommended next task:

Phase 8V-9 Dense Graph to Report Candidate Decision Docs-only.

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

source_update_recommended = consider_after_8V_8_commit

Reason:

8V-8 is the first controlled generated-run to dense graph bridge execution in the 8V provider/staging/generated-run chain. Do not create Source files in this repo. Recommend ChatGPT-side Source patch only after the user commits 8V-8 and the working tree is clean.
