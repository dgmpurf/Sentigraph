from __future__ import annotations

import json
from pathlib import Path

import pytest

import app.services.private_collector_provider_result_reader as provider_reader_module
from app.services.private_collector_package_resolver import (
    GOVERNED_B05_METADATA_READ_PROFILE,
    PrivateCollectorPackageResolutionResult,
    REQUIRED_PACKAGE_METADATA_FILES,
)
from app.services.private_collector_provider_result_reader import (
    build_provider_handoff_summary,
    read_provider_result_metadata,
    resolve_provider_result_package,
    validate_provider_result_metadata,
)


def _write_package(root: Path, package_name: str) -> Path:
    package_dir = root / package_name
    package_dir.mkdir(parents=True)
    for filename in REQUIRED_PACKAGE_METADATA_FILES:
        target = package_dir / filename
        if filename.endswith(".json"):
            target.write_text("{}", encoding="utf-8")
        else:
            target.write_text("metadata only", encoding="utf-8")
    return package_dir


def _provider_result_payload(
    *,
    package_name: str = "helldivers_package",
    status: str = "package_ready",
    locator_strategy: str = "package_name_under_configured_export_root",
) -> dict:
    return {
        "schema": "sentigraph_provider_job_result_v0_1",
        "provider_result_id": "provider_result_fixture",
        "provider_job_id": "provider_job_fixture",
        "request_id": "analysis_request_fixture",
        "provider_type": "private_collector_local_file",
        "adapter_id": "private_collector_metadata_only_adapter",
        "contract_version": "0.1",
        "status": status,
        "package_contract": "sentigraph_evidence_export_v1",
        "package_reference": {
            "package_name": package_name,
            "package_role": "review_ready_candidate",
            "package_index_ref": "package_index.json",
            "package_locator_strategy": locator_strategy,
        },
        "metadata_summary": {
            "evidence_count": 34,
            "source_count": 7,
            "comment_count": 28,
        },
        "validation_summary": {
            "status": "passed",
            "errors": 0,
            "warnings": 0,
        },
        "coverage_note": "Selected package coverage only; not full-web or full-platform coverage.",
        "safety_markers": {
            "raw_author_id_exported": False,
            "raw_author_name_exported": False,
            "profile_url_exported": False,
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "no_private_messages": True,
        },
        "created_at": "2026-06-29T00:00:00Z",
    }


def _write_provider_result(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _accepted_resolution(package_name: str = "helldivers_package") -> PrivateCollectorPackageResolutionResult:
    return PrivateCollectorPackageResolutionResult(
        status="accepted_metadata_only",
        package_name=package_name,
        locator_strategy="package_name_under_configured_export_root",
    )


def test_valid_provider_result_with_package_name_resolves_to_metadata_only_summary(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "helldivers_package")
    provider_path = _write_provider_result(tmp_path / "provider_result.json", _provider_result_payload())

    result = read_provider_result_metadata(provider_path, export_root)

    assert result.status == "accepted_metadata_only"
    assert result.provider_status == "package_ready"
    assert result.resolver_result is not None
    assert result.resolver_result.status == "accepted_metadata_only"
    assert result.safe_summary["package_summary"]["package_name"] == "helldivers_package"
    assert result.safe_summary["provider_result_id"] == "provider_result_fixture"


def test_validation_passed_status_maps_to_safe_ready_metadata_status(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "passed_package")
    payload = _provider_result_payload(package_name="passed_package", status="validation_passed")

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "validation_passed"
    assert result.safe_summary["status"] == "validation_passed"
    assert result.resolver_result is not None
    assert result.resolver_result.status == "accepted_metadata_only"


def test_validation_warn_maps_to_manual_review_status(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "warn_package")
    payload = _provider_result_payload(package_name="warn_package", status="validation_warn")

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "validation_warn"
    assert any("manual review" in warning for warning in result.warnings)
    assert result.resolver_result is not None


def test_package_name_locator_calls_resolver_with_package_name(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "named_package")
    payload = _provider_result_payload(package_name="named_package")

    result = resolve_provider_result_package(payload, export_root)

    assert result.status == "accepted_metadata_only"
    assert result.package_name == "named_package"
    assert result.locator_strategy == "package_name_under_configured_export_root"


def test_relative_locator_calls_resolver_with_explicit_relative_field(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "relative_package")
    payload = _provider_result_payload(
        package_name="relative_package",
        locator_strategy="package_path_relative_to_export_root",
    )
    payload["package_reference"]["package_path_relative_to_export_root"] = "relative_package"

    result = resolve_provider_result_package(payload, export_root)

    assert result.status == "accepted_metadata_only"
    assert result.package_name == "relative_package"
    assert result.locator_strategy == "package_path_relative_to_export_root"


def test_named_metadata_read_profile_is_forwarded_to_resolver_exactly_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, object, object]] = []

    def fake_resolver(
        export_root: object,
        package_entry: object,
        *,
        metadata_read_profile: object,
    ) -> PrivateCollectorPackageResolutionResult:
        calls.append((export_root, package_entry, metadata_read_profile))
        return _accepted_resolution()

    monkeypatch.setattr(
        provider_reader_module,
        "resolve_private_collector_package",
        fake_resolver,
    )

    result = read_provider_result_metadata(
        _provider_result_payload(),
        tmp_path / "exports",
        metadata_read_profile=GOVERNED_B05_METADATA_READ_PROFILE,
    )

    assert result.status == "accepted_metadata_only"
    assert calls == [
        (
            tmp_path / "exports",
            {"package_name": "helldivers_package"},
            GOVERNED_B05_METADATA_READ_PROFILE,
        )
    ]


