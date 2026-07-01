# Sentigraph 8V-7 Generated-run to Dense Graph Integration Decision v0.1

## A. Decision / Status

phase = 8V-7

task = generated_run_to_dense_graph_integration_decision

decision = ready

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_code_changed = no

tests_changed = no

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

dense_graph_executed = no

frontend_integration_approved = no

report_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

source_files_created = no

docs_project_sources_created = no

current_ready_state = ready_for_8V_8_controlled_generated_run_to_dense_graph_integration_smoke

Decision:

8V-7 approves only a future controlled backend-only dense graph integration smoke from a safe 8V-6 generated-run execution object.

8V-7 does not implement runtime code, does not execute dense graph, does not add routes, does not touch frontend, does not parse evidence rows, and does not approve public/customer output.

## B. Current Proven Chain Through 8V-6

The current proven chain is:

1. safe review-only staging summary
2. `sentigraph_staging_candidate_generated_run_bridge_v0_1`
3. `sentigraph_minimum_real_run_bridge_execution_v0_1`
4. existing `sentigraph_opinion_ecosystem_run_v0_1` generated run

8V-6 proved:

- a safe 8V-4 bridge candidate can execute the existing backend-only minimum real-run wrapper
- the generated run remains selected-sample / controlled metadata scoped
- `human_review_required = true`
- coefficient/calibration/validation metadata remains conservative
- runtime side-effect flags remain false
- dense graph is not called
- no Evidence Layer write occurs
- no production case is created
- no production `analysis_run` is created
- no report, Sandbox, public event, route, frontend, real API, real LLM, collector, URL fetch, or scrape is introduced

Separately, earlier 8U dense graph work proved backend-only dense graph integration and a disabled-by-default internal route. 8V-7 does not expand that route and does not approve frontend or public access.

## C. Generated-run to Dense Graph Problem Statement

The next narrow problem is:

Can Sentigraph safely pass a generated run produced through the 8V-6 bridge execution path into the existing dense graph integration helper while preserving all boundaries?

This is not the same as:

- exposing dense graph through frontend
- adding a route
- changing the existing disabled/internal route behavior
- creating a production analysis
- generating a B-end report
- generating Sandbox or public event runtime
- parsing original evidence rows
- recalibrating algorithm weights
- claiming full-web, official verification, prediction, or causal proof

The future 8V-8 smoke should prove only backend-only compatibility between the 8V-6 generated-run object and dense graph integration.

## D. Allowed Future Input

Future 8V-8 may use only a safe generated run object produced through an 8V-6 execution object.

Required generated-run input:

- `run_schema = sentigraph_opinion_ecosystem_run_v0_1` or current equivalent
- `human_review_required = true`
- selected-sample / controlled metadata scoped
- `coefficient_source = mock_default` or current equivalent
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- boundary flags present
- runtime side-effect flags all false
- no response text
- no public output
- no blockers indicating privacy, security, path, side-effect, production, public-output, or real-provider risk

Allowed safe upstream refs:

- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `input_source_kind`
- `execution_mode`

The future smoke may also carry safe count/summary fields already present in the generated run or execution object. It must not use original package rows.

## E. Forbidden Input / Forbidden Output

Forbidden input:

- evidence row content
- raw comments
- raw author identifiers
- actual author name values
- actual profile URL values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- absolute private paths
- browser profile paths
- collector internals
- external URL contents
- live platform payloads
- original package rows

Forbidden output:

- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- `auto_execute`
- `publish_now`
- `send_now`
- `post_now`
- `execute_now`
- public route
- public URL
- B-end report runtime
- Sandbox/public event runtime
- Evidence Layer write result
- production case
- production `analysis_run`

Safe negative boundary flags may name these concepts only to confirm that they are false, blocked, or not approved.

## F. Future Dense Graph Integration Gate Conditions

Future 8V-8 must stop unless all of these are true:

- 8V-6 execution object exists
- execution schema is recognized
- execution status is `executed_local_minimum_real_run`
- `minimum_real_run_executed = true`
- `dense_graph_called = false` before 8V-8 execution
- generated run exists
- generated-run schema is recognized
- generated-run runtime side-effect flags are all false
- generated-run boundary flags are present and conservative
- generated-run `human_review_required = true`
- generated-run blockers do not include privacy/security/path/side-effect blockers
- no requested row parsing exists
- no requested Evidence Layer write exists
- no requested production case or production `analysis_run` exists
- no requested route, frontend, report, Sandbox/public event, public output, publish/send/post/execute action exists
- no requested real API, real LLM, collector, private collector access, URL fetch, or scrape exists

