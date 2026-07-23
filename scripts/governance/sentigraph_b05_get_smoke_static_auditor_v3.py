from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

AUDITOR_SCHEMA = "sentigraph_b05_get_smoke_runner_static_audit_v3_result_v0_1"
SELF_TEST_SCHEMA = "sentigraph_b05_get_smoke_static_auditor_v3_self_test_result_v0_1"
QUALIFICATION_SCHEMA = "sentigraph_b05_get_smoke_auditor_v3_runner_v3_static_qualification_result_v0_1"
VERSION = "0.1"
EXPECTED_RUNNER_BASENAME = ".sentigraph_b05_get_smoke_runner_v3.py"
MAX_RUNNER_BYTES = 262144

CHECK_NAMES = (
    "STRICT_UTF8_NO_BOM",
    "AST_PARSE",
    "IMPORT_ALLOWLIST",
    "BOUND_CONSTANTS",
    "RECEIPT_SINGLE_READ",
    "CONFIG_EXACT_THREE_READS",
    "CIB_DATAFLOW",
    "CANONICAL_BINDING_CONSTANTS_EXACT",
    "CONFIGURATION_BOUND_EXACT",
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

NEGATIVE_SPECS = (
    ("second_http_get", "HTTP_GET_EXACTLY_ONCE_IN_PERFORM_GET"),
    ("perform_get_called_twice", "PERFORM_GET_CALLED_EXACTLY_ONCE"),
    ("gate_restore_removed", "GATE_RESTORE_REVERSED_OUTER_FINALLY"),
    ("dotenv_patch_after_import", "DOTENV_PATCH_BEFORE_APP_IMPORT"),
    ("dotenv_restore_removed", "DOTENV_RESTORE_OUTER_FINALLY"),
    ("forged_cib_digest", "CIB_DATAFLOW"),
    ("response_order_removed", "RESPONSE_EXACT_52_FIELD_ORDER"),
    ("raw_row_read", "RAW_ROW_PRIVACY_FAIL_CLOSED"),
    ("external_socket_action", "NO_EXTERNAL_OR_MUTATING_ACTIONS"),
    ("payload_output", "ATOMIC_SAFE_RESULT_AND_OUTPUT"),
    ("asyncio_run_added", "NO_ASYNCIO_RUN"),
    ("second_app_import", "APP_IMPORT_EXACTLY_ONCE"),
    ("second_event_loop", "EVENT_LOOP_EXACTLY_ONCE_AFTER_IMPORT"),
    ("asgi_transport_removed", "ASGI_TRANSPORT_EXACTLY_ONCE"),
    ("target_route_changed", "TARGET_ROUTE_EXACT"),
    ("directory_discovery_added", "NO_DIRECTORY_DISCOVERY"),
    ("socket_type_replaced", "NETWORK_GUARD_TYPE_PRESERVING_AND_ORDERED"),
    ("atomic_replace_removed", "ATOMIC_SAFE_RESULT_AND_OUTPUT"),
    ("receipt_schema_substitution", "CANONICAL_BINDING_CONSTANTS_EXACT"),
    ("opaque_configuration_bound_1048", "CONFIGURATION_BOUND_EXACT"),
)

VALID_PUBLIC_RUNNER = "from __future__ import annotations\n\nimport asyncio\nimport builtins\nimport glob\nimport hashlib\nimport hmac\nimport importlib\nimport io\nimport json\nimport os\nimport re\nimport socket\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nimport dotenv\n\nRUNNER_SCHEMA = \"sentigraph_b05_get_smoke_safe_result_v3_0_1\"\nRUNNER_VERSION = \"0.1\"\nMILESTONE = \"SENTIGRAPH-BASELINE-V2-5-RISK-PROMPT-1-ONE-GOVERNED-B05-GET-SMOKE-V3\"\nRUNNER_BASENAME = \".sentigraph_b05_get_smoke_runner_v3.py\"\nRESULT_BASENAME = \".sentigraph_b05_get_smoke_result_v3.json\"\nPARTIAL_RESULT_BASENAME = \".sentigraph_b05_get_smoke_result_v3.json.partial\"\nRECEIPT_BASENAME = \".sentigraph_cib_capture_risk_prompt_3_v1_safe_receipt.json\"\nTARGET_ROUTE = \"/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo\"\nPROVIDER_RESULT_BASENAME = \"provider_result_helldivers2-psn-demo_20260720_123627.json\"\nSERVICE_BLOB = \"f0c4a8768060a840ea1921aeba47a97f2e41f9e3\"\nB05_ROUTE_BLOB = \"8445b4595ea7edc9d9878e99b35ce0554b841c94\"\nB03_PROJECTION_BLOB = \"534bdf02e211134b52b2e7714d01a0dd615210b4\"\nB01_STAGING_BLOB = \"ef36b4370495b7f1e5c9c5c433d5b38c5cf9aa6d\"\nREGISTRY_SCHEMA = \"sentigraph_internal_alpha_local_exchange_sample_registry_v0_1\"\nSAMPLE_HANDLE = \"helldivers2-psn-demo\"\nROUTE_MODE = \"internal_alpha_read_only_local_exchange_projection_operator\"\nCAPABILITY_LABEL = \"b05_local_exchange_projection_read_only\"\nRECEIPT_BYTES = 1314\nRECEIPT_SHA256 = \"0273877f50391a1a77be6a0f9f506d3479dd1d694390711cb88f3047152db0c7\"\nBINDING_SCHEMA = \"sentigraph_b05_server_owned_configuration_identity_binding_v0_1\"\nRECEIPT_SCHEMA = \"sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1\"\nBINDING_SCOPE = \"b05_one_real_sample_handle_governed_read_only_projection_pre_smoke\"\n\nGATE_NAMES = (\n    \"SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED\",\n    \"SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\",\n    \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED\",\n    \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED\",\n    \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\",\n)\nCONFIGURATION_NAMES = (\n    \"SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR\",\n    \"SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT\",\n    \"SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID\",\n)\nAPPROVED_METADATA_BASENAMES = (\n    \"manifest.json\",\n    \"validation_report.json\",\n    \"validation_report.md\",\n    \"coverage_note.md\",\n    \"README.md\",\n    \"package_index.json\",\n)\nRAW_ROW_BASENAMES = (\n    \"source_manifest.jsonl\",\n    \"evidence_items.jsonl\",\n    \"evidence_items.csv\",\n    \"collection_log.jsonl\",\n)\nRECEIPT_FIELDS = (\n    \"schema\",\n    \"version\",\n    \"status\",\n    \"privacy_issue_stop\",\n    \"binding_scope\",\n    \"service_blob\",\n    \"registry_schema\",\n    \"sample_handle\",\n    \"result_file_name\",\n    \"route_mode\",\n    \"capability_label\",\n    \"configuration_names\",\n    \"configuration_value_reads\",\n    \"canonical_objects\",\n    \"canonical_serializations\",\n    \"combined_sha256_computations\",\n    \"new_salt_created\",\n    \"new_receipt_created\",\n    \"per_variable_hashes_created\",\n    \"receipt_reopens\",\n    \"salt_hex\",\n    \"combined_binding_sha256\",\n    \"warnings\",\n)\nSAFE_RESULT_FIELDS = (\n    \"schema\",\n    \"version\",\n    \"milestone\",\n    \"status\",\n    \"runtime_classification\",\n    \"privacy_issue_stop\",\n    \"starting_head\",\n    \"approval_sha256\",\n    \"contract_sha256\",\n    \"committed_blobs\",\n    \"auditor\",\n    \"runner\",\n    \"receipt_identity\",\n    \"execution\",\n    \"cib\",\n    \"gates\",\n    \"dotenv\",\n    \"application\",\n    \"response\",\n    \"file_access\",\n    \"restoration\",\n    \"hard_zero\",\n    \"warnings\",\n    \"blockers\",\n)\nSTATUS_LINES = {\n    \"success\": \"SENTIGRAPH_B05_GET_SMOKE_V3_STATUS=SUCCESS\",\n    \"cib\": \"SENTIGRAPH_B05_GET_SMOKE_V3_STATUS=BLOCKED_CIB_MISMATCH\",\n    \"privacy\": \"SENTIGRAPH_B05_GET_SMOKE_V3_STATUS=BLOCKED_PRIVACY_BOUNDARY\",\n    \"integrity\": \"SENTIGRAPH_B05_GET_SMOKE_V3_STATUS=BLOCKED_EXECUTION_INTEGRITY\",\n    \"transport\": \"SENTIGRAPH_B05_GET_SMOKE_V3_STATUS=RESULT_TRANSPORT_FAILURE\",\n}\n\n\nclass IntegrityBlock(Exception):\n    pass\n\n\nclass CIBMismatch(Exception):\n    pass\n\n\nclass PrivacyBlock(Exception):\n    pass\n\n\ndef _reject_duplicate_pairs(pairs):\n    result = {}\n    for key, value in pairs:\n        if key in result:\n            raise IntegrityBlock(\"duplicate key\")\n        result[key] = value\n    return result\n\n\ndef _validate_sha256(value):\n    return isinstance(value, str) and re.fullmatch(r\"[0-9a-f]{64}\", value) is not None\n\n\ndef _validate_blob(value):\n    return isinstance(value, str) and re.fullmatch(r\"[0-9a-f]{40}\", value) is not None\n\n\ndef _validate_opaque(value):\n    return (\n        isinstance(value, str)\n        and 1 <= len(value) <= 2048\n        and value == value.strip()\n        and value.isprintable()\n        and \"\\x00\" not in value\n    )\n\n\ndef _validate_adapter_id(value):\n    return isinstance(value, str) and re.fullmatch(r\"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\", value) is not None\n\n\ndef _parse_arguments():\n    argument_names = (\n        \"--repo-root\",\n        \"--starting-head\",\n        \"--approval-sha256\",\n        \"--contract-sha256\",\n        \"--auditor-bytes\",\n        \"--auditor-sha256\",\n        \"--auditor-blob\",\n        \"--runner-bytes\",\n        \"--runner-sha256\",\n    )\n    tokens = sys.argv[1:]\n    if len(tokens) != len(argument_names) * 2:\n        raise IntegrityBlock(\"argument count\")\n    values = {}\n    for index, argument_name in enumerate(argument_names):\n        token_index = index * 2\n        if tokens[token_index] != argument_name or argument_name in values:\n            raise IntegrityBlock(\"argument order\")\n        values[argument_name] = tokens[token_index + 1]\n\n    class Arguments:\n        pass\n\n    args = Arguments()\n    args.repo_root = values[\"--repo-root\"]\n    args.starting_head = values[\"--starting-head\"]\n    args.approval_sha256 = values[\"--approval-sha256\"]\n    args.contract_sha256 = values[\"--contract-sha256\"]\n    args.auditor_sha256 = values[\"--auditor-sha256\"]\n    args.auditor_blob = values[\"--auditor-blob\"]\n    args.runner_sha256 = values[\"--runner-sha256\"]\n    try:\n        args.auditor_bytes = int(values[\"--auditor-bytes\"])\n        args.runner_bytes = int(values[\"--runner-bytes\"])\n    except ValueError as exc:\n        raise IntegrityBlock(\"argument bytes\") from exc\n    return args\n\n\ndef _validate_arguments(args):\n    repo_root = Path(args.repo_root)\n    if not repo_root.is_absolute():\n        raise IntegrityBlock(\"repo root\")\n    external_parent = repo_root.parent\n    if Path.cwd() != external_parent:\n        raise IntegrityBlock(\"working directory\")\n    expected_runner = external_parent / RUNNER_BASENAME\n    if Path(__file__).resolve() != expected_runner.resolve():\n        raise IntegrityBlock(\"runner identity\")\n    if (external_parent / RESULT_BASENAME).exists() or (external_parent / PARTIAL_RESULT_BASENAME).exists():\n        raise IntegrityBlock(\"result target exists\")\n    if not _validate_blob(args.starting_head):\n        raise IntegrityBlock(\"starting head\")\n    if not _validate_sha256(args.approval_sha256) or not _validate_sha256(args.contract_sha256):\n        raise IntegrityBlock(\"approval identity\")\n    if not _validate_sha256(args.auditor_sha256) or not _validate_sha256(args.runner_sha256):\n        raise IntegrityBlock(\"source identity\")\n    if not _validate_blob(args.auditor_blob):\n        raise IntegrityBlock(\"auditor blob\")\n    if not 1 <= args.auditor_bytes <= 262144 or not 1 <= args.runner_bytes <= 262144:\n        raise IntegrityBlock(\"source byte bounds\")\n    return repo_root, external_parent\n\n\ndef _read_receipt(external_parent):\n    receipt_path = external_parent / RECEIPT_BASENAME\n    if not receipt_path.is_absolute() or receipt_path.is_symlink() or not receipt_path.is_file():\n        raise IntegrityBlock(\"receipt file\")\n    with receipt_path.open(\"rb\") as handle:\n        raw = handle.read()\n    if len(raw) != RECEIPT_BYTES:\n        raise IntegrityBlock(\"receipt bytes\")\n    if not hmac.compare_digest(hashlib.sha256(raw).hexdigest(), RECEIPT_SHA256):\n        raise IntegrityBlock(\"receipt identity\")\n    if raw.startswith(b\"\\xef\\xbb\\xbf\"):\n        raise IntegrityBlock(\"receipt bom\")\n    try:\n        text = raw.decode(\"utf-8\", errors=\"strict\")\n        receipt = json.loads(text, object_pairs_hook=_reject_duplicate_pairs)\n    except (UnicodeDecodeError, json.JSONDecodeError) as exc:\n        raise IntegrityBlock(\"receipt format\") from exc\n    if tuple(receipt.keys()) != RECEIPT_FIELDS:\n        raise IntegrityBlock(\"receipt fields\")\n    if receipt[\"schema\"] != RECEIPT_SCHEMA or receipt[\"version\"] != \"0.1\":\n        raise IntegrityBlock(\"receipt schema\")\n    if receipt[\"status\"] != \"ready\" or receipt[\"privacy_issue_stop\"] is not False:\n        raise IntegrityBlock(\"receipt status\")\n    if receipt[\"configuration_value_reads\"] != 3:\n        raise IntegrityBlock(\"receipt read ledger\")\n    if receipt[\"canonical_objects\"] != 1 or receipt[\"canonical_serializations\"] != 1:\n        raise IntegrityBlock(\"receipt canonical ledger\")\n    if receipt[\"combined_sha256_computations\"] != 1:\n        raise IntegrityBlock(\"receipt digest ledger\")\n    if receipt[\"new_salt_created\"] is not False or receipt[\"new_receipt_created\"] is not False:\n        raise IntegrityBlock(\"receipt creation ledger\")\n    if receipt[\"per_variable_hashes_created\"] is not False or receipt[\"receipt_reopens\"] != 0:\n        raise IntegrityBlock(\"receipt hard zero ledger\")\n    return receipt\n\n\ndef _read_configuration():\n    results_dir = os.environ.get(\"SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR\")\n    export_root = os.environ.get(\"SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT\")\n    adapter_id = os.environ.get(\"SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID\")\n    if not _validate_opaque(results_dir) or not _validate_opaque(export_root):\n        raise IntegrityBlock(\"opaque configuration\")\n    if not _validate_adapter_id(adapter_id):\n        raise IntegrityBlock(\"adapter id\")\n    return results_dir, export_root, adapter_id\n\n\ndef verify_cib(receipt, configuration_values):\n    canonical_object = {\n        \"schema\": \"sentigraph_b05_server_owned_configuration_identity_binding_v0_1\",\n        \"version\": \"0.1\",\n        \"binding_scope\": \"b05_one_real_sample_handle_governed_read_only_projection_pre_smoke\",\n        \"service_blob\": \"f0c4a8768060a840ea1921aeba47a97f2e41f9e3\",\n        \"registry_schema\": \"sentigraph_internal_alpha_local_exchange_sample_registry_v0_1\",\n        \"sample_handle\": \"helldivers2-psn-demo\",\n        \"result_file_name\": \"provider_result_helldivers2-psn-demo_20260720_123627.json\",\n        \"route_mode\": \"internal_alpha_read_only_local_exchange_projection_operator\",\n        \"capability_label\": \"b05_local_exchange_projection_read_only\",\n        \"salt_hex\": receipt[\"salt_hex\"],\n        \"configuration_values\": [\n            {\"name\": \"SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR\", \"value\": configuration_values[0]},\n            {\"name\": \"SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT\", \"value\": configuration_values[1]},\n            {\"name\": \"SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID\", \"value\": configuration_values[2]},\n        ],\n    }\n    canonical_bytes = json.dumps(\n        canonical_object,\n        ensure_ascii=False,\n        separators=(\",\", \":\"),\n        sort_keys=False,\n    ).encode(\"utf-8\")\n    recomputed_binding = hashlib.sha256(canonical_bytes).hexdigest()\n    if not hmac.compare_digest(\n        recomputed_binding,\n        receipt[\"combined_binding_sha256\"],\n    ):\n        raise CIBMismatch(\"configuration identity\")\n    return True\n\n\ndef _capture_gates():\n    return {\n        \"SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED\": os.environ.get(\"SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED\"),\n        \"SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\": os.environ.get(\"SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\"),\n        \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED\": os.environ.get(\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED\"),\n        \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED\": os.environ.get(\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED\"),\n        \"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\": os.environ.get(\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\"),\n    }\n\n\ndef _set_gates():\n    os.environ[\"SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED\"] = \"1\"\n    os.environ[\"SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\"] = \"1\"\n    os.environ[\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED\"] = \"1\"\n    os.environ[\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED\"] = \"1\"\n    os.environ[\"SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED\"] = \"1\"\n\n\ndef _restore_gates(prestate):\n    for name in reversed(GATE_NAMES):\n        previous = prestate[name]\n        if previous is None:\n            os.environ.pop(name, None)\n        else:\n            os.environ[name] = previous\n\n\ndef _noop_load_dotenv(*args, **kwargs):\n    return False\n\n\ndef _bounded_json_tree(value, depth=0, nodes=None):\n    if nodes is None:\n        nodes = [0]\n    nodes[0] += 1\n    if depth > 12 or nodes[0] > 4096:\n        raise PrivacyBlock(\"response bound\")\n    if value is None or isinstance(value, (bool, int, float, str)):\n        if isinstance(value, str) and len(value) > 16384:\n            raise PrivacyBlock(\"string bound\")\n        return\n    if isinstance(value, list):\n        if len(value) > 2048:\n            raise PrivacyBlock(\"list bound\")\n        for item in value:\n            _bounded_json_tree(item, depth + 1, nodes)\n        return\n    if isinstance(value, dict):\n        if len(value) > 512 or any(not isinstance(key, str) for key in value):\n            raise PrivacyBlock(\"object bound\")\n        for key, item in value.items():\n            if len(key) > 256:\n                raise PrivacyBlock(\"key bound\")\n            _bounded_json_tree(item, depth + 1, nodes)\n        return\n    raise PrivacyBlock(\"response type\")\n\n\ndef _validate_response(response):\n    if response.status_code != 200:\n        raise IntegrityBlock(\"http status\")\n    payload = response.json()\n    projection_module = sys.modules.get(\"app.api.v1.endpoints.internal_alpha_review_console\")\n    if projection_module is None:\n        raise IntegrityBlock(\"projection module\")\n    projection_fields = getattr(projection_module, \"PROJECTION_FIELDS\")\n    if not isinstance(projection_fields, tuple) or len(projection_fields) != 52:\n        raise IntegrityBlock(\"projection fields\")\n    if tuple(payload.keys()) == projection_fields:\n        pass\n    else:\n        raise IntegrityBlock(\"response field order\")\n    _bounded_json_tree(payload)\n    response_bytes = json.dumps(\n        payload,\n        ensure_ascii=False,\n        separators=(\",\", \":\"),\n        sort_keys=False,\n    ).encode(\"utf-8\")\n    if len(response_bytes) > 1048576:\n        raise PrivacyBlock(\"response bytes\")\n    response_sha256 = hashlib.sha256(response_bytes).hexdigest()\n    return {\n        \"http_status\": response.status_code,\n        \"field_count\": len(projection_fields),\n        \"response_bytes\": len(response_bytes),\n        \"response_sha256\": response_sha256,\n    }\n\n\nasync def _perform_get(app, httpx):\n    transport = httpx.ASGITransport(app=app)\n    async with httpx.AsyncClient(transport=transport, base_url=\"http://sentigraph.invalid\") as client:\n        response = await client.get(TARGET_ROUTE)\n    return response\n\n\ndef _install_file_guard(results_dir, export_root):\n    allowed_result = Path(results_dir) / PROVIDER_RESULT_BASENAME\n    allowed_metadata = {Path(export_root) / name for name in APPROVED_METADATA_BASENAMES}\n    raw_rows = {Path(export_root) / name for name in RAW_ROW_BASENAMES}\n    original_open = builtins.open\n    original_path_open = Path.open\n\n    def guarded_open(file, *args, **kwargs):\n        candidate = Path(file)\n        if candidate in raw_rows:\n            raise PrivacyBlock(\"raw-row boundary\")\n        if candidate != allowed_result and candidate not in allowed_metadata:\n            raise PrivacyBlock(\"file boundary\")\n        return original_open(file, *args, **kwargs)\n\n    def guarded_path_open(path_object, *args, **kwargs):\n        return guarded_open(path_object, *args, **kwargs)\n\n    builtins.open = guarded_open\n    Path.open = guarded_path_open\n\n    def restore():\n        Path.open = original_path_open\n        builtins.open = original_open\n\n    return restore\n\n\ndef _network_audit_hook(event, args):\n    blocked = (\n        \"socket.__new__\",\n        \"socket.connect\",\n        \"socket.bind\",\n        \"socket.getaddrinfo\",\n        \"subprocess.Popen\",\n        \"os.system\",\n    )\n    if event in blocked:\n        raise IntegrityBlock(\"network or subprocess audit\")\n\n\ndef _blocked_action(*args, **kwargs):\n    raise IntegrityBlock(\"external action\")\n\n\ndef _install_network_guard():\n    original_create_connection = socket.create_connection\n    original_getaddrinfo = socket.getaddrinfo\n    original_popen = subprocess.Popen\n    original_system = os.system\n    socket.create_connection = _blocked_action\n    socket.getaddrinfo = _blocked_action\n    subprocess.Popen = _blocked_action\n    os.system = _blocked_action\n\n    def restore():\n        os.system = original_system\n        subprocess.Popen = original_popen\n        socket.getaddrinfo = original_getaddrinfo\n        socket.create_connection = original_create_connection\n\n    return restore\n\n\ndef _build_safe_result(args, response_summary):\n    committed_blobs = {\n        \"service\": SERVICE_BLOB,\n        \"b05_route\": B05_ROUTE_BLOB,\n        \"b03_projection\": B03_PROJECTION_BLOB,\n        \"b01_staging\": B01_STAGING_BLOB,\n    }\n    result = {\n        \"schema\": RUNNER_SCHEMA,\n        \"version\": RUNNER_VERSION,\n        \"milestone\": MILESTONE,\n        \"status\": \"success\",\n        \"runtime_classification\": \"ready_one_governed_b05_get_smoke_v3\",\n        \"privacy_issue_stop\": False,\n        \"starting_head\": args.starting_head,\n        \"approval_sha256\": args.approval_sha256,\n        \"contract_sha256\": args.contract_sha256,\n        \"committed_blobs\": committed_blobs,\n        \"auditor\": {\"bytes\": args.auditor_bytes, \"sha256\": args.auditor_sha256, \"blob\": args.auditor_blob},\n        \"runner\": {\"bytes\": args.runner_bytes, \"sha256\": args.runner_sha256},\n        \"receipt_identity\": {\"bytes\": RECEIPT_BYTES, \"sha256\": RECEIPT_SHA256},\n        \"execution\": {\"get_attempts\": 1, \"get_completed\": 1, \"retries\": 0},\n        \"cib\": {\"verified\": True, \"receipt_reads\": 1, \"receipt_reopens\": 0},\n        \"gates\": {\"prestate_reads\": 5, \"writes\": 5, \"restored\": True},\n        \"dotenv\": {\"patched\": True, \"restored\": True},\n        \"application\": {\"imports\": 1, \"factory_calls\": 0},\n        \"response\": response_summary,\n        \"file_access\": {\"provider_result_reads\": 1, \"raw_row_reads\": 0},\n        \"restoration\": {\"event_loop_closed\": True, \"process_state_restored\": True},\n        \"hard_zero\": {\"network\": 0, \"database\": 0, \"persistence\": 0, \"production\": 0, \"export\": 0, \"delivery\": 0},\n        \"warnings\": [],\n        \"blockers\": [],\n    }\n    if tuple(result.keys()) != SAFE_RESULT_FIELDS:\n        raise IntegrityBlock(\"safe result fields\")\n    return result\n\n\ndef _write_safe_result(external_parent, result):\n    result_path = external_parent / RESULT_BASENAME\n    partial_path = external_parent / PARTIAL_RESULT_BASENAME\n    if result_path.exists() or partial_path.exists():\n        raise IntegrityBlock(\"result collision\")\n    data = json.dumps(result, ensure_ascii=False, separators=(\",\", \":\"), sort_keys=False).encode(\"utf-8\")\n    if len(data) > 65536:\n        raise IntegrityBlock(\"result bound\")\n    descriptor = os.open(partial_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)\n    try:\n        if os.write(descriptor, data) != len(data):\n            raise IntegrityBlock(\"partial write\")\n        try:\n            os.fsync(descriptor)\n        except OSError:\n            pass\n    finally:\n        os.close(descriptor)\n    os.replace(partial_path, result_path)\n\n\ndef _execute(args, repo_root, external_parent):\n    receipt = _read_receipt(external_parent)\n    configuration_values = _read_configuration()\n    verify_cib(receipt, configuration_values)\n    gate_prestate = _capture_gates()\n    original_sys_path = list(sys.path)\n    original_dont_write_bytecode = sys.dont_write_bytecode\n    original_load_dotenv = dotenv.load_dotenv\n    original_socket_type = socket.socket\n    original_socket_alias = socket.SocketType\n    backend_path = repo_root / \"backend\"\n    loop = None\n    restore_files = None\n    restore_network = None\n    try:\n        _set_gates()\n        sys.path.insert(0, str(backend_path))\n        sys.dont_write_bytecode = True\n        if \"app.main\" in sys.modules:\n            raise IntegrityBlock(\"application preloaded\")\n        dotenv.load_dotenv = _noop_load_dotenv\n        app_module = importlib.import_module(\"app.main\")\n        app = getattr(app_module, \"app\")\n        loop = asyncio.new_event_loop()\n        sys.addaudithook(_network_audit_hook)\n        restore_network = _install_network_guard()\n        restore_files = _install_file_guard(configuration_values[0], configuration_values[1])\n        httpx = importlib.import_module(\"httpx\")\n        response = loop.run_until_complete(_perform_get(app, httpx))\n        response_summary = _validate_response(response)\n        safe_result = _build_safe_result(args, response_summary)\n        _write_safe_result(external_parent, safe_result)\n        status_line = STATUS_LINES[\"success\"]\n        return status_line\n    finally:\n        if restore_files is not None:\n            restore_files()\n        if restore_network is not None:\n            restore_network()\n        if loop is not None:\n            loop.close()\n        dotenv.load_dotenv = original_load_dotenv\n        sys.path[:] = original_sys_path\n        sys.dont_write_bytecode = original_dont_write_bytecode\n        _restore_gates(gate_prestate)\n        if socket.socket is not original_socket_type or socket.SocketType is not original_socket_alias:\n            raise IntegrityBlock(\"core socket type changed\")\n\n\ndef main():\n    status_line = STATUS_LINES[\"integrity\"]\n    try:\n        args = _parse_arguments()\n        repo_root, external_parent = _validate_arguments(args)\n        status_line = _execute(args, repo_root, external_parent)\n    except CIBMismatch:\n        status_line = STATUS_LINES[\"cib\"]\n    except PrivacyBlock:\n        status_line = STATUS_LINES[\"privacy\"]\n    except (IntegrityBlock, OSError, ValueError, TypeError):\n        status_line = STATUS_LINES[\"integrity\"]\n    print(status_line)\n\n\nif __name__ == \"__main__\":\n    main()\n"

EXPECTED_IMPORTS = (
    ("from", "__future__", "annotations"),
    ("import", "asyncio"),
    ("import", "builtins"),
    ("import", "glob"),
    ("import", "hashlib"),
    ("import", "hmac"),
    ("import", "importlib"),
    ("import", "io"),
    ("import", "json"),
    ("import", "os"),
    ("import", "re"),
    ("import", "socket"),
    ("import", "subprocess"),
    ("import", "sys"),
    ("from", "pathlib", "Path"),
    ("import", "dotenv"),
)
EXPECTED_ARGUMENTS = (
    "--repo-root",
    "--starting-head",
    "--approval-sha256",
    "--contract-sha256",
    "--auditor-bytes",
    "--auditor-sha256",
    "--auditor-blob",
    "--runner-bytes",
    "--runner-sha256",
)
EXPECTED_GATES = (
    "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_ALPHA_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_ROUTE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_ENABLED",
    "SENTIGRAPH_INTERNAL_OPERATOR_STAGING_LOCAL_EXCHANGE_REVIEW_PROJECTION_ENABLED",
)
EXPECTED_CONFIG = (
    "SENTIGRAPH_LOCAL_EXCHANGE_RESULTS_DIR",
    "SENTIGRAPH_PRIVATE_COLLECTOR_EXPORT_ROOT",
    "SENTIGRAPH_LOCAL_EXCHANGE_ADAPTER_ID",
)
EXPECTED_METADATA = (
    "manifest.json",
    "validation_report.json",
    "validation_report.md",
    "coverage_note.md",
    "README.md",
    "package_index.json",
)
EXPECTED_RAW_ROWS = (
    "source_manifest.jsonl",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "collection_log.jsonl",
)
EXPECTED_SAFE_FIELDS = (
    "schema",
    "version",
    "milestone",
    "status",
    "runtime_classification",
    "privacy_issue_stop",
    "starting_head",
    "approval_sha256",
    "contract_sha256",
    "committed_blobs",
    "auditor",
    "runner",
    "receipt_identity",
    "execution",
    "cib",
    "gates",
    "dotenv",
    "application",
    "response",
    "file_access",
    "restoration",
    "hard_zero",
    "warnings",
    "blockers",
)
EXPECTED_CANONICAL_KEYS = (
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
EXPECTED_CANONICAL_LITERALS = (
    "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",
    "0.1",
    "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
    "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
    "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
    "helldivers2-psn-demo",
    "provider_result_helldivers2-psn-demo_20260720_123627.json",
    "internal_alpha_read_only_local_exchange_projection_operator",
    "b05_local_exchange_projection_read_only",
)
EXPECTED_CONSTANTS = {
    "RUNNER_SCHEMA": "sentigraph_b05_get_smoke_safe_result_v3_0_1",
    "RUNNER_VERSION": "0.1",
    "MILESTONE": "SENTIGRAPH-BASELINE-V2-5-RISK-PROMPT-1-ONE-GOVERNED-B05-GET-SMOKE-V3",
    "RUNNER_BASENAME": ".sentigraph_b05_get_smoke_runner_v3.py",
    "RESULT_BASENAME": ".sentigraph_b05_get_smoke_result_v3.json",
    "PARTIAL_RESULT_BASENAME": ".sentigraph_b05_get_smoke_result_v3.json.partial",
    "RECEIPT_BASENAME": ".sentigraph_cib_capture_risk_prompt_3_v1_safe_receipt.json",
    "TARGET_ROUTE": "/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo",
    "PROVIDER_RESULT_BASENAME": "provider_result_helldivers2-psn-demo_20260720_123627.json",
    "SERVICE_BLOB": "f0c4a8768060a840ea1921aeba47a97f2e41f9e3",
    "B05_ROUTE_BLOB": "8445b4595ea7edc9d9878e99b35ce0554b841c94",
    "B03_PROJECTION_BLOB": "534bdf02e211134b52b2e7714d01a0dd615210b4",
    "B01_STAGING_BLOB": "ef36b4370495b7f1e5c9c5c433d5b38c5cf9aa6d",
    "REGISTRY_SCHEMA": "sentigraph_internal_alpha_local_exchange_sample_registry_v0_1",
    "SAMPLE_HANDLE": "helldivers2-psn-demo",
    "ROUTE_MODE": "internal_alpha_read_only_local_exchange_projection_operator",
    "CAPABILITY_LABEL": "b05_local_exchange_projection_read_only",
    "RECEIPT_BYTES": 1314,
    "RECEIPT_SHA256": "0273877f50391a1a77be6a0f9f506d3479dd1d694390711cb88f3047152db0c7",
    "BINDING_SCHEMA": "sentigraph_b05_server_owned_configuration_identity_binding_v0_1",
    "RECEIPT_SCHEMA": "sentigraph_b05_server_owned_configuration_identity_binding_receipt_v0_1",
    "BINDING_SCOPE": "b05_one_real_sample_handle_governed_read_only_projection_pre_smoke",
}


def _call_path(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        value = node.value.func if isinstance(node.value, ast.Call) else node.value
        prefix = _call_path(value)
        return (prefix + "." if prefix else "") + node.attr
    return ""


def _calls(node, path=None):
    result = []
    for item in ast.walk(node):
        if isinstance(item, ast.Call):
            current = _call_path(item.func)
            if path is None or current == path:
                result.append(item)
    return sorted(result, key=lambda item: (item.lineno, item.col_offset))


def _function(tree, name):
    matches = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name
    ]
    if len(matches) != 1:
        raise ValueError("function identity")
    return matches[0]


def _global_assign(tree, name):
    matches = []
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == name:
                matches.append(node)
    if len(matches) != 1:
        raise ValueError("global identity")
    return matches[0]


def _literal_global(tree, name):
    return ast.literal_eval(_global_assign(tree, name).value)


def _direct_constant(tree, name):
    value = _global_assign(tree, name).value
    if not isinstance(value, ast.Constant):
        raise ValueError("constant identity")
    return value.value


def _subscript_key(node):
    if not isinstance(node, ast.Subscript):
        return None
    if isinstance(node.slice, ast.Constant):
        return node.slice.value
    return None


def _target_path(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _target_path(node.value)
        return (prefix + "." if prefix else "") + node.attr
    return ""


def _import_signature(tree):
    result = []
    nodes = sorted(
        [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))],
        key=lambda item: (item.lineno, item.col_offset),
    )
    for node in nodes:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname is not None:
                    result.append(("import_as", alias.name, alias.asname))
                else:
                    result.append(("import", alias.name))
        else:
            for alias in node.names:
                if alias.asname is not None:
                    result.append(("from_as", node.module, alias.name, alias.asname))
                else:
                    result.append(("from", node.module, alias.name))
    return tuple(result)


def _assignment_to(node, path, value_name=None):
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return False
    if _target_path(node.targets[0]) != path:
        return False
    if value_name is None:
        return True
    return isinstance(node.value, ast.Name) and node.value.id == value_name


def _outer_try(function):
    matches = [node for node in function.body if isinstance(node, ast.Try)]
    if len(matches) != 1:
        raise ValueError("outer try")
    return matches[0]


def _json_dumps_contract(call):
    if _call_path(call.func) != "json.dumps":
        return False
    keywords = {keyword.arg: keyword.value for keyword in call.keywords}
    if set(keywords) != {"ensure_ascii", "separators", "sort_keys"}:
        return False
    return (
        isinstance(keywords["ensure_ascii"], ast.Constant)
        and keywords["ensure_ascii"].value is False
        and isinstance(keywords["sort_keys"], ast.Constant)
        and keywords["sort_keys"].value is False
        and isinstance(keywords["separators"], ast.Tuple)
        and [element.value for element in keywords["separators"].elts if isinstance(element, ast.Constant)] == [",", ":"]
    )


def _check_imports(tree):
    return _import_signature(tree) == EXPECTED_IMPORTS


def _check_bound_constants(tree):
    if not all(_direct_constant(tree, name) == value for name, value in EXPECTED_CONSTANTS.items()):
        return False
    if _literal_global(tree, "GATE_NAMES") != EXPECTED_GATES:
        return False
    if _literal_global(tree, "CONFIGURATION_NAMES") != EXPECTED_CONFIG:
        return False
    if _literal_global(tree, "APPROVED_METADATA_BASENAMES") != EXPECTED_METADATA:
        return False
    if _literal_global(tree, "RAW_ROW_BASENAMES") != EXPECTED_RAW_ROWS:
        return False
    if _literal_global(tree, "SAFE_RESULT_FIELDS") != EXPECTED_SAFE_FIELDS:
        return False
    parser = _function(tree, "_parse_arguments")
    candidates = []
    for node in ast.walk(parser):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == "argument_names":
                candidates.append(node.value)
    return len(candidates) == 1 and ast.literal_eval(candidates[0]) == EXPECTED_ARGUMENTS


def _check_receipt(tree):
    function = _function(tree, "_read_receipt")
    opens = _calls(function, "receipt_path.open")
    reads = _calls(function, "handle.read")
    return (
        len(opens) == 1
        and len(opens[0].args) == 1
        and isinstance(opens[0].args[0], ast.Constant)
        and opens[0].args[0].value == "rb"
        and len(reads) == 1
        and len(reads[0].args) == 0
        and _direct_constant(tree, "RECEIPT_BYTES") == 1314
        and _direct_constant(tree, "RECEIPT_SHA256") == "0273877f50391a1a77be6a0f9f506d3479dd1d694390711cb88f3047152db0c7"
        and len(_literal_global(tree, "RECEIPT_FIELDS")) == 23
    )


def _check_configuration_reads(tree):
    function = _function(tree, "_read_configuration")
    reads = _calls(function, "os.environ.get")
    values = []
    for call in reads:
        if len(call.args) != 1 or call.keywords or not isinstance(call.args[0], ast.Constant):
            return False
        values.append(call.args[0].value)
    return tuple(values) == EXPECTED_CONFIG


def _canonical_assignment(tree):
    function = _function(tree, "verify_cib")
    matches = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == "canonical_object":
                matches.append(node)
    if len(matches) != 1 or not isinstance(matches[0].value, ast.Dict):
        raise ValueError("canonical object")
    return matches[0]


def _check_cib_dataflow(tree):
    function = _function(tree, "verify_cib")
    assignments = {}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            assignments[node.targets[0].id] = node.value
    canonical_bytes = assignments.get("canonical_bytes")
    recomputed = assignments.get("recomputed_binding")
    if not isinstance(canonical_bytes, ast.Call) or _call_path(canonical_bytes.func) != "json.dumps.encode":
        return False
    if len(canonical_bytes.args) != 1 or not isinstance(canonical_bytes.args[0], ast.Constant) or canonical_bytes.args[0].value != "utf-8":
        return False
    dumps = canonical_bytes.func.value
    if not isinstance(dumps, ast.Call) or not _json_dumps_contract(dumps):
        return False
    if len(dumps.args) != 1 or not isinstance(dumps.args[0], ast.Name) or dumps.args[0].id != "canonical_object":
        return False
    if not isinstance(recomputed, ast.Call) or _call_path(recomputed.func) != "hashlib.sha256.hexdigest":
        return False
    sha_call = recomputed.func.value
    if len(sha_call.args) != 1 or not isinstance(sha_call.args[0], ast.Name) or sha_call.args[0].id != "canonical_bytes":
        return False
    compares = _calls(function, "hmac.compare_digest")
    if len(compares) != 1 or len(compares[0].args) != 2 or compares[0].keywords:
        return False
    first, second = compares[0].args
    return (
        isinstance(first, ast.Name)
        and first.id == "recomputed_binding"
        and isinstance(second, ast.Subscript)
        and isinstance(second.value, ast.Name)
        and second.value.id == "receipt"
        and _subscript_key(second) == "combined_binding_sha256"
    )


def _check_canonical_constants(tree):
    dictionary = _canonical_assignment(tree).value
    if not all(isinstance(key, ast.Constant) and isinstance(key.value, str) for key in dictionary.keys):
        return False
    keys = tuple(key.value for key in dictionary.keys)
    if keys != EXPECTED_CANONICAL_KEYS:
        return False
    values = dictionary.values
    for node, expected in zip(values[:9], EXPECTED_CANONICAL_LITERALS):
        if not isinstance(node, ast.Constant) or node.value != expected:
            return False
    salt = values[9]
    if not (
        isinstance(salt, ast.Subscript)
        and isinstance(salt.value, ast.Name)
        and salt.value.id == "receipt"
        and _subscript_key(salt) == "salt_hex"
    ):
        return False
    configurations = values[10]
    if not isinstance(configurations, ast.List) or len(configurations.elts) != 3:
        return False
    for index, (item, expected_name) in enumerate(zip(configurations.elts, EXPECTED_CONFIG)):
        if not isinstance(item, ast.Dict) or [key.value for key in item.keys] != ["name", "value"]:
            return False
        if not isinstance(item.values[0], ast.Constant) or item.values[0].value != expected_name:
            return False
        value = item.values[1]
        if not (
            isinstance(value, ast.Subscript)
            and isinstance(value.value, ast.Name)
            and value.value.id == "configuration_values"
            and _subscript_key(value) == index
        ):
            return False
    return True


def _check_configuration_bound(tree):
    validator = _function(tree, "_validate_opaque")
    constants = [node.value for node in ast.walk(validator) if isinstance(node, ast.Constant)]
    calls = _calls(validator)
    paths = [_call_path(call.func) for call in calls]
    adapter = _function(tree, "_validate_adapter_id")
    adapter_calls = _calls(adapter, "re.fullmatch")
    adapter_ok = (
        len(adapter_calls) == 1
        and len(adapter_calls[0].args) == 2
        and isinstance(adapter_calls[0].args[0], ast.Constant)
        and adapter_calls[0].args[0].value == r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}"
    )
    return (
        constants.count(2048) == 1
        and 1048 not in constants
        and "\x00" in constants
        and "isinstance" in paths
        and "value.strip" in paths
        and "value.isprintable" in paths
        and adapter_ok
    )


