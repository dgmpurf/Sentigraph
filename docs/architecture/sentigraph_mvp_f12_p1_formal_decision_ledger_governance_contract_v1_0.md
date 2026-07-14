# Sentigraph MVP-F12-P1 Formal Decision Ledger Governance Contract v1.0

## 1. Contract status and authority

This document is the complete MVP-F12-P1 docs-only governance contract. It binds the accepted MVP-F11 human-review decision-capture surface to one future formal decision-ledger target, freezes the initialization and first-decision boundaries, and defines a later independent post-write audit. It does not initialize or inspect a target, access SQLite, invoke product code, capture a decision, or authorize MVP-F12-P2, MVP-F12-P3, or MVP-F12-P4.

Milestone classification: `planned_fixed_milestone_part_1_of_4`.

The exact authority for this document is:

`APPROVE_SENTIGRAPH_MVP_F12_P1_FORMAL_DECISION_LEDGER_GOVERNANCE_CONTRACT_DOCS_ONLY_PLANNED_FIXED_MILESTONE_PART_1_OF_4_BIND_ACCEPTED_MVP_F11_STATUS_SELECT_ONE_FORMAL_DECISION_LEDGER_INITIALIZATION_ARCHITECTURE_DEFINE_FORMAL_TARGET_STATE_INITIALIZATION_RECEIPT_FIRST_REAL_DECISION_GOVERNANCE_BOUNDARY_HUMAN_AUTHORITY_BOUNDARY_POST_WRITE_AUDIT_SEQUENCE_AND_FUTURE_P2_P3_P4_ALLOWLIST_REUSE_ACCEPTED_F11_SCHEMA_IDEMPOTENCY_APPEND_ONLY_RECEIPT_AND_ROUTE_CONTRACT_NO_CODE_CHANGE_NO_FORMAL_TARGET_INITIALIZATION_NO_SQLITE_ACCESS_NO_REAL_HUMAN_DECISION_CAPTURE_NO_FRONTEND_NO_F10_ROUTE_ADAPTER_HELPER_TARGET_WRITER_GOVERNED_RECORD_MUTATION_PRODUCTION_REVIEW_QUEUE_TRUST_UPGRADE_ANALYSIS_REPORT_CORRECTION_REVOCATION_EXPORT_DELIVERY_OR_PROJECT_SOURCE_CHANGE`

This authority permits one architecture document, bounded static inspection, docs/static validation, and ready-only Git finalization. It grants no authority for later implementation or execution. Each future phase requires the independent acceptance and fresh exact authorization gates frozen below.

## 2. Accepted baseline and frozen architecture

The contract binds repository identity `dgmpurf/Sentigraph`, branch `main`, accepted effective MVP-F11 commit `1300e10fba526c0d37f310a004e17a17a9c65420`, and these accepted static anchors:

| Anchor | Frozen value |
| --- | --- |
| F11-P1 contract blob | `29d3806a535680247713ae317c1d1c9097f69d06` |
| F11-P1 contract SHA-256 | `dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152` |
| Decision-ledger service blob | `b9d74ca5d3d593fbe27043dcb7db0a76e25d4056` |
| Internal decision route blob | `5dd5033f1de76cac86087a2e50d2a8fda74102ee` |
| Focused F11-P2 test blob | `02aaa25df98348caeb501e9f23ae593d0a590906` |
| API registration blob | `d9523f761537af0e7a08ce834d6e3b36c9117a24` |
| F11-P2-RC1 report blob | `f60a4775cd34d034c739be14e063230262cdf961` |

The accepted business-state anchor is that MVP-F11 and MVP-F11-P2 are `completed_and_independently_accepted`; all MVP-F12 phases were not started when this contract was authorized. The stated absence, non-initialization, and non-access of the formal target and the absence of an actual human-review decision are governance premises retained from the accepted brief, not claims produced by runtime observation in P1.

The selected architecture has four strictly separated milestones:

1. P1 freezes this docs-only contract.
2. P2 may add formal-target support and perform one bounded exact-empty initialization, emit its receipt, and stop.
3. P3 may, only after separate authorization, use a nonreusable repository-external runner to record one first real human-review decision through the service and then stop.
4. P4 may, only after separate authorization, use an independent repository-external direct SQLite read-only audit and emit its report, then stop.