If any condition fails, the future smoke should return a blocked integration candidate and must not call dense graph.

## G. Future Dense Graph Output Boundary

Future dense graph output must remain:

- selected-sample-only
- controlled generated-run only
- internal backend preview
- anonymous aggregate/proxy only
- `frontend_ready = false`
- `route_ready = false` for the 8V-8 bridge smoke
- `production_ready = false`
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human-review-required

Dense graph may summarize proxy counts and preview graph metadata. It must not expose raw identities, raw comments, original package rows, private paths, or public response text.

## H. Relationship to Frontend / Report / Sandbox / Public Event

8V-7 does not approve frontend dense graph integration.

8V-7 does not approve public route creation.

8V-7 does not approve B-end or customer route creation.

8V-7 does not approve B-end report runtime.

8V-7 does not approve Sandbox/public event runtime.

8V-7 does not approve algorithm or weight recalibration.

8V-7 does not approve frontend polish.

Existing dense graph backend/internal route work remains governed by its own disabled-by-default boundary. 8V-8 should not change route behavior.

## I. Next-slice Options

| Option | Description | Risk | Recommended |
| --- | --- | --- | --- |
| 8V-8 Controlled Generated-run to Dense Graph Integration Smoke | Backend-only, test-first smoke from an 8V-6 generated run into existing dense graph integration | low | yes |
| 8V-8 Docs-only test plan | Add more test design before implementation | lowest | acceptable if caution is preferred |
| Dense graph frontend integration | UI/API consumption of dense graph output | medium | not now |
| Row parsing | Parse package evidence files | medium/high | not now |
| Report/Sandbox/public-event runtime | Product output generation | high | not approved |
| Production Evidence import | Evidence Layer / production case / production analysis | high | not approved |

## J. Recommended Next Step

Recommended next task:

Phase 8V-8 Controlled Generated-run to Dense Graph Integration Smoke / Backend-only Test-first.

Recommended scope:

- backend-only
- test-first
- input is a safe 8V-6 execution object with generated run
- use existing dense graph integration/helper only under controlled test path
- no API route
- no frontend
- no runtime persistence
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no B-end report
- no Sandbox/public event runtime
- no public output
- no row parsing
- no collector/private project access
- no real API or real LLM
- no URL fetch or scraping

If implementation requires route changes, frontend changes, row parsing, production writes, report generation, or public output, stop and create a new decision checkpoint instead.

## K. Explicit Non-approvals

8V-7 does not approve:

- backend runtime implementation in this task
- dense graph execution in this task
- route change
- API route addition
- frontend integration
- frontend polish
- runtime persistence
- collector execution
- private collector inspection
- real exchange directory read
- evidence row parsing
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- B-end report runtime
- Sandbox/public event runtime
- generated response text
- public route
- public URL
- real API
- real LLM
- URL fetching
- scraping
- MediaCrawler integration
- OpenClaw production integration
- algorithm/weight recalibration

## L. Validation / Not Run

Validation for this docs-only phase:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git diff --check
```

Optional static scan:

```text
rg -n "fetch\(|axios|http://|https://|API key|token|cookie|author_name|author_id|profile_url|evidence_items|production_case|analysis_run|auto_execute|publish_now|send_now|post_now|execute_now|frontend_ready|production_ready" docs/planning/sentigraph_8v_7_generated_run_to_dense_graph_integration_decision_v0_1.md docs/architecture/sentigraph_generated_run_to_dense_graph_integration_contract_v0_1.md
```

Expected scan result:

- Matches are acceptable only in boundary, forbidden, blocker, false-flag, or explicit non-approval language.
- No runtime implementation should appear.

Not run:

- pytest: not run because this phase is docs-only.
- frontend build: not run because no frontend code changed.
- browser smoke: not run because no UI changed.
- collector: not run by boundary.
- real APIs/LLMs/network: not run by boundary.
- dense graph execution: not run because this phase is a decision checkpoint.

## M. Source Maintenance Note

source_update_recommended = no immediate

Reason:

8V-7 is a docs-only decision checkpoint. It does not change runtime behavior, route behavior, frontend behavior, provider/package behavior, or Project Source files.

After a future 8V-8 implementation and validation, Source maintenance may be reconsidered as a batched update.
