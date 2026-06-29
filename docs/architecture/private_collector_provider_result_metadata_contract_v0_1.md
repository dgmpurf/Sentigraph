# Private Collector Provider Result Metadata Contract v0.1

Status: docs-only contract. This document defines future metadata shapes and safety boundaries. It does not implement backend schemas, routes, tests, frontend UI, provider execution, collector execution, package import, Evidence Layer writes, case creation, analysis, reports, Sandbox generation, public event generation, or strategy execution.

## 1. Purpose

This contract defines how Sentigraph should interpret private collector provider result metadata and Evidence Export package metadata in a local-file exchange workflow.

Provider output is evidence, not truth. Package metadata may become review-ready input later, but it is not production evidence, not official verification, not a report, not a public event, and not a generated response.

## 2. Object A: `sentigraph_collector_package_index_v0_1`

### Required Fields

- `schema`: `sentigraph_collector_package_index_v0_1`
- `schema_version`
- `generated_at`
- `safety`
- `summary`
- `packages`

Each package entry should include:

- `package_name`
- `package_role`
- `case_id`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `recommended_for_sentigraph_demo`

### Optional Fields

- `package_path_relative_to_export_root`
- `sample_quality_label`
- `comment_count`
- `root_count`
- `exported_at`
- `notes`
- `demo_recommendation`

### Legacy / Ambiguous Fields

- `package_path_relative`

If the base is unclear, this field is not canonical and should produce `manual_review_required` unless `package_name` resolves safely under `configured_export_root`.

### Forbidden Fields

- `cookie`
- `token`
- `session`
- `password`
- `api_key`
- `browser_profile`
- `profile_path`
- `raw_author_id` as an actual exported identifier
- `raw_author_name` as an actual exported identifier
- `profile_url` as an actual exported value
- `private_message` as an actual exported value
- `raw_comment_dump`
- `full_evidence_rows`
- `absolute_media_path`
- `collector_runtime_internal_path`

### Safety Markers

The index should include or allow safety markers such as:

- `real_apis_called=false`
- `url_fetching_or_scraping=false`
- `cookies_accounts_sessions_used=false`
- `secrets_read_or_printed=false`
- `raw_author_identifiers_exposed=false`
- `raw_comment_dumps_included=false`

Safety markers are not the same as exported secret or identifier values.

## 3. Object B: `sentigraph_provider_job_result_v0_1`

### Required Fields

- `schema`: `sentigraph_provider_job_result_v0_1`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `provider_type`
- `adapter_id`
- `contract_version`
- `status`
- `package_contract`
- `package_reference`
- `metadata_summary`
- `validation_summary`
- `coverage_note`
- `safety_markers`
- `created_at`

### Required `package_reference` Fields

- `package_name`
- `package_role`
- `package_index_ref`
- `package_locator_strategy`

Allowed `package_locator_strategy` values:

- `package_name_under_configured_export_root`
- `package_path_relative_to_export_root`
- `manual_review_required_legacy_path`

### Optional Fields

- `case_id`
- `case_title`
- `sample_quality_label`
- `package_path_relative_to_export_root`
- `warnings`
- `errors`
- `next_action`
- `operator_notes`

### Status Values

- `accepted_metadata_only`
- `package_ready`
- `validation_passed`
- `validation_warn`
- `manual_review_required`
- `adapter_required`
- `field_quality_weak`
- `blocked_safety`
- `blocked_path_escape`
- `blocked_missing_package`
- `blocked_privacy_issue`
- `unsupported_platform`
- `live_collection_not_authorized`

### Forbidden Fields

Provider result metadata must not include:

- cookies, tokens, sessions, passwords, salts, API keys, saved login state
- browser profile paths
- proxy credentials
- crawler runtime internals
- raw author ids
- raw author names
- profile URLs as actual values
- private messages as actual values
- raw comment dumps
- full evidence rows
- absolute media paths
- absolute package paths for frontend/API exposure
- generated public response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

### Privacy Behavior

If any forbidden field appears as an actual exported value, status must be `blocked_privacy_issue`.

If metadata contains marker fields such as `raw_author_id_exported=false`, `raw_author_name_exported=false`, `profile_url_exported=false`, `raw_author_id_removed=true`, or `raw_author_name_removed=true`, these should be treated as safety markers, not as raw identifier exposure.

