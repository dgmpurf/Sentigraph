import os

from pydantic import BaseModel

from app.core.environment import load_project_env


load_project_env()


class Settings(BaseModel):
    app_name: str = "Sentigraph"
    app_version: str = "0.1.0"
    app_env: str = os.getenv("APP_ENV", "development")
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


settings = Settings()
