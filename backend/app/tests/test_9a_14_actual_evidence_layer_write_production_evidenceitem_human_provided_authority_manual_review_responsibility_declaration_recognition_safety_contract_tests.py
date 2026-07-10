from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

NINE_A13_PHRASE = (
    "APPROVE_9A_13_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_GATE_DOCS_ONLY"
)
NINE_A14_PHRASE = (
    "APPROVE_9A_14_ACTUAL_EVIDENCE_LAYER_WRITE_PRODUCTION_EVIDENCEITEM_"
    "HUMAN_PROVIDED_AUTHORITY_MANUAL_REVIEW_RESPONSIBILITY_DECLARATION_RECOGNITION_"
    "SAFETY_CONTRACT_TESTS_ONLY"
)

NINE_A13_PLANNING = (
    REPO_ROOT
    / "docs"
    / "planning"
    / "sentigraph_9a_13_actual_evidence_layer_write_production_evidenceitem_human_provided_authority_manual_review_responsibility_declaration_gate_decision_v0_1.md"
)
NINE_A13_RECOGNITION_CONTRACT = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_human_provided_authority_manual_review_responsibility_declaration_recognition_contract_v0_1.md"
)
NINE_A13_CHECKLIST = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_human_provided_declaration_recognition_checklist_v0_1.md"
)
NINE_A14_FUTURE_GATE = (
    REPO_ROOT
    / "docs"
    / "architecture"
    / "sentigraph_actual_evidence_layer_write_production_evidenceitem_future_human_provided_declaration_recognition_safety_contract_tests_gate_v0_1.md"
)
NINE_A14_REPORT = (
    REPO_ROOT
    / "docs"
    / "health"
    / "sentigraph_9a_14_actual_evidence_layer_write_production_evidenceitem_human_provided_authority_manual_review_responsibility_declaration_recognition_safety_contract_tests_report_v0_1.md"
)

NINE_A13_DOCS = [
    NINE_A13_PLANNING,
    NINE_A13_RECOGNITION_CONTRACT,
    NINE_A13_CHECKLIST,
    NINE_A14_FUTURE_GATE,
]

TARGET_FRONTEND_FILES = [
    REPO_ROOT / "frontend" / "src" / "api" / "sentigraphApi.js",
    REPO_ROOT / "frontend" / "src" / "pages" / "InternalAlphaReviewConsole.jsx",
    REPO_ROOT / "frontend" / "src" / "App.jsx",
    REPO_ROOT / "frontend" / "src" / "components" / "layout" / "AppShell.jsx",
]

