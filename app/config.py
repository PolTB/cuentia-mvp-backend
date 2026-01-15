from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # OpenAI
    openai_api_key: str
    openai_model_primary: str = "gpt-4"
    openai_model_fallback: str = "gpt-3.5-turbo"
    openai_timeout: int = 45
    openai_max_retries: int = 1
        
    # DALL-E
    dalle_timeout: int = 60  # Longer timeout for image generation
    
    # Supabase
    supabase_url: str
    supabase_key: str
    
    # API Settings
    api_port: int = 8000
    api_host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
