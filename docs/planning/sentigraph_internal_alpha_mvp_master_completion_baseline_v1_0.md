# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.0

## 1. Purpose

This document freezes one evidence-based completion endpoint for Sentigraph
Internal Alpha / MVP v1. It defines what must be true before the endpoint may
be accepted, distinguishes current implementation from historical boundary
objects, and prevents Production v1 scope from silently entering the MVP.

This is a planning and accounting contract. It does not authorize any listed
milestone or change current runtime behavior.

## 2. Baseline Summary

```text
baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_0
baseline_version = 1.0
baseline_scope = internal_alpha_mvp_v1
baseline_status = candidate_ready_for_commit
baseline_project_state_anchor = e3fb9f9249069fc72b23dd3bd5b6e197d1417f7c
baseline_project_state_message = Repair 9A-23B synthetic persistence conformance
baseline_effective_when = both baseline documents are committed and pushed to Git main, the worktree is clean, and ChatGPT records the baseline-document commit
baseline_planning_correction_prompts_consumed = 1
baseline_planning_correction_prompts_remaining = 0
consumed_engineering_prompts_since_baseline = 0
product_shape = B-core + C-demo
current_9a_engineering_mainline_preserved = yes
first_fixed_remaining_milestone = independent_9a23b_post_repair_conformance_audit
real_safe_payload_authorized = no
logical_runtime_target_authorized = no
gate_activation_authorized = no
actual_write_authorized = no
production_evidenceitem_authorized = no
```

The baseline is not effective while it is only an uncommitted candidate.

The one Baseline v1.0 planning-correction Prompt was consumed by the narrow
pre-commit correction that clarified audit/cleanup ownership, sample fallback
semantics, review acceptance binding, and source precedence. It is outside the
engineering budget, cannot be transferred, and leaves no second v1.0 planning
correction Prompt. Another pre-commit material defect requires pause and a new
planning decision rather than conditional or risk-buffer consumption.

## 3. Baseline Anchors

### 3.1 Project-state anchor

`baseline_project_state_anchor` is fixed at commit `e3fb9f9`, whose full SHA is
recorded above. The inspected branch was `main`, it matched `origin/main`, and
the starting worktree was clean.

This anchor identifies the engineering state inspected to create the baseline.
It is not changed by later documentation commits.

### 3.2 Baseline-document commit

`baseline_document_commit` means the future Git commit that adds both baseline
documents. That commit is identified authoritatively by Git history after the
user commits and pushes it. A Git commit cannot reliably embed its own future
SHA, so no SHA is guessed here.

After that commit is pushed, ChatGPT must record its exact SHA in Canonical
Source and in the main-task handoff. The absence of a self-embedded future SHA
is intentional and is not a design gap.

## 4. Current Verified Project State

At the project-state anchor:

- 9A-23B is committed and reports a ready synthetic exact-conformance repair.
- Command v0.2, receipt v0.2, durable attempt reservation, one-attempt
  enforcement, strict binding, idempotent replay, ambiguity pause behavior,
  and temporary-SQLite validation exist.
- The independent 9A-23B post-repair conformance audit is not complete.
- One exact candidate identity is locked by committed governance records. This
  baseline intentionally does not reproduce its ID, hash, package name, row,
  or source content.
- A full real safe payload has not been captured.
- The logical nonproduction runtime target has not been accessed or initialized.
- The execution gate is inactive and no activation decision exists for this
  endpoint.
- No governed real-candidate nonproduction persistence has occurred.
- No production `EvidenceItem`, production Review Queue item, production case,
  production `analysis_run`, or production Analysis Result has been created.
- The Internal Alpha review console has a tested static shell and consumes an
  existing disabled-by-default GET route safely, but it shows synthetic or
  fallback metadata rather than the future governed persisted record.
- Local fixture generated runs, Opinion Ecosystem modules, dense graph helpers,
  selected public sample pages, and sample report pages are implemented and
  have focused build/browser evidence.
