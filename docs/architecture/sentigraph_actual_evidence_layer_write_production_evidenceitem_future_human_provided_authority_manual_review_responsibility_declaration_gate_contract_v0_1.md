# Sentigraph Future Human-provided Authority / Manual-review Responsibility Declaration Gate Contract v0.1

## A. Contract Purpose

This contract defines the inactive future 9A-13 docs-only declaration gate. Its purpose is to shape, if separately approved later, how Sentigraph could recognize whether a human outside Codex has supplied an explicit authority and manual-review responsibility declaration before any later final write authorization discussion.

This contract does not approve implementation now. It does not authorize actual write, production EvidenceItem creation, helper execution that writes, runtime human authority validation, runtime manual review responsibility acceptance, final write authorization, Review Queue runtime, production case, production analysis_run, actual analysis execution, production Analysis Result, Source 11, FinalSummaryReport, public/export/final delivery, provider/collector jobs, real package reads, raw identity exposure, or real human PII collection in repo docs.

## B. Inactive Future Phrase

Inactive future phrase:

`APPROVE_9A_13_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_GATE_DOCS_ONLY`

This phrase may only be used in a future prompt for a docs-only human-provided declaration gate. It must not authorize actual write, a write-permitting authorization object, runtime human authority validation, runtime manual review responsibility acceptance, final write authorization, production EvidenceItem creation, Review Queue runtime, production case, production analysis_run, production Analysis Result, Source 11, FinalSummaryReport, or public delivery.

## C. Future Allowed Scope

If separately approved later, 9A-13 may:

- remain docs-only
- define declaration-gate recognition/design only
- define a future human-provided declaration recognition checklist
- define required declaration fields
- define allowed safe labels and forbidden PII
- define that the user/human must explicitly provide an authority/responsibility statement outside Codex-generated text
- define that Codex can only classify whether the declaration text is present, sufficient, insufficient, or blocked
- define declaration insufficiency blockers

## D. Future Forbidden Scope

Future 9A-13 must not:

- perform actual Evidence Layer write
- execute helper code that writes
- create a persisted Evidence Layer record
- create production EvidenceItem
- create a write authorization object that permits write
- validate human authority in runtime
- accept manual review responsibility in runtime
- perform final write authorization
- use Review Queue runtime
- create production Review Queue item
- create production case
- create production analysis_run
- start actual analysis execution
- authorize or create production Analysis Result
- call Source 11 runtime
- call FinalSummaryReport runtime
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final delivery
- call provider/collector jobs
- inspect private collector source
- read real exchange/package directories
- parse production package rows
- perform additional row parsing
- expose raw rows/comments/identities
- read or expose secrets
- collect real human PII in repo docs

## E. Future Declaration Recognition Sketch

If later approved, docs may define expected safe declaration components such as:

- declaration_source = explicit_human_message_or_external_audit_note_later
- human_authority_identity_label = safe role label only
- authority_basis_label = safe role / project-owner / responsible-reviewer label
- manual_review_responsibility_label = explicit human acceptance required later
- warning_count_acknowledgment = required
- human_review_required_acknowledgment = required
- no_automatic_trust_upgrade_acknowledgment = required
- blocker_review_status = required
- risk_review_status = required
- lineage_review_status = required
- raw_private_secret_absence_acknowledgment = required
- rollback_pause_responsibility = required
- final_write_authorization_still_required = true
- actual_write_authorized = false
- production_evidenceitem_creation_authorized = false
- ready_for_actual_write = false

The recognition sketch is not a declaration. It is only a future docs-only checklist shape.

## F. Declaration Source Rule

A future declaration must be supplied by a human outside Codex in a later separate step.

Codex must not fabricate the declaration.

Codex must not infer authority from the user saying "continue".

Codex must not infer authority from a docs-only gate approval phrase.

Codex may only classify whether a provided declaration is present, sufficient, insufficient, or blocked under the future gate's rules.

## G. Declaration Insufficiency Blockers

A future declaration should be insufficient or blocked if:

- authority is missing
- manual review responsibility is missing
- warning_count acknowledgment is missing
- human_review_required acknowledgment is missing
- no_automatic_trust_upgrade acknowledgment is missing
- blocker review status is missing
- risk review status is missing
- lineage review status is missing
- raw/private/secret absence acknowledgment is missing
- rollback/pause responsibility is missing
- any real human PII is requested or stored
- any raw rows/comments/identities are included
- any secret, token, cookie, session, salt, password, or `.env` value appears
- any production EvidenceItem creation claim appears
- any actual write readiness claim appears
- any final write authorization claim appears

## H. Actual Write Remains Separate

Passing a future 9A-13 declaration gate would not permit actual write.

Any later actual-write phase must be separately approved and must include explicit human authority, a human acceptance step for manual review responsibility, warning/manual-review acknowledgments, no automatic trust upgrade, blocker clearance or pause, risk classification, input lineage verification, raw/private/secret absence, audit/rollback/revocation plan, final write authorization, and a stop-before-write rule for any unresolved blocker.

## I. Relationship To Product Surfaces

The review console may remain a boundary display only. It must not expose write buttons, approve-write CTAs, final-authorization CTAs, production EvidenceItem creation, or customer/public claims.

Recording and video work remain outside this gate.

## J. Contract Decision

9A-13 is only an inactive future docs-only human-provided authority / manual-review responsibility declaration gate. It is not implementation approval, not runtime authority validation, not runtime responsibility acceptance, not final authorization, and not actual-write approval.
