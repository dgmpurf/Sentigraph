# Opinion Ecosystem ContentAggregate First Formula Slice v0.1

Status: docs-only first formula slice plan. This document does not implement formulas, backend code, backend tests, frontend UI, API routes, schemas, runtime persistence, file IO, product behavior, analysis, report generation, Sandbox generation, public event generation, provider execution, collector execution, real API calls, real LLM calls, or Evidence Layer writes.

## A. First Formula Slice Name

Phase 8P-2 ContentAggregate Formula Calculator.

## B. Purpose

Future 8P-2 implementation should calculate only `ContentAggregateWeightV01` using local synthetic in-memory fixtures that already passed the 8P-1 fixture validator.

The goal is to add the smallest formula-bearing module while preserving all 8P-1 governance boundaries.

## C. Expected Future Code Scope If Approved Later

Likely update only:

- `backend/app/services/opinion_ecosystem_mock_calculator.py`
- `backend/app/tests/test_opinion_ecosystem_mock_calculator.py`

Do not add:

- API routes
- frontend UI
- runtime persistence
- package files
- schema files, unless a later implementation proves plain dict contracts are insufficient

## D. Future Pure Function Candidates

Future pure function candidates:

- `clamp01(value)`
- `log_norm(value, cap)`
- `get_trust_weight(evidence)`
- `get_review_weight(evidence)`
- `get_dedup_weight(evidence)`
- `get_relevance_weight(evidence)`
- `get_recency_weight(evidence)`
- `calculate_evidence_base_weight(evidence)`
- `calculate_evidence_confidence(evidence_items)`
- `calculate_coverage_quality(evidence_items)`
- `calculate_content_aggregate_weight(aggregate, evidence_items)`
- `calculate_all_content_aggregate_weights(fixture)`

All functions should remain deterministic and should operate only on in-memory synthetic fixture dicts.

## E. Input Assumptions

Future 8P-2 may use only safe metadata from:

- `fixture_metadata`
- `evidence_items_safe`
- `content_aggregates`

Allowed evidence fields:

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
- `aggregate_ref`
- `created_at_bucket`
- `relative_stage_bucket`
- synthetic raw metric summary if already safe

Not required and not allowed:

- full text rows
- raw author fields
- profile URLs
- private messages
- cookies
- tokens
- sessions
- browser profile data
- localStorage
- secrets
- real package rows
- collector output

## F. Formula Scope

Future 8P-2 should implement the following 8N-g formulas only for ContentAggregate.

### Evidence Base Weight

```text
w_e = trust_weight * review_weight * dedup_weight * relevance_weight * recency_weight
```

Trust defaults:

| Source / provenance | trust_weight |
| --- | ---: |
| official_api_public | 1.00 |
| official_api_oauth | 0.95 |
| reviewed_public_parser | 0.80 |
| manual_url_with_attestation | 0.65 |
| data_vendor_attested | 0.55 |
| user_upload_with_source | 0.50 |
| search_discovery_candidate | 0.40 |
| manual_text_without_source | 0.30 |
| screenshot_transcription | 0.30 |
| mock_fixture | 0.25 |
| unknown_or_unclear_source | 0.20 |

Review defaults:

| review_status | review_weight |
| --- | ---: |
| approved | 1.00 |
| not_reviewed | 0.70 |
| review_needed | 0.70 |
| needs_more_source | 0.55 |
| marked_weak | 0.45 |
| rejected | 0.00 |
| human_rejected | 0.00 |

Dedup:

```text
dedup_weight_e = 1 / sqrt(duplicate_group_size)
```

If missing duplicate group:

```text
dedup_weight_e = 1
```

Repetition:

```text
repetition_signal_g = log(1 + duplicate_group_size) / log(1 + duplicate_cap)
```

Relevance:

| relevance | relevance_weight |
| --- | ---: |
| strong_case_match | 1.00 |
| partial_case_match | 0.60 |
| weak_case_match | 0.30 |
| off_topic | 0.00 |

Recency:

| recency | recency_weight |
| --- | ---: |
| inside_stage_window | 1.00 |
| near_stage_window | 0.70 |
| outside_but_relevant | 0.40 |
| unknown_time | 0.60 |

Utility:

```text
log_norm(x, cap) = clamp(log(1 + x) / log(1 + cap), 0, 1)
```

### Heat

```text
H_observed_A =
  0.30 * V_A
+ 0.20 * I_A
+ 0.15 * G_A
+ 0.15 * E_A
+ 0.10 * S_A
+ 0.10 * R_A
```

Missing components must re-normalize over available components.

Confidence-adjusted heat:

```text
H_conf_A = H_observed_A * (0.60 + 0.40 * Q_A)
```

### Evidence Confidence

```text
Q_A = weighted_mean(trust_weight_e * review_weight_e, dedup_adjusted_weight_e)
```

Coverage quality:

```text
coverage_quality_A =
  0.35 * source_url_present_share
+ 0.25 * reviewed_or_approved_share
+ 0.20 * non_low_trust_share
+ 0.20 * non_unknown_stance_share
```

Evidence confidence:

```text
evidence_confidence_A =
  0.65 * Q_A
+ 0.35 * coverage_quality_A
```

### Polarization And Controversy

```text
conflict_mass = p_support + p_oppose
balance = 1 - abs(p_support - p_oppose) / (p_support + p_oppose + epsilon)
known_ratio = 1 - p_unknown
P_A = conflict_mass * balance * sqrt(known_ratio)
```

