# Sentigraph 9A-18 Candidate Demo Sample Role-policy Clarification Decision v0.1

## Decision

- phase = 9A-18
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- implementation_performed = no
- backend_code_changed = no
- tests_changed = no
- frontend_changed = no
- route_changed = no
- runtime_changed = no

This prospective policy resolves the candidate-role blocker recorded by 9A-17. It does not alter historical 9A-16B, 9A-16C, or 9A-17 records and does not authorize or execute a write.

## Approval

- exact_approval_phrase_received = yes
- exact_approval_phrase_validated = yes
- approval_scope = 9A-18 candidate_demo_sample role-policy clarification docs-only

Exact approval phrase:

`APPROVE_9A_18_CANDIDATE_DEMO_SAMPLE_ROLE_POLICY_CLARIFICATION_DOCS_ONLY`

The approval permits only this planning decision, its paired architecture contract, exact-candidate binding, and docs-only validation. It is not final-write authorization or actual-write execution authorization.

## Exact Locked-candidate Binding

- approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016
- approved_package_role = candidate_demo_sample
- approved_case_id_hint = donglu_sunjihai_youth_football_202606
- approved_row_source = evidence_items.jsonl
- selected_preview_row_opaque_id = preview-row-001
- selected_preview_row_safe_hash = ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391
- final_candidate_id = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- final_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- final_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- identity_schema = sentigraph_one_real_source_locked_candidate_identity_v0_1
- candidate_lock_status = locked_for_single_candidate_governance_review_only

Scope invariants:

- candidate_scope = exactly_one_locked_real_source_controlled_candidate
- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- hash_mismatch_invalidates_decision = yes
- candidate_id_mismatch_invalidates_decision = yes
- schema_or_role_change_invalidates_decision = yes

The governance key is indivisible. This decision cannot transfer to another candidate, package, row, schema, or role.

## Historical 9A-17 Blocker

Before this clarification:

- candidate_role = candidate_demo_sample
- candidate_role_policy_clear = no
- write_target_eligibility_outcome = blocked_pending_candidate_role_policy_clarification
- final_write_authorization_readiness_status = conditionally_ready_pending_candidate_role_policy_resolution
- approval_guard_consistency_status = stable_current_exact_guards
- ready_for_actual_write = false
- next_default = pause

Identity binding, candidate-specific review, lineage, privacy, rollback, and guard consistency were complete. This document changes only the prospective role-policy conclusion.

## General Candidate Demo Sample Policy

- candidate_role = candidate_demo_sample
- candidate_role_reclassified = no
- candidate_demo_sample_general_classification = non_production_governance_sample
- candidate_demo_sample_automatic_write_permission = no
- candidate_demo_sample_automatic_production_eligibility = no
- candidate_demo_sample_automatic_trust_upgrade = no
- candidate_demo_sample_whole_package_approval = no

Every `candidate_demo_sample` remains non-production, review-oriented, and candidate-specific. The role neither permanently qualifies nor permanently disqualifies every future sample from a human authorization review. A separate explicit policy decision is required for each locked candidate.

## Exact Locked-candidate Exception

- exact_locked_candidate_exception_created = yes
- exception_scope = future_separate_human_final_authorization_review_eligibility_only
- candidate_eligible_for_future_human_final_authorization_review = yes
- candidate_eligible_for_actual_write_now = no
- candidate_eligible_for_production_evidenceitem_creation_now = no
- production_write_target_eligible_now = no
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- final_write_authorization_performed = no
- ready_for_actual_write = false

The exception permits only the exact locked candidate to enter a later, separate, directly human-authored final-write authorization decision. It does not change the role to production, authorize a write, approve the package, confer eligibility on another candidate, supply the future human decision, or transfer responsibility to ChatGPT or Codex.

## Write-target Eligibility Decision

- candidate_role_policy_clear = yes
- write_target_eligibility_outcome = eligible_for_separate_human_final_authorization_review_only
- candidate_specific_review_complete = yes
- production_write_target_eligible_now = no
- actual_write_next = no
- production_evidenceitem_creation_next = no

Eligibility for a future decision is a governance state, not write permission.

## Final-write Authorization Readiness Decision

- final_write_authorization_readiness_status = ready_for_separate_human_final_authorization_decision_for_locked_candidate
- final_write_authorization_decision_received_now = no
- final_write_authorization_performed = no
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- ready_for_actual_write = false

The next human decision must be separately authored and cannot be inferred from this document. This document supplies no approval phrase and no ready-to-sign authorization template.

## Human Authority Boundary

- declared_authority_role_label = self_declared_project_owner_role
- authority_basis_label = authority_basis_not_independently_validated
- manual_review_responsibility_statement_present = yes
- warning_count_acknowledgment_present = yes
- human_review_required_acknowledgment_present = yes
- no_automatic_trust_upgrade_acknowledgment_present = yes
- human_authority_validated = no
- runtime_human_authority_validation_performed = no
- manual_review_responsibility_accepted_as_runtime_or_audit_state = no
- runtime_manual_review_responsibility_acceptance_performed = no

ChatGPT and Codex cannot validate legal or organizational authority, accept responsibility for the user, or convert generated wording into a human decision.

## Invalidation Rules

This role-policy exception is invalid if any locked package, role, case, source, schema, ID, or hash field changes. It is also invalid after candidate/package/row substitution, role reclassification, automatic trust upgrade, whole-package inference, privacy concern, lineage change, unresolved blocker, or guard inconsistency.

Invalidation returns the candidate to `pause`; it never authorizes a fallback candidate.

## Hard Stops

Stop before any later final-authorization decision if:

- the locked governance key does not match exactly
- any other row, candidate, or package scope is introduced
- the role or schema changes
- candidate review, lineage, privacy, rollback, or guard status changes
- a warning or trust boundary is ignored
- generated wording is represented as a human decision
- a request attempts to execute write, persistence, production, route, API, frontend, Source 11, report, or delivery behavior

## No-write and No-production Proof

- actual_evidence_layer_write_approved = no
- actual_evidence_layer_write_performed = no
- persisted_evidence_layer_record_created = no
- production_evidenceitem_creation_authorized = false
- production_evidenceitem_created = no
- review_queue_runtime_used = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_created = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- public_delivery_created = no
- provider_called = no
- collector_called = no
- real_api_called = no
- real_llm_called = no
- url_fetch_or_scrape = no

## Selected Next Boundary

- selected_next_boundary = pause_before_separate_human_final_authorization_decision
- actual_write_next = no
- production_evidenceitem_creation_next = no
- next_default = pause

No final-write phrase is created. No next phase begins automatically.

## Validation and Not-run Items

- validation_scope = docs-only identity, policy, overclaim, whitespace, and Git allowlist checks
- backend_tests = not run, docs-only
- frontend_build = not run, no frontend change
- browser_smoke = not run, no UI change
- full_pytest = not run, docs-only

## Git and Source Recommendation

- commit_recommended = yes
- recommended_commit_message = Add 9A-18 candidate demo sample role policy clarification
- tag_recommended = no
- project_source_update_recommended = no for this small docs-only step
- source11_update_recommended = no
