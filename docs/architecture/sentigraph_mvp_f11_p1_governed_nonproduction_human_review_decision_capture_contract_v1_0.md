# Sentigraph MVP-F11-P1 Governed Nonproduction Human Review Decision Capture Contract v1.0

Date: 2026-07-14

Milestone: MVP-F11-P1, planned fixed milestone part 1 of 2

Decision: `ready`

privacy_issue_stop: `no`

MVP_F11_P1_status: `candidate_completed_pending_chatgpt_acceptance`

MVP_F11_P2_authorized: `no`

MVP_F11_P2_executed: `no`

## Exact approval

`APPROVE_SENTIGRAPH_MVP_F11_P1_GOVERNED_NONPRODUCTION_HUMAN_REVIEW_DECISION_CAPTURE_ARCHITECTURE_AND_CONTRACT_DOCS_ONLY_PLANNED_FIXED_MILESTONE_PART_1_OF_2_BIND_ACCEPTED_MVP_F10_COMMIT_AND_READ_ONLY_REVIEW_PROJECTION_SELECT_ONE_DEDICATED_DISABLED_BY_DEFAULT_INTERNAL_APPEND_ONLY_NONPRODUCTION_HUMAN_REVIEW_DECISION_LEDGER_ARCHITECTURE_DEFINE_EXACT_DECISION_SCHEMA_SERVER_OWNED_RECORD_RESERVATION_AND_SNAPSHOT_BINDINGS_ALLOWED_KEEP_PENDING_AND_REQUEST_MORE_GOVERNANCE_REVIEW_DECISIONS_IDEMPOTENCY_APPEND_ONLY_AUDIT_RECEIPT_HUMAN_REVIEW_NO_TRUST_UPGRADE_AND_FUTURE_P2_EXACT_FILE_ALLOWLIST_REJECT_DIRECT_GOVERNED_RECORD_MUTATION_PRODUCTION_REVIEW_QUEUE_TRUST_APPROVAL_ANALYSIS_REPORT_CORRECTION_REVOCATION_DELETE_PUBLIC_ROUTE_FRONTEND_IMPLEMENTATION_TARGET_GET_HELPER_WRITER_SQLITE_PAYLOAD_SOURCE_ROW_RUNTIME_OR_PROJECT_SOURCE_CHANGE`

This approval authorizes this contract document only. It does not authorize implementation, storage initialization, decision capture, runtime access, or MVP-F11-P2.

## Goal lifecycle and prompt accounting

- P0 completed before Goal creation.
- Exactly one new MVP-F11-P1 Goal was created after the repository, anchor, frozen blobs, clean state, and output absence all passed.
- The completed MVP-F10 Goal was not resumed or replaced.
- This Goal remains limited to one architecture document, static validation, and ready-only Git finalization.

| Prompt counter | Value |
| --- | ---: |
| consumed_engineering_prompts_since_v1_3 | 13 |
| consumed_fixed_prompts_since_v1_3 | 6 |
| consumed_conditional_prompts_since_v1_3 | 6 |
| consumed_risk_prompts_since_v1_3 | 1 |
| remaining_fixed_prompts | 8 |
| remaining_conditional_allowance | 0 |
| remaining_risk_buffer | 1 |

## Starting anchor and accepted MVP-F10 binding

- Repository identity: `dgmpurf/Sentigraph`
- Branch: `main`
- Starting HEAD: `6ba3d437ed2db5c907c5a70888650fc2729f2f0c`
- Starting HEAD message: `Implement MVP-F10-P2 review-console integration`
- Starting origin/main: `6ba3d437ed2db5c907c5a70888650fc2729f2f0c`
- Starting ahead/behind: `0/0`
- Starting worktree: clean, zero staged files, zero nonignored untracked files
- Accepted MVP-F10 report: `docs/health/sentigraph_mvp_f10_p2_governed_nonproduction_record_to_internal_review_console_read_only_integration_report_v1_0.md`
- Accepted report Git blob: `f118dc69b80ce24c0fbe02454f314786db1d1e50`
- Accepted report SHA-256: `6cadaab5c6d53fab3c49403568ddb6442714248c859b788d955105ed7b733709`
- MVP-F10 status at this authorization boundary: `completed_and_independently_accepted`

