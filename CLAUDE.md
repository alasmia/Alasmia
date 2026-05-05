# CLAUDE.md — Alasmia

Instructions for AI coding assistants (Claude Code, etc.) working on this repository.

## Project Overview

Alasmia is a Python-based AI Life Partner — an autonomous companion that builds genuine relationships through memory, proactive engagement, and emotional intelligence.

## Key Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python main.py setup

# Start CLI chat
python main.py --platform cli

# Syntax check
python -m py_compile alasmia/**/*.py
```

## Architecture

```
alasmia/
├── agent/          # AI brain (brain, memory, personality, mood, emotion)
├── core/            # State, scheduling, analytics
├── integrations/    # Platform adapters (CLI, Telegram, Discord, WhatsApp)
└── models/          # LLM provider abstraction
```

## Important Rules

1. **Never commit secrets** — .env files, API keys, tokens
2. **One concern per PR** — avoid mixed feature+refactor patches
3. **Validate changes** — run `python -m py_compile` on modified files
4. **Respect memory** — user data belongs to the user, never expose it
5. **Async-first** — use asyncio for I/O operations

## File Responsibilities

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point |
| `onboard.py` | Interactive setup wizard |
| `alasmia/agent/brain.py` | LLM orchestration |
| `alasmia/integrations/*.py` | Platform channels |
| `.env` | Secrets (never commit) |

## Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py setup
```

## Extension Points

- **New provider**: Add to `alasmia/models/model_loader.py`
- **New channel**: Add to `alasmia/integrations/`
- **New AI feature**: Add to `alasmia/agent/`

## No-Go Zones

- Never modify `AGENTS.md` without understanding its purpose
- Never add dependencies without checking `requirements.txt`
- Never commit anything with real credentials