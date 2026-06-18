# Evidence Provider Boundary v1

Status: architecture contract draft

Scope: Sentigraph core and external evidence providers

This document defines the boundary between Sentigraph and any external system that acquires public-opinion evidence. It is a design contract only. It does not add a crawler, provider API, job runner, backend route, or collector integration.

## 1. Purpose

Sentigraph needs to analyze public-opinion evidence without becoming dependent on a single crawler, account setup, vendor, or collection runtime. This boundary document defines what Sentigraph owns, what an evidence provider owns, and how the two sides exchange normalized evidence safely.

The main goal is to keep Sentigraph provider-agnostic:

- Sentigraph receives evidence packages or future evidence streams.
- External providers perform acquisition and produce normalized artifacts.
- Provider output is treated as evidence, not truth.
- Sentigraph still applies validation, trust, provenance, review, deduplication, coverage display, and audit.

## 2. Core Principle

Sentigraph core is provider-agnostic.

Sentigraph must not depend on one crawler implementation. Provider-specific authentication, cookies, sessions, browser profiles, platform rate limits, profile health, host health, and safety gates stay outside Sentigraph core.

Sentigraph should be able to consume the same contract from:

- a private collector,
- an official API provider,
- a data vendor,
- a manual upload flow,
- a local snapshot package,
- or a future approved public parser.

If a provider can output the agreed Evidence Export v1 package, Sentigraph should not need a major frontend or analysis rewrite.

## 3. Responsibility Split

### Sentigraph Responsibilities

Sentigraph owns:

- create analysis request,
- receive package metadata,
- read Evidence Export v1 package,
- run validator,
- perform privacy and safety checks,
- apply trust, provenance, review, deduplication, and audit,
- display evidence coverage and coverage limits,
- create case draft from validated evidence,
- run analysis, Opinion Ecosystem, Sandbox, and report views,
- communicate user-facing boundaries.

Sentigraph must preserve user-facing clarity:

- imported or provider-supplied evidence is not automatically verified,
- selected public samples are not full-web coverage,
- selected public samples are not full-platform coverage,
- evidence coverage does not equal truth coverage,
- source limits and review status remain visible.

### Provider Responsibilities

The evidence provider owns:

- accept job request,
- plan sampling,
- enforce safety budget,
- handle platform-specific access,
- handle platform-specific auth outside Sentigraph,
- handle provider rate limits and cooldown,
- track profile health and host health if applicable,
- skip unsafe sources,
- generate Evidence Export v1 package,
- generate `validation_report`,
- refresh `package_index`,
- record `coverage_note` and `collection_log`.

The provider must not require Sentigraph core to store or operate provider credentials, cookies, sessions, or browser profiles.

## 4. Supported Provider Types

Current and planned provider categories:

| Provider type | Meaning | Current role |
| --- | --- | --- |
| `private_collector` | Local/private acquisition project that exports a normalized package | External provider, not Sentigraph core |
| `official_api_provider` | Approved official platform API integration | Future or platform-gated provider |
| `vendor_api_provider` | Contracted third-party data vendor | Future after POC, contract, and compliance checks |
| `manual_upload_provider` | User-uploaded CSV/Excel/JSON evidence | Existing ingestion style |
| `local_snapshot_provider` | Local evidence package copied or exported from a previous snapshot | Existing demo and sample style |
| `reviewed_public_parser_provider` | Narrow public parser approved for specific pages/sources | Future, only after review |

## 5. Explicit Non-Goals

Sentigraph core does not:

- store cookies or sessions,
- run platform crawler scripts,
- manage browser profiles,
- bypass login, captcha, or anti-bot controls,
- operate proxy evasion,
- collect private content,
- expose raw author identifiers,
- claim full-web or full-platform coverage,
- convert provider output into official truth automatically.

Sentigraph should avoid wording that implies:

- live scraping,
- hidden API use,
- automatic official verification,
- complete platform capture,
- guaranteed predictions,
- or real-world action execution.

## 6. Data Contract Principle

The shared artifact between provider and Sentigraph is:

- Evidence Export v1 package, or
- future Evidence Stream v1.

The current Evidence Export v1 package should include:

| File | Purpose |
| --- | --- |
| `manifest.json` | Package identity, schema, event metadata, generation metadata, package hash fields |
| `source_manifest.jsonl` | Source-level metadata and source coverage records |
| `evidence_items.jsonl` | Normalized evidence rows for ingestion and analysis |
| `evidence_items.csv` | Optional spreadsheet-compatible evidence rows |
| `collection_log.jsonl` | Provider-side collection and skip events |
| `coverage_note.md` | Human-readable coverage limits and sample caveats |
| `README.md` | Package overview and usage notes |
| `validation_report.json` | Machine-readable validation result |
| `validation_report.md` | Human-readable validation result |

Sentigraph should prefer machine-readable files for ingestion and human-readable files for review, demo, and audit.

## 7. Trust Boundary

Provider output is evidence, not truth.

Even if a package is structurally valid, Sentigraph must still apply:

- `provenance_type`,
- `verification_status`,
- `trust_label`,
- `review_status`,
- deduplication,
- coverage limits,
- audit timeline,
- manual review decisions,
- rejected-evidence exclusion where configured.

Recommended defaults:

- official API evidence can receive higher trust only when official source and scope are documented,
- vendor data should default to vendor-attested, not official verified,
- local snapshot and selected public sample packages should remain reviewable,
- missing source URLs, missing timestamps, screenshots, transcriptions, and repeated evidence should be review-visible.

## 8. Current Boundary in Sentigraph

Sentigraph owns the core evidence lifecycle:

```text
analysis request
-> evidence package metadata
-> local validation
-> evidence intake
-> trust/provenance/dedup/review/audit
-> analysis and report surfaces
-> user-facing boundary display
```

The provider owns acquisition:

```text
job request
-> provider planning
-> safety gate
-> external acquisition or local snapshot handling
-> package generation
-> package index refresh
-> provider job result
```

The boundary is crossed only through normalized package files or future normalized streams.

## 9. Future Migration Path

The private collector can later be replaced or supplemented by:

- official platform APIs,
- vendor APIs,
- manual upload packages,
- local snapshot packages,
- reviewed public parsers.

The migration path should not require major Sentigraph frontend or analysis rewrites if new providers output the same contract.

Future implementation phases:

1. File-based provider bridge reads `package_index.json` and validates local packages.
2. Sentigraph creates local analysis request JSON files for providers to pick up.
3. Provider writes local job result JSON and refreshes package index.
4. Sentigraph imports validated packages into case drafts.
5. Optional future HTTP provider API is introduced only after security and product gates.

## 10. Boundary Language

Use these terms:

- evidence provider,
- selected public sample,
- package generated,
- safety gate,
- coverage limitation,
- needs review,
- provider output,
- evidence package.

Avoid these terms in product-facing descriptions:

- crawling,
- full-web,
- real-time full-platform,
- official verified,
- hidden API,
- bypass,
- live scraping.

