from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_SRC = REPO_ROOT / "frontend/src"
APP_FILE = FRONTEND_SRC / "App.jsx"
SHELL_FILE = FRONTEND_SRC / "pages/InternalAlphaReviewConsole.jsx"
FIXTURE_FILE = FRONTEND_SRC / "data/internalAlphaReviewConsoleStaticFixture.js"
STYLE_FILE = FRONTEND_SRC / "styles/global.css"
COMPATIBILITY_TEST = (
    REPO_ROOT
    / "backend/app/tests/test_8z_24_internal_alpha_review_console_frontend_safety_contract_tests.py"
)

APPROVAL_PHRASE_8Z26 = "APPROVE_8Z_26_INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FRONTEND_SHELL_SMOKE"
INTERNAL_ROUTE = "#/internal-alpha/review-console"
BACKEND_ROUTE_FRAGMENT = "/api/v1/internal/alpha/review-console"

REQUIRED_VISIBLE_BOUNDARIES = [
    "Internal Alpha Review Console static preview",
    "source_chain_boundary = evidence_layer_write_candidate_boundary",
    "route_backend_connection =",
    "static_shell_only_not_connected",
    "static fallback active",
    "human_review_required = true",
    "no_automatic_trust_upgrade = true",
    "no actual write",
    "no production object",
    "no Review Queue runtime",
    "no Source 11 / FinalSummaryReport runtime",
    "selected sample / no-write / no-production boundary",
    "this shell is not operator runtime",
]

REQUIRED_FIXTURE_FIELDS = [
    "projection_schema",
    "projection_mode",
    "source_chain_boundary",
    "stage_summaries",
    "evidence_count_summary",
    "source_count_summary",
    "warning_count",
    "blocker_count",
    "coverage_note_summary",
    "validation_summary",
    "safety_flags",
    "boundary_flags",
    "human_review_required",
    "no_automatic_trust_upgrade",
    "allowed_actions",
    "blocked_actions",
    "route_backend_connection",
    "static_shell_only_not_connected",
]

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

FORBIDDEN_API_CONSUMPTION_TERMS = [
    "fetch(",
    "axios",
    BACKEND_ROUTE_FRAGMENT,
    "getReviewConsole",
    "review-console/projections",
]

FORBIDDEN_ACTIVE_ACTION_TERMS = [
    "<button",
    "onClick",
    "href=",
    "window.location",
    "approveWrite",
    "writeNow",
    "publishNow",
    "sendNow",
    "postNow",
    "executeNow",
    "createProduction",
    "runCollector",
    "runProvider",
    "callSource11",
    "createFinalSummaryReport",
]

FORBIDDEN_DISPLAY_FIELDS = [
    "raw_author_id",
    "raw_author_name",
    "author_id",
    "author_name",
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

FORBIDDEN_READY_OVERCLAIMS = [
    "production-ready",
    "customer-ready",
    "public-ready",
    "export-ready",
    "final-ready",
    "backend connected",
    "route connected",
    "operator runtime ready",
    "Evidence Layer write approved",
    "production EvidenceItem approved",
    "Review Queue runtime approved",
    "Source 11 runtime ready",
    "FinalSummaryReport runtime ready",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _combined_shell_text() -> str:
    return "\n".join(_read(path) for path in [SHELL_FILE, FIXTURE_FILE])


def test_static_frontend_shell_files_exist() -> None:
    assert SHELL_FILE.exists()
    assert FIXTURE_FILE.exists()
    assert STYLE_FILE.exists()
    assert APP_FILE.exists()


def test_internal_only_route_is_registered_without_public_aliases() -> None:
    app_text = _read(APP_FILE)
    frontend_text = "\n".join(_read(path) for path in [APP_FILE, SHELL_FILE, FIXTURE_FILE])

    assert INTERNAL_ROUTE in app_text
    assert "internalAlphaReviewConsole" in app_text
    assert "InternalAlphaReviewConsole" in app_text

    for forbidden in FORBIDDEN_PUBLIC_ALIASES:
        assert forbidden not in frontend_text, forbidden


def test_shell_consumes_only_8z30_read_only_helper_without_direct_backend_route() -> None:
    shell_text = _combined_shell_text()

    assert "getInternalAlphaReviewConsoleProjection" in shell_text
    assert "INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]" in shell_text
    for forbidden in FORBIDDEN_API_CONSUMPTION_TERMS:
        assert forbidden not in shell_text, forbidden


def test_shell_displays_required_static_boundaries() -> None:
    shell_text = _combined_shell_text()

    for required in REQUIRED_VISIBLE_BOUNDARIES:
        assert required in shell_text, required


def test_static_fixture_uses_only_safe_metadata_summary_fields() -> None:
    fixture_text = _read(FIXTURE_FILE)

    for required in REQUIRED_FIXTURE_FIELDS:
        assert required in fixture_text, required

    assert "route_backend_connection: 'static_shell_only_not_connected'" in fixture_text
    assert "human_review_required: true" in fixture_text
    assert "no_automatic_trust_upgrade: true" in fixture_text


def test_shell_has_no_active_write_or_operator_cta() -> None:
    shell_text = _combined_shell_text()

    for forbidden in FORBIDDEN_ACTIVE_ACTION_TERMS:
        assert forbidden not in shell_text, forbidden


def test_shell_does_not_expose_forbidden_raw_private_or_secret_fields() -> None:
    shell_text = _combined_shell_text().casefold()

    for forbidden in FORBIDDEN_DISPLAY_FIELDS:
        assert forbidden.casefold() not in shell_text, forbidden


def test_shell_does_not_make_readiness_overclaims() -> None:
    shell_text = _combined_shell_text().casefold()

    for forbidden in FORBIDDEN_READY_OVERCLAIMS:
        assert forbidden.casefold() not in shell_text, forbidden


def test_8z24_compatibility_test_was_narrowly_updated_for_static_internal_shell() -> None:
    compatibility_text = _read(COMPATIBILITY_TEST)

    assert "ALLOWED_8Z26_STATIC_FRONTEND_SHELL_PATHS" in compatibility_text
    assert "static internal frontend shell" in compatibility_text
    assert "frontend API consumption" in compatibility_text
    assert BACKEND_ROUTE_FRAGMENT in compatibility_text


def test_8z26_phrase_is_static_shell_context_only() -> None:
    test_text = _read(Path(__file__))
    shell_text = _combined_shell_text()

    assert APPROVAL_PHRASE_8Z26 in test_text
    assert "static frontend shell" in test_text
    assert "production analysis result" not in shell_text.casefold()