The route is not the first-decision execution surface. Initialization authority cannot be reused for a decision, first-decision authority cannot be reused for a second decision or repair, and write authority cannot be reused for the independent audit.

## 3. Canonicalization and safe-hash rules

Both frozen objects below are canonicalized independently as JSON encoded as UTF-8, with non-ASCII characters preserved, object keys sorted lexicographically, and compact separators (comma and colon with no surrounding whitespace). The safe hash is the lowercase hexadecimal SHA-256 digest of those canonical bytes. Arrays preserve their declared order. All object keys and listed inputs are unique.

Physical filesystem paths, environment-derived paths, target contents, row data, raw evidence, protected payloads, secrets, credentials, and runtime observations are forbidden hash inputs. Repository-relative owner and allowlist paths and the exact logical target label are safe contract identifiers rather than physical target disclosure.

## 4. Formal-target identity

The identity object has exactly 19 ordered inputs. It freezes one table, no additional tables, the accepted 38-field decision schema, eight integer-backed Boolean columns, four canonical-JSON columns, three uniqueness columns, and plain insert-only append semantics. Its canonical safe hash is `4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202`.

<!-- TARGET_IDENTITY_OBJECT_BEGIN -->
```json
{
  "target_identity_schema": "sentigraph_governed_nonproduction_human_review_decision_ledger_formal_target_identity_v0_1",
  "target_identity_version": "0.1",
  "target_kind": "dedicated_local_sqlite_nonproduction_human_review_decision_ledger",
  "target_logical_label": "runtime/governed_nonproduction_human_review_decisions/review_decisions_v0_1.sqlite3",
  "table_count": 1,
  "additional_tables_allowed": false,
  "primary_table": "governed_nonproduction_human_review_decisions_v0_1",
  "schema_version": "0.1",
  "owner_module": "backend/app/services/governed_nonproduction_human_review_decision_ledger.py",
  "owner_class": "GovernedNonproductionHumanReviewDecisionLedger",
  "decision_schema": "sentigraph_governed_nonproduction_human_review_decision_record_v0_1",
  "decision_version": "0.1",
  "decision_fields": [
    "decision_schema",
    "decision_version",
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference",
    "ledger_scope",
    "decision_type",
    "decision_status",
    "recorded_at",
    "reviewer_role_label",
    "reviewer_authority_basis_label",
    "reviewer_identity_verified",
    "source_projection_schema",
    "source_projection_version",
    "source_projection_id",
    "source_projection_status",
    "source_projection_canonical_sha256",
    "source_outer_response_canonical_sha256",
    "persisted_record_id",
    "attempt_reservation_id",
    "candidate_identity_digest",
    "input_safe_hash",
    "gate_contract_safe_hash",
    "activation_decision_safe_hash",
    "record_snapshot_digest",
    "reservation_snapshot_digest",
    "decision_canonical_hash",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_changed",
    "production_case_changed",
    "downstream_runtime_called",
    "correction_or_revocation_performed",
    "deleted_or_updated",
    "allowed_follow_up_labels",
    "blocked_follow_up_labels",
    "warnings",
    "blockers"
  ],
  "integer_boolean_columns": [
    "reviewer_identity_verified",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_evidenceitem_changed",
    "production_case_changed",
    "downstream_runtime_called",
    "correction_or_revocation_performed",
    "deleted_or_updated"
  ],
  "canonical_json_columns": [
    "allowed_follow_up_labels",
    "blocked_follow_up_labels",
    "warnings",
    "blockers"
  ],
  "unique_columns": [
    "decision_id",
    "idempotency_key",
    "audit_receipt_reference"
  ],
  "ledger_scope": "governed_nonproduction_record_human_review_only",
  "decision_status": "recorded_append_only_nonproduction",
  "append_only_policy": "plain_insert_only_no_existing_row_mutation"
}
```
<!-- TARGET_IDENTITY_OBJECT_END -->

This identity is exclusive. Alternate targets, discovery, caller-supplied physical targets, environment overrides, aliases, additional tables, and schema substitution are forbidden. Any identity disagreement is a blocking classification, not a migration or repair opportunity.

## 5. P2 authorization contract

The authorization object has exactly 49 ordered inputs. It binds the repository and accepted F11 anchors, the formal-target identity hash, fresh phase gates, exact initialization-only operation, one-session resource limits, the exact 25-field receipt, and the three-file P2 allowlist. Its canonical safe hash is `de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d`.

