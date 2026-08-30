from __future__ import annotations

import copy
from pathlib import Path

import pytest

from scripts.governance import sentigraph_json_framing_static_auditor_v0_1 as auditor


REPO_ROOT = Path(__file__).resolve().parents[3]

SAFE_R4_EVIDENCE_TOPOLOGY = {
    "formal_auditor": {
        "member": "05_STATIC_AUDITOR.py",
        "output": {
            "argument_target": "output",
            "normal_target": "output",
            "failure_target": "output",
            "write_target": "output",
            "writer": "create_only_json",
            "write_count": 1,
            "result_object": "result",
            "writer_payload_source": "result",
            "normal_and_failure_share_result_object": True,
            "writer_payload": "sanitized_result",
        },
        "member_09": {
            "source_target": "output",
            "derives_only_from_output": True,
            "binding_after_final_write": True,
        },
        "sanitizer": {
            "present": True,
            "covers_normal_result": True,
            "covers_failure_safe_result": True,
            "before_final_write": True,
            "sanitized_value": "sanitized_result",
            "writer_consumes": "sanitized_result",
        },
    },
    "orchestrator": {
        "member": "01_RUNTIME_CANARY_ORCHESTRATOR.py",
        "host_attestation": {
            "validated": True,
            "sanitized": True,
            "allowed_origin_mapping_validated": True,
            "validated_before_runtime_admission": True,
            "origin": "host_attested_pre_runtime",
            "receipt_path": "/planned_final_receipt/accepted_package_identity/outer_identity",
            "builder_role": "host_attestation_outer_identity",
            "evidence_object": "outer_identity",
        },
        "package_validation": {
            "validated": True,
            "manifest_and_sha256sums_verified": True,
            "independent_from_host_attestation": True,
            "origin": "package_validated",
            "receipt_path": "/planned_final_receipt/package_member_validation",
            "builder_role": "package_member_validation",
            "evidence_object": "package_member_validation",
        },
        "provenance": {
            "distinct_objects": True,
            "distinct_origin_classes": True,
            "distinct_builder_roles": True,
            "guard_present": True,
            "guard_effective": True,
            "guard_inputs": ["outer_identity", "package_member_validation"],
        },
    },
    "preinteraction": {
        "controller_member": "02_RUNTIME_CANARY_CONTROLLER.cjs",
        "fixture_member": "06_PUBLIC_END_TO_END_FIXTURES.json",
        "consumer_member": "05_STATIC_AUDITOR.py",
        "fixtures": [
            {
                "identity": "fixture_formal_state",
                "method": "GET",
                "route": "/api/v1/internal/alpha/governed-review-decisions/formal-state",
                "request_counter": "/base/controller_raw/fixture_formal_state_request_count",
                "fulfill_counter": "/base/controller_raw/fixture_formal_state_fulfill_count",
                "request_key": "fixture_formal_state_request_count",
                "fulfill_key": "fixture_formal_state_fulfill_count",
                "request_count": 1,
                "fulfill_count": 1,
            },
            {
                "identity": "fixture_local_exchange_samples",
                "method": "GET",
                "route": "/api/v1/internal/alpha/review-console/local-exchange-samples",
                "request_counter": "/base/controller_raw/fixture_local_exchange_samples_request_count",
                "fulfill_counter": "/base/controller_raw/fixture_local_exchange_samples_fulfill_count",
                "request_key": "fixture_local_exchange_samples_request_count",
                "fulfill_key": "fixture_local_exchange_samples_fulfill_count",
                "request_count": 1,
                "fulfill_count": 1,
            },
            {
                "identity": "fixture_governed_review_projection",
                "method": "GET",
                "route": "/api/v1/internal/alpha/review-console/projections/governed-nonproduction-record-review-v0-1",
                "request_counter": "/base/controller_raw/fixture_governed_review_projection_request_count",
                "fulfill_counter": "/base/controller_raw/fixture_governed_review_projection_fulfill_count",
                "request_key": "fixture_governed_review_projection_request_count",
                "fulfill_key": "fixture_governed_review_projection_fulfill_count",
                "request_count": 1,
                "fulfill_count": 1,
            },
        ],
        "aggregate": {"expected": 3, "completed": 3, "fulfilled": 3},
        "unexpected_api_request_count": 0,
        "gate_uses_exact_fixture_pairs": True,
        "broad_api_fail_closed_before_interaction": True,
    },
}


