from __future__ import annotations

import configparser
import hashlib
import json
import os
import re
import sqlite3
import stat
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, Final

from app.services.governed_nonproduction_evidence_persistence import (
    ATTEMPT_RESERVATION_TABLE,
    LOGICAL_RUNTIME_TARGET_LABEL,
    TABLE_NAME,
    _CREATE_ATTEMPT_RESERVATION_TABLE_SQL,
    _CREATE_TABLE_SQL,
)
from app.services.protected_value_boundary_scanner import (
    SAFE_CAPTURE_RECEIPT_PROFILE,
    scan_protected_value_boundary,
)


SYNTHETIC_EXECUTION_PROFILE: Final = "synthetic_temporary_repository"
FORMAL_EXECUTION_PROFILE: Final = "formal_exact_sentigraph_repository"
RESULT_SCHEMA: Final = (
    "sentigraph_governed_nonproduction_target_initialization_smoke_result_v0_3"
)
RESULT_VERSION: Final = "0.3"
EXECUTION_MODE: Final = (
    "backend_only_local_profiled_repository_schema_initialization_smoke"
)
TARGET_KIND: Final = "dedicated_local_sqlite_nonproduction_store"
LOCKED_TARGET_LOGICAL_LABEL: Final = LOGICAL_RUNTIME_TARGET_LABEL
LOCKED_TARGET_IDENTITY_SAFE_HASH: Final = (
    "6f2f543e3f1e463ec19dda2d7c156786432d4fc738e0a57c280390f8b2bf3e5b"
)
LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH: Final = (
    "f3a9a5dc1b23f0ad45cac3ea2bccca357b7b782b512a679f915e850dad17c5d2"
)
LOCKED_RECEIPT_LOGICAL_LABEL: Final = (
    "runtime/governed_nonproduction_evidence_persistence/"
    "target-initialization-receipt-"
    f"{LOCKED_TARGET_IDENTITY_SAFE_HASH}.json"
)
FORMAL_REPOSITORY_IDENTITY_SCHEMA: Final = (
    "sentigraph_formal_repository_identity_v0_1"
)
FORMAL_REPOSITORY_IDENTITY_VERSION: Final = "0.1"
FORMAL_REPOSITORY_IDENTITY_PROJECTION: Final = MappingProxyType(
    {
        "repository_identity_schema": FORMAL_REPOSITORY_IDENTITY_SCHEMA,
        "repository_identity_version": FORMAL_REPOSITORY_IDENTITY_VERSION,
        "project_id": "Sentigraph",
        "repository_identity": "dgmpurf/Sentigraph",
        "expected_origin_transport": "github_https",
        "expected_origin_repository": "dgmpurf/Sentigraph",
        "git_marker_kind": "ordinary_directory",
        "git_config_kind": "ordinary_file",
        "formal_target_logical_label": LOCKED_TARGET_LOGICAL_LABEL,
        "formal_receipt_logical_label": LOCKED_RECEIPT_LOGICAL_LABEL,
        "production_target": False,
        "generic_repository_allowed": False,
        "target_substitution_allowed": False,
    }
)
FORMAL_REPOSITORY_IDENTITY_SAFE_HASH: Final = (
    "66ae70377a33d036ab68729e7b9a6f509c7218cbbc6d40739e1ca5a755a2d82b"
)
FORMAL_EXECUTION_PROFILE_CONTRACT_SCHEMA: Final = (
    "sentigraph_formal_execution_profile_contract_v0_1"
)
FORMAL_EXECUTION_PROFILE_CONTRACT_VERSION: Final = "0.1"
FORMAL_EXECUTION_PROFILE_CONTRACT_PROJECTION: Final = MappingProxyType(
    {
        "contract_schema": FORMAL_EXECUTION_PROFILE_CONTRACT_SCHEMA,
        "contract_version": FORMAL_EXECUTION_PROFILE_CONTRACT_VERSION,
        "execution_profile": FORMAL_EXECUTION_PROFILE,
        "repository_identity_safe_hash": FORMAL_REPOSITORY_IDENTITY_SAFE_HASH,
        "target_identity_safe_hash": LOCKED_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "locked_target_logical_label": LOCKED_TARGET_LOGICAL_LABEL,
        "locked_receipt_logical_label": LOCKED_RECEIPT_LOGICAL_LABEL,
        "sqlite_session_maximum": 1,
        "automatic_retry": False,
        "second_attempt": False,
        "candidate_DML_allowed": False,
        "reservation_DML_allowed": False,
        "runtime_enumeration_allowed": False,
        "target_substitution_allowed": False,
        "separate_exact_human_approval_required": True,
        "formal_execution_disabled_by_default": True,
        "production_action_allowed": False,
    }
)
FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH: Final = (
    "5225ff83fd2de19cb32e26b831da410f51a162c32afc40be97d522f87d2137bf"
)
ATTEMPT_DDL_SAFE_HASH: Final = (
    "2881c0efdb35d79f4cda59f4919c4a159ade57a9d24e521ec8758e2bcf68b266"
)
PRIMARY_DDL_SAFE_HASH: Final = (
    "d44a6c46000b8c156b1367aae348be799e9a814d1328b686b2efc9e57cab7e26"
)
RECEIPT_SCHEMA: Final = (
    "sentigraph_governed_nonproduction_target_initialization_receipt_v0_2"
)
RECEIPT_VERSION: Final = "0.2"
_EXPECTED_FORMAL_ORIGIN: Final = (
    "https://github.com/"
    f"{FORMAL_REPOSITORY_IDENTITY_PROJECTION['repository_identity']}.git"
)
_FORMAL_ORIGIN_SECTION: Final = 'remote "origin"'
_MAX_GIT_CONFIG_BYTES: Final = 64 * 1024

PHASES: Final = (
    "validate_inputs",
    "verify_execution_profile",
    "verify_locked_governance",
    "verify_committed_DDL",
    "verify_formal_repository_identity",
    "derive_exact_paths",
    "verify_path_components",
    "verify_exact_collisions",
    "classify_preexistence",
    "create_exact_parents",
    "open_SQLite_session",
    "begin_schema_transaction",
    "initialize_attempt_schema",
    "initialize_primary_schema",
    "verify_schema",
    "verify_zero_rows",
    "run_integrity_check",
    "commit_initialization",
    "verify_post_commit_same_session",
    "close_SQLite_session",
    "verify_exact_post_connection_state",
    "build_receipt",
    "scan_receipt",
    "write_receipt",
    "readback_receipt",
    "evaluate_cleanup",
    "perform_cleanup",
    "completed",
    "terminal_failure",
)

SAFE_ERROR_CODES: Final = frozenset(
    {
        "none",
        "runner_disabled",
        "invalid_input",
        "invalid_execution_profile",
        "formal_execution_disabled",
        "formal_repository_identity_hash_mismatch",
        "formal_profile_contract_hash_mismatch",
        "formal_git_marker_invalid",
        "formal_git_config_invalid",
        "formal_origin_remote_invalid",
        "governance_identity_hash_mismatch",
        "governance_contract_hash_mismatch",
        "DDL_hash_mismatch",
        "unsafe_repository_root",
        "path_policy_failure",
        "path_escape",
        "symlink_or_reparse_point",
        "mount_device_boundary",
        "receipt_preexistence",
        "unsafe_target_collision",
        "ambiguous_sidecar",
        "target_preexistence_ambiguity",
        "parent_creation_failure",
        "SQLite_connect_failure",
        "transaction_begin_failure",
        "attempt_DDL_failure",
        "primary_DDL_failure",
        "schema_verification_failed",
        "unexpected_schema_object",
        "nonzero_candidate_rows",
        "nonzero_reservations",
        "integrity_failure",
        "known_commit_failure",
        "commit_ambiguity",
        "post_commit_verification_failure",
        "connection_close_failure",
        "post_connection_state_failure",
        "receipt_build_failure",
        "receipt_privacy_scan_failure",
        "receipt_exclusive_write_failure",
        "receipt_fsync_failure",
        "receipt_readback_failure",
        "receipt_hash_mismatch",
        "cleanup_evaluation_failure",
        "cleanup_failure",
        "injected_failure",
        "unexpected_internal_failure",
    }
)