<!-- TARGET_AUTHORIZATION_OBJECT_BEGIN -->
```json
{
  "authorization_contract_schema": "sentigraph_governed_nonproduction_human_review_decision_ledger_formal_target_authorization_contract_v0_1",
  "authorization_contract_version": "0.1",
  "architecture_id": "exact_formal_target_profile_with_initialization_only_operation_separate_nonreusable_first_decision_operation_and_independent_read_only_post_write_audit",
  "milestone_id": "MVP-F12-P2",
  "repository_identity": "dgmpurf/Sentigraph",
  "required_branch": "main",
  "repository_root_binding": "git_top_level_with_required_repository_identity_and_anchor_blobs",
  "accepted_f11_p1_contract_blob": "29d3806a535680247713ae317c1d1c9097f69d06",
  "accepted_f11_p1_contract_sha256": "dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152",
  "accepted_effective_f11_commit": "1300e10fba526c0d37f310a004e17a17a9c65420",
  "accepted_decision_ledger_service_blob": "b9d74ca5d3d593fbe27043dcb7db0a76e25d4056",
  "accepted_internal_decision_route_blob": "5dd5033f1de76cac86087a2e50d2a8fda74102ee",
  "accepted_focused_test_blob": "02aaa25df98348caeb501e9f23ae593d0a590906",
  "target_identity_safe_hash": "4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202",
  "independent_p1_acceptance_required": true,
  "fresh_exact_p2_user_approval_required": true,
  "new_p2_goal_required": true,
  "formal_initialization_operation_symbol": "initialize_exact_formal_governed_nonproduction_human_review_decision_ledger",
  "authorized_operation": "exact_empty_formal_target_initialization_only",
  "target_resolution_mode": "internal_exact_logical_label_only",
  "required_initial_state": "contract_defined_uninitialized",
  "allowed_success_state": "initialized_exact_empty",
  "allowed_preexistence_classifications": [
    "absent",
    "existing_exact_empty"
  ],
  "blocked_preexistence_classifications": [
    "existing_nonempty",
    "schema_mismatch_or_unrelated_table",
    "target_identity_mismatch"
  ],
  "formal_target_access_session_maximum": 1,
  "sqlite_connection_open_maximum": 1,
  "sqlite_connection_reopen_maximum": 0,
  "schema_ddl_statement_count_maximum": 1,
  "decision_table_dml_statement_count_maximum": 0,
  "decision_insert_maximum": 0,
  "decision_writer_invocation_maximum": 0,
  "route_invocation_maximum": 0,
  "automatic_retry_allowed": false,
  "caller_supplied_physical_target_allowed": false,
  "environment_target_override_allowed": false,
  "first_real_decision_allowed": false,
  "commit_ambiguity_policy": "pause_without_automatic_retry_or_first_decision",
  "unavailable_observation_policy": "null_not_fabricated_zero",
  "initialization_receipt_schema": "sentigraph_governed_nonproduction_human_review_decision_ledger_initialization_receipt_v0_1",
  "initialization_receipt_version": "0.1",
  "initialization_receipt_fields": [
    "receipt_schema",
    "receipt_version",
    "outcome",
    "target_kind",
    "target_logical_label",
    "target_identity_safe_hash",
    "target_authorization_contract_safe_hash",
    "target_preexistence_classification",
    "initialization_action",
    "schema_version",
    "primary_table",
    "sqlite_connection_open_count",
    "sqlite_connection_reopen_count",
    "schema_ddl_statement_count",
    "decision_table_dml_statement_count",
    "decision_row_count",
    "exact_schema_verified",
    "exact_empty_verified",
    "integrity_result",
    "final_sidecar_count",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "production_ready",
    "warnings",
    "blockers"
  ],
  "initialization_receipt_outcomes": [
    "initialized_exact_empty_formal_decision_ledger",
    "verified_existing_exact_empty_formal_decision_ledger",
    "blocked_existing_nonempty_formal_decision_ledger",
    "blocked_formal_decision_ledger_schema_mismatch",
    "blocked_formal_decision_ledger_target_identity_mismatch",
    "paused_formal_decision_ledger_initialization_ambiguous",
    "bounded_formal_decision_ledger_initialization_failure"
  ],
  "p2_repository_file_allowlist": [
    "backend/app/services/governed_nonproduction_human_review_decision_ledger.py",
    "backend/app/tests/test_mvp_f12_p2_formal_decision_ledger_initialization.py",
    "docs/health/sentigraph_mvp_f12_p2_formal_decision_ledger_initialization_report_v1_0.md"
  ],
  "repository_external_runner_required": true,
  "repository_external_runner_execution_maximum": 1,
  "repository_external_runner_retained_after_receipt": false,
  "human_review_required": true,
  "no_automatic_trust_upgrade": true,
  "production_ready": false
}
```
<!-- TARGET_AUTHORIZATION_OBJECT_END -->

