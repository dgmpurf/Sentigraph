from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_SRC = REPO_ROOT / "frontend/src"
FRONTEND_API = FRONTEND_SRC / "api"
APP_FILE = FRONTEND_SRC / "App.jsx"
SHELL_FILE = FRONTEND_SRC / "pages/InternalAlphaReviewConsole.jsx"
FIXTURE_FILE = FRONTEND_SRC / "data/internalAlphaReviewConsoleStaticFixture.js"

PLANNING_8Z27 = (
    REPO_ROOT
    / "docs/planning/sentigraph_8z_27_internal_alpha_review_console_static_shell_completion_backend_route_consumption_readiness_gate_decision_v0_1.md"
)
CONTRACT_8Z27 = (
    REPO_ROOT
    / "docs/architecture/sentigraph_internal_alpha_review_console_static_shell_completion_backend_route_consumption_readiness_contract_v0_1.md"
)
FUTURE_GATE_8Z27 = (
    REPO_ROOT
    / "docs/architecture/sentigraph_internal_alpha_review_console_future_backend_route_consumption_safety_contract_gate_v0_1.md"
)

DOCS_8Z27 = [PLANNING_8Z27, CONTRACT_8Z27, FUTURE_GATE_8Z27]

APPROVAL_PHRASE_8Z28 = (
    "APPROVE_8Z_28_INTERNAL_ALPHA_REVIEW_CONSOLE_BACKEND_ROUTE_CONSUMPTION_SAFETY_CONTRACT_TESTS_ONLY"
)
APPROVAL_PHRASE_8Z27 = (
    "APPROVE_8Z_27_INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_SHELL_COMPLETION_BACKEND_ROUTE_CONSUMPTION_READINESS_GATE_DECISION_DOCS_ONLY"
)
SELECTED_8Z28_BOUNDARY = (
    "ready_for_8Z_28_internal_alpha_review_console_backend_route_consumption_safety_contract_tests_only"
)
INTERNAL_FRONTEND_ROUTE = "#/internal-alpha/review-console"
BACKEND_ROUTE_FRAGMENT = "/api/v1/internal/alpha/review-console"
READ_ONLY_HELPER_8Z30 = "getInternalAlphaReviewConsoleProjection"

API_HOOK_TERMS = [
    "getReviewConsole",
    "fetchReviewConsole",
    "listReviewConsole",
    "getInternalAlphaReviewConsole",
    "fetchInternalAlphaReviewConsole",
    "getReviewConsoleProjection",
    "fetchReviewConsoleProjection",
    "internalAlphaReviewConsole",
    "reviewConsoleProjection",
    "reviewConsoleProjections",
    "internalAlphaReviewConsoleProjection",
    BACKEND_ROUTE_FRAGMENT,
    "internal/alpha/review-console",
    "review-console/projections",
]

SHELL_ROUTE_CONSUMPTION_TERMS = [
    "sentigraphApi",
    "fetch(",
    "axios",
    "XMLHttpRequest",
    BACKEND_ROUTE_FRAGMENT,
    "internal/alpha/review-console",
    "review-console/projections",
    "useEffect(",
    "async function",
    "Promise.",
]

FORBIDDEN_PUBLIC_ALIASES = [
    "#/review-console",
    "#/public/review-console",
    "#/public-events/review-console",
    "#/reports/review-console",
    "#/customer/review-console",
    "#/b-end/review-console",
    "#/c-end/review-console",
    "#/review-console/public",
    "/public/review-console",
    "/public-events/review-console",
    "/reports/review-console",
    "/customer/review-console",
    "/b-end/review-console",
    "/c-end/review-console",
    "/review-console/public",
]

ROUTE_CONSUMPTION_SIDE_EFFECT_TERMS = [
    "loadReviewConsole",
    "loadProjection",
    "refreshProjection",
    "retryProjection",
    "setProjectionLoading",
    "setRouteError",
    "backendResponse",
    "backendError",
    "projectionIdInput",
    "packageIdInput",
    "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED",
]

ACTIVE_OPERATOR_CTA_TERMS = [
    "<button",
    "<Button",
    "onClick",
    "href=",
    "<form",
    "approveWrite",
    "writeNow",
    "publishNow",
    "sendNow",
    "postNow",
    "executeNow",
    "auto_execute",
    "approve_write",
    "createProduction",
    "runCollector",
    "runProvider",
    "callSource11",
    "createFinalSummaryReport",
    "startActualAnalysisExecution",
    "createProductionAnalysisResult",
]

