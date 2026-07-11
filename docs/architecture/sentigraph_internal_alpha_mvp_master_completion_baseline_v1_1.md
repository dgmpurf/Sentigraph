# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.1

## 1. Purpose

This document establishes the post-P1A completion baseline for Sentigraph
Internal Alpha / MVP v1. It closes Baseline v1.0 for future prompt accounting,
preserves every historical consumption fact, and places two known F06 recovery
steps ahead of the inherited downstream plan.

This is a governance and planning contract. It does not authorize code changes,
formal target access, runtime execution, gate activation, persistence, or a
production object.

## 2. Baseline Identity

```text
baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_1
baseline_version = 1.1
baseline_scope = internal_alpha_mvp_v1_recovery_and_remaining_completion
baseline_status = effective_after_v1_1_baseline_commit_and_chatgpt_acceptance
baseline_project_state_anchor = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
baseline_rebaseline_reason = v1_0_risk_buffer_exhausted_with_two_known_F06_recovery_steps_remaining
baseline_v1_1_rebaseline_governance_prompt_consumed = 1
baseline_v1_1_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
consumed_engineering_prompts_since_v1_1_baseline = 0
```

The project-state anchor identifies the committed post-P1A engineering state
inspected for this rebaseline. The future documentation commit cannot embed its
own SHA; Git history and the final Codex receipt record that commit after it is
created and pushed.

## 3. Baseline v1.0 Historical Closure

Baseline v1.0 is historical, closed for future prompt accounting, and
immutable. It is not deleted, replaced, rewritten, or reclassified.

```text
baseline_version = 1.0
baseline_status = historical_closed_for_future_prompt_accounting
baseline_v1_0_final_anchor = b193bd70c89326c8606f204b2749ffa0ddf2bf8c
consumed_engineering_prompts_since_v1_0_baseline = 14
consumed_fixed_prompts = 6
consumed_conditional_prompts = 4
consumed_risk_prompts = 4
remaining_fixed_prompts_at_v1_0_closure = 14
remaining_conditional_allowance_at_v1_0_closure = 6
remaining_risk_buffer_at_v1_0_closure = 0
risk_buffer_exhausted = yes
rebaseline_required = yes
```

The v1.0 governance sources remain byte-preserved:

- `docs/planning/sentigraph_internal_alpha_mvp_master_completion_baseline_v1_0.md`
  with SHA-256
  `af6b066bf4ca145361695201d4314e4de37a24507946e0c0beaad232a40a7173`;
- `docs/planning/sentigraph_internal_alpha_mvp_remaining_milestones_prompt_budget_and_change_control_v1_0.md`
  with SHA-256
  `9f50a0f77023dc9a8c02517143b8cd6af3613e90b3ca7b4af05f1081367c5b45`.

The following remain historical facts:

- the cross-project routing incident occurred and its mistaken commit was
  reverted without history rewrite;
- the incident Goal is not valid milestone evidence;
- the first F06 remains `needs_fix`, incomplete, unreclassified, and without a
  successfully initialized formal target;
- the MVP-C03 allowance is exhausted at two consumed prompts;
- P1 and P1A remain committed evidence;
- no formal target recheck has succeeded;
- no execution gate, persistence action, or production-object creation has
  occurred.

No v1.0 consumption is reset or transferred into v1.1.

## 4. Current Business and Authorization State

```text
latest_valid_business_checkpoint = MVP-F05 completed
human_final_write_authorization_performed = yes
final_write_authorization_scope = exact_locked_candidate_only
execution_gate_contract_established = yes
execution_gate_status = defined_but_inactive_pending_separate_execution_approval
execution_gate_activated = no
historical_first_MVP_F06_status = needs_fix
historical_first_MVP_F06_completed = no
historical_first_MVP_F06_reclassified = no
effective_MVP_F06_completed = no
formal_target_recheck_completed = no
actual_write_execution_authorized_now = no
actual_evidence_layer_write_performed = no
persisted_real_candidate_record_created = no
production_evidenceitem_creation_authorized = false
production_evidenceitem_created = no
8W_69_pause_preserved = yes
production_analysis_result_authorized = no
public_or_customer_delivery_authorized = no
MVP_F07_status = not_started
MVP_F07_authorized = no
MVP_F07_executed = no
```

Historical exact-candidate authorization does not activate a gate, authorize
current execution, or permit a production `EvidenceItem`.

## 5. Baseline v1.1 Prompt Budget

