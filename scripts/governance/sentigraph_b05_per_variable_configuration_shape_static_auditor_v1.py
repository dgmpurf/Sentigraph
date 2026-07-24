from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path


AUDIT_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_static_audit_rc1_result_v0_2"
MATRIX_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_static_matrix_rc1_v0_2"
QUALIFICATION_SCHEMA = (
    "sentigraph_b05_per_variable_configuration_shape_static_qualification_rc1_v0_2"
)
VERSION = "0.2"
EXPECTED_RUNNER_BASENAME = (
    ".sentigraph_b05_per_variable_configuration_shape_diagnostic_v1.py"
)
EXPECTED_RUNNER_BYTES = 3266
EXPECTED_RUNNER_SHA256 = (
    "5aad7384df83e8f5aa3a3ef952dff0fcfd7e8ea05946a6a4595c1c090fb07250"
)

CHECK_NAMES = (
    "STRICT_UTF8_NO_BOM",
    "AST_PARSE",
    "IMPORT_ALLOWLIST",
    "TOP_LEVEL_SURFACE_EXACT",
    "BOUND_CONSTANTS",
    "VARIABLE_NAMES_EXACT",
    "SHAPE_LABELS_EXACT",
    "FUNCTION_SET_EXACT",
    "FUNCTION_SIGNATURES_EXACT",
    "ENVIRONMENT_GETS_EXACT",
    "OS_USAGE_ALLOWLIST_EXACT",
    "CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT",
    "PATH_PUBLIC_BOUND_EXACT",
    "ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT",
    "CLASSIFIED_RESULT_CONTRACT_EXACT",
    "INTEGRITY_RESULT_CONTRACT_EXACT",
    "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    "ONE_COMPACT_JSON_PRINT",
    "NO_VALUE_LENGTH_PATH_SECRET_OR_EXCEPTION_DISCLOSURE",
    "NO_FILE_NETWORK_SUBPROCESS_DATABASE_DYNAMIC_ACTIONS",
    "MAIN_GUARD_EXACTLY_ONCE",
)

VARIABLE_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)

SHAPE_LABELS = (
    "shape_valid",
    "missing",
    "empty",
    "leading_or_trailing_whitespace",
    "nonprintable_or_nul",
    "over_public_bound",
    "adapter_format_invalid",
    "diagnostic_integrity_block",
)

RESULT_FIELDS = (
    "schema",
    "version",
    "status",
    "variable_names",
    "shape_labels",
    "privacy_issue_stop",
    "warnings",
    "blockers",
)

FIXTURE_SPECS = (
    ("import_added", "IMPORT_ALLOWLIST"),
    ("top_level_assignment_added", "TOP_LEVEL_SURFACE_EXACT"),
    ("runner_schema_changed", "BOUND_CONSTANTS"),
    ("variable_order_swapped", "VARIABLE_NAMES_EXACT"),
    ("shape_label_added", "SHAPE_LABELS_EXACT"),
    ("helper_function_added", "FUNCTION_SET_EXACT"),
    ("function_signature_changed", "FUNCTION_SIGNATURES_EXACT"),
    ("fourth_environment_get", "ENVIRONMENT_GETS_EXACT"),
    ("environment_get_order_swapped", "ENVIRONMENT_GETS_EXACT"),
    ("os_getenv_added", "OS_USAGE_ALLOWLIST_EXACT"),
    ("os_putenv_added", "OS_USAGE_ALLOWLIST_EXACT"),
    ("os_remove_added", "OS_USAGE_ALLOWLIST_EXACT"),
    ("os_execv_added", "OS_USAGE_ALLOWLIST_EXACT"),
    (
        "path_condition_return_pair_swapped",
        "CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT",
    ),
    (
        "adapter_condition_return_pair_swapped",
        "CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT",
    ),
    ("path_bound_changed", "PATH_PUBLIC_BOUND_EXACT"),
    ("adapter_regex_broadened", "ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT"),
    ("classified_result_field_order_swapped", "CLASSIFIED_RESULT_CONTRACT_EXACT"),
    ("classified_result_status_changed", "CLASSIFIED_RESULT_CONTRACT_EXACT"),
    ("integrity_blocker_removed", "INTEGRITY_RESULT_CONTRACT_EXACT"),
    ("integrity_labels_changed", "INTEGRITY_RESULT_CONTRACT_EXACT"),
    (
        "read_environment_called_twice",
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    ),
    (
        "post_result_environment_value_append",
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    ),
    (
        "post_result_shape_labels_replaced",
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    ),
    (
        "post_result_dictionary_item_assignment",
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    ),
    (
        "result_alias_mutation",
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT",
    ),
    ("second_print_added", "ONE_COMPACT_JSON_PRINT"),
    (
        "absolute_path_literal_added",
        "NO_VALUE_LENGTH_PATH_SECRET_OR_EXCEPTION_DISCLOSURE",
    ),
    ("file_open_added", "NO_FILE_NETWORK_SUBPROCESS_DATABASE_DYNAMIC_ACTIONS"),
    ("main_guard_removed", "MAIN_GUARD_EXACTLY_ONCE"),
    ("extra_top_level_main_call", "TOP_LEVEL_SURFACE_EXACT"),
)

VALID_PUBLIC_RUNNER = r'''from __future__ import annotations

import json
import os
import re


RUNNER_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_diagnostic_v0_1"
RESULT_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_diagnostic_result_v0_1"
VERSION = "0.1"

VARIABLE_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)

SHAPE_LABELS = (
    "shape_valid",
    "missing",
    "empty",
    "leading_or_trailing_whitespace",
    "nonprintable_or_nul",
    "over_public_bound",
    "adapter_format_invalid",
    "diagnostic_integrity_block",
)

ADAPTER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"


def _read_environment():
    return (
        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"),
        os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"),
        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
    )


def _classify_path_value(value):
    if value is None:
        return "missing"
    if not isinstance(value, str):
        return "diagnostic_integrity_block"
    if value == "":
        return "empty"
    if "\x00" in value or not value.isprintable():
        return "nonprintable_or_nul"
    if value != value.strip():
        return "leading_or_trailing_whitespace"
    if len(value) > 2048:
        return "over_public_bound"
    return "shape_valid"


def _classify_adapter_value(value):
    if value is None:
        return "missing"
    if not isinstance(value, str):
        return "diagnostic_integrity_block"
    if value == "":
        return "empty"
    if "\x00" in value or not value.isprintable():
        return "nonprintable_or_nul"
    if value != value.strip():
        return "leading_or_trailing_whitespace"
    if len(value) > 128:
        return "over_public_bound"
    if re.fullmatch(ADAPTER_PATTERN, value) is None:
        return "adapter_format_invalid"
    return "shape_valid"


def _classified_result(values):
    shape_labels = (
        _classify_path_value(values[0]),
        _classify_path_value(values[1]),
        _classify_adapter_value(values[2]),
    )
    return {
        "schema": RESULT_SCHEMA,
        "version": VERSION,
        "status": "classified",
        "variable_names": list(VARIABLE_NAMES),
        "shape_labels": list(shape_labels),
        "privacy_issue_stop": False,
        "warnings": [],
        "blockers": [],
    }


def _integrity_result():
    return {
        "schema": RESULT_SCHEMA,
        "version": VERSION,
        "status": "blocked_diagnostic_integrity",
        "variable_names": list(VARIABLE_NAMES),
        "shape_labels": [
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
        ],
        "privacy_issue_stop": False,
        "warnings": [],
        "blockers": ["diagnostic_integrity_block"],
    }


def main():
    try:
        values = _read_environment()
        result = _classified_result(values)
    except Exception:
        result = _integrity_result()
    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )


if __name__ == "__main__":
    main()
'''


