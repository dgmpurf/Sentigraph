# Sentigraph MVP-F02 Real Safe-payload Capture Readiness and Access Contract v1.0

## 1. Title and Milestone Identity

- milestone_id = MVP-F02
- prompt_package_id = MVP-F02-P1
- baseline_version = 1.0
- baseline_task_classification = planned_fixed_milestone
- capture_contract_schema = sentigraph_mvp_f02_real_safe_payload_capture_readiness_and_access_contract_v1_0
- capture_contract_version = 1.0
- contract_mode = docs_only_future_single_access_capture_contract

Cardinality and access limits:

- source_access_sessions_allowed = 1
- approved_package_count = 1
- approved_row_source_count = 1
- approved_candidate_count = 1
- approved_output_payload_count = 1
- alternate_source_allowed = no
- fallback_allowed = no
- automatic_retry_allowed = no
- source_file_reopen_allowed = no
- directory_enumeration_allowed = no
- candidate_substitution_allowed = no
- package_substitution_allowed = no
- row_substitution_allowed = no
- schema_substitution_allowed = no
- hash_substitution_allowed = no

Current no-side-effect state:

- real_package_accessed_now = no
- real_row_read_now = no
- real_source_line_length_measured_now = no
- real_payload_created_now = no
- parser_implemented_now = no
- runtime_target_accessed_now = no
- database_accessed_now = no
- gate_activated_now = no
- write_performed_now = no

## 2. Purpose

This contract freezes one fail-closed procedure for a later MVP-F03 capture of
one safe payload for the already locked candidate. It defines one approved
source file, one physical record position, one source-file open, one protected
payload, one safe receipt, exact field origins, and an independent MVP-F04
handoff before any real source is opened.

The corrected contract additionally fixes a 1048576-byte raw physical-line cap,
one binary probe read, strict UTF-8 decoding, strict duplicate-free standard JSON
parsing, and parser-safe receipt evidence. It does not claim the real row fits
the cap and does not implement the future procedure.

The contract is deliberately narrower than the historical row-preview helper.
MVP-F03 may inspect only the first physical JSONL record selected by the
committed identity chain. It may not skip a malformed or blocked first record
and continue looking for another row.

## 3. Approval and No-authorization Boundary

The exact approval received for this document-only milestone was:

`APPROVE_SENTIGRAPH_MVP_F02_REAL_SAFE_PAYLOAD_CAPTURE_READINESS_AND_ACCESS_CONTRACT_DOCS_ONLY`

The exact approval received for the bounded-line and strict-parser correction was:

`APPROVE_SENTIGRAPH_MVP_F02_BOUNDED_SOURCE_LINE_AND_STRICT_JSON_PARSER_CONTRACT_CORRECTION_DOCS_ONLY`

Together they authorize tracked-repository inspection and these two MVP-F02
documents only. The correction approval adds no implementation or data-access
authority. Neither approval authorizes MVP-F03, real source access, package or
row reading, source-line measurement, payload creation, output-directory
creation, database access, gate activation, persistence, or any production
object.

No later authorization text is supplied here. Historical 9A approvals remain
historical governance evidence and cannot be reused as permission for F03.

## 4. Baseline Classification and Prompt Accounting

- baseline_document_commit = cb81379ccc48ba5177c1b23adab2ea90fbad6408
- latest_committed_checkpoint = 35dd3e1cd0e317d2b0514ef99d1ca30dd13ffe4d
- fixed_prompt_budget = 20
- conditional_prompt_allowance = 10
- risk_buffer_prompt_allowance = 4
- consumed_engineering_prompts_since_baseline = 3
- consumed_fixed_prompts = 2
- consumed_conditional_prompts = 0
- consumed_risk_prompts = 1
- remaining_fixed_prompts = 18
- remaining_conditional_allowance = 10
- remaining_risk_buffer = 3
- MVP_F02_prompt_consumed = yes
- MVP_F02_risk_correction_prompt_consumed = yes
- MVP_C01_trigger_eligible = yes
- MVP_C01_authorized = no
- MVP_C01_consumed = no
- MVP_C01_blocking_MVP_F02 = no
- MVP_C02_triggered = no
- MVP_C02_authorized = no
- MVP_C02_consumed = no

The fixed Prompt was consumed when the original F02 Goal started. The correction
Prompt is consumed from the four-Prompt risk buffer under `MVP-CHG-001`; the
risk-buffer total remains 4 and its remaining balance becomes 3. No conditional
allowance is consumed. The full approved change-control record is in the
companion decision. MVP-C01 and MVP-C02 remain unused and do not broaden this
contract.

## 5. Git and Committed Evidence Anchors

