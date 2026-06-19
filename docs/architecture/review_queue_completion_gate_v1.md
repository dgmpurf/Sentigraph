# Review Queue Completion Gate v1

## Purpose

This document defines when a review-only case review queue may be considered complete enough for a later dedup preview gate.

Completion does not mean analysis can run. Completion only means the queue has enough human review state to consider the next gate.

## Completion Requirements

A review queue is not complete until either:

1. all queue items have a non-`review_needed` status, or
2. a minimum review threshold is met and all remaining items are explicitly deferred.

Additionally:

- `privacy_hold` count must be 0
- rejected items must remain excluded
- weak items must be warning-marked
- `needs_more_source` items must not be promoted
- every decision must have an audit record
- coverage limitations must be acknowledged
- `reviewer_label` must be present for all actions
- duplicate candidates must be marked or prepared for later dedup review

## Suggested Summary Object

```json
{
  "schema": "sentigraph_review_queue_completion_summary_v1",
  "review_case_id": "review_case_...",
  "request_id": "analysis_request_...",
  "queue_item_count": 20,
  "review_needed_count": 0,
  "approved_count": 12,
  "rejected_count": 3,
  "marked_weak_count": 3,
  "needs_more_source_count": 2,
  "duplicate_merged_count": 0,
  "privacy_hold_count": 0,
  "audit_complete": true,
  "coverage_limitations_acknowledged": true,
  "completion_state": "complete_for_future_dedup_preview",
  "can_run_analysis_now": false,
  "can_generate_report_now": false,
  "can_generate_sandbox_now": false,
  "can_generate_public_event_now": false
}
```

## Completion Does Not Mean

Completion does not mean:

- analysis can run immediately
- report can generate
- Sandbox can generate
- public event can generate
- production case can be created
- Evidence Layer can be written
- official verification occurred
- trust was upgraded
- full-web or full-platform coverage exists
- risk score was updated

## Completion Allows Only

Completion may allow:

- future dedup preview gate
- future promotion gate consideration
- future analysis-readiness design

Each later phase must still preserve safety boundaries and must block if privacy, source, audit, or duplicate risks remain unresolved.

## Deferred Items

If the queue uses a threshold rule, deferred items must be explicitly marked and excluded from downstream analysis candidates.

Deferred items should include:

- deferral reason
- reviewer label
- reviewed or deferred timestamp
- whether more source is needed
- whether privacy review is required

Deferred items must not silently disappear.

## Coverage Limitation Acknowledgement

Before completion, the reviewer must acknowledge:

- staged evidence is a selected package sample
- it is not full-web coverage
- it is not full-platform coverage
- it is not full-thread coverage
- it is not official verification
- it is not causal proof
- provider output is evidence, not truth

## Blockers

Completion must block if:

- any item is in `privacy_hold`
- audit records are missing
- rejected evidence is still marked as downstream-eligible
- weak evidence lacks warning state
- `needs_more_source` evidence is marked as promoted
- duplicate evidence can amplify risk
- reviewer labels are missing
- coverage limitations are not acknowledged