def test_omitted_metadata_read_profile_preserves_two_argument_resolver_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[object, object]] = []

    def strict_two_argument_resolver(
        export_root: object,
        package_entry: object,
    ) -> PrivateCollectorPackageResolutionResult:
        calls.append((export_root, package_entry))
        return _accepted_resolution()

    monkeypatch.setattr(
        provider_reader_module,
        "resolve_private_collector_package",
        strict_two_argument_resolver,
    )

    result = read_provider_result_metadata(
        _provider_result_payload(),
        tmp_path / "exports",
    )

    assert result.status == "accepted_metadata_only"
    assert calls == [
        (
            tmp_path / "exports",
            {"package_name": "helldivers_package"},
        )
    ]


def test_manual_review_required_legacy_path_does_not_silently_accept(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload(
        package_name="legacy_package",
        locator_strategy="manual_review_required_legacy_path",
    )
    payload["package_reference"]["package_path_relative"] = "exports/sentigraph-evidence-v1/legacy_package"

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "manual_review_required"
    assert result.resolver_result is None
    assert any("legacy package path" in warning for warning in result.warnings)


def test_missing_package_reference_returns_needs_fix_metadata_contract(tmp_path: Path) -> None:
    payload = _provider_result_payload()
    payload.pop("package_reference")

    result = read_provider_result_metadata(payload, tmp_path / "exports")

    assert result.status == "needs_fix_metadata_contract"
    assert any("package_reference" in error for error in result.errors)


@pytest.mark.parametrize("field_name", ["schema", "provider_result_id", "package_contract", "created_at"])
def test_missing_required_provider_result_fields_returns_needs_fix_metadata_contract(
    tmp_path: Path,
    field_name: str,
) -> None:
    payload = _provider_result_payload()
    payload.pop(field_name)

    result = validate_provider_result_metadata(payload)

    assert result.status == "needs_fix_metadata_contract"
    assert any(field_name in error for error in result.errors)


def test_unsupported_schema_returns_needs_fix_metadata_contract(tmp_path: Path) -> None:
    payload = _provider_result_payload()
    payload["schema"] = "sentigraph_provider_job_result_v9"

    result = validate_provider_result_metadata(payload)

    assert result.status == "needs_fix_metadata_contract"
    assert any("schema" in error for error in result.errors)


def test_live_collection_not_authorized_remains_blocked_without_resolving_package(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "blocked_package")
    payload = _provider_result_payload(package_name="blocked_package", status="live_collection_not_authorized")

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "live_collection_not_authorized"
    assert result.resolver_result is None
    assert any("blocked" in warning for warning in result.warnings)


def test_blocked_missing_package_from_resolver_propagates_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload(package_name="missing_package")

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "blocked_missing_package"
    assert result.resolver_result is not None
    assert result.safe_summary["package_summary"]["status"] == "blocked_missing_package"


def test_blocked_path_escape_from_resolver_propagates_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    payload = _provider_result_payload(
        package_name="escape_package",
        locator_strategy="package_path_relative_to_export_root",
    )
    payload["package_reference"]["package_path_relative_to_export_root"] = "../escape_package"

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "blocked_path_escape"
    assert result.resolver_result is not None


def test_blocked_privacy_issue_from_resolver_propagates_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    package_dir = _write_package(export_root, "unsafe_package")
    (package_dir / "manifest.json").write_text(json.dumps({"token": "actual-token"}), encoding="utf-8")
    payload = _provider_result_payload(package_name="unsafe_package")

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "blocked_privacy_issue"
    assert result.resolver_result is not None
    assert "token" in result.forbidden_fields


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("token", "actual-token"),
        ("raw_author_id", "actual-id"),
    ],
)
def test_actual_forbidden_provider_metadata_field_returns_blocked_privacy_issue(
    tmp_path: Path,
    field: str,
    value: str,
) -> None:
    payload = _provider_result_payload()
    payload[field] = value

    result = read_provider_result_metadata(payload, tmp_path / "exports")

    assert result.status == "blocked_privacy_issue"
    assert field in result.forbidden_fields


def test_safety_marker_fields_are_allowed(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "marker_package")
    payload = _provider_result_payload(package_name="marker_package")
    payload["safety_markers"]["raw_author_id_exported"] = False
    payload["safety_markers"]["raw_author_id_removed"] = True

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "accepted_metadata_only"
    assert result.forbidden_fields == []


def test_safe_handoff_summary_does_not_include_absolute_filesystem_paths(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    payload = _provider_result_payload(package_name="safe_package")

    result = read_provider_result_metadata(payload, export_root)
    summary = build_provider_handoff_summary(payload, result.resolver_result)
    summary_text = json.dumps(summary, ensure_ascii=False)

    assert str(tmp_path) not in summary_text
    assert str(export_root) not in summary_text
    assert summary["package_summary"]["path_exposed"] is False


def test_evidence_item_files_are_not_parsed_or_opened(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    payload = _provider_result_payload(package_name="safe_package")
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be parsed")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    result = read_provider_result_metadata(payload, export_root)

    assert result.status == "accepted_metadata_only"


def test_provider_reader_has_no_runtime_or_production_side_effect_flags(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    payload = _provider_result_payload(package_name="safe_package")

    result = read_provider_result_metadata(payload, export_root)

    assert result.safe_mode["metadata_only"] is True
    for flag in [
        "runtime_file_written",
        "evidence_layer_written",
        "production_case_created",
        "analysis_run_created",
        "collector_run",
        "real_api_called",
        "real_llm_called",
        "url_fetching",
        "scraping",
        "evidence_items_jsonl_parsed",
        "evidence_items_csv_parsed",
    ]:
        assert result.safe_mode[flag] is False
