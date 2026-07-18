# Sentigraph Internal Alpha / MVP Master Completion Baseline v1.9

This document establishes the governance-only Baseline v1.9 after the ENV-R2 and ENV-R2-R1 pre-protected helper-audit blockers and before fixed-helper ENV-R2-R2. It records accepted state, historical accounting, blocked outcomes, future static-safety requirements, milestone selection, and authority boundaries only.

## 1. Decision and docs-only scope

- Decision = ready
- privacy_issue_stop = no
- docs_only = yes
- read_only_committed_repository_audit = yes
- implementation_performed = no
- helper_or_auditor_package_created = no
- auditor_self_test_performed = no
- local_discovery_performed = no
- environment_or_registry_access_performed = no
- runtime_action_performed = no

Baseline v1.9 is a governance-only rebaseline after the ENV-R2 and ENV-R2-R1 pre-protected helper-audit blockers and before fixed-helper ENV-R2-R2.

## 2. Baseline identity, approval and Goal

- baseline_name = sentigraph_internal_alpha_mvp_master_completion_baseline_v1_9
- baseline_version = 1.9
- baseline_scope = post_ENV_R2_and_ENV_R2_R1_pre_protected_helper_audit_blockers_pre_fixed_helper_ENV_R2_R2_governance
- baseline_project_state_anchor = 998e5f3ca25ddd6f270a35d59ab24e281917401c
- baseline_status = candidate_effective_pending_independent_ChatGPT_acceptance
- exact approval SHA-256 = 34a177a36b111d61991d9bfca7f418fbe1dbe0a843d41b83ab94b0157ffc1ed9
- governance Goal = Sentigraph Baseline v1.9 Post-ENV-R2 Helper-audit Blockers Governance Rebaseline
- governance Prompt classification = governance_only_not_engineering_prompt
- approval reusable = no
- Goal reusable = no

Independent ChatGPT acceptance of Baseline v1.9 has not been claimed or granted by this document.

## 3. Accepted project checkpoint

The accepted state is preserved through Baseline v1.8:

- MVP-B01 = completed_and_independently_accepted
- MVP-B02 = completed_and_independently_accepted
- MVP-B03 = completed_and_independently_accepted
- MVP-B04 = completed_and_independently_accepted
- MVP-B05-P1 = completed_and_independently_accepted
- effective MVP-B05-P2 = completed_and_independently_accepted_via_RC1
- MVP-B05-P3 = completed_and_independently_accepted
- effective MVP-B05-P4 = completed_and_independently_accepted_via_RC1
- MVP-B05-CIB-P1 = completed_and_independently_accepted
- Baseline v1.8 = completed_and_independently_accepted

The P4 initial needs-fix outcome and P4-RC1 test-only repair remain distinct history:

- P4 initial implementation commit = 0ee548deb8cb6fafbf44f8a5a6e5c52ec76cae56
- P4 initial independent review = needs_fix_directly_coupled_suite_order_dependent_lazy_import_test
- P4-RC1 commit = 06b843d6e6ec39cd982bf8b5f1344e58ade45f77
- P4 historical needs_fix reclassified = no
- CIB-P1 commit = c7dc7adcdf2c889ad43df2f68554e45cd993945f
- CIB-P1 contract blob = 939190f8794468b0485051e9ab6801a484129cb8
- P4 service blob = 9818622c3000092e4f9ee84b4a86300bb415d074
- Baseline v1.8 commit = 998e5f3ca25ddd6f270a35d59ab24e281917401c
- Baseline v1.8 document blob = eb3346e5cd71a1dd2b14ff0da5553d93e08c1c6f

The accepted boundary before Baseline v1.9 is:

- latest accepted business checkpoint = Baseline v1.8 effective after accepted CIB-P1, with all later CIB/ENV attempts preserved as blocked history
- latest repository anchor before v1.9 = 998e5f3ca25ddd6f270a35d59ab24e281917401c
- configuration identity binding captured = no
- Windows environment repaired = no
- runtime use authorized = no
- artifact access authorized = no
- B05 GET authorized = no

## 4. Initial CIB-P2 blocked history

