"""File-based static auditor for a governed Sentigraph CIB capture runner."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from typing import Any, Callable


VERSION = "0.1"
APPROVED_ENVIRONMENT_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)
RUNNER_IMPORT_ALLOWLIST = frozenset({"os", "re", "json", "hashlib", "secrets", "sys"})
CHECK_NAMES = (
    "SOURCE_UTF8_NO_BOM",
    "SOURCE_PARSE",
    "IMPORT_ALLOWLIST",
    "EXACT_ENVIRONMENT_LOOKUPS",
    "ENVIRONMENT_LOOKUP_ORDER",
    "NO_ENVIRONMENT_ENUMERATION",
    "EXACT_ONE_SALT_GENERATION",
    "EXACT_ONE_COMBINED_SHA256",
    "ZERO_PER_VARIABLE_HASHES",
    "CANONICAL_OBJECT_FIELD_ORDER",
    "CONFIGURATION_VALUES_SHAPE",
    "SAFE_RECEIPT_FIELD_ORDER",
    "CURRENT_PRODUCT_CONSTANTS",
    "SAFE_RECEIPT_PUBLICATION",
    "NONDISCLOSING_OUTPUT",
    "FORBIDDEN_OPERATION_SCAN",
)
CANONICAL_OBJECT_FIELDS = (
    "schema",
    "version",
    "binding_scope",
    "service_blob",
    "registry_schema",
    "sample_handle",
    "result_file_name",
    "route_mode",
    "capability_label",
    "salt_hex",
    "configuration_values",
)
SAFE_RECEIPT_FIELDS = (
    "schema",
    "version",
    "binding_scope",
    "service_blob",
    "registry_schema",
    "sample_handle",
    "result_file_name",
    "route_mode",
    "capability_label",
    "variable_names",
    "salt_hex",
    "combined_binding_sha256",
    "canonicalization_label",
    "configuration_source",
    "environment_read_count",
    "binding_status",
    "raw_values_exposed",
    "per_variable_hashes_created",
    "path_operations_performed",
    "application_imported",
    "artifact_accessed",
    "endpoint_called",
    "runtime_authorized",
)
CANONICAL_CONSTANTS: dict[str, object] = {
    "schema": "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",
    "version": "0.1",
    "binding_scope": "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
    "service_blob": "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
    "registry_schema": "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
    "sample_handle": "helldivers2-psn-demo",
    "result_file_name": "provider_result_helldivers2-psn-demo_20260720_123627.json",
    "route_mode": "internal_alpha_read_only_local_exchange_projection_operator",
    "capability_label": "b05_local_exchange_projection_read_only",
}
RECEIPT_CONSTANTS: dict[str, object] = {
    "schema": "sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1",
    "version": "0.1",
    "binding_scope": "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
    "service_blob": "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
    "registry_schema": "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
    "sample_handle": "helldivers2-psn-demo",
    "result_file_name": "provider_result_helldivers2-psn-demo_20260720_123627.json",
    "route_mode": "internal_alpha_read_only_local_exchange_projection_operator",
    "capability_label": "b05_local_exchange_projection_read_only",
    "canonicalization_label": "sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1",
    "configuration_source": "process_environment_exact_names_only",
    "environment_read_count": 3,
    "binding_status": "configuration_identity_bound",
    "raw_values_exposed": False,
    "per_variable_hashes_created": False,
    "path_operations_performed": False,
    "application_imported": False,
    "artifact_accessed": False,
    "endpoint_called": False,
    "runtime_authorized": False,
}
ALLOWED_OUTPUT_PATTERN = re.compile(r"^SENTIGRAPH_CIB_CAPTURE_STATUS=[A-Z0-9_]+\n?$")
FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "pathlib",
        "subprocess",
        "socket",
        "http",
        "urllib",
        "requests",
        "sqlite3",
        "winreg",
        "ctypes",
        "tempfile",
        "glob",
        "shutil",
        "logging",
        "traceback",
        "backend",
        "app",
    }
)
FORBIDDEN_CALL_NAMES = frozenset(
    {
        "eval",
        "exec",
        "compile",
        "__import__",
        "input",
        "os.getenv",
        "os.putenv",
        "os.unsetenv",
        "os.listdir",
        "os.scandir",
        "os.walk",
        "os.stat",
        "os.lstat",
        "os.system",
        "os.popen",
        "glob.glob",
        "Path",
        "resolve",
        "exists",
        "is_file",
        "is_dir",
    }
)


class AuditStructureError(Exception):
    """Internal bounded structural-check failure."""


def _require(condition: bool) -> None:
    if not condition:
        raise AuditStructureError


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    result: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            result[child] = parent
    return result


def _assignment_value(tree: ast.AST, name: str) -> ast.AST:
    matches: list[ast.AST] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id == name:
            matches.append(node.value)
    _require(len(matches) == 1)
    return matches[0]


def _function(tree: ast.AST, name: str) -> ast.FunctionDef:
    matches = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    _require(len(matches) == 1)
    return matches[0]


def _dict_items(node: ast.AST) -> tuple[list[str], dict[str, ast.AST]]:
    _require(isinstance(node, ast.Dict))
    keys: list[str] = []
    values: list[ast.AST] = []
    for key, value in zip(node.keys, node.values):
        _require(isinstance(key, ast.Constant) and isinstance(key.value, str))
        keys.append(key.value)
        values.append(value)
    _require(len(keys) == len(set(keys)))
    return keys, dict(zip(keys, values))


def _is_os_environ(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "environ"
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
    )


def _is_os_environ_get(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "get"
        and _is_os_environ(node.value)
    )


def _environment_calls(tree: ast.AST) -> list[ast.Call]:
    return sorted(
        [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and _is_os_environ_get(node.func)
        ],
        key=lambda node: (node.lineno, node.col_offset),
    )


def _environment_bindings(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> list[str]:
    bindings: list[str] = []
    for call in _environment_calls(tree):
        assignment = parent_map.get(call)
        _require(isinstance(assignment, ast.Assign) and assignment.value is call)
        _require(len(assignment.targets) == 1)
        target = assignment.targets[0]
        _require(isinstance(target, ast.Name))
        bindings.append(target.id)
    return bindings


def _compact_json_bytes_assignment(
    tree: ast.AST,
    parent_map: dict[ast.AST, ast.AST],
    assignment_name: str,
    object_name: str,
) -> bool:
    value = _assignment_value(tree, assignment_name)
    if not (
        isinstance(value, ast.Call)
        and isinstance(value.func, ast.Attribute)
        and value.func.attr == "encode"
    ):
        return False
    if len(value.args) != 1 or not isinstance(value.args[0], ast.Constant):
        return False
    if value.args[0].value != "utf-8" or value.keywords:
        return False
    encode_attribute = value.func
    if not isinstance(encode_attribute, ast.Attribute):
        return False
    dump_call = encode_attribute.value
    if not isinstance(dump_call, ast.Call) or _call_name(dump_call.func) != "json.dumps":
        return False
    if len(dump_call.args) != 1 or not isinstance(dump_call.args[0], ast.Name):
        return False
    if dump_call.args[0].id != object_name:
        return False
    keywords = {keyword.arg: keyword.value for keyword in dump_call.keywords}
    if set(keywords) != {"ensure_ascii", "separators", "sort_keys"}:
        return False
    if not (
        isinstance(keywords["ensure_ascii"], ast.Constant)
        and keywords["ensure_ascii"].value is False
        and isinstance(keywords["sort_keys"], ast.Constant)
        and keywords["sort_keys"].value is False
    ):
        return False
    separators = keywords["separators"]
    return (
        isinstance(separators, ast.Tuple)
        and len(separators.elts) == 2
        and all(isinstance(item, ast.Constant) for item in separators.elts)
        and [item.value for item in separators.elts] == [",", ":"]
        and parent_map.get(dump_call) is encode_attribute
    )


def _check_import_allowlist(tree: ast.AST) -> bool:
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            return False
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname is not None:
                    return False
                imports.append(alias.name.split(".")[0])
    return bool(imports) and set(imports).issubset(RUNNER_IMPORT_ALLOWLIST)


def _check_exact_environment_lookups(tree: ast.AST) -> bool:
    calls = _environment_calls(tree)
    if len(calls) != 3:
        return False
    for call in calls:
        if len(call.args) != 1 or call.keywords:
            return False
        if not isinstance(call.args[0], ast.Constant) or not isinstance(call.args[0].value, str):
            return False
    return sorted(call.args[0].value for call in calls) == sorted(APPROVED_ENVIRONMENT_NAMES)


def _check_environment_order(tree: ast.AST) -> bool:
    calls = _environment_calls(tree)
    if len(calls) != 3:
        return False
    return [call.args[0].value for call in calls] == list(APPROVED_ENVIRONMENT_NAMES)


def _check_no_environment_enumeration(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    calls = _environment_calls(tree)
    environ_nodes = [node for node in ast.walk(tree) if _is_os_environ(node)]
    if len(environ_nodes) != 3:
        return False
    for node in environ_nodes:
        get_attribute = parent_map.get(node)
        if not (
            isinstance(get_attribute, ast.Attribute)
            and get_attribute.attr == "get"
            and isinstance(parent_map.get(get_attribute), ast.Call)
            and parent_map[get_attribute] in calls
        ):
            return False
    if any(
        isinstance(node, ast.Subscript) and _is_os_environ(node.value)
        for node in ast.walk(tree)
    ):
        return False
    forbidden_environment_calls = {
        "os.getenv",
        "os.putenv",
        "os.unsetenv",
        "os.environ.keys",
        "os.environ.items",
        "os.environ.values",
    }
    return not any(
        isinstance(node, ast.Call) and _call_name(node.func) in forbidden_environment_calls
        for node in ast.walk(tree)
    )


def _check_one_salt(tree: ast.AST) -> bool:
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "secrets.token_bytes"
    ]
    return (
        len(calls) == 1
        and len(calls[0].args) == 1
        and isinstance(calls[0].args[0], ast.Constant)
        and calls[0].args[0].value == 32
        and not calls[0].keywords
    )


def _combined_hash_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "hashlib.sha256"
    ]


def _check_one_combined_hash(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    calls = _combined_hash_calls(tree)
    if len(calls) != 1:
        return False
    call = calls[0]
    if not (
        len(call.args) == 1
        and isinstance(call.args[0], ast.Name)
        and call.args[0].id == "canonical_bytes"
        and not call.keywords
    ):
        return False
    hexdigest_attribute = parent_map.get(call)
    hexdigest_call = parent_map.get(hexdigest_attribute) if hexdigest_attribute else None
    return (
        isinstance(hexdigest_attribute, ast.Attribute)
        and hexdigest_attribute.attr == "hexdigest"
        and isinstance(hexdigest_call, ast.Call)
        and not hexdigest_call.args
        and not hexdigest_call.keywords
    )


def _check_zero_per_variable_hashes(tree: ast.AST) -> bool:
    calls = _combined_hash_calls(tree)
    return (
        len(calls) == 1
        and len(calls[0].args) == 1
        and isinstance(calls[0].args[0], ast.Name)
        and calls[0].args[0].id == "canonical_bytes"
        and not any(
            isinstance(node, ast.Call) and _call_name(node.func) == "hashlib.new"
            for node in ast.walk(tree)
        )
    )


def _check_canonical_order(tree: ast.AST) -> bool:
    try:
        keys, _ = _dict_items(_assignment_value(tree, "canonical_object"))
        return keys == list(CANONICAL_OBJECT_FIELDS)
    except AuditStructureError:
        return False


def _configuration_value_nodes(tree: ast.AST) -> tuple[list[ast.AST], list[str]]:
    canonical_node = _assignment_value(tree, "canonical_object")
    _, canonical_map = _dict_items(canonical_node)
    configuration_values = canonical_map["configuration_values"]
    _require(isinstance(configuration_values, ast.List) and len(configuration_values.elts) == 3)
    value_nodes: list[ast.AST] = []
    names: list[str] = []
    for item in configuration_values.elts:
        keys, item_map = _dict_items(item)
        _require(keys == ["name", "value"])
        _require(
            isinstance(item_map["name"], ast.Constant)
            and isinstance(item_map["name"].value, str)
        )
        names.append(item_map["name"].value)
        value_nodes.append(item_map["value"])
    return value_nodes, names


def _check_configuration_shape(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    try:
        value_nodes, names = _configuration_value_nodes(tree)
        bindings = _environment_bindings(tree, parent_map)
        return (
            names == list(APPROVED_ENVIRONMENT_NAMES)
            and all(isinstance(node, ast.Name) for node in value_nodes)
            and [node.id for node in value_nodes if isinstance(node, ast.Name)] == bindings
        )
    except AuditStructureError:
        return False


def _check_receipt_order(tree: ast.AST) -> bool:
    try:
        keys, _ = _dict_items(_assignment_value(tree, "safe_receipt"))
        return keys == list(SAFE_RECEIPT_FIELDS)
    except AuditStructureError:
        return False


def _constant_matches(node: ast.AST, expected: object) -> bool:
    return isinstance(node, ast.Constant) and type(node.value) is type(expected) and node.value == expected


def _check_validation_contract(tree: ast.AST) -> bool:
    try:
        bounded = _function(tree, "_valid_bounded_value")
        adapter = _function(tree, "_valid_adapter_id")
    except AuditStructureError:
        return False
    bounded_calls = {
        _call_name(node.func)
        for node in ast.walk(bounded)
        if isinstance(node, ast.Call)
    }
    bounded_constants = {
        node.value
        for node in ast.walk(bounded)
        if isinstance(node, ast.Constant) and isinstance(node.value, (str, int))
    }
    adapter_calls = [
        node
        for node in ast.walk(adapter)
        if isinstance(node, ast.Call) and _call_name(node.func) == "re.fullmatch"
    ]
    return (
        {"isinstance", "len", "value.strip", "value.isprintable"}.issubset(bounded_calls)
        and {1, 2048, "\x00"}.issubset(bounded_constants)
        and len(adapter_calls) == 1
        and len(adapter_calls[0].args) == 2
        and isinstance(adapter_calls[0].args[0], ast.Constant)
        and adapter_calls[0].args[0].value == r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"
        and isinstance(adapter_calls[0].args[1], ast.Name)
        and adapter_calls[0].args[1].id == "value"
    )


def _check_current_constants(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    try:
        _, canonical_map = _dict_items(_assignment_value(tree, "canonical_object"))
        _, receipt_map = _dict_items(_assignment_value(tree, "safe_receipt"))
        for key, expected in CANONICAL_CONSTANTS.items():
            if not _constant_matches(canonical_map[key], expected):
                return False
        for key, expected in RECEIPT_CONSTANTS.items():
            if not _constant_matches(receipt_map[key], expected):
                return False
        variable_names = receipt_map["variable_names"]
        if not isinstance(variable_names, ast.List):
            return False
        if not all(isinstance(node, ast.Constant) for node in variable_names.elts):
            return False
        if [node.value for node in variable_names.elts] != list(APPROVED_ENVIRONMENT_NAMES):
            return False
        if not (
            isinstance(canonical_map["salt_hex"], ast.Name)
            and canonical_map["salt_hex"].id == "salt_hex"
            and isinstance(receipt_map["salt_hex"], ast.Name)
            and receipt_map["salt_hex"].id == "salt_hex"
            and isinstance(receipt_map["combined_binding_sha256"], ast.Name)
            and receipt_map["combined_binding_sha256"].id == "combined_binding_sha256"
        ):
            return False
        if not _check_validation_contract(tree):
            return False
        return (
            _compact_json_bytes_assignment(tree, parent_map, "canonical_bytes", "canonical_object")
            and _compact_json_bytes_assignment(tree, parent_map, "receipt_bytes", "safe_receipt")
        )
    except (AuditStructureError, KeyError):
        return False


def _check_publication(tree: ast.AST, parent_map: dict[ast.AST, ast.AST]) -> bool:
    open_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "open"
    ]
    write_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "stream.write"
    ]
    flush_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "stream.flush"
    ]
    fsync_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "os.fsync"
    ]
    replace_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "os.replace"
    ]
    try:
        receipt_path = _assignment_value(tree, "RECEIPT_PATH")
        partial_path = _assignment_value(tree, "PARTIAL_PATH")
    except AuditStructureError:
        return False
    if not (
        isinstance(receipt_path, ast.Constant)
        and isinstance(receipt_path.value, str)
        and isinstance(partial_path, ast.Constant)
        and isinstance(partial_path.value, str)
        and receipt_path.value
        and partial_path.value
        and receipt_path.value != partial_path.value
    ):
        return False
    if not (
        len(open_calls) == 1
        and len(open_calls[0].args) == 2
        and isinstance(open_calls[0].args[0], ast.Name)
        and open_calls[0].args[0].id == "PARTIAL_PATH"
        and isinstance(open_calls[0].args[1], ast.Constant)
        and open_calls[0].args[1].value == "xb"
        and isinstance(parent_map.get(open_calls[0]), ast.withitem)
    ):
        return False
    if not (
        len(write_calls) == 1
        and len(write_calls[0].args) == 1
        and isinstance(write_calls[0].args[0], ast.Name)
        and write_calls[0].args[0].id == "receipt_bytes"
        and len(flush_calls) == 1
        and not flush_calls[0].args
        and len(fsync_calls) == 1
        and len(fsync_calls[0].args) == 1
        and isinstance(fsync_calls[0].args[0], ast.Call)
        and _call_name(fsync_calls[0].args[0].func) == "stream.fileno"
        and not fsync_calls[0].args[0].args
        and not fsync_calls[0].args[0].keywords
        and len(replace_calls) == 1
        and len(replace_calls[0].args) == 2
        and all(isinstance(node, ast.Name) for node in replace_calls[0].args)
        and [node.id for node in replace_calls[0].args] == ["PARTIAL_PATH", "RECEIPT_PATH"]
    ):
        return False
    return not any(
        isinstance(node, (ast.For, ast.AsyncFor, ast.While)) for node in ast.walk(tree)
    )


def _check_nondisclosing_output(tree: ast.AST) -> bool:
    output_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _call_name(node.func) in {"print", "sys.stdout.write"}
    ]
    if not output_calls:
        return False
    for call in output_calls:
        if len(call.args) != 1 or call.keywords:
            return False
        argument = call.args[0]
        if not isinstance(argument, ast.Constant) or not isinstance(argument.value, str):
            return False
        if len(argument.value) > 128 or ALLOWED_OUTPUT_PATTERN.fullmatch(argument.value) is None:
            return False
    return not any(
        isinstance(node, ast.Attribute) and _call_name(node) == "sys.stderr"
        for node in ast.walk(tree)
    )


def _check_forbidden_operations(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    import_roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            return False
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
    if import_roots.intersection(FORBIDDEN_IMPORT_ROOTS):
        return False
    os_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "os"
    }
    if os_attributes != {"environ", "fsync", "replace"}:
        return False
    sys_attributes = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "sys"
    }
    if not sys_attributes.issubset({"stdout", "exit"}) or "stdin" in sys_attributes:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = _call_name(node.func)
            if name in FORBIDDEN_CALL_NAMES:
                return False
            if any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in (
                    "pathlib",
                    "subprocess",
                    "socket",
                    "http",
                    "urllib",
                    "requests",
                    "sqlite3",
                    "winreg",
                    "ctypes",
                    "tempfile",
                    "glob",
                    "shutil",
                    "logging",
                    "traceback",
                    "backend",
                    "app",
                )
            ):
                return False
        if isinstance(node, ast.keyword) and node.arg == "env":
            return False
        if isinstance(
            node,
            (ast.For, ast.AsyncFor, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp),
        ):
            return False
    try:
        value_nodes, _ = _configuration_value_nodes(tree)
        allowed_value_nodes = set(value_nodes)
        bindings = _environment_bindings(tree, parent_map)
    except AuditStructureError:
        return False
    load_counts = {name: 0 for name in bindings}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Name) or not isinstance(node.ctx, ast.Load):
            continue
        if node.id not in load_counts:
            continue
        load_counts[node.id] += 1
        parent = parent_map.get(node)
        allowed_validation = (
            isinstance(parent, ast.Call)
            and node in parent.args
            and _call_name(parent.func) in {"_valid_bounded_value", "_valid_adapter_id"}
        )
        if node not in allowed_value_nodes and not allowed_validation:
            return False
    return len(bindings) == 3 and all(count == 2 for count in load_counts.values())


def _dataflow_name_nodes(
    tree: ast.AST, name: str, context_type: type[ast.expr_context]
) -> list[ast.Name]:
    """Collect exact Name occurrences for one identifier and AST context."""

    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and node.id == name
        and isinstance(node.ctx, context_type)
    ]


def _dataflow_direct_assignment(tree: ast.AST, name: str) -> ast.Assign | None:
    """Return the sole ordinary direct assignment to a simple name."""

    assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == name
    ]
    if len(assignments) != 1:
        return None
    return assignments[0]


def _dataflow_has_alternate_target(
    tree: ast.AST, name: str, allowed_assignment: ast.Assign
) -> bool:
    """Reject alternate, destructuring, annotated, augmented, or named targets."""

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if node is allowed_assignment:
                continue
            if any(
                isinstance(candidate, ast.Name)
                and candidate.id == name
                and isinstance(candidate.ctx, ast.Store)
                for target in node.targets
                for candidate in ast.walk(target)
            ):
                return True
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign, ast.NamedExpr)):
            target = node.target
            if any(
                isinstance(candidate, ast.Name) and candidate.id == name
                for candidate in ast.walk(target)
            ):
                return True
    return any(
        isinstance(node, ast.Name)
        and node.id == name
        and isinstance(node.ctx, ast.Del)
        for node in ast.walk(tree)
    )


def _dataflow_dict_field(
    tree: ast.AST, object_name: str, field_name: str
) -> ast.expr | None:
    """Return a field value from the sole direct dict-literal assignment."""

    assignment = _dataflow_direct_assignment(tree, object_name)
    if assignment is None or not isinstance(assignment.value, ast.Dict):
        return None
    matches: list[ast.expr] = []
    for key, value in zip(assignment.value.keys, assignment.value.values):
        if (
            isinstance(key, ast.Constant)
            and isinstance(key.value, str)
            and key.value == field_name
        ):
            matches.append(value)
    if len(matches) != 1:
        return None
    return matches[0]


def _dataflow_compact_json_object_load(
    tree: ast.AST, object_name: str, bytes_name: str
) -> ast.Name | None:
    """Prove the exact compact JSON-to-UTF-8 assignment and return its object Load."""

    assignment = _dataflow_direct_assignment(tree, bytes_name)
    if assignment is None or not isinstance(assignment.value, ast.Call):
        return None
    encode_call = assignment.value
    if not (
        isinstance(encode_call.func, ast.Attribute)
        and encode_call.func.attr == "encode"
        and len(encode_call.args) == 1
        and isinstance(encode_call.args[0], ast.Constant)
        and encode_call.args[0].value == "utf-8"
        and not encode_call.keywords
        and isinstance(encode_call.func.value, ast.Call)
    ):
        return None
    dumps_call = encode_call.func.value
    if not (
        _call_name(dumps_call.func) == "json.dumps"
        and len(dumps_call.args) == 1
        and isinstance(dumps_call.args[0], ast.Name)
        and dumps_call.args[0].id == object_name
        and isinstance(dumps_call.args[0].ctx, ast.Load)
        and len(dumps_call.keywords) == 3
    ):
        return None
    keywords = {keyword.arg: keyword.value for keyword in dumps_call.keywords}
    if set(keywords) != {"ensure_ascii", "separators", "sort_keys"}:
        return None
    separators = keywords["separators"]
    if not (
        isinstance(keywords["ensure_ascii"], ast.Constant)
        and keywords["ensure_ascii"].value is False
        and isinstance(separators, ast.Tuple)
        and len(separators.elts) == 2
        and all(isinstance(element, ast.Constant) for element in separators.elts)
        and [element.value for element in separators.elts] == [",", ":"]
        and isinstance(keywords["sort_keys"], ast.Constant)
        and keywords["sort_keys"].value is False
    ):
        return None
    return dumps_call.args[0]


def _dataflow_object_is_immutable_single_use(
    tree: ast.AST, object_name: str, bytes_name: str
) -> bool:
    """Require one dict Store and one exact serialization Load with no mutation."""

    assignment = _dataflow_direct_assignment(tree, object_name)
    serialization_load = _dataflow_compact_json_object_load(
        tree, object_name, bytes_name
    )
    stores = _dataflow_name_nodes(tree, object_name, ast.Store)
    loads = _dataflow_name_nodes(tree, object_name, ast.Load)
    return bool(
        assignment is not None
        and isinstance(assignment.value, ast.Dict)
        and not _dataflow_has_alternate_target(tree, object_name, assignment)
        and len(stores) == 1
        and stores[0] is assignment.targets[0]
        and len(loads) == 1
        and serialization_load is not None
        and loads[0] is serialization_load
    )


_transport_check_one_salt = _check_one_salt
_transport_check_one_combined_hash = _check_one_combined_hash
_transport_check_current_constants = _check_current_constants


def _check_one_salt(tree: ast.AST) -> bool:
    """Prove salt generation, salt.hex(), and both salt_hex consumers by identity."""

    if not _transport_check_one_salt(tree):
        return False
    token_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and _call_name(node.func) == "secrets.token_bytes"
    ]
    if not (
        len(token_calls) == 1
        and len(token_calls[0].args) == 1
        and isinstance(token_calls[0].args[0], ast.Constant)
        and token_calls[0].args[0].value == 32
        and not token_calls[0].keywords
    ):
        return False
    salt_assignment = _dataflow_direct_assignment(tree, "salt")
    if not (
        salt_assignment is not None
        and salt_assignment.value is token_calls[0]
        and not _dataflow_has_alternate_target(tree, "salt", salt_assignment)
    ):
        return False
    salt_stores = _dataflow_name_nodes(tree, "salt", ast.Store)
    salt_loads = _dataflow_name_nodes(tree, "salt", ast.Load)
    if not (
        len(salt_stores) == 1
        and salt_stores[0] is salt_assignment.targets[0]
        and len(salt_loads) == 1
    ):
        return False
    hex_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "hex"
    ]
    if not (
        len(hex_calls) == 1
        and not hex_calls[0].args
        and not hex_calls[0].keywords
        and isinstance(hex_calls[0].func.value, ast.Name)
        and hex_calls[0].func.value.id == "salt"
        and isinstance(hex_calls[0].func.value.ctx, ast.Load)
        and salt_loads[0] is hex_calls[0].func.value
    ):
        return False
    salt_hex_assignment = _dataflow_direct_assignment(tree, "salt_hex")
    if not (
        salt_hex_assignment is not None
        and salt_hex_assignment.value is hex_calls[0]
        and not _dataflow_has_alternate_target(
            tree, "salt_hex", salt_hex_assignment
        )
    ):
        return False
    salt_hex_stores = _dataflow_name_nodes(tree, "salt_hex", ast.Store)
    salt_hex_loads = _dataflow_name_nodes(tree, "salt_hex", ast.Load)
    canonical_value = _dataflow_dict_field(tree, "canonical_object", "salt_hex")
    receipt_value = _dataflow_dict_field(tree, "safe_receipt", "salt_hex")
    if not (
        len(salt_hex_stores) == 1
        and salt_hex_stores[0] is salt_hex_assignment.targets[0]
        and len(salt_hex_loads) == 2
        and isinstance(canonical_value, ast.Name)
        and canonical_value.id == "salt_hex"
        and isinstance(canonical_value.ctx, ast.Load)
        and isinstance(receipt_value, ast.Name)
        and receipt_value.id == "salt_hex"
        and isinstance(receipt_value.ctx, ast.Load)
    ):
        return False
    return all(
        node is canonical_value or node is receipt_value for node in salt_hex_loads
    ) and canonical_value is not receipt_value


def _check_one_combined_hash(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    """Prove canonical-byte hashing and receipt digest use by AST identity."""

    if not _transport_check_one_combined_hash(tree, parent_map):
        return False
    sha_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "hashlib.sha256"
    ]
    if not (
        len(sha_calls) == 1
        and len(sha_calls[0].args) == 1
        and isinstance(sha_calls[0].args[0], ast.Name)
        and sha_calls[0].args[0].id == "canonical_bytes"
        and isinstance(sha_calls[0].args[0].ctx, ast.Load)
        and not sha_calls[0].keywords
    ):
        return False
    digest_attribute = parent_map.get(sha_calls[0])
    digest_call = parent_map.get(digest_attribute)
    if not (
        isinstance(digest_attribute, ast.Attribute)
        and digest_attribute.value is sha_calls[0]
        and digest_attribute.attr == "hexdigest"
        and isinstance(digest_call, ast.Call)
        and digest_call.func is digest_attribute
        and not digest_call.args
        and not digest_call.keywords
    ):
        return False
    combined_assignment = _dataflow_direct_assignment(
        tree, "combined_binding_sha256"
    )
    if not (
        combined_assignment is not None
        and combined_assignment.value is digest_call
        and not _dataflow_has_alternate_target(
            tree, "combined_binding_sha256", combined_assignment
        )
    ):
        return False
    combined_stores = _dataflow_name_nodes(
        tree, "combined_binding_sha256", ast.Store
    )
    combined_loads = _dataflow_name_nodes(
        tree, "combined_binding_sha256", ast.Load
    )
    receipt_value = _dataflow_dict_field(
        tree, "safe_receipt", "combined_binding_sha256"
    )
    if not (
        len(combined_stores) == 1
        and combined_stores[0] is combined_assignment.targets[0]
        and len(combined_loads) == 1
        and isinstance(receipt_value, ast.Name)
        and receipt_value.id == "combined_binding_sha256"
        and isinstance(receipt_value.ctx, ast.Load)
        and combined_loads[0] is receipt_value
    ):
        return False
    canonical_assignment = _dataflow_direct_assignment(tree, "canonical_bytes")
    canonical_stores = _dataflow_name_nodes(tree, "canonical_bytes", ast.Store)
    canonical_loads = _dataflow_name_nodes(tree, "canonical_bytes", ast.Load)
    canonical_object_load = _dataflow_compact_json_object_load(
        tree, "canonical_object", "canonical_bytes"
    )
    return bool(
        canonical_assignment is not None
        and canonical_object_load is not None
        and not _dataflow_has_alternate_target(
            tree, "canonical_bytes", canonical_assignment
        )
        and len(canonical_stores) == 1
        and canonical_stores[0] is canonical_assignment.targets[0]
        and len(canonical_loads) == 1
        and canonical_loads[0] is sha_calls[0].args[0]
    )


def _check_current_constants(
    tree: ast.AST, parent_map: dict[ast.AST, ast.AST]
) -> bool:
    """Retain constants while enforcing immutable single-use binding objects."""

    return bool(
        _transport_check_current_constants(tree, parent_map)
        and _dataflow_object_is_immutable_single_use(
            tree, "canonical_object", "canonical_bytes"
        )
        and _dataflow_object_is_immutable_single_use(
            tree, "safe_receipt", "receipt_bytes"
        )
    )


def _evaluate_checks(text: str, tree: ast.AST) -> dict[str, bool]:
    parent_map = _parents(tree)
    check_functions: dict[str, Callable[[], bool]] = {
        "IMPORT_ALLOWLIST": lambda: _check_import_allowlist(tree),
        "EXACT_ENVIRONMENT_LOOKUPS": lambda: _check_exact_environment_lookups(tree),
        "ENVIRONMENT_LOOKUP_ORDER": lambda: _check_environment_order(tree),
        "NO_ENVIRONMENT_ENUMERATION": lambda: _check_no_environment_enumeration(tree, parent_map),
        "EXACT_ONE_SALT_GENERATION": lambda: _check_one_salt(tree),
        "EXACT_ONE_COMBINED_SHA256": lambda: _check_one_combined_hash(tree, parent_map),
        "ZERO_PER_VARIABLE_HASHES": lambda: _check_zero_per_variable_hashes(tree),
        "CANONICAL_OBJECT_FIELD_ORDER": lambda: _check_canonical_order(tree),
        "CONFIGURATION_VALUES_SHAPE": lambda: _check_configuration_shape(tree, parent_map),
        "SAFE_RECEIPT_FIELD_ORDER": lambda: _check_receipt_order(tree),
        "CURRENT_PRODUCT_CONSTANTS": lambda: _check_current_constants(tree, parent_map),
        "SAFE_RECEIPT_PUBLICATION": lambda: _check_publication(tree, parent_map),
        "NONDISCLOSING_OUTPUT": lambda: _check_nondisclosing_output(tree),
        "FORBIDDEN_OPERATION_SCAN": lambda: _check_forbidden_operations(tree, parent_map),
    }
    results = {name: True for name in CHECK_NAMES}
    for name, function in check_functions.items():
        try:
            results[name] = bool(function())
        except Exception:
            results[name] = False
    return results


def _audit_source_bytes(source_bytes: bytes) -> dict[str, Any]:
    runner_sha256 = hashlib.sha256(source_bytes).hexdigest()
    results = {name: False for name in CHECK_NAMES}
    if source_bytes.startswith(b"\xef\xbb\xbf"):
        return {
            "runner_bytes": len(source_bytes),
            "runner_sha256": runner_sha256,
            "checks": results,
        }
    try:
        source_text = source_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return {
            "runner_bytes": len(source_bytes),
            "runner_sha256": runner_sha256,
            "checks": results,
        }
    results["SOURCE_UTF8_NO_BOM"] = True
    try:
        tree = ast.parse(source_text)
    except SyntaxError:
        return {
            "runner_bytes": len(source_bytes),
            "runner_sha256": runner_sha256,
            "checks": results,
        }
    results["SOURCE_PARSE"] = True
    results.update(_evaluate_checks(source_text, tree))
    return {
        "runner_bytes": len(source_bytes),
        "runner_sha256": runner_sha256,
        "checks": results,
    }


VALID_FIXTURE_SOURCE = r'''import hashlib
import json
import os
import re
import secrets
import sys

RECEIPT_PATH = r"C:\sentigraph_public_fixture\safe_receipt.json"
PARTIAL_PATH = r"C:\sentigraph_public_fixture\safe_receipt.json.partial"

def _valid_bounded_value(value):
    return (
        isinstance(value, str)
        and 1 <= len(value) <= 2048
        and value == value.strip()
        and value.isprintable()
        and "\x00" not in value
    )

def _valid_adapter_id(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value) is not None

def capture():
    results_dir = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR")
    export_root = os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT")
    adapter_id = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID")
    if not _valid_bounded_value(results_dir):
        sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=BLOCKED_CONFIGURATION_PRECONDITION\n")
        return 2
    if not _valid_bounded_value(export_root):
        sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=BLOCKED_CONFIGURATION_PRECONDITION\n")
        return 2
    if not _valid_adapter_id(adapter_id):
        sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=BLOCKED_CONFIGURATION_PRECONDITION\n")
        return 2
    salt = secrets.token_bytes(32)
    salt_hex = salt.hex()
    canonical_object = {
        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",
        "version": "0.1",
        "binding_scope": "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
        "service_blob": "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
        "registry_schema": "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
        "sample_handle": "helldivers2-psn-demo",
        "result_file_name": "provider_result_helldivers2-psn-demo_20260720_123627.json",
        "route_mode": "internal_alpha_read_only_local_exchange_projection_operator",
        "capability_label": "b05_local_exchange_projection_read_only",
        "salt_hex": salt_hex,
        "configuration_values": [
            {"name": "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR", "value": results_dir},
            {"name": "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT", "value": export_root},
            {"name": "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID", "value": adapter_id},
        ],
    }
    canonical_bytes = json.dumps(canonical_object, ensure_ascii=False, separators=(",", ":"), sort_keys=False).encode("utf-8")
    combined_binding_sha256 = hashlib.sha256(canonical_bytes).hexdigest()
    safe_receipt = {
        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1",
        "version": "0.1",
        "binding_scope": "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
        "service_blob": "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
        "registry_schema": "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
        "sample_handle": "helldivers2-psn-demo",
        "result_file_name": "provider_result_helldivers2-psn-demo_20260720_123627.json",
        "route_mode": "internal_alpha_read_only_local_exchange_projection_operator",
        "capability_label": "b05_local_exchange_projection_read_only",
        "variable_names": [
            "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
            "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
            "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
        ],
        "salt_hex": salt_hex,
        "combined_binding_sha256": combined_binding_sha256,
        "canonicalization_label": "sentigraph_ordered_utf8_compact_json_salted_sha256_v0_1",
        "configuration_source": "process_environment_exact_names_only",
        "environment_read_count": 3,
        "binding_status": "configuration_identity_bound",
        "raw_values_exposed": False,
        "per_variable_hashes_created": False,
        "path_operations_performed": False,
        "application_imported": False,
        "artifact_accessed": False,
        "endpoint_called": False,
        "runtime_authorized": False,
    }
    receipt_bytes = json.dumps(safe_receipt, ensure_ascii=False, separators=(",", ":"), sort_keys=False).encode("utf-8")
    with open(PARTIAL_PATH, "xb") as stream:
        stream.write(receipt_bytes)
        stream.flush()
        try:
            os.fsync(stream.fileno())
        except OSError:
            pass
    os.replace(PARTIAL_PATH, RECEIPT_PATH)
    sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=SUCCESS\n")
    return 0

def main():
    try:
        return capture()
    except Exception:
        sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=FAILURE_INTERNAL\n")
        return 70

if __name__ == "__main__":
    sys.exit(main())
'''


def _replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise AuditStructureError
    return source.replace(old, new, 1)


def _self_test_fixtures() -> list[tuple[str, str | None]]:
    valid = VALID_FIXTURE_SOURCE
    lookup_block = (
        '    results_dir = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR")\n'
        '    export_root = os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT")\n'
        '    adapter_id = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID")'
    )
    wrong_order_block = (
        '    export_root = os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT")\n'
        '    results_dir = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR")\n'
        '    adapter_id = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID")'
    )
    canonical_prefix = (
        '        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",\n'
        '        "version": "0.1",'
    )
    canonical_swapped = (
        '        "version": "0.1",\n'
        '        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",'
    )
    receipt_prefix = (
        '        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1",\n'
        '        "version": "0.1",'
    )
    receipt_swapped = (
        '        "version": "0.1",\n'
        '        "schema": "sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1",'
    )
    fixtures = [
        (valid, None),
        (valid + "\nif (\n", "SOURCE_PARSE"),
        ("import pathlib\n" + valid, "IMPORT_ALLOWLIST"),
        (
            _replace_once(
                valid,
                lookup_block,
                lookup_block + '\n    extra_value = os.environ.get("SENTIGRAPH_EXTRA_VALUE")',
            ),
            "EXACT_ENVIRONMENT_LOOKUPS",
        ),
        (_replace_once(valid, lookup_block, wrong_order_block), "ENVIRONMENT_LOOKUP_ORDER"),
        (
            _replace_once(valid, lookup_block, lookup_block + "\n    environment_snapshot = tuple(os.environ)"),
            "NO_ENVIRONMENT_ENUMERATION",
        ),
        (
            _replace_once(
                valid,
                "    salt = secrets.token_bytes(32)",
                "    salt = secrets.token_bytes(32)\n    second_salt = secrets.token_bytes(32)",
            ),
            "EXACT_ONE_SALT_GENERATION",
        ),
        (
            _replace_once(
                valid,
                "    combined_binding_sha256 = hashlib.sha256(canonical_bytes).hexdigest()",
                "    combined_binding_sha256 = hashlib.sha256(canonical_bytes).hexdigest()\n    per_variable_hash = hashlib.sha256(results_dir.encode(\"utf-8\")).hexdigest()",
            ),
            "ZERO_PER_VARIABLE_HASHES",
        ),
        (_replace_once(valid, canonical_prefix, canonical_swapped), "CANONICAL_OBJECT_FIELD_ORDER"),
        (_replace_once(valid, receipt_prefix, receipt_swapped), "SAFE_RECEIPT_FIELD_ORDER"),
        (
            _replace_once(
                valid,
                "    salt = secrets.token_bytes(32)",
                '    unsafe_stream = open(results_dir, "rb")\n    salt = secrets.token_bytes(32)',
            ),
            "FORBIDDEN_OPERATION_SCAN",
        ),
        (
            _replace_once(
                valid,
                '    sys.stdout.write("SENTIGRAPH_CIB_CAPTURE_STATUS=SUCCESS\\n")',
                "    sys.stdout.write(results_dir)",
            ),
            "NONDISCLOSING_OUTPUT",
        ),
        (_replace_once(valid, 'with open(PARTIAL_PATH, "xb")', 'with open(PARTIAL_PATH, "wb")'), "SAFE_RECEIPT_PUBLICATION"),
        (
            _replace_once(valid, lookup_block, lookup_block + "\n    supplied_input = sys.stdin.read()"),
            "FORBIDDEN_OPERATION_SCAN",
        ),
        (
            _replace_once(
                valid,
                "    salt = secrets.token_bytes(32)\n    salt_hex = salt.hex()",
                '    unused_salt = secrets.token_bytes(32)\n    salt_hex = "0" * 64',
            ),
            "EXACT_ONE_SALT_GENERATION",
        ),
        (
            _replace_once(
                valid,
                "    combined_binding_sha256 = hashlib.sha256(canonical_bytes).hexdigest()",
                '    unused_hash = hashlib.sha256(canonical_bytes).hexdigest()\n    combined_binding_sha256 = "0" * 64',
            ),
            "EXACT_ONE_COMBINED_SHA256",
        ),
    ]
    _require(len(fixtures) == 16)
    return fixtures


def _emit_self_test_result(passed_count: int) -> None:
    result = {
        "schema": "sentigraph_cib_capture_static_auditor_self_test_result_v0_1",
        "version": VERSION,
        "mode": "self_test",
        "fixture_count": 16,
        "passed_count": passed_count,
        "failed_count": 16 - passed_count,
        "status": "pass" if passed_count == 16 else "fail",
        "environment_accessed": False,
        "runner_executed": False,
    }
    sys.stdout.write(json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n")


def _run_self_test() -> int:
    passed_count = 0
    try:
        fixtures = _self_test_fixtures()
        for source, expected_failure in fixtures:
            outcome = _audit_source_bytes(source.encode("utf-8"))
            checks = outcome["checks"]
            status_pass = all(checks[name] for name in CHECK_NAMES)
            if expected_failure is None:
                fixture_passed = status_pass
            else:
                fixture_passed = not status_pass and checks[expected_failure] is False
            if fixture_passed:
                passed_count += 1
    except Exception:
        passed_count = 0
    _emit_self_test_result(passed_count)
    return 0 if passed_count == 16 else 1


def _emit_audit_result(
    outcome: dict[str, Any], runner_source_reads: int
) -> int:
    checks = outcome["checks"]
    checks_passed = sum(1 for name in CHECK_NAMES if checks[name])
    checks_failed = len(CHECK_NAMES) - checks_passed
    result = {
        "schema": "sentigraph_cib_capture_static_auditor_result_v0_1",
        "version": VERSION,
        "mode": "runner_file_audit",
        "status": "pass" if checks_failed == 0 else "fail",
        "runner_source_reads": runner_source_reads,
        "runner_source_reopens": 0,
        "runner_bytes": outcome["runner_bytes"],
        "runner_sha256": outcome["runner_sha256"],
        "check_names": list(CHECK_NAMES),
        "checks_passed": checks_passed,
        "checks_failed": checks_failed,
        "environment_accessed": False,
        "runner_executed": False,
    }
    sys.stdout.write(json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n")
    return 0 if checks_failed == 0 else 1


def _run_file_audit(runner_path: str) -> int:
    try:
        with open(runner_path, "rb") as stream:
            source_bytes = stream.read()
    except OSError:
        empty_outcome = {
            "runner_bytes": 0,
            "runner_sha256": "",
            "checks": {name: False for name in CHECK_NAMES},
        }
        return _emit_audit_result(empty_outcome, 0)
    outcome = _audit_source_bytes(source_bytes)
    return _emit_audit_result(outcome, 1)


def _emit_cli_failure() -> int:
    result = {
        "schema": "sentigraph_cib_capture_static_auditor_cli_error_v0_1",
        "version": VERSION,
        "status": "fail",
    }
    sys.stdout.write(json.dumps(result, ensure_ascii=True, separators=(",", ":")) + "\n")
    return 2


def main() -> int:
    arguments = sys.argv[1:]
    if arguments == ["--self-test"]:
        return _run_self_test()
    if len(arguments) == 2 and arguments[0] == "--audit-runner":
        return _run_file_audit(arguments[1])
    return _emit_cli_failure()


if __name__ == "__main__":
    raise SystemExit(main())
