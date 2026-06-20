# Analysis-ready Promotion Gate Design v1

## Purpose

The Analysis-ready Promotion Gate decides whether a review-only case can be considered for a later Manual Analysis Trigger phase.

It evaluates reviewed, audited, dedup-reviewed, privacy-safe, coverage-limited evidence candidates after the review-only governance chain has completed enough prior gates.

The gate answers only this question:

Can this review-only case be considered eligible for a future manual analysis trigger design or runtime?

## Core Principle

Analysis-ready promotion gate is not analysis.

Analysis-ready promotion gate is not an Evidence Layer write.

Analysis-ready promotion gate is not production case creation.

Analysis-ready promotion gate is not report generation.

Analysis-ready promotion gate is not official verification.

Analysis-ready promotion gate is not automatic trust upgrade.

Provider output remains evidence, not truth. Promotion eligibility means only that a later manual analysis trigger may be considered.

## Required Prior Chain

Promotion gate can be considered only after:

- Review-only Case exists.
- Review-only Staging Import exists.
- Review Queue Initialization exists.
- Review Action Audit exists.
- Review Queue Completion Gate passed.
- Dedup Preview exists and status is `preview_ready`.
- Dedup Group Review exists.
- Dedup Group Review Completion Gate status is `complete_enough_for_future_promotion_gate_design`.
- No `privacy_hold` blockers exist.
- No unresolved `needs_more_source` blockers exist.
- Rejected items and rejected groups are excluded.
- Weak items and weak groups remain warning-marked.
- Coverage limitations are acknowledged.
- Audit timeline is complete.
- Human promotion decision is explicitly required.
- All review-only items remain `analysis_included=false`.

If any prior gate is missing, unsafe, incomplete, or inconsistent, the promotion gate must return `incomplete`, `blocked`, or `privacy_hold`.

## Non-Goals

This design does not implement:

- runtime code
- analysis trigger
- production Evidence Layer write
- production case creation
- production review queue
- production dedup
- report generation
- Sandbox fixture generation
- public event page generation
- B-end report generation
- provider execution
- collector job execution
- live collection
- URL fetching
- scraping
- real API integration
- real LLM
- trust upgrade
- official verification

## Output Statuses

### `eligible_for_future_manual_analysis_trigger_design`

Prior governance gates are complete enough for a future Manual Analysis Trigger design or runtime to be considered.

This status still does not run analysis and does not mark items `analysis_included=true`.

### `incomplete`

Required review, dedup group review, audit, coverage acknowledgement, or human promotion decision preparation is incomplete.

### `blocked`

Unsafe state exists, such as unresolved source blockers, audit inconsistency, side-effect flags, `may_amplify_risk=true`, or attempted trust/verification upgrade.

### `privacy_hold`

Raw/private/secret-like field risk is present. All downstream gates must stop until privacy review resolves the issue.

## Promotion Eligibility Rules

The gate may be eligible for future manual analysis trigger design only when:

- candidate items are approved or warning-marked, not rejected
- rejected items and groups are excluded from the promotion set preview
- weak items and groups carry warnings
- confirmed dedup groups remain review-only
- duplicate evidence cannot amplify risk, sentiment, coverage, or conclusions
- coverage limitations are acknowledged
- audit timeline is append-only and complete
- no item or group has privacy hold
- no item or group needs more source
- all `now_flags` remain false
- human promotion decision is required before any future manual analysis trigger

## Boundary Language

Use:

- analysis-ready promotion gate
- eligible for future manual analysis trigger
- `analysis_included=false` until manual trigger
- rejected excluded
- weak warning
- duplicate evidence must not amplify risk
- provider output is evidence, not truth
- audit-visible
- coverage limitation acknowledged

Avoid:

- analysis completed
- production Evidence imported
- production case created
- report generated
- official verified
- full-web coverage
- risk score updated
- auto analysis