The accepted report remains immutable. Its earlier candidate wording is superseded only by the independent-acceptance boundary expressed in the current authorization; no F10 artifact is edited by P1.

### Frozen relevant committed blobs

| Committed path | Git blob |
| --- | --- |
| `backend/app/services/governed_nonproduction_review_console_projection.py` | `1320813d42a08fd6cc292bc40d082c1117eb27a4` |
| `backend/app/api/v1/routes/internal_alpha_review_console.py` | `7661fa969352889858b59a141642e4f1670c3788` |
| `backend/app/tests/test_mvp_f10_p2_governed_nonproduction_review_console_projection.py` | `e3a3e12d38cb2afc0fbb2b443720b0c8a664eca4` |
| `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py` | `4f79bc4af3bbd929b68dc8a75d8a214712fa5c12` |
| `frontend/src/api/sentigraphApi.js` | `32c70215ff3c12fe04f7d0138fdcc0273ca21771` |
| `frontend/src/pages/InternalAlphaReviewConsole.jsx` | `3dda533be80d77a1ed5e78943a4a76c087dd2d19` |

## Audited current surface

The bounded static audit established the following current-state facts without importing or executing product code:

- The accepted F10 report fixes the ready projection and outer-response canonical hashes plus eight approved opaque record, reservation, candidate, and snapshot bindings.
- `governed_nonproduction_review_console_projection.py` owns the server-side ready projection constants and preserves human-review/no-trust-upgrade boundaries.
- `internal_alpha_review_console.py` is an internal read-only GET route with explicit global and governed-projection gates and false production/runtime readiness flags.
- `backend/app/api/v1/api.py` registers route modules through explicit imports and explicit prefixes/tags. A future decision route therefore requires this exact registration file.
- `governed_nonproduction_evidence_persistence.py` demonstrates reusable architectural patterns: disabled-by-default store construction, injected temporary targets for tests, canonical hashing, deterministic idempotency, bounded receipts, rollback for known pre-commit failure, and read-only verification after commit ambiguity.
- Focused F10 tests lock the existing review-console route family, its GET-only posture, and its frontend fallback. They do not require modification for a separate governed-review-decisions route family.
- Repository guidance favors strict JSON, Pydantic validation, modular services, thin routes, no secrets, and mock/synthetic validation before runtime activation. Its general progress-file handoff rule is not applied because this approval requires exactly one changed document.

The audit did not access runtime storage, any database target, private artifacts, raw evidence, Git history beyond the current anchor, or any product runtime.

## Rejected architecture options

The following options are rejected:

1. Mutating the accepted governed nonproduction record to store review status. This would violate append-only separation and the F10 read-only boundary.
2. Reusing the governed-record persistence database or its record table. This would couple a human-review event to the evidence persistence lifecycle and increase mutation risk.
3. Reusing production Review Queue, case, analysis, report, export, or delivery storage. Those are outside the nonproduction boundary and could imply trust or production readiness.
4. Accepting client-supplied record, reservation, hash, snapshot, reviewer, or target bindings. Those values must remain server-owned and non-overridable.
5. Using a generic environment-selected path, discovery, glob, directory walk, or fallback target. Target identity must be singular and explicit.
6. Adding a frontend decision surface in the initial implementation slice. Initial P2 is backend-only and synthetic-only.
7. Supporting correction, revocation, update, reset, or deletion of a recorded decision. A later event may be separately authorized, but an existing row is immutable.

## Selected architecture

architecture_id: `dedicated_disabled_by_default_internal_append_only_nonproduction_human_review_decision_ledger`

The future component is one dedicated local nonproduction decision ledger. It is separate from the governed-record persistence database and from production Review Queue. It is internal-only, disabled by default, append-only, and incapable of updating or deleting an existing decision row. It does not mutate the governed record, upgrade trust, trigger analysis/report work, execute correction/revocation, or expose a public/customer route. It stores no raw evidence and no reviewer identity.

