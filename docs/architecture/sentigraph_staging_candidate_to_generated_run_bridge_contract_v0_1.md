# Sentigraph Staging Candidate to Generated-run Bridge Contract v0.1

## A. Contract Purpose

This document defines the future bridge contract between:

- a safe review-only staging candidate produced from provider package metadata
- a future minimum real-run / generated-run input candidate

The bridge is governance and contract structure only. It is not a runtime implementation. It is not an API. It is not frontend integration. It is not Evidence Layer import. It is not production analysis.

Core principle:

Provider output is evidence, not truth. A review-only staging candidate is metadata for human review, not an analysis-ready dataset.

## B. Proposed Schema

Proposed schema name:

```json
{
  "bridge_schema": "sentigraph_staging_candidate_generated_run_bridge_v0_1"
}
```

Proposed top-level object:

```json
{
  "bridge_id": "staging_generated_run_bridge_...",
  "bridge_schema": "sentigraph_staging_candidate_generated_run_bridge_v0_1",
  "bridge_status": "candidate_ready_for_future_minimum_real_run",
  "created_at": "2026-07-01T00:00:00Z",
  "created_by": "sentigraph_internal_operator",
  "staging_candidate_id": "review_staging_candidate_...",
  "provider_result_id": "provider_result_...",
  "provider_job_id": "provider_job_...",
  "request_id": "analysis_request_...",
  "case_id_hint": "case_...",
  "package_name": "controlled_package_name",
  "input_source_kind": "review_only_staging_candidate",
  "input_scope_note": "selected sample / controlled package metadata only",
  "metadata_only": true,
  "evidence_rows_parsed": false,
  "evidence_layer_write": false,
  "production_case_created": false,
  "production_analysis_run_created": false,
  "human_review_required": true,
  "generated_run_requested": false,
  "minimum_real_run_input_candidate": {},
  "boundary_flags": {},
  "runtime_side_effects": {},
  "warnings": [],
  "blockers": [],
  "audit_refs": [],
  "downstream_allowed_actions": [],
  "downstream_blocked_actions": []
}
```

## C. Input Contract

Input source:

`review_only_staging_candidate`

Allowed safe input fields:

- `staging_candidate_id`
- `analysis_request_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
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
- `package_reference.package_name`
- `package_reference.package_role`
- `package_reference.package_index_ref`
- `package_reference.package_locator_strategy`
- `package_summary.required_files_presence`
- `package_summary.missing_required_files`
- `package_summary.forbidden_fields`
- `blockers`
- `warnings`
- `audit_refs`
- `gate_result.package_resolution_status`
- `gate_result.provider_result_status`
- `gate_result.privacy_status`
- `gate_result.path_status`
- `gate_result.metadata_contract_status`
- `gate_result.evidence_row_boundary_status`
- `metadata_only`
- `path_exposed=false`

Input must already be safe metadata. The bridge must not open package files, read original rows, follow URLs, or inspect private collector internals.

## D. Output Contract

Required bridge identity fields:

- `bridge_id`
- `bridge_schema`
- `bridge_status`
- `created_at`
- `created_by`

Required upstream references:

- `staging_candidate_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `case_id_hint`
- `package_name`

Required boundary fields:

- `input_source_kind`
- `input_scope_note`
- `metadata_only`
- `evidence_rows_parsed`
- `evidence_layer_write`
- `production_case_created`
- `production_analysis_run_created`
- `human_review_required`
- `generated_run_requested`
- `boundary_flags`
- `runtime_side_effects`

Required downstream fields:

- `minimum_real_run_input_candidate`
- `downstream_allowed_actions`
- `downstream_blocked_actions`
- `warnings`
- `blockers`
- `audit_refs`

Recommended bridge statuses:

- `candidate_ready_for_future_minimum_real_run`
- `manual_review_required`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_path_escape`
- `blocked_missing_validation`
- `blocked_count_inconsistency`
- `blocked_requested_side_effect`

## E. Boundary Flags

All boundary flags should be explicit:

```json
{
  "selected_sample_only": true,
  "controlled_package_only": true,
  "metadata_only": true,
  "not_full_web": true,
  "not_full_platform": true,
  "not_full_thread": true,
  "not_official_verification": true,
  "not_causal_proof": true,
  "not_prediction": true,
  "not_production_score": true,
  "provider_output_is_evidence_not_truth": true,
  "human_review_required": true,
  "no_auto_execute": true,
  "no_generated_public_response": true
}
```

These flags are not decorative. Future tests should fail if required flags are missing or false.

## F. Runtime Side-effect Flags

All runtime side-effect flags must be false:

```json
{
  "called_real_api": false,
  "called_real_llm": false,
  "ran_collector": false,
  "accessed_private_collector": false,
  "read_real_exchange_dir": false,
  "fetched_url": false,
  "scraped_page": false,
  "parsed_evidence_items_file": false,
  "read_original_package_rows": false,
  "wrote_evidence_layer": false,
  "created_production_case": false,
  "created_analysis_run": false,
  "generated_b_end_report_runtime": false,
  "generated_sandbox_runtime": false,
  "generated_public_event_runtime": false,
  "generated_response_text": false,
  "published_or_sent": false,
  "auto_executed": false
}
```

If any side-effect flag is true, the bridge status must be blocked.

## G. Safety Blockers

Hard blocker categories:

- `missing_package_name`
- `package_resolution_not_accepted`
- `blocked_privacy_issue`
- `forbidden_metadata_field_present`
- `blocked_path_escape`
- `missing_validation_report`
- `missing_required_metadata_file`
- `evidence_source_count_inconsistent`
- `unknown_future_platform_manual_review_required`
- `requested_row_parsing`
- `requested_evidence_layer_write`
- `requested_production_case`
- `requested_production_analysis_run`
- `requested_public_output`
- `requested_generated_response_text`
- `requested_auto_execute`
- `requested_publish_send_post`
- `requested_collector_run`
- `requested_real_api_or_llm`

The bridge may carry warnings, but warnings do not make the object analysis-ready.

## H. Audit Fields

Each future bridge object should carry audit references, not hidden provenance:

- `audit_refs`
- `source_staging_audit_refs`
- `bridge_created_by`
- `bridge_created_at`
- `bridge_reason`
- `input_summary_hash` if later needed
- `boundary_confirmation_snapshot`
- `blocked_action_snapshot`

Audit must not include raw author identifiers, private paths, secrets, browser profile paths, row contents, or generated public text.

## I. Downstream Policy

Allowed downstream actions in 8V-4-style smoke:

- create bridge candidate object
- validate bridge object
- create minimum real-run input candidate metadata
- request future minimum real-run execution decision

Blocked downstream actions:

- parse row files
- write Evidence Layer
- create production case
- create production `analysis_run`
- call generated-run automatically without a separate future decision
- attach dense graph directly
- create frontend/API route
- create B-end report
- create Sandbox/public event
- generate public response text
- publish/send/post/execute

Dense graph policy:

- Dense graph is downstream of a safe generated-run object.
- This bridge does not call dense graph.
- This bridge does not approve dense graph frontend or public route integration.

Report policy:

- Reports require separate analysis/result/report gates.
- This bridge does not create Summary Report Candidate, Final Summary Report, export artifact, or public access delivery.

## J. Future Tests

Future 8V-4 tests should verify:

- bridge object has schema `sentigraph_staging_candidate_generated_run_bridge_v0_1`
- bridge input accepts safe review-only staging summary
- bridge rejects missing `package_name`
- bridge rejects non-accepted package resolution status
- bridge rejects privacy issue status
- bridge rejects forbidden metadata fields
- bridge rejects path escape
- bridge rejects missing validation report
- bridge rejects count inconsistency
- bridge preserves unknown/future platform as manual review required
- bridge does not parse `evidence_items.jsonl` or `evidence_items.csv`
- bridge does not open package row files
- bridge does not expose absolute paths
- bridge side-effect flags are all false
- bridge boundary flags are present and true
- bridge output has no raw identity fields
- bridge output has no response text or generated public message
- bridge output has no target-user, persuasion, truth, official verification, prediction, psychology, or personality fields
- bridge does not create runtime files
- bridge does not add API route
- bridge does not touch frontend

Suggested test file:

`backend/app/tests/test_staging_candidate_to_generated_run_bridge.py`

This is a future recommendation only. 8V-3 does not create tests.

## K. Forbidden Interpretations

Do not interpret this bridge contract as:

- Evidence Layer import
- production case creation
- production `analysis_run` creation
- analysis-ready promotion
- official verification
- truth scoring
- full-web coverage
- full-platform coverage
- causal proof
- prediction
- public opinion control
- generated response authorization
- dense graph frontend approval
- report runtime approval
- public route approval
- collector integration
- real API or real LLM integration

The bridge is a safe metadata handoff candidate only.

