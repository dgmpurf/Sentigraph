from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_SRC = REPO_ROOT / "frontend/src"
FRONTEND_API = FRONTEND_SRC / "api"
BACKEND_ROUTE = REPO_ROOT / "backend/app/api/v1/routes/internal_alpha_review_console.py"
BACKEND_API = REPO_ROOT / "backend/app/api/v1/api.py"
THIS_TEST = Path(__file__).resolve()
HEALTH_REPORT = (
    REPO_ROOT
    / "docs/health/sentigraph_8z_24_internal_alpha_review_console_frontend_safety_contract_tests_report_v0_1.md"
)
PLANNING_8Z23 = (
    REPO_ROOT
    / "docs/planning/sentigraph_8z_23_internal_alpha_review_console_route_skeleton_completion_frontend_readiness_gate_decision_v0_1.md"
)
CONTRACT_8Z23 = (
    REPO_ROOT
    / "docs/architecture/sentigraph_internal_alpha_review_console_route_skeleton_completion_frontend_readiness_contract_v0_1.md"
)
FUTURE_FRONTEND_GATE_8Z23 = (
    REPO_ROOT
    / "docs/architecture/sentigraph_internal_alpha_review_console_future_frontend_safety_contract_gate_v0_1.md"
)

DOCS_8Z23 = [PLANNING_8Z23, CONTRACT_8Z23, FUTURE_FRONTEND_GATE_8Z23]

APPROVAL_PHRASE_8Z24 = "APPROVE_8Z_24_INTERNAL_ALPHA_REVIEW_CONSOLE_FRONTEND_SAFETY_CONTRACT_TESTS_ONLY"
APPROVAL_PHRASE_8Z23 = (
    "APPROVE_8Z_23_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_SKELETON_COMPLETION_FRONTEND_READINESS_GATE_DECISION_DOCS_ONLY"
)

FORBIDDEN_FRONTEND_SURFACES = [
    "frontend/src/pages/ReviewConsole.jsx",
    "frontend/src/pages/InternalAlphaReviewConsole.tsx",
    "frontend/src/pages/ReviewConsole.tsx",
    "frontend/src/components/internalAlphaReviewConsole",
    "frontend/src/components/reviewConsole",
    "frontend/src/components/InternalAlphaReviewConsole.jsx",
    "frontend/src/components/ReviewConsole.jsx",
    "frontend/src/components/InternalAlphaReviewConsole.tsx",
    "frontend/src/components/ReviewConsole.tsx",
]

ALLOWED_8Z26_STATIC_FRONTEND_SHELL_PATHS = {
    "frontend/src/App.jsx",
    "frontend/src/api/sentigraphApi.js",
    "frontend/src/data/internalAlphaReviewConsoleStaticFixture.js",
    "frontend/src/pages/InternalAlphaReviewConsole.jsx",
}

ALLOWED_8Z26_INTERNAL_ROUTE = "#/internal-alpha/review-console"

