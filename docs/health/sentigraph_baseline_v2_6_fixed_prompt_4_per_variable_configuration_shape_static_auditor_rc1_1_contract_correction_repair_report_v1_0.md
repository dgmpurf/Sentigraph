# Sentigraph Baseline v2.6 Fixed Prompt 4 Per-variable Configuration-shape Static Auditor RC1.1 Contract-correction Repair Report v1.0

## Milestone and classification

- Milestone: `SENTIGRAPH-BASELINE-V2-6-FIXED-PROMPT-4-PER-VARIABLE-CONFIGURATION-SHAPE-STATIC-AUDITOR-RC1-1-CONTRACT-CORRECTION-REPAIR`
- Decision candidate: `ready`
- Runtime classification candidate: `ready_per_variable_configuration_shape_static_auditor_rc1_1_contract_correction_repair_pending_independent_acceptance`
- Privacy issue stop: `false`
- This is a static governance-tool repair. It is not a Runner runtime result, application result, or GET result.

## Approval, Goal, and accounting

- Exact approval received: `yes`
- Compact approval phrase SHA-256: `4ecca79333811f0eda24fe23540c91bb67d572be570b443f325c35ca502eed83`
- Fixed Prompt 4 Auditor RC1.1 Contract V1 SHA-256: `e0b0123804830be7f4387c7bf3c79ea8cb2faf2320296bbe7c2ed79ae367edc3`
- Approval consumed / reusable: `yes / no`
- Fresh Goal title: `Sentigraph Baseline v2.6 Auditor RC1.1 Contract-correction Repair`
- Goal requested / activated / reusable: `yes / yes / no`
- Accounting before, engineering / fixed / conditional / risk: `7 / 3 / 0 / 0`
- Accounting after activation, engineering / fixed / conditional / risk: `8 / 4 / 0 / 0`
- Budget fixed / conditional / risk: `4 / 2 / 3`
- Remaining fixed / conditional / risk: `0 / 2 / 3`

## Bound repository evidence

### Contract-correction amendment

- Repository path: `docs/architecture/sentigraph_baseline_v2_6_fixed_prompt_3_blocked_and_auditor_rc1_1_contract_correction_budget_extension_amendment_v1_0.md`
- Reads / reopens: `1 / 0`
- Bytes: `15897`
- SHA-256: `32d415466d74ca8e2483f987973c1da0e8c2f08787da6d3a78c911bb9d3a23bd`
- Git blob: `bfb321965c876dcf7dcc68e07ea0ab74fadbdb3d`
- Strict UTF-8 / BOM absent: `pass / pass`

### Starting Auditor RC1

- Repository path: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
- Reads / reopens before modification: `1 / 0`
- Bytes: `69306`
- SHA-256: `ec3f1d116a6c9a22043398f65211d90341e628a61b76e076aef8304a052c24c6`
- Git blob: `c7641dff83b823dc492b6c300c84da8ecd423f41`
- Strict UTF-8 / BOM absent / AST: `pass / pass / pass`

## Preserved Prompt histories

- Fixed Prompt 1: `needs_fix / consumed / nonreusable / unreclassified`
- Fixed Prompt 2: `needs_fix / consumed / nonreusable / unreclassified`
- Fixed Prompt 3: `blocked / consumed / nonreusable / unreclassified`
- Fixed Prompt 3 classification: `blocked_auditor_rc1_1_identity_scope_or_authority_mismatch`
- Fixed Prompt 3 independent status: `completed_and_independently_accepted_as_terminal_safe_block`
- Fixed Prompt 3 candidates / matrices / qualifications / repository changes: `0 / 0 / 0 / 0`
- Fixed Prompt 4 consumed / reusable: `yes / no`

No earlier Prompt result was reclassified.

## Auditor candidate ledger

Candidate versions total: `2`. Pre-freeze matrix invocations total: `2`. Recovery versions used: `1`.

| Candidate | Reason code | Auditor changed | Runner changed | Matrix executions | Status | Valid checks | External checks | Negative tested/rejected | Exact matches | Parse failures | Fixture 30 failures | Fixture 31 failures | Runner reads/reopens/imports/executions |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | `initial_fixed_prompt_4_candidate` | yes | no | 1 | fail | 21/21 | 21/21 | 31/31 | 29/31 | 1 | `TOP_LEVEL_SURFACE_EXACT`, `MAIN_GUARD_EXACTLY_ONCE` | `[]` | 1/0/0/0 |
| 2 | `fixture_30_correction_defect` | yes | no | 1 | pass | 21/21 | 21/21 | 31/31 | 31/31 | 0 | `MAIN_GUARD_EXACTLY_ONCE` | `TOP_LEVEL_SURFACE_EXACT` | 1/0/0/0 |

