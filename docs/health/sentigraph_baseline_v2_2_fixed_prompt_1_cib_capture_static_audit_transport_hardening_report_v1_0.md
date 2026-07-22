# Sentigraph Baseline v2.2 Fixed Prompt 1 CIB Capture Static-audit Transport Hardening Report v1.0

## 1. Status and scope

```text
status = candidate_completed_pending_independent_ChatGPT_acceptance
Decision = candidate_completed_pending_independent_ChatGPT_acceptance
runtime classification = ready_file_based_cib_capture_static_auditor_hardened_pending_independent_acceptance
privacy_issue_stop = false
```

This Fixed Prompt 1 result establishes a file-based, standard-library-only static auditor as a candidate pending independent ChatGPT acceptance. It hardens static-audit transport only. It performs no configuration capture and creates no runtime authority.

## 2. Exact approval and Goal lifecycle

```text
milestone = SENTIGRAPH-BASELINE-V2-2-FIXED-PROMPT-1-CIB-CAPTURE-STATIC-AUDIT-TRANSPORT-HARDENING
compact approval SHA-256 = d5eef2cfb41480b00b430aec3b4dfcfdcc624394537d299c98ea039c9ca48f0d
Static Hardening Contract V1 SHA-256 = 0855f986f1bbfa0c6432c6655be1bf57ca1e30fa51368abd4327f0d2dfb724b8
blocked Risk Prompt 1 approval SHA-256 = 2b58d22bf15cdb61f1f805ab5255d6ee51da7d071cd12c2b265efe9fbd907866
CIB Capture Contract V1 SHA-256 = 19b8fb71d9cb1ba640b2a240e516a8fc28bbb58c8795da8263938ebc560d9ccf
Goal title = Sentigraph Baseline v2.2 CIB Static Audit Transport Hardening
Goal activation verified = yes
approval consumed / reusable = yes / no
Goal reusable = no
```

The raw approval phrase is intentionally excluded. Fixed Prompt 1 does not resume, rerun, or reinterpret Risk Prompt 1.

## 3. Starting repository and Baseline anchors

```text
starting branch = main
starting HEAD = 436db438d7e633f75df9cbc1574835c6fe068077
starting HEAD message = Establish Baseline v2.2 current-product CIB overlay
starting worktree = clean
Baseline v2.2 overlay blob = 4a828454c4f99bf624c7ad1330843e69eedde3c7
Baseline v2.2 overlay SHA-256 = 83fed1e8a7e4aa854a95d0dc93f916611e0fd12d79d8a3dc78bf250127a98fad
Baseline v2.2 overlay bytes = 16153
historical CIB-P1 contract blob = 939190f8794468b0485051e9ab6801a484129cb8
current B05 service blob = f0c4a8768060a840ea1921aeba47a97f2e41f9e3
```

The committed evidence was read once per source with zero reopen. No product module was imported or executed.

## 4. Preserved Risk Prompt 1 blocked history

```text
Risk Prompt 1 Decision = blocked
Risk Prompt 1 runtime classification = blocked_pre_capture_runner_static_audit
Risk Prompt 1 approval / Goal reusable = no / no
Risk Prompt 1 historical result reclassified = no
Risk Prompt 1 formal capture executions = 0
Risk Prompt 1 environment reads = 0
Risk Prompt 1 CIB captured = no
```

This report preserves that terminal history exactly. Static-auditor hardening does not restore, replace, or retry the consumed Risk Prompt 1 authority.

## 5. Root-cause classification

```text
direct root-cause class = multiline_python_c_audit_transport_parse_failure_before_runner_read
```

The blocked attempt transported a multiline audit program through `python -c`; native-shell argument handling corrupted the audit program before it could read the runner. This was an audit-transport parse failure. It was not a Sentigraph configuration failure, process-environment failure, CIB contract failure, or product failure.

The hardened architecture removes multiline interpreter-source transport entirely.

## 6. File-based auditor architecture

The candidate auditor is:

