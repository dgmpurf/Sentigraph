# Manual Evidence Import Execution v1

Status: architecture design draft

Scope: future manual import path from Evidence Import Plan into the Sentigraph Evidence Layer

This document is design-only. It does not implement evidence import, backend routes, frontend UI, provider execution, collector execution, API calls, URL fetching, scraping, analysis generation, Sandbox fixture generation, public event page generation, or report generation.

## 1. Purpose

Sentigraph already supports a local file-based handoff chain:

```text
Analysis Request
-> Provider Result
-> Case Draft Handoff
-> Evidence Import Plan
```

The next product question is how a human reviewer should later approve and execute a manual Evidence import into the Sentigraph Evidence Layer. This document defines the future execution model, preconditions, governance defaults, target-case decisions, and safe implementation phases.

The core principle is conservative:

- Provider output is evidence, not truth.
- Evidence Import Plan is not an import.
- Import must be explicit, human-reviewed, auditable, and reversible where possible.
- Analysis, Sandbox, public event pages, and B-end reports are separate later actions.

## 2. Non-Goals

This design does not allow or implement:

- automatic import,
- automatic case creation,
- automatic analysis,
- automatic Sandbox fixture generation,
- automatic B-end report generation,
- automatic public event generation,
- provider execution,
- crawler execution,
- real API calls,
- URL fetching,
- scraping,
- platform account/session/cookie usage,
- official verification by provider claim alone,
- full-web or full-platform coverage claims.

## 3. Full Future Chain

The intended future flow is:

```text
Analysis Request
-> Provider Result
-> Case Draft Handoff
-> Evidence Import Plan
-> Import Preview
-> Human Review Decision
-> Manual Evidence Import Job
-> Evidence Governance
-> Analysis / Sandbox / Report only after later explicit action
```

Each arrow is a gate. A later stage must not silently happen because an earlier stage exists.

| Stage | Meaning | Must not imply |
| --- | --- | --- |
| Analysis Request | Local request metadata for a provider | Provider job has run |
| Provider Result | Provider reports package metadata | Package is truthful or official |
| Case Draft Handoff | Local case seed from eligible provider result | Case exists in production |
| Evidence Import Plan | Manual import planning record | Evidence rows were imported |
| Import Preview | Future metadata or safe-sample preview | Import or truth verification |
| Human Review Decision | Reviewer approves, rejects, or holds | Automatic analysis |
| Manual Evidence Import Job | Future explicit import execution | Full-web/full-platform coverage |
| Evidence Governance | Trust, review, dedup, audit | Official verification |
| Analysis / Sandbox / Report | Later explicit product action | Real-world action or guaranteed prediction |

## 4. Required Import Preconditions

A future manual import may proceed only if all conditions are satisfied:

- Evidence Import Plan exists.
- Human reviewer explicitly approves the import.
- `package_name` exists.
- `validation.errors = 0`.
- `validation.status` is `passed` or `warn`.
- Safety status is `safe` or `medium`.
- Evidence count is greater than 0.
- Coverage limitations are preserved.
- Privacy flags are present.
- Raw author ids, raw author names, profile URLs, and private messages are absent, removed, or explicitly excluded according to the active privacy policy.
- Default evidence governance policy is set.
- Audit record is created.

The future import must be blocked if any of these are true:

- `validation_failed`.
- `validation.errors > 0`.
- missing privacy flags.
- missing package reference.
- unsafe safety status, including `hold`, `cooldown`, or `blocked`.
- full-web or full-platform overclaim.
- provider output lacks coverage note or validation report.
- raw identity fields are present.
- reviewer did not approve.
- package requests private content, private messages, account-only data, or non-public content.

## 5. Future Import Behavior

A future manual import should:

- create or select target case explicitly,
- import `EvidenceItem` rows only after approval,
- default `review_status = review_needed`,
- default `verification_status = source_url_provided_unverified`,
- default `trust_label = medium_low`,
- preserve `provenance_type` and acquisition mode from package where valid,
- mark package source as `external_provider_package` or equivalent if the schema supports it,
- run dedup before analysis,
- create audit timeline entries,
- keep rejected or weak evidence from amplifying risk,
- keep coverage limitation notes visible in analysis and reports,
- never upgrade provider output to official verification automatically.

