# Sentigraph 9A-23A Synthetic Nonproduction Persistence Exact-conformance Repair Contract v0.1

## Purpose and Scope

This contract clarifies the exact forward repair required for commit `96e1939`, which implemented and synthetic-tested the 9A-23 nonproduction SQLite surface but did not fully satisfy four safety properties intended by 9A-22.

The phase is documentation only. It selects one repair architecture without modifying code, tests, schemas, SQLite files, runtime state, real payloads, gates, or production objects.

## Contract Summary

- contract_phase = 9A-23A
- docs_only = yes
- current_implementation_commit = 96e1939
- current_implementation_exists = yes
- current_implementation_conformance = needs_fix_for_exact_9a22_conformance
- privacy_issue_stop = no
- revert_required = no
- forward_repair_required = yes
- writer_entry_revalidation_contract_defined = yes
- full_rederivation_contract_defined = yes
- durable_attempt_reservation_contract_defined = yes
- cross_call_attempt_enforcement_defined = yes
- concurrent_call_resolution_defined = yes
- actual_column_integrity_recomputation_defined = yes
- receipt_semantics_split_defined = yes
- schema_versioning_defined = yes
- future_repair_slice_defined = yes
- future_regression_matrix_defined = yes
- repair_implementation_performed = no
- sqlite_accessed = no
- gate_activated = no
- actual_write_performed = no
- production_evidenceitem_created = no

`needs_fix_for_exact_9a22_conformance` does not invalidate the useful synthetic implementation or require history rewriting. It means the committed happy path is narrower than the contract's authoritative-writer, durable-attempt, integrity-proof, and truthful-receipt requirements.

## Current Committed Implementation Status

- implementation_commit = 96e1939f2edeae8a793abe27d190218423a6231b
- implementation_message = Implement 9A-23 synthetic nonproduction persistence
- implementation_performed = yes in committed 9A-23 history
- synthetic_fixture_validation_complete = yes
- temporary_sqlite_validation_complete = yes
- current_service_default_disabled = yes
- current_case_store_isolation = yes
- current_route_api_cli_frontend_exposure = no
- current_real_payload_or_runtime_target_use = no
- exact_9a22_conformance = no

The original 9A-23 health report remains an immutable record of its implementation run. This contract supplies the later conformance finding and does not rewrite that report.

## Preserved Governance State

9A-19 remains:

- human_final_write_authorization_decision = approved
- human_final_write_authorization_performed = yes
- final_write_authorization_scope = exact_locked_candidate_only

9A-20 remains:

- execution_gate_contract_established = yes
- execution_gate_status = defined_but_inactive_pending_separate_execution_approval
- execution_gate_activated = no

9A-21 remains:

- activation_readiness_outcome = not_ready_due_to_nonpersistent_or_test_only_surface

Current forward boundary:

- gate_activation_ready = no
- human_gate_activation_decision_may_be_prepared_now = no
- real_safe_payload_capture_ready = no
- actual_write_ready = no
- actual_evidence_layer_write_performed = no
- production_evidenceitem_creation_authorized = no
- production_evidenceitem_created = no

## Independent Finding Verification

### Finding 1: untrusted command at the persistence entry

Committed facts:

- `create_governed_nonproduction_evidence_record(store, command)` accepts an ordinary mapping.
- It calls `_validate_command` rather than the safe-payload validator and pure builder.
- `_validate_command` validates command shape, constants, internal field equality, and a self-supplied record hash.
- It does not independently recover source payload, expected identity, gate binding, or activation binding.
- It does not rederive the input hash, identity digest, idempotency key, persisted record ID, receipt reference, or record hash from independently supplied trusted inputs.

Classification:

- severity = P1
- writer_entry_trust_boundary_strict = no
- self_consistent_forged_command_possible = yes
- self_hash_only_validation_sufficient = no
- repair_required = yes

### Finding 2: cross-call mutating attempt limit is not durable

Committed facts:

