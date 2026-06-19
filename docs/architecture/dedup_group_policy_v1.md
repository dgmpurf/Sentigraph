# Dedup Group Policy v1

## Purpose

This policy defines how future dedup preview may group duplicate candidates and how those groups should be interpreted.

Duplicate grouping protects analysis from repeated evidence amplification. It does not verify truth.

## Grouping Rules

### Exact URL Match

Confidence: high.

Rules:

- same safe `source_url`
- no URL fetch
- no network canonicalization
- query stripping only if deterministic and local
- requires human confirmation before downstream effect

### Normalized URL Match

Confidence: medium/high depending on normalization.

Allowed normalization:

- lower-case host
- remove trailing slash
- remove obvious tracking fragments if already local and safe
- preserve path identity

Forbidden normalization:

- URL fetch
- redirect resolution
- external API canonicalization
- login/session/cookie use

### Content Preview Hash Match

Confidence: medium.

Rules:

- compare only `title_preview` and `body_text_preview`
- normalize whitespace
- optionally lower-case for hash comparison
- do not inspect original package rows
- do not use raw author identifiers

### Lineage Match

Confidence: high.

Rules:

- same staging lineage or source preview row lineage
- safe only if lineage fields are already in review-only records
- does not mean the evidence is official truth

### Reviewer Merge Hint

Confidence: medium unless URL/content/lineage also matches.

Rules:

- based on `merge_duplicate` review action metadata
- must remain audit-visible
- must not automatically collapse counts

### Cross-Platform Text-Only Match

Confidence: low.

Rules:

- requires human confirmation
- should not be used to merge automatically
- should be labeled as a weak duplicate candidate
- must not imply coordinated behavior without later evidence

## Weak And Rejected Evidence

Weak evidence can be grouped but remains warning-marked.

Rejected evidence is excluded from dedup preview by default. It may remain audit-visible in review records, but it must not influence future analysis candidates.

## Representative Item Selection

Representative selection should prefer:

1. approved over marked_weak
2. higher allowed `trust_label`
3. source URL present
4. richer title/body preview
5. earliest `created_at` if otherwise tied
6. reviewer-selected representative if a future audit supports it

Representative selection does not upgrade trust and does not verify evidence.

## Count Policy

- `duplicate_count_preview` is only preview metadata.
- `duplicate_count_preview` must not amplify risk.
- `unique_candidate_count` should count groups, not raw items.
- duplicates should not multiply sentiment or risk.
- group size can be shown as evidence density, not truth strength.
- repeated items may be treated as repetition signal only after a later policy gate.

## Blockers

Dedup preview should block on:

- privacy risk
- raw identifiers
- private content
- secret-like values
- missing action audit for reviewed items
- unresolved `needs_more_source`
- `privacy_hold`
- production side-effect attempts
- full-web or full-platform overclaim

## Safe Output Language

Use:

- duplicate group candidate
- preview-only duplicate count
- human confirmation required
- duplicate evidence must not amplify risk
- audit-visible

Avoid:

- dedup completed
- evidence verified
- official duplicate
- production evidence merged
- risk score updated

