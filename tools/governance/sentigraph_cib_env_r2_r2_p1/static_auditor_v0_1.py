import ast
import json
import sys

EXPECTED_SEARCH_ROOT = r"G:\AICODING"
EXPECTED_MAX_SEARCH_DEPTH = 12
EXPECTED_PROVIDER_RESULT_BASENAME = (
    "provider_result_helldivers2-psn-demo_20260614_055754.json"
)
EXPECTED_ENVIRONMENT_VARIABLE_NAMES = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)
EXPECTED_REGISTRY_SUBKEY = "Environment"
EXPECTED_HWND_BROADCAST = 0xFFFF
EXPECTED_WM_SETTINGCHANGE = 0x001A
EXPECTED_SMTO_ABORTIFHUNG = 0x0002
EXPECTED_ENVIRONMENT_BROADCAST_LPARAM = "Environment"
EXPECTED_BROADCAST_TIMEOUT_MS = 2000
EXPECTED_HELPER_OUTPUTS = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR=PASS",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT=PASS",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID=PASS",
    "CIB_ENV_R2_R2_P2=REPAIR_COMPLETED_PENDING_CODEX_RESTART",
    "CIB_ENV_R2_R2_P2=BLOCKED_SAFE_DISAMBIGUATION_OR_REPAIR",
    "WINDOWS_ENVIRONMENT_CHANGE_BROADCAST=PASS",
    "CIB_ENV_R2_R2_P2=BLOCKED_ENVIRONMENT_CHANGE_BROADCAST_AFTER_REGISTRY_REPAIR",
)
ALLOWED_HELPER_IMPORTS = {
    "ctypes",
    "json",
    "os",
    "re",
    "stat",
    "sys",
    "winreg",
}
FORBIDDEN_CALL_NAMES = {
    "compile",
    "eval",
    "exec",
    "__import__",
}
FORBIDDEN_NORMALIZATION_NAMES = {
    "abspath",
    "normcase",
    "normpath",
    "realpath",
    "resolve",
}
SELF_TEST_CASE_ORDER = (
    "stdout_positive_multiple_allowlisted_constants",
    "stdout_negative_fstring",
    "stdout_negative_runtime_concatenation",
    "stdout_negative_runtime_formatting",
    "stdout_negative_exception_text",
    "stdout_negative_path",
    "stdout_negative_value",
    "stdout_negative_id",
    "stdout_negative_count",
    "stdout_negative_registry_content",
    "reparse_positive_direct_attribute",
    "reparse_positive_safe_getattr",
    "reparse_negative_missing_bitmask",
    "reparse_negative_missing_skip",
    "reparse_negative_detection_followed_by_descent",
    "reparse_negative_normalization_fallback",
    "broadcast_positive_exact_bounded_after_readbacks",
    "broadcast_negative_missing_broadcast",
    "broadcast_negative_wrong_message",
    "broadcast_negative_wrong_lparam",
    "broadcast_negative_before_readback",
    "broadcast_negative_dynamic_lparam",
    "broadcast_negative_non_timeout_send",
    "broadcast_negative_ignored_return",
    "broadcast_negative_retry_or_second_broadcast",
)
SELF_TEST_OUTPUTS = {
    name: "SELF_TEST_" + name.upper() + "=PASS"
    for name in SELF_TEST_CASE_ORDER
}
HELPER_AUDIT_CHECK_ORDER = (
    "source_parse",
    "constants",
    "imports",
    "forbidden_calls",
    "stdout",
    "reparse",
    "registry",
    "broadcast",
)
HELPER_AUDIT_OUTPUTS = {
    name: "HELPER_AUDIT_" + name.upper() + "=PASS"
    for name in HELPER_AUDIT_CHECK_ORDER
}


class AuditError(Exception):
    pass


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuditError()
        result[key] = value
    return result


