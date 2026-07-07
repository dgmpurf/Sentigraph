# Sentigraph 8Z-8 On-demand Collector Review-only Staging to Route C Entry Gate Decision v0.1

## Decision

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

## Purpose

8Z-8 is a docs-only gate decision. It decides whether the 8Z-7 local controlled review-only staging candidate may be considered for a future controlled Route C entry / row-preview smoke.

This phase does not execute row preview, call `controlled_row_preview`, call the review-only staging helper, read package rows, parse evidence files, call package resolver/provider reader/local exchange reader, write Evidence Layer, create production objects, change routes, change frontend code, change runtime behavior, or update Project Source files.

## 8Z State Summary

- 8Z-1 created the on-demand collector workflow contract as docs-only.
- 8Z-2 created the request/result metadata contract as docs-only.
- 8Z-3 completed controlled request metadata fixture smoke.
- 8Z-4 completed controlled provider_result metadata fixture smoke.
- 8Z-5 completed controlled request/result correlation smoke.
- 8Z-6 created the review-only staging handoff gate docs-only.
- 8Z-7 completed controlled request/result correlation to review-only staging handoff smoke.
- 8Z-8 is only the Route C entry / row-preview gate decision.
- 8Y Route C remains stage-complete and paused.
- 8W-69 pause remains preserved.
- 8W-70 reactivation remains not selected.

## 8Z-7 Output Interpretation

8Z-7 produced a local controlled review-only staging candidate inside a backend test path only.

8Z-7 output is:

- metadata-only
- controlled backend test path only
- using an opaque safe package reference
- human-review-required
- no automatic trust upgrade
- not persistent staging storage
- not Review Queue runtime
- not a production Review Queue item
- not Evidence Layer write
- not production EvidenceItem
- not production case
- not production analysis_run
- not actual analysis execution
- not production Analysis Result authorization or creation
- not row preview
- not row parsing
- not package resolver output
- not Source 11 / FinalSummaryReport / B-end / Sandbox / export / delivery runtime

Therefore 8Z-7 can be used only as a governance input for deciding whether a future row-preview entry should even be discussed. It cannot be promoted automatically into Route C or row-preview execution.

## Route C Entry / Row-preview Surface Audit Summary

| Surface | Classification | Relation to 8Z | Side effects / notes |
| --- | --- | --- | --- |
| `backend/app/services/private_collector_review_only_staging.py` | backend_helper | review_only_staging_source | metadata-only helper; no persistence flags; no production flags |
| `backend/app/tests/test_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke.py` | test_only | review_only_staging_source | creates 8Z-7 candidate in controlled test path only |
| `docs/health/sentigraph_8z_7_controlled_on_demand_collector_request_result_correlation_to_review_only_staging_handoff_smoke_report_v0_1.md` | docs_only | review_only_staging_source | reports 8Z-7 no-call/no-read proof |
| `backend/app/services/controlled_row_preview.py` | backend_helper | controlled_row_preview | existing controlled helper; canonical ASCII 8W-7 phrase; opens fixed approved row source if executed |
| `backend/app/tests/test_controlled_row_preview.py` | test_only | controlled_row_preview | proves canonical phrase and rejects missing/wrong/old garbled phrase before row source open |
| `backend/app/tests/test_8y_4_controlled_redacted_review_only_row_preview_smoke.py` | test_only | row_preview_entry | controlled Route C row-preview smoke from 8Y path; reads bounded approved row source under helper behavior |
| `docs/health/sentigraph_8y_4_controlled_redacted_review_only_row_preview_smoke_report_v0_1.md` | docs_only | row_preview_entry | records redacted review-only preview boundary |
| `docs/planning/sentigraph_8y_3b_row_preview_gate_reevaluation_after_phrase_repair_decision_v0_1.md` | docs_only | controlled_row_preview | confirms 8W-7 phrase repair and 8Y-4 proposal readiness |
| `docs/architecture/sentigraph_row_preview_gate_reevaluation_after_phrase_repair_contract_v0_1.md` | docs_only | controlled_row_preview | defines repaired row-preview gate contract |
| `backend/app/services/controlled_evidence_candidate.py` | backend_helper | evidence_candidate_downstream | downstream Route C helper; not eligible in 8Z-8 |
| `backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py` | test_only | evidence_candidate_downstream | downstream after row preview; not eligible in 8Z-8 |
| `backend/app/services/private_collector_package_resolver.py` | backend_helper | package_resolution | package metadata/path resolution surface; not allowed for 8Z-9 by default |
| `backend/app/services/private_collector_provider_result_reader.py` | backend_helper | provider_result_reader | provider result reader surface; not allowed for 8Z-9 by default |
| `backend/app/services/local_exchange_reader.py` | runtime_helper | provider_result_reader | local exchange metadata reader; not allowed for 8Z-9 by default |

Audit result:

- A controlled row-preview helper exists.
- Row-preview tests exist.
- A canonical ASCII 8W-7 helper phrase exists: `APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`.
- Tests reject old garbled and wrong approval phrases before row source open.
- A Route C row-preview to evidence candidate path exists downstream.
- A review-only staging helper exists.
- Package resolver, provider reader, and local exchange reader surfaces exist but remain out of scope.

