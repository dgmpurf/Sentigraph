from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from scripts import validate_external_evidence_package as validator


REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_external_evidence_package.py"
SAMPLE_PACKAGE = (
    REPO_ROOT
    / "docs"
    / "samples"
    / "helldivers2_psn_demo"
    / "helldivers2-psn-demo_20260614_055754"
)


def load_validator():
    return validator


def test_validator_uses_canonical_repository_root_module_identity() -> None:
    assert validator.__name__ == "scripts.validate_external_evidence_package"


def test_canonical_module_invocation_help_succeeds_without_package_access() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "scripts.validate_external_evidence_package", "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    assert "package_folder" in completed.stdout
    assert "Traceback" not in completed.stderr


def test_legacy_direct_script_invocation_has_bounded_migration_marker() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR_PATH), "--help"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 2
    assert completed.stderr.strip() == validator.LEGACY_DIRECT_INVOCATION_MARKER
    assert "Traceback" not in completed.stderr
    assert str(REPO_ROOT) not in completed.stderr


def test_external_evidence_validator_accepts_helldivers_sample_with_expected_warnings() -> None:
    validator = load_validator()

    result = validator.validate_package(
        SAMPLE_PACKAGE,
        case_keywords=["helldivers", "psn", "playstation", "steam"],
    )

    assert result["status"] == "warn"
    assert result["errors_count"] == 0
    assert result["warnings_count"] >= 2
    assert result["case_id"] == "helldivers2_psn_demo"
    assert result["evidence_count"] == 34
    assert result["source_count"] == 7
    assert result["root_content_count"] == 6
    assert result["comment_count"] == 28
    assert result["privacy_status"] == "pass"
    assert result["coverage_status"] == "pass"
    assert result["case_relevance"]["status"] == "pass"
    assert result["distribution"]["platform"]["reddit"] == 31


def test_external_evidence_validator_reports_missing_required_package_file(tmp_path: Path) -> None:
    validator = load_validator()

    package_dir = tmp_path / "package"
    package_dir.mkdir()

    result = validator.validate_package(package_dir)

    assert result["status"] == "fail"
    assert result["errors_count"] > 0
    assert any(error["code"] == "MISSING_REQUIRED_FILE" for error in result["errors"])


def test_external_evidence_validator_blocks_forbidden_identity_keys(tmp_path: Path) -> None:
    validator = load_validator()
    package_dir = tmp_path / "package"
    package_dir.mkdir()

    (package_dir / "manifest.json").write_text(
        json.dumps(
            {
                "package_version": "sentigraph_external_export_v1",
                "contract_version": "evidence_to_opinion_ecosystem_mapping_contract_v1",
                "case_id": "case_1",
                "case_title": "Case One",
                "data_scope": {
                    "evidence_items_count": 1,
                    "source_urls_count": 1,
                    "comment_sample_count": 1,
                    "root_content_count": 0,
                },
                "coverage_note": "Selected public sample only; not full-web coverage; not full-platform coverage; not full-thread coverage; not official verification; not causal proof.",
            }
        ),
        encoding="utf-8",
    )
    (package_dir / "validation_report.json").write_text(json.dumps({"status": "passed"}), encoding="utf-8")
    (package_dir / "source_manifest.jsonl").write_text(
        json.dumps(
            {
                "source_id": "source_1",
                "source_url": "https://example.invalid/source",
                "platform": "example",
                "source_type": "community_discussion",
                "content_visibility": "public",
                "access_scope": "public",
                "collection_method": "manual_url",
                "captcha_bypass_used": False,
                "anti_bot_bypass_used": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    evidence_row = {
        key: ""
        for key in validator.EVIDENCE_REQUIRED_KEYS
    }
    evidence_row.update(
        {
            "evidence_id": "ev_1",
            "case_id": "case_1",
            "platform": "example",
            "source_type": "community_discussion",
            "acquisition_mode": "manual_url",
            "provenance_type": "manual_url",
            "verification_status": "source_url_provided_unverified",
            "trust_label": "medium_low",
            "trust_score": 0.4,
            "review_status": "review_needed",
            "evidence_type": "comment",
            "language": "en",
            "source_url": "https://example.invalid/source",
            "url": "https://example.invalid/source",
            "root_id": "source_1",
            "raw_author_id_removed": True,
            "raw_author_name_removed": True,
            "duplicate_count": 1,
            "risk_flags": [],
            "content_visibility": "public",
            "access_scope": "public",
            "source_capture_method": "manual_comment_sample",
            "raw_data_safe": {},
            "ingestion_metadata": {},
            "comment_user_name": "should-not-be-exported",
        }
    )
    (package_dir / "evidence_items.jsonl").write_text(json.dumps(evidence_row) + "\n", encoding="utf-8")
    (package_dir / "collection_log.jsonl").write_text(json.dumps({"action": "export_finished"}) + "\n", encoding="utf-8")
    for file_name in ["evidence_items.csv", "coverage_note.md", "README.md", "validation_report.md"]:
        (package_dir / file_name).write_text(
            "Selected public sample only; not full-web coverage; not full-platform coverage; not full-thread coverage; not official verification; not causal proof.",
            encoding="utf-8",
        )

    result = validator.validate_package(package_dir)

    assert result["status"] == "fail"
    assert any(error["code"] == "FORBIDDEN_EVIDENCE_KEY" for error in result["errors"])


def test_external_evidence_validator_rejects_duplicate_manifest_keys(tmp_path: Path) -> None:
    package_dir = tmp_path / "package"
    package_dir.mkdir()
    (package_dir / "manifest.json").write_bytes(b'{"case_id":"one","case_id":"two"}')

    result = validator.validate_package(package_dir)

    assert result["status"] == "fail"
    parse_error = next(error for error in result["errors"] if error["code"] == "JSON_PARSE_FAILED")
    assert parse_error["detail"]["reason_code"] == "DUPLICATE_OBJECT_KEY"


def test_external_evidence_validator_rejects_array_manifest_root(tmp_path: Path) -> None:
    package_dir = tmp_path / "package"
    package_dir.mkdir()
    (package_dir / "manifest.json").write_bytes(b"[]")

    result = validator.validate_package(package_dir)

    parse_error = next(error for error in result["errors"] if error["code"] == "JSON_PARSE_FAILED")
    assert parse_error["detail"]["reason_code"] == "ROOT_SHAPE_OBJECT_REQUIRED"
