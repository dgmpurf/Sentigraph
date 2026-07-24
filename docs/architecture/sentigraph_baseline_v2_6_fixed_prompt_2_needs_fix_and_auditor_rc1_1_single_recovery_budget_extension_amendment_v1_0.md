# Sentigraph Baseline v2.6 Fixed Prompt 2 Needs-fix and Auditor RC1.1 Single-recovery Budget Extension Amendment v1.0

## 1. Amendment identity

```text
amendment schema =
sentigraph_baseline_v2_6_auditor_rc1_1_single_recovery_budget_extension_amendment_v0_1

amendment version =
1.0

document state at commit =
amendment_candidate_pending_independent_acceptance

intended effective state after independent ChatGPT acceptance =
effective_and_independently_accepted

repository =
dgmpurf/Sentigraph

starting branch / HEAD =
main / 9307c5865464defee2099a000db2c8edc9b3528f
```

This committed document is an amendment candidate. It does not claim independent acceptance.

Milestone:

`SENTIGRAPH-BASELINE-V2-6-FIXED-PROMPT-2-NEEDS-FIX-AND-AUDITOR-RC1-1-SINGLE-RECOVERY-BUDGET-EXTENSION-AMENDMENT`

Exact approval received: `yes`.

Compact approval phrase SHA-256:

`02ac254c4480b4032e4e623e013aff99005a1921e4c8a4f78b43b9e919d2a3e3`

Single-recovery Budget Extension Contract V1 SHA-256:

`22a5ad05ed0e08b7bed023e10836a92b594606932000bb8e2f8e6ee16c9a537b`

The approval authorizes only this one docs-only amendment, bounded documentation validation, and ready-only Git finalization of this file. It creates no RC1.1 implementation or runtime authority.

## 2. Purpose and effect boundary

This amendment:

1. preserves Fixed Prompt 1 and Fixed Prompt 2 as distinct consumed, nonreusable, unreclassified needs-fix histories;
2. records the independently identified Auditor RC1 top-level execution-surface proof gap;
3. preserves the RC1 Auditor, RC1 report, and external Runner identities;
4. expands only the Baseline v2.6 Fixed budget from 2 to 3;
5. preserves Fixed consumption at 2 and establishes one remaining Fixed recovery reservation;
6. reserves Fixed Prompt 3 for an Auditor RC1.1 top-level execution-surface repair;
7. freezes the minimum future RC1.1 scope and fixture requirement;
8. preserves Risk Prompt 1 as unconsumed and ineligible pending independent RC1.1 acceptance; and
9. creates no engineering implementation, protected-access, runtime, or Project Source authority.

This task does not implement RC1.1.

## 3. Bound evidence and read ledger

### 3.1 Accepted RC1 recovery amendment

Repository-relative path:

`docs/architecture/sentigraph_baseline_v2_6_fixed_prompt_1_needs_fix_and_auditor_rc1_recovery_amendment_v1_0.md`

```text
reads / reopens =
1 / 0

bytes =
16084

SHA-256 =
f2f20902579b090609cdf3baf61cde5e6c7472ffb72118361bcf11205fc24a8f

Git blob =
f81049efb79306a4770b4edd914e6745f868e4f2

strict UTF-8 / BOM absent =
pass / pass
```

### 3.2 Auditor RC1

Repository-relative path:

`scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`

```text
reads / reopens / executions =
1 / 0 / 0

bytes =
69306

SHA-256 =
ec3f1d116a6c9a22043398f65211d90341e628a61b76e076aef8304a052c24c6

Git blob =
c7641dff83b823dc492b6c300c84da8ecd423f41

strict UTF-8 / BOM absent / AST =
pass / pass / pass
```

The Auditor is preserved as committed historical evidence. This amendment does not modify or execute it.

### 3.3 Auditor RC1 report

Repository-relative path:

`docs/health/sentigraph_baseline_v2_6_fixed_prompt_2_per_variable_configuration_shape_static_auditor_rc1_forward_repair_report_v1_0.md`

```text
reads / reopens =
1 / 0

bytes =
12084

SHA-256 =
4c03e76492ed656002dffacbfcc1b6b913877db655807864499f6fe5e5ed7a1b

Git blob =
92706a9b360949fbb883bb3c25e3ee08f610f234

strict UTF-8 / BOM absent =
pass / pass
```

