from typing import List, Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "RAG System"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # LLM Provider Config
    LLM_PROVIDER: Literal["openai", "groq", "gemini", "local"] = "openai"
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    LOCAL_LLM_URL: str = "http://localhost:11434"
    
    # Vector DB Config
    VECTOR_DB_PATH: str = "./chroma_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Redis Config
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_QUEUE_NAME: str = "rag_ingestion_queue"
    
    # Ingestion Config
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
