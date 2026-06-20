# Summary Report Candidate Contract v1

## Purpose

This contract defines the future `sentigraph_summary_report_candidate_v1` object.

The object is a local candidate for human review. It is not a final Summary Report, B-end report, PDF, Markdown, briefing deck, Sandbox fixture, public event page, production Evidence Layer record, production case, official verification, or full-web analysis.

## Future Object

```json
{
  "schema": "sentigraph_summary_report_candidate_v1",
  "summary_report_candidate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "result_candidate_id": "...",
  "manual_analysis_execution_id": "...",
  "report_gate_id": "...",
  "boundary_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "summary_report_candidate_created|incomplete|blocked|privacy_hold",
  "input_refs": {
    "manual_analysis_execution_id": "...",
    "manual_analysis_execution_audit_ids": [],
    "result_candidate_id": "...",
    "boundary_gate_id": "...",
    "boundary_gate_audit_ids": [],
    "report_gate_id": "...",
    "report_gate_audit_ids": []
  },
  "executive_summary_candidate": {
    "headline": "",
    "summary_points": [],
    "confidence_note": "",
    "candidate_only_note": ""
  },
  "evidence_scope_section": {
    "review_case_id": "...",
    "included_item_count": 0,
    "included_group_count": 0,
    "weak_evidence_count": 0,
    "rejected_evidence_excluded_count": 0,
    "duplicate_group_count": 0,
    "coverage_statement": ""
  },
  "analysis_summary_section": {
    "topic_summary": [],
    "sentiment_summary": {},
    "narrative_summary": [],
    "representative_commentary": []
  },
  "risk_and_topic_section": {
    "risk_level_candidate": "",
    "risk_drivers": [],
    "topic_clusters": [],
    "limitations": []
  },
  "representative_evidence_section": {
    "items": [],
    "selection_policy": "safe_preview_only_no_raw_identifiers"
  },
  "boundary_block": {
    "provider_output_is_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true,
    "not_full_platform_coverage": true,
    "not_full_thread_coverage": true,
    "weak_evidence_warning": true,
    "rejected_evidence_excluded": true,
    "dedup_no_amplification": true,
    "candidate_only": true
  },
  "limitations": [],
  "warnings": [],
  "audit_trace": {
    "manual_analysis_execution_audit_ids": [],
    "boundary_gate_audit_ids": [],
    "report_gate_audit_ids": []
  },
  "downstream_flags": {
    "final_summary_report_ready": false,
    "b_end_report_ready": false,
    "pdf_export_ready": false,
    "markdown_export_ready": false,
    "deck_export_ready": false,
    "sandbox_ready": false,
    "public_event_ready": false
  },
  "safe_mode": {
    "summary_report_candidate_only": true,
    "final_report_generated": false,
    "b_end_report_generated": false,
    "pdf_export_generated": false,
    "markdown_export_generated": false,
    "briefing_deck_generated": false,
    "sandbox_fixture_generated": false,
    "public_event_page_generated": false,
    "evidence_layer_written": false,
    "production_case_created": false,
    "original_package_rows_re_read": false,
    "provider_execution": false,
    "collector_jobs_run": false,
    "real_api_calls": false,
    "real_llm_calls": false,
    "url_fetching": false,
    "scraping": false,
    "secrets_exposed": false,
    "raw_author_identifiers_exposed": false
  }
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_summary_report_candidate_v1`.

### `summary_report_candidate_id`

Unique local identifier for this candidate. It must not be treated as a final report id, export id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The report candidate remains review-only unless a later production promotion gate explicitly changes that.

### `result_candidate_id`

Manual Analysis Result Candidate id. This is the only allowed analysis content source.

### `manual_analysis_execution_id`

Manual Analysis Execution id. The execution must have an append-only audit record.

### `report_gate_id`

Report Generation Gate id. The gate must be ready and must have an audit record.

### `boundary_gate_id`

Analysis Result Boundary Gate id. The boundary must remain valid and must not be privacy-held or blocked.

### `created_at`

UTC timestamp for the local candidate creation.

### `created_by`

Local operator or UI label. It must not include secrets, cookie values, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, raw author identifiers, profile URLs, or private account identifiers.

### `status`

One of:

- `summary_report_candidate_created`
- `incomplete`
- `blocked`
- `privacy_hold`

`summary_report_candidate_created` means only that a local candidate object exists. It does not mean final report readiness, export readiness, B-end readiness, Sandbox readiness, or public-event readiness.

### `input_refs`

References to the safe local inputs and audits used to create the candidate. It must not reference original package row files or external URLs as runtime inputs.

### `executive_summary_candidate`

A bounded summary of the candidate analysis. It must be written as a candidate-only summary and must not imply full truth, official verification, causal proof, or complete public opinion coverage.

### `evidence_scope_section`

Reader-facing evidence scope and counts. Counts are governance context only and must not imply full-web, full-platform, or full-thread coverage.

### `analysis_summary_section`

Reader-facing organization of safe topic, sentiment, and narrative summaries from the `ManualAnalysisResultCandidate`.

### `risk_and_topic_section`

Risk and topic interpretation candidate. It must preserve weak-evidence warnings, rejected-evidence exclusion, duplicate non-amplification, and confidence limitations.

### `representative_evidence_section`

Safe representative evidence preview. It must not include raw author identifiers, profile URLs, private messages, secret-like values, or private contact details.

### `boundary_block`

Required report boundary flags. These flags must preserve the upstream result candidate boundary block and report gate boundary notes.

### `limitations`

Limitations that must be visible to future reviewers and readers.

### `warnings`

Warnings that must travel with future report finalization, export, Sandbox, or public event gates.

### `audit_trace`

Append-only audit references proving that manual analysis execution, boundary gate, and report generation gate records existed before candidate creation.

### `downstream_flags`

All downstream readiness flags must remain false in this runtime:

- `final_summary_report_ready=false`
- `b_end_report_ready=false`
- `pdf_export_ready=false`
- `markdown_export_ready=false`
- `deck_export_ready=false`
- `sandbox_ready=false`
- `public_event_ready=false`

### `safe_mode`

Machine-readable proof that this candidate did not create downstream artifacts, call real APIs or LLMs, fetch URLs, scrape websites, expose secrets, or expose raw author identifiers.

## Required Invariants

- The only analysis content source is `ManualAnalysisResultCandidate`.
- Report Generation Gate must be ready.
- Report Generation Gate Audit must exist.
- Manual Analysis Execution Audit must exist.
- Analysis Result Boundary Gate Audit must exist.
- Boundary block must be preserved.
- Rejected evidence must remain excluded.
- Weak evidence must remain warning-marked.
- Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.
- Provider output must remain evidence, not truth.
- Trust labels must not be upgraded.
- Verification status must not be upgraded.
- No raw author identifiers, private content, or secret-like values may be displayed.
- No final report or export readiness may be set true.
