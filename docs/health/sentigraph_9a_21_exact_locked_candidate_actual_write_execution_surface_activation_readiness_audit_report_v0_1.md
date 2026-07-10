# Sentigraph 9A-21 Exact Locked-candidate Actual Write Execution Surface Activation-readiness Audit Report v0.1

## Audit Metadata

- phase = 9A-21
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- read_only_repo_audit = yes
- package_or_row_read = no
- write_helper_called = no
- persistence_accessed = no
- gate_activated = no
- write_performed = no
- production_evidenceitem_created = no
- audit_task_complete = yes
- gate_activation_ready = no

`decision = ready` means this read-only audit is complete and evidence-backed. It does not mean the execution gate is ready for activation.

## Approval Validation

- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- approval_scope = repository-code-history-read-only activation-readiness audit and two docs only

Exact audit approval phrase:

`APPROVE_9A_21_EXACT_LOCKED_CANDIDATE_ACTUAL_WRITE_EXECUTION_SURFACE_AND_ACTIVATION_READINESS_AUDIT_DOCS_ONLY`

The phrase authorizes only inspection and documentation. It is not gate activation approval, write execution approval, production EvidenceItem authorization, or permission to read the real package or row.

## Committed Anchor

- expected_branch = main
- observed_branch = main
- expected_commit = 2d34a21
- observed_commit = 2d34a21cd38766da678d58985af4d6afbf8775d1
- observed_commit_message = Establish 9A-20 exact candidate write execution gate contract
- origin_main_commit = 2d34a21cd38766da678d58985af4d6afbf8775d1
- worktree_started_clean = yes
- origin_alignment = exact

## Immutable Identity Verification

The following indivisible governance key matched the committed 9A-16C, 9A-19, and 9A-20 safe records without reopening package or row content:

- approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016
- approved_package_role = candidate_demo_sample
- approved_case_id_hint = donglu_sunjihai_youth_football_202606
- approved_row_source = evidence_items.jsonl
- selected_preview_row_opaque_id = preview-row-001
- selected_preview_row_safe_hash = ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391
- final_candidate_id = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- final_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- final_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- identity_schema = sentigraph_one_real_source_locked_candidate_identity_v0_1
- identity_version = 0.1
- hash_algorithm = sha256
- hash_input_scope = versioned_safe_canonical_projection_only
- candidate_lock_status = locked_for_single_candidate_governance_review_only
- immutable_identity_exact_match = yes

Scope remains exactly one candidate. The whole package and other rows are not approved; candidate, package, row, role, row-source, schema, ID, and hash substitution remain forbidden.

## Preserved Governance State

9A-19 remains unchanged:

- human_final_write_authorization_decision_received = yes
- human_final_write_authorization_decision = approved
- human_final_write_authorization_performed = yes
- final_write_authorization_scope = exact_locked_candidate_only
- candidate_authorized_for_future_separately_gated_evidence_layer_write = yes

9A-20 remains unchanged and inactive:

- execution_gate_establishment_authorization_recorded = yes
- execution_gate_contract_established = yes
- execution_gate_status = defined_but_inactive_pending_separate_execution_approval
- execution_gate_activated = no
- execution_gate_activation_approval_received = no
- actual_write_execution_approval_received = no
- actual_write_execution_authorized_now = no
- actual_write_authorized = false
- actual_evidence_layer_write_performed = no
- persisted_evidence_layer_record_created = no
- ready_for_actual_write = false
- production_evidenceitem_creation_authorized = false
- production_evidenceitem_created = no

## Audit Summary Fields

- exact_execution_surface_identified = yes
- exact_execution_surface_classification = existing_but_non_persistent
- exact_input_schema_identified = yes
- exact_locked_candidate_input_available_from_safe_committed_records = no
- persistence_target_identified = no
- persisted_result_schema_identified = no
- mutation_semantics_identified = yes
- duplicate_idempotency_behavior_identified = no
- bounded_attempt_retry_behavior_identified = no
- partial_failure_behavior_identified = no
- rollback_compensation_behavior_identified = no
- post_write_verification_plan_supported_by_existing_repo = no
- activation_readiness_outcome = not_ready_due_to_nonpersistent_or_test_only_surface

