# Sentigraph Dense Graph to Report Candidate Contract v0.1

## A. Contract Purpose

This contract defines a future controlled backend-only handoff from:

- a safe 8V-8 dense graph bridge integration object
- to a local report candidate boundary object

The contract exists to keep a future 8V-10 implementation narrow:

- consume only safe dense graph preview metadata
- create only a local report candidate object
- preserve selected-sample, human-review, and no-public-output boundaries
- keep FinalSummaryReport, export, download, public access, frontend, route, B-end report, Sandbox/public event, Evidence Layer, and production runtime disconnected

This contract is not an implementation. It is not a route. It is not frontend integration. It is not report generation. It is not export generation. It is not public delivery.

## B. Proposed Future Report Candidate Contract

Proposed schema:

```json
{
  "report_candidate_schema": "sentigraph_dense_graph_report_candidate_v0_1"
}
```

Proposed future object:

```json
{
  "report_candidate_id": "dense_graph_report_candidate_...",
  "report_candidate_schema": "sentigraph_dense_graph_report_candidate_v0_1",
  "report_candidate_status": "candidate_ready|blocked_metadata_contract|blocked_privacy_issue|blocked_requested_side_effect|manual_review_required",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "input_source_kind": "generated_run_dense_graph_bridge_integration",
  "candidate_mode": "backend_only_local_report_candidate",
  "integration_id": "generated_run_dense_graph_bridge_integration_...",
  "execution_id": "minimum_real_run_bridge_execution_...",
  "bridge_id": "staging_generated_run_bridge_...",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "generated_run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
  "dense_graph_integration_schema": "sentigraph_generated_run_dense_graph_bridge_integration_v0_1",
  "dense_graph_summary": {},
  "report_candidate_summary": {},
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

- `candidate_ready`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_requested_side_effect`
- `blocked_forbidden_input`
- `manual_review_required`

`candidate_ready` means only that a local backend candidate object was created. It does not mean final report readiness, export readiness, customer readiness, or public readiness.

## C. Input Contract

Future 8V-10 may accept only a safe 8V-8 dense graph bridge integration object.

Required input values:

- `integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- `integration_status = integrated_backend_dense_graph_preview`
- `dense_graph_executed = true`
- `dense_graph_integration` present
- `dense_graph_summary` present
- `frontend_integration_approved = false`
- `route_changed = false`
- `api_route_added = false`
- `report_generated = false`
- `sandbox_public_event_generated = false`
- `generated_response_text = false`
- `public_route_created = false`
- `runtime_side_effects` present and all false
- `boundary_flags` present
- `boundary_flags.human_review_required = true`
- `dense_graph_summary.frontend_ready = false`
- `dense_graph_summary.route_ready = false`
- `dense_graph_summary.production_ready = false`

Allowed upstream refs:

- `integration_id`
- `execution_id`
- `bridge_id`
- `staging_candidate_id`
- `provider_result_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `generated_run_schema`
- `input_source_kind`
- `integration_mode`

Allowed dense graph summaries:

- `dense_graph_attached`
- `people_cluster_proxy_count`
- `influence_core_proxy_count`
- `content_aggregate_proxy_count`
- `echobox_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode`
- density note
- selected sample coverage limitation
- warning and blocker summaries

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
- original package rows
- collector internals
- response text
- generated public message
- target user list
- persuasion score
- truth score
- official verification claim
- prediction probability
- psychological profile
- personality diagnosis

## D. Output Contract

The future report candidate output should summarize possible report sections without creating those sections as final report artifacts.

Allowed output fields:

- candidate identity and schema
- upstream refs
- dense graph proxy counts
- selected sample scope note
- coverage limitation note
- safe warning summary
- safe blocker summary
- candidate section outline
- candidate evidence governance summary
- candidate graph interpretation summary
- candidate risk and limitation summary
- boundary flags
- runtime side-effect flags
- audit refs
- downstream policy

Recommended `report_candidate_summary` shape:

```json
{
  "candidate_title": "Dense graph preview report candidate",
  "candidate_scope": "selected_sample_only_dense_graph_preview",
  "candidate_sections": [
    "scope_and_boundaries",
    "dense_graph_proxy_summary",
    "coverage_limitations",
    "human_review_required",
    "not_final_report"
  ],
  "dense_graph_proxy_counts": {},
  "coverage_limitations": [],
  "human_review_required": true,
  "final_report_ready": false,
  "export_ready": false,
  "public_ready": false,
  "b_end_runtime_ready": false,
  "sandbox_public_event_ready": false
}
```

Forbidden output:

- final report content
- B-end report runtime
- Sandbox/public event runtime
- PDF file
- Markdown report file
- briefing deck file
- ZIP file
- export artifact
- public URL
- signed URL
- download package
- file-byte response
- generated public response text
- publish/send/post/execute instruction
- Evidence Layer write result
- production case
- production `analysis_run`

## E. Boundary Flags

The future object must keep these boundary flags explicit:

```json
{
  "selected_sample_only": true,
  "dense_graph_preview_derived": true,
  "backend_only_local_candidate": true,
  "metadata_only_upstream": true,
  "anonymous_aggregate_only": true,
  "not_full_web": true,
  "not_full_platform": true,
  "not_full_thread": true,
  "not_official_verification": true,
  "not_causal_proof": true,
  "not_prediction": true,
  "not_production_score": true,
  "not_final_report": true,
  "not_b_end_report_runtime": true,
  "not_sandbox_public_event_runtime": true,
  "not_export_artifact": true,
  "human_review_required": true,
  "no_auto_execute": true,
  "no_generated_public_response": true,
  "frontend_ready": false,
  "route_ready": false,
  "production_ready": false,
  "export_ready": false,
  "public_ready": false
}
```

