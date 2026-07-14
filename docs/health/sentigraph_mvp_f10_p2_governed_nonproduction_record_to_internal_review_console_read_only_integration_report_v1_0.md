# Sentigraph MVP-F10-P2 Governed Nonproduction Record to Internal Review Console Read-only Integration Report v1.0

Date: 2026-07-14

Milestone: MVP-F10-P2 with conditional recovery R1

Decision: `ready`

privacy_issue_stop: `no`

## Executive result

The governed nonproduction record is exposed to the existing Internal Alpha Review Console through the approved read-only route, a request-local 46-field projection, dual process gates, and a frontend presentation limited to approved opaque metadata. The two legacy synthetic projections and the static unavailable-backend fallback remain preserved.

All retained synthetic, regression, compilation, static, frontend-build, and browser-fallback evidence is accepted. The separately audited R1 runner then completed exactly one governed route GET. That request produced the exact ready contract, invoked the adapter and accepted helper once each, performed no retry, and used no writer, direct SQLite access, or mutation path.

MVP_F10_P2_status: `candidate_completed_pending_chatgpt_acceptance`

MVP_F10_status: `candidate_completed_pending_chatgpt_acceptance`

## Approval bindings

### Exact MVP-F10-P2 approval

`APPROVE_SENTIGRAPH_MVP_F10_P2_GOVERNED_NONPRODUCTION_RECORD_TO_INTERNAL_REVIEW_CONSOLE_READ_ONLY_INTEGRATION_IMPLEMENTATION_AND_VALIDATION_PLANNED_FIXED_MILESTONE_PART_2_OF_2_BIND_ACCEPTED_MVP_F10_P1_COMMIT_CONTRACT_SHA_EXACT_SEVEN_FILE_ALLOWLIST_EXISTING_INTERNAL_GET_ROUTE_EXACT_NEW_PROJECTION_ID_DUAL_ENV_GATES_ACCEPTED_EXACT_TARGET_READ_ONLY_AUDIT_HELPER_REQUEST_LOCAL_ADAPTER_EXACT_46_FIELD_PROJECTION_SCHEMA_SEVEN_OUTCOME_MAPPING_PRESERVE_EXISTING_SYNTHETIC_PROJECTION_IDS_AND_STATIC_FALLBACK_TDD_SYNTHETIC_TESTS_BACKEND_ROUTE_FRONTEND_BUILD_BROWSER_IF_AVAILABLE_ONE_BOUNDED_EXACT_TARGET_GET_SMOKE_ONLY_AFTER_SYNTHETIC_PASS_BOTH_GATES_PROCESS_LOCAL_ONE_HELPER_INVOCATION_NO_RETRY_NO_WRITER_NO_DIRECT_SQLITE_NO_PAYLOAD_CAPTURE_RECEIPT_SOURCE_PACKAGE_ROW_NO_TARGET_MUTATION_NO_PRODUCTION_EVIDENCEITEM_REVIEW_QUEUE_CASE_ANALYSIS_REPORT_EXPORT_DELIVERY_OR_PROJECT_SOURCE_CHANGE`

### Exact MVP-F10-P2-R1 recovery approval

`APPROVE_SENTIGRAPH_MVP_F10_P2_R1_ONE_CORRECTED_REPOSITORY_EXTERNAL_EXACT_TARGET_SMOKE_RUNNER_EXECUTION_IMPORT_PATH_BOOTSTRAP_ONLY_RESUME_EXISTING_BLOCKED_F10_P2_GOAL_BIND_ACCEPTED_F10_P2_SIX_PRE_REPORT_ALLOWLISTED_CHANGES_PRIOR_RUNNER_SHA_A9FF93270B82312F4C110054FD3AE8A2F0BA52FD6082DA22F41278A674489D98_PRIOR_EXECUTION_FAILED_BEFORE_PRODUCT_IMPORT_EXACT_TARGET_GET_ADAPTER_HELPER_RETRY_WRITER_AND_DIRECT_SQLITE_COUNTS_ALL_ZERO_AUTHORIZE_ONE_NEW_RUNNER_SHA_READBACK_AST_AUDIT_AND_ONE_EXECUTION_WITH_PROCESS_LOCAL_PYTHONPATH_BOUND_TO_EXACT_SENTIGRAPH_BACKEND_ONE_TESTCLIENT_GET_EXACT_GOVERNED_PROJECTION_ID_BOTH_GATES_PROCESS_LOCAL_ONE_ADAPTER_INVOCATION_ONE_ACCEPTED_HELPER_INVOCATION_ZERO_RETRY_ZERO_WRITER_ZERO_DIRECT_SQLITE_NO_SECOND_RUN_NO_CODE_OR_TEST_CHANGE_BEFORE_SMOKE_NO_BROWSER_OR_SYNTHETIC_TEST_RERUN_THEN_ONLY_IF_READY_CREATE_THE_SEVENTH_ALLOWLISTED_HEALTH_REPORT_FINAL_VALIDATE_COMMIT_PUSH_NO_TAG_NO_PROJECT_SOURCE_CHANGE_NO_MVP_F11`

