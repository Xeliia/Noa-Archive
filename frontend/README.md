# Frontend — Noa Chat UI

Messenger-style chat interface built with **Svelte 5**, **Tailwind CSS 4**, and **DaisyUI 5**. Features a Nord color theme with smooth light/dark mode transitions.

## Stack

- **Svelte 5** — runes-based reactivity (`$state`, `$derived`, `$props`)
- **Vite 6** — dev server & build
- **Tailwind CSS 4** — CSS-first config via `@theme` and `@plugin`
- **DaisyUI 5** — component utility classes
- **Lucide Svelte** — icons
- **PostCSS** — via `@tailwindcss/postcss`

## ⚠️ Configure `.env` First

The frontend needs a `.env` file to know where the backend is and what API key to use.  
**You must create it before running** — otherwise the defaults (`localhost:8000` / `changeme`) are used.

```bash
cp .env.example .env
# Then edit .env with your settings
```

```env
VITE_API_URL=http://localhost:8000   # Backend URL
VITE_API_KEY=changeme                # Must match API_KEY in root .env
```

> **Important:** `VITE_API_KEY` must match the `API_KEY` set in the root `.env` file, otherwise the backend will reject requests with a 401 error.

> **Remote access:** When exposing the backend via ngrok or hosting it remotely, update `VITE_API_URL` to the public URL (e.g., `https://xxxx-xxxx.ngrok-free.app`). Also update `FRONTEND_URL` in the root `.env` so the backend's CORS allows requests from your frontend's origin.

## Getting Started

```bash
npm install
npm run dev
```

Opens at http://localhost:5173

## Build for Production

```bash
npm run build
npm run preview   # Preview the production build locally
```

## Project Structure

```
frontend/
├── index.html              # HTML entry point
├── vite.config.js          # Vite + Svelte plugin
├── postcss.config.js       # PostCSS with @tailwindcss/postcss
├── package.json            # Dependencies & scripts
├── .env                    # ⚠️ API URL + key (create from .env.example)
├── .env.example            # Template — copy to .env
├── public/                 # Static assets (served as-is)
└── src/
    ├── main.js             # Svelte mount point (#app)
    ├── app.svelte          # Main chat UI — all state, logic, and layout
    ├── app.css             # Nord theme (light + dark), animations, scrollbar
    └── lib/
        ├── assets/
        │   ├── mini-profile.png    # Noa avatar (front)
        │   ├── mini-profile2.png   # Noa avatar (back — card flip)
        │   ├── cover-photo.jpg     # Character card cover image
        │   └── momochat.ico        # Favicon
        └── components/
            ├── ChatHeader.svelte       # Name, status, theme toggle, action buttons
            ├── ChatMessage.svelte      # Individual text message bubble
            ├── RichMessage.svelte      # Message with stat cards (icon + label + value)
            ├── ChatInput.svelte        # Auto-resize textarea + send/stop button
            ├── TypingIndicator.svelte  # Bouncing dots while generating
            ├── CharacterCard.svelte    # Flippable avatar card with cover photo + info
            ├── ProjectCard.svelte      # Tech stack, credits, links
            ├── HistoryPanel.svelte     # Saved chat list — load, delete, clear all
            └── Lightbox.svelte         # Full-size image overlay
```

## UI Features

- **Progressive streaming** — paragraphs appear as separate chat bubbles in real-time with natural typing delays
- **Stop button** — cancel generation mid-response; Noa replies with a randomized in-character interruption response
- **Typing indicator** — bouncing dots while Noa is generating
- **Character card** — flippable avatar, cover photo, birthday badge
- **Project info card** — tech stack, credits, links
- **Chat history** — conversations stored in localStorage, loadable from a side panel (up to 50 entries)
- **Theme toggle** — Nord light/dark mode with smooth CSS transitions across all components
- **Message presets** — randomized greeting messages on load and chat clear
- **Auto-resize textarea** — grows with input, submits on Enter
- **Responsive layout** — mobile overlay for side panels, desktop side-by-side
