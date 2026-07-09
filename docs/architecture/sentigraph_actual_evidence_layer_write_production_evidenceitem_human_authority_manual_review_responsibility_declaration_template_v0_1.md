# Sentigraph Actual Evidence Layer Write / Production EvidenceItem Human Authority / Manual Review Responsibility Declaration Template v0.1

## A. Template Purpose

This template defines a safe, non-authorizing declaration shape for future discussion. It is docs-only and must not be treated as runtime input, authority validation, responsibility acceptance, final authorization, actual Evidence Layer write approval, or production EvidenceItem creation approval.

Codex cannot fabricate human authority, cannot accept manual review responsibility on behalf of the user, and cannot convert this template into write authorization.

## B. Non-authorizing Template

```json
{
  "declaration_schema": "sentigraph_actual_evidence_layer_write_human_authority_declaration_v0_1",
  "declaration_scope": "docs_only_declaration_gate",
  "human_authority_identity_label": "not_validated_by_codex",
  "authority_basis": "not_validated_by_codex",
  "manual_review_responsibility_label": "not_accepted_by_codex",
  "warning_count_acknowledgment": "required_later",
  "human_review_required_acknowledgment": "required_later",
  "no_automatic_trust_upgrade_acknowledgment": "required_later",
  "blocker_review_status": "required_later",
  "risk_review_status": "required_later",
  "lineage_review_status": "required_later",
  "raw_private_secret_absence_acknowledgment": "required_later",
  "rollback_pause_responsibility": "required_later",
  "final_write_authorization_still_required": true,
  "actual_write_authorized": false,
  "production_evidenceitem_creation_authorized": false,
  "ready_for_actual_write": false
}
```

This template is not a write authorization object. It does not validate human authority, does not accept responsibility, does not permit helper execution, and does not permit write.

## C. Field Meanings

- declaration_schema: identifies the future declaration shape only.
- declaration_scope: must remain `docs_only_declaration_gate` for this phase.
- human_authority_identity_label: safe role/status label only; no real person PII.
- authority_basis: safe status label only; no credentials, secrets, or private proof.
- manual_review_responsibility_label: safe status label only; not a runtime acceptance.
- warning_count_acknowledgment: required later before any write discussion.
- human_review_required_acknowledgment: required later before any write discussion.
- no_automatic_trust_upgrade_acknowledgment: required later before any write discussion.
- blocker_review_status: required later; no blockers are cleared by this template.
- risk_review_status: required later; no risk is accepted by this template.
- lineage_review_status: required later; no source lineage is verified by this template.
- raw_private_secret_absence_acknowledgment: required later; no raw content is inspected here.
- rollback_pause_responsibility: required later; no operational responsibility is accepted here.
- final_write_authorization_still_required: must be true.
- actual_write_authorized: must be false.
- production_evidenceitem_creation_authorized: must be false.
- ready_for_actual_write: must be false.

## D. Allowed Placeholder Values

Allowed safe placeholder values:

- not_validated_by_codex
- not_accepted_by_codex
- required_later
- not_authorized
- human_required_later
- blocked_until_separate_final_authorization

These labels are intentionally non-authorizing.

## E. Forbidden Content

This template must not contain:

- real raw rows
- raw comments
- raw author IDs/names
- private messages
- secrets/tokens/cookies/sessions/passwords/salts
- `.env` values
- arbitrary filesystem paths
- production package row contents
- evidence_items.jsonl contents
- evidence_items.csv contents
- source_manifest row contents
- collection_log row contents
- write execution payload
- route/API/frontend trigger payload
- production case payload
- production analysis_run payload
- production Analysis Result payload
- Source 11 payload
- FinalSummaryReport payload
- export/download/public/final-delivery payload
- response_text
- generated_public_message
- target_user_list
- persuasion_score
- truth_score
- official_verified
- prediction_probability
- psychological_profile
- personality_diagnosis

## F. Use Restrictions

This template may be referenced only as docs-only planning material.

It must not be loaded by runtime code, sent to an API, used as a route payload, stored as a runtime permission object, transformed into a write authorization object, attached to a production EvidenceItem, attached to a production case, attached to a production analysis_run, attached to production Analysis Result creation, sent to Source 11, sent to FinalSummaryReport, or exposed through export/download/public/final delivery.

## G. Future Gate Separation

A future 9A-9 tests-only gate may verify this template remains non-authorizing. Even if such tests pass, actual write would still require a later separate exact approval phrase, explicit human authority provided by a human outside Codex, a human acceptance step for manual review responsibility, warning/manual-review/no-upgrade acknowledgments, blocker and risk classification, source lineage verification, raw/private/secret absence, rollback/pause planning, and final write authorization.
