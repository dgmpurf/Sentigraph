# Sentigraph 8V-2 Controlled Exported Package Metadata Smoke Report v0.1

## A. Decision / Status

phase = 8V-2

task = controlled_exported_package_metadata_smoke

decision = ready

privacy_issue_stop = no

backend_test_added = yes

backend_production_code_changed = no

frontend_code_changed = no

api_route_added = no

runtime_behavior_changed = no

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

evidence_rows_parsed = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

Summary:

- Added a focused backend test proving a controlled exported package-style metadata fixture can move through provider result metadata, safe package resolver, local exchange metadata smoke, and review-only staging candidate creation.
- The fixture includes deliberately invalid `evidence_items.jsonl` and `evidence_items.csv` files with sentinel values. The test guards against reading those row files.
- The smoke remains metadata-only and review-only. It does not import evidence, create production cases, start analysis, generate reports, generate public events, or expose package paths.

## B. Changed Files

Backend tests:

- `backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py`

Docs / health:

- `docs/health/sentigraph_8v_2_controlled_exported_package_metadata_smoke_report_v0_1.md`

Production backend code:

- none

Frontend code:

- none

Runtime files:

- none

Project Source files:

- none

## C. Controlled Temp Fixture

The test builds a temporary exported package-style fixture under pytest `tmp_path`.

Safe metadata files created in the temporary package:

- `manifest.json`
- `validation_report.json`
- `validation_report.md`
- `coverage_note.md`
- `README.md`
- `source_manifest.jsonl`
- `collection_log.jsonl`

Presence-only row files created in the temporary package:

- `evidence_items.jsonl`
- `evidence_items.csv`

Those row files are intentionally invalid and include sentinel strings. The test monkeypatches `Path.read_text` so any attempt to read either row file raises immediately. This proves the 8V-2 chain checks row-file presence only and does not parse evidence rows.

## D. Smoke Chain Result

Validated chain:

1. controlled provider result JSON metadata
2. `read_provider_result_metadata`
3. safe package resolution under configured temporary export root
4. `run_private_collector_local_exchange_metadata_smoke`
5. `create_review_only_staging_candidate`
6. `build_review_only_staging_gate_result`
7. `build_safe_review_only_staging_summary`

Expected ready path:

- provider reader status: `accepted_metadata_only`
- resolver status: `accepted_metadata_only`
- smoke status: `ready_for_metadata_only_handoff`
- review-only staging status: `ready_for_human_review`
- promotion status: `promotion_required`
- evidence row boundary: `evidence_rows_not_read`

Blocked-path checks:

- invalid package-name traversal shape produces `needs_fix_metadata_contract` at reader/smoke level.
- explicit relative path escape produces `blocked_path_escape` and stays blocked at staging level.

Forbidden metadata check:

- an actual top-level `token` field in provider result metadata is blocked as `blocked_privacy_issue`.
- the actual token value is not emitted in safe summaries.

## E. Safety Assertions

The new test asserts:

- no row files are parsed
- metadata-only flags remain true
- full evidence row read flags remain false
- Evidence Layer write flags remain false
- production case creation flags remain false
- analysis run creation flags remain false
- review-only staging remains human-review oriented
- production actions stay blocked
- actual secret-like sentinel values are not emitted
- actual raw-author sentinel values are not emitted
- actual private-message/profile/cookie/session/path sentinels are not emitted
- pytest temp absolute paths are not emitted
- no staging/runtime/evidence-layer/production-case/analysis-run files are written

Allowed safety marker names such as `raw_author_identifiers_printed=false` may appear because they are negative boundary flags, not raw identifier exposure.

## F. Existing Helpers Reused

The smoke reused existing helper surfaces:

- `backend/app/services/private_collector_package_resolver.py`
- `backend/app/services/private_collector_provider_result_reader.py`
- `backend/app/services/private_collector_local_exchange_smoke.py`
- `backend/app/services/private_collector_review_only_staging.py`

No production helper behavior was changed.

