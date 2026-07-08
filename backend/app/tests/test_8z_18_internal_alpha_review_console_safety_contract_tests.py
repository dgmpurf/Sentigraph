from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

PLANNING_DOC = REPO_ROOT / "docs/planning/sentigraph_8z_17_internal_alpha_review_console_and_operator_workflow_planning_decision_v0_1.md"
CONTRACT_DOC = REPO_ROOT / "docs/architecture/sentigraph_internal_alpha_review_console_operator_workflow_contract_v0_1.md"
SAFETY_TEST_PLAN_DOC = REPO_ROOT / "docs/architecture/sentigraph_internal_alpha_review_console_safety_test_plan_v0_1.md"

DOC_PATHS = [PLANNING_DOC, CONTRACT_DOC, SAFETY_TEST_PLAN_DOC]

APPROVAL_PHRASE_8Z18 = "APPROVE_8Z_18_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFETY_CONTRACT_TESTS_ONLY"

FORBIDDEN_IMPLEMENTATION_PATHS = [
    "backend/app/api/v1/routes/internal_alpha_review_console.py",
    "backend/app/api/v1/routes/review_console.py",
    "frontend/src/pages/InternalAlphaReviewConsole.jsx",
    "frontend/src/pages/ReviewConsole.jsx",
    "frontend/src/components/internalAlphaReviewConsole",
]

FORBIDDEN_PUBLIC_ALIASES = [
    "/public/review-console",
    "/public-events/review-console",
    "/reports/review-console",
    "/customer/review-console",
    "/b-end/review-console",
    "/c-end/review-console",
    "/api/v1/public/review-console",
    "/api/v1/review-console/public",
]