The initial P2 implementation remains a synthetic-only backend slice. It may validate the service and route against injected temporary SQLite storage, but it must not initialize or access the formal runtime ledger target and must not capture a real human decision.

## Future logical target and owner

- target_kind: `dedicated_local_sqlite_nonproduction_human_review_decision_ledger`
- logical_repository_relative_target_label: `runtime/governed_nonproduction_human_review_decisions/review_decisions_v0_1.sqlite3`
- primary_table: `governed_nonproduction_human_review_decisions_v0_1`
- owner module: `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
- owner class: `GovernedNonproductionHumanReviewDecisionLedger`
- public operation: `record_governed_nonproduction_human_review_decision`

The owner class must default to disabled. The formal logical target is a server-owned constant, not a request value or environment-selected physical path. A temporary path may be injected only by focused synthetic tests. No alternate filename, table, case-store reuse, production target, target discovery, glob, directory walk, or fallback target is permitted.

Formal runtime-target initialization and the first real human-review decision capture require later, separate approvals. Neither belongs to MVP-F11-P2.

## Future P2 implementation classification

- implementation_scope: `synthetic_only_disabled_internal_decision_ledger_and_route`
- validation target: temporary SQLite only
- formal runtime ledger target accessed: no
- actual human decision captured: no
- F10 exact target read: no
- F10 helper invoked: no
- frontend implemented: no
- production Review Queue used: no

## Exact request contract

- request_schema: `sentigraph_governed_nonproduction_human_review_decision_request_v0_1`
- request_version: `0.1`
- request_field_count: 3
- unknown_fields_allowed: no
- free_text_allowed: no

Exact ordered request fields:

1. `request_schema`
2. `request_version`
3. `decision_type`

All three fields are required strings. `request_schema` and `request_version` must equal the fixed values above. The request object must reject extra keys, alternate versions, nulls, arrays, nested objects, numbers, and booleans.

Exact allowed `decision_type` values, in order:

1. `keep_pending_human_review`
2. `request_more_governance_review`

Every other value is rejected. The request cannot contain a record, reservation, candidate, package, case, or row identifier; any hash or digest; a target path; reviewer name, email, account, or external identifier; a free-form note; a trust score/status; a production status; a correction/revocation instruction; or an analysis/report instruction.

## Server-owned review context

The route and service must bind every accepted request to the following immutable server-owned constants. The request cannot supply or override any of them.

| Context field | Exact value |
| --- | --- |
| `source_projection_schema` | `sentigraph_internal_alpha_governed_nonproduction_record_review_projection_v0_1` |
| `source_projection_version` | `0.1` |
| `source_projection_id` | `governed-nonproduction-record-review-v0-1` |
| `source_projection_status` | `governed_record_review_ready` |
| `source_projection_canonical_sha256` | `0b9dc55caf3a375b1c5c4c2b66d851c1e192807fb0fd5259fcab77c32a74575f` |
| `source_outer_response_canonical_sha256` | `9163797b7aa4ec5506ebbab00d1180451b5631a32c6f3a236c4127526366e110` |
| `reviewer_role_label` | `self_declared_project_owner_role` |
| `reviewer_authority_basis_label` | `authority_basis_not_independently_validated` |
| `reviewer_identity_verified` | `false` |
| `persisted_record_id` | `gnpepr-c886bd087e84dceff806e748d2f2ceaf` |
| `attempt_reservation_id` | `gnpepr-attempt-34d95623c3678bdd63430d97fdc7d922` |
| `candidate_identity_digest` | `078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54` |
| `input_safe_hash` | `71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5` |
| `gate_contract_safe_hash` | `a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a` |
| `activation_decision_safe_hash` | `e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d` |
| `record_snapshot_digest` | `eda50fc437940ac519881638d76fa0443481fc9fda8f50cf62805be0d83baf20` |
| `reservation_snapshot_digest` | `076584df7f9d712b78e9c3e5dee06cc55ff817487084074e34824bd9185f7a6c` |

These are approved opaque metadata values, not raw evidence. Initial P2 must use constants derived from this accepted contract and must not call the F10 route, adapter, helper, or target to reconstruct them.

## Exact decision-record contract

- decision_schema: `sentigraph_governed_nonproduction_human_review_decision_record_v0_1`
- decision_version: `0.1`
- decision_record_field_count: 38
- extra_fields_allowed: no

Exact ordered decision-record fields:

1. `decision_schema`
2. `decision_version`
3. `decision_id`
4. `idempotency_key`
5. `audit_receipt_reference`
6. `ledger_scope`
7. `decision_type`
8. `decision_status`
9. `recorded_at`
10. `reviewer_role_label`
11. `reviewer_authority_basis_label`
12. `reviewer_identity_verified`
13. `source_projection_schema`
14. `source_projection_version`
15. `source_projection_id`
16. `source_projection_status`
17. `source_projection_canonical_sha256`
18. `source_outer_response_canonical_sha256`
19. `persisted_record_id`
20. `attempt_reservation_id`
21. `candidate_identity_digest`
22. `input_safe_hash`
23. `gate_contract_safe_hash`
24. `activation_decision_safe_hash`
25. `record_snapshot_digest`
26. `reservation_snapshot_digest`
27. `decision_canonical_hash`
28. `human_review_required`
29. `no_automatic_trust_upgrade`
30. `production_evidenceitem_changed`
31. `production_case_changed`
32. `downstream_runtime_called`
33. `correction_or_revocation_performed`
34. `deleted_or_updated`
35. `allowed_follow_up_labels`
36. `blocked_follow_up_labels`
37. `warnings`
38. `blockers`

### Required decision-record values and types

- `decision_schema` and `decision_version` equal the fixed values above.
- `decision_id` matches `ghrd-` followed by 32 lowercase hexadecimal characters.
- `idempotency_key` is exactly 64 lowercase hexadecimal characters.
- `audit_receipt_reference` matches `ghrd-receipt-` followed by 32 lowercase hexadecimal characters.
- `ledger_scope = governed_nonproduction_record_human_review_only`.
- `decision_type` is one of the two exact allowed values.
- `decision_status = recorded_append_only_nonproduction`.
- `recorded_at` is a server-generated canonical UTC timestamp ending in `Z`. It is not request-controlled.
- Reviewer and source fields equal the server-owned context above.
- All eight opaque record/reservation/candidate/snapshot bindings equal the server-owned context above.
- `decision_canonical_hash` is exactly 64 lowercase hexadecimal characters and follows the derivation below.
- `human_review_required = true`.
- `no_automatic_trust_upgrade = true`.
- `production_evidenceitem_changed = false`.
- `production_case_changed = false`.
- `downstream_runtime_called = false`.
- `correction_or_revocation_performed = false`.
- `deleted_or_updated = false`.
- `warnings = []` and `blockers = []`.

Exact ordered `allowed_follow_up_labels`:

1. `keep_pending_human_review`
2. `request_more_governance_review`

Exact ordered `blocked_follow_up_labels`:

1. `trust_approval_blocked`
2. `automatic_trust_upgrade_blocked`
3. `governed_record_mutation_blocked`
4. `production_review_queue_blocked`
5. `production_promotion_blocked`
6. `analysis_trigger_blocked`
7. `report_generation_blocked`
8. `correction_or_revocation_execution_blocked`
9. `delete_or_reset_blocked`
10. `public_delivery_blocked`

These labels are inert strings. None is an executable callback or permission grant.

## Idempotency, identifiers, and canonical hashes

The service must derive the idempotency key from one canonical versioned object containing exactly these server-owned or strictly validated values:

1. request schema
2. request version
3. decision type
4. reviewer role label
5. reviewer authority-basis label
6. source projection schema
7. source projection version
8. source projection ID
9. source projection status
10. source projection canonical SHA-256
11. source outer-response canonical SHA-256
12. persisted record ID
13. attempt reservation ID
14. candidate identity digest
15. input safe hash
16. gate-contract safe hash
17. activation-decision safe hash
18. record snapshot digest
19. reservation snapshot digest

`recorded_at` does not participate in idempotency derivation. Canonicalization uses UTF-8 JSON, lexicographically sorted object keys, compact separators with no insignificant whitespace, preserved array order, standard JSON booleans/nulls, and SHA-256 over the exact encoded bytes.

Deterministic identifiers:

- `decision_id = ghrd-<first_32_lowercase_hex_characters_of_idempotency_key>`
- `audit_receipt_reference = ghrd-receipt-<first_32_lowercase_hex_characters_of_idempotency_key>`

The decision canonical hash uses the same canonical UTF-8 JSON rules over all 38 persisted record fields except `decision_canonical_hash`. Unlike the idempotency key, the decision hash includes `recorded_at`.

## Append-only, conflict, and ambiguity semantics

- The store permits a plain INSERT for a new exact decision only.
- UPDATE, mutation-producing UPSERT, DELETE, replacement, reset, and status transition of an existing row are forbidden.
- `decision_id`, `idempotency_key`, and `audit_receipt_reference` are unique.
- The same exact decision for the same reviewed snapshot performs zero mutation, returns the existing exact record, and reports `already_exists_same_human_review_decision`.
- A different allowed decision type for the same reviewed snapshot may append one new distinct record because its idempotency key and identifiers differ.
- An occupied identifier or idempotency key whose persisted fields do not exactly match is a conflict and performs zero mutation.
- A known pre-commit failure rolls back and returns a bounded zero-mutation receipt.
- After commit ambiguity, no second insert or automatic mutation retry is allowed. One read-only lookup by deterministic idempotency key may verify an exact existing row or a conflict.
- If read-only verification proves the exact row, the operation returns the exact existing decision. If it proves a mismatch, it returns the conflict outcome. If it cannot establish either result, it returns `paused_pending_read_only_idempotency_verification` and stops.
- No operation may update or delete an existing decision to express correction or revocation. Any future event type requires a separate contract and authorization.

## Exact receipt contract

- receipt_schema: `sentigraph_governed_nonproduction_human_review_decision_receipt_v0_1`
- receipt_version: `0.1`
- receipt_field_count: 27
- extra_fields_allowed: no

Exact ordered receipt fields:

1. `receipt_schema`
2. `receipt_version`
3. `outcome`
4. `audit_receipt_reference`
5. `decision_id`
6. `idempotency_key`
7. `decision_type`
8. `decision_status`
9. `decision_canonical_hash`
10. `created_new_entry`
11. `reused_existing_entry`
12. `mutation_count`
13. `decision_row_count_before`
14. `decision_row_count_after`
15. `exact_expected_entry_present`
16. `conflicting_entry_present`
17. `unrelated_entry_changed`
18. `append_only_verified`
19. `human_review_required`
20. `no_automatic_trust_upgrade`
21. `production_evidenceitem_changed`
22. `production_case_changed`
23. `downstream_runtime_called`
24. `correction_or_revocation_performed`
25. `deleted_or_updated`
26. `warnings`
27. `blockers`

All fields are required and no extra key is accepted. Identifier/hash/status fields may be null only when a blocked or bounded-failure outcome occurs before safe deterministic derivation. Row counts are nonnegative integers when safely observed and null when observation is unavailable. Boolean verification fields are true only when positively verified; unverified is false. `warnings` and `blockers` are ordered bounded-label arrays, never free text.

Exact receipt outcomes, in order:

1. `created_exactly_one_human_review_decision`
2. `already_exists_same_human_review_decision`
3. `blocked_unsupported_decision_type`
4. `blocked_binding_or_snapshot_mismatch`
5. `blocked_idempotency_conflict`
6. `paused_pending_read_only_idempotency_verification`
7. `bounded_decision_ledger_failure`

### Outcome invariants

| Outcome | created_new_entry | reused_existing_entry | mutation_count | exact_expected_entry_present | conflicting_entry_present | append_only_verified |
| --- | --- | --- | ---: | --- | --- | --- |
| `created_exactly_one_human_review_decision` | true | false | 1 | true | false | true |
| `already_exists_same_human_review_decision` | false | true | 0 | true | false | true |
| `blocked_unsupported_decision_type` | false | false | 0 | false | false | true |
| `blocked_binding_or_snapshot_mismatch` | false | false | 0 | false | false | true |
| `blocked_idempotency_conflict` | false | false | 0 | false | true | true |
| `paused_pending_read_only_idempotency_verification` | false | false | 0 | false | false | false |
| `bounded_decision_ledger_failure` | false | false | 0 | false | false | false |

For create, `decision_row_count_after = decision_row_count_before + 1`. For exact reuse, conflict, and every safely verified zero-mutation outcome, before/after counts are equal. For unavailable observation, both counts are null. `unrelated_entry_changed` is false for every outcome.

Every outcome also fixes these values:

- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- `production_evidenceitem_changed = false`
- `production_case_changed = false`
- `downstream_runtime_called = false`
- `correction_or_revocation_performed = false`
- `deleted_or_updated = false`

Successful create and reuse have `warnings = []` and `blockers = []`. Blocked, paused, and bounded-failure outcomes use only one bounded blocker label corresponding to the outcome and never expose internal exception or storage details.

## Future internal route and response contracts

- route module: `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py`
- route family: `/api/v1/internal/alpha/governed-review-decisions`
- registration file: `backend/app/api/v1/api.py`
- registration prefix: `/internal/alpha/governed-review-decisions`
- gate: `SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_LEDGER_ENABLED`
- route mode: `internal_disabled_by_default_append_only_nonproduction_human_review_decision_ledger`

The gate is false for missing, empty, malformed, or non-allowlisted values. Initial P2 tests may enable it process-locally. A disabled route must fail closed without initializing or opening a ledger.

### POST endpoint

Endpoint: `POST /decisions`

Full path: `/api/v1/internal/alpha/governed-review-decisions/decisions`

The endpoint accepts only the exact three-field request. It must not call the F10 route, projection adapter, accepted helper, governed target, writer, or any downstream runtime.

POST response schema: `sentigraph_internal_alpha_governed_review_decision_post_response_v0_1`

Exact ordered POST response fields:

1. `response_schema`
2. `route_mode`
3. `decision_id`
4. `decision`
5. `receipt`
6. `human_review_required`
7. `no_automatic_trust_upgrade`
8. `decision_ledger_write_performed`
9. `production_object_enabled`
10. `review_queue_runtime_enabled`
11. `operator_runtime_ready`
12. `public_ready`
13. `production_ready`

`decision` is the exact 38-field record for created/reused success and null otherwise. `decision_ledger_write_performed` is true only for `created_exactly_one_human_review_decision`. All production/runtime readiness flags are false for every outcome.

Outcome-to-status mapping:

| Receipt outcome | HTTP status |
| --- | ---: |
| `created_exactly_one_human_review_decision` | 201 |
| `already_exists_same_human_review_decision` | 200 |
| `blocked_unsupported_decision_type` | 422 |
| `blocked_binding_or_snapshot_mismatch` | 409 |
| `blocked_idempotency_conflict` | 409 |
| `paused_pending_read_only_idempotency_verification` | 503 |
| `bounded_decision_ledger_failure` | 500 |

### Exact-ID GET endpoint

Endpoint: `GET /decisions/{decision_id}`

Full path: `/api/v1/internal/alpha/governed-review-decisions/decisions/{decision_id}`

GET response schema: `sentigraph_internal_alpha_governed_review_decision_get_response_v0_1`

Exact ordered GET response fields:

1. `response_schema`
2. `route_mode`
3. `decision_id`
4. `decision`
5. `human_review_required`
6. `no_automatic_trust_upgrade`
7. `production_object_enabled`
8. `review_queue_runtime_enabled`
9. `operator_runtime_ready`
10. `public_ready`
11. `production_ready`

GET accepts one strict deterministic decision ID and returns only its exact safe 38-field record. It performs no mutation and exposes no receipt or list. Unknown or malformed IDs fail closed with no ledger write.

The route family has no list endpoint, PUT, PATCH, DELETE, public/customer alias, production Review Queue reuse, automatic retry, or frontend integration.

## Privacy and product boundaries

- The request carries only schema, version, and one of two bounded decision labels.
- All reviewed-record bindings are immutable server-owned opaque metadata.
- Reviewer context is limited to a self-declared role label and an explicitly unvalidated authority-basis label; identity verification remains false.
- No reviewer name, account, email, external identifier, raw evidence, private content, source material, package, row, case details, target locator, credential, or secret is accepted or stored.
- Recording a decision does not approve trust, promote evidence, mutate a governed record, change a case, call downstream runtime, trigger analysis/report work, perform correction/revocation, or delete/reset anything.
- The ledger is nonproduction, internal, disabled by default, append-only, and separate from production Review Queue.
- No label is executable.
- No frontend or public delivery surface belongs to initial P2.

## Exact future MVP-F11-P2 file allowlist

P2_scope_bounded: `yes`

P2_implementation_ready: `yes`, subject to a fresh exact authorization after independent P1 acceptance

Maximum allowed changed-file count: 5

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py`
3. `backend/app/api/v1/api.py`
4. `backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py`
5. `docs/health/sentigraph_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger_implementation_report_v1_0.md`

