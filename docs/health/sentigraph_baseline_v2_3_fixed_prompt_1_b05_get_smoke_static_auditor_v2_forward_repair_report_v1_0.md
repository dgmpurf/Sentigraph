# Sentigraph Baseline v2.3 Fixed Prompt 1: B05 GET Smoke Static Auditor V2 Forward Repair

## Milestone and decision candidate

- Milestone: `SENTIGRAPH-BASELINE-V2-3-FIXED-PROMPT-1-B05-GET-SMOKE-STATIC-AUDITOR-V2-FORWARD-REPAIR`
- Runtime classification: `fixed_public_static_only_auditor_v2_forward_repair`
- Decision candidate: `ready_pending_independent_acceptance`
- Privacy issue stop: `false`
- Independent acceptance claimed by this report: `no`

The candidate is ready only for independent ChatGPT acceptance. This report does
not create runtime, runner, CIB, application, endpoint, or GET authority.

## Approval and Goal lifecycle

- Exact approval received: `yes`
- Compact approval phrase SHA-256:
  `d3214ef63de82ed233e65f896547d2081a221ff382a98d5fa78e95efa65f4983`
- Static Auditor V2 Forward Repair Contract V1 SHA-256:
  `0019f8168956a9ae1fa7a0b0a255cbf8b71aacbf023d059cafa0e7320b013a0d`
- Approval consumed / reusable: `yes / no`
- Goal requested / activated / completed at report freeze / reusable:
  `yes / yes / no / no`
- Goal title: `Sentigraph Baseline v2.3 Static Auditor V2 Forward Repair`
- Baseline v2.3 Fixed Prompt 1 consumed / reusable: `yes / no`

## Starting identity and guards

- Repository: `dgmpurf/Sentigraph`
- Branch: `main`
- Starting HEAD: `3fe98c6482107a2852562cfb0461cd65b2993a88`
- Starting commit message: `Establish Baseline v2.3 static auditor recovery`
- Pre-Goal worktree: `clean`
- Wrong-project guard: `passed`
- Stale-task guard: `passed`
- Old Goal cleared / `get_goal` null / prior executor inactive:
  `yes / yes / yes`
- Both authorized targets initially absent: `yes`
- Exact parent directories initially present: `yes`

No fetch, pull, branch switch, alternate repository search, or project change was
performed.

## Exact changed-file allowlist

Exactly these two new repository files are authorized:

1. `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v2.py`
2. `docs/health/sentigraph_baseline_v2_3_fixed_prompt_1_b05_get_smoke_static_auditor_v2_forward_repair_report_v1_0.md`

Existing files modified, deleted, moved, renamed, or copied: `0`.

## Baseline accounting

Before fresh Goal activation:

- Engineering / fixed / conditional / risk: `0 / 0 / 0 / 0`
- Remaining fixed / conditional / risk: `1 / 1 / 1`

After verified fresh Goal activation:

- Engineering / fixed / conditional / risk: `1 / 1 / 0 / 0`
- Remaining fixed / conditional / risk: `0 / 1 / 1`
- Fixed Prompt 1 consumed / reusable: `yes / no`
- Conditional Prompt 1 consumed: `no`
- Risk Prompt 1 consumed: `no`

## Preserved Baseline v2.2 history

Baseline v2.2 remains historical and closed for future Prompt accounting:

- Final engineering / fixed / conditional / risk: `5 / 1 / 1 / 3`
- Remaining fixed / conditional / risk: `0 / 0 / 0`
- Risk Prompt 1: `blocked / consumed / nonreusable / unreclassified`
- Fixed Prompt 1: `needs_fix / consumed / nonreusable / unreclassified`
- Conditional Prompt 1:
  `ready / consumed / nonreusable / independently accepted`
- Risk Prompt 3:
  `ready / consumed / nonreusable / independently accepted`
- Risk Prompt 2:
  `blocked / consumed / nonreusable / unreclassified`
- Manual active Source replacement:
  `substantively valid with preserved procedural needs_fix`

The Baseline v2.2 Risk Prompt 2 result remains:

- Decision: `blocked`
- Runtime classification:
  `blocked_risk_prompt_2_get_runner_static_audit`
- Approval / Goal: `consumed and nonreusable`
- GET attempts: `0`
- Historical result reclassified: `no`

## Root cause and forward repair

The blocked result was caused by a task-specific static-auditor construction and
semantic-audit defect, not by an established runner or product defect.

Static Auditor V2 repairs these semantic classes:

1. Fixture mutations use unique anchors with an exact single replacement, so a
   mutation cannot alter both a definition and an invocation.
2. Every valid and negative fixture is parsed before audit; a parse failure is a
   fixture-generation error and never counts as the intended rejection.
3. Failure results retain actual valid-fixture and negative-fixture progress.
4. Dotenv patch and restore assignments are distinguished by scope and by the
   outermost-finally location.
