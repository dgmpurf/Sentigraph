# Sentigraph MVP-F11-P2-RC1 Receipt Truthfulness and Route-mode Conformance Report v1.0

## Decision and privacy status

- `decision = ready`
- `privacy_issue_stop = no`
- `MVP_F11_P2_RC1_status = candidate_completed_pending_chatgpt_acceptance`
- `effective_MVP_F11_P2_status = candidate_repaired_pending_chatgpt_acceptance`
- `effective_MVP_F11_status = candidate_completed_pending_chatgpt_acceptance`
- `MVP_F12_eligibility_candidate_after_chatgpt_acceptance = yes`
- `MVP_F12_authorized = no`
- `MVP_F12_executed = no`

RC1 is a bounded completion repair for two accepted exact-contract findings. It does not authorize formal-ledger initialization, real decision capture, production behavior, or any later milestone.

## Exact RC1 approval

```text
APPROVE_SENTIGRAPH_MVP_F11_P2_RC1_RECEIPT_TRUTHFULNESS_AND_EXACT_ROUTE_MODE_CONFORMANCE_FIXED_MILESTONE_COMPLETION_REPAIR_BIND_REPAIRED_COMMIT_952B77D72C16F85826D292D0F5BCE59CEC1FAC91_AND_ACCEPTED_F11_P1_CONTRACT_BLOB_29D3806A535680247713AE317C1D1C9097F69D06_EXACT_FOUR_FILE_ALLOWLIST_LEDGER_SERVICE_INTERNAL_DECISION_ROUTE_FOCUSED_TEST_AND_NEW_RC1_REPORT_SET_RECEIPT_DECISION_ROW_COUNT_BEFORE_AND_AFTER_TO_NULL_WHEN_ROW_COUNT_OBSERVATION_IS_UNAVAILABLE_PRESERVE_EXACT_INTEGER_COUNTS_ONLY_WHEN_SAFELY_OBSERVED_SET_ONE_EXACT_ROUTE_MODE_INTERNAL_DISABLED_BY_DEFAULT_APPEND_ONLY_NONPRODUCTION_HUMAN_REVIEW_DECISION_LEDGER_FOR_ALL_POST_GET_SUCCESS_DISABLED_REJECTED_UNAVAILABLE_NOT_FOUND_INTEGRITY_AND_FAILURE_RESPONSES_ADD_GENUINE_TDD_RED_AND_EXACT_BRANCH_MATRIX_PRESERVE_CHG_005_GOLDEN_VECTORS_APPEND_ONLY_SQL_TEMPORARY_SQLITE_ONLY_EXISTING_API_REGISTRATION_ORIGINAL_CONTRACT_AND_REPORTS_NO_FORMAL_RUNTIME_TARGET_REAL_HUMAN_DECISION_F10_ROUTE_ADAPTER_HELPER_TARGET_OR_WRITER_GOVERNED_RECORD_MUTATION_PRODUCTION_REVIEW_QUEUE_TRUST_UPGRADE_ANALYSIS_REPORT_FRONTEND_PROJECT_SOURCE_TAG_OR_MVP_F12
```

## Starting identity and classification

- Repository: `dgmpurf/Sentigraph`
- Branch: `main`
- Starting commit and `origin/main`: `952b77d72c16f85826d292d0f5bce59cec1fac91`
- Starting subject: `Repair MVP-F11-P2 exact contract conformance`
- Starting ahead/behind: `0/0`
- Starting worktree: clean
- Accepted F11-P1 contract blob: `29d3806a535680247713ae317c1d1c9097f69d06`
- Accepted F11-P1 contract SHA-256: `dc3e6a696facc1d93cfce0b51218820b6eed8bd7dcbf4e1177d460bdc9e8b152`
- Historical F11-P2 commit: `49f3e00dc1e6d2508b43568b5b926daee9bfb4e3`
- CHG-005-P1 commit: `952b77d72c16f85826d292d0f5bce59cec1fac91`
- CHG-005 repaired service blob: `d378fd7e4a202ba566f28a52fbb0a0ff6375521e`
- CHG-005 focused-test blob: `b22c7384dde77a294084ae9b3fe535a7727a40d7`
- Pre-RC1 route blob: `9ea1fc2b34e60dab26124957cc342a0397dfdcf7`
- Starting classification: `needs_fix_for_remaining_exact_F11_P1_contract_conformance`
- Accepted remaining exact findings: 2

CHG-005 was preserved as a forward commit. RC1 used no revert, amend, reset, rebase, force push, or history rewrite.

