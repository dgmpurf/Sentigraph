# Sentigraph MVP-C03-P1-R1 F06 Initialization Runner Synthetic Repair and Acceptance Report v1.0

## 1. Conditional Milestone Identity

- conditional_milestone_id = MVP-C03
- prompt_package_id = MVP-C03-P1-R1
- affected_fixed_milestone = MVP-F06
- classification = conditional_allowance
- report_schema = sentigraph_mvp_c03_p1_r1_f06_initialization_runner_synthetic_repair_and_acceptance_report_v1_0
- report_version = 1.0

## 2. Decision

- decision = ready
- privacy_issue_stop = no
- MVP_C03_P1_R1_status = candidate_completed_pending_chatgpt_acceptance
- durable_F06_runner_ready_for_future_separate_formal_recheck = yes

This decision applies only to the new backend-only runner and its synthetic
temporary-root acceptance evidence. It does not initialize, inspect, or verify
the formal logical target and does not complete MVP-F06.

## 3. Prompt Accounting

- MVP_C03_P1_R1_prompt_consumed = yes
- MVP_C03_prompt_allowance_consumed = 2
- MVP_C03_prompt_allowance_remaining = 0
- consumed_engineering_prompts_since_baseline = 12
- consumed_fixed_prompts = 6
- consumed_conditional_prompts = 4
- consumed_risk_prompts = 2
- remaining_fixed_prompts = 14
- remaining_conditional_allowance = 6
- remaining_risk_buffer = 2

## 4. Recovered Starting State

- starting_HEAD = e2c837a71e635ee5d5f032e51f045b5f143f4807
- starting_origin_main = e2c837a71e635ee5d5f032e51f045b5f143f4807
- starting_tracked_tree = b6c39414ecd33275eb107f3d85d72af2852e4980
- tracked_tree_matches_F05 = yes
- valid_F05_checkpoint = 03d8ae9c32f33aafa1129dcdf18c1242735d36ea
- incident_e33443c_reused = no

The reverted incident remains public-history audit context only. Its patch,
blobs, implementation, tests, and validation results were not inspected or
used.

## 5. Historical F06 Preservation

- historical_first_F06_status = needs_fix
- historical_first_F06_completed = no
- historical_first_F06_reclassified = no
- historical_first_F06_target_initialized = no
- historical_F06_report_preserved = yes
- historical_F06_report_byte_hash_unchanged = yes
- historical_F06_report_sha256 = 4f455eaeef1253f795da3b13b3cb960e5c55349e1858d866178047179b65c214

The historical report was not edited, normalized, regenerated, or re-encoded.
It is included in the candidate commit as historical needs-fix evidence, not as
a reclassified success report.

## 6. Locked Governance Verification

- target_kind = dedicated_local_sqlite_nonproduction_store
- locked_target_logical_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- locked_receipt_logical_label = runtime/governed_nonproduction_evidence_persistence/target-initialization-receipt-6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b.json
- target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b
- target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2
- attempt_table_DDL_safe_hash = 2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266
- primary_table_DDL_safe_hash = d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26
- locked_governance_hashes_verified_before_SQLite = yes
- committed_DDL_hashes_verified_before_SQLite = yes

Both governance hashes were recomputed from the two normative current F05 JSON
blocks. Both DDL hashes were recomputed from the current committed Python string
constants before any synthetic SQLite access.

## 7. Durable Runner Result Contract

- durable_runner_implemented = yes
- result_schema = sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_1
- complete_terminal_result_fields = yes
- bounded_execution_phase_enum = yes
- bounded_safe_error_enum = yes
- unexpected_internal_failure_retains_complete_state = yes
- disabled_by_default = yes
- exact_target_only = yes
- caller_supplied_target_or_receipt_path = no
- environment_target_override = no
- fallback_target = no
- automatic_retry_present = no
- second_attempt_present = no
- no_module_level_mutable_execution_state = yes

Every terminal return has the same complete field set. Unreached values retain
bounded status labels or zero/false counters; raw exception text is never
returned.

## 8. Single SQLite Session and Schema-only Boundary

- single_SQLite_session_enforced = yes
- SQLite_connection_session_limit = 1
- SQLite_connection_open_count_maximum = 1
- SQLite_connection_reopen_count = 0
- absent_target_explicit_transaction = yes
- absent_target_commit_count = 1
- same_session_post_commit_verification = yes
- existing_target_URI_read_only = yes
- existing_target_query_only = yes
- existing_target_commit_count = 0
- existing_target_byte_hash_unchanged = yes
- exact_expected_user_table_count = 2
- exact_expected_internal_autoindex_count = 6
- zero_named_indexes = yes
- zero_triggers = yes
- zero_views = yes
- zero_foreign_keys = yes
- exact_columns_and_constraints_verified = yes
- candidate_table_DML_statement_count = 0
- attempt_table_DML_statement_count = 0
- other_user_DML_statement_count = 0
- candidate_writer_reachable = no
- reservation_writer_reachable = no

