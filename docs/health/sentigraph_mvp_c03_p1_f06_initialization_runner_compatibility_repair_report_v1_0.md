# Sentigraph MVP-C03-P1 F06 Initialization Runner Compatibility Repair Report v1.0

## 1. Title and Conditional Identity

- conditional_milestone_id = MVP-C03
- prompt_package_id = MVP-C03-P1
- affected_fixed_milestone = MVP-F06
- classification = conditional_allowance
- baseline_version = 1.0
- scope = durable exact-target initialization runner and synthetic compatibility repair only

## 2. Decision

- decision = ready
- privacy_issue_stop = no
- MVP_C03_P1_status = completed
- durable_F06_runner_ready_for_separate_independent_compatibility_recheck = yes
- MVP_F06_effective_acceptance_complete = no

The conditional repair is ready because the durable runner and its bounded result
contract pass the authorized synthetic test matrix. This decision does not
reclassify the historical F06 attempt and does not authorize a formal target run.

## 3. Privacy Status

- protected_value_exposed = no
- raw_exception_exposed = no
- physical_path_exposed = no
- raw_SQL_exposed = no
- raw_key_echoed = no
- raw_value_echoed = no
- local_username_exposed = no
- drive_exposed = no

All terminal results are bounded and value-free. Physical paths, exception text,
SQL text, usernames, drives, source content, and protected values are absent.

## 4. Exact Approval Validation

- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- approval_scope = MVP-C03-P1 only
- formal_logical_target_access_authorized = no
- actual_runtime_enumeration_authorized = no
- protected_payload_or_source_read_authorized = no
- automatic_Git_if_ready_authorized = yes

## 5. Execution Routing and Model Exposure

- interface = Codex
- environment = Local
- execution_route = selected repository plus pytest temporary roots only
- exact_deployment_identifier_exposed_to_assistant = no
- actual_model_claim = current Codex session only

The task recommended a model, but the exact deployment identifier was not exposed
to the assistant. This report therefore makes no unavailable model claim.

## 6. Goal Activation and Completion

- Goal_created = yes
- Goal_activated = yes
- active_Goal_state_observed = yes
- Goal_scope_matched_MVP_C03_P1 = yes
- Goal_completion_condition = implementation_validation_report_and_Git_resolution
- Goal_completed_at_report_finalization = pending_automatic_Git_resolution

The Goal remains active through the required post-report Git ready gate. Final Goal
completion is reported after that gate is resolved.

## 7. Baseline Conditional Accounting

- MVP_C03_P1_prompt_consumed = yes
- MVP_C03_prompt_allowance_consumed = 1
- MVP_C03_prompt_allowance_remaining = 1
- consumed_engineering_prompts_since_baseline = 11
- consumed_fixed_prompts = 6
- consumed_conditional_prompts = 3
- consumed_risk_prompts = 2
- remaining_fixed_prompts = 14
- remaining_conditional_allowance = 7
- remaining_risk_buffer = 2
- MVP_C01_trigger_eligible = yes
- MVP_C01_authorized = no
- MVP_C01_consumed = no
- MVP_C02_status = completed

## 8. Git Preflight

- expected_branch = main
- actual_branch = main
- preflight_HEAD = 03d8ae9c32f33aafa1129dcdf18c1242735d36ea
- preflight_origin_main = 03d8ae9c32f33aafa1129dcdf18c1242735d36ea
- preflight_message = Establish MVP-F05 logical target authorization contract
- tracked_modified_file_count = 0
- staged_file_count = 0
- expected_untracked_historical_F06_report_only = yes
- preflight = pass

## 9. Historical F06 Report Preservation

- historical_first_F06_status = needs_fix
- historical_first_F06_completed = no
- historical_first_F06_reclassified = no
- historical_first_F06_target_initialized = no
- historical_F06_report_preserved = yes
- historical_F06_report_byte_hash_unchanged = yes
- historical_F06_report_byte_sha256 = 4f455eaeef1253f795da3b13b3cb960e5c55349e1858d866178047179b65c214

