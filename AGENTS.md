# AGENTS.md — Alasmia

Cross-tool agent instructions for any AI coding assistant working on this repository.

## Commands

```bash
# Format check
python -m py_compile alasmia/**/*.py

# Run tests
pytest tests/

# Full pre-PR validation
./dev/ci.sh all
```

## Project Snapshot

Alasmia is a Python-based autonomous AI Life Partner — a companion that builds genuine relationships through memory, proactive engagement, and emotional intelligence.

Core architecture is modular and async-first:

```
alasmia/
├── agent/          # AI brain systems (brain, memory, personality, mood, emotion)
├── core/           # State management, scheduling, analytics
├── integrations/   # Platform adapters (CLI, Telegram, Discord, WhatsApp)
└── models/         # LLM provider abstraction (OpenAI, Anthropic, Ollama, etc.)
```

Key extension points:

- `alasmia/agent/brain.py` — LLM orchestration, prompt management
- `alasmia/models/model_loader.py` — Provider abstraction (`Provider` trait)
- `alasmia/integrations/` — Platform channels (Channel trait)
- `alasmia/agent/memory.py` — Memory and conversation persistence

## Stability Tiers

| Component | Tier | Notes |
|----------|------|-------|
| `core/` | Stable | Core systems |
| `models/` | Beta | LLM abstraction |
| `integrations/cli` | Stable | CLI chat |
| `integrations/telegram` | Stable | Telegram bot |
| `integrations/discord` | Beta | Discord bot |
| `integrations/whatsapp` | Experimental | WhatsApp integration |
| `agent/` | Beta | AI systems |

**Tiers**: Stable = covered by breaking-change policy. Beta = breaking changes permitted in MINOR with changelog notes. Experimental = no stability guarantee.

## Repository Map

```
Alasmia/
├── main.py              # CLI entrypoint and command routing
├── onboard.py           # Interactive setup wizard
├── install.sh           # One-command installer (Unix)
├── setup.bat            # Windows installer
├── .env.example         # Configuration template
│
├── alasmia/
│   ├── agent/           # AI systems
│   │   ├── brain.py          # LLM chain orchestration
│   │   ├── memory.py        # MemoryManager (vector + graph)
│   │   ├── personality.py   # Tone, empathy, style
│   │   ├── mood_handler.py  # Mood detection and response
│   │   ├── emotion_tracker.py
│   │   ├── proactive_engine.py  # Initiates conversations
│   │   ├── interest_tracker.py  # Tracks user interests
│   │   ├── emotional_continuity.py  # Follow-up on emotions
│   │   ├── shared_experiences.py
│   │   ├── milestone.py
│   │   └── alas_prompts.py / mia_prompts.py  # Gender-specific prompts
│   │
│   ├── core/            # Infrastructure
│   │   ├── state_manager.py  # Session state
│   │   ├── scheduler.py      # Proactive message scheduling
│   │   ├── enhanced_scheduler.py
│   │   ├── setup_flow.py     # Configuration helper
│   │   └── analytics.py
│   │
│   ├── integrations/    # Platform channels
│   │   ├── cli_chat.py       # Terminal chat (Rich-based)
│   │   ├── telegram_bot.py   # Telegram bot
│   │   ├── discord_bot.py    # Discord bot
│   │   └── whatsapp_bot.py   # WhatsApp webhook
│   │
│   └── models/
│       └── model_loader.py   # Multi-provider LLM abstraction
│
├── docs/               # Documentation
│   └── book/src/           # MDBook documentation
│
├── tests/              # Test suite
│
└── assets/             # Logos and banners
```

## Workflow

1. **Read before write** — inspect existing module structure before editing
2. **One concern per PR** — avoid mixed feature+refactor patches
3. **Implement minimal patch** — no speculative abstractions
4. **Validate** — run `python -m py_compile` on changed files
5. **Document impact** — update PR notes for behavior, risk, side effects

Branch/commit/PR rules:
- Work from a non-`main` branch. Open a PR to `main`.
- Never commit secrets, personal data, or real API keys.

## Anti-Patterns

- Do not add heavy dependencies for minor convenience
- Do not silently weaken security or access constraints
- Do not add speculative config flags "just in case"
- Do not modify unrelated modules "while here"
- Do not leave `unwrap()` / `expect()` in production paths
- Do not include personal identity or sensitive information in test data

## Environment Setup

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Copy and configure .env
cp .env.example .env
nano .env  # Add your API keys

# Run setup wizard
python main.py setup

# Start
python main.py --platform cli
```

## Key Files

| File | Purpose | Risk |
|------|---------|------|
| `main.py` | Entry point, argument parsing | Medium |
| `onboard.py` | Interactive setup wizard | Low |
| `alasmia/agent/brain.py` | LLM calls, prompt management | High |
| `alasmia/integrations/` | External platform integrations | Medium |
| `.env` | Secrets, never commit | **Critical** |

## Linked References

- `@SETUP.md` — Full installation guide
- `@VISION.md` — Project vision and philosophy
- `@SECURITY.md` — Security policy and best practices