from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

NINE_A6_PHRASE = (
    "APPROVE_9A_6_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "HUMAN_AUTHORITY_FINAL_AUTHORIZATION_PROTOCOL_TESTS_ONLY"
)
NINE_A5_PHRASE = (
    "APPROVE_9A_5_NO_WRITE_EVIDENCE_LAYER_WRITE_AUTHORIZATION_READINESS_CANDIDATE_"
    "COMPLETION_ACTUAL_WRITE_AUTHORIZATION_GATE_DECISION_DOCS_ONLY"
)
NINE_A7_FUTURE_PHRASE = (
    "APPROVE_9A_7_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_HUMAN_AUTHORITY_"
    "PROTOCOL_COMPLETION_ACTUAL_WRITE_READINESS_GATE_DECISION_DOCS_ONLY"
)

NINE_A5_DOCS = [
    REPO_ROOT
    / "docs"
    / "planning"
    / "sentigraph_9a_5_no_write_evidence_layer_write_authorization_readiness_candidate_completion_actual_write_authorization_gate_decision_v0_1.md",
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_no_write_evidence_layer_write_authorization_readiness_candidate_completion_actual_write_authorization_gate_contract_v0_1.md",
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_future_human_authority_final_authorization_protocol_tests_gate_contract_v0_1.md",
]
NINE_A1_BLOCKER_MATRIX = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_authorization_blocker_matrix_v0_1.md"
)
NINE_A4_HELPER = REPO_ROOT / "backend" / "app" / "services" / "evidence_layer_write_authorization_readiness_candidate.py"
NINE_A4_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_4_controlled_no_write_evidence_layer_write_production_evidenceitem_authorization_readiness_candidate_fixture_smoke_report_v0_1.md"
)
NINE_A6_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_6_actual_evidence_layer_write_production_evidenceitem_human_authority_final_authorization_protocol_tests_report_v0_1.md"
)

TARGET_FRONTEND_FILES = [
    REPO_ROOT / "frontend" / "src" / "api" / "sentigraphApi.js",
    REPO_ROOT / "frontend" / "src" / "pages" / "InternalAlphaReviewConsole.jsx",
    REPO_ROOT / "frontend" / "src" / "App.jsx",
    REPO_ROOT / "frontend" / "src" / "components" / "layout" / "AppShell.jsx",
]

ACTIVE_RUNTIME_AUTHORITY_TOKENS = [
    "validate_human_authority_for_write",
    "perform_human_authority_validation",
    "human_authority_validated = true",
    "human_authority_validated: true",
    '"human_authority_validated": true',
    "set_human_authority_validated",
    "approve_human_authority",
    "authority_token_write_approval",
    "authority credential write approval",
]

ACTIVE_FINAL_WRITE_TOKENS = [
    "perform_final_write_authorization",
    "final_write_authorization_performed = true",
    "final_write_authorization_performed: true",
    '"final_write_authorization_performed": true',
    "set_final_write_authorization",
    "approve_final_write",
    "finalize_evidence_layer_write",
    "write_authorization_object_created_that_permits_write = true",
    "write_authorization_object_created_that_permits_write: true",
    '"write_authorization_object_created_that_permits_write": true',
    "final_authorize_write",
]

