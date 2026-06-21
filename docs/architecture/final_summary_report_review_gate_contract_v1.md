# Final Summary Report Review Gate Contract v1

## Purpose

This contract defines the future `sentigraph_final_summary_report_review_gate_v1` object.

The object records a human review decision for a local `SummaryReportCandidate`. It is not a final Summary Report, B-end report, export package, Sandbox fixture, public event page, production case, Evidence Layer write, official verification, or full-web analysis.

## Future Object

```json
{
  "schema": "sentigraph_final_summary_report_review_gate_v1",
  "final_report_review_gate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "summary_report_candidate_id": "...",
  "report_gate_id": "...",
  "result_candidate_id": "...",
  "manual_analysis_execution_id": "...",
  "boundary_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "ready_for_future_final_summary_report_runtime|needs_revision|blocked|privacy_hold",
  "review_decision": "approve_for_future_final_runtime|request_revision|block|privacy_hold",
  "required_final_report_sections": {
    "executive_summary": true,
    "evidence_scope": true,
    "analysis_summary": true,
    "risk_and_topic": true,
    "representative_evidence": true,
    "boundary_block": true,
    "limitations": true,
    "warnings": true,
    "audit_trace": true
  },
  "input_boundary": {
    "source": "summary_report_candidate",
    "read_original_package_rows_now": false,
    "call_llm_now": false,
    "call_external_api_now": false,
    "write_evidence_layer_now": false,
    "create_production_case_now": false
  },
  "downstream_readiness": {
    "can_run_future_final_summary_report_runtime": true,
    "can_export_now": false,
    "can_generate_b_end_report_now": false,
    "can_generate_sandbox_now": false,
    "can_generate_public_event_now": false,
    "requires_export_gate": true,
    "requires_b_end_report_gate": true,
    "requires_sandbox_gate": true,
    "requires_public_event_gate": true
  },
  "blocked_reasons": [],
  "required_revisions": [],
  "warnings": [],
  "boundary_notes": [],
  "audit_refs": {}
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_final_summary_report_review_gate_v1`.

### `final_report_review_gate_id`

Unique local identifier for the review gate. It must not be treated as a final report id, export id, B-end report id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The gate does not create a production case.

### `summary_report_candidate_id`

The local candidate being reviewed. This is the only allowed report content source for the gate.

### `report_gate_id`

The prior `ReportGenerationGate` id. The gate must be ready and must have audit evidence.

### `result_candidate_id`

The upstream `ManualAnalysisResultCandidate` id referenced through the summary candidate.

### `manual_analysis_execution_id`

The upstream `ManualAnalysisExecution` id. Its audit trace must remain available.

### `boundary_gate_id`

The upstream `AnalysisResultBoundaryGate` id. Boundary warnings and exclusions must remain intact.

### `created_at`

UTC timestamp for local review gate creation.

### `created_by`

Reviewer label or local UI label. It must not include secrets, cookie values, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, raw author identifiers, profile URLs, or private account identifiers.

### `status`

One of:

- `ready_for_future_final_summary_report_runtime`
- `needs_revision`
- `blocked`
- `privacy_hold`

Readiness means only future final runtime eligibility. It does not mean final report generation or downstream artifact readiness.

### `review_decision`

One of:

- `approve_for_future_final_runtime`
- `request_revision`
- `block`
- `privacy_hold`

The decision records human review only. It must not mutate the candidate automatically.

### `required_final_report_sections`

Required candidate sections that must be present before a future final summary runtime can be considered.

### `input_boundary`

Machine-readable input-safety block. All immediate side-effect fields must remain false.

### `downstream_readiness`

Future readiness flags and downstream gate requirements. Export, B-end report, Sandbox, and public event outputs require separate gates.

### `blocked_reasons`

Reasons the candidate cannot proceed to future final summary runtime.

### `required_revisions`

Human-readable revisions needed before another review attempt.

### `warnings`

Warnings that must remain visible to future final report runtime and downstream gates.

### `boundary_notes`

Required boundary copy, including coverage limitation, rejected-evidence exclusion, weak-evidence warnings, duplicate non-amplification, provider-output caveat, and no-official-verification caveat.

### `audit_refs`

References to prior append-only audits:

- summary report candidate audit
- report generation gate audit
- manual analysis execution audit
- analysis result boundary gate audit

## Required Invariants

- The source is `SummaryReportCandidate` only.
- The candidate remains non-final until future final runtime.
- Original package rows are not read.
- `evidence_items.jsonl` and `evidence_items.csv` are not parsed.
- URLs are not fetched.
- Providers and collectors are not called.
- Real LLMs are not called.
- Evidence Layer is not written.
- Production case is not created.
- Trust and verification are not upgraded.
- Warnings are not removed.
- Rejected evidence remains excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- No official verification or full-web/full-platform/full-thread claim is introduced.

## Suggested Audit Companion

A future runtime should also append a separate audit object, for example `sentigraph_final_summary_report_review_gate_audit_v1`, recording:

- previous status if any
- new status
- review decision
- reviewer label
- note
- required revisions
- blocked reasons
- analysis effect
- downstream side-effect flags, all false
- safe-mode flags, including no export, no B-end report, no Sandbox, no public event, no Evidence Layer write, no production case, no URL fetch, no real API, and no real LLM