def _mutated_r4_topology(path: tuple[str | int, ...], value: object) -> dict[str, object]:
    topology = copy.deepcopy(SAFE_R4_EVIDENCE_TOPOLOGY)
    cursor: object = topology
    for part in path[:-1]:
        cursor = cursor[part]  # type: ignore[index]
    cursor[path[-1]] = value  # type: ignore[index]
    return topology


R4_TOPOLOGY_NEGATIVE_FIXTURES = (
    (
        "R4_SG1_SECOND_OUTPUT_WRITER",
        "auditor_single_output_target",
        ("formal_auditor", "output", "write_count"),
        2,
    ),
    (
        "R4_SG1_FAILURE_TARGET_NOT_SHARED",
        "auditor_single_output_target",
        ("formal_auditor", "output", "failure_target"),
        "alternate_output",
    ),
    (
        "R4_SG1_MEMBER09_ALTERNATE_TARGET",
        "auditor_single_output_target",
        ("formal_auditor", "member_09", "source_target"),
        "alternate_output",
    ),
    (
        "R4_SG1_SANITIZER_REMOVED",
        "sanitizer_present",
        ("formal_auditor", "sanitizer", "present"),
        False,
    ),
    (
        "R4_SG1_SANITIZER_AFTER_WRITE",
        "sanitizer_present",
        ("formal_auditor", "sanitizer", "before_final_write"),
        False,
    ),
    (
        "R4_SG1_WRITER_CONSUMES_UNSANITIZED_RESULT",
        "sanitizer_present",
        ("formal_auditor", "output", "writer_payload"),
        "result",
    ),
    (
        "R4_SG2_HOST_GATE_TO_ORIGIN_FLOW_BROKEN",
        "outer_origin_host_attested",
        ("orchestrator", "host_attestation", "validated"),
        False,
    ),
    (
        "R4_SG2_HOST_ORIGIN_REPLACED",
        "outer_origin_host_attested",
        ("orchestrator", "host_attestation", "origin"),
        "package_validated",
    ),
    (
        "R4_SG2_PACKAGE_GATE_TO_ORIGIN_FLOW_BROKEN",
        "package_origin_validated",
        ("orchestrator", "package_validation", "manifest_and_sha256sums_verified"),
        False,
    ),
    (
        "R4_SG2_PACKAGE_NOT_INDEPENDENT",
        "package_origin_validated",
        ("orchestrator", "package_validation", "independent_from_host_attestation"),
        False,
    ),
    (
        "R4_SG2_PROVENANCE_OBJECT_ALIAS",
        "provenance_not_collapsed",
        ("orchestrator", "package_validation", "evidence_object"),
        "outer_identity",
    ),
    (
        "R4_SG2_PROVENANCE_BUILDER_ROLE_COLLAPSE",
        "provenance_not_collapsed",
        ("orchestrator", "package_validation", "builder_role"),
        "host_attestation_outer_identity",
    ),
    (
        "R4_SG2_NON_COLLAPSE_GUARD_INEFFECTIVE",
        "provenance_not_collapsed",
        ("orchestrator", "provenance", "guard_effective"),
        False,
    ),
    (
        "R4_SG3_CANONICAL_ROUTE_REPLACED",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "route"),
        "/api/v1/internal/alpha/governed-review-decisions/replaced-formal-state",
    ),
    (
        "R4_SG3_DUPLICATE_ROUTE_SUBSTITUTION",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 1, "route"),
        "/api/v1/internal/alpha/governed-review-decisions/formal-state",
    ),
    (
        "R4_SG3_REQUEST_COUNTER_WRONG_ROUTE_PAIR",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "request_key"),
        "fixture_local_exchange_samples_request_count",
    ),
    (
        "R4_SG3_FULFILL_COUNTER_WRONG_ROUTE_PAIR",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "fulfill_key"),
        "fixture_local_exchange_samples_fulfill_count",
    ),
    (
        "R4_SG3_REQUEST_COUNTER_NOT_ONE",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "request_count"),
        2,
    ),
    (
        "R4_SG3_FULFILL_COUNTER_NOT_ONE",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "fulfill_count"),
        2,
    ),
    (
        "R4_SG3_AGGREGATE_THREE_BUT_PER_FIXTURE_BINDING_WRONG",
        "preinteraction_fixtures_three",
        ("preinteraction", "fixtures", 0, "request_counter"),
        "/base/controller_raw/fixture_local_exchange_samples_request_count",
    ),
)

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


SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE = '''
def build_preinteraction_fixture_evidence(controller_raw):
    fixture_formal_state = {
        "identity": "fixture_formal_state",
        "method": "GET",
        "route": "/api/v1/internal/alpha/governed-review-decisions/formal-state",
        "request_counter": "/base/controller_raw/fixture_formal_state_request_count",
        "fulfill_counter": "/base/controller_raw/fixture_formal_state_fulfill_count",
        "request_count": controller_raw["fixture_formal_state_request_count"],
        "fulfill_count": controller_raw["fixture_formal_state_fulfill_count"],
    }
    fixture_local_exchange_samples = {
        "identity": "fixture_local_exchange_samples",
        "method": "GET",
        "route": "/api/v1/internal/alpha/review-console/local-exchange-samples",
        "request_counter": "/base/controller_raw/fixture_local_exchange_samples_request_count",
        "fulfill_counter": "/base/controller_raw/fixture_local_exchange_samples_fulfill_count",
        "request_count": controller_raw["fixture_local_exchange_samples_request_count"],
        "fulfill_count": controller_raw["fixture_local_exchange_samples_fulfill_count"],
    }
    fixture_governed_review_projection = {
        "identity": "fixture_governed_review_projection",
        "method": "GET",
        "route": "/api/v1/internal/alpha/review-console/projections/governed-nonproduction-record-review-v0-1",
        "request_counter": "/base/controller_raw/fixture_governed_review_projection_request_count",
        "fulfill_counter": "/base/controller_raw/fixture_governed_review_projection_fulfill_count",
        "request_count": controller_raw["fixture_governed_review_projection_request_count"],
        "fulfill_count": controller_raw["fixture_governed_review_projection_fulfill_count"],
    }
    expected = 3
    completed = 3
    fulfilled = 3
    unexpected_api_request_count = controller_raw["unexpected_api_request_count"]
    exact_fixture_contract = (
        fixture_formal_state["request_count"] == 1
        and fixture_formal_state["fulfill_count"] == 1
        and fixture_local_exchange_samples["request_count"] == 1
        and fixture_local_exchange_samples["fulfill_count"] == 1
        and fixture_governed_review_projection["request_count"] == 1
        and fixture_governed_review_projection["fulfill_count"] == 1
    )
    broad_api_fail_closed = (
        exact_fixture_contract
        and expected == 3
        and completed == 3
        and fulfilled == 3
        and unexpected_api_request_count == 0
    )
    if not broad_api_fail_closed:
        raise ValueError("preinteraction_fixture_contract_failed")
    return {
        "preinteraction_fixtures": [
            fixture_formal_state,
            fixture_local_exchange_samples,
            fixture_governed_review_projection,
        ],
        "expected": expected,
        "completed": completed,
        "fulfilled": fulfilled,
        "unexpected_api_request_count": unexpected_api_request_count,
        "broad_api_fail_closed": broad_api_fail_closed,
    }
'''


