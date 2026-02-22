# Noa — Blue Archive AI Chatbot

A roleplay chatbot featuring **Ushio Noa** from Blue Archive. Chat with Noa through a polished messenger-style UI powered by your local LLM.

![Svelte](https://img.shields.io/badge/Svelte_5-FF3E00?logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS_4-06B6D4?logo=tailwindcss&logoColor=white)
![DaisyUI](https://img.shields.io/badge/DaisyUI_5-5A0EF8?logo=daisyui&logoColor=white)

## Features

- **Character roleplay** — Noa's personality, speech patterns, and mannerisms driven by a detailed prompt file
- **Swappable LLM backends** — Ollama or llama.cpp via OpenAI-compatible API
- **Progressive streaming** — Responses appear paragraph-by-paragraph as chat bubbles
- **Stop & interrupt** — Cancel generation mid-response; Noa reacts in-character
- **Nord theme** — Clean light/dark mode toggle
- **Character card** — Flip avatar, cover photo with 3D tilt, birthday badge
- **Configurable via `.env`** — Model, backend, API key, generation params, prompt file

## Project Structure

```
Simple-chatbot/
├── .env                    # All configuration (backend, model, API key, params)
├── requirements.txt        # Python dependencies
├── backend/
│   ├── run.py              # Entry point (uvicorn)
│   ├── main.py             # FastAPI app, /chat /models /health endpoints
│   ├── config.py           # Pydantic settings, loads .env
│   └── prompts/
│       └── noa.txt         # Noa character prompt
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.svelte      # Main chat UI
        ├── app.css         # Nord theme + animations
        └── assets/         # Profile images, cover photo, favicon
```

## Quick Start

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- **Ollama** (or llama.cpp) running locally

### 1. Clone & configure

```bash
git clone <your-repo-url>
cd Simple-chatbot
cp .env.example .env   # Edit .env with your settings
```

### 2. Backend

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
cd backend
python run.py
```

Backend runs at `http://localhost:8000`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 4. Pull a model

```bash
ollama pull llama3.2        # 3B — needs ~3GB VRAM
# or for low VRAM:
ollama pull llama3.2:1b     # 1B — fits ~2GB VRAM
```

## Configuration

All config lives in the root `.env` file:

```env
# LLM Backend
LLM_BACKEND_TYPE=ollama              # ollama or llamacpp
LLM_BACKEND_URL=http://localhost:11434
LLM_MODEL=llama3.2

# API Key (must match frontend/.env VITE_API_KEY)
API_KEY=changeme

# Character prompt file (from backend/prompts/)
SYSTEM_PROMPT=noa.txt

# Generation parameters
TEMPERATURE=0.8
MAX_TOKENS=512
TOP_P=0.9
REPEAT_PENALTY=1.1
```

Frontend config lives in `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_API_KEY=changeme
```

## Remote LLM (LAN Setup)

Run Ollama on a more powerful machine and point the backend at it:

```env
LLM_BACKEND_URL=http://192.168.x.x:11434
```

## Credits

- Character © NEXON Games / Blue Archive
- UI inspired by modern messenger apps