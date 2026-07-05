# Sentigraph 8X-1 Metadata-only Provider Result to Review-only Staging Handoff Smoke Report v0.1

## Decision

- phase: 8X-1
- decision: ready
- privacy_issue_stop: no
- implementation_type: test-only smoke plus health report
- backend_service_code_changed: no
- backend_route_changed: no
- frontend_changed: no
- runtime_changed: no
- project_source_changed: no

## Scope

This phase strengthens the safe backend mainline from provider result metadata to review-only staging:

provider result metadata / controlled local package metadata
-> safe package resolver / provider result reader
-> review-only staging candidate

This phase does not use the External Collector Bridge validate path as the mainline because that path may read row files during validation. The 8X-1 smoke uses synthetic `tmp_path` fixtures only.

## What Was Proven

- A synthetic provider result metadata file can be read by the metadata-only provider result reader.
- A synthetic exported package directory can be resolved by package name under a configured temporary export root.
- Presence-only row files can exist with invalid sentinel content without being opened or parsed.
- The metadata-only local exchange smoke summary can create a review-only staging candidate.
- The resulting review-only staging summary contains safe metadata only.
- Path traversal is blocked before a candidate can become ready.
- Forbidden provider/package metadata fields block as privacy issues.
- Raw row/comment/identity sentinel values are not exposed in safe summaries.
- Runtime and production side-effect flags remain false.

## Evidence Row Boundary

Synthetic row-like files were created only as presence markers:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`

The focused smoke monkeypatches `Path.read_text` to fail if these files are opened. The passing test proves this handoff path did not open or parse them.

## Safety Boundaries

- collector_run: false
- real_api_called: false
- real_llm_called: false
- url_fetching: false
- scraping: false
- evidence_items_jsonl_parsed: false
- evidence_items_csv_parsed: false
- evidence_layer_written: false
- production_case_created: false
- analysis_run_created: false
- b_end_report_runtime_generated: false
- sandbox_public_event_runtime_generated: false
- frontend_api_route_added: false
- project_source_changed: false

## Files Added

- `backend/app/tests/test_private_collector_provider_result_to_review_only_staging_handoff_smoke.py`
- `docs/health/sentigraph_8x_1_metadata_only_provider_result_to_review_only_staging_handoff_smoke_report_v0_1.md`

## Validation Plan

Required focused validation:

```bash
python -m pytest backend/app/tests/test_private_collector_provider_result_to_review_only_staging_handoff_smoke.py -q
```

Relevant nearby validation:

```bash
python -m pytest backend/app/tests/test_private_collector_provider_result_reader.py backend/app/tests/test_private_collector_review_only_staging.py backend/app/tests/test_private_collector_review_only_staging_integration_smoke.py -q
python -m pytest backend/app/tests/test_local_exchange_reader.py backend/app/tests/test_analysis_request_golden_contracts.py -q
```

Static validation:

```bash
python -m py_compile backend/app/services/private_collector_package_resolver.py backend/app/services/private_collector_provider_result_reader.py backend/app/services/private_collector_review_only_staging.py
git diff --check
git status --short
```

## Not Implemented

- No External Collector Bridge validate-path integration.
- No backend route.
- No frontend UI.
- No runtime persistence.
- No real exchange directory read.
- No private collector inspection.
- No collector job.
- No real API or LLM.
- No URL fetching or scraping.
- No Evidence Layer write.
- No production case, production EvidenceItem, production analysis run, Review Queue runtime, B-end report, Sandbox/public event, export/download/public/final-delivery runtime.

## Next Recommended Task

Phase 8X-2 should remain backend-only and conservative. A safe next slice would be a docs-only or tests-only decision for whether the existing metadata-only staging summary may feed the already-controlled generated-run bridge. It should not parse evidence rows, add routes, add frontend, or write runtime state.
