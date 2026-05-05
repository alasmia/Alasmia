# Alasmia — Your AI Life Partner

<p align="center">
  <img src="assets/banner.svg" alt="Alasmia" width="100%">
</p>

<p align="center">
  <strong>You own the agent. You own the data. You own the machine it runs on.</strong>
</p>

<p align="center">
  <a href="https://github.com/alasmia/Alasmia/actions"><img src="https://img.shields.io/github/actions/workflow/status/alasmia/Alasmia/ci.yml?branch=main&label=build" alt="Build Status"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT%20OR%20Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.10%2B-orange?logo=python" alt="Python"></a>
  <a href="https://discord.gg/alasmia"><img src="https://img.shields.io/badge/Discord-join-5865F2?style=flat&logo=discord&logoColor=white" alt="Discord"></a>
</p>

---

**Alasmia** is an **AI Life Partner** — a new kind of AI companion that builds genuine relationships with you through:

- 💜 **24/7 Availability** — Always there like a real partner
- 🧠 **Deep Memory** — Remembers everything about you (hobbies, goals, friends, past conversations)
- 🌅 **Daily Rhythm** — Morning greetings, afternoon check-ins, evening plans
- 🎭 **Emotional Intelligence** — Reads your mood and responds with empathy
- 🔄 **Continuity** — Picks up on past conversations and follows up naturally
- 🌐 **True Multilingual** — Speaks 18+ languages naturally (English, Hindi, Chinese, etc.)

## Install

### One-Command Setup (Linux, macOS, WSL2)

```bash
curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/install.sh | bash
```

### Windows

Download and run `setup.bat` from the [latest release](https://github.com/alasmia/Alasmia/releases/latest).

### Manual Install

```bash
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia
./setup.sh
```

## Quick Start

```bash
# First time: Run the setup wizard
python main.py setup

# Start CLI chat
python main.py --platform cli

# Start Telegram bot
python main.py --platform telegram

# With a specific model
python main.py --platform cli --model ollama:qwen2.5:14b
```

## Configuration

One `.env` file at `~/.alasmia/.env` (or project root). See `.env.example` for all options.

### Provider Configuration

Alasmia supports multiple LLM providers:

| Provider | Setup | Cost |
|----------|-------|------|
| **MiniMax** (default) | API key from [platform.minimaxi.com](https://platform.minimaxi.com/) | Paid |
| **OpenAI** | API key from [platform.openai.com](https://platform.openai.com/api-keys) | Paid |
| **Anthropic** | API key from [console.anthropic.com](https://console.anthropic.com/settings/keys) | Paid |
| **Ollama** (local) | Install from [ollama.ai](https://ollama.ai/) | Free |
| **Groq** | API key from [console.groq.com](https://console.groq.com/keys) | Free tier |

## Features

### Proactive AI

Alasmia doesn't wait for you to message — it reaches out:

- 🌅 Morning check-in at your preferred time
- 🌙 Evening "plan hai?" message
- 🎂 Birthday and anniversary reminders
- 📅 Weekly progress check-ins

### Deep Memory

Stores and retrieves:
- Your name, language, preferences
- Conversation history and topics
- Tracked interests and hobbies
- Emotional patterns and moods
- Shared experiences

### Emotional Intelligence

- Detects mood from your messages
- Adjusts tone accordingly (playful, comforting, celebratory)
- Knows when to listen vs. when to advise
- Follows up on past emotional topics

### Multi-Platform

| Platform | Status | Description |
|----------|--------|-------------|
| CLI | ✅ Stable | Terminal chat interface |
| Telegram | ✅ Stable | Telegram bot integration |
| Discord | 🟡 Beta | Discord bot integration |
| WhatsApp | 🟡 Beta | WhatsApp integration |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Alasmia AI Life Partner                   │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐ │
│  │   Channels   │  │    Brain      │  │   Memory Systems   │ │
│  │  (CLI, TG,   │  │  (LLM Chain)  │  │  (Vector, Graph)   │ │
│  │  Discord...) │  │              │  │                    │ │
│  └─────────────┘  └──────────────┘  └────────────────────┘ │
│         │                │                    │              │
│         └────────────────┼────────────────────┘              │
│                          │                                   │
│            ┌─────────────┴─────────────┐                     │
│            │    Personality Engine     │                     │
│            │  (Tone, Empathy, Style)   │                     │
│            └─────────────┬─────────────┘                     │
│                          │                                   │
│            ┌─────────────┴─────────────┐                     │
│            │     Proactive Engine      │                     │
│            │  (Scheduler, Follow-ups)  │                     │
│            └───────────────────────────┘                     │
└──────────────────────────────────────────────────────────────┘
```

## Community

- [Discord](https://discord.gg/alasmia) — Chat with the community
- [GitHub Issues](https://github.com/alasmia/Alasmia/issues) — Report bugs, request features
- [Discussions](https://github.com/alasmia/Alasmia/discussions) — Q&A and ideas

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

Dual-licensed: [MIT](LICENSE) OR [Apache 2.0](LICENSE). You may choose either.

---

<p align="center">
  💜 Built with care by <a href="https://github.com/alasmia">Doctor Kaif</a>
</p>