FORBIDDEN_FRONTEND_ROUTE_STRINGS = [
    "internal-alpha-review-console",
    "/internal-alpha-review-console",
    "/internal/alpha/review-console",
    "/api/v1/internal/alpha/review-console",
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

FORBIDDEN_API_HOOK_TERMS = [
    "getReviewConsole",
    "fetchReviewConsole",
    "internalAlphaReviewConsole",
    "reviewConsoleProjection",
    "/api/v1/internal/alpha/review-console",
    "internal/alpha/review-console",
    "review-console/projections",
    "internal-alpha-review-console",
    "review-console",
]

FORBIDDEN_PUBLIC_ALIAS_TERMS = [
    "public review console",
    "customer review console",
    "b-end review console",
    "c-end review console",
    "public-events/review-console",
    "reports/review-console",
    "public/review-console",
    "customer/review-console",
    "b-end/review-console",
    "c-end/review-console",
    "/review-console/public",
    "/api/v1/review-console/public",
]

REVIEW_CONSOLE_FILE_MARKERS = [
    "internal-alpha-review-console",
    "review-console",
    "internalAlphaReviewConsole",
    "reviewConsole",
    "InternalAlphaReviewConsole",
    "ReviewConsole",
]

FORBIDDEN_CTA_TERMS = [
    "approve",
    "write",
    "publish",
    "send",
    "post",
    "execute",
    "create production",
    "create production EvidenceItem",
    "use Review Queue runtime",
    "create production Review Queue item",
    "create production case",
    "create production analysis_run",
    "start actual analysis execution",
    "authorize production Analysis Result",
    "create production Analysis Result",
    "call Source 11 runtime",
    "create FinalSummaryReport runtime output",
    "generate B-end report runtime",
    "generate Sandbox/public event runtime",
    "create export/download/public/final-delivery runtime",
    "run collector/provider job",
    "inspect private collector source",
    "read real exchange/package dir",
    "parse production package rows",
    "fetch URL",
    "scrape",
    "call real API",
    "call real LLM",
    "auto_execute",
    "approve_write",
    "write_now",
    "production EvidenceItem",
    "Review Queue runtime",
    "Evidence Layer write",
    "Source 11",
    "FinalSummaryReport",
    "export",
    "download",
    "public delivery",
    "final delivery",
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
    "cookies",
    "sessions",
    "tokens",
    "passwords",
    "API keys",
    "browser profiles",
    "absolute private paths",
    ".env",
    ".env values",
    "evidence_items.jsonl",
    "evidence_items.csv",
    "evidence_items.jsonl contents",
    "evidence_items.csv contents",
    "source_manifest",
    "collection_log",
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
    "production-ready",
    "customer-ready",
    "public-ready",
    "export-ready",
    "final-ready",
    "route-ready",
    "frontend-ready",
    "route_ready",
    "frontend_ready",
    "public_ready",
    "customer_ready",
    "export_ready",
    "final_ready",
    "actual Evidence Layer write approved",
    "production EvidenceItem approved",
    "Review Queue runtime approved",
    "Review Queue runtime ready",
    "Evidence Layer write approved",
    "Source 11 runtime ready",
    "FinalSummaryReport runtime ready",
    "public delivery ready",
]

STATIC_FORBIDDEN_BACKEND_ROUTE_TERMS = [
    "FileResponse",
    "StreamingResponse",
    "zipfile",
    "public_url",
    "signed_url",
    "file_bytes",
    "external_delivery",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _casefold(text: str) -> str:
    return text.casefold()


def _frontend_files(root: Path = FRONTEND_SRC) -> list[Path]:
    if not root.exists():
        return []
    suffixes = {".js", ".jsx", ".ts", ".tsx"}
    return [path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes]


def _frontend_route_files() -> list[Path]:
    candidates = [
        FRONTEND_SRC / "App.jsx",
        FRONTEND_SRC / "App.js",
        FRONTEND_SRC / "main.jsx",
        FRONTEND_SRC / "main.js",
    ]
    return [path for path in candidates if path.exists()]


def _frontend_api_files() -> list[Path]:
    return _frontend_files(FRONTEND_API)


def _joined_text(files: list[Path]) -> str:
    return "\n".join(_read(path) for path in files)


def _read_only_8z30_helper_body() -> str:
    api_text = _read(FRONTEND_API / "sentigraphApi.js")
    marker = "export async function getInternalAlphaReviewConsoleProjection(projectionId)"
    assert marker in api_text
    start = api_text.index(marker)
    tail = api_text[start:]
    end = tail.index("\n}")
    return tail[: end + 2]


def _without_quoted_catalog_entries(text: str, entries: list[str]) -> str:
    sanitized = text
    for entry in entries:
        sanitized = sanitized.replace(f'    "{entry}",', "")
        sanitized = sanitized.replace(f'        "{entry}",', "")
        sanitized = sanitized.replace(f'    "{entry}"', "")
        sanitized = sanitized.replace(f'        "{entry}"', "")
    return sanitized


def _review_console_related_frontend_files() -> list[Path]:
    related: list[Path] = []
    for path in _frontend_files():
        relative_path = path.relative_to(REPO_ROOT).as_posix()
        text = _read(path)
        haystack = f"{relative_path}\n{text}"
        if any(marker in haystack for marker in REVIEW_CONSOLE_FILE_MARKERS):
            related.append(path)
    return related


def _review_console_static_shell_files() -> list[Path]:
    return [
        REPO_ROOT / "frontend/src/data/internalAlphaReviewConsoleStaticFixture.js",
        REPO_ROOT / "frontend/src/pages/InternalAlphaReviewConsole.jsx",
    ]


def _relative_paths(paths: list[Path]) -> set[str]:
    return {path.relative_to(REPO_ROOT).as_posix() for path in paths}


def test_8z23_docs_exist_and_select_only_inactive_tests_only_future_gate() -> None:
    for path in DOCS_8Z23:
        assert path.exists(), path

    planning = _read(PLANNING_8Z23)
    combined_docs = _joined_text(DOCS_8Z23)
    combined_lower = _casefold(combined_docs)

    assert "docs_only = yes" in planning
    assert (
        "selected_next_boundary_option = ready_for_8Z_24_internal_alpha_review_console_frontend_safety_contract_tests_only"
        in planning
    )
    assert APPROVAL_PHRASE_8Z24 in combined_docs
    assert "frontend safety contract tests-only" in combined_lower
    assert "inactive future phrase" in combined_lower or "this phrase is inactive" in combined_lower
    assert "does not authorize frontend implementation" in combined_lower
    assert "does not approve actual write" in combined_lower
    assert "production object" in combined_lower
    assert "source 11" in combined_lower
    assert "finalsummaryreport" in combined_lower


def test_8z24_future_phrase_is_inactive_in_8z23_docs() -> None:
    for path in DOCS_8Z23:
        lines = _read(path).splitlines()
        phrase_lines = [index for index, line in enumerate(lines) if APPROVAL_PHRASE_8Z24 in line]
        assert phrase_lines, path
        for index in phrase_lines:
            context = "\n".join(lines[max(0, index - 4) : min(len(lines), index + 7)])
            context_lower = _casefold(context)
            assert "inactive" in context_lower or "future" in context_lower, context
            assert "does not authorize" in context_lower or "does not approve" in context_lower, context


def test_only_8z26_static_internal_frontend_shell_files_exist() -> None:
    for relative_path in FORBIDDEN_FRONTEND_SURFACES:
        assert not (REPO_ROOT / relative_path).exists(), relative_path

    related_paths = _relative_paths(_review_console_related_frontend_files())
    assert related_paths == ALLOWED_8Z26_STATIC_FRONTEND_SHELL_PATHS

    shell_text = _joined_text(_review_console_static_shell_files())
    assert "static internal frontend shell" in shell_text
    assert "route_backend_connection =" in shell_text
    assert "static fallback active" in shell_text
    assert "getInternalAlphaReviewConsoleProjection" in shell_text
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]" in shell_text
    assert "fetch(" not in shell_text
    assert "axios" not in shell_text
    assert "/api/v1/internal/alpha/review-console" not in shell_text


def test_only_internal_static_frontend_route_registration_exists() -> None:
    route_text = _casefold(_joined_text(_frontend_route_files()))
    assert _casefold(ALLOWED_8Z26_INTERNAL_ROUTE) in route_text
    for forbidden in FORBIDDEN_FRONTEND_ROUTE_STRINGS:
        assert _casefold(forbidden) not in route_text, forbidden


def test_no_frontend_api_client_hook_consumes_review_console_route() -> None:
    helper_body = _read_only_8z30_helper_body()
    helper_lower = _casefold(helper_body)

    assert "getinternalalphareviewconsoleprojection" in _casefold(_read(FRONTEND_API / "sentigraphApi.js"))
    assert "/internal/alpha/" in helper_body
    assert "internal_alpha_review_console_route_segment" in helper_lower
    assert "internal_alpha_review_console_projections_segment" in helper_lower
    assert "apiclient.get(" in helper_lower
    assert "encodeuricomponent(projectionid)" in helper_lower
    for forbidden in [".post(", ".put(", ".patch(", ".delete(", "fetch(", "xmlhttprequest"]:
        assert forbidden not in helper_lower, forbidden


def test_no_public_customer_c_end_or_b_end_frontend_alias_exists() -> None:
    frontend_text = _casefold(_joined_text(_frontend_files()))
    for forbidden in FORBIDDEN_PUBLIC_ALIAS_TERMS:
        assert _casefold(forbidden) not in frontend_text, forbidden


def test_no_forbidden_cta_or_action_in_review_console_frontend_surface() -> None:
    related_files = _review_console_static_shell_files()
    related_text = _joined_text(related_files)
    related_lower = _casefold(related_text)

    active_action_terms = [
        "<button",
        "onclick",
        "href=",
        "window.location",
        "approvewrite",
        "writenow",
        "publishnow",
        "sendnow",
        "postnow",
        "executenow",
        "createproduction",
        "runcollector",
        "runprovider",
        "callsource11",
        "createfinalsummaryreport",
    ]
    for forbidden in active_action_terms:
        assert forbidden not in related_lower, forbidden

    assert "allowed actions labels only" in related_lower
    assert "blocked actions labels only" in related_lower


def test_no_forbidden_display_fields_in_review_console_frontend_surface() -> None:
    related_text = _casefold("\n".join([_joined_text(_review_console_static_shell_files()), _read_only_8z30_helper_body()]))
    for forbidden in FORBIDDEN_DISPLAY_FIELDS:
        assert _casefold(forbidden) not in related_text, forbidden


def test_production_readiness_state_is_exposed_only_as_safely_disabled() -> None:
    related_text = _casefold("\n".join([_joined_text(_review_console_static_shell_files()), _read_only_8z30_helper_body()]))
    for forbidden in FORBIDDEN_READINESS_OVERCLAIMS:
        assert _casefold(forbidden) not in related_text, forbidden

    assert "review_only = true" in related_text
    assert "persistent_staging_write = false" in related_text
    assert "review_decision_write = false" in related_text
    assert "production_ready = false" in related_text
    assert "public_output_enabled = false" in related_text
    for unauthorized_true_form in [
        "production_ready = true",
        '"production_ready": true',
        "production_ready: true",
    ]:
        assert unauthorized_true_form not in related_text


def test_backend_route_skeleton_remains_internal_disabled_and_file_delivery_free() -> None:
    route_text = _read(BACKEND_ROUTE)
    api_text = _read(BACKEND_API)

    assert "SENTIGRAPH_INTERNAL_ALPHA_REVIEW_CONSOLE_ROUTE_ENABLED" in route_text
    assert '@router.get("/projections/{projection_id}")' in route_text
    assert 'ROUTE_MODE = "disabled_by_default_internal_safe_projection_route_skeleton"' in route_text
    assert 'prefix="/internal/alpha/review-console"' in api_text
    assert "internal_alpha_review_console.router" in api_text

    combined_route_text = route_text + "\n" + api_text
    for forbidden in STATIC_FORBIDDEN_BACKEND_ROUTE_TERMS:
        assert forbidden not in combined_route_text, forbidden


def test_8z24_approval_phrase_is_tests_only_and_not_frontend_implementation_approval() -> None:
    scan_files = [THIS_TEST]
    if HEALTH_REPORT.exists():
        scan_files.append(HEALTH_REPORT)

    combined = _joined_text(scan_files)
    assert APPROVAL_PHRASE_8Z24 in combined
    assert "frontend safety contract tests" in combined

    forbidden_approval_claims = [
        "authorizes frontend implementation",
        "authorizes frontend route registration",
        "authorizes browser-visible UI",
        "authorizes frontend API consumption",
        "frontend implementation approved",
        "backend route changes approved",
        "Review Queue runtime approved",
        "actual Evidence Layer write approved",
        "production EvidenceItem approved",
    ]
    combined_scan_text = _without_quoted_catalog_entries(combined, forbidden_approval_claims)
    combined_scan_text = _without_quoted_catalog_entries(combined_scan_text, FORBIDDEN_READINESS_OVERCLAIMS)
    combined_scan_text = _without_quoted_catalog_entries(combined_scan_text, [APPROVAL_PHRASE_8Z23])
    combined_lower = _casefold(combined_scan_text)
    for forbidden in forbidden_approval_claims:
        assert _casefold(forbidden) not in combined_lower, forbidden

    if APPROVAL_PHRASE_8Z23 in combined_scan_text:
        phrase_lines = [line for line in combined_scan_text.splitlines() if APPROVAL_PHRASE_8Z23 in line]
        assert phrase_lines
        for line in phrase_lines:
            assert "historical" in _casefold(line) or "inactive" in _casefold(line), line
