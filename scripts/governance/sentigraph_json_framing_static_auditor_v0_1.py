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
