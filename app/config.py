from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str
    ENVIRONMENT: str
    DEBUG: bool
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # tells pydantic to read from .env
        env_file_encoding = "utf-8"
        case_sensitive = True  # APP_NAME != app_name
        extra = "allow"  # allow extra fields in .env without throwing an error


# single instance shared across entire app
settings = Settings()
