from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

NINE_A1_APPROVAL_PHRASE = (
    "APPROVE_9A_1_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_GO_NO_GO_GATE_DECISION_DOCS_ONLY"
)
NINE_A2_APPROVAL_PHRASE = (
    "APPROVE_9A_2_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_AUTHORIZATION_PROTOCOL_TESTS_ONLY"
)
NINE_A3_INACTIVE_PHRASE = (
    "APPROVE_9A_3_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_AUTHORIZATION_PROTOCOL_"
    "COMPLETION_WRITE_AUTHORIZATION_READINESS_GATE_DECISION_DOCS_ONLY"
)
CONTROLLED_WRITE_HELPER_PHRASE = (
    "APPROVE_8W_28_CONTROLLED_EVIDENCEITEM_EVIDENCE_LAYER_WRITE_RUNTIME_IMPLEMENTATION"
)

NINE_A1_DOCS = [
    REPO_ROOT
    / "docs"
    / "planning"
    / "sentigraph_9a_1_actual_evidence_layer_write_production_evidenceitem_go_no_go_gate_decision_v0_1.md",
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_go_no_go_gate_contract_v0_1.md",
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_authorization_blocker_matrix_v0_1.md",
]
HEALTH_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_2_actual_evidence_layer_write_production_evidenceitem_authorization_protocol_tests_report_v0_1.md"
)

