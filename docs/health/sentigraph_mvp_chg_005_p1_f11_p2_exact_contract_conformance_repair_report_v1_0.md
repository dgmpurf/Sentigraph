# Sentigraph MVP-CHG-005-P1 F11-P2 Exact Contract Conformance Repair Report v1.0

## Decision and privacy status

- `decision = ready`
- `privacy_issue_stop = no`
- `MVP_CHG_005_P1_status = candidate_completed_pending_chatgpt_acceptance`
- `effective_MVP_F11_P2_status = candidate_repaired_pending_chatgpt_acceptance`
- `effective_MVP_F11_status = candidate_completed_pending_chatgpt_acceptance`
- `MVP_F12_eligibility_candidate_after_chatgpt_acceptance = yes`
- `MVP_F12_authorized = no`
- `MVP_F12_executed = no`

This report records a bounded forward repair of four accepted exact-contract findings. It does not approve a real human-review decision, initialize a formal ledger, authorize production behavior, or start a later milestone.

## Exact CHG-005-P1 approval

```text
APPROVE_SENTIGRAPH_MVP_CHG_005_P1_F11_P2_EXACT_F11_P1_CONTRACT_CONFORMANCE_FORWARD_REPAIR_RISK_BUFFER_BIND_COMMIT_49F3E00DC1E6D2508B43568B5B926DAEE9BFB4E3_AND_ACCEPTED_F11_P1_CONTRACT_SHA_DC3E6A696FACC1D93CFCE0B51218820B6EED8BD7DCBF4E1177D460BDC9E8B152_EXACT_THREE_FILE_ALLOWLIST_SERVICE_FOCUSED_TEST_AND_NEW_REPAIR_REPORT_SET_LEDGER_SCOPE_TO_GOVERNED_NONPRODUCTION_RECORD_HUMAN_REVIEW_ONLY_SET_DECISION_STATUS_TO_RECORDED_APPEND_ONLY_NONPRODUCTION_FOR_BOTH_ALLOWED_DECISION_TYPES_DERIVE_IDEMPOTENCY_FROM_THE_EXACT_ACCEPTED_P1_NINETEEN_FIELDS_INCLUDE_REQUEST_SCHEMA_AND_REQUEST_VERSION_EXCLUDE_LEDGER_SCOPE_AND_REVIEWER_IDENTITY_VERIFIED_DERIVE_DECISION_ID_AND_AUDIT_RECEIPT_REFERENCE_FROM_THE_DIRECT_FIRST_32_LOWERCASE_HEX_CHARACTERS_OF_IDEMPOTENCY_KEY_ADD_EXACT_CANONICAL_GOLDEN_VECTOR_TDD_AND_RERUN_FOCUSED_AND_MINIMUM_NEARBY_VALIDATION_PRESERVE_EXISTING_ROUTE_API_REGISTRATION_AND_ORIGINAL_IMPLEMENTATION_REPORT_TEMPORARY_SQLITE_ONLY_NO_FORMAL_RUNTIME_TARGET_REAL_HUMAN_DECISION_F10_ROUTE_ADAPTER_HELPER_TARGET_GOVERNED_RECORD_WRITER_OR_MUTATION_PRODUCTION_REVIEW_QUEUE_TRUST_UPGRADE_ANALYSIS_REPORT_FRONTEND_PROJECT_SOURCE_TAG_OR_LATER_MILESTONE
```

## Starting identity and classification

- Repository: `dgmpurf/Sentigraph`
- Branch: `main`
- Starting commit: `49f3e00dc1e6d2508b43568b5b926daee9bfb4e3`
- Starting commit subject: `Implement MVP-F11-P2 human review decision ledger`
- Starting `origin/main`: `49f3e00dc1e6d2508b43568b5b926daee9bfb4e3`
- Starting ahead/behind: `0/0`
- Starting worktree: clean
- Accepted F11-P1 contract blob: `29d3806a535680247713ae317c1d1c9097f69d06`
- Accepted F11-P1 contract SHA-256: `dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152`
- `MVP_F11_P1_status = completed_and_independently_accepted`
- `historical_MVP_F11_P2_commit = 49f3e00dc1e6d2508b43568b5b926daee9bfb4e3`
- Historical classification: `needs_fix_for_exact_F11_P1_contract_conformance`
- `revert_required = no`
- `forward_repair_required = yes`

