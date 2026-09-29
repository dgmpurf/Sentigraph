from fastapi import APIRouter, HTTPException

from app.schemas.notification import (
    NotificationOutboxItem,
    NotificationOutboxItemView,
    NotificationOutboxStatus,
    NotificationSendResult,
)
from app.services.notifications.notification_service import (
    get_outbox_status,
    list_notifications,
    mark_notification_read,
    simulate_send,
    simulate_send_all_pending,
)
from app.services.case_store import get_case_repository

router = APIRouter()


@router.get("", response_model=list[NotificationOutboxItemView])
def list_all_notifications() -> list[NotificationOutboxItemView]:
    repository = get_case_repository()
    return [repository.notification_view(item) for item in list_notifications(repository=repository)]


@router.get("/outbox/status", response_model=NotificationOutboxStatus)
def get_notification_outbox_status() -> NotificationOutboxStatus:
    return get_outbox_status()


@router.post("/simulate-send-pending", response_model=list[NotificationSendResult])
def simulate_send_pending_notifications() -> list[NotificationSendResult]:
    return simulate_send_all_pending()


@router.post("/{notification_id}/read", response_model=NotificationOutboxItem)
def mark_read(notification_id: str) -> NotificationOutboxItem:
    notification = mark_notification_read(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.post("/{notification_id}/simulate-send", response_model=NotificationSendResult)
def simulate_notification_send(notification_id: str) -> NotificationSendResult:
    result = simulate_send(notification_id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return result
