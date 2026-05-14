from pydantic import BaseModel, Field


class KeywordExpandRequest(BaseModel):
    keyword: str = Field(..., min_length=1, examples=["Tesla"])
    platforms: list[str] = Field(default_factory=list, examples=[["reddit", "weibo"]])
    language: str = Field(default="auto", examples=["auto"])


class KeywordExpandResponse(BaseModel):
    original_keyword: str
    expanded_keywords: list[str]
    search_queries: list[str]
