# Sentigraph 8Y-5 Evidence Layer Import Gate Decision v0.1

## Decision

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
- future_8y6_exact_approval_phrase_required: yes, if this gate is later reopened
- future_8y6_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Approval Phrase Received for 8Y-5

The exact user approval phrase for this docs-only decision was received:

`APPROVE_8Y_5_EVIDENCE_LAYER_IMPORT_GATE_DECISION_DOCS_ONLY`

This phrase authorizes only this 8Y-5 docs-only gate decision. It does not authorize Evidence Layer import implementation, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, actual FinalSummaryReport runtime, route/API/frontend work, or export/download/public delivery behavior.

## Route C State

Route C is the selected backend mainline for real data chain / Evidence Layer / production case / production `analysis_run` pre-governance.

Current Route C checkpoints:

- 8Y-1 selected Route C as the preferred backend mainline while Route B remains deferred.
- 8Y-2 defined the Route C staged sequence.
- 8Y-3 audited review-only row preview surfaces and found the 8W-7 approval phrase blocker.
- 8Y-3A repaired the 8W-7 row-preview approval phrase to ASCII.
- 8Y-3B re-evaluated the blocker and selected 8Y-4 as a future controlled row-preview smoke.
- 8Y-4 completed a backend-only controlled redacted review-only row preview smoke.
- 8Y-5 is C3: Evidence Layer import gate docs-only.
- C4 / future 8Y-6 is not active.
- Route B / actual Source 11 and actual FinalSummaryReport runtime remains deferred.

## Interpretation of 8Y-4 Output

8Y-4 output is a safe input candidate for future import-governance discussion only.

It is:

- a redacted review-only row preview
- bounded to the approved controlled row source and row limit
- derived from `evidence_items.jsonl` only in the approved controlled backend test path
- human-review-required
- warning-preserving
- no automatic trust upgrade
- not production evidence
- not official truth
- not Evidence Layer record
- not production EvidenceItem
- not production case input unless separately gated
- not production `analysis_run` input unless separately gated
- not Source 11 input
- not actual FinalSummaryReport runtime input
- not B-end report, Sandbox/public event, export/download/public-delivery input

8Y-4 proved:

- row_preview_created: yes
- approved_row_source: `evidence_items.jsonl`
- evidence_items_jsonl_opened: yes only in approved controlled path
- evidence_items_jsonl_parsed: yes only in approved controlled path
- evidence_items_csv_opened: no
- evidence_items_csv_parsed: no
- source_manifest_rows_parsed: no
- collection_log_rows_parsed: no
- original_package_rows_read: no
- raw_rows_exposed: no
- raw_comments_exposed: no
- raw_identities_exposed: no
- Evidence Layer write: no
- production EvidenceItem: no
- production case: no
- production `analysis_run`: no
- Review Queue runtime: no
- Source 11 runtime: no
- actual FinalSummaryReport runtime: no

## Import Surface Audit Summary

8Y-5 inspected existing repo surfaces only at code/docs reference level. It did not execute helper logic, parse rows, read exchange directories, inspect private collector source, or create any candidate/import objects.

