# Sentigraph Generated-run to Dense Graph Integration Contract v0.1

## A. Contract Purpose

This contract defines a future controlled backend-only integration object between:

- a safe generated run produced through the 8V-6 bridge execution path
- the existing dense graph integration/helper surface

The contract exists to keep the future 8V-8 implementation narrow:

- consume only a safe 8V-6 execution object and generated run
- call dense graph only in a backend-only controlled smoke
- preserve selected-sample and human-review boundaries
- keep frontend, route, report, Sandbox, public event, production, and public-output readiness false

This contract is not an implementation. It is not a route. It is not frontend integration. It is not Evidence Layer import. It is not production analysis. It is not report generation.

## B. Proposed Future Integration Contract

Proposed schema:

```json
{
  "integration_schema": "sentigraph_generated_run_dense_graph_bridge_integration_v0_1"
}
```

Proposed future object:

```json
{
  "integration_id": "generated_run_dense_graph_bridge_integration_...",
  "integration_schema": "sentigraph_generated_run_dense_graph_bridge_integration_v0_1",
  "integration_status": "integrated_backend_dense_graph_preview|blocked|manual_review_required",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "execution_id": "minimum_real_run_bridge_execution_...",
  "bridge_id": "staging_generated_run_bridge_...",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "input_source_kind": "minimum_real_run_bridge_execution",
  "integration_mode": "controlled_backend_only_generated_run_dense_graph",
  "generated_run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
  "dense_graph_executed": true,
  "frontend_integration_approved": false,
  "route_changed": false,
  "api_route_added": false,
  "report_generated": false,
  "sandbox_public_event_generated": false,
  "dense_graph_integration": {},
  "dense_graph_summary": {},
  "boundary_flags": {},
  "runtime_side_effects": {},
  "warnings": [],
  "blockers": [],
  "audit_refs": [],
  "downstream_allowed_actions": [],
  "downstream_blocked_actions": []
}
```

Recommended future statuses:

- `integrated_backend_dense_graph_preview`
- `blocked_generated_run_not_ready`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_requested_side_effect`
- `blocked_forbidden_input`
- `manual_review_required`

## C. Input Contract

Future 8V-8 may accept only a safe 8V-6 execution object containing a generated run.

Required execution object fields:

- `execution_id`
- `execution_schema`
- `execution_status`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `input_source_kind`
- `execution_mode`
- `metadata_only`
- `evidence_rows_parsed`
- `minimum_real_run_executed`
- `dense_graph_called`
- `generated_run`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`

Required execution object values:

- `execution_schema = sentigraph_minimum_real_run_bridge_execution_v0_1`
- `execution_status = executed_local_minimum_real_run`
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `minimum_real_run_executed = true`
- `dense_graph_called = false`
- all runtime side-effect flags false
- no blockers

Required generated-run values:

- `run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- `human_review_required = true`
- selected-sample / controlled metadata scoped
- `coefficient_source = mock_default` or current equivalent
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`
- boundary flags present
- runtime side-effect flags false
- no response text
- no public output
- no privacy/security/path/side-effect blockers

The future integration must not open package files, parse rows, follow URLs, inspect private collector internals, read real exchange directories, or execute routes.

## D. Output Contract

Required integration identity:

- `integration_id`
- `integration_schema`
- `integration_status`
- `created_at`
- `created_by`

Required upstream refs:

- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`

Required integration boundary:

- `input_source_kind`
- `integration_mode`
- `generated_run_schema`
- `dense_graph_executed`
- `frontend_integration_approved`
- `route_changed`
- `api_route_added`
- `report_generated`
- `sandbox_public_event_generated`
- `boundary_flags`
- `runtime_side_effects`

Required dense graph fields:

- `dense_graph_integration`
- `dense_graph_summary`

The dense graph summary may include:

- `dense_graph_attached`
- `people_cluster_proxy_count`
- `influence_core_proxy_count`
- `content_aggregate_proxy_count`
- `echobox_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode`
- `frontend_ready = false`
- `route_ready = false` for the 8V-8 smoke
- `production_ready = false`

Required downstream policy:

- `downstream_allowed_actions`
- `downstream_blocked_actions`
- `warnings`
- `blockers`
- `audit_refs`

## E. Boundary Flags

The future object must keep these boundary flags explicit:

```json
{
  "selected_sample_only": true,
  "controlled_generated_run_only": true,
  "metadata_only_upstream": true,
  "anonymous_aggregate_only": true,
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
  "no_generated_public_response": true,
  "frontend_ready": false,
  "route_ready": false,
  "production_ready": false
}
```

Missing or unsafe boundary flags should block the future smoke or mark it manual-review-required.

## F. Runtime Side-effect Flags

All runtime side-effect flags must remain false:

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

Allowed integration marker:

```json
{
  "dense_graph_executed": true
}
```

This marker means only that a backend-only dense graph preview was produced from a safe generated run. It does not mean frontend readiness, route readiness, production readiness, report generation, public event generation, or public access.

## G. Blockers / Warnings

Hard blockers:

- execution schema not recognized
- execution status not ready
- generated run missing
- generated-run schema not recognized
- generated-run boundary flags missing
- runtime side-effect flag not false
- generated-run blocker indicates privacy/security/path/side-effect risk
- forbidden active field present
- raw author identifier present
- actual author name value present
- actual profile URL value present
- private message present
- secret-like field present
- private or absolute path present
- requested evidence row parsing
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested route or frontend integration
- requested B-end report
- requested Sandbox/public event
- requested generated response text
- requested publish/send/post/execute action
- requested real API, real LLM, collector, private project access, URL fetch, or scrape

Warnings:

- generated-run status is manual-review-required
- validation status is warn
- evidence/sample count is low
- source coverage is weak
- unknown or future platform remains manual-review-only
- dense graph attachment is degraded
- dense graph values are deterministic, mock/default, and uncalibrated
- empirical validation is not started

Warnings do not upgrade trust and do not make the output production-ready.

## H. Audit Fields

Future integration should carry audit metadata:

- `audit_refs`
- `source_execution_audit_refs`
- `integration_created_by`
- `integration_created_at`
- `integration_reason`
- `input_execution_summary`
- `input_generated_run_summary`
- `boundary_confirmation_snapshot`
- `blocked_action_snapshot`
- `dense_graph_helper_name`
- `dense_graph_helper_version` if available

Audit must not include raw author identifiers, private paths, row contents, secrets, browser profile paths, public response text, or raw comment payloads.

## I. Downstream Policy

Allowed after future 8V-8:

- inspect backend dense graph preview summary
- validate boundary flags
- validate runtime side-effect flags
- decide whether a later backend route/UI decision is appropriate
- decide whether frontend integration remains deferred

Blocked after future 8V-8 unless separately approved:

- frontend integration
- route change
- public route
- B-end/customer route
- Evidence Layer write
- production case
- production `analysis_run`
- report generation
- B-end report runtime
- Sandbox/public event runtime
- generated public response text
- public access or delivery
- collector job
- row parsing
- real API
- real LLM
- URL fetch or scraping
- algorithm/weight recalibration

The dense graph output remains internal, selected-sample-only, anonymous aggregate/proxy, and human-review-required.

## J. Future Tests

Future 8V-8 tests should verify:

- integration object has schema `sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- safe 8V-6 execution object can enter dense graph integration
- generated-run schema and boundaries are validated before dense graph call
- blocked generated run does not call dense graph
- execution with missing generated run does not call dense graph
- execution with side-effect flag true blocks
- execution requesting route/frontend/report/public output blocks
- forbidden active fields block without exposing values
- runtime side-effect flags remain false
- dense graph marker records only backend preview execution
- output summary keeps `frontend_ready = false`
- output summary keeps `route_ready = false` for the 8V-8 smoke
- output summary keeps `production_ready = false`
- no Evidence Layer write
- no production case or production `analysis_run`
- no B-end report
- no Sandbox/public event runtime
- no generated response text
- no package rows are parsed
- no package files are opened
- no real API / real LLM / collector call occurs

Suggested future test file:

`backend/app/tests/test_generated_run_dense_graph_bridge_integration.py`

This is a future recommendation only. 8V-7 does not create tests.

## K. Forbidden Interpretations

Do not interpret this contract as:

- frontend dense graph approval
- route approval
- public route approval
- B-end/customer route approval
- Evidence Layer import
- production case creation
- production `analysis_run` creation
- report runtime approval
- B-end report approval
- Sandbox/public event runtime approval
- public access approval
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
- algorithm/weight recalibration

The contract only defines how a future backend-only smoke may connect a safe 8V-6 generated run to the existing dense graph integration surface.
