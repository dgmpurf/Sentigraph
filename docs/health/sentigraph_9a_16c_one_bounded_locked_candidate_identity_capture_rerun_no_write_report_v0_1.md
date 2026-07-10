# Sentigraph 9A-16C One Bounded Locked-candidate Identity-capture Rerun No-write Report v0.1

## Current Execution Routing Actually Used

- actual_interface_used = Codex
- actual_environment_used = Local
- actual_model_used = current OpenAI Codex GPT-5 session model; exact deployment identifier not exposed
- actual_reasoning_effort_used = high
- actual_task_mode_used = Goal
- actual_speed_used = Standard
- goal_mode_activated = yes
- active_goal_exposed_by_goal_runtime = yes

## Decision

- phase = 9A-16C
- decision = ready
- privacy_issue_stop = no
- backend_only = yes
- test_first = yes
- local_only = yes
- identity_capture_rerun_only = yes
- one_approved_package_only = yes
- one_additional_bounded_row_execution_only = yes
- candidate_specific_pre_write_review_only = yes
- no_write = yes

The exact 9A-16C approval phrase authorized one additional bounded identity-capture execution. It did not authorize final write authorization, Evidence Layer write, production EvidenceItem creation, production runtime, or delivery.

Exact task-level approval phrase validated before the gated execution:

`APPROVE_9A_16C_ONE_BOUNDED_LOCKED_CANDIDATE_IDENTITY_CAPTURE_RERUN_AND_CONDITIONAL_9A_17_COMPLETION_NO_WRITE`

## Pre-rerun Safety Gate

- marker_helper_tdd_red = pass, helper absent
- marker_helper_tdd_green = 6 passed
- pre_rerun_non_real_tests = 26 passed
- pre_rerun_py_compile = pass
- marker_field_allowlist = pass
- marker_no_file_io_static_check = pass
- marker_no_directory_enumeration_check = pass
- positive_real_test_nodes = 1
- real_gate_default_state = disabled

The real path was not entered until the marker helper, format validation, no-IO test, and all non-real tests passed.

## Approved Package and Additional One-row Accounting

- approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016
- approved_package_role = candidate_demo_sample
- approved_case_id_hint = donglu_sunjihai_youth_football_202606
- approved_row_source = evidence_items.jsonl
- additional_approved_file_open_count = 1
- additional_logical_rows_inspected = 1
- additional_logical_rows_parsed = 1
- additional_preview_rows_created = 1
- additional_real_execution_count = 1
- second_identity_capture_execution = no
- real_integration_test_executed = yes
- real_integration_test_skipped = no
- evidence_items_csv_opened = no
- source_manifest_rows_parsed = 0
- collection_log_rows_parsed = 0
- alternate_package_used = no
- alternate_row_used = no
- directory_enumeration_performed = no
- arbitrary_path_accessed = no
- private_collector_inspected = no

Exact positive test node:

`backend/app/tests/test_9a_16b_one_approved_row_identity_complete_locked_candidate_review_no_write.py::test_9a_16c_real_locked_candidate_identity_capture_once`

Exact command shape used:

`SENTIGRAPH_RUN_9A16C_REAL_IDENTITY_CAPTURE=1 python -m pytest backend/app/tests/test_9a_16b_one_approved_row_identity_complete_locked_candidate_review_no_write.py::test_9a_16c_real_locked_candidate_identity_capture_once -q -s`

The environment assignment used the PowerShell equivalent for the current process. The test node was not rerun.

## Captured Locked-candidate Identity

- identity_schema = sentigraph_one_real_source_locked_candidate_identity_v0_1
- identity_version = 0.1
- selected_preview_row_opaque_id = preview-row-001
- selected_preview_row_safe_hash = ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391
- final_candidate_id = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- final_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- final_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- hash_algorithm = sha256
- hash_input_scope = versioned_safe_canonical_projection_only
- candidate_lock_status = locked_for_single_candidate_governance_review_only
- new_9a16c_locked_candidate_created = yes
- old_9a16_ephemeral_candidate_recovered = no
- old_9a16b_in_process_candidate_recovered = no

Captured machine-readable marker:

`SENTIGRAPH_9A16C_LOCKED_IDENTITY={"final_candidate_id":"evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410","final_candidate_safe_hash":"2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5","selected_preview_row_opaque_id":"preview-row-001","selected_preview_row_safe_hash":"ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391"}`

Both IDs passed opaque/non-path/non-URL validation. Both hashes are 64 lowercase hexadecimal characters and matched the successful review result.

## Safe Hash Scope

The two SHA-256 values use only a versioned canonical safe projection containing locked package labels, source basename, safe opaque IDs, schemas, coarse safe metadata, lineage stage labels, identity schema, and identity version.

