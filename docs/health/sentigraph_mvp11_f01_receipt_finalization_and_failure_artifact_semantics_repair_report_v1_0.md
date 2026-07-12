# Sentigraph MVP11-F01 Receipt Finalization and Failure-artifact Semantics Repair Report v1.0

## 1. Decision

- phase = MVP11-F01
- decision = ready
- privacy_issue_stop = no
- MVP11_F01_status = candidate_completed_pending_chatgpt_acceptance
- actual_model_deployment_identifier = hidden_by_current_Codex_session
- Goal_created = yes
- Goal_activated = yes
- active_Goal_state_observed = yes
- Goal_completed = yes

This decision covers one synthetic-only receipt-finalization repair. It does
not authorize or execute MVP11-F02, access the actual Sentigraph runtime or
formal target, activate a gate, execute persistence, or create a production
object.

## 2. Starting State and Accounting

- repository_identity = dgmpurf/Sentigraph
- branch = main
- starting_HEAD = 649eba241c34da8c367d1b24df7841dbedad977b
- starting_origin_main = 649eba241c34da8c367d1b24df7841dbedad977b
- starting_ahead_behind = 0/0
- starting_worktree_clean = yes
- frozen_input_runner_sha256 = 8da67238eebf30c915723b6dfe685ec797354edf53c30246ec060cad46d22eec
- frozen_input_test_sha256 = 1272ab8ffd0c76e384fa4d45cfef9d57e28b083af77e07a9ab620c423d52fd7b
- consumed_engineering_prompts_since_v1_1_baseline = 1
- consumed_fixed_prompts_since_v1_1 = 1
- consumed_conditional_prompts_since_v1_1 = 0
- consumed_risk_prompts_since_v1_1 = 0
- remaining_fixed_prompts = 15
- remaining_conditional_allowance = 6
- remaining_risk_buffer = 2

## 3. Confirmed Defects and TDD RED

- durable_receipt_self_finalization_defect_confirmed = yes
- post_create_unaccepted_receipt_artifact_defect_confirmed = yes
- TDD_RED = 2_failed
- TDD_RED_test_1 = test_tdd_red_durable_receipt_has_no_self_finalization_claims
- TDD_RED_assertion_1 = forbidden_exact_fields_isdisjoint_receipt_was_false
- TDD_RED_test_2 = test_tdd_red_fsync_failure_removes_exact_same_run_unaccepted_receipt
- TDD_RED_assertion_2 = exact_receipt_path_still_existed_after_fsync_failure

The pre-repair receipt was built before creation, fsync, and readback but
contained `formal_receipt_write_completed` and
`formal_receipt_readback_completed`. A synthetic fsync failure also left the
same-run unaccepted receipt beside a successfully committed exact-empty target.

## 4. Contract Repair

- result_schema = sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_4
- result_version = 0.4
- receipt_schema = sentigraph_governed_nonproduction_target_initialization_receipt_v0_3
- receipt_version = 0.3
- durable_formal_receipt_write_completed_field_removed = yes
- durable_formal_receipt_readback_completed_field_removed = yes
- equivalent_receipt_self_finalization_claims_prohibited = yes
- outer_result_records_write_state = yes
- outer_result_records_flush_state = yes
- outer_result_records_fsync_state = yes
- outer_result_records_readback_and_object_equality_state = yes
- outer_result_records_safe_hash_and_byte_hash_state = yes
- outer_result_records_finalization_state = yes
- receipt_privacy_scanner_preserved = yes

Durable receipt bytes retain only facts established before byte construction.
They do not claim their own write, flush, fsync, readback, equality, hash
verification, finalization, or independent acceptance has completed.

## 5. Same-run Failure-artifact Disposition

- exclusive_creation_required = yes
- created_handle_identity_bound_internally = yes
- raw_file_identity_exposed = no
- receipt_preexistence_must_be_false = yes
- ordinary_non_reparse_file_required = yes
- current_identity_must_match_created_handle = yes
- receipt_cleanup_attempt_maximum = 1
- exact_path_absence_verified_after_cleanup = yes
- directory_enumeration_used = no
- wildcard_or_recursive_cleanup_used = no
- alternate_path_cleanup_used = no
- overwrite_or_receipt_retry_used = no
- preexisting_receipt_deletion_allowed = no

The closed classifications are `not_applicable`, `not_created`,
`accepted_receipt_preserved`,
`removed_exact_same_run_unaccepted_receipt`, and
`incomplete_unaccepted_receipt_artifact`. Identity absence, mismatch,
replacement, unlink failure, or ambiguous absence verification leaves the
artifact unaccepted and pauses without another deletion or runner attempt.