TARGET_SERVICE_FILES = [
    REPO_ROOT / "backend" / "app" / "services" / "controlled_evidenceitem_evidence_layer_write_runtime.py",
    REPO_ROOT / "backend" / "app" / "services" / "controlled_evidence_layer_write_candidate.py",
    REPO_ROOT / "backend" / "app" / "services" / "controlled_evidence_layer_import_candidate.py",
    REPO_ROOT / "backend" / "app" / "services" / "controlled_production_evidence_import_candidate.py",
    REPO_ROOT / "backend" / "app" / "services" / "evidence_import.py",
    REPO_ROOT / "backend" / "app" / "services" / "evidence_ingestion.py",
]
TARGET_FRONTEND_FILES = [
    REPO_ROOT / "frontend" / "src" / "api" / "sentigraphApi.js",
    REPO_ROOT / "frontend" / "src" / "pages" / "InternalAlphaReviewConsole.jsx",
    REPO_ROOT / "frontend" / "src" / "App.jsx",
    REPO_ROOT / "frontend" / "src" / "components" / "layout" / "AppShell.jsx",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_existing(paths: list[Path]) -> dict[Path, str]:
    return {path: _read(path) for path in paths if path.exists()}


def _assert_contains_all(text: str, required: list[str], *, label: str) -> None:
    missing = [item for item in required if item not in text]
    assert not missing, f"{label} missing required text: {missing}"


def _all_route_sources() -> dict[Path, str]:
    routes_dir = REPO_ROOT / "backend" / "app" / "api" / "v1" / "routes"
    return {path: _read(path) for path in routes_dir.glob("*.py")}


def _line_contexts(text: str, token: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if token in line]


def test_9a1_docs_exist_and_remain_no_write() -> None:
    for path in NINE_A1_DOCS:
        assert path.exists(), path

    joined = "\n".join(_read(path) for path in NINE_A1_DOCS)
    _assert_contains_all(
        joined,
        [
            "docs_only = yes",
            "actual_write_ready_now = no",
            "production_evidenceitem_creation_ready_now = no",
            "actual_evidence_layer_write_approved = no",
            "actual_evidence_layer_write_performed = no",
            "production_evidenceitem_created = no",
            "ready_for_9A_2_actual_evidence_layer_write_production_evidenceitem_authorization_protocol_tests_only",
            NINE_A2_APPROVAL_PHRASE,
            "Source 11 update = no",
        ],
        label="9A-1 docs",
    )


def test_9a2_phrase_is_tests_only_and_not_write_authorization() -> None:
    scan_paths = [*NINE_A1_DOCS, Path(__file__)]
    if HEALTH_REPORT.exists():
        scan_paths.append(HEALTH_REPORT)

    joined = "\n".join(_read(path) for path in scan_paths)
    assert NINE_A2_APPROVAL_PHRASE in joined

    for line in _line_contexts(joined, NINE_A2_APPROVAL_PHRASE):
        normalized = line.lower()
        assert (
            "tests-only" in normalized
            or "tests_only" in normalized
            or "inactive" in normalized
            or "approval_phrase" in normalized
        ), line

    docs_and_report = "\n".join(_read(path) for path in scan_paths if path != Path(__file__))
    forbidden_authorization_claims = [
        "authorizes actual Evidence Layer write",
        "authorizes production EvidenceItem creation",
        "authorizes helper execution that writes",
        "authorizes Review Queue runtime",
        "authorizes production case",
        "authorizes production analysis_run",
        "authorizes production Analysis Result",
        "authorizes Source 11",
        "authorizes public delivery",
    ]
    for claim in forbidden_authorization_claims:
        assert claim not in docs_and_report


def test_authorization_protocol_requirements_remain_present() -> None:
    joined = "\n".join(_read(path) for path in NINE_A1_DOCS)
    _assert_contains_all(
        joined,
        [
            "exact approval phrase for that later write phase",
            "explicit human authority",
            "manual review responsibility acceptance",
            "warning_count acknowledgment",
            "human_review_required acknowledgment",
            "no_automatic_trust_upgrade acknowledgment",
            "blocker status classification",
            "risk category classification",
            "input object lineage verification",
            "raw/private/secret field absence",
            "safe evidence identity policy",
            "audit note",
            "rollback / revocation / pause handling",
            "validation plan",
            "stop before write if any blocker remains",
        ],
        label="authorization protocol requirements",
    )


def test_blocker_matrix_covers_mandatory_blockers() -> None:
    matrix = _read(NINE_A1_DOCS[2])
    _assert_contains_all(
        matrix,
        [
            "Missing explicit human authority",
            "Missing manual review responsibility",
            "warning_count greater than zero not acknowledged",
            "human_review_required not acknowledged",
            "no_automatic_trust_upgrade not acknowledged",
            "Attempted automatic trust upgrade",
            "Unsafe input schema",
            "Uncontrolled source object lineage",
            "Raw row/comment/identity/secret present",
            "Real package directory read required",
            "Production package row parsing required",
            "Private collector inspection required",
            "Route/API/frontend write surface required",
            "Review Queue runtime required",
            "Production case or production analysis_run required",
            "Actual analysis execution required",
            "Production Analysis Result required",
            "Source 11 / FinalSummaryReport required",
            "Export/public/final delivery required",
            "Collector/provider job required",
            "Real API/LLM/network/fetch/scrape required",
            "Audit or rollback missing",
            "Approval phrase missing or ambiguous",
        ],
        label="blocker matrix",
    )


def test_backend_routes_do_not_expose_9a_write_surface() -> None:
    route_sources = _all_route_sources()
    assert route_sources, "backend route files should be discoverable"

    forbidden_route_tokens = [
        NINE_A1_APPROVAL_PHRASE,
        NINE_A2_APPROVAL_PHRASE,
        "approve actual Evidence Layer write",
        "perform actual Evidence Layer write",
        "create production EvidenceItem",
        "production-evidenceitem write route",
        "approve_write",
        "write_now",
        "actual_evidence_layer_write endpoint",
        "production_evidenceitem endpoint",
    ]
    for path, source in route_sources.items():
        for token in forbidden_route_tokens:
            assert token not in source, f"{path} exposes forbidden route token: {token}"

    for path, source in route_sources.items():
        lowered = source.lower()
        if "9a" not in lowered:
            continue
        assert "@router.post" not in lowered
        assert "@router.put" not in lowered
        assert "@router.patch" not in lowered
        assert "@router.delete" not in lowered


def test_frontend_has_no_9a_write_cta_or_api_hook() -> None:
    frontend_sources = _read_existing(TARGET_FRONTEND_FILES)
    assert frontend_sources, "targeted frontend files should be discoverable"

    forbidden_frontend_tokens = [
        NINE_A1_APPROVAL_PHRASE,
        NINE_A2_APPROVAL_PHRASE,
        "approve actual Evidence Layer write",
        "perform actual Evidence Layer write",
        "create production EvidenceItem",
        "approve_write",
        "write_now",
        "actual_evidence_layer_write",
        "productionEvidenceItem",
        "Review Queue runtime write CTA",
        "public/customer production Evidence write",
    ]
    for path, source in frontend_sources.items():
        for token in forbidden_frontend_tokens:
            assert token not in source, f"{path} exposes forbidden frontend token: {token}"


def test_controlled_write_helper_surface_remains_isolated() -> None:
    helper_path = TARGET_SERVICE_FILES[0]
    assert helper_path.exists(), helper_path
    helper_source = _read(helper_path)

    assert CONTROLLED_WRITE_HELPER_PHRASE in helper_source
    assert NINE_A1_APPROVAL_PHRASE not in helper_source
    assert NINE_A2_APPROVAL_PHRASE not in helper_source
    assert "production EvidenceItem runtime ready" not in helper_source
    assert "operator-runtime-ready" not in helper_source

    route_sources = _all_route_sources()
    for path, source in route_sources.items():
        assert "controlled_evidenceitem_evidence_layer_write_runtime" not in source, (
            f"{path} imports controlled write runtime helper"
        )


def test_project_source_and_adjacent_chain_boundaries_remain_separate() -> None:
    assert not (REPO_ROOT / "docs" / "project_sources").exists()
    assert not list(REPO_ROOT.glob("SENTIGRAPH_PROJECT_SOURCE_*"))
    assert not list((REPO_ROOT / "docs").glob("SENTIGRAPH_PROJECT_SOURCE_*"))

    joined = "\n".join(_read(path) for path in NINE_A1_DOCS)
    _assert_contains_all(
        joined,
        [
            "8W-69 pause remains preserved",
            "8W-70 reactivation remains not selected",
            "9A Evidence write authorization does not satisfy production Analysis Result creation authorization protocol",
            "Source 11 / FinalSummaryReport runtime is not affected",
            "Source 11 update = no",
        ],
        label="adjacent chain separation",
    )


def test_new_report_has_no_positive_readiness_overclaim_if_present() -> None:
    if not HEALTH_REPORT.exists():
        return

    report = _read(HEALTH_REPORT)
    forbidden_positive_claims = [
        "actual Evidence Layer write approved",
        "actual Evidence Layer write performed",
        "persisted Evidence Layer record created",
        "production EvidenceItem approved",
        "production EvidenceItem created",
        "Review Queue runtime approved",
        "production case approved",
        "production analysis_run approved",
        "actual analysis execution approved",
        "production Analysis Result approved",
        "Source 11 runtime ready",
        "FinalSummaryReport runtime ready",
        "public delivery ready",
        "production-ready",
        "public-ready",
        "customer-ready",
        "operator-runtime-ready",
    ]
    allowed_markers = (
        " no",
        "= no",
        "not ",
        "forbidden",
        "negative",
        "blocked",
        "does not",
        "must not",
        "not approve",
        "no ",
    )
    for claim in forbidden_positive_claims:
        for line in _line_contexts(report, claim):
            assert any(marker in line.lower() for marker in allowed_markers), line
