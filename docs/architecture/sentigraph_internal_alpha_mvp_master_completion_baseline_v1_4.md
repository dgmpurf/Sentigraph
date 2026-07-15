# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.4

## 1. Purpose and scope

~~~text
decision = ready
privacy_issue_stop = no
docs_only = yes
baseline_v1_4_status = candidate_effective_pending_chatgpt_acceptance
~~~

Baseline v1.4 closes Baseline v1.3 for future Prompt accounting while
preserving every v1.3 historical record. It establishes a new bounded
completion allowance, freezes MVP-F12-P3 and MVP-F12-P4 as separate future
milestones in that order, and performs no runtime or implementation action.

## 2. Baseline identity and approval

~~~text
baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_4
baseline_version = 1.4
baseline_scope = post_MVP_F12_P2_first_formal_decision_and_independent_post_write_audit_completion
baseline_project_state_anchor = 8d31265ff9fa2af77da2e24e528df83ba04477fd
baseline_rebaseline_reason = accepted_MVP_F12_P2_requires_two_separate_mandatory_fixed_milestones_P3_and_P4_while_v1_3_has_only_one_fixed_prompt_remaining
baseline_v1_4_rebaseline_governance_prompt_consumed = 1
baseline_v1_4_rebaseline_governance_prompt_classification = governance_only_not_engineering_prompt
exact_rebaseline_approval_received = yes
exact_rebaseline_approval_match = yes
exact_rebaseline_approval_sha256 = 5478ed7bd11de2c958781f5ccd4396ac7ebf6d3dc515af47cc06dc2edac86632
~~~

Exact approval:

~~~text
APPROVE_SENTIGRAPH_INTERNAL_ALPHA_MVP_MASTER_COMPLETION_BASELINE_V1_4_DOCS_ONLY_GOVERNANCE_REBASELINE_AFTER_ACCEPTED_MVP_F12_P2_BIND_STARTING_COMMIT_8D31265FF9FA2AF77DA2E24E528DF83BA04477FD_AND_ACCEPTED_P2_SERVICE_BLOB_13ADE443CD3186D17E8F10AF229F5F7EA82984ED_AND_TEST_BLOB_5E9DD6C8B60643926C6EEA73C1B49345B114EEA4_AND_REPORT_BLOB_1626B16DB8362C3F32A00F89ACECB625F50412FD_AND_ACCEPTED_INITIALIZATION_RECEIPT_CANONICAL_SHA256_5D65DA59110352DEF9C0160F78F38A94251FF51ADB918C8C1EA142A44B0B4874_CLOSE_BASELINE_V1_3_HISTORICALLY_WITH_CONSUMPTION_ENGINEERING_21_FIXED_13_CONDITIONAL_6_RISK_2_AND_REMAINING_FIXED_1_CONDITIONAL_0_RISK_0_WITH_NO_HISTORICAL_RESET_TRANSFER_ERASURE_OR_RECLASSIFICATION_CLASSIFY_THE_V1_4_REBASELINE_PROMPT_AS_GOVERNANCE_ONLY_NOT_ENGINEERING_PROMPT_ESTABLISH_BASELINE_V1_4_WITH_INHERITED_FIXED_ALLOWANCE_1_NEW_KNOWN_FIXED_ALLOWANCE_2_FOR_SEPARATE_MVP_F12_P3_AND_MVP_F12_P4_MILESTONES_FIXED_PROMPT_BUDGET_3_CONDITIONAL_PROMPT_ALLOWANCE_6_RISK_BUFFER_PROMPT_ALLOWANCE_2_BEST_CASE_3_CONTROLLED_CEILING_9_HARD_CEILING_11_FREEZE_THE_SEQUENCE_P3_FIRST_EXACT_KEEP_PENDING_HUMAN_REVIEW_DECISION_THEN_P4_INDEPENDENT_DIRECT_SQLITE_READ_ONLY_POST_WRITE_AUDIT_REQUIRE_SEPARATE_EXACT_APPROVAL_NEW_GOAL_AND_INDEPENDENT_CHATGPT_ACCEPTANCE_FOR_EACH_PHASE_PRESERVE_THE_TWO_HISTORICAL_P2_BLOCKED_OUTCOMES_AND_EFFECTIVE_P2_R2_ACCEPTANCE_DEFINE_P3_BINDING_TO_ACCEPTED_F11_CONSTANTS_P1_TARGET_HASHES_P2_RECEIPT_HASH_INITIALIZED_EXACT_EMPTY_STATE_SELF_DECLARED_AUTHORITY_ONE_FUTURE_NONREUSABLE_ACTIVATION_HASH_ONE_WRITER_INVOCATION_ONE_INSERT_ZERO_ROUTE_CALLS_ZERO_RETRIES_AND_NO_SECOND_DECISION_DEFINE_P4_EXACT_NINETEEN_FIELD_IDEMPOTENCY_DIRECT_IDENTIFIER_AND_ACTUAL_COLUMN_DECISION_HASH_RECOMPUTATION_WITH_NO_WRITER_REPLAY_EXACT_ONE_FILE_ALLOWLIST_DOCS_ARCHITECTURE_SENTIGRAPH_INTERNAL_ALPHA_MVP_MASTER_COMPLETION_BASELINE_V1_4_MD_NO_CODE_TEST_ROUTE_API_RUNTIME_SQLITE_FORMAL_TARGET_ACCESS_REAL_DECISION_FRONTEND_PROJECT_SOURCE_TAG_RELEASE_PRODUCTION_OR_LATER_PHASE_EXECUTION
~~~

