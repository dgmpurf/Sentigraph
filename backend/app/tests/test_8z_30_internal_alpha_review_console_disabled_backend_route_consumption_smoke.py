from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_SRC = REPO_ROOT / "frontend/src"
FRONTEND_API_CLIENT = FRONTEND_SRC / "api/sentigraphApi.js"
FRONTEND_APP = FRONTEND_SRC / "App.jsx"
FRONTEND_SHELL = FRONTEND_SRC / "pages/InternalAlphaReviewConsole.jsx"
FRONTEND_FIXTURE = FRONTEND_SRC / "data/internalAlphaReviewConsoleStaticFixture.js"
BACKEND_ROUTE_TEST = (
    REPO_ROOT
    / "backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py"
)

APPROVAL_PHRASE_8Z30 = (
    "APPROVE_8Z_30_INTERNAL_ALPHA_REVIEW_CONSOLE_DISABLED_BACKEND_ROUTE_CONSUMPTION_SMOKE"
)
INTERNAL_FRONTEND_ROUTE = "#/internal-alpha/review-console"
BACKEND_ROUTE_FRAGMENT = "/api/v1/internal/alpha/review-console/projections/"
API_ROUTE_PREFIX_FRAGMENT = "/internal/alpha/"
READ_ONLY_HELPER = "getInternalAlphaReviewConsoleProjection"
SAFE_PROJECTION_ID = "internal-alpha-safe-projection-fixture"
SAFE_ALT_PROJECTION_ID = "8z16-no-write-alpha-fixture"

FORBIDDEN_PUBLIC_ALIASES = [
    "#/review-console",
    "#/public/review-console",
    "#/public-events/review-console",
    "#/reports/review-console",
    "#/customer/review-console",
    "#/b-end/review-console",
    "#/c-end/review-console",
    "/public/review-console",
    "/public-events/review-console",
    "/reports/review-console",
    "/customer/review-console",
    "/b-end/review-console",
    "/c-end/review-console",
]

