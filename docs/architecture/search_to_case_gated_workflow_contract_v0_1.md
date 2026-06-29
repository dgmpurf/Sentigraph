# Search-to-Case Gated Workflow Contract v0.1

Status: architecture contract only. This document does not implement backend code, frontend code, routes, tests, runtime persistence, collector jobs, Evidence import, production case creation, analysis runs, reports, Sandbox/public event runtime, or public response behavior.

## A. Contract Objects

### 1. `search_to_case_user_context_v0_1`

Future fields:

- `request_id`
- `user_query`
- `query_type`
- `entity_or_event_hint`
- `platform_scope`
- `time_window`
- `requested_output`
- `safety_mode`
- `allow_live_collection`
- `provider_selection`
- `created_at`

Purpose: capture user search intent without treating the query as authorization to collect live data.

### 2. `search_to_case_analysis_request_v0_1`

Future fields:

- `analysis_request_id`
- `search_context_ref`
- `requested_case_title`
- `topic_summary`
- `source_scope`
- `requested_modules`
- `safety_mode`
- `status`
- `created_at`

Purpose: draft a governed request for a possible case workspace, not a production case.

### 3. `search_to_case_provider_request_v0_1`

Future fields:

- `provider_request_id`
- `analysis_request_id`
- `provider_type`
- `adapter_id`
- `collection_mode`
- `package_expected`
- `live_collection_authorized`
- `status`
- `created_at`

Purpose: define what a provider would be asked for after authorization and gate checks. It does not execute a provider by itself.

### 4. `search_to_case_provider_result_ref_v0_1`

Future fields:

- `provider_result_id`
- `provider_job_id`
- `package_reference`
- `metadata_summary`
- `validation_summary`
- `safety_markers`
- `status`
- `created_at`

Purpose: reference metadata-only provider output and package metadata. It is not Evidence Layer data.

### 5. `search_to_case_review_staging_candidate_v0_1`

Future fields:

- `staging_candidate_id`
- `analysis_request_id`
- `provider_result_id`
- `package_name`
- `case_id_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `review_status`
- `promotion_status`
- `blockers`
- `warnings`
- `created_at`

Purpose: hold safe metadata for future review-only staging. It does not import evidence rows.

### 6. `search_to_case_workspace_candidate_v0_1`

Future fields:

- `workspace_candidate_id`
- `case_id`
- `case_title`
- `query_context_ref`
- `provider_result_refs`
- `package_refs`
- `review_state`
- `dedup_state`
- `evidence_promotion_state`
- `allowed_modules`
- `blocked_modules`
- `audit_refs`
- `safety_flags`
- `created_at`

Purpose: represent a governed workspace candidate after staging, review, dedup, and promotion gates. It is not public output and not automatically production evidence.

## B. Gate States

Allowed state vocabulary:

- `search_received`
- `analysis_request_drafted`
- `provider_request_drafted`
- `provider_result_metadata_received`
- `package_reference_ready`
- `metadata_validation_passed`
- `metadata_validation_warn`
- `manual_review_required`
- `review_only_staging_candidate`
- `evidence_review_required`
- `dedup_required`
- `promotion_required`
- `workspace_candidate_ready`
- `blocked_missing_package`
- `blocked_path_escape`
- `blocked_privacy_issue`
- `blocked_live_collection_not_authorized`
- `blocked_unsupported_platform`
- `blocked_metadata_contract`
- `production_import_blocked`

## C. Allowed Transitions

Allowed transitions:

```text
search_received -> analysis_request_drafted
analysis_request_drafted -> provider_request_drafted
provider_request_drafted -> provider_result_metadata_received
provider_result_metadata_received -> package_reference_ready
package_reference_ready -> metadata_validation_passed
package_reference_ready -> metadata_validation_warn
package_reference_ready -> blocked_missing_package
package_reference_ready -> blocked_path_escape
package_reference_ready -> blocked_privacy_issue
package_reference_ready -> blocked_live_collection_not_authorized
package_reference_ready -> blocked_unsupported_platform
package_reference_ready -> blocked_metadata_contract
metadata_validation_passed -> review_only_staging_candidate
metadata_validation_warn -> manual_review_required
review_only_staging_candidate -> evidence_review_required
evidence_review_required -> dedup_required
dedup_required -> promotion_required
promotion_required -> workspace_candidate_ready
```

`promotion_required -> workspace_candidate_ready` is allowed only after a future explicit promotion gate.

## D. Explicitly Blocked Transitions

Blocked direct transitions:

- `search_received` directly to production case
- `provider_result_metadata_received` directly to Evidence Layer write
- `package_reference_ready` directly to `analysis_run`
- `review_only_staging_candidate` directly to public event
- `review_only_staging_candidate` directly to report runtime
- `workspace_candidate_ready` directly to public response
- any state directly to publish / send / post / execute

No state in this contract authorizes live collection, raw evidence row parsing, public delivery, or production write behavior.

## E. Integration With 8T-3 / 8T-4 / 8T-5

Existing safe metadata-only helpers define the first compatible foundation:

- 8T-3 resolver validates package path and metadata boundaries.
- 8T-4 reader validates provider result metadata and package reference.
- 8T-5 smoke proves fixture-level metadata handoff summary.

Search-to-Case must use those helper boundaries before any future staging/import design.

## F. Safety Gates

Blocking conditions:

- `privacy_issue_stop`
- path escape
- missing package
- forbidden fields
- raw author identifier exposure
- private messages
- full evidence rows in metadata stage
- live collection without authorization
- unsupported platform
- generated response text
- public execution action

Forbidden field categories include cookies, tokens, sessions, passwords, API keys, browser profile paths, proxy credentials, raw author identifiers, profile URLs as actual exported values, private messages, raw comment dumps, full evidence rows, generated public response text, `target_user_list`, `persuasion_score`, `truth_score`, `official_verified`, `prediction_probability`, `psychological_profile`, and `personality_diagnosis`.

## G. Review-Only Staging Boundary

Review-only staging may contain:

- safe metadata summary
- package presence
- validation summary
- counts
- warnings / errors
- coverage note
- package reference
- provider result reference

Review-only staging must not perform:

- Evidence Layer writes
- production case creation
- `analysis_run` creation
- public output
- report runtime
- Sandbox/public event runtime
- generated response text
- publish / send / post / execute behavior

## H. Future Implementation Order

Recommended future order:

1. docs-only Search-to-Case contract
2. review-only staging import design
3. metadata-only staging helper
4. internal operator route/UI only after staging helper is safe
5. evidence preview gate
6. evidence import gate
7. case workspace gate
8. `analysis_run` gate
9. report / Sandbox / public event gates

Production import remains blocked until the relevant review, dedup, promotion, and safety gates exist and pass.
