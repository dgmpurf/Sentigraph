# Opinion Ecosystem Dense Graph Frontend/API Integration Contract v0.1

## A. Future Frontend Data Contract

This document defines a future-safe frontend/API contract for dense graph consumption. It does not approve or implement frontend integration.

Future UI may consume only safe route envelope fields:

- `response_schema`
- `route_status`
- `sample_id`
- generated-run integration status summary
- `graph_summary`
- `preview_limits`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`
- `human_review_required`
- `frontend_ready`
- `production_ready`
- `recommended_visualization_mode`
- aggregate node / edge / timeline counts
- safe preview nodes / edges only if already redacted

The UI must treat `generated_run_integration` as backend contract data, not as production truth. If a future adapter exposes it to React components, it should normalize the payload into a frontend-safe view model before rendering.

Allowed aggregate display fields include:

- `people_cluster_proxy_count`
- `influence_core_proxy_count`
- `content_aggregate_proxy_count`
- `echobox_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode`

Allowed safe preview display may include:

- anonymous node ids
- node type
- aggregate/proxy size
- aggregate/proxy stance or category labels
- edge source/target ids
- edge type
- edge weight or normalized strength
- timeline bucket id / stage id / aggregate counts

Forbidden display:

- raw evidence rows
- raw comments without governance
- raw author id
- actual `author_name`
- actual `profile_url`
- username / account id
- private collector path
- absolute filesystem path
- cookie / session / token / secret
- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- psychological profile or personality diagnosis
- publish / send / post / execute CTA

## B. Future Frontend State Model

Future UI state should be explicit and non-magical.

### `route_disabled`

The backend route is disabled by env gate.

UI behavior:

- show static/local fallback if available
- label fallback as static/local demo
- do not imply backend dense graph is active
- do not ask the user to enable secrets or env values in the browser

### `unsupported_sample`

The route does not support the selected sample id.

UI behavior:

- show unsupported sample message
- keep the requested sample identity visible
- do not silently fallback to another sample
- provide local static fallback only if it matches the same active sample

### `unavailable`

The route cannot be reached or returns an unexpected safe error.

UI behavior:

- stop loading
- show explanation
- keep static/local fallback if available
- do not loop or poll

### `ready`

The route returns safe dense graph data.

UI behavior:

- show selected-sample boundary copy
- show `frontend_ready=false` / `production_ready=false` if present
- render only safe normalized data
- keep static/local sample identity visible

### `degraded`

The route returns dense graph data with warnings.

UI behavior:

- show warnings
- label graph as degraded
- keep boundary copy visible
- do not hide sample limitations

### `blocked`

The route reports a blocker.

UI behavior:

- do not render graph previews
- show blocker categories without forbidden values
- preserve static/local fallback only if safe and sample-matched

### `stale_static_fallback`

Static local fallback is shown because route data is disabled, unavailable, or not approved.

UI behavior:

- label fallback as static/local demo
- do not imply current backend route execution
- do not imply live data

### `safety_blocked`

Client adapter detects unsafe fields or forbidden output.

UI behavior:

- block rendering
- show safety-blocked message
- do not print forbidden values
- do not attempt recovery by showing raw payload

## C. Future Fallback Behavior

If backend disabled:

- show static/local demo fallback with clear label
- do not tell the browser user how to enable env gates
- do not make route enablement a UI action

If unsupported sample:

- do not fallback to another sample silently
- do not show Helldivers when Dong/Sun was requested
- do not show Dong/Sun when Helldivers was requested
- show unsupported sample state or sample-matched static fallback only

If Dong/Sun requested:

- preserve active sample as `donglu-sunjihai-youth-football`
- never silently show Helldivers as active sample
- if backend dense graph is unavailable, show Dong/Sun static/local fallback or unavailable state

If graph fails:

- show a clear explanation
- do not keep a spinner forever
- do not print raw exception payload
- do not print absolute paths

If counts are sparse:

- show sample coverage explanation
- state that graph density is an artifact of selected sample and preview bounds
- do not interpret small count as low real-world importance
- do not interpret large count as truth strength

## D. Future Route / Client Policy

Future integration must obey:

- no public default use
- no production assumption
- no real-time refresh
- no polling unless separately approved
- no analytics / user tracking
- no external fetch
- no route enabling from frontend
- no secret or env exposure
- no public route promotion
- no B-end/C-end customer surface unless separately approved

The existing internal route must remain env-gated. Frontend code must not rely on it for default public demo viability.

Recommended future client pattern:

1. Keep static/local fixture as the public demo default.
2. Add a small frontend-safe adapter only after explicit approval.
3. Adapter normalizes dense graph response into a safe display model.
4. Adapter blocks unsafe fields.
5. UI displays route state and boundary copy before graph preview.

## E. Future Browser Smoke Requirements

Minimum browser smoke if frontend integration is ever implemented:

- open `/#/opinion-ecosystem`
- open `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- open `/#/public-events/donglu-sunjihai-youth-football`
- click Dong/Sun historical replay / Sandbox CTA
- confirm query is preserved
- confirm active sample remains Dong/Sun
- confirm no fallback to Helldivers unless user explicitly selects Helldivers
- confirm dense graph UI shows selected-sample boundary
- confirm no `[object Object]`
- confirm no `undefined`
- confirm no `NaN`
- confirm no visible 500
- confirm no ErrorBoundary
- confirm no publish / send / post / execute CTA
- confirm no raw author or profile fields

Additional route-state smoke if future UI calls the backend:

- route disabled state
- unsupported sample state
- ready known Dong/Sun sample
- ready known Helldivers sample
- degraded state if test fixture supports it
- blocked/safety-blocked state if test fixture supports it
- static fallback state

## F. Required UI Boundary Labels

Future UI must include these labels or equivalent nearby copy:

- selected sample only
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- proxy graph, not real social graph
- PeopleCluster is anonymous aggregate proxy
- InfluenceCore is content / narrative / media / official / meme / forum core, not a person
- no auto execute
- no generated public response
- no target user list
- no persuasion score

## G. Stop Rules for Future Implementation

Stop if implementation would require:

- enabling the backend route by default
- creating a public dense graph route
- creating a customer route
- reading arbitrary sample paths
- reading private collector paths
- accepting package paths
- accepting URL input
- printing raw rows
- printing raw comments without governance
- exposing raw author/profile fields
- exposing absolute filesystem paths
- generating response text
- ranking target users
- scoring persuasion
- claiming truth score
- claiming official verification
- claiming prediction probability
- generating psychological profiles
- writing Evidence Layer
- creating production case
- creating production `analysis_run`
- calling real API
- calling real LLM
- running collector
- publishing/sending/posting/executing platform action

## H. Implementation Approval Requirement

This contract does not approve implementation.

Future implementation requires explicit user approval and should name the exact scope, for example:

```text
Approve 8U-8 frontend-safe dense graph adapter implementation
```

Casual wording such as "continue", "next", or "good" must not be treated as approval.
