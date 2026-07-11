# Sentigraph MVP-F05 Exact Logical Nonproduction Persistence Target Authorization Contract v1.0

## 1. Contract Identity

- milestone_id = MVP-F05
- prompt_package_id = MVP-F05-P1
- baseline_version = 1.0
- baseline_task_classification = planned_fixed_milestone
- contract_schema = sentigraph_exact_logical_nonproduction_persistence_target_authorization_contract_v1_0
- contract_version = 1.0
- contract_id = sentigraph-mvp-f05-exact-logical-nonproduction-target-authorization-v1-0
- contract_mode = docs_only_exact_logical_target_authorization
- target_authorization_contract_lock_status = locked_for_MVP_F06_initialization_eligibility_only

This contract selects one logical nonproduction persistence target and makes it
the sole candidate for a future, separately approved initialization smoke. It
does not inspect, open, create, initialize, migrate, or modify that target.

## 2. Exact Approval and Current Boundary

The exact approval received for MVP-F05-P1 was:

APPROVE_SENTIGRAPH_MVP_F05_EXACT_LOGICAL_NONPRODUCTION_PERSISTENCE_TARGET_AUTHORIZATION_CONTRACT_DOCS_ONLY_NO_TARGET_ACCESS_NO_INITIALIZATION

The approval permits tracked-repository evidence review and exactly this
contract plus its companion planning decision. It is not target-access,
target-initialization, SQLite, gate-activation, persistence, actual-write, or
production authorization.

Current no-side-effect state:

- docs_only = yes
- target_accessed = no
- runtime_enumerated = no
- SQLite_accessed = no
- SQLite_created = no
- SQLite_initialized = no
- schema_created = no
- table_created = no
- protected_payload_reread = no
- safe_receipt_reread = no
- source_or_package_reread = no
- gate_activated = no
- persistence_performed = no
- production_object_created = no

## 3. Committed Evidence Anchors

Only committed Git evidence was used. Protected artifacts, package rows,
runtime state, and the target itself were not inspected.

| Evidence | Commit | Contract role |
| --- | --- | --- |
| 9A-16C locked-candidate identity report | 11ae4bb33e1d45afc6153e4dd28be0e4b5178e34 | Authoritative locked-candidate schema and safe-hash governance reference |
| 9A-22 persistence prerequisite contract and decision | 1c853ae2563c5e4d000767e52a351660c3c0c43c | Logical target, owner surface, and nonproduction persistence boundary |
| 9A-23A exact-conformance repair contract | 162c3604efd6a270a62147f27bf67026181d12fa | Fail-closed mutation and reservation design |
| 9A-23B repaired service, tests, and health report | e3fb9f9249069fc72b23dd3bd5b6e197d1417f7c | Committed owner module, store class, writer, tables, and disabled-by-default implementation evidence |
| F02 capture contract and decision | 768cc4e70728f812d998d571c9821977c2bab1e0 | Safe-payload schema and bounded capture governance |
| C02-P2 remediation report | ba812561b20a86296d363e462930fc146865b56b | Accepted payload schema, version, and safe hash |
| First F04 report | e1d680c3b9a79633cc054a7e9c31502d7cc0f4e3 | Preserved historical needs-fix outcome |
| MVP-CHG-002 effective F04 report | e1d680c3b9a79633cc054a7e9c31502d7cc0f4e3 | Effective payload and receipt acceptance plus artifact byte-hash evidence |

The current Git anchor for this contract is
e1d680c3b9a79633cc054a7e9c31502d7cc0f4e3. The first F04 result remains
historically needs_fix; MVP-CHG-002 supplies the later effective acceptance
without reclassifying that first result.

## 4. Exactly One Selected Target

