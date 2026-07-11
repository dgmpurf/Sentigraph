# Sentigraph 9A-23A Synthetic Nonproduction Persistence Exact-conformance Repair Decision v0.1

## Decision

- phase = 9A-23A
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- current_implementation_commit = 96e1939
- current_implementation_conformance = needs_fix_for_exact_9a22_conformance
- revert_required = no
- history_rewrite_required = no
- forward_repair_required = yes
- repair_implementation_performed = no
- sqlite_accessed = no
- gate_activation_ready = no
- human_gate_activation_decision_may_be_prepared_now = no
- real_safe_payload_capture_ready = no
- actual_write_ready = no
- production_evidenceitem_creation_authorized = no

`decision = ready` means the 9A-23A clarification is complete. It does not mean the existing implementation is exactly conformant, the repair is authorized, or any real payload, activation, write, or production object is ready.

## Approval Validation

- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- approval_scope = docs-only exact-conformance clarification and future repair design

Validated phrase:

`APPROVE_9A_23A_SYNTHETIC_NONPRODUCTION_PERSISTENCE_EXACT_9A22_CONFORMANCE_REPAIR_ARCHITECTURE_CLARIFICATION_DOCS_ONLY`

This phrase did not authorize code repair, tests, SQLite access, real payload capture, runtime-target access, gate activation, actual write, or production `EvidenceItem` creation.

## Committed Anchor

- expected_branch = main
- observed_branch = main
- expected_commit = 96e1939
- observed_commit = 96e1939f2edeae8a793abe27d190218423a6231b
- observed_commit_message = Implement 9A-23 synthetic nonproduction persistence
- origin_main_commit = 96e1939f2edeae8a793abe27d190218423a6231b
- worktree_started_clean = yes
- origin_alignment = exact

## Finding 1 Decision: Writer Trust Boundary

- severity = P1
- writer_entry_trust_boundary_strict = no
- self_consistent_forged_command_possible = yes
- current_public_writer_revalidates_safe_payload = no
- current_public_writer_rederives_all_bindings_and_ids = no
- self_hash_only_validation_sufficient = no
- repair_required = yes

The current public writer accepts a command mapping and validates only its shape, internal equalities, constants, and self-supplied hash. It does not independently rebuild authority from payload, expected identity, gate, and activation inputs.

## Finding 2 Decision: Durable Attempt Limit

- severity = P1
- same_call_automatic_retry = no
- mutation_attempt_number_field_check_exists = yes
- durable_attempt_consumption_record_exists = no
- cross_call_second_insert_prevented = no
- maximum_mutating_attempts_durable = no
- repair_required = yes

The current base-record transaction can roll back without leaving attempt evidence. A later call can again present attempt number 1 and reach insert.

## Finding 3 Decision: Stored-row Integrity

- severity = P2
- stored_row_hash_recomputed_from_actual_columns = no
- stale_hash_tamper_detection = missing
- snapshot_uses_stored_hash_column = yes
- concurrent_integrity_attribution = partial
- repair_required = yes

The current snapshot digest trusts the stored hash column rather than reconstructing and hashing actual row columns.

## Finding 4 Decision: Receipt Rollback and Revocation

- severity = P2
- pre_commit_transaction_rollback_implemented = yes
- post_commit_transaction_rollback_available = no
- post_commit_revocation_implemented = no
- current_combined_field_always_true = yes
- combined_receipt_field_overclaims = yes
- repair_required = yes

The combined field cannot truthfully represent the distinct pre-commit rollback and post-commit revocation states.

## Current Implementation Conformance

- implementation_performed = yes in 9A-23 history
- synthetic_fixture_validation_complete = yes
- temporary_sqlite_validation_complete = yes
- disabled_by_default_implemented = yes
- generic_case_store_isolated = yes
- exact_9a22_conformance = no
- current_classification = needs_fix_for_exact_9a22_conformance
- privacy_issue_stop = no

The implementation remains a useful synthetic checkpoint, but its health report cannot be used as proof of the four missing properties.

## No-revert and Forward-repair Decision

- commit_96e1939_preserved = yes
- revert_96e1939_required = no
- history_rewrite_required = no
- original_health_report_remains_immutable = yes
- new_forward_repair_commit_required = yes

The correction is additive: retain the historical implementation and commit a separately authorized repair.

## Selected Writer Trust Model

- model = source_inputs_revalidated_and_command_internally_rederived
- arbitrary_command_mapping_accepted_by_public_writer = no
- public_writer_inputs = payload, expected identity, gate binding, activation binding, logical target, attempt number
- safe_payload_validator_called_inside_writer = yes
- pure_builder_called_inside_writer = yes
- private_persistence_symbol = _persist_rederived_governed_nonproduction_command
- caller_derived_fields_authoritative = no

The pure builder may remain public for inspection, but its returned mapping cannot independently authorize persistence.

## Selected Canonical Rederivation Model

The public writer independently recomputes:

- safe payload and input hash;
- candidate identity digest;
- gate and activation bindings;
- idempotency key;
- persisted record ID;
- receipt reference;
- record canonical hash;
- attempt scope key;
- reservation ID and hash.

Any supplied diagnostic command is compare-only and cannot replace rederivation.

## Selected Attempt-reservation Model

- execution_model = durable_attempt_reservation_then_transactional_create_only
- reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- reservation_schema = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1
- reservation_mode = immutable_append_only
- base_record_mode = transactional_create_only
- two_transaction_model = yes
- reservation_committed_before_base_insert = yes
- maximum_mutating_attempts = 1
- unique_attempt_scope_key = yes
- cross_call_second_insert_prevented_by_unique_scope = yes
- unique_idempotency_key = yes

The previous one-table model is superseded. The reservation and base record use separate transactions in the same isolated SQLite database.

