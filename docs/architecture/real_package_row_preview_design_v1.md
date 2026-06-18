# Real Package Row Preview Design v1

Status: architecture design draft

Scope: future Phase 6N/6O real package row preview runtime after Phase 6L synthetic fixture row-reader dry-run

This document is design-only. It does not implement real package row preview runtime, row parsing, evidence import, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector execution, real API calls, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, official API providers, vendor API providers, or real LLM integration.

## 1. Purpose

Real package row preview is a future safety step that may allow Sentigraph to read a tiny redacted sample from an approved local Evidence Export v1 package for reviewer inspection only.

It is considered only after the synthetic fixture row-reader dry-run has passed. The goal is to verify the row shape, redaction behavior, privacy blocking, and future staging-readiness of a controlled local package without importing rows or treating provider output as truth.

This design exists so the later runtime can be implemented conservatively, with explicit human opt-in and strong stop conditions before any real package row is read.

## 2. Non-Goals

Real package row preview is not:

- evidence import,
- Evidence Layer write,
- production case creation,
- review queue creation,
- dedup execution,
- analysis,
- Sandbox generation,
- public event page generation,
- B-end report generation,
- live collection,
- provider execution,
- collector execution,
- full package read,
- row scan beyond explicit max preview rows,
- full-web coverage,
- full-platform coverage,
- full-thread coverage,
- official verification upgrade,
- model calibration,
- report material,
- public display material.

## 3. Required Chain Before Preview

Real package row preview can only be considered after all of these exist:

- Analysis Request.
- Provider Result.
- Case Draft Handoff.
- Evidence Import Plan.
- Metadata-only Import Preview.
- Human Review Decision.
- `approve_import` decision.
- Dry-run Import Job.
- Execution Preflight.
- Synthetic Row Reader Dry-Run with passed or acceptable warn status.
- Explicit reviewer approval for real package row preview.

Every stage remains a gate. Later stages must not occur automatically because an earlier stage exists.

## 4. Preview Purpose

The preview is only for:

- verifying row shape,
- verifying redaction behavior,
- showing a tiny safe sample to a reviewer,
- detecting privacy blockers,
- confirming whether future staging import design is safe to consider.

The preview is not:

- evidence import,
- analysis input,
- public display,
- report material,
- final verification,
- model calibration,
- dataset summary,
- source authenticity proof,
- official platform verification.

Provider output is evidence, not truth.

## 5. Package Eligibility

Allowed only for:

- local Evidence Export v1 package,
- selected public sample or controlled candidate public sample,
- validation errors equal 0,
- explicit coverage limitation present,
- privacy flags present,
- package README present,
- coverage note present,
- validation report present,
- manifest present,
- explicit human row preview decision present.

Blocked if:

- validation errors are greater than 0,
- coverage note is missing,
- validation report is missing,
- manifest is missing,
- privacy flags are missing,
- package claims full-web, full-platform, or full-thread coverage,
- raw identity fields are known present,
- private messages or non-public content are possible,
- package path is outside the allowed local package root,
- package role is unknown or unsafe,
- reviewer did not approve row preview,
- package source is live session, cookie, or browser-profile based without exported privacy flags,
- package points to a live system instead of a stable local export.

## 6. Max-Row Rule

The first runtime must use:

- `max_rows <= 20`,
- default `max_rows = 10`,
- line-by-line streaming,
- immediate stop after `max_rows`,
- immediate stop after privacy stop,
- no full dataset scan,
- no aggregate conclusion from the preview sample.

The runtime must not read beyond the explicit cap to compute totals, sample proportions, sentiment distribution, source distribution, author statistics, or any other aggregate.

## 7. Output Boundaries

Every preview output must clearly state:

- preview rows are not imported,
- preview rows are not representative,
- preview rows do not prove full coverage,
- preview rows are redacted,
- preview rows are for reviewer safety inspection only,
- preview rows are not analysis input,
- preview rows are not report material,
- future staging import still requires a separate phase and a separate decision.

## 8. Reviewer Decision Requirements

The reviewer must explicitly acknowledge:

- the package is local and selected,
- the package is not full-web coverage,
- the package is not full-platform coverage,
- the package is not official verification,
- the preview will read at most the configured row cap,
- the preview will not import rows,
- the preview will not generate analysis or reports,
- any privacy stop blocks future import until review.

## 9. Future Runtime Shape

A future runtime should:

- read only a selected local package path already checked by execution preflight,
- verify manifest, validation report, coverage note, and privacy flags before opening row files,
- open only the allowed evidence row file,
- stream rows line by line,
- produce redacted preview rows,
- quarantine rows with forbidden fields when values can be withheld,
- reject malformed or unsafe rows,
- stop immediately on severe privacy violation,
- store an append-only preview result.

It must not:

- open unrelated package files,
- scan the full package,
- log raw rows,
- return forbidden values,
- import rows,
- write Evidence Layer records,
- create production case records,
- run analysis,
- generate reports.

## 10. Boundary Language

Use:

- real package row preview,
- redacted sample,
- reviewer safety inspection,
- privacy stop,
- quarantine,
- rejected invalid row,
- no import,
- no analysis,
- provider output is evidence, not truth,
- selected / controlled public sample.

Avoid:

- full dataset scan,
- automatic import completed,
- official verified,
- real-time crawl,
- report generated,
- case completed,
- analysis ready.

## 11. Ready-State Recommendation

Current decision after this design:

- `ready_for_phase_6N_real_package_row_preview_runtime_limited`

Recommended next step:

- Implement only a limited runtime after explicit review, keeping max rows at 20 or less, default 10, redacted output only, no import, and no analysis.
