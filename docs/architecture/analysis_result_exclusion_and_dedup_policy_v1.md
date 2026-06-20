# Analysis Result Exclusion And Dedup Policy v1

## Purpose

This policy defines how future Analysis Result generation must handle rejected evidence, privacy exclusions, needs-more-source exclusions, weak evidence, duplicate groups, and representative evidence.

The policy protects result metrics from being inflated by repeated submissions, unsafe evidence, or unresolved review decisions.

This document is design-only and does not run analysis or deduplication.

## Exclusion Rules

### Rejected Evidence

Rejected items and rejected groups must not be included in:

- primary risk metrics
- sentiment metrics
- topic metrics
- representative evidence
- conclusion text
- coverage counts
- Summary Report inputs
- Sandbox inputs
- public event inputs
- B-end report inputs

Rejected evidence remains audit-visible, but not analysis-included.

### Privacy-Hold Evidence

Privacy-held items and groups must not be included in any Analysis Result.

If privacy-held evidence appears in the candidate scope, the boundary gate must return `privacy_hold`.

### Needs-More-Source Evidence

Items and groups marked `needs_more_source` must not be included in result metrics or representative evidence.

They remain audit-visible and may be reconsidered only after a later human review resolves the source requirement.

### Weak Evidence

Weak items and weak groups may be included only when:

- they are not rejected
- they are not privacy-held
- they do not need more source
- they carry visible weak evidence warnings
- they do not receive a trust or verification upgrade

Weak evidence must not be described as verified.

## Deduplication Rules

Duplicate groups must count as one representative for primary risk, sentiment, topic, and coverage metrics.

Duplicate evidence must not multiply:

- risk
- sentiment
- coverage
- trend strength
- conclusion strength
- public heat
- evidence trust

`duplicate_count` may be shown as context, evidence density, or repetition signal only when clearly labeled as non-amplifying.

## Representative Item Selection

Representative selection must be audit-visible.

A future runtime should prefer:

- approved over marked-weak
- no privacy or source blockers
- source URL present
- richer title/body/comment preview
- higher trust label within allowed values
- earlier created_at if otherwise tied
- reviewer-selected representative if future audit supports it

Representative selection must not upgrade trust, verification, or coverage claims.

## Excluded Evidence Visibility

Excluded evidence remains visible in audit and governance views, but not in analysis output metrics or representative examples.

Future result metadata may show aggregate exclusion counts:

- rejected excluded count
- privacy excluded count
- needs-more-source excluded count
- duplicate group count
- weak warning count

The future result must not display raw excluded private content.

## Raw Identifier And Secret Safety

Future Analysis Result output must not display:

- raw_author_id
- raw_author_name
- profile_url
- private message content
- cookie values
- token values
- API key values
- .env values
- password-like values
- email addresses
- phone numbers

If any such field appears in candidate representative evidence, the boundary gate must block or privacy-hold before presentation.

## Metric Policy

Primary metrics must use the included unique representative scope.

Duplicate group size can be shown separately as evidence density, not truth strength.

Weak evidence can affect qualitative warnings, but must not be hidden behind a clean final score.

Coverage counts must describe reviewed evidence scope, not full-web or full-platform coverage.

## Audit Policy

Future result metadata should reference:

- Manual Analysis Trigger id
- Manual Analysis Trigger audit id
- Analysis-ready Promotion Gate id
- Dedup Group Review Completion Gate id
- Dedup group representative decisions
- Review Action audit ids
- exclusion counts and reasons

Audit references must not expose secrets or raw author identifiers.

## Blockers

The boundary gate must block if:

- rejected evidence leaks into included scope
- privacy-held evidence leaks into included scope
- needs-more-source evidence leaks into included scope
- duplicate evidence can amplify primary metrics
- representative item selection is not audit-visible
- weak evidence warning is missing
- raw identifiers are exposed
- private content is exposed
- secret-like values are exposed
- coverage limitations are missing
