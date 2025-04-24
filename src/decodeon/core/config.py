from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


from decodeon.types.enums import EnvironmentEnum


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    openai_api_key: str = Field(
        ..., description="API key for OpenAI to interact with models"
    )
    pinecone_api_key: str = Field(
        ..., description="API key for Pinecone to manage vector embeddings"
    )
    langsmith_api_key: Optional[str] = Field(
        default=None, description="API key for LangSmith for LangChain integration"
    )

    environment: EnvironmentEnum = Field(
        EnvironmentEnum.production,
        description="Environment type (development, production, etc.)",
    )
    port: int = Field(8000, description="The port the server will run on")
    langchain_tracing_v2: bool = Field(
        default=False, description="Enable or disable LangChain tracing V2"
    )
    langchain_project: str = Field(
        default="Decodeon", description="The name of the LangChain project"
    )
    langsmith_url: Optional[str] = Field(
        default=None,
        description="Base URL for LangSmith API",
    )


settings = Settings()
