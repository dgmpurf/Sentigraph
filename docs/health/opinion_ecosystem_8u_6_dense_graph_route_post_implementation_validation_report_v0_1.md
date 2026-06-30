# Opinion Ecosystem 8U-6 Dense Graph Route Post-implementation Validation Report v0.1

## A. Decision / Status

phase = 8U-6
task = backend_dense_graph_route_post_implementation_validation
decision = ready
privacy_issue_stop = no
validation_only = yes
backend_only = yes
frontend_changed = no
route_changed = no
api_route_added = no
code_changed = no
tests_changed = no
route_implemented = yes
route_disabled_by_default = yes
route_get_only = yes
route_internal_local_only = yes
sample_allowlist_enforced = yes
arbitrary_path_input_allowed = no
private_collector_path_allowed = no
url_fetch_allowed = no
dense_graph_service_called_when_disabled = no
real_api_called = no
real_llm_called = no
collector_run = no
private_collector_accessed = no
real_exchange_dir_read = no
evidence_layer_write = no
production_case_created = no
production_analysis_run_created = no
generated_response_text = no
publish_send_post_execute = no

## B. Git / Repo State

- branch: `main`
- HEAD: `dcda98ee314c0a414b0d83bb88c7aaf7954f3313`
- latest commit: `dcda98e Implement 8U-5 dense graph internal route`
- working tree before report creation: clean
- unexpected modified/untracked files before report creation: none
- `docs/project_sources/`: not present
- visible local-only/generated paths:
  - `.env`: exists, untracked, ignored
  - `runtime/`: exists, untracked, ignored
  - `frontend/dist/`: exists, untracked, ignored
  - `.venv/`: exists, untracked, ignored
  - `node_modules/`: not present

## C. Route Behavior Summary

- Route path under validation:
  - `GET /api/v1/internal/opinion-ecosystem/dense-graph/generated-runs/{sample_id}`
- Registered prefix:
  - `/api/v1/internal/opinion-ecosystem/dense-graph`
- Route module:
  - `backend/app/api/v1/routes/opinion_ecosystem_dense_graph.py`
- Router registration:
  - `backend/app/api/v1/api.py` includes the route with tag `internal-opinion-ecosystem-dense-graph`.
- Env gate:
  - `SENTIGRAPH_OPINION_ECOSYSTEM_DENSE_GRAPH_ROUTE_ENABLED`
- Enabled values after normalization:
  - `1`
  - `true`
  - `yes`
- Default:
  - disabled
- GET-only route surface:
  - `POST` returned 405 in smoke.
  - `PUT` returned 405 in smoke.
- Allowed sample IDs:
  - `donglu-sunjihai-youth-football`
  - `helldivers-psn`
- Allowed query params:
  - `node_limit`
  - `edge_limit`
  - `include_previews`
- Bounded params:
  - `node_limit` lower bound 20, upper bound 240
  - `edge_limit` lower bound 50, upper bound 800
  - `include_previews=false` removes previews
- Disabled response:
  - schema: `sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1`
  - `route_status=disabled`
  - `error_code=route_disabled`
  - `path_exposed=false`
  - `raw_metadata_exposed=false`
  - `private_collector_path_exposed=false`
  - `evidence_rows_exposed=false`
  - dense graph service was not called while disabled
- Unsupported sample response:
  - `route_status=unsupported_sample`
  - `error_code=unsupported_sample`
  - no fallback to Helldivers or Dong/Sun
  - no generated run payload
  - no absolute path, private collector path, or evidence rows exposed
- Unknown query parameter response:
  - `error_code=unsupported_query_parameter`
  - safe error envelope
  - no evidence rows exposed

## D. Known Sample Smoke Summary

Only aggregate counts were printed. No raw evidence rows or comments were printed.

| sample_id | route_status | people_cluster_proxy_count | edge_count | timeline_bucket_count | frontend_ready | production_ready |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `donglu-sunjihai-youth-football` | `ready` | 240 | 800 | 7 | false | false |
| `helldivers-psn` | `ready` | 68 | 375 | 1 | false | false |

