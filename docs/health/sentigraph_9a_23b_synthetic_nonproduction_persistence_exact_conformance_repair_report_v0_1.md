# Sentigraph 9A-23B Synthetic Nonproduction Persistence Exact-conformance Repair Report v0.1

## Decision

- phase = 9A-23B
- decision = ready
- privacy_issue_stop = no
- implementation_scope = narrow_synthetic_only_exact_9a22_conformance_repair
- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- implementation_performed = yes, synthetic conformance repair only
- starting_branch = main
- starting_commit = 162c3604efd6a270a62147f27bf67026181d12fa
- starting_commit_message = Clarify 9A-23A exact persistence conformance repair
- origin_alignment = exact
- starting_worktree_clean = yes
- actual_model_exposure = current local Codex model; exact deployment identifier hidden
- goal_requested = yes
- goal_activation_verified = yes
- goal_completion_verified = yes

The approval phrase was:

`APPROVE_9A_23B_NARROW_SYNTHETIC_ONLY_GOVERNED_NONPRODUCTION_PERSISTENCE_EXACT_9A22_CONFORMANCE_REPAIR_IMPLEMENTATION`

It authorized only the synthetic conformance repair described here. It did not authorize a real payload, logical runtime target, gate activation, actual Evidence Layer write, or production `EvidenceItem`.

## Changed Files

