from pydantic import BaseModel


class SummaryGenerateRequest(BaseModel):
    project_id: str
    include_representative_comments: bool = True


class SummaryGenerateResponse(BaseModel):
    project_id: str
    summary: str
    key_findings: list[str]
    representative_comments: list[str]

