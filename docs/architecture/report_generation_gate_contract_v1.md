# Report Generation Gate Contract v1

## Purpose

This contract defines the future Report Generation Gate object shape.

The object is a governance gate result. It is not a Summary Report, B-end report, PDF export, Markdown export, briefing deck, Sandbox fixture, public event page, production Evidence Layer write, production case, or official verification.

## Future Object

```json
{
  "schema": "sentigraph_report_generation_gate_v1",
  "report_gate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "manual_analysis_execution_id": "...",
  "result_candidate_id": "...",
  "boundary_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "report_gate_ready_for_future_runtime|incomplete|blocked|privacy_hold",
  "allowed_future_outputs": {
    "summary_report_candidate": true,
    "b_end_report_candidate": false,
    "pdf_export": false,
    "markdown_export": false,
    "briefing_deck_export": false,
    "sandbox": false,
    "public_event": false
  },
  "required_report_sections": {
    "executive_summary": true,
    "evidence_scope": true,
    "boundary_block": true,
    "coverage_limitation": true,
    "weak_evidence_warning": true,
    "rejected_evidence_exclusion": true,
    "dedup_no_amplification": true,
    "provider_output_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true,
    "audit_trace": true,
    "limitations": true
  },
  "input_boundary": {
    "source": "manual_analysis_result_candidate",
    "write_evidence_layer_now": false,
    "create_production_case_now": false,
    "read_original_package_rows_now": false,
    "call_llm_now": false,
    "call_external_api_now": false
  },
  "readiness": {
    "can_generate_summary_report_candidate_in_future": true,
    "can_generate_b_end_report_now": false,
    "can_export_now": false,
    "can_generate_sandbox_now": false,
    "can_generate_public_event_now": false,
    "requires_report_runtime": true,
    "requires_export_gate": true,
    "requires_sandbox_gate": true,
    "requires_public_event_gate": true
  },
  "blocked_reasons": [],
  "warnings": [],
  "boundary_notes": [],
  "recommended_next_steps": []
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_report_generation_gate_v1`.

### `report_gate_id`

Unique local identifier for the gate evaluation. It must not be treated as a report id, export id, production case id, or Evidence Layer write id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The source remains review-only unless a separate future production promotion gate explicitly changes that.

### `manual_analysis_execution_id`

Manual Analysis Execution id. The execution must have an audit record and a result candidate.

### `result_candidate_id`

Manual Analysis Result Candidate id. The candidate is the only allowed content input for this gate.

### `boundary_gate_id`

Analysis Result Boundary Gate id. The boundary gate must exist and must not be blocked or privacy-held.

### `created_at`

UTC timestamp for the gate evaluation.

### `created_by`

Local operator or UI label. It must not contain secrets, cookie values, token values, API key values, `.env` values, browser session identifiers, password values, email addresses, phone numbers, raw author identifiers, or private account identifiers.

### `status`

One of:

- `report_gate_ready_for_future_runtime`
- `incomplete`
- `blocked`
- `privacy_hold`

Readiness only means a future report runtime may consider creating a report candidate. It does not generate a report or export.

### `allowed_future_outputs`

Defines what the gate may allow later.

`summary_report_candidate=true` means a future Summary Report Candidate runtime may be considered if all warnings and boundary sections are preserved.

`b_end_report_candidate=false`, `pdf_export=false`, `markdown_export=false`, `briefing_deck_export=false`, `sandbox=false`, and `public_event=false` mean those outputs still require separate downstream gates.

### `required_report_sections`

Defines sections that any future report candidate must include.

`executive_summary` is allowed only as a summary of bounded analysis, not as a truth claim.

`evidence_scope` must explain the reviewed evidence scope.

`boundary_block` must preserve the candidate boundary block.

`coverage_limitation` must state that the result is not full-web, full-platform, or full-thread coverage.

`weak_evidence_warning` must disclose weak or low-trust evidence.

`rejected_evidence_exclusion` must disclose that rejected evidence was excluded.

`dedup_no_amplification` must state that duplicates do not multiply risk, sentiment, or conclusions.

`provider_output_evidence_not_truth` must state that provider output is evidence, not truth.

`not_official_verification` must state that the report is not official platform verification.

`not_full_web_coverage` must repeat the coverage boundary in reader-friendly language.

`audit_trace` must reference review, dedup, promotion, analysis, and boundary audits.

`limitations` must collect remaining limitations and uncertainty.

### `input_boundary`

Defines the only allowed input and side-effect limits.

`source` must be `manual_analysis_result_candidate`.

`write_evidence_layer_now=false` forbids Evidence Layer writes.

`create_production_case_now=false` forbids production case creation.

`read_original_package_rows_now=false` forbids re-reading provider package rows, CSV files, JSONL files, or original collector output.

`call_llm_now=false` forbids real LLM calls.

`call_external_api_now=false` forbids external API calls.

### `readiness`

`can_generate_summary_report_candidate_in_future=true` means the next future runtime may create only a bounded Summary Report Candidate, not a final report export.

`can_generate_b_end_report_now=false` blocks B-end report generation.

`can_export_now=false` blocks PDF, Markdown, and deck exports.

`can_generate_sandbox_now=false` blocks Sandbox fixture generation.

`can_generate_public_event_now=false` blocks public event page generation.

`requires_report_runtime=true` means this gate is not report runtime.

`requires_export_gate=true`, `requires_sandbox_gate=true`, and `requires_public_event_gate=true` preserve downstream gate separation.

### `blocked_reasons`

Machine-readable blockers such as `missing_result_candidate`, `missing_boundary_gate`, `missing_boundary_block`, `privacy_hold`, `needs_more_source`, `rejected_evidence_leakage`, `duplicate_amplification_risk`, `missing_coverage_limitation`, `missing_weak_evidence_warning`, `missing_audit_trace`, or `overclaim_detected`.

### `warnings`

Warnings that must be visible to future report consumers, such as selected evidence scope, weak evidence, rejected exclusion, duplicate governance, provider evidence-not-truth, no official verification, no full-web coverage, and candidate-only status.

### `boundary_notes`

Human-readable safety notes that should travel with the future report candidate.

### `recommended_next_steps`

Safe next actions such as resolve blockers, complete audit trace, add missing boundary sections, or proceed to future 7I runtime design.

## Required Invariants

- No output flag may generate a final report, export, Sandbox, or public event.
- The only allowed input source is `ManualAnalysisResultCandidate`.
- Rejected evidence must remain excluded.
- Weak evidence must remain warning-marked.
- Duplicate groups must not amplify risk, sentiment, coverage, or conclusions.
- Provider output must remain evidence, not truth.
- Trust labels must not be upgraded.
- Verification status must not be upgraded.
- No raw author identifiers, private content, or secret-like values may be displayed.
