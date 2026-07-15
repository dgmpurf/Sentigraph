# Sentigraph MVP-F12-P2 Formal Decision-ledger Initialization Report v1.0

## Historical initial decision and privacy

```text
historical_initial_P2_decision = blocked_one_time_formal_execution_result_unavailable
privacy_issue_stop = no
do_not_rerun = yes
historical_initial_MVP_F12_P2_status = blocked_pending_separate_recovery_authorization
historical_initial_formal_target_state = unknown_or_ambiguous
actual_human_review_decision_captured = no
MVP_F12_P3_authorized = no
MVP_F12_P3_executed = no
MVP_F12_P4_authorized = no
MVP_F12_P4_executed = no
```

The sole authorized execution was consumed. Its captured artifact failed the required UTF-8 validation, so this report does not infer an initialization outcome, target state, receipt, or SQLite counter.

## Exact P2 approval

```text
APPROVE_SENTIGRAPH_MVP_F12_P2_EXACT_FORMAL_DECISION_LEDGER_INITIALIZATION_PLANNED_FIXED_MILESTONE_BIND_STARTING_COMMIT_C50E54ABD74AAD98F5DF15044A9E51B58AEFF168_AND_ACCEPTED_F12_P1_CONTRACT_BLOB_C2B9645BA1EE2724BA4A023FA267D4DFB5059302_AND_CONTRACT_SHA256_0D0E4C0C12A534EB5F523FFFB4430F223480339D197EC031C5621F6E1312B4B8_AND_TARGET_IDENTITY_SAFE_HASH_4D2B1EE233433B774D30B82B57C77A58A5AAB6427FCF8454A7BF05E5590D7202_AND_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH_DE3CBFE49DFEB836F3BC8B95B5A46D51366892E2277F86402306EDBFD543EA4D_EXACT_THREE_FILE_REPOSITORY_ALLOWLIST_DECISION_LEDGER_SERVICE_NEW_P2_FOCUSED_TEST_AND_P2_INITIALIZATION_HEALTH_REPORT_IMPLEMENT_ONE_DEDICATED_EXACT_FORMAL_PROFILE_INITIALIZATION_OPERATION_WITH_INTERNAL_LOGICAL_TARGET_RESOLUTION_NO_CALLER_SUPPLIED_PHYSICAL_TARGET_NO_ROUTE_BINDING_AND_NO_RELAXATION_OF_THE_EXISTING_SYNTHETIC_FORMAL_TARGET_GUARD_RUN_GENUINE_TDD_RED_FOCUSED_SYNTHETIC_TESTS_NEARBY_F11_REGRESSIONS_PYCOMPILE_STATIC_SAFETY_AND_DIFF_CHECKS_THEN_EXECUTE_EXACTLY_ONE_HASHED_READBACK_VERIFIED_AST_AUDITED_REPOSITORY_EXTERNAL_UTF8_INITIALIZATION_RUNNER_WITH_ONE_FORMAL_TARGET_ACCESS_SESSION_ONE_SQLITE_CONNECTION_OPEN_ZERO_REOPENS_MAXIMUM_ONE_SCHEMA_DDL_ZERO_DECISION_TABLE_DML_ZERO_DECISION_INSERTS_ZERO_DECISION_WRITER_INVOCATIONS_ZERO_ROUTE_INVOCATIONS_AND_NO_AUTOMATIC_RETRY_ALLOW_ONLY_ABSENT_TARGET_INITIALIZED_EXACT_EMPTY_OR_EXISTING_EXACT_EMPTY_VERIFIED_WITHOUT_MUTATION_BLOCK_EXISTING_NONEMPTY_SCHEMA_MISMATCH_UNRELATED_TABLE_TARGET_IDENTITY_MISMATCH_MALFORMED_TARGET_OR_COMMIT_AMBIGUITY_WITHOUT_REPAIR_MIGRATION_TRUNCATION_REPLACEMENT_SECOND_CONNECTION_OR_SECOND_EXECUTION_EMIT_AND_PRESERVE_ONE_EXACT_TWENTY_FIVE_FIELD_INITIALIZATION_RECEIPT_WITH_ONE_OF_SEVEN_FROZEN_OUTCOMES_COMPUTE_ITS_CANONICAL_SHA256_DELETE_AND_VERIFY_DELETION_OF_THE_EXTERNAL_RUNNER_AND_STOP_NO_REAL_HUMAN_REVIEW_DECISION_NO_P3_ACTIVATION_HASH_NO_F10_ACCESS_NO_GOVERNED_RECORD_MUTATION_NO_FRONTEND_NO_PRODUCTION_REVIEW_QUEUE_TRUST_UPGRADE_ANALYSIS_REPORT_CORRECTION_REVOCATION_EXPORT_DELIVERY_PROJECT_SOURCE_TAG_RELEASE_OR_LATER_PHASE
```