- status = blocked_configuration_identity_capture
- protected runner executions = 1
- fresh runner processes = 1
- environment-source sessions = 1
- direct environment reads = 3
- reads per exact variable = 1
- second reads = 0
- automatic retries = 0
- salt generations = 0
- canonical configuration objects = 0
- configuration-derived SHA-256 computations = 0
- safe receipts = 0
- reports = 0
- repository changes = 0
- commits = 0
- pushes = 0
- approval reusable = no
- Goal reusable = no
- result reclassified = no
- capture replayed = no

This was a valid fail-closed protected attempt, not a completed result. No salt, canonical object, binding, or receipt exists. Its approval and Goal are consumed, and no replay or retry authority survives.

## 5. ENV-R1 blocked history

- status = blocked_safe_discovery_or_repair
- exact Provider Result match count = 1
- Provider Result opens / reads = 1 / 1
- strict UTF-8 = pass
- duplicate-key rejection = pass
- package-directory searches = 1
- package candidate state = candidate_count_not_exactly_one
- derived values = 0
- Windows user-environment writes = 0
- Windows user-environment readbacks = 0
- configuration capture = no
- repository changes = 0
- commits = 0
- pushes = 0
- approval reusable = no
- Goal reusable = no
- result reclassified = no
- helper replayed = no

Exact Provider Result discovery succeeded, but the candidate state did not yield exactly one permitted candidate. The exact candidate count and locations remain intentionally undisclosed. No values were derived or written. The approval and Goal are consumed, and no replay authority survives.

## 6. Initial ENV-R2 blocked helper-audit history

- status = blocked_helper_audit
- audit result = AUDIT_ROOT_FAIL
- helper construction/readback/hash/AST parse = 1 / 1 / 1 / 1
- helper AST audits passed = 0
- helper execution = 0
- Provider Result searches / opens / reads / reopens = 0 / 0 / 0 / 0
- package searches = 0
- safe metadata reads = 0
- derived values = 0
- environment writes/readbacks = 0 / 0
- repository changes = 0
- approval reusable = no
- Goal reusable = no
- result reclassified = no
- helper replayed = no

Diagnostic context only: the later Codex explanation identified a fixed search-root escape construction defect. This diagnostic statement does not replace the terminal counters, independently validate the deleted helper source, reclassify the blocked outcome, or create retry authority.

## 7. ENV-R2-R1 blocked pre-protected helper-audit history

- status = blocked_pre_protected_helper_audit
- helper construction/audit attempt count = 2
- helpers simultaneously present maximum = 1
- attempt 1 = AUDIT_STDOUT_FAIL
- attempt 2 = AUDIT_REPARSE_FAIL
- search-root AST semantic equality = pass for both attempts
- standard-library-only = pass
- forbidden import/call scan = pass
- helper execution = 0
- execution retry / second execution = 0 / 0
- Provider Result searches / opens / reads / reopens = 0 / 0 / 0 / 0
- package searches = 0
- safe metadata reads = 0
- protected/local data operations = 0
- environment writes/readbacks = 0 / 0
- repository changes = 0
- approval reusable = no
- Goal reusable = no
- result reclassified = no
- helper replayed = no

Diagnostic context for attempt 1 only: the auditor rejected three controlled allowlisted constant output points because it incorrectly relied on output-call structure rather than exact allowlisted constant dataflow.

Diagnostic context for attempt 2 only: the auditor rejected a safe `getattr(file_stat, "st_file_attributes", 0)` plus `FILE_ATTRIBUTE_REPARSE_POINT` bitmask pattern because it incorrectly required direct attribute syntax.

These diagnostic explanations do not override terminal counters, independently prove or re-review the deleted helper source, reclassify ENV-R2-R1, or create execution or retry authority. No blocked result is reclassified.

## 8. Baseline v1.8 historical closure

- budget fixed/conditional/risk = 2 / 4 / 3
- consumed engineering/fixed/conditional/risk = 2 / 0 / 0 / 2
- remaining fixed/conditional/risk = 2 / 4 / 1
- Baseline v1.8 status = historical_closed_for_future_prompt_accounting_after_ENV_R2_and_ENV_R2_R1_pre_protected_helper_audit_blockers
- historical reset = no
- historical transfer = no
- historical erasure = no
- historical merge = no
- historical reclassification = no
- historical outcome reclassification = no
- unused fixed transferred into v1.9 = no
- unused conditional transferred into v1.9 = no
- unused risk transferred into v1.9 = no

