import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application Settings configuration."""
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_PROVIDER: str = "openai"
    DEMO_MODE: bool = False
    
    # Path resolution: find project root containing 'data'
    DATA_DIR: str = os.getenv("DATA_DIR", str(Path(__file__).resolve().parent.parent.parent / "data"))
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def is_demo_mode(self) -> bool:
        """Determines whether demo/mock mode is active."""
        if self.DEMO_MODE or self.LLM_PROVIDER.lower() == "mock":
            return True
        if not self.OPENAI_API_KEY or self.OPENAI_API_KEY.strip() == "":
            return True
        return False

settings = Settings()
