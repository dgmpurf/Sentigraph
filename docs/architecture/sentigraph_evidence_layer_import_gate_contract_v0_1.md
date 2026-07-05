# Sentigraph Evidence Layer Import Gate Contract v0.1

## Purpose

This contract records the 8Y-5 Evidence Layer Import Gate boundary for Route C.

It decides whether the 8Y-4 controlled redacted review-only row preview output may later be considered as input for a controlled Evidence Layer import candidate smoke.

This contract is docs-only and gate-only. It does not implement import, create import candidates, create EvidenceItem-shaped candidates, write Evidence Layer, create production EvidenceItems, create production cases, create production `analysis_run` records, create Review Queue runtime, add route/API/frontend behavior, call Source 11 runtime, create actual FinalSummaryReport runtime output, generate B-end/Sandbox/export/public-delivery runtime, call real APIs/LLMs, run provider/collector jobs, fetch URLs, scrape pages, inspect private collector source, or read arbitrary exchange/package directories.

## Status Fields

- phase: 8Y-5
- decision: blocked
- privacy_issue_stop: no
- docs_only: yes
- gate_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- import_implemented: no
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
- selected_next_boundary_option: pause_or_blocked_before_controlled_evidence_layer_import_candidate_smoke
- future_8y6_exact_approval_phrase_required: yes, if reopened
- future_8y6_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Source Object Contract

8Y-5 may consider only the 8Y-4 redacted review-only row preview output as a future source candidate for governance discussion.

Required source envelope:

- schema: `sentigraph_controlled_row_preview_v0_1` or existing safe equivalent
- preview mode: `review_only_redacted_preview` or equivalent
- approved source: `evidence_items.jsonl` only in approved controlled backend test path
- row source policy: `single_approved_jsonl_source_only`
- row limit enforced: true
- raw rows exposed: false
- raw comments exposed: false
- raw identities exposed: false
- author names or profile URLs exposed: false
- secrets read: false
- human review required: true
- warning/manual-review preserved: true
- no automatic trust upgrade: true
- Evidence Layer write: false
- production EvidenceItem created: false
- production case created: false
- production `analysis_run` created: false
- Review Queue runtime used: false
- Source 11 runtime called: false
- actual FinalSummaryReport runtime created: false

The source object is not an Evidence Layer record, not production evidence, not officially verified status, not production case input, not production `analysis_run` input, not analysis-ready material, not report-ready material, and not public/customer-facing output.

## Existing Surface Classification

8Y-5 classifies relevant existing surfaces as follows:

| Surface | Kind | Relation to Evidence Layer | Side effects | Contract finding |
| --- | --- | --- | --- | --- |
| `controlled_row_preview` helper | backend_helper | no_import | approved controlled row read only | Valid 8Y-4 source preview surface; not import. |
| 8Y-4 smoke test | test_only | no_import | controlled test path only | Valid proof of redacted preview envelope; not import. |
| `controlled_evidence_candidate` helper | backend_helper | import_candidate_only | no_persistence | Intermediate candidate helper from row preview; not Evidence Layer import. |
| `controlled_review_queue_candidate` helper | backend_helper | review_only_candidate | no_persistence | Intermediate review-queue-candidate helper; not Review Queue runtime. |
| `controlled_evidence_layer_import_candidate` helper | backend_helper | import_candidate_only | no_persistence | Existing import candidate helper expects review queue candidate set, not direct row preview. |
| `controlled_evidence_layer_write_candidate` helper | backend_helper | evidence_layer_write_possible only as candidate boundary | no_persistence | Later-stage candidate; out of scope. |
| `controlled_production_evidence_import_candidate` helper | backend_helper | production_write_possible only as candidate boundary | no_persistence | Later-stage candidate; out of scope. |
| `controlled_evidenceitem_evidence_layer_write_runtime` helper | backend_helper/runtime_helper | Evidence Layer write possible in controlled path | local controlled test path only | Too far downstream; hard blocker for 8Y-6. |
| `evidence.py` schema | backend_schema | production EvidenceItem schema | unknown unless called | Must not be used for production object creation in 8Y-6. |
| `evidence_import.py` service | backend_service | import/runtime possible | unknown unless called | Must not be called by 8Y-6. |
| `evidence_ingestion.py` service | backend_service | ingestion/runtime possible | unknown unless called | Must not be called by 8Y-6. |
| existing Evidence Layer import docs | docs_only | governance contract | no_persistence | Useful background only; does not approve runtime. |

