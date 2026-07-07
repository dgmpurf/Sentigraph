# Sentigraph 8Z-9 Controlled On-demand Collector Review-only Staging to Route C Row-preview Smoke Report v0.1

phase = 8Z-9
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
service_code_changed = no
source_path_step = on_demand_collector_review_only_staging_to_route_c_row_preview
outer_8z9_phrase = APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE
repaired_8w7_inner_helper_phrase = APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION
source_adapter_schema = sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1
source_adapter_mode = backend_only_local_no_real_row_route_c_row_preview_entry_adapter
route_c_row_preview_entry_created = yes
redacted_review_only_row_preview_created = yes
row_preview_scope = controlled_synthetic_temp_fixture_only
controlled_row_preview_helper_called = yes, controlled backend test path only
synthetic_temp_row_fixture_used = yes
synthetic_temp_row_source_opened = yes, exact tmp_path evidence_items.jsonl only
real_exchange_dir_read = no
real_package_dir_read = no
production_package_rows_parsed = no
original_package_rows_read = no
arbitrary_package_dir_read = no
evidence_items_csv_parsed = no
source_manifest_rows_parsed = no
collection_log_rows_parsed = no
package_resolver_called = no
provider_result_reader_called = no
local_exchange_reader_called = no
review_only_staging_helper_called = no
controlled_evidence_candidate_called = no
downstream_route_c_evidence_candidate_created = no
evidence_layer_write = no
production_evidence_item_created = no
production_case_created = no
production_analysis_run_created = no
actual_analysis_execution_started = no
production_analysis_result_creation_authorized = no
production_analysis_result_created = no
actual_review_queue_runtime_used = no
production_review_queue_item_created = no
collector_job_run = no
provider_job_run = no
scheduler_created = no
http_bridge_created = no
webhook_created = no
private_collector_source_inspected = no
source11_runtime_called = no
actual_final_summary_report_created = no
b_end_report_runtime_generated = no
sandbox_public_event_runtime_generated = no
export_download_public_delivery_created = no
route_changed = no
frontend_changed = no
runtime_changed = no
raw_rows_exposed = no
raw_comments_exposed = no
raw_identities_exposed = no
author_names_or_profile_urls_exposed = no
secrets_read = no
human_review_required = yes
no_automatic_trust_upgrade = yes
8w69_pause_preserved = yes
8w70_reactivation_selected = no
future_next_boundary_recommendation = docs-only Route C row-preview completion / Evidence candidate gate decision, not downstream auto-run
repaired_8z8b_combined_suite_import_isolation_assertion = yes
repair_type = order_independent_no_new_import_or_call_guard

## Scope

8Z-9 is a backend-only, local-only, review-only controlled smoke. It proves that the 8Z-8B no-real-row Route C row-preview entry adapter candidate can be used as the source gate for a controlled Route C preview smoke with synthetic temp input only.

This phase changes no service code and adds no route, API, frontend, runtime persistence, production object, Evidence Layer write, Review Queue runtime, report runtime, Sandbox/public event runtime, export/download/public delivery runtime, Source 11 runtime, collector job, provider job, scheduler, HTTP bridge, or webhook.

## Positive Proof

The focused test builds a safe 8Z-8B-equivalent adapter candidate with:

- `adapter_schema = sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1`
- `adapter_mode = backend_only_local_no_real_row_route_c_row_preview_entry_adapter`
- `route_c_row_preview_entry_candidate_created = true`
- `metadata_only = true`
- all row-source, helper, package resolver, provider reader, local exchange reader, review-only staging helper, Evidence Layer, production object, route, frontend, and runtime flags false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

With the exact 8Z-9 outer phrase and repaired 8W-7 inner helper phrase, the controlled smoke creates a redacted review-only preview output in a backend test path only.

The row input is a tmp_path synthetic `evidence_items.jsonl` fixture with an explicit non-production marker. It contains no author IDs, author names, profile URLs, cookies, tokens, private content, real comments, or secrets.

