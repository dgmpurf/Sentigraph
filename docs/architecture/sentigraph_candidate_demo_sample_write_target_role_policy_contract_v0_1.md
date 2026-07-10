# Sentigraph Candidate Demo Sample Write-target Role-policy Contract v0.1

## Purpose

This contract defines the conservative general policy for `candidate_demo_sample` and one narrow exception for the exact 9A-16C locked candidate. The exception permits future human final-authorization review eligibility only. It does not authorize or execute a write.

## Policy Scope

- policy_phase = 9A-18
- policy_scope = candidate_demo_sample governance classification and one exact-candidate exception
- docs_only = yes
- role_reclassification_performed = no
- runtime_or_persistence_effect = no

The general policy applies to the role classification. The exception applies only to the exact locked governance key below.

## Exact Locked Candidate

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

## Scope Invariants

- candidate_scope = exactly_one_locked_real_source_controlled_candidate
- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- hash_mismatch_invalidates_decision = yes
- candidate_id_mismatch_invalidates_decision = yes
- schema_or_role_change_invalidates_decision = yes

No candidate, package, row, role, or schema may inherit this exception.

## General Classification

- candidate_role = candidate_demo_sample
- candidate_role_reclassified = no
- candidate_demo_sample_general_classification = non_production_governance_sample
- candidate_demo_sample_automatic_write_permission = no
- candidate_demo_sample_automatic_production_eligibility = no
- candidate_demo_sample_automatic_trust_upgrade = no
- candidate_demo_sample_whole_package_approval = no

General `candidate_demo_sample` objects are non-production governance/review samples. The role is not an automatic qualification for authorization review and not a universal permanent disqualification. Eligibility requires an exact-candidate policy exception with immutable identity binding and completed governance review.

## Candidate-specific Exception Rules

- exact_locked_candidate_exception_created = yes
- exception_scope = future_separate_human_final_authorization_review_eligibility_only
- candidate_role_policy_clear = yes
- candidate_eligible_for_future_human_final_authorization_review = yes
- candidate_eligible_for_actual_write_now = no
- candidate_eligible_for_production_evidenceitem_creation_now = no
- production_write_target_eligible_now = no

The exception is valid only while every locked field and review boundary remains unchanged. It does not reclassify the candidate, authorize a write, approve a package, or establish precedent for another candidate.

## Eligibility-state Distinctions

The following states are independent and must not be collapsed:

1. Candidate-specific review complete: true.
2. Candidate role policy clear: true.
3. Candidate eligible for a future human final-authorization decision: true.
4. Candidate finally authorized for actual Evidence Layer write: false.
5. Candidate authorized for production EvidenceItem creation: false.
6. Actual write execution separately approved: false.

Current policy result:

- write_target_eligibility_outcome = eligible_for_separate_human_final_authorization_review_only
- final_write_authorization_readiness_status = ready_for_separate_human_final_authorization_decision_for_locked_candidate
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- ready_for_actual_write = false

States 1 through 3 are governance readiness states. They do not imply states 4 through 6.

## Human Final-authorization Boundary

A later final-authorization decision must be separately and directly human-authored, refer to every exact locked field, preserve one-candidate-only scope, acknowledge open and unknown risks, and accept rollback/pause/revocation responsibility.

- final_write_authorization_decision_received_now = no
- final_write_authorization_performed = no
- human_authority_validated = no
- manual_review_responsibility_accepted_as_runtime_or_audit_state = no

ChatGPT or Codex cannot supply, sign, infer, or accept responsibility for that human decision. Copied generated wording is not sufficient by itself.

## Trust and Role Boundaries

- no_automatic_trust_upgrade = yes
- role_reclassification_allowed = no
- production_role_inferred = no
- official_verification_inferred = no
- whole_package_approval_inferred = no

Provider or sample output remains evidence for review, not truth. Future-review eligibility does not change trust, verification, production, or causality status.

## Field and Substitution Invalidation

The exception is immediately invalid if:

- either ID or hash differs
- package name, package role, case hint, source basename, schema, or lock status differs
- a different candidate, package, or row is substituted
- the role is reclassified
- whole-package approval is inferred
- a privacy, lineage, rollback, warning, trust, or guard boundary changes

Invalidation requires pause and a new governance decision. It never selects a replacement automatically.

## Rollback, Pause, and Revocation

- pause_on_any_blocker = yes
- revocation_target_kind = one_real_source_locked_candidate
- revocation_target_ref = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- rollback_action = discard_governance_eligibility_and_return_to_pause
- persistence_rollback_required = no
- no_persistence = yes
- final_write_authorization_still_required = yes

Revocation removes only the candidate-specific review eligibility exception. No persisted evidence or production object exists to roll back.

## Hard Stops

Stop before any final-authorization discussion or execution if:

- immutable identity binding fails
- candidate/package/row substitution is attempted
- role or schema changes
- candidate review, risk, lineage, privacy, rollback, warning, or guard status is incomplete or changed
- automatic trust or production eligibility is inferred
- a generated template is presented as a human decision
- a request crosses into route, API, frontend, runtime, persistence, write, production, Source 11, reporting, export, public access, or delivery behavior

## No-side-effect Guarantees

- implementation_performed = no
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
- provider_or_collector_called = no
- real_api_or_llm_called = no
- url_fetch_or_scrape = no

## Future Decision Boundary

- selected_next_boundary = pause_before_separate_human_final_authorization_decision
- actual_write_next = no
- production_evidenceitem_creation_next = no
- next_default = pause

The next boundary is a separate human decision, not an implementation phase. This contract creates no final-write phrase, authorization template, write route, or execution permission.