- target_scope = exactly_one_logical_nonproduction_persistence_target
- target_kind = dedicated_local_sqlite_nonproduction_store
- implementation_runtime = Python standard-library sqlite3
- logical_repository_relative_target_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- target_primary_table = governed_nonproduction_evidence_records_v0_1
- target_attempt_reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
- persistence_module = backend/app/services/governed_nonproduction_evidence_persistence.py
- store_class = GovernedNonproductionEvidencePersistenceStore
- public_writer = create_governed_nonproduction_evidence_record

No second target is selected. Temporary SQLite, an in-memory database,
LocalJsonCaseStore, CaseRepository, MongoDbCaseStore, generic case storage,
caller-supplied targets, environment overrides, alternate runtime files, and
production databases are excluded.

Target classification:

- target_environment = local
- target_classification = internal_governed_nonproduction_only
- production_target = no
- customer_target = no
- public_target = no
- generic_case_store = no
- route_exposed = no
- API_exposed = no
- CLI_exposed = no
- frontend_exposed = no
- provider_or_collector_target = no
- disabled_by_default = yes

## 5. Normative Target Identity

The identity object is complete, versioned, environment-independent, and
contains no physical path, drive, user name, filesystem status, or target
metadata.

Canonicalization:

- hash_algorithm = sha256
- text_encoding = UTF-8
- ensure_ascii = true
- object_keys = sorted
- separators = compact
- target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b

Normative target identity object:

~~~json
{
  "API_exposed": false,
  "CLI_exposed": false,
  "case_store_reuse_allowed": false,
  "customer_target": false,
  "disabled_by_default": true,
  "fallback_target_allowed": false,
  "frontend_exposed": false,
  "generic_case_store": false,
  "implementation_runtime": "Python standard-library sqlite3",
  "logical_repository_relative_target_label": "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3",
  "persistence_module": "backend/app/services/governed_nonproduction_evidence_persistence.py",
  "production_target": false,
  "provider_or_collector_target": false,
  "public_target": false,
  "public_writer": "create_governed_nonproduction_evidence_record",
  "route_exposed": false,
  "store_class": "GovernedNonproductionEvidencePersistenceStore",
  "target_attempt_reservation_table": "governed_nonproduction_evidence_persistence_attempt_reservations_v0_1",
  "target_classification": "internal_governed_nonproduction_only",
  "target_environment": "local",
  "target_identity_schema": "sentigraph_exact_logical_nonproduction_persistence_target_identity_v1_0",
  "target_identity_version": "1.0",
  "target_kind": "dedicated_local_sqlite_nonproduction_store",
  "target_lock_status": "locked_for_future_separately_gated_initialization_only",
  "target_primary_table": "governed_nonproduction_evidence_records_v0_1",
  "target_scope": "exactly_one_logical_nonproduction_persistence_target",
  "target_substitution_allowed": false
}
~~~

The safe hash is SHA-256 of the complete object above after the stated
canonicalization.

## 6. Authorization State

- target_authorization_contract_established = yes
- target_authorized_for_future_separately_gated_initialization = yes
- target_authorization_status = defined_but_inactive_pending_separate_MVP_F06_initialization_approval
- target_access_authorized_now = no
- target_inspection_authorized_now = no
- target_initialization_authorized_now = no
- SQLite_access_authorized_now = no
- schema_creation_authorized_now = no
- table_creation_authorized_now = no
- candidate_persistence_authorized_now = no
- attempt_reservation_authorized_now = no
- gate_activation_authorized_now = no
- actual_write_authorized_now = no
- production_object_creation_authorized_now = no
- MVP_F06_authorized = no
- MVP_F06_executed = no
- MVP_F07_authorized = no
- MVP_F07_executed = no
- MVP_F08_authorized = no
- MVP_F08_executed = no

Authorization establishes only future initialization eligibility for the exact
logical identity. It does not assert that the target exists, has been inspected,
is initialized, is ready, or may receive the accepted candidate.

## 7. Ownership and No-substitution Rules

Ownership is frozen:

- target_owner_module = backend/app/services/governed_nonproduction_evidence_persistence.py
- target_owner_class = GovernedNonproductionEvidencePersistenceStore
- target_writer_authority_model = source_inputs_revalidated_and_command_internally_rederived
- caller_supplied_command_is_write_authority = no
- caller_supplied_target_is_authority = no
- generic_repository_is_write_authority = no

Substitution is forbidden:

- target_substitution_allowed = no
- logical_label_substitution_allowed = no
- target_kind_substitution_allowed = no
- database_filename_substitution_allowed = no
- table_substitution_allowed = no
- store_class_substitution_allowed = no
- persistence_module_substitution_allowed = no
- temporary_target_substitution_allowed = no
- in_memory_target_substitution_allowed = no
- production_target_substitution_allowed = no
- fallback_target_allowed = no
- automatic_target_discovery_allowed = no
- environment_override_allowed = no
- caller_supplied_physical_path_allowed = no
- generic_case_store_reuse_allowed = no

Any mismatch requires:

- target_authorization_valid_for_attempt = no
- workflow_disposition = pause
- fresh_governance_required = yes

## 8. Accepted Candidate, Payload, and Receipt Binding

The binding uses committed safe evidence only:

- accepted_input_binding_complete = yes
- authoritative_locked_candidate_identity_report = docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md
- authoritative_locked_candidate_identity_commit = 11ae4bb33e1d45afc6153e4dd28be0e4b5178e34
- locked_candidate_identity_schema = sentigraph_one_real_source_locked_candidate_identity_v0_1
- locked_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- locked_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- accepted_candidate_count = 1
- accepted_payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
- accepted_payload_version = 0.1
- accepted_payload_safe_hash = 71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5
- accepted_payload_artifact_byte_sha256 = 64316f33d1673e67c9fd8b5286d1fa60af96f55a9b79e937915430aacec286e3
- accepted_receipt_artifact_byte_sha256 = dc7fea053636b561eed00bd3863f455559630aa39ab533aa3ae1a9136edaf6d8
- C02_P2_commit = ba812561b20a86296d363e462930fc146865b56b
- effective_F04_acceptance_commit = e1d680c3b9a79633cc054a7e9c31502d7cc0f4e3
- human_review_required = true
- automatic_trust_upgrade_allowed = false
- production_evidenceitem_created = false

The binding intentionally omits raw row content, source text, author identity,
network location, physical artifact location, absolute target location, and
protected artifact content.

## 9. Normative Authorization Contract Projection

The projection below is the complete hash input. Its own safe-hash field is the
only field excluded from the hash input.