The import job should be idempotent:

- same package hash should not create duplicate evidence rows without explicit duplicate handling,
- same import decision should not create repeated import jobs unless forced by a new audit entry,
- failed imports should preserve enough metadata for review without storing unsafe raw content.

## 6. Case Target Decision

Future import UI should require an explicit target decision.

| Option | Meaning | Pros | Cons |
| --- | --- | --- | --- |
| Attach to existing case | Import into a selected existing case | Useful for ongoing event analysis | Risk of mixing incompatible coverage or trust levels |
| Create new case draft then import | Create a new case shell, then import evidence | Clear event separation | Needs careful naming and duplicate detection |
| Import into temporary review-only case | Import into a quarantine/review case first | Safest MVP; supports governance before analysis | Adds one extra promotion step |
| Reject package | Keep package metadata but do not import rows | Clear audit trail | No immediate analysis output |

Recommended MVP:

Use a review-only case first, then promote after review. This keeps package evaluation, evidence governance, and analysis separate.

## 7. Evidence Governance Defaults

Every future import from an external provider package should start with these defaults:

```json
{
  "review_status": "review_needed",
  "verification_status": "source_url_provided_unverified",
  "trust_label": "medium_low",
  "dedup_required": true,
  "audit_required": true,
  "coverage_warning_required": true,
  "low_trust_warning_required": true
}
```

If the source is an official API in the future:

- `verification_status` may be upgraded only by provider-specific proof and human review.
- The upgrade must not be based on provider claim alone.
- The scope of official access must remain visible.
- Official API evidence still needs coverage notes if it is not complete platform/thread coverage.

## 8. Security and Privacy

Sentigraph must not store:

- cookies,
- sessions,
- browser profile paths,
- account credentials,
- API keys,
- salts,
- private messages,
- non-public content.

Sentigraph must not import raw author IDs or raw author names unless a future privacy/legal review explicitly allows that data category for a specific purpose. Profile URLs and private messages must remain excluded by default.

Minor-sensitive mode must preserve stricter defaults:

- stronger redaction,
- no individual profiling,
- no raw identity retention,
- no private message import,
- review-only case preference,
- human review before analysis.

## 9. Future Implementation Phases

Recommended sequence:

### 6G: Import Preview Runtime

Create a metadata-only preview from Evidence Import Plan. It should not import rows. If a safe sample preview is later allowed, it should read only a small redacted sample after privacy checks.

### 6H: Human Review Decision Record UI

Add explicit approve/reject/hold decision records. The decision must be auditable and should be append-only.

### 6I: Manual Evidence Import Job MVP

Implement the first real manual import job, likely into a review-only case. It should require an approved review decision and should run dedup/governance defaults.

### 6J: Evidence Governance Review Queue Integration

Integrate imported evidence with review queue, trust labels, dedup summary, audit timeline, and rejected/weak evidence exclusion.

### 6K: Analysis After Import

Allow analysis only as a later explicit action after evidence governance. The UI should keep coverage limitations and low-trust warnings visible.

## 10. Boundary Language

Use these terms:

- manual import,
- import preview,
- review decision,
- Evidence governance,
- `review_needed`,
- `source_url_provided_unverified`,
- `medium_low`,
- coverage limitation,
- selected / controlled public sample,
- evidence, not truth,
- provider output.

Avoid these terms:

- automatic full import,
- full-web coverage,
- official verified,
- real-time crawl,
- crawler integration,
- prediction guarantee,
- public report generated,
- case completed.

## 11. Current Non-Implementation Statement

This document does not implement:

- evidence row import,
- production case creation,
- analysis generation,
- Sandbox fixture generation,
- public event page generation,
- B-end report generation,
- provider execution,
- collector jobs,
- real API calls,
- URL fetching,
- scraping,
- browser automation,
- official API provider,
- vendor API provider,
- real LLM.

