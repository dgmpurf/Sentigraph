# Evidence Trust and Deduplication

Last updated: 2026-05-25

Sentigraph now treats evidence reliability as an explicit part of the Evidence Layer. The goal is conservative analysis: user-provided material, screenshots, manual URL entries, CSV/Excel rows, official API records, public-parser fixtures, and mock fixtures can all be normalized, but they are not treated as equally verified.

## Trust Boundaries

- Official API evidence is labeled `official_api`, `verified_by_official_api`, and high trust for source provenance. This is still not a guarantee that every claim inside the content is true.
- Reviewed public-parser evidence is labeled `public_parser` and medium/high trust because the source page structure is known, but it still requires human review for interpretation.
- Manual URL evidence with a source URL and user attestation is medium trust and `source_url_provided_unverified`.
- CSV/Excel or other user-uploaded evidence is low/medium at best unless it includes source context and user attestation.
- Screenshot or transcribed evidence is always `screenshot_unverified`; Sentigraph never automatically verifies screenshots.
- Search Discovery candidates are leads only. They are not evidence until a user reviews and attaches text through Manual URL Evidence, CSV/Excel import, or a reviewed parser path.
- Mock fixtures remain deterministic demo data and must not be described as real-world evidence.

## Provenance Fields

Each `EvidenceItem` can now carry:

- `provenance_type`
- `verification_status`
- `trust_score`
- `trust_label`
- `source_url_present`
- `source_url`
- `source_platform_claim`
- `source_capture_method`
- `submitted_by_label` / `submitter_hash`
- `submitted_at`
- `user_attestation_required`
- `user_attestation_text`
- `verification_notes`
- `risk_flags`

These fields are for source review and abuse/dedup auditing only. They must not be used to create individual persuasion profiles, account-level influenceability scores, or targeting lists.

## Deduplication

Sentigraph computes deterministic hashes for each item:

- `content_hash`
- `normalized_content_hash`
- `canonical_url_hash`
- `duplicate_group_id`

Normalization trims whitespace, lower-cases comparable text, removes common tracking URL parameters such as `utm_*`, and combines platform/source/evidence type/text/URL into a stable hash. Within a case, exact duplicate text/URL submissions are collapsed into one unique evidence item with `duplicate_count` and `duplicate_group_size`.

Repeated submissions remain visible as repetition signals, but they do not directly inflate sentiment, topic, or risk counts. Analysis uses the unique evidence set by default.

## Human Review Queue

The Evidence Review Queue is a human review workflow layered on top of trust and dedup metadata. It is not an AI authenticity verifier.

Items enter the queue when they are low-trust, unverified, screenshot/transcription-based, missing a source URL, missing required user attestation, part of a duplicate group, or carrying risk flags such as secret-like text, suspiciously short content, or raw HTML/script-like input.

Review decisions:

- `approve`: keep the item usable and mark it reviewed.
- `reject`: keep the normalized item stored but exclude it from default analysis and representative comments.
- `mark_weak`: keep the item usable while preserving a weak-evidence warning.
- `request_more_source`: keep the item visible but flag that stronger source context is needed.
- `merge_duplicate`: preserve duplicate grouping so the item does not inflate counts.
- `reset_review`: return to computed default review status.

Rejected evidence is excluded only from default analysis. It is not deleted, so an analyst can audit what was submitted and why it was rejected. Screenshot or transcribed evidence is never called verified unless a separate trusted source confirms it.

## User Attestation

Manual and uploaded evidence records require or record this attestation:

> I confirm I have the right to submit this public-opinion evidence for analysis.

If attestation is missing, Sentigraph still stores the normalized item when product flow allows it, but marks it with `user_attestation_missing`, lowers trust, and sets review-needed status.

## Malicious Or Low-Quality Input

Sentigraph adds review flags for:

- missing source URL
- screenshot transcription
- missing timestamp
- possible secret-like text
- high duplicate count
- unsupported platform claim
- suspiciously short content
- raw HTML/script-like text

Secret-like text is redacted. HTML/script-like input is treated as plain text and never executed. Uploaded raw files are not persisted by default; only normalized `EvidenceItem` records and safe metadata are stored.

## No Truth Guarantee

Trust labels describe source/provenance confidence, not truth. A high-trust official API record proves that the item came through the official API path; it does not prove that claims made by users inside the content are accurate. Real-world action still requires human, policy, and legal review.
