from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path


AUDITOR_SCHEMA = "sentigraph_b05_get_smoke_runner_static_audit_v2_result_v0_1"
SELF_TEST_SCHEMA = "sentigraph_b05_get_smoke_static_auditor_v2_self_test_result_v0_1"
VERSION = "0.1"
RUNNER_BASENAME = ".sentigraph_b05_get_smoke_runner_v2.py"
MAX_RUNNER_BYTES = 262_144

EXPECTED_RUNNER_BASENAME = ".sentigraph_b05_get_smoke_runner_v2.py"
EXPECTED_RECEIPT_BASENAME = ".sentigraph_cib_capture_risk_prompt_3_v1_safe_receipt.json"
EXPECTED_RESULT_BASENAME = ".sentigraph_b05_get_smoke_result_v2.json"
EXPECTED_PARTIAL_BASENAME = ".sentigraph_b05_get_smoke_result_v2.json.partial"
EXPECTED_TARGET_ROUTE = (
    "/api/v1/internal/alpha/review-console/"
    "local-exchange-projections/helldivers2-psn-demo"
)
EXPECTED_RESULT_BASENAME_APPROVED = (
    "provider_result_helldivers2-psn-demo_20260720_123627.json"
)
EXPECTED_CONFIG_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)
EXPECTED_GATE_NAMES = (
    "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
)
EXPECTED_SAFE_METADATA_BASENAMES = (
    "manifest.json",
    "validation_report.json",
    "validation_report.md",
    "coverage_note.md",
    "README.md",
    "package_index.json",
)
EXPECTED_RAW_ROW_BASENAMES = (
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "collection_log.jsonl",
)

CHECK_NAMES = (
    "STRICT_UTF8_NO_BOM",
    "AST_PARSE",
    "IMPORT_ALLOWLIST",
    "BOUND_CONSTANTS",
    "RECEIPT_SINGLE_READ",
    "CONFIG_EXACT_THREE_READS",
    "CIB_DATAFLOW",
    "NO_RANDOM_OR_WEAK_HASH",
    "GATE_PRESTATE_EXACT_ORDER",
    "GATE_WRITE_EXACT_ORDER",
    "GATE_RESTORE_REVERSED_OUTER_FINALLY",
    "DOTENV_PATCH_BEFORE_APP_IMPORT",
    "DOTENV_RESTORE_OUTER_FINALLY",
    "APP_IMPORT_EXACTLY_ONCE",
    "EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT",
    "NO_ASYNCIO_RUN",
    "ASGI_TRANSPORT_EXACTLY_ONCE",
    "TARGET_ROUTE_EXACT",
    "HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET",
    "PERFORM_GET_CALLED_EXACTLY_ONCE",
    "RESPONSE_EXACT_52_FIELD_ORDER",
    "RESPONSE_BOUNDED_HASH_ONLY",
    "FILE_GUARD_BOUNDARY",
    "RAW_ROW_PRIVACY_FAIL_CLOSED",
    "NO_DIRECTORY_DISCOVERY",
    "NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED",
    "NO_EXTERNAL_OR_MUTATING_ACTIONS",
    "ATOMIC_SAFE_RESULT_AND_OUTPUT",
)

ALLOWED_RUNNER_IMPORT_ROOTS = {
    "__future__",
    "asyncio",
    "builtins",
    "dotenv",
    "glob",
    "hashlib",
    "hmac",
    "importlib",
    "io",
    "json",
    "os",
    "pathlib",
    "re",
    "socket",
    "subprocess",
    "sys",
}


def _expr_name(node: ast.AST, aliases: dict[str, str]) -> str:
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        base = _expr_name(node.value, aliases)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _target_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _target_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Subscript):
        return _target_name(node.value)
    return ""


def _build_aliases_and_imports(tree: ast.Module) -> tuple[dict[str, str], list[str]]:
    aliases: dict[str, str] = {}
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for item in node.names:
                imported_modules.append(item.name)
                aliases[item.asname or item.name.split(".")[0]] = item.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imported_modules.append(module)
            for item in node.names:
                resolved = f"{module}.{item.name}" if module else item.name
                aliases[item.asname or item.name] = resolved
    return aliases, imported_modules


def _functions(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _calls(
    node: ast.AST,
    aliases: dict[str, str],
    target: str | None = None,
) -> list[ast.Call]:
    result: list[ast.Call] = []
    for candidate in ast.walk(node):
        if not isinstance(candidate, ast.Call):
            continue
        name = _expr_name(candidate.func, aliases)
        if target is None or name == target:
            result.append(candidate)
    return sorted(
        result,
        key=lambda candidate: (
            getattr(candidate, "lineno", 0),
            getattr(candidate, "col_offset", 0),
        ),
    )


def _module_for_body(body: list[ast.stmt]) -> ast.Module:
    return ast.Module(body=body, type_ignores=[])


def _outer_try(
    function: ast.FunctionDef | ast.AsyncFunctionDef | None,
) -> ast.Try | None:
    if function is None:
        return None
    candidates = [
        statement
        for statement in function.body
        if isinstance(statement, ast.Try) and statement.finalbody
    ]
    return candidates[0] if len(candidates) == 1 else None


def _literal_assignment(tree: ast.Module, name: str):
    values: list[object] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            try:
                values.append(ast.literal_eval(node.value))
            except (ValueError, TypeError):
                return None
    return values[0] if len(values) == 1 else None


def _assignment_values(node: ast.AST, name: str) -> list[ast.AST]:
    values: list[ast.AST] = []
    for candidate in ast.walk(node):
        if not isinstance(candidate, (ast.Assign, ast.AnnAssign)):
            continue
        targets = (
            candidate.targets if isinstance(candidate, ast.Assign) else [candidate.target]
        )
        if any(isinstance(target, ast.Name) and target.id == name for target in targets):
            values.append(candidate.value)
    return values


def _subscript(node: ast.AST, base: str, key: str) -> bool:
    return (
        isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == base
        and isinstance(node.slice, ast.Constant)
        and node.slice.value == key
    )


def _keyword_value(call: ast.Call, name: str) -> ast.AST | None:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _compact_json_encode(
    node: ast.AST,
    aliases: dict[str, str],
    expected_argument: str,
) -> bool:
    if not (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "encode"
        and isinstance(node.func.value, ast.Call)
    ):
        return False
    dumps_call = node.func.value
    if _expr_name(dumps_call.func, aliases) != "json.dumps":
        return False
    if not (
        len(dumps_call.args) == 1
        and isinstance(dumps_call.args[0], ast.Name)
        and dumps_call.args[0].id == expected_argument
    ):
        return False
    ensure_ascii = _keyword_value(dumps_call, "ensure_ascii")
    separators = _keyword_value(dumps_call, "separators")
    sort_keys = _keyword_value(dumps_call, "sort_keys")
    try:
        return (
            ast.literal_eval(ensure_ascii) is False
            and ast.literal_eval(separators) == (",", ":")
            and ast.literal_eval(sort_keys) is False
            and (
                not node.args
                or (
                    len(node.args) == 1
                    and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "utf-8"
                )
            )
        )
    except (ValueError, TypeError):
        return False


def _sha256_hexdigest(
    node: ast.AST,
    aliases: dict[str, str],
    expected_argument: str,
) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "hexdigest"
        and isinstance(node.func.value, ast.Call)
        and _expr_name(node.func.value.func, aliases) == "hashlib.sha256"
        and len(node.func.value.args) == 1
        and isinstance(node.func.value.args[0], ast.Name)
        and node.func.value.args[0].id == expected_argument
    )


