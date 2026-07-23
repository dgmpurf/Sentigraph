# Sentigraph Baseline v2.6 Fixed Prompt 1 Per-variable Configuration-shape Diagnostic Static Qualification Report v1.0

## 1. Milestone and candidate classification

```text
milestone =
SENTIGRAPH-BASELINE-V2-6-FIXED-PROMPT-1-PER-VARIABLE-CONFIGURATION-SHAPE-DIAGNOSTIC-STATIC-QUALIFICATION

Decision = ready

runtime classification =
ready_per_variable_configuration_shape_diagnostic_static_qualification_pending_independent_acceptance

privacy_issue_stop = false

candidate state =
static_qualification_complete_pending_independent_acceptance
```

This report records static qualification only. The repository-external
diagnostic Runner was not executed, and no real environment, receipt, HKCU,
CIB, application, GET, Provider Result, package, collector, database, or
Project Source was accessed.

## 2. Approval, Goal, and accounting

```text
exact approval received = yes

Compact approval phrase SHA-256 =
538fa4dbb43be4114b0c048e1b71b507e0baee3df17ae15552dcef9573622d1e

Fixed Prompt 1 Contract V1 SHA-256 =
3b91cf95e340791d7d50d6776217e32797ea9a30b141c0d3fcb8783617008dec

approval consumed / reusable = yes / no
Fixed Prompt 1 consumed / reusable = yes / no

Goal title =
Sentigraph Baseline v2.6 Per-variable Configuration-shape Diagnostic Static Qualification

Goal requested / activated / reusable =
yes / yes / no
```

```text
accounting before engineering / fixed / conditional / risk =
1 / 0 / 0 / 0

accounting after activation engineering / fixed / conditional / risk =
2 / 1 / 0 / 0

remaining fixed / conditional / risk =
1 / 2 / 3
```

Risk Prompt 1 remains unconsumed, unselected, unauthorized, Goal-unauthorized,
and unexecuted.

## 3. Bound Baseline document identity and read ledger

Approved repository-relative identity:

`docs/architecture/sentigraph_post_baseline_v2_5_configuration_shape_block_and_recovery_baseline_v2_6.md`

```text
reads / reopens = 1 / 0
bytes = 14698
SHA-256 = 5440770204d30b18f2d7eb3855ee6f90a7e6281f6922a4f9be34c5f6f8dad408
Git blob = 3dcece387d0b90a5d719bef90f4478b4e15aa245
strict UTF-8 / BOM absent = pass / pass
identity verification = pass
```

The retained immutable bytes supplied all later governance verification. No
Canonical Source was read.

## 4. Candidate-version ledger

Hard limits:

```text
pre-freeze candidate versions allowed = 3
candidate versions used = 1
bounded recovery versions used = 0
pre-freeze complete matrix invocations = 1
matrix invocation repeats on unchanged candidate = 0
```

| Candidate | Auditor changed | Runner changed | Reason code | Matrix result | Valid / external checks | Negative rejected | Exact single failures | Parse failures |
|---|---:|---:|---|---|---|---:|---:|---:|
| 1 | yes | yes | `initial_candidate` | pass | 24/24 / 24/24 | 20/20 | 20/20 | 0 |

No recovery candidate was required. No defect was classified as an auditor
false positive.

Candidate 1 also established:

```text
embedded/external equality = true
Runner executions = 0
environment / receipt / product access = 0 / 0 / 0
```

## 5. Frozen Auditor identity

Repository-relative path:

`scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`

```text
bytes = 40290
SHA-256 = bf2ef0c113a5c9b13f9c44574ccb16cceca9e791c0d6d40c088e833625e3b09d
strict UTF-8 / BOM absent / AST = pass / pass / pass
source modifications after freeze = 0
```

Exact imports:

```python
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
```

## 6. Frozen repository-external Runner identity

External basename:

`.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py`

```text
bytes = 3266
SHA-256 = 5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250
strict UTF-8 / BOM absent / AST = pass / pass / pass
external files created = 1
post-freeze modifications = 0
embedded / frozen / external equality = true / true / true
diagnostic Runner runtime executions = 0
```

Exact imports:

```python
from __future__ import annotations

import json
import os
import re
```

The static audit established exactly three direct `os.environ.get` calls using
the three approved public names once each and in order. It established no
environment enumeration or mutation and no alternate name access.

## 7. Exact static check inventory

The Auditor contains 24 unique fixed check identifiers in this exact order:

