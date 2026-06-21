# Final Summary Report Export Runtime Design v1

## Purpose

Final Summary Report Export Runtime is a future controlled local runtime that may create report-file artifacts from a local `FinalSummaryReport`.

It can only be considered after `FinalSummaryReportExportGate.status` is `ready_for_future_export_runtime`.

This document is design-only. It does not implement the runtime and does not generate any export artifact.

## Required Prior Gate

The future runtime may run only when all of the following are true:

- `FinalSummaryReport` exists.
- `FinalSummaryReport.status` is `final_summary_report_created`.
- `FinalSummaryReportAudit` exists.
- `FinalSummaryReportExportGate` exists.
- `FinalSummaryReportExportGate.status` is `ready_for_future_export_runtime`.
- `FinalSummaryReportExportGateAudit` exists.
- upstream audit references are available for the final report, final report review gate, summary report candidate, report generation gate, manual analysis execution, and analysis result boundary gate.
- no privacy hold is active.
- no unresolved revision blocks remain.

Approval of the export gate means only that a later export runtime may be considered. It is not file generation, publication, delivery, B-end packaging, Sandbox generation, or public event generation.

## Allowed Future Inputs

The future runtime may read only safe local records:

- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- audit references embedded in those records

The future runtime must not read:

- original provider package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- private collector project files
- external collector raw row files
- browser profile data
- login, cookie, token, session, salt, password, API key, or `.env` values
- raw author identifiers
- profile URLs
- private messages

## Runtime Boundaries

The future export runtime is not:

- Final Summary Report creation
- B-end report runtime
- Sandbox generation
- public event generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- actual analysis engine execution
- real LLM call
- real platform, search, vendor, or provider API call
- provider execution
- collector execution
- URL fetching
- scraping
- official verification
- trust upgrade
- verification upgrade
- full-web, full-platform, or full-thread coverage

## Permitted Future Output Category

The only permitted future output category is a local export artifact derived from `FinalSummaryReport`.

Candidate artifact types are:

- `analyst_markdown`
- `executive_pdf`
- `briefing_deck_outline`
- `evidence_appendix_package`

These artifacts must remain local runtime artifacts until a separate publish, B-end, Sandbox, or public-event gate explicitly approves a downstream use.

## Required Boundary Preservation

Every future export artifact must preserve:

- boundary block
- evidence scope
- coverage limitation
- warnings
- audit trace
- source and scope metadata
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence remains warning-marked
- rejected evidence remains excluded
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions

Formatting must not hide or weaken these sections.

## Non-Goals

This phase does not implement:

- export runtime code
- Markdown file generation
- PDF file generation
- PowerPoint or briefing deck generation
- B-end report generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- analysis engine execution
- real LLM calls
- real platform, search, vendor, or provider API calls
- URL fetching
- scraping
- provider or collector jobs

## Future Runtime Recommendation

Future Phase 7S should implement a local runtime that:

1. reads `FinalSummaryReport`
2. verifies `FinalSummaryReportExportGate.status == ready_for_future_export_runtime`
3. verifies `FinalSummaryReportExportGateAudit`
4. verifies required audit references
5. selects one allowed export artifact type
6. writes only into an ignored runtime export folder
7. emits a `sentigraph_final_summary_report_export_artifact_v1` metadata record
8. preserves all boundary sections and warnings
9. records an append-only export artifact audit
10. leaves B-end, Sandbox, public-event, Evidence Layer, production case, and analysis flags false

The runtime must stop with `blocked` or `privacy_hold` if it detects missing audit references, unsafe claims, missing boundary sections, rejected evidence leakage, duplicate amplification, trust upgrade, verification upgrade, or private/secret-like values.

## Boundary Copy

Future UI or CLI output should include language equivalent to:

- This export is generated from a local Final Summary Report.
- Provider output is evidence, not truth.
- This artifact is not official verification.
- This artifact is not full-web, full-platform, or full-thread coverage.
- Weak evidence remains warning-marked.
- Rejected evidence remains excluded.
- Duplicate evidence is not counted as separate risk strength.
- B-end report, Sandbox, and public-event output require separate gates.

