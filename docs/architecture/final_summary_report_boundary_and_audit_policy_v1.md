# Final Summary Report Boundary and Audit Policy v1

## Purpose

This policy defines boundary and audit requirements for any future local Final Summary Report Runtime.

The final report object may make the candidate easier to read, but it must not weaken governance guarantees or remove safety caveats.

## Boundary Preservation Requirements

The future runtime must preserve the `SummaryReportCandidate.boundary_block`.

It must also preserve `FinalSummaryReportReviewGate.boundary_notes`, including:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence remains warning-marked
- rejected evidence remains excluded
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- no original package row read
- no URL fetch
- no real API
- no real LLM
- no provider or collector execution
- downstream gates required for export, B-end report, Sandbox, and public event

## Required Audit References

The final Summary Report object must include audit refs to:

- `SummaryReportCandidate`
- `SummaryReportCandidateAudit`
- `FinalSummaryReportReviewGate`
- `FinalSummaryReportReviewGateAudit`
- `ReportGenerationGate`
- `ReportGenerationGateAudit`
- `ManualAnalysisExecution`
- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGate`
- `AnalysisResultBoundaryGateAudit`

If any required audit record is missing, the future runtime must return `incomplete` or `blocked`.

## Warning Preservation

The future runtime must not remove:

- weak evidence warning
- rejected-evidence exclusion
- duplicate non-amplification warning
- privacy limitation
- source coverage limitation
- selected sample limitation
- not-official-verification statement
- not-full-web/full-platform/full-thread statement
- provider-output-is-evidence-not-truth statement

## Evidence Exclusion Requirements

The future runtime must not include:

- rejected evidence
- privacy-held evidence
- needs-more-source evidence unless a later explicit governance rule allows it
- raw/private rows
- original package rows
- unreviewed collector rows
- secret-like values
- raw author identifiers
- private messages

## No Trust or Verification Upgrade

The future runtime must not upgrade:

- trust label
- verification status
- provenance type
- coverage scope
- official verification status
- causal confidence

The report may repeat the reviewed status of evidence, but it must not make a stronger claim than the candidate and gate support.

## Duplicate Handling

Duplicate evidence must not amplify:

- sentiment
- risk
- topic importance
- coverage claims
- report conclusions

Duplicate group size can be shown only as a clearly labeled evidence-density or repetition signal.

## Raw Identifier and Secret Safety

The future runtime must not expose:

- raw author identifiers
- raw author names
- profile URLs
- private messages
- cookies
- tokens
- sessions
- API key values
- `.env` values
- passwords
- email addresses
- phone numbers

These names may appear only in safety checks, forbidden-field lists, or redaction policy text.

## Downstream Boundary Statement

Every future final Summary Report object must state:

- export requires a separate Export Gate
- B-end report requires a separate B-end Report Gate
- Sandbox generation requires a separate Sandbox Generation Gate
- public event generation requires a separate Public Event Generation Gate

The final Summary Report Runtime must not set downstream output flags to ready.

## Audit Companion Requirements

A future `sentigraph_final_summary_report_audit_v1` should record:

- final report id
- candidate id
- review gate id
- audit refs
- runtime label
- created timestamp
- boundary preservation checklist
- warnings copied
- exclusions copied
- downstream flags all false
- no Evidence Layer write
- no production case
- no export
- no B-end report
- no Sandbox
- no public event
- no provider/collector job
- no real API
- no real LLM
- no URL fetch or scraping

Audit records must be append-only and must not overwrite prior candidate or gate audits.

