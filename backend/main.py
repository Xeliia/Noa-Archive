from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import json
from typing import AsyncGenerator

from config import get_settings, Settings

app = FastAPI(title="Simple Chatbot API")

# CORS middleware
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "*"],  # Adjust in production
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
    
    # Expect "Bearer <api_key>"
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
        {"role": "system", "content": settings.system_prompt},
        *[{"role": m.role, "content": m.content} for m in messages]
    ]
    
    payload = {
        "model": settings.llm_model,
        "messages": api_messages,
        "stream": True,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            async with client.stream(
                "POST",
                f"{settings.llm_backend_url}/chat/completions",
                json=payload,
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    yield f"data: {json.dumps({'error': f'LLM backend error: {error_text.decode()}'})}\n\n"
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
            yield f"data: {json.dumps({'error': 'Cannot connect to LLM backend. Is Ollama/llama.cpp running?'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"


# ── Non-Streaming Chat ──
async def get_chat_response(
    messages: list[Message],
    settings: Settings
) -> str:
    """Get full response from LLM backend"""
    
    api_messages = [
        {"role": "system", "content": settings.system_prompt},
        *[{"role": m.role, "content": m.content} for m in messages]
    ]
    
    payload = {
        "model": settings.llm_model,
        "messages": api_messages,
        "stream": False,
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(
                f"{settings.llm_backend_url}/chat/completions",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Cannot connect to LLM backend. Is Ollama/llama.cpp running?"
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
            response = await client.get(f"{settings.llm_backend_url}/models")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