P2 may resolve only the internally owned logical target and classify it within the same single access session. `absent` permits the one bounded schema-initialization action; `existing_exact_empty` permits verification without schema mutation. Every success must prove the exact schema, an empty decision table, integrity success, and zero final sidecars. An existing nonempty target, schema mismatch or unrelated table, identity mismatch, or ambiguous commit observation must block or pause exactly as represented by the receipt outcomes. No automatic retry, reopen, repair, migration, first decision, or route call is permitted.

On successful P2 initialization or verification, the receipt must report DML count `0`, decision row count `0`, both exact-verification flags `true`, final sidecar count `0`, `human_review_required=true`, `no_automatic_trust_upgrade=true`, `production_ready=false`, and empty warning and blocker arrays. An observation unavailable within the bounded session is `null`; it must never be fabricated as zero or success. Failure receipts retain the observations safely available before the stop boundary and use warnings and blockers to explain the terminal classification.

## 6. State machine

Transitions require the preceding phase's accepted receipt or report, independent acceptance, a fresh exact phase authorization, and a new Goal. There are exactly four normal states:

<!-- STATE_MACHINE_NORMAL_BEGIN -->
1. `contract_defined_uninitialized`
2. `initialized_exact_empty`
3. `first_exact_decision_recorded`
4. `one_exact_decision_independently_audited`
<!-- STATE_MACHINE_NORMAL_END -->

The only normal transitions are 1 to 2 in P2, 2 to 3 in P3, and 3 to 4 in P4. Skipping, combining, replaying, or reversing a transition is forbidden. There are exactly six blocking or paused terminal states:

<!-- STATE_MACHINE_TERMINAL_BEGIN -->
1. `blocked_preexisting_nonempty`
2. `blocked_schema_mismatch`
3. `blocked_target_identity_mismatch`
4. `paused_initialization_commit_ambiguity`
5. `paused_first_decision_commit_ambiguity`
6. `blocked_post_write_integrity_mismatch`
<!-- STATE_MACHINE_TERMINAL_END -->

A blocked or paused state permits only evidence-preserving stop and a new explicitly authorized recovery contract. It does not imply retry, repair, mutation, or continuation authority.

## 7. P3 first-real-decision governance boundary

P3 begins only from accepted state 2 and requires independent P2 acceptance, a fresh exact P3 user authorization, and a new P3 Goal. The one permitted first decision type is `keep_pending_human_review`; `request_more_governance_review` is expressly blocked for the first formal decision. The reviewer labels are fixed as `self_declared_project_owner_role` and `authority_basis_not_independently_validated`, and `reviewer_identity_verified` is `false`. These values record a bounded human decision without upgrading identity, trust, production readiness, or evidence status.

The future one-time service operation symbol is `record_first_exact_formal_governed_nonproduction_human_review_decision`. It must be invoked by one UTF-8 repository-external runner through the service directly, never through the route. The runner may execute once, the decision writer may be invoked once, and at most one decision insert may occur. Route calls, automatic retry, repair, a second decision, correction, revocation, deletion, update, governed-record mutation, production mutation, frontend work, and downstream runtime calls remain forbidden. Commit ambiguity pauses with no automatic replay.

The exact P3 repository allowlist has three files:

<!-- P3_FILE_ALLOWLIST_BEGIN -->
```json
[
  "backend/app/services/governed_nonproduction_human_review_decision_ledger.py",
  "backend/app/tests/test_mvp_f12_p3_first_formal_human_review_decision.py",
  "docs/health/sentigraph_mvp_f12_p3_first_formal_human_review_decision_report_v1_0.md"
]
```
<!-- P3_FILE_ALLOWLIST_END -->