The historical report remains byte-for-byte unchanged and retains its original
needs-fix decision.

## 10. Originating F06 Failure

- originating_failure_code = unexpected_internal_failure
- root_cause_category = ephemeral_runner_incomplete_safe_diagnostic_state_retention
- historical_actual_session_count = not_conclusively_returned
- historical_actual_transaction_count = not_conclusively_returned
- historical_cleanup_result = not_conclusively_returned
- historical_formal_retry = no

The one approved F06 runner collapsed its failure into a generic code without
returning complete phase, connection, transaction, creation, schema, row-count,
receipt, cleanup, and final-state accounting.

## 11. Confirmed and Unproven Findings

Confirmed:

- The historical runner did not retain a complete bounded diagnostic state.
- Exact post-terminal checks recorded no target, receipt, sidecar, target parent,
  or runtime parent.
- No payload, source, candidate, gate, persistence, or production action occurred.

Not proven:

- The committed SQLite schema is incompatible.
- The locked logical target is unsafe.
- The historical target was successfully created.
- Historical cleanup was performed.
- SQLite was never opened during the historical attempt.

## 12. Selected Repair Architecture

- selected_repair = durable_tracked_bounded_state_machine_runner
- durable_runner_implemented = yes
- local_only = yes
- internal_only = yes
- nonproduction_only = yes
- disabled_by_default_at_non_test_call_sites = yes
- caller_supplied_target_authority = no
- automatic_retry_present = no
- fallback_target_present = no

The runner initializes one complete state object before filesystem operations,
updates it before every operation phase, and always returns a complete bounded
projection.

## 13. Durable Runner Public Surface

The runner exposes one keyword-only function with these inputs:

- repository_root
- expected_target_identity_safe_hash
- expected_target_authorization_contract_safe_hash
- allow_same_run_empty_target_cleanup

There is no target path, receipt path, table, schema, logical-label, environment,
or fallback override.

## 14. Locked Target and DDL Bindings

- target_kind = dedicated_local_sqlite_nonproduction_store
- locked_target_logical_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- target_primary_table = governed_nonproduction_evidence_records_v0_1
- target_attempt_reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- locked_target_identity_hash_verified = yes
- locked_contract_hash_verified = yes
- attempt_DDL_hash_verified = yes
- primary_DDL_hash_verified = yes
- target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b
- target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2
- attempt_table_DDL_safe_hash = 2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266
- primary_table_DDL_safe_hash = d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26

Both F05 hashes were independently reproduced from the two committed normative
JSON objects. Both DDL hashes were reproduced from the exact imported committed
statements before any SQLite access.

## 15. State-machine Phases

- bounded_execution_phase_enum = yes
- execution_phase_count = 26

The bounded phases cover input validation, governance and DDL verification,
exact-path derivation and checks, collision and preexistence classification,
parent creation, one SQLite session, transaction and schema work, schema and row
verification, integrity checking, commit, same-session post-commit verification,
close, exact post-connection checks, receipt build/scan/write/readback, cleanup,
completion, and terminal failure.

## 16. Safe Error Taxonomy

- bounded_safe_error_enum = yes
- safe_error_code_count = 34
- last_resort_code = unexpected_internal_failure

The taxonomy distinguishes input, governance, DDL, repository-root, path,
collision, sidecar, SQLite, transaction, schema, row, integrity, commit,
post-commit, close, receipt, cleanup, and last-resort failures. No error code
contains exception text or a physical value.

## 17. Complete Terminal-result Contract

- durable_runner_result_schema = sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_1
- durable_runner_result_version = 0.1
- required_result_field_count = 87
- complete_terminal_result_fields = yes
- every_terminal_path_returns_all_fields = yes
- bounded_unavailable_values = yes
- unexpected_internal_failure_retains_complete_state = yes

Every success and injected failure returns exactly the required result fields.
Unreached operations use explicit bounded states rather than missing keys.

