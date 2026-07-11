# Sentigraph MVP-F02 Real Safe-payload Capture Readiness and Access Decision v1.0

## 1. Title and Decision Identity

- milestone_id = MVP-F02
- prompt_package_id = MVP-F02-P1
- decision_schema = sentigraph_mvp_f02_real_safe_payload_capture_readiness_and_access_decision_v1_0
- decision_version = 1.0
- baseline_version = 1.0
- baseline_task_classification = planned_fixed_milestone

## 2. Decision

- decision = ready
- decision_scope = docs_only_future_one_bounded_source_access_readiness
- capture_path_selected = yes
- capture_path_has_equal_alternatives = no
- F03_preparation_may_be_recommended = yes

`ready` means the F02 planning contract is complete and one exact future capture
path is defined. It does not mean the real source may be opened or that F03 is
authorized.

## 3. Privacy Status

- privacy_issue_stop = no
- real_package_accessed = no
- real_row_read = no
- real_source_line_length_measured = no
- real_payload_created = no
- real_payload_hash_calculated = no
- parser_implemented = no
- runtime_target_accessed = no
- SQLite_accessed = no
- gate_activated = no
- persistence_mutation_performed = no
- production_evidenceitem_created = no

Only Git-tracked code, tests, contracts, decisions, health reports, Baseline
documents, Git history, and `.gitignore` were inspected. No runtime, exchange,
package, row, configured store, or private collector location was accessed.

## 4. Exact Approval Validation

- exact_approval_received = yes
- exact_approval_valid = yes
- approval_scope_respected = yes
- correction_approval_received = yes
- correction_approval_valid = yes

The original F02 approval was:

`APPROVE_SENTIGRAPH_MVP_F02_REAL_SAFE_PAYLOAD_CAPTURE_READINESS_AND_ACCESS_CONTRACT_DOCS_ONLY`

The exact bounded-line and strict-parser correction approval was:

`APPROVE_SENTIGRAPH_MVP_F02_BOUNDED_SOURCE_LINE_AND_STRICT_JSON_PARSER_CONTRACT_CORRECTION_DOCS_ONLY`

They authorize only this docs-only decision and the companion architecture
contract. The correction approval is not parser implementation, real-data, F03,
runtime, gate, persistence, or production authorization.

## 5. Execution Routing and Actual-model Exposure

- execution_interface = Codex
- execution_environment = local
- execution_mode = Goal
- requested_model_recommendation = GPT-5.6 Sol
- requested_reasoning_effort = Extra High
- actual_model_exposure = current_Codex_session
- exact_deployment_identifier_exposed = no
- unavailable_model_identifier_claimed = no

The exact deployment identifier was hidden, so this decision does not claim that
the recommended deployment name was actually exposed or selected.

## 6. Goal Activation and Completion

- goal_created = yes
- goal_activated = yes
- active_goal_state_observed = yes
- goal_scope_matched_MVP_F02 = yes
- goal_completed = yes
- stop_condition_reached = no

The Goal covered one exact capture procedure, a 1 MiB raw-line cap, one bounded
binary read, strict UTF-8 and strict JSON rules, parser-safe receipt evidence,
schema/source mapping, privacy, custody, retention, F04 handoff, risk-buffer
accounting, exactly two docs, and no real source or runtime access.

## 7. Baseline and Prompt Accounting

- MVP_F02_prompt_consumed = yes
- MVP_F02_risk_correction_prompt_consumed = yes
- fixed_prompt_budget = 20
- conditional_prompt_allowance = 10
- risk_buffer_prompt_allowance = 4
- consumed_engineering_prompts_since_baseline = 3
- consumed_fixed_prompts = 2
- consumed_conditional_prompts = 0
- consumed_risk_prompts = 1
- remaining_fixed_prompts = 18
- remaining_conditional_allowance = 10
- remaining_risk_buffer = 3
- accounting_arithmetic_verified = yes

The fixed pool moved from 19 after F01 to 18 when the original F02 Goal started.
This correction consumes one Prompt from the four-Prompt risk buffer, leaving 3.
The risk-buffer total remains 4. No conditional allowance is consumed.

Change-control record:

- change_id = MVP-CHG-001
- affected_milestone = MVP-F02
- classification = risk_buffer_consumption
- originating_finding = independent_ChatGPT_review_found_unbounded_raw_line_bytes_and_missing_duplicate_key_and_nonstandard_numeric_constant_rejection
- scope_boundary = docs_only_correction_of_the_two_existing_MVP_F02_documents
- baseline_version_changes = no
- fixed_milestone_count_changes = no
- fixed_prompt_budget_changes = no
- conditional_prompt_allowance_changes = no
- risk_buffer_total_changes = no
- user_approval_required = yes
- user_approval_received = yes
- exact_user_approval_phrase_validated = yes
- old_remaining_risk_buffer = 4
- new_remaining_risk_buffer = 3
- risk_buffer_change_record_complete = yes

