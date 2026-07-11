# Sentigraph Baseline v1.1 Rebaseline After Risk-buffer Exhaustion Decision v1.0

## 1. Decision Identity

- decision_record_schema = sentigraph_baseline_v1_1_rebaseline_after_risk_buffer_exhaustion_decision_v1_0
- decision_record_version = 1.0
- decision = ready
- privacy_issue_stop = no
- baseline_v1_1_status = candidate_effective_pending_chatgpt_acceptance
- docs_only = yes
- actual_model_deployment_identifier = hidden_by_current_Codex_session

## 2. Goal

- Goal_created = yes
- Goal_activated = yes
- active_Goal_state_observed = yes
- Goal_completed = yes
- goal_scope = Baseline_v1_1_docs_only_rebaseline

## 3. Git Preflight

- repository_identity = dgmpurf/Sentigraph
- branch = main
- starting_HEAD = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
- starting_origin_main = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
- starting_HEAD_message = Repair MVP-CHG-003-P1A formal execution receipt truthfulness
- starting_ahead_behind = 0/0
- starting_worktree_state = clean
- starting_staged_file_count = 0
- starting_untracked_file_count = 0
- Baseline_v1_1_preexisted = no
- preflight = pass

## 4. Baseline v1.0 Historical Closure

- baseline_v1_0_historical_closure_recorded = yes
- baseline_v1_0_final_accounting_verified = yes
- baseline_v1_0_status = historical_closed_for_future_prompt_accounting
- baseline_v1_0_final_anchor = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
- consumed_engineering_prompts_since_v1_0_baseline = 14
- consumed_fixed_prompts = 6
- consumed_conditional_prompts = 4
- consumed_risk_prompts = 4
- remaining_fixed_prompts_at_v1_0_closure = 14
- remaining_conditional_allowance_at_v1_0_closure = 6
- remaining_risk_buffer_at_v1_0_closure = 0
- risk_buffer_exhausted = yes
- historical_consumption_reset = no
- historical_first_MVP_F06_status = needs_fix
- historical_first_MVP_F06_completed = no
- historical_first_MVP_F06_reclassified = no
- MVP_C03_prompt_allowance_consumed = 2
- MVP_C03_prompt_allowance_remaining = 0

Committed v1.0 document evidence:

- master SHA-256 =
  `af6b066bf4ca145361695201d4314e4de37a24507946e0c0beaad232a40a7173`;
- prompt-budget/change-control SHA-256 =
  `9f50a0f77023dc9a8c02517143b8cd6af3613e90b3ca7b4af05f1081367c5b45`.

## 5. Baseline v1.1 Establishment

- baseline_v1_1_established = yes
- baseline_v1_1_anchor = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
- baseline_v1_1_scope = internal_alpha_mvp_v1_recovery_and_remaining_completion
- baseline_v1_1_rebaseline_reason = v1_0_risk_buffer_exhausted_with_two_known_F06_recovery_steps_remaining
- baseline_v1_1_rebaseline_governance_prompt_consumed = 1
- baseline_v1_1_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
- consumed_engineering_prompts_since_v1_1_baseline = 0
- baseline_v1_1_budget = fixed_16_conditional_6_risk_2
- fixed_prompt_budget = 16
- conditional_prompt_allowance = 6
- risk_buffer_prompt_allowance = 2
- best_case_remaining_prompts = 16
- controlled_ceiling_remaining_prompts = 22
- hard_ceiling_remaining_without_another_rebaseline = 24
- consumed_fixed_prompts_since_v1_1 = 0
- consumed_conditional_prompts_since_v1_1 = 0
- consumed_risk_prompts_since_v1_1 = 0
- remaining_fixed_prompts = 16
- remaining_conditional_allowance = 6
- remaining_risk_buffer = 2
- budget_arithmetic_verified = yes

The v1.1 governance prompt is not retroactively added to v1.0 engineering or
allowance consumption.

## 6. Recovery Milestones and Sequence

- MVP11_F01_defined = yes
- MVP11_F01_title = Receipt Finalization and Failure-artifact Semantics Repair
- MVP11_F01_prompt_count = 1
- MVP11_F01_status = not_started
- MVP11_F01_authorized = no
- MVP11_F01_executed = no
- MVP11_F02_defined = yes
- MVP11_F02_title = Independent Formal-profile Acceptance and One Exact Formal-target F06 Recheck
- MVP11_F02_prompt_count = 1
- MVP11_F02_status = not_started
- MVP11_F02_authorized = no
- MVP11_F02_executed = no
- sequence_hard_gate_defined = yes
- F01_and_F02_combination_allowed = no
- F02_requires_independent_F01_acceptance = yes
- F02_requires_fresh_post_F01_exact_approval = yes
- F02_execution_limit = one
- F02_retry_allowed = no
- automatic_progression_to_F02 = no
- automatic_progression_to_F07 = no