1. `STRICT_UTF8_NO_BOM`
2. `AST_PARSE`
3. `IMPORT_ALLOWLIST`
4. `BOUND_CONSTANTS`
5. `VARIABLE_NAMES_EXACT`
6. `SHAPE_LABELS_EXACT`
7. `ENVIRONMENT_GETS_EXACT`
8. `NO_ENVIRONMENT_ENUMERATION`
9. `NO_ENVIRONMENT_MUTATION`
10. `CLASSIFIER_FUNCTIONS_EXACT`
11. `CLASSIFICATION_PRECEDENCE_EXACT`
12. `CLASSIFIER_RETURN_LABELS_EXACT`
13. `PATH_PUBLIC_BOUND_EXACT`
14. `ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT`
15. `RESULT_FIELDS_EXACT`
16. `RESULT_LABEL_CARDINALITY_AND_ORDER`
17. `INTEGRITY_RESULT_FIXED`
18. `ONE_COMPACT_JSON_PRINT`
19. `NO_VALUE_OR_LENGTH_DISCLOSURE`
20. `NO_PATH_SECRET_OR_EXCEPTION_DISCLOSURE`
21. `NO_FILE_IO`
22. `NO_NETWORK_SUBPROCESS_DATABASE`
23. `NO_DYNAMIC_EXECUTION_OR_REFLECTION`
24. `MAIN_GUARD_EXACTLY_ONCE`

```text
check count / uniqueness / order = 24 / pass / pass
valid fixture accepted = 1 / 1
valid fixture checks = 24 / 24
external Runner checks = 24 / 24
failed_checks fixed-enum only = yes
successful failed_checks = []
```

## 8. Exact negative-fixture matrix

| # | Fixture | Expected sole failed check | Actual failed checks | Result |
|---:|---|---|---|---|
| 1 | `import_added` | `IMPORT_ALLOWLIST` | `IMPORT_ALLOWLIST` | exact |
| 2 | `variable_order_swapped` | `VARIABLE_NAMES_EXACT` | `VARIABLE_NAMES_EXACT` | exact |
| 3 | `shape_label_added` | `SHAPE_LABELS_EXACT` | `SHAPE_LABELS_EXACT` | exact |
| 4 | `fourth_environment_get` | `ENVIRONMENT_GETS_EXACT` | `ENVIRONMENT_GETS_EXACT` | exact |
| 5 | `environment_items_added` | `NO_ENVIRONMENT_ENUMERATION` | `NO_ENVIRONMENT_ENUMERATION` | exact |
| 6 | `environment_write_added` | `NO_ENVIRONMENT_MUTATION` | `NO_ENVIRONMENT_MUTATION` | exact |
| 7 | `classification_precedence_swapped` | `CLASSIFICATION_PRECEDENCE_EXACT` | `CLASSIFICATION_PRECEDENCE_EXACT` | exact |
| 8 | `unknown_classifier_label` | `CLASSIFIER_RETURN_LABELS_EXACT` | `CLASSIFIER_RETURN_LABELS_EXACT` | exact |
| 9 | `path_bound_changed` | `PATH_PUBLIC_BOUND_EXACT` | `PATH_PUBLIC_BOUND_EXACT` | exact |
| 10 | `adapter_regex_broadened` | `ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT` | `ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT` | exact |
| 11 | `result_field_order_swapped` | `RESULT_FIELDS_EXACT` | `RESULT_FIELDS_EXACT` | exact |
| 12 | `output_labels_reversed` | `RESULT_LABEL_CARDINALITY_AND_ORDER` | `RESULT_LABEL_CARDINALITY_AND_ORDER` | exact |
| 13 | `integrity_blocker_removed` | `INTEGRITY_RESULT_FIXED` | `INTEGRITY_RESULT_FIXED` | exact |
| 14 | `second_print_added` | `ONE_COMPACT_JSON_PRINT` | `ONE_COMPACT_JSON_PRINT` | exact |
| 15 | `environment_value_output_added` | `NO_VALUE_OR_LENGTH_DISCLOSURE` | `NO_VALUE_OR_LENGTH_DISCLOSURE` | exact |
| 16 | `absolute_path_literal_added` | `NO_PATH_SECRET_OR_EXCEPTION_DISCLOSURE` | `NO_PATH_SECRET_OR_EXCEPTION_DISCLOSURE` | exact |
| 17 | `file_open_added` | `NO_FILE_IO` | `NO_FILE_IO` | exact |
| 18 | `os_system_added` | `NO_NETWORK_SUBPROCESS_DATABASE` | `NO_NETWORK_SUBPROCESS_DATABASE` | exact |
| 19 | `eval_added` | `NO_DYNAMIC_EXECUTION_OR_REFLECTION` | `NO_DYNAMIC_EXECUTION_OR_REFLECTION` | exact |
| 20 | `main_guard_removed` | `MAIN_GUARD_EXACTLY_ONCE` | `MAIN_GUARD_EXACTLY_ONCE` | exact |

