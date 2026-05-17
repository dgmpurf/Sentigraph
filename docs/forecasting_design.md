# Public Opinion Forecasting Design

Status: v4.5 deterministic MVP foundation.

## Purpose

The forecasting foundation estimates near-future public-opinion risk from existing case monitoring snapshots. It is a local deterministic signal for demos and regression testing, not a guaranteed prediction and not a machine-learning model.

## Inputs

Forecasting reads persisted `AnalysisSnapshot` records for one case:

- `risk_score` / `overall_risk`
- `risk_level`
- `risk_model_version`
- `real_crisis_risk`
- `manipulation_risk`
- `top_risk_topics`
- `created_at`

It does not fetch live data, call real platform APIs, call real LLM APIs, or enable live public fetching.

## Trend Features

For total risk, real-crisis risk, manipulation risk, and topic risk series, the MVP computes:

- `latest_risk`
- `moving_average`
- `slope`
- `acceleration`
- `volatility`
- `snapshot_count`
- `trend_direction`: `rising`, `falling`, `stable`, or `unknown`

Trend direction is intentionally coarse. With fewer than two snapshots, the trend is `unknown`.

## Horizons

The forecast returns four deterministic horizons:

- `next_check`
- `1h`
- `6h`
- `24h`

The top-level `ForecastResult` mirrors `next_check`; the full horizon list is available under `risk_forecasts`.

## Formula

The MVP formula is:

```text
predicted_risk = latest_risk + slope_factor + acceleration_factor
```

The implementation uses horizon multipliers for slope and acceleration, then clamps every predicted score to `0-100`.

Risk level mapping:

- `0-39`: `low`
- `40-69`: `medium`
- `70-84`: `high`
- `85-100`: `critical`

## Confidence

Forecast confidence is based only on snapshot count:

- `0`: `insufficient_history`
- `1`: `low`
- `2-3`: `medium_low`
- `4+`: `medium`

The MVP deliberately does not expose high confidence.

With zero snapshots, the API returns `forecast_status="insufficient_history"` and a safe recommended action to run monitoring again. With one snapshot, it returns a conservative baseline forecast with `low` confidence and `trend_direction="unknown"` rather than overstating a trend.

## Topic Forecasts

For latest `top_risk_topics`, the topic forecaster matches prior snapshots by topic id, cluster id, or topic text. It predicts:

- current topic risk score
- predicted topic risk score
- predicted topic risk level
- topic trend direction
- deterministic forecast reason

If topic history is missing, the latest topic score is used as a low-information baseline.

## Prediction Explanation UI

The Risk Monitor forecasting panel now renders user-facing explanation cards derived from existing deterministic forecast fields. The frontend does not change the forecast algorithm; it explains:

- `forecast_status`
- predicted risk score and level
- trend direction and confidence
- slope, acceleration, volatility, and snapshot count
- real-crisis and manipulation-risk direction
- top topic forecast reasons when available
- recommended action for insufficient or thin history

The UI includes the disclaimer: current forecasting is a deterministic MVP trend extrapolation based on historical snapshots and does not mean the future will necessarily happen. When history is missing or thin, the page emphasizes `历史不足` and asks the user to continue running monitoring to accumulate snapshots.

## API

- `GET /api/v1/cases/{case_id}/forecast`: compute and return the current forecast from persisted snapshots.
- `POST /api/v1/cases/{case_id}/forecast/run`: compute the current forecast explicitly. Persistence is intentionally not added yet; forecasts are derived from snapshots.

Both endpoints are offline-only and never trigger platform calls, LLM calls, live public fetch, or crawlers.

## Limitations

- Deterministic and rule-based only.
- Synthetic/demo-friendly; not calibrated on real production datasets.
- No external signals, seasonality, event calendars, or velocity baselines yet.
- Forecast confidence is intentionally conservative.
- Forecast results should be reviewed as a triage aid, not as a guaranteed prediction.

## Future Work

- Add longer history windows and baseline normalization.
- Evaluate forecasting against labeled historical incidents.
- Add per-topic time series persistence when real data flow is stable.
- Explore V2 dynamic risk forecasting after benchmark coverage expands.
- Consider ML or LLM-assisted forecasting only after real data access, safety gates, cost guardrails, and evaluation datasets are ready.