## 18. Exception and Finally Behavior

- exception_escapes = no
- opened_connection_closed_in_finally = yes
- retained_counters_survive_failure = yes
- target_creation_state_retained = yes
- commit_ambiguity_retained = yes
- result_assembly_fallback_complete = yes

The runner never opens another connection for diagnosis. Known precommit failure
rolls back when possible; ambiguous commit state is preserved and never cleaned.

## 19. Exact-path and No-enumeration Policy

- exact_locked_components_only = yes
- lexical_repository_escape_check = yes
- symlink_check = yes
- junction_or_reparse_check = yes
- mount_boundary_check = yes
- exact_collision_check = yes
- runtime_enumeration_API_present = no
- wildcard_or_latest_file_discovery = no
- recursive_delete = no

Only the exact root, locked components, target, receipt, and three known SQLite
sidecar labels are inspected.

## 20. Single SQLite Session Contract

- single_SQLite_session_enforced = yes
- SQLite_connection_session_limit = 1
- SQLite_connection_reopen_count = 0
- automatic_retry_present = no
- second_attempt_present = no
- absent_branch_connection_mode = one_read_write_create_session
- existing_branch_connection_mode = one_URI_read_only_query_only_session
- candidate_writer_reachable = no
- reservation_writer_reachable = no

## 21. Schema Inventory and Zero-DML Behavior

- exact_imported_DDL_only = yes
- expected_user_table_count = 2
- unexpected_named_index_allowed = no
- unexpected_trigger_allowed = no
- unexpected_view_allowed = no
- target_schema_inventory_safe_hash_returned = yes
- base_record_row_count_required = 0
- attempt_reservation_row_count_required = 0
- candidate_table_DML_statement_count = 0
- attempt_table_DML_statement_count = 0
- other_user_DML_statement_count = 0
- migration_operation_executed = no

The safe inventory hashes structural metadata only. It returns no SQL, physical
path, or row value.

## 22. Receipt Construction and Privacy Behavior

- initialization_receipt_schema = sentigraph_mvp_f06_exact_logical_target_initialization_receipt_v1_0
- initialization_receipt_version = 1.0
- canonical_UTF8_JSON = yes
- exclusive_create = yes
- overwrite_allowed = no
- flush_and_fsync = yes
- readback_count = 1
- strict_object_equality = yes
- safe_hash_verified = yes
- byte_sha256_verified = yes
- protected_value_scanner_passed = yes
- receipt_contains_physical_path = no
- receipt_contains_SQL = no
- receipt_contains_exception = no

## 23. Bounded Cleanup Behavior

- cleanup_exact_known_paths_only = yes
- same_run_uncommitted_target_cleanup_proven = yes
- same_run_sidecar_cleanup_proven = yes
- same_run_empty_parent_cleanup_proven = yes
- preexisting_target_preserved = yes
- preexisting_sidecar_preserved = yes
- committed_target_preserved = yes
- ambiguous_commit_target_preserved = yes
- successful_receipt_target_preserved = yes
- partial_cleanup_reports_needs_fix = yes
- cleanup_count_accounting = exact

## 24. TDD RED

- TDD_RED = one_collection_error_import_failure_runner_module_not_yet_present
- TDD_RED_genuine = yes
- TDD_RED_runner_tests_executed = 0
- TDD_RED_sensitive_exception_text_copied = no

The focused test module was created before the runner. The first run failed at
collection because the runner module did not yet exist.

## 25. Focused GREEN

- focused_runner_tests = 74 passed
- focused_runner_test_duration_latest = 1.24s
- focused_runner_failures = 0
- focused_runner_errors = 0

## 26. Nearby Regressions

- persistence_regressions = 68 passed
- scanner_regressions = 57 passed
- safe_receipt_auditor_regressions = 155 passed
- combined_nearby_suite = 354 passed
- combined_nearby_suite_duration_latest = 2.94s
- full_pytest_run = no

## 27. Failure-injection Matrix

