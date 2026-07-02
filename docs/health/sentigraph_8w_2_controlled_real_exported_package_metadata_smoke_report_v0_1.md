# Sentigraph 8W-2 Controlled Real Exported Package Metadata Smoke Report v0.1

## A. Decision / Status

decision = ready

privacy_issue_stop = no

backend_only = yes

test_first = yes

metadata_only = yes

approved_target_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016

approved_target_package_role = candidate_demo_sample

approved_target_case_id_hint = donglu_sunjihai_youth_football_202606

backend_code_changed = yes

frontend_code_changed = no

tests_changed = yes

route_changed = no

api_route_added = no

runtime_changed = local_backend_object_only

selector_implemented = no

package_metadata_smoke_executed = yes

created_local_metadata_smoke = yes

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

private_collector_inspected = no

private_collector_source_inspected = no

real_exchange_dir_read = no

evidence_items_jsonl_parsed = no

evidence_items_csv_parsed = no

original_package_rows_read = no

raw_comments_read = no

raw_identities_read = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

final_delivery_runtime_used = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

absolute_path_exposed = no

package_path_exposed = no

source_files_created = no

docs_project_sources_created = no

Final smoke status:

`metadata_warn_manual_review_required`

The approved package metadata target was found under the repo-controlled sample path and produced a local backend metadata-only smoke object. The object is warn/manual-review because the validation report carries one warning. This is acceptable for 8W-2 because the phase is metadata-only and explicitly requires human review.

## B. Approved Package Metadata Target

Approved target:

- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`
- provider_result_id: `unknown`
- provider_job_id: `unknown`
- request_id: `unknown`

The helper accepts only this explicit target identity. It does not implement a selector, scan directories, inspect private collector source, use env-provided export roots, or broaden to nearby packages.

The repo-relative package location is used only as an internal lookup for this exact approved target. The output does not emit absolute paths or package paths.

## C. Changed Files

- `backend/app/services/real_exported_package_metadata_smoke.py`
- `backend/app/tests/test_real_exported_package_metadata_smoke.py`
- `docs/health/sentigraph_8w_2_controlled_real_exported_package_metadata_smoke_report_v0_1.md`

No frontend, route, API registration, runtime persistence, package, private collector, Project Source, or `docs/project_sources/` files were changed.

## D. Metadata-only Helper Summary

The new helper builds a local safe object with schema:

`sentigraph_real_exported_package_metadata_smoke_v0_1`

The helper:

- requires the explicit 8W-2 approval flag in the caller
- requires exact approved package name, role, and case id hint
- accepts only the explicit package directory supplied for this approved target
- reads `manifest.json`, `validation_report.json`, and `coverage_note.md` for safe metadata summaries only
- checks presence only for row/log files
- blocks requested side effects
- blocks forbidden metadata fields such as tokens, cookies, API keys, raw author ids, author names, profile URLs, raw comments, private messages, and actual path fields
- returns only safe reason codes in blockers
- keeps all runtime side effects false

The helper does not persist runtime files.

## E. Safe Metadata Fields Inspected

Safe metadata used or summarized:

- target package name, role, and case id hint from explicit user-approved identity
- validation status
- warning count
- error count
- evidence count summary when available in safe metadata
- source count summary when available in safe metadata
- coverage note summary
- metadata file presence flags
- privacy status
- path status
- safe warning / blocker reason codes

Observed safe summary for the approved target:

- validation_status: `passed`
- warning_count: `1`
- error_count: `0`
- evidence_count_summary: `unknown`
- source_count_summary: `unknown`
- privacy_status: `metadata_only_no_known_privacy_blocker`
- path_status: `repo_controlled_target_path_ok`

Unknown count summaries mean those counts were not present in the safe fields used by this helper. The helper did not parse row files to derive them.

## F. Row-read Prevention Proof

Focused tests monkeypatch `Path.read_text` to fail if the helper attempts to read:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The ready/warn path still passes with that guard in place. This proves those files remain presence-only for this phase.

Runtime flags remain false:

- `parsed_evidence_items_jsonl`
- `parsed_evidence_items_csv`
- `read_original_package_rows`
- `read_raw_comments`
- `read_raw_identities`

## G. Private Collector Separation Proof

The helper does not import private collector code, does not read the private collector project, does not use env-provided export roots, and does not access real exchange directories.

The approved repo-relative sample path is used only for this exact target. Tests assert the safe output does not contain private collector path sentinels or absolute path markers.

Runtime flags remain false:

- `ran_provider_job`
- `ran_collector`
- `accessed_private_collector`
- `inspected_private_collector_source`
- `read_real_exchange_dir`

## H. Blocked Path Behavior

Focused tests cover these blocked paths:

- wrong package name
- missing target metadata
- path traversal in package name
- wrong package role
- missing approved target path
- forbidden metadata fields
- side-effect requests

Blocked outputs keep `created_local_metadata_smoke = false`, do not echo forbidden sentinel values, do not expose paths, and keep all runtime side effects false.

## I. Output Boundary Object

The output object includes:

- schema: `sentigraph_real_exported_package_metadata_smoke_v0_1`
- phase: `8W-2`
- smoke status
- approved target identity
- target identity method: `explicit_user_approved_package_metadata_target`
- target source kind: `repo_controlled_already_exported_package_metadata`
- metadata-only flags
- row-read false flags
- private collector false flags
- file presence flags
- safe summary
- boundary flags
- runtime side effects
- safe warnings and blockers

Boundary flags include:

- selected sample only
- not full-web
- not full-platform
- not full-thread
- not official verification
- not causal proof
- not prediction
- not production score
- provider output is evidence candidate, not truth
- human review required
- metadata only
- no row read
- no private collector source inspection
- no Evidence Layer write
- no production case
- no production analysis run
- no frontend route
- no real API / LLM / provider / collector

## J. Relationship to 8W-1 and Source 24

8W-2 implements the controlled metadata-only smoke option selected by 8W-1, using the explicit user approval phrase:

`批准 8W-2 Controlled Real Exported Package Metadata Smoke implementation`

8W-2 does not broaden 8W-1. It remains metadata-only, one-target, backend-only, no-row-read, no selector, and no private collector source inspection.

After commit, a ChatGPT-side Source 24 or equivalent project-context patch can summarize this new controlled metadata smoke. Do not create Project Source files inside the repo.

## K. Relationship to Source 11 / Evidence Layer

8W-2 does not update Source 11 behavior and does not write Evidence Layer.

It does not create:

- production case
- production `analysis_run`
- production review queue
- production dedup
- B-end report runtime
- Sandbox runtime
- public event runtime
- report/export/download/public/final-delivery runtime

The metadata smoke output is a checkpoint only. It is not import approval, analysis approval, report approval, public output, customer output, official verification, full-web coverage, full-platform coverage, causal proof, prediction, or production score.

## L. Validation Commands and Results

Preflight:

- `git status --short`: clean before implementation.
- `git branch --show-current`: `main`.
- `git rev-parse HEAD`: `4cca62b28256945ea631132b04d0b64b1f28cb6e`.
- latest commit message: `Add 8W-1 real package metadata selection decision`.

TDD red:

- `python -m pytest backend/app/tests/test_real_exported_package_metadata_smoke.py -q`
- failed as expected with `ModuleNotFoundError: No module named 'app.services.real_exported_package_metadata_smoke'`.

Focused:

- `python -m pytest backend/app/tests/test_real_exported_package_metadata_smoke.py -q`
- passed, 6 tests.

Nearby:

- `python -m pytest backend/app/tests/test_real_exported_package_metadata_smoke.py backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_private_collector_controlled_exported_package_metadata_smoke.py backend/app/tests/test_external_collector_bridge.py backend/app/tests/test_analysis_request_golden_contracts.py -q`
- passed, 32 tests.

Compile:

- `python -m py_compile backend/app/services/real_exported_package_metadata_smoke.py backend/app/services/local_exchange_reader.py`
- passed.

Diff:

- `git diff --check`
- passed before this report was added.

## M. Not Run and Why

Not run:

- full pytest
- frontend build
- browser smoke
- collector
- real APIs
- real LLMs
- URL fetch
- scrape
- private collector source inspection
- real exchange directory read
- evidence row parsing
- row preview
- Evidence Layer write
- production case / production `analysis_run`
- report/export/download/public/final-delivery runtime smoke
- route/frontend smoke

Reason:

8W-2 is a backend-only controlled metadata smoke. The task explicitly forbids those actions and asks not to run them.

## N. Issues P0/P1/P2/P3

- P0: none.
- P1: none.
- P2: future phase must decide whether the metadata-smoke output can proceed to review-only staging or remain as a metadata-only checkpoint; do not jump to row preview or import.
- P3: consider ChatGPT-side Source 24 patch after commit.

## O. Recommended Next Step

Recommended next task:

Phase 8W-3 Real Package Metadata Smoke Completion / Review-only Staging Decision Docs-only.

Do not proceed directly to row preview, Evidence Layer import, production case, production `analysis_run`, frontend/route, B-end report runtime, Sandbox/public event runtime, public/download/final-delivery runtime, real API, real LLM, provider execution, or collector execution.

## P. Source Maintenance Recommendation

Recommended after commit:

- consider ChatGPT-side Source 24 or equivalent project-context patch for 8W-2 controlled metadata smoke
- do not update Source 11
- do not create Project Source files inside this repository
- do not create `docs/project_sources/`
