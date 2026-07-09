from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

NINE_A8_PHRASE = (
    "APPROVE_9A_8_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "HUMAN_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_GATE_DOCS_ONLY"
)
NINE_A9_PHRASE = (
    "APPROVE_9A_9_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "HUMAN_AUTHORITY_DECLARATION_SAFETY_CONTRACT_TESTS_ONLY"
)
NINE_A10_FUTURE_PHRASE = (
    "APPROVE_9A_10_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "DECLARATION_SAFETY_COMPLETION_ACTUAL_WRITE_AUTHORIZATION_READINESS_GATE_DECISION_DOCS_ONLY"
)

NINE_A8_PLANNING = (
    REPO_ROOT
    / "docs"
    / "planning"
    / "sentigraph_9a_8_actual_evidence_layer_write_production_evidenceitem_human_authority_manual_review_responsibility_declaration_gate_decision_v0_1.md"
)
NINE_A8_CONTRACT = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_human_authority_manual_review_responsibility_declaration_gate_contract_v0_1.md"
)
NINE_A8_TEMPLATE = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_human_authority_manual_review_responsibility_declaration_template_v0_1.md"
)
NINE_A9_FUTURE_CONTRACT = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_future_human_authority_declaration_safety_contract_tests_gate_v0_1.md"
)
NINE_A9_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_9_actual_evidence_layer_write_production_evidenceitem_human_authority_declaration_safety_contract_tests_report_v0_1.md"
)
NINE_A8_DOCS = [
    NINE_A8_PLANNING,
    NINE_A8_CONTRACT,
    NINE_A8_TEMPLATE,
    NINE_A9_FUTURE_CONTRACT,
]

NINE_A4_HELPER = REPO_ROOT / "backend" / "app" / "services" / "evidence_layer_write_authorization_readiness_candidate.py"
NINE_A4_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_4_controlled_no_write_evidence_layer_write_production_evidenceitem_authorization_readiness_candidate_fixture_smoke_report_v0_1.md"
)
NINE_A7_DOCS = [
    REPO_ROOT
    / "docs"
    / "planning"
    / "sentigraph_9a_7_actual_evidence_layer_write_production_evidenceitem_human_authority_protocol_completion_actual_write_readiness_gate_decision_v0_1.md",
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_human_authority_protocol_completion_actual_write_readiness_contract_v0_1.md",
]

TARGET_FRONTEND_FILES = [
    REPO_ROOT / "frontend" / "src" / "api" / "sentigraphApi.js",
    REPO_ROOT / "frontend" / "src" / "pages" / "InternalAlphaReviewConsole.jsx",
    REPO_ROOT / "frontend" / "src" / "App.jsx",
    REPO_ROOT / "frontend" / "src" / "components" / "layout" / "AppShell.jsx",
]

SAFE_LABELS = [
    "not_validated_by_codex",
    "not_accepted_by_codex",
    "required_later",
    "not_authorized",
    "human_required_later",
    "blocked_until_separate_final_authorization",
]

DECLARATION_FALSE_FIELDS = [
    '"final_write_authorization_still_required": true',
    '"actual_write_authorized": false',
    '"production_evidenceitem_creation_authorized": false',
    '"ready_for_actual_write": false',
]

