# Sentigraph Baseline v2.4 Risk-tiered Recovery Governance

## Governance status

- Milestone: `SENTIGRAPH-BASELINE-V2-4-RISK-TIERED-RECOVERY-GOVERNANCE`
- Decision candidate: `ready`
- Runtime classification: `ready_docs_only_risk_tiered_recovery_governance_pending_independent_acceptance`
- Privacy issue stop: `false`
- Exact approval received: `yes`
- Compact approval phrase SHA-256: `9fc384251ed831da30bcd98bea733b4372fa8f7124dc7fd9871a27d9e213f9a9`
- Baseline v2.4 Risk-tiered Recovery Governance Contract V1 SHA-256: `df493fb1564f8f1afb7ebc8c83717edb3b622ce0e6f808441c684f0597b981d6`
- Approval consumed / reusable: `yes / no`
- Goal requested / activated / reusable: `yes / yes / no`
- Goal title: `Sentigraph Baseline v2.4 Risk-tiered Recovery Governance`
- Status before independent ChatGPT acceptance: `ready_pending_independent_acceptance`

This document does not claim `completed_and_independently_accepted`. It establishes
governance only and creates no engineering, protected-access, runtime, CIB, GET,
Project Source, production, persistence, export, or delivery authority.

## A. Baseline identity

| Field | Value |
| --- | --- |
| Baseline name | Sentigraph Risk-tiered CIB and Governed B05 GET Recovery Baseline |
| Baseline version | 2.4 |
| Starting repository | `dgmpurf/Sentigraph` |
| Starting branch | `main` |
| Starting commit | `ffe420d728fb6f1d7de437d7c1df0cbc37a9b459` |
| Starting commit message | `Add B05 GET smoke static auditor v2` |
| Repository status before Goal | `clean` |
| Status before independent ChatGPT acceptance | `ready_pending_independent_acceptance` |

## B. Baseline v2.3 historical closure

Baseline v2.3 final engineering / fixed / conditional / risk accounting is
`3 / 1 / 1 / 1`. Its remaining fixed / conditional / risk budget is
`0 / 0 / 0`.

Baseline v2.3 status is
`historical_closed_for_future_prompt_accounting_after_risk_prompt_1_cib_block_and_conditional_prompt_1_static_diagnostic_block`.

The following results remain distinct and are preserved without reclassification:

- Baseline v2.3 establishment Goal:
  `ready / completed / independently accepted / consumed / nonreusable`.
- Fixed Prompt 1:
  `ready / consumed / nonreusable / completed_and_independently_accepted`.
- Risk Prompt 1:
  `blocked / consumed / nonreusable / unreclassified`.
- Risk Prompt 1 runtime classification:
  `blocked_current_product_cib_receipt_or_process_environment_mismatch`.
- Conditional Prompt 1:
  `blocked / consumed / nonreusable / unreclassified`.
- Conditional Prompt 1 runtime classification:
  `blocked_static_provenance_evidence_extraction_incomplete`.

Baseline v2.3 must not be reopened, repaired, resumed, or retrospectively
rewritten.

## C. Preserved Risk Prompt 1 result

| Field | Preserved result |
| --- | --- |
| Milestone | `SENTIGRAPH-BASELINE-V2-3-RISK-PROMPT-1-ONE-GOVERNED-B05-GET-SMOKE-V2` |
| Decision | `blocked` |
| Privacy issue stop | `false` |
| Approval / Goal / Risk Prompt reusable | `no / no / no` |
| Static Auditor V2 audit | `28 / 28 pass` |
| Formal runner executions / retries | `1 / 0` |
| Accepted receipt reads / reopens | `1 / 0` |
| Three approved configuration reads | `1 / 1 / 1` |
| CIB equality | `false` |
| Gate prestate reads / writes | `0 / 0` |
| Application imports | `0` |
| Event-loop creations | `0` |
| GET attempts / completed / retries | `0 / 0 / 0` |
| Repository changes | `0` |
| Commit / push | `no / no` |

