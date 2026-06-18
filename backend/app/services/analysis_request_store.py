from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from app.schemas.analysis_request import (
    AnalysisRequestCancelResult,
    AnalysisRequestConfig,
    AnalysisRequestCreate,
    AnalysisRequestFile,
    AnalysisRequestRecord,
    CaseDraftHandoff,
    CaseDraftPackageReference,
    CaseDraftProviderSummary,
    CaseDraftReadiness,
    EvidenceImportPlan,
    EvidenceImportPlanReadiness,
    ProviderJobResult,
)


ANALYSIS_REQUESTS_ENV_VAR = "SENTIGRAPH_ANALYSIS_REQUESTS_DIR"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ROOT = PROJECT_ROOT / "runtime" / "analysis_requests"
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


class AnalysisRequestStoreError(Exception):
    pass


class AnalysisRequestNotFoundError(AnalysisRequestStoreError):
    pass


class AnalysisRequestValidationError(AnalysisRequestStoreError):
    pass


def get_analysis_request_config() -> AnalysisRequestConfig:
    root = _request_root()
    requests_dir = root / "requests"
    results_dir = root / "results"
    return AnalysisRequestConfig(
        configured_by_env=bool(os.environ.get(ANALYSIS_REQUESTS_ENV_VAR, "").strip()),
        root_exists=root.exists(),
        requests_dir_exists=requests_dir.exists(),
        results_dir_exists=results_dir.exists(),
        request_count=_json_count(requests_dir),
        result_count=_json_count(results_dir),
        root_label=_safe_root_label(root),
    )


def create_analysis_request(payload: AnalysisRequestCreate) -> AnalysisRequestRecord:
    root = _ensure_root()
    request_id = _new_request_id(payload.case_seed.title)
    output = payload.output.model_copy()
    if not output.package_slug:
        output.package_slug = _slugify(payload.case_seed.title) or request_id
    request = AnalysisRequestFile(
        request_id=request_id,
        created_by=payload.created_by or "sentigraph_local_user",
        case_seed=payload.case_seed,
        sampling_plan=payload.sampling_plan,
        safety_policy=payload.safety_policy,
        privacy_policy=payload.privacy_policy,
        output=output,
        sentigraph_metadata={
            "request_status": "draft",
            "provider_execution": "outside_sentigraph_core",
            "collector_jobs_run": False,
            "real_api_calls": False,
            "url_fetching": False,
            "scraping": False,
        },
    )
    _write_json(root / "requests" / f"{request_id}.json", request.model_dump(mode="json", by_alias=True))
    return read_analysis_request(request_id)


def list_analysis_requests() -> list[AnalysisRequestRecord]:
    root = _ensure_root()
    records: list[AnalysisRequestRecord] = []
    for path in sorted((root / "requests").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            records.append(_record_from_path(path))
        except AnalysisRequestValidationError:
            continue
    return records


def read_analysis_request(request_id: str) -> AnalysisRequestRecord:
    request_path = _request_path(request_id)
    if not request_path.exists():
        raise AnalysisRequestNotFoundError(f"Analysis request {request_id} was not found.")
    return _record_from_path(request_path)


def cancel_analysis_request(request_id: str) -> AnalysisRequestCancelResult:
    record = read_analysis_request(request_id)
    if record.provider_result and record.provider_result.status == "package_ready":
        return AnalysisRequestCancelResult(
            request_id=request_id,
            status=record.request_status,
            request=record.request,
            warning="Provider result is already package_ready; local cancel did not call provider or change provider state.",
        )

    metadata = dict(record.request.sentigraph_metadata or {})
    metadata.update(
        {
            "request_status": "canceled",
            "canceled_at": datetime.now(timezone.utc).isoformat(),
            "provider_cancel_called": False,
            "collector_jobs_run": False,
        }
    )
    updated = record.request.model_copy(update={"sentigraph_metadata": metadata})
    _write_json(_request_path(request_id), updated.model_dump(mode="json", by_alias=True))
    return AnalysisRequestCancelResult(request_id=request_id, status="canceled", request=updated)


def read_case_draft_handoff(request_id: str) -> CaseDraftHandoff:
    draft_path = _case_draft_path(request_id)
    if not draft_path.exists():
        raise AnalysisRequestNotFoundError(f"Case draft handoff for {request_id} was not found.")
    try:
        parsed = json.loads(draft_path.read_text(encoding="utf-8-sig"))
        return CaseDraftHandoff.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{draft_path.name} is not a valid case draft handoff: {type(exc).__name__}") from exc


def list_case_draft_handoffs() -> list[CaseDraftHandoff]:
    root = _ensure_root()
    drafts: list[CaseDraftHandoff] = []
    for path in sorted((root / "case_drafts").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            drafts.append(CaseDraftHandoff.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return drafts


def create_case_draft_handoff(request_id: str) -> CaseDraftHandoff:
    draft_path = _case_draft_path(request_id)
    if draft_path.exists():
        return read_case_draft_handoff(request_id)

    record = read_analysis_request(request_id)
    _validate_case_draft_eligibility(record)
    result = record.provider_result
    assert result is not None

    draft = CaseDraftHandoff(
        draft_id=f"draft_{request_id}",
        request_id=request_id,
        case_seed=record.request.case_seed,
        provider_summary=CaseDraftProviderSummary(
            provider_job_id=result.provider_job_id,
            provider_type=result.provider_type,
            status=result.status,
            safety_status=result.safety_status,
        ),
        package_reference=CaseDraftPackageReference(
            package_name=result.package_name,
            package_role=result.package_role,
            package_path=result.package_path,
            package_index_path=result.package_index_path,
        ),
        counts=result.counts,
        validation=result.validation,
        coverage=result.coverage,
        privacy=result.privacy,
        readiness=CaseDraftReadiness(
            state="ready_for_manual_review",
            can_import_evidence=False,
            requires_human_review=True,
            reason="Provider result is validation_warn/package_ready but evidence import is not automatic.",
        ),
        boundary_notes=[
            "Provider output is evidence metadata, not official truth.",
            "Draft creation does not import evidence rows.",
            "Draft creation does not run analysis, generate reports, or create public event pages.",
            "Coverage is selected/controlled available evidence, not full-web or full-platform coverage.",
        ],
        recommended_next_steps=[
            "Review provider result and coverage note.",
            "Run or open the external package validator manually if needed.",
            "Decide whether to import the package into the Evidence layer.",
            "If imported, mark review_status and verification_status clearly.",
            "Only after manual review generate public event sample, Sandbox fixture, or B-end report draft.",
        ],
    )
    _write_json(draft_path, draft.model_dump(mode="json", by_alias=True))
    return read_case_draft_handoff(request_id)


def read_evidence_import_plan(request_id: str) -> EvidenceImportPlan:
    plan_path = _import_plan_path(request_id)
    if not plan_path.exists():
        raise AnalysisRequestNotFoundError(f"Evidence import plan for {request_id} was not found.")
    try:
        parsed = json.loads(plan_path.read_text(encoding="utf-8-sig"))
        return EvidenceImportPlan.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{plan_path.name} is not a valid evidence import plan: {type(exc).__name__}") from exc


def list_evidence_import_plans() -> list[EvidenceImportPlan]:
    root = _ensure_root()
    plans: list[EvidenceImportPlan] = []
    for path in sorted((root / "import_plans").glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        try:
            parsed = json.loads(path.read_text(encoding="utf-8-sig"))
            plans.append(EvidenceImportPlan.model_validate(parsed))
        except (OSError, json.JSONDecodeError, ValidationError):
            continue
    return plans


def create_evidence_import_plan(request_id: str) -> EvidenceImportPlan:
    plan_path = _import_plan_path(request_id)
    if plan_path.exists():
        return read_evidence_import_plan(request_id)

    draft = read_case_draft_handoff(request_id)
    _validate_import_plan_eligibility(draft)

    plan = EvidenceImportPlan(
        plan_id=f"import_plan_{request_id}",
        draft_id=draft.draft_id,
        request_id=request_id,
        package_reference=draft.package_reference,
        counts=draft.counts,
        validation=draft.validation,
        coverage=draft.coverage,
        privacy=draft.privacy,
        readiness=EvidenceImportPlanReadiness(
            state="ready_for_manual_import_review",
            can_import_now=False,
            requires_human_review=True,
            reason="Import plan only. Evidence rows are not imported automatically.",
        ),
        manual_review_checklist=[
            "Review coverage_note and validation_report before any import.",
            "Confirm the package is a selected/controlled public sample, not full-web coverage.",
            "Confirm privacy flags are present.",
            "Confirm raw author ids/names/profile URLs/private messages are not included.",
            "Confirm evidence should default to review_needed.",
            "Confirm verification_status should default to source_url_provided_unverified unless official API proof exists.",
            "Confirm trust_label should default to medium_low unless upgraded by human review.",
            "Confirm duplicate folding/dedup should run before analysis.",
            "Confirm rejected/weak evidence must not amplify risk.",
            "Confirm no report, Sandbox fixture, or public event page should be generated before import review.",
        ],
        blockers=[],
        boundary_notes=[
            "This is an Evidence import plan only; no evidence rows are imported.",
            "No production case is created by this plan.",
            "No analysis, report, Sandbox fixture, or public event page is generated by this plan.",
            "Provider output is evidence, not official truth.",
            "Coverage remains a selected/controlled available evidence sample, not full-web or full-platform coverage.",
        ],
        recommended_next_steps=[
            "Human reviewer opens the package README, coverage note, and validation report.",
            "Decide whether to import evidence rows into the Evidence layer.",
            "Choose an import target case or create a new case manually in a later task.",
            "Run deduplication and review queue after import.",
            "Only after evidence governance generate analysis, public event page, Sandbox fixture, or B-end report.",
        ],
    )
    _write_json(plan_path, plan.model_dump(mode="json", by_alias=True))
    return read_evidence_import_plan(request_id)


def _record_from_path(path: Path) -> AnalysisRequestRecord:
    try:
        parsed = json.loads(path.read_text(encoding="utf-8-sig"))
        request = AnalysisRequestFile.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise AnalysisRequestValidationError(f"{path.name} is not a valid analysis request: {type(exc).__name__}") from exc

    result, result_warning, result_file = _read_result(request.request_id)
    request_status = str((request.sentigraph_metadata or {}).get("request_status") or "draft")
    stat = path.stat()
    return AnalysisRequestRecord(
        request_id=request.request_id,
        request=request,
        request_status=request_status,
        request_file=f"runtime/analysis_requests/requests/{path.name}",
        result_file=f"runtime/analysis_requests/results/{result_file.name}" if result_file else None,
        provider_result=result,
        result_warning=result_warning,
        provider_status=result.status if result else None,
        safety_status=result.safety_status if result else None,
        package_name=result.package_name if result else None,
        created_at=request.created_at,
        updated_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
    )


def _read_result(request_id: str) -> tuple[ProviderJobResult | None, str | None, Path | None]:
    result_path = _result_path(request_id)
    if not result_path.exists():
        return None, None, None
    try:
        parsed = json.loads(result_path.read_text(encoding="utf-8-sig"))
        result = ProviderJobResult.model_validate(parsed)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        return None, f"Matching provider result JSON is invalid: {type(exc).__name__}", result_path
    if result.request_id != request_id:
        return None, "Matching provider result request_id does not match file name.", result_path
    return result, None, result_path


def _validate_case_draft_eligibility(record: AnalysisRequestRecord) -> None:
    if record.result_warning:
        raise AnalysisRequestValidationError(f"Cannot create case draft: provider result is invalid ({record.result_warning}).")
    result = record.provider_result
    if not result:
        raise AnalysisRequestValidationError("Cannot create case draft: provider result is missing.")
    if result.status not in {"package_ready", "validation_warn"}:
        raise AnalysisRequestValidationError(f"Cannot create case draft: provider status {result.status} is not eligible.")
    if result.safety_status not in {"safe", "medium"}:
        raise AnalysisRequestValidationError(f"Cannot create case draft: safety status {result.safety_status} is not eligible.")
    if result.validation.errors > 0:
        raise AnalysisRequestValidationError("Cannot create case draft: provider validation errors must be 0.")
    if not result.package_name:
        raise AnalysisRequestValidationError("Cannot create case draft: package_name is missing.")
    if result.counts.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create case draft: counts.evidence must be greater than 0.")

    raw = _read_result_payload(record.request_id)
    raw_privacy = raw.get("privacy") if isinstance(raw.get("privacy"), dict) else {}
    required_privacy = [
        "raw_author_ids_removed",
        "raw_author_names_removed",
        "profile_urls_removed",
        "private_messages_excluded",
    ]
    missing_privacy = [field for field in required_privacy if field not in raw_privacy]
    if missing_privacy:
        raise AnalysisRequestValidationError(f"Cannot create case draft: privacy fields missing ({', '.join(missing_privacy)}).")
    if not all(bool(raw_privacy.get(field)) for field in required_privacy):
        raise AnalysisRequestValidationError("Cannot create case draft: privacy flags must all be true.")

    raw_coverage = raw.get("coverage") if isinstance(raw.get("coverage"), dict) else {}
    required_coverage = ["not_full_web", "not_full_platform", "not_full_thread"]
    missing_coverage = [field for field in required_coverage if field not in raw_coverage]
    if missing_coverage:
        raise AnalysisRequestValidationError(f"Cannot create case draft: coverage limitation fields missing ({', '.join(missing_coverage)}).")
    if not all(bool(raw_coverage.get(field)) for field in required_coverage):
        raise AnalysisRequestValidationError("Cannot create case draft: coverage must not claim full-web/full-platform/full-thread coverage.")


def _validate_import_plan_eligibility(draft: CaseDraftHandoff) -> None:
    if draft.readiness.state not in {"ready_for_manual_review", "ready_for_manual_import_review"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: draft readiness {draft.readiness.state} is not eligible.")
    if draft.provider_summary.safety_status not in {"safe", "medium"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: safety status {draft.provider_summary.safety_status} is not eligible.")
    if not draft.package_reference.package_name:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: package_name is missing.")
    if draft.counts.evidence <= 0:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: counts.evidence must be greater than 0.")
    if draft.validation.status not in {"passed", "warn", "not_run"}:
        raise AnalysisRequestValidationError(f"Cannot create evidence import plan: validation status {draft.validation.status} is not eligible.")
    if draft.validation.errors > 0:
        raise AnalysisRequestValidationError("Cannot create evidence import plan: validation errors must be 0.")
    required_privacy = [
        draft.privacy.raw_author_ids_removed,
        draft.privacy.raw_author_names_removed,
        draft.privacy.profile_urls_removed,
        draft.privacy.private_messages_excluded,
    ]
    if not all(required_privacy):
        raise AnalysisRequestValidationError("Cannot create evidence import plan: privacy flags must all be true.")
    if not (draft.coverage.not_full_web and draft.coverage.not_full_platform and draft.coverage.not_full_thread):
        raise AnalysisRequestValidationError("Cannot create evidence import plan: coverage must not claim full-web/full-platform/full-thread coverage.")


def _read_result_payload(request_id: str) -> dict[str, Any]:
    result_path = _result_path(request_id)
    try:
        parsed = json.loads(result_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _request_root() -> Path:
    raw_value = os.environ.get(ANALYSIS_REQUESTS_ENV_VAR, "").strip()
    if raw_value:
        return Path(raw_value).expanduser().resolve()
    return DEFAULT_ROOT


def _ensure_root() -> Path:
    root = _request_root()
    (root / "requests").mkdir(parents=True, exist_ok=True)
    (root / "results").mkdir(parents=True, exist_ok=True)
    (root / "case_drafts").mkdir(parents=True, exist_ok=True)
    (root / "import_plans").mkdir(parents=True, exist_ok=True)
    return root


def _request_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "requests" / f"{request_id}.json"


def _result_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "results" / f"{request_id}.json"


def _case_draft_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "case_drafts" / f"{request_id}.json"


def _import_plan_path(request_id: str) -> Path:
    _validate_request_id(request_id)
    root = _ensure_root()
    return root / "import_plans" / f"{request_id}.json"


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def _validate_request_id(request_id: str) -> None:
    if not REQUEST_ID_PATTERN.fullmatch(request_id) or request_id in {".", ".."}:
        raise AnalysisRequestValidationError("Invalid request_id.")


def _new_request_id(title: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _slugify(title)[:40] or "analysis-request"
    return f"req_{timestamp}_{slug}_{uuid.uuid4().hex[:8]}"


def _slugify(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return text or "public-opinion-event"


def _json_count(path: Path) -> int:
    if not path.exists() or not path.is_dir():
        return 0
    return sum(1 for item in path.glob("*.json") if item.is_file())


def _safe_root_label(root: Path) -> str:
    try:
        relative = root.resolve().relative_to(PROJECT_ROOT.resolve())
        return str(relative).replace("\\", "/")
    except ValueError:
        return "configured_external_analysis_requests_dir"
