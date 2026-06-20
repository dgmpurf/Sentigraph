# Promotion Decision Audit Policy v1

## Purpose

This policy defines the future human promotion decision audit required before a Manual Analysis Trigger phase can be considered.

The audit records a human governance decision. It does not run analysis, write to the Evidence Layer, create production records, generate reports, generate Sandbox output, or create public event pages.

## Required Audit Fields

Future promotion decision audit records should include:

- `promotion_decision_id`
- `promotion_gate_id`
- `request_id`
- `review_case_id`
- `previous_status`
- `new_status`
- `reviewer_label`
- `decided_at`
- `note`
- `included_item_ids`
- `excluded_item_ids`
- `warning_item_ids`
- `included_group_ids`
- `excluded_group_ids`
- `coverage_limitation_acknowledgement`
- `privacy_acknowledgement`
- no-production-side-effect flags
- `analysis_effect = eligible_for_manual_trigger_only`

## Example Shape

```json
{
  "schema": "sentigraph_promotion_decision_audit_v1",
  "promotion_decision_id": "promotion_decision_...",
  "promotion_gate_id": "promotion_gate_...",
  "request_id": "req_...",
  "review_case_id": "review_only_case_...",
  "previous_status": "incomplete",
  "new_status": "eligible_for_future_manual_analysis_trigger_design",
  "reviewer_label": "human_reviewer",
  "decided_at": "2026-06-20T00:00:00Z",
  "note": "Reviewed coverage, privacy, weak evidence warnings, rejected exclusions, and dedup group state.",
  "included_item_ids": [],
  "excluded_item_ids": [],
  "warning_item_ids": [],
  "included_group_ids": [],
  "excluded_group_ids": [],
  "coverage_limitation_acknowledgement": true,
  "privacy_acknowledgement": true,
  "analysis_effect": "eligible_for_manual_trigger_only",
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

## Audit Rules

Promotion decision audit is append-only.

Old decisions must not be deleted.

Reset or replacement decisions must append new audit records.

The audit must preserve:

- included item ids
- excluded item ids
- warning item ids
- included group ids
- excluded group ids
- coverage acknowledgement
- privacy acknowledgement
- reviewer label
- note
- timestamp
- no-production side-effect flags

## Required Acknowledgements

The human promotion decision should acknowledge:

- selected evidence is review-derived
- provider output is evidence, not truth
- rejected items and groups are excluded
- weak items and groups remain warning-marked
- duplicate evidence must not amplify risk
- coverage is limited and not full-web
- coverage is limited and not full-platform
- evidence is not official verification
- manual analysis trigger is a later separate phase

## Missing Audit Behavior

Missing promotion decision audit means the future Manual Analysis Trigger phase must not proceed.

Inconsistent audit means blocked.

Audit with privacy or secret-like values means privacy hold or blocked.

## No-Production Side-Effect Rule

Promotion decision does not run analysis.

Promotion decision does not write Evidence Layer.

Promotion decision does not create production case.

Promotion decision does not create production review queue.

Promotion decision does not run production dedup.

Promotion decision does not create report, Sandbox output, or public event page.

Any audit that claims one of those effects happened must block downstream gates.