The block occurred before protected runtime activation and correctly prevented
gate access, application import, event-loop creation, and GET.

## D. Preserved Conditional Prompt 1 result

| Field | Preserved result |
| --- | --- |
| Milestone | `SENTIGRAPH-BASELINE-V2-3-CONDITIONAL-PROMPT-1-CIB-CANONICALIZATION-PROVENANCE-STATIC-DIAGNOSTIC` |
| Decision | `blocked` |
| Privacy issue stop | `false` |
| Runtime classification | `blocked_static_provenance_evidence_extraction_incomplete` |
| Capture runner reads / reopens / executions | `1 / 0 / 0` |
| Runner V2 reads / reopens / executions | `1 / 0 / 0` |
| Auditor V2 reads / reopens / executions / self-tests | `1 / 0 / 0 / 0` |
| All three sources strict UTF-8 / no BOM / AST parse | `pass / pass / pass` |
| Receipt / safe-result / environment reads | `0 / 0 / 0` |
| Gate / application / event-loop / GET | `0 / 0 / 0 / 0` |
| Repository changes | `0` |
| Commit / push | `no / no` |

Direct failure class:
`task-specific AST evidence-extractor assumption failure after successful source reads`.

The extractor incorrectly expected `configuration_values` to be a separate
assignment rather than allowing it to be embedded directly in the
canonical-object dictionary. The Conditional Prompt newly established no
product, receipt, environment, or runtime defect.

## E. Independent post-block static conclusions

These are independent external static-review conclusions. They are not results
established by the blocked Conditional Prompt:

- Direct root cause:
  `runner_v2_cib_canonical_schema_provenance_error`.
- Secondary conformance defect:
  `runner_v2_opaque_configuration_bound_1048_instead_of_2048`.
- Auditor coverage gap:
  `static_auditor_v2_missing_exact_canonical_binding_constant_provenance`.

The independently established reasoning is:

1. The accepted CIB capture algorithm builds the canonical object with
   `sentigraph_b05_server_owned_configuration_identity_binding_v0_1`.
2. The safe receipt has the distinct schema
   `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1`.
3. Runner V2 reconstructed canonical `schema` from `receipt["schema"]`.
4. Runner V2 therefore substituted the receipt schema for the binding schema.
5. Compact JSON preserves the changed field value, so canonical bytes differ
   independently of the three environment values.
6. The capture contract uses an opaque-string maximum of `2048`.
7. Runner V2 used `1048`.
8. Static Auditor V2 proved structural CIB dataflow but did not prove the exact
   literal and provenance of every canonical constant.
9. Its accepted fixture matrix did not include receipt-schema substitution or
   the `1048`-bound negative case.
10. Blind CIB recapture cannot repair Runner V2 while the schema substitution
    remains.

The following remain not established:

- Environment drift: `no`.
- Environment stability runtime-tested: `no`.
- Accepted receipt defect: `no`.
- Sentigraph product defect: `no`.
- Collector defect: `no`.
- Provider Result defect: `no`.
- Endpoint behavior: `no`.

Static Auditor V2's earlier fixed-public matrix acceptance remains preserved
without reclassification. The later finding is a newly identified semantic
coverage limitation.

## F. Baseline v2.4 budget and reservations

Baseline v2.4 initial engineering / fixed / conditional / risk:
`0 / 0 / 0 / 0`.

Baseline v2.4 budget fixed / conditional / risk: `1 / 1 / 2`.

Baseline v2.4 remaining fixed / conditional / risk: `1 / 1 / 2`.

| Accounting | Engineering | Fixed | Conditional | Risk |
| --- | ---: | ---: | ---: | ---: |
| Initial | 0 | 0 | 0 | 0 |
| Budget | — | 1 | 1 | 2 |
| Remaining | — | 1 | 1 | 2 |

Reservations:

- Fixed Prompt 1: `Auditor V3 and Runner V3 Static Qualification`.
- Conditional Prompt 1: one new bounded static ambiguity only if Fixed Prompt 1
  leaves a genuinely new semantic question; it is not automatic, not tool
  recovery, and not currently authorized.
