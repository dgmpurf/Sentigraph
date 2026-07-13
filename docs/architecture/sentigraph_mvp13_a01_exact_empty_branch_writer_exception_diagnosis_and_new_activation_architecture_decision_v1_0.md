# Sentigraph MVP13-A01 Exact-empty Branch Writer-exception Diagnosis and New Activation Architecture Decision v1.0

## 1. Decision

- phase = MVP13-A01
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- MVP13_A01_status = candidate_completed_pending_chatgpt_acceptance
- diagnosis_outcome = strongest_deterministic_pre_reservation_candidate_identified_historical_exact_callsite_unproven
- selected_repair_architecture = reservation_target_logical_label_validation_domain_separation
- historical_root_cause_proven = no
- exact_historical_exception_callsite_proven = no
- runtime_target_accessed = no
- helper_invoked = no
- writer_invoked = no
- mutation_performed = no

This decision accepts the current exact-empty state as bounded runtime evidence and
selects one narrow synthetic repair architecture. It does not authorize repair,
activation, persistence execution, production use, or downstream use.

## 2. Goal Lifecycle and Model Exposure

- goal_created = yes
- goal_activated = yes
- goal_active_state_observed = yes
- goal_resumed_from_existing_paused_state = yes
- goal_recreated_after_resume = no
- goal_terminal_completion_state = candidate_complete_after_document_and_static_validation
- actual_model_used = current OpenAI Codex GPT-5 session model; exact deployment identifier not exposed

## 3. Starting State and Approval

- repository_identity = dgmpurf/Sentigraph
- branch = main
- starting_commit = 55c3d21e19bae9c45ec0416ed2f8acb83c1802d7
- starting_commit_message = Record MVP13-F02 exact-target read-only audit
- origin_main_matched_starting_commit = yes
- starting_ahead_behind = 0/0
- starting_worktree_clean = yes
- exact_A01_approval_match = yes
- Baseline_v1_3_effective = yes
- Project_Source_synchronization_through_accepted_MVP13_F02_acknowledged = yes

## 4. Prompt Accounting

- consumed_engineering_prompts_since_v1_3_baseline = 4
- consumed_fixed_prompts_since_v1_3 = 2
- consumed_conditional_prompts_since_v1_3 = 1
- consumed_risk_prompts_since_v1_3 = 1
- remaining_fixed_prompts = 12
- remaining_conditional_allowance = 5
- remaining_risk_buffer = 1

The resumed Goal does not consume or create another Prompt.

## 5. Evidence Classes

Only the following evidence classes are used in this decision:

- `proven_runtime_state`: a bounded fact established by the accepted MVP13-F02
  read-only audit.
- `deterministic_current_code_path`: behavior established from committed source,
  AST order, and language evaluation order without executing product code.
- `historically_code_consistent_but_exact_callsite_unproven`: current deterministic
  behavior also existed byte-for-byte at the historical execution anchor, but no
  preserved historical receipt, exception class, or exact callsite proves that it
  was the actual terminating path.
- `possible_but_not_specifically_supported`: a source-visible path compatible with
  an empty state but not selected by preserved evidence.
- `excluded_by_current_exact_empty_state`: a retained durable reservation or
  governed record state that the accepted exact-empty audit rules out now.

Deterministic current-code behavior is not historical-callsite proof.

## 6. Frozen Proven Runtime State

Evidence class: `proven_runtime_state`.

- MVP13_F02_status = completed_and_independently_accepted
- helper_result_canonical_sha256 = 3d7b1487cd7a506e36064b94a0c3327897fe669db663086dee96b61f493f14fa
- target_state_outcome = exact_empty
- classification = A
- record_count_class = exact_0
- reservation_count_class = exact_0
- actual_implementation_mutating_attempt_consumed = no
- actual_attempt_reservation_state = exact_absent
- actual_governed_record_state = exact_absent

The accepted audit also established successful sidecar preflight and postflight,
SQLite URI read-only mode, connection-local query-only posture, restrictive
authorizer posture, and the exact two-table schema contract.