## 6. Target Preservation and Safety

- successfully_committed_target_deleted_for_receipt_failure = no
- existing_target_modified_for_receipt_failure = no
- existing_target_byte_stability_verified = yes
- exact_empty_target_preserved_after_receipt_failure = yes
- pre_commit_target_cleanup_contract_preserved = yes
- SQLite_connection_session_limit = 1
- SQLite_connection_reopen_count = 0
- candidate_DML_count = 0
- reservation_DML_count = 0
- other_user_DML_count = 0
- automatic_retry = false
- second_attempt = false

Receipt-artifact disposition is separate from the existing pre-commit target
cleanup procedure. A successful or ambiguous target commit is never rolled
back or deleted because receipt finalization later fails.

## 7. Validation

- focused_runner_tests = 124_passed
- focused_new_failure_and_identity_tests = pass
- governed_persistence_regressions = 68_passed
- protected_value_scanner_regressions = 57_passed
- safe_receipt_auditor_regressions = 155_passed
- combined_nearby_synthetic_suite = 404_passed
- py_compile = pass
- AST_and_forbidden_capability_scan = pass
- exact_single_receipt_unlink_site_scan = pass
- durable_receipt_field_scan = pass
- privacy_and_value_free_diagnostic_scan = pass
- git_diff_check = pass
- no_index_whitespace_check = pass

The focused matrix covers pre-create failure, partial write, flush, fsync,
readback, object mismatch, safe-hash, byte/post-write state, identity mismatch,
actual same-path replacement, identity unavailability, unlink failure,
preexisting receipt collision, successful synthetic and formal fixtures, and
existing-target byte stability. Every runner call used a pytest temporary Git
root and temporary SQLite target.

## 8. Frozen Acceptance

- runner_module_sha256 = 841702c8464dc33385f959ced0392fa29e5b78adfa4203b0eedaee75daf7b995
- runner_test_sha256 = 81b48907922676b7b0cddd17b4c6ab9a8044c6e1688c1c18851e4cf1ad891918
- F01_report_sha256_before_commit = eb1455b8feb92fcdaa154b6c77f95e405d7c4e86bb77e900a8bf193f778c3ad6
- F01_report_sha256_scope = UTF8_report_bytes_with_only_the_F01_report_sha256_before_commit_value_replaced_by_64_zeroes
- frozen_read_only_acceptance = pass
- post_acceptance_hash_equality = pass
- frozen_acceptance_attempt_count = 1

The self-field-excluded report hash permits this report to record a stable
scope. The final Codex receipt records the full frozen report byte hash without
editing any frozen file.

## 9. Exact Change Inventory

- changed_file_count = 3
- modified_file_1 = backend/app/services/governed_nonproduction_target_initialization_smoke.py
- modified_file_2 = backend/app/tests/test_governed_nonproduction_target_initialization_smoke.py
- created_file_3 = docs/health/sentigraph_mvp11_f01_receipt_finalization_and_failure_artifact_semantics_repair_report_v1_0.md
- fourth_file_changed = no
- persistence_service_changed = no
- route_or_API_changed = no
- frontend_changed = no
- configuration_or_workflow_changed = no
- Project_Source_changed = no

## 10. Isolation and No-overreach Proof

- actual_Sentigraph_root_passed_to_runner = no
- actual_git_config_read = no
- actual_runtime_enumerated = no
- formal_logical_target_accessed = no
- formal_initialization_receipt_accessed = no
- protected_payload_read = no
- protected_capture_receipt_read = no
- source_or_package_read = no
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no
- network_called = no
- subprocess_called = no
- provider_or_collector_called = no
- Quant_or_other_project_accessed = no
- runtime_artifact_staged = no

All formal-profile tests used exact temporary fixtures. No test received the
actual Sentigraph repository root.

## 11. Git and Next Boundary

- required_commit_message = Complete MVP11-F01 receipt finalization repair
- commit_result = pending_ready_only_auto_commit
- push_result = pending_ready_only_auto_push
- tag = no
- next_boundary = ChatGPT independent acceptance of MVP11-F01
- MVP11_F02_authorized = no
- MVP11_F02_executed = no
- effective_MVP_F06_completed = no
- MVP_F07_eligible = no
- Project_Source_update = no

The old P2 approval is not reusable. No subsequent Goal or formal execution is
started by this report.