5. HTTP GET recognition is restricted to the exact awaited
   `client.get(TARGET_ROUTE)` call inside `_perform_get`; unrelated `.get` calls
   do not count.
6. Runtime ordering is proved from call sites inside the execution function.
7. CIB verification is structural dataflow validation rather than call-presence
   matching.
8. Response order, bounded hashing, network-guard type preservation, atomic
   publication, and bounded output have distinct check ownership.

These repairs were constructed solely from fixed-public synthetic source.

## Ordered 28-check contract

`CHECK_NAMES` contains exactly these ordered names:

1. `STRICT_UTF8_NO_BOM`
2. `AST_PARSE`
3. `IMPORT_ALLOWLIST`
4. `BOUND_CONSTANTS`
5. `RECEIPT_SINGLE_READ`
6. `CONFIG_EXACT_THREE_READS`
7. `CIB_DATAFLOW`
8. `NO_RANDOM_OR_WEAK_HASH`
9. `GATE_PRESTATE_EXACT_ORDER`
10. `GATE_WRITE_EXACT_ORDER`
11. `GATE_RESTORE_REVERSED_OUTER_FINALLY`
12. `DOTENV_PATCH_BEFORE_APP_IMPORT`
13. `DOTENV_RESTORE_OUTER_FINALLY`
14. `APP_IMPORT_EXACTLY_ONCE`
15. `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
16. `NO_ASYNCIO_RUN`
17. `ASGI_TRANSPORT_EXACTLY_ONCE`
18. `TARGET_ROUTE_EXACT`
19. `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
20. `PERFORM_GET_CALLED_EXACTLY_ONCE`
21. `RESPONSE_EXACT_52_FIELD_ORDER`
22. `RESPONSE_BOUNDED_HASH_ONLY`
23. `FILE_GUARD_BOUNDARY`
24. `RAW_ROW_PRIVACY_FAIL_CLOSED`
25. `NO_DIRECTORY_DISCOVERY`
26. `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
27. `NO_EXTERNAL_OR_MUTATING_ACTIONS`
28. `ATOMIC_SAFE_RESULT_AND_OUTPUT`

- Check count: `28`
- Checks passed by the valid public fixture: `28`

## Exact negative-fixture matrix

Each fixture parsed successfully and failed exactly its assigned check:

1. `second_http_get` ->
   `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
2. `perform_get_called_twice` ->
   `PERFORM_GET_CALLED_EXACTLY_ONCE`
3. `gate_restore_removed` ->
   `GATE_RESTORE_REVERSED_OUTER_FINALLY`
4. `dotenv_patch_after_import` ->
   `DOTENV_PATCH_BEFORE_APP_IMPORT`
5. `dotenv_restore_removed` ->
   `DOTENV_RESTORE_OUTER_FINALLY`
6. `forged_cib_digest` ->
   `CIB_DATAFLOW`
7. `response_order_removed` ->
   `RESPONSE_EXACT_52_FIELD_ORDER`
8. `raw_row_read` ->
   `RAW_ROW_PRIVACY_FAIL_CLOSED`
9. `external_socket_action` ->
   `NO_EXTERNAL_OR_MUTATING_ACTIONS`
10. `payload_output` ->
    `ATOMIC_SAFE_RESULT_AND_OUTPUT`
11. `asyncio_run_added` ->
    `NO_ASYNCIO_RUN`
12. `second_app_import` ->
    `APP_IMPORT_EXACTLY_ONCE`
13. `second_event_loop` ->
    `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
14. `asgi_transport_removed` ->
    `ASGI_TRANSPORT_EXACTLY_ONCE`
15. `target_route_changed` ->
    `TARGET_ROUTE_EXACT`
16. `directory_discovery_added` ->
    `NO_DIRECTORY_DISCOVERY`
17. `socket_type_replaced` ->
    `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
18. `atomic_replace_removed` ->
    `ATOMIC_SAFE_RESULT_AND_OUTPUT`

Fixture-generation integrity:

- Valid fixture count: `1`
- Negative fixture count: `18`
- Unique anchors required: `yes`
- Exact single replacements required: `yes`
- Common signature/name/repeated-fragment replacements: `0`
- Parse-before-audit enforced: `yes`
- Exactly one expected failed check per negative fixture enforced: `yes`
- Actual progress retained on failure: `yes`
- Fixture source disclosed: `no`

## Frozen self-test result

- Self-test executions / retries: `1 / 0`
- Exit code: `0`
- Standard error empty: `yes`
- Valid total / accepted: `1 / 1`
- Negative total / tested / rejected: `18 / 18 / 18`
- Fixture parse failures: `0`
- Single-violation matches: `18`
- First failure fixture / code: `not applicable / not applicable`

Exact bounded self-test result:

```json
{"schema":"sentigraph_b05_get_smoke_static_auditor_v2_self_test_result_v0_1","version":"0.1","status":"pass","checks_total":28,"valid_total":1,"valid_accepted":1,"negative_total":18,"negative_tested":18,"negative_rejected":18,"fixture_parse_failures":0,"single_violation_matches":18,"runner_execution":0,"environment_access":0,"receipt_access":0,"product_access":0}
```