An exact helper candidate is identifiable, but it is not an actual persistence surface and is not connected to the separately existing case-store persistence chain.

## Files and Symbols Inspected

Current committed source-of-truth files:

- `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py`
  - `build_controlled_evidenceitem_evidence_layer_write_runtime`
  - `create_controlled_evidenceitem_evidence_layer_write_runtime`
  - `build_safe_controlled_evidenceitem_evidence_layer_write_runtime_summary`
  - `_base_output`, `_write_result`, `_approval_blockers`, `_build_controlled_items`
- `backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py`
- `backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py`
  - `_build_8y14_smoke`, a test-only wrapper
- `backend/app/services/controlled_evidence_layer_write_candidate_from_production_import_candidate.py`
- `backend/app/services/evidence_layer_one_real_candidate_pre_write_review.py`
- `backend/app/services/evidence_layer_one_real_locked_candidate_pre_write_review.py`
  - `build_safe_locked_candidate_identity`
  - `build_safe_locked_candidate_identity_capture_marker`
- `backend/app/services/controlled_production_case_candidate.py`
- `backend/app/services/evidence_import.py`
- `backend/app/services/evidence_ingestion.py`
- `backend/app/services/case_store.py`
  - `attach_case_evidence`, `commit_case_evidence_import`
- `backend/app/repositories/case_repository.py`
  - `CaseRepository.save_case_evidence`
- `backend/app/services/storage/base_store.py`
- `backend/app/services/storage/local_json_store.py`
  - `LocalJsonCaseStore.update_case`, `LocalJsonCaseStore._write_data`
- `backend/app/services/storage/mongodb_store.py`
  - `MongoDbCaseStore.update_case`
- `backend/app/services/storage/store_factory.py`
- `backend/app/api/v1/routes/cases.py`
- `backend/app/schemas/evidence.py`
  - `EvidenceItem`, `EvidenceIngestionBatch`, `EvidenceImportCommitResult`
- `backend/app/tests/test_evidence_ingestion.py`
- `backend/app/tests/test_evidence_import.py`
- `backend/app/tests/test_local_json_case_store.py`
- committed 9A-16C, 9A-19, and 9A-20 governance documents

Historical locators used read-only:

- `98004770e5a76eb822ee56372b4d957b32057507` - initial 8W-28 controlled runtime
- `47ba96a67220581c1fa4a6a574a7ccbdebfad7c8` - current ASCII guard repair lineage
- `3b7b8510dcfacb1f09d582101f894aec702af6b0` - 8Y-14 test-path smoke lineage

Current main code and current committed contracts, not historical wording, determine every conclusion below.

## Execution-surface Inventory

