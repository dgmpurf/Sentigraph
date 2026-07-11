# Sentigraph Internal Alpha / MVP Remaining Milestones, Prompt Budget, and Change Control v1.0

## 1. Purpose

This document is the auditable execution ledger for the endpoint defined in
`sentigraph_internal_alpha_mvp_master_completion_baseline_v1_0.md`. It freezes
the remaining fixed milestones, conditional allowances, risk reserve, Prompt
counting rules, dependency path, and rebaseline rules.

It is a planning contract only. No milestone is authorized by appearing here.

## 2. Accounting Summary

```text
baseline_budget_version = 1.0
baseline_planning_prompt_consumed = 1
baseline_planning_correction_allowance = 1
baseline_planning_correction_prompts_consumed = 1
baseline_planning_correction_prompts_remaining = 0
engineering_budget_starts_after_baseline_effective = yes
consumed_engineering_prompts_since_baseline = 0
fixed_milestone_count = 17
conditional_milestone_count = 6
fixed_remaining_prompt_budget = 20
conditional_prompt_allowance = 10
risk_buffer_prompt_allowance = 4
best_case_remaining_prompts = 20
controlled_ceiling_remaining_prompts = 30
hard_ceiling_without_rebaseline = 34
budget_arithmetic_verified = yes
baseline_budget_reliability = evidence_based_but_not_a_guarantee
```

The planning Prompt already consumed is not part of the engineering budget.
The one planning-correction allowance was consumed by the narrow correction to
these two baseline documents. It is outside the engineering budget, cannot be
transferred, and leaves no second Baseline v1.0 correction Prompt. Another
pre-commit material defect requires explicit pause and a new planning decision;
it must not silently consume engineering conditional or risk allowance.

## 3. Prompt Counting Unit

One Codex Prompt is counted when all of these are true:

1. A distinct approved task is sent to Codex.
2. Codex activates or begins the task as a Goal.
3. Codex returns a task receipt or final result.

A task counts even when its result is `blocked` or `needs_fix`. A task does not
become free because no file changed.

The following do not count as engineering Prompts:

- ChatGPT explanations or planning discussion that never start in Codex;
- an approval statement sent by the user without a Codex task beginning;
- a Codex receipt pasted back into ChatGPT;
- manual Git commit, push, tag, or Source replacement performed by the user;
- clarification messages that do not start a new Goal;
- drafted tasks that are never sent;
- a stopped preflight before Goal activation.

One Prompt may combine a narrow implementation, focused tests, nearby
regressions, a health report, and static scans when they share one safety
boundary. Real package or row access, real safe-payload capture, target
authorization, target initialization, gate activation, mutation, and post-write
audit remain separate Prompt boundaries.

ChatGPT must classify each started task against this baseline before decrementing
the appropriate category. A multi-Prompt milestone remains incomplete until all
its work packages and completion evidence are accepted.

## 4. Accounting Start

The engineering ledger starts only after the baseline becomes effective:

```text
baseline_project_state_anchor = e3fb9f9249069fc72b23dd3bd5b6e197d1417f7c
baseline_document_commit = resolved later from Git history
consumed_engineering_prompts_since_baseline = 0
remaining_fixed_prompts = 20
remaining_conditional_allowance = 10
remaining_risk_buffer = 4
baseline_planning_correction_prompts_consumed = 1
baseline_planning_correction_prompts_remaining = 0
```

Suggested milestone states are `not_started`, `authorized`, `in_progress`,
`needs_fix`, `blocked`, `completed`, `replaced`, `deferred`, and
`cancelled_with_reason`.

### 4.1 Source-of-truth and Conflict Resolution

Use this precedence order:

1. Current explicit user instruction and exact current approval scope.
2. Latest committed repository code, tests, docs, health reports, and Git state.
3. Latest main-chat handoff.
4. Committed Master Completion Baseline documents for the frozen MVP endpoint,
   milestone accounting, and change control.
5. Current Canonical Project Source summary.
6. Older historical planning records and archived Sources.

Code and tests define executable behavior. Accepted health reports define
recorded validation evidence. The baseline defines the frozen endpoint,
accounting, and change control. Git identifies authoritative commits, and
Canonical Source summarizes stable committed state. Planning text cannot
upgrade a fixture, candidate, helper, disabled route, static UI, or boundary
object into runtime capability. A newer instruction does not silently widen an
older approval; scope change still requires exact approval and, where
applicable, rebaselining.

## 5. Completed Capability Inventory

The budget does not restart completed historical work.

| Existing capability | Evidence used | Accounting treatment |
| --- | --- | --- |
| Selected-sample C-demo, event detail, sandbox, T0-T6, and report sample routes | Frontend routes/pages; 8S-13 and 8U-8A reports | Preserve and run final regression; do not rebuild. |
| Deterministic Opinion Ecosystem calculator and generated-run contract | Minimum-real-run service/tests; 8S-13 report | Reuse behind governed input; do not redesign formulas. |
| Dense graph builder and controlled generated-run attachment | Dense graph services/tests; 8U and 8V records | Reuse; do not treat controlled fixtures as real-source execution. |
| Analysis Request governance records and routes | Analysis Request schemas/store/routes/golden tests | Preserve; production evidence and production analysis remain outside MVP. |
| Controlled metadata/candidate/report handoff helpers | 8V, 8X, and 8Y completion decisions | Historical boundary evidence only; reuse narrowly where contracts fit. |
| Internal Alpha static shell and disabled GET route consumption | 8Z-20 through 8Z-32 reports and code | Extend to governed safe metadata; do not rebuild the shell. |
| One exact candidate identity lock | 9A-16C through 9A-20 records | Preserve without reproducing protected ID/hash values. |
| Synthetic governed nonproduction persistence implementation | 9A-23A contract, service/tests, 9A-23B report | Audit first, then use only through separately governed future steps. |

## 6. Ordered Fixed Milestones

### MVP-F01 - Independent 9A-23B Post-repair Conformance Audit

- **Completion purpose:** Independently determine whether commit `e3fb9f9`
  satisfies the committed 9A-23A exact-conformance repair contract.
- **Current evidence:** 9A-23A repair contract and decision; 9A-23B service,
  focused test, and health report; commit `e3fb9f9`.
