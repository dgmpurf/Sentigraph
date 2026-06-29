# Private Collector 8T-2 Provider Result Metadata Contract Alignment v0.1

## A. Decision / Status

phase = 8T-2
task = provider_result_metadata_contract_local_exchange_alignment
docs_only = yes
code_changed = no
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no

decision = ready
privacy_issue_stop = no

## B. What 8T-1 Proved

8T-1 proved:

- the configured collector export root was available
- `package_index.json` was readable
- `package_index.md` was present
- a recommended package was found
- recommended package metadata was readable
- required package files exist
- `manifest.json` and `validation_report.json` were readable as metadata
- `coverage_note.md` was readable as metadata summary
- no full evidence rows were read
- `evidence_items.jsonl` was not parsed
- `evidence_items.csv` was not parsed
- no raw comments were printed
- no raw author ids or names were printed
- compatibility decision was `ready_for_metadata_only_provider_handoff`

8T-1 also found one P2 issue:

- `package_path_relative` has ambiguous base semantics. The actual package also exists directly under the configured export root by `package_name`.

## C. Contract Decisions

8T-2 defines these contract decisions:

- `configured_export_root / package_name` is the preferred canonical package resolution path.
- `package_path_relative_to_export_root` is allowed only when explicitly declared relative to `configured_export_root`.
- legacy `package_path_relative` is not canonical when its base is unclear.
- metadata-only provider handoff is allowed.
- package validation metadata inspection is allowed.
- review-only staging import may be a future next step after a separate gate.
- production import remains blocked.

Production Evidence import, production case creation, `analysis_run` creation, B-end report runtime, Sandbox/public event runtime, public event generation, and response generation remain blocked.

## D. Search-to-Case Product Alignment

Future search is not just a search-result list. The intended product direction is that a user can search a person, event, brand, company, or topic and eventually create a full case workspace that can use Sentigraph modules.

Before that can happen safely:

- the data source must be package/provider-result based
- provider results must be metadata-only before row preview gates
- package metadata must pass safety and path validation
- evidence must pass validation, review, dedup, and promotion gates
- production case creation must remain gated
- `analysis_run` creation must remain gated
- report and Sandbox/public event generation must remain gated
- generated public response and publish/send/post/execute behavior must remain blocked

Future sequence:

1. user search context
2. analysis request
3. provider request
4. provider job result metadata
5. safe package reference
6. metadata-only package validation
7. review-only staging candidate
8. review/dedup/promotion gates
9. future case workspace after explicit gates

This task does not implement search, provider execution, collector execution, Evidence import, case creation, analysis, report runtime, Sandbox/public event runtime, or strategy execution.

## E. Safety / Privacy Policy

Blockers:

- secret, cookie, token, session, password, API key, proxy credential, or saved login state
- browser profile path or browser state
- raw author id as an actual exported value
- raw author name as an actual exported value
- profile URL as an actual exported value
- private messages
- non-public data
- package path escaping configured export root
- absolute private paths exposed to frontend/UI/API responses
- live collection without approval
- full evidence rows in metadata stage
- generated public response
- publish/send/post/execute behavior
- target user list, persuasion score, truth score, official verification flag, prediction probability, psychological profile, or personality diagnosis

Allowed safety markers:

- `raw_author_id_exported=false`
- `raw_author_name_exported=false`
- `profile_url_exported=false`
- `raw_author_id_removed=true`
- `raw_author_name_removed=true`
- `no_private_messages=true`

These marker fields are allowed only when they indicate removal, non-export, or boundary enforcement.

## F. Recommended 8T-3

Recommended next step:

Phase 8T-3 tiny metadata-only package resolver/helper + targeted tests.

The 8T-3 helper should:

- accept an operator-configured export root
- resolve `package_name` under that root
- support `package_path_relative_to_export_root` only when explicitly declared
- classify legacy ambiguous `package_path_relative` as `manual_review_required`
- block path traversal
- block path escape
- check metadata file presence
- return safe metadata-only status

8T-3 must not:

- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- write Evidence Layer
- create a production case
- create an `analysis_run`
- generate reports
- generate Sandbox/public event runtime
- run collector jobs
- call real APIs or real LLMs
- fetch URLs or scrape pages

## G. Source Update Policy

No immediate Project Source update.

Batch update later after actual connection implementation, review-only staging import, or milestone-level state change.

## H. Validation

Validation for this docs-only phase:

- `git diff --check`
- `git status --short`

Backend tests, frontend build, and browser smoke are intentionally not required because this phase does not change code or UI behavior.

## I. Safety Confirmations

- docs-only
- no code changed
- no collector run
- no live crawl
- no browser automation
- no real API
- no real LLM
- no URL fetch/scrape
- no full evidence rows parsed
- no `evidence_items.jsonl` parsed
- no `evidence_items.csv` parsed
- no raw comments printed
- no raw author ids/names printed
- no cookies/tokens/sessions/profile paths read
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no Project Source change
- no GitHub Actions workflow recreated

