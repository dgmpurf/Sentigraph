# Sentigraph MVP-B01 Local Exchange to Review-only Staging Runtime Bridge Report v1.0

## Decision

`READY`

MVP-B01 adds one backend-only, internal-only, GET-only, disabled-by-default bridge from one explicitly named local-exchange provider-result metadata file to exactly one in-memory review-only staging candidate and gate. The bridge performs no discovery, persistence, production import, evidence-row parsing, provider execution, network activity, or public delivery.

## Privacy and product boundary

- Metadata-only and review-only: yes.
- Real provider-result files accessed: 0.
- Real packages accessed: 0.
- Evidence row files parsed: 0.
- Persistent staging writes: 0.
- Evidence Layer writes: 0.
- Production EvidenceItem, case, analysis run, analysis result, report, or public-event actions: 0.
- Network, scraping, browser, provider, collector, or LLM calls: 0.
- Frontend changes: 0.
- Tag, release, export, public delivery, and Project Source changes: 0.

## Goal and authority

- Goal: `MVP-B01 Local Exchange to Review-only Staging Bridge`
- Task mode: Goal; one new Goal was created and activated before formal repository preflight.
- Starting commit: `26ac82c27636603c5b92320df9d88d371c9bf894`
- Starting branch: `main`
- Starting repository: `dgmpurf/Sentigraph`
- Starting alignment: `HEAD == origin/main`, ahead/behind `0/0`, clean worktree.
- Approval SHA-256: `9575f33439760a9216ab2d2be8b5274bb1db0c7e882bb185225d0e763e055b0e`
- Approval phrase verification: exactly one phrase was found and its UTF-8 SHA-256 matched the approved digest.
- Approval binding: `APPROVE_SENTIGRAPH_MVP_B01_LOCAL_EXCHANGE_PROVIDER_HANDOFF_TO_REVIEW_ONLY_STAGING_RUNTIME_BRIDGE_IMPLEMENTATION_BIND_STARTING_COMMIT_26AC82C27636603C5B92320DF9D88D371C9BF894_BACKEND_ONLY_INTERNAL_ONLY_DISABLED_BY_DEFAULT_GET_ONLY_METADATA_ONLY_IMPLEMENT_DETERMINISTIC_PROVIDER_RESULT_V1_TO_V0_1_COMPATIBILITY_ADAPTER_COMPOSE_LOCAL_EXCHANGE_READER_PRIVATE_COLLECTOR_PROVIDER_RESULT_READER_SAFE_PACKAGE_RESOLVER_AND_IN_MEMORY_REVIEW_ONLY_STAGING_ADD_ONE_STRICT_BASENAME_LOCAL_EXCHANGE_CANDIDATE_ENDPOINT_PRESERVE_EXISTING_SYNTHETIC_ENDPOINT_BEHAVIOR_USE_SERVER_OWNED_RESULTS_DIR_AND_EXPORT_ROOT_TDD_FOCUSED_REGRESSIONS_PYCOMPILE_STATIC_SAFETY_SCANS_AND_DIFF_CHECK_READY_ONLY_COMMIT_PUSH_NO_REAL_LOCAL_PROVIDER_FILE_ACCESS_NO_DIRECTORY_DISCOVERY_NO_EVIDENCE_ROW_OR_PACKAGE_ROW_PARSE_NO_PERSISTENT_STAGING_NO_EVIDENCE_LAYER_WRITE_NO_PRODUCTION_EVIDENCEITEM_CASE_ANALYSIS_RUN_ANALYSIS_RESULT_NO_FRONTEND_NO_COLLECTOR_OR_PROVIDER_JOB_EXECUTION_NO_NETWORK_SCRAPING_LLM_PROJECT_SOURCE_TAG_RELEASE_EXPORT_OR_PUBLIC_DELIVERY`

## Baseline v1.4 approval accounting

This activation consumes the final Baseline v1.4 fixed reserve:

- engineering prompts consumed: 3
- fixed reserve: 3
- fixed reserve remaining: 0
- conditional reserve remaining: 6
- risk reserve remaining: 2

No P2, P3, P4, or F12 authority was reused.

## Architecture

The new route reads only three server-owned settings and the strict path parameter:

1. The existing internal staging route gate is checked first.
2. The B01 local-exchange bridge gate is checked second.
3. The path parameter is validated as one strict JSON basename before any reader call.
4. A `LocalExchangeReaderConfig` is built from server-owned values.
5. `local_exchange_reader.read_provider_result_metadata` is called exactly once for the one named file inside `resultsDir`.
6. A pure deterministic adapter maps validated `sentigraph_provider_job_result_v1` / `1.0` metadata into an in-memory `sentigraph_provider_job_result_v0_1` / `0.1` dictionary.
7. `private_collector_provider_result_reader` consumes that dictionary directly; it does not reopen a provider-result file.
8. The existing safe package resolver resolves only the explicit package reference beneath the configured export root and reads only its fixed metadata allowlist.
9. Exactly one nonpersistent staging candidate and exactly one gate are created in memory for an adapted result, including safe manual or blocked package outcomes.
10. Only a safe response envelope and safe staging/gate summaries are returned.