~~~json
{
  "accepted_input_binding": {
    "accepted_candidate_count": 1,
    "accepted_input_binding_complete": true,
    "accepted_payload_artifact_byte_sha256": "64316f33d1673e67c9fd8b5286d1fa60af96f55a9b79e937915430aacec286e3",
    "accepted_payload_safe_hash": "71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5",
    "accepted_payload_schema": "sentigraph_exact_locked_candidate_safe_write_payload_v0_1",
    "accepted_payload_version": "0.1",
    "accepted_receipt_artifact_byte_sha256": "dc7fea053636b561eed00bd3863f455559630aa39ab533aa3ae1a9136edaf6d8",
    "automatic_trust_upgrade_allowed": false,
    "c02_p2_commit": "ba812561b20a86296d363e462930fc146865b56b",
    "c02_p2_report": "docs/health/sentigraph_mvp_c02_p2_independent_repaired_scanner_acceptance_and_bounded_remediation_capture_report_v1_0.md",
    "effective_f04_acceptance_commit": "e1d680c3b9a79633cc054a7e9c31502d7cc0f4e3",
    "effective_f04_acceptance_report": "docs/health/sentigraph_mvp_chg_002_f04_durable_receipt_auditor_and_exact_path_acceptance_recheck_report_v1_0.md",
    "human_review_required": true,
    "production_evidenceitem_created": false,
    "safe_payload_independently_accepted": true,
    "safe_receipt_independently_accepted": true
  },
  "allowed_future_milestone": "MVP-F06 Exact Logical Target Initialization Smoke",
  "atomicity_and_ambiguity_policy": {
    "ambiguous_create_or_commit_disposition": "pause_without_automatic_retry_or_fallback",
    "automatic_retry_allowed": false,
    "fallback_allowed": false,
    "overwrite_allowed": false,
    "rename_replacement_allowed": false,
    "target_substitution_allowed": false
  },
  "cleanup_policy": {
    "cleanup_authorized_now": false,
    "completed_or_ambiguous_target_action": "preserve_and_pause",
    "preexisting_target_deletion_allowed": false,
    "preexisting_target_migration_allowed": false,
    "same_run_new_target_removal_conditions": [
      "target_conclusively_absent_before_F06",
      "target_created_by_same_F06_run",
      "initialization_failed_before_declared_complete",
      "base_record_row_count_equals_zero",
      "attempt_reservation_row_count_equals_zero",
      "no_final_initialized_target_receipt_issued",
      "exact_cleanup_path_known_without_enumeration",
      "future_F06_approval_explicitly_permits_cleanup"
    ]
  },
  "contract_id": "sentigraph-mvp-f05-exact-logical-nonproduction-target-authorization-v1-0",
  "contract_lock_status": "locked_for_MVP_F06_initialization_eligibility_only",
  "contract_schema": "sentigraph_exact_logical_nonproduction_persistence_target_authorization_contract_v1_0",
  "contract_version": "1.0",
  "current_authorization_state": {
    "SQLite_access_authorized_now": false,
    "actual_write_authorized_now": false,
    "attempt_reservation_authorized_now": false,
    "candidate_persistence_authorized_now": false,
    "gate_activation_authorized_now": false,
    "production_object_creation_authorized_now": false,
    "schema_creation_authorized_now": false,
    "table_creation_authorized_now": false,
    "target_access_authorized_now": false,
    "target_authorization_contract_established": true,
    "target_authorization_status": "defined_but_inactive_pending_separate_MVP_F06_initialization_approval",
    "target_authorized_for_future_separately_gated_initialization": true,
    "target_initialization_authorized_now": false,
    "target_inspection_authorized_now": false
  },
  "existing_target_and_collision_policy": {
    "ambiguous_target_state_future_outcome": "pause_no_automatic_retry_no_fallback",
    "target_absent_future_outcome": "separately_approved_F06_may_create_exact_empty_target",
    "target_existence_status": "not_inspected",
    "target_exists_candidate_row_future_outcome": "pause_no_mutation_no_cleanup_fresh_governance",
    "target_exists_conforming_future_outcome": "read_only_schema_and_zero_row_verification_only",
    "target_exists_reservation_future_outcome": "pause_no_mutation_fresh_governance",
    "target_exists_schema_diff_future_outcome": "pause_no_migration_no_deletion_no_overwrite",
    "target_row_count_status": "not_inspected",
    "target_schema_status": "not_inspected"
  },
  "future_initialization_content_boundary": {
    "attempt_reservation_mutations_allowed": 0,
    "base_record_row_count_required": 0,
    "candidate_mutations_allowed": 0,
    "gate_activation_count_required": 0,
    "inserted_activation_decision_count": 0,
    "inserted_candidate_count": 0,
    "inserted_identity_count": 0,
    "inserted_payload_count": 0,
    "inserted_receipt_count": 0,
    "production_object_count_required": 0,
    "reservation_row_count_required": 0
  },
  "future_initialization_receipt_requirements": [
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "exact_logical_target_label",
    "target_preexistence_classification",
    "path_and_symlink_checks",
    "SQLite_open_or_create_count",
    "schema_table_and_index_verification",
    "base_record_row_count",
    "attempt_reservation_row_count",
    "target_initialization_outcome",
    "cleanup_performed",
    "no_payload_read",
    "no_candidate_mutation",
    "no_reservation_mutation",
    "no_gate_activation",
    "no_persistence",
    "no_production_object",
    "no_physical_absolute_path",
    "no_raw_or_protected_value"
  ],
  "initialization_prerequisites": {
    "exact_contract_hash_match_required": true,
    "exact_target_identity_hash_match_required": true,
    "generic_case_store_initialization_allowed": false,
    "protected_payload_or_receipt_read_allowed": false,
    "runtime_directory_enumeration_allowed": false,
    "separate_exact_human_approval_required": true,
    "target_attempt_reservation_count_must_equal_zero": true,
    "target_candidate_record_count_must_equal_zero": true
  },
  "locked_candidate_governance_reference": {
    "authoritative_identity_commit": "11ae4bb33e1d45afc6153e4dd28be0e4b5178e34",
    "authoritative_identity_report": "docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md",
    "final_candidate_safe_hash": "2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5",
    "final_candidate_schema": "sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1",
    "identity_schema": "sentigraph_one_real_source_locked_candidate_identity_v0_1",
    "locked_candidate_count": 1
  },
  "milestone_separation": {
    "F05": "contract_only",
    "F05_ready_implies_F06_authorized": false,
    "F06": "target_initialization_smoke",
    "F06_ready_implies_F07_authorized": false,
    "F07": "gate_activation_decision",
    "F07_ready_implies_F08_authorized": false,
    "F08": "single_persistence_execution",
    "F08_authorized_by_earlier_readiness_marker": false
  },
  "no_production_boundary": {
    "actual_write_authorized_now": false,
    "candidate_persistence_authorized_now": false,
    "gate_activation_authorized_now": false,
    "production_evidenceitem_creation_authorized_now": false,
    "production_object_creation_authorized_now": false,
    "target_initialization_authorized_now": false
  },
  "no_substitution_rules": {
    "automatic_target_discovery_allowed": false,
    "caller_supplied_physical_path_allowed": false,
    "database_filename_substitution_allowed": false,
    "environment_override_allowed": false,
    "fallback_target_allowed": false,
    "in_memory_target_substitution_allowed": false,
    "logical_label_substitution_allowed": false,
    "persistence_module_substitution_allowed": false,
    "production_target_substitution_allowed": false,
    "store_class_substitution_allowed": false,
    "table_substitution_allowed": false,
    "target_kind_substitution_allowed": false,
    "target_substitution_allowed": false,
    "temporary_target_substitution_allowed": false
  },
  "path_and_symlink_policy": {
    "UNC_substitution_allowed": false,
    "absolute_input_allowed": false,
    "caller_supplied_alternate_target_allowed": false,
    "drive_substitution_allowed": false,
    "exact_existing_component_symlink_or_reparse_escape_must_be_rejected": true,
    "fallback_path_allowed": false,
    "logical_target_must_derive_from_locked_identity": true,
    "parent_traversal_allowed": false,
    "path_escape_allowed": false,
    "runtime_directory_enumeration_allowed": false,
    "wildcard_or_latest_selection_allowed": false
  },
  "target_identity": {
    "API_exposed": false,
    "CLI_exposed": false,
    "case_store_reuse_allowed": false,
    "customer_target": false,
    "disabled_by_default": true,
    "fallback_target_allowed": false,
    "frontend_exposed": false,
    "generic_case_store": false,
    "implementation_runtime": "Python standard-library sqlite3",
    "logical_repository_relative_target_label": "runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3",
    "persistence_module": "backend/app/services/governed_nonproduction_evidence_persistence.py",
    "production_target": false,
    "provider_or_collector_target": false,
    "public_target": false,
    "public_writer": "create_governed_nonproduction_evidence_record",
    "route_exposed": false,
    "store_class": "GovernedNonproductionEvidencePersistenceStore",
    "target_attempt_reservation_table": "governed_nonproduction_evidence_persistence_attempt_reservations_v0_1",
    "target_classification": "internal_governed_nonproduction_only",
    "target_environment": "local",
    "target_identity_schema": "sentigraph_exact_logical_nonproduction_persistence_target_identity_v1_0",
    "target_identity_version": "1.0",
    "target_kind": "dedicated_local_sqlite_nonproduction_store",
    "target_lock_status": "locked_for_future_separately_gated_initialization_only",
    "target_primary_table": "governed_nonproduction_evidence_records_v0_1",
    "target_scope": "exactly_one_logical_nonproduction_persistence_target",
    "target_substitution_allowed": false
  },
  "target_identity_safe_hash": "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b",
  "target_ownership": {
    "caller_supplied_command_is_write_authority": false,
    "caller_supplied_target_is_authority": false,
    "generic_repository_is_write_authority": false,
    "public_writer": "create_governed_nonproduction_evidence_record",
    "target_owner_class": "GovernedNonproductionEvidencePersistenceStore",
    "target_owner_module": "backend/app/services/governed_nonproduction_evidence_persistence.py",
    "target_writer_authority_model": "source_inputs_revalidated_and_command_internally_rederived"
  }
}
~~~