- 8V, 8X, and 8Y prove local controlled boundary chains only. Their candidate,
  handoff, report, Source 11, export, delivery, case, analysis, and result shapes
  are not production runtime records.
- 8Z proves a disabled-by-default safe review-console shell and route-consumption
  behavior, not an active operator runtime over real governed state.
- The C-demo is usable with no known P0/P1 issue. A historical P2 note remains
  about PeopleCluster visual prominence and is conditional, not automatically
  a fixed feature request.

## 5. Product Shape

`product_shape = B-core + C-demo`

### 5.1 B-core

The B-core is a local, internal, human-reviewed workflow for one bounded
real-source candidate. It must demonstrate exact governance, safe nonproduction
persistence, review/audit visibility, deterministic internal analysis, a dense
graph where applicable, and a human-reviewable internal result/report.

### 5.2 C-demo

The C-demo is the existing selected-public-sample experience: guided demo,
Event Plaza, public event details, Opinion Ecosystem sandbox, historical T0-T6
replay, and sample reports. It explains the product without claiming live
collection, full-web coverage, official verification, causal proof, or
production analysis.

The B-core and C-demo may share concepts and components, but the C-demo must not
be presented as proof that the bounded real-source B-core has executed.

## 6. Exact Internal Alpha / MVP Endpoint

Sentigraph Internal Alpha / MVP v1 is complete only when a local internal
operator can, under separate approvals, take exactly one approved bounded
real-source candidate through this chain:

```text
approved locked candidate
-> governed safe-payload capture
-> independent identity, lineage, privacy, and hash acceptance
-> explicitly authorized dedicated local nonproduction target
-> explicitly activated one-attempt persistence gate
-> exactly one governed nonproduction persisted record and safe receipt
-> read-only human review and audit visibility
-> controlled deterministic analysis and dense-graph interpretation
-> human-reviewable internal result/report
-> final local recovery and end-to-end validation evidence
```

The endpoint also retains an understandable selected-sample C-demo. The endpoint
does not require a production `EvidenceItem`, production case, production
`analysis_run`, production Analysis Result, Source 11 runtime, production
FinalSummaryReport, public export, external delivery, or live all-platform
collector.

## 7. Definition of Done

### A. Scope and governance

Completion requires all of the following:

1. The versioned Internal Alpha scope and this B-core + C-demo endpoint remain
   explicit.
2. Human review remains required at every governed decision point.
3. Automatic trust upgrade remains prohibited.
4. Candidate, row, package, role, schema, opaque ID, safe hash, payload, gate,
   activation, and target substitution fail closed.
5. Internal nonproduction objects are visibly distinct from production objects.
6. Provider output and selected public samples remain evidence, not truth.
7. Deferred Production v1 scope remains outside the MVP critical path.

### B. One bounded real-source evidence path

Completion requires:

1. One separately approved real-source candidate only.
2. One governed safe payload with a strict field allowlist and no raw row,
   raw comment, raw identity, profile, private content, credential value, or
   physical path.
3. Exact identity, lineage, schema, hash, gate, activation, and target binding.
4. A dedicated local nonproduction persistence target that is ignored by Git,
   disabled by default, and isolated from generic case persistence.
5. Durable one-attempt enforcement, no automatic mutation retry, conflict
   blocking, and zero-mutation idempotent replay.
6. Exactly-one-record post-write verification and a safe receipt.
7. No silent fallback to another candidate, row, package, source, or target.
8. No production `EvidenceItem` requirement.

### C. Review and audit

The internal review path must display or prove:

- source and provenance status;
- review status, warning count, blocker count, and coverage limitations;
- `human_review_required = true`;
- `no_automatic_trust_upgrade = true`;
- identity/lineage binding without exposing protected values;
- receipt and audit references;
- duplicate, conflict, idempotency, and attempt state;
- pause, failure, and revocation/cleanup state;
- no production object or downstream side effect.

The review path must be read-only. It may use the existing Internal Alpha review
console route and UI after they are connected to the governed nonproduction
record through a safe metadata projection.