| Evidence | Commit | Contract role |
| --- | --- | --- |
| 9A-16 bounded one-row review report | `870257ad41c5dda5c88081738fb7374fcba64663` | Proves one approved source file, one parsed row, and no alternate source in the prior bounded review |
| 9A-16B and 9A-16C locked-identity reports | `11ae4bb33e1d45afc6153e4dd28be0e4b5178e34` | Authoritative package, row-source, preview-row, candidate, schema, and safe-hash governance binding |
| 9A-19 final-write decision record | `20f1bbb564430ebcf6f95dcdbfe0a45af67093e2` | Historical exact-candidate governance only; not F03 permission |
| 9A-20 inactive gate decision | `2d34a21cd38766da678d58985af4d6afbf8775d1` | Confirms gate defined but inactive |
| 9A-21 readiness audit | `20cfe59498ee9967376f24dc291024032ca85f7b` | Identifies the missing full safe payload and keeps activation paused |
| 9A-22 prerequisite contract and decision | `1c853ae2563c5e4d000767e52a351660c3c0c43c` | Defines payload v0.1, strict fields, canonical hash, and no-production boundaries |
| 9A-23B service/tests/report | `e3fb9f9249069fc72b23dd3bd5b6e197d1417f7c` | Implements and validates the current payload validator and synthetic persistence boundary |
| MVP-F01 independent audit | `35dd3e1cd0e317d2b0514ef99d1ca30dd13ffe4d` | Accepts the frozen synthetic surface and records the remaining real-payload gap |
| Baseline v1.0 documents | `cb81379ccc48ba5177c1b23adab2ea90fbad6408` | Assigns one fixed Prompt to F02 and separates F02/F03/F04 |

Tracked implementation anchors:

- `backend/app/services/controlled_row_preview.py`
- `backend/app/services/evidence_layer_one_real_candidate_pre_write_review.py`
- `backend/app/services/evidence_layer_one_real_locked_candidate_pre_write_review.py`
- `backend/app/services/controlled_evidence_layer_write_candidate_from_production_import_candidate.py`
- `backend/app/services/governed_nonproduction_evidence_persistence.py`
- `backend/app/tests/test_governed_nonproduction_evidence_persistence.py`
- `.gitignore`

## 6. Authoritative Identity Records

The authoritative identity record is:

`docs/health/sentigraph_9a_16c_one_bounded_locked_candidate_identity_capture_rerun_no_write_report_v0_1.md`

at commit `11ae4bb33e1d45afc6153e4dd28be0e4b5178e34`.

The companion 9A-16B report at the same commit and the 9A-16 report at commit
`870257ad41c5dda5c88081738fb7374fcba64663` provide the prior package, one-file,
one-row, lineage, and no-write evidence.

F03 must load, without alteration, exactly these fields from the authoritative
9A-16C record:

- approved package name;
- approved package role;
- approved case ID hint;
- approved row source;
- selected preview-row opaque ID;
- selected preview-row safe hash;
- final candidate ID;
- final candidate safe hash;
- final candidate schema;
- identity schema and version;
- hash algorithm and hash-input scope;
- candidate lock status.

The values are not duplicated in this contract. Their commit-and-path binding is
the authority. F03 must stop if the tracked record is absent, changed, ambiguous,
or does not expose one complete identity object.

## 7. Exact Capture Path

The selected future path is one bounded ephemeral in-memory F03 procedure. No
persistent reader or script is created by F02.

1. Read the authoritative tracked governance records at their committed anchors.
   This is governance metadata access and does not count as real source access.
2. Import only the committed schema constants and pure candidate adapters. Do not
   invoke a package resolver, exchange reader, provider, collector, or database.
3. Obtain the exact source-file object only from
   `controlled_row_preview.APPROVED_ROW_FILE`; do not accept a path argument.
4. Lexically verify its basename equals the authoritative approved row source and
   that the package/role/case/source constants match the 9A-16C record. Do not
   resolve, stat, list, glob, or enumerate the containing directory.
5. Open that exact source file once in binary read-only mode. This begins and
   consumes the single source-access session. Do not use text-mode universal
   newline translation.
6. Make exactly one `handle.readline(1048577)` call. Do not call unbounded
   `readline()`, iterate the handle, seek, use `tell()` to probe, read the whole
   file, inspect a second line, or infer size from `stat()`.
7. Apply the byte-count outcomes in section 8 before decoding. If the result is
   within the 1 MiB contract cap, remove at most one trailing `LF` byte and, only
   when that `LF` was removed, one immediately preceding `CR` byte. Do not apply
   broad stripping or alter bytes inside JSON strings.
8. Decode the normalized bytes exactly with
   `normalized_line_bytes.decode("utf-8", errors="strict")`. Do not replace
   invalid bytes, repair a BOM, or try another encoding.
9. Parse the decoded line with an equivalent of
   `json.loads(decoded_line, object_pairs_hook=reject_duplicate_keys,
   parse_constant=reject_nonstandard_numeric_constant)`. Reject duplicate keys
   in every nested object and reject `NaN`, `Infinity`, and `-Infinity` without
   echoing the key or token. Require the top-level value to be exactly one JSON
   object.
10. Reproduce the current row-preview safe projection for physical row index 1,
   then build the existing one-candidate in-memory lineage through the committed
   pure candidate adapters. Each stage must contain exactly one item.
11. Verify the resulting preview-row opaque ID/hash and final candidate
   ID/hash/schema against the authoritative 9A-16C values.
12. Build exactly one payload object matching
    `sentigraph_exact_locked_candidate_safe_write_payload_v0_1`, compute its
    canonical `input_safe_hash`, and call
    `validate_exact_locked_candidate_safe_write_payload`.
13. Recursively scan the payload and receipt for forbidden keys and values.
14. Write one protected payload and one safe receipt to the output class in
    section 15 with exclusive, non-overwriting creation. Close and discard all
    in-memory source data.

The existing broad row-preview loop is not called as the file reader because it
may inspect later lines after an invalid first line. F03 uses its committed safe
projection rules but enforces the stricter first-record-only bound inline.

## 8. Single Source-access Session Definition

