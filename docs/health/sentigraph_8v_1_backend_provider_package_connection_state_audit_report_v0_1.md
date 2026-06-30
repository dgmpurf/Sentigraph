# Sentigraph 8V-1 Backend Provider / Collector Package Connection State Audit Report v0.1

## A. Decision / Status

phase = 8V-1

task = backend_provider_package_connection_state_audit

decision = ready

privacy_issue_stop = no

audit_only = yes

report_only = yes

backend_code_changed = no

frontend_code_changed = no

route_changed = no

api_route_added = no

tests_changed = no

runtime_changed = no

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

source_files_created = no

docs_project_sources_created = no

Summary:

- Sentigraph has an implemented metadata-first backend connection spine for provider / collector package handoff.
- The private collector remains an external provider / package producer, not a built-in Sentigraph crawler.
- The strongest implemented path today is metadata-only: provider result metadata -> safe package resolver -> safe handoff summary -> review-only staging candidate.
- The Analysis Request governance chain is runtime-capable for local JSON governance records, bounded previews, review gates, dedup/promotion/manual-analysis/report/export/public-access gates, but remains deliberately staged and gate-oriented.
- Minimum real-run and dense graph backend pieces are implemented against controlled fixtures/samples; dense graph route is internal/local-only, disabled by default, and sample-allowlist only.
- The biggest backend gap is not another model/weight change; it is a single controlled metadata smoke that proves the provider package reference can move into a review-only staging candidate from an exported package-style fixture without row import or production side effects.

## B. Git / Repo State

Initial repo state before this report:

- branch: `main`
- HEAD: `20581adb75929e3f2c38a3a3e439dc1b9c2d81fa`
- latest commit: `20581ad Add Dong/Sun historical replay browser regression smoke report`
- working tree before this report: clean

Latest 10 commits:

- `20581ad Add Dong/Sun historical replay browser regression smoke report`
- `c654fff Add 8U-7 dense graph frontend integration decision`
- `561d843 Add 8U-6 dense graph route validation report`
- `dcda98e Implement 8U-5 dense graph internal route`
- `b998212 Add 8U-4 dense graph route contract`
- `a94517f Implement 8U-3 dense graph generated-run integration`
- `a73d17d Implement 8U-2 dense graph generated-run attachment`
- `c7b689a Implement 8U-1 dense opinion graph builder`
- `19fdc91 Add 8S-16-NR no-recording path decision`
- `5713b22 Add 8S-15 internal recording capture package`

## C. Component Inventory

