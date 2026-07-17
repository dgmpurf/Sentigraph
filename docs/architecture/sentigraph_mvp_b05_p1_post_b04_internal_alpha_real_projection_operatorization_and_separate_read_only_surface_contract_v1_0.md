# Sentigraph MVP-B05-P1 Post-B04 Internal Alpha Real Projection Operatorization and Separate Read-only Surface Contract v1.0

## 1. Decision and evidence basis

- decision = `ready`
- privacy_issue_stop = `no`
- docs_only = `yes`
- read_only_repository_audit = `yes`
- implementation_performed = `no`
- starting_commit = `61581c1d63350a85654493c3aaa1c7b01c4fc950`
- approval_sha256 = `af52e18e29fb78a7a10b35e3f7ce076557c227f9a2236be24c37d2be1cf3310b`
- B05-P1 approval reusable = `no`
- B05-P1 Goal reusable = `no`

MVP-B01, MVP-B02, MVP-B03, and MVP-B04 remain completed and independently
accepted. MVP-B04-D1 was not selected, was not triggered, and is not required.
The accepted B04 execution was evidence for this contract only; it was not
replayed. This audit performed no application import, event-loop creation,
artifact or package access, endpoint call, test, build, browser run, database
access, provider or collector call, external network call, model call, or
product execution.

### Audited B03/B04 surfaces

- `backend/app/services/local_exchange_review_only_projection_bridge.py`
- `backend/app/services/local_exchange_review_only_staging_bridge.py`
- `backend/app/api/v1/routes/internal_operator_review_only_staging.py`
- `backend/app/main.py`
- `backend/app/api/v1/api.py`
- `backend/app/tests/test_mvp_b03_local_exchange_review_only_projection_bridge.py`
- `backend/app/tests/test_internal_operator_review_only_staging_routes.py`
- `backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py`
- `docs/health/sentigraph_mvp_b03_local_exchange_review_only_projection_bridge_report_v1_0.md`
- `docs/health/sentigraph_mvp_b04_one_real_metadata_only_governed_read_only_projection_smoke_report_v1_0.md`

### Audited F10 Internal Alpha surfaces

- `backend/app/services/governed_nonproduction_review_console_projection.py`
- `backend/app/api/v1/routes/internal_alpha_review_console.py`
- `backend/app/api/v1/api.py`
- `backend/app/tests/test_mvp_f10_p2_governed_nonproduction_review_console_projection.py`
- `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py`
- `frontend/src/api/sentigraphApi.js`
- `frontend/src/pages/InternalAlphaReviewConsole.jsx`
- `frontend/src/data/internalAlphaReviewConsoleStaticFixture.js`
- `frontend/src/App.jsx`
- `docs/architecture/sentigraph_mvp_f10_p1_governed_nonproduction_record_to_internal_review_console_read_only_integration_contract_v1_0.md`
- `docs/health/sentigraph_mvp_f10_p2_governed_nonproduction_record_to_internal_review_console_read_only_integration_report_v1_0.md`

No unrelated repository file was inspected. The current frontend contains no
reference to the B03 projection schema, B03 local-exchange projection route, or
the approved B04 sample handle. The B03/B04 operator surface described below
does not exist in the current frontend.

## 2. Semantic separation matrix

| Dimension | B03/B04 local-exchange projection | F10 governed-record projection |
| --- | --- | --- |
| Schema | `sentigraph_local_exchange_review_only_candidate_projection_v0_1` | `sentigraph_internal_alpha_governed_nonproduction_record_review_projection_v0_1` |
| Version | `0.1` | `0.1` |
| Exact field count | `52` | `46` |
| Object meaning | In-memory review candidate projection | Persisted governed nonproduction record projection |
| Source boundary | Local-exchange Provider Result metadata through the bounded B01 response | F09/F10 exact-target record and reservation integrity lineage |
| Persistence identity | None | Exact `persisted_record_id` and reservation identity |
| Actual-column audit semantics | None | Exact record and reservation actual-column verification |
| Candidate persistence | `in_memory_only` | Reads an already persisted governed record |
| Human authority | Human review required; no trust upgrade | Human review required; no trust upgrade |
| Promotion | Still required; not completed | Production promotion remains blocked |
| Mutation authority | None | None on the F10 read-only surface |
| Current backend family | Internal staging review-only route | Internal Alpha review-console projection-ID route |
| Current frontend | No integration | Existing Internal Alpha review-console surface |

