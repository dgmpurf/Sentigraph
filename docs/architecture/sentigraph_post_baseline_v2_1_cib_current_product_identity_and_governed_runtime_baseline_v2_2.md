# Sentigraph Post-Baseline-v2.1 Current-product CIB Identity and Governed Runtime Baseline v2.2

## 1. Title and authority posture

This document is a docs-only governance establishment for a current-product Configuration Identity Binding (CIB) overlay and governed runtime Baseline v2.2. It does not capture a CIB, generate a salt, read configuration values, access protected resources, import the application, or authorize runtime work.

The document becomes an effective Baseline v2.2 authority only after all three events occur:

1. this document is committed;
2. the commit is pushed to `origin/main`;
3. the result is independently accepted by ChatGPT.

Before independent acceptance, its status is:

```text
candidate_completed_pending_independent_ChatGPT_acceptance
```

Planning capacity recorded here is not runtime authority. Every protected action remains subject to a separate exact approval and fresh Goal.

## 2. Immutable anchors

```text
milestone = SENTIGRAPH-BASELINE-V2-2-DOCS-ONLY-CIB-CURRENT-PRODUCT-IDENTITY-REBASELINE
starting repository HEAD = 8e0e58b2b14320d709ed6b7b46a2a9f7f8a476f5
starting HEAD message = Establish post-RP2 Baseline v2.1
compact approval SHA-256 = 3a507f6c6a655659d8fdc10eb286dab54762814efe71a2e98a4307f87b3fad75
Rebaseline Contract V1 SHA-256 = ad04e52c0217a4a90b081ccf07219d26e874ec63bbe48389b47167b378efb059
current Source-maintenance approval SHA-256 = 54dcfc6fec39b8205a2a1ba332f5e6d43c9f72f074a4f681d63df55bf36d196e
historical CIB-P1 contract blob = 939190f8794468b0485051e9ab6801a484129cb8
current B05 service blob = f0c4a8768060a840ea1921aeba47a97f2e41f9e3
Baseline v2.1 document SHA-256 = f99e24a1d4781373c98fb7273447c568b61b47faf3214425e58142149e5dcbb1
Baseline v2.1 document bytes = 10079
```

The raw approval phrase is intentionally excluded. These safe hashes identify governance inputs but grant no runtime authority.

## 3. Baseline v2.1 closure

Baseline v2.1 closes at the accepted later handoff state:

```text
final engineering / fixed / conditional / risk = 3 / 1 / 1 / 1
remaining fixed / conditional / risk = 0 / 0 / 2
```

The two unused Risk reservations become historical unused capacity only. They are not transferred, reset, reused, merged, carried forward, erased, or reclassified as Baseline v2.2 capacity.

The committed Baseline v2.1 establishment document remains authoritative establishment history. Its original starting accounting is preserved as history, while the accepted later handoff above controls final v2.1 closure accounting.

## 4. Distinct preserved v2.1 history

The following outcomes remain distinct and are preserved without reclassification.

### 4.1 Fixed Prompt 1

```text
Decision = blocked
runtime classification = blocked_artifact_or_hkcu_validation
historical result reclassified = no
```

Directly established:

- public sentinel transport worked;
- one formal protected execution received complete input;
- three artifact identities matched;
- strict JSON integrity passed;
- HKCU access remained zero.

Direct failure:

- the controller chose the wrong Provider Result contract layer;
- execution stopped before HKCU.

### 4.2 Risk Prompt 3

```text
Decision = ready
runtime classification = ready_hkcu_configuration_persisted_and_broadcast_restart_required
```

Directly established:

- the raw `v1` / `1.0` Provider Result contract passed;
- deterministic in-memory `v0.1` / `0.1` adapter output passed;
- package, adapter, and privacy checks passed;
- all three HKCU values were initially missing;
- each exact name was written once as `REG_SZ`;
- all three readbacks were exact;
- the single environment broadcast succeeded;
- persistent configuration was established.

### 4.3 Conditional Prompt 1

```text
Decision = ready
runtime classification = ready_post_restart_inherited_environment_all_three_present_contract_valid
```

Directly established:

- full Codex application exit and restart were user-confirmed;
- a new top-level Sentigraph task was used;
- the diagnostic child read each approved variable exactly once;
- all three entries were present and contract-valid;
- no other-name lookup, enumeration, or environment mutation occurred.

Conditional Prompt 1 did not reread HKCU and did not compare inherited values with protected artifacts. It established only the bounded inherited-process result from that diagnostic execution context.

## 5. Historical CIB-P1 contract status

The committed historical CIB-P1 contract at blob `939190f8794468b0485051e9ab6801a484129cb8` remains a valid historical contract for its frozen historical product identity.

Its historical product constants were:

| Element | Historical value |
| --- | --- |
| `service_blob` | `9818622c3000092e4f9ee84b4a86300bb415d074` |
| `result_file_name` | `provider_result_helldivers2-psn-demo_20260614_055754.json` |

That historical contract is not current-product CIB authority. It must not be substituted for, silently reinterpreted as, or used to bypass the current-product overlay defined below.

The historical contract's preserved product-independent semantics are:

- exactly three immutable variable names in a fixed order;
- exact bounded value-validation rules;
- fixed binding and receipt schemas and versions;
- fixed binding scope and canonicalization label;
- an 11-field insertion-ordered canonical object;
- three ordered `name` / `value` objects;
- compact insertion-order UTF-8 serialization;
- exactly one 32-byte salt and one 64-character lowercase `salt_hex` during an authorized successful capture;
- exactly one combined configuration-derived SHA-256;
- zero per-variable hashes;
- a 23-field safe receipt in fixed order;
- no-substitution and fail-closed behavior;
- `runtime_authorized = false`.

## 6. Current B05 product identity

The current B05 service is the committed HEAD blob `f0c4a8768060a840ea1921aeba47a97f2e41f9e3`:

```text
service_blob = f0c4a8768060a840ea1921aeba47a97f2e41f9e3
registry_schema = sentigraph_internal_alpha_local_exchange_sample_registry_v0_1
sample_handle = helldivers2-psn-demo
result_file_name = provider_result_helldivers2-psn-demo_20260720_123627.json
route_mode = internal_alpha_read_only_local_exchange_projection_operator
capability_label = b05_local_exchange_projection_read_only
registry_entry_count = 1
entry_enabled = true
```

The server-owned variable order is immutable:

1. `SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR`
2. `SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT`
3. `SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID`

All five product gates remain default-disabled by product posture. Registry presence and `entry_enabled = true` do not authorize a gate read, gate change, application import, artifact access, or endpoint call.

## 7. Current-product CIB overlay

Baseline v2.2 defines a docs-only overlay over the accepted historical CIB-P1 contract. Exactly two stale product-identity constants change:

| Canonical field | Historical CIB-P1 value | Current-product overlay value |
| --- | --- | --- |
| `service_blob` | `9818622c3000092e4f9ee84b4a86300bb415d074` | `f0c4a8768060a840ea1921aeba47a97f2e41f9e3` |
| `result_file_name` | `provider_result_helldivers2-psn-demo_20260614_055754.json` | `provider_result_helldivers2-psn-demo_20260720_123627.json` |

No other product or contract constant changes. The registry schema, sample handle, route mode, capability label, registry cardinality, enabled state, variable names and order, validation contract, schemas, versions, field orders, binding scope, canonicalization, one-salt behavior, and one-combined-digest behavior remain unchanged.

The authority states are explicit:

```text
historical CIB-P1 contract = valid historical contract for its frozen historical product identity
current-product overlay = future current-product CIB capture authority definition, inactive until a separate Risk Prompt 1 approval and Goal
CIB captured by this docs Goal = no
salt generated = no
binding created = no
receipt created = no
runtime authority created = no
```

## 8. Preserved schema, canonicalization, and receipt semantics

### 8.1 Value validation and no substitution

The results-directory and collector-export-root values must each be an actual string, used exactly without modification, contain from 1 through 2048 characters inclusive, satisfy `value == value.strip()`, be printable, and contain no NUL character.

The adapter ID must be an actual string whose original value exactly matches:

```text
^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$
```

No trimming, case normalization, repair, fallback, or replacement is permitted. All three values remain opaque strings for CIB capture. CIB validation performs no path construction, normalization, resolution, existence check, file-type check, directory listing, glob, walk, search, filesystem opening, package lookup, or artifact lookup.

The only future value source is the authorized capture process environment under the three exact names in the frozen order, with one direct read per name. Forbidden substitutions include environment files, configuration files, shell dumps, client or caller input, aliases, command-line values, request values, registry-entry fields, committed-document reconstructions, guesses, prior-run values, and path-derived values.

### 8.2 Binding identifiers

```text
binding schema = sentigraph_b05_server_owned_configuration_identity_binding_v0_1
binding version = 0.1
receipt schema = sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1
receipt version = 0.1
binding scope = b05_one_real_sample_handle_governed_read_only_projection_pre_smoke
canonicalization label = sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1
```

Versions are the exact string `0.1`.

### 8.3 Canonical object and digest

The future in-memory canonical object contains exactly 11 fields in this insertion order:

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

`configuration_values` is an ordered list of exactly three objects in the frozen variable order. Each object contains exactly two fields in this order:

1. `name`
2. `value`

