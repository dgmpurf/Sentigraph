# Sentigraph Baseline v2.5 Auditor V3 and Runner V3 Static Qualification Recovery

## Decision and identity

- Milestone: `SENTIGRAPH-BASELINE-V2-5-FIXED-PROMPT-1-AUDITOR-V3-RUNNER-V3-STATIC-QUALIFICATION-RECOVERY`
- Candidate classification: `ready_auditor_v3_runner_v3_static_qualification_recovery_pending_independent_acceptance`
- Privacy issue stop: `false`
- Approval SHA-256: `0aedb25cd160390b87e8880e429f8cda5228ef4004649fa7d5d7f25b2144aecf`
- Contract SHA-256: `56c0959b70d0b04892f3569de5b16ac827dca8c8dda64b568533555f0c18696e`
- Exact approval received / consumed / reusable: `yes / yes / no`

## Goal and starting identity

- Goal: `Sentigraph Baseline v2.5 Auditor V3 and Runner V3 Static Qualification Recovery`
- Goal requested / activated / completed / reusable at candidate handoff: `yes / yes / pending terminal completion / no`
- Repository / branch: `dgmpurf/Sentigraph / main`
- Starting commit: `8f33ec8ebe90f404be5beb6c9c802ac4e78bc622`
- Starting message: `Establish Baseline v2.5 static qualification recovery`
- Pre-Goal status: clean; staged `0`; untracked `0`.
- Wrong-project and stale-task guards: passed.
- Prior executor inactive and `get_goal = null` before activation.
- Baseline v2.4 Fixed Prompt 1 remains `needs_fix`, terminated and nonreusable; it is not reclassified.
- Baseline v2.5 governance establishment remains independently accepted and nonreusable.

## Accounting transition

- Before engineering / fixed / conditional / risk: `0 / 0 / 0 / 0`.
- After engineering / fixed / conditional / risk: `1 / 1 / 0 / 0`.
- Remaining fixed / conditional / risk: `0 / 1 / 2`.
- Fixed Prompt 1: candidate completed, consumed, nonreusable.
- Conditional Prompt 1: unconsumed, unselected, unauthorized.
- Risk Prompt 1: eligibility candidate only, unselected, unauthorized.
- Risk Prompt 2: unconsumed, unselected, unauthorized.

## Fresh reconstruction and no-reuse ledger

Both candidates were independently reconstructed from the Baseline v2.5 contract in a freshly cleared in-memory state. Auditor V2 and Runner V2 reads / modifications / executions were `0 / 0 / 0`. Baseline v2.4 candidate reads / reuse were `0 / 0`. No prior candidate source, shell history, log, cache, Git blob, external artifact or task variable was used as construction input.

## Pre-freeze lifecycle

- Total complete matrix attempts: `2` of a maximum `3`.
- Primary attempt: stopped before aggregate acceptance because the auditor helper did not represent chained-call AST identity when validating the forged-CIB mutation inventory.
- Primary Auditor identity: `77696` bytes, SHA-256 `3cea396b5a3fcc5f73eab64393bd334c5fe07f393fe233d6d4b5db1ae038c8f5`.
- Primary Runner identity: `22613` bytes, SHA-256 `70fe65f50ee2dfeb07c04790086929bf05ceb8956a0cfa6fda3448b2905b0c92`.
- Bounded recovery count: `1`.
- Recovery 1 classification: `checker_helper_chained_call_identity`.
- Affected check / fixture: `CIB_DATAFLOW / forged_cib_digest`.
- Auditor bytes changed / Runner bytes changed: `yes / no`.
- Recovery verification: valid CIB dataflow accepted; forged digest dataflow rejected; mutation delta `cib_sha = -1`.
- Attempt 2 result: valid `30 / 30`; negatives tested/rejected `20 / 20`; parse failures `0`; exact single-violation matches `20 / 20`.
- Final pre-freeze Auditor identity: `77775` bytes, SHA-256 `0d43a408f86904f981be9091be035b19e4baa8830045393fe712b41c19905743`.
- Final pre-freeze Runner identity: `22613` bytes, SHA-256 `70fe65f50ee2dfeb07c04790086929bf05ceb8956a0cfa6fda3448b2905b0c92`.
- Filesystem targets created before complete matrix passage: `0`.
- Approved local governance processes performed only candidate compilation, AST analysis, fixture construction and static matrix evaluation; Runner V3 and product code were never executed.

## Frozen candidate identities

