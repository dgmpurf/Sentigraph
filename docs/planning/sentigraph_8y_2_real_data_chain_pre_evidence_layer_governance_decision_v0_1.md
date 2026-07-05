# Sentigraph 8Y-2 Real Data Chain Pre-Evidence Layer Governance Decision v0.1

## Decision

- phase: 8Y-2
- decision: ready
- privacy_issue_stop: no
- docs_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- row_preview_implemented: no
- evidence_rows_parsed: no
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
- selected_route_now: C_real_data_chain_pre_evidence_layer_governance
- selected_next_boundary_option: ready_for_8Y_3_review_only_row_preview_existing_surface_audit_and_gate_decision_docs_only
- future_8y3_exact_approval_phrase_required: yes
- future_8y3_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Current Post-8Y-1 Route Order

8Y-1 completed the route reset:

- A completed as pause / route reset.
- C is selected as the preferred next backend mainline.
- D remains a support and parallel line.
- B remains deferred.

8V is stage-complete as a local backend metadata and governance boundary chain.

8W-1 through 8W-69 are complete. The production Analysis Result creation go/no-go authorization chain remains paused and must not continue into 8W-70 from this decision.

8X-1 through 8X-17 are complete. The 8X backend handoff chain is stage-complete only as a local controlled backend handoff chain and remains paused before actual Source 11 or FinalSummaryReport runtime.

## Route C Architecture

Route C is the real data chain / Evidence Layer / production case / analysis_run pre-governance path.

In Route C:

- external/private collector remains an external provider and local package producer
- Sentigraph remains a safe metadata consumer and governance system
- Sentigraph must not become a live crawler
- Sentigraph must not inspect private collector source
- Sentigraph must not run collector jobs
- Sentigraph must not use an HTTP/API bridge to collector by default
- Sentigraph must only consider already-exported package metadata and future explicitly approved redacted review paths

Provider metadata and package validation are evidence governance inputs, not official truth. Review-only material must not become production material automatically.

## Route C Staged Sequence

### C0 / 8Y-2

Docs-only Route C governance decision. This phase defines the sequence and selects the next docs-only boundary. It does not implement row preview, Evidence Layer import, production case creation, or analysis_run creation.

### C1 / 8Y-3

Review-only row preview existing-surface audit and gate decision, docs-only.

This future phase may inspect repo docs and existing code surfaces if needed, but must not modify code. It should identify existing review-only row preview or import governance surfaces and decide whether a later controlled redacted row preview smoke may be considered.

### C2

Future controlled redacted row preview smoke only if separately approved by an exact phrase. This is not authorized by 8Y-2.

### C3

Evidence Layer import gate, docs-only.

### C4

Future controlled Evidence Layer import candidate smoke only if separately approved. This is not authorized by 8Y-2.

### C5

Production case gate, docs-only.

### C6

Future controlled production case candidate smoke only if separately approved. This is not authorized by 8Y-2.

### C7

Production analysis_run gate, docs-only.

### C8

Future controlled production analysis_run candidate smoke only if separately approved. This is not authorized by 8Y-2.

### B Route

Actual Source 11 runtime and actual FinalSummaryReport runtime remain deferred until Route C governance is clearer.

## Why Route C Must Not Jump Directly to Evidence Layer Write

Route C must not jump directly to Evidence Layer write because:

- row preview changes privacy and exposure risk
- import changes persistence and governance risk
- production case creation changes product-state risk
- analysis_run creation changes interpretation and downstream-reporting risk
- each step needs its own docs-only gate and exact approval phrase
- package validation or provider metadata is not official truth
- review-only material must not become production material automatically

## Immediate Next Boundary

The selected next boundary option is:

ready_for_8Y_3_review_only_row_preview_existing_surface_audit_and_gate_decision_docs_only

## Future 8Y-3 Placeholder

Future 8Y-3 is inactive in this decision.

Future 8Y-3 exact phrase:

`APPROVE_8Y_3_REVIEW_ONLY_ROW_PREVIEW_EXISTING_SURFACE_AUDIT_AND_GATE_DECISION_DOCS_ONLY`

This phrase is inactive in 8Y-2. It does not authorize row parsing, real exchange directory read, Evidence Layer write, production case creation, production analysis_run creation, route/frontend/runtime implementation, Source 11 runtime, or actual FinalSummaryReport runtime.

## Future 8Y-3 Allowed Scope

Future 8Y-3 may be only a docs-only audit and gate decision.

It may:

- inspect repo docs and existing code surfaces if needed
- identify existing review-only row preview surfaces
- identify existing import governance surfaces
- decide whether a future 8Y-4 may perform a controlled redacted row preview smoke
- define safe input, blockers, output constraints, and validation expectations

It must not:

- modify backend code
- modify tests
- modify routes/API
- modify frontend
- create runtime files
- parse rows
- read real exchange directories
- write Evidence Layer
- create production case
- create production analysis_run

## Future Row-preview-related Blockers

Block any future row-preview-related task that requests:

- raw row exposure
- raw comment dump
- raw author identity exposure
- profile URL exposure as actual values
- private collector source inspection
- collector job execution
- reading real exchange directory without explicit gate
- reading real package rows without explicit gate
- Evidence Layer write
- production case
- production analysis_run
- Review Queue runtime
- generated response text
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- real API/LLM/network/fetch/scrape
- automatic trust upgrade
- customer/public/production readiness claims

## Route D Handling

Route D can proceed in parallel only as docs, material, demo, playtest, website, business, or POC support.

Route D must not claim production data integration and must not override Route C as the backend mainline unless explicitly selected.

## Route B Handling

Route B remains deferred.

Actual Source 11 runtime and actual FinalSummaryReport runtime require a fresh docs-only gate after Route C governance is clearer. No B implementation is selected by 8Y-2.

## Source Recommendation

source_update_recommended_after_commit: no

Source 00 / Source 15 / Source 25 are already sufficient for the current 8Y-1 route-order state unless the user later decides they need an additional summary. Source 11 update is not recommended unless existing Analysis Request, Provider, Import Governance, or Source 11 runtime behavior changes.

Codex must not create Project Source files inside this repository for 8Y-2.

## Tag Recommendation

recommended_tag: no