### 3.4 External Runner identity

The following safe identity is recorded only from the exact approval:

```text
basename =
.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py

bytes =
3266

SHA-256 =
5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250

state =
byte_immutable_unexecuted_candidate

reads / modifications / imports / executions in this task =
0 / 0 / 0 / 0
```

The external Runner was not located, opened, read, imported, modified, or executed.

## 4. Preserved Fixed Prompt histories

### 4.1 Fixed Prompt 1

```text
Fixed Prompt 1 independent Decision =
needs_fix

classification =
needs_fix_static_auditor_incomplete_dataflow_and_side_effect_proof

consumed / reusable =
yes / no

historical result reclassified =
no
```

### 4.2 Fixed Prompt 2 Codex candidate

```text
Fixed Prompt 2 Codex Decision =
ready

Codex runtime classification =
ready_per_variable_configuration_shape_static_auditor_rc1_forward_repair_pending_independent_acceptance

completion commit =
9307c5865464defee2099a000db2c8edc9b3528f

Auditor RC1 bytes / SHA-256 / blob =
69306 /
ec3f1d116a6c9a22043398f65211d90341e628a61b76e076aef8304a052c24c6 /
c7641dff83b823dc492b6c300c84da8ecd423f41

RC1 report bytes / SHA-256 / blob =
12084 /
4c03e76492ed656002dffacbfcc1b6b913877db655807864499f6fe5e5ed7a1b /
92706a9b360949fbb883bb3c25e3ee08f610f234

Runner runtime executions / real environment reads =
0 / 0
```

### 4.3 Fixed Prompt 2 independent result

```text
Fixed Prompt 2 independent Decision =
needs_fix

independent classification =
needs_fix_auditor_rc1_top_level_execution_surface_gap

Fixed Prompt 2 consumed / reusable =
yes / no

historical result reclassified =
no

Fixed Prompt 2 independently accepted as ready =
no
```

The Codex ready candidate and the independent needs-fix result are distinct. The independent needs-fix result does not establish a defect in the retained Runner; it establishes an incomplete Auditor proof surface. The committed RC1 Auditor and report remain preserved history and are not rewritten by this amendment.

## 5. Exact RC1 proof gap

The independently supplied finding is:

The RC1 Auditor's top-level surface check permitted direct top-level `main()` statements to be skipped as allowed content, while the separate main-guard check only verified that one canonical guard existed.

Consequently, a Runner containing an additional direct top-level call such as:

```python
main()

if __name__ == "__main__":
    main()
```

could retain:

```text
audit status =
pass

failed_checks =
[]
```

This incomplete proof could permit:

- execution during module import;
- multiple `main()` executions when run as a script; and
- more than one environment-read and output path.

```text
external Runner defect established =
no

external Runner bytes changed =
no

Auditor RC1 proof complete =
no

Risk Prompt 1 eligibility established =
no
```

The counterexample was documented only. It was not executed or reproduced during this amendment task.

## 6. Fixed budget extension

```text
previous Fixed budget / consumed / remaining =
2 / 2 / 0

amended Fixed budget / consumed / remaining =
3 / 2 / 1

Conditional budget / consumed / remaining =
2 / 0 / 2

Risk budget / consumed / remaining =
3 / 0 / 3
```

The extension creates one and only one additional Fixed recovery reservation. It does not replenish Fixed Prompt 1 or Fixed Prompt 2, and it does not create an open-ended retry policy.

Task accounting after this amendment Goal activation:

```text
engineering / fixed / conditional / risk =
5 / 2 / 0 / 0

budget fixed / conditional / risk =
3 / 2 / 3

remaining fixed / conditional / risk =
1 / 2 / 3
```

This docs-only amendment increments engineering only. Budget existence creates no execution authority.

## 7. Fixed Prompt 3 reservation

```text
Fixed Prompt 3 =
Per-variable Configuration-shape Static Auditor RC1.1
Top-level Execution Surface Repair

consumed =
no

selected / authorized / Goal-authorized / executed =
no / no / no / no
```

The future Fixed Prompt 3 purpose is limited to:

- modifying exactly the committed Auditor path;
- creating exactly one RC1.1 repair report;
- keeping the external Runner byte-for-byte unchanged;
- preserving all already accepted RC1 semantic checks;
- closing only the top-level execution-surface proof gap;
- preserving the existing thirty public negative fixtures;
- adding exactly one new public single-violation fixture;
- executing no external Runner; and
- reading no real environment or protected state.

