# Sentigraph 8Z-6 On-demand Collector Review-only Staging Handoff Gate Decision v0.1

## A. Decision / Status

phase = 8Z-6
decision = ready
privacy_issue_stop = no
docs_only = yes
gate_decision_only = yes
review_only_staging_handoff_gate_only = yes
backend_code_changed = no
tests_changed = no
route_changed = no
frontend_changed = no
runtime_changed = no
helper_called = no
package_resolver_called = no
provider_result_reader_called = no
local_exchange_reader_called = no
review_only_staging_created = no
review_only_staging_handoff_performed = no
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
source_files_created = no
docs_project_sources_created = no
selected_next_boundary_option = ready_for_8Z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke
future_8z7_exact_approval_phrase_required = yes
future_8z7_exact_approval_phrase_active = no
future_8z7_exact_approval_phrase = APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE
source_update_recommended_after_commit = no
source11_update_recommended = no
recommended_tag = no

## B. Purpose

8Z-6 decides whether the 8Z-5 local controlled request/result correlation summary may be considered for a future controlled review-only staging handoff smoke.

It is docs-only. It does not implement the handoff, call helper code, call package resolver, call provider result reader, call local exchange reader, create review-only staging candidate, create persistent staging storage, create Review Queue runtime, run collector/provider jobs, read real package or exchange directories, parse rows, write Evidence Layer, create production objects, authorize production Analysis Result, or reactivate 8W-70.

## C. 8Z State Summary

- 8Z-1 created the on-demand collector workflow contract as docs-only.
- 8Z-2 created the request/result metadata contract as docs-only.
- 8Z-3 completed controlled request metadata fixture smoke.
- 8Z-4 completed controlled provider_result metadata fixture smoke.
- 8Z-5 completed controlled request/result correlation smoke.
- 8Z-6 is only a review-only staging handoff gate decision.
- 8Y Route C remains stage-complete and paused.
- 8W-69 pause remains preserved.

## D. 8Z-5 Output Interpretation

8Z-5 produced only a local controlled request/result correlation summary:

- `request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1`
- `request_result_correlation_mode = backend_only_local_on_demand_request_result_correlation_fixture`
- metadata-only
- controlled backend test path only
- package resolver not called
- review-only staging not created
- no review-only staging handoff performed
- no row parsing
- no Evidence Layer write
- no production EvidenceItem, case, analysis_run, or Analysis Result
- no trust upgrade
- `human_review_required = true`

This output may be considered only as a future input candidate. It is not review-only staging, not Review Queue, not Evidence Layer, not production case, and not analysis authorization.

## E. Review-only Staging Surface Audit Summary

| Surface | Classification | Relation to 8Z | Side effects |
| --- | --- | --- | --- |
| `backend/app/services/private_collector_review_only_staging.py` | backend_helper | review_only_staging_candidate | metadata_only; no_persistence flags; no production flags |
| `backend/app/tests/test_private_collector_review_only_staging.py` | test_only | review_only_staging_candidate tests | test_local_only |
| `backend/app/services/private_collector_provider_result_reader.py` | backend_helper | provider_result/package_resolution | package_read_possible through resolver path; default not allowed in 8Z-7 |
| `backend/app/services/private_collector_package_resolver.py` | backend_helper | package_resolution | package_read_possible; default not allowed in 8Z-7 |
| `backend/app/services/local_exchange_reader.py` | runtime_helper | provider_result metadata read | metadata_only when explicitly configured; default not allowed in 8Z-7 |
| `docs/architecture/review_only_staging_import_contract_v0_1.md` | docs_only | review-only staging boundary contract | no runtime |
| `backend/app/tests/test_8z_5_controlled_on_demand_collector_request_result_correlation_smoke.py` | test_only | correlated_metadata_source | test_local_only; no reads |

Existing code has a review-only staging helper surface and tests. It does not show a need for persistent staging storage in the helper surface. Existing package resolver, provider result reader, and local exchange reader are adjacent surfaces and must remain uncalled by default in 8Z-7 unless a separate gate explicitly allows them.

## F. Gate Interpretation

8Z-6 allows only a future local controlled review-only staging handoff smoke discussion.

Future 8Z-7 may transform an 8Z-5-style correlated metadata summary into a local controlled review-only staging candidate object only if the existing safe helper surface supports it without widening behavior.

Future 8Z-7 must not:

- create persistent staging storage
- create actual Review Queue runtime
- create production Review Queue item
- call package resolver unless a later explicit gate allows it
- read real exchange or package directories
- parse row files
- write Evidence Layer
- create production EvidenceItem, case, analysis_run, or Analysis Result
- call Source 11, FinalSummaryReport, B-end report, Sandbox/public event, export, or delivery runtime

## G. Allowed Future 8Z-7 Input

Allowed future input is only an 8Z-5 local controlled request/result correlation summary or equivalent safe fixture with:

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
- `package_resolver_called = false`
- `review_only_staging_created = false`
- `review_only_staging_handoff_performed = false`
- `collector_job_run = false`
- `provider_job_run = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- production objects all false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## H. Allowed Future 8Z-7 Action

If separately approved, future 8Z-7 may be:

- backend-only
- test-first
- controlled smoke only
- local-only
- metadata-only
- handoff-candidate-only
- using only existing safe review-only staging helper if safe
- allowed to create a local controlled review-only staging candidate object only inside backend test path

It must preserve human review and no automatic trust upgrade.

## I. Future 8Z-7 Output Constraints

Future 8Z-7 output constraints:

- `review_only_staging_candidate_created` may be true only inside controlled backend test path
- `review_only_staging_candidate_schema = sentigraph_on_demand_collector_review_only_staging_candidate_v0_1` or existing safe equivalent as local boundary wording only
- `review_only_staging_mode = backend_only_local_review_only_staging_handoff_candidate` or safe equivalent
- `persistent_staging_storage_created = false`
- `actual_review_queue_runtime_used = false`
- `production_review_queue_item_created = false`
- `package_resolver_called = false` by default
- `provider_result_reader_called = false` by default
- `local_exchange_reader_called = false` by default
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- `production_evidence_item_created = false`
- `production_case_created = false`
- `production_analysis_run_created = false`
- `actual_analysis_execution_started = false`
- `production_analysis_result_creation_authorized = false`
- `production_analysis_result_created = false`
- `source11_runtime_called = false`
- `actual_final_summary_report_created = false`
- `b_end_report_runtime_generated = false`
- `sandbox_public_event_runtime_generated = false`
- `export_download_public_delivery_created = false`
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `customer_ready = false`
- `public_ready = false`
- `raw_rows_exposed = false`
- `raw_comments_exposed = false`
- `raw_identities_exposed = false`
- `author_names_or_profile_urls_exposed = false`
- `secrets_read = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## J. Hard Blockers For Future 8Z-7

Block future 8Z-7 if:

- no safe review-only staging helper surface is available
- helper requires package resolver call or real package directory read
- helper requires row file parsing
- helper creates persistent staging storage
- helper creates actual Review Queue runtime or production Review Queue item
- helper writes Evidence Layer
- helper creates production EvidenceItem, case, analysis_run, or Analysis Result
- helper requires route/API/frontend
- helper requires collector/provider job execution
- helper requires scheduler, HTTP bridge, or webhook
- helper exposes raw rows, raw comments, raw identities, or actual profile URLs
- helper requires secrets, cookies, sessions, or browser profiles
- helper requires real API, LLM, URL fetch, or scraping
- helper makes customer/public/production-ready claims

## K. Relationship to Route C

Future 8Z-7, if later approved, may only create a local review-only staging candidate.

Route C row preview, Evidence, case, and analysis gates remain separate.

8Z-6 and future 8Z-7 do not reopen actual analysis execution and do not authorize production Analysis Result.

## L. Relationship to 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

Review-only staging handoff cannot satisfy the 8W-68 / 8W-69 authorization protocol.

## M. Relationship to Source 11 / Project Source

Source 11 update is not required unless runtime behavior changes.

8Z-6 does not change runtime behavior.

8Z-6 must not create Project Source files or `docs/project_sources`.

Future Source update may be considered after a larger 8Z checkpoint, not after this single docs-only gate.

## N. Future 8Z-7 Phrase Status

Future 8Z-7 exact approval phrase:

```text
APPROVE_8Z_7_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_RESULT_CORRELATION_TO_REVIEW_ONLY_STAGING_HANDOFF_SMOKE
```

This phrase is inactive in 8Z-6. It does not authorize implementation in 8Z-6, collector execution, provider jobs, request runtime, result reader runtime, package resolver behavior, real exchange/package directory reads, row parsing, persistent staging storage, actual Review Queue runtime, Evidence Layer write, production case, production analysis_run, actual analysis execution, or production Analysis Result.

## O. Final Decision

8Z-6 selects:

`ready_for_8Z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke`

This selection is a future gate only. It does not authorize implementation now.
