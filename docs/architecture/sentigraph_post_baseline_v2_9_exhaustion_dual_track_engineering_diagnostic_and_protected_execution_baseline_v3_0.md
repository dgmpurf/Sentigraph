# Sentigraph Post-Baseline v2.9 Exhaustion Dual-track Engineering Diagnostic and Protected Execution Baseline v3.0

## 1. Purpose and authority boundary

This document establishes the trial governance definition for Sentigraph
Baseline v3.0. It closes Baseline v2.9 without reclassifying its historical
results and separates future engineering diagnosis from future protected
execution.

This document is a docs-only governance artifact. Its creation does not select
or authorize an Engineering Diagnostic Track, Protected Execution Track, or
Recovery Track Goal. It creates planning capacity only.

Baseline v3.0 becomes repository-effective with status
`effective_pending_independent_ChatGPT_acceptance` only after this exact
document is committed and pushed. Independent ChatGPT acceptance remains a
separate requirement.

## 2. Baseline v2.9 historical closure

Baseline v2.9 is closed as follows:

```text
final accounting engineering / fixed / conditional / risk =
4 / 1 / 1 / 2

remaining fixed / conditional / risk =
0 / 0 / 0

status =
historically_closed_and_exhausted

objective completed =
no

historical results reclassified =
no
```

Baseline v2.9 has no remaining planning or execution capacity. Every Baseline
v2.9 approval and Goal is nonreusable. Clearing a Goal does not erase its
history, consumption, or accounting. Later diagnosis must not reclassify any
prior ready, blocked, or needs-fix result.

The browser-visible current-real B05 objective was not completed under
Baseline v2.9.

## 3. Preserved Baseline v2.9 histories

The following histories remain distinct and unchanged:

```text
Fixed Prompt 1 =
ready_playwright_launch_first_toolchain_stabilized /
completed_and_independently_accepted /
consumed / nonreusable

Conditional Prompt 1 =
needs_fix_contract_repair_source_fact_indentation_mismatch_before_v2_write /
consumed / nonreusable

Risk Prompt 1 =
blocked_playwright_execution_integrity /
navigation completed /
selection not completed /
B05 GET attempts zero /
screenshot attempts zero /
consumed / nonreusable

Risk Prompt 2 =
needs_fix_selection_stage_option_resolution_after_bounded_diagnostics /
actual control Ant Design Select 5.15.4 combobox /
first diagnostic control not rendered /
second diagnostic control found and visible but role-option unresolved /
B05 outbound network zero /
B05 HTTP response zero /
screenshot zero /
full cleanup pass /
consumed / nonreusable
```

These histories do not establish that a B05 GET failed or returned a non-200
response. They do not establish a Sentigraph product defect, retained-runtime
failure, CIB failure, gate-restoration failure, or server-start failure.

## 4. Reported repository-external candidate identities

The following identities are recorded as reported terminal evidence only:

```text
Controller candidate filename =
sentigraph_baseline_v2_9_risk_prompt_2_selection_stage_recovery_business_controller_v2.py

Controller candidate reported bytes / SHA-256 =
46694 /
2ccc2f6e84165c9be4cbdc7da524c962727e9f5fd96f1d98ef439f78c5ec4679

Adapter candidate filename =
sentigraph_baseline_v2_9_risk_prompt_2_selection_stage_recovery_adapter_v3.py

Adapter candidate reported bytes / SHA-256 =
34297 /
15f55d6641416efe5a2133a8c4de1bf8b10ee6db56264ccff65a4b808052c0a5
```

Their governance status is:

```text
repository-external = yes
repository content = no
attachment identity independently verified = no
formal B05 execution authority = none
```

Any future use requires exact attachment-identity verification and successful
Engineering Diagnostic Track acceptance. This document does not inspect or
validate either candidate.

## 5. Baseline v3.0 definition

```text
baseline name =
sentigraph_dual_track_engineering_diagnostic_and_protected_execution

baseline version =
3.0

status after ready repository completion =
effective_pending_independent_ChatGPT_acceptance

execution model =
dual_track_plus_recovery

legacy fixed / conditional / risk budget =
historic only

starting diagnostic / protected / recovery counters =
0 / 0 / 0

budget diagnostic / protected / recovery =
1 / 1 / 1

remaining diagnostic / protected / recovery =
1 / 1 / 1
```

For every Baseline v3.0 reservation:

```text
planning capacity only = yes
selected = no
execution authorized = no
Goal authorized = no
executed = no
reusable execution authority = none
```

## 6. Engineering Diagnostic Track

Baseline v3.0 reserves one planned Engineering Diagnostic Track Goal. A
separately approved Goal may combine:

- targeted tracked-source inspection;
- repository-external Controller and Adapter diagnosis and repair;
- bounded candidate validation;
- zero-B05 browser diagnostics;
- post-validation candidate identity freezing;
- return to ChatGPT for independent engineering acceptance.

The planned resource limit is:

```text
candidate pairs = at most 3
zero-B05 diagnostics = at most 3
```

A local mechanical failure within an approved Engineering Diagnostic Goal does
not require a new approval for every candidate when the same Goal remains
inside its approved semantic repair classes, resource limits, and hard-zero
boundaries.

