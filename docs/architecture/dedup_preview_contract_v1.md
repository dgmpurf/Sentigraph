# Dedup Preview Contract v1

## Purpose

This document defines the future data contract for a review-only dedup preview.

The contract is for architecture handoff only. It does not mean runtime exists.

## Dedup Preview Object

```json
{
  "schema": "sentigraph_dedup_preview_v1",
  "dedup_preview_id": "dedup_preview_...",
  "request_id": "req_...",
  "review_case_id": "review_only_case_...",
  "queue_init_id": "review_queue_init_...",
  "completion_gate_id": "review_queue_completion_gate_...",
  "created_at": "2026-06-19T00:00:00Z",
  "created_by": "sentigraph_local_ui",
  "execution_mode": "review_only_dedup_preview",
  "status": "preview_ready",
  "input_scope": {
    "source": "review_only_queue_items",
    "include_statuses": ["approved", "marked_weak", "duplicate_merged"],
    "exclude_statuses": ["rejected", "needs_more_source", "privacy_hold", "review_needed"],
    "analysis_included": false
  },
  "counts": {
    "items_seen": 0,
    "items_eligible_for_preview": 0,
    "items_excluded": 0,
    "duplicate_group_candidates": 0,
    "unique_candidate_count": 0
  },
  "dedup_signals": {
    "exact_url_match": true,
    "normalized_url_match": true,
    "content_preview_hash_match": true,
    "lineage_match": true,
    "reviewer_merge_hint": true,
    "semantic_llm_match": false
  },
  "groups": [],
  "excluded_items": [],
  "privacy_scan": {
    "raw_identifier_found": false,
    "secret_like_found": false,
    "privacy_stop": false
  },
  "now_flags": {
    "write_evidence_layer_now": false,
    "create_production_case_now": false,
    "run_dedup_now": false,
    "run_analysis_now": false,
    "generate_report_now": false,
    "generate_sandbox_now": false
  },
  "readiness": {
    "state": "ready_for_future_dedup_runtime",
    "can_run_dedup_now": false,
    "can_run_analysis_now": false,
    "requires_human_dedup_confirmation": true
  }
}
```

## Field Definitions

- `schema`: fixed contract name, `sentigraph_dedup_preview_v1`.
- `dedup_preview_id`: local append-only preview record id.
- `request_id`: source Analysis Request id.
- `review_case_id`: source review-only case id.
- `queue_init_id`: source Review Queue Initialization id.
- `completion_gate_id`: Review Queue Completion Gate id that allowed preview consideration.
- `created_at`: local creation timestamp.
- `created_by`: local UI or reviewer label.
- `execution_mode`: must be `review_only_dedup_preview`.
- `status`: `preview_ready`, `incomplete`, `blocked`, or `privacy_hold`.
- `input_scope`: declares which review-only statuses were included or excluded.
- `counts`: preview-only item and group counts.
- `dedup_signals`: deterministic signal switches used by the preview.
- `groups`: list of `DedupGroupCandidate` objects.
- `excluded_items`: excluded review item ids with reasons.
- `privacy_scan`: safe scan result from review-only item fields only.
- `now_flags`: all immediate production/action flags must remain false.
- `readiness`: next-phase readiness only; no current dedup or analysis permission.

## Dedup Group Candidate Object

```json
{
  "schema": "sentigraph_dedup_group_candidate_v1",
  "group_candidate_id": "dedup_group_candidate_...",
  "review_case_id": "review_only_case_...",
  "reason": "exact_url_match",
  "confidence": "high",
  "item_ids": [],
  "representative_item_id": "review_queue_item_...",
  "duplicate_count_preview": 0,
  "may_amplify_risk": false,
  "human_confirmation_required": true,
  "analysis_effect": "preview_only_no_analysis_effect"
}
```

## Dedup Group Candidate Fields

- `schema`: fixed contract name, `sentigraph_dedup_group_candidate_v1`.
- `group_candidate_id`: local candidate id.
- `review_case_id`: review-only case id.
- `reason`: one of `exact_url_match`, `normalized_url_match`, `content_preview_hash_match`, `lineage_match`, `reviewer_merge_hint`, or `mixed`.
- `confidence`: `high`, `medium`, or `low`.
- `item_ids`: review-only queue item ids in the candidate group.
- `representative_item_id`: preview representative item selected by policy.
- `duplicate_count_preview`: preview-only group size metadata.
- `may_amplify_risk`: must remain false.
- `human_confirmation_required`: true for all groups in v1.
- `analysis_effect`: must be `preview_only_no_analysis_effect`.

## Status Semantics

- `preview_ready`: safe preview candidates exist or all eligible items are unique.
- `incomplete`: prior review/completion state is insufficient.
- `blocked`: unsafe fields or side-effect attempts were detected.
- `privacy_hold`: privacy risk blocks preview.

## Contract Boundaries

This contract must not imply:

- dedup completed
- production evidence merged
- analysis readiness
- official verification
- report generation
- full-web or full-platform coverage
- risk score updates

