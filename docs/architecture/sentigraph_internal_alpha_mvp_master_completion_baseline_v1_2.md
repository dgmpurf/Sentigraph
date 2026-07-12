# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.2

## 1. Purpose and Scope

This document establishes Baseline v1.2 after Baseline v1.1 exhausted its
narrow risk buffer. It preserves the historical MVP-F08 and
MVP-CHG-004-P1A `needs_fix` outcomes, closes v1.1 for future Prompt accounting,
selects the receipt idempotency-key cross-binding recovery architecture, and
places two known recovery milestones ahead of the inherited downstream plan.

This is a docs-only governance contract. It does not authorize or perform code
or test changes, payload or target access, SQLite work, a writer call,
persistence, remediation execution, or production/downstream activity.

```text
decision = ready
privacy_issue_stop = no
docs_only = yes
baseline_v1_2_status = candidate_effective_pending_chatgpt_acceptance
```

## 2. Baseline Identity and Approval

```text
baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_2
baseline_version = 1.2
baseline_scope = internal_alpha_mvp_v1_F08_recovery_and_remaining_completion
baseline_status = candidate_effective_pending_baseline_commit_and_chatgpt_acceptance
baseline_project_state_anchor = 52cbc3f1832e61596b54e58a4c2d80e171b1ba88
baseline_rebaseline_reason = v1_1_risk_buffer_exhausted_with_receipt_cross_binding_and_F08_remediation_recovery_remaining
baseline_v1_2_rebaseline_governance_prompt_consumed = 1
baseline_v1_2_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
exact_rebaseline_approval_received = yes
exact_rebaseline_approval_match = yes
approval_phrase_sha256 = ebb02805d6f198190b1066c85bfb13fe39b59c0a756cb7ead5c2a45c17b81d1e
```

The project-state anchor identifies the committed P1 engineering state used by
this rebaseline. The future Baseline v1.2 commit SHA cannot be embedded before
that commit exists. Git history and the final Codex receipt provide the commit
SHA after ready-only commit and push.

## 3. Baseline v1.1 Historical Closure

Baseline v1.1 is historical, closed for future Prompt accounting, and remains
immutable. Its consumption is neither erased nor transferred into v1.2.

```text
baseline_version = 1.1
baseline_status = historical_closed_for_future_prompt_accounting_after_risk_buffer_exhaustion
baseline_v1_1_final_committed_engineering_anchor = 52cbc3f1832e61596b54e58a4c2d80e171b1ba88
historical_v1_1_engineering_prompts_consumed = 6
historical_v1_1_fixed_prompts_consumed = 4
historical_v1_1_conditional_prompts_consumed = 0
historical_v1_1_risk_prompts_consumed = 2
historical_v1_1_fixed_prompts_remaining_at_closure = 12
historical_v1_1_conditional_allowance_remaining_at_closure = 6
historical_v1_1_risk_buffer_remaining_at_closure = 0
historical_v1_1_risk_buffer_exhausted = yes
historical_consumption_reset = no
historical_milestones_reclassified = no
```

Arithmetic and closure checks:

```text
historical_v1_1_engineering_prompts_consumed = 4 + 0 + 2 = 6
historical_v1_1_remaining_allowance_at_closure = 12_fixed + 6_conditional + 0_risk
v1_2_governance_prompt_added_to_v1_1_engineering_consumption = no
```

## 4. Preserved Historical Reports

The two historical reports are added to Git without byte changes and retain
their original `needs_fix` classifications.

| Historical report | Size | SHA-256 | Preserved state |
| --- | ---: | --- | --- |
| `docs/health/sentigraph_mvp_f08_single_governed_nonproduction_persistence_execution_report_v1_0.md` | 9551 | `db4962a0908924235b7db2a48730025d1165475e3b33636a9ae28580ee1af710` | MVP-F08 terminal needs-fix |
| `docs/health/sentigraph_mvp_chg_004_p1a_f08_outer_execution_latch_receipt_bound_attempt_consumption_transition_repair_report_v1_0.md` | 7254 | `83cc182836707f3b927c7c4c470e79216cb053e0801bb9e1ff126e4584b3276f` | P1A terminal needs-fix before TDD/implementation |

