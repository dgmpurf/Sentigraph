# Evidence Row Staging Contract v1

Status: architecture contract draft

Scope: future row-level staging object for manual evidence import execution

This document is design-only. It does not implement row reading, row parsing, evidence import, Evidence Layer writes, case creation, dedup, review queue initialization, analysis, Sandbox fixture generation, public event pages, B-end reports, provider execution, collector jobs, real APIs, URL fetching, scraping, or real LLM.

## 1. Purpose

Evidence row staging is the future quarantine-and-review layer between an approved Manual Evidence Import Job and any analysis-ready evidence pool.

Staging lets Sentigraph safely inspect and govern imported rows without claiming that they are verified, complete, or analysis-ready.

Staging does not mean analysis inclusion.

## 2. Suggested Object Shape

```json
{
  "schema": "sentigraph_evidence_row_staging_v1",
  "staging_id": "staging_20260618_example_000001",
  "import_job_id": "manual_import_job_20260618_example",
  "request_id": "req_20260618_example",
  "package_name": "example-package",
  "source_row_id": "row_hash_or_package_row_id",
  "row_index": 0,
  "row_status": "accepted_for_review",
  "evidence_candidate": {
    "evidence_type": "comment",
    "platform": "public_web",
    "source_url": "https://example.invalid/public-post",
    "title": "Safe public title",
    "body_text": "Safe public body text",
    "comment_text": "Safe public comment text",
    "created_at": "2026-06-18T00:00:00Z",
    "language": "zh-CN"
  },
  "governance_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "analysis_included": false
  },
  "privacy_check": {
    "raw_author_id_present": false,
    "raw_author_name_present": false,
    "profile_url_present": false,
    "private_message_present": false,
    "passed": true
  },
  "dedup_check": {
    "computed_now": false,
    "required_before_analysis": true,
    "content_hash": "sha256_example"
  },
  "audit": {
    "import_job_id": "manual_import_job_20260618_example",
    "package_name": "example-package",
    "source": "external_provider_package",
    "created_at": "2026-06-18T00:00:00Z"
  }
}
```

## 3. Row Status Values

| Status | Meaning | Analysis included |
| --- | --- | --- |
| `accepted_for_review` | Row passed basic schema/privacy checks and can enter review queue | No |
| `quarantined` | Row is retained for audit because it has warnings or incomplete data | No |
| `rejected` | Row is blocked from review and analysis because of validation, privacy, or policy failure | No |

`accepted_for_review` is not approval. It only means the row can be reviewed.

## 4. Privacy Blocker Behavior

Hard privacy blockers should trigger `privacy_stop` at execution level when systemic, or `rejected` / `quarantined` at row level when isolated and safe to record.

Hard blockers include:

- raw author id present,
- raw author name present,
- profile URL present,
- private message present,
- credential-like field present,
- cookie-like field present,
- token-like field present,
- session-like field present,
- browser profile path present,
- non-public content present.

When a hard privacy blocker is detected:

- do not import the row into analysis-ready evidence,
- do not print row content,
- do not print author-like values,
- record only safe reason codes,
- stop the import if the violation suggests package-level contamination.

## 5. Safe Fields

Future staging may retain these fields after validation and redaction:

- `evidence_type`
- `platform`
- `source_type`
- `acquisition_mode`
- `source_url` if it is a public URL and not a profile URL
- `title`
- `body_text`
- `comment_text`
- `created_at`
- `language`
- `like_count`
- `reply_count`
- `share_count`
- `view_count`
- `content_hash`
- `package_name`
- `import_job_id`
- coverage note
- validation report reference
- row-level warning codes

## 6. Forbidden Fields

Future staging must not retain:

- cookies,
- tokens,
- sessions,
- API keys,
- passwords,
- salts,
- browser profile paths,
- raw author ids,
- raw author names,
- profile URLs,
- private messages,
- non-public content,
- hidden account data,
- credentials or credential-like values.

If a package uses fields with similar names, the row sanitizer must treat them conservatively and either drop, redact, quarantine, or reject them.

## 7. Log Redaction Rule

Logs must never include full row content or author-like fields.

Allowed log content:

- row index,
- staging id,
- package name,
- import job id,
- validation status,
- privacy reason code,
- content hash prefix,
- count summary.

Disallowed log content:

- full title/body/comment,
- raw user labels,
- raw source row payload,
- source profile links,
- private messages,
- credentials,
- secrets.

## 8. Max-Row MVP Strategy

The first row staging MVP should use a conservative row limit:

- default max rows: small local fixture only,
- configurable max rows for controlled local testing,
- streaming reader,
- early privacy stop,
- partial import audit if stopped,
- no unbounded memory load.

The limit should be visible in audit output.

## 9. Staging Is Not Analysis Inclusion

Rows in staging must default to:

```json
{
  "review_status": "review_needed",
  "verification_status": "source_url_provided_unverified",
  "trust_label": "medium_low",
  "analysis_included": false
}
```

Analysis inclusion requires later explicit governance:

- no privacy blockers,
- dedup complete,
- review queue initialized,
- human review threshold met,
- coverage limitations acknowledged,
- rejected rows excluded,
- weak evidence flagged.

## 10. Current Non-Implementation Statement

This contract does not implement:

- row reader,
- row sanitizer,
- evidence staging storage,
- review queue writes,
- dedup,
- case writes,
- analysis,
- Sandbox fixture generation,
- report generation,
- public event generation,
- provider execution,
- collector jobs,
- real APIs,
- URL fetching,
- scraping,
- real LLM.
