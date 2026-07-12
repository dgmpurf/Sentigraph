# Sentigraph MVP13-F01 Durable Synthetic Exact-target Read-only Audit Helper Report v1.0

## 1. Decision

decision = ready
privacy_issue_stop = no
task = MVP13-F01 durable synthetic-tested exact-target read-only audit helper implementation
MVP13_F01_status = candidate_completed_pending_chatgpt_acceptance
durable_helper_implemented = yes
synthetic_validation_complete = yes
repository_runtime_target_accessed = no
current_target_state = unknown_not_safely_classified

The implementation is a synthetic-only, explicit-target, bounded read-only audit
helper. This phase did not execute the helper against a repository runtime target
and did not classify current runtime state.

## 2. Goal, Model, and Approval

Goal_created = yes
Goal_activated = yes
Goal_active_state_observed = yes
Goal_completion_status_at_report_generation = implementation_and_validation_complete_pending_git_finalization

actual_model_used = current OpenAI Codex GPT-5 session model
exact_deployment_identifier_exposed = no

approval_phrase_match = yes
approval_phrase_scope = MVP13-F01 synthetic helper, focused test, and health report only
approval_phrase_sha256 = ca87ce64d713d1c0a902c315de2dfdc1b2f995adf8336cccdf2105e736fdc585
MVP13_F02_authorized = no
MVP13_F02_executed = no

## 3. Starting State and Prompt Accounting

starting_branch = main
starting_commit = 486bc547da6b97e121565489cf3b6e1a8c15080e
starting_commit_message = Establish Baseline v1.3 after F02 audit risk exhaustion
starting_origin_main = 486bc547da6b97e121565489cf3b6e1a8c15080e
starting_ahead_behind = 0/0
starting_worktree_clean = yes
starting_staged_file_count = 0
starting_untracked_file_count = 0
all_three_output_paths_absent_at_preflight = yes

consumed_engineering_prompts_since_v1_3_baseline = 1
consumed_fixed_prompts_since_v1_3 = 1
consumed_conditional_prompts_since_v1_3 = 0
consumed_risk_prompts_since_v1_3 = 0
remaining_fixed_prompts = 13
remaining_conditional_allowance = 6
remaining_risk_buffer = 2

## 4. Frozen Artifact Verification

Baseline v1.3 architecture document:

- size = 20011 bytes
- SHA-256 = d524d2670ba03880e10f2e957a6029f8a272062494fb1afef6771161086ddf93

Governed nonproduction evidence persistence service:

- SHA-256 = ca5021eb28779685a3d5c0ec42874528025baaaae7c7de3026528d8e0c10e99c

MVP12-F02 execution report:

- size = 7410 bytes
- SHA-256 = eb0eae1db9ff0ce3552134206c38a7467b918331a1a7db4f311b750c277e2946

MVP12-CHG-002-P1 F02 audit report:

- size = 12291 bytes
- SHA-256 = 90fa8f145725e679d52c5a5b18409897b5384f6ab5083d4913cfc71c62d8e4d8

frozen_files_modified = no

## 5. Source and AST Alignment

The committed persistence service was inspected as UTF-8 source and AST only.
The helper aligns to the committed logical label, exact two-table names, record
and reservation schemas, command schema, create-only mutation mode, one-attempt
limit, exact column orders, canonical hashes, identity/payload contracts, and
pure command derivation.

record_reconstruction = committed pure row converter reused
reservation_reconstruction = exact actual-column reconstruction in owner
canonical_record_hash = committed pure hash behavior reused
canonical_reservation_hash = committed pure hash behavior reused
pure_command_derivation_parity = verified

The frozen reservation converter has a pre-existing validation-order mismatch:
it applies an opaque-token check to the valid slash-bearing logical label before
its dedicated logical-label validation. The new owner therefore reconstructs
reservation columns with the same exact field, schema, version, hash, timestamp,
token, and logical-label contracts while applying the dedicated logical-label
validator to that field. The frozen persistence service was not modified, and
the helper did not weaken reservation validation.

writer_path_separately_identified = yes
writer_path_imported_by_owner = no
writer_path_called_by_owner = no
mutation_helper_imported_or_called = no

## 6. Genuine TDD Evidence

test_file_created_before_owner_module = yes
RED_command_scope = public symbol plus A, B, and C synthetic classifications
RED_collected_case_count = 4
RED_failed_case_count = 4
RED_failure_class = expected owner module absent
fake_stub_used = no

After the owner was created, the smallest classification loop exposed the
frozen reservation validation-order mismatch described above. The narrow owner
reconstruction was added, the A/B/C loop became green, and the complete focused
matrix was then run.