- source_access_sessions_allowed = 1
- source_file_open_count_maximum = 1
- source_file_reopen_count_maximum = 0
- physical_rows_read_maximum = 1
- parsed_row_objects_maximum = 1
- selected_rows_maximum = 1
- payload_artifacts_maximum = 1
- receipt_artifacts_maximum = 1
- source_file_open_mode = binary_read_only
- source_line_utf8_byte_limit = 1048576
- source_line_probe_read_size = 1048577
- source_read_call_count_maximum = 1
- source_seek_allowed = no
- source_second_read_allowed = no
- source_line_terminator_counted_in_limit = yes
- UTF8_decode_errors = pause
- UTF8_replacement_character_fallback_allowed = no
- UTF8_BOM_auto_repair_allowed = no
- encoding_fallback_allowed = no
- top_level_JSON_object_required = yes
- duplicate_JSON_keys_allowed = no
- nonstandard_numeric_constants_allowed = no
- NaN_allowed = no
- positive_infinity_allowed = no
- negative_infinity_allowed = no

Reading Git-tracked governance records and importing code constants do not count
as real source access. The first successful source-file open starts and consumes
the session. One binary handle may perform exactly one
`readline(source_line_utf8_byte_limit + 1)` call. Closing the handle ends source
access. Payload and receipt writes do not create another source session.

The 1 MiB cap applies to the complete raw physical-line byte sequence returned
by that one call. An `LF` or `CRLF` terminator is included in the count. It is a
contract safety cap, not evidence that the unknown real row fits. F02 did not
open the source or measure the row.

Exact byte-count outcomes:

| Read result | Outcome | Parser and output rule |
| --- | --- | --- |
| `len(raw_line) == 0` | `paused_zero_matching_row` | Session consumed; bytes read 0; no decode, parse, payload, retry, or second read |
| `len(raw_line) > 1048576` | `paused_source_line_exceeds_bound` | Bytes read 1048577; oversize true; no decode, parse, payload, retry, or second read; fresh governance required |
| `0 < len(raw_line) <= 1048576` | continue | Normalize at most one `LF` and its immediately preceding `CR`, then apply strict UTF-8 and strict JSON rules |

The bounded probe never checks whether later physical lines exist. If the first
line exceeds the cap, the cap is not raised automatically and no second read is
allowed.

A failure before source open records `source_access_session_consumed = false`.
A failure after source open records it as true. Neither outcome permits an
automatic retry. Any later attempt needs a new human decision and governance
record; no unused portion of the failed session carries forward.

## 9. Package and Row Binding

The capture is bound to one package and one row source by reference to the
authoritative 9A-16C record, not by a caller-supplied name or path.

Required pre-open checks:

- authoritative package identity is complete;
- package role and case ID hint equal committed locks;
- approved row source equals `evidence_items.jsonl`;
- committed `APPROVED_ROW_FILE` basename equals that source label;
- physical path is never placed in payload, receipt, report, or exception text;
- no alternate package, CSV, source manifest, collection log, or fallback file
  is opened.

Required post-parse checks:

- physical row index = 1;
- preview row count = 1;
- every downstream candidate-stage count = 1;
- final item schema and set schema equal current committed constants;
- preview and final identity values match 9A-16C exactly;
- all lineage references are continuous and opaque.

## 10. Row-selection Algorithm

The selector is the first physical JSONL record only. This is supported by the
committed 9A-16 evidence showing one inspected row and by the 9A-16C preview-row
identity produced for physical row index 1.

Algorithm:

1. Set `row_index = 1` before source open.
2. Open the approved source once as `binary_read_only` and make exactly one
   `readline(1048577)` call.
3. Apply the byte-count outcomes in section 8. EOF pauses. Oversize pauses before
   decoding or parsing. Neither outcome permits another read.
4. Remove only the permitted trailing line terminator bytes, decode as strict
   UTF-8, and treat decoded JSON-whitespace-only content as blank and paused.
5. Parse one strict JSON object. Reject malformed JSON, a duplicate key at any
   object depth, `NaN`, `Infinity`, `-Infinity`, or a non-object top level with
   its distinct safe outcome and no raw-value echo.
6. Derive the opaque preview-row ID using the committed row-index algorithm.
7. Build the versioned safe preview projection and its SHA-256 hash using the
   9A-16C algorithm.
8. Require exact equality with the committed preview-row ID and safe hash.
9. Build one candidate chain and require exact final candidate ID/hash/schema.
10. Require each candidate container to contain exactly one item. Zero or more
   than one item stops before payload output.

Strict decode and parser contract:

- Size validation occurs before decoding.
- Decoding is exactly
  `normalized_line_bytes.decode("utf-8", errors="strict")`.
- Invalid UTF-8 yields `paused_source_line_invalid_utf8`, records no offending
  bytes, offsets, decoded fragment, exception message, or source path, and does
  not attempt JSON parsing.
- `reject_duplicate_keys` runs for every JSON object, including nested objects,
  and rejects the second occurrence of an identical decoded key within the same
  object. It raises only a bounded internal parser outcome and never exposes the
  duplicate key text.
- `reject_nonstandard_numeric_constant` rejects `NaN`, `Infinity`, and
  `-Infinity` without echoing the token.
- Malformed standard JSON yields `paused_strict_JSON_parse_failure`.
- A duplicate key yields `paused_duplicate_JSON_key_detected`.
- A non-standard numeric constant yields
  `paused_nonstandard_numeric_constant_detected`.
- A parsed top-level array, string, number, boolean, or null yields
  `paused_source_row_not_object`.
