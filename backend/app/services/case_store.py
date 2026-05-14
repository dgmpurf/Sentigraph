from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    MarkdownExportResponse,
)
from app.services.mock_pipeline import build_mock_pipeline
from app.services.mock_service import _pipeline_representative_comments
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.visualization.chart_data_builder import build_visualization_response


_BASE_TIME = datetime(2026, 5, 14, 9, 0, 0, tzinfo=timezone.utc)
_CASES: dict[str, AnalysisCaseDetail] = {}
_CASE_COUNTER = 0
_TIME_COUNTER = 0


def reset_case_store() -> None:
    """Reset the in-memory store for deterministic tests."""
    global _CASE_COUNTER, _TIME_COUNTER
    _CASES.clear()
    _CASE_COUNTER = 0
    _TIME_COUNTER = 0


def list_cases() -> list[AnalysisCaseListItem]:
    cases = sorted(_CASES.values(), key=lambda item: item.updated_at, reverse=True)
    return [_to_list_item(case) for case in cases]


def create_case(payload: AnalysisCaseCreateRequest) -> AnalysisCaseDetail:
    global _CASE_COUNTER
    _CASE_COUNTER += 1
    case_id = f"case_{_CASE_COUNTER:03d}"
    project_id = f"project_{_CASE_COUNTER:03d}"
    timestamp = _next_timestamp()
    keyword = payload.keyword.strip()
    title = (payload.title or f"{keyword} 舆情分析").strip()

    detail = AnalysisCaseDetail(
        case_id=case_id,
        project_id=project_id,
        title=title,
        keyword=keyword,
        platforms=_normalize_platforms(payload.platforms),
        status="draft",
        created_at=timestamp,
        updated_at=timestamp,
        report_language=payload.report_language,
    )
    _CASES[case_id] = detail
    return detail.model_copy(deep=True)


def get_case(case_id: str) -> AnalysisCaseDetail | None:
    case = _CASES.get(case_id)
    return case.model_copy(deep=True) if case else None


def run_case(case_id: str) -> AnalysisCaseDetail | None:
    case = _CASES.get(case_id)
    if not case:
        return None

    running_case = case.model_copy(update={"status": "running", "updated_at": _next_timestamp()})
    _CASES[case_id] = running_case

    pipeline = build_mock_pipeline(running_case.project_id, platforms=running_case.platforms)
    visualization = build_visualization_response(
        running_case.project_id,
        pipeline.analysis,
        clean_comments=pipeline.clean_comments,
        raw_comments=pipeline.raw_comments,
        propagation=pipeline.propagation,
        risk_result=pipeline.risk_result,
        topic_risk_result=pipeline.topic_risk_result,
    )
    report = build_public_opinion_report(
        pipeline.analysis,
        visualization=visualization,
        propagation=pipeline.propagation,
        risk_factors=pipeline.risk_result.factors,
        topic_risk_result=pipeline.topic_risk_result,
        representative_comments=_pipeline_representative_comments(pipeline),
        include_representative_comments=True,
        report_language=running_case.report_language,
    )

    completed_case = running_case.model_copy(
        update={
            "status": "completed",
            "updated_at": _next_timestamp(),
            "analysis_result": pipeline.analysis,
            "visualization_data": visualization,
            "report": report,
            "markdown_available": True,
            "risk_score": _report_score(report),
            "risk_level": report.risk_level,
            "risk_model_version": report.risk_model_version,
        },
        deep=True,
    )
    _CASES[case_id] = completed_case
    return completed_case.model_copy(deep=True)


def export_case_markdown(case_id: str) -> MarkdownExportResponse | None:
    case = _CASES.get(case_id)
    if not case or not case.report:
        return None
    return MarkdownExportResponse(
        case_id=case.case_id,
        project_id=case.project_id,
        filename=f"{_safe_filename(case.title)}_{case.case_id}.md",
        markdown=_build_markdown(case),
        generated_at=_next_timestamp(),
    )


