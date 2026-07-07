# Sentigraph 8Z-8A No-real-row Route C Row-preview Entry Compatibility Design Decision v0.1

## Decision

- phase: 8Z-8A
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- compatibility_design_only: yes
- no_real_row_design_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- helper_called: no
- adapter_implemented: no
- row_preview_executed: no
- controlled_row_preview_helper_called: no
- row_preview_entry_created: no
- redacted_review_only_row_preview_created: no
- row_source_file_opened: no
- evidence_items_jsonl_parsed: no
- evidence_items_csv_parsed: no
- source_manifest_rows_parsed: no
- collection_log_rows_parsed: no
- package_resolver_called: no
- provider_result_reader_called: no
- local_exchange_reader_called: no
- review_only_staging_helper_called: no
- real_exchange_dir_read: no
- real_package_dir_read: no
- evidence_layer_write: no
- production_evidence_item_created: no
- production_case_created: no
- production_analysis_run_created: no
- actual_analysis_execution_started: no
- production_analysis_result_creation_authorized: no
- production_analysis_result_created: no
- 8w69_pause_preserved: yes
- 8w70_reactivation_selected: no
- source11_runtime_called: no
- actual_final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- export_download_public_delivery_created: no
- source_files_created: no
- docs_project_sources_created: no
- selected_compatibility_option: option_A_no_real_row_route_c_row_preview_entry_adapter
- selected_next_boundary_option: ready_for_8Z_8B_controlled_no_real_row_route_c_row_preview_entry_adapter_smoke
- future_8z8b_exact_approval_phrase_required: yes
- future_8z8b_exact_approval_phrase_active: no
- future_8z8b_exact_approval_phrase: APPROVE_8Z_8B_CONTROLLED_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_ADAPTER_SMOKE
- future_8z9_phrase_status: inactive_not_ready_pending_no_real_row_adapter_smoke_and_re_gate
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Purpose

8Z-8A is a docs-only compatibility design. It resolves, on paper only, how 8Z can safely bridge:

`8Z-7 local controlled review-only staging candidate -> no-real-row Route C row-preview entry candidate / adapter candidate`

without executing row preview, opening approved row files, parsing real rows, calling package resolver, calling provider reader, calling local exchange reader, calling helper code, writing Evidence Layer, or creating production objects.

8Z-8A does not implement the adapter and does not create 8Z-9 row-preview smoke.

## 8Z State Summary

- 8Z-1 created the on-demand collector workflow contract as docs-only.
- 8Z-2 created the request/result metadata contract as docs-only.
- 8Z-3 completed controlled request metadata fixture smoke.
- 8Z-4 completed controlled provider_result metadata fixture smoke.
- 8Z-5 completed controlled request/result correlation smoke.
- 8Z-6 created the review-only staging handoff gate docs-only.
- 8Z-7 completed controlled correlation to review-only staging handoff smoke.
- 8Z-8 created the Route C row-preview gate decision and selected a blocked/pause boundary.
- 8Z-8A is compatibility design docs-only.
- 8Y Route C remains stage-complete and paused.
- 8W-69 pause remains preserved.
- 8W-70 reactivation remains not selected.

## Restated 8Z-8 Blocker

8Z-7 output is a local controlled review-only staging candidate. It is metadata-only, created in a controlled backend test path, and preserves `human_review_required = true` plus `no_automatic_trust_upgrade = true`.

8Z-8 wanted to consider Route C row-preview re-entry, but found this blocker:

- existing `controlled_row_preview` is safe only in its existing approved context
- it is not confirmed as a direct adapter from the 8Z-7 candidate shape
- it opens/parses a fixed approved row source when successful
- 8Z re-entry requires no real row read
- 8Z re-entry requires no real package directory read
- 8Z re-entry requires no production row parsing

Therefore 8Z-9 remains blocked and must not be run directly after 8Z-8A.

## Compatibility Options

### Option A: no_real_row_route_c_row_preview_entry_adapter

This option creates a future metadata-only entry candidate.

