# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.3

## 1. Purpose and Scope

This document establishes Baseline v1.3 after Baseline v1.2 exhausted its
narrow risk buffer. It preserves the historical MVP12-F02 and
MVP12-CHG-002-P1 `needs_fix` outcomes, closes v1.2 for future Prompt
accounting, and selects a durable synthetic-tested exact-target read-only audit
helper before one separately approved fresh exact-target audit.

This is a docs-only governance contract. It does not authorize or perform code
or test changes, runtime or target access, SQLite work, payload or receipt
access, a writer call, persistence, reconciliation, repair, production, or
downstream activity.

```text
decision = ready
privacy_issue_stop = no
docs_only = yes
baseline_v1_3_status = candidate_effective_pending_chatgpt_acceptance
```

## 2. Baseline Identity and Approval

```text
baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_3
baseline_version = 1.3
baseline_scope = internal_alpha_mvp_v1_F02_post_exception_target_state_recovery_and_remaining_completion
baseline_status = candidate_effective_pending_baseline_commit_and_chatgpt_acceptance
baseline_project_state_anchor = 441602dd459c70ac7ff0cbecc803e1fa5edee8dd
baseline_rebaseline_reason = v1_2_risk_buffer_exhausted_with_F02_writer_exception_and_unclassified_exact_target_state
baseline_v1_3_rebaseline_governance_prompt_consumed = 1
baseline_v1_3_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
exact_rebaseline_approval_received = yes
exact_rebaseline_approval_match = yes
approval_phrase_sha256 = a1347dc2027c9b8a40b7a3a666da8c08ea2694fa411f7139e0f152e44bdb00ba
```

The project-state anchor identifies the committed CHG-001 engineering state
used by this rebaseline. The future Baseline v1.3 commit SHA cannot be embedded
before that commit exists. Git history and the final Codex receipt provide the
SHA after ready-only commit and push.

## 3. Baseline v1.2 Historical Closure

Baseline v1.2 is historical, closed for future Prompt accounting, and remains
immutable. Its consumption is neither reset, transferred, erased, nor
reclassified by v1.3. Baselines v1.1 and v1.0 remain older immutable historical
ledgers.

```text
baseline_version = 1.2
baseline_status = historical_closed_for_future_prompt_accounting_after_risk_buffer_exhaustion
baseline_v1_2_final_committed_engineering_anchor = 441602dd459c70ac7ff0cbecc803e1fa5edee8dd
historical_v1_2_engineering_prompts_consumed = 4
historical_v1_2_fixed_prompts_consumed = 2
historical_v1_2_conditional_prompts_consumed = 0
historical_v1_2_risk_prompts_consumed = 2
historical_v1_2_fixed_prompts_remaining_at_closure = 12
historical_v1_2_conditional_allowance_remaining_at_closure = 6
historical_v1_2_risk_buffer_remaining_at_closure = 0
historical_v1_2_risk_buffer_exhausted = yes
historical_consumption_reset = no
historical_milestones_reclassified = no
```

Arithmetic and closure checks:

```text
historical_v1_2_engineering_prompts_consumed = 2_fixed + 0_conditional + 2_risk = 4
historical_v1_2_remaining_allowance_at_closure = 12_fixed + 6_conditional + 0_risk
v1_3_governance_prompt_added_to_v1_2_engineering_consumption = no
```

## 4. Preserved Historical Reports

The two historical reports are added to Git without byte changes and retain
their original failure classifications.

| Historical report | Size | SHA-256 | Preserved state |
| --- | ---: | --- | --- |
| `docs/health/sentigraph_mvp12_f02_one_fresh_bounded_f08_remediation_nonproduction_persistence_execution_report_v1_0.md` | 7410 | `eb0eae1db9ff0ce3552134206c38a7467b918331a1a7db4f311b750c277e2946` | MVP12-F02 terminal needs-fix |
| `docs/health/sentigraph_mvp12_chg_002_p1_f02_public_writer_raised_post_exception_exact_target_read_only_state_and_safe_exception_provenance_audit_report_v1_0.md` | 12291 | `90fa8f145725e679d52c5a5b18409897b5384f6ab5083d4913cfc71c62d8e4d8` | CHG-002-P1 audit terminal not ready |