def _to_list_item(case: AnalysisCaseDetail) -> AnalysisCaseListItem:
    return AnalysisCaseListItem(
        case_id=case.case_id,
        project_id=case.project_id,
        title=case.title,
        keyword=case.keyword,
        platforms=case.platforms,
        status=case.status,
        created_at=case.created_at,
        updated_at=case.updated_at,
        risk_score=case.risk_score,
        risk_level=case.risk_level,
        risk_model_version=case.risk_model_version,
        report_language=case.report_language,
    )


def _build_markdown(case: AnalysisCaseDetail) -> str:
    report = case.report
    if not report:
        return ""

    risk_score = _report_score(report)
    platforms = ", ".join(case.platforms) if case.platforms else "mock default platforms"
    lines = [
        f"# {case.title}",
        "",
        f"- 案例ID：{case.case_id}",
        f"- 项目ID：{case.project_id}",
        f"- 关键词：{case.keyword}",
        f"- 平台：{platforms}",
        f"- 状态：{case.status}",
        f"- 风险分数：{risk_score:.1f}/100",
        f"- 风险等级：{report.risk_level_label or report.risk_level} ({report.risk_level})",
        f"- 风险模型版本：{report.risk_model_version}",
        f"- 生成方式：{'离线 mock 管线' if report.generated_from_mock_pipeline else '外部生成'}",
        "",
        "## 舆情总览",
        "",
        report.overall_summary,
        "",
        "## 核心发现",
        "",
        *_markdown_bullets(report.key_findings, "暂无核心发现。"),
        "",
        "## 高风险话题",
        "",
        *_markdown_topic_risks(report.top_risk_topics),
        "",
        "## 主要风险因素",
        "",
        *_markdown_bullets(report.main_risk_factors, "暂无主要风险因素。"),
        "",
        "## 代表性评论",
        "",
        *_markdown_quotes(report.representative_comments, "暂无代表性评论。"),
        "",
        "## 疑似水军/重复话术信号",
        "",
        *_markdown_bullets(report.suspected_bot_signals, "暂无疑似水军或重复话术信号。"),
        "",
        "## 建议行动",
        "",
        *_markdown_bullets(report.recommended_actions, "暂无建议行动。"),
        "",
        "## 建议公开回应文案",
        "",
        report.suggested_public_response or "暂无建议公开回应文案。",
        "",
    ]
    return "\n".join(lines)


def _markdown_bullets(items: Iterable[str], empty_text: str) -> list[str]:
    values = [item for item in items if item]
    if not values:
        return [f"- {empty_text}"]
    return [f"- {item}" for item in values]


def _markdown_quotes(items: Iterable[str], empty_text: str) -> list[str]:
    values = [item for item in items if item]
    if not values:
        return [f"> {empty_text}"]
    return [f"> {item}" for item in values]


def _markdown_topic_risks(items) -> list[str]:
    if not items:
        return ["- 暂无 V1.5 话题风险数据。"]
    lines: list[str] = []
    for topic in items:
        lines.append(
            "- "
            f"{topic.topic}：{topic.topic_risk_score:.1f}/100，"
            f"{topic.topic_risk_level}，{topic.risk_explanation}"
        )
    return lines


def _normalize_platforms(platforms: list[str]) -> list[str]:
    return list(dict.fromkeys(platform.strip().lower() for platform in platforms if platform.strip()))


def _report_score(report) -> float:
    value = report.overall_risk if report.overall_risk is not None else report.risk_score
    return float(value or 0.0)


def _safe_filename(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value.strip())
    return safe.strip("_") or "sentigraph_report"


def _next_timestamp() -> datetime:
    global _TIME_COUNTER
    timestamp = _BASE_TIME + timedelta(minutes=_TIME_COUNTER)
    _TIME_COUNTER += 1
    return timestamp
