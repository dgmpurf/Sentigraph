# Summary Report Candidate to Export Gate v1

## Purpose

This document defines the downstream gate relationship after a future `SummaryReportCandidate` is created.

Summary Report Candidate Runtime is not export runtime. It does not create final Summary Report, B-end report, PDF, Markdown, briefing deck, Sandbox, or public event output.

## Candidate Is Not Final

Candidate creation does not mean:

- final Summary Report is ready
- B-end report is ready
- PDF export is ready
- Markdown export is ready
- briefing deck is ready
- Sandbox fixture is ready
- public event page is ready
- Evidence Layer write is allowed
- production case is created
- official verification exists
- full-web, full-platform, or full-thread coverage exists

## Required Future Gates

### Final Summary Report Review Gate

A final Summary Report requires a future finalization or review gate.

That gate must verify:

- candidate sections are complete
- warnings are visible
- limitations are visible
- audit trace is complete
- reviewer approves finalization
- no downstream export is implied

### B-end Report Gate

B-end report output requires a separate B-end Report Gate.

That gate must verify:

- audience-specific language is appropriate
- commercial claims remain conservative
- legal, PR, and business guarantees are not made
- evidence boundaries remain visible

### Export Gate

PDF, Markdown, and briefing deck outputs require a separate Export Gate.

That gate must verify:

- no secrets
- no raw author identifiers
- no private content
- no unsafe claims
- all required boundary sections survive formatting
- export metadata states candidate/final status accurately

### Sandbox Generation Gate

Sandbox output requires a separate Sandbox Generation Gate.

That gate must verify:

- simplified visualization does not remove evidence boundaries
- PeopleCluster and InfluenceCore language remains safe
- no causal-proof claim is introduced
- no public event readiness is implied

### Public Event Generation Gate

Public or C-end event output requires a separate Public Event Generation Gate.

That gate must verify:

- public language is simplified without removing warnings
- selected sample boundaries remain visible
- request/vote or public interest labels are not represented as natural public-opinion heat unless proven
- no official verification or full-web claim is introduced

## Public/C-End Simplification Rule

Public and C-end surfaces may simplify wording, but must not remove:

- candidate-only status
- selected or available evidence scope
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence warning when applicable
- rejected evidence excluded
- duplicate non-amplification
- provider output is evidence, not truth

## Downstream Flags

`SummaryReportCandidate.downstream_flags` must remain:

```json
{
  "final_summary_report_ready": false,
  "b_end_report_ready": false,
  "pdf_export_ready": false,
  "markdown_export_ready": false,
  "deck_export_ready": false,
  "sandbox_ready": false,
  "public_event_ready": false
}
```

Any future transition that changes one of these flags requires a separate gate, append-only audit, and explicit human decision.

## Suggested Future Phases

- 7K: Summary Report Candidate Runtime
- 7L: Summary Report Candidate Review Gate Design
- 7M: Summary Report Candidate Review Gate Runtime
- 7N: Final Summary Report Finalization Gate Design
- 7O: Final Summary Report Finalization Gate Runtime
- 7P: Export Gate Design for PDF, Markdown, and briefing deck
- 7Q: Export Gate Runtime
- 7R: B-end Report Gate Design
- 7S: Sandbox/Public Event Generation Gate Design

## Boundary Language

Use:

- future gate required
- candidate is not final
- export not ready
- public event not ready
- Sandbox not ready
- B-end report not ready
- warnings must survive formatting
- public language may simplify but not remove boundaries

Avoid:

- final report ready
- PDF ready
- public page ready
- Sandbox ready
- B-end report ready
- official verified
- full-web coverage
- all-platform coverage
- causal proof
- public opinion complete