```text
historical_reports_modified = no
historical_reports_reclassified = no
historical_reports_superseded = no
```

## 5. Historical MVP-F08 State

```text
historical_MVP_F08_decision = needs_fix
historical_MVP_F08_status = terminal_needs_fix
historical_MVP_F08_completed = no
historical_MVP_F08_reclassified = no
historical_MVP_F08_payload_open_count = 1
historical_MVP_F08_payload_read_call_count = 1
historical_MVP_F08_payload_reopen_count = 0
historical_MVP_F08_payload_read_session_consumed = yes
historical_MVP_F08_public_writer_invocation_count = 0
historical_MVP_F08_writer_retry_count = 0
historical_MVP_F08_attempt_reservation_commit_count = 0
historical_MVP_F08_base_record_insert_count = 0
historical_MVP_F08_F07_activation_execution_use_consumed = no
historical_MVP_F08_implementation_mutating_attempt_consumed = no
historical_MVP_F08_original_approval_reusable = no
historical_MVP_F08_original_prompt_reusable = no
historical_MVP_F08_automatic_retry_allowed = no
historical_MVP_F08_failure_surface = outer_execution_report_latch_update_procedure
historical_MVP_F08_persistence_writer_defect_proven = no
historical_MVP_F08_target_integrity_defect_proven = no
historical_MVP_F08_payload_defect_proven = no
```

The last authorized historical pre-write snapshots reported zero records and
zero reservations. Baseline v1.2 does not claim current target emptiness and
does not perform a new target inspection.

```text
actual_evidence_layer_write_performed = no
persisted_real_candidate_record_created = no
production_evidenceitem_created = no
production_case_changed = no
downstream_runtime_called = no
```

## 6. MVP-CHG-004-P1 and P1A State

```text
MVP_CHG_004_P1_commit = 52cbc3f1832e61596b54e58a4c2d80e171b1ba88
MVP_CHG_004_P1_status = safe_committed_work_with_independent_needs_fix_for_P2_readiness
P1_overlap_and_substring_replacement_defect_closed = yes
P1_whole_block_CAS_and_atomic_update_preserved = yes
P1_revert_required = no
P1_state_machine_missing_attempt_consumption_transition = yes
MVP_CHG_004_P1A_status = terminal_needs_fix_before_TDD_or_implementation
P1A_latch_module_changed = no
P1A_latch_tests_changed = no
P1A_transition_implemented = no
P1A_receipt_proof_builder_implemented = no
P1A_CAS_proof_integration_implemented = no
P1A_atomic_proof_integration_implemented = no
P1A_receipt_contract_alignment_gap = yes
P1A_proof_contract_weakened = no
P1A_missing_fields_inferred = no
```

The originally proposed direct-field proof could not be built because the
current receipt does not directly expose:

```text
input_safe_hash
gate_contract_safe_hash
```

P1A stopped before TDD or implementation rather than inferring those fields or
weakening the proof boundary.

## 7. Selected Recovery Architecture

```text
selected_recovery_architecture = receipt_idempotency_key_cross_binding_without_persistence_receipt_schema_change
persistence_receipt_schema_change_selected = no
persistence_service_change_selected = no
F07_activation_rebinding_selected = no
```

The current receipt exposes `idempotency_key`. The current committed writer
derives that key as SHA-256 over canonical JSON with UTF-8 encoding,
`ensure_ascii=true`, sorted keys, and compact separators. Its frozen projection
contains the following exact fields:

```text
namespace = sentigraph_governed_nonproduction_idempotency_v0_2
candidate_identity_digest
input_safe_hash
persisted_record_schema
persisted_record_schema_version
gate_contract_schema
gate_contract_version
gate_contract_safe_hash
activation_decision_safe_hash
mutation_mode
target_logical_label
command_schema
command_version
```

A future synthetic proof helper must:

1. Accept the direct in-memory writer receipt and exact frozen expected F07
   governance bindings.
