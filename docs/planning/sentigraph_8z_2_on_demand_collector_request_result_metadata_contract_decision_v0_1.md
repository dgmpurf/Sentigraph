# Sentigraph 8Z-2 On-demand Collector Request / Result Metadata Contract Decision v0.1

## A. Decision / Status

phase = 8Z-2
decision = ready
privacy_issue_stop = no
docs_only = yes
metadata_contract_only = yes
workflow_contract_only = yes
backend_code_changed = no
tests_changed = no
route_changed = no
frontend_changed = no
runtime_changed = no
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
selected_next_boundary_option = ready_for_8Z_3_controlled_on_demand_collector_request_metadata_fixture_smoke
future_8z3_exact_approval_phrase_required = yes
future_8z3_exact_approval_phrase_active = no
future_8z3_exact_approval_phrase = APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE
source_update_recommended_after_commit = no
source11_update_recommended = no
recommended_tag = no

## B. Purpose

8Z-2 defines the docs-only metadata contract for an on-demand collector request/result handoff.

It does not implement request runtime, result reader runtime, package resolver behavior, staging behavior, route/API, frontend, runtime persistence, scheduler, webhook, HTTP bridge, collector execution, provider execution, row parsing, Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result authorization, production Analysis Result creation, Source 11 runtime, FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, Project Source files, or GitHub Actions changes.

## C. 8Z-1 Workflow Summary

8Z-1 established the on-demand collector cooperation boundary:

- the collector is external to Sentigraph
- the collector is on-demand, not periodic
- the collector produces provider_result / package metadata outside Sentigraph runtime
- Sentigraph consumes safe metadata first
- Sentigraph remains a metadata consumer and governance runner
- review-only staging and Route C remain gated
- 8W-69 remains the controlling pause for production Analysis Result authorization

8Z-2 accepts that workflow only as a planning anchor and narrows it to request/result metadata contract design.

## D. Request Metadata Contract Decision

The future request metadata contract name should be:

`sentigraph_on_demand_collection_request_metadata_v0_1`

This name is docs-only in 8Z-2. It is not a backend schema and does not authorize a route, runtime object, or collector job.

Allowed request metadata fields:

- `request_id`
- `request_schema`
- `request_version`
- `case_id_hint`
- `event_slug`
- `event_title`
- `event_summary_safe_text`
- `topic_query_safe_text`
- `requested_platform_labels`
- `collection_goal`
- `collection_scope_note`
- `time_window_hint`
- `expected_output_contract`
- `expected_package_role`
- `operator_label`
- `request_created_at`
- `request_created_by_label`
- `safety_constraints`
- `review_required`
- `no_cookie_transfer = true`
- `no_secret_transfer = true`
- `no_browser_profile_transfer = true`
- `no_automatic_execution_by_sentigraph = true`
- `no_sentigraph_scheduler = true`
- `no_sentigraph_live_fetch = true`
- `no_automatic_trust_upgrade = true`
- `human_review_required = true`

Forbidden request metadata fields:

- platform passwords
- cookies
- sessions
- tokens
- browser profile paths
- proxy credentials
- captcha bypass instructions
- anti-bot bypass instructions
- hidden API endpoint instructions
- login instructions
- raw identity lists
- `target_user_list`
- `persuasion_score`
- `psychological_profile`
- `personality_diagnosis`
- private messages
- raw author IDs or raw author names
- profile URLs as actual values
- secrets
- `.env` values
- direct instruction for Sentigraph to scrape or fetch
- direct instruction for Sentigraph to run collector
- `auto_execute`, `publish_now`, `send_now`, `post_now`, or `execute_now`

## E. Request State Labels

Future request metadata may use these labels:

- `draft`
- `pending_operator_review`
- `ready_for_external_collector_task`
- `handed_to_external_collector`
- `external_collection_in_progress_external_only`
- `external_collection_completed`
- `provider_result_metadata_available`
- `package_metadata_available`
- `review_only_staging_candidate_ready`
- `blocked_by_safety_policy`
- `rejected_by_operator`
- `expired`
- `cancelled`

These are future metadata labels only. 8Z-2 does not implement a state machine.

## F. Result Metadata Contract Decision

The future on-demand result metadata contract name should be:

`sentigraph_on_demand_collector_provider_result_metadata_v0_1`

If implementation is later approved and the existing shape remains sufficient, reuse the existing `sentigraph_provider_job_result_v0_1` equivalent instead of creating a duplicate runtime schema.

Allowed result metadata fields:

- `provider_result_id`
- `provider_result_schema`
- `request_id`
- `provider_job_id`
- `external_collector_label`
- `collector_project_label`
- `package_name`
- `package_role`
- `package_schema_version`
- `package_reference_kind`
- `package_reference_safe_id`
- `validation_status`
- `validation_summary`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `coverage_note_summary`
- `platform_label_summary`
- `source_type_summary`
- `package_file_presence_map`
- `manifest_present`
- `validation_report_present`
- `coverage_note_present`
- `evidence_items_jsonl_present`
- `evidence_items_csv_present`
- `source_manifest_present`
- `collection_log_present`
- `export_timestamp`
- `provider_attestation_summary`
- `safety_markers`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

