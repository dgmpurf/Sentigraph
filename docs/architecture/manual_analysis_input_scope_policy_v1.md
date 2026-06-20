# Manual Analysis Input Scope Policy v1

## Purpose

This policy defines what a future Manual Analysis Trigger may consider as analysis input after Analysis-ready Promotion Gate approval.

The policy is design-only. It does not parse evidence rows, import evidence, write Evidence Layer records, or run analysis.

## Source Of Included Evidence

Included evidence must come only from `promotion_set_preview`.

The trigger must not read original package rows, private collector state, browser sessions, external URLs, or raw platform data.

The trigger must not expand its scope beyond the promoted review-only candidate set.

## Scope Categories

### `include_for_analysis_candidate`

Items or groups approved by the promotion gate that may enter a future analysis runtime.

They remain candidates until a future runtime and result boundary gate execute.

### `exclude_rejected`

Rejected items and rejected groups must remain excluded.

They may stay audit-visible, but they must not influence analysis, reports, risk, sentiment, or coverage counts.

### `exclude_privacy`

Items or groups with privacy blockers must be excluded.

Privacy exclusion is a hard stop until a separate privacy review resolves it.

### `exclude_needs_more_source`

Items or groups marked as needing more source must be excluded unless a later review and audit clears the blocker.

### `include_with_weak_warning`

Weak items or weak groups may be included only with visible warnings.

The warning must travel into analysis context, result boundary checks, and any later report or Sandbox gate.

### `include_as_duplicate_group_representative`

Confirmed duplicate groups may contribute through a representative item or group.

The group size can be shown as evidence density, but it must not multiply risk, sentiment, coverage, or conclusion strength.

### `include_as_context_only`

Some safe items may be included only as context, for example timeline background or source coverage context.

Context-only items must not drive sentiment, risk, or conclusion scoring.

## Required Rules

- Rejected items and groups must remain excluded.
- Weak items and groups may be included only with warnings.
- Duplicate groups must not amplify counts.
- Duplicate count must be treated as context or density, not truth strength.
- Provider output remains evidence, not truth.
- `source_url_provided_unverified` remains unverified unless a separate future verification gate changes it.
- Trust labels cannot be upgraded by the analysis trigger.
- Verification status cannot be upgraded by the analysis trigger.
- No raw author identifiers may enter analysis.
- No private content may enter analysis.
- Coverage limitation must be passed into analysis context.
- All source and coverage notes must remain visible in downstream result boundaries.

## Duplicate And Coverage Handling

Future analysis should count duplicate groups as unique representatives by default.

Duplicate group size may be carried as a separate context signal. It must not be interpreted as truth strength or risk certainty.

Coverage limitation text must be preserved when data comes from:

- selected public samples
- user uploads
- provider output
- vendor samples
- local package previews
- search discovery candidates
- any non-full-platform evidence source

## Forbidden Inputs

The future trigger must not include:

- rejected items
- rejected groups
- privacy-held items
- privacy-held groups
- unresolved source-blocked items
- unresolved source-blocked groups
- raw identity fields
- private messages
- credential-like values
- original collector rows
- externally fetched page content

## Boundary Copy

Future UI or runtime should display:

- This analysis input is based on reviewed promoted candidates, not full-web coverage.
- Provider output is evidence, not truth.
- Weak evidence remains warning-marked.
- Duplicate evidence is collapsed or represented to avoid amplification.
- Rejected evidence is excluded by default.