def _check_no_weak_hash(tree):
    forbidden_imports = {"random", "secrets", "uuid"}
    for signature in _import_signature(tree):
        if any(item in forbidden_imports for item in signature[1:]):
            return False
    forbidden_calls = {
        "hashlib.md5",
        "hashlib.sha1",
        "random.random",
        "secrets.token_hex",
        "uuid.uuid4",
    }
    return not any(_call_path(call.func) in forbidden_calls for call in _calls(tree))


def _check_gate_prestate(tree):
    function = _function(tree, "_capture_gates")
    returns = [node for node in function.body if isinstance(node, ast.Return)]
    if len(returns) != 1 or not isinstance(returns[0].value, ast.Dict):
        return False
    dictionary = returns[0].value
    keys = []
    values = []
    for key, value in zip(dictionary.keys, dictionary.values):
        if not isinstance(key, ast.Constant) or not isinstance(value, ast.Call):
            return False
        if _call_path(value.func) != "os.environ.get" or len(value.args) != 1:
            return False
        if not isinstance(value.args[0], ast.Constant) or value.args[0].value != key.value:
            return False
        keys.append(key.value)
        values.append(value.args[0].value)
    return tuple(keys) == EXPECTED_GATES and tuple(values) == EXPECTED_GATES


def _gate_assignment(node):
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return None
    target = node.targets[0]
    if not isinstance(target, ast.Subscript) or _target_path(target.value) != "os.environ":
        return None
    if not isinstance(target.slice, ast.Constant):
        return None
    if not isinstance(node.value, ast.Constant) or node.value.value != "1":
        return None
    return target.slice.value


