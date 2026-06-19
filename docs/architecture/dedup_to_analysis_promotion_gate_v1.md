# Dedup To Analysis Promotion Gate v1

## Purpose

This document defines the later gate required after dedup preview and dedup group review.

Dedup preview completion does not mean analysis-ready.

A separate analysis-ready promotion gate is required before review-only evidence can become analysis input.

## Promotion Requirements

Promotion requires:

- no privacy blockers
- Review Queue Completion Gate passed
- dedup preview completed
- duplicate groups reviewed or accepted
- rejected evidence excluded
- weak evidence warning-marked
- coverage limitations acknowledged
- audit timeline complete
- human promotion decision
- no production side-effect flags in prior gates
- no raw/private/secret-like field risk

Even after promotion, report, Sandbox, and public event generation need separate gates.

## What Promotion Still Does Not Mean

Promotion does not mean:

- official verification
- full-web coverage
- full-platform coverage
- causal proof
- automatic report generation
- automatic public event generation
- automatic Sandbox fixture generation
- real-world action execution

## Suggested Promotion Gate Object

```json
{
  "schema": "sentigraph_analysis_ready_promotion_gate_v1",
  "promotion_gate_id": "promotion_gate_...",
  "request_id": "req_...",
  "review_case_id": "review_only_case_...",
  "dedup_preview_id": "dedup_preview_...",
  "status": "promotion_ready|incomplete|blocked|privacy_hold",
  "human_decision_required": true,
  "analysis_included_preview": false,
  "can_run_analysis_now": false,
  "can_generate_report_now": false,
  "coverage_limitations_acknowledged": false,
  "blocked_reasons": [],
  "boundary_notes": []
}
```

The object is a future design placeholder. It must not be treated as implemented runtime.

## Future Phase Sequence

Suggested future phases:

- 6X: Dedup Preview Runtime
- 6Y: Dedup Group Review Runtime
- 6Z: Analysis-ready Promotion Gate Design
- 7A: Analysis-ready Promotion Gate Runtime
- 7B: Manual Analysis Trigger from Review-only Case

## Future Analysis Trigger Boundary

The eventual manual analysis trigger should require:

- explicit human promotion decision
- promoted safe input set
- duplicate groups resolved
- rejected evidence excluded
- weak evidence warning labels preserved
- coverage limitations carried into analysis result
- no claims of official verification
- no report/Sandbox/public event generation unless separately approved

## Boundary Wording

Use:

- analysis-ready promotion gate
- promoted safe input set
- review-only source
- duplicate group candidate
- `analysis_included=false` until promotion
- rejected evidence excluded
- weak evidence warning-marked
- coverage limitations acknowledged

Avoid:

- dedup completed means analysis-ready
- evidence verified
- report can be generated
- production case updated
- full-web coverage
- official verified
- risk score updated