Serialization is compact insertion-order JSON with `ensure_ascii = false`, separators `(",", ":")`, `sort_keys = false`, UTF-8, no BOM, no terminal newline, no Unicode normalization, no fallback encoding, no key sorting, no inserted whitespace, and no value transformation.

An authorized successful capture generates exactly one salt with `secrets.token_bytes(32)`. Its hexadecimal representation is exactly 64 lowercase characters. Exactly one combined configuration-derived SHA-256 is computed over the canonical UTF-8 bytes. No individual value, name/value pair, or partial canonical object is hashed, and per-variable hashes remain zero.

### 8.4 Safe receipt

The safe receipt contains exactly 23 fields in this order:

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

The current-product receipt uses the overlay's current `service_blob` and `result_file_name`, the three names in their frozen order, and these unchanged constants:

```text
configuration_source = process_environment_exact_names_only
environment_read_count = 3
binding_status = configuration_identity_bound
raw_values_exposed = false
per_variable_hashes_created = false
path_operations_performed = false
application_imported = false
artifact_accessed = false
endpoint_called = false
runtime_authorized = false
```

The receipt contains no raw value, value fragment, value length, path, path status, per-variable hash, environment dump, credential, private identity, exception, traceback, or extension field. The salt and combined digest are equality-binding governance evidence, not encryption or proof of runtime readiness.

### 8.5 Fail-closed behavior

Any missing, non-string, blank, whitespace-altered, over-bound, nonprintable, NUL-containing, or adapter-regex-invalid value stops capture without salt generation, configuration-derived hashing, or a successful receipt. There is no automatic retry, second read, substitution, repair, raw exception, raw value, fragment, length, path, traceback, or environment dump.

Even a successful future binding retains `runtime_authorized = false` and grants no artifact, application, gate, endpoint, persistence, or production authority.

## 9. Overlay invalidation conditions

The current-product overlay becomes stale before capture if any of the following changes:

- B05 service blob;
- registry schema;
- sample handle;
- result basename;
- route mode;
- capability label;
- registry cardinality or enabled state;
- approved variable names or order;
- value-validation contract;
- binding or receipt schema or version;
- binding scope;
- canonicalization;
- salt or digest semantics.

A later change requires a separate governance decision. A historical or stale overlay must never be used silently.

## 10. Baseline v2.2 accounting and reservations

Baseline v2.2 is established only after commit, push to `origin/main`, and independent ChatGPT acceptance. Before independent acceptance:

```text
status = candidate_completed_pending_independent_ChatGPT_acceptance
```

After independent acceptance:

```text
starting engineering / fixed / conditional / risk = 0 / 0 / 0 / 0
budget fixed / conditional / risk = 1 / 1 / 3
remaining fixed / conditional / risk = 1 / 1 / 3
```

The docs-only establishment Goal consumes no Baseline v2.2 category. The reservations are:

| Reservation | Reserved scope |
| --- | --- |
| Fixed Prompt 1 | One directly coupled CIB contract correction or static hardening reserve |
| Conditional Prompt 1 | One post-capture, pre-GET narrow diagnostic reserve |
| Risk Prompt 1 | One current-product CIB capture |
| Risk Prompt 2 | One governed B05 GET smoke |
| Risk Prompt 3 | One post-protected recovery reserve |

Budget is planning capacity only. CIB capture and B05 GET must not be merged merely to conserve accounting.

## 11. Current no-authority boundary

This document grants no authority for:

- process-environment or HKCU reads or writes;
- salt generation;
- CIB canonical-object creation;
- binding digest or safe-receipt creation;
- protected-path or artifact access;
- gate reads, enablement, or mutation;
- application import or app-factory execution;
- TestClient or ASGI execution;
- route, endpoint, or B05 GET execution;
- database or persistence access;
- production, public export, or delivery;
- Collector action or network access;
- Project Source maintenance.

This Goal performs documentation governance only. It executes no product code, tests, build, runtime, endpoint, or protected operation.

## 12. Next default

After independent ChatGPT acceptance, the default next route is:

```text
Baseline v2.2 Risk Prompt 1 = one current-product CIB capture
selected = no
authorized = no
Goal-authorized = no
executed = no
```

Risk Prompt 2 and Risk Prompt 3 remain separately reserved and unauthorized. This next-default statement selects no route and authorizes no action.

The required next action is to stop and return this candidate for independent ChatGPT review. Only a later exact Risk Prompt 1 approval and fresh Goal may authorize current-product CIB capture.

## 13. Project Source follow-up

This repository document does not generate, upload, add, delete, replace, or modify an active ChatGPT Project Source or Project instruction.

After independent acceptance, ChatGPT may separately decide whether candidate Source files should be generated. Candidate Source generation and active Source replacement are distinct operations. Neither operation is included in, implied by, or authorized by this docs-only Goal.
