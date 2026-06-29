# Private Collector 8T-6 Search-to-Case Product Contract Report v0.1

## A. Decision / Status

```text
phase = 8T-6
task = search_to_case_product_contract
privacy_issue_stop = no
code_changed = no
docs_only = yes
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no
api_route_added = no
frontend_changed = no
```

Decision: ready.

## B. What 8T-3 / 8T-4 / 8T-5 Proved

8T-3 proved:

- package resolver exists.
- package paths can be resolved under an operator-configured export root.
- `package_name` is preferred.
- explicit `package_path_relative_to_export_root` is supported.
- legacy ambiguous `package_path_relative` stays manual-review oriented.
- required package files are checked by existence only.
- no evidence rows are parsed.

8T-4 proved:

- provider result reader exists.
- provider result metadata can be validated.
- `package_reference` can be validated.
- resolver status can be propagated safely.
- no production import occurs.

8T-5 proved:

- local exchange fixture smoke exists.
- provider result JSON fixture can flow through reader and resolver.
- output can become safe metadata-only handoff summary.
- no evidence rows are parsed.
- no Evidence Layer write.
- no production case.
- no `analysis_run`.
- no route/UI/API bridge.

## C. Product Contract Decisions

Search-to-Case is:

```text
search query -> governed case workspace candidate
```

It is not merely a search result list.

It is not live crawling by default.

It is not production case creation by default.

It should eventually let a user search a person, event, brand, company, product, public topic, or controversy and create a governed case workspace candidate through metadata, package, review, dedup, and promotion gates.

## D. Gated Workflow Decisions

Canonical object chain:

```text
user_search_context
-> analysis_request
-> provider_request
-> provider_job_result metadata
-> package_reference
-> metadata_only_validation
-> review_only_staging_candidate
-> evidence_review_and_dedup
-> case_workspace_candidate
-> future explicit promotion gates
-> future analysis/report/sandbox gates
```

Gate states include search receipt, analysis request draft, provider request draft, provider result metadata received, package reference ready, metadata validation passed/warn, manual review required, review-only staging, evidence review, dedup, promotion required, workspace candidate ready, and blocker states.

## E. Forbidden Transitions

Forbidden direct jumps:

- search directly to Evidence Layer
- search directly to production case
- provider result metadata directly to Evidence Layer
- provider result metadata directly to production case
- package reference directly to `analysis_run`
- review-only staging directly to report runtime
- review-only staging directly to Sandbox/public event runtime
- workspace candidate directly to public response
- any state directly to publish / send / post / execute

## F. Safety / Privacy Policy

Blockers:

- `privacy_issue_stop`
- path escape
- missing package
- forbidden fields
- raw author identifier exposure
- private messages
- full evidence rows in metadata stage
- live collection without authorization
- unsupported platform
- generated response text
- public execution action

Forbidden field categories:

- cookies
- tokens
- sessions
- passwords
- API keys
- browser profile paths
- proxy credentials
- raw author identifiers
- profile URLs as actual exported values
- private messages
- raw comment dumps
- full evidence rows
- generated public response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

## G. Recommended Next Step

Recommend Phase 8T-7 review-only staging import design.

Do not recommend production import yet.

Do not recommend UI yet unless staging design is complete.

## H. Source Update Policy

No immediate Project Source update.

Batch later after review-only staging import design or implementation milestone.

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
- no frontend/API route added
- no Project Source change
- no GitHub Actions workflow recreated
