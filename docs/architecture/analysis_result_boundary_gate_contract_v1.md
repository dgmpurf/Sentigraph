# Analysis Result Boundary Gate Contract v1

## Purpose

This contract defines the future Analysis Result Boundary Gate object shape.

The object is a governance boundary result. It is not an Analysis Result, report, Sandbox output, public event page, production Evidence Layer write, production case, or official verification.

## Future Object

```json
{
  "schema": "sentigraph_analysis_result_boundary_gate_v1",
  "boundary_gate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "manual_trigger_id": "...",
  "promotion_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "boundary_ready_for_future_analysis_result_runtime|incomplete|blocked|privacy_hold",
  "analysis_input_boundary": {
    "source": "review_only_promoted_candidates",
    "provider_output_is_truth": false,
    "official_verification": false,
    "full_web_coverage": false,
    "analysis_includes_rejected": false,
    "duplicates_amplify_risk": false
  },
  "required_boundary_sections": {
    "coverage_limitation": true,
    "weak_evidence_warning": true,
    "rejected_evidence_exclusion_note": true,
    "dedup_warning": true,
    "provider_output_evidence_not_truth_note": true,
    "not_official_verification_note": true,
    "not_full_web_coverage_note": true,
    "audit_trace_note": true
  },
  "counts": {
    "included_item_count": 0,
    "excluded_rejected_count": 0,
    "weak_warning_count": 0,
    "duplicate_group_count": 0,
    "privacy_excluded_count": 0,
    "needs_more_source_excluded_count": 0
  },
  "now_flags": {
    "write_evidence_layer_now": false,
    "create_production_case_now": false,
    "run_analysis_now": false,
    "generate_analysis_result_now": false,
    "generate_report_now": false,
    "generate_sandbox_now": false,
    "generate_public_event_now": false
  },
  "readiness": {
    "can_present_analysis_result_now": false,
    "requires_future_analysis_execution": true,
    "requires_boundary_runtime": true,
    "requires_report_gate": true,
    "requires_sandbox_gate": true
  },
  "blocked_reasons": [],
  "warnings": [],
  "boundary_notes": [],
  "recommended_next_steps": []
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_analysis_result_boundary_gate_v1`.

### `boundary_gate_id`

Unique local identifier for the boundary gate evaluation. It must not be treated as an analysis id, report id, production case id, or Evidence Layer write id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The source case remains review-only unless a separate future production promotion gate explicitly changes that.

### `manual_trigger_id`

Manual Analysis Trigger id. The trigger must have an audit record and must allow future analysis runtime.

### `promotion_gate_id`

Analysis-ready Promotion Gate id. The promotion gate must have been eligible before any future manual analysis trigger.

### `created_at`

UTC timestamp for the gate evaluation.

### `created_by`

Local operator or UI label. It must not contain secrets, cookies, tokens, API key values, browser session identifiers, email addresses, phone numbers, or private account identifiers.

### `status`

One of:

- `boundary_ready_for_future_analysis_result_runtime`
- `incomplete`
- `blocked`
- `privacy_hold`

Readiness only means a future boundary runtime can evaluate or prepare a result boundary. It does not present or store an Analysis Result.

### `analysis_input_boundary`

Defines the conservative input boundary for future result handling.

`source` must be `review_only_promoted_candidates`.

`provider_output_is_truth` must be false because provider output remains evidence, not truth.

`official_verification` must be false unless a separate future official verification gate proves otherwise.

`full_web_coverage` must be false because the source is a reviewed evidence scope, not full-web or full-platform coverage.

`analysis_includes_rejected` must be false.

`duplicates_amplify_risk` must be false.

### `required_boundary_sections`

Defines sections that future Analysis Result UI, API response, and downstream metadata must include.

`coverage_limitation` requires a visible note that analysis uses available reviewed evidence only.

`weak_evidence_warning` requires warning text for weak or low-trust evidence.

`rejected_evidence_exclusion_note` requires a note that rejected evidence was excluded.

`dedup_warning` requires a note that duplicate evidence was governed and must not amplify risk.

`provider_output_evidence_not_truth_note` requires a note that provider output is evidence, not truth.

`not_official_verification_note` requires a no-official-verification statement.

`not_full_web_coverage_note` requires a no-full-web/full-platform statement.

`audit_trace_note` requires a link or metadata reference to prior trigger, promotion, review, and dedup audits.

### `counts`

Governance counts used for boundary disclosure.

`included_item_count` counts included representative items or eligible item candidates.

`excluded_rejected_count` counts rejected items or groups excluded from future result metrics.

`weak_warning_count` counts weak items or groups that require warnings.

`duplicate_group_count` counts duplicate groups handled as representatives for primary metrics.

`privacy_excluded_count` counts privacy-held or privacy-excluded items.

`needs_more_source_excluded_count` counts items or groups excluded because more source material is required.

Counts are boundary metadata only. They must not silently update risk, sentiment, coverage, or reports.

### `now_flags`

All values must remain false in this design phase.

`write_evidence_layer_now` forbids Evidence Layer writes.

`create_production_case_now` forbids production case creation.

`run_analysis_now` forbids analysis execution by this gate.

`generate_analysis_result_now` forbids result generation by this gate.

`generate_report_now` forbids report generation.

`generate_sandbox_now` forbids Sandbox generation.

`generate_public_event_now` forbids public event generation.

### `readiness`

`can_present_analysis_result_now` must be false in this design phase.

`requires_future_analysis_execution` must be true because this gate design does not run analysis.

`requires_boundary_runtime` must be true because a later runtime is required.

`requires_report_gate` must be true because reports need a separate gate.

`requires_sandbox_gate` must be true because Sandbox output needs a separate gate.

### `blocked_reasons`

Machine-readable blockers such as `missing_manual_trigger_audit`, `privacy_hold`, `needs_more_source`, `rejected_evidence_leakage`, `duplicate_amplification_risk`, `missing_coverage_limitation`, `missing_audit_trace`, or `overclaim_detected`.

### `warnings`

Warnings that must be visible to future result consumers, such as weak evidence, selected sample limitation, dedup limitation, rejected exclusion, provider evidence-not-truth, and no official verification.

### `boundary_notes`

Human-readable safety notes that should travel with the future result boundary response.

### `recommended_next_steps`

Safe next actions such as resolve blockers, complete audit trace, add missing boundary sections, or proceed to future 7F runtime design.

## Required Invariants

- No `now_flags` value may be true.
- Rejected items and groups must not be included.
- Privacy-held items and groups must not be included.
- Needs-more-source items and groups must not be included.
- Duplicate groups must not amplify risk, sentiment, coverage, or conclusions.
- Weak items and groups must remain warning-marked.
- Provider output must remain evidence, not truth.
- Trust labels must not be upgraded.
- Verification status must not be upgraded.
- No raw author identifiers, private content, or secret-like values may be displayed.
