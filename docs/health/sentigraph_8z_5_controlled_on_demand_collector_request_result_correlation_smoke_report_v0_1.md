# Sentigraph 8Z-5 Controlled On-demand Collector Request / Result Correlation Smoke Report v0.1

## A. Status

phase = 8Z-5
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
test_only = yes
source_path_step = on_demand_collector_request_result_correlation
outer_8z5_phrase = APPROVE_8Z_5_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_SMOKE
request_result_correlation_created = yes
request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1
request_result_correlation_mode = backend_only_local_on_demand_request_result_correlation_fixture
request_metadata_schema = sentigraph_on_demand_collection_request_metadata_v0_1
provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1
request_id_match = yes
provider_result_id_unique_in_fixture_scope = yes
package_reference_policy = opaque_safe_identifier_only
package_resolver_called = no
review_only_staging_created = no
review_only_staging_handoff_performed = no
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
future_next_boundary_recommendation = review-only staging handoff gate docs-only, not staging runtime

## B. Scope

8Z-5 is a backend-only, local-only, metadata-only, correlation-only, test-local controlled fixture smoke.

It proves only:

```text
8Z-3-equivalent safe request metadata fixture
+ 8Z-4-equivalent safe provider_result metadata fixture
+ exact 8Z-5 approval phrase
-> local request/result correlation summary object
```

It does not implement request runtime, result reader runtime, package resolver behavior, review-only staging behavior, backend route/API, frontend, runtime persistence, collector execution, provider execution, scheduler, HTTP bridge, webhook, real exchange/package reads, row parsing, Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result authorization, production Analysis Result creation, Source 11 runtime, FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, Project Source files, or GitHub Actions changes.

## C. Correlation Proof

The focused test file creates local request, result, and correlation helpers inside the test module only:

`backend/app/tests/test_8z_5_controlled_on_demand_collector_request_result_correlation_smoke.py`

The safe correlation summary requires:

- `request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1`
- `request_result_correlation_mode = backend_only_local_on_demand_request_result_correlation_fixture`
- `request_metadata_schema = sentigraph_on_demand_collection_request_metadata_v0_1`
- `provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1`
- exact `request_id` match
- request ID present in request and result
- provider result ID present
- provider result ID unique in fixture scope
- package name present and treated as opaque identifier
- `package_reference_policy = opaque_safe_identifier_only`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `request_result_correlation_performed = true` only in controlled test path
- `package_resolver_called = false`
- `review_only_staging_created = false`
- `review_only_staging_handoff_performed = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- `correlation_status = correlation_ready_for_manual_review`
- correlation does not create case, public event, or Evidence Layer record

## D. Approval Phrase Safety Proof

The exact accepted phrase is:

```text
APPROVE_8Z_5_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_SMOKE
```

The test blocks missing or wrong phrases before correlation creation.

Regression phrase values from 8Z-4, 8Z-3, 8Z-2, 8Z-1, 8Y, and 8W are rejected when presented alone. They are historical or not-authorizing contexts only.

## E. Blocker Proof

The focused tests block:

- missing request ID in request
- missing request ID in provider_result
- mismatched request ID
- duplicate provider_result ID
- forbidden request/result fields
- forbidden correlation output fields
- false request safety flags
- unsafe provider_result side-effect flags
- path-like request ID, provider_result ID, package name, or package reference
- production-case interpretation of `case_id_hint`
- route/public-event interpretation of `event_slug`
- non-boolean file presence values
- unsafe summary text containing raw rows, comments, identities, or secrets
- unsupported request or result state
- attempted package resolver call
- attempted review-only staging creation
- attempted review-only staging handoff

## F. No Collector / Runtime / Read Proof

The test-local fixture does not import or call collector/provider/package resolver/staging runtime.

The defensive no-read test monkeypatches `Path.read_text`, `Path.read_bytes`, and `Path.open` to fail if any file read is attempted during fixture creation or correlation. The correlation smoke passes without reading files.

False side-effect assertions preserve:

- `collector_job_run = false`
- `provider_job_run = false`
- `scheduler_created = false`
- `http_bridge_created = false`
- `webhook_created = false`
- `private_collector_source_inspected = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `package_resolver_called = false`
- `review_only_staging_created = false`
- `review_only_staging_handoff_performed = false`
- `evidence_rows_parsed = false`
- `evidence_items_jsonl_parsed = false`
- `evidence_items_csv_parsed = false`
- `source_manifest_rows_parsed = false`
- `collection_log_rows_parsed = false`
- `evidence_layer_write = false`
- `production_evidence_item_created = false`
- `production_case_created = false`
- `production_analysis_run_created = false`
- `actual_analysis_execution_started = false`
- `production_analysis_result_creation_authorized = false`
- `production_analysis_result_created = false`
- `8w69_pause_preserved = true`
- `8w70_reactivation_selected = false`
- `source11_runtime_called = false`
- `actual_final_summary_report_created = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_runtime_generated = false`
- `export_download_public_delivery_created = false`
- `route_changed = false`
- `frontend_changed = false`
- `runtime_changed = false`
- `raw_rows_exposed = false`
- `raw_comments_exposed = false`
- `raw_identities_exposed = false`
- `author_names_or_profile_urls_exposed = false`
- `secrets_read = false`

## G. Future 8Z-6 Placeholder

Future 8Z-6 exact approval phrase:

```text
APPROVE_8Z_6_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_HANDOFF_GATE_DECISION_DOCS_ONLY
```

This phrase is inactive in 8Z-5. It does not authorize implementation, collector execution, provider jobs, request runtime, result reader runtime, package resolver behavior, staging behavior, review-only staging handoff, HTTP bridge, webhook, scheduler, real exchange directory reads, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, production Analysis Result, report runtime, public event runtime, or delivery runtime.

## H. Recommendation

The next boundary may be discussed as a review-only staging handoff gate docs-only decision.

It must not be treated as staging runtime, collector runtime, provider runtime, scheduler, HTTP bridge, webhook, real package read, row parsing, Evidence Layer write, production object creation, or production Analysis Result authorization.
