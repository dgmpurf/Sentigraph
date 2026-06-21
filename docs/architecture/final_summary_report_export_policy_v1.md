# Final Summary Report Export Policy v1

## Purpose

This policy defines the human review requirements before any future export runtime may consider a local `FinalSummaryReport`.

Export review is a governance checkpoint. It is not export execution.

## Human Review Requirement

Human review is required before future export runtime.

The reviewer must confirm that the local final Summary Report is safe to pass into a future export-specific runtime. Approval does not create a Markdown file, PDF file, PowerPoint deck, B-end report, Sandbox fixture, or public event page.

## Reviewer Checklist

The reviewer must confirm:

- final report sections are present
- boundary block is present
- warnings are preserved
- representative evidence is safe and redacted
- rejected evidence is excluded
- weak evidence warning remains
- duplicate no-amplification note remains
- provider output evidence-not-truth note remains
- not official verification remains
- not full-web coverage remains
- not full-platform coverage remains
- not full-thread coverage remains
- audit trace exists
- no raw, private, or secret-like fields are present

If any item fails, the reviewer must choose `request_revision`, `block`, or `privacy_hold`.

## Export Decisions

### `approve_for_future_export_runtime`

The final Summary Report may be considered by a later dedicated export runtime.

This decision does not:

- generate Markdown
- generate PDF
- generate PowerPoint or briefing deck
- generate B-end report
- generate Sandbox fixture
- generate public event page
- write Evidence Layer
- create production case
- call real LLM
- call external API
- fetch URL

### `request_revision`

The final Summary Report needs changes before export eligibility can be reconsidered.

Requesting revision does not rewrite the final report automatically. Revision requires a separate future workflow, audit trail, and renewed review.

### `block`

The final Summary Report has unsafe, inconsistent, incomplete, or overclaiming content that should not enter future export runtime.

Common block reasons:

- missing boundary block
- rejected evidence leakage
- weak evidence warning removed
- duplicate amplification risk
- official verification overclaim
- full-web, full-platform, or full-thread overclaim
- missing audit trace
- unsafe representative evidence

### `privacy_hold`

Privacy, private-content, raw-identifier, or secret-like risk is present.

`privacy_hold` blocks downstream export and public use until the issue is resolved through a separate audited process.

## Required Preserved Wording

Future export runtime must preserve wording equivalent to:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- rejected evidence excluded
- weak evidence remains warning-marked
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- coverage limitations remain visible
- audit trace is available

## Unsafe Claim Policy

The reviewer must reject or request revision for wording that implies:

- complete public-opinion truth
- official platform verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- guaranteed PR, legal, business, or public-opinion outcome
- real-world platform action
- automated authenticity verification

## Representative Evidence Safety

Representative evidence included in future exports must be safe and redacted.

It must not include:

- raw author identifiers
- profile URLs
- private messages
- cookie values
- token values
- session identifiers
- API key values
- `.env` values
- password values
- email addresses
- phone numbers
- personal account identifiers

When in doubt, the reviewer should choose `privacy_hold`.

## Export Mode Policy

The export gate may record candidate future export modes:

- Markdown export candidate
- PDF export candidate
- briefing deck outline candidate
- evidence appendix package candidate

These are future candidates only. The gate itself must not generate, save, or publish files.

## Audit Requirement

Every decision must be audit-visible and append-only.

The audit should record:

- reviewer label
- decision
- reason
- required revisions or blocked reasons
- boundary checklist result
- audit refs
- downstream no-side-effect flags

