from __future__ import annotations

from app.schemas.alert import AlertEvent, AlertLevel, AlertThresholdConfig, AnalysisSnapshot


RISK_LEVEL_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def evaluate_alerts(
    previous_snapshot: AnalysisSnapshot | None,
    latest_snapshot: AnalysisSnapshot,
    *,
    config: AlertThresholdConfig | None = None,
) -> list[AlertEvent]:
    """Compare monitoring snapshots and return deterministic alert events."""
    thresholds = config or AlertThresholdConfig()
    alerts: list[AlertEvent] = []

    if previous_snapshot is None:
        return [
            _make_alert(
                latest_snapshot,
                index=1,
                level="info",
                alert_type="baseline_created",
                message="已创建该案例的首个监控快照。",
                reason="暂无上一轮快照可比对，本次结果作为后续监控基线。",
                metadata={"snapshot_count": 1},
            )
        ]

    risk_delta = latest_snapshot.risk_score - previous_snapshot.risk_score
    if risk_delta >= thresholds.risk_score_delta_warning:
        level: AlertLevel = "critical" if risk_delta >= thresholds.risk_score_delta_critical else "warning"
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level=level,
                alert_type="risk_score_increase",
                message=f"总体风险分上升 {risk_delta:.1f} 分。",
                reason="最新快照相对上一轮出现明显风险增量，建议优先复核高风险话题和传播信号。",
                metadata={
                    "previous_risk_score": previous_snapshot.risk_score,
                    "latest_risk_score": latest_snapshot.risk_score,
                    "risk_score_delta": round(risk_delta, 2),
                },
            )
        )

    if _level_rank(latest_snapshot.risk_level) > _level_rank(previous_snapshot.risk_level):
        level = "critical" if latest_snapshot.risk_level == "critical" else "warning"
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level=level,
                alert_type="risk_level_escalation",
                message=f"风险等级由 {previous_snapshot.risk_level} 升至 {latest_snapshot.risk_level}。",
                reason="风险等级跨档上升，建议提高监控频率并准备统一回应口径。",
                metadata={
                    "previous_risk_level": previous_snapshot.risk_level,
                    "latest_risk_level": latest_snapshot.risk_level,
                },
            )
        )

    real_crisis_delta = latest_snapshot.real_crisis_risk - previous_snapshot.real_crisis_risk
    if real_crisis_delta >= thresholds.real_crisis_delta_warning:
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level="warning",
                alert_type="real_crisis_risk_increase",
                message=f"真实危机风险上升 {real_crisis_delta:.1f} 分。",
                reason="真实事件、服务体验、合规安全等风险信号增强，需核对事实链路。",
                metadata={
                    "previous_real_crisis_risk": previous_snapshot.real_crisis_risk,
                    "latest_real_crisis_risk": latest_snapshot.real_crisis_risk,
                    "real_crisis_delta": round(real_crisis_delta, 2),
                },
            )
        )

    manipulation_delta = latest_snapshot.manipulation_risk - previous_snapshot.manipulation_risk
    if manipulation_delta >= thresholds.manipulation_delta_warning:
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level="warning",
                alert_type="manipulation_risk_increase",
                message=f"操纵传播风险上升 {manipulation_delta:.1f} 分。",
                reason="疑似水军、重复话术或异常协同信号增强，建议标记样本并继续观察。",
                metadata={
                    "previous_manipulation_risk": previous_snapshot.manipulation_risk,
                    "latest_manipulation_risk": latest_snapshot.manipulation_risk,
                    "manipulation_delta": round(manipulation_delta, 2),
                },
            )
        )

    previous_topic_ids = {_topic_key(topic) for topic in previous_snapshot.top_risk_topics}
    for topic in latest_snapshot.top_risk_topics:
        if _topic_key(topic) in previous_topic_ids:
            continue
        if topic.topic_risk_score < thresholds.topic_risk_high:
            continue
        level = "critical" if topic.topic_risk_score >= thresholds.topic_risk_critical else "warning"
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level=level,
                alert_type="new_high_risk_topic",
                message=f"出现新的高风险话题：{topic.topic}。",
                reason=f"该话题风险分达到 {topic.topic_risk_score:.1f}/100，建议加入重点监控列表。",
                metadata={
                    "topic_id": topic.topic_id,
                    "topic": topic.topic,
                    "topic_risk_score": topic.topic_risk_score,
                },
            )
        )

    previous_leader = previous_snapshot.top_risk_topics[0] if previous_snapshot.top_risk_topics else None
    latest_leader = latest_snapshot.top_risk_topics[0] if latest_snapshot.top_risk_topics else None
    if (
        previous_leader
        and latest_leader
        and _topic_key(previous_leader) != _topic_key(latest_leader)
        and latest_leader.topic_risk_score > previous_leader.topic_risk_score
    ):
        alerts.append(
            _make_alert(
                latest_snapshot,
                index=len(alerts) + 1,
                level="warning",
                alert_type="top_risk_topic_shift",
                message=f"首要风险话题切换为：{latest_leader.topic}。",
                reason="最新首要话题风险高于上一轮首要话题，说明讨论焦点可能发生升级或迁移。",
                metadata={
                    "previous_topic": previous_leader.topic,
                    "previous_topic_risk_score": previous_leader.topic_risk_score,
                    "latest_topic": latest_leader.topic,
                    "latest_topic_risk_score": latest_leader.topic_risk_score,
                },
            )
        )

    return alerts


def _make_alert(
    snapshot: AnalysisSnapshot,
    *,
    index: int,
    level: AlertLevel,
    alert_type: str,
    message: str,
    reason: str,
    metadata: dict[str, object],
) -> AlertEvent:
    return AlertEvent(
        alert_id=f"alert_{snapshot.snapshot_id}_{index:03d}",
        case_id=snapshot.case_id,
        snapshot_id=snapshot.snapshot_id,
        level=level,
        alert_type=alert_type,
        message=message,
        reason=reason,
        created_at=snapshot.created_at,
        metadata=metadata,
    )


def _level_rank(level: str) -> int:
    return RISK_LEVEL_ORDER.get(level, 0)


def _topic_key(topic) -> str:
    return topic.topic_id or topic.cluster_id or topic.topic
