# Sentigraph MVP-CHG-002 F04 Durable Receipt Auditor and Exact-path Acceptance Recheck Report v1.0

## 1. Title and Change Identity

- change_id = MVP-CHG-002
- affected_milestone = MVP-F04
- classification = risk_buffer_consumption
- baseline_version = 1.0
- scope = durable_pure_receipt_auditor_and_one_exact_path_read_only_recheck

## 2. Decision

- decision = ready
- final_outcome = F04_baseline_requirement_satisfied_via_MVP_CHG_002_recheck
- change_control_status = completed
- effective_F04_acceptance = completed_via_change_control_recheck

The historical first F04 attempt remains `needs_fix`. This change-control recheck
provides the effective acceptance result without rewriting that history.

## 3. Privacy Status

- privacy_issue_stop = no
- protected_value_exposed = no
- raw_key_echoed = no
- raw_value_echoed = no
- artifact_content_printed = no
- exact_identity_values_exposed = no

Only bounded categories, counts, byte lengths, and safe hashes are recorded.

## 4. Exact Approval Validation

- exact_user_approval_phrase_received = yes
- exact_user_approval_phrase_validated = yes
- approval_scope = MVP_CHG_002_only
- source_access_authorized = no
- artifact_repair_authorized = no
- recapture_authorized = no
- persistence_authorized = no
- production_authorized = no

Validated phrase:

`APPROVE_SENTIGRAPH_MVP_CHG_002_F04_DURABLE_RECEIPT_AUDITOR_AND_ONE_EXACT_PATH_READ_ONLY_ACCEPTANCE_RECHECK_RISK_BUFFER_NO_SOURCE_REREAD_NO_ARTIFACT_MUTATION`

## 5. Execution Routing and Model Exposure

- interface = Codex
- environment = Local
- requested_model_label = GPT-5.6 Sol
- requested_reasoning_effort = extra_high
- actual_deployment_identifier_exposed = no
- unavailable_deployment_identifier_claimed = no

The current session did not expose a verifiable deployment identifier.

## 6. Goal Activation and Completion

- Goal_requested = yes
- Goal_created = yes
- Goal_active_state_observed = yes
- Goal_objective_matched_MVP_CHG_002 = yes
- Goal_terminal_ready_condition_reached = yes
- Goal_completion_recorded_after_final_Git_resolution = yes

## 7. Baseline Change-control and Prompt Accounting

- baseline_document_commit = cb81379ccc48ba5177c1b23adab2ea90fbad6408
- latest_committed_checkpoint_before_change = ba812561b20a86296d363e462930fc146865b56b
- baseline_version_changes = no
- fixed_milestone_count_changes = no
- fixed_prompt_budget_changes = no
- conditional_prompt_allowance_changes = no
- risk_buffer_total_changes = no
- MVP_CHG_002_prompt_consumed = yes
- consumed_engineering_prompts_since_baseline = 8
- consumed_fixed_prompts = 4
- consumed_conditional_prompts = 2
- consumed_risk_prompts = 2
- remaining_fixed_prompts = 16
- remaining_conditional_allowance = 8
- remaining_risk_buffer = 2
- risk_buffer_prompt_allowance = 4

## 8. Git Preflight

- expected_branch = main
- observed_branch = main
- expected_HEAD = ba812561b20a86296d363e462930fc146865b56b
- observed_HEAD = ba812561b20a86296d363e462930fc146865b56b
- expected_HEAD_message = Complete MVP-C02 repaired scanner acceptance and bounded recapture
- observed_HEAD_message_match = yes
- origin_main_aligned = yes
- tracked_modified_files_before_change = 0
- staged_files_before_change = 0
- expected_untracked_first_F04_report_only = yes
- unrelated_work_found = no
- CHG_002_file_collision_found = no

## 9. First F04 Report Preservation

- historical_first_F04_status = needs_fix
- historical_first_MVP_F04_completed = no
- historical_first_F04_atomic_acceptance_completed = no
- historical_first_F04_receipt_structure_audit_completed = no
- historical_first_F04_report_preserved = yes
- historical_first_F04_report_byte_hash_unchanged = yes
- historical_first_F04_report_sha256 = 0ac252c7b9715a9150ee3616bebd0c03049051584a9115f89fdd91d8f02b8410
- historical_first_F04_reclassified = no

The first report remains byte-for-byte unchanged and is included as historical
evidence, not rewritten as a successful run.

## 10. Original Audit-procedure Finding

