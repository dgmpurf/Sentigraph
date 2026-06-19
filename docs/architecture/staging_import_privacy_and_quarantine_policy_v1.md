# Staging Import Privacy And Quarantine Policy v1

Status: architecture policy draft

Scope: future privacy, quarantine, rejection, logging, and recovery rules for review-only case staging import

This document is design-only. It does not implement runtime code, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, reports, Sandbox fixtures, provider execution, live collection, real APIs, URL fetching, scraping, browser automation, or real LLM integration.

## 1. Purpose

Future staging import must fail closed when candidate rows contain private, secret-like, or unsafe data.

The staging layer is a review-only governance area, not a place to preserve raw private data. Provider output is evidence, not truth, and unsafe evidence must not be promoted by accident.

## 2. Privacy Blockers

The following categories are privacy blockers:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- `private_message`
- token-like content
- cookie-like content
- session-like content
- password-like value
- email
- phone
- precise address
- minor personal details
- non-public content marker

The future runtime should treat these as categories, not as values to display.

## 3. Quarantine Behavior

A row with removable forbidden fields may be quarantined when the system can safely avoid storing the forbidden values and preserve only a category-level reason.

Quarantined rows:

- are not analysis-included,
- are not report-visible,
- are not public-visible,
- are not Sandbox-visible,
- do not enter dedup as analysis candidates,
- remain visible for audit only through safe metadata.

Quarantine summaries must not include raw values. They should include:

- `row_index`,
- category codes,
- safe reason code,
- package name,
- staging import id,
- timestamp.

## 4. Privacy Stop Behavior

Severe private content, private messages, credentials, secret-like values, or systemic package contamination should trigger `privacy_stop`.

`privacy_stop` means:

- stop staging immediately,
- do not continue scanning rows for content display,
- do not write additional staged rows,
- do not create review queue items,
- do not run dedup,
- do not run analysis,
- do not generate reports or public outputs,
- require privacy/security review before any retry.

## 5. Rejection Behavior

Rows should be rejected when they cannot be safely staged.

Rejection reasons include:

- invalid JSON,
- malformed schema,
- missing required content fields,
- unsafe content that cannot be sanitized,
- path/source mismatch,
- unsupported package role,
- package hash mismatch,
- row count exceeds approved limit,
- review-only case mismatch.

Rejected rows are not staged for review and are never analysis-included.

## 6. Logging Rules

Logs must be safe by default.

Do not log:

- full raw rows,
- raw author identifiers,
- profile URLs,
- private messages,
- token values,
- cookie values,
- session values,
- password-like values,
- email values,
- phone values,
- precise addresses,
- browser profile paths,
- `.env` values,
- API keys,
- salts,
- credentials.

Log only:

- category codes,
- row indexes,
- counts,
- safe status,
- package name,
- import id,
- review case id,
- generic reason codes.

## 7. Recovery Rules

A `privacy_stop` requires privacy/security review.

Recovery should require:

- rollback of any partially staged rows,
- review of quarantine/rejection counts,
- a new human review decision,
- a new staging import id,
- explicit acknowledgement of coverage limitations,
- proof that no forbidden values are exposed in responses or logs.

Future staging retry must require a new review decision. It must not silently reuse a stale approval.

## 8. Audit And Rollback

Every staging import attempt should produce audit metadata, even when blocked.

Audit metadata should include:

- staging import id,
- review case id,
- request id,
- package name,
- source preview run id,
- import job id,
- reviewer label,
- timestamp,
- safe counts,
- privacy status,
- rollback id when applicable.

Rollback must be available before any future analysis inclusion can be considered.

## 9. Human-Readable Boundary

The UI should explain:

> Some rows may be quarantined or rejected for privacy and safety. Quarantine is audit-only. It does not mean the row is verified, analysis-ready, report-ready, public, or safe to use without human review.
