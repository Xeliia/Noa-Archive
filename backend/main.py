from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import json
from typing import AsyncGenerator

from config import get_settings, Settings, LLMBackendType

app = FastAPI(title="Simple Chatbot API")

# CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Auth Dependency ──
async def verify_api_key(
    authorization: str | None = Header(None),
    settings: Settings = Depends(get_settings)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization format")
    
    if parts[1] != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return True


# ── Request/Response Models ──
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    stream: bool = True


# ── Streaming Generator ──
async def stream_chat_response(
    messages: list[Message],
    settings: Settings
) -> AsyncGenerator[str, None]:
    """Stream response from LLM backend (Ollama or llama.cpp)"""
    
    # Build messages with system prompt
    api_messages = [
        {"role": "system", "content": settings.resolved_system_prompt},
        *[{"role": m.role, "content": m.content} for m in messages]
    ]
    
    payload = {
        "model": settings.llm_model,
        "messages": api_messages,
        "stream": True,
        # Generation parameters (helps with roleplay on weaker models)
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": settings.top_p,
        "repeat_penalty": settings.repeat_penalty,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                settings.chat_completions_url,
                json=payload,
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode()
                    # Provide helpful hint for common errors
                    if "not found" in error_msg.lower():
                        if settings.llm_backend_type == LLMBackendType.OLLAMA:
                            error_msg += f" (Try running: ollama pull {settings.llm_model})"
                    yield f"data: {json.dumps({'error': f'LLM backend error: {error_msg}'})}\n\n"
                    return
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        
                        try:
                            chunk = json.loads(data)
                            # Extract content from OpenAI-compatible format
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield f"data: {json.dumps({'content': content})}\n\n"
                        except json.JSONDecodeError:
                            continue
                            
        except httpx.ConnectError:
            backend_name = "Ollama" if settings.llm_backend_type == LLMBackendType.OLLAMA else "llama.cpp"
            yield f"data: {json.dumps({'error': f'Cannot connect to {backend_name} at {settings.llm_backend_url}. Is it running?'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


# ── Non-Streaming Chat ──
async def get_chat_response(
    messages: list[Message],
    settings: Settings
) -> str:
    """Get full response from LLM backend"""
    
    api_messages = [
        {"role": "system", "content": settings.resolved_system_prompt},
        *[{"role": m.role, "content": m.content} for m in messages]
    ]
    
    payload = {
        "model": settings.llm_model,
        "messages": api_messages,
        "stream": False,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
        "top_p": settings.top_p,
        "repeat_penalty": settings.repeat_penalty,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                settings.chat_completions_url,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.ConnectError:
            backend_name = "Ollama" if settings.llm_backend_type == LLMBackendType.OLLAMA else "llama.cpp"
            raise HTTPException(
                status_code=503,
                detail=f"Cannot connect to {backend_name} at {settings.llm_backend_url}. Is it running?"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# ── Endpoints ──
@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/chat")
async def chat(
    request: ChatRequest,
    _: bool = Depends(verify_api_key),
    settings: Settings = Depends(get_settings)
):
    if request.stream:
        return StreamingResponse(
            stream_chat_response(request.messages, settings),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    else:
        content = await get_chat_response(request.messages, settings)
        return {"content": content}


@app.get("/models")
async def list_models(
    _: bool = Depends(verify_api_key),
    settings: Settings = Depends(get_settings)
):
    """List available models from the LLM backend"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(settings.models_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
async def get_config(
    _: bool = Depends(verify_api_key),
    settings: Settings = Depends(get_settings)
):
    """Get current LLM backend configuration (non-sensitive)"""
    return {
        "backend_type": settings.llm_backend_type.value,
        "model": settings.llm_model,
        "backend_url": settings.llm_backend_url,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