Review visibility is not review acceptance. MVP-F10 may show the record,
warnings, blockers, and receipt, but it must not create or imply a human
acceptance decision. Before MVP-F11-P2 or MVP-F12 may build or execute governed
analysis input, a separately governed, versioned
`human_review_acceptance_reference` must exist and bind at minimum:

- the exact persisted record ID or safe record reference;
- the exact persistence receipt reference;
- the candidate identity digest or equivalent safe identity binding;
- the accepted canonical record hash or safe record hash;
- warning count and blocker count;
- the narrow review decision;
- a bounded reviewer label or reviewer-role label;
- `reviewed_at`;
- human-review-required and no-automatic-trust-upgrade acknowledgments;
- acceptance schema, version, and safe hash.

The review decision must be limited to
`accepted_for_controlled_nonproduction_analysis` or an equally narrow
nonproduction decision. It is not truth verification, official verification,
trust upgrade, production promotion, production `EvidenceItem` approval, or
public-output approval. Missing, rejected, or mismatched acceptance blocks the
analysis bridge. Listing this requirement does not pre-authorize the future
human decision.

### D. Controlled analysis

Completion requires one deterministic internal analysis path over the governed
record or its strictly derived safe projection. The bounded real-source demo
must not silently fall back to a mock sample.

The path requires an accepted `human_review_acceptance_reference` that matches
the exact record, receipt, identity binding, accepted record hash, warning
count, and blocker count. Acceptance validation must not mutate evidence,
upgrade trust, or create a production object.

The minimum analysis path must:

- create a nonproduction internal analysis context, not a production case or
  production `analysis_run`;
- reuse the tested local calculator and generated-run contracts where safe;
- expose ContentAggregate, InfluenceCore, EchoBox, PeopleCluster, and
  ResponseStrategyComparisonV01 outputs when input is valid;
- attach or derive a dense graph where applicable;
- preserve uncertainty, selected-sample, human-review, and coverage labels;
- avoid prediction, official-verification, causal-proof, truth-score, or
  production-score claims;
- produce no public response text and perform no automatic action.

### E. Internal result or report

Completion requires one human-reviewable internal result/report derived from
the governed analysis path. It may reuse controlled report-boundary helpers,
but must have explicit provenance back to the persisted record and analysis
receipt.

It must not require or imply:

- production Source 11 runtime;
- production FinalSummaryReport runtime;
- public or signed download URLs;
- customer portal publication;
- external delivery;
- B-end customer report production;
- public Sandbox or public event generation.

### F. Internal operator experience and C-demo

An internal evaluator must be able to:

1. Open the Internal Alpha review console and distinguish disabled, empty,
   blocked, error, fallback, and governed-ready states.
2. Inspect safe evidence/review state, warnings, blockers, audit references,
   and no-trust-upgrade boundaries.
3. Start or inspect the controlled internal analysis only through an explicit
   local action that cannot mutate evidence or publish output.
4. Follow continuity from review to analysis, dense graph, and internal result.
5. Open the C-demo routes and understand that they use selected public samples.
6. Distinguish PeopleCluster anonymous aggregate proxies from InfluenceCore
   narrative/content/media cores.
7. See no `[object Object]`, `undefined`, `NaN`, obvious 500, or unsafe action
   control on the final paths.

The C-demo permits correctly selected and clearly labeled sample content. A
disabled internal surface may preserve an explicitly labeled static fallback,
empty state, or unavailable state when it is semantically correct. It must not
silently change the selected event, retain a stale prior sample, substitute an
unlabeled mock, or display one event as another.

```text
explicitly_labeled_selected_sample = allowed
explicitly_labeled_disabled_or_static_fallback = allowed_when_semantically_correct
cross_event_substitution = forbidden
silent_selected_event_change = forbidden
stale_sample_substitution = forbidden
unlabeled_mock_substitution = forbidden
```

The known PeopleCluster prominence issue becomes required work only if the
final C-demo validation shows that a first-time evaluator still cannot make the
distinction. Decorative polish, recording, and promotional assets are not DoD.

### G. Local operation and recovery

