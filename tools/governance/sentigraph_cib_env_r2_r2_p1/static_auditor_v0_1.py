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
EXPECTED_HELPER_OUTPUTS = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR=PASS",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT=PASS",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID=PASS",
    "CIB_ENV_R2_R2_P2=REPAIR_COMPLETED_PENDING_CODEX_RESTART",
    "CIB_ENV_R2_R2_P2=BLOCKED_SAFE_DISAMBIGUATION_OR_REPAIR",
)
ALLOWED_HELPER_IMPORTS = {
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
    return checks


def _run_self_test(fixtures):
    if fixtures.get("schema") != "sentigraph_cib_env_r2_r2_auditor_self_test_fixtures_v0_1":
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
        if category not in {"stdout", "reparse"}:
            raise AuditError()
        if not isinstance(expected, bool) or not isinstance(source, str):
            raise AuditError()
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            raise AuditError() from exc
        actual = (
            _audit_stdout_tree(tree)
            if category == "stdout"
            else _audit_reparse_tree(tree)
        )
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
