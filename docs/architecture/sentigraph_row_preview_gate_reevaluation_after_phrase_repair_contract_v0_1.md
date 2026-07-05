# Sentigraph Row Preview Gate Re-evaluation After Phrase Repair Contract v0.1

## Purpose

This contract records the 8Y-3B docs-only re-evaluation after the 8Y-3A approval-phrase repair.

It determines whether the previous 8Y-3 blocker is repaired enough to allow a future controlled redacted review-only row preview smoke to be proposed. It does not implement or execute that future smoke.

## Status Fields

- phase: 8Y-3B
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- audit_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- row_preview_implemented: no
- evidence_rows_parsed: no
- real_exchange_dir_read: no
- real_package_rows_read: no
- evidence_layer_write: no
- production_evidence_item_created: no
- production_case_created: no
- production_analysis_run_created: no
- production_analysis_result_creation_authorized: no
- source11_runtime_called: no
- actual_final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- export_download_public_delivery_created: no
- source_files_created: no
- docs_project_sources_created: no
- blocker_repaired: yes
- selected_next_boundary_option: ready_for_8Y_4_controlled_redacted_review_only_row_preview_smoke
- future_8y4_exact_approval_phrase_required: yes
- future_8y4_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Re-evaluation Inputs

8Y-3B may inspect only repository-controlled files:

- `backend/app/services/controlled_row_preview.py`
- `backend/app/tests/test_controlled_row_preview.py`
- `docs/health/sentigraph_8w_7_controlled_row_preview_implementation_report_v0_1.md`
- `docs/health/sentigraph_8y_3a_repair_8w_7_row_preview_approval_phrase_encoding_report_v0_1.md`
- `docs/planning/sentigraph_8y_3_review_only_row_preview_existing_surface_audit_gate_decision_v0_1.md`
- `docs/architecture/sentigraph_review_only_row_preview_existing_surface_gate_contract_v0_1.md`

8Y-3B must not inspect private collector source, real exchange directories, real package directories, package row content, raw comments, raw identities, actual author names, actual profile URLs, secrets, sessions, tokens, cookies, browser profiles, or private paths.

## Repair Acceptance Criteria

The 8Y-3 blocker is considered repaired only if all criteria are true:

- 8W-7 active helper phrase is `APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`.
- The helper phrase is ASCII.
- The test expectation matches the active helper phrase.
- The old Chinese phrase is present only as a negative input or superseded history.
- The old garbled phrase is present only as a negative input or superseded history.
- Missing, wrong, old Chinese, and old garbled phrase cases block before row-source access.
- Focused tests for the controlled row-preview helper passed in 8Y-3A.
- Nearby tests for the next candidate helper and golden contracts passed in 8Y-3A.
- 8Y-3A did not expand row-preview capability.
- 8Y-3A did not add route/API/frontend/runtime persistence.
- 8Y-3A did not write Evidence Layer or create production EvidenceItem/case/analysis_run.

The current audit satisfies these criteria, so `blocker_repaired = yes`.

## Future 8Y-4 Gate Contract

Future 8Y-4 remains inactive.

Future exact approval phrase:

`APPROVE_8Y_4_CONTROLLED_REDACTED_REVIEW_ONLY_ROW_PREVIEW_SMOKE`

This phrase is not active in 8Y-3B. It is only future gate wording. It must not be treated as approval to implement, execute row preview, parse rows, write Evidence Layer, create production EvidenceItems, create production cases, create production analysis_run objects, call Source 11 runtime, or create actual FinalSummaryReport runtime output.

## Future 8Y-4 Allowed Envelope

If later separately approved, 8Y-4 must remain within this envelope:

- backend-only
- test-first
- controlled smoke only
- use existing controlled row-preview helper surface only
- require canonical 8W-7 ASCII phrase
- require separate 8Y-4 exact phrase
- bounded row preview only
- redacted row preview only
- review-only output
- no raw rows, comments, identities, actual author names, or actual profile URLs
- no arbitrary package path
- no private collector source
- no collector job
- no Evidence Layer write
- no production EvidenceItem
- no production case
- no production analysis_run
- no Review Queue runtime
- no route/API/frontend
- no Source 11 runtime
- no actual FinalSummaryReport runtime
- no B-end/Sandbox/export/public delivery

## Future 8Y-4 Required Output Constraints

Future 8Y-4 output, if separately approved, must preserve:

- preview_mode: review_only_redacted_preview or equivalent
- row_preview_created: true only in a controlled backend test path
- max_rows_applied: bounded integer
- row_limit_enforced: true
- redaction_policy_version: explicit
- human_review_required: true
- no_automatic_trust_upgrade: true
- raw_rows_exposed: false
- raw_comments_exposed: false
- raw_identities_exposed: false
- author_names_or_profile_urls_exposed: false
- secrets_read: false
- evidence_layer_write: false
- production_evidence_item_created: false
- production_case_created: false
- production_analysis_run_created: false
- review_queue_runtime_used: false
- source11_runtime_called: false
- actual_final_summary_report_created: false
- route_ready: false
- frontend_ready: false
- production_ready: false
- customer_ready: false
- public_ready: false

## Future 8Y-4 Blockers

Future 8Y-4 must block on:

- canonical 8W-7 phrase missing or changed
- old garbled phrase accepted
- missing or wrong phrase opens a row source
- arbitrary real exchange directory request
- arbitrary real package directory request
- raw row/comment/identity exposure request
- private collector source inspection request
- collector job execution request
- Evidence Layer write request
- production EvidenceItem, case, or analysis_run request
- Review Queue runtime request
- route/API/frontend request
- Source 11 runtime request
- actual FinalSummaryReport runtime request
- B-end/Sandbox/export/public delivery request
- real API/LLM/network/fetch/scrape request
- automatic trust upgrade request
- customer/public/production readiness claim request

## Non-authorization Boundary

8Y-3B is not:

- row preview implementation
- row preview execution
- row parsing
- Evidence Layer import
- production EvidenceItem creation
- production case creation
- production analysis_run creation
- Review Queue runtime
- Source 11 runtime
- actual FinalSummaryReport runtime
- route/API/frontend integration
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime

8Y-3B only authorizes discussion of a future 8Y-4 proposal, not 8Y-4 execution.

## Validation Contract

Validation for 8Y-3B is docs-only:

- `git diff --check`
- whitespace scan for the two new docs
- open-item marker and garbled-text scan
- future approval phrase inactive scan
- scope scan proving no backend/frontend/tests/runtime/Project Source files changed
- forbidden positive-claim scan on changed docs

Do not run pytest, frontend build, browser smoke, collector, API/LLM/network calls, URL fetching, or scraping for 8Y-3B.

## Source Sync Contract

Do not update Source 11 for 8Y-3B.

Do not create Source files or `docs/project_sources/` files inside the repo.

Source updates are not recommended after this commit unless the user wants a separate ChatGPT-side context patch.

