# Sentigraph Import-candidate Source Path Contract v0.1

## Purpose

This contract records the 8Y-5A source-path decision after the 8Y-5 Evidence Layer import gate pause.

It selects the source path that must be used before any Evidence Layer import candidate smoke is proposed.

This contract is docs-only and gate-only. It does not implement the source path, create evidence candidates, create import candidates, write Evidence Layer, create production EvidenceItems, create production cases, create production `analysis_run` records, create Review Queue runtime, add route/API/frontend behavior, call Source 11 runtime, create actual FinalSummaryReport runtime output, generate B-end/Sandbox/export/public-delivery runtime, call real APIs/LLMs, run provider/collector jobs, fetch URLs, scrape pages, inspect private collector source, or read arbitrary exchange/package directories.

## Status Fields

- phase: 8Y-5A
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- gate_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- source_path_implemented: no
- evidence_candidate_created: no
- import_candidate_created: no
- evidence_item_shaped_candidate_created: no
- evidence_layer_write: no
- production_evidence_item_created: no
- production_case_created: no
- production_analysis_run_created: no
- production_analysis_result_creation_authorized: no
- review_queue_runtime_used: no
- source11_runtime_called: no
- actual_final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- export_download_public_delivery_created: no
- source_files_created: no
- docs_project_sources_created: no
- selected_source_path: option_A_multi_step_helper_chain
- selected_next_boundary_option: ready_for_8Y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke
- future_8y6_exact_approval_phrase_required: yes
- future_8y6_exact_approval_phrase_active: no
- old_direct_import_candidate_phrase_status: inactive_not_selected_after_source_path_decision
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Selected Source Path

Selected:

`option_A_multi_step_helper_chain`

Required path:

`redacted row preview -> controlled evidence candidate -> review-only / review queue candidate -> Evidence Layer import candidate`

This path is selected because it keeps Route C stepwise and avoids jumping directly from redacted row preview into Evidence Layer import semantics.

## Non-selected Paths

Option B, direct adapter:

`redacted row preview -> Evidence Layer import candidate`

Status:

`not_selected`

Reason:

It would over-compress Route C and skip intermediate evidence candidate and review queue candidate boundaries.

Option C, continue pause:

Status:

`not_selected`

Reason:

Existing helper and test surfaces are sufficient to select a future controlled row-preview-to-evidence-candidate source-path smoke as the next gate.

## Required Existing Surface Chain

The selected source path relies on these existing surfaces:

| Step | Existing surface | Surface type | Expected output class | Side-effect contract |
| --- | --- | --- | --- | --- |
| 1 | `controlled_row_preview` | backend_helper | `sentigraph_controlled_row_preview_v0_1` | approved controlled row preview only |
| 2 | `controlled_evidence_candidate` | backend_helper | `sentigraph_controlled_evidence_candidate_set_v0_1` | local candidate only |
| 3 | `controlled_review_queue_candidate` | backend_helper | `sentigraph_controlled_review_queue_candidate_set_v0_1` | local review queue candidate only |
| 4 | `controlled_evidence_layer_import_candidate` | backend_helper | `sentigraph_controlled_evidence_layer_import_candidate_set_v0_1` | local import candidate only |

8Y-6 may only target step 2:

`redacted row preview -> controlled evidence candidate`

Later steps require separate gates.

## Future 8Y-6 Contract

Future 8Y-6, if separately approved, may only create a local controlled evidence candidate object from an existing safe row preview output.

It must use this inactive future phrase:

`APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE`

future_8y6_exact_approval_phrase_active: no

8Y-5A does not approve 8Y-6 implementation.

## Old Direct Import Candidate Phrase

Earlier direct 8Y-6 phrase from 8Y-5:

`APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE`

Status:

`inactive_not_selected_after_source_path_decision`

It must not be treated as active approval for any future work.

## Future 8Y-6 Input Contract

Allowed input:

- 8Y-4 controlled redacted review-only row preview output
- schema `sentigraph_controlled_row_preview_v0_1` or safe equivalent
- bounded rows only
- redacted snippets only
- human_review_required = true
- no_automatic_trust_upgrade = true
- no Evidence Layer write
- no production EvidenceItem
- no production case
- no production `analysis_run`
- no Review Queue runtime
- no Source 11 runtime
- no actual FinalSummaryReport runtime