SG3_NEGATIVE_FIXTURES = (
    (
        "CANONICAL_ROUTE_REPLACED",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            '"route": "/api/v1/internal/alpha/governed-review-decisions/formal-state"',
            '"route": "/api/v1/internal/alpha/governed-review-decisions/replaced-formal-state"',
        ),
    ),
    (
        "DUPLICATE_ROUTE_SUBSTITUTION",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            '"route": "/api/v1/internal/alpha/review-console/local-exchange-samples"',
            '"route": "/api/v1/internal/alpha/governed-review-decisions/formal-state"',
        ),
    ),
    (
        "REQUEST_COUNTER_WRONG_ROUTE_PAIR",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            '"request_counter": "/base/controller_raw/fixture_formal_state_request_count"',
            '"request_counter": "/base/controller_raw/fixture_local_exchange_samples_request_count"',
        ).replace(
            '"request_count": controller_raw["fixture_formal_state_request_count"]',
            '"request_count": controller_raw["fixture_local_exchange_samples_request_count"]',
        ),
    ),
    (
        "FULFILL_COUNTER_WRONG_ROUTE_PAIR",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            '"fulfill_counter": "/base/controller_raw/fixture_formal_state_fulfill_count"',
            '"fulfill_counter": "/base/controller_raw/fixture_local_exchange_samples_fulfill_count"',
        ).replace(
            '"fulfill_count": controller_raw["fixture_formal_state_fulfill_count"]',
            '"fulfill_count": controller_raw["fixture_local_exchange_samples_fulfill_count"]',
        ),
    ),
    (
        "REQUEST_COUNTER_NOT_ONE",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            'fixture_formal_state["request_count"] == 1',
            'fixture_formal_state["request_count"] == 2',
        ),
    ),
    (
        "FULFILL_COUNTER_NOT_ONE",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            'fixture_formal_state["fulfill_count"] == 1',
            'fixture_formal_state["fulfill_count"] == 2',
        ),
    ),
    (
        "AGGREGATE_THREE_OF_THREE_BUT_PER_FIXTURE_BINDING_WRONG",
        SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE.replace(
            'fixture_formal_state["request_count"] == 1',
            'fixture_local_exchange_samples["request_count"] == 1',
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


def test_sg3_preinteraction_fixture_bindings_positive() -> None:
    result = auditor.audit_preinteraction_fixture_bindings_source(SAFE_SG3_PREINTERACTION_FIXTURE_SOURCE)

    assert result["status"] == "pass"
    assert result["checks"] == {"preinteraction_fixtures_three": True}
    assert result["target_executed"] is False


@pytest.mark.parametrize(
    ("semantic_label", "fixture_source"),
    SG3_NEGATIVE_FIXTURES,
    ids=[fixture[0] for fixture in SG3_NEGATIVE_FIXTURES],
)
def test_sg3_preinteraction_fixture_negative_fixtures_fail_closed(
    semantic_label: str,
    fixture_source: str,
) -> None:
    result = auditor.audit_preinteraction_fixture_bindings_source(fixture_source)

    assert semantic_label
    assert result["status"] == "fail"
    assert result["checks"]["preinteraction_fixtures_three"] is False
    assert result["target_executed"] is False


def test_accepted_r4_evidence_topology_proves_exactly_six_semantic_invariants() -> None:
    result = auditor.audit_existing_r4_evidence_topology(SAFE_R4_EVIDENCE_TOPOLOGY)

    assert result["status"] == "pass"
    assert result["check_count"] == 6
    assert result["exact_check_set"] is True
    assert result["checks"] == {
        "auditor_single_output_target": True,
        "sanitizer_present": True,
        "outer_origin_host_attested": True,
        "package_origin_validated": True,
        "provenance_not_collapsed": True,
        "preinteraction_fixtures_three": True,
    }
    assert result["later_synthetic_helper_shapes_required"] is False
    assert result["package_regeneration_or_materialization_required"] is False
    assert result["target_executed"] is False


@pytest.mark.parametrize(
    ("semantic_label", "target_assertion", "path", "replacement"),
    R4_TOPOLOGY_NEGATIVE_FIXTURES,
    ids=[fixture[0] for fixture in R4_TOPOLOGY_NEGATIVE_FIXTURES],
)
def test_accepted_r4_topology_semantic_edges_fail_closed(
    semantic_label: str,
    target_assertion: str,
    path: tuple[str | int, ...],
    replacement: object,
) -> None:
    topology = _mutated_r4_topology(path, replacement)
    result = auditor.audit_existing_r4_evidence_topology(topology)

    assert semantic_label
    assert result["status"] == "fail"
    assert result["checks"][target_assertion] is False
    assert result["later_synthetic_helper_shapes_required"] is False
    assert result["target_executed"] is False
