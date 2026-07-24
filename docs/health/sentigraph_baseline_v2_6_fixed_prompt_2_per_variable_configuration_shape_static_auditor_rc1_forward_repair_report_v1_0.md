# Sentigraph Baseline v2.6 Fixed Prompt 2 Per-variable Configuration-shape Static Auditor RC1 Forward Repair

## Milestone and classification

- Milestone: `SENTIGRAPH-BASELINE-V2-6-FIXED-PROMPT-2-PER-VARIABLE-CONFIGURATION-SHAPE-STATIC-AUDITOR-RC1-FORWARD-REPAIR`
- Decision candidate: `ready`
- Runtime classification candidate: `ready_per_variable_configuration_shape_static_auditor_rc1_forward_repair_pending_independent_acceptance`
- Privacy issue stop: `false`
- This is a static governance-tool forward repair. It is not a Runner runtime result, an application result, or a GET result.

## Approval, Goal, and accounting

- Exact approval received: `yes`
- Compact approval phrase SHA-256: `5e874ef49b16df90fefd66fc1b490ea999df75aa4141d99d8e729039c9847c1f`
- Fixed Prompt 2 Auditor RC1 Contract V1 SHA-256: `8da7d85996082501798662f7a484f850ad25d200f508080a36bd527ee5dac768`
- Approval consumed / reusable: `yes / no`
- Fresh Goal title: `Sentigraph Baseline v2.6 Per-variable Configuration-shape Static Auditor RC1 Forward Repair`
- Goal requested / activated / reusable: `yes / yes / no`
- Accounting before, engineering / fixed / conditional / risk: `3 / 1 / 0 / 0`
- Accounting after activation, engineering / fixed / conditional / risk: `4 / 2 / 0 / 0`
- Remaining fixed / conditional / risk: `0 / 2 / 3`

## Bound repository evidence

### Recovery amendment

- Repository path: `docs/architecture/sentigraph_baseline_v2_6_fixed_prompt_1_needs_fix_and_auditor_rc1_recovery_amendment_v1_0.md`
- Reads / reopens: `1 / 0`
- Bytes: `16084`
- SHA-256: `f2f20902579b090609cdf3baf61cde5e6c7472ffb72118361bcf11205fc24a8f`
- Git blob: `f81049efb79306a4770b4edd914e6745f868e4f2`
- Strict UTF-8 / BOM absent: `pass / pass`

### Starting Auditor

- Repository path: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
- Reads / reopens before modification: `1 / 0`
- Bytes: `40290`
- SHA-256: `bf2ef0c113a5c9b13f9c44574ccb16cceca9e791c0d6d40c088e833625e3b09d`
- Git blob: `9077f454ce8adc54306206416b4f43c634e530ad`
- Strict UTF-8 / BOM absent / AST: `pass / pass / pass`

## Historical boundary

- Fixed Prompt 1 state: `needs_fix / consumed / nonreusable / unreclassified`
- The Baseline v2.6 recovery amendment remains accepted and authoritative for this RC1 repair.
- No prior Fixed Prompt 1 result was reclassified.
- No old approval, Goal, execution state, or candidate authority was reused.

## Auditor candidate ledger

Candidate versions total: `2`. Pre-freeze matrix invocations total: `2`. Recovery versions used: `1`.

| Candidate | Reason code | Auditor changed | Runner changed | Matrix executions | Status | Valid checks | External checks | Negative tested/rejected | Exact single failures | Parse failures | Runner reads/reopens/executions |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- | ---: | --- |
| 1 | `initial_rc1_candidate` | yes | no | 1 | fail | 21/21 | 21/21 | 30/30 | 28/30 | 2 | 1/0/0 |
| 2 | `fixture_isolation_defect` | yes | no | 1 | pass | 21/21 | 21/21 | 30/30 | 30/30 | 0 | 1/0/0 |

Candidate 1 failed safely because two fixture routing names did not bind to their intended fixture constructors. Its fixed-enum failed checks were:

- `CLASSIFIED_RESULT_CONTRACT_EXACT`
- `INTEGRITY_RESULT_CONTRACT_EXACT`

