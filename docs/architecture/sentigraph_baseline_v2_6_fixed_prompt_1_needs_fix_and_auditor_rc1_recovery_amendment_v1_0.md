# Sentigraph Baseline v2.6 Fixed Prompt 1 Needs-fix and Auditor RC1 Recovery Amendment v1.0

## 1. Amendment identity and state

```text
amendment schema =
sentigraph_baseline_v2_6_fixed_prompt_1_auditor_rc1_recovery_amendment_v0_1

amendment version = 1.0

document state at commit =
amendment_candidate_pending_independent_acceptance

intended effective state after independent ChatGPT acceptance =
effective_and_independently_accepted

repository =
dgmpurf/Sentigraph

starting branch / HEAD =
main / 52d28a9b0078e557f6729ac9113a5a1e96d6af40
```

This document is a governance amendment candidate. It does not claim its own
independent acceptance, authorize Auditor RC1 implementation, or create
protected-access or runtime authority.

### Approval and contract identities

```text
exact approval received = yes

Compact approval phrase SHA-256 =
0e14244e4e2b6ede9f1d13f78047735cd436dc48cf9f3e13f5cb82aeb886ad36

Recovery Amendment Contract V1 SHA-256 =
62c016caee63fcf05eb6dbf9eed5ae9a334e91233c15ff1f02466d36a6a959ad
```

The approval authorizes one fresh Goal, this one new docs-only amendment,
bounded documentation validation, and ready-only commit and push. It does not
authorize modifying the committed Auditor, opening or executing the external
Runner, creating Auditor RC1, reading configuration or Project Source, or
performing CIB, application, GET, product, or runtime work.

## 2. Preserved Baseline v2.6 establishment

```text
Baseline v2.6 status =
effective_and_independently_accepted

Baseline establishment commit =
2519763b30377737d783941e449602a6dfa048f9

Baseline document bytes / SHA-256 / blob =
14698 /
5440770204d30b18f2d7eb3855ee6f90a7e6281f6922a4f9be34c5f6f8dad408 /
3dcece387d0b90a5d719bef90f4478b4e15aa245
```

The bound Baseline document passed identity, strict UTF-8, and no-BOM
verification. It was read once and reopened zero times under this amendment.

This amendment changes only the planned use of the remaining Fixed reservation
and the late-stage route. It does not erase, replace, or reclassify the accepted
Baseline establishment.

## 3. Fixed Prompt 1 history preserved without reclassification

The Codex candidate result and the independent review result remain separate.

### Codex candidate history

```text
Fixed Prompt 1 Codex Decision = ready

Codex runtime classification =
ready_per_variable_configuration_shape_diagnostic_static_qualification_pending_independent_acceptance

completion commit =
52d28a9b0078e557f6729ac9113a5a1e96d6af40

Auditor bytes / SHA-256 / blob =
40290 /
bf2ef0c113a5c9b13f9c44574ccb16cceca9e791c0d6d40c088e833625e3b09d /
9077f454ce8adc54306206416b4f43c634e530ad

candidate versions / matrix invocations =
1 / 1

Runner executions / environment reads =
0 / 0
```

The committed Auditor passed identity, strict UTF-8, no-BOM, and AST checks
under this amendment. It was read once, reopened zero times, and not executed.

### Independent review result

```text
Fixed Prompt 1 independent Decision = needs_fix

independent classification =
needs_fix_static_auditor_incomplete_dataflow_and_side_effect_proof

Fixed Prompt 1 consumed / reusable =
yes / no

historical result reclassified =
no

Fixed Prompt 1 independently accepted as ready =
no
```

The independent needs-fix result accepts neither the Codex ready candidate nor
protected-execution eligibility. It does not establish that the retained Runner
source is defective. It establishes that the committed Auditor did not prove
all required semantics strongly enough.

## 4. Retained external Runner candidate identity

The following identity is recorded from the exact approval only:

```text
external Runner basename =
.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py

bytes =
3266

SHA-256 =
5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250

state =
retained_unexecuted_byte_immutable_candidate

Runner executions =
0

environment reads attributable to Runner runtime =
0

Runner source modification required by current independent review =
not established
```

This amendment did not open, read, modify, or execute the external Runner.
Future Auditor RC1 must keep its bytes unchanged. Any future Runner-byte change
invalidates this RC1 recovery route and requires new governance. Retaining the
Runner identity creates no runtime authorization.

## 5. Independent finding 1 — condition-to-return-label binding

The original Auditor separately checked condition order and the presence of the
expected return-label set. It did not sufficiently prove every exact ordered
pair:

```text
exact branch condition
→ exact Return literal
```

Set or sorted-label equivalence is insufficient.

### Required path-classifier pairs

For `_classify_path_value`, future Auditor RC1 must prove:

```text
value is None
→ missing

not isinstance(value, str)
→ diagnostic_integrity_block

value == ""
→ empty

"\x00" in value or not value.isprintable()
→ nonprintable_or_nul

value != value.strip()
→ leading_or_trailing_whitespace

len(value) > 2048
→ over_public_bound

final return
→ shape_valid
```

### Required adapter-classifier pairs

For `_classify_adapter_value`, future Auditor RC1 must prove:

```text
value is None
→ missing

not isinstance(value, str)
→ diagnostic_integrity_block

value == ""
→ empty

"\x00" in value or not value.isprintable()
→ nonprintable_or_nul

value != value.strip()
→ leading_or_trailing_whitespace

len(value) > 128
→ over_public_bound

re.fullmatch(ADAPTER_PATTERN, value) is None
→ adapter_format_invalid

final return
→ shape_valid
```

Auditor RC1 must structurally bind each condition to its exact literal return
in source order.

## 6. Independent finding 2 — final-output dataflow and no post-result mutation

The original Auditor did not completely prove:

```text
_read_environment()
→ exact values assignment
→ classifier-only uses
→ bounded shape_labels tuple
→ _classified_result return
→ result assignment
→ no later result or nested-container mutation
→ exact json.dumps(result)
→ exact print consumer
```

Auditor RC1 must prove all of the following:

- `_read_environment()` output is assigned exactly once;
- the returned values are used only as the three exact classifier arguments;
- no environment value reaches `warnings`, `blockers`, `variable_names`,
  `shape_labels`, or another output field;
- no result dictionary mutation occurs after `_classified_result(values)` or
  `_integrity_result()`;
- no mutation occurs through `append`, `extend`, item assignment, `update`,
  `setdefault`, `pop`, or alias;
- the only final consumer is the approved compact `json.dumps(result)` inside
  the single print call;
- the exception object is never bound, retained, formatted, or disclosed.

The proof must follow dataflow and side effects structurally rather than infer
safety from isolated nodes.

## 7. Independent finding 3 — exact os usage allowlist

Because `os` is necessarily imported for the three approved environment reads,
an incomplete forbidden-call list is insufficient.

Future Auditor RC1 must apply this fail-closed rule:

```text
allowed references rooted at os =
exactly the three approved os.environ.get calls

all other references, attributes, calls, loads, stores or mutations rooted at os =
rejected
```

The structural proof must reject, without being limited to:

```text
os.getenv
os.environ iteration or conversion
os.environ mutation
os.putenv
os.unsetenv
os.listdir
os.scandir
os.walk
os.remove
os.unlink
os.rename
os.replace
os.mkdir
os.makedirs
os.rmdir
os.removedirs
os.system
os.popen
os.exec*
os.spawn*
```

Substring-only matching is insufficient.

## 8. Remaining Fixed reservation rebound to Auditor RC1

The original planning scope is superseded:

```text
previous Fixed Prompt 2 =
Stage-specific Runner/Auditor RC2 Static Qualification
```

The amended scope is:

```text
Fixed Prompt 2 =
Per-variable Configuration-shape Static Auditor RC1 Forward Repair

consumed =
no

selected / authorized / Goal-authorized / executed =
no / no / no / no
```

Its future purpose is limited to:

- modifying only the committed static Auditor;
- generating one RC1 forward-repair report;
- preserving the external Runner bytes exactly;
- adding structural dataflow proofs for the three independent findings;
- adding exact single-violation negative fixtures;
- executing no external Runner;
- reading no real environment state;
- creating no protected or runtime authority.

Auditor RC1 requires a fresh exact approval and fresh Goal. This amendment is
not that approval and does not consume Fixed Prompt 2.

## 9. Minimum future RC1 fixture requirements

The future exact RC1 contract must include single-violation fixtures covering
at least:

```text
path_condition_return_pair_swapped
→ exact condition-to-return binding check

adapter_condition_return_pair_swapped
→ exact condition-to-return binding check

post_result_environment_value_append
→ final-output dataflow check

post_result_shape_labels_replaced
→ final-output dataflow check

post_result_dictionary_item_assignment
→ no-post-result-mutation check

os_putenv_added
→ exact os usage allowlist

os_remove_added
→ exact os usage allowlist

os_execv_added
→ exact os usage allowlist
```

Every future fixture must:

- remain valid UTF-8 Python;
- parse successfully;
- alter one bounded semantic region;
- fail exactly one intended safe check;
- contain no real environment value, protected path, or secret.

The future Fixed Prompt 2 exact contract must freeze the final check names,
matrix size, and RC1 file identities. This amendment does not invent them.

## 10. Late-stage scopes deferred

The following original Baseline v2.6 scopes are deferred:

```text
original Fixed Prompt 2 =
Stage-specific Runner/Auditor RC2 Static Qualification

original Risk Prompt 3 =
One Governed B05 GET Smoke RC2

new status =
deferred_to_future_baseline
```

