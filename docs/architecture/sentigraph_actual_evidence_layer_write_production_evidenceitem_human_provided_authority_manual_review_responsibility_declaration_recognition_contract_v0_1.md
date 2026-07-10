# Sentigraph Human-provided Authority / Manual-review Responsibility Declaration Recognition Contract v0.1

## A. Contract Purpose

This contract defines the 9A-13 docs-only declaration-recognition design. It describes how a future explicit human-provided authority and manual-review responsibility declaration could be recognized structurally, without validating authority, accepting responsibility, authorizing write, or collecting real-person PII.

This contract is docs-only. It does not implement backend code, tests, frontend behavior, routes, APIs, runtime persistence, helper execution, Evidence Layer write, production EvidenceItem creation, Review Queue runtime, production case creation, production analysis_run creation, actual analysis execution, production Analysis Result creation, Source 11 runtime, FinalSummaryReport runtime, public/export/final-delivery runtime, provider/collector jobs, or Project Source files.

## B. Non-declaration Rule

The 9A-13 approval phrase is not a human declaration.

Codex-generated text is not a human declaration.

No human declaration is received or recorded by 9A-13.

The declaration may only be considered in a future phase if it is separately supplied as:

- explicit_human_message_later
- separately_governed_external_audit_note_later

## C. Codex Authority Boundary

Codex cannot fabricate human authority.

Codex cannot infer authority from approval phrases, "continue", "ready", commits, or project ownership assumptions.

Codex cannot accept manual-review responsibility on behalf of a user.

Codex cannot validate identity, employment, legal power, organizational delegation, or signature authenticity.

Codex can only classify whether later human-supplied text contains required safe structural components.

Presence/sufficiency classification is not identity validation, authority validation, responsibility acceptance, final authorization, or write permission.

## D. Safe Recognition Fields

A future recognition object or checklist should use safe labels only:

- declaration_source_kind
- declaration_scope
- declared_authority_role_label
- authority_basis_label
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

Allowed role/basis labels remain non-PII and self-declared:

- self_declared_project_owner_role
- self_declared_designated_reviewer_role
- self_declared_organization_reviewer_role
- authority_basis_not_independently_validated
- external_audit_reference_required_later
- not_specified

These labels must not be described as verified authority.

## E. Recognition Outcomes

Allowed conservative outcomes:

- declaration_missing
- declaration_insufficient
- declaration_ambiguous
- declaration_present_for_docs_only_review
- privacy_issue_stop
- pause

Forbidden outcomes:

- authority_validated
- responsibility_accepted
- final_authorization_complete
- ready_for_write
- write_approved
- production_ready

`declaration_present_for_docs_only_review` means only that required textual components appear to be present. It does not validate identity, authority, responsibility, or write permission.

## F. Required Components

A future human-supplied declaration would need:

- explicit statement that the declaration comes from a human
- safe declared role label
- safe authority-basis label
- explicit statement accepting responsibility for manual review
- explicit warning_count acknowledgment
- explicit human_review_required acknowledgment
- explicit no_automatic_trust_upgrade acknowledgment
- blocker review statement
- risk review statement
- input-lineage review statement
- raw/private/secret absence acknowledgment
- rollback / pause / revocation responsibility statement
- acknowledgment that final write authorization is still required
- acknowledgment that actual write is not authorized by the declaration
- acknowledgment that production EvidenceItem creation is not authorized by the declaration
- acknowledgment that the system is not ready for actual write

## G. Insufficiency And Stop Rules

Classify as missing, insufficient, ambiguous, privacy_issue_stop, or pause if:

- no separate human-supplied source exists
- the content was generated entirely by Codex
- only a phase approval phrase is supplied
- role label is missing
- authority-basis label is missing
- manual-review responsibility statement is missing or ambiguous
- required acknowledgments are missing
- blockers or risks are not addressed
- lineage status is absent
- raw/private/secret absence is not acknowledged
- rollback/pause responsibility is missing
- wording claims actual write, final authorization, production EvidenceItem readiness, or automatic trust upgrade
- wording attempts to authorize production case, analysis_run, Analysis Result, Source 11, FinalSummaryReport, or public delivery
- wording contains real-person PII or secrets
- scope is ambiguous
- the declaration is presented as a route/UI/runtime trigger
- any unresolved blocker remains

## H. Privacy Rule

The recognition design must not request or store:

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

Use safe role labels only.

## I. Actual-write Separation

This contract does not approve actual write.

This contract does not approve production EvidenceItem creation.

This contract does not validate authority.

This contract does not accept responsibility.

This contract does not perform final write authorization.

Even after a future declaration-recognition test phase, actual write would still require a later exact approval phrase, a separately supplied human declaration, blocker/risk/lineage/privacy review, rollback/pause/revocation plan, and separate final write authorization.

## J. Contract Decision

9A-13 is a docs-only declaration-recognition design. It selects a future tests-only safety contract gate and keeps all write, production, authority-validation, responsibility-acceptance, and final-authorization boundaries closed.