### Exact B03/B04 52-field order

| No. | Field |
| ---: | --- |
| 1 | `projection_schema` |
| 2 | `projection_version` |
| 3 | `projection_mode` |
| 4 | `projection_status` |
| 5 | `projection_error_code` |
| 6 | `source_chain_boundary` |
| 7 | `result_file_name` |
| 8 | `upstream_schema` |
| 9 | `upstream_status` |
| 10 | `reader_status` |
| 11 | `adapter_status` |
| 12 | `provider_result_status` |
| 13 | `package_resolution_status` |
| 14 | `candidate_count` |
| 15 | `staging_candidate_id` |
| 16 | `gate_result_id` |
| 17 | `analysis_request_id` |
| 18 | `provider_result_id` |
| 19 | `package_name` |
| 20 | `case_id_hint` |
| 21 | `case_title_hint` |
| 22 | `validation_summary` |
| 23 | `coverage_summary` |
| 24 | `review_status` |
| 25 | `promotion_status` |
| 26 | `staging_status` |
| 27 | `gate_summary` |
| 28 | `warnings` |
| 29 | `blockers` |
| 30 | `allowed_actions` |
| 31 | `blocked_actions` |
| 32 | `metadata_only` |
| 33 | `review_only` |
| 34 | `human_review_required` |
| 35 | `no_automatic_trust_upgrade` |
| 36 | `candidate_persistence` |
| 37 | `persistent_staging_write` |
| 38 | `review_decision_write` |
| 39 | `evidence_layer_write` |
| 40 | `production_evidenceitem_created` |
| 41 | `production_case_created` |
| 42 | `analysis_run_created` |
| 43 | `analysis_result_created` |
| 44 | `frontend_action_enabled` |
| 45 | `public_output_enabled` |
| 46 | `export_delivery_enabled` |
| 47 | `path_exposed` |
| 48 | `raw_metadata_exposed` |
| 49 | `trust_approved` |
| 50 | `production_ready` |
| 51 | `promotion_completed` |
| 52 | `mutable_authority_granted` |

The ready B03/B04 object requires one candidate, safe metadata statuses,
consistent gate summaries, no blocker, `candidate_persistence = in_memory_only`,
`human_review_required = true`, `no_automatic_trust_upgrade = true`, and
`promotion_status = promotion_required`. Its persistence, review-write,
Evidence Layer, production, frontend-action, public-output, delivery, trust,
promotion-completed, and mutable-authority flags remain false.

### Exact F10 46-field order

| No. | Field |
| ---: | --- |
| 1 | `projection_schema` |
| 2 | `projection_version` |
| 3 | `projection_id` |
| 4 | `projection_status` |
| 5 | `projection_mode` |
| 6 | `source_chain_boundary` |
| 7 | `upstream_source_chain_boundary` |
| 8 | `review_disposition` |
| 9 | `target_state_outcome` |
| 10 | `persisted_record_id` |
| 11 | `attempt_reservation_id` |
| 12 | `candidate_identity_digest` |
| 13 | `input_safe_hash` |
| 14 | `gate_contract_safe_hash` |
| 15 | `activation_decision_safe_hash` |
| 16 | `record_snapshot_digest` |
| 17 | `reservation_snapshot_digest` |
| 18 | `record_count_class` |
| 19 | `reservation_count_class` |
| 20 | `expected_record_present` |
| 21 | `expected_reservation_present` |
| 22 | `unexpected_record_present` |
| 23 | `unexpected_reservation_present` |
| 24 | `record_actual_columns_verified` |
| 25 | `reservation_actual_columns_verified` |
| 26 | `record_canonical_hash_verified` |
| 27 | `reservation_canonical_hash_verified` |
| 28 | `record_exact_binding_verified` |
| 29 | `reservation_exact_binding_verified` |
| 30 | `record_reservation_cross_binding_verified` |
| 31 | `implementation_mutating_attempt_consumed` |
| 32 | `governed_nonproduction_record_exists` |
| 33 | `record_status` |
| 34 | `human_review_required` |
| 35 | `no_automatic_trust_upgrade` |
| 36 | `production_evidenceitem_created` |
| 37 | `production_case_changed` |
| 38 | `downstream_runtime_called` |
| 39 | `internal_read_only_projection_ready` |
| 40 | `operator_runtime_ready` |
| 41 | `production_ready` |
| 42 | `public_ready` |
| 43 | `allowed_actions` |
| 44 | `blocked_actions` |
| 45 | `warnings` |
| 46 | `blockers` |

