# Sentigraph Baseline v2.5 Static Qualification Recovery Governance

## Governance status

- Milestone: `SENTIGRAPH-BASELINE-V2-5-STATIC-QUALIFICATION-RECOVERY-GOVERNANCE`
- Decision candidate: `ready`
- Runtime classification:
  `ready_docs_only_baseline_v2_5_static_qualification_recovery_governance_pending_independent_acceptance`
- Privacy issue stop: `false`
- Exact approval received: `yes`
- Compact approval phrase SHA-256:
  `cea8c406fadc9ea24d6099c1df09bd14381ff1c6a5ec9909b645fd53aefd757a`
- Baseline v2.5 Static Qualification Recovery Governance Contract V1
  SHA-256:
  `7bc9cfffc82cefb967dfc9c6e40605cb95d991c2e70164a9067a44098a419b9b`
- Approval consumed / reusable: `yes / no`
- Goal requested / activated / reusable: `yes / yes / no`
- Goal title:
  `Sentigraph Baseline v2.5 Static Qualification Recovery Governance`
- Status before independent ChatGPT acceptance:
  `ready_pending_independent_acceptance`

This document does not claim `completed_and_independently_accepted`. It creates
governance only. It creates no present engineering, static-V3,
protected-access, runtime, CIB, GET, Project Source, persistence, production,
export, or delivery authority.

## A. Baseline identity

| Field | Value |
| --- | --- |
| Baseline name | Sentigraph Auditor V3 and Runner V3 Static Qualification Recovery Baseline |
| Baseline version | `2.5` |
| Starting repository | `dgmpurf/Sentigraph` |
| Starting branch | `main` |
| Starting commit | `aef7fe7ad0805fca5831d1e70be01a5a1faac855` |
| Starting commit message | `Establish Baseline v2.4 risk-tiered recovery` |
| Repository status before Goal | `clean` |
| Status before independent ChatGPT acceptance | `ready_pending_independent_acceptance` |

## B. Baseline v2.4 historical closure

Baseline v2.4 governance establishment is preserved as:
`ready / completed / independently accepted / consumed / nonreusable`.

Baseline v2.4 final engineering / fixed / conditional / risk:
`1 / 1 / 0 / 0`.

Baseline v2.4 remaining fixed / conditional / risk: `0 / 1 / 2`.

Baseline v2.4 status:
`historical_closed_for_future_prompt_accounting_after_fixed_prompt_1_static_qualification_needs_fix`.

The unused Baseline v2.4 Conditional Prompt 1 and Risk Prompts 1–2:

- Remain historically unconsumed.
- Are not transferred to Baseline v2.5.
- Create no current authority.
- Are closed unused with Baseline v2.4.

Baseline v2.4 Fixed Prompt 1 remains:

| Field | Preserved result |
| --- | --- |
| Decision | `needs_fix` |
| Privacy issue stop | `false` |
| Consumed / reusable | `yes / no` |
| Reclassified as blocked | `no` |
| Reclassified as ready | `no` |
| Runtime classification | `needs_fix_negative_fixture_single_violation_matrix_19_of_20` |

The generic executor UI terminal state does not reclassify this project
Decision. Baseline v2.4 must not be reopened, resumed, repaired, or
retrospectively rewritten.

## C. Preserved Fixed Prompt 1 terminal evidence

| Field | Preserved evidence |
| --- | --- |
| Milestone | `SENTIGRAPH-BASELINE-V2-4-FIXED-PROMPT-1-AUDITOR-V3-RUNNER-V3-STATIC-QUALIFICATION` |
| Approval SHA-256 | `3cae89ae56c5457d18e090ad3b11a10d4f18c9dd8923550315c3959ad06b5c45` |
| Contract SHA-256 | `f6e323494b2a042858c9a12c8413892d6f8c73147f7628da84e4b7c2baeb3397` |
| Goal requested / activated / completed / reusable | `yes / yes / no / no` |
| In-memory validation attempts | `2` |
| Bounded Tier C recovery | `used once` |
| Valid Runner V3 audit | `30 / 30 / 0` |
| Negative fixtures total / tested / rejected | `20 / 20 / 20` |
| Fixture parse failures | `0` |
| Single-violation matches | `19 / 20` |
| Canonical binding constants check | `pass` |
| Configuration bound check | `pass` |
| Receipt-schema-substitution fixture | `pass` |
| Opaque-1048 fixture | `pass` |
| Canonical schema | `exact binding-schema literal` |
| Opaque configuration bound | `2048` |

## D. Exact remaining fixture defect

- Fixture name: `asyncio_run_added`.
- Expected failed checks: `[NO_ASYNCIO_RUN]`.
- Actual failed checks:
  `[NO_ASYNCIO_RUN, PERFORM_GET_CALLED_EXACTLY_ONCE]`.

Direct cause: the fixture added an `asyncio.run(...)` call that also referenced
or called `_perform_get`, thereby introducing two static violations instead of
one.

This is a fixture/check-coupling defect. It is not:

- A Runner V3 semantic defect.
- An Auditor V3 canonicalization defect.
- A product defect.
- A protected-state defect.
- A privacy issue.
- A runtime failure.

The required successor mutation must:

- Insert one syntactically valid AST call equivalent to `asyncio.run(None)`.
- Contain no `_perform_get` name or call.
- Introduce no event-loop creation, ASGI, GET, or application-runtime
  reference.
- Remain syntactically valid Python.
- Fail exactly `NO_ASYNCIO_RUN`.
- Pass the other 29 checks.

Its exact source location and mutation implementation remain subject to the
separately approved Baseline v2.5 Fixed Prompt 1.

## E. Non-durable candidate identities

These are historical in-memory candidate identities from the terminated
Baseline v2.4 Goal only:

| Candidate | Bytes | SHA-256 |
| --- | ---: | --- |
| Auditor V3 | `52159` | `92fdbd0d2f3e2712716a721e29f32338ec0f9c45c9b56b0f731cb7d72cebc88d` |
| Runner V3 | `21428` | `a29714c5574eeaad86afef3e68ef7ffee6983cdc0204b58eeafd431ca34dd07f` |

Explicit boundaries:

- Filesystem targets created: `0`.
- These are not durable artifact identities.
- They are not accepted.
- They are not reusable.
- They must not be used as Baseline v2.5 starting artifacts.
- Baseline v2.5 Fixed Prompt 1 must reconstruct fresh candidates from its exact
  contract.

## F. Preserved zero-change and hard-zero outcome

| Outcome | Preserved value |
| --- | --- |
| Auditor V3 filesystem files created | `0` |
| Runner V3 filesystem files created | `0` |
| Health report created | `0` |
| Repository changed files | `0` |
| Stage / commit / push | `no / no / no` |
| Final repository | `clean` |
| Final HEAD | `aef7fe7ad0805fca5831d1e70be01a5a1faac855` |

Tier A hard-zero ledger:

| Activity | Count |
| --- | --- |
| Auditor V2 / Runner V2 access or reuse | `0` |
| CIB receipt reads | `0` |
| Safe-result reads | `0` |
| Environment reads / enumeration / writes | `0 / 0 / 0` |
| Gate reads / writes | `0 / 0` |
| Application imports | `0` |
| Event-loop creations | `0` |
| Runner V3 executions | `0` |
| GET attempts | `0` |
| Provider Result / package / collector access | `0 / 0 / 0` |
| Network / address resolution / product subprocess | `0 / 0 / 0` |
| Database / persistence | `0 / 0` |
| Product-code changes | `0` |
| Project Source generation / replacement | `0 / 0` |
| Production / export / delivery | `0 / 0 / 0` |

## G. Baseline v2.5 accounting and budget

Baseline v2.5 initial engineering / fixed / conditional / risk:
`0 / 0 / 0 / 0`.

Baseline v2.5 budget fixed / conditional / risk: `1 / 1 / 2`.

Baseline v2.5 remaining fixed / conditional / risk: `1 / 1 / 2`.

Reservations:

- Fixed Prompt 1:
  `Auditor V3 and Runner V3 Static Qualification Recovery`.
- Conditional Prompt 1: one genuinely new, bounded static semantic ambiguity
  only if Fixed Prompt 1 leaves a new unresolved semantic question; it is not
  automatic, not ordinary tool recovery, and not currently authorized.
- Risk Prompt 1: `One Governed B05 GET Smoke V3`, only after Fixed Prompt 1 is
  independently accepted.
- Risk Prompt 2: one post-protected recovery reserve only if Risk Prompt 1
  creates a new bounded protected-state question; it is not automatic and not
  currently authorized.

No reservation creates present engineering, static-source, protected, runtime,
CIB, GET, or Project Source authority.

## H. Risk-tiered policy

### Tier A — protected runtime

- Requires exact approval and a fresh Goal.
- Allows one authorized read or execution and zero automatic retry.
- Allows no alternate resource or endpoint.
- A protected mismatch is `blocked`.
- Tool recovery must not repeat Tier A work.

### Tier B — bound static source

- Primary physical read: `1`.
- Maximum byte-identical recovery physical read: `1`.
- Retained immutable in-memory bytes may be analyzed repeatedly.
- Source identity must be recorded first.
- Source execution remains `0`.
- An identity mismatch is `blocked`.

### Tier C — future Baseline v2.5 static qualification

- Applies only before final byte freeze.
- Parser, checker, fixture-mutation, and report-tool defects are
  `needs_fix_in_goal`.
- Up to two bounded in-Goal static-tool recoveries are allowed.
- Each recovery remains within the same approval, Goal, source contract, and
  file allowlist.
- Recoveries consume no additional Fixed, Conditional, or Risk Prompt.
- Recovery attempts must be separately recorded.
- Completed evidence must survive a later tool failure.
- After two unresolved recoveries, the outcome is terminal `needs_fix`.
- Identity, authorization, privacy, or scope violations remain `blocked`.