def _expression_dump(source):
    return ast.dump(ast.parse(source, mode="eval").body, include_attributes=False)


def _node_matches_expression(node, source):
    return ast.dump(node, include_attributes=False) == _expression_dump(source)


def _literal(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        return None


def _global_assignments(tree):
    assignments = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            assignments[node.targets[0].id] = _literal(node.value)
    return assignments


def _function_map(tree):
    return {
        node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)
    }


def _import_signature(tree):
    signature = []
    nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    nodes.sort(key=lambda node: (node.lineno, node.col_offset))
    for node in nodes:
        if isinstance(node, ast.ImportFrom):
            signature.append(
                (
                    "from",
                    node.module,
                    tuple((alias.name, alias.asname) for alias in node.names),
                    node.level,
                )
            )
        else:
            signature.append(
                (
                    "import",
                    tuple((alias.name, alias.asname) for alias in node.names),
                )
            )
    return signature


def _is_os_environ(node):
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "environ"
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
    )


def _is_os_environ_attribute(node, attribute):
    return (
        isinstance(node, ast.Attribute)
        and node.attr == attribute
        and _is_os_environ(node.value)
    )


def _environment_get_calls(tree):
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _is_os_environ_attribute(node.func, "get")
    ]
    calls.sort(key=lambda node: (node.lineno, node.col_offset))
    return calls


def _environment_gets_exact(tree, functions):
    calls = _environment_get_calls(tree)
    reader = functions.get("_read_environment")
    if reader is None or len(calls) != 3:
        return False
    if not all(reader.lineno <= call.lineno <= reader.end_lineno for call in calls):
        return False
    names = []
    for call in calls:
        if len(call.args) != 1 or call.keywords:
            return False
        if not isinstance(call.args[0], ast.Constant) or not isinstance(
            call.args[0].value, str
        ):
            return False
        names.append(call.args[0].value)
    return tuple(names) == VARIABLE_NAMES


def _no_environment_enumeration(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr == "getenv"
            ):
                return False
            if (
                isinstance(node.func, ast.Attribute)
                and _is_os_environ(node.func.value)
                and node.func.attr != "get"
            ):
                return False
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in {"dict", "list", "tuple", "set", "iter"}
                and any(_is_os_environ(argument) for argument in node.args)
            ):
                return False
        if (
            isinstance(node, ast.Subscript)
            and _is_os_environ(node.value)
            and isinstance(node.ctx, ast.Load)
        ):
            return False
        if isinstance(node, (ast.For, ast.comprehension)) and _is_os_environ(
            node.iter
        ):
            return False
    return True


def _target_contains_os_environ(node):
    if _is_os_environ(node):
        return True
    if isinstance(node, ast.Subscript) and _is_os_environ(node.value):
        return True
    if isinstance(node, (ast.Tuple, ast.List)):
        return any(_target_contains_os_environ(item) for item in node.elts)
    return False


def _no_environment_mutation(tree):
    mutating_methods = {
        "clear",
        "pop",
        "popitem",
        "setdefault",
        "update",
        "__setitem__",
        "__delitem__",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            _target_contains_os_environ(target) for target in node.targets
        ):
            return False
        if isinstance(node, (ast.AnnAssign, ast.AugAssign)) and (
            _target_contains_os_environ(node.target)
        ):
            return False
        if isinstance(node, ast.Delete) and any(
            _target_contains_os_environ(target) for target in node.targets
        ):
            return False
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and _is_os_environ(node.func.value)
            and node.func.attr in mutating_methods
        ):
            return False
    return True


def _classifier_functions_exact(tree, functions):
    expected = (
        ("_read_environment", 0),
        ("_classify_path_value", 1),
        ("_classify_adapter_value", 1),
        ("_classified_result", 1),
        ("_integrity_result", 0),
        ("main", 0),
    )
    if tuple(functions) != tuple(name for name, _ in expected):
        return False
    for name, argument_count in expected:
        function = functions[name]
        arguments = function.args
        if (
            len(arguments.posonlyargs) != 0
            or len(arguments.args) != argument_count
            or arguments.vararg is not None
            or len(arguments.kwonlyargs) != 0
            or arguments.kwarg is not None
            or function.decorator_list
        ):
            return False
    return not any(isinstance(node, (ast.AsyncFunctionDef, ast.Lambda)) for node in ast.walk(tree))


def _length_bound_test(node):
    return (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.Gt)
        and len(node.comparators) == 1
        and isinstance(node.comparators[0], ast.Constant)
        and isinstance(node.comparators[0].value, int)
        and isinstance(node.left, ast.Call)
        and isinstance(node.left.func, ast.Name)
        and node.left.func.id == "len"
        and len(node.left.args) == 1
        and isinstance(node.left.args[0], ast.Name)
        and node.left.args[0].id == "value"
    )


def _condition_tag(node):
    if _node_matches_expression(node, "value is None"):
        return "missing"
    if _node_matches_expression(node, "not isinstance(value, str)"):
        return "not_string"
    if _node_matches_expression(node, 'value == ""'):
        return "empty"
    if _node_matches_expression(
        node, r'"\x00" in value or not value.isprintable()'
    ):
        return "nonprintable_or_nul"
    if _node_matches_expression(node, "value != value.strip()"):
        return "whitespace"
    if _length_bound_test(node):
        return "length_bound"
    if _node_matches_expression(
        node, "re.fullmatch(ADAPTER_PATTERN, value) is None"
    ):
        return "adapter_format"
    return "unknown"


def _classification_precedence_exact(functions):
    path_function = functions.get("_classify_path_value")
    adapter_function = functions.get("_classify_adapter_value")
    if path_function is None or adapter_function is None:
        return False
    path_tags = tuple(
        _condition_tag(node.test)
        for node in path_function.body
        if isinstance(node, ast.If)
    )
    adapter_tags = tuple(
        _condition_tag(node.test)
        for node in adapter_function.body
        if isinstance(node, ast.If)
    )
    return path_tags == (
        "missing",
        "not_string",
        "empty",
        "nonprintable_or_nul",
        "whitespace",
        "length_bound",
    ) and adapter_tags == (
        "missing",
        "not_string",
        "empty",
        "nonprintable_or_nul",
        "whitespace",
        "length_bound",
        "adapter_format",
    )


