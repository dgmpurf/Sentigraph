# Manual Analysis Trigger Contract v1

## Purpose

This document defines the future Manual Analysis Trigger object shape.

The object records a human trigger decision over a promoted review-only candidate set. It is a design contract only and must not be treated as implemented runtime.

## Future Object

```json
{
  "schema": "sentigraph_manual_analysis_trigger_v1",
  "manual_trigger_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "promotion_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "trigger_decision": "trigger_analysis|hold|cancel",
  "status": "trigger_ready_for_future_runtime|incomplete|blocked|privacy_hold|cancelled",
  "analysis_scope": {
    "source": "review_only_promoted_set",
    "include_item_ids": [],
    "include_group_ids": [],
    "exclude_item_ids": [],
    "exclude_group_ids": [],
    "weak_warning_item_ids": [],
    "weak_warning_group_ids": [],
    "analysis_input_source": "review_only_promoted_candidates",
    "analysis_included_after_runtime": "future_runtime_only"
  },
  "required_warnings": {
    "coverage_limitations": [],
    "weak_evidence_warnings": [],
    "dedup_preview_warnings": [],
    "provider_output_is_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true
  },
  "now_flags": {
    "write_evidence_layer_now": false,
    "create_production_case_now": false,
    "create_production_review_queue_now": false,
    "run_production_dedup_now": false,
    "run_analysis_now": false,
    "generate_report_now": false,
    "generate_sandbox_now": false,
    "generate_public_event_now": false
  },
  "readiness": {
    "can_run_analysis_now": false,
    "eligible_for_future_analysis_runtime": false,
    "requires_manual_runtime_implementation": true,
    "requires_result_boundary_gate": true
  },
  "blocked_reasons": [],
  "warnings": [],
  "boundary_notes": [],
  "recommended_next_steps": []
}
```

## Field Definitions

`schema` identifies this future contract.

`manual_trigger_id` is the unique future trigger record id.

`request_id` links back to the original Analysis Request.

`review_case_id` links to the review-only case.

`promotion_gate_id` links to the successful Analysis-ready Promotion Gate output.

`created_at` records when the future trigger record is created.

`created_by` records the human or local operator label. It must not store private credentials.

`trigger_decision` records whether the human wants to trigger future analysis, hold, or cancel.

`status` records whether the trigger is ready for future runtime, incomplete, blocked, held for privacy, or cancelled.

`analysis_scope` lists candidate items and groups for future runtime. It does not mark them analyzed and does not write production state.

`analysis_scope.source` must be `review_only_promoted_set`.

`include_item_ids` lists item candidates that may be included by a future runtime.

`include_group_ids` lists dedup group representatives or groups that may be included by a future runtime.

`exclude_item_ids` lists items that must remain excluded.

`exclude_group_ids` lists groups that must remain excluded.

`weak_warning_item_ids` lists item candidates that can be included only with weak-evidence warnings.

`weak_warning_group_ids` lists group candidates that can be included only with weak-evidence warnings.

`analysis_input_source` describes the intended future input source for analysis.

`analysis_included_after_runtime` must remain `future_runtime_only` in this design phase.

`required_warnings` carries warnings that must be preserved into future analysis and result boundary gates.

`coverage_limitations` records known coverage limits, such as selected sample, imported evidence only, or not full-platform coverage.

`weak_evidence_warnings` records weak or low-trust evidence warnings.

`dedup_preview_warnings` records duplicate grouping limitations and non-amplification rules.

`provider_output_is_evidence_not_truth` must remain true.

`not_official_verification` must remain true unless a separate future verification gate changes it.

`not_full_web_coverage` must remain true.

`now_flags` records side effects that are forbidden in this design phase. All values must be false.

`readiness.can_run_analysis_now` must be false because this phase is design-only.

`readiness.eligible_for_future_analysis_runtime` is false in the design object until a future runtime validates the trigger.

`readiness.requires_manual_runtime_implementation` must be true.

`readiness.requires_result_boundary_gate` must be true because result generation needs another boundary check.

`blocked_reasons` lists unsafe or missing prerequisites.

`warnings` lists non-blocking issues that must be surfaced to users.

`boundary_notes` records human-readable safety boundaries.

`recommended_next_steps` suggests safe next actions without executing them.

## Required Invariants

- No `now_flags` value may be true.
- Rejected items and groups must not appear in include lists.
- Privacy-held items and groups must not appear in include lists.
- Duplicate groups must not amplify sentiment, risk, coverage, or conclusion strength.
- Weak items and groups must stay warning-marked.
- Trust labels must not be upgraded by this object.
- Verification status must not be upgraded by this object.

