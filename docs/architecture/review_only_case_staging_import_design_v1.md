# Review-Only Case Staging Import Design v1

Status: architecture design draft

Scope: future staging import gate after Phase 6P review-only case runtime

This document is design-only. It does not implement staging import runtime, row parsing, evidence import, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, live collection, real APIs, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, official API providers, vendor API providers, or real LLM integration.

## 1. Purpose

The future staging import step moves sanitized candidate rows from an approved provider package path into an isolated review-only staging area.

It exists after a review-only case has been created. Its job is to prepare candidate evidence for later governance, review queue initialization, deduplication, audit, and rollback. It must not make any row analysis-ready.

## 2. Core Principle

Staging import is not production import.

Staging import is not analysis inclusion.

Staging import is not public case creation.

Staging import is not report generation.

Staging import is not official verification.

Provider output is evidence, not truth. A package that passes local structure checks is still a selected, unverified, coverage-limited evidence source until later human review, dedup, and promotion gates approve a narrower analysis scope.

## 3. Non-Goals

This design does not add:

- runtime implementation,
- row parsing,
- Evidence Layer writes,
- production case creation,
- automatic analysis,
- Sandbox fixture generation,
- public event generation,
- B-end report generation,
- provider execution,
- live collection,
- real LLM,
- trust upgrade.

It also does not authorize full-web, full-platform, or full-thread coverage claims.

## 4. Required Prior Chain

Staging import can only be considered after all of these exist and remain valid:

- Analysis Request exists.
- Provider Result exists.
- Case Draft Handoff exists.
- Evidence Import Plan exists.
- Metadata-only Import Preview exists.
- Human Review Decision `approve_import` exists and remains the latest effective decision.
- Dry-run Import Job exists.
- Execution Preflight exists.
- Synthetic Row Reader Dry-Run passed.
- Limited Real Package Row Preview passed or warned without `privacy_stop`.
- Review-only Case exists.
- Human reviewer explicitly approves staging import design / future staging execution.

If any upstream artifact is missing, stale, superseded, rejected, blocked, or privacy-stopped, staging import must not begin.

## 5. Staging Import Purpose

Staging import is only for:

- moving sanitized candidate rows into isolated review-only staging,
- initializing governance metadata,
- preparing for review queue and dedup in later phases,
- preserving audit and rollback readiness.

Staging import is not for:

- analysis,
- public display,
- report material,
- sentiment score update,
- risk score update,
- model calibration,
- official verification,
- full dataset representation.

## 6. Staging Container Model

A future staging area should be linked to one review-only case.

Minimum container fields:

- `review_case_id`
- `staging_import_id`
- `package_name`
- `import_job_id`
- `source_preview_run_id`
- `created_at`
- `status`
- `counts`
- `privacy_summary`
- `governance_defaults`
- `rollback`
- `audit`

The staging container should be append-only. A new staging attempt should create a new `staging_import_id` rather than silently overwriting prior records.

## 7. First MVP Staging Strategy

Recommended first runtime:

- require another explicit review before enabling any runtime,
- use `max_rows=20` for the first controlled runtime, or `max_rows=100` only after a separate review,
- stream rows rather than loading the full package into memory,
- fail closed on privacy violation,
- keep `analysis_included=false` for every accepted staged row,
- keep `public_visible=false`, `report_visible=false`, and `sandbox_visible=false`,
- keep quarantined rows visible for audit only,
- reject unsafe rows without exposing raw values,
- do not stage rejected rows for review,
- do not run analysis until review, dedup, and promotion gates complete.

The first MVP should prefer small, controlled local packages over large datasets. It should not perform full package import, live collection, URL fetching, provider execution, or automatic public output generation.

## 8. Relationship To Existing Evidence Layer

Staged evidence should either be stored separately or explicitly flagged as staging-only.

If a future implementation reuses existing case evidence storage, staged rows must be isolated by:

- `review_case_id`,
- `staging_import_id`,
- `review_status`,
- `analysis_included=false`,
- `public_visible=false`,
- `report_visible=false`,
- `sandbox_visible=false`,
- `promotion_status=pending`.

Production analysis must ignore staged evidence until a later promotion gate explicitly marks a reviewed, deduped, audited subset as analysis-ready.

## 9. Boundary Language

UI, logs, API responses, docs, and demo scripts should use:

- staging import,
- review-only case,
- evidence staging,
- `analysis_included=false`,
- `review_needed`,
- `source_url_provided_unverified`,
- `medium_low`,
- quarantine,
- `privacy_stop`,
- audit and rollback,
- provider output is evidence, not truth.

They must avoid:

- automatic import completed,
- production case created,
- official verified,
- full-web coverage,
- analysis completed,
- report generated,
- Sandbox generated,
- live crawl.

## 10. Future Phase Recommendation

Next phase should be Phase 6R: Staging Import Runtime with a tiny local fixture or controlled package.

Phase 6R should still block production case creation, Evidence Layer analysis inclusion, review queue creation, dedup, analysis, reports, Sandbox fixtures, public event pages, provider execution, collector execution, URL fetching, and real API calls.
