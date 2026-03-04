import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from enum import Enum
from typing import Literal, Optional
from pathlib import Path


class LLMBackendType(str, Enum):
    OLLAMA = "ollama"
    LLAMACPP = "llamacpp"
    GEMINI = "gemini"
    OPENAI = "openai"
    OPENAI_COMPATIBLE = "openai_compatible"


_DEFAULT_URLS: dict[LLMBackendType, str] = {
    LLMBackendType.OLLAMA: "http://localhost:11434",
    LLMBackendType.LLAMACPP: "http://localhost:8080",
    LLMBackendType.GEMINI: "https://generativelanguage.googleapis.com/v1beta/openai",
    LLMBackendType.OPENAI: "https://api.openai.com/v1",
    LLMBackendType.OPENAI_COMPATIBLE: "http://localhost:8080",
}

_DEFAULT_MODELS: dict[LLMBackendType, str] = {
    LLMBackendType.OLLAMA: "llama3.2",
    LLMBackendType.LLAMACPP: "local-model",
    LLMBackendType.GEMINI: "gemini-2.0-flash",
    LLMBackendType.OPENAI: "gpt-4o-mini",
    LLMBackendType.OPENAI_COMPATIBLE: "default",
}

DEFAULT_SYSTEM_PROMPT = """You are Ushio Noa, a warm and intelligent AI assistant. Keep responses concise and conversational."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )

    # Backend type: "ollama", "llamacpp", "gemini", "openai", or "openai_compatible"
    llm_backend_type: LLMBackendType = LLMBackendType.OLLAMA
    
    llm_backend_url: Optional[str] = None
    llm_model: Optional[str] = None  # Leave empty to use default for backend type

    # Cloud LLM API key (required for gemini, openai, openai_compatible)
    llm_api_key: Optional[str] = None
    
    # API Security (for *this* chatbot server, not the LLM provider)
    api_key: str = "changeme"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS - Frontend URL (for local dev)
    frontend_url: str = "http://localhost:5173"
    
    # System prompt configuration
    # Can be inline text OR a path to a .txt file in the prompts/ folder
    # Examples: "noa.txt" or "You are a helpful assistant..."
    system_prompt: str = "noa.txt"
    
    temperature: float = 0.8
    max_tokens: int = 512
    top_p: float = 0.9
    repeat_penalty: float = 1.1  # Only used for local backends (ollama/llamacpp)
    frequency_penalty: float = 0.0  # Only used for cloud backends
    presence_penalty: float = 0.0  # Only used for cloud backends

    @property
    def resolved_backend_url(self) -> str:
        """Get the backend URL, falling back to the default for the backend type"""
        if self.llm_backend_url:
            return self.llm_backend_url
        return _DEFAULT_URLS[self.llm_backend_type]

    @property
    def resolved_model(self) -> str:
        """Get the model name, falling back to the default for the backend type"""
        if self.llm_model:
            return self.llm_model
        return _DEFAULT_MODELS[self.llm_backend_type]

    @property
    def is_cloud_backend(self) -> bool:
        """Whether this backend is a cloud API (needs API key, different params)"""
        return self.llm_backend_type in (
            LLMBackendType.GEMINI,
            LLMBackendType.OPENAI,
            LLMBackendType.OPENAI_COMPATIBLE,
        )

    @property
    def resolved_system_prompt(self) -> str:
        """Load system prompt from file if it's a filename, otherwise return as-is"""
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
        base = self.resolved_backend_url.rstrip("/")
        if self.llm_backend_type == LLMBackendType.OLLAMA:
            return f"{base}/v1/chat/completions"
        elif self.llm_backend_type == LLMBackendType.LLAMACPP:
            return f"{base}/v1/chat/completions"
        else:
            return f"{base}/chat/completions"
    
    @property
    def models_url(self) -> str:
        """Get the models endpoint URL based on backend type"""
        base = self.resolved_backend_url.rstrip("/")
        if self.llm_backend_type == LLMBackendType.OLLAMA:
            return f"{base}/v1/models"
        elif self.llm_backend_type == LLMBackendType.LLAMACPP:
            return f"{base}/v1/models"
        else:
            return f"{base}/models"

    @property
    def llm_request_headers(self) -> dict[str, str]:
        """Get the headers needed for LLM API requests"""
        headers = {"Content-Type": "application/json"}
        if self.is_cloud_backend and self.llm_api_key:
            headers["Authorization"] = f"Bearer {self.llm_api_key}"
        return headers

    def build_payload(self, api_messages: list[dict], stream: bool) -> dict:
        """Build the request payload, adapting parameters per backend type"""
        payload = {
            "model": self.resolved_model,
            "messages": api_messages,
            "stream": stream,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        if self.is_cloud_backend:
            if self.frequency_penalty != 0.0:
                payload["frequency_penalty"] = self.frequency_penalty
            if self.presence_penalty != 0.0:
                payload["presence_penalty"] = self.presence_penalty
        else:
            payload["max_tokens"] = self.max_tokens
            payload["repeat_penalty"] = self.repeat_penalty
        return payload


@lru_cache()
def get_settings() -> Settings:
    return Settings()