The exact-empty result proves that no durable reservation and no governed record
currently exist. It does not prove:

- the exact exception class;
- the exact historical callsite;
- whether a transaction was briefly opened and rolled back;
- whether a non-durable filesystem or connection action occurred historically;
- that historical MVP12-F02 succeeded; or
- that the consumed historical approval may be retried.

## 7. Historical MVP12-F02 Boundary

- historical_MVP12_F02_status = terminal_needs_fix
- historical_MVP12_F02_reclassified_as_success = no
- historical_public_writer_invocation_count = 1
- historical_writer_retry_count = 0
- historical_writer_receipt_returned = no
- F07_activation_execution_use_consumed = yes
- fresh_MVP12_F02_writer_use_consumed = yes
- old_activation_or_writer_use_reusable = no

The accepted current state narrows the durable outcome but does not rewrite the
historical terminal result.

## 8. Historical Source Continuity

Inspected file:

- `backend/app/services/governed_nonproduction_evidence_persistence.py`

Historical execution anchor:

- commit = 441602dd459c70ac7ff0cbecc803e1fa5edee8dd
- Git_blob_SHA = e7fddfb20d47625cdc042344bf2faf60462b3c7b
- SHA_256 = ca5021eb28779685a3d5c0ec42874528025baaaae7c7de3026528d8e0c10e99c
- byte_count = 85165

Current anchor:

- commit = 55c3d21e19bae9c45ec0416ed2f8acb83c1802d7
- Git_blob_SHA = e7fddfb20d47625cdc042344bf2faf60462b3c7b
- SHA_256 = ca5021eb28779685a3d5c0ec42874528025baaaae7c7de3026528d8e0c10e99c
- byte_count = 85165

- historical_current_file_byte_identical = yes
- relevant_command_order_materially_identical = yes
- relevant_reservation_validation_materially_identical = yes
- relevant_logical_label_validation_materially_identical = yes
- relevant_public_writer_order_materially_identical = yes

This proves source continuity. It does not prove which source-visible exception
path terminated the historical invocation.

## 9. Source-confirmed Public Writer Call Order

Evidence class: `deterministic_current_code_path`.

The source and AST establish this order:

1. `create_governed_nonproduction_evidence_record` evaluates the private UTC
   timestamp call used as the command builder argument.
2. `build_governed_nonproduction_evidence_persistence_command` validates the safe
   payload and expected identity.
3. The builder derives the candidate identity digest, validates gate binding,
   validates activation binding, validates the dedicated logical target label,
   checks the single mutation-attempt number, and validates the timestamp.
4. The builder derives stable identifiers and constructs the record and
   reservation, including their canonical hashes.
5. The public writer passes the derived command to
   `_persist_rederived_governed_nonproduction_command`.
6. Persistence calls `_validate_command` before examining store target binding,
   store configuration, existing target state, or any SQLite connection.
7. `_validate_command` checks command fields, schema, mode, dedicated logical
   label, attempt number, identity, gate, activation, derived identifiers, and
   then calls `_validate_record` followed by `_validate_reservation`.
8. Only after command revalidation returns can persistence compare the store
   logical label, enforce the candidate scope, and require enabled store
   configuration.
9. Only after those checks can existing state be opened read-only and resolved.
10. Only after existing-state resolution can the durable reservation phase begin.
11. Only after a verified reservation commit can the post-reservation boundary
    run and the base-record phase begin.

No product function was imported or executed to establish this order.

## 10. Bounded Pre-reservation Exception-path Inventory

All rows are bounded to paths before a proven durable reservation commit. No row
claims the historical terminating callsite.

