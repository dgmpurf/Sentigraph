from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from collections import Counter
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from app.api.v1.routes import internal_alpha_review_console as review_console_route
from app.services.b05_review_subject_identity import (
    B05_REVIEW_SUBJECT_IDENTITY_FIELDS,
    GOVERNED_B05_IDENTITY_METADATA_FILES,
    text_from_same_read_raw_bytes,
)
from app.services.internal_alpha_local_exchange_review_projection import (
    ADAPTER_ID_ENV,
    B01_LOCAL_EXCHANGE_GATE_ENV,
    B01_ROUTE_GATE_ENV,
    B03_PROJECTION_GATE_ENV,
    B05_GATE_ENV,
    CAPABILITY_LABEL,
    EXPORT_ROOT_ENV,
    RESULTS_DIR_ENV,
    ROUTE_MODE,
    SHARED_ALPHA_GATE_ENV,
    InternalAlphaLocalExchangeSampleRegistryEntry,
    build_internal_alpha_local_exchange_identity_ready_review_projection,
    build_internal_alpha_local_exchange_sample_registry,
)
from app.services.local_exchange_review_only_projection_bridge import (
    PROJECTION_FIELDS,
    PROJECTION_SCHEMA,
    PROJECTION_VERSION,
    VERSIONED_PROJECTION_FIELDS,
    VERSIONED_PROJECTION_SCHEMA,
    VERSIONED_PROJECTION_VERSION,
    build_identity_ready_local_exchange_review_only_projection,
)
from app.services.private_collector_package_resolver import (
    GOVERNED_B05_METADATA_READ_PROFILE,
    resolve_private_collector_package_with_identity,
)


SAFE_HANDLE = "helldivers2-psn-demo"
RESULT_FILE_NAME = "provider_result_synthetic-current.json"
PACKAGE_NAME = "synthetic_package"
LOWER_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
ALL_GATES = (
    SHARED_ALPHA_GATE_ENV,
    B05_GATE_ENV,
    B01_ROUTE_GATE_ENV,
    B01_LOCAL_EXCHANGE_GATE_ENV,
    B03_PROJECTION_GATE_ENV,
)
ROUTE_SOURCE_PATH = (
    Path(__file__).resolve().parents[3]
    / "backend/app/api/v1/routes/internal_alpha_review_console.py"
)


def _canonical_sha256(value: dict[str, Any]) -> str:
    canonical = json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _provider_payload() -> dict[str, Any]:
    return {
        "schema": "sentigraph_provider_job_result_v1",
        "request_schema": "sentigraph_analysis_request_v1",
        "contract_version": "1.0",
        "adapter_id": "synthetic_local_exchange_adapter",
        "compatibility_status": "compatible",
        "status": "package_ready",
        "provider_result_id": "synthetic_provider_result",
        "provider_job_id": "synthetic_provider_job",
        "sentigraph_request_id": "synthetic_analysis_request",
        "provider_type": "private_collector_local_file",
        "package_contract": "sentigraph_evidence_export_v1",
        "package_id": PACKAGE_NAME,
        "package_role": "review_ready_candidate",
        "package_index_ref": "package_index.json",
        "package_root_ref": "configured_export_root",
        "package_relative_path": PACKAGE_NAME,
        "summary": {
            "evidence_items": 7,
            "sources": 3,
            "comment_samples": 4,
            "root_candidates": 3,
        },
        "validation_summary": {"status": "passed", "errors": 0, "warnings": 0},
        "coverage_note": "Selected package metadata counts only.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-08-12T00:00:00Z",
        "warnings": [],
        "errors": [],
        "nextAction": "review_package_metadata",
    }


