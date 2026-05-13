from typing import Literal

from pydantic import BaseModel, Field


TaskStatus = Literal["queued", "running", "completed", "failed"]
RiskLevel = Literal["low", "medium", "high", "critical"]


class DateRange(BaseModel):
    start: str = Field(..., examples=["2026-05-01"])
    end: str = Field(..., examples=["2026-05-13"])

