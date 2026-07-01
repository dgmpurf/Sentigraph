# Sentigraph 8V-5 Minimum Real-run Bridge Execution Decision v0.1

## A. Decision / Status

phase = 8V-5

task = minimum_real_run_bridge_execution_decision

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

minimum_real_run_executed = no

dense_graph_called = no

generated_response_text = no

public_route_created = no

source_files_created = no

docs_project_sources_created = no

current_ready_state = ready_for_8V_6_controlled_minimum_real_run_bridge_execution_smoke

Decision:

8V-5 approves a future controlled backend-only smoke slice that may execute the existing minimum real-run wrapper from an 8V-4 bridge candidate, provided every gate condition in this document is met.

8V-5 does not execute the wrapper, does not implement runtime, does not add an API route, does not add frontend UI, does not call dense graph, and does not parse evidence rows.

## B. Current Proven Chain Through 8V-4

The current proven chain is:

1. controlled provider/package metadata
2. package resolver and metadata-only local exchange fixtures
3. review-only staging candidate
4. staging candidate to generated-run bridge skeleton
5. minimum real-run input candidate metadata

8V-4 proved that the bridge helper can map a safe review-only staging summary into a `sentigraph_staging_candidate_generated_run_bridge_v0_1` object with:

- `bridge_status = ready_for_minimum_real_run_input_candidate` for eligible metadata
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- `production_case_created = false`
- `production_analysis_run_created = false`
- `generated_response_text = false`
- `public_route_created = false`
- `human_review_required = true`
- `generated_run_requested = false`
- `minimum_real_run_input_candidate` present
- runtime side-effect flags false

8V-4 also proved that the bridge helper does not call the minimum real-run wrapper and does not call dense graph integration.

## C. Minimum Real-run Execution Problem Statement

The next problem is narrow:

Can Sentigraph safely call the existing backend-only minimum real-run wrapper using only the safe in-memory input candidate created by the 8V-4 bridge?

This is not the same as:

- importing evidence
- reading original package rows
- promoting a staging candidate to production
- creating a production `analysis_run`
- generating a report
- generating a Sandbox or public event runtime
- calling dense graph directly
- generating public response text

The future 8V-6 smoke should prove only that a safe bridge candidate can become a local generated-run object while preserving all governance boundaries.

## D. Allowed Future Execution Input

Future 8V-6 may use only an 8V-4 bridge object whose safe metadata confirms:

- `bridge_schema = sentigraph_staging_candidate_generated_run_bridge_v0_1`
- `bridge_status = ready_for_minimum_real_run_input_candidate`
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `human_review_required = true`
- `minimum_real_run_input_candidate` exists
- `minimum_real_run_input_candidate.model_input_kind = metadata_only_staging_summary`
- `minimum_real_run_input_candidate.evidence_items_safe = []`
- `minimum_real_run_input_candidate.coefficient_source` remains the existing mock/default coefficient source if present
- `minimum_real_run_input_candidate.calibration_status = uncalibrated`
- `minimum_real_run_input_candidate.empirical_validation = not_started`
- no blockers
- all bridge runtime side-effect flags are false
- no requested production actions are present

Future 8V-6 should pass only a safe in-memory dict/object to the existing backend-only minimum real-run wrapper.

## E. Forbidden Input / Forbidden Output

Forbidden input:

- `evidence_items.jsonl`
- `evidence_items.csv`
- original package row files
- raw evidence rows
- raw comments
- raw author identifiers
- raw author names
- profile URL values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- absolute private package paths
- browser profile paths
- collector runtime internals
- external URL contents
- any live platform payload

Forbidden output:

- Evidence Layer write result
- production case
- production `analysis_run`
- dense graph attachment
- B-end report
- Sandbox/public event runtime
- public route
- public URL
- response text
- generated public message
- target user list
- persuasion score
- truth score
- official verification field
- prediction probability
- psychology or personality diagnosis
- publish/send/post/execute action

The future execution smoke may mention these concepts only as false flags, blockers, or explicit non-approvals.

## F. Future Execution Gate Conditions

Future 8V-6 must stop unless all of these are true:

- bridge object exists
- bridge schema is recognized
- bridge status is `ready_for_minimum_real_run_input_candidate`
- bridge is metadata-only
- no evidence rows were parsed
- no original package rows were read
- no privacy blocker exists
- no path escape blocker exists
- no forbidden metadata field is present
- no requested production action exists
- no requested dense graph action exists
- no requested public route or generated public response exists
- no requested collector job exists
- no requested real API or real LLM exists
- minimum real-run input candidate exists
- human review remains required
- coefficient/calibration/validation metadata remains conservative
- runtime side-effect flags are all false before execution

