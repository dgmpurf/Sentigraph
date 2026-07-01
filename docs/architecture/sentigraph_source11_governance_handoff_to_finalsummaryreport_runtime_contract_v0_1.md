# Sentigraph Source 11 Governance Handoff to FinalSummaryReport Runtime Contract v0.1

## A. Contract Purpose

This contract defines the future backend-only adapter boundary between:

- a safe `sentigraph_final_report_boundary_source11_governance_handoff_v0_1` object
- a later possible controlled local `sentigraph_final_summary_report_v1` runtime path

The contract exists to keep future 8V-16 narrow:

- consume only a safe 8V-14 Source 11 governance handoff marker
- preserve separation from export/download/public-access runtimes
- preserve B-end, Sandbox, public event, frontend, route, Evidence Layer, production case, and production `analysis_run` non-approval
- preserve no real API, no real LLM, no provider/collector execution, no URL fetch, and no scraping boundaries

This contract is not an implementation. It is not a route. It is not frontend integration. It is not export runtime. It is not public access or external delivery. It is not Evidence Layer import. It is not production analysis.

## B. Proposed Future FinalSummaryReport Runtime Adapter Boundary

Selected future contract direction:

`sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1`

Future 8V-16 may either:

1. create a local adapter-smoke object proving the safe handoff can feed the FinalSummaryReport runtime boundary, or
2. create a local `sentigraph_final_summary_report_v1` object only if Source 11 runtime inputs can be satisfied without breaking any stop rule.

If a local FinalSummaryReport object is created, it must still be:

- local-only
- backend-only
- selected-sample-derived
- human-review-required
- not export-ready
- not public-ready
- not customer-ready
- not production-ready
- not B-end-ready
- not Sandbox-ready
- not public-event-ready

Future 8V-16 must not create export artifacts, download packages, public access, external delivery, B-end reports, Sandbox/public events, routes, frontend integration, Evidence Layer writes, production cases, production `analysis_run` records, generated response text, public URLs, signed URLs, file-byte routes, or platform actions.

## C. Input Contract

Future 8V-16 may accept only a safe 8V-14 Source 11 governance handoff object.

Required input values:

- `source11_governance_handoff_schema = sentigraph_final_report_boundary_source11_governance_handoff_v0_1`
- `source11_governance_handoff_status = handoff_ready_for_manual_source11_governance_review`
- `source11_governance_handoff_created = true`
- `input_source_kind = final_report_boundary`
- `handoff_mode = backend_only_local_source11_governance_handoff`
- `final_report_boundary_schema = sentigraph_report_candidate_final_report_boundary_v0_1`
- `final_report_boundary_status = boundary_ready`
- `report_candidate_schema = sentigraph_dense_graph_report_candidate_v0_1`
- `dense_graph_integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- `generated_run_schema = sentigraph_opinion_ecosystem_run_v0_1`
- `boundary_flags` present
- `runtime_side_effects` present and all false
- `human_review_required = true`
- `source11_manual_review_ready = true`
- `source11_runtime_ready = false`
- `source11_final_summary_report_runtime_used = false`
- `source11_runtime_called = false`
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

- `source11_governance_handoff_id`
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
- `final_report_boundary_schema`

Allowed safe summaries:

- selected-sample scope note
- final-report-boundary summary
- Source 11 governance review summary
- compatibility notes
- limitations
- warning summary
- blocker summary
- human review status
- boundary confirmation
- audit refs
- downstream policy summary

The future adapter must not open package files, parse rows, inspect private collector internals, read real exchange dirs, follow URLs, execute routes, call real APIs, call real LLMs, or invoke export/download/public-access runtime.

## D. Output Contract

If 8V-16 creates an adapter-smoke object, required output identity should include:

- `adapter_schema`
- `adapter_id`
- `adapter_status`
- `created_at`
- `created_by`

If 8V-16 creates a local FinalSummaryReport object, it must use:

- `schema = sentigraph_final_summary_report_v1`
- `status = final_summary_report_created`

Required upstream refs for either output:

- `source11_governance_handoff_id`
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

- `source_and_scope`
- `report_sections` or `adapter_section_map`
- `boundary_block`
- `coverage_limitations`
- `warnings`
- `blockers`
- `human_review_status`
- `boundary_flags`
- `runtime_side_effects`
- `audit_refs`
- `downstream_policy`

Required Source 11 and downstream false flags:

- `source11_runtime_called = false` for adapter-smoke objects before actual runtime call
- `source11_final_summary_report_runtime_used = false` unless future 8V-16 explicitly creates local FinalSummaryReport through the approved runtime boundary
- `export_artifact_created = false`
- `download_package_created = false`
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

Future 8V-16 output must keep these true boundary flags:

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
- `local_final_summary_report_only`
- `not_export_ready`
- `not_public_ready`
- `not_customer_ready`
- `not_production_ready`
- `not_b_end_ready`
- `not_sandbox_ready`
- `not_public_event_ready`

If 8V-16 remains adapter-contract only and does not create FinalSummaryReport, it must also keep:

- `source11_runtime_not_used`
- `final_summary_report_not_created`

If 8V-16 creates a local FinalSummaryReport object, it must replace those with explicit local-only boundaries:

- `source11_runtime_used_only_for_local_finalsummaryreport_boundary`
- `final_summary_report_created_local_only`
- `downstream_gates_required`

## F. Runtime Side-effect Flags

All unrelated runtime side-effect flags must remain false:

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

If future 8V-16 creates a local FinalSummaryReport, only the narrowly scoped local final-summary-report runtime flag may become true. Export, public, B-end, Sandbox, Evidence Layer, production, provider, collector, LLM, URL fetch, and scraping flags must remain false.

## G. Blockers / Warnings

Required blockers:

- missing Source 11 governance handoff id
- wrong Source 11 governance handoff schema
- handoff status not `handoff_ready_for_manual_source11_governance_review`
- handoff not created
- missing boundary flags
- missing runtime side-effect flags
- any disallowed runtime side-effect flag true
- requested export runtime or artifact
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
- FinalSummaryReport is local-only if created
- export/download/public-access not approved
- B-end, Sandbox, public event, frontend, route, production, and customer outputs require separate future gates

## H. Audit Fields

Allowed audit fields for future 8V-16:

- `audit_id`
- `audit_schema`
- `audit_action`
- `created_at`
- `created_by`
- `adapter_id` or `final_summary_report_id`
- `source11_governance_handoff_id`
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

Future 8V-16 output must state:

- FinalSummaryReport export requires a later decision and explicit implementation approval.
- Export/download/package runtime requires a later decision and explicit implementation approval.
- Public access / external delivery requires a later decision and explicit implementation approval.
- B-end report runtime requires a later decision and explicit implementation approval.
- Sandbox/public event runtime requires a later decision and explicit implementation approval.
- Frontend/API route integration requires a later decision and explicit implementation approval.
- Evidence Layer write is not allowed by this adapter.
- Production case creation is not allowed by this adapter.
- Production `analysis_run` creation is not allowed by this adapter.
- Generated response text and platform action are not allowed by this adapter.

Required downstream readiness:

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

Future 8V-16 should add tests proving:

- safe 8V-14 handoff is the only accepted input
- wrong handoff schema blocks
- non-ready handoff status blocks
- missing boundary flags block
- missing runtime side-effect flags block
- any requested export/download/public/B-end/Sandbox/route/frontend side effect blocks
- forbidden actual fields or sentinel values block or are omitted
- no file IO is required
- no `evidence_items.jsonl` or `evidence_items.csv` is parsed
- no private collector files or real exchange dirs are read
- no routes or frontend files are changed
- local FinalSummaryReport, if created, keeps all downstream flags false
- no export artifacts, download packages, public access, external delivery, B-end report, Sandbox/public event, Evidence Layer, production case, or production `analysis_run` are created

Recommended future validation:

- focused new adapter tests
- existing 8V-14 Source 11 governance handoff tests
- existing 8V-12 final-report-boundary tests
- existing Source 11 FinalSummaryReport tests only if the future adapter touches that runtime boundary
- py_compile for touched backend files
- `git diff --check`

Do not require full pytest or frontend build unless future implementation touches shared code, routes, frontend, or the user explicitly requests full validation.

## K. Forbidden Interpretations

Do not interpret this contract as:

- immediate Source 11 FinalSummaryReport runtime approval in 8V-15
- export approval
- download package approval
- public access approval
- signed URL approval
- external delivery approval
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

The future adapter is only a tightly bounded backend transition from the 8V governance handoff to the Source 11 FinalSummaryReport boundary. It must not be treated as export, delivery, public access, B-end, Sandbox, public event, or production promotion.
