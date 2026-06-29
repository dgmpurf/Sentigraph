# Private Collector 8T-3 Metadata-only Package Resolver Helper Report v0.1

## A. Decision / Status

```text
phase = 8T-3
task = tiny_metadata_only_package_resolver_helper
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
```

Decision: ready.

## B. Implemented Scope

Implemented helper:

- `backend/app/services/private_collector_package_resolver.py`

Implemented targeted tests:

- `backend/app/tests/test_private_collector_package_resolver.py`

This helper is metadata-only. It is not wired to backend routes, frontend UI, production runtime, Evidence Layer, production case creation, analysis runs, report generation, Sandbox generation, public event generation, provider execution, or collector execution.

## C. Path Resolution Behavior

The helper implements the 8T-2 package path policy:

- `package_name` is preferred when it safely resolves under the operator-configured export root.
- `package_path_relative_to_export_root` is supported only when it is explicitly present and remains under the configured export root.
- legacy `package_path_relative` alone returns `manual_review_required`.
- path traversal is blocked.
- path escape outside `configured_export_root` is blocked.
- invalid package names such as nested paths, empty names, `.`, or `..` are rejected as metadata contract issues.
- missing package directories return `blocked_missing_package`.
- safe summary output does not include absolute filesystem paths.

## D. Metadata Boundary

Required package files are checked by existence only:

- `manifest.json`
- `source_manifest.jsonl`
- `evidence_items.jsonl`
- `evidence_items.csv`
- `collection_log.jsonl`
- `coverage_note.md`
- `README.md`
- `validation_report.json`
- `validation_report.md`

The helper may read only safe metadata files:

- `manifest.json`
- `validation_report.json`
- `coverage_note.md`
- `README.md`
- `validation_report.md`
- `package_index.json`

Boundary confirmations:

- `evidence_items.jsonl` existence only.
- `evidence_items.csv` existence only.
- no full rows parsed.
- no raw comments printed.
- no raw identifiers printed.
- privacy marker fields such as `raw_author_id_exported=false` and `raw_author_id_removed=true` are allowed.
- actual forbidden fields such as `raw_author_id` or `token` in metadata cause `blocked_privacy_issue`.

## E. Tests

Targeted tests cover:

- package name resolves safely under export root.
- package name is preferred over ambiguous legacy `package_path_relative`.
- explicit `package_path_relative_to_export_root` resolves safely.
- legacy `package_path_relative` alone returns `manual_review_required`.
- invalid package names are rejected.
- path traversal is blocked.
- path escape outside export root is blocked.
- required metadata file presence is reported.
- `evidence_items.jsonl` and `evidence_items.csv` are not parsed or opened.
- safe summary does not include absolute filesystem paths.
- privacy marker fields are allowed.
- actual forbidden metadata fields cause `blocked_privacy_issue`.
- missing package directory returns `blocked_missing_package`.
- missing required metadata files are reported without parsing evidence rows.

Latest targeted test result:

```text
python -m pytest backend/app/tests/test_private_collector_package_resolver.py
18 passed
```

Additional validation results:

```text
python -m pytest backend/app/tests/test_local_exchange_reader.py
9 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
7 passed

python -m py_compile backend/app/services/private_collector_package_resolver.py
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

- text metadata scanning is intentionally conservative and limited to field-like `key:` / `key=` patterns.
- helper is not connected to provider result reader or local exchange smoke yet.

P3 nice-to-have:

- future tests may cover Windows symlink escape behavior if a safe local fixture is approved.

## G. Recommended Next Step

If final validation remains green, prefer Phase 8T-4 metadata-only provider result reader / local exchange smoke.

Alternative safe option: Phase 8T-4 Search-to-Case product contract.

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
