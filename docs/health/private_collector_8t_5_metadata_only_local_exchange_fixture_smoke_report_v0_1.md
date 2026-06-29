# Private Collector 8T-5 Metadata-only Local Exchange Fixture Smoke Report v0.1

## A. Decision / Status

```text
phase = 8T-5
task = metadata_only_local_exchange_fixture_smoke
privacy_issue_stop = no
code_changed = yes
docs_only = no
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

## B. Implemented Scope

Implemented helper:

- `backend/app/services/private_collector_local_exchange_smoke.py`

Implemented targeted tests:

- `backend/app/tests/test_private_collector_local_exchange_smoke.py`

The helper is metadata-only. It is not wired to backend routes, frontend UI, production runtime, Evidence Layer, production case creation, analysis runs, report generation, Sandbox generation, public event generation, provider execution, collector execution, or HTTP/API bridge behavior.

## C. Local Exchange Fixture Smoke Behavior

The smoke helper supports:

- explicit provider result JSON path handling.
- explicit operator-configured export root handling.
- 8T-4 provider result reader integration.
- 8T-3 package resolver integration.
- safe summary output.
- blocker and warning propagation.

Smoke status behavior:

- safe `package_ready` provider result plus safe package resolves to `ready_for_metadata_only_handoff`.
- `validation_warn` remains `manual_review_required`.
- `live_collection_not_authorized` remains blocked.
- missing provider result JSON returns `blocked_missing_provider_result`.
- schema / contract problems return `needs_fix_metadata_contract`.
- resolver blockers such as `blocked_missing_package`, `blocked_path_escape`, and `blocked_privacy_issue` propagate safely.

The safe smoke summary includes only safe metadata such as:

- `package_name`
- `case_id`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`

It does not include absolute filesystem paths.

## D. Evidence Row Boundary

Evidence row files remain outside smoke helper scope:

- `evidence_items.jsonl` existence may be checked by resolver only.
- `evidence_items.csv` existence may be checked by resolver only.
- local exchange smoke does not open or parse evidence row files.
- no raw comments printed.
- no raw identifiers printed.

## E. Tests

Targeted tests cover:

- valid local exchange fixture returns `ready_for_metadata_only_handoff`.
- missing provider result JSON returns `blocked_missing_provider_result`.
- invalid provider result schema returns `needs_fix_metadata_contract`.
- `package_ready` plus safe package returns metadata-only ready status.
- `validation_warn` remains warning/manual-review oriented.
- `live_collection_not_authorized` remains blocked.
- package resolver `blocked_missing_package` propagates safely.
- package resolver `blocked_path_escape` propagates safely.
- provider metadata with actual `token` or `raw_author_id` returns `blocked_privacy_issue`.
- safety marker fields are allowed when they preserve the boundary.
- safe smoke summary does not include absolute filesystem paths.
- `evidence_items.jsonl` and `evidence_items.csv` are not opened or parsed.
- smoke helper does not write runtime files, Evidence Layer, cases, or `analysis_run`.
- smoke helper uses `tmp_path` synthetic fixtures and does not require a real collector export root.
- smoke helper produces concise safe summary counts.

Latest validation:

```text
python -m pytest backend/app/tests/test_private_collector_local_exchange_smoke.py
16 passed

python -m pytest backend/app/tests/test_private_collector_provider_result_reader.py
22 passed

python -m pytest backend/app/tests/test_private_collector_package_resolver.py
18 passed

python -m pytest backend/app/tests/test_local_exchange_reader.py
9 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
7 passed

python -m py_compile backend/app/services/private_collector_local_exchange_smoke.py
passed

git diff --check
passed
```

## F. Issues Found

P0 privacy/safety:

- none

P1 helper correctness blocker:

- none

P2 non-blocking limitation:

- smoke helper uses synthetic `tmp_path` fixtures only and does not read a real private collector export path.
- smoke helper is not wired to route/UI/production runtime.
- Search-to-Case product flow is still not implemented.

P3 nice-to-have:

- a future docs-only Search-to-Case product contract can define how user search becomes a full case workspace later.

## G. Recommended Next Step

Prefer Phase 8T-6 Search-to-Case product contract because the metadata-only smoke is clean and the intended future workflow is for search to create a full case workspace later.

Alternative safe option: Phase 8T-6 review-only staging import design.

Do not proceed to production import yet.

## H. Source Update Policy

No immediate Project Source update.

Batch later after actual connection implementation, review-only staging import, or another milestone-level change.

## I. Safety Confirmations

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