Completion requires evidence-based operator documentation and a local drill for:

- clean backend and frontend startup;
- explicit disabled-by-default feature behavior;
- safe configuration without exposing protected values;
- creation and use of only the selected nonproduction target;
- deterministic cleanup/reset of nonproduction state;
- pause behavior after ambiguity or conflict;
- recovery and revocation limitations;
- no hidden local state required by the documented happy path;
- no production deployment, cloud, tenancy, or availability dependency.

MVP-F09 is a strictly read-only audit. It may inspect record/reservation
integrity, exactly-one state, read-only idempotent replay, pause behavior,
receipt truthfulness, recovery limitations, and cleanup/revocation procedure
design. It must not delete, reset, revoke, repair, update, replace, recreate, or
otherwise mutate the authoritative record or attempt ledger, and it must not
execute the cleanup/reset drill.

MVP-F15 owns procedure documentation and the controlled cleanup/reset rehearsal.
Its destructive rehearsal must use a disposable temporary or otherwise
explicitly isolated non-authoritative target. The authoritative governed MVP
record must remain unchanged and available through MVP-F16 evidence capture.
Listing F15 does not authorize final or post-completion cleanup of that record.

```text
MVP-F09_audit_mode = strictly_read_only
MVP-F09_actual_cleanup_execution = no
MVP-F09_actual_reset_execution = no
MVP-F09_mutation_allowed = no
MVP-F15_cleanup_drill_target = disposable_temporary_rehearsal_target_only
authoritative_governed_record_cleanup_before_MVP_F16 = forbidden
authoritative_record_retention = retain_unchanged_through_MVP_F16_evidence_capture
```

### H. Validation and completion checkpoint

The final checkpoint must include:

- focused tests for every final fixed milestone;
- nearby governance and compatibility regressions;
- the full non-slow backend suite;
- offline benchmark validation where applicable;
- frontend build;
- browser smoke for the final operator and C-demo paths;
- a controlled local end-to-end Internal Alpha smoke;
- privacy, protected-value, forbidden-integration, and unsafe-claim scans;
- Git diff checks and a clean pushed worktree;
- synchronized current-state and Canonical Source records;
- a final human completion decision.

Prompt budget exhaustion alone does not prove completion. Unused conditional or
risk allowance does not block completion and expires after final acceptance.

## 8. Included Scope

- One locked and separately approved bounded real-source candidate.
- One strict safe-payload capture and independent acceptance.
- One dedicated local nonproduction persistence target.
- One separately governed activation decision and at most one mutating attempt.
- One persisted nonproduction record, safe receipt, idempotency proof, and audit.
- Read-only operator review through safe metadata.
- Deterministic internal analysis and dense graph over governed input.
- One internal human-reviewable result/report.
- Existing selected-public-sample C-demo routes and boundary copy.
- Local startup, cleanup, pause, recovery, and validation documentation.
- Final full regression, build, browser, and end-to-end checkpoint.

## 9. Deferred Scope

The following is deferred to v1.1, Production v1, or an explicit rebaseline:

- production `EvidenceItem`, Review Queue item, case, `analysis_run`, or
  Analysis Result creation;
- production Source 11 or FinalSummaryReport runtime;
- B-end customer report generation;
- public Sandbox or public event runtime generation;
- export, binary package, download, signed URL, public access, email, portal,
  or external delivery runtime;
- live all-platform collection or unrestricted provider expansion;
- production account, cookie, session, proxy, or anti-bot systems;
- real LLM integration or automated public response execution;
- billing, subscriptions, multi-tenancy, organization authorization, and
  customer onboarding;
- cloud production deployment, high availability, and a full observability
  platform;
- a complete B-end customer portal or operations administration suite;
- recording, promotional video, website, pitch, and ICP work as engineering
  completion dependencies;
- broad algorithm recalibration or empirical production scoring.

## 10. Capability Classification

Each capability is assigned exactly one baseline classification.