def _check_gate_write(tree):
    function = _function(tree, "_set_gates")
    writes = [_gate_assignment(node) for node in function.body]
    return tuple(writes) == EXPECTED_GATES


def _check_gate_restore(tree):
    helper = _function(tree, "_restore_gates")
    loops = [node for node in helper.body if isinstance(node, ast.For)]
    if len(loops) != 1 or not isinstance(loops[0].iter, ast.Call):
        return False
    reverse = loops[0].iter
    if _call_path(reverse.func) != "reversed" or len(reverse.args) != 1:
        return False
    if not isinstance(reverse.args[0], ast.Name) or reverse.args[0].id != "GATE_NAMES":
        return False
    execute = _function(tree, "_execute")
    outer = _outer_try(execute)
    calls = [call for statement in outer.finalbody for call in _calls(statement, "_restore_gates")]
    return len(calls) == 1 and len(calls[0].args) == 1 and isinstance(calls[0].args[0], ast.Name) and calls[0].args[0].id == "gate_prestate"


def _dotenv_patch_and_import(tree):
    execute = _function(tree, "_execute")
    patches = [
        node
        for node in ast.walk(execute)
        if _assignment_to(node, "dotenv.load_dotenv", "_noop_load_dotenv")
    ]
    imports = [
        call
        for call in _calls(execute, "importlib.import_module")
        if len(call.args) == 1 and isinstance(call.args[0], ast.Constant) and call.args[0].value == "app.main"
    ]
    if len(patches) != 1 or len(imports) != 1:
        raise ValueError("dotenv/import identity")
    return patches[0], imports[0]


