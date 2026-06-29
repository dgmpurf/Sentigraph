# Private Collector 8T-13 Tiny Disabled Internal Operator Route Skeleton Report v0.1

## A. Decision / Status

```text
phase = 8T-13
task = tiny_disabled_internal_operator_read_only_staging_route_skeleton
privacy_issue_stop = no
docs_only = no
code_changed = yes
tests_changed = yes
runtime_code_changed = yes
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no
project_source_files_created_in_repo = no
api_route_added = yes
frontend_changed = no
persistent_staging_storage_created = no
route_enabled_by_default = no
route_methods_added = GET only
```

Decision: ready.

Implementation slice: 8T-13 tiny disabled-by-default internal operator read-only staging backend route skeleton.

## B. Implemented Scope

Changed files:

- backend/app/api/v1/routes/internal_operator_review_only_staging.py
- backend/app/api/v1/api.py
- backend/app/tests/test_internal_operator_review_only_staging_routes.py
- docs/health/private_collector_8t_13_tiny_disabled_internal_operator_route_skeleton_report_v0_1.md

The route skeleton is:

- backend-only
- GET-only
- disabled by default
- internal operator scoped
- metadata-only
- safe-schema-only
- synthetic fixture-only when explicitly enabled in tests

No frontend UI was added.

No persistent staging storage was added.

No Evidence Layer write, production case, `analysis_run`, report runtime, Sandbox/public event runtime, collector integration, or external delivery was added.

## C. Disabled-by-default Behavior

The route is controlled by:

```text
SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED
```

Accepted enabled values:

- `1`
- `true`
- `yes`

Everything else is disabled.

When disabled, both GET endpoints return:

```text
schema = internal_operator_review_only_staging_error_v0_1
error_code = route_disabled
path_exposed = false
raw_metadata_exposed = false
```

Disabled route behavior does not read package directories, evidence files, collector directories, runtime storage, or external data.

## D. Synthetic Fixture Mode

Synthetic fixture mode exists only when the route is explicitly enabled.

It is:

- in-memory
- safe metadata only
- not backed by disk
- not backed by private collector
- not backed by runtime storage
- not backed by Evidence Layer

The synthetic detail route returns:

```text
schema = internal_operator_review_only_staging_response_v0_1
```

The synthetic list route returns:

```text
schema = internal_operator_review_only_staging_response_list_v0_1
```

Unknown candidate IDs return a safe `not_found` error without leaking paths or raw metadata.

## E. Safe Response Boundary

Allowed safe response scope includes:

- staging candidate IDs
- analysis request/provider result IDs as synthetic safe IDs
- package name
- case hints
- validation status
- evidence/source/warning/error counts
- metadata summary
- validation summary
- coverage summary
- review status
- promotion status
- gate summary
- allowed action labels
- blocked action labels
- safety flags
- warnings
- blockers
- safe audit refs

Allowed actions are labels only:

- `continue_review`
- `request_more_metadata`
- `mark_manual_review_required`
- `reject_package`
- `block_privacy_issue`
- `request_future_evidence_preview_gate`
- `request_future_dedup_gate`
- `request_future_promotion_gate`

Blocked actions include:

- `approve_production_evidence`
- `create_production_case`
- `start_analysis_run`
- `generate_report`
- `generate_public_event`
- `generate_public_response`
- `publish`
- `send`
- `post`
- `execute`
- `target_individuals`

Safety flags include false values for collector, crawl, real API, real LLM, URL fetch, scraping, evidence row parsing, raw comment printing, raw identifier printing, secrets, Evidence Layer write, production case, analysis run, report runtime, Sandbox/public event runtime, and persistent staging storage.

Forbidden fields are not returned:

- raw evidence rows
- raw comments
- raw author ids/names
- profile URLs as actual values
- private messages
- cookies/sessions/tokens/passwords
- API keys
- browser profile paths
- absolute private paths
- response text
- generated public messages
- target user lists
- persuasion/truth scores
- official verification claims
- prediction probabilities
- psychological profiles
- personality diagnosis

## F. Tests

Validation run:

```text
python -m pytest backend/app/tests/test_internal_operator_review_only_staging_routes.py
12 passed

python -m pytest backend/app/tests/test_private_collector_review_only_staging.py
22 passed

python -m pytest backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py
20 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
7 passed

python -m py_compile backend/app/api/v1/routes/internal_operator_review_only_staging.py
passed
```

Route tests cover:

- disabled-by-default list route
- disabled-by-default detail route
- safe disabled error schema
- no absolute paths or raw metadata in disabled response
- disabled routes do not open evidence item files
- enabled synthetic fixture list response
- enabled synthetic fixture detail response
- required false safety flags
- review-only allowed labels
- blocked production/public/publish/send/post/execute/targeting labels
- no forbidden field keys in response
- no absolute private paths in response
- safe unknown-candidate error
- GET-only route family
- no file stream, ZIP, public URL, signed URL, or external delivery behavior in route module

## G. Issues Found

P0 privacy/safety:

- none.

P1 route correctness blocker:

- none.

P2 non-blocking limitation:

- route is a skeleton only.
- enabled mode is synthetic fixture-only.
- no persistent staging storage exists.
- no frontend exists.
- no production import exists.

P3 nice-to-have:

- future smoke checkpoint can verify route remains disabled-by-default after broader app imports.

## H. Recommended Next Step

Recommend:

```text
Phase 8T-14 internal operator route disabled-mode smoke/readiness checkpoint
```

Alternative:

```text
Phase 8T-14 route contract/source update planning
```

Do not recommend UI yet.

Do not recommend production import.

Do not recommend persistent staging storage.

Do not recommend evidence row preview.

## I. Source Update Policy

No immediate Project Source update.

Batch later after route skeleton readiness checkpoint or route milestone.

Do not create Source files in repo.

## J. Safety Confirmations

- no collector run
- no live crawl
- no browser automation
- no real API
- no real LLM
- no URL fetch/scrape
- no `evidence_items.jsonl` parsed
- no `evidence_items.csv` parsed
- no full evidence rows parsed
- no raw comments printed
- no raw author identifiers printed
- no cookies/tokens/sessions/profile paths read
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no frontend UI
- no persistent staging storage
- no Project Source files created in repo
- no GitHub Actions workflow recreated
- route disabled by default
- GET-only
- no `POST` / `PUT` / `PATCH` / `DELETE`
- no `FileResponse` / `StreamingResponse` / ZIP / public URL / signed URL / external delivery
