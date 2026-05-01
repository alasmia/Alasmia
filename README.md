# 🤖 Alasmia - 100% CPU-Based AI Companion

> Your personal AI companion that grows with every conversation. No GPU required.

## Features

- 💬 **Natural Conversations** - Chat like a real friend
- 🧠 **Memory System** - Remembers details about you across sessions  
- ⭐ **Trust Levels** - Relationship grows as you talk more
- 🛠️ **Skills Automation** - Calculator, file ops, code execution, web search
- 📱 **Telegram Bot** - Talk to Alasmia anywhere via @Alasmiabot
- 🖥️ **100% CPU** - No GPU required, runs on any server

## Requirements

- Ubuntu 20.04+ / Debian
- Python 3.10+
- 16GB+ RAM (for 14B model)
- Telegram Bot Token (from @BotFather)

## Quick Setup

```bash
# 1. Clone the repo
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# 2. Install dependencies
pip install aiohttp python-telegram-bot pyyaml sqlite3

# 3. Download Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:14b

# 4. Configure
# Edit config/config.yaml and add your Telegram bot token
nano config/config.yaml

# 5. Run
python3 alasmia-core/__main__.py
```

## Systemd Service (Recommended)

```bash
# Copy service file
sudo cp alasmia.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable alasmia ollama
sudo systemctl start ollama alasmia
```

## Trust Levels

| Level | Conversations | Access |
|-------|---------------|--------|
| Stranger | 0-50 | Basic chat |
| Acquaintance | 50-200 | +File reading |
| Friend | 200-500 | +Code execution |
| Close | 500-1000 | +Email access |
| Partner | 1000+ | Full access |

## Project Structure

```
alasmia/
├── alasmia-core/          # Main bot code
│   ├── __main__.py       # Entry point
│   ├── core.py           # Memory & trust engine
│   ├── telegram_bot.py   # Telegram integration
│   └── skills.py         # Task automation
├── config/
│   └── config.yaml       # Configuration
├── skills/               # Custom skills (add yours)
└── run.sh               # Quick launcher
```

## Available Skills

- `calculate 2+2` - Math calculator
- `read /path/to/file` - Read files (trust level 1+)
- `write /path:content` - Write files (trust level 2+)
- `run print('hello')` - Execute code (trust level 2+)
- `system info` - Server status (trust level 2+)

## License

MIT License - Built with 💜 by Alasmia Team
