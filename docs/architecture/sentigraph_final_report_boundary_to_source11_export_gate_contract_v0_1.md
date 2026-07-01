# Sentigraph Final Report Boundary to Source 11 / Export Gate Contract v0.1

## A. Contract Purpose

This contract defines a future backend-only local governance handoff boundary between:

- a safe `sentigraph_report_candidate_final_report_boundary_v0_1` object
- a later possible manual review against existing Source 11 report governance

The contract exists to keep future 8V-14 narrow:

- consume only a safe 8V-12 final-report-boundary object
- create only a local governance handoff/readiness object
- preserve separation from Source 11 FinalSummaryReport runtime
- preserve export/download/public-access non-approval
- preserve B-end, Sandbox, public event, frontend, route, Evidence Layer, production case, and production `analysis_run` non-approval

This contract is not an implementation. It is not a route. It is not frontend integration. It is not Source 11 FinalSummaryReport runtime. It is not export runtime. It is not public access or external delivery. It is not Evidence Layer import. It is not production analysis.

## B. Proposed Future Handoff or Separation Contract

Selected future contract:

`sentigraph_final_report_boundary_source11_governance_handoff_v0_1`

Proposed object:

```json
{
  "handoff_schema": "sentigraph_final_report_boundary_source11_governance_handoff_v0_1",
  "handoff_id": "final_report_boundary_source11_handoff_...",
  "handoff_status": "handoff_ready|blocked_metadata_contract|blocked_privacy_issue|blocked_requested_side_effect|blocked_forbidden_input|manual_review_required",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "final_report_boundary_id": "report_candidate_final_report_boundary_...",
  "report_candidate_id": "dense_graph_report_candidate_...",
  "integration_id": "generated_run_dense_graph_bridge_integration_...",
  "execution_id": "minimum_real_run_bridge_execution_...",
  "bridge_id": "staging_generated_run_bridge_...",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "input_source_kind": "final_report_boundary",
  "handoff_mode": "backend_only_local_source11_governance_handoff",
  "final_report_boundary_schema": "sentigraph_report_candidate_final_report_boundary_v0_1",
  "final_report_boundary_status": "boundary_ready",
  "source11_target": {
    "source11_final_summary_report_runtime_candidate": true,
    "source11_runtime_invoked_now": false,
    "final_summary_report_created_now": false,
    "export_gate_invoked_now": false,
    "download_package_invoked_now": false,
    "public_access_invoked_now": false
  },
  "safe_boundary_summary": {},
  "source11_mapping_summary": {},
  "coverage_limitations": [],
  "warnings": [],
  "blockers": [],
  "human_review_status": "required",
  "human_review_required": true,
  "boundary_flags": {},
  "runtime_side_effects": {},
  "audit_refs": [],
  "downstream_policy": {}
}
```

Alternative fallback contract:

`sentigraph_final_report_boundary_source11_separation_hardening_v0_1`

The fallback object should be used only if future implementation risk makes handoff readiness too ambiguous. It should prove separation from Source 11 and export/public gates rather than creating a handoff candidate.

## C. Input Contract

Future 8V-14 may accept only a safe 8V-12 local final-report-boundary object.

Required input values:

- `final_report_boundary_schema = sentigraph_report_candidate_final_report_boundary_v0_1`
- `final_report_boundary_status = boundary_ready`
- `input_source_kind = dense_graph_report_candidate`
- `boundary_mode = backend_only_local_final_report_boundary`
- `final_report_boundary_created = true`
- `report_candidate_schema = sentigraph_dense_graph_report_candidate_v0_1`
- `report_candidate_status = candidate_ready`
- `dense_graph_integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- `generated_run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- `boundary_flags` present
- `runtime_side_effects` present and false
- `human_review_required = true`
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
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `public_ready = false`
- `customer_ready = false`

Allowed refs:

- `final_report_boundary_id`
- `report_candidate_id`
- `integration_id`
- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `generated_run_schema`
- `report_candidate_schema`
- `dense_graph_integration_schema`

Allowed safe summaries:

- selected-sample scope note
- dense graph proxy summary
- report candidate summary
- candidate section outline
- coverage limitations
- warning summary
- blocker summary
- human review status
- boundary confirmation
- audit refs
- downstream policy summary

The future helper must not open package files, parse rows, call Source 11 runtime, call export/download/public-access runtime, inspect private collector internals, read real exchange dirs, follow URLs, or execute routes.

## D. Output Contract

Required output identity:

- `handoff_schema`
- `handoff_id`
- `handoff_status`
- `created_at`
- `created_by`

Required upstream refs:

- `final_report_boundary_id`
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

- `source11_target`
- `safe_boundary_summary`
- `source11_mapping_summary`
- `coverage_limitations`
- `warnings`
- `blockers`
- `human_review_status`
- `boundary_flags`
- `runtime_side_effects`
- `audit_refs`
- `downstream_policy`

