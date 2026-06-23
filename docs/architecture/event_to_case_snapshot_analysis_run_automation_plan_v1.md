# Event To Case Snapshot Analysis Run Automation Plan v1

Status: architecture design only. No backend or frontend runtime is implemented by this document.

## 1. Purpose

This plan describes a future minimum automation path from a public event query to a review-ready case snapshot and analysis run candidate. It connects C-end event discovery expectations with B-end professional analysis boundaries without overclaiming live collection, full-web coverage, or official verification.

## 2. Future Concept Chain

```text
event query
-> AnalysisRequest
-> local request file
-> ProviderJob in external private collector
-> local result file
-> EvidenceExportPackage metadata
-> package validation
-> review-ready case candidate
-> case snapshot
-> analysis_run
-> Opinion Ecosystem mapping candidate
-> Sandbox sample candidate
-> B-end report candidate
```

The chain uses local file exchange only. It does not use HTTP/HTTPS exchange in the MVP.

## 3. Core Objects

- `event query`: user-facing event keyword or event hint.
- `AnalysisRequest`: Sentigraph-side request record with safety boundaries.
- `local request file`: versioned `sentigraph_analysis_request_v1` JSON written to a configured requests directory.
- `ProviderJob`: external private collector job concept; not run inside Sentigraph.
- `local result file`: versioned `sentigraph_provider_job_result_v1` JSON written to a configured results directory.
- `EvidenceExportPackage`: package metadata and validated package folder produced outside Sentigraph.
- `review-ready case candidate`: a candidate package that may be reviewed before import.
- `case snapshot`: a bounded view of available evidence for one event and time window.
- `analysis_run`: a specific analysis attempt over one snapshot, time window, and sample size.
- `Opinion Ecosystem mapping candidate`: future visual mapping candidate; not generated automatically.
- `Sandbox sample candidate`: future frontend/demo sample candidate; not generated automatically.
- `B-end report candidate`: future professional report candidate; not generated automatically.

## 4. Time Semantics

A generated case must be a snapshot, not an always-live truth object.

Required future fields:

- `event_id`
- `analysis_run_id`
- `time_window.start`
- `time_window.end`
- `sample_size`
- `coverage_note`
- `source_package_id`
- `review_status_summary`
- `dedup_status_summary`
- `analysis_input_scope`

Multiple `analysis_run` records may exist for one event over time. Later runs should not overwrite the historical meaning of earlier runs.

## 5. Coverage Semantics

Every generated case snapshot or analysis run must carry boundary copy:

- Selected available evidence only.
- Not full-web coverage.
- Not full-platform coverage.
- Not full-thread coverage.
- Not official verification unless an official source confirms it.
- Not causal proof.
- Provider output is evidence, not truth.

## 6. Review And Promotion Requirements

Before any professional analysis case is generated, future runtime should require:

- package metadata validation
- privacy scan
- review-only case creation
- review queue initialization
- human review decisions where needed
- dedup preview and dedup group review where needed
- analysis-ready promotion gate
- explicit human analysis trigger

Rejected evidence remains excluded by default. Weak evidence remains warning-marked. Duplicate evidence must not amplify risk, sentiment, or report conclusions.

## 7. Out Of Scope

This plan does not implement:

- production Evidence Layer write
- production case creation
- production review queue creation
- provider execution
- collector execution
- real API calls
- scraping
- HTTP/HTTPS exchange
- backend runtime
- frontend runtime beyond separate demo fixes
- B-end report runtime
- Sandbox fixture runtime
- public event page runtime
- real LLM runtime

## 8. Safe Next Phases

1. Wait for private collector local exchange adapter MVP evidence.
2. Design Sentigraph-side local exchange reader as a disabled-by-default runtime.
3. Add metadata-only provider result read smoke tests.
4. Add review-ready case snapshot planning gate.
5. Add manual analysis-run trigger only after review and dedup gates pass.