```text
inherited_downstream_fixed_prompt_allowance = 14
new_known_recovery_fixed_prompt_allowance = 2
fixed_prompt_budget = 16
conditional_prompt_allowance = 6
risk_buffer_prompt_allowance = 2
best_case_remaining_prompts = 16
controlled_ceiling_remaining_prompts = 22
hard_ceiling_remaining_without_another_rebaseline = 24
consumed_fixed_prompts_since_v1_1 = 0
consumed_conditional_prompts_since_v1_1 = 0
consumed_risk_prompts_since_v1_1 = 0
remaining_fixed_prompts = 16
remaining_conditional_allowance = 6
remaining_risk_buffer = 2
```

Arithmetic:

```text
fixed_prompt_budget = 14 + 2 = 16
controlled_ceiling_remaining_prompts = 16 + 6 = 22
hard_ceiling_remaining_without_another_rebaseline = 16 + 6 + 2 = 24
```

The 14 inherited fixed prompts preserve the former downstream plan. The two
known F06 recovery steps are fixed work, not risk work. Conditional allowance
is inherited without expansion and remains subject to the original trigger and
expiry rules. The new risk buffer is narrow and covers only genuinely new
defects discovered after v1.1.

A budget entry never authorizes execution. Unused allowance cannot bypass a
milestone prerequisite or hard sequence gate.

## 6. Fixed Recovery Milestone MVP11-F01

```text
milestone = MVP11-F01
title = Receipt Finalization and Failure-artifact Semantics Repair
prompt_count = 1
status = not_started
authorized = no
executed = no
scope_classification = synthetic_only_code_test_and_health_report_repair
```

MVP11-F01 must establish all of the following:

1. Result and receipt schemas are upgraded where required.
2. Durable receipt bytes do not claim their own write, fsync, readback, or byte
   acceptance has already completed.
3. Receipt bytes may describe execution profile, safe repository/target
   bindings, schema and zero-row results, no candidate/reservation/gate/
   persistence/production behavior, and the requirement for external human
   approval.
4. Neither runner nor receipt grants authorization.
5. Receipt write, fsync, readback, and byte-acceptance completion belong only
   in the outer runner result, the later formal execution report, and
   independent ChatGPT acceptance.
6. If an exact same-run receipt was created but finalization did not
   conclusively complete, there is no overwrite and no retry.
7. The target commit, if already successful, remains untouched.
8. The exact same-run receipt may be deleted only when current-run creation,
   prior absence, locked path identity, and unambiguous deletion are all
   proven.
9. Successful exact deletion is recorded. Failed or ambiguous deletion yields
   `incomplete_unaccepted_receipt_artifact` and pauses.
10. Wildcard, recursive, alternate-path, and substitute cleanup are forbidden.
11. Tests use temporary Git roots and temporary SQLite only.
12. Actual Sentigraph root, runtime, target, and receipt access are forbidden.

MVP11-F01 completion does not authorize MVP11-F02.

## 7. Fixed Recovery Milestone MVP11-F02

```text
milestone = MVP11-F02
title = Independent Formal-profile Acceptance and One Exact Formal-target F06 Recheck
prompt_count = 1
status = not_started
authorized = no
executed = no
scope_classification = frozen_code_single_formal_execution_no_retry
```

Prerequisites:

1. MVP11-F01 is committed and pushed.
2. ChatGPT independently accepts MVP11-F01.
3. Runner, tests, and relevant reports have frozen hashes.
4. The worktree is clean.
5. A fresh exact MVP11-F02 approval is received after F01 acceptance.
6. No pre-P1A or pre-F01 P2 approval is reused.

Execution contract:

1. No code or test modification.
2. Exactly one actual Sentigraph repository-root runner invocation.
3. Exactly one formal execution and no automatic or manual retry.
4. One SQLite connection maximum.
5. Exact F05 target/receipt labels and exact repository/profile hashes only.
6. No runtime enumeration or target substitution.
7. No payload, source, package, or candidate read.
8. No candidate or reservation write.
9. No gate activation, persistence execution, or production object.
10. Outer governance records actual-root provenance.
11. Runtime artifacts remain ignored and unstaged.
12. Only the safe F02 health report may be committed.

For an absent target, the one execution may create and verify the exact empty
schema and safe receipt. For an existing target, it may open only the exact
target read-only, verify exact schema and zero rows, prove database bytes
unchanged, and create the exact receipt only if absent.

Any blocked, `needs_fix`, ambiguous, or privacy-stop result ends the execution.
There is no second run or same-Goal repair.

MVP11-F02 plus independent ChatGPT acceptance may establish effective F06
completion. It does not authorize MVP-F07.

## 8. Sequence Hard Gate

```text
MVP11-F01
-> ChatGPT independent acceptance
-> fresh exact MVP11-F02 approval
-> MVP11-F02 one formal execution
-> ChatGPT independent acceptance
-> only then consider MVP-F07
```

The following are forbidden:

- combining F01 code repair with F02 real execution;
- executing F02 before independent F01 acceptance;
- reusing the earlier P2 approval;
- automatic progression from F01 to F02;
- automatic progression from F02 to F07;
- using conditional or risk allowance to bypass sequence order.

