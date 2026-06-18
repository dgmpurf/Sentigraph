# Real Package Row Preview Safety Gate v1

Status: architecture safety contract draft

Scope: future real package row preview gate for local Evidence Export v1 packages

This document is design-only. It does not implement row preview runtime, row parsing, evidence import, Evidence Layer writes, case creation, review queue creation, dedup, analysis, reporting, provider execution, collector jobs, real API calls, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, vendor API providers, official API providers, or real LLM integration.

## 1. Preflight Gate

The preview runtime may proceed only if the latest execution preflight confirms:

- package reference exists,
- package path is local,
- manifest file name exists,
- validation report file name exists,
- coverage note file name exists,
- privacy flags are present,
- row files were not opened during preflight,
- row files were not parsed during preflight,
- no import was performed,
- no analysis was generated,
- no report was generated.

Block if preflight is missing, blocked, stale, superseded, or inconsistent with the selected package.

## 2. Human Decision Gate

The reviewer must explicitly approve real package row preview. Existing `approve_import` is not enough by itself.

The approval must acknowledge:

- selected local package only,
- max row cap,
- redacted preview only,
- no import,
- no Evidence Layer write,
- no case creation,
- no analysis,
- no report,
- provider output is evidence, not truth.

Block if reviewer approval is missing, stale, superseded, or ambiguous.

## 3. Package Path Gate

The runtime must validate:

- package path is inside an allowed local package root,
- no path traversal is present,
- package path resolves to the same package inspected by preflight,
- package path is not a live session path,
- package path is not a browser profile path,
- package path is not a credential or configuration directory.

Hard blockers:

- package path traversal,
- package path outside allowed root,
- package path points to private collector runtime that has not been exported as an Evidence Export package,
- package path points to a live account/session/profile location.

## 4. Manifest / Validation / Coverage Gate

Before opening any row file, the runtime must verify:

- package manifest exists,
- validation report exists,
- coverage note exists,
- validation errors equal 0,
- validation status is passed or warn,
- coverage limitations are explicit,
- package does not claim full-web coverage,
- package does not claim full-platform coverage,
- package does not claim full-thread coverage,
- package role is selected public sample or controlled candidate public sample.

Hard blockers:

- missing manifest,
- missing validation report,
- missing coverage note,
- validation errors greater than 0,
- unsafe package role,
- full-web/full-platform/full-thread overclaim.

## 5. Privacy Flag Gate

The runtime must require exported privacy flags showing that raw identity and private fields were removed or excluded.

Required privacy flags:

- raw author identifiers removed,
- raw author names removed or anonymized,
- profile URLs removed,
- private messages excluded,
- non-public content excluded,
- secrets excluded.

Hard blockers:

- missing privacy flags,
- flags indicate possible private content,
- flags indicate raw identity values may remain,
- package source is cookie/session/profile based without exported privacy checks.

## 6. Row-Level Privacy Gate

Each row must be checked before preview output is generated.

Hard blockers:

- `raw_author_id` present,
- `raw_author_name` present,
- `profile_url` present,
- `private_message` present,
- password/token/cookie/session-like string present,
- non-public content marker,
- malformed row that cannot be safely sanitized,
- any attempt to import rows now,
- any attempt to generate analysis or report now.

If the row contains forbidden fields but the values can be fully withheld, the row may be quarantined instead of accepted for preview.

If a severe privacy violation appears, trigger privacy stop.

## 7. Redaction Gate

Preview output must contain only allowed redacted fields.

The runtime must:

- strip or omit forbidden fields,
- truncate text previews,
- remove line breaks,
- avoid raw usernames and handles where detected,
- avoid direct personal identifiers,
- avoid private message content,
- avoid full row dumps.

Block if a safe preview cannot be produced without leaking forbidden values.

## 8. Logging Gate

Logging rule:

- never log full raw row,
- never log forbidden values,
- never log secrets,
- never log private message content,
- log only row index, blocker categories, redacted field names, counts, status, and safe package references.

Allowed log fields:

- `preview_run_id`,
- `request_id`,
- `preflight_id`,
- `import_job_id`,
- `row_index`,
- blocker category,
- status,
- count summary,
- redacted field names.

## 9. UI Display Gate

The UI must show:

- real package row preview only,
- redacted preview only,
- no import,
- no analysis,
- no report,
- preview rows are not representative,
- provider output is evidence, not truth,
- selected / controlled public sample boundary,
- coverage limitation,
- privacy stop if triggered.

The UI must not show:

- raw rows,
- raw author identifiers,
- raw author names,
- profile URLs,
- private messages,
- tokens,
- cookies,
- sessions,
- browser profile paths,
- full dataset summaries inferred from the tiny preview.

## 10. Stop / Privacy Stop Gate

Privacy stop behavior:

- stop reading immediately,
- do not return the raw violating value,
- write only blocker category and row index,
- set `status=privacy_stop`,
- set `privacy_stop_triggered=true`,
- set `can_import_now=false`,
- block future import until privacy/security review.

Privacy stop does not delete the package. It prevents the preview result from being treated as safe and forces a separate human/security review.

## 11. Hard Blocker Summary

Hard blockers include:

- raw author id present,
- raw author name present,
- profile URL present,
- private message present,
- password/token/cookie/session-like string present,
- non-public content marker,
- malformed row that cannot be safely sanitized,
- package path traversal,
- row count exceeds limit without explicit cap,
- any attempt to import rows now,
- any attempt to generate analysis/report now,
- missing manifest,
- missing validation report,
- missing coverage note,
- validation errors greater than 0,
- missing privacy flags,
- reviewer did not approve row preview.

## 12. Future Implementation Requirement

The future runtime should fail closed. Any ambiguous privacy, source, path, validation, or reviewer decision state must block preview rather than attempting to continue.
