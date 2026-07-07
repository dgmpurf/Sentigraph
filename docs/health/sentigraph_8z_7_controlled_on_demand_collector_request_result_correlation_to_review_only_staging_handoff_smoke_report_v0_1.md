# Sentigraph 8Z-7 Controlled On-demand Collector Review-only Staging Handoff Smoke Report v0.1

phase = 8Z-7
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
service_code_changed = no
source_path_step = on_demand_collector_request_result_correlation_to_review_only_staging_handoff
outer_8z7_phrase = APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE
review_only_staging_candidate_created = yes
review_only_staging_candidate_schema = sentigraph_on_demand_collector_review_only_staging_candidate_v0_1
review_only_staging_mode = backend_only_local_review_only_staging_handoff_candidate
source_request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1
package_reference_policy = opaque_safe_identifier_only
package_resolver_called = no
provider_result_reader_called = no
local_exchange_reader_called = no
persistent_staging_storage_created = no
actual_review_queue_runtime_used = no
production_review_queue_item_created = no
collector_job_run = no
provider_job_run = no
scheduler_created = no
http_bridge_created = no
webhook_created = no
private_collector_source_inspected = no
real_exchange_dir_read = no
real_package_dir_read = no
evidence_rows_parsed = no
evidence_layer_write = no
production_evidence_item_created = no
production_case_created = no
production_analysis_run_created = no
actual_analysis_execution_started = no
production_analysis_result_creation_authorized = no
production_analysis_result_created = no
8w69_pause_preserved = yes
8w70_reactivation_selected = no
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
future_next_boundary_recommendation = docs-only on-demand collector Route C entry / row-preview gate decision, not implementation

## Scope

8Z-7 is a backend-only, local-only, metadata-only controlled smoke. It proves that a safe 8Z-5-equivalent request/result correlation summary can be transformed inside a backend test path into the existing review-only staging helper input shape, then create a local review-only staging candidate object.

This smoke does not add product runtime behavior. It does not change services, routes, API contracts, frontend code, runtime persistence, package resolution, provider-result reading, local-exchange reading, row parsing, Evidence Layer write behavior, production objects, reports, Sandbox/public event runtime, export delivery, Source 11 runtime, or FinalSummaryReport runtime.

## Positive Proof

The focused test file creates a safe in-memory correlation summary with:

- `request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1`
- `request_metadata_schema = sentigraph_on_demand_collection_request_metadata_v0_1`
- `provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1`
- `request_id_match = true`
- `provider_result_id_unique_in_fixture_scope = true`
- `package_reference_policy = opaque_safe_identifier_only`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

The smoke then calls only the existing review-only staging helper surface with in-memory metadata and receives a local candidate summary:

- `review_only_staging_candidate_created = true`
- `review_only_staging_mode = backend_only_local_review_only_staging_handoff_candidate`
- `review_only_staging_handoff_performed = true`, controlled backend test path only
- `candidate_staging_status = ready_for_human_review`
- `candidate_review_status = ready_for_human_review`
- `candidate_promotion_status = promotion_required`
- `path_exposed = false`
- `path_reference = review_only_metadata_summary`

## Approval Phrase Safety

The 8Z-7 exact approval phrase is accepted only in the controlled smoke/test/report context:

`APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE`

The test proves missing, wrong, future, 8Z-6, 8Z-5, 8Z-4, 8Z-3, 8Z-2, 8Z-1, 8Y, and 8W phrases block before the staging helper is called.

The future 8Z-8 phrase is included only as inactive future wording and does not authorize anything in 8Z-7:

`APPROVE_8Z_8_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ENTRY_GATE_DECISION_DOCS_ONLY`

## No-call / No-read Proof

The focused test monkeypatches `Path.read_text`, `Path.read_bytes`, and `Path.open` to fail during the smoke. The passing test proves this controlled path does not perform file reads while creating the local review-only staging candidate from safe in-memory metadata.

The resulting smoke summary keeps all relevant side-effect flags false:

- `package_resolver_called = false`
- `provider_result_reader_called = false`
- `local_exchange_reader_called = false`
- `collector_job_run = false`
- `provider_job_run = false`
- `scheduler_created = false`
- `http_bridge_created = false`
- `webhook_created = false`
- `private_collector_source_inspected = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_items_jsonl_parsed = false`
- `evidence_items_csv_parsed = false`
- `source_manifest_rows_parsed = false`
- `collection_log_rows_parsed = false`

## Blocker Coverage

The test blocks before the staging helper call when any unsafe source state appears:

- wrong or unsafe correlation schema
- missing or false request-id match
- duplicate provider-result-id state
- non-opaque package reference policy
- `metadata_only = false`
- row content, raw identity, or secrets included
- package resolver / provider reader / local exchange reader call flags
- review-only staging already created or handoff already performed upstream
- collector/provider/scheduler/HTTP bridge/webhook flags
- real exchange or package directory read flags
- evidence row, evidence_items, source_manifest, or collection_log parsing flags
- Evidence Layer / production EvidenceItem / production case / production analysis_run flags
- actual analysis execution or production Analysis Result flags
- Source 11 / FinalSummaryReport / B-end / Sandbox / export delivery flags
- raw rows, raw comments, identities, author names/profile URLs, secrets, cookies, sessions, tokens, browser profile paths, private messages, response text, generated public messages, target-user lists, persuasion/truth/official/prediction/psychological fields
- automatic execution / publish / send / post / execute claims
- production-ready, customer-ready, public-ready, export-ready, final-ready, or Source-11-runtime-ready claims

## Interpretation Boundary

The 8Z-7 object is a local-only, backend-only, metadata-only review-only staging candidate in a controlled test path.

It is not persistent staging storage.
It is not Review Queue runtime.
It is not a production Review Queue item.
It is not production Evidence import.
It is not Evidence Layer write.
It is not production EvidenceItem / case / analysis_run / Analysis Result.
It is not actual analysis execution.
It is not Source 11 / FinalSummaryReport runtime.
It is not B-end report runtime.
It is not Sandbox/public event runtime.
It is not export/download/public/final delivery runtime.

## Validation

Focused test:

`python -m pytest backend/app/tests/test_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke.py -q`

Result: pass.

Nearby validation and static checks are reported in the final Codex response for this phase.

## Next Boundary

Recommended next task: docs-only on-demand collector Route C entry / row-preview gate decision, not implementation.