```text
historical_reports_modified = no
historical_reports_reclassified = no
historical_reports_superseded = no
```

## 5. Preserved Historical MVP12-F02 State

```text
historical_MVP12_F02_decision = needs_fix
historical_MVP12_F02_status = terminal_needs_fix
historical_MVP12_F02_completed = no
historical_MVP12_F02_reclassified_as_success = no
historical_MVP12_F02_safe_error_code = public_writer_raised
historical_MVP12_F02_payload_successful_open_count = 1
historical_MVP12_F02_payload_read_call_count = 1
historical_MVP12_F02_payload_reopen_count = 0
historical_MVP12_F02_payload_second_read_count = 0
historical_MVP12_F02_payload_seek_count = 0
historical_MVP12_F02_payload_read_session_consumed = yes
historical_MVP12_F02_public_writer_invocation_count = 1
historical_MVP12_F02_writer_retry_count = 0
historical_MVP12_F02_writer_receipt_returned = no
historical_MVP12_F02_cross_binding_proof_created = no
historical_MVP12_F02_F07_activation_execution_use_consumed = yes
historical_MVP12_F02_fresh_writer_use_consumed = yes
historical_MVP12_F02_outer_latch_implementation_mutating_attempt_consumed = no
```

The outer-latch false value means only that no receipt-bound proof transition
completed. It does not prove the actual database mutating-attempt state.

```text
actual_implementation_mutating_attempt_consumed = unknown_not_safely_classified
actual_attempt_reservation_state = unknown_not_safely_classified
actual_governed_record_state = unknown_not_safely_classified
current_target_state = not_inspected_by_this_rebaseline
current_target_emptiness_claimed = no
current_sidecar_state_claimed = no
historical_MVP_F08_status = terminal_needs_fix
historical_MVP_F08_reclassified = no
production_evidenceitem_created = no
production_case_changed = no
downstream_runtime_called = no
```

The historical F02 field `target_sidecars_absent_after_writer = yes` has this
governance status:

```text
historical_post_writer_sidecar_claim_status = unsupported_as_post_exception_state_evidence_due_to_no_post_exception_target_inspection
```

The historical report is not altered. Baseline v1.3 does not use that field as
current target-state evidence.

## 6. Preserved Historical MVP12-CHG-002-P1 State

```text
historical_MVP12_CHG_002_P1_decision = needs_fix
historical_MVP12_CHG_002_P1_status = audit_terminal_not_ready
historical_MVP12_CHG_002_P1_completed = no
historical_MVP12_CHG_002_P1_reclassified = no
historical_MVP12_CHG_002_P1_safe_error_code = one_shot_audit_terminated_before_safe_classification
one_shot_audit_process_executed_count = 1
one_shot_audit_process_rerun_count = 0
bounded_safe_summary_returned = no
target_accessed = not_safely_proven
target_database_opened = not_safely_proven
sidecar_state = not_obtained
record_count = not_obtained
reservation_count = not_obtained
exact_row_validation = not_completed
exact_empty_state_proven = no
exact_expected_reservation_only_proven = no
exact_expected_reservation_and_record_proven = no
audit_outcome = inconsistent_or_not_safely_classifiable_exact_target_state
original_writer_exception_class = unavailable_from_preserved_evidence
original_writer_exact_exception_callsite = not_proven
MVP12_CHG_002_P1_rerun_allowed = no
```

This report is historical failure evidence. It does not prove that the target
is inconsistent; it proves only that the one-shot audit did not safely classify
the target. Baseline v1.3 makes no target-state inference from that process.

## 7. Selected Recovery Architecture

```text
selected_recovery_architecture = durable_synthetic_tested_exact_target_read_only_audit_helper_then_one_fresh_exact_target_read_only_audit
ephemeral_one_shot_audit_driver_selected = no
direct_fresh_target_reaudit_before_helper_acceptance = no
payload_or_writer_reexecution_selected = no
target_repair_or_reconciliation_selected = no
planned_owner_module = backend/app/services/governed_nonproduction_exact_target_read_only_audit.py
planned_focused_test_module = backend/app/tests/test_governed_nonproduction_exact_target_read_only_audit.py
planned_result_schema = sentigraph_governed_nonproduction_exact_target_read_only_audit_result_v0_1
```

