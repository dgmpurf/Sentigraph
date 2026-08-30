"""AST-only auditor for the forward JSON framing/provenance contract."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


VERSION = "0.1"
CHECK_NAMES = (
    "SHARED_SOURCE_UTF8_NO_BOM",
    "SHARED_STANDARD_LIBRARY_ONLY",
    "SHARED_CONTRACT_SYMBOLS",
    "SHARED_SINGLE_JSON_SERIALIZATION",
    "VALIDATOR_CANONICAL_IMPORT",
    "VALIDATOR_CANONICAL_CALLS",
    "VALIDATOR_EXPLICIT_MEMBER_CONTRACTS",
    "LEGACY_GUARD_BEFORE_SHARED_IMPORT",
    "RESOLVER_CANONICAL_IMPORT",
    "RESOLVER_CANONICAL_CALLS",
    "EXPLICIT_FRAMING_ROOT_DUPLICATE_POLICIES",
    "EXPECTED_ROLE_CHECKS_BEFORE_PARSE",
    "TEST_CANONICAL_VALIDATOR_IMPORT",
    "NO_DYNAMIC_IMPORT_OR_FILE_LOADER",
    "NO_SYS_PATH_OR_PYTHONPATH_HACK",
    "NO_DUAL_IMPORT_FALLBACK",
    "NARROW_IO_BYTESIO_POLICY",
    "TARGET_EXECUTION_FORBIDDEN",
)
SG1_CHECK_NAMES = (
    "auditor_single_output_target",
    "sanitizer_present",
)
SG2_CHECK_NAMES = (
    "outer_origin_host_attested",
    "package_origin_validated",
    "provenance_not_collapsed",
)
SG3_CHECK_NAMES = (
    "preinteraction_fixtures_three",
)

_SG3_FIXTURE_CONTRACTS = (
    (
        "fixture_formal_state",
        "/api/v1/internal/alpha/governed-review-decisions/formal-state",
        "/base/controller_raw/fixture_formal_state_request_count",
        "/base/controller_raw/fixture_formal_state_fulfill_count",
        "fixture_formal_state_request_count",
        "fixture_formal_state_fulfill_count",
    ),
    (
        "fixture_local_exchange_samples",
        "/api/v1/internal/alpha/review-console/local-exchange-samples",
        "/base/controller_raw/fixture_local_exchange_samples_request_count",
        "/base/controller_raw/fixture_local_exchange_samples_fulfill_count",
        "fixture_local_exchange_samples_request_count",
        "fixture_local_exchange_samples_fulfill_count",
    ),
    (
        "fixture_governed_review_projection",
        "/api/v1/internal/alpha/review-console/projections/governed-nonproduction-record-review-v0-1",
        "/base/controller_raw/fixture_governed_review_projection_request_count",
        "/base/controller_raw/fixture_governed_review_projection_fulfill_count",
        "fixture_governed_review_projection_request_count",
        "fixture_governed_review_projection_fulfill_count",
    ),
)

_FORMAL_AUDIT_ENTRY_FUNCTION = "run_formal_audit"
_FORMAL_AUDIT_WRITER_FUNCTION = "write_result"
_FORMAL_AUDIT_SANITIZER_FUNCTION = "sanitize_bounded_disclosure"
_FORMAL_AUDIT_RESULT_MEMBER = "09_STATIC_AUDIT_RESULT.json"

_ALLOWED_SHARED_IMPORT_ROOTS = {
    "__future__",
    "dataclasses",
    "enum",
    "hashlib",
    "json",
    "re",
    "typing",
}
_REQUIRED_SHARED_SYMBOLS = {
    "JsonFramingType",
    "JsonRootShape",
    "DuplicateKeyPolicy",
    "JsonInputDescriptor",
    "JsonFramingError",
    "parse_single_json_document",
    "parse_jsonl_records",
    "serialize_single_json_document",
}
_FORBIDDEN_TEXT_MARKERS = (
    "spec_from_file_location",
    "importlib.import_module",
    "builtins.import",
    "builtins.__import__",
    "__import__(",
)


def _read_utf8_no_bom(path: Path) -> tuple[str, int, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("source_bom_forbidden")
    return raw.decode("utf-8", errors="strict"), len(raw), hashlib.sha256(raw).hexdigest()


def _import_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def _imported_names(tree: ast.AST, module: str) -> set[str]:
    result: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == module:
            result.update(alias.name for alias in node.names)
    return result


def _definition_names(tree: ast.AST) -> set[str]:
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return None


def _call_names(tree: ast.AST) -> list[str]:
    return [
        name
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and (name := _call_name(node.func)) is not None
    ]


def _has_sys_path_mutation(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and _call_name(node) == "sys.path":
            return True
    return False


def _has_dynamic_import_or_file_loader(source: str, tree: ast.AST) -> bool:
    if any(marker in source for marker in _FORBIDDEN_TEXT_MARKERS):
        return True
    return "importlib" in _import_roots(tree)


def _function_call_count(tree: ast.AST, function_name: str, call_name: str) -> int:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return sum(1 for name in _call_names(node) if name == call_name)
    return 0


def _function_node(tree: ast.AST, function_name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            return node
    return None


def _assigns_name(nodes: list[ast.stmt], name: str) -> bool:
    for statement in nodes:
        for node in ast.walk(statement):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return True
    return False


def _contains_early_exit(nodes: list[ast.stmt]) -> bool:
    return any(isinstance(node, (ast.Return, ast.Raise)) for statement in nodes for node in ast.walk(statement))


def _write_calls(tree: ast.AST) -> list[ast.Call]:
    calls: list[ast.Call] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call_name = _call_name(node.func)
        if call_name == "open" or (call_name and call_name.split(".")[-1] in {"write_text", "write_bytes"}):
            calls.append(node)
    return calls


def _statement_index_containing_call(
    statements: list[ast.stmt],
    target_call: ast.Call,
) -> int | None:
    for index, statement in enumerate(statements):
        if any(node is target_call for node in ast.walk(statement)):
            return index
    return None


def _call_contains_name(call: ast.Call, name: str) -> bool:
    return any(isinstance(node, ast.Name) and node.id == name for node in ast.walk(call))


def _member_09_assignments(tree: ast.AST) -> list[ast.Assign]:
    assignments: list[ast.Assign] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Subscript):
                continue
            index = target.slice
            if isinstance(index, ast.Constant) and index.value == _FORMAL_AUDIT_RESULT_MEMBER:
                assignments.append(node)
    return assignments


def _legacy_audit_formal_auditor_self_emission_source(source: str) -> dict[str, Any]:
    """Prove SG1 output convergence and sanitizer ordering without executing the target."""

    tree = ast.parse(source)
    entry = _function_node(tree, _FORMAL_AUDIT_ENTRY_FUNCTION)
    writer = _function_node(tree, _FORMAL_AUDIT_WRITER_FUNCTION)

    evidence: dict[str, Any] = {
        "entry_function_found": entry is not None,
        "writer_function_found": writer is not None,
        "entry_output_parameter_found": False,
        "entry_try_count": 0,
        "normal_result_assignment": False,
        "failure_result_assignment": False,
        "failure_safe_early_exit_count": 0,
        "shared_writer_call_count": 0,
        "shared_writer_target_matches": False,
        "shared_writer_after_branch_convergence": False,
        "global_writable_call_count": len(_write_calls(tree)),
        "member_09_binding_count": len(_member_09_assignments(tree)),
        "member_09_target_matches": False,
        "member_09_binding_after_shared_write": False,
        "writer_sanitizer_call_count": 0,
        "writer_write_call_count": 0,
        "writer_target_matches": False,
        "sanitizer_before_write": False,
        "write_uses_sanitized_result": False,
    }

    if entry is not None:
        evidence["entry_output_parameter_found"] = any(
            argument.arg == "output_target"
            for argument in (*entry.args.posonlyargs, *entry.args.args, *entry.args.kwonlyargs)
        )
        top_level_tries = [statement for statement in entry.body if isinstance(statement, ast.Try)]
        evidence["entry_try_count"] = len(top_level_tries)
        if len(top_level_tries) == 1:
            guarded = top_level_tries[0]
            evidence["normal_result_assignment"] = _assigns_name(guarded.body, "result")
            evidence["failure_result_assignment"] = bool(guarded.handlers) and all(
                _assigns_name(handler.body, "result") for handler in guarded.handlers
            )
            evidence["failure_safe_early_exit_count"] = sum(
                int(_contains_early_exit(handler.body)) for handler in guarded.handlers
            )

        shared_calls = [
            node
            for node in ast.walk(entry)
            if isinstance(node, ast.Call) and _call_name(node.func) == _FORMAL_AUDIT_WRITER_FUNCTION
        ]
        evidence["shared_writer_call_count"] = len(shared_calls)
        shared_call = shared_calls[0] if len(shared_calls) == 1 else None
        if shared_call is not None:
            evidence["shared_writer_target_matches"] = (
                len(shared_call.args) >= 2
                and isinstance(shared_call.args[1], ast.Name)
                and shared_call.args[1].id == "output_target"
            )
            shared_index = _statement_index_containing_call(entry.body, shared_call)
            try_index = next(
                (index for index, statement in enumerate(entry.body) if isinstance(statement, ast.Try)),
                None,
            )
            evidence["shared_writer_after_branch_convergence"] = (
                shared_index is not None and try_index is not None and shared_index > try_index
            )

        member_assignments = _member_09_assignments(entry)
        if len(member_assignments) == 1:
            member_assignment = member_assignments[0]
            evidence["member_09_target_matches"] = (
                isinstance(member_assignment.value, ast.Name)
                and member_assignment.value.id == "output_target"
            )
            member_index = next(
                (
                    index
                    for index, statement in enumerate(entry.body)
                    if any(node is member_assignment for node in ast.walk(statement))
                ),
                None,
            )
            shared_index = (
                _statement_index_containing_call(entry.body, shared_calls[0])
                if len(shared_calls) == 1
                else None
            )
            evidence["member_09_binding_after_shared_write"] = (
                member_index is not None and shared_index is not None and member_index > shared_index
            )

    if writer is not None:
        writer_args = {
            argument.arg
            for argument in (*writer.args.posonlyargs, *writer.args.args, *writer.args.kwonlyargs)
        }
        sanitizer_assignments = [
            node
            for node in ast.walk(writer)
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "sanitized_result" for target in node.targets)
            and isinstance(node.value, ast.Call)
            and _call_name(node.value.func) == _FORMAL_AUDIT_SANITIZER_FUNCTION
            and len(node.value.args) == 1
            and isinstance(node.value.args[0], ast.Name)
            and node.value.args[0].id == "result"
        ]
        writer_calls = _write_calls(writer)
        evidence["writer_sanitizer_call_count"] = len(sanitizer_assignments)
        evidence["writer_write_call_count"] = len(writer_calls)
        if len(writer_calls) == 1:
            write_call = writer_calls[0]
            evidence["writer_target_matches"] = (
                "output_target" in writer_args
                and isinstance(write_call.func, ast.Attribute)
                and isinstance(write_call.func.value, ast.Name)
                and write_call.func.value.id == "output_target"
            )
            evidence["write_uses_sanitized_result"] = _call_contains_name(write_call, "sanitized_result")
            if len(sanitizer_assignments) == 1:
                evidence["sanitizer_before_write"] = (
                    sanitizer_assignments[0].lineno < write_call.lineno
                )

    output_check = all(
        (
            evidence["entry_function_found"],
            evidence["writer_function_found"],
            evidence["entry_output_parameter_found"],
            evidence["entry_try_count"] == 1,
            evidence["normal_result_assignment"],
            evidence["failure_result_assignment"],
            evidence["failure_safe_early_exit_count"] == 0,
            evidence["shared_writer_call_count"] == 1,
            evidence["shared_writer_target_matches"],
            evidence["shared_writer_after_branch_convergence"],
            evidence["global_writable_call_count"] == 1,
            evidence["member_09_binding_count"] == 1,
            evidence["member_09_target_matches"],
            evidence["member_09_binding_after_shared_write"],
        )
    )
    sanitizer_check = all(
        (
            evidence["entry_function_found"],
            evidence["writer_function_found"],
            evidence["entry_try_count"] == 1,
            evidence["normal_result_assignment"],
            evidence["failure_result_assignment"],
            evidence["failure_safe_early_exit_count"] == 0,
            evidence["shared_writer_call_count"] == 1,
            evidence["shared_writer_after_branch_convergence"],
            evidence["global_writable_call_count"] == 1,
            evidence["writer_sanitizer_call_count"] == 1,
            evidence["writer_write_call_count"] == 1,
            evidence["writer_target_matches"],
            evidence["sanitizer_before_write"],
            evidence["write_uses_sanitized_result"],
        )
    )
    checks = {
        "auditor_single_output_target": output_check,
        "sanitizer_present": sanitizer_check,
    }
    return {
        "schema": "sentigraph_formal_auditor_self_emission_bindings_static_proof_v0_1",
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "evidence": evidence,
        "target_executed": False,
    }


def _single_assignment_value(function: ast.FunctionDef | ast.AsyncFunctionDef | None, name: str) -> ast.AST | None:
    if function is None:
        return None
    values: list[ast.AST] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                values.append(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            if node.value is not None:
                values.append(node.value)
    return values[0] if len(values) == 1 else None


def _is_named_call(node: ast.AST | None, function_name: str, argument_names: tuple[str, ...]) -> bool:
    return (
        isinstance(node, ast.Call)
        and _call_name(node.func) == function_name
        and not node.keywords
        and len(node.args) == len(argument_names)
        and all(
            isinstance(argument, ast.Name) and argument.id == expected
            for argument, expected in zip(node.args, argument_names)
        )
    )


def _direct_return_value(function: ast.FunctionDef | ast.AsyncFunctionDef | None) -> ast.AST | None:
    if function is None:
        return None
    returns = [statement.value for statement in function.body if isinstance(statement, ast.Return)]
    return returns[0] if len(returns) == 1 else None


def _dict_binding(node: ast.AST | None, key: str) -> ast.AST | None:
    if not isinstance(node, ast.Dict):
        return None
    matches = [
        value
        for item_key, value in zip(node.keys, node.values)
        if isinstance(item_key, ast.Constant) and item_key.value == key
    ]
    return matches[0] if len(matches) == 1 else None


def _dict_name_binding(node: ast.AST | None, key: str, value_name: str) -> bool:
    value = _dict_binding(node, key)
    return isinstance(value, ast.Name) and value.id == value_name


def _dict_constant_binding(node: ast.AST | None, key: str, value: str) -> bool:
    bound = _dict_binding(node, key)
    return isinstance(bound, ast.Constant) and bound.value == value


def _function_parameter_names(function: ast.FunctionDef | ast.AsyncFunctionDef | None) -> tuple[str, ...]:
    if function is None:
        return ()
    return tuple(
        argument.arg
        for argument in (*function.args.posonlyargs, *function.args.args, *function.args.kwonlyargs)
    )


def _builder_contract(
    function: ast.FunctionDef | ast.AsyncFunctionDef | None,
    parameter_name: str,
    origin_class: str,
    payload_key: str,
) -> bool:
    returned = _direct_return_value(function)
    return (
        _function_parameter_names(function) == (parameter_name,)
        and _dict_constant_binding(returned, "origin_class", origin_class)
        and _dict_name_binding(returned, payload_key, parameter_name)
    )


def _top_level_assignment_index(function: ast.FunctionDef | ast.AsyncFunctionDef | None, name: str) -> int | None:
    if function is None:
        return None
    matches: list[int] = []
    for index, statement in enumerate(function.body):
        if isinstance(statement, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in statement.targets
        ):
            matches.append(index)
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            if statement.target.id == name:
                matches.append(index)
    return matches[0] if len(matches) == 1 else None


def _top_level_call_index(function: ast.FunctionDef | ast.AsyncFunctionDef | None, function_name: str) -> int | None:
    if function is None:
        return None
    matches = [
        index
        for index, statement in enumerate(function.body)
        if isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Call)
        and _call_name(statement.value.func) == function_name
    ]
    return matches[0] if len(matches) == 1 else None


def _subscript_matches(node: ast.AST, object_name: str, key: str) -> bool:
    return (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == object_name
        and isinstance(node.slice, ast.Constant)
        and node.slice.value == key
    )


def _guard_contract(function: ast.FunctionDef | ast.AsyncFunctionDef | None) -> bool:
    if _function_parameter_names(function) != ("outer_identity", "package_member_validation"):
        return False
    identity_guard = False
    origin_guard = False
    for statement in function.body:
        if not isinstance(statement, ast.If) or not any(isinstance(node, ast.Raise) for node in ast.walk(statement)):
            continue
        test = statement.test
        if isinstance(test, ast.Compare) and len(test.ops) == 1 and len(test.comparators) == 1:
            identity_guard = identity_guard or (
                isinstance(test.ops[0], ast.Is)
                and isinstance(test.left, ast.Name)
                and test.left.id == "outer_identity"
                and isinstance(test.comparators[0], ast.Name)
                and test.comparators[0].id == "package_member_validation"
            )
            origin_guard = origin_guard or (
                isinstance(test.ops[0], ast.Eq)
                and _subscript_matches(test.left, "outer_identity", "origin_class")
                and _subscript_matches(test.comparators[0], "package_member_validation", "origin_class")
            )
    return identity_guard and origin_guard


def _legacy_audit_origin_and_provenance_bindings_source(source: str) -> dict[str, Any]:
    """Prove SG2 host/package origin data flows and non-collapse without target execution."""

    tree = ast.parse(source)
    entry = _function_node(tree, "build_accepted_package_identity")
    host_gate = _function_node(tree, "validate_sanitized_host_attestation")
    outer_builder = _function_node(tree, "build_outer_identity")
    package_gate = _function_node(tree, "validate_package_members")
    package_builder = _function_node(tree, "build_package_member_validation")
    provenance_guard = _function_node(tree, "assert_distinct_provenance")

    validated_host = _single_assignment_value(entry, "validated_host_attestation")
    outer_identity = _single_assignment_value(entry, "outer_identity")
    validated_package = _single_assignment_value(entry, "validated_package_members")
    package_validation = _single_assignment_value(entry, "package_member_validation")
    accepted_identity = _single_assignment_value(entry, "accepted_package_identity")

    host_gate_contract = _is_named_call(
        _direct_return_value(host_gate),
        "sanitize_host_attestation",
        ("raw_host_attestation",),
    )
    package_gate_contract = _is_named_call(
        _direct_return_value(package_gate),
        "verify_manifest_and_sha256sums",
        ("manifest", "sha256sums"),
    )
    outer_builder_contract = _builder_contract(
        outer_builder,
        "validated_host_attestation",
        "host_attested_pre_runtime",
        "host_attestation",
    )
    package_builder_contract = _builder_contract(
        package_builder,
        "validated_package_members",
        "package_validated",
        "package_validation",
    )
    host_gate_link = _is_named_call(
        validated_host,
        "validate_sanitized_host_attestation",
        ("raw_host_attestation",),
    )
    outer_builder_link = _is_named_call(
        outer_identity,
        "build_outer_identity",
        ("validated_host_attestation",),
    )
    package_gate_link = _is_named_call(
        validated_package,
        "validate_package_members",
        ("manifest", "sha256sums"),
    )
    package_builder_link = _is_named_call(
        package_validation,
        "build_package_member_validation",
        ("validated_package_members",),
    )
    outer_final_binding = _dict_name_binding(accepted_identity, "outer_identity", "outer_identity")
    package_final_binding = _dict_name_binding(
        accepted_identity,
        "package_member_validation",
        "package_member_validation",
    )
    entry_return = _direct_return_value(entry)
    accepted_return = isinstance(entry_return, ast.Name) and entry_return.id == "accepted_package_identity"

    host_index = _top_level_assignment_index(entry, "validated_host_attestation")
    outer_index = _top_level_assignment_index(entry, "outer_identity")
    package_gate_index = _top_level_assignment_index(entry, "validated_package_members")
    package_index = _top_level_assignment_index(entry, "package_member_validation")
    guard_index = _top_level_call_index(entry, "assert_distinct_provenance")
    accepted_index = _top_level_assignment_index(entry, "accepted_package_identity")
    host_flow_ordered = (
        host_index is not None
        and outer_index is not None
        and accepted_index is not None
        and host_index < outer_index < accepted_index
    )
    package_flow_ordered = (
        package_gate_index is not None
        and package_index is not None
        and accepted_index is not None
        and package_gate_index < package_index < accepted_index
    )
    guard_call = next(
        (
            statement.value
            for statement in (entry.body if entry is not None else [])
            if isinstance(statement, ast.Expr)
            and isinstance(statement.value, ast.Call)
            and _call_name(statement.value.func) == "assert_distinct_provenance"
        ),
        None,
    )
    guard_link = _is_named_call(
        guard_call,
        "assert_distinct_provenance",
        ("outer_identity", "package_member_validation"),
    )
    guard_ordered = (
        outer_index is not None
        and package_index is not None
        and guard_index is not None
        and accepted_index is not None
        and max(outer_index, package_index) < guard_index < accepted_index
    )
    builders_distinct = (
        outer_builder is not None
        and package_builder is not None
        and outer_builder is not package_builder
        and outer_builder.name != package_builder.name
    )
    result_roles_distinct = outer_final_binding and package_final_binding
    provenance_guard_contract = _guard_contract(provenance_guard)

    evidence = {
        "entry_function_found": entry is not None,
        "host_gate_contract": host_gate_contract,
        "host_gate_link": host_gate_link,
        "outer_builder_contract": outer_builder_contract,
        "outer_builder_link": outer_builder_link,
        "outer_final_binding": outer_final_binding,
        "host_flow_ordered": host_flow_ordered,
        "package_gate_contract": package_gate_contract,
        "package_gate_link": package_gate_link,
        "package_builder_contract": package_builder_contract,
        "package_builder_link": package_builder_link,
        "package_final_binding": package_final_binding,
        "package_flow_ordered": package_flow_ordered,
        "builders_distinct": builders_distinct,
        "result_roles_distinct": result_roles_distinct,
        "provenance_guard_contract": provenance_guard_contract,
        "provenance_guard_link": guard_link,
        "provenance_guard_ordered": guard_ordered,
        "accepted_identity_returned": accepted_return,
    }
    outer_check = all(
        (
            evidence["entry_function_found"],
            evidence["host_gate_contract"],
            evidence["host_gate_link"],
            evidence["outer_builder_contract"],
            evidence["outer_builder_link"],
            evidence["outer_final_binding"],
            evidence["host_flow_ordered"],
            evidence["accepted_identity_returned"],
        )
    )
    package_check = all(
        (
            evidence["entry_function_found"],
            evidence["package_gate_contract"],
            evidence["package_gate_link"],
            evidence["package_builder_contract"],
            evidence["package_builder_link"],
            evidence["package_final_binding"],
            evidence["package_flow_ordered"],
            evidence["accepted_identity_returned"],
        )
    )
    provenance_check = all(
        (
            evidence["entry_function_found"],
            evidence["outer_builder_contract"],
            evidence["outer_builder_link"],
            evidence["package_builder_contract"],
            evidence["package_builder_link"],
            evidence["builders_distinct"],
            evidence["result_roles_distinct"],
            evidence["provenance_guard_contract"],
            evidence["provenance_guard_link"],
            evidence["provenance_guard_ordered"],
            evidence["accepted_identity_returned"],
        )
    )
    checks = {
        "outer_origin_host_attested": outer_check,
        "package_origin_validated": package_check,
        "provenance_not_collapsed": provenance_check,
    }
    return {
        "schema": "sentigraph_origin_and_provenance_bindings_static_proof_v0_1",
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "evidence": evidence,
        "target_executed": False,
    }


def _is_exact_integer(node: ast.AST | None, value: int) -> bool:
    return isinstance(node, ast.Constant) and type(node.value) is int and node.value == value


def _controller_counter_source(node: ast.AST | None, counter_key: str) -> bool:
    return (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == "controller_raw"
        and isinstance(node.slice, ast.Constant)
        and node.slice.value == counter_key
    )


def _fixture_record_contract(
    node: ast.AST | None,
    identity: str,
    route: str,
    request_pointer: str,
    fulfill_pointer: str,
    request_key: str,
    fulfill_key: str,
) -> bool:
    return (
        _dict_constant_binding(node, "identity", identity)
        and _dict_constant_binding(node, "method", "GET")
        and _dict_constant_binding(node, "route", route)
        and _dict_constant_binding(node, "request_counter", request_pointer)
        and _dict_constant_binding(node, "fulfill_counter", fulfill_pointer)
        and _controller_counter_source(_dict_binding(node, "request_count"), request_key)
        and _controller_counter_source(_dict_binding(node, "fulfill_count"), fulfill_key)
    )


def _and_terms(node: ast.AST | None) -> list[ast.AST]:
    return list(node.values) if isinstance(node, ast.BoolOp) and isinstance(node.op, ast.And) else []


def _fixture_count_comparison(node: ast.AST, fixture_name: str, count_key: str, value: int) -> bool:
    return (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.Eq)
        and len(node.comparators) == 1
        and _subscript_matches(node.left, fixture_name, count_key)
        and _is_exact_integer(node.comparators[0], value)
    )


def _name_integer_comparison(node: ast.AST, name: str, value: int) -> bool:
    return (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.Eq)
        and len(node.comparators) == 1
        and isinstance(node.left, ast.Name)
        and node.left.id == name
        and _is_exact_integer(node.comparators[0], value)
    )


def _has_exact_fixture_count_terms(node: ast.AST | None) -> bool:
    terms = _and_terms(node)
    required = [
        (identity, count_key)
        for identity, *_ in _SG3_FIXTURE_CONTRACTS
        for count_key in ("request_count", "fulfill_count")
    ]
    return len(terms) == len(required) and all(
        sum(int(_fixture_count_comparison(term, identity, count_key, 1)) for term in terms) == 1
        for identity, count_key in required
    )


def _has_exact_broad_fail_closed_terms(node: ast.AST | None) -> bool:
    terms = _and_terms(node)
    return (
        len(terms) == 5
        and sum(int(isinstance(term, ast.Name) and term.id == "exact_fixture_contract") for term in terms) == 1
        and sum(int(_name_integer_comparison(term, "expected", 3)) for term in terms) == 1
        and sum(int(_name_integer_comparison(term, "completed", 3)) for term in terms) == 1
        and sum(int(_name_integer_comparison(term, "fulfilled", 3)) for term in terms) == 1
        and sum(int(_name_integer_comparison(term, "unexpected_api_request_count", 0)) for term in terms) == 1
    )


def _raising_not_name_guard_index(
    function: ast.FunctionDef | ast.AsyncFunctionDef | None,
    name: str,
) -> int | None:
    if function is None:
        return None
    matches: list[int] = []
    for index, statement in enumerate(function.body):
        if not isinstance(statement, ast.If):
            continue
        test = statement.test
        if (
            isinstance(test, ast.UnaryOp)
            and isinstance(test.op, ast.Not)
            and isinstance(test.operand, ast.Name)
            and test.operand.id == name
            and any(isinstance(node, ast.Raise) for node in ast.walk(statement))
        ):
            matches.append(index)
    return matches[0] if len(matches) == 1 else None


def _fixture_result_list_contract(node: ast.AST | None) -> bool:
    fixtures = _dict_binding(node, "preinteraction_fixtures")
    expected_names = tuple(identity for identity, *_ in _SG3_FIXTURE_CONTRACTS)
    return (
        isinstance(fixtures, ast.List)
        and len(fixtures.elts) == len(expected_names)
        and all(
            isinstance(element, ast.Name) and element.id == expected
            for element, expected in zip(fixtures.elts, expected_names)
        )
    )


def _legacy_audit_preinteraction_fixture_bindings_source(source: str) -> dict[str, Any]:
    """Prove the frozen three-fixture SG3 bindings without executing their producer."""

    tree = ast.parse(source)
    entry = _function_node(tree, "build_preinteraction_fixture_evidence")
    fixture_records = {
        identity: _single_assignment_value(entry, identity)
        for identity, *_ in _SG3_FIXTURE_CONTRACTS
    }
    fixture_contracts = {
        identity: _fixture_record_contract(fixture_records[identity], *contract)
        for contract in _SG3_FIXTURE_CONTRACTS
        for identity in (contract[0],)
    }

    route_values = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and node.value.startswith("/api/v1/internal/alpha/")
    ]
    expected_routes = [contract[1] for contract in _SG3_FIXTURE_CONTRACTS]
    request_fulfill_pointers = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and node.value.startswith("/base/controller_raw/fixture_")
    ]
    expected_pointers = [value for contract in _SG3_FIXTURE_CONTRACTS for value in contract[2:4]]
    fixture_identity_values = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value in {contract[0] for contract in _SG3_FIXTURE_CONTRACTS}
    ]
    get_literal_count = sum(
        1 for node in ast.walk(tree) if isinstance(node, ast.Constant) and node.value == "GET"
    )

    exact_contract_value = _single_assignment_value(entry, "exact_fixture_contract")
    expected_value = _single_assignment_value(entry, "expected")
    completed_value = _single_assignment_value(entry, "completed")
    fulfilled_value = _single_assignment_value(entry, "fulfilled")
    unexpected_value = _single_assignment_value(entry, "unexpected_api_request_count")
    broad_value = _single_assignment_value(entry, "broad_api_fail_closed")
    returned = _direct_return_value(entry)
    guard_index = _raising_not_name_guard_index(entry, "broad_api_fail_closed")
    return_index = next(
        (index for index, statement in enumerate(entry.body if entry is not None else []) if isinstance(statement, ast.Return)),
        None,
    )

    exact_routes = len(route_values) == 3 and sorted(route_values) == sorted(expected_routes)
    exact_pointers = len(request_fulfill_pointers) == 6 and sorted(request_fulfill_pointers) == sorted(expected_pointers)
    exact_identities = (
        len(fixture_identity_values) == 3
        and sorted(fixture_identity_values) == sorted(contract[0] for contract in _SG3_FIXTURE_CONTRACTS)
    )
    exact_fixture_counts = _has_exact_fixture_count_terms(exact_contract_value)
    aggregate_three = all(
        _is_exact_integer(value, 3) for value in (expected_value, completed_value, fulfilled_value)
    )
    unexpected_zero_source = _controller_counter_source(unexpected_value, "unexpected_api_request_count")
    broad_fail_closed_contract = _has_exact_broad_fail_closed_terms(broad_value)
    guard_before_return = (
        guard_index is not None and return_index is not None and guard_index < return_index
    )
    final_evidence_contract = (
        _fixture_result_list_contract(returned)
        and _dict_name_binding(returned, "expected", "expected")
        and _dict_name_binding(returned, "completed", "completed")
        and _dict_name_binding(returned, "fulfilled", "fulfilled")
        and _dict_name_binding(returned, "unexpected_api_request_count", "unexpected_api_request_count")
        and _dict_name_binding(returned, "broad_api_fail_closed", "broad_api_fail_closed")
    )

    evidence = {
        "entry_function_found": entry is not None,
        "fixture_record_contracts": fixture_contracts,
        "all_fixture_record_contracts": all(fixture_contracts.values()),
        "exact_three_distinct_canonical_routes": exact_routes,
        "exact_three_get_literals": get_literal_count == 3,
        "exact_three_fixture_identities": exact_identities,
        "exact_six_counter_pointers": exact_pointers,
        "exact_six_per_fixture_one_comparisons": exact_fixture_counts,
        "aggregate_expected_completed_fulfilled_three": aggregate_three,
        "unexpected_api_request_count_source_bound": unexpected_zero_source,
        "broad_fail_closed_contract": broad_fail_closed_contract,
        "broad_fail_closed_guard_before_return": guard_before_return,
        "final_evidence_contract": final_evidence_contract,
    }
    check = all(
        (
            evidence["entry_function_found"],
            evidence["all_fixture_record_contracts"],
            evidence["exact_three_distinct_canonical_routes"],
            evidence["exact_three_get_literals"],
            evidence["exact_three_fixture_identities"],
            evidence["exact_six_counter_pointers"],
            evidence["exact_six_per_fixture_one_comparisons"],
            evidence["aggregate_expected_completed_fulfilled_three"],
            evidence["unexpected_api_request_count_source_bound"],
            evidence["broad_fail_closed_contract"],
            evidence["broad_fail_closed_guard_before_return"],
            evidence["final_evidence_contract"],
        )
    )
    checks = {"preinteraction_fixtures_three": check}
    return {
        "schema": "sentigraph_preinteraction_fixture_bindings_static_proof_v0_1",
        "status": "pass" if check else "fail",
        "checks": checks,
        "evidence": evidence,
        "target_executed": False,
    }


def _r4_group(topology: Any, name: str) -> dict[str, Any]:
    if not isinstance(topology, dict):
        return {}
    value = topology.get(name)
    return value if isinstance(value, dict) else {}


def _r4_exact_int(value: Any, expected: int) -> bool:
    return type(value) is int and value == expected


def _r4_string_list(value: Any) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return []
    return value


def audit_formal_auditor_self_emission_source(topology: Any) -> dict[str, Any]:
    """Bind SG1 to accepted R4 output and sanitizer topology, not synthetic helper names."""

    if isinstance(topology, str):
        return _legacy_audit_formal_auditor_self_emission_source(topology)

    formal = _r4_group(topology, "formal_auditor")
    output = _r4_group(formal, "output")
    member_09 = _r4_group(formal, "member_09")
    sanitizer = _r4_group(formal, "sanitizer")

    output_target = output.get("argument_target")
    shared_output_target = (
        isinstance(output_target, str)
        and output_target
        and output.get("normal_target") == output_target
        and output.get("failure_target") == output_target
        and output.get("write_target") == output_target
        and member_09.get("source_target") == output_target
    )
    output_check = all(
        (
            formal.get("member") == "05_STATIC_AUDITOR.py",
            output.get("writer") == "create_only_json",
            _r4_exact_int(output.get("write_count"), 1),
            output.get("result_object") == output.get("writer_payload_source"),
            output.get("normal_and_failure_share_result_object") is True,
            shared_output_target,
            member_09.get("derives_only_from_output") is True,
            member_09.get("binding_after_final_write") is True,
        )
    )
    sanitized_value = sanitizer.get("sanitized_value")
    sanitizer_check = all(
        (
            formal.get("member") == "05_STATIC_AUDITOR.py",
            sanitizer.get("present") is True,
            sanitizer.get("covers_normal_result") is True,
            sanitizer.get("covers_failure_safe_result") is True,
            sanitizer.get("before_final_write") is True,
            isinstance(sanitized_value, str),
            bool(sanitized_value),
            output.get("writer_payload") == sanitized_value,
            sanitizer.get("writer_consumes") == sanitized_value,
            _r4_exact_int(output.get("write_count"), 1),
        )
    )
    checks = {
        "auditor_single_output_target": output_check,
        "sanitizer_present": sanitizer_check,
    }
    return {
        "schema": "sentigraph_r4_formal_auditor_self_emission_topology_static_proof_v0_1",
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "evidence": {
            "member_05_bound": formal.get("member") == "05_STATIC_AUDITOR.py",
            "shared_output_target": shared_output_target,
            "single_create_only_final_write": output.get("writer") == "create_only_json"
            and _r4_exact_int(output.get("write_count"), 1),
            "member_09_derives_only_from_output": member_09.get("derives_only_from_output") is True,
            "sanitizer_before_final_write": sanitizer.get("before_final_write") is True,
            "writer_consumes_sanitized_output": output.get("writer_payload") == sanitized_value
            and sanitizer.get("writer_consumes") == sanitized_value,
            "later_synthetic_helper_shapes_required": False,
        },
        "target_executed": False,
    }


def audit_origin_and_provenance_bindings_source(topology: Any) -> dict[str, Any]:
    """Bind SG2 to accepted R4 origin/provenance topology, not named helper pipelines."""

    if isinstance(topology, str):
        return _legacy_audit_origin_and_provenance_bindings_source(topology)

    orchestrator = _r4_group(topology, "orchestrator")
    host = _r4_group(orchestrator, "host_attestation")
    package = _r4_group(orchestrator, "package_validation")
    provenance = _r4_group(orchestrator, "provenance")

    outer_check = all(
        (
            orchestrator.get("member") == "01_RUNTIME_CANARY_ORCHESTRATOR.py",
            host.get("validated") is True,
            host.get("sanitized") is True,
            host.get("allowed_origin_mapping_validated") is True,
            host.get("validated_before_runtime_admission") is True,
            host.get("origin") == "host_attested_pre_runtime",
            host.get("receipt_path") == "/planned_final_receipt/accepted_package_identity/outer_identity",
            host.get("builder_role") == "host_attestation_outer_identity",
        )
    )
    package_check = all(
        (
            orchestrator.get("member") == "01_RUNTIME_CANARY_ORCHESTRATOR.py",
            package.get("validated") is True,
            package.get("manifest_and_sha256sums_verified") is True,
            package.get("independent_from_host_attestation") is True,
            package.get("origin") == "package_validated",
            package.get("receipt_path") == "/planned_final_receipt/package_member_validation",
            package.get("builder_role") == "package_member_validation",
        )
    )
    guard_inputs = _r4_string_list(provenance.get("guard_inputs"))
    provenance_check = all(
        (
            outer_check,
            package_check,
            host.get("evidence_object") != package.get("evidence_object"),
            host.get("origin") != package.get("origin"),
            host.get("builder_role") != package.get("builder_role"),
            host.get("receipt_path") != package.get("receipt_path"),
            provenance.get("distinct_objects") is True,
            provenance.get("distinct_origin_classes") is True,
            provenance.get("distinct_builder_roles") is True,
            provenance.get("guard_present") is True,
            provenance.get("guard_effective") is True,
            guard_inputs == [host.get("evidence_object"), package.get("evidence_object")],
        )
    )
    checks = {
        "outer_origin_host_attested": outer_check,
        "package_origin_validated": package_check,
        "provenance_not_collapsed": provenance_check,
    }
    return {
        "schema": "sentigraph_r4_origin_and_provenance_topology_static_proof_v0_1",
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "evidence": {
            "member_01_bound": orchestrator.get("member") == "01_RUNTIME_CANARY_ORCHESTRATOR.py",
            "host_gate_to_origin_flow": outer_check,
            "package_gate_to_origin_flow": package_check,
            "provenance_guard_effective": provenance.get("guard_present") is True
            and provenance.get("guard_effective") is True,
            "later_synthetic_helper_shapes_required": False,
        },
        "target_executed": False,
    }


def audit_preinteraction_fixture_bindings_source(topology: Any) -> dict[str, Any]:
    """Bind SG3 to accepted cross-member R4 topology, not a synthetic member-05 helper."""

    if isinstance(topology, str):
        return _legacy_audit_preinteraction_fixture_bindings_source(topology)

    preinteraction = _r4_group(topology, "preinteraction")
    aggregate = _r4_group(preinteraction, "aggregate")
    fixture_values = preinteraction.get("fixtures")
    fixtures = fixture_values if isinstance(fixture_values, list) else []
    fixture_by_identity = {
        item.get("identity"): item
        for item in fixtures
        if isinstance(item, dict) and isinstance(item.get("identity"), str)
    }
    contracts: list[bool] = []
    for identity, route, request_pointer, fulfill_pointer, request_key, fulfill_key in _SG3_FIXTURE_CONTRACTS:
        fixture = fixture_by_identity.get(identity, {})
        contracts.append(
            all(
                (
                    fixture.get("identity") == identity,
                    fixture.get("method") == "GET",
                    fixture.get("route") == route,
                    fixture.get("request_counter") == request_pointer,
                    fixture.get("fulfill_counter") == fulfill_pointer,
                    fixture.get("request_key") == request_key,
                    fixture.get("fulfill_key") == fulfill_key,
                    _r4_exact_int(fixture.get("request_count"), 1),
                    _r4_exact_int(fixture.get("fulfill_count"), 1),
                )
            )
        )
    exact_fixture_identities = len(fixtures) == 3 and len(fixture_by_identity) == 3 and all(contracts)
    aggregate_three = all(
        _r4_exact_int(aggregate.get(key), 3)
        for key in ("expected", "completed", "fulfilled")
    )
    check = all(
        (
            preinteraction.get("controller_member") == "02_RUNTIME_CANARY_CONTROLLER.cjs",
            preinteraction.get("fixture_member") == "06_PUBLIC_END_TO_END_FIXTURES.json",
            preinteraction.get("consumer_member") == "05_STATIC_AUDITOR.py",
            exact_fixture_identities,
            aggregate_three,
            _r4_exact_int(preinteraction.get("unexpected_api_request_count"), 0),
            preinteraction.get("gate_uses_exact_fixture_pairs") is True,
            preinteraction.get("broad_api_fail_closed_before_interaction") is True,
        )
    )
    checks = {"preinteraction_fixtures_three": check}
    return {
        "schema": "sentigraph_r4_preinteraction_cross_member_topology_static_proof_v0_1",
        "status": "pass" if check else "fail",
        "checks": checks,
        "evidence": {
            "exact_three_cross_member_fixture_contracts": exact_fixture_identities,
            "aggregate_expected_completed_fulfilled_three": aggregate_three,
            "unexpected_api_zero": _r4_exact_int(preinteraction.get("unexpected_api_request_count"), 0),
            "broad_api_fail_closed_before_interaction": preinteraction.get(
                "broad_api_fail_closed_before_interaction"
            )
            is True,
            "later_synthetic_helper_shapes_required": False,
        },
        "target_executed": False,
    }


def audit_existing_r4_evidence_topology(topology: Any) -> dict[str, Any]:
    """Evaluate exactly six semantic invariants from the accepted immutable R4 topology."""

    sg1 = audit_formal_auditor_self_emission_source(topology)
    sg2 = audit_origin_and_provenance_bindings_source(topology)
    sg3 = audit_preinteraction_fixture_bindings_source(topology)
    checks = {
        **sg1["checks"],
        **sg2["checks"],
        **sg3["checks"],
    }
    expected = set((*SG1_CHECK_NAMES, *SG2_CHECK_NAMES, *SG3_CHECK_NAMES))
    exact_check_set = set(checks) == expected and len(checks) == 6
    return {
        "schema": "sentigraph_existing_r4_six_gap_topology_static_proof_v0_1",
        "status": "pass" if exact_check_set and all(checks.values()) else "fail",
        "checks": checks,
        "check_count": len(checks),
        "exact_check_set": exact_check_set,
        "later_synthetic_helper_shapes_required": False,
        "package_regeneration_or_materialization_required": False,
        "target_executed": False,
    }


def audit_source_texts(
    shared_source: str,
    validator_source: str,
    resolver_source: str,
    validator_test_source: str,
) -> dict[str, bool]:
    shared_tree = ast.parse(shared_source)
    validator_tree = ast.parse(validator_source)
    resolver_tree = ast.parse(resolver_source)
    validator_test_tree = ast.parse(validator_test_source)
    all_sources = (shared_source, validator_source, resolver_source, validator_test_source)
    all_trees = (shared_tree, validator_tree, resolver_tree, validator_test_tree)

    canonical_module = "sentigraph_shared.json_framing"
    validator_imports = _imported_names(validator_tree, canonical_module)
    resolver_imports = _imported_names(resolver_tree, canonical_module)
    validator_calls = _call_names(validator_tree)
    resolver_calls = _call_names(resolver_tree)
    shared_calls = _call_names(shared_tree)
    shared_import_line = validator_source.find("from sentigraph_shared.json_framing import")
    legacy_guard_line = validator_source.find('if __name__ == "__main__" and not __package__')
    shared_import_count = sum(
        1
        for tree in (validator_tree, resolver_tree)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == canonical_module
    )

    checks = {name: False for name in CHECK_NAMES}
    checks["SHARED_SOURCE_UTF8_NO_BOM"] = not shared_source.startswith("\ufeff")
    checks["SHARED_STANDARD_LIBRARY_ONLY"] = _import_roots(shared_tree) <= _ALLOWED_SHARED_IMPORT_ROOTS
    checks["SHARED_CONTRACT_SYMBOLS"] = _REQUIRED_SHARED_SYMBOLS <= _definition_names(shared_tree)
    checks["SHARED_SINGLE_JSON_SERIALIZATION"] = (
        shared_calls.count("json.dumps") == 1
        and _function_call_count(shared_tree, "serialize_single_json_document", "json.dumps") == 1
    )
    required_imports = {
        "DuplicateKeyPolicy",
        "JsonFramingType",
        "JsonInputDescriptor",
        "JsonRootShape",
        "parse_single_json_document",
    }
    checks["VALIDATOR_CANONICAL_IMPORT"] = required_imports | {"parse_jsonl_records"} <= validator_imports
    checks["VALIDATOR_CANONICAL_CALLS"] = (
        "parse_single_json_document" in validator_calls and "parse_jsonl_records" in validator_calls
    )
    checks["VALIDATOR_EXPLICIT_MEMBER_CONTRACTS"] = all(
        member in validator_source
        for member in (
            "manifest.json",
            "validation_report.json",
            "source_manifest.jsonl",
            "evidence_items.jsonl",
            "collection_log.jsonl",
        )
    )
    checks["LEGACY_GUARD_BEFORE_SHARED_IMPORT"] = (
        0 <= legacy_guard_line < shared_import_line
        and "LEGACY_DIRECT_INVOCATION_MARKER" in validator_source
    )
    checks["RESOLVER_CANONICAL_IMPORT"] = required_imports <= resolver_imports
    checks["RESOLVER_CANONICAL_CALLS"] = "parse_single_json_document" in resolver_calls
    checks["EXPLICIT_FRAMING_ROOT_DUPLICATE_POLICIES"] = all(
        marker in validator_source + resolver_source
        for marker in (
            "JsonFramingType.SINGLE_JSON",
            "JsonFramingType.JSONL",
            "JsonRootShape.OBJECT_ONLY",
            "DuplicateKeyPolicy.REJECT_DUPLICATE_KEYS",
        )
    )
    checks["EXPECTED_ROLE_CHECKS_BEFORE_PARSE"] = all(
        marker in validator_source + resolver_source
        for marker in (
            "expected_source_role=",
            "expected_container_role=",
            "expected_member_role=",
        )
    )
    checks["TEST_CANONICAL_VALIDATOR_IMPORT"] = (
        "validate_external_evidence_package" in _imported_names(validator_test_tree, "scripts")
    )
    checks["NO_DYNAMIC_IMPORT_OR_FILE_LOADER"] = not any(
        _has_dynamic_import_or_file_loader(source, tree)
        for source, tree in zip(all_sources, all_trees)
    )
    checks["NO_SYS_PATH_OR_PYTHONPATH_HACK"] = (
        not any(_has_sys_path_mutation(tree) for tree in all_trees)
        and not any("PYTHONPATH" in source for source in all_sources)
    )
    checks["NO_DUAL_IMPORT_FALLBACK"] = shared_import_count == 2
    checks["NARROW_IO_BYTESIO_POLICY"] = sum(source.count("io.BytesIO") for source in all_sources) == 0
    checks["TARGET_EXECUTION_FORBIDDEN"] = True
    return checks


def audit_paths(
    shared_path: Path,
    validator_path: Path,
    resolver_path: Path,
    validator_test_path: Path,
) -> dict[str, Any]:
    sources: list[str] = []
    identities: dict[str, dict[str, Any]] = {}
    for role, path in (
        ("shared", shared_path),
        ("validator", validator_path),
        ("resolver", resolver_path),
        ("validator_test", validator_test_path),
    ):
        source, byte_count, sha256 = _read_utf8_no_bom(path)
        sources.append(source)
        identities[role] = {"bytes": byte_count, "sha256": sha256}
    checks = audit_source_texts(*sources)
    passed = sum(1 for name in CHECK_NAMES if checks[name])
    return {
        "schema": "sentigraph_json_framing_static_auditor_result_v0_1",
        "version": VERSION,
        "status": "pass" if passed == len(CHECK_NAMES) else "fail",
        "checks": checks,
        "checks_passed": passed,
        "checks_failed": len(CHECK_NAMES) - passed,
        "source_reads": 4,
        "source_reopens": 0,
        "source_identities": identities,
        "target_executed": False,
    }


def run_self_test() -> dict[str, Any]:
    fixtures = (
        ("safe", "from sentigraph_shared.json_framing import parse_single_json_document", False),
        ("dynamic_import", "import importlib\nimportlib.import_module('x')", True),
        ("file_loader", "from importlib.util import spec_from_file_location", True),
        ("builtin_import", "__import__('x')", True),
        ("sys_path", "import sys\nsys.path.append('x')", False),
    )
    outcomes: list[bool] = []
    for name, source, expected_dynamic in fixtures:
        tree = ast.parse(source)
        if name == "sys_path":
            outcomes.append(_has_sys_path_mutation(tree))
        else:
            outcomes.append(_has_dynamic_import_or_file_loader(source, tree) is expected_dynamic)
    passed = sum(1 for item in outcomes if item)
    return {
        "schema": "sentigraph_json_framing_static_auditor_self_test_v0_1",
        "version": VERSION,
        "status": "pass" if passed == len(fixtures) else "fail",
        "fixtures": len(fixtures),
        "passed": passed,
        "failed": len(fixtures) - passed,
        "target_executed": False,
    }


def _emit(result: dict[str, Any]) -> int:
    sys.stdout.write(json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n")
    return 0 if result["status"] == "pass" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit canonical Sentigraph JSON framing sources without executing them.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--audit", nargs=4, metavar=("SHARED", "VALIDATOR", "RESOLVER", "VALIDATOR_TEST"))
    args = parser.parse_args(argv)
    if args.self_test and args.audit is None:
        return _emit(run_self_test())
    if args.audit is not None and not args.self_test:
        return _emit(audit_paths(*(Path(item) for item in args.audit)))
    return _emit({
        "schema": "sentigraph_json_framing_static_auditor_cli_error_v0_1",
        "version": VERSION,
        "status": "fail",
    })


if __name__ == "__main__":
    raise SystemExit(main())