| candidate_id | source_stage | before_or_after_any_SQLite_open | before_or_after_durable_reservation_commit | can_leave_exact_empty_state | deterministic_with_frozen_exact_inputs | specific_supporting_evidence | evidence_class | historical_exact_callsite_proven |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PX-01 | private timestamp acquisition | before | before | yes | no | AST places timestamp evaluation before command construction; no historical callsite evidence survives | possible_but_not_specifically_supported | no |
| PX-02 | payload validation | before | before | yes | no failure supported | historical safe report records payload validation as passed | possible_but_not_specifically_supported | no |
| PX-03 | expected-identity comparison | before | before | yes | no failure supported | historical safe report records identity binding as passed | possible_but_not_specifically_supported | no |
| PX-04 | gate-contract binding | before | before | yes | no failure supported | historical safe report records gate binding as passed | possible_but_not_specifically_supported | no |
| PX-05 | activation binding | before | before | yes | no failure supported | historical safe report records activation binding as passed | possible_but_not_specifically_supported | no |
| PX-06 | builder-level dedicated logical-label validation | before | before | yes | no | exact label satisfies the dedicated slash-bearing label domain | deterministic_current_code_path | no |
| PX-07 | mutation-attempt-number validation | before | before | yes | no | historical latch records attempt number 1 and source maximum is 1 | deterministic_current_code_path | no |
| PX-08 | command revalidation | before | before | yes | yes at current-code level | `_validate_command` deterministically reaches record then reservation validation before store access | historically_code_consistent_but_exact_callsite_unproven | no |
| PX-09 | record validation inside command revalidation | before | before | yes | no specific failure supported | record is constructed by the same builder after safe input binding; no preserved record-validator failure evidence | possible_but_not_specifically_supported | no |
| PX-10 | reservation validation inside command revalidation | before | before | yes | yes | slash-bearing label is tested by generic opaque-token validation before dedicated label validation | historically_code_consistent_but_exact_callsite_unproven | no |
| PX-11 | store target-logical-label comparison | before | before | yes | no failure supported | historical safe report records target binding as passed; this check is after command revalidation | deterministic_current_code_path | no |
| PX-12 | disabled or invalid store configuration | before | before | yes | not established | source check exists after command and scope validation but was not reached by the selected deterministic candidate | possible_but_not_specifically_supported | no |
| PX-13 | initial read-only target open or snapshot | after open attempt | before | yes | not established | source opens existing state only after store configuration; current healthy audit does not prove historical open behavior | possible_but_not_specifically_supported | no |
| PX-14 | durable reservation transaction failure before commit | after | before | yes | not established | source contains pre-commit rollback and ambiguous-unproven paths; no historical receipt identifies one | possible_but_not_specifically_supported | no |

The current exact-empty result assigns `excluded_by_current_exact_empty_state` to
any claim that a reservation or governed record remains durably present now. It
does not exclude transient historical work that left no durable state.

## 11. Slash-bearing Logical-label Validation Mismatch

Exact logical label under review:

- `runtime/governed_nonproduction_evidence_persistence/evidence_records_v0_1.sqlite3`

The six required findings are source-proven:

1. The dedicated logical-label regular-expression domain permits repository-
   relative slash-bearing labels and independently rejects absolute, backslash,
   drive-colon, and traversal forms.
2. `_validate_reservation` includes `target_logical_label` in the generic
   opaque-token field set.
3. The generic opaque-token domain does not permit `/`, so the exact valid label
   is rejected there before the dedicated logical-label validator is called.
4. `_validate_command` calls `_validate_reservation` before persistence can check
   store target binding, configuration, existing state, or create a durable
   reservation.
5. The accepted read-only helper reconstructs reservation columns locally with
   the same field, schema, version, hash, timestamp, opaque-field, and logical-
   label contracts, but excludes `target_logical_label` from the generic opaque
   set and applies the dedicated validator to it. The frozen F01 health report
   explicitly records this domain separation as the response to the mismatch.
6. The persistence source at the historical execution anchor and current anchor
   is byte-identical.

Classification:

- strongest_deterministic_candidate = reservation_target_logical_label_validation_domain_and_order_mismatch
- candidate_evidence_class = historically_code_consistent_but_exact_callsite_unproven
- candidate_confidence = high_code_derived_not_direct_historical_callsite_proof
- historical_root_cause_proven = no
- exact_historical_exception_callsite_proven = no

