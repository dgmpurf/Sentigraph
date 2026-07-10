# Sentigraph One Real-source Candidate Write-target Eligibility and Final-write Authorization Readiness Contract v0.1

## Purpose

This contract defines how one identity-complete, no-write, real-source controlled candidate may be assessed for future human final-authorization readiness. It does not authorize or execute a write.

## Locked Candidate

- identity_schema = sentigraph_one_real_source_locked_candidate_identity_v0_1
- identity_version = 0.1
- selected_preview_row_opaque_id = preview-row-001
- selected_preview_row_safe_hash = ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391
- final_candidate_id = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- final_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- final_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016
- approved_package_role = candidate_demo_sample
- approved_case_id_hint = donglu_sunjihai_youth_football_202606
- approved_row_source = evidence_items.jsonl
- candidate_lock_status = locked_for_single_candidate_governance_review_only

These values form one indivisible governance key. Any mismatch invalidates downstream readiness decisions.

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

This candidate does not confer status on any other row, candidate, package content, or future execution.

## Eligibility Distinctions

The following states must remain separate:

1. Candidate-specific review complete.
2. Candidate eligible for a future human final-authorization review.
3. Candidate authorized for actual Evidence Layer write.
4. Candidate authorized for production EvidenceItem creation.

For this candidate:

- candidate_specific_review_complete = yes
- candidate_eligible_for_future_human_final_authorization_review = no, pending role-policy resolution
- candidate_eligible_for_actual_write_now = no
- candidate_eligible_for_production_evidenceitem_creation_now = no
- production_write_target_eligible_now = no

## Candidate Role Gate

The repository identifies the role as `candidate_demo_sample` and consistently treats it as non-production. Current contracts do not state whether it is a permanent write disqualifier or may enter a later final-authorization review.

- candidate_role_policy_clear = no
- candidate_role_is_automatic_write_disqualifier = unknown
- required_resolution = explicit repository policy for candidate_demo_sample eligibility
- role_reclassification_allowed_by_this_contract = no

Until that policy exists, the candidate remains in governance review only.

## Review Preconditions

All of the following must remain true:

- exact candidate identity binding complete
- candidate-specific structural blockers clear
- required risks classified conservatively
- full lineage continuity verified
- privacy/raw/private/secret review complete
- rollback/pause/revocation plan verified
- human_review_required acknowledged
- no_automatic_trust_upgrade acknowledged
- warning state acknowledged
- no production/public/customer readiness claim

Open or unknown risk labels are not silently upgraded by candidate locking.

## Approval-guard Contract

- approval_guard_consistency_status = stable_current_exact_guards
- guard_variant_substitution_allowed = no
- historical_or_mojibake_guard_allowed = no
- guard_change_allowed_by_9a17 = no

ASCII helper guards and the exact UTF-8 8W-22/8W-25 guards are independently tested. A later guard change requires separate approval and tests but is not currently a readiness blocker.

## Human Decision Boundary

The human declaration context remains non-authorizing:

- authority basis is self-declared and not independently validated
- manual-review responsibility statement is present but not runtime-accepted
- final-write authorization has not been received or performed
- Codex cannot validate authority or accept responsibility
- generated or copied wording is not a human authorization by itself

No automatic trust upgrade, authorization inference, or candidate substitution is permitted.

## Readiness Outcomes

Allowed outcomes are:

- `ready_for_separate_human_final_authorization_decision_for_locked_candidate`
- `conditionally_ready_pending_candidate_role_policy_resolution`
- `conditionally_ready_pending_guard_consistency_resolution`
- `not_ready_due_to_identity_binding_gap`
- `not_ready_due_to_unresolved_authorization_blockers`
- `pause`

Current outcome:

- final_write_authorization_readiness_status = conditionally_ready_pending_candidate_role_policy_resolution
- overall_write_disposition = pause
- ready_for_actual_write = false

## Hard Stops

Stop before any authorization or write if any of these occur:

- candidate ID, hash, schema, role, package, or source mismatch
- candidate/package/row substitution
- privacy, raw identity, private content, or secret concern
- lineage gap or unreviewed blocker
- unacknowledged warning or trust upgrade
- guard ambiguity or changed guard contract
- candidate role policy remains unresolved
- production/public/customer-ready overclaim
- request to execute a helper, route, persistence, or production runtime

## No Side Effects

- final_write_authorization_performed = no
- actual_write_authorized = false
- actual_evidence_layer_write_performed = no
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

Even a later valid human final-authorization decision would not execute a write. Execution requires another separately approved gate.