The external runner is never added to the repository and must be removed after its receipt is captured. P3 must stop after the first-decision receipt and report; it cannot perform P4.

## 8. P4 independent post-write audit boundary

P4 begins only from accepted state 3 and requires independent P3 acceptance, a fresh exact P4 user authorization, and a new P4 Goal. It uses one repository-external direct SQLite read-only audit runner, separate from the P3 writer runner and without importing or invoking the ledger service or route. The audit verifies the frozen target identity, exact schema and table set, integrity, exactly one decision row, canonical field and Boolean/JSON encodings, uniqueness invariants, decision and receipt hash linkage, append-only posture, and zero unexpected sidecars. It must not replay a decision, invoke a writer, mutate a row or schema, repair anything, call a route, or touch frontend or production surfaces.

The exact P4 repository allowlist has one file:

<!-- P4_FILE_ALLOWLIST_BEGIN -->
```json
[
  "docs/health/sentigraph_mvp_f12_p4_independent_formal_decision_ledger_post_write_audit_report_v1_0.md"
]
```
<!-- P4_FILE_ALLOWLIST_END -->

The external audit runner is never added to the repository and must be removed after the report evidence is captured. An integrity, identity, schema, row-count, canonicalization, uniqueness, linkage, append-only, or sidecar mismatch enters `blocked_post_write_integrity_mismatch` and stops without mutation.

## 9. Future validation contracts

P2 synthetic validation must statically and deterministically cover identity-object canonicalization, both safe hashes, exact schema ownership, exact-empty initialization, already-exact-empty verification, every blocked or paused preexistence classification, all seven receipt outcomes, receipt field order and null semantics, one-session counters, no DML, no writer, no route, no retry, and no caller or environment target substitution. Exact-target execution, if later authorized, is limited to the single external runner execution and must compare the emitted receipt against every P2 invariant before stopping.

P3 synthetic validation must cover request validation, the fixed first-decision values, all 38 decision fields, idempotency inputs, canonical decision hashing, receipt linkage, insert-only behavior, ambiguity stop behavior, and rejection of alternate decision types, repeat calls, route use, updates, deletions, correction, and revocation. Future exact-target execution must start from an accepted exact-empty P2 receipt, use the one external runner once, validate the one result, emit the health report, and stop without audit reuse.

P4 validation is the repository-external read-only exact-target audit itself, preceded by static validation of the one-file report allowlist and audit assertions. It must independently recompute safe hashes and linkage from read-only observations, distinguish unavailable observations from zero, record every check and counter in the report, and stop. No product test, build, browser, route, service, writer, target, payload, source-reader, or SQLite execution occurs in P1.

## 10. Product and side-effect boundaries

All four phases remain nonproduction and human-review-only. Nothing in this contract changes a production EvidenceItem or case, upgrades trust, calls downstream runtime, authorizes an analysis or report pipeline, performs correction or revocation, exports or delivers data, creates a production Review Queue, changes Project Source, or changes frontend behavior. The accepted internal route contract is retained for compatibility but is excluded from P2 initialization, P3 first-decision execution, and P4 audit execution.

P1 creates only this Markdown file. Formal-target access count, SQLite access count, route invocation count, ledger-service invocation count, decision-writer invocation count, decision capture count, F10 adapter/helper/target/writer invocation counts, frontend execution count, and product-runtime execution count are all `0`. No target, payload, receipt artifact, raw evidence, row data, secret, or credential was read. No tag or release is authorized.

## 11. Phase acceptance and handoff

P1 is ready only when docs/static checks prove that this is the sole repository change; the authority literal occurs once; canonical object input counts, key uniqueness, hashes, receipt field and outcome cardinalities, states, and future allowlists match this contract; Markdown fences and whitespace are valid; and no forbidden physical path, raw query, placeholder, mojibake, runtime claim, or implementation overclaim appears.

Successful P1 completion authorizes only handoff for independent review. It does not advance the state machine and does not grant P2 authority. P2, P3, and P4 each remain unstarted until their preceding acceptance, fresh exact authorization, and new Goal requirements are satisfied.

## 12. RC1 administrative and governance completeness

<!-- RC1_ADMINISTRATIVE_COMPLETENESS_BEGIN -->