Blocking compatibility finding:

The current controlled row-preview helper is not a direct 8Z-7 review-only staging candidate entry. It expects the earlier Route C metadata-smoke/review-only-staging boundary shape and, when executed successfully, opens and parses its fixed approved `evidence_items.jsonl` row source. The 8Z-8 future scope requires no real exchange/package dir reads and no real package row parsing. Because no in-memory/synthetic/no-real-row adapter from the 8Z-7 candidate to Route C row-preview is confirmed, this gate selects pause/block rather than readiness.

## Gate Interpretation

8Z-8 may only allow a future local controlled row-preview entry smoke if a safe entry surface exists for the 8Z-7 candidate.

The current decision is blocked because the safe direct entry surface is not yet confirmed. A future 8Z-9 should not be started until the next prompt explicitly resolves the compatibility gap.

Any future 8Z-9, if later reopened, must be:

- backend-only
- test-first
- controlled smoke only
- local-only
- review-only
- using only safe in-memory, synthetic, or temp fixture material inside backend test path
- using the existing controlled row-preview helper only if it can be used without real exchange/package dir reads and without production package row parsing
- redacted preview only if row-preview output is created
- preserving human review and no automatic trust upgrade

## Allowed Future 8Z-9 Input If Reopened

Future 8Z-9 may use only the 8Z-7 local controlled review-only staging candidate or an equivalent safe fixture with:

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

## Future 8Z-9 Inactive Approval Phrase

Future 8Z-9 exact approval phrase:

`APPROVE_8Z_9_CONTROLLED_ON_DEMAND_COLLECTOR_REVIEW_ONLY_STAGING_TO_ROUTE_C_ROW_PREVIEW_SMOKE`

This phrase is inactive in 8Z-8. It does not authorize implementation, row preview execution, row parsing, collector execution, provider jobs, request/result reader runtime, package resolver behavior, real exchange/package directory reads, Evidence Layer write, production EvidenceItem/case/analysis_run creation, actual analysis execution, production Analysis Result authorization, or production Analysis Result creation.

The repaired 8W-7 helper phrase may be required for a future helper call only if 8Z-9 is separately approved and the compatibility blocker is resolved:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

That 8W-7 helper phrase is inactive for 8Z-8 and does not authorize 8Z-9 by itself.

## Future 8Z-9 Output Constraints If Later Approved

Future 8Z-9 output must preserve:

- `route_c_row_preview_entry_created = true` only inside controlled backend test path
- `redacted_review_only_row_preview_created = true` only inside controlled backend test path if a safe helper output uses that shape
- `row_preview_schema = sentigraph_controlled_redacted_review_only_row_preview_v0_1` or existing safe equivalent
- `row_preview_mode = backend_only_local_route_c_row_preview_entry` or existing safe equivalent
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

## Hard Blockers For Future 8Z-9

Block future 8Z-9 if any of these hold:

- no safe controlled row-preview helper surface is found for 8Z-7 candidate input
- row-preview helper approval phrase is missing, unsafe, garbled, or not ASCII
- old garbled or Chinese row-preview phrase is accepted
- helper requires real exchange/package directory reads
- helper requires production package row parsing
- helper exposes raw rows/comments/identities
- helper requires package resolver or provider reader call unless separately gated
- helper writes Evidence Layer
- helper creates production EvidenceItem, production case, production analysis_run, or production Analysis Result
- helper creates Review Queue runtime or production Review Queue item
- helper requires route/API/frontend
- helper requires collector/provider job execution
- helper requires scheduler / HTTP bridge / webhook
- helper requires secrets/cookies/sessions/browser profiles
- helper requires real API / LLM / URL fetch / scraping
- helper makes customer/public/production/final/export readiness claims

## Relationship To Route C

8Z-9, if later approved, can only re-enter Route C at the controlled row-preview boundary. After any future 8Z-9 row-preview smoke, downstream Route C Evidence candidate, Review Queue candidate, Evidence Layer gates, production case gates, analysis_run gates, actual analysis execution gates, and Analysis Result gates remain separate.

8Z-8 and any future 8Z-9 do not reopen actual analysis execution and do not authorize production Analysis Result. 8Y-21 stage-complete / pause remains preserved.

## Relationship To 8W

8W-69 pause remains preserved.

8W-70 reactivation remains not selected.

Row-preview entry cannot satisfy the 8W-68 / 8W-69 authorization protocol.

## Relationship To Source 11 / Project Source

Source 11 update is not required because 8Z-8 changes no runtime behavior.

Do not create Project Source files or `docs/project_sources/` files for 8Z-8.

A future Source update may be considered after a larger 8Z checkpoint, not after this single docs-only gate.

## Recommended Next Task

Recommended next task:

Phase 8Z-8A docs-only compatibility design for a no-real-row, in-memory/synthetic 8Z-7 candidate to Route C row-preview entry adapter.

Do not implement 8Z-9 until the compatibility blocker is resolved by a separate gate.
