# Sentigraph MVP-B05-CIB-P1 Safe Three-variable Server-owned Configuration Identity Binding Contract v1.0

## 1. Decision and scope

| State | Value |
| --- | --- |
| Decision | `ready` |
| `privacy_issue_stop` | `no` |
| `docs_only` | `yes` |
| `read_only_committed_repository_audit` | `yes` |
| `environment_values_accessed` | `no` |
| `environment_values_recorded` | `no` |
| `environment_values_hashed` | `no` |
| `salt_generated` | `no` |
| `configuration_canonical_object_created` | `no` |
| `configuration_binding_SHA256_created` | `no` |
| `safe_receipt_created` | `no` |
| Artifact/package/runtime-directory access | `0/0/0` |
| Application imports | `0` |
| Endpoint calls | `0` |
| Product changes | `none` |

This docs-only contract defines a future, separately approved safe identity binding for exactly three existing server-owned process-environment variables. CIB-P1 reads committed repository evidence only. It does not capture a configuration value, generate a salt, build the canonical configuration object, compute a configuration-derived digest, create a safe receipt, inspect an artifact or authorize runtime use.

## 2. Approval, Goal and accounting

- Exact approval SHA-256: `08c92be5a9f244a46ac6677408320f5dbf3ccb39a318dd0c690000f925e9b1e6`.
- Goal requested: `MVP-B05-CIB-P1 Safe Three-variable Server-owned Configuration Identity Binding Contract`.
- Goal activation verified: `yes`.
- Goal completion: `pending_ready_only_terminal_receipt` until the containing commit, push, `0/0` alignment, clean worktree and Goal completion are verified.
- Starting commit and P4-RC1 commit: `06b843d6e6ec39cd982bf8b5f1344e58ade45f77`.
- Initial P4 implementation commit: `0ee548deb8cb6fafbf44f8a5a6e5c52ec76cae56`.
- Prompt classification: `conditional`.
- Baseline v1.7 before activation, consumed engineering/fixed/conditional/risk: `3/2/1/0`.
- Baseline v1.7 before activation, remaining fixed/conditional/risk: `0/3/2`.
- Baseline v1.7 after activation and final CIB-P1 accounting, consumed engineering/fixed/conditional/risk: `4/2/2/0`.
- Baseline v1.7 after activation and final CIB-P1 accounting, remaining fixed/conditional/risk: `0/2/2`.
- `MVP_B05_CIB_P1_status = candidate_completed_pending_independent_ChatGPT_acceptance`.
- `MVP_B05_CIB_P1_approval_reusable = no`.
- `MVP_B05_CIB_P1_Goal_reusable = no`.

All committed-evidence inspection, contract authoring, static validation, ordinary commit and push belong to this one conditional Prompt. This contract does not claim independent CIB-P1 acceptance.

The following accepted state is preserved without reclassification:

| Milestone | Preserved state |
| --- | --- |
| Baseline v1.7 | `effective` |
| MVP-B01 through MVP-B04 | `completed_and_independently_accepted` |
| MVP-B05-P1 | `completed_and_independently_accepted` |
| Effective MVP-B05-P2 | `completed_and_independently_accepted_via_RC1` |
| MVP-B05-P3 | `completed_and_independently_accepted` |
| Effective MVP-B05-P4 | `completed_and_independently_accepted_via_RC1` |
| Initial P4 review | `needs_fix_directly_coupled_suite_order_dependent_lazy_import_test` |
| Historical P4 needs-fix reclassified | `no` |

The initial P4 implementation and P4-RC1 test-only forward repair remain distinct history.

## 3. Preserved product identity

The future binding scope is frozen to this product identity:

| Element | Exact value |
| --- | --- |
| Service blob | `9818622c3000092e4f9ee84b4a86300bb415d074` |
| Registry schema | `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1` |
| Sample handle | `helldivers2-psn-demo` |
| Result basename | `provider_result_helldivers2-psn-demo_20260614_055754.json` |
| Route mode | `internal_alpha_read_only_local_exchange_projection_operator` |
| Capability label | `b05_local_exchange_projection_read_only` |
| Default registry entries | `1` |
| Entry enabled | `true` |

Mapping presence and `enabled = true` do not authorize runtime use. The real mapping remains implemented and present, all five gates remain disabled by default, runtime smoke remains unperformed, and the current complete three-variable configuration identity binding remains `unavailable_from_current_committed_safe_evidence`.

## 4. Exact configuration-variable order

The only permitted variable names, in immutable order, are:

1. `SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR`
2. `SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT`
3. `SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID`

Variable aliases, alternate names, lowercase variants, file sources, dotenv sources, shell dumps, client values and fallback configuration are forbidden. No client or caller may select, reorder or override the three names.

## 5. Future value-validation contract

This section applies only to a future separately approved CIB-P2.

The results-directory value and collector-export-root value must each:

- be an actual string;
- be used exactly and without modification;
- contain from 1 through 2048 characters inclusive;
- satisfy `value == value.strip()`;
- be printable;
- contain no NUL character.

Validation may compare a value with its stripped representation, but it must never replace the original with a trimmed result.

The adapter ID must be an actual string that exactly matches:

```text
^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$
```

The match applies to the original value in full. No case normalization, trimming, encoding fallback, repair or replacement is permitted.

CIB-P2 must treat all three values as opaque strings, never as paths. It must perform no path construction, normalization, resolution, existence check, file-type check, parent or child check, directory listing, glob, walk, search, filesystem opening, package lookup or artifact lookup.

## 6. Exact binding schema

| Element | Exact value |
| --- | --- |
| Binding schema | `sentigraph_b05_server_owned_configuration_identity_binding_v0_1` |
| Version | `0.1` |
| Binding scope | `b05_one_real_sample_handle_governed_read_only_projection_pre_smoke` |
| Canonicalization label | `sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1` |

The version is the exact string `0.1`. These identifiers are immutable for this contract version.

## 7. Exact canonical object

The future CIB-P2 canonical object exists in memory only and contains exactly 11 top-level fields in this insertion order:

1. `schema`
2. `version`
3. `binding_scope`
4. `service_blob`
5. `registry_schema`
6. `sample_handle`
7. `result_file_name`
8. `route_mode`
9. `capability_label`
10. `salt_hex`
11. `configuration_values`

`configuration_values` is an ordered list of exactly three objects in the frozen variable order. Each item contains exactly two fields in this order:

1. `name`
2. `value`

Each in-memory `value` is the exact validated value read directly from the runner process environment. Values must never be written to disk, stdout, stderr, logs, reports, Git, tracebacks or safe receipts.

Serialization is exactly equivalent to:

```python
json.dumps(
    canonical_object,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=False,
).encode("utf-8")
```

Canonicalization uses explicit insertion order only, UTF-8 only, no BOM, no terminal newline, no Unicode normalization, no encoding fallback, no sorting, no whitespace insertion and no value transformation.

## 8. Salt and binding digest

A successful future CIB-P2 generates exactly one salt using:

```python
secrets.token_bytes(32)
```

Calling `bytes.hex()` on that salt produces exactly one 64-character lowercase hexadecimal `salt_hex`. The single configuration-derived binding digest is:

```python
hashlib.sha256(canonical_bytes).hexdigest()
```

Successful-capture counters are frozen as follows:

| Counter | Exact value |
| --- | --- |
| Process-environment source count | `1` |
| Exact variable names | `3` |
| Direct value reads | `3` |
| Reads per exact variable | `1` |
| Reopens | `0` |
| Second reads | `0` |
| Salt generations | `1` |
| Configuration canonical objects | `1` |
| Configuration-derived SHA-256 computations | `1` |
| Per-variable hashes | `0` |

The exactly-one SHA-256 limit applies to the single configuration-derived canonical-object digest. The repository-external runner-safety protocol is reconciled as follows:

- one pre-protected integrity hash of the generic runner file is permitted and contains no configuration value;
- the runner-integrity digest is separate from the configuration-derived binding digest;
- no safe-receipt SHA-256 is computed during capture;
- no individual value, name/value pair or partial canonical object is hashed;
- the configuration canonical bytes are hashed exactly once.

This contract does not claim memory zeroization. Raw values and canonical bytes are process-local, are never serialized to an output artifact, and cease to be retained when the runner process terminates.

## 9. Exact safe-receipt schema

The receipt schema is `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1`.

A successful receipt contains exactly 23 fields in this order:

1. `schema`
2. `version`
3. `binding_scope`
4. `service_blob`
5. `registry_schema`
6. `sample_handle`
7. `result_file_name`
8. `route_mode`
9. `capability_label`
10. `variable_names`
11. `salt_hex`
12. `combined_binding_sha256`
13. `canonicalization_label`
14. `configuration_source`
15. `environment_read_count`
16. `binding_status`
17. `raw_values_exposed`
18. `per_variable_hashes_created`
19. `path_operations_performed`
20. `application_imported`
21. `artifact_accessed`
22. `endpoint_called`
23. `runtime_authorized`