`scripts/governance/sentigraph_cib_capture_static_auditor_v1.py`

```text
auditor source bytes = 39587
auditor source SHA-256 = e9820e2e4729d1ab0387bba7c67a98532b89d40acaf3dc3b11c96f8719b01056
source encoding = strict UTF-8
BOM = absent
imports = Python standard library only
product imports = 0
environment access = 0
audited-runner imports = 0
audited-runner executions = 0
subprocess / network / registry / database actions = 0 / 0 / 0 / 0
multiline python -c used = no
```

The auditor supports exactly `--self-test` and `--audit-runner` with one file argument. Unknown, missing, or conflicting arguments fail closed with bounded JSON. The auditor never echoes the supplied path and never uses stdin to carry source or instructions.

For file audit, it opens the source exactly once in binary mode, retains the bytes, strict-decodes UTF-8, rejects BOM, parses the AST, and reuses the retained bytes, text, and AST for every check. It never imports, executes, or compiles the audited runner into executable bytecode.

## 7. Exact auditor checks

The successful ordered check list is:

1. `SOURCE_UTF8_NO_BOM`
2. `SOURCE_PARSE`
3. `IMPORT_ALLOWLIST`
4. `EXACT_ENVIRONMENT_LOOKUPS`
5. `ENVIRONMENT_LOOKUP_ORDER`
6. `NO_ENVIRONMENT_ENUMERATION`
7. `EXACT_ONE_SALT_GENERATION`
8. `EXACT_ONE_COMBINED_SHA256`
9. `ZERO_PER_VARIABLE_HASHES`
10. `CANONICAL_OBJECT_FIELD_ORDER`
11. `CONFIGURATION_VALUES_SHAPE`
12. `SAFE_RECEIPT_FIELD_ORDER`
13. `CURRENT_PRODUCT_CONSTANTS`
14. `SAFE_RECEIPT_PUBLICATION`
15. `NONDISCLOSING_OUTPUT`
16. `FORBIDDEN_OPERATION_SCAN`

The auditor requires the immutable identifier order:

1. `SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR`
2. `SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT`
3. `SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID`

These are public configuration identifiers only. No value associated with any identifier was accessed or recorded.

The auditor also freezes the current product identity: registry schema `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1`, sample handle `helldivers2-psn-demo`, result filename `provider_result_helldivers2-psn-demo_20260720_123627.json`, route mode `internal_alpha_read_only_local_exchange_projection_operator`, and capability label `b05_local_exchange_projection_read_only`.

## 8. Built-in fixed-public self-test

The built-in self-test used exactly 14 deterministic in-memory fixtures:

1. valid conforming runner accepted;
2. invalid Python syntax rejected;
3. forbidden import rejected;
4. extra environment lookup rejected;
5. wrong environment lookup order rejected;
6. environment enumeration rejected;
7. second salt-generation call rejected;
8. per-variable hash call rejected;
9. wrong canonical-object field order rejected;
10. wrong receipt field order rejected;
11. configuration value used in a path operation rejected;
12. dynamic or value-bearing output rejected;
13. unsafe receipt publication rejected;
14. stdin access rejected.

```text
self-test process executions / retries = 1 / 0
fixture count = 14
fixtures passed / failed = 14 / 0
output schema = sentigraph_cib_capture_static_auditor_self_test_result_v0_1
status = pass
environment_accessed = false
runner_executed = false
external file reads = 0
files created by self-test = 0
```

## 9. External public synthetic-runner audit

One fixed-public repository-external synthetic runner source was created after the built-in self-test passed. Only its fixed basename was used; no absolute temporary path is recorded here.

The synthetic source contains public identifiers, current product constants, representative in-memory object construction, and representative safe-publication syntax. It contains no real configuration value, private path, credential, generated salt, binding, or receipt. It was never imported or executed.

