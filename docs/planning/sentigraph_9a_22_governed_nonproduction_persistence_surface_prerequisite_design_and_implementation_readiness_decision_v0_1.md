# Sentigraph 9A-22 Governed Nonproduction Persistence Surface Prerequisite Design and Implementation-readiness Decision v0.1

## Decision

- phase = 9A-22
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- implementation_performed = no
- persistence_accessed = no
- gate_activated = no
- write_performed = no
- production_evidenceitem_created = no
- implementation_readiness_outcome = ready_for_separate_narrow_nonproduction_persistence_implementation_authorization
- gate_activation_ready = no
- human_gate_activation_decision_may_be_prepared_now = no
- actual_write_ready = no
- production_evidenceitem_creation_authorized = no

`decision = ready` means the architecture design task is complete. It does not authorize implementation, activation, persistence, actual write, or production `EvidenceItem` creation.

## Approval Validation

- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- approval_scope = docs-only prerequisite architecture design and implementation-readiness decision

Validated phrase:

`APPROVE_9A_22_GOVERNED_NONPRODUCTION_PERSISTENCE_SURFACE_PREREQUISITE_DESIGN_AND_IMPLEMENTATION_READINESS_DECISION_DOCS_ONLY`

This phrase is not an implementation approval, activation approval, execution approval, or production-object authorization.

## Committed Anchor

- expected_branch = main
- observed_branch = main
- expected_commit = 20cfe59
- observed_commit = 20cfe59498ee9967376f24dc291024032ca85f7b
- observed_commit_message = Audit 9A-21 exact candidate write activation readiness
- origin_main_commit = 20cfe59498ee9967376f24dc291024032ca85f7b
- worktree_started_clean = yes
- origin_alignment = exact

## Exact Candidate Binding

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
- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no

The design neither reclassifies `candidate_demo_sample` nor broadens scope beyond this one exact locked candidate.

## Preserved 9A-19, 9A-20, and 9A-21 State

9A-19 remains preserved:

- human_final_write_authorization_decision_received = yes
- human_final_write_authorization_decision = approved
- human_final_write_authorization_performed = yes
- final_write_authorization_scope = exact_locked_candidate_only
- candidate_authorized_for_future_separately_gated_evidence_layer_write = yes

9A-20 remains established and inactive:

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

9A-21 remains the current activation-readiness result:

- audit_task_complete = yes
- exact_execution_surface_classification = existing_but_non_persistent
- activation_readiness_outcome = not_ready_due_to_nonpersistent_or_test_only_surface
- gate_activation_ready = no
- workflow_disposition = pause

## 9A-21 Blocker Summary

9A-21 found an in-memory controlled builder but no governed persistence surface. The committed safe identity does not retain the full adapter input. The repository had no selected target, persisted record schema, receipt, candidate-to-store adapter, activation binding, idempotency key, uniqueness guard, bounded attempt policy, write atomicity, rollback/revocation mechanism, or post-write isolation proof.

The generic case-store chain was not suitable because it is broader, whole-case-oriented, configurable to production-capable stores, and not bound to this candidate or gate.

## Repository Evidence Inspected

Read-only inspection confirmed:

- `runtime/` is ignored by `.gitignore`;
- Python 3.10 provides standard-library `sqlite3` with no new package dependency;
- the repository has no active SQLite implementation in backend code;
- current requirements do not add a SQLite package;
- the strongest controlled helper returns dictionaries in memory and has no non-test caller;
- generic local JSON and MongoDB stores mutate whole case records and have no exact-candidate adapter;
- current controlled candidate validators use a strict safe-field model and bounded redacted snippets;
- no current route or CLI is appropriate for the prerequisite surface.

No runtime directory, configured store, database, package, row, or real payload was opened.

## Selected Architecture

- selected_architecture = dedicated_disabled_by_default_local_sqlite_nonproduction_store
- implementation_runtime = Python standard-library sqlite3
- persistence_target_kind = dedicated_local_sqlite_nonproduction_store
- logical_repository_relative_target_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- target_table = governed_nonproduction_evidence_records_v0_1
- mutation_mode = transactional_create_only
- production_target = no
- case_store_reuse = no
- route_or_cli_exposed = no
- target_created_now = no

This is the only selected design. It isolates one nonproduction record, permits database-enforced uniqueness and transaction tests, and avoids production case replacement.

## Safe Full-input Contract

- safe_input_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
- safe_input_version = 0.1
- real_payload_created_now = no
- future_capture_requires_separate_approval = yes
- silent_package_or_row_reopen_allowed = no

The schema binds every immutable identity field and contains only the strict safe candidate fields required by the adapter: opaque lineage IDs, evidence hash, bounded redacted snippet, bounded optional metadata, current warning/trust/review boundaries, schema versions, and its canonical safe hash. Raw rows, raw identities, URLs, secrets, paths, unrelated rows, and unbounded text are forbidden.

The initial implementation phase must use synthetic payload fixtures only. A future real payload capture remains separately governed.

## Adapter Plan

- proposed_module = backend/app/services/governed_nonproduction_evidence_persistence.py
- validation_symbol = validate_exact_locked_candidate_safe_write_payload
- adapter_symbol = build_governed_nonproduction_evidence_persistence_command
- adapter_io = none
- adapter_output_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_1

The pure adapter validates exact identity, payload hash, schema versions, gate binding, and future activation binding, then returns one deterministic create-only command. It cannot create a production `EvidenceItem`, call `CaseRepository.save_case_evidence`, invoke import/ingestion, replace a case, or select another candidate.

## Persisted Record and Receipt Schemas

- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1
- initial_record_status = governed_nonproduction_pending_human_review
- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_1

The record separates immutable identity, safe payload, gate and activation binding, persistence metadata, human-review/trust boundaries, revocation projection, and audit linkage. It preserves `human_review_required = true` and `automatic_trust_upgrade_allowed = false`.

The receipt reports target label, transaction result, attempt number, mutation count, duplicate state, exact-record readback, isolation checks, revocation availability, and explicit false production/downstream flags. Neither object contains raw row text, secrets, private identity, URLs, or absolute paths.

## Identity and Future Activation Binding

- candidate_identity_digest = canonical SHA-256 of every versioned immutable identity field
- activation_decision_safe_hash = canonical SHA-256 of a future separately recorded human activation decision
- helper_guard_phrase_alone_sufficient = no
- real_candidate_digest_calculated_now = no
- activation_decision_created_now = no

Both bindings are mandatory before any future mutation. 9A-22 supplies neither real activation values nor an activation phrase.

## Mutation and Idempotency Policy

- operation_model = transactional_create_only
- insert_count_per_new_request = 1
- update_or_upsert_allowed = no
- whole_case_replace_allowed = no
- fallback_target_allowed = no
- production_object_creation_allowed = no

The SQLite table must enforce primary-key uniqueness for `persisted_record_id`, uniqueness for `idempotency_key`, and uniqueness for `candidate_identity_digest`, plus checks that the record stays nonproduction and human-review-only.

Exact outcomes:

- new valid request: one insert, `created_exactly_one_governed_nonproduction_record`
- same key and canonical content: zero inserts, `already_exists_same_record`
- same identity with conflicting payload or activation: zero inserts, `blocked_identity_or_payload_conflict`
- different candidate: zero inserts, `scope_violation`
- indeterminate prior result: read-only lookup, `paused_pending_read_only_idempotency_verification`

The idempotency key hashes candidate identity, safe payload, record schema, gate contract, activation decision, mutation mode, and target. Deterministic IDs alone are not treated as sufficient.

## Attempt and Retry Policy

- maximum_mutating_attempts_per_activation = 1
- automatic_retry_allowed = no
- automatic_repair_write_allowed = no
- automatic_second_write_allowed = no
- read_only_verification_retry_allowed = yes

An ambiguous result permits read-only verification only. Another mutation requires fresh governance unless non-commit is conclusively proven.

## Atomicity and Partial-failure Policy

All validation occurs before `BEGIN IMMEDIATE`. One plain insert occurs inside one SQLite transaction. Constraints are enforced before one commit. A known pre-commit failure rolls back and records zero committed mutations. No other store is touched.

An ambiguous commit is followed only by read-only lookup. If exact single-record proof is unavailable, the result remains paused and does not claim success.

## Rollback and Revocation Policy

An uncommitted failure uses transaction rollback and no compensating write. A successfully persisted record is not deleted or silently updated. Later revocation requires separate human authorization and one append-only event using `sentigraph_governed_nonproduction_evidence_persistence_revocation_event_v0_1`; the immutable base record and receipt reference remain preserved.

Revocation is outside the initial implementation slice and does not authorize another base-record write.

## Post-write Verification Policy

A future successful receipt must prove the exact record exists once, stored identity and hashes match, mutation count is one for create or zero for idempotent reuse, no unrelated record changed, no case evidence list changed, no production `EvidenceItem` was created, and no downstream production or delivery runtime ran. Missing proof produces pause.

## Future Implementation File Allowlist Recommendation

The next separately approved implementation should be limited to:

- `backend/app/services/governed_nonproduction_evidence_persistence.py`
- `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
- `docs/health/sentigraph_governed_nonproduction_evidence_persistence_implementation_report_v0_1.md`

No route, CLI, frontend, generic case-store integration, provider, collector, runtime configuration, or Project Source file belongs in that slice.

## Future Test Plan

The future slice must be test-first and synthetic-only. It must cover RED before implementation, one create, idempotent second call, conflict rejection, identity and activation mismatch, safe-hash and schema mismatch, transaction rollback, ambiguous-result read-only lookup, no automatic retry, attempt enforcement, exactly-one receipt, no unrelated change, no production case or `EvidenceItem`, privacy rejection, no route/API/network/subprocess, focused regressions, `py_compile`, static forbidden-import/IO scans, and `git diff --check`.

The test database must use a temporary directory. The real logical target, candidate payload, package, and row remain unopened.

## Implementation-readiness Outcome

- selected_outcome = ready_for_separate_narrow_nonproduction_persistence_implementation_authorization
- exact_target_selected = yes
- safe_input_contract_complete = yes
- adapter_contract_complete = yes
- record_and_receipt_contracts_complete = yes
- identity_and_activation_bindings_complete = yes
- idempotency_and_uniqueness_complete = yes
- attempt_and_retry_policy_complete = yes
- atomicity_and_partial_failure_complete = yes
- rollback_and_revocation_complete = yes
- post_write_verification_complete = yes
- synthetic_validation_plan_complete = yes
- unresolved_design_gap = none_for_the_narrow_synthetic_implementation_slice

This outcome permits preparation of a separately scoped implementation authorization request only. It does not make gate activation, a real payload capture, a real write, or production object creation ready.

## Whether Narrow Implementation Authorization May Be Prepared

- narrow_nonproduction_implementation_authorization_may_be_prepared = yes
- gate_activation_authorization_may_be_prepared = no
- actual_write_authorization_may_be_prepared = no
- production_evidenceitem_authorization_may_be_prepared = no

Any future authorization must be newly human-authored and limited to the isolated service, synthetic fixtures, and temporary SQLite validation. This document intentionally provides no approval phrase or ready-to-sign text.

## Selected Next Boundary

- next_default = pause_before_implementation
- selected_next_boundary = separately_approved_narrow_synthetic_only_nonproduction_persistence_implementation
- real_candidate_payload_next = no
- gate_activation_next = no
- actual_write_next = no
- production_evidenceitem_creation_next = no

## No-side-effect State

- package_or_row_read = no
- runtime_or_configured_store_read = no
- sqlite_database_created = no
- persistence_accessed = no
- backend_code_changed = no
- backend_tests_changed = no
- schema_or_route_changed = no
- frontend_changed = no
- gate_activated = no
- actual_write_execution_performed = no
- persisted_evidence_layer_record_created = no
- production_evidenceitem_created = no
- production_case_changed = no
- downstream_runtime_called = no
- provider_or_collector_called = no
- real_api_or_llm_called = no
- url_fetch_or_scrape = no

## Git, Release, and Source Recommendation

- commit_recommended = yes
- recommended_commit_message = Design 9A-22 governed nonproduction persistence prerequisite
- tag_recommended = no
- project_source_update_recommended = yes after commit
- project_source_replacement_scope = Canonical 00 and Canonical 09
- canonical_03_or_source11_domain_update_recommended = no

Canonical 03 and Source 11 remain unchanged because 9A-22 changes architecture documentation only and does not change runtime or business behavior.