Missing or unsafe boundary flags should block the future candidate or mark it manual-review-required.

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
  "created_final_report": false,
  "generated_b_end_report_runtime": false,
  "generated_sandbox_runtime": false,
  "generated_public_event_runtime": false,
  "created_export_artifact": false,
  "generated_pdf": false,
  "generated_markdown_report": false,
  "generated_briefing_deck": false,
  "generated_response_text": false,
  "created_public_route": false,
  "generated_public_url": false,
  "generated_signed_url": false,
  "created_download_package": false,
  "performed_external_delivery": false,
  "published_or_sent": false,
  "auto_executed": false
}
```

Allowed candidate marker:

```json
{
  "report_candidate_created": true
}
```

This marker would mean only that a local backend candidate object was created from a safe dense graph preview. It must not imply final report generation, export generation, public delivery, route readiness, frontend readiness, or production readiness.

## G. Blockers / Warnings

Hard blockers:

- input schema not recognized
- input status not `integrated_backend_dense_graph_preview`
- `dense_graph_executed` is not true
- dense graph integration missing
- dense graph summary missing
- runtime side-effect flag not false
- boundary flags missing
- `human_review_required` missing or false
- `frontend_ready`, `route_ready`, or `production_ready` true
- route/frontend/API/report/public-output flag true
- upstream blocker indicates privacy, secret, raw identity, path, side-effect, production, public-output, or real-provider risk
- forbidden active field present
- requested evidence row parsing
- requested original package row reading
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested final report generation
- requested B-end report runtime
- requested Sandbox/public event runtime
- requested export artifact
- requested PDF, Markdown report, briefing deck, ZIP, public URL, signed URL, download package, file-byte route, or external delivery
- requested generated response text
- requested publish/send/post/execute action
- requested real API, real LLM, collector, private project access, URL fetch, or scrape

Warnings:

- selected sample is small
- selected sample coverage is weak
- source coverage limitation is material
- dense graph attachment is degraded
- dense graph values are deterministic/default and uncalibrated
- empirical validation is not started
- report candidate requires human review before any future report generation gate
- report candidate remains disconnected from FinalSummaryReport governance

Warnings do not upgrade trust and do not make the candidate production-ready.

## H. Audit Fields

Future report candidate should carry audit metadata:

- `audit_refs`
- `source_integration_audit_refs`
- `candidate_created_by`
- `candidate_created_at`
- `candidate_reason`
- `input_integration_summary`
- `input_dense_graph_summary`
- `boundary_confirmation_snapshot`
- `blocked_action_snapshot`
- `report_candidate_helper_name`
- `report_candidate_helper_version` if available

Audit must not include raw author identifiers, actual author names, profile URLs, private paths, row contents, secrets, browser profile paths, public response text, or raw comment payloads.

## I. Downstream Policy

Allowed after future 8V-10:

- inspect local report candidate summary
- validate boundary flags
- validate runtime side-effect flags
- decide whether another docs-only gate should connect report candidate to report generation
- decide whether frontend and route integration remain deferred

Blocked after future 8V-10 unless separately approved:

- FinalSummaryReport runtime
- report export/download/package runtime
- public-access or external-delivery runtime
- B-end/customer report runtime
- Sandbox/public event runtime
- frontend integration
- route change
- API route addition
- public route
- Evidence Layer write
- production case
- production `analysis_run`
- generated public response text
- public URL
- signed URL
- file-byte response
- collector job
- row parsing
- real API
- real LLM
- URL fetch or scraping
- algorithm/weight recalibration

The report candidate remains internal, selected-sample-only, dense-graph-preview-derived, and human-review-required.

## J. Future Tests

Future 8V-10 tests should verify:

- report candidate object has schema `sentigraph_dense_graph_report_candidate_v0_1`
- safe 8V-8 dense graph bridge integration can produce a local candidate
- candidate requires `integration_schema = sentigraph_generated_run_dense_graph_bridge_integration_v0_1`
- candidate requires `integration_status = integrated_backend_dense_graph_preview`
- candidate requires `dense_graph_executed = true`
- missing dense graph integration blocks
- missing dense graph summary blocks
- frontend/route/production readiness true blocks
- runtime side-effect flag true blocks
- route/frontend/API/report/public output request blocks
- export/public-access/download request blocks
- forbidden active fields block without exposing values
- candidate output keeps final report/export/public/B-end/Sandbox flags false
- candidate output keeps `human_review_required = true`
- candidate output contains only safe summaries and upstream refs
- no Evidence Layer write
- no production case or production `analysis_run`
- no FinalSummaryReport runtime
- no B-end report runtime
- no Sandbox/public event runtime
- no export artifact
- no generated response text
- no package rows are parsed
- no package files are opened
- no real API / real LLM / collector call occurs

Suggested future test file:

`backend/app/tests/test_dense_graph_report_candidate_bridge.py`

This is a future recommendation only. 8V-9 does not create tests.

## K. Forbidden Interpretations

Do not interpret this contract as:

- report generation approval
- FinalSummaryReport approval
- report export approval
- download package approval
- public access approval
- external delivery approval
- frontend approval
- route approval
- public route approval
- B-end/customer route approval
- B-end report runtime approval
- Sandbox/public event runtime approval
- Evidence Layer import
- production case creation
- production `analysis_run` creation
- generated public response authorization
- official verification
- calibrated prediction
- causal proof
- truth score
- full-web coverage
- full-platform coverage
- collector integration
- real API integration
- real LLM integration
- algorithm/weight recalibration

The contract only defines how a future backend-only smoke may create a local report candidate object from a safe dense graph bridge integration preview.
