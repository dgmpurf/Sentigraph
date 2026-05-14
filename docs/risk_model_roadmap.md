# Sentigraph Risk Model Roadmap

This roadmap separates the current MVP risk model from the future advanced model so implementation can stay incremental and testable.

## Current Active Model

```text
RISK_MODEL_VERSION = v1_static_mvp
TOPIC_RISK_MODEL_VERSION = v1_5_topic_risk_mvp
```

The current backend uses a deterministic V1-style static weighted scoring service in:

```text
backend/app/services/scoring/risk_score.py
```

This model is suitable for the mock-first desktop MVP because it can produce stable project-level scores from sentiment, bot impact, propagation speed, controversy, and trend-shift signals.

The current visualization and normalized report responses also include V1.5 topic-level risk output from:

```text
backend/app/services/scoring/topic_risk_score.py
```

V1.5 keeps the old `risk_score` and `risk_level` fields backward-compatible while adding topic-level fields such as `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`.

## V1 MVP Scope

V1 includes:

- keyword expansion
- mock/public data collection placeholders
- language-aware text handling
- comment cleaning
- duplicate detection
- sentiment analysis
- topic clustering
- propagation graph
- bot/AI signal penalty
- project-level overall risk score
- visualization output
- template-based response recommendation

V1 is intentionally simple. It should be easy to test and should not require real crawlers, real platform APIs, or external LLM calls.

## V1.5 Practical Topic Risk Scope

V1.5 is the recommended next algorithm upgrade:

```text
risk_model_version = v1_5_topic_risk_mvp
```

V1.5 should calculate topic-level risk using the current mock pipeline outputs. It should not require historical baselines, real crawlers, real platform APIs, or external LLM calls.

V1.5 should add per-topic fields:

- `topic_id`
- `topic`
- `comment_count`
- `negative_ratio`
- `average_sentiment_score`
- `neg_severity`
- `spread_signal`
- `controversy_signal`
- `bot_signal`
- `influence_proxy`
- `topic_risk_score`
- `topic_risk_level`
- `risk_explanation`

Suggested formula:

```text
topic_risk = clamp(
    neg_severity * 35
  + spread_signal * 20
  + controversy_signal * 15
  + bot_signal * 15
  + influence_proxy * 15,
  0,
  100
)
```

Suggested aggregation:

```text
overall_risk = 0.65 * max_topic_risk + 0.35 * average_topic_risk
```

V1.5 should also emit:

- `top_risk_topics`
- `real_crisis_risk`
- `manipulation_risk`
- `risk_explanation`

Implementation is now present in the mock pipeline as a deterministic offline V1.5 topic-level layer. Existing V1 static scoring code remains in place for factor/radar compatibility.

## V2 Future Scope

V2 is the topic-cluster dynamic risk model described in `docs/algorithm_design.md`.

V2 requires:

- time-windowed comment and engagement data
- stable topic cluster history
- historical topic baselines for novelty detection
- influence graph and graph centrality metrics
- author/account credibility modeling
- separate real crisis risk and manipulation risk outputs
- calibrated coefficients from historical cases or evaluation fixtures

## Implementation Plan

1. Keep V1 stable and versioned as `v1_static_mvp`.
2. Add V1.5 as a deterministic topic-level shadow model using current mock data. Done for the mock pipeline.
3. Add optional schema fields for `topic_risks`, `top_risk_topics`, `real_crisis_risk`, `manipulation_risk`, and `risk_explanation`. Done.
4. Integrate V1.5 explanations into report and visualization responses without breaking V1 fields. Done for backend responses.
5. Collect or generate deterministic time-window fixtures in mock data.
6. Build topic history and baseline utilities behind tests.
7. Add V2 as a later shadow model that does not affect current API score decisions.
8. Compare V1, V1.5, and V2 outputs on fixture scenarios.
9. Expose V2 only after API, frontend, and tests are ready.

## Compatibility Rules

- Do not break existing `risk_score` and `risk_level` fields.
- Add new risk fields as optional fields first.
- Keep MongoDB dictionary keys as strings.
- Keep frontend API transformations centralized under `frontend/src/api`.
- Do not change the active scoring behavior without an explicit migration task.

## Next Recommended Step

The next implementation step is to connect V1.5 topic-risk explanations more explicitly in the frontend dashboard/report views, then add browser QA coverage. Do not activate full V2 scoring yet.
