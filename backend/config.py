import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # LLM Backend Configuration
    # Ollama default: http://localhost:11434/v1
    # llama.cpp default: http://localhost:8080/v1
    llm_backend_url: str = "http://localhost:11434/v1"
    llm_model: str = "llama3"
    
    # API Security
    api_key: str = "changeme"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS - Frontend URL (for local dev)
    frontend_url: str = "http://localhost:5173"
    
    # System prompt for the AI
    system_prompt: str = "You are a helpful, warm AI assistant named Ushio Noa. Keep responses concise and conversational."

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