FORBIDDEN_DISPLAY_FIELDS = [
    "raw evidence rows",
    "raw comments",
    "raw author ID",
    "raw author name",
    "raw author IDs",
    "raw author names",
    "actual profile URLs",
    "profile_url",
    "private messages",
    "private_message",
    "cookies",
    "sessions",
    "tokens",
    "passwords",
    "API keys",
    "browser profiles",
    "absolute private paths",
    ".env values",
    "evidence_items.jsonl contents",
    "evidence_items.csv contents",
    "source_manifest row contents",
    "collection_log row contents",
    "response_text",
    "generated_public_message",
    "target_user_list",
    "persuasion_score",
    "truth_score",
    "official_verified",
    "prediction_probability",
    "psychological_profile",
    "personality_diagnosis",
]

FORBIDDEN_READINESS_OVERCLAIMS = [
    "production_ready = true",
    "public_ready = true",
    "customer_ready = true",
    "export_ready = true",
    "final_ready = true",
    "route_consumption_ready = true",
    "backend_connected = true",
    "route_backend_connection = connected",
    "Source 11 runtime ready",
    "FinalSummaryReport runtime ready",
    "Review Queue runtime ready",
    "Evidence Layer write approved",
    "production EvidenceItem approved",
]

REQUIRED_STATIC_BOUNDARY_STRINGS = [
    "static shell only",
    "not connected",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "evidence_layer_write_candidate_boundary",
    "no actual write",
    "no production object",
    "no Review Queue runtime",
    "no Source 11 / FinalSummaryReport runtime",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _helper_body(api_text: str) -> str:
    marker = f"export async function {READ_ONLY_HELPER_8Z30}(projectionId)"
    assert marker in api_text
    start = api_text.index(marker)
    tail = api_text[start:]
    end = tail.index("\n}")
    return tail[: end + 2]


def _casefold(text: str) -> str:
    return text.casefold()


def _joined(files: list[Path]) -> str:
    return "\n".join(_read(path) for path in files if path.exists())


def _frontend_api_files() -> list[Path]:
    if not FRONTEND_API.exists():
        return []
    return [
        path
        for path in FRONTEND_API.rglob("*")
        if path.is_file() and path.suffix in {".js", ".jsx", ".ts", ".tsx"}
    ]


def _shell_context_text() -> str:
    return _joined([SHELL_FILE, FIXTURE_FILE])


def _strip_catalog_entries(text: str, entries: list[str]) -> str:
    stripped = text
    for entry in entries:
        stripped = stripped.replace(f'    "{entry}",', "")
        stripped = stripped.replace(f'    "{entry}"', "")
        stripped = stripped.replace(f'        "{entry}",', "")
        stripped = stripped.replace(f'        "{entry}"', "")
        stripped = stripped.replace(f"    '{entry}',", "")
        stripped = stripped.replace(f"    '{entry}'", "")
        stripped = stripped.replace(f"        '{entry}',", "")
        stripped = stripped.replace(f"        '{entry}'", "")
    return stripped


def _assert_phrase_context_is_inactive(lines: list[str], phrase: str) -> None:
    indexes = [index for index, line in enumerate(lines) if phrase in line]
    assert indexes
    for index in indexes:
        context = "\n".join(lines[max(0, index - 5) : min(len(lines), index + 7)])
        context_lower = _casefold(context)
        assert "inactive" in context_lower or "future" in context_lower, context
        assert "does not authorize" in context_lower or "does not approve" in context_lower, context


def test_8z27_docs_exist_and_select_inactive_tests_only_future_gate() -> None:
    for path in DOCS_8Z27:
        assert path.exists(), path

    docs_text = _joined(DOCS_8Z27)
    docs_lower = _casefold(docs_text)

    assert "docs_only = yes" in docs_text
    assert "tests-only" in docs_lower
    assert SELECTED_8Z28_BOUNDARY in docs_text
    assert APPROVAL_PHRASE_8Z28 in docs_text
    assert "inactive future phrase" in docs_lower or "inactive phrase" in docs_lower
    assert "frontend api consumption is not approved" in docs_lower
    assert "sentigraphapi" in docs_lower
    assert "review-console hook is not approved" in docs_lower
    assert "8z-27 does not expand backend route behavior" in docs_lower
    assert "8z-27 does not approve actual write" in docs_lower
    assert "production object" in docs_lower
    assert "source 11" in docs_lower
    assert "finalsummaryreport" in docs_lower


def test_8z28_future_phrase_is_tests_only_and_not_implementation_approval() -> None:
    for path in DOCS_8Z27:
        _assert_phrase_context_is_inactive(_read(path).splitlines(), APPROVAL_PHRASE_8Z28)

    docs_text = _joined(DOCS_8Z27)
    scan_text = _strip_catalog_entries(docs_text, [APPROVAL_PHRASE_8Z27, APPROVAL_PHRASE_8Z28])
    scan_lower = _casefold(scan_text)

    forbidden_claims = [
        "authorizes frontend api hook implementation",
        "authorizes backend route consumption implementation",
        "api hook approved",
        "backend route consumption approved",
        "actual write approved",
        "production object approved",
        "public delivery approved",
    ]
    for forbidden in forbidden_claims:
        assert forbidden not in scan_lower, forbidden


def test_frontend_api_hook_is_limited_to_8z30_read_only_internal_projection_helper() -> None:
    api_text = _joined(_frontend_api_files())
    helper_body = _helper_body(api_text)

    assert READ_ONLY_HELPER_8Z30 in api_text
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS" in api_text
    assert "/internal/alpha/" in helper_body
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_SEGMENT" in helper_body
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_PROJECTIONS_SEGMENT" in helper_body
    assert "apiClient.get(" in helper_body
    assert "encodeURIComponent(projectionId)" in helper_body
    for forbidden in [".post(", ".put(", ".patch(", ".delete(", "fetch(", "XMLHttpRequest"]:
        assert forbidden not in helper_body, forbidden


def test_static_shell_consumes_only_8z30_safe_helper_and_not_raw_backend_route() -> None:
    shell_text = _shell_context_text()

    assert READ_ONLY_HELPER_8Z30 in shell_text
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]" in shell_text
    direct_route_terms = [
        "fetch(",
        "axios",
        "XMLHttpRequest",
        BACKEND_ROUTE_FRAGMENT,
        "internal/alpha/review-console",
        "review-console/projections",
    ]
    for forbidden in direct_route_terms:
        assert forbidden not in shell_text, forbidden