FAILURE_INJECTION_PHASES: Final = frozenset(
    {
        "validate_inputs",
        "verify_locked_governance",
        "verify_committed_DDL",
        "derive_exact_paths",
        "verify_path_components",
        "verify_exact_collisions",
        "classify_preexistence",
        "create_exact_parents",
        "open_SQLite_session",
        "begin_schema_transaction",
        "initialize_attempt_schema",
        "initialize_primary_schema",
        "verify_schema",
        "verify_zero_rows",
        "run_integrity_check",
        "commit_known_failure",
        "commit_ambiguity",
        "verify_post_commit_same_session",
        "close_SQLite_session",
        "verify_exact_post_connection_state",
        "build_receipt",
        "scan_receipt",
        "write_receipt",
        "fsync_receipt",
        "readback_receipt",
        "verify_receipt_hash",
        "evaluate_cleanup",
        "perform_cleanup",
        "unexpected_internal_failure",
    }
)

_INJECTION_ERROR_CODES: Final = MappingProxyType(
    {
        "validate_inputs": "invalid_input",
        "verify_locked_governance": "injected_failure",
        "verify_committed_DDL": "DDL_hash_mismatch",
        "derive_exact_paths": "path_policy_failure",
        "verify_path_components": "path_policy_failure",
        "verify_exact_collisions": "target_preexistence_ambiguity",
        "classify_preexistence": "target_preexistence_ambiguity",
        "create_exact_parents": "parent_creation_failure",
        "open_SQLite_session": "SQLite_connect_failure",
        "begin_schema_transaction": "transaction_begin_failure",
        "initialize_attempt_schema": "attempt_DDL_failure",
        "initialize_primary_schema": "primary_DDL_failure",
        "verify_schema": "schema_verification_failed",
        "verify_zero_rows": "schema_verification_failed",
        "run_integrity_check": "integrity_failure",
        "verify_post_commit_same_session": "post_commit_verification_failure",
        "close_SQLite_session": "connection_close_failure",
        "verify_exact_post_connection_state": "post_connection_state_failure",
        "build_receipt": "receipt_build_failure",
        "scan_receipt": "receipt_privacy_scan_failure",
        "write_receipt": "receipt_exclusive_write_failure",
        "fsync_receipt": "receipt_fsync_failure",
        "readback_receipt": "receipt_readback_failure",
        "verify_receipt_hash": "receipt_hash_mismatch",
    }
)

_HASH_RE: Final = re.compile(r"^[0-9a-f]{64}$")
_DML_PREFIXES: Final = ("INSERT", "UPDATE", "DELETE", "REPLACE")
_SIDECAR_SUFFIXES: Final = ("-journal", "-wal", "-shm")
_EXPECTED_USER_TABLES: Final = frozenset({ATTEMPT_RESERVATION_TABLE, TABLE_NAME})
_EXPECTED_INTERNAL_AUTOINDEX_COUNT: Final = 6


class _SmokeFailure(RuntimeError):
    def __init__(self, safe_error_code: str) -> None:
        self.safe_error_code = safe_error_code
        super().__init__(safe_error_code)


class _CommitAmbiguity(_SmokeFailure):
    pass


