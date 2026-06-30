# Opinion Ecosystem 8U-7 Dense Graph Frontend/API Integration Decision v0.1

## A. Decision / Status

phase = 8U-7
task = dense_graph_frontend_api_integration_decision_docs_only
decision = ready
privacy_issue_stop = no
docs_only = yes
backend_code_changed = no
frontend_code_changed = no
route_changed = no
api_route_added = no
tests_changed = no
frontend_implementation_approved_now = no
backend_route_expansion_approved_now = no
public_route_approved_now = no
production_integration_approved_now = no
c_end_customer_surface_approved_now = no
b_end_customer_surface_approved_now = no
real_api_approved_now = no
real_llm_approved_now = no
collector_runtime_approved_now = no
source_update_recommended = no immediate

Decision summary:

- Do not approve frontend dense graph implementation now.
- Do not approve public route, customer route, production integration, or route expansion now.
- Keep the existing dense graph route backend-only, internal/local-only, disabled-by-default, and sample allowlist-only.
- Prefer a future decision gate before implementation: either Dong/Sun historical replay browser regression smoke or a more detailed frontend/API contract refinement.

## B. Current Backend State Summary

8U-1 created a backend-only dense opinion graph builder. It turns safe evidence-like fixture rows into anonymous aggregate/proxy dense graph runs.

8U-2 created a generated-run-compatible dense graph attachment adapter. It packages dense graph output with boundary flags, runtime side-effect flags, graph summaries, safe previews, warnings, and blockers.

8U-3 created backend generated-run dense graph integration. It combines the base minimum real-run output and dense graph attachment into a backend-only integration object.

8U-4 created the backend dense graph route contract. It selected the future internal/local-only route direction and explicitly deferred frontend integration.

8U-5 implemented the internal dense graph route:

```text
GET /api/v1/internal/opinion-ecosystem/dense-graph/generated-runs/{sample_id}
```

8U-6 validated the route. It confirmed:

- disabled-by-default
- GET-only
- internal/local-only
- sample allowlist-only
- no arbitrary path input
- no private collector path input
- no URL fetch
- no frontend integration
- no public/customer route
- no Evidence Layer write
- no production case or production `analysis_run`
- no real API, real LLM, or collector

Known 8U-6 aggregate smoke results:

| sample_id | people_cluster_proxy_count | edge_count | timeline_bucket_count | frontend_ready | production_ready |
| --- | ---: | ---: | ---: | --- | --- |
| `donglu-sunjihai-youth-football` | 240 | 800 | 7 | false | false |
| `helldivers-psn` | 68 | 375 | 1 | false | false |

The backend route remains not frontend-ready and not production-ready.

## C. Integration Options Compared

### Option A: Keep Backend-only for Now

User value:

- Low direct user value today.
- Preserves the route as a backend contract and validation surface.

Demo value:

- Useful for internal technical review.
- Not useful as a visual demo unless paired with existing static Sandbox UI.

Risk:

- Lowest risk.
- No risk of users reading dense graph as full-web, production, official, or causal graph.

Required gates:

- None for status quo.
- Continue route contract validation if route behavior changes later.

Why not approved now:

- This option is the current state, not a new implementation.

Confusion risk:

- Low because no frontend user sees it by default.

### Option B: Internal Developer/Reviewer-only Frontend Diagnostic Panel Later

User value:

- Helps developers/reviewers inspect route status, aggregate counts, boundary flags, warnings, and safe previews.

Demo value:

- Moderate for internal review.
- Useful as a bridge between backend route and future visual integration.

Risk:

- Medium-low if hidden/internal and clearly labeled.
- Risk rises if it appears as a normal product page.

Required gates:

- Frontend/API contract refinement.
- Browser smoke plan.
- Safety copy matrix.
- Explicit user approval before implementation.
- Route remains env-gated and disabled by default.

Why not approved now:

- No frontend contract has been approved.
- No browser smoke has checked Dong/Sun historical replay state after 8U-6.
- User-facing copy and fallback behavior still need a dedicated contract.

Confusion risk:

- Can confuse reviewers if it shows graph previews without strong labels. Must state proxy graph, selected sample only, and no production readiness.

### Option C: Opinion Ecosystem Sandbox Optional Dense Graph View Later

User value:

- Potentially high for explaining dense PeopleCluster / InfluenceCore / EchoBox structure in the existing Sandbox.
- Could improve comparison between static fixture visualization and backend-generated proxy graph.

Demo value:

- High if the UI clearly separates static local demo from backend-generated route output.

Risk:

- Medium.
- The Sandbox is already visually persuasive; adding backend graph data may make users believe it is full-web, official, causal, or production-grade.

Required gates:

- Dong/Sun historical replay browser regression smoke.
- Frontend/API contract docs.
- Fallback behavior approved.
- Safety copy matrix approved.
- Explicit implementation approval.
- No public default dependency on enabled backend route.

Why not approved now:

- Backend route says `frontend_ready=false`.
- Static/local fallback is still safer for public demo.
- Dong/Sun route preservation should be browser-smoked before adding another dynamic path.

Confusion risk:

- Significant without boundary copy. Must never present as real social graph, truth graph, prediction graph, or complete public-opinion map.

### Option D: Public Event Page Dense Graph Preview Later

User value:

- Could make public event pages more understandable.

Demo value:

- High visual impact.

Risk:

- High.
- Public event pages are C-end oriented and can easily be interpreted as public truth, full-web capture, or official verification.

Required gates:

- Stronger governance gate than an internal/Sandbox surface.
- Separate public-copy review.
- Explicit public-surface approval.
- No customer/public route dependency on env-enabled internal route.

Why not approved now:

- Public route is not approved.
- Customer/C-end surface is not approved.
- Production readiness remains false.

Confusion risk:

- High. This option can easily overclaim dense graph as complete social graph or causal proof.

### Option E: B-end Report Dense Graph Appendix Later

User value:

- Could help B-end readers understand evidence structure, spread concentration, and review limitations.

Demo value:

- Moderate to high for professional review.

Risk:

- Medium-high.
- A report appendix can be interpreted as a formal analytic conclusion, production metric, or verified source map.

Required gates:

- Report section contract.
- Report export boundary.
- Human-review language.
- No production score.
- Explicit B-end surface approval.

Why not approved now:

- B-end report dense graph appendix is a customer-facing/reporting surface.
- Current route is backend/internal and `production_ready=false`.

Confusion risk:

- High if graph size is read as truth strength or source completeness.

## D. Recommended Future Path

Primary recommended future candidate:

```text
Dong/Sun historical replay browser regression smoke before any frontend dense graph implementation
```

Reason:

- The user previously noticed possible Dong/Sun historical replay / Sandbox entry confusion.
- The canonical query route is known: `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`.
- A browser regression pass can confirm that the current static/demo route does not silently fall back to Helldivers.
- It is safer to verify the existing user-visible route before adding backend dense graph consumption.

Secondary candidate after that:

```text
8U-8 frontend/API contract refinement docs-only
```

Any later frontend contract must remain:

- local/internal/demo-only
- controlled samples only
- no public route
- no production score
- no real API / LLM / collector
- no auto execute
- no generated public response
- no target user list
- no persuasion score

Implementation still requires a later explicit user approval phrase.

## E. API Consumption Policy

Should frontend call the existing internal route directly?

- Not now.
- Later public demo surfaces should not directly depend on the internal route by default.
- A later frontend-safe adapter/contract should be designed before any implementation.

Should there be a separate frontend-safe adapter/contract later?

- Yes.
- The contract should define safe normalization, disabled-state display, unsupported-sample display, fallback behavior, and preview limits before any UI code is changed.

Should the route stay env-gated?

- Yes.
- The route must remain disabled by default.
- Frontend must not expose a way to enable the route.

How should disabled response be shown in UI if a future UI exists?

- Show a compact internal/demo-only explanation:
  - dense graph backend route disabled
  - static/local fallback shown
  - no live backend graph fetched
  - no production readiness implied

How should unsupported sample be shown?

