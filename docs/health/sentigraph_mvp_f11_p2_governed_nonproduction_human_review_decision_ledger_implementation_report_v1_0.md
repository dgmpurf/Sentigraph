# Sentigraph MVP-F11-P2 Governed Nonproduction Human-Review Decision Ledger Implementation Report v1.0

## 1. Result

**Status: READY FOR READY-ONLY GIT FINALIZATION**

MVP-F11-P2 implements the accepted synthetic-only, governed-nonproduction human-review decision ledger contract. The implementation:

- accepts only the two bounded human-review decisions defined by MVP-F11-P1;
- persists only to an explicitly supplied synthetic SQLite path;
- rejects the formal runtime target before opening SQLite;
- provides a disabled-by-default internal POST and exact-ID GET route family;
- preserves the existing MVP-F10 read-only review-console route as a separate surface;
- performs no trust approval, automatic trust upgrade, production-object mutation, review-queue activation, downstream runtime call, correction, revocation, deletion, or reset; and
- exposes no reviewer name, email address, credential, secret, filesystem path, SQL text, or raw exception detail.

The focused contract module completed GREEN with all 41 collected cases passing.

## 2. Accepted Input and Frozen Identity

Implementation began from the accepted repository state:

- baseline `HEAD`: `9284934b6008e711309a655ed80f1919fe8e6834`
- baseline `origin/main`: `9284934b6008e711309a655ed80f1919fe8e6834`
- baseline ahead/behind: `0/0`
- accepted MVP-F11-P1 contract blob: `29d3806a535680247713ae317c1d1c9097f69d06`
- accepted MVP-F11-P1 contract SHA-256: `dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152`
- frozen API registration blob: `80bf807cdbde2618bae19ee79056b2f1ff8a3454`
- frozen governed-nonproduction persistence blob: `75a5280cec9fe7d2ec3ffffc707699fb8d8f2ebe`

No repository change existed at the start of the Goal. The formal target did not exist and was not created.

## 3. Exact Five-File Scope