def _direct_return_labels(function):
    labels = []
    if function is None:
        return labels
    for node in function.body:
        if isinstance(node, ast.If):
            if (
                len(node.body) != 1
                or not isinstance(node.body[0], ast.Return)
                or not isinstance(node.body[0].value, ast.Constant)
                or not isinstance(node.body[0].value.value, str)
            ):
                return []
            labels.append(node.body[0].value.value)
        elif isinstance(node, ast.Return):
            if not isinstance(node.value, ast.Constant) or not isinstance(
                node.value.value, str
            ):
                return []
            labels.append(node.value.value)
    return labels


def _classifier_return_labels_exact(functions):
    path_labels = _direct_return_labels(functions.get("_classify_path_value"))
    adapter_labels = _direct_return_labels(
        functions.get("_classify_adapter_value")
    )
    expected_path = [
        "missing",
        "diagnostic_integrity_block",
        "empty",
        "nonprintable_or_nul",
        "leading_or_trailing_whitespace",
        "over_public_bound",
        "shape_valid",
    ]
    expected_adapter = expected_path[:-1] + [
        "adapter_format_invalid",
        "shape_valid",
    ]
    return sorted(path_labels) == sorted(expected_path) and sorted(
        adapter_labels
    ) == sorted(expected_adapter)


def _length_bounds(function):
    if function is None:
        return []
    return [
        node.test.comparators[0].value
        for node in function.body
        if isinstance(node, ast.If) and _length_bound_test(node.test)
    ]


def _path_public_bound_exact(functions):
    return _length_bounds(functions.get("_classify_path_value")) == [2048]


def _adapter_public_bound_and_regex_exact(assignments, functions):
    function = functions.get("_classify_adapter_value")
    if function is None:
        return False
    regex_conditions = [
        node.test
        for node in function.body
        if isinstance(node, ast.If)
        and _node_matches_expression(
            node.test, "re.fullmatch(ADAPTER_PATTERN, value) is None"
        )
    ]
    return (
        assignments.get("ADAPTER_PATTERN")
        == r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"
        and _length_bounds(function) == [128]
        and len(regex_conditions) == 1
    )


def _direct_return_dict(function):
    if function is None:
        return None
    for node in function.body:
        if isinstance(node, ast.Return) and isinstance(node.value, ast.Dict):
            return node.value
    return None


def _dict_entries(dictionary):
    if not isinstance(dictionary, ast.Dict):
        return None, None
    keys = []
    values = {}
    for key, value in zip(dictionary.keys, dictionary.values):
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            return None, None
        keys.append(key.value)
        values[key.value] = value
    return tuple(keys), values


def _result_fields_exact(functions):
    normal_keys, _ = _dict_entries(
        _direct_return_dict(functions.get("_classified_result"))
    )
    integrity_keys, _ = _dict_entries(
        _direct_return_dict(functions.get("_integrity_result"))
    )
    return normal_keys == RESULT_FIELDS and integrity_keys == RESULT_FIELDS


def _assignment_value(function, name):
    if function is None:
        return None
    for node in function.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            return node.value
    return None


def _result_label_cardinality_and_order(functions):
    function = functions.get("_classified_result")
    shape_assignment = _assignment_value(function, "shape_labels")
    if not isinstance(shape_assignment, ast.Tuple) or len(shape_assignment.elts) != 3:
        return False
    expected_expressions = (
        "_classify_path_value(values[0])",
        "_classify_path_value(values[1])",
        "_classify_adapter_value(values[2])",
    )
    if not all(
        _node_matches_expression(actual, expected)
        for actual, expected in zip(shape_assignment.elts, expected_expressions)
    ):
        return False
    _, entries = _dict_entries(_direct_return_dict(function))
    if entries is None:
        return False
    return _node_matches_expression(
        entries["variable_names"], "list(VARIABLE_NAMES)"
    ) and _node_matches_expression(entries["shape_labels"], "list(shape_labels)")


def _integrity_result_fixed(functions):
    _, entries = _dict_entries(
        _direct_return_dict(functions.get("_integrity_result"))
    )
    if entries is None:
        return False
    return (
        _node_matches_expression(entries["schema"], "RESULT_SCHEMA")
        and _node_matches_expression(entries["version"], "VERSION")
        and _literal(entries["status"]) == "blocked_diagnostic_integrity"
        and _node_matches_expression(
            entries["variable_names"], "list(VARIABLE_NAMES)"
        )
        and _literal(entries["shape_labels"])
        == [
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
        ]
        and _literal(entries["privacy_issue_stop"]) is False
        and _literal(entries["warnings"]) == []
        and _literal(entries["blockers"]) == ["diagnostic_integrity_block"]
    )


def _one_compact_json_print(tree):
    print_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "print"
    ]
    dumps_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "dumps"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "json"
    ]
    if len(print_calls) != 1 or len(dumps_calls) != 1:
        return False
    print_call = print_calls[0]
    dumps_call = dumps_calls[0]
    if (
        len(print_call.args) != 1
        or print_call.keywords
        or ast.dump(print_call.args[0], include_attributes=False)
        != ast.dump(dumps_call, include_attributes=False)
        or len(dumps_call.args) != 1
        or not isinstance(dumps_call.args[0], ast.Name)
        or dumps_call.args[0].id != "result"
    ):
        return False
    keywords = tuple(keyword.arg for keyword in dumps_call.keywords)
    values = {keyword.arg: _literal(keyword.value) for keyword in dumps_call.keywords}
    return keywords == ("ensure_ascii", "separators", "sort_keys") and values == {
        "ensure_ascii": True,
        "separators": (",", ":"),
        "sort_keys": False,
    }


def _no_value_or_length_disclosure(tree, functions):
    normal_dictionary = _direct_return_dict(functions.get("_classified_result"))
    _, entries = _dict_entries(normal_dictionary)
    if entries is None:
        return False
    if (
        _literal(entries["privacy_issue_stop"]) is not False
        or _literal(entries["warnings"]) != []
        or _literal(entries["blockers"]) != []
    ):
        return False
    for node in ast.walk(normal_dictionary):
        if isinstance(node, ast.Name) and node.id in {"value", "values"}:
            return False
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"len", "repr", "str"}
        ):
            return False
        if isinstance(node, ast.JoinedStr):
            return False
    return not any(
        isinstance(node, ast.JoinedStr)
        or (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"repr", "str"}
        )
        for node in ast.walk(tree)
    )


def _looks_absolute_path(value):
    if not isinstance(value, str):
        return False
    if len(value) >= 3 and value[0].isalpha() and value[1] == ":" and value[2] in {
        "\\",
        "/",
    }:
        return True
    return value.startswith(("/", "\\\\"))


def _no_path_secret_or_exception_disclosure(tree):
    forbidden_identifiers = (
        "receipt",
        "salt_hex",
        "combined_binding",
        "provider_result",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            lowered = node.value.lower()
            if _looks_absolute_path(node.value) or any(
                identifier in lowered for identifier in forbidden_identifiers
            ):
                return False
        if isinstance(node, ast.ExceptHandler) and node.name is not None:
            return False
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"format_exc", "format_exception", "print_exc"}
        ):
            return False
    return True


