"""
Run script for the chatbot backend.

Usage:
    python run.py
"""

import uvicorn
from config import get_settings


def main():
    settings = get_settings()
    
    print(f"🤖 LLM Backend: {settings.llm_backend_url}")
    print(f"📦 Model: {settings.llm_model}")
    print(f"🌐 Server: http://{settings.host}:{settings.port}\n")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )


if __name__ == "__main__":
    main()