| Component | Status | Main files | Tests | Runtime type | Disabled by default | Reads metadata | Parses evidence rows | Writes production Evidence | Creates production case / analysis_run | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| External Collector Bridge | implemented runtime | `backend/app/schemas/external_collector_bridge.py`; `backend/app/services/external_collector_bridge.py`; `backend/app/api/v1/routes/external_collector.py` | `backend/app/tests/test_external_collector_bridge.py` | local bridge route over configured export directory | effectively no-op when not configured | yes | validation route can read local package evidence rows for safety validation | no | no | Does not run collector. Lists/details packages and validates local export package structure. |
| Local Exchange Reader | disabled-by-default runtime/helper | `backend/app/schemas/local_exchange.py`; `backend/app/services/local_exchange_reader.py` | `backend/app/tests/test_local_exchange_reader.py` | metadata reader | yes, `exchange_enabled` defaults false | yes | no | no | no | Reads provider result JSON metadata only when explicitly enabled in config. |
| Private Collector Package Resolver | implemented helper / tests-covered | `backend/app/services/private_collector_package_resolver.py` | `backend/app/tests/test_private_collector_package_resolver.py` | metadata-only helper | caller-controlled | yes | no | no | no | Resolves package name/path safely under configured export root; checks row-file presence only. |
| Private Collector Provider Result Reader | implemented helper / tests-covered | `backend/app/services/private_collector_provider_result_reader.py` | `backend/app/tests/test_private_collector_provider_result_reader.py` | metadata-only helper | caller-controlled | yes | no | no | no | Validates provider result contract, package reference, safety markers, and resolver outcome. |
| Review-only Staging Helper | implemented helper / tests-covered | `backend/app/services/private_collector_review_only_staging.py` | `backend/app/tests/test_private_collector_review_only_staging.py`; `backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py` | metadata-only review staging candidate helper | caller-controlled | yes | no | no | no | Produces review-only candidate/summary and blocks production side-effect flags. |
| Internal Operator Review-only Staging Route | disabled-by-default runtime route | `backend/app/api/v1/routes/internal_operator_review_only_staging.py` | `backend/app/tests/test_internal_operator_review_only_staging_routes.py`; disabled/enabled fixture smoke tests | internal/local route skeleton | yes, env-gated | synthetic metadata only | no | no | no | Route is safe disabled by default; enabled fixture mode is synthetic, not real package access. |
| Analysis Request Governance Store / Routes | implemented runtime | `backend/app/schemas/analysis_request.py`; `backend/app/services/analysis_request_store.py`; `backend/app/api/v1/routes/analysis_requests.py` | `backend/app/tests/test_analysis_request_store.py`; `test_analysis_request_routes.py`; `test_analysis_request_golden_contracts.py` | local ignored JSON governance runtime | no, but guarded by explicit gates | yes | yes, only in approved bounded preview helpers | no | no production case / no production analysis_run | Implements governance spine from request to import/review/dedup/promotion/manual-analysis/report/export/public-access gates. |
| Evidence Import / Review / Dedup / Promotion Gates | implemented runtime inside Analysis Request store | `analysis_request.py`; `analysis_request_store.py`; `analysis_requests.py` | covered by route/store/golden tests | local governance records | no | yes | row-reader dry-run and real-package row preview are bounded/safe preview only | no | no | Preview/review gates do not write Evidence Layer or production cases. |
| Minimum Real-run Service | implemented runtime helper | `backend/app/services/opinion_ecosystem_minimum_real_run.py` | `backend/app/tests/test_opinion_ecosystem_minimum_real_run.py` | backend-only pure local generated-run wrapper | caller-controlled | fixture metadata | no external/package row parsing | no | no | Wraps existing calculator output into `sentigraph_opinion_ecosystem_run_v0_1` with boundary and side-effect flags. |
| Dense Graph Builder | implemented runtime helper | `backend/app/services/opinion_ecosystem_dense_graph_builder.py` | `backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py` | backend-only controlled sample graph builder | caller-controlled | safe evidence item dicts | can load controlled repo sample evidence items by allowlisted path | no | no | Builds dense proxy graph, not production score or public action. |
| Dense Graph Generated-run Adapter / Integration | implemented runtime helper | `backend/app/services/opinion_ecosystem_dense_graph_generated_run_adapter.py`; `backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py` | `test_opinion_ecosystem_dense_graph_generated_run_adapter.py`; `test_opinion_ecosystem_dense_graph_generated_run_integration.py` | backend-only attachment/integration helper | caller-controlled | generated run + graph metadata | no arbitrary package rows | no | no | Attaches graph payload to generated run; frontend-ready/production-ready remain false. |
| Dense Graph Internal Route | disabled-by-default runtime route | `backend/app/api/v1/routes/opinion_ecosystem_dense_graph.py` | `backend/app/tests/test_opinion_ecosystem_dense_graph_route.py` | internal/local GET route | yes, env-gated | yes | only allowlisted controlled repo sample files when enabled | no | no | Disabled default; sample allowlist; no arbitrary paths/private collector paths/URLs. |
| External Evidence Package Validator | implemented CLI validator | `scripts/validate_external_evidence_package.py` | `backend/app/tests/test_external_evidence_package_validator.py` | local package validation script | manual command only | yes | yes, for local validation | no | no | Validates package structure and safety; not a collector. |
| Frontend Fixture Generator | implemented utility | `scripts/generate_opinion_ecosystem_frontend_fixture.py` | `backend/app/tests/test_opinion_ecosystem_frontend_fixture_generator.py` | local generator utility | manual command only | reads local sample package | yes, for fixture generation only | no | no | Not part of production backend chain. |
| Docs Samples: Helldivers | fixture package | `docs/samples/helldivers2_psn_demo/` | validator/generator tests cover expected shape | fixture-only | n/a | package metadata available | row files present | no | no | Selected public sample package for demo/prototype validation. |
| Docs Samples: Dong/Sun | fixture package | `docs/samples/donglu_sunjihai_youth_football/` | dense graph route allowlist and frontend fixtures use controlled sample | fixture-only | n/a | package metadata available | row files present | no | no | Selected public sample package for Dong/Sun demo/prototype validation. |

## D. Backend Connection Chain Map

