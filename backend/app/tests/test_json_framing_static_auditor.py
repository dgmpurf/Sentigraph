from __future__ import annotations

from pathlib import Path

from scripts.governance import sentigraph_json_framing_static_auditor_v0_1 as auditor


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_static_auditor_self_test_passes_bounded_fixtures() -> None:
    result = auditor.run_self_test()

    assert result["status"] == "pass"
    assert result["fixtures"] == 5
    assert result["passed"] == 5
    assert result["target_executed"] is False


def test_current_governed_sources_pass_without_target_execution() -> None:
    result = auditor.audit_paths(
        REPO_ROOT / "sentigraph_shared" / "json_framing.py",
        REPO_ROOT / "scripts" / "validate_external_evidence_package.py",
        REPO_ROOT / "backend" / "app" / "services" / "private_collector_package_resolver.py",
        REPO_ROOT / "backend" / "app" / "tests" / "test_external_evidence_package_validator.py",
    )

    assert result["status"] == "pass"
    assert result["checks_passed"] == len(auditor.CHECK_NAMES)
    assert result["checks_failed"] == 0
    assert result["source_reads"] == 4
    assert result["source_reopens"] == 0
    assert result["target_executed"] is False


def test_forbidden_dynamic_import_and_path_fixtures_fail_closed() -> None:
    assert auditor._has_dynamic_import_or_file_loader("__import__('x')", auditor.ast.parse("__import__('x')")) is True
    assert auditor._has_sys_path_mutation(auditor.ast.parse("import sys\nsys.path.append('x')")) is True