FORBIDDEN_DISPLAY_TERMS = [
    "raw evidence rows",
    "raw comments",
    "raw author IDs",
    "raw author names",
    "actual profile URLs",
    "private messages",
    "cookies",
    "sessions",
    "tokens",
    "passwords",
    "API keys",
    "browser profiles",
    "absolute private paths",
    "`.env` values",
    "evidence_items.jsonl",
    "evidence_items.csv",
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

FORBIDDEN_ACTION_TERMS = [
    "approve actual Evidence Layer write",
    "perform actual Evidence Layer write",
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
    "read real exchange/package directory",
    "parse production package rows",
    "fetch URL",
    "scrape",
    "call real API",
    "call real LLM",
    "publish/send/post/execute",
]

FUTURE_ROUTE_POSTURE_TERMS = [
    "safety contract tests",
    "docs-only contract",
    "internal-only",
    "local-only",
    "disabled-by-default",
    "GET/read-only first",
    "safe metadata only",
    "no raw rows",
    "no file bytes",
    "no FileResponse / StreamingResponse / ZIP",
    "no public / C-end / B-end / customer alias",
    "no direct write buttons",
    "no production approval actions",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined_docs() -> str:
    return "\n\n".join(_read(path) for path in DOC_PATHS)


def _lower(text: str) -> str:
    return text.casefold()


def _source_files_for_static_scan() -> list[Path]:
    roots = [
        REPO_ROOT / "backend/app/api/v1/routes",
        REPO_ROOT / "frontend/src",
    ]
    suffixes = {".py", ".js", ".jsx", ".ts", ".tsx"}
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix in suffixes)
    return files


def test_8z17_planning_docs_exist_and_remain_docs_only_contracts() -> None:
    for path in DOC_PATHS:
        assert path.exists(), path

    planning = _read(PLANNING_DOC)
    combined = _combined_docs()
    combined_lower = _lower(combined)

    required_fragments = [
        "phase = 8Z-17",
        "docs_only = yes",
        "planning_only = yes",
        "8Z-17 does not implement this console",
        "safe metadata only",
        "label-only outcomes",
        "human_review_required",
        "no_automatic_trust_upgrade",
        "Forbidden Future Display Fields",
        "Forbidden Future Active Actions",
        "actual_evidence_layer_write = no",
        "production_evidence_item_created = no",
        "review_queue_runtime_used = no",
        "source11_runtime_called = no",
        "finalsummaryreport_runtime_called = no",
        "public_delivery_created = no",
    ]
    for fragment in required_fragments:
        assert _lower(fragment) in _lower(planning if " = no" in fragment or "phase =" in fragment else combined), fragment

    assert "future internal alpha review console" in combined_lower
    assert "safe, internal, local, read-only operator planning surface" in combined_lower
    assert "does not approve route/api/frontend implementation" in combined_lower


def test_future_8z18_phrase_is_inactive_tests_only_wording() -> None:
    for path in DOC_PATHS:
        text = _read(path)
        if APPROVAL_PHRASE_8Z18 not in text:
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if APPROVAL_PHRASE_8Z18 not in line:
                continue
            context = "\n".join(lines[max(0, index - 4) : min(len(lines), index + 6)]).casefold()
            assert "inactive" in context
            assert "does not authorize" in context or "not authorize" in context
            assert "implementation" in context or "tests-only" in context

    combined = _combined_docs()
    assert APPROVAL_PHRASE_8Z18 in combined
    forbidden_approvals = [
        "authorizes route/API/frontend implementation",
        "authorizes actual Evidence Layer write",
        "authorizes production objects",
        "authorizes Review Queue runtime",
    ]
    for phrase in forbidden_approvals:
        assert phrase.casefold() not in combined.casefold()


def test_no_current_review_console_implementation_surface_exists() -> None:
    for relative_path in FORBIDDEN_IMPLEMENTATION_PATHS:
        assert not (REPO_ROOT / relative_path).exists(), relative_path

    active_text = "\n".join(_read(path) for path in _source_files_for_static_scan())
    active_lower = active_text.casefold()
    assert "internal-alpha-review-console" not in active_lower
    assert "review-console" not in active_lower
    assert "internalalphareviewconsole" not in active_lower
    assert "reviewconsole" not in active_lower


def test_no_public_or_customer_review_console_aliases_exist_in_active_code() -> None:
    active_text = "\n".join(_read(path) for path in _source_files_for_static_scan())
    active_lower = active_text.casefold()
    for alias in FORBIDDEN_PUBLIC_ALIASES:
        assert alias.casefold() not in active_lower, alias


def test_forbidden_display_fields_are_blocked_by_contract() -> None:
    combined_lower = _lower(_combined_docs())
    for term in FORBIDDEN_DISPLAY_TERMS:
        assert _lower(term) in combined_lower, term

    assert "future display must not include" in combined_lower
    assert "blocked fields include" in combined_lower


def test_forbidden_active_actions_are_blocked_by_contract() -> None:
    combined_lower = _lower(_combined_docs())
    for term in FORBIDDEN_ACTION_TERMS:
        assert _lower(term) in combined_lower, term

    assert "future active actions remain forbidden" in combined_lower
    assert "blocked actions include" in combined_lower


def test_future_route_ui_posture_is_read_only_disabled_by_default_and_safe_metadata_only() -> None:
    combined_lower = _lower(_combined_docs())
    for term in FUTURE_ROUTE_POSTURE_TERMS:
        assert _lower(term) in combined_lower, term

    assert "8z-17 does not implement route/ui" in combined_lower
    assert "8z-17 does not create or modify any route/ui" in combined_lower


def test_8z18_test_file_does_not_import_or_call_controlled_helpers() -> None:
    test_text = _read(Path(__file__))
    forbidden_helper_terms = [
        "controlled_evidence_candidate",
        "controlled_review_queue_candidate",
        "controlled_evidence_layer_import_candidate",
        "controlled_evidence_layer_write_candidate",
        "controlled_row_preview",
        "local_exchange_reader",
        "package_resolver",
        "collector_job",
        "provider_job",
    ]
    quoted_terms = "\n".join(f'"{term}"' for term in forbidden_helper_terms)
    scan_text = test_text.replace(quoted_terms, "")
    for term in forbidden_helper_terms:
        assert f"import app.services.{term}" not in scan_text
        assert f"from app.services import {term}" not in scan_text
        assert f"from app.services.{term}" not in scan_text


def test_no_project_source_docs_are_created_for_8z18() -> None:
    project_sources_dir = REPO_ROOT / "docs/project_sources"
    if project_sources_dir.exists():
        assert not any(path.name.startswith("SENTIGRAPH_PROJECT_SOURCE_") for path in project_sources_dir.rglob("*"))

    source_like_docs = list((REPO_ROOT / "docs").rglob("SENTIGRAPH_PROJECT_SOURCE_*"))
    assert source_like_docs == []
