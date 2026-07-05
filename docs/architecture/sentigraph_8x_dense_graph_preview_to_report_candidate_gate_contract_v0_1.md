# Sentigraph 8X Dense Graph Preview to Report Candidate Gate Contract v0.1

## Contract Purpose

This contract defines the boundary for a possible future 8X-10 controlled smoke that hands the 8X-8 local controlled backend dense graph preview to the existing dense graph report candidate bridge.

The contract is docs-only in 8X-9. It does not call dense graph, create a report candidate, create FinalSummaryReport, add tests, modify backend code, add routes, add frontend UI, persist runtime state, or create any production object.

## Gate Object

```json
{
  "schema": "sentigraph_8x_dense_graph_preview_to_report_candidate_gate_v0_1",
  "phase": "8X-9",
  "decision": "ready",
  "docs_only": true,
  "privacy_issue_stop": false,
  "selected_next_boundary_option": "ready_for_8X_10_controlled_dense_graph_preview_report_candidate_bridge_smoke",
  "source_checkpoint": {
    "phase": "8X-8",
    "dense_graph_preview_present": true,
    "dense_graph_preview_scope": "local_controlled_backend_preview_only",
    "anonymous_aggregate_proxy_only": true,
    "frontend_ready": false,
    "route_ready": false,
    "production_ready": false,
    "report_candidate_created": false
  },
  "allowed_future_input": {
    "input_kind": "local_controlled_backend_dense_graph_preview",
    "created_by": "8X-8 ready generated-run dense graph bridge path",
    "anonymous_aggregate_proxy_only": true,
    "frontend_ready": false,
    "route_ready": false,
    "production_ready": false,
    "human_review_required": true,
    "no_automatic_trust_upgrade": true,
    "evidence_rows_allowed": false,
    "raw_comments_allowed": false,
    "raw_identities_allowed": false,
    "author_name_values_allowed": false,
    "profile_url_values_allowed": false,
    "real_package_directory_allowed": false,
    "private_collector_source_allowed": false
  },
  "allowed_future_action": {
    "backend_only": true,
    "test_first": true,
    "controlled_smoke_only": true,
    "synthetic_temp_fixture_only": true,
    "use_existing_dense_graph_report_candidate_bridge": true,
    "local_backend_report_candidate_object_only": true,
    "final_summary_report_allowed": false,
    "b_end_report_runtime_allowed": false,
    "sandbox_public_event_runtime_allowed": false,
    "route_allowed": false,
    "frontend_allowed": false,
    "runtime_persistence_allowed": false,
    "production_write_allowed": false,
    "export_download_public_delivery_allowed": false
  },
  "required_future_output_constraints": {
    "report_candidate_created": "true_only_inside_controlled_backend_test_path",
    "report_candidate": "local_controlled_backend_object_only",
    "final_summary_report_created": false,
    "b_end_report_runtime_generated": false,
    "sandbox_public_event_runtime_generated": false,
    "evidence_rows_parsed": false,
    "evidence_layer_write": false,
    "production_case_created": false,
    "production_analysis_run_created": false,
    "production_evidence_item_created": false,
    "review_queue_runtime_used": false,
    "generated_response_text": false,
    "public_route_created": false,
    "export_download_public_delivery_created": false,
    "frontend_ready": false,
    "route_ready": false,
    "production_ready": false,
    "customer_ready": false,
    "human_review_required": true,
    "no_automatic_trust_upgrade": true,
    "coefficient_source": "mock_default_or_existing_safe_local_equivalent",
    "calibration_status": "uncalibrated_or_existing_safe_local_equivalent",
    "empirical_validation": "not_started_or_existing_safe_local_equivalent",
    "not_full_web": true,
    "not_full_platform": true,
    "not_official_verification": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "not_production_score": true
  },
  "future_approval": {
    "exact_phrase_required": true,
    "exact_phrase": "APPROVE_8X_10_CONTROLLED_DENSE_GRAPH_PREVIEW_REPORT_CANDIDATE_BRIDGE_SMOKE",
    "active_in_8x9": false,
    "production_authorization": false
  }
}
```

## Field Notes

- `decision`: `ready` means the docs-only report candidate gate criteria are defined. It does not mean 8X-10 is authorized.
- `source_checkpoint`: records the 8X-8 local controlled dense graph preview status and keeps it separate from production readiness or customer readiness.
- `allowed_future_input`: restricts future input to the safe dense graph preview created through the 8X-8 path.
- `allowed_future_action`: restricts future work to a backend-only, test-first, controlled report candidate bridge smoke.
- `required_future_output_constraints`: prevents report candidate creation from becoming FinalSummaryReport, B-end report runtime, Sandbox/public event runtime, production write, public output, runtime state, frontend readiness, route readiness, or trust upgrade.
- `future_approval`: records the inactive future phrase required by a later prompt.

