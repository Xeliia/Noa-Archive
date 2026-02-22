# Frontend — Noa Chat UI

Messenger-style chat interface built with Svelte 5, Tailwind CSS 4, and DaisyUI 5. Features a Nord color theme with light/dark mode.

## Stack

- **Svelte 5** — runes-based reactivity (`$state`, `$derived`)
- **Vite 6** — dev server & build
- **Tailwind CSS 4** — CSS-first config via `@theme`
- **DaisyUI 5** — component utility classes
- **Lucide Svelte** — icons

## Getting Started

```bash
npm install
npm run dev
```

Open http://localhost:5173

## Build

```bash
npm run build
npm run preview
```

## Configuration

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
VITE_API_KEY=changeme
```

`VITE_API_KEY` must match the `API_KEY` in the root `.env`.

## Project Structure

```
frontend/
├── index.html
├── vite.config.js
├── postcss.config.js
├── package.json
├── .env                # API URL + key
└── src/
    ├── main.js         # Svelte mount
    ├── app.css         # Nord theme, animations, dark mode
    ├── App.svelte      # Chat UI (all logic)
    └── assets/
        ├── mini-profile.png    # Noa avatar
        ├── mini-profile2.png   # Noa avatar (back)
        ├── cover-photo.jpg     # Character card cover
        └── momochat.ico        # Favicon
```

## UI Features

- **Progressive streaming** — paragraphs appear as separate bubbles in real-time
- **Stop button** — cancel generation mid-response with in-character interruption
- **Typing indicator** — bouncing dots while Noa is generating
- **Character card** — flippable avatar, cover photo with 3D tilt effect, birthday badge
- **Project info card** — tech stack, credits, links
- **Theme toggle** — Nord light/dark mode
- **Message presets** — randomized greeting messages on load/clear
- **Auto-resize textarea** — grows with input, submits on Enter