Controversy:

```text
C_A =
  0.30 * P_A
+ 0.20 * E_A
+ 0.15 * X_A
+ 0.15 * D_A
+ 0.10 * R_A
+ 0.10 * L_A
```

### Discussion Risk

```text
DR_A =
  0.25 * H_observed_A
+ 0.25 * C_A
+ 0.15 * E_A
+ 0.15 * S_A
+ 0.10 * issue_sensitivity_A
+ 0.10 * response_gap_A
```

### Review Risk And Overall Risk

```text
RR_A =
  0.30 * (1 - evidence_confidence_A)
+ 0.25 * low_trust_share_A
+ 0.20 * review_needed_share_A
+ 0.15 * missing_source_url_share_A
+ 0.10 * sensitive_privacy_flag_share_A
```

```text
R_A = 0.70 * DR_A + 0.30 * RR_A
```

## G. Missing Data Policy

Future 8P-2 should use this missing-data policy:

- missing `interaction_score`: component unavailable, re-normalize
- missing `growth_score`: component unavailable, or neutral only if explicitly documented in output warnings
- missing emotion: component unavailable, not zero
- missing stance distribution: controversy downgrades and adds warning
- rejected evidence: excluded from analysis-ready scoring, counted in warning
- unknown trust: low confidence default
- missing `duplicate_count`: treat as 1
- no evidence for aggregate: blocked or `insufficient_data` warning, no strong score

## H. Future Minimal Output

Future `ContentAggregateWeightV01` output shape:

```json
{
  "schema": "sentigraph_content_aggregate_weight_v0_1",
  "aggregate_id": "aggregate_example",
  "model_status": "8P_2_content_aggregate_local_formula",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "sample_scope": "selected_sample_only",
  "evidence_mass": {},
  "scores": {
    "sample_heat_score": 0.0,
    "heat_confidence_adjusted": 0.0,
    "sample_controversy_score": 0.0,
    "discussion_risk_score": 0.0,
    "review_risk_score": 0.0,
    "overall_risk_score": 0.0,
    "evidence_confidence_score": 0.0
  },
  "components": {},
  "quality_flags": [],
  "warnings": [],
  "explanation": [],
  "boundary_flags": {
    "not_real_hotlist": true,
    "not_full_web": true,
    "not_full_platform": true,
    "not_official_verification": true,
    "not_causal_proof": true,
    "not_prediction": true,
    "evidence_not_truth": true,
    "human_review_required": true
  }
}
```

This is a future output contract only. It is not implemented by this document.

## I. Integration With 8P-1 Run Object

Future `calculate_opinion_ecosystem_mock_fixture` should:

- validate fixture with the existing 8P-1 validator first
- if blocked, not calculate ContentAggregate
- if `manual_review_required` due unknown/future platform, either not calculate or calculate only with warning
- never imply any provider is runnable
- if `metadata_ready`, calculate ContentAggregate only
- keep all 8P-1 boundary flags
- keep all runtime side-effect flags false
- mark other module outputs as `not_calculated_in_8P_2`
- add no frontend, API route, schema, or runtime persistence

## J. Future Tests List

Future 8P-2 tests should include:

- `test_content_aggregate_minimal_fixture_calculates_weight_v0_1`
- `test_rejected_evidence_excluded_from_content_aggregate_scores`
- `test_duplicate_evidence_folded_not_linear_amplification`
- `test_low_trust_emotional_screenshot_lowers_confidence_and_raises_review_risk`
- `test_one_sided_high_heat_does_not_imply_high_controversy`
- `test_missing_optional_components_renormalize_safely`
- `test_no_evidence_for_aggregate_yields_insufficient_data_warning`
- `test_forbidden_fields_still_block_before_scoring`
- `test_overclaim_fields_still_block_before_scoring`
- `test_auto_execute_still_blocks_before_scoring`
- `test_future_unknown_platform_does_not_imply_provider_runnable`
- `test_no_non_contentaggregate_module_scores_in_8P_2`
- `test_no_real_io_or_runtime_side_effects_by_design`
- `test_deterministic_same_fixture_same_output`

Do not implement these tests in this docs-only phase.

## K. Not Allowed In 8P-2 Implementation

Future 8P-2 implementation must not include:

- InfluenceCore scoring
- EchoBox scoring
- PeopleCluster transition
- ResponseStrategy scoring
- frontend UI
- API route
- backend schema unless absolutely necessary
- runtime persistence
- filesystem read/write except optional safe source scan inside tests if needed
- collector access
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- Evidence Layer write
- production case creation
- analysis_run creation
- B-end report runtime
- Sandbox runtime
- public event runtime
- real API calls
- real LLM calls
- auto execution
- `persuasion_score`
- `prediction_probability`
- `truth_score`
- `official_verified` output

## L. Next Slices Only After 8P-2 Passes

Only after 8P-2 passes targeted validation should later slices be considered:

- 8P-3 InfluenceCore formula only
- 8P-4 EchoBox formula only
- 8P-5 PeopleCluster transition only
- 8P-6 ResponseStrategy comparison only
- 8Q frontend explanatory UI only after backend/local calculator and model card QA are stable
- 8R model card QA / screenshot smoke

Each later slice must preserve sample scope, uncalibrated metadata, human review, and all no-real-API/no-real-LLM/no-collector/no-public-action boundaries.