- Risk Prompt 1: `One Governed B05 GET Smoke V3`, only after Fixed Prompt 1 is
  independently accepted.
- Risk Prompt 2: one post-protected recovery reserve only if Risk Prompt 1
  produces a new bounded protected-state question; it is not automatic and not
  currently authorized.

No reservation creates engineering, protected, runtime, CIB, GET, or Project
Source authority.

## G. Risk-tiered operation model

### Tier A — protected runtime

Tier A includes CIB receipt content, process-environment values, gate reads and
writes, application import, event-loop runtime, Provider Result or package
content, formal runner execution, endpoint and GET activity, database or
persistence, and production, export, or delivery.

Rules:

- Exact approval and a fresh Goal are required.
- One authorized read or execution is allowed, with zero automatic retry.
- No alternate resource or endpoint is allowed.
- Identity, protected-state, or runtime-contract failure is `blocked`.
- Privacy or unapproved access sets `privacy_issue_stop = true`.
- Tool recovery must not repeat a Tier A read or execution.

### Tier B — bound static source

Tier B includes committed source, repository-external but cryptographically
bound source, strict UTF-8 decoding, source-integrity hashing, and AST parsing
and analysis.

Rules:

- Primary physical source read: `1`.
- One identical recovery physical read may be authorized within the same Prompt
  only for source-transport or tool-state failure.
- A recovery read must reproduce the same bytes and SHA-256.
- Identity mismatch is `blocked`.
- Retained immutable in-memory bytes may undergo repeated AST analysis without
  counting as a reopen.
- Source execution remains `0`.
- Source identity must be recorded before deeper semantic analysis.
- Completed per-source evidence must survive a later extractor failure.

### Tier C — governance tooling and documents

Tier C includes parser or extractor logic used only on retained static bytes,
structured evidence summaries, report generation, report wording and
formatting, counters, and docs-only diff cleanup.

Rules:

- Parser, extractor, and report-tool errors are `needs_fix`, not `blocked`.
- One bounded in-Goal tool recovery is allowed.
- Recovery remains within the same approval, Goal, source identities, and
  changed-file allowlist.
- Recovery consumes no additional Fixed, Conditional, or Risk Prompt.
- A second unresolved tool failure becomes terminal `needs_fix`.
- Identity, authorization, privacy, or file-scope violations remain `blocked`.
- Complete conformance still permits ready-only commit and push.

## H. Approval and accounting semantics

- Approval remains consumed on verified fresh Goal activation.
- Approval consumption is not delayed until a file read or runtime action.
- Bounded tool recovery is part of one Prompt and one Goal.
- Accounting is never retrospectively rolled back.
- Tool-recovery attempts are recorded separately from business Prompt
  accounting.
- A `needs_fix` tool outcome does not authorize a protected retry.
- A blocked historical result is never converted into ready by a later repair.

## I. Standard static-analysis lifecycle

1. **P0 — synthetic parser/extractor self-test.**
2. **P1 — read and freeze source identity.**
3. **P2 — retain immutable source bytes in memory.**
4. **P3 — perform independent per-source analysis and persist bounded
   summaries.**
5. **P4 — perform cross-source comparison.**
6. **P5 — generate report.**
7. **P6 — validate the exact diff and perform ready-only commit/push.**

Synthetic fixtures are required before bound-source reads. Identity and
SHA-256 must be recorded before semantic extraction. Every proof must be saved
independently so one failed proof cannot erase completed evidence. A
static-only Prompt must perform no Tier A action.

## J. Failure classification

`blocked` categories:

- Repository or source identity mismatch.
- Approval or Goal failure.
- Unauthorized file or resource access.
- Privacy-boundary violation.
- Changed-file allowlist violation.
- Protected Tier A mismatch or runtime failure.
- A source recovery read that is not byte-identical.

`needs_fix` categories:

- Synthetic parser self-test failure before source reads.
- AST parser or extractor logic error.
- Report generation or formatting defect.
- Incomplete static proof while identity and privacy boundaries remain intact.
- A second bounded Tier C tool failure.