## Starting state and accepted anchors

- Starting commit: `c50e54abd74aad98f5df15044a9e51b58aeff168`
- Branch: `main`
- Accepted P1 contract blob: `c2b9645ba1ee2724ba4a023fa267d4dfb5059302`
- Accepted P1 contract SHA-256: `0d0e4c0c12a534eb5f523fffb4430f223480339d197ec031c5621f6e1312b4b8`
- Target identity safe hash: `4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202`
- Target authorization contract safe hash: `de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d`
- Starting service blob: `b9d74ca5d3d593fbe27043dcb7db0a76e25d4056`
- Existing F11 focused-test blob: `02aaa25df98348caeb501e9f23ae593d0a590906`
- Internal route blob: `5dd5033f1de76cac86087a2e50d2a8fda74102ee`
- API-registration blob: `d9523f761537af0e7a08ce834d6e3b36c9117a24`
- F11-P2-RC1 report blob: `f60a4775cd34d034c739be14e063230262cdf961`

No runtime directory or formal target was enumerated or pre-inspected.

## Goal lifecycle and prompt accounting

```text
goal_requested = yes
goal_activation_verified = yes
goal_completion_verified = no
consumed_engineering_prompts_since_v1_3 = 19
consumed_fixed_prompts_since_v1_3 = 11
consumed_conditional_prompts_since_v1_3 = 6
consumed_risk_prompts_since_v1_3 = 2
remaining_fixed_prompts = 3
remaining_conditional_allowance = 0
remaining_risk_buffer = 0
```

## Exact repository allowlist

1. `backend/app/services/governed_nonproduction_human_review_decision_ledger.py`
2. `backend/app/tests/test_mvp_f12_p2_formal_decision_ledger_initialization.py`
3. `docs/health/sentigraph_mvp_f12_p2_formal_decision_ledger_initialization_report_v1_0.md`

## Genuine TDD RED and implemented operation

- RED command: `python -m pytest backend/app/tests/test_mvp_f12_p2_formal_decision_ledger_initialization.py -q --tb=line -k public_operation_signature_and_disabled_default`
- RED failed/passed: `1/0`.
- RED reason: exact public initialization symbol absent.
- Formal-target/SQLite access during RED: `0/0`.

```python
def initialize_exact_formal_governed_nonproduction_human_review_decision_ledger(
    *,
    repository_root: str | Path,
    enabled: bool = False,
) -> dict[str, Any]:
```

The operation is disabled by default, validates the accepted contract before target access, resolves only the frozen logical target internally, and does not invoke the generic initializer, writer, or route.

## Preserved synthetic guard and validation

`_formal_target_selected` and `GovernedNonproductionHumanReviewDecisionLedger._require_available` remain unchanged. The generic class continues rejecting the formal target.

- New P2 focused module: `30 passed`; all `35` required controls covered.
- Existing F11-P2 focused module: `78 passed`.
- Nearby API/internal-route safety selection: `5 passed`.
- Modified service and new test py_compile: PASS.
- Static safety and diff checks: PASS.

## Pre-one-time freeze