The source makes the mismatch deterministic for a command carrying the exact
slash-bearing label. The absence of the historical exception class, stack, and
receipt prevents elevating that code-derived candidate to proven historical root
cause.

## 12. Selected A02 Synthetic Repair Architecture

- selected_repair_architecture = reservation_target_logical_label_validation_domain_separation
- planned_milestone = MVP13-A02
- title = Narrow Synthetic Reservation Logical-label Validation-order Repair
- MVP13_A02_classification = conditional
- MVP13_A02_prompt_count = 1
- MVP13_A02_status = not_started
- MVP13_A02_authorized = no
- MVP13_A02_executed = no
- MVP13_A02_eligible_after_chatgpt_acceptance = yes

Exact future implementation scope:

- `backend/app/services/governed_nonproduction_evidence_persistence.py`
- `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
- `docs/health/sentigraph_mvp13_a02_synthetic_reservation_logical_label_validation_order_repair_report_v1_0.md`

No other repair architecture is selected.

### A02 Repair Contract

- Remove `target_logical_label` from generic opaque-token reservation validation.
- Validate that field only through the dedicated logical-label validator.
- Retain the exact reservation field set, schema, and version.
- Retain canonical hash behavior.
- Retain command, idempotency, attempt-scope, and record-ID formulas.
- Retain the public writer signature.
- Retain durable-attempt and two-transaction semantics.
- Retain the one-attempt limit.
- Retain no-retry and no-second-INSERT semantics.
- Retain strict generic opaque-token validation for genuinely opaque fields.
- Add no alternate label, target, route, CLI, discovery path, or fallback.

### A02 Future Synthetic Validation Matrix

- The exact authorized slash-bearing logical label passes reservation validation.
- Pure command build and command revalidation agree.
- The public writer reaches and commits exactly one reservation and one exact
  record only against temporary synthetic SQLite state and valid synthetic input.
- Empty labels are rejected.
- Absolute labels are rejected.
- Backslashes are rejected.
- Drive-colon forms are rejected.
- Traversal is rejected.
- Malformed segments are rejected.
- Every other opaque-token field remains strict.
- Store target-label mismatch remains fail-closed.
- The prompt-frozen 68 persistence tests remain passing.
- Durable-attempt, ambiguity, actual-column integrity, and receipt regressions
  remain passing.
- No repository runtime target or real candidate value is used.

A01 does not implement or run this matrix.

## 13. Fresh Activation Architecture

The frozen future sequence is:

1. MVP13-A01 candidate completion.
2. ChatGPT independent acceptance.
3. One fresh exact MVP13-A02 authorization decision.
4. Synthetic-only A02 repair implementation and validation.
5. ChatGPT independent acceptance.
6. One fresh exact MVP13-A03 authorization decision.
7. Docs-only new activation decision.
8. ChatGPT independent acceptance.
9. One fresh exact MVP13-A04 authorization decision.
10. One fresh bounded persistence execution.
11. ChatGPT independent acceptance.
12. Only then determine MVP-F09 eligibility.

No later step is authorized by A01.

## 14. MVP13-A03

- title = Fresh Exact Nonproduction Persistence Activation Decision After Accepted A02
- classification = conditional
- prompt_count = 1
- status = not_started
- authorized = no
- executed = no

A03 must bind without reading protected content:

- the exact locked-candidate identity digest;
- the already accepted safe-payload input hash;
- the exact gate-contract binding, revalidated but not silently replaced;
- the exact target-authorization binding;
- the accepted MVP13-F02 exact-empty result hash;
- the accepted A02 repaired-writer commit and source hash;
- exact schemas and mutation mode;
- one-use activation semantics;
- one public-writer invocation maximum; and
- no retry, second INSERT, or automatic repair.

A03 must create a new activation decision ID and safe hash. That new activation
safe hash must derive new values for:

- idempotency key;
- persisted-record ID;
- audit-receipt reference;
- attempt-scope key; and
- attempt-reservation ID.

Old F07 activation identifiers and old derived persistence identifiers must not
be reused. A03 remains docs-only and performs no payload, target, SQLite, or
writer access.

## 15. MVP13-A04

- title = One Fresh Bounded Nonproduction Persistence Execution After New Activation
- classification = conditional
- prompt_count = 1
- status = not_started
- authorized = no
- executed = no

A04 must require:

- accepted A02 and A03 checkpoints;
- one fresh exact authorization;
- one fresh protected-payload read session for only the already accepted safe
  payload;
- no source package or row reread;
- exactly one public-writer invocation;
- no retry, second writer call, or second INSERT;
- no automatic repair;
- one bounded receipt or safe terminal failure; and
- no production or downstream runtime.

Existing-state resolution must remain fail-closed if target state changes after
MVP13-F02. A04 must not treat the old exact-empty result as a guarantee of future
emptiness.

## 16. Planned Prompt Accounting

Current after A01 activation:

- engineering_consumed = 4
- fixed_consumed = 2
- conditional_consumed = 1
- risk_consumed = 1
- remaining_fixed = 12
- remaining_conditional = 5
- remaining_risk = 1

Planned but not consumed:

- MVP13_A02_conditional_prompt = 1
- MVP13_A03_conditional_prompt = 1
- MVP13_A04_conditional_prompt = 1

Projected after successful activation of A02, A03, and A04:

- remaining_fixed = 12
- remaining_conditional = 2
- remaining_risk = 1

No future Prompt is consumed now.

## 17. MVP-F09 Boundary

- MVP_F09_eligible = no
- MVP_F09_authorized = no
- MVP_F09_executed = no

MVP-F09 can become eligible only after accepted A02 repair, accepted A03 new
activation, accepted A04 execution, and ChatGPT acceptance of a returned receipt
plus exact post-write proof. Exact-empty, A01, A02, or A03 alone is insufficient.

## 18. Current Authorization and No-side-effect Proof

- persistence_code_changed = no
- tests_changed = no
- runtime_changed = no
- new_activation_created = no
- reservation_created = no
- governed_record_created = no
- runtime_target_accessed = no
- target_sidecars_accessed = no
- SQLite_opened = no
- helper_invoked = no
- writer_imported = no
- writer_invoked = no
- mutation_helper_imported_or_invoked = no
- payload_or_receipt_accessed = no
- source_package_or_row_accessed = no
- production_or_downstream_runtime_used = no
- Project_Source_modified = no
- MVP13_A02_authorized = no
- MVP13_A03_authorized = no
- MVP13_A04_authorized = no

The analysis used only committed source text, AST, bounded Git history, tests as
text, architecture documents, and safe health reports.

## 19. Validation Status

- historical_current_source_hash_comparison = passed
- source_AST_call_order_extraction = passed
- candidate_inventory_required_count = 14
- candidate_inventory_complete = yes
- evidence_class_vocabulary_bounded = yes
- historical_root_cause_overclaim_absent = yes
- A02_A03_A04_sequence_consistent = yes
- Prompt_accounting_arithmetic = passed
- exact_one_file_allowlist = passed
- document_static_validation = passed
- pytest_run = no
- py_compile_run = no
- product_import_probe_run = no

## 20. Project Source Recommendation

- Project_Source_modified_by_Codex = no
- Project_Source_update_recommendation = replace Canonical 00, 03 and 09 after ChatGPT independent acceptance
- Canonical_05_change = no
- Source_11_change = no

## 21. Next Boundary

- next_boundary = ChatGPT independent acceptance of MVP13-A01 followed by one fresh exact MVP13-A02 synthetic-repair authorization decision
- persistence_code_or_test_change_allowed_now = no
- A02_execution_allowed_now = no
- new_activation_allowed_now = no
- A03_or_A04_execution_allowed_now = no
- runtime_target_or_sidecar_access_allowed_now = no
- payload_or_receipt_access_allowed_now = no
- helper_writer_or_mutation_call_allowed_now = no
- reservation_or_record_creation_allowed_now = no
- MVP_F09_execution_allowed_now = no