### 12.1 Candidate decision and phase status

This section records candidate contract completeness only. It does not self-attest the final RC1 Git commit or the terminal Goal receipt; the external terminal receipt supplies that evidence after ready-only Git finalization.

```text
decision = ready
privacy_issue_stop = no

MVP_F12_P1_RC1_status = candidate_completed_pending_chatgpt_acceptance
effective_MVP_F12_P1_status = candidate_repaired_pending_chatgpt_acceptance

MVP_F12_P2_eligibility_candidate_after_chatgpt_acceptance = yes
MVP_F12_P2_authorized = no
MVP_F12_P2_executed = no
MVP_F12_P3_authorized = no
MVP_F12_P3_executed = no
MVP_F12_P4_authorized = no
MVP_F12_P4_executed = no
```

P2 remains unauthorized. No later phase is represented as implemented, executed, accepted, or complete.

### 12.2 Exact Goal lifecycle

```text
original_P1_goal_created = yes
original_P1_goal_completed = yes
original_P1_goal_reused_for_RC1 = no

RC1_goal_created = yes
RC1_goal_activated = yes
```

The RC1 Goal is separate from the completed original P1 Goal and cannot be replaced or reused by a later phase.

### 12.3 Prompt accounting

```text
before_RC1:
consumed_engineering_prompts_since_v1_3 = 17
consumed_fixed_prompts_since_v1_3 = 9
consumed_conditional_prompts_since_v1_3 = 6
consumed_risk_prompts_since_v1_3 = 2
remaining_fixed_prompts = 5
remaining_conditional_allowance = 0
remaining_risk_buffer = 0

after_RC1_goal_activation:
consumed_engineering_prompts_since_v1_3 = 18
consumed_fixed_prompts_since_v1_3 = 10
consumed_conditional_prompts_since_v1_3 = 6
consumed_risk_prompts_since_v1_3 = 2
remaining_fixed_prompts = 4
remaining_conditional_allowance = 0
remaining_risk_buffer = 0
```

### 12.4 Inspected static anchors

The RC1 inspection was bounded to the existing contract, its accepted Git anchor, and the retained accepted F11 static findings. It did not inspect a runtime target or row data.

| Inspected anchor | Exact value |
| --- | --- |
| Accepted effective F11 commit | `1300e10fba526c0d37f310a004e17a17a9c65420` |
| F11-P1 contract blob | `29d3806a535680247713ae317c1d1c9097f69d06` |
| F11-P1 contract SHA-256 | `dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152` |
| Decision-ledger service blob | `b9d74ca5d3d593fbe27043dcb7db0a76e25d4056` |
| Internal route blob | `5dd5033f1de76cac86087a2e50d2a8fda74102ee` |
| Focused test blob | `02aaa25df98348caeb501e9f23ae593d0a590906` |
| API registration blob | `d9523f761537af0e7a08ce834d6e3b36c9117a24` |
| F11-P2-RC1 report blob | `f60a4775cd34d034c739be14e063230262cdf961` |
| Historical P1 commit | `95cace0b2a5a71a99833af912dfc874c96ac977f` |
| Current pre-RC1 P1 contract blob | `4fd220fb5a7de1188a9a6be9f52d8b28b78580d9` |
| Current pre-RC1 P1 contract SHA-256 | `25950130529a6602724bf9439ab73094af7741b3f72fc286060338990d5dd17f` |

### 12.5 Rejected architectures

<!-- RC1_REJECTED_ARCHITECTURES_BEGIN -->

1. `rejected_combine_initialization_and_first_decision_in_P2` — it would destroy the exact-empty initialization boundary and reuse P2 authority for a real write.
2. `rejected_internal_HTTP_route_as_first_formal_write_surface` — the first formal write requires a one-time nonreusable direct-service binding that the route does not provide.
3. `rejected_bind_existing_internal_route_factory_to_formal_target` — it would expose formal-target selection to a reusable request surface outside the frozen phase boundary.
4. `rejected_caller_supplied_physical_SQLite_target` — caller-selected storage permits substitution and breaks the internally owned logical-target identity.
5. `rejected_target_discovery_globbing_aliases_or_environment_substitution` — discovery and substitution make target resolution ambiguous and non-canonical.
6. `rejected_generic_case_or_evidence_store` — a shared store would violate the dedicated ledger schema, scope, and isolation contract.
7. `rejected_commit_one_time_P2_P3_or_P4_runners` — committed runners would remain reusable instead of repository-external and disposable after their receipts.
8. `rejected_replay_writer_during_P4_idempotency_proof` — a writer replay is a mutation-capable action and cannot constitute an independent read-only audit.
9. `rejected_frontend_controls_before_independent_P4_audit` — controls would expose a formal decision surface before independent integrity acceptance.
10. `rejected_self_declared_authority_as_verified_identity` — a role declaration and unvalidated authority basis cannot prove reviewer identity.