- originating_finding_confirmed = yes
- first_auditor_combined_required_and_float_guard = yes
- first_auditor_discarded_safe_in_memory_diagnostics = yes
- first_auditor_receipt_reopened = no
- first_auditor_result_reclassified = no

The first procedure could not distinguish a missing required field from a
floating value and stopped before completing unrelated safe checks. The defect
was in the ephemeral audit procedure, not proven to be in the receipt.

## 11. Durable Receipt Auditor Design

- durable_receipt_auditor_implemented = yes
- durable_receipt_auditor_independently_accepted = yes
- audit_schema = sentigraph_safe_payload_receipt_acceptance_audit_v0_1
- audit_version = 0.1
- pure = yes
- deterministic = yes
- in_memory_only = yes
- file_IO = no
- environment_access = no
- network_access = no
- database_access = no
- subprocess_access = no
- logging = no
- timestamps_generated = no
- mutable_global_state = no
- physical_path_input = no
- combined_ambiguous_guard_removed = yes
- complete_in_memory_diagnostics_implemented = yes
- finding_output_value_free = yes

The public function accepts only an already parsed receipt and bounded expected
values. It has no path parameter and no side-effect surface.

## 12. Required, Extension, and Forbidden Field Policy

- receipt_required_fields_defined_from_F02_table = yes
- receipt_classification_treated_as_contracted_optional_extension = yes
- required_field_can_be_satisfied_by_extension = no
- bounded_nonauthoritative_extensions_allowed = yes
- disallowed_authority_bearing_extensions_fail_closed = yes
- exact_forbidden_fields_fail_closed = yes
- extension_names_returned_in_findings = no
- extension_values_returned_in_findings = no

The auditor requires every field in the committed F02 required-fields table.
Additional bounded metadata is non-authoritative and cannot replace or override
a core field.

## 13. Type and Float Semantics

- exact_string_type_enforced = yes
- exact_integer_type_enforced = yes
- boolean_as_integer_rejected = yes
- exact_boolean_type_enforced = yes
- nullable_pause_reason_type_enforced = yes
- recursive_float_scan = yes
- finite_float_rejected = yes
- NaN_rejected = yes
- positive_infinity_rejected = yes
- negative_infinity_rejected = yes
- nested_float_count_complete = yes
- type_and_float_categories_separate = yes

## 14. Negative-proof Semantics

- required_root_negative_proof_count = 10
- exact_false_only = yes
- false_like_integer_rejected = yes
- false_like_string_rejected = yes
- null_rejected = yes
- container_value_rejected = yes
- nested_only_negative_proof_rejected = yes
- contracted_C02_P2_negative_extensions_checked_when_present = yes
- negative_proof_findings_value_free = yes

## 15. Arithmetic and Cross-binding Semantics

- source_open_read_reopen_counts_checked = yes
- source_line_limit_probe_and_byte_count_checked = yes
- UTF8_and_JSON_state_checked = yes
- row_and_artifact_counts_checked = yes
- package_row_selector_hash_candidate_bindings_checked = yes
- final_outcome_checked = yes
- milestone_context_checked = yes
- payload_schema_version_hash_binding_checked = yes
- scanner_claims_checked = yes
- safe_diagnostics_accumulate_after_nonprivacy_finding = yes

## 16. TDD RED

- TDD_RED = collection_error_ModuleNotFoundError_new_auditor_module_absent
- TDD_RED_exit_code = 1
- TDD_RED_genuine = yes
- runtime_access_before_RED = no

The focused test was created first and failed during collection because the new
auditor module did not yet exist.

## 17. Focused GREEN

- auditor_focused_tests = 155 passed in 0.22s
- auditor_focused_test_exit_code = 0
- complete_synthetic_success_case = pass
- former_combined_guard_case = pass
- deterministic_output_case = pass
- input_mutation_case = pass
- bounded_finding_enum_case = pass

## 18. Nearby Safe Regressions

- scanner_focused_tests = 57 passed in 0.10s
- pure_validator_regressions = 27 passed in 0.21s
- combined_safe_tests = 239 passed in 0.42s
- combined_safe_test_exit_code = 0
- full_pytest_run = no
- SQLite_tests_run = no
- source_reader_tests_run = no

## 19. Auditor Purity and Value-free Findings