- Service SHA-256: `e2f6891b47a2cf065b0a7fc252b7bcb05efa2cbccde4162be233496ce31a70ba`
- New test SHA-256: `01e637f02ce42fb66c5a1430fd8a39cfc60d62884a867860707c690c3b05f6ff`
- Accepted P1 contract, route, and API registration: unchanged.

## Runner hash, AST audit, and execution

- Runner SHA-256: `ba422d870edf80688c3327fb286ae61c7fc0a53d0023c0320d0101902b7078b3`
- UTF-8 source readback and AST audit: PASS.
- Operation callsites: `1`.
- Loops/retries and forbidden imports/calls: `0/0`.
- Formal runner execution count: `1`.
- Formal operation invocation count: `1`.
- Process exit: `0`.
- Captured result validation: blocked because the artifact was not valid UTF-8.
- Executed runner deleted and deletion verified: yes.
- Result artifact retained without a second read: yes.

## Initialization receipt and formal target outcome

```text
initialization_receipt = unavailable
initialization_receipt_canonical_sha256 = unavailable
receipt_field_count = unavailable
formal_target_preexistence_classification = unavailable
formal_target_outcome = unknown_or_ambiguous
formal_decision_ledger_state = unknown_or_ambiguous
```

No success outcome is claimed. The existing result artifact must not be reread, transcoded, deleted, or otherwise processed without separate exact recovery authorization.

## No-side-effect and uncertainty proof

```text
formal runner executions = 1
formal operation invocations = 1
formal target access sessions = unavailable
SQLite opens = unavailable
SQLite reopens = unavailable
schema DDL = unavailable
decision-table DML = 0
decision INSERTs = 0
decision writer calls = 0
route calls = 0
F10 calls = 0
governed-record mutations = 0
human-review decisions captured = 0
frontend actions = 0
production/downstream actions = 0
automatic retries = 0
automatic repairs = 0
second executions = 0
Project Source changes = 0
tag/release creations = 0
```

## Git posture

```text
stage = no
commit = no
push = no
tag = no
```

The three allowlisted diagnostic files remain local and unstaged.

## Source recommendation

Project Source remains unchanged. The success-only Source replacement recommendation is not activated while the formal outcome is ambiguous.

## Next boundary

Do not start P3 or P4. Do not rerun the operation or inspect the formal target. Any recovery requires a separate exact authorization limited to the already-captured external result artifact; it must preserve the consumed one-execution boundary.

## P2-R1 bounded preserved-result recovery

```text
historical_P2_R1_decision = blocked_receipt_field_order_mismatch
artifact_binary_open_count = 1
artifact_binary_read_count = 1
second_artifact_read_count = 0
recovery_success_gate_passed = no
initialization_receipt = unavailable
initialization_receipt_canonical_sha256 = unavailable
preserved_result_artifact_deleted = no
preserved_result_artifact_retained = yes
recovery_validator_deleted = yes
formal_operation_reruns = 0
formal_target_accesses_during_recovery = 0
SQLite_accesses_during_recovery = 0
stage = no
commit = no
push = no
```

The single authorized recovery read used the deterministic BOM-declared UTF-16LE branch and recovered one strict JSON object, but the object's insertion order did not match the frozen 25-field order. No receipt or canonical receipt hash is accepted. The preserved result artifact remains retained without another content read, and the nonreusable recovery validator was deleted.

## P2-R2 canonical transport-order reconciliation

~~~text
P2_R2_decision = ready
privacy_issue_stop = no
MVP_F12_P2_status = candidate_completed_pending_chatgpt_acceptance
formal_decision_ledger_state = initialized_exact_empty
actual_human_review_decision_captured = no
MVP_F12_P3_eligibility_candidate_after_chatgpt_acceptance = yes
MVP_F12_P3_authorized = no
MVP_F12_P3_executed = no
MVP_F12_P4_authorized = no
MVP_F12_P4_executed = no
~~~

### Exact R2 approval