Unused Baseline v1.8 capacities are historical facts only. They grant no current authority and are not transferred into Baseline v1.9.

## 9. Baseline v1.9 budget

- fixed_prompt_budget = 2
- conditional_prompt_allowance = 4
- risk_buffer_prompt_allowance = 3
- consumed_engineering_prompts_since_v1_9 = 0
- consumed_fixed_prompts_since_v1_9 = 0
- consumed_conditional_prompts_since_v1_9 = 0
- consumed_risk_prompts_since_v1_9 = 0
- remaining_fixed_prompts = 2
- remaining_conditional_allowance = 4
- remaining_risk_buffer = 3
- this governance Goal charged to v1.8 = no
- this governance Goal charged to v1.9 = no

Budget is planning capacity, not execution authority.

## 10. One-Prompt and one-category accounting

1. One fresh approved engineering Prompt and verified Goal consume one category.
2. No Prompt is charged to multiple categories.
3. Sub-actions inside one Goal are not separately charged.
4. A verified Goal remains consumed after a blocked or failed outcome.
5. A new recovery or replacement requires fresh approval and Goal.
6. Governance rebaseline work is not an engineering Prompt.
7. Budget and reservation do not authorize execution.
8. A blocked Goal cannot be replayed under a later baseline.
9. Diagnostic explanations do not override terminal-receipt counters.

## 11. Selected next fixed milestone: ENV-R2-R2-P1

- milestone = MVP-B05-CIB-ENV-R2-R2-P1 Fixed Helper, Auditor and Auditor Self-test Package Creation and Static Validation
- classification = planned fixed milestone 1
- status = selected_not_started_not_authorized
- ENV_R2_R2_P1_selected = yes
- ENV_R2_R2_P1_eligible_after_v1_9_acceptance = yes
- ENV_R2_R2_P1_authorized = no
- ENV_R2_R2_P1_Goal_authorized = no
- ENV_R2_R2_P1_executed = no

The future P1 scope must remain static-only:

- ChatGPT-provided fixed UTF-8 helper source.
- Fixed auditor rules.
- Fixed positive and negative auditor self-test fixtures.
- Fixed SHA-256 identities.
- No Provider Result or package access.
- No environment or registry access.
- No helper business execution.

Selection and eligibility after independent acceptance create no present implementation or execution authority.

## 12. Auditor self-test contract for future P1

Future P1 must complete and pass the auditor self-test before any helper attempt is consumed or any helper is executed.

### Stdout positive fixture

Multiple output callsites must be accepted when every reachable output value resolves through exact constant dataflow to the approved constant-output set. Acceptance must not depend on output-call count or structure alone.

### Stdout negative fixtures

The auditor must reject:

- f-strings;
- runtime string concatenation;
- formatting with runtime data;
- exception text;
- paths;
- values;
- IDs;
- counts;
- registry contents.

### Reparse positive fixtures

The auditor must accept both `file_stat.st_file_attributes` and `getattr(file_stat, "st_file_attributes", 0)` only when each is combined with all of the following:

- Exact `FILE_ATTRIBUTE_REPARSE_POINT` bitmask semantics.
- Skip/no-descent control flow.
- Non-following directory-inspection semantics.

### Reparse negative fixtures

The auditor must reject:

- Attribute extraction without the reparse-point bitmask.
- A bitmask check without skip/no-descent control flow.
- Detection followed by recursive descent.
- A broad exemption or path-normalization fallback.

The auditor self-test must complete before a helper attempt is consumed.

## 13. Future ENV-R2-R2-P2 reserve

- Baseline v1.9 risk Prompt 1 = MVP-B05-CIB-ENV-R2-R2-P2 One Fixed-helper Bounded Package Disambiguation and Windows User Environment Repair Execution
- ENV_R2_R2_P2_selected = no
- ENV_R2_R2_P2_eligible = no
- ENV_R2_R2_P2_authorized = no
- ENV_R2_R2_P2_Goal_authorized = no
- ENV_R2_R2_P2_executed = no

Eligibility requires all of the following:

1. P1 completion.
2. Independent ChatGPT acceptance.
3. Exact fixed helper, auditor, and fixture identities.
4. Fresh exact risk approval.
5. Fresh Goal.

The reserve creates no implementation or execution authority.

## 14. CIB-P2-R1 reserve

