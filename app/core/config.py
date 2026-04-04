from pydantic_settings import BaseSettings
from typing import Literal
from pathlib import Path
import os


class Settings(BaseSettings):
    """Application configuration settings loaded from environment."""
    
    # ============ API Configuration ============
    APP_NAME: str = "AI Learning Tutor & Chatbot Backend"
    APP_VERSION: str = "2.0.0"
    ENV: Literal["development", "production"] = "development"
    
    # ============ Database Configuration ============
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # ============ AI Services Configuration ============
    # OpenAI API (Required)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
    
    # Optional AI Services
    ELEVENLABS_API_KEY: str = ""  # Optional: for advanced TTS
    
    # ============ Chat Behavior Configuration ============
    MAX_CONTEXT_MESSAGES: int = 5  # Last 5 messages for context
    SESSION_TIMEOUT: int = 3600  # 1 hour in seconds
    
    # ============ Voice Configuration ============
    ENABLE_VOICE: bool = False
    DEFAULT_TTS_VOICE: str = "alloy"
    
    # ============ Logging Configuration ============
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic configuration."""
        # Look for .env in the pod3 directory
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            ".env"
        )
        case_sensitive = True


# Global settings instance
settings = Settings()