~~~text
APPROVE_SENTIGRAPH_MVP_F12_P2_R2_CANONICAL_JSON_TRANSPORT_KEY_ORDER_RECONCILIATION_AND_RECEIPT_ACCEPTANCE_FIXED_MILESTONE_COMPLETION_REPAIR_RESUME_EXISTING_P2_GOAL_NO_REPLACEMENT_GOAL_BIND_REPOSITORY_HEAD_C50E54ABD74AAD98F5DF15044A9E51B58AEFF168_AND_FROZEN_SERVICE_SHA256_E2F6891B47A2CF065B0A7FC252B7BCB05EFA2CBCCDE4162BE233496CE31A70BA_AND_FROZEN_TEST_SHA256_01E637F02CE42FB66C5A1430FD8A39CFC60D62884A867860707C690C3B05F6FF_AND_CURRENT_REPORT_SHA256_5EABD443C4E1CA249B8DDBD6EB15EE459440BE2132A69993B6FB60055143EC8A_AND_EXACT_PRESERVED_ARTIFACT_RAW_SHA256_F99DBE0B442F128AB4DDC7059D6C38EA07AE8DAD106ED8386B60FAADD4D8F26C_AND_EXACT_ARTIFACT_BYTE_COUNT_2318_AND_ENCODING_BOM_DECLARED_UTF16LE_AND_PRIOR_RECOVERY_VALIDATOR_SHA256_565A3E5998BEEAFBCCC44323FA4FDBAB961D3FA5C380D8509FCDA7116B6E5682_AUTHORIZE_ONLY_THE_SAME_EXACT_ALREADY_KNOWN_PRESERVED_RESULT_ARTIFACT_ALLOW_EXACTLY_ONE_ADDITIONAL_BINARY_OPEN_AND_ONE_READ_OF_AT_MOST_65537_BYTES_WITHOUT_DIRECTORY_ENUMERATION_PATH_DISCOVERY_GLOBBING_SEARCH_OR_FALLBACK_REQUIRE_BYTE_COUNT_2318_AND_RAW_SHA256_F99DBE0B442F128AB4DDC7059D6C38EA07AE8DAD106ED8386B60FAADD4D8F26C_BEFORE_RECEIPT_ACCEPTANCE_REQUIRE_EXACT_BOM_DECLARED_UTF16LE_STRICT_DECODE_NO_REPLACEMENT_CHARACTER_EXACTLY_ONE_STRICT_JSON_OBJECT_NO_DUPLICATE_KEYS_NO_NONSTANDARD_NUMERIC_CONSTANTS_REQUIRE_THE_EXACT_FROZEN_TWENTY_FIVE_KEY_SET_AND_ACCEPT_TRANSPORT_ORDER_ONLY_IF_IT_EQUALS_THE_EXACT_LEXICOGRAPHIC_SORT_ORDER_OF_THOSE_TWENTY_FIVE_KEYS_TREAT_THIS_ONLY_AS_CANONICAL_JSON_TRANSPORT_ORDER_AND_NOT_AS_A_CHANGE_TO_THE_FROZEN_RECEIPT_SCHEMA_ORDER_RECONSTRUCT_THE_RECEIPT_IN_MEMORY_IN_THE_FROZEN_TWENTY_FIVE_FIELD_SCHEMA_ORDER_VALIDATE_EXACT_TYPES_NULL_SEMANTICS_CONSTANTS_ONE_OF_SEVEN_OUTCOMES_AND_ALL_SUCCESS_INVARIANTS_AND_COMPUTE_THE_CANONICAL_RECEIPT_SHA256_WITH_ENSURE_ASCII_FALSE_SORT_KEYS_TRUE_COMPACT_SEPARATORS_UTF8_IF_AND_ONLY_IF_THE_OUTCOME_IS_INITIALIZED_EXACT_EMPTY_FORMAL_DECISION_LEDGER_OR_VERIFIED_EXISTING_EXACT_EMPTY_FORMAL_DECISION_LEDGER_AND_ALL_INVARIANTS_PASS_UPDATE_ONLY_THE_EXISTING_P2_HEALTH_REPORT_PRESERVE_BOTH_HISTORICAL_BLOCKED_OUTCOMES_DELETE_AND_VERIFY_DELETION_OF_THE_EXACT_RESULT_ARTIFACT_RETAIN_FROZEN_SERVICE_AND_TEST_BYTES_RUN_STATIC_REPORT_AND_GIT_DIFF_VALIDATION_AND_READY_ONLY_COMMIT_PUSH_THE_EXISTING_EXACT_THREE_FILE_ALLOWLIST_IF_RAW_IDENTITY_ENCODING_JSON_KEY_SET_EXACT_LEXICOGRAPHIC_TRANSPORT_ORDER_TYPES_VALUES_OUTCOME_OR_SUCCESS_INVARIANTS_FAIL_PRESERVE_THE_ARTIFACT_STOP_WITH_NO_COMMIT_AND_NO_FURTHER_READ_NO_FORMAL_INITIALIZER_RERUN_NO_SECOND_RUNNER_NO_FORMAL_TARGET_RUNTIME_OR_SQLITE_ACCESS_NO_SERVICE_ROUTE_WRITER_F10_CALL_OR_SERVICE_TEST_EDIT_NO_TEST_OR_PYCOMPILE_RERUN_NO_P3_ACTIVATION_HASH_NO_REAL_HUMAN_REVIEW_DECISION_NO_FRONTEND_PRODUCTION_PROJECT_SOURCE_TAG_RELEASE_OR_LATER_PHASE
~~~