Targeted inspection may cover only the minimum relevant frontend components,
route declarations, option definitions, directly relevant tests, input
Controller and Adapter implementation, and adjacent package metadata required
for the diagnosis.

Allowed repair classes include:

- locator resolution;
- Ant Design portal or virtual-list readiness;
- native-select, combobox, menu, radio, or button interaction;
- option or target-state resolution;
- selected-state confirmation;
- bounded safe-stage instrumentation;
- local result-envelope, cleanup, and candidate-identity binding;
- mechanical Python, parser, schema, import, path, or process defects.

Forbidden repair classes include:

- product behavior redesign;
- Business API changes;
- CIB, gate, or privacy weakening;
- GET-count weakening;
- acceptance-criterion deletion;
- unbounded fallback;
- dependency or browser substitution;
- tracked repository product-code writes.

A future diagnostic approval may authorize, per diagnostic, one retained
runtime validation, one current CIB verification, three configuration reads,
five process-local gate prestate reads with temporary overrides and restores,
one backend start, one frontend start, one loopback navigation, and one
selection-stage execution.

Every diagnostic must preserve:

```text
B05 outbound network = 0
B05 HTTP response = 0
screenshot = 0
repository / Project Source / Git writes = 0 / 0 / 0
```

### 6.1 Candidate hash rule

Input evidence identities may be bound at Goal activation. New implementation
hashes are frozen only after bounded candidate materialization, diagnosis, and
zero-B05 validation. A candidate implementation hash is not required before
the candidate exists.

### 6.2 Contract style rule

Future contracts should bind authority, semantic invariants, privacy
boundaries, and resource limits. They must not bind fragile whitespace,
absolute indentation, or unverified candidate implementation details.
AST-based or semantic-invariant validation is preferred over
formatting-sensitive assertions.

## 7. Protected Execution Track

Baseline v3.0 reserves one planned Protected Execution Track Goal. It becomes
eligible only after all of the following:

1. Controller and Adapter identities are frozen.
2. Engineering Diagnostic Track zero-B05 validation succeeds.
3. ChatGPT independently accepts the engineering result.
4. A fresh exact Protected Execution approval is received.
5. A fresh Goal is activated.

The planned one-shot invariant is:

```text
retained-runtime receipt reads = 1
stable CIB receipt reads = 1
configuration reads = 3
CIB computations = 1
gate prestate reads / temporary overrides / restores = 5 / 5 / 5
backend / frontend starts = 1 / 1
loopback navigation / refresh / selection = 1 / 0 / 1
B05 GET attempts / completed / retries / second GET = 1 / 1 / 0 / 0
screenshot attempts / completed / second screenshot = 1 / 1 / 0
complete browser, server, port, gate, and tracked-process cleanup = required
```

Protected Execution hard zeros include:

```text
second GET = 0
GET retry = 0
second screenshot = 0
non-loopback browser network = 0
Provider / Collector = 0 / 0
database / persistence mutation = 0 / 0
production / public / export / delivery = 0 / 0 / 0 / 0
repository / Project Source change = 0 / 0
Git write = 0
```

The Protected Execution Track may not repair or modify its frozen
implementation. A required implementation change must return to an available
Engineering Diagnostic Track or require a new baseline after diagnostic
capacity is exhausted.

## 8. Recovery Track

```text
Recovery Track budget = 1
selected at establishment = no
authorized at establishment = no
purpose = post-protected recovery reserve
```

Ordinary engineering diagnosis that fits the Engineering Diagnostic Track
must not consume Recovery capacity.

## 9. Track separation

```text
Engineering Diagnostic Track =
may inspect and repair, but real B05 GET and screenshot are forbidden

Protected Execution Track =
may perform the exact approved protected business action, but may not repair
or change the frozen implementation

Recovery Track =
reserved for post-protected recovery, not normal mechanical development
```

The tracks are separate reservations. No reservation creates authority for
another track.

## 10. Trial status and Project Source lifecycle

```text
dual-track model status =
effective for Baseline v3.0 only /
trial-only /
noncanonical

Project Source update during this Goal = no

Source reconsideration point =
after a stable independently accepted Baseline v3.0 terminal checkpoint and
review of the external governance-research results in the next Chat
```

Canonical Source has not adopted the dual-track model.

## 11. Docs-only no-side-effect record

For this establishment Goal:

```text
runtime / protected actions = 0 / 0
CIB / configuration / gates = 0 / 0 / 0
servers / browser / B05 GET / screenshot = 0 / 0 / 0 / 0
Provider / Collector = 0 / 0
database / persistence = 0 / 0
production / public / export / delivery = 0 / 0 / 0 / 0
Project Source reads / changes = 0 / 0
product code / tests / configuration changes = 0 / 0 / 0
```

The sole repository change authorized by this Goal is this architecture
document.

## 12. Current authorization state and next action

```text
current selected track = none
current execution authority = none
Diagnostic Track selected / authorized / Goal-authorized / executed =
no / no / no / no
Protected Track selected / authorized / Goal-authorized / executed =
no / no / no / no
Recovery Track selected / authorized / Goal-authorized / executed =
no / no / no / no
```

The next action is independent ChatGPT review of this repository governance
document. No Engineering Diagnostic, Protected Execution, Recovery, Source, or
runtime action follows automatically.
