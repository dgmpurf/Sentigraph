# Sentigraph MVP-F06 Exact Logical Target Initialization Smoke Report v1.0

## 1. Title and Milestone Identity

- milestone_id = MVP-F06
- prompt_package_id = MVP-F06-P1
- baseline_version = 1.0
- baseline_task_classification = planned_fixed_milestone
- milestone_title = Exact Logical Target Initialization Smoke
- report_schema = sentigraph_mvp_f06_exact_logical_target_initialization_smoke_report_v1_0
- report_version = 1.0

## 2. Decision

- decision = needs_fix
- MVP_F06_status = needs_fix
- target_initialized = no
- target_initialization_outcome = not_completed
- eligible_for_separate_MVP_F07_gate_activation_decision = no

The one approved F06 procedure terminated with the safe error code
unexpected_internal_failure before it could return its bounded session,
transaction, schema, row-count, cleanup, or receipt accounting. The operation
was not retried. Exact post-terminal metadata checks found no target, receipt,
SQLite sidecar, exact target parent, or runtime parent. That clean final
filesystem state does not supply the missing execution proof and therefore
cannot be promoted to ready.

## 3. Privacy Status

- privacy_issue_stop = no
- protected_value_exposed = no
- physical_absolute_path_recorded = no
- local_username_recorded = no
- drive_letter_recorded = no
- raw_SQL_recorded = no
- exception_dump_recorded = no
- protected_payload_read = no
- safe_capture_receipt_read = no
- source_or_package_read = no
- raw_candidate_identity_read = no

Only safe logical labels, committed schema identifiers, safe hashes, bounded
counts, and safe outcome codes are recorded.

## 4. Exact Approval Validation

The exact approval received for MVP-F06-P1 was:

APPROVE_SENTIGRAPH_MVP_F06_EXACT_LOGICAL_NONPRODUCTION_SQLITE_TARGET_INITIALIZATION_SMOKE_SINGLE_SESSION_WITH_BOUNDED_SAME_RUN_EMPTY_TARGET_CLEANUP_NO_PAYLOAD_READ_NO_CANDIDATE_OR_RESERVATION_WRITE_NO_GATE_ACTIVATION_NO_PRODUCTION

- exact_approval_received = yes
- exact_approval_valid_for_MVP_F06_P1 = yes
- approval_scope_respected = yes
- second_initialization_attempt_authorized = no
- automatic_retry_allowed = no
- F07_authorized_by_phrase = no
- F08_authorized_by_phrase = no

The approval permitted one exact-target initialization smoke only. It did not
authorize retry, candidate persistence, reservation creation, gate activation,
actual write, or production behavior.

## 5. Execution Routing and Model Exposure

- execution_interface = Codex
- execution_environment = local
- execution_mode = Goal
- requested_model_recommendation = GPT-5.6 Sol
- requested_reasoning_effort = Extra High
- actual_model_exposure = current_Codex_session
- exact_deployment_identifier_exposed = no
- unavailable_deployment_identifier_claimed = no

The requested model name is recorded as a recommendation only because the exact
deployment identifier was not exposed.

## 6. Goal Activation and Completion

- goal_created = yes
- goal_activated = yes
- active_goal_state_observed = yes
- goal_scope_matched_MVP_F06 = yes
- stop_condition_reached = yes
- stop_condition = bounded_runner_returned_unexpected_internal_failure
- goal_completed = yes
- goal_terminal_classification = completed_with_needs_fix_pause

Goal completion here means the required safe terminal outcome, report, and
pause were reached. It does not mean F06 initialization succeeded.

## 7. Baseline Prompt Accounting

- fixed_prompt_budget = 20
- conditional_prompt_allowance = 10
- risk_buffer_prompt_allowance = 4
- MVP_F06_prompt_consumed = yes
- consumed_engineering_prompts_since_baseline = 10
- consumed_fixed_prompts = 6
- consumed_conditional_prompts = 2
- consumed_risk_prompts = 2
- remaining_fixed_prompts = 14
- remaining_conditional_allowance = 8
- remaining_risk_buffer = 2
- MVP_C01_trigger_eligible = yes
- MVP_C01_authorized = no
- MVP_C01_consumed = no
- MVP_C02_status = completed
- MVP_C02_prompt_allowance_remaining = 0