| Surface | Classification | Relation to Evidence Layer | Side effects | 8Y-5 interpretation |
| --- | --- | --- | --- | --- |
| `backend/app/services/controlled_row_preview.py` | backend_helper | no_import | reads only approved row source in controlled path | Safe source preview helper already used by 8Y-4; not an import helper. |
| `backend/app/tests/test_8y_4_controlled_redacted_review_only_row_preview_smoke.py` | test_only | no_import | approved controlled row preview only | Proves 8Y-4 preview envelope; not an import candidate. |
| `docs/health/sentigraph_8y_4_controlled_redacted_review_only_row_preview_smoke_report_v0_1.md` | docs_only | no_import | no_persistence | Records 8Y-4 boundaries and validation. |
| `backend/app/services/controlled_evidence_candidate.py` | backend_helper | import_candidate_only, not Evidence Layer import | no_persistence | Consumes controlled row preview into local evidence-candidate-shaped objects; still not Evidence Layer import. |
| `backend/app/services/controlled_review_queue_candidate.py` | backend_helper | review_only_candidate | no_persistence | Consumes evidence candidate set into local review-queue-candidate-shaped objects; not Review Queue runtime. |
| `backend/app/services/controlled_evidence_layer_import_candidate.py` | backend_helper | import_candidate_only | no_persistence | Existing 8W-16 helper expects a review queue candidate set, not direct 8Y-4 row preview output. |
| `backend/app/services/controlled_evidence_layer_write_candidate.py` | backend_helper | evidence_layer_write_possible only as future candidate boundary | no_persistence | Downstream candidate surface; not appropriate for 8Y-6. |
| `backend/app/services/controlled_production_evidence_import_candidate.py` | backend_helper | production_write_possible only as future candidate boundary | no_persistence | Later-stage surface; out of scope for 8Y-6. |
| `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py` | backend_helper/runtime_helper | evidence_layer_write_possible | local controlled test path only | Later write-runtime surface; hard blocker for 8Y-6. |
| `backend/app/schemas/evidence.py` | backend schema | production EvidenceItem schema | unknown unless called | Must not be used by 8Y-6 except as a field-reference boundary, if separately approved. |
| `backend/app/services/evidence_import.py` | backend service | production/import behavior possible | unknown unless called | Out of scope for 8Y-6; do not call. |
| `backend/app/services/evidence_ingestion.py` | backend service | ingestion behavior possible | unknown unless called | Out of scope for 8Y-6; do not call. |
| `docs/architecture/sentigraph_evidence_layer_import_gate_contract_v0_1.md` | docs_only | import gate contract | no_persistence | Updated by 8Y-5 to record the current Route C gate. |
| `docs/architecture/sentigraph_row_preview_to_evidence_candidate_gate_contract_v0_1.md` | docs_only | import_candidate_only | no_persistence | Relevant earlier candidate-boundary contract. |
| `docs/architecture/sentigraph_evidence_candidate_to_review_queue_gate_contract_v0_1.md` | docs_only | review_only_candidate | no_persistence | Relevant intermediate gate contract. |
| `docs/architecture/sentigraph_review_queue_candidate_to_evidence_layer_import_gate_contract_v0_1.md` | docs_only | import_candidate_only | no_persistence | Shows the historical 8W route required review queue candidate as source. |
| `docs/architecture/evidence_import_preview_contract_v1.md` | docs_only | review/import planning | no_persistence | Background import-governance material only. |
| `docs/architecture/review_only_case_staging_import_contract_v1.md` | docs_only | review-only staging | no_persistence | Background only; not 8Y-6 source. |

## Gate Finding

8Y-5 does not find enough direct safe surface to justify activating 8Y-6 immediately.

Reasons:

- The existing Evidence Layer import candidate helper expects `sentigraph_controlled_review_queue_candidate_set_v0_1`, not the 8Y-4 `sentigraph_controlled_row_preview_v0_1` output directly.
- The safe historical chain is row preview to evidence candidate to review queue candidate to Evidence Layer import candidate, and each transition has its own gate.
- Future 8Y-6 as named by this Route C task would need either a new direct redacted-row-preview-to-import-candidate adapter or an explicitly approved staged reuse of intermediate candidate helpers.
- 8Y-5 must not approve implementation, helper expansion, direct adapter creation, row parsing, candidate creation, or Evidence Layer write.
- Existing production/import/write/runtime surfaces are intentionally too far downstream for this gate.

Selected option:

`pause_or_blocked_before_controlled_evidence_layer_import_candidate_smoke`

This is a governance pause, not a privacy stop.

## Evidence Layer Import Gate Interpretation

8Y-5 may only allow a future import candidate discussion after a separate gate reopens the source path.

Future candidate work, if later approved, may only transform a redacted review-only preview or safe equivalent into local controlled candidate objects. It must not:

- write Evidence Layer
- create production EvidenceItem
- create production case
- create production `analysis_run`
- create Review Queue runtime
- create Source 11 runtime
- create actual FinalSummaryReport runtime output
- create B-end report, Sandbox/public event, export/download/public-delivery runtime
- expose raw rows, raw comments, raw identities, author names, profile URLs, secrets, cookies, sessions, tokens, private paths, or private collector material

## Allowed Future 8Y-6 Input, If Gate Is Reopened

Future 8Y-6 may use only:

- the 8Y-4 redacted review-only row preview output or an equivalent safe summary
- preview schema `sentigraph_controlled_row_preview_v0_1` or an existing safe equivalent
- preview mode `review_only_redacted_preview` or equivalent
- bounded rows
- redacted snippets only
- `raw_rows_exposed = false`
- `raw_comments_exposed = false`
- `raw_identities_exposed = false`
- `author_names_or_profile_urls_exposed = false`
- `evidence_layer_write = false`
- `production_evidence_item_created = false`
- `production_case_created = false`
- `production_analysis_run_created = false`
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

It must not read arbitrary real exchange directories, arbitrary package directories, source manifests, collection logs, CSV rows, original package rows, private collector source, private collector raw output, URLs, or external services.

## Allowed Future 8Y-6 Action, If Separately Approved

Future 8Y-6 may be considered only as:

- backend-only
- test-first
- controlled smoke only
- local controlled import candidate object only
- EvidenceItem-shaped candidate object only as a local controlled test-path object, if the future contract explicitly allows it
- review-only / candidate-only
- warning-preserving
- human-review-required
- no automatic trust upgrade

It must remain:

- no Evidence Layer write
- no production EvidenceItem creation
- no production case
- no production `analysis_run`
- no Review Queue runtime
- no route/API/frontend
- no Source 11 runtime
- no actual FinalSummaryReport runtime
- no B-end/Sandbox/export/public delivery
- no real API, real LLM, provider job, collector job, URL fetch, or scraping

## Future 8Y-6 Inactive Approval Phrase

Future 8Y-6 exact approval phrase, if a later gate reopens it:

`APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE`

future_8y6_exact_approval_phrase_active: no

This phrase is inactive in 8Y-5. It must not be interpreted as authorization to implement 8Y-6, create an import candidate, write Evidence Layer, create production EvidenceItem, create production case, create production `analysis_run`, create Review Queue runtime, call Source 11 runtime, create actual FinalSummaryReport runtime output, or generate delivery/runtime outputs.

## Minimum Future 8Y-6 Output Constraints

If a later task explicitly approves 8Y-6, output constraints must include:

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

## Hard Blockers for Future 8Y-6

Future 8Y-6 must stop if it needs:

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
- raw row, raw comment, or identity exposure
- author names/profile URLs as actual values
- arbitrary real exchange directory
- arbitrary package directory
- private collector source inspection
- collector job execution
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claims

Additional 8Y-5-specific blocker:

- A future task must first decide whether 8Y-6 is allowed to use the existing multi-step candidate chain or must define a new direct redacted-row-preview-to-import-candidate adapter. 8Y-5 does not decide or approve that implementation shape.

## Relationship to Later Route C Steps

8Y-6, if later reopened and separately approved, can only create an import candidate.

Later Route C steps remain separate:

- C5 production case gate remains future.
- C6 controlled production case candidate smoke remains future.
- C7 production `analysis_run` gate remains future.
- C8 controlled production `analysis_run` candidate smoke remains future.
- actual Source 11 and actual FinalSummaryReport runtime remain Route B and deferred.

## Not Approved

8Y-5 does not approve:

- Evidence Layer import
- import candidate creation
- EvidenceItem-shaped candidate creation
- Evidence Layer write
- production EvidenceItem creation
- production case creation
- production `analysis_run` creation
- production Analysis Result creation authorization
- Review Queue runtime
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- route/API/frontend behavior
- generated response text
- provider or collector jobs
- private collector inspection
- real exchange directory read
- new row parsing
- real API or real LLM calls
- URL fetching or scraping

## Source Recommendation

source_update_recommended_after_commit: no

Source 11 update is not recommended because 8Y-5 changes no existing runtime behavior.

Do not create Project Source files inside this repository for 8Y-5.

## Recommended Next Task

Recommended next task:

Phase 8Y-5A or 8Y-6-preflight docs-only decision to choose the import-candidate source path:

- option 1: repair/re-evaluate the existing multi-step candidate chain before 8Y-6
- option 2: define a new direct redacted-row-preview-to-import-candidate adapter contract
- option 3: pause Route C before import candidate work

Do not implement 8Y-6 until that source-path decision is complete and a fresh exact approval phrase is provided.