## Gate Interpretation

8Y-5 is an Evidence Layer import gate, not import execution.

The gate finding is blocked because the audited safe helper chain does not provide a direct, already-governed transformation from 8Y-4 row preview to Evidence Layer import candidate.

The historical chain is:

`row preview -> evidence candidate -> review queue candidate -> Evidence Layer import candidate`

8Y-5 does not decide whether future Route C should reuse that multi-step chain or define a new direct redacted-row-preview-to-import-candidate adapter. That choice requires another docs-only source-path decision before implementation.

## Future 8Y-6 Source Requirements If Reopened

Future 8Y-6 may only use:

- the 8Y-4 redacted review-only row preview output, or
- an equivalent safe summary that preserves the same redaction, row bound, warning/manual-review, and no-side-effect flags.

Future 8Y-6 must not use:

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

## Future 8Y-6 Action Constraints If Reopened

Future 8Y-6 may be considered only as:

- backend-only
- test-first
- controlled smoke only
- local controlled import candidate object only
- review-only
- candidate-only
- human-review-required
- warning-preserving
- selected-sample-only
- no automatic trust upgrade

It must not:

- write Evidence Layer
- create production EvidenceItem
- create production case
- create production `analysis_run`
- create Review Queue runtime
- add route/API/frontend behavior
- call Source 11 runtime
- create actual FinalSummaryReport runtime output
- generate B-end report runtime
- generate Sandbox/public event runtime
- generate export/download/public/final-delivery runtime
- generate response text
- call real APIs or real LLMs
- run provider or collector jobs
- fetch URLs
- scrape pages

## Future 8Y-6 Inactive Approval Phrase

Future 8Y-6 exact approval phrase:

`APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE`

This phrase is inactive in 8Y-5. It is only a future placeholder.

It does not authorize implementation in 8Y-5, Evidence Layer import, import candidate creation, EvidenceItem-shaped candidate creation, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, actual FinalSummaryReport runtime output, generated response text, route/API/frontend behavior, B-end/Sandbox/export/public-delivery runtime, real API/LLM calls, provider/collector jobs, URL fetching, or scraping.

## Minimum Future Output Contract If Reopened

Future 8Y-6 output must preserve:

- import_candidate_created may be true only inside controlled backend test path
- import_candidate_mode = review_only_local_evidence_layer_import_candidate or safe equivalent
- evidence_item_shaped_candidate_created may be true only as local controlled candidate object
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
- raw_rows_exposed = false
- raw_comments_exposed = false
- raw_identities_exposed = false
- author_names_or_profile_urls_exposed = false
- secrets_read = false
- human_review_required = true
- no_automatic_trust_upgrade = true

## Hard Blockers

Future 8Y-6 must stop if any of these are required:

- no safe existing import candidate surface found
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
- author names or profile URLs as actual values
- arbitrary real exchange directory
- arbitrary package directory
- private collector source inspection
- collector job execution
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claims
- implementation path that bypasses the unresolved source-path decision

## Relationship to Later Route C Gates

If later reopened and separately approved, 8Y-6 can only create a local controlled import candidate.

It cannot authorize:

- production case gate
- production case candidate smoke
- production `analysis_run` gate
- production `analysis_run` candidate smoke
- Source 11 runtime
- actual FinalSummaryReport runtime
- report generation
- Sandbox/public event generation
- export/download/public/final delivery

Those remain separate future gates.

## Validation Contract

Validation for 8Y-5 is docs-only:

- `git diff --check`
- whitespace scan for the two 8Y-5 docs
- open-marker/mojibake scan
- future approval phrase inactive scan
- backend/frontend/tests/runtime/Project Source scope scan
- forbidden positive-claim scan with matches accepted only when they are explicit no/false/boundary language

Do not run pytest, frontend build, browser smoke, collector jobs, real API/LLM/network calls, URL fetching, scraping, row parsing, or exchange-directory reads for 8Y-5.

## Source Sync Contract

Do not update Source 11 for 8Y-5.

Do not create Source files or `docs/project_sources/` files inside the repo.

Source updates are not recommended after this commit unless the user separately wants a ChatGPT-side summary patch.