The fixed F06 Prompt is consumed regardless of this needs-fix result.

## 8. Git Preflight

- expected_branch = main
- observed_branch = main
- expected_HEAD = 03d8ae9c32f33aafa1129dcdf18c1242735d36ea
- observed_HEAD = 03d8ae9c32f33aafa1129dcdf18c1242735d36ea
- observed_HEAD_message = Establish MVP-F05 logical target authorization contract
- main_aligned_with_origin_main = yes
- ahead_count = 0
- behind_count = 0
- worktree_clean_before_F06 = yes
- F06_report_preexisting = no
- required_tracked_evidence_complete = yes
- exact_target_ignored = yes
- exact_initialization_receipt_ignored = yes
- exact_runtime_paths_tracked = no
- staged_path_count_before_F06 = 0

## 9. F05 Target-identity and Contract-hash Verification

- target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b
- target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2
- F05_normative_JSON_block_count = 2
- F05_target_identity_hash_verified = yes
- F05_contract_hash_verified = yes
- F05_decision_identity_hash_match = yes
- F05_decision_contract_hash_match = yes
- F05_exact_locked_target_match = yes

Both hashes were independently recomputed from the committed normative JSON
before any target access.

## 10. Static Schema Inventory

- logical_repository_relative_target_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- target_primary_table = governed_nonproduction_evidence_records_v0_1
- target_attempt_reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- expected_user_table_count = 2
- expected_named_index_count = 0
- expected_internal_autoindex_count = 6
- expected_trigger_count = 0
- expected_view_count = 0
- expected_foreign_key_count = 0
- committed_initializer_connection_call_count = 1
- committed_initializer_DDL_execute_call_count = 2
- committed_initializer_commit_call_count = 1
- committed_initializer_close_call_count = 1
- committed_initializer_forbidden_DML_count = 0
- committed_constructor_connection_call_count = 0
- committed_constructor_filesystem_mutation_token_count = 0

Attempt-reservation table:

- column_count = 19
- TEXT_column_count = 17
- INTEGER_column_count = 2
- explicit_NOT_NULL_count = 18
- default_value_count = 0
- primary_key_count = 1
- unique_constraint_count = 2
- CHECK_constraint_count = 5
- primary_key_column = attempt_reservation_id
- unique_columns = attempt_scope_key, idempotency_key
- committed_DDL_safe_hash = 2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266

Primary record table:

- column_count = 39
- TEXT_column_count = 32
- INTEGER_column_count = 7
- explicit_NOT_NULL_count = 36
- nullable_business_column_count = 2
- default_value_count = 0
- primary_key_count = 1
- unique_constraint_count = 2
- CHECK_constraint_count = 16
- primary_key_column = persisted_record_id
- unique_columns = candidate_identity_digest, idempotency_key
- committed_DDL_safe_hash = d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26

No named index, trigger, view, migration, ALTER operation, initializer DML, or
hidden constructor mutation was present in the committed implementation.

## 11. Exact Target-path Derivation

- target_derived_from_Git_root = yes
- target_derived_from_F05_locked_logical_label = yes
- caller_supplied_target_used = no
- environment_override_used = no
- alternate_target_used = no
- fallback_target_used = no
- parent_traversal_allowed = no
- absolute_input_allowed = no
- runtime_directory_enumerated = no

The procedure contained only the locked logical component sequence. No
directory listing, glob, walk, search, or latest-file selection was used.

## 12. Path, Symlink, Junction, and Reparse Checks

- path_escape_check_passed = no
- symlink_check_passed = no
- junction_check_passed = no
- reparse_point_check_passed = no
- mount_boundary_check_passed = no
- check_result_semantics = not_conclusively_returned

The no values mean the checks were not conclusively reported by the terminated
procedure, not that an unsafe component was observed. No readiness claim may be
derived from an unreturned check result.

## 13. Exact Collision Checks

