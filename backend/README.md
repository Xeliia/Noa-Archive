# Backend - Simple Chatbot API

FastAPI backend that works with both **Ollama** and **llama.cpp** as LLM providers.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy and configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Configure for your machine**

   **Laptop (Ollama with MX350):**
   ```env
   LLM_BACKEND_URL=http://localhost:11434/v1
   LLM_MODEL=llama3
   ```

   **PC (llama.cpp with RX580):**
   ```env
   LLM_BACKEND_URL=http://localhost:8080/v1
   LLM_MODEL=your-model-name
   ```

## Running

### Local only
```bash
cd backend
python run.py
```

### With ngrok (first time - set auth token)
```bash
python run.py --ngrok-auth YOUR_NGROK_AUTH_TOKEN
```

### With ngrok tunnel
```bash
python run.py --ngrok
```

This will print the public URL. Update your frontend's `API_URL` with it.

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check |
| `/chat` | POST | Yes | Chat with streaming SSE |
| `/models` | GET | Yes | List available models |

### Chat Request Example
```json
POST /chat
Authorization: Bearer your-api-key

{
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": true
}
```

## LLM Backend Setup

### Ollama
```bash
# Install Ollama and pull a model
ollama pull llama3
ollama serve  # Runs on port 11434
```

### llama.cpp
```bash
# Run with OpenAI-compatible API
./llama-server -m your-model.gguf --port 8080
```