- **Exact remaining gap:** The repair is self-reported ready but has not received
  the required independent post-repair audit.
- **Prerequisites:** Effective baseline; clean project anchor; no real payload or
  runtime target access.
- **Expected deliverables:** One independent read-only or docs-only audit report
  with contract-item findings, verdict, and any narrowly scoped defect list.
- **Required validation:** Tracked-file contract/code/test comparison and only
  the synthetic focused validation explicitly approved for that audit.
- **Approval class:** Independent synthetic conformance audit.
- **Exact Prompt count:** 1.
- **Why fixed:** The current 9A engineering mainline cannot be relied on for the
  MVP until its persistence surface passes independent acceptance.
- **Completion evidence required:** Accepted audit verdict. If a defect is found,
  any separately approved repair must pass and be independently accepted before
  this milestone is complete.
- **Does not authorize:** Repair implementation, real payload, logical runtime
  target, gate activation, mutation, or production `EvidenceItem`.
- **Prompt package:** `MVP-F01-P1` independent audit and receipt.

### MVP-F02 - Real Safe-payload Capture Readiness and Access Contract

- **Completion purpose:** Freeze the exact one-candidate capture procedure,
  allowed fields, access limit, stop rules, custody, and output handling before
  any real row or package is opened.
- **Current evidence:** One exact identity is locked; the 9A-22 architecture
  defines the safe-payload schema; 9A-23B states that no real safe payload exists.
- **Exact remaining gap:** No accepted task-specific capture plan proves how the
  full payload will be obtained once without fallback or protected-value spread.
- **Prerequisites:** MVP-F01 completed; candidate identity remains unchanged.
- **Expected deliverables:** Docs-only readiness decision for exactly one source
  access, strict allowlist, no-substitution behavior, output location class,
  cleanup rule, and independent audit handoff.
- **Required validation:** Contract cross-check against 9A-22, privacy catalog,
  exact-identity binding, and proof that no source access occurred.
- **Approval class:** Docs-only real-data access readiness decision.
- **Exact Prompt count:** 1.
- **Why fixed:** The endpoint requires a bounded real-source path and cannot
  safely jump from an identity record to payload capture.
- **Completion evidence required:** Accepted readiness document with one
  unambiguous capture path and no unresolved equal alternatives.
- **Does not authorize:** Opening a package or row, creating a payload,
  initializing a target, activation, or mutation.
- **Prompt package:** `MVP-F02-P1` capture readiness contract.

### MVP-F03 - One Bounded Real Safe-payload Capture

- **Completion purpose:** Capture one strict safe payload for the locked
  candidate using the accepted single-access procedure.
- **Current evidence:** Identity governance and safe-payload schema exist; no
  real payload has been created.
- **Exact remaining gap:** The governed persistence path has no complete real
  safe input.
- **Prerequisites:** MVP-F02 accepted; separate exact user approval for the one
  bounded source access; unchanged candidate identity and source scope.
- **Expected deliverables:** One local protected safe-payload artifact or record
  in the approved nonproduction location class, a safe capture receipt, and no
  second row/package read.
- **Required validation:** Strict schema, canonical safe hash, identity and
  lineage continuity, one-candidate count, recursive protected-value scan, and
  no extra source access.
- **Approval class:** One bounded real-source safe-payload capture.
- **Exact Prompt count:** 1.
- **Why fixed:** The real-source B-core cannot execute from synthetic input or
  identity metadata alone.
- **Completion evidence required:** Safe receipt showing one candidate, one
  access scope, valid payload schema/hash, and no mutation or production object.
- **Does not authorize:** Persistence target access, gate activation, database
  mutation, production evidence, analysis, report, or public output.
- **Prompt package:** `MVP-F03-P1` one-candidate safe capture and validation.

### MVP-F04 - Independent Real Safe-payload Acceptance Audit

- **Completion purpose:** Independently verify that the captured payload matches
  the locked identity and is safe to present to later nonproduction governance.
- **Current evidence:** F03 will provide the first full real safe payload; the
  schema and forbidden-field contract are already tracked.
- **Exact remaining gap:** Capture self-validation is insufficient for the first
  real-source transition.
- **Prerequisites:** MVP-F03 completed; payload remains unchanged and local.
- **Expected deliverables:** Read-only acceptance audit covering identity,
  lineage, schemas, canonical hashes, warnings, privacy, protected fields,
  substitution, and access history.
- **Required validation:** No source reread; no database access; deterministic
  recomputation from the approved safe artifact only; no protected value in the
  report.
- **Approval class:** Independent safe-payload audit.
- **Exact Prompt count:** 1.
- **Why fixed:** Independent acceptance is required before the first real input
  can cross into a persistence decision.
- **Completion evidence required:** Accepted verdict with
  `candidate_specific_safe_payload_accepted` or a closed defect path.
- **Does not authorize:** Target selection change, activation, mutation,
  production object, analysis, or delivery.
- **Prompt package:** `MVP-F04-P1` independent payload audit.

### MVP-F05 - Logical Nonproduction Target Authorization and Operations Contract

- **Completion purpose:** Authoritatively bind the audited payload path to the
  existing dedicated logical local nonproduction target and define lifecycle,
  cleanup, pause, recovery, and isolation rules.
- **Current evidence:** 9A-22 selects a dedicated repository-relative SQLite
  target and rejects generic case persistence; 9A-23B has not accessed it.
- **Exact remaining gap:** The logical target has design evidence but no
  endpoint-specific authorization or final operator contract.
- **Prerequisites:** MVP-F04 accepted; target label and persistence schemas remain
  compatible with the audited 9A-23B implementation.
- **Expected deliverables:** Docs-only target decision binding candidate,
  payload, target, schema version, disabled default, cleanup, backup exclusion,
  pause behavior, and no-production classification.
- **Required validation:** Git-ignore boundary, no physical path exposure, no
  generic store coupling, no target access, and no environment-value read.
- **Approval class:** Docs-only local nonproduction target authorization.
- **Exact Prompt count:** 1.
- **Why fixed:** The MVP requires durable local governance, and no target may be
  inferred or initialized without a separate decision.
- **Completion evidence required:** Accepted target contract with one target,
  one schema family, and explicit no-fallback semantics.
- **Does not authorize:** Directory/database creation, initialization, gate
  activation, mutation, production storage, or case-store use.