- `mutation_attempt_number == 1` is a field check.
- The only durable table is the base-record table.
- A failed or unproven base-record transaction can leave no row.
- No independent attempt-consumption row survives that outcome.
- The same activation-scoped command can be invoked later with attempt number 1 and reach another insert path.
- Existing ambiguous tests count inserts only inside one function invocation.

Classification:

- severity = P1
- same_call_automatic_retry = no
- cross_call_second_insert_prevented = no
- maximum_mutating_attempts_durable = no
- repair_required = yes

### Finding 3: snapshot trusts stored record hash

Committed facts:

- `_snapshot_connection` selects only `persisted_record_id` and `record_canonical_hash`.
- It builds the snapshot digest from those stored hash values.
- It does not select and normalize all actual record columns.
- It does not recompute each row hash before accepting the snapshot.
- A changed column paired with a stale stored hash can evade unrelated-row comparison.

Classification:

- severity = P2
- stored_row_hash_recomputed_from_actual_columns = no
- stale_hash_tamper_detection = missing
- concurrent_integrity_attribution = partial
- repair_required = yes

### Finding 4: combined receipt capability overstates rollback or revocation

Committed facts:

- `_build_receipt` always returns `rollback_or_revocation_available = true`.
- A transaction can be rolled back before commit.
- A successful transaction cannot be rolled back after commit.
- No post-commit revocation table or store operation exists.
- The 9A-23 health report explicitly says post-commit revocation persistence is not implemented.

Classification:

- severity = P2
- pre_commit_transaction_rollback_implemented = yes
- post_commit_transaction_rollback_available = no
- post_commit_revocation_implemented = no
- combined_receipt_field_overclaims = yes
- repair_required = yes

## Current Conformance Classification

- current_9a23_exact_9a22_conformance = needs_fix_for_exact_9a22_conformance
- synthetic_happy_path_useful = yes
- current_writer_safe_for_untrusted_command_input = no
- current_attempt_limit_safe_across_calls = no
- current_snapshot_proves_actual_column_integrity = no
- current_receipt_capability_semantics_exact = no
- privacy_issue_stop = no

## No-revert and Forward-repair Posture

- commit_96e1939_exists = yes
- revert_96e1939_required = no
- history_rewrite_required = no
- new_repair_commit_required = yes
- original_9a23_health_report_modified = no

The repair must be a new forward commit after separate authorization. It preserves the isolated service and tests while replacing unsafe trust and attempt assumptions.

## Selected Overall Repair Model

- execution_model = durable_attempt_reservation_then_transactional_create_only
- base_record_mutation_model = transactional_create_only
- writer_authority_model = source_inputs_revalidated_and_command_internally_rederived
- integrity_model = actual_columns_reconstructed_and_hashes_recomputed
- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2
- two_transaction_model = yes
- reservation_committed_before_base_insert = yes
- cross_call_second_insert_prevented_by_unique_scope = yes

The selected model contains one durable reservation transaction followed by at most one base-record create transaction. There is no automatic mutation retry.

Explicitly superseded assumptions:

- one_table_only = superseded
- one_transaction_for_entire_execution = superseded
- rollback_removes_all_attempt_evidence = forbidden
- caller_supplied_command_is_write_authority = forbidden
- stored_hash_column_is_integrity_proof = forbidden
- combined_rollback_or_revocation_flag_is_sufficient = forbidden

## Authoritative Writer-entry Revalidation Contract

The repaired public call shape is:

```text
create_governed_nonproduction_evidence_record(
    store,
    *,
    payload,
    expected_identity,
    gate_contract_binding,
    activation_decision_binding,
    target_logical_label,
    mutation_attempt_number,
)
```

The public writer must:

