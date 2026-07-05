# Sentigraph Real Data Chain Pre-Evidence Layer Governance Contract v0.1

## Purpose

This contract defines the Route C governance boundary for real data chain work before any Evidence Layer import, production case creation, or production analysis_run creation.

It is docs-only and planning-only. It does not implement row preview, parse evidence rows, read real exchange directories, write Evidence Layer, create production objects, call Source 11 runtime, create actual FinalSummaryReport runtime output, generate B-end/Sandbox/export/public delivery, call real APIs/LLMs, fetch URLs, or scrape.

## Status Fields

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

## External Provider Boundary

The external/private collector is an external provider and local package producer. Sentigraph remains a safe metadata consumer and governance system.

The Route C boundary requires:

- no live crawler role for Sentigraph
- no private collector source inspection
- no collector job execution
- no default HTTP/API bridge to collector
- no real exchange directory read unless explicitly gated later
- no real package row read unless explicitly gated later
- no raw comment or raw identity exposure
- no automatic trust upgrade from package metadata

Already-exported package metadata may be considered as a governance input. It is not official truth and does not create production evidence by itself.

## Route C Sequence Contract

```text
C0 / 8Y-2:
  docs-only Route C governance decision

C1 / 8Y-3:
  review-only row preview existing-surface audit and gate decision docs-only

C2:
  future controlled redacted row preview smoke only with separate exact approval

C3:
  Evidence Layer import gate docs-only

C4:
  future controlled Evidence Layer import candidate smoke only with separate exact approval

C5:
  production case gate docs-only

C6:
  future controlled production case candidate smoke only with separate exact approval

C7:
  production analysis_run gate docs-only

C8:
  future controlled production analysis_run candidate smoke only with separate exact approval

B route:
  actual Source 11 / actual FinalSummaryReport runtime deferred
```

Each step changes governance risk. Each later runtime smoke must have a separate docs-only gate and exact approval phrase before it can be discussed as implementation.

## Future 8Y-3 Contract

Future 8Y-3 is inactive in 8Y-2.

Future exact phrase:

`APPROVE_8Y_3_REVIEW_ONLY_ROW_PREVIEW_EXISTING_SURFACE_AUDIT_AND_GATE_DECISION_DOCS_ONLY`

This phrase is an inactive future gate marker. It does not authorize row parsing, real exchange directory read, Evidence Layer write, production case creation, production analysis_run creation, route/frontend/runtime implementation, Source 11 runtime, actual FinalSummaryReport runtime, real API/LLM/network behavior, URL fetching, scraping, or collector execution.

Future 8Y-3 may only:

- inspect repository docs
- inspect existing code surfaces if needed
- identify existing review-only row preview surfaces
- identify import governance surfaces
- define whether a later controlled redacted row preview smoke can be proposed
- define safe input, blockers, output constraints, and validation expectations

## Why No Direct Evidence Layer Write

Route C cannot jump directly to Evidence Layer write because:

- row preview is the first privacy boundary
- import is a persistence boundary
- production case creation is a product-state boundary
- production analysis_run creation is an interpretation boundary
- package validation is not official truth
- provider metadata is evidence input, not proof
- review-only material must not become production material automatically
- human review and explicit gates are required between each step

## Route D Contract

Route D remains parallel and supporting:

- docs
- demo material
- playtest material
- website material
- business material
- POC material

Route D must not claim production data integration and must not replace Route C unless explicitly selected.

## Route B Contract

Route B remains deferred. Actual Source 11 runtime and actual FinalSummaryReport runtime require a future fresh docs-only gate after Route C governance is clearer.

8Y-2 selects no B implementation.

## Hard Blockers

Block any future Route C task that requests:

- raw row exposure
- raw comment dump
- raw author identity exposure
- profile URL exposure as actual values
- private collector source inspection
- collector job execution
- reading real exchange directory without explicit gate
- reading real package rows without explicit gate
- Evidence Layer write
- production EvidenceItem
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

## Validation Expectations for Future 8Y-3

Future 8Y-3 should remain docs-only. Validation should be limited to:

- `git diff --check`
- whitespace scan for changed docs
- open-item marker and mojibake scan
- future approval phrase inactive scan
- scope scan proving no backend/frontend/tests/runtime/Project Source changes
- forbidden positive-claim scan

It should not run pytest, frontend build, browser smoke, collector, API/LLM/network, URL fetching, or scraping unless a future prompt explicitly changes scope.

## Source Sync Contract

Source updates are not recommended after 8Y-2 unless Source 00 / Source 15 / Source 25 are found insufficient. Source 11 update is not recommended unless existing Analysis Request, Provider, Import Governance, or Source 11 runtime behavior changes.

Codex must not create Project Source files inside this repository for 8Y-2.

## Recommended Tag

recommended_tag: no
