# Evidence Import Preview Contract v1

Status: architecture contract draft

Scope: future preview object after Evidence Import Plan and before Human Review Decision

This document is design-only. It does not implement preview runtime, evidence import, backend routes, frontend UI, row parsing, provider execution, collector execution, API calls, URL fetching, scraping, analysis generation, Sandbox fixture generation, public event page generation, or report generation.

## 1. Purpose

Evidence Import Preview is a future metadata gate between `EvidenceImportPlan` and a human review decision. It lets a reviewer understand what an import would use before any evidence rows are imported into the Sentigraph Evidence Layer.

Preview is not import. Preview is not case creation. Preview is not analysis. Preview is not official verification.

The first runtime implementation can be metadata-only, using the existing Evidence Import Plan and provider result metadata. A later runtime may read a small safe sample only after privacy checks.

## 2. Suggested Object Shape

```json
{
  "schema": "sentigraph_evidence_import_preview_v1",
  "preview_id": "preview_req_20260618_example",
  "plan_id": "import_plan_req_20260618_example",
  "request_id": "req_20260618_example",
  "created_at": "2026-06-18T00:00:00Z",
  "package_reference": {
    "package_name": "example-package",
    "package_role": "selected_public_sample",
    "package_path": "exports/sentigraph-evidence-v1/example-package",
    "package_index_path": "exports/sentigraph-evidence-v1/package_index.json"
  },
  "metadata_summary": {
    "evidence": 0,
    "comments": 0,
    "sources": 0,
    "roots": 0
  },
  "validation_summary": {
    "status": "warn",
    "errors": 0,
    "warnings": 0
  },
  "coverage_summary": {
    "coverage_level": "selected_public_sample",
    "not_full_web": true,
    "not_full_platform": true,
    "not_full_thread": true
  },
  "privacy_summary": {
    "raw_author_ids_removed": true,
    "raw_author_names_removed": true,
    "profile_urls_removed": true,
    "private_messages_excluded": true
  },
  "proposed_evidence_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low"
  },
  "dedup_preview": {
    "required": true,
    "computed_now": false,
    "reason": "Preview phase does not import or compute final dedup."
  },
  "sample_preview_policy": {
    "read_rows_now": false,
    "max_safe_sample_rows_future": 20,
    "redact_author_fields": true
  },
  "blockers": [],
  "warnings": [],
  "readiness": {
    "state": "ready_for_human_review",
    "can_import_now": false,
    "requires_review_decision": true
  }
}
```

## 3. Field Notes

| Field | Meaning |
| --- | --- |
| `schema` | Contract schema name. Use `sentigraph_evidence_import_preview_v1`. |
| `preview_id` | Stable preview identifier. |
| `plan_id` | Evidence Import Plan identifier. |
| `request_id` | Original Analysis Request identifier. |
| `created_at` | Preview creation timestamp. |
| `package_reference` | Package metadata copied from the import plan. |
| `metadata_summary` | Count summary only. It is not evidence row import. |
| `validation_summary` | Provider/package validation status. |
| `coverage_summary` | Coverage limits that must remain visible. |
| `privacy_summary` | Privacy flags that must be true or explicitly reviewed. |
| `proposed_evidence_defaults` | Defaults for future imported EvidenceItems. |
| `dedup_preview` | States whether dedup is required and whether computed now. |
| `sample_preview_policy` | Controls whether rows may be read for preview. |
| `blockers` | Reasons preview cannot proceed to human decision. |
| `warnings` | Non-blocking caveats for the reviewer. |
| `readiness` | Preview readiness for human review. |

## 4. Preview Boundaries

Import Preview must clearly state:

- preview is not import,
- preview does not create case records,
- preview does not run analysis,
- preview does not generate reports,
- preview does not generate Sandbox fixtures,
- preview does not generate public event pages,
- preview does not verify truth,
- preview does not upgrade provider output to official verification,
- preview does not mean full-web, full-platform, or full-thread coverage.

## 5. Metadata-Only MVP

The first runtime version should be metadata-only:

- read Evidence Import Plan,
- copy package reference,
- copy counts,
- copy validation summary,
- copy coverage summary,
- copy privacy summary,
- copy proposed governance defaults,
- compute no final dedup,
- read no evidence rows,
- parse no `evidence_items.jsonl`,
- create no case,
- import no evidence rows.

This MVP is safe because it continues the local planning chain without touching row-level evidence.

## 6. Future Safe Sample Preview

A later phase may support a small safe sample preview only if:

- privacy summary passes,
- raw author IDs are absent or removed,
- raw author names are absent or removed,
- profile URLs are excluded,
- private messages are excluded,
- reviewer understands it is a selected sample,
- maximum safe sample rows are capped, for example 20 rows,
- sample rows are redacted before display,
- no row-level data is stored outside intended local runtime artifacts.

Even with sample preview, final import still requires a human review decision.

## 7. Blocker Examples

Preview should block human approval if:

- package reference is missing,
- validation status is `failed`,
- validation errors are greater than 0,
- coverage claims full-web/full-platform without proof and limitation notes,
- privacy flags are missing,
- raw identity fields are detected,
- package lacks validation report or coverage note,
- safety status is `hold`, `cooldown`, or `blocked`.

## 8. Warning Examples

Preview can warn without blocking when:

- validation status is `warn` with zero errors,
- sample size is below target,
- some provider sources were skipped,
- source coverage is selected/controlled rather than broad,
- trust defaults remain `medium_low`,
- evidence will default to `review_needed`.

## 9. Current Non-Implementation Statement

This contract does not implement:

- import preview runtime,
- row parsing,
- evidence import,
- production case creation,
- analysis generation,
- Sandbox fixture generation,
- public event generation,
- B-end report generation,
- provider execution,
- collector jobs,
- real API calls,
- URL fetching,
- scraping,
- real LLM.