| Capability | Classification | Tracked evidence | Baseline interpretation |
| --- | --- | --- | --- |
| Explicit safety and product boundaries | `complete_for_internal_alpha_mvp` | `AGENTS.md`, `README.md`, architecture and planning records | Boundary language and mock/offline defaults are established; final regression still checks preservation. |
| Selected-sample C-demo routes and reports | `complete_but_requires_final_regression` | `frontend/src/App.jsx`, public event, sandbox, report pages, 8S-13 and 8U-8A health reports | Usable demo exists; it remains selected-sample only. |
| Local generated-run calculator contract | `complete_but_requires_final_regression` | `opinion_ecosystem_minimum_real_run.py` and tests; 8S-13 health report | Deterministic fixture path is implemented; governed real-source input is not connected. |
| Dense graph builder and generated-run adapters | `complete_but_requires_final_regression` | dense graph services/tests and 8U/8V health reports | Controlled local graph path exists; it is not yet driven by the future governed record. |
| Analysis Request governance spine | `complete_but_requires_final_regression` | `analysis_request_store.py`, routes, schemas, golden tests | Broad local governance records exist; they do not create production evidence or production analysis objects. |
| 8V/8X/8Y candidate, report, and delivery chains | `historical_boundary_only` | 8V-25, 8X-17, and 8Y-21 decisions | Stage-complete controlled object chains are reusable evidence, not runtime completion. |
| Exact single-candidate identity governance | `complete_but_requires_final_regression` | 9A-16C through 9A-20 committed records | One identity is locked; the baseline does not expose it or treat it as payload/write permission. |
| 9A-23B synthetic persistence surface | `partial_fixed_remaining` | persistence service/test, 9A-23A contract, 9A-23B health report | Synthetic implementation exists; independent audit and real target path remain. |
| Real safe-payload capture | `blocked_pending_governance` | 9A-22 contract and 9A-23B limitations | Schema is designed, but no real safe payload exists and no access is authorized now. |
| Logical target, activation, and governed persistence | `blocked_pending_governance` | 9A-20 through 9A-23B | Target is selected logically and code exists, but target access, activation, and mutation remain unapproved. |
| Internal Alpha review console | `partial_fixed_remaining` | 8Z-20 through 8Z-32, backend route, frontend page | Static/synthetic disabled-route behavior is complete; governed persisted metadata is not connected. |
| Governed evidence to controlled analysis | `partial_fixed_remaining` | 8V/8X helpers and minimum-real-run services | Existing pieces are reusable, but no accepted bridge from the governed record exists. |
| Internal result/report over governed evidence | `partial_fixed_remaining` | controlled report/final-boundary helpers and 8V/8X records | Boundary shapes exist; governed nonproduction result continuity and UI remain. |
| Local operation, cleanup, pause, and recovery package | `partial_fixed_remaining` | current run docs plus 9A persistence limitations | General local commands exist; the new target and final happy path need one coherent operator contract and drill. |
| Final repository-wide Internal Alpha validation | `partial_fixed_remaining` | milestone health reports | Focused evidence exists, but the final integrated non-slow/build/browser/end-to-end checkpoint does not. |
| PeopleCluster first-time readability | `partial_conditional` | 8U-8A browser report | One nonblocking P2 note exists; work triggers only if final evaluator comprehension fails. |
| Production evidence, cases, analysis objects, Source 11, final report, and delivery | `deferred_production_v1` | repeated 8V/8X/8Y/9A pause records | These are intentionally not required for Internal Alpha. |
| Live all-platform collection, real LLM, SaaS, billing, tenancy, and HA | `deferred_production_v1` | `README.md`, provider and platform boundaries | Not required for this endpoint. |
| Legacy optional real-API demo paths | `out_of_scope` | `README.md` and existing adapters | They are not selected as proof of the bounded B-core path and are not expanded by this baseline. |
| Recording, website, pitch, and promotional assets | `out_of_scope` | 8S-16-NR decision | Presentation work is not an engineering completion dependency. |

## 11. Mandatory Governance Boundaries

- A milestone listing is not an approval.
- A Prompt budget is not blanket authorization.
- Every later Codex task requires its own exact user approval under the existing
  Sentigraph protocol.