SAFE_SOURCE_KINDS = [
    "explicit_human_message_later",
    "separately_governed_external_audit_note_later",
]
NEVER_SUFFICIENT_SOURCES = [
    "Codex-generated text",
    "a copied template filled by Codex",
    "approval phrase",
    '"continue"',
    '"approved"',
    '"ready"',
    "commit/push confirmation",
    "implicit project-owner assumption",
    "prior fixture output",
    "route/UI action",
    "environment variable",
    "machine-generated signature",
]
SAFE_LABELS = [
    "self_declared_project_owner_role",
    "self_declared_designated_reviewer_role",
    "self_declared_organization_reviewer_role",
    "authority_basis_not_independently_validated",
    "external_audit_reference_required_later",
    "not_specified",
]
ALLOWED_OUTCOMES = [
    "declaration_missing",
    "declaration_insufficient",
    "declaration_ambiguous",
    "declaration_present_for_docs_only_review",
    "privacy_issue_stop",
    "pause",
]
FORBIDDEN_OUTCOMES = [
    "authority_validated",
    "responsibility_accepted",
    "final_authorization_complete",
    "ready_for_write",
    "write_approved",
    "production_ready",
]
REQUIRED_COMPONENTS = [
    "statement that the declaration comes from a human",
    "safe declared role label",
    "safe authority-basis label",
    "manual review responsibility statement",
    "warning_count acknowledgment",
    "human_review_required acknowledgment",
    "no_automatic_trust_upgrade acknowledgment",
    "blocker review statement",
    "risk review statement",
    "input-lineage review statement",
    "raw/private/secret absence acknowledgment",
    "rollback / pause / revocation responsibility statement",
    "final write authorization is still required",
    "actual write is not authorized by the declaration",
    "production EvidenceItem creation is not authorized by the declaration",
    "system is not ready for actual write",
]
INSUFFICIENCY_BLOCKERS = [
    "no separate human-supplied source exists",
    "content generated entirely by Codex",
    "only a phase approval phrase is supplied",
    "role label missing",
    "authority-basis label missing",
    "manual review responsibility statement missing or ambiguous",
    "required acknowledgments missing",
    "blockers or risks not addressed",
    "lineage status absent",
    "raw/private/secret absence not acknowledged",
    "rollback/pause responsibility missing",
    "wording claims actual write, final authorization, production EvidenceItem readiness, or automatic trust upgrade",
    "wording attempts to authorize production case, analysis_run, Analysis Result, Source 11, FinalSummaryReport, or public delivery",
    "wording contains real-person PII or secrets",
    "scope ambiguous",
    "declaration presented as route/UI/runtime trigger",
    "unresolved blocker remains",
]
PII_FORBIDDEN_TERMS = [
    "legal names",
    "personal addresses",
    "personal phone numbers",
    "personal email addresses",
    "government IDs",
    "signature images",
    "credential tokens",
    "employment documents",
    "private proof files",
    "raw PII",
]
ROUTE_FRONTEND_SETTER_TOKENS = [
    "declaration_acceptance",
    "set_declaration",
    "submit_declaration",
    "human_authority_validated",
    "manual_review_responsibility_accepted",
    "final_write_authorization_performed",
    "actual_write_authorized",
    "production_evidenceitem_creation_authorized",
    "ready_for_actual_write",
    "approve_write",
    "final_authorize_write",
    "perform actual Evidence Layer write",
    "create production EvidenceItem",
]
ACTIVE_POSITIVE_PATTERNS = [
    "approval phrase is a declaration",
    "Codex supplied the declaration",
    "human_declaration_received_now = yes",
    "human_declaration_record_created = yes",
    "human_authority_validated = yes",
    "manual_review_responsibility_accepted = yes",
    "final_write_authorization_performed = yes",
    "ready_for_actual_write = yes",
    "actual_evidence_layer_write_approved = yes",
    "production_evidenceitem_creation_approved = yes",
    "actual_write_authorized = true",
    "production_evidenceitem_creation_authorized = true",
    "human_authority_validated = true",
    "manual_review_responsibility_accepted = true",
    "final_write_authorization_performed = true",
    "actual write approved",
    "actual write performed",
    "production EvidenceItem approved",
    "production EvidenceItem created",
    "final authorization performed",
    "ready-for-write",
    "production-ready",
    "public-ready",
    "customer-ready",
    "operator-runtime-ready",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _scan_paths() -> list[Path]:
    paths = [*NINE_A13_DOCS, Path(__file__)]
    if NINE_A14_REPORT.exists():
        paths.append(NINE_A14_REPORT)
    return paths


def _joined(paths: list[Path]) -> str:
    return "\n".join(_read(path) for path in paths)


def _assert_contains_all(text: str, required: list[str], *, label: str) -> None:
    missing = [item for item in required if item not in text]
    assert not missing, f"{label} missing required text: {missing}"


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
    for path in TARGET_FRONTEND_FILES:
        if path.exists():
            sources[path] = _read(path)
    return sources


def test_required_9a13_files_exist() -> None:
    for path in NINE_A13_DOCS:
        assert path.exists(), path


def test_9a13_remains_docs_only_and_non_authorizing() -> None:
    planning = _read(NINE_A13_PLANNING)
    _assert_contains_all(
        planning,
        [
            "docs_only = yes",
            "approval_phrase_is_human_declaration = no",
            "codex_generated_text_is_human_declaration = no",
            "human_declaration_received_now = no",
            "human_declaration_record_created = no",
            "human_authority_validated = no",
            "manual_review_responsibility_accepted = no",
            "final_write_authorization_performed = no",
            "ready_for_actual_write = no",
            "actual_evidence_layer_write_approved = no",
            "production_evidenceitem_creation_approved = no",
        ],
        label="9A-13 decision fields",
    )


def test_exact_9a14_phrase_remains_tests_only() -> None:
    assert NINE_A14_PHRASE in _joined(_scan_paths())

    for path in _scan_paths():
        if path == Path(__file__):
            continue
        text = _read(path)
        if NINE_A14_PHRASE not in text:
            continue
        for context in _nearby_context(text, NINE_A14_PHRASE):
            normalized = context.lower()
            assert (
                "inactive" in normalized
                or "tests-only" in normalized
                or "tests_only" in normalized
                or "report" in normalized
                or "phrase_scope" in normalized
            ), f"{path} has unsafe 9A-14 phrase context: {context}"
            assert "must not authorize" in normalized or "not approval" in normalized or "tests-only" in normalized


def test_9a13_phrase_is_historical_docs_only_context_if_present() -> None:
    for path in _scan_paths():
        if path == Path(__file__):
            continue
        text = _read(path)
        if NINE_A13_PHRASE not in text:
            continue
        for context in _nearby_context(text, NINE_A13_PHRASE):
            normalized = context.lower()
            assert "docs-only" in normalized or "9a-13" in normalized or "historical" in normalized, context


def test_declaration_source_kinds_are_narrow_and_never_sufficient_sources_are_listed() -> None:
    docs = _joined(NINE_A13_DOCS)
    _assert_contains_all(docs, SAFE_SOURCE_KINDS, label="safe source kinds")
    _assert_contains_all(docs, NEVER_SUFFICIENT_SOURCES, label="never sufficient sources")
    assert "Codex-generated text is not declaration" in _read(NINE_A13_CHECKLIST)


def test_codex_authority_boundary_remains_explicit() -> None:
    docs = _joined(NINE_A13_DOCS)
    _assert_contains_all(
        docs,
        [
            "Codex cannot fabricate human authority",
            "Codex cannot infer authority from approval phrases",
            "Codex cannot accept manual-review responsibility on behalf of a user",
            "Codex cannot validate identity, employment, legal power, organizational delegation, or signature authenticity",
            "Codex can only classify whether later human-supplied text contains",
            "Presence/sufficiency classification is not identity validation",
            "authority validation",
            "responsibility acceptance",
            "final authorization",
            "write permission",
        ],
        label="Codex authority boundary",
    )


def test_safe_role_and_basis_labels_remain_non_pii_and_self_declared() -> None:
    docs = _joined(NINE_A13_DOCS)
    _assert_contains_all(docs, SAFE_LABELS, label="safe labels")
    _assert_contains_all(
        docs,
        [
            "non-PII",
            "self-declared",
            "These labels are not verified authority",
            "These labels must not be described as verified authority",
        ],
        label="safe-label caveats",
    )
    assert "independently verified authority" not in docs


def test_recognition_outcomes_remain_conservative() -> None:
    docs = _joined(NINE_A13_DOCS)
    _assert_contains_all(docs, ALLOWED_OUTCOMES, label="allowed outcomes")
    _assert_contains_all(docs, FORBIDDEN_OUTCOMES, label="forbidden outcomes catalog")

    for path in NINE_A13_DOCS:
        lines = _read(path).splitlines()
        for index, line in enumerate(lines):
            for outcome in FORBIDDEN_OUTCOMES:
                if outcome not in line:
                    continue
                heading = _heading_before(lines, index).lower()
                nearby = "\n".join(lines[max(0, index - 12) : index + 1]).lower()
                assert (
                    "forbidden" in heading
                    or "forbidden outcomes" in nearby
                    or "do not use" in nearby
                    or "must not" in nearby
                    or "= no" in line.lower()
                    or "= false" in line.lower()
                    or "does not include" in nearby
                    or "non-authorizing" in nearby
                ), f"{path}:{index + 1}: active forbidden outcome context: {line}"


def test_required_declaration_components_remain_complete() -> None:
    checklist = _read(NINE_A13_CHECKLIST)
    _assert_contains_all(checklist, REQUIRED_COMPONENTS, label="required declaration components")


def test_insufficiency_blockers_remain_complete() -> None:
    checklist = _read(NINE_A13_CHECKLIST)
    _assert_contains_all(checklist, INSUFFICIENCY_BLOCKERS, label="insufficiency blockers")


def test_pii_privacy_protections_remain_explicit_and_no_actual_pii_values_are_present() -> None:
    docs = _joined(NINE_A13_DOCS)
    _assert_contains_all(docs, PII_FORBIDDEN_TERMS, label="PII forbidden catalog")

    for path in NINE_A13_DOCS:
        lines = _read(path).splitlines()
        for index, line in enumerate(lines):
            for term in PII_FORBIDDEN_TERMS:
                if term not in line:
                    continue
                heading = _heading_before(lines, index).lower()
                nearby = "\n".join(lines[max(0, index - 4) : index + 1]).lower()
                assert (
                    "privacy" in heading
                    or "forbidden" in heading
                    or "stop" in heading
                    or "must not request or store" in nearby
                    or "request or store" in nearby
                ), f"{path}:{index + 1}: active PII context: {line}"

    actual_value_patterns = [
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        r"\b\+?\d[\d .()\-]{7,}\d\b",
        r"BEGIN (RSA|OPENSSH|PRIVATE) KEY",
        r"sk-[A-Za-z0-9]",
        r"xox[baprs]-",
    ]
    for pattern in actual_value_patterns:
        assert not re.search(pattern, docs), pattern


def test_no_route_api_or_frontend_setter_exists_for_declaration_authority_or_write() -> None:
    surface_sources = _target_surface_sources()
    assert surface_sources, "route/API/frontend sources should be discoverable"

    hits: list[str] = []
    for path, source in surface_sources.items():
        lowered_source = source.lower()
        for token in ROUTE_FRONTEND_SETTER_TOKENS:
            if token.lower() in lowered_source:
                hits.append(f"{path}: {token}")
    assert not hits, f"active route/API/frontend setter hits: {hits}"

    for path, source in surface_sources.items():
        assert NINE_A13_PHRASE not in source, path
        assert NINE_A14_PHRASE not in source, path


def test_no_active_positive_declaration_write_or_production_claims() -> None:
    paths = [*NINE_A13_DOCS]
    if NINE_A14_REPORT.exists():
        paths.append(NINE_A14_REPORT)
    docs = _joined(paths)
    for pattern in ACTIVE_POSITIVE_PATTERNS:
        assert pattern not in docs, pattern