<!-- RC1_REJECTED_ARCHITECTURES_END -->

### 12.6 Exact P1 no-side-effect proof

```text
docs_only = yes
backend_code_changed = no
frontend_code_changed = no
tests_changed = no
route_executed = no
service_invoked = no
formal_target_access_count = 0
SQLite_access_count = 0
decision_writer_invocation_count = 0
decision_capture_count = 0
F10_runtime_call_count = 0
production_or_downstream_action_count = 0
Project_Source_changed = no
tag_or_release_created = no
```

### 12.7 Source recommendation and next boundary

Only after independent acceptance of RC1, the Source recommendation is:

```text
Canonical 00 = replace
Canonical 03 = replace
Canonical 09 = replace
Canonical 08 = no change until P2 runtime status changes
Canonical 05 = no change
Source 11 = no change
```

Project Source remains unchanged during RC1.

```text
next_boundary = ChatGPT independent acceptance of F12-P1-RC1, Source synchronization, then one fresh exact P2 authorization
```

P2 remains unauthorized at this boundary.

<!-- RC1_ADMINISTRATIVE_COMPLETENESS_END -->

## 13. Exact P3 receipt and activation binding contract

<!-- P3_ACTIVATION_BINDING_CONTRACT_BEGIN -->

P3 may approach its writer boundary only after independently accepted P2 initialization evidence proves the formal target is in the required exact-empty state. The future P3 authority must bind exactly the following 23 fields in this order:

<!-- P3_ACTIVATION_BINDING_FIELDS_BEGIN -->
1. `accepted_f11_p1_contract_blob`
2. `accepted_f11_p1_contract_sha256`
3. `accepted_effective_f11_commit`
4. `accepted_decision_ledger_service_blob`
5. `accepted_request_schema`
6. `accepted_request_version`
7. `accepted_decision_schema`
8. `accepted_decision_version`
9. `accepted_ledger_scope`
10. `accepted_decision_status`
11. `target_identity_safe_hash`
12. `target_authorization_contract_safe_hash`
13. `independently_accepted_p2_initialization_receipt_canonical_sha256`
14. `required_formal_target_state`
15. `first_real_decision_type`
16. `reviewer_role_label`
17. `reviewer_authority_basis_label`
18. `reviewer_identity_verified`
19. `p3_activation_binding_safe_hash`
20. `p3_activation_binding_nonreusable`
21. `formal_writer_invocation_limit`
22. `automatic_retry_allowed`
23. `route_invocation_limit`
<!-- P3_ACTIVATION_BINDING_FIELDS_END -->

The exact values already frozen by P1 are:

```text
accepted_f11_p1_contract_blob = 29d3806a535680247713ae317c1d1c9097f69d06
accepted_f11_p1_contract_sha256 = dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152
accepted_effective_f11_commit = 1300e10fba526c0d37f310a004e17a17a9c65420
accepted_decision_ledger_service_blob = b9d74ca5d3d593fbe27043dcb7db0a76e25d4056
accepted_request_schema = sentigraph_governed_nonproduction_human_review_decision_request_v0_1
accepted_request_version = 0.1
accepted_decision_schema = sentigraph_governed_nonproduction_human_review_decision_record_v0_1
accepted_decision_version = 0.1
accepted_ledger_scope = governed_nonproduction_record_human_review_only
accepted_decision_status = recorded_append_only_nonproduction
target_identity_safe_hash = 4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202
target_authorization_contract_safe_hash = de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d
required_formal_target_state = initialized_exact_empty
first_real_decision_type = keep_pending_human_review
reviewer_role_label = self_declared_project_owner_role
reviewer_authority_basis_label = authority_basis_not_independently_validated
reviewer_identity_verified = false
p3_activation_binding_nonreusable = true
formal_writer_invocation_limit = 1
automatic_retry_allowed = false
route_invocation_limit = 0
```