GREEN_focused_test_function_count = 29
GREEN_focused_pytest_case_count = 75
GREEN_focused_failed_case_count = 0

## 7. Owner Module and Public API

owner_module = backend/app/services/governed_nonproduction_exact_target_read_only_audit.py
public_function_count = 1
public_function = audit_governed_nonproduction_exact_target_read_only
public_default_physical_target = none

The API requires an explicit authorized root, explicit database path, exact
logical target label, expected identity, gate and activation bindings, expected
input safe hash, and every caller-derived stable ID or digest. All derived
bindings are recomputed before filesystem access and must match exactly.

## 8. Explicit Path and Sidecar Contract

explicit_authorized_root_required = yes
explicit_database_path_required = yes
lexical_absolute_equality_required = yes
target_inside_authorized_root_required = yes
target_discovery = no
directory_enumeration = no
environment_override = no
working_directory_fallback = no
in_memory_fallback = no

Root, existing parent components, and target receive exact metadata probes.
Symlinks, simulated Windows reparse points, non-regular targets, missing targets,
outside-root paths, and lexical mismatches fail closed before SQLite opens.

exact_sidecar_preflight = journal, WAL, and SHM only
exact_sidecar_postflight = journal, WAL, and SHM only
sidecar_deletion_or_checkpoint = no
preflight_sidecar_opens_sqlite = no
postflight_sidecar_appearance_classification = inconsistent_or_not_safely_classifiable

## 9. SQLite Read-only Posture

sqlite_file_uri_mode = ro
immutable_mode_used = no
connection_local_query_only_enabled = yes
connection_local_query_only_readback_verified = yes
sqlite_row_factory = actual named columns
restrictive_authorizer_installed_before_target_rows = yes

The authorizer permits only the minimum query-only pragma, selection, and exact
column reads for the two allowlisted tables. Focused tests prove denial of row
mutation, schema mutation, transaction control, attach/detach, unsafe pragmas,
reindex, analyze, and reads outside the exact table/column allowlist. No mutation
was executed as an owner-module self-test.

## 10. Schema, Rows, and Binding Verification

allowlisted_table_count = 2
schema_enumeration = no
metadata_catalog_query = no
exact_cursor_column_order_required = yes
maximum_rows_read_per_table = 2
unbounded_fetch = no

count_classes = exact_0, exact_1, at_least_2, not_obtained
strict_canonical_JSON_parsing = yes
strict_SQLite_boolean_0_or_1 = yes
actual_column_reconstruction = yes
record_canonical_hash_recomputed = yes
reservation_canonical_hash_recomputed = yes

Reservation binding covers the exact reservation ID, scope, candidate digest,
input hash, gate binding, activation binding, logical label, mutation mode,
idempotency key, expected record ID, one-attempt maximum, and reserved attempt
number. Its variable timestamp remains validated and canonical-hash covered.

Record binding covers exact record schema, identity projection, input hash,
validated safe payload, source-schema and lineage projections, gate and
activation bindings, stable IDs, create-only mode, pending-human-review status,
required human review, no automatic trust upgrade, null revocation fields, and
all production/downstream side-effect flags false.

When both rows exist, candidate, input, gate, activation, idempotency, and
timestamp bindings must agree.

## 11. Result Contract

result_schema = sentigraph_governed_nonproduction_exact_target_read_only_audit_result_v0_1
result_version = 0.1
exact_result_field_count = 43
exact_result_field_set_verified = yes
JSON_serializable_results_verified = yes
deterministic_identical_state_results_verified = yes

safe_stage_count = 13
safe_stages = input_validation, target_identity, target_metadata, sidecar_preflight, sqlite_open, read_only_posture, schema_contract, row_read, row_reconstruction, binding_validation, classification, sidecar_postflight, completed

outcome_count = 7
outcomes = exact_empty, exact_expected_reservation_only, exact_expected_reservation_and_record, inconsistent_or_not_safely_classifiable, sidecar_present_read_prohibited, target_identity_or_metadata_blocked, bounded_read_only_failure

Results contain bounded tokens, booleans, nulls, count classes, and safe
snapshot digests only. They contain no physical path, raw row, full record,
full reservation, expected identity, payload projection, SQL, exception text,
or stack trace.

## 12. Outcome Semantics

A_exact_empty = zero record rows, zero reservation rows, exact schema, no sidecars
A_mutating_attempt_consumed = no
A_record_exists = no

B_exact_expected_reservation_only = zero record rows and one exact reservation
B_mutating_attempt_consumed = yes
B_record_exists = no

