# Alasmia Setup Guide

A quick guide to get Alasmia running on your system.

## Prerequisites

- Python 3.10 or higher
- Git
- pip or poetry
- An AI model (Ollama, OpenAI, Anthropic, etc.)

## Quick Install (CLI)

```bash
# Clone the repository
git clone https://github.com/alasmia/Alasmia.git
cd Alasmia

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor

# Run Alasmia
python main.py
```

## Platform Setup

### Telegram Bot

1. Open Telegram and chat with [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow the prompts and get your bot token
4. Add token to `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
5. Run: `python -m alasmia.integrations.telegram_bot`

### WhatsApp Integration

1. Create a Meta Business account at [business.facebook.com](https://business.facebook.com)
2. Create a WhatsApp Business app
3. Get your Phone Number ID and Access Token
4. Add to `.env`:
   ```
   WHATSAPP_TOKEN=your_token
   WHATSAPP_PHONE_ID=your_phone_id
   WHATSAPP_WEBHOOK_VERIFY=your_secret_token
   ```
5. Run: `python -m alasmia.integrations.whatsapp_bot`

## AI Model Setup

### Ollama (Recommended - Local)

1. Install Ollama: [ollama.ai](https://ollama.ai)
2. Pull a model:
   ```bash
   ollama pull qwen2.5:14b
   ```
3. Add to `.env`:
   ```
   MODEL_PROVIDER=ollama
   MODEL_NAME=qwen2.5:14b
   OLLAMA_URL=http://localhost:11434
   ```

### OpenAI

1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to `.env`:
   ```
   MODEL_PROVIDER=openai
   MODEL_NAME=gpt-4
   OPENAI_API_KEY=sk-your-key
   ```

### Anthropic

1. Get API key from [anthropic.com](https://anthropic.com)
2. Add to `.env`:
   ```
   MODEL_PROVIDER=anthropic
   MODEL_NAME=claude-3-opus
   ANTHROPIC_API_KEY=sk-ant-your-key
   ```

## First Run

When you first run Alasmia:

1. **Choose Companion** — Alas (male energy) or Mia (female energy)
2. **Start Chatting** — Type in any language, AI will understand!

```
$ python main.py

🤍 Alasmia - Your AI Life Partner

Choose your companion:
👨 ALAS - Male energy (strong, supportive)
👩 MIA - Female energy (warm, nurturing)

Enter choice: Mia

Hello! I'm Mia, your AI companion. 
What's your name? Raj

Nice to meet you, Raj! 😊 How are you today?

You: 
```

## Troubleshooting

### Import Errors

```bash
pip install -r requirements.txt
```

### Model Not Found

```bash
# For Ollama
ollama pull qwen2.5:14b
```

### Connection Issues

- Check your `.env` settings
- Verify Ollama is running: `curl http://localhost:11434`
- Check firewall settings

## Getting Help

- **GitHub Issues:** https://github.com/alasmia/Alasmia/issues
- **Discord:** https://discord.gg/alasmia
- **Docs:** https://docs.alasmia.ai

## Updating

```bash
cd Alasmia
git pull origin main
pip install -r requirements.txt
```

---

**Need more details?** Check [README.md](README.md) or [VISION.md](VISION.md).
