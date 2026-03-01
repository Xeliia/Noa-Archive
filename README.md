# Noa's Archive — AI Chatbot

In partial fulfillment on **CS321L-M / CS322-M Artificial Intelligence**.  
A roleplay chatbot featuring **Ushio Noa** from Blue Archive — but in this setting, she's the **Student Council President of South City Homes Academy (SCHA)**, serving as your personal guide for onboarding with the school.  
Chat with Noa through a polished messenger-style UI powered by your choice of LLM backend.

![Svelte](https://img.shields.io/badge/Svelte_5-FF3E00?logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS_4-06B6D4?logo=tailwindcss&logoColor=white)
![DaisyUI](https://img.shields.io/badge/DaisyUI_5-5A0EF8?logo=daisyui&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?logo=ollama&logoColor=white)
![llama.cpp](https://img.shields.io/badge/llama.cpp-2C2C2C?logo=cplusplus&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=googlegemini&logoColor=white)
![ChatGPT](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.10+-3776AB?logo=python&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js_18+-5FA04E?logo=nodedotjs&logoColor=white)
![Vite](https://img.shields.io/badge/Vite_6-646CFF?logo=vite&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic_v2-E92063?logo=pydantic&logoColor=white)

## Features

- **Character roleplay** — Noa's personality, speech patterns, and mannerisms are driven by a detailed system prompt file
- **5 swappable LLM backends** — Ollama, llama.cpp, Google Gemini, OpenAI, or any OpenAI-compatible API (OpenRouter, Together, etc.)
- **Progressive streaming** — Responses appear paragraph-by-paragraph as separate chat bubbles
- **Stop & interrupt** — Cancel generation mid-response; Noa reacts in-character
- **Nord theme** — Clean light/dark mode toggle with smooth transitions
- **Character card** — Flippable avatar with cover photo and info
- **Project info card** — Tech stack, credits, and links
- **Chat history** — Conversations saved in localStorage, loadable from a side panel
- **Configurable via `.env`** — Model, backend, API key, generation params, prompt file — all in one place

## Project Structure

```
Simple-chatbot/
├── .env                    # ⚠️ Root config (backend reads this)
├── .env.example            # Template — copy to .env
├── requirements.txt        # Python dependencies
├── backend/
│   ├── run.py              # Entry point (uvicorn with hot reload)
│   ├── main.py             # FastAPI app — /chat, /models, /health, /config
│   ├── config.py           # Pydantic settings — loads .env, resolves defaults
│   └── prompts/
│       ├── noa.txt         # Original Noa character prompt
│       └── *.txt           # Add your own prompt files here
└── frontend/
    ├── .env                # ⚠️ Frontend config (API URL + key)
    ├── .env.example        # Template — copy to .env
    ├── package.json        # Node dependencies
    ├── vite.config.js      # Vite config
    ├── postcss.config.js   # PostCSS (Tailwind)
    └── src/
        ├── main.js         # Svelte mount point
        ├── app.svelte      # Main chat UI — all state & logic
        ├── app.css         # Nord theme, dark mode, animations
        └── lib/
            ├── assets/     # Avatar images, cover photo, favicon
            └── components/ # ChatHeader, ChatMessage, ChatInput,
                            # RichMessage, TypingIndicator, CharacterCard,
                            # ProjectCard, HistoryPanel, Lightbox
```

## Quick Start

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- One of the following LLM backends:
  - [Ollama](https://ollama.com/) (local, easiest setup)
  - [llama.cpp](https://github.com/ggerganov/llama.cpp) (local, for AMD/ROCm)
  - [Google Gemini API key](https://aistudio.google.com/apikey) (cloud)
  - [OpenAI API key](https://platform.openai.com/api-keys) (cloud)
  - Any OpenAI-compatible API (OpenRouter, Together, etc.)

---

### ⚠️ IMPORTANT: Set Up Your `.env` Files First

This project requires **two `.env` files** — one for the backend (root) and one for the frontend. **The app will not work without them.**

#### 1. Root `.env` (backend configuration)

```bash
cp .env.example .env
```

Edit `.env` and set your LLM backend, model, and API keys. See [Configuration](#configuration) below.

#### 2. Frontend `.env`

```bash
cp frontend/.env.example frontend/.env
```

Edit `frontend/.env` and make sure `VITE_API_KEY` matches the `API_KEY` in your root `.env`.

---

### 2. Backend

```bash
python -m venv .venv
.venv\Scripts\activate.ps1       # Windows PowerShell
# source .venv/bin/activate      # Linux / Mac

pip install -r requirements.txt
cd backend
python run.py
```

Backend starts at `http://localhost:8000`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend starts at `http://localhost:5173`.

### 4. Pull a model (if using Ollama)

```bash
ollama pull llama3.2        # 3B — needs ~3 GB VRAM
# or for low VRAM:
ollama pull llama3.2:1b     # 1B — fits ~2 GB VRAM
```

## Configuration

### Root `.env` — Backend Settings

All backend config lives in the root `.env` file. The backend reads it via Pydantic Settings.

```env
# === LLM Backend ===
LLM_BACKEND_TYPE=ollama                # ollama | llamacpp | gemini | openai | openai_compatible
# LLM_BACKEND_URL=http://localhost:11434 # Auto-detected per backend type
# LLM_MODEL=llama3.2                     # Auto-detected per backend type

# === Cloud API Key (gemini / openai / openai_compatible only) ===
# LLM_API_KEY=your-api-key-here

# === API Security (for this chatbot server) ===
API_KEY=changeme                       # Must match VITE_API_KEY in frontend/.env

# === Character Prompt ===
SYSTEM_PROMPT=noa.txt                  # Filename in backend/prompts/ OR inline text

# === Generation Parameters ===
TEMPERATURE=0.8
MAX_TOKENS=512
TOP_P=0.9
REPEAT_PENALTY=1.1                     # Local backends only (ollama/llamacpp)
# FREQUENCY_PENALTY=0.0                # Cloud backends only
# PRESENCE_PENALTY=0.0                 # Cloud backends only
```

### `frontend/.env` — Frontend Settings

```env
VITE_API_URL=http://localhost:8000     # Where the backend is running
VITE_API_KEY=changeme                  # Must match API_KEY in root .env
```

> **Tip:** The frontend `.env` becomes important when exposing your backend via ngrok or hosting remotely — update `VITE_API_URL` to your tunnel/public URL and ensure the backend's CORS (`FRONTEND_URL` in root `.env`) allows it.

### Backend Defaults by Type

| Backend | Default URL | Default Model |
|---------|-------------|---------------|
| `ollama` | `http://localhost:11434` | `llama3.2` |
| `llamacpp` | `http://localhost:8080` | `local-model` |
| `gemini` | `https://generativelanguage.googleapis.com/v1beta/openai` | `gemini-2.0-flash` |
| `openai` | `https://api.openai.com/v1` | `gpt-4o-mini` |
| `openai_compatible` | `http://localhost:8080` | `default` |

## Remote LLM (LAN Setup)

Run Ollama on a more powerful machine and point the backend at it:

```env
LLM_BACKEND_URL=http://192.168.x.x:11434
```

## Credits

- Character © NEXON Games / Blue Archive
- UI inspired by modern messenger apps