Fixed Prompt 3 requires a separate fresh exact approval and fresh Goal. This amendment is not that approval.

## 8. Minimum future RC1.1 contract

The future RC1.1 may modify only:

`scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`

It must add exactly one report with a future path equivalent to:

`docs/health/sentigraph_baseline_v2_6_fixed_prompt_3_per_variable_configuration_shape_static_auditor_rc1_1_top_level_execution_surface_repair_report_v1_0.md`

It must preserve:

- the external Runner identity;
- the current twenty-one fixed check identifiers and order;
- the current thirty fixtures and mappings;
- condition-to-return binding;
- dataflow and mutation proof;
- fail-closed `os` usage proof;
- fixed-enum safe failures; and
- all hard-zero runtime boundaries.

### 8.1 Exact module-level surface

The combined future checks must establish an exact module body containing only:

1. the exact `from __future__ import annotations`;
2. exact imports `json`, `os`, and `re`;
3. six exact constant assignments, in order:
   - `RUNNER_SCHEMA`;
   - `RESULT_SCHEMA`;
   - `VERSION`;
   - `VARIABLE_NAMES`;
   - `SHAPE_LABELS`;
   - `ADAPTER_PATTERN`;
4. six exact top-level function definitions, in order:
   - `_read_environment`;
   - `_classify_path_value`;
   - `_classify_adapter_value`;
   - `_classified_result`;
   - `_integrity_result`;
   - `main`;
5. one exact canonical main guard as the final top-level statement; and
6. zero other top-level statements.

No direct top-level `main()` call may be permitted outside the canonical guard. No executable expression, alias assignment, extra guard, extra import, extra function, or other statement may be ignored.

### 8.2 Check-isolation rule

To preserve the existing `main_guard_removed` fixture as an exact single violation:

- `TOP_LEVEL_SURFACE_EXACT` must reject any additional or disallowed top-level statement, including direct `main()` calls;
- it may treat the total absence of the canonical guard as belonging solely to `MAIN_GUARD_EXACTLY_ONCE`;
- when a canonical guard is present, it must be the only allowed guard and the final module statement; and
- `MAIN_GUARD_EXACTLY_ONCE` must continue to require exactly one canonical guard.

The combined checks therefore enforce one exact final guard without causing the existing guard-removal fixture to fail two checks.

### 8.3 New fixture

Add exactly:

```text
extra_top_level_main_call
-> TOP_LEVEL_SURFACE_EXACT
```

The fixture must preserve the canonical main guard, insert one additional direct top-level `main()` call, remain strict UTF-8 without BOM, parse successfully, fail exactly `TOP_LEVEL_SURFACE_EXACT`, pass the other twenty checks, and contain no real environment value, protected path, or secret.

```text
existing fixtures preserved =
30

new fixtures =
1

total fixtures =
31

required rejected / exact matches / parse failures =
31 / 31 / 0
```

The future exact RC1.1 approval must separately freeze candidate-version limits, final identities, and qualification counters.

## 9. Current ordered route

After independent acceptance of this amendment, the retained Baseline v2.6 route is:

```text
1. Fixed Prompt 3
   Auditor RC1.1 Top-level Execution Surface Repair

2. Risk Prompt 1
   One Protected Per-variable Configuration-shape Diagnostic

3. Conditional Prompt 1
   Authoritative Configuration-source Diagnosis

4. Risk Prompt 2
   One Bounded Configuration Repair

5. Conditional Prompt 2
   Post-restart Inheritance and CIB Comparison
```

Deferred to a future Baseline:

```text
Stage-specific Runner/Auditor RC2 Static Qualification
One Governed B05 GET Smoke RC2
```

Every retained stage requires separate selection, fresh exact approval, a fresh Goal, and independent acceptance. No stage automatically authorizes the next.

## 10. Current Prompt states

