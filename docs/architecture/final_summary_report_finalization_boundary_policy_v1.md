# Final Summary Report Finalization Boundary Policy v1

## Purpose

This policy defines what a future final Summary Report runtime may and may not do after a Final Summary Report Review Gate exists.

The policy is intentionally conservative. A reviewed candidate is not a license to re-open raw data, fetch URLs, call providers, call LLMs, or create downstream artifacts.

## Allowed Future Final Runtime Inputs

A future final Summary Report runtime may read only:

- `SummaryReportCandidate`
- `FinalSummaryReportReviewGate`
- `SummaryReportCandidateAudit`
- `ReportGenerationGateAudit`
- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGateAudit`
- other local append-only audit records that are already part of the governed chain

The final runtime should use the reviewed candidate as the report content source, not original data files.

## Forbidden Inputs And Side Effects

Future final report runtime must not:

- read original package rows
- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- fetch URLs
- scrape websites
- call provider jobs
- call collector jobs
- call real platform APIs
- call real search APIs
- call real vendor APIs
- call real LLM APIs
- use login, profile, cookie, token, session, proxy, captcha, or anti-bot bypass state
- read or print secrets, API key values, `.env` values, salts, passwords, cookies, tokens, or sessions
- write Evidence Layer
- create production case
- create production review queue
- run production dedup
- create B-end report
- create export files
- create Sandbox fixtures
- create public event pages

## Trust And Verification Boundaries

Future final report runtime must not:

- upgrade trust labels
- upgrade verification status
- claim official verification
- claim full-web coverage
- claim full-platform coverage
- claim full-thread coverage
- claim causal proof
- claim provider output is truth
- remove evidence limitations
- remove weak-evidence warnings
- include rejected evidence
- amplify duplicate evidence into risk, sentiment, coverage, or conclusions

The final report can improve formatting and reader structure, but not truth status.

## Warning Preservation

The following warnings must remain visible:

- selected reviewed evidence scope
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not official verification
- provider output is evidence, not truth
- weak evidence remains warning-marked
- rejected evidence excluded
- duplicate evidence does not amplify risk
- audit trace available

If a future final report cannot preserve these warnings, it must block or return `needs_revision`.

## Privacy Boundary

Future final runtime must stop if it detects:

- raw author identifiers
- raw author names
- profile URLs
- private messages
- email addresses
- phone numbers
- password-like values
- API key values
- token values
- cookie values
- session values
- `.env` values
- private account identifiers

Such detection should produce `privacy_hold`, not a final report.

## Final Runtime Output Boundary

Future final Summary Report Runtime may create only a local final summary report object if a later phase explicitly implements it.

It must not also create:

- PDF export
- Markdown export
- briefing deck
- B-end report
- Sandbox fixture
- public event page
- production Evidence Layer writes
- production case records

Those outputs require separate downstream gates.

## Recommended Future Runtime Checks

Before creating any local final report object, future runtime should verify:

- review gate status is `ready_for_future_final_summary_report_runtime`
- candidate status is valid
- candidate audit exists
- review gate audit exists
- all required sections are present
- all boundary notes are preserved
- downstream output flags remain false
- privacy scan has no blockers
- rejected evidence is excluded
- weak evidence warning remains
- duplicate evidence is not amplified

If any check fails, no final report object should be created.

