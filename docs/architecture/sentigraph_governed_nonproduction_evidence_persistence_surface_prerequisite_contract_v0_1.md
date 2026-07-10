# Sentigraph Governed Nonproduction Evidence Persistence Surface Prerequisite Contract v0.1

## Purpose and Scope

This contract defines the architecture prerequisite for one future governed, local, nonproduction persistence surface for one exact locked candidate. It closes the design gaps identified by 9A-21 without implementing a store, creating a database, activating the 9A-20 gate, executing a write, or creating a production `EvidenceItem`.

The design is internal, disabled by default, synthetic-fixture-testable, and isolated from production case persistence. It is not an execution approval or a ready-to-sign activation instrument.

## Contract Summary

- contract_phase = 9A-22
- docs_only = yes
- implementation_performed = no
- persistence_accessed = no
- gate_activated = no
- write_performed = no
- production_evidenceitem_created = no
- recommended_target_selected = yes
- safe_input_contract_defined = yes
- adapter_contract_defined = yes
- persisted_record_schema_defined = yes
- receipt_schema_defined = yes
- identity_binding_defined = yes
- activation_binding_defined = yes
- idempotency_contract_defined = yes
- bounded_attempt_policy_defined = yes
- atomicity_partial_failure_contract_defined = yes
- rollback_revocation_contract_defined = yes
- post_write_verification_contract_defined = yes
- future_implementation_slice_defined = yes

`recommended_target_selected = yes` means one design target is selected. It does not mean the target exists or may be created now.

## Preserved Governance State

9A-19 remains unchanged:

- human_final_write_authorization_decision_received = yes
- human_final_write_authorization_decision = approved
- human_final_write_authorization_performed = yes
- final_write_authorization_scope = exact_locked_candidate_only
- candidate_authorized_for_future_separately_gated_evidence_layer_write = yes

9A-20 remains established but inactive:

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

9A-21 remains the current readiness finding:

- audit_task_complete = yes
- exact_execution_surface_classification = existing_but_non_persistent
- persistence_target_bound_to_gate = no
- activation_readiness_outcome = not_ready_due_to_nonpersistent_or_test_only_surface
- gate_activation_ready = no
- workflow_disposition = pause

9A-22 defines a prerequisite architecture only. It does not change any of these states.

## Exact Candidate Governance Binding

The future payload, command, record, receipt, lookup, and revocation event must bind to this indivisible identity:

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

The whole package and other rows remain unapproved. Candidate, package, role, case hint, row source, preview identity, schema, ID, and hash substitution are forbidden. A mismatch stops before persistence and requires fresh governance.

## Selected Persistence Target

- persistence_target_kind = dedicated_local_sqlite_nonproduction_store
- implementation_runtime = Python standard-library `sqlite3`
- logical_repository_relative_target_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
- target_table = governed_nonproduction_evidence_records_v0_1
- production_target = no
- case_store_reuse = no
- route_or_cli_exposed = no
- frontend_exposed = no
- disabled_by_default = yes
- target_creation_requires_future_implementation_approval = yes
- target_exists_or_was_created_in_9a22 = no

The repository ignores `runtime/`, Python 3.10 includes `sqlite3`, and no runtime SQLite dependency is declared. The future module must accept an explicit disabled-by-default configuration and must not infer enablement from a route, CLI, provider, collector, or current environment. Synthetic tests must use a temporary test database, not the logical runtime target.

## Target Rationale and Case-store Isolation

The dedicated SQLite target is safer than adapting the generic case persistence chain because it:

- stores one isolated nonproduction governance record rather than replacing a whole case;
- supports enforceable uniqueness and one-transaction create-only semantics;
- avoids `CaseRepository.save_case_evidence`, `LocalJsonCaseStore`, and `MongoDbCaseStore`;
- cannot mutate a case evidence list or create a production `EvidenceItem`;
- has no API, route, CLI, frontend, provider, or collector entry point;
- can be validated with synthetic fixtures and a temporary database;
- keeps its schema and lifecycle distinct from production case schemas;
- permits deterministic read-only verification after an ambiguous result.

The generic chain remains out of scope because it is broader, whole-case-oriented, configurable to production-capable stores, and not bound to the exact candidate or 9A-20 gate.

## Safe Full-input Payload Contract

### Schema

- payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
- payload_version = 0.1
- creation_mode = separately_approved_one_time_safe_capture
- created_in_9a22 = no
- package_or_row_reopen_allowed = no
- canonical_hash_algorithm = sha256
- canonical_hash_scope = versioned_safe_canonical_payload_projection_only

The future real payload may be created only by a separate, explicitly approved capture step. It must not be reconstructed from identity alone and must not silently reopen a package or row. The initial implementation slice uses synthetic payloads only.

### Required top-level fields

1. `payload_schema`
2. `payload_version`
3. `source_candidate_set_schema`
4. `source_candidate_schema`
5. `source_schema_versions`
6. `immutable_candidate_identity`
7. `candidate_projection`
8. `lineage_projection`
9. `boundary_projection`
10. `input_safe_hash`

`immutable_candidate_identity` contains every field listed in the exact candidate governance binding.

`candidate_projection` is a strict allowlist with these required fields, matching the minimum accepted by the controlled candidate shape:

- evidence_layer_write_candidate_schema
- evidence_layer_write_candidate_id
- source_production_evidence_import_candidate_id
- source_evidence_layer_write_candidate_id
- source_evidence_layer_import_candidate_id
- source_review_queue_candidate_id
- source_evidence_candidate_id
- evidence_id_hash
- text_snippet_redacted

The following bounded safe fields are allowed when present and validated:

- preview_hash
- case_id_hint
- platform
- evidence_type
- created_at_date
- source_url_present
- acquisition_mode
- provenance_type
- verification_status
- review_status
- trust_label
- redaction_status
- title_or_label_redacted
- redaction_warnings
- warning_labels
- blocker_codes

The adapter maps the payload's single `created_at_date` field to the command's `coarse_created_at` field. No alternate date field is accepted by this payload schema.

`text_snippet_redacted` and `title_or_label_redacted` are capped at 160 characters, must already be redacted, and are not raw-row fields. No arbitrary extra field is accepted.

`lineage_projection` contains only opaque source candidate IDs and schema labels required to prove the existing controlled lineage. It contains no path, URL, package row, or source content.

`boundary_projection` must assert:

- human_review_required = true
- no_automatic_trust_upgrade = true
- preview_only = true
- import_candidate_only = true
- production_import_candidate_only = true
- write_candidate_only = true
- evidence_layer_write_candidate_only = true
- not_production_evidence_item = true
- no_evidence_layer_write = true at payload-capture time
- warning_count = 1
- warning_labels includes manual_review_required

The contract forbids raw row text, raw comments, raw author identity, profile URLs, source URLs, private messages, secrets, credentials, API keys, tokens, cookies, sessions, salts, passwords, environment values, absolute paths, package paths, unrelated rows, response text, generated public messages, targeting or persuasion fields, truth or official-verification claims, prediction probabilities, psychological profiles, and real-person PII.

The payload is invalid if any immutable identity field differs, its canonical safe hash differs, a required field is missing, an extra field is present, redaction bounds fail, or a boundary is weakened.

### Top-level field types and constraints

| Field | Type | Constraint |
|---|---|---|
| `payload_schema` | string | Exact schema name only |
| `payload_version` | string | Exact value `0.1` |
| `source_candidate_set_schema` | string | Exact locked set schema |
| `source_candidate_schema` | string | Exact item schema `sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_v0_1` |
| `source_schema_versions` | object | Exact string labels for set, item, identity, and payload schemas; no extra keys |
| `immutable_candidate_identity` | object | All exact immutable fields, strict key set |
| `candidate_projection` | object | Strict required and allowed safe fields defined above |
| `lineage_projection` | object | Opaque IDs and schema labels only |
| `boundary_projection` | object | Exact required booleans, warning count, and warning labels |
| `input_safe_hash` | 64-character lower-case hexadecimal string | Canonical SHA-256 over all prior payload fields and schema/version |

Opaque IDs must match the repository's bounded safe-token form and must not be URL-like or path-like. Hashes must be 64-character lower-case hexadecimal strings. Dates use `YYYY-MM-DD`. Arrays are bounded to 20 safe labels; labels are bounded to 80 characters.

## Pure Adapter Contract

The future pure adapter is defined as:

