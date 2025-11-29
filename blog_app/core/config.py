from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+psycopg2://user_name:password@localhost:5432/blog_app"

    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    REFRESH_TOKEN_COOKIE_NAME: str = "refresh_token"
    
    # Email Settings
    EMAIL_USER: str = "your-email@example.com"
    EMAIL_PASSWORD: str = "your-app-password"

    # App Settings
    APP_NAME: str = "Blog App Backend"
    DEBUG: bool = True

    ALLOWED_ORIGINS: list[str] = ["http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 