2. Independently recompute the expected idempotency key with the exact frozen
   formula.
3. Require equality with the receipt's `idempotency_key`.
4. Require direct equality for every binding the receipt exposes.
5. Require the exact receipt schema and exact boolean types for reservation
   committed, mutating attempt consumed, and reservation verified.
6. Require all three consumption/verification booleans to be true before the
   latch records implementation mutating-attempt consumption.
7. Reject any formula, service hash, schema, candidate, payload, gate,
   activation, target, mutation-mode, command-version, or receipt mismatch.
8. Return only bounded, value-safe proof metadata.

The proof must not rely on final-outcome text alone, a receipt hash alone, a
caller boolean alone, a partial match, missing-field inference, receipt schema
modification, writer re-execution, or target inspection.

## 8. Baseline v1.2 Prompt Budget

```text
consumed_engineering_prompts_since_v1_2_baseline = 0
consumed_fixed_prompts_since_v1_2 = 0
consumed_conditional_prompts_since_v1_2 = 0
consumed_risk_prompts_since_v1_2 = 0
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

The v1.2 governance Prompt is governance-only and does not consume an
engineering, fixed, conditional, or risk Prompt. A budget entry is not an
execution authorization and cannot bypass a sequence prerequisite.

## 9. Known Recovery Fixed Milestone MVP12-F01

```text
milestone = MVP12-F01
title = Synthetic Receipt Idempotency Cross-binding Proof and Explicit Attempt-consumption Latch Transition Repair
prompt_count = 1
status = not_started
authorized = no
executed = no
scope_classification = synthetic_receipt_fixture_only_code_test_and_health_report
```

MVP12-F01 may use synthetic receipt fixtures, inspect the current persistence
service only as read-only source/AST, recompute the expected idempotency key,
implement a strict cross-binding proof and one-time monotonic latch transition,
integrate CAS and atomic update, and add focused tests and a safe health report.

It may not read a real payload or target, call the writer, execute persistence,
change the receipt schema, or create a production/downstream object.

## 10. Known Recovery Fixed Milestone MVP12-F02

```text
milestone = MVP12-F02
title = One Fresh Bounded F08 Remediation Persistence Execution
prompt_count = 1
status = not_started
authorized = no
executed = no
scope_classification = fresh_exact_single_execution_no_retry
```

MVP12-F02 may be considered only after committed MVP12-F01 work receives
independent ChatGPT acceptance and a fresh exact human approval. Its future
boundary is one newly governed protected payload read, one public writer
invocation, no retry, maximum one mutating attempt, the exact target, the new
structured outer latch, and receipt idempotency cross-binding proof.

MVP12-F02 is the only planned successor to the historical unexecuted writer
portion of MVP-F08. It does not reclassify or reuse the historical F08 attempt.

## 11. Inherited Downstream Fixed Plan

The twelve inherited fixed Prompts remain ordered after successful MVP12-F02
acceptance:

| Inherited milestone | Prompt count | v1.2 initial state |
| --- | ---: | --- |
| MVP-F09 Independent Post-write Integrity, Idempotency, and Recovery Audit | 1 | not started, unauthorized |
| MVP-F10 Governed Record to Internal Review Console Integration | 2 | not started, unauthorized |
| MVP-F11 Governed Record to Controlled Analysis Input Bridge | 2 | not started, unauthorized |
| MVP-F12 Controlled Opinion Ecosystem and Dense Graph Execution | 1 | not started, unauthorized |
| MVP-F13 Human-reviewable Internal Result/Report and Operator Continuity | 2 | not started, unauthorized |
| MVP-F14 C-demo Final Continuity and Comprehension Regression | 1 | not started, unauthorized |
| MVP-F15 Local Operations, Cleanup, Pause, and Recovery Package | 1 | not started, unauthorized |
| MVP-F16 Final Integrated Internal Alpha Validation Package | 1 | not started, unauthorized |
| MVP-F17 Internal Alpha Completion Decision and Source Synchronization | 1 | not started, unauthorized |
| **Total inherited downstream fixed Prompts** | **12** | |

Together, the two known recovery Prompts and twelve inherited downstream
Prompts equal the v1.2 fixed budget of fourteen.

## 12. Sequence Hard Gate

```text
Baseline v1.2 commit
-> ChatGPT independent acceptance
-> Project Source synchronization
-> fresh exact MVP12-F01 approval
-> one MVP12-F01 implementation
-> ChatGPT independent acceptance
-> fresh exact MVP12-F02 approval
-> one MVP12-F02 execution with no retry
-> ChatGPT independent acceptance
-> only then consider MVP-F09
```

Forbidden sequence shortcuts:

- automatic progression;
- reuse of the historical F08 approval or P1A approval;
- combining F01 repair with F02 execution;
- modifying the persistence receipt schema during F01;
- executing F02 before independent F01 acceptance;
- using conditional or risk allowance to bypass the order;
- starting MVP-F09 before accepted F02 completion.

This baseline contains no future approval phrase or ready-to-sign template.

## 13. Current Business and Authorization State

```text
latest_valid_business_checkpoint = MVP-F07 exact nonproduction persistence gate activation decision effective
latest_committed_engineering_checkpoint = MVP-CHG-004-P1 safe committed overlap repair
execution_gate_status = activated_pending_separate_fresh_F08_remediation_execution_approval
F07_activation_execution_use_consumed = no
historical_MVP_F08_completed = no
MVP12_F01_eligible_after_chatgpt_acceptance_and_source_sync = yes
MVP12_F01_authorized = no
MVP12_F01_executed = no
MVP12_F02_authorized = no
MVP12_F02_executed = no
MVP_F09_authorized = no
actual_write_execution_authorized_now = no
actual_evidence_layer_write_performed = no
attempt_reservation_created = no
persisted_real_candidate_record_created = no
production_evidenceitem_creation_authorized = false
production_evidenceitem_created = no
8W_69_pause_preserved = yes
production_analysis_result_authorized = no
public_or_customer_delivery_authorized = no
```

## 14. Rebaseline Governance Rules

1. Baseline v1.1 remains the immutable source of historical v1.1 accounting.
2. Baseline v1.2 becomes the source of current remaining-budget and recovery
   sequence state only after commit and independent ChatGPT acceptance.
3. Historical v1.1 consumption is not reset, transferred, or erased.
4. MVP12-F01 and MVP12-F02 consume their fixed Prompts only when separately
   approved Goals are activated.
5. Conditional and risk allowances cannot bypass the hard sequence gate.
6. Newly discovered work requires explicit classification before consuming
   conditional or risk allowance.
7. Exhausting the v1.2 risk buffer requires another governance decision before
   unplanned engineering work.
8. Prompt exhaustion does not prove product completion; completion requires
   evidence and independent human acceptance.

## 15. No-side-effect State

```text
docs_only = yes
code_changed = no
tests_changed = no
runtime_accessed = no
protected_payload_or_capture_receipt_accessed = no
source_package_row_candidate_author_or_URL_accessed = no
target_or_initialization_receipt_accessed = no
SQLite_accessed = no
persistence_writer_imported_or_called = no
candidate_or_reservation_mutation_performed = no
persistence_executed = no
F08_remediation_executed = no
production_or_downstream_object_created = no
Project_Source_changed = no
```

## 16. Baseline Lifecycle, Source Recommendation, and Next Boundary

```text
baseline_v1_2_status = candidate_effective_pending_chatgpt_acceptance
next_boundary = ChatGPT independent acceptance of Baseline v1.2 and Project Source synchronization
Project_Source_update_recommended_after_ChatGPT_acceptance = yes
Canonical_00_recommendation = replace
Canonical_09_recommendation = replace
Canonical_03_recommendation = replace
Canonical_05_recommendation = no_change
Source_11_recommendation = no_change
next_engineering_milestone = MVP12-F01
MVP12_F01_authorized_now = no
```

Codex does not modify Project Source in this task. After independent ChatGPT
acceptance, Source synchronization occurs outside this repository change.