- Baseline v1.9 conditional Prompt 1 = MVP-B05-CIB-P2-R1 One Fresh Safe Configuration Identity Capture
- MVP_B05_CIB_P2_R1_selected = yes
- MVP_B05_CIB_P2_R1_eligible = no
- MVP_B05_CIB_P2_R1_authorized = no
- MVP_B05_CIB_P2_R1_Goal_authorized = no
- MVP_B05_CIB_P2_R1_executed = no

Eligibility requires all of the following:

1. Successful ENV-R2-R2-P2 repair.
2. Applicable independent acceptance.
3. Full closure of every Codex process.
4. Closure of old launch terminals.
5. Startup of a new process inheriting the repaired environment.
6. Fresh exact conditional approval.
7. Fresh Goal.

The reserve leaves CIB-P2-R1 selected but ineligible and unauthorized.

## 15. P5 and recovery reserves

- Baseline v1.9 risk Prompt 2 = MVP-B05-P5 One Real Sample-handle Governed Read-only Projection Smoke
- MVP_B05_P5_selected = no
- MVP_B05_P5_eligible = no
- MVP_B05_P5_authorized = no
- MVP_B05_P5_Goal_authorized = no
- MVP_B05_P5_executed = no
- Baseline v1.9 risk Prompt 3 = one narrow fixed-helper, ENV, capture or P5 protected-action recovery
- Baseline v1.9 fixed Prompt 2 = one bounded pre-execution fixed-package repair or equivalent static safety hardening

P5 eligibility requires independently accepted CIB-P2-R1 binding evidence. The risk Prompt 3 recovery reserve and fixed Prompt 2 reserve are unselected and unauthorized. All remaining fixed, conditional, and risk capacity is likewise unselected and unauthorized.

## 16. No-runtime and no-side-effect proof

- local Provider Result searches = 0
- package searches = 0
- environment reads/writes = 0/0
- registry reads/writes = 0/0
- helper/auditor package creation = 0
- auditor self-test executions = 0
- helper executions = 0
- configuration capture/hash/salt/receipt = 0/0/0/0
- artifact access/hash = 0/0
- application imports = 0
- endpoint calls = 0
- provider/collector/network/LLM/browser = 0/0/0/0/0
- database/persistence = 0/0
- product code/test/config/route/API/frontend changes = 0/0/0/0/0/0
- Project Source changed = no
- tag = no
- release = no

## 17. Source responsibility and synchronization boundary

- Baseline v1.9 governs post-helper-audit-blocker accounting and sequencing.
- It does not replace CIB-P1's technical binding contract.
- It does not validate deleted ENV helper source.
- It does not create a fixed helper or auditor package.
- It does not prove successful environment repair or capture.
- It does not modify Project Source.
- Project Source synchronization requires a later separate bounded task after independent acceptance.
- Source synchronization creates no P1, P2, CIB-P2-R1, or P5 authority.

## 18. Exact authorization state

- Baseline v1.9 document created = yes
- Baseline v1.9 independently accepted = no
- ENV-R2-R2-P1 selected = yes
- ENV-R2-R2-P1 eligible = yes
- ENV-R2-R2-P1 authorized = no
- ENV-R2-R2-P1 executed = no
- ENV-R2-R2-P2 selected = no
- ENV-R2-R2-P2 eligible = no
- ENV-R2-R2-P2 authorized = no
- ENV-R2-R2-P2 executed = no
- CIB-P2-R1 selected = yes
- CIB-P2-R1 eligible = no
- CIB-P2-R1 authorized = no
- CIB-P2-R1 executed = no
- B05-P5 selected = no
- B05-P5 eligible = no
- B05-P5 authorized = no
- B05-P5 executed = no
- runtime authority created = no
- Baseline_v1_9_status = candidate_effective_pending_independent_ChatGPT_acceptance

The next boundary is independent ChatGPT acceptance only. Until a later separate exact authorization is granted: do not create the ENV-R2-R2-P1 fixed helper/auditor package; do not run auditor self-tests; do not search Provider Results or packages; do not read or write environment or registry values; do not execute ENV-R2-R2-P2; do not execute CIB-P2-R1; do not access or hash the artifact; do not import the application; do not call B05 GET; do not start B05-P5; and do not perform persistence, production, public, export, or delivery work.
