# Sentigraph Exact Locked-candidate Human Final-write Authorization Contract v0.1

## Purpose

This contract governs the recorded human final-write authorization decision for one exact 9A-16C locked candidate. It separates that completed governance decision from any later Evidence Layer write execution and from production EvidenceItem creation.

## Contract Scope

- contract_phase = 9A-19
- docs_only = yes
- human_final_write_authorization_recording_only = yes
- runtime_or_persistence_effect = no
- actual_write_execution_authorized_now = no
- production_evidenceitem_creation_authorized = false

The contract records an existing human decision. It does not make, strengthen, broaden, execute, or operationalize that decision.

## Immutable Exact-candidate Binding

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
- identity_version = 0.1
- hash_algorithm = sha256
- hash_input_scope = versioned_safe_canonical_projection_only
- candidate_lock_status = locked_for_single_candidate_governance_review_only

All fields are one indivisible authorization key. No partial match, nearest match, inferred identity, or replacement is valid.

## Authorization Scope Invariants

- candidate_scope = exactly_one_locked_real_source_controlled_candidate
- final_write_authorization_scope = exact_locked_candidate_only
- whole_package_approved = no
- other_rows_approved = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- candidate_id_mismatch_invalidates_authorization = yes
- candidate_hash_mismatch_invalidates_authorization = yes
- package_mismatch_invalidates_authorization = yes
- role_mismatch_invalidates_authorization = yes
- schema_mismatch_invalidates_authorization = yes
- row_source_mismatch_invalidates_authorization = yes

Authorization cannot transfer to another candidate, row, package, case, source, schema, role, ID, or hash.

## Recorded Human Decision

- decision_source_kind = explicit_human_message_in_main_chat
- human_authored_decision_present = yes
- human_final_write_authorization_decision_received = yes
- human_final_write_authorization_decision = approved
- human_final_write_authorization_performed = yes
- candidate_authorized_for_future_separately_gated_evidence_layer_write = yes

These fields record the human's completed candidate-specific governance decision. They do not constitute execution-gate approval.

## Candidate Demo Sample Boundary

- candidate_role = candidate_demo_sample
- candidate_role_reclassified = no
- candidate_role_policy_clear = yes
- candidate_demo_sample_general_classification = non_production_governance_sample
- candidate_demo_sample_automatic_write_permission = no
- candidate_demo_sample_automatic_production_eligibility = no
- candidate_demo_sample_automatic_trust_upgrade = no
- candidate_demo_sample_whole_package_approval = no
- exact_locked_candidate_exception_created = yes

The candidate retains its non-production governance-sample role. The authorization is an exact-candidate exception and establishes no package-wide, row-wide, role-wide, trust, verification, or production precedent.

## Final Authorization and Execution Are Separate

The following states must not be collapsed:

1. Candidate-specific governance review is complete.
2. The human final-write authorization decision for this exact candidate is complete.
3. A later actual-write execution gate has not been approved.
4. No Evidence Layer write has occurred.
5. Production EvidenceItem creation is unapproved and has not occurred.

Current contract state:

- human_final_write_authorization_performed = yes
- candidate_authorized_for_future_separately_gated_evidence_layer_write = yes
- actual_write_execution_authorized_now = no
- actual_write_execution_gate_approval_received = no
- actual_write_authorized = false
- actual_evidence_layer_write_approved_now = no
- actual_evidence_layer_write_performed = no
- persisted_evidence_layer_record_created = no
- ready_for_actual_write = false
- production_evidenceitem_creation_authorized = false
- production_evidenceitem_created = no

A later execution may be discussed only under a new exact approval gate. This contract contains no execution approval phrase and no ready-to-sign execution template.

## Human Authority and Responsibility Boundary