Candidate 2 changed only those two fixture routing names. It was the first passing candidate and was frozen immediately. No matrix invocation occurred after freeze.

## Frozen Auditor RC1 identity

- Repository path: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
- Candidate: `2`
- Bytes: `69306`
- SHA-256: `ec3f1d116a6c9a22043398f65211d90341e628a61b76e076aef8304a052c24c6`
- Git blob: `c7641dff83b823dc492b6c300c84da8ecd423f41`
- Strict UTF-8 / BOM absent / AST: `pass / pass / pass`
- Exact import allowlist: `pass`
- Post-freeze source modifications: `0`
- Embedded Runner bytes / SHA-256: `3266 / 5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250`

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

`failed_checks` is restricted to this fixed enum, preserves the stated order, and uses stage-gated decode/parse reporting.

## Exact public fixture matrix

The passing candidate and the final qualification produced the same exact outcomes:

| # | Fixture | Expected and actual sole failed check |
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

Passing matrix result:

- Matrix schema / version / status: `sentigraph_b05_per_variable_configuration_shape_static_matrix_rc1_v0_2 / 0.2 / pass`
- Valid fixture accepted / checks: `1/1 / 21/21`
- External Runner checks: `21/21`
- Negative fixtures tested / rejected: `30/30 / 30/30`
- Exact single-violation matches: `30/30`
- Fixture parse failures: `0`
- Failed checks: `[]`

## External Runner immutability and read ledger

- Basename: `.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py`
- Approved bytes: `3266`
- Approved SHA-256: `5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250`
- State: `byte_immutable_unexecuted_candidate`
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
- Negative tested / rejected: `30/30 / 30/30`
- Exact single failures: `30/30`
- Parse failures: `0`
- Runner reads / reopens / executions: `1 / 0 / 0`
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
- Diagnostic Runner runtime executions: `0`
- GET attempts: `0`
- Provider Result / package / collector access: `0 / 0 / 0`
- Runner network / subprocess actions: `0 / 0`
- Database / persistence: `0 / 0`
- Product-code changes: `0`
- Test changes: `0`
- Project Source reads / changes: `0 / 0`
- Production / export / delivery: `0 / 0 / 0`

Auditor matrix and qualification invocations were static governance-tool processes and did not execute or import the Runner.

## Repository scope

Exact changed-file allowlist:

1. Modified: `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
2. Added: `docs/health/sentigraph_baseline_v2_6_fixed_prompt_2_per_variable_configuration_shape_static_auditor_rc1_forward_repair_report_v1_0.md`

Files modified / added / deleted: `1 / 1 / 0`.

Product code / tests / Project Source changes: `0 / 0 / 0`.

## Directly established

- The frozen Auditor RC1 statically accepts the exact embedded valid fixture and retained external Runner under all 21 fixed checks.
- Every required classifier branch is bound to its exact ordered return label.
- The bounded `main()` environment-read-to-output dataflow, result construction, and no-alias/no-post-result-mutation rules are structurally enforced.
- The `os` usage rule is fail-closed while allowing only the exact three approved environment-read calls.
- All 30 public single-violation fixtures parse and fail exactly their named check.
- The retained external Runner matched its approved and embedded byte identities in all three authorized reads and was never executed.

## Not established

- No real environment value, receipt, HKCU state, or CIB binding was examined.
- No Sentigraph application module was imported.
- No event loop or HTTP GET was attempted.
- No endpoint behavior, response schema, Provider Result, collector behavior, product defect, or configuration validity was established.
- This task does not independently accept RC1 and does not authorize Risk Prompt 1.

## Risk Prompt 1 and Source boundary

- Risk Prompt 1 state: `unconsumed / unselected / unauthorized / Goal-unauthorized / unexecuted`
- Risk Prompt 1 candidate eligibility: `pending independent ChatGPT acceptance of this RC1 repair`
- Source update recommendation: `no Project Source update in this task; obtain independent ChatGPT acceptance first, then make any later Source decision under separate authority`
- Next action: independently review the pushed Auditor RC1, this report, the complete terminal receipt, and a fresh user re-upload of the unchanged repository-external Runner.
