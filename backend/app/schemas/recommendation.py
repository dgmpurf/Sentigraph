from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    project_id: str
    user_type: str = "brand"
    tone: str = "professional"


class RecommendationResponse(BaseModel):
    summary: str
    main_risks: list[str]
    recommended_actions: list[str]
    suggested_response: str

