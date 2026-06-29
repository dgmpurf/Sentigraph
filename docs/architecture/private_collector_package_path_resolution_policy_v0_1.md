# Private Collector Package Path Resolution Policy v0.1

Status: docs-only policy. This document does not implement runtime path resolution, provider execution, collector execution, package import, Evidence Layer writes, case creation, analysis, reports, Sandbox generation, public event generation, API routes, frontend UI, or tests.

## 1. Purpose

This policy defines how a future Sentigraph metadata-only provider handoff should resolve package locations from a private collector Evidence Export v1 package index.

The policy exists because 8T-1 found a non-blocking ambiguity: `package_path_relative` was stored relative to a higher-level export context, while the actual package was also present directly under the configured export root by `package_name`.

Sentigraph must resolve package metadata safely without becoming a crawler, without importing collector code, and without parsing full evidence rows during metadata handoff.

## 2. Core Terms

`configured_export_root`
: The trusted root directory configured by the operator for metadata-only package discovery. Sentigraph may inspect only approved metadata below this root.

`package_name`
: The preferred canonical package locator. It should be a directory name, not a path expression.

`package_path_relative_to_export_root`
: A future allowed path field only when it is explicitly declared relative to `configured_export_root`.

`package_path_relative`
: A legacy or ambiguous field. If the base directory is not explicitly declared, this field must not be treated as canonical.

`resolved_package_path`
: An internal backend-only filesystem path after validation. It must not be exposed to frontend, UI, API responses, reports, public pages, or logs that may be shared externally.

## 3. Canonical Resolution Order

Future Sentigraph metadata-only handoff should resolve a package using this order:

1. Validate `configured_export_root`.
2. Prefer `configured_export_root / package_name` when `package_name` is present and the resulting directory exists.
3. If `package_name` does not resolve and `package_path_relative_to_export_root` is present, resolve `configured_export_root / package_path_relative_to_export_root`.
4. If only legacy `package_path_relative` is present and its base is unclear, set status to `manual_review_required`.
5. If metadata points outside `configured_export_root`, set status to `blocked_path_escape` or `privacy_issue_stop`.

If both `package_name` and `package_path_relative` exist, and `configured_export_root / package_name` exists, Sentigraph should prefer `package_name`.

## 4. Required Validations

Future implementation must validate:

- `configured_export_root` exists and is operator configured.
- `package_name` contains no path separators.
- `package_name` is not empty.
- `package_name` is not `.` or `..`.
- `package_path_relative_to_export_root` does not escape the configured root.
- no path traversal segments such as `..` are accepted.
- symlink resolution does not escape `configured_export_root`.
- resolved package path is a directory.
- required metadata files can be checked by name.

If symlink behavior cannot be safely resolved on the host OS, status must be `manual_review_required` or `blocked_path_escape`.

## 5. Exposure Rules

Absolute package paths from collector metadata must not be exposed to:

- frontend UI
- public API responses
- public event pages
- reports
- downloadable artifacts
- generated run metadata shown to users

Allowed user-facing references:

- `package_name`
- `package_role`
- `case_id`
- `validation_status`
- safe counts
- generic note such as `configured_export_root package`

Internal logs may contain a redacted or operator-local diagnostic path only when explicitly intended for local debugging. Shared reports should avoid absolute private paths except for explicitly configured root names in internal health reports.

## 6. Metadata Handoff Boundaries

During metadata handoff, Sentigraph must not:

- copy package files into production storage
- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- print raw comments
- print raw author identifiers
- write Evidence Layer
- create a production case
- create an `analysis_run`
- generate a B-end report runtime
- generate a Sandbox/public event runtime
- generate a public event page
- execute provider or collector jobs
- call real APIs or real LLMs
- fetch URLs or scrape pages

Required evidence-row files may be checked by existence only.

## 7. Examples

### 7.1 Valid `package_name` Resolution

Input:

```json
{
  "configured_export_root": "operator configured root",
  "package_name": "helldivers2-psn-demo_20260614_055754"
}
```

Resolution:

```text
configured_export_root / helldivers2-psn-demo_20260614_055754
```

Decision:

```text
accepted_metadata_only
```

Only metadata files may be read. Evidence rows remain unparsed.

### 7.2 Valid `package_path_relative_to_export_root`

Input:

```json
{
  "configured_export_root": "operator configured root",
  "package_path_relative_to_export_root": "helldivers2-psn-demo_20260614_055754"
}
```

Decision:

```text
accepted_metadata_only
```

The field is acceptable because its base is explicit.

### 7.3 Ambiguous Legacy `package_path_relative`

Input:

```json
{
  "package_path_relative": "exports/sentigraph-evidence-v1/helldivers2-psn-demo_20260614_055754"
}
```

Decision:

```text
manual_review_required
```

This field is ambiguous unless a separate contract states the base directory.

### 7.4 Blocked Absolute Path Exposure

Input:

```json
{
  "absolute_package_path": "G:/private/path/to/package"
}
```

Decision:

```text
blocked_path_escape
```

Absolute collector paths must not become frontend/UI/API fields. Internal operator-only diagnostics may exist only in local health reports when explicitly allowed.

### 7.5 Blocked Path Traversal

Input:

```json
{
  "package_path_relative_to_export_root": "../private-runtime/package"
}
```

Decision:

```text
blocked_path_escape
```

Path traversal is blocked even if the target exists.

## 8. Recommended 8T-3 Runtime Shape

A future tiny helper may implement:

- input validation for `configured_export_root`
- `package_name` resolution
- `package_path_relative_to_export_root` resolution
- legacy `package_path_relative` manual-review classification
- required metadata file presence checks
- safe status output

It must not parse `evidence_items.jsonl` or `evidence_items.csv`, and it must not write Evidence Layer or create a case.

