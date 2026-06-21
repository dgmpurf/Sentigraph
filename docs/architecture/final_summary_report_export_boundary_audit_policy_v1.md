# Final Summary Report Export Boundary Audit Policy v1

## Purpose

This policy defines boundary preservation and audit requirements for a future Final Summary Report Export Runtime.

It is design-only. It does not implement export runtime and does not generate any file.

## Required Boundary Preservation

Future export runtime must preserve the `FinalSummaryReport` boundary block.

It must also preserve `FinalSummaryReportExportGate` boundary notes.

The artifact must clearly state:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence remains warning-marked
- rejected evidence remains excluded
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- B-end, Sandbox, and public event outputs require separate gates

These statements must be visible in the exported artifact, not only in metadata.

## Required Audit References

Future export runtime must include audit references to:

- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- `FinalSummaryReportReviewGate`
- `SummaryReportCandidate`
- `ReportGenerationGate`
- `ManualAnalysisExecution`
- `AnalysisResultBoundaryGate`

When available, the artifact metadata should also retain references to:

- `ManualAnalysisResultCandidate`
- `SummaryReportCandidateAudit`
- `ReportGenerationGateAudit`
- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGateAudit`
- `FinalSummaryReportReviewGateAudit`

Missing required audit references must block export artifact creation.

## Warning Preservation

The runtime must not:

- remove weak evidence warnings
- remove coverage limitations
- remove review limitations
- remove uncertainty wording
- remove sample limitation text
- rewrite unverified evidence as verified evidence
- rewrite vendor-attested or user-attested evidence as official API evidence
- rewrite selected public samples as full-web or full-platform coverage

## Rejected Evidence Policy

Rejected evidence must remain excluded from export support.

The artifact may include a count or audit note that rejected evidence was excluded, but it must not use rejected evidence text, rejected evidence snippets, or rejected evidence claims as report support.

## Duplicate Evidence Policy

Duplicate evidence must not amplify:

- risk
- sentiment
- coverage
- conclusions
- urgency
- confidence

Group size may be shown as evidence density or repetition signal only when labeled as such and when it does not become truth strength.

## Trust and Verification Policy

The export runtime must not upgrade:

- trust label
- verification status
- source authority
- coverage status
- causal certainty

Screenshots and transcriptions must not be described as automatically verified.

Provider output remains evidence, not truth.

## Privacy and Secret Policy

The runtime must not expose:

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
- emails
- phone numbers
- salts
- browser profile paths
- private account identifiers

If any such value appears in the final report, export gate, or audit metadata, the runtime must stop with `privacy_hold`.

## Audit Event Recommendation

Future runtime should append an export artifact audit record containing:

- export artifact id
- export gate id
- final summary report id
- artifact type and format
- local runtime path
- reviewer or runtime label
- created timestamp
- boundary preservation checklist
- warning preservation checklist
- rejected evidence exclusion confirmation
- duplicate no-amplification confirmation
- trust and verification no-upgrade confirmation
- privacy scan result
- downstream flags, all false

## Downstream Boundary

Export runtime is not a downstream generation gate.

It must explicitly state:

- B-end report requires B-end Report Gate.
- Sandbox requires Sandbox Generation Gate.
- Public event requires Public Event Generation Gate.
- Public or C-end versions may simplify language but must not remove warnings, uncertainty, evidence scope, or coverage limitations.

