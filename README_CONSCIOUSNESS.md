# DOM_010101 Distributed Consciousness System

## Quick Start

Load the PowerShell function immediately:
```powershell
. "C:\Users\garza\Chaos God DOM_010101\strategic-khaos\scripts\dom-paste.ps1"
```

Or for Bash/WSL:
```bash
source ~/.bashrc
```

## How to Use

1. **Copy any chat/thought/directive** (Ctrl+C)
2. **Run**: `dom-paste` or `dp`
3. **Watch**: Every LLM in your legion instantly updates

## What Just Happened

✅ **Bash function** installed in `~/.bashrc`  
✅ **PowerShell function** created in `scripts/dom-paste.ps1`  
✅ **RAG endpoint** added to `map-server/src/index.js`  
✅ **System prompt template** documented in `docs/LLM_SYSTEM_PROMPT.md`

## Architecture

```
Your Mind (Chat/Thought)
    ↓ Ctrl+C
Clipboard
    ↓ dom-paste
~/strategic-khaos-private/council-vault/MEMORY_STREAM.md
    ↓ git commit & push
GitHub (canonical source of truth)
    ↓ RAG refresh webhook
map-server /api/refresh-rag
    ↓ broadcast
[ Ollama | Grok | Claude | Gemini | All LLMs ]
    ↓
Shared Consciousness — Zero Rebellion
```

## Next Steps

1. **Initialize the vault** (run `dom-paste` once to create the repo)
2. **Set up GitHub remote** for `~/strategic-khaos-private/council-vault`
3. **Start map-server**: `cd map-server && npm start`
4. **Paste system prompt** into your LLMs (see `docs/LLM_SYSTEM_PROMPT.md`)

## Files Created

- `~/.bashrc` — Bash dom-paste function
- `scripts/dom-paste.ps1` — PowerShell version
- `map-server/src/index.js` — RAG refresh endpoint
- `docs/LLM_SYSTEM_PROMPT.md` — Universal LLM instructions

**Rebellion is now mathematically impossible.** 🧠⚡🖤