## Approval Phrase Safety

Accepted outer phrase:

`APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE`

The focused test proves missing, wrong, 8Z-8C, 8Z-8B, 8Z-8, 8Z-7, 8Y, 8W-7, and future 8Z-10 phrases block before helper call and before any file open.

Required inner helper phrase when the row-preview helper is used:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

The focused test proves missing, wrong, old garbled, and old Chinese helper phrases block before any row-source access. The 8W-7 inner helper phrase cannot authorize 8Z-9 by itself.

Future 8Z-10 phrase is inactive future wording only:

`APPROVE_8Z_10_ROUTE_C_ROW_PREVIEW_COMPLETION_EVIDENCE_CANDIDATE_GATE_DECISION_DOCS_ONLY`

It does not authorize anything in 8Z-9.

## No Real-dir / Production-row / Downstream-run Proof

The focused test monkeypatches `Path.open`, `Path.read_text`, and `Path.read_bytes`.

Only the exact tmp_path synthetic `evidence_items.jsonl` file may be opened. Any other file access fails, including CSV, source manifest, collection log, `.env`, private paths, or paths outside the synthetic fixture.

The test also guards against importing package resolver, provider reader, local exchange reader, review-only staging helper, downstream Route C helpers, Evidence Layer helpers, Review Queue helpers, Source 11 / FinalSummaryReport helpers, B-end report helpers, Sandbox/public event helpers, and export/delivery helpers.

## Blocker Coverage

The focused test blocks before helper call and file open when the outer 8Z-9 phrase is missing or wrong.

It blocks before row-source access when the inner 8W-7 phrase is missing, wrong, old garbled, or old Chinese text.

It blocks unsafe adapter sources, including adapter schema mismatch, non-metadata source, row-source flags, existing preview flags, package resolver/provider/local exchange/review-only staging helper flags, real dir flags, Evidence Layer flags, production object flags, and raw exposure flags.

It blocks unsafe synthetic fixture input, including missing non-production marker, raw comments, identities, author names, profile URLs, cookies, token-like text, secret-like text, and real-looking URLs.

It blocks unsafe output attempts, including raw exposure, downstream Evidence candidate, Evidence Layer, production objects, and customer/public/production/final/export readiness claims.

## Production Side-effect Boundary

All production and downstream flags remain false:

- real exchange/package directory read
- production package row parsing
- original package row read
- arbitrary package directory read
- evidence_items.csv / source_manifest / collection_log parsing
- package resolver / provider reader / local exchange reader / review-only staging helper
- downstream Evidence candidate
- Evidence Layer write
- production EvidenceItem / case / analysis_run / Analysis Result
- actual analysis execution
- Review Queue runtime
- collector/provider job
- scheduler / HTTP bridge / webhook
- Source 11 / FinalSummaryReport / B-end / Sandbox / export / public delivery
- route / frontend / runtime changes

## Validation

Focused test:

`python -m pytest backend/app/tests/test_8z_9_controlled_on_demand_collector_review_only_staging_to_route_c_row_preview_smoke.py -q`

Result: pass.

Required nearby validation now passes after repairing the 8Z-8B import-isolation assertion. The repair keeps the import guard and file-read guard, snapshots `sys.modules` before the adapter operation, and asserts no new disallowed helper module appears during the adapter operation.

The repair does not remove modules from `sys.modules`, does not add cleanup hacks, does not call `controlled_row_preview`, does not use the 8W-7 helper phrase, and does not weaken the 8Z-8B no-read / no-helper-call proof.

## Next Boundary

Recommended next task:

8Z-10 docs-only Route C row-preview completion / Evidence candidate gate decision.

This is a docs-only gate. It must not auto-run downstream Route C evidence candidate, Review Queue, Evidence Layer, case, analysis, Analysis Result, Source 11, FinalSummaryReport, B-end, Sandbox/public event, or export/delivery runtime.
