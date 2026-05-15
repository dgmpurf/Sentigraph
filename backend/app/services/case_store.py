from __future__ import annotations

from typing import Iterable

from app.repositories.case_repository import CaseRepository
from app.schemas.alert import AlertEvent, AlertThresholdConfig, AnalysisSnapshot, MonitoringStatus
from app.schemas.case import (
    AnalysisCaseCreateRequest,
    AnalysisCaseDetail,
    AnalysisCaseListItem,
    MarkdownExportResponse,
)
from app.services.mock_pipeline import build_mock_pipeline
from app.services.mock_service import _pipeline_representative_comments
from app.services.monitoring.alert_evaluator import evaluate_alerts
from app.services.monitoring.snapshot_builder import build_analysis_snapshot
from app.services.notifications.notification_service import create_notifications_from_alerts
from app.services.recommendation.report_builder import build_public_opinion_report
from app.services.storage.base_store import CaseStore
from app.services.storage.store_factory import create_case_store_from_env
from app.services.visualization.chart_data_builder import build_visualization_response


_CASE_REPOSITORY: CaseRepository | None = None


def get_case_repository() -> CaseRepository:
    global _CASE_REPOSITORY
    if _CASE_REPOSITORY is None:
        _CASE_REPOSITORY = CaseRepository(create_case_store_from_env())
    return _CASE_REPOSITORY


def configure_case_repository(repository: CaseRepository) -> None:
    """Swap the case repository, primarily for tests with temporary storage."""

    global _CASE_REPOSITORY
    _CASE_REPOSITORY = repository


def configure_case_store(store: CaseStore) -> None:
    configure_case_repository(CaseRepository(store))


def reset_case_store() -> None:
    """Reset the configured case store for tests or explicit local cleanup."""

    get_case_repository().reset()


def list_cases() -> list[AnalysisCaseListItem]:
    return get_case_repository().list_cases()


def create_case(payload: AnalysisCaseCreateRequest) -> AnalysisCaseDetail:
    return get_case_repository().create_case(payload)


def get_case(case_id: str) -> AnalysisCaseDetail | None:
    return get_case_repository().get_case(case_id)


def run_case(case_id: str) -> AnalysisCaseDetail | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    if not case:
        return None

    running_case = case.model_copy(update={"status": "running", "updated_at": repository.next_timestamp()})
    repository.update_case(running_case)

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
            "updated_at": repository.next_timestamp(),
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
    repository.update_case(completed_case)
    repository.save_markdown_report(
        completed_case.case_id,
        MarkdownExportResponse(
            case_id=completed_case.case_id,
            project_id=completed_case.project_id,
            filename=f"{_safe_filename(completed_case.title)}_{completed_case.case_id}.md",
            markdown=_build_markdown(completed_case),
            generated_at=repository.next_timestamp(),
        ),
    )
    _save_case_snapshot(repository, completed_case, apply_mock_shift=False)
    return completed_case.model_copy(deep=True)


def list_case_snapshots(case_id: str) -> list[AnalysisSnapshot] | None:
    repository = get_case_repository()
    if not repository.get_case(case_id):
        return None
    return repository.list_analysis_snapshots(case_id)


def list_case_alerts(case_id: str) -> list[AlertEvent] | None:
    repository = get_case_repository()
    if not repository.get_case(case_id):
        return None
    return repository.list_case_alerts(case_id)


def list_all_case_alerts() -> list[AlertEvent]:
    return get_case_repository().list_all_alert_events()