If any condition fails, the future smoke must produce a blocked result instead of executing the wrapper.

## G. Future Controlled Execution Output Boundary

Future 8V-6 may produce a local backend-only object using schema:

`sentigraph_minimum_real_run_bridge_execution_v0_1`

The future object may carry:

- bridge refs
- staging refs
- package name
- controlled input metadata
- the generated `sentigraph_opinion_ecosystem_run_v0_1` object
- boundary flags
- runtime side-effect flags
- warnings
- blockers
- audit metadata

The future object must make these boundaries visible:

- selected sample only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- no auto-execute
- no generated public response
- provider output is evidence, not truth

In 8V-6, `minimum_real_run_executed` may be true only for the controlled local wrapper call. It must not mean production `analysis_run` creation, Evidence Layer write, report generation, dense graph generation, or public output.

## H. Relationship to Dense Graph / Calculator / Report

The existing minimum real-run wrapper remains upstream of dense graph.

The future 8V-6 smoke must not call dense graph directly. Dense graph may only be considered after a safe generated-run object exists and after a separate decision approves the next integration step.

The existing calculator remains mock/default and uncalibrated. It should not be presented as:

- official verification
- causal proof
- prediction
- production score
- calibrated empirical model
- full-web or full-platform result

Report generation remains a separate gated chain. 8V-6 must not generate Summary Report Candidate, Final Summary Report, export package, public access, B-end report, Sandbox runtime, or public event runtime.

## I. Next-slice Options

| Option | Description | Risk | Recommended |
| --- | --- | --- | --- |
| 8V-6 Controlled Minimum Real-run Bridge Execution Smoke | Backend-only, test-first wrapper execution from a safe bridge candidate | low | yes |
| 8V-6 Docs-only test plan | Add more detail before execution | lowest | acceptable if caution is preferred |
| Dense graph integration | Attach dense graph after generated-run | medium | not now |
| Row parsing | Parse package evidence files | medium/high | not now |
| Production Evidence import | Write Evidence Layer / production case | high | not approved |
| Public route or report runtime | Customer-facing output | high | not approved |

## J. Recommended Next Step

Recommended next task:

Phase 8V-6 Controlled Minimum Real-run Bridge Execution Smoke.

Recommended scope:

- backend-only
- test-first
- no API route
- no frontend
- no runtime persistence unless a test-local in-memory object is enough
- execute only the existing minimum real-run wrapper
- input only the safe 8V-4 bridge candidate
- no row parsing
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no dense graph call
- no report/Sandbox/public event output
- no collector/private project access
- no real API or real LLM
- no URL fetch or scraping

If implementation requires file IO, row parsing, route changes, frontend work, dense graph, or production writes, stop and create a new decision checkpoint instead.

## K. Explicit Non-approvals

8V-5 does not approve:

- backend runtime implementation in this task
- API route
- frontend integration
- route change
- runtime persistence
- collector execution
- private collector inspection
- real exchange directory read
- package row parsing
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- dense graph call in the same step
- report runtime
- B-end report runtime
- Sandbox/public event runtime
- Strategy Lab runtime
- generated response text
- public route
- public URL
- real API
- real LLM
- URL fetching
- scraping
- MediaCrawler integration
- OpenClaw production integration

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
rg -n "fetch\(|axios|http://|https://|API key|token|cookie|author_name|author_id|profile_url|evidence_items|production_case|analysis_run|auto_execute|publish_now|send_now|post_now|execute_now" docs/planning/sentigraph_8v_5_minimum_real_run_bridge_execution_decision_v0_1.md docs/architecture/sentigraph_minimum_real_run_bridge_execution_contract_v0_1.md
```

Expected scan result:

- Matches are acceptable only in boundary, forbidden, blocker, or false-flag language.
- No runtime implementation should appear.

Not run:

- pytest: not run because this phase is docs-only.
- frontend build: not run because no frontend code changed.
- browser smoke: not run because no UI changed.
- collector: not run by boundary.
- real APIs/LLMs/network: not run by boundary.

## M. Source Maintenance Note

source_update_recommended = no immediate

Reason:

This is a docs-only decision checkpoint. It does not change runtime behavior, API behavior, frontend behavior, Analysis Request governance, provider package behavior, or Project Source files.

After a future 8V-6 implementation and validation, Source maintenance may be reconsidered as a batched update.