- failure_injection_cases_passed = 27
- governance_failure_covered = yes
- DDL_failure_covered = yes
- path_and_collision_failures_covered = yes
- SQLite_and_transaction_failures_covered = yes
- both_DDL_failures_covered = yes
- schema_row_integrity_failures_covered = yes
- known_and_ambiguous_commit_failures_covered = yes
- close_and_post_connection_failures_covered = yes
- receipt_build_scan_write_readback_hash_failures_covered = yes
- cleanup_and_last_resort_failures_covered = yes

Every injected failure returns all 87 fields with bounded phases, bounded error
codes, truthful counters, explicit cleanup state, and no raw exception or path.

## 28. Value-free Diagnostic Proof

- physical_temporary_path_in_result = no
- local_username_in_result = no
- drive_in_result = no
- SQL_in_result = no
- exception_class_or_message_in_result = no
- raw_field_finding_in_result = no
- raw_value_in_result = no
- safe_full_SHA256_phone_pattern_exception_test = pass
- genuine_phone_pattern_scanner_test = pass
- deterministic_result_across_temporary_roots = pass
- caller_inputs_mutated = no

## 29. Formal-target Isolation Proof

- synthetic_temporary_repository_only = yes
- synthetic_temporary_SQLite_only = yes
- actual_Git_root_passed_to_runner = no
- formal_logical_target_accessed = no
- actual_runtime_enumerated = no
- formal_initialization_receipt_accessed = no
- formal_runtime_parent_created = no
- autouse_root_observer_enabled_for_every_test = yes
- test_source_contains_formal_target_literal = no

Every runner call in the focused suite is dynamically observed and constrained to
its pytest temporary root or a child of that root.

## 30. No-payload and No-source Proof

- protected_payload_read = no
- protected_capture_receipt_read = no
- source_or_package_read = no
- source_row_read = no
- real_candidate_identity_used = no
- network_accessed = no

## 31. No-gate, Persistence, or Production Proof

- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no
- MVP_C03_P2_authorized = no
- MVP_C03_P2_executed = no
- MVP_F07_eligible = no
- MVP_F07_authorized = no
- MVP_F07_executed = no
- MVP_F08_authorized = no
- MVP_F08_executed = no

## 32. Git Auto-commit and Push Result

- Git_ready_gate_at_report_finalization = pass
- automatic_commit_and_push_required_after_report_finalization = yes
- staged_file_count_at_report_finalization = 0
- intended_commit_message = Repair MVP-C03-P1 F06 initialization runner diagnostics
- tag = no
- force_push = no
- history_rewrite = no
- final_commit_SHA = reported_externally_after_non_self_referential_commit
- push_result = reported_externally_after_report_is_committed

The final commit SHA cannot be embedded in the report that contributes to that
same commit. The exact SHA, push outcome, committed inventory, and final worktree
state are therefore returned by Codex after the required Git operation.

## 33. Project Source Recommendation

- Canonical_00_update = no
- Canonical_09_update = no
- Canonical_03_update = no
- Canonical_05_update = no
- Source_11_update = no

C03-P1 repairs and validates only the synthetic durable runner. It does not
complete F06 or alter formal target state.

## 34. Next Boundary

- next_recommended_conditional_boundary = MVP-C03-P2 Independent Runner Acceptance and One Exact-target F06 Recheck
- next_boundary_requires_separate_exact_approval = yes
- MVP_C03_P2_authorized = no
- MVP_C03_P2_executed = no
- MVP_F06_effective_acceptance_complete = no
- MVP_F07_eligible = no

No next-boundary operation was executed by MVP-C03-P1.

## Required Validation Summary

- py_compile = pass
- AST_static_scan = pass
- forbidden_integration_scan = pass
- no_index_whitespace_check = pass
- git_diff_check = pass
- historical_F06_report_byte_hash_unchanged = yes
- actual_runtime_accessed = no
- formal_target_accessed = no
- exact_allowed_change_set = exact_four_files