def run_monitoring_check(
    case_id: str,
    *,
    threshold_config: AlertThresholdConfig | None = None,
) -> MonitoringStatus | None:
    repository = get_case_repository()
    case = repository.get_case(case_id)
    if not case:
        return None

    if not case.report:
        completed_case = run_case(case_id)
        if not completed_case:
            return None
        snapshots = repository.list_analysis_snapshots(case_id)
        latest = snapshots[-1]
        alerts = evaluate_alerts(None, latest, config=threshold_config)
        saved_alerts = repository.save_alert_events(case_id, alerts)
        create_notifications_from_alerts(saved_alerts, repository=repository)
        return _build_monitoring_status(
            case_id,
            latest_snapshot=latest,
            previous_snapshot=None,
            alerts=saved_alerts,
            snapshot_count=len(snapshots),
        )

    previous_snapshots = repository.list_analysis_snapshots(case_id)
    previous_snapshot = previous_snapshots[-1] if previous_snapshots else None
    latest_snapshot = _save_case_snapshot(repository, case, apply_mock_shift=True)
    alerts = evaluate_alerts(previous_snapshot, latest_snapshot, config=threshold_config)
    saved_alerts = repository.save_alert_events(case_id, alerts)
    create_notifications_from_alerts(saved_alerts, repository=repository)
    return _build_monitoring_status(
        case_id,
        latest_snapshot=latest_snapshot,
        previous_snapshot=previous_snapshot,
        alerts=saved_alerts,
        snapshot_count=len(previous_snapshots) + 1,
    )


def export_case_markdown(case_id: str) -> MarkdownExportResponse | None:
    repository = get_case_repository()
    persisted_report = repository.get_markdown_report(case_id)
    if persisted_report:
        return persisted_report

    case = repository.get_case(case_id)
    if not case or not case.report:
        return None

    report = MarkdownExportResponse(
        case_id=case.case_id,
        project_id=case.project_id,
        filename=f"{_safe_filename(case.title)}_{case.case_id}.md",
        markdown=_build_markdown(case),
        generated_at=repository.next_timestamp(),
    )
    return repository.save_markdown_report(case_id, report)


def _save_case_snapshot(
    repository: CaseRepository,
    case: AnalysisCaseDetail,
    *,
    apply_mock_shift: bool,
) -> AnalysisSnapshot:
    run_index = repository.next_snapshot_number(case.case_id)
    snapshot = build_analysis_snapshot(
        case,
        snapshot_id=f"{case.case_id}_snapshot_{run_index:03d}",
        created_at=repository.next_timestamp(),
        run_index=run_index,
        apply_mock_shift=apply_mock_shift,
    )
    return repository.save_analysis_snapshot(case.case_id, snapshot)


def _build_monitoring_status(
    case_id: str,
    *,
    latest_snapshot: AnalysisSnapshot,
    previous_snapshot: AnalysisSnapshot | None,
    alerts: list[AlertEvent],
    snapshot_count: int,
) -> MonitoringStatus:
    if previous_snapshot is None:
        status = "baseline_created"
        message = "已创建监控基线快照。"
        latest_risk_delta = 0.0
    elif alerts:
        status = "alerts_detected"
        message = f"本轮监控触发 {len(alerts)} 条预警事件。"
        latest_risk_delta = latest_snapshot.risk_score - previous_snapshot.risk_score
    else:
        status = "stable"
        message = "本轮监控未触发新的风险阈值。"
        latest_risk_delta = latest_snapshot.risk_score - previous_snapshot.risk_score

    return MonitoringStatus(
        case_id=case_id,
        status=status,
        latest_snapshot=latest_snapshot,
        previous_snapshot=previous_snapshot,
        alerts=alerts,
        snapshot_count=snapshot_count,
        latest_risk_delta=round(latest_risk_delta, 2),
        latest_risk_level=latest_snapshot.risk_level,
        message=message,
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
        f"- 案例ID: {case.case_id}",
        f"- 项目ID: {case.project_id}",
        f"- 关键词: {case.keyword}",
        f"- 平台: {platforms}",
        f"- 状态: {case.status}",
        f"- 风险分数: {risk_score:.1f}/100",
        f"- 风险等级: {report.risk_level_label or report.risk_level} ({report.risk_level})",
        f"- 风险模型版本: {report.risk_model_version}",
        f"- 生成方式: {'离线 mock 管线' if report.generated_from_mock_pipeline else '外部生成'}",
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
            f"{topic.topic}: {topic.topic_risk_score:.1f}/100, "
            f"{topic.topic_risk_level}, {topic.risk_explanation}"
        )
    return lines


def _report_score(report) -> float:
    value = report.overall_risk if report.overall_risk is not None else report.risk_score
    return float(value or 0.0)


def _safe_filename(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in value.strip())
    return safe.strip("_") or "sentigraph_report"
