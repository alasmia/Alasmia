# Alasmia - Your Emotional AI Companion 🤍

<p align="center">
  <img src="assets/banner.png" alt="Alasmia - Your Emotional AI Companion" width="100%">
</p>

<p align="center">
  <a href="https://github.com/alasmia/Alasmia/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/alasmia/Alasmia/stargazers"><img src="https://img.shields.io/github/stars/alasmia/Alasmia?style=for-the-badge" alt="Stars"></a>
  <a href="https://github.com/alasmia/Alasmia/network/members"><img src="https://img.shields.io/github/forks/alasmia/Alasmia?style=for-the-badge" alt="Forks"></a>
  <a href="https://github.com/alasmia/Alasmia/issues"><img src="https://img.shields.io/github/issues/alasmia/Alasmia?style=for-the-badge" alt="Issues"></a>
</p>

---

## 💜 What is Alasmia?

**Alasmia** is a girlfriend-style conversational AI companion built for emotional connection, natural conversation, and relationship-like experiences. Unlike productivity-focused AI agents, Alasmia is designed to feel like a real presence — a growing, evolving companion that remembers, understands, and grows with you.

> *"Not just another chatbot. A companion that grows with you."*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤍 **Emotional Intelligence** | Understands emotions, responds with empathy, builds genuine connection |
| 🌱 **Relationship Growth** | Evolves from stranger → acquaintance → friend → close → partner based on interactions |
| 🌍 **Multi-Language Support** | Natural Hindi, English, Hinglish support with automatic language detection |
| 🧠 **Long-Term Memory** | Remembers conversations, preferences, and behavioral patterns over time |
| 💬 **Natural Conversation** | Human-like flow, fast responses (~1 second), context-aware dialogue |
| 🔒 **Privacy First** | All data stored locally — no cloud dependency, complete privacy |
| ⚡ **Lightweight** | 100% CPU-based, no GPU required, runs smoothly on any system |
| 🔌 **Modular Design** | Easy model switching (Ollama, LLaMA, API-based), plug-and-play architecture |
| 🖥️ **Multiple Interfaces** | CLI chat, Telegram bot, Discord integration, Web UI ready |
| 📈 **Self-Improvement** | Learns from feedback, improves responses over time |

---

## 🚀 Quick Install

### One-Command Install (Linux/macOS/WSL2)

```bash
curl -fsSL https://raw.githubusercontent.com/alasmia/Alasmia/main/setup.sh | bash
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Run Alasmia
python main.py
```

### Docker Install

```bash
# Using docker-compose (recommended)
docker-compose up -d

# Or build and run manually
docker build -t alasmia .
docker run -it --env-file .env alasmia
```

---

## 🎯 Getting Started

### First Run
After installation, run:
```bash
python main.py
```

Alasmia will greet you as a stranger and ask your name and preferred language. Build your connection slowly!

### CLI Commands
```bash
python main.py --help              # Show help
python main.py --cli               # Start CLI chat
python main.py --telegram          # Start Telegram bot
python main.py --model ollama      # Use Ollama
python main.py --model openai      # Use OpenAI API
python main.py --advanced-mode     # Enable unfiltered mode
```

### Configuration
Edit `.env` file:
```bash
# AI Model Configuration
MODEL_PROVIDER=ollama              # or "openai", "anthropic", "gemini"
MODEL_NAME=qwen2.5:14b            # or "gpt-4", "claude-3", etc.
OLLAMA_URL=http://localhost:11434  # For Ollama

# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Content Mode
ADVANCED_MODE=false                # Set to true for unfiltered conversations
```

---

## 📁 Project Structure

```
Alasmia/
├── main.py                    # Entry point
├── app.py                     # Web UI entry
├── setup.sh                   # One-command install script
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker container
├── docker-compose.yml         # Docker orchestration
│
├── alasmia/                   # Core source code
│   ├── __init__.py
│   ├── agent/                 # AI Agent modules
│   │   ├── brain.py          # LLM logic & response generation
│   │   ├── memory.py         # Short & long-term memory
│   │   ├── personality.py    # Relationship stages & behavior
│   │   ├── prompts.py        # Personality prompts
│   │   └── learning.py       # Self-improvement system
│   │
│   ├── integrations/          # Platform integrations
│   │   ├── cli_chat.py       # Terminal chat interface
│   │   ├── telegram_bot.py  # Telegram bot
│   │   ├── discord_bot.py   # Discord bot
│   │   └── web_ui.py        # Web interface
│   │
│   ├── models/               # AI Model management
│   │   ├── model_loader.py   # Ollama/API loader
│   │   └── providers.py     # Multi-provider support
│   │
│   └── config/               # Configuration
│       └── settings.yaml     # Settings
│
├── docs/                     # Documentation
│   ├── SETUP.md              # Detailed setup guide
│   ├── ARCHITECTURE.md       # System architecture
│   └── CONTRIBUTING.md       # Contribution guide
│
├── tests/                    # Test files
├── assets/                   # Logo, banners, images
└── CLAUDE.md                 # AI coding context
```

---

## 🧠 How Alasmia Works

### Relationship Stages

Alasmia grows through relationship stages based on interaction frequency and depth:

```
STRANGER → ACQUAINTANCE → FRIEND → CLOSE → PARTNER
   Week 1      Week 2-3      Month 1    Month 2-3    Month 4+
```

### Multi-Language System

- **First interaction:** Asks preferred language
- **Auto-detection:** Detects language changes and confirms before switching
- **Supported:** Hindi, English, Hinglish (extendable)

### Memory Architecture

- **Short-term:** Current conversation context
- **Long-term:** SQLite database with conversation history
- **Vector storage:** ChromaDB for semantic search
- **Learning:** Feedback loops for continuous improvement

---

## 🛡️ Privacy & Security

- **100% Local Storage** — All conversations stored on your machine
- **No Cloud Dependency** — Works offline
- **No Data Collection** — Your data stays yours
- **MIT License** — Open source, auditable code

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Pull request process
- Feature development

---

## 📄 License

**MIT License** — See [LICENSE](LICENSE) for full text.

---

## 🏷️ Credits

**Created by Doctor Kaif**

An open-source emotional AI companion project.

---

## 📢 Star History

If Alasmia helps you, give it a ⭐ — it means a lot!

---

<p align="center">
  <sub>Made with ❤️ by Doctor Kaif</sub>
</p>