## 4. Object C: `sentigraph_evidence_export_package_metadata_v0_1`

### Required Fields

- `schema`: `sentigraph_evidence_export_package_metadata_v0_1`
- `package_name`
- `package_role`
- `case_id`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `coverage_note_exists`
- `validation_report_exists`
- `manifest_exists`
- `required_files_presence`
- `privacy_markers`

### Required `required_files_presence` Keys

- `manifest.json`
- `source_manifest.jsonl`
- `evidence_items.jsonl`
- `evidence_items.csv`
- `collection_log.jsonl`
- `coverage_note.md`
- `README.md`
- `validation_report.json`
- `validation_report.md`

Existence checks are allowed. Parsing `evidence_items.jsonl` or `evidence_items.csv` is not allowed in metadata-only handoff.

### Required Privacy Markers

- `raw_author_id_exported=false`
- `raw_author_name_exported=false`
- `profile_url_exported=false`
- `no_private_messages=true`
- `no_saved_credentials=true`
- `no_captcha_bypass=true`
- `no_anti_bot_bypass=true`

### Optional Fields

- `recommended_default_trust_label`
- `legal_review_status`
- `coverage_summary`
- `comment_count`
- `root_count`
- `skipped_sources_count`
- `source_manifest_exists`
- `collection_log_exists`

### Status Handling

If validation status is `passed`, package metadata may be `accepted_metadata_only`.

If validation status is `warn`, package metadata may be `validation_warn` and should remain `manual_review_required`.

If metadata is missing required privacy markers, status should be `manual_review_required` or `blocked_privacy_issue` depending on severity.

## 5. Object D: `sentigraph_search_to_case_request_context_v0_1` (Future Only)

This object is future planning only. It is not implemented in this phase.

### Future Required Fields

- `schema`: `sentigraph_search_to_case_request_context_v0_1`
- `request_id`
- `user_query`
- `query_type`
- `event_or_entity_hint`
- `platform_scope`
- `time_window`
- `requested_output`
- `safety_mode`
- `allow_live_collection`
- `provider_selection`
- `expected_handoff`

### Future Alignment

User search should eventually create:

1. `analysis_request`
2. `provider_request`
3. `provider_job_result` metadata
4. package reference
5. review-only staging candidate
6. future case workspace after gates

### Current Boundary

This phase does not implement:

- search UI
- request submission
- collector execution
- live collection
- Evidence import
- case creation
- `analysis_run`
- report runtime
- Sandbox/public event runtime
- strategy execution

## 6. Path Handling Rules

All metadata objects should follow the path policy in `private_collector_package_path_resolution_policy_v0_1.md`.

Rules:

- Prefer `package_name` under `configured_export_root`.
- Allow `package_path_relative_to_export_root` only when explicitly declared.
- Treat legacy `package_path_relative` as ambiguous unless `package_name` resolves safely.
- Block path traversal.
- Block package metadata that resolves outside `configured_export_root`.
- Never expose absolute private paths to frontend/UI/API responses.

## 7. Safety Markers Versus Actual Secret Fields

The contract must distinguish:

- actual secret or identifier fields, which are forbidden
- safety marker fields, which are allowed when they indicate non-export or removal

Allowed marker examples:

- `raw_author_id_exported=false`
- `raw_author_name_exported=false`
- `profile_url_exported=false`
- `raw_author_id_removed=true`
- `raw_author_name_removed=true`
- `no_private_messages=true`

Forbidden actual value examples:

- `"raw_author_id": "actual-id"`
- `"raw_author_name": "actual-name"`
- `"profile_url": "actual-profile-url"`
- `"private_message": "actual-private-content"`
- `"token": "actual-token"`
- `"session": "actual-session"`

## 8. Recommended Future Implementation Boundary

A future implementation may add a tiny metadata-only resolver/helper and tests.

It must not:

- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- call real APIs
- call real LLMs
- run collector jobs
- import collector code
- create an HTTP/API bridge to the collector
- write Evidence Layer
- create a production case
- create an `analysis_run`
- generate reports
- generate Sandbox/public event runtime
- generate public response text
- publish, send, post, or execute platform actions