- **Prompt package:** `MVP-F05-P1` target authorization and operations contract.

### MVP-F06 - Disabled-by-default Logical Target Initialization Smoke

- **Completion purpose:** Prove the selected logical target can be initialized
  safely, remains disabled by default, and can be cleaned without touching
  unrelated state.
- **Current evidence:** The store supports explicit enablement and temporary
  SQLite tests; the real logical target has never been exercised.
- **Exact remaining gap:** There is no evidence for the actual local target's
  directory, schema initialization, disabled behavior, or cleanup drill.
- **Prerequisites:** MVP-F05 authorization; separate approval for target access;
  no payload mutation and no gate activation.
- **Expected deliverables:** Initialized empty nonproduction target, safe schema
  inventory/health receipt, disabled-default proof, and deterministic cleanup or
  reset evidence.
- **Required validation:** Disabled construction creates nothing; only the
  authorized target is touched; tables and constraints match contract; record
  count remains zero; cleanup is bounded and auditable.
- **Approval class:** Local nonproduction target initialization and empty-store
  smoke.
- **Exact Prompt count:** 1.
- **Why fixed:** Temporary SQLite tests do not prove the documented local target
  is operable.
- **Completion evidence required:** Empty-target receipt with logical labels
  only, no physical path leak, zero records, and clean reset proof.
- **Does not authorize:** Payload write, gate activation, production evidence,
  generic database migration, or route exposure.
- **Prompt package:** `MVP-F06-P1` target initialization and empty-store smoke.

### MVP-F07 - Exact Gate Activation Decision for Nonproduction Persistence

- **Completion purpose:** Record a separate human decision binding the exact
  candidate, audited payload, gate contract, selected nonproduction target,
  mutation mode, and maximum attempt count.
- **Current evidence:** 9A-20 defines an inactive gate; 9A-22 defines activation
  binding; 9A-23B confirms no activation decision exists.
- **Exact remaining gap:** The MVP endpoint has no activation record for the
  audited payload and initialized target.
- **Prerequisites:** MVP-F06 passed; identity, payload, target, and contract
  hashes unchanged; human review responsibility acknowledged.
- **Expected deliverables:** Docs-only activation decision record with exact
  binding, one-attempt scope, expiry/revocation conditions, and stop rules.
- **Required validation:** Human-authored decision provenance, strict binding,
  no substitution, no automatic trust upgrade, and proof that no mutation ran.
- **Approval class:** Human gate-activation decision recording only.
- **Exact Prompt count:** 1.
- **Why fixed:** A disabled implementation cannot mutate merely because a target
  exists; activation is an independent governance boundary.
- **Completion evidence required:** Accepted activation record that remains
  distinct from execution and contains no reusable broad permission.
- **Does not authorize:** The persistence call itself, a second attempt,
  production `EvidenceItem`, case, analysis, report, or delivery.
- **Prompt package:** `MVP-F07-P1` bound activation decision.

### MVP-F08 - Single Governed Nonproduction Persistence Execution

- **Completion purpose:** Persist exactly one governed nonproduction record for
  the audited candidate under the activated one-attempt contract.
- **Current evidence:** 9A-23B implements the synthetic exact-conformance store,
  command, receipt, attempt reservation, and verification behavior.
- **Exact remaining gap:** No real safe payload has been written to the selected
  local nonproduction target.
- **Prerequisites:** MVP-F01 through MVP-F07 completed; fresh exact execution
  approval; unchanged bindings; empty or conclusively idempotent target state.
- **Expected deliverables:** At most one new governed nonproduction record, one
  attempt reservation, receipt v0.2-compatible evidence, and read-only
  post-commit snapshot.
- **Required validation:** Preflight before mutation; maximum attempt one;
  exactly-one intended record or zero-mutation idempotent outcome; conflict and
  ambiguity pause; no physical path or protected value in record/receipt.
- **Approval class:** One exact local nonproduction persistence execution.
- **Exact Prompt count:** 1.
- **Why fixed:** Durable local state is part of the frozen Internal Alpha endpoint.
- **Completion evidence required:** Safe receipt and snapshots proving mutation
  count, attempt state, exact bindings, and no unrelated change.
- **Does not authorize:** Production Evidence Layer write, production
  `EvidenceItem`, second insert, automatic retry, case mutation, analysis, or
  downstream runtime.
- **Prompt package:** `MVP-F08-P1` one-attempt persistence execution and receipt.

### MVP-F09 - Independent Post-write Integrity, Idempotency, and Recovery Audit

- **Completion purpose:** Independently accept the persisted record and prove
  the workflow can pause, inspect, and obtain a read-only idempotent replay
  result without any hidden mutation.
- **Current evidence:** 9A-23B defines synthetic integrity and ambiguity
  semantics; F08 will provide the first endpoint-specific persisted evidence.
- **Exact remaining gap:** No independent real-path post-write audit exists.
- **Prerequisites:** MVP-F08 completed; no record alteration after receipt.
- **Expected deliverables:** Read-only audit of record/reservation hashes,
  exactly-one count, replay outcome, conflict state, receipt truthfulness,
  recovery limitations, cleanup/revocation procedure design, absence of
  automatic repair/retry, and no-downstream-side-effect proof.
- **Required validation:** Exact replay produces zero mutations; no second
  insert under ambiguity; protected-value/path scan; table isolation; pause and
  recovery procedure review; no record or attempt-ledger mutation during audit.
- **Approval class:** Independent post-write audit and recovery verification.
- **Exact Prompt count:** 1.
- **Why fixed:** A successful write call alone does not prove durable integrity
  or safe operator recovery.
- **Completion evidence required:** Accepted audit with exactly-one or accepted
  idempotent state, no unresolved integrity blocker, and proof that the
  authoritative record and attempt ledger remained unchanged.
- **Does not authorize:** Delete, reset, revoke, repair, update, replace,
  recreate, cleanup/reset drill execution, post-commit repair write, production
  object creation, analysis, or delivery.
- **Prompt package:** `MVP-F09-P1` strictly read-only post-write integrity,
  idempotency, recovery-limit, and procedure-design audit.

```text
MVP-F09_audit_mode = strictly_read_only
MVP-F09_actual_cleanup_execution = no
MVP-F09_actual_reset_execution = no
MVP-F09_mutation_allowed = no
```