C_exact_expected_reservation_and_record = one exact reservation and one exact cross-bound record
C_mutating_attempt_consumed = yes
C_record_exists = yes

D_inconsistent_or_not_safely_classifiable = observed row, integrity, binding, cross-binding, or postflight-sidecar inconsistency

metadata_failure = target_identity_or_metadata_blocked before SQLite open
preflight_sidecar_failure = sidecar_present_read_prohibited before SQLite open
read_only_operation_failure = bounded_read_only_failure without exception text

audit_task_completed_on_bounded_return = yes
production_evidenceitem_created = no
production_case_changed = no
downstream_runtime_called = no
writer_invoked = no
mutation_attempted = no

## 13. Focused and Nearby Validation

Focused helper suite:

- test function count = 29
- collected pytest case count = 75
- result = pass

Existing governed nonproduction persistence suite:

- test function count = 49
- collected pytest case count = 68
- result = pass

Combined nearby suite:

- test function count = 78
- collected pytest case count = 143
- result = pass

Compilation:

- new owner module = pass
- new test module = pass

File and documentation validation:

- no-index whitespace checks for all three new files = pass
- trailing-whitespace matches = 0
- placeholder-marker matches = 0
- mojibake matches = 0
- Markdown fence count = 0
- Markdown fences balanced = yes
- standalone Markdown lint command available = no
- Markdown structure and bounded-content checks = pass

full_pytest_run = no
full_pytest_reason = narrow task required focused and nearby validation only
frontend_build_run = no
browser_smoke_run = no

## 14. Static Capability and Value-safety Scan

public_audit_function_count = 1
forbidden_writer_calls = 0
forbidden_writer_imports = 0
forbidden_mutation_helper_calls = 0
store_initialization_calls = 0
mutating_open_calls = 0
mutation_SQL_in_owner = no
target_discovery_calls = 0
immutable_mode_reference = no
environment_fallback = no
automatic_runtime_physical_path_literal = no
payload_or_capture_receipt_capability = no
network_or_subprocess_imports = 0
provider_or_collector_capability = no
logging_or_print_calls = 0

Privacy and value-safety tests cover physical paths, SQL, expected identity,
row values, exception text, and stack traces. Synthetic values and temporary
SQLite targets were used exclusively.

absolute_physical_path_literals_in_changed_files = 0
URL_literals_in_changed_files = 0
actual_PII_in_changed_files = no
secret_values_in_changed_files = no

## 15. Exact Changed-file Inventory

1. backend/app/services/governed_nonproduction_exact_target_read_only_audit.py
2. backend/app/tests/test_governed_nonproduction_exact_target_read_only_audit.py
3. docs/health/sentigraph_mvp13_f01_durable_synthetic_exact_target_read_only_audit_helper_report_v1_0.md

tracked_files_outside_allowlist_changed = no
runtime_artifacts_staged = no
repository_runtime_target_accessed = no
protected_payload_accessed = no
capture_receipt_accessed = no
source_package_or_row_accessed = no
real_candidate_content_accessed = no
public_writer_called = no
mutation_helper_called = no
target_initialized_or_repaired = no
production_or_downstream_runtime_called = no

## 16. Git and Source Boundary

git_diff_check_at_report_generation = pass
git_scope_at_report_generation = exact_three_file_allowlist
git_finalization_at_report_generation = pending_ready_only_final_validation
required_commit_message = Implement MVP13-F01 durable read-only target audit helper
tag = no

Project_Source_modified = no
Project_Source_update_recommendation = defer until ChatGPT independent acceptance
Canonical_00_immediate_change = no
Canonical_03_immediate_change = no
Canonical_09_immediate_change = no
Canonical_05_change = no
Source_11_change = no

## 17. Completion Boundary

MVP13_F01_status = candidate_completed_pending_chatgpt_acceptance
durable_helper_implemented = yes
synthetic_validation_complete = yes
repository_runtime_target_accessed = no

MVP13_F02_technical_eligibility = yes_pending_chatgpt_independent_acceptance
MVP13_F02_authorized = no
MVP13_F02_executed = no
current_target_state = unknown_not_safely_classified

MVP_F09_eligible = no
MVP_F09_authorized = no

next_boundary = ChatGPT independent acceptance of MVP13-F01 followed by a separate fresh MVP13-F02 authorization decision

Do not execute this helper against a repository runtime target, access payload
or capture-receipt material, invoke a writer or mutation helper, initialize or
repair target state, start MVP13-F02, or start MVP-F09 under this report.
