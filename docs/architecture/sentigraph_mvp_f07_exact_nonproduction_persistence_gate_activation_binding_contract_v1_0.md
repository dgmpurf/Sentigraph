# Sentigraph MVP-F07 Exact Nonproduction Persistence Gate Activation Binding Contract v1.0

## 1. Purpose and Boundary

This document defines the canonical governance bindings for one exact
nonproduction persistence gate-activation decision. It binds one locked
candidate, one independently accepted safe payload, one established gate
contract, one initialized exact-empty target, and the current frozen public
writer surface.

This contract records no runtime activation. It does not read the protected
payload or receipt, inspect the SQLite target, create an attempt reservation,
invoke the writer, execute persistence, or create a production object.

```text
contract_schema = sentigraph_mvp_f07_exact_nonproduction_persistence_gate_activation_binding_contract_v1_0
contract_version = 1.0
MVP_F07_status = candidate_completed_pending_chatgpt_acceptance
gate_activation_record_status = candidate_pending_chatgpt_independent_acceptance
execution_gate_effective_activation = no_pending_chatgpt_acceptance
MVP_F08_authorized_now = false
MVP_F08_executed = false
```

## 2. Authoritative Committed Evidence

All SHA-256 values below are calculated from committed blob bytes at commit
`60a61157ecfc3b2768f710376ecdea90ee02f1b3`.

| Evidence | Committed blob SHA-256 |
| --- | --- |
| `docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md` | `a853d5826c5e553bda64ed790ef87e693175e85bfd2d4a18797c5983c60d5f80` |
| `docs/architecture/sentigraph_exact_locked_candidate_human_final_write_authorization_contract_v0_1.md` | `532030df71a16d151ea48ecfbde8daacae26982ec947e0cf51bb65be2029d776` |
| `docs/planning/sentigraph_9a_19_exact_locked_candidate_human_final_write_authorization_decision_v0_1.md` | `ed19ac164f8ce56a3b7b6981bd408bc3fd3fba95b293432a28180c53d94321a6` |
| `docs/architecture/sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1.md` | `7469fbf64060e6c9fcc0217e89400e5a251b17e74eebe30de122b13a8f2e85ea` |
| `docs/planning/sentigraph_9a_20_exact_locked_candidate_actual_evidence_layer_write_execution_gate_establishment_authorization_decision_v0_1.md` | `45ee6de13f54074a53793b2789f79918cb7463b868449602c989bd3ead36eed0` |
| `docs/health/sentigraph_mvp_c02_p2_independent_repaired_scanner_acceptance_and_bounded_remediation_capture_report_v1_0.md` | `b6e5b7f60e11bb6981080cef9cc4da520fbb0504c6d43e1cdfeb344bbb5c8af7` |
| `docs/health/sentigraph_mvp_chg_002_f04_durable_receipt_auditor_and_exact_path_acceptance_recheck_report_v1_0.md` | `0dc82215ea2e8d6e16de5ade1471c488c601ecf1ba3900cbbec53ba52ef29a1b` |
| `docs/architecture/sentigraph_mvp_f05_exact_logical_nonproduction_persistence_target_authorization_contract_v1_0.md` | `0b319cbdf48348136d779e64c7634d1827bf9c5bee70e65f9a9878198856a9b3` |
| `docs/planning/sentigraph_mvp_f05_exact_logical_nonproduction_persistence_target_authorization_decision_v1_0.md` | `28603bc684a50414fe5f744bf4038d1178d064c027f5c6aa37d46197e7dda662` |
| `docs/health/sentigraph_mvp11_f01_receipt_finalization_and_failure_artifact_semantics_repair_report_v1_0.md` | `52f3f42a78e3703b0af587feb64b7b3d6c73e5b4b0226ff71503ab29fdf63517` |
| `docs/health/sentigraph_mvp11_f02_independent_formal_profile_acceptance_and_exact_formal_target_f06_recheck_report_v1_0.md` | `ec60ecffd2235722c7c8b95367c260cd3a6e375b33cd9bccaca20b6f24dc9bbe` |
| `backend/app/services/governed_nonproduction_evidence_persistence.py` | `ca5021eb28779685a3d5c0ec42874528025baaaae7c7de3026528d8e0c10e99c` |
| `docs/architecture/sentigraph_internal_alpha_mvp_master_completion_baseline_v1_1.md` | `9c4e341792c4226ea5a2431dd6af694feb9cff306f697849c3f73901c86da399` |