### Same-Goal lifecycle and prompt accounting

~~~text
goal_resume_requested = yes
goal_resume_verified = yes
goal_completion_verified = no
replacement_goal_created = no
consumed_engineering_prompts_since_v1_3 = 21
consumed_fixed_prompts_since_v1_3 = 13
consumed_conditional_prompts_since_v1_3 = 6
consumed_risk_prompts_since_v1_3 = 2
remaining_fixed_prompts = 1
remaining_conditional_allowance = 0
remaining_risk_buffer = 0
~~~

### Frozen implementation and recovery identities

- Frozen service SHA-256: e2f6891b47a2cf065b0a7fc252b7bcb05efa2cbccde4162be233496ce31a70ba
- Frozen test SHA-256: 01e637f02ce42fb66c5a1430fd8a39cfc60d62884a867860707c690c3b05f6ff
- Original runner SHA-256: ba422d870edf80688c3327fb286ae61c7fc0a53d0023c0320d0101902b7078b3
- R1 validator SHA-256: 565a3e5998beeafcbcc44323fa4fdbab961d3fa5c380d8509fcda7116b6e5682
- R2 validator SHA-256: 38166dd9a4f45a0408a57344844cb427d47e594f7176af1424cf5237c994249b
- Raw artifact SHA-256: f99dbe0b442f128ab4ddc7059d6c38ea07ae8dad106ed8386b60faadd4d8f26c
- Raw artifact byte count: 2318
- Detected encoding: bom_declared_utf16le
- R2 binary opens/reads: 1/1
- Cumulative result-artifact recovery reads: 2
- Further artifact reads: 0

### Transport order and frozen schema order

The original runner used sort_keys=True, so the artifact carried canonical lexicographic transport order. R2 accepts only that one exact transport sequence; it does not alter the frozen receipt schema or future receipt representation.

Observed transport order:

~~~json
["blockers","decision_row_count","decision_table_dml_statement_count","exact_empty_verified","exact_schema_verified","final_sidecar_count","human_review_required","initialization_action","integrity_result","no_automatic_trust_upgrade","outcome","primary_table","production_ready","receipt_schema","receipt_version","schema_ddl_statement_count","schema_version","sqlite_connection_open_count","sqlite_connection_reopen_count","target_authorization_contract_safe_hash","target_identity_safe_hash","target_kind","target_logical_label","target_preexistence_classification","warnings"]
~~~