FORBIDDEN_ACTIVE_CTA_TERMS = [
    "<button",
    "<Button",
    "<form",
    "href=",
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

FORBIDDEN_DISPLAY_TERMS = [
    "raw_author_id",
    "raw_author_name",
    "profile_url",
    "private_message",
    "cookie",
    "session",
    "token",
    "password",
    "api_key",
    "browser_profile",
    ".env",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "source_manifest",
    "collection_log",
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

FORBIDDEN_OVERCLAIMS = [
    "production_ready = true",
    "public_ready = true",
    "customer_ready = true",
    "export_ready = true",
    "final_ready = true",
    "backend_connected = true",
    "route_backend_connection = connected",
    "browser QA passed",
    "browser smoke passed",
]

FORBIDDEN_ROUTE_METHODS = [
    ".post(",
    ".put(",
    ".patch(",
    ".delete(",
    "fetch(",
    "XMLHttpRequest",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _casefold(text: str) -> str:
    return text.casefold()


def _helper_body(api_text: str) -> str:
    pattern = re.compile(
        rf"export async function {READ_ONLY_HELPER}\([^)]*\) \{{(?P<body>.*?)\n\}}",
        re.DOTALL,
    )
    match = pattern.search(api_text)
    assert match is not None, f"{READ_ONLY_HELPER} helper is missing"
    return match.group("body")


def _shell_text() -> str:
    return "\n".join([_read(FRONTEND_SHELL), _read(FRONTEND_FIXTURE)])


def test_approval_phrase_is_exact_ascii_and_phase_is_smoke_only() -> None:
    assert APPROVAL_PHRASE_8Z30 == (
        "APPROVE_8Z_30_INTERNAL_ALPHA_REVIEW_CONSOLE_DISABLED_BACKEND_ROUTE_CONSUMPTION_SMOKE"
    )
    assert "APPROVE_8Z_30" in APPROVAL_PHRASE_8Z30
    assert "WRITE" not in APPROVAL_PHRASE_8Z30
    assert "PRODUCTION" not in APPROVAL_PHRASE_8Z30


def test_api_helper_exists_and_is_narrow_get_only() -> None:
    api_text = _read(FRONTEND_API_CLIENT)
    helper_body = _helper_body(api_text)

    assert f"export async function {READ_ONLY_HELPER}(projectionId" in api_text
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS" in api_text
    assert SAFE_PROJECTION_ID in api_text
    assert SAFE_ALT_PROJECTION_ID in api_text
    assert API_ROUTE_PREFIX_FRAGMENT in helper_body
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_SEGMENT" in helper_body
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_PROJECTIONS_SEGMENT" in helper_body
    assert "apiClient.get(" in helper_body
    assert "encodeURIComponent(projectionId)" in helper_body

    for forbidden in FORBIDDEN_ROUTE_METHODS:
        assert forbidden not in helper_body, forbidden

    for forbidden in ["credentials", "withCredentials", "Authorization", "cookie", "token"]:
        assert forbidden not in helper_body, forbidden


def test_api_helper_rejects_unsupported_projection_id_without_fallback() -> None:
    api_text = _read(FRONTEND_API_CLIENT)
    helper_body = _helper_body(api_text)

    assert "includes(projectionId)" in helper_body
    assert "Unsupported internal alpha review console projection id" in helper_body
    assert "internal-alpha-safe-projection-fixture" in api_text
    assert "8z16-no-write-alpha-fixture" in api_text
    assert "unknown-projection-id" not in api_text
    assert "review-console/projections" not in api_text
    assert "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED" not in api_text
    assert "VITE_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED" not in api_text


def test_shell_consumes_only_safe_helper_and_not_raw_route_string() -> None:
    shell = _read(FRONTEND_SHELL)

    assert READ_ONLY_HELPER in shell
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS" in shell
    assert "SAFE_REVIEW_CONSOLE_PROJECTION_ID" in shell
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]" in shell
    assert "useEffect" in shell
    assert "fetch(" not in shell
    assert "axios" not in shell
    assert BACKEND_ROUTE_FRAGMENT not in shell
    assert API_ROUTE_PREFIX_FRAGMENT not in shell
    assert SAFE_ALT_PROJECTION_ID not in shell


def test_disabled_or_unavailable_route_uses_static_fallback_copy() -> None:
    shell = _shell_text()
    shell_lower = _casefold(shell)

    assert "route_disabled" in shell
    assert "backend route disabled" in shell_lower
    assert "not connected" in shell_lower
    assert "static fallback active" in shell_lower
    assert "static fallback" in shell_lower
    assert "unsupported_projection" in shell
    assert "safe not-connected state" in shell_lower
    assert "route enablement" not in shell_lower
    assert "projectionidinput" not in shell_lower
    assert "packageidinput" not in shell_lower


def test_frontend_route_remains_internal_only_without_public_aliases() -> None:
    route_text = _read(FRONTEND_APP)
    shell_context = "\n".join([route_text, _shell_text()])

    assert INTERNAL_FRONTEND_ROUTE in route_text
    assert "InternalAlphaReviewConsole" in route_text

    for alias in FORBIDDEN_PUBLIC_ALIASES:
        assert alias not in shell_context, alias


def test_no_active_write_operator_or_runtime_cta_exists() -> None:
    shell = _shell_text()

    for forbidden in FORBIDDEN_ACTIVE_CTA_TERMS:
        assert forbidden not in shell, forbidden

    shell_lower = _casefold(shell)
    assert "allowed actions labels only" in shell_lower
    assert "blocked actions labels only" in shell_lower
    assert "no actual write" in shell_lower
    assert "no production object" in shell_lower
    assert "no review queue runtime" in shell_lower
    assert "no source 11 / finalsummaryreport runtime" in shell_lower


def test_no_forbidden_display_fields_or_readiness_overclaims() -> None:
    api_text = _read(FRONTEND_API_CLIENT)
    helper_match = re.search(
        rf"export async function {READ_ONLY_HELPER}\([^)]*\) \{{(?P<body>.*?)\n\}}",
        api_text,
        re.DOTALL,
    )
    helper_text = helper_match.group("body") if helper_match else ""
    api_and_shell = "\n".join([helper_text, _shell_text()])
    api_and_shell_lower = _casefold(api_and_shell)

    for forbidden in FORBIDDEN_DISPLAY_TERMS:
        assert _casefold(forbidden) not in api_and_shell_lower, forbidden

    for forbidden in FORBIDDEN_OVERCLAIMS:
        assert _casefold(forbidden) not in api_and_shell_lower, forbidden

    assert "human_review_required" in api_and_shell
    assert "no_automatic_trust_upgrade" in api_and_shell


def test_backend_route_tests_still_define_existing_disabled_internal_get_route() -> None:
    route_test_text = _read(BACKEND_ROUTE_TEST)

    assert 'ROUTE_PREFIX = "/api/v1/internal/alpha/review-console"' in route_test_text
    assert 'ALLOWED_PROJECTION_ID = "internal-alpha-safe-projection-fixture"' in route_test_text
    assert 'ALLOWED_ALT_PROJECTION_ID = "8z16-no-write-alpha-fixture"' in route_test_text
    assert "GET" in route_test_text
    assert "route_disabled" in route_test_text
    assert "unsupported_projection" in route_test_text