Successful receipt constants are frozen as follows:

| Field | Exact value |
| --- | --- |
| `schema` | `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1` |
| `version` | exact string `0.1` |
| `binding_scope` | `b05_one_real_sample_handle_governed_read_only_projection_pre_smoke` |
| `service_blob` | `9818622c3000092e4f9ee84b4a86300bb415d074` |
| `registry_schema` | `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1` |
| `sample_handle` | `helldivers2-psn-demo` |
| `result_file_name` | `provider_result_helldivers2-psn-demo_20260614_055754.json` |
| `route_mode` | `internal_alpha_read_only_local_exchange_projection_operator` |
| `capability_label` | `b05_local_exchange_projection_read_only` |
| `variable_names` | exact three names in the frozen order |
| `canonicalization_label` | `sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1` |
| `configuration_source` | `process_environment_exact_names_only` |
| `environment_read_count` | `3` |
| `binding_status` | `configuration_identity_bound` |
| `raw_values_exposed` | `false` |
| `per_variable_hashes_created` | `false` |
| `path_operations_performed` | `false` |
| `application_imported` | `false` |
| `artifact_accessed` | `false` |
| `endpoint_called` | `false` |
| `runtime_authorized` | `false` |

`salt_hex` and `combined_binding_sha256` are each exactly 64 lowercase hexadecimal characters and contain only the future successful capture's one salt representation and one combined digest. The receipt contains no configuration value, value fragment, value length, path length, per-variable hash, path status, normalized path, filesystem identity, environment dump, credential, raw exception, traceback or arbitrary extension field.

The salt and combined digest are internal governance equality-binding evidence. They are not encryption, secret storage, proof of path safety, proof of artifact existence or proof of runtime readiness. A public salt does not prevent targeted offline guessing of low-entropy configuration values. The binding is an equality fingerprint, not a confidentiality guarantee.

## 10. Fail-closed behavior

A future CIB-P2 must stop without a successful safe receipt when any required value is missing, non-string, blank, leading- or trailing-whitespace-bearing, longer than its exact bound, nonprintable, NUL-containing or invalid under the adapter-ID regular expression where applicable.

On any such failure:

- environment reads already performed remain counted;
- salt generations are `0`;
- configuration-derived SHA-256 computations are `0`;
- successful safe receipts are `0`;
- automatic retries are `0`;
- second reads are `0`.

No raw exception, raw value, value fragment, value length, path, traceback or environment dump may be emitted. A future Codex terminal receipt may contain only a bounded constant failure classification from the closed validation categories; it must never include the failed value.

## 11. No-substitution contract

The only future source is the current CIB-P2 runner process environment. Each frozen exact name is read directly once.

The following are forbidden sources or substitutions:

- `.env` or any environment file;
- configuration files;
- subprocess shell dumps;
- text pasted or supplied by a client;
- alternate or fallback variable names;
- command-line values;
- query, body, header or frontend input;
- registry-entry configuration fields;
- values reconstructed from committed documents;
- guessed values;
- values derived from a path;
- values copied from any previous run.

No client or caller may select or override the names or their order, and no unavailable value may be replaced.

## 12. Future CIB-P2 candidate

Define, but do not select or authorize:

- `MVP-B05-CIB-P2 = One Safe Three-variable Server-owned Configuration Identity Capture`.
- Candidate classification: `conditional`.
- `MVP_B05_CIB_P2_candidate_defined = yes`.
- `MVP_B05_CIB_P2_selected = no`.
- `MVP_B05_CIB_P2_authorized = no`.
- `MVP_B05_CIB_P2_Goal_authorized = no`.
- `MVP_B05_CIB_P2_executed = no`.

The future candidate repository allowlist contains exactly one file:

`docs/health/sentigraph_mvp_b05_cib_p2_safe_three_variable_server_owned_configuration_identity_capture_report_v1_0.md`

The only repository-external temporary objects are one UTF-8 standard-library-only runner and one bounded successful safe-receipt JSON artifact. Neither object is committed.

Future CIB-P2 success limits are:

| Counter | Exact value |
| --- | --- |
| Runner executions | `1` |
| Fresh runner processes | `1` |
| Automatic retries | `0` |
| Environment-source sessions | `1` |
| Direct variable reads | `3` |
| Reads per variable | `1` |
| Salt generations | `1` |
| Configuration-binding SHA-256 computations | `1` |
| Safe-receipt creations | `1` |
| Safe-receipt readbacks | `1` |
| Safe-receipt reopens | `0` |
| Application imports | `0` |
| Artifact/package accesses | `0/0` |
| Endpoint calls | `0` |
| Database/persistence actions | `0/0` |
| Product changes | `0` |