- For every parse-stage failure, `strict_JSON_parse_passed = false`,
  `rows_examined_or_parsed = 0`, `rows_selected = 0`, and
  `payload_artifact_count = 0`; the consumed source session permits no reopen,
  second read, retry, fallback, or raw-value echo.

These rules define a future inline F03 procedure only. F02 does not implement or
execute a parser.

There is no fuzzy title, text-similarity, latest-row, first-valid-row, package
prefix, case guess, alternate hash, or visual similarity fallback. Because the
selector names one fixed physical position, it cannot select two source rows.
Any downstream multiplicity is still an explicit stop.

## 11. Complete Safe-payload Field Allowlist

Common rules used below:

- `CONST`: exact constant from current committed validator.
- `GOV`: exact field from the committed 9A-16C identity record.
- `ROW`: value derived only from the one selected source row in memory.
- `CHAIN`: value from the exactly-one committed pure candidate chain.
- `DERIVED`: deterministic canonical safe transformation defined here.
- `H=yes`: included in `input_safe_hash`; `H=no`: the hash field itself.
- Opaque strings are 3-160 characters and may not be URL/path-like.
- Hashes are exactly 64 lowercase hexadecimal characters.
- Safe label lists contain at most 20 opaque labels of at most 80 characters.
- Any missing required field, unknown field, type/bound error, sensitive value,
  or origin mismatch yields pause with no payload.

### 11.1 Top-level fields

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `payload_schema` | string, exact | CONST | Exact v0.1 schema name | H=yes | mismatch stops |
| `payload_version` | string, exact `0.1` | CONST | No substitution | H=yes | mismatch stops |
| `source_candidate_set_schema` | string, exact | CONST | Exact current set schema; require GOV final schema equality | H=yes | mismatch stops |
| `source_candidate_schema` | string, exact | CONST | Exact current item schema | H=yes | mismatch stops |
| `source_schema_versions` | object, 4 exact keys | CONST | Section 11.2 only | H=yes | missing/extra/mismatch stops |
| `immutable_candidate_identity` | object, 14 exact keys | GOV | Section 11.3 only | H=yes | any mismatch stops |
| `candidate_projection` | object, strict fields | DERIVED | Assemble only the individually sourced fields in section 11.4 | H=yes | unknown/missing required field stops |
| `lineage_projection` | object, 7 exact keys | DERIVED | Assemble only the individually sourced fields in section 11.5 | H=yes | discontinuity stops |
| `boundary_projection` | object, 11 exact keys | CONST | Section 11.6 only | H=yes | weakened boundary stops |
| `input_safe_hash` | string, 64 hex | DERIVED | SHA-256 over all other top-level fields | H=no | mismatch stops |

### 11.2 Source schema versions

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `source_schema_versions.candidate_set_schema` | exact string | CONST | Equal set schema | H=yes | mismatch stops |
| `source_schema_versions.candidate_schema` | exact string | CONST | Equal item schema | H=yes | mismatch stops |
| `source_schema_versions.identity_schema` | exact string | CONST | Equal identity schema; require GOV equality | H=yes | mismatch stops |
| `source_schema_versions.payload_schema` | exact string | CONST | Equal payload schema | H=yes | mismatch stops |

### 11.3 Immutable candidate identity

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `immutable_candidate_identity.approved_package_name` | opaque string | GOV | Copy exact committed value | H=yes | missing/different/unsafe stops |
| `immutable_candidate_identity.approved_package_role` | opaque string | GOV | Copy exact committed value | H=yes | mismatch stops |
| `immutable_candidate_identity.approved_case_id_hint` | opaque string | GOV | Copy exact committed value | H=yes | mismatch stops |
| `immutable_candidate_identity.approved_row_source` | opaque string | GOV | Must also equal approved filename | H=yes | mismatch stops |
| `immutable_candidate_identity.selected_preview_row_opaque_id` | opaque string | GOV | Copy, then verify against ROW projection | H=yes | mismatch stops |
| `immutable_candidate_identity.selected_preview_row_safe_hash` | 64-hex string | GOV | Copy, then recompute from ROW safe projection | H=yes | mismatch stops |
| `immutable_candidate_identity.final_candidate_id` | opaque string | GOV | Copy, then verify against CHAIN | H=yes | mismatch stops |
| `immutable_candidate_identity.final_candidate_safe_hash` | 64-hex string | GOV | Copy, then recompute from safe final projection | H=yes | mismatch stops |
| `immutable_candidate_identity.final_candidate_schema` | exact string | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |
| `immutable_candidate_identity.identity_schema` | exact string | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |
| `immutable_candidate_identity.identity_version` | exact string `0.1` | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |
| `immutable_candidate_identity.hash_algorithm` | exact string `sha256` | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |
| `immutable_candidate_identity.hash_input_scope` | exact opaque string | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |
| `immutable_candidate_identity.candidate_lock_status` | exact opaque string | GOV | Copy exact committed value; require current CONST equality | H=yes | mismatch stops |

### 11.4 Candidate projection