- module = backend/app/services/governed_nonproduction_evidence_persistence.py
- validation_symbol = validate_exact_locked_candidate_safe_write_payload
- adapter_symbol = build_governed_nonproduction_evidence_persistence_command
- command_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_1
- store_class = GovernedNonproductionEvidencePersistenceStore
- create_symbol = create_governed_nonproduction_evidence_record
- lookup_symbol = find_governed_nonproduction_record_by_idempotency_key
- verification_symbol = verify_governed_nonproduction_evidence_record

The adapter accepts the safe payload, immutable governance identity, gate contract binding, and separately recorded activation-decision binding. It performs no IO and returns one deterministic persistence command.

It must:

- validate exact identity, schema, version, and safe hash;
- preserve `human_review_required = true`;
- preserve `no_automatic_trust_upgrade = true`;
- reject missing fields, extra identity fields, and every substitution;
- produce exactly one record command for exactly one candidate;
- never produce a production `EvidenceItem`;
- never call `CaseRepository.save_case_evidence`;
- never replace a whole case;
- never invoke `evidence_import.py`, `evidence_ingestion.py`, or import/ingestion routes;
- never select a fallback candidate or target.

The command contains only validated canonical values. It does not contain an open connection, path discovered from input, callback, executable action, or mutable production object.

The store constructor accepts an explicitly injected repository-relative target and `enabled = false` by default. Validation and construction while disabled must not create a directory or database. Only a future separately authorized synthetic test may pass `enabled = true` with a temporary target; no environment variable, global singleton, route, or CLI can enable it.

## Persisted-record Schema

- persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1
- initial_status = governed_nonproduction_pending_human_review
- mutation_mode = transactional_create_only

The record contains these groups and fields.

### Record identity and candidate binding

- persisted_record_id
- persisted_record_schema
- candidate_id
- candidate_safe_hash
- candidate_identity_digest
- preview_row_id
- preview_row_safe_hash
- package_name
- candidate_role
- case_id_hint
- row_source
- identity_schema
- identity_version

### Safe input projection

- input_schema
- input_schema_version
- input_safe_hash
- safe_payload_projection
- source_schema_versions
- lineage_projection

### Gate and future activation binding

- gate_contract_schema
- gate_contract_version
- gate_contract_safe_hash
- activation_decision_id
- activation_decision_safe_hash

These activation fields are schema definitions only. 9A-22 assigns no real activation values.

### Persistence and review metadata

- idempotency_key
- mutation_mode
- status
- human_review_required
- automatic_trust_upgrade_allowed
- created_at
- revoked_at, nullable read-model field
- revocation_reason, nullable read-model field
- audit_receipt_reference

`automatic_trust_upgrade_allowed` must be false. Status may not be `verified`, `production`, `approved_for_analysis`, `analysis_ready`, `official`, or `trusted_high`.

### Audit boundaries

- production_evidenceitem_created = false
- production_case_changed = false
- downstream_runtime_called = false
- package_or_row_read_during_persistence = false
- trust_or_role_reclassified = false

The base record is immutable after initial insertion. `revoked_at` and `revocation_reason` are derived in the read model from a separately authorized append-only revocation event; they are null in the initial base row.

### Record field types

| Field group | Types and constraints |
|---|---|
| IDs and hashes | Opaque bounded strings for IDs; 64-character lower-case hexadecimal strings for all digests |
| Schemas and versions | Exact versioned string constants |
| `safe_payload_projection`, `source_schema_versions`, `lineage_projection` | Canonical JSON objects validated before insertion |
| `mutation_mode`, `status` | Exact enumerated strings defined by this contract |
| Review and side-effect boundaries | SQLite integers constrained to 0 or 1, with required fixed values |
| `created_at` | UTC RFC 3339 string assigned once at insert |
| `revoked_at`, `revocation_reason` | Nullable read-model values derived from a revocation event, never initial base-row updates |
| `audit_receipt_reference` | Deterministic opaque receipt ID |

## Persistence Receipt Schema

- receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_1
- receipt_persistence_in_initial_slice = no
- receipt_kind = safe_in_memory_post_transaction_result

The receipt contains:

- receipt_id
- receipt_schema
- persisted_record_id
- idempotency_key
- candidate_identity_digest
- activation_decision_safe_hash
- target_logical_label
- mutation_mode
- mutation_attempt_limit
- mutation_attempt_number
- transaction_started
- transaction_committed
- mutation_count, constrained to 0, 1, or null for an unresolved ambiguous commit
- already_exists
- duplicate_conflict
- persisted_record_verified
- exactly_one_record_verified
- unrelated_record_change_detected
- post_write_readback_verified
- rollback_or_revocation_available
- production_evidenceitem_created = false
- production_case_changed = false
- downstream_runtime_called = false
- final_outcome
- created_at