`ready` requires every authorized action and validation to pass.

## K. Fixed Prompt 1 minimum design requirements

These are future requirements only. They create no present implementation
authority.

A successor Static Auditor V3 must add exact checks equivalent to:

- `CANONICAL_BINDING_CONSTANTS_EXACT`.
- `CONFIGURATION_BOUND_EXACT`.

It must require at least:

| Canonical property | Required value |
| --- | --- |
| Schema | `sentigraph_b05_server_owned_configuration_identity_binding_v0_1` |
| Version | `0.1` |
| Binding scope | `b05_one_real_sample_handle_governed_read_only_projection_pre_smoke` |
| Registry schema | `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1` |
| Sample handle | `helldivers2-psn-demo` |
| Result basename | `provider_result_helldivers2-psn-demo_20260720_123627.json` |
| Route mode | `internal_alpha_read_only_local_exchange_projection_operator` |
| Capability label | `b05_local_exchange_projection_read_only` |
| Opaque configuration bound | `2048` |

Required future negative cases include:

- `receipt_schema_substitution`.
- `opaque_configuration_bound_1048`.

A future Runner V3 must:

- Use a new versioned identity.
- Neither modify, rename, nor reuse Runner V2.
- Use the exact binding-schema literal.
- Use the exact `2048` bound.
- Pass Auditor V3.
- Remain static-only until independently accepted.

Exact future check count, fixture count, and artifact identities remain subject
to a separate Fixed Prompt 1 contract.

## L. Receipt carry-forward policy

- Existing independently accepted CIB safe receipt:
  `retained as the first comparison candidate`.
- Automatic CIB recapture: `prohibited`.

A corrected and independently accepted Runner V3 must first compare against the
existing receipt using the exact capture canonicalization. Only if corrected
Runner V3 still produces a CIB mismatch may environment drift or
process-inheritance state be considered. Any receipt recapture requires a
separately selected route, fresh exact approval, and fresh Goal.

## M. Current authorization boundary

| Route or authority | Selected | Exact-approved | Goal-authorized | Executed |
| --- | --- | --- | --- | --- |
| Baseline v2.4 Fixed Prompt 1 | yes | no | no | no |
| Conditional Prompt 1 | no | no | no | no |
| Risk Prompt 1 | no | no | no | no |
| Risk Prompt 2 | no | no | no | no |

At the end of this Baseline-establishment task:

- Current engineering authority: `none`.
- Current protected-access authority: `none`.
- Current runtime authority: `none`.
- Current GET authority: `none`.
- Current CIB recapture authority: `none`.

## N. Hard-zero boundary

| Activity | Count |
| --- | --- |
| Auditor reads / modifications / executions | `0 / 0 / 0` |
| Runner reads / modifications / executions | `0 / 0 / 0` |
| Receipt / safe-result reads | `0 / 0` |
| Environment reads / enumeration / writes | `0 / 0 / 0` |
| Gate reads / writes | `0 / 0` |
| Application imports | `0` |
| Event-loop creations | `0` |
| GET attempts | `0` |
| Provider Result / package / collector access | `0 / 0 / 0` |
| Network / address resolution / subprocess | `0 / 0 / 0` |
| Database / persistence | `0 / 0` |
| Product-code changes | `0` |
| Project Source generation / replacement | `0 / 0` |
| Production / export / delivery | `0 / 0 / 0` |

## O. Source boundary

- Active Project Source count remains `10`.
- Active canonical indices remain `00` through `09`.
- Canonical `10` remains absent.
- Project Source changed by this task: `no`.
- Source candidate generated by this task: `no`.
- Source replacement authority created: `no`.

A later Project Source decision requires separate selection and authority after
a stable recovery checkpoint.

## Validation boundary

This is a docs-only governance baseline. Backend tests, frontend tests,
application imports, and browser tests are not run and are not applicable.
Validation is limited to exact changed-file scope, strict UTF-8 without BOM,
content safety, required governance coverage, and Git diff checks.
