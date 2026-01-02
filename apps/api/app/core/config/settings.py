from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


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
    DATABASE_URL: str = Field(
        default="postgresql://laundromate:laundromate@localhost:5432/laundromate"
    )

    # Email Configuration (SendGrid)
    SENDGRID_API_KEY: str = Field(default="")
    FROM_EMAIL: str = Field(default="noreply@laundromate.com")
    FRONTEND_URL: str = Field(default="http://localhost:3000")

    # Invitation Configuration
    INVITATION_EXPIRATION_DAYS: int = Field(default=7)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
