# Sentigraph MVP-B05-CIB-ENV-R2-R2-P1 Fixed Package Report v1.0

## 1. Decision

```text
Decision = ready
privacy_issue_stop = no
milestone = MVP-B05-CIB-ENV-R2-R2-P1
status = candidate_completed_pending_independent_ChatGPT_acceptance
classification = Baseline v1.9 fixed Prompt 1
package_scope = committed fixed helper, static auditor, auditor self-test fixtures, manifest, and report
helper_execution = 0
protected_access = 0
runtime_authority_created = no
```

This report is a frozen static package record. It is valid only when the exact
five repository files match the externally bound SHA-256 identities and the
target Codex run reproduces the one self-test invocation and one fixed-helper
static-audit invocation with zero retry.

## 2. Governance Binding

```text
repository = dgmpurf/Sentigraph
branch = main
starting_commit = fd4624d753f3edeca694ae80d29014ed893cf947
Baseline_v1_9_document_blob = c32e5d8574d57cb6112b2e0b50144baeb6a23cc3
approval_SHA256 = 2a428aa4efe36e1c86231c6f796c22fe27945db38322e86dd625dd90b041b39d
```

Baseline v1.9 accounting after verified Goal activation:

```text
consumed engineering/fixed/conditional/risk = 1/1/0/0
remaining fixed/conditional/risk = 1/4/3
```

The initial CIB-P2, ENV-R1, ENV-R2, and ENV-R2-R1 blocked histories remain
distinct, consumed, nonreusable, and unreclassified.

## 3. Exact Package Files

```text
tools/governance/sentigraph_cib_env_r2_r2_p1/fixed_helper_v0_1.py.txt
SHA-256 = 73a067c2a6dfef3de6a206f121300cfa128e611d3d4386dceb2ada477cc8ed5f
bytes = 11872

tools/governance/sentigraph_cib_env_r2_r2_p1/static_auditor_v0_1.py
SHA-256 = ee855827f3885d89896965c843988adf0d475c2c3cac183182f4260848bfae1a
bytes = 13469

tools/governance/sentigraph_cib_env_r2_r2_p1/auditor_self_test_fixtures_v0_1.json
SHA-256 = 8324157052fe09a5daf02260b505f9cc7b72ccc268ff58233866a2f0433ea8c4
bytes = 4588
```

The manifest binds the report and the first three package files. The manifest
and this report are additionally bound by the final Codex Prompt, avoiding a
self-referential hash cycle.

## 4. Fixed Helper Posture

```text
filename_suffix = .py.txt
importable_by_normal_module_resolution = no
P1_imported = no
P1_compiled = no
P1_copied_to_dot_py = no
P1_executed = no

SEARCH_ROOT_AST_semantic_value = G:\AICODING
MAX_SEARCH_DEPTH = 12
exact_Provider_Result_basename =
  provider_result_helldivers2-psn-demo_20260614_055754.json
```

The helper is future P2 material only. It contains bounded search,
strict-JSON, package-disambiguation, safe reparse-point skipping, exact
three-variable HKCU Environment REG_SZ write/readback logic, and constant-only
stdout. P1 does not execute any of that behavior.

## 5. Auditor Self-test Matrix

One frozen self-test invocation must produce PASS for all cases:

```text
stdout_positive_multiple_allowlisted_constants = PASS
stdout_negative_fstring = PASS
stdout_negative_runtime_concatenation = PASS
stdout_negative_runtime_formatting = PASS
stdout_negative_exception_text = PASS
stdout_negative_path = PASS
stdout_negative_value = PASS
stdout_negative_id = PASS
stdout_negative_count = PASS
stdout_negative_registry_content = PASS

reparse_positive_direct_attribute = PASS
reparse_positive_safe_getattr = PASS
reparse_negative_missing_bitmask = PASS
reparse_negative_missing_skip = PASS
reparse_negative_detection_followed_by_descent = PASS
reparse_negative_normalization_fallback = PASS

AUDITOR_SELF_TEST = PASS
```

The stdout result is based on exact allowlisted constant dataflow, not output
call count. The reparse result accepts both direct attribute access and
`getattr(file_stat, "st_file_attributes", 0)` only with the exact reparse-point
bitmask, non-following inspection, and skip/no-descent control flow.

## 6. Fixed-helper Static Audit

One frozen helper-audit invocation must produce:

```text
HELPER_AUDIT_SOURCE_PARSE = PASS
HELPER_AUDIT_CONSTANTS = PASS
HELPER_AUDIT_IMPORTS = PASS
HELPER_AUDIT_FORBIDDEN_CALLS = PASS
HELPER_AUDIT_STDOUT = PASS
HELPER_AUDIT_REPARSE = PASS
HELPER_AUDIT_REGISTRY = PASS
FIXED_HELPER_STATIC_AUDIT = PASS
```

The static auditor parses the helper with `ast`. It does not import, compile,
copy, or execute the helper.

## 7. P1 Zero-action Ledger

```text
fixed helper imports/compiles/executions = 0/0/0
Provider Result searches/opens/reads/hashes = 0/0/0/0
package searches/safe metadata reads = 0/0
environment reads/writes = 0/0
registry reads/writes = 0/0
configuration capture/hash/salt/canonical object/binding/receipt = 0/0/0/0/0/0
artifact access/hash = 0/0
application imports = 0
endpoint/B05 GET = 0/0
provider/collector/network/LLM/browser = 0/0/0/0/0
database/persistence = 0/0
product code/test/config/route/API/frontend changes = 0/0/0/0/0/0
Project Source/tag/release changes = 0/0/0
```

## 8. Authorization Boundary

```text
ENV-R2-R2-P1 independently accepted = no
ENV-R2-R2-P2 selected/eligible/authorized/executed = no/no/no/no
CIB-P2-R1 selected/eligible/authorized/executed = yes/no/no/no
B05-P5 selected/eligible/authorized/executed = no/no/no/no
```

P1 completion does not authorize helper execution, local discovery,
environment repair, configuration capture, artifact access, application
import, endpoint calls, persistence, production, public, export, or delivery
work.

## 9. Next Boundary

```text
next_boundary = independent ChatGPT acceptance only
```

After independent acceptance, ENV-R2-R2-P2 still requires separate selection,
fresh exact risk approval, and a fresh Goal bound to the exact committed helper,
auditor, fixtures, manifest, and report identities.