```text
external synthetic runner files created = 1
external synthetic runner source bytes = 4837
external synthetic runner source SHA-256 = a96663c94766f8598d0f042605268365090efa682dbd808987df0e006cdf6f63
external synthetic runner executions = 0
external synthetic runner environment accesses = 0
file-based auditor process executions / retries = 1 / 0
synthetic runner physical reads / reopens = 1 / 0
static checks passed / failed = 16 / 0
file-audit output schema = sentigraph_cib_capture_static_auditor_result_v0_1
file-audit status = pass
environment_accessed = false
runner_executed = false
multiline python -c used = no
```

## 10. Baseline v2.2 accounting

```text
before Fixed Prompt 1 activation, engineering / fixed / conditional / risk = 1 / 0 / 0 / 1
after Fixed Prompt 1 activation, engineering / fixed / conditional / risk = 2 / 1 / 0 / 1
remaining fixed / conditional / risk = 0 / 1 / 2
Fixed Prompt 1 consumed = yes
Risk Prompt 2 = reserved, unconsumed and unauthorized
Risk Prompt 3 = reserved, unconsumed and unauthorized
Conditional Prompt 1 = reserved, unconsumed and unauthorized
```

The Fixed Prompt 1 reservation is consumed by this Goal. No Risk or Conditional reservation is consumed.

## 11. Zero-action and privacy ledger

```text
actual capture runner creation / execution = 0 / 0
environment-source sessions / approved environment reads = 0 / 0
other-name reads / environment enumeration = 0 / 0
environment writes / deletes = 0 / 0
HKCU / HKLM reads or writes = 0 / 0
salt generations = 0
canonical objects = 0
configuration-derived SHA-256 computations = 0
per-variable hashes = 0
safe CIB receipt creations = 0
artifact / package / Provider Result access = 0 / 0 / 0
gate read / enable / mutation = 0 / 0 / 0
application import / app factory / client = 0 / 0 / 0
route / endpoint / B05 GET = 0 / 0 / 0
database / persistence = 0 / 0
provider / collector / network / browser / LLM = 0 / 0 / 0 / 0 / 0
production / public export / delivery = 0 / 0 / 0
Project Source generation / replacement = 0 / 0
```

No raw environment value, adapter-ID value, environment dump, credential, private identity, generated salt value, configuration-derived binding, exception, or traceback is present in this report or committed result.

## 12. Current authorization boundary

```text
file-based auditor hardening = established as candidate pending independent acceptance
new CIB capture authority = not created
CIB captured = no
B05 GET eligibility or authority = not created
next engineering route = not selected by this report
```

This Goal authorizes no actual capture runner, environment lookup, salt generation, canonical object, binding, safe receipt, artifact, gate, application, endpoint, persistence, production, or Project Source action.

Any later engineering action requires a separate governance decision, fresh exact approval, and fresh Goal. The consumed Risk Prompt 1 must not be reused.

## 13. Git finalization

The exact changed-file allowlist is:

1. `scripts/governance/sentigraph_cib_capture_static_auditor_v1.py`
2. `docs/health/sentigraph_baseline_v2_2_fixed_prompt_1_cib_capture_static_audit_transport_hardening_report_v1_0.md`

Ready-only finalization requires cached diff validation, the exact two-path staged set, an ordinary commit with message `Harden CIB capture static audit transport`, an ordinary push of current `main` to `origin/main`, local/remote alignment, and a clean final worktree. The terminal receipt records the resulting commit and alignment; this report does not self-assert its own commit identity.

No amend, rebase, reset, force push, tag, release, history rewrite, or Project Source action is authorized.

## 14. Claims not established

This result does not establish:

- a successful actual CIB capture;
- a process-environment configuration state;
- any real salt, canonical object, combined binding, or safe receipt;
- reuse or reclassification of blocked Risk Prompt 1;
- authority or eligibility for a governed B05 GET;
- artifact existence, identity, or accessibility;
- gate readiness;
- application, route, endpoint, persistence, or production readiness;
- selection or authorization of a next engineering route;
- independent ChatGPT acceptance.

The next action is to stop after ready-only Git finalization and return the committed auditor and health report for independent ChatGPT review.