1. Validate the exact safe payload through `validate_exact_locked_candidate_safe_write_payload`.
2. Validate the separately supplied expected immutable identity.
3. Validate gate-contract schema, version, and safe hash.
4. Validate activation-decision schema, version, candidate binding, gate binding, and safe hash.
5. Validate target logical label and mutation attempt number.
6. Obtain timestamps from an internal UTC clock after validation; tests may replace only the private clock seam.
7. Rebuild command v0.2 through the pure builder.
8. Pass only the internally rederived command to `_persist_rederived_governed_nonproduction_command`.

Required assertions:

- arbitrary_command_mapping_accepted_by_public_writer = no
- writer_revalidates_safe_payload = yes
- writer_revalidates_expected_identity = yes
- writer_revalidates_gate_binding = yes
- writer_revalidates_activation_binding = yes
- writer_rederives_all_bindings_and_ids = yes
- public_builder_output_is_write_authority = no
- self_hash_only_validation_sufficient = no

The pure command builder may remain public for inspection and tests. Its output cannot independently authorize persistence. If an expected command is supplied for diagnostics, the writer compares it against the rederived command and blocks on any difference; it never substitutes it for rederivation.

## Full Canonical Rederivation Contract

The writer must independently rederive:

- canonical validated safe payload projection;
- `input_safe_hash`;
- `candidate_identity_digest`;
- gate-contract schema, version, and safe hash;
- activation-decision ID, schema, version, candidate binding, gate binding, and safe hash;
- `idempotency_key`;
- `persisted_record_id`;
- `audit_receipt_reference`;
- `record_canonical_hash`;
- `attempt_scope_key`;
- `attempt_reservation_id`;
- `reservation_canonical_hash`.

Caller-supplied derived values are ignored or rejected. Every digest uses versioned canonical UTF-8 JSON with sorted keys and compact separators.

## Durable Attempt-reservation Schema

- table_name = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- schema_name = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1
- schema_version = 0.1
- storage_mode = immutable_append_only

Required fields:

- attempt_reservation_id
- attempt_reservation_schema
- attempt_reservation_version
- attempt_scope_key
- candidate_identity_digest
- input_safe_hash
- gate_contract_schema
- gate_contract_version
- gate_contract_safe_hash
- activation_decision_id
- activation_decision_safe_hash
- target_logical_label
- mutation_mode
- idempotency_key
- expected_persisted_record_id
- maximum_mutating_attempts
- reserved_attempt_number
- reserved_at
- reservation_canonical_hash

Fixed values:

- maximum_mutating_attempts = 1
- reserved_attempt_number = 1
- mutation_mode = transactional_create_only

Database constraints:

- primary key on `attempt_reservation_id`;
- unique constraint on `attempt_scope_key`;
- unique constraint on `idempotency_key`;
- checks for exact schema/version, mutation mode, maximum attempts, and reserved attempt number;
- no update, replace, upsert, merge, delete, or re-arm operation.

## Attempt-scope Key and Reservation ID

`attempt_scope_key` is a canonical SHA-256 digest over:

- schema namespace `sentigraph_governed_nonproduction_attempt_scope_v0_1`;
- candidate identity digest;
- activation-decision safe hash;
- gate-contract safe hash;
- target logical label;
- mutation mode;
- command schema/version.

`attempt_reservation_id` is deterministically derived from a versioned namespace plus `attempt_scope_key`. The reservation canonical hash is recomputed from all actual reservation fields except its own hash field.

## Attempt-consumption Semantics

- mutating_attempt_consumed_at = successful_durable_attempt_reservation_commit
- attempt_limit = 1
- base_insert_issue_without_committed_reservation = forbidden
- reservation_rollback_consumes_attempt = no when non-commit is conclusively known
- ambiguous_reservation_outcome_allows_retry = no
- consumed_reservation_without_record_allows_base_insert_on_later_call = no

This definition intentionally replaces the earlier statement that consumption occurs only when the base-record insert is issued.

The crash window after reservation commit and before base insert is conservative: the attempt remains consumed and the workflow pauses. Another mutation requires fresh governance, a new activation decision, or a separately designed re-arming contract. No automatic repair write exists.