The runner imports the current committed DDL constants but does not invoke the
governed candidate writer, reservation writer, or any generic case store.

## 9. Path, Collision, and Cleanup Safety

- locked_paths_derived_internally = yes
- repository_escape_rejected = yes
- parent_traversal_rejected = yes
- absolute_logical_input_rejected = yes
- drive_or_UNC_substitution_rejected = yes
- symlink_or_reparse_component_rejected = yes
- mount_or_device_boundary_checked = yes
- target_directory_collision_rejected = yes
- receipt_preexistence_rejected = yes
- exact_journal_WAL_SHM_collision_rejected = yes
- runtime_enumeration_API_present = no
- wildcard_or_recursive_cleanup_present = no
- bounded_same_run_cleanup_implemented = yes
- preexisting_target_cleanup_allowed = no
- committed_target_cleanup_allowed = no
- ambiguous_commit_target_cleanup_allowed = no
- successful_receipt_target_cleanup_allowed = no

Cleanup uses only exact known target, sidecar, and same-run-created parent paths.
It is eligible only before a conclusive commit, with zero user DML, no final
receipt, conclusive absence before the run, and explicit caller permission.

## 10. Receipt Safety

- initialization_receipt_schema = sentigraph_governed_nonproduction_target_initialization_receipt_v0_1
- canonical_UTF8_JSON = yes
- sorted_keys = yes
- compact_separators = yes
- exclusive_creation = yes
- overwrite_allowed = no
- flush_and_fsync = yes
- strict_readback_parse = yes
- exact_object_equality_verified = yes
- self_hash_excludes_only_self_hash_field = yes
- byte_SHA256_verified = yes
- committed_protected_value_scanner_used = yes
- receipt_contains_physical_path = no
- receipt_contains_username_or_drive = no
- receipt_contains_SQL_or_exception_text = no
- receipt_contains_protected_or_raw_value = no

## 11. TDD and Validation

- TDD_RED = collection_error_ModuleNotFoundError_app.services.governed_nonproduction_target_initialization_smoke
- focused_runner_tests = 53_passed
- persistence_regressions = 68_passed
- scanner_regressions = 57_passed
- safe_receipt_auditor_regressions = 155_passed
- combined_nearby_suite = 333_passed
- failure_injection_cases_passed = 29
- py_compile = pass
- AST_static_scan = pass
- git_diff_check = pass
- no_index_whitespace_check = pass

The failure matrix covers input/governance/DDL/path/collision/parent/connection/
transaction/both-DDL/schema/row/integrity/known-commit/ambiguous-commit/
same-session-post-commit/close/post-connection/receipt-build/scan/write/fsync/
readback/hash/cleanup and last-resort internal failure paths.

## 12. Frozen File Hashes

- runner_module_sha256 = 6e585f66072ec0bb2833951e83ee6e256774134929fc324759eb42ca1302dfc4
- runner_test_sha256 = 537d72cddd2191cd545382f4a5221ad7694d759d415b8666a09190c5ca575b0a
- historical_F06_report_sha256 = 4f455eaeef1253f795da3b13b3cb960e5c55349e1858d866178047179b65c214
- R1_report_sha256_before_commit = a1bd2ac84deb0af7008b5ea4d91a0ce67137b32fda03118159e8eaa8f6ff4a3e
- R1_report_sha256_scope = UTF8_report_bytes_with_only_the_R1_report_sha256_before_commit_value_replaced_by_64_zeroes
- frozen_read_only_acceptance = pass
- post_acceptance_hash_equality = pass

The R1 report field uses a deterministic self-field-excluded scope because a
file cannot contain its own full byte hash. The separate frozen acceptance
records and compares the full report byte SHA-256 out of band.

## 13. Synthetic-only and No-overreach Proof

- synthetic_temporary_repository_only = yes
- synthetic_temporary_SQLite_only = yes
- actual_Git_root_passed_to_runner = no
- formal_logical_target_accessed = no
- actual_runtime_enumerated = no
- formal_initialization_receipt_accessed = no
- protected_payload_read = no
- protected_capture_receipt_read = no
- source_or_package_read = no
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no
- route_or_API_changed = no
- frontend_changed = no
- provider_or_collector_called = no
- network_called = no
- subprocess_called = no
- Project_Source_changed = no

## 14. Effective Boundary

- MVP_F06_effective_acceptance_complete = no
- formal_F06_recheck_authorized = no
- MVP_F07_eligible = no
- MVP_F07_authorized = no
- MVP_F07_executed = no
- MVP_F08_authorized = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no

## 15. Next Boundary

- next_recommended_boundary = separate_change_control_decision_for_one_exact_formal_target_F06_compatibility_recheck
- next_boundary_authorized_now = no
- next_default = pause_for_ChatGPT_independent_acceptance

No approval phrase for the next boundary is generated here.
