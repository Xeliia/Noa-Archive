# Character Prompts

This folder contains system prompts for different characters. The backend will load the prompt specified in `SYSTEM_PROMPT` in your `.env` file.

## Usage

Set in your `.env`:
```
SYSTEM_PROMPT=noa.txt
```

## Creating Your Own Character

1. Create a new `.txt` file in this folder (e.g., `mycharacter.txt`)
2. Follow this structure for best results with weak models:

```
You are [Character Name], [brief description]. You are chatting with [User Role].

## Character
- Key trait 1
- Key trait 2
- Key trait 3 (keep it concise!)

## Speech Style
- How they talk
- Verbal tics or catchphrases
- Keep responses short (2-4 sentences)

## Example Responses
User: "Hello"
Character: "Example response showing their personality"

Stay in character.
```

## Tips for Weak Models (<7B params)

1. **Keep prompts short** (~300-500 words max)
2. **Use bullet points** instead of paragraphs
3. **Include 1-2 example responses** - this helps small models understand the format
4. **Emphasize brevity** - "Keep responses to 2-3 sentences"
5. **Lower temperature** (0.5-0.7) for more consistent roleplay
6. **Lower max_tokens** (100-200) to prevent rambling

## Available Prompts

- `noa.txt` - Ushio Noa from Blue Archive (default)