Both known sample responses included:

- `response_schema=sentigraph_opinion_ecosystem_dense_graph_route_response_v0_1`
- `recommended_visualization_mode=dense_sandbox_proxy_graph`
- `human_review_required=true`
- boundary flags present and true
- runtime side-effect values present in the response were false

## E. Safety Behavior

Confirmed:

- no arbitrary path input
- no private collector path input
- no URL input
- no package path input
- unsupported samples do not fallback
- disabled route does not call the dense graph service
- no raw author identifiers were printed
- no active `profile_url`, username, account id, cookie, token, password, API key, browser profile path, or private collector path was exposed by the smoke summary
- no generated public response text
- no auto-execute / publish / send / post behavior
- no Evidence Layer write
- no production case creation
- no production `analysis_run` creation
- no frontend route or UI exposure was added
- no public / C-end / B-end / customer dense graph route exists
- no file-byte response
- no ZIP/package generation
- no public URL / signed URL
- no external delivery
- no real API call
- no real LLM call
- no collector run

The route can load explicitly allowlisted controlled repo sample files under `docs/samples` when enabled. It does not accept arbitrary package paths, private collector paths, URLs, or caller-provided evidence file paths.

## F. Validation Commands and Results

Commands run:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git log --oneline -8
```

Result: passed. Initial working tree was clean; branch `main`; HEAD `dcda98ee314c0a414b0d83bb88c7aaf7954f3313`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_route.py
```

Result: passed, `13 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
```

Result: passed, `10 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
```

Result: passed, `9 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
```

Result: passed, `11 passed`.

```text
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
```

Result: passed, `7 passed`.

```text
python -m pytest backend/app/tests/test_local_exchange_reader.py
```

Result: passed, `9 passed`.

```text
python -m py_compile backend/app/api/v1/routes/opinion_ecosystem_dense_graph.py
python -m py_compile backend/app/api/v1/api.py
```

Result: passed.

```text
git diff --check
```

Result: passed.

```text
git status --short
```

Result before report creation: clean. After report creation, only this health report is expected to appear.

Additional local TestClient route smoke:

- disabled response checked
- disabled route service-call guard checked
- unsupported sample checked
- path traversal-like sample checked
- URL-like sample checked
- private-path-like sample checked
- known Dong/Sun sample checked
- known Helldivers sample checked
- bounds checked
- unknown query parameters checked
- `POST` / `PUT` method rejection checked

## G. Not Run and Why

- Frontend build not run because no frontend files changed and this was backend route validation only.
- Browser smoke not run because this was backend route validation only.
- Full backend pytest not run because the required focused contract, dense graph, golden contract, and local exchange tests passed.
- Collector not run by design.
- Real APIs not called by design.
- Real LLMs not called by design.
- URL fetching and scraping not performed by design.

## H. Issues

### P0 privacy/security stop

None.

### P1 route correctness / demo blocker

None.

### P2 stabilization / contract gaps

None.

### P3 cleanup / docs/source-sync notes

- Unknown query parameters currently return a safe envelope with `error_code=unsupported_query_parameter` and `route_status=unsupported_sample`. This is safe and accepted by the route contract smoke as a safe equivalent, but a future cleanup could make `route_status` more specific if desired.
- The successful route response does not expose a dedicated top-level `parsed_evidence_items_file` side-effect flag. The route behavior remains bounded because it only loads allowlisted controlled repo samples and does not accept arbitrary evidence file paths.

## I. Source Maintenance Note

source_update_recommended = no immediate

Reason:
Source 12 has already been manually added by the user for 8U-1 to 8U-5. 8U-6 adds only this validation report and no behavior changes. No immediate ChatGPT Project Source update is required.

Do not create `docs/project_sources/`.
Do not create ChatGPT Project Source files in repo.

## J. Next Recommendation

Prefer one of:

1. `8U-7 dense graph frontend/API integration decision docs-only`
2. `Dong/Sun historical replay browser regression smoke`
3. pause

Do not proceed to frontend implementation until the user explicitly approves that route.