- initialization_receipt_preexistence_result = not_conclusively_returned
- target_collision_result = not_conclusively_returned
- preexisting_sidecar_result = not_conclusively_returned
- post_terminal_exact_target_exists = no
- post_terminal_exact_initialization_receipt_exists = no
- post_terminal_journal_sidecar_exists = no
- post_terminal_WAL_sidecar_exists = no
- post_terminal_SHM_sidecar_exists = no
- post_terminal_exact_target_parent_exists = no
- post_terminal_runtime_parent_exists = no

Post-terminal checks used exact path metadata only. They did not enumerate
runtime or inspect database or receipt content.

## 14. Target Preexistence Classification

- target_preexistence_classification = unsafe_or_ambiguous
- target_preexistence_reason = bounded_procedure_did_not_return_its_classification
- initial_target_existence_check_count = not_conclusively_recorded
- post_terminal_exact_target_metadata_check_count = 1
- target_preexistence_guessed = no

Although the final target is absent, the report cannot distinguish never
created from created-then-eligible-cleanup without the missing runner result.

## 15. Single SQLite Session Accounting

- SQLite_connection_session_limit = 1
- SQLite_connection_open_count = 0_or_1_not_conclusively_recorded
- SQLite_connection_reopen_count = 0
- SQLite_create_count = 0_or_1_not_conclusively_recorded
- second_initialization_attempt_performed = no
- automatic_retry_performed = no
- runner_static_connect_branch_cardinality = one_mutually_exclusive_connect_call

The approved runner was executed exactly once and contained no code path that
could reopen SQLite. Its actual open count was not returned, so the stronger
ready proof is unavailable.

## 16. Initialization or Existing-target Verification Branch

- selected_branch = not_conclusively_returned
- absent_target_branch_completed = no
- existing_target_read_only_branch_completed = no
- target_initialization_outcome = not_completed
- target_initialized = no
- schema_only_initialization_proven = no
- read_only_exact_conformance_proven = no

The first attempt to pass the full script as a PowerShell command was rejected
by the Windows command-length limit before process creation. That transport
failure performed no target operation. The same program was then compiled and
executed once through interactive standard input; that single approved
execution returned unexpected_internal_failure. It was not retried.

## 17. Schema, Table, Index, and Constraint Verification

- target_primary_table_verified = no
- target_attempt_reservation_table_verified = no
- target_indexes_verified = no
- target_constraints_verified = no
- unexpected_user_schema_object_count = not_available
- target_schema_inventory_safe_hash = not_available
- target_schema_exact_conformance_proven = no

Static committed schema inventory is complete, but target-side verification did
not return. Static design evidence is not substituted for runtime conformance.

## 18. Zero-row Verification

- base_record_row_count = not_available
- attempt_reservation_row_count = not_available
- zero_candidate_record_state_proven = no
- zero_attempt_reservation_state_proven = no
- row_content_inspected = no

No row content was accessed. The final absence of the target is not represented
as a successful zero-row target verification.

## 19. DML Zero-mutation Proof

- candidate_table_DML_statement_count = 0
- attempt_table_DML_statement_count = 0
- other_user_DML_statement_count = 0
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- payload_insert_count = 0
- receipt_insert_count_into_SQLite = 0
- identity_insert_count = 0
- activation_decision_insert_count = 0
- DML_trace_result_returned = no
- zero_DML_basis = approved_runner_contains_no_user_DML_statement

The bounded runner contained only exact DDL, transaction control, schema
introspection, row counts, query-only controls, and quick-check operations. It
contained no INSERT, UPDATE, DELETE, REPLACE, UPSERT, writer invocation,
candidate creation, or reservation creation.

## 20. Integrity Check

- integrity_check = not_run
- integrity_result_returned = no
- integrity_pass_claimed = no

A quick-check pass was required for ready, but no result was returned and no
target remains for a permitted same-session result.

## 21. Commit or Read-only Verification Outcome

- transaction_begin_count = not_conclusively_recorded
- commit_call_count = 0
- rollback_count = not_conclusively_recorded
- successful_initialization_commit = no
- ambiguous_commit_claimed = no
- read_only_verification_completed = no

No successfully committed target can be claimed. A successful commit would
have required target preservation, while the exact final target is absent.

## 22. Sidecar and Post-connection State

