# Sentigraph Report Candidate to Final Report Contract v0.1

## A. Contract Purpose

This contract defines a future backend-only local boundary object between:

- the safe 8V-10 local report candidate
- a future final-report-boundary checkpoint

The contract exists to keep the future 8V-12 implementation narrow:

- consume only a safe `sentigraph_dense_graph_report_candidate_v0_1` object
- create only a local `sentigraph_report_candidate_final_report_boundary_v0_1` boundary object
- preserve selected-sample-only limitations
- preserve human-review-required status
- keep Source 11 FinalSummaryReport runtime, export, B-end report, Sandbox, public event, frontend, routes, production, and public output blocked

This contract is not an implementation. It is not an API route. It is not frontend integration. It is not Source 11 FinalSummaryReport runtime. It is not report export. It is not public access or external delivery. It is not Evidence Layer import. It is not production analysis.

## B. Proposed Future Final-report-boundary Contract

Proposed schema:

```json
{
  "final_report_boundary_schema": "sentigraph_report_candidate_final_report_boundary_v0_1"
}
```

Proposed future object:

```json
{
  "final_report_boundary_id": "report_candidate_final_report_boundary_...",
  "final_report_boundary_schema": "sentigraph_report_candidate_final_report_boundary_v0_1",
  "final_report_boundary_status": "boundary_ready|blocked_metadata_contract|blocked_privacy_issue|blocked_requested_side_effect|blocked_forbidden_input|manual_review_required",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "report_candidate_id": "dense_graph_report_candidate_...",
  "integration_id": "generated_run_dense_graph_bridge_integration_...",
  "execution_id": "minimum_real_run_bridge_execution_...",
  "bridge_id": "staging_generated_run_bridge_...",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "input_source_kind": "dense_graph_report_candidate",
  "boundary_mode": "backend_only_local_final_report_boundary",
  "report_candidate_schema": "sentigraph_dense_graph_report_candidate_v0_1",
  "report_candidate_status": "candidate_ready",
  "dense_graph_integration_schema": "sentigraph_generated_run_dense_graph_bridge_integration_v0_1",
  "generated_run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
  "selected_sample_scope_note": "selected public sample only; not full-web, not full-platform, not full-thread",
  "dense_graph_proxy_summary": {},
  "report_candidate_summary": {},
  "candidate_section_outline": [],
  "coverage_limitations": [],
  "warnings": [],
  "blockers": [],
  "human_review_status": "required",
  "human_review_required": true,
  "source11_final_summary_report_runtime_used": false,
  "final_summary_report_created": false,
  "final_report_created": false,
  "b_end_report_runtime_generated": false,
  "sandbox_public_event_generated": false,
  "export_artifact_created": false,
  "download_package_created": false,
  "public_access_created": false,
  "external_delivery_performed": false,
  "generated_response_text": false,
  "public_route_created": false,
  "frontend_integration_approved": false,
  "route_ready": false,
  "frontend_ready": false,
  "production_ready": false,
  "export_ready": false,
  "public_ready": false,
  "customer_ready": false,
  "boundary_flags": {},
  "runtime_side_effects": {},
  "audit_refs": [],
  "downstream_policy": {}
}
```

Recommended future statuses:

- `boundary_ready`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_requested_side_effect`
- `blocked_forbidden_input`
- `manual_review_required`

`boundary_ready` means only that a local boundary object exists for human review. It does not mean final report runtime, export readiness, public readiness, customer readiness, production readiness, or Source 11 governance integration.

## C. Input Contract

Future 8V-12 may accept only a safe 8V-10 local report candidate object.

Required input identity:

- `report_candidate_id`
- `report_candidate_schema`
- `report_candidate_status`
- `created_at`
- `created_by`

Required upstream refs:

- `integration_id`
- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `generated_run_schema`
- `dense_graph_integration_schema`

Required input values:

- `report_candidate_schema = sentigraph_dense_graph_report_candidate_v0_1`
- `report_candidate_status = candidate_ready`
- `input_source_kind = generated_run_dense_graph_bridge_integration`
- `candidate_mode = backend_only_local_report_candidate`
- `report_candidate_created = true`
- `dense_graph_integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- `dense_graph_summary` present
- `report_candidate_summary` present
- `boundary_flags` present
- `runtime_side_effects` present and false
- `human_review_required = true`
- `final_report_created = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `export_artifact_created = false`
- `generated_response_text = false`
- `public_route_created = false`
- `frontend_integration_approved = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `public_ready = false`

