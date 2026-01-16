from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anthropic_api_key: str
    jira_url: str
    jira_email: str
    jira_api_token: str
    service_port: int = 8000
    log_level: str = "INFO"
    enable_jira_mcp: bool = False  # Use JIRA MCP server instead of direct API

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