No working-tree line-ending conversion is used as hash authority.

## 3. Canonicalization Rules

Every digest in this contract uses canonical JSON with these exact rules:

```text
encoding = UTF-8
ensure_ascii = true
sort_keys = true
separators = comma_and_colon_without_spaces
extra_fields = forbidden
hash_algorithm = SHA-256
```

## 4. Immutable Candidate Identity

The following complete safe identity is equal across the committed 9A-16C,
9A-19, human-authorization contract, gate contract, and 9A-20 decision. No
nearby value or substitute is used.

```json
{"approved_case_id_hint":"donglu_sunjihai_youth_football_202606","approved_package_name":"donglu-sunjihai-youth-football-202606-v2_20260617_121016","approved_package_role":"candidate_demo_sample","approved_row_source":"evidence_items.jsonl","candidate_lock_status":"locked_for_single_candidate_governance_review_only","final_candidate_id":"evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410","final_candidate_safe_hash":"2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5","final_candidate_schema":"sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1","hash_algorithm":"sha256","hash_input_scope":"versioned_safe_canonical_projection_only","identity_schema":"sentigraph_one_real_source_locked_candidate_identity_v0_1","identity_version":"0.1","selected_preview_row_opaque_id":"preview-row-001","selected_preview_row_safe_hash":"ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391"}
```

```text
candidate_identity_cross_document_equality = pass
candidate_identity_digest = 078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54
candidate_substitution_allowed = false
```

## 5. Audited Safe-payload Binding

Committed C02-P2 evidence establishes one payload with schema
`sentigraph_exact_locked_candidate_safe_write_payload_v0_1`, version `0.1`,
and one unique input safe hash. Its validator and protected-value scanner
passed. CHG-002 independently accepted the same payload and passed canonical
hash, immutable identity, lineage, boundary, validator, scanner, receipt, and
cross-binding checks. No later committed rejection supersedes that acceptance.

```json
{"C02_P2_report_committed_blob_sha256":"b6e5b7f60e11bb6981080cef9cc4da520fbb0504c6d43e1cdfeb344bbb5c8af7","C02_P2_report_path":"docs/health/sentigraph_mvp_c02_p2_independent_repaired_scanner_acceptance_and_bounded_remediation_capture_report_v1_0.md","CHG_002_report_committed_blob_sha256":"0dc82215ea2e8d6e16de5ade1471c488c601ecf1ba3900cbbec53ba52ef29a1b","CHG_002_report_path":"docs/health/sentigraph_mvp_chg_002_f04_durable_receipt_auditor_and_exact_path_acceptance_recheck_report_v1_0.md","input_safe_hash":"71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5","payload_runtime_artifact_read_during_F07":false,"payload_schema":"sentigraph_exact_locked_candidate_safe_write_payload_v0_1","payload_version":"0.1","safe_payload_independently_accepted":true}
```

## 6. Gate-contract Binding

The established 9A-20 gate remains bound to the same candidate, requires a
separate activation and execution approval, prohibits automatic retry and a
second write, requires exactly-one mutation and post-write verification, and
does not authorize production `EvidenceItem` creation.

Canonical gate-contract projection:

```json
{"gate_contract_document_committed_blob_sha256":"7469fbf64060e6c9fcc0217e89400e5a251b17e74eebe30de122b13a8f2e85ea","gate_contract_document_path":"docs/architecture/sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1.md","gate_contract_schema":"sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1","gate_contract_version":"0.1","gate_establishment_decision_document_committed_blob_sha256":"45ee6de13f54074a53793b2789f79918cb7463b868449602c989bd3ead36eed0","gate_establishment_decision_document_path":"docs/planning/sentigraph_9a_20_exact_locked_candidate_actual_evidence_layer_write_execution_gate_establishment_authorization_decision_v0_1.md"}
```

```text
gate_contract_safe_hash = a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a
```

Writer-compatible gate binding:

```json
{"gate_contract_safe_hash":"a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a","gate_contract_schema":"sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1","gate_contract_version":"0.1"}
```

## 7. Target and Initialization Binding