## Goal lifecycle

- The existing MVP-F10-P2 Goal was created for the implementation and validation milestone and was never replaced.
- The Goal reached the one-time exact-target smoke after the six pre-report changes and all synthetic/build/browser-fallback checks were accepted.
- The first repository-external runner process failed before product import. It issued no request and invoked no adapter or helper.
- The no-rerun boundary was preserved. The Goal was marked blocked only after the same authorization blocker persisted for three consecutive Goal turns.
- R1 manually resumed that same Goal and authorized one corrected external runner execution limited to process-local import bootstrapping.
- No Goal was cleared, duplicated, or replaced during recovery.

## Starting commit and accepted P1 binding

- Starting commit: `1b73e629e2415ea25d0c5fe6b7881763b9f0f03c`
- Starting branch: `main`
- Accepted P1 contract: `docs/architecture/sentigraph_mvp_f10_p1_governed_nonproduction_record_to_internal_review_console_read_only_integration_contract_v1_0.md`
- P2 remained bound to the accepted P1 commit and contract throughout implementation and R1 recovery.
- The R1 resume guard reconfirmed the expected repository identity, commit, branch, six changed files, zero staged files, absent report, and removed prior runner.

## Prompt accounting

| Counter | Value |
| --- | ---: |
| consumed_engineering_prompts_since_v1_3 | 11 |
| consumed_fixed_prompts_since_v1_3 | 5 |
| consumed_conditional_prompts_since_v1_3 | 5 |
| consumed_risk_prompts_since_v1_3 | 1 |
| remaining_fixed_prompts | 9 |
| remaining_conditional_allowance | 1 |
| remaining_risk_buffer | 1 |

## Exact seven-file change allowlist

1. `backend/app/services/governed_nonproduction_review_console_projection.py`
2. `backend/app/api/v1/routes/internal_alpha_review_console.py`
3. `backend/app/tests/test_mvp_f10_p2_governed_nonproduction_review_console_projection.py`
4. `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py`
5. `frontend/src/api/sentigraphApi.js`
6. `frontend/src/pages/InternalAlphaReviewConsole.jsx`
7. `docs/health/sentigraph_mvp_f10_p2_governed_nonproduction_record_to_internal_review_console_read_only_integration_report_v1_0.md`

No eighth tracked file is authorized.

## Retained implementation result

- A new request-local projection adapter calls only the accepted exact-target read-only audit helper and returns the exact ordered 46-field contract.
- All seven P1-defined target outcomes map to bounded review-console states. Non-ready and malformed states fail closed and expose none of the eight ready-only opaque values.
- The existing route keeps its original global gate and adds the governed-record gate. The new projection is reachable only when both are enabled.
- The two legacy synthetic projection identifiers and their behavior remain unchanged.
- The frontend helper adds the governed projection identifier to the existing allowlist and retains one encoded GET shape.
- The console renders ready, absent, reservation-only, inconsistent, sidecar-unavailable, target-unavailable, and bounded-failure states without adding an operator action.
- The static unavailable-backend fallback remains present.
- No production evidence object, case mutation, review-queue runtime, downstream runtime, or public/production readiness path was added.

## Retained validation evidence

### TDD RED