- Show unsupported sample state.
- Do not silently fallback to Helldivers or Dong/Sun.
- Do not show another sample as active.

What should happen if route is disabled?

- Keep static/local fallback.
- Label fallback clearly as static/local demo.
- Do not show backend dense graph route as active.

What should happen if frontend sample is Dong/Sun but backend route unavailable?

- Preserve Dong/Sun active sample in UI.
- Show Dong/Sun static/local fixture or a clear unavailable state.
- Never silently switch active graph context to Helldivers.

Should static/local fallback remain?

- Yes.
- Static/local fallback should remain the public/demo default until a later explicit integration approval.

## F. UI Boundary Copy Requirements

Any future UI must clearly state:

- selected sample only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- human review required
- PeopleCluster is anonymous aggregate proxy
- InfluenceCore is content / narrative / media / official / meme / forum core, not a person
- dense graph is a proxy graph, not a real social graph
- no auto execute
- no generated public response
- no target user list
- no persuasion score

Suggested short copy:

```text
Dense graph is a selected-sample proxy graph for review and explanation. It is not full-web coverage, not full-platform coverage, not official verification, not causal proof, not prediction, and not a production score.
```

## G. Forbidden UI / Output Behavior

Future frontend must not:

- show raw evidence rows
- show raw comments without governance
- expose raw author id / actual author_name / actual profile_url / username / account id
- show private collector path
- show absolute filesystem path
- show cookies / sessions / tokens / secrets
- show `response_text` / `generated_public_message`
- show `target_user_list`
- show `persuasion_score`
- show `truth_score`
- show `official_verified`
- show `prediction_probability`
- show `psychological_profile` / `personality_diagnosis`
- show publish / send / post / execute CTA
- imply automated public action
- imply official verification or causal proof

## H. Dong/Sun Regression Relationship

The user previously observed that Dong/Sun historical replay / Sandbox entry might fall back to Helldivers / PSN.

Static audit found the canonical route:

```text
/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football
```

8U-6 did not run browser smoke.

If a fallback-to-Helldivers issue is reproducible, it is a P1 demo blocker because it would undermine sample identity and trust.

Recommendation:

- Run Dong/Sun historical replay browser regression smoke before any frontend dense graph integration.
- Minimum check: from `/#/public-events/donglu-sunjihai-youth-football`, click Sandbox / historical replay CTA and confirm the query route preserves Dong/Sun as the active sample.

## I. Required Gates Before Implementation

Future implementation requires:

- 8U-8 frontend/API contract docs-only or Dong/Sun browser regression smoke
- explicit user approval before implementation
- backend route remains stable
- sample allowlist preserved
- frontend fallback contract defined
- browser smoke plan defined
- safety copy matrix approved
- no Source files generated by Codex

Implementation must not begin from a casual "continue" or "next" prompt.

## J. Stop Rules

Future implementation must stop if:

- route must be enabled by default
- frontend needs public/customer route
- arbitrary sample path is requested
- private collector path or package path is needed
- raw rows or author identifiers are needed
- `response_text` / `generated_public_message` is requested
- `target_user_list` / `persuasion_score` is requested
- production Evidence write is requested
- production case / `analysis_run` is requested
- real API / LLM / collector is requested
- any public publish / send / post / execute action is requested

## K. Validation

Validation for this docs-only phase:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git log --oneline -8
git diff --check
```

No backend tests are required because this phase does not modify backend code.

No frontend build is required because this phase does not modify frontend code.

No browser smoke is run because this phase is a decision checkpoint, not UI validation.

## L. Safety Confirmations

- docs-only
- no backend code changed
- no frontend code changed
- no route behavior changed
- no API route added
- no tests changed
- no frontend implementation approved now
- no backend route expansion approved now
- no public route approved now
- no production integration approved now
- no real API approved or called
- no real LLM approved or called
- no collector runtime approved or run
- no Evidence Layer write
- no production case created
- no production `analysis_run` created
- no Source files created in repo
- no `docs/project_sources/` created
- no GitHub Actions workflow recreated