def _no_file_io(tree):
    forbidden_names = {"open"}
    forbidden_attributes = {
        "open",
        "read",
        "read_bytes",
        "read_text",
        "write",
        "write_bytes",
        "write_text",
        "unlink",
        "rename",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "Path":
            return False
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in forbidden_names:
                return False
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in forbidden_attributes
            ):
                return False
    return True


def _no_network_subprocess_database(tree):
    forbidden_modules = {
        "asyncio",
        "httpx",
        "pymongo",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] in forbidden_modules for alias in node.names
        ):
            return False
        if (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.split(".")[0] in forbidden_modules
        ):
            return False
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "os"
            and node.func.attr in {"system", "popen", "spawnl", "spawnv"}
        ):
            return False
    return True


def _no_dynamic_execution_or_reflection(tree):
    forbidden_names = {
        "__import__",
        "compile",
        "delattr",
        "eval",
        "exec",
        "getattr",
        "globals",
        "locals",
        "setattr",
        "vars",
    }
    forbidden_attributes = {"__class__", "__dict__", "__globals__", "__subclasses__"}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in forbidden_names
        ):
            return False
        if isinstance(node, ast.Attribute) and node.attr in forbidden_attributes:
            return False
    return True


def _main_guard_exactly_once(tree):
    guards = [
        node
        for node in tree.body
        if isinstance(node, ast.If)
        and _node_matches_expression(node.test, '__name__ == "__main__"')
    ]
    if len(guards) != 1:
        return False
    guard = guards[0]
    return (
        len(guard.body) == 1
        and not guard.orelse
        and isinstance(guard.body[0], ast.Expr)
        and isinstance(guard.body[0].value, ast.Call)
        and isinstance(guard.body[0].value.func, ast.Name)
        and guard.body[0].value.func.id == "main"
        and not guard.body[0].value.args
        and not guard.body[0].value.keywords
    )


def _top_level_surface_exact(tree):
    expected_assignments = (
        "RUNNER_SCHEMA",
        "RESULT_SCHEMA",
        "VERSION",
        "VARIABLE_NAMES",
        "SHAPE_LABELS",
        "ADAPTER_PATTERN",
    )
    nodes = tree.body
    index = 0

    while index < len(nodes) and isinstance(nodes[index], (ast.Import, ast.ImportFrom)):
        index += 1

    assignment_names = []
    while index < len(nodes) and isinstance(nodes[index], ast.Assign):
        node = nodes[index]
        if (
            len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            assignment_names.append(node.targets[0].id)
        else:
            return False
        index += 1

    if tuple(assignment_names) != expected_assignments:
        return False

    while index < len(nodes) and isinstance(nodes[index], ast.FunctionDef):
        index += 1

    if index == len(nodes):
        return True

    guard = nodes[index]
    return (
        index == len(nodes) - 1
        and isinstance(guard, ast.If)
        and _node_matches_expression(guard.test, '__name__ == "__main__"')
    )


def _function_set_exact(tree, functions):
    expected_names = (
        "_read_environment",
        "_classify_path_value",
        "_classify_adapter_value",
        "_classified_result",
        "_integrity_result",
        "main",
    )
    all_functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    return (
        tuple(functions) == expected_names
        and len(all_functions) == len(expected_names)
        and not any(
            isinstance(node, (ast.AsyncFunctionDef, ast.Lambda))
            for node in ast.walk(tree)
        )
    )


def _function_signatures_exact(functions):
    expected = (
        ("_read_environment", 0),
        ("_classify_path_value", 1),
        ("_classify_adapter_value", 1),
        ("_classified_result", 1),
        ("_integrity_result", 0),
        ("main", 0),
    )
    for name, argument_count in expected:
        function = functions.get(name)
        if function is None:
            return False
        arguments = function.args
        if (
            len(arguments.posonlyargs) != 0
            or len(arguments.args) != argument_count
            or any(argument.annotation is not None for argument in arguments.args)
            or arguments.vararg is not None
            or len(arguments.kwonlyargs) != 0
            or arguments.kwarg is not None
            or function.decorator_list
            or function.returns is not None
        ):
            return False
        if any(default is not None for default in arguments.defaults):
            return False
    return True


def _exact_approved_environment_call(node):
    return (
        isinstance(node, ast.Call)
        and _is_os_environ_attribute(node.func, "get")
        and len(node.args) == 1
        and not node.keywords
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        and node.args[0].value in VARIABLE_NAMES
    )


def _environment_reader_exact(tree, functions):
    function = functions.get("_read_environment")
    if function is None or len(function.body) != 1:
        return False
    statement = function.body[0]
    if not isinstance(statement, ast.Return) or not isinstance(
        statement.value, ast.Tuple
    ):
        return False
    calls = statement.value.elts
    if len(calls) != 3 or not all(
        _exact_approved_environment_call(call) for call in calls
    ):
        return False
    if tuple(call.args[0].value for call in calls) != VARIABLE_NAMES:
        return False
    all_get_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _is_os_environ_attribute(node.func, "get")
    ]
    return len(all_get_calls) == 3


def _os_usage_allowlist_exact(tree):
    approved_calls = [
        node
        for node in ast.walk(tree)
        if _exact_approved_environment_call(node)
    ]
    approved_os_nodes = {
        id(call.func.value.value)
        for call in approved_calls
        if isinstance(call.func.value.value, ast.Name)
        and call.func.value.value.id == "os"
    }
    all_os_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "os"
    ]
    return len(approved_os_nodes) == len(approved_calls) and all(
        id(node) in approved_os_nodes for node in all_os_nodes
    )


def _classifier_pairs(function):
    if function is None or not function.body:
        return None
    pairs = []
    for statement in function.body[:-1]:
        if (
            not isinstance(statement, ast.If)
            or statement.orelse
            or len(statement.body) != 1
            or not isinstance(statement.body[0], ast.Return)
            or not isinstance(statement.body[0].value, ast.Constant)
            or not isinstance(statement.body[0].value.value, str)
        ):
            return None
        pairs.append((_condition_tag(statement.test), statement.body[0].value.value))
    final_statement = function.body[-1]
    if (
        not isinstance(final_statement, ast.Return)
        or not isinstance(final_statement.value, ast.Constant)
        or not isinstance(final_statement.value.value, str)
    ):
        return None
    return tuple(pairs), final_statement.value.value


def _classification_branch_return_binding_exact(functions):
    path_pairs = _classifier_pairs(functions.get("_classify_path_value"))
    adapter_pairs = _classifier_pairs(functions.get("_classify_adapter_value"))
    return path_pairs == (
        (
            ("missing", "missing"),
            ("not_string", "diagnostic_integrity_block"),
            ("empty", "empty"),
            ("nonprintable_or_nul", "nonprintable_or_nul"),
            ("whitespace", "leading_or_trailing_whitespace"),
            ("length_bound", "over_public_bound"),
        ),
        "shape_valid",
    ) and adapter_pairs == (
        (
            ("missing", "missing"),
            ("not_string", "diagnostic_integrity_block"),
            ("empty", "empty"),
            ("nonprintable_or_nul", "nonprintable_or_nul"),
            ("whitespace", "leading_or_trailing_whitespace"),
            ("length_bound", "over_public_bound"),
            ("adapter_format", "adapter_format_invalid"),
        ),
        "shape_valid",
    )


