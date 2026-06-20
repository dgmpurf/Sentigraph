# Promotion Input Readiness Matrix v1

## Purpose

This matrix defines how review-only items and dedup group statuses should be interpreted by a future Analysis-ready Promotion Gate.

No row in this matrix makes evidence production-imported, officially verified, analysis-run, report-ready, or full-web coverage.

## Item Readiness Matrix

| Input state | Promotion consideration | Required audit | Analysis effect now | Notes |
| --- | --- | --- | --- | --- |
| Approved review queue item | Eligible only if not rejected, not privacy hold, and not needs more source | Required | None | Still `analysis_included=false`. |
| Marked weak item | Eligible only with warning | Required | None | Weak evidence warning must carry forward. |
| Rejected item | Completed exclusion state | Required | None | Excluded from promotion set preview. |
| Needs more source | Incomplete or blocked | Required | None | Cannot proceed until resolved. |
| Privacy hold | Privacy hold | Required | None | Blocks promotion. |

## Group Readiness Matrix

| Group state | Promotion consideration | Required audit | Analysis effect now | Notes |
| --- | --- | --- | --- | --- |
| Confirmed dedup group | Eligible as review-only duplicate group candidate | Required | None | Does not mean production dedup completed. |
| Marked weak group | Eligible only with group-level weak warning | Required | None | Must not upgrade trust. |
| Rejected group | Completed exclusion state | Required | None | Excluded from promotion. |
| Split group | Incomplete unless resolved subgroup metadata exists | Required | None | Future runtime may support subgroup review. |
| Representative changed group | Acceptable only if audit complete and representative is valid | Required | None | Representative must be within `item_ids`. |
| Needs more source group | Incomplete or blocked | Required | None | Cannot proceed until resolved. |
| Privacy hold group | Privacy hold | Required | None | Blocks promotion. |
| Review needed group | Incomplete | Not required yet | None | Human group review still needed. |

## Detailed Item Rules

### Approved Review Queue Item

- Eligible only if not rejected, not `privacy_hold`, and not `needs_more_source`.
- Must remain `analysis_included=false`.
- Must have review action audit.
- Must retain coverage and trust limitations.

### Marked Weak Item

- Eligible only with weak warning.
- Must carry weak evidence warning into future analysis trigger.
- Must not upgrade trust.
- Must not become official verification.

### Rejected Item

- Completed review state but excluded from promotion.
- Remains audit-visible.
- Must not appear in the future manual analysis trigger input set.

### Needs More Source

- Incomplete or blocked until resolved.
- Cannot be included in the promotion set preview.

### Privacy Hold

- Causes `privacy_hold` gate status.
- Blocks promotion.
- Requires privacy review before any later analysis consideration.

## Detailed Group Rules

### Confirmed Dedup Group

- Eligible only as review-only duplicate group candidate.
- Does not mean production dedup completed.
- Duplicate count cannot amplify risk.
- Confirmed group remains audit-visible.

### Marked Weak Group

- Eligible only with group-level weak warning.
- Weak warning must carry into future manual analysis trigger.

### Rejected Group

- Completed review state but excluded from promotion.
- Related rejected group ids should remain audit-visible.

### Split Group

- Incomplete unless resolved subgroup metadata exists.
- If only a split status exists, promotion gate should remain incomplete.

### Representative Changed Group

- Acceptable only if audit is complete.
- `representative_item_id` must be inside `item_ids`.
- Representative selection is not official verification.

## Cross-Cutting Blockers

Any raw/private/secret-like field is blocked or privacy hold.

Forbidden examples include:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- private message values
- cookie / token / session values
- API key values
- `.env` values
- password-like values
- email or phone-like values

These terms are allowed here only as detection and exclusion rules.

Any `may_amplify_risk=true` group is blocked.

Any attempt to set `analysis_included=true` before manual analysis trigger is blocked.

## Count Policy

- Rejected items/groups are excluded.
- Weak items/groups are warning-marked.
- Duplicate evidence must not multiply risk, sentiment, or coverage.
- Promotion counts are preview metadata only.