Required fields:

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `candidate_projection.evidence_layer_write_candidate_schema` | exact opaque string | CONST | Exact item schema; require CHAIN equality | H=yes | mismatch stops |
| `candidate_projection.evidence_layer_write_candidate_id` | opaque string | CHAIN | Copy exact one-candidate value; require GOV final ID equality | H=yes | mismatch stops |
| `candidate_projection.source_production_evidence_import_candidate_id` | opaque string | CHAIN | Copy exact lineage reference | H=yes | missing/unsafe stops |
| `candidate_projection.source_evidence_layer_write_candidate_id` | opaque string | CHAIN | Copy exact lineage reference | H=yes | missing/unsafe stops |
| `candidate_projection.source_evidence_layer_import_candidate_id` | opaque string | CHAIN | Copy exact lineage reference | H=yes | missing/unsafe stops |
| `candidate_projection.source_review_queue_candidate_id` | opaque string | CHAIN | Copy exact lineage reference | H=yes | missing/unsafe stops |
| `candidate_projection.source_evidence_candidate_id` | opaque string | CHAIN | Copy exact lineage reference | H=yes | missing/unsafe stops |
| `candidate_projection.evidence_id_hash` | 64-hex string | DERIVED | Full SHA-256 from the selected ROW evidence/content/id precedence; first 16 hex must equal CHAIN evidence hash | H=yes | missing/prefix mismatch stops |
| `candidate_projection.text_snippet_redacted` | nonempty string, max 160 | DERIVED | Exact literal `[redacted selected source content]`; no row text retained | H=yes | altered/raw/sensitive text stops |

Allowed optional fields and the selected F03 profile:

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `candidate_projection.preview_hash` | 64-hex string | GOV | Include exact preview-row safe hash | H=yes | mismatch stops |
| `candidate_projection.case_id_hint` | opaque string | GOV | Include exact committed case hint | H=yes | mismatch stops |
| `candidate_projection.platform` | opaque string | ROW through CHAIN | Include only when nonempty and safe; otherwise omit | H=yes if present | unsafe value stops; absence omits |
| `candidate_projection.evidence_type` | opaque string | ROW through CHAIN | Include only when nonempty and safe | H=yes if present | unsafe value stops; absence omits |
| `candidate_projection.created_at_date` | `YYYY-MM-DD` | ROW through CHAIN | Map only a validated coarse date | H=yes if present | invalid date stops; absence omits |
| `candidate_projection.source_url_present` | boolean | ROW | Include presence boolean only; never copy URL | H=yes if present | non-boolean stops |
| `candidate_projection.acquisition_mode` | opaque string | current schema allowlist | Omit in F03 profile; no unique committed source | not present | presence stops under F03 profile |
| `candidate_projection.provenance_type` | opaque string | current schema allowlist | Omit in F03 profile; no unique committed source | not present | presence stops under F03 profile |
| `candidate_projection.verification_status` | opaque string | ROW through CHAIN | Include only when nonempty and safe | H=yes if present | unsafe value stops; absence omits |
| `candidate_projection.review_status` | opaque string | ROW through CHAIN | Include only when nonempty and safe | H=yes if present | unsafe value stops; absence omits |
| `candidate_projection.trust_label` | opaque string | ROW through CHAIN | Include only when nonempty and safe; no upgrade | H=yes if present | unsafe/high-trust substitution stops |
| `candidate_projection.redaction_status` | opaque string | DERIVED | Exact `redacted` | H=yes | mismatch stops |
| `candidate_projection.title_or_label_redacted` | nonempty string, max 160 | current schema allowlist | Omit in F03 profile to avoid content spread | not present | presence stops under F03 profile |
| `candidate_projection.redaction_warnings` | list, max 20 labels | DERIVED | Exact `source_content_fully_redacted` warning | H=yes | unknown/unsafe label stops |
| `candidate_projection.warning_labels` | list, max 20 labels | CONST | Exact manual-review and selected-sample labels | H=yes | missing manual-review label stops |
| `candidate_projection.blocker_codes` | list, max 20 labels | CHAIN | Copy safe candidate blocker labels, including empty list | H=yes | unsafe label stops |

No optional field outside this table is allowed. Conditional inclusion is one
deterministic rule, not a choice of capture methods.

### 11.5 Lineage projection

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `lineage_projection.source_production_evidence_import_candidate_id` | opaque string | CHAIN | Equal candidate projection field | H=yes | mismatch stops |
| `lineage_projection.source_evidence_layer_write_candidate_id` | opaque string | CHAIN | Equal candidate projection field | H=yes | mismatch stops |
| `lineage_projection.source_evidence_layer_import_candidate_id` | opaque string | CHAIN | Equal candidate projection field | H=yes | mismatch stops |
| `lineage_projection.source_review_queue_candidate_id` | opaque string | CHAIN | Equal candidate projection field | H=yes | mismatch stops |
| `lineage_projection.source_evidence_candidate_id` | opaque string | CHAIN | Equal candidate projection field | H=yes | mismatch stops |
| `lineage_projection.source_candidate_set_schema` | exact string | CONST | Exact candidate-set schema | H=yes | mismatch stops |
| `lineage_projection.source_candidate_schema` | exact string | CONST | Exact candidate item schema | H=yes | mismatch stops |

### 11.6 Boundary projection