| Surface | Path and symbol | Current status | Mutation or persistence | Audit classification |
|---|---|---|---|---|
| Controlled EvidenceItem-shaped builder | `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py:252` `build_controlled_evidenceitem_evidence_layer_write_runtime` | Production-directory internal helper; referenced for invocation only by tests | Builds and returns dictionaries in memory; no file, store, database, route, or repository call | `existing_but_non_persistent` |
| Controlled runtime alias | Same file, `create_controlled_evidenceitem_evidence_layer_write_runtime` | Alias of the same builder | Same pure in-memory behavior | `existing_but_non_persistent` |
| Controlled summary builder | Same file, `build_safe_controlled_evidenceitem_evidence_layer_write_runtime_summary` | Internal helper | Calls the in-memory builder and returns minimized counts/boundaries | `existing_but_non_persistent` |
| 8Y-14 wrapper | `backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py:173` `_build_8y14_smoke` | Test-only | Calls the controlled builder; explicitly reports no persisted record | `existing_but_test_semantics_only` |
| Production-import-derived candidate builder | `backend/app/services/controlled_evidence_layer_write_candidate_from_production_import_candidate.py` | Internal candidate builder | Produces candidate dictionaries only | `pure_builder` |
| Real-row candidate-chain builder | `backend/app/services/evidence_layer_one_real_candidate_pre_write_review.py:354-454` | Internal no-write review chain | Full candidate exists transiently only after row-preview input; no persistence | `existing_but_non_persistent` and prohibited for this audit |
| Locked identity projection | `backend/app/services/evidence_layer_one_real_locked_candidate_pre_write_review.py:242` | Internal safe summary helper | Keeps identity fields only; intentionally excludes candidate payload | `pure_builder` |
| Controlled production-case candidate | `backend/app/services/controlled_production_case_candidate.py` | Internal downstream candidate builder | Consumes controlled runtime-shaped data but creates no case and persists nothing | `pure_builder` |
| Manual Evidence ingestion | `backend/app/services/case_store.py:385` `attach_case_evidence`; route `backend/app/api/v1/routes/cases.py:194` | Non-test API/service path | Converts `EvidenceIngestionBatch` to `EvidenceItem`, merges, and replaces case evidence through `CaseRepository` | Existing persistence path, but incompatible and not bound to the locked candidate or gate |
| Evidence import commit | `backend/app/services/case_store.py:509` `commit_case_evidence_import`; route `backend/app/api/v1/routes/cases.py:256` | Non-test API/service path | Parses upload content, builds `EvidenceItem` objects, merges, and replaces case evidence | Existing persistence path, but prohibited input mode and not candidate/gate bound |
| Case persistence facade | `backend/app/repositories/case_repository.py:99` `save_case_evidence` | Production code | Replaces an analysis case's entire `evidence_items` list through configured `CaseStore` | Real case mutation surface, not an exact candidate adapter |
| Local JSON case store | `backend/app/services/storage/local_json_store.py:52,231` | Default configured store by code | Whole-case replace via temporary file and filesystem replace | Governed generic case persistence, not selected for 9A-20 |
| MongoDB case store | `backend/app/services/storage/mongodb_store.py:100` | Optional configured store | Whole-document `replace_one`, no upsert on update | Governed generic case persistence, not selected for 9A-20 |

No CLI, route, API, non-test orchestration function, or store adapter invokes the controlled 8W-28 builder. `git grep` found its calls only in tests. Schema-string consumption by the controlled production-case candidate does not invoke or persist the runtime.

## Strongest Surface Candidate

- strongest_surface_path = backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py
- strongest_surface_symbol = build_controlled_evidenceitem_evidence_layer_write_runtime
- surface_visibility = internal_local_helper
- production_directory_code = yes
- non_test_production_caller_exists = no
- route_or_cli_exists = no
- mutation_performed = no
- persistence_performed = no
- output_kind = controlled EvidenceItem-shaped in-memory dictionaries
- classification = existing_but_non_persistent
- selected_for_activation = no

This is the strongest candidate because its accepted set schema matches the final-candidate set schema and its name and result flags model a controlled write. Its own docstring, boundary fields, imports, call graph, tests, and 8W-28 report all constrain it to local helper/test-path semantics.

## Input and Schema Assessment

- expected_input_python_type = dict[str, Any] or None
- required_set_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- required_item_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1
- locked_governance_schema_string_compatible = yes
- full_input_mapping_available_in_committed_safe_records = no
- exact_locked_candidate_representable_from_identity_only = no
- raw_row_text_required_by_helper_type = no
- full_safe_candidate_payload_required = yes
- unavailable_required_fields_include = lineage source IDs, evidence_id_hash, and text_snippet_redacted
- existing_reconstruction_path = real-row candidate chain only
- reconstruction_without_package_or_row_read = no
- transformation_selected_or_executed = no

The 9A-16C record deliberately retains only a safe identity projection. It excludes preview text, candidate payloads, source URLs, paths, and raw content. Searching the committed `backend/app` and governance-doc scope found the exact final candidate ID only in governance records, not in a persisted full candidate object.

## Persistence Truth

- strongest_surface_persistence_target_kind = none
- persistence_target_path_or_store_label = none_for_controlled_8w28_helper
- persistence_target_selected_for_activation = no
- persistence_target_exists = no for the strongest surface
- persistence_target_is_governed = unknown because no target is bound
- persistence_target_is_production = no
- actual_configured_case_store_inspected = no