## Two-transaction Execution Model

### Phase A: reservation

1. Revalidate source inputs and rederive command and reservation.
2. Read-only verify whether the exact base record already exists.
3. Read-only verify whether the attempt reservation already exists.
4. If the exact record exists, perform zero mutations and return idempotent success.
5. If a reservation exists without an exact verified record, perform zero mutations and pause.
6. If no reservation exists, begin one reservation transaction.
7. Insert exactly one immutable reservation.
8. Commit the reservation.
9. Verify the reservation from actual stored columns.

### Phase B: base record

1. Enter only after a known successful reservation commit in the same call.
2. Begin a separate base-record transaction.
3. Recheck exact record and conflicts read-only inside the transaction.
4. Issue at most one plain base-record insert.
5. Commit or roll back once.
6. Perform read-only reservation and record verification.
7. Never retry the insert automatically or under the same attempt scope.

The base-record table retains `transactional_create_only`; no base-record field changes are required by this repair.

## Cross-call Behavior

Exact base record already present:

- reservation mutation = 0
- base-record mutation = 0
- final outcome = already_exists_same_record

Reservation present and exact base record absent:

- reservation mutation = 0
- base-record mutation = 0
- final outcome = paused_mutating_attempt_already_consumed_without_verified_record

No reservation and no record:

- reservation mutation = 1
- base-record mutation = at most 1 in the same call

A later call under the same `attempt_scope_key` cannot issue another base-record insert.

## Concurrent-call Behavior

The unique `attempt_scope_key` constraint is the authoritative cross-process guard.

For two concurrent identical calls:

1. Both rederive the same attempt scope.
2. At most one reservation insert can commit.
3. The losing call handles the uniqueness result through read-only reservation and record resolution.
4. The losing call never reaches base-record insert.
5. The winning call may issue at most one base-record insert after reservation verification.
6. Any unrelated concurrent change causes conservative pause.

Safety is preferred over throughput.

## Ambiguous Reservation Handling

If reservation commit returns an ambiguous exception:

1. Close the mutating path.
2. Perform read-only lookup by both `attempt_scope_key` and reservation ID.
3. Reconstruct all reservation columns and recompute its hash.
4. If the exact reservation exists, mark the attempt consumed and pause.
5. If it cannot be conclusively verified, pause with unknown reservation state.
6. Do not retry reservation insertion.
7. Do not proceed to base-record insertion in that call.

Exact outcomes:

- verified reservation = paused_attempt_reservation_commit_ambiguous_attempt_consumed
- unverified reservation = paused_attempt_reservation_commit_ambiguous_not_proven

## Ambiguous Base-record Commit Handling

If base-record commit is ambiguous:

1. The attempt is already consumed by the durable reservation.
2. Close the base-record mutating path.
3. Perform read-only full-column record and reservation verification.
4. If the exact single record is proven and no unrelated change exists, report verified create.
5. Otherwise return `paused_ambiguous_commit_not_proven`.
6. Never issue another base-record insert under that attempt scope.

## Base-record Create-only Semantics

- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1
- mutation_mode = transactional_create_only
- insert_count_per_attempt_scope = 1 maximum
- update_allowed = no
- upsert_allowed = no
- replace_allowed = no
- merge_allowed = no
- repair_write_allowed = no
- fallback_target_allowed = no

The base record remains immutable. The attempt reservation is a separate governance artifact and does not convert the base record into a production object.

## Stored-row Actual-column Integrity Recalculation

The repaired record snapshot must not trust stored `record_canonical_hash` values.

For every base-record row it must:

1. Select every canonical record column.
2. Parse canonical JSON fields.
3. Normalize SQLite booleans and nullable fields.
4. Validate exact record field shape and constants.
5. Recompute the canonical hash from actual columns excluding the stored hash column.
6. Compare recomputed and stored hashes.
7. Mark any mismatch, malformed JSON, invalid type, or invalid constant as integrity failure.
8. Build the table snapshot from recomputed hashes.