F10 is bound to exact persisted-record and reservation identities, canonical
hash and binding checks, actual-column verification, an already consumed
mutating-attempt lineage, and seven exact-target outcomes. Its existing client
selects `governed-nonproduction-record-review-v0-1`, calls the projection-ID
route once on page mount, and renders that persisted governed-record state.

B03/B04 must never be cast, renamed, wrapped, or described as an F10 persisted
governed record. F10 must never be used as proof that a B03/B04 in-memory
candidate was persisted. The two surfaces may share visual vocabulary, layout
primitives, and generic read-only status components only while their data
contracts, source-chain labels, state branches, and provenance copy remain
distinct.

## 3. Selected B05 operator-surface architecture

- selected_architecture = `separate_internal_alpha_sample_handle_direct_b03_projection`
- selected_operator_route = `GET /api/v1/internal/alpha/review-console/local-exchange-projections/{sample_handle}`
- route_mode = `internal_alpha_read_only_local_exchange_projection_operator`
- capability_label = `b05_local_exchange_projection_read_only`
- frontend_surface_id = `internalAlphaLocalExchangeProjectionReview`
- response_schema = `sentigraph_local_exchange_review_only_candidate_projection_v0_1`
- response_field_count = `52`
- response_envelope = `none`

Exactly one architecture is selected. It adds a separate GET-only operation to
the existing Internal Alpha review-console router. The operation accepts only a
safe sample handle, resolves it through a server-owned registry, calls the B01
staging builder once and the B03 projection builder once, and returns the exact
ordered 52-field B03 projection directly.

No envelope is selected. The existing B03 route already proves that the
52-field object is a valid direct route response, and the current FastAPI router
does not require an envelope. Adding one would create another schema and make
it easier to confuse B03/B04 with the F10 governed-record envelope.

The selected operation is owned by the existing
`backend/app/api/v1/routes/internal_alpha_review_console.py` router and a
proposed dedicated adapter service. The existing registration in
`backend/app/api/v1/api.py` already supplies the Internal Alpha prefix, so no
API-registration change is needed. The existing frontend hash route remains
`#/internal-alpha/review-console`; B05 is a distinct view branch inside that
page, not a public route and not a replacement for F10.

Every successful or fail-closed response must retain the exact B03 field order,
schema, and 52-field count. The service must compare the returned key tuple to
the frozen B03 `PROJECTION_FIELDS` tuple. It must not convert the response to the
F10 schema, add persisted-record fields, invoke the F10 service, call either
existing HTTP endpoint internally, persist a decision, or expose mutation
controls.

## 4. Server-owned sample-handle contract

- registry_schema = `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1`
- registry_owner = `backend/app/services/internal_alpha_local_exchange_review_projection.py`
- accepted_demo_handle = `helldivers2-psn-demo`
- handle_maximum_length = `64`
- handle_pattern = `^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$`
- registry_default = `disabled`
- unknown_handle_result = `projection_unavailable / unknown_sample_handle`
- malformed_handle_result = `projection_unavailable / invalid_sample_handle`

The client may send only a handle that matches the exact pattern. Lowercase
ASCII letters, digits, and internal hyphens are the only allowed characters.
The validator rejects leading or trailing hyphens, periods, underscores,
slashes, backslashes, colons, percent encoding, query or fragment markers,
whitespace, URL syntax, drive syntax, traversal tokens, empty strings, and
overlength values before registry lookup.

The immutable registry owns the mapping from handle to a server-owned result
basename and server-owned bridge configuration reference. Neither the mapping
nor an enabled entry is client-controlled. Duplicate handles are rejected when
the registry is constructed. Registry lookup performs no directory listing,
glob, latest-file selection, fallback selection, or search. An unknown handle
fails closed and never selects another entry.