The repository separately supports generic case persistence. Code defaults to logical repository-relative label `backend/data/cases.json`, with optional configured MongoDB. Neither target is connected to the controlled runtime or selected by 9A-20. The current configured target was intentionally not inspected because environment state is outside this audit.

## Result and Schema Assessment

- runtime_schema = sentigraph_controlled_evidenceitem_evidence_layer_write_runtime_v0_1
- write_result_schema = sentigraph_controlled_evidence_layer_write_result_v0_1
- controlled_item_schema = sentigraph_controlled_evidence_item_v0_1
- result_type = plain dictionary
- evidenceitem_shaped_result_produced = yes
- pydantic_evidence_item_produced = no
- persisted_record_identifier_present = no
- persistence_proof_present = no
- persisted_result_schema_identified = no
- controlled_created_flags_mean_persistence = no

`controlled_evidenceitem_created`, `evidence_item_created`, and `evidence_layer_write` are true only on the helper's successful in-memory path. `evidence_layer_write_scope` explicitly limits them to `controlled_local_helper_test_path_only`; every runtime side-effect flag remains false.

## Mutation Semantics

- strongest_surface_operation_semantics = pure_builder
- in_memory_object_returned = yes
- external_state_mutated = no
- exactly_one_persistent_mutation_guaranteed = no
- generic_case_store_semantics = whole_case_replace
- generic_local_json_write_shape = temp_file_then_replace
- generic_mongodb_write_shape = replace_one_no_upsert_for_update
- generic_case_store_bound_to_gate = no

The controlled helper validates and constructs data in process. The generic case-store chain has real mutation semantics, but no adapter, approval binding, or exact-candidate contract connects it to this gate.

## Duplicate and Idempotency Assessment

- controlled_helper_duplicate_lookup = missing
- controlled_helper_candidate_id_uniqueness_check = missing
- controlled_helper_safe_hash_uniqueness_check = missing
- controlled_helper_already_persisted_check = missing
- controlled_helper_idempotency_key = missing
- controlled_helper_compare_and_set_or_transaction_guard = missing
- controlled_helper_second_call_test = missing
- deterministic_controlled_item_ids = yes
- deterministic_ids_prove_idempotency = no
- duplicate_idempotency_behavior_identified = no

Generic ingestion performs in-memory normalized-content-hash deduplication before whole-case replacement. That behavior is not connected to the locked candidate schema, has no gate-bound idempotency key or storage uniqueness constraint, and does not make the controlled helper idempotent.

## Attempts and Retry Assessment

- maximum_execution_attempt_count_defined = no
- retry_allowed_or_forbidden_defined = no
- second_invocation_behavior_defined = no
- partial_retry_behavior_defined = no
- repair_write_behavior_defined = no
- duplicate_creation_prevention_for_gate_defined = no
- hard_candidate_bound = 10
- hard_candidate_bound_is_attempt_limit = no
- bounded_attempt_retry_behavior_identified = no

`candidate_limit` and `HARD_CANDIDATE_BOUND` constrain item count, not invocation count. 9A-20 correctly requires a later explicit attempt and retry policy; current code does not supply one.

## Partial Failure and Atomicity Assessment

- controlled_helper_persistent_partial_failure_possible = no because no persistence exists
- controlled_helper_validation_before_output = yes
- actual_write_atomicity_defined = no
- actual_write_partial_failure_behavior_defined = no
- partial_failure_tests_for_controlled_actual_write = missing
- generic_local_json_atomicity_signal = temporary file followed by replace under process lock
- generic_mongodb_atomicity_signal = single-document replace
- generic_store_atomicity_bound_to_gate = no

The pure builder cannot leave partial persisted state. That fact does not establish atomicity or partial-failure behavior for a future actual write, because no such surface is connected.

## Rollback and Revocation Assessment

- controlled_helper_rollback_code_exists = no
- controlled_helper_compensating_action_exists = no
- controlled_helper_persisted_state_can_be_revoked = not_applicable because no state is persisted
- governance_revocation_exists = yes
- governance_rollback_action = discard in-memory candidate, identity, or audit state and pause
- generic_case_evidence_rollback_exists = no
- rollback_tested_for_gate = no
- pre_execution_revocation_bound_to_helper = no
- failed_write_distinguishable_from_successful_persisted_write = no actual persisted write surface exists
- rollback_compensation_behavior_identified = no

`CaseStore.reset` clears a store for tests or explicit local cleanup; it is not a candidate-specific rollback and is not suitable evidence of rollback readiness.

## Post-write Verification Assessment

- exactly_one_mutation_proof_supported = no
- persisted_record_readback_proof_supported_for_controlled_helper = no
- no_unrelated_record_changed_proof_supported = no
- duplicate_not_created_proof_supported = no
- downstream_nonexecution_flags_present = yes for the in-memory helper only
- rollback_availability_proof_supported = no
- post_write_verification_plan_supported_by_existing_repo = no

Generic local-store tests prove that generic cases can be reloaded from temporary test storage. They do not prove a locked-candidate write, mutation count, isolation, idempotency, or rollback. Store update methods return a copy of the submitted case rather than a dedicated persisted Evidence Layer receipt.

## Approval and Guard Consistency

- current_helper_guard_phrase = APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION
- helper_guard_is_ascii = yes
- missing_or_wrong_phrase_blocks = yes
- old_chinese_phrase_accepted = no
- historical_mojibake_variants_accepted = no
- multiple_helper_phrase_variants_accepted = no
- 8y14_outer_guard_exists = yes, test-only
- current_guard_protects_true_persistence = no
- separate_gate_activation_guard_exists = no
- activation_approval_bound_to_immutable_candidate = no
- current_9a20_phrase_can_activate_helper = no

The current exact guard protects construction of a local/test-path result. It does not check 9A-19, 9A-20, the locked identity hashes, an activation decision, a persistence target, or an attempt count.

## Production-boundary Classification

- primary_classification = controlled_local_write_semantics_only
- controlled_local_evidenceitem_shaped_result = yes
- persisted_nonproduction_governed_record = no
- production_evidenceitem = no
- production_review_queue_item = no
- production_case_or_analysis_run = no
- downstream_runtime_permission = no

The generic case routes can persist standard `EvidenceItem` objects inside a case, but they are separate broad application paths and are not proof that this controlled candidate is eligible for or connected to that behavior.

## Evidence Table

| Repository evidence | What it proves | What it does not prove |
|---|---|---|
| `backend/app/services/controlled_evidenceitem_evidence_layer_write_runtime.py:252-303` | Exact helper signature, schema validation flow, and in-memory output construction | Persistence, activation binding, or exactly-one mutation |
| Same file `:363-483` | Plain dict output, local/test scope, false side-effect map | Persisted-record receipt or store target |
| Same file `:486-491` | One exact current ASCII helper guard | Human activation approval or candidate-hash binding |
| Same file `:598-764` | Deterministic controlled-item mapping and safe fields | Full locked candidate availability, duplicate lookup, or persistence |
| `backend/app/tests/test_controlled_evidenceitem_evidence_layer_write_runtime.py:289-456` | Current schemas, boundary flags, guard rejection, and no downstream calls | Non-test invocation or persistence |
| Same test `:573-674` | Candidate-count bound and no file opens | Attempt bound, retry policy, or second-call idempotency |
| `backend/app/tests/test_8y_14_controlled_evidenceitem_write_runtime_smoke_after_reroute_and_phrase_repair.py:173-214` | Test-only outer guard and explicit `persisted_evidence_layer_record_created = False` | Runtime activation or production orchestration |
| `backend/app/services/evidence_layer_one_real_candidate_pre_write_review.py:354-454` | Full candidate chain can be rebuilt after row preview | Safe reconstruction from committed identity without row access |
| `backend/app/services/evidence_layer_one_real_locked_candidate_pre_write_review.py:242-310` | Safe identity and marker are intentionally minimized | Full candidate object or input payload persistence |
| `backend/app/services/case_store.py:385-430` | Manual Evidence ingestion merges and calls case persistence | Compatibility with the controlled candidate or activation guard |
| `backend/app/services/case_store.py:509-561` | Import commit parses content, deduplicates, and persists case evidence | Permitted no-row-read activation surface |
| `backend/app/repositories/case_repository.py:99-122` | Case evidence list is replaced through the configured store | Standalone Evidence Layer record, mutation receipt, or rollback |
| `backend/app/services/storage/local_json_store.py:52-59,231-237` | Whole-case JSON replacement through a temporary file | Gate binding, record-level transaction, or candidate rollback |
| `backend/app/services/storage/mongodb_store.py:100-104` | Whole-case document replacement | Gate binding, CAS, idempotency key, or candidate rollback |
| `backend/app/tests/test_local_json_case_store.py:14-33` | Generic case reload works in temporary test storage | Locked-candidate persistence or exactly-one write proof |
| `docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md:103-144` | Safe hashes exclude row text and full candidate payload | Reconstructible helper input |
| `docs/architecture/sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1.md:129-261` | 9A-20 requires target, idempotency, attempts, failure, rollback, and receipt facts | Satisfaction of those requirements |

## Unknowns and Gaps

- No persisted full candidate object is available in the inspected committed safe scope.
- The current configured case-store backend is intentionally unknown; environment state was not inspected.
- No adapter maps the controlled item dictionary to `EvidenceItem` and `CaseRepository.save_case_evidence`.
- No governed persistence target or persisted result schema is selected for the gate.
- No standalone Evidence Layer record model or receipt proves persistence.
- No activation guard is bound to the immutable identity.
- No duplicate lookup, idempotency key, storage uniqueness constraint, or second-call contract exists for the controlled helper.
- No execution attempt maximum, retry, repair-write, or second-write policy exists.
- No actual-write partial-failure, rollback, compensating-action, or exactly-one-mutation verification path exists.
- No post-write receipt can prove isolation from unrelated case or downstream state.

Unknowns remain unknown and are not treated as passes.

## Activation-readiness Outcome

- activation_readiness_outcome = not_ready_due_to_nonpersistent_or_test_only_surface
- human_gate_activation_decision_may_be_prepared_now = no
- workflow_disposition = pause
- fresh_governance_required_if_identity_changes = yes
- selected_next_boundary = pause_due_to_nonpersistent_test_only_surface

The strongest candidate surface is clear enough to audit but is not a persistent execution surface. The generic persistence chain is real but incompatible, unbound, and broader than the locked-candidate gate. Activation preparation must therefore remain paused.

## Privacy and No-real-data Confirmation

- approved_package_directory_inspected = no
- package_file_statted_or_enumerated = no
- evidence_items_jsonl_read = no
- evidence_items_csv_read = no
- source_manifest_rows_read = no
- collection_log_rows_read = no
- ignored_runtime_data_read = no
- private_collector_inspected = no
- configured_export_root_inspected = no
- database_or_persistence_file_accessed = no
- environment_secret_or_value_read = no
- raw_row_or_comment_exposed = no
- raw_author_identifier_exposed = no
- real_person_pii_exposed = no

Only committed source code, tests, governance documentation, and Git metadata were inspected.

## No-side-effect Confirmation

- helper_imported_or_called = no
- persistence_instantiated_or_accessed = no
- backend_code_changed = no
- backend_tests_changed = no
- frontend_changed = no
- route_or_schema_changed = no
- runtime_changed = no
- gate_activated = no
- actual_write_execution_approved = no
- actual_write_execution_performed = no
- persisted_evidence_layer_record_created = no
- production_evidenceitem_creation_authorized = no
- production_evidenceitem_created = no
- production_review_queue_item_created = no
- production_case_created = no
- production_analysis_run_created = no
- production_analysis_result_created = no
- source11_or_finalsummaryreport_runtime_called = no
- report_export_public_or_delivery_runtime_used = no
- provider_or_collector_called = no
- real_api_or_llm_called = no
- url_fetch_or_scrape = no