1. `backend/app/services/governed_nonproduction_evidence_persistence.py`
2. `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
3. `docs/health/sentigraph_9a_23b_synthetic_nonproduction_persistence_exact_conformance_repair_report_v0_1.md`

- three_file_allowlist_result = pass
- fourth_file_changed = no

## Caller Inventory

- service_definition_found = yes
- approved_focused_test_callers_found = yes
- other_test_caller_found = no
- non_test_caller_found = no
- compatibility_overload_required = no

The old writer signature had no non-test consumer. The only executable callers were the service and the approved focused test module. Documentation references remain historical or contractual text.

## TDD Evidence

- test_first = yes
- red_test_command = `python -m pytest backend/app/tests/test_governed_nonproduction_evidence_persistence.py -q`
- red_failed_tests = 4
- red_failure_reasons = missing source-input writer signature; no durable attempt-consumption receipt or ledger; actual-column tampering not detected by snapshot; receipt remained v0.1 with the combined rollback/revocation claim
- red_verified = yes
- red_unrelated_failure_used = no
- green_test_command = `python -m pytest backend/app/tests/test_governed_nonproduction_evidence_persistence.py -q`
- green_result = pass
- focused_test_count = 68
- focused_passed_count = 68
- focused_failed_count = 0
- focused_duration = 1.08 seconds from the summary-enabled confirmation run

The four RED failures came from the committed 9A-23 behavior. After the service repair and full matrix completion, the same focused module passed.

## Repair Results

- authoritative_writer_entry_implemented = yes
- caller_command_write_authority_removed = yes
- command_v0_2_implemented = yes
- full_internal_rederivation_implemented = yes
- attempt_reservation_table_implemented = yes
- durable_cross_call_attempt_limit_implemented = yes
- concurrent_second_insert_prevention_implemented = yes
- two_transaction_model_implemented = yes
- actual_column_record_hash_recomputation_implemented = yes
- actual_column_reservation_hash_recomputation_implemented = yes
- conservative_concurrency_verification_implemented = yes
- receipt_v0_2_implemented = yes
- old_combined_receipt_field_removed = yes
- truthful_rollback_fields_implemented = yes
- post_commit_revocation_reported_unimplemented = yes

The public writer now accepts only source payload, expected identity, gate binding, activation binding, logical target, and attempt number as keyword-only inputs. It validates and rederives the internal command itself. A positional or keyword `command` mapping is rejected by the Python call contract before SQLite can open.

## Schema Results

- payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1, unchanged
- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1, unchanged
- attempt_reservation_schema = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1, new
- command_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_2, new
- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2, new
- attempt_reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- base_record_table = governed_nonproduction_evidence_records_v0_1
- initialization_table_count = 2

No production schema or generic storage module changed.

## Transaction Results

- attempt_consumption_point = successful_durable_attempt_reservation_commit
- reservation_transaction = separate append-only transaction
- base_record_transaction = separate create-only transaction
- maximum_mutating_attempts = 1
- known_reservation_rollback_behavior = reservation absent, attempt not consumed, no base INSERT in that call
- reservation_ambiguity_behavior = read-only verification and pause; base INSERT forbidden
- known_base_record_rollback_behavior = reservation remains committed, attempt remains consumed, base record count remains zero
- base_record_ambiguity_behavior = read-only verification only; no INSERT retry
- cross_call_replay_behavior = exact record returns zero-mutation idempotent result; consumed reservation without record returns pause
- concurrent_call_behavior = one reservation winner; competing call performs no base INSERT
- automatic_retry = no
- rearm_or_attempt_reset = no

The attempt scope is a canonical SHA-256 binding of the versioned namespace, candidate digest, activation hash, gate hash, logical target, mutation mode, and command schema/version. It contains no timestamp.

## Integrity Results

- record_snapshot_source = all actual record columns
- reservation_snapshot_source = all actual reservation columns
- canonical_json_parsed = yes
- sqlite_boolean_and_null_normalization = yes
- stored_record_hash_recomputed = yes
- stored_reservation_hash_recomputed = yes
- stale_record_hash_detected = yes
- changed_json_with_stale_hash_detected = yes
- malformed_json_detected = yes
- stale_reservation_hash_detected = yes
- unrelated_concurrent_change_causes_pause = yes
- stored_hash_column_used_as_authority = no

No unsafe value is echoed by integrity errors.

## Receipt Results

- receipt_persistence = in_memory_only
- receipt_physical_database_path_present = no
- receipt_raw_payload_present = no
- receipt_source_url_present = no
- receipt_pii_present = no
- receipt_secret_present = no
- receipt_approval_phrase_present = no
- transaction_rollback_available_after_commit = false
- post_commit_revocation_implemented = false
- post_commit_revocation_available = false
- production_evidenceitem_created = false
- production_case_changed = false
- downstream_runtime_called = false

The v0.1 field `rollback_or_revocation_available` appears in this report only as the historical defect name and in a focused negative assertion. It is absent from the live v0.2 receipt builder and returned receipts.

## Timestamp and Idempotency

- public_writer_accepts_created_at = no
- private_utc_clock_seam = yes
- idempotency_key_depends_on_timestamp = no
- persisted_record_id_depends_on_timestamp = no
- attempt_scope_key_depends_on_timestamp = no
- attempt_reservation_id_depends_on_timestamp = no
- audit_receipt_reference_depends_on_timestamp = no
- exact_replay_preserves_original_created_at = yes
- created_at_assigned_only_to_new_record = yes
- reserved_at_assigned_only_to_new_reservation = yes

## Forty-item Synthetic Regression Matrix

Evidence command aliases:

- `FOCUSED`: `python -m pytest backend/app/tests/test_governed_nonproduction_evidence_persistence.py -q`
- `NEARBY`: the individual nearby commands listed under Validation
- `COMBINED`: the four-file combined pytest command listed under Validation
- `COMPILE`: the py_compile command listed under Validation
- `STATIC`: caller, forbidden-integration, safety, whitespace, and Git checks listed under Validation

| # | Required proof | Test or static check | Result | Evidence command |
| --- | --- | --- | --- | --- |
| 1 | Tampered redacted text in builder output | `test_public_writer_has_keyword_only_source_contract_and_all_forged_commands_block_before_io` | pass | FOCUSED |
| 2 | Old record hash can be recomputed but gains no authority | same forged-command test | pass | FOCUSED |
| 3 | Writer rejects command authority and rederives source inputs | `test_public_writer_rederives_from_source_inputs_and_rejects_command_authority` | pass | FOCUSED |
| 4 | Self-consistent safe-payload command tampering blocks | forged-command test | pass | FOCUSED |
| 5 | Candidate digest tampering blocks | forged-command test | pass | FOCUSED |
| 6 | Gate binding tampering blocks | forged-command test and `test_gate_and_activation_bindings_are_strict` | pass | FOCUSED |
| 7 | Activation binding tampering blocks | same binding and forged-command tests | pass | FOCUSED |
| 8 | Idempotency-key tampering blocks | forged-command test | pass | FOCUSED |
| 9 | Persisted-record ID tampering blocks | forged-command test | pass | FOCUSED |
| 10 | Receipt-reference tampering blocks | forged-command test | pass | FOCUSED |
| 11 | Caller-command tampering blocks before SQLite | forged-command test with failing sqlite seam | pass | FOCUSED |
| 12 | First call creates one reservation and one record | `test_valid_single_create_and_receipt_verification` | pass | FOCUSED |
| 13 | Exact replay performs zero mutations | `test_exact_replay_performs_zero_reservation_and_record_mutations` | pass | FOCUSED |
| 14 | Base INSERT rollback leaves reservation consumed | `test_consumed_attempt_blocks_second_call_after_record_rollback` | pass | FOCUSED |
| 15 | Second call after rollback issues zero base INSERTs | same consumed-attempt test | pass | FOCUSED |
| 16 | Ambiguous base rollback followed by another call issues zero INSERTs | `test_ambiguous_base_record_rollback_consumes_attempt_and_later_call_never_inserts` | pass | FOCUSED |
| 17 | Controlled stop after reservation leaves attempt consumed | `test_controlled_stop_after_reservation_commit_leaves_attempt_consumed` | pass | FOCUSED |
| 18 | Concurrent identical calls create one reservation and at most one base INSERT | `test_concurrent_identical_calls_allow_at_most_one_base_record_insert` | pass | FOCUSED |
| 19 | Competing call receives read-only pause or idempotent result | same deterministic concurrency test | pass | FOCUSED |
| 20 | Reservation ambiguity never reaches base INSERT | `test_reservation_commit_ambiguity_never_reaches_base_record_insert` and unproven variant | pass | FOCUSED |
| 21 | Actual unrelated stored column change with stale hash | `test_snapshot_recomputes_hash_from_actual_record_columns` | pass | FOCUSED |
| 22 | Recomputed snapshot detects integrity failure | same actual-column snapshot test | pass | FOCUSED |
| 23 | Canonical JSON column change with stale hash | `test_snapshot_detects_stale_hash_after_canonical_json_column_change` | pass | FOCUSED |
| 24 | Malformed stored JSON blocks | `test_snapshot_rejects_malformed_stored_record_json` | pass | FOCUSED |
| 25 | Concurrent unrelated insertion causes conservative pause | `test_unrelated_concurrent_record_insert_forces_conservative_pause` | pass | FOCUSED |
| 26 | Reservation stale-hash tampering is detected | `test_attempt_snapshot_detects_stale_reservation_hash` | pass | FOCUSED |
| 27 | Successful commit reports rollback unavailable after commit | `test_receipt_v02_removes_combined_rollback_revocation_claim` | pass | FOCUSED |
| 28 | Post-commit revocation is unimplemented and unavailable | same receipt test | pass | FOCUSED |
| 29 | Pre-commit base rollback reports rollback performed | `test_known_insert_failure_rolls_back_without_record` | pass | FOCUSED |
| 30 | Idempotent replay reports no base INSERT | exact replay tests | pass | FOCUSED |
| 31 | Consumed reservation without record reports pause | consumed-attempt and controlled-stop tests | pass | FOCUSED |
| 32 | Old combined receipt claim is absent | receipt negative assertion and source scan | pass | FOCUSED + STATIC |
| 33 | Store remains disabled by default | `test_store_defaults_disabled_and_creates_nothing` | pass | FOCUSED |
| 34 | SQLite targets are temporary only | focused fixtures use `tmp_path`; no repository target accessed | pass | FOCUSED + STATIC |
| 35 | No real candidate values appear | synthetic-value scan | pass | STATIC |
| 36 | No physical database path leaks | `test_record_and_receipt_do_not_expose_physical_path_or_production_objects` | pass | FOCUSED |
| 37 | Generic stores, routes, network, provider, collector, and production objects remain isolated | `test_new_module_has_no_forbidden_integration_references` and caller scan | pass | FOCUSED + STATIC |
| 38 | Focused and nearby regressions pass | 68 focused and 202 combined tests | pass | FOCUSED + NEARBY + COMBINED |
| 39 | Service and test compile | both approved Python files | pass | COMPILE |
| 40 | Static scans and Git diff check pass | static safety and `git diff --check` | pass | STATIC |

- regression_matrix_mapped_count = 40
- regression_matrix_passed_count = 40
- regression_matrix_failed_count = 0
- regression_matrix_result = pass

## Validation

Focused test:

`python -m pytest backend/app/tests/test_governed_nonproduction_evidence_persistence.py -q`

- result = pass
- confirmation_count = 68 passed
- confirmation_duration = 1.08 seconds

Nearby regression 1:

`python -m pytest backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py -q`

- result = pass

Nearby regression 2:

`python -m pytest backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py -q`

- result = pass

Selected temporary/local storage-boundary regression:

`python -m pytest backend/app/tests/test_local_exchange_reader.py -q`

- result = pass
- safety_basis = all file writes and reads are under pytest `tmp_path`; the reader is metadata-only, performs no network request, accesses no configured real exchange directory, and does not parse evidence row files

Combined suite:

`python -m pytest backend/app/tests/test_governed_nonproduction_evidence_persistence.py backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py backend/app/tests/test_local_exchange_reader.py -q`

- result = pass
- combined_count = 202 passed
- combined_duration = 1.61 seconds

Compile:

`python -m py_compile backend/app/services/governed_nonproduction_evidence_persistence.py backend/app/tests/test_governed_nonproduction_evidence_persistence.py`

- result = pass

Static results:

- caller_scan_result = pass; no non-test caller
- forbidden_integration_scan_result = pass; standard-library-only service imports
- real_candidate_value_scan_result = pass; synthetic fixtures only
- physical_path_leak_scan_result = pass
- receipt_overclaim_scan_result = pass; old field only in negative test and historical report text
- text_quality_scan_result = pass
- git_diff_check_result = pass
- three_file_allowlist_result = pass

The URL and email-like strings in the focused test are reserved synthetic negative-test markers using invalid domains. No actual PII or credential value is present.

## Synthetic-only Proof

- temporary_sqlite_only = yes
- logical_runtime_target_accessed = no
- repository_runtime_directory_created = no
- configured_store_accessed = no
- real_candidate_values_used = no
- real_payload_created = no
- package_or_row_read = no
- physical_runtime_database_resolved = no
- physical_runtime_database_opened = no
- physical_runtime_database_initialized = no
- environment_enablement_used = no
- network_called = no
- provider_called = no
- collector_called = no
- real_llm_called = no

The repaired persistence capability remains local, internal, nonproduction, disabled by default, synthetic-only, and validated only against temporary SQLite targets.

## Preserved Boundaries

- execution_gate_activated = no
- execution_gate_activation_approval_received = no
- logical_runtime_target_accessed = no
- real_safe_payload_capture_ready = no
- human_gate_activation_decision_may_be_prepared_now = no
- gate_activation_ready = no
- actual_write_ready = no
- actual_evidence_layer_write_performed = no
- production_evidenceitem_creation_authorized = no
- production_evidenceitem_created = no
- production_case_changed = no
- production_analysis_run_created = no
- review_queue_runtime_used = no
- downstream_runtime_called = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- public_delivery_created = no
- automatic_trust_upgrade = no

## Known Limitations

- Real safe payload capture is not implemented.
- The logical runtime target was not exercised and is not ready.
- No real activation decision was created.
- Post-commit revocation persistence remains unimplemented and unavailable.
- No route, API, CLI, frontend, provider, or collector integration exists.
- No production `EvidenceItem` exists.
- The repaired contract is validated only with synthetic fixtures and temporary SQLite.

## Not Run

- full pytest, because this was a narrow three-file repair and focused plus nearby results showed no cross-cutting failure
- frontend build and browser smoke, because no frontend or route changed
- real package or row readers
- real safe-payload capture
- logical runtime-target initialization or query
- configured external-store tests
- provider or collector jobs
- network, real API, or real LLM calls
- gate activation
- actual Evidence Layer write
- production object creation
- commit, push, or tag

## Git and Source Recommendation

- commit_recommended = yes after independent ChatGPT review
- recommended_commit_message = Repair 9A-23B synthetic persistence conformance
- recommended_tag = no
- project_source_update = yes after commit
- Canonical_00 = replace after commit
- Canonical_09 = replace after commit
- Canonical_03 = replace narrowly after commit because backend runtime, receipt, and attempt semantics changed
- Source_11 = no update

## Next Boundary

- next_default = pause
- next_recommended_task = independent 9A-23B post-repair conformance audit against the committed 9A-23A contract
- real_payload_approval_phrase_created = no
- gate_activation_declaration_prepared = no
- actual_write_next = no
- production_evidenceitem_next = no
