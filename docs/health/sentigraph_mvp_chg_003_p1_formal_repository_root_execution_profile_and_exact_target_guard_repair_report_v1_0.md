# Sentigraph MVP-CHG-003-P1 Formal Repository-root Execution Profile and Exact Target Guard Repair Report v1.0

## 1. Change Identity

- change_id = MVP-CHG-003
- prompt_package_id = MVP-CHG-003-P1
- affected_milestone = MVP-F06
- classification = risk_buffer_consumption
- report_schema = sentigraph_mvp_chg_003_p1_formal_repository_root_execution_profile_and_exact_target_guard_repair_report_v1_0
- report_version = 1.0
- actual_model_deployment_identifier = hidden_by_current_Codex_session

## 2. Decision

- decision = ready
- privacy_issue_stop = no
- MVP_CHG_003_P1_status = candidate_completed_pending_chatgpt_acceptance
- formal_runner_ready_for_separate_exact_target_recheck = yes

This decision covers only the explicit execution-profile separation and the
temporary-fixture verification of the formal repository identity guard. It is
not a formal target recheck and does not complete MVP-F06.

## 3. Goal and Prompt Accounting

- Goal_created = yes
- Goal_activated = yes
- active_Goal_state_observed = yes
- MVP_CHG_003_P1_prompt_consumed = yes
- consumed_engineering_prompts_since_baseline = 13
- consumed_fixed_prompts = 6
- consumed_conditional_prompts = 4
- consumed_risk_prompts = 3
- remaining_fixed_prompts = 14
- remaining_conditional_allowance = 6
- remaining_risk_buffer = 1
- MVP_C03_prompt_allowance_consumed = 2
- MVP_C03_prompt_allowance_remaining = 0

## 4. Starting State

- starting_HEAD = 32c55b2874e5de25f8098352b0c9f9110b240257
- starting_origin_main = 32c55b2874e5de25f8098352b0c9f9110b240257
- starting_HEAD_message = Complete MVP-C03-P1-R1 F06 runner synthetic repair
- starting_ahead_behind = 0/0
- starting_worktree_clean = yes
- starting_staged_file_count = 0
- starting_untracked_file_count = 0
- repository_identity = dgmpurf/Sentigraph
- originating_formal_root_reachability_defect_confirmed = yes
- defect_safe_error_code = unsafe_repository_root

The genuine TDD RED used an exact synthetic Git-root fixture under pytest
temporary storage. The pre-repair runner reached its unconditional `.git`
rejection and returned the bounded error above. No formal repository or target
was used to confirm the defect.

## 5. Execution-profile Contract

- synthetic_profile = synthetic_temporary_repository
- formal_profile = formal_exact_sentigraph_repository
- synthetic_profile_preserved = yes
- synthetic_profile_remains_default = yes
- formal_profile_implemented = yes
- formal_profile_disabled_by_default = yes
- explicit_general_enable_required = yes
- explicit_formal_enable_required = yes
- generic_Git_repository_allowed = no
- caller_supplied_target_path_allowed = no
- caller_supplied_receipt_path_allowed = no
- caller_supplied_remote_allowed = no
- environment_profile_or_target_override_allowed = no
- implicit_profile_upgrade_allowed = no
- target_substitution_allowed = no
- fallback_allowed = no

## 6. Frozen Safe Projections

- repository_identity_schema = sentigraph_formal_repository_identity_v0_1
- repository_identity_version = 0.1
- repository_identity_safe_hash = 66ae70377a33d036ab68729e7b9a6f509c7218cbbc6d40739e1ca5a755a2d82b
- formal_execution_profile_contract_schema = sentigraph_formal_execution_profile_contract_v0_1
- formal_execution_profile_contract_version = 0.1
- formal_execution_profile_contract_safe_hash = 5225ff83fd2de19cb32e26b831da410f51a162c32afc40be97d522f87d2137bf
- canonical_encoding = UTF-8
- canonical_JSON_ensure_ascii = true
- canonical_JSON_sorted_keys = true
- canonical_JSON_compact_separators = true
- immutable_projection_objects = yes
- projection_hashes_recomputed_independently = yes

The identity projection contains only bounded repository identity, transport,
marker-kind, locked logical-label, and false capability fields. It contains no
physical path, drive, username, raw Git configuration, credential, or token.

## 7. Formal Repository Identity Verification

- exact_origin_identity_verified_in_temporary_fixture = yes
- expected_transport = github_https
- expected_repository_identity = dgmpurf/Sentigraph
- exact_origin_case_required = yes
- single_exact_origin_section_required = yes
- single_exact_origin_URL_value_required = yes
- wrong_owner_or_repository_rejected = yes
- case_variant_rejected = yes
- SSH_local_file_UNC_or_credentialed_origin_rejected = yes
- query_or_fragment_rejected = yes
- duplicate_origin_or_URL_rejected = yes
- Git_marker_must_be_ordinary_directory = yes
- Git_config_must_be_ordinary_nonreparse_file = yes
- Git_marker_or_config_symlink_reparse_rejected = yes
- unexpected_device_boundary_rejected = yes
- strict_noninterpolating_parser_used = yes
- bounded_Git_config_size = yes
- raw_origin_value_exposed = no
- raw_Git_config_exposed = no
- git_subprocess_used_by_runner = no
- formal_identity_verified_before_target_derivation = yes
- formal_identity_verified_before_SQLite = yes

