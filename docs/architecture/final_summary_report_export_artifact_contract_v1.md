# Final Summary Report Export Artifact Contract v1

## Purpose

This contract defines the future `sentigraph_final_summary_report_export_artifact_v1` object.

The object records metadata for a local export artifact generated from `FinalSummaryReport` after `FinalSummaryReportExportGate.status` is `ready_for_future_export_runtime`.

This contract is design-only. It does not generate Markdown, PDF, PowerPoint, B-end report, Sandbox, public event, or any runtime artifact.

## Future Object

```json
{
  "schema": "sentigraph_final_summary_report_export_artifact_v1",
  "export_artifact_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "final_summary_report_id": "...",
  "export_gate_id": "...",
  "export_gate_audit_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "export_artifact_created|incomplete|blocked|privacy_hold",
  "artifact_type": "analyst_markdown|executive_pdf|briefing_deck_outline|evidence_appendix_package",
  "artifact_format": "md|pdf|pptx_outline|json_bundle",
  "artifact_scope": {
    "source": "final_summary_report",
    "is_b_end_report": false,
    "is_public_event": false,
    "is_sandbox": false,
    "is_production_case": false
  },
  "artifact_paths": {
    "local_runtime_path": "...",
    "public_url": null
  },
  "export_sections": {
    "boundary_block": true,
    "evidence_scope": true,
    "coverage_limitation": true,
    "warnings": true,
    "audit_trace": true,
    "source_and_scope": true
  },
  "source_and_scope": {
    "provider_output_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true,
    "not_full_platform_coverage": true,
    "not_full_thread_coverage": true
  },
  "downstream_flags": {
    "b_end_report_ready": false,
    "sandbox_ready": false,
    "public_event_ready": false
  },
  "required_next_gates": {
    "b_end_report_gate": true,
    "sandbox_generation_gate": true,
    "public_event_generation_gate": true
  },
  "audit_refs": {}
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_final_summary_report_export_artifact_v1`.

### `export_artifact_id`

Unique local id for the export artifact metadata record. It must not be treated as a B-end report id, Sandbox id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The export artifact does not create or promote a production case.

### `final_summary_report_id`

The `FinalSummaryReport` used as the only report content source.

### `export_gate_id`

The `FinalSummaryReportExportGate` that approved future export runtime consideration.

### `export_gate_audit_id`

Audit record for the export gate decision.

### `created_at`

UTC timestamp for local artifact metadata creation.

### `created_by`

Local runtime or reviewer label. It must not contain cookies, tokens, sessions, API key values, `.env` values, passwords, emails, phone numbers, raw author identifiers, profile URLs, private messages, or private account identifiers.

### `status`

One of:

- `export_artifact_created`
- `incomplete`
- `blocked`
- `privacy_hold`

`export_artifact_created` means a local export artifact metadata record and local artifact path exist. It does not mean the artifact is public, client-approved, B-end packaged, Sandbox-ready, or public-event-ready.

### `artifact_type`

One of:

- `analyst_markdown`: analyst-readable local report draft
- `executive_pdf`: rendered executive summary or client-facing local artifact after future runtime support
- `briefing_deck_outline`: structured outline for a deck, not a full PowerPoint file unless a future PPTX runtime exists
- `evidence_appendix_package`: safe metadata and audit appendix package

### `artifact_format`

One of:

- `md`
- `pdf`
- `pptx_outline`
- `json_bundle`

The format must match the artifact type. `pptx_outline` is not a generated `.pptx` deck.

### `artifact_scope`

Machine-readable scope boundaries:

- `source` must be `final_summary_report`
- `is_b_end_report` must be false
- `is_public_event` must be false
- `is_sandbox` must be false
- `is_production_case` must be false

### `artifact_paths`

Local runtime path metadata only.

- `local_runtime_path` must remain inside an ignored runtime export folder.
- `public_url` must be null unless a later public publishing gate exists.

### `export_sections`

Required sections that must appear in the export artifact. No artifact may omit the boundary block, evidence scope, coverage limitation, warnings, audit trace, or source and scope metadata.

### `source_and_scope`

Required scope claims that must remain true and visible:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage

### `downstream_flags`

All downstream readiness flags must remain false. Export artifact creation does not make B-end report, Sandbox, or public event output ready.

### `required_next_gates`

Separate downstream gates are required before later B-end report, Sandbox, or public event generation.

### `audit_refs`

References to upstream audit records. At minimum, this should include:

- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- `FinalSummaryReportReviewGate`
- `SummaryReportCandidate`
- `ReportGenerationGate`
- `ManualAnalysisExecution`
- `AnalysisResultBoundaryGate`

## Required Invariants

- Input source is `FinalSummaryReport` only.
- `FinalSummaryReportExportGate.status` must be `ready_for_future_export_runtime`.
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
- B-end, Sandbox, and public-event readiness remain false.