MVP-C01 remains separate:

- MVP_C01_trigger_eligible = yes
- MVP_C01_authorized = no
- MVP_C01_consumed = no
- MVP_C01_blocking_MVP_F02 = no

MVP-C02 remains separate and unused:

- MVP_C02_triggered = no
- MVP_C02_authorized = no
- MVP_C02_consumed = no

This pre-F03 correction is paid from the risk buffer, not MVP-C02.

## 8. Git Preflight

- preflight_result = pass
- branch = main
- expected_HEAD = 35dd3e1cd0e317d2b0514ef99d1ca30dd13ffe4d
- observed_HEAD = 35dd3e1cd0e317d2b0514ef99d1ca30dd13ffe4d
- origin_main_aligned = yes
- worktree_clean_before_F02 = yes
- materially_equivalent_F02_document_found = no
- target_files_preexisted = no
- Baseline_F02_prompt_count = 1
- correction_preflight_result = pass
- correction_expected_untracked_doc_count = 2
- correction_observed_untracked_doc_count = 2
- correction_tracked_modified_files = 0
- correction_staged_files = 0
- correction_additional_untracked_files = 0
- correction_HEAD_matched_expected = yes
- correction_origin_main_aligned = yes

The observed commit message was `Complete MVP-F01 post-repair conformance audit`.
At correction preflight, the same two F02 documents were the only untracked
files; no tracked or staged file differed.

## 9. Evidence Inspected

Authoritative tracked governance records:

- `docs/health/sentigraph_9a_16_one_real_exported_package_bounded_redacted_row_candidate_specific_evidence_layer_pre_write_review_no_write_report_v0_1.md`
- `docs/health/sentigraph_9a_16b_one_approved_row_identity_complete_locked_candidate_review_no_write_report_v0_1.md`
- `docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md`
- `docs/planning/sentigraph_9a_19_exact_locked_candidate_human_final_write_authorization_decision_v0_1.md`
- `docs/planning/sentigraph_9a_20_exact_locked_candidate_actual_evidence_layer_write_execution_gate_establishment_authorization_decision_v0_1.md`
- `docs/health/sentigraph_9a_21_exact_locked_candidate_actual_write_execution_surface_activation_readiness_audit_report_v0_1.md`
- `docs/architecture/sentigraph_governed_nonproduction_evidence_persistence_surface_prerequisite_contract_v0_1.md`
- `docs/planning/sentigraph_9a_22_governed_nonproduction_persistence_surface_prerequisite_design_and_implementation_readiness_decision_v0_1.md`
- `docs/health/sentigraph_9a_23b_synthetic_nonproduction_persistence_exact_conformance_repair_report_v0_1.md`
- `docs/health/sentigraph_mvp_f01_independent_9a23b_post_repair_conformance_audit_report_v1_0.md`
- the two Internal Alpha MVP Baseline v1.0 documents.

Tracked code/test evidence:

- controlled row-preview and one-real-candidate review services/tests;
- 9A-16C locked-identity helper and tests;
- production-import-derived candidate helper;
- governed nonproduction payload validator and focused tests;
- committed `.gitignore`.

## 10. Exact Capture-path Decision

- selected_capture_mechanism = one_ephemeral_inline_local_F03_procedure
- persistent_reader_implementation_required = no
- package_resolver_invoked = no
- caller_supplied_path_allowed = no
- approved_source_file_open_count = 1
- physical_source_lines_read_maximum = 1
- source_reopen_allowed = no
- source_file_open_mode = binary_read_only
- source_line_utf8_byte_limit = 1048576
- source_line_probe_read_size = 1048577
- source_read_call_count_maximum = 1
- source_second_read_allowed = no
- source_seek_allowed = no

The one selected path reads committed governance bindings first, imports tracked
constants and pure adapters, then opens only the committed approved row-file
object once in binary read-only mode. It makes exactly one
`handle.readline(1048577)` call for physical line 1, applies the byte cap before
strict UTF-8 and strict JSON parsing, builds one in-memory safe candidate chain,
verifies all committed preview/final identities, validates one payload, performs
recursive safety scans, and writes one payload plus one receipt to the protected
runtime output class.

The current public row-preview loop is not selected as the F03 file reader
because it may continue past an invalid first line. F03 instead applies the same
safe projection rules under a stricter one-line bound.

## 11. Identity-binding Decision

- identity_binding_complete = yes
- authoritative_identity_record_count = 1
- authoritative_identity_record_commit = 11ae4bb33e1d45afc6153e4dd28be0e4b5178e34
- authoritative_identity_record_path = docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md
- identity_values_reproduced_in_this_decision = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- candidate_substitution_allowed = no