Accepted committed anchors:

- Baseline v1.3 blob: e2fb07738a0c2f477713d23d1de9d3cb0d18d788
- Baseline v1.3 commit: 486bc547da6b97e121565489cf3b6e1a8c15080e
- F12-P1 contract blob: c2b9645ba1ee2724ba4a023fa267d4dfb5059302
- F12-P1 contract SHA-256: 0d0e4c0c12a534eb5f523fffb4430f223480339d197ec031c5621f6e1312b4b8
- Formal target identity safe hash: 4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202
- Formal target authorization safe hash: de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d

The future Baseline v1.4 commit SHA is intentionally not fabricated here.
Git history and the terminal completion receipt provide it after commit.

## 3. Baseline v1.3 historical closure

~~~text
baseline_version = 1.3
Baseline_v1_3_status = historical_closed_for_future_prompt_accounting_after_MVP_F12_P2_acceptance
baseline_status = historical_closed_for_future_prompt_accounting_after_MVP_F12_P2_acceptance
baseline_v1_3_final_committed_engineering_anchor = 8d31265ff9fa2af77da2e24e528df83ba04477fd
historical_v1_3_engineering_prompts_consumed = 21
historical_v1_3_fixed_prompts_consumed = 13
historical_v1_3_conditional_prompts_consumed = 6
historical_v1_3_risk_prompts_consumed = 2
historical_v1_3_fixed_prompts_remaining_at_closure = 1
historical_v1_3_conditional_allowance_remaining_at_closure = 0
historical_v1_3_risk_buffer_remaining_at_closure = 0
historical_v1_3_conditional_allowance_exhausted = yes
historical_v1_3_risk_buffer_exhausted = yes
historical_v1_3_fixed_allowance_exhausted = no
historical_consumption_reset = no
historical_consumption_transferred = no
historical_consumption_erased = no
historical_milestones_reclassified = no
historical_v1_3_engineering_prompts_consumed = 13 fixed + 6 conditional + 2 risk = 21
historical_v1_3_remaining_allowance_at_closure = 1 fixed + 0 conditional + 0 risk
v1_4_governance_prompt_added_to_v1_3_engineering_consumption = no
~~~

Baseline v1.3 remains immutable historical evidence. This closure does not
reset, transfer, erase, or reclassify any historical consumption or milestone.

## 4. Preserved P2 history and accepted checkpoint

~~~text
historical_initial_MVP_F12_P2_decision = blocked_one_time_formal_execution_result_unavailable
historical_MVP_F12_P2_R1_decision = blocked_receipt_field_order_mismatch
MVP_F12_P2_R2_decision = ready
effective_MVP_F12_P1_status = completed_and_independently_accepted
effective_MVP_F12_P2_status = completed_and_independently_accepted
accepted_MVP_F12_P2_commit = 8d31265ff9fa2af77da2e24e528df83ba04477fd
accepted_P2_service_blob = 13ade443cd3186d17e8f10af229f5f7ea82984ed
accepted_P2_test_blob = 5e9dd6c8b60643926c6eea73c1b49345b114eea4
accepted_P2_report_blob = 1626b16db8362c3f32a00f89acecb625f50412fd
accepted_initialization_receipt_canonical_sha256 = 5d65da59110352def9c0160f78f38a94251ff51adb918c8c1ea142a44b0b4874
formal_decision_ledger_state = initialized_exact_empty
accepted_formal_decision_row_count = 0
actual_human_review_decision_captured = no
MVP_F12_P3_authorized = no
MVP_F12_P3_executed = no
MVP_F12_P4_authorized = no
MVP_F12_P4_executed = no
~~~

