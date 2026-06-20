# Dedup Group Status Readiness Matrix v1

## Purpose

This matrix defines how each preview-only duplicate group status should be interpreted by the future Dedup Group Review Completion Gate.

The matrix is conservative. No status makes evidence production-merged, verified, analysis-ready, or report-ready.

## Status Matrix

| Group status | Future promotion gate consideration | Required audit | Analysis effect now | Notes |
| --- | --- | --- | --- | --- |
| `confirmed` | Acceptable | Required | None | Still review-only; still not production dedup. |
| `representative_changed` | Conditionally acceptable | Required | None | Representative must be within `item_ids`; warning recommended if not also confirmed. |
| `marked_weak` | Acceptable with warning | Required | None | Must carry weak evidence warning; must not upgrade trust. |
| `rejected` | Completed exclusion state | Required | None | Excluded from future promotion; remains audit-visible. |
| `split` | Usually incomplete | Required | None | Incomplete unless split metadata defines resolved subgroups and subgroup review state. |
| `needs_more_source` | Incomplete or blocked | Required | None | Cannot proceed to promotion gate until resolved or explicitly deferred by a later policy. |
| `privacy_hold` | Privacy hold | Required | None | Blocks all downstream gates. |
| `review_needed` | Incomplete | Not required yet | None | Human group review has not completed. |

## Detailed Status Rules

### `confirmed`

- Acceptable for future promotion gate consideration.
- Still not production dedup.
- Still not analysis-ready.
- Must have at least one valid audit record.
- Must keep `may_amplify_risk=false`.
- Must keep all related review-only queue items `analysis_included=false`.

### `representative_changed`

- Acceptable only if the latest action audit exists.
- `representative_item_id` must be within group `item_ids`.
- May need a warning if the group is not also confirmed by a future action.
- Does not imply the representative has been verified.
- Does not alter item analysis state.

### `marked_weak`

- Acceptable only with weak warning.
- Remains warning-marked.
- Must not become high trust.
- Must not become official verification.
- Future promotion gate must carry weak evidence warning.

### `rejected`

- Acceptable as a completed review state.
- Must be excluded from future promotion.
- Remains audit-visible.
- Must not be deleted only to make counts look cleaner.

### `split`

- Incomplete unless split metadata defines resolved subgroups.
- If runtime only records split status without creating reviewed subgroups, treat as incomplete for promotion gate.
- Future runtime may support split subgroup review.
- Split must not silently delete or hide original group candidates.

### `needs_more_source`

- Incomplete or blocked.
- Cannot proceed to promotion gate until the source issue is resolved or a future explicit deferral policy exists.
- Must remain visible in audit and recommended next steps.

### `privacy_hold`

- `privacy_hold` gate status.
- Blocks all downstream gates.
- Requires privacy review before any future promotion consideration.
- Must not expose raw/private/secret-like values in UI, logs, reports, or docs.

### `review_needed`

- Incomplete.
- Indicates human group review is still required.
- No future promotion gate should be considered until this status changes or is explicitly handled by a future policy.

## Cross-Cutting Blockers

Any group with `may_amplify_risk=true` is blocked.

Any group or item with raw/private/secret-like fields is blocked or privacy hold.

Forbidden examples include:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- private message fields
- cookie / token / session values
- API key values
- `.env` values
- password-like values
- email or phone-like values

These terms are listed as forbidden detection targets, not as allowed stored content.

## Count Policy

- Confirmed or rejected states may count toward review completion.
- Rejected groups must be excluded from future promotion.
- Weak groups may be considered only with warning.
- Duplicate group size may be evidence density, not truth strength.
- Duplicate evidence must not multiply sentiment, risk, coverage, or conclusions.