- Auditor path: `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v3.py`.
- Auditor bytes / SHA-256 / Git blob: `77775 / 0d43a408f86904f981be9091be035b19e4baa8830045393fe712b41c19905743 / dea9254dcb4b822ad7539327812db11c26fb24f8`.
- Auditor strict UTF-8 / BOM absent: `true / true`.
- Auditor imports: future annotations, `ast`, `hashlib`, `json`, `sys`, and `Path` from `pathlib` only.
- Runner basename: `.sentigraph_b05_get_smoke_runner_v3.py`.
- Runner bytes / SHA-256: `22613 / 70fe65f50ee2dfeb07c04790086929bf05ceb8956a0cfa6fda3448b2905b0c92`.
- Runner strict UTF-8 / BOM absent: `true / true`.
- Embedded fixture / frozen bytes / external file equality: `true`.
- Source modifications after freeze: `0`.

## Exact ordered checks

1. `STRICT_UTF8_NO_BOM`
2. `AST_PARSE`
3. `IMPORT_ALLOWLIST`
4. `BOUND_CONSTANTS`
5. `RECEIPT_SINGLE_READ`
6. `CONFIG_EXACT_THREE_READS`
7. `CIB_DATAFLOW`
8. `CANONICAL_BINDING_CONSTANTS_EXACT`
9. `CONFIGURATION_BOUND_EXACT`
10. `NO_RANDOM_OR_WEAK_HASH`
11. `GATE_PRESTATE_EXACT_ORDER`
12. `GATE_WRITE_EXACT_ORDER`
13. `GATE_RESTORE_REVERSED_OUTER_FINALLY`
14. `DOTENV_PATCH_BEFORE_APP_IMPORT`
15. `DOTENV_RESTORE_OUTER_FINALLY`
16. `APP_IMPORT_EXACTLY_ONCE`
17. `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
18. `NO_ASYNCIO_RUN`
19. `ASGI_TRANSPORT_EXACTLY_ONCE`
20. `TARGET_ROUTE_EXACT`
21. `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
22. `PERFORM_GET_CALLED_EXACTLY_ONCE`
23. `RESPONSE_EXACT_52_FIELD_ORDER`
24. `RESPONSE_BOUNDED_HASH_ONLY`
25. `FILE_GUARD_BOUNDARY`
26. `RAW_ROW_PRIVACY_FAIL_CLOSED`
27. `NO_DIRECTORY_DISCOVERY`
28. `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
29. `NO_EXTERNAL_OR_MUTATING_ACTIONS`
30. `ATOMIC_SAFE_RESULT_AND_OUTPUT`

The list contains `30` unique names in exact contract order.

## Exact negative fixture outcomes

1. `second_http_get` -> `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
2. `perform_get_called_twice` -> `PERFORM_GET_CALLED_EXACTLY_ONCE`
3. `gate_restore_removed` -> `GATE_RESTORE_REVERSED_OUTER_FINALLY`
4. `dotenv_patch_after_import` -> `DOTENV_PATCH_BEFORE_APP_IMPORT`
5. `dotenv_restore_removed` -> `DOTENV_RESTORE_OUTER_FINALLY`
6. `forged_cib_digest` -> `CIB_DATAFLOW`
7. `response_order_removed` -> `RESPONSE_EXACT_52_FIELD_ORDER`
8. `raw_row_read` -> `RAW_ROW_PRIVACY_FAIL_CLOSED`
9. `external_socket_action` -> `NO_EXTERNAL_OR_MUTATING_ACTIONS`
10. `payload_output` -> `ATOMIC_SAFE_RESULT_AND_OUTPUT`
11. `asyncio_run_added` -> `NO_ASYNCIO_RUN`
12. `second_app_import` -> `APP_IMPORT_EXACTLY_ONCE`
13. `second_event_loop` -> `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
14. `asgi_transport_removed` -> `ASGI_TRANSPORT_EXACTLY_ONCE`
15. `target_route_changed` -> `TARGET_ROUTE_EXACT`
16. `directory_discovery_added` -> `NO_DIRECTORY_DISCOVERY`
17. `socket_type_replaced` -> `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
18. `atomic_replace_removed` -> `ATOMIC_SAFE_RESULT_AND_OUTPUT`
19. `receipt_schema_substitution` -> `CANONICAL_BINDING_CONSTANTS_EXACT`
20. `opaque_configuration_bound_1048` -> `CONFIGURATION_BOUND_EXACT`

All 20 fixtures parsed, were audited once in the complete matrix, were rejected, and passed the other 29 checks.

## Isolated asyncio fixture preflight