- Expected P2 failures: 21
- Legacy passes in the same run: 6
- The failures covered the intentionally absent adapter, governed route/gate behavior, and governed frontend rendering before implementation.

### Focused GREEN

- Result: 27 / 27 passed
- Coverage included the adapter, exact projection shape, seven outcomes, dual gates, one-call route behavior, frontend identifier, and safe rendering contract.

### Required synthetic matrix

- Result: 157 / 157 passed
- Synthetic exact-target GET count: 0
- The matrix covered the new P2 tests, retained route contracts, frontend static contracts, disabled-backend consumption smoke, and accepted reader tests.

### Additional retained regression evidence

- Focused safe-metadata projection and governed persistence regression selection: 162 / 162 passed.
- The historical pre-implementation absence assertion remains outside the required P2 matrix because its purpose was to prove that this integration did not yet exist.

### Compilation, static, and frontend build

- Changed Python files compiled successfully.
- Static scans found no direct SQLite or writer import in the adapter or route.
- Static scans found no mutation route, mutation control, retry, or discovery path.
- Static whitespace validation passed.
- The production frontend build completed successfully: 4,028 modules transformed in 10.03 seconds.
- The build emitted only its existing large-chunk advisory; it produced no build failure.

### Browser fallback result

- Browser smoke: `pass_backend_unavailable_fallback`
- The browser navigated to the Internal Alpha Review Console while the backend port was confirmed unavailable.
- The governed static fallback rendered with status `unavailable`, explicit no-write/no-production boundary copy, and all eight ready-only values withheld.
- Interactive controls inside the review surface: 0.
- Browser console warnings: 0.
- Two expected unavailable-backend resource errors were recorded from React development-mode effect replay. Neither request reached a backend, adapter, helper, or target.
- The browser session and frontend-only development server were closed, and browser artifacts remained outside the repository.

## Prior failed runner

- Runner SHA-256: `a9ff93270b82312f4c110054fd3ae8a2f0ba52fd6082da22f41278a674489d98`
- Runner process execution count: 1
- Classification: pre-import module-resolution failure from the repository-external script context.
- Product import completed: no
- Exact-target GET count: 0
- Adapter invocation count: 0
- Helper invocation count: 0
- Retry count: 0
- Writer invocation count: 0
- Direct SQLite access count: 0
- Target mutation count: 0
- Prior runner removed: yes

No second execution occurred until the separate R1 authorization resumed the same Goal.

## Corrected runner SHA and AST audit

- Corrected runner SHA-256: `f9db95534e8f095f635e0dd94926bc6341108d3b23c84f5df1c4294c7e7a054c`
- UTF-8 byte readback: pass
- AST parse: pass
- Runner GET call count: 1
- Runner direct helper call count: 0
- Counting-wrapper delegation call count: 1
- Loop node count: 0
- Recursion detected: no
- Retry construct count: 0
- SQLite import count: 0
- Writer symbol reference count: 0
- Direct target-open count: 0
- Subprocess reference count: 0
- Network client count outside TestClient: 0
- TestClient constructor count: 1
- Response parse count: 1

The import bootstrap and both route gates existed only in the corrected runner process. No repository configuration or product package file changed.

## One-time smoke result

- Corrected runner execution count: 1
- Total runner process execution count, including the prior pre-import failure: 2
- HTTP status: 200
- Outer response schema: `sentigraph_internal_alpha_review_console_governed_record_route_response_v0_1`
- Projection schema: `sentigraph_internal_alpha_governed_nonproduction_record_review_projection_v0_1`
- Projection field count: 46
- Projection fields unique: yes
- Extra projection fields: none
- Projection status: `governed_record_review_ready`
- Target state outcome: `exact_expected_reservation_and_record`
- Record count class: `exact_1`
- Reservation count class: `exact_1`

### One-time counters

| Counter | Value |
| --- | ---: |
| prior_runner_execution_count | 1 |
| corrected_runner_execution_count | 1 |
| total_runner_process_execution_count | 2 |
| exact_target_GET_count | 1 |
| adapter_invocation_count | 1 |
| helper_invocation_count | 1 |
| helper_retry_count | 0 |
| writer_invocation_count | 0 |
| direct_SQLite_access_count | 0 |
| target_mutation_count | 0 |

