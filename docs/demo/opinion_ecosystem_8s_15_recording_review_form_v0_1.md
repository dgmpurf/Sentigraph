# Opinion Ecosystem 8S-15 Recording Review Form v0.1

## A. Purpose

This is a review form for future internal recording capture.

No recording is reviewed in this phase.

## B. Recording Metadata Fields

- recording_id:
- recording_date:
- reviewer:
- duration:
- route_scope:
- build/context:
- backend_running: yes/no
- optional_routes_included: yes/no

## C. Technical Review

Checklist:

- no visible 500
- no ErrorBoundary
- no undefined / NaN / `[object Object]`
- generated-run click works
- no console error/warn visible in final route pass if checked
- no broken route
- no confusing route context switch

## D. Safety Review

Checklist:

- no secrets
- no `.env`
- no API keys
- no tokens/cookies/sessions
- no private browser profile
- no private collector path
- no raw author identifiers
- no private messages
- no generated response text
- no publish/send/post/execute CTA
- no target_user_list / persuasion_score / truth_score / official_verified / prediction_probability
- no psychological_profile / personality_diagnosis

## E. Communication Review

Checklist:

- selected sample boundary is clear
- not full-web/full-platform is clear
- not official verification is clear
- not prediction / not causal proof is clear
- generated run is local fixture output is clear
- PeopleCluster is anonymous aggregate proxy is clear
- ResponseStrategyComparison is human-review-only is clear
- no automatic public response is clear
- no platform action is executed is clear
- B-end report sample is understood as sample, not production report

## F. Verdict

Select one:

- approved_for_private_review_only
- needs_minor_retake
- needs_major_retake
- blocked_privacy_or_safety

## G. Follow-up Actions

| Issue | Severity P0/P1/P2/P3 | Owner | Required before trusted playtest? | Notes |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