ROUTE_FRONTEND_WRITE_TOKENS = [
    "human_authority_validated = true",
    "human_authority_validated: true",
    '"human_authority_validated": true',
    "final_write_authorization_performed = true",
    "final_write_authorization_performed: true",
    '"final_write_authorization_performed": true',
    "ready_for_actual_write = true",
    "ready_for_actual_write: true",
    '"ready_for_actual_write": true',
    "approve_write",
    "final_authorize_write",
    "create production EvidenceItem",
    "actual Evidence Layer write",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_existing(paths: list[Path]) -> dict[Path, str]:
    return {path: _read(path) for path in paths if path.exists()}


def _joined(paths: list[Path]) -> str:
    return "\n".join(_read(path) for path in paths)


def _line_contexts(text: str, token: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if token in line]


def _nearby_context(text: str, token: str, *, radius: int = 2) -> list[str]:
    lines = text.splitlines()
    contexts: list[str] = []
    for index, line in enumerate(lines):
        if token not in line:
            continue
        start = max(0, index - radius)
        end = min(len(lines), index + radius + 1)
        contexts.append(" ".join(part.strip() for part in lines[start:end]))
    return contexts


def _assert_contains_all(text: str, required: list[str], *, label: str) -> None:
    missing = [item for item in required if item not in text]
    assert not missing, f"{label} missing required text: {missing}"


def _route_sources() -> dict[Path, str]:
    route_dir = REPO_ROOT / "backend" / "app" / "api" / "v1" / "routes"
    return {path: _read(path) for path in route_dir.glob("*.py")}


def _target_surface_sources() -> dict[Path, str]:
    sources = dict(_route_sources())
    sources.update(_read_existing(TARGET_FRONTEND_FILES))
    return sources


def _service_sources() -> dict[Path, str]:
    service_dir = REPO_ROOT / "backend" / "app" / "services"
    return {
        path: _read(path)
        for path in [
            service_dir / "evidence_layer_write_authorization_readiness_candidate.py",
            service_dir / "controlled_evidence_layer_write_candidate.py",
            service_dir / "controlled_evidence_layer_write_candidate_from_production_import_candidate.py",
            service_dir / "controlled_evidenceitem_evidence_layer_write_runtime.py",
            service_dir / "evidence_import.py",
            service_dir / "evidence_ingestion.py",
        ]
        if path.exists()
    }


def _assert_no_active_tokens(sources: dict[Path, str], tokens: list[str], *, label: str) -> None:
    hits: list[str] = []
    for path, source in sources.items():
        lowered_source = source.lower()
        for token in tokens:
            if token.lower() in lowered_source:
                hits.append(f"{path}: {token}")
    assert not hits, f"{label} active token hits: {hits}"


def test_9a5_docs_exist_and_preserve_tests_only_future_9a6_gate() -> None:
    for path in NINE_A5_DOCS:
        assert path.exists(), path

    joined = _joined(NINE_A5_DOCS)
    _assert_contains_all(
        joined,
        [
            "docs_only = yes",
            "human_authority_validated = no",
            "final_write_authorization_performed = no",
            "ready_for_actual_write = no",
            "actual_write_ready_now = no",
            "production_evidenceitem_creation_ready_now = no",
            "ready_for_9A_6_actual_evidence_layer_write_production_evidenceitem_human_authority_final_authorization_protocol_tests_only",
            NINE_A6_PHRASE,
            "tests-only",
            "Inactive future phrase",
            "Source 11 update = no",
        ],
        label="9A-5 docs",
    )


def test_9a6_phrase_is_tests_only_and_not_write_authorization() -> None:
    scan_paths = [*NINE_A5_DOCS, Path(__file__)]
    if NINE_A6_REPORT.exists():
        scan_paths.append(NINE_A6_REPORT)

    for path in scan_paths:
        text = _read(path)
        if NINE_A6_PHRASE not in text:
            continue
        if path == Path(__file__):
            continue
        for context in _nearby_context(text, NINE_A6_PHRASE):
            normalized = context.lower()
            assert (
                "tests-only" in normalized
                or "inactive" in normalized
                or "report" in normalized
                or "phrase_scope" in normalized
            ), f"{path} has unsafe 9A-6 phrase context: {context}"

    joined = "\n".join(_read(path) for path in scan_paths if path != Path(__file__))
    forbidden_claims = [
        "authorizes actual Evidence Layer write",
        "authorizes runtime human authority validation",
        "authorizes final write authorization",
        "authorizes production EvidenceItem",
        "authorizes helper write execution",
        "authorizes Review Queue runtime",
        "authorizes production case",
        "authorizes production analysis_run",
        "authorizes production Analysis Result",
        "authorizes Source 11",
        "authorizes public delivery",
    ]
    for claim in forbidden_claims:
        assert claim not in joined


def test_required_human_authority_protocol_fields_are_represented() -> None:
    joined = "\n".join([_joined(NINE_A5_DOCS), _read(NINE_A4_HELPER)])
    required_any = [
        ["explicit human authority"],
        ["required_human_authority_status"],
        ["manual review responsibility"],
        ["manual_review_responsibility_status"],
        ["warning_count acknowledgment", "warning_count_acknowledgment_status"],
        ["human_review_required acknowledgment", "human_review_required_acknowledgment_status"],
        ["no_automatic_trust_upgrade acknowledgment", "no_automatic_trust_upgrade_acknowledgment_status"],
        ["blocker classification", "blocker_statuses"],
        ["risk classification", "risk_statuses"],
        ["input lineage verification", "input_lineage_summary"],
        ["raw/private/secret absence"],
        ["safe evidence identity policy", "safe_identity_policy_status"],
        ["rollback/pause/revocation plan", "rollback_pause_policy_status"],
        ["audit note", "audit_note_status"],
        ["final write authorization"],
    ]
    missing = [options for options in required_any if not any(option in joined for option in options)]
    assert not missing, f"missing protocol vocabulary options: {missing}"


def test_runtime_human_authority_validation_remains_absent() -> None:
    sources = _service_sources()
    sources.update(_route_sources())
    _assert_no_active_tokens(
        sources,
        ACTIVE_RUNTIME_AUTHORITY_TOKENS,
        label="runtime human authority validation",
    )


def test_final_write_authorization_remains_absent() -> None:
    sources = _service_sources()
    sources.update(_route_sources())
    _assert_no_active_tokens(
        sources,
        ACTIVE_FINAL_WRITE_TOKENS,
        label="final write authorization",
    )


def test_9a4_no_write_candidate_remains_not_ready_for_write() -> None:
    helper = _read(NINE_A4_HELPER)
    report = _read(NINE_A4_REPORT)
    combined = f"{helper}\n{report}"
    _assert_contains_all(
        combined,
        [
            "ready_for_actual_write",
            "human_authority_validated",
            "final_write_authorization_performed",
            "actual_evidence_layer_write_authorized",
            "production_evidenceitem_creation_authorized",
            "write_authorization_object_created_that_permits_write",
            "candidate_ready_for_human_review_no_write",
            "candidate_blocked_no_write",
        ],
        label="9A-4 no-write candidate boundary",
    )
    for import_token in [
        "controlled_evidenceitem_evidence_layer_write_runtime",
        "evidence_import",
        "evidence_ingestion",
    ]:
        assert import_token not in helper
    assert "route_api_frontend_trigger_payload" in helper
    assert '"ready_for_actual_write": True' not in helper
    assert '"human_authority_validated": True' not in helper
    assert '"final_write_authorization_performed": True' not in helper


def test_no_route_api_or_frontend_can_set_authority_or_final_authorization() -> None:
    surface_sources = _target_surface_sources()
    assert surface_sources, "target route/frontend surfaces should be discoverable"
    _assert_no_active_tokens(
        surface_sources,
        ROUTE_FRONTEND_WRITE_TOKENS,
        label="route/API/frontend authority or write surface",
    )


def test_9a1_blocker_matrix_covers_human_authority_and_final_authorization() -> None:
    joined = f"{_read(NINE_A1_BLOCKER_MATRIX)}\n{_joined(NINE_A5_DOCS)}"
    _assert_contains_all(
        joined,
        [
            "Missing explicit human authority",
            "Missing manual review responsibility",
            "warning_count greater than zero not acknowledged",
            "human_review_required not acknowledged",
            "no_automatic_trust_upgrade not acknowledged",
            "Audit or rollback missing",
            "Approval phrase missing or ambiguous",
            "final write authorization absent",
        ],
        label="blocker matrix and 9A-5 final authorization coverage",
    )


def test_8w_and_source11_separation_remains_preserved() -> None:
    joined = "\n".join([_joined(NINE_A5_DOCS), _read(NINE_A4_REPORT)])
    _assert_contains_all(
        joined,
        [
            "8W-69 pause remains preserved",
            "8W-70 reactivation remains not selected",
            "9A write-readiness discussion does not satisfy production Analysis Result authorization protocol",
            "Source 11 update = no",
        ],
        label="8W and Source 11 separation",
    )
    assert (
        "Source 11 / FinalSummaryReport runtime remains separate" in joined
        or "Source 11 / FinalSummaryReport runtime remains a separate gate" in joined
    )


def test_new_tests_and_report_have_no_positive_readiness_overclaim() -> None:
    scan_paths = [Path(__file__)]
    if NINE_A6_REPORT.exists():
        scan_paths.append(NINE_A6_REPORT)

    forbidden_claims = [
        "actual Evidence Layer write " + "approved",
        "actual Evidence Layer write " + "performed",
        "persisted Evidence Layer record " + "created",
        "production EvidenceItem " + "approved",
        "production EvidenceItem " + "created",
        "helper execution that writes " + "approved",
        "write authorization object " + "permits write",
        "human authority " + "validated",
        "final write authorization " + "performed",
        "ready for " + "actual write",
        "Review Queue runtime " + "approved",
        "production case " + "approved",
        "production analysis_run " + "approved",
        "actual analysis execution " + "approved",
        "production Analysis Result " + "approved",
        "Source 11 runtime " + "ready",
        "FinalSummaryReport runtime " + "ready",
        "public delivery " + "ready",
        "production-" + "ready",
        "public-" + "ready",
        "customer-" + "ready",
        "operator-runtime-" + "ready",
    ]
    allowed_markers = (
        "forbidden",
        "not ",
        "no ",
        "= no",
        "= false",
        "false",
        "must not",
        "does not",
        "absent",
        "blocked",
        "negative",
        "scope",
        "catalog",
    )
    for path in scan_paths:
        for line in _read(path).splitlines():
            normalized = line.strip().lower()
            for claim in forbidden_claims:
                if claim not in line:
                    continue
                assert any(marker in normalized for marker in allowed_markers), f"{path}: {line}"
