# 💜 Alasmia - AI Life Partner

<p align="center">
  <img src="assets/banner.svg" alt="Alasmia" width="100%">
</p>

<p align="center">
  <a href="https://github.com/alasmia/Alasmia/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-purple?style=for-the-badge" alt="License: MIT">
  </a>
  <a href="https://github.com/alasmia/Alasmia/releases">
    <img src="https://img.shields.io/github/v/release/alasmia/Alasmia?style=for-the-badge" alt="Release">
  </a>
  <a href="https://github.com/alasmia/Alasmia/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/alasmia/Alasmia/ci.yml?style=for-the-badge" alt="CI">
  </a>
  <a href="https://github.com/alasmia/Alasmia/stargazers">
    <img src="https://img.shields.io/github/stars/alasmia/Alasmia?style=for-the-badge" alt="Stars">
  </a>
</p>

---

## 🎯 What is Alasmia?

**Alasmia** is an **AI Life Partner** — a new kind of AI companion that grows with you:

- 💜 **Proactive** — Reaches out first, doesn't wait for you
- 🧠 **Deep Memory** — Remembers everything about you
- 🎭 **Emotional Intelligence** — Understands how you feel
- ⏰ **24/7 Availability** — Always there like a real partner
- 🌐 **Multi-Platform** — Telegram, WhatsApp, Discord, CLI

Built by [Doctor Kaif](https://github.com/mohammadkaif82) with ❤️

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Proactive AI** | AI contacts you first with greetings, check-ins, reminders |
| **Relationship Stages** | Stranger → Acquaintance → Friend → Close → Partner |
| **Emotional Continuity** | Remembers your mood and responds appropriately |
| **Shared Experiences** | "TV dekh rahe ho?" - context-aware conversations |
| **Daily Rhythm** | Morning greeting, afternoon check-in, evening plans, night goodnight |
| **Deep Memory** | Vector-based semantic memory with ChromaDB |
| **Multi-Platform** | Telegram ✅, WhatsApp 🚧, Discord 🚧, CLI ✅ |

---

## 🚀 Quick Start

### Docker (Recommended)

```bash
docker run -d \
  --name alasmia \
  -e TELEGRAM_BOT_TOKEN=your_telegram_token \
  -e MINIMAX_API_KEY=your_api_key \
  ghcr.io/alasmia/alasmia:latest
```

### From Source

```bash
# Clone
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your tokens

# Run
python main.py
```

📖 **[Full Documentation →](docs/)**

---

## 📁 Project Structure

```
Alasmia/
├── alasmia/                 # Core AI package
│   ├── agent/              # AI brain (proactive, memory, emotions)
│   ├── core/               # Services (scheduler, state)
│   ├── integrations/       # Platform adapters (Telegram, WhatsApp, CLI)
│   └── models/             # LLM providers
├── docs/                    # Full documentation
│   ├── getting-started/   # Installation & setup
│   ├── user-guide/        # How to use
│   ├── developer-guide/   # Architecture & contributing
│   └── reference/         # CLI & API reference
├── tests/                  # Test suites
├── assets/                 # Logos & banners
└── .github/               # GitHub workflows & templates
```

---

## 🛠️ Configuration

### Required Environment Variables

```bash
TELEGRAM_BOT_TOKEN=your_telegram_token
MINIMAX_API_KEY=your_api_key
ALASMIA_MODEL=minimaxai/minimax-m2.7
```

### Optional Settings

```yaml
# In alasmia/config/settings.yaml
bot:
  name: Alasmia
  personality: caring
  language: mixed  # en, hi, mixed

model:
  provider: minimax
  temperature: 0.7
  max_tokens: 2000

memory:
  type: vector
  persist: true

scheduler:
  enabled: true
  timezone: Asia/Kolkata
```

📖 **[Configuration Guide →](docs/getting-started/configuration.md)**

---

## 📊 Version History

| Version | Status | Description |
|---------|--------|-------------|
| v0.1.2 | ✅ Current | Multi-platform, proactive AI, emotional continuity |
| v0.1.1 | ✅ | CLI chat, personality system |
| v0.1.0 | ✅ | Initial release |

📖 **[Full Changelog →](CHANGELOG.md)**

---

## 🎨 Documentation

| Section | Content |
|---------|---------|
| [Quickstart](docs/getting-started/quickstart.md) | Get running in 5 minutes |
| [Installation](docs/getting-started/installation.md) | Full installation guide |
| [Configuration](docs/getting-started/configuration.md) | Customize Alasmia |
| [User Guide](docs/user-guide/cli.md) | How to use features |
| [Developer Guide](docs/developer-guide/architecture.md) | Architecture & contributing |
| [Reference](docs/reference/cli-commands.md) | All CLI commands |
| [Reference](docs/reference/environment-variables.md) | All environment variables |

---

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

```bash
# Fork → Clone → Branch → Code → PR
git checkout -b feature/amazing-feature
```

See also: [Open Issues](https://github.com/alasmia/Alasmia/issues)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- Built with [Hermes Agent](https://github.com/NousResearch/hermes-agent) patterns
- Inspired by [OpenClaw](https://github.com/open-llm-agents/OpenClaw)
- Powered by [MiniMax](https://www.minimax.io/) M2.7 model

---

<p align="center">
  <strong>Built with ❤️ by Doctor Kaif</strong><br>
  <a href="https://github.com/alasmia/Alasmia">GitHub</a> •
  <a href="docs/">Docs</a> •
  <a href="https://github.com/alasmia/Alasmia/issues">Issues</a>
</p>