The client must not submit or store an independent result filename, directory,
absolute or relative path, export root, results root, adapter ID, provider
schema override, latest-file selector, package path, collector root, or
configuration override. No such value may appear in a query string, request
body, header, browser-storage key, or frontend control.

The accepted demo handle is recorded only as a safe identifier and does not
enable a real mapping. B05-P1 grants no artifact access or endpoint replay. A
future synthetic P2 may install only a synthetic injected registry entry in
tests. Enabling a real server-owned mapping requires a later, separate exact
authorization beyond P2.

## 5. Gate and authority contract

The exact proposed backend gate conjunction is:

1. `SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED = true`
2. `SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED = true`
3. `SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED = true`
4. `SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED = true`
5. `SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED = true`
6. the exact sample handle exists as one enabled server-owned registry entry;
7. the server-owned B01 configuration is complete and internally valid.

Every Boolean gate defaults disabled and uses the existing strict true-value
convention. Failure of any conjunct returns an exact 52-field fail-closed B03
projection before B01/B03 work. The new B05-specific environment variable is
proposed only by this contract; B05-P1 does not add or set it.

`SENTIGRAPH_INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_ENABLED` is the F10
governed-record gate and is not B05 authority. Its value must not enable,
disable, or alter the B05 branch. The shared Internal Alpha family gate is only
a common internal-visibility boundary. B05 also retains all existing B01 and
B03 gates and therefore cannot weaken them.

The frontend surface requires explicit selection of
`internalAlphaLocalExchangeProjectionReview` and an allowlisted safe handle.
The presence of the backend route, a successful backend health check, or the
F10 view being visible does not select or authorize B05.

No gate creates persistence, review-decision, trust, promotion, production,
public, export, delivery, writer, database, or mutable authority. All labels
remain human-review-only.

## 6. Frontend read-only state contract

The future frontend must add a state branch separate from the existing F10
`routeState` branch. It must not replace the current F10 projection selection or
reuse F10's persisted-record status map.

- API helper = `getInternalAlphaLocalExchangeProjection(sampleHandle)`
- response validator = `normalizeInternalAlphaLocalExchangeProjection`
- state branch = `localExchangeProjectionState`
- selected view = `internalAlphaLocalExchangeProjectionReview`
- selected sample handle = `helldivers2-psn-demo`
- request phases = `idle`, `loading`, `loaded`, `unavailable`, `bounded_error`
- projection phases = `manual_review_required`, `blocked_upstream`,
  `projection_unavailable`, `ready_for_human_review`

`loaded` means that schema, version, exact key order, field count, handle-bound
server response, privacy flags, and B03 invariants passed validation. A loaded
projection is still only human-review-ready. `unavailable` covers disabled or
unknown server-owned state. `bounded_error` contains only a safe error code and
must retain no response body. `manual_review_required` and `blocked_upstream`
remain distinct from ready.

The helper receives only a client-side allowlisted handle, validates it before
encoding, issues one GET, and performs no retry, second request, alternate
handle, fallback fixture selection, or projection-ID fallback. The page stores
no filename or path field independently. The exact 52-field object may exist
only in transient component memory after validation; `result_file_name` must
not be copied, rendered, logged, serialized, cached, or written to browser
storage.

The B05 branch contains no approve or reject button, decision-ledger POST,
trust-upgrade control, promotion action, persistence action, retry loop,
automatic fallback, export control, public action, filename input, path input,
or configuration input.

The visible B05 copy is exactly:

```text
Real metadata compatibility demonstrated for one approved sample.
Read-only and human-review-only.
Not a persisted governed record.
Not trust approval.
Not production readiness.
Not full-web or full-platform coverage.
```

The current frontend does not implement this state, helper, selection, copy, or
surface. This is a future contract only.

## 7. Data and privacy boundary

The operator boundary permits only the exact bounded 52-field projection and
the safe sample handle. It permits no source payload, package content,
evidence/source/log row, external absolute path, private collector root,
credential, secret, author identity, unbounded exception text, or endpoint
response log.

