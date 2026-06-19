# Review Queue To Dedup Gate v1

## Purpose

This document defines the future gate between review queue completion and dedup preview.

Deduplication is a separate safety and quality step. It must not run automatically during review queue initialization or completion.

## Dedup Gate Preconditions

The dedup gate can be considered only after:

1. review queue has been initialized
2. review queue completion or threshold state is reached
3. privacy holds are resolved
4. rejected items are excluded
5. weak items are warning-marked
6. `needs_more_source` items are blocked from promotion
7. duplicate candidates are identified or prepared
8. audit trail is complete
9. coverage limitations are acknowledged
10. reviewer labels are present

If any precondition fails, the dedup gate remains blocked.

## Dedup Gate Responsibilities

The dedup gate must:

- prevent duplicate evidence from amplifying risk or sentiment
- preserve `duplicate_group_id`
- preserve `duplicate_count`
- identify exact and near-duplicate candidates before analysis
- require human review for uncertain merge decisions
- preserve rejected evidence as audit-visible but excluded
- preserve weak evidence warnings
- keep `analysis_included=false`
- avoid automatic analysis

## Suggested Dedup Readiness Object

```json
{
  "schema": "sentigraph_review_queue_to_dedup_gate_v1",
  "review_case_id": "review_case_...",
  "request_id": "analysis_request_...",
  "state": "ready_for_dedup_preview",
  "eligible_review_item_count": 12,
  "rejected_excluded_count": 3,
  "weak_warning_count": 3,
  "needs_more_source_blocked_count": 2,
  "privacy_hold_count": 0,
  "duplicate_candidates_prepared": true,
  "audit_complete": true,
  "analysis_included": false,
  "can_run_analysis_now": false,
  "recommended_next_phase": "6W_dedup_preview_design"
}
```

## Duplicate Handling Principles

Duplicate evidence must not amplify:

- risk scores
- sentiment counts
- topic prevalence
- public interest claims
- source coverage claims

Duplicate evidence may be preserved as:

- repetition signal
- coordinated amplification hint
- audit trail
- source coverage context

But it must be explicitly labeled and must not be counted as independent evidence without dedup policy.

## Human Review For Merge Decisions

Human review should be required when:

- URLs differ but content is similar
- titles differ but body previews are similar
- the same snippet appears across multiple sources
- source attribution is unclear
- weak evidence and duplicate evidence overlap
- duplicate grouping may change downstream interpretation

Uncertain duplicates should remain separate but warning-marked until a reviewer decides.

## What This Gate Does Not Do

This gate does not:

- run dedup automatically
- include evidence in analysis
- create production EvidenceItems
- create production cases
- generate reports
- generate Sandbox fixtures
- generate public events
- update risk scores
- call real APIs
- call real LLMs
- verify official truth

## Suggested Future Phases

- 6T: Review Queue Initialization Runtime
- 6U: Review Action Runtime / Audit Timeline
- 6V: Review Queue Completion Gate Runtime
- 6W: Dedup Preview Design
- 6X: Dedup Preview Runtime
- 6Y: Analysis-ready Promotion Gate Design

## Boundary Language

Use:

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

Avoid:

- automatic analysis
- production case created
- official verified
- full-web coverage
- full-platform coverage
- report generated
- Sandbox generated
- risk score updated
- evidence verified

