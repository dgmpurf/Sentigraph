# Sentigraph Public Opinion Risk Algorithm Design

This document organizes the Sentigraph public opinion risk algorithm into the current V1 MVP model, a practical V1.5 topic-level upgrade path, and a future V2 topic-cluster dynamic model.

The current product direction remains mock-first and offline. No real crawler, real platform API, real OpenAI/LLM call, login bypass, captcha bypass, anti-bot evasion, paywall bypass, or private data collection is required for these models.

## 1. System Pipeline

Sentigraph risk analysis is designed as a staged pipeline:

```text
keyword expansion
  -> mock/public data collection
  -> language-aware text handling
  -> comment cleaning
  -> duplicate detection
  -> user aggregation
  -> sentiment analysis
  -> topic clustering
  -> propagation graph
  -> bot/AI signal scoring
  -> overall risk scoring
  -> visualization output
  -> template-based response recommendation
```

The MVP implementation should keep each step deterministic where possible so backend tests stay stable and the frontend can rely on a predictable API contract.

## 2. V1 MVP Static Scoring Model

`v1_static_mvp` is the active model family for the current MVP. It uses global analysis signals and produces a single project-level risk score.

The V1 design target is:

```text
sentiment_score = avg(sentiment_weight * intensity / 10) * 100
```

Sentiment weights:

```text
positive = 1.0
neutral = 0.5
negative = 0.0
```

Propagation score:

```text
propagation_score = min(100, total_nodes * 2 + max_depth * 5)
```

AI/bot penalty:

```text
ai_bot_penalty = (ai_generated + bot_comments) / total_comments * 100
```

Overall score:

```text
overall_score = clamp(
  sentiment_score * 0.4 + propagation_score * 0.4 - ai_bot_penalty * 0.2,
  0,
  100
)
```

Risk levels:

```text
0-39   low
40-69  medium
70-100 high
```

Implementation note: the current backend scoring code already uses a deterministic V1-style weighted factor model in `backend/app/services/scoring/risk_score.py`. This document records the target static model and versioning direction, but this task does not change the working score calculation.

## 3. V1.5 Topic-Level Risk MVP Model

`v1_5_topic_risk_mvp` is the recommended bridge between the current global V1 score and the future V2 dynamic model.

V1.5 should not require historical baselines, real platform APIs, real crawlers, or external LLM calls. It should use the mock pipeline data that already exists: cleaned comments, duplicate groups, sentiment outputs, topic clusters, bot/repeated-script signals, and propagation/engagement proxies when available.

V1.5 should run as a shadow or optional model first. The active production-like score should remain `v1_static_mvp` until the new output is tested and wired into the frontend safely.

Per-topic output should include:

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

Suggested deterministic formula:

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

Signal guidance:

- `neg_severity`: negative ratio multiplied by average negative intensity or harm proxy.
- `spread_signal`: normalized topic volume and available propagation breadth/depth proxy.
- `controversy_signal`: mixed positive/negative participation or high disagreement proxy.
- `bot_signal`: duplicate ratio, repeated-script density, suspicious author concentration, and sentiment uniformity.
- `influence_proxy`: likes, replies, shares, author influence, or fallback comment-count weight.

Risk levels should stay compatible with existing display conventions:

```text
0-39   low
40-69  medium
70-100 high
```

Overall aggregation should avoid diluting one dangerous topic with many low-risk topics. A simple first implementation can use:

```text
overall_risk = 0.65 * max_topic_risk + 0.35 * average_topic_risk
```

A deterministic softmax aggregation can be added later if it remains easy to test.

V1.5 should also output:

- `top_risk_topics`
- `real_crisis_risk`
- `manipulation_risk`
- `risk_model_version = "v1_5_topic_risk_mvp"`

`real_crisis_risk` should emphasize credible negative topics, safety, legal, ethics, or service-impact signals. `manipulation_risk` should emphasize bot-like, repeated-script, low-credibility, or suspicious amplification signals. These two outputs can initially be deterministic summary scores derived from topic risk drivers.

## 4. V2 Topic-Cluster Dynamic Risk Model

V2 should avoid mixing all comments into one global average. Instead, it should calculate risk by topic cluster and time window.

Core formula:

```text
Risk(c,t) = 100 * sigmoid(
    beta_0
  + 1.25 * NegSeverity(c,t)
  + 1.05 * SpreadMomentum(c,t)
  + 0.85 * Polarization(c,t)
  + 0.75 * Influence(c,t)
  + 0.60 * Novelty(c,t)
  + 0.45 * Persistence(c,t)
  - 0.65 * LowCredibilityPenalty(c,t)
)
```

Where:

- `c` is a topic cluster.
- `t` is a time window.
- Coefficients are initial design weights and should be calibrated with historical data later.
- The model should emit both topic-level risk and project-level aggregate risk.

V2 should also distinguish:

- `real_crisis_risk`: risk driven by credible negative signals, material issues, public safety, legal exposure, or sustained stakeholder concern.
- `manipulation_risk`: risk driven by repeated scripts, suspicious coordination, low-trust accounts, bot-like behavior, or artificial amplification.

## 5. Metric Definitions

### NegSeverity

```text
NegSeverity = negative_probability * emotion_intensity * harm_type_weight
```

Harm-type weights:

```text
normal complaint                                      1.0
service experience issue                             1.2
integrity / ethics concern                           1.4
discrimination / fraud / safety / legal risk          1.7
public safety / major crisis                          2.0
```

### SpreadMomentum

Spread momentum combines:

- volume anomaly versus historical baseline
- first derivative growth rate
- second derivative acceleration

### Polarization

```text
Polarization = 4 * support_ratio * oppose_ratio
```

This peaks when opinion is evenly split and drops when one side dominates.

### Influence

Influence should combine:

- graph centrality
- likes, replies, shares, or equivalent platform engagement signals
- author influence
- cross-community or cross-platform spread

### Novelty

Novelty measures semantic distance from the historical topic baseline. A new complaint pattern or new allegation type should produce higher novelty.

### Persistence

Persistence measures continuous activity across time windows. Repeated or recurring negative discussion should have higher persistence than a one-off spike.

### LowCredibilityPenalty

Low credibility penalty reduces crisis risk when activity is dominated by AI/bot/low-trust signals. It should not hide manipulation risk; instead, V2 should track manipulation separately.

## 6. Risk Aggregation

Topic-level risks should be aggregated with softmax weighting:

```text
OverallRisk = sum(softmax(Risk(c) / tau) * Risk(c))
```

Default `tau`:

```text
12 to 20
```

Lower `tau` gives more weight to the highest-risk topic. Higher `tau` spreads weight across more topics.

V2 aggregate output should include:

- `overall_risk`
- `topic_risks`
- `real_crisis_risk`
- `manipulation_risk`
- `risk_explanation`

## 7. Visualization Outputs

V1 visualizations:

- project-level risk score card
- risk radar chart
- sentiment trend
- platform/time heatmap
- topic cluster list
- bot impact summary
- propagation graph

V2 visualizations:

- topic risk ranking by time window
- topic risk heatmap
- real crisis versus manipulation split
- spread momentum curve
- polarization trend
- influence graph overlays
- risk explanation panel showing dominant drivers

V1.5 visualizations should add:

- topic risk ranking
- top risk topic explanation cards
- real crisis versus manipulation split
- topic risk contribution to overall risk
- repeated-script signal per topic where available

## 8. Recommendation Generation

Recommendation generation stays template-based in the MVP.

V1 recommendations should use:

- `risk_score`
- `risk_level`
- negative sentiment ratio
- topic clusters
- bot impact
- propagation graph size
- representative comments

V2 recommendations should also use:

- highest-risk topic clusters
- whether the dominant risk is real crisis risk or manipulation risk
- persistence across time windows
- novelty of the issue
- influence and cross-community spread

V1.5 recommendations should use the top topic risk drivers when present:

- highest-risk topic
- whether topic risk is driven by negativity, spread, controversy, bot signal, or influence
- `real_crisis_risk` and `manipulation_risk` split
- topic-specific recommended action and public response emphasis

The response tone should remain professional, calm, factual, and public-facing. Representative comments should stay in their original language.

## 9. Future LLM Integration Notes

LLMs may be added later for:

- keyword expansion assistance
- topic labeling
- harm-type classification
- risk explanation drafting
- response template drafting
- sanitized public HTML selector maintenance suggestions

LLMs must not be used to:

- bypass login
- bypass captcha
- bypass paywalls
- evade anti-bot systems
- access private data
- infer hidden identities
- collect credentials, tokens, cookies, private messages, or other secrets

When JSON output is expected from an LLM, the response must be validated against strict schemas before use.