The frontend must not retain a filename, path, export root, results root,
adapter value, package location, or collector location in local storage,
session storage, IndexedDB, URL state, telemetry, analytics, console output, or
an independent React state field. The server-returned 52-field object remains
transient and read-only; its basename field is not a client input and is never
displayed or persisted.

No source payload or package content may be returned under a renamed field,
nested object, debug field, error detail, warning, or log. The frontend must
discard an unexpected schema or field set without logging the response.

## 8. Failure semantics

| Condition | Exact fail-closed result | Forbidden follow-up |
| --- | --- | --- |
| Malformed handle | `projection_unavailable / invalid_sample_handle` | No registry lookup or builder call |
| Unknown handle | `projection_unavailable / unknown_sample_handle` | No alternate handle or fixture |
| Any disabled gate | `projection_unavailable / b05_operator_surface_disabled` | No B01/B03/F10 call |
| Incomplete server-owned configuration | `projection_unavailable / invalid_server_owned_configuration` | No client override |
| Upstream schema mismatch | Existing B03 `projection_unavailable / unexpected_upstream_schema` | No coercion |
| Candidate count not one | Existing B03 `projection_unavailable / candidate_count_not_one` | No candidate selection |
| B01 manual-review response | Existing B03 `manual_review_required / upstream_manual_review_required` | No trust upgrade |
| B01 blocked or unavailable | Existing B03 `blocked_upstream / upstream_not_ready` | No retry or fallback |
| Unexpected 52-field deviation | `projection_unavailable / projection_contract_deviation` | No partial response |
| Path or configuration injection attempt | `projection_unavailable / invalid_sample_handle` | No normalization into a path |
| Route/registry mismatch | `projection_unavailable / registry_route_mismatch` | No directory discovery |
| Frontend schema mismatch | `bounded_error / frontend_projection_contract_mismatch` | Discard body; no second request |

All backend outcomes retain the exact 52-field B03 schema and field order.
No failure may automatically select another sample, latest sample, replacement
file, fallback fixture, F10 projection, or second request.

## 9. Future B05-P2 synthetic-first implementation slice

B05-P2 is not authorized by this document. The only eligible future slice is a
synthetic-first implementation that performs zero real B04 artifact access,
zero replay of either accepted B04 endpoint, zero provider/collector/network
call, zero persistence or mutation, and zero change to B01, B03, B04, or F10
semantics.

The backend focused tests must inject a synthetic registry entry and synthetic
B01 response. The production adapter path must still compose exactly one call
to `build_local_exchange_review_only_staging_response` followed by exactly one
call to `build_local_exchange_review_only_projection`; tests may substitute the
first call to prevent filesystem access while exercising the real B03
projection semantics. There is no internal HTTP call and no retry.

The frontend adds one separate helper and one separate state/view branch on the
existing Internal Alpha page. F10 remains the existing default governed-record
branch and its projection ID, helper, state mapping, route, 46-field contract,
and persisted identity display remain unchanged.

### Exact candidate B05-P2 changed-file allowlist

- future_P2_candidate_changed_file_count = `7`
- wildcard_entries = `0`
- convenience_refactors = `0`

| No. | Repository-relative path | Status | Candidate responsibility |
| ---: | --- | --- | --- |
| 1 | `backend/app/services/internal_alpha_local_exchange_review_projection.py` | `proposed_new_file` | Handle validator, immutable registry, B01/B03 composition, exact 52-field check |
| 2 | `backend/app/api/v1/routes/internal_alpha_review_console.py` | existing | One separate GET route and B05-specific gate; F10 branch unchanged |
| 3 | `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py` | `proposed_new_file` | Synthetic backend, route, contract, privacy, zero-side-effect, and frontend-static checks |
| 4 | `frontend/src/api/sentigraphApi.js` | existing | Safe-handle allowlist, GET helper, exact response normalizer |
| 5 | `frontend/src/pages/InternalAlphaReviewConsole.jsx` | existing | Separate B05 state/view branch and required read-only copy |
| 6 | `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py` | existing | Extend directly coupled frontend/static safety ownership without weakening F10 assertions |
| 7 | `docs/health/sentigraph_mvp_b05_p2_internal_alpha_real_projection_operatorization_report_v1_0.md` | `proposed_new_file` | Bounded future P2 evidence report |