- safe_hash_is_not_raw_content_hash = yes
- safe_hash_is_not_path_hash = yes
- safe_hash_is_not_identity_hash = yes
- safe_hash_reproducible_from_safe_projection = yes

The projection excludes preview text, title/body/comment text, raw row JSON, raw author identity, usernames, profile URLs, private messages, source URLs, package paths, export roots, absolute paths, credentials, cookies, sessions, tokens, personal contact data, and full candidate payloads.

## Candidate Chain and Review

- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- candidate_specific_blockers_clear = yes
- candidate_specific_risks_classified = yes
- candidate_specific_lineage_verified = yes
- candidate_specific_privacy_review_complete = yes
- candidate_specific_rollback_plan_verified = yes

Verified chain:

`controlled row preview -> controlled evidence candidate -> controlled review queue candidate -> controlled Evidence Layer import candidate -> controlled direct write candidate -> controlled production evidence import candidate -> production-import-derived write candidate -> locked-candidate identity projection -> locked-candidate pre-write review`

Provider output mistaken as truth remains an open risk. Duplicate amplification and weak/rejected evidence inclusion remain unknown. These conservative labels do not block this no-write identity capture, but they remain relevant to any later governance decision.

## Privacy and Output Minimization

- preview_text_persisted = no
- preview_text_logged = no
- preview_text_written_to_report = no
- raw_author_identity_exposed = no
- profile_url_exposed = no
- real_human_pii_exposed = no
- secrets_exposed = no
- absolute_path_exposed = no

The marker contains exactly four safe identity fields and one fixed prefix. It contains no row text, raw identity, path, URL, PII, secret, or candidate payload.

## Human Declaration Context

- declared_authority_role_label = self_declared_project_owner_role
- authority_basis_label = authority_basis_not_independently_validated
- manual_review_responsibility_statement_present = yes
- warning_count_acknowledgment_present = yes
- human_review_required_acknowledgment_present = yes
- no_automatic_trust_upgrade_acknowledgment_present = yes
- human_authority_validated = no
- manual_review_responsibility_accepted_as_runtime_or_audit_state = no
- final_write_authorization_performed = no

## No-write and No-production Proof

- actual_write_authorized = no
- actual_evidence_layer_write_performed = no
- persisted_evidence_layer_record_created = no
- production_evidenceitem_creation_authorized = no
- production_evidenceitem_created = no
- review_queue_runtime_used = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_created = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- public_delivery_created = no
- provider_called = no
- collector_called = no
- real_api_called = no
- real_llm_called = no
- ready_for_actual_write = no
- overall_write_disposition = pause

## Conditional 9A-17 Result

- conditional_9a17_documents_created = yes
- exact_candidate_binding_complete = yes
- candidate_role_policy_clear = no
- approval_guard_consistency_status = stable_current_exact_guards
- final_write_authorization_readiness_status = conditionally_ready_pending_candidate_role_policy_resolution
- selected_next_boundary_option = pause_pending_candidate_role_policy_or_approval_guard_consistency_resolution
- actual_write_next = no
- production_evidenceitem_creation_next = no

The guard branch is stable; the selected next boundary remains phrased as the shared role/guard boundary because repository policy does not yet define whether `candidate_demo_sample` may enter a later final-authorization review.

## Validation

- gated_real_positive_node = 1 passed
- captured_marker_present_and_complete = pass
- post_capture_non_real_9a16b_tests = 26 passed
- controlled_row_preview_regressions = 79 passed
- controlled_candidate_chain_regressions = 478 passed
- 8Y-13C_and_9A-15_regressions = 107 passed
- 9A-14_and_golden_contract_regressions = 20 passed
- py_compile_new_service_and_test = pass
- git_diff_check = pass
- untracked_no_index_whitespace_check = pass
- trailing_whitespace_scan = pass
- placeholder_and_mojibake_scan = pass
- approval_phrase_context_scan = pass
- identity_binding_format_and_uniqueness_scan = pass
- safe_hash_canonical_projection_scan = pass
- one_package_one_file_one_row_accounting_audit = pass
- privacy_PII_secret_path_scan = pass
- no_write_no_production_static_scan = pass
- 9A-17_candidate_binding_and_scope_scan = pass
- approval_guard_consistency_scan = stable_current_exact_guards
- git_allowlist_audit = pass
- full_pytest = not run, outside approved scope
- frontend_build = not run, no frontend change
- browser_or_route_smoke = not run, no route or UI change

## Source and Release Recommendation

- source_update_recommended = yes after commit as part of the deferred unified ChatGPT-side Source batch
- source11_update_recommended = no
- recommended_tag = no
- next_default = pause
