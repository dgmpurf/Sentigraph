# Opinion Ecosystem 8S-15 Pre-recording Safety Checklist v0.1

## A. Purpose

This checklist is for any future 8S-16 actual recording.

No recording is executed in this phase.

## B. Environment Checklist

Before future recording, confirm:

- repo clean before recording
- backend running if backend-dependent pages are shown
- frontend running
- browser window prepared
- bookmarks or typed routes prepared
- no dev console showing secrets
- no terminal showing `.env`, keys, or private paths
- no private collector directory visible
- no personal browser tabs visible

## C. Route Checklist

For each route:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- `/#/reports/donglu-sunjihai-youth-football-sample`
- optional `/#/public-events/request`
- optional `/#/analysis-requests` only if backend is running and no visible 500 appears

Check:

- loads successfully
- no visible 500
- no ErrorBoundary
- no undefined / NaN / `[object Object]`
- no secret/private path/raw author identifiers
- no publish/send/post/execute CTA
- boundary labels visible

## D. Generated-run Checklist

Confirm:

- generated-run click succeeds
- output clearly labeled local fixture/generated run
- selected sample boundary visible
- not full-web/full-platform visible
- not official verification visible
- not prediction / not causal proof visible
- PeopleCluster anonymous aggregate proxy wording visible
- ResponseStrategyComparison human-review-only wording visible
- no response_text / generated_public_message visible as active output
- no auto_execute / publish_now / send_now / post_now visible as active capability

## E. Recording Safety Checklist

Confirm capture area does not include:

- secrets
- private directories
- personal messages
- API keys
- tokens/cookies/sessions
- raw author identifiers
- private collector path
- unsupported claims

## F. Abort Checklist

Abort future recording if any stop condition appears:

- visible 500
- ErrorBoundary
- page crash
- undefined / NaN / `[object Object]`
- generated-run click failure
- console error/warn during checked route
- secret or private path
- raw author identifier
- publish/send/post/execute CTA
- generated public response text
- UI implies live crawling
- UI implies official verification
- UI implies full-web/full-platform coverage
