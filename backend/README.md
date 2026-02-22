# Backend — FastAPI Chat Server

FastAPI backend that proxies chat requests to a local LLM (Ollama or llama.cpp) via the OpenAI-compatible API format.

## Setup

```bash
# From project root
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

## Running

```bash
cd backend
python run.py
```

Server starts at `http://localhost:8000` with CORS enabled for the frontend.

## Configuration

All settings are loaded from the root `.env` file via pydantic-settings. See the root README for the full list.

Key settings:

| Env Variable | Default | Description |
|---|---|---|
| `LLM_BACKEND_TYPE` | `ollama` | `ollama` or `llamacpp` |
| `LLM_BACKEND_URL` | `http://localhost:11434` | LLM server address |
| `LLM_MODEL` | `llama3.2` | Model name |
| `API_KEY` | `changeme` | Bearer token for auth |
| `SYSTEM_PROMPT` | `noa.txt` | Prompt file in `prompts/` or inline text |
| `TEMPERATURE` | `0.8` | Sampling temperature |
| `MAX_TOKENS` | `512` | Max response tokens |
| `TOP_P` | `0.9` | Nucleus sampling |
| `REPEAT_PENALTY` | `1.1` | Repetition penalty |

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/chat` | POST | Bearer | Chat with streaming SSE |
| `/models` | GET | Bearer | List available models |
| `/config` | GET | Bearer | Current config (safe fields) |

### Chat Request

```json
POST /chat
Authorization: Bearer your-api-key
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": true
}
```

Response is a Server-Sent Events stream with `data: {"content": "..."}` chunks.

## Character Prompts

Place `.txt` files in the `prompts/` folder, then set `SYSTEM_PROMPT=filename.txt` in `.env`.

The prompt file is loaded at startup via the `resolved_system_prompt` property in `config.py`.

## LLM Backend Setup

### Ollama
```bash
ollama pull llama3.2
ollama serve   # Default port 11434
```

### llama.cpp
```bash
./llama-server -m model.gguf --port 8080
# Set LLM_BACKEND_TYPE=llamacpp and LLM_BACKEND_URL=http://localhost:8080
```
