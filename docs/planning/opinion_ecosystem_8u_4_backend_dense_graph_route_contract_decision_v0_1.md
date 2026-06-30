# Opinion Ecosystem 8U-4 Backend Dense Graph Route Contract Decision v0.1

## A. Decision / Status

phase = 8U-4

task = backend_dense_graph_route_contract_docs_only

decision = ready

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_changed = no

tests_changed = no

runtime_code_changed = no

route_changed = no

api_route_added = no

route_implemented = no

frontend_integration_approved_now = no

route_implementation_approved_now = no

production_ready = no

collector_run = no

private_collector_accessed = no

real_exchange_dir_read = no

real_api_called = no

real_llm_called = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

generated_response_text = no

publish_send_post_execute = no

project_source_files_created_in_repo = no

dense_graph_route_contract_created = yes

future_route_contract_selected = yes

future_route_disabled_by_default_required = yes

future_route_local_or_internal_only_required = yes

future_frontend_consumption_deferred = yes

future_route_implementation_requires_explicit_approval = yes

exact_future_route_approval_phrase = 批准 8U-5 backend dense graph route implementation

recommended_next_state = ready_to_request_explicit_8U_5_backend_dense_graph_route_implementation_or_tests_only_gate_or_pause

## B. Inputs from 8U-1 / 8U-2 / 8U-3

8U-1 created a backend-only dense opinion graph builder. It can turn safe in-memory evidence items into anonymous aggregate/proxy dense graph runs.

The Dong/Sun controlled sample smoke reported 240 `people_cluster_proxy` nodes, 800 edges, and 7 timeline buckets. That smoke was aggregate-only and did not imply full-web coverage, platform coverage, official verification, causal proof, prediction, or production score.

8U-2 packaged dense graph runs into generated-run-compatible dense graph attachment objects. The attachment remains backend-only and carries boundary flags, runtime side-effect flags, graph summary counts, previews, and warnings/blockers.

8U-3 integrated the base generated run and dense graph attachment into a backend-only generated-run dense graph integration object. 8U-3 still has no backend route and no frontend exposure.

## C. Route Contract Decision

Option 1: no route yet; keep service-only.

- Lowest immediate risk.
- Does not help future route consumers test an HTTP contract.
- Best if backend output shape still needs stabilization.

Option 2: new future internal/local-only dense graph generated-run route.

- Preferred future route direction.
- Keeps blast radius smaller than extending existing public/generated-run routes.
- Can be disabled by default and guarded by explicit sample allowlist.
- Avoids changing existing API response contracts.

Option 3: extend an existing generated-run route later.

- Deferred.
- Higher compatibility risk because it may change route-visible behavior for existing callers.
- Should only be considered after the internal/local route contract is proven safe.

Option 4: direct frontend consumption now.

- Rejected for 8U-4.
- Frontend remains frozen.
- Frontend consumption requires a separate explicit approval after backend route semantics are stable.

Conclusion:

- Create a contract for a new future backend dense graph route.
- Do not implement the route now.
- Do not extend existing routes now.
- Do not allow frontend consumption now.
- Prefer a future disabled-by-default internal/local route first, because it limits blast radius and avoids changing existing route contracts.

## D. Future Explicit Approval Protocol

Route implementation is not approved in 8U-4.

Future route implementation requires this exact approval phrase:

```text
批准 8U-5 backend dense graph route implementation
```

Do not treat any of these as approval:

- 下一步
- 继续
- 好
- git clean
- commit 完了
- Codex says ready

## E. Files Changed

- `docs/planning/opinion_ecosystem_8u_4_backend_dense_graph_route_contract_decision_v0_1.md`
- `docs/architecture/opinion_ecosystem_dense_graph_backend_route_contract_v0_1.md`
- `docs/architecture/opinion_ecosystem_dense_graph_route_response_schema_v0_1.md`
- `docs/architecture/opinion_ecosystem_dense_graph_route_test_plan_v0_1.md`

## F. Validation

Validation for this docs-only phase:

```text
git diff --check
git status --short
```

Docs-only scans:

- trailing whitespace scan
- placeholder keyword scan

Not run:

- backend tests
- frontend build
- browser smoke
- collector
- dense graph service execution

Reason: 8U-4 is docs-only and does not modify backend code, frontend code, tests, route runtime, or runtime files.

## G. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Contract Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- Route implementation remains unapproved.
- Frontend consumption remains deferred.
- Future route must be separately approved and tested.

### P3 Nice-to-have

- Add future tests-only route gate before any runtime implementation if the user wants one more safety checkpoint.

## H. Source Update Policy

No immediate Project Source update.

Do not create Source files in repo.

Do not create `docs/project_sources`.

## I. Safety Confirmations

- docs-only
- no backend code changed
- no frontend code changed
- no tests changed
- no runtime code changed
- no backend route implemented
- no API route added
- no frontend integration approved
- no route implementation approved
- no collector run
- no private collector access
- no real exchange dir read
- no real API called
- no real LLM called
- no Evidence Layer write
- no production case created
- no production analysis run created
- no B-end report runtime generated
- no Sandbox/public event runtime generated
- no generated response text
- no publish/send/post/execute behavior
- no Project Source files created in repo
- no GitHub Actions workflow recreated