P1 cannot supply the two future evidence values. Their non-fabricated status is recorded as:

```text
independently_accepted_p2_initialization_receipt_canonical_sha256 = future_required_lowercase_64_hex_not_yet_available
p3_activation_binding_safe_hash = future_required_lowercase_64_hex_not_yet_available
```

The future P3 authorization must replace each status with exactly one lowercase 64-hex SHA-256 value and bind both values explicitly. The initialization receipt hash covers the exact independently accepted 25-field canonical receipt object; it never hashes a report, filename, physical path, or terminal summary.

`P3_PRE_WRITER_HASH_GATE`: P3 must stop before writer invocation if either future hash is absent, malformed, not independently accepted, mismatched, substituted, or reused. The activation binding identifies only the first `keep_pending_human_review` decision, binds the exact accepted P2 receipt hash and both formal-target hashes, is nonreusable, and authorizes at most one writer invocation and one INSERT. It authorizes no automatic retry, repair, second decision, route call, or frontend action.

<!-- P3_ACTIVATION_BINDING_CONTRACT_END -->

## 14. Exact P4 direct recomputation contract

<!-- P4_DIRECT_RECOMPUTATION_CONTRACT_BEGIN -->

P4 is an independent repository-external direct SQLite read-only audit. It reads actual stored columns and derives identity and integrity values itself. `P4_UNTRUSTED_STORED_VALUES`: it must not trust the stored decision_canonical_hash, stored idempotency_key, stored decision_id, stored audit_receipt_reference, the P3 service result alone, or a report summary alone.

P4 reconstructs the exact 19-field idempotency object in this order:

<!-- P4_IDEMPOTENCY_FIELDS_BEGIN -->
1. `request_schema`
2. `request_version`
3. `decision_type`
4. `reviewer_role_label`
5. `reviewer_authority_basis_label`
6. `source_projection_schema`
7. `source_projection_version`
8. `source_projection_id`
9. `source_projection_status`
10. `source_projection_canonical_sha256`
11. `source_outer_response_canonical_sha256`
12. `persisted_record_id`
13. `attempt_reservation_id`
14. `candidate_identity_digest`
15. `input_safe_hash`
16. `gate_contract_safe_hash`
17. `activation_decision_safe_hash`
18. `record_snapshot_digest`
19. `reservation_snapshot_digest`
<!-- P4_IDEMPOTENCY_FIELDS_END -->

The first two fields use the accepted F11 request constants bound by P3; every row-derived field uses its actual SQLite column. P4 canonicalizes the object with `ensure_ascii = false`, `sort_keys = true`, compact separators, UTF-8 encoding, and SHA-256 lowercase hexadecimal output.

P4 independently derives:

```text
recomputed_idempotency_key = SHA-256 of the exact 19-field canonical object
recomputed_decision_id = "ghrd-" + the first 32 lowercase hexadecimal characters of recomputed_idempotency_key
recomputed_audit_receipt_reference = "ghrd-receipt-" + the first 32 lowercase hexadecimal characters of recomputed_idempotency_key
```

P4 compares all three recomputed values with the actual stored `idempotency_key`, `decision_id`, and `audit_receipt_reference` columns.

P4 then reconstructs the complete canonical decision object from all actual canonical columns in the frozen 38-field decision schema. It normalizes the eight SQLite Boolean columns to canonical Boolean values and parses the four canonical-JSON columns to their canonical values. It recomputes `decision_canonical_hash` as the SHA-256 lowercase hexadecimal digest of the complete canonical decision object excluding only the decision_canonical_hash field, then compares that result with the actual stored hash column.

The independent audit also verifies:

```text
decision_type = keep_pending_human_review
ledger_scope = governed_nonproduction_record_human_review_only
decision_status = recorded_append_only_nonproduction
reviewer_identity_verified = false
exact_row_count = 1
unrelated_row_count = 0
unexpected_sidecar_count = 0
```

Any mismatch is classified `blocked_post_write_integrity_mismatch`. P4 then stops without a route or service call, writer invocation, mutation, retry, repair, deletion, update, or second decision.

<!-- P4_DIRECT_RECOMPUTATION_CONTRACT_END -->
