# Review Queue Initialization Design v1

## Purpose

This document defines how a future runtime may initialize review queue items from staged evidence candidates inside a review-only case.

The review queue initialization gate exists to move already-redacted staged evidence candidates into a human review workflow. It does not make the evidence production-ready, analysis-ready, public, verified, or deduplicated.

## Core Principle

Review queue initialization is not analysis.

Review queue initialization is not deduplication.

Review queue initialization is not promotion.

Review queue initialization is not production case creation.

Review queue initialization is not report, Sandbox, or public event generation.

Provider output is evidence, not truth. Staged candidate text remains `source_url_provided_unverified` and `medium_low` unless later gates explicitly and safely change those labels.

## Non-Goals

This design does not implement runtime behavior.

This phase does not:

- write to the production Evidence Layer
- create a production case
- automatically run analysis
- initialize production evidence review queues
- run deduplication
- generate Sandbox fixtures
- generate public event pages
- generate B-end reports
- execute provider or collector jobs
- perform live collection
- call real APIs
- call a real LLM
- upgrade trust
- claim official verification
- claim full-web, full-platform, or full-thread coverage

## Required Prior Chain

Review queue initialization can only be considered after all prior gates exist and remain valid:

1. Analysis Request exists.
2. Provider Result exists.
3. Case Draft Handoff exists.
4. Evidence Import Plan exists.
5. Metadata-only Import Preview exists.
6. Human Review Decision with `approve_import` exists and is still the latest applicable decision.
7. Dry-run Import Job exists.
8. Execution Preflight exists.
9. Synthetic Row Reader Dry-Run passed.
10. Limited Real Package Row Preview passed or warned without `privacy_stop`.
11. Review-only Case exists.
12. Review-only Staging Import completed.
13. Staged evidence candidates exist.
14. A human reviewer explicitly approves the future review queue initialization runtime.

If any upstream gate is missing, stale, rejected, privacy-held, or blocked, review queue initialization must not proceed.

## Review Queue Purpose

The review queue is only for:

- human review of staged evidence candidates
- marking evidence as approved, rejected, weak, duplicate-merged, privacy-held, or needing more source context
- preparing for a future dedup preview gate
- preserving append-only audit trail
- preventing unreviewed evidence from affecting analysis

The review queue is not for:

- sentiment analysis
- risk score update
- public display
- report material
- official verification
- full dataset representation
- model calibration
- public event generation
- Sandbox fixture generation

## Queue Initialization Strategy

The first future runtime should:

- initialize review queue items from staged evidence candidates only
- keep `analysis_included=false`
- keep `public_visible=false`
- keep `report_visible=false`
- keep `sandbox_visible=false`
- preserve `review_status=review_needed`
- preserve `verification_status=source_url_provided_unverified`
- preserve `trust_label=medium_low`
- attach `review_case_id`
- attach `staging_import_id`
- attach `package_name`
- attach `source_preview_run_id`
- create append-only audit metadata
- avoid silently changing the original staged candidate record

The runtime must not re-read package source rows. It must not parse `evidence_items.jsonl`, `evidence_items.csv`, `source_manifest.jsonl`, or any collector-side file. It must use only staged evidence candidate records that were already created from redacted preview rows.

## Queue Ownership

The review queue belongs to the review-only case.

It must not mix with a production case queue unless a later promotion gate explicitly creates an isolated production transition.

The existing Evidence Review Queue concept may be reused only if it can guarantee:

- isolation by `review_case_id`
- `analysis_included=false`
- `public_visible=false`
- `report_visible=false`
- `sandbox_visible=false`
- no production case dependency
- audit-visible decisions

## Relationship To Dedup

Deduplication must not run automatically during queue initialization.

Review queue completion may feed a later dedup preview gate, but only after:

- reviewed/rejected/deferred statuses are clear
- privacy holds are resolved
- weak items are warning-marked
- duplicate candidates are identified or prepared
- audit trail exists

Duplicate evidence must not amplify risk, sentiment, or coverage claims. Any duplicate count is a repetition signal only after a later dedup gate decides how to preserve it safely.

## Initialization Blockers

Future runtime must block if:

- staged candidates are missing
- staging import is not completed
- review-only case is not active for internal review
- review-only case was promoted, archived, rejected, or privacy-held
- any staged candidate exposes raw author identifiers
- any staged candidate contains private messages
- any upstream preview had `privacy_stop`
- latest human decision is not `approve_import`
- request attempts analysis, report, Sandbox, public event, production case, Evidence Layer write, or trust upgrade

## Boundary Notes

Use these labels in UI and API output:

- review queue initialization
- review-only case
- staged evidence candidate
- `review_needed`
- `source_url_provided_unverified`
- `medium_low`
- `analysis_included=false`
- audit-visible
- rejected evidence excluded
- weak evidence warning-marked
- duplicate evidence must not amplify risk
- provider output is evidence, not truth

Avoid these claims:

- automatic analysis
- production case created
- official verified
- full-web coverage
- full-platform coverage
- report generated
- Sandbox generated
- risk score updated
- evidence verified