## 9. Earlier P2 Approval

```text
MVP_CHG_003_P2_approval_received_before_P1A = yes
MVP_CHG_003_P2_goal_activated = no
MVP_CHG_003_P2_execution_performed = no
MVP_CHG_003_P2_prompt_consumed = no
MVP_CHG_003_P2_previous_approval_reusable = no
invalidation_reason = runner_result_and_receipt_contract_changed_after_approval
fresh_post_F01_exact_MVP11_F02_approval_required = yes
```

The old approval is neither executed nor consumed nor retroactively revoked.
It simply cannot authorize the post-P1A/post-F01 code state.

## 10. Inherited Downstream Fixed Plan

The 14 inherited fixed prompts retain their v1.0 definitions and ordering after
successful MVP11-F02 acceptance:

| Inherited milestone | Prompt count | v1.1 initial state |
| --- | ---: | --- |
| MVP-F07 Exact Gate Activation Decision | 1 | not started, unauthorized |
| MVP-F08 Single Governed Nonproduction Persistence Execution | 1 | not started, unauthorized |
| MVP-F09 Independent Post-write Integrity, Idempotency, and Recovery Audit | 1 | not started, unauthorized |
| MVP-F10 Governed Record to Internal Review Console Integration | 2 | not started, unauthorized |
| MVP-F11 Governed Record to Controlled Analysis Input Bridge | 2 | not started, unauthorized |
| MVP-F12 Controlled Opinion Ecosystem and Dense Graph Execution | 1 | not started, unauthorized |
| MVP-F13 Human-reviewable Internal Result/Report and Operator Continuity | 2 | not started, unauthorized |
| MVP-F14 C-demo Final Continuity and Comprehension Regression | 1 | not started, unauthorized |
| MVP-F15 Local Operations, Cleanup, Pause, and Recovery Package | 1 | not started, unauthorized |
| MVP-F16 Final Integrated Internal Alpha Validation Package | 1 | not started, unauthorized |
| MVP-F17 Internal Alpha Completion Decision and Source Synchronization | 1 | not started, unauthorized |
| **Total** | **14** | |

MVP-F07 is the first inherited downstream boundary. Its definition remains
inherited, but its current status is `not_started`, `authorized = no`, and
`executed = no`.

## 11. Completion Endpoint and Product Boundary

The v1.0 B-core + C-demo endpoint remains inherited. Baseline v1.1 changes the
recovery sequence and prompt accounting, not the product endpoint.

The endpoint still requires one bounded governed nonproduction record,
read-only review and audit visibility, deterministic internal analysis and
dense-graph interpretation, a human-reviewable internal result/report, final
local recovery evidence, and the selected-sample C-demo.

It still does not require or authorize production `EvidenceItem`, production
case/Review Queue/`analysis_run`/Analysis Result, Source 11 production runtime,
B-end customer report, Sandbox/public event runtime, public export, external
delivery, live unrestricted collection, or real LLM execution.

## 12. Rebaseline Governance Rules

1. Baseline v1.0 remains the source of historical accounting and definitions.
2. Baseline v1.1 is the source of current remaining-budget and recovery-sequence
   state after ChatGPT acceptance.
3. The v1.1 governance prompt does not count as an engineering, fixed,
   conditional, or risk prompt.
4. MVP11-F01 and MVP11-F02 consume the two new fixed prompts only when their
   separately authorized Goals are activated.
5. A genuinely new defect after v1.1 requires explicit classification before
   risk-buffer consumption.
6. Exhaustion of the new risk buffer requires another rebaseline before new
   unplanned engineering work.
7. Prompt exhaustion does not prove product completion.
8. Completion requires evidence and independent human acceptance.

## 13. No-side-effect State

```text
docs_only = yes
code_changed = no
tests_changed = no
runtime_accessed = no
formal_target_accessed = no
formal_receipt_accessed = no
payload_or_source_read = no
candidate_mutation_performed = no
attempt_reservation_mutation_performed = no
gate_activated = no
persistence_executed = no
production_object_created = no
Project_Source_changed = no
```

## 14. Baseline Lifecycle and Next Boundary

```text
baseline_v1_1_status = candidate_effective_pending_chatgpt_acceptance
next_boundary = ChatGPT independent acceptance of Baseline v1.1 and Project Source synchronization
Project_Source_update_recommended_after_ChatGPT_acceptance = yes
next_engineering_milestone = MVP11-F01 Receipt Finalization and Failure-artifact Semantics Repair
MVP11_F01_authorized_now = no
```

After acceptance, ChatGPT may prepare replacements for Canonical 00, 09, 03,
and 05 outside this repository task. No Project Source file is created or
modified here.