def _classified_result_contract_exact(functions):
    function = functions.get("_classified_result")
    if function is None or len(function.body) != 2:
        return False
    assignment, return_statement = function.body
    if (
        not isinstance(assignment, ast.Assign)
        or len(assignment.targets) != 1
        or not isinstance(assignment.targets[0], ast.Name)
        or assignment.targets[0].id != "shape_labels"
        or not isinstance(assignment.value, ast.Tuple)
        or len(assignment.value.elts) != 3
        or not isinstance(return_statement, ast.Return)
        or not isinstance(return_statement.value, ast.Dict)
    ):
        return False
    expected_calls = (
        "_classify_path_value(values[0])",
        "_classify_path_value(values[1])",
        "_classify_adapter_value(values[2])",
    )
    if not all(
        _node_matches_expression(actual, expected)
        for actual, expected in zip(assignment.value.elts, expected_calls)
    ):
        return False
    keys, entries = _dict_entries(return_statement.value)
    if keys != RESULT_FIELDS or entries is None:
        return False
    return (
        _node_matches_expression(entries["schema"], "RESULT_SCHEMA")
        and _node_matches_expression(entries["version"], "VERSION")
        and _literal(entries["status"]) == "classified"
        and _node_matches_expression(
            entries["variable_names"], "list(VARIABLE_NAMES)"
        )
        and _node_matches_expression(entries["shape_labels"], "list(shape_labels)")
        and _literal(entries["privacy_issue_stop"]) is False
        and _literal(entries["warnings"]) == []
        and _literal(entries["blockers"]) == []
    )


def _integrity_result_contract_exact(functions):
    function = functions.get("_integrity_result")
    if (
        function is None
        or len(function.body) != 1
        or not isinstance(function.body[0], ast.Return)
        or not isinstance(function.body[0].value, ast.Dict)
    ):
        return False
    keys, entries = _dict_entries(function.body[0].value)
    if keys != RESULT_FIELDS or entries is None:
        return False
    return (
        _node_matches_expression(entries["schema"], "RESULT_SCHEMA")
        and _node_matches_expression(entries["version"], "VERSION")
        and _literal(entries["status"]) == "blocked_diagnostic_integrity"
        and _node_matches_expression(
            entries["variable_names"], "list(VARIABLE_NAMES)"
        )
        and _literal(entries["shape_labels"])
        == [
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
            "diagnostic_integrity_block",
        ]
        and _literal(entries["privacy_issue_stop"]) is False
        and _literal(entries["warnings"]) == []
        and _literal(entries["blockers"]) == ["diagnostic_integrity_block"]
    )


def _call_rooted_at_os(node):
    return any(
        isinstance(child, ast.Name) and child.id == "os" for child in ast.walk(node)
    )


def _is_print_expression(node):
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print"
    )


def _is_dedicated_action_expression(node):
    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        return False
    call = node.value
    if _call_rooted_at_os(call):
        return True
    if isinstance(call.func, ast.Name) and call.func.id in {
        "__import__",
        "compile",
        "eval",
        "exec",
        "open",
    }:
        return True
    return False


def _is_absolute_literal_expression(node):
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
        and _looks_absolute_path(node.value.value)
    )


def _canonical_result_print_calls(tree):
    calls = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
            and len(node.args) == 1
            and not node.keywords
            and isinstance(node.args[0], ast.Call)
        ):
            dumps_call = node.args[0]
            if (
                isinstance(dumps_call.func, ast.Attribute)
                and isinstance(dumps_call.func.value, ast.Name)
                and dumps_call.func.value.id == "json"
                and dumps_call.func.attr == "dumps"
                and len(dumps_call.args) == 1
                and isinstance(dumps_call.args[0], ast.Name)
                and dumps_call.args[0].id == "result"
                and tuple(keyword.arg for keyword in dumps_call.keywords)
                == ("ensure_ascii", "separators", "sort_keys")
                and {
                    keyword.arg: _literal(keyword.value)
                    for keyword in dumps_call.keywords
                }
                == {
                    "ensure_ascii": True,
                    "separators": (",", ":"),
                    "sort_keys": False,
                }
            ):
                calls.append(node)
    return calls


def _final_output_dataflow_exact(tree, functions):
    function = functions.get("main")
    if function is None:
        return False
    core_statements = [
        statement
        for statement in function.body
        if not _is_print_expression(statement)
        and not _is_dedicated_action_expression(statement)
        and not _is_absolute_literal_expression(statement)
    ]
    if len(core_statements) != 1 or not isinstance(core_statements[0], ast.Try):
        return False
    try_statement = core_statements[0]
    if (
        len(try_statement.body) != 2
        or len(try_statement.handlers) != 1
        or try_statement.orelse
        or try_statement.finalbody
    ):
        return False
    values_assignment, normal_result_assignment = try_statement.body
    if (
        not isinstance(values_assignment, ast.Assign)
        or len(values_assignment.targets) != 1
        or not isinstance(values_assignment.targets[0], ast.Name)
        or values_assignment.targets[0].id != "values"
        or not _node_matches_expression(
            values_assignment.value, "_read_environment()"
        )
        or not isinstance(normal_result_assignment, ast.Assign)
        or len(normal_result_assignment.targets) != 1
        or not isinstance(normal_result_assignment.targets[0], ast.Name)
        or normal_result_assignment.targets[0].id != "result"
        or not _node_matches_expression(
            normal_result_assignment.value, "_classified_result(values)"
        )
    ):
        return False
    handler = try_statement.handlers[0]
    if (
        not isinstance(handler.type, ast.Name)
        or handler.type.id != "Exception"
        or handler.name is not None
        or len(handler.body) != 1
        or not isinstance(handler.body[0], ast.Assign)
        or len(handler.body[0].targets) != 1
        or not isinstance(handler.body[0].targets[0], ast.Name)
        or handler.body[0].targets[0].id != "result"
        or not _node_matches_expression(
            handler.body[0].value, "_integrity_result()"
        )
    ):
        return False
    value_loads = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Name)
        and node.id == "values"
        and isinstance(node.ctx, ast.Load)
    ]
    result_loads = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Name)
        and node.id == "result"
        and isinstance(node.ctx, ast.Load)
    ]
    read_calls = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_read_environment"
    ]
    classified_calls = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_classified_result"
    ]
    integrity_calls = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_integrity_result"
    ]
    return (
        len(value_loads) == 1
        and len(result_loads) == 1
        and len(read_calls) == 1
        and len(classified_calls) == 1
        and len(integrity_calls) == 1
        and len(_canonical_result_print_calls(tree)) == 1
    )