The receipt contains no raw row text, source URL, path, secret, identity, or production object. `audit_receipt_reference` in the base record is a deterministic safe receipt ID known before insertion. The receipt object is assembled after commit and readback; its existence does not add a second database mutation.

Receipt booleans are strict booleans. Attempt fields are positive integers bounded by one. `mutation_count` is `0`, `1`, or null only for an unresolved ambiguous commit. `final_outcome` is one of the exact outcomes in this contract or a bounded failure/pause code; it may not imply production readiness or official verification.

## Immutable Identity Binding

`candidate_identity_digest` is the lower-case hexadecimal SHA-256 digest of UTF-8 canonical JSON containing every immutable candidate identity field, with schema/version included, keys sorted, no insignificant whitespace, and no omitted or null-substituted field.

The canonical projection is versioned. Any field, type, ordering rule, schema, or version mismatch blocks before transaction. 9A-22 does not calculate the real digest.

## Future Activation-decision Binding

The future execution requires a separately recorded human activation decision with:

- activation_decision_id
- activation_decision_schema
- activation_decision_version
- activation_decision_safe_hash
- candidate_identity_digest
- gate_contract_safe_hash
- decision_scope = exact_locked_candidate_and_selected_nonproduction_target_only

`activation_decision_safe_hash` is a SHA-256 digest over the versioned safe decision projection. A helper guard phrase alone is insufficient. The decision must independently bind the candidate identity, 9A-20 gate contract, selected target, mutation mode, and maximum attempt count.

No activation decision exists or is supplied here, and this contract contains no activation phrase.

## Idempotency-key Contract

`idempotency_key` is the lower-case hexadecimal SHA-256 digest of versioned canonical JSON containing at least:

- candidate_identity_digest
- input_safe_hash
- persisted_record_schema and version
- gate_contract_schema, version, and safe hash
- activation_decision_safe_hash
- mutation_mode = transactional_create_only
- target logical label

`persisted_record_id` is deterministically derived from a versioned namespace plus the idempotency key. Deterministic IDs supplement but do not replace storage uniqueness and readback verification.

## Transactional Create-only Semantics

The exact operation model is `transactional_create_only`:

1. Validate all schemas, identity, hashes, gate binding, activation binding, target, privacy boundaries, and attempt state before opening a transaction.
2. Open one SQLite connection to the explicitly injected approved target.
3. Begin one immediate transaction.
4. Perform read-only conflict checks inside the transaction.
5. Execute one plain `INSERT`; do not use update, replace, merge, or upsert.
6. Commit once.
7. Close the mutation path.
8. Perform read-only post-write verification.
9. Return one safe receipt.

There is no whole-case replacement, implicit migration, fallback target, automatic second write, repair write, production object creation, or unrelated store mutation.

## Uniqueness Constraints

The table must enforce:

- primary key on `persisted_record_id`;
- unique constraint on `idempotency_key`;
- unique constraint on `candidate_identity_digest`;
- checks for the exact record schema, `transactional_create_only`, initial nonproduction status, `human_review_required = 1`, `automatic_trust_upgrade_allowed = 0`, and all production/downstream flags false.

Unique `candidate_identity_digest` is intentionally conservative: one candidate cannot silently create another base record under a different payload or activation. Any later exception requires fresh governance and a new contract, not an upsert.

## Duplicate, Already-exists, and Conflict Outcomes

| Request state | Mutation | Exact outcome |
|---|---:|---|
| New valid request | 1 | `created_exactly_one_governed_nonproduction_record` |
| Same idempotency key and same canonical content | 0 | `already_exists_same_record` |
| Same candidate identity with conflicting payload, gate, or activation binding | 0 | `blocked_identity_or_payload_conflict` |
| Different candidate | 0 | `scope_violation` |
| Unknown or indeterminate prior result | 0 pending lookup | `paused_pending_read_only_idempotency_verification` |

An unknown result triggers a read-only lookup by idempotency key and candidate digest. It never triggers an automatic mutation retry.

## Maximum Attempts and Retry Policy