def _metadata_raw_by_name() -> dict[str, bytes]:
    return {
        "README.md": b"Synthetic metadata-only package.\r\n",
        "coverage_note.md": b"Selected package metadata counts only.\r",
        "manifest.json": json.dumps(
            {
                "schema": "sentigraph_evidence_export_manifest_v1",
                "package_name": PACKAGE_NAME,
                "raw_author_id_removed": True,
                "raw_author_name_removed": True,
                "profile_url_exported": False,
            },
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8"),
        "validation_report.json": b'{"status":"passed","errors":0,"warnings":0}',
        "validation_report.md": b"Validation passed.\n",
    }


def _write_fixture(tmp_path: Path) -> tuple[dict[str, str], Path, Path, bytes, dict[str, bytes]]:
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    provider_raw = json.dumps(
        _provider_payload(),
        ensure_ascii=False,
        indent=2,
    ).replace("\n", "\r\n").encode("utf-8")
    result_path = results_dir / RESULT_FILE_NAME
    result_path.write_bytes(provider_raw)

    export_root = tmp_path / "exports"
    package_dir = export_root / PACKAGE_NAME
    package_dir.mkdir(parents=True)
    metadata_raw = _metadata_raw_by_name()
    for name in GOVERNED_B05_IDENTITY_METADATA_FILES:
        (package_dir / name).write_bytes(metadata_raw[name])

    environment = {gate: "true" for gate in ALL_GATES}
    environment.update(
        {
            RESULTS_DIR_ENV: str(results_dir),
            EXPORT_ROOT_ENV: str(export_root),
            ADAPTER_ID_ENV: "synthetic_local_exchange_adapter",
        }
    )
    return environment, result_path, package_dir, provider_raw, metadata_raw


def _registry() -> Any:
    return build_internal_alpha_local_exchange_sample_registry(
        (
            InternalAlphaLocalExchangeSampleRegistryEntry(
                sample_handle=SAFE_HANDLE,
                result_file_name=RESULT_FILE_NAME,
                display_label="Synthetic current sample",
                sample_role="synthetic_current",
                is_default=True,
                enabled=True,
                catalog_order=0,
                route_mode=ROUTE_MODE,
                capability_label=CAPABILITY_LABEL,
            ),
        )
    )


def _synthetic_route_projection() -> dict[str, Any]:
    review_subject_identity = {
        "identity_schema": "sentigraph_b05_review_subject_identity_v0_1",
        "identity_version": "0.1",
        "identity_status": "ready",
        "sample_handle": SAFE_HANDLE,
        "result_file_name": RESULT_FILE_NAME,
        "package_name": PACKAGE_NAME,
        "provider_result_content_bytes": 1,
        "provider_result_content_sha256": "1" * 64,
        "metadata_profile": GOVERNED_B05_METADATA_READ_PROFILE,
        "metadata_entry_count": 5,
        "safe_metadata_bundle_sha256": "2" * 64,
        "review_subject_content_safe_hash": "3" * 64,
        "review_subject_binding_safe_hash": "4" * 64,
    }
    upstream_response = {
        "schema": "internal_operator_review_only_staging_local_exchange_response_v0_2",
        "metadata_only": True,
        "review_only": True,
        "status": "manual_review_required",
        "result_file_name": RESULT_FILE_NAME,
        "staging_candidate": {"package_name": PACKAGE_NAME},
        "path_exposed": False,
        "raw_metadata_exposed": False,
    }
    return build_identity_ready_local_exchange_review_only_projection(
        SAFE_HANDLE,
        RESULT_FILE_NAME,
        upstream_response,
        review_subject_identity,
    )


def test_same_read_text_reconstruction_matches_read_text_newline_and_bom_semantics() -> None:
    raw = b"\xef\xbb\xbffirst\r\nsecond\rthird\n"

    assert text_from_same_read_raw_bytes(raw) == "\ufefffirst\nsecond\nthird\n"


def test_v0_1_contract_is_unchanged_and_v0_2_is_an_exact_final_field_extension() -> None:
    assert PROJECTION_SCHEMA == "sentigraph_local_exchange_review_only_candidate_projection_v0_1"
    assert PROJECTION_VERSION == "0.1"
    assert len(PROJECTION_FIELDS) == 52
    assert VERSIONED_PROJECTION_SCHEMA == "sentigraph_local_exchange_review_only_candidate_projection_v0_2"
    assert VERSIONED_PROJECTION_VERSION == "0.2"
    assert VERSIONED_PROJECTION_FIELDS == (*PROJECTION_FIELDS, "review_subject_identity")
    assert len(VERSIONED_PROJECTION_FIELDS) == 53


def test_ready_identity_is_preserved_when_legacy_projection_prefix_requires_manual_review() -> None:
    review_subject_identity = {
        "identity_schema": "sentigraph_b05_review_subject_identity_v0_1",
        "identity_version": "0.1",
        "identity_status": "ready",
        "sample_handle": SAFE_HANDLE,
        "result_file_name": RESULT_FILE_NAME,
        "package_name": PACKAGE_NAME,
        "provider_result_content_bytes": 1,
        "provider_result_content_sha256": "1" * 64,
        "metadata_profile": GOVERNED_B05_METADATA_READ_PROFILE,
        "metadata_entry_count": 5,
        "safe_metadata_bundle_sha256": "2" * 64,
        "review_subject_content_safe_hash": "3" * 64,
        "review_subject_binding_safe_hash": "4" * 64,
    }
    upstream_response = {
        "schema": "internal_operator_review_only_staging_local_exchange_response_v0_2",
        "metadata_only": True,
        "review_only": True,
        "status": "manual_review_required",
        "result_file_name": RESULT_FILE_NAME,
        "staging_candidate": {"package_name": PACKAGE_NAME},
        "path_exposed": False,
        "raw_metadata_exposed": False,
    }

    projection = build_identity_ready_local_exchange_review_only_projection(
        SAFE_HANDLE,
        RESULT_FILE_NAME,
        upstream_response,
        review_subject_identity,
    )

    assert tuple(projection) == VERSIONED_PROJECTION_FIELDS
    assert len(projection) == 53
    assert projection["projection_status"] == "manual_review_required"
    assert projection["projection_error_code"] == "upstream_manual_review_required"
    assert projection["review_subject_identity"] == review_subject_identity
    assert projection["review_subject_identity"]["identity_status"] == "ready"


def test_identity_ready_service_path_uses_each_same_read_buffer_once_and_emits_exact_hashes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    environment, result_path, package_dir, provider_raw, metadata_raw = _write_fixture(tmp_path)
    allowed_paths = {
        result_path.resolve(),
        *((package_dir / name).resolve() for name in GOVERNED_B05_IDENTITY_METADATA_FILES),
    }
    observed_reads: list[Path] = []
    original_read_bytes = Path.read_bytes

    def tracked_read_bytes(path: Path) -> bytes:
        resolved = path.resolve()
        assert resolved in allowed_paths
        observed_reads.append(resolved)
        return original_read_bytes(path)

    def prohibited_read_text(path: Path, *args: Any, **kwargs: Any) -> str:
        raise AssertionError(f"versioned path reopened content through read_text: {path.name}")

    monkeypatch.setattr(Path, "read_bytes", tracked_read_bytes)
    monkeypatch.setattr(Path, "read_text", prohibited_read_text)

    projection = build_internal_alpha_local_exchange_identity_ready_review_projection(
        SAFE_HANDLE,
        registry=_registry(),
        environment=environment,
    )

    assert tuple(projection) == VERSIONED_PROJECTION_FIELDS
    assert tuple(projection)[:-1] == PROJECTION_FIELDS
    assert len(projection) == 53
    assert projection["projection_schema"] == VERSIONED_PROJECTION_SCHEMA
    assert projection["projection_version"] == VERSIONED_PROJECTION_VERSION
    assert projection["projection_status"] == "ready_for_human_review"
    assert projection["projection_error_code"] is None

    identity = projection["review_subject_identity"]
    assert tuple(identity) == B05_REVIEW_SUBJECT_IDENTITY_FIELDS
    assert identity["identity_status"] == "ready"
    assert identity["sample_handle"] == SAFE_HANDLE
    assert identity["result_file_name"] == RESULT_FILE_NAME
    assert identity["package_name"] == PACKAGE_NAME
    assert identity["provider_result_content_bytes"] == len(provider_raw)
    assert identity["provider_result_content_sha256"] == hashlib.sha256(provider_raw).hexdigest()
    assert identity["metadata_profile"] == GOVERNED_B05_METADATA_READ_PROFILE
    assert identity["metadata_entry_count"] == 5

    entries = [
        {
            "name": name,
            "content_bytes": len(metadata_raw[name]),
            "content_sha256": hashlib.sha256(metadata_raw[name]).hexdigest(),
        }
        for name in GOVERNED_B05_IDENTITY_METADATA_FILES
    ]
    bundle = {
        "bundle_schema": "sentigraph_b05_governed_metadata_identity_bundle_v0_1",
        "bundle_version": "0.1",
        "profile": GOVERNED_B05_METADATA_READ_PROFILE,
        "entry_count": 5,
        "entries": entries,
    }
    expected_bundle_hash = _canonical_sha256(bundle)
    provider_identity = {
        "identity_schema": "sentigraph_b05_provider_result_content_identity_v0_1",
        "identity_version": "0.1",
        "result_file_name": RESULT_FILE_NAME,
        "content_bytes": len(provider_raw),
        "content_sha256": hashlib.sha256(provider_raw).hexdigest(),
    }
    content_identity = {
        "subject_schema": "sentigraph_b05_review_subject_content_identity_v0_1",
        "subject_version": "0.1",
        "provider_result_identity": provider_identity,
        "metadata_profile": GOVERNED_B05_METADATA_READ_PROFILE,
        "safe_metadata_bundle_sha256": expected_bundle_hash,
    }
    expected_content_hash = _canonical_sha256(content_identity)
    binding = {
        "binding_schema": "sentigraph_b05_review_subject_binding_v0_1",
        "binding_version": "0.1",
        "sample_handle": SAFE_HANDLE,
        "result_file_name": RESULT_FILE_NAME,
        "package_name": PACKAGE_NAME,
        "review_subject_content_safe_hash": expected_content_hash,
    }
    assert identity["safe_metadata_bundle_sha256"] == expected_bundle_hash
    assert identity["review_subject_content_safe_hash"] == expected_content_hash
    assert identity["review_subject_binding_safe_hash"] == _canonical_sha256(binding)
    for field in (
        "provider_result_content_sha256",
        "safe_metadata_bundle_sha256",
        "review_subject_content_safe_hash",
        "review_subject_binding_safe_hash",
    ):
        assert LOWER_HEX_64.fullmatch(identity[field]) is not None

    read_counts = Counter(observed_reads)
    assert sum(read_counts.values()) == 6
    assert read_counts[result_path.resolve()] == 1
    assert [read_counts[(package_dir / name).resolve()] for name in GOVERNED_B05_IDENTITY_METADATA_FILES] == [
        1,
        1,
        1,
        1,
        1,
    ]
    serialized = json.dumps(projection, ensure_ascii=False)
    assert str(result_path.parent) not in serialized
    assert str(package_dir.parent) not in serialized
    assert "provider_result_payload" not in serialized
    assert "entries" not in identity


def test_versioned_resolver_requires_exact_profile_and_all_five_regular_files(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    package_dir = export_root / PACKAGE_NAME
    package_dir.mkdir(parents=True)
    metadata_raw = _metadata_raw_by_name()
    for name in GOVERNED_B05_IDENTITY_METADATA_FILES[:-1]:
        (package_dir / name).write_bytes(metadata_raw[name])

    wrong_profile = resolve_private_collector_package_with_identity(
        export_root,
        {"package_name": PACKAGE_NAME},
        metadata_read_profile="generic_six_file",
    )
    missing_member = resolve_private_collector_package_with_identity(
        export_root,
        {"package_name": PACKAGE_NAME},
        metadata_read_profile=GOVERNED_B05_METADATA_READ_PROFILE,
    )

    assert wrong_profile.identity_status == "blocked_metadata_profile_or_order_mismatch"
    assert missing_member.identity_status == "blocked_metadata_member_missing_or_nonfile"
    assert missing_member.metadata_entry_count == 0
    assert missing_member.safe_metadata_bundle_sha256 is None


def test_versioned_resolver_rejects_named_entry_reparse_before_content_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    export_root = tmp_path / "exports"
    package_dir = export_root / PACKAGE_NAME
    package_dir.mkdir(parents=True)
    original_lstat = os.lstat
    package_key = os.path.normcase(os.path.normpath(str(package_dir)))

    def marked_reparse(path: os.PathLike[str] | str, *args: Any, **kwargs: Any) -> Any:
        result = original_lstat(path, *args, **kwargs)
        if os.path.normcase(os.path.normpath(str(path))) != package_key:
            return result
        return SimpleNamespace(
            st_mode=stat.S_IFDIR,
            st_file_attributes=getattr(result, "st_file_attributes", 0) | 0x400,
        )

    monkeypatch.setattr(os, "lstat", marked_reparse)
    monkeypatch.setattr(
        Path,
        "read_bytes",
        lambda _path: pytest.fail("content read occurred before package provenance rejection"),
    )

    result = resolve_private_collector_package_with_identity(
        export_root,
        {"package_name": PACKAGE_NAME},
        metadata_read_profile=GOVERNED_B05_METADATA_READ_PROFILE,
    )

    assert result.identity_status == "blocked_package_name_provenance_mismatch"
    assert result.metadata_entry_count == 0
    assert result.safe_metadata_bundle_sha256 is None


def test_v02_route_inventory_is_exactly_one_get_without_mutation_siblings() -> None:
    source = ROUTE_SOURCE_PATH.read_text(encoding="utf-8")
    v02_relative_path = "/v0.2/local-exchange-projections/{sample_handle}"

    assert f'@router.get("{v02_relative_path}")' in source
    assert source.count(f'"{v02_relative_path}"') == 1
    for method in ("post", "put", "patch", "delete"):
        assert f'@router.{method}("/v0.2/local-exchange-projections/' not in source

    assert '@router.get("/local-exchange-projections/{sample_handle}")' in source
    assert source.count('"/local-exchange-projections/{sample_handle}"') == 1


def test_v02_route_gates_and_exact_allowlist_short_circuit_before_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def prohibited_service(_sample_handle: object) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        raise AssertionError("protected service must not run")

    monkeypatch.setattr(
        review_console_route,
        "build_internal_alpha_local_exchange_identity_ready_review_projection",
        prohibited_service,
    )
    monkeypatch.delenv(review_console_route.ENV_FLAG, raising=False)
    monkeypatch.delenv(review_console_route.IDENTITY_READY_V02_ENV_FLAG, raising=False)
    shared_gate_disabled = (
        review_console_route.get_internal_alpha_local_exchange_identity_ready_review_projection_v0_2(
            SAFE_HANDLE
        )
    )

    monkeypatch.setenv(review_console_route.ENV_FLAG, "true")
    v02_gate_disabled = (
        review_console_route.get_internal_alpha_local_exchange_identity_ready_review_projection_v0_2(
            SAFE_HANDLE
        )
    )

    monkeypatch.setenv(review_console_route.IDENTITY_READY_V02_ENV_FLAG, "true")
    nonallowlisted = (
        review_console_route.get_internal_alpha_local_exchange_identity_ready_review_projection_v0_2(
            "helldivers2-psn-demo-20260614"
        )
    )

    assert calls == 0
    for projection in (shared_gate_disabled, v02_gate_disabled, nonallowlisted):
        assert tuple(projection) == VERSIONED_PROJECTION_FIELDS
        assert len(projection) == 53
        assert tuple(projection["review_subject_identity"]) == B05_REVIEW_SUBJECT_IDENTITY_FIELDS
    assert shared_gate_disabled["projection_error_code"] == "b05_operator_surface_disabled"
    assert v02_gate_disabled["projection_error_code"] == "b05_operator_surface_disabled"
    assert nonallowlisted["projection_error_code"] == "unknown_sample_handle"


def test_v02_route_calls_service_once_and_returns_exact_versioned_projection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ready_projection = _synthetic_route_projection()
    calls = 0

    def synthetic_service(sample_handle: object) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        assert sample_handle == SAFE_HANDLE
        return ready_projection

    monkeypatch.setenv(review_console_route.ENV_FLAG, "true")
    monkeypatch.setenv(review_console_route.IDENTITY_READY_V02_ENV_FLAG, "true")
    monkeypatch.setattr(
        review_console_route,
        "build_internal_alpha_local_exchange_identity_ready_review_projection",
        synthetic_service,
    )

    projection = (
        review_console_route.get_internal_alpha_local_exchange_identity_ready_review_projection_v0_2(
            SAFE_HANDLE
        )
    )

    assert calls == 1
    assert projection is ready_projection
    assert tuple(projection) == VERSIONED_PROJECTION_FIELDS
    assert len(projection) == 53
    assert tuple(projection["review_subject_identity"]) == B05_REVIEW_SUBJECT_IDENTITY_FIELDS


def test_v02_route_contract_mismatch_fails_closed_after_one_service_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def malformed_service(_sample_handle: object) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        return {"projection_schema": "malformed"}

    monkeypatch.setenv(review_console_route.ENV_FLAG, "true")
    monkeypatch.setenv(review_console_route.IDENTITY_READY_V02_ENV_FLAG, "true")
    monkeypatch.setattr(
        review_console_route,
        "build_internal_alpha_local_exchange_identity_ready_review_projection",
        malformed_service,
    )

    projection = (
        review_console_route.get_internal_alpha_local_exchange_identity_ready_review_projection_v0_2(
            SAFE_HANDLE
        )
    )

    assert calls == 1
    assert tuple(projection) == VERSIONED_PROJECTION_FIELDS
    assert len(projection) == 53
    assert projection["projection_schema"] == VERSIONED_PROJECTION_SCHEMA
    assert projection["projection_version"] == VERSIONED_PROJECTION_VERSION
    assert projection["projection_error_code"] == "b05_projection_contract_mismatch"
