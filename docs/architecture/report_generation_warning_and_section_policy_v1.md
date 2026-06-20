# Report Generation Warning And Section Policy v1

## Purpose

This policy defines required warning sections and forbidden claims for any future report candidate generated from a `ManualAnalysisResultCandidate`.

Reports are reader-facing, so they must be more explicit about boundaries than internal analysis objects.

## Required Report Warning Sections

### Coverage Limitation

The report must state that the analysis covers reviewed and available evidence only.

It must not imply full-web, full-platform, full-thread, or all-community coverage.

### Selected Or Reviewed Evidence Scope

The report must explain the source scope used for the candidate, including whether evidence came from user upload, manual URL entry, provider package handoff, Search Discovery mock metadata, or another governed source.

### Provider Output Is Evidence, Not Truth

The report must state that provider output and collector packages are evidence inputs, not truth guarantees.

### Not Official Verification

The report must state that Sentigraph has not officially verified platform authenticity unless a separate official verification gate exists.

### Not Full-Web, Full-Platform, Or Full-Thread Coverage

The report must include a clear boundary that results do not represent all public opinion, all posts, all comments, all users, or the whole web.

### Weak Evidence Warning

The report must disclose weak, low-trust, unverified, or marked-weak evidence.

Weak evidence may be summarized, but the warning must remain visible.

### Rejected Evidence Excluded

The report must state that rejected evidence was excluded from analysis and report conclusions by default.

### Duplicate Evidence Does Not Amplify Risk

The report must state that duplicate evidence was handled as duplicate groups or representatives and must not multiply risk, sentiment, coverage, or conclusions.

Group size may be shown as evidence density or repetition context, not truth strength.

### Privacy And Needs-More-Source Exclusions

The report must disclose privacy exclusions and needs-more-source exclusions when present.

Privacy-held material must not appear in report text.

### Audit Trace

The report must reference available review, dedup, promotion, analysis execution, and boundary gate audit records.

### Candidate-Only Status

The report candidate must state that it is a candidate or future report input until a final report runtime and export gate approve a specific output.

### No Automatic Public Event, Sandbox, Or B-End Export

The report candidate must state that it does not automatically create a public event page, Sandbox fixture, PDF export, Markdown export, briefing deck, or B-end report.

## Required Report Sections

A future Summary Report Candidate should include:

- executive summary
- evidence scope
- boundary block
- coverage limitation
- key findings with caution wording
- weak evidence warning
- rejected evidence exclusion
- dedup non-amplification note
- provider output evidence-not-truth note
- not official verification note
- not full-web/full-platform/full-thread coverage note
- audit trace
- limitations
- safe next steps

## Forbidden Report Claims

Future reports must not claim:

- official verified
- full-web coverage
- all-platform coverage
- complete public opinion
- public truth conclusion
- causality proven
- production evidence merged
- report generated automatically
- PDF ready
- Markdown ready
- briefing deck ready
- public event ready
- Sandbox ready
- B-end report ready without a B-end gate
- legal guarantee
- public-relations guarantee
- risk score updated from all data
- screenshots or transcriptions verified automatically
- real-world action executed

## Wording Guidance

Use:

- reviewed evidence scope
- selected sample
- available evidence
- evidence candidate
- report candidate
- boundary note
- warning-marked evidence
- rejected evidence excluded
- duplicate group context
- not official verification
- not full-web coverage
- audit trace available

Avoid:

- public truth
- official verified
- full public opinion
- all comments
- all platforms
- causality proven
- automatic report
- production merged
- guaranteed forecast
- guaranteed PR outcome

## Escalation Rules

The future gate must block report candidate creation if:

- any required warning section is missing
- the candidate tries to hide weak evidence warnings
- the candidate includes rejected evidence
- the candidate treats duplicate count as truth strength
- the candidate removes coverage limitations
- the candidate lacks audit trace references
- the candidate uses forbidden claims
- privacy-held material appears in report text
- secret-like or raw identifier fields appear in report text

## Reader-Friendly Boundary Example

> This report candidate summarizes reviewed evidence available to Sentigraph. It is not full-web coverage, not full-platform coverage, and not official verification. Provider output is treated as evidence, not truth. Rejected evidence was excluded, weak evidence remains warning-marked, and duplicate evidence does not amplify risk or sentiment.
