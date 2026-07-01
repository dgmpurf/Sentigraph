# Sentigraph Download/Public Access Boundary to Final Delivery Contract v0.1

## A. Contract Purpose

This contract defines the future backend-only boundary between:

- a safe `sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1` local download/public-access boundary/readiness marker
- a later possible local final-delivery boundary/readiness marker

The contract exists to keep future 8V-24 narrow:

- consume only a safe 8V-22 local download/public-access boundary object
- preserve separation from final-delivery runtime
- preserve separation from customer delivery
- preserve separation from download/package runtime
- preserve separation from public-access runtime
- preserve separation from external-delivery runtime
- preserve separation from ZIP/package generation
- preserve separation from public URL and signed URL generation
- preserve separation from file-byte routes
- preserve separation from object storage upload, email sending, and portal publication
- preserve B-end, Sandbox, public event, frontend, route, Evidence Layer, production case, and production `analysis_run` non-approval
- preserve no real API, no real LLM, no provider/collector execution, no URL fetch, and no scraping boundaries

This contract is not an implementation. It is not a route. It is not frontend integration. It is not final delivery. It is not customer delivery. It is not a download package. It is not ZIP generation. It is not a public URL or signed URL. It is not public access or external delivery. It is not B-end report generation. It is not Sandbox/public event generation. It is not Evidence Layer import. It is not production analysis.

## B. Proposed Future Final-delivery Boundary/readiness Contract

Selected future contract direction:

`sentigraph_download_public_access_boundary_final_delivery_boundary_v0_1`

Future 8V-24 may create only a local boundary/readiness object proving that a safe local download/public-access boundary marker can be considered by a later final-delivery runtime review.

The future object may state:

- final-delivery review may be considered later
- human review remains required
- selected-sample boundaries remain visible
- final-delivery runtime is not called
- public-access runtime is not called
- external-delivery runtime is not called
- download/package runtime is not called
- ZIP/package/download files are not generated
- public URL is not generated
- signed URL is not generated
- file-byte route is not created
- public access is not created
- external delivery is not performed
- customer delivery is not created
- object storage is not uploaded
- email is not sent
- portal is not published
- B-end, Sandbox, public event, frontend, route, customer, public, and production readiness remain false

The future object must not create file content, runtime file paths, package paths, ZIPs, download links, public URLs, signed URLs, file-byte routes, public access, external delivery, final delivery, customer delivery, object storage uploads, email deliveries, portal publications, B-end reports, Sandbox output, public event output, route/frontend behavior, Evidence Layer writes, production case, production `analysis_run`, generated response text, or platform action.

## C. Input Contract

Future 8V-24 may accept only a safe 8V-22 local download/public-access boundary/readiness marker.

Required input values:

- `download_public_access_boundary_schema = sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1`
- `download_public_access_boundary_status = download_public_access_boundary_ready_for_manual_review`
- `download_public_access_boundary_created = true`
- `created_local_download_public_access_boundary = true`
- `input_source_kind = export_artifact_boundary`
- `boundary_mode = backend_only_local_download_public_access_boundary_readiness_smoke`
- `export_artifact_boundary_schema = sentigraph_export_gate_handoff_export_artifact_boundary_v0_1`
- `export_artifact_boundary_status = export_artifact_boundary_ready_for_manual_review`
- `export_artifact_boundary_created = true`
- `created_local_export_artifact_boundary = true`
- `export_gate_handoff_schema = sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1`
- `export_gate_handoff_status = export_gate_handoff_ready_for_manual_review`
- `export_gate_handoff_created = true`
- `created_local_export_gate_handoff = true`
- `final_summary_report_created = true`
- `final_summary_report_created_local_only = true`
- `local_final_summary_report_only = true`
- `human_review_required = true`
- `download_package_runtime_used = false`
- `called_download_package_runtime = false`
- `public_access_runtime_used = false`
- `called_public_access_runtime = false`
- `external_delivery_runtime_used = false`
- `called_external_delivery_runtime = false`
- `download_package_created = false`
- `generated_zip_package = false`
- `public_url_created = false`
- `signed_url_created = false`
- `public_access_created = false`
- `external_delivery_performed = false`
- `file_byte_route_created = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- `frontend_integration_approved = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `download_ready = false`
- `public_ready = false`
- `public_access_ready = false`
- `external_delivery_ready = false`
- `customer_ready = false`
- `b_end_ready = false`
- `sandbox_ready = false`
- `public_event_ready = false`
- `boundary_flags` present
- `runtime_side_effects` present and unrelated side effects false

Allowed refs:

- `download_public_access_boundary_id`
- `export_artifact_boundary_id`
- `export_gate_handoff_id`
- `adapter_id`
- `final_summary_report_id`
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

Allowed safe summaries:

- `source_and_scope`
- `download_public_access_boundary_readiness_summary`
- `export_artifact_boundary_summary`
- `export_gate_handoff_summary`
- `boundary_block`
- `coverage_limitations`
- warning summary
- blocker summary
- human review status
- audit refs
- downstream policy summary

