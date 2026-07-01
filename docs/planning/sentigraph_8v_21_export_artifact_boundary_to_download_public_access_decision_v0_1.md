# Sentigraph 8V-21 Export Artifact Boundary to Download/Public Access Decision v0.1

## A. Decision / Status

phase = 8V-21

task = export_artifact_boundary_to_download_public_access_decision

decision = ready

selected_next_boundary_option = ready_for_8V_22_controlled_export_artifact_boundary_to_download_public_access_boundary_smoke

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

export_artifact_boundary_created = no

download_public_access_boundary_created = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

download_package_created = no

generated_zip_package = no

public_url_created = no

signed_url_created = no

public_access_created = no

external_delivery_performed = no

file_byte_route_created = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

source_files_created = no

docs_project_sources_created = no

Decision:

Sentigraph is ready for a future 8V-22 controlled backend-only export-artifact-boundary to download/public-access boundary/readiness smoke.

This decision does not approve download package runtime, ZIP/package generation, public URL creation, signed URL creation, public access runtime, external delivery runtime, file-byte routes, frontend or API routes, B-end report runtime, Sandbox/public event runtime, Evidence Layer writes, production case creation, production `analysis_run` creation, evidence row parsing, real API/LLM/provider/collector calls, URL fetching, scraping, or generated response text.

## B. Current Proven Chain Through 8V-20

The current proven 8V chain is:

1. provider result metadata
2. safe package resolver
3. local exchange metadata smoke
4. review-only staging candidate
5. staging candidate generated-run bridge
6. controlled minimum real-run bridge execution
7. `sentigraph_opinion_ecosystem_run_v0_1` generated run
8. controlled generated-run dense graph bridge integration
9. backend-only dense graph preview
10. `sentigraph_dense_graph_report_candidate_v0_1` local report candidate
11. `sentigraph_report_candidate_final_report_boundary_v0_1` local final-report-boundary object
12. `sentigraph_final_report_boundary_source11_governance_handoff_v0_1` local Source 11 governance handoff marker
13. `sentigraph_source11_governance_handoff_finalsummaryreport_adapter_v0_1` local FinalSummaryReport boundary adapter
14. local in-memory `sentigraph_final_summary_report_v1`-shaped boundary object
15. `sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1` local export-gate handoff/readiness marker
16. `sentigraph_export_gate_handoff_export_artifact_boundary_v0_1` local export-artifact boundary/readiness marker

8V-20 proved only:

safe 8V-18 local export-gate handoff marker -> backend-only local export-artifact boundary/readiness marker.

8V-20 did not:

- call existing Source 11 export artifact runtime/store/route
- create `sentigraph_final_summary_report_export_artifact_v1`
- create export artifact files
- generate analyst Markdown
- generate PDF
- generate briefing deck
- generate evidence appendix package
- generate ZIP/package/download package
- create public URL or signed URL
- create public access
- perform external delivery
- add route or touch frontend
- create B-end report runtime
- create Sandbox/public event runtime
- parse evidence rows
- write Evidence Layer
- create production case
- create production `analysis_run`
- call real API, LLM, provider, or collector
- fetch URL or scrape
- generate response text

## C. Export Artifact Boundary to Download/Public-access Problem Statement

The next boundary question is:

Can a safe 8V-20 local export-artifact boundary/readiness marker later enter a download/public-access boundary?

The answer is yes, but only as a future backend-only metadata boundary/readiness object. The future object may record that the safe local export-artifact boundary marker is eligible for later manual download/public-access review.

It must not create a download package, ZIP, public URL, signed URL, file-byte route, public access artifact, external delivery artifact, B-end report, Sandbox/public event output, frontend state, API route, Evidence Layer record, production case, or production `analysis_run`.

This distinction matters because existing report export download/package governance assumes a later formal export artifact and dedicated package/public access gates. The 8V chain is still one step earlier: it has only a local pre-artifact boundary marker, not a real export artifact runtime output.

## D. Allowed Future Input

Future 8V-22 may accept only a safe 8V-20 local export-artifact boundary/readiness marker.

Allowed input must include:

- `export_artifact_boundary_schema = sentigraph_export_gate_handoff_export_artifact_boundary_v0_1`
- `export_artifact_boundary_status = export_artifact_boundary_ready_for_manual_review`
- `export_artifact_boundary_created = true`
- `created_local_export_artifact_boundary = true`
- `input_source_kind = export_gate_handoff`
- `boundary_mode = backend_only_local_export_artifact_boundary_readiness_smoke`
- `export_gate_handoff_schema = sentigraph_finalsummaryreport_boundary_export_gate_handoff_v0_1`
- `export_gate_handoff_status = export_gate_handoff_ready_for_manual_review`
- `export_gate_handoff_created = true`
- `created_local_export_gate_handoff = true`
- `final_summary_report_created = true`
- `final_summary_report_created_local_only = true`
- `local_final_summary_report_only = true`
- `human_review_required = true`
- `export_artifact_runtime_used = false`
- `called_export_artifact_runtime = false`
- `final_summary_report_export_artifact_created = false`
- `export_artifact_created = false`
- `generated_markdown_file = false`
- `generated_pdf_file = false`
- `generated_briefing_deck = false`
- `generated_evidence_appendix_package = false`
- `generated_zip_package = false`
- `download_package_created = false`
- `public_access_created = false`
- `external_delivery_performed = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- `frontend_integration_approved = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `export_ready = false`
- `public_ready = false`
- `customer_ready = false`
- `b_end_ready = false`
- `sandbox_ready = false`
- `public_event_ready = false`
- `boundary_flags` present
- `runtime_side_effects` present and unrelated side effects false

Allowed upstream refs:

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
- `export_gate_handoff_summary`
- `export_artifact_boundary_readiness_summary`
- `boundary_block`
- `coverage_limitations`
- warning summary
- blocker summary
- human review status
- audit refs
- downstream policy summary

## E. Forbidden Input / Forbidden Output

Future 8V-22 must not accept, produce, copy, expose, or imply:

- evidence row content
- raw comments
- raw author identifiers
- actual author name values
- actual profile URL values
- private messages
- cookies, sessions, tokens, passwords, or API keys
- absolute private paths
- browser profile paths
- original package rows
- collector internals
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
- `publish`
- `send`
- `post`
- `execute`
- actual Markdown report content
- PDF file path
- briefing deck file path
- evidence appendix package path
- ZIP/package path
- download package path
- public URL
- signed URL
- file-byte route
- external delivery target
- object storage upload
- email sending
- portal publication

Safe negative boundary language may name these only to say they are false, forbidden, blocked, deferred, or require separate later gates.

## F. Download/public-access Relationship Decision

Decision: choose option A.

`ready_for_8V_22_controlled_export_artifact_boundary_to_download_public_access_boundary_smoke`

Rationale:

- 8V-20 provides a local metadata export-artifact boundary/readiness marker with export artifact runtime, download package, public access, external delivery, B-end, Sandbox, route, frontend, production, public, customer, and Evidence Layer readiness false.
- Existing download/package and public access/external delivery governance documents already separate gate decisions from runtime output, file-byte routes, public URLs, signed URLs, object storage, email, portal publication, B-end report generation, Sandbox generation, and public event generation.
- Existing download/public access contracts assume a formal export artifact and package artifact. The future 8V-22 object must therefore be pre-download/public-access boundary metadata only, not a direct invocation of existing package or public access runtimes.
- A backend-only local boundary/readiness object can be safely bounded if it preserves every false side-effect flag and requires separate later decisions for package/runtime/public/delivery work.

8V-21 therefore approves only a future controlled boundary/readiness smoke. It does not approve any download package, ZIP, public URL, signed URL, public access, external delivery, route, frontend, B-end, Sandbox, or production behavior.

## G. Future 8V-22 Option A: Controlled Download/public-access Boundary/readiness Object

Future 8V-22 may create only a backend-only local download/public-access boundary/readiness object, such as:

`sentigraph_export_artifact_boundary_download_public_access_boundary_v0_1`

or an equivalent name that clearly indicates boundary/readiness only.

This future object may only say:

- the local export-artifact boundary marker is eligible for later manual download/public-access review
- no download/package runtime has been called
- no public-access runtime has been called
- no external-delivery runtime has been called
- no ZIP/package/download file has been generated
- no public URL or signed URL has been created
- no file-byte route has been created
- no B-end report or Sandbox/public event runtime has been generated
- no route/frontend/public/customer/production readiness has been granted

Future 8V-22 must not:

- generate download package
- generate ZIP/package
- create public URL or signed URL
- return file bytes
- create public route
- perform external delivery
- send email
- upload object storage
- publish portal
- touch frontend
- create B-end report runtime
- create Sandbox/public event runtime
- write Evidence Layer
- create production case
- create production `analysis_run`
- parse evidence rows
- call real API, LLM, provider, or collector
- fetch URL or scrape

## H. Future 8V-22 Option B: Separation Hardening

Option B remains the fallback:

`ready_for_8V_22_export_artifact_boundary_download_public_access_separation_hardening_smoke`

