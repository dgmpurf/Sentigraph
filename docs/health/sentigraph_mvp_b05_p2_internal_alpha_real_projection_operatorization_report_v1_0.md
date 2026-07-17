# Sentigraph MVP-B05-P2 Synthetic-first Internal Alpha Real Projection Operatorization Report v1.0

## 1. Decision and privacy status

- Decision = `ready`
- privacy_issue_stop = `no`
- implementation mode = `synthetic_first_only`
- production/default registry state = `empty_and_disabled`
- real sample mapping present = `no`
- real B04 artifact, package, endpoint, or result replay = `no`
- persistence, mutation, trust promotion, production, public, export, and delivery authority = `none`

This slice exposes one separate Internal Alpha read-only operator view over the
existing B03 52-field in-memory projection. It does not convert that projection
into the F10 persisted governed-record surface and does not increase trust or
production authority.

## 2. Approval, Goal, accounting, and repository baseline

- approval SHA-256 = `b8592aee743b778cd21796ac95ab972b679bc66f046ecf135d9472901369f316`
- Goal = `MVP-B05-P2 Synthetic-first Internal Alpha Sample-handle Direct B03 52-field Read-only Operator Surface`
- Goal activation = `verified_fresh_goal`
- Goal replacement or reuse = `no`
- baseline = `sentigraph_internal_alpha_mvp_master_completion_baseline_v1_6`
- accounting before approval, engineering / fixed / conditional / risk = `5 / 2 / 2 / 1`
- accounting after approval, engineering / fixed / conditional / risk = `6 / 2 / 3 / 1`
- remaining fixed / conditional / risk = `0 / 1 / 1`
- approval classification = `conditional`
- repository identity = `dgmpurf/Sentigraph`
- branch = `main`
- starting HEAD = `10d06461244b7c7ba7b51073f3f7cc58d2664014`
- origin alignment before = `0 / 0`
- worktree before = `clean`
- B05-P1 contract = `verified_present`
- B03 service blob = `verified_against_approved_frozen_blob`
- B03 field contract = `52_fields_exact_order_verified`
- already completed or superseded = `no`

The B05-P2 approval and Goal are consumed and are not reusable.

## 3. Exact changed-file allowlist

The ready diff contains exactly these seven paths:

1. `backend/app/services/internal_alpha_local_exchange_review_projection.py`
2. `backend/app/api/v1/routes/internal_alpha_review_console.py`
3. `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py`
4. `frontend/src/api/sentigraphApi.js`
5. `frontend/src/pages/InternalAlphaReviewConsole.jsx`
6. `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py`
7. `docs/health/sentigraph_mvp_b05_p2_internal_alpha_real_projection_operatorization_report_v1_0.md`

- unexpected files = `0`
- API registration file changed = `no`
- `frontend/src/App.jsx` changed = `no`
- Project Source changed = `no`
- protected/runtime artifact present = `no`

## 4. Genuine TDD RED

The focused test file was the first implementation change. The service, route,
and frontend B05 surface did not yet exist.

- RED command = `python -m pytest app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py --maxfail=1`
- RED collection command = `python -m pytest app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py --collect-only -q`
- RED collected / failed / passed = `50 / 1 / 0`
- RED failure class = `ModuleNotFoundError`
- missing surface = `app.services.internal_alpha_local_exchange_review_projection`
- failure occurred before implementation = `yes`
- intentionally false assertion used = `no`

During implementation, intermediate focused runs exposed only test-fixture or
test-scope corrections before the final green run: a syntactically valid handle
was relabeled as truly malformed; a constant-backed route segment was accepted
without weakening its exact value assertion; and required boundary-copy words
were separated from mutation-control names. No production contract was weakened
to make the suite pass.

## 5. Backend service, validator, and immutable registry

The new service freezes:

- registry schema = `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1`
- route mode = `internal_alpha_read_only_local_exchange_projection_operator`
- capability label = `b05_local_exchange_projection_read_only`
- B05 gate = `SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED`
- safe-handle regex = `^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$`
- safe-handle maximum = `64`

The production/default registry is a process-local immutable mapping with zero
entries. It contains no real sample handle, real result name, path, root,
package location, provider payload, or metadata. Tests inject only an immutable
synthetic entry. Registry construction rejects duplicate handles.

Validation occurs before every registry lookup. The malformed matrix covers
empty, uppercase, leading/trailing hyphen, underscore, period, slash,
backslash, colon, percent encoding, query/fragment syntax, whitespace,
URL/URI syntax, traversal, overlength, and non-string values. Client filename,
path, root, adapter, package, or configuration input is not accepted.

The exact fail-closed order is:

1. validate the handle;
2. verify the shared Internal Alpha gate;
3. verify the B05 gate;
4. verify the three existing B01/B03 gates;
5. look up the immutable registry entry;
6. verify entry enablement, route mode, and capability;
7. verify bounded server-owned B01 configuration without opening a path;
8. call one B01 builder;
9. call one B03 builder;
10. verify the result keys against `PROJECTION_FIELDS`.

## 6. Exact 52-field sentinel matrix

Every B05 pre-builder failure is constructed by the existing B03
`build_disabled_local_exchange_review_only_projection` factory with
`result_file_name=None`.

| Condition | Error code | Registry/B01/B03 calls before return |
| --- | --- | --- |
| malformed handle | `invalid_sample_handle` | `0 / 0 / 0` |
| any required gate disabled | `b05_operator_surface_disabled` | `0 / 0 / 0` |
| unknown or disabled entry | `unknown_sample_handle` | lookup only, then `0 / 0` builders |
| absent, blank, or unbounded server configuration | `invalid_server_owned_configuration` | `0 / 0` builders |
| route-mode or capability mismatch | `registry_route_mismatch` | `0 / 0` builders |

For all five sentinels:

- ordered keys equal B03 `PROJECTION_FIELDS` and count = `52`;
- status = `projection_unavailable`;
- blockers = the singleton exact error code;
- candidate count = `0`;
- result name, upstream, identifier, summary, review, promotion, staging, and gate fields = `null`;
- warnings and all action lists = empty;
- metadata-only, review-only, human-review-required, and no-automatic-trust-upgrade = `true`;
- candidate persistence = `in_memory_only`;
- every write, production, frontend-action, public, export, path, raw-metadata, trust, readiness, promotion, and mutable-authority flag = `false`.

No envelope or B05/sample-handle field is added.

## 7. Synthetic ready-path and route proof

- selected route = `GET /api/v1/internal/alpha/review-console/local-exchange-projections/{sample_handle}`
- path parameters = `sample_handle` only
- capability = `b05_local_exchange_projection_read_only`
- route registration = `existing Internal Alpha router`
- API registration change = `no`
- ready and fail-closed HTTP status = `200`
- B01 staging-builder calls = `1`
- B03 projection-builder calls = `1`
- internal HTTP calls = `0`
- retries = `0`
- second requests = `0`
- F10 service imports/calls from B05 = `0`
- direct unmodified B03 response = `yes`
- response envelope = `none`

The synthetic ready test injects one bounded registry entry, one bounded B01
response, and call-counting builders. It proves the same ordered 52-field B03
object is returned by identity after the exact-key check.

The existing F10 `GET /projections/{projection_id}` branch, its governed-record
gate, its 46-field projection, and its frontend default selection remain
separate. B05 never imports or converts F10 persisted-record semantics.

## 8. Frontend contract

The API layer adds a single allowlisted-handle helper and one normalizer:

- helper = `getInternalAlphaLocalExchangeProjection(sampleHandle)`
- normalizer = `normalizeInternalAlphaLocalExchangeProjection`
- request count = `1`
- request method = `GET`
- query/body/configuration arguments = `none`
- alternate handle, retry, second call, or F10 fallback = `none`
- response keys = `52_exact_order`
- schema/version and all safety flags = `exactly_validated`
- unexpected/F10 persisted-record fields = `rejected`
- accepted object = `deep_frozen_transient_copy`
- browser storage or response logging = `none`

The page keeps F10 as the default and adds the explicit selected view
`internalAlphaLocalExchangeProjectionReview` with the separate
`localExchangeProjectionState`. Request phases are `idle`, `loading`, `loaded`,
`unavailable`, and `bounded_error`; projection phases are
`manual_review_required`, `blocked_upstream`, `projection_unavailable`, and
`ready_for_human_review`.

B05 is not fetched before explicit selection and is requested at most once for
the bounded handle. The page renders no result name, path, root, configuration,
raw response, raw metadata, or F10 persisted-record identifier. It has no
reload/retry, approve/reject, persistence, trust, promotion, production,
public, export, or delivery control.

Required copy is present exactly:

> Real metadata compatibility demonstrated for one approved sample.
> Read-only and human-review-only.
> Not a persisted governed record.
> Not trust approval.
> Not production readiness.
> Not full-web or full-platform coverage.

## 9. Validation evidence

### 9.1 Focused backend and static frontend tests

| Command/scope | Final result |
| --- | --- |
| new B05 focused test | `50 passed / 0 failed` |
| modified 8Z30 route/frontend smoke | `13 passed / 0 failed` |
| existing B03 projection focused test | `23 passed / 0 failed` |
| existing F10 governed-record focused test | `17 passed / 0 failed` |
| still-applicable 8Z22 Internal Alpha assertions | `16 passed / 1 superseded inventory assertion deselected` |
| existing local-exchange route test | `12 passed / 0 failed` |
| existing B01 local-exchange staging bridge test | `48 passed / 0 failed` |