- declared_authority_role_label = self_declared_project_owner_role
- authority_basis_label = authority_basis_not_independently_validated
- human_authority_independently_validated = no
- runtime_human_authority_validation_performed = no
- human_review_required_acknowledgment_present = yes
- no_automatic_trust_upgrade_acknowledgment_present = yes
- pause_responsibility_accepted = yes
- revocation_responsibility_accepted = yes
- rollback_responsibility_accepted = yes
- manual_review_responsibility_statement_present = yes
- manual_review_responsibility_accepted_as_runtime_or_audit_state = no
- runtime_manual_review_responsibility_acceptance_performed = no

ChatGPT and Codex cannot sign for the human, independently validate authority, accept operational responsibility, or reinterpret the decision. No signature, legal identity, organization title, timestamp proof, or cryptographic authority evidence is inferred.

## Human Review and Trust Boundary

- human_review_required = yes
- no_automatic_trust_upgrade = yes
- official_verification_inferred = no
- provider_output_treated_as_truth = no
- production_readiness_inferred = no

Human review remains mandatory. Authorization does not increase trust, establish official verification, turn provider or sample output into truth, or imply production readiness.

## Mismatch and Fresh-governance Rules

Any change to candidate ID, candidate hash, preview ID, preview hash, package, role, case hint, row source, schema, identity schema, hash method, hash scope, or lock status invalidates this record. Candidate, package, or row substitution also invalidates it.

After invalidation:

- authorization_record_valid = no
- workflow_disposition = pause
- replacement_candidate_selected_automatically = no
- fresh_governance_required = yes
- fresh_human_decision_required = yes

No fallback candidate or package scope is inferred.

## Later Execution-gate Requirements

A later actual-write execution gate must, before any write:

- recheck every immutable field without opening or substituting unrelated rows
- confirm this authorization record remains valid and unrecalled
- stop on any identity, role, schema, hash, package, source, privacy, lineage, warning, trust, or guard mismatch
- preserve one-candidate-only scope
- preserve human review and no-automatic-trust-upgrade requirements
- separately govern production EvidenceItem creation
- avoid inferring permission for cases, analysis runs, Analysis Results, Source 11, reports, exports, public access, or delivery

This section defines prerequisites only. It does not approve an execution gate or a write.

## Pause, Revocation, and Rollback

- pause_on_any_mismatch_or_blocker = yes
- revocation_target_kind = one_real_source_locked_candidate
- revocation_target_ref = evidence-layer-write-candidate-from-production-import-001-0deacf3cded01410
- rollback_action = revoke_candidate_specific_authorization_record_and_return_to_pause
- persistence_rollback_required = no
- no_persistence = yes
- actual_write_execution_gate_still_required = yes

Revocation or mismatch removes the candidate-specific authorization state. Because 9A-19 performs no persistence or write, no Evidence Layer data or production object requires rollback.

## Downstream Non-authorization

Final-write authorization for this candidate does not imply permission for:

- production Review Queue runtime or item creation
- production case creation
- production analysis_run creation
- actual analysis execution
- production Analysis Result creation
- Source 11 runtime
- FinalSummaryReport runtime
- B-end report or Sandbox/public-event generation
- export, download, public access, external delivery, or final delivery
- provider, collector, real API, real LLM, URL fetch, or scraping

All such capabilities remain outside this contract and unperformed.

## No-side-effect Guarantees

- backend_code_changed = no
- tests_changed = no
- frontend_changed = no
- route_changed = no
- runtime_changed = no
- package_or_row_opened_or_parsed = no
- write_helper_called = no
- evidence_import_called = no
- evidence_ingestion_called = no
- persisted_evidence_layer_record_created = no
- production_review_queue_runtime_used = no
- production_review_queue_item_created = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_created = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- b_end_report_runtime_generated = no
- sandbox_public_event_generated = no
- export_download_public_final_delivery_created = no
- provider_or_collector_called = no
- real_api_or_llm_called = no
- url_fetch_or_scrape = no

## Next Boundary

- next_default = pause_before_separate_actual_evidence_layer_write_execution_gate
- actual_write_next = no
- production_evidenceitem_creation_next = no
- ready_for_actual_write = false

The next boundary is a separate governance decision about an execution gate. No write, production EvidenceItem, or Phase 9A-20 action begins automatically.
