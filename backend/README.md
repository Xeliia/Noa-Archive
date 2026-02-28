# Backend — FastAPI Chat Server

FastAPI backend that proxies chat requests to any LLM backend (Ollama, llama.cpp, Google Gemini, OpenAI, or any OpenAI-compatible API) via the OpenAI-compatible chat completions format. Supports both streaming (SSE) and non-streaming responses.

## Setup

```bash
# From project root
python -m venv .venv
.venv\Scripts\activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # Linux / Mac

pip install -r requirements.txt
```

## ⚠️ Configure `.env` First

The backend reads **all settings** from the root `.env` file (one level up from this folder).  
**You must create it before running the server** — otherwise defaults are used and cloud backends won't have API keys.

```bash
# From project root
cp .env.example .env
# Then edit .env with your settings
```

See the [root README](../README.md#configuration) for the full list of environment variables.

## Running

```bash
cd backend
python run.py
```

Server starts at `http://localhost:8000` with:
- CORS enabled for the frontend (`FRONTEND_URL` in `.env`, defaults to `http://localhost:5173`)
- Hot reload via uvicorn

## Configuration Reference

All settings are loaded from the root `.env` via `pydantic-settings`. The `config.py` file defines defaults that are used **only when** the corresponding `.env` variable is not set.

| Env Variable | Default | Description |
|---|---|---|
| `LLM_BACKEND_TYPE` | `ollama` | `ollama`, `llamacpp`, `gemini`, `openai`, or `openai_compatible` |
| `LLM_BACKEND_URL` | *(auto per type)* | LLM server address — leave empty to use the default for your backend type |
| `LLM_MODEL` | *(auto per type)* | Model name — leave empty to use the default for your backend type |
| `LLM_API_KEY` | *(none)* | API key for cloud backends (Gemini, OpenAI, OpenAI-compatible) |
| `API_KEY` | `changeme` | Bearer token for authenticating frontend → backend requests |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `FRONTEND_URL` | `http://localhost:5173` | Allowed CORS origin |
| `SYSTEM_PROMPT` | `noa.txt` | Prompt filename in `prompts/` folder, or inline text |
| `TEMPERATURE` | `0.8` | Sampling temperature (0.1–1.5) |
| `MAX_TOKENS` | `512` | Max response length — local backends only |
| `TOP_P` | `0.9` | Nucleus sampling |
| `REPEAT_PENALTY` | `1.1` | Repetition penalty — local backends only (ollama/llamacpp) |
| `FREQUENCY_PENALTY` | `0.0` | Frequency penalty — cloud backends only |
| `PRESENCE_PENALTY` | `0.0` | Presence penalty — cloud backends only |

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check — returns `{"status": "ok"}` |
| `/chat` | POST | Bearer | Chat with the LLM (streaming SSE or full response) |
| `/models` | GET | Bearer | List available models from the LLM backend |
| `/config` | GET | Bearer | Current config (backend type, model, URL — no secrets) |

### POST `/chat`

```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ],
  "stream": true
}
```

**Headers:**
```
Authorization: Bearer your-api-key
Content-Type: application/json
```

**Streaming response** (`stream: true`): Server-Sent Events with `data: {"content": "..."}` chunks, ending with `data: [DONE]`.

**Non-streaming response** (`stream: false`): JSON `{"content": "full response text"}`.

## Character Prompts

Place `.txt` files in the `prompts/` folder, then set `SYSTEM_PROMPT=filename.txt` in `.env`.

The prompt is loaded at startup via the `resolved_system_prompt` property in `config.py`. If the specified file doesn't exist, a hardcoded fallback is used.

**Current prompts:**
- `noa.txt` — Original Noa character (Millennium Science School)
- `assignment_prompt.txt` — Noa as SCHA Student Council President

## LLM Backend Setup

### Ollama (easiest)
```bash
ollama pull llama3.2
ollama serve   # Default port 11434
```

### llama.cpp
```bash
./llama-server -m model.gguf --port 8080
```
```env
LLM_BACKEND_TYPE=llamacpp
LLM_BACKEND_URL=http://localhost:8080
```

### Google Gemini
```env
LLM_BACKEND_TYPE=gemini
LLM_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-2.0-flash
```
Get your key at: https://aistudio.google.com/apikey

### OpenAI
```env
LLM_BACKEND_TYPE=openai
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4o-mini
```

### OpenAI-Compatible (OpenRouter, Together, etc.)
```env
LLM_BACKEND_TYPE=openai_compatible
LLM_BACKEND_URL=https://openrouter.ai/api/v1
LLM_API_KEY=your-api-key
LLM_MODEL=meta-llama/llama-3-8b-instruct
```