- maximum_mutating_attempts_per_activation = 1
- automatic_retry_allowed = no
- automatic_repair_write_allowed = no
- automatic_second_write_allowed = no
- read_only_verification_retry_allowed = yes

The attempt is consumed when the transaction reaches the insert operation. Validation failure does not consume it because no mutation began. After an ambiguous commit, only read-only verification is allowed. A second mutating attempt requires a new governance decision unless it is conclusively proven that the insert was never issued or the transaction rolled back before commit.

## Validation Before Mutation

All of the following must pass before `BEGIN IMMEDIATE`:

- exact immutable identity match;
- payload schema/version and canonical hash match;
- strict payload field allowlist and redaction bounds;
- lineage continuity and opaque reference checks;
- gate contract schema/version/hash match;
- separately recorded activation decision match;
- target logical label match;
- attempt number equals 1 and no prior mutation attempt is recorded;
- privacy and secret scan clear;
- `human_review_required = true`;
- `no_automatic_trust_upgrade = true`;
- all production and downstream flags false;
- idempotency and candidate conflict state determinable.

Any failure pauses before transaction.

## Atomicity and Partial Failure

For the selected SQLite design:

- schema and input validation finish before the transaction;
- `BEGIN IMMEDIATE` obtains the write reservation before conflict lookup and insert;
- one insert is the only mutation inside the transaction;
- SQLite constraints are enforced inside the transaction;
- commit outcome is captured;
- a pre-commit exception causes explicit rollback;
- no external side effect occurs before commit;
- no other persistence target is updated;
- a known rollback returns failure with zero committed mutations;
- an ambiguous commit performs read-only lookup only and never retries the mutation.

An ambiguous result is successful only if readback can conclusively verify the exact record, identity, payload hash, gate binding, activation binding, and single-record count. Otherwise the receipt uses `mutation_count = null`, final outcome `paused_ambiguous_commit_not_proven`, and the workflow pauses.

## Rollback and Revocation

### Failed uncommitted transaction

- Execute transaction rollback.
- Persist no record.
- Return a safe failure receipt with `transaction_committed = false` and `mutation_count = 0` when rollback is known.
- Do not invoke any compensating write.

### Successful record later revoked

Revocation is a separate governed operation, not rollback and not part of the initial implementation slice. It must:

- require separate human authorization;
- append one event using schema `sentigraph_governed_nonproduction_evidence_persistence_revocation_event_v0_1`;
- identify the original record, candidate digest, receipt, reason code, authorizing decision digest, and revocation time;
- preserve the immutable base record and creation receipt reference;
- derive effective `revoked_at` and `revocation_reason` in the read model;
- never silently delete, restore trust, permit a second base write, or broaden scope.

The future revocation table is append-only with a unique constraint on `persisted_record_id`. It is not created or exercised in 9A-22.

## Post-write Verification Contract

Minimum proof for a successful future receipt requires read-only evidence that:

- the intended `persisted_record_id` exists;
- exactly one record matches both record ID and candidate digest;
- canonical stored identity equals the approved identity;
- stored `input_safe_hash` equals the command;
- gate and activation bindings equal the command;
- `mutation_count = 1` for a new write or `0` for `already_exists_same_record`;
- the table-wide before/after identity set differs only by the intended new record for a new write;
- no unrelated record changed;
- no case evidence list or generic case-store record changed;
- no production `EvidenceItem`, Review Queue item, case, `analysis_run`, Analysis Result, Source 11, FinalSummaryReport, B-end report, Sandbox/public event, export, public, or delivery runtime ran;
- revocation capability is represented by the contract and record reference;
- human review remains required;
- automatic trust upgrade remains forbidden.

The minimum evidence is: validated command digest; pre-transaction candidate/idempotency lookup result; SQLite transaction outcome; post-transaction exact-record readback; exact matching count; a before/after digest of safe record IDs and canonical record hashes; false side-effect assertions; and the receipt. Missing proof yields pause, not success.

## Auditability

The future module must use canonical JSON and versioned hashes, record the target logical label rather than an absolute path, return explicit outcomes, and preserve safe before/after counts and digests. It must not log payload text, paths, secrets, or raw identity. The base record, receipt, and any later revocation event are linked by opaque IDs and canonical digests.

## Privacy and Redaction