The two blocked outcomes remain historical failure evidence and are not
rewritten as successful runs. Effective P2 completion derives only from the
accepted R2 forward recovery and the accepted final P2 commit.

## 5. Baseline v1.4 Prompt budget

~~~text
inherited_fixed_prompt_allowance = 1
new_known_fixed_prompt_allowance = 2
new_known_fixed_milestone_MVP_F12_P3 = 1 fixed prompt
new_known_fixed_milestone_MVP_F12_P4 = 1 fixed prompt
fixed_prompt_budget = 3
conditional_prompt_allowance = 6
risk_buffer_prompt_allowance = 2
consumed_engineering_prompts_since_v1_4 = 0
consumed_fixed_prompts_since_v1_4 = 0
consumed_conditional_prompts_since_v1_4 = 0
consumed_risk_prompts_since_v1_4 = 0
remaining_fixed_prompts = 3
remaining_conditional_allowance = 6
remaining_risk_buffer = 2
best_case_remaining_prompts = 3
controlled_ceiling_remaining_prompts = 9
hard_ceiling_remaining_without_another_rebaseline = 11
fixed_prompt_budget = 1 inherited + 2 new known = 3
controlled_ceiling = 3 + 6 = 9
hard_ceiling = 3 + 6 + 2 = 11
~~~

The inherited fixed allowance is an unassigned bounded reserve. It is not
automatic authorization for P3, P4, recovery, or another milestone.

Conditional and risk allowances require a separately confirmed trigger and a
fresh exact approval. They cannot automatically fund a failed one-time write,
cannot authorize a retry merely because budget exists, and do not alter any
business or runtime gate.

## 6. Required completion sequence

The required sequence is frozen exactly:

~~~text
Baseline v1.4 acceptance
-> separate exact P3 approval
-> new P3 Goal
-> one P3 execution
-> independent ChatGPT P3 acceptance
-> separate exact P4 approval
-> new P4 Goal
-> one P4 read-only audit
-> independent ChatGPT P4 acceptance
~~~

No phase may automatically authorize the next phase, reuse the prior phase
approval, reuse a completed Goal, merge P3 and P4, or treat a readiness marker
as runtime authority.

## 7. Planned fixed milestone MVP-F12-P3

Title: First Exact Formal Human-review Decision

~~~text
prompt_count = 1
status = not_started
authorized = no
executed = no
formal_decision_ledger_state = initialized_exact_empty
accepted_initialization_receipt_canonical_sha256 = 5d65da59110352def9c0160f78f38a94251ff51adb918c8c1ea142a44b0b4874
first_real_decision_type = keep_pending_human_review
forbidden_first_real_decision_type = request_more_governance_review
reviewer_role_label = self_declared_project_owner_role
reviewer_authority_basis_label = authority_basis_not_independently_validated
reviewer_identity_verified = false
independently_accepted_p2_initialization_receipt_canonical_sha256 = 5d65da59110352def9c0160f78f38a94251ff51adb918c8c1ea142a44b0b4874
p3_activation_binding_safe_hash = not_yet_available_requires_fresh_exact_P3_authorization
formal_writer_invocation_limit = 1
decision_INSERT_limit = 1
route_invocation_limit = 0
automatic_retry_allowed = false
automatic_repair_allowed = false
second_decision_allowed = false
~~~

The accepted F12-P1 exact 23-field P3 binding contract remains authoritative.
The future nonreusable activation object must bind at minimum:

- repository identity dgmpurf/Sentigraph;
- branch main;
- the exact future P3 starting commit;
- accepted F11 decision constants and idempotency semantics;
- accepted F12-P1 contract blob and target hashes;
- accepted P2 service blob 13ade443cd3186d17e8f10af229f5f7ea82984ed;
- accepted P2 test and report blobs;
- accepted P2 initialization receipt canonical SHA-256;
- required state initialized_exact_empty;
- decision type keep_pending_human_review;
- the exact authority labels and reviewer_identity_verified=false;
- the exact future P3 approval SHA-256;
- nonreusable activation=true;
- writer invocation limit=1;
- decision INSERT limit=1;
- route invocation limit=0;
- automatic retry=false;
- automatic repair=false;
- second decision=false.

P3 uses one repository-external UTF-8 direct-service runner, no HTTP route, no
frontend, and no committed runner. It permits at most one writer invocation
and one INSERT, with zero automatic retries and zero second decisions. Commit
ambiguity permits read-only deterministic verification only; unresolved
ambiguity pauses and never causes a second INSERT.

Exact future P3 repository allowlist:

1. backend/app/services/governed_nonproduction_human_review_decision_ledger.py
2. backend/app/tests/test_mvp_f12_p3_first_formal_human_review_decision.py
3. docs/health/sentigraph_mvp_f12_p3_first_formal_human_review_decision_report_v1_0.md

P3 stops after its decision and receipt. It does not execute P4.

## 8. Planned fixed milestone MVP-F12-P4

Title: Independent Formal Decision-ledger Post-write Audit

~~~text
prompt_count = 1
status = not_started
authorized = no
executed = no
required_starting_formal_decision_ledger_state = first_exact_decision_recorded
~~~

P4 uses one repository-external direct-SQLite read-only audit runner. It has no
service import, route, writer, mutation, writer replay, retry, repair, or second
decision.

P4 reconstructs this exact 19-field idempotency object in order:

1. request_schema
2. request_version
3. decision_type
4. reviewer_role_label
5. reviewer_authority_basis_label
6. source_projection_schema
7. source_projection_version
8. source_projection_id
9. source_projection_status
10. source_projection_canonical_sha256
11. source_outer_response_canonical_sha256
12. persisted_record_id
13. attempt_reservation_id
14. candidate_identity_digest
15. input_safe_hash
16. gate_contract_safe_hash
17. activation_decision_safe_hash
18. record_snapshot_digest
19. reservation_snapshot_digest

P4 canonicalizes using ensure_ascii=false, sort_keys=true, compact separators,
UTF-8, and lowercase SHA-256. It independently derives:

~~~text
recomputed_idempotency_key = SHA-256 of the exact canonical 19-field object
recomputed_decision_id = "ghrd-" + recomputed_idempotency_key[:32]
recomputed_audit_receipt_reference = "ghrd-receipt-" + recomputed_idempotency_key[:32]
~~~

Every recomputed value is compared with the actual stored column. P4
reconstructs the complete 38-field decision object from actual SQLite columns,
normalizes all eight Boolean columns, parses all four canonical-JSON columns,
and recomputes decision_canonical_hash as the SHA-256 of the canonical decision
object excluding only decision_canonical_hash.

P4 must verify:

~~~text
decision_type = keep_pending_human_review
ledger_scope = governed_nonproduction_record_human_review_only
decision_status = recorded_append_only_nonproduction
reviewer_identity_verified = false
exact_decision_row_count = 1
unrelated_row_count = 0
unexpected_sidecar_count = 0
integrity_mismatch_classification = blocked_post_write_integrity_mismatch
~~~

Any mismatch stops without mutation.

Exact future P4 repository allowlist:

1. docs/health/sentigraph_mvp_f12_p4_independent_formal_decision_ledger_post_write_audit_report_v1_0.md

The P4 runner remains repository-external and is removed after its bounded
read-only audit.

## 9. Product and authority boundaries

Baseline v1.4 does not authorize or imply verified reviewer identity, trust
approval or trust upgrade, governed-record mutation, a production Review
Queue, a production case or analysis_run, a production Analysis Result,
analysis, report, correction, revocation, frontend decision controls, public
export or final delivery, or P3/P4 execution.

A formal human-review decision remains append-only, nonproduction,
human-review-only, not an official verification, and not a production
approval.

## 10. No-side-effect proof

~~~text
docs_only = yes
new_document_count = 1
existing_repository_files_modified = 0
backend_code_changed = no
tests_changed = no
route_or_API_changed = no
frontend_changed = no
runtime_accessed = no
formal_target_accessed = no
SQLite_accessed = no
service_or_writer_invoked = no
real_human_review_decision_captured = no
Project_Source_changed = no
tag_or_release_created = no
~~~

## 11. Source recommendation

Only after independent ChatGPT acceptance:

- Canonical 00 = replace
- Canonical 09 = replace
- Canonical 03 = no runtime change
- Canonical 08 = no runtime change
- Canonical 05 = no protocol change
- all other Canonical Sources = no change

Project Source is not updated during this Goal.

## 12. Next boundary and readiness

~~~text
next_boundary = ChatGPT independent acceptance of Baseline v1.4, Project Source synchronization, then one fresh exact MVP-F12-P3 authorization
p3_activation_binding_safe_hash = not_yet_available_requires_fresh_exact_P3_authorization
P3_READY_TO_AUTHORIZE_AFTER_BASELINE_ACCEPTANCE = yes
MVP_F12_P3_authorized = no
MVP_F12_P3_executed = no
MVP_F12_P4_authorized = no
MVP_F12_P4_executed = no
~~~

The P3 readiness field is planning status only and is not P3 authorization.
Do not start P3, P4, or any later phase.