- py_compile = pass
- purity_scan = pass
- banned_import_count = 0
- banned_call_count = 0
- dynamic_finding_interpolation_count = 0
- unsafe_output_interpolation_count = 0
- raw_field_name_in_finding = no
- raw_receipt_value_in_finding = no
- input_mutated = no
- diagnostic_accumulation_tests = pass
- phone_like_safe_hash_scanner_case = pass
- genuine_phone_like_value_scanner_case = pass

## 20. Frozen Module Hashes

- auditor_module_sha256 = a0abf3ea1d244bc170ccd5172d278304b61632edeb030b6410c36f993bbc6d97
- auditor_test_sha256 = acda72380e93050df2beb53f4234e091ab9281cec64d71ba3b9724c6dbe56d62
- protected_value_scanner_sha256 = 5c28a7aaef0af30619638c28901d24cdf257e8a936fd621325d47fa74616a487
- modules_frozen_before_artifact_access = yes
- frozen_imports_resolved = yes
- post_freeze_edit_performed = no

## 21. Exact Artifact-path Derivation

- authoritative_final_hash_uniquely_derived = yes
- exact_artifact_path_count = 2
- artifact_directory_enumerated = no
- wildcard_used = no
- latest_file_selection_used = no
- caller_supplied_artifact_path_used = no
- path_escape_detected = no
- source_component_in_artifact_path = no
- payload_exact_path_present = yes
- receipt_exact_path_present = yes
- payload_artifact_git_ignored = yes
- receipt_artifact_git_ignored = yes
- runtime_artifact_tracked = no
- runtime_artifact_staged = no
- physical_artifact_path_exposed = no

The exact relative names were derived from the committed immutable identity.
Neither name nor identity value is reproduced here.

## 22. One-read Artifact Accounting

- payload_artifact_open_count = 1
- payload_artifact_read_call_count = 1
- payload_artifact_reopen_count = 0
- receipt_artifact_open_count = 1
- receipt_artifact_read_call_count = 1
- receipt_artifact_reopen_count = 0
- payload_artifact_open_mode = binary_read_only
- receipt_artifact_open_mode = binary_read_only
- payload_artifact_byte_count = 4347
- receipt_artifact_byte_count = 2387
- payload_artifact_byte_sha256 = 64316f33d1673e67c9fd8b5286d1fa60af96f55a9b79e937915430aacec286e3
- receipt_artifact_byte_sha256 = dc7fea053636b561eed00bd3863f455559630aa39ab533aa3ae1a9136edaf6d8
- artifact_byte_hashes_retained_from_first_reads = yes
- parsed_objects_retained_until_report_validation = yes
- artifact_handles_read_only = yes
- artifact_sizes_stable_on_open_handles = yes
- artifact_hashes_stable_in_memory = yes

## 23. Strict Parser Results

- payload_strict_JSON_passed = yes
- receipt_strict_JSON_passed = yes
- strict_UTF8_used = yes
- duplicate_key_rejection_enabled = yes
- nonstandard_numeric_constant_rejection_enabled = yes
- top_level_object_required = yes
- replacement_decoding_used = no
- alternate_encoding_used = no

## 24. Payload Independent Recheck

- payload_schema_verified = yes
- payload_top_level_field_count_verified = yes
- payload_field_path_contract_verified = yes
- payload_canonical_hash_match = yes
- immutable_identity_verified = yes
- candidate_lineage_verified = yes
- boundary_projection_verified = yes
- payload_validator_passed = yes
- payload_scanner_passed = yes
- C02_P2_payload_cross_binding = yes
- safe_payload_independently_accepted = yes

The payload was accepted from its first in-memory read without source access or
use of a stored hash claim as sole proof.

## 25. Receipt Durable-auditor Result

- receipt_required_fields_verified = yes
- receipt_extension_policy_verified = yes
- receipt_field_types_verified = yes
- receipt_no_floating_values_verified = yes
- receipt_arithmetic_verified = yes
- receipt_negative_proofs_verified = yes
- receipt_payload_cross_binding_verified = yes
- receipt_input_unchanged = yes
- receipt_auditor_passed = yes
- receipt_auditor_finding_count = 0
- receipt_auditor_finding_categories = []
- receipt_missing_required_field_count = 0
- receipt_disallowed_extension_field_count = 0
- receipt_invalid_field_type_count = 0
- receipt_floating_value_count = 0
- receipt_arithmetic_mismatch_count = 0
- receipt_negative_proof_violation_count = 0
- receipt_scanner_contract_mismatch_count = 0
- receipt_payload_cross_binding_mismatch_count = 0
- receipt_remediation_context_mismatch_count = 0

