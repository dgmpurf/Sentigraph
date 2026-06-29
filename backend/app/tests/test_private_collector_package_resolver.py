from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.services.private_collector_package_resolver import (
    REQUIRED_PACKAGE_METADATA_FILES,
    build_safe_package_summary,
    resolve_private_collector_package,
    summarize_private_collector_package_metadata,
)


def _write_package(root: Path, package_name: str, *, include_required: bool = True) -> Path:
    package_dir = root / package_name
    package_dir.mkdir(parents=True)
    if include_required:
        for filename in REQUIRED_PACKAGE_METADATA_FILES:
            target = package_dir / filename
            if filename.endswith(".json"):
                target.write_text("{}", encoding="utf-8")
            else:
                target.write_text("metadata only", encoding="utf-8")
    return package_dir


def _write_metadata_json(package_dir: Path, filename: str, payload: dict) -> None:
    (package_dir / filename).write_text(json.dumps(payload), encoding="utf-8")


def test_package_name_resolves_safely_under_export_root(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "helldivers_package")

    result = resolve_private_collector_package(export_root, {"package_name": "helldivers_package"})

    assert result.status == "accepted_metadata_only"
    assert result.package_name == "helldivers_package"
    assert result.locator_strategy == "package_name_under_configured_export_root"
    assert result.required_files_presence["evidence_items.jsonl"] is True
    assert result.required_files_presence["evidence_items.csv"] is True


def test_package_name_is_preferred_over_ambiguous_legacy_path(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "preferred_package")

    result = resolve_private_collector_package(
        export_root,
        {
            "package_name": "preferred_package",
            "package_path_relative": "exports/sentigraph-evidence-v1/wrong_package",
        },
    )

    assert result.status == "accepted_metadata_only"
    assert result.package_name == "preferred_package"
    assert result.locator_strategy == "package_name_under_configured_export_root"
    assert any("legacy package_path_relative ignored" in warning for warning in result.warnings)


def test_explicit_package_path_relative_to_export_root_resolves_safely(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "relative_package")

    result = resolve_private_collector_package(
        export_root,
        {"package_path_relative_to_export_root": "relative_package"},
    )

    assert result.status == "accepted_metadata_only"
    assert result.package_name == "relative_package"
    assert result.locator_strategy == "package_path_relative_to_export_root"


def test_legacy_package_path_relative_alone_requires_manual_review(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()

    result = resolve_private_collector_package(
        export_root,
        {"package_path_relative": "exports/sentigraph-evidence-v1/legacy_package"},
    )

    assert result.status == "manual_review_required"
    assert result.resolved_package_path is None
    assert any("legacy package_path_relative is ambiguous" in warning for warning in result.warnings)


@pytest.mark.parametrize("bad_name", ["nested/package", "nested\\package", "", ".", ".."])
def test_invalid_package_name_is_blocked_or_needs_fix(tmp_path: Path, bad_name: str) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()

    result = resolve_private_collector_package(export_root, {"package_name": bad_name})

    assert result.status in {"needs_fix_metadata_contract", "blocked_path_escape"}
    assert result.resolved_package_path is None


def test_path_traversal_in_relative_to_export_root_is_blocked(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()

    result = resolve_private_collector_package(
        export_root,
        {"package_path_relative_to_export_root": "../private-runtime/package"},
    )

    assert result.status == "blocked_path_escape"
    assert result.resolved_package_path is None


def test_resolved_path_outside_export_root_is_blocked(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()
    outside = tmp_path / "outside" / "package"
    outside.mkdir(parents=True)

    result = resolve_private_collector_package(
        export_root,
        {"package_path_relative_to_export_root": "../outside/package"},
    )

    assert result.status == "blocked_path_escape"
    assert result.resolved_package_path is None


def test_required_metadata_file_presence_is_reported(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    package_dir = _write_package(export_root, "partial_package", include_required=False)
    (package_dir / "manifest.json").write_text("{}", encoding="utf-8")
    (package_dir / "coverage_note.md").write_text("coverage only", encoding="utf-8")

    result = resolve_private_collector_package(export_root, {"package_name": "partial_package"})

    assert result.status == "accepted_metadata_only"
    assert result.required_files_presence["manifest.json"] is True
    assert result.required_files_presence["coverage_note.md"] is True
    assert result.required_files_presence["evidence_items.jsonl"] is False
    assert "evidence_items.jsonl" in result.missing_required_files


def test_evidence_item_files_are_not_parsed_or_opened(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")
    original_read_text = Path.read_text

    def guarded_read_text(self: Path, *args, **kwargs):
        if self.name in {"evidence_items.jsonl", "evidence_items.csv"}:
            raise AssertionError(f"{self.name} must not be parsed")
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", guarded_read_text)

    result = resolve_private_collector_package(export_root, {"package_name": "safe_package"})
    summary = summarize_private_collector_package_metadata(result)

    assert result.status == "accepted_metadata_only"
    assert summary.status == "accepted_metadata_only"


def test_safe_summary_does_not_include_absolute_filesystem_paths(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    _write_package(export_root, "safe_package")

    result = resolve_private_collector_package(export_root, {"package_name": "safe_package"})
    summary = build_safe_package_summary(result)
    summary_text = json.dumps(summary, ensure_ascii=False)

    assert result.resolved_package_path is not None
    assert str(tmp_path) not in summary_text
    assert str(export_root) not in summary_text
    assert summary["package_name"] == "safe_package"


def test_privacy_marker_fields_are_allowed(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    package_dir = _write_package(export_root, "safe_markers")
    _write_metadata_json(
        package_dir,
        "manifest.json",
        {
            "privacy_markers": {
                "raw_author_id_exported": False,
                "raw_author_name_exported": False,
                "profile_url_exported": False,
                "raw_author_id_removed": True,
                "raw_author_name_removed": True,
                "no_private_messages": True,
            }
        },
    )

    result = resolve_private_collector_package(export_root, {"package_name": "safe_markers"})

    assert result.status == "accepted_metadata_only"
    assert result.forbidden_fields == []


@pytest.mark.parametrize(
    ("filename", "payload", "field"),
    [
        ("manifest.json", {"raw_author_id": "actual-id"}, "raw_author_id"),
        ("validation_report.json", {"token": "actual-token"}, "token"),
    ],
)
def test_actual_forbidden_metadata_field_blocks_privacy_issue(
    tmp_path: Path,
    filename: str,
    payload: dict,
    field: str,
) -> None:
    export_root = tmp_path / "exports"
    package_dir = _write_package(export_root, "unsafe_package")
    _write_metadata_json(package_dir, filename, payload)

    result = resolve_private_collector_package(export_root, {"package_name": "unsafe_package"})

    assert result.status == "blocked_privacy_issue"
    assert field in result.forbidden_fields


def test_missing_package_directory_returns_blocked_missing_package(tmp_path: Path) -> None:
    export_root = tmp_path / "exports"
    export_root.mkdir()

    result = resolve_private_collector_package(export_root, {"package_name": "missing_package"})

    assert result.status == "blocked_missing_package"
    assert result.resolved_package_path is None