The historical commit was preserved. No revert, amend, reset, rebase, force push, or history rewrite was used.

## Prompt accounting

- `consumed_engineering_prompts_since_v1_3 = 15`
- `consumed_fixed_prompts_since_v1_3 = 7`
- `consumed_conditional_prompts_since_v1_3 = 6`
- `consumed_risk_prompts_since_v1_3 = 2`
- `remaining_fixed_prompts = 7`
- `remaining_conditional_allowance = 0`
- `remaining_risk_buffer = 0`

The exhausted risk buffer limits this repair to the four approved findings. No fifth finding was discovered or repaired.

## Exact three-file allowlist

Exactly these three paths comprise the change:

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py`
3. `docs/health/sentigraph_mvp_chg_005_p1_f11_p2_exact_contract_conformance_repair_report_v1_0.md`

The route, API registration, accepted F11-P1 contract, original F11-P2 implementation report, frontend, F10 files, Project Source, runtime files, and all unrelated files remain outside the change.

## Four historical findings

### Finding 1: ledger scope

The historical service used a synthetic implementation label where the accepted contract required the exact governed-nonproduction record scope.

Repaired constant:

```text
LEDGER_SCOPE = governed_nonproduction_record_human_review_only
```

Every newly built decision record uses this value.

### Finding 2: decision status

The historical service selected a persisted status from the decision type. The accepted contract requires one append-only nonproduction status for both allowed decision types.

Repaired constant:

```text
DECISION_STATUS = recorded_append_only_nonproduction
```

Both allowed decisions retain their distinct `decision_type`; both persist the same fixed `decision_status`. The two historical dynamic status literals are absent from the repaired product service.

### Finding 3: exact idempotency inputs

The historical idempotency object included two excluded values and omitted the request schema/version bindings. It now contains exactly 19 unique fields:

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

`request_schema` is bound to `REQUEST_SCHEMA`, and `request_version` is bound to `REQUEST_VERSION`. The idempotency object excludes `ledger_scope`, `reviewer_identity_verified`, `recorded_at`, `decision_status`, `decision_id`, `audit_receipt_reference`, and `decision_canonical_hash`.

Canonicalization remains compact sorted-key UTF-8 JSON with non-ASCII preservation and SHA-256 lowercase hexadecimal output.

### Finding 4: direct identifier derivation

The historical service applied second-level hashes to derive identifiers. The repaired derivation is direct:

```text
decision_id = ghrd- + idempotency_key first 32 lowercase hexadecimal characters
audit_receipt_reference = ghrd-receipt- + idempotency_key first 32 lowercase hexadecimal characters
```

The historical second-level decision and receipt hash inputs are absent from the repaired service.

## Genuine repair RED

Only the focused test was modified before the service. The smallest repair subset was then run against the historical service:

```text
python -m pytest backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py -q --tb=line -k exact_contract_conformance_repair
```

Result:

- failed: 11
- passed: 0
- ledger-scope defect represented: yes
- decision-status defect represented: yes
- idempotency-input defect represented: yes
- direct-identifier defect represented: yes
- both golden vectors failed against the historical implementation: yes

The service was not modified until this genuine RED result was recorded.

## Exact code changes

The service change is limited to:

- replacing the ledger-scope constant;
- replacing the decision-type status mapping with one fixed status constant;
- replacing the idempotency field tuple with the accepted exact 19-field tuple;
- binding request schema/version into the idempotency material;
- excluding ledger scope and identity-verification state from that material;
- deriving both identifiers directly from the first 32 characters of the idempotency key; and
- keeping existing-record identity verification aligned with the repaired hash-material boundary.

The focused test adds exact constants, hash-material capture, participation/exclusion checks, fixed-status checks for both decisions, direct-identifier checks, second-level-hash absence checks, and both canonical golden vectors.

No architecture, route, response envelope, schema field order, outcome mapping, or persistence model was redesigned.

## Canonical golden vectors

### `keep_pending_human_review`

- `idempotency_key = b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db`
- `decision_id = ghrd-b666c0f03a975c94e6b3b248bd05cdc9`
- `audit_receipt_reference = ghrd-receipt-b666c0f03a975c94e6b3b248bd05cdc9`

### `request_more_governance_review`

- `idempotency_key = 5f9f0459a81b470e4e4cbc1d41bc96832d550ee130c86ff791920ff8c92b09cc`
- `decision_id = ghrd-5f9f0459a81b470e4e4cbc1d41bc9683`
- `audit_receipt_reference = ghrd-receipt-5f9f0459a81b470e4e4cbc1d41bc9683`

Both vectors are locked by focused tests.

## Focused and nearby validation

### Exact repair subset

```text
11 passed
```

### Full existing F11-P2 focused module

```text
52 passed
```

This preserves the exact three request fields, two decision types, 38 decision-record fields, 27 receipt fields, seven outcomes, canonical decision hash, append-only behavior, uniqueness, actual-column verification, idempotent reuse, second-decision append, rollback, commit ambiguity, disabled defaults, explicit temporary database injection, formal-target rejection, and route/API behavior.

### Minimum nearby API and route-safety regression

```text
5 passed
```

This selection covered generic API health registration and the existing F11 disabled-gate, enabled-without-ledger, exact API-registration, and exact route-surface safety cases.

### Additional validation

- modified service/test `py_compile`: PASS
- static exact-contract scan: PASS
- ledger-scope exact literal count: 1
- fixed decision status present: yes
- historical dynamic status literals absent from product service: yes
- idempotency fields: 19, unique, exact
- request schema/version included: yes
- ledger scope excluded: yes
- identity-verification state excluded: yes
- direct first-32 derivation: yes
- second-level identifier derivations absent: yes
- append-only SQL scan: PASS
- forbidden dependency/call scan: PASS
- `git diff --check`: PASS
- no-index whitespace check: PASS

The Windows line-ending advisory did not represent a whitespace defect.

## Unchanged route, API, and original-report proof

- Route blob: `9ea1fc2b34e60dab26124957cc342a0397dfdcf7` — unchanged
- API-registration blob: `d9523f761537af0e7a08ce834d6e3b36c9117a24` — unchanged
- Original F11-P2 implementation-report blob: `496423f0b675c202ffa2070c39eaef6464d9bd0b` — unchanged

No route or API adaptation was needed for the repair.

## Append-only and temporary-SQLite proof

- The service still contains exactly one plain insert operation.
- Existing-row mutation/removal, replacement, and conflict-upsert operations remain absent.
- Unique decision, idempotency, and receipt bindings remain preserved.
- Persistence tests used only pytest-owned temporary SQLite databases.
- The formal runtime target remained absent before and after validation.
- Formal-target initialization/access count: 0
- Actual human-review decisions captured: 0

No raw database statement, physical temporary path, private exception detail, or reviewer identity is included in this report.

## Safety and no-side-effect boundaries

- F10 route runtime calls: 0
- F10 adapter/helper calls: 0
- F10 target accesses: 0
- governed-record writer calls: 0
- governed-record mutations: 0
- production Review Queue actions: 0
- trust upgrades: 0
- downstream analysis/report actions: 0
- correction/revocation actions: 0
- export/delivery actions: 0
- frontend changes: 0
- Project Source changes: 0
- tags/releases: 0
- newly discovered unapproved contract findings: 0

The route remains disabled by default. Public readiness, production readiness, operator readiness, review-queue runtime, and automatic trust upgrade remain false or unavailable.

## Git readiness result

- Exact changed-file count required: 3
- Exact changed-file allowlist validation: required before commit
- Cached whitespace validation: required before commit
- Approved commit subject: `Repair MVP-F11-P2 exact contract conformance`
- Push target: current `main` to `origin/main`
- Amend/rebase/force/history rewrite: forbidden and unused
- Tag: no
- Pre-finalization classification: ready for cached validation, exact commit, and push

The terminal task receipt records the resulting commit identity, push, final `0/0` alignment, and clean worktree because the report itself is part of that commit.

## Source recommendation

If this repair is later independently accepted:

- Canonical 00: replace
- Canonical 03: replace
- Canonical 08: replace
- Canonical 09: replace
- Canonical 05: no change
- Source 11: no change

Project Source remains unchanged until independent ChatGPT acceptance.

## Next boundary

Do not initialize the formal ledger. Do not capture a real human-review decision. Do not start MVP-F12.

After independent acceptance of CHG-005-P1 and effective acceptance of MVP-F11-P2 and MVP-F11, a separate authorization must select the route for formal-target initialization and the first real human-review decision governance sequence.