## I. Freeze boundary

### Pre-freeze phase

A separately approved future Fixed Prompt 1 may:

- Construct Auditor V3 and Runner V3 in memory.
- Run synthetic parser and fixture self-tests.
- Perform repeated in-memory AST analysis.
- Use up to two bounded Tier C recoveries.
- Retain independent evidence after every completed proof.
- Create no final filesystem target until the complete matrix passes.

### Post-freeze phase

After final candidate bytes and hashes are frozen:

- Auditor V3 may be created exactly once.
- External Runner V3 may be created exactly once.
- Source modification after creation: `0`.
- Final qualification process executions / retries: `1 / 0`.
- No post-freeze tool recovery may change frozen bytes.
- A final identity mismatch or qualification failure is terminal `needs_fix`,
  or `blocked` when identity, privacy, authorization, or scope integrity fails.
- No Tier A resource may be accessed.

## J. Future Fixed Prompt 1 qualification target

Future requirements only:

- Exactly 30 ordered check names.
- Exactly one valid public Runner V3 fixture.
- Exactly 20 negative fixtures.
- Every negative fixture parses successfully.
- Every negative fixture is rejected.
- Every fixture fails exactly its expected single check.
- Single-violation matches: `20 / 20`.
- Valid Runner V3 audit: `30 / 30`.
- Fixture-byte equality among the embedded fixture, frozen bytes, and external
  Runner V3.
- Runner V3 executions: `0`.

The exact ordered 30 checks and 20 fixture names remain those frozen by the
Baseline v2.4 Fixed Prompt 1 contract, including:

- `CANONICAL_BINDING_CONSTANTS_EXACT`.
- `CONFIGURATION_BOUND_EXACT`.
- `receipt_schema_substitution`.
- `opaque_configuration_bound_1048`.
- `asyncio_run_added`.

The corrected `asyncio_run_added` fixture must contain a syntactically valid
call equivalent to `asyncio.run(None)` and no `_perform_get` reference.

## K. V3 canonicalization guarantees

| Property | Required future value |
| --- | --- |
| Canonical binding schema | `sentigraph_b05_server_owned_configuration_identity_binding_v0_1` |
| Receipt schema | `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1` |
| Canonical schema provenance | Direct exact literal, not `receipt["schema"]` |
| Opaque configuration bound | Integer literal `2048` |
| Forbidden bound | `1048` |

A future Auditor V3 must statically require these properties, and a future
Runner V3 must satisfy them.

## L. Receipt carry-forward policy

- Existing independently accepted CIB safe receipt:
  `retained as the first comparison candidate`.
- Automatic CIB recapture: `prohibited`.

A corrected and independently accepted Runner V3 must first compare against the
existing accepted receipt using the exact capture canonicalization. Only if
corrected Runner V3 still produces a CIB mismatch may environment drift or
process-inheritance state be considered. Any recapture requires a separately
selected route, fresh exact approval, and fresh Goal.

## M. Failure classification

`blocked` categories:

- Repository or source identity mismatch.
- Approval or Goal lifecycle failure.
- Unauthorized file or resource access.
- Privacy-boundary violation.
- Changed-file allowlist violation.
- Non-identical Tier B recovery read.
- Tier A protected mismatch or runtime failure.

`needs_fix` categories:

- Parser or checker defect.
- Fixture-mutation coupling.
- Incomplete single-violation matrix.
- Report generation or formatting defect.
- Incomplete static proof while identity and privacy boundaries remain intact.
- Unresolved defect after two bounded pre-freeze Tier C recoveries.
- Post-freeze final qualification failure with identity and privacy intact.

`ready` requires all authorized work and validation to pass.

## N. Current authorization boundary

| Route | Selected | Exact-approved | Goal-authorized | Executed |
| --- | --- | --- | --- | --- |
| Baseline v2.5 Fixed Prompt 1 | yes | no | no | no |
| Conditional Prompt 1 | no | no | no | no |
| Risk Prompt 1 | no | no | no | no |
| Risk Prompt 2 | no | no | no | no |

At the end of this Baseline-establishment task:

- Current engineering authority: `none`.
- Current static-source authority: `none`.
- Current protected-access authority: `none`.
- Current runtime authority: `none`.
- Current GET authority: `none`.
- Current CIB recapture authority: `none`.

## O. Source boundary

- Active Project Source count remains `10`.
- Active canonical indices remain `00` through `09`.
- Canonical `10` remains absent.
- Project Source changed by this task: `no`.
- Source candidate generated by this task: `no`.
- Source replacement authority created: `no`.

A Project Source update remains deferred until a stable V3 qualification or a
later protected-runtime checkpoint.

## Validation boundary

This is a docs-only Baseline v2.5 governance task. Backend tests, frontend
tests, application imports, browser tests, and static V3 qualification are not
run. Validation is limited to the exact changed-file allowlist, strict UTF-8
without BOM, content-safety checks, required governance coverage, and Git diff
checks.
