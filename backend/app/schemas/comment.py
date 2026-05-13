from pydantic import BaseModel, Field


class RawPost(BaseModel):
    platform: str
    post_id: str
    author_id: str
    author_name: str
    title: str
    content: str
    like_count: int = 0
    reply_count: int = 0
    share_count: int = 0
    created_at: str
    url: str
    raw_data: dict[str, object] = Field(default_factory=dict)


class RawComment(BaseModel):
    platform: str
    post_id: str
    comment_id: str
    parent_id: str | None = None
    author_id: str
    author_name: str
    content: str
    like_count: int = 0
    reply_count: int = 0
    share_count: int = 0
    created_at: str
    url: str
    raw_data: dict[str, object] = Field(default_factory=dict)


class CleanComment(BaseModel):
    clean_comment_id: str
    original_comment_ids: list[str]
    platforms: list[str]
    post_ids: list[str]
    author_id: str
    clean_text: str
    language: str
    duplicate_group_id: str | None = None
    duplicate_count: int = 1
    semantic_similarity_group: str | None = None
    is_repeated_script: bool = False
    created_at_min: str
    created_at_max: str


class UserAggregationResult(BaseModel):
    author_id: str
    platforms: list[str]
    comment_count: int
    unique_comment_count: int
    duplicate_comment_ratio: float
    average_sentiment_score: float
    first_seen_at: str
    last_seen_at: str