The final repo-root combined run across all seven suites reported
`179 passed / 1 explicitly superseded legacy inventory assertion deselected`
in `1.85s`.

The complete legacy 8Z22 diagnostic was also run once. It reported
`14 passed / 3 failed`: two failures were caused only by invoking its
repo-root-relative static reads from the backend directory, and one was its
obsolete exact-one-route inventory. The two path assertions passed from the
repository root. The old one-route assertion is intentionally superseded by
the approved B05 route and the modified 8Z30 exact two-route inventory; the
8Z22 file was not allowlisted for modification.

The local-exchange route and B01 bridge tests were likewise first invoked from
the backend directory and reported `11 passed / 1 path-only failure` and
`47 passed / 1 path-only failure`. Their complete repo-root reruns are the
green `12` and `48` results recorded above.

### 9.2 Compilation, scans, and build

- changed-Python `py_compile` = `4 files / pass`
- exact changed-file allowlist scan = `pass`
- forbidden F10/database/persistence/network/provider/collector/LLM/browser imports in B05 service = `absent`
- discovery/glob/walk/latest/fallback/retry logic in B05 service = `absent`
- real B04 result name, artifact hash, or sample path in implementation/tests = `absent`
- frontend storage and raw response logging = `absent`
- route mutation methods = `absent`
- B03 service blob = `unchanged`
- Project Source change = `absent`
- `git diff --check` = `pass`
- frontend focused/static validation = `B05 50-test file plus 8Z30 13-test file / pass`
- frontend production build = `pass`, `4028 modules transformed`, `9.91s`
- package installation or upgrade = `none`

The build emitted only the repository's chunk-size advisory; it emitted no
build error.

## 10. Synthetic-only browser smoke

- browser capability = `available`
- browser = `Codex in-app browser`
- browser smoke = `pass`
- mode = `frontend preview plus repository-external CDP interception`
- Sentigraph backend started = `no`
- real registry mapping used = `no`
- synthetic response keys = `52`
- F10 view initially visible and default = `yes`
- B05 view visibly separate and explicitly selected = `yes`
- B05 request intercepted before backend/network delivery = `yes`
- loaded projection phase = `ready_for_human_review`
- required boundary copy visible = `yes`
- result name and F10 identifiers visible = `no`
- forms / mutation buttons = `0 / 0`
- filename/path/configuration inputs = `0`; the only input was the view combobox
- browser console warnings/errors = `0 / 0`
- committed screenshot or browser artifact = `no`

The B05 request was the single exact local B05 URL and was fulfilled in the
browser with the synthetic object. The existing default F10 GET attempted only
the deliberately unstarted local proxy and was refused; therefore no backend,
real endpoint, B04 artifact, or external network was reached. The screenshot
was temporary and was not written into the repository.

## 11. No-real-replay and no-side-effect ledgers

| Boundary | Count/status |
| --- | --- |
| production/default registry accesses | `empty registry only` |
| real B04 artifact/package accesses | `0` |
| accepted B04 endpoint replays | `0` |
| provider/collector/external-network/LLM calls | `0` |
| database/SQLite/persistence accesses | `0` |
| review-decision writes | `0` |
| Evidence Layer writes | `0` |
| production objects | `0` |
| trust/promotion actions | `0` |
| public/export/delivery actions | `0` |
| internal HTTP calls / retries / second requests | `0 / 0 / 0` |

## 12. Ready-only Git evidence and next boundary

Pre-staging evidence:

- Decision = `ready`
- privacy_issue_stop = `no`
- genuine RED = `established`
- all required focused tests = `pass`
- focused Python compilation = `pass`
- static scans = `pass`
- frontend production build = `pass`
- browser result = `synthetic_only_pass_with_local_F10_proxy_refusal_disclosed`
- exact seven-file allowlist = `satisfied`
- protected/runtime artifact = `absent`
- `git diff --check` = `pass`
- expected commit parent = `10d06461244b7c7ba7b51073f3f7cc58d2664014`
- required commit message = `Implement MVP-B05-P2 synthetic internal alpha projection operator surface`
- push mode = `ordinary_non_force`
- tag / release = `none / none`

The final commit hash, cached-diff result, push result, origin alignment, and
clean-worktree result are recorded in the terminal receipt because a commit
cannot contain its own hash.

Next boundary = independent ChatGPT acceptance. Do not access the B04 artifact
or endpoint, enable a real sample mapping, start B05-P3, or begin persistence,
production, public, export, or delivery work.
