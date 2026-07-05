# Sentigraph 8X Generated-run to Dense Graph Gate Contract v0.1

## Contract Purpose

This contract defines the boundary for a possible future 8X-8 controlled smoke that hands the 8X-6 local controlled ready generated-run object to the existing dense graph bridge.

The contract is docs-only in 8X-7. It does not call dense graph, create a dense graph preview, create a report candidate, add tests, modify backend code, add routes, add frontend UI, persist runtime state, or create any production object.

## Gate Object

```json
{
  "schema": "sentigraph_8x_generated_run_to_dense_graph_gate_v0_1",
  "phase": "8X-7",
  "decision": "ready",
  "docs_only": true,
  "privacy_issue_stop": false,
  "selected_next_boundary_option": "ready_for_8X_8_controlled_ready_generated_run_dense_graph_bridge_smoke",
  "source_checkpoint": {
    "phase": "8X-6",
    "generated_run_schema": "sentigraph_opinion_ecosystem_run_v0_1",
    "generated_run_status": "ready",
    "previous_blocker_cleared": "required_fixture_metadata_missing",
    "local_controlled_test_path_only": true,
    "production_ready": false
  },
  "allowed_future_input": {
    "input_kind": "local_controlled_ready_generated_run",
    "created_by": "8X-6 metadata bridge minimum-real-run fixture metadata completion path",
    "generated_run_schema": "sentigraph_opinion_ecosystem_run_v0_1_or_existing_safe_equivalent",
    "generated_run_status": "ready",
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
    "use_existing_generated_run_to_dense_graph_bridge": true,
    "local_backend_dense_graph_preview_only": true,
    "report_candidate_allowed": false,
    "route_allowed": false,
    "frontend_allowed": false,
    "runtime_persistence_allowed": false,
    "production_write_allowed": false
  },
  "required_future_output_constraints": {
    "dense_graph_called": "true_only_inside_controlled_backend_test_path",
    "dense_graph_preview": "local_controlled_test_path_object_only",
    "report_candidate_created": false,
    "evidence_rows_parsed": false,
    "evidence_layer_write": false,
    "production_case_created": false,
    "production_analysis_run_created": false,
    "production_evidence_item_created": false,
    "review_queue_runtime_used": false,
    "b_end_report_runtime_generated": false,
    "sandbox_public_event_runtime_generated": false,
    "generated_response_text": false,
    "public_route_created": false,
    "export_download_public_delivery_created": false,
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
    "exact_phrase": "APPROVE_8X_8_CONTROLLED_READY_GENERATED_RUN_DENSE_GRAPH_BRIDGE_SMOKE",
    "active_in_8x7": false,
    "production_authorization": false
  }
}
```

## Field Notes

- `decision`: `ready` means the docs-only dense graph gate criteria are defined. It does not mean 8X-8 is authorized.
- `source_checkpoint`: records the 8X-6 local controlled ready generated-run status and keeps it separate from production readiness.
- `allowed_future_input`: restricts future input to the safe generated-run object created through the 8X-6 path.
- `allowed_future_action`: restricts future work to a backend-only, test-first, controlled dense graph bridge smoke.
- `required_future_output_constraints`: prevents dense graph preview from becoming report candidate creation, production write, public output, runtime state, frontend readiness, or trust upgrade.
- `future_approval`: records the inactive future phrase required by a later prompt.

## Required Input Checklist for Future 8X-8

Future 8X-8 may proceed only if the prompt and local state confirm:

- exact future approval phrase is present
- input was created through the 8X-6 path
- generated-run schema is `sentigraph_opinion_ecosystem_run_v0_1` or an existing safe equivalent
- generated-run status is `ready`
- human review remains required
- no automatic trust upgrade occurs
- coefficient source remains `mock_default` or an existing safe local equivalent
- calibration status remains `uncalibrated` or an existing safe local equivalent
- empirical validation remains `not_started` or an existing safe local equivalent
- boundary flags preserve not-full-web, not-full-platform, not-official-verification, not-causal-proof, not-prediction, and not-production-score semantics
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
- no report candidate, B-end report, Sandbox/public event, export/download/public delivery, route, frontend, or runtime persistence is requested

## Blocker Categories

Future 8X-8 must stop on:

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
- report_candidate_requested
- b_end_report_or_sandbox_public_event_requested
- export_download_public_delivery_requested
- route_frontend_or_runtime_persistence_requested
- broad_service_behavior_change_required
- automatic_trust_upgrade_requested
- production_authorization_confusion
- missing_or_changed_approval_phrase

## Required Future 8X-8 Validation Expectations

A future 8X-8 controlled smoke should prove:

- safe 8X-6 generated-run object can enter the existing dense graph bridge
- blocked or missing generated run does not call dense graph
- missing boundary flags block before dense graph call
- runtime side-effect flags remain false
- dense graph preview is local controlled test-path only
- report candidate is not created
- evidence rows are not parsed
- package files are not opened
- Evidence Layer is not written
- production case, production EvidenceItem, and production analysis_run are not created
- Review Queue runtime is not used
- B-end report, Sandbox/public event, generated response text, export/download/public delivery, route, frontend, and runtime persistence remain false
- forbidden active fields block without exposing values
- human review remains required
- no automatic trust upgrade occurs

## 8X-7 Non-execution Confirmation

- dense_graph_called: no
- report_candidate_created: no
- evidence_rows_parsed: no
- evidence_layer_write: no
- production_case_created: no
- production_analysis_run_created: no
- production_evidence_item_created: no
- review_queue_runtime_used: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- generated_response_text: no
- public_route_created: no
- export_download_public_delivery_created: no
- human_review_required: yes
- no_automatic_trust_upgrade: yes

## Boundary Language

The future dense graph bridge smoke, if separately approved, is allowed to test whether an existing dense graph bridge can produce a local backend preview from a safe 8X-6 generated-run object.

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
- customer-ready report generation
- public event generation
- external delivery

Provider output remains evidence, not truth. The generated run remains selected-sample-only, controlled, uncalibrated, and human-review-required. Dense graph preview, if later produced, must remain anonymous aggregate/proxy and must not upgrade trust.