| Edge | Implemented | Runtime | Disabled by default | Metadata only | Parses evidence rows | Writes Evidence Layer | Creates production case / analysis_run | Tests | Main files |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| provider result metadata -> package reference / package name | yes | helper/runtime depending caller | caller-controlled | yes | no | no | no | yes | `private_collector_provider_result_reader.py`; `local_exchange_reader.py` |
| package reference -> package resolver | yes | helper | caller-controlled | yes | no, file presence only | no | no | yes | `private_collector_package_resolver.py` |
| package resolver -> safe handoff summary | yes | helper | caller-controlled | yes | no | no | no | yes | `private_collector_provider_result_reader.py` |
| safe handoff summary -> review-only staging candidate | yes | helper | caller-controlled | yes | no | no | no | yes | `private_collector_review_only_staging.py` |
| review-only staging candidate -> internal operator route skeleton | partial | route skeleton | yes | synthetic fixture only | no | no | no | yes | `internal_operator_review_only_staging.py` |
| review-only staging -> review queue / dedup / promotion gates | yes in Analysis Request governance | local JSON runtime | no | mostly metadata/governance records | bounded preview helpers only | no | no | yes | `analysis_request_store.py`; `analysis_requests.py` |
| promotion/manual trigger -> manual analysis/result/report gates | yes in Analysis Request governance | local JSON runtime | no | governance/result candidate records | no package row parsing for report gates | no | no production analysis_run | yes | `analysis_request_store.py`; `analysis_requests.py` |
| minimum real-run generated output | yes | backend helper | caller-controlled | fixture metadata | no | no | no | yes | `opinion_ecosystem_minimum_real_run.py` |
| generated run -> dense graph attachment | yes | backend helper | caller-controlled | generated run + safe graph metadata | no arbitrary package rows | no | no | yes | dense graph adapter/integration services |
| dense graph internal route | yes | internal GET route | yes | safe route response metadata | only allowlisted controlled repo samples when enabled | no | no | yes | `opinion_ecosystem_dense_graph.py` |

## E. Controlled Fixture Capability

What can run today with controlled fixtures / repo samples:

- Synthetic provider result fixture through local exchange reader tests.
- Metadata-only provider result -> package resolver -> handoff summary helpers.
- Temp package metadata fixture with required filenames present.
- Review-only staging helper integration smoke from synthetic provider result fixture to staging candidate.
- Local exchange reader disabled mode and explicitly enabled fixture mode.
- Analysis Request governance chain tests for contracts and local JSON records.
- Minimum real-run wrapper over in-memory safe fixture/calculator output.
- Dense graph builder over safe evidence item dicts.
- Dense graph generated-run attachment and integration helpers.
- Dense graph internal route when explicitly enabled and sample ID is allowlisted.

What this does not mean:

- It does not mean real collector jobs run inside Sentigraph.
- It does not mean arbitrary package paths or private collector paths are allowed.
- It does not mean Evidence Layer import or production case creation is approved.
- It does not mean frontend dense graph integration is approved.

## F. Already-exported Package Capability

For an already-exported Evidence Export v1-style package, current Sentigraph-side capability is layered:

Metadata-only inspection:

- External Collector Bridge can list package status/details when an export directory is configured.
- Package resolver can resolve a package reference under an explicitly configured export root and check required file presence.
- Provider result reader can validate provider result metadata and produce a safe handoff summary.
- Local exchange reader can read provider result metadata when explicitly enabled.

Manifest / validation / source summary:

- External Collector Bridge can return safe manifest and validation summaries.
- Package resolver can read safe metadata files such as manifest, validation report, coverage note, README, and package index.
- The audit did not inspect any private collector directory or external package export root.

Evidence item presence check:

- Package resolver and bridge can check whether `evidence_items.jsonl` / `evidence_items.csv` exist.
- Metadata-only helpers do not parse those files.

Limited redacted row preview:

- Analysis Request store includes bounded row-reader dry-run and real-package row-preview helpers.
- These are preview/gate mechanisms, not production import.

Full evidence row parsing:

- External package validator and some preview/generator utilities can parse local package rows for validation or fixture generation.
- This is not automatic production ingestion.

Production Evidence import:

- Still blocked/not approved in this provider package chain.
- No Evidence Layer write, production case creation, or production `analysis_run` creation is performed by the current provider/package handoff path.

## G. Gap Analysis

P0 privacy/security:

- None found in this audit.

P1 backend connection blockers:

- None in the tested metadata/helper surfaces.
- The remaining backend gap is sequencing, not a broken existing test.

P2 sequencing/stabilization gaps:

- No single current smoke stitches a controlled exported package-style provider result through resolver -> handoff summary -> review-only staging candidate -> readiness for minimum real-run/dense graph.
- Internal operator route is disabled by default and synthetic fixture only; it is not yet a true controlled metadata package operator surface.
- Dense graph internal route can load allowlisted repo samples, but the provider/package chain is not yet connected to generated-run/dense graph as a single audited backend path.
- Limited real row preview exists, but should remain behind explicit gates and should not become the next automatic step unless metadata smoke is stable.

