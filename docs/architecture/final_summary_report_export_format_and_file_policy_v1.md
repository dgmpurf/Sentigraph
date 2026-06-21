# Final Summary Report Export Format and File Policy v1

## Purpose

This policy defines allowed future export formats and file placement rules for Final Summary Report Export Runtime.

It is design-only. It does not generate Markdown, PDF, PowerPoint, B-end report, Sandbox, public event, or any runtime file.

## Allowed Future Export Formats

Future export runtime may support only these artifact types unless a later design explicitly expands the list:

- `analyst_markdown`
- `executive_pdf`
- `briefing_deck_outline`
- `evidence_appendix_package`

## Format Definitions

### `analyst_markdown`

Markdown export is for an analyst-readable local report draft.

It must include:

- boundary block
- evidence scope
- coverage limitation
- warnings
- source and scope metadata
- audit trace

It must not be treated as a public post, B-end report, legal certification, official verification, or full-web/full-platform report.

### `executive_pdf`

PDF export is a rendered executive summary or client-facing local artifact only after future runtime support.

It must preserve all boundary sections and warnings. Visual layout must not hide uncertainty, weak evidence warnings, rejected evidence exclusion, duplicate no-amplification policy, or coverage limitations.

### `briefing_deck_outline`

Briefing deck outline is a structured outline for a future deck.

It is not a full PowerPoint deck unless a future PPTX generation runtime is explicitly designed and implemented. The outline must not imply that a `.pptx` file was generated.

### `evidence_appendix_package`

Evidence appendix package is a safe metadata and audit-reference bundle.

It may include:

- report section ids
- safe evidence scope summaries
- coverage limitation summaries
- warning summaries
- dedup and review summaries
- audit references

It must not include raw private rows, rejected evidence text, private messages, cookies, tokens, sessions, API key values, `.env` values, passwords, emails, phone numbers, raw author identifiers, or profile URLs.

## Required Content Policy

No export file may omit:

- boundary block
- evidence scope
- coverage limitation
- warnings
- audit trace
- source and scope metadata

No export file may claim:

- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- provider output is truth
- screenshots or transcriptions are automatically verified
- duplicate volume is independent truth strength

No export file may include:

- rejected evidence as analysis support
- duplicate evidence as separate risk amplification
- raw author identifiers
- raw author names
- profile URLs
- private messages
- cookies
- tokens
- sessions
- API key values
- `.env` values
- passwords
- emails
- phone numbers

## File Placement Policy

Future export runtime must write only under an ignored runtime folder, such as:

```text
runtime/analysis_requests/final_summary_report_exports/
```

or another explicitly ignored runtime folder documented before implementation.

Export runtime must not write into:

- `docs/`
- `frontend/`
- `backend/`
- `website/`
- `public/`
- committed demo asset folders
- project source files
- private collector project folders

## File Naming Policy

Future local export filenames should include:

- `request_id`
- `final_summary_report_id`
- `export_artifact_id`
- artifact type
- UTC timestamp

Suggested pattern:

```text
runtime/analysis_requests/final_summary_report_exports/<request_id>/<export_artifact_id>_<artifact_type>.<extension>
```

The filename must not include secrets, user handles, raw author identifiers, private account identifiers, or external profile paths.

## Public URL Policy

`public_url` must be null by default.

A public URL can only exist after a later public publishing or public event gate explicitly approves public output. Export runtime alone must not publish files.

## Future Runtime Failure Conditions

Future export runtime must block if:

- export gate is missing
- export gate is not ready
- export gate audit is missing
- boundary block is missing
- coverage limitation is missing
- warnings are missing
- audit trace is missing
- rejected evidence appears as support
- duplicates amplify risk
- trust or verification is upgraded
- private or secret-like fields are detected
- output path is outside the allowed runtime export folder
- requested format is not allowed