They do not transfer into another current Baseline reservation.

Baseline v2.6 Risk Prompt 3 now has:

```text
selected = no
authorized = no
Goal-authorized = no
executed = no
eligible = no

expected disposition =
close_unused_at_Baseline_v2_6_closure

exception =
only a future explicit governance amendment may change this disposition
```

No current GET RC2 authorization remains.

## 11. Amended ordered route after independent acceptance

The retained Baseline v2.6 route becomes:

```text
1. Fixed Prompt 2
   Per-variable Configuration-shape Static Auditor RC1 Forward Repair

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

Every retained stage requires its own separate selection, exact approval,
Goal authorization, execution, and independent acceptance. No stage
automatically authorizes the next.

## 12. Accounting after amendment Goal activation

```text
accounting before engineering / fixed / conditional / risk =
2 / 1 / 0 / 0

accounting after engineering / fixed / conditional / risk =
3 / 1 / 0 / 0

remaining fixed / conditional / risk =
1 / 2 / 3
```

This docs-only amendment increments engineering only. It consumes no Fixed,
Conditional, or Risk reservation. Planning-budget existence creates no
execution authority.

## 13. Current route states

```text
Fixed Prompt 1 =
needs_fix / consumed / nonreusable / unreclassified

Fixed Prompt 2 Auditor RC1 =
unconsumed / unselected / unauthorized / unexecuted

Risk Prompt 1 =
unconsumed / unselected / unauthorized / unexecuted /
ineligible_pending_Auditor_RC1_independent_acceptance

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

## 14. Current zero-authority matrix

```text
selected engineering route = none
engineering implementation authority = none
protected access = none
receipt read = none
environment read = none
HKCU or persistent-source access = none
configuration mutation = none
CIB comparison / recapture = none / none
Auditor modification = none under this amendment
Runner read / modification / execution = none / none / none
application import / event loop / GET = none / none / none
product-code authority = none
Project Source authority = none
database / persistence = none / none
production / export / delivery = none / none / none
```

After independent acceptance of this amendment, the next-default candidate is
only:

```text
Baseline v2.6 Fixed Prompt 2 =
Per-variable Configuration-shape Static Auditor RC1 Forward Repair

selected / authorized / Goal-authorized / executed =
no / no / no / no
```

A planning default is not approval.

## 15. Directly established by this amendment

This amendment candidate directly records:

- the independently supplied Fixed Prompt 1 needs-fix classification;
- the separation between the prior Codex ready candidate and independent
  needs-fix result;
- Fixed Prompt 1 as consumed, nonreusable, and unreclassified;
- the retained external Runner identity without opening or executing it;
- the three minimum semantic proof gaps for future Auditor RC1;
- the rebind of the remaining Fixed reservation to Auditor RC1 forward repair;
- deferral of Runner/Auditor RC2 qualification and GET RC2 to a future
  Baseline;
- Risk Prompt 1 as currently ineligible pending independent Auditor RC1
  acceptance;
- a complete current zero-authority boundary.

## 16. Not established

This amendment does not establish:

- that its own candidate has been independently accepted;
- any Auditor RC1 implementation, identity, matrix, or report;
- that the external Runner is defective or safe for protected execution;
- any real configuration value, shape classification, or persistent source;
- current CIB equality;
- application, route, HTTP, response, Provider Result, or product behavior;
- any Runtime, GET, repair, production, persistence, export, or delivery
  authority.

## 17. Source lifecycle

- this task does not read or modify Project Source;
- active Project Source remains the accepted Canonical 00–09 set;
- no immediate Source update is required solely for this docs-only amendment;
- Source synchronization should be reconsidered after Auditor RC1 and the first
  stable Risk Prompt 1 result;
- a later stable checkpoint may consider Protocol v2.11 admission for the
  validated static-recovery profile;
- this task does not generate Source candidates.

## 18. Security and privacy boundary

This amendment contains no external Runner source, environment value or
per-variable length, receipt body, HKCU value, salt or combined binding,
absolute local path, Provider Result or package content, exception message or
traceback, credential, or private identity.

Safe content is limited to approved repository-relative filenames, the external
Runner basename, public identity hashes and counters, fixed governance
classifications, and the minimum semantic contract needed to explain future
Auditor RC1.

## 19. Establishment-task action boundary

This task creates one docs-only amendment and performs bounded documentation
and Git validation.

It performs no:

- Auditor modification or execution;
- external Runner read, modification, or execution;
- protected artifact or receipt read;
- environment or HKCU read;
- CIB comparison or recapture;
- application import, event-loop creation, or GET;
- product-code or test modification;
- Project Source read or change;
- database, persistence, production, export, or delivery action.

Auditor execution, Runner execution, product/backend/frontend/browser tests,
application imports, and environment or HKCU diagnostics are not run.