The record contains the complete package/role/case/source, preview ID/hash,
final candidate ID/hash/schema, identity schema/version, hash rules, and lock
status required by the current validator. F03 must load these exact committed
values and independently reproduce the preview and final safe hashes from its
single selected row.

## 12. Single-access Decision

- single_access_semantics_complete = yes
- source_access_sessions_allowed = 1
- approved_package_count = 1
- approved_row_source_count = 1
- approved_candidate_count = 1
- approved_output_payload_count = 1
- source_file_open_count_maximum = 1
- source_file_reopen_count_maximum = 0
- physical_rows_read_maximum = 1
- parsed_row_objects_maximum = 1
- selected_rows_maximum = 1
- source_read_call_count_maximum = 1
- source_second_read_allowed = no
- source_line_terminator_counted_in_limit = yes
- alternate_source_allowed = no
- automatic_retry_allowed = no
- directory_enumeration_allowed = no
- recursive_scan_allowed = no
- glob_allowed = no

The source session starts at successful binary source-file open. One handle
makes one bounded read and then closes. Any failure after open consumes the
session. Oversize detection, decode failure, or parser failure permits no second
read. Output creation does not create another source session. No fallback or
later retry is inherited from a partial failure.

## 13. Row-selection Readiness

- row_selection_contract_complete = yes
- exact_row_source_bound = yes
- selector_kind = first_physical_JSONL_record_only
- selector_row_index = 1
- unbounded_scan_required = no
- broad_row_inspection_required = no
- exactly_one_selected_row_required = yes
- bounded_source_line_contract_complete = yes
- strict_UTF8_decode_contract_complete = yes
- strict_JSON_parser_contract_complete = yes
- source_line_utf8_byte_limit = 1048576
- source_line_probe_read_size = 1048577
- UTF8_decode_errors = pause
- UTF8_replacement_character_fallback_allowed = no
- encoding_fallback_allowed = no
- duplicate_JSON_keys_allowed = no
- nonstandard_numeric_constants_allowed = no
- top_level_JSON_object_required = yes

The selector is supported by committed 9A-16 evidence showing one inspected row
and by the 9A-16C identity for the row-index-1 preview projection. EOF, blank,
oversize input, invalid UTF-8, malformed JSON, a duplicate key at any depth,
`NaN`/`Infinity`/`-Infinity`, a non-object top level, blocked projection, any
identity/hash mismatch, zero candidate, or multiple candidate results stops
with no payload and no second line read.

The 1048576-byte cap includes an `LF` or `CRLF` terminator. It is a contract cap,
not a claim that the unknown real row fits. F02 did not measure the source line.

## 14. Payload Allowlist Readiness

- safe_payload_allowlist_complete = yes
- source_to_payload_mapping_complete = yes
- canonicalization_contract_complete = yes
- payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
- payload_version = 0.1
- payload_top_level_field_count = 10
- payload_field_paths_documented = 71
- unknown_fields_allowed = no
- missing_required_fields_allowed = no
- raw_source_text_retained = no
- capture_receipt_parser_evidence_complete = yes
- capture_receipt_raw_bytes_allowed = no
- capture_receipt_parser_exception_text_allowed = no

The companion contract lists every top-level, source-schema, identity,
candidate, lineage, and boundary field accepted by the current validator. It
also freezes the F03 optional-field profile and maps every included field to one
authoritative origin.

The safe receipt separately records the fixed cap, bounded read count and byte
count, oversize status, strict UTF-8 attempt/pass state, strict JSON attempt/pass
state, duplicate-key and non-standard-constant detection, and top-level-object
verification. It records no raw bytes, decoded line, key/token text, exception,
or source path.

The required evidence ID hash is the full SHA-256 of the selected row's one
evidence/content/id source value under the existing precedence. Its first 16 hex
characters must match the current safe candidate-chain evidence hash. The
required redacted snippet is a fixed full-redaction marker, not source text.

## 15. Output-location Readiness

- output_location_class_selected = yes
- logical_output_directory_label = runtime/protected_safe_payload_captures/mvp_f03_v1/
- output_location_git_ignored = yes
- gitignore_evidence = committed_runtime_directory_rule
- payload_artifact_count = 1
- receipt_artifact_count = 1
- persistence_target = no
- public_or_frontend_target = no

The output class is covered by the committed `runtime/` ignore rule. F02 did not
create or stat it. Filenames use only the full committed final candidate safe
hash and contain no raw title, identity, URL, username, or physical path.

## 16. Privacy, Custody, and Retention Readiness