The architecture separates two milestones:

1. Durable helper implementation and synthetic acceptance.
2. One later exact-target runtime audit after separate approval.

The helper must return a bounded, value-safe result for every expected
fail-closed condition. It must not depend on an ephemeral script producing its
final summary outside a durable tested contract.

## 8. Baseline v1.3 Prompt Budget

```text
baseline_v1_3_rebaseline_governance_prompt_consumed = 1
baseline_v1_3_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
consumed_engineering_prompts_since_v1_3_baseline = 0
consumed_fixed_prompts_since_v1_3 = 0
consumed_conditional_prompts_since_v1_3 = 0
consumed_risk_prompts_since_v1_3 = 0
inherited_downstream_fixed_prompt_allowance = 12
new_known_recovery_fixed_prompt_allowance = 2
fixed_prompt_budget = 14
conditional_prompt_allowance = 6
risk_buffer_prompt_allowance = 2
remaining_fixed_prompts = 14
remaining_conditional_allowance = 6
remaining_risk_buffer = 2
best_case_remaining_prompts = 14
controlled_ceiling_remaining_prompts = 20
hard_ceiling_remaining_without_another_rebaseline = 22
```

Arithmetic:

```text
fixed_prompt_budget = 12 + 2 = 14
controlled_ceiling_remaining_prompts = 14 + 6 = 20
hard_ceiling_remaining_without_another_rebaseline = 14 + 6 + 2 = 22
```

No historical v1.2 consumption is transferred, erased, reset, or reclassified.
A budget entry is not runtime authorization and cannot bypass a sequence gate.

## 9. Known Recovery Fixed Milestone MVP13-F01

```text
milestone = MVP13-F01
title = Durable Synthetic-tested Exact-target Read-only Audit Helper
prompt_count = 1
status = not_started
authorized = no
executed = no
planned_scope_classification = synthetic_only_helper_code_tests_and_health_report
planned_owner_module = backend/app/services/governed_nonproduction_exact_target_read_only_audit.py
planned_focused_tests = backend/app/tests/test_governed_nonproduction_exact_target_read_only_audit.py
planned_health_report = docs/health/sentigraph_mvp13_f01_durable_synthetic_exact_target_read_only_audit_helper_report_v1_0.md
planned_result_schema = sentigraph_governed_nonproduction_exact_target_read_only_audit_result_v0_1
```

MVP13-F01 must implement and synthetic-test:

- one explicit target path with no discovery, fallback, glob, walk, or
  directory enumeration;
- the exact logical target label and exact two-table allowlist;
- the exact three-sidecar preflight;
- SQLite URI `mode=ro`, connection-local `query_only`, and a restrictive
  authorizer, without `immutable=1`;
- no initialization, writer, or mutation API;
- actual-column reconstruction and canonical-hash recomputation;
- exact expected reservation and record binding checks;
- no unrelated row acceptance;
- bounded, value-safe, stage-aware failure results;
- no physical path, query text, row, payload, identity mapping, exception text,
  or stack trace in its result;
- zero writer, mutation-helper, payload, or capture-receipt callsites.

Synthetic tests must use temporary SQLite and synthetic sidecar fixtures only.
MVP13-F01 must not access the repository runtime target.

Required result classifications:

```text
exact_empty
exact_expected_reservation_only
exact_expected_reservation_and_record
inconsistent_or_not_safely_classifiable
sidecar_present_read_prohibited
target_identity_or_metadata_blocked
bounded_read_only_failure
```

The helper must distinguish task completion from target-state outcome. A
bounded D/inconsistent classification may still mean the helper worked
correctly.

## 10. Known Recovery Fixed Milestone MVP13-F02

```text
milestone = MVP13-F02
title = One Fresh Exact-target Read-only Audit Using the Accepted Durable Helper
prompt_count = 1
status = not_started
authorized = no
executed = no
planned_scope_classification = one_exact_target_read_only_audit_no_payload_no_writer_no_mutation
```

