# Opinion Ecosystem Dense Graph Backend Route Contract v0.1

## A. Purpose

This document defines the future backend route contract for dense graph generated-run output.

This is docs-only. No route is implemented now.

The route contract exists to describe how the 8U-3 backend-only generated-run dense graph integration object may be exposed later, if and only if the user explicitly approves implementation.

## B. Future Route Candidate

Preferred future route candidate:

```text
GET /api/v1/internal/opinion-ecosystem/dense-graph/generated-runs/{sample_id}
```

Alternative route candidates are deferred:

```text
GET /api/v1/opinion-ecosystem/generated-runs/{sample_id}/dense-graph
```

Extending an existing generated-run route is also deferred.

Expected decision:

- use internal/local-only route contract first
- do not implement it now
- do not extend an existing route now
- do not expose the response to frontend now

## C. Future Route Gate

Future route must be:

- disabled by default
- GET-only
- local/internal only
- explicit sample allowlist only
- no arbitrary file path input
- no private collector path
- no package path parameter
- no URL fetch
- no search query execution
- no production case creation
- no Evidence Layer write

Suggested environment gate:

```text
SENTIGRAPH_OPINION_ECOSYSTEM_DENSE_GRAPH_ROUTE_ENABLED
```

Allowed true values after normalization:

- `1`
- `true`
- `yes`

All other values must behave as:

```text
route_disabled
```

## D. Future Sample Policy

Allow only known controlled sample IDs, such as:

- `donglu-sunjihai-youth-football`
- `helldivers-psn`

Do not allow:

- arbitrary sample path
- absolute path
- path traversal
- user-provided file path
- private collector export root
- URL
- search query
- package path parameter

## E. Future Response Behavior

If disabled:

- return safe disabled response
- do not call dense graph service
- do not reveal filesystem paths or private metadata

If enabled and sample is allowed:

- return generated-run dense graph integration object from 8U-3
- preserve boundary flags
- preserve runtime side-effect flags
- keep frontend readiness false unless a later approved frontend phase changes that contract

If sample unknown:

- return safe `not_found` or `unsupported_sample` response
- do not fall back to default sample
- do not reveal local paths or sample search behavior

If graph attachment is degraded:

- return degraded status with warnings
- keep `frontend_ready = false`
- set route-level readiness only for successful route execution, not product readiness
- keep `production_ready = false`

If graph attachment is blocked:

- return blocked status with blockers
- do not return unsafe payload
- do not expose forbidden field values

## F. Query Parameter Policy

For future route only, optional bounded params may be considered:

- `node_limit`: min 20, max 240
- `edge_limit`: min 50, max 800
- `include_previews`: true/false

Do not implement params now.

Do not allow:

- arbitrary `expand_all`
- raw mode
- raw rows
- raw comments
- full evidence row output
- arbitrary file path
- URL input

## G. Forbidden Output

Future route must never output:

- `raw_author_id`
- actual `author_name` value
- actual `profile_url` value
- `username`
- account id
- private messages
- cookies
- sessions
- tokens
- browser profile paths
- private collector path
- absolute private path
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- `auto_execute`
- `publish_now`
- `send_now`
- `post_now`
- `execute_now`

## H. Non-goals

- no frontend integration
- no public route
- no customer route
- no C-end/B-end direct route
- no collector bridge
- no production import
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no B-end report runtime
- no Sandbox/public event runtime
- no generated public response
- no platform action
- no full-web coverage claim
- no full-platform coverage claim
- no official verification claim
- no causal proof claim
- no prediction claim