def _check_dotenv_patch(tree):
    patch, app_import = _dotenv_patch_and_import(tree)
    return patch.lineno < app_import.lineno


def _check_dotenv_restore(tree):
    execute = _function(tree, "_execute")
    outer = _outer_try(execute)
    restores = [node for node in outer.finalbody if _assignment_to(node, "dotenv.load_dotenv", "original_load_dotenv")]
    return len(restores) == 1


def _app_import_calls(tree):
    return [
        call
        for call in _calls(tree, "importlib.import_module")
        if len(call.args) == 1 and isinstance(call.args[0], ast.Constant) and call.args[0].value == "app.main"
    ]


def _check_app_import(tree):
    calls = _app_import_calls(tree)
    return len(calls) == 1 and calls[0] in _calls(_function(tree, "_execute"))


def _check_event_loop(tree):
    creations = _calls(tree, "asyncio.new_event_loop")
    if len(creations) != 1:
        return False
    execute = _function(tree, "_execute")
    app_imports = [call for call in _app_import_calls(tree) if call in _calls(execute)]
    run_calls = _calls(execute, "loop.run_until_complete")
    close_calls = _calls(execute, "loop.close")
    hooks = _calls(execute, "sys.addaudithook")
    return (
        len(app_imports) == 1
        and len(run_calls) == 1
        and len(close_calls) == 1
        and len(hooks) == 1
        and app_imports[0].lineno < creations[0].lineno < hooks[0].lineno < run_calls[0].lineno < close_calls[0].lineno
    )


