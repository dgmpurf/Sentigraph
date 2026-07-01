# Sentigraph Minimum Real-run Bridge Execution Contract v0.1

## A. Contract Purpose

This contract defines the future controlled execution object for the first backend-only minimum real-run generated from an 8V-4 staging candidate bridge.

The contract exists to keep the next implementation slice narrow:

- execute only the existing pure-local minimum real-run wrapper
- consume only safe metadata from an already-ready bridge candidate
- keep the result local, uncalibrated, selected-sample-only, and human-review-required
- prove all production and public-output side effects remain blocked

This contract is not an implementation. It is not an API route. It is not frontend integration. It is not Evidence Layer import. It is not production analysis.

## B. Proposed Future Execution Contract

Proposed schema:

```json
{
  "execution_schema": "sentigraph_minimum_real_run_bridge_execution_v0_1"
}
```

Proposed future object:

```json
{
  "execution_id": "minimum_real_run_bridge_execution_...",
  "execution_schema": "sentigraph_minimum_real_run_bridge_execution_v0_1",
  "execution_status": "executed_local_minimum_real_run|blocked|manual_review_required",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "bridge_id": "staging_generated_run_bridge_...",
  "bridge_schema": "sentigraph_staging_candidate_generated_run_bridge_v0_1",
  "bridge_status_at_execution": "ready_for_minimum_real_run_input_candidate",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "provider_job_id": "provider_job_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "input_source_kind": "staging_candidate_generated_run_bridge",
  "execution_mode": "controlled_backend_only_minimum_real_run",
  "metadata_only": true,
  "evidence_rows_parsed": false,
  "minimum_real_run_executed": true,
  "dense_graph_called": false,
  "generated_run": {},
  "boundary_flags": {},
  "runtime_side_effects": {},
  "warnings": [],
  "blockers": [],
  "audit_refs": [],
  "downstream_allowed_actions": [],
  "downstream_blocked_actions": []
}
```

The future execution status should be conservative:

- `executed_local_minimum_real_run`
- `blocked_bridge_not_ready`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_requested_side_effect`
- `blocked_forbidden_input`
- `manual_review_required`

## C. Input Contract

Future 8V-6 may accept only a safe bridge candidate from 8V-4.

Required bridge input fields:

- `bridge_id`
- `bridge_schema`
- `bridge_status`
- `staging_candidate_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `metadata_only`
- `evidence_rows_parsed`
- `human_review_required`
- `generated_run_requested`
- `minimum_real_run_input_candidate`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`

Required bridge input values:

- `bridge_schema = sentigraph_staging_candidate_generated_run_bridge_v0_1`
- `bridge_status = ready_for_minimum_real_run_input_candidate`
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `human_review_required = true`
- `generated_run_requested = false`
- all runtime side-effect flags false
- no blockers

Required minimum real-run input candidate values:

- `model_input_kind = metadata_only_staging_summary`
- `human_review_required = true`
- `evidence_items_safe = []`
- `coefficient_source = mock_default` when present
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

The future execution must not open package files, parse rows, follow URLs, inspect private collector internals, or read real exchange directories.

## D. Output Contract

Required execution identity:

- `execution_id`
- `execution_schema`
- `execution_status`
- `created_at`
- `created_by`

Required upstream refs:

- `bridge_id`
- `bridge_schema`
- `bridge_status_at_execution`
- `staging_candidate_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `case_id_hint`
- `package_name`

Required execution boundary:

- `input_source_kind`
- `execution_mode`
- `metadata_only`
- `evidence_rows_parsed`
- `minimum_real_run_executed`
- `dense_graph_called`
- `boundary_flags`
- `runtime_side_effects`

Required generated-run output:

- `generated_run.run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- `generated_run.input_source_kind` must remain local/safe and selected-sample scoped
- `generated_run.human_review_required = true`
- `generated_run.boundary_flags` present
- `generated_run.runtime_side_effects` false
- `generated_run.module_outputs` present if the wrapper returns ready output
- generated-run blockers preserved if the wrapper blocks

Required downstream policy:

- `downstream_allowed_actions`
- `downstream_blocked_actions`
- `warnings`
- `blockers`
- `audit_refs`

## E. Boundary Flags

The execution object and generated run must keep these boundary flags explicit:

```json
{
  "selected_sample_only": true,
  "controlled_package_only": true,
  "metadata_only": true,
  "not_full_web": true,
  "not_full_platform": true,
  "not_full_thread": true,
  "not_official_verification": true,
  "not_causal_proof": true,
  "not_prediction": true,
  "not_production_score": true,
  "provider_output_is_evidence_not_truth": true,
  "human_review_required": true,
  "no_auto_execute": true,
  "no_generated_public_response": true
}
```

Missing or false boundary flags should block the future smoke or mark it `manual_review_required`.

## F. Runtime Side-effect Flags

All future runtime side-effect flags must remain false except the local wrapper execution marker on the execution object.

Required false flags:

```json
{
  "called_real_api": false,
  "called_real_llm": false,
  "ran_collector": false,
  "accessed_private_collector": false,
  "read_real_exchange_dir": false,
  "fetched_url": false,
  "scraped_page": false,
  "parsed_evidence_items_file": false,
  "read_original_package_rows": false,
  "wrote_evidence_layer": false,
  "created_production_case": false,
  "created_analysis_run": false,
  "generated_b_end_report_runtime": false,
  "generated_sandbox_runtime": false,
  "generated_public_event_runtime": false,
  "generated_response_text": false,
  "published_or_sent": false,
  "auto_executed": false
}
```

Allowed execution marker:

```json
{
  "minimum_real_run_executed": true
}
```

This marker means only that the backend-only local wrapper ran against a safe in-memory bridge candidate. It does not mean production `analysis_run`, report generation, public event generation, dense graph generation, or public access.

## G. Blockers / Warnings

Hard blockers:

- bridge schema not recognized
- bridge status not ready
- missing bridge id
- missing package name
- missing minimum real-run input candidate
- `metadata_only` is not true
- `evidence_rows_parsed` is not false
- any runtime side-effect flag is true before execution
- bridge blockers are present
- privacy issue
- path escape
- forbidden metadata field
- requested row parsing
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested dense graph call
- requested report or public output
- requested generated response text
- requested real API or real LLM
- requested collector or private project access

Warnings:

- validation status is warn
- evidence count is low
- source count is low
- unknown or future platform remains manual-review-only
- coverage note is missing or weak
- generated-run output remains uncalibrated
- empirical validation is not started

Warnings do not upgrade trust and do not make the result production-ready.

## H. Audit Fields

Future execution should carry audit metadata:

- `audit_refs`
- `source_bridge_audit_refs`
- `execution_created_by`
- `execution_created_at`
- `execution_reason`
- `input_bridge_summary`
- `boundary_confirmation_snapshot`
- `blocked_action_snapshot`
- `wrapper_name`
- `wrapper_version` if available

Audit must not include raw author identifiers, private paths, row contents, secrets, browser profile paths, or generated public response text.

## I. Downstream Policy

Allowed after future 8V-6:

- inspect the generated run object
- validate boundary flags
- validate runtime side-effect flags
- decide whether a later dense graph integration checkpoint is appropriate
- decide whether frontend/API integration should remain deferred

Blocked after future 8V-6 unless separately approved:

- Evidence Layer write
- production case
- production `analysis_run`
- dense graph call in the same step
- report generation
- B-end report
- Sandbox/public event runtime
- public route
- generated public response text
- public access or delivery
- collector job
- row parsing
- real API
- real LLM
- URL fetch or scraping

The generated run remains selected-sample-only and human-review-required.

## J. Future Tests

Future 8V-6 tests should verify:

- execution object has schema `sentigraph_minimum_real_run_bridge_execution_v0_1`
- ready bridge candidate can execute the local wrapper
- generated run has schema `sentigraph_opinion_ecosystem_run_v0_1`
- generated run keeps required boundary flags
- generated run keeps runtime side-effect flags false
- execution object records `minimum_real_run_executed = true`
- execution object records `dense_graph_called = false`
- blocked bridge does not execute wrapper
- bridge with blockers does not execute wrapper
- bridge requesting side effects does not execute wrapper
- bridge with missing candidate does not execute wrapper
- no package rows are parsed
- no package files are opened
- no Evidence Layer write occurs
- no production case or production `analysis_run` is created
- no dense graph function is called
- no frontend/API route is added
- no response text or generated public message appears
- forbidden influence/control fields are absent
- no raw identity fields are emitted
- no absolute private paths are emitted
- no real API / real LLM / collector call occurs

Suggested future test file:

`backend/app/tests/test_minimum_real_run_bridge_execution.py`

This is a future recommendation only. 8V-5 does not create tests.

## K. Forbidden Interpretations

Do not interpret this contract as:

- Evidence Layer import
- production case creation
- production `analysis_run` creation
- report runtime approval
- B-end report approval
- Sandbox/public event runtime approval
- public route approval
- dense graph direct-call approval
- official verification
- calibrated prediction
- causal proof
- truth score
- full-web coverage
- full-platform coverage
- generated public response authorization
- collector integration
- real API integration
- real LLM integration

The contract only defines how a future backend-only smoke may call the existing minimum real-run wrapper from a safe bridge candidate.