## 26. Receipt Protected-value Scanner Result

- receipt_scanner_profile = safe_capture_receipt_v1_0
- receipt_scanner_passed = yes
- receipt_scanner_finding_count = 0
- receipt_scanner_protected_value_exposed = no
- receipt_scanner_raw_key_echoed = no
- receipt_scanner_raw_value_echoed = no
- auditor_and_scanner_outcomes_agree = yes

## 27. Complete Safe Diagnostic Categories

- missing_required_field = 0
- disallowed_extension_field = 0
- invalid_field_type = 0
- floating_value_present = 0
- receipt_arithmetic_mismatch = 0
- negative_proof_state_violation = 0
- scanner_contract_mismatch = 0
- payload_cross_binding_mismatch = 0
- remediation_context_mismatch = 0
- complete_safe_diagnostics_resolved_from_same_object = yes
- second_receipt_read_needed = no

## 28. Artifact Cross-binding

- payload_filename_binding_verified = yes
- receipt_filename_binding_verified = yes
- payload_receipt_cross_binding_verified = yes
- payload_schema_cross_binding_verified = yes
- payload_version_cross_binding_verified = yes
- payload_safe_hash_cross_binding_verified = yes
- artifact_count_cross_binding_verified = yes
- C02_P2_report_used_as_comparison_only = yes
- third_artifact_inferred_or_searched = no
- file_time_used_as_truth = no

## 29. Historical-record Preservation

- historical_F03_preserved = yes
- historical_F03_status = privacy_issue_stop
- historical_F03_completed = no
- historical_F03_reclassified = no
- C02_P1_preserved = yes
- C02_P1_status = needs_fix_prior_semantics_unavailable
- C02_P1_actual_historical_false_positive_proven = no
- C02_P2_preserved = yes
- C02_P2_status = completed
- first_F04_preserved = yes
- first_F04_reclassified = no

## 30. No-production Proof

- source_accessed = no
- source_reopened = no
- package_or_row_reread = no
- runtime_directory_enumerated = no
- artifact_mutation_performed = no
- artifact_writer_called = no
- SQLite_accessed = no
- logical_persistence_target_accessed = no
- gate_activated = no
- persistence_executed = no
- production_evidenceitem_created = no
- production_case_created = no
- production_analysis_run_created = no
- production_analysis_result_created = no
- source11_runtime_called = no
- public_or_delivery_runtime_called = no
- provider_or_collector_called = no
- network_called = no

## 31. Effective F04 Outcome

- MVP_F04_baseline_requirement_satisfied_via_MVP_CHG_002_recheck = yes
- historical_first_MVP_F04_completed = no
- historical_first_MVP_F04_status = needs_fix
- historical_first_MVP_F04_reclassified = no
- safe_payload_independently_accepted = yes
- safe_receipt_independently_accepted = yes
- effective_F04_status = completed_via_MVP_CHG_002_recheck
- MVP_F05_authorized = no
- MVP_F05_executed = no

## 32. Git Auto-commit and Push Result

- auto_commit_eligibility = yes_subject_to_final_repository_validation
- required_commit_message = Complete MVP-CHG-002 F04 acceptance recheck
- allowed_repository_file_count = 4
- runtime_artifact_stage_allowed = no
- tag_required = no
- force_push_allowed = no
- history_rewrite_allowed = no
- Git_execution_receipt_location = final_Codex_response

This report is materialized before the Git transaction by necessity. The actual
commit identifier, push result, committed inventory, and final worktree state
are recorded by Codex after the final repository gate.

## 33. Project Source Recommendation

- Project_Source_update_before_independent_ChatGPT_acceptance = no
- Canonical_00_replacement_after_acceptance = recommended
- Canonical_09_narrow_replacement_after_acceptance = recommended
- Canonical_03_update = no
- Canonical_05_update = no
- Source_11_update = no

Any later canonical update should preserve the historical first F04 failure,
record CHG-002 completion, and keep MVP-F05 unapproved.

## 34. Next Boundary

- next_recommended_fixed_milestone = MVP-F05 Target Authorization Contract
- MVP_F05_authorized = no
- MVP_F05_executed = no
- source_reopen_authorized = no
- recapture_authorized = no
- artifact_reread_authorized = no
- artifact_mutation_authorized = no
- gate_activation_authorized = no
- persistence_authorized = no
- production_creation_authorized = no

Stop after CHG-002 Git resolution. This report does not authorize MVP-F05 or
any source, target, gate, persistence, or production operation.