It does not create actual row preview output.
It does not create redacted preview rows.
It does not synthesize fake evidence rows.
It outputs only safe entry metadata, blockers, boundary flags, and manual-review state.
It keeps future downstream row-preview separately gated.

This option avoids claiming that preview rows exist.

### Option B: synthetic_placeholder_row_preview_fixture

This option would create a synthetic placeholder preview object from safe metadata only.

It would need very clear non-evidence labels and must not be consumed as an Evidence candidate. This carries higher overclaim risk because the output can look like preview rows even if it contains no real evidence rows.

8Z-8A does not select Option B.

### Option C: continue_pause

This option keeps the 8Z chain paused before Route C row-preview re-entry.

It is safest if no no-real-row adapter shape can be defined. However, it does not advance the handoff design from 8Z-7 candidate to a future Route C entry gate.

## Selected Compatibility Option

Selected:

`option_A_no_real_row_route_c_row_preview_entry_adapter`

Rationale:

- It resolves the 8Z-8 blocker on paper without executing row preview.
- It avoids opening fixed approved row files.
- It avoids real package row parsing.
- It avoids fake evidence rows.
- It defines a metadata-only entry candidate rather than a preview.
- It keeps actual Route C row-preview and downstream Evidence candidate gates separate.

## Future Adapter Object

Suggested future schema:

`sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1`

Suggested object type:

`route_c_row_preview_entry_candidate`

Required semantics:

- entry candidate only
- metadata-only
- no actual preview run
- no redacted row preview created
- no preview rows created
- no evidence rows created
- no fake evidence rows
- no row source path
- no package resolver call
- no provider reader call
- no local exchange reader call
- no file reads
- no Evidence Layer write
- no production object creation
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Allowed Future 8Z-8B Input

Future 8Z-8B may accept only an 8Z-7 local controlled review-only staging candidate or equivalent safe fixture with:

- `review_only_staging_candidate_schema = sentigraph_on_demand_collector_review_only_staging_candidate_v0_1` or existing safe equivalent
- `review_only_staging_mode = backend_only_local_review_only_staging_handoff_candidate` or existing safe equivalent
- `source_request_result_correlation_schema = sentigraph_on_demand_collector_request_result_correlation_v0_1` or existing safe equivalent
- `package_reference_policy = opaque_safe_identifier_only`
- `metadata_only = true`
- `row_content_included = false`
- `raw_identity_included = false`
- `secrets_included = false`
- `package_resolver_called = false`
- `provider_result_reader_called = false`
- `local_exchange_reader_called = false`
- `persistent_staging_storage_created = false`
- `actual_review_queue_runtime_used = false`
- `production_review_queue_item_created = false`
- `collector_job_run = false`
- `provider_job_run = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- all production object flags false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Allowed Future 8Z-8B Action

If separately approved, future 8Z-8B may be:

- backend-only
- test-first
- controlled smoke only
- local-only
- metadata-only
- adapter-candidate-only
- using in-memory safe fixture material only
- creating only a local no-real-row Route C row-preview entry adapter candidate inside a backend test path

Future 8Z-8B must not:

- call `controlled_row_preview`
- execute row preview
- use the 8W-7 helper phrase
- create redacted row-preview output
- create preview rows
- create evidence rows
- create synthetic fake evidence rows
- open row source files
- read files
- call package resolver / provider reader / local exchange reader
- write Evidence Layer
- create production objects
- create Review Queue runtime
- change route/API/frontend/runtime behavior

## Future 8Z-8B Approval Phrase

Future 8Z-8B exact approval phrase:

`APPROVE_8Z_8B_CONTROLLED_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_ADAPTER_SMOKE`

This phrase is inactive in 8Z-8A.

It does not authorize implementation in 8Z-8A.
It does not authorize row-preview execution.
It does not authorize `controlled_row_preview` helper calls.
It does not authorize use of the 8W-7 helper phrase.
It does not authorize row parsing.
It does not authorize package resolver, provider reader, or local exchange reader behavior.
It does not authorize Evidence Layer write or production objects.

## 8Z-9 Phrase Status

8Z-9 phrase:

`APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE`

Status:

`inactive_not_ready_pending_no_real_row_adapter_smoke_and_re_gate`

8Z-9 must not be run directly after 8Z-8A. If 8Z-8B later succeeds, a separate docs-only re-gate must decide whether 8Z-9 may be reconsidered.

The repaired 8W-7 helper phrase remains only an inner helper phrase for actual controlled row-preview contexts and does not authorize 8Z-8B or 8Z-9.

## Future 8Z-8B Output Constraints

Future 8Z-8B output must preserve:

- `no_real_row_route_c_row_preview_entry_adapter_created = true` only inside controlled backend test path
- `adapter_schema = sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1` or safe equivalent
- `adapter_mode = backend_only_local_no_real_row_route_c_row_preview_entry_adapter`
- `route_c_row_preview_entry_candidate_created = true` only as metadata-only entry candidate
- `row_preview_executed = false`
- `controlled_row_preview_helper_called = false`
- `redacted_review_only_row_preview_created = false`
- `row_preview_rows_created = false`
- `synthetic_evidence_rows_created = false`
- `row_source_path_present = false`
- `row_source_file_opened = false`
- `evidence_items_jsonl_parsed = false`
- `evidence_items_csv_parsed = false`
- `source_manifest_rows_parsed = false`
- `collection_log_rows_parsed = false`
- `package_resolver_called = false`
- `provider_result_reader_called = false`
- `local_exchange_reader_called = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `evidence_layer_write = false`
- production EvidenceItem / case / analysis_run / Analysis Result flags false
- Review Queue runtime flags false
- Source 11 / FinalSummaryReport / B-end / Sandbox / export / delivery runtime flags false
- `route_ready = false`
- `frontend_ready = false`
- `production_ready = false`
- `customer_ready = false`
- `public_ready = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Hard Blockers For Future 8Z-8B

Block future 8Z-8B if:

- adapter requires file reads
- adapter requires `controlled_row_preview` helper call
- adapter requires 8W-7 helper phrase
- adapter creates actual row preview
- adapter creates redacted row-preview output
- adapter creates synthetic fake evidence rows
- adapter requires package resolver / provider reader / local exchange reader call
- adapter reads real exchange/package directories
- adapter parses evidence_items / source_manifest / collection_log rows
- adapter exposes raw rows/comments/identities/profile URLs
- adapter writes Evidence Layer
- adapter creates production EvidenceItem/case/analysis_run/Analysis Result
- adapter creates persistent staging storage
- adapter creates Review Queue runtime or production Review Queue item
- adapter requires route/API/frontend
- adapter requires collector/provider job, scheduler, HTTP bridge, or webhook
- adapter requires secrets/cookies/sessions/browser profiles
- adapter makes customer/public/production/final/export readiness claims

## Relationship To Route C

8Z-8A does not reopen Route C.

Future 8Z-8B, if separately approved, can only create a no-real-row entry adapter candidate.

Future 8Z-9, if ever reconsidered, requires a separate docs-only re-gate after 8Z-8B.

Downstream Route C Evidence candidate, Review Queue candidate, Evidence Layer, production case, analysis_run, actual analysis execution, and Analysis Result gates remain separate.

8Y-21 Route C stage-complete / pause remains preserved.

## Relationship To 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

The no-real-row adapter cannot satisfy the 8W-68 / 8W-69 authorization protocol.

## Relationship To Source 11 / Project Source

Source 11 update is not required because 8Z-8A changes no runtime behavior.

8Z-8A must not create Project Source files or `docs/project_sources`.

Future Source update may be considered only after a larger 8Z checkpoint.

## Recommended Next Task

Recommended next task:

Phase 8Z-8B Controlled No-real-row Route C Row-preview Entry Adapter Smoke.

That future task must use its own exact approval phrase and remain adapter-candidate-only, no-real-row, metadata-only, local-only, and backend-test-path-only.
