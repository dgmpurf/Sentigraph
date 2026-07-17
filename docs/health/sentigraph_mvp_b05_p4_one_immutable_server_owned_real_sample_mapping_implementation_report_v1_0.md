# Sentigraph MVP-B05-P4 One Immutable Server-owned Real Sample Mapping Implementation Report v1.0

## Decision

- Goal: `MVP-B05-P4 One Immutable Server-owned Real Sample Mapping Implementation`
- Status: `candidate_completed_pending_independent_ChatGPT_acceptance`
- Implementation decision: `ready`
- Privacy or public-release impact: `no`
- Replacement Goal created: `no`

This implementation adds exactly one immutable, server-owned default sample mapping to the existing B05 internal-alpha read-only projection service. It does not authorize or perform runtime verification against the mapped result file.

## Accepted starting identity

- Repository starting HEAD: `d1caa8f046b473df81b07c3b65b38465e2f800f9`
- Accepted approval brief SHA-256: `1362d5cf1987d7d694701123ca41ee910d00c1ee586e2a49eaee953416ea64cb`
- Accepted B05-P3 contract blob: `1d4ef773f9f1b251a7d271623fe7fb2723366e38`
- Starting service blob: `f4b3d87c370ca91bb85504552f1c325ea5f15b58`
- Starting focused-test blob: `474430e0d985c14250bf97e985d18eb254e4f6e2`
- Starting branch alignment: `main` and `origin/main` at `0/0`
- Starting worktree: clean
- Default registry at the starting identity: empty
- P4 completion report at the starting identity: absent

The accepted B05-P3 prerequisite and all frozen-identity checks passed before implementation. Goal activation accounting was recorded as engineering/fixed/conditional/risk `2/2/0/0`, with remaining fixed/conditional/risk `0/4/2`.

## Exact changed-file allowlist

Only these three paths are authorized for this implementation:

1. `backend/app/services/internal_alpha_local_exchange_review_projection.py`
2. `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py`
3. `docs/health/sentigraph_mvp_b05_p4_one_immutable_server_owned_real_sample_mapping_implementation_report_v1_0.md`

No route, API-registration, frontend, configuration, manifest, lock, artifact, package, runtime-data, Project Source, tag, or release file is changed.

## Immutable server-owned mapping

The existing `InternalAlphaLocalExchangeSampleRegistryEntry` remains a frozen five-field dataclass, and the existing registry builder continues to return a `MappingProxyType` while rejecting duplicate handles. The default registry now contains exactly one entry:

| Field | Exact value |
| --- | --- |
| `sample_handle` | `helldivers2-psn-demo` |
| `result_file_name` | `provider_result_helldivers2-psn-demo_20260614_055754.json` |
| `enabled` | `true` |
| `route_mode` | `internal_alpha_read_only_local_exchange_projection_operator` |
| `capability_label` | `b05_local_exchange_projection_read_only` |

The entry contains a basename only. It adds no path, artifact digest, environment value, provider credential, mutable alias, discovery rule, latest-file selection, fallback, retry, glob, directory scan, or additional field. Existing enablement and configuration gates remain unchanged and disabled by default.

## Focused-test adaptation and isolation

The focused test module no longer imports `app.main` or `TestClient` at module load. Those dependencies are imported and a client is constructed only inside the helper called by the two pre-existing route runtime tests. Those two tests remain present without skip or xfail markers.

Tests that require an unknown sample now inject an explicit empty immutable registry, preserving their original meaning after the real default entry was added. The real-default proof omits the registry argument and injects fake staging and projection builders. It proves that the exact mapped basename is handed to each fake exactly once, returns the same direct projection object, and performs no real artifact read.

The isolation test executes before the two route runtime tests and proves, for the selected P4 test set, that application imports and TestClient creations remain zero.

## TDD evidence

### RED

Command:

```text
python -m pytest backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py::test_constants_default_registry_and_exact_b03_contract_are_frozen backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py::test_real_default_mapping_uses_exact_basename_with_injected_fake_builders backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py::test_route_runtime_dependencies_remain_lazy_for_selected_service_tests -q
```

Result: `3 collected / 1 passed / 2 failed`. The failures were the intended pre-implementation failures: the default registry was empty, and the omitted-registry fake-builder proof therefore returned the unknown-sample fail-closed projection. The isolation proof passed with zero application imports and zero TestClient creations.

### Implementation correction before final GREEN

The first selected run after adding the entry exposed a module-initialization ordering error because the populated registry invoked its existing validation helper before that helper had been defined. The same exact mapping initialization was moved below the helper definitions; no contract value or control-flow behavior was changed. This was a source-order correction only and caused no runtime, artifact, endpoint, network, writer, database, or persistence access.

### Final GREEN

Command:

```text
python -m pytest backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py -q -k "not test_route_is_one_path_parameter_get_only_and_preserves_http_200_fail_closed and not test_route_returns_ready_projection_directly_with_http_200"
```

Final result: `52 collected / 50 selected / 50 passed / 0 failed / 2 deselected / 0 skipped / 0 xfailed`.

The two deselected tests were exactly:

- `test_route_is_one_path_parameter_get_only_and_preserves_http_200_fail_closed`
- `test_route_returns_ready_projection_directly_with_http_200`

No full module route run, endpoint run, application startup, TestClient construction, browser run, provider call, collector call, network call, LLM call, database access, writer access, or real result-file read was performed.

## Static and compile validation

- `py_compile` passed for the service and focused-test files only, with bytecode written to and removed with a system temporary directory.
- The final changed-file set before this report contained exactly the two authorized Python files.
- The service contains exactly one occurrence of the mapped result basename and no approval digest.
- The default registry contains exactly one entry.
- Module-level `app.main` imports: `0`.
- Module-level `TestClient` imports: `0`.
- Skip and xfail markers: `0`.
- `git diff --check`: pass.
- Repository bytecode or runtime artifact creation: `0`.

## No-side-effect and product boundary

This P4 implementation is a static server-owned name binding only. It does not verify that the named result exists, does not bind a configured directory, does not inspect an artifact identity, and does not authorize a runtime smoke test. The production staging and projection builders were not invoked through the new real default mapping. All P4 proof for that mapping used injected fakes.

Existing fail-closed behavior, direct B03 projection shape, the 52-field projection contract, route inventory, HTTP behavior, gate names, and environment lookup behavior remain unchanged. No response envelope, persisted-record field, path disclosure, configuration disclosure, or mutation capability is introduced.

## Ready-only Git finalization boundary

Git finalization is permitted only after the report is the third and final changed file, all static validation passes, and the cached diff contains exactly the three allowlisted paths. The only authorized commit message is:

```text
Implement MVP-B05-P4 immutable real sample mapping
```

Push is limited to current `main` to `origin/main`. No tag or release is authorized.

## Post-P4 state

| Question | Answer |
| --- | --- |
| One exact real default mapping implemented and present | `yes` |
| Default registry entry count | `1` |
| Entry enabled | `true` |
| Runtime use authorized | `no` |
| Existing gates disabled by default | `yes` |
| Runtime smoke performed | `no` |
| Mapped artifact identity verified in P4 | `no` |
| Configuration binding created | `no` |
| P5 candidate defined | `yes` |
| P5 selected, eligible, authorized, assigned a Goal, or executed | `no` |

The terminal P4 status is `candidate_completed_pending_independent_ChatGPT_acceptance` after ready-only Git finalization succeeds.
