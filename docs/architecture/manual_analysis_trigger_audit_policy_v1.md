# Manual Analysis Trigger Audit Policy v1

## Purpose

This policy defines the future append-only audit record required before any Manual Analysis Trigger runtime can execute.

The audit makes the human decision visible and preserves the safety boundaries around promoted review-only evidence.

This document does not implement runtime and does not run analysis.

## Future Audit Object

```json
{
  "schema": "sentigraph_manual_analysis_trigger_audit_v1",
  "manual_trigger_audit_id": "...",
  "manual_trigger_id": "...",
  "promotion_gate_id": "...",
  "review_case_id": "...",
  "decision": "trigger_analysis|hold|cancel",
  "reviewer_label": "...",
  "decided_at": "...",
  "note": "...",
  "included_item_ids": [],
  "excluded_item_ids": [],
  "weak_warning_item_ids": [],
  "included_group_ids": [],
  "excluded_group_ids": [],
  "coverage_acknowledgement": true,
  "privacy_acknowledgement": true,
  "dedup_warning_acknowledgement": true,
  "provider_output_is_evidence_not_truth_acknowledgement": true,
  "analysis_effect": "future_runtime_only",
  "now_flags": {
    "run_analysis_now": false,
    "write_evidence_layer_now": false,
    "generate_report_now": false,
    "generate_sandbox_now": false,
    "generate_public_event_now": false
  }
}
```

## Field Definitions

`schema` identifies the audit contract.

`manual_trigger_audit_id` is the append-only audit event id.

`manual_trigger_id` links to the future trigger decision object.

`promotion_gate_id` links to the promotion gate output that made the trigger eligible.

`review_case_id` links to the review-only case.

`decision` records whether the human chose to trigger future analysis, hold, or cancel.

`reviewer_label` records a non-sensitive reviewer label.

`decided_at` records the decision time.

`note` captures the human review note. It must not include private data or credentials.

`included_item_ids` records item candidates included in the future scope.

`excluded_item_ids` records item candidates excluded from the future scope.

`weak_warning_item_ids` records items that require weak-evidence warnings.

`included_group_ids` records dedup groups included in the future scope.

`excluded_group_ids` records dedup groups excluded from the future scope.

`coverage_acknowledgement` records that coverage limitations were acknowledged.

`privacy_acknowledgement` records that privacy boundaries were acknowledged.

`dedup_warning_acknowledgement` records that duplicate non-amplification warnings were acknowledged.

`provider_output_is_evidence_not_truth_acknowledgement` records that the reviewer acknowledged the evidence-not-truth boundary.

`analysis_effect` must remain `future_runtime_only` in this design.

`now_flags` records forbidden side effects. All values must be false.

## Audit Requirements

- Audit is append-only.
- Trigger design does not run analysis.
- Trigger audit must be created before any future runtime analysis execution.
- Missing audit blocks future analysis runtime.
- Audit with unsafe side-effect flags blocks future analysis runtime.
- Audit must preserve included, excluded, weak-warning, and dedup-scope decisions.
- Audit must preserve coverage, privacy, dedup, and provider-output acknowledgements.

## Blocking Conditions

Future runtime must block when:

- audit is missing
- audit was overwritten instead of appended
- coverage acknowledgement is false
- privacy acknowledgement is false
- dedup warning acknowledgement is false
- provider-output acknowledgement is false
- a rejected item or group appears in included lists
- a privacy-held item or group appears in included lists
- any `now_flags` value is true
- audit attempts trust upgrade, official verification, report generation, Sandbox generation, or public event generation

## Boundary Language

Use:

- append-only trigger audit
- human decision
- future runtime only
- coverage acknowledged
- rejected excluded
- weak evidence warning
- duplicate non-amplification acknowledged

Avoid:

- analysis executed
- report generated
- production case updated
- evidence verified
- full-web coverage
- automatic analysis