This is a candidate allowlist, not authorization. No change is proposed for
`backend/app/api/v1/api.py` because the Internal Alpha router is already
registered. No change is proposed for `frontend/src/App.jsx` because the
Internal Alpha hash page already exists. The F10 focused test remains unchanged
and is run only as a regression check under future P2 authority.

## 10. Future P2 validation matrix

No validation in this section is executed by B05-P1.

### Backend evidence

| Validation | Required future evidence |
| --- | --- |
| Genuine RED | Focused test fails because the new service/route is absent before implementation |
| Handle validator | Exact regex, maximum length, safe demo handle, and every forbidden character class |
| Registry | Immutable server-owned map, duplicate rejection, unknown-handle fail-closed behavior |
| Disabled behavior | Every gate defaults disabled and prevents registry/builders as specified |
| Exact response | Schema/version/key order/count equal the frozen B03 52-field contract |
| Builder path | Exactly one B01 builder and one B03 builder call; no endpoint call |
| F10 separation | No F10 service import, projection ID, 46-field conversion, or persisted-record identifier |
| Side effects | Zero writes, database calls, network calls, provider/collector calls, subprocesses, and retries |
| Compilation | Focused `py_compile` only for changed Python files |
| Static scan | Forbidden imports, path exposure, mutation verbs, delivery behavior, and route-method scan |
| Regression | Existing B03, F10, route-family, and 8z30 focused tests remain green |
| Git hygiene | Exact allowlist plus `git diff --check` and cached diff validation |

### Frontend evidence

| Validation | Required future evidence |
| --- | --- |
| Response type | Exact 52 fields; no F10 type or envelope accepted |
| Separate state | B05 state/view branch exists and F10 branch remains byte-for-byte semantically unchanged |
| State coverage | Loading, loaded, unavailable, blocked-upstream, manual-review, ready, and bounded-error states |
| Controls | No approve/reject, mutation, decision, persistence, trust, promotion, public, export, or retry control |
| Input | Only one allowlisted safe handle; no filename, path, root, adapter, package, or free-form input |
| API behavior | One encoded GET; no fallback and no second call |
| Copy | Exact separation and human-review-only text is visible |
| Focused tests | Frontend API/state/component static tests pass when present |
| Build | Frontend production build passes under future P2 authority |
| Browser | Conditional smoke follows Section 11 only |

## 11. Browser boundary

- browser execution in B05-P1 = `forbidden`
- browser execution performed in B05-P1 = `no`

A future B05-P2 browser smoke is allowed only when its separate approval names
browser execution and the capability is available. It must use synthetic
fixture/server state only, perform no real B04 artifact access or endpoint
replay, verify no console errors, verify that F10 and B05 are visibly distinct,
verify the exact read-only copy, and verify the absence of mutation controls,
filename/path inputs, and public/export actions.

If browser capability is unavailable, the future report must record
`browser_smoke = not_run` and rely on the authorized frontend build and focused
static tests. Unavailability is not permission to use another browser or a real
sample.

## 12. Accounting and next boundary

- consumed engineering/fixed/conditional/risk = `5/2/2/1`
- remaining fixed/conditional/risk = `0/2/1`
- B05-P1 classification = `fixed`
- B05-P1 completed = `yes` only after this contract is accepted, committed, and pushed
- B05-P2 eligible candidate = `yes`
- B05-P2 authorized = `no`
- B05-P2 executed = `no`
- Project Source changed = `no`
- tag = `none`
- release = `none`

Accounting arithmetic: B05-P1 consumes one engineering event and the last
fixed prompt. The accepted ledger moves from `4/1/2/1` consumed with `1/2/1`
remaining to `5/2/2/1` consumed with `0/2/1` remaining. Conditional and risk
capacity is unchanged and does not authorize B05-P2.

Next boundary:

1. independent ChatGPT acceptance;
2. optional Project Source decision;
3. separate B05-P2 route selection;
4. fresh exact approval;
5. fresh Goal.

Do not implement B05-P2. Do not access the B04 artifact or endpoint. Do not
import the application, create an event loop, run tests/build/browser, or
perform persistence, production, public, export, or delivery actions under this
contract.