P3 cleanup/docs:

- Analysis Request store is broad and already documented as needing modularization over time.
- Report/source maintenance can remain batched; no immediate Project Source update is needed for this audit-only phase.

## H. Next-slice Options

| Option | Business value | Technical value | Risk | Size | Safety boundary | Moves closer to "backend really runs" | Recommended mode |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A. Metadata-only provider result -> package resolver smoke against controlled exported package metadata | high | high | low | small | metadata only, no row parsing | yes | backend-only tests/runtime smoke |
| B. Local exchange reader controlled real exported package metadata smoke | high | high | medium-low | small/medium | must avoid private collector access unless explicitly configured; metadata only | yes | backend-only smoke after A or combined narrowly |
| C. Review-only staging candidate from real package metadata | high | high | medium | medium | review-only, no production import | yes | backend-only after A/B |
| D. Limited redacted row preview gate | medium | high | medium/high | medium | bounded preview, redaction, no production import | yes, but riskier | wait until metadata chain smoke passes |
| E. Staging -> minimum real-run / generated-run bridge | high | high | medium | medium | generated run remains selected-sample only and human-review-required | yes | after metadata/staging smoke |
| F. Generated-run -> dense graph / calculator bridge with controlled package | high | high | medium | medium | allowlist + no frontend/public route | yes | after E |
| G. Operator route / internal review UI | medium | medium | medium/high | larger | disabled/local/internal only | indirectly | wait; not mainline now |

## I. Recommended Next Step

Primary recommendation:

Phase 8V-2 Controlled Exported Package Metadata Smoke / Readiness Check.

Suggested scope:

- backend-only / test-first
- use controlled fixture or repo sample metadata, not private collector source code
- no collector run
- no real APIs / LLMs
- no URL fetch/scrape
- no Evidence Layer write
- no production case / production `analysis_run`
- no frontend changes
- no full evidence row parsing
- prove package metadata can move through:
  - provider result metadata
  - safe resolver
  - safe handoff summary
  - review-only staging candidate

Alternative if the team wants one more gate before implementation:

Phase 8V-2 Backend Provider Package Connection Next-Slice Decision Docs-only.

Do not choose frontend polish, dense graph frontend integration, or algorithm/weight recalibration as the mainline next task until the backend package connection can run as a controlled metadata chain.

## J. Safety Confirmations

- no collector run
- no real API called
- no real LLM called
- no URL fetching/scraping
- no private collector source inspected
- no private collector job run
- no browser/cookie/session/profile inspected
- no secrets or `.env` values read or printed
- no raw author/profile values printed
- no Evidence Layer write
- no production case created
- no production `analysis_run` created
- no route changed
- no API route added
- no frontend code changed
- no backend code changed
- no tests changed
- no runtime changed
- no Project Source files created
- no `docs/project_sources/` created
- no GitHub Actions workflow recreated

## K. Validation Commands and Results

Git / repo commands:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git log --oneline -10
```

Result:

- initial working tree clean
- branch `main`
- HEAD `20581adb75929e3f2c38a3a3e439dc1b9c2d81fa`

Targeted tests:

```text
python -m pytest backend/app/tests/test_external_collector_bridge.py
```

Result: passed, `6 passed`.

```text
python -m pytest backend/app/tests/test_local_exchange_reader.py
```

Result: passed, `9 passed`.

```text
python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
```

Result: passed, `7 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_minimum_real_run.py
```

Result: passed, `8 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
```

Result: passed, `10 passed`.

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_route.py
```

Result: passed, `13 passed`.

Py compile:

```text
python -m py_compile backend/app/services/external_collector_bridge.py backend/app/services/local_exchange_reader.py backend/app/services/analysis_request_store.py backend/app/services/opinion_ecosystem_minimum_real_run.py backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py
```

Result: passed.

Final checks:

```text
git diff --check
git status --short
```

To be run after report creation.

## L. Not Run and Why

- Full backend pytest: not run because task requested targeted tests only and no code changed.
- Frontend build: not run because this is backend audit/report-only and no frontend files changed.
- Browser smoke: not run because this task is backend connection audit/report-only.
- Collector: not run by boundary.
- Real API / real LLM / network: not run by boundary.
- Private collector project inspection: not run by boundary.
- Evidence row parsing: not run by this audit. The sample directory was listed by filenames/sizes only.

## M. Source Maintenance Note

source_update_recommended = no immediate

Reason:

This is an audit-only report. Do not create Source files in repo. If future backend implementation changes behavior, ChatGPT/user can manually update Project Source later.