def _base_result() -> dict[str, Any]:
    return {
        "result_schema": RESULT_SCHEMA,
        "result_version": RESULT_VERSION,
        "passed": False,
        "decision": "blocked",
        "privacy_issue_stop": False,
        "execution_mode": EXECUTION_MODE,
        "execution_profile_requested": "not_validated",
        "execution_profile_effective": "not_selected",
        "synthetic_profile_selected": False,
        "formal_profile_selected": False,
        "formal_execution_enabled": False,
        "formal_execution_guard_verified": False,
        "repository_identity_schema": FORMAL_REPOSITORY_IDENTITY_SCHEMA,
        "repository_identity_safe_hash_expected": (
            FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
        ),
        "repository_identity_safe_hash_verified": False,
        "formal_profile_contract_safe_hash_expected": (
            FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
        ),
        "formal_profile_contract_safe_hash_verified": False,
        "git_marker_check_started": False,
        "git_marker_verified": False,
        "git_config_check_started": False,
        "git_config_verified": False,
        "origin_remote_check_started": False,
        "origin_remote_verified": False,
        "formal_repository_identity_check_completed": False,
        "formal_repository_identity_check_passed": False,
        "generic_git_repository_accepted": False,
        "raw_origin_remote_exposed": False,
        "formal_target_path_derivation_authorized": False,
        "formal_target_path_derivation_started": False,
        "git_repository_root_passed_to_runner": False,
        "formal_repository_identity_verified": False,
        "runner_can_distinguish_actual_root_from_exact_fixture": False,
        "formal_target_path_derived": False,
        "formal_target_metadata_access_started": False,
        "formal_target_SQLite_open_attempted": False,
        "formal_target_SQLite_opened": False,
        "formal_receipt_path_derived": False,
        "formal_receipt_metadata_access_started": False,
        "formal_receipt_write_attempted": False,
        "formal_receipt_write_completed": False,
        "formal_receipt_readback_started": False,
        "formal_receipt_readback_completed": False,
        "formal_target_or_receipt_access_occurred": False,
        "external_human_authorization_evaluated_by_runner": False,
        "runner_grants_authorization": False,
        "runner_receipt_grants_authorization": False,
        "separate_exact_human_approval_required": True,
        "execution_phase": "validate_inputs",
        "terminal_phase": "not_completed",
        "safe_error_code": "none",
        "failure_injection_phase": "none",
        "target_initialization_outcome": "not_completed",
        "target_preexistence_classification": "not_started",
        "target_kind": TARGET_KIND,
        "target_logical_label": LOCKED_TARGET_LOGICAL_LABEL,
        "receipt_logical_label": LOCKED_RECEIPT_LOGICAL_LABEL,
        "target_identity_safe_hash_expected": LOCKED_TARGET_IDENTITY_SAFE_HASH,
        "target_identity_safe_hash_verified": False,
        "target_authorization_contract_safe_hash_expected": (
            LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "target_authorization_contract_safe_hash_verified": False,
        "attempt_DDL_safe_hash_expected": ATTEMPT_DDL_SAFE_HASH,
        "attempt_DDL_safe_hash_observed": "not_started",
        "primary_DDL_safe_hash_expected": PRIMARY_DDL_SAFE_HASH,
        "primary_DDL_safe_hash_observed": "not_started",
        "DDL_hashes_verified": False,
        "path_derivation_completed": False,
        "repository_root_verified_safe": False,
        "path_escape_check_passed": False,
        "symlink_check_passed": False,
        "junction_check_passed": False,
        "reparse_point_check_passed": False,
        "mount_boundary_check_passed": False,
        "exact_component_check_count": 0,
        "collision_checks_completed": False,
        "target_preexisted": "unknown",
        "receipt_preexisted": "unknown",
        "journal_sidecar_preexisted": "unknown",
        "WAL_sidecar_preexisted": "unknown",
        "SHM_sidecar_preexisted": "unknown",
        "target_created_by_this_run": False,
        "exact_parent_created_by_this_run": False,
        "parent_directory_create_count": 0,
        "existing_target_read_only": False,
        "existing_target_bytes_unchanged": "not_applicable",
        "initialization_attempt_limit": 1,
        "initialization_attempt_count": 0,
        "SQLite_connection_session_limit": 1,
        "SQLite_connection_open_count": 0,
        "SQLite_connection_reopen_count": 0,
        "SQLite_create_count": 0,
        "transaction_begin_count": 0,
        "schema_DDL_statement_count": 0,
        "commit_call_count": 0,
        "rollback_count": 0,
        "connection_close_count": 0,
        "successful_initialization_commit": False,
        "commit_outcome_ambiguous": False,
        "read_only_verification_completed": False,
        "candidate_table_DML_statement_count": 0,
        "attempt_table_DML_statement_count": 0,
        "other_user_DML_statement_count": 0,
        "schema_exact_conformance_verified": False,
        "target_primary_table_verified": False,
        "target_attempt_reservation_table_verified": False,
        "target_indexes_verified": False,
        "target_constraints_verified": False,
        "expected_user_table_count": 2,
        "observed_user_table_count": "not_available",
        "expected_internal_autoindex_count": _EXPECTED_INTERNAL_AUTOINDEX_COUNT,
        "observed_internal_autoindex_count": "not_available",
        "unexpected_user_schema_object_count": "not_available",
        "schema_inventory_safe_hash": "not_available",
        "base_record_row_count": "not_available",
        "attempt_reservation_row_count": "not_available",
        "zero_candidate_record_state_verified": False,
        "zero_attempt_reservation_state_verified": False,
        "integrity_check": "not_run",
        "integrity_result": "not_available",
        "post_commit_same_session_verified": False,
        "post_connection_state_verified": False,
        "cleanup_allowed_by_caller": False,
        "cleanup_eligible": False,
        "cleanup_attempted": False,
        "cleanup_performed": False,
        "cleanup_file_count": 0,
        "cleanup_directory_count": 0,
        "receipt_build_completed": False,
        "receipt_privacy_scan_executed": False,
        "receipt_privacy_scan_passed": False,
        "receipt_privacy_finding_count": "not_available",
        "receipt_exclusive_write_attempt_count": 0,
        "receipt_exclusive_write_performed": False,
        "receipt_write_completed": False,
        "receipt_fsync_performed": False,
        "receipt_readback_count": 0,
        "receipt_readback_verified": False,
        "receipt_hash_verified": False,
        "receipt_safe_hash": "not_created",
        "receipt_byte_sha256": "not_created",
        "final_target_exists": False,
        "final_target_regular_file": False,
        "final_receipt_exists": False,
        "final_receipt_regular_file": False,
        "final_journal_sidecar_exists": False,
        "final_WAL_sidecar_exists": False,
        "final_SHM_sidecar_exists": False,
        "final_sidecar_count": 0,
        "final_exact_target_parent_exists": False,
        "final_runtime_parent_exists": False,
        "automatic_retry": False,
        "second_attempt": False,
        "candidate_writer_called": False,
        "reservation_writer_called": False,
        "generic_store_used": False,
        "actual_Git_root_passed_to_runner": False,
        "formal_logical_target_accessed": False,
        "actual_runtime_enumerated": False,
        "formal_initialization_receipt_accessed": False,
        "protected_payload_read": False,
        "protected_capture_receipt_read": False,
        "source_or_package_read": False,
        "candidate_reconstructed": False,
        "gate_prepared": False,
        "gate_activated": False,
        "persistence_executed": False,
        "production_object_created": False,
        "network_called": False,
        "subprocess_called": False,
        "environment_target_override_used": False,
        "target_substitution_used": False,
        "fallback_used": False,
        "physical_path_exposed": False,
        "raw_exception_exposed": False,
        "raw_SQL_exposed": False,
        "raw_key_exposed": False,
        "raw_value_exposed": False,
        "value_free_diagnostics": True,
        "synthetic_temporary_repository_only": False,
        "synthetic_temporary_SQLite_only": False,
    }


RESULT_FIELDS: Final = frozenset(_base_result())


def run_governed_nonproduction_target_initialization_smoke(
    *,
    repository_root: Path,
    expected_target_identity_safe_hash: str,
    expected_target_authorization_contract_safe_hash: str,
    allow_same_run_empty_target_cleanup: bool,
    enabled: bool = False,
    execution_profile: str = SYNTHETIC_EXECUTION_PROFILE,
    expected_repository_identity_safe_hash: str | None = None,
    expected_formal_execution_profile_contract_safe_hash: str | None = None,
    formal_execution_enabled: bool = False,
    _failure_injection_phase: str | None = None,
) -> dict[str, Any]:
    """Run one bounded schema-only smoke under an explicit repository profile."""

    result = _base_result()
    known_profiles = {SYNTHETIC_EXECUTION_PROFILE, FORMAL_EXECUTION_PROFILE}
    result["execution_profile_requested"] = (
        execution_profile
        if isinstance(execution_profile, str) and execution_profile in known_profiles
        else "invalid"
    )
    result["formal_execution_enabled"] = (
        formal_execution_enabled if isinstance(formal_execution_enabled, bool) else False
    )
    result["cleanup_allowed_by_caller"] = (
        allow_same_run_empty_target_cleanup
        if isinstance(allow_same_run_empty_target_cleanup, bool)
        else False
    )
    result["failure_injection_phase"] = _failure_injection_phase or "none"
    paths: dict[str, Path] | None = None
    created_directories: list[Path] = []
    target_was_absent = False
    sidecars_were_absent = False
    connection: sqlite3.Connection | None = None
    operation_error: Exception | None = None
    existing_target_before_hash: str | None = None

    def enter(phase: str) -> None:
        result["execution_phase"] = phase

    try:
        enter("validate_inputs")
        if _failure_injection_phase not in FAILURE_INJECTION_PHASES | {None}:
            raise _SmokeFailure("invalid_input")
        if _failure_injection_phase == "unexpected_internal_failure":
            raise RuntimeError("bounded synthetic internal failure")
        if not isinstance(repository_root, Path):
            raise _SmokeFailure("invalid_input")
        if not isinstance(allow_same_run_empty_target_cleanup, bool):
            raise _SmokeFailure("invalid_input")
        if not isinstance(enabled, bool):
            raise _SmokeFailure("invalid_input")
        if not isinstance(formal_execution_enabled, bool):
            raise _SmokeFailure("invalid_input")
        if not isinstance(execution_profile, str) or execution_profile not in known_profiles:
            raise _SmokeFailure("invalid_execution_profile")
        result["execution_profile_effective"] = execution_profile
        result["synthetic_profile_selected"] = (
            execution_profile == SYNTHETIC_EXECUTION_PROFILE
        )
        result["formal_profile_selected"] = (
            execution_profile == FORMAL_EXECUTION_PROFILE
        )
        if not enabled:
            raise _SmokeFailure("runner_disabled")
        _inject("validate_inputs", _failure_injection_phase)

        enter("verify_execution_profile")
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            if not formal_execution_enabled:
                raise _SmokeFailure("formal_execution_disabled")
            if (
                not _is_hash(expected_repository_identity_safe_hash)
                or expected_repository_identity_safe_hash
                != FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
            ):
                raise _SmokeFailure("formal_repository_identity_hash_mismatch")
            result["repository_identity_safe_hash_verified"] = True
            if (
                not _is_hash(expected_formal_execution_profile_contract_safe_hash)
                or expected_formal_execution_profile_contract_safe_hash
                != FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
            ):
                raise _SmokeFailure("formal_profile_contract_hash_mismatch")
            result["formal_profile_contract_safe_hash_verified"] = True
            result["formal_execution_guard_verified"] = True

        enter("verify_locked_governance")
        if not _is_hash(expected_target_identity_safe_hash):
            raise _SmokeFailure("invalid_input")
        if not _is_hash(expected_target_authorization_contract_safe_hash):
            raise _SmokeFailure("invalid_input")
        if expected_target_identity_safe_hash != LOCKED_TARGET_IDENTITY_SAFE_HASH:
            raise _SmokeFailure("governance_identity_hash_mismatch")
        result["target_identity_safe_hash_verified"] = True
        if (
            expected_target_authorization_contract_safe_hash
            != LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ):
            raise _SmokeFailure("governance_contract_hash_mismatch")
        result["target_authorization_contract_safe_hash_verified"] = True
        _inject("verify_locked_governance", _failure_injection_phase)

        enter("verify_committed_DDL")
        attempt_hash = _sha256_bytes(_CREATE_ATTEMPT_RESERVATION_TABLE_SQL.encode("utf-8"))
        primary_hash = _sha256_bytes(_CREATE_TABLE_SQL.encode("utf-8"))
        result["attempt_DDL_safe_hash_observed"] = attempt_hash
        result["primary_DDL_safe_hash_observed"] = primary_hash
        if attempt_hash != ATTEMPT_DDL_SAFE_HASH or primary_hash != PRIMARY_DDL_SAFE_HASH:
            raise _SmokeFailure("DDL_hash_mismatch")
        result["DDL_hashes_verified"] = True
        _inject("verify_committed_DDL", _failure_injection_phase)

        if execution_profile == FORMAL_EXECUTION_PROFILE:
            enter("verify_formal_repository_identity")
            _verify_formal_repository_identity(repository_root, result)
            result["formal_target_path_derivation_authorized"] = True

        enter("derive_exact_paths")
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_target_path_derivation_started"] = True
        _inject("derive_exact_paths", _failure_injection_phase)
        paths = _derive_exact_paths(repository_root)
        result["path_derivation_completed"] = True
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_target_path_derived"] = True
            result["formal_receipt_path_derived"] = True

        enter("verify_path_components")
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_target_metadata_access_started"] = True
            result["formal_receipt_metadata_access_started"] = True
            result["formal_target_or_receipt_access_occurred"] = True
            result["formal_logical_target_accessed"] = True
            result["formal_initialization_receipt_accessed"] = True
        _verify_path_components(paths, result, execution_profile)
        _inject("verify_path_components", _failure_injection_phase)

        enter("verify_exact_collisions")
        target_state, receipt_state, sidecar_states = _verify_exact_collisions(
            paths,
            result,
        )
        target_was_absent = target_state == "absent"
        sidecars_were_absent = all(state == "absent" for state in sidecar_states.values())
        _inject("verify_exact_collisions", _failure_injection_phase)

        enter("classify_preexistence")
        if target_state == "absent":
            result["target_preexistence_classification"] = "absent"
            result["target_preexisted"] = False
        elif target_state == "file":
            result["target_preexistence_classification"] = "existing_regular_file"
            result["target_preexisted"] = True
            result["existing_target_read_only"] = True
            existing_target_before_hash = _sha256_file(paths["target"])
        else:
            raise _SmokeFailure("target_preexistence_ambiguity")
        result["receipt_preexisted"] = receipt_state != "absent"
        _inject("classify_preexistence", _failure_injection_phase)

        if target_was_absent:
            enter("create_exact_parents")
            created_directories = _create_exact_parents(paths, result)
            _inject("create_exact_parents", _failure_injection_phase)

        if _failure_injection_phase in {"evaluate_cleanup", "perform_cleanup"}:
            _failure_injection_phase_for_SQL = "initialize_attempt_schema"
        else:
            _failure_injection_phase_for_SQL = _failure_injection_phase

        try:
            enter("open_SQLite_session")
            _inject("open_SQLite_session", _failure_injection_phase_for_SQL)
            result["initialization_attempt_count"] = 1
            if execution_profile == FORMAL_EXECUTION_PROFILE:
                result["formal_target_SQLite_open_attempted"] = True
            connection = _open_one_connection(paths["target"], target_was_absent)
            result["SQLite_connection_open_count"] = 1
            if execution_profile == FORMAL_EXECUTION_PROFILE:
                result["formal_target_SQLite_opened"] = True
            if target_was_absent:
                result["SQLite_create_count"] = 1
                result["target_created_by_this_run"] = True
            connection.row_factory = sqlite3.Row
            connection.set_trace_callback(lambda statement: _count_DML(statement, result))

            if target_was_absent:
                enter("begin_schema_transaction")
                _inject("begin_schema_transaction", _failure_injection_phase_for_SQL)
                try:
                    connection.execute("BEGIN IMMEDIATE")
                except sqlite3.Error as exc:
                    raise _SmokeFailure("transaction_begin_failure") from exc
                result["transaction_begin_count"] = 1

                enter("initialize_attempt_schema")
                _inject("initialize_attempt_schema", _failure_injection_phase_for_SQL)
                try:
                    connection.execute(_CREATE_ATTEMPT_RESERVATION_TABLE_SQL)
                except sqlite3.Error as exc:
                    raise _SmokeFailure("attempt_DDL_failure") from exc
                result["schema_DDL_statement_count"] = 1

                enter("initialize_primary_schema")
                _inject("initialize_primary_schema", _failure_injection_phase_for_SQL)
                try:
                    connection.execute(_CREATE_TABLE_SQL)
                except sqlite3.Error as exc:
                    raise _SmokeFailure("primary_DDL_failure") from exc
                result["schema_DDL_statement_count"] = 2
            else:
                try:
                    connection.execute("PRAGMA query_only = ON")
                except sqlite3.Error as exc:
                    raise _SmokeFailure("SQLite_connect_failure") from exc

            enter("verify_schema")
            _inject("verify_schema", _failure_injection_phase_for_SQL)
            _verify_schema(connection, result)

            enter("verify_zero_rows")
            _inject("verify_zero_rows", _failure_injection_phase_for_SQL)
            _verify_zero_rows(connection, result)

            enter("run_integrity_check")
            _inject("run_integrity_check", _failure_injection_phase_for_SQL)
            _verify_integrity(connection, result)

            if target_was_absent:
                enter("commit_initialization")
                result["commit_call_count"] = 1
                if _failure_injection_phase == "commit_known_failure":
                    try:
                        connection.rollback()
                    finally:
                        result["rollback_count"] = 1
                    raise _SmokeFailure("known_commit_failure")
                try:
                    connection.commit()
                except sqlite3.Error as exc:
                    try:
                        connection.rollback()
                    finally:
                        result["rollback_count"] = 1
                    raise _SmokeFailure("known_commit_failure") from exc
                if _failure_injection_phase == "commit_ambiguity":
                    result["commit_outcome_ambiguous"] = True
                    raise _CommitAmbiguity("commit_ambiguity")
                result["successful_initialization_commit"] = True

                enter("verify_post_commit_same_session")
                _inject(
                    "verify_post_commit_same_session",
                    _failure_injection_phase_for_SQL,
                )
                _verify_schema(connection, result)
                _verify_zero_rows(connection, result)
                _verify_integrity(connection, result)
                result["post_commit_same_session_verified"] = True
                result["target_initialization_outcome"] = "initialized_exact_empty_target"
            else:
                result["read_only_verification_completed"] = True
                result["target_initialization_outcome"] = (
                    "verified_existing_exact_empty_target_read_only"
                )
        except Exception as exc:
            operation_error = exc
        finally:
            if connection is not None:
                result["execution_phase"] = "close_SQLite_session"
                if (
                    operation_error is not None
                    and connection.in_transaction
                    and not result["commit_outcome_ambiguous"]
                    and result["rollback_count"] == 0
                ):
                    try:
                        connection.rollback()
                        result["rollback_count"] = 1
                    except sqlite3.Error:
                        operation_error = _SmokeFailure("known_commit_failure")
                try:
                    connection.close()
                    result["connection_close_count"] = 1
                except sqlite3.Error:
                    operation_error = _SmokeFailure("connection_close_failure")
                connection = None
                if (
                    operation_error is None
                    and _failure_injection_phase == "close_SQLite_session"
                ):
                    operation_error = _SmokeFailure("connection_close_failure")
        if operation_error is not None:
            raise operation_error

        enter("verify_exact_post_connection_state")
        _inject("verify_exact_post_connection_state", _failure_injection_phase)
        _refresh_exact_final_state(paths, result)
        if not result["final_target_exists"] or not result["final_target_regular_file"]:
            raise _SmokeFailure("post_connection_state_failure")
        if result["final_sidecar_count"] != 0:
            raise _SmokeFailure("post_connection_state_failure")
        if not target_was_absent:
            result["existing_target_bytes_unchanged"] = (
                _sha256_file(paths["target"]) == existing_target_before_hash
            )
            if result["existing_target_bytes_unchanged"] is not True:
                raise _SmokeFailure("post_connection_state_failure")
        result["post_connection_state_verified"] = True

        enter("build_receipt")
        _inject("build_receipt", _failure_injection_phase)
        receipt = _build_receipt(result)
        result["receipt_build_completed"] = True

        enter("scan_receipt")
        _inject("scan_receipt", _failure_injection_phase)
        scan = scan_protected_value_boundary(
            receipt,
            profile=SAFE_CAPTURE_RECEIPT_PROFILE,
        )
        result["receipt_privacy_scan_executed"] = True
        result["receipt_privacy_finding_count"] = scan["finding_count"]
        result["receipt_privacy_scan_passed"] = (
            scan["passed"] is True
            and scan["finding_count"] == 0
            and scan["protected_value_exposed"] is False
            and scan["raw_key_echoed"] is False
            and scan["raw_value_echoed"] is False
        )
        if not result["receipt_privacy_scan_passed"]:
            raise _SmokeFailure("receipt_privacy_scan_failure")

        enter("write_receipt")
        receipt_bytes = _canonical_json_bytes(receipt)
        result["receipt_exclusive_write_attempt_count"] = 1
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_receipt_write_attempted"] = True
        _inject("write_receipt", _failure_injection_phase)
        try:
            with paths["receipt"].open("xb") as handle:
                result["receipt_exclusive_write_performed"] = True
                handle.write(receipt_bytes)
                handle.flush()
                _inject("fsync_receipt", _failure_injection_phase)
                os.fsync(handle.fileno())
                result["receipt_fsync_performed"] = True
                result["receipt_write_completed"] = True
                if execution_profile == FORMAL_EXECUTION_PROFILE:
                    result["formal_receipt_write_completed"] = True
        except FileExistsError as exc:
            raise _SmokeFailure("receipt_preexistence") from exc
        except _SmokeFailure:
            raise
        except OSError as exc:
            raise _SmokeFailure("receipt_exclusive_write_failure") from exc

        enter("readback_receipt")
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_receipt_readback_started"] = True
        _inject("readback_receipt", _failure_injection_phase)
        try:
            readback_bytes = paths["receipt"].read_bytes()
            result["receipt_readback_count"] = 1
            readback = json.loads(readback_bytes.decode("utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise _SmokeFailure("receipt_readback_failure") from exc
        if readback != receipt:
            raise _SmokeFailure("receipt_readback_failure")
        result["receipt_readback_verified"] = True
        if execution_profile == FORMAL_EXECUTION_PROFILE:
            result["formal_receipt_readback_completed"] = True

        _inject("verify_receipt_hash", _failure_injection_phase)
        readback_without_hash = dict(readback)
        observed_safe_hash = readback_without_hash.pop("receipt_safe_hash", None)
        expected_safe_hash = _sha256_bytes(_canonical_json_bytes(readback_without_hash))
        if observed_safe_hash != expected_safe_hash:
            raise _SmokeFailure("receipt_hash_mismatch")
        result["receipt_safe_hash"] = expected_safe_hash
        result["receipt_byte_sha256"] = _sha256_bytes(readback_bytes)
        result["receipt_hash_verified"] = True

        _refresh_exact_final_state(paths, result)
        if not result["final_receipt_exists"] or not result["final_receipt_regular_file"]:
            raise _SmokeFailure("post_connection_state_failure")

        enter("completed")
        result["passed"] = True
        result["decision"] = "ready"
        result["terminal_phase"] = "completed"
        result["safe_error_code"] = "none"
        result["synthetic_temporary_repository_only"] = (
            execution_profile == SYNTHETIC_EXECUTION_PROFILE
        )
        result["synthetic_temporary_SQLite_only"] = (
            execution_profile == SYNTHETIC_EXECUTION_PROFILE
        )
        return result
    except _SmokeFailure as exc:
        result["safe_error_code"] = exc.safe_error_code
        result["decision"] = "needs_fix" if _paths_or_SQL_started(result) else "blocked"
    except Exception:
        result["safe_error_code"] = "unexpected_internal_failure"
        result["decision"] = "needs_fix" if _paths_or_SQL_started(result) else "blocked"

    if paths is not None:
        try:
            if (
                target_was_absent
                and not result["target_created_by_this_run"]
                and _path_state(paths["target"]) == "file"
            ):
                result["target_created_by_this_run"] = True
            _evaluate_and_perform_cleanup(
                paths=paths,
                result=result,
                created_directories=created_directories,
                target_was_absent=target_was_absent,
                sidecars_were_absent=sidecars_were_absent,
                failure_injection_phase=_failure_injection_phase,
            )
            _refresh_exact_final_state(paths, result)
        except Exception:
            result["safe_error_code"] = "cleanup_failure"
            result["decision"] = "needs_fix"
    result["terminal_phase"] = "terminal_failure"
    result["synthetic_temporary_repository_only"] = (
        execution_profile == SYNTHETIC_EXECUTION_PROFILE
        and result["repository_root_verified_safe"] is True
    )
    result["synthetic_temporary_SQLite_only"] = (
        execution_profile == SYNTHETIC_EXECUTION_PROFILE
        and result["SQLite_connection_open_count"] <= 1
        and result["actual_Git_root_passed_to_runner"] is False
    )
    return result


def _verify_formal_repository_identity(
    repository_root: Path,
    result: dict[str, Any],
) -> None:
    result["git_marker_check_started"] = True
    try:
        if _path_state(repository_root) != "directory":
            raise _SmokeFailure("formal_git_marker_invalid")
        try:
            root_status = repository_root.lstat()
        except OSError as exc:
            raise _SmokeFailure("formal_git_marker_invalid") from exc
        if _is_reparse(root_status):
            raise _SmokeFailure("formal_git_marker_invalid")

        git_marker = repository_root / ".git"
        if _path_state(git_marker) != "directory":
            raise _SmokeFailure("formal_git_marker_invalid")
        try:
            git_status = git_marker.lstat()
        except OSError as exc:
            raise _SmokeFailure("formal_git_marker_invalid") from exc
        if _is_reparse(git_status):
            raise _SmokeFailure("formal_git_marker_invalid")
        if git_status.st_dev != root_status.st_dev:
            raise _SmokeFailure("mount_device_boundary")
        result["git_marker_verified"] = True
        result["git_repository_root_passed_to_runner"] = True
        result["actual_Git_root_passed_to_runner"] = True

        result["git_config_check_started"] = True
        git_config = git_marker / "config"
        if _path_state(git_config) != "file":
            raise _SmokeFailure("formal_git_config_invalid")
        try:
            config_status = git_config.lstat()
        except OSError as exc:
            raise _SmokeFailure("formal_git_config_invalid") from exc
        if _is_reparse(config_status):
            raise _SmokeFailure("formal_git_config_invalid")
        if config_status.st_dev != root_status.st_dev:
            raise _SmokeFailure("mount_device_boundary")
        if config_status.st_size > _MAX_GIT_CONFIG_BYTES:
            raise _SmokeFailure("formal_git_config_invalid")
        try:
            config_text = git_config.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise _SmokeFailure("formal_git_config_invalid") from exc

        parser = configparser.RawConfigParser(interpolation=None, strict=True)
        parser.optionxform = str
        try:
            parser.read_string(config_text, source="bounded_git_config")
        except configparser.Error as exc:
            raise _SmokeFailure("formal_git_config_invalid") from exc
        result["git_config_verified"] = True

        result["origin_remote_check_started"] = True
        origin_like_sections = [
            section
            for section in parser.sections()
            if section.casefold() == _FORMAL_ORIGIN_SECTION.casefold()
        ]
        if origin_like_sections != [_FORMAL_ORIGIN_SECTION]:
            raise _SmokeFailure("formal_origin_remote_invalid")
        if any(
            key.casefold() in {"url", "pushurl"}
            for key in parser.defaults()
        ):
            raise _SmokeFailure("formal_origin_remote_invalid")
        origin_items = parser.items(_FORMAL_ORIGIN_SECTION, raw=True)
        origin_url_items = [
            (key, value)
            for key, value in origin_items
            if key.casefold() in {"url", "pushurl"}
        ]
        if len(origin_url_items) != 1 or origin_url_items[0][0] != "url":
            raise _SmokeFailure("formal_origin_remote_invalid")
        if origin_url_items[0][1] != _EXPECTED_FORMAL_ORIGIN:
            raise _SmokeFailure("formal_origin_remote_invalid")

        result["origin_remote_verified"] = True
        result["formal_repository_identity_check_passed"] = True
        result["formal_repository_identity_verified"] = True
    finally:
        result["formal_repository_identity_check_completed"] = True


def _derive_exact_paths(repository_root: Path) -> dict[str, Path]:
    target_label = PurePosixPath(LOCKED_TARGET_LOGICAL_LABEL)
    receipt_label = PurePosixPath(LOCKED_RECEIPT_LOGICAL_LABEL)
    for label in (target_label, receipt_label):
        if label.is_absolute() or ".." in label.parts or not label.parts:
            raise _SmokeFailure("path_policy_failure")
        if any(":" in part or "\\" in part for part in label.parts):
            raise _SmokeFailure("path_policy_failure")
    root = repository_root
    return {
        "root": root,
        "runtime_parent": root / target_label.parts[0],
        "target_parent": root.joinpath(*target_label.parts[:-1]),
        "target": root.joinpath(*target_label.parts),
        "receipt": root.joinpath(*receipt_label.parts),
        "journal": Path(str(root.joinpath(*target_label.parts)) + "-journal"),
        "wal": Path(str(root.joinpath(*target_label.parts)) + "-wal"),
        "shm": Path(str(root.joinpath(*target_label.parts)) + "-shm"),
    }


def _verify_path_components(
    paths: dict[str, Path],
    result: dict[str, Any],
    execution_profile: str,
) -> None:
    root = paths["root"]
    root_state = _path_state(root)
    if root_state != "directory":
        raise _SmokeFailure("unsafe_repository_root")
    if execution_profile == SYNTHETIC_EXECUTION_PROFILE:
        if _path_state(root / ".git") != "absent":
            result["actual_Git_root_passed_to_runner"] = True
            raise _SmokeFailure("unsafe_repository_root")
    elif not result["formal_repository_identity_check_passed"]:
        raise _SmokeFailure("formal_git_marker_invalid")
    root_status = root.lstat()
    if _is_reparse(root_status):
        raise _SmokeFailure("symlink_or_reparse_point")
    root_resolved = root.resolve(strict=True)
    target_resolved = paths["target"].resolve(strict=False)
    receipt_resolved = paths["receipt"].resolve(strict=False)
    if root_resolved not in target_resolved.parents or root_resolved not in receipt_resolved.parents:
        raise _SmokeFailure("path_escape")

    checked = 1
    for component in (
        paths["runtime_parent"],
        paths["target_parent"],
        paths["target"],
        paths["receipt"],
        paths["journal"],
        paths["wal"],
        paths["shm"],
    ):
        state = _path_state(component)
        if state in {"symlink", "reparse"}:
            raise _SmokeFailure("symlink_or_reparse_point")
        if state != "absent":
            checked += 1
            status = component.lstat()
            if status.st_dev != root_status.st_dev:
                raise _SmokeFailure("mount_device_boundary")
    result["exact_component_check_count"] = checked
    result["repository_root_verified_safe"] = True
    result["path_escape_check_passed"] = True
    result["symlink_check_passed"] = True
    result["junction_check_passed"] = True
    result["reparse_point_check_passed"] = True
    result["mount_boundary_check_passed"] = True


def _verify_exact_collisions(
    paths: dict[str, Path],
    result: dict[str, Any],
) -> tuple[str, str, dict[str, str]]:
    target_state = _path_state(paths["target"])
    receipt_state = _path_state(paths["receipt"])
    sidecar_states = {
        "journal": _path_state(paths["journal"]),
        "wal": _path_state(paths["wal"]),
        "shm": _path_state(paths["shm"]),
    }
    result["receipt_preexisted"] = receipt_state != "absent"
    result["journal_sidecar_preexisted"] = sidecar_states["journal"] != "absent"
    result["WAL_sidecar_preexisted"] = sidecar_states["wal"] != "absent"
    result["SHM_sidecar_preexisted"] = sidecar_states["shm"] != "absent"
    if receipt_state != "absent":
        raise _SmokeFailure("receipt_preexistence")
    if target_state in {"symlink", "reparse"}:
        raise _SmokeFailure("symlink_or_reparse_point")
    if target_state not in {"absent", "file"}:
        raise _SmokeFailure("unsafe_target_collision")
    if any(state != "absent" for state in sidecar_states.values()):
        raise _SmokeFailure("ambiguous_sidecar")
    result["collision_checks_completed"] = True
    return target_state, receipt_state, sidecar_states


def _create_exact_parents(
    paths: dict[str, Path],
    result: dict[str, Any],
) -> list[Path]:
    created: list[Path] = []
    root_status = paths["root"].lstat()
    for parent in (paths["runtime_parent"], paths["target_parent"]):
        state = _path_state(parent)
        if state == "absent":
            try:
                parent.mkdir()
            except OSError as exc:
                raise _SmokeFailure("parent_creation_failure") from exc
            created.append(parent)
            result["parent_directory_create_count"] += 1
        elif state != "directory":
            raise _SmokeFailure("path_policy_failure")
        status = parent.lstat()
        if _is_reparse(status):
            raise _SmokeFailure("symlink_or_reparse_point")
        if status.st_dev != root_status.st_dev:
            raise _SmokeFailure("mount_device_boundary")
    result["exact_parent_created_by_this_run"] = bool(created)
    return created


def _open_one_connection(target: Path, create: bool) -> sqlite3.Connection:
    try:
        if create:
            return sqlite3.connect(str(target))
        return sqlite3.connect(f"{target.resolve().as_uri()}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise _SmokeFailure("SQLite_connect_failure") from exc


def _verify_schema(connection: sqlite3.Connection, result: dict[str, Any]) -> None:
    try:
        rows = connection.execute(
            "SELECT type, name, tbl_name, sql FROM sqlite_master ORDER BY type, name"
        ).fetchall()
    except sqlite3.Error as exc:
        raise _SmokeFailure("schema_verification_failed") from exc

    user_tables = {
        row["name"]
        for row in rows
        if row["type"] == "table" and not row["name"].startswith("sqlite_")
    }
    named_indexes = [
        row for row in rows if row["type"] == "index" and row["sql"] is not None
    ]
    internal_indexes = [
        row for row in rows if row["type"] == "index" and row["sql"] is None
    ]
    triggers = [row for row in rows if row["type"] == "trigger"]
    views = [row for row in rows if row["type"] == "view"]
    unexpected_count = (
        len(user_tables - _EXPECTED_USER_TABLES)
        + len(named_indexes)
        + len(triggers)
        + len(views)
    )
    result["observed_user_table_count"] = len(user_tables)
    result["observed_internal_autoindex_count"] = len(internal_indexes)
    result["unexpected_user_schema_object_count"] = unexpected_count
    if unexpected_count:
        raise _SmokeFailure("unexpected_schema_object")
    if user_tables != _EXPECTED_USER_TABLES:
        raise _SmokeFailure("schema_verification_failed")
    if len(internal_indexes) != _EXPECTED_INTERNAL_AUTOINDEX_COUNT:
        raise _SmokeFailure("schema_verification_failed")

    table_SQL = {
        row["name"]: row["sql"]
        for row in rows
        if row["type"] == "table" and row["name"] in _EXPECTED_USER_TABLES
    }
    expected_hashes = {
        ATTEMPT_RESERVATION_TABLE: _normalized_DDL_hash(
            _CREATE_ATTEMPT_RESERVATION_TABLE_SQL
        ),
        TABLE_NAME: _normalized_DDL_hash(_CREATE_TABLE_SQL),
    }
    observed_hashes = {
        name: _normalized_DDL_hash(table_SQL.get(name))
        for name in _EXPECTED_USER_TABLES
    }
    if observed_hashes != expected_hashes:
        raise _SmokeFailure("schema_verification_failed")

    expected_column_counts = {
        ATTEMPT_RESERVATION_TABLE: 19,
        TABLE_NAME: 39,
    }
    foreign_key_count = 0
    for table, expected_count in expected_column_counts.items():
        try:
            columns = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
            foreign_keys = connection.execute(
                f'PRAGMA foreign_key_list("{table}")'
            ).fetchall()
        except sqlite3.Error as exc:
            raise _SmokeFailure("schema_verification_failed") from exc
        if len(columns) != expected_count:
            raise _SmokeFailure("schema_verification_failed")
        foreign_key_count += len(foreign_keys)
    if foreign_key_count != 0:
        raise _SmokeFailure("schema_verification_failed")

    projection = {
        "autoindex_count": len(internal_indexes),
        "foreign_key_count": foreign_key_count,
        "named_index_count": len(named_indexes),
        "table_DDL_hashes": observed_hashes,
        "table_names": sorted(user_tables),
        "trigger_count": len(triggers),
        "view_count": len(views),
    }
    result["schema_inventory_safe_hash"] = _sha256_bytes(_canonical_json_bytes(projection))
    result["schema_exact_conformance_verified"] = True
    result["target_primary_table_verified"] = True
    result["target_attempt_reservation_table_verified"] = True
    result["target_indexes_verified"] = True
    result["target_constraints_verified"] = True


def _verify_zero_rows(connection: sqlite3.Connection, result: dict[str, Any]) -> None:
    try:
        base_count = int(
            connection.execute(f'SELECT COUNT(*) FROM "{TABLE_NAME}"').fetchone()[0]
        )
        attempt_count = int(
            connection.execute(
                f'SELECT COUNT(*) FROM "{ATTEMPT_RESERVATION_TABLE}"'
            ).fetchone()[0]
        )
    except (sqlite3.Error, TypeError, ValueError) as exc:
        raise _SmokeFailure("schema_verification_failed") from exc
    result["base_record_row_count"] = base_count
    result["attempt_reservation_row_count"] = attempt_count
    if base_count != 0:
        raise _SmokeFailure("nonzero_candidate_rows")
    if attempt_count != 0:
        raise _SmokeFailure("nonzero_reservations")
    result["zero_candidate_record_state_verified"] = True
    result["zero_attempt_reservation_state_verified"] = True


def _verify_integrity(connection: sqlite3.Connection, result: dict[str, Any]) -> None:
    try:
        rows = connection.execute("PRAGMA quick_check").fetchall()
    except sqlite3.Error as exc:
        raise _SmokeFailure("integrity_failure") from exc
    result["integrity_check"] = "quick_check"
    if len(rows) != 1 or rows[0][0] != "ok":
        result["integrity_result"] = "failed"
        raise _SmokeFailure("integrity_failure")
    result["integrity_result"] = "ok"


def _build_receipt(result: dict[str, Any]) -> dict[str, Any]:
    formal_receipt_completion_claim = bool(
        result["formal_profile_selected"]
        and result["formal_execution_guard_verified"]
        and result["formal_repository_identity_verified"]
        and result["formal_target_SQLite_opened"]
        and result["formal_receipt_metadata_access_started"]
    )
    # These assertions are valid only after the exact bytes pass fsync and readback.
    receipt = {
        "receipt_schema": RECEIPT_SCHEMA,
        "receipt_version": RECEIPT_VERSION,
        "result_schema": RESULT_SCHEMA,
        "execution_profile": result["execution_profile_effective"],
        "formal_execution_guard_verified": result[
            "formal_execution_guard_verified"
        ],
        "repository_identity_safe_hash": (
            FORMAL_REPOSITORY_IDENTITY_SAFE_HASH
            if result["formal_repository_identity_verified"]
            else "not_applicable"
        ),
        "formal_execution_profile_contract_safe_hash": (
            FORMAL_EXECUTION_PROFILE_CONTRACT_SAFE_HASH
            if result["formal_execution_guard_verified"]
            else "not_applicable"
        ),
        "git_repository_root_passed_to_runner": result[
            "git_repository_root_passed_to_runner"
        ],
        "formal_target_metadata_access_started": result[
            "formal_target_metadata_access_started"
        ],
        "formal_target_SQLite_opened": result["formal_target_SQLite_opened"],
        "formal_receipt_write_completed": formal_receipt_completion_claim,
        "formal_receipt_readback_completed": formal_receipt_completion_claim,
        "separate_exact_human_approval_required": True,
        "external_human_authorization_evaluated_by_runner": False,
        "runner_grants_authorization": False,
        "receipt_grants_authorization": False,
        "target_kind": TARGET_KIND,
        "target_identity_safe_hash": LOCKED_TARGET_IDENTITY_SAFE_HASH,
        "target_authorization_contract_safe_hash": (
            LOCKED_TARGET_AUTHORIZATION_CONTRACT_SAFE_HASH
        ),
        "target_logical_label": LOCKED_TARGET_LOGICAL_LABEL,
        "receipt_logical_label": LOCKED_RECEIPT_LOGICAL_LABEL,
        "target_preexistence_classification": result[
            "target_preexistence_classification"
        ],
        "target_initialization_outcome": result["target_initialization_outcome"],
        "path_and_symlink_checks_passed": (
            result["path_escape_check_passed"]
            and result["symlink_check_passed"]
            and result["reparse_point_check_passed"]
        ),
        "SQLite_connection_open_count": result["SQLite_connection_open_count"],
        "SQLite_connection_reopen_count": result["SQLite_connection_reopen_count"],
        "schema_DDL_statement_count": result["schema_DDL_statement_count"],
        "schema_exact_conformance_verified": result[
            "schema_exact_conformance_verified"
        ],
        "schema_inventory_safe_hash": result["schema_inventory_safe_hash"],
        "base_record_row_count": result["base_record_row_count"],
        "attempt_reservation_row_count": result["attempt_reservation_row_count"],
        "integrity_result": result["integrity_result"],
        "candidate_table_DML_statement_count": result[
            "candidate_table_DML_statement_count"
        ],
        "attempt_table_DML_statement_count": result[
            "attempt_table_DML_statement_count"
        ],
        "other_user_DML_statement_count": result["other_user_DML_statement_count"],
        "cleanup_performed": False,
        "raw_row_retained": False,
        "raw_author_identity_retained": False,
        "absolute_path_recorded": False,
        "production_object_created": False,
        "network_called": False,
        "gate_activated": False,
        "persistence_mutation_performed": False,
        "directory_enumeration_performed": False,
        "alternate_source_used": False,
        "protected_payload_read": False,
        "protected_capture_receipt_read": False,
        "source_or_package_read": False,
        "candidate_reconstructed": False,
        "candidate_writer_called": False,
        "reservation_writer_called": False,
        "automatic_retry": False,
        "target_substitution_used": False,
        "fallback_used": False,
        "human_review_required": True,
        "MVP_F07_eligible": False,
    }
    receipt["receipt_safe_hash"] = _sha256_bytes(_canonical_json_bytes(receipt))
    return receipt


def _evaluate_and_perform_cleanup(
    *,
    paths: dict[str, Path],
    result: dict[str, Any],
    created_directories: list[Path],
    target_was_absent: bool,
    sidecars_were_absent: bool,
    failure_injection_phase: str | None,
) -> None:
    result["execution_phase"] = "evaluate_cleanup"
    if failure_injection_phase == "evaluate_cleanup":
        result["safe_error_code"] = "cleanup_evaluation_failure"
        result["decision"] = "needs_fix"
        return
    eligible = (
        result["cleanup_allowed_by_caller"] is True
        and target_was_absent
        and (
            result["target_created_by_this_run"] is True
            or result["exact_parent_created_by_this_run"] is True
        )
        and result["successful_initialization_commit"] is False
        and result["commit_outcome_ambiguous"] is False
        and result["candidate_table_DML_statement_count"] == 0
        and result["attempt_table_DML_statement_count"] == 0
        and result["other_user_DML_statement_count"] == 0
        and result["receipt_hash_verified"] is False
        and sidecars_were_absent
    )
    result["cleanup_eligible"] = eligible
    if not eligible:
        return
    result["execution_phase"] = "perform_cleanup"
    result["cleanup_attempted"] = True
    if failure_injection_phase == "perform_cleanup":
        result["safe_error_code"] = "cleanup_failure"
        result["decision"] = "needs_fix"
        return
    try:
        for sidecar in (paths["journal"], paths["wal"], paths["shm"]):
            if _path_state(sidecar) == "file":
                sidecar.unlink()
                result["cleanup_file_count"] += 1
        if _path_state(paths["target"]) == "file":
            paths["target"].unlink()
            result["cleanup_file_count"] += 1
        for directory in reversed(created_directories):
            if _path_state(directory) == "directory":
                directory.rmdir()
                result["cleanup_directory_count"] += 1
        result["cleanup_performed"] = True
    except OSError:
        result["safe_error_code"] = "cleanup_failure"
        result["decision"] = "needs_fix"


def _refresh_exact_final_state(
    paths: dict[str, Path],
    result: dict[str, Any],
) -> None:
    target_state = _path_state(paths["target"])
    receipt_state = _path_state(paths["receipt"])
    journal = _path_state(paths["journal"]) != "absent"
    wal = _path_state(paths["wal"]) != "absent"
    shm = _path_state(paths["shm"]) != "absent"
    result["final_target_exists"] = target_state != "absent"
    result["final_target_regular_file"] = target_state == "file"
    result["final_receipt_exists"] = receipt_state != "absent"
    result["final_receipt_regular_file"] = receipt_state == "file"
    result["final_journal_sidecar_exists"] = journal
    result["final_WAL_sidecar_exists"] = wal
    result["final_SHM_sidecar_exists"] = shm
    result["final_sidecar_count"] = int(journal) + int(wal) + int(shm)
    result["final_exact_target_parent_exists"] = (
        _path_state(paths["target_parent"]) == "directory"
    )
    result["final_runtime_parent_exists"] = (
        _path_state(paths["runtime_parent"]) == "directory"
    )


def _count_DML(statement: str, result: dict[str, Any]) -> None:
    stripped = statement.lstrip()
    upper = stripped.upper()
    if not upper.startswith(_DML_PREFIXES):
        return
    lowered = stripped.casefold()
    if TABLE_NAME.casefold() in lowered:
        result["candidate_table_DML_statement_count"] += 1
    elif ATTEMPT_RESERVATION_TABLE.casefold() in lowered:
        result["attempt_table_DML_statement_count"] += 1
    else:
        result["other_user_DML_statement_count"] += 1


def _inject(phase: str, selected: str | None) -> None:
    if selected != phase:
        return
    raise _SmokeFailure(_INJECTION_ERROR_CODES.get(phase, "injected_failure"))


def _path_state(path: Path) -> str:
    try:
        status = path.lstat()
    except FileNotFoundError:
        return "absent"
    except OSError as exc:
        raise _SmokeFailure("path_policy_failure") from exc
    if stat.S_ISLNK(status.st_mode):
        return "symlink"
    if _is_reparse(status):
        return "reparse"
    if stat.S_ISREG(status.st_mode):
        return "file"
    if stat.S_ISDIR(status.st_mode):
        return "directory"
    return "other"


def _is_reparse(status: os.stat_result) -> bool:
    attribute = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return bool(getattr(status, "st_file_attributes", 0) & attribute)


def _normalized_DDL_hash(value: str | None) -> str:
    if not isinstance(value, str):
        return "not_available"
    normalized = re.sub(r"\s+", "", value).casefold()
    normalized = normalized.replace("createtableifnotexists", "createtable")
    return _sha256_bytes(normalized.encode("utf-8"))


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_hash(value: Any) -> bool:
    return isinstance(value, str) and _HASH_RE.fullmatch(value) is not None


def _paths_or_SQL_started(result: dict[str, Any]) -> bool:
    return bool(
        result["path_derivation_completed"]
        or result["SQLite_connection_open_count"]
        or result["parent_directory_create_count"]
    )
