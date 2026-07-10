# Sentigraph Single Locked-candidate Human Final-write Authorization Readiness Checklist v0.1

## Status

This checklist is not an authorization. It cannot be completed, signed, or submitted by ChatGPT or Codex on the user's behalf. Copying generated wording does not make it a human decision.

Current readiness is conditional on explicit repository policy for `candidate_demo_sample`. Do not use this checklist to bypass that unresolved policy.

## Locked Candidate Reference

- selected_preview_row_opaque_id = preview-row-001
- selected_preview_row_safe_hash = ec06201c92f2fc6c22bca509a285fb02c317bd582460852b82669b79ff711391
- final_candidate_id = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- final_candidate_safe_hash = 2d60536b6afa3324ac5518df545d0826f4109e1580da447d02fee8413e352cb5
- final_candidate_schema = sentigraph_controlled_evidence_layer_write_candidate_from_production_import_candidate_set_v0_1
- approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016
- approved_package_role = candidate_demo_sample
- approved_case_id_hint = donglu_sunjihai_youth_football_202606
- approved_row_source = evidence_items.jsonl

Any mismatch invalidates the readiness review. No substitution is allowed.

## Scope Lock

- candidate_scope = exactly_one_locked_real_source_controlled_candidate
- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- hash_mismatch_invalidates_decision = yes
- candidate_id_mismatch_invalidates_decision = yes

## Preconditions Before a Human Decision

- [ ] Repository policy explicitly permits this exact `candidate_demo_sample` candidate to enter a final-authorization decision.
- [ ] The message is authored directly by the human decision-maker.
- [ ] The exact candidate ID, candidate hash, preview ID, preview hash, schema, package, role, case hint, and source basename are reproduced without change.
- [ ] Scope is explicitly limited to this one candidate.
- [ ] The message states that no other row, candidate, or package content is approved.
- [ ] Candidate-specific structural blocker review is acknowledged.
- [ ] Conservative risk classifications, including open and unknown risks, are acknowledged.
- [ ] Full lineage verification is acknowledged.
- [ ] Privacy, secret, and output-minimization review is acknowledged.
- [ ] Rollback, pause, and revocation responsibility is explicitly accepted by the human.
- [ ] `human_review_required` is acknowledged.
- [ ] `no_automatic_trust_upgrade` is acknowledged.
- [ ] The self-declared authority basis and lack of independent authority validation are acknowledged.
- [ ] Production EvidenceItem creation remains separately governed.
- [ ] Stop-before-write is required if any locked field, blocker, privacy status, lineage status, guard, or role policy changes.

## Required Human Message Properties

A later, separate human message must contain:

- an explicit statement that it is human-authored
- all exact locked candidate fields listed above
- one-candidate-only and no-package-approval scope
- review, risk, lineage, privacy, warning, and trust acknowledgments
- rollback/pause/revocation responsibility acceptance
- an explicit final-write authorization decision written by that human
- acknowledgment that final authorization still does not execute a write

This document intentionally supplies no authorization phrase or ready-to-sign authorization template.

## Invalidation Rules

The decision is invalid if:

- either ID or hash differs
- package, role, case hint, source basename, or schema differs
- another candidate or row is substituted
- whole-package approval is inferred
- candidate role policy is still unresolved
- a blocker, privacy issue, lineage gap, or guard ambiguity exists
- authority is represented as independently validated when it is not
- generated wording is presented as the human's independent decision

## Execution Boundary

- final_write_authorization_decision_received_now = no
- final_write_authorization_performed = no
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- ready_for_actual_write = false
- actual_write_next = no

One-candidate final authorization would not authorize the package and would not execute a write automatically. Actual Evidence Layer write and production EvidenceItem creation require a later separately approved execution gate.

## Current Next Boundary

- selected_next_boundary_option = pause_pending_candidate_role_policy_or_approval_guard_consistency_resolution
- blocking_branch = candidate_role_policy
- approval_guard_consistency_status = stable_current_exact_guards
- next_default = pause

ChatGPT and Codex must remain paused until a human supplies a separate decision after role-policy resolution.