Required Source 11 and downstream false flags:

- `source11_runtime_invoked_now = false`
- `source11_final_summary_report_runtime_used = false`
- `final_summary_report_created_now = false`
- `final_summary_report_created = false`
- `final_report_created = false`
- `export_gate_invoked_now = false`
- `export_artifact_created = false`
- `download_package_invoked_now = false`
- `download_package_created = false`
- `public_access_invoked_now = false`
- `public_access_created = false`
- `external_delivery_performed = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `public_ready = false`
- `customer_ready = false`

The output must not include raw row content, raw comments, raw author identifiers, actual author names, actual profile URLs, private paths, secrets, browser profile paths, collector internals, generated response text, public URLs, signed URLs, file paths for download, artifact bytes, or delivery targets.

## E. Boundary Flags

The future object must keep these true boundary flags:

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
- `source11_runtime_not_invoked`
- `final_summary_report_not_created`
- `export_not_created`
- `download_not_created`
- `public_access_not_created`
- `external_delivery_not_performed`
- `not_public_ready`
- `not_customer_ready`
- `not_production_ready`

These flags must remain visible to future reviewers and must not be softened by handoff wording.

## F. Runtime Side-effect Flags

All runtime side-effect flags must remain false:

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
- `generated_final_report_artifact`
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

If any flag is true or missing, the future helper must block.

## G. Blockers / Warnings

Required blockers:

- missing final-report-boundary id
- wrong final-report-boundary schema
- final-report-boundary status not `boundary_ready`
- final-report-boundary not created
- missing boundary flags
- missing runtime side-effect flags
- any runtime side-effect flag true
- requested Source 11 FinalSummaryReport runtime
- requested FinalSummaryReport creation
- requested final report artifact
- requested export gate/runtime/artifact
- requested download package
- requested public access
- requested external delivery
- requested B-end report runtime
- requested Sandbox/public event runtime
- requested route/frontend/API behavior
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested evidence row parsing
- requested provider, collector, real API, or real LLM
- requested URL fetch or scraping
- forbidden actual field or value present
- privacy, raw identity, private path, secret, or browser profile risk

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
- Source 11 runtime not invoked
- FinalSummaryReport not created
- export/download/public-access not approved
- B-end, Sandbox, public event, frontend, route, production, and customer outputs require separate future gates

## H. Audit Fields

Allowed audit fields:

- `audit_id`
- `audit_schema`
- `audit_action`
- `created_at`
- `created_by`
- `handoff_id`
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

The future handoff object must state:

- Source 11 FinalSummaryReport runtime requires a later decision and explicit implementation approval
- Source 11 store/schema/route changes require a later decision and explicit implementation approval
- export/download/package runtime requires a later decision and explicit implementation approval
- public access / external delivery requires a later decision and explicit implementation approval
- B-end report runtime requires a later decision and explicit implementation approval
- Sandbox/public event runtime requires a later decision and explicit implementation approval
- frontend/API route integration requires a later decision and explicit implementation approval
- Evidence Layer write is not allowed by this handoff
- production case creation is not allowed by this handoff
- production `analysis_run` creation is not allowed by this handoff
- generated response text and platform action are not allowed by this handoff

Required downstream readiness:

- `source11_runtime_ready = false`
- `final_summary_report_ready = false`
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

Future 8V-14 should add tests proving:

- safe 8V-12 boundary creates `sentigraph_final_report_boundary_source11_governance_handoff_v0_1`
- Source 11 runtime is not invoked
- FinalSummaryReport is not created
- export/download/public-access runtimes are not invoked
- B-end, Sandbox, public event, route, frontend, production, and customer readiness remain false
- runtime side-effect flags remain false
- selected-sample and human-review boundaries survive
- wrong final-report-boundary schema blocks
- non-ready boundary status blocks
- missing boundary flags block
- missing runtime side-effect flags block
- any requested Source 11/export/public/B-end/Sandbox/route/frontend side effect blocks
- forbidden actual fields or sentinel values block or are omitted
- no file IO is required
- no `evidence_items.jsonl` or `evidence_items.csv` is parsed
- no routes or frontend files are changed

Recommended future validation:

- focused new handoff tests
- existing 8V-12 final-report-boundary tests
- nearby 8V-10 report candidate tests
- py_compile for touched backend files
- `git diff --check`

Do not require full pytest or frontend build unless future implementation touches shared code or the user explicitly requests full validation.

## K. Forbidden Interpretations

Do not interpret this contract as:

- Source 11 FinalSummaryReport runtime approval
- FinalSummaryReport creation approval
- final report artifact generation
- export generation
- download package generation
- public access or signed URL generation
- external delivery
- B-end report generation
- Sandbox/public event generation
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
- automatic platform action

The handoff object is only a governance-readiness marker. It is not a report, not an export, not a public/customer artifact, and not a production data promotion.