## Required Input Checklist for Future 8X-10

Future 8X-10 may proceed only if the prompt and local state confirm:

- exact future approval phrase is present
- input was created through the 8X-8 path
- dense graph preview is local controlled backend preview only
- dense graph preview remains anonymous aggregate/proxy only
- frontend readiness is false
- route readiness is false
- production readiness is false
- customer readiness is false if present
- human review remains required
- no automatic trust upgrade occurs
- coefficient source remains `mock_default` or an existing safe local equivalent
- calibration status remains `uncalibrated` or an existing safe local equivalent
- empirical validation remains `not_started` or an existing safe local equivalent
- boundary flags preserve not-full-web, not-full-platform, not-full-thread, not-official-verification, not-causal-proof, not-prediction, and not-production-score semantics
- no evidence rows are needed
- no raw comments or raw identities are present
- no author names or profile URLs are present as actual values
- no real package directory is needed
- no private collector source inspection is needed
- no real exchange directory read is needed
- no collector job is needed
- no real API, real LLM, URL fetching, or scraping is needed
- no Evidence Layer write is requested
- no production case, production EvidenceItem, or production analysis_run is requested
- no FinalSummaryReport, B-end report, Sandbox/public event, export/download/public delivery, route, frontend, or runtime persistence is requested

## Blocker Categories

Future 8X-10 must stop on:

- evidence_row_parsing_required
- real_exchange_dir_required
- real_package_directory_required
- private_collector_inspection_required
- collector_job_required
- real_api_or_llm_required
- network_or_url_fetch_required
- scrape_required
- evidence_layer_write_requested
- production_case_or_analysis_run_requested
- production_evidence_item_requested
- review_queue_runtime_requested
- raw_identity_or_comment_exposure
- actual_author_name_or_profile_url_exposure
- secret_or_private_path_exposure
- generated_response_text_requested
- final_summary_report_requested
- b_end_report_or_sandbox_public_event_requested
- export_download_public_delivery_requested
- route_frontend_or_runtime_persistence_requested
- customer_ready_or_public_ready_claim_requested
- broad_service_behavior_change_required
- automatic_trust_upgrade_requested
- production_authorization_confusion
- missing_or_changed_approval_phrase

## Required Future 8X-10 Validation Expectations

A future 8X-10 controlled smoke should prove:

- safe 8X-8 dense graph preview can enter the existing report candidate bridge
- wrong or missing dense graph preview does not create a report candidate
- missing dense graph summary blocks
- frontend/route/production readiness true blocks
- runtime side-effect flags remain false
- report candidate object is local controlled backend object only
- FinalSummaryReport is not created
- B-end report runtime is not generated
- Sandbox/public event runtime is not generated
- export/download/public delivery is not created
- evidence rows are not parsed
- package files are not opened
- Evidence Layer is not written
- production case, production EvidenceItem, and production analysis_run are not created
- Review Queue runtime is not used
- generated response text remains false
- forbidden active fields block without exposing values
- human review remains required
- no automatic trust upgrade occurs
- frontend_ready, route_ready, production_ready, and customer_ready remain false

## 8X-9 Non-execution Confirmation

- dense_graph_called: no
- report_candidate_created: no
- final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- evidence_rows_parsed: no
- evidence_layer_write: no
- production_case_created: no
- production_analysis_run_created: no
- production_evidence_item_created: no
- review_queue_runtime_used: no
- generated_response_text: no
- public_route_created: no
- export_download_public_delivery_created: no
- human_review_required: yes
- no_automatic_trust_upgrade: yes

## Boundary Language

The future report candidate bridge smoke, if separately approved, is allowed to test whether an existing report candidate bridge can produce a local backend candidate object from a safe 8X-8 dense graph preview.

It is not allowed to claim:

- full-web coverage
- full-platform coverage
- full-thread coverage
- official verification
- causal proof
- prediction
- production scoring
- production Analysis Result creation
- production case creation
- production analysis_run creation
- FinalSummaryReport creation
- B-end report runtime
- Sandbox/public event runtime
- export artifact creation
- download package creation
- public URL or signed URL creation
- customer-ready output
- public-ready output

Provider output remains evidence, not truth. The dense graph preview remains selected-sample-only, controlled, uncalibrated, anonymous aggregate/proxy, and human-review-required. A future report candidate must not upgrade trust or become a final report.
