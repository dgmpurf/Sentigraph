# Sentigraph No-real-row Route C Row-preview Entry Compatibility Contract v0.1

## Purpose

This contract defines a docs-only compatibility design for a future no-real-row Route C row-preview entry adapter candidate.

It bridges, on paper only:

`8Z-7 local controlled review-only staging candidate -> no-real-row Route C row-preview entry candidate`

The contract does not implement an adapter, execute row preview, call `controlled_row_preview`, call package resolver, call provider reader, call local exchange reader, call review-only staging helper, read files, parse rows, write Evidence Layer, create production objects, change routes, change frontend code, change runtime behavior, or create Project Source files.

## Status Fields

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

## Compatibility Problem

8Z-7 created a safe local review-only staging candidate from correlated on-demand collector metadata. 8Z-8 audited Route C row-preview surfaces and found:

- `controlled_row_preview` exists
- the 8W-7 helper phrase is repaired and ASCII
- row-preview helper tests reject old garbled and wrong phrases before row-source access
- existing Route C redacted row-preview smoke exists
- but the helper is not a confirmed direct adapter from the 8Z-7 candidate shape
- successful helper execution opens/parses its fixed approved row source

8Z re-entry requires a no-real-row path. The future adapter candidate must therefore sit before any actual row-preview execution.

## Selected Design Option

Selected:

`option_A_no_real_row_route_c_row_preview_entry_adapter`

This option creates only an entry candidate.

It does not create actual row-preview output.
It does not create redacted row-preview output.
It does not synthesize evidence rows.
It does not create fake preview rows.
It does not call `controlled_row_preview`.
It does not use the 8W-7 helper phrase.
It does not open row source files.

The output is governance metadata for deciding whether a later true row-preview gate may be considered.

## Future Adapter Candidate Schema

Suggested schema:

`sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1`

Suggested object type:

`route_c_row_preview_entry_candidate`

Suggested future object shape:

```json
{
  "schema": "sentigraph_on_demand_collector_no_real_row_route_c_row_preview_entry_adapter_v0_1",
  "phase": "8Z-8B",
  "adapter_mode": "backend_only_local_no_real_row_route_c_row_preview_entry_adapter",
  "source_review_only_staging_candidate_schema": "sentigraph_on_demand_collector_review_only_staging_candidate_v0_1",
  "source_review_only_staging_mode": "backend_only_local_review_only_staging_handoff_candidate",
  "source_request_result_correlation_schema": "sentigraph_on_demand_collector_request_result_correlation_v0_1",
  "package_reference_policy": "opaque_safe_identifier_only",
  "metadata_only": true,
  "route_c_row_preview_entry_candidate_created": true,
  "row_preview_executed": false,
  "controlled_row_preview_helper_called": false,
  "redacted_review_only_row_preview_created": false,
  "row_preview_rows_created": false,
  "synthetic_evidence_rows_created": false,
  "row_source_path_present": false,
  "row_source_file_opened": false,
  "human_review_required": true,
  "no_automatic_trust_upgrade": true,
  "boundary_flags": {},
  "blockers": [],
  "warnings": [],
  "next_gate": "separate_docs_only_re_gate_required_before_8z9"
}
```

The future object must not include row bodies, row snippets, row source paths, absolute paths, source URLs, author names, author IDs, profile URLs, raw comments, private messages, cookies, sessions, tokens, secrets, generated response text, target-user lists, persuasion scores, truth scores, official-status assertion fields, forecast probability fields, psychological profiles, personality diagnoses, publish/send/post/execute flags, or production readiness claims.

## Required Boundary Flags

Future 8Z-8B output must explicitly preserve:

- `entry_candidate_only = true`
- `metadata_only = true`
- `row_preview_executed = false`
- `controlled_row_preview_helper_called = false`
- `redacted_review_only_row_preview_created = false`
- `row_preview_rows_created = false`
- `synthetic_evidence_rows_created = false`
- `fake_evidence_rows_created = false`
- `row_source_path_present = false`
- `row_source_file_opened = false`
- `evidence_items_jsonl_parsed = false`
- `evidence_items_csv_parsed = false`
- `source_manifest_rows_parsed = false`
- `collection_log_rows_parsed = false`
- `package_resolver_called = false`
- `provider_result_reader_called = false`
- `local_exchange_reader_called = false`
- `review_only_staging_helper_called = false`
- `collector_job_run = false`
- `provider_job_run = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `raw_rows_exposed = false`
- `raw_comments_exposed = false`
- `raw_identities_exposed = false`
- `author_names_or_profile_urls_exposed = false`
- `secrets_read = false`
- `persistent_staging_storage_created = false`
- `actual_review_queue_runtime_used = false`
- `production_review_queue_item_created = false`
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
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Future 8Z-8B Input Contract

Future 8Z-8B may consume only safe in-memory metadata from an 8Z-7-equivalent candidate:

- review-only staging candidate schema is present as safe boundary wording
- review-only staging mode is local controlled handoff candidate
- source request/result correlation schema is present as safe boundary wording
- package reference policy is opaque safe identifier only
- metadata-only is true
- row content included is false
- raw identity included is false
- secrets included is false
- package resolver called is false
- provider result reader called is false
- local exchange reader called is false
- persistent staging storage created is false
- actual review queue runtime used is false
- production review queue item created is false
- collector job run is false
- provider job run is false
- real exchange directory read is false
- real package directory read is false
- evidence rows parsed is false
- Evidence Layer write is false
- all production object flags are false
- human review is required
- no automatic trust upgrade is required

If any required safety value is missing, ambiguous, or unsafe, future 8Z-8B must return a blocked adapter candidate and must not call any helper.

## Future 8Z-8B Action Contract

Future 8Z-8B may only transform in-memory safe metadata into a no-real-row entry candidate.

It must not:

- call `controlled_row_preview`
- call `build_controlled_row_preview`
- call `build_safe_controlled_row_preview_summary`
- use `APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`
- execute row preview
- create redacted review-only row preview
- create row-preview rows
- create synthetic evidence rows
- create fake evidence rows
- open any row source file
- read or parse `evidence_items.jsonl`
- read or parse `evidence_items.csv`
- read or parse source_manifest rows
- read or parse collection_log rows
- call package resolver
- call provider result reader
- call local exchange reader
- call review-only staging helper
- write runtime persistence
- write Evidence Layer
- create production objects
- change route/API/frontend behavior

## Future 8Z-8B Approval Phrase

Future exact approval phrase:

`APPROVE_8Z_8B_CONTROLLED_NO_REAL_ROW_ROUTE_C_ROW_PREVIEW_ENTRY_ADAPTER_SMOKE`

This phrase is inactive in 8Z-8A and must appear only as future gate wording.

It does not authorize implementation in 8Z-8A.
It does not authorize row preview execution.
It does not authorize use of the 8W-7 helper phrase.
It does not authorize `controlled_row_preview` helper calls.
It does not authorize row parsing.
It does not authorize package resolver/provider reader/local exchange reader behavior.
It does not authorize Evidence Layer write or production object creation.

## 8Z-9 Re-gate Requirement

8Z-9 phrase:

`APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE`

Status:

`inactive_not_ready_pending_no_real_row_adapter_smoke_and_re_gate`

8Z-9 cannot follow 8Z-8A directly.

If future 8Z-8B succeeds, a separate docs-only re-gate must decide whether 8Z-9 may be reconsidered. That re-gate must inspect the 8Z-8B output and confirm that no rows were read, no preview rows were created, no helper was called, no package resolver/provider reader/local exchange reader was called, no Evidence Layer write occurred, and no production objects were created.

## Relationship To 8W-7 Helper Phrase

Repaired 8W-7 helper phrase:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

This phrase is historical/future inner-helper boundary context only in 8Z-8A.

It must not authorize 8Z-8B.
It must not authorize 8Z-9.
It must not be accepted as a replacement for the 8Z-8B exact phrase.
It must not be used by the no-real-row adapter.

## Hard Blockers

Future 8Z-8B must block if:

- input is not an 8Z-7-equivalent safe review-only staging candidate
- adapter needs file reads
- adapter calls `controlled_row_preview`
- adapter uses the 8W-7 helper phrase
- adapter creates actual row preview
- adapter creates redacted row-preview output
- adapter creates preview rows
- adapter creates synthetic fake evidence rows
- adapter includes a row source path
- adapter opens a row source file
- adapter parses evidence_items / source_manifest / collection_log rows
- adapter calls package resolver / provider reader / local exchange reader
- adapter calls review-only staging helper
- adapter reads real exchange/package directories
- adapter exposes raw rows/comments/identities/profile URLs
- adapter reads secrets/cookies/sessions/browser profiles/private paths
- adapter writes Evidence Layer
- adapter creates production EvidenceItem/case/analysis_run/Analysis Result
- adapter creates persistent staging storage
- adapter creates Review Queue runtime or production Review Queue item
- adapter requires route/API/frontend
- adapter requires collector/provider job, scheduler, HTTP bridge, or webhook
- adapter requires real API / LLM / URL fetch / scraping
- adapter makes customer/public/production/final/export readiness claims

## Route C Relationship

8Z-8A does not reopen Route C.

Future 8Z-8B can only create a no-real-row entry candidate. It cannot create a row preview.

Future 8Z-9 requires a separate re-gate after 8Z-8B.

Downstream Route C Evidence candidate, Review Queue candidate, Evidence Layer write, production case, production analysis_run, actual analysis execution, and Analysis Result gates remain separate and inactive.

8Y-21 Route C stage-complete / pause remains preserved.

## 8W Relationship

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

The no-real-row entry adapter cannot satisfy 8W-68 / 8W-69 authorization protocol.

## Source Sync Contract

Source 11 update is not required because 8Z-8A changes no runtime behavior.

Do not create Source files or `docs/project_sources`.

Consider a future Source update only after a larger 8Z checkpoint and user approval.

## Validation Contract

8Z-8A validation is docs-only:

- `git diff --check`
- whitespace scan for the two new docs
- open-marker and garbled-text scan
- future 8Z-8B phrase inactive scan
- 8Z-9 phrase inactive/not-ready scan
- repaired 8W-7 helper phrase context scan
- historical phase phrase context scan
- backend/frontend/tests/runtime/Project Source scope scan
- forbidden positive-claim scan

Do not run pytest, frontend build, browser smoke, collector, provider jobs, real API/LLM/network calls, URL fetching, scraping, row-preview helper tests, or package resolver tests for 8Z-8A.