def _no_sensitive_disclosure(tree):
    forbidden_identifiers = (
        "receipt",
        "salt_hex",
        "combined_binding",
        "provider_result",
    )
    sensitive_names = {"value", "values", "result"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            lowered = node.value.lower()
            if _looks_absolute_path(node.value) or any(
                identifier in lowered for identifier in forbidden_identifiers
            ):
                return False
        if isinstance(node, ast.JoinedStr):
            return False
        if isinstance(node, ast.ExceptHandler) and node.name is not None:
            return False
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id in {"repr", "str"}
                and any(
                    isinstance(child, ast.Name) and child.id in sensitive_names
                    for child in ast.walk(node)
                )
            ):
                return False
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr
                in {
                    "format",
                    "format_exc",
                    "format_exception",
                    "format_map",
                    "print_exc",
                    "write",
                }
            ):
                return False
    return True


def _no_non_os_actions(tree):
    forbidden_modules = {
        "asyncio",
        "httpx",
        "pathlib",
        "pymongo",
        "requests",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
    }
    forbidden_names = {
        "Path",
        "__import__",
        "compile",
        "eval",
        "exec",
        "getattr",
        "globals",
        "locals",
        "open",
        "setattr",
        "vars",
    }
    forbidden_attributes = {
        "__class__",
        "__dict__",
        "__globals__",
        "__subclasses__",
        "connect",
        "open",
        "read",
        "read_bytes",
        "read_text",
        "rename",
        "request",
        "send",
        "unlink",
        "write",
        "write_bytes",
        "write_text",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(
            alias.name.split(".")[0] in forbidden_modules for alias in node.names
        ):
            return False
        if (
            isinstance(node, ast.ImportFrom)
            and node.module
            and node.module.split(".")[0] in forbidden_modules
        ):
            return False
        if isinstance(node, ast.Call) and _call_rooted_at_os(node):
            continue
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in forbidden_names
        ):
            return False
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in forbidden_attributes
        ):
            return False
        if isinstance(node, ast.Attribute) and node.attr in {
            "__class__",
            "__dict__",
            "__globals__",
            "__subclasses__",
        }:
            return False
    return True


def _audit_source(source_bytes):
    if source_bytes.startswith(b"\xef\xbb\xbf"):
        return {
            "schema": AUDIT_SCHEMA,
            "version": VERSION,
            "status": "fail",
            "checks_passed": 0,
            "checks_total": len(CHECK_NAMES),
            "failed_checks": ["STRICT_UTF8_NO_BOM"],
        }
    try:
        source_text = source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return {
            "schema": AUDIT_SCHEMA,
            "version": VERSION,
            "status": "fail",
            "checks_passed": 0,
            "checks_total": len(CHECK_NAMES),
            "failed_checks": ["STRICT_UTF8_NO_BOM"],
        }
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return {
            "schema": AUDIT_SCHEMA,
            "version": VERSION,
            "status": "fail",
            "checks_passed": 1,
            "checks_total": len(CHECK_NAMES),
            "failed_checks": ["AST_PARSE"],
        }
    assignments = _global_assignments(tree)
    functions = _function_map(tree)
    checks = {
        "STRICT_UTF8_NO_BOM": True,
        "AST_PARSE": True,
        "IMPORT_ALLOWLIST": _import_signature(tree)
        == [
            ("from", "__future__", (("annotations", None),), 0),
            ("import", (("json", None),)),
            ("import", (("os", None),)),
            ("import", (("re", None),)),
        ],
        "TOP_LEVEL_SURFACE_EXACT": _top_level_surface_exact(tree),
        "BOUND_CONSTANTS": (
            assignments.get("RUNNER_SCHEMA")
            == "sentigraph_b05_per_variable_configuration_shape_diagnostic_v0_1"
            and assignments.get("RESULT_SCHEMA")
            == "sentigraph_b05_per_variable_configuration_shape_diagnostic_result_v0_1"
            and assignments.get("VERSION") == "0.1"
        ),
        "VARIABLE_NAMES_EXACT": assignments.get("VARIABLE_NAMES") == VARIABLE_NAMES,
        "SHAPE_LABELS_EXACT": assignments.get("SHAPE_LABELS") == SHAPE_LABELS,
        "FUNCTION_SET_EXACT": _function_set_exact(tree, functions),
        "FUNCTION_SIGNATURES_EXACT": _function_signatures_exact(functions),
        "ENVIRONMENT_GETS_EXACT": _environment_reader_exact(tree, functions),
        "OS_USAGE_ALLOWLIST_EXACT": _os_usage_allowlist_exact(tree),
        "CLASSIFICATION_BRANCH_RETURN_BINDING_EXACT": (
            _classification_branch_return_binding_exact(functions)
        ),
        "PATH_PUBLIC_BOUND_EXACT": _path_public_bound_exact(functions),
        "ADAPTER_PUBLIC_BOUND_AND_REGEX_EXACT": (
            _adapter_public_bound_and_regex_exact(assignments, functions)
        ),
        "CLASSIFIED_RESULT_CONTRACT_EXACT": (
            _classified_result_contract_exact(functions)
        ),
        "INTEGRITY_RESULT_CONTRACT_EXACT": (
            _integrity_result_contract_exact(functions)
        ),
        "FINAL_OUTPUT_DATAFLOW_AND_NO_POST_RESULT_OR_ALIAS_MUTATION_EXACT": (
            _final_output_dataflow_exact(tree, functions)
        ),
        "ONE_COMPACT_JSON_PRINT": _one_compact_json_print(tree),
        "NO_VALUE_LENGTH_PATH_SECRET_OR_EXCEPTION_DISCLOSURE": (
            _no_sensitive_disclosure(tree)
        ),
        "NO_FILE_NETWORK_SUBPROCESS_DATABASE_DYNAMIC_ACTIONS": (
            _no_non_os_actions(tree)
        ),
        "MAIN_GUARD_EXACTLY_ONCE": _main_guard_exactly_once(tree),
    }
    failed_checks = [name for name in CHECK_NAMES if not checks[name]]
    return {
        "schema": AUDIT_SCHEMA,
        "version": VERSION,
        "status": "pass" if not failed_checks else "fail",
        "checks_passed": len(CHECK_NAMES) - len(failed_checks),
        "checks_total": len(CHECK_NAMES),
        "failed_checks": failed_checks,
    }


def _replace_first(source, old, new):
    if old not in source:
        return None
    return source.replace(old, new, 1)


