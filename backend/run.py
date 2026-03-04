import uvicorn
from config import get_settings


def main():
    settings = get_settings()
    
    print(f"LLM Backend: {settings.llm_backend_type.value} @ {settings.resolved_backend_url}")
    print(f"Model: {settings.resolved_model}")
    if settings.is_cloud_backend:
        key_preview = (settings.llm_api_key[:8] + "...") if settings.llm_api_key else "NOT SET"
    print(f"Server: http://{settings.host}:{settings.port}\n")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )


if __name__ == "__main__":
    main()
