from __future__ import annotations

from typing import TYPE_CHECKING

from app.schemas.alert import AlertEvent
from app.schemas.notification import (
    NotificationChannel,
    NotificationChannelType,
    NotificationOutboxItem,
    NotificationOutboxStatus,
    NotificationSendResult,
)

if TYPE_CHECKING:
    from app.repositories.case_repository import CaseRepository


DEFAULT_CHANNELS = [
    NotificationChannel(
        channel_id="in_app",
        channel_type="in_app",
        display_name="站内通知",
        enabled=True,
        mock_only=True,
        notes="MVP 本地通知，不发送外部消息。",
    ),
    NotificationChannel(
        channel_id="email_placeholder",
        channel_type="email_placeholder",
        display_name="邮件占位通道",
        enabled=False,
        mock_only=True,
        notes="未来可接入 SMTP 或邮件服务；当前只保留占位。",
    ),
    NotificationChannel(
        channel_id="webhook_placeholder",
        channel_type="webhook_placeholder",
        display_name="Webhook 占位通道",
        enabled=False,
        mock_only=True,
        notes="未来可接入通用 webhook；当前不会发起网络请求。",
    ),
    NotificationChannel(
        channel_id="slack_placeholder",
        channel_type="slack_placeholder",
        display_name="Slack 占位通道",
        enabled=False,
        mock_only=True,
        notes="未来可接入 Slack webhook；当前不会发起网络请求。",
    ),
    NotificationChannel(
        channel_id="enterprise_wechat_placeholder",
        channel_type="enterprise_wechat_placeholder",
        display_name="企业微信占位通道",
        enabled=False,
        mock_only=True,
        notes="未来可接入企业微信机器人；当前不会发起网络请求。",
    ),
    NotificationChannel(
        channel_id="feishu_placeholder",
        channel_type="feishu_placeholder",
        display_name="飞书占位通道",
        enabled=False,
        mock_only=True,
        notes="未来可接入飞书机器人；当前不会发起网络请求。",
    ),
]


def create_notification_from_alert(
    alert_event: AlertEvent,
    *,
    channel_type: NotificationChannelType = "in_app",
    repository: "CaseRepository | None" = None,
) -> NotificationOutboxItem:
    repo = _get_repository(repository)
    notification_id = _notification_id(alert_event.alert_id, channel_type)
    existing = repo.get_notification(notification_id)
    if existing:
        return existing

    notification = NotificationOutboxItem(
        notification_id=notification_id,
        alert_id=alert_event.alert_id,
        case_id=alert_event.case_id,
        level=alert_event.level,
        title=_title_for_level(alert_event.level),
        message=_message_for_level(alert_event.level),
        channel_type=channel_type,
        status="pending",
        created_at=alert_event.created_at,
        metadata={
            "alert_type": alert_event.alert_type,
            "alert_message": alert_event.message,
            "reason": alert_event.reason,
            "snapshot_id": alert_event.snapshot_id,
        },
    )
    return repo.save_notification(notification)


def create_notifications_from_alerts(
    alert_events: list[AlertEvent],
    *,
    repository: "CaseRepository | None" = None,
) -> list[NotificationOutboxItem]:
    repo = _get_repository(repository)
    return [create_notification_from_alert(alert, repository=repo) for alert in alert_events]


def list_notifications(*, repository: "CaseRepository | None" = None) -> list[NotificationOutboxItem]:
    return _get_repository(repository).list_notifications()


def list_case_notifications(
    case_id: str,
    *,
    repository: "CaseRepository | None" = None,
) -> list[NotificationOutboxItem]:
    return _get_repository(repository).list_case_notifications(case_id)


def mark_notification_read(
    notification_id: str,
    *,
    repository: "CaseRepository | None" = None,
) -> NotificationOutboxItem | None:
    repo = _get_repository(repository)
    notification = repo.get_notification(notification_id)
    if not notification:
        return None
    if notification.read_at:
        return notification
    updated = notification.model_copy(update={"read_at": repo.next_timestamp()}, deep=True)
    return repo.update_notification(updated)


def simulate_send(
    notification_id: str,
    *,
    repository: "CaseRepository | None" = None,
) -> NotificationSendResult | None:
    repo = _get_repository(repository)
    notification = repo.get_notification(notification_id)
    if not notification:
        return None
    if notification.status != "simulated_sent":
        notification = notification.model_copy(
            update={
                "status": "simulated_sent",
                "simulated_sent_at": repo.next_timestamp(),
            },
            deep=True,
        )
        notification = repo.update_notification(notification) or notification

    return NotificationSendResult(
        notification_id=notification.notification_id,
        channel_type=notification.channel_type,
        status=notification.status,
        simulated=True,
        simulated_sent_at=notification.simulated_sent_at,
        message="通知已完成本地模拟发送，未调用任何外部通道。",
        notification=notification,
    )


def simulate_send_all_pending(
    *,
    repository: "CaseRepository | None" = None,
) -> list[NotificationSendResult]:
    repo = _get_repository(repository)
    results: list[NotificationSendResult] = []
    for notification in repo.list_notifications():
        if notification.status == "pending":
            result = simulate_send(notification.notification_id, repository=repo)
            if result:
                results.append(result)
    return results


def get_outbox_status(*, repository: "CaseRepository | None" = None) -> NotificationOutboxStatus:
    notifications = _get_repository(repository).list_notifications()
    pending = sum(1 for item in notifications if item.status == "pending")
    simulated_sent = sum(1 for item in notifications if item.status == "simulated_sent")
    failed = sum(1 for item in notifications if item.status == "failed")
    unread = sum(1 for item in notifications if item.read_at is None)

    return NotificationOutboxStatus(
        total=len(notifications),
        unread=unread,
        pending=pending,
        simulated_sent=simulated_sent,
        failed=failed,
        mock_only=True,
        channels=DEFAULT_CHANNELS,
        message="通知出箱仅用于本地模拟，不会发送真实外部消息。",
    )


def _get_repository(repository: "CaseRepository | None" = None) -> "CaseRepository":
    if repository is not None:
        return repository
    from app.services.case_store import get_case_repository

    return get_case_repository()


def _notification_id(alert_id: str, channel_type: NotificationChannelType) -> str:
    return f"notification_{alert_id}_{channel_type}"


def _title_for_level(level: str) -> str:
    return {
        "critical": "严重舆情预警",
        "warning": "舆情风险预警",
        "info": "监控任务通知",
    }.get(level, "舆情通知")


def _message_for_level(level: str) -> str:
    return {
        "critical": "舆情风险显著升高，建议立即检查高风险话题。",
        "warning": "舆情风险出现上升，请关注该案例。",
        "info": "监控任务已完成，暂无严重异常。",
    }.get(level, "监控任务已完成，暂无严重异常。")