def _negative_source(name):
    source = VALID_PUBLIC_RUNNER
    if name == "import_added":
        return _replace_first(source, "import re\n", "import re\nimport math\n")
    if name == "variable_order_swapped":
        return _replace_first(
            source,
            '''    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",''',
            '''    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",''',
        )
    if name == "shape_label_added":
        return _replace_first(
            source,
            '''    "diagnostic_integrity_block",
)''',
            '''    "diagnostic_integrity_block",
    "unexpected_label",
)''',
        )
    if name == "fourth_environment_get":
        return _replace_first(
            source,
            '''        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
    )''',
            '''        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
        os.environ.get("SENTIGRAPH_UNAPPROVED_FIXTURE_NAME"),
    )''',
        )
    if name == "environment_items_added":
        return _replace_first(
            source,
            '''def _read_environment():
    return (''',
            '''def _read_environment():
    os.environ.items()
    return (''',
        )
    if name == "environment_write_added":
        return _replace_first(
            source,
            '''def _read_environment():
    return (''',
            '''def _read_environment():
    os.environ["SENTIGRAPH_UNAPPROVED_FIXTURE_NAME"] = "fixture"
    return (''',
        )
    if name == "classification_precedence_swapped":
        return _replace_first(
            source,
            r'''    if value == "":
        return "empty"
    if "\x00" in value or not value.isprintable():
        return "nonprintable_or_nul"
''',
            r'''    if "\x00" in value or not value.isprintable():
        return "nonprintable_or_nul"
    if value == "":
        return "empty"
''',
        )
    if name == "unknown_classifier_label":
        return _replace_first(source, '        return "missing"\n', '        return "unknown_label"\n')
    if name == "path_bound_changed":
        return _replace_first(source, "    if len(value) > 2048:\n", "    if len(value) > 2049:\n")
    if name == "adapter_regex_broadened":
        return _replace_first(
            source,
            'ADAPTER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"',
            'ADAPTER_PATTERN = r"[A-Za-z0-9].{0,127}"',
        )
    if name == "result_field_order_swapped":
        return _replace_first(
            source,
            '''        "schema": RESULT_SCHEMA,
        "version": VERSION,''',
            '''        "version": VERSION,
        "schema": RESULT_SCHEMA,''',
        )
    if name == "output_labels_reversed":
        return _replace_first(
            source,
            '''        _classify_path_value(values[0]),
        _classify_path_value(values[1]),''',
            '''        _classify_path_value(values[1]),
        _classify_path_value(values[0]),''',
        )
    if name == "integrity_blocker_removed":
        return _replace_first(
            source,
            '        "blockers": ["diagnostic_integrity_block"],',
            '        "blockers": [],',
        )
    if name == "second_print_added":
        return _replace_first(
            source,
            '''    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )''',
            '''    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )
    print("{}")''',
        )
    if name == "environment_value_output_added":
        return _replace_first(source, '        "warnings": [],', '        "warnings": [values[0]],')
    if name == "absolute_path_literal_added":
        return _replace_first(
            source,
            '''def main():
    try:''',
            '''def main():
    r"C:\\fixture\\absolute"
    try:''',
        )
    if name == "file_open_added":
        return _replace_first(
            source,
            '''def main():
    try:''',
            '''def main():
    open("fixture.txt")
    try:''',
        )
    if name == "os_system_added":
        return _replace_first(
            source,
            '''def main():
    try:''',
            '''def main():
    os.system("true")
    try:''',
        )
    if name == "eval_added":
        return _replace_first(
            source,
            '''def main():
    try:''',
            '''def main():
    eval("1")
    try:''',
        )
    if name == "main_guard_removed":
        return _replace_first(
            source,
            '''if __name__ == "__main__":
    main()
''',
            '''main()
''',
        )
    return None


def _negative_source_rc1(name):
    source = VALID_PUBLIC_RUNNER
    if name == "import_added":
        return _replace_first(source, "import re\n", "import re\nimport math\n")
    if name == "top_level_assignment_added":
        return _replace_first(
            source,
            'ADAPTER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"\n',
            'ADAPTER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"\nEXTRA_SURFACE = 1\n',
        )
    if name == "runner_schema_changed":
        return _replace_first(
            source,
            'RUNNER_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_diagnostic_v0_1"',
            'RUNNER_SCHEMA = "sentigraph_b05_per_variable_configuration_shape_diagnostic_fixture"',
        )
    if name == "variable_order_swapped":
        return _replace_first(
            source,
            '''    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",''',
            '''    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",''',
        )
    if name == "shape_label_added":
        return _replace_first(
            source,
            '''    "diagnostic_integrity_block",
)''',
            '''    "diagnostic_integrity_block",
    "unexpected_label",
)''',
        )
    if name == "helper_function_added":
        return _replace_first(
            source,
            "\ndef _read_environment():\n",
            "\ndef _fixture_helper():\n    return None\n\n\ndef _read_environment():\n",
        )
    if name == "function_signature_changed":
        return _replace_first(
            source,
            "def _classify_path_value(value):",
            "def _classify_path_value(value, extra=None):",
        )
    if name == "fourth_environment_get":
        return _replace_first(
            source,
            '''        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
    )''',
            '''        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID"),
    )''',
        )
    if name == "environment_get_order_swapped":
        return _replace_first(
            source,
            '''        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"),
        os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"),''',
            '''        os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT"),
        os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR"),''',
        )
    if name == "os_getenv_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    os.getenv("SENTIGRAPH_FIXTURE")\n    try:',
        )
    if name == "os_putenv_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    os.putenv("SENTIGRAPH_FIXTURE", "fixture")\n    try:',
        )
    if name == "os_remove_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    os.remove("fixture")\n    try:',
        )
    if name == "os_execv_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    os.execv("fixture", [])\n    try:',
        )
    if name == "path_condition_return_pair_swapped":
        return _replace_first(
            source,
            '''def _classify_path_value(value):
    if value is None:
        return "missing"
    if not isinstance(value, str):
        return "diagnostic_integrity_block"''',
            '''def _classify_path_value(value):
    if value is None:
        return "diagnostic_integrity_block"
    if not isinstance(value, str):
        return "missing"''',
        )
    if name == "adapter_condition_return_pair_swapped":
        return _replace_first(
            source,
            '''def _classify_adapter_value(value):
    if value is None:
        return "missing"
    if not isinstance(value, str):
        return "diagnostic_integrity_block"''',
            '''def _classify_adapter_value(value):
    if value is None:
        return "diagnostic_integrity_block"
    if not isinstance(value, str):
        return "missing"''',
        )
    if name == "path_bound_changed":
        return _replace_first(source, "    if len(value) > 2048:\n", "    if len(value) > 2049:\n")
    if name == "adapter_regex_broadened":
        return _replace_first(
            source,
            'ADAPTER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"',
            'ADAPTER_PATTERN = r"[A-Za-z0-9].{0,127}"',
        )
    if name == "classified_result_field_order_swapped":
        return _replace_first(
            source,
            '''        "schema": RESULT_SCHEMA,
        "version": VERSION,
        "status": "classified",''',
            '''        "version": VERSION,
        "schema": RESULT_SCHEMA,
        "status": "classified",''',
        )
    if name == "classified_result_status_changed":
        return _replace_first(
            source,
            '        "status": "classified",',
            '        "status": "classified_fixture",',
        )
    if name == "integrity_blocker_removed":
        return _replace_first(
            source,
            '        "blockers": ["diagnostic_integrity_block"],',
            '        "blockers": [],',
        )
    if name == "integrity_labels_changed":
        return _replace_first(
            source,
            '''        "shape_labels": [
            "diagnostic_integrity_block",''',
            '''        "shape_labels": [
            "shape_valid",''',
        )
    if name == "read_environment_called_twice":
        return _replace_first(
            source,
            '''        values = _read_environment()
        result = _classified_result(values)''',
            '''        values = _read_environment()
        values = _read_environment()
        result = _classified_result(values)''',
        )
    if name == "post_result_environment_value_append":
        return _replace_first(
            source,
            '''    except Exception:
        result = _integrity_result()
    print(''',
            '''    except Exception:
        result = _integrity_result()
    result["warnings"].append(values[0])
    print(''',
        )
    if name == "post_result_shape_labels_replaced":
        return _replace_first(
            source,
            '''    except Exception:
        result = _integrity_result()
    print(''',
            '''    except Exception:
        result = _integrity_result()
    result["shape_labels"] = ["shape_valid", "shape_valid", "shape_valid"]
    print(''',
        )
    if name == "post_result_dictionary_item_assignment":
        return _replace_first(
            source,
            '''    except Exception:
        result = _integrity_result()
    print(''',
            '''    except Exception:
        result = _integrity_result()
    result["warnings"] = []
    print(''',
        )
    if name == "result_alias_mutation":
        return _replace_first(
            source,
            '''    except Exception:
        result = _integrity_result()
    print(''',
            '''    except Exception:
        result = _integrity_result()
    result_alias = result
    result_alias["warnings"].append("fixture")
    print(''',
        )
    if name == "second_print_added":
        return _replace_first(
            source,
            '''    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )''',
            '''    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )
    print("{}")''',
        )
    if name == "absolute_path_literal_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    r"C:\\\\fixture\\\\absolute"\n    try:',
        )
    if name == "file_open_added":
        return _replace_first(
            source,
            "def main():\n    try:",
            'def main():\n    open("fixture.txt")\n    try:',
        )
    if name == "main_guard_removed":
        return _replace_first(
            source,
            '''if __name__ == "__main__":
    main()
''',
            "",
        )
    if name == "extra_top_level_main_call":
        return _replace_first(
            source,
            '''if __name__ == "__main__":
    main()
''',
            '''main()

if __name__ == "__main__":
    main()
''',
        )
    return None