def test_frontend_route_remains_internal_only_without_public_aliases() -> None:
    route_text = _read(APP_FILE)
    route_and_shell_text = "\n".join([route_text, _shell_context_text()])

    assert INTERNAL_FRONTEND_ROUTE in route_text
    assert "InternalAlphaReviewConsole" in route_text

    for forbidden in FORBIDDEN_PUBLIC_ALIASES:
        assert forbidden not in route_and_shell_text, forbidden


def test_no_route_consumption_side_effects_exist_in_static_shell_or_api_context() -> None:
    scan_text = "\n".join([_shell_context_text(), _joined(_frontend_api_files())])

    for forbidden in ROUTE_CONSUMPTION_SIDE_EFFECT_TERMS:
        assert forbidden not in scan_text, forbidden


def test_no_active_write_or_operator_cta_exists_in_shell_context() -> None:
    shell_text = _shell_context_text()

    for forbidden in ACTIVE_OPERATOR_CTA_TERMS:
        assert forbidden not in shell_text, forbidden

    shell_lower = _casefold(shell_text)
    assert "allowed actions labels only" in shell_lower
    assert "blocked actions labels only" in shell_lower


def test_no_forbidden_raw_private_or_secret_fields_in_shell_or_review_console_api_context() -> None:
    shell_text = _shell_context_text()
    api_text = _joined(_frontend_api_files())
    helper_text = _helper_body(api_text)

    assert "review-console/projections" not in api_text
    assert BACKEND_ROUTE_FRAGMENT not in api_text

    shell_lower = _casefold("\n".join([shell_text, helper_text]))
    for forbidden in FORBIDDEN_DISPLAY_FIELDS:
        assert _casefold(forbidden) not in shell_lower, forbidden


def test_no_readiness_overclaim_in_shell_or_review_console_api_context() -> None:
    shell_text = _shell_context_text()
    api_text = _joined(_frontend_api_files())

    assert "reviewConsole" not in api_text
    assert "internalAlphaReviewConsole" not in api_text

    shell_lower = _casefold(shell_text)
    for forbidden in FORBIDDEN_READINESS_OVERCLAIMS:
        assert _casefold(forbidden) not in shell_lower, forbidden

    assert "static_shell_only_not_connected" in shell_text


def test_8z26_static_shell_remains_visibly_static_by_source() -> None:
    shell_text = _shell_context_text()

    for required in REQUIRED_STATIC_BOUNDARY_STRINGS:
        assert required in shell_text, required


def test_future_route_consumption_implementation_remains_separately_gated() -> None:
    docs_text = _joined(DOCS_8Z27)
    docs_lower = _casefold(docs_text)

    assert "any later actual implementation" in docs_lower
    assert "requires a separate exact approval phrase" in docs_lower
    assert "frontend build" in docs_lower
    assert "browser smoke if available" in docs_lower
    assert "8z-22 route tests" in docs_lower
    assert "8z-26 and 8z-24 safety tests" in docs_lower
    assert "browser_unavailable = yes" in docs_lower
