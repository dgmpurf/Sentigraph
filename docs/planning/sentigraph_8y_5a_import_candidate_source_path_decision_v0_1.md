# Sentigraph 8Y-5A Import-candidate Source Path Decision v0.1

## Decision

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

## Approval Phrase Received for 8Y-5A

The exact user approval phrase for this docs-only source-path decision was received:

`APPROVE_8Y_5A_IMPORT_CANDIDATE_SOURCE_PATH_DECISION_DOCS_ONLY`

This phrase authorizes only the 8Y-5A docs-only decision. It does not authorize source-path implementation, evidence candidate creation, Evidence Layer import candidate creation, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, actual FinalSummaryReport runtime, route/API/frontend work, provider or collector execution, or delivery runtime.

## Current Route C State

Route C is the preferred backend mainline for real data chain / Evidence Layer / production case / production `analysis_run` pre-governance.

Current state:

- 8Y-4 completed a backend-only controlled redacted review-only row preview smoke.
- 8Y-5 blocked the direct Evidence Layer import candidate path.
- 8Y-5 found that the safe existing source path is not direct row preview to Evidence Layer import candidate.
- 8Y-5A is a source-path decision only.
- Future import candidate smoke remains inactive.
- Route B / actual Source 11 and actual FinalSummaryReport runtime remains deferred.

## Interpretation of 8Y-5 Pause

8Y-5 paused because the existing safe chain is layered.

8Y-4 row preview is:

- a safe review-only preview output
- not an Evidence Layer record
- not an EvidenceItem
- not production evidence
- not production case input by default
- not production `analysis_run` input by default
- not an import candidate by default

It should not directly become an Evidence Layer import candidate without an explicit source-path decision.

## Source Path Audit Summary

8Y-5A inspected existing repo surfaces only at docs/code-reference level. It did not execute helper logic, create candidate objects, parse rows, inspect private collector source, read exchange directories, or write runtime files.

| Surface | Classification | Route C relation | Side effects | 8Y-5A interpretation |
| --- | --- | --- | --- | --- |
| `backend/app/services/controlled_row_preview.py` | backend_helper | row_preview_source | approved controlled row read only when called | Existing 8Y-4 source surface. |
| `backend/app/tests/test_8y_4_controlled_redacted_review_only_row_preview_smoke.py` | test_only | row_preview_source | controlled test path only | Proves bounded redacted preview envelope. |
| `backend/app/services/controlled_evidence_candidate.py` | backend_helper | evidence_candidate | no_persistence | Existing first source-path helper from row preview. |
| `backend/app/tests/test_controlled_evidence_candidate.py` | test_only | evidence_candidate | no_persistence | Verifies candidate creation remains local, bounded, and no Evidence Layer write. |
| `backend/app/services/controlled_review_queue_candidate.py` | backend_helper | review_queue_candidate | no_persistence | Existing second source-path helper from evidence candidate. |
| `backend/app/tests/test_controlled_review_queue_candidate.py` | test_only | review_queue_candidate | no_persistence | Verifies review queue candidate remains candidate-only, not Review Queue runtime. |
| `backend/app/services/controlled_evidence_layer_import_candidate.py` | backend_helper | import_candidate | no_persistence | Existing third source-path helper from review queue candidate. |
| `backend/app/tests/test_controlled_evidence_layer_import_candidate.py` | test_only | import_candidate | no_persistence | Verifies import candidate remains local, not Evidence Layer write. |
| `backend/app/services/controlled_evidence_layer_write_candidate.py` | backend_helper | production_import / later write candidate | no_persistence | Too far downstream for 8Y-6. |
| `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py` | backend_helper | production_import / write runtime | runtime_local_only in controlled test path | Out of scope for 8Y-6. |
| `backend/app/schemas/evidence.py` | backend_schema | production import | unknown unless called | Not a future 8Y-6 source path. |
| `backend/app/services/evidence_import.py` | backend_service | production import | unknown unless called | Not a future 8Y-6 source path. |
| `backend/app/services/evidence_ingestion.py` | backend_service | production import | unknown unless called | Not a future 8Y-6 source path. |
| `docs/planning/sentigraph_8y_5_evidence_layer_import_gate_decision_v0_1.md` | docs_only | source-path gate | no_persistence | Established the pause before source-path selection. |
| `docs/architecture/sentigraph_evidence_layer_import_gate_contract_v0_1.md` | docs_only | source-path gate | no_persistence | Established the contract need for source-path decision. |

Existing code already has:

- controlled evidence candidate helper: yes
- review-only / review queue candidate helper: yes
- Evidence Layer import candidate helper: yes
- import preview helper: docs/background surfaces exist, not selected for 8Y-6
- dry-run import helper: background governance exists, not selected for 8Y-6
- Evidence Layer write/runtime helper: exists downstream, explicitly not selected