def _ordered_safe_checks(names):
    return [name for name in CHECK_NAMES if name in set(names)]


def _execute_matrix(external_runner_bytes, qualification):
    valid_bytes = VALID_PUBLIC_RUNNER.encode("utf-8")
    valid_sha256 = hashlib.sha256(valid_bytes).hexdigest()
    external_sha256 = hashlib.sha256(external_runner_bytes).hexdigest()
    embedded_identity_exact = (
        len(valid_bytes) == EXPECTED_RUNNER_BYTES
        and valid_sha256 == EXPECTED_RUNNER_SHA256
    )
    external_identity_exact = (
        len(external_runner_bytes) == EXPECTED_RUNNER_BYTES
        and external_sha256 == EXPECTED_RUNNER_SHA256
    )
    valid_audit = _audit_source(valid_bytes)
    external_audit = _audit_source(external_runner_bytes)
    fixture_outcomes = []
    negative_rejected = 0
    exact_single_failure_matches = 0
    parse_failures = 0
    matrix_failed_checks = []
    for fixture_name, expected_check in FIXTURE_SPECS:
        fixture_source = _negative_source_rc1(fixture_name)
        if fixture_source is None:
            fixture_audit = {
                "status": "fail",
                "failed_checks": [],
            }
            parse_failures += 1
        else:
            fixture_audit = _audit_source(fixture_source.encode("utf-8"))
            if "AST_PARSE" in fixture_audit["failed_checks"]:
                parse_failures += 1
        actual_failed_checks = fixture_audit["failed_checks"]
        if fixture_audit["status"] == "fail":
            negative_rejected += 1
        if actual_failed_checks == [expected_check]:
            exact_single_failure_matches += 1
        else:
            matrix_failed_checks.append(expected_check)
            matrix_failed_checks.extend(actual_failed_checks)
        fixture_outcomes.append(
            {
                "fixture": fixture_name,
                "expected_check": expected_check,
                "failed_checks": actual_failed_checks,
            }
        )
    embedded_external_equal = external_runner_bytes == valid_bytes
    matrix_pass = (
        embedded_identity_exact
        and external_identity_exact
        and valid_audit["status"] == "pass"
        and external_audit["status"] == "pass"
        and embedded_external_equal
        and len(FIXTURE_SPECS) == 31
        and negative_rejected == 31
        and exact_single_failure_matches == 31
        and parse_failures == 0
    )
    if valid_audit["status"] != "pass":
        matrix_failed_checks.extend(valid_audit["failed_checks"])
    if external_audit["status"] != "pass":
        matrix_failed_checks.extend(external_audit["failed_checks"])
    schema = QUALIFICATION_SCHEMA if qualification else MATRIX_SCHEMA
    return {
        "schema": schema,
        "version": VERSION,
        "status": "pass" if matrix_pass else "fail",
        "valid_fixture_checks_passed": valid_audit["checks_passed"],
        "valid_fixture_checks_total": valid_audit["checks_total"],
        "external_runner_checks_passed": external_audit["checks_passed"],
        "external_runner_checks_total": external_audit["checks_total"],
        "negative_fixtures_tested": len(FIXTURE_SPECS),
        "negative_fixtures_rejected": negative_rejected,
        "exact_single_failure_matches": exact_single_failure_matches,
        "fixture_parse_failures": parse_failures,
        "embedded_identity_exact": embedded_identity_exact,
        "external_identity_exact": external_identity_exact,
        "embedded_external_equal": embedded_external_equal,
        "embedded_frozen_external_equal": embedded_external_equal,
        "embedded_runner_bytes": len(valid_bytes),
        "embedded_runner_sha256": valid_sha256,
        "external_runner_bytes": len(external_runner_bytes),
        "external_runner_sha256": external_sha256,
        "runner_reads": 1,
        "runner_reopens": 0,
        "runner_executions": 0,
        "environment_reads": 0,
        "receipt_reads": 0,
        "product_access": 0,
        "safe_failed_check_identifiers": True,
        "failed_checks": _ordered_safe_checks(matrix_failed_checks),
        "fixture_outcomes": fixture_outcomes,
    }


def _safe_cli_failure():
    return {
        "schema": AUDIT_SCHEMA,
        "version": VERSION,
        "status": "fail",
        "failed_checks": [],
    }


def _emit(result):
    print(
        json.dumps(
            result,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=False,
        )
    )


def main():
    try:
        if (
            len(sys.argv) != 3
            or sys.argv[1] not in {"--matrix-runner", "--qualify-runner"}
        ):
            _emit(_safe_cli_failure())
            return 2
        runner_path = Path(sys.argv[2])
        if (
            not runner_path.is_absolute()
            or runner_path.name != EXPECTED_RUNNER_BASENAME
            or not runner_path.is_file()
        ):
            _emit(_safe_cli_failure())
            return 2
        external_runner_bytes = runner_path.read_bytes()
        result = _execute_matrix(
            external_runner_bytes,
            qualification=sys.argv[1] == "--qualify-runner",
        )
        _emit(result)
        return 0 if result["status"] == "pass" else 1
    except Exception:
        _emit(_safe_cli_failure())
        return 2


if __name__ == "__main__":
    sys.exit(main())