```text
target_kind = dedicated_local_sqlite_nonproduction_store
target_logical_label = runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3
target_primary_table = governed_nonproduction_evidence_records_v0_1
target_attempt_reservation_table = governed_nonproduction_evidence_persistence_attempt_reservations_v0_1
target_identity_safe_hash = 6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b
target_authorization_contract_safe_hash = f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2
target_initialization_report_commit = 60a61157ecfc3b2768f710376ecdea90ee02f1b3
target_initialization_report_sha256 = ec60ecffd2235722c7c8b95367c260cd3a6e375b33cd9bccaca20b6f24dc9bbe
target_initialization_outcome = initialized_exact_empty_target
```

The committed F02 report proves one formal invocation, zero retries, one
SQLite connection, zero reopens, two DDL statements, one successful commit,
exact schema conformance, zero base records, zero reservations, `ok` integrity,
zero sidecars, an accepted finalized receipt, zero user DML, and no payload,
source, gate, persistence, or production action. F07 does not re-open the
target or receipt.

## 8. Execution-surface Binding

```text
module = backend/app/services/governed_nonproduction_evidence_persistence.py
writer = create_governed_nonproduction_evidence_record
store = GovernedNonproductionEvidencePersistenceStore
payload_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
payload_version = 0.1
persisted_record_schema = sentigraph_governed_nonproduction_evidence_persistence_record_v0_1
attempt_reservation_schema = sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1
internal_command_schema = sentigraph_governed_nonproduction_evidence_persistence_command_v0_2
persistence_receipt_schema = sentigraph_governed_nonproduction_evidence_persistence_receipt_v0_2
mutation_mode = transactional_create_only
maximum_mutating_attempts = 1
automatic_retry_allowed = false
automatic_second_write_allowed = false
automatic_repair_write_allowed = false
```

The public writer accepts source payload, expected identity, gate binding,
activation binding, logical target label, and mutation attempt number. It
internally revalidates and rederives the command, IDs, digests, reservation,
and record. F07 neither imports nor calls the writer.

## 9. Activation-decision Projection

The supplied human approval is bound only to this exact nonproduction scope.
The canonical hash input excludes only `activation_decision_safe_hash`:

```json
{"MVP_F08_authorized_now":false,"MVP_F08_executed":false,"activation_decision_id":"sentigraph-mvp-f07-exact-nonproduction-persistence-gate-activation-001","activation_decision_reusable":false,"activation_decision_revocable_before_writer_invocation":true,"activation_decision_schema":"sentigraph_exact_locked_candidate_nonproduction_persistence_gate_activation_decision_v0_1","activation_decision_version":"0.1","activation_writer_invocation_limit":1,"attempt_reservation_schema":"sentigraph_governed_nonproduction_evidence_persistence_attempt_reservation_v0_1","audited_payload_input_safe_hash":"71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5","audited_payload_schema":"sentigraph_exact_locked_candidate_safe_write_payload_v0_1","audited_payload_version":"0.1","automatic_repair_write_allowed":false,"automatic_retry_allowed":false,"automatic_second_write_allowed":false,"binding_mismatch_invalidates_activation":true,"candidate_identity_digest":"078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54","candidate_or_reservation_write_performed":false,"decision_scope":"exact_locked_candidate_and_selected_nonproduction_target_only","exact_user_approval_phrase":"APPROVE_SENTIGRAPH_MVP_F07_EXACT_NONPRODUCTION_PERSISTENCE_GATE_ACTIVATION_DECISION_RECORDING_DOCS_ONLY_BIND_EXACT_LOCKED_CANDIDATE_AUDITED_SAFE_PAYLOAD_EXISTING_GATE_CONTRACT_INITIALIZED_EXACT_TARGET_TRANSACTIONAL_CREATE_ONLY_MUTATION_MODE_AND_ONE_MUTATING_ATTEMPT_NO_CODE_CHANGE_NO_PAYLOAD_SOURCE_TARGET_OR_RECEIPT_REREAD_NO_CANDIDATE_OR_RESERVATION_WRITE_NO_PERSISTENCE_EXECUTION_NO_PRODUCTION_OBJECT","gate_contract_safe_hash":"a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a","gate_contract_schema":"sentigraph_exact_locked_candidate_actual_evidence_layer_write_execution_gate_contract_v0_1","gate_contract_version":"0.1","gate_runtime_side_effect_performed":false,"human_gate_activation_decision":"approved","human_review_required":true,"maximum_mutating_attempts":1,"mutation_mode":"transactional_create_only","no_automatic_trust_upgrade":true,"persisted_record_schema":"sentigraph_governed_nonproduction_evidence_persistence_record_v0_1","persistence_execution_performed":false,"persistence_writer":"create_governed_nonproduction_evidence_record","production_evidenceitem_creation_authorized":false,"read_only_resolution_after_ambiguous_commit_allowed":true,"revocation_requires_new_exact_human_decision":true,"separate_MVP_F08_execution_approval_required":true,"superseding_decision_invalidates_activation":true,"target_authorization_contract_safe_hash":"f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2","target_identity_safe_hash":"6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b","target_initialization_outcome":"initialized_exact_empty_target","target_initialization_report_commit":"60a61157ecfc3b2768f710376ecdea90ee02f1b3","target_initialization_report_sha256":"ec60ecffd2235722c7c8b95367c260cd3a6e375b33cd9bccaca20b6f24dc9bbe","target_kind":"dedicated_local_sqlite_nonproduction_store","target_logical_label":"runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3"}
```

