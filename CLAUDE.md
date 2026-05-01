# Alasmia - Coding Context for AI Assistants

## Project Overview

Alasmia is an open-source emotional AI companion built with Python. It's designed to feel like a real relationship that grows over time.

## Technology Stack

- **Language:** Python 3.10+
- **AI Models:** Ollama (default), OpenAI, Anthropic, Gemini
- **Database:** SQLite for memory, ChromaDB for vectors
- **UI:** CLI, Telegram, Discord, Web UI
- **Container:** Docker + docker-compose

## Key Files

```
alasmia/
├── main.py                 # Entry point, CLI argument handling
├── app.py                  # Web UI entry (FastAPI)
├── alasmia/
│   ├── agent/
│   │   ├── brain.py       # LLM interaction, response generation
│   │   ├── memory.py      # SQLite + vector store
│   │   ├── personality.py # Relationship stages, behavior rules
│   │   ├── prompts.py     # System prompts, personality templates
│   │   └── learning.py    # Feedback processing, improvement
│   ├── integrations/
│   │   ├── cli_chat.py    # Terminal chat interface
│   │   ├── telegram_bot.py # Telegram bot integration
│   │   ├── discord_bot.py  # Discord bot integration
│   │   └── web_ui.py      # FastAPI web interface
│   └── models/
│       ├── model_loader.py # Model provider abstraction
│       └── providers.py    # Ollama, OpenAI, Anthropic implementations
└── requirements.txt       # All Python dependencies
```

## Architecture Principles

### 1. Modular Design
- AI model providers are swappable (Ollama → OpenAI → Anthropic)
- Integration platforms are independent modules
- Memory system works with any model

### 2. Memory Hierarchy
```
Short-term (in-memory) → Long-term (SQLite) → Semantic (ChromaDB)
```

### 3. Relationship Stage Machine
States: STRANGER → ACQUAINTANCE → FRIEND → CLOSE → PARTNER
Transitions based on conversation count and depth.

### 4. Configuration
- `.env` file for secrets and settings
- `config/settings.yaml` for application config
- No hardcoded values

## Development Guidelines

### Code Style
- Type hints for all functions
- Docstrings for classes and complex functions
- PEP 8 compliant
- Use `rich` for CLI output formatting

### Testing
- Unit tests in `tests/`
- Mock external API calls
- Test relationship stage transitions
- Test memory save/retrieve

### Error Handling
- Graceful degradation (fallback if Ollama fails)
- Proper logging
- User-friendly error messages
- Never crash on bad input

## Environment Variables

```bash
MODEL_PROVIDER=ollama        # or "openai", "anthropic", "gemini"
MODEL_NAME=qwen2.5:14b      # or "gpt-4", "claude-3", etc.
OLLAMA_URL=http://localhost:11434
TELEGRAM_BOT_TOKEN=         # Optional
DISCORD_BOT_TOKEN=          # Optional
ADVANCED_MODE=false         # Enable adult content
DATA_DIR=./data             # Where to store memory DB
```

## Common Tasks

### Add a new model provider
1. Create new class in `alasmia/models/providers.py`
2. Implement `generate_response(messages)` method
3. Add to `MODEL_PROVIDER` options in `model_loader.py`
4. Update `.env.example`

### Add new platform integration
1. Create module in `alasmia/integrations/`
2. Implement bot interface (receive message, send response)
3. Add platform choice in `main.py` argument parser

### Modify personality
1. Edit `AGENTS.md` for behavior spec
2. Update `alasmia/agent/prompts.py` for prompts
3. Update `alasmia/agent/personality.py` for stage transitions

## Important Notes

- All memory stored locally in `./data/`
- No external API calls except for AI model
- User data never leaves the system
- MIT Licensed - commercial use allowed