## Option Comparison

### Option A: Multi-step helper chain

Path:

`redacted row preview -> controlled evidence candidate -> review-only / review queue candidate -> Evidence Layer import candidate`

Evaluation:

- safety: strongest, because each boundary already has a narrowed helper/test surface
- reuse: high, existing helper surfaces match the staged governance pattern
- validation burden: medium, because each step requires focused tests and exact approval
- privacy risk: lower than direct adapter, because redacted/minimized fields are checked at each step
- production-write risk: lower, because all audited helper outputs keep write and production flags false
- governance alignment: best match with existing Route C style

### Option B: Direct adapter contract

Path:

`redacted row preview -> Evidence Layer import candidate`

Evaluation:

- safety: weaker, because it skips evidence candidate and review queue candidate layers
- reuse: lower, would require a new contract and likely a new helper surface
- validation burden: high, because the adapter would need to duplicate several blocker checks
- privacy risk: higher, because fewer intermediate boundaries can catch unsafe fields
- production-write risk: higher semantic risk, because it jumps directly toward Evidence Layer import naming
- governance alignment: poor fit for the current stepwise chain

### Option C: Continue pause

Continue pause should be selected if:

- evidence candidate helper is absent or unsafe
- review queue candidate helper is absent or unsafe
- import candidate helper is absent or unsafe
- helper tests no longer prove no Evidence Layer write and no production side effects
- future work requires raw row/comment/identity exposure
- future work requires route/API/frontend/runtime, real API/LLM, private collector, or exchange directory reads

8Y-5A does not select Option C because the existing helper surfaces are sufficient to select a future source-path smoke as the next gate.

## Selected Source Path

selected_source_path:

`option_A_multi_step_helper_chain`

Rationale:

Option A preserves the project structure already visible in 8W and Route C: narrow helper, focused test, docs-only completion gate, then next boundary. It avoids jumping directly from row preview semantics into Evidence Layer import semantics.

## Adjusted Route C Micro-sequence

The adjusted micro-sequence is:

- C3a / 8Y-5A: source path decision docs-only
- C3b / future 8Y-6: controlled row-preview-to-evidence-candidate source-path smoke
- C3c / future gate: review-only / review queue candidate gate docs-only if needed
- C3d / future gate: Evidence Layer import candidate gate docs-only
- later: Evidence Layer import write gate remains separate
- later: production case gate remains separate
- later: production `analysis_run` gate remains separate

This sequence supersedes the old direct 8Y-6 import-candidate phrase from 8Y-5.

## Future 8Y-6 Approval Phrase

Future 8Y-6 exact approval phrase:

`APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE`

future_8y6_exact_approval_phrase_active: no

This phrase is inactive in 8Y-5A. It must not authorize implementation in 8Y-5A, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, actual FinalSummaryReport runtime, route/API/frontend, provider/collector jobs, real API/LLM calls, URL fetching, scraping, or delivery runtime.

## Old Direct Import Candidate Phrase Status

Earlier direct 8Y-6 phrase from 8Y-5:

`APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE`

old_direct_import_candidate_phrase_status:

`inactive_not_selected_after_source_path_decision`

This older phrase must not be treated as active approval. It does not authorize direct adapter work, import candidate creation, Evidence Layer write, production EvidenceItem creation, production case creation, production `analysis_run` creation, Review Queue runtime, Source 11 runtime, actual FinalSummaryReport runtime, or delivery runtime.

## Allowed Future 8Y-6 Scope

If separately approved, future 8Y-6 may only be:

- backend-only
- test-first
- controlled smoke only
- existing redacted row preview output as input
- existing controlled evidence candidate helper surface if safe
- local controlled evidence candidate object only
- review-only / candidate-only
- no Evidence Layer write
- no production EvidenceItem
- no production case
- no production `analysis_run`
- no Review Queue runtime
- no route/API/frontend
- no Source 11 runtime
- no actual FinalSummaryReport runtime
- no B-end/Sandbox/export/public delivery

## Future 8Y-6 Output Constraints

Future 8Y-6 output constraints:

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

## Hard Blockers for Future Source-path Smoke

Future source-path smoke must stop if it needs:

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

## Not Approved

8Y-5A does not approve:

- source-path implementation
- evidence candidate creation
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

Source 11 update is not recommended because 8Y-5A changes no existing runtime behavior.

Do not create Project Source files inside this repository for 8Y-5A.

## Recommended Next Task

Recommended next task:

Phase 8Y-6 Controlled Row Preview to Evidence Candidate Source Path Smoke.

That future task must use its own exact approval phrase and remain backend-only, test-first, local-only, controlled smoke only, and no-write/no-production/no-route/no-runtime beyond the controlled test path.
