from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./feedback.db"
    
    # AI Services
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Vector DB (Optional)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # App Settings
    PROJECT_NAME: str = "Feedback Intelligence API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    class Config:
        # Look for .env in parent directory (project root)
        env_file = os.path.join(Path(__file__).parent.parent.parent, ".env")
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()