The adapter and store must use strict field allowlists plus recursive forbidden-key and forbidden-value checks. Redacted snippets remain bounded to 160 characters. URL-like, path-like, credential-like, private-message, raw-identity, and real-person PII values block before transaction. The database and receipt must never contain raw package rows, comments, author identifiers, profiles, source URLs, secrets, cookies, sessions, environment values, or absolute paths.

## Production and Downstream Nonauthorization

This contract does not authorize or perform:

- execution-gate activation;
- actual Evidence Layer write for the real candidate;
- production `EvidenceItem` creation;
- generic case persistence or case evidence-list mutation;
- production Review Queue, case, `analysis_run`, analysis execution, or Analysis Result;
- Source 11, FinalSummaryReport, B-end report, Sandbox/public event, export, download, public access, external delivery, or final delivery;
- provider, collector, real API, real LLM, URL fetch, or scraping;
- real package, row, runtime, configured store, or database access.

## Future Implementation File Plan

A separately approved narrow implementation should be limited to:

1. `backend/app/services/governed_nonproduction_evidence_persistence.py`
   - strict schema constants and validators;
   - pure payload-to-command adapter;
   - disabled-by-default SQLite store;
   - create-only transaction and read-only verification;
   - safe receipt builder;
   - no route, CLI, case-store, provider, or collector integration.
2. `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
   - synthetic fixtures and temporary SQLite target only;
   - contract, atomicity, idempotency, privacy, and no-overreach tests.
3. `docs/health/sentigraph_governed_nonproduction_evidence_persistence_implementation_report_v0_1.md`
   - generated only during the separately authorized implementation phase;
   - records synthetic validation and no-real-data boundaries.

No schema module is required for the first slice because an isolated service-local typed contract keeps this nonproduction surface out of production API schemas. The future implementation must not modify routes, frontend, generic case persistence, Project Source, or runtime configuration.

## Future Synthetic Validation Plan

The future phase must start with TDD RED and use only in-memory payload fixtures plus a temporary SQLite database. Required tests are:

1. Valid single create commits exactly one record.
2. Same request on second call returns `already_exists_same_record` with no mutation.
3. Conflicting duplicate returns `blocked_identity_or_payload_conflict`.
4. Different candidate returns `scope_violation`.
5. Candidate identity mismatch blocks before transaction.
6. Activation-decision binding mismatch blocks before transaction.
7. Payload safe-hash mismatch blocks before transaction.
8. Schema or version mismatch blocks before transaction.
9. Transaction exception rolls back with zero committed mutations.
10. Ambiguous result permits read-only lookup and no mutation retry.
11. Maximum mutating attempt count is enforced.
12. Receipt proves exactly one mutation or zero-mutation idempotent reuse.
13. Before/after digest proves no unrelated record changed.
14. No production `EvidenceItem`, case, or case evidence list changes.
15. No route, API, network, subprocess, provider, or collector access.
16. Forbidden raw, private, secret, URL, and path fields block.
17. Revocation contract is tested only if the separately governed revocation slice is included; it is not required in the initial create-only slice.
18. Focused tests and nearby no-write governance regressions pass.
19. `py_compile`, forbidden import/IO/network/subprocess scans, and `git diff --check` pass.

The initial implementation must not read the real candidate payload, package, row, configured runtime target, or current persistence state.

## No-side-effect State

- package_or_row_read = no
- configured_store_or_database_read = no
- sqlite_database_created = no
- write_helper_imported_or_called = no
- persistence_accessed = no
- gate_activated = no
- actual_write_execution_approved = no
- actual_write_execution_performed = no
- production_evidenceitem_creation_authorized = no
- production_evidenceitem_created = no
- production_case_changed = no
- downstream_runtime_called = no
- provider_or_collector_called = no
- real_api_or_llm_called = no
- url_fetch_or_scrape = no

## Architecture Outcome and Next Boundary

- implementation_readiness_outcome = ready_for_separate_narrow_nonproduction_persistence_implementation_authorization
- gate_activation_ready = no
- human_gate_activation_decision_may_be_prepared_now = no
- actual_write_ready = no
- production_evidenceitem_creation_authorized = no
- next_boundary = separately_approved_narrow_synthetic_only_nonproduction_persistence_implementation

The next boundary may authorize only the isolated implementation and synthetic validation described above. It must not activate the 9A-20 gate, read the real candidate payload, execute the real write, or create a production `EvidenceItem`.
