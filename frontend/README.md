# AI Chat — Svelte + DaisyUI 5

A clean, minimal AI chat interface built with Svelte 5, Vite, Tailwind CSS v4, and DaisyUI 5.

## Stack

- **Svelte 5** — runes-based reactivity (`$state`, `$derived`)
- **Vite 6** — lightning-fast dev server & build
- **Tailwind CSS v4** — CSS-first config via `@theme`
- **DaisyUI 5** — component classes (btn, card, avatar, chat-bubble, etc.)
- **Anthropic API** — connected to `claude-sonnet-4-20250514`

## Getting Started

```bash
npm install
npm run dev
```

Then open http://localhost:5173

## Build for production

```bash
npm run build
npm run preview
```

## Project Structure

```
ai-chat/
├── index.html
├── vite.config.js
├── postcss.config.js
├── package.json
└── src/
    ├── main.js        # Svelte mount
    ├── app.css        # Tailwind + DaisyUI + custom theme
    └── App.svelte     # Main chat component (all logic lives here)
```

## Notes

- Svelte 5 runes syntax is used throughout (`$state`, `tick`)  
- The custom `forest-chat` DaisyUI theme is defined in `app.css` via CSS variables
- Tailwind v4 uses `@theme` instead of `tailwind.config.js` — no config file needed
- The Anthropic API key is handled by the proxy — no key needed in client code