### MVP-F10 - Governed Record to Internal Review Console Integration

- **Completion purpose:** Replace synthetic-only operator evidence with a safe,
  read-only projection of the governed record and audit state while preserving
  disabled-by-default behavior.
- **Current evidence:** 8Z provides a safe projection helper, disabled GET route,
  static shell, read-only frontend helper, and browser smoke; all use fixture or
  fallback data.
- **Exact remaining gap:** The operator surface cannot inspect the persisted
  record, attempt state, receipt, warnings, blockers, or pause state.
- **Prerequisites:** MVP-F09 accepted; safe read model is stable; no write action
  is exposed.
- **Expected deliverables:** A backend safe read adapter and route contract over
  the selected nonproduction store, plus frontend rendering for governed,
  disabled, empty, blocked, error, and fallback states.
- **Required validation:** Focused backend/frontend tests, disabled-route tests,
  strict projection allowlist, build, browser smoke, no unsafe CTA, and no path
  or protected-value exposure.
- **Approval class:** Read-only backend/API/frontend integration.
- **Exact Prompt count:** 2.
- **Why fixed:** Human review visibility is a mandatory endpoint capability.
- **Completion evidence required:** Accepted route/API report and browser report
  showing the same safe record/audit state with human review required.
- **Does not authorize:** Write methods, route enablement by default, Review
  Queue runtime, production objects, analysis execution, or public access.
- **Prompt packages:** `MVP-F10-P1` backend read adapter/route contract and
  tests; `MVP-F10-P2` frontend integration, build, and browser QA.

MVP-F10 provides visibility and safe projection only. Page visibility,
`human_review_required = true`, absence of blockers, static labels, an existing
record, or generic prior authorization must not create or imply human review
acceptance.

```text
MVP-F10_responsibility = read_only_operator_visibility_and_safe_projection_only
MVP-F10_human_review_acceptance_created = no
```

### MVP-F11 - Governed Record to Controlled Analysis Input Bridge

- **Completion purpose:** Define and implement a strict one-way adapter from the
  governed nonproduction record plus a separately accepted, versioned human
  review reference to a deterministic internal analysis context without mock
  fallback.
- **Current evidence:** Minimum-real-run, metadata bridge, and generated-run
  helpers exist; 8V/8X use controlled fixtures and do not consume this record.
- **Exact remaining gap:** No accepted bridge or versioned human-review
  acceptance-decision contract binds the persisted record, receipt, warnings,
  blockers, and safe identity to calculator input and run metadata.
- **Prerequisites:** MVP-F10 backend projection accepted. MVP-F11-P1 precedes any
  acceptance action. Before MVP-F11-P2, a separately governed accepted
  `human_review_acceptance_reference` must exist for the exact nonproduction
  record and receipt.
- **Expected deliverables:** MVP-F11-P1 defines the strict bridge projection,
  versioned human-review acceptance-decision contract, required reference
  fields, binding rules, and fail-closed behavior. MVP-F11-P2 implements the
  adapter, accepted-reference validation, tests, lineage/audit references, and
  explicit blocked outcomes.
- **Required validation:** No source or package reread; no mock fallback; exact
  record/receipt/identity/hash binding; missing or rejected acceptance blocks;
  warning/blocker mismatch blocks; unknown fields and weakened boundaries
  block; acceptance does not mutate evidence, upgrade trust, or create a
  production case, `analysis_run`, or other production object.
- **Approval class:** Controlled nonproduction analysis bridge design and backend
  implementation.
- **Exact Prompt count:** 2.
- **Why fixed:** The MVP requires analysis over governed evidence, not only
  fixture demonstrations.
- **Completion evidence required:** Accepted contract and tests proving the
  governed record plus exact accepted reference creates one valid internal
  input or a safe blocked result, while the decision remains nonproduction.
- **Does not authorize:** Production analysis objects, real LLM, provider call,
  public response, automatic execution, or report delivery.
- **Prompt packages:** `MVP-F11-P1` bridge contract, versioned human-review
  acceptance-decision contract, and blocking rules; `MVP-F11-P2` bridge
  implementation, accepted-reference validation, focused tests, regressions,
  and health report.

The `human_review_acceptance_reference` must bind these minimum fields without
embedding real values in the baseline:

- exact persisted record ID or safe record reference;
- exact persistence receipt reference;
- candidate identity digest or equivalent safe identity binding;
- canonical record hash or accepted safe record hash;
- warning count and blocker count;
- `review_decision = accepted_for_controlled_nonproduction_analysis` or an
  equally narrow nonproduction decision;
- bounded reviewer label or reviewer-role label;
- `reviewed_at`;
- human-review-required acknowledgment;
- no-automatic-trust-upgrade acknowledgment;
- acceptance schema, version, and safe hash.

The acceptance is a separate future human action governed by exact approval.
Listing it does not pre-authorize the decision. It does not mean truth verified,
official verification, trust upgrade, production promotion, production
`EvidenceItem` approval, or public-output approval.

### MVP-F12 - Controlled Opinion Ecosystem and Dense Graph Execution

- **Completion purpose:** Run the existing deterministic Opinion Ecosystem and
  dense graph path on the governed analysis input and retain a safe audit link.
- **Current evidence:** The calculator, generated-run contract, dense graph
  builder, adapters, route tests, and fixture browser evidence exist.
- **Exact remaining gap:** Existing runs are fixture/sample driven, not derived
  from the governed nonproduction record.
- **Prerequisites:** MVP-F11 accepted; an accepted
  `human_review_acceptance_reference` exists and matches the exact record,
  receipt, identity binding, record hash, warning count, and blocker count;
  valid internal input; explicit local human action; no production analysis
  object.
- **Expected deliverables:** One controlled internal generated run and graph
  projection with source receipt reference, model metadata, warnings, and all
  required boundary flags.
- **Required validation:** Required modules present; graph consistency;
  deterministic replay; missing/rejected/mismatched acceptance blocks; no mock
  fallback; acceptance causes no evidence mutation, trust upgrade, or
  production object; no prediction/verification/causal or production-score
  claim; no generated public response.
- **Approval class:** Local deterministic analysis and graph execution over
  governed nonproduction input.
