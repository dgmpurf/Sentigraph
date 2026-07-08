# Sentigraph Internal Alpha Review Console Future Static Frontend Shell Gate Contract v0.1

## Scope

This document defines the future 8Z-26 static frontend shell smoke gate. It is inactive in 8Z-25 and does not implement frontend code, backend code, routes, APIs, runtime persistence, UI, or browser-visible behavior.

The future gate may be discussed only under:

`APPROVE_8Z_26_INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FRONTEND_SHELL_SMOKE`

This phrase is inactive here and does not authorize anything in 8Z-25.

## Gate Purpose

The future gate would allow a narrow static/internal frontend shell only after 8Z-24 frontend safety tests and 8Z-25 readiness decision. The shell would be a visual/internal preview only, not an operator runtime.

## Allowed Future Scope

If separately approved, future 8Z-26 may:

- create frontend-only static/internal shell
- use an internal-only route name such as `/#/internal-alpha/review-console`
- display safe static metadata labels only
- display no-write and no-production boundaries
- display `human_review_required = true`
- display `no_automatic_trust_upgrade = true`
- display route/backend connection status as not connected / static shell only
- display warning_count / blocker_count summaries
- display allowed_actions labels only
- display blocked_actions labels only
- run frontend build
- run browser smoke if browser capability is available
- check console errors if browser smoke runs
- produce screenshot/contact sheet if useful
- run static forbidden CTA and forbidden field scans
- run 8Z-24 frontend safety tests

## Forbidden Future Scope

Future 8Z-26 must not:

- consume the 8Z-22 backend route
- add `sentigraphApi` review console hook
- make API calls
- change backend route behavior
- add backend route/API behavior
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

## Route/path Boundary

Allowed future path suggestion:

- `/#/internal-alpha/review-console`

Forbidden future path patterns:

- `/#/review-console` as public-facing generic route
- `/#/public/review-console`
- `/#/public-events/review-console`
- `/#/reports/review-console`
- `/#/customer/review-console`
- `/#/b-end/review-console`
- `/#/c-end/review-console`

## Allowed Display

Future static shell may display:

- title explaining internal alpha review console preview
- safe static projection summary
- `source_chain_boundary = evidence_layer_write_candidate_boundary`
- route/backend connection status = not connected / static shell only
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`
- no actual write
- no production object
- no Review Queue runtime
- no Source 11 / FinalSummaryReport runtime
- warning_count / blocker_count summaries
- allowed_actions labels only
- blocked_actions labels only
- next gate inactive phrase labels only
- explanation that shell is not operator runtime

## Forbidden Display Fields

Future static shell must not display:

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

Future static shell must not:

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

## Future Validation Requirements

If separately approved, future 8Z-26 must validate:

- frontend build
- browser smoke if browser capability is available
- console error check if browser smoke runs
- screenshot/contact sheet if useful
- static forbidden CTA scan
- static forbidden field scan
- static no API consumption scan
- 8Z-24 frontend safety tests
- 8Z-22 backend route skeleton regression if route references are mentioned
- `git diff --check`
- scope scan

No backend tests are required unless backend files are touched, except focused regressions if needed.

If browser automation is unavailable, Codex must report `browser_unavailable = yes` and use frontend build plus static scan plus module-load smoke if feasible.

## Blockers

Future 8Z-26 must stop if:

- backend route consumption is required
- `sentigraphApi` hook is required
- backend route/API changes are required
- runtime persistence is required
- raw/private/secret fields appear
- active write/approve/publish/send/post/execute CTA appears
- public / C-end / B-end / customer route naming appears
- readiness wording implies production/customer/public/export/final operation
- browser smoke cannot be run and no acceptable fallback exists
- approval phrase is missing or ambiguous

## Relationship to Actual Write and Production Objects

This future static shell gate does not approve actual write. Actual Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, and production Analysis Result creation remain separate high-risk gates.

## Relationship to Backend Route Consumption

This future static shell gate must not consume the 8Z-22 backend route. Backend route consumption requires a later separate route-consumption gate.

## Relationship to Recording/video

This future gate is not recording and does not prepare external presentation assets. Recording/video remains a later presentation activity after product/runtime boundaries are safe.

## Source Update Recommendation

No immediate Project Source update is required for this inactive future gate unless it becomes part of a larger checkpoint.

Source 11 update = no.