Use option B if future implementation inspection finds ambiguity in:

- download package runtime coupling
- manifest package runtime coupling
- public access runtime coupling
- external delivery runtime coupling
- signed URL behavior
- public URL behavior
- file-byte route behavior
- runtime file path exposure
- ZIP generation
- frontend route coupling
- Source 11 behavior
- privacy, raw identity, private path, secret, production-readiness, or public-output risk

In option B, future 8V-22 should only prove separation and should not create a download/public-access boundary object.

## I. Download Package / Public URL / Signed URL / External Delivery Non-approval

8V-21 does not approve:

- download/package runtime
- ZIP/package generation
- local file download generation
- public download route
- file-byte response
- public URL
- signed URL
- object storage upload
- email sending
- portal publication
- public access runtime
- external delivery runtime

Any future actual download/package runtime requires a later docs-only decision and explicit implementation approval.

Any future public access or external delivery requires separate later gates, explicit implementation approval, and dedicated validation that no private path, raw row, secret, artifact bytes, runtime file exposure, public URL, signed URL, absolute filesystem path exposure, or external delivery target leakage occurs.

## J. Relationship to Frontend / Public Route / B-end / Sandbox

8V-21 does not approve:

- frontend report integration
- public route
- B-end/customer route
- B-end report runtime
- Sandbox/public event runtime
- download/package runtime
- public access
- signed URL
- external delivery
- object storage upload
- email sending
- portal publication
- file-byte response

Frontend polish remains paused.

Any future frontend/API route integration requires a separate later gate and explicit implementation approval.

## K. Next-slice Options

Available next options:

1. Proceed to 8V-22 controlled export-artifact boundary to download/public-access boundary/readiness smoke.
2. Switch to 8V-22 separation hardening if implementation risk appears.
3. Pause for more download/public access governance inventory if required inputs or side effects are unclear.
4. Stop if privacy, raw identity, private path, secret, production-readiness, public-output, file-generation, route/frontend, or side-effect risk appears.

Option 1 is recommended, with strict stop conditions.

## L. Recommended Next Step

Recommended next task:

Phase 8V-22 Controlled Export Artifact Boundary to Download/Public Access Boundary / Readiness Smoke, backend-only and test-first.

8V-22 should:

- accept only a safe 8V-20 local export-artifact boundary/readiness marker
- remain backend-only and local-only
- be test-first
- create at most a local download/public-access boundary/readiness marker
- not call download/package runtime
- not call public-access runtime
- not call external-delivery runtime
- not create download package, ZIP, public URL, signed URL, file-byte route, public access, or external delivery
- not touch frontend or routes
- not create B-end, Sandbox, or public event runtime
- not write Evidence Layer
- not create production case or production `analysis_run`
- keep human review required
- preserve selected-sample-only limitations
- include tests for forbidden fields, side-effect requests, public/download/delivery non-approval, and no file generation

## M. Explicit Non-approvals

This phase explicitly does not approve:

- backend runtime implementation
- backend code modification
- tests
- frontend implementation
- route/API addition
- export artifact boundary creation in this phase
- download/public-access boundary creation in this phase
- download package runtime use
- public access runtime use
- external delivery runtime use
- ZIP/package generation
- public URL creation
- signed URL creation
- file-byte route creation
- public access
- external delivery
- B-end report runtime
- Sandbox/public event runtime
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- row parsing
- provider/collector execution
- real API calls
- real LLM calls
- URL fetching
- scraping
- generated response text
- publish, send, post, execute, or auto-execute behavior
- Project Source file creation
- `docs/project_sources/` creation

## N. Validation / Not Run

Validation for this docs-only phase:

- `git status --short`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git diff --check`
- static scan of the two new docs for forbidden-capability terms

Backend tests, frontend build, browser smoke, runtime smoke, provider jobs, collector jobs, API calls, LLM calls, URL fetching, scraping, private collector inspection, real exchange dir reads, evidence row parsing, export artifact runtime smoke, download/package runtime smoke, public-access runtime smoke, and external-delivery runtime smoke are intentionally not run because this phase changes only docs and must not exercise runtime behavior.

## O. Source Maintenance Note

No immediate Source update is recommended.

Reason:

8V-21 is a docs-only decision checkpoint. It does not change Analysis Request, Provider, Import Governance, Source 11 runtime, export runtime, download runtime, public access runtime, frontend, routes, or public-output behavior.

After a future 8V-22 implementation is committed and the working tree is clean, Source 00 / 08 / 09 / 10 may be considered for update if the user approves. Do not update Source 11 unless actual Analysis Request / Provider / Import Governance behavior changes.