- **Exact Prompt count:** 1.
- **Why fixed:** Controlled analysis and ecosystem interpretation are central to
  the B-core endpoint.
- **Completion evidence required:** Accepted run/graph health receipt tied to the
  persisted record and showing all downstream side effects false.
- **Does not authorize:** Production `analysis_run`, production Analysis Result,
  Source 11 runtime, public Sandbox generation, or action execution.
- **Prompt package:** `MVP-F12-P1` integration execution, tests, and health proof.

### MVP-F13 - Human-reviewable Internal Result/Report and Operator Continuity

- **Completion purpose:** Provide a safe internal result/report and a coherent
  review-to-analysis-to-result operator path.
- **Current evidence:** Controlled report-candidate/final-boundary helpers and
  sample report UIs exist; 8V/8X explicitly stop before actual Source 11 and
  FinalSummaryReport runtime.
- **Exact remaining gap:** No accepted internal result/report is tied to the
  governed record and shown through the Internal Alpha operator experience.
- **Prerequisites:** MVP-F12 accepted; provenance and warnings preserved.
- **Expected deliverables:** Backend internal result/report projection with audit
  lineage, then frontend continuity from review console to analysis/graph and
  result, including blocked/error/empty states.
- **Required validation:** Contract and focused tests, no production report
  object, frontend build, browser interaction smoke, provenance continuity,
  boundary visibility, and no publish/download/send control.
- **Approval class:** Controlled internal report projection and frontend operator
  integration.
- **Exact Prompt count:** 2.
- **Why fixed:** Internal Alpha requires a human-readable conclusion surface,
  not only backend dictionaries or graph payloads.
- **Completion evidence required:** Accepted backend health report and browser QA
  showing one governed internal result with review boundaries intact.
- **Does not authorize:** Source 11 production runtime, FinalSummaryReport
  production runtime, B-end customer report, export, download, public access,
  external delivery, or customer readiness.
- **Prompt packages:** `MVP-F13-P1` internal result/report projection and tests;
  `MVP-F13-P2` operator UI continuity, build, and browser QA.

### MVP-F14 - C-demo Final Continuity and Comprehension Regression

- **Completion purpose:** Confirm the C-demo remains understandable and separate
  from the governed B-core after final integration.
- **Current evidence:** Guided demo, Event Plaza, Helldivers and Dong/Sun detail,
  Sandbox, T0-T6, and sample report routes have browser evidence; one historical
  PeopleCluster prominence P2 note exists.
- **Exact remaining gap:** The final integrated repository has not received one
  end-state C-demo continuity and first-time comprehension check.
- **Prerequisites:** MVP-F13 complete; final route and copy set stable.
- **Expected deliverables:** Browser regression report for canonical routes,
  sample retention, module boundaries, safety copy, and C-demo/B-core distinction.
- **Required validation:** Desktop browser smoke, route/CTA checks, no sample
  cross-event substitution, no stale sample substitution, no silent selected
  event change, no unlabeled mock substitution, no console errors, no unsafe
  claims, and evaluator comprehension of PeopleCluster versus InfluenceCore.
- **Approval class:** Browser QA and report-only C-demo checkpoint.
- **Exact Prompt count:** 1.
- **Why fixed:** The frozen product shape includes an understandable C-demo.
- **Completion evidence required:** Accepted browser report with no P0/P1 and no
  unresolved endpoint-blocking P2.
- **Does not authorize:** New feature design, recording, public launch, live
  collection, or optional visual polish unless a conditional trigger fires.
- **Prompt package:** `MVP-F14-P1` final C-demo browser/comprehension regression.

Correctly selected and clearly labeled sample content is allowed. A clearly
labeled disabled/static fallback, empty state, or unavailable state is allowed
when it remains semantically correct. The selected event must never silently
change or display another event's content. The C-demo remains selected-sample
and is not converted into a live-data requirement.

```text
explicitly_labeled_selected_sample = allowed
explicitly_labeled_disabled_or_static_fallback = allowed_when_semantically_correct
cross_event_substitution = forbidden
silent_selected_event_change = forbidden
stale_sample_substitution = forbidden
unlabeled_mock_substitution = forbidden
```

### MVP-F15 - Local Operations, Cleanup, Pause, and Recovery Package

- **Completion purpose:** Make the complete local happy path reproducible without
  hidden state and document safe cleanup and failure handling.
- **Current evidence:** General local run commands and feature boundaries exist;
  the new nonproduction target and integrated B-core path have no unified
  operator package.
- **Exact remaining gap:** Startup, target enablement, reset, pause, ambiguity,
  cleanup, and state ownership are distributed across phase records.
- **Prerequisites:** MVP-F09 and MVP-F13 complete; final local paths stable.
- **Expected deliverables:** One operator runbook/checklist and a bounded local
  drill on a disposable non-authoritative rehearsal target covering startup,
  disabled defaults, state inventory, cleanup/reset, pause, recovery limits,
  bounded cleanup, and no-hidden-state proof.
- **Required validation:** Fresh local sequence, disabled-state checks,
  deterministic rehearsal-target reset, logical-label-only output, ignored
  runtime boundary, no protected-value exposure, no unrelated-state change,
  and proof that the authoritative governed record remains unchanged and
  available for MVP-F16.
- **Approval class:** Local operations documentation and controlled drill.
- **Exact Prompt count:** 1.
- **Why fixed:** Internal evaluators need a reproducible and recoverable local
  workflow, not historical command fragments.
- **Completion evidence required:** Accepted reproducible runbook and drill
  report proving the disposable rehearsal target can be cleaned safely,
  unrelated and authoritative state is untouched, and the authoritative record
  remains available for MVP-F16 evidence capture.
- **Does not authorize:** Production deployment, cloud infrastructure, backup
  service, multi-tenancy, real provider operation, or destructive unrelated
  cleanup. It also does not authorize cleanup of the authoritative governed
  record before or after MVP-F16.
- **Prompt package:** `MVP-F15-P1` operator package and local recovery drill.

```text
MVP-F15_cleanup_drill_target = disposable_temporary_rehearsal_target_only
authoritative_governed_record_cleanup_before_MVP_F16 = forbidden
authoritative_record_retention = retain_unchanged_through_MVP_F16_evidence_capture
```

