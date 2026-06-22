# AnalysisRequests Frontend Module Boundary v1

Status: design only. This document proposes future frontend module boundaries and does not change UI behavior.

## Purpose

`frontend/src/pages/AnalysisRequests.jsx` has become the page shell, API orchestrator, form host, gate dashboard, audit timeline, debug JSON surface, and boundary-copy renderer for the full governance chain. The future refactor should reduce page complexity without changing `/#/analysis-requests` behavior.

## Proposed Future Folder Shape

Suggested future frontend structure:

```text
frontend/src/pages/analysisRequests/
  AnalysisRequestsPage.jsx
  AnalysisRequestsShell.jsx
  requestList/
  requestDetail/
  sections/
    RequestCoreSection.jsx
    ProviderResultSection.jsx
    ImportGovernanceSection.jsx
    ReviewOnlyCaseSection.jsx
    ReviewQueueSection.jsx
    DedupGovernanceSection.jsx
    AnalysisPromotionSection.jsx
    ManualAnalysisSection.jsx
    ReportGenerationSection.jsx
    SummaryReportCandidateSection.jsx
    FinalSummaryReportSection.jsx
    FinalSummaryReportExportSection.jsx
    ReportExportDownloadPackageSection.jsx
    ReportExportPublicAccessExternalDeliverySection.jsx
  components/
    GovernanceGateCard.jsx
    AuditTimeline.jsx
    BoundaryBlock.jsx
    EligibilitySummary.jsx
    JsonPreview.jsx
    StatusTag.jsx
    SafeModeFlags.jsx
  hooks/
    useAnalysisRequestData.js
    useGateFormState.js
  constants/
    boundaryCopy.js
    decisionOptions.js
    statusColors.js
  utils/
    copyHelpers.js
    displayFormatters.js
```

`frontend/src/pages/AnalysisRequests.jsx` should remain as a compatibility entrypoint during migration, re-exporting or rendering the new page module.

## API Helper Grouping

`frontend/src/api/sentigraphApi.js` can remain a facade while Analysis Request helpers move into smaller files:

```text
frontend/src/api/analysisRequests/
  core.js
  providerResult.js
  importGovernance.js
  reviewQueue.js
  dedupGovernance.js
  analysisPromotion.js
  manualAnalysis.js
  reportGeneration.js
  reportExport.js
  normalizers.js
```

Existing named exports should continue to work until all consumers migrate.

## Shared UI Components

### AnalysisRequests page shell

Owns layout, selected request, high-level loading state, and section ordering. It should not own every form field.

### Shared gate card components

Reusable for gate-only stages:

- title
- status tag
- decision
- upstream IDs
- readiness state
- warnings
- boundary block
- create button

### Shared audit timeline components

Reusable for append-only audit lists:

- audit ID
- reviewer label
- decision
- previous/new status when available
- analysis effect
- no-side-effect flags
- created timestamp

### Shared boundary block components

Boundary blocks must make unsafe states visible without creating actions. They should render booleans and notes as text/tags only.

### Shared copy and debug helpers

The current page contains many JSON copy/debug surfaces. Future helpers should stringify safely and never render raw objects directly.

### Phase-specific section components

Each governance family should own its own form values, submit handler, local derived state, and local warnings. Shared data should come through props from the page shell.

## Behavior Preservation

The refactor must preserve:

- route `/#/analysis-requests`
- current section order unless a separate UX decision is approved
- current form fields and payload keys
- current create/list/read behavior
- current boundary copy
- current JSON preview behavior
- current warning visibility
- current disabled/acknowledgement patterns

## Public Access and Delivery UI Boundaries

Frontend extraction must not add:

- clickable runtime file download link
- public URL link
- signed URL link
- external delivery button
- file-byte preview or download action
- ZIP package action
- object storage action
- portal publication action
- email send action

The public-access / external-delivery UI should remain a gate-only panel that records future candidate modes and boundary acknowledgements.

## Reducing Page and Bundle Complexity

The immediate objective is not aggressive code splitting. It is safer first to extract pure components and constants. Later phases may use dynamic import only if the application already has a stable pattern and browser smoke confirms no route regressions.

Recommended frontend migration order:

1. Extract display helpers and constants.
2. Extract read-only components: status tags, boundary blocks, audit timelines.
3. Extract one late-chain gate section with minimal dependencies.
4. Extract form state for that section.
5. Repeat one family at a time.
6. Split API helper groups only after section imports are stable.
7. Keep `sentigraphApi.js` re-exports until all sections use grouped APIs.

## Form Safety

Existing forms should remain unchanged during early extraction:

- same initial values
- same acknowledgement defaults
- same `false` no-side-effect flags
- same validation messages
- same submit handlers through adapter functions

No extracted section should submit automatically on mount or when props change.

## Smoke Expectations

After any frontend extraction:

- `npm --prefix frontend run build`
- open `/#/analysis-requests`
- confirm the moved section renders
- confirm no `[object Object]`, `undefined`, or `NaN`
- confirm no error boundary
- confirm no clickable runtime download or public/signed URL link
- confirm no console error/warn from the page

