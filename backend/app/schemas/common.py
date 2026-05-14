from typing import Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["queued", "running", "completed", "failed"]
RiskLevel = Literal["low", "medium", "high", "critical"]
RISK_MODEL_VERSION = "v1_static_mvp"


def get_risk_level_label(risk_level: str, language: str = "zh-CN") -> str:
    """Return a display label without changing the raw risk_level enum."""
    if language == "zh-CN":
        return {
            "low": "低风险",
            "medium": "中等风险",
            "high": "高风险",
            "critical": "严重风险",
        }.get(risk_level, risk_level)
    return {
        "low": "low risk",
        "medium": "medium risk",
        "high": "high risk",
        "critical": "critical risk",
    }.get(risk_level, risk_level)


class DateRange(BaseModel):
    start: str = Field(..., examples=["2026-05-01"])
    end: str = Field(..., examples=["2026-05-13"])
