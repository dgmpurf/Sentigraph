# Report Generation Input Boundary Policy v1

## Purpose

This policy defines what a future Report Generation Gate and report candidate runtime may read, and what it must not read.

The policy protects Sentigraph from accidentally turning provider output, review-only data, or analysis candidates into overclaimed reports.

## Allowed Input Source

Report generation may use only:

- `ManualAnalysisResultCandidate` metadata
- the candidate boundary block
- safe representative evidence already included in the candidate
- included and excluded counts already included in the candidate
- warning metadata already included in the candidate
- audit references already included in the candidate

Report generation must not expand the input scope.

## Allowed Safe Representative Evidence

Safe representative evidence may include only data already carried by the candidate:

- representative evidence id
- platform label
- evidence type
- title preview
- body or comment preview
- source URL presence indicator
- safe source URL if already present in the candidate
- trust label
- verification status
- review status
- duplicate group id
- duplicate count as context only
- exclusion reason
- warning flags

Representative evidence must not be used to infer raw identity, private message content, or unreviewed source rows.

## Prohibited Inputs

Report generation must not:

- read original package rows
- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- parse vendor raw files
- parse collector raw files
- fetch URLs
- call provider jobs
- call collector jobs
- call external APIs
- call real LLMs
- inspect browser profile state
- inspect login state
- inspect cookie, token, session, API key, `.env`, password, email, or phone values
- inspect `raw_author_id`
- inspect `raw_author_name`
- inspect `profile_url`
- inspect private messages

If any future runtime requires more evidence, it must return a blocker or request another reviewed upstream gate. It must not silently widen the input scope.

## Prohibited Side Effects

Report generation must not:

- write Evidence Layer records
- create production cases
- create production review queues
- upgrade trust labels
- upgrade verification status
- include rejected evidence
- remove weak-evidence warnings
- amplify duplicate groups
- remove audit references
- run production dedup
- run analysis
- generate Sandbox fixtures
- generate public event pages
- generate B-end reports
- export PDF, Markdown, or briefing deck files

## Boundary Requirements

Any future report candidate must preserve:

- boundary block
- coverage limitation
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- weak evidence warning
- rejected evidence exclusion
- duplicate evidence non-amplification
- privacy exclusion note
- needs-more-source exclusion note
- audit trace
- candidate-only status

## Block Conditions

The gate must return `blocked` or `privacy_hold` if:

- the candidate boundary block is missing
- rejected evidence appears in report input
- duplicate counts are used as risk, sentiment, or truth strength
- weak evidence warnings are missing
- coverage limitations are missing
- audit trace references are missing
- source scope is overclaimed
- provider output is described as truth
- official verification is implied
- full-web or full-platform coverage is implied
- raw identifiers or secret-like values are present

## Reader Boundary Copy

Future report readers should see copy equivalent to:

> This report candidate is based on a reviewed evidence scope. Provider output is evidence, not truth. It is not official verification, not full-web coverage, and not full-platform coverage. Rejected evidence is excluded. Weak evidence and duplicate handling remain visible.

## Future Runtime Recommendation

Future 7I should implement this policy as a read-scope validator before any report candidate is created.

The validator should fail closed. If a field or source is not explicitly allowed, it should be treated as out of scope.
