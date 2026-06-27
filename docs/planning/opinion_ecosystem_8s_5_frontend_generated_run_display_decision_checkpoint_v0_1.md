# Phase 8S-5 Frontend Generated-run Display Decision Checkpoint v0.1

## A. Decision

```text
phase = 8S-5
decision = docs_only_frontend_generated_run_display_implementation_decision
current_state = ready_for_8S_5_frontend_generated_run_display_planning
next_state_if_ready = ready_for_8S_6_frontend_generated_run_display_first_slice_implementation
```

8S-5 approves only a planning decision for the next frontend slice. It does not implement frontend code, backend code, tests, runtime persistence, package handling, or Project Source changes.

## B. Current Backend Availability

The backend route now exists:

```text
POST /api/v1/opinion-ecosystem/generated-runs/local-fixture
```

The route is backend-only and limited to safe local fixtures. It supports only these `sample_key` values:

- `mock_default`
- `helldivers_psn`
- `donglu_sunjihai_youth_football`

The route does not read real exchange dirs, parse `evidence_items.jsonl` or `evidence_items.csv`, access the private collector, run provider jobs, call real APIs, call real LLMs, fetch URLs, scrape pages, write Evidence Layer records, create production cases, create `analysis_run` records, generate B-end report runtime output, generate Sandbox/public event runtime output, or generate response text.

## C. Why Not Manual Playtest / Recording Yet

```text
manual_playtest_status = deferred_until_frontend_displays_generated_run
recording_status = deferred_until_frontend_displays_generated_run
```

Manual playtest and recording remain deferred because the current Opinion Ecosystem Sandbox still presents static/local explanatory UI by default. The next credible playtest should wait until the frontend can display generated-run metadata, module outputs, boundary flags, blocked/error states, and static fallback behavior clearly.

## D. Recommended First Frontend Implementation Slice

The recommended 8S-6 slice should be very small:

- add a frontend API helper for `POST /api/v1/opinion-ecosystem/generated-runs/local-fixture`
- add one generated-run panel or section inside `OpinionEcosystemSandbox`
- default to the existing static/local explanatory UI unless the user/operator explicitly clicks a local generated-run action
- support only `helldivers_psn` and `donglu_sunjihai_youth_football` sample keys from the UI
- show loading, success, blocked, and error states
- show run metadata and boundary flags
- show module outputs as generated-run data
- keep existing static explanation as fallback

The UI should map current sandbox sample modes conservatively:

| Current sandbox mode | Generated-run `sample_key` |
| --- | --- |
| `helldivers_psn_sample` | `helldivers_psn` |
| `donglu_sunjihai_sample` | `donglu_sunjihai_youth_football` |

The default route `/#/opinion-ecosystem` may keep using Helldivers as the default visible sample. The query route `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` must continue selecting Dong/Sun and must not fall back to Helldivers.

## E. What Must Not Be Implemented In 8S-6

8S-6 must not implement:

- real package row parsing
- real exchange dir read
- private collector access
- production Evidence import
- production case / `analysis_run`
- B-end report runtime
- Sandbox/public event runtime generation
- generated response text
- Strategy Lab runtime
- publish/send/post/execute behavior
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

These strings may appear only as forbidden-field, boundary, deferred, or stop-condition language. They must not appear as active capabilities.

## F. Acceptance Criteria For Future 8S-6

Future 8S-6 should be accepted only if:

- frontend build passes
- backend route tests still pass
- default `/#/opinion-ecosystem` still works
- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football` still selects Dong/Sun
- generated-run display can call the local fixture route
- fallback static explanation remains available
- boundary labels remain visible
- no visible `undefined`
- no visible `NaN`
- no visible `[object Object]`
- no visible 500 prompt
- no visible ErrorBoundary
- no publish/send/post/execute CTA
- no raw author identifiers
- no generated public response text

Recommended browser smoke for 8S-6:

- open `/#/opinion-ecosystem`
- confirm static fallback is visible before any generated-run action
- click the local generated-run action for Helldivers
- confirm generated-run metadata, boundary flags, warnings/blockers, and module output cards render
- open `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- click the local generated-run action for Dong/Sun
- confirm the displayed generated-run sample does not fall back to Helldivers
- confirm console has no Sentigraph page errors or warnings

## G. Source Recommendation

After future 8S-6 implementation commit:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request / Provider / Import Governance behavior changes.
