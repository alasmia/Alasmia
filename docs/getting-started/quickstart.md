# 🚀 Quickstart Guide

Get Alasmia running in 5 minutes!

## Prerequisites

- Python 3.10+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- any OpenAI-compatible API API Key (or any supported LLM)

## Option 1: Docker (Recommended)

```bash
# Pull and run
docker run -d \
  --name alasmia \
  -e TELEGRAM_BOT_TOKEN=your_telegram_token \
  -e ALASMIA_MODEL=your_preferred_model \
  -e any OpenAI-compatible API_API_KEY=your_api_key \
  -v alasmia-data:/data \
  ghcr.io/alasmia/alasmia:latest
```

## Option 2: pip Install

```bash
# Install
pip install alasmia-ai

# Configure
export TELEGRAM_BOT_TOKEN=your_token
export any OpenAI-compatible API_API_KEY=your_key

# Run
alasmia
```

## Option 3: From Source

```bash
# Clone
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Install dependencies
pip install -r requirements.txt

# Copy environment
cp .env.example .env
# Edit .env with your tokens

# Run
python main.py
```

## Verify Installation

Once running, send `/start` to your Telegram bot. Alasmia should respond with a greeting!

## Next Steps

1. [Configure Alasmia](configuration.md) - Customize behavior
2. [Set up Memory](user-guide/memory.md) - Enable deep memory
3. [Explore Commands](user-guide/cli.md) - Learn available commands

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot not responding | Check Telegram token is correct |
| Memory not working | Ensure data directory is persisted |
| Slow responses | Try a faster model |

## Need Help?

- 📖 [Full Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/alasmia/Alasmia/issues)
- 💬 [Community Chat](https://t.me/alasmia_ai)