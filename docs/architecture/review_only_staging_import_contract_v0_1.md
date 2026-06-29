# Review-only Staging Import Contract v0.1

Status: architecture contract only. This document does not implement backend code, frontend code, tests, routes, UI, staging helpers, Evidence import, production case creation, analysis runs, report runtime, Sandbox/public event runtime, collector execution, API bridges, or generated public response behavior.

## A. Definition

Review-only staging import means:

```text
metadata handoff -> internal review candidate
```

It is not an Evidence Layer write.

It is not a production case.

It is not an `analysis_run`.

It is not public output.

Review-only staging exists to preserve a safe metadata handoff for future human review before any evidence preview, evidence import, dedup, promotion, case workspace, analysis, report, Sandbox, or public event gate.

## B. Allowed Inputs

Allowed future staging inputs:

- `provider_result_id`
- `provider_job_id`
- `request_id`
- `package_name`
- `package_role`
- `case_id_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `coverage_note_summary`
- `validation_summary`
- `metadata_only_safe_summary`
- package file presence map
- safety markers
- blockers
- warnings
- audit references

These inputs are metadata-only. Counts, validation summaries, and package presence are not evidence truth, official confirmation, or causal proof.

## C. Forbidden Inputs

Forbidden in review-only staging:

- full evidence rows
- raw comment dumps
- raw author ids
- raw author names
- profile URLs as actual exported values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profile paths
- absolute private package paths exposed to UI/API
- generated public response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

If any forbidden input appears as an actual exported value, the staging design must block with a privacy or metadata-contract status.

## D. Contract Objects

### 1. `review_only_staging_import_request_v0_1`

Future fields:

- `staging_request_id`
- `analysis_request_id`
- `provider_result_id`
- `package_name`
- `package_locator_strategy`
- `requested_by`
- `requested_at`
- `safety_mode`
- `import_mode = review_only_metadata`
- `allow_evidence_row_preview = false`
- `allow_production_import = false`

Purpose: record an operator or system request to create a review-only metadata staging candidate. It does not read evidence rows or create production records.

### 2. `review_only_staging_candidate_v0_1`

Future fields:

- `staging_candidate_id`
- `analysis_request_id`
- `provider_result_id`
- `package_name`
- `case_id_hint`
- `case_title_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- `metadata_summary`
- `validation_summary`
- `coverage_summary`
- `review_status`
- `promotion_status`
- `blockers`
- `warnings`
- `allowed_actions`
- `blocked_actions`
- `safety_flags`
- `audit_refs`
- `created_at`

Purpose: preserve a safe metadata-only candidate for human review. It is not production evidence and not a production case.

### 3. `review_only_staging_gate_result_v0_1`

Future fields:

- `gate_result_id`
- `staging_candidate_id`
- `package_resolution_status`
- `provider_result_status`
- `privacy_status`
- `path_status`
- `metadata_contract_status`
- `evidence_row_boundary_status`
- `staging_status`
- `blockers`
- `warnings`
- `created_at`

Purpose: record gate status before a staging candidate can be considered ready for human review.

### 4. `review_only_staging_audit_record_v0_1`

Future fields:

- `audit_id`
- `staging_candidate_id`
- `action`
- `actor_type`
- `action_time`
- `input_refs`
- `output_refs`
- `safety_flags`
- `notes`

Purpose: append audit-visible records for review-only staging decisions. Audit records must not expose raw evidence rows, raw identities, secrets, or absolute private paths.

## E. Status Values

Future status values:

- `staging_request_drafted`
- `staging_metadata_validating`
- `staging_candidate_created`
- `ready_for_human_review`
- `manual_review_required`
- `metadata_validation_warn`
- `blocked_missing_package`
- `blocked_path_escape`
- `blocked_privacy_issue`
- `blocked_metadata_contract`
- `blocked_evidence_rows_in_metadata_stage`
- `blocked_live_collection_not_authorized`
- `blocked_unsupported_platform`
- `promotion_required`
- `production_import_blocked`

## F. Allowed Transitions

Allowed transitions:

```text
provider_result_metadata_received -> package_reference_ready
package_reference_ready -> metadata_validation_passed
metadata_validation_passed -> staging_request_drafted
staging_request_drafted -> staging_metadata_validating
staging_metadata_validating -> staging_candidate_created
staging_candidate_created -> ready_for_human_review
ready_for_human_review -> future evidence review gate
```

The final transition to a future evidence review gate requires explicit future implementation. This document does not implement that gate.

## G. Blocked Transitions

Blocked transitions:

- `staging_candidate_created -> Evidence Layer write`
- `staging_candidate_created -> production case`
- `staging_candidate_created -> analysis_run`
- `staging_candidate_created -> B-end report runtime`
- `staging_candidate_created -> Sandbox/public event runtime`
- `staging_candidate_created -> public response`
- `staging_candidate_created -> publish/send/post/execute`
- `ready_for_human_review -> production import` without future explicit gate
- `metadata_validation_warn -> staging_candidate_created` without manual review

Review-only staging must never be used as a shortcut around evidence preview, human review, dedup, promotion, or case workspace gates.

## H. Review-only Visibility

Future review-only staging may show:

- `package_name`
- `case_id_hint`
- safe title hint
- `validation_status`
- evidence/source counts
- warnings/errors
- coverage summary
- safety markers
- blocker summary
- audit trail

It must not show:

- raw comments
- raw author ids/names
- private URLs/profile URLs as actual exported values
- absolute local paths
- credentials/secrets
- public response text
- target lists

## I. Relationship to Search-to-Case

Search-to-Case must pass through review-only staging before any future workspace candidate or Evidence import gate.

Search does not directly create a production case.

Search does not directly write Evidence Layer.

Search does not directly create an `analysis_run`, report, Sandbox, public event, or public response.

Review-only staging is the future checkpoint where safe metadata handoff can become human-reviewable without becoming production data.
