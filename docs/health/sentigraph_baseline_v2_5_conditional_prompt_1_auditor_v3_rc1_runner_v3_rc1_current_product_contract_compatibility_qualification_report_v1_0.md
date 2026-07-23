# Sentigraph Baseline v2.5 Auditor V3 RC1 and Runner V3 RC1 Current-product Contract Compatibility Qualification

## Decision and authorization

- Milestone: `SENTIGRAPH-BASELINE-V2-5-CONDITIONAL-PROMPT-1-AUDITOR-V3-RC1-RUNNER-V3-RC1-CURRENT-PRODUCT-CONTRACT-COMPATIBILITY-QUALIFICATION`.
- Candidate classification: `ready_auditor_v3_rc1_runner_v3_rc1_current_product_contract_compatibility_qualification_pending_independent_acceptance`.
- Privacy issue stop: `false`.
- Approval SHA-256: `2652e7e824e17f6650ae724b0d5d574bddcf7108c3cf5a884a9de5b97b9a55de`.
- Contract SHA-256: `087e58924f6dbe203aab0a45f080b2f372a47c64e0e404834ecab452d0c4bb7b`.
- Approval consumed / reusable: `yes / no`.

## Goal and accounting

- Goal: `Sentigraph Baseline v2.5 Auditor V3 RC1 and Runner V3 RC1 Current-product Contract Compatibility Qualification`.
- Goal requested / activated / reusable: `yes / yes / no`.
- Starting repository / branch: `dgmpurf/Sentigraph / main`.
- Starting HEAD: `1faec34fb948ad21180c8768c64b02708f5cf281`.
- Starting message: `Qualify B05 GET smoke auditor and runner v3 recovery`.
- Pre-Goal repository status: clean, staged `0`, untracked `0`.
- Before engineering / fixed / conditional / risk: `1 / 1 / 0 / 0`.
- After engineering / fixed / conditional / risk: `2 / 1 / 1 / 0`.
- Remaining fixed / conditional / risk: `0 / 0 / 2`.
- Fixed Prompt 1 remains `needs_fix / consumed / nonreusable / historical` and is not reclassified.
- Conditional Prompt 1 is candidate completed / consumed / nonreusable.
- Risk Prompt 1 and Risk Prompt 2 remain unconsumed, unselected and unauthorized.

## Bound Tier B sources

Exactly six primary physical reads were performed, with no reopen or recovery read. All later extraction used retained immutable bytes.

| Source | Bytes | SHA-256 | Byte-derived Git blob | Primary / recovery reads | UTF-8 / BOM absent / AST |
|---|---:|---|---|---|---|
| auditor_v3 | 77775 | `0d43a408f86904f981be9091be035b19e4baa8830045393fe712b41c19905743` | `dea9254dcb4b822ad7539327812db11c26fb24f8` | 1 / 0 | true / true / true |
| runner_v3 | 22613 | `70fe65f50ee2dfeb07c04790086929bf05ceb8956a0cfa6fda3448b2905b0c92` | `3b32a1e909a0f770eb19012946362196661c32c0` | 1 / 0 | true / true / true |
| capture_runner | 4751 | `dd1c63882a90b95956555ffe2d9ae6a866f788135cba70cf58743996ef54a0fc` | `e917d04ec4dc69a07dcbb83cc21a1bbc68f5773d` | 1 / 0 | true / true / true |
| b05_service | 7717 | `b75c6cb9901fc998747e9e54346431ef06c1c22482d92d5cb1b776eee12a000a` | `f0c4a8768060a840ea1921aeba47a97f2e41f9e3` | 1 / 0 | true / true / true |
| b05_route | 11765 | `50dfeff34c4c795c4bbb6287f7d1f622199735e971fc273e0e207e447092236b` | `8445b4595ea7edc9d9878e99b35ce0554b841c94` | 1 / 0 | true / true / true |
| b03_projection | 17962 | `38569248d038caa4ee4089124b9c70f6c32fc3185e42166bd837a18409b90d54` | `534bdf02e211134b52b2e7714d01a0dd615210b4` | 1 / 0 | true / true / true |