- target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2

The contract safe hash is SHA-256 of the projection above after recursive key
sorting and compact UTF-8 JSON serialization with ensure_ascii=true.

## 10. Future MVP-F06 Boundary

MVP-F06 is named Exact Logical Target Initialization Smoke. It is not
authorized by this contract.

A separately approved F06 may only:

1. derive the exact logical target from the locked identity;
2. inspect the exact authorized target without scanning runtime;
3. validate path components and reject symlink or reparse-point escape;
4. classify the exact target as absent or existing;
5. create the exact empty SQLite target if conclusively absent, or verify it
   read-only if already exactly conforming;
6. create or verify only committed tables and indexes;
7. prove zero candidate records and zero attempt reservations;
8. issue a safe initialization receipt containing no physical path or protected
   value.

F06 may not read the payload, receipt, source, package, or candidate; create a
candidate or reservation; activate a gate; perform persistence; use a generic
case store; discover or substitute a target; or create a production object.

F06 requires a new exact human approval. This contract does not supply or
generate that future approval text.

## 11. Future Path, Symlink, and Escape Policy

Future F06 must:

- derive the logical label from the locked target identity;
- reject parent traversal, absolute input, drive substitution, UNC
  substitution, and repository escape;
- check each exact existing component for symlink or reparse-point escape;
- avoid directory enumeration, wildcards, and latest-file selection;
- reject caller-supplied alternate targets;
- preserve every pre-existing file;
- stop on ambiguous identity or state;
- use no fallback path.