No frontend path is allowed. No existing review-console safety test is included because the audited tests constrain the existing `/internal/alpha/review-console` family; the new focused test must own the separate governed-review-decisions route, registration, strict schemas, and safety boundaries. If implementation later proves a sixth exact safety-test path necessary, P2 must stop for a revised exact authorization rather than expanding this allowlist implicitly.

## Future MVP-F11-P2 validation plan

Define and later execute only under fresh authorization:

- genuine TDD RED before product implementation;
- strict three-field request validation with unknown keys rejected;
- exactly two allowed decision types and every other value rejected;
- deterministic idempotency key, decision ID, and receipt reference;
- exact ordered 38-field decision record with unique names and no extras;
- exact ordered 27-field receipt with unique names and no extras;
- exact seven receipt outcomes and their invariant flags;
- create exactly one record and exact idempotent reuse with zero mutation;
- distinct allowed decision type appends one distinct record;
- binding mismatch, identifier conflict, known rollback, and commit-ambiguity outcomes;
- append-only enforcement with no mutation-producing upsert, update, delete, replacement, reset, or status transition;
- injected temporary SQLite only, with the formal runtime ledger target absent and unopened;
- route gate disabled by default and enabled only process-locally in focused tests;
- internal POST and exact-ID GET only, with no list/PUT/PATCH/DELETE/public route;
- no frontend, Review Queue, F10 route/helper/target, governed-record writer, governed-record mutation, analysis, report, export, or delivery call;
- Python compilation for the exact future Python files;
- focused tests plus the minimum nearby registration and safety regressions without changing their files;
- forbidden import, route, privacy, raw-data, target, production-overclaim, and retry scans;
- exact five-file allowlist, cached diff validation, and clean Git finalization.

Formal runtime ledger initialization and one real decision capture are excluded from this validation plan.

## P1 no-side-effect proof

| Proof item | Result |
| --- | --- |
| docs_only | yes |
| backend_code_changed | no |
| frontend_code_changed | no |
| tests_changed | no |
| route_executed | no |
| target_GET_count | 0 |
| helper_invocation_count | 0 |
| writer_invocation_count | 0 |
| SQLite_access_count | 0 |
| decision_ledger_created | no |
| human_review_decision_captured | no |
| production_object_created | no |
| Project_Source_changed | no |

No product import, test, compilation, frontend build, browser, server, route, helper, writer, target, SQLite, or runtime command is authorized or required for P1.

## Source recommendation

If this P1 contract is independently accepted later:

- Canonical 00: replace
- Canonical 03: replace
- Canonical 09: replace
- Canonical 08: no runtime-status change until MVP-F11-P2
- Canonical 05: no change
- Source 11: no change
- Project Source: unchanged by this milestone

## Next boundary

next_boundary: `ChatGPT independent acceptance of MVP-F11-P1 followed by one fresh exact MVP-F11-P2 synthetic-only implementation authorization`

MVP-F11-P2 remains unauthorized and unexecuted. No MVP-F12 or later milestone is started by this contract.