The future committed health report may contain the exact safe-receipt fields, the generic runner integrity digest, the accepted CIB-P1 contract identity, counters and validation outcomes. It must contain no raw configuration value. The runner and safe receipt must be deleted after conclusive validation.

CIB-P2 requires independent CIB-P1 acceptance, later route selection, fresh exact approval and a fresh Goal.

## 13. Future P5 recomputation gate

CIB-P1 acceptance alone does not make P5 eligible. After an independently accepted CIB-P2, a future separately approved P5 must perform these steps in order before any artifact access or B05 GET:

1. Verify the exact accepted CIB-P1 contract identity.
2. Verify the accepted CIB-P2 report and binding state.
3. Verify the exact service blob, registry schema and one-entry mapping.
4. Use the accepted CIB-P2 `salt_hex` without generating a new salt.
5. Read the same three process-environment values exactly once each.
6. Apply the same validation and canonicalization contract.
7. Compute exactly one configuration-derived SHA-256.
8. Require an exact match with the accepted `combined_binding_sha256`.

A mismatch or unavailable value requires stop before artifact access, stop before application import when safely detected during preflight, no B05 GET, no alternate configuration, no retry, no second environment read and no binding replacement.

Even after an exact match, P5 requires its own route selection, fresh exact risk approval and fresh Goal. Its protected limits remain:

| Protected action | Exact limit |
| --- | --- |
| Fresh artifact identity verification | `1` |
| Direct artifact opens/reads/reopens | `1/1/0` |
| Direct artifact SHA-256 computations | `1` |
| B05 GET attempts/completed maximum | `1/1` |
| Automatic retries/second GETs | `0/0` |
| B01 calls/B03 calls | `1/1` |
| Persistence | `0` |
| Production/public-export-delivery | `0/0` |

Current P5 state is frozen as:

- `MVP_B05_P5_candidate_defined = yes`.
- `MVP_B05_P5_selected = no`.
- `MVP_B05_P5_eligible = no`.
- `MVP_B05_P5_authorized = no`.
- `MVP_B05_P5_Goal_authorized = no`.
- `MVP_B05_P5_executed = no`.

## 14. Privacy and security interpretation

CIB-P1 captures no raw value. A future CIB-P2 output is a combined equality binding only and must never be described as encrypted configuration. The salt is non-secret and may be recorded. The binding does not validate path existence, permissions, ownership, accessibility, filesystem identity or artifact location, and it does not prove configuration correctness beyond exact equality under this schema.

P5 must independently enforce every artifact-identity, gate, schema, call-count, fail-closed and no-side-effect control even when configuration recomputation matches. Neither CIB-P1 nor a future CIB-P2 creates runtime authority.

## 15. Exact authorization state

At CIB-P1 document completion:

| State | Value |
| --- | --- |
| CIB-P1 contract created | `yes` |
| Environment values accessed | `no` |
| Salt generated | `no` |
| Combined binding captured | `no` |
| Configuration identity binding available | `no` |
| CIB-P2 defined | `yes` |
| CIB-P2 selected | `no` |
| CIB-P2 authorized | `no` |
| CIB-P2 executed | `no` |
| P5 selected | `no` |
| P5 eligible | `no` |
| P5 authorized | `no` |
| P5 executed | `no` |
| Runtime authority created | `no` |

The exact CIB-P1 changed-file allowlist is this contract alone:

`docs/architecture/sentigraph_mvp_b05_cib_p1_safe_three_variable_server_owned_configuration_identity_binding_contract_v1_0.md`

Ready-only Git finalization is permitted only after one-file, UTF-8, Markdown, schema-order, field-count, forbidden-content, service-blob and diff validations pass with zero environment-value access, zero salt generation and zero configuration-derived SHA-256 computations. The only commit message is:

```text
Define B05 safe configuration identity binding contract
```

The only authorized push is an ordinary non-force push of current `main` to `origin/main`. No amend, reset, force push, tag, release, Project Source change, CIB-P2 execution, salt generation, binding capture or P5 action is authorized.

The next boundary is independent ChatGPT acceptance. Do not read environment values, generate a salt or configuration binding, begin CIB-P2, access or hash the artifact, import the application, call the B05 endpoint, begin B05-P5, or perform persistence, production, public, export or delivery work.