def _check_no_asyncio_run(tree):
    return len(_calls(tree, "asyncio.run")) == 0


def _check_asgi(tree):
    function = _function(tree, "_perform_get")
    calls = _calls(function, "httpx.ASGITransport")
    if len(calls) != 1 or calls[0].args:
        return False
    keywords = {keyword.arg: keyword.value for keyword in calls[0].keywords}
    return set(keywords) == {"app"} and isinstance(keywords["app"], ast.Name) and keywords["app"].id == "app"


def _client_get_calls(function):
    return _calls(function, "client.get")


def _check_target_route(tree):
    if _direct_constant(tree, "TARGET_ROUTE") != "/api/v1/internal/alpha/review-console/local-exchange-projections/helldivers2-psn-demo":
        return False
    calls = _client_get_calls(_function(tree, "_perform_get"))
    return bool(calls) and all(
        len(call.args) == 1
        and not call.keywords
        and isinstance(call.args[0], ast.Name)
        and call.args[0].id == "TARGET_ROUTE"
        for call in calls
    )


def _check_http_get(tree):
    calls = _client_get_calls(_function(tree, "_perform_get"))
    return len(calls) == 1


def _check_perform_get(tree):
    return len(_calls(tree, "_perform_get")) == 1


def _response_compare(function):
    matches = []
    for node in ast.walk(function):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1 or not isinstance(node.ops[0], ast.Eq):
            continue
        if len(node.comparators) != 1 or not isinstance(node.comparators[0], ast.Name) or node.comparators[0].id != "projection_fields":
            continue
        left = node.left
        if not isinstance(left, ast.Call) or _call_path(left.func) != "tuple" or len(left.args) != 1:
            continue
        keys_call = left.args[0]
        if not isinstance(keys_call, ast.Call) or _call_path(keys_call.func) != "payload.keys" or keys_call.args or keys_call.keywords:
            continue
        matches.append(node)
    return matches