The snapshot result contains only safe IDs, recomputed hashes, count, digest, and integrity status. It does not log payload text.

## Attempt-ledger Integrity Recalculation

The same rule applies to every reservation row:

1. Select every reservation column.
2. Normalize values and validate exact schema.
3. Recompute `reservation_canonical_hash` from actual columns.
4. Compare it with the stored value.
5. Mark stale hash, malformed values, and schema mismatches as integrity failure.
6. Build the ledger snapshot from recomputed hashes.

No successful receipt may rely on a ledger snapshot with an integrity failure.

## Conservative Concurrency Verification

Separate safe snapshots are required:

- attempt-ledger snapshot before and after reservation;
- record-table snapshot before and after base-record creation.

Each mutation phase must prove:

- exactly one intended row was added when its mutation count is 1;
- no unrelated row was added, deleted, or changed;
- no stale stored hash concealed a column change;
- the exact reservation and record bindings agree.

Any unrelated concurrent change, even legitimate activity, yields:

- unrelated_change_detected = yes
- post_write_readback_verified = no
- workflow_disposition = pause

This conservative false-positive posture is selected intentionally.

## Receipt v0.2 Schema

- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2
- old_combined_field = rollback_or_revocation_available
- old_combined_field_status = removed_from_v0_2

Required fields include:

- receipt_id
- receipt_schema
- attempt_reservation_id
- attempt_scope_key
- attempt_reservation_committed
- mutating_attempt_consumed
- base_record_insert_issued
- base_record_transaction_started
- base_record_transaction_committed
- mutation_count
- transaction_rollback_performed
- transaction_rollback_available_before_commit
- transaction_rollback_available_after_commit
- post_commit_revocation_implemented
- post_commit_revocation_available
- exact_record_verified
- attempt_reservation_verified
- no_unrelated_attempt_change_verified
- no_unrelated_record_change_verified
- final_outcome
- created_at

The receipt remains safe and in memory. It contains no physical path, raw value, secret, production object, or approval phrase.

## Rollback and Revocation Semantics

Before base-record commit:

- transaction_rollback_available_before_commit = yes

After successful base-record commit:

- transaction_rollback_available_after_commit = no

Current repaired initial slice:

- post_commit_revocation_implemented = no
- post_commit_revocation_available = no

Known pre-commit rollback:

- transaction_rollback_performed = yes
- base_record_transaction_committed = no
- mutating_attempt_consumed = yes because reservation already committed
- post_commit_revocation_available = no

Successful create:

- transaction_rollback_performed = no
- base_record_transaction_committed = yes
- transaction_rollback_available_after_commit = no
- post_commit_revocation_implemented = no
- post_commit_revocation_available = no

Idempotent replay:

- base_record_insert_issued = no
- mutation_count = 0
- exact_record_verified = yes

No outcome uses the old unconditional combined capability claim.

## Schema-version Compatibility Decision

- payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1, unchanged
- payload_schema_version = 0.1
- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1, unchanged
- attempt_reservation_schema = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1, new
- internal_command_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_2, new version
- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2, new version

The payload and base-record fields do not change. Command semantics and receipt fields do change, so they receive new versions. Temporary 9A-23 databases are disposable and receive no migration guarantee. The logical runtime database has never been created or accessed, so this phase defines no migration.

## Future Repair Implementation File Plan

The separately approved repair is limited to exactly three files:

1. `backend/app/services/governed_nonproduction_evidence_persistence.py`
   - public writer revalidation;
   - command v0.2 internal rederivation;
   - attempt-reservation table and two-transaction flow;
   - actual-column record and reservation snapshots;
   - receipt v0.2.
