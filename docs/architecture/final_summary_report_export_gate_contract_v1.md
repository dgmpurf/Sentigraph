# Final Summary Report Export Gate Contract v1

## Purpose

This contract defines the future `sentigraph_final_summary_report_export_gate_v1` object.

The object records a human export-readiness decision for a local `FinalSummaryReport`. It is not a Markdown file, PDF file, briefing deck, B-end report, Sandbox fixture, public event page, Evidence Layer write, production case, official verification, or full-web analysis.

## Future Object

```json
{
  "schema": "sentigraph_final_summary_report_export_gate_v1",
  "export_gate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "final_summary_report_id": "...",
  "final_summary_report_audit_id": "...",
  "summary_report_candidate_id": "...",
  "final_report_review_gate_id": "...",
  "report_gate_id": "...",
  "result_candidate_id": "...",
  "manual_analysis_execution_id": "...",
  "boundary_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "ready_for_future_export_runtime|needs_revision|blocked|privacy_hold",
  "export_decision": "approve_for_future_export_runtime|request_revision|block|privacy_hold",
  "allowed_future_exports": {
    "markdown_export_candidate": true,
    "pdf_export_candidate": true,
    "briefing_deck_outline_candidate": true,
    "evidence_appendix_package_candidate": true
  },
  "not_allowed_now": {
    "markdown_file_now": true,
    "pdf_file_now": true,
    "pptx_file_now": true,
    "b_end_report_now": true,
    "sandbox_now": true,
    "public_event_now": true
  },
  "input_boundary": {
    "source": "final_summary_report",
    "read_original_package_rows_now": false,
    "call_llm_now": false,
    "call_external_api_now": false,
    "write_evidence_layer_now": false,
    "create_production_case_now": false
  },
  "required_export_sections": {
    "boundary_block": true,
    "evidence_scope": true,
    "coverage_limitation": true,
    "warnings": true,
    "audit_trace": true,
    "source_and_scope": true
  },
  "downstream_readiness": {
    "can_run_future_markdown_export_runtime": true,
    "can_run_future_pdf_export_runtime": true,
    "can_run_future_deck_outline_runtime": true,
    "can_generate_export_now": false,
    "can_generate_b_end_report_now": false,
    "can_generate_sandbox_now": false,
    "can_generate_public_event_now": false,
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

Constant value: `sentigraph_final_summary_report_export_gate_v1`.

### `export_gate_id`

Unique local identifier for this export gate object. It must not be treated as an export file id, B-end report id, Sandbox id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The export gate does not create a production case.

### `final_summary_report_id`

The local final Summary Report being reviewed for future export eligibility.

### `final_summary_report_audit_id`

Audit record proving that the local final Summary Report was created through the approved final Summary Report runtime path.

### `summary_report_candidate_id`

Upstream `SummaryReportCandidate` id used as the source for the final Summary Report.

### `final_report_review_gate_id`

Upstream `FinalSummaryReportReviewGate` id. It should have previously allowed the final Summary Report runtime.

### `report_gate_id`

Upstream `ReportGenerationGate` id.

### `result_candidate_id`

Upstream `ManualAnalysisResultCandidate` id.

### `manual_analysis_execution_id`

Upstream `ManualAnalysisExecution` id.

### `boundary_gate_id`

Upstream `AnalysisResultBoundaryGate` id. Export eligibility must preserve boundary notes and exclusions from this gate.

### `created_at`

UTC timestamp for local export gate creation.

### `created_by`

Local reviewer or runtime label. It must not include cookies, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, raw author identifiers, profile URLs, or private account identifiers.

### `status`

One of:

- `ready_for_future_export_runtime`
- `needs_revision`
- `blocked`
- `privacy_hold`

Ready means only that a future export runtime may be considered. It does not generate files and does not create downstream artifacts.

### `export_decision`

One of:

- `approve_for_future_export_runtime`
- `request_revision`
- `block`
- `privacy_hold`

The decision records human review outcome. It does not rewrite the final report automatically.

### `allowed_future_exports`

Candidate export modes that may be considered by future dedicated runtimes. These are candidates only, not generated artifacts.

### `not_allowed_now`

Explicit no-side-effect flags. `true` means that the action is not allowed during this gate phase.

### `input_boundary`

Machine-readable input restrictions. The only source is the local `FinalSummaryReport`; no original rows, network calls, LLM calls, Evidence Layer writes, or production case creation are allowed.

### `required_export_sections`

Sections and metadata that must survive into any future export runtime and output.

### `downstream_readiness`

Future-runtime readiness booleans. `can_run_future_*` values only authorize a later gate/runtime to be considered. `can_generate_*_now` values must remain false.

### `blocked_reasons`

Human-readable reasons for `blocked` or `privacy_hold`, such as unsafe claims, missing boundary block, rejected evidence leakage, duplicate amplification risk, missing audit trace, or privacy risk.

### `required_revisions`

Specific revisions required before the final Summary Report can be reconsidered for future export runtime.

### `warnings`

Warnings that must remain visible to reviewers and future export runtime.

### `boundary_notes`

Boundary statements preserved from upstream gates and local final Summary Report.

### `audit_refs`

References to upstream audit records, including final summary report audit, final review gate audit, summary candidate audit, report gate audit, manual execution audit, and boundary gate audit.

## Required Invariants

- The input source is `FinalSummaryReport` only.
- The final Summary Report audit must exist.
- Required upstream gates and audits must exist.
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
- No Markdown, PDF, PowerPoint, B-end, Sandbox, or public-event artifact is generated.

## Suggested Audit Companion

A future runtime should append `sentigraph_final_summary_report_export_gate_audit_v1`, recording:

- export gate id
- final Summary Report id
- reviewer label
- export decision
- previous and new gate status
- required revisions or blocked reasons
- boundary preservation checklist
- audit references
- downstream side-effect flags, all false
- safe-mode flags, including no export file now, no B-end report, no Sandbox, no public event, no Evidence Layer write, no production case, no URL fetch, no real API, and no real LLM

