# Final Summary Report Review Policy v1

## Purpose

This policy defines how humans should review a `SummaryReportCandidate` before any future final Summary Report runtime may be considered.

The policy exists because a candidate can be well structured but still unsuitable for final report formatting if it drops warnings, overstates coverage, contains unsafe representative evidence, lacks audit trace, or implies verification that Sentigraph does not have.

## Human Review Requirement

Human review is required before future final report runtime.

The reviewer must confirm:

- report candidate sections are present
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
- audit trace is visible
- no raw, private, or secret-like fields are present

Approval is only approval for a future final runtime to consider the candidate. It is not final report generation.

## Required Section Review

The reviewer should inspect:

- executive summary candidate
- evidence scope section
- analysis summary section
- risk and topic section
- representative evidence section
- boundary block
- limitations
- warnings
- audit trace

If any section is missing or misleading, the reviewer should choose `request_revision` or `block`.

## Representative Evidence Review

Representative evidence must be safe preview content only.

It must not include:

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

If unsafe content is present, the decision must be `privacy_hold` unless the issue is clearly a harmless boundary-field mention in documentation or schema text.

## Boundary Review

The reviewer must confirm the candidate still says:

- provider output is evidence, not truth
- this is not official verification
- this is not full-web coverage
- this is not full-platform coverage
- this is not full-thread coverage
- weak evidence remains warning-marked
- rejected evidence remains excluded
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- downstream export, B-end report, Sandbox, and public event outputs require separate gates

Boundary language must be visible to future readers or downstream gate operators.

## Possible Decisions

### `approve_for_future_final_runtime`

The candidate is ready for a future final Summary Report runtime to consider.

This decision does not:

- generate a final Summary Report
- generate export files
- generate a B-end report
- generate Sandbox fixtures
- generate public event pages
- write Evidence Layer
- create production cases

### `request_revision`

The candidate needs human or future runtime revision before final runtime.

This decision must list required revisions. It does not rewrite the candidate automatically.

### `block`

The candidate has unsafe, inconsistent, misleading, or incomplete content that should not proceed.

Examples include missing required sections, missing audit trace, rejected-evidence leakage, duplicate amplification, full-web overclaim, official-verification overclaim, or missing weak-evidence warning.

### `privacy_hold`

The candidate contains privacy, private-content, raw-identifier, secret-like, or contact-data risk.

This decision blocks all downstream use until separate privacy review resolves the issue.

## Audit Requirements

Every future review action must append audit history with:

- review gate id
- summary report candidate id
- reviewer label
- decision
- note
- required revisions
- blocked reasons
- preserved boundary notes
- downstream side-effect flags, all false
- safe-mode flags

The audit record must be append-only.

## What Approval Does Not Mean

Approval does not mean:

- final Summary Report generated
- report facts are officially verified
- coverage is full-web, full-platform, or full-thread
- provider output is truth
- duplicate evidence strengthens factual certainty
- weak evidence is upgraded
- rejected evidence can be used
- export files are ready
- B-end report is ready
- Sandbox or public event is ready

## Reviewer Wording Guidance

Use:

- approved for future final runtime
- candidate remains non-final
- warnings preserved
- limited reviewed evidence scope
- evidence, not truth
- human-reviewed boundary

Avoid:

- report finalized
- official verified
- complete public opinion
- full-web conclusion
- causal proof
- export ready
- B-end ready
- public-ready