- Inserted `asyncio.run` calls: `1`.
- Positional argument: literal `None`.
- Keyword count: `0`.
- Inserted subtree `_perform_get` names: `0`.
- Complete-source `_perform_get` call delta: `0`.
- `asyncio.new_event_loop` delta: `0`.
- `client.get` delta: `0`.
- `importlib.import_module("app.main")` delta: `0`.
- Changed AST regions: `1`.
- Parse result: pass.
- Complete-matrix failed checks: `[NO_ASYNCIO_RUN]`.

## Canonical and configuration-bound results

- Canonical binding schema is the direct literal `sentigraph_b05_server_owned_configuration_identity_binding_v0_1`.
- Receipt schema remains the distinct literal `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1`.
- Canonical dictionary contains exactly 11 fields in required insertion order; the first nine identities are direct string literals.
- `salt_hex` is sourced only from the receipt and the ordered configuration list contains exactly the three approved names.
- Shared opaque-value upper bound is the direct integer literal `2048`; `1048` is absent from the valid Runner.
- `receipt_schema_substitution` failed only `CANONICAL_BINDING_CONSTANTS_EXACT`.
- `opaque_configuration_bound_1048` failed only `CONFIGURATION_BOUND_EXACT`.

## Final one-process qualification

- Executions / retries: `1 / 0`.
- Exit code / stderr empty: `0 / true`.
- Schema / version / status: `sentigraph_b05_get_smoke_auditor_v3_runner_v3_static_qualification_result_v0_1 / 0.1 / pass`.
- Self-test schema / status: `sentigraph_b05_get_smoke_static_auditor_v3_self_test_result_v0_1 / pass`.
- Checks total: `30`.
- Valid total / accepted: `1 / 1`.
- Negative total / tested / rejected: `20 / 20 / 20`.
- Fixture parse failures / single-violation matches: `0 / 20`.
- Check-name / fixture-name order exact: `true / true`.
- Final Runner audit checks total / passed / failed: `30 / 30 / 0`.
- Final failed checks: `[]`.
- Runner reads / reopens / executed: `1 / 0 / 0`.
- Environment / receipt / product access: `0 / 0 / 0`.

## File and Git allowlists

Repository creation allowlist contains exactly:

1. `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v3.py`
2. `docs/health/sentigraph_baseline_v2_5_fixed_prompt_1_auditor_v3_runner_v3_static_qualification_recovery_report_v1_0.md`

The sole external creation is `.sentigraph_b05_get_smoke_runner_v3.py`, outside Git and never staged. Existing repository files modified: `0`. Backend, frontend, browser, application and product tests were not run because this is a static-only V3 recovery qualification using one embedded public Runner fixture.

## Hard-zero Tier A ledger

- Auditor V2 reads / modifications / executions: `0 / 0 / 0`.
- Runner V2 reads / modifications / executions: `0 / 0 / 0`.
- v2.4 candidate reads / reuse: `0 / 0`.
- CIB receipt reads / reopens: `0 / 0`.
- Blocked safe-result reads / reopens: `0 / 0`.
- Environment reads / enumeration / writes: `0 / 0 / 0`.
- Gate reads / writes: `0 / 0`.
- Application imports / app-factory calls: `0 / 0`.
- Event-loop creations / Runner V3 executions / GET attempts: `0 / 0 / 0`.
- Provider Result / package / collector access: `0 / 0 / 0`.
- Raw evidence / source / comment / log reads: `0 / 0 / 0 / 0`.
- External product network / address resolution: `0 / 0`.
- Unapproved product subprocess: `0`.
- Database / persistence: `0 / 0`.
- Product-code changes: `0`.
- Project Source generation / replacement: `0 / 0`.
- Production / export / delivery: `0 / 0 / 0`.

## Directly established

Fresh Auditor V3 and Runner V3 candidates were reconstructed without V2 or old-candidate reuse. Auditor V3 has exactly 30 ordered scope-aware AST checks. All 20 negative fixtures parse and fail exactly their intended single check; the asyncio fixture fails only `NO_ASYNCIO_RUN`. Exact canonical constants and the literal 2048 bound are enforced. The external Runner is byte-identical to the accepted embedded public fixture, passes 30/30, and has never been executed. Fixed Prompt 1 is ready for independent ChatGPT acceptance.

## Not established and authorization boundary

This work does not establish current CIB equality, environment stability, application readiness, B05 GET success, product correctness, collector correctness, receipt-read authority, Runner execution authority, Risk Prompt selection, CIB recapture authority, Project Source replacement authority, or production/persistence/export/delivery readiness.

Current protected-access authority, runtime authority, GET authority and CIB recapture authority are all `none`. Risk Prompt 1 is only an eligibility candidate and remains unselected and unauthorized. The next action is independent ChatGPT acceptance of this Fixed Prompt 1 candidate; no Runner execution or new Goal is authorized here.