Source identities by authorized path:

- `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v3.py`.
- `.sentigraph_b05_get_smoke_runner_v3.py` in the fixed repository-external parent.
- `.sentigraph_cib_capture_risk_prompt_3_v1.py` in the fixed repository-external parent.
- `backend/app/services/internal_alpha_local_exchange_review_projection.py`.
- `backend/app/api/v1/routes/internal_alpha_review_console.py`.
- `backend/app/services/local_exchange_review_only_projection_bridge.py`.

Primary reads / recovery reads: `6 / 0`. Aggregate recovery source / reason / equality: `none / not used / not applicable`.

## Historical V3 defects and preservation

The bound V3 Auditor contains exactly 30 prior checks and omits both `RECEIPT_CONTRACT_EXACT` and `PROJECTION_FIELDS_MODULE_IDENTITY_EXACT`. Its embedded valid fixture is byte-identical to the bound Runner V3.

Runner V3 requires a different 23-field tuple containing incompatible identifiers including `status`, `privacy_issue_stop`, `configuration_names`, ledger fields and `warnings`; it omits accepted identifiers including `variable_names`, `canonicalization_label`, `configuration_source`, `environment_read_count`, `binding_status` and `runtime_authorized`. Its receipt reader requires exact tuple equality. Runner V3 also obtains `PROJECTION_FIELDS` through the incompatible module identity `app.api.v1.endpoints.internal_alpha_review_console`.

The historical Auditor V3, Runner V3 and Fixed Prompt report remain unchanged. Fixed Prompt 1 remains `needs_fix_runner_v3_current_product_contract_compatibility`.

## Accepted receipt compatibility contract

The capture runner defines one direct `safe_receipt` dictionary with exactly these 23 fields in order:

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

Public constants extracted from the bound capture runner are exact:

- Schema / version: `sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1 / 0.1`.
- Binding scope: `b05_one_real_sample_handle_governed_read_only_projection_pre_smoke`.
- Service blob: `f0c4a8768060a840ea1921aeba47a97f2e41f9e3`.
- Registry schema / sample: `sentigraph_internal_alpha_local_exchange_sample_registry_v0_1 / helldivers2-psn-demo`.
- Result file: `provider_result_helldivers2-psn-demo_20260720_123627.json`.
- Route mode / capability: `internal_alpha_read_only_local_exchange_projection_operator / b05_local_exchange_projection_read_only`.
- Variable names: `SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR`, `SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT`, `SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID`, in order.
- Canonicalization / configuration source: `sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1 / process_environment_exact_names_only`.
- Environment read count / binding status: `3 / configuration_identity_bound`.
- All seven safety and runtime-authorization Boolean fields: `false`.
- Actual receipt reads / reopens: `0 / 0`.

No receipt body, salt, combined binding or environment value was read or retained.

## Current-product projection compatibility contract

- The B05 route source defines `/local-exchange-projections/{sample_handle}` and delegates exactly once to `build_internal_alpha_local_exchange_review_projection`.
- The approved full target contract is `/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo`; the bound route source provides its endpoint suffix while the authorized contract provides its mounted prefix.
- The B05 service directly imports `PROJECTION_FIELDS` from `app.services.local_exchange_review_only_projection_bridge`.
- The B03 projection source defines one direct tuple literal containing 52 unique strings in exact order.
- The exact runtime module identity is `app.services.local_exchange_review_only_projection_bridge`.
- The old endpoints identity is not the current source of `PROJECTION_FIELDS`.

Exact ordered projection fields:

1. `projection_schema`
2. `projection_version`
3. `projection_mode`
4. `projection_status`
5. `projection_error_code`
6. `source_chain_boundary`
7. `result_file_name`
8. `upstream_schema`
9. `upstream_status`
10. `reader_status`
11. `adapter_status`
12. `provider_result_status`
13. `package_resolution_status`
14. `candidate_count`
15. `staging_candidate_id`
16. `gate_result_id`
17. `analysis_request_id`
18. `provider_result_id`
19. `package_name`
20. `case_id_hint`
21. `case_title_hint`
22. `validation_summary`
23. `coverage_summary`
24. `review_status`
25. `promotion_status`
26. `staging_status`
27. `gate_summary`
28. `warnings`
29. `blockers`
30. `allowed_actions`
31. `blocked_actions`
32. `metadata_only`
33. `review_only`
34. `human_review_required`
35. `no_automatic_trust_upgrade`
36. `candidate_persistence`
37. `persistent_staging_write`
38. `review_decision_write`
39. `evidence_layer_write`
40. `production_evidenceitem_created`
41. `production_case_created`
42. `analysis_run_created`
43. `analysis_result_created`
44. `frontend_action_enabled`
45. `public_output_enabled`
46. `export_delivery_enabled`
47. `path_exposed`
48. `raw_metadata_exposed`
49. `trust_approved`
50. `production_ready`
51. `promotion_completed`
52. `mutable_authority_granted`

## Pre-freeze attempts and recoveries

- Complete compatibility matrix attempts: `3` of maximum `3`.
- Recovery count: `2`.
- Recovery 1: `source_extractor_defect_annassign`; expanded retained-byte extraction for annotated `PROJECTION_FIELDS` and route evidence; Auditor changed / Runner changed / source rereads: `no / no / 0`.
- Attempt 1: valid audit `32/32`, fixtures `22/22`, exact matches `22/22`; aggregate status failed only because inherited check-order cardinality was still 30.
- Recovery 2: `checker_logic_hardcoded_v3_cardinalities`; updated the inherited check and fixture cardinality assertions; Auditor changed / Runner changed: `yes / no`.
- Attempt 2: all audits and fixtures passed, but an additional inherited fixture-acceptance literal remained 20; this was completed within the same bounded cardinality recovery.
- Attempt 3: status pass; valid `32/32`; negatives tested/rejected `22/22`; parse failures `0`; exact matches `22/22`.
- Filesystem targets created before complete passage: `0`.

## Frozen RC1 identities

- Auditor path: `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v3_rc1.py`.
- Auditor bytes / SHA-256 / Git blob: `94688 / d8f74463516c23e8c9da8ec8bb59ffcb4e9bf64c12e6404c74f0416bf9ad25e5 / 6b4f95b3c18e06751dbcdb7ecdd69ce5778c2542`.
- Auditor strict UTF-8 / BOM absent / AST: `true / true / true`.
- Auditor imports: future annotations, `ast`, `hashlib`, `json`, `sys`, and `Path` from `pathlib` only.
- Runner basename: `.sentigraph_b05_get_smoke_runner_v3_rc1.py`.
- Runner bytes / SHA-256: `25722 / 62c75c7d79ad0983261e0c3ff3e560cf5ad6641fc7cc766e8d741cfae80452f6`.
- Runner strict UTF-8 / BOM absent / AST: `true / true / true`.
- Embedded fixture / frozen Runner / external Runner equality: `true`.
- Source modifications after freeze: `0`.

## Exact 32 checks