## Ready projection evidence

### Approved opaque ready values

| Field | Value |
| --- | --- |
| persisted_record_id | `gnpepr-c886bd087e84dceff806e748d2f2ceaf` |
| attempt_reservation_id | `gnpepr-attempt-34d95623c3678bdd63430d97fdc7d922` |
| candidate_identity_digest | `078e2f428e42050eea013c8d2a3ee1ef1c7e341805e7a6fb38aa3cf276622d54` |
| input_safe_hash | `71f39d8067543ae508d1d319e9c950c99030df65aa197d40f82e1f95ea76ebd5` |
| gate_contract_safe_hash | `a3150e96893218a6bd5a25adec1dac38e3b3f2f48bf07dcc72313c05d919fc0a` |
| activation_decision_safe_hash | `e1b0fa0b7dbb885962ef5e36f6c87d8c7d0cebd18d2e31e2525fc6bbebe5695d` |
| record_snapshot_digest | `eda50fc437940ac519881638d76fa0443481fc9fda8f50cf62805be0d83baf20` |
| reservation_snapshot_digest | `076584df7f9d712b78e9c3e5dee06cc55ff817487084074e34824bd9185f7a6c` |

### Binding and readiness assertions

- Expected record present: true
- Expected reservation present: true
- Unexpected record present: false
- Unexpected reservation present: false
- Record actual columns verified: true
- Reservation actual columns verified: true
- Record canonical hash verified: true
- Reservation canonical hash verified: true
- Record exact binding verified: true
- Reservation exact binding verified: true
- Record/reservation cross-binding verified: true
- Implementation mutating attempt consumed: true
- Governed nonproduction record exists: true
- Human review required: true
- No automatic trust upgrade: true
- Production evidence object created: false
- Production case changed: false
- Downstream runtime called: false
- Operator runtime ready: false
- Production ready: false
- Public ready: false
- Warnings: none
- Blockers: none

### Canonical response hashes

- Ready projection canonical SHA-256: `0b9dc55caf3a375b1c5c4c2b66d851c1e192807fb0fd5259fcab77c32a74575f`
- Governed outer response canonical SHA-256: `9163797b7aa4ec5506ebbab00d1180451b5631a32c6f3a236c4127526366e110`

## Runner deletion proof

- Corrected runner removed after its single successful execution: yes
- Post-deletion existence check: false
- Repository runner artifact: none
- Corrected runner re-executed: no

## Safety, privacy, and product boundaries

- The projection exposes only the eight approved opaque identifiers, hashes, and digests in the ready state.
- No raw evidence content, person identity, network locator, query text, target locator, secret, or credential is present in this report or the frontend projection.
- The runner made no direct helper call, target open, direct SQLite access, writer call, subprocess call, external network call, retry, loop, recursion, or mutation.
- The route remains read-only and dual-gated.
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- `actual_write_enabled = false`
- `production_object_enabled = false`
- `review_queue_runtime_enabled = false`
- `operator_runtime_ready = false`
- `production_ready = false`
- `public_ready = false`
- `privacy_issue_stop = no`

## Git result

- Ready-only decision at report finalization: `ready`
- Exact commit message reserved: `Implement MVP-F10-P2 review-console integration`
- Authorized changed-file count: 7
- Tag: no
- Project Source change: no
- Commit and push confirmation are terminal operations recorded in the final execution receipt; they are not predicted or back-written into this report.

## Source recommendation

- Project Source remains unchanged by this milestone.
- After independent acceptance, canonical Sources 00, 03, 08, and 09 are candidates for controlled replacement with the accepted F10 result.
- Canonical Source 05 is not a replacement candidate from this milestone.
- Source 11 is not changed or activated.

## Next boundary

- Independent acceptance of MVP-F10-P2 and MVP-F10 is required before any subsequent milestone.
- MVP_F11_eligibility_candidate_after_chatgpt_acceptance: `yes`
- MVP_F11_authorized: `no`
- MVP_F11_executed: `no`
- No subsequent milestone work begins from this report.