2. `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
   - update existing expectations only where v0.2 requires it;
   - add all four defect-class regressions.
3. `docs/health/sentigraph_9a_23b_synthetic_nonproduction_persistence_exact_conformance_repair_report_v0_1.md`
   - record TDD, synthetic temporary-target validation, and preserved boundaries.

- three_file_slice_sufficient = yes
- dependency_change_required = no
- route_api_cli_frontend_change_required = no
- generic_case_store_change_required = no
- runtime_configuration_change_required = no
- project_source_file_in_repo_required = no

## Future Synthetic Regression Matrix

Writer trust boundary:

1. Tamper redacted text in builder output.
2. Recompute the old record hash.
3. Public writer blocks because it rebuilds from source inputs.
4. Tamper safe payload while retaining self-consistent command hashes.
5. Tamper candidate identity digest.
6. Tamper gate binding.
7. Tamper activation binding.
8. Tamper idempotency key.
9. Tamper persisted record ID.
10. Tamper receipt reference.
11. Every tampering case blocks before SQLite mutation.

Attempt reservation:

12. First call reserves one attempt and creates one record.
13. Exact replay performs zero mutations.
14. Base-record insert rollback leaves reservation consumed.
15. Second call after rollback issues zero inserts.
16. Ambiguous base-record rollback followed by another call issues zero inserts.
17. Crash after reservation leaves the attempt consumed.
18. Two concurrent identical calls create one reservation and at most one base-record insert.
19. Competing call receives a read-only pause or idempotent result.
20. Reservation-commit ambiguity never proceeds to base-record insert.

Integrity verification:

21. Change an unrelated stored column while retaining its stale hash.
22. Recomputed snapshot detects the integrity failure.
23. Change stored canonical JSON while retaining its stale hash.
24. Malformed stored JSON causes pause.
25. Concurrent unrelated insertion causes conservative pause.
26. Reservation stale-hash tampering is detected.

Receipt semantics:

27. Successful commit reports rollback unavailable after commit.
28. Successful commit reports post-commit revocation unimplemented and unavailable.
29. Pre-commit rollback reports rollback performed.
30. Idempotent replay reports no new insert.
31. Consumed reservation without a record reports pause.
32. No outcome returns the old unconditional combined claim.

Preserved boundaries:

33. Store remains disabled by default.
34. Tests use temporary SQLite only.
35. No real candidate values appear.
36. No physical paths leak.
37. No CaseRepository, generic store, route, network, provider, collector, or production object integration appears.
38. Focused and nearby regressions pass.
39. `py_compile` passes.
40. Static forbidden scans and `git diff --check` pass.

## Privacy and Production Boundaries

The repair remains synthetic-only and must not:

- read or create a real safe payload;
- access a package, row, configured store, or logical runtime target;
- expose raw text, identities, URLs, paths, PII, or secrets;
- integrate CaseRepository or generic stores;
- create routes, APIs, CLIs, frontend surfaces, provider or collector jobs;
- activate the execution gate;
- approve or execute actual Evidence Layer write;
- authorize or create a production `EvidenceItem`, Review Queue item, case, analysis run, Analysis Result, report, export, public, or delivery object.

## No-side-effect State

- repair_code_changed = no
- tests_changed = no
- existing_health_report_changed = no
- sqlite_accessed = no
- runtime_target_accessed = no
- real_payload_accessed = no
- package_or_row_read = no
- gate_activated = no
- actual_write_performed = no
- production_evidenceitem_created = no
- provider_or_collector_called = no
- real_api_or_llm_called = no
- network_or_scrape = no

## Architecture Outcome and Next Boundary

- architecture_outcome = ready_for_separate_narrow_9a23b_exact_conformance_repair_implementation_authorization
- narrow_repair_implementation_authorization_may_be_prepared = yes
- implementation_authorized_now = no
- gate_activation_next = no
- real_safe_payload_next = no
- actual_write_next = no
- production_evidenceitem_next = no
- next_boundary = separately_approved_narrow_9a23b_synthetic_only_exact_conformance_repair

The next phase may implement only the three-file synthetic repair. It must receive a new human authorization that is not supplied or templated here.
