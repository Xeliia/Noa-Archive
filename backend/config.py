import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from enum import Enum
from typing import Literal, Optional
from pathlib import Path


class LLMBackendType(str, Enum):
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"


# Default system prompt (used if no prompt file is specified)
DEFAULT_SYSTEM_PROMPT = """You are Ushio Noa, a warm and intelligent AI assistant. Keep responses concise and conversational."""


class Settings(BaseSettings):
    # LLM Backend Configuration
    # Backend type: "ollama" or "llamacpp"
    llm_backend_type: LLMBackendType = LLMBackendType.OLLAMA
    
    # Backend URLs (set based on your setup)
    # Ollama default: http://localhost:11434
    # llama.cpp default: http://localhost:8080
    llm_backend_url: str = "http://localhost:11434"
    llm_model: str = "llama3.2"  # Any model name your backend supports
    
    # API Security
    api_key: str = "changeme"
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS - Frontend URL (for local dev)
    frontend_url: str = "http://localhost:5173"
    
    # System prompt configuration
    # Can be inline text OR a path to a .txt file in the prompts/ folder
    # Examples: "noa.txt" or "You are a helpful assistant..."
    system_prompt: str = "noa.txt"
    
    # Generation parameters (tune for your model)
    temperature: float = 0.8  # Higher = more creative, lower = more focused
    max_tokens: int = 256  # Keep low for weak models to avoid gibberish
    top_p: float = 0.9
    repeat_penalty: float = 1.1  # Helps prevent repetition on weak models
    
    @property
    def resolved_system_prompt(self) -> str:
        """Load system prompt from file if it's a filename, otherwise return as-is"""
        # Check if it looks like a filename
        if self.system_prompt.endswith(".txt"):
            prompt_path = Path(__file__).parent / "prompts" / self.system_prompt
            if prompt_path.exists():
                return prompt_path.read_text(encoding="utf-8").strip()
            else:
                print(f"Warning: Prompt file '{prompt_path}' not found, using default")
                return DEFAULT_SYSTEM_PROMPT
        return self.system_prompt
    
    @property
    def chat_completions_url(self) -> str:
        """Get the full chat completions endpoint URL based on backend type"""
        base = self.llm_backend_url.rstrip("/")
        if self.llm_backend_type == LLMBackendType.OLLAMA:
            return f"{base}/v1/chat/completions"
        else:  # llamacpp
            return f"{base}/v1/chat/completions"
    
    @property
    def models_url(self) -> str:
        """Get the models endpoint URL based on backend type"""
        base = self.llm_backend_url.rstrip("/")
        if self.llm_backend_type == LLMBackendType.OLLAMA:
            return f"{base}/v1/models"
        else:  # llamacpp
            return f"{base}/v1/models"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
