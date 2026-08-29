from __future__ import annotations

from pathlib import Path

import pytest

from scripts.governance import sentigraph_json_framing_static_auditor_v0_1 as auditor


REPO_ROOT = Path(__file__).resolve().parents[3]

SAFE_FORMAL_AUDITOR_SOURCE = '''
from pathlib import Path

def sanitize_bounded_disclosure(value):
    return value

def serialize_result(value):
    return str(value)

def build_success_result():
    return {"status": "pass"}

def build_failure_result(error):
    return {"status": "fail", "error": str(error)}

def write_result(result, output_target: Path):
    sanitized_result = sanitize_bounded_disclosure(result)
    output_target.write_text(serialize_result(sanitized_result), encoding="utf-8")

def run_formal_audit(output_target: Path, planned_members):
    try:
        result = build_success_result()
    except Exception as error:
        result = build_failure_result(error)
    write_result(result, output_target)
    planned_members["09_STATIC_AUDIT_RESULT.json"] = output_target
'''


SG1_NEGATIVE_FIXTURES = (
    (
        "SECOND_OUTPUT_TARGET",
        "auditor_single_output_target",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            '    planned_members["09_STATIC_AUDIT_RESULT.json"] = output_target\n',
            '    alternate_output_target.write_text(serialize_result(result), encoding="utf-8")\n'
            '    planned_members["09_STATIC_AUDIT_RESULT.json"] = output_target\n',
        ),
    ),
    (
        "FAILURE_SAFE_SHARED_TARGET_BYPASS",
        "auditor_single_output_target",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            '    except Exception as error:\n        result = build_failure_result(error)\n',
            '    except Exception as error:\n'
            '        result = build_failure_result(error)\n'
            '        return write_result(result, failure_output_target)\n',
        ),
    ),
    (
        "MEMBER09_ALTERNATE_TARGET",
        "auditor_single_output_target",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            'planned_members["09_STATIC_AUDIT_RESULT.json"] = output_target',
            'planned_members["09_STATIC_AUDIT_RESULT.json"] = alternate_output_target',
        ),
    ),
    (
        "SANITIZER_REMOVED",
        "sanitizer_present",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            "    sanitized_result = sanitize_bounded_disclosure(result)\n",
            "    sanitized_result = result\n",
        ),
    ),
    (
        "SANITIZER_AFTER_WRITE",
        "sanitizer_present",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            "    sanitized_result = sanitize_bounded_disclosure(result)\n"
            "    output_target.write_text(serialize_result(sanitized_result), encoding=\"utf-8\")\n",
            "    output_target.write_text(serialize_result(result), encoding=\"utf-8\")\n"
            "    sanitized_result = sanitize_bounded_disclosure(result)\n",
        ),
    ),
    (
        "ALTERNATE_UNSANITIZED_FAILURE_SAFE_WRITER",
        "sanitizer_present",
        SAFE_FORMAL_AUDITOR_SOURCE.replace(
            "def run_formal_audit(output_target: Path, planned_members):\n",
            "def write_failure_result(result, output_target: Path):\n"
            "    output_target.write_text(serialize_result(result), encoding=\"utf-8\")\n\n"
            "def run_formal_audit(output_target: Path, planned_members):\n",
        ).replace(
            '    except Exception as error:\n        result = build_failure_result(error)\n',
            '    except Exception as error:\n'
            '        result = build_failure_result(error)\n'
            '        return write_failure_result(result, output_target)\n',
        ),
    ),
)


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


def test_sg1_formal_auditor_self_emission_bindings_positive() -> None:
    result = auditor.audit_formal_auditor_self_emission_source(SAFE_FORMAL_AUDITOR_SOURCE)

    assert result["status"] == "pass"
    assert result["checks"] == {
        "auditor_single_output_target": True,
        "sanitizer_present": True,
    }
    assert result["target_executed"] is False


@pytest.mark.parametrize(
    ("semantic_label", "target_assertion", "fixture_source"),
    SG1_NEGATIVE_FIXTURES,
    ids=[fixture[0] for fixture in SG1_NEGATIVE_FIXTURES],
)
def test_sg1_formal_auditor_self_emission_negative_fixtures_fail_closed(
    semantic_label: str,
    target_assertion: str,
    fixture_source: str,
) -> None:
    result = auditor.audit_formal_auditor_self_emission_source(fixture_source)

    assert semantic_label
    assert result["status"] == "fail"
    assert result["checks"][target_assertion] is False
    assert result["target_executed"] is False