This policy is prospective. F05 did not perform any path or filesystem check.

## 12. Existing-target and Collision Policy

- target_existence_status = not_inspected
- target_schema_status = not_inspected
- target_row_count_status = not_inspected

Future outcomes:

| Future F06 observation | Required disposition |
| --- | --- |
| Exact target absent | A separately approved F06 may create only the exact empty target |
| Exact target exists and conforms | Read-only schema and zero-row verification only |
| Schema differs | Pause; no migration, deletion, overwrite, or repair |
| Any candidate row exists | Pause; no mutation or cleanup; fresh governance required |
| Any attempt reservation exists | Pause; no mutation; fresh governance required |
| State is ambiguous | Pause; no automatic retry or fallback |

No current existence, schema, or row-count claim is made.

## 13. Future Initialization Content Boundary

Future F06 is schema-only:

- candidate_mutations_allowed = 0
- attempt_reservation_mutations_allowed = 0
- base_record_row_count = 0
- attempt_reservation_row_count = 0
- production_object_count = 0
- gate_activation_count = 0
- payload_insert_count = 0
- receipt_insert_count = 0
- candidate_insert_count = 0
- identity_insert_count = 0
- activation_decision_insert_count = 0

## 14. Failure, Ambiguity, and Cleanup

Future F06 must allow no automatic retry after ambiguous SQLite creation or
commit. It may not migrate, repair, delete, overwrite, rename, or substitute a
pre-existing target.