There is no list/latest fallback, directory enumeration, glob, recursive glob, walk, package discovery, absolute-path fallback, writer, database, queue, runtime job, or product import.

## Endpoint and gates

- Method: `GET`
- Effective endpoint: `/api/v1/internal/staging/review-only/local-exchange/candidates/{result_file_name}`
- Existing gate: `SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED`
- B01 gate: `SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED`
- Both gates default disabled and accept only the existing bounded true values `1`, `true`, and `yes`.
- Primary-gate failure returns `route_disabled` before bridge or file access.
- B01-gate failure returns `local_exchange_route_disabled` before bridge or file access.
- Existing synthetic `/candidates` and exact `/candidates/{staging_candidate_id}` behavior remains unchanged.

Server-owned configuration:

- `SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR`
- `SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT`
- `SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID`

The client supplies only `result_file_name`.

## Strict-basename contract

The accepted name is a bounded ASCII basename beginning with an alphanumeric character, continuing only with alphanumeric characters, dot, underscore, or hyphen, and ending exactly in `.json`. The maximum length is 160 characters.

The bridge rejects empty names, `.`, `..`, slash, backslash, drive/colon syntax, NUL/control characters, URL/URI syntax, whitespace, percent-encoded URL-like names, non-JSON suffixes, path components, and oversized names before constructing or reading a candidate file. The local-exchange reader independently enforces containment inside the configured results directory.

## Adapter input, output, and field mapping

- Input schema: `sentigraph_provider_job_result_v1`
- Input contract version: `1.0`
- Output schema: `sentigraph_provider_job_result_v0_1`
- Output contract version: `0.1`

| v1 actual field | v0.1 field | Rule |
| --- | --- | --- |
| `provider_result_id` | `provider_result_id` | actual nonempty safe identifier |
| `provider_job_id` | `provider_job_id` | actual nonempty safe identifier |
| `sentigraph_request_id` | `request_id` | actual nonempty safe identifier |
| `provider_type` | `provider_type` | actual value; never fabricated |
| `adapter_id` | `adapter_id` | actual value, already matched to server configuration by the v1 reader |
| fixed adapter contract | `contract_version` | deterministic `0.1` |
| source `status` | `status` | exact bounded mapping below |
| `package_contract` | `package_contract` | actual nonempty safe identifier |
| `package_id`, `package_role`, `package_index_ref` | `package_reference` | explicit package identity only |
| `summary.evidence_items` | `metadata_summary.evidence_count` | actual nonnegative integer |
| `summary.sources` | `metadata_summary.source_count` | actual nonnegative integer |
| `summary.comment_samples` | `metadata_summary.comment_count` | actual nonnegative integer |
| `validation_summary` | `validation_summary` | actual status/error/warning values |
| `coverage_note` | `coverage_note` | actual bounded text |
| `safety_markers` | `safety_markers` | all six actual markers must be present with boundary-preserving values |
| `created_at` | `created_at` | actual bounded value; never synthesized |

The adapter stops before package resolution if required provenance, package identity, validation metadata, coverage, timestamp, or safety markers are missing or unsafe. It does not invent provider type, timestamp, provenance, package location, or safety facts.

## Status mapping

| v1 source status | v0.1 / bridge outcome |
| --- | --- |
| `package_ready` | `package_ready`, then existing reader/resolver/staging result |
| `needs_manual_snapshot` | `manual_review_required`; never ready |
| `blocked` | `blocked_safety` |
| `invalid_schema` | `needs_fix_metadata_contract` |
| `unsupported_contract` | `needs_fix_metadata_contract` |
| `failed` | `blocked_safety` |
| `manual_review_required` | `manual_review_required` |
| unknown future source or platform status | manual review or bounded block; never ready |

Warnings and manual outcomes are never upgraded to ready.

## Package-reference contract

- `package_id` must be one plain safe directory name.
- `package_role` and `package_index_ref` must be explicit safe values.
- `package_root_ref` must explicitly identify `configured_export_root`.
- `package_relative_path` must be one safe relative component exactly matching `package_id`.
- The adapter emits `package_name_under_configured_export_root`; no absolute path or legacy path is emitted.
- Missing, escaping, mismatched, or ambiguous location data stops as manual review or path block before the package resolver.
- The existing resolver independently enforces export-root containment and fixed metadata filenames.

## Response contract

