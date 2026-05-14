from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from app.schemas.analysis import AnalysisResultResponse
from app.schemas.case import AnalysisCaseDetail, MarkdownExportResponse
from app.schemas.common import RiskLevel
from app.schemas.report import PublicOpinionReport
from app.schemas.visualization import VisualizationResponse


class CaseStore(ABC):
    """Persistence interface for Sentigraph analysis cases.

    Implementations must stay local/offline for the MVP. A MongoDB-backed
    implementation can be added later behind this interface after persistence
    requirements and deployment constraints are clearer.
    """

    @abstractmethod
    def create_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        """Persist a newly-created case."""

    @abstractmethod
    def list_cases(self) -> list[AnalysisCaseDetail]:
        """Return all persisted case details."""

    @abstractmethod
    def get_case(self, case_id: str) -> AnalysisCaseDetail | None:
        """Return one case detail, if it exists."""

    @abstractmethod
    def update_case(self, case: AnalysisCaseDetail) -> AnalysisCaseDetail:
        """Replace an existing case detail."""

    @abstractmethod
    def save_analysis_result(
        self,
        case_id: str,
        *,
        analysis_result: AnalysisResultResponse,
        visualization_data: VisualizationResponse | None = None,
        risk_score: float | None = None,
        risk_level: RiskLevel | None = None,
        risk_model_version: str | None = None,
        updated_at: datetime | None = None,
    ) -> AnalysisCaseDetail | None:
        """Attach analysis/visualization output to a case."""

    @abstractmethod
    def save_report(
        self,
        case_id: str,
        *,
        report: PublicOpinionReport,
        updated_at: datetime | None = None,
        markdown_available: bool = True,
    ) -> AnalysisCaseDetail | None:
        """Attach a structured report to a case."""

    @abstractmethod
    def save_markdown_report(self, case_id: str, report: MarkdownExportResponse) -> MarkdownExportResponse:
        """Persist a rendered Markdown report."""

    @abstractmethod
    def get_markdown_report(self, case_id: str) -> MarkdownExportResponse | None:
        """Return a persisted Markdown report, if available."""

    @abstractmethod
    def list_markdown_reports(self) -> list[MarkdownExportResponse]:
        """Return all persisted Markdown reports."""

    @abstractmethod
    def reset(self) -> None:
        """Clear persisted cases for tests or explicit local reset."""

