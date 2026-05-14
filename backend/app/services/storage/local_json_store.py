from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock
from typing import Any

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.common import RiskLevel
from app.schemas.report import PublicOpinionReport
from app.schemas.visualization import VisualizationResponse
from app.services.storage.base_store import CaseStore


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_CASE_STORE_PATH = PROJECT_ROOT / "backend" / "data" / "cases.json"


class LocalJsonCaseStore(CaseStore):
    """Project-local JSON case store for the mock-first MVP."""

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = _resolve_store_path(path or DEFAULT_CASE_STORE_PATH)
        self._lock = RLock()

    @classmethod
    def from_env(cls) -> "LocalJsonCaseStore":
        backend = os.getenv("CASE_STORE_BACKEND", "local_json").strip().lower()
        if backend != "local_json":
            # Future TODO: add MongoDB/Redis-backed implementations behind CaseStore.
            backend = "local_json"
        return cls(os.getenv("CASE_STORE_PATH") or DEFAULT_CASE_STORE_PATH)

    def create_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        with self._lock:
            data = self._read_data()
            data["cases"][case.case_id] = _case_to_json(case)
            self._write_data(data)
        return case.model_copy(deep=True)

    def list_cases(self) -> list[AnalysisCaseDetail]:
        with self._lock:
            data = self._read_data()
        return [AnalysisCaseDetail.model_validate(item) for item in data["cases"].values()]

    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        with self._lock:
            data = self._read_data()
            raw_case = data["cases"].get(case_id)
        return AnalysisCaseDetail.model_validate(raw_case) if raw_case else None

    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        with self._lock:
            data = self._read_data()
            if case.case_id not in data["cases"]:
                raise KeyError(f"Analysis case '{case.case_id}' does not exist.")
            data["cases"][case.case_id] = _case_to_json(case)
            self._write_data(data)
        return case.model_copy(deep=True)

    def save_analysis_result(
        self,
        case_id: str,
        *,
        analysis_result: AnalysisResultResponse,
        visualization_data: VisualizationResponse | None = None,
        risk_score: float | None = None,
        risk_level: RiskLevel | None = None,
        risk_model_version: str | None = None,
        updated_at: Any | None = None,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        updated_case = case.model_copy(
            update={
                "analysis_result": analysis_result,
                "visualization_data": visualization_data,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "risk_model_version": risk_model_version,
                "updated_at": updated_at or case.updated_at,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_report(
        self,
        case_id: str,
        *,
        report: PublicOpinionReport,
        updated_at: Any | None = None,
        markdown_available: bool = True,
    ) -> AnalysisCaseDetail | None:
        case = self.get_case(case_id)
        if not case:
            return None
        updated_case = case.model_copy(
            update={
                "report": report,
                "markdown_available": markdown_available,
                "risk_score": float(report.overall_risk if report.overall_risk is not None else report.risk_score),
                "risk_level": report.risk_level,
                "risk_model_version": report.risk_model_version,
                "updated_at": updated_at or case.updated_at,
            },
            deep=True,
        )
        return self.update_case(updated_case)

    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        with self._lock:
            data = self._read_data()
            data["markdown_reports"][case_id] = report.model_dump(mode="json")
            self._write_data(data)
        return report.model_copy(deep=True)

    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        with self._lock:
            data = self._read_data()
            raw_report = data["markdown_reports"].get(case_id)
        return MarkdownExportResponse.model_validate(raw_report) if raw_report else None

    def list_markdown_reports(self) -> list[MarkdownExportResponse]:
        with self._lock:
            data = self._read_data()
        return [MarkdownExportResponse.model_validate(item) for item in data["markdown_reports"].values()]

    def reset(self) -> None:
        with self._lock:
            if self.path.exists():
                self.path.unlink()

    def _read_data(self) -> dict[str, dict[str, Any]]:
        if not self.path.exists():
            return _empty_data()
        with self.path.open("r", encoding="utf-8") as file:
            raw = json.load(file)
        if not isinstance(raw, dict):
            return _empty_data()
        cases = raw.get("cases")
        markdown_reports = raw.get("markdown_reports")
        return {
            "cases": cases if isinstance(cases, dict) else {},
            "markdown_reports": markdown_reports if isinstance(markdown_reports, dict) else {},
        }

    def _write_data(self, data: dict[str, dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
            file.write("\n")
        tmp_path.replace(self.path)


def _empty_data() -> dict[str, dict[str, Any]]:
    return {"cases": {}, "markdown_reports": {}}


def _case_to_json(case: AnalysisCaseDetail) -> dict[str, Any]:
    return case.model_dump(mode="json")


def _resolve_store_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate
