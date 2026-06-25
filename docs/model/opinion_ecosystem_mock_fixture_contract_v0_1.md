# Opinion Ecosystem Mock Fixture Contract v0.1

Status: docs-only / design-only / future deterministic local mock calculator contract. This is not implemented, not runtime, not backend schema, not frontend UI, not real API, not real LLM, not crawler, not full-web, not full-platform, not official verification, not causal proof, not prediction, not personality diagnosis, not individual persuasion scoring, and not auto-executed response strategy.

Scope is selected sample / local fixture / imported evidence only.

Required model metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

This document designs a future mock fixture input contract for a deterministic local calculator. It defines safe fixture groups and forbidden fields.

The future fixture must be synthetic, local, and safe. It must not contain raw author identifiers, private messages, cookies, tokens, sessions, browser profiles, localStorage, secrets, or real collector internals.

## 2. Top-Level Fixture Shape

Illustrative Markdown-only example:

```json
{
  "schema": "sentigraph_opinion_ecosystem_mock_fixture_v0_1",
  "fixture_metadata": {},
  "evidence_items_safe": [],
  "content_aggregates": [],
  "influence_cores": [],
  "people_clusters": [],
  "echo_boxes": [],
  "response_strategy_candidates": []
}
```

This snippet is illustrative only. No executable fixture file is created in this phase.

## 3. fixture_metadata

Required fields:

- `fixture_id`
- `case_id`
- `sample_id`
- `fixture_role`
- `source_mode`
- `stage_id`
- `time_window`
- `coverage_note`
- `selected_sample_only = true`
- `not_full_web = true`
- `not_full_platform = true`

Recommended constraints:

- `source_mode` should be `synthetic_fixture`, `selected_public_sample_fixture`, or `imported_evidence_fixture`.
- `coverage_note` must state sample coverage limitations.

## 4. evidence_items_safe

Allowed safe fields:

- `evidence_id`
- `platform`
- `evidence_type`
- `acquisition_mode`
- `provenance_type`
- `verification_status`
- `trust_label`
- `trust_score`
- `review_status`
- `duplicate_group_id`
- `duplicate_count`
- `relevance_label`
- `recency_label`
- `stance_hint`
- `emotion_intensity_hint`
- `narrative_frame_hint`
- `source_url_present`
- `created_at_bucket`
- `relative_stage_bucket`
- `aggregate_ref`
- `influence_core_refs`

Forbidden:

- raw author identifiers
- `raw_author_id`
- `author_name`
- `profile_url`
- full text rows unless explicitly synthetic safe text in Markdown examples only
- private messages
- cookies
- tokens
- sessions
- profile data
- localStorage
- secrets

Illustrative safe item:

```json
{
  "evidence_id": "safe_evidence_001",
  "platform": "sample_forum",
  "evidence_type": "comment_summary",
  "acquisition_mode": "mock_fixture",
  "provenance_type": "mock_fixture",
  "verification_status": "mock_fixture",
  "trust_label": "low",
  "trust_score": 0.25,
  "review_status": "approved",
  "duplicate_group_id": "dup_group_001",
  "duplicate_count": 4,
  "relevance_label": "strong_case_match",
  "recency_label": "inside_stage_window",
  "stance_hint": "oppose",
  "emotion_intensity_hint": 0.72,
  "narrative_frame_hint": "accountability",
  "source_url_present": true,
  "relative_stage_bucket": "T1",
  "aggregate_ref": "agg_001",
  "influence_core_refs": ["core_001"]
}
```

## 5. content_aggregates

Fields:

- `aggregate_id`
- `aggregate_type`
- `platform`
- `evidence_ids`
- `stage_id`
- `raw_metric_summary`
- `stance_distribution`
- `trust_summary`
- `review_summary`
- `dedup_summary`

`raw_metric_summary` must be safe aggregate counts only. It must not contain raw text rows or raw identities.

## 6. influence_cores

Fields:

- `core_id`
- `core_type`
- `frame_direction`
- `associated_evidence_ids`
- `source_identity_hint`
- `clarity_hint`
- `novelty_hint`
- `bridge_hint`
- `backlash_hint`
- `risk_flags`

InfluenceCore represents content / narrative / official / media / KOL / meme / explanation core, not a people ball.

## 7. people_clusters

Fields:

- `cluster_id`
- `cluster_role`
- `initial_expressed_stance`
- `stance_confidence`
- `attention_budget`
- `fatigue`
- `expression_intensity`
- `openness`
- `visibility_weight`
- `action_threshold`
- `reputation_memory_sensitivity`
- `connected_echo_box_ids`

No real persons, accounts, author names, profile URLs, or raw identifiers are allowed.

## 8. echo_boxes

Fields:

- `echo_box_id`
- `echo_box_role`
- `platform_refs`
- `aggregate_ids`
- `people_cluster_ids`
- `influence_core_ids`
- `stance_distribution`
- `interaction_proxy_summary`
- `cross_cutting_proxy_summary`

EchoBox is a sample-scoped discussion container proxy, not a real community map.

## 9. response_strategy_candidates

Fields:

- `strategy_id`
- `strategy_type`
- `stage_id`
- `claim_intensity`
- `exposure_level`
- `transparency_level`
- `accountability_level`
- `privacy_sensitivity`
- `human_review_state`

Forbidden:

- `auto_execute`
- covert manipulation
- fake consensus
- sockpuppet / bot / water-army strategy
- individual targeting
- harassment

## 10. Invalid / Forbidden Fixture Examples

These examples must be rejected or blocked by future validation.

### raw_author_id present

```json
{ "raw_author_id": "user_123" }
```

### author_name present

```json
{ "author_name": "real user name" }
```

### profile_url present

```json
{ "profile_url": "https://example.invalid/profile/user" }
```

### cookie / token / session present

```json
{
  "cookie": "forbidden",
  "token": "forbidden",
  "session": "forbidden"
}
```

### auto_execute response strategy

```json
{ "response_strategy": "auto_execute" }
```

### overclaim flags

```json
{
  "full_web_claim": true,
  "official_verification_claim": true,
  "causal_proof_claim": true,
  "prediction_claim": true
}
```

## 11. Fixture-Level Boundary Requirements

Every valid fixture must state:

- docs-only if embedded in documentation
- future deterministic local mock calculator if used later
- selected sample only
- not full-web
- not full-platform
- not official verification
- not causal proof
- not prediction
- not personality diagnosis
- not individual persuasion scoring
- no real API
- no real LLM
- no crawler
- human review required for response strategies
