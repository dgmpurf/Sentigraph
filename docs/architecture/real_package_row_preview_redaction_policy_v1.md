# Real Package Row Preview Redaction Policy v1

Status: architecture redaction policy draft

Scope: future redacted preview of a tiny local Evidence Export v1 package sample

This document is design-only. It does not implement row reading, row parsing, evidence import, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, reporting, provider execution, collector jobs, real API calls, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, official API providers, vendor API providers, or real LLM integration.

## 1. Policy Goal

The goal is to allow a future reviewer to inspect a tiny safe sample of package row shape without exposing raw identity fields, private content, secrets, or anything that would imply import, verification, analysis, or full coverage.

The preview is a reviewer safety inspection artifact only.

## 2. Allowed Preview Fields

Allowed fields:

- `row_index`
- `evidence_type`
- `platform`
- `source_url` if safe
- `title_preview`
- `body_text_preview`
- `created_at`
- `language`
- counts if non-sensitive
- governance defaults

Allowed governance defaults:

- `review_status=review_needed`
- `verification_status=source_url_provided_unverified`
- `trust_label=medium_low`
- `analysis_included=false`

The preview may include safe categories such as quarantine reason names, blocker categories, and redacted field names. It must not include forbidden values.

## 3. Forbidden Preview Fields

Forbidden preview fields:

- `raw_author_id`
- `raw_author_name`
- `author_name` unless already anonymized and allowed by future policy
- `author_id` unless already anonymized and allowed by future policy
- `profile_url`
- `avatar_url`
- `private_message`
- `cookie`
- `token`
- `session`
- browser profile path
- `password`
- email address if detected
- phone number if detected
- precise personal address
- minors' personal details
- direct personal identifiers
- full raw row
- raw platform account handle if not already anonymized by policy

Forbidden fields must be omitted, redacted, quarantined, or trigger privacy stop depending on severity.

## 4. Body Preview Rule

`body_text_preview` must:

- be at most 160 characters,
- strip line breaks,
- strip tabs and repeated whitespace,
- strip handles if detected where possible,
- avoid raw usernames,
- avoid private message content,
- avoid full row dumps,
- avoid direct personal identifiers,
- preserve enough context for reviewer safety inspection only.

If a body cannot be safely previewed, the row must be quarantined or rejected.

## 5. Title Preview Rule

`title_preview` must:

- be short,
- strip line breaks,
- avoid raw usernames and private identifiers,
- avoid credential-like strings,
- avoid private message content.

If a title contains unsafe personal or secret-like content that cannot be safely redacted, the row must be quarantined, rejected, or privacy-stopped.

## 6. Source URL Rule

`source_url` may be shown only if:

- it is a public content URL,
- it is not a profile URL,
- it is not a private message URL,
- it does not include session-like query parameters,
- it does not include access tokens,
- it does not include tracking parameters that expose personal information.

If a URL is unsafe, show only a redacted URL category or omit it.

## 7. Counts Rule

Non-sensitive counts may be shown, for example:

- like count,
- reply count,
- share count,
- view count,
- repost count.

Counts must not be used to infer full-package statistics from the preview. The UI must state that the sample is not representative.

## 8. Quarantine Behavior

Row outcomes:

- `accepted_for_preview`: row can be safely sanitized and displayed.
- `quarantined`: forbidden fields are present, but values can be withheld safely.
- `rejected`: invalid JSON, malformed structure, or unsafe content that cannot be sanitized.
- `privacy_stop`: severe privacy violation requiring immediate stop.

Quarantine output may include:

- row index,
- reason code,
- forbidden field names,
- safe category labels.

Quarantine output must not include:

- forbidden values,
- raw identity values,
- private message content,
- secrets,
- full raw row.

## 9. Rejection Behavior

Reject if:

- invalid JSON,
- unsupported row type,
- row cannot be parsed safely,
- row cannot be sanitized safely,
- row has structural ambiguity that could leak forbidden values.

Rejection output may include:

- row index,
- reason code,
- parser category,
- safe summary.

Rejection output must not include raw row text.

## 10. Privacy Stop Behavior

Trigger privacy stop if:

- severe direct personal identifier appears,
- private message content appears,
- secret-like value appears,
- non-public content marker appears,
- browser/session/profile artifact appears,
- repeated forbidden-field violations suggest package privacy flags are unreliable.

Privacy stop must:

- stop reading immediately,
- not return the violating value,
- record only row index and blocker category,
- set `status=privacy_stop`,
- block future import until security/privacy review.

## 11. Redacted Preview Row Shape

Suggested preview row:

```json
{
  "row_index": 0,
  "status": "accepted_for_preview",
  "evidence_candidate": {
    "evidence_type": "comment",
    "platform": "selected_public_sample",
    "source_url": "https://example.invalid/public-item",
    "title_preview": "Redacted title preview",
    "body_text_preview": "Redacted body preview for reviewer safety inspection only.",
    "created_at": "2026-06-18T00:00:00Z",
    "language": "en"
  },
  "governance_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "analysis_included": false
  },
  "privacy_check": {
    "passed": true,
    "forbidden_fields_detected": []
  }
}
```

The example is illustrative. Future runtime output must not include raw forbidden values.

## 12. Boundary Language

Use:

- redacted sample,
- reviewer safety inspection,
- privacy stop,
- quarantine,
- rejected invalid row,
- no import,
- no analysis,
- provider output is evidence, not truth.

Avoid:

- full row dump,
- official verified,
- full dataset scan,
- analysis ready,
- report generated,
- case completed.