## Selected Attempt-consumption Point

- mutating_attempt_consumed_at = successful_durable_attempt_reservation_commit
- base_record_insert_consumes_attempt = no, reservation already consumed it
- rollback_removes_attempt_evidence = no
- crash_after_reservation_rearms_automatically = no
- second_call_after_consumed_reservation_may_insert = no

A committed reservation without a verified base record returns `paused_mutating_attempt_already_consumed_without_verified_record`.

## Cross-call and Concurrent-call Policy

- cross_call_guard = unique attempt_scope_key
- concurrent_winner_count = 1 maximum
- concurrent_loser_mutations_after_resolution = 0
- concurrent_loser_base_insert_allowed = no
- unrelated_concurrent_change_policy = conservative_pause

Two identical calls derive the same attempt scope. Only the reservation winner may proceed toward one base-record insert; the loser performs read-only resolution.

## Ambiguous Reservation Policy

- mutation_retry_allowed = no
- base_record_insert_after_ambiguous_reservation = no
- exact_reservation_found = attempt consumed and pause
- reservation_not_proven = pause with unknown state

The current call never proceeds to base-record mutation from an ambiguous reservation-commit state.

## Ambiguous Base-record Policy

- attempt_already_consumed = yes
- second_insert_in_same_or_later_call = no
- verification_mode = read-only full-column reconstruction
- exact_record_verified = report verified create
- exact_record_not_verified = paused_ambiguous_commit_not_proven

## Selected Actual-column Snapshot Policy

- stored_hash_trusted_without_recomputation = no
- actual_columns_selected = all canonical columns
- canonical_json_parsed = yes
- SQLite booleans_and_nulls_normalized = yes
- actual_record_shape_validated = yes
- hash_recomputed_from_actual_columns = yes
- stale_hash_mismatch = integrity failure
- snapshot_digest_source = recomputed hashes

The same policy applies independently to the attempt ledger and base-record table. Malformed JSON, stale hashes, or unrelated concurrent changes force pause.

## Selected Receipt Schema and Field Split

- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2
- old_combined_field = rollback_or_revocation_available
- old_combined_field_status = removed
- pre_commit_rollback_field = transaction_rollback_available_before_commit
- post_commit_rollback_field = transaction_rollback_available_after_commit
- rollback_performed_field = transaction_rollback_performed
- revocation_implemented_field = post_commit_revocation_implemented
- revocation_available_field = post_commit_revocation_available

The v0.2 receipt also records reservation commitment, attempt consumption, insert issuance, base transaction state, reservation verification, record verification, and separate unrelated-change proofs.

Truthful current values after successful create:

- transaction_rollback_available_after_commit = no
- post_commit_revocation_implemented = no
- post_commit_revocation_available = no

## Schema-version Decision

- payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1, unchanged
- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1, unchanged
- attempt_reservation_schema = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1, new
- command_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_2, new
- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2, new
- migration_required_for_9a23_temporary_databases = no
- logical_runtime_database_migration_required = no because it has never been created or accessed

## Future Implementation Allowlist

The 9A-23B repair is limited to:

- `backend/app/services/governed_nonproduction_evidence_persistence.py`
- `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
- `docs/health/sentigraph_9a_23b_synthetic_nonproduction_persistence_exact_conformance_repair_report_v0_1.md`

- three_file_slice_sufficient = yes
- fourth_file_required = no
- dependency_change_required = no
- route_api_cli_frontend_change_required = no
- generic_store_change_required = no
- runtime_configuration_change_required = no

## Future Test Matrix Summary

The future synthetic suite contains 40 required checks:

- 11 writer revalidation and command-tampering checks;
- 9 durable reservation, cross-call, crash, and concurrency checks;
- 6 actual-column and stale-hash integrity checks;
- 6 receipt-state checks;
- 8 preserved safety, temporary-target, regression, compile, and static checks.

The complete numbered matrix is normative in the companion architecture contract.

## Architecture Outcome

- architecture_outcome = ready_for_separate_narrow_9a23b_exact_conformance_repair_implementation_authorization
- all_four_findings_verified = yes
- repair_model_single_and_complete = yes
- unresolved_repair_design_gap = none
- code_repair_performed = no

## Whether Narrow Repair Authorization May Be Prepared

- narrow_9a23b_repair_authorization_may_be_prepared = yes
- repair_authorized_now = no
- gate_activation_authorization_may_be_prepared = no
- real_payload_authorization_may_be_prepared = no
- actual_write_authorization_may_be_prepared = no

Any later implementation authorization must be newly human-authored. This document contains no future approval phrase or ready-to-sign text.

## Selected Next Boundary

- next_default = pause_before_repair_implementation
- selected_next_boundary = separately_approved_narrow_9a23b_synthetic_only_exact_conformance_repair
- real_safe_payload_next = no
- gate_activation_next = no
- actual_write_next = no
- production_evidenceitem_next = no

## No-side-effect State

- backend_code_changed = no
- backend_tests_changed = no
- existing_health_report_changed = no
- sqlite_accessed = no
- runtime_target_accessed = no
- package_or_row_read = no
- real_payload_accessed = no
- gate_activated = no
- actual_write_performed = no
- production_evidenceitem_created = no
- project_source_changed = no
- github_actions_changed = no

## Git, Tag, and Source Recommendation

- commit_recommended = yes
- recommended_commit_message = Clarify 9A-23A exact persistence conformance repair
- tag_recommended = no
- project_source_update_recommended = yes after commit
- canonical_00_recommendation = replace after commit
- canonical_09_recommendation = replace after commit
- canonical_03_recommendation = no update in 9A-23A because runtime behavior did not change

Canonical 03 should be updated only after the repair implementation is committed.