A newly created same-run target may be removed only when every condition below
is conclusive:

1. the exact target did not exist before F06;
2. that F06 run created it;
3. initialization failed before completion;
4. it contains zero candidate records;
5. it contains zero attempt reservations;
6. no final initialized-target receipt was issued;
7. the exact cleanup location is known without enumeration;
8. the separate F06 approval explicitly permits cleanup.

Ambiguous or completed targets must be preserved and paused. F05 performs no
cleanup.

## 15. Future Initialization Receipt

A future F06 safe receipt must contain:

- target identity safe hash;
- target authorization contract safe hash;
- exact logical target label;
- pre-existence classification;
- path and symlink check results;
- SQLite open or create count;
- schema, table, and index verification;
- base-record and attempt-reservation row counts;
- initialization outcome;
- cleanup-performed status;
- explicit no-payload-read, no-candidate-mutation, no-reservation-mutation,
  no-gate-activation, no-persistence, and no-production-object fields.

It must contain no absolute physical location, raw value, or protected value.
No F06 receipt is created by F05.

## 16. Milestone Separation

- F05 = contract_only
- F06 = target_initialization_smoke
- F07 = gate_activation_decision
- F08 = single_persistence_execution
- F05_ready_does_not_imply_F06_authorized = yes
- F06_ready_does_not_imply_F07_authorized = yes
- F07_ready_does_not_imply_F08_authorized = yes
- F08_authorized_by_earlier_readiness_marker = no
- MVP_F06_authorized = no
- MVP_F07_authorized = no
- MVP_F08_authorized = no

No milestone silently consumes the authority of the next milestone.

## 17. Prompt Accounting

- fixed_prompt_budget = 20
- conditional_prompt_allowance = 10
- risk_buffer_prompt_allowance = 4
- consumed_engineering_prompts_since_baseline = 9
- consumed_fixed_prompts = 5
- consumed_conditional_prompts = 2
- consumed_risk_prompts = 2
- remaining_fixed_prompts = 15
- remaining_conditional_allowance = 8
- remaining_risk_buffer = 2
- MVP_C02_prompt_allowance_remaining = 0
- MVP_C01_trigger_eligible = yes
- MVP_C01_authorized = no
- MVP_C01_consumed = no

The fixed MVP-F05 Prompt is consumed by Goal activation regardless of final
decision or commit outcome.

## 18. Historical State Preservation

- historical_MVP_F03_status = privacy_issue_stop
- historical_MVP_F03_completed = no
- historical_MVP_F03_reclassified = no
- MVP_C02_P1_status = needs_fix_prior_semantics_unavailable
- MVP_C02_P2_status = completed
- historical_first_MVP_F04_status = needs_fix
- historical_first_MVP_F04_completed = no
- historical_first_MVP_F04_reclassified = no
- MVP_CHG_002_status = completed
- effective_F04_status = completed_via_MVP_CHG_002_recheck

## 19. Contract Completion Criteria

The contract is complete only when:

- exactly one target identity is present;
- identity and contract hashes reproduce from the normative JSON;
- owner module, store class, and writer match committed evidence;
- candidate, payload, and receipt bindings use committed safe evidence only;
- substitution and generic-store reuse are forbidden;
- existence remains not inspected;
- future F06 path, collision, zero-row, failure, cleanup, and receipt boundaries
  are explicit;
- F06, F07, and F08 remain separately governed;
- no target, runtime, SQLite, source, protected artifact, gate, persistence, or
  production access occurs.

When these criteria hold, the target is authorized only for a future,
separately gated initialization smoke and remains inactive.
