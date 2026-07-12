from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables only."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    pefy_env: str = "development"
    pefy_log_level: str = "INFO"
    pefy_default_provider: str = "rules"
    pefy_openai_model: str = "gpt-5-mini"
    openai_api_key: str | None = Field(default=None, repr=False)
    pefy_require_human_approval: bool = True
    pefy_allowed_origins: str = "http://localhost:3000"

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.pefy_allowed_origins.split(",") if origin.strip()]

    @property
    def ai_enabled(self) -> bool:
        return self.pefy_default_provider == "openai" and bool(self.openai_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
