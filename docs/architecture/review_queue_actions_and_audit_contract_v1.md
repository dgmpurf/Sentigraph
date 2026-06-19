# Review Queue Actions And Audit Contract v1

## Purpose

This document defines future human review actions for review-only queue items and the append-only audit record each action must create.

Human review decisions guide later gates. They do not automatically run analysis, deduplication, reporting, Sandbox generation, or production promotion.

## Review Actions

### approve

Meaning: reviewer accepts the item as eligible for later gates.

Allowed previous statuses:

- `review_needed`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`

New status: `approved`

Effects:

- `analysis_included` remains false
- `trust_label` may remain `medium_low` unless later policy allows a conservative upgrade
- audit record required
- item may proceed to a future dedup preview gate
- item must remain excluded from analysis until a later promotion gate

### reject

Meaning: reviewer rejects the item for future analysis/promotion.

Allowed previous statuses:

- `review_needed`
- `approved`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`

New status: `rejected`

Effects:

- `analysis_included=false`
- `trust_label` may become `rejected`
- audit record required
- item cannot proceed to dedup except as audit-visible excluded evidence
- rejected evidence remains excluded from analysis and reports

### mark_weak

Meaning: reviewer considers the item potentially useful but weak, incomplete, or low-confidence.

Allowed previous statuses:

- `review_needed`
- `approved`
- `needs_more_source`

New status: `marked_weak`

Effects:

- `analysis_included=false`
- `trust_label` remains `medium_low` or becomes `low`
- audit record required
- item may proceed only as warning-marked material in later gates
- item must remain excluded from analysis until later promotion logic explicitly handles weak evidence

### request_more_source

Meaning: reviewer needs source context, better URL traceability, safer provenance, or additional explanation.

Allowed previous statuses:

- `review_needed`
- `approved`
- `marked_weak`

New status: `needs_more_source`

Effects:

- `analysis_included=false`
- `trust_label` remains `medium_low` or lower
- audit record required
- item cannot proceed to dedup or promotion
- item remains excluded from analysis

### merge_duplicate

Meaning: reviewer identifies the item as a duplicate or near-duplicate that must not amplify risk.

Allowed previous statuses:

- `review_needed`
- `approved`
- `marked_weak`

New status: `duplicate_merged`

Effects:

- `analysis_included=false`
- `trust_label` unchanged unless weak/rejected policy applies
- audit record required
- item may proceed to dedup preview only with duplicate context
- duplicate evidence must not amplify risk or sentiment counts

### hold_for_privacy_review

Meaning: reviewer detected possible privacy, safety, or source risk.

Allowed previous statuses:

- `review_needed`
- `approved`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`

New status: `privacy_hold`

Effects:

- `analysis_included=false`
- `trust_label` may become `unverified` or `rejected`
- audit record required
- item cannot proceed downstream
- item remains excluded from analysis

### reset_review

Meaning: reviewer returns the item to review-needed state while preserving prior audit history.

Allowed previous statuses:

- `approved`
- `rejected`
- `marked_weak`
- `needs_more_source`
- `duplicate_merged`
- `privacy_hold`

New status: `review_needed`

Effects:

- `analysis_included=false`
- trust label should return to the conservative default unless policy says otherwise
- audit record required
- old decisions must not be deleted
- item remains excluded from analysis

## Audit Object

```json
{
  "schema": "sentigraph_review_queue_action_audit_v1",
  "audit_id": "review_audit_...",
  "review_item_id": "review_item_...",
  "review_case_id": "review_case_...",
  "previous_status": "review_needed",
  "new_status": "approved",
  "action": "approve",
  "reviewer_label": "local_reviewer",
  "reviewed_at": "2026-06-19T00:00:00Z",
  "note": "Source URL present; still unverified and excluded from analysis.",
  "analysis_effect": "eligible_for_future_dedup",
  "trust_label_before": "medium_low",
  "trust_label_after": "medium_low"
}
```

## Analysis Effects

`analysis_effect` may be:

- `still_excluded`
- `eligible_for_future_dedup`
- `blocked`

No review action directly sets `analysis_included=true`.

## Required Audit Rules

Every action must:

- append a new audit record
- preserve previous decisions
- include `reviewer_label`
- include `reviewed_at`
- record previous and new queue status
- record trust label before and after
- record analysis effect
- avoid raw author identifiers and private messages

The audit timeline is a governance record. It is not official verification and not a public report.