Only temporary `.git/config` fixture bytes were read. The raw origin value was
not copied into the result, receipt, or this report.

## 8. Locked Target and SQLite Safety

- locked_target_logical_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- locked_receipt_logical_label = runtime/governed_nonproduction_evidence_persistence/target-initialization-receipt-6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b.json
- target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b
- target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2
- exact_target_and_receipt_derived_internally = yes
- single_SQLite_session_preserved = yes
- SQLite_connection_session_limit = 1
- SQLite_connection_reopen_count = 0
- automatic_retry = false
- second_attempt = false
- candidate_DML_count = 0
- reservation_DML_count = 0
- other_user_DML_count = 0
- absent_target_schema_only_initialization_verified = yes
- existing_exact_empty_target_read_only_verified = yes
- existing_target_bytes_unchanged = yes
- receipt_privacy_scan_passed = yes
- receipt_exclusive_creation_and_single_readback_preserved = yes

Both successful formal-profile cases used temporary Git roots and temporary
SQLite targets only. The existing schema, transaction, commit ambiguity,
cleanup, receipt, and zero-row logic was preserved.

## 9. TDD and Validation

- TDD_RED = 1_failed_53_passed_exact_temporary_Git_fixture_returned_unsafe_repository_root
- TDD_RED_genuine_unconditional_Git_guard_failure = yes
- focused_runner_tests = 95_passed
- preexisting_synthetic_runner_tests = 53_passed
- formal_profile_new_tests = 42
- persistence_regressions = 68_passed
- scanner_regressions = 57_passed
- safe_receipt_auditor_regressions = 155_passed
- combined_nearby_suite = 375_passed
- py_compile = pass
- AST_static_scan = pass
- canonical_projection_hash_check = pass
- git_diff_check = pass
- no_index_whitespace_check = pass
- placeholder_and_mojibake_scan = pass
- privacy_and_value_exposure_scan = pass

The formal matrix covers profile selection, disabled and mismatched bindings,
ordinary marker/config requirements, strict origin identity, ambiguous config,
single-session absent and existing target behavior, ordering, bounded failure
diagnostics, and temporary-root-only access. All preexisting synthetic cases
remain green.

## 10. Frozen File Hashes

- runner_module_sha256 = 48c5b0f2edd09754732e7f144ae5d50c18e4e60b353ee6e18565d41175d7ed61
- runner_test_sha256 = 62f05268edf007fa0d9640cf6e672375080499da735c41528c552630624bf6fc
- CHG_003_P1_report_sha256_before_commit = f52f8a866b8f73a39cb8d2f9a353b7fe845ccc9b9494d1c3adebdda7ffabfbe1
- CHG_003_P1_report_sha256_scope = UTF8_report_bytes_with_only_the_CHG_003_P1_report_sha256_before_commit_value_replaced_by_64_zeroes
- frozen_read_only_acceptance = pass
- post_acceptance_hash_equality = pass

The report hash uses a deterministic self-field-excluded scope. The separate
frozen acceptance compares the full report byte hash out of band without
editing any frozen file.

## 11. Protected Historical Evidence

- historical_F06_report_sha256 = 4f455eaeef1253f795da3b13b3cb960e5c55349e1858d866178047179b65c214
- historical_F06_report_byte_identical = yes
- R1_report_full_sha256 = 9bb758aeabb004bd3bdca3a2f5b86887c13602b33e66eb36424f8fb3288b1b84
- R1_report_byte_identical = yes
- historical_first_MVP_F06_status = needs_fix
- historical_first_MVP_F06_completed = no
- historical_first_MVP_F06_reclassified = no
- historical_first_MVP_F06_target_initialized = no
- MVP_C03_P1_R1_synthetic_scope_accepted = yes
- MVP_C03_P1_R1_formal_scope_accepted = no

## 12. Isolation and No-overreach Proof

- actual_Sentigraph_root_passed_to_runner = no
- actual_git_config_read = no
- formal_logical_target_accessed = no
- actual_runtime_enumerated = no
- formal_initialization_receipt_accessed = no
- protected_payload_read = no
- protected_capture_receipt_read = no
- source_or_package_read = no
- source_row_or_approved_row_read = no
- evidence_items_file_read = no
- candidate_reconstructed = no
- candidate_mutation_performed = no
- attempt_reservation_mutation_performed = no
- gate_prepared = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no
- route_or_API_changed = no
- frontend_changed = no
- provider_or_collector_called = no
- network_called = no
- subprocess_called = no
- Quant_repository_accessed = no
- incident_commit_implementation_consulted = no
- Project_Source_changed = no
- GitHub_Actions_changed = no
- runtime_artifact_staged = no

## 13. Effective Boundary

- MVP_CHG_003_P2_authorized = no
- MVP_CHG_003_P2_executed = no
- MVP_F06_effective_acceptance_complete = no
- MVP_F07_eligible = no
- MVP_F07_authorized = no
- MVP_F07_executed = no
- gate_activated = no
- persistence_executed = no
- production_object_created = no

## 14. Next Boundary

- next_recommended_boundary = MVP-CHG-003-P2 Independent Formal-profile Acceptance and One Exact-target F06 Recheck
- next_boundary_authorized_now = no
- next_default = pause_for_independent_ChatGPT_acceptance
- Project_Source_update = no
- tag = no

No approval phrase for the next boundary is generated here. The runner must not
be invoked against the actual Sentigraph repository root without a new,
separate authorization.
