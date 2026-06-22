# AnalysisRequests Backend Module Boundary v1

Status: design only. This document proposes future module boundaries and does not move code.

## Purpose

The backend Analysis Requests chain should be split into smaller modules while keeping the current API and persisted runtime data compatible. The split should make each governance family easier to review, test, and extend without accidentally creating production side effects.

## Proposed Future Package Shape

Suggested future package:

```text
backend/app/services/analysis_requests/
  __init__.py
  core.py
  provider_result.py
  import_governance.py
  review_only_case.py
  review_queue.py
  dedup_governance.py
  analysis_promotion.py
  manual_analysis.py
  report_generation.py
  summary_report_candidate.py
  final_summary_report.py
  final_summary_report_export.py
  report_export_download_package.py
  report_export_public_access_external_delivery.py
  audit_helpers.py
  runtime_io.py
  eligibility.py
  boundary_validators.py
  ids.py
  paths.py
```

The existing `backend/app/services/analysis_request_store.py` should remain as a facade during migration. Existing imports continue to work while functions delegate to the split modules.

## Proposed Boundary Families

### request_core

Owns:

- request creation and listing
- request ID generation facade
- config and runtime root label
- provider-agnostic request metadata

Stable public methods:

- `create_analysis_request`
- `list_analysis_requests`
- `read_analysis_request`
- `read_analysis_request_config`

### provider_result

Owns:

- local provider result record reading
- schema compatibility checks
- provider output boundary labels

Boundary:

- Provider output is evidence, not truth.
- No provider job execution happens in Sentigraph.
- No private collector project access.

### import_governance

Owns:

- case draft handoff
- evidence import plan
- metadata-only import preview
- review decision record
- dry-run import job
- execution preflight
- synthetic row reader dry-run
- limited real package row preview

Boundary:

- No production Evidence Layer write.
- No original package rows unless the specific existing preview runtime permits safe bounded metadata preview.
- No automatic promotion to analysis.

### review_only_case

Owns:

- review-only case creation
- staging import
- staged candidate batch references
- review-only lifecycle policy

Boundary:

- Review-only cases are not production cases.
- `analysis_included=false` stays the default until a later gate.

### review_queue

Owns:

- review queue initialization
- review item batch references
- review action runtime
- append-only review action audit
- review queue completion gate

Boundary:

- Human review decisions are audit-visible.
- Rejected items stay excluded from future analysis consideration.
- Privacy holds stop downstream gates.

### dedup_governance

Owns:

- dedup preview
- dedup group review action
- dedup group review audit
- dedup group completion readiness

Boundary:

- Duplicate groups are candidates until human confirmation.
- Duplicate count is preview metadata and must not amplify risk.
- No production dedup execution.

### analysis_promotion

Owns:

- analysis-ready promotion gate
- promotion decision audit

Boundary:

- Promotion is a human gate.
- It does not run analysis.
- It does not generate reports.

### manual_analysis

Owns:

- manual analysis trigger
- manual analysis trigger audit
- manual analysis execution
- manual analysis execution audit
- manual analysis result candidate
- analysis result boundary gate

Boundary:

- No automatic evidence write.
- No real LLM.
- No real platform calls.

### report_generation

Owns:

- report generation gate
- report generation gate audit

Boundary:

- Gate only unless a separate report runtime phase is explicitly active.

### summary_report_candidate

Owns:

- summary report candidate runtime
- summary report candidate audit
- candidate section policy

Boundary:

- Candidate is not final.
- Review gate is required.

### final_summary_report

Owns:

- final summary report review gate
- final summary report review audit
- final summary report runtime
- final summary report audit

Boundary:

- Final report remains local until export gates allow further handling.

### final_summary_report_export

Owns:

- final summary report export gate
- final summary report export gate audit
- export artifact runtime
- export artifact audit

Boundary:

- Export artifacts stay local.
- No public delivery.
- No signed URL.

### report_export_download_package

Owns:

- download/package gate
- gate audit
- local manifest-only package artifact record
- package artifact audit

Boundary:

- No file-byte route.
- No clickable runtime file exposure.
- No ZIP generation.

### report_export_public_access_external_delivery

Owns:

- public-access / external-delivery gate
- public-access / external-delivery gate audit
- future mode declarations

Boundary:

- Gate records only.
- No public access runtime.
- No external delivery runtime.
- No URL generation.
- No object storage upload.
- No portal publication.
- No email sending.

## Shared Backend Modules

### shared audit helpers

Reusable helpers should build append-only audit records with:

- previous state where relevant
- new state where relevant
- reviewer label
- reason or note
- analysis effect
- safe mode flags
- no-side-effect flags

### shared runtime IO helpers

Runtime IO helpers should own:

- root discovery
- ignored runtime directory creation
- safe JSON read/write
- path containment checks
- safe root labels
- runtime-relative labels

They must not expose absolute filesystem paths through API/UI contracts.

### shared eligibility and boundary validators

Validators should own:

- required upstream gate presence
- upstream readiness status
- no privacy blockers
- no unresolved review blockers
- no unsafe metadata
- no artifact content exposure
- no public URL or signed URL fields
- no file bytes

## Runtime Path Policy

Runtime paths stay under the existing ignored local runtime root. The refactor must not move existing records or require data migration in early phases. New modules should call shared path helpers rather than constructing paths inline.

No module should return absolute paths to API consumers. Public responses should use safe IDs, safe labels, and runtime-relative summaries only.

## API Compatibility Policy

The current router path prefix remains:

```text
/api/v1/analysis-requests
```

Future route modules may be mounted under the same router. Response models, field names, status values, and decision values remain compatible.

## Artifact Content Boundary

Backend modules must distinguish metadata records from artifact file content. Modularization must not introduce reading, parsing, copying, zipping, or exposing export artifact file bytes. Package metadata summaries already represented in records may be inspected; manifest package file content should not be read by the public-access / external-delivery gate.

## Evidence and Production Boundary

No backend extraction phase may write the production Evidence Layer, create a production case, create a production review queue, or run production dedup. Governance records remain local review artifacts until an explicit future promotion runtime is designed and approved.