## Prompt accounting

- `consumed_engineering_prompts_since_v1_3 = 16`
- `consumed_fixed_prompts_since_v1_3 = 8`
- `consumed_conditional_prompts_since_v1_3 = 6`
- `consumed_risk_prompts_since_v1_3 = 2`
- `remaining_fixed_prompts = 6`
- `remaining_conditional_allowance = 0`
- `remaining_risk_buffer = 0`

No conditional or risk allowance remains. No third exact-contract finding was discovered or repaired.

## Exact four-file allowlist

Exactly these paths comprise RC1:

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/api/v1/routes/internal_alpha_governed_review_decisions.py`
3. `backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py`
4. `docs/health/sentigraph_mvp_f11_p2_rc1_receipt_truthfulness_and_route_mode_conformance_report_v1_0.md`

API registration, the accepted contract, the original F11-P2 report, the CHG-005 report, F10 files, frontend files, Project Source, runtime files, and unrelated files remain outside the change.

## Two confirmed RC1 findings

### Finding 1: receipt row-count truthfulness

Before RC1, unavailable observations could be represented as zero even though no row count had been safely obtained. RC1 changes the two receipt count defaults to nullable values.

The exact 27 receipt fields and their order are unchanged. The only semantic change is:

- unavailable or unknown observation: `decision_row_count_before = null`, `decision_row_count_after = null`
- safely observed or conclusively verified state: exact nonnegative integer values

Zero is retained only when zero was actually observed or conclusively verified.

### Finding 2: one exact route mode

Before RC1, `route_mode` acted as a dynamic branch label. RC1 defines one constant used by both response builders:

```text
internal_disabled_by_default_append_only_nonproduction_human_review_decision_ledger
```

HTTP status, decision payload, and receipt continue to communicate branch outcome. POST remains exactly 13 fields; GET remains exactly 11 fields. No status field was added.

## Genuine TDD RED

Only the focused test changed before the service or route. The smallest RC1 subset was run against the starting implementation:

```text
python -m pytest backend/app/tests/test_mvp_f11_p2_governed_nonproduction_human_review_decision_ledger.py -q --tb=line -k rc1_repair
```

Result:

- failed: 22
- passed: 4
- receipt-truthfulness defect represented: yes
- route-mode defect represented: yes
- unavailable-count failures represented: 5
- exact route constant and POST/GET branch failures represented: 17
- safely observed-count preservation cases already passing: 4

The service and route were not modified until this genuine RED result was recorded.

## Receipt row-count truthfulness matrix

| Branch | Before RC1 repair | After RC1 repair |
| --- | --- | --- |
| Invalid request before database access | unavailable placeholder | `null/null` |
| Frozen server-context mismatch before database access | unavailable placeholder | `null/null` |
| Ledger unavailable before observation | unavailable placeholder | `null/null` |
| Database failure before observation | unavailable placeholder | `null/null` |
| Commit ambiguity with unreadable post-state | unavailable placeholder | `null/null` |
| Successful create | exact integers | exact `before`, `before + 1` |
| Exact idempotent reuse | exact integers | exact equal integers |
| Safely observed identifier conflict | exact integers | exact equal integers |
| Successfully verified commit ambiguity | exact integers | exact verified integers |
| Known rollback after observed pre-state | exact only when conclusive | exact equal integers when conclusively rolled back |

No unavailable branch substitutes `0/0` after RC1. Receipt outcome invariants, fields, field order, warnings, and blockers are unchanged.

## Exact route mode

- Product route constant count: 1
- POST response builders using the constant: all
- GET response builders using the constant: all
- Historical dynamic route-mode response values remaining: 0
- Gate name and semantics: unchanged
- Route family and paths: unchanged
- List, PUT, PATCH, and DELETE routes added: 0

## POST/GET branch matrix

Every row below uses the same exact RC1 route mode.

### POST

| Branch | HTTP | Decision/receipt semantics |
| --- | ---: | --- |
| Gate disabled | 404 | no decision, no receipt |
| Gate enabled; ledger unavailable | 503 | no decision, no receipt |
| Created | 201 | decision plus created receipt |
| Idempotent reuse | 200 | existing decision plus reuse receipt |
| Unsupported decision | 422 | no decision plus blocked receipt |
| Binding mismatch | 409 | no decision plus blocked receipt |
| Idempotency conflict | 409 | no decision plus conflict receipt |
| Paused ambiguity | 503 | no decision plus paused receipt |
| Bounded ledger failure | 500 | no decision plus bounded receipt |

### GET

| Branch | HTTP | Decision semantics |
| --- | ---: | --- |
| Malformed decision ID | 422 | no decision |
| Gate disabled | 404 | no decision |
| Ledger unavailable before lookup | 503 | no decision |
| Exact decision found | 200 | exact decision |
| Exact decision not found | 404 | no decision |
| Integrity blocked | 409 | no decision |
| Bounded lookup failure | 503 | no decision |

The route mode is not a success, failure, readiness, or status label.

## CHG-005 preservation

The following accepted CHG-005 behavior remains unchanged:

- ledger scope: `governed_nonproduction_record_human_review_only`
- decision status: `recorded_append_only_nonproduction`
- exact 19-field idempotency material
- direct first-32 identifier derivation
- exact 38-field decision record
- exact 27-field receipt and seven outcomes
- canonical decision hashing and actual-column verification
- append-only persistence and one insert operation
- rollback and commit-ambiguity semantics
- disabled-by-default and explicitly injected temporary-database posture

Canonical golden vectors remain:

- keep pending: `b666c0f03a975c94e6b3b248bd05cdc95fdeb596b950abbe6a4a029f0935b3db`
- request more review: `5f9f0459a81b470e4e4cbc1d41bc96832d550ee130c86ff791920ff8c92b09cc`

Both exact vector tests passed after RC1.

## Focused and nearby validation

- RC1 repair-focused subset: 26 passed
- Full F11-P2 focused module: 78 passed
- Minimum nearby API/internal-route safety selection: 5 passed
- CHG-005 golden-vector selection: 2 passed
- Modified service, route, and test compilation: PASS
- Receipt field count: 27
- Receipt order unchanged: yes
- Receipt default counts: `None/None`
- Safely observed integer-count branches: PASS
- Exact route-mode literal count: 1
- All POST/GET response builders use the exact constant: yes
- Historical dynamic route-mode values: 0
- Append-only persistence scan: PASS
- Forbidden dependency/call scan: PASS
- Formal-target absence check: PASS
- Diff and no-index whitespace checks: PASS

The Windows line-ending advisory was non-failing and did not represent a whitespace defect.

## Unchanged frozen files

- API-registration blob: `d9523f761537af0e7a08ce834d6e3b36c9117a24`
- Original F11-P2 report blob: `496423f0b675c202ffa2070c39eaef6464d9bd0b`
- CHG-005-P1 report blob: `d6b3f8e7c758a3e75fb632e3a36ce5922c752e15`
- Accepted F11-P1 contract blob: `29d3806a535680247713ae317c1d1c9097f69d06`

The API registration, accepted contract, and prior reports were not edited.

## Temporary-SQLite, formal-target, and append-only proof

- Persistence validation used pytest-owned temporary databases only.
- Formal runtime target existed before RC1: no
- Formal runtime target existed after validation: no
- Formal-target initialization/access count: 0
- Actual human-review decisions captured: 0
- Plain insert operation count: unchanged at 1
- Existing-row mutation/removal, replacement, or mutation-producing conflict operation: absent

No raw database statement, physical temporary path, traceback, private exception detail, identity detail, raw evidence, or secret is reproduced here.

## Safety and privacy boundaries

- F10 route/helper/target/writer runtime count: 0
- Governed-record mutation count: 0
- Production Review Queue actions: 0
- Trust upgrades: 0
- Analysis/report/correction/revocation/export/delivery actions: 0
- Frontend changes: 0
- Project Source changes: 0
- Tags/releases: 0
- New unapproved RC1 findings: 0
- Privacy issue stop: no

## Git readiness result

- Required changed-file count: 4
- Approved commit subject: `Repair MVP-F11-P2 receipt and route conformance`
- Push target: current `main` to `origin/main`
- Forbidden history operations: unused
- Tag: no
- Pre-finalization result: ready for exact cached validation, commit, and push

The terminal task receipt records the resulting commit identity, push, final `0/0` alignment, and clean worktree because this report is part of that commit.

## Source recommendation

Only after independent ChatGPT acceptance:

- Canonical 00: replace
- Canonical 03: replace
- Canonical 08: replace
- Canonical 09: replace
- Canonical 05: no change
- Source 11: no change

Project Source remains unchanged during RC1.

## Next boundary

Do not initialize the formal ledger. Do not capture a real human-review decision. Do not start MVP-F12.

After independent ChatGPT acceptance of RC1 and effective acceptance of MVP-F11-P2 and MVP-F11, a separate authorization must select the route for formal-target initialization and first-real-human-review-decision governance.
