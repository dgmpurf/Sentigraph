# Sentigraph 8Z-4 Controlled On-demand Collector Provider Result Metadata Fixture Smoke Report v0.1

## A. Status

phase = 8Z-4
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
test_only = yes
source_path_step = on_demand_collector_provider_result_metadata_fixture
outer_8z4_phrase = APPROVE_8Z_4_CONTROLLED_ON_DEMAND_COLLECTOR_PROVIDER_RESULT_METADATA_FIXTURE_SMOKE
provider_result_metadata_fixture_created = yes
provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1
provider_result_metadata_mode = backend_only_local_on_demand_provider_result_metadata_fixture
request_id_present = yes
request_result_correlation_performed = no
request_result_correlation_deferred_to_8z5 = yes
package_reference_policy = opaque_safe_identifier_only
package_file_presence_map_mode = boolean_presence_only
collector_job_run = no
provider_job_run = no
scheduler_created = no
http_bridge_created = no
webhook_created = no
private_collector_source_inspected = no
real_exchange_dir_read = no
real_package_dir_read = no
package_resolver_called = no
review_only_staging_created = no
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
future_next_boundary_recommendation = controlled request/result correlation smoke docs-only/test-only gate, not collector runtime

## B. Scope

8Z-4 is a backend-only, local-only, metadata-only, test-local controlled fixture smoke.

It proves only:

```text
exact 8Z-4 approval phrase
-> safe on-demand collector provider_result / package metadata fixture
-> local validation summary
```

It does not implement request runtime, result reader runtime, package resolver behavior, review-only staging behavior, backend route/API, frontend, runtime persistence, collector execution, provider execution, scheduler, HTTP bridge, webhook, real exchange/package reads, row parsing, Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result authorization, production Analysis Result creation, Source 11 runtime, FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, Project Source files, or GitHub Actions changes.

## C. Provider Result Metadata Fixture Proof

The focused test file creates a local fixture builder and validator inside the test module only:

`backend/app/tests/test_8z_4_controlled_on_demand_collector_provider_result_metadata_fixture_smoke.py`

The safe fixture requires:

- `provider_result_metadata_schema = sentigraph_on_demand_collector_provider_result_metadata_v0_1`
- `provider_result_metadata_mode = backend_only_local_on_demand_provider_result_metadata_fixture`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- opaque `provider_result_id`
- present `request_id` as an opaque correlation field only
- `request_result_correlation_performed = false`
- `request_result_correlation_deferred_to_8z5 = true`
- opaque `package_name`
- safe `package_reference_kind`
- opaque `package_reference_safe_id`
- allowed result state label
- boolean-only package file presence map
- boolean-only `evidence_items_jsonl_present`, `evidence_items_csv_present`, `source_manifest_present`, and `collection_log_present`
- safe text-only validation, coverage, and provider attestation summaries
- safety markers confirming metadata-only, no raw identity, no secrets, human review, and no automatic trust upgrade

## D. Approval Phrase Safety Proof

The exact accepted phrase is:

```text
APPROVE_8Z_4_CONTROLLED_ON_DEMAND_COLLECTOR_PROVIDER_RESULT_METADATA_FIXTURE_SMOKE
```

The test blocks missing or wrong phrases before fixture creation.

Regression phrase values from 8Z-3, 8Z-2, 8Z-1, 8Y, and 8W are rejected when presented alone. They are historical or not-authorizing contexts only.

## E. Blocker Proof

The focused tests block:

- forbidden provider_result metadata fields
- `metadata_only = false`
- `row_content_included = true`
- `raw_identity_included = true`
- `secrets_included = true`
- `human_review_required = false`
- `no_automatic_trust_upgrade = false`
- path-like or absolute `package_name`
- path-like or absolute `package_reference_safe_id`
- path-like `provider_result_id`
- non-boolean file presence fields
- embedded row content in `package_file_presence_map`
- raw rows, comments, identities, or secrets in validation / coverage / attestation summaries
- unsupported result state
- missing `provider_result_id`
- missing `request_id`

Request/result correlation is explicitly deferred to 8Z-5.

## F. No Collector / Runtime / Read Proof

The test-local fixture does not import or call collector/provider/package resolver/staging runtime.

The defensive no-read test monkeypatches `Path.read_text`, `Path.read_bytes`, and `Path.open` to fail if any file read is attempted during fixture creation. The fixture smoke passes without reading files.

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
- `request_result_correlation_performed = false`
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

## G. Future 8Z-5 Placeholder

Future 8Z-5 exact approval phrase:

```text
APPROVE_8Z_5_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_SMOKE
```

This phrase is inactive in 8Z-4. It does not authorize implementation, collector execution, provider jobs, request runtime, result reader runtime, package resolver behavior, staging behavior, request/result correlation runtime, HTTP bridge, webhook, scheduler, real exchange directory reads, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, production Analysis Result, report runtime, public event runtime, or delivery runtime.

## H. Recommendation

The next boundary may be discussed as a controlled request/result correlation smoke docs-only/test-only gate.

It must not be treated as collector runtime, provider runtime, scheduler, HTTP bridge, webhook, real package read, row parsing, Evidence Layer write, production object creation, or production Analysis Result authorization.
