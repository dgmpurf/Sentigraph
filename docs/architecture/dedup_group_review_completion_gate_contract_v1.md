# Dedup Group Review Completion Gate Contract v1

## Purpose

This contract defines the future object shape for evaluating whether review-only duplicate group candidates are complete enough for future analysis-ready promotion gate design.

The object is a gate result, not production dedup output.

## Object Shape

```json
{
  "schema": "sentigraph_dedup_group_review_completion_gate_v1",
  "group_completion_gate_id": "dedup_group_completion_gate_...",
  "request_id": "req_...",
  "review_case_id": "review_only_case_...",
  "dedup_preview_id": "dedup_preview_...",
  "created_at": "2026-06-20T00:00:00Z",
  "created_by": "sentigraph_local_ui",
  "status": "complete_enough_for_future_promotion_gate_design|incomplete|blocked|privacy_hold",
  "counts": {
    "total_group_candidates": 0,
    "review_needed": 0,
    "confirmed": 0,
    "split": 0,
    "representative_changed": 0,
    "marked_weak": 0,
    "rejected": 0,
    "needs_more_source": 0,
    "privacy_hold": 0,
    "groups_with_audit": 0,
    "groups_missing_audit": 0
  },
  "readiness": {
    "eligible_for_future_analysis_ready_promotion_gate_design": false,
    "can_run_production_dedup_now": false,
    "can_run_analysis_now": false,
    "can_generate_report_now": false,
    "requires_promotion_gate": true,
    "requires_human_promotion_decision": true
  },
  "blocked_reasons": [],
  "warnings": [],
  "boundary_notes": [],
  "recommended_next_steps": [],
  "now_flags": {
    "write_evidence_layer_now": false,
    "create_production_case_now": false,
    "create_production_review_queue_now": false,
    "run_production_dedup_now": false,
    "run_analysis_now": false,
    "generate_report_now": false,
    "generate_sandbox_now": false,
    "generate_public_event_now": false
  }
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_dedup_group_review_completion_gate_v1`.

### `group_completion_gate_id`

Unique local identifier for this completion gate evaluation. It is audit metadata only and must not be used as a production dedup identifier.

### `request_id`

The local file-based Analysis Request id.

### `review_case_id`

The review-only case container id. The case must remain internal and review-only.

### `dedup_preview_id`

The preview-only dedup preview being evaluated.

### `created_at`

UTC timestamp for the gate evaluation.

### `created_by`

Local UI or reviewer label that created the gate evaluation. It must not contain secrets or private account identifiers.

### `status`

One of:

- `complete_enough_for_future_promotion_gate_design`
- `incomplete`
- `blocked`
- `privacy_hold`

The status is about future promotion gate consideration only. It is not analysis-ready status.

### `counts`

Status counts for duplicate group candidates. These counts help reviewers see completion state, but they must not update sentiment, risk, coverage, or report conclusions.

- `total_group_candidates`: all group candidates in the dedup preview
- `review_needed`: groups still awaiting group review
- `confirmed`: groups confirmed as review-only candidates
- `split`: groups marked split
- `representative_changed`: groups where the representative changed
- `marked_weak`: groups warning-marked as weak evidence
- `rejected`: groups excluded from future promotion consideration
- `needs_more_source`: groups requiring more source material
- `privacy_hold`: groups blocked by privacy risk
- `groups_with_audit`: groups with at least one valid group review audit record
- `groups_missing_audit`: groups whose status requires audit but no valid audit is present

### `readiness`

Readiness flags must remain conservative.

- `eligible_for_future_analysis_ready_promotion_gate_design`: true only when the gate status is complete enough for future promotion gate design
- `can_run_production_dedup_now`: always false in this phase
- `can_run_analysis_now`: always false in this phase
- `can_generate_report_now`: always false in this phase
- `requires_promotion_gate`: always true
- `requires_human_promotion_decision`: always true

### `blocked_reasons`

Machine-readable or reviewer-readable reasons that prevent completion, such as `group_review_needed`, `missing_group_audit`, `privacy_hold`, `may_amplify_risk`, or `needs_more_source`.

### `warnings`

Non-blocking warnings that must be carried forward, such as weak evidence warnings, rejected group exclusion, split group limitations, or coverage limitations.

### `boundary_notes`

Human-readable safety notes. Required notes should include:

- Dedup group review completion is not production dedup.
- Evidence remains review-only.
- Duplicate evidence must not amplify risk.
- Provider output is evidence, not truth.
- A future promotion gate and human promotion decision are required.

### `recommended_next_steps`

Suggested next actions, for example:

- continue group review
- resolve `needs_more_source`
- resolve `privacy_hold`
- review split subgroup handling
- proceed to future analysis-ready promotion gate design

### `now_flags`

All flags must remain false:

- `write_evidence_layer_now`
- `create_production_case_now`
- `create_production_review_queue_now`
- `run_production_dedup_now`
- `run_analysis_now`
- `generate_report_now`
- `generate_sandbox_now`
- `generate_public_event_now`

Any true value is a blocker.