## G. Validation Results

Repository context:

```text
git branch --show-current
```

Result: `main`

```text
git rev-parse HEAD
```

Result: `9332cf5cea49f7cd9f1511e2b5be820e978fe235`

New focused test:

```text
python -m pytest backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py -q
```

Result: passed, `4 passed`.

Existing targeted tests:

```text
python -m pytest backend/app/tests/test_private_collector_package_resolver.py backend/app/tests/test_private_collector_provider_result_reader.py backend/app/tests/test_private_collector_review_only_staging.py backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Result: passed, `98 passed`.

Py compile:

```text
python -m py_compile backend/app/services/private_collector_package_resolver.py backend/app/services/private_collector_provider_result_reader.py backend/app/services/private_collector_review_only_staging.py backend/app/services/local_exchange_reader.py
```

Result: passed.

Final checks:

```text
git diff --check
git status --short
```

Result:

- `git diff --check`: passed.
- `git status --short`: two untracked files only:
  - `backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py`
  - `docs/health/sentigraph_8v_2_controlled_exported_package_metadata_smoke_report_v0_1.md`

Static safety scan:

```text
rg -n "fetch\(|axios|http://|https://|API key|token|cookie|author_name|author_id|profile_url|G:/|C:/|evidence_items|private collector" backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py docs/health/sentigraph_8v_2_controlled_exported_package_metadata_smoke_report_v0_1.md
```

Result:

- Expected matches only: sentinel values, forbidden-field tests, presence-only `evidence_items` filenames, and written boundary language.
- No `fetch(`, `axios`, `http://`, or `https://` matches.
- No runtime network implementation found.
- No real secret value found.

## H. Not Run and Why

- Full backend pytest: not run because this was a focused backend metadata-smoke task.
- Frontend build: not run because no frontend code changed.
- Browser smoke: not run because no UI or route behavior changed.
- Collector job: not run by boundary.
- Private collector project inspection: not run by boundary.
- Real exchange directory read: not run by boundary.
- Real APIs / real LLMs / network: not run by boundary.
- Evidence row parsing: intentionally blocked by test guard.

## I. Issues / Follow-ups

P0 privacy/security:

- none found.

P1 functional blockers:

- none found.

P2 next bridge:

- The next missing piece is not another metadata smoke. It is a design checkpoint for how a safe review-only staging candidate can be bridged into a minimum real-run / generated-run request without importing evidence rows, writing Evidence Layer, creating production cases, or generating public artifacts.

P3 optional cleanup:

- The existing review-only staging helper treats `needs_fix_metadata_contract` as a reader/smoke-level status rather than a staging blocker. This is acceptable for 8V-2 because explicit path escape is blocked; a future helper cleanup may normalize this status if the operator flow needs it.

## J. Recommended Next Step

Recommended next task:

Phase 8V-3 Staging Candidate to Minimum Real-run / Generated-run Bridge Decision Docs-only.

Suggested scope:

- docs-only first
- define input from safe review-only staging summary
- keep `metadata_only=true`
- no evidence row parsing
- no Evidence Layer write
- no production case
- no production analysis run
- no frontend/API route
- no collector/private project access
- no real APIs/LLMs

## K. Safety Confirmations

- no production backend code changed
- no frontend code changed
- no API route added
- no runtime behavior changed
- no collector run
- no private collector project touched
- no real exchange directory read
- no provider/collector jobs run
- no real APIs called
- no real LLM called
- no URL fetching/scraping
- no MediaCrawler integration
- no OpenClaw production integration
- no browser automation
- no login/profile/cookie/session access
- no `.env`, token, API key, cookie, session, or salt read or printed
- no raw author identifiers exposed
- no original package rows read
- no `evidence_items.jsonl` / `evidence_items.csv` parsed
- no Evidence Layer write
- no production case created
- no production review queue created
- no production dedup
- no production analysis run created
- no B-end report generated
- no Sandbox/public event generated
- no Project Source files changed
- no GitHub Actions workflow recreated