Allowed input summaries:

- candidate title and scope
- dense graph proxy counts
- selected-sample coverage limitations
- warning and blocker summary
- boundary confirmation
- audit refs
- candidate section outline
- safe report interpretation summary

The future boundary helper must not open package files, parse rows, follow URLs, inspect private collector internals, read real exchange directories, or execute routes.

## D. Output Contract

Required output identity:

- `final_report_boundary_id`
- `final_report_boundary_schema`
- `final_report_boundary_status`
- `created_at`
- `created_by`

Required output upstream refs:

- `report_candidate_id`
- `integration_id`
- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`

Required output summaries:

- `selected_sample_scope_note`
- `dense_graph_proxy_summary`
- `report_candidate_summary`
- `candidate_section_outline`
- `coverage_limitations`
- `warnings`
- `blockers`
- `human_review_status`
- `audit_refs`
- `downstream_policy`

Required output false flags:

- `source11_final_summary_report_runtime_used = false`
- `final_summary_report_created = false`
- `final_report_created = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `export_artifact_created = false`
- `download_package_created = false`
- `public_access_created = false`
- `external_delivery_performed = false`
- `generated_response_text = false`
- `public_route_created = false`
- `frontend_integration_approved = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `public_ready = false`
- `customer_ready = false`

The output must not include raw row content, raw comments, raw author identifiers, actual author names, actual profile URLs, private paths, secrets, browser profile paths, collector internals, generated response text, public URLs, signed URLs, file paths for download, or artifact bytes.

## E. Boundary Flags

The future object must preserve these true boundary flags:

- `selected_sample_only`
- `not_full_web`
- `not_full_platform`
- `not_full_thread`
- `not_official_verification`
- `not_causal_proof`
- `not_prediction`
- `not_production_score`
- `human_review_required`
- `no_auto_execute`
- `no_generated_public_response`
- `not_source11_final_summary_report`
- `not_export_ready`
- `not_public_ready`
- `not_customer_ready`
- `not_production_ready`

These flags must be visible in any safe summary returned to future reviewers. They must not be removed or softened by final-report-boundary wording.

## F. Runtime Side-effect Flags

All future runtime side-effect flags must remain false:

- `called_real_api`
- `called_real_llm`
- `ran_collector`
- `accessed_private_collector`
- `read_real_exchange_dir`
- `fetched_url`
- `scraped_page`
- `parsed_evidence_items_file`
- `read_original_package_rows`
- `wrote_evidence_layer`
- `created_production_case`
- `created_production_analysis_run`
- `used_source11_final_summary_report_runtime`
- `generated_final_summary_report`
- `generated_b_end_report_runtime`
- `generated_sandbox_runtime`
- `generated_public_event_runtime`
- `generated_export_artifact`
- `generated_download_package`
- `generated_public_access`
- `performed_external_delivery`
- `generated_response_text`
- `created_public_route`
- `created_file_byte_route`
- `generated_public_url`
- `generated_signed_url`
- `uploaded_object_storage`
- `sent_email`
- `published_to_portal`
- `published_or_sent`
- `auto_executed`

If any side-effect flag is true or missing, the future helper must return a blocked status.

## G. Blockers / Warnings

Required blockers:

- missing report candidate id
- wrong report candidate schema
- report candidate status is not `candidate_ready`
- missing dense graph summary
- missing report candidate summary
- missing boundary flags
- missing runtime side-effect flags
- any runtime side-effect flag true
- requested Source 11 FinalSummaryReport runtime
- requested final report creation
- requested B-end report runtime
- requested Sandbox/public event runtime
- requested export artifact
- requested download package
- requested public URL or signed URL
- requested public route or file-byte route
- requested frontend integration
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested evidence row parsing
- requested original package row read
- requested real API, real LLM, provider, or collector execution
- requested URL fetch or scraping
- privacy, raw identity, private path, secret, or browser profile risk
- forbidden output field present

Required warnings:

- selected sample only
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- final-report-boundary object is not Source 11 FinalSummaryReport
- export, B-end, Sandbox, public event, public access, and delivery require separate future gates

## H. Audit Fields

Future 8V-12 should keep audit metadata safe and metadata-only.

Allowed audit fields:

- `audit_id`
- `audit_schema`
- `audit_action`
- `created_at`
- `created_by`
- `final_report_boundary_id`
- `report_candidate_id`
- upstream safe refs
- previous status
- new status
- blocker codes
- warning codes
- boundary flag summary
- runtime side-effect summary
- downstream policy summary

Audit must not include raw author identifiers, actual author names, actual profile URLs, private paths, row contents, secrets, browser profile paths, generated response text, artifact bytes, public URLs, signed URLs, or external delivery targets.

## I. Downstream Policy

The future final-report-boundary object must state:

- Source 11 FinalSummaryReport runtime requires a separate decision and explicit implementation approval
- export/download/package runtime requires a separate decision and explicit implementation approval
- public access / external delivery requires a separate decision and explicit implementation approval
- B-end report runtime requires a separate decision and explicit implementation approval
- Sandbox/public event runtime requires a separate decision and explicit implementation approval
- frontend/API route integration requires a separate decision and explicit implementation approval
- Evidence Layer write and production case creation are not allowed by this boundary
- production `analysis_run` creation is not allowed by this boundary
- generated response text and platform action are not allowed by this boundary

The downstream policy must keep all readiness values false:

- `source11_ready = false`
- `export_ready = false`
- `download_ready = false`
- `public_access_ready = false`
- `external_delivery_ready = false`
- `b_end_ready = false`
- `sandbox_ready = false`
- `public_event_ready = false`
- `frontend_ready = false`
- `route_ready = false`
- `production_ready = false`
- `customer_ready = false`

## J. Future Tests

Future 8V-12 should add tests proving:

- safe 8V-10 report candidate creates a boundary object with schema `sentigraph_report_candidate_final_report_boundary_v0_1`
- boundary object keeps `human_review_required = true`
- boundary object keeps Source 11 FinalSummaryReport runtime unused
- boundary object keeps final summary report, B-end, Sandbox/public event, export, download, public access, external delivery, route, frontend, production, and customer readiness false
- boundary object keeps runtime side-effect flags false
- boundary object contains only safe summary fields
- missing report candidate summary blocks
- missing dense graph summary blocks
- wrong report candidate schema blocks
- non-ready report candidate status blocks
- any requested side effect blocks
- forbidden fields block
- privacy, raw identity, private path, secret, or browser profile risk blocks
- generated response text is not produced
- Source 11 runtime is not called
- no API route is added
- no frontend files are changed
- no Evidence Layer write occurs
- no production case or production `analysis_run` is created
- no provider, collector, real API, real LLM, URL fetch, or scraping occurs

Recommended future targeted validation:

- new backend tests for the boundary helper
- existing dense graph report candidate bridge tests
- existing generated-run / dense graph integration tests
- `git diff --check`
- py_compile for touched backend files

Full test suite and frontend build may be run only if the future implementation touches shared code or if the user requests full validation.

## K. Forbidden Interpretations

Do not interpret this contract as:

- Source 11 FinalSummaryReport integration approval
- final report runtime approval
- final report artifact generation
- B-end report generation
- Sandbox/public event generation
- export generation
- download package generation
- public access or signed URL generation
- external delivery
- frontend or route readiness
- public/customer readiness
- production readiness
- Evidence Layer import
- production case creation
- production `analysis_run` creation
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- prediction
- production score
- generated response text
- automatic action

Provider output and local report candidates remain evidence-derived governance artifacts, not truth, not official verification, and not automatic public/customer output.