- Real package or row access, safe-payload capture, target authorization, target
  initialization, gate activation, nonproduction mutation, and post-write audit
  remain separate high-risk boundaries.
- No future approval text or ready-to-use declaration is supplied here.
- No historical authorization is silently widened to this baseline endpoint.
- A mismatch in candidate, row, package, role, schema, ID, hash, payload, gate,
  activation, or target stops the path.
- Ambiguous commit permits read-only verification only and never a second insert.
- Human review and no automatic trust upgrade remain invariant.
- Selected public sample output is not full-web coverage, full-platform coverage,
  official verification, causal proof, prediction, or production score.

## 12. MVP Completion Rule

Internal Alpha / MVP v1 may be declared complete only when:

1. Every fixed milestone in the companion budget document is completed or
   formally replaced by an accepted equivalent.
2. No unresolved P1 or P2 blocker remains inside the frozen endpoint.
3. Every required final validation passes.
4. The repository is clean, committed, and pushed.
5. Current-state documentation and Canonical Source are synchronized.
6. Deferred Production v1 capabilities remain visibly deferred.
7. The user makes the final human completion decision.

An exhausted budget does not waive any item. A passed milestone does not approve
the next milestone.

## 13. First Fixed Remaining Milestone

The first fixed milestone is `MVP-F01`, Independent 9A-23B Post-repair
Conformance Audit. Its Prompt count is exactly 1.

It must independently compare commit `e3fb9f9` with the committed 9A-23A
exact-conformance repair contract. It remains synthetic-only and read-only or
docs-only unless a later repair is separately authorized. It must not access a
real payload, logical runtime target, gate activation, actual mutation, or
production `EvidenceItem`.

The companion document defines all remaining milestones and accounting.

## 14. Relationship to the 9A Mainline

`current_9a_engineering_mainline_preserved = yes`

The baseline does not renumber or restart the 9A chain. Stable baseline IDs
provide completion accounting while later engineering tasks may retain their
own phase labels. The baseline also does not reactivate paused 8W, 8X, 8Y, or 8Z
production boundaries.

## 15. Source-of-truth Precedence

When sources disagree, use this order:

1. Current explicit user instruction and exact current approval scope.
2. Latest committed repository code, tests, docs, health reports, and Git state.
3. Latest main-chat handoff.
4. Committed Master Completion Baseline documents for the frozen MVP endpoint,
   milestone accounting, and change control.
5. Current Canonical Project Source summary.
6. Older historical planning records and archived Sources.

Code and tests define executable behavior. Accepted health reports define the
validation evidence recorded at their commit. Baseline documents define the
frozen endpoint, Prompt accounting, and change control. Git history identifies
authoritative commits, while Canonical Source summarizes stable committed state.

Planning text cannot upgrade a candidate, boundary object, fixture, helper,
disabled route, or static UI into runtime capability. A newer explicit
instruction does not silently widen an older approval. A scope-changing
instruction still requires exact approval and, when applicable, rebaselining.

## 16. Baseline Lifecycle and Versioning

- Candidate: both files exist locally but are not yet effective.
- Effective v1.0: both files are committed and pushed to `main`, the worktree is
  clean, and ChatGPT records the baseline-document commit.
- In-scope material revision: increment v1.0 to v1.1.
- Endpoint or product-scope change: create v2.0.
- Completion: all fixed milestones and DoD conditions are accepted by the user.
- Expiry: unused conditional and risk allowance expires on completion.

The companion document contains the exact change-control and rebaseline rules.

## 17. No-side-effect State

Creation of this baseline performed no engineering implementation, test run,
build, browser or API smoke, runtime access, SQLite access, package or row read,
real safe-payload capture, target initialization, gate activation, mutation,
production object creation, provider or collector job, network call, model
call, commit, push, tag, or Project Source update.

This narrow correction consumed one planning-correction Prompt and zero
engineering Prompts. It performed no engineering or runtime action and leaves
`baseline_status = candidate_ready_for_commit`.
