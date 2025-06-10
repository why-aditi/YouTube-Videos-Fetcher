import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    # YouTube API Configuration
    youtube_api_keys: str = ""
    search_query: str = "python programming"
    fetch_interval: int = 10
    max_results_per_request: int = 50
    
    # MongoDB Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "youtube_videos"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
    
    @field_validator('youtube_api_keys')
    @classmethod
    def parse_api_keys(cls, v):
        if isinstance(v, str):
            return [key.strip() for key in v.split(",") if key.strip()]
        return v or []
    
    def get_api_keys(self) -> List[str]:
        """Get parsed API keys as a list"""
        if isinstance(self.youtube_api_keys, str):
            return [key.strip() for key in self.youtube_api_keys.split(",") if key.strip()]
        return self.youtube_api_keys or []


settings = Settings()

