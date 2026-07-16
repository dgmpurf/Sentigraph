# Sentigraph MVP-B02 One Real Metadata-only Review-only Staging Smoke Report v1.0

## Decision

- Decision: `ready`
- `privacy_issue_stop`: `no`
- Scope: one real provider-result metadata artifact, one in-process ASGI GET, one nonpersistent review-only candidate, and this report only.

## Goal state and authorization

- Goal requested: `MVP-B02-R1 Real Metadata-only Staging Smoke Recovery`
- Goal activation verified: yes.
- Goal completion verification: pending ready-only Git finalization at report creation.
- R1 approval SHA-256: `92bee9903eba8e12e0a124b58a02e623d2b48b9a55a21b743d09800c06411d56`
- Starting repository identity: `dgmpurf/Sentigraph`
- Starting branch: `main`
- Starting commit: `45de38fb2b99b750c744c5e86aa8cb8b48614c69`
- Starting origin alignment: ahead/behind `0/0` with a clean tracked and nonignored worktree.
- Prior B02 attempt classification: blocked during local TestClient asyncio plumbing before the B01 provider-result reader was reached; it was not counted as a successful smoke.

Prompt accounting after verified R1 activation: five engineering prompts consumed since Baseline v1.4, one conditional prompt consumed, one risk prompt consumed, five conditional prompts remaining, and one risk prompt remaining.

## Safe logical external configuration

- Results directory label: `external_collector_export_root/results`
- Export-root label: `external_collector_export_root`
- Exact result filename: `provider_result_helldivers2-psn-demo_20260614_055754.json`
- Adapter contract label: `sentigraph_analysis_request_v1_to_provider_job_result_v1`
- No absolute external path or raw process-local setting value is recorded in this report.

## Artifact identity

- Expected SHA-256: `6297f09939b205877940d1de964f9d7a0a6dec1f5817d7a6520949357cf8e553`
- Actual SHA-256: `6297f09939b205877940d1de964f9d7a0a6dec1f5817d7a6520949357cf8e553`
- Identity result: exact match.
- Direct artifact binary opens: 1.
- Direct artifact binary reads: 1.
- Direct artifact reopens: 0.
- The identity read did not parse JSON or inspect evidence content.

## In-process ASGI execution

- Invocation: `httpx.AsyncClient` with `httpx.ASGITransport` and the existing FastAPI application.
- Endpoint: `GET /api/v1/internal/staging/review-only/local-exchange/candidates/provider_result_helldivers2-psn-demo_20260614_055754.json`
- GET attempts: 1.
- Completed GET responses: 1.
- Automatic retries: 0.
- Second GET: 0.
- Alternate endpoint calls: 0.
- HTTP status: `200`.
- Response schema: `internal_operator_review_only_staging_local_exchange_response_v0_1`.
- Actual top-level response status: `ready_for_human_review`.
- Reader status: `metadata_ready`.
- Adapter status: `adapted`.
- Provider-result status: `accepted_metadata_only`.
- Package-resolution status: `accepted_metadata_only`.
- Candidate count: 1.
- Candidate review status: `ready_for_human_review`.
- Candidate promotion status: `promotion_required`.
- Gate staging status: `ready_for_human_review`.

The ASGI transport remained entirely in process. It started no Uvicorn process or listening server and performed no DNS resolution, loopback request, TCP/UDP connection, or external HTTP transport call.

## Access ledger

| Access class | Result |
| --- | --- |
| Direct artifact hash opens / reads | `1 / 1` |
| B01 provider-result metadata opens / reads | `1 / 1` |
| `manifest.json` opens / reads | `1 / 1` |
| `validation_report.json` opens / reads | `1 / 1` |
| `coverage_note.md` opens / reads | `1 / 1` |
| `README.md` opens / reads | `1 / 1` |
| `validation_report.md` opens / reads | `1 / 1` |
| Forbidden evidence/source/log file opens | `0` |
| Directory enumerations | `0` |
| File writes during GET | `0` |
| Persistence/database mutations | `0` |
| DNS calls | `0` |
| Bind/listen/accept calls | `0` |
| Loopback or external connects | `0` |
| External HTTP transport calls | `0` |
| Provider, collector, browser, scraping, or LLM calls | `0` |

The package resolver performed only fixed-name existence checks and the five allowed safe metadata reads. It did not open evidence rows, source manifests, or collection logs.

## Review-only boundary

| Boundary | Verified result |
| --- | --- |
| Metadata-only | true |
| Review-only | true |
| Human review required | true |
| Automatic trust upgrade | false |
| Candidate persistence | in memory only |
| Persistent staging write | false |
| Evidence Layer write | false |
| Production EvidenceItem creation | false |
| Production case creation | false |
| Production analysis run creation | false |
| Production Analysis Result creation | false |
| Downstream runtime call | false |
| Frontend action | false |
| Export or public delivery | false |

The returned `ready_for_human_review` status means only that metadata may be reviewed by a human. The `accepted_metadata_only` provider/package statuses and any source `package_ready` metadata do not mean human approval, trust approval, Evidence import approval, analysis-ready promotion, or production readiness. Promotion remains explicitly required.

## Safe-response validation

- No absolute external path was exposed.
- No process-local setting value was exposed.
- No raw provider-result JSON was returned in the report.
- No raw package metadata object, evidence content, author identifier, secret, or collector internal was exposed.
- A first-pass substring rule matched the required false-valued safety field `full_evidence_rows_parsed`. The conclusive runtime flag value and frozen B01 focused-test contract prove this was a field-name false positive, not evidence content. No raw-content finding remained.
- All process-local settings were restored after the single attempt, including on exception paths.

## No-side-effect matrix

- Provider or collector job execution: not run.
- External network, DNS, loopback server, browser, scraping, API, or LLM activity: not run.
- Evidence/source/log row parsing: not run.
- Persistent review queue or staging storage: not created.
- Evidence Layer, production evidence, case, analysis, analysis-result, report-runtime, public-event, or frontend action: not run.
- External artifact or package modification: none.
- Backend, test, frontend, runtime, or Project Source modification: none.
- Tag, release, export, and public delivery: none.

## Validation and Git boundary

Only Markdown required-section validation, forbidden-content scanning, `git diff --check`, an exact one-report allowlist check, cached-diff validation, and ready-only Git finalization are authorized after this report. The GET must not be repeated and the backend test suite must not be run.

Ready-only commit message: `Record MVP-B02 real metadata-only staging smoke`.

## Next boundary

Return the final B02-R1 receipt to ChatGPT for independent acceptance. Do not configure Sentigraph, do not call the endpoint again, and do not begin another B02 action without separate authorization.