### MVP-F16 - Final Integrated Internal Alpha Validation Package

- **Completion purpose:** Validate the frozen endpoint as one repository state
  after all implementation milestones are complete.
- **Current evidence:** Many focused phase validations exist, but 9A-23B did not
  run full pytest and no final governed-record end-to-end checkpoint exists.
- **Exact remaining gap:** No single accepted package proves backend, frontend,
  governance, privacy, and C-demo continuity together.
- **Prerequisites:** MVP-F01 through MVP-F15 complete; no known unresolved P1/P2.
- **Expected deliverables:** Final health report with focused suites, nearby
  regressions, full non-slow backend suite, offline benchmarks where applicable,
  frontend build, operator/C-demo browser smoke, controlled local end-to-end
  smoke, static scans, and Git checks.
- **Required validation:** Every command and exact result recorded; no real
  external call; no protected-value leak; no production object; no unsafe
  runtime capability; clean diff check.
- **Approval class:** Validation-only final checkpoint.
- **Exact Prompt count:** 1.
- **Why fixed:** Completion claims require integrated evidence, not the sum of
  historical focused reports.
- **Completion evidence required:** Accepted final validation report with all
  required checks passing or explicitly not applicable by the frozen DoD.
- **Does not authorize:** Scope repair, new feature implementation, production
  promotion, public delivery, or release tagging.
- **Prompt package:** `MVP-F16-P1` complete validation and health report.

### MVP-F17 - Internal Alpha Completion Decision and Source Synchronization

- **Completion purpose:** Reconcile completed milestones, Prompt accounting,
  remaining allowances, Git state, deferred scope, and the final human decision.
- **Current evidence:** The baseline defines the endpoint and Source maintenance
  plan; final implementation evidence will come from MVP-F16.
- **Exact remaining gap:** No final completion checkpoint or post-baseline Source
  synchronization can exist before all work passes.
- **Prerequisites:** MVP-F16 accepted; all fixed milestones completed or formally
  replaced; repository committed, pushed, and clean.
- **Expected deliverables:** Docs-only completion report, final budget ledger,
  deferred backlog confirmation, Canonical Source update recommendations, and
  explicit user completion decision request.
- **Required validation:** Milestone and arithmetic reconciliation, clean Git
  status, baseline/project/document commit references, no unresolved P1/P2, and
  no scope drift.
- **Approval class:** Docs-only completion and source-sync checkpoint.
- **Exact Prompt count:** 1.
- **Why fixed:** Internal Alpha is not complete until evidence, accounting,
  documentation, Git, and human acceptance agree.
- **Completion evidence required:** User-accepted completion decision and
  synchronized Canonical Source after the final commit.
- **Does not authorize:** Production v1, tag creation, public launch, production
  objects, live collection, or deferred backlog execution.
- **Prompt package:** `MVP-F17-P1` completion ledger and handoff.

## 7. Fixed Milestone Prompt Ledger

| Milestone | Title | Exact Prompt count | Prompt packages |
| --- | --- | ---: | --- |
| MVP-F01 | Independent 9A-23B Post-repair Conformance Audit | 1 | F01-P1 |
| MVP-F02 | Real Safe-payload Capture Readiness and Access Contract | 1 | F02-P1 |
| MVP-F03 | One Bounded Real Safe-payload Capture | 1 | F03-P1 |
| MVP-F04 | Independent Real Safe-payload Acceptance Audit | 1 | F04-P1 |
| MVP-F05 | Logical Nonproduction Target Authorization and Operations Contract | 1 | F05-P1 |
| MVP-F06 | Disabled-by-default Logical Target Initialization Smoke | 1 | F06-P1 |
| MVP-F07 | Exact Gate Activation Decision for Nonproduction Persistence | 1 | F07-P1 |
| MVP-F08 | Single Governed Nonproduction Persistence Execution | 1 | F08-P1 |
| MVP-F09 | Independent Post-write Integrity, Idempotency, and Recovery Audit | 1 | F09-P1 |
| MVP-F10 | Governed Record to Internal Review Console Integration | 2 | F10-P1, F10-P2 |
| MVP-F11 | Governed Record to Controlled Analysis Input Bridge | 2 | F11-P1, F11-P2 |
| MVP-F12 | Controlled Opinion Ecosystem and Dense Graph Execution | 1 | F12-P1 |
| MVP-F13 | Human-reviewable Internal Result/Report and Operator Continuity | 2 | F13-P1, F13-P2 |
| MVP-F14 | C-demo Final Continuity and Comprehension Regression | 1 | F14-P1 |
| MVP-F15 | Local Operations, Cleanup, Pause, and Recovery Package | 1 | F15-P1 |
| MVP-F16 | Final Integrated Internal Alpha Validation Package | 1 | F16-P1 |
| MVP-F17 | Internal Alpha Completion Decision and Source Synchronization | 1 | F17-P1 |
| **Total** | **17 fixed milestones** | **20** | **20 work packages** |

## 8. Conditional Milestones

### MVP-C01 - 9A-23B Audit Repair Allowance

- **Trigger:** MVP-F01 finds a narrow defect against the committed 9A-23A
  contract.
- **Maximum Prompt allowance:** 1.
- **Scope:** One synthetic-only in-scope conformance repair with focused tests,
  regressions, health report, and static validation.
- **Why not fixed:** The independent audit may pass without repair.
- **Expiry:** Expires when MVP-F01 is accepted with no defect or the one repair
  is accepted. A second repair requires risk-buffer classification or rebaseline.
- **Budget category:** Conditional allowance.

### MVP-C02 - Safe-payload Capture and Acceptance Remediation

- **Trigger:** MVP-F03 or MVP-F04 finds a correctable field, hash, lineage,
  custody, redaction, or protected-value defect inside the already approved
  one-candidate scope.
- **Maximum Prompt allowance:** 2.
- **Scope:** Narrow capture-procedure or safe-artifact repair and one independent
  recheck; no additional candidate and no broader source access.
- **Why not fixed:** A correctly captured payload needs no remediation.
- **Expiry:** Expires when MVP-F04 is accepted. Any need for another candidate,
  another source, or expanded row access requires rebaseline.
- **Budget category:** Conditional allowance.

### MVP-C03 - Logical Target or Persistence Compatibility Repair