Candidate 1 failed safely because the fixture mutation patch landed in an older unused helper rather than `_negative_source_rc1`. Candidate 2 restored that helper byte-semantically, changed only the authorized RC1 fixture 30 branch, and appended the fixture 31 branch. Candidate 2 was the first passing candidate and was frozen immediately. No matrix invocation occurred after freeze.

## Frozen Auditor RC1.1 identity

- Repository path: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
- Candidate: `2`
- Bytes: `69562`
- SHA-256: `5e2be4198cbc0451cc14a90b2189a67a66705c0caa7579e9b5ba3302f4f5819e`
- Git blob: `1b5315dee6682a0008311d9491204ef857503b90`
- Strict UTF-8 / BOM absent / AST: `pass / pass / pass`
- Exact Auditor import allowlist: `pass`
- Post-freeze source modifications: `0`

Auditor schemas and version remain unchanged:

```text
AUDIT_SCHEMA =
sentigraph_b05_per_variable_configuration_shape_static_audit_rc1_result_v0_2

MATRIX_SCHEMA =
sentigraph_b05_per_variable_configuration_shape_static_matrix_rc1_v0_2

QUALIFICATION_SCHEMA =
sentigraph_b05_per_variable_configuration_shape_static_qualification_rc1_v0_2

VERSION =
0.2
```

The exact Auditor imports remain:

1. `from __future__ import annotations`
2. `import ast`
3. `import hashlib`
4. `import json`
5. `import sys`
6. `from pathlib import Path`

## Exact fixed checks

Check count / uniqueness / order: `21 / 21 / exact`.

1. `STRICT_UTF8_NO_BOM`
2. `AST_PARSE`
3. `IMPORT_ALLOWLIST`
4. `TOP_LEVEL_SURFACE_EXACT`
5. `BOUND_CONSTANTS`
6. `VARIABLE_NAMES_EXACT`
7. `SHAPE_LABELS_EXACT`
8. `FUNCTION_SET_EXACT`
9. `FUNCTION_SIGNATURES_EXACT`
10. `ENVIRONMENT_GETS_EXACT`
11. `OS_USAGE_ALLOWLIST_EXACT`
12. `CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT`
13. `PATH_PUBLIC_BOUND_EXACT`
14. `ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT`
15. `CLASSIFIED_RESULT_CONTRACT_EXACT`
16. `INTEGRITY_RESULT_CONTRACT_EXACT`
17. `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT`
18. `ONE_COMPACT_JSON_PRINT`
19. `NO_VALUE_LENGTH_PATH_SECRET_OR_EXCEPTION_DISCLOSURE`
20. `NO_FILE_NETWORK_SUBPROCESS_DATABASE_DYNAMIC_ACTIONS`
21. `MAIN_GUARD_EXACTLY_ONCE`

`failed_checks` remains restricted to this fixed enum and preserves its order. Decode and parse stage-gating remains unchanged.

## Fixture preservation and correction evidence

### Fixtures 1 through 29

For every fixture 1 through 29, comparison between the immutable starting Auditor and frozen Auditor established:

- fixture name present in both: `yes`;
- branch source byte-semantically equal: `yes`;
- matched source region equal: `yes`;
- replacement source region equal: `yes`; and
- generated negative Runner source equal: `yes`.

### Fixture names, order, and mappings 1 through 30

The first thirty `FIXTURE_SPECS` entries in the frozen Auditor exactly equal the first thirty entries in the starting Auditor: `yes`.

### Fixture 30 correction

Fixture 30 preserves:

```text
name =
main_guard_removed

position =
30

mapping =
MAIN_GUARD_EXACTLY_ONCE
```

The old mutation replaced the complete canonical guard with:

```python
main()
```

The corrected mutation replaces the complete canonical guard, including its trailing newline, with an empty string.

Generated fixture 30:

```text
AST parse =
pass

canonical main guards =
0

direct top-level main calls =
0

actual failed checks =
["MAIN_GUARD_EXACTLY_ONCE"]

TOP_LEVEL_SURFACE_EXACT =
pass
```

### Fixture 31 construction

Fixture 31 is appended exactly as:

```text
name =
extra_top_level_main_call

position =
31

mapping =
TOP_LEVEL_SURFACE_EXACT
```

It preserves the canonical guard and inserts exactly one additional direct top-level call immediately before it:

```python
main()

if __name__ == "__main__":
    main()
```

Generated fixture 31:

```text
AST parse =
pass

canonical main guards =
1

direct top-level main calls =
1

actual failed checks =
["TOP_LEVEL_SURFACE_EXACT"]

MAIN_GUARD_EXACTLY_ONCE =
pass
```

## Module-body execution-surface proof

The combined fixed checks now prove that a valid Runner module body contains only:

1. the exact future import;
2. the exact imports `json`, `os`, and `re`;
3. six ordered constant assignments;
4. six ordered top-level function definitions;
5. one canonical main guard as the final top-level statement; and
6. zero other top-level statements.

`TOP_LEVEL_SURFACE_EXACT` structurally consumes only leading imports, exactly six approved simple assignments, top-level `FunctionDef` statements, and an optional canonical final guard. Every expression, direct call, extra assignment, noncanonical `if`, class, async function, loop, `try`, `with`, `match`, deletion, or other statement is rejected. Complete guard absence remains solely the responsibility of `MAIN_GUARD_EXACTLY_ONCE`.

The prior direct-main skip helper is absent from the frozen Auditor.

## Exact public fixture outcomes

| # | Fixture | Actual sole failed check |
| ---: | --- | --- |
| 1 | `import_added` | `IMPORT_ALLOWLIST` |
| 2 | `top_level_assignment_added` | `TOP_LEVEL_SURFACE_EXACT` |
| 3 | `runner_schema_changed` | `BOUND_CONSTANTS` |
| 4 | `variable_order_swapped` | `VARIABLE_NAMES_EXACT` |
| 5 | `shape_label_added` | `SHAPE_LABELS_EXACT` |
| 6 | `helper_function_added` | `FUNCTION_SET_EXACT` |
| 7 | `function_signature_changed` | `FUNCTION_SIGNATURES_EXACT` |
| 8 | `fourth_environment_get` | `ENVIRONMENT_GETS_EXACT` |
| 9 | `environment_get_order_swapped` | `ENVIRONMENT_GETS_EXACT` |
| 10 | `os_getenv_added` | `OS_USAGE_ALLOWLIST_EXACT` |
| 11 | `os_putenv_added` | `OS_USAGE_ALLOWLIST_EXACT` |
| 12 | `os_remove_added` | `OS_USAGE_ALLOWLIST_EXACT` |
| 13 | `os_execv_added` | `OS_USAGE_ALLOWLIST_EXACT` |
| 14 | `path_condition_return_pair_swapped` | `CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT` |
| 15 | `adapter_condition_return_pair_swapped` | `CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT` |
| 16 | `path_bound_changed` | `PATH_PUBLIC_BOUND_EXACT` |
| 17 | `adapter_regex_broadened` | `ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT` |
| 18 | `classified_result_field_order_swapped` | `CLASSIFIED_RESULT_CONTRACT_EXACT` |
| 19 | `classified_result_status_changed` | `CLASSIFIED_RESULT_CONTRACT_EXACT` |
| 20 | `integrity_blocker_removed` | `INTEGRITY_RESULT_CONTRACT_EXACT` |
| 21 | `integrity_labels_changed` | `INTEGRITY_RESULT_CONTRACT_EXACT` |
| 22 | `read_environment_called_twice` | `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT` |
| 23 | `post_result_environment_value_append` | `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT` |
| 24 | `post_result_shape_labels_replaced` | `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT` |
| 25 | `post_result_dictionary_item_assignment` | `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT` |
| 26 | `result_alias_mutation` | `FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT` |
| 27 | `second_print_added` | `ONE_COMPACT_JSON_PRINT` |
| 28 | `absolute_path_literal_added` | `NO_VALUE_LENGTH_PATH_SECRET_OR_EXCEPTION_DISCLOSURE` |
| 29 | `file_open_added` | `NO_FILE_NETWORK_SUBPROCESS_DATABASE_DYNAMIC_ACTIONS` |
| 30 | `main_guard_removed` | `MAIN_GUARD_EXACTLY_ONCE` |
| 31 | `extra_top_level_main_call` | `TOP_LEVEL_SURFACE_EXACT` |

Passing matrix result:

- Matrix schema / version / status: `sentigraph_b05_per_variable_configuration_shape_static_matrix_rc1_v0_2 / 0.2 / pass`
- Valid fixture accepted / checks: `1/1 / 21/21`
- External Runner checks: `21/21`
- Negative fixtures tested / rejected: `31/31 / 31/31`
- Exact single-violation matches: `31/31`
- Fixture parse failures: `0`
- Failed checks: `[]`

## External Runner immutability and read ledger

- Basename: `.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py`
- Approved bytes: `3266`
- Approved SHA-256: `5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250`
- Embedded bytes / SHA-256: `3266 / 5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250`
- Candidate 1 matrix reads / reopens: `1 / 0`
- Candidate 2 matrix reads / reopens: `1 / 0`
- Final qualification reads / reopens: `1 / 0`
- Total physical reads: `3`
- Manual reads outside authorized processes: `0`
- Modifications / replacements / normalizations / repository copies: `0 / 0 / 0 / 0`
- Imports / runtime executions: `0 / 0`
- Embedded / frozen / external equality: `true / true / true`

## Final qualification

- Executions / retries: `1 / 0`
- Exit code: `0`
- Stderr: `empty`
- Stdout lines: `1`
- Schema: `sentigraph_b05_per_variable_configuration_shape_static_qualification_rc1_v0_2`
- Version / status: `0.2 / pass`
- Valid / external checks: `21/21 / 21/21`
- Negative tested / rejected: `31/31 / 31/31`
- Exact single failures: `31/31`
- Parse failures: `0`
- Fixture 30 actual failed checks: `["MAIN_GUARD_EXACTLY_ONCE"]`
- Fixture 31 actual failed checks: `["TOP_LEVEL_SURFACE_EXACT"]`
- Runner reads / reopens / imports / executions: `1 / 0 / 0 / 0`
- Embedded / frozen / external equality: `true / true / true`
- Safe failed-check identifiers: `fixed enum only`
- Failed checks: `[]`

## Hard-zero ledger

- Protected artifact reads: `0`
- Receipt reads: `0`
- Real environment reads / enumeration: `0 / 0`
- HKCU reads / writes: `0 / 0`
- CIB operations: `0`
- Application imports / event loops: `0 / 0`
- Diagnostic Runner runtime executions / imports: `0 / 0`
- GET attempts: `0`
- Provider Result / package / collector access: `0 / 0 / 0`
- Runner network / subprocess actions: `0 / 0`
- Database / persistence: `0 / 0`
- Product-code changes: `0`
- Test changes: `0`
- Project Source reads / changes: `0 / 0`
- Production / export / delivery: `0 / 0 / 0`

Auditor matrix and qualification invocations were static governance-tool processes and did not import or execute the Runner.

## Repository scope

Exact changed-file allowlist:

1. Modified: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
2. Added: `docs/health/sentigraph_baseline_v2_6_fixed_prompt_4_per_variable_configuration_shape_static_auditor_rc1_1_contract_correction_repair_report_v1_0.md`

Files modified / added / deleted: `1 / 1 / 0`.

Product code / tests / Project Source changes: `0 / 0 / 0`.

## Directly established

- The corrected frozen Auditor accepts the embedded valid fixture and exact external Runner under all twenty-one checks.
- Fixtures 1 through 29 retain identical matched regions, replacement regions, branch source, and generated negative Runner source.
- Fixture 30 is the only changed pre-existing mutation and now isolates total main-guard absence.
- Fixture 31 proves that every additional direct top-level `main()` call is rejected.
- The complete thirty-one-fixture matrix has exact single-check isolation.
- The external Runner matched its approved and embedded identities in all three authorized reads and was never imported or executed.

## Not established

- No real environment value, receipt, HKCU state, or CIB binding was examined.
- No Sentigraph application or product module was imported.
- No event loop or HTTP GET was attempted.
- No endpoint behavior, Provider Result, collector behavior, configuration validity, or product defect was established.
- This task does not independently accept RC1.1 and does not authorize Risk Prompt 1.

## Risk Prompt 1 and Source boundary

- Risk Prompt 1 state: `unconsumed / unselected / unauthorized / Goal-unauthorized / unexecuted`
- Risk Prompt 1 candidate eligibility: `pending independent ChatGPT acceptance of the corrected Auditor RC1.1`
- Source recommendation: `no Project Source update in this task; obtain independent acceptance and a stable Risk Prompt 1 terminal result before reconsidering synchronization`
- Next action: independently review the pushed frozen Auditor, this report, the complete terminal receipt, and a fresh user re-upload of the unchanged repository-external Runner.