- privacy_contract_complete = yes
- custody_contract_complete = yes
- retention_cleanup_contract_complete = yes
- protected_value_recursive_scan_required = yes
- silent_overwrite_allowed = no
- duplicate_copy_allowed = no
- upload_share_publish_allowed = no
- Git_add_or_commit_allowed = no
- successful_artifact_retained_through_F04 = yes
- automatic_cleanup_allowed = no

Only the F03 executor and the separately approved F04 audit may read the
artifacts before F04. Raw bytes, decoded source text, duplicate key names,
non-standard numeric tokens, and parser exceptions never enter either artifact.
Source data remains in memory only for the single session. A known temporary
partial may be removed only under an explicit F03 cleanup clause; final or
ambiguous artifacts are not overwritten. Cleanup never touches the source
package or unrelated runtime state.

## 17. F04 Handoff Readiness

- F04_handoff_complete = yes
- F04_source_reread_required = no
- F04_directory_enumeration_required = no
- F04_database_or_network_required = no
- F04_mutation_required = no

F04 receives only the payload, receipt, tracked governance references, and safe
schema/hash metadata. It independently recomputes the payload hash, checks
identity/lineage and one-candidate scope, verifies warnings and no-production
boundaries, scans protected values, and audits the receipt's byte-bound, read,
decode, strict-parser, and artifact arithmetic without reopening the source.

## 18. Unresolved Issues

- unresolved_blocking_issues = 0
- unresolved_equal_capture_alternatives = 0
- schema_mapping_gap = no
- output_ignore_gap = no
- F04_source_dependency_gap = no
- source_line_bound_gap = no
- strict_UTF8_gap = no
- strict_JSON_parser_gap = no
- parser_receipt_evidence_gap = no
- risk_buffer_accounting_gap = no

The following are intentional future boundaries, not F02 gaps:

- no real payload currently exists;
- F03 requires a separate exact human decision;
- F04 independently audits any later artifact;
- target authorization, initialization, activation, and persistence remain later
  milestones;
- the optional MVP-C01 repair allowance remains unapproved and unused.

## 19. No-side-effect Proof

- docs_only = yes
- backend_code_changed = no
- frontend_code_changed = no
- tests_changed = no
- runtime_changed = no
- configuration_changed = no
- Project_Source_changed = no
- real_package_accessed = no
- real_row_read = no
- real_payload_created = no
- real_payload_hash_calculated = no
- runtime_target_accessed = no
- SQLite_accessed = no
- gate_activated = no
- persistence_mutation_performed = no
- production_evidenceitem_created = no
- provider_or_collector_called = no
- network_or_scrape = no

All inspected inputs were tracked Git objects. No real file path was resolved or
tested, no source line was measured, and no directory outside the tracked
repository view was enumerated.

## 20. Milestone Outcome

- MVP_F02_status = candidate_completed_pending_chatgpt_acceptance_and_commit
- bounded_source_line_contract_complete = yes
- strict_UTF8_decode_contract_complete = yes
- strict_JSON_parser_contract_complete = yes
- risk_buffer_change_record_complete = yes
- F03_preparation_may_be_recommended = yes
- MVP_F03_authorized = no
- MVP_F03_executed = no
- real_source_access_authorized_now = no
- next_default = pause_pending_independent_review_and_manual_commit

F02 is candidate-complete only. This decision does not self-accept or execute
the next milestone. Its `ready` result depends on the exact byte cap, one-call
binary read, pre-decode oversize stop, strict UTF-8, nested duplicate-key and
non-standard numeric rejection, top-level object requirement, parser-safe
receipt truth rules, and `MVP-CHG-001` accounting all remaining complete and
consistent.

## 21. Git and Project Source Recommendation

- commit_recommended = yes_after_independent_ChatGPT_review
- recommended_commit_message = Establish MVP-F02 safe-payload capture readiness contract
- recommended_tag = no
- Project_Source_update_recommended = yes_after_commit

After commit:

- Canonical 00: replace to record F02 complete, fixed Prompts consumed 2,
  risk Prompts consumed 1, remaining fixed 18, conditional 10, risk 3, next fixed
  milestone F03, and no real source access.
- Canonical 09: narrow replace to record the corrected bounded-line and
  strict-parser contract, one exact future capture path, untouched
  package/row/payload state, and F03 unapproved.
- Canonical 03: no update because no stable runtime or provider/import behavior
  changed.
- Canonical 05: no update.
- Source 11: no update.

No Project Source file is modified by MVP-F02.

## 22. Next Boundary

The next recommended fixed milestone is MVP-F03, One Bounded Real Safe-payload
Capture. It remains unapproved and unexecuted. Before any source access, the
human must separately approve that exact milestone and its one-session cleanup
rules. This document supplies no reusable authorization text.