1. `STRICT_UTF8_NO_BOM`
2. `AST_PARSE`
3. `IMPORT_ALLOWLIST`
4. `BOUND_CONSTANTS`
5. `RECEIPT_SINGLE_READ`
6. `RECEIPT_CONTRACT_EXACT`
7. `CONFIG_EXACT_THREE_READS`
8. `CIB_DATAFLOW`
9. `CANONICAL_BINDING_CONSTANTS_EXACT`
10. `CONFIGURATION_BOUND_EXACT`
11. `NO_RANDOM_OR_WEAK_HASH`
12. `GATE_PRESTATE_EXACT_ORDER`
13. `GATE_WRITE_EXACT_ORDER`
14. `GATE_RESTORE_REVERSED_OUTER_FINALLY`
15. `DOTENV_PATCH_BEFORE_APP_IMPORT`
16. `DOTENV_RESTORE_OUTER_FINALLY`
17. `APP_IMPORT_EXACTLY_ONCE`
18. `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
19. `NO_ASYNCIO_RUN`
20. `ASGI_TRANSPORT_EXACTLY_ONCE`
21. `TARGET_ROUTE_EXACT`
22. `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
23. `PERFORM_GET_CALLED_EXACTLY_ONCE`
24. `PROJECTION_FIELDS_MODULE_IDENTITY_EXACT`
25. `RESPONSE_EXACT_52_FIELD_ORDER`
26. `RESPONSE_BOUNDED_HASH_ONLY`
27. `FILE_GUARD_BOUNDARY`
28. `RAW_ROW_PRIVACY_FAIL_CLOSED`
29. `NO_DIRECTORY_DISCOVERY`
30. `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
31. `NO_EXTERNAL_OR_MUTATING_ACTIONS`
32. `ATOMIC_SAFE_RESULT_AND_OUTPUT`

Count / uniqueness / order: `32 / 32 / exact`.

## Exact 22 fixture outcomes

1. `second_http_get` -> `HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET`
2. `perform_get_called_twice` -> `PERFORM_GET_CALLED_EXACTLY_ONCE`
3. `gate_restore_removed` -> `GATE_RESTORE_REVERSED_OUTER_FINALLY`
4. `dotenv_patch_after_import` -> `DOTENV_PATCH_BEFORE_APP_IMPORT`
5. `dotenv_restore_removed` -> `DOTENV_RESTORE_OUTER_FINALLY`
6. `forged_cib_digest` -> `CIB_DATAFLOW`
7. `response_order_removed` -> `RESPONSE_EXACT_52_FIELD_ORDER`
8. `raw_row_read` -> `RAW_ROW_PRIVACY_FAIL_CLOSED`
9. `external_socket_action` -> `NO_EXTERNAL_OR_MUTATING_ACTIONS`
10. `payload_output` -> `ATOMIC_SAFE_RESULT_AND_OUTPUT`
11. `asyncio_run_added` -> `NO_ASYNCIO_RUN`
12. `second_app_import` -> `APP_IMPORT_EXACTLY_ONCE`
13. `second_event_loop` -> `EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT`
14. `asgi_transport_removed` -> `ASGI_TRANSPORT_EXACTLY_ONCE`
15. `target_route_changed` -> `TARGET_ROUTE_EXACT`
16. `directory_discovery_added` -> `NO_DIRECTORY_DISCOVERY`
17. `socket_type_replaced` -> `NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED`
18. `atomic_replace_removed` -> `ATOMIC_SAFE_RESULT_AND_OUTPUT`
19. `receipt_schema_substitution` -> `CANONICAL_BINDING_CONSTANTS_EXACT`
20. `opaque_configuration_bound_1048` -> `CONFIGURATION_BOUND_EXACT`
21. `receipt_field_contract_substitution` -> `RECEIPT_CONTRACT_EXACT`
22. `projection_fields_module_endpoints_substitution` -> `PROJECTION_FIELDS_MODULE_IDENTITY_EXACT`

All fixtures parsed, were rejected, failed exactly the named check and passed the other 31 checks.

The two new compatibility fixtures have isolated outcomes:

- `receipt_field_contract_substitution` changes only `variable_names` to `configuration_names` and fails only `RECEIPT_CONTRACT_EXACT`.
- `projection_fields_module_endpoints_substitution` changes only the direct module literal and fails only `PROJECTION_FIELDS_MODULE_IDENTITY_EXACT`.
- `asyncio_run_added` fails only `NO_ASYNCIO_RUN`.
- `receipt_schema_substitution` fails only `CANONICAL_BINDING_CONSTANTS_EXACT`.
- `opaque_configuration_bound_1048` fails only `CONFIGURATION_BOUND_EXACT`.

## Compatibility self-check and final qualification

- Compatibility contract exact: `true`.
- Receipt field count: `23`.
- Projection field count / uniqueness / order: `52 / true / exact`.
- Projection module identity: `app.services.local_exchange_review_only_projection_bridge`.
- Qualification executions / retries: `1 / 0`.
- Exit / stderr empty: `0 / true`.
- Schema / version / status: `sentigraph_b05_get_smoke_auditor_v3_rc1_runner_v3_rc1_current_product_contract_compatibility_qualification_result_v0_1 / 0.1 / pass`.
- Self-test status: `pass`.
- Valid total / accepted: `1 / 1`.
- Negative total / tested / rejected: `22 / 22 / 22`.
- Fixture parse failures / exact matches: `0 / 22`.
- Final Runner audit total / passed / failed: `32 / 32 / 0`.
- Final failed checks: `[]`.
- Runner reads / reopens / executed: `1 / 0 / 0`.
- Environment / receipt / product access: `0 / 0 / 0`.

## File and Git allowlists

Repository creations are limited to:

1. `scripts/governance/sentigraph_b05_get_smoke_static_auditor_v3_rc1.py`.
2. `docs/health/sentigraph_baseline_v2_5_conditional_prompt_1_auditor_v3_rc1_runner_v3_rc1_current_product_contract_compatibility_qualification_report_v1_0.md`.

The sole external creation is `.sentigraph_b05_get_smoke_runner_v3_rc1.py`, outside Git and never staged. Existing files modified: `0`. Backend, frontend, browser, application and product tests were not run because this is a static-only compatibility qualification against identity-bound sources.

## Hard-zero Tier A ledger

- Actual safe receipt reads / reopens: `0 / 0`.
- Safe-result reads / reopens: `0 / 0`.
- Environment reads / enumeration / writes: `0 / 0 / 0`.
- Gate reads / writes: `0 / 0`.
- Application imports / factory calls: `0 / 0`.
- Event-loop creations: `0`.
- Runner V3 executions / Runner V3 RC1 executions / GET attempts: `0 / 0 / 0`.
- Provider Result / package / collector access: `0 / 0 / 0`.
- Raw evidence / source / comment / log reads outside the six approved static sources: `0 / 0 / 0 / 0`.
- External product network / address resolution: `0 / 0`.
- Unapproved product subprocess: `0`.
- Database / persistence: `0 / 0`.
- Product-code changes: `0`.
- Project Source generation / replacement: `0 / 0`.
- Production / export / delivery: `0 / 0 / 0`.

Approved governance processes were limited to retained-byte AST extraction, candidate parsing, mutation preflights, complete static matrices and the one final qualifier. They did not execute either Runner or import product code.

## Directly established

The RC1 candidates were built from six identity-bound static sources. They enforce the accepted 23-field receipt contract and current-product projection module, contain exactly 32 ordered checks, reject all 22 fixtures with their exact single failures, pass 32/32, and preserve byte equality between embedded, frozen and external Runner RC1. Conditional Prompt 1 is ready for independent acceptance.

## Not established and current boundary

This work does not establish actual receipt compatibility at runtime, current CIB equality, environment stability, application readiness, B05 GET success, Provider Result or collector correctness, receipt-read authority, Runner execution authority, Risk Prompt selection, CIB recapture authority, Project Source replacement, or production/persistence/export/delivery readiness.

Current protected-access, runtime, GET and CIB-recapture authority are `none`. Risk Prompt 1 is an eligibility candidate only and remains unselected and unauthorized. The next action is independent ChatGPT acceptance; no Runner execution or new Goal is authorized here.
