# Sentigraph On-demand Collector Review-only Staging to Route C Entry Gate Contract v0.1

## Purpose

This contract defines the 8Z-8 docs-only gate between the 8Z-7 on-demand collector review-only staging candidate and any future Route C row-preview entry smoke.

It is a planning and governance contract only. It does not implement or execute row preview, call helper code, call package resolver/provider reader/local exchange reader, read real exchange or package directories, parse rows, write Evidence Layer, create production objects, change routes, change frontend code, change runtime behavior, or create Project Source files.

## Status Fields

- phase: 8Z-8
- decision: blocked
- privacy_issue_stop: no
- docs_only: yes
- gate_decision_only: yes
- route_c_entry_gate_only: yes
- row_preview_gate_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- helper_called: no
- row_preview_executed: no
- controlled_row_preview_helper_called: no
- route_c_row_preview_entry_created: no
- redacted_review_only_row_preview_created: no
- package_resolver_called: no
- provider_result_reader_called: no
- local_exchange_reader_called: no
- review_only_staging_helper_called: no
- persistent_staging_storage_created: no
- actual_review_queue_runtime_used: no
- production_review_queue_item_created: no
- collector_job_run: no
- provider_job_run: no
- scheduler_created: no
- http_bridge_created: no
- webhook_created: no
- private_collector_source_inspected: no
- real_exchange_dir_read: no
- real_package_dir_read: no
- evidence_rows_parsed: no
- original_package_rows_read: no
- evidence_items_csv_parsed: no
- source_manifest_rows_parsed: no
- collection_log_rows_parsed: no
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
- selected_next_boundary_option: pause_or_blocked_before_on_demand_collector_route_c_row_preview_smoke
- future_8z9_exact_approval_phrase_required: no_until_blockers_repaired
- future_8z9_exact_approval_phrase_active: no
- future_8z9_exact_approval_phrase: APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE
- repaired_8w7_helper_phrase_required_for_future_8z9: yes_if_later_reopened
- repaired_8w7_helper_phrase_active_for_8z8: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Inputs Considered

8Z-8 considered these local repo surfaces by inspection only:

- `backend/app/services/private_collector_review_only_staging.py`
- `backend/app/tests/test_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke.py`
- `docs/health/sentigraph_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke_report_v0_1.md`
- `backend/app/services/controlled_row_preview.py`
- `backend/app/tests/test_controlled_row_preview.py`
- `backend/app/tests/test_8y_4_controlled_redacted_review_only_row_preview_smoke.py`
- `docs/health/sentigraph_8y_4_controlled_redacted_review_only_row_preview_smoke_report_v0_1.md`
- `docs/planning/sentigraph_8y_3b_row_preview_gate_reevaluation_after_phrase_repair_decision_v0_1.md`
- `docs/architecture/sentigraph_row_preview_gate_reevaluation_after_phrase_repair_contract_v0_1.md`
- `docs/architecture/sentigraph_on_demand_collector_review_only_staging_handoff_gate_contract_v0_1.md`
- `docs/planning/sentigraph_8z_6_on_demand_collector_review_only_staging_handoff_gate_decision_v0_1.md`

This inspection did not call helper code, run tests, execute row preview, inspect private collector source, read exchange directories, read package directories, parse evidence rows, or read secrets.

## Surface Classification

| Surface | Surface type | 8Z relation | Side-effect class |
| --- | --- | --- | --- |
| `private_collector_review_only_staging.py` | backend_helper | review_only_staging_source | metadata_only; no_persistence flags |
| `test_8z_7_controlled...handoff_smoke.py` | test_only | review_only_staging_source | test_local_only; no reads by monkeypatch proof |
| 8Z-7 health report | docs_only | review_only_staging_source | no runtime |
| `controlled_row_preview.py` | backend_helper | controlled_row_preview | controlled helper; real approved row source open if executed |
| `test_controlled_row_preview.py` | test_only | controlled_row_preview | phrase and safety tests |
| `test_8y_4_controlled_redacted_review_only_row_preview_smoke.py` | test_only | row_preview_entry | controlled Route C path; bounded/redacted output |
| 8Y-4 health report | docs_only | row_preview_entry | no runtime |
| 8Y-3B planning/contract docs | docs_only | controlled_row_preview | phrase repair and future row-preview gate |
| `controlled_evidence_candidate.py` / 8Y-6 tests | backend_helper / test_only | evidence_candidate_downstream | downstream only, not 8Z-8 eligible |
| package resolver / provider reader / local exchange reader | backend_helper / runtime_helper | package_resolution / provider_result_reader | out of scope for 8Z-9 by default |

## Compatibility Decision

The selected next boundary is:

`pause_or_blocked_before_on_demand_collector_route_c_row_preview_smoke`

Reason:

- The existing controlled row-preview helper is safe for its prior Route C context only when called under its own gate.
- The helper has a repaired canonical ASCII inner phrase: `APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`.
- The helper tests reject old garbled/wrong phrases before row-source open.
- However, the helper does not currently expose a confirmed direct adapter from the 8Z-7 review-only staging candidate shape.
- Successful helper execution opens and parses the fixed approved `evidence_items.jsonl` row source.
- 8Z-9 scope must not read real exchange/package directories or parse real package rows.
- No in-memory/synthetic/no-real-row 8Z-7 candidate to Route C row-preview entry adapter is confirmed.

Therefore 8Z-8 does not mark 8Z-9 ready. It blocks until a separate compatibility design or gate resolves the no-real-row entry requirement.

## Required Future 8Z-9 Input Envelope If Reopened

Future 8Z-9 may accept only an 8Z-7 local controlled review-only staging candidate or equivalent safe fixture where all of these are true:

- `review_only_staging_candidate_schema` is an existing safe equivalent or `sentigraph_on_demand_collector_review_only_staging_candidate_v0_1`
- `review_only_staging_mode` is an existing safe equivalent or `backend_only_local_review_only_staging_handoff_candidate`
- `source_request_result_correlation_schema` is an existing safe equivalent or `sentigraph_on_demand_collector_request_result_correlation_v0_1`
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
- production EvidenceItem/case/analysis_run/Analysis Result flags are false
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Future 8Z-9 Action Envelope If Reopened

Future 8Z-9 must be separately approved and may only be:

- backend-only
- test-first
- controlled smoke only
- local-only
- review-only
- no route/API/frontend
- no runtime persistence
- no collector/provider jobs
- no scheduler / HTTP bridge / webhook
- no package resolver / provider reader / local exchange reader calls by default
- no private collector source inspection
- no real exchange/package directory reads
- no production package row parsing
- no raw rows/comments/identities/author names/profile URLs exposure
- no Evidence Layer write
- no production EvidenceItem/case/analysis_run/Analysis Result
- no Review Queue runtime or production Review Queue item
- no Source 11 / FinalSummaryReport / B-end / Sandbox / export / delivery runtime
- no real API / LLM / URL fetch / scraping

Future 8Z-9 may create a local controlled Route C row-preview entry object or redacted review-only row-preview output only inside a backend test path, and only after the compatibility blocker is resolved.

## Inactive Future Approval Phrase

Future 8Z-9 phrase:

`APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE`

This phrase is inactive in 8Z-8. It appears only as future gate wording.

It does not authorize implementation, row-preview execution, helper calls, row parsing, package resolver behavior, provider jobs, collector jobs, request/result reader runtime, real exchange/package directory reads, Evidence Layer writes, production object creation, actual analysis execution, production Analysis Result authorization, or production Analysis Result creation.

## Repaired Inner Helper Phrase Boundary

Repaired inner helper phrase:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

This phrase is an 8W-7 controlled row-preview helper phrase. It is inactive for 8Z-8 and cannot authorize 8Z-9 by itself.

If 8Z-9 is later reopened, that phase must prove:

- the 8W-7 helper phrase remains ASCII
- old garbled / Chinese row-preview phrases remain rejected
- missing or wrong phrase blocks before row-source access
- the 8Z-9 outer phrase is separately required
- the 8W-7 inner phrase cannot substitute for the 8Z-9 outer phrase

## Future 8Z-9 Output Contract If Reopened

Any future output must include false side-effect flags:

- `raw_rows_exposed = false`
- `raw_comments_exposed = false`
- `raw_identities_exposed = false`
- `author_names_or_profile_urls_exposed = false`
- `real_exchange_dir_read = false`
- `real_package_dir_read = false`
- `original_package_rows_read = false`
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
- `actual_review_queue_runtime_used = false`
- `production_review_queue_item_created = false`
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

## Stop Rules

Future work must stop if it requires or discovers:

- no safe row-preview entry surface for 8Z-7 candidate input
- helper approval phrase missing, unsafe, garbled, non-ASCII, or bypassable
- old garbled or Chinese phrase accepted
- file open before exact approval phrase validation
- real exchange/package directory reads
- production package row parsing
- raw rows/comments/identities exposure
- actual author names/profile URLs exposure
- cookies/sessions/tokens/browser profiles/secrets/private paths
- package resolver/provider reader/local exchange reader call without a separate gate
- persistent staging storage
- Review Queue runtime or production Review Queue item
- Evidence Layer write
- production EvidenceItem/case/analysis_run/Analysis Result
- actual analysis execution
- 8W-70 reactivation
- Source 11 / FinalSummaryReport / B-end / Sandbox / export / delivery runtime
- route/API/frontend requirement
- collector/provider job
- scheduler / polling / daemon
- HTTP bridge / webhook
- real API / LLM / URL fetch / scraping
- customer/public/production/final/export readiness claim

## Validation Contract For 8Z-8

8Z-8 validation is docs-only:

- `git diff --check`
- no-index whitespace check for the two new docs
- open-marker and garbled-text scan
- future 8Z-9 phrase inactive scan
- repaired 8W-7 helper phrase scan
- historical 8Z / 8Y / 8W phrase context scan
- backend/frontend/tests/runtime/Project Source scope scan
- forbidden positive-claim scan

Do not run pytest, frontend build, browser smoke, collector, provider jobs, real API/LLM/network calls, URL fetching, scraping, row-preview helper tests, or package resolver tests for 8Z-8.

## Source Sync Contract

Source update is not recommended after 8Z-8 because this phase changes no runtime behavior and selects a pause/block boundary.

Do not update Source 11.

Do not create `docs/project_sources/`.

Do not create Project Source package files in this repository.
