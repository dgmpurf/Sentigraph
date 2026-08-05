from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
PROJECT_PYTHON = Path(sys.executable).resolve()


FRESH_PROCESS_PROBE = r'''
import ast
import json
import os
import sys
from collections import Counter
from pathlib import Path

import fastapi
import fastapi.routing as fastapi_routing
from starlette.routing import Match


CHILD_PATH = "/local-exchange-projections/{sample_handle}"
AGGREGATE_PATH = (
    "/internal/alpha/review-console/local-exchange-projections/{sample_handle}"
)
APP_PREFIX = "/api/v1"
APP_PATH = APP_PREFIX + AGGREGATE_PATH
CONCRETE_PATH = (
    "/api/v1/internal/alpha/review-console/"
    "local-exchange-projections/helldivers2-psn-demo"
)


class UnsupportedRouteInventoryContract(Exception):
    pass


def normalized_path(value):
    return os.path.normcase(str(Path(value).resolve()))


def same_path(actual, expected):
    return normalized_path(actual) == normalized_path(expected)


def effective_routes(routes):
    iterator = getattr(fastapi_routing, "iter_route_contexts", None)
    if iterator is not None:
        return list(iterator(routes)), "iter_route_contexts"
    immediate = list(routes)
    required = ("path", "methods", "matches")
    if all(all(hasattr(route, name) for name in required) for route in immediate):
        return immediate, "flat_immediate_routes"
    raise UnsupportedRouteInventoryContract


def route_signature(route):
    return (
        str(getattr(route, "path", "")),
        tuple(sorted(str(method) for method in (getattr(route, "methods", None) or ()))),
        str(getattr(route, "name", None) or ""),
    )


def path_counts(signatures, expected_path):
    path_only = sum(signature[0] == expected_path for signature in signatures)
    with_get = sum(
        signature[0] == expected_path and "GET" in signature[1]
        for signature in signatures
    )
    return path_only, with_get


def prefixed_signature(signature, prefix):
    path, methods, name = signature
    return (prefix.rstrip("/") + path, methods, name)


def full_match_count(routes):
    scope = {
        "type": "http",
        "method": "GET",
        "path": CONCRETE_PATH,
        "root_path": "",
        "headers": [],
        "query_string": b"",
    }
    return sum(
        getattr(route, "path", None) == APP_PATH
        and route.matches(dict(scope))[0] == Match.FULL
        for route in routes
    )


def dotted_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def run_probe():
    repository_root = Path(sys.argv[1]).resolve()
    backend_root = Path(sys.argv[2]).resolve()
    pycache_root = Path(sys.argv[3]).resolve()

    import app.api.v1.api as api_module
    import app.api.v1.routes.internal_alpha_review_console as target_module
    import app.main as main_module

    expected_main = backend_root / "app" / "main.py"
    expected_api = backend_root / "app" / "api" / "v1" / "api.py"
    expected_target = (
        backend_root
        / "app"
        / "api"
        / "v1"
        / "routes"
        / "internal_alpha_review_console.py"
    )

    target_routes, target_mode = effective_routes(target_module.router.routes)
    aggregate_routes, aggregate_mode = effective_routes(api_module.api_router.routes)
    app_one = main_module.create_app()
    app_two = main_module.create_app()
    app_one_routes, app_one_mode = effective_routes(app_one.routes)
    app_two_routes, app_two_mode = effective_routes(app_two.routes)
    compatibility_modes = {
        target_mode,
        aggregate_mode,
        app_one_mode,
        app_two_mode,
    }
    compatibility_mode = (
        next(iter(compatibility_modes))
        if len(compatibility_modes) == 1
        else "mixed_route_inventory_modes"
    )

    target_signatures = [route_signature(route) for route in target_routes]
    aggregate_signatures = [route_signature(route) for route in aggregate_routes]
    app_one_signatures = [route_signature(route) for route in app_one_routes]
    app_two_signatures = [route_signature(route) for route in app_two_routes]

    target_path_only, target_with_get = path_counts(target_signatures, CHILD_PATH)
    aggregate_path_only, aggregate_with_get = path_counts(
        aggregate_signatures,
        AGGREGATE_PATH,
    )
    app_one_path_only, app_one_with_get = path_counts(app_one_signatures, APP_PATH)
    app_two_path_only, app_two_with_get = path_counts(app_two_signatures, APP_PATH)

    aggregate_counter = Counter(aggregate_signatures)
    app_one_counter = Counter(app_one_signatures)
    app_two_counter = Counter(app_two_signatures)
    api_prefix = str(main_module.settings.api_v1_prefix)
    expected_application_counter = Counter()
    for signature, count in aggregate_counter.items():
        expected_application_counter[prefixed_signature(signature, api_prefix)] += count
    app_one_missing_aggregate = sum(
        max(count - app_one_counter[signature], 0)
        for signature, count in expected_application_counter.items()
    )
    app_two_missing_aggregate = sum(
        max(count - app_two_counter[signature], 0)
        for signature, count in expected_application_counter.items()
    )

    aggregate_target_signatures = [
        signature
        for signature in aggregate_signatures
        if signature[0] == AGGREGATE_PATH and "GET" in signature[1]
    ]
    if len(aggregate_target_signatures) == 1:
        expected_target_signature = prefixed_signature(
            aggregate_target_signatures[0],
            api_prefix,
        )
        app_one_target_signature_count = app_one_counter[expected_target_signature]
        app_two_target_signature_count = app_two_counter[expected_target_signature]
    else:
        app_one_target_signature_count = -1
        app_two_target_signature_count = -1

    main_path = Path(main_module.__file__).resolve()
    main_tree = ast.parse(main_path.read_text(encoding="utf-8"))
    include_calls = [
        node
        for node in ast.walk(main_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "include_router"
    ]
    aggregate_include_count = sum(
        bool(call.args) and dotted_name(call.args[0]) == "api_router"
        for call in include_calls
    )
    direct_target_include_count = sum(
        any(
            isinstance(node, (ast.Name, ast.Attribute))
            and "internal_alpha_review_console" in dotted_name(node)
            for node in ast.walk(call)
        )
        for call in include_calls
    )

    result = {
        "status": "contract_failure",
        "fastapi_version": str(getattr(fastapi, "__version__", "unknown")),
        "compatibility_mode": compatibility_mode,
        "main_origin_matches_expected": same_path(main_module.__file__, expected_main),
        "api_origin_matches_expected": same_path(api_module.__file__, expected_api),
        "target_origin_matches_expected": same_path(
            target_module.__file__,
            expected_target,
        ),
        "repository_argument_matches_backend_parent": (
            normalized_path(repository_root) == normalized_path(backend_root.parent)
        ),
        "sys_pycache_prefix_matches_unique_directory": same_path(
            sys.pycache_prefix,
            pycache_root,
        ),
        "sys_dont_write_bytecode": bool(sys.dont_write_bytecode),
        "main_api_router_is_api_module_api_router": (
            main_module.api_router is api_module.api_router
        ),
        "api_prefix_matches_expected": api_prefix == APP_PREFIX,
        "target_child_path_only_count": target_path_only,
        "target_child_with_get_count": target_with_get,
        "aggregate_target_path_only_count": aggregate_path_only,
        "aggregate_target_with_get_count": aggregate_with_get,
        "app_one_target_path_only_count": app_one_path_only,
        "app_one_target_with_get_count": app_one_with_get,
        "app_two_target_path_only_count": app_two_path_only,
        "app_two_target_with_get_count": app_two_with_get,
        "concrete_scope_full_match_count": full_match_count(app_one_routes),
        "app_one_missing_aggregate_signature_instances": app_one_missing_aggregate,
        "app_two_missing_aggregate_signature_instances": app_two_missing_aggregate,
        "fresh_app_signature_multisets_identical": app_one_counter == app_two_counter,
        "app_one_target_signature_count": app_one_target_signature_count,
        "app_two_target_signature_count": app_two_target_signature_count,
        "main_aggregate_include_count": aggregate_include_count,
        "main_direct_target_include_count": direct_target_include_count,
    }
    result["all_contracts_pass"] = all(
        (
            result["compatibility_mode"]
            in {"iter_route_contexts", "flat_immediate_routes"},
            result["main_origin_matches_expected"],
            result["api_origin_matches_expected"],
            result["target_origin_matches_expected"],
            result["repository_argument_matches_backend_parent"],
            result["sys_pycache_prefix_matches_unique_directory"],
            result["sys_dont_write_bytecode"],
            result["main_api_router_is_api_module_api_router"],
            result["api_prefix_matches_expected"],
            target_path_only == 1,
            target_with_get == 1,
            aggregate_path_only == 1,
            aggregate_with_get == 1,
            app_one_path_only == 1,
            app_one_with_get == 1,
            app_two_path_only == 1,
            app_two_with_get == 1,
            result["concrete_scope_full_match_count"] == 1,
            app_one_missing_aggregate == 0,
            app_two_missing_aggregate == 0,
            result["fresh_app_signature_multisets_identical"],
            app_one_target_signature_count == 1,
            app_two_target_signature_count == 1,
            aggregate_include_count == 1,
            direct_target_include_count == 0,
        )
    )
    if result["all_contracts_pass"]:
        result["status"] = "pass"
    return result


try:
    payload = run_probe()
except UnsupportedRouteInventoryContract:
    payload = {
        "status": "unsupported_fastapi_route_inventory_contract",
        "fastapi_version": str(getattr(fastapi, "__version__", "unknown")),
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    raise SystemExit(30)
except Exception as exc:
    payload = {
        "status": "probe_failure",
        "exception_type": type(exc).__name__,
    }
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    raise SystemExit(31)

print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
'''


