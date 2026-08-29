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


SAFE_SG2_ORIGIN_PROVENANCE_SOURCE = '''
def sanitize_host_attestation(raw_host_attestation):
    return raw_host_attestation

def verify_manifest_and_sha256sums(manifest, sha256sums):
    return manifest, sha256sums

def validate_sanitized_host_attestation(raw_host_attestation):
    return sanitize_host_attestation(raw_host_attestation)

def build_outer_identity(validated_host_attestation):
    return {
        "origin_class": "host_attested_pre_runtime",
        "host_attestation": validated_host_attestation,
    }

def validate_package_members(manifest, sha256sums):
    return verify_manifest_and_sha256sums(manifest, sha256sums)

def build_package_member_validation(validated_package_members):
    return {
        "origin_class": "package_validated",
        "package_validation": validated_package_members,
    }

def assert_distinct_provenance(outer_identity, package_member_validation):
    if outer_identity is package_member_validation:
        raise ValueError("provenance_object_alias")
    if outer_identity["origin_class"] == package_member_validation["origin_class"]:
        raise ValueError("provenance_origin_class_collapse")

def build_accepted_package_identity(raw_host_attestation, manifest, sha256sums):
    validated_host_attestation = validate_sanitized_host_attestation(raw_host_attestation)
    outer_identity = build_outer_identity(validated_host_attestation)
    validated_package_members = validate_package_members(manifest, sha256sums)
    package_member_validation = build_package_member_validation(validated_package_members)
    assert_distinct_provenance(outer_identity, package_member_validation)
    accepted_package_identity = {
        "outer_identity": outer_identity,
        "package_member_validation": package_member_validation,
    }
    return accepted_package_identity
'''


SG2_NEGATIVE_FIXTURES = (
    (
        "OUTER_LITERAL_RETAINED_HOST_GATE_BROKEN",
        "outer_origin_host_attested",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    return sanitize_host_attestation(raw_host_attestation)\n",
            "    return raw_host_attestation\n",
        ),
    ),
    (
        "OUTER_WRONG_BUILDER_PROVENANCE",
        "outer_origin_host_attested",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    outer_identity = build_outer_identity(validated_host_attestation)\n",
            "    outer_identity = build_package_member_validation(validated_host_attestation)\n",
        ),
    ),
    (
        "PACKAGE_LITERAL_RETAINED_VALIDATION_GATE_BROKEN",
        "package_origin_validated",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    return verify_manifest_and_sha256sums(manifest, sha256sums)\n",
            "    return manifest\n",
        ),
    ),
    (
        "PACKAGE_WRONG_OR_ALIASED_PROVENANCE",
        "package_origin_validated",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    package_member_validation = build_package_member_validation(validated_package_members)\n",
            "    package_member_validation = outer_identity\n",
        ),
    ),
    (
        "PROVENANCE_SHARED_BUILDER_COLLAPSE",
        "provenance_not_collapsed",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    package_member_validation = build_package_member_validation(validated_package_members)\n",
            "    package_member_validation = build_outer_identity(validated_package_members)\n",
        ),
    ),
    (
        "PROVENANCE_RESULT_OBJECT_ALIAS_COLLAPSE",
        "provenance_not_collapsed",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            '        "package_member_validation": package_member_validation,\n',
            '        "package_member_validation": outer_identity,\n',
        ),
    ),
    (
        "PROVENANCE_NON_COLLAPSE_GUARD_REMOVED",
        "provenance_not_collapsed",
        SAFE_SG2_ORIGIN_PROVENANCE_SOURCE.replace(
            "    assert_distinct_provenance(outer_identity, package_member_validation)\n",
            "    pass\n",
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


def test_sg2_origin_and_provenance_bindings_positive() -> None:
    result = auditor.audit_origin_and_provenance_bindings_source(SAFE_SG2_ORIGIN_PROVENANCE_SOURCE)

    assert result["status"] == "pass"
    assert result["checks"] == {
        "outer_origin_host_attested": True,
        "package_origin_validated": True,
        "provenance_not_collapsed": True,
    }
    assert result["target_executed"] is False


@pytest.mark.parametrize(
    ("semantic_label", "target_assertion", "fixture_source"),
    SG2_NEGATIVE_FIXTURES,
    ids=[fixture[0] for fixture in SG2_NEGATIVE_FIXTURES],
)
def test_sg2_origin_and_provenance_negative_fixtures_fail_closed(
    semantic_label: str,
    target_assertion: str,
    fixture_source: str,
) -> None:
    result = auditor.audit_origin_and_provenance_bindings_source(fixture_source)

    assert semantic_label
    assert result["status"] == "fail"
    assert result["checks"][target_assertion] is False
    assert result["target_executed"] is False