MVP13-F02 may be considered only after MVP13-F01 is committed, independently
accepted by ChatGPT, and followed by a fresh exact human approval.

MVP13-F02 may use one exact target, one accepted durable helper invocation,
exact sidecar metadata checks, bounded read-only SQLite inspection, exact
reservation/record classification, and one safe audit report.

It must not access a payload, capture receipt, source package, or row; invoke a
writer; retry; mutate, initialize, repair, reconcile, clean, migrate, or delete
target state; or create production/downstream objects.

An MVP13-F02 audit task may be `ready` when the accepted helper returns one
complete bounded classification, including D/inconsistent. Its separate field
must be:

```text
target_state_outcome = independently_reported_bounded_classification
```

`audit_task_decision = ready` must never be conflated with exact successful
persistence.

## 11. Target-state Branches After MVP13-F02

These branches are non-authorizing planning directions:

| Outcome | Proven state | Future governance direction |
| --- | --- | --- |
| A | Exact empty | Writer-exception diagnosis plus entirely new activation/execution governance |
| B | Exact expected reservation only | Mutating attempt consumed; no second INSERT; missing-record recovery governance |
| C | Exact expected reservation plus exact expected record | Receiptless state reconciliation and latch/governance recovery |
| D | Inconsistent, unsafe, sidecar-present, or not classifiable | Pause and separate governance decision |

The branches are not authorized by Baseline v1.3, are not part of MVP13-F01
implementation or MVP13-F02 execution, do not automatically authorize MVP-F09,
and may require conditional, risk, or later rebaseline allocation.

## 12. Inherited Downstream Fixed Plan

The twelve inherited fixed Prompts remain reserved but blocked behind
successful recovery governance:

| Inherited milestone | Prompt count | v1.3 initial state |
| --- | ---: | --- |
| MVP-F09 Independent Post-write Integrity, Idempotency, and Recovery Audit | 1 | blocked, unauthorized |
| MVP-F10 Governed Record to Internal Review Console Integration | 2 | blocked, unauthorized |
| MVP-F11 Governed Record to Controlled Analysis Input Bridge | 2 | blocked, unauthorized |
| MVP-F12 Controlled Opinion Ecosystem and Dense Graph Execution | 1 | blocked, unauthorized |
| MVP-F13 Human-reviewable Internal Result/Report and Operator Continuity | 2 | blocked, unauthorized |
| MVP-F14 C-demo Final Continuity and Comprehension Regression | 1 | blocked, unauthorized |
| MVP-F15 Local Operations, Cleanup, Pause, and Recovery Package | 1 | blocked, unauthorized |
| MVP-F16 Final Integrated Internal Alpha Validation Package | 1 | blocked, unauthorized |
| MVP-F17 Internal Alpha Completion Decision and Source Synchronization | 1 | blocked, unauthorized |
| **Total inherited downstream fixed Prompts** | **12** | |

The two known recovery Prompts and twelve inherited Prompts equal the fixed
budget of fourteen. MVP-F09 is not eligible merely because MVP13-F02 completes
its audit task. Eligibility requires independent acceptance of the target-state
outcome and a separate branch-specific governance decision.

## 13. Sequence Hard Gate

```text
Baseline v1.3 commit
-> ChatGPT independent acceptance
-> Project Source synchronization
-> fresh exact MVP13-F01 approval
-> one MVP13-F01 synthetic implementation
-> ChatGPT independent acceptance
-> fresh exact MVP13-F02 approval
-> one MVP13-F02 exact-target read-only audit
-> ChatGPT independent acceptance
-> separate branch-specific governance decision
-> only then consider reconciliation, repair, execution, or MVP-F09
```

Forbidden sequence shortcuts:

- automatic progression;
- reuse of MVP12-F02 or MVP12-CHG-002-P1 approval;
- rerunning the old one-shot audit;
- direct target access before accepted MVP13-F01;
- combining helper implementation and exact-target audit;
- payload reread or writer retry;
- target mutation or repair;
- use of conditional or risk allowance to bypass the sequence;
- automatic MVP-F09 eligibility.