- final_target_exists = no
- final_target_regular_file_verified = no
- final_sidecar_count = 0
- final_receipt_exists = no
- final_exact_target_parent_exists = no
- final_runtime_parent_exists = no
- SQLite_reopened_for_post_check = no
- database_bytes_read_after_terminal_failure = no
- database_content_hashed = no

## 23. Bounded Cleanup Eligibility and Result

- cleanup_eligible = no
- cleanup_performed = not_conclusively_recorded
- cleanup_file_count = not_conclusively_recorded
- cleanup_directory_count = not_conclusively_recorded
- post_terminal_manual_cleanup_performed = no
- cleanup_effective_post_state = no_exact_runtime_artifact_or_parent_remains

Cleanup eligibility is no because the runner did not return the evidence needed
to prove all cleanup predicates. No additional cleanup was attempted after the
terminal result. The exact final state was already empty.

## 24. Initialization Receipt Construction

- initialization_receipt_artifact_count = 0
- initialization_receipt_safe_hash = not_created
- initialization_receipt_byte_sha256 = not_created
- initialization_receipt_object_completed = no
- physical_absolute_path_recorded = no
- protected_value_recorded = no

## 25. Receipt Privacy Scan

- receipt_privacy_scan_executed = no
- receipt_privacy_scan_passed = no
- receipt_privacy_finding_count = not_available
- protected_value_exposed = no
- raw_key_echoed = no
- raw_value_echoed = no

No F06 receipt existed to scan after the terminal failure.

## 26. Receipt Exclusive Write and Readback

- initialization_receipt_exclusive_write_performed = no
- initialization_receipt_readback_verified = no
- initialization_receipt_overwritten = no
- initialization_receipt_deleted = no
- initialization_receipt_retry_performed = no

## 27. No-payload and No-source Proof

- protected_payload_read = no
- protected_payload_stat_performed = no
- protected_capture_receipt_read = no
- protected_capture_receipt_stat_performed = no
- source_or_package_read = no
- source_row_read = no
- evidence_items_JSONL_read = no
- approved_row_file_read = no
- candidate_reconstructed = no
- candidate_identity_artifact_read = no

The procedure imported only tracked code definitions and did not reference any
protected artifact or source location.

## 28. No-gate, No-persistence, and No-production Proof

- persistence_store_invoked = no
- public_writer_invoked = no
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_prepared = no
- gate_activated = no
- persistence_executed = no
- actual_write_performed = no
- production_evidenceitem_created = no
- production_object_created = no
- route_or_API_changed = no
- frontend_changed = no
- provider_or_collector_called = no
- network_called = no

## 29. Effective F06 Outcome

- effective_F06_outcome = needs_fix_pause_with_no_remaining_runtime_artifacts
- target_initialized = no
- target_verified_exact_empty = no
- F06_ready = no
- eligible_for_separate_MVP_F07_gate_activation_decision = no
- MVP_F07_authorized = no
- MVP_F07_executed = no
- MVP_F08_authorized = no
- MVP_F08_executed = no
- next_default = pause

The missing bounded runner result is a proof failure. The absent final target
does not authorize a second attempt.

## 30. Git Auto-commit and Push Result

- auto_commit_eligibility = no
- report_staged = no
- commit_performed = no
- push_performed = no
- tag_created = no
- force_push_performed = no
- history_rewritten = no

The task requires no staging, commit, or push when decision is needs_fix.

## 31. Project Source Recommendation

- Canonical_00_update = no
- Canonical_09_update = no
- Canonical_03_update = no
- Canonical_05_update = no
- Source_11_update = no
- Project_Source_update_reason = F06_not_completed

No Source record should claim target initialization or exact-empty
verification.

## 32. Next Boundary

- next_recommended_action = pause_for_independent_review_of_F06_runner_failure
- automatic_F06_retry_recommended = no
- fresh_governance_required_before_any_new_target_attempt = yes
- F07_recommended_now = no
- F07_authorized_now = no
- persistence_authorized_now = no

Any later work should first review the bounded runner's safe diagnostic design
and decide whether a separately approved F06 repair attempt is warranted. This
report does not create or imply that approval.