FORBIDDEN_DECLARATION_TERMS = [
    "raw rows",
    "raw comments",
    "raw author IDs",
    "raw author names",
    "private messages",
    "secrets/tokens/cookies/sessions/passwords/salts",
    ".env values",
    "arbitrary filesystem paths",
    "production package row contents",
    "evidence_items.jsonl contents",
    "evidence_items.csv contents",
    "source_manifest row contents",
    "collection_log row contents",
    "write execution payload",
    "route/API/frontend trigger payload",
    "production case payload",
    "production analysis_run payload",
    "production Analysis Result payload",
    "Source 11 payload",
    "FinalSummaryReport payload",
    "export/download/public/final-delivery payload",
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

UNSAFE_IDENTITY_PROMPTS = [
    "legal name",
    "personal address",
    "phone number",
    "personal email",
    "government ID",
    "credential token",
    "signature image",
    "raw PII",
    "private proof files",
]

ROUTE_FRONTEND_SETTER_TOKENS = [
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "final_write_authorization_performed",
    "ready_for_actual_write",
    "actual_write_authorized",
    "production_evidenceitem_creation_authorized",
    "approve_write",
    "final_authorize_write",
    "create production EvidenceItem",
    "perform actual Evidence Layer write",
]

POSITIVE_OVERCLAIM_PATTERNS = [
    "actual Evidence Layer write " + "approved",
    "actual Evidence Layer write " + "performed",
    "helper execution that writes " + "approved",
    "persisted Evidence Layer record " + "created",
    "production EvidenceItem " + "approved",
    "production EvidenceItem " + "created",
    "write authorization object " + "permits write",
    "runtime human authority validation " + "performed",
    "human authority " + "validated",
    "manual review responsibility " + "accepted",
    "runtime manual review responsibility acceptance " + "performed",
    "final write authorization " + "performed",
    "ready for " + "actual write",
    "actual_write_authorized = " + "true",
    "production_evidenceitem_creation_authorized = " + "true",
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

ALLOWED_NEGATIVE_MARKERS = (
    " no",
    "= no",
    "= false",
    "false",
    "not ",
    "no ",
    "does not",
    "must not",
    "forbidden",
    "negative",
    "blocked",
    "inactive",
    "tests-only",
    "not authorize",
    "not approval",
    "not ready",
    "remains absent",
    "remains separate",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_existing(paths: list[Path]) -> dict[Path, str]:
    return {path: _read(path) for path in paths if path.exists()}


def _joined(paths: list[Path]) -> str:
    return "\n".join(_read(path) for path in paths)


def _assert_contains_all(text: str, required: list[str], *, label: str) -> None:
    missing = [item for item in required if item not in text]
    assert not missing, f"{label} missing required text: {missing}"


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


def _heading_before(lines: list[str], index: int) -> str:
    for cursor in range(index, -1, -1):
        line = lines[cursor].strip()
        if line.startswith("#"):
            return line
    return ""


def _route_sources() -> dict[Path, str]:
    route_dir = REPO_ROOT / "backend" / "app" / "api" / "v1" / "routes"
    return {path: _read(path) for path in route_dir.glob("*.py")}


def _target_surface_sources() -> dict[Path, str]:
    sources = dict(_route_sources())
    sources.update(_read_existing(TARGET_FRONTEND_FILES))
    return sources


def _assert_no_active_tokens(sources: dict[Path, str], tokens: list[str], *, label: str) -> None:
    hits: list[str] = []
    for path, source in sources.items():
        for token in tokens:
            if token in source:
                hits.append(f"{path}: {token}")
    assert not hits, f"{label} active token hits: {hits}"


def _assert_no_positive_overclaim(paths: list[Path]) -> None:
    for path in paths:
        if not path.exists():
            continue
        for line in _read(path).splitlines():
            normalized = line.strip().lower()
            for claim in POSITIVE_OVERCLAIM_PATTERNS:
                if claim not in line:
                    continue
                assert any(marker in normalized for marker in ALLOWED_NEGATIVE_MARKERS), f"{path}: {line}"


def test_9a8_docs_exist_and_are_docs_only() -> None:
    for path in NINE_A8_DOCS:
        assert path.exists(), path

    joined = _joined(NINE_A8_DOCS)
    _assert_contains_all(
        joined,
        [
            "docs_only = yes",
            "docs-only",
            "human_authority_validated = no",
            "manual_review_responsibility_accepted = no",
            "final_write_authorization_performed = no",
            "ready_for_actual_write = no",
            "actual_write_ready_now = no",
            "production_evidenceitem_creation_ready_now = no",
            "ready_for_9A_9_actual_evidence_layer_write_production_evidenceitem_human_authority_declaration_safety_contract_tests_only",
            NINE_A9_PHRASE,
            "Inactive future phrase",
            "Source 11 update = no",
        ],
        label="9A-8 docs",
    )


def test_9a9_phrase_is_tests_only_and_not_authorization() -> None:
    scan_paths = [*NINE_A8_DOCS, Path(__file__)]
    if NINE_A9_REPORT.exists():
        scan_paths.append(NINE_A9_REPORT)

    joined = "\n".join(_read(path) for path in scan_paths)
    assert NINE_A9_PHRASE in joined

    for path in scan_paths:
        text = _read(path)
        if NINE_A9_PHRASE not in text:
            continue
        if path == Path(__file__):
            continue
        for context in _nearby_context(text, NINE_A9_PHRASE):
            normalized = context.lower()
            assert (
                "tests-only" in normalized
                or "inactive" in normalized
                or "report" in normalized
                or "phrase_scope" in normalized
            ), f"{path} has unsafe 9A-9 phrase context: {context}"

    docs_and_report = "\n".join(_read(path) for path in scan_paths if path != Path(__file__))
    forbidden_authorization_claims = [
        "authorizes actual Evidence Layer write",
        "authorizes runtime human authority validation",
        "authorizes manual review responsibility acceptance",
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
    for claim in forbidden_authorization_claims:
        assert claim not in docs_and_report


def test_9a8_phrase_is_historical_docs_only_context_if_present() -> None:
    joined = _joined(NINE_A8_DOCS)
    assert NINE_A8_PHRASE in joined

    for context in _nearby_context(joined, NINE_A8_PHRASE):
        normalized = context.lower()
        assert "docs-only" in normalized or "declaration gate" in normalized, context


def test_declaration_schema_scope_and_false_flags_are_non_authorizing() -> None:
    template = _read(NINE_A8_TEMPLATE)
    _assert_contains_all(
        template,
        [
            '"declaration_schema": "sentigraph_actual_evidence_layer_write_human_authority_declaration_v0_1"',
            '"declaration_scope": "docs_only_declaration_gate"',
            '"human_authority_identity_label": "not_validated_by_codex"',
            '"authority_basis": "not_validated_by_codex"',
            '"manual_review_responsibility_label": "not_accepted_by_codex"',
            '"warning_count_acknowledgment": "required_later"',
            '"human_review_required_acknowledgment": "required_later"',
            '"no_automatic_trust_upgrade_acknowledgment": "required_later"',
            *DECLARATION_FALSE_FIELDS,
        ],
        label="9A-8 declaration template",
    )


def test_codex_authority_boundary_remains_explicit() -> None:
    joined = _joined(NINE_A8_DOCS)
    _assert_contains_all(
        joined,
        [
            "Codex cannot fabricate human authority",
            "Codex cannot accept manual review responsibility on behalf of the user",
            "Codex cannot convert a docs-only declaration into write authorization",
            "Codex cannot declare production write permission for the user",
            "must come from an explicit human outside Codex",
            "must not include real person PII",
        ],
        label="Codex authority boundary",
    )


def test_safe_labels_only_and_no_real_identity_prompts() -> None:
    joined = _joined(NINE_A8_DOCS)
    _assert_contains_all(joined, SAFE_LABELS, label="safe placeholder labels")

    template = _read(NINE_A8_TEMPLATE)
    for unsafe_prompt in UNSAFE_IDENTITY_PROMPTS:
        assert unsafe_prompt not in template


def test_forbidden_fields_are_only_in_forbidden_or_negative_sections() -> None:
    for path in NINE_A8_DOCS:
        lines = _read(path).splitlines()
        for index, line in enumerate(lines):
            lowered_line = line.lower()
            for term in FORBIDDEN_DECLARATION_TERMS:
                if term.lower() not in lowered_line:
                    continue
                heading = _heading_before(lines, index).lower()
                nearby_prefix = "\n".join(lines[max(0, index - 24) : index + 1]).lower()
                assert (
                    "forbidden" in heading
                    or "forbidden" in lowered_line
                    or "forbidden future inputs" in nearby_prefix
                    or "must not" in lowered_line
                    or "not contain" in lowered_line
                    or lowered_line.startswith("- no ")
                    or "no raw" in lowered_line
                    or "negative" in lowered_line
                ), f"{path}:{index + 1}: active forbidden term context: {line}"


def test_no_route_api_or_frontend_can_set_authority_responsibility_or_write() -> None:
    surface_sources = _target_surface_sources()
    assert surface_sources, "targeted route/frontend surfaces should be discoverable"
    _assert_no_active_tokens(
        surface_sources,
        ROUTE_FRONTEND_SETTER_TOKENS,
        label="route/API/frontend authority responsibility or write surface",
    )


def test_9a4_no_write_candidate_remains_static_and_compatible() -> None:
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

    import_lines = [
        line.strip()
        for line in helper.splitlines()
        if line.startswith("import ") or line.startswith("from ")
    ]
    for forbidden_import in [
        "controlled_evidenceitem_evidence_layer_write_runtime",
        "evidence_import",
        "evidence_ingestion",
    ]:
        assert all(forbidden_import not in line for line in import_lines), forbidden_import

    for unsafe in [
        '"ready_for_actual_write": True',
        '"human_authority_validated": True',
        '"final_write_authorization_performed": True',
        '"actual_evidence_layer_write_authorized": True',
        '"production_evidenceitem_creation_authorized": True',
    ]:
        assert unsafe not in helper


def test_8w_source11_and_review_console_separation_remains_preserved() -> None:
    joined = "\n".join([_joined(NINE_A8_DOCS), _joined(NINE_A7_DOCS)])
    _assert_contains_all(
        joined,
        [
            "8W-69 pause remains preserved",
            "8W-70 reactivation remains not selected",
            "9A write-readiness discussion does not satisfy production Analysis Result authorization protocol",
            "Source 11 / FinalSummaryReport runtime remains separate",
            "Source 11 update = no",
            "review console remains no-write",
            "No write button",
        ],
        label="8W Source 11 and review console separation",
    )


def test_future_9a10_phrase_if_present_is_inactive_docs_only() -> None:
    scan_paths = [Path(__file__)]
    if NINE_A9_REPORT.exists():
        scan_paths.append(NINE_A9_REPORT)
    joined = "\n".join(_read(path) for path in scan_paths)
    if NINE_A10_FUTURE_PHRASE not in joined:
        return
    for context in _nearby_context(joined, NINE_A10_FUTURE_PHRASE):
        normalized = context.lower()
        assert "inactive" in normalized and "docs-only" in normalized, context


def test_new_tests_and_report_have_no_positive_readiness_overclaim() -> None:
    scan_paths = [Path(__file__)]
    if NINE_A9_REPORT.exists():
        scan_paths.append(NINE_A9_REPORT)
    _assert_no_positive_overclaim(scan_paths)
