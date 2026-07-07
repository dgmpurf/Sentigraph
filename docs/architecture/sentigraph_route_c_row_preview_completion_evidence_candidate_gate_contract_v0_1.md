# Sentigraph Route C Row-preview Completion / Evidence Candidate Gate Contract v0.1

phase = 8Z-10
contract_schema = sentigraph_route_c_row_preview_completion_evidence_candidate_gate_contract_v0_1
decision = blocked
privacy_issue_stop = no
docs_only = yes
gate_decision_only = yes
received_8z10_exact_approval_phrase = APPROVE_8Z_10_ROUTE_C_ROW_PREVIEW_COMPLETION_EVIDENCE_CANDIDATE_GATE_DECISION_DOCS_ONLY
backend_code_changed = no
tests_changed = no
route_changed = no
frontend_changed = no
runtime_changed = no
helper_called = no
row_preview_executed = no
controlled_row_preview_helper_called = no
controlled_evidence_candidate_called = no
controlled_evidence_candidate_created = no
downstream_route_c_auto_run = no
evidence_layer_write = no
production_evidence_item_created = no
actual_review_queue_runtime_used = no
production_review_queue_item_created = no
evidence_layer_import_candidate_created = no
production_case_created = no
production_analysis_run_created = no
actual_analysis_execution_started = no
production_analysis_result_creation_authorized = no
production_analysis_result_created = no
package_resolver_called = no
provider_result_reader_called = no
local_exchange_reader_called = no
review_only_staging_helper_called = no
collector_job_run = no
provider_job_run = no
scheduler_created = no
http_bridge_created = no
webhook_created = no
private_collector_source_inspected = no
real_exchange_dir_read = no
real_package_dir_read = no
production_package_rows_parsed = no
raw_rows_exposed = no
raw_comments_exposed = no
raw_identities_exposed = no
author_names_or_profile_urls_exposed = no
8w69_pause_preserved = yes
8w70_reactivation_selected = no
source11_runtime_called = no
actual_final_summary_report_created = no
b_end_report_runtime_generated = no
sandbox_public_event_runtime_generated = no
export_download_public_delivery_created = no
source_files_created = no
docs_project_sources_created = no
selected_next_boundary_option = pause_or_blocked_before_on_demand_collector_route_c_evidence_candidate_smoke
future_8z11_exact_approval_phrase_required = yes, after helper phrase repair
future_8z11_exact_approval_phrase_active = no
future_8z11_exact_approval_phrase = APPROVE_8Z_11_CONTROLLED_ON_DEMAND_COLLECTOR_ROUTE_C_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SMOKE
source_update_recommended_after_commit = no
source11_update_recommended = no
recommended_tag = no

## Purpose

This contract defines the 8Z-10 docs-only gate between a completed controlled Route C row-preview smoke and any future controlled Evidence candidate smoke.

8Z-10 does not create a candidate, does not execute a helper, does not read rows, and does not persist runtime state. It only records the gate decision, blocker categories, and the inactive future 8Z-11 boundary.

The received 8Z-10 phrase, `APPROVE_8Z_10_ROUTE_C_ROW_PREVIEW_COMPLETION_EVIDENCE_CANDIDATE_GATE_DECISION_DOCS_ONLY`, is used only for this docs-only decision context.

## Input Interpretation

The only acceptable future input family for a reopened 8Z-11 discussion is:

- 8Z-9 controlled row-preview smoke output or equivalent safe fixture.
- `row_preview_scope = controlled_synthetic_temp_fixture_only` or `in_memory_non_production_fixture_only`.
- `source_adapter_schema = sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1` or safe equivalent.
- `real_exchange_dir_read = false`.
- `real_package_dir_read = false`.
- `production_package_rows_parsed = false`.
- `original_package_rows_read = false`.
- `evidence_items_csv_parsed = false`.
- `source_manifest_rows_parsed = false`.
- `collection_log_rows_parsed = false`.
- `package_resolver_called = false`.
- `provider_result_reader_called = false`.
- `local_exchange_reader_called = false`.
- `review_only_staging_helper_called = false`.
- `downstream_route_c_evidence_candidate_created = false`.
- `evidence_layer_write = false`.
- `production_evidence_item_created = false`.
- `production_case_created = false`.
- `production_analysis_run_created = false`.
- `actual_analysis_execution_started = false`.
- `production_analysis_result_creation_authorized = false`.
- `production_analysis_result_created = false`.
- `raw_rows_exposed = false`.
- `raw_comments_exposed = false`.
- `raw_identities_exposed = false`.
- `author_names_or_profile_urls_exposed = false`.
- `human_review_required = true`.
- `no_automatic_trust_upgrade = true`.

## Existing Surface Contract

The existing Evidence candidate helper surface has the following useful shape:

- Candidate-set schema: `sentigraph_controlled_evidence_candidate_set_v0_1`.
- Candidate schema: `sentigraph_controlled_evidence_candidate_v0_1`.
- Summary schema: `sentigraph_controlled_evidence_candidate_summary_v0_1`.
- Candidate mode: backend-only local preview-derived candidate.
- Output flags keep Evidence Layer write and production object creation false.
- Candidate entries contain safe preview fields and boundary flags.
- Tests assert forbidden preview fields, requested downstream actions, runtime side effects, and file-open behavior remain blocked.

However, the helper approval phrase is encoding-unsafe. This contract therefore blocks 8Z-11 until the helper phrase is repaired or verified by a separate focused checkpoint.

## Future 8Z-11 Contract If Later Reopened

The future 8Z-11 phrase is:

`APPROVE_8Z_11_CONTROLLED_ON_DEMAND_COLLECTOR_ROUTE_C_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SMOKE`

This phrase is inactive in this contract and must appear only as future gate wording.

If later reopened after helper phrase repair, 8Z-11 must be:

- backend-only;
- test-first;
- controlled smoke only;
- local-only;
- review-only;
- candidate-only;
- limited to 8Z-9 controlled row-preview output or equivalent safe fixture;
- dependent only on a safe controlled Evidence candidate helper;
- blocked before any Evidence Layer, Review Queue, production object, route/API, frontend, Source 11, report, Sandbox, public event, export, download, public delivery, collector, provider, scheduler, HTTP bridge, webhook, real API, real LLM, URL fetch, or scraping action.

## Future 8Z-11 Output Constraints

If later approved, a controlled 8Z-11 smoke may produce only a local controlled Evidence candidate object inside a backend test path. Its output must satisfy:

- `controlled_evidence_candidate_created = true` only inside controlled backend test path.
- `evidence_candidate_schema = sentigraph_controlled_evidence_candidate_v0_1` or safe equivalent.
- `evidence_candidate_mode = backend_only_local_controlled_evidence_candidate` or safe equivalent.
- `candidate_only = true`.
- `review_only = true`.
- `evidence_layer_write = false`.
- `production_evidence_item_created = false`.
- `actual_review_queue_runtime_used = false`.
- `production_review_queue_item_created = false`.
- `evidence_layer_import_candidate_created = false` unless a future separate gate authorizes it.
- `production_case_created = false`.
- `production_analysis_run_created = false`.
- `production_analysis_result_created = false`.
- `raw_rows_exposed = false`.
- `raw_comments_exposed = false`.
- `raw_identities_exposed = false`.
- `author_names_or_profile_urls_exposed = false`.
- `real_exchange_dir_read = false`.
- `real_package_dir_read = false`.
- `production_package_rows_parsed = false`.
- `source11_runtime_called = false`.
- `actual_final_summary_report_created = false`.
- `b_end_report_runtime_generated = false`.
- `sandbox_public_event_runtime_generated = false`.
- `export_download_public_delivery_created = false`.
- `route_ready = false`.
- `frontend_ready = false`.
- `production_ready = false`.
- `customer_ready = false`.
- `public_ready = false`.
- `human_review_required = true`.
- `no_automatic_trust_upgrade = true`.

## Stop Rules

Stop before future 8Z-11 if any of the following are true:

- Evidence candidate helper approval phrase remains encoding-unsafe.
- The helper phrase is missing, ambiguous, or not covered by positive and negative tests.
- The helper opens files, reads arbitrary package paths, reads real exchange dirs, or parses production package rows.
- The helper emits raw rows, raw comments, raw identities, author names, profile URLs, cookies, sessions, tokens, private paths, or secrets.
- The helper writes Evidence Layer data or creates production EvidenceItem records.
- The helper calls Review Queue runtime or creates production Review Queue items.
- The helper creates Evidence Layer import candidate automatically.
- The helper creates production case, production analysis run, actual analysis execution, or production Analysis Result.
- The helper requires route/API, frontend, runtime persistence, Source 11, FinalSummaryReport, B-end report, Sandbox/public event, export/download/public delivery, collector/provider job, scheduler, HTTP bridge, webhook, real API, real LLM, URL fetch, or scraping.
- The helper asserts customer/public/production/final/export readiness.

## Relationship Boundaries

8Z-10 does not change runtime behavior and does not require a Source 11 update. It must not create Project Source files or `docs/project_sources`.

8W-69 pause remains preserved. 8W-70 reactivation remains not selected. This contract cannot satisfy any 8W production Analysis Result authorization protocol.

Route C does not auto-run after row preview. Evidence candidate, Review Queue candidate, Evidence Layer import candidate, Evidence Layer write candidate, production EvidenceItem, production case, production analysis run, actual analysis execution, and Analysis Result each require separate gated decisions.
