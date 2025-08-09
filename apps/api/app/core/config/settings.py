from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "LaundroMate API"
    ENV: str = Field(default="development")

    # CORS / Allowed Origins
    ALLOWED_HOSTS: List[str] = Field(default_factory=lambda: ["*"])

    # Security / Auth
    SECRET_KEY: str = Field(default="change-me")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)  # 24 hours

    # Database
    DATABASE_URL: str = Field(default="postgresql://laundromate:laundromate@localhost:5432/laundromate")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