Required sequence:

```text
MVP11-F01
-> ChatGPT independent acceptance
-> fresh exact MVP11-F02 approval
-> one formal MVP11-F02 execution
-> ChatGPT independent acceptance
-> only then consider MVP-F07
```

## 7. Earlier P2 Approval

- MVP_CHG_003_P2_approval_received_before_P1A = yes
- MVP_CHG_003_P2_goal_activated = no
- MVP_CHG_003_P2_execution_performed = no
- MVP_CHG_003_P2_prompt_consumed = no
- old_P2_approval_invalidated_for_reuse = yes
- MVP_CHG_003_P2_previous_approval_reusable = no
- invalidation_reason = runner_result_and_receipt_contract_changed_after_approval
- fresh_post_F01_exact_MVP11_F02_approval_required = yes

The earlier approval is recorded as unexecuted and unconsumed. It is not
described as retroactively revoked; it simply cannot authorize the changed code
state.

## 8. Inherited Plan and Current Authorization

- inherited_downstream_fixed_prompt_allowance = 14
- new_known_recovery_fixed_prompt_allowance = 2
- inherited_downstream_definitions_preserved = yes
- first_inherited_downstream_milestone = MVP-F07 Exact Gate Activation Decision
- MVP_F07_status = not_started
- MVP_F07_authorized = no
- MVP_F07_executed = no
- human_final_write_authorization_performed = yes
- final_write_authorization_scope = exact_locked_candidate_only
- execution_gate_contract_established = yes
- execution_gate_status = defined_but_inactive_pending_separate_execution_approval
- execution_gate_activated = no
- effective_MVP_F06_completed = no
- formal_target_recheck_completed = no
- actual_write_execution_authorized_now = no
- actual_evidence_layer_write_performed = no
- persisted_real_candidate_record_created = no
- production_evidenceitem_creation_authorized = false
- production_evidenceitem_created = no
- 8W_69_pause_preserved = yes
- production_analysis_result_authorized = no
- public_or_customer_delivery_authorized = no

## 9. Validation

- exact_two_file_allowlist_verification = pass
- Markdown_structural_check = pass
- required_field_presence_check = pass
- accounting_arithmetic_check = pass
- milestone_sequence_consistency_check = pass
- approval_state_consistency_check = pass
- stale_current_commit_reference_scan = pass
- absolute_path_secret_protected_value_scan = pass
- placeholder_and_mojibake_scan = pass
- git_diff_check = pass
- no_index_whitespace_check = pass
- pytest_run = no_docs_only
- frontend_build_run = no_docs_only
- browser_smoke_run = no_docs_only
- runner_or_SQLite_run = no

## 10. Changed-file Inventory

- changed_file_count = 2
- created_file_1 = docs/architecture/sentigraph_internal_alpha_mvp_master_completion_baseline_v1_1.md
- created_file_2 = docs/health/sentigraph_baseline_v1_1_rebaseline_after_risk_buffer_exhaustion_decision_v1_0.md
- existing_file_modified = no
- code_changed = no
- tests_changed = no
- configuration_changed = no
- workflow_changed = no

## 11. Safety and No-side-effect Proof

- runtime_accessed = no
- formal_target_accessed = no
- formal_receipt_accessed = no
- actual_Sentigraph_root_passed_to_runner = no
- runner_invoked = no
- SQLite_opened = no
- protected_payload_read = no
- protected_capture_receipt_read = no
- source_or_package_read = no
- candidate_reconstructed = no
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no
- provider_or_collector_called = no
- network_called = no
- Quant_or_other_project_accessed = no
- Project_Source_changed = no
- GitHub_Actions_changed = no

## 12. Git Publication Policy

- commit_result = pending_ready_only_auto_commit
- push_result = pending_ready_only_auto_push
- future_commit_SHA_self_embedding_possible = no
- required_commit_message = Establish Baseline v1.1 after risk-buffer exhaustion
- tag = no

The final Codex receipt records the actual commit SHA, push result, and clean
worktree after publication. This document cannot safely predict its own future
Git commit.

## 13. Project Source and Next Boundary

- Project_Source_update_recommended_after_ChatGPT_acceptance = yes
- Project_Source_changed_by_Codex = no
- expected_later_replacements = Canonical_00_09_03_05
- next_boundary = ChatGPT independent acceptance of Baseline v1.1 and Project Source synchronization
- next_engineering_milestone = MVP11-F01 Receipt Finalization and Failure-artifact Semantics Repair
- next_engineering_milestone_authorized_now = no
- subsequent_Goal_started = no

No exact approval phrase for MVP11-F01 or MVP11-F02 is generated here.
