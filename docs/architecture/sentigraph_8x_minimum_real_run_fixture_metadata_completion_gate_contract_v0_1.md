# Sentigraph 8X Minimum-real-run Fixture Metadata Completion Gate Contract v0.1

## Contract Purpose

This contract defines the boundary for a possible future 8X-6 controlled smoke that completes only the minimum fixture metadata required by the existing minimum-real-run wrapper.

The contract is docs-only in 8X-5. It does not add fixture metadata, execute the wrapper, create a generated run, call dense graph, create a report candidate, or create runtime state.

## Gate Object

```json
{
  "schema": "sentigraph_8x_minimum_real_run_fixture_metadata_completion_gate_v0_1",
  "phase": "8X-5",
  "decision": "ready",
  "docs_only": true,
  "privacy_issue_stop": false,
  "selected_next_boundary_option": "ready_for_8X_6_controlled_metadata_bridge_minimum_real_run_fixture_metadata_completion_smoke",
  "current_blocker": {
    "reason": "required_fixture_metadata_missing",
    "treated_as_safe_conservative_outcome": true
  },
  "allowed_future_input": {
    "input_kind": "metadata_only_minimum_real_run_input_candidate",
    "created_by": "8X-2/8X-4 metadata bridge path",
    "synthetic_or_temp_fixture_only": true,
    "minimum_fixture_metadata_only": true,
    "evidence_rows_allowed": false,
    "raw_comments_allowed": false,
    "raw_identities_allowed": false,
    "real_package_directory_allowed": false,
    "private_collector_source_allowed": false
  },
  "allowed_future_action": {
    "backend_only": true,
    "test_first": true,
    "controlled_smoke_only": true,
    "complete_existing_wrapper_required_fixture_metadata": true,
    "rerun_existing_minimum_real_run_wrapper": true,
    "local_controlled_generated_run_object_only": true,
    "dense_graph_allowed": false,
    "report_candidate_allowed": false,
    "route_allowed": false,
    "frontend_allowed": false,
    "runtime_persistence_allowed": false,
    "production_write_allowed": false
  },
  "required_future_output_constraints": {
    "minimum_real_run_executed": "true_only_inside_controlled_backend_test_path",
    "generated_run": "local_controlled_test_path_object_only",
    "generated_run_status": "non_blocked_only_if_existing_wrapper_contract_permits",
    "dense_graph_called": false,
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
    "empirical_validation": "not_started_or_existing_safe_local_equivalent"
  },
  "future_approval": {
    "exact_phrase_required": true,
    "exact_phrase": "APPROVE_8X_6_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_FIXTURE_METADATA_COMPLETION_SMOKE",
    "active_in_8x5": false,
    "production_authorization": false
  }
}
```

## Field Notes

- `decision`: `ready` means the docs-only fixture metadata completion gate is defined. It does not mean 8X-6 is authorized.
- `current_blocker`: records the 8X-4 wrapper result blocker and treats it as a safe conservative outcome.
- `allowed_future_input`: restricts future input to synthetic/temp metadata bridge candidates.
- `allowed_future_action`: restricts future work to minimum fixture metadata completion and wrapper rerun in a backend test path.
- `required_future_output_constraints`: prevents fixture metadata completion from becoming dense graph, report, production write, public output, or trust upgrade.
- `future_approval`: records the inactive future phrase required by a later prompt.

## Required Input Checklist for Future 8X-6

Future 8X-6 may proceed only if the prompt and local state confirm:

- exact future approval phrase is present
- input was created through the 8X-2 / 8X-4 metadata bridge path
- only minimum fixture metadata required by the existing wrapper is being completed
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
- no dense graph, report candidate, public output, route, frontend, or runtime persistence is requested
- no broad service behavior change is needed

## Blocker Categories

Future 8X-6 must stop on:

- evidence_row_parsing_required
- real_exchange_dir_required
- real_package_directory_required
- private_collector_inspection_required
- collector_job_required
- real_api_or_llm_required
- url_fetch_or_scrape_required
- evidence_layer_write_requested
- production_case_or_analysis_run_requested
- production_evidence_item_requested
- raw_identity_or_comment_exposure
- generated_response_text_requested
- dense_graph_or_report_candidate_requested
- route_frontend_or_runtime_persistence_requested
- export_download_public_delivery_requested
- broad_service_behavior_change_required
- automatic_trust_upgrade_requested
- production_authorization_confusion
- missing_or_changed_approval_phrase

## 8X-5 Non-execution Confirmation

- fixture_metadata_completed: no
- minimum_real_run_executed: no
- generated_run_created: no
- dense_graph_called: no
- report_candidate_created: no
- evidence_rows_parsed: no
- evidence_layer_write: no
- production_case_created: no
- production_analysis_run_created: no
- human_review_required: yes
- no_automatic_trust_upgrade: yes

## Boundary Language

The future fixture metadata completion smoke, if approved, is allowed to test whether the existing minimum-real-run wrapper can produce a non-blocked local test-path generated run from a safe metadata bridge candidate.

It is not allowed to claim:

- full-web coverage
- full-platform coverage
- official verification
- causal proof
- prediction
- production scoring
- production Analysis Result creation
- customer-ready report generation
- public event generation
- external delivery

Provider output remains evidence, not truth. Human review remains required.
