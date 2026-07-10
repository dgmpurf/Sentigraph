# Sentigraph Human-provided Declaration Recognition Checklist v0.1

## Purpose

This checklist gives a future docs-only or tests-only phase a conservative structure for recognizing whether later human-supplied text contains the minimum safe components for review. It is not a declaration and it does not create write permission.

## Source Requirement

Acceptable future source kinds:

- explicit_human_message_later
- separately_governed_external_audit_note_later

Never sufficient:

- Codex-generated text
- a copied template filled by Codex
- phase approval phrase
- "continue"
- "approved"
- "ready"
- commit/push confirmation
- implicit project-owner assumption
- prior fixture output
- route/UI action
- environment variable
- machine-generated signature

## Safe Role And Basis Labels

Allowed safe role labels:

- self_declared_project_owner_role
- self_declared_designated_reviewer_role
- self_declared_organization_reviewer_role
- not_specified

Allowed safe basis labels:

- authority_basis_not_independently_validated
- external_audit_reference_required_later
- not_specified

These labels are self-declared labels only. They are not verified authority.

## Required Structural Checks

- declaration_source_kind present
- declaration_scope present
- declared_authority_role_label present
- authority_basis_label present
- manual_review_responsibility_statement_present
- warning_count_acknowledgment_present
- human_review_required_acknowledgment_present
- no_automatic_trust_upgrade_acknowledgment_present
- blocker_review_status_present
- risk_review_status_present
- lineage_review_status_present
- raw_private_secret_absence_acknowledgment_present
- rollback_pause_responsibility_statement_present
- final_write_authorization_still_required = true
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- ready_for_actual_write = false
- human_authority_validated = false
- manual_review_responsibility_accepted = false
- final_write_authorization_performed = false

## Allowed Outcomes

- declaration_missing
- declaration_insufficient
- declaration_ambiguous
- declaration_present_for_docs_only_review
- privacy_issue_stop
- pause

## Forbidden Outcomes

- authority_validated
- responsibility_accepted
- final_authorization_complete
- ready_for_write
- write_approved
- production_ready

## Required Human Text Components For A Later Phase

- statement that the declaration comes from a human
- safe declared role label
- safe authority-basis label
- manual review responsibility statement
- warning_count acknowledgment
- human_review_required acknowledgment
- no_automatic_trust_upgrade acknowledgment
- blocker review statement
- risk review statement
- input-lineage review statement
- raw/private/secret absence acknowledgment
- rollback / pause / revocation responsibility statement
- statement that final write authorization is still required
- statement that actual write is not authorized by the declaration
- statement that production EvidenceItem creation is not authorized by the declaration
- statement that the system is not ready for actual write

## Insufficiency Blockers

- no separate human-supplied source exists
- content generated entirely by Codex
- only a phase approval phrase is supplied
- role label missing
- authority-basis label missing
- manual review responsibility statement missing or ambiguous
- required acknowledgments missing
- blockers or risks not addressed
- lineage status absent
- raw/private/secret absence not acknowledged
- rollback/pause responsibility missing
- wording claims actual write, final authorization, production EvidenceItem readiness, or automatic trust upgrade
- wording attempts to authorize production case, analysis_run, Analysis Result, Source 11, FinalSummaryReport, or public delivery
- wording contains real-person PII or secrets
- scope ambiguous
- declaration presented as route/UI/runtime trigger
- unresolved blocker remains

## Privacy Stop Catalog

Stop if future text requests or stores:

- legal names
- personal addresses
- personal phone numbers
- personal email addresses
- government IDs
- signature images
- credential tokens
- employment documents
- private proof files
- raw PII

## Boundary Checklist

- approval phrase is not declaration
- Codex-generated text is not declaration
- declaration presence classification is not identity validation
- declaration presence classification is not authority validation
- declaration presence classification is not responsibility acceptance
- declaration presence classification is not final write authorization
- declaration presence classification is not write permission
- actual Evidence Layer write remains not approved
- production EvidenceItem creation remains not approved
- final write authorization remains required later
