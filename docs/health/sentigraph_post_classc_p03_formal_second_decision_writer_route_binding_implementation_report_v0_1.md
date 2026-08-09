# Sentigraph Post-Class-C P03 formal second-decision writer and route binding

## Status

- Lifecycle: repository implementation and synthetic validation candidate.
- Goal: `SENTIGRAPH_POST_CLASSC_P03_FORMAL_SECOND_DECISION_WRITER_ROUTE_BINDING_REPOSITORY_IMPLEMENTATION_AND_SYNTHETIC_VALIDATION_V01`.
- Implementation authority: `1/0/1 -> 1/1/0`, consumed on the first authorized repository-byte mutation and nonreusable.
- Real formal target access / real SQLite access: `0 / 0`.
- Backend, frontend, Vite, Sentigraph browser, HTTP, decision POST, decision GET: `0 / 0 / 0 / 0 / 0 / 0 / 0`.
- Project Source access / change: `0 / 0`.
- Live runtime or live POST authority created: `0`.
- Future live runtime is **not authorized** by this implementation.

## Exact change boundary

The candidate changes exactly these four authorized paths:

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py`
3. `backend/app/tests/test_post_classc_p03_formal_second_decision_writer_route_binding.py`
4. `docs/health/sentigraph_post_classc_p03_formal_second_decision_writer_route_binding_implementation_report_v0_1.md`

No other repository path is part of the candidate.

## File identities

| Path | Preimplementation bytes / SHA-256 | Candidate bytes / SHA-256 | Changed |
|---|---|---|---|
| `backend/app/services/governed_nonproduction_human_review_decision_ledger.py` | `74788 / 4873ac214091dd9e8d7d65a78639ddf769cbba87fb9615c1a4caaab737599295` | `99111 / 1a719d5511c86f5925f743e5d40c3479f540759481e258addde96eac71415c36` | yes |
| `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py` | `6063 / 11afc86363cf6198f961aa46b67e42da7a97b6dd659cf0e039d11edf804f94e7` | `9952 / a7bff2159606ec97edfe95e86cb7292663ed7a38b9adad0d8052a4405e08a438` | yes |
| `backend/app/tests/test_post_classc_p03_formal_second_decision_writer_route_binding.py` | absent | `24783 / 0b4d21e56e2063e408866983a9ba95ee466bbfa84a7a8099a70cc820177f8c79` | yes, created |

The report's final bytes and SHA-256 are sealed externally in the implementation result package; a report cannot safely embed its own final digest.

The following required files remain byte-exact:

| Path | Bytes / SHA-256 |
|---|---|
| `backend/app/api/v1/api.py` | `3391 / 8e049efb8ae1145e3a53764f2fa36f7850bb6dd35d0a54c2cbbe858a860cdd1b` |
| `frontend/src/api/sentigraphApi.js` | `274065 / 188e7f942cdd376324003c0b27a84056149c7a14743aeb9374941f43553c0b87` |
| `frontend/src/pages/InternalAlphaReviewConsole.jsx` | `36158 / 97f92ded390d08cb84f924b34e298e7a14b891b5abbc53fcfbdc5a3fc4dc965b` |

## Implementation design

The generic ledger remains isolated from the formal target:

- `GovernedNonproductionHumanReviewDecisionLedger._require_available()` still rejects the exact formal target.
- `record_governed_nonproduction_human_review_decision` keeps its injected/nonformal behavior.
- `DECISION_FIELDS`, `RECEIPT_FIELDS`, `_IDEMPOTENCY_FIELDS`, `_BOOLEAN_FIELDS`, and `_JSON_FIELDS` remain `38`, `27`, `19`, `8`, and `4` fields respectively.
- The formal primary table and schema are unchanged.
- The accepted first formal decision is append-only and is neither updated nor deleted.

The new private `_identity_for_context(decision_type, context)` requires the exact frozen context keys and exact value types. The generic `_identity_for(decision_type)` delegates with the original `SERVER_OWNED_CONTEXT`. No global context mutation occurs. A formal second context may differ from the frozen context only at `activation_decision_safe_hash`.

The new public `record_second_exact_formal_human_review_decision` accepts only server-side repository root, the strict three-field request, the strict second-activation object and binding hash, and an enabled boolean. It accepts no physical database path. On the protected path it uses one connection, starts `BEGIN IMMEDIATE` before state verification, requires one exact accepted first row, and never retries or reopens.

- `keep_pending_human_review`: requires a fresh activation to enter, verifies identity with the frozen first-row context, keeps row count `1 -> 1`, issues `INSERT=0`, and returns the existing row without mutation.
- `request_more_governance_review`: uses the per-call second context, requires a distinct identity, keeps the first row exact, changes row count `1 -> 2`, and issues at most one insert.
- Commit ambiguity never issues a second insert and never reopens. It returns a paused outcome for later independent read-only audit.

The route preserves the primary gate and adds the default-off formal-second gate plus process-local server-owned activation JSON/SHA configuration. It adds no target-path or database-path environment variable or request field. The request remains exactly `request_schema`, `request_version`, and `decision_type`, with extra fields forbidden. The process-local activation latch is consumed before the dedicated protected writer invocation and is never reset. The GET route is unchanged and obtains no formal-target binding.

## Exact second-activation contract

- Schema: `sentigraph_post_classc_p03_formal_second_decision_activation_v0_1`.
- Version: `0.1`.
- Canonical binding: SHA-256 of canonical JSON using sorted keys, ASCII-safe encoding, and compact separators.
- Exact ordered field list, 33 fields:

1. `activation_schema`
2. `activation_version`
3. `milestone_id`
4. `route_purpose`
5. `repository_identity`
6. `required_branch`
7. `implementation_commit`
8. `implementation_service_sha256`
9. `implementation_route_sha256`
10. `implementation_test_sha256`
11. `implementation_report_sha256`
12. `accepted_p03_design_result_sha256`
13. `accepted_p03_design_acceptance_sha256`
14. `target_identity_safe_hash`
15. `target_authorization_contract_safe_hash`
16. `accepted_first_decision_type`
17. `accepted_first_decision_id`
18. `accepted_first_idempotency_key`
19. `accepted_first_audit_receipt_reference`
20. `accepted_first_decision_canonical_sha256`
21. `required_prestate_row_count`
22. `allowed_mutation_decision_type`
23. `activation_decision_safe_hash`
24. `fresh_runtime_goal_id`
25. `fresh_runtime_approval_sha256`
26. `formal_target_access_session_limit`
27. `sqlite_connection_open_limit`
28. `sqlite_connection_reopen_limit`
29. `decision_insert_limit`
30. `automatic_retry_allowed`
31. `automatic_repair_allowed`
32. `third_decision_allowed`
33. `nonreusable`

Validation requires an exact object, exact field order, exact field types, exact fixed values, lowercase hex identities, a 40-hex implementation commit, a `SENTIGRAPH_` fresh runtime Goal ID, and the exact canonical activation hash. The new activation hash must differ from both the frozen first-row activation provenance and the historical P3 activation binding. Limits are one target session, one SQLite open, zero reopen, at most one insert, zero retry, zero repair, zero third decision, and nonreusable true. No active future activation value is baked into the repository.

## Synthetic validation receipt

All tests used repository-external cache storage, bytecode writing disabled, the project Python, and no application server or HTTP transport.

### Genuine RED

The first focused P03 run was executed before implementation completion and failed genuinely with a missing-contract `AttributeError` for `_identity_for_context`. It was not fabricated or reclassified.

### Final passing evidence

| Validation | Result |
|---|---|
| New focused P03 test file | `22 passed` |
| Accepted fresh-process lazy-router assembly test | `1 passed` |
| Historical P3 plus remaining F11 tests, excluding exactly the known-invalid direct `app.routes` assertion | `103 passed` (`26` P3, `77` remaining F11) |
| Formal-ledger P2 initialization regression | `30 passed` |
| Static route-surface and exact API registration assertion inside remaining F11 | passed |
| Consolidated final blocking gate across all five listed test files | `156 passed`; exactly one known-invalid historical assertion explicitly excluded |
| Changed Python files plus new test `py_compile` | passed |
| `git diff --check` | passed; line-ending notices only, no whitespace errors |

No repository test implementing the repository-external one-shot P4 formal-decision post-write auditor is present. The Work Prompt condition was “P4 audit tests if available and synthetic-only”; therefore P4 test execution is `0`, availability is `false`, and the historical P4 audit result is not reclassified. An unrelated evidence-layer read-only-audit suite was deliberately not presented as formal-decision P4 evidence.

### Preserved known-invalid historical assertion

The combined P3/F11 run directly observed this one failure and preserves it as a failure:

`test_registered_app_exposes_only_post_and_exact_id_get_for_new_family`

Its failure shape was exactly an empty family set from immediate `app.routes` enumeration. Mainline independently classified it as:

`KNOWN_LAZY_INCLUDED_ROUTER_DIRECT_APP_ROUTES_FALSE_NEGATIVE`

It is not reported as PASS, not modified, and not historically reclassified. The accepted fresh-process route-assembly test supplies the replacement registration evidence by validating the lazy-router-aware route contexts, target/aggregate/app counts, GET method, full concrete-path match, no missing aggregate signatures, identical fresh-app signatures, one aggregate include, zero direct target include, and `all_contracts_pass=true`.

## Negative authority and future boundary

- Real formal target / SQLite access: `0 / 0`.
- Provider, collector, database, persistence, production, public, export, delivery: `0`.
- Sentigraph backend/frontend/browser/HTTP/POST/GET: `0`.
- Project Source access/change: `0/0`.
- Generic guard weakened: `false`.
- Formal schema migrated: `false`.
- Existing first decision changed: `false`.
- Frontend or `api.py` changed: `false`.
- Live activation issued: `false`.
- Live POST/runtime authorized: `false`.

Any later live formal-second runtime requires a separately accepted implementation commit, a fresh read-only preflight, a new server-owned nonreusable activation, a distinct one-shot execution authority, and a later independent read-only formal-ledger audit. This report grants none of that authority.
