# Sentigraph v0.9 Release Notes

Date: 2026-05-15

## Summary

Sentigraph v0.9 is a mock-first, offline desktop web MVP for public opinion risk monitoring. It supports local case management, deterministic V1.5 topic-level risk scoring, Chinese structured reports, Markdown export, persisted monitoring snapshots, threshold alerts, manual scheduler simulation, and a local notification outbox.

This checkpoint is intended to stabilize the project before v1.0 MongoDB persistence work. It does not implement MongoDB, real crawlers, real platform API calls, external LLM calls, real notification delivery, authentication, or background workers.

## Current Capabilities

- Desktop-first React/Vite dashboard with Ant Design, ECharts, and Framer Motion.
- FastAPI backend with mock-first public opinion analysis pipeline.
- Platform registry with 9 mock-selectable platforms and inactive future platform groups.
- Reddit adapter scaffold with mock mode by default and credential-gated optional real mode.
- Local JSON-backed analysis cases.
- V1.5 topic-level risk outputs:
  - `risk_model_version`
  - `overall_risk`
  - `topic_risks`
  - `top_risk_topics`
  - `real_crisis_risk`
  - `manipulation_risk`
- Chinese structured public opinion report builder.
- Markdown report export.
- Persisted analysis snapshots and alert events.
- Manual scheduler foundation through `POST /api/v1/scheduler/run-due`.
- Local in-app notification outbox with mark-read and simulate-send behavior.
- Safe local demo utilities:
  - `scripts/reset_local_data.py`
  - `scripts/seed_demo_cases.py`
  - `scripts/api_smoke_check.py`

## Validation

- Backend tests: `92 passed in 2.82s`.
- Frontend production build: passed in 7.75s.
- API smoke check: `26 passed, 0 failed`.
- The smoke check used a temporary project-local JSON store and did not call external APIs or require Reddit credentials.

## Known Limitations

- Vite still reports large vendor chunks for Ant Design and ECharts. Route-level page chunks are split, and the warning is non-blocking for local demo use.
- Local JSON persistence is for demo/development only and is not a production concurrent database.
- Monitoring is deterministic/manual mock logic; no real background scheduler runs by default.
- Notifications are stored locally only; no email, Slack, webhook, Enterprise WeChat, Feishu, SMS, or push messages are sent.
- Reddit real mode remains optional and credential-gated; the default product flow remains offline/mock.
- Chinese terminal output may render incorrectly in some Windows shells depending on code page, but source files are kept in UTF-8.

## Recommended Checkpoint

Suggested tag name:

```text
v0.9-pre-v1-hardening
```

Do not create the tag automatically unless explicitly instructed.

## Next v1.0 Direction

Implement an optional MongoDB-backed case store behind the existing repository/storage interface while keeping `local_json` as the default local development backend.

Recommended v1.0 scope:

- Add `CASE_STORE_BACKEND=mongo` as an optional mode.
- Keep `CASE_STORE_BACKEND=local_json` as the default.
- Persist cases, reports, snapshots, alerts, scheduler state, and notifications.
- Document connection settings without committing secrets.
- Add indexes/schema notes.
- Add migration/export/backfill tooling from local JSON.
- Keep all current API contracts backward-compatible.
- Keep backend tests runnable without MongoDB unless Mongo-specific tests are explicitly enabled.