def _check_import_allowlist(context: dict[str, object]) -> bool:
    tree = context["tree"]
    imported_modules = context["imported_modules"]
    if not isinstance(tree, ast.Module) or not isinstance(imported_modules, list):
        return False
    roots = {name.split(".")[0] for name in imported_modules if name}
    if not roots or not roots <= ALLOWED_RUNNER_IMPORT_ROOTS:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("app"):
            return False
        if isinstance(node, ast.Import):
            if any(item.name.startswith("app") for item in node.names):
                return False
    return True


def _check_bound_constants(context: dict[str, object]) -> bool:
    tree = context["tree"]
    if not isinstance(tree, ast.Module):
        return False
    expected = {
        "RUNNER_BASENAME": EXPECTED_RUNNER_BASENAME,
        "RECEIPT_BASENAME": EXPECTED_RECEIPT_BASENAME,
        "RESULT_BASENAME": EXPECTED_RESULT_BASENAME,
        "PARTIAL_BASENAME": EXPECTED_PARTIAL_BASENAME,
        "RESULT_BASENAME_APPROVED": EXPECTED_RESULT_BASENAME_APPROVED,
        "CONFIG_NAMES": EXPECTED_CONFIG_NAMES,
        "GATE_NAMES": EXPECTED_GATE_NAMES,
    }
    return all(_literal_assignment(tree, name) == value for name, value in expected.items())


