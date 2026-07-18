from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_url: str = "http://app:8000"
    # transport in mcp.run() expects a literal for mcp_transport
    mcp_transport: Literal["stdio", "sse", "streamable-http"] = "stdio"
    mcp_port: int = 9000

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
