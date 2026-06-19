# Review-Only Case Design v1

Status: architecture design draft

Scope: future review-only case / staging container before any real Evidence import runtime

This document is design-only. It does not implement review-only case runtime, evidence import, row parsing, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, Strategy Lab output, forecast output, provider execution, collector jobs, real APIs, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, official API providers, vendor API providers, or real LLM integration.

## 1. Purpose

A review-only case is a quarantine and staging container for future manually imported Evidence rows.

It exists between a governed local Evidence Export package and any production / analysis-ready Sentigraph case. Its job is to hold staged evidence under governance defaults while reviewers inspect source coverage, privacy risk, trust, deduplication needs, and audit history.

A review-only case is not a production case. It is a safe place to prepare evidence for review before any row can affect risk scores, reports, public event pages, Sandbox output, or B-end materials.

## 2. Core Principle

A review-only case is:

- internal review only,
- governance-first,
- excluded from analysis by default,
- excluded from public and report surfaces by default,
- blocked from automatic promotion.

A review-only case is not:

- a production case,
- analysis-ready,
- public,
- officially verified,
- full-web coverage,
- full-platform coverage,
- report-ready,
- Sandbox-ready,
- Strategy Lab-ready,
- forecast-ready.

It cannot generate Sandbox fixtures, public event pages, B-end reports, Summary Reports, Strategy Lab outputs, Simulation Lab outputs, forecast output, or public-facing event material.

## 3. Non-Goals

This design does not add:

- Evidence import runtime,
- row parsing,
- Evidence Layer write,
- production case creation,
- automatic analysis,
- public event generation,
- B-end report generation,
- dedup runtime,
- review queue runtime,
- real LLM,
- provider execution,
- collector execution,
- URL fetching,
- scraping,
- official API provider integration,
- vendor API provider integration.

## 4. Why This Layer Is Needed

Provider output is evidence, not truth.

Package validation checks structure, safety metadata, coverage notes, and local contract compatibility. It does not prove that the rows are complete, officially verified, representative, or safe for direct scoring.

A review-only case is needed because:

- imported rows must not immediately affect risk scores,
- low-trust, unverified, selected-sample data needs governance before analysis,
- package validation is not official platform verification,
- coverage notes must travel with evidence before any interpretation,
- repeated or duplicated evidence must not amplify sentiment or risk,
- weak or rejected evidence must be excluded or warned before analysis,
- privacy blockers must be able to stop promotion,
- reviewers need a place to inspect staged data without contaminating the production case pool.

The layer prevents accidental promotion of provider package rows into analysis, public pages, Sandbox demos, B-end reports, or strategy recommendations.

## 5. Suggested Object Model

Future object shape:

```json
{
  "schema": "sentigraph_review_only_case_v1",
  "review_case_id": "review_case_20260619_example",
  "request_id": "req_20260619_example",
  "source_import_job_id": "manual_import_job_20260619_example",
  "source_preview_run_id": "real_package_preview_20260619_example",
  "created_at": "2026-06-19T00:00:00Z",
  "created_by": "local_reviewer",
  "status": "draft",
  "visibility": "internal_review_only",
  "analysis_included": false,
  "public_visible": false,
  "report_allowed": false,
  "sandbox_allowed": false,
  "strategy_lab_allowed": false,
  "package_reference": {
    "package_name": "example-package",
    "package_role": "selected_public_sample",
    "package_path": "docs/samples/example-package"
  },
  "coverage": {
    "coverage_level": "selected_public_sample",
    "not_full_web": true,
    "not_full_platform": true,
    "not_full_thread": true
  },
  "governance_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "dedup_required": true,
    "audit_required": true
  },
  "allowed_actions": [
    "inspect_package_metadata",
    "inspect_limited_redacted_row_preview"
  ],
  "blocked_actions": [
    "run_analysis",
    "generate_summary_report",
    "generate_sandbox_fixture",
    "generate_public_event_page",
    "generate_b_end_report",
    "run_strategy_lab"
  ],
  "promotion_requirements": [
    "no_privacy_blockers",
    "validation_errors_zero",
    "coverage_acknowledged",
    "dedup_completed",
    "review_queue_completed_or_threshold_met",
    "audit_timeline_present",
    "human_promotion_decision_recorded"
  ],
  "audit": {
    "created_from_preview": true,
    "append_only": true
  }
}
```

## 6. Default Governance Policy

Every review-only case must default to:

- `review_status = review_needed`
- `verification_status = source_url_provided_unverified`
- `trust_label = medium_low`
- `analysis_included = false`
- `public_visible = false`
- `report_allowed = false`
- `sandbox_allowed = false`
- `strategy_lab_allowed = false`
- `dedup_required = true`
- `audit_required = true`
- `coverage_warning_required = true`
- `low_trust_warning_required = true`

These defaults are conservative. A reviewer may later approve a promotion decision, but the default state must never be analysis-ready.

## 7. Future Allowed Actions

Inside a review-only case, future phases may allow:

- inspect package metadata,
- inspect validation and coverage summaries,
- inspect limited redacted row preview,
- stage rows in a future phase,
- initialize review queue in a future phase,
- mark evidence approved, weak, rejected, or needs more source in a future phase,
- run dedup in a future phase,
- view audit and coverage notes,
- rollback staged import before promotion,
- request more source before promotion.

These actions are governance actions only. They do not make the case production-ready.

## 8. Blocked Actions

Until explicit promotion, a review-only case must block:

- run analysis,
- generate Summary Report,
- generate Sandbox fixture,
- generate public event page,
- generate B-end report,
- run Strategy Lab,
- run Simulation Lab output,
- generate forecast output,
- publish or share as public evidence page,
- claim official verification,
- claim full-web coverage,
- claim full-platform coverage,
- claim full-thread coverage,
- update production risk scores.

## 9. Relationship to Existing Cases

Review-only cases should be separate from production cases.

If a user selects an existing case target, imported rows should still land in review-only mode first. The system should create a review-only attachment or staging container linked to the existing case scope, not directly write analysis-ready evidence into the production case.

Promotion from review-only to production / analysis-ready state must be a separate human decision. That decision must include coverage acknowledgement, privacy review, dedup status, audit review, and rejected-evidence exclusion.

## 10. Boundary Language

Use:

- review-only case,
- staging container,
- governance before analysis,
- provider output is evidence, not truth,
- selected public sample,
- not full-web coverage,
- not full-platform coverage,
- not official verification,
- analysis disabled until promotion,
- public/report/Sandbox output disabled until promotion.

Avoid:

- case completed,
- evidence verified,
- full-web analysis completed,
- official verification completed,
- ready for report,
- automatically enters Sandbox,
- risk score updated,
- real monitoring started.

## 11. Current Decision

Decision after this design:

- `ready_for_phase_6P_review_only_case_runtime`

Recommended next phase:

- Implement a review-only case runtime that creates only internal staging containers, with all analysis/public/report/Sandbox outputs disabled by default.