```text
negative fixtures tested / rejected = 20 / 20
exact single-violation matches = 20 / 20
fixture parse failures = 0
```

Every fixture was public, valid UTF-8 Python, AST-parseable, and isolated to one
bounded negative region.

## 9. Final post-freeze qualification

```text
qualification executions / retries = 1 / 0
exit code = 0
stderr empty = yes
stdout lines = 1
stdout format = compact JSON

schema =
sentigraph_b05_per_variable_configuration_shape_static_qualification_v0_1

version = 0.1
status = pass

valid fixture checks = 24 / 24
external Runner checks = 24 / 24
negative tested / rejected = 20 / 20
exact single-violation matches = 20 / 20
fixture parse failures = 0
embedded / frozen / external equality = true / true / true

Runner reads / reopens / executions = 1 / 0 / 0
environment reads = 0
receipt reads = 0
product access = 0
safe failed-check identifiers = fixed enum only
failed_checks = []
```

The final qualification did not modify or unfreeze either source.

## 10. Exact file allowlist

Repository additions:

1. `scripts/governance/sentigraph_b05_per_variable_configuration_shape_static_auditor_v1.py`
2. `docs/health/sentigraph_baseline_v2_6_fixed_prompt_1_per_variable_configuration_shape_diagnostic_static_qualification_report_v1_0.md`

Repository-external addition:

1. `.sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py`

```text
existing repository files modified = 0
other repository files created = 0
other repository-external files created = 0
temporary scripts / results / fixtures created = 0 / 0 / 0
```

The external Runner remains outside Git.

## 11. Hard-zero ledger

```text
protected artifact reads = 0
receipt reads = 0
environment reads / enumeration = 0 / 0
HKCU reads / writes = 0 / 0
CIB operations = 0
application imports = 0
event loops = 0
diagnostic Runner runtime executions = 0
GET attempts = 0
Provider Result / package / collector access = 0 / 0 / 0
network / subprocess actions by Runner = 0 / 0
database / persistence = 0 / 0
product-code changes = 0
Project Source reads / changes = 0 / 0
production / export / delivery = 0 / 0 / 0
```

The one pre-freeze matrix process and one post-freeze qualification process were
static governance-tool executions. They were not diagnostic Runner executions.

## 12. Validation ledger

Performed:

- Auditor strict UTF-8, no BOM, and successful Python parse;
- Runner strict UTF-8, no BOM, and AST parse;
- exact import allowlists;
- one complete passing pre-freeze matrix;
- one complete passing post-freeze qualification;
- embedded, frozen, and external Runner equality;
- 24-check identity, uniqueness, and order validation;
- 20-fixture exact single-failure validation;
- exact repository and external file allowlist validation;
- docs-safe Git diff and cached-diff validation before finalization.

Not run:

- product tests;
- backend tests;
- frontend tests or builds;
- browser tests;
- application-importing tests;
- diagnostic Runner runtime.

These were prohibited or not applicable to static qualification.

## 13. Directly established

Static qualification directly establishes that the frozen Runner source:

- uses only the exact allowed imports;
- reads exactly three approved public environment names once each and in order;
- contains no environment enumeration or mutation;
- implements mutually exclusive ordered shape classifications;
- emits only the bounded ordered result contract through one compact JSON line;
- contains no file, network, subprocess, database, product, application, CIB,
  receipt, or GET operation;
- does not disclose values, lengths, paths, adapter identity, exceptions, or
  tracebacks;
- is byte-identical to the valid embedded fixture;
- passed all 24 static checks and all 20 exact single-violation negative
  fixtures.

## 14. Not established

This static task does not establish:

- any real environment value or per-variable shape label;
- whether persistent or process configuration is present or correct;
- current CIB equality;
- application, Runner runtime, route, HTTP, response, Provider Result, or
  product behavior;
- eligibility as authorization for protected execution;
- independent acceptance of this qualification candidate.

## 15. Current next boundary

```text
Fixed Prompt 1 consumed / reusable = yes / no

Risk Prompt 1 eligibility =
candidate only after independent acceptance of this qualification

Risk Prompt 1 selected / authorized / Goal-authorized / executed =
no / no / no / no
```

No immediate Project Source update is required by this static qualification.
Source synchronization may be reconsidered after independent acceptance or a
later stable Baseline v2.6 runtime checkpoint.

The next action is independent ChatGPT review of this report, the pushed
Auditor, and the separately handed-off frozen external Runner. This report does
not create Risk Prompt 1, a new approval, a protected Goal, or runtime authority.
