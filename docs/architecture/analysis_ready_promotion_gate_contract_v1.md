# Analysis-ready Promotion Gate Contract v1

## Purpose

This contract defines the future object shape for an Analysis-ready Promotion Gate result.

The object is a governance gate result. It is not an analysis result, production Evidence Layer write, production case, report, Sandbox output, or official verification.

## Object Shape

```json
{
  "schema": "sentigraph_analysis_ready_promotion_gate_v1",
  "promotion_gate_id": "promotion_gate_...",
  "request_id": "req_...",
  "review_case_id": "review_only_case_...",
  "queue_init_id": "review_queue_init_...",
  "completion_gate_id": "review_queue_completion_gate_...",
  "dedup_preview_id": "dedup_preview_...",
  "dedup_group_completion_gate_id": "dedup_group_completion_gate_...",
  "created_at": "2026-06-20T00:00:00Z",
  "created_by": "sentigraph_local_ui",
  "status": "eligible_for_future_manual_analysis_trigger_design|incomplete|blocked|privacy_hold",
  "input_scope": {
    "source": "review_only_case_governance_chain",
    "analysis_included": false,
    "provider_output_is_truth": false,
    "official_verification": false
  },
  "counts": {
    "candidate_items_seen": 0,
    "items_eligible_for_future_analysis": 0,
    "items_excluded_rejected": 0,
    "items_warning_weak": 0,
    "items_blocked_needs_more_source": 0,
    "items_blocked_privacy": 0,
    "confirmed_dedup_groups": 0,
    "rejected_dedup_groups": 0,
    "weak_dedup_groups": 0
  },
  "readiness": {
    "eligible_for_future_manual_analysis_trigger": false,
    "can_run_analysis_now": false,
    "can_generate_report_now": false,
    "can_generate_sandbox_now": false,
    "requires_manual_analysis_trigger_phase": true,
    "requires_human_promotion_decision": true
  },
  "promotion_set_preview": {
    "item_ids": [],
    "group_ids": [],
    "excluded_item_ids": [],
    "warning_item_ids": [],
    "coverage_limitations_acknowledged": false
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

Constant value: `sentigraph_analysis_ready_promotion_gate_v1`.

### `promotion_gate_id`

Unique local identifier for the promotion gate evaluation.

This id must not be treated as a production case id, analysis id, or Evidence Layer write id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case container id. The case remains internal and review-only.

### `queue_init_id`

Review Queue Initialization id used as part of the governance chain.

### `completion_gate_id`

Review Queue Completion Gate id. It must have passed before this promotion gate can be considered.

### `dedup_preview_id`

Dedup Preview id. The dedup preview must be `preview_ready`.

### `dedup_group_completion_gate_id`

Dedup Group Review Completion Gate id. It must be `complete_enough_for_future_promotion_gate_design`.

### `created_at`

UTC timestamp for the gate evaluation.

### `created_by`

Local UI or reviewer label. It must not contain secrets or private account identifiers.

### `status`

One of:

- `eligible_for_future_manual_analysis_trigger_design`
- `incomplete`
- `blocked`
- `privacy_hold`

Eligibility is only for future manual analysis trigger consideration. It is not an analysis run.

### `input_scope`

Defines the conservative input boundary:

- `source`: always `review_only_case_governance_chain`
- `analysis_included`: false in this gate
- `provider_output_is_truth`: false
- `official_verification`: false

### `counts`

Preview counts for eligibility and exclusions.

Counts are governance metadata only. They must not update risk, sentiment, coverage, or reports.

### `readiness`

Readiness flags must remain conservative:

- `eligible_for_future_manual_analysis_trigger`: true only when status is eligible
- `can_run_analysis_now`: always false in this phase
- `can_generate_report_now`: always false in this phase
- `can_generate_sandbox_now`: always false in this phase
- `requires_manual_analysis_trigger_phase`: always true
- `requires_human_promotion_decision`: always true

### `promotion_set_preview`

Preview of the candidate set that may later be passed to a Manual Analysis Trigger phase.

It must not mark any item as analysis-included now.

- `item_ids`: item ids considered eligible for future manual analysis trigger
- `group_ids`: dedup group ids considered eligible or warning-marked
- `excluded_item_ids`: rejected, blocked, or privacy-held item ids excluded from future promotion
- `warning_item_ids`: weak or warning-marked item ids
- `coverage_limitations_acknowledged`: whether selected-sample and coverage limits were acknowledged

### `blocked_reasons`

Reasons preventing eligibility, such as `privacy_hold`, `needs_more_source`, `missing_audit`, `dedup_group_incomplete`, `may_amplify_risk`, or `coverage_not_acknowledged`.

### `warnings`

Warnings that must be carried into future manual analysis trigger, such as weak evidence, selected public sample limits, rejected exclusions, and dedup group limitations.

### `boundary_notes`

Human-readable safety notes. Required notes should include:

- Promotion gate does not run analysis.
- Promotion gate does not write the Evidence Layer.
- Provider output is evidence, not truth.
- Duplicate evidence must not amplify risk.
- Coverage is limited and acknowledged.
- Manual analysis trigger is a later separate phase.

### `recommended_next_steps`

Suggested next actions:

- resolve blockers
- complete audits
- acknowledge coverage limitations
- prepare human promotion decision
- proceed to future Manual Analysis Trigger design or runtime

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

