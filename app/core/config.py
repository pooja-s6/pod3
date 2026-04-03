from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # API Configuration
    APP_NAME: str = "AI Learning Chatbot Backend"
    APP_VERSION: str = "1.0.0"
    ENV: Literal["development", "production"] = "development"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./app.db"  # Loaded from .env
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = "sk-test-key"  # Will be loaded from .env
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_TEMPERATURE: float = 0.7
    OPENAI_MAX_TOKENS: int = 2000
    
    # Chat Configuration
    MAX_CONTEXT_MESSAGES: int = 5  # Last 5 messages for context
    SESSION_TIMEOUT: int = 3600  # 1 hour in seconds
    
    # Audio Configuration
    ELEVENLABS_API_KEY: str = ""  # Optional: for advanced TTS
    ENABLE_VOICE: bool = True
    DEFAULT_TTS_VOICE: str = "alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