Frozen semantic schema order:

~~~json
["receipt_schema","receipt_version","outcome","target_kind","target_logical_label","target_identity_safe_hash","target_authorization_contract_safe_hash","target_preexistence_classification","initialization_action","schema_version","primary_table","sqlite_connection_open_count","sqlite_connection_reopen_count","schema_ddl_statement_count","decision_table_dml_statement_count","decision_row_count","exact_schema_verified","exact_empty_verified","integrity_result","final_sidecar_count","human_review_required","no_automatic_trust_upgrade","production_ready","warnings","blockers"]
~~~

### Reconstructed initialization receipt

~~~json
{
  "receipt_schema": "sentigraph_governed_nonproduction_human_review_decision_ledger_initialization_receipt_v0_1",
  "receipt_version": "0.1",
  "outcome": "initialized_exact_empty_formal_decision_ledger",
  "target_kind": "dedicated_local_sqlite_nonproduction_human_review_decision_ledger",
  "target_logical_label": "runtime/governed_nonproduction_human_review_decisions/review_decisions_v0_1.sqlite3",
  "target_identity_safe_hash": "4d2b1ee233433b774d30b82b57c77a58a5aab6427fcf8454a7bf05e5590d7202",
  "target_authorization_contract_safe_hash": "de3cbfe49dfeb836f3bc8b95b5a46d51366892e2277f86402306edbfd543ea4d",
  "target_preexistence_classification": "absent",
  "initialization_action": "created_exact_schema",
  "schema_version": "0.1",
  "primary_table": "governed_nonproduction_human_review_decisions_v0_1",
  "sqlite_connection_open_count": 1,
  "sqlite_connection_reopen_count": 0,
  "schema_ddl_statement_count": 1,
  "decision_table_dml_statement_count": 0,
  "decision_row_count": 0,
  "exact_schema_verified": true,
  "exact_empty_verified": true,
  "integrity_result": "ok",
  "final_sidecar_count": 0,
  "human_review_required": true,
  "no_automatic_trust_upgrade": true,
  "production_ready": false,
  "warnings": [],
  "blockers": []
}
~~~

Initialization receipt canonical SHA-256:
5d65da59110352def9c0160f78f38a94251ff51adb918c8c1ea142a44b0b4874

### Recovered outcome and deletion proof

~~~text
target_preexistence_classification = absent
recovered_formal_outcome = initialized_exact_empty_formal_decision_ledger
formal_decision_ledger_state = initialized_exact_empty
preserved_result_artifact_deleted = yes
preserved_result_artifact_exact_path_absent = yes
R2_validator_deleted = yes
R2_validator_exact_path_absent = yes
~~~

### Retained validation and no-side-effect proof

- P2 focused tests: 30 passed; required controls covered: 35.
- F11 focused tests: 78 passed.
- Nearby route safety: 5 passed.
- Tests rerun during R2: no.
- Pycompile rerun during R2: no.
- Service/test edits during R2: no.

~~~text
formal runner executions = 1
formal operation invocations = 1
formal initializer reruns during R2 = 0
formal target accesses during R2 = 0
SQLite accesses during R2 = 0
service calls during R2 = 0
route calls during R2 = 0
writer calls during R2 = 0
F10 calls during R2 = 0
decision writer calls = 0
human-review decisions captured = 0
frontend actions = 0
production/downstream actions = 0
automatic retries = 0
automatic repairs = 0
second formal executions = 0
Project Source changes = 0
tag/release creations = 0
~~~

### Source recommendation and next boundary

Project Source remains unchanged. Only after independent ChatGPT acceptance, Canonical 00, 03, 08, and 09 are recommended for replacement; Canonical 05 and all other Canonical Sources remain unchanged.

Do not start P3. The next boundary is independent ChatGPT acceptance of P2, Project Source synchronization, and then a separately authorized P3 activation-binding design using the accepted initialization receipt canonical SHA-256. The first future decision remains keep_pending_human_review.
