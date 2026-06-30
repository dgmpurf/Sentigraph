# Opinion Ecosystem 8S-16-NR Internal Self-guided Walkthrough QA Plan v0.1

## A. Purpose

This document defines a no-recording internal QA route for the Opinion Ecosystem demo.

The output is simple private notes only. No media file, screenshot, public sharing, or external tester is required.

## B. No-recording QA Route

Walk through:

- `/#/demo`
- `/#/public-events`
- `/#/public-events/donglu-sunjihai-youth-football`
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- explicit generated-run click
- `/#/reports/donglu-sunjihai-youth-football-sample`
- optional `/#/public-events/request`
- optional `/#/analysis-requests` only if backend is running and no visible 500 appears

## C. Page and Route Checklist

For each route, check:

- no visible 500
- no ErrorBoundary
- no undefined / NaN / `[object Object]`
- no confusing route context switch
- no secrets/private paths/raw author identifiers
- no publish/send/post/execute CTA
- boundary labels visible

## D. Generated-run Checklist

Check:

- generated-run click works
- selected sample boundary visible
- not full-web / not full-platform visible
- not official verification visible
- not prediction / not causal proof visible
- PeopleCluster anonymous aggregate proxy wording visible
- ResponseStrategyComparison human-review-only wording visible
- no generated response text
- no response_text / generated_public_message active output
- no auto_execute / publish_now / send_now / post_now active capability

## E. Notes-only Output

Future self-guided QA output should be simple notes only:

- route checked
- issue observed
- severity P0/P1/P2/P3
- whether it blocks trusted playtest
- short note

The output must not include:

- media file
- screenshot requirement
- public sharing
- external tester
- real API/LLM call
- collector run
- private collector path
- raw author identifier

## F. Stop Conditions

Stop the walkthrough if:

- visible 500
- ErrorBoundary
- page crash
- undefined / NaN / `[object Object]`
- generated-run click fails
- secret or private path appears
- raw author identifier appears
- publish/send/post/execute CTA appears
- generated public response text appears
- UI implies live crawling
- UI implies official verification
- UI implies full-web/full-platform coverage

## G. Recommended Next Decision

If the walkthrough passes, decide whether to:

1. prepare trusted playtest without recording, or
2. pause, or
3. fix small route/copy issues before any trusted user sees the demo.

Do not proceed to trusted playtest without explicit approval.
