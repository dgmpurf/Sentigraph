# Dedup Group Review Completion Gate Design v1

## Purpose

The Dedup Group Review Completion Gate evaluates whether all preview-only duplicate group candidates in a review-only dedup preview have enough human group review to proceed to a future analysis-ready promotion gate design.

The gate answers only one question:

Are dedup group candidates reviewed enough to design the next promotion gate?

## Core Principle

Dedup group review completion is not production dedup.

Dedup group review completion is not an Evidence Layer write.

Dedup group review completion is not production case creation.

Dedup group review completion is not analysis.

Dedup group review completion is not report generation.

Dedup group review completion is not official verification.

Provider output remains evidence, not truth. A confirmed group remains review-only and must not amplify risk, sentiment, coverage, or report conclusions.

## Non-Goals

This design does not implement:

- runtime code
- production dedup
- Evidence Layer writes
- production case creation
- production Evidence Review Queue creation
- analysis
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
- real LLM review
- trust upgrade
- official verification

## Required Prior Chain

The completion gate can be considered only after:

- Review-only Case exists.
- Review Queue Completion Gate passed.
- Dedup Preview exists and status is `preview_ready`.
- Dedup Group Review actions exist where group status changed.
- No group has unresolved privacy risk.
- No group is treated as production merged.
- All review-only queue items remain `analysis_included=false`.
- Prior gates keep production side-effect flags false.
- Rejected review-only items and rejected groups remain audit-visible but excluded from future promotion consideration.

If any prior gate is missing, unsafe, or inconsistent, this gate must return `incomplete`, `blocked`, or `privacy_hold`.

## Gate Purpose

The gate only answers:

- Are dedup group candidates reviewed enough to design the next promotion gate?
- Are review statuses and audit records complete enough for future promotion-gate evaluation?
- Are blockers such as privacy hold, unresolved source requests, or unsafe amplification risk still present?

It does not answer:

- Can analysis run now?
- Can a report be generated now?
- Are duplicates merged in production?
- Is evidence verified?
- Is this full-web coverage?
- Is this full-platform coverage?
- Can evidence be written to the Evidence Layer?

## Output Statuses

### `complete_enough_for_future_promotion_gate_design`

All duplicate group candidates are in statuses that are acceptable for future promotion gate consideration, required audits exist, no privacy hold is present, and no group can amplify risk.

This status still does not make anything analysis-ready.

### `incomplete`

At least one group still requires review, split resolution, more source material, or missing audit records. The next step should remain human review or audit repair.

### `blocked`

The gate found an unsafe state, inconsistent audit, forbidden side-effect flag, may-amplify-risk group, unresolved blocker, or other state that cannot proceed until fixed.

### `privacy_hold`

Any group, group audit, or related review-only item indicates raw/private/secret-like field risk. All downstream gates must stop until privacy review resolves the issue.

## Completion Criteria

The gate may return `complete_enough_for_future_promotion_gate_design` only when:

- every group candidate has a recognized group status
- no group status is `review_needed`
- no group status is `needs_more_source`
- no group status is `privacy_hold`
- no group has `may_amplify_risk=true`
- every non-`review_needed` group status has at least one valid audit record
- `confirmed` groups remain review-only
- `marked_weak` groups carry weak warning
- `rejected` groups are excluded from future promotion
- `representative_changed` groups have a valid latest audit
- `split` groups are resolved by future subgroup metadata, or otherwise remain incomplete
- all review-only queue items remain `analysis_included=false`

## Boundary Language

Use:

- dedup group review completion gate
- future promotion gate consideration
- confirmed group is still review-only
- duplicate evidence must not amplify risk
- `analysis_included=false`
- audit-visible
- weak warning
- rejected excluded
- provider output is evidence, not truth

Avoid:

- production dedup completed
- Evidence Layer merged
- evidence verified
- analysis-ready
- report-ready
- official verified
- risk score updated
- full-web coverage

