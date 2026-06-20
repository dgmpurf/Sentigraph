# Summary Report Candidate Section Policy v1

## Purpose

This policy defines the required sections and forbidden claims for any future `SummaryReportCandidate`.

The candidate should help a reviewer understand a bounded analysis result without implying final report readiness, official verification, or full coverage.

## Required Sections

### Executive Summary Candidate

Must summarize the bounded result in candidate-only language.

Required language:

- local candidate
- reviewed evidence scope
- not a final report
- limitations apply

Must not claim:

- official verified
- full-web coverage
- full-platform coverage
- complete public opinion
- causal proof

### Evidence Scope

Must disclose:

- review-only case id
- included item count
- included group count
- weak evidence count
- rejected evidence excluded count
- duplicate group count
- selected or available evidence scope
- coverage limitations

Counts must not be framed as full-web, all-platform, or all-thread totals.

### Coverage Limitation

Must explicitly state:

- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not official platform verification
- not complete public opinion

### Source / Provider Statement

Must explain the source path without overclaiming:

- provider output is evidence, not truth
- user-provided or provider-provided data may require review
- Search Discovery and mock providers are not live verification
- vendor-attested data is not official platform verification unless separately proven

### Provider Output Is Evidence, Not Truth

Must include the rule as a visible section or note:

Provider output is evidence, not truth.

The section must avoid truth-certification language.

### Not Official Verification

Must state that neither the candidate nor its upstream evidence is official verification unless a separately approved official API/source explicitly supports that claim.

### Not Full-Web / Full-Platform / Full-Thread Coverage

Must state all three boundaries:

- not full-web coverage
- not full-platform coverage
- not full-thread coverage

### Weak Evidence Warning

Must disclose weak, low-trust, unverified, or manually entered evidence when present.

Weak evidence may be included only with warning language. It must not be silently upgraded.

### Rejected Evidence Excluded

Must state that rejected evidence is excluded by default.

Rejected evidence may remain audit-visible, but it must not be included in representative evidence, sentiment, risk, or topic conclusions.

### Duplicate Evidence Does Not Amplify Risk

Must state that duplicate evidence is collapsed or governed.

Duplicate group size may be shown as density or repetition context, but it must not multiply sentiment, risk, coverage, or conclusions.

### Privacy / Needs-More-Source Exclusions

Must disclose that privacy-held, private, raw-identifier, secret-like, and unresolved needs-more-source items are excluded or blocked.

The candidate must not display:

- raw author identifiers
- profile URLs
- private messages
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- email addresses or phone numbers

### Audit Trace

Must include audit references to:

- manual analysis execution
- analysis result boundary gate
- report generation gate

Future implementations may also include review, dedup, and promotion audit references when available.

### Candidate-Only Status

Must state:

- candidate only
- not final Summary Report
- no PDF, Markdown, or briefing deck generated
- no B-end report generated
- no Sandbox or public event generated

### Limitations and Confidence Notes

Must include:

- source coverage limitations
- weak evidence caveats
- dedup caveats
- review caveats
- any missing-source or deferred-source caveats
- no causal proof language

## Forbidden Claims

Future candidates must not say or imply:

- official verified
- official platform certified
- full-web coverage
- all-platform coverage
- full-thread coverage
- complete public opinion
- causal proof
- report finalized
- PDF ready
- Markdown ready
- briefing deck ready
- public event ready
- Sandbox ready
- B-end report ready
- legal guarantee
- PR guarantee
- user persuasion guarantee
- real-world action executed

## Reader Tone

Use conservative report language:

- "candidate"
- "bounded evidence"
- "reviewed sample"
- "available/imported evidence"
- "risk signal"
- "requires human review"
- "confidence note"

Avoid absolute language:

- "truth"
- "all users"
- "entire platform"
- "proves"
- "guarantees"
- "officially verified"
- "complete capture"

## Section Readiness

A future runtime should block candidate creation if it cannot populate the required boundary sections.

It should prefer `blocked` over creating a candidate that lacks warnings, audit references, rejected-evidence exclusion, dedup non-amplification, or coverage limitation.