| Field path | Type/bound | Sole origin | Capture rule | Hash | Failure rule |
| --- | --- | --- | --- | --- | --- |
| `boundary_projection.human_review_required` | boolean | CONST | `true` | H=yes | any other value stops |
| `boundary_projection.no_automatic_trust_upgrade` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.preview_only` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.import_candidate_only` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.production_import_candidate_only` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.write_candidate_only` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.evidence_layer_write_candidate_only` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.not_production_evidence_item` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.no_evidence_layer_write` | boolean | CONST | `true` | H=yes | weakening stops |
| `boundary_projection.warning_count` | integer | CONST | Exact `1`; booleans forbidden | H=yes | mismatch stops |
| `boundary_projection.warning_labels` | list, max 20 labels | CONST | Must include `manual_review_required` | H=yes | missing/unsafe label stops |

## 12. Source-to-payload Mapping

There is one origin hierarchy and no equal alternatives:

| Payload area | Authoritative origin | Replacement prohibited |
| --- | --- | --- |
| Schema names/versions and boundary flags | Current validator constants at `e3fb9f9` | Source row, caller input, historical schema |
| Immutable identity and package/row lock | 9A-16C committed identity record at `11ae4bb` | Source row, package resolver, guessed package name |
| Preview ID/hash and final candidate ID/hash/schema | 9A-16C record, independently recomputed from the one selected row and safe chain | Similar row, alternate hash, earlier preview guess |
| Required lineage IDs | Exactly-one current candidate chain generated in memory | Caller-supplied IDs, stale report copy |
| Full evidence ID hash | SHA-256 of the selected row's one evidence/content/id source value with the existing precedence; 16-hex prefix must match CHAIN | Raw ID persistence, alternate ID, arbitrary digest |
| Redacted snippet and redaction warnings | Fixed F03 privacy transformation | Raw title/body/comment or helper excerpt |
| Safe optional metadata | One selected row through the committed safe chain | Governance value substitution or unrelated row |
| `input_safe_hash` | Canonical payload projection excluding that field | Stored claim, caller-supplied hash |

Governance fields always win over row fields. Row-derived fields cannot replace
identity, package, schema, or boundary values. A safe optional field with no
valid deterministic row-derived value is omitted, never guessed.

## 13. Forbidden Content Catalog

The payload, receipt, output names, logs, and errors must reject or omit:

- raw package rows or full serialized source objects;
- full raw title, body, comment, reply, or private text;
- raw author IDs/names, handles, avatars, account links, or profile data;
- email, phone, address, device identifier, or real-person identifying data;
- private messages or nonpublic content;
- cookies, sessions, tokens, keys, passwords, credentials, salts, or environment values;
- local username, drive path, absolute path, package path, or SQLite path;
- source URL or any unredacted URL;
- unrelated rows, candidates, package metadata, or lineage;
- executable code, binary data, provider/collector internals, or hidden values;
- targeting, persuasion, truth, official-verification, prediction, psychological,
  personality, generated-response, or public-message fields;
- production approval markers, production objects, trust upgrades, or downstream
  execution flags.

The scan is recursive over dictionary keys, list items, and string values before
either final artifact is committed.

## 14. Canonicalization and Hash Contract

- hash_algorithm = sha256
- hash_input_scope = versioned_safe_canonical_projection_only
- JSON encoding = UTF-8
- key ordering = lexicographically sorted
- separators = comma and colon without extra spaces
- Unicode handling = `ensure_ascii = true`
- booleans = JSON `true`/`false`
- null policy = optional candidate fields are omitted rather than stored as null
- numeric policy = no floating-point values; only exact integer warning count 1
- timestamp policy = no capture timestamp participates in the payload hash
- excluded field = `input_safe_hash` only

Procedure:

1. Assemble the complete payload without `input_safe_hash`.
2. Serialize with `json.dumps(..., ensure_ascii=True, sort_keys=True,
   separators=(",", ":"))`.
3. Encode as UTF-8 and calculate SHA-256 lowercase hexadecimal.
4. Add that digest as `input_safe_hash`.
5. Call `validate_exact_locked_candidate_safe_write_payload` with the separately
   loaded immutable identity.
6. Require the validator to return an equal deep copy.

The selected preview-row safe hash and final candidate safe hash use the
committed 9A-16C safe-projection algorithms. F02 calculates none of these real
hashes now.

## 15. Output Location Class

- logical_output_directory_label = runtime/protected_safe_payload_captures/mvp_f03_v1/
- payload_filename_pattern = safe-payload-{final_candidate_safe_hash}.json
- receipt_filename_pattern = capture-receipt-{final_candidate_safe_hash}.json
- artifact_schema = sentigraph_exact_locked_candidate_safe_write_payload_v0_1
- artifact_version = 0.1
- receipt_schema = sentigraph_mvp_f03_real_safe_payload_capture_receipt_v1_0
- receipt_version = 1.0
- local_only = yes
- git_tracked = no
- output_location_git_ignored = yes
- production_target = no
- persistence_target = no
- publicly_accessible = no
- automatic_backup_assumed = no

The committed `.gitignore` rule `runtime/` covers this logical class. The class
is separate from the logical SQLite target, generic case storage, provider
packages, frontend assets, and Project Source. F02 does not create, stat, or list
the directory.

F03 must use full safe hashes in names, exclusive creation, and no overwrite.
Raw titles, identities, source URLs, package paths, or local usernames are
forbidden in filenames. Successful capture leaves exactly one payload and one
receipt, with no copy elsewhere.

## 16. Capture Receipt Schema

- receipt_schema = sentigraph_mvp_f03_real_safe_payload_capture_receipt_v1_0
- receipt_version = 1.0
- receipt_classification = safe_local_nonproduction_metadata_only

Required safe fields:

| Field | Type/truth rule |
| --- | --- |
| `receipt_schema`, `receipt_version`, `milestone_id` | Exact constants |
| `capture_session_id` | Opaque ID derived from the committed final candidate safe hash; no path/value content |
| `capture_started_at`, `capture_completed_at` | UTC timestamps; receipt only, excluded from payload identity |
| `source_access_session_consumed` | True iff source open succeeded |
| `source_file_open_count` | 0 before open failure, otherwise exactly 1 |
| `source_file_reopen_count` | Always 0 |
| `source_file_open_mode` | Exact `binary_read_only` |
| `source_line_utf8_byte_limit` | Exact integer 1048576 |
| `source_line_probe_read_size` | Exact integer 1048577 |
| `source_read_call_count` | 0 before source open, otherwise exactly 1 |
| `source_line_bytes_read` | Integer from 0 through 1048577 |
| `source_line_terminator_counted_in_limit` | Always true |
| `oversized_source_line_detected` | True only when `source_line_bytes_read > 1048576` |
| `UTF8_decode_attempted` | False for empty or oversized input; otherwise true |
| `UTF8_decode_passed` | True only after strict UTF-8 decoding succeeds |
| `JSON_parse_attempted` | True only after size and UTF-8 checks pass |
| `duplicate_JSON_key_detected` | True only for duplicate-key rejection at any object depth |
| `nonstandard_numeric_constant_detected` | True only for `NaN`, `Infinity`, or `-Infinity` rejection |
| `strict_JSON_parse_passed` | True only for valid syntax with no duplicate key and no non-standard numeric constant |
| `top_level_JSON_object_verified` | True only when the parsed top level is an object |
| `directory_enumeration_performed` | Always false |
| `alternate_source_used` | Always false |
| `approved_package_binding_verified` | True only after committed lock comparison |
| `approved_row_source_verified` | True only for the exact approved filename |
| `row_selector_verified` | True only for physical row index 1 and matching opaque ID |
| `row_hash_verified` | True only after recomputing the committed safe preview hash |
| `candidate_binding_verified` | True only after final ID/hash/schema equality |
| `rows_examined_or_parsed` | 0 or 1 only |
| `rows_selected` | 0 or 1 only |
| `payload_artifact_count`, `receipt_artifact_count` | Each 1 only on complete success |
| `payload_schema`, `payload_version`, `payload_safe_hash` | Exact validated payload metadata; hash only |
| `forbidden_field_scan_passed`, `protected_value_scan_passed` | True only after recursive scan |
| `raw_row_retained`, `raw_author_identity_retained`, `absolute_path_recorded` | Always false |
| `production_object_created`, `database_accessed`, `network_called` | Always false |
| `gate_activated`, `persistence_mutation_performed` | Always false |
| `final_outcome` | One bounded outcome below |
| `pause_reason` | Safe enumerated reason or null on success; no unsafe exception text |

Truthful outcomes:

| Condition | `final_outcome` | Output rule |
| --- | --- | --- |
| One exact row, all bindings/scans/validation pass, both final artifacts committed | `captured_one_safe_payload_for_independent_audit` | Counts 1/1; source consumed |
| EOF/blank first line | `paused_zero_matching_row` | No payload; no alternate source |
| First raw physical line exceeds 1048576 bytes | `paused_source_line_exceeds_bound` | Bytes read 1048577; no decode, parse, payload, second read, or retry; fresh governance required |
| Strict UTF-8 decoding fails | `paused_source_line_invalid_utf8` | Decode attempted and failed; JSON not attempted; no raw bytes, exception, payload, or retry |
| Malformed standard JSON | `paused_strict_JSON_parse_failure` | Parse attempted and failed; no payload, raw value echo, second read, or retry |
| Duplicate JSON key at any object depth | `paused_duplicate_JSON_key_detected` | Duplicate flag true; no key text, payload, second read, or retry |
| `NaN`, `Infinity`, or `-Infinity` | `paused_nonstandard_numeric_constant_detected` | Constant flag true; no token text, payload, second read, or retry |
| Parsed top level is not an object | `paused_source_row_not_object` | Object verification false; no payload, second read, or retry |
| Any stage returns more than one item | `paused_multiple_candidate_matches` | No payload; no manual choice |
| Identity/hash/schema mismatch | `paused_binding_mismatch` | No payload; fresh governance required |
| Forbidden field/value | `privacy_issue_stop` | No payload; no value echoed |
| Safe projection or transformation failure after strict parse | `paused_projection_failure` | Source consumed; no payload, reopen, or retry |
| Output write failure | `paused_output_write_failure` | No source reopen; partial handling per section 19 |
| Final artifact state cannot be proven | `paused_ambiguous_output_state` | No retry or overwrite |

Every failure after source open records the session as consumed and permits no
fallback, reopen, second read, or retry. The receipt contains no raw bytes, raw
decoded text, duplicate key names, non-standard numeric tokens, parser exception
messages, physical path, raw row, raw identity, URL, credential, authorization
text, or exception dump.

## 17. Privacy and Protected-value Checks

F03 must perform two scans:

1. Before payload construction, reject active forbidden keys and sensitive
   patterns in every value selected from the row or chain.
2. Immediately before final output, recursively scan the complete payload and
   receipt for forbidden keys, URLs, path forms, emails, phone patterns, secret
   patterns, raw identity markers, and production/downstream flags.

The raw source bytes, normalized bytes, decoded line, and parsed object exist in
memory only for the bounded session. They are not logged, printed, returned,
placed in the receipt, or retained. Parser errors are converted to safe
enumerated outcomes before receipt construction. The payload's required snippet
is a fixed full-redaction marker, not source text.

Any protected-value detection sets `privacy_issue_stop`, writes no payload, and
does not permit another source open.

## 18. Custody and Access Control

- F03 initiator = explicit human approval only
- capture executor = local Codex execution under the separately approved F03 task
- artifact classification = protected local nonproduction governance artifact
- allowed readers before F04 = F03 executor and separately approved F04 audit only
- modification after creation = forbidden
- silent overwrite = forbidden
- duplicate copy = forbidden
- upload, share, sync, publication = forbidden
- inclusion in Project Source or chat = forbidden
- Git add or commit = forbidden
- provider/collector return path = forbidden

The receipt exposes safe metadata only. Access outside this list requires a new
governance decision and cannot be inferred from F02.

## 19. Retention and Cleanup

- source package remains untouched;
- successful payload and receipt remain byte-for-byte unchanged through F04;
- no automatic deletion, overwrite, repair-in-place, backup, replica, or copy;
- a successful payload is not deleted before F04;
- final cleanup after F04 is not authorized by F02;
- cleanup may never delete or modify the source package or unrelated runtime state.

F03 may delete only a conclusively identified temporary file created by that
same F03 process, only if the later F03 approval explicitly includes this bounded
cleanup rule and no final artifact exists. An ambiguous final output is preserved
for a separately approved inspection; it is not overwritten or retried.

## 20. Error and Stop Conditions

The workflow disposition is `pause` on any of the following:

- missing/incomplete/changed authoritative identity record;
- package, role, case, row-source, preview, candidate, schema, or hash mismatch;
- missing source file at the exact locked object;
- source open count would exceed one or reopening appears necessary;
- a source read other than the one bounded binary `readline(1048577)` appears necessary;
- the first physical line is empty, JSON-whitespace-only, or exceeds 1048576 bytes;
- strict UTF-8 decoding fails or any replacement/BOM/encoding fallback appears necessary;
- strict JSON syntax fails, a duplicate key appears at any object depth,
  `NaN`/`Infinity`/`-Infinity` appears, or the top level is not an object;
- a blocked or unexpected first record is produced after strict parsing;
- a second physical line, broad scan, glob, or directory enumeration appears necessary;
- zero or more than one candidate at any stage;
- unknown/missing payload field or invalid field type/bound;
- invalid canonicalization or payload hash;
- forbidden key/value, raw identity, private content, URL, or path exposure;
- output class is not proven ignored or an artifact already exists;
- output state is ambiguous or an alternate source seems necessary;
- any database, runtime target, provider, collector, network, gate, persistence,
  production object, or downstream action appears necessary.

There is no automatic retry, fallback, manual substitution, line-bound increase,
parser repair, or best-effort payload. A failed source-open session is consumed.

## 21. No-substitution and No-fallback Rules

The following are invariant:

- one committed package identity;
- one approved row-source label;
- one tracked source-file object;
- physical row index 1 only;
- one binary `readline(1048577)` call under a 1048576-byte line cap;
- strict UTF-8 and strict, duplicate-free, standard-numeric JSON parsing;
- one preview identity and one final candidate identity;
- current exact payload, identity, set, and item schemas;
- current SHA-256 and canonical JSON rules;
- one output directory class and two exact filename patterns.

Caller-supplied path, package, row index, candidate, schema, hash, title, or
fallback is forbidden. Missing data stops. A similar-looking row is not a match.

## 22. F04 Independent-audit Handoff

F04 receives only:

- the protected safe-payload artifact;
- the safe capture receipt;
- tracked references to this contract, the 9A-16C identity record, 9A-22, 9A-23B,
  and MVP-F01;
- safe schema/version names and hashes.

F04 must not reopen the source, package, or row; enumerate directories; access a
database or logical persistence target; use network; activate a gate; or mutate
anything.

F04 independently verifies:

- exact payload schema and strict field set;
- canonical `input_safe_hash` from the artifact only;
- immutable identity and lineage equality to committed governance;
- preview/final safe hash and candidate binding consistency;
- warning, review, no-trust-upgrade, and no-production boundaries;
- forbidden/protected-value absence;
- one candidate, one payload, one receipt;
- receipt byte-bound, decode, strict-parser, arithmetic, and
  no-substitution/no-reopen claims;
- no production or downstream side effects.

F04 acceptance is required before any target or persistence decision. F02 and
F03 self-validation cannot substitute for it.

## 23. Preserved Production No-go Boundaries

This contract does not authorize or create:

- a production EvidenceItem, Review Queue item, case, analysis run, or Analysis Result;
- Source 11 or FinalSummaryReport runtime;
- B-end report, Sandbox/public event, export, download, public access, or delivery;
- provider/collector jobs, private collector inspection, API/LLM/network use, URL fetch, or scraping;
- runtime target initialization, SQLite access, gate activation, persistence, or actual write;
- automatic trust upgrade, official verification, causal proof, prediction, or public/customer readiness.

Provider or collector output remains evidence, not truth. Human review remains
required.

## 24. No-side-effect Statement

MVP-F02 inspected only Git-tracked repository evidence. It did not open, stat,
hash, enumerate, parse, copy, or move a real package or source row. It did not
inspect or measure the real source-line length, inspect runtime or exchange
directories, calculate a real payload/candidate hash, create an output directory
or artifact, access SQLite, activate a gate, execute persistence, or create a
production object. Exactly this contract and its companion decision are the
intended file changes.