- **Trigger:** MVP-F06, MVP-F08, or MVP-F09 identifies a narrow local path,
  schema initialization, SQLite compatibility, idempotency, receipt, integrity,
  or cleanup defect inside the selected nonproduction target contract.
- **Maximum Prompt allowance:** 2.
- **Scope:** One narrow implementation repair and one independent acceptance or
  compatibility recheck; no generic store and no production target.
- **Why not fixed:** Synthetic tests and the existing implementation may work on
  the logical target without modification.
- **Expiry:** Expires when MVP-F09 is accepted. Target replacement, schema-family
  expansion, or additional mutation semantics requires rebaseline.
- **Budget category:** Conditional allowance.

### MVP-C04 - Review, Analysis, or Result Integration Repair

- **Trigger:** MVP-F10 through MVP-F13 expose an in-scope contract mismatch,
  safe projection defect, disabled-route regression, analysis binding defect,
  result lineage gap, or required browser-visible error.
- **Maximum Prompt allowance:** 2.
- **Scope:** Narrow backend or frontend compatibility repair within the frozen
  review-to-result path, including focused validation.
- **Why not fixed:** Existing helpers and UI may integrate without additional
  repair beyond the fixed implementation packages.
- **Expiry:** Expires when MVP-F13 is accepted. A new feature or production
  object is not eligible.
- **Budget category:** Conditional allowance.

### MVP-C05 - Final Validation Regression Repair

- **Trigger:** MVP-F16 finds an in-scope regression after the contributing
  milestone was previously accepted.
- **Maximum Prompt allowance:** 2.
- **Scope:** Narrow repair of the failing fixed requirement plus rerun of the
  failed final checks.
- **Why not fixed:** The final suite may pass on the first run.
- **Expiry:** Expires when MVP-F16 passes. A material architectural or endpoint
  change requires rebaseline.
- **Budget category:** Conditional allowance.

### MVP-C06 - C-demo Comprehension Polish

- **Trigger:** MVP-F14 shows that a first-time evaluator still cannot distinguish
  PeopleCluster from InfluenceCore, misses mandatory boundary labels, or cannot
  follow the canonical selected-sample route.
- **Maximum Prompt allowance:** 1.
- **Scope:** Small explanatory copy, layout, or visual hierarchy correction plus
  targeted build/browser recheck; no new product capability.
- **Why not fixed:** The current demo is usable and the known issue is P2 only.
- **Expiry:** Expires when MVP-F14 passes without the trigger or after the one
  accepted polish task.
- **Budget category:** Conditional allowance.

## 9. Conditional Allowance Ledger

| Conditional ID | Trigger summary | Maximum Prompt allowance |
| --- | --- | ---: |
| MVP-C01 | F01 finds a narrow 9A-23B conformance defect | 1 |
| MVP-C02 | Safe-payload capture or audit needs bounded remediation | 2 |
| MVP-C03 | Selected nonproduction target/persistence needs compatibility repair | 2 |
| MVP-C04 | Review-to-result integration exposes an in-scope defect | 2 |
| MVP-C05 | Final integrated validation finds an in-scope regression | 2 |
| MVP-C06 | Final C-demo comprehension check triggers narrow polish | 1 |
| **Total** | **6 conditional milestones** | **10** |

Only one category pays for a finding. A defect discovered during F10-F13 uses
MVP-C04; the same already-accepted area failing later in final integration uses
MVP-C05. Conditional allowance is a ceiling, not a pre-authorization.

## 10. Risk-buffer Policy

`risk_buffer_prompt_allowance = 4`

The four single-Prompt reserve units cover unforeseen work that remains inside
the frozen DoD and does not match an explicit conditional trigger. They may be
used only for:

- an unexpected `needs_fix` inside an existing fixed milestone;
- a missing test or safety check discovered while completing a fixed milestone;
- a narrow compatibility repair required by a fixed MVP requirement;
- a post-audit repair that does not expand the endpoint.

They may not fund:

- a new product feature;
- Production v1 work;
- public or external delivery;
- a new provider or platform;
- commercial SaaS capability;
- unrelated architecture expansion;
- optional polish;
- another real candidate or broader data access.

Each consumption event requires a change record before the task starts. The
buffer is not a list of authorized tasks. If all four units are consumed, the
workflow pauses and rebaselines before another unplanned task starts.

## 11. Exact Budget Arithmetic

### 11.1 Fixed budget

```text
MVP-F01..MVP-F09 = 9 prompts
MVP-F10 = 2 prompts
MVP-F11 = 2 prompts
MVP-F12 = 1 prompt
MVP-F13 = 2 prompts
MVP-F14 = 1 prompt
MVP-F15 = 1 prompt
MVP-F16 = 1 prompt
MVP-F17 = 1 prompt
fixed_remaining_prompt_budget = 9 + 2 + 2 + 1 + 2 + 1 + 1 + 1 + 1 = 20
```

### 11.2 Conditional allowance

```text
conditional_prompt_allowance = 1 + 2 + 2 + 2 + 2 + 1 = 10
```

### 11.3 Ceilings

```text
best_case_remaining_prompts = fixed_remaining_prompt_budget = 20
controlled_ceiling_remaining_prompts = fixed_remaining_prompt_budget + conditional_prompt_allowance = 20 + 10 = 30
hard_ceiling_without_rebaseline = fixed_remaining_prompt_budget + conditional_prompt_allowance + risk_buffer_prompt_allowance = 20 + 10 + 4 = 34
```

The planning Prompt and consumed planning-correction Prompt are outside these
three engineering figures. The correction consumed one of one and leaves zero;
engineering consumption remains zero. These are Prompt counts, not days, hours,
or delivery-time guarantees.

## 12. Critical Path and Dependencies

```text
MVP-F01
  -> MVP-F02 -> MVP-F03 -> MVP-F04
  -> MVP-F05 -> MVP-F06 -> MVP-F07 -> MVP-F08 -> MVP-F09
  -> MVP-F10 -> MVP-F11 -> MVP-F12 -> MVP-F13
  -> MVP-F14
  -> MVP-F16 -> MVP-F17

MVP-F09 -> MVP-F15 -> MVP-F16
```

Rules:

- MVP-F01 is always first.
- F02-F04 keep readiness, one real capture, and independent acceptance separate.
- F05-F09 keep target authorization, initialization, activation, one mutation,
  and independent post-write audit separate.
- F09 is strictly read-only and leaves the authoritative record and attempt
  ledger unchanged.
- F10-F13 connect review, controlled analysis, graph, internal result, and UI
  only after persistence is accepted.
- F10 visibility is not acceptance. F11-P1 defines the acceptance contract;
  F11-P2 and F12 require a matching accepted reference.
- F14 and F15 must both complete before final validation.
- F15 rehearses cleanup only on a disposable non-authoritative target and must
  retain the authoritative governed record unchanged through F16 capture.
- F16 validates; it does not repair.
- F17 accounts and requests the final human decision; it does not declare
  completion automatically.

## 13. Change-control Classifications

Every newly proposed task after baseline effectiveness must be classified as
exactly one of:

- `planned_fixed_milestone`;
- `conditional_milestone_triggered`;
- `risk_buffer_consumption`;
- `replacement_of_existing_milestone`;
- `deferred_to_v1_1_or_production_v1`;
- `formal_scope_expansion_requiring_rebaseline`.

No task may silently enter the critical path. A listed Prompt count does not
authorize its task, and an approval for one milestone cannot be reused by
another.

## 14. Change-record Template

Each change-control event must record:

```text
change_id = unique baseline-local ID
date_or_checkpoint = Git or task checkpoint
originating_finding = concise evidence-backed finding
affected_milestone = one fixed or conditional ID, or baseline-wide
old_prompt_budget = integer
added_or_removed_prompt_count = signed integer
new_prompt_budget = integer
classification = one allowed change-control classification
user_approval_required = yes/no
baseline_version_changes = yes/no
evidence_refs = tracked paths or accepted task receipts
scope_boundary = explicit inclusions and exclusions
```

A replacement must identify the replaced milestone, preserve or improve its DoD
coverage, and show the net Prompt change. Cancellation without equivalent DoD
coverage requires rebaseline.

## 15. Re-baselining Triggers

A new baseline version is mandatory when:

- the Definition of Done changes materially;
- the endpoint expands beyond Internal Alpha / MVP v1;
- a new fixed capability enters the endpoint;
- the fixed Prompt budget increases for a reason not covered by conditional or
  risk allowance;
- the hard ceiling of 34 would be exceeded;
- a deferred Production v1 capability moves into the MVP;
- another candidate, source, or broader real-data access becomes required;
- production `EvidenceItem`, production case, production `analysis_run`,
  production Analysis Result, Source 11 runtime, FinalSummaryReport runtime, or
  public delivery becomes mandatory;
- the baseline project-state anchor or source-of-truth model changes materially;
- a fixed milestone must be removed without an accepted equivalent.

Use v1.0 to v1.1 for an in-scope material revision. Use v2.0 for an endpoint or
product-scope change.

## 16. Consumption and Remaining-budget Rules

After a task starts:

1. Record its baseline classification.
2. Decrement one Prompt from the matching fixed package, conditional ceiling,
   or risk buffer.
3. Record the task outcome even if `blocked` or `needs_fix`.
4. Keep the milestone incomplete until all packages and completion evidence pass.
5. Do not move unused allowance between categories.

At any checkpoint:

```text
remaining_fixed_prompts = 20 - consumed_fixed_prompts
remaining_conditional_allowance = 10 - consumed_conditional_prompts
remaining_risk_buffer = 4 - consumed_risk_prompts
```

If a fixed task is replaced, its unstarted packages may be removed only through
a change record. A started failed task remains consumed. If a conditional task
hits its maximum without closure, pause and classify the next proposal as risk
buffer or rebaseline before starting it.

## 17. Completion Accounting

Internal Alpha / MVP v1 is complete only when:

- all 17 fixed milestones are completed or formally replaced;
- all 20 fixed Prompt packages have accepted completion evidence, unless a
  documented replacement changes the count;
- no unresolved endpoint P1/P2 remains;
- MVP-F16 passes;
- the repository is clean and pushed;
- Canonical Source is synchronized;
- Production v1 scope remains deferred;
- the user makes the final human completion decision.

The fixed budget reaching zero is not completion by itself. Completion may occur
with unused conditional or risk allowance, which then expires.

## 18. Deferred Backlog Boundary

The following does not consume this budget unless a formal rebaseline moves it
inside the endpoint:

- production evidence, Review Queue, case, analysis, result, Source 11, or
  FinalSummaryReport runtime;
- public report, export, download, signed link, delivery, portal, or customer UI;
- additional real candidates, platforms, providers, or collector jobs;
- real LLM or automated response behavior;
- multi-tenancy, billing, production authorization, cloud deployment, HA, or
  full observability;
- recording, website, pitch, promotional assets, or optional visual polish;
- broad model recalibration, new scoring systems, or all-web claims.

## 19. First Next Engineering Task

The only recommended next engineering boundary is:

`MVP-F01 - Independent 9A-23B Post-repair Conformance Audit`

It is one Prompt, independently approved, synthetic-only, and read-only or
docs-only unless a later repair is separately approved. This document neither
executes it nor supplies future authorization text.

## 20. Git and Source Maintenance

After the two baseline documents are independently reviewed, committed, and
pushed:

- record the baseline-document commit from Git history;
- replace Canonical 00 with baseline version, project-state anchor,
  baseline-document commit, fixed budget 20, conditional allowance 10, risk
  buffer 4, hard ceiling 34, and MVP-F01;
- update Canonical 09 narrowly to record that the baseline is established, the
  9A mainline is preserved, and MVP-F01 remains first;
- do not update Canonical 03 because runtime behavior did not change;
- do not update Canonical 05 unless the collaboration protocol itself changes;
- do not update Source 11.

Recommended baseline commit message:

`Establish Internal Alpha MVP completion baseline`

No tag is recommended.

## 21. No-authorization and No-side-effect Statement

This ledger does not approve any future task. It creates no future approval
text, performs no test/build/runtime/database/package/row/network action, and
does not authorize safe-payload capture, target access, gate activation,
nonproduction mutation, production Evidence Layer write, production
`EvidenceItem`, production case, production `analysis_run`, production Analysis
Result, Source 11 runtime, FinalSummaryReport runtime, public output, or delivery.
