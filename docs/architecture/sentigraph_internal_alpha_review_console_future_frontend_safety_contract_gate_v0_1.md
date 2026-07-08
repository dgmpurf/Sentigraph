# Sentigraph Internal Alpha Review Console Future Frontend Safety Contract Gate v0.1

## Scope

This document defines the future 8Z-24 frontend safety contract tests-only gate. It is inactive in 8Z-23 and does not implement frontend code, backend code, routes, APIs, runtime persistence, or UI.

The future gate may be discussed only under:

`APPROVE_8Z_24_INTERNAL_ALPHA_REVIEW_CONSOLE_FRONTEND_SAFETY_CONTRACT_TESTS_ONLY`

This phrase is inactive here and does not authorize anything in 8Z-23.

## Gate Purpose

The future gate should verify, before any frontend implementation, that the repo still has no unsafe review console UI surface and no frontend/API overreach connected to the internal alpha review console.

It should act as a protective contract between the completed 8Z-22 disabled backend route skeleton and any later internal UI discussion.

## Allowed Future Scope

If separately approved, future 8Z-24 may:

- add frontend safety contract tests only
- statically inspect frontend route/config files
- statically inspect frontend API client files
- assert no frontend review-console page exists unless separately approved
- assert no public / C-end / B-end / customer alias exists
- assert no forbidden CTA exists
- assert no raw field display exists
- assert no download/export/public delivery UI exists
- assert no production readiness overclaim exists
- preserve 8Z-22 backend route safety tests
- document validation results

## Forbidden Future Scope

Future 8Z-24 must not:

- implement frontend UI
- register frontend route
- create browser-visible review console
- change backend route behavior
- add backend route/API
- add POST / PUT / PATCH / DELETE behavior
- create runtime persistence
- use Review Queue runtime
- perform actual Evidence Layer write
- create persisted Evidence Layer record
- create production EvidenceItem
- create production Review Queue item
- create production case
- create production analysis_run
- start actual analysis execution
- authorize production Analysis Result
- create production Analysis Result
- call Source 11 runtime
- create FinalSummaryReport runtime output
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- run collector/provider job
- inspect private collector source
- read real exchange/package dir
- parse production package rows
- fetch URL
- scrape
- call real API
- call real LLM
- publish/send/post/execute platform action
- expose raw rows/comments/identities
- expose secrets

## Safety-test Categories

Future 8Z-24 tests should cover:

- no frontend route/page for review console unless separately approved
- no public / C-end / B-end / customer aliases
- no `sentigraphApi` hook for review console unless separately approved
- no publish / send / post / execute / approve / write CTA
- no Evidence Layer write wording
- no production object readiness wording
- no Source 11 / FinalSummaryReport runtime readiness wording
- no raw rows/comments/identities/profile URLs/secrets fields
- no download/export/public delivery UI
- no route_ready / frontend_ready / production_ready overclaim
- 8Z-22 backend route skeleton tests still pass
- browser smoke not required because no UI implementation

## Forbidden Display Fields

Future frontend must not display:

- raw evidence rows
- raw comments
- raw author IDs
- raw author names
- actual profile URLs
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profiles
- absolute private paths
- `.env` values
- evidence_items.jsonl contents
- evidence_items.csv contents
- source_manifest row contents
- collection_log row contents
- response_text
- generated_public_message
- target_user_list
- persuasion_score
- truth_score
- official_verified
- prediction_probability
- psychological_profile
- personality_diagnosis

## Forbidden Actions

Future frontend must not:

- approve actual Evidence Layer write
- perform actual Evidence Layer write
- create production EvidenceItem
- use Review Queue runtime
- create production Review Queue item
- create production case
- create production analysis_run
- start actual analysis execution
- authorize production Analysis Result
- create production Analysis Result
- call Source 11 runtime
- create FinalSummaryReport runtime output
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- run collector/provider job
- inspect private collector source
- read real exchange/package dir
- parse production package rows
- fetch URL
- scrape
- call real API
- call real LLM
- publish/send/post/execute platform action

## Future UI Boundary After Safety Tests

Any later UI implementation requires a separate exact approval phrase. It must remain:

- internal-only
- local-only
- disabled/default hidden
- safe metadata only
- no public route
- no C-end route
- no B-end route
- no customer route
- no write actions
- no production object actions
- no Review Queue runtime actions

## Future UI Self-validation

If a later UI task is approved, Codex must self-validate:

- frontend build
- browser smoke if browser capability is available
- console error check
- forbidden CTA scan
- static forbidden field scan
- screenshot/contact sheet if useful

If browser automation is unavailable, Codex must report `browser_unavailable = yes` and use build/static/module-load fallback.

## Relationship to Actual Write and Production Objects

This future safety-test gate does not approve actual write. Actual Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, and production Analysis Result creation remain separate high-risk gates.

## Relationship to Recording/video

This future safety-test gate is not recording and does not prepare external presentation assets. Recording/video remains a later presentation activity after product/runtime boundaries are safe.

## Source Update Recommendation

No immediate Project Source update is required for this inactive future gate unless it becomes part of a larger checkpoint.

Source 11 update = no.