The first successful self-test froze the auditor. It was not edited or rerun
after that success.

## Frozen auditor identity

- Path:
  `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v2.py`
- Bytes: `65247`
- SHA-256:
  `452020e596e0ef993d8118ef48e9efecf124b02cda5c4917e811caee3ec2ebf2`
- Git blob: `aa7040a308b83ef257e482e4042398d63b96d0b8`
- Strict UTF-8: `pass`
- BOM absent: `pass`

## Bounded source inspection

Inspection was limited to the newly created auditor. The auditor was parsed as
source but was not imported.

- Outer AST parse: `pass`
- Standard-library-only imports:
  `__future__, ast, hashlib, json, pathlib, sys`
- Additional imports: `0`
- Repository-local application imports in executable auditor code: `0`
- `eval`, `exec`, dynamic import, or executable base64: `0`
- Environment or registry access by executable auditor code: `0`
- Network, address-resolution, or subprocess execution by the auditor: `0`
- Audited-runner execution paths: `0`
- `CHECK_NAMES` count / unique: `28 / 28`
- Negative fixture names count / unique: `18 / 18`
- Repeated-fragment fixture replacement: `0`
- Bounded single-line JSON output: `pass`
- Absolute paths, source text, tracebacks, payloads, receipt values, salts,
  bindings, response bodies, or protected values emitted: `0`

The inner public runner fixture contains only fixed-public dummy values. No real
configuration value, local path, salt, combined binding, or receipt body is
present.

## Hard-zero boundary

For this Goal:

- Old external auditor reads / executions: `0 / 0`
- Old external runner reads / executions: `0 / 0`
- External runner reads / reopens / executions: `0 / 0 / 0`
- External runner audit executions: `0`
- CIB receipt reads / reopens: `0 / 0`
- Environment reads / writes / enumeration: `0 / 0 / 0`
- HKCU / HKLM / broadcast: `0 / 0 / 0`
- Gate reads / writes: `0 / 0`
- Application imports: `0`
- Event-loop creations / closes: `0 / 0`
- `run_until_complete` / `asyncio.run` executions: `0 / 0`
- GET attempts / completed / retries: `0 / 0 / 0`
- Provider Result / package / collector access: `0 / 0 / 0`
- Raw evidence / source / comment / log reads: `0 / 0 / 0 / 0`
- Directory discovery outside exact repository validation: `0`
- Forbidden network / address resolution / subprocess actions: `0 / 0 / 0`
- Database / persistence: `0 / 0`
- Product-code changes: `0`
- Project Source generation / replacement: `0 / 0`
- Production / export / delivery: `0 / 0 / 0`

Parsing fixed-public source strings in memory is not product or protected
access.

## Repository and test validation

At report freeze:

- Expected changed-file count: `2`
- Expected changed files: exact two-file allowlist
- Expected unexpected files: `0`
- Auditor strict UTF-8 / no BOM: `pass / pass`
- Report strict UTF-8 / no BOM: pending final repository validation
- `git diff --check`: pending final repository validation
- Cached diff check: pending ready-only Git finalization
- Backend tests: `not run`
- Frontend tests: `not run`
- Application imports: `not run`
- Browser tests: `not run`
- Reason: `static-only governance tooling task`

## Ready-only Git fields

The following fields are intentionally pending until this report is frozen and
the complete two-file repository diff passes:

- Stage: `pending_ready_only_finalization`
- Commit: `pending_ready_only_finalization`
- Push: `pending_ready_only_finalization`
- Required commit message: `Add B05 GET smoke static auditor v2`
- Required destination: current `main` to `origin/main`
- Tag / release / force push / rebase / reset / history rewrite: `none`

## Established and not established

Directly established:

> Static Auditor V2 is a committed-candidate, fixed-public, static-only
> auditor that passed its embedded 1-valid / 18-single-violation public
> fixture matrix and is ready for repository validation and independent
> ChatGPT acceptance.

Not established:

- An actual runner is conformant.
- An actual runner was read or executed.
- CIB equality.
- Application readiness.
- B05 GET success.
- HTTP response correctness.
- Sentigraph product correctness.
- Collector or Provider Result correctness.
- Runtime authority.
- GET authority.

## Downstream authority and next action

- Static Auditor V2 independent acceptance completed: `no`
- Conditional Prompt 1 selected / authorized / executed: `no / no / no`
- Risk Prompt 1 selected / authorized / executed: `no / no / no`
- Current engineering authority after this Goal: `none`
- Current runtime authority: `none`
- Current GET authority: `none`
- Next route selected: `independent ChatGPT acceptance of Static Auditor V2`
- Next route authorized by this Goal: `no`
- Next action: complete exact two-file repository validation and ready-only Git
  finalization, then stop for independent acceptance.
