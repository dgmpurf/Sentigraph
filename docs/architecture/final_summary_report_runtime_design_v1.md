# Final Summary Report Runtime Design v1

## Purpose

Final Summary Report Runtime is the future local runtime that may create a local final Summary Report object after a human-approved Final Summary Report Review Gate.

The runtime can only run when `FinalSummaryReportReviewGate.status` is `ready_for_future_final_summary_report_runtime`.

This design is architecture-only. It does not implement runtime and does not generate a final Summary Report.

## Core Principle

A future Final Summary Report is a local final report object only.

It is still not:

- PDF export
- Markdown export
- briefing deck export
- B-end report
- Sandbox fixture
- public event page
- Evidence Layer write
- production case
- production review queue
- production dedup
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- legal, PR, or business guarantee

The object may organize already reviewed local candidate content into a final local report shape, but it must not upgrade trust, verification, coverage, causality, or downstream readiness.

## Required Prior Chain

The future runtime can only be considered after:

- `SummaryReportCandidate` exists.
- `SummaryReportCandidate.status` is `summary_report_candidate_created`.
- `SummaryReportCandidateAudit` exists.
- `FinalSummaryReportReviewGate` exists.
- `FinalSummaryReportReviewGate.status` is `ready_for_future_final_summary_report_runtime`.
- `FinalSummaryReportReviewGateAudit` exists.
- `ReportGenerationGate` exists and remains ready.
- `ManualAnalysisExecution` exists.
- `ManualAnalysisExecutionAudit` exists.
- `ManualAnalysisResultCandidate` exists.
- `AnalysisResultBoundaryGate` exists and remains ready.
- The candidate boundary block is present and complete.
- Weak evidence remains warning-marked.
- Rejected evidence remains excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- Provider output is evidence, not truth.
- The candidate and gate do not claim official verification.
- The candidate and gate do not claim full-web, full-platform, or full-thread coverage.
- No privacy blocker exists.
- No unresolved needs-more-source blocker exists.

If any prior record is missing, inconsistent, incomplete, privacy-held, or unsafe, the future runtime must return `incomplete`, `blocked`, or `privacy_hold`.

## Allowed Inputs

The future runtime may read only safe local records:

- `SummaryReportCandidate`
- `SummaryReportCandidateAudit`
- `FinalSummaryReportReviewGate`
- `FinalSummaryReportReviewGateAudit`
- `ReportGenerationGate`
- `ReportGenerationGateAudit`
- `ManualAnalysisExecution`
- `ManualAnalysisExecutionAudit`
- `ManualAnalysisResultCandidate`
- `AnalysisResultBoundaryGate`
- `AnalysisResultBoundaryGateAudit`

It must not read:

- original provider package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- external collector output rows
- private collector project files
- browser profile data
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- raw author identifiers
- private messages
- URLs through network fetch

## Non-Goals

This design does not implement:

- runtime code
- final Summary Report generation
- B-end report generation
- PDF, Markdown, or briefing deck export
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- actual analysis engine execution
- real LLM calls
- real platform, search, vendor, or provider API calls
- provider execution
- collector execution
- URL fetching
- scraping
- trust upgrade
- verification upgrade

## Future Runtime Behavior

Future 7O should:

- read one approved `FinalSummaryReportReviewGate`
- read its referenced `SummaryReportCandidate`
- verify all audit references remain available
- copy required report sections from the candidate into a final local report object
- preserve candidate boundary block and review gate boundary notes
- preserve limitations, confidence notes, warnings, and audit trace
- keep downstream flags false
- require separate downstream gates for export, B-end report, Sandbox, and public event
- write only the local final Summary Report object and its audit if that audit is separately designed

Future 7O must not:

- generate PDF, Markdown, or briefing deck files
- generate B-end report files
- generate Sandbox fixtures
- generate public event pages
- write Evidence Layer
- create production case
- call real LLMs
- call external APIs
- re-read original rows
- fetch URLs

## Required Boundary Copy

Any future UI or JSON output should include boundary copy equivalent to:

- This is a local final Summary Report object.
- It is based on a reviewed local Summary Report Candidate.
- Provider output is evidence, not truth.
- It is not official verification.
- It is not full-web, full-platform, or full-thread coverage.
- Weak evidence remains warning-marked.
- Rejected evidence remains excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- Export, B-end report, Sandbox, and public-event output require separate future gates.

## First Runtime Recommendation

Future 7O should implement a local final Summary Report writer behind `FinalSummaryReportReviewGate`.

It should create `sentigraph_final_summary_report_v1` only when:

- the review gate status is `ready_for_future_final_summary_report_runtime`
- review gate audit exists
- summary candidate audit exists
- report gate audit exists
- manual execution audit exists
- boundary gate audit exists
- all required sections can be populated from safe candidate/gate/audit records
- all downstream flags remain false

## Boundary Language

Use:

- Final Summary Report
- local final report object
- reviewed local candidate source
- evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence warning
- rejected evidence excluded
- duplicate evidence does not amplify risk
- downstream gates required

Avoid:

- PDF ready
- Markdown ready
- deck ready
- B-end report ready
- public event ready
- Sandbox ready
- official verified
- full-web coverage
- all-platform coverage
- complete public opinion
- causal proof
- legal guarantee
- PR guarantee