```text
activation_decision_safe_hash = 5906eecd4eabb6d82a07af455f3558590938fc75f007faaa5bdd3299218c03be
```

Writer-compatible activation binding:

```json
{"activation_decision_id":"sentigraph-mvp-f07-exact-nonproduction-persistence-gate-activation-001","activation_decision_safe_hash":"5906eecd4eabb6d82a07af455f3558590938fc75f007faaa5bdd3299218c03be","activation_decision_schema":"sentigraph_exact_locked_candidate_nonproduction_persistence_gate_activation_decision_v0_1","activation_decision_version":"0.1","candidate_identity_digest":"078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54","decision_scope":"exact_locked_candidate_and_selected_nonproduction_target_only","gate_contract_safe_hash":"a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a"}
```

The gate object has exactly three service-compatible keys. The activation
object has exactly seven service-compatible keys. The decision scope exactly
equals the current `ACTIVATION_DECISION_SCOPE` constant.

## 10. Gate-state Transition

```text
human_execution_gate_activation_decision_received = yes
human_execution_gate_activation_decision = approved
human_execution_gate_activation_decision_recorded = yes
gate_activation_record_status = candidate_pending_chatgpt_independent_acceptance
execution_gate_effective_activation = no_pending_chatgpt_acceptance
```

Only after independent ChatGPT acceptance is the intended governance state:

```text
execution_gate_status = activated_pending_separate_MVP_F08_execution_approval
execution_gate_activated = yes
actual_write_execution_approval_received = no
actual_write_execution_authorized_now = no
actual_evidence_layer_write_performed = no
attempt_reservation_created = no
persisted_real_candidate_record_created = no
production_evidenceitem_creation_authorized = false
production_evidenceitem_created = no
```

## 11. One-use, Expiry, Revocation, and Stop Rules

The activation decision is non-reusable and may govern only one later,
separately approved MVP-F08 public-writer invocation. The writer invocation
limit and mutating-attempt maximum are both one. A durable mutating attempt is
consumed only when the implementation commits its attempt reservation.

After the writer call starts, a second call, automatic retry, repair write, or
second mutating attempt is forbidden. Only the implementation's bounded
read-only ambiguity resolution is allowed.

Before writer invocation, the activation expires on any candidate field,
payload hash, gate binding, target identity, target authorization hash, target
label, service schema, mutation mode, initialization evidence, human-review,
or trust-boundary change. It also expires on explicit human revocation, a
superseding gate decision, or any requirement for production-object creation.
Revocation requires a new exact human decision.

## 12. MVP-F08 Stop-before-write Requirements

Any future F08 must stop before writer invocation unless it independently
recomputes every binding and verifies an exact match, confirms F07 independent
acceptance, receives a fresh exact F08 execution approval, proves the target
and service contracts remain unchanged without unauthorized discovery, and
arms its own one-call/no-retry latch. This document supplies no F08 approval
phrase or ready-to-sign template.

## 13. No-side-effect Proof

```text
docs_only = yes
runtime_accessed = no
payload_or_capture_receipt_read = no
target_or_initialization_receipt_accessed = no
source_package_or_row_read = no
writer_imported_or_called = no
attempt_reservation_created = no
candidate_or_reservation_write_performed = no
persistence_execution_performed = no
gate_runtime_side_effect_performed = no
production_object_created = no
code_or_test_changed = no
Project_Source_changed = no
```