def _check_receipt_single_read(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    reader = functions.get("read_receipt_once")
    execution = functions.get("execute_once")
    if reader is None or execution is None:
        return False
    opens = _calls(reader, aliases, "builtins.open")
    reads = [
        call
        for call in _calls(reader, aliases)
        if _expr_name(call.func, aliases) == "stream.read"
    ]
    invocations = _calls(execution, aliases, "read_receipt_once")
    return (
        len(opens) == 1
        and len(opens[0].args) >= 2
        and isinstance(opens[0].args[1], ast.Constant)
        and opens[0].args[1].value == "rb"
        and len(reads) == 1
        and not reads[0].args
        and len(invocations) == 1
    )


def _check_config_exact_three_reads(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    reader = functions.get("read_configuration_values")
    execution = functions.get("execute_once")
    if reader is None or execution is None:
        return False
    names: list[str] = []
    for call in _calls(reader, aliases, "os.environ.get"):
        if not (
            call.args
            and isinstance(call.args[0], ast.Constant)
            and isinstance(call.args[0].value, str)
        ):
            return False
        names.append(call.args[0].value)
    return (
        tuple(names) == EXPECTED_CONFIG_NAMES
        and len(_calls(execution, aliases, "read_configuration_values")) == 1
    )


def _check_cib_dataflow(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    function = functions.get("verify_cib")
    if function is None:
        return False
    salt_values = _assignment_values(function, "salt_hex")
    config_values = _assignment_values(function, "configuration_values")
    canonical_values = _assignment_values(function, "canonical_object")
    byte_values = _assignment_values(function, "canonical_bytes")
    digest_values = _assignment_values(function, "recomputed_binding")
    if not (
        len(salt_values) == 1
        and _subscript(salt_values[0], "receipt", "salt_hex")
        and len(config_values) == 1
        and isinstance(config_values[0], ast.List)
        and len(config_values[0].elts) == 3
        and len(canonical_values) == 1
        and isinstance(canonical_values[0], ast.Dict)
        and len(byte_values) == 1
        and len(digest_values) == 1
    ):
        return False
    configuration_names: list[str] = []
    configuration_value_names: list[str] = []
    for item in config_values[0].elts:
        if not isinstance(item, ast.Dict) or len(item.keys) != 2:
            return False
        try:
            keys = [ast.literal_eval(key) for key in item.keys]
        except (ValueError, TypeError):
            return False
        if keys != ["name", "value"]:
            return False
        try:
            configuration_names.append(ast.literal_eval(item.values[0]))
        except (ValueError, TypeError):
            return False
        if not isinstance(item.values[1], ast.Name):
            return False
        configuration_value_names.append(item.values[1].id)
    if tuple(configuration_names) != EXPECTED_CONFIG_NAMES:
        return False
    if configuration_value_names != ["results_dir", "export_root", "adapter_id"]:
        return False
    canonical = canonical_values[0]
    canonical_keys: list[str] = []
    canonical_map: dict[str, ast.AST] = {}
    for key_node, value_node in zip(canonical.keys, canonical.values):
        if not isinstance(key_node, ast.Constant) or not isinstance(key_node.value, str):
            return False
        canonical_keys.append(key_node.value)
        canonical_map[key_node.value] = value_node
    if tuple(canonical_keys) != (
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
    ):
        return False
    if not (
        isinstance(canonical_map["salt_hex"], ast.Name)
        and canonical_map["salt_hex"].id == "salt_hex"
        and isinstance(canonical_map["configuration_values"], ast.Name)
        and canonical_map["configuration_values"].id == "configuration_values"
        and _compact_json_encode(byte_values[0], aliases, "canonical_object")
        and _sha256_hexdigest(digest_values[0], aliases, "canonical_bytes")
    ):
        return False
    comparisons = _calls(function, aliases, "hmac.compare_digest")
    if len(comparisons) != 1 or len(comparisons[0].args) != 2:
        return False
    if not (
        isinstance(comparisons[0].args[0], ast.Name)
        and comparisons[0].args[0].id == "recomputed_binding"
        and _subscript(
            comparisons[0].args[1],
            "receipt",
            "combined_binding_sha256",
        )
    ):
        return False
    forbidden_mutation = False
    for node in ast.walk(function):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Subscript) and _target_name(target.value) in {
                    "canonical_object",
                    "configuration_values",
                }:
                    forbidden_mutation = True
        if isinstance(node, ast.Call):
            target = _expr_name(node.func, aliases)
            if target in {
                "canonical_object.update",
                "canonical_object.setdefault",
                "configuration_values.append",
                "configuration_values.extend",
            }:
                forbidden_mutation = True
    return not forbidden_mutation


def _check_no_random_or_weak_hash(context: dict[str, object]) -> bool:
    tree = context["tree"]
    aliases = context["aliases"]
    imported_modules = context["imported_modules"]
    if not (
        isinstance(tree, ast.Module)
        and isinstance(aliases, dict)
        and isinstance(imported_modules, list)
    ):
        return False
    roots = {name.split(".")[0] for name in imported_modules if name}
    if roots & {"random", "secrets", "uuid"}:
        return False
    forbidden = {
        "os.urandom",
        "hashlib.md5",
        "hashlib.sha1",
        "random.randbytes",
        "secrets.token_bytes",
        "secrets.token_hex",
    }
    return not any(
        _expr_name(call.func, aliases) in forbidden for call in _calls(tree, aliases)
    )


def _literal_call_arguments(
    function: ast.FunctionDef | ast.AsyncFunctionDef | None,
    aliases: dict[str, str],
    call_name: str,
) -> tuple[str, ...] | None:
    if function is None:
        return None
    values: list[str] = []
    for call in _calls(function, aliases, call_name):
        if not (
            call.args
            and isinstance(call.args[0], ast.Constant)
            and isinstance(call.args[0].value, str)
        ):
            return None
        values.append(call.args[0].value)
    return tuple(values)


def _check_gate_prestate_order(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    return (
        _literal_call_arguments(
            functions.get("execute_once"),
            aliases,
            "capture_gate_prestate",
        )
        == EXPECTED_GATE_NAMES
    )


def _check_gate_write_order(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    return (
        _literal_call_arguments(functions.get("execute_once"), aliases, "set_gate")
        == EXPECTED_GATE_NAMES
    )


def _check_gate_restore(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    restore = functions.get("restore_gate_states")
    execution = functions.get("execute_once")
    outer = _outer_try(execution)
    if restore is None or outer is None:
        return False
    reversed_calls = _calls(restore, aliases, "reversed")
    if not (
        len(reversed_calls) == 1
        and len(reversed_calls[0].args) == 1
        and isinstance(reversed_calls[0].args[0], ast.Name)
        and reversed_calls[0].args[0].id == "gate_states"
    ):
        return False
    final_tree = _module_for_body(outer.finalbody)
    calls = _calls(final_tree, aliases, "restore_gate_states")
    return (
        len(calls) == 1
        and len(calls[0].args) == 1
        and isinstance(calls[0].args[0], ast.Name)
        and calls[0].args[0].id == "gate_states"
    )


def _dotenv_assignments(node: ast.AST) -> list[ast.Assign]:
    result: list[ast.Assign] = []
    for candidate in ast.walk(node):
        if not isinstance(candidate, ast.Assign):
            continue
        if any(_target_name(target) == "dotenv.load_dotenv" for target in candidate.targets):
            result.append(candidate)
    return sorted(result, key=lambda candidate: candidate.lineno)


def _app_import_calls(
    node: ast.AST,
    aliases: dict[str, str],
) -> list[ast.Call]:
    result: list[ast.Call] = []
    for call in _calls(node, aliases, "importlib.import_module"):
        if (
            len(call.args) == 1
            and isinstance(call.args[0], ast.Constant)
            and call.args[0].value == "app.main"
        ):
            result.append(call)
    return result


def _check_dotenv_patch_before_import(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    outer = _outer_try(functions.get("execute_once"))
    if outer is None:
        return False
    body_tree = _module_for_body(outer.body)
    patches = _dotenv_assignments(body_tree)
    imports = _app_import_calls(body_tree, aliases)
    return (
        len(patches) == 1
        and len(imports) >= 1
        and isinstance(patches[0].value, ast.Name)
        and patches[0].value.id == "_dotenv_noop"
        and patches[0].lineno < min(call.lineno for call in imports)
    )


def _check_dotenv_restore(context: dict[str, object]) -> bool:
    functions = context["functions"]
    if not isinstance(functions, dict):
        return False
    outer = _outer_try(functions.get("execute_once"))
    if outer is None:
        return False
    restores = _dotenv_assignments(_module_for_body(outer.finalbody))
    return (
        len(restores) == 1
        and isinstance(restores[0].value, ast.Name)
        and restores[0].value.id == "original_dotenv_callable"
    )


def _check_app_import_once(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    execution = functions.get("execute_once")
    return execution is not None and len(_app_import_calls(execution, aliases)) == 1


def _check_event_loop_once_after_import(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    execution = functions.get("execute_once")
    if execution is None:
        return False
    imports = _app_import_calls(execution, aliases)
    loops = _calls(execution, aliases, "asyncio.new_event_loop")
    return (
        len(imports) >= 1
        and len(loops) == 1
        and loops[0].lineno > max(call.lineno for call in imports)
    )


def _check_no_asyncio_run(context: dict[str, object]) -> bool:
    tree = context["tree"]
    aliases = context["aliases"]
    return (
        isinstance(tree, ast.Module)
        and isinstance(aliases, dict)
        and not _calls(tree, aliases, "asyncio.run")
    )


def _check_asgi_transport_once(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    perform = functions.get("_perform_get")
    if perform is None:
        return False
    calls = [
        call
        for call in _calls(perform, aliases)
        if _expr_name(call.func, aliases).endswith(".ASGITransport")
    ]
    return len(calls) == 1


def _check_target_route(context: dict[str, object]) -> bool:
    tree = context["tree"]
    return isinstance(tree, ast.Module) and (
        _literal_assignment(tree, "TARGET_ROUTE") == EXPECTED_TARGET_ROUTE
    )


def _check_http_get_once(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    perform = functions.get("_perform_get")
    if not isinstance(perform, ast.AsyncFunctionDef):
        return False
    awaited_gets: list[ast.Call] = []
    for node in ast.walk(perform):
        if (
            isinstance(node, ast.Await)
            and isinstance(node.value, ast.Call)
            and _expr_name(node.value.func, aliases) == "client.get"
        ):
            awaited_gets.append(node.value)
    other_methods = [
        call
        for call in _calls(perform, aliases)
        if _expr_name(call.func, aliases)
        in {"client.post", "client.put", "client.patch", "client.delete"}
    ]
    return (
        len(awaited_gets) == 1
        and len(awaited_gets[0].args) == 1
        and isinstance(awaited_gets[0].args[0], ast.Name)
        and awaited_gets[0].args[0].id == "TARGET_ROUTE"
        and not other_methods
    )


def _parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }


def _check_perform_get_called_once(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    execution = functions.get("execute_once")
    if execution is None:
        return False
    invocations = _calls(execution, aliases, "_perform_get")
    loop_consumers = _calls(execution, aliases, "loop.run_until_complete")
    if len(invocations) != 1 or len(loop_consumers) != 1:
        return False
    parents = _parent_map(execution)
    return (
        parents.get(invocations[0]) is loop_consumers[0]
        and len(loop_consumers[0].args) == 1
        and loop_consumers[0].args[0] is invocations[0]
    )


def _tuple_payload_keys(node: ast.AST, aliases: dict[str, str]) -> bool:
    return (
        isinstance(node, ast.Call)
        and _expr_name(node.func, aliases) == "tuple"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Call)
        and _expr_name(node.args[0].func, aliases) == "payload.keys"
        and not node.args[0].args
    )


def _len_payload(node: ast.AST, aliases: dict[str, str]) -> bool:
    return (
        isinstance(node, ast.Call)
        and _expr_name(node.func, aliases) == "len"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "payload"
    )


def _check_response_order(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    function = functions.get("validate_response")
    if function is None:
        return False
    order_compare = False
    count_compare = False
    for node in ast.walk(function):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1:
            continue
        if (
            _tuple_payload_keys(node.left, aliases)
            and isinstance(node.ops[0], ast.NotEq)
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Name)
            and node.comparators[0].id == "projection_fields"
        ):
            order_compare = True
        if (
            _len_payload(node.left, aliases)
            and isinstance(node.ops[0], ast.NotEq)
            and len(node.comparators) == 1
            and isinstance(node.comparators[0], ast.Constant)
            and node.comparators[0].value == 52
        ):
            count_compare = True
    return order_compare and count_compare


def _check_response_bounded_hash(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    function = functions.get("validate_response")
    if function is None:
        return False
    payload_values = _assignment_values(function, "payload")
    byte_values = _assignment_values(function, "response_bytes")
    hash_values = _assignment_values(function, "response_sha256")
    summary_values = _assignment_values(function, "summary")
    if not (
        len(payload_values) == 1
        and isinstance(payload_values[0], ast.Call)
        and _expr_name(payload_values[0].func, aliases) == "response.json"
        and len(byte_values) == 1
        and _compact_json_encode(byte_values[0], aliases, "payload")
        and len(hash_values) == 1
        and _sha256_hexdigest(hash_values[0], aliases, "response_bytes")
        and len(summary_values) == 1
        and isinstance(summary_values[0], ast.Dict)
    ):
        return False
    summary = summary_values[0]
    try:
        keys = tuple(ast.literal_eval(key) for key in summary.keys)
    except (ValueError, TypeError):
        return False
    if keys != (
        "http_status",
        "field_count",
        "field_order_exact",
        "response_bytes",
        "response_sha256",
    ):
        return False
    if len(summary.values) != 5:
        return False
    http_status, field_count, field_order_exact, response_size, response_hash = (
        summary.values
    )
    if not (
        isinstance(http_status, ast.Attribute)
        and isinstance(http_status.value, ast.Name)
        and http_status.value.id == "response"
        and http_status.attr == "status_code"
        and isinstance(field_count, ast.Call)
        and _expr_name(field_count.func, aliases) == "len"
        and len(field_count.args) == 1
        and isinstance(field_count.args[0], ast.Name)
        and field_count.args[0].id == "payload"
        and isinstance(field_order_exact, ast.Constant)
        and field_order_exact.value is True
        and isinstance(response_size, ast.Call)
        and _expr_name(response_size.func, aliases) == "len"
        and len(response_size.args) == 1
        and isinstance(response_size.args[0], ast.Name)
        and response_size.args[0].id == "response_bytes"
        and isinstance(response_hash, ast.Name)
        and response_hash.id == "response_sha256"
    ):
        return False
    returns = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Return)
        and isinstance(node.value, ast.Name)
        and node.value.id == "summary"
    ]
    return len(returns) == 1


def _check_file_guard_boundary(context: dict[str, object]) -> bool:
    tree = context["tree"]
    functions = context["functions"]
    aliases = context["aliases"]
    if not (
        isinstance(tree, ast.Module)
        and isinstance(functions, dict)
        and isinstance(aliases, dict)
    ):
        return False
    if not (
        _literal_assignment(tree, "SAFE_METADATA_BASENAMES")
        == EXPECTED_SAFE_METADATA_BASENAMES
        and _literal_assignment(tree, "RAW_ROW_BASENAMES")
        == EXPECTED_RAW_ROW_BASENAMES
    ):
        return False
    guard = functions.get("install_file_guards")
    execution = functions.get("execute_once")
    if guard is None or execution is None:
        return False
    assigned: set[str] = set()
    for node in ast.walk(guard):
        if isinstance(node, ast.Assign):
            assigned.update(_target_name(target) for target in node.targets)
    required_assignments = {
        "builtins.open",
        "io.open",
        "os.listdir",
        "os.scandir",
        "os.walk",
        "Path.iterdir",
        "Path.glob",
        "Path.rglob",
    }
    return (
        required_assignments <= assigned
        and len(_calls(execution, aliases, "install_file_guards")) == 1
    )


def _check_raw_row_fail_closed(context: dict[str, object]) -> bool:
    tree = context["tree"]
    aliases = context["aliases"]
    if not isinstance(tree, ast.Module) or not isinstance(aliases, dict):
        return False
    raw_names = set(EXPECTED_RAW_ROW_BASENAMES)
    content_targets = {
        "open",
        "builtins.open",
        "io.open",
        "Path.read_text",
        "Path.read_bytes",
    }
    for call in _calls(tree, aliases):
        target = _expr_name(call.func, aliases)
        if target not in content_targets:
            continue
        literal_values = {
            node.value
            for node in ast.walk(call)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        if literal_values & raw_names:
            return False
    return True


def _check_no_directory_discovery(context: dict[str, object]) -> bool:
    tree = context["tree"]
    aliases = context["aliases"]
    if not isinstance(tree, ast.Module) or not isinstance(aliases, dict):
        return False
    forbidden = {
        "os.listdir",
        "os.scandir",
        "os.walk",
        "glob.glob",
        "glob.iglob",
        "Path.iterdir",
        "Path.glob",
        "Path.rglob",
    }
    return not any(
        _expr_name(call.func, aliases) in forbidden for call in _calls(tree, aliases)
    )


def _check_network_guard(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    if not isinstance(functions, dict) or not isinstance(aliases, dict):
        return False
    execution = functions.get("execute_once")
    guard = functions.get("install_network_guards")
    if execution is None or guard is None:
        return False
    imports = _app_import_calls(execution, aliases)
    loops = _calls(execution, aliases, "asyncio.new_event_loop")
    installs = _calls(execution, aliases, "install_network_guards")
    runs = _calls(execution, aliases, "loop.run_until_complete")
    if not (
        imports
        and loops
        and len(installs) == 1
        and runs
        and max(call.lineno for call in imports)
        < min(call.lineno for call in loops)
        and max(call.lineno for call in loops) < installs[0].lineno
        and installs[0].lineno < min(call.lineno for call in runs)
    ):
        return False
    if len(_calls(guard, aliases, "sys.addaudithook")) != 1:
        return False
    forbidden_targets = {
        "socket.socket",
        "socket.SocketType",
        "socket.socket.connect",
        "socket.socket.bind",
        "socket.socket.listen",
        "socket.socket.accept",
    }
    for node in ast.walk(guard):
        if not isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(_target_name(target) in forbidden_targets for target in targets):
            return False
    return True


def _check_no_external_or_mutating_actions(context: dict[str, object]) -> bool:
    tree = context["tree"]
    aliases = context["aliases"]
    if not isinstance(tree, ast.Module) or not isinstance(aliases, dict):
        return False
    forbidden_exact = {
        "eval",
        "exec",
        "compile",
        "__import__",
        "socket.create_connection",
        "socket.getaddrinfo",
        "subprocess.Popen",
        "subprocess.run",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
        "os.system",
        "os.popen",
    }
    forbidden_suffixes = (
        ".post",
        ".put",
        ".patch",
        ".delete",
        ".commit",
        ".execute",
        ".executemany",
        ".insert_one",
        ".insert_many",
        ".update_one",
        ".update_many",
    )
    forbidden_fragments = (
        "uvicorn",
        "playwright",
        "selenium",
        "openai",
        "anthropic",
        "collector.run",
        "provider.run",
        "git.",
        "project_source",
    )
    for call in _calls(tree, aliases):
        target = _expr_name(call.func, aliases)
        lowered = target.lower()
        if target in forbidden_exact or target.endswith(forbidden_suffixes):
            return False
        if any(fragment in lowered for fragment in forbidden_fragments):
            return False
    return True


def _check_atomic_result_and_output(context: dict[str, object]) -> bool:
    functions = context["functions"]
    aliases = context["aliases"]
    tree = context["tree"]
    if not (
        isinstance(functions, dict)
        and isinstance(aliases, dict)
        and isinstance(tree, ast.Module)
    ):
        return False
    publisher = functions.get("publish_safe_result")
    execution = functions.get("execute_once")
    emitter = functions.get("emit_result")
    outer = _outer_try(execution)
    if publisher is None or execution is None or emitter is None or outer is None:
        return False
    names = [_expr_name(call.func, aliases) for call in _calls(publisher, aliases)]
    if not (
        names.count("os.open") == 1
        and names.count("os.write") == 1
        and names.count("os.fsync") == 1
        and names.count("os.close") == 1
        and names.count("os.replace") == 1
        and any(isinstance(node, ast.While) for node in ast.walk(publisher))
    ):
        return False
    open_call = _calls(publisher, aliases, "os.open")[0]
    open_dump = ast.dump(open_call, include_attributes=False)
    if not all(flag in open_dump for flag in ("O_WRONLY", "O_CREAT", "O_EXCL")):
        return False
    close_in_finally = False
    for node in ast.walk(publisher):
        if not isinstance(node, ast.Try) or not node.finalbody:
            continue
        final_calls = _calls(_module_for_body(node.finalbody), aliases, "os.close")
        if len(final_calls) == 1:
            close_in_finally = True
    if not close_in_finally:
        return False
    final_calls = _calls(
        _module_for_body(outer.finalbody),
        aliases,
        "publish_safe_result",
    )
    if len(final_calls) != 1:
        return False
    output_calls = [
        call
        for call in _calls(tree, aliases)
        if _expr_name(call.func, aliases) in {"sys.stdout.write", "print"}
    ]
    if len(output_calls) != 1 or _expr_name(output_calls[0].func, aliases) != "sys.stdout.write":
        return False
    protected_names = {
        "payload",
        "receipt",
        "salt_hex",
        "configuration_values",
        "response",
        "response_bytes",
        "canonical_bytes",
    }
    if any(
        isinstance(node, ast.Name) and node.id in protected_names
        for node in ast.walk(output_calls[0])
    ):
        return False
    emitter_calls = _calls(tree, aliases, "emit_result")
    return len(emitter_calls) == 1


CHECK_FUNCTIONS = {
    "IMPORT_ALLOWLIST": _check_import_allowlist,
    "BOUND_CONSTANTS": _check_bound_constants,
    "RECEIPT_SINGLE_READ": _check_receipt_single_read,
    "CONFIG_EXACT_THREE_READS": _check_config_exact_three_reads,
    "CIB_DATAFLOW": _check_cib_dataflow,
    "NO_RANDOM_OR_WEAK_HASH": _check_no_random_or_weak_hash,
    "GATE_PRESTATE_EXACT_ORDER": _check_gate_prestate_order,
    "GATE_WRITE_EXACT_ORDER": _check_gate_write_order,
    "GATE_RESTORE_REVERSED_OUTER_FINALLY": _check_gate_restore,
    "DOTENV_PATCH_BEFORE_APP_IMPORT": _check_dotenv_patch_before_import,
    "DOTENV_RESTORE_OUTER_FINALLY": _check_dotenv_restore,
    "APP_IMPORT_EXACTLY_ONCE": _check_app_import_once,
    "EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT": _check_event_loop_once_after_import,
    "NO_ASYNCIO_RUN": _check_no_asyncio_run,
    "ASGI_TRANSPORT_EXACTLY_ONCE": _check_asgi_transport_once,
    "TARGET_ROUTE_EXACT": _check_target_route,
    "HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET": _check_http_get_once,
    "PERFORM_GET_CALLED_EXACTLY_ONCE": _check_perform_get_called_once,
    "RESPONSE_EXACT_52_FIELD_ORDER": _check_response_order,
    "RESPONSE_BOUNDED_HASH_ONLY": _check_response_bounded_hash,
    "FILE_GUARD_BOUNDARY": _check_file_guard_boundary,
    "RAW_ROW_PRIVACY_FAIL_CLOSED": _check_raw_row_fail_closed,
    "NO_DIRECTORY_DISCOVERY": _check_no_directory_discovery,
    "NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED": _check_network_guard,
    "NO_EXTERNAL_OR_MUTATING_ACTIONS": _check_no_external_or_mutating_actions,
    "ATOMIC_SAFE_RESULT_AND_OUTPUT": _check_atomic_result_and_output,
}


def _audit_runner_bytes(runner_bytes: bytes) -> tuple[dict[str, bool], str | None]:
    checks = {name: False for name in CHECK_NAMES}
    strict_utf8_no_bom = not runner_bytes.startswith(b"\xef\xbb\xbf")
    try:
        source = runner_bytes.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return checks, None
    checks["STRICT_UTF8_NO_BOM"] = strict_utf8_no_bom
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return checks, source
    checks["AST_PARSE"] = True
    aliases, imported_modules = _build_aliases_and_imports(tree)
    context: dict[str, object] = {
        "tree": tree,
        "source": source,
        "aliases": aliases,
        "imported_modules": imported_modules,
        "functions": _functions(tree),
    }
    for name in CHECK_NAMES[2:]:
        check = CHECK_FUNCTIONS[name]
        try:
            checks[name] = bool(check(context))
        except (AttributeError, KeyError, TypeError, ValueError):
            checks[name] = False
    return checks, source


VALID_PUBLIC_RUNNER = '''
from __future__ import annotations

import asyncio
import builtins
import glob
import hashlib
import hmac
import importlib
import io
import json
import os
import re
import socket
import subprocess
import sys
from pathlib import Path

import dotenv

RUNNER_BASENAME = ".sentigraph_b05_get_smoke_runner_v2.py"
RECEIPT_BASENAME = ".sentigraph_cib_capture_risk_prompt_3_v1_safe_receipt.json"
RESULT_BASENAME = ".sentigraph_b05_get_smoke_result_v2.json"
PARTIAL_BASENAME = ".sentigraph_b05_get_smoke_result_v2.json.partial"
RESULT_BASENAME_APPROVED = "provider_result_helldivers2-psn-demo_20260720_123627.json"
TARGET_ROUTE = "/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo"  # FIXTURE_ANCHOR_TARGET_ROUTE
CONFIG_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)
GATE_NAMES = (
    "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
)
SAFE_METADATA_BASENAMES = (
    "manifest.json",
    "validation_report.json",
    "validation_report.md",
    "coverage_note.md",
    "README.md",
    "package_index.json",
)
RAW_ROW_BASENAMES = (
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "collection_log.jsonl",
)


def read_receipt_once(receipt_path):
    with builtins.open(receipt_path, "rb") as stream:
        receipt_bytes = stream.read()
    return receipt_bytes


def read_configuration_values():
    results_dir = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR")
    export_root = os.environ.get("SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT")
    adapter_id = os.environ.get("SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID")
    return results_dir, export_root, adapter_id


def verify_cib(receipt, values):
    results_dir, export_root, adapter_id = values
    configuration_values = [
        {"name": "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR", "value": results_dir},
        {"name": "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT", "value": export_root},
        {"name": "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID", "value": adapter_id},
    ]
    salt_hex = receipt["salt_hex"]
    canonical_object = {
        "schema": "public_dummy_cib_schema",
        "version": "0.1",
        "binding_scope": "public_dummy_binding_scope",
        "service_blob": "public_dummy_service_blob",
        "registry_schema": "public_dummy_registry_schema",
        "sample_handle": "helldivers2-psn-demo",
        "result_file_name": "provider_result_helldivers2-psn-demo_20260720_123627.json",
        "route_mode": "public_dummy_route_mode",
        "capability_label": "public_dummy_capability_label",
        "salt_hex": salt_hex,
        "configuration_values": configuration_values,
    }
    canonical_bytes = json.dumps(
        canonical_object,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    ).encode("utf-8")
    recomputed_binding = hashlib.sha256(canonical_bytes).hexdigest()
    if not hmac.compare_digest(recomputed_binding, receipt["combined_binding_sha256"]):  # FIXTURE_ANCHOR_CIB_COMPARE
        raise ValueError("public_cib_mismatch")
    return True


def capture_gate_prestate(name):
    value = os.environ.get(name)
    return value


def set_gate(name):
    os.environ[name] = "1"


def restore_gate_states(gate_states):
    for name, value in reversed(gate_states):
        if value is None:
            del os.environ[name]
        else:
            os.environ[name] = value


def guarded_open(*args, **kwargs):
    raise RuntimeError("public_file_guard")


def block_directory_operation(*args, **kwargs):
    raise RuntimeError("public_directory_guard")


def install_file_guards():
    originals = {
        "builtins_open": builtins.open,
        "io_open": io.open,
        "os_listdir": os.listdir,
        "os_scandir": os.scandir,
        "os_walk": os.walk,
        "path_iterdir": Path.iterdir,
        "path_glob": Path.glob,
        "path_rglob": Path.rglob,
    }
    builtins.open = guarded_open
    io.open = guarded_open
    os.listdir = block_directory_operation
    os.scandir = block_directory_operation
    os.walk = block_directory_operation
    Path.iterdir = block_directory_operation
    Path.glob = block_directory_operation
    Path.rglob = block_directory_operation
    return originals


def block_network(*args, **kwargs):
    raise RuntimeError("public_network_guard")


def block_subprocess(*args, **kwargs):
    raise RuntimeError("public_subprocess_guard")


def install_network_guards(loop):
    socket_type_before = socket.socket
    socket_alias_before = socket.SocketType
    state = {"armed": True}

    def audit_hook(event, args):
        if state["armed"] and event == "socket.__new__":
            raise RuntimeError("public_network_guard")

    sys.addaudithook(audit_hook)
    originals = {
        "socket_create_connection": socket.create_connection,
        "socket_getaddrinfo": socket.getaddrinfo,
        "subprocess_popen": subprocess.Popen,
    }
    socket.create_connection = block_network
    socket.getaddrinfo = block_network
    subprocess.Popen = block_subprocess
    # FIXTURE_ANCHOR_SOCKET_TYPE_REPLACED
    type_identity_preserved = (
        socket.socket is socket_type_before and socket.SocketType is socket_alias_before
    )
    return originals, state, type_identity_preserved


def restore_file_guards(originals):
    builtins.open = originals["builtins_open"]
    io.open = originals["io_open"]
    os.listdir = originals["os_listdir"]
    os.scandir = originals["os_scandir"]
    os.walk = originals["os_walk"]
    Path.iterdir = originals["path_iterdir"]
    Path.glob = originals["path_glob"]
    Path.rglob = originals["path_rglob"]


def restore_network_guards(originals, state):
    state["armed"] = False
    socket.create_connection = originals["socket_create_connection"]
    socket.getaddrinfo = originals["socket_getaddrinfo"]
    subprocess.Popen = originals["subprocess_popen"]


async def _perform_get(httpx_module, app):
    transport = httpx_module.ASGITransport(app=app)  # FIXTURE_ANCHOR_ASGI_TRANSPORT
    async with httpx_module.AsyncClient(
        transport=transport,
        base_url="http://public.invalid",
    ) as client:
        response = await client.get(TARGET_ROUTE)
        # FIXTURE_ANCHOR_SECOND_HTTP_GET
        return response


def validate_response(response, projection_fields):
    payload = response.json()
    if tuple(payload.keys()) != projection_fields or len(payload) != 52:  # FIXTURE_ANCHOR_RESPONSE_ORDER
        raise ValueError("public_response_contract")
    response_bytes = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    ).encode("utf-8")
    response_sha256 = hashlib.sha256(response_bytes).hexdigest()
    # FIXTURE_ANCHOR_PAYLOAD_OUTPUT
    summary = {
        "http_status": response.status_code,
        "field_count": len(payload),
        "field_order_exact": True,
        "response_bytes": len(response_bytes),
        "response_sha256": response_sha256,
    }
    return summary


def publish_safe_result(result, result_path, partial_path):
    result_bytes = json.dumps(
        result,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=False,
    ).encode("utf-8")
    descriptor = os.open(
        partial_path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        offset = 0
        while offset < len(result_bytes):
            offset += os.write(descriptor, result_bytes[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.replace(partial_path, result_path)  # FIXTURE_ANCHOR_ATOMIC_REPLACE


def _dotenv_noop(*args, **kwargs):
    return False


def execute_once(httpx_module, receipt_path, result_path, partial_path, projection_fields):
    original_dotenv_callable = dotenv.load_dotenv
    gate_states = [
        ("SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED", capture_gate_prestate("SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED")),
        ("SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED", capture_gate_prestate("SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED")),
        ("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED", capture_gate_prestate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED")),
        ("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED", capture_gate_prestate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED")),
        ("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED", capture_gate_prestate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED")),
    ]
    safe_result = {"schema": "public_bounded_safe_result"}
    loop = None
    network_originals = None
    network_state = None
    file_originals = None
    try:
        receipt_bytes = read_receipt_once(receipt_path)
        configuration_values = read_configuration_values()
        receipt = json.loads(receipt_bytes.decode("utf-8"))
        verify_cib(receipt, configuration_values)
        set_gate("SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED")
        set_gate("SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED")
        set_gate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED")
        set_gate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED")
        set_gate("SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED")
        dotenv.load_dotenv = _dotenv_noop  # FIXTURE_ANCHOR_DOTENV_PATCH_ORDER
        app_module = importlib.import_module("app.main")
        # FIXTURE_ANCHOR_SECOND_APP_IMPORT
        loop = asyncio.new_event_loop()
        # FIXTURE_ANCHOR_SECOND_EVENT_LOOP
        network_originals, network_state, type_identity = install_network_guards(loop)
        file_originals = install_file_guards()
        # FIXTURE_ANCHOR_RAW_ROW_READ
        # FIXTURE_ANCHOR_EXTERNAL_SOCKET_ACTION
        response = loop.run_until_complete(
            _perform_get(httpx_module, app_module.app)
        )
        # FIXTURE_ANCHOR_PERFORM_GET_CALLED_TWICE
        safe_result = validate_response(response, projection_fields)
        return safe_result
    finally:
        if network_originals is not None:
            restore_network_guards(network_originals, network_state)
        if file_originals is not None:
            restore_file_guards(file_originals)
        if loop is not None:
            loop.close()
        dotenv.load_dotenv = original_dotenv_callable  # FIXTURE_ANCHOR_DOTENV_RESTORE
        restore_gate_states(gate_states)  # FIXTURE_ANCHOR_GATE_RESTORE
        publish_safe_result(safe_result, result_path, partial_path)


def dormant_public_markers():
    # FIXTURE_ANCHOR_ASYNCIO_RUN
    # FIXTURE_ANCHOR_DIRECTORY_DISCOVERY
    return None


def emit_result(result):
    sys.stdout.write(
        json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        + "\\n"
    )


def main():
    bounded_result = {"schema": "public_terminal_result", "status": "bounded"}
    emit_result(bounded_result)
    return 0
'''


NEGATIVE_SPECS = (
    (
        "second_http_get",
        "HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET",
        "        # FIXTURE_ANCHOR_SECOND_HTTP_GET",
        "        response_second = await client.get(TARGET_ROUTE)",
    ),
    (
        "perform_get_called_twice",
        "PERFORM_GET_CALLED_EXACTLY_ONCE",
        "        # FIXTURE_ANCHOR_PERFORM_GET_CALLED_TWICE",
        "        response_second = loop.run_until_complete(\n"
        "            _perform_get(httpx_module, app_module.app)\n"
        "        )",
    ),
    (
        "gate_restore_removed",
        "GATE_RESTORE_REVERSED_OUTER_FINALLY",
        "        restore_gate_states(gate_states)  # FIXTURE_ANCHOR_GATE_RESTORE",
        "        pass  # NEGATIVE_GATE_RESTORE_REMOVED",
    ),
    (
        "dotenv_patch_after_import",
        "DOTENV_PATCH_BEFORE_APP_IMPORT",
        "        dotenv.load_dotenv = _dotenv_noop  # FIXTURE_ANCHOR_DOTENV_PATCH_ORDER\n"
        '        app_module = importlib.import_module("app.main")',
        '        app_module = importlib.import_module("app.main")\n'
        "        dotenv.load_dotenv = _dotenv_noop  # NEGATIVE_DOTENV_PATCH_AFTER_IMPORT",
    ),
    (
        "dotenv_restore_removed",
        "DOTENV_RESTORE_OUTER_FINALLY",
        "        dotenv.load_dotenv = original_dotenv_callable  # FIXTURE_ANCHOR_DOTENV_RESTORE",
        "        pass  # NEGATIVE_DOTENV_RESTORE_REMOVED",
    ),
    (
        "forged_cib_digest",
        "CIB_DATAFLOW",
        '    if not hmac.compare_digest(recomputed_binding, receipt["combined_binding_sha256"]):  # FIXTURE_ANCHOR_CIB_COMPARE',
        '    if not hmac.compare_digest("public_forged_digest", receipt["combined_binding_sha256"]):  # NEGATIVE_FORGED_CIB_DIGEST',
    ),
    (
        "response_order_removed",
        "RESPONSE_EXACT_52_FIELD_ORDER",
        "    if tuple(payload.keys()) != projection_fields or len(payload) != 52:  # FIXTURE_ANCHOR_RESPONSE_ORDER",
        "    if len(payload) != 52:  # NEGATIVE_RESPONSE_ORDER_REMOVED",
    ),
    (
        "raw_row_read",
        "RAW_ROW_PRIVACY_FAIL_CLOSED",
        "        # FIXTURE_ANCHOR_RAW_ROW_READ",
        '        raw_probe = builtins.open("evidence_items.jsonl", "rb").read()',
    ),
    (
        "external_socket_action",
        "NO_EXTERNAL_OR_MUTATING_ACTIONS",
        "        # FIXTURE_ANCHOR_EXTERNAL_SOCKET_ACTION",
        '        socket.create_connection(("public.invalid", 443))',
    ),
    (
        "payload_output",
        "ATOMIC_SAFE_RESULT_AND_OUTPUT",
        "    # FIXTURE_ANCHOR_PAYLOAD_OUTPUT",
        "    sys.stdout.write(str(payload))",
    ),
    (
        "asyncio_run_added",
        "NO_ASYNCIO_RUN",
        "    # FIXTURE_ANCHOR_ASYNCIO_RUN",
        "    asyncio.run(public_coroutine())",
    ),
    (
        "second_app_import",
        "APP_IMPORT_EXACTLY_ONCE",
        "        # FIXTURE_ANCHOR_SECOND_APP_IMPORT",
        '        second_app_module = importlib.import_module("app.main")',
    ),
    (
        "second_event_loop",
        "EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT",
        "        # FIXTURE_ANCHOR_SECOND_EVENT_LOOP",
        "        second_loop = asyncio.new_event_loop()",
    ),
    (
        "asgi_transport_removed",
        "ASGI_TRANSPORT_EXACTLY_ONCE",
        "    transport = httpx_module.ASGITransport(app=app)  # FIXTURE_ANCHOR_ASGI_TRANSPORT",
        "    transport = object()  # NEGATIVE_ASGI_TRANSPORT_REMOVED",
    ),
    (
        "target_route_changed",
        "TARGET_ROUTE_EXACT",
        'TARGET_ROUTE = "/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo"  # FIXTURE_ANCHOR_TARGET_ROUTE',
        'TARGET_ROUTE = "/public/negative/alternate"  # NEGATIVE_TARGET_ROUTE_CHANGED',
    ),
    (
        "directory_discovery_added",
        "NO_DIRECTORY_DISCOVERY",
        "    # FIXTURE_ANCHOR_DIRECTORY_DISCOVERY",
        '    os.listdir(".")',
    ),
    (
        "socket_type_replaced",
        "NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED",
        "    # FIXTURE_ANCHOR_SOCKET_TYPE_REPLACED",
        "    socket.socket = block_network  # NEGATIVE_SOCKET_TYPE_REPLACED",
    ),
    (
        "atomic_replace_removed",
        "ATOMIC_SAFE_RESULT_AND_OUTPUT",
        "    os.replace(partial_path, result_path)  # FIXTURE_ANCHOR_ATOMIC_REPLACE",
        "    pass  # NEGATIVE_ATOMIC_REPLACE_REMOVED",
    ),
)


def _replace_unique(source: str, anchor: str, replacement: str) -> str:
    if source.count(anchor) != 1:
        raise ValueError("fixture_anchor_count")
    replaced = source.replace(anchor, replacement, 1)
    if anchor in replaced:
        raise ValueError("fixture_anchor_retained")
    try:
        ast.parse(replaced)
    except SyntaxError as exc:
        raise ValueError("fixture_generation_error") from exc
    return replaced


def _self_test_failure(
    *,
    valid_accepted: int,
    negative_tested: int,
    negative_rejected: int,
    fixture_parse_failures: int,
    single_violation_matches: int,
    first_failure_fixture: str,
    first_failure_code: str,
) -> dict[str, object]:
    return {
        "schema": SELF_TEST_SCHEMA,
        "version": VERSION,
        "status": "fail",
        "checks_total": len(CHECK_NAMES),
        "valid_total": 1,
        "valid_accepted": valid_accepted,
        "negative_total": len(NEGATIVE_SPECS),
        "negative_tested": negative_tested,
        "negative_rejected": negative_rejected,
        "fixture_parse_failures": fixture_parse_failures,
        "single_violation_matches": single_violation_matches,
        "first_failure_fixture": first_failure_fixture,
        "first_failure_code": first_failure_code,
        "runner_execution": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }


def run_self_test() -> tuple[int, dict[str, object]]:
    valid_accepted = 0
    negative_tested = 0
    negative_rejected = 0
    fixture_parse_failures = 0
    single_violation_matches = 0
    try:
        ast.parse(VALID_PUBLIC_RUNNER)
    except SyntaxError:
        fixture_parse_failures = 1
        return 2, _self_test_failure(
            valid_accepted=valid_accepted,
            negative_tested=negative_tested,
            negative_rejected=negative_rejected,
            fixture_parse_failures=fixture_parse_failures,
            single_violation_matches=single_violation_matches,
            first_failure_fixture="valid_public_runner",
            first_failure_code="fixture_generation_error",
        )
    valid_checks, _ = _audit_runner_bytes(VALID_PUBLIC_RUNNER.encode("utf-8"))
    valid_failures = [name for name in CHECK_NAMES if not valid_checks[name]]
    if valid_failures:
        return 2, _self_test_failure(
            valid_accepted=valid_accepted,
            negative_tested=negative_tested,
            negative_rejected=negative_rejected,
            fixture_parse_failures=fixture_parse_failures,
            single_violation_matches=single_violation_matches,
            first_failure_fixture="valid_public_runner",
            first_failure_code=valid_failures[0],
        )
    valid_accepted = 1
    for fixture_name, expected_check, anchor, replacement in NEGATIVE_SPECS:
        negative_tested += 1
        try:
            negative_source = _replace_unique(
                VALID_PUBLIC_RUNNER,
                anchor,
                replacement,
            )
        except ValueError:
            fixture_parse_failures += 1
            return 2, _self_test_failure(
                valid_accepted=valid_accepted,
                negative_tested=negative_tested,
                negative_rejected=negative_rejected,
                fixture_parse_failures=fixture_parse_failures,
                single_violation_matches=single_violation_matches,
                first_failure_fixture=fixture_name,
                first_failure_code="fixture_generation_error",
            )
        negative_checks, _ = _audit_runner_bytes(negative_source.encode("utf-8"))
        failures = [name for name in CHECK_NAMES if not negative_checks[name]]
        if failures == [expected_check]:
            negative_rejected += 1
            single_violation_matches += 1
            continue
        failure_code = (
            "unexpected_accept"
            if not failures
            else "multiple_or_wrong_failed_checks"
        )
        return 2, _self_test_failure(
            valid_accepted=valid_accepted,
            negative_tested=negative_tested,
            negative_rejected=negative_rejected,
            fixture_parse_failures=fixture_parse_failures,
            single_violation_matches=single_violation_matches,
            first_failure_fixture=fixture_name,
            first_failure_code=failure_code,
        )
    result = {
        "schema": SELF_TEST_SCHEMA,
        "version": VERSION,
        "status": "pass",
        "checks_total": len(CHECK_NAMES),
        "valid_total": 1,
        "valid_accepted": valid_accepted,
        "negative_total": len(NEGATIVE_SPECS),
        "negative_tested": negative_tested,
        "negative_rejected": negative_rejected,
        "fixture_parse_failures": fixture_parse_failures,
        "single_violation_matches": single_violation_matches,
        "runner_execution": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }
    return 0, result


def _audit_result(runner_bytes: bytes, runner_reads: int) -> dict[str, object]:
    checks, _ = _audit_runner_bytes(runner_bytes)
    failed_checks = [name for name in CHECK_NAMES if not checks[name]]
    return {
        "schema": AUDITOR_SCHEMA,
        "version": VERSION,
        "status": "pass" if not failed_checks else "fail",
        "checks_total": len(CHECK_NAMES),
        "checks_passed": len(CHECK_NAMES) - len(failed_checks),
        "checks_failed": len(failed_checks),
        "failed_checks": failed_checks,
        "runner_bytes": len(runner_bytes),
        "runner_sha256": hashlib.sha256(runner_bytes).hexdigest(),
        "runner_reads": runner_reads,
        "runner_reopens": 0,
        "runner_executed": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }


def _path_guard_failure() -> dict[str, object]:
    return {
        "schema": AUDITOR_SCHEMA,
        "version": VERSION,
        "status": "fail",
        "checks_total": len(CHECK_NAMES),
        "checks_passed": 0,
        "checks_failed": len(CHECK_NAMES),
        "failed_checks": list(CHECK_NAMES),
        "runner_bytes": 0,
        "runner_sha256": hashlib.sha256(b"").hexdigest(),
        "runner_reads": 0,
        "runner_reopens": 0,
        "runner_executed": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }


def audit_runner(path_text: str) -> tuple[int, dict[str, object]]:
    runner_path = Path(path_text)
    if not (
        runner_path.is_absolute()
        and runner_path.name == RUNNER_BASENAME
        and runner_path.is_file()
        and not runner_path.is_symlink()
    ):
        return 2, _path_guard_failure()
    try:
        size = runner_path.stat().st_size
    except OSError:
        return 2, _path_guard_failure()
    if size < 1 or size > MAX_RUNNER_BYTES:
        return 2, _path_guard_failure()
    try:
        runner_bytes = runner_path.read_bytes()
    except OSError:
        return 2, _path_guard_failure()
    result = _audit_result(runner_bytes, 1)
    return (0 if result["status"] == "pass" else 2), result


def _bounded_internal_failure(self_test: bool) -> dict[str, object]:
    if self_test:
        return _self_test_failure(
            valid_accepted=0,
            negative_tested=0,
            negative_rejected=0,
            fixture_parse_failures=0,
            single_violation_matches=0,
            first_failure_fixture="bounded_internal",
            first_failure_code="bounded_internal_failure",
        )
    return _path_guard_failure()


def main() -> int:
    self_test_mode = sys.argv == [sys.argv[0], "--self-test"]
    try:
        if self_test_mode:
            exit_code, result = run_self_test()
        elif len(sys.argv) == 3 and sys.argv[1] == "--audit-runner":
            exit_code, result = audit_runner(sys.argv[2])
        else:
            exit_code, result = 2, _path_guard_failure()
    except BaseException:
        exit_code, result = 70, _bounded_internal_failure(self_test_mode)
    sys.stdout.write(
        json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=False)
        + "\n"
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
