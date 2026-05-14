from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.alert import AlertLevel


NotificationChannelType = Literal[
    "in_app",
    "email_placeholder",
    "webhook_placeholder",
    "slack_placeholder",
    "enterprise_wechat_placeholder",
    "feishu_placeholder",
]
NotificationStatus = Literal["pending", "simulated_sent", "failed"]


class NotificationChannel(BaseModel):
    channel_id: str
    channel_type: NotificationChannelType = "in_app"
    display_name: str
    enabled: bool = True
    mock_only: bool = True
    notes: str | None = None


class NotificationMessage(BaseModel):
    notification_id: str
    alert_id: str
    case_id: str
    level: AlertLevel
    title: str
    message: str
    channel_type: NotificationChannelType = "in_app"
    status: NotificationStatus = "pending"
    created_at: datetime
    read_at: datetime | None = None
    simulated_sent_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class NotificationOutboxItem(NotificationMessage):
    pass


class NotificationSendResult(BaseModel):
    notification_id: str
    channel_type: NotificationChannelType = "in_app"
    status: NotificationStatus
    simulated: bool = True
    simulated_sent_at: datetime | None = None
    message: str
    notification: NotificationOutboxItem | None = None


class NotificationOutboxStatus(BaseModel):
    total: int
    unread: int
    pending: int
    simulated_sent: int
    failed: int
    mock_only: bool = True
    channels: list[NotificationChannel] = Field(default_factory=list)
    message: str


class NotificationPreference(BaseModel):
    enabled: bool = True
    channel_types: list[NotificationChannelType] = Field(default_factory=lambda: ["in_app"])
    minimum_level: AlertLevel = "info"