def _read_utf8_no_bom(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AuditError()
    try:
        return raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise AuditError() from exc


def _read_strict_json_object(path):
    text = _read_utf8_no_bom(path)
    try:
        value = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    except (json.JSONDecodeError, AuditError) as exc:
        raise AuditError() from exc
    if not isinstance(value, dict):
        raise AuditError()
    return value


def _module_assignments(tree):
    values = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (str, int)):
            values[target.id] = node.value.value
        elif isinstance(node.value, (ast.Tuple, ast.List)):
            elements = []
            valid = True
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    elements.append(element.value)
                elif isinstance(element, ast.Name) and element.id in values:
                    elements.append(values[element.id])
                else:
                    valid = False
                    break
            if valid:
                values[target.id] = tuple(elements)
    return values


def _call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _attribute_chain(node):
    parts = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return tuple(reversed(parts))
    return ()


def _audit_stdout_tree(tree):
    assignments = _module_assignments(tree)
    approved = assignments.get("APPROVED_STDOUT")
    if not isinstance(approved, tuple) or not approved:
        return False
    print_calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        chain = _attribute_chain(node.func)
        if chain in {
            ("sys", "stdout", "write"),
            ("sys", "stderr", "write"),
        }:
            return False
        if not isinstance(node.func, ast.Name) or node.func.id != "print":
            continue
        print_calls += 1
        if len(node.args) != 1 or node.keywords:
            return False
        argument = node.args[0]
        if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
            output_value = argument.value
        elif isinstance(argument, ast.Name):
            output_value = assignments.get(argument.id)
        else:
            return False
        if not isinstance(output_value, str) or output_value not in approved:
            return False
    return print_calls > 0


def _is_false_constant(node):
    return isinstance(node, ast.Constant) and node.value is False


def _has_nonfollowing_stat(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "stat":
            continue
        for keyword in node.keywords:
            if keyword.arg == "follow_symlinks" and _is_false_constant(keyword.value):
                return True
    return False


def _is_direct_attributes(node):
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "file_stat"
        and node.attr == "st_file_attributes"
    )


def _is_safe_getattr_attributes(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
        and len(node.args) == 3
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "file_stat"
        and isinstance(node.args[1], ast.Constant)
        and node.args[1].value == "st_file_attributes"
        and isinstance(node.args[2], ast.Constant)
        and node.args[2].value == 0
        and not node.keywords
    )


def _is_reparse_mask(node):
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "stat"
        and node.attr == "FILE_ATTRIBUTE_REPARSE_POINT"
    ) or (
        isinstance(node, ast.Name)
        and node.id == "FILE_ATTRIBUTE_REPARSE_POINT"
    )


def _contains_reparse_bitand(node):
    for child in ast.walk(node):
        if not isinstance(child, ast.BinOp) or not isinstance(child.op, ast.BitAnd):
            continue
        left_ok = _is_direct_attributes(child.left) or _is_safe_getattr_attributes(child.left)
        right_ok = _is_reparse_mask(child.right)
        reverse_left_ok = _is_direct_attributes(child.right) or _is_safe_getattr_attributes(child.right)
        reverse_right_ok = _is_reparse_mask(child.left)
        if (left_ok and right_ok) or (reverse_left_ok and reverse_right_ok):
            return True
    return False


