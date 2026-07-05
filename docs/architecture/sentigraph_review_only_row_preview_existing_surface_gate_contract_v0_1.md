# Sentigraph Review-only Row Preview Existing-surface Gate Contract v0.1

## Purpose

This contract records the 8Y-3 docs-only audit boundary for existing review-only row preview and import-governance surfaces.

It defines why 8Y-3 is audit-only, why no implementation is authorized, and why the next controlled redacted review-only row preview smoke remains paused until the existing approval-phrase encoding blocker is repaired.

## Status Fields

- phase: 8Y-3
- decision: blocked
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
- selected_next_boundary_option: pause_or_blocked_before_controlled_redacted_review_only_row_preview_smoke
- future_8y4_exact_approval_phrase_required: no
- future_8y4_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Existing Surface Classification Contract

8Y-3 classifies existing surfaces by kind, row interaction, and side effect.

Surface kinds:

- docs_only
- test_only
- backend_helper
- route
- runtime
- unknown

Row interaction classes:

- no_row_read
- synthetic_fixture_only
- redacted_preview_only
- real_row_read_possible
- unknown

Side-effect classes:

- no_persistence
- runtime_local_only
- Evidence_Layer_write_possible
- production_case_possible
- production_analysis_run_possible
- unknown

The current audit found:

- metadata-only staging helpers with no row read
- disabled-by-default internal operator route with synthetic fixture-only enabled behavior
- existing controlled row-preview helper with real row read possible inside an approved controlled path
- downstream controlled candidate helpers that consume row-preview output but should not be used to justify row preview while the source gate is unsafe

## Contract Finding

8Y-3 must treat the existing row-preview implementation surface as blocked for future reuse because its exact approval phrase is currently encoded as mojibake in the helper and expected test constant.

The unsafe governance condition is:

- existing helper phrase: `鎵瑰噯 8W-7 Controlled Row Preview Implementation`
- existing test expectation: same mojibake phrase

This contract does not repair that condition. It only records that the condition blocks a future 8Y-4 controlled row-preview smoke.

## What 8Y-3 Does Not Authorize

8Y-3 does not authorize:

- backend code changes
- test changes
- route/API changes
- frontend changes
- runtime persistence
- row preview implementation
- row parsing
- real exchange directory reads
- real package row reads
- Evidence Layer write
- production EvidenceItem creation
- production case creation
- production analysis_run creation
- production Analysis Result creation authorization
- Review Queue runtime creation
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- generated response text
- provider or collector jobs
- private collector source inspection
- real API/LLM behavior
- URL fetching
- scraping
- automatic trust upgrade

## Future 8Y-4 Inactive Gate

Future 8Y-4 remains inactive.

Inactive placeholder phrase:

`APPROVE_8Y_4_CONTROLLED_REDACTED_REVIEW_ONLY_ROW_PREVIEW_SMOKE`

This phrase is not active in 8Y-3. It is only a future gate marker. It must not be interpreted as implementation approval, row parsing approval, Evidence Layer write approval, production case approval, production analysis_run approval, Source 11 runtime approval, or actual FinalSummaryReport runtime approval.

## Conditions To Reconsider 8Y-4

Before a later task can propose 8Y-4 as ready, it must prove:

- the 8W-7 approval phrase encoding is repaired or explicitly superseded
- mojibake approval text is rejected before any row source opens
- the intended phrase is tested as the only accepted phrase for that phase
- missing or wrong phrase blocks before row file access
- row count limit is explicit
- redaction policy is explicit
- allowed output fields are explicit
- privacy guard is explicit
- no-production-write guard is explicit
- no route/frontend/runtime persistence is included without a later gate

## Future 8Y-4 Hard Stop Rules

Future 8Y-4 must stop if it requires:

- accepting the mojibake 8W-7 phrase
- inspecting private collector source
- running collector jobs
- reading arbitrary real exchange directories
- reading arbitrary real package directories
- exposing raw rows, raw comments, raw identities, actual author names, or actual profile URLs
- reading or printing secrets, cookies, sessions, tokens, browser profiles, or private paths
- writing Evidence Layer
- creating production EvidenceItems
- creating production case objects
- creating production analysis_run objects
- creating Review Queue runtime objects
- adding route/API/frontend behavior
- calling Source 11 runtime
- creating actual FinalSummaryReport runtime output
- generating B-end report, Sandbox/public event, export/download/public delivery, or final delivery runtime
- calling real APIs or real LLMs
- fetching URLs or scraping
- upgrading trust automatically

## Safe Future Output Envelope

If a later 8Y-4 is separately authorized after the blocker is repaired, its output must be constrained to a safe envelope:

- schema: sentigraph_controlled_redacted_review_only_row_preview_smoke_v0_1 or equivalent
- phase: 8Y-4
- preview_mode: review_only_redacted_preview
- row_preview_created: true only in a controlled backend test path
- max_rows_applied: bounded integer
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

## Route C Interpretation

Route C remains the preferred backend mainline, but Route C is still pre-governance at this point.

8Y-3 proves only this:

- existing surfaces were audited at docs/code-reference level
- a blocker was found
- future 8Y-4 should pause until the blocker is repaired

8Y-3 does not move Sentigraph into production import, production case, production analysis_run, Source 11 runtime, actual FinalSummaryReport runtime, or public/customer-facing output.

## Validation Contract

Validation for this docs-only phase is limited to:

- `git diff --check`
- whitespace scan for the two new docs
- open-item marker and mojibake scan
- future approval phrase inactive scan
- scope scan proving no backend/frontend/tests/runtime/Project Source files changed
- forbidden positive-claim scan on changed docs

Do not run backend tests, frontend build, browser smoke, collector jobs, API/LLM/network calls, URL fetching, or scraping for 8Y-3.

## Source Sync Contract

Do not update Source 11 for 8Y-3.

Do not create Source files or `docs/project_sources/` files inside the repo.

Source updates are not recommended after this commit unless the user wants a ChatGPT-side context patch that records the pause/blocker.
