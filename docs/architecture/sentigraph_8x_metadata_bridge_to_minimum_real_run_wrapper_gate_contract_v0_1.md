# Sentigraph 8X Metadata Bridge to Minimum-real-run Wrapper Gate Contract v0.1

## Contract Purpose

This contract defines the boundary between the 8X metadata-only bridge candidate and any future controlled minimum-real-run wrapper smoke.

The contract is docs-only in 8X-3. It does not execute the wrapper, create a generated run, call dense graph, or create any runtime object.

## Gate Object

```json
{
  "schema": "sentigraph_8x_metadata_bridge_to_minimum_real_run_wrapper_gate_v0_1",
  "phase": "8X-3",
  "decision": "ready",
  "docs_only": true,
  "privacy_issue_stop": false,
  "selected_next_boundary_option": "ready_for_8X_4_controlled_metadata_bridge_minimum_real_run_wrapper_execution_smoke",
  "allowed_future_input": {
    "input_kind": "metadata_only_minimum_real_run_input_candidate",
    "created_by": "8X-2 staging candidate generated-run bridge",
    "provider_metadata_only": true,
    "review_only_staging_metadata_only": true,
    "synthetic_or_temp_fixture_only": true,
    "evidence_rows_allowed": false,
    "raw_comments_allowed": false,
    "raw_identities_allowed": false
  },
  "allowed_future_action": {
    "backend_only": true,
    "test_first": true,
    "controlled_smoke_only": true,
    "execute_minimum_real_run_wrapper_from_safe_candidate_only": true,
    "dense_graph_allowed": false,
    "report_candidate_allowed": false,
    "route_allowed": false,
    "frontend_allowed": false,
    "runtime_persistence_allowed": false
  },
  "required_future_output_constraints": {
    "minimum_real_run_executed": "true_only_inside_controlled_backend_test_path",
    "generated_run": "local_controlled_test_path_object_only",
    "dense_graph_called": false,
    "report_candidate_created": false,
    "evidence_rows_parsed": false,
    "evidence_layer_write": false,
    "production_case_created": false,
    "production_analysis_run_created": false,
    "human_review_required": true,
    "no_automatic_trust_upgrade": true
  },
  "future_approval": {
    "exact_phrase_required": true,
    "exact_phrase": "APPROVE_8X_4_CONTROLLED_METADATA_BRIDGE_MINIMUM_REAL_RUN_WRAPPER_EXECUTION_SMOKE",
    "active_in_8x3": false,
    "production_authorization": false
  }
}
```

## Field Notes

- `decision`: `ready` means the docs-only gate criteria are defined. It does not mean 8X-4 is authorized.
- `selected_next_boundary_option`: names the next possible boundary only.
- `allowed_future_input`: restricts future input to the 8X-2 metadata-only candidate path.
- `allowed_future_action`: restricts future work to a backend-only controlled smoke.
- `required_future_output_constraints`: prevents wrapper smoke from becoming dense graph, report, public output, Evidence Layer, production case, or production analysis runtime.
- `future_approval`: records the inactive future phrase required by a later prompt.

## Required Input Checklist for Future 8X-4

Future 8X-4 may proceed only if the prompt and local state confirm:

- exact future approval phrase is present
- input was created through the 8X-2 metadata bridge path
- no evidence rows are needed
- no raw comments or raw identities are present
- no author names or profile URLs are present as actual values
- no private collector source inspection is needed
- no real exchange directory read is needed
- no collector job is needed
- no real API, real LLM, URL fetching, or scraping is needed
- no Evidence Layer write is requested
- no production case or production analysis_run is requested
- no dense graph, report candidate, public output, route, frontend, or runtime persistence is requested

## Blocker Categories

Future 8X-4 must stop on:

- evidence_row_parsing_required
- real_exchange_dir_required
- private_collector_inspection_required
- collector_job_required
- real_api_or_llm_required
- url_fetch_or_scrape_required
- evidence_layer_write_requested
- production_case_or_analysis_run_requested
- raw_identity_or_comment_exposure
- generated_response_text_requested
- dense_graph_or_report_candidate_requested
- route_frontend_or_runtime_persistence_requested
- export_download_public_delivery_requested
- production_authorization_confusion
- missing_or_changed_approval_phrase

## 8X-3 Non-execution Confirmation

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

The future wrapper smoke, if approved, is allowed to test compatibility with a safe local metadata candidate. It is not allowed to claim:

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
