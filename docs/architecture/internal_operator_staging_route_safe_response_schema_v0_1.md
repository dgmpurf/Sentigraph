# Internal Operator Staging Route Safe Response Schema v0.1

## A. Schema Object

Schema name:

```text
internal_operator_review_only_staging_response_v0_1
```

Purpose: define the safe response envelope for a future internal operator read-only staging route.

This schema is design only. It does not implement a route, service, UI, persistent storage, Evidence Layer write, production case, `analysis_run`, report runtime, Sandbox/public event runtime, collector integration, or public delivery.

## B. Required Fields

The future response object must include:

- `schema`
- `staging_candidate_id`
- `route_scope`
- `access_scope`
- `metadata_only`
- `review_only`
- `production_import_allowed = false`
- `evidence_layer_write_allowed = false`
- `production_case_creation_allowed = false`
- `analysis_run_allowed = false`
- `public_output_allowed = false`
- `staging_candidate`
- `gate_summary`
- `allowed_actions`
- `blocked_actions`
- `safety_flags`
- `warnings`
- `blockers`
- `audit_refs`

Required fixed values:

```json
{
  "schema": "internal_operator_review_only_staging_response_v0_1",
  "route_scope": "internal_operator",
  "access_scope": "local_or_disabled_by_default",
  "metadata_only": true,
  "review_only": true,
  "production_import_allowed": false,
  "evidence_layer_write_allowed": false,
  "production_case_creation_allowed": false,
  "analysis_run_allowed": false,
  "public_output_allowed": false
}
```

## C. Safe `staging_candidate` Schema

The `staging_candidate` object may include:

```json
{
  "staging_candidate_id": "review_staging_candidate_example",
  "analysis_request_id": "analysis_request_fixture",
  "provider_result_id": "provider_result_fixture",
  "package_name": "helldivers_package",
  "case_id_hint": "analysis_request_fixture",
  "case_title_hint": "Example selected public sample",
  "validation_status": "passed",
  "evidence_count": 34,
  "source_count": 7,
  "warning_count": 0,
  "error_count": 0,
  "metadata_summary": {
    "evidence_count": 34,
    "source_count": 7,
    "package_name": "helldivers_package"
  },
  "validation_summary": {
    "status": "passed",
    "warnings": 0,
    "errors": 0
  },
  "coverage_summary": {
    "coverage_note_present": true,
    "not_full_web": true,
    "not_full_platform": true
  },
  "review_status": "ready_for_human_review",
  "promotion_status": "promotion_required",
  "created_at": "2026-06-29T00:00:00Z"
}
```

The object must not include raw evidence rows, raw comments, raw identifiers, profile URL values, secrets, absolute private paths, generated response text, production action payloads, or public delivery payloads.

## D. Safe `gate_summary` Schema

The `gate_summary` object may include:

```json
{
  "package_resolution_status": "accepted_metadata_only",
  "provider_result_status": "accepted_metadata_only",
  "privacy_status": "clear",
  "path_status": "accepted_metadata_only",
  "metadata_contract_status": "metadata_contract_ok",
  "evidence_row_boundary_status": "evidence_rows_not_read",
  "staging_status": "ready_for_human_review"
}
```

Allowed safe status values include:

- `ready_for_human_review`
- `metadata_validation_warn`
- `manual_review_required`
- `blocked_missing_package`
- `blocked_path_escape`
- `blocked_privacy_issue`
- `blocked_metadata_contract`
- `blocked_evidence_rows_in_metadata_stage`
- `production_import_blocked`
- `live_collection_not_authorized`
- `route_disabled`
- `operator_auth_required`

## E. Required Boundary Flags

The future response must include these boundary flags:

```json
{
  "metadata_only": true,
  "review_only": true,
  "full_evidence_rows_included": false,
  "raw_identifiers_included": false,
  "absolute_paths_included": false,
  "production_actions_included": false,
  "public_actions_included": false
}
```

Recommended `safety_flags`:

```json
{
  "metadata_only": true,
  "review_only": true,
  "collector_run": false,
  "live_crawl": false,
  "real_api_called": false,
  "real_llm_called": false,
  "url_fetching": false,
  "scraping": false,
  "full_evidence_rows_parsed": false,
  "evidence_items_jsonl_parsed": false,
  "evidence_items_csv_parsed": false,
  "raw_comments_printed": false,
  "raw_author_identifiers_printed": false,
  "secrets_read": false,
  "evidence_layer_written": false,
  "production_case_created": false,
  "analysis_run_created": false,
  "b_end_report_runtime_generated": false,
  "sandbox_public_event_runtime_generated": false,
  "persistent_staging_storage_created": false
}
```

## F. Error Response Schema

Safe error response:

```json
{
  "schema": "internal_operator_review_only_staging_error_v0_1",
  "route_scope": "internal_operator",
  "access_scope": "local_or_disabled_by_default",
  "metadata_only": true,
  "review_only": true,
  "error_code": "route_disabled",
  "message": "Review-only staging route is disabled.",
  "blockers": ["route_disabled"],
  "warnings": [],
  "path_exposed": false,
  "raw_metadata_exposed": false
}
```

Allowed safe error codes:

- `not_found`
- `manual_review_required`
- `blocked_privacy_issue`
- `blocked_metadata_contract`
- `blocked_path_escape`
- `route_disabled`
- `operator_auth_required`

Error responses must not leak absolute paths, raw metadata, raw evidence rows, raw comments, raw identifiers, secrets, profile URLs, generated response text, or production action payloads.

## G. Examples

### Safe Ready Example

