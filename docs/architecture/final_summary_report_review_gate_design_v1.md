# Final Summary Report Review Gate Design v1

## Purpose

Final Summary Report Review Gate is the future governance gate between a local `SummaryReportCandidate` and any future final Summary Report runtime.

The gate records whether a candidate has been reviewed by a human and is ready for a future final-summary runtime to consider. It does not generate the final Summary Report.

## Core Principle

A `SummaryReportCandidate` is not a final report.

Final Summary Report Review Gate is not:

- final Summary Report generation
- B-end report generation
- PDF export
- Markdown export
- briefing deck generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof

The gate only records future readiness, revision need, block state, or privacy hold for a local report candidate.

## Required Prior Chain

The future gate can only be considered after:

- `ReportGenerationGate` exists and is ready.
- `SummaryReportCandidate` exists.
- `SummaryReportCandidateAudit` exists.
- `ManualAnalysisResultCandidate` exists.
- `AnalysisResultBoundaryGate` exists.
- `ManualAnalysisExecutionAudit` exists.
- `ReportGenerationGateAudit` exists.
- The summary candidate keeps `candidate_only` status.
- The summary candidate has required report sections.
- The summary candidate includes audit trace references.

If any prior record is missing, inconsistent, privacy-held, or incomplete, the gate must return `needs_revision`, `blocked`, or `privacy_hold`.

## Required Preserved Boundaries

The gate must preserve:

- coverage limitation
- weak evidence warning
- rejected evidence excluded
- duplicate evidence no amplification
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- audit trace
- candidate-only status until future final runtime

These boundaries must remain visible in the gate record and must travel into any future final report runtime.

## Allowed Inputs

The future gate may inspect only safe local records:

- `SummaryReportCandidate`
- `SummaryReportCandidateAudit`
- `ReportGenerationGate`
- `ReportGenerationGateAudit`
- `ManualAnalysisResultCandidate`
- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGate`
- `AnalysisResultBoundaryGateAudit`

It must not inspect:

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

## Future Statuses

### `ready_for_future_final_summary_report_runtime`

The candidate has passed human review for a future final Summary Report runtime.

This status still does not generate a final Summary Report, export file, B-end report, Sandbox fixture, public event page, Evidence Layer write, or production case.

### `needs_revision`

The candidate has sections, warnings, wording, representative evidence, or audit trace gaps that should be revised before final runtime.

Requesting revision does not rewrite the candidate automatically.

### `blocked`

The candidate has unsafe or inconsistent content, missing boundary notes, attempted overclaims, rejected-evidence leakage, duplicate amplification risk, missing audit trace, or missing required sections.

### `privacy_hold`

Privacy, private-content, raw-identifier, or secret-like risk is present. All downstream final report, export, B-end, Sandbox, and public-event gates must stop.

## Future Runtime Recommendation

Future 7M should:

- read one `SummaryReportCandidate`
- verify related gate and audit references
- require a human review decision
- create a local `FinalSummaryReportReviewGate`
- append an audit record
- keep all downstream output flags false
- keep candidate-only and warning boundaries visible
- output required revisions or blocked reasons when needed

Future 7M must not:

- generate final report content
- generate export files
- generate B-end report files
- generate Sandbox fixtures
- generate public event pages
- write Evidence Layer
- create production case
- call real LLMs
- call external APIs
- re-read original rows
- fetch URLs

## Boundary Language

Use:

- Final Summary Report Review Gate
- review gate only
- future final summary runtime
- candidate remains non-final
- evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence warning
- rejected evidence excluded
- duplicate evidence does not amplify risk
- human review required
- downstream gates required

Avoid:

- final report generated
- report finalized
- export ready
- B-end report ready
- Sandbox ready
- public event ready
- official verified
- full-web coverage
- complete public opinion
- causal proof

