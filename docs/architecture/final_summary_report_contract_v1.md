# Final Summary Report Contract v1

## Purpose

This contract defines the future `sentigraph_final_summary_report_v1` object.

The object is a local final Summary Report record created from a reviewed `SummaryReportCandidate` and an approved `FinalSummaryReportReviewGate`. It is not an export, B-end report, Sandbox fixture, public event page, production case, Evidence Layer write, official verification, or full-web analysis.

## Future Object

```json
{
  "schema": "sentigraph_final_summary_report_v1",
  "final_summary_report_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "summary_report_candidate_id": "...",
  "final_report_review_gate_id": "...",
  "report_gate_id": "...",
  "result_candidate_id": "...",
  "manual_analysis_execution_id": "...",
  "boundary_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "final_summary_report_created|incomplete|blocked|privacy_hold",
  "report_sections": {
    "executive_summary": {},
    "evidence_scope": {},
    "analysis_summary": {},
    "risk_and_topic": {},
    "representative_evidence": {},
    "limitations": [],
    "warnings": [],
    "boundary_block": {},
    "audit_trace": {}
  },
  "source_and_scope": {
    "source": "summary_report_candidate",
    "provider_output_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true,
    "not_full_platform_coverage": true,
    "not_full_thread_coverage": true
  },
  "downstream_flags": {
    "pdf_export_ready": false,
    "markdown_export_ready": false,
    "deck_export_ready": false,
    "b_end_report_ready": false,
    "sandbox_ready": false,
    "public_event_ready": false
  },
  "required_next_gates": {
    "export_gate": true,
    "b_end_report_gate": true,
    "sandbox_generation_gate": true,
    "public_event_generation_gate": true
  }
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_final_summary_report_v1`.

### `final_summary_report_id`

Unique local identifier for the final Summary Report object. It must not be treated as a PDF export id, Markdown export id, briefing deck id, B-end report id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. Creating the final Summary Report object does not create a production case.

### `summary_report_candidate_id`

The reviewed local candidate used as the only content source for the final Summary Report object.

### `final_report_review_gate_id`

The approved review gate id. The gate must have status `ready_for_future_final_summary_report_runtime`.

### `report_gate_id`

The prior `ReportGenerationGate` id.

### `result_candidate_id`

The upstream `ManualAnalysisResultCandidate` id referenced through the candidate.

### `manual_analysis_execution_id`

The upstream `ManualAnalysisExecution` id.

### `boundary_gate_id`

The upstream `AnalysisResultBoundaryGate` id. Boundary notes and exclusions must remain intact.

### `created_at`

UTC timestamp for local final Summary Report object creation.

### `created_by`

Local reviewer or runtime label. It must not include secrets, cookie values, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, raw author identifiers, profile URLs, or private account identifiers.

### `status`

One of:

- `final_summary_report_created`
- `incomplete`
- `blocked`
- `privacy_hold`

Created means only that the local final Summary Report object exists. It does not mean export, B-end report, Sandbox, or public event readiness.

### `report_sections`

Reader-facing sections copied or normalized from the reviewed local candidate while preserving boundaries.

### `source_and_scope`

Machine-readable source and coverage caveats. These booleans must remain true in every final Summary Report object.

### `downstream_flags`

All downstream readiness flags remain false. A final Summary Report object does not export itself and does not create B-end, Sandbox, or public artifacts.

### `required_next_gates`

Separate future gates required before downstream artifact generation.

## Required Invariants

- The source is `SummaryReportCandidate` only.
- The final review gate must be ready.
- The final review gate audit must exist.
- The summary candidate audit must exist.
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

A future runtime should also append a separate audit object, for example `sentigraph_final_summary_report_audit_v1`, recording:

- final Summary Report id
- source candidate id
- final review gate id
- reviewer/runtime label
- created timestamp
- boundary preservation checklist
- audit refs copied from candidate and gate
- downstream side-effect flags, all false
- safe-mode flags, including no export, no B-end report, no Sandbox, no public event, no Evidence Layer write, no production case, no URL fetch, no real API, and no real LLM