The future boundary must not open package files, parse rows, inspect private collector internals, read real exchange dirs, follow URLs, execute routes, call real APIs, call real LLMs, or invoke final-delivery, download/public-access, external-delivery, B-end, Sandbox, Evidence Layer, production case, or production `analysis_run` runtime.

## D. Output Contract

If future 8V-24 creates a boundary/readiness object, required output identity should include:

- `final_delivery_boundary_schema = sentigraph_download_public_access_boundary_final_delivery_boundary_v0_1`
- `final_delivery_boundary_id`
- `final_delivery_boundary_status`
- `created_at`
- `created_by`

Required ready status:

- `final_delivery_boundary_status = final_delivery_boundary_ready_for_manual_review`

Required upstream refs:

- `download_public_access_boundary_id`
- `export_artifact_boundary_id`
- `export_gate_handoff_id`
- `adapter_id`
- `final_summary_report_id`
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
- `download_public_access_boundary_summary`
- `final_delivery_boundary_readiness_summary`
- `boundary_block`
- `coverage_limitations`
- `warnings`
- `blockers`
- `human_review_status`
- `boundary_flags`
- `runtime_side_effects`
- `audit_refs`
- `downstream_policy`

Blocked statuses should include:

- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_requested_side_effect`
- `blocked_forbidden_input`
- `blocked_final_delivery_runtime_side_effect_risk`
- `manual_review_required`

Required false output flags:

- `final_delivery_runtime_used = false`
- `called_final_delivery_runtime = false`
- `public_access_runtime_used = false`
- `called_public_access_runtime = false`
- `external_delivery_runtime_used = false`
- `called_external_delivery_runtime = false`
- `download_package_runtime_used = false`
- `called_download_package_runtime = false`
- `download_package_created = false`
- `generated_zip_package = false`
- `public_url_created = false`
- `signed_url_created = false`
- `public_access_created = false`
- `external_delivery_performed = false`
- `final_delivery_performed = false`
- `customer_delivery_created = false`
- `file_byte_route_created = false`
- `object_storage_uploaded = false`
- `email_sent = false`
- `portal_published = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- `frontend_integration_approved = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `download_ready = false`
- `public_ready = false`
- `public_access_ready = false`
- `external_delivery_ready = false`
- `customer_ready = false`
- `b_end_ready = false`
- `sandbox_ready = false`
- `public_event_ready = false`

The output must not include raw row content, raw comments, raw author identifiers, actual author names, actual profile URLs, private paths, secrets, browser profile paths, collector internals, generated response text, artifact bytes, file paths, local runtime paths, package paths, public URLs, signed URLs, download URLs, file-byte routes, object storage targets, email delivery targets, portal targets, customer delivery targets, or external delivery targets.

## E. Boundary Flags

Future 8V-24 output must keep these true boundary flags:

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
- `export_gate_handoff_only`
- `export_artifact_boundary_only`
- `download_public_access_boundary_only`
- `final_delivery_boundary_only`
- `download_package_runtime_not_used`
- `public_access_runtime_not_used`
- `external_delivery_runtime_not_used`
- `final_delivery_runtime_not_used`
- `download_package_not_created`
- `zip_package_not_generated`
- `public_url_not_created`
- `signed_url_not_created`
- `file_byte_route_not_created`
- `public_access_not_created`
- `external_delivery_not_performed`
- `final_delivery_not_performed`
- `customer_delivery_not_created`
- `object_storage_not_uploaded`
- `email_not_sent`
- `portal_not_published`
- `b_end_report_not_generated`
- `sandbox_public_event_not_generated`
- `downstream_gates_required`
- `not_export_ready`
- `not_download_ready`
- `not_public_ready`
- `not_customer_ready`
- `not_production_ready`
- `not_b_end_ready`
- `not_sandbox_ready`
- `not_public_event_ready`

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
- `called_download_package_runtime`
- `called_public_access_runtime`
- `called_external_delivery_runtime`
- `called_final_delivery_runtime`
- `generated_download_package`
- `generated_zip_package`
- `generated_public_access`
- `performed_external_delivery`
- `performed_final_delivery`
- `created_customer_delivery`
- `created_file_byte_route`
- `generated_public_url`
- `generated_signed_url`
- `uploaded_object_storage`
- `sent_email`
- `published_to_portal`
- `generated_b_end_report_runtime`
- `generated_sandbox_runtime`
- `generated_public_event_runtime`
- `generated_response_text`
- `created_public_route`
- `published_or_sent`
- `auto_executed`

Future 8V-24 may set a narrow metadata-only marker such as `created_local_final_delivery_boundary = true` only if no runtime, file, route, frontend, public, customer, delivery, B-end, Sandbox, Evidence Layer, production, provider, collector, LLM, URL fetch, or scraping side effect occurs.

## G. Blockers / Warnings

Required blockers:

- missing download/public-access boundary id
- wrong download/public-access boundary schema
- download/public-access boundary status not `download_public_access_boundary_ready_for_manual_review`
- download/public-access boundary not created
- missing created-local download/public-access boundary marker
- missing export-artifact boundary summary
- missing download/public-access readiness summary
- missing boundary flags
- missing runtime side-effect flags
- any disallowed runtime side-effect flag true
- requested final-delivery runtime
- requested customer delivery
- requested download/package runtime
- requested public-access runtime
- requested external-delivery runtime
- requested ZIP or package generation
- requested download package
- requested public URL
- requested signed URL
- requested file-byte route
- requested public access
- requested external delivery
- requested object storage upload
- requested email sending
- requested portal publication
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
- privacy, raw identity, private path, secret, browser profile, runtime path, artifact path, public URL, signed URL, file-byte route, object storage target, email target, portal target, customer delivery target, or external delivery target risk

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
- FinalSummaryReport remains local-only
- download/public-access boundary is not download package runtime
- final-delivery boundary is not final delivery runtime
- download package not created
- ZIP not generated
- public URL not created
- signed URL not created
- file-byte route not created
- public access not created
- external delivery not performed
- final delivery not performed
- customer delivery not created
- object storage not uploaded
- email not sent
- portal not published
- B-end, Sandbox, public event, frontend, route, production, and customer outputs require separate future gates

## H. Audit Fields

Allowed audit fields for future 8V-24:

- `audit_id`
- `audit_schema`
- `audit_action`
- `created_at`
- `created_by`
- `final_delivery_boundary_id`
- `download_public_access_boundary_id`
- `export_artifact_boundary_id`
- `export_gate_handoff_id`
- `adapter_id`
- `final_summary_report_id`
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

Audit must not include raw author identifiers, actual author names, actual profile URLs, private paths, row contents, secrets, browser profile paths, generated response text, artifact bytes, file paths, local runtime paths, public URLs, signed URLs, download URLs, file-byte routes, object storage targets, email targets, portal targets, customer delivery targets, or external delivery targets.

## I. Downstream Policy

Future 8V-24 output must state:

- Final-delivery runtime requires a later decision and explicit implementation approval.
- Customer delivery requires a later decision and explicit implementation approval.
- Download/package runtime requires a later decision and explicit implementation approval.
- ZIP/package generation requires a later decision and explicit implementation approval.
- Public URL generation requires a later decision and explicit implementation approval.
- Signed URL generation requires a later decision and explicit implementation approval.
- File-byte route creation requires a later decision and explicit implementation approval.
- Public access runtime requires a later decision and explicit implementation approval.
- External delivery runtime requires a later decision and explicit implementation approval.
- Object storage upload requires a later decision and explicit implementation approval.
- Email sending requires a later decision and explicit implementation approval.
- Portal publication requires a later decision and explicit implementation approval.
- B-end report runtime requires a later decision and explicit implementation approval.
- Sandbox/public event runtime requires a later decision and explicit implementation approval.
- Frontend/API route integration requires a later decision and explicit implementation approval.
- Evidence Layer write is not allowed by this boundary.
- Production case creation is not allowed by this boundary.
- Production `analysis_run` creation is not allowed by this boundary.
- Generated response text and platform action are not allowed by this boundary.

Required downstream readiness:

- `final_delivery_ready = false`
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

Future 8V-24 should add tests proving:

- safe 8V-22 download/public-access boundary marker is the only accepted input
- wrong boundary schema blocks
- non-ready boundary status blocks
- missing local download/public-access boundary marker blocks
- missing boundary flags block
- missing runtime side-effect flags block
- any requested final delivery, customer delivery, download/package, public access, external delivery, URL, file-byte, object storage, email, portal, B-end, Sandbox, route, or frontend side effect blocks
- forbidden actual fields or sentinel values block or are omitted
- no file IO is required
- no ZIP/package/download file is generated
- no public URL or signed URL is created
- no file-byte route is created
- no public access, external delivery, or final delivery is performed
- no customer delivery, object storage upload, email, or portal publication occurs
- no `evidence_items.jsonl` or `evidence_items.csv` is parsed
- no private collector files or real exchange dirs are read
- no routes or frontend files are changed
- final-delivery boundary output keeps all downstream flags false
- no B-end report, Sandbox/public event, Evidence Layer, production case, or production `analysis_run` is created

Recommended future validation:

- focused new final-delivery boundary tests
- existing 8V-22 download/public-access boundary tests
- existing 8V-20 export-artifact boundary tests
- existing 8V-18 export-gate handoff tests
- existing 8V-16 FinalSummaryReport adapter tests
- py_compile for touched backend files
- `git diff --check`

Do not require full pytest or frontend build unless future implementation touches shared code, routes, frontend, or the user explicitly requests full validation.

## K. Forbidden Interpretations

Do not interpret this contract as:

- final-delivery runtime approval in 8V-23
- customer delivery approval
- download/package runtime approval
- ZIP/package generation approval
- public URL approval
- signed URL approval
- file-byte route approval
- public access approval
- external delivery approval
- object storage approval
- email sending approval
- portal publication approval
- frontend or route readiness
- B-end report generation
- Sandbox/public event generation
- customer/public readiness
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

The future boundary is only a tightly bounded backend transition from the 8V local download/public-access boundary/readiness marker to a later final-delivery runtime review boundary. It must not be treated as final delivery, customer delivery, download, public access, external delivery, B-end, Sandbox, public event, or production promotion.