def _has_forbidden_normalization(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name in FORBIDDEN_NORMALIZATION_NAMES:
            return True
    return False


def _audit_reparse_tree(tree):
    if _has_forbidden_normalization(tree):
        return False
    if not _has_nonfollowing_stat(tree):
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        if not _contains_reparse_bitand(node.test):
            continue
        if node.body and isinstance(node.body[0], ast.Continue):
            return True
    return False


def _audit_imports(tree):
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module is None:
                return False
            imports.add(node.module.split(".")[0])
    return imports == ALLOWED_HELPER_IMPORTS


def _audit_forbidden_calls(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALL_NAMES:
                return False
            chain = _attribute_chain(node.func)
            if chain in {
                ("importlib", "import_module"),
                ("os", "getenv"),
                ("os", "putenv"),
                ("os", "unsetenv"),
                ("subprocess", "run"),
                ("subprocess", "Popen"),
            }:
                return False
        if isinstance(node, ast.Attribute):
            chain = _attribute_chain(node)
            if chain in {
                ("os", "environ"),
                ("winreg", "HKEY_LOCAL_MACHINE"),
            }:
                return False
    return True


def _audit_constants(tree):
    assignments = _module_assignments(tree)
    return (
        assignments.get("SEARCH_ROOT") == EXPECTED_SEARCH_ROOT
        and assignments.get("MAX_SEARCH_DEPTH") == EXPECTED_MAX_SEARCH_DEPTH
        and assignments.get("PROVIDER_RESULT_BASENAME") == EXPECTED_PROVIDER_RESULT_BASENAME
        and assignments.get("ENVIRONMENT_VARIABLE_NAMES") == EXPECTED_ENVIRONMENT_VARIABLE_NAMES
        and assignments.get("REGISTRY_SUBKEY") == EXPECTED_REGISTRY_SUBKEY
        and assignments.get("HWND_BROADCAST") == EXPECTED_HWND_BROADCAST
        and assignments.get("WM_SETTINGCHANGE") == EXPECTED_WM_SETTINGCHANGE
        and assignments.get("SMTO_ABORTIFHUNG") == EXPECTED_SMTO_ABORTIFHUNG
        and assignments.get("ENVIRONMENT_BROADCAST_LPARAM")
        == EXPECTED_ENVIRONMENT_BROADCAST_LPARAM
        and assignments.get("BROADCAST_TIMEOUT_MS") == EXPECTED_BROADCAST_TIMEOUT_MS
        and assignments.get("APPROVED_STDOUT") == EXPECTED_HELPER_OUTPUTS
    )


def _audit_registry(tree):
    set_calls = 0
    query_calls = 0
    has_hkcu = False
    has_reg_sz = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            chain = _attribute_chain(node)
            if chain == ("winreg", "HKEY_CURRENT_USER"):
                has_hkcu = True
            elif chain == ("winreg", "REG_SZ"):
                has_reg_sz = True
        if not isinstance(node, ast.Call):
            continue
        chain = _attribute_chain(node.func)
        if chain == ("winreg", "SetValueEx"):
            set_calls += 1
        elif chain == ("winreg", "QueryValueEx"):
            query_calls += 1
    return has_hkcu and has_reg_sz and set_calls == 1 and query_calls == 1


def _function_def(tree, name):
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    return matches[0] if len(matches) == 1 else None


def _is_true_constant(node):
    return isinstance(node, ast.Constant) and node.value is True


def _is_zero_constant(node):
    return isinstance(node, ast.Constant) and node.value == 0


def _is_name(node, name):
    return isinstance(node, ast.Name) and node.id == name


def _is_chain(node, expected):
    return _attribute_chain(node) == expected


def _is_win_dll_call(node):
    if not isinstance(node, ast.Call) or not _is_chain(node.func, ("ctypes", "WinDLL")):
        return False
    if len(node.args) != 1:
        return False
    if not isinstance(node.args[0], ast.Constant) or node.args[0].value != "user32":
        return False
    if len(node.keywords) != 1:
        return False
    keyword = node.keywords[0]
    return keyword.arg == "use_last_error" and _is_true_constant(keyword.value)


def _is_pointer_to_c_size_t(node):
    return (
        isinstance(node, ast.Call)
        and _is_chain(node.func, ("ctypes", "POINTER"))
        and len(node.args) == 1
        and not node.keywords
        and _is_chain(node.args[0], ("ctypes", "c_size_t"))
    )


def _is_exact_argtypes_tuple(node):
    if not isinstance(node, ast.Tuple) or len(node.elts) != 7:
        return False
    expected = (
        ("ctypes", "wintypes", "HWND"),
        ("ctypes", "wintypes", "UINT"),
        ("ctypes", "wintypes", "WPARAM"),
        ("ctypes", "wintypes", "LPARAM"),
        ("ctypes", "wintypes", "UINT"),
        ("ctypes", "wintypes", "UINT"),
    )
    for index, chain in enumerate(expected):
        if not _is_chain(node.elts[index], chain):
            return False
    return _is_pointer_to_c_size_t(node.elts[6])


def _is_exact_broadcast_call(node):
    if not isinstance(node, ast.Call):
        return False
    if not _is_name(node.func, "send_message_timeout_w"):
        return False
    if len(node.args) != 7 or node.keywords:
        return False
    return (
        _is_name(node.args[0], "HWND_BROADCAST")
        and _is_name(node.args[1], "WM_SETTINGCHANGE")
        and _is_zero_constant(node.args[2])
        and _is_name(node.args[3], "lparam_value")
        and _is_name(node.args[4], "SMTO_ABORTIFHUNG")
        and _is_name(node.args[5], "BROADCAST_TIMEOUT_MS")
        and isinstance(node.args[6], ast.Call)
        and _is_chain(node.args[6].func, ("ctypes", "byref"))
        and len(node.args[6].args) == 1
        and _is_name(node.args[6].args[0], "message_result")
        and not node.args[6].keywords
    )


def _contains_call_chain(node, chain):
    return any(
        isinstance(child, ast.Call) and _is_chain(child.func, chain)
        for child in ast.walk(node)
    )


def _top_level_print_names(function):
    names = []
    for statement in function.body:
        if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
            continue
        call = statement.value
        if not _is_name(call.func, "print") or len(call.args) != 1 or call.keywords:
            continue
        if isinstance(call.args[0], ast.Name):
            names.append(call.args[0].id)
    return names


def _handler_type_name(handler):
    if handler.type is None:
        return None
    if isinstance(handler.type, ast.Name):
        return handler.type.id
    return None


def _audit_broadcast_tree(tree):
    assignments = _module_assignments(tree)
    if (
        assignments.get("HWND_BROADCAST") != EXPECTED_HWND_BROADCAST
        or assignments.get("WM_SETTINGCHANGE") != EXPECTED_WM_SETTINGCHANGE
        or assignments.get("SMTO_ABORTIFHUNG") != EXPECTED_SMTO_ABORTIFHUNG
        or assignments.get("ENVIRONMENT_BROADCAST_LPARAM")
        != EXPECTED_ENVIRONMENT_BROADCAST_LPARAM
        or assignments.get("BROADCAST_TIMEOUT_MS") != EXPECTED_BROADCAST_TIMEOUT_MS
    ):
        return False

    broadcast_function = _function_def(tree, "_broadcast_environment_change")
    repair_function = _function_def(
        tree, "_write_and_readback_current_user_environment"
    )
    run_function = _function_def(tree, "_run")
    main_function = _function_def(tree, "main")
    if None in {broadcast_function, repair_function, run_function, main_function}:
        return False

    if any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(broadcast_function)):
        return False

    win_dll_assignments = []
    send_function_assignments = []
    argtypes_assignments = []
    restype_assignments = []
    environment_text_assignments = []
    lparam_assignments = []
    message_result_assignments = []
    broadcast_result_assignments = []
    set_last_error_calls = []
    send_calls = []

    for node in ast.walk(broadcast_function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if _is_name(target, "user32") and _is_win_dll_call(node.value):
                win_dll_assignments.append(node)
            elif (
                _is_name(target, "send_message_timeout_w")
                and isinstance(node.value, ast.Attribute)
                and _is_name(node.value.value, "user32")
                and node.value.attr == "SendMessageTimeoutW"
            ):
                send_function_assignments.append(node)
            elif (
                isinstance(target, ast.Attribute)
                and _is_name(target.value, "send_message_timeout_w")
                and target.attr == "argtypes"
                and _is_exact_argtypes_tuple(node.value)
            ):
                argtypes_assignments.append(node)
            elif (
                isinstance(target, ast.Attribute)
                and _is_name(target.value, "send_message_timeout_w")
                and target.attr == "restype"
                and _is_chain(node.value, ("ctypes", "wintypes", "LPARAM"))
            ):
                restype_assignments.append(node)
            elif (
                _is_name(target, "environment_text")
                and isinstance(node.value, ast.Call)
                and _is_chain(node.value.func, ("ctypes", "c_wchar_p"))
                and len(node.value.args) == 1
                and _is_name(node.value.args[0], "ENVIRONMENT_BROADCAST_LPARAM")
                and not node.value.keywords
            ):
                environment_text_assignments.append(node)
            elif (
                _is_name(target, "lparam_value")
                and isinstance(node.value, ast.Attribute)
                and node.value.attr == "value"
                and isinstance(node.value.value, ast.Call)
                and _is_chain(node.value.value.func, ("ctypes", "cast"))
                and len(node.value.value.args) == 2
                and _is_name(node.value.value.args[0], "environment_text")
                and _is_chain(node.value.value.args[1], ("ctypes", "c_void_p"))
                and not node.value.value.keywords
            ):
                lparam_assignments.append(node)
            elif (
                _is_name(target, "message_result")
                and isinstance(node.value, ast.Call)
                and _is_chain(node.value.func, ("ctypes", "c_size_t"))
                and len(node.value.args) == 1
                and _is_zero_constant(node.value.args[0])
                and not node.value.keywords
            ):
                message_result_assignments.append(node)
            elif _is_name(target, "broadcast_result") and _is_exact_broadcast_call(
                node.value
            ):
                broadcast_result_assignments.append(node)

        if isinstance(node, ast.Call):
            if _is_chain(node.func, ("ctypes", "set_last_error")):
                if (
                    len(node.args) == 1
                    and _is_zero_constant(node.args[0])
                    and not node.keywords
                ):
                    set_last_error_calls.append(node)
            if _is_name(node.func, "send_message_timeout_w"):
                send_calls.append(node)
            if isinstance(node.func, ast.Attribute) and node.func.attr == "SendMessageW":
                return False

    if not all(
        len(items) == 1
        for items in (
            win_dll_assignments,
            send_function_assignments,
            argtypes_assignments,
            restype_assignments,
            environment_text_assignments,
            lparam_assignments,
            message_result_assignments,
            broadcast_result_assignments,
            set_last_error_calls,
            send_calls,
        )
    ):
        return False

    return_check = False
    for node in ast.walk(broadcast_function):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not (
            isinstance(test, ast.Compare)
            and _is_name(test.left, "broadcast_result")
            and len(test.ops) == 1
            and isinstance(test.ops[0], ast.Eq)
            and len(test.comparators) == 1
            and _is_zero_constant(test.comparators[0])
        ):
            continue
        if (
            node.body
            and isinstance(node.body[0], ast.Raise)
            and isinstance(node.body[0].exc, ast.Call)
            and _is_name(node.body[0].exc.func, "BroadcastBlocked")
        ):
            return_check = True
    if not return_check:
        return False

    repair_try_index = None
    repair_broadcast_index = None
    for index, statement in enumerate(repair_function.body):
        if isinstance(statement, ast.Try):
            has_set = _contains_call_chain(statement, ("winreg", "SetValueEx"))
            has_query = _contains_call_chain(statement, ("winreg", "QueryValueEx"))
            if has_set and has_query:
                repair_try_index = index
        if (
            isinstance(statement, ast.Expr)
            and isinstance(statement.value, ast.Call)
            and _is_name(statement.value.func, "_broadcast_environment_change")
            and not statement.value.args
            and not statement.value.keywords
        ):
            if repair_broadcast_index is not None:
                return False
            repair_broadcast_index = index
    if (
        repair_try_index is None
        or repair_broadcast_index is None
        or repair_broadcast_index <= repair_try_index
    ):
        return False

    print_names = _top_level_print_names(run_function)
    if "OUTPUT_BROADCAST_PASS" not in print_names:
        return False
    broadcast_index = print_names.index("OUTPUT_BROADCAST_PASS")
    for required in (
        "OUTPUT_RESULTS_DIR_PASS",
        "OUTPUT_EXPORT_ROOT_PASS",
        "OUTPUT_ADAPTER_ID_PASS",
        "OUTPUT_REPAIR_PASS",
    ):
        if required not in print_names or print_names.index(required) <= broadcast_index:
            return False

    try_statements = [node for node in main_function.body if isinstance(node, ast.Try)]
    if len(try_statements) != 1:
        return False
    handlers = try_statements[0].handlers
    if len(handlers) < 2 or _handler_type_name(handlers[0]) != "BroadcastBlocked":
        return False
    first_handler_prints = [
        node
        for node in ast.walk(handlers[0])
        if isinstance(node, ast.Call) and _is_name(node.func, "print")
    ]
    if len(first_handler_prints) != 1:
        return False
    first_print = first_handler_prints[0]
    if (
        len(first_print.args) != 1
        or not _is_name(first_print.args[0], "OUTPUT_BROADCAST_BLOCKED")
    ):
        return False
    if _handler_type_name(handlers[1]) != "Exception":
        return False

    return True



def _audit_helper_source(source):
    checks = {name: False for name in HELPER_AUDIT_CHECK_ORDER}
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return checks
    checks["source_parse"] = True
    checks["constants"] = _audit_constants(tree)
    checks["imports"] = _audit_imports(tree)
    checks["forbidden_calls"] = _audit_forbidden_calls(tree)
    checks["stdout"] = _audit_stdout_tree(tree)
    checks["reparse"] = _audit_reparse_tree(tree)
    checks["registry"] = _audit_registry(tree)
    checks["broadcast"] = _audit_broadcast_tree(tree)
    return checks


def _run_self_test(fixtures):
    if fixtures.get("schema") != "sentigraph_cib_env_r2_r2_auditor_self_test_fixtures_v0_2":
        raise AuditError()
    cases = fixtures.get("cases")
    if not isinstance(cases, list):
        raise AuditError()
    names = tuple(case.get("name") for case in cases if isinstance(case, dict))
    if names != SELF_TEST_CASE_ORDER:
        raise AuditError()
    for case in cases:
        category = case.get("category")
        expected = case.get("expected")
        source = case.get("source")
        if category not in {"stdout", "reparse", "broadcast"}:
            raise AuditError()
        if not isinstance(expected, bool) or not isinstance(source, str):
            raise AuditError()
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            raise AuditError() from exc
        if category == "stdout":
            actual = _audit_stdout_tree(tree)
        elif category == "reparse":
            actual = _audit_reparse_tree(tree)
        else:
            actual = _audit_broadcast_tree(tree)
        if actual is not expected:
            raise AuditError()
        print(SELF_TEST_OUTPUTS[case["name"]])
    print("AUDITOR_SELF_TEST=PASS")


def _run_helper_audit(source):
    checks = _audit_helper_source(source)
    for name in HELPER_AUDIT_CHECK_ORDER:
        if not checks[name]:
            raise AuditError()
        print(HELPER_AUDIT_OUTPUTS[name])
    print("FIXED_HELPER_STATIC_AUDIT=PASS")


def main(argv):
    if len(argv) != 3:
        print("STATIC_AUDITOR=BLOCKED_ARGUMENTS")
        return 2
    mode = argv[1]
    try:
        if mode == "self-test":
            fixtures = _read_strict_json_object(argv[2])
            _run_self_test(fixtures)
        elif mode == "audit-helper":
            source = _read_utf8_no_bom(argv[2])
            _run_helper_audit(source)
        else:
            raise AuditError()
    except (AuditError, OSError):
        print("STATIC_AUDITOR=FAIL")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