Only these paths are in the MVP-F11-P2 allowlist:

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py`
3. `backend/app/api/v1/api.py`
4. `backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py`
5. `docs/health/sentigraph_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger_implementation_report_v1_0.md`

No frontend file, existing MVP-F10 route, projection helper, evidence writer, formal target, product database, or unrelated test was changed.

## 4. Implemented Architecture

### 4.1 Isolated append-only ledger service

The new service owns request validation, deterministic identity derivation, canonical hashing, append-only SQLite persistence, readback integrity verification, receipt construction, and read-only ambiguity resolution.

The service has no default physical database path and is disabled by default. Enabling it still requires an explicit caller-supplied path. A path equal to, or ending in, the formal logical target is rejected before any SQLite connection or directory creation.

The synthetic table is:

`governed_nonproduction_human_review_decisions_v0_1`

It has exactly the 38 decision-record columns in contract order. `decision_id`, `idempotency_key`, and `audit_receipt_reference` are unique. The service contains one plain `INSERT INTO` operation and contains no mutation statement for an existing row.

### 4.2 Disabled internal route family

The new route family is:

`/api/v1/internal/alpha/governed-review-decisions`

It exposes only:

- `POST /decisions`
- `GET /decisions/{decision_id}`

The environment gate is:

`SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_LEDGER_ENABLED`

With the gate absent or false, the route returns a safe `404` posture and does not construct a ledger. With the gate true but no explicitly injected synthetic ledger, it returns `503` and opens no SQLite database. There is no collection GET and no PUT, PATCH, or DELETE route.

### 4.3 Existing read-only console remains separate

MVP-F10 remains a GET-only review-projection surface. MVP-F11-P2 neither imports its projection helper into the ledger service nor writes through its route. The only shared integration point is registration under the existing API router.

## 5. Exact Request Contract

The request schema is:

`sentigraph_governed_nonproduction_human_review_decision_request_v0_1`

Version: `0.1`

The request contains exactly three ordered fields:

1. `request_schema`
2. `request_version`
3. `decision_type`

The only allowed decision types are:

1. `keep_pending_human_review`
2. `request_more_governance_review`

Missing, extra, reordered, non-string, or binding-mismatched fields are blocked before clock acquisition and before SQLite access. Any other decision type is classified as `blocked_unsupported_decision_type`.

## 6. Exact Decision Record Contract

The decision schema is:

`sentigraph_governed_nonproduction_human_review_decision_record_v0_1`

Version: `0.1`

The record contains exactly these 38 ordered fields:

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

The record always retains the nonproduction safety posture:

- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- `reviewer_identity_verified = false`
- `production_evidenceitem_changed = false`
- `production_case_changed = false`
- `downstream_runtime_called = false`
- `correction_or_revocation_performed = false`
- `deleted_or_updated = false`

The two decision-status mappings are:

- `keep_pending_human_review` -> `pending_human_review_retained`
- `request_more_governance_review` -> `more_governance_review_requested`

## 7. Deterministic Identity and Canonical Hashing

The idempotency key is the SHA-256 of compact, sorted-key, UTF-8 canonical JSON over exactly 19 inputs:

1. `ledger_scope`
2. `decision_type`
3. `source_projection_schema`
4. `source_projection_version`
5. `source_projection_id`
6. `source_projection_status`
7. `source_projection_canonical_sha256`
8. `source_outer_response_canonical_sha256`
9. `reviewer_role_label`
10. `reviewer_authority_basis_label`
11. `reviewer_identity_verified`
12. `persisted_record_id`
13. `attempt_reservation_id`
14. `candidate_identity_digest`
15. `input_safe_hash`
16. `gate_contract_safe_hash`
17. `activation_decision_safe_hash`
18. `record_snapshot_digest`
19. `reservation_snapshot_digest`

`recorded_at` is excluded from idempotency. `decision_id` and `audit_receipt_reference` are deterministic derivatives of the idempotency key with prefixes `ghrd-` and `ghrd-receipt-`. The decision canonical hash includes every decision field except `decision_canonical_hash`, including `recorded_at`.

Actual stored columns are read back, JSON arrays are parsed and type-checked, booleans are normalized, and the decision hash is recomputed before any record is returned or reused.

## 8. Exact Receipt and Outcome Contract

The receipt schema is:

`sentigraph_governed_nonproduction_human_review_decision_receipt_v0_1`

Version: `0.1`

The receipt contains exactly these 27 ordered fields:

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

The seven outcomes and POST status mapping are:

| Outcome | HTTP | created | reused | mutations | exact | conflict | append-only verified |
| --- | ---: | --- | --- | ---: | --- | --- | --- |
| `created_exactly_one_human_review_decision` | 201 | true | false | 1 | true | false | true |
| `already_exists_same_human_review_decision` | 200 | false | true | 0 | true | false | true |
| `blocked_unsupported_decision_type` | 422 | false | false | 0 | false | false | true |
| `blocked_binding_or_snapshot_mismatch` | 409 | false | false | 0 | false | false | true |
| `blocked_idempotency_conflict` | 409 | false | false | 0 | false | true | true |
| `paused_pending_read_only_idempotency_verification` | 503 | false | false | 0 | false | false | false |
| `bounded_decision_ledger_failure` | 500 | false | false | 0 | false | false | false |

Every receipt preserves the same human-review, no-trust-upgrade, no-production-mutation, no-downstream-call, no-correction, and no-deletion posture as the decision record.

## 9. Commit Ambiguity and Append-Only Behavior

The service performs at most one insert attempt for a new decision.

- A known failure before commit rolls back and returns `bounded_decision_ledger_failure` without raw detail.
- An ambiguous result after commit causes only a read-only exact-entry verification.
- An exact committed row resolves to `created_exactly_one_human_review_decision` without a second insert.
- A present but mismatched or integrity-invalid row resolves to `blocked_idempotency_conflict`.
- An unavailable or unresolvable ledger resolves to `paused_pending_read_only_idempotency_verification`.

No branch modifies or removes an existing decision row.

## 10. Route Response Boundaries

The POST response contains exactly 13 fields:

`response_schema`, `route_mode`, `decision_id`, `decision`, `receipt`, `human_review_required`, `no_automatic_trust_upgrade`, `decision_ledger_write_performed`, `production_object_enabled`, `review_queue_runtime_enabled`, `operator_runtime_ready`, `public_ready`, `production_ready`.

The exact-ID GET response contains exactly 11 fields:

`response_schema`, `route_mode`, `decision_id`, `decision`, `human_review_required`, `no_automatic_trust_upgrade`, `production_object_enabled`, `review_queue_runtime_enabled`, `operator_runtime_ready`, `public_ready`, `production_ready`.

All five runtime-readiness fields remain false. A ledger write is reported only for the single created outcome with mutation count one.

## 11. TDD and Validation Evidence

### 11.1 RED

The test module was created before product implementation. An initial collection-only naming defect was corrected inside the same allowlisted test file. The subsequent RED run collected successfully: the two pre-existing-boundary guards passed, while all implementation-facing cases failed because the new service, route, and registration did not yet exist.

Command:

```text
python -m pytest backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py -q --tb=line
```

### 11.2 GREEN

After implementation, the same focused module completed with all 41 cases passing:

```text
.........................................                                [100%]
```

Command:

```text
python -m pytest backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py -q --tb=short
```

The focused coverage includes:

- exact constants, field order, field uniqueness, and outcome matrix;
- strict request shape, types, bindings, and allowed decision values;
- no SQLite or clock acquisition for invalid inputs and frozen-context mismatch;
- disabled defaults, explicit synthetic path requirement, and formal-target rejection;
- exact table columns and uniqueness constraints;
- deterministic identity, idempotent reuse, distinct allowed decisions, and row counts;
- stored-column readback, JSON-array parsing, canonical hash verification, and tamper detection;
- known pre-commit failure and all three commit-ambiguity outcomes;
- source-level append-only and dependency-isolation guards;
- disabled-gate and enabled-without-ledger route postures;
- POST creation, reuse, unsupported decision, exact-ID GET, malformed ID, and unknown ID;
- exact route family and API registration; and
- path, SQL, exception, identity, credential, and secret non-disclosure.

`git diff --check` also completed successfully before report creation. Its only output was the platform line-ending advisory for the already tracked API registration file.

## 12. Explicit Non-Goals and Safety Statement

MVP-F11-P2 is not a production review queue, trust adjudicator, operator console, evidence mutator, case mutator, analysis trigger, report generator, correction/revocation executor, delivery service, or public endpoint.

It does not consume real human decisions. It does not access the formal ledger target:

`runtime/governed_nonproduction_human_review_decisions/review_decisions_v0_1.sqlite3`

It does not create that target or its parent directory. It does not activate MVP-F12 or any later runtime. Synthetic temporary SQLite files created by the focused tests are pytest-owned and are outside the formal runtime location.

## 13. Readiness Decision

The implementation is ready for final bounded validation and ready-only Git finalization if and only if:

1. the focused module remains GREEN;
2. the formal target remains absent;
3. static source and diff checks remain clean;
4. exactly the five allowlisted files are changed; and
5. cached diff validation confirms those five files and no others.

Any failure of those conditions changes this report's operational result to blocked and forbids commit/push until resolved within the accepted scope.