```text
Fixed Prompt 1 =
needs_fix / consumed / nonreusable / unreclassified

Fixed Prompt 2 =
needs_fix / consumed / nonreusable / unreclassified

Fixed Prompt 3 =
unconsumed / unselected / unauthorized / unexecuted

Risk Prompt 1 =
unconsumed / unselected / unauthorized / Goal-unauthorized /
unexecuted / ineligible_pending_RC1_1_independent_acceptance

Conditional Prompt 1 =
unconsumed / unselected / unauthorized / unexecuted

Risk Prompt 2 =
unconsumed / unselected / unauthorized / unexecuted

Conditional Prompt 2 =
unconsumed / unselected / unauthorized / unexecuted

Risk Prompt 3 =
unconsumed / unselected / unauthorized / unexecuted /
ineligible / expected_close_unused
```

After independent amendment acceptance, the next-default candidate is only:

```text
Baseline v2.6 Fixed Prompt 3 =
Auditor RC1.1 Top-level Execution Surface Repair

selected / authorized / Goal-authorized / executed =
no / no / no / no
```

Planning default is not approval.

## 11. Current zero-authority matrix

```text
selected engineering route = none
engineering implementation authority = none
Auditor modification / execution = none / none
Runner read / modification / execution = none / none / none
protected access = none
receipt read = none
environment read = none
HKCU or persistent-source access = none
configuration mutation = none
CIB comparison / recapture = none / none
application import / event loop / GET = none / none / none
product-code authority = none
test-change authority = none
Project Source authority = none
database / persistence = none / none
production / export / delivery = none / none / none
```

## 12. Source lifecycle

- This task does not read or modify Project Source.
- Active Source remains the accepted Canonical 00-09 set.
- This amendment alone does not trigger Source synchronization.
- Source synchronization should be reconsidered only after Auditor RC1.1 is independently accepted and Risk Prompt 1 reaches a stable terminal result.
- A later stable checkpoint may assess Protocol v2.11 admission for the validated static-recovery profile.
- No Source candidate is generated by this task.

## 13. Security, privacy, and hard-zero boundary

This amendment contains no external Runner source, absolute local path, environment value or length, receipt body, HKCU value, salt or combined binding, Provider Result or package content, exception text or traceback, credential, or private identity.

Task hard-zero ledger:

```text
protected artifact access = 0
receipt reads = 0
real environment reads / enumeration = 0 / 0
HKCU reads / writes = 0 / 0
CIB operations = 0
Auditor modifications / executions = 0 / 0
external Runner reads / modifications / executions = 0 / 0 / 0
application imports / event loops / GET attempts = 0 / 0 / 0
product-code changes = 0
test changes = 0
Project Source reads / changes / candidates = 0 / 0 / 0
database / persistence = 0 / 0
production / export / delivery = 0 / 0 / 0
```

## 14. Repository scope and validation boundary

Exact repository allowlist:

```text
created =
docs/architecture/sentigraph_baseline_v2_6_fixed_prompt_2_needs_fix_and_auditor_rc1_1_single_recovery_budget_extension_amendment_v1_0.md

existing repository files modified = 0
other repository files created = 0
repository deletions = 0
repository-external changes = 0
product-code changes = 0
test changes = 0
Project Source reads / changes = 0 / 0
```

Required validation is limited to document encoding, required governance content, identity and arithmetic checks, forbidden-content scanning, exact Git scope, `git diff --check`, and the cached diff check.

Not run and not claimed:

- Auditor;
- external Runner;
- matrix or qualification;
- product, backend, frontend, or browser tests;
- application imports; and
- environment, receipt, HKCU, or CIB diagnostics.

## 15. Directly established and not established

Directly established:

- the three bound repository identities match the exact approval;
- Fixed Prompt 1 and Fixed Prompt 2 remain separate, consumed, nonreusable, and unreclassified;
- the independently identified RC1 defect class is an incomplete Auditor top-level execution-surface proof;
- the Fixed budget is extended from `2 / 2 / 0` to `3 / 2 / 1`;
- one and only one unconsumed Fixed Prompt 3 planning reservation is created; and
- all engineering, protected-access, runtime, and Source authority remains zero.

Not established:

- no defect in the retained external Runner;
- no RC1.1 implementation correctness or qualification;
- no real configuration, environment, receipt, HKCU, or CIB state;
- no application, event-loop, endpoint, HTTP, Provider Result, collector, database, or product behavior;
- no Risk Prompt 1 eligibility; and
- no independent acceptance of this amendment.

Next action after independent acceptance is to prepare a separate exact approval and fresh Goal for Fixed Prompt 3. Until then, Fixed Prompt 3 remains unselected and unauthorized, and Risk Prompt 1 remains ineligible.