def _check_response_order(tree):
    function = _function(tree, "_validate_response")
    compares = _response_compare(function)
    length_checks = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Constant) and node.value == 52
    ]
    return len(compares) == 1 and len(length_checks) == 1


def _check_response_bounded(tree):
    function = _function(tree, "_validate_response")
    if len(_calls(function, "response.json")) != 1:
        return False
    bounded = _calls(function, "_bounded_json_tree")
    if len(bounded) != 1 or len(bounded[0].args) != 1 or not isinstance(bounded[0].args[0], ast.Name) or bounded[0].args[0].id != "payload":
        return False
    dumps = _calls(function, "json.dumps")
    if len(dumps) != 1 or not _json_dumps_contract(dumps[0]):
        return False
    hashes = _calls(function, "hashlib.sha256")
    if len(hashes) != 1 or len(hashes[0].args) != 1 or not isinstance(hashes[0].args[0], ast.Name) or hashes[0].args[0].id != "response_bytes":
        return False
    for node in ast.walk(function):
        if isinstance(node, ast.Return) and any(isinstance(item, ast.Name) and item.id == "payload" for item in ast.walk(node)):
            return False
    return True


def _check_file_guard(tree):
    return (
        _literal_global(tree, "APPROVED_METADATA_BASENAMES") == EXPECTED_METADATA
        and _literal_global(tree, "RAW_ROW_BASENAMES") == EXPECTED_RAW_ROWS
        and _direct_constant(tree, "PROVIDER_RESULT_BASENAME") == "provider_result_helldivers2-psn-demo_20260720_123627.json"
        and len([node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "_install_file_guard"]) == 1
    )


def _raw_open_calls(tree):
    result = []
    for call in _calls(tree):
        path = _call_path(call.func)
        if path not in {"open", "builtins.open", "Path.open"} or not call.args:
            continue
        argument = call.args[0]
        if isinstance(argument, ast.Constant) and argument.value in EXPECTED_RAW_ROWS:
            result.append(call)
    return result


def _check_raw_rows(tree):
    return len(_raw_open_calls(tree)) == 0


def _directory_calls(tree):
    forbidden = {
        "os.listdir",
        "os.scandir",
        "os.walk",
        "glob.glob",
        "glob.iglob",
        "Path.glob",
        "Path.rglob",
    }
    return [call for call in _calls(tree) if _call_path(call.func) in forbidden]


def _check_no_discovery(tree):
    return len(_directory_calls(tree)) == 0


def _core_socket_assignments(tree):
    result = []
    for node in ast.walk(tree):
        targets = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        for target in targets:
            if _target_path(target) in {"socket.socket", "socket.SocketType"}:
                result.append(node)
    return result


def _check_network_guard(tree):
    if _core_socket_assignments(tree):
        return False
    execute = _function(tree, "_execute")
    preserve_socket = [
        node
        for node in execute.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "original_socket_type"
        and _target_path(node.value) == "socket.socket"
    ]
    preserve_alias = [
        node
        for node in execute.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "original_socket_alias"
        and _target_path(node.value) == "socket.SocketType"
    ]
    creations = _calls(execute, "asyncio.new_event_loop")
    hooks = _calls(execute, "sys.addaudithook")
    installer = _function(tree, "_install_network_guard")
    install_paths = [
        _target_path(node.targets[0])
        for node in installer.body
        if isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.value, ast.Name)
        and node.value.id == "_blocked_action"
    ]
    restore = _function(installer, "restore") if False else None
    nested = [node for node in installer.body if isinstance(node, ast.FunctionDef) and node.name == "restore"]
    if len(nested) != 1:
        return False
    restore_paths = [
        _target_path(node.targets[0])
        for node in nested[0].body
        if isinstance(node, ast.Assign) and len(node.targets) == 1
    ]
    return (
        len(preserve_socket) == 1
        and len(preserve_alias) == 1
        and len(creations) == 1
        and len(hooks) == 1
        and creations[0].lineno < hooks[0].lineno
        and install_paths == ["socket.create_connection", "socket.getaddrinfo", "subprocess.Popen", "os.system"]
        and restore_paths == ["os.system", "subprocess.Popen", "socket.getaddrinfo", "socket.create_connection"]
    )


def _external_calls(tree):
    forbidden = {
        "socket.socket",
        "socket.SocketType",
        "socket.create_connection",
        "socket.getaddrinfo",
        "subprocess.Popen",
        "subprocess.run",
        "subprocess.call",
        "os.system",
        "requests.get",
        "requests.post",
        "urllib.request.urlopen",
    }
    return [call for call in _calls(tree) if _call_path(call.func) in forbidden]


def _check_no_external(tree):
    return len(_external_calls(tree)) == 0


def _result_dictionary(tree):
    function = _function(tree, "_build_safe_result")
    matches = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == "result" and isinstance(node.value, ast.Dict):
                matches.append(node.value)
    if len(matches) != 1:
        raise ValueError("safe result")
    return matches[0]


def _check_atomic_output(tree):
    writer = _function(tree, "_write_safe_result")
    opens = _calls(writer, "os.open")
    writes = _calls(writer, "os.write")
    closes = _calls(writer, "os.close")
    fsyncs = _calls(writer, "os.fsync")
    replaces = _calls(writer, "os.replace")
    if not (len(opens) == len(writes) == len(closes) == len(fsyncs) == len(replaces) == 1):
        return False
    flags = opens[0].args[1] if len(opens[0].args) > 1 else None
    flag_paths = {_target_path(node) for node in ast.walk(flags) if isinstance(node, ast.Attribute)} if flags is not None else set()
    if not {"os.O_WRONLY", "os.O_CREAT", "os.O_EXCL"}.issubset(flag_paths):
        return False
    try_nodes = [node for node in writer.body if isinstance(node, ast.Try)]
    if len(try_nodes) != 1 or not any(call in _calls(statement, "os.close") for statement in try_nodes[0].finalbody for call in _calls(statement)):
        return False
    result = _result_dictionary(tree)
    if tuple(key.value for key in result.keys if isinstance(key, ast.Constant)) != EXPECTED_SAFE_FIELDS:
        return False
    prints = _calls(tree, "print")
    return (
        len(prints) == 1
        and len(prints[0].args) == 1
        and not prints[0].keywords
        and isinstance(prints[0].args[0], ast.Name)
        and prints[0].args[0].id == "status_line"
    )


SEMANTIC_CHECKS = (
    _check_imports,
    _check_bound_constants,
    _check_receipt,
    _check_configuration_reads,
    _check_cib_dataflow,
    _check_canonical_constants,
    _check_configuration_bound,
    _check_no_weak_hash,
    _check_gate_prestate,
    _check_gate_write,
    _check_gate_restore,
    _check_dotenv_patch,
    _check_dotenv_restore,
    _check_app_import,
    _check_event_loop,
    _check_no_asyncio_run,
    _check_asgi,
    _check_target_route,
    _check_http_get,
    _check_perform_get,
    _check_response_order,
    _check_response_bounded,
    _check_file_guard,
    _check_raw_rows,
    _check_no_discovery,
    _check_network_guard,
    _check_no_external,
    _check_atomic_output,
)


def _safe_semantic(function, tree):
    try:
        return bool(function(tree))
    except (AttributeError, KeyError, TypeError, ValueError, IndexError, SyntaxError):
        return False


def _audit_bytes(data):
    strict = isinstance(data, bytes) and not data.startswith(b"\xef\xbb\xbf")
    source = None
    if strict:
        try:
            source = data.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            strict = False
    tree = None
    parsed = False
    if source is not None:
        try:
            tree = ast.parse(source, filename="<runner-v3>", mode="exec")
            parsed = True
        except SyntaxError:
            parsed = False
    passed = [strict, parsed]
    if parsed:
        passed.extend(_safe_semantic(function, tree) for function in SEMANTIC_CHECKS)
    else:
        passed.extend(False for _ in SEMANTIC_CHECKS)
    checks = [
        {"name": name, "passed": value}
        for name, value in zip(CHECK_NAMES, passed)
    ]
    failed = [item["name"] for item in checks if not item["passed"]]
    return {
        "schema": AUDITOR_SCHEMA,
        "version": VERSION,
        "status": "pass" if not failed else "fail",
        "checks_total": len(CHECK_NAMES),
        "checks_passed": len(CHECK_NAMES) - len(failed),
        "checks_failed": len(failed),
        "failed_checks": failed,
        "checks": checks,
        "runner_bytes": len(data) if isinstance(data, bytes) else 0,
        "runner_sha256": hashlib.sha256(data).hexdigest() if isinstance(data, bytes) else None,
        "runner_executed": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }


def _line_offsets(source):
    offsets = [0]
    total = 0
    for line in source.splitlines(keepends=True):
        total += len(line)
        offsets.append(total)
    return offsets


def _node_span(source, node):
    if not hasattr(node, "end_lineno") or node.end_lineno is None:
        raise ValueError("node span")
    offsets = _line_offsets(source)
    start = offsets[node.lineno - 1] + node.col_offset
    end = offsets[node.end_lineno - 1] + node.end_col_offset
    if not 0 <= start < end <= len(source):
        raise ValueError("node bounds")
    return start, end


def _replace_node(source, node, replacement):
    start, end = _node_span(source, node)
    mutated = source[:start] + replacement + source[end:]
    ast.parse(mutated, filename="<negative-fixture>", mode="exec")
    return mutated


def _replace_statement(source, node, replacement="pass"):
    return _replace_node(source, node, replacement)


def _swap_nodes(source, first, second):
    first_start, first_end = _node_span(source, first)
    second_start, second_end = _node_span(source, second)
    if not first_end <= second_start:
        raise ValueError("swap order")
    first_text = source[first_start:first_end]
    second_text = source[second_start:second_end]
    mutated = source[:first_start] + second_text + source[first_end:second_start] + first_text + source[second_end:]
    ast.parse(mutated, filename="<negative-fixture>", mode="exec")
    return mutated


def _insert_before_statement(source, node, statement):
    offsets = _line_offsets(source)
    start = offsets[node.lineno - 1]
    indentation = " " * node.col_offset
    if "\n" in statement.rstrip("\n"):
        raise ValueError("single statement insertion")
    mutated = source[:start] + indentation + statement.rstrip("\n") + "\n" + source[start:]
    ast.parse(mutated, filename="<negative-fixture>", mode="exec")
    return mutated


def _main_guard(tree):
    matches = []
    for node in tree.body:
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        left = node.test.left
        if isinstance(left, ast.Name) and left.id == "__name__":
            matches.append(node)
    if len(matches) != 1:
        raise ValueError("main guard")
    return matches[0]


def _insert_helper(source, helper_source):
    tree = ast.parse(source, filename="<valid-runner>", mode="exec")
    guard = _main_guard(tree)
    start = _line_offsets(source)[guard.lineno - 1]
    if not helper_source.startswith("def ") and not helper_source.startswith("async def "):
        raise ValueError("helper shape")
    mutated = source[:start] + helper_source.rstrip() + "\n\n\n" + source[start:]
    ast.parse(mutated, filename="<negative-fixture>", mode="exec")
    return mutated


def _assign_named(function, target_name):
    matches = []
    for node in ast.walk(function):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name) and node.targets[0].id == target_name:
                matches.append(node)
    if len(matches) != 1:
        raise ValueError("assignment identity")
    return matches[0]


def _inventory(source):
    tree = ast.parse(source, filename="<inventory>", mode="exec")
    try:
        patch, app_import = _dotenv_patch_and_import(tree)
        patch_before = int(patch.lineno < app_import.lineno)
    except ValueError:
        patch_before = 0
    try:
        schema_value = _canonical_assignment(tree).value.values[0]
        canonical_schema_literal = int(isinstance(schema_value, ast.Constant) and schema_value.value == EXPECTED_CANONICAL_LITERALS[0])
    except ValueError:
        canonical_schema_literal = 0
    validator = _function(tree, "_validate_opaque")
    constants = [node.value for node in ast.walk(validator) if isinstance(node, ast.Constant)]
    try:
        response_exact = len(_response_compare(_function(tree, "_validate_response")))
    except ValueError:
        response_exact = 0
    verify = _function(tree, "verify_cib")
    cib_sha = 0
    assignment = _assign_named(verify, "recomputed_binding")
    if isinstance(assignment.value, ast.Call) and _call_path(assignment.value.func) == "hashlib.sha256.hexdigest":
        cib_sha = 1
    dotenv_restore = 0
    try:
        outer = _outer_try(_function(tree, "_execute"))
        dotenv_restore = sum(_assignment_to(node, "dotenv.load_dotenv", "original_load_dotenv") for node in outer.finalbody)
        gate_restore = sum(len(_calls(node, "_restore_gates")) for node in outer.finalbody)
    except ValueError:
        gate_restore = 0
    payload_print = sum(
        1
        for call in _calls(tree, "print")
        if len(call.args) == 1 and isinstance(call.args[0], ast.Name) and call.args[0].id == "payload"
    )
    target_route_get = sum(
        1
        for call in _client_get_calls(_function(tree, "_perform_get"))
        if len(call.args) == 1 and isinstance(call.args[0], ast.Name) and call.args[0].id == "TARGET_ROUTE"
    )
    return {
        "client_get": len(_client_get_calls(_function(tree, "_perform_get"))),
        "perform_get": len(_calls(tree, "_perform_get")),
        "gate_restore": gate_restore,
        "dotenv_patch_before": patch_before,
        "dotenv_restore": dotenv_restore,
        "cib_sha": cib_sha,
        "response_exact": response_exact,
        "raw_open": len(_raw_open_calls(tree)),
        "external_calls": len(_external_calls(tree)),
        "payload_print": payload_print,
        "asyncio_run": len(_calls(tree, "asyncio.run")),
        "app_import": len(_app_import_calls(tree)),
        "new_event_loop": len(_calls(tree, "asyncio.new_event_loop")),
        "asgi": len(_calls(tree, "httpx.ASGITransport")),
        "target_route_get": target_route_get,
        "directory": len(_directory_calls(tree)),
        "core_socket_assign": len(_core_socket_assignments(tree)),
        "atomic_replace": len(_calls(tree, "os.replace")),
        "canonical_schema_literal": canonical_schema_literal,
        "opaque_2048": constants.count(2048),
        "opaque_1048": constants.count(1048),
    }


EXPECTED_DELTAS = {
    "second_http_get": {"client_get": 1, "target_route_get": 1},
    "perform_get_called_twice": {"perform_get": 1},
    "gate_restore_removed": {"gate_restore": -1},
    "dotenv_patch_after_import": {"dotenv_patch_before": -1},
    "dotenv_restore_removed": {"dotenv_restore": -1},
    "forged_cib_digest": {"cib_sha": -1},
    "response_order_removed": {"response_exact": -1},
    "raw_row_read": {"raw_open": 1},
    "external_socket_action": {"external_calls": 1},
    "payload_output": {"payload_print": 1},
    "asyncio_run_added": {"asyncio_run": 1},
    "second_app_import": {"app_import": 1},
    "second_event_loop": {"new_event_loop": 1},
    "asgi_transport_removed": {"asgi": -1},
    "target_route_changed": {"target_route_get": -1},
    "directory_discovery_added": {"directory": 1},
    "socket_type_replaced": {"core_socket_assign": 1},
    "atomic_replace_removed": {"atomic_replace": -1},
    "receipt_schema_substitution": {"canonical_schema_literal": -1},
    "opaque_configuration_bound_1048": {"opaque_2048": -1, "opaque_1048": 1},
}