Forbidden result metadata fields:

- raw evidence row contents
- raw comment dumps
- full `evidence_items` content
- raw author IDs
- raw author names
- profile URLs as actual values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profile paths
- proxy credentials
- absolute private paths exposed to UI/API
- `source_manifest` row contents
- `collection_log` row contents
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- production-ready, customer-ready, public-ready, export-ready, or final-ready claims

## G. Result State Labels

Future result metadata may use these labels:

- `metadata_received`
- `metadata_schema_valid`
- `metadata_schema_invalid`
- `package_reference_valid`
- `package_reference_blocked`
- `package_metadata_ready`
- `validation_pass`
- `validation_warn`
- `validation_error`
- `review_only_ready`
- `blocked_pending_manual_review`
- `blocked_for_forbidden_metadata`
- `blocked_for_path_policy`
- `blocked_for_row_content_presence`
- `blocked_for_secret_or_identity_exposure`

These are future metadata labels only. 8Z-2 does not implement result reader runtime.

## H. Correlation Rules

- `request_id` must match or be linked by explicit correlation metadata.
- `provider_result_id` must be unique within the result metadata scope.
- `package_name` is an opaque safe identifier, not an executable path.
- `case_id_hint` is only a hint and does not create a production case.
- `event_slug` is only a label and does not create a route or public event.
- missing correlation requires manual review.
- mismatched `request_id` blocks automatic handoff.
- duplicate `provider_result_id` requires manual review.
- result metadata cannot auto-upgrade trust or create Evidence Layer records.

## I. Package Reference Policy

Package reference policy:

- use `package_name` or a safe package reference only.
- forbid path traversal.
- do not expose absolute private paths in UI/API.
- do not read arbitrary package directories in 8Z-2.
- do not read row files in 8Z-2.
- keep future path resolution separate and gated by existing safe resolver behavior or a future explicit smoke.
- record `evidence_items.jsonl` / `evidence_items.csv` presence as booleans only.
- record `source_manifest` / `collection_log` presence as booleans only.

## J. Metadata-first Gate Order

The future gate order is:

1. request metadata contract.
2. provider_result metadata contract.
3. safe result/package reference validation.
4. package metadata presence check.
5. review-only staging candidate.
6. future controlled row preview only with separate approval.
7. Route C gates remain separate.
8. 8W authorization remains separate for production Analysis Result.

## K. Relationship to Route C

8Z request/result metadata can only feed review-only staging or Route C entry after future gates.

Route C stage-complete status remains paused. 8Z-2 does not reopen actual analysis execution, does not authorize production Analysis Result, and does not change the 8Y-21 pause.

## L. Relationship to 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

8Z request/result metadata cannot authorize production Analysis Result creation and cannot satisfy the 8W-68 / 8W-69 authorization protocol.

## M. Relationship to Source 11 / Project Source

Source 11 update is not required unless runtime behavior changes.

8Z-2 does not change Analysis Request / Provider / Import Governance runtime.

8Z-2 must not create Project Source files and must not create `docs/project_sources`.

A future Source update may be considered only after a larger 8Z checkpoint, not after this single docs-only contract.

## N. Future Gates

Future gates may be considered only after explicit approval:

- 8Z-3 controlled request metadata fixture smoke
- 8Z-4 controlled provider_result metadata fixture smoke
- 8Z-5 controlled request/result correlation smoke
- 8Z-6 review-only staging handoff gate

Route C gates remain separate for row preview, Evidence, case, and analysis boundaries.

8W gates remain separate for production Analysis Result authorization.

## O. Future 8Z-3 Phrase Status

Future 8Z-3 exact approval phrase:

```text
APPROVE_8Z_3_CONTROLLED_ON_DEMAND_COLLECTOR_REQUEST_METADATA_FIXTURE_SMOKE
```

This phrase is inactive in 8Z-2. It does not authorize implementation, collector execution, provider jobs, HTTP bridge, webhook, scheduler, real exchange directory reads, row parsing, Evidence Layer write, production case, production analysis_run, actual analysis execution, or production Analysis Result.

## P. 8Z-2 Governance Interpretation

8Z-2 is a metadata-contract checkpoint only.

It makes the on-demand collector workflow easier to reason about, but it does not run the collector, does not ask Sentigraph to fetch or scrape, does not read real packages, does not parse evidence rows, does not promote trust, and does not create production objects.

The selected next boundary option is:

`ready_for_8Z_3_controlled_on_demand_collector_request_metadata_fixture_smoke`

That next step is not active until separately approved.