```json
{
  "schema": "internal_operator_review_only_staging_response_v0_1",
  "staging_candidate_id": "review_staging_candidate_example",
  "route_scope": "internal_operator",
  "access_scope": "local_or_disabled_by_default",
  "metadata_only": true,
  "review_only": true,
  "production_import_allowed": false,
  "evidence_layer_write_allowed": false,
  "production_case_creation_allowed": false,
  "analysis_run_allowed": false,
  "public_output_allowed": false,
  "staging_candidate": {
    "staging_candidate_id": "review_staging_candidate_example",
    "analysis_request_id": "analysis_request_fixture",
    "provider_result_id": "provider_result_fixture",
    "package_name": "helldivers_package",
    "case_id_hint": "analysis_request_fixture",
    "case_title_hint": "Selected public sample",
    "validation_status": "passed",
    "evidence_count": 34,
    "source_count": 7,
    "warning_count": 0,
    "error_count": 0,
    "metadata_summary": {
      "evidence_count": 34,
      "source_count": 7,
      "package_name": "helldivers_package"
    },
    "validation_summary": {
      "status": "passed",
      "warnings": 0,
      "errors": 0
    },
    "coverage_summary": {
      "coverage_note_present": true,
      "not_full_web": true,
      "not_full_platform": true
    },
    "review_status": "ready_for_human_review",
    "promotion_status": "promotion_required",
    "created_at": "2026-06-29T00:00:00Z"
  },
  "gate_summary": {
    "package_resolution_status": "accepted_metadata_only",
    "provider_result_status": "accepted_metadata_only",
    "privacy_status": "clear",
    "path_status": "accepted_metadata_only",
    "metadata_contract_status": "metadata_contract_ok",
    "evidence_row_boundary_status": "evidence_rows_not_read",
    "staging_status": "ready_for_human_review"
  },
  "allowed_actions": [
    "continue_review",
    "request_more_metadata",
    "mark_manual_review_required",
    "reject_package",
    "block_privacy_issue",
    "request_future_evidence_preview_gate",
    "request_future_dedup_gate",
    "request_future_promotion_gate"
  ],
  "blocked_actions": [
    "approve_production_evidence",
    "create_production_case",
    "start_analysis_run",
    "generate_report",
    "generate_public_event",
    "generate_public_response",
    "publish",
    "send",
    "post",
    "execute",
    "target_individuals"
  ],
  "safety_flags": {
    "metadata_only": true,
    "review_only": true,
    "full_evidence_rows_included": false,
    "raw_identifiers_included": false,
    "absolute_paths_included": false,
    "production_actions_included": false,
    "public_actions_included": false
  },
  "warnings": [],
  "blockers": [],
  "audit_refs": [
    {
      "audit_ref_id": "review_staging_audit_ref_example",
      "actor_type": "internal_operator",
      "action": "create_review_only_staging_candidate",
      "scope": "metadata_only"
    }
  ]
}
```

### Blocked Privacy Issue Example

```json
{
  "schema": "internal_operator_review_only_staging_response_v0_1",
  "staging_candidate_id": "review_staging_candidate_blocked",
  "route_scope": "internal_operator",
  "access_scope": "local_or_disabled_by_default",
  "metadata_only": true,
  "review_only": true,
  "production_import_allowed": false,
  "evidence_layer_write_allowed": false,
  "production_case_creation_allowed": false,
  "analysis_run_allowed": false,
  "public_output_allowed": false,
  "staging_candidate": {
    "staging_candidate_id": "review_staging_candidate_blocked",
    "analysis_request_id": "analysis_request_fixture",
    "provider_result_id": "provider_result_fixture",
    "package_name": "blocked_package",
    "case_id_hint": "analysis_request_fixture",
    "case_title_hint": null,
    "validation_status": "blocked",
    "evidence_count": null,
    "source_count": null,
    "warning_count": null,
    "error_count": null,
    "metadata_summary": {},
    "validation_summary": {},
    "coverage_summary": {
      "not_full_web": true,
      "not_full_platform": true
    },
    "review_status": "manual_review_required",
    "promotion_status": "promotion_required",
    "created_at": "2026-06-29T00:00:00Z"
  },
  "gate_summary": {
    "package_resolution_status": "blocked_privacy_issue",
    "provider_result_status": "blocked_privacy_issue",
    "privacy_status": "blocked_privacy_issue",
    "path_status": "blocked_privacy_issue",
    "metadata_contract_status": "metadata_contract_ok",
    "evidence_row_boundary_status": "evidence_rows_not_read",
    "staging_status": "blocked_privacy_issue"
  },
  "allowed_actions": [
    "request_more_metadata",
    "block_privacy_issue",
    "reject_package"
  ],
  "blocked_actions": [
    "approve_production_evidence",
    "create_production_case",
    "start_analysis_run",
    "generate_report",
    "generate_public_event",
    "generate_public_response",
    "publish",
    "send",
    "post",
    "execute",
    "target_individuals"
  ],
  "safety_flags": {
    "metadata_only": true,
    "review_only": true,
    "full_evidence_rows_included": false,
    "raw_identifiers_included": false,
    "absolute_paths_included": false,
    "production_actions_included": false,
    "public_actions_included": false
  },
  "warnings": [],
  "blockers": ["blocked_privacy_issue"],
  "audit_refs": []
}
```

### Route Disabled Example

```json
{
  "schema": "internal_operator_review_only_staging_error_v0_1",
  "route_scope": "internal_operator",
  "access_scope": "local_or_disabled_by_default",
  "metadata_only": true,
  "review_only": true,
  "error_code": "route_disabled",
  "message": "Review-only staging route is disabled.",
  "blockers": ["route_disabled"],
  "warnings": [],
  "path_exposed": false,
  "raw_metadata_exposed": false
}
```
