# Sentigraph Local Exchange Reader Contract Tests v1

Status: contract-test plan for future backend coverage.

## 1. Purpose

The contract tests ensure Sentigraph can safely inspect local exchange metadata without turning that inspection into live collection, production import, or report generation.

## 2. Initial test scope

The first runtime tests should cover:

- disabled-by-default config does not read files
- metadata-only provider result can be accepted
- forbidden fields block the result
- unknown schema/version blocks as unsupported
- unknown future platform rows require manual review
- invalid `evidence_items.jsonl` beside the package is not parsed

## 3. Required invariants

Every reader result must preserve:

- `metadata_only=true`
- `evidence_items_read=false`
- `evidence_items_parsed=false`
- `evidence_items_imported=false`
- `evidence_layer_written=false`
- `production_case_created=false`
- `analysis_run_created=false`
- `b_end_report_generated=false`
- `sandbox_fixture_generated=false`
- `public_event_page_generated=false`
- `provider_execution=false`
- `collector_jobs_run=false`
- `http_provider_integration=false`
- `real_api_calls=false`
- `real_llm_calls=false`
- `url_fetching=false`
- `scraping=false`
- `secrets_exposed=false`
- `raw_author_identifiers_exposed=false`

## 4. Fixture principles

Tests must use temporary fixture directories only.

Tests must not:

- read private collector directories
- read production runtime directories
- read `.env`
- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- import collector code
- run provider jobs
- create production Evidence, cases, review queues, dedup runs, analysis results, reports, Sandbox fixtures, or public event pages

## 5. Compatibility scenarios

The tests should cover:

- `compatible` result metadata
- `deprecated_compatible` metadata in a future test
- `unsupported_contract`
- `invalid_schema`
- `manual_review_required`
- unknown compatibility status
- unknown provider result status
- adapter mismatch

Unknown future platform metadata must not become runnable inside Sentigraph.

## 6. Future test extensions

Later phases can add:

- package index metadata-only reading
- path traversal protection tests
- UI status rendering tests
- fixture smoke with collector-exported metadata only
- review-ready case snapshot planning tests

Those extensions must still avoid parsing evidence rows or running collection.