- Schema: `internal_operator_review_only_staging_local_exchange_response_v0_1`
- Safe fields include route/access scope, metadata/review-only flags, bounded status fields, the safe basename, reader/adapter/provider/package statuses, candidate count, one safe staging summary, one safe gate summary, blockers, warnings, and explicit false-valued product-boundary flags.
- The response excludes absolute paths, configured directory values, environment values, raw provider payloads, package-relative source paths, file bytes, evidence rows, raw comments, author identifiers, authentication data, secrets, collector internals, and public output.

## TDD RED and focused validation

The focused B01 test module was created before the bridge or route implementation. Its first run produced the required genuine RED during collection:

- `ModuleNotFoundError: No module named 'app.services.local_exchange_review_only_staging_bridge'`
- result: 1 collection error; no product, provider, package, row, or runtime access occurred.

After implementation:

- isolated B01 focused suite: 48 passed.
- B01 plus the two modified route smoke suites: 84 passed.
- approved focused-first regression matrix: 223 passed.
- matrix coverage: B01 bridge, local-exchange reader, private provider-result reader, package resolver, local-exchange smoke, review-only staging, provider-to-staging handoff, disabled/enabled route smokes, route behavior, environment-gate helper, and narrow UI/route safety contract.

The focused B01 suite covers at least the required 22 behaviors: primary and secondary gates, missing configuration, strict basenames, containment, not-found, JSON/schema errors, unsupported contracts, future platforms, deterministic mapping, ready package resolution, manual snapshot, missing provenance, path ambiguity/escape, provider privacy, package privacy, row-file exclusion, nonpersistence, safe response shape, unchanged synthetic routes, GET-only registration, default-off behavior, side-effect flags, reader call counts, status non-upgrade, and static forbidden behavior.

## Synthetic execution ledger

- B01 suite RED run: synthetic provider-result reads 0; package metadata reads 0.
- Each green B01 suite run: 25 synthetic temporary provider-result file reads under pytest `tmp_path`.
- Each green B01 suite run: 40 synthetic temporary safe package metadata reads, derived from 8 explicit package resolutions times 5 existing readable safe metadata files.
- Two green B01 suite executions completed: 50 B01 synthetic provider-result reads and 80 B01 synthetic safe package metadata reads in aggregate.
- The wider focused regression matrix also used only its existing synthetic `tmp_path` fixtures; it performed no real provider or package access.
- Evidence row or package row files parsed: 0. Guarded sentinels prove they were not opened by the bridge/resolver path.

## Changed files

1. `backend/app/services/local_exchange_review_only_staging_bridge.py`
2. `backend/app/api/v1/routes/internal_operator_review_only_staging.py`
3. `backend/app/tests/test_mvp_b01_local_exchange_review_only_staging_runtime_bridge.py`
4. `backend/app/tests/test_internal_operator_review_only_staging_disabled_smoke.py`
5. `backend/app/tests/test_internal_operator_review_only_staging_enabled_fixture_smoke.py`
6. `docs/health/sentigraph_mvp_b01_local_exchange_review_only_staging_runtime_bridge_report_v1_0.md`

No reader, schema, provider reader, package resolver, local-exchange smoke helper, staging helper, API registration, frontend, runtime, configuration file, README, or unrelated test was modified.

## Compile, static, and diff validation

- Changed-Python `py_compile`: PASS for all five changed Python files.
- Static bridge boundary scan: PASS; no discovery, network client, subprocess, database, file-response, writer, or direct file-open pattern exists in the bridge.
- Route contract scan: PASS; the exact GET decorator, both gates, and all three server-owned configuration names are present, with no state-changing route decorator.
- Changed-file allowlist: PASS; exactly the six approved files are changed.
- Documentation required-evidence scan: PASS.
- Trailing-whitespace scan across all six changed files: PASS.
- Unstaged tracked `git diff --check`: PASS.
- Cached diff validation: required immediately after exact-file staging and before ready-only commit.

## Not run

- no real local-exchange provider-result smoke
- no configured results-directory or export-root inspection
- no real provider or package path access
- no directory discovery
- no evidence/source/package row parsing
- no writer, SQLite, or persistent staging operation
- no full backend test suite
- no frontend test or build
- no browser or UI runtime
- no provider or collector job
- no network, scraping, real API, or LLM call
- no product import, production case, analysis run, report, public event, export, or delivery

## Git finalization plan

- Ready-only commit message: `Connect local exchange to review-only staging`
- Push target: current `main` to `origin/main`
- Required final evidence: exact cached six-file allowlist, successful commit/push, ahead/behind `0/0`, and clean tracked/nonignored worktree.
- Tag: no.
- Release: no.
- Project Source changed: no.

## Source recommendation after independent ChatGPT acceptance

- Canonical 00: replace.
- Canonical 03: replace.
- Canonical 09: replace.
- Canonical 08: no change.

The next boundary is an independent ChatGPT review of the B01 completion receipt. No real metadata smoke and no B02 work are authorized by this Goal.