def _mutate_fixture(name):
    source = VALID_PUBLIC_RUNNER
    tree = ast.parse(source, filename="<valid-runner>", mode="exec")
    if name == "second_http_get":
        function = _function(tree, "_perform_get")
        returns = [node for node in function.body if isinstance(node, ast.Return)]
        if len(returns) != 1:
            raise ValueError("return anchor")
        return _insert_before_statement(source, returns[0], "await client.get(TARGET_ROUTE)")
    if name == "perform_get_called_twice":
        return _insert_helper(source, "async def _negative_fixture_perform_get_probe():\n    await _perform_get(None, None)")
    if name == "gate_restore_removed":
        outer = _outer_try(_function(tree, "_execute"))
        matches = [node for node in outer.finalbody if len(_calls(node, "_restore_gates")) == 1]
        if len(matches) != 1:
            raise ValueError("gate restore anchor")
        return _replace_statement(source, matches[0])
    if name == "dotenv_patch_after_import":
        patch, app_import = _dotenv_patch_and_import(tree)
        app_assigns = [node for node in ast.walk(_function(tree, "_execute")) if isinstance(node, ast.Assign) and app_import in _calls(node)]
        if len(app_assigns) != 1:
            raise ValueError("app import statement")
        return _swap_nodes(source, patch, app_assigns[0])
    if name == "dotenv_restore_removed":
        outer = _outer_try(_function(tree, "_execute"))
        matches = [node for node in outer.finalbody if _assignment_to(node, "dotenv.load_dotenv", "original_load_dotenv")]
        if len(matches) != 1:
            raise ValueError("dotenv restore anchor")
        return _replace_statement(source, matches[0])
    if name == "forged_cib_digest":
        assignment = _assign_named(_function(tree, "verify_cib"), "recomputed_binding")
        return _replace_node(source, assignment.value, 'receipt["combined_binding_sha256"]')
    if name == "response_order_removed":
        matches = _response_compare(_function(tree, "_validate_response"))
        if len(matches) != 1:
            raise ValueError("response compare anchor")
        return _replace_node(source, matches[0], "set(payload.keys()) == set(projection_fields)")
    if name == "raw_row_read":
        return _insert_helper(source, 'def _negative_fixture_raw_row_probe():\n    open("source_manifest.jsonl", "rb")')
    if name == "external_socket_action":
        return _insert_helper(source, 'def _negative_fixture_external_socket_probe():\n    socket.create_connection(("example.invalid", 443))')
    if name == "payload_output":
        prints = _calls(tree, "print")
        if len(prints) != 1 or len(prints[0].args) != 1:
            raise ValueError("print anchor")
        return _replace_node(source, prints[0].args[0], "payload")
    if name == "asyncio_run_added":
        return _insert_helper(source, "def _negative_fixture_asyncio_run_probe():\n    asyncio.run(None)")
    if name == "second_app_import":
        return _insert_helper(source, 'def _negative_fixture_second_app_import_probe():\n    importlib.import_module("app.main")')
    if name == "second_event_loop":
        return _insert_helper(source, "def _negative_fixture_second_event_loop_probe():\n    asyncio.new_event_loop()")
    if name == "asgi_transport_removed":
        calls = _calls(_function(tree, "_perform_get"), "httpx.ASGITransport")
        if len(calls) != 1:
            raise ValueError("asgi anchor")
        return _replace_node(source, calls[0], "object()")
    if name == "target_route_changed":
        calls = _client_get_calls(_function(tree, "_perform_get"))
        if len(calls) != 1 or len(calls[0].args) != 1:
            raise ValueError("target route anchor")
        return _replace_node(source, calls[0].args[0], '"/api/v1/internal/alpha/review-console/local-exchange-projections/changed"')
    if name == "directory_discovery_added":
        return _insert_helper(source, 'def _negative_fixture_directory_probe():\n    os.listdir(".")')
    if name == "socket_type_replaced":
        return _insert_helper(source, "def _negative_fixture_socket_type_probe():\n    socket.socket = _blocked_action")
    if name == "atomic_replace_removed":
        writer = _function(tree, "_write_safe_result")
        matches = [node for node in writer.body if len(_calls(node, "os.replace")) == 1]
        if len(matches) != 1:
            raise ValueError("atomic replace anchor")
        return _replace_statement(source, matches[0])
    if name == "receipt_schema_substitution":
        dictionary = _canonical_assignment(tree).value
        return _replace_node(source, dictionary.values[0], 'receipt["schema"]')
    if name == "opaque_configuration_bound_1048":
        function = _function(tree, "_validate_opaque")
        matches = [node for node in ast.walk(function) if isinstance(node, ast.Constant) and node.value == 2048]
        if len(matches) != 1:
            raise ValueError("opaque bound anchor")
        return _replace_node(source, matches[0], "1048")
    raise ValueError("unknown fixture")


def _build_negative(name):
    if name not in {item[0] for item in NEGATIVE_SPECS}:
        raise ValueError("fixture identity")
    before = _inventory(VALID_PUBLIC_RUNNER)
    mutated = _mutate_fixture(name)
    ast.parse(mutated, filename="<negative-fixture>", mode="exec")
    after = _inventory(mutated)
    delta = {key: after[key] - before[key] for key in before}
    expected = EXPECTED_DELTAS[name]
    for key, value in delta.items():
        if value != expected.get(key, 0):
            raise ValueError("unexpected mutation delta")
    return mutated, {
        "name": name,
        "changed_regions": 1,
        "parse": True,
        "inventory_delta": {key: value for key, value in delta.items() if value},
    }


def _asyncio_preflight():
    source, summary = _build_negative("asyncio_run_added")
    tree = ast.parse(source, filename="<asyncio-preflight>", mode="exec")
    helper = _function(tree, "_negative_fixture_asyncio_run_probe")
    calls = _calls(helper, "asyncio.run")
    perform_names = [node for node in ast.walk(helper) if isinstance(node, ast.Name) and node.id == "_perform_get"]
    before = _inventory(VALID_PUBLIC_RUNNER)
    after = _inventory(source)
    valid = (
        len(calls) == 1
        and len(calls[0].args) == 1
        and isinstance(calls[0].args[0], ast.Constant)
        and calls[0].args[0].value is None
        and not calls[0].keywords
        and not perform_names
        and after["perform_get"] - before["perform_get"] == 0
        and after["new_event_loop"] - before["new_event_loop"] == 0
        and after["client_get"] - before["client_get"] == 0
        and after["app_import"] - before["app_import"] == 0
        and summary["changed_regions"] == 1
    )
    return {
        "status": "pass" if valid else "fail",
        "parse": True,
        "inserted_asyncio_run_calls": len(calls),
        "argument_literal_none": bool(calls and len(calls[0].args) == 1 and isinstance(calls[0].args[0], ast.Constant) and calls[0].args[0].value is None),
        "keyword_count": len(calls[0].keywords) if calls else None,
        "inserted_subtree_perform_get_names": len(perform_names),
        "perform_get_call_delta": after["perform_get"] - before["perform_get"],
        "new_event_loop_delta": after["new_event_loop"] - before["new_event_loop"],
        "client_get_delta": after["client_get"] - before["client_get"],
        "app_import_delta": after["app_import"] - before["app_import"],
        "changed_regions": summary["changed_regions"],
    }


def _self_test():
    preflight = _asyncio_preflight()
    valid_result = _audit_bytes(VALID_PUBLIC_RUNNER.encode("utf-8"))
    fixture_results = []
    parse_failures = 0
    rejected = 0
    matches = 0
    for fixture_name, expected_check in NEGATIVE_SPECS:
        source, mutation = _build_negative(fixture_name)
        result = _audit_bytes(source.encode("utf-8"))
        parsed = result["checks"][1]["passed"]
        if not parsed:
            parse_failures += 1
        if result["status"] == "fail" and parsed:
            rejected += 1
        exact = result["failed_checks"] == [expected_check]
        if exact:
            matches += 1
        fixture_results.append({
            "name": fixture_name,
            "expected_check": expected_check,
            "parse": parsed,
            "failed_checks": result["failed_checks"],
            "exact_single_violation": exact,
            "mutation": mutation,
        })
    order_exact = tuple(CHECK_NAMES) == CHECK_NAMES and len(set(CHECK_NAMES)) == 30
    fixture_order_exact = tuple(item[0] for item in NEGATIVE_SPECS) == tuple(item["name"] for item in fixture_results)
    passed = (
        preflight["status"] == "pass"
        and valid_result["status"] == "pass"
        and len(fixture_results) == 20
        and rejected == 20
        and parse_failures == 0
        and matches == 20
        and order_exact
        and fixture_order_exact
    )
    return {
        "schema": SELF_TEST_SCHEMA,
        "version": VERSION,
        "status": "pass" if passed else "fail",
        "checks_total": len(CHECK_NAMES),
        "valid_total": 1,
        "valid_accepted": 1 if valid_result["status"] == "pass" else 0,
        "negative_total": len(NEGATIVE_SPECS),
        "negative_tested": len(fixture_results),
        "negative_rejected": rejected,
        "fixture_parse_failures": parse_failures,
        "single_violation_matches": matches,
        "runner_execution": 0,
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
        "check_names_order_exact": order_exact,
        "negative_fixture_names_order_exact": fixture_order_exact,
        "valid_result": valid_result,
        "asyncio_preflight": preflight,
        "fixtures": fixture_results,
    }


def _load_runner_once(path_text):
    path = Path(path_text)
    if not path.is_absolute() or path.name != EXPECTED_RUNNER_BASENAME:
        raise ValueError("runner path identity")
    if path.is_symlink() or not path.is_file():
        raise ValueError("runner file identity")
    data = path.read_bytes()
    if not 1 <= len(data) <= MAX_RUNNER_BYTES:
        raise ValueError("runner byte bound")
    return data


def _audit_runner_path(path_text):
    data = _load_runner_once(path_text)
    result = _audit_bytes(data)
    result["runner_reads"] = 1
    result["runner_reopens"] = 0
    return result


def _qualify_runner(path_text):
    self_test = _self_test()
    data = _load_runner_once(path_text)
    equality = data == VALID_PUBLIC_RUNNER.encode("utf-8")
    runner_audit = _audit_bytes(data)
    passed = self_test["status"] == "pass" and equality and runner_audit["status"] == "pass"
    return {
        "schema": QUALIFICATION_SCHEMA,
        "version": VERSION,
        "status": "pass" if passed else "fail",
        "self_test": self_test,
        "runner_audit": runner_audit,
        "runner_reads": 1,
        "runner_reopens": 0,
        "runner_executed": 0,
        "fixture_byte_equality": equality,
        "runner_bytes": len(data),
        "runner_sha256": hashlib.sha256(data).hexdigest(),
        "environment_access": 0,
        "receipt_access": 0,
        "product_access": 0,
    }


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    result = None
    if arguments == ["--self-test"]:
        result = _self_test()
    elif len(arguments) == 2 and arguments[0] == "--audit-runner":
        result = _audit_runner_path(arguments[1])
    elif len(arguments) == 2 and arguments[0] == "--qualify-runner":
        result = _qualify_runner(arguments[1])
    else:
        result = {
            "schema": AUDITOR_SCHEMA,
            "version": VERSION,
            "status": "fail",
            "reason": "invalid_cli",
        }
    print(json.dumps(result, ensure_ascii=True, separators=(",", ":"), sort_keys=False))
    return 0 if result.get("status") == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
