# Evidence Review Workflow

Last updated: 2026-05-26

Sentigraph now includes a lightweight human review queue for normalized evidence that is low-trust, unverified, duplicated, missing source context, screenshot/transcription-based, or otherwise flagged by the Evidence Layer. This workflow is for human review only. It does not use AI to verify authenticity and it does not fetch URLs, scrape pages, call real APIs, or call real LLM APIs.

## Purpose

The review queue helps analysts separate usable evidence from weak, duplicate, or unsupported submissions before running offline deterministic analysis. Evidence can remain stored for audit and provenance while being excluded or down-weighted from analysis decisions.

Queue candidates include evidence with:

- `verification_status` containing `unverified` or `needs_review`
- `trust_label` of `low` or `unverified`
- `provenance_type=screenshot_transcription`
- missing source URL
- `duplicate_count > 1`
- missing user attestation when attestation is required
- non-empty `risk_flags`

Official API evidence is normally not queued unless it has extra risk flags.

## Review Statuses

- `not_reviewed`: no explicit human decision has been applied.
- `review_needed`: the item has trust, provenance, duplicate, or source-context flags.
- `approved`: a reviewer accepted the item for use.
- `rejected`: the item remains stored but is excluded from analysis by default.
- `marked_weak`: the item remains usable but is clearly labeled weak evidence.
- `needs_more_source`: the item should get better source context before being trusted.
- `duplicate_merged`: the item is part of a duplicate group and should not inflate analysis counts.

## Review Decisions

- `approve`: sets `review_status=approved` and keeps the item usable.
- `reject`: sets `review_status=rejected`, records rejection flags, and excludes the item from default analysis and representative comments.
- `mark_weak`: keeps the item usable while preserving a low-trust warning.
- `request_more_source`: keeps the item visible but marks it as needing better source evidence.
- `merge_duplicate`: keeps duplicate grouping while preserving the duplicate-collapse behavior.
- `reset_review`: returns the item to computed default review status based on its trust/provenance flags.

## Review History / Audit Timeline

Every review decision appends an `EvidenceReviewHistoryEntry` to the evidence item. The history is append-only: old decisions are not overwritten when a later reviewer changes the current `review_status`.

Each history entry records:

- previous status and new status
- decision, reason code, reviewer label, reviewed time, and optional reviewer note
- trust label and verification status before/after the decision
- analysis effect: `included_in_analysis`, `excluded_from_analysis`, `weak_evidence`, or `duplicate_collapsed`
- safe-mode flags showing no AI authenticity verification, no URL fetch, and no secret exposure

The audit timeline endpoints are:

- `GET /api/v1/cases/{case_id}/evidence/{evidence_id}/review-history`
- `GET /api/v1/cases/{case_id}/evidence/review-timeline`
- `GET /api/v1/cases/{case_id}/evidence/review-audit-summary`

Reviewer notes are treated as plain text and secret-like values are redacted before they appear in stored history or API responses. The audit trail records human decisions only; it is not platform official verification and does not mean the evidence is true.

## Analysis Behavior

When a case has `raw_comments`, `case_raw_data` still wins and YouTube raw-data analysis remains unchanged. When a case has only `evidence_items`, analysis uses eligible normalized evidence. Rejected evidence is excluded from default analysis counts and representative comments. Duplicate evidence remains collapsed so repeated uploads or repeated manual submissions cannot directly inflate sentiment, topic, or risk counts.

Marked-weak and needs-more-source evidence can still appear in analysis, but the report surfaces warnings that parts of the evidence are low-trust or unreviewed.

## Screenshot And User-Submitted Evidence

Screenshots, pasted transcriptions, and manually typed claims are never automatically verified. Source URLs and user attestation improve context, but they still do not guarantee that the content is true. The UI should always preserve this distinction:

- official source provenance is not a truth guarantee
- screenshot transcription is unverified by default
- user upload/manual evidence requires human review
- AI is not used for authenticity verification in this MVP

## Safety Boundaries

The review queue is local, deterministic, and evidence-metadata based. It must not:

- fetch or scrape URLs
- call real search/platform APIs
- call real LLM APIs
- store API keys, cookies, tokens, or `.env` values
- integrate MediaCrawler
- create individual persuasion profiles or account-level influenceability scores
- automatically execute moderation, communication, or platform actions

Reviewer labels, if used, are for audit and dedup control only.