This baseline contains no future approval phrase or ready-to-sign template.

## 14. Current Business and Authorization State

```text
latest_valid_business_checkpoint = MVP-F07 exact nonproduction persistence gate activation decision effective_but_execution_use_consumed
latest_committed_engineering_checkpoint = MVP12-CHG-001-P1 ambiguous-receipt proof compatibility repair
latest_committed_repo_checkpoint = 441602dd459c70ac7ff0cbecc803e1fa5edee8dd
MVP12_F01_effective_completion = yes_via_MVP12_CHG_001_P1
historical_MVP12_F02_status = terminal_needs_fix
historical_MVP12_CHG_002_P1_status = audit_terminal_not_ready
F07_activation_execution_use_consumed = yes
fresh_MVP12_F02_writer_use_consumed = yes
historical_MVP12_F02_payload_session_consumed = yes
actual_implementation_mutating_attempt_consumed = unknown_not_safely_classified
actual_attempt_reservation_state = unknown_not_safely_classified
actual_governed_record_state = unknown_not_safely_classified
current_target_state_inspected_by_baseline_v1_3 = no
MVP13_F01_eligible_after_chatgpt_acceptance_and_source_sync = yes
MVP13_F01_authorized = no
MVP13_F01_executed = no
MVP13_F02_authorized = no
MVP13_F02_executed = no
MVP_F09_eligible = no
MVP_F09_authorized = no
MVP_F09_executed = no
actual_write_execution_authorized_now = no
writer_retry_authorized = no
target_repair_authorized = no
production_evidenceitem_creation_authorized = false
production_evidenceitem_created = no
production_case_changed = no
downstream_runtime_called = no
8W_69_pause_preserved = yes
production_analysis_result_authorized = no
public_or_customer_delivery_authorized = no
```

## 15. Rebaseline Governance Rules

1. Baseline v1.2 remains immutable historical accounting.
2. Baseline v1.3 becomes current only after commit and independent ChatGPT
   acceptance.
3. Historical v1.2 consumption is not reset, transferred, or erased.
4. MVP13-F01 and MVP13-F02 consume fixed Prompts only when their separately
   approved Goals activate.
5. Conditional and risk allowances cannot bypass the hard sequence.
6. A bounded audit task may complete when target outcome is D if the accepted
   helper safely classifies it.
7. No target-state inference may be made from failed one-shot audits.
8. Exhausting the v1.3 risk buffer requires another governance decision before
   further unplanned work.
9. Prompt availability does not authorize runtime access.
10. Completion requires evidence and independent ChatGPT acceptance.

## 16. No-side-effect State

```text
docs_only = yes
code_changed = no
tests_changed = no
runtime_accessed = no
target_or_sidecar_metadata_accessed = no
SQLite_accessed = no
protected_payload_or_capture_receipt_accessed = no
source_package_row_candidate_author_or_URL_accessed = no
persistence_writer_imported_or_called = no
candidate_or_reservation_mutation_performed = no
target_initialized_repaired_reconciled_cleaned_or_migrated = no
production_or_downstream_object_created = no
Project_Source_changed = no
```

## 17. Baseline Lifecycle, Source Recommendation, and Next Boundary

```text
baseline_v1_3_status = candidate_effective_pending_chatgpt_acceptance
historical_v1_2_status = historical_closed_for_future_prompt_accounting
current_target_state = unknown_not_safely_classified
next_boundary = ChatGPT_independent_acceptance_of_Baseline_v1_3_and_Project_Source_synchronization
Project_Source_update_recommended_after_ChatGPT_acceptance = yes
Canonical_00_recommendation = replace
Canonical_03_recommendation = replace
Canonical_09_recommendation = replace
Canonical_05_recommendation = no_change
Source_11_recommendation = no_change
next_engineering_milestone = MVP13-F01
MVP13_F01_authorized_now = no
```

Codex does not modify Project Source in this task. After independent ChatGPT
acceptance, Source synchronization occurs outside this repository change. No
runtime, target, SQLite, payload, writer, repair, or downstream action is the
next automatic step.
