# Dedup Preview Design v1

## Purpose

Dedup preview is a governance-only duplicate grouping preview after Review Queue Completion Gate.

It helps reviewers see which review-only queue items may represent the same public-opinion evidence before any later analysis, promotion, report, Sandbox output, or production Evidence Layer write.

## Core Principle

Dedup preview is not dedup execution.

Dedup preview is not a production Evidence Layer write.

Dedup preview is not analysis.

Dedup preview is not promotion.

Dedup preview is not report generation.

Dedup preview is not official verification.

Provider output remains evidence, not truth. Duplicate grouping candidates are governance signals, not facts.

## Non-Goals

This design does not implement:

- runtime code
- row parsing
- original package row reads
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- production Evidence Layer writes
- production case creation
- production Evidence Review Queue creation
- automatic merge
- dedup execution
- analysis
- Sandbox fixture generation
- public event generation
- B-end report generation
- provider execution
- collector job execution
- live collection
- URL fetching
- scraping
- real LLM semantic dedup
- trust upgrade

## Required Prior Chain

Dedup preview can be considered only after:

- Review-only Case exists
- Review-only Staging Import exists
- Review Queue Initialization exists
- Review Action Audit exists where needed
- Review Queue Completion Gate status is `complete_enough_for_future_dedup_preview`
- no `privacy_hold` items exist
- no unresolved `needs_more_source` blockers exist unless explicitly deferred by the completion gate
- rejected items are excluded from future analysis consideration
- weak items are warning-marked
- approved items remain `analysis_included=false`

If any prior gate is missing, unsafe, or incomplete, dedup preview remains blocked.

## Allowed Input Scope

Dedup preview may inspect only safe fields from review-only queue items:

- `review_item_id`
- `staging_id`
- `review_case_id`
- `package_name`
- `platform`
- `evidence_type`
- `source_url`
- `title_preview`
- `body_text_preview`
- `created_at`
- `language`
- `safe_counts`
- `queue_status`
- `review_status`
- `verification_status`
- `trust_label`
- existing duplicate metadata, if any

Dedup preview must not inspect:

- `raw_author_id`
- `raw_author_name`
- `profile_url`
- `private_message`
- cookie / token / session values
- email / phone / password-like values
- original package rows
- external URLs
- collector profiles
- browser sessions

## Candidate Duplicate Signals

Safe duplicate signals:

- exact `source_url` match
- normalized `source_url` match
- same platform plus same title/body preview hash
- same normalized `body_text_preview` hash
- near-identical title/body preview within a local deterministic threshold
- same source row or preview row lineage
- explicit `merge_duplicate` review action metadata
- same `canonical_url_hash` if already present from a safe earlier phase

Boundary rules:

- No network canonicalization.
- No URL fetch.
- No external API.
- No real LLM semantic dedup in this phase.
- Cross-platform dedup must be conservative.
- Text-only cross-platform grouping requires human confirmation.

## First Runtime Recommendation

Future Phase 6X should:

- compute preview-only duplicate groups from review-only queue items
- produce `duplicate_group_candidates`
- not mutate production evidence
- not collapse counts automatically
- not mark `analysis_included=true`
- require human confirmation before any merge effect
- preserve audit trail
- output clear "dedup preview only" boundary copy

## Preview Statuses

Suggested dedup preview statuses:

- `preview_ready`: local duplicate group candidates were generated safely
- `incomplete`: prior review/completion state is not sufficient
- `blocked`: unsafe field, missing gate, side-effect attempt, or inconsistent state was detected
- `privacy_hold`: privacy risk blocks preview

## Count Interpretation

Dedup preview may report:

- raw review-only item count
- eligible preview item count
- excluded item count
- duplicate group candidate count
- unique candidate count

These counts are preview metadata. They must not update risk scores, sentiment counts, coverage claims, or report conclusions.

## Boundary Language

Use:

- dedup preview
- duplicate group candidate
- review-only queue item
- `analysis_included=false`
- preview-only duplicate count
- duplicate evidence must not amplify risk
- audit-visible
- human confirmation required
- provider output is evidence, not truth

Avoid:

- dedup completed
- evidence verified
- production evidence merged
- analysis-ready
- report generated
- official verified
- full-web coverage
- risk score updated