def _is_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.relative_to(parent)
    except ValueError:
        return False
    return True


def _safe_subprocess_payload(stdout: str) -> dict[str, object]:
    try:
        payload = json.loads(stdout)
    except (json.JSONDecodeError, TypeError):
        raise AssertionError(
            json.dumps({"failure_stage": "bounded_json_parse"}, sort_keys=True)
        ) from None
    if not isinstance(payload, dict):
        raise AssertionError(
            json.dumps({"failure_stage": "bounded_json_type"}, sort_keys=True)
        )
    return payload


def test_api_router_assembly_in_fresh_process(tmp_path: Path) -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden_tokens = (
        "G:" + chr(92),
        "C:" + chr(92) + "Us" + "ers",
        "ms" + "jpurf",
        "." + "co" + "dex",
        "SENTIGRAPH_" + "RUNTIME",
    )
    assert all(token not in source for token in forbidden_tokens)
    assert re.search(r"[A-Za-z]:[\\/]", source) is None

    repository_root = REPOSITORY_ROOT.resolve()
    backend_root = BACKEND_ROOT.resolve()
    project_python = PROJECT_PYTHON.resolve()
    unique_root = tmp_path.resolve()
    assert repository_root.is_dir()
    assert backend_root.is_dir()
    assert project_python.is_file()
    assert project_python == Path(sys.executable).resolve()
    assert not _is_within(unique_root, repository_root)

    pycache_root = unique_root / "pycache"
    pycache_root.mkdir(parents=True, exist_ok=False)
    assert not any(pycache_root.iterdir())

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(backend_root)
    environment["PYTHONPYCACHEPREFIX"] = str(pycache_root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    try:
        try:
            completed = subprocess.run(
                [
                    str(project_python),
                    "-B",
                    "-c",
                    FRESH_PROCESS_PROBE,
                    str(repository_root),
                    str(backend_root),
                    str(pycache_root),
                ],
                cwd=unique_root,
                env=environment,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise AssertionError(
                json.dumps({"failure_stage": "fresh_process_timeout"}, sort_keys=True)
            ) from None
        except OSError as exc:
            raise AssertionError(
                json.dumps(
                    {
                        "failure_stage": "fresh_process_start",
                        "exception_type": type(exc).__name__,
                    },
                    sort_keys=True,
                )
            ) from None

        observed = _safe_subprocess_payload(completed.stdout)
        if completed.returncode != 0:
            safe_failure = {
                key: observed[key]
                for key in ("status", "fastapi_version", "exception_type")
                if key in observed
            }
            raise AssertionError(
                json.dumps(
                    {
                        "failure_stage": "fresh_process_exit",
                        "return_code": completed.returncode,
                        "bounded_result": safe_failure,
                    },
                    sort_keys=True,
                )
            )

        expected_exact = {
            "status": "pass",
            "main_origin_matches_expected": True,
            "api_origin_matches_expected": True,
            "target_origin_matches_expected": True,
            "repository_argument_matches_backend_parent": True,
            "sys_pycache_prefix_matches_unique_directory": True,
            "sys_dont_write_bytecode": True,
            "main_api_router_is_api_module_api_router": True,
            "api_prefix_matches_expected": True,
            "target_child_path_only_count": 1,
            "target_child_with_get_count": 1,
            "aggregate_target_path_only_count": 1,
            "aggregate_target_with_get_count": 1,
            "app_one_target_path_only_count": 1,
            "app_one_target_with_get_count": 1,
            "app_two_target_path_only_count": 1,
            "app_two_target_with_get_count": 1,
            "concrete_scope_full_match_count": 1,
            "app_one_missing_aggregate_signature_instances": 0,
            "app_two_missing_aggregate_signature_instances": 0,
            "fresh_app_signature_multisets_identical": True,
            "app_one_target_signature_count": 1,
            "app_two_target_signature_count": 1,
            "main_aggregate_include_count": 1,
            "main_direct_target_include_count": 0,
            "all_contracts_pass": True,
        }
        bounded_mismatches = {
            key: observed.get(key)
            for key, expected in expected_exact.items()
            if observed.get(key) != expected
        }
        assert observed.get("compatibility_mode") in {
            "iter_route_contexts",
            "flat_immediate_routes",
        }
        assert not bounded_mismatches, json.dumps(
            {
                "failure_stage": "route_assembly_contract",
                "bounded_mismatches": bounded_mismatches,
            },
            sort_keys=True,
        )
    finally:
        cache_entries = list(pycache_root.rglob("*")) if pycache_root.exists() else []
        if not cache_entries and pycache_root.exists():
            pycache_root.rmdir()

    assert not cache_entries
    assert not pycache_root.exists()