Forbidden input:

- arbitrary package directory
- arbitrary real exchange directory
- private collector source
- private collector raw output
- source manifest rows
- collection log rows
- CSV rows
- original package rows
- raw comments
- raw identities
- actual author names
- actual profile URLs
- route/API request objects
- frontend state
- Evidence Layer records
- production case objects
- production `analysis_run` objects
- Source 11 outputs
- FinalSummaryReport outputs

## Future 8Y-6 Output Contract

Required output constraints:

- evidence_candidate_created may be true only inside controlled backend test path
- evidence_candidate_mode = review_only_local_controlled_evidence_candidate or safe equivalent
- source_preview_schema = `sentigraph_controlled_row_preview_v0_1` or safe equivalent
- raw_rows_exposed = false
- raw_comments_exposed = false
- raw_identities_exposed = false
- author_names_or_profile_urls_exposed = false
- secrets_read = false
- evidence_layer_write = false
- production_evidence_item_created = false
- production_case_created = false
- production_analysis_run_created = false
- review_queue_runtime_used = false
- source11_runtime_called = false
- actual_final_summary_report_created = false
- b_end_report_runtime_generated = false
- sandbox_public_event_runtime_generated = false
- export_download_public_delivery_created = false
- generated_response_text = false
- route_ready = false
- frontend_ready = false
- production_ready = false
- customer_ready = false
- public_ready = false
- human_review_required = true
- no_automatic_trust_upgrade = true

## Future 8Y-6 Validation Expectations

Future 8Y-6 tests should prove:

- exact 8Y-6 phrase is required for the smoke
- inactive old direct import phrase is rejected
- 8W-10 controlled evidence candidate helper phrase is provided only inside the controlled test path if needed
- source preview schema must be safe
- source preview status must preserve review/manual-warning state
- candidate count stays bounded
- raw rows, comments, identities, author names, profile URLs, and secret-like fields are blocked
- Evidence Layer write remains false
- production EvidenceItem creation remains false
- production case creation remains false
- production `analysis_run` creation remains false
- Review Queue runtime remains false
- route/API/frontend flags remain false
- Source 11 and actual FinalSummaryReport runtime flags remain false
- B-end/Sandbox/export/public-delivery flags remain false

## Hard Stop Rules

Stop any future source-path smoke if it requires:

- no safe evidence candidate helper surface found
- direct Evidence Layer write
- production EvidenceItem creation
- production case creation
- production `analysis_run` creation
- Review Queue runtime
- route/API/frontend
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- raw row/comment/identity exposure
- author names/profile URLs as actual values
- arbitrary real exchange directory
- arbitrary package directory
- private collector source inspection
- collector job execution
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claims

## Relationship to Later Gates

Future 8Y-6 can only validate the first selected source-path hop:

`row preview -> controlled evidence candidate`

Later gates remain separate:

- review-only / review queue candidate gate
- Evidence Layer import candidate gate
- Evidence Layer write gate
- production case gate
- production `analysis_run` gate
- Source 11 runtime gate
- actual FinalSummaryReport runtime gate
- B-end/Sandbox/export/public-delivery gates

## Validation Contract

Validation for 8Y-5A is docs-only:

- `git diff --check`
- whitespace scan for the two 8Y-5A docs
- open-marker/mojibake scan
- future approval phrase inactive scan
- old direct phrase inactive scan
- backend/frontend/tests/runtime/Project Source scope scan
- forbidden positive-claim scan with matches accepted only when they are explicit no/false/boundary language

Do not run pytest, frontend build, browser smoke, collector jobs, real API/LLM/network calls, URL fetching, scraping, row parsing, or exchange-directory reads for 8Y-5A.

## Source Sync Contract

Do not update Source 11 for 8Y-5A.

Do not create Source files or `docs/project_sources/` files inside the repo.

Source updates are not recommended after this commit unless the user separately wants a ChatGPT-side summary